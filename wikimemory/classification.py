from __future__ import annotations

import json
import os
import re
import shutil
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from .discovery import DiscoveryError, atomic_write_text, ensure_directory, utc_now
from .normalization import append_jsonl_text, read_json_file, write_text_file
from .raw_event_resolver import RawEventResolver
from .segmentation import SegmentationStateRecord, load_segmentation_state

STATE_SCHEMA_VERSION = 1
CLASSIFICATION_SCHEMA_VERSION = 4
RESERVED_LABELS = {"cross-project", "unclassified"}
MATCHED_SIGNAL_FAMILIES = {"alias", "keyword", "path_hint", "repo_hint", "global_pattern", "context"}


class ClassificationError(DiscoveryError):
    """Fatal classification error that must stop the run."""


@dataclass(frozen=True)
class Thresholds:
    weak_min: int
    inferred_min: int
    strong_min: int
    dominance_gap: int
    cross_project_min: int
    global_secondary_min: int
    project_presence_min: int


@dataclass(frozen=True)
class RuleConfig:
    rule_id: str
    terms: tuple[str, ...]
    weight: int
    family: str


@dataclass(frozen=True)
class LabelConfig:
    label: str
    category: str
    aliases: tuple[RuleConfig, ...]
    keywords: tuple[RuleConfig, ...]
    path_hints: tuple[RuleConfig, ...]
    repo_hints: tuple[RuleConfig, ...]
    global_patterns: tuple[RuleConfig, ...]

    @property
    def all_rules(self) -> tuple[RuleConfig, ...]:
        return (
            *self.aliases,
            *self.keywords,
            *self.path_hints,
            *self.repo_hints,
            *self.global_patterns,
        )


@dataclass(frozen=True)
class TaxonomyConfig:
    schema_version: int
    taxonomy_version: int
    thresholds: Thresholds
    labels: tuple[LabelConfig, ...]

    @property
    def label_map(self) -> dict[str, LabelConfig]:
        return {label.label: label for label in self.labels}

    @property
    def project_labels(self) -> list[str]:
        return [label.label for label in self.labels if label.category == "project"]

    @property
    def global_labels(self) -> list[str]:
        return [label.label for label in self.labels if label.category == "global"]


