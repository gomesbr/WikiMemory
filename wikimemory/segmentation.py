from __future__ import annotations

import json
import os
import re
import shutil
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

from .discovery import DiscoveryError, atomic_write_text, ensure_directory, utc_now
from .normalization import (
    NormalizationStateRecord,
    append_jsonl_text,
    load_normalization_state,
    read_json_file,
    write_text_file,
)

STATE_SCHEMA_VERSION = 1
SEGMENTATION_SCHEMA_VERSION = 1
TARGET_TEXT_SURFACE_CHARS = 2200
MAX_TEXT_SURFACE_CHARS = 4200
MAX_EVENTS_PER_SEGMENT = 80
LOW_SIGNAL_GAP_THRESHOLD = 3
REFERENCE_FIELDS = ("turn_id", "call_id", "thread_id")
STOPWORDS = {
    "a",
    "about",
    "after",
    "all",
    "also",
    "an",
    "and",
    "any",
    "are",
    "as",
    "at",
    "be",
    "because",
    "been",
    "before",
    "being",
    "between",
    "both",
    "but",
    "by",
    "can",
    "could",
    "did",
    "do",
    "does",
    "done",
    "for",
    "from",
    "get",
    "had",
    "has",
    "have",
    "he",
    "her",
    "here",
    "him",
    "his",
    "how",
    "i",
    "if",
    "in",
    "into",
    "is",
    "it",
    "its",
    "just",
    "me",
    "more",
    "my",
    "new",
    "no",
    "not",
    "now",
    "of",
    "on",
    "or",
    "our",
    "out",
    "over",
    "same",
    "she",
    "so",
    "some",
    "that",
    "the",
    "their",
    "them",
    "then",
    "there",
    "these",
    "they",
    "this",
    "to",
    "too",
    "up",
    "us",
    "very",
    "was",
    "we",
    "were",
    "what",
    "when",
    "which",
    "who",
    "will",
    "with",
    "would",
    "you",
    "your",
}
LOW_SIGNAL_KINDS = {
    "session_meta",
    "turn_context",
    "event_msg.task_started",
    "event_msg.task_complete",
    "event_msg.item_completed",
    "event_msg.token_count",
    "event_msg.exec_command_end",
    "event_msg.patch_apply_end",
}
COMPACTION_KINDS = {"compacted", "event_msg.context_compacted"}
CONTROLLED_BOUNDARY_REASONS = {
    "end_of_stream",
    "forced_size_split",
    "low_signal_gap",
    "max_event_guardrail",
    "semantic_shift",
    "size_guardrail",
}


class SegmentationError(DiscoveryError):
    """Fatal segmentation error that must stop the run."""


