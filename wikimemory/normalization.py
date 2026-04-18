from __future__ import annotations

import json
import os
import shutil
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator

from .discovery import (
    DiscoveryError,
    SourceRecord,
    atomic_write_text,
    ensure_directory,
    load_registry,
    load_source_roots,
    open_shared_binary,
    utc_now,
)
from .raw_event_resolver import RawEventResolver, compute_event_digest

STATE_SCHEMA_VERSION = 1
PAYLOAD_NONE_KEY = "<none>"
TEXT_SURFACE_KEYS = {
    "aggregated_output",
    "arguments",
    "command",
    "comment",
    "formatted_output",
    "input",
    "message",
    "output",
    "review",
    "stderr",
    "stdout",
    "text",
}
REFERENCE_FIELDS = ("turn_id", "call_id", "thread_id")
MAX_PERSISTED_TEXT_SURFACES = 12
MAX_PERSISTED_TEXT_SURFACE_CHARS = 1024
MAX_PERSISTED_TOTAL_TEXT_SURFACE_CHARS = 4096


class NormalizationError(DiscoveryError):
    """Fatal normalization error that must stop the run."""


@dataclass(frozen=True)
class NormalizationStateRecord:
    source_id: str
    normalization_schema_version: int
    phase1_committed_byte_end: int
    phase1_committed_line_count: int
    phase1_fingerprint_digest: str
    normalized_event_count: int
    status: str
    last_normalized_at: str
    last_run_id: str

    def to_dict(self) -> dict[str, object]:
        return {
            "source_id": self.source_id,
            "normalization_schema_version": self.normalization_schema_version,
            "phase1_committed_byte_end": self.phase1_committed_byte_end,
            "phase1_committed_line_count": self.phase1_committed_line_count,
            "phase1_fingerprint_digest": self.phase1_fingerprint_digest,
            "normalized_event_count": self.normalized_event_count,
            "status": self.status,
            "last_normalized_at": self.last_normalized_at,
            "last_run_id": self.last_run_id,
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "NormalizationStateRecord":
        return cls(
            source_id=str(data["source_id"]),
            normalization_schema_version=int(data["normalization_schema_version"]),
            phase1_committed_byte_end=int(data["phase1_committed_byte_end"]),
            phase1_committed_line_count=int(data["phase1_committed_line_count"]),
            phase1_fingerprint_digest=str(data["phase1_fingerprint_digest"]),
            normalized_event_count=int(data["normalized_event_count"]),
            status=str(data["status"]),
            last_normalized_at=str(data["last_normalized_at"]),
            last_run_id=str(data["last_run_id"]),
        )


@dataclass(frozen=True)
class NormalizationNotice:
    run_id: str
    source_id: str
    severity: str
    notice_type: str
    outer_type: str | None
    payload_type: str | None
    count_in_source: int
    first_seen_event_id: str

    def to_dict(self) -> dict[str, object]:
        return {
            "run_id": self.run_id,
            "source_id": self.source_id,
            "severity": self.severity,
            "notice_type": self.notice_type,
            "outer_type": self.outer_type,
            "payload_type": self.payload_type,
            "count_in_source": self.count_in_source,
            "first_seen_event_id": self.first_seen_event_id,
        }


@dataclass(frozen=True)
class NormalizationRunReport:
    run_id: str
    started_at: str
    finished_at: str
    source_status_counts: dict[str, int]
    normalized_event_count: int
    event_counts_by_outer_type: dict[str, int]
    event_counts_by_payload_type: dict[str, int]
    unknown_signature_summary: dict[str, int]
    success: bool
    fatal_error_summary: str | None

    def to_dict(self) -> dict[str, object]:
        return {
            "run_id": self.run_id,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "source_status_counts": self.source_status_counts,
            "normalized_event_count": self.normalized_event_count,
            "event_counts_by_outer_type": self.event_counts_by_outer_type,
            "event_counts_by_payload_type": self.event_counts_by_payload_type,
            "unknown_signature_summary": self.unknown_signature_summary,
            "success": self.success,
            "fatal_error_summary": self.fatal_error_summary,
        }


@dataclass(frozen=True)
class NormalizationResult:
    report: NormalizationRunReport
    state_path: Path
    run_log_path: Path
    notice_log_path: Path


@dataclass(frozen=True)
class NormalizationCatalog:
    schema_version: int
    normalization_schema_version: int
    known_outer_types: dict[str, dict[str, object]]


@dataclass(frozen=True)
class ProcessedSourceArtifacts:
    session_payload: dict[str, object]
    stats_payload: dict[str, object]
    state_record: NormalizationStateRecord
    notices: list[NormalizationNotice]
    processed_event_count: int
    event_counts_by_outer_type: Counter[str]
    event_counts_by_payload_type: Counter[str]


def run_normalization(
    config_path: Path | str,
    state_dir: Path | str,
    schema_path: Path | str,
    normalized_dir: Path | str,
    audits_dir: Path | str,
) -> NormalizationResult:
    config_path = Path(config_path)
    state_dir = Path(state_dir)
    schema_path = Path(schema_path)
    normalized_dir = Path(normalized_dir)
    audits_dir = Path(audits_dir)

    registry_path = state_dir / "source_registry.json"
    state_path = state_dir / "normalization_state.json"
    run_log_path = state_dir / "normalization_runs.jsonl"
    notice_log_path = audits_dir / "normalization_notices.jsonl"

    ensure_directory(state_dir)
    ensure_directory(audits_dir)
    ensure_directory(normalized_dir / "sources")

    run_id = f"normalize-{utc_now().replace(':', '').replace('.', '').replace('-', '')}"
    started_at = utc_now()
    staging_root = normalized_dir / ".staging" / run_id
    changed_source_ids: list[str] = []

    previous_state_text = state_path.read_text(encoding="utf-8") if state_path.exists() else None
    previous_run_log_text = run_log_path.read_text(encoding="utf-8") if run_log_path.exists() else ""
    previous_notice_log_text = notice_log_path.read_text(encoding="utf-8") if notice_log_path.exists() else ""

    try:
        catalog = load_catalog(schema_path)
        source_roots = {
            root.root_alias: root.resolved_path
            for root in load_source_roots(config_path)
        }
        registry = load_registry(registry_path)
        raw_event_resolver = RawEventResolver(
            registry=registry,
            source_roots=source_roots,
        )
        previous_state = load_normalization_state(state_path)

        next_state: dict[str, NormalizationStateRecord] = {}
        source_status_counts: Counter[str] = Counter()
        run_outer_counts: Counter[str] = Counter()
        run_payload_counts: Counter[str] = Counter()
        run_unknown_summary: Counter[str] = Counter()
        notices_for_run: list[NormalizationNotice] = []
        normalized_event_count = 0

        for source_id in sorted(registry):
            source = registry[source_id]
            prior_state = previous_state.get(source_id)
            source_output_dir = normalized_dir / "sources" / source_id

            if source.status == "tombstoned":
                next_state[source_id] = tombstone_state_record(
                    source=source,
                    prior_state=prior_state,
                    run_id=run_id,
                    normalization_schema_version=catalog.normalization_schema_version,
                )
                source_status_counts["tombstoned"] += 1
                continue

            mode = determine_normalization_mode(
                source=source,
                prior_state=prior_state,
                source_output_dir=source_output_dir,
                normalization_schema_version=catalog.normalization_schema_version,
            )
            if mode == "unchanged":
                next_state[source_id] = prior_state
                source_status_counts["unchanged"] += 1
                continue

            staged_source_dir = staging_root / "sources" / source_id
            processed = normalize_source(
                source=source,
                source_roots=source_roots,
                prior_state=prior_state,
                source_output_dir=source_output_dir,
                staged_source_dir=staged_source_dir,
                catalog=catalog,
                run_id=run_id,
                mode=mode,
            )
            validate_processed_source(
                source=source,
                processed=processed,
                staged_source_dir=staged_source_dir,
                raw_event_resolver=raw_event_resolver,
            )

            next_state[source_id] = processed.state_record
            source_status_counts["normalized"] += 1
            normalized_event_count += processed.processed_event_count
            run_outer_counts.update(processed.event_counts_by_outer_type)
            run_payload_counts.update(processed.event_counts_by_payload_type)
            notices_for_run.extend(processed.notices)
            for notice in processed.notices:
                summary_key = make_notice_summary_key(notice.notice_type, notice.outer_type, notice.payload_type)
                run_unknown_summary[summary_key] += notice.count_in_source
            changed_source_ids.append(source_id)

        validate_state_against_registry(registry, next_state)

        staged_state_path = staging_root / "normalization_state.json"
        staged_run_log_path = staging_root / "normalization_runs.jsonl"
        staged_notice_log_path = staging_root / "normalization_notices.jsonl"

        report = NormalizationRunReport(
            run_id=run_id,
            started_at=started_at,
            finished_at=utc_now(),
            source_status_counts=dict(sorted(source_status_counts.items())),
            normalized_event_count=normalized_event_count,
            event_counts_by_outer_type=dict(sorted(run_outer_counts.items())),
            event_counts_by_payload_type=dict(sorted(run_payload_counts.items())),
            unknown_signature_summary=dict(sorted(run_unknown_summary.items())),
            success=True,
            fatal_error_summary=None,
        )

        write_text_file(
            staged_state_path,
            json.dumps(
                build_state_payload(
                    state_records=next_state,
                    normalization_schema_version=catalog.normalization_schema_version,
                ),
                indent=2,
                sort_keys=True,
            )
            + "\n",
        )
        write_text_file(
            staged_run_log_path,
            append_jsonl_text(previous_run_log_text, report.to_dict()),
        )
        write_text_file(
            staged_notice_log_path,
            append_jsonl_text(previous_notice_log_text, [notice.to_dict() for notice in notices_for_run]),
        )

        promote_staged_sources(
            staging_root=staging_root,
            normalized_dir=normalized_dir,
            changed_source_ids=changed_source_ids,
        )
        os.replace(staged_state_path, state_path)
        ensure_directory(run_log_path.parent)
        os.replace(staged_run_log_path, run_log_path)
        ensure_directory(notice_log_path.parent)
        os.replace(staged_notice_log_path, notice_log_path)
        cleanup_staging_root(staging_root)
        return NormalizationResult(
            report=report,
            state_path=state_path,
            run_log_path=run_log_path,
            notice_log_path=notice_log_path,
        )
    except Exception as exc:
        cleanup_staging_root(staging_root)
        failure_report = NormalizationRunReport(
            run_id=run_id,
            started_at=started_at,
            finished_at=utc_now(),
            source_status_counts={},
            normalized_event_count=0,
            event_counts_by_outer_type={},
            event_counts_by_payload_type={},
            unknown_signature_summary={},
            success=False,
            fatal_error_summary=str(exc),
        )
        atomic_write_text(
            run_log_path,
            append_jsonl_text(previous_run_log_text, failure_report.to_dict()),
        )
        if previous_state_text is None and state_path.exists():
            state_path.unlink(missing_ok=True)
        if previous_state_text is not None and state_path.exists():
            atomic_write_text(state_path, previous_state_text)
        if previous_notice_log_text:
            atomic_write_text(notice_log_path, previous_notice_log_text)
        return NormalizationResult(
            report=failure_report,
            state_path=state_path,
            run_log_path=run_log_path,
            notice_log_path=notice_log_path,
        )


def load_catalog(schema_path: Path) -> NormalizationCatalog:
    try:
        payload = json.loads(schema_path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError as exc:
        raise NormalizationError(f"Missing normalization schema catalog: {schema_path}") from exc
    except json.JSONDecodeError as exc:
        raise NormalizationError(f"Invalid normalization schema catalog JSON: {schema_path}") from exc

    known_outer_types = payload.get("known_outer_types")
    if not isinstance(known_outer_types, dict) or not known_outer_types:
        raise NormalizationError("Normalization schema catalog must define known_outer_types")
    return NormalizationCatalog(
        schema_version=int(payload["schema_version"]),
        normalization_schema_version=int(payload["normalization_schema_version"]),
        known_outer_types=known_outer_types,
    )


def load_normalization_state(state_path: Path) -> dict[str, NormalizationStateRecord]:
    if not state_path.exists():
        return {}

    try:
        payload = json.loads(state_path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise NormalizationError(f"Invalid normalization state JSON: {state_path}") from exc

    if int(payload.get("schema_version", -1)) != STATE_SCHEMA_VERSION:
        raise NormalizationError(
            f"Unsupported normalization state schema version in {state_path}: {payload.get('schema_version')}"
        )

    records = [
        NormalizationStateRecord.from_dict(item)
        for item in payload.get("sources", [])
    ]
    return {record.source_id: record for record in records}


def determine_normalization_mode(
    source: SourceRecord,
    prior_state: NormalizationStateRecord | None,
    source_output_dir: Path,
    normalization_schema_version: int,
) -> str:
    if prior_state is None:
        return "full"
    if prior_state.status != "normalized":
        return "full"
    if prior_state.normalization_schema_version != normalization_schema_version:
        return "full"
    if not source_artifacts_exist(source_output_dir):
        return "full"

    if prior_state.phase1_committed_byte_end == source.committed_byte_end:
        if prior_state.phase1_committed_line_count != source.committed_line_count:
            raise NormalizationError(
                f"Phase 1 committed line count drift without byte drift for source {source.source_id}"
            )
        if prior_state.phase1_fingerprint_digest == source.sampled_fingerprint.digest:
            return "unchanged"
        raise NormalizationError(
            f"Phase 1 fingerprint drift without committed growth for source {source.source_id}"
        )

    if prior_state.phase1_committed_byte_end > source.committed_byte_end:
        raise NormalizationError(
            f"Phase 1 committed byte end moved backwards for source {source.source_id}"
        )

    if prior_state.phase1_committed_line_count >= source.committed_line_count:
        raise NormalizationError(
            f"Phase 1 committed line count did not grow for source {source.source_id}"
        )

    return "incremental"


def normalize_source(
    source: SourceRecord,
    source_roots: dict[str, Path],
    prior_state: NormalizationStateRecord | None,
    source_output_dir: Path,
    staged_source_dir: Path,
    catalog: NormalizationCatalog,
    run_id: str,
    mode: str,
) -> ProcessedSourceArtifacts:
    ensure_directory(staged_source_dir)
    raw_path = resolve_source_path(source, source_roots)
    existing_session: dict[str, object] | None = None
    existing_stats: dict[str, object] | None = None

    start_offset = 0
    start_line_no = 1
    normalized_event_count = 0
    first_event_timestamp: str | None = None
    last_event_timestamp: str | None = None
    session_meta_ref: dict[str, object] | None = None
    session_meta_fields: dict[str, object] = {}
    event_counts_by_outer_type: Counter[str] = Counter()
    event_counts_by_payload_type: Counter[str] = Counter()
    event_counts_by_canonical_kind: Counter[str] = Counter()
    notice_map: dict[tuple[str, str | None, str | None], dict[str, object]] = {}

    staged_events_path = staged_source_dir / "events.jsonl"
    if mode == "incremental":
        existing_session = read_json_file(source_output_dir / "session.json")
        existing_stats = read_json_file(source_output_dir / "stats.json")
        if existing_session is None or existing_stats is None:
            mode = "full"
        elif not existing_artifacts_match_state(existing_session, existing_stats, prior_state):
            mode = "full"
        else:
            shutil.copy2(source_output_dir / "events.jsonl", staged_events_path)
            normalized_event_count = int(existing_stats["normalized_event_count"])
            first_event_timestamp = as_optional_str(existing_session.get("first_event_timestamp"))
            last_event_timestamp = as_optional_str(existing_session.get("last_event_timestamp"))
            session_meta_ref = existing_session.get("session_meta_ref")
            if isinstance(session_meta_ref, dict):
                session_meta_ref = dict(session_meta_ref)
            else:
                session_meta_ref = None
            session_meta_fields = dict(existing_session.get("session_meta_fields", {}))
            event_counts_by_outer_type.update(existing_stats.get("event_counts_by_outer_type", {}))
            event_counts_by_payload_type.update(existing_stats.get("event_counts_by_payload_type", {}))
            event_counts_by_canonical_kind.update(existing_stats.get("event_counts_by_canonical_kind", {}))
            seed_notice_map(notice_map, existing_stats.get("unknown_signatures", []))
            start_offset = prior_state.phase1_committed_byte_end
            start_line_no = prior_state.phase1_committed_line_count + 1

    if mode == "full":
        session_meta_ref = None
        session_meta_fields = {}
        first_event_timestamp = None
        last_event_timestamp = None
        normalized_event_count = 0
        event_counts_by_outer_type.clear()
        event_counts_by_payload_type.clear()
        event_counts_by_canonical_kind.clear()
        notice_map.clear()
        start_offset = 0
        start_line_no = 1

    processed_event_count = 0
    with staged_events_path.open(
        "a" if mode == "incremental" else "w",
        encoding="utf-8",
        newline="\n",
    ) as events_handle:
        for source_line_no, source_byte_start, source_byte_end, raw_bytes, raw_event in iter_committed_events(
            raw_path=raw_path,
            committed_byte_end=source.committed_byte_end,
            start_offset=start_offset,
            start_line_no=start_line_no,
        ):
            normalized_event, event_notice = build_normalized_event(
                source=source,
                raw_event=raw_event,
                source_line_no=source_line_no,
                source_byte_start=source_byte_start,
                source_byte_end=source_byte_end,
                raw_bytes=raw_bytes,
                catalog=catalog,
            )
            events_handle.write(json.dumps(normalized_event, separators=(",", ":"), sort_keys=True))
            events_handle.write("\n")
            processed_event_count += 1
            normalized_event_count += 1

            if session_meta_ref is None and normalized_event["outer_type"] == "session_meta":
                session_meta_ref = {
                    "event_id": normalized_event["event_id"],
                    "source_line_no": source_line_no,
                    "source_byte_start": source_byte_start,
                    "source_byte_end": source_byte_end,
                    "event_digest": normalized_event["event_digest"],
                }
                session_meta_fields = extract_session_meta_fields(raw_event, catalog)

            timestamp = normalized_event.get("timestamp")
            if first_event_timestamp is None and timestamp is not None:
                first_event_timestamp = str(timestamp)
            if timestamp is not None:
                last_event_timestamp = str(timestamp)

            event_counts_by_outer_type[normalized_event["outer_type"]] += 1
            event_counts_by_payload_type[payload_counter_key(normalized_event.get("payload_type"))] += 1
            event_counts_by_canonical_kind[normalized_event["canonical_kind"]] += 1

            if event_notice is not None:
                notice_key = (
                    event_notice["notice_type"],
                    event_notice.get("outer_type"),
                    event_notice.get("payload_type"),
                )
                current = notice_map.get(notice_key)
                if current is None:
                    notice_map[notice_key] = {
                        "severity": "warning",
                        "notice_type": event_notice["notice_type"],
                        "outer_type": event_notice.get("outer_type"),
                        "payload_type": event_notice.get("payload_type"),
                        "count_in_source": 1,
                        "first_seen_event_id": normalized_event["event_id"],
                    }
                else:
                    current["count_in_source"] = int(current["count_in_source"]) + 1

    if session_meta_ref is None:
        raise NormalizationError(f"Normalized source is missing session_meta event: {source.source_id}")

    unknown_signatures = build_unknown_signature_list(notice_map)
    session_payload = {
        "source_id": source.source_id,
        "session_id": source.source_id,
        "root_alias": source.preferred_locator.root_alias,
        "relative_path": source.preferred_locator.relative_path,
        "session_meta_ref": session_meta_ref,
        "session_meta_fields": session_meta_fields,
        "normalization_schema_version": catalog.normalization_schema_version,
        "first_event_timestamp": first_event_timestamp,
        "last_event_timestamp": last_event_timestamp,
        "committed_line_count": source.committed_line_count,
        "committed_byte_end": source.committed_byte_end,
        "unknown_signatures": unknown_signatures,
    }
    stats_payload = {
        "source_id": source.source_id,
        "session_id": source.source_id,
        "normalization_schema_version": catalog.normalization_schema_version,
        "normalized_event_count": normalized_event_count,
        "event_counts_by_outer_type": dict(sorted(event_counts_by_outer_type.items())),
        "event_counts_by_payload_type": dict(sorted(event_counts_by_payload_type.items())),
        "event_counts_by_canonical_kind": dict(sorted(event_counts_by_canonical_kind.items())),
        "unknown_signatures": unknown_signatures,
    }
    write_text_file(
        staged_source_dir / "session.json",
        json.dumps(session_payload, indent=2, sort_keys=True) + "\n",
    )
    write_text_file(
        staged_source_dir / "stats.json",
        json.dumps(stats_payload, indent=2, sort_keys=True) + "\n",
    )

    notices = [
        NormalizationNotice(
            run_id=run_id,
            source_id=source.source_id,
            severity="warning",
            notice_type=str(item["notice_type"]),
            outer_type=as_optional_str(item.get("outer_type")),
            payload_type=as_optional_str(item.get("payload_type")),
            count_in_source=int(item["count_in_source"]),
            first_seen_event_id=str(item["first_seen_event_id"]),
        )
        for item in unknown_signatures
    ]

    state_record = NormalizationStateRecord(
        source_id=source.source_id,
        normalization_schema_version=catalog.normalization_schema_version,
        phase1_committed_byte_end=source.committed_byte_end,
        phase1_committed_line_count=source.committed_line_count,
        phase1_fingerprint_digest=source.sampled_fingerprint.digest,
        normalized_event_count=normalized_event_count,
        status="normalized",
        last_normalized_at=utc_now(),
        last_run_id=run_id,
    )
    return ProcessedSourceArtifacts(
        session_payload=session_payload,
        stats_payload=stats_payload,
        state_record=state_record,
        notices=notices,
        processed_event_count=processed_event_count,
        event_counts_by_outer_type=Counter(event_counts_by_outer_type),
        event_counts_by_payload_type=Counter(event_counts_by_payload_type),
    )


def existing_artifacts_match_state(
    existing_session: dict[str, object],
    existing_stats: dict[str, object],
    prior_state: NormalizationStateRecord,
) -> bool:
    return (
        int(existing_session.get("committed_byte_end", -1)) == prior_state.phase1_committed_byte_end
        and int(existing_session.get("committed_line_count", -1)) == prior_state.phase1_committed_line_count
        and int(existing_stats.get("normalized_event_count", -1)) == prior_state.phase1_committed_line_count
    )


def build_normalized_event(
    source: SourceRecord,
    raw_event: dict[str, object],
    source_line_no: int,
    source_byte_start: int,
    source_byte_end: int,
    raw_bytes: bytes,
    catalog: NormalizationCatalog,
) -> tuple[dict[str, object], dict[str, object] | None]:
    outer_type = as_optional_str(raw_event.get("type"))
    payload = raw_event.get("payload")
    payload_dict = payload if isinstance(payload, dict) else {}
    payload_type = as_optional_str(payload_dict.get("type"))
    role = as_optional_str(payload_dict.get("role"))
    timestamp = as_optional_str(raw_event.get("timestamp"))

    canonical_kind, normalization_flags, notice = resolve_catalog_signature(
        outer_type=outer_type,
        payload_type=payload_type,
        catalog=catalog,
    )
    references, explicit_ids = extract_explicit_references(payload_dict)
    text_surfaces, text_surface_truncated, text_surface_total_chars = extract_bounded_text_surfaces(raw_event)
    normalized_event = {
        "event_id": f"{source.source_id}:{source_line_no}",
        "source_id": source.source_id,
        "session_id": source.source_id,
        "source_line_no": source_line_no,
        "source_byte_start": source_byte_start,
        "source_byte_end": source_byte_end,
        "event_digest": compute_event_digest(raw_bytes),
        "timestamp": timestamp,
        "outer_type": outer_type,
        "payload_type": payload_type,
        "canonical_kind": canonical_kind,
        "role": role,
        "turn_id": explicit_ids.get("turn_id"),
        "call_id": explicit_ids.get("call_id"),
        "thread_id": explicit_ids.get("thread_id"),
        "references": references,
        "text_surfaces": text_surfaces,
        "text_surface_truncated": text_surface_truncated,
        "text_surface_total_chars": text_surface_total_chars,
        "normalization_flags": normalization_flags,
    }
    return normalized_event, notice


def resolve_catalog_signature(
    outer_type: str | None,
    payload_type: str | None,
    catalog: NormalizationCatalog,
) -> tuple[str, list[str], dict[str, object] | None]:
    if outer_type is None:
        return "generic_event", ["unknown_outer_type"], {
            "notice_type": "unknown_outer_type",
            "outer_type": None,
            "payload_type": payload_type,
        }

    outer_definition = catalog.known_outer_types.get(outer_type)
    if outer_definition is None:
        return "generic_event", ["unknown_outer_type"], {
            "notice_type": "unknown_outer_type",
            "outer_type": outer_type,
            "payload_type": payload_type,
        }

    flags: list[str] = []
    payload_subtypes = outer_definition.get("payload_subtypes")
    if not isinstance(payload_subtypes, dict) or not payload_subtypes:
        return str(outer_definition["canonical_kind"]), flags, None

    requires_payload_type = bool(outer_definition.get("requires_payload_type", False))
    if payload_type is None:
        if requires_payload_type:
            flags.append("missing_payload_type")
            return str(outer_definition["canonical_kind"]), flags, {
                "notice_type": "catalog_mismatch",
                "outer_type": outer_type,
                "payload_type": None,
            }
        return str(outer_definition["canonical_kind"]), flags, None

    subtype_definition = payload_subtypes.get(payload_type)
    if subtype_definition is None:
        flags.append("unknown_payload_type")
        return str(outer_definition["canonical_kind"]), flags, {
            "notice_type": "unknown_payload_type",
            "outer_type": outer_type,
            "payload_type": payload_type,
        }
    return str(subtype_definition["canonical_kind"]), flags, None


def extract_explicit_references(payload: dict[str, object]) -> tuple[list[dict[str, str]], dict[str, str | None]]:
    references: list[dict[str, str]] = []
    explicit_ids: dict[str, str | None] = {}
    for field in REFERENCE_FIELDS:
        value = as_optional_str(payload.get(field))
        explicit_ids[field] = value
        if value is not None:
            references.append(
                {
                    "kind": field,
                    "value": value,
                    "source": f"payload.{field}",
                }
            )
    return references, explicit_ids


def extract_session_meta_fields(raw_event: dict[str, object], catalog: NormalizationCatalog) -> dict[str, object]:
    payload = raw_event.get("payload")
    if not isinstance(payload, dict):
        return {}
    session_meta_definition = catalog.known_outer_types.get("session_meta", {})
    common_fields = session_meta_definition.get("common_fields", [])
    fields: dict[str, object] = {}
    for field in common_fields:
        if field in payload:
            fields[str(field)] = payload[field]
    return fields


def extract_text_surfaces(raw_event: Any) -> list[dict[str, str]]:
    surfaces: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()

    def visit(value: Any, path: str) -> None:
        if isinstance(value, dict):
            for key, nested in value.items():
                next_path = f"{path}.{key}" if path else str(key)
                if isinstance(nested, str) and key in TEXT_SURFACE_KEYS and nested:
                    candidate = (next_path, nested)
                    if candidate not in seen:
                        seen.add(candidate)
                        surfaces.append({"path": next_path, "text": nested})
                    parsed_nested = maybe_parse_embedded_json(key, nested)
                    if parsed_nested is not None:
                        visit(parsed_nested, f"{next_path}.$parsed")
                else:
                    visit(nested, next_path)
            return

        if isinstance(value, list):
            for index, nested in enumerate(value):
                visit(nested, f"{path}[{index}]")

    visit(raw_event, "")
    return surfaces


def extract_bounded_text_surfaces(raw_event: Any) -> tuple[list[dict[str, str]], bool, int]:
    bounded: list[dict[str, str]] = []
    all_surfaces = extract_text_surfaces(raw_event)
    total_source_chars = sum(len(str(surface.get("text", ""))) for surface in all_surfaces)
    total_chars = 0
    truncated = False
    for surface in all_surfaces:
        if len(bounded) >= MAX_PERSISTED_TEXT_SURFACES:
            truncated = True
            break
        text = str(surface.get("text", ""))
        remaining_total = MAX_PERSISTED_TOTAL_TEXT_SURFACE_CHARS - total_chars
        if remaining_total <= 0:
            truncated = True
            break
        allowed_chars = min(MAX_PERSISTED_TEXT_SURFACE_CHARS, remaining_total)
        if len(text) > allowed_chars:
            text = text[:allowed_chars]
            truncated = True
        bounded.append(
            {
                "path": str(surface.get("path", "")),
                "text": text,
            }
        )
        total_chars += len(text)
    return bounded, truncated, total_source_chars


def maybe_parse_embedded_json(key: str, value: str) -> Any | None:
    if key not in {"arguments", "input", "output"}:
        return None
    stripped = value.strip()
    if not stripped or stripped[0] not in "[{":
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return None


def iter_committed_events(
    raw_path: Path,
    committed_byte_end: int,
    start_offset: int,
    start_line_no: int,
) -> Iterator[tuple[int, int, int, bytes, dict[str, object]]]:
    with open_shared_binary(raw_path) as handle:
        handle.seek(start_offset)
        line_no = start_line_no
        while handle.tell() < committed_byte_end:
            source_byte_start = handle.tell()
            line = handle.readline()
            if not line:
                raise NormalizationError(
                    f"Unexpected EOF before committed byte end for source file: {raw_path}"
                )
            source_byte_end = handle.tell()
            if source_byte_end > committed_byte_end:
                raise NormalizationError(
                    f"Committed byte end bisected a line for source file: {raw_path}"
                )
            if not line.endswith(b'\n'):
                raise NormalizationError(
                    f"Committed content contains a partial line for source file: {raw_path}"
                )
            try:
                raw_event = json.loads(line.decode("utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError) as exc:
                raise NormalizationError(
                    f"Malformed committed JSON line {line_no} in source file {raw_path}: {exc}"
                ) from exc
            if not isinstance(raw_event, dict):
                raise NormalizationError(
                    f"Committed JSON line {line_no} is not an object in source file {raw_path}"
                )
            yield line_no, source_byte_start, source_byte_end, line, raw_event
            line_no += 1
        if handle.tell() != committed_byte_end:
            raise NormalizationError(
                f"Committed byte end mismatch for source file {raw_path}: {handle.tell()} != {committed_byte_end}"
            )


def validate_processed_source(
    source: SourceRecord,
    processed: ProcessedSourceArtifacts,
    staged_source_dir: Path,
    raw_event_resolver: RawEventResolver,
) -> None:
    session_payload = processed.session_payload
    stats_payload = processed.stats_payload
    events_path = staged_source_dir / "events.jsonl"
    if session_payload["source_id"] != source.source_id:
        raise NormalizationError(f"Session payload source mismatch for {source.source_id}")
    if int(session_payload["committed_byte_end"]) != source.committed_byte_end:
        raise NormalizationError(f"Committed byte mismatch in session payload for {source.source_id}")
    if int(session_payload["committed_line_count"]) != source.committed_line_count:
        raise NormalizationError(f"Committed line mismatch in session payload for {source.source_id}")
    if int(stats_payload["normalized_event_count"]) != source.committed_line_count:
        raise NormalizationError(
            f"Normalized event count does not match committed line count for {source.source_id}"
        )

    unknown_notice_keys = {
        (notice.notice_type, notice.outer_type, notice.payload_type)
        for notice in processed.notices
    }
    unknown_event_keys: set[tuple[str, str | None, str | None]] = set()
    session_meta_event_id = str(session_payload.get("session_meta_ref", {}).get("event_id", ""))

    last_line_no = 0
    previous_byte_end = 0
    event_count = 0
    with events_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.rstrip("\n")
            if not line:
                continue
            event = json.loads(line)
            event_count += 1
            line_no = int(event["source_line_no"])
            byte_start = int(event["source_byte_start"])
            byte_end = int(event["source_byte_end"])
            if line_no != last_line_no + 1:
                raise NormalizationError(f"Non-contiguous source_line_no for {source.source_id}")
            if byte_start < previous_byte_end or byte_end <= byte_start:
                raise NormalizationError(f"Non-monotonic byte positions for {source.source_id}")
            if "raw_event" in event:
                raise NormalizationError(f"Persisted raw_event is not allowed in normalized event for {source.source_id}")
            if not str(event.get("event_digest", "")):
                raise NormalizationError(f"Missing event_digest in normalized event for {source.source_id}")
            if "text_surface_truncated" not in event:
                raise NormalizationError(f"Missing text_surface_truncated flag in normalized event for {source.source_id}")
            if int(event.get("text_surface_total_chars", -1)) < sum(
                len(str(item.get("text", ""))) for item in event.get("text_surfaces", []) if isinstance(item, dict)
            ):
                raise NormalizationError(f"Invalid text_surface_total_chars in normalized event for {source.source_id}")
            hydrated = raw_event_resolver.hydrate_normalized_event(event)
            if compute_event_digest(hydrated.raw_bytes) != str(event["event_digest"]):
                raise NormalizationError(f"Hydrated raw-event digest mismatch for {source.source_id}")
            if str(event["event_id"]) == session_meta_event_id and str(event.get("outer_type")) != "session_meta":
                raise NormalizationError(f"session_meta_ref did not point to session_meta for {source.source_id}")
            flags = set(event.get("normalization_flags", []))
            if "unknown_outer_type" in flags:
                unknown_event_keys.add(("unknown_outer_type", event.get("outer_type"), event.get("payload_type")))
            if "unknown_payload_type" in flags:
                unknown_event_keys.add(("unknown_payload_type", event.get("outer_type"), event.get("payload_type")))
            if "missing_payload_type" in flags:
                unknown_event_keys.add(("catalog_mismatch", event.get("outer_type"), event.get("payload_type")))
            last_line_no = line_no
            previous_byte_end = byte_end

    if event_count != source.committed_line_count:
        raise NormalizationError(f"Event count mismatch in staged events for {source.source_id}")
    if last_line_no != source.committed_line_count:
        raise NormalizationError(f"Last source_line_no mismatch for {source.source_id}")
    if previous_byte_end != source.committed_byte_end:
        raise NormalizationError(f"Last source_byte_end mismatch for {source.source_id}")
    if not unknown_event_keys.issubset(unknown_notice_keys):
        raise NormalizationError(f"Unknown signatures missing notices for {source.source_id}")
    session_meta_ref = session_payload.get("session_meta_ref")
    if not isinstance(session_meta_ref, dict):
        raise NormalizationError(f"Missing session_meta_ref in session payload for {source.source_id}")
    if int(session_meta_ref.get("source_line_no", 0)) < 1:
        raise NormalizationError(f"Invalid session_meta_ref line for {source.source_id}")
    if int(session_meta_ref.get("source_byte_end", 0)) <= int(session_meta_ref.get("source_byte_start", 0)):
        raise NormalizationError(f"Invalid session_meta_ref bytes for {source.source_id}")


def validate_state_against_registry(
    registry: dict[str, SourceRecord],
    state_records: dict[str, NormalizationStateRecord],
) -> None:
    for source_id, source in registry.items():
        state_record = state_records.get(source_id)
        if state_record is None:
            raise NormalizationError(f"Missing normalization state for source {source_id}")
        if source.status == "tombstoned":
            if state_record.status != "tombstoned":
                raise NormalizationError(f"Tombstoned source not marked tombstoned in state: {source_id}")
            continue
        if state_record.status != "normalized":
            raise NormalizationError(f"Active source not marked normalized in state: {source_id}")
        if state_record.phase1_committed_byte_end != source.committed_byte_end:
            raise NormalizationError(f"State committed byte mismatch for source {source_id}")
        if state_record.phase1_committed_line_count != source.committed_line_count:
            raise NormalizationError(f"State committed line mismatch for source {source_id}")
        if state_record.phase1_fingerprint_digest != source.sampled_fingerprint.digest:
            raise NormalizationError(f"State fingerprint mismatch for source {source_id}")


def tombstone_state_record(
    source: SourceRecord,
    prior_state: NormalizationStateRecord | None,
    run_id: str,
    normalization_schema_version: int,
) -> NormalizationStateRecord:
    if prior_state is None:
        return NormalizationStateRecord(
            source_id=source.source_id,
            normalization_schema_version=normalization_schema_version,
            phase1_committed_byte_end=source.committed_byte_end,
            phase1_committed_line_count=source.committed_line_count,
            phase1_fingerprint_digest=source.sampled_fingerprint.digest,
            normalized_event_count=0,
            status="tombstoned",
            last_normalized_at=utc_now(),
            last_run_id=run_id,
        )
    return NormalizationStateRecord(
        source_id=prior_state.source_id,
        normalization_schema_version=normalization_schema_version,
        phase1_committed_byte_end=source.committed_byte_end,
        phase1_committed_line_count=source.committed_line_count,
        phase1_fingerprint_digest=source.sampled_fingerprint.digest,
        normalized_event_count=prior_state.normalized_event_count,
        status="tombstoned",
        last_normalized_at=utc_now(),
        last_run_id=run_id,
    )


def resolve_source_path(source: SourceRecord, source_roots: dict[str, Path]) -> Path:
    root_path = source_roots.get(source.preferred_locator.root_alias)
    if root_path is None:
        raise NormalizationError(
            f"Missing source root for alias {source.preferred_locator.root_alias}"
        )
    return root_path / Path(source.preferred_locator.relative_path)


def source_artifacts_exist(source_output_dir: Path) -> bool:
    return (
        (source_output_dir / "session.json").exists()
        and (source_output_dir / "stats.json").exists()
        and (source_output_dir / "events.jsonl").exists()
    )


def read_json_file(path: Path) -> dict[str, object] | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError:
        return None


def seed_notice_map(
    notice_map: dict[tuple[str, str | None, str | None], dict[str, object]],
    existing_unknown_signatures: list[dict[str, object]],
) -> None:
    for item in existing_unknown_signatures:
        key = (
            str(item["notice_type"]),
            as_optional_str(item.get("outer_type")),
            as_optional_str(item.get("payload_type")),
        )
        notice_map[key] = {
            "severity": "warning",
            "notice_type": key[0],
            "outer_type": key[1],
            "payload_type": key[2],
            "count_in_source": int(item["count_in_source"]),
            "first_seen_event_id": str(item["first_seen_event_id"]),
        }


def build_unknown_signature_list(
    notice_map: dict[tuple[str, str | None, str | None], dict[str, object]],
) -> list[dict[str, object]]:
    return [
        {
            "severity": "warning",
            "notice_type": item["notice_type"],
            "outer_type": item["outer_type"],
            "payload_type": item["payload_type"],
            "count_in_source": int(item["count_in_source"]),
            "first_seen_event_id": item["first_seen_event_id"],
        }
        for _, item in sorted(
            notice_map.items(),
            key=lambda pair: (pair[0][0], pair[0][1] or "", pair[0][2] or ""),
        )
    ]


def build_state_payload(
    state_records: dict[str, NormalizationStateRecord],
    normalization_schema_version: int,
) -> dict[str, object]:
    return {
        "schema_version": STATE_SCHEMA_VERSION,
        "normalization_schema_version": normalization_schema_version,
        "generated_at": utc_now(),
        "source_count": len(state_records),
        "sources": [state_records[source_id].to_dict() for source_id in sorted(state_records)],
    }


def append_jsonl_text(existing_text: str, entries: dict[str, object] | list[dict[str, object]]) -> str:
    merged = existing_text
    if merged and not merged.endswith("\n"):
        merged += "\n"
    if isinstance(entries, dict):
        entries = [entries]
    for entry in entries:
        merged += json.dumps(entry, sort_keys=True) + "\n"
    return merged


def write_text_file(path: Path, content: str) -> None:
    ensure_directory(path.parent)
    path.write_text(content, encoding="utf-8")


def promote_staged_sources(staging_root: Path, normalized_dir: Path, changed_source_ids: list[str]) -> None:
    if not changed_source_ids:
        return

    staged_sources_root = staging_root / "sources"
    backup_root = staging_root / "_backup"
    promoted: list[tuple[Path, Path, bool]] = []
    try:
        for source_id in changed_source_ids:
            staged_dir = staged_sources_root / source_id
            target_dir = normalized_dir / "sources" / source_id
            backup_dir = backup_root / source_id
            had_existing = target_dir.exists()
            if had_existing:
                ensure_directory(backup_dir.parent)
                os.replace(target_dir, backup_dir)
            ensure_directory(target_dir.parent)
            os.replace(staged_dir, target_dir)
            promoted.append((target_dir, backup_dir, had_existing))
    except Exception as exc:
        rollback_promoted_sources(promoted)
        raise NormalizationError(f"Failed to promote staged normalized sources: {exc}") from exc


def rollback_promoted_sources(promoted: list[tuple[Path, Path, bool]]) -> None:
    for target_dir, backup_dir, had_existing in reversed(promoted):
        if target_dir.exists():
            shutil.rmtree(target_dir)
        if had_existing and backup_dir.exists():
            ensure_directory(target_dir.parent)
            os.replace(backup_dir, target_dir)


def cleanup_staging_root(staging_root: Path) -> None:
    if staging_root.exists():
        shutil.rmtree(staging_root, ignore_errors=True)


def payload_counter_key(payload_type: str | None) -> str:
    return payload_type if payload_type is not None else PAYLOAD_NONE_KEY


def make_notice_summary_key(notice_type: str, outer_type: str | None, payload_type: str | None) -> str:
    return f"{notice_type}:{outer_type or PAYLOAD_NONE_KEY}:{payload_type or PAYLOAD_NONE_KEY}"


def as_optional_str(value: object) -> str | None:
    return value if isinstance(value, str) and value else None