@dataclass(frozen=True)
class ClassificationStateRecord:
    source_id: str
    classification_schema_version: int
    taxonomy_version: int
    segmentation_schema_version: int
    segmentation_last_run_id: str
    segment_count: int
    status: str
    last_classified_at: str
    last_run_id: str

    def to_dict(self) -> dict[str, object]:
        return {
            "source_id": self.source_id,
            "classification_schema_version": self.classification_schema_version,
            "taxonomy_version": self.taxonomy_version,
            "segmentation_schema_version": self.segmentation_schema_version,
            "segmentation_last_run_id": self.segmentation_last_run_id,
            "segment_count": self.segment_count,
            "status": self.status,
            "last_classified_at": self.last_classified_at,
            "last_run_id": self.last_run_id,
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "ClassificationStateRecord":
        return cls(
            source_id=str(data["source_id"]),
            classification_schema_version=int(data["classification_schema_version"]),
            taxonomy_version=int(data["taxonomy_version"]),
            segmentation_schema_version=int(data["segmentation_schema_version"]),
            segmentation_last_run_id=str(data.get("segmentation_last_run_id", "")),
            segment_count=int(data["segment_count"]),
            status=str(data["status"]),
            last_classified_at=str(data["last_classified_at"]),
            last_run_id=str(data["last_run_id"]),
        )


@dataclass(frozen=True)
class ClassificationNotice:
    run_id: str
    source_id: str
    segment_id: str
    severity: str
    notice_type: str
    summary: str

    def to_dict(self) -> dict[str, object]:
        return {
            "run_id": self.run_id,
            "source_id": self.source_id,
            "segment_id": self.segment_id,
            "severity": self.severity,
            "notice_type": self.notice_type,
            "summary": self.summary,
        }


@dataclass(frozen=True)
class ClassificationRunReport:
    run_id: str
    started_at: str
    finished_at: str
    source_status_counts: dict[str, int]
    classified_segment_count: int
    primary_label_counts: dict[str, int]
    confidence_counts: dict[str, int]
    notice_count: int
    success: bool
    fatal_error_summary: str | None

    def to_dict(self) -> dict[str, object]:
        return {
            "run_id": self.run_id,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "source_status_counts": self.source_status_counts,
            "classified_segment_count": self.classified_segment_count,
            "primary_label_counts": self.primary_label_counts,
            "confidence_counts": self.confidence_counts,
            "notice_count": self.notice_count,
            "success": self.success,
            "fatal_error_summary": self.fatal_error_summary,
        }


@dataclass(frozen=True)
class ClassificationResult:
    report: ClassificationRunReport
    state_path: Path
    run_log_path: Path
    notice_log_path: Path


@dataclass(frozen=True)
class ClassifiedSourceArtifacts:
    segment_records: list[dict[str, object]]
    stats_payload: dict[str, object]
    state_record: ClassificationStateRecord
    notices: list[ClassificationNotice]
    label_counts: Counter[str]
    confidence_counts: Counter[str]


@dataclass(frozen=True)
class SegmentContext:
    source_id: str
    segment_record: dict[str, object]
    segment_text: str
    topic_text: str
    dominant_kind_text: str
    path_text: str
    repo_text: str
    segment_has_content: bool


@dataclass(frozen=True)
class LabelMatch:
    score: int
    matched_signals: list[dict[str, object]]
    explicit: bool


@dataclass(frozen=True)
class ContextOverride:
    primary_label: str
    secondary_labels: tuple[str, ...]
    confidence: str
    decision_type: str
    matched_signals: tuple[dict[str, object], ...]
    classification_flags: tuple[str, ...]
    explanation: dict[str, object]


def run_classification(
    taxonomy_path: Path | str,
    state_dir: Path | str,
    normalized_dir: Path | str,
    segmented_dir: Path | str,
    classified_dir: Path | str,
    audits_dir: Path | str,
    source_ids: Iterable[str] | None = None,
    source_roots_config_path: Path | str | None = None,
) -> ClassificationResult:
    taxonomy_path = Path(taxonomy_path)
    state_dir = Path(state_dir)
    normalized_dir = Path(normalized_dir)
    segmented_dir = Path(segmented_dir)
    classified_dir = Path(classified_dir)
    audits_dir = Path(audits_dir)
    source_roots_config_path = Path(source_roots_config_path) if source_roots_config_path is not None else None

    state_path = state_dir / "classification_state.json"
    run_log_path = state_dir / "classification_runs.jsonl"
    notice_log_path = audits_dir / "classification_notices.jsonl"
    segmentation_state_path = state_dir / "segmentation_state.json"

    ensure_directory(state_dir)
    ensure_directory(audits_dir)
    ensure_directory(classified_dir / "sources")

    run_id = f"classify-{utc_now().replace(':', '').replace('.', '').replace('-', '')}"
    started_at = utc_now()
    staging_root = classified_dir / ".staging" / run_id
    changed_source_ids: list[str] = []

    previous_state_text = state_path.read_text(encoding="utf-8") if state_path.exists() else None
    previous_run_log_text = run_log_path.read_text(encoding="utf-8") if run_log_path.exists() else ""
    previous_notice_log_text = notice_log_path.read_text(encoding="utf-8") if notice_log_path.exists() else ""

    try:
        taxonomy = load_taxonomy(taxonomy_path)
        segmentation_state = load_segmentation_state(segmentation_state_path)
        previous_state = load_classification_state(state_path)
        next_state = dict(previous_state)
        target_source_ids = resolve_target_source_ids(source_ids, segmentation_state)
        raw_event_resolver = (
            RawEventResolver.from_paths(
                registry_path=state_dir / "source_registry.json",
                source_roots_config_path=source_roots_config_path,
            )
            if source_roots_config_path is not None
            else None
        )

        source_status_counts: Counter[str] = Counter()
        primary_label_counts: Counter[str] = Counter()
        confidence_counts: Counter[str] = Counter()
        classified_segment_count = 0
        notices_for_run: list[ClassificationNotice] = []

        for source_id in target_source_ids:
            segmentation_state_record = segmentation_state[source_id]
            source_output_dir = classified_dir / "sources" / source_id

            if segmentation_state_record.status == "tombstoned":
                next_state[source_id] = tombstone_state_record(
                    source_id=source_id,
                    segmentation_state_record=segmentation_state_record,
                    prior_state=previous_state.get(source_id),
                    taxonomy_version=taxonomy.taxonomy_version,
                    run_id=run_id,
                )
                source_status_counts["tombstoned"] += 1
                continue

            mode = determine_classification_mode(
                segmentation_state_record=segmentation_state_record,
                prior_state=previous_state.get(source_id),
                source_output_dir=source_output_dir,
                taxonomy_version=taxonomy.taxonomy_version,
            )
            if mode == "unchanged":
                next_state[source_id] = previous_state[source_id]
                source_status_counts["unchanged"] += 1
                continue

            staged_source_dir = staging_root / "sources" / source_id
            processed = classify_source(
                source_id=source_id,
                segmentation_state_record=segmentation_state_record,
                normalized_dir=normalized_dir,
                segmented_dir=segmented_dir,
                staged_source_dir=staged_source_dir,
                taxonomy=taxonomy,
                run_id=run_id,
                raw_event_resolver=raw_event_resolver,
            )
            validate_processed_source(
                source_id=source_id,
                segmentation_state_record=segmentation_state_record,
                taxonomy=taxonomy,
                processed=processed,
                staged_source_dir=staged_source_dir,
            )
            next_state[source_id] = processed.state_record
            source_status_counts["classified"] += 1
            primary_label_counts.update(processed.label_counts)
            confidence_counts.update(processed.confidence_counts)
            classified_segment_count += len(processed.segment_records)
            notices_for_run.extend(processed.notices)
            changed_source_ids.append(source_id)

        if source_ids is None:
            validate_state_against_segmentation(segmentation_state, next_state)

        staged_state_path = staging_root / "classification_state.json"
        staged_run_log_path = staging_root / "classification_runs.jsonl"
        staged_notice_log_path = staging_root / "classification_notices.jsonl"
        report = ClassificationRunReport(
            run_id=run_id,
            started_at=started_at,
            finished_at=utc_now(),
            source_status_counts=dict(sorted(source_status_counts.items())),
            classified_segment_count=classified_segment_count,
            primary_label_counts=dict(sorted(primary_label_counts.items())),
            confidence_counts=dict(sorted(confidence_counts.items())),
            notice_count=len(notices_for_run),
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
        write_text_file(
            staged_notice_log_path,
            append_jsonl_text(previous_notice_log_text, [notice.to_dict() for notice in notices_for_run]),
        )

        promote_staged_sources(
            staging_root=staging_root,
            classified_dir=classified_dir,
            changed_source_ids=changed_source_ids,
        )
        os.replace(staged_state_path, state_path)
        ensure_directory(run_log_path.parent)
        os.replace(staged_run_log_path, run_log_path)
        ensure_directory(notice_log_path.parent)
        os.replace(staged_notice_log_path, notice_log_path)
        cleanup_staging_root(staging_root)
        return ClassificationResult(
            report=report,
            state_path=state_path,
            run_log_path=run_log_path,
            notice_log_path=notice_log_path,
        )
    except Exception as exc:
        cleanup_staging_root(staging_root)
        failure_report = ClassificationRunReport(
            run_id=run_id,
            started_at=started_at,
            finished_at=utc_now(),
            source_status_counts={},
            classified_segment_count=0,
            primary_label_counts={},
            confidence_counts={},
            notice_count=0,
            success=False,
            fatal_error_summary=str(exc),
        )
        atomic_write_text(run_log_path, append_jsonl_text(previous_run_log_text, failure_report.to_dict()))
        if previous_state_text is None and state_path.exists():
            state_path.unlink(missing_ok=True)
        if previous_state_text is not None and state_path.exists():
            atomic_write_text(state_path, previous_state_text)
        if previous_notice_log_text:
            atomic_write_text(notice_log_path, previous_notice_log_text)
        return ClassificationResult(
            report=failure_report,
            state_path=state_path,
            run_log_path=run_log_path,
            notice_log_path=notice_log_path,
        )


def load_taxonomy(taxonomy_path: Path) -> TaxonomyConfig:
    try:
        payload = json.loads(taxonomy_path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError as exc:
        raise ClassificationError(f"Missing classification taxonomy: {taxonomy_path}") from exc
    except json.JSONDecodeError as exc:
        raise ClassificationError(f"Invalid classification taxonomy JSON: {taxonomy_path}") from exc

    labels_payload = payload.get("labels")
    thresholds_payload = payload.get("thresholds")
    if not isinstance(labels_payload, list) or not labels_payload:
        raise ClassificationError("Classification taxonomy must define labels")
    if not isinstance(thresholds_payload, dict):
        raise ClassificationError("Classification taxonomy must define thresholds")

    rule_ids: set[str] = set()
    labels: list[LabelConfig] = []
    for label_payload in labels_payload:
        label = str(label_payload["label"])
        if label in RESERVED_LABELS:
            raise ClassificationError(f"Reserved classification label may not appear in taxonomy config: {label}")
        category = str(label_payload["category"])
        if category not in {"project", "global"}:
            raise ClassificationError(f"Unsupported label category for {label}: {category}")
        if any(existing.label == label for existing in labels):
            raise ClassificationError(f"Duplicate classification label in taxonomy config: {label}")

        labels.append(
            LabelConfig(
                label=label,
                category=category,
                aliases=load_rules(label_payload, "aliases", "alias", rule_ids),
                keywords=load_rules(label_payload, "keywords", "keyword", rule_ids),
                path_hints=load_rules(label_payload, "path_hints", "path_hint", rule_ids),
                repo_hints=load_rules(label_payload, "repo_hints", "repo_hint", rule_ids),
                global_patterns=load_rules(label_payload, "global_patterns", "global_pattern", rule_ids),
            )
        )

    thresholds = Thresholds(
        weak_min=int(thresholds_payload["weak_min"]),
        inferred_min=int(thresholds_payload["inferred_min"]),
        strong_min=int(thresholds_payload["strong_min"]),
        dominance_gap=int(thresholds_payload["dominance_gap"]),
        cross_project_min=int(thresholds_payload["cross_project_min"]),
        global_secondary_min=int(thresholds_payload["global_secondary_min"]),
        project_presence_min=int(thresholds_payload["project_presence_min"]),
    )
    if thresholds.weak_min <= 0:
        raise ClassificationError("Classification taxonomy weak_min must be positive")
    if not any(label.category == "project" for label in labels):
        raise ClassificationError("Classification taxonomy must define at least one project label")
    if not any(label.category == "global" for label in labels):
        raise ClassificationError("Classification taxonomy must define at least one global label")
    return TaxonomyConfig(
        schema_version=int(payload["schema_version"]),
        taxonomy_version=int(payload["taxonomy_version"]),
        thresholds=thresholds,
        labels=tuple(labels),
    )


def load_rules(
    label_payload: dict[str, object],
    key: str,
    family: str,
    rule_ids: set[str],
) -> tuple[RuleConfig, ...]:
    rules_payload = label_payload.get(key, [])
    if rules_payload is None:
        return ()
    if not isinstance(rules_payload, list):
        raise ClassificationError(f"Classification taxonomy field {key} must be a list")
    rules: list[RuleConfig] = []
    for item in rules_payload:
        if not isinstance(item, dict):
            raise ClassificationError(f"Classification taxonomy rule in {key} must be an object")
        rule_id = str(item["id"])
        if rule_id in rule_ids:
            raise ClassificationError(f"Duplicate classification rule id in taxonomy config: {rule_id}")
        terms_payload = item.get("terms")
        if not isinstance(terms_payload, list) or not terms_payload:
            raise ClassificationError(f"Classification taxonomy rule {rule_id} must define terms")
        terms = tuple(str(term).strip().lower() for term in terms_payload if str(term).strip())
        if not terms:
            raise ClassificationError(f"Classification taxonomy rule {rule_id} has no usable terms")
        rule = RuleConfig(
            rule_id=rule_id,
            terms=terms,
            weight=int(item["weight"]),
            family=family,
        )
        rules.append(rule)
        rule_ids.add(rule_id)
    return tuple(rules)


def load_classification_state(state_path: Path) -> dict[str, ClassificationStateRecord]:
    if not state_path.exists():
        return {}
    try:
        payload = json.loads(state_path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise ClassificationError(f"Invalid classification state JSON: {state_path}") from exc
    if int(payload.get("schema_version", -1)) != STATE_SCHEMA_VERSION:
        raise ClassificationError(
            f"Unsupported classification state schema version in {state_path}: {payload.get('schema_version')}"
        )
    records = [ClassificationStateRecord.from_dict(item) for item in payload.get("sources", [])]
    return {record.source_id: record for record in records}


def resolve_target_source_ids(
    source_ids: Iterable[str] | None,
    segmentation_state: dict[str, SegmentationStateRecord],
) -> list[str]:
    if source_ids is None:
        return sorted(segmentation_state)
    target_source_ids = sorted(dict.fromkeys(str(source_id) for source_id in source_ids))
    missing = [source_id for source_id in target_source_ids if source_id not in segmentation_state]
    if missing:
        raise ClassificationError(
            f"Requested source_ids are missing from segmentation state: {', '.join(missing)}"
        )
    return target_source_ids


def determine_classification_mode(
    segmentation_state_record: SegmentationStateRecord,
    prior_state: ClassificationStateRecord | None,
    source_output_dir: Path,
    taxonomy_version: int,
) -> str:
    if prior_state is None:
        return "full"
    if prior_state.status != "classified":
        return "full"
    if prior_state.classification_schema_version != CLASSIFICATION_SCHEMA_VERSION:
        return "full"
    if prior_state.taxonomy_version != taxonomy_version:
        return "full"
    if prior_state.segmentation_schema_version != segmentation_state_record.segmentation_schema_version:
        return "full"
    if prior_state.segmentation_last_run_id != segmentation_state_record.last_run_id:
        return "full"
    if prior_state.segment_count != segmentation_state_record.segment_count:
        return "full"
    if not source_artifacts_exist(source_output_dir):
        return "full"
    return "unchanged"


def classify_source(
    source_id: str,
    segmentation_state_record: SegmentationStateRecord,
    normalized_dir: Path,
    segmented_dir: Path,
    staged_source_dir: Path,
    taxonomy: TaxonomyConfig,
    run_id: str,
    raw_event_resolver: RawEventResolver | None,
) -> ClassifiedSourceArtifacts:
    ensure_directory(staged_source_dir)
    normalized_source_dir = normalized_dir / "sources" / source_id
    segmented_source_dir = segmented_dir / "sources" / source_id

    normalized_session = read_json_required(normalized_source_dir / "session.json")
    normalized_events = read_jsonl_required(normalized_source_dir / "events.jsonl")
    segmented_session_flow = read_json_required(segmented_source_dir / "session_flow.json")
    segmented_segments = read_jsonl_required(segmented_source_dir / "segments.jsonl")

    if len(segmented_segments) != segmentation_state_record.segment_count:
        raise ClassificationError(
            f"Segment count mismatch for source {source_id}: {len(segmented_segments)} != {segmentation_state_record.segment_count}"
        )

    classified_segments: list[dict[str, object]] = []
    label_counts: Counter[str] = Counter()
    confidence_counts: Counter[str] = Counter()

    for segment_record in segmented_segments:
        context = build_segment_context(
            source_id=source_id,
            segment_record=segment_record,
            normalized_session=normalized_session,
            normalized_events=normalized_events,
            raw_event_resolver=raw_event_resolver,
        )
        classified_segment, _segment_notices = classify_segment(
            source_id=source_id,
            segment_record=segment_record,
            context=context,
            taxonomy=taxonomy,
            run_id=run_id,
        )
        classified_segments.append(classified_segment)

    classified_segments = apply_contextual_overrides(classified_segments, taxonomy)

    notices: list[ClassificationNotice] = []
    for classified_segment in classified_segments:
        notices.extend(
            build_segment_notices(
                source_id=source_id,
                segment_id=str(classified_segment["segment_id"]),
                primary_label=str(classified_segment["primary_label"]),
                confidence=str(classified_segment["confidence"]),
                matched_signals=[dict(item) for item in classified_segment.get("matched_signals", [])],
                decision_type=str(classified_segment["classification_explanation"]["decision_type"]),
                run_id=run_id,
                segment_has_content=bool(
                    classified_segment.get("text_surface_char_count", 0)
                    or classified_segment.get("topic_hints")
                    or classified_segment.get("dominant_kinds")
                ),
            )
        )
        label_counts[classified_segment["primary_label"]] += 1
        confidence_counts[classified_segment["confidence"]] += 1

    stats_payload = {
        "source_id": source_id,
        "session_id": normalized_session["session_id"],
        "classification_schema_version": CLASSIFICATION_SCHEMA_VERSION,
        "taxonomy_version": taxonomy.taxonomy_version,
        "segmentation_schema_version": segmentation_state_record.segmentation_schema_version,
        "segment_count": len(classified_segments),
        "primary_label_counts": dict(sorted(label_counts.items())),
        "confidence_counts": dict(sorted(confidence_counts.items())),
        "notice_counts": dict(sorted(Counter(notice.notice_type for notice in notices).items())),
        "session_flow_summary": {
            "normalized_event_count": segmented_session_flow["normalized_event_count"],
            "flow_window_count": len(segmented_session_flow.get("flow_windows", [])),
            "detected_call_chain_count": len(segmented_session_flow.get("detected_call_chains", [])),
        },
    }

    write_text_file(
        staged_source_dir / "segments.jsonl",
        "".join(json.dumps(record, separators=(",", ":"), sort_keys=True) + "\n" for record in classified_segments),
    )
    write_text_file(
        staged_source_dir / "stats.json",
        json.dumps(stats_payload, indent=2, sort_keys=True) + "\n",
    )

    state_record = ClassificationStateRecord(
        source_id=source_id,
        classification_schema_version=CLASSIFICATION_SCHEMA_VERSION,
        taxonomy_version=taxonomy.taxonomy_version,
        segmentation_schema_version=segmentation_state_record.segmentation_schema_version,
        segmentation_last_run_id=segmentation_state_record.last_run_id,
        segment_count=len(classified_segments),
        status="classified",
        last_classified_at=utc_now(),
        last_run_id=run_id,
    )
    return ClassifiedSourceArtifacts(
        segment_records=classified_segments,
        stats_payload=stats_payload,
        state_record=state_record,
        notices=notices,
        label_counts=label_counts,
        confidence_counts=confidence_counts,
    )


def build_segment_context(
    source_id: str,
    segment_record: dict[str, object],
    normalized_session: dict[str, object],
    normalized_events: list[dict[str, object]],
    raw_event_resolver: RawEventResolver | None,
) -> SegmentContext:
    start_line = int(segment_record["start_line_no"])
    end_line = int(segment_record["end_line_no"])
    if start_line < 1 or end_line > len(normalized_events) or end_line < start_line:
        raise ClassificationError(f"Invalid segment line bounds for source {source_id}")

    event_slice = normalized_events[start_line - 1 : end_line]
    if [int(event["source_line_no"]) for event in event_slice] != list(range(start_line, end_line + 1)):
        raise ClassificationError(f"Segment line slice is not contiguous for source {source_id}")

    unique_texts: list[str] = []
    seen_texts: set[str] = set()
    for event in event_slice:
        surfaces = (
            raw_event_resolver.collect_text_surfaces(event)
            if raw_event_resolver is not None and bool(event.get("text_surface_truncated"))
            else event.get("text_surfaces", [])
        )
        for item in surfaces:
            text = str(item.get("text", "")).strip()
            lowered = text.lower()
            if text and lowered not in seen_texts:
                seen_texts.add(lowered)
                unique_texts.append(text)

    topic_hints = [str(item).strip() for item in segment_record.get("topic_hints", []) if str(item).strip()]
    dominant_kinds = [str(item).strip() for item in segment_record.get("dominant_kinds", []) if str(item).strip()]
    relative_path = str(normalized_session.get("relative_path", "")).strip()
    session_meta_fields = normalized_session.get("session_meta_fields", {})
    cwd = str(session_meta_fields.get("cwd", "")).strip() if isinstance(session_meta_fields, dict) else ""

    path_text = normalize_path_text(" ".join(part for part in (relative_path, cwd) if part))
    repo_text = normalize_path_text(" ".join(collect_repo_tokens(relative_path, cwd)))
    segment_text = normalize_text(" ".join([*topic_hints, *dominant_kinds, *unique_texts]))
    topic_text = normalize_text(" ".join(topic_hints))
    dominant_kind_text = normalize_text(" ".join(dominant_kinds))

    return SegmentContext(
        source_id=source_id,
        segment_record=segment_record,
        segment_text=segment_text,
        topic_text=topic_text,
        dominant_kind_text=dominant_kind_text,
        path_text=path_text,
        repo_text=repo_text,
        segment_has_content=bool(segment_text or path_text or repo_text),
    )


def classify_segment(
    source_id: str,
    segment_record: dict[str, object],
    context: SegmentContext,
    taxonomy: TaxonomyConfig,
    run_id: str,
) -> tuple[dict[str, object], list[ClassificationNotice]]:
    label_matches = {
        label.label: score_label(label, context)
        for label in taxonomy.labels
    }
    label_scores = {
        label: match.score
        for label, match in label_matches.items()
    }
    sorted_labels = sorted(label_scores.items(), key=lambda item: (-item[1], item[0]))
    project_labels = taxonomy.project_labels
    project_scores = sorted(
        [(label, label_scores[label]) for label in project_labels],
        key=lambda item: (-item[1], item[0]),
    )
    best_project_label, best_project_score = first_or_default(project_scores)
    second_project_score = project_scores[1][1] if len(project_scores) > 1 else 0
    best_global_label, best_global_score = best_label_for_category(taxonomy, label_scores, "global")

    strong_projects = [
        label
        for label, score in project_scores
        if score >= taxonomy.thresholds.cross_project_min
    ]
    cross_project = (
        len(strong_projects) >= 2
        and (best_project_score - second_project_score) < taxonomy.thresholds.dominance_gap
        and not explicit_preference_wins(label_matches, project_scores)
    )

    project_clear = best_project_label is not None and (
        (label_matches[best_project_label].explicit and best_project_score >= taxonomy.thresholds.weak_min)
        or (
            best_project_score >= taxonomy.thresholds.project_presence_min
            and (
                len(project_scores) == 1
                or (best_project_score - second_project_score) >= taxonomy.thresholds.dominance_gap
            )
        )
    )

    primary_label: str
    secondary_labels: list[str] = []
    decision_type: str

    if cross_project:
        primary_label = "cross-project"
        secondary_labels = strong_projects
        if best_global_label is not None and best_global_score >= taxonomy.thresholds.global_secondary_min:
            secondary_labels.append(best_global_label)
        decision_type = "mixed"
    elif project_clear:
        primary_label = best_project_label
        if best_global_label is not None and best_global_score >= taxonomy.thresholds.global_secondary_min:
            secondary_labels.append(best_global_label)
        decision_type = "explicit" if label_matches[best_project_label].explicit else "weighted"
    elif best_global_label is not None and best_global_score >= taxonomy.thresholds.weak_min:
        primary_label = best_global_label
        decision_type = "explicit" if label_matches[best_global_label].explicit else "weighted"
    else:
        primary_label = "unclassified"
        decision_type = "downgraded_unclassified"

    secondary_labels = dedupe_preserving_order(
        [label for label in secondary_labels if label != primary_label]
    )
    confidence = determine_confidence(
        primary_label=primary_label,
        decision_type=decision_type,
        best_score=max((score for _, score in sorted_labels), default=0),
        label_matches=label_matches,
        primary_candidates=secondary_labels if primary_label == "cross-project" else [primary_label],
        thresholds=taxonomy.thresholds,
    )

    primary_and_secondary = (
        secondary_labels if primary_label == "cross-project" else [primary_label, *secondary_labels]
    )
    matched_signals = collect_matched_signals(label_matches, primary_and_secondary)
    explanation = build_classification_explanation(
        primary_label=primary_label,
        secondary_labels=secondary_labels,
        confidence=confidence,
        decision_type=decision_type,
        label_scores=label_scores,
        matched_signals=matched_signals,
    )

    classification_flags: list[str] = []
    if primary_label == "cross-project":
        classification_flags.append("cross_project")
    if "global" in secondary_labels:
        classification_flags.append("has_global_secondary")
    if primary_label == "unclassified":
        classification_flags.append("conservative_unclassified")
    if confidence == "weak":
        classification_flags.append("low_confidence")
    if any(label_matches.get(label, LabelMatch(0, [], False)).explicit for label in primary_and_secondary):
        classification_flags.append("explicit_signal")

    classified_segment = dict(segment_record)
    classified_segment.update(
        {
            "primary_label": primary_label,
            "secondary_labels": secondary_labels,
            "confidence": confidence,
            "classification_explanation": explanation,
            "matched_signals": matched_signals,
            "label_scores": dict(sorted(label_scores.items())),
            "classification_flags": classification_flags,
        }
    )
    notices = build_segment_notices(
        source_id=source_id,
        segment_id=str(segment_record["segment_id"]),
        primary_label=primary_label,
        confidence=confidence,
        matched_signals=matched_signals,
        decision_type=decision_type,
        run_id=run_id,
        segment_has_content=context.segment_has_content,
    )
    return classified_segment, notices


def score_label(label: LabelConfig, context: SegmentContext) -> LabelMatch:
    score = 0
    matched_signals: list[dict[str, object]] = []
    explicit = False

    for rule in label.all_rules:
        match_source, matched_term = match_rule(rule, context)
        if match_source is None:
            continue
        score += rule.weight
        matched_signals.append(
            {
                "label": label.label,
                "rule_id": rule.rule_id,
                "signal_family": rule.family,
                "matched_term": matched_term,
                "weight": rule.weight,
                "evidence_source": match_source,
            }
        )
        if rule.family in {"alias", "global_pattern"}:
            explicit = True
    return LabelMatch(score=score, matched_signals=matched_signals, explicit=explicit)


def match_rule(rule: RuleConfig, context: SegmentContext) -> tuple[str | None, str | None]:
    if rule.family == "path_hint":
        return match_terms(rule.terms, [("path", context.path_text)], is_path=True)
    if rule.family == "repo_hint":
        return match_terms(rule.terms, [("repo", context.repo_text)], is_path=True)
    if rule.family == "keyword":
        return match_terms(
            rule.terms,
            [
                ("topic_hints", context.topic_text),
                ("dominant_kinds", context.dominant_kind_text),
                ("segment_text", context.segment_text),
            ],
        )
    return match_terms(
        rule.terms,
        [
            ("topic_hints", context.topic_text),
            ("segment_text", context.segment_text),
            ("dominant_kinds", context.dominant_kind_text),
        ],
    )


def match_terms(
    terms: tuple[str, ...],
    sources: list[tuple[str, str]],
    is_path: bool = False,
) -> tuple[str | None, str | None]:
    for match_source, text in sources:
        if not text:
            continue
        for term in terms:
            if term_matches(term, text, is_path=is_path):
                return match_source, term
    return None, None


def term_matches(term: str, text: str, is_path: bool = False) -> bool:
    if not text:
        return False
    term = term.strip().lower()
    text = text.lower()
    if not term:
        return False
    if is_path:
        return normalize_path_text(term) in text
    if any(char in term for char in (" ", "-", "_", "\\", "/", ".")):
        return term in text
    return re.search(rf"(?<![a-z0-9]){re.escape(term)}(?![a-z0-9])", text) is not None


def explicit_preference_wins(
    label_matches: dict[str, LabelMatch],
    project_scores: list[tuple[str, int]],
) -> bool:
    if len(project_scores) < 2:
        return False
    best_label, best_score = project_scores[0]
    second_label, second_score = project_scores[1]
    if best_score <= second_score:
        return False
    return label_matches[best_label].explicit and not label_matches[second_label].explicit


def determine_confidence(
    primary_label: str,
    decision_type: str,
    best_score: int,
    label_matches: dict[str, LabelMatch],
    primary_candidates: list[str],
    thresholds: Thresholds,
) -> str:
    if primary_label == "unclassified":
        return "weak"
    if decision_type == "mixed":
        if all(label_matches.get(label, LabelMatch(0, [], False)).explicit for label in primary_candidates):
            return "explicit"
        if best_score >= thresholds.strong_min:
            return "strong"
        return "inferred"
    if any(label_matches.get(label, LabelMatch(0, [], False)).explicit for label in primary_candidates):
        return "explicit"
    if best_score >= thresholds.strong_min:
        return "strong"
    if best_score >= thresholds.inferred_min:
        return "inferred"
    return "weak"


def collect_matched_signals(
    label_matches: dict[str, LabelMatch],
    labels: list[str],
) -> list[dict[str, object]]:
    signals: list[dict[str, object]] = []
    seen: set[tuple[str, str]] = set()
    for label in labels:
        for signal in label_matches.get(label, LabelMatch(0, [], False)).matched_signals:
            key = (str(signal["label"]), str(signal["rule_id"]))
            if key in seen:
                continue
            seen.add(key)
            signals.append(signal)
    return sorted(
        signals,
        key=lambda item: (-int(item["weight"]), str(item["label"]), str(item["rule_id"])),
    )


def build_classification_explanation(
    primary_label: str,
    secondary_labels: list[str],
    confidence: str,
    decision_type: str,
    label_scores: dict[str, int],
    matched_signals: list[dict[str, object]],
) -> dict[str, object]:
    if primary_label == "cross-project":
        winning_reason = "multiple strong project labels scored closely, so the segment stayed mixed"
    elif primary_label == "unclassified":
        winning_reason = "evidence stayed below the conservative assignment threshold"
    elif decision_type == "explicit":
        winning_reason = "explicit project or global naming signals dominated the decision"
    else:
        winning_reason = "weighted taxonomy signals produced a clear winning label"

    competing_labels = [
        {"label": label, "score": score}
        for label, score in sorted(label_scores.items(), key=lambda item: (-item[1], item[0]))
        if score > 0 and label != primary_label
    ][:3]
    return {
        "decision_type": decision_type,
        "winning_label_reason": winning_reason,
        "primary_label": primary_label,
        "secondary_labels": secondary_labels,
        "confidence": confidence,
        "competing_labels": competing_labels,
        "matched_rule_ids": [str(signal["rule_id"]) for signal in matched_signals],
        "signal_families": sorted({str(signal["signal_family"]) for signal in matched_signals}),
    }


def build_segment_notices(
    source_id: str,
    segment_id: str,
    primary_label: str,
    confidence: str,
    matched_signals: list[dict[str, object]],
    decision_type: str,
    run_id: str,
    segment_has_content: bool,
) -> list[ClassificationNotice]:
    notices: list[ClassificationNotice] = []
    if primary_label == "unclassified":
        notice_type = "taxonomy_gap" if segment_has_content and not matched_signals else "unclassified"
        summary = (
            "segment had usable content but no taxonomy signals matched"
            if notice_type == "taxonomy_gap"
            else "segment stayed unclassified under conservative thresholds"
        )
        notices.append(
            ClassificationNotice(
                run_id=run_id,
                source_id=source_id,
                segment_id=segment_id,
                severity="warning",
                notice_type=notice_type,
                summary=summary,
            )
        )
        return notices
    if primary_label == "cross-project":
        notices.append(
            ClassificationNotice(
                run_id=run_id,
                source_id=source_id,
                segment_id=segment_id,
                severity="warning",
                notice_type="conflicting_signals",
                summary="segment matched multiple strong project labels without a clear winner",
            )
        )
    elif confidence == "weak":
        notices.append(
            ClassificationNotice(
                run_id=run_id,
                source_id=source_id,
                segment_id=segment_id,
                severity="warning",
                notice_type="low_confidence",
                summary="segment classification remained below strong confidence thresholds",
            )
        )
    elif decision_type == "weighted" and not matched_signals:
        notices.append(
            ClassificationNotice(
                run_id=run_id,
                source_id=source_id,
                segment_id=segment_id,
                severity="warning",
                notice_type="taxonomy_gap",
                summary="segment classification succeeded without any persisted matched signals",
            )
        )
    return notices


def apply_contextual_overrides(
    classified_segments: list[dict[str, object]],
    taxonomy: TaxonomyConfig,
) -> list[dict[str, object]]:
    if not classified_segments:
        return classified_segments

    current_segments = [dict(segment) for segment in classified_segments]
    max_passes = max(1, len(current_segments))

    for _ in range(max_passes):
        turn_index: dict[str, list[int]] = {}
        for index, segment in enumerate(current_segments):
            for turn_id in extract_turn_ids(segment):
                turn_index.setdefault(turn_id, []).append(index)

        changed = False
        next_segments: list[dict[str, object]] = []
        for index, segment in enumerate(current_segments):
            updated = dict(segment)
            override = resolve_context_override(
                index=index,
                segments=current_segments,
                turn_index=turn_index,
                taxonomy=taxonomy,
            )
            if override is None:
                next_segments.append(updated)
                continue

            updated["primary_label"] = override.primary_label
            updated["secondary_labels"] = list(override.secondary_labels)
            updated["confidence"] = override.confidence
            updated["matched_signals"] = [dict(item) for item in override.matched_signals]
            updated["classification_flags"] = dedupe_preserving_order(
                [
                    flag
                    for flag in [
                        *override.classification_flags,
                        *[
                            str(item)
                            for item in updated.get("classification_flags", [])
                            if str(item) != "conservative_unclassified"
                        ],
                    ]
                    if flag
                ]
            )
            updated["classification_explanation"] = dict(override.explanation)
            if updated != segment:
                changed = True
            next_segments.append(updated)

        current_segments = next_segments
        if not changed:
            break

    return current_segments


def resolve_context_override(
    index: int,
    segments: list[dict[str, object]],
    turn_index: dict[str, list[int]],
    taxonomy: TaxonomyConfig,
) -> ContextOverride | None:
    current = segments[index]
    primary_label = str(current.get("primary_label", ""))
    confidence = str(current.get("confidence", ""))
    if primary_label != "unclassified" and confidence not in {"weak"}:
        return None
    if not is_contextual_segment(current):
        return None

    by_turn = resolve_turn_context_override(index, segments, turn_index, taxonomy)
    if by_turn is not None:
        return by_turn
    by_neighbor = resolve_neighbor_context_override(index, segments, taxonomy)
    if by_neighbor is not None:
        return by_neighbor
    by_window = resolve_window_context_override(index, segments, taxonomy)
    if by_window is not None:
        return by_window
    return resolve_source_context_override(index, segments, taxonomy)


def resolve_turn_context_override(
    index: int,
    segments: list[dict[str, object]],
    turn_index: dict[str, list[int]],
    taxonomy: TaxonomyConfig,
) -> ContextOverride | None:
    current = segments[index]
    turn_ids = extract_turn_ids(current)
    if not turn_ids:
        return None

    candidate_labels: Counter[str] = Counter()
    explicit_labels: set[str] = set()
    supporting_indices: list[int] = []
    for turn_id in turn_ids:
        for candidate_index in turn_index.get(turn_id, []):
            if candidate_index == index:
                continue
            candidate = segments[candidate_index]
            candidate_label = str(candidate.get("primary_label", ""))
            if candidate_label == "unclassified":
                continue
            candidate_labels[candidate_label] += 1
            supporting_indices.append(candidate_index)
            if has_explicit_signal(candidate):
                explicit_labels.add(candidate_label)

    if not candidate_labels:
        return None
    best_label, best_count = candidate_labels.most_common(1)[0]
    second_count = candidate_labels.most_common(2)[1][1] if len(candidate_labels) > 1 else 0
    if best_count <= second_count:
        return None

    confidence = "strong" if best_label in explicit_labels and best_count >= 2 else "inferred"
    signal = {
        "label": best_label,
        "rule_id": "context.turn_id",
        "signal_family": "context",
        "matched_term": ",".join(turn_ids),
        "weight": taxonomy.thresholds.project_presence_min,
        "evidence_source": "turn_context",
    }
    return build_context_override(
        label=best_label,
        confidence=confidence,
        signal=signal,
        decision_reason="shared turn context carried a stable label across adjacent segment slices",
        supporting_segments=[segments[i] for i in sorted(set(supporting_indices))],
    )


def resolve_neighbor_context_override(
    index: int,
    segments: list[dict[str, object]],
    taxonomy: TaxonomyConfig,
) -> ContextOverride | None:
    previous = nearest_labeled_segment(index, segments, step=-1)
    following = nearest_labeled_segment(index, segments, step=1)
    if previous is None and following is None:
        return None

    if previous is not None and following is not None:
        previous_label = str(previous.get("primary_label", ""))
        following_label = str(following.get("primary_label", ""))
        if previous_label and previous_label == following_label:
            signal = {
                "label": previous_label,
                "rule_id": "context.neighbor_consensus",
                "signal_family": "context",
                "matched_term": f"{previous.get('segment_id')}|{following.get('segment_id')}",
                "weight": taxonomy.thresholds.project_presence_min,
                "evidence_source": "neighbor_context",
            }
            confidence = "strong" if has_explicit_signal(previous) or has_explicit_signal(following) else "inferred"
            return build_context_override(
                label=previous_label,
                confidence=confidence,
                signal=signal,
                decision_reason="neighboring segments agreed on the dominant label and the current segment was low-signal context",
                supporting_segments=[previous, following],
            )

    inherited = previous or following
    if inherited is None:
        return None
    inherited_label = str(inherited.get("primary_label", ""))
    if inherited_label == "unclassified":
        return None
    signal = {
        "label": inherited_label,
        "rule_id": "context.neighbor_inheritance",
        "signal_family": "context",
        "matched_term": str(inherited.get("segment_id")),
        "weight": taxonomy.thresholds.weak_min,
        "evidence_source": "neighbor_context",
    }
    return build_context_override(
        label=inherited_label,
        confidence="inferred",
        signal=signal,
        decision_reason="the nearest labeled neighbor provided the best available context for a low-signal segment",
        supporting_segments=[inherited],
    )


def resolve_window_context_override(
    index: int,
    segments: list[dict[str, object]],
    taxonomy: TaxonomyConfig,
    max_distance: int = 8,
) -> ContextOverride | None:
    label_weights: Counter[str] = Counter()
    explicit_labels: set[str] = set()
    supporting_indices_by_label: dict[str, list[int]] = {}

    for candidate_index in range(max(0, index - max_distance), min(len(segments), index + max_distance + 1)):
        if candidate_index == index:
            continue
        candidate = segments[candidate_index]
        candidate_label = str(candidate.get("primary_label", ""))
        if candidate_label == "unclassified":
            continue
        weight = contextual_support_weight(candidate)
        label_weights[candidate_label] += weight
        supporting_indices_by_label.setdefault(candidate_label, []).append(candidate_index)
        if has_explicit_signal(candidate):
            explicit_labels.add(candidate_label)

    if not label_weights:
        return None

    ranked_labels = label_weights.most_common(2)
    best_label, best_weight = ranked_labels[0]
    second_weight = ranked_labels[1][1] if len(ranked_labels) > 1 else 0
    supporting_indices = supporting_indices_by_label.get(best_label, [])

    if best_weight <= second_weight:
        return None
    if best_weight < 2 and best_label not in explicit_labels:
        return None

    signal = {
        "label": best_label,
        "rule_id": "context.window_consensus",
        "signal_family": "context",
        "matched_term": str(max_distance),
        "weight": taxonomy.thresholds.project_presence_min,
        "evidence_source": "window_context",
    }
    confidence = "strong" if best_label in explicit_labels or best_weight >= 4 else "inferred"
    return build_context_override(
        label=best_label,
        confidence=confidence,
        signal=signal,
        decision_reason="nearby labeled segments formed a stable context window around a weak local slice",
        supporting_segments=[segments[i] for i in sorted(set(supporting_indices))[:5]],
    )


def resolve_source_context_override(
    index: int,
    segments: list[dict[str, object]],
    taxonomy: TaxonomyConfig,
) -> ContextOverride | None:
    del index
    label_weights: Counter[str] = Counter()
    explicit_labels: set[str] = set()
    supporting_segments_by_label: dict[str, list[dict[str, object]]] = {}

    for segment in segments:
        label = str(segment.get("primary_label", ""))
        if label == "unclassified":
            continue
        weight = contextual_support_weight(segment)
        label_weights[label] += weight
        supporting_segments_by_label.setdefault(label, []).append(segment)
        if has_explicit_signal(segment):
            explicit_labels.add(label)

    if not label_weights:
        return None

    ranked_labels = label_weights.most_common(2)
    best_label, best_weight = ranked_labels[0]
    second_weight = ranked_labels[1][1] if len(ranked_labels) > 1 else 0
    total_weight = sum(label_weights.values())

    if best_weight < 6:
        return None
    if (best_weight - second_weight) < 3:
        return None
    if total_weight > 0 and (best_weight / total_weight) < 0.45:
        return None

    signal = {
        "label": best_label,
        "rule_id": "context.source_dominance",
        "signal_family": "context",
        "matched_term": f"{best_weight}:{total_weight}",
        "weight": taxonomy.thresholds.project_presence_min,
        "evidence_source": "source_context",
    }
    confidence = "strong" if best_label in explicit_labels and best_weight >= 8 else "inferred"
    return build_context_override(
        label=best_label,
        confidence=confidence,
        signal=signal,
        decision_reason="the source carried a dominant label across many stronger segments, so this weak slice inherited that context",
        supporting_segments=supporting_segments_by_label.get(best_label, [])[:5],
    )


def build_context_override(
    label: str,
    confidence: str,
    signal: dict[str, object],
    decision_reason: str,
    supporting_segments: list[dict[str, object]],
) -> ContextOverride:
    secondary_labels = dedupe_preserving_order(
        [
            secondary
            for segment in supporting_segments
            for secondary in [str(item) for item in segment.get("secondary_labels", [])]
            if secondary and secondary != label
        ]
    )
    return ContextOverride(
        primary_label=label,
        secondary_labels=tuple(secondary_labels),
        confidence=confidence,
        decision_type="contextual",
        matched_signals=(signal,),
        classification_flags=("contextual_inheritance",),
        explanation={
            "decision_type": "contextual",
            "winning_label_reason": decision_reason,
            "primary_label": label,
            "secondary_labels": secondary_labels,
            "confidence": confidence,
            "competing_labels": [],
            "matched_rule_ids": [str(signal["rule_id"])],
            "signal_families": [str(signal["signal_family"])],
        },
    )


def extract_turn_ids(segment: dict[str, object]) -> list[str]:
    explicit_link_ids = segment.get("explicit_link_ids", {})
    if not isinstance(explicit_link_ids, dict):
        return []
    turn_ids = explicit_link_ids.get("turn_id", [])
    if not isinstance(turn_ids, list):
        return []
    return [str(item) for item in turn_ids if str(item)]


def has_explicit_signal(segment: dict[str, object]) -> bool:
    return "explicit_signal" in [str(item) for item in segment.get("classification_flags", [])]


def contextual_support_weight(segment: dict[str, object]) -> int:
    confidence = str(segment.get("confidence", ""))
    if has_explicit_signal(segment):
        return 3
    if confidence == "strong":
        return 2
    return 1


def is_contextual_segment(segment: dict[str, object]) -> bool:
    dominant_kinds = [str(item) for item in segment.get("dominant_kinds", [])]
    if not dominant_kinds:
        return False
    if any(
        any(
            token in kind
            for token in (
                "reasoning",
                "function_call",
                "function_call_output",
                "web_search_call",
                "agent_message",
                "token_count",
            )
        )
        for kind in dominant_kinds
    ):
        return True

    text_surface_char_count = int(segment.get("text_surface_char_count", 0) or 0)
    low_signal_message_kinds = {
        "response_item.message",
        "event_msg.agent_message",
        "event_msg.task_complete",
        "event_msg.task_started",
        "event_msg.token_count",
    }
    has_only_low_signal_messages = all(kind in low_signal_message_kinds for kind in dominant_kinds)
    has_high_signal_user_content = any(
        any(token in kind for token in ("user_message", "turn_context"))
        for kind in dominant_kinds
    )
    if has_only_low_signal_messages and not has_high_signal_user_content and text_surface_char_count <= 1500:
        return True

    weak_context_kinds = {
        "event_msg.generic",
        "response_item.message",
        "event_msg.agent_message",
        "event_msg.user_message",
        "turn_context",
        "session_meta",
        "event_msg.task_started",
        "event_msg.task_complete",
        "event_msg.turn_aborted",
        "event_msg.token_count",
    }
    classification_flags = {str(item) for item in segment.get("classification_flags", [])}
    has_matched_signals = bool(segment.get("matched_signals"))
    is_weak_generic_context = all(kind in weak_context_kinds for kind in dominant_kinds)
    is_weak_segment = "low_confidence" in classification_flags or str(segment.get("primary_label", "")) == "unclassified"
    return is_weak_segment and is_weak_generic_context and (text_surface_char_count <= 400 or not has_matched_signals)


def nearest_labeled_segment(
    index: int,
    segments: list[dict[str, object]],
    step: int,
    max_distance: int = 2,
) -> dict[str, object] | None:
    distance = 0
    cursor = index + step
    while 0 <= cursor < len(segments) and distance < max_distance:
        candidate = segments[cursor]
        if str(candidate.get("primary_label", "")) != "unclassified":
            return candidate
        cursor += step
        distance += 1
    return None


def validate_processed_source(
    source_id: str,
    segmentation_state_record: SegmentationStateRecord,
    taxonomy: TaxonomyConfig,
    processed: ClassifiedSourceArtifacts,
    staged_source_dir: Path,
) -> None:
    segments_path = staged_source_dir / "segments.jsonl"
    stats_payload = processed.stats_payload
    classified_segments = read_jsonl_required(segments_path)
    if len(classified_segments) != segmentation_state_record.segment_count:
        raise ClassificationError(f"Classified segment count mismatch for source {source_id}")
    if int(stats_payload["segment_count"]) != segmentation_state_record.segment_count:
        raise ClassificationError(f"Classified stats segment count mismatch for source {source_id}")
    if int(stats_payload["taxonomy_version"]) != taxonomy.taxonomy_version:
        raise ClassificationError(f"Taxonomy version mismatch in stats for source {source_id}")

    notice_segment_ids = {notice.segment_id for notice in processed.notices}
    project_labels = set(taxonomy.project_labels)
    for segment in classified_segments:
        primary_label = str(segment.get("primary_label", ""))
        if not primary_label:
            raise ClassificationError(f"Missing primary_label for source {source_id}")
        secondary_labels = [str(label) for label in segment.get("secondary_labels", [])]
        if primary_label in secondary_labels:
            raise ClassificationError(f"Secondary labels duplicate primary label for source {source_id}")
        if primary_label == "cross-project":
            project_secondaries = [label for label in secondary_labels if label in project_labels]
            if len(project_secondaries) < 2:
                raise ClassificationError(f"Cross-project segment missing project secondaries for source {source_id}")
        explanation = segment.get("classification_explanation")
        if not isinstance(explanation, dict):
            raise ClassificationError(f"Missing classification explanation for source {source_id}")
        if not explanation.get("matched_rule_ids", []) and primary_label not in {"cross-project", "unclassified"}:
            raise ClassificationError(f"Missing matched rule ids for classified segment in source {source_id}")
        if not set(explanation.get("signal_families", [])).issubset(MATCHED_SIGNAL_FAMILIES):
            raise ClassificationError(f"Unknown signal families in explanation for source {source_id}")
        confidence = str(segment.get("confidence", ""))
        if primary_label == "unclassified" or confidence == "weak":
            if str(segment["segment_id"]) not in notice_segment_ids:
                raise ClassificationError(f"Missing classification notice for low-confidence segment in source {source_id}")


def validate_state_against_segmentation(
    segmentation_state: dict[str, SegmentationStateRecord],
    classification_state: dict[str, ClassificationStateRecord],
) -> None:
    for source_id, segmentation_state_record in segmentation_state.items():
        state_record = classification_state.get(source_id)
        if state_record is None:
            raise ClassificationError(f"Missing classification state for source {source_id}")
        if segmentation_state_record.status == "tombstoned":
            if state_record.status != "tombstoned":
                raise ClassificationError(f"Tombstoned source not marked tombstoned in classification state: {source_id}")
            continue
        if state_record.status != "classified":
            raise ClassificationError(f"Active source not marked classified in state: {source_id}")
        if state_record.segment_count != segmentation_state_record.segment_count:
            raise ClassificationError(f"Classification segment count mismatch for source {source_id}")
        if state_record.segmentation_schema_version != segmentation_state_record.segmentation_schema_version:
            raise ClassificationError(f"Segmentation schema mismatch in classification state for source {source_id}")


def tombstone_state_record(
    source_id: str,
    segmentation_state_record: SegmentationStateRecord,
    prior_state: ClassificationStateRecord | None,
    taxonomy_version: int,
    run_id: str,
) -> ClassificationStateRecord:
    segment_count = prior_state.segment_count if prior_state is not None else segmentation_state_record.segment_count
    return ClassificationStateRecord(
        source_id=source_id,
        classification_schema_version=CLASSIFICATION_SCHEMA_VERSION,
        taxonomy_version=taxonomy_version,
        segmentation_schema_version=segmentation_state_record.segmentation_schema_version,
        segmentation_last_run_id=segmentation_state_record.last_run_id,
        segment_count=segment_count,
        status="tombstoned",
        last_classified_at=utc_now(),
        last_run_id=run_id,
    )


def build_state_payload(state_records: dict[str, ClassificationStateRecord]) -> dict[str, object]:
    return {
        "schema_version": STATE_SCHEMA_VERSION,
        "classification_schema_version": CLASSIFICATION_SCHEMA_VERSION,
        "generated_at": utc_now(),
        "source_count": len(state_records),
        "sources": [state_records[source_id].to_dict() for source_id in sorted(state_records)],
    }


def source_artifacts_exist(source_output_dir: Path) -> bool:
    return (
        (source_output_dir / "segments.jsonl").exists()
        and (source_output_dir / "stats.json").exists()
    )


def read_json_required(path: Path) -> dict[str, object]:
    payload = read_json_file(path)
    if payload is None:
        raise ClassificationError(f"Missing or invalid JSON artifact: {path}")
    return payload


def read_jsonl_required(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        raise ClassificationError(f"Missing JSONL artifact: {path}")
    records: list[dict[str, object]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.rstrip("\n")
            if not line:
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ClassificationError(f"Invalid JSONL artifact line in {path}: {exc}") from exc
            if not isinstance(payload, dict):
                raise ClassificationError(f"JSONL artifact line is not an object in {path}")
            records.append(payload)
    return records


def promote_staged_sources(staging_root: Path, classified_dir: Path, changed_source_ids: list[str]) -> None:
    if not changed_source_ids:
        return
    staged_sources_root = staging_root / "sources"
    backup_root = staging_root / "_backup"
    promoted: list[tuple[Path, Path, bool]] = []
    try:
        for source_id in changed_source_ids:
            staged_dir = staged_sources_root / source_id
            target_dir = classified_dir / "sources" / source_id
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
        raise ClassificationError(f"Failed to promote staged classified sources: {exc}") from exc


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


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def normalize_path_text(value: str) -> str:
    normalized = value.replace("\\", " ").replace("/", " ").replace("-", " ").replace("_", " ")
    return normalize_text(normalized)


def collect_repo_tokens(relative_path: str, cwd: str) -> list[str]:
    tokens: list[str] = []
    for raw in (relative_path, cwd):
        if not raw:
            continue
        raw = raw.replace("\\", "/")
        parts = [part for part in raw.split("/") if part]
        tokens.extend(parts)
        if parts:
            tokens.append(parts[-1])
    return [token for token in tokens if token]


def first_or_default(items: list[tuple[str, int]]) -> tuple[str | None, int]:
    if not items:
        return None, 0
    return items[0]


def best_label_for_category(
    taxonomy: TaxonomyConfig,
    label_scores: dict[str, int],
    category: str,
) -> tuple[str | None, int]:
    candidates = [
        (label.label, label_scores.get(label.label, 0))
        for label in taxonomy.labels
        if label.category == category
    ]
    candidates.sort(key=lambda item: (-item[1], item[0]))
    return first_or_default(candidates)


def dedupe_preserving_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        ordered.append(item)
    return ordered