@dataclass(frozen=True)
class SegmentationStateRecord:
    source_id: str
    segmentation_schema_version: int
    normalization_schema_version: int
    normalized_event_count: int
    phase2_committed_byte_end: int
    status: str
    segment_count: int
    last_segmented_at: str
    last_run_id: str

    def to_dict(self) -> dict[str, object]:
        return {
            "source_id": self.source_id,
            "segmentation_schema_version": self.segmentation_schema_version,
            "normalization_schema_version": self.normalization_schema_version,
            "normalized_event_count": self.normalized_event_count,
            "phase2_committed_byte_end": self.phase2_committed_byte_end,
            "status": self.status,
            "segment_count": self.segment_count,
            "last_segmented_at": self.last_segmented_at,
            "last_run_id": self.last_run_id,
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "SegmentationStateRecord":
        return cls(
            source_id=str(data["source_id"]),
            segmentation_schema_version=int(data["segmentation_schema_version"]),
            normalization_schema_version=int(data["normalization_schema_version"]),
            normalized_event_count=int(data["normalized_event_count"]),
            phase2_committed_byte_end=int(data["phase2_committed_byte_end"]),
            status=str(data["status"]),
            segment_count=int(data["segment_count"]),
            last_segmented_at=str(data["last_segmented_at"]),
            last_run_id=str(data["last_run_id"]),
        )


@dataclass(frozen=True)
class SegmentationRunReport:
    run_id: str
    started_at: str
    finished_at: str
    source_status_counts: dict[str, int]
    segmented_source_count: int
    segment_count: int
    boundary_reason_counts: dict[str, int]
    success: bool
    fatal_error_summary: str | None

    def to_dict(self) -> dict[str, object]:
        return {
            "run_id": self.run_id,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "source_status_counts": self.source_status_counts,
            "segmented_source_count": self.segmented_source_count,
            "segment_count": self.segment_count,
            "boundary_reason_counts": self.boundary_reason_counts,
            "success": self.success,
            "fatal_error_summary": self.fatal_error_summary,
        }


@dataclass(frozen=True)
class SegmentationResult:
    report: SegmentationRunReport
    state_path: Path
    run_log_path: Path


@dataclass(frozen=True)
class SegmentedSourceArtifacts:
    session_flow_payload: dict[str, object]
    stats_payload: dict[str, object]
    segment_records: list[dict[str, object]]
    state_record: SegmentationStateRecord
    boundary_reason_counts: Counter[str]


@dataclass(frozen=True)
class EventProfile:
    event_id: str
    source_line_no: int
    timestamp: str | None
    canonical_kind: str
    role: str | None
    text_surfaces: list[dict[str, str]]
    text_len: int
    keywords: Counter[str]
    explicit_ids: dict[str, set[str]]
    meaningful: bool
    low_signal: bool
    compaction: bool


@dataclass
class SegmentBuilder:
    source_id: str
    index: int
    events: list[dict[str, object]] = field(default_factory=list)
    profiles: list[EventProfile] = field(default_factory=list)
    keyword_counts: Counter[str] = field(default_factory=Counter)
    dominant_kinds: Counter[str] = field(default_factory=Counter)
    explicit_ids: dict[str, set[str]] = field(
        default_factory=lambda: {field: set() for field in REFERENCE_FIELDS}
    )
    text_surface_char_count: int = 0
    low_signal_attachment_count: int = 0

    def add(self, event: dict[str, object], profile: EventProfile) -> None:
        self.events.append(event)
        self.profiles.append(profile)
        self.keyword_counts.update(profile.keywords)
        self.dominant_kinds[profile.canonical_kind] += 1
        self.text_surface_char_count += profile.text_len
        for field_name, values in profile.explicit_ids.items():
            self.explicit_ids[field_name].update(values)
        if profile.low_signal and len(self.events) > 1:
            self.low_signal_attachment_count += 1

    @property
    def event_count(self) -> int:
        return len(self.events)

    @property
    def first_event(self) -> dict[str, object]:
        return self.events[0]

    @property
    def last_event(self) -> dict[str, object]:
        return self.events[-1]

    @property
    def last_profile(self) -> EventProfile:
        return self.profiles[-1]

    @property
    def meaningful_profiles(self) -> list[EventProfile]:
        return [profile for profile in self.profiles if profile.meaningful]


def run_segmentation(
    state_dir: Path | str,
    normalized_dir: Path | str,
    segmented_dir: Path | str,
    source_ids: Iterable[str] | None = None,
) -> SegmentationResult:
    state_dir = Path(state_dir)
    normalized_dir = Path(normalized_dir)
    segmented_dir = Path(segmented_dir)
    state_path = state_dir / "segmentation_state.json"
    run_log_path = state_dir / "segmentation_runs.jsonl"
    normalization_state_path = state_dir / "normalization_state.json"

    ensure_directory(state_dir)
    ensure_directory(segmented_dir / "sources")

    run_id = f"segment-{utc_now().replace(':', '').replace('.', '').replace('-', '')}"
    started_at = utc_now()
    staging_root = segmented_dir / ".staging" / run_id
    changed_source_ids: list[str] = []

    previous_state_text = state_path.read_text(encoding="utf-8") if state_path.exists() else None
    previous_run_log_text = run_log_path.read_text(encoding="utf-8") if run_log_path.exists() else ""

    try:
        normalization_state = load_normalization_state(normalization_state_path)
        previous_state = load_segmentation_state(state_path)
        next_state = dict(previous_state)
        target_source_ids = resolve_target_source_ids(
            source_ids=source_ids,
            normalization_state=normalization_state,
        )

        source_status_counts: Counter[str] = Counter()
        boundary_reason_counts: Counter[str] = Counter()
        total_segment_count = 0

        for source_id in target_source_ids:
            normalized_state_record = normalization_state[source_id]
            source_output_dir = segmented_dir / "sources" / source_id

            if normalized_state_record.status == "tombstoned":
                next_state[source_id] = tombstone_state_record(
                    source_id=source_id,
                    normalized_state_record=normalized_state_record,
                    prior_state=previous_state.get(source_id),
                    run_id=run_id,
                )
                source_status_counts["tombstoned"] += 1
                continue

            mode = determine_segmentation_mode(
                normalized_state_record=normalized_state_record,
                prior_state=previous_state.get(source_id),
                source_output_dir=source_output_dir,
            )
            if mode == "unchanged":
                next_state[source_id] = previous_state[source_id]
                source_status_counts["unchanged"] += 1
                continue

            staged_source_dir = staging_root / "sources" / source_id
            processed = segment_source(
                source_id=source_id,
                normalized_state_record=normalized_state_record,
                normalized_dir=normalized_dir,
                staged_source_dir=staged_source_dir,
                run_id=run_id,
            )
            validate_processed_source(
                source_id=source_id,
                normalized_state_record=normalized_state_record,
                processed=processed,
                staged_source_dir=staged_source_dir,
            )
            next_state[source_id] = processed.state_record
            source_status_counts["segmented"] += 1
            boundary_reason_counts.update(processed.boundary_reason_counts)
            total_segment_count += len(processed.segment_records)
            changed_source_ids.append(source_id)

        if source_ids is None:
            validate_state_against_normalization(
                normalization_state=normalization_state,
                segmentation_state=next_state,
            )

        staged_state_path = staging_root / "segmentation_state.json"
        staged_run_log_path = staging_root / "segmentation_runs.jsonl"
        report = SegmentationRunReport(
            run_id=run_id,
            started_at=started_at,
            finished_at=utc_now(),
            source_status_counts=dict(sorted(source_status_counts.items())),
            segmented_source_count=source_status_counts.get("segmented", 0),
            segment_count=total_segment_count,
            boundary_reason_counts=dict(sorted(boundary_reason_counts.items())),
            success=True,
            fatal_error_summary=None,
        )
        write_text_file(
            staged_state_path,
            json.dumps(build_state_payload(next_state), indent=2, sort_keys=True) + "\n",
        )
        write_text_file(
            staged_run_log_path,
            append_jsonl_text(previous_run_log_text, report.to_dict()),
        )
        promote_staged_sources(
            staging_root=staging_root,
            segmented_dir=segmented_dir,
            changed_source_ids=changed_source_ids,
        )
        os.replace(staged_state_path, state_path)
        ensure_directory(run_log_path.parent)
        os.replace(staged_run_log_path, run_log_path)
        cleanup_staging_root(staging_root)
        return SegmentationResult(report=report, state_path=state_path, run_log_path=run_log_path)
    except Exception as exc:
        cleanup_staging_root(staging_root)
        failure_report = SegmentationRunReport(
            run_id=run_id,
            started_at=started_at,
            finished_at=utc_now(),
            source_status_counts={},
            segmented_source_count=0,
            segment_count=0,
            boundary_reason_counts={},
            success=False,
            fatal_error_summary=str(exc),
        )
        atomic_write_text(run_log_path, append_jsonl_text(previous_run_log_text, failure_report.to_dict()))
        if previous_state_text is None and state_path.exists():
            state_path.unlink(missing_ok=True)
        if previous_state_text is not None and state_path.exists():
            atomic_write_text(state_path, previous_state_text)
        return SegmentationResult(report=failure_report, state_path=state_path, run_log_path=run_log_path)


def load_segmentation_state(state_path: Path) -> dict[str, SegmentationStateRecord]:
    if not state_path.exists():
        return {}
    try:
        payload = json.loads(state_path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise SegmentationError(f"Invalid segmentation state JSON: {state_path}") from exc
    if int(payload.get("schema_version", -1)) != STATE_SCHEMA_VERSION:
        raise SegmentationError(
            f"Unsupported segmentation state schema version in {state_path}: {payload.get('schema_version')}"
        )
    records = [SegmentationStateRecord.from_dict(item) for item in payload.get("sources", [])]
    return {record.source_id: record for record in records}


def resolve_target_source_ids(
    source_ids: Iterable[str] | None,
    normalization_state: dict[str, NormalizationStateRecord],
) -> list[str]:
    if source_ids is None:
        return sorted(normalization_state)
    target_source_ids = sorted(dict.fromkeys(str(source_id) for source_id in source_ids))
    missing = [source_id for source_id in target_source_ids if source_id not in normalization_state]
    if missing:
        raise SegmentationError(f"Requested source_ids are missing from normalization state: {', '.join(missing)}")
    return target_source_ids


def determine_segmentation_mode(
    normalized_state_record: NormalizationStateRecord,
    prior_state: SegmentationStateRecord | None,
    source_output_dir: Path,
) -> str:
    if prior_state is None:
        return "full"
    if prior_state.status != "segmented":
        return "full"
    if prior_state.segmentation_schema_version != SEGMENTATION_SCHEMA_VERSION:
        return "full"
    if prior_state.normalization_schema_version != normalized_state_record.normalization_schema_version:
        return "full"
    if not source_artifacts_exist(source_output_dir):
        return "full"
    if prior_state.phase2_committed_byte_end == normalized_state_record.phase1_committed_byte_end:
        if prior_state.normalized_event_count != normalized_state_record.normalized_event_count:
            raise SegmentationError(
                f"Normalized event count drift without committed byte drift for source {normalized_state_record.source_id}"
            )
        return "unchanged"
    if prior_state.phase2_committed_byte_end > normalized_state_record.phase1_committed_byte_end:
        raise SegmentationError(
            f"Normalized committed byte end moved backwards for source {normalized_state_record.source_id}"
        )
    return "full"


def segment_source(
    source_id: str,
    normalized_state_record: NormalizationStateRecord,
    normalized_dir: Path,
    staged_source_dir: Path,
    run_id: str,
) -> SegmentedSourceArtifacts:
    ensure_directory(staged_source_dir)
    source_dir = normalized_dir / "sources" / source_id
    session_payload = read_json_required(source_dir / "session.json")
    stats_payload = read_json_required(source_dir / "stats.json")
    events = read_jsonl_required(source_dir / "events.jsonl")

    if len(events) != normalized_state_record.normalized_event_count:
        raise SegmentationError(
            f"Normalized event count mismatch for source {source_id}: {len(events)} != {normalized_state_record.normalized_event_count}"
        )

    session_flow_payload, segment_records, boundary_counts, stats = build_segmentation_outputs(
        source_id=source_id,
        session_payload=session_payload,
        normalized_stats=stats_payload,
        events=events,
    )

    write_text_file(
        staged_source_dir / "session_flow.json",
        json.dumps(session_flow_payload, indent=2, sort_keys=True) + "\n",
    )
    write_text_file(
        staged_source_dir / "segments.jsonl",
        "".join(json.dumps(record, separators=(",", ":"), sort_keys=True) + "\n" for record in segment_records),
    )
    write_text_file(
        staged_source_dir / "stats.json",
        json.dumps(stats, indent=2, sort_keys=True) + "\n",
    )

    state_record = SegmentationStateRecord(
        source_id=source_id,
        segmentation_schema_version=SEGMENTATION_SCHEMA_VERSION,
        normalization_schema_version=normalized_state_record.normalization_schema_version,
        normalized_event_count=normalized_state_record.normalized_event_count,
        phase2_committed_byte_end=normalized_state_record.phase1_committed_byte_end,
        status="segmented",
        segment_count=len(segment_records),
        last_segmented_at=utc_now(),
        last_run_id=run_id,
    )
    return SegmentedSourceArtifacts(
        session_flow_payload=session_flow_payload,
        stats_payload=stats,
        segment_records=segment_records,
        state_record=state_record,
        boundary_reason_counts=boundary_counts,
    )


def build_segmentation_outputs(
    source_id: str,
    session_payload: dict[str, object],
    normalized_stats: dict[str, object],
    events: list[dict[str, object]],
) -> tuple[dict[str, object], list[dict[str, object]], Counter[str], dict[str, object]]:
    if not events:
        raise SegmentationError(f"Normalized source has no events: {source_id}")

    profiles = [build_event_profile(event) for event in events]
    builders: list[SegmentBuilder] = []
    current = SegmentBuilder(source_id=source_id, index=0)
    current.add(events[0], profiles[0])

    trailing_boundary_reasons: dict[int, list[str]] = {}
    for event, profile in zip(events[1:], profiles[1:]):
        boundary_reasons = determine_boundary_reasons(current, profile)
        if boundary_reasons:
            trailing_boundary_reasons[len(builders)] = boundary_reasons
            builders.append(current)
            current = SegmentBuilder(source_id=source_id, index=len(builders))
        current.add(event, profile)
    builders.append(current)

    segment_records: list[dict[str, object]] = []
    boundary_counts: Counter[str] = Counter()
    total_low_signal_attachments = 0
    forced_split_sources: set[str] = set()

    for index, builder in enumerate(builders):
        if index < len(builders) - 1:
            boundary_reasons = trailing_boundary_reasons.get(index, ["semantic_shift"])
        else:
            boundary_reasons = ["end_of_stream"]
        boundary_counts.update(boundary_reasons)
        total_low_signal_attachments += builder.low_signal_attachment_count
        forced_split_sources.update(reason for reason in boundary_reasons if "split" in reason)
        segment_records.append(finalize_segment_record(builder, boundary_reasons))

    flow_windows = build_flow_windows(profiles)
    session_flow_payload = {
        "source_id": source_id,
        "session_id": session_payload["session_id"],
        "normalized_event_count": len(events),
        "first_event_timestamp": session_payload.get("first_event_timestamp"),
        "last_event_timestamp": session_payload.get("last_event_timestamp"),
        "flow_windows": flow_windows,
        "detected_turn_markers": build_explicit_chain_windows(events, "turn_id"),
        "detected_call_chains": build_explicit_chain_windows(events, "call_id"),
        "segmentation_schema_version": SEGMENTATION_SCHEMA_VERSION,
    }
    stats_payload = {
        "source_id": source_id,
        "session_id": session_payload["session_id"],
        "segmentation_schema_version": SEGMENTATION_SCHEMA_VERSION,
        "segment_count": len(segment_records),
        "event_counts_by_canonical_kind": dict(
            sorted(dict(normalized_stats.get("event_counts_by_canonical_kind", {})).items())
        ),
        "boundary_reason_counts": dict(sorted(boundary_counts.items())),
        "largest_segment_by_events": describe_largest_segment(segment_records, key="event_count"),
        "largest_segment_by_text_size": describe_largest_segment(segment_records, key="text_surface_char_count"),
        "forced_split_sources": sorted(forced_split_sources),
        "low_signal_attachment_count": total_low_signal_attachments,
    }
    return session_flow_payload, segment_records, boundary_counts, stats_payload


def build_event_profile(event: dict[str, object]) -> EventProfile:
    canonical_kind = str(event["canonical_kind"])
    role = as_optional_str(event.get("role"))
    text_surfaces = list(event.get("text_surfaces", []))
    text_len = int(
        event.get(
            "text_surface_total_chars",
            sum(len(str(item.get("text", ""))) for item in text_surfaces),
        )
    )
    keywords = extract_keywords(text_surfaces)
    explicit_ids = {
        field: ({value} if (value := as_optional_str(event.get(field))) else set())
        for field in REFERENCE_FIELDS
    }
    low_signal = canonical_kind in LOW_SIGNAL_KINDS
    compaction = canonical_kind in COMPACTION_KINDS
    meaningful = bool(text_len or keywords or not low_signal or compaction)
    return EventProfile(
        event_id=str(event["event_id"]),
        source_line_no=int(event["source_line_no"]),
        timestamp=as_optional_str(event.get("timestamp")),
        canonical_kind=canonical_kind,
        role=role,
        text_surfaces=text_surfaces,
        text_len=text_len,
        keywords=keywords,
        explicit_ids=explicit_ids,
        meaningful=meaningful,
        low_signal=low_signal,
        compaction=compaction,
    )


def determine_boundary_reasons(current: SegmentBuilder, next_profile: EventProfile) -> list[str]:
    if not current.events:
        return []
    if has_explicit_continuity(current, next_profile):
        return []
    if next_profile.low_signal:
        return []
    if not current.meaningful_profiles:
        return []

    boundary_reasons: list[str] = []
    shared_keywords = len(set(current.keyword_counts) & set(next_profile.keywords))
    semantic_shift = shared_keywords == 0 and not kind_family_matches(
        current.last_profile.canonical_kind,
        next_profile.canonical_kind,
    )

    trailing_low_signal = count_trailing_low_signal(current.profiles)
    if trailing_low_signal >= LOW_SIGNAL_GAP_THRESHOLD and next_profile.meaningful:
        boundary_reasons.append("low_signal_gap")

    projected_text_size = current.text_surface_char_count + next_profile.text_len
    if projected_text_size > MAX_TEXT_SURFACE_CHARS:
        boundary_reasons.append("forced_size_split")
    elif projected_text_size > TARGET_TEXT_SURFACE_CHARS and semantic_shift:
        boundary_reasons.append("size_guardrail")

    if current.event_count >= MAX_EVENTS_PER_SEGMENT and semantic_shift:
        boundary_reasons.append("max_event_guardrail")

    if semantic_shift:
        boundary_reasons.append("semantic_shift")

    if boundary_reasons and not can_cut_safely(current, next_profile):
        return []
    return dedupe_preserving_order(boundary_reasons)


def has_explicit_continuity(current: SegmentBuilder, next_profile: EventProfile) -> bool:
    for field in REFERENCE_FIELDS:
        if current.explicit_ids[field] & next_profile.explicit_ids[field]:
            return True
    if current.last_profile.compaction or next_profile.compaction:
        return True
    return False


def kind_family_matches(left: str, right: str) -> bool:
    return left.split(".", 1)[0] == right.split(".", 1)[0]


def count_trailing_low_signal(profiles: list[EventProfile]) -> int:
    count = 0
    for profile in reversed(profiles):
        if not profile.low_signal:
            break
        count += 1
    return count


def can_cut_safely(current: SegmentBuilder, next_profile: EventProfile) -> bool:
    if current.last_profile.low_signal and next_profile.meaningful:
        return True
    return not has_explicit_continuity(current, next_profile)


def finalize_segment_record(builder: SegmentBuilder, boundary_reasons: list[str]) -> dict[str, object]:
    flags: list[str] = []
    if all(profile.low_signal for profile in builder.profiles):
        flags.append("low_signal_only")
    if any(reason in {"forced_size_split", "max_event_guardrail"} for reason in boundary_reasons):
        flags.append("forced_split")

    return {
        "segment_id": f"{builder.source_id}:{builder.index}",
        "source_id": builder.source_id,
        "segment_index": builder.index,
        "start_event_id": builder.first_event["event_id"],
        "end_event_id": builder.last_event["event_id"],
        "start_line_no": int(builder.first_event["source_line_no"]),
        "end_line_no": int(builder.last_event["source_line_no"]),
        "start_timestamp": builder.first_event.get("timestamp"),
        "end_timestamp": builder.last_event.get("timestamp"),
        "event_count": builder.event_count,
        "text_surface_char_count": builder.text_surface_char_count,
        "dominant_kinds": [kind for kind, _ in builder.dominant_kinds.most_common(3)],
        "explicit_link_ids": {
            field: sorted(values) for field, values in builder.explicit_ids.items() if values
        },
        "topic_hints": build_topic_hints(builder),
        "boundary_reasons": boundary_reasons,
        "segment_flags": flags,
    }


def build_topic_hints(builder: SegmentBuilder) -> list[str]:
    hints: list[str] = []
    for keyword, _ in builder.keyword_counts.most_common(3):
        if keyword not in hints:
            hints.append(keyword)
    if hints:
        return hints[:3]

    kind_hint_map = {
        "compacted": "context compaction",
        "event_msg.agent_message": "agent message",
        "event_msg.user_message": "user request",
        "response_item.function_call": "tool activity",
        "response_item.function_call_output": "tool results",
        "response_item.custom_tool_call": "custom tool activity",
        "response_item.custom_tool_call_output": "custom tool results",
        "response_item.message": "assistant response",
        "turn_context": "turn context",
        "session_meta": "session metadata",
    }
    for kind, _ in builder.dominant_kinds.most_common():
        hint = kind_hint_map.get(kind)
        if hint and hint not in hints:
            hints.append(hint)
        if len(hints) == 3:
            break
    if not hints:
        hints.append("operational context")
    return hints[:3]


def build_flow_windows(profiles: list[EventProfile]) -> list[dict[str, object]]:
    windows: list[dict[str, object]] = []
    current_kind = classify_flow_window(profiles[0])
    start_index = 0

    for index, profile in enumerate(profiles[1:], start=1):
        next_kind = classify_flow_window(profile)
        if next_kind == current_kind:
            continue
        windows.append(
            {
                "window_index": len(windows),
                "window_kind": current_kind,
                "start_event_id": profiles[start_index].event_id,
                "end_event_id": profiles[index - 1].event_id,
                "event_count": index - start_index,
            }
        )
        start_index = index
        current_kind = next_kind

    windows.append(
        {
            "window_index": len(windows),
            "window_kind": current_kind,
            "start_event_id": profiles[start_index].event_id,
            "end_event_id": profiles[-1].event_id,
            "event_count": len(profiles) - start_index,
        }
    )
    return windows


def classify_flow_window(profile: EventProfile) -> str:
    if profile.low_signal:
        return "low_signal"
    if profile.explicit_ids["call_id"]:
        return "call_chain"
    if profile.explicit_ids["turn_id"]:
        return "turn_scoped"
    if profile.compaction:
        return "context_shift"
    return "meaningful"


def build_explicit_chain_windows(events: list[dict[str, object]], field: str) -> list[dict[str, object]]:
    windows: list[dict[str, object]] = []
    for value, indices in collect_explicit_indices(events, field).items():
        windows.append(
            {
                field: value,
                "start_event_id": events[indices[0]]["event_id"],
                "end_event_id": events[indices[-1]]["event_id"],
                "event_count": len(indices),
            }
        )
    return sorted(windows, key=lambda item: (item.get(field) or "", item["start_event_id"]))


def collect_explicit_indices(events: list[dict[str, object]], field: str) -> dict[str, list[int]]:
    collected: dict[str, list[int]] = {}
    for index, event in enumerate(events):
        value = as_optional_str(event.get(field))
        if value is None:
            continue
        collected.setdefault(value, []).append(index)
    return collected


def describe_largest_segment(segment_records: list[dict[str, object]], key: str) -> dict[str, object]:
    segment = max(segment_records, key=lambda item: int(item[key]))
    return {
        "segment_id": segment["segment_id"],
        key: int(segment[key]),
    }


def validate_processed_source(
    source_id: str,
    normalized_state_record: NormalizationStateRecord,
    processed: SegmentedSourceArtifacts,
    staged_source_dir: Path,
) -> None:
    session_flow = processed.session_flow_payload
    stats_payload = processed.stats_payload
    segments_path = staged_source_dir / "segments.jsonl"
    if session_flow["source_id"] != source_id:
        raise SegmentationError(f"Session flow source mismatch for {source_id}")
    if int(session_flow["normalized_event_count"]) != normalized_state_record.normalized_event_count:
        raise SegmentationError(f"Session flow event count mismatch for {source_id}")
    if int(processed.state_record.phase2_committed_byte_end) != normalized_state_record.phase1_committed_byte_end:
        raise SegmentationError(f"State committed byte mismatch for {source_id}")
    if int(stats_payload["segment_count"]) != processed.state_record.segment_count:
        raise SegmentationError(f"Segment count mismatch in stats for {source_id}")

    segment_records = read_jsonl_required(segments_path)
    if len(segment_records) != processed.state_record.segment_count:
        raise SegmentationError(f"Segment file count mismatch for {source_id}")

    expected_line = 1
    for expected_index, segment in enumerate(segment_records):
        if int(segment["segment_index"]) != expected_index:
            raise SegmentationError(f"Non-contiguous segment_index for {source_id}")
        if int(segment["start_line_no"]) != expected_line:
            raise SegmentationError(f"Segment coverage gap or overlap for {source_id}")
        end_line = int(segment["end_line_no"])
        if end_line < expected_line:
            raise SegmentationError(f"Invalid segment line range for {source_id}")
        topic_hints = segment.get("topic_hints", [])
        if len(topic_hints) == 0 or len(topic_hints) > 3:
            raise SegmentationError(f"Invalid topic hint count for {source_id}")
        if any(not str(hint).strip() for hint in topic_hints):
            raise SegmentationError(f"Empty topic hint for {source_id}")
        reasons = segment.get("boundary_reasons", [])
        if not reasons:
            raise SegmentationError(f"Missing boundary reasons for {source_id}")
        if any(reason not in CONTROLLED_BOUNDARY_REASONS for reason in reasons):
            raise SegmentationError(f"Unknown boundary reason for {source_id}")
        start_timestamp = segment.get("start_timestamp")
        end_timestamp = segment.get("end_timestamp")
        if start_timestamp and end_timestamp and str(start_timestamp) > str(end_timestamp):
            raise SegmentationError(f"Segment timestamp ordering mismatch for {source_id}")
        expected_line = end_line + 1

    if expected_line - 1 != normalized_state_record.normalized_event_count:
        raise SegmentationError(f"Segment coverage does not match event count for {source_id}")


def validate_state_against_normalization(
    normalization_state: dict[str, NormalizationStateRecord],
    segmentation_state: dict[str, SegmentationStateRecord],
) -> None:
    for source_id, normalized_state_record in normalization_state.items():
        state_record = segmentation_state.get(source_id)
        if state_record is None:
            raise SegmentationError(f"Missing segmentation state for source {source_id}")
        if normalized_state_record.status == "tombstoned":
            if state_record.status != "tombstoned":
                raise SegmentationError(f"Tombstoned source not marked tombstoned in segmentation state: {source_id}")
            continue
        if state_record.status != "segmented":
            raise SegmentationError(f"Active source not marked segmented in state: {source_id}")
        if state_record.normalized_event_count != normalized_state_record.normalized_event_count:
            raise SegmentationError(f"Segmented event count mismatch for source {source_id}")
        if state_record.phase2_committed_byte_end != normalized_state_record.phase1_committed_byte_end:
            raise SegmentationError(f"Segmented committed byte mismatch for source {source_id}")


def tombstone_state_record(
    source_id: str,
    normalized_state_record: NormalizationStateRecord,
    prior_state: SegmentationStateRecord | None,
    run_id: str,
) -> SegmentationStateRecord:
    segment_count = prior_state.segment_count if prior_state is not None else 0
    return SegmentationStateRecord(
        source_id=source_id,
        segmentation_schema_version=SEGMENTATION_SCHEMA_VERSION,
        normalization_schema_version=normalized_state_record.normalization_schema_version,
        normalized_event_count=normalized_state_record.normalized_event_count,
        phase2_committed_byte_end=normalized_state_record.phase1_committed_byte_end,
        status="tombstoned",
        segment_count=segment_count,
        last_segmented_at=utc_now(),
        last_run_id=run_id,
    )


def build_state_payload(state_records: dict[str, SegmentationStateRecord]) -> dict[str, object]:
    return {
        "schema_version": STATE_SCHEMA_VERSION,
        "segmentation_schema_version": SEGMENTATION_SCHEMA_VERSION,
        "generated_at": utc_now(),
        "source_count": len(state_records),
        "sources": [state_records[source_id].to_dict() for source_id in sorted(state_records)],
    }


def source_artifacts_exist(source_output_dir: Path) -> bool:
    return (
        (source_output_dir / "session_flow.json").exists()
        and (source_output_dir / "segments.jsonl").exists()
        and (source_output_dir / "stats.json").exists()
    )


def read_json_required(path: Path) -> dict[str, object]:
    payload = read_json_file(path)
    if payload is None:
        raise SegmentationError(f"Missing or invalid JSON artifact: {path}")
    return payload


def read_jsonl_required(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        raise SegmentationError(f"Missing JSONL artifact: {path}")
    records: list[dict[str, object]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.rstrip("\n")
            if not line:
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError as exc:
                raise SegmentationError(f"Invalid JSONL artifact line in {path}: {exc}") from exc
            if not isinstance(payload, dict):
                raise SegmentationError(f"JSONL artifact line is not an object in {path}")
            records.append(payload)
    return records


def promote_staged_sources(staging_root: Path, segmented_dir: Path, changed_source_ids: list[str]) -> None:
    if not changed_source_ids:
        return
    staged_sources_root = staging_root / "sources"
    backup_root = staging_root / "_backup"
    promoted: list[tuple[Path, Path, bool]] = []
    try:
        for source_id in changed_source_ids:
            staged_dir = staged_sources_root / source_id
            target_dir = segmented_dir / "sources" / source_id
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
        raise SegmentationError(f"Failed to promote staged segmented sources: {exc}") from exc


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


def extract_keywords(text_surfaces: list[dict[str, str]]) -> Counter[str]:
    keywords: Counter[str] = Counter()
    for item in text_surfaces:
        for token in tokenize_text(str(item.get("text", ""))):
            keywords[token] += 1
    return keywords


def tokenize_text(text: str) -> list[str]:
    tokens = re.findall(r"[a-z0-9][a-z0-9_-]{2,}", text.lower())
    return [token for token in tokens if token not in STOPWORDS and not token.isdigit()]


def dedupe_preserving_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        ordered.append(item)
    return ordered


def as_optional_str(value: Any) -> str | None:
    return value if isinstance(value, str) and value else None
