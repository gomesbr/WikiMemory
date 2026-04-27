from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from .classification import ClassificationStateRecord, load_classification_state
from .discovery import DiscoveryError, atomic_write_text, ensure_directory, utc_now
from .normalization import append_jsonl_text, read_json_file, write_text_file
from .raw_event_resolver import RawEventResolver

STATE_SCHEMA_VERSION = 1
EXTRACTION_SCHEMA_VERSION = 6
VALID_CONFIDENCE = {"explicit", "strong", "inferred"}
VALID_TEMPORAL_STATUS = {"active", "historical", "superseded", "durable"}
GLOBAL_LABEL = "global"
UNCLASSIFIED_LABEL = "unclassified"
CROSS_PROJECT_LABEL = "cross-project"
PROJECT_LABELS = {"ai-trader", "open-brain", "ai-scientist"}
EXTRACTABLE_CANONICAL_KINDS = {
    "event_msg.user_message",
    "event_msg.agent_message",
    "response_item.message",
    "turn_context",
}
PATH_PATTERN = re.compile(
    r"(?P<path>(?:[A-Za-z]:\\[^\s:;,)\]]+|(?:[A-Za-z0-9_.-]+/)+[A-Za-z0-9_.-]+\.[A-Za-z0-9_]+))"
)
MODULE_PATTERN = re.compile(r"\b(?P<module>[A-Za-z_]\w*(?:\.[A-Za-z_]\w*){1,})\b")
CLAUSE_SPLIT_PATTERN = re.compile(r"(?:[\r\n]+|;+\s*|(?<=[.!?])\s+)")
WHITESPACE_PATTERN = re.compile(r"\s+")
SIGNATURE_PUNCTUATION = re.compile(r"[^a-z0-9._/\-=\s]+")
TOKEN_PATTERN = re.compile(r"[a-z0-9][a-z0-9._/\-]*")
LEADING_CUE_PATTERN = re.compile(
    r"^(?:for\s+(?:ai[- ]trader|open[- ]brain|ai[- ]scientist)[,:]?\s*)?",
    re.IGNORECASE,
)
STOPWORDS = {
    "a",
    "about",
    "after",
    "all",
    "also",
    "and",
    "are",
    "as",
    "at",
    "be",
    "been",
    "both",
    "but",
    "by",
    "for",
    "from",
    "get",
    "had",
    "has",
    "have",
    "if",
    "in",
    "into",
    "is",
    "it",
    "its",
    "just",
    "later",
    "more",
    "new",
    "not",
    "now",
    "of",
    "on",
    "or",
    "our",
    "out",
    "over",
    "please",
    "so",
    "some",
    "that",
    "the",
    "then",
    "there",
    "these",
    "this",
    "to",
    "too",
    "up",
    "use",
    "using",
    "was",
    "we",
    "were",
    "what",
    "when",
    "with",
    "would",
}
GENERIC_SUBJECT_KEYS = {"it", "this", "that"}
EXAMPLE_MARKERS = ("e.g.", "e.g", "for example", "example", "examples:", "examples like")
COMMON_TLDS = {"com", "io", "org", "net", "dev", "app", "ai"}
RUNTIME_ONLY_PREFIXES = (
    "exit code:",
    "token count",
    "task started",
    "task complete",
    "item completed",
)
RULEISH_ITEM_TYPES = {"communication_preference", "workflow_rule", "do_rule", "dont_rule"}
PROGRESS_STATUS_PREFIXES = (
    "i'm ",
    "i am ",
    "iâ€™ll ",
    "i'll ",
    "next i'll ",
    "next iâ€™ll ",
    "i am fixing",
    "i'm fixing",
    "i am doing",
    "i'm doing",
    "we are ",
    "we're ",
)
SCHEMA_LABEL_PATTERN = re.compile(
    r"^(?:[#>*\-\s]*)(?:response style|communication preferences?|agent interaction style|workflow rules?)(?:\s*:?\s*)$",
    re.IGNORECASE,
)
LEADING_MARKDOWN_PATTERN = re.compile(r"^(?:[#>*\-]+\s*)+")
NUMBERED_LIST_PREFIX = re.compile(r"^\d+[\)\].:-]\s*")
INLINE_NUMBERED_LIST = re.compile(r"(?:^|\s)\d+\)")
TECHNICAL_IDENTIFIER_PATTERN = re.compile(r"`[^`]+`|\b[a-z]+[A-Z][A-Za-z0-9_]*\b|\b[a-z_]+(?:\.[a-z_]+)+\b")
PIPELINE_PHASE_TERMS = {
    "discover",
    "normalize",
    "segment",
    "classify",
    "extract",
    "wiki",
    "bootstrap",
    "audit",
    "refresh",
}


class ExtractionError(DiscoveryError):
    """Fatal extraction error that must stop the run."""


@dataclass(frozen=True)
class ExtractionRule:
    rule_id: str
    item_type: str
    terms: tuple[str, ...]
    confidence: str


@dataclass(frozen=True)
class ExtractionRulesConfig:
    schema_version: int
    extraction_rules_version: int
    durable_item_types: frozenset[str]
    temporal_item_types: frozenset[str]
    global_default_item_types: frozenset[str]
    project_default_item_types: frozenset[str]
    target_page_keys: dict[str, str]
    imperative_verbs: tuple[str, ...]
    replacement_cues: tuple[str, ...]
    code_location_indicators: tuple[str, ...]
    stable_policy_terms: tuple[str, ...]
    explicit_preference_terms: tuple[str, ...]
    global_scope_terms: tuple[str, ...]
    one_off_imperative_terms: tuple[str, ...]
    progress_status_terms: tuple[str, ...]
    runtime_local_terms: tuple[str, ...]
    schema_scaffold_terms: tuple[str, ...]
    schema_label_terms: tuple[str, ...]
    durable_policy_min_sessions: int
    durable_policy_min_days: int
    rules: tuple[ExtractionRule, ...]

    @property
    def all_item_types(self) -> frozenset[str]:
        return self.durable_item_types | self.temporal_item_types


@dataclass(frozen=True)
class ExtractionStateRecord:
    source_id: str
    extraction_schema_version: int
    extraction_rules_version: int
    classification_schema_version: int
    taxonomy_version: int
    classification_last_run_id: str
    classified_segment_count: int
    status: str
    touched_domains: tuple[str, ...]
    last_extracted_at: str
    last_run_id: str

    def to_dict(self) -> dict[str, object]:
        return {
            "source_id": self.source_id,
            "extraction_schema_version": self.extraction_schema_version,
            "extraction_rules_version": self.extraction_rules_version,
            "classification_schema_version": self.classification_schema_version,
            "taxonomy_version": self.taxonomy_version,
            "classification_last_run_id": self.classification_last_run_id,
            "classified_segment_count": self.classified_segment_count,
            "status": self.status,
            "touched_domains": list(self.touched_domains),
            "last_extracted_at": self.last_extracted_at,
            "last_run_id": self.last_run_id,
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "ExtractionStateRecord":
        return cls(
            source_id=str(data["source_id"]),
            extraction_schema_version=int(data["extraction_schema_version"]),
            extraction_rules_version=int(data["extraction_rules_version"]),
            classification_schema_version=int(data["classification_schema_version"]),
            taxonomy_version=int(data["taxonomy_version"]),
            classification_last_run_id=str(data.get("classification_last_run_id", "")),
            classified_segment_count=int(data["classified_segment_count"]),
            status=str(data["status"]),
            touched_domains=tuple(str(item) for item in data.get("touched_domains", [])),
            last_extracted_at=str(data["last_extracted_at"]),
            last_run_id=str(data["last_run_id"]),
        )


@dataclass(frozen=True)
class ExtractionNotice:
    run_id: str
    source_id: str
    segment_id: str | None
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
class ExtractionRunReport:
    run_id: str
    started_at: str
    finished_at: str
    source_status_counts: dict[str, int]
    extracted_observation_count: int
    domain_item_count: int
    item_type_counts: dict[str, int]
    notice_count: int
    success: bool
    fatal_error_summary: str | None

    def to_dict(self) -> dict[str, object]:
        return {
            "run_id": self.run_id,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "source_status_counts": self.source_status_counts,
            "extracted_observation_count": self.extracted_observation_count,
            "domain_item_count": self.domain_item_count,
            "item_type_counts": self.item_type_counts,
            "notice_count": self.notice_count,
            "success": self.success,
            "fatal_error_summary": self.fatal_error_summary,
        }


@dataclass(frozen=True)
class ExtractionResult:
    report: ExtractionRunReport
    state_path: Path
    run_log_path: Path
    notice_log_path: Path


@dataclass(frozen=True)
class SegmentExtractionContext:
    source_id: str
    session_id: str
    classified_segment: dict[str, object]
    normalized_session: dict[str, object]
    event_slice: list[dict[str, object]]
    unique_texts: list[str]
    candidate_clauses: list[str]


@dataclass(frozen=True)
class SourceExtractionArtifacts:
    observations: list[dict[str, object]]
    stats_payload: dict[str, object]
    state_record: ExtractionStateRecord
    notices: list[ExtractionNotice]
    touched_domains: tuple[str, ...]
    item_type_counts: Counter[str]


def run_extraction(
    rules_path: Path | str,
    state_dir: Path | str,
    normalized_dir: Path | str,
    classified_dir: Path | str,
    extracted_dir: Path | str,
    audits_dir: Path | str,
    source_ids: Iterable[str] | None = None,
    source_roots_config_path: Path | str | None = None,
) -> ExtractionResult:
    rules_path = Path(rules_path)
    state_dir = Path(state_dir)
    normalized_dir = Path(normalized_dir)
    classified_dir = Path(classified_dir)
    extracted_dir = Path(extracted_dir)
    audits_dir = Path(audits_dir)
    source_roots_config_path = Path(source_roots_config_path) if source_roots_config_path is not None else None

    classification_state_path = state_dir / "classification_state.json"
    state_path = state_dir / "extraction_state.json"
    run_log_path = state_dir / "extraction_runs.jsonl"
    notice_log_path = audits_dir / "extraction_notices.jsonl"

    ensure_directory(state_dir)
    ensure_directory(audits_dir)
    ensure_directory(extracted_dir / "sources")
    ensure_directory(extracted_dir / "domains")

    run_id = f"extract-{utc_now().replace(':', '').replace('.', '').replace('-', '')}"
    started_at = utc_now()
    staging_root = extracted_dir / ".staging" / run_id

    previous_state_text = state_path.read_text(encoding="utf-8") if state_path.exists() else None
    previous_run_log_text = run_log_path.read_text(encoding="utf-8") if run_log_path.exists() else ""
    previous_notice_log_text = notice_log_path.read_text(encoding="utf-8") if notice_log_path.exists() else ""

    try:
        rules = load_extraction_rules(rules_path)
        classification_state = load_classification_state(classification_state_path)
        previous_state = load_extraction_state(state_path)
        target_source_ids = resolve_target_source_ids(source_ids, classification_state)
        raw_event_resolver = (
            RawEventResolver.from_paths(
                registry_path=state_dir / "source_registry.json",
                source_roots_config_path=source_roots_config_path,
            )
            if source_roots_config_path is not None
            else None
        )

        next_state = dict(previous_state)
        source_status_counts: Counter[str] = Counter()
        item_type_counts: Counter[str] = Counter()
        notices_for_run: list[ExtractionNotice] = []
        domains_to_rebuild: set[str] = set()
        changed_source_ids: list[str] = []
        extracted_observation_count = 0

        for source_id in target_source_ids:
            classification_state_record = classification_state[source_id]
            source_output_dir = extracted_dir / "sources" / source_id
            prior_state = previous_state.get(source_id)

            if classification_state_record.status == "tombstoned":
                next_state[source_id] = tombstone_state_record(
                    source_id=source_id,
                    classification_state_record=classification_state_record,
                    prior_state=prior_state,
                    rules_version=rules.extraction_rules_version,
                    run_id=run_id,
                )
                source_status_counts["tombstoned"] += 1
                continue

            mode = determine_extraction_mode(
                classification_state_record=classification_state_record,
                prior_state=prior_state,
                source_output_dir=source_output_dir,
                rules_version=rules.extraction_rules_version,
            )
            if mode == "unchanged":
                next_state[source_id] = previous_state[source_id]
                source_status_counts["unchanged"] += 1
                continue

            processed = extract_source(
                source_id=source_id,
                classification_state_record=classification_state_record,
                normalized_dir=normalized_dir,
                classified_dir=classified_dir,
                staged_source_dir=staging_root / "sources" / source_id,
                rules=rules,
                run_id=run_id,
                raw_event_resolver=raw_event_resolver,
            )
            validate_processed_source(
                source_id=source_id,
                classification_state_record=classification_state_record,
                rules=rules,
                processed=processed,
                staged_source_dir=staging_root / "sources" / source_id,
            )
            next_state[source_id] = processed.state_record
            source_status_counts["extracted"] += 1
            item_type_counts.update(processed.item_type_counts)
            notices_for_run.extend(processed.notices)
            extracted_observation_count += len(processed.observations)
            domains_to_rebuild.update(processed.touched_domains)
            if prior_state is not None:
                domains_to_rebuild.update(prior_state.touched_domains)
            changed_source_ids.append(source_id)

        domain_item_count = rebuild_touched_domains(
            domains=sorted(domains_to_rebuild),
            staging_root=staging_root,
            extracted_dir=extracted_dir,
            changed_source_ids=changed_source_ids,
        )

        if source_ids is None:
            validate_state_against_classification(classification_state, next_state)

        report = ExtractionRunReport(
            run_id=run_id,
            started_at=started_at,
            finished_at=utc_now(),
            source_status_counts=dict(sorted(source_status_counts.items())),
            extracted_observation_count=extracted_observation_count,
            domain_item_count=domain_item_count,
            item_type_counts=dict(sorted(item_type_counts.items())),
            notice_count=len(notices_for_run),
            success=True,
            fatal_error_summary=None,
        )

        staged_state_path = staging_root / "extraction_state.json"
        staged_run_log_path = staging_root / "extraction_runs.jsonl"
        staged_notice_log_path = staging_root / "extraction_notices.jsonl"
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

        promote_staged_sources(staging_root, extracted_dir, changed_source_ids)
        promote_staged_domains(staging_root, extracted_dir, sorted(domains_to_rebuild))
        os.replace(staged_state_path, state_path)
        ensure_directory(run_log_path.parent)
        os.replace(staged_run_log_path, run_log_path)
        ensure_directory(notice_log_path.parent)
        os.replace(staged_notice_log_path, notice_log_path)
        cleanup_staging_root(staging_root)
        return ExtractionResult(
            report=report,
            state_path=state_path,
            run_log_path=run_log_path,
            notice_log_path=notice_log_path,
        )
    except Exception as exc:
        cleanup_staging_root(staging_root)
        failure_report = ExtractionRunReport(
            run_id=run_id,
            started_at=started_at,
            finished_at=utc_now(),
            source_status_counts={},
            extracted_observation_count=0,
            domain_item_count=0,
            item_type_counts={},
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
        return ExtractionResult(
            report=failure_report,
            state_path=state_path,
            run_log_path=run_log_path,
            notice_log_path=notice_log_path,
        )


def load_extraction_rules(rules_path: Path) -> ExtractionRulesConfig:
    try:
        payload = json.loads(rules_path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError as exc:
        raise ExtractionError(f"Missing extraction rules config: {rules_path}") from exc
    except json.JSONDecodeError as exc:
        raise ExtractionError(f"Invalid extraction rules JSON: {rules_path}") from exc

    taxonomy = payload.get("item_taxonomy")
    defaults = payload.get("domain_resolution_defaults")
    target_page_keys = payload.get("target_page_keys")
    rules_payload = payload.get("rules")
    durability = payload.get("durability", {})
    if not isinstance(taxonomy, dict):
        raise ExtractionError("Extraction rules must define item_taxonomy")
    if not isinstance(defaults, dict):
        raise ExtractionError("Extraction rules must define domain_resolution_defaults")
    if not isinstance(target_page_keys, dict):
        raise ExtractionError("Extraction rules must define target_page_keys")
    if not isinstance(rules_payload, list):
        raise ExtractionError("Extraction rules must define rules")
    if not isinstance(durability, dict):
        raise ExtractionError("Extraction rules durability must be an object")

    durable = frozenset(str(item) for item in taxonomy.get("durable", []))
    temporal = frozenset(str(item) for item in taxonomy.get("temporal", []))
    if not durable or not temporal:
        raise ExtractionError("Extraction rules must define durable and temporal item types")
    all_item_types = durable | temporal

    global_defaults = frozenset(str(item) for item in defaults.get("global_default_item_types", []))
    project_defaults = frozenset(str(item) for item in defaults.get("project_default_item_types", []))
    if not global_defaults <= all_item_types:
        raise ExtractionError("Extraction rules global_default_item_types contains unknown item types")
    if not project_defaults <= all_item_types:
        raise ExtractionError("Extraction rules project_default_item_types contains unknown item types")

    imperative_verbs = tuple(
        sorted({normalize_signature_text(str(item)) for item in payload.get("imperative_verbs", []) if str(item).strip()})
    )
    replacement_cues = tuple(
        sorted({normalize_signature_text(str(item)) for item in payload.get("replacement_cues", []) if str(item).strip()})
    )
    code_location_indicators = tuple(
        sorted(
            {
                normalize_signature_text(str(item))
                for item in payload.get("code_location_indicators", [])
                if str(item).strip()
            }
        )
    )
    stable_policy_terms = tuple(
        sorted(
            {
                normalize_signature_text(str(item))
                for item in durability.get("stable_policy_terms", [])
                if normalize_signature_text(str(item))
            }
        )
    )
    explicit_preference_terms = tuple(
        sorted(
            {
                normalize_signature_text(str(item))
                for item in durability.get("explicit_preference_terms", [])
                if normalize_signature_text(str(item))
            }
        )
    )
    global_scope_terms = tuple(
        sorted(
            {
                normalize_signature_text(str(item))
                for item in durability.get("global_scope_terms", [])
                if normalize_signature_text(str(item))
            }
        )
    )
    one_off_imperative_terms = tuple(
        sorted(
            {
                normalize_signature_text(str(item))
                for item in durability.get("one_off_imperative_terms", [])
                if normalize_signature_text(str(item))
            }
        )
    )
    progress_status_terms = tuple(
        sorted(
            {
                normalize_signature_text(str(item))
                for item in durability.get("progress_status_terms", [])
                if normalize_signature_text(str(item))
            }
        )
    )
    runtime_local_terms = tuple(
        sorted(
            {
                normalize_signature_text(str(item))
                for item in durability.get("runtime_local_terms", [])
                if normalize_signature_text(str(item))
            }
        )
    )
    schema_scaffold_terms = tuple(
        sorted(
            {
                normalize_signature_text(str(item))
                for item in durability.get("schema_scaffold_terms", [])
                if normalize_signature_text(str(item))
            }
        )
    )
    schema_label_terms = tuple(
        sorted(
            {
                normalize_signature_text(str(item))
                for item in durability.get("schema_label_terms", [])
                if normalize_signature_text(str(item))
            }
        )
    )

    loaded_rules: list[ExtractionRule] = []
    rule_ids: set[str] = set()
    for rule_payload in rules_payload:
        if not isinstance(rule_payload, dict):
            raise ExtractionError("Extraction rule entries must be objects")
        rule_id = str(rule_payload["id"])
        if rule_id in rule_ids:
            raise ExtractionError(f"Duplicate extraction rule id: {rule_id}")
        item_type = str(rule_payload["item_type"])
        if item_type not in all_item_types:
            raise ExtractionError(f"Extraction rule {rule_id} references unknown item type: {item_type}")
        confidence = str(rule_payload["confidence"])
        if confidence not in VALID_CONFIDENCE:
            raise ExtractionError(f"Extraction rule {rule_id} has unsupported confidence: {confidence}")
        terms_payload = rule_payload.get("terms")
        if not isinstance(terms_payload, list) or not terms_payload:
            raise ExtractionError(f"Extraction rule {rule_id} must define non-empty terms")
        terms = tuple(
            normalize_signature_text(str(item))
            for item in terms_payload
            if normalize_signature_text(str(item))
        )
        if not terms:
            raise ExtractionError(f"Extraction rule {rule_id} has no usable terms")
        loaded_rules.append(
            ExtractionRule(
                rule_id=rule_id,
                item_type=item_type,
                terms=terms,
                confidence=confidence,
            )
        )
        rule_ids.add(rule_id)

    missing_targets = sorted(all_item_types - {str(key) for key in target_page_keys})
    if missing_targets:
        raise ExtractionError(
            f"Extraction rules are missing target_page_keys for: {', '.join(missing_targets)}"
        )

    return ExtractionRulesConfig(
        schema_version=int(payload["schema_version"]),
        extraction_rules_version=int(payload["extraction_rules_version"]),
        durable_item_types=durable,
        temporal_item_types=temporal,
        global_default_item_types=global_defaults,
        project_default_item_types=project_defaults,
        target_page_keys={str(key): str(value) for key, value in target_page_keys.items()},
        imperative_verbs=imperative_verbs,
        replacement_cues=replacement_cues,
        code_location_indicators=code_location_indicators,
        stable_policy_terms=stable_policy_terms,
        explicit_preference_terms=explicit_preference_terms,
        global_scope_terms=global_scope_terms,
        one_off_imperative_terms=one_off_imperative_terms,
        progress_status_terms=progress_status_terms,
        runtime_local_terms=runtime_local_terms,
        schema_scaffold_terms=schema_scaffold_terms,
        schema_label_terms=schema_label_terms,
        durable_policy_min_sessions=int(durability.get("minimum_supporting_sessions", 2)),
        durable_policy_min_days=int(durability.get("minimum_supporting_days", 2)),
        rules=tuple(loaded_rules),
    )


def load_extraction_state(state_path: Path) -> dict[str, ExtractionStateRecord]:
    if not state_path.exists():
        return {}
    try:
        payload = json.loads(state_path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise ExtractionError(f"Invalid extraction state JSON: {state_path}") from exc
    if int(payload.get("schema_version", -1)) != STATE_SCHEMA_VERSION:
        raise ExtractionError(
            f"Unsupported extraction state schema version in {state_path}: {payload.get('schema_version')}"
        )
    records = [ExtractionStateRecord.from_dict(item) for item in payload.get("sources", [])]
    return {record.source_id: record for record in records}


def resolve_target_source_ids(
    source_ids: Iterable[str] | None,
    classification_state: dict[str, ClassificationStateRecord],
) -> list[str]:
    if source_ids is None:
        return sorted(classification_state)
    target_source_ids = sorted(dict.fromkeys(str(source_id) for source_id in source_ids))
    missing = [source_id for source_id in target_source_ids if source_id not in classification_state]
    if missing:
        raise ExtractionError(
            f"Requested source_ids are missing from classification state: {', '.join(missing)}"
        )
    return target_source_ids


def determine_extraction_mode(
    classification_state_record: ClassificationStateRecord,
    prior_state: ExtractionStateRecord | None,
    source_output_dir: Path,
    rules_version: int,
) -> str:
    if prior_state is None:
        return "full"
    if prior_state.status != "extracted":
        return "full"
    if prior_state.extraction_schema_version != EXTRACTION_SCHEMA_VERSION:
        return "full"
    if prior_state.extraction_rules_version != rules_version:
        return "full"
    if prior_state.classification_schema_version != classification_state_record.classification_schema_version:
        return "full"
    if prior_state.taxonomy_version != classification_state_record.taxonomy_version:
        return "full"
    if prior_state.classification_last_run_id != classification_state_record.last_run_id:
        return "full"
    if prior_state.classified_segment_count != classification_state_record.segment_count:
        return "full"
    if not source_artifacts_exist(source_output_dir):
        return "full"
    return "unchanged"


def extract_source(
    source_id: str,
    classification_state_record: ClassificationStateRecord,
    normalized_dir: Path,
    classified_dir: Path,
    staged_source_dir: Path,
    rules: ExtractionRulesConfig,
    run_id: str,
    raw_event_resolver: RawEventResolver | None,
) -> SourceExtractionArtifacts:
    ensure_directory(staged_source_dir)
    normalized_source_dir = normalized_dir / "sources" / source_id
    classified_source_dir = classified_dir / "sources" / source_id

    normalized_session = read_json_required(normalized_source_dir / "session.json")
    normalized_events = read_jsonl_required(normalized_source_dir / "events.jsonl")
    classified_segments = read_jsonl_required(classified_source_dir / "segments.jsonl")
    classified_stats = read_json_required(classified_source_dir / "stats.json")

    if len(classified_segments) != classification_state_record.segment_count:
        raise ExtractionError(
            f"Classified segment count mismatch for source {source_id}: {len(classified_segments)} != {classification_state_record.segment_count}"
        )

    notices: list[ExtractionNotice] = []
    item_type_counts: Counter[str] = Counter()
    deduped_observations: dict[tuple[str, str, str], dict[str, object]] = {}

    for classified_segment in classified_segments:
        context = build_segment_extraction_context(
            source_id=source_id,
            normalized_session=normalized_session,
            normalized_events=normalized_events,
            classified_segment=classified_segment,
            raw_event_resolver=raw_event_resolver,
        )
        segment_observations, segment_notices = extract_segment_observations(
            context=context,
            rules=rules,
            run_id=run_id,
        )
        notices.extend(segment_notices)
        for observation in segment_observations:
            key = (
                str(observation["primary_domain"]),
                str(observation["item_type"]),
                str(observation["normalized_signature"]),
            )
            if key not in deduped_observations:
                deduped_observations[key] = observation
                item_type_counts[str(observation["item_type"])] += 1
                continue
            merge_source_observation(deduped_observations[key], observation)

    observations = sorted(
        deduped_observations.values(),
        key=lambda item: (
            str(item["segment_id"]),
            str(item["item_type"]),
            str(item["statement"]).lower(),
        ),
    )
    assign_observation_ids(observations)
    apply_temporal_supersession(observations, rules)
    notices.extend(assign_conflict_candidates(observations, run_id=run_id, source_id=source_id))

    touched_domains = tuple(sorted({str(item["primary_domain"]) for item in observations}))
    stats_payload = {
        "source_id": source_id,
        "session_id": normalized_session["session_id"],
        "extraction_schema_version": EXTRACTION_SCHEMA_VERSION,
        "extraction_rules_version": rules.extraction_rules_version,
        "classification_schema_version": classification_state_record.classification_schema_version,
        "taxonomy_version": classification_state_record.taxonomy_version,
        "classified_segment_count": classification_state_record.segment_count,
        "observation_count": len(observations),
        "item_type_counts": dict(sorted(item_type_counts.items())),
        "domain_counts": dict(sorted(Counter(str(item["primary_domain"]) for item in observations).items())),
        "confidence_counts": dict(sorted(Counter(str(item["confidence"]) for item in observations).items())),
        "notice_counts": dict(sorted(Counter(notice.notice_type for notice in notices).items())),
        "classified_stats_summary": {
            "primary_label_counts": classified_stats.get("primary_label_counts", {}),
            "confidence_counts": classified_stats.get("confidence_counts", {}),
        },
    }

    write_text_file(staged_source_dir / "items.jsonl", render_jsonl(observations))
    write_text_file(
        staged_source_dir / "stats.json",
        json.dumps(stats_payload, indent=2, sort_keys=True) + "\n",
    )

    state_record = ExtractionStateRecord(
        source_id=source_id,
        extraction_schema_version=EXTRACTION_SCHEMA_VERSION,
        extraction_rules_version=rules.extraction_rules_version,
        classification_schema_version=classification_state_record.classification_schema_version,
        taxonomy_version=classification_state_record.taxonomy_version,
        classification_last_run_id=classification_state_record.last_run_id,
        classified_segment_count=classification_state_record.segment_count,
        status="extracted",
        touched_domains=touched_domains,
        last_extracted_at=utc_now(),
        last_run_id=run_id,
    )
    return SourceExtractionArtifacts(
        observations=observations,
        stats_payload=stats_payload,
        state_record=state_record,
        notices=notices,
        touched_domains=touched_domains,
        item_type_counts=item_type_counts,
    )


def build_segment_extraction_context(
    source_id: str,
    normalized_session: dict[str, object],
    normalized_events: list[dict[str, object]],
    classified_segment: dict[str, object],
    raw_event_resolver: RawEventResolver | None,
) -> SegmentExtractionContext:
    start_line = int(classified_segment["start_line_no"])
    end_line = int(classified_segment["end_line_no"])
    if start_line < 1 or end_line < start_line or end_line > len(normalized_events):
        raise ExtractionError(f"Invalid classified segment line bounds for source {source_id}")

    event_slice = normalized_events[start_line - 1 : end_line]
    if [int(event["source_line_no"]) for event in event_slice] != list(range(start_line, end_line + 1)):
        raise ExtractionError(f"Classified segment line slice is not contiguous for source {source_id}")

    unique_texts: list[str] = []
    seen_texts: set[str] = set()
    for event in event_slice:
        if not should_extract_from_event(event):
            continue
        surfaces = (
            raw_event_resolver.collect_text_surfaces(event)
            if raw_event_resolver is not None and bool(event.get("text_surface_truncated"))
            else event.get("text_surfaces", [])
        )
        for item in surfaces:
            if not isinstance(item, dict):
                continue
            text = str(item.get("text", "")).strip()
            lowered = text.lower()
            if text and lowered not in seen_texts:
                seen_texts.add(lowered)
                unique_texts.append(text)

    candidate_clauses = build_candidate_clauses(
        unique_texts=unique_texts,
        topic_hints=[str(item).strip() for item in classified_segment.get("topic_hints", []) if str(item).strip()],
        primary_label=str(classified_segment.get("primary_label", "")),
        secondary_labels=[str(item) for item in classified_segment.get("secondary_labels", [])],
    )

    return SegmentExtractionContext(
        source_id=source_id,
        session_id=str(normalized_session.get("session_id", source_id)),
        classified_segment=classified_segment,
        normalized_session=normalized_session,
        event_slice=event_slice,
        unique_texts=unique_texts,
        candidate_clauses=candidate_clauses,
    )


def should_extract_from_event(event: dict[str, object]) -> bool:
    canonical_kind = str(event.get("canonical_kind", ""))
    if canonical_kind not in EXTRACTABLE_CANONICAL_KINDS:
        return False
    if canonical_kind == "response_item.message":
        role = str(event.get("role", ""))
        return role in {"user", "assistant"}
    return True


def build_candidate_clauses(
    unique_texts: list[str],
    topic_hints: list[str],
    primary_label: str,
    secondary_labels: list[str],
) -> list[str]:
    clauses: list[str] = []
    seen: set[str] = set()
    text_bases = [*unique_texts, *topic_hints]
    classification_context = " ".join(
        item for item in [primary_label, *secondary_labels] if item and item not in {UNCLASSIFIED_LABEL}
    )
    for text in text_bases:
        for piece in CLAUSE_SPLIT_PATTERN.split(text):
            cleaned = normalize_clause(piece)
            if not cleaned:
                continue
            lowered = cleaned.lower()
            if lowered in seen:
                continue
            seen.add(lowered)
            clauses.append(cleaned)
    if classification_context:
        lowered_context = classification_context.lower()
        if lowered_context not in seen:
            clauses.append(classification_context)
    return clauses


def clean_ruleish_statement(clause: str, item_type: str, rules: ExtractionRulesConfig) -> str:
    text = LEADING_MARKDOWN_PATTERN.sub("", normalize_clause(clause)).strip()
    if item_type in {"communication_preference", "workflow_rule"}:
        text = strip_leading_item_cues(item_type, text)
    if item_type == "communication_preference":
        lowered = normalize_signature_text(text)
        for label in rules.schema_label_terms:
            if lowered.startswith(label):
                suffix = text[len(label) :].lstrip(" :-")
                if suffix:
                    text = suffix
                    lowered = normalize_signature_text(text)
                    break
    return normalize_clause(text)


def is_schema_label_fragment(text: str, rules: ExtractionRulesConfig) -> bool:
    if not text:
        return True
    normalized = normalize_signature_text(text)
    if not normalized:
        return True
    if SCHEMA_LABEL_PATTERN.match(text):
        return True
    return normalized in set(rules.schema_label_terms)


def is_pipeline_orchestration_clause(normalized_text: str) -> bool:
    if "always runs" in normalized_text or "runs full" in normalized_text:
        return any(term in normalized_text.split() for term in PIPELINE_PHASE_TERMS)
    return False


def contains_technical_identifier(text: str) -> bool:
    return bool(TECHNICAL_IDENTIFIER_PATTERN.search(text))


def classify_ruleish_clause(
    clause: str,
    item_type: str,
    context: SegmentExtractionContext,
    rules: ExtractionRulesConfig,
) -> dict[str, object]:
    cleaned_statement = clean_ruleish_statement(clause, item_type, rules)
    normalized_cleaned = normalize_signature_text(cleaned_statement)
    normalized_clause = normalize_signature_text(clause)
    blockers: list[str] = []

    if is_schema_label_fragment(cleaned_statement, rules):
        return {
            "durability_class": "schema_scaffold",
            "statement": cleaned_statement,
            "promotion_blockers": ["schema_label_fragment"],
            "wiki_eligible": False,
        }

    if any(term in normalized_clause for term in rules.schema_scaffold_terms):
        blockers.append("schema_scaffold")
        return {
            "durability_class": "schema_scaffold",
            "statement": cleaned_statement,
            "promotion_blockers": blockers,
            "wiki_eligible": False,
        }

    if any(term in normalized_clause for term in rules.runtime_local_terms):
        blockers.append("runtime_local_instruction")
        return {
            "durability_class": "session_instruction",
            "statement": cleaned_statement,
            "promotion_blockers": blockers,
            "wiki_eligible": False,
        }

    if item_type != "communication_preference" and normalized_clause.startswith(
        ("i ", "we ", "it was ", "it wasn t ", "added ", "applied ", "identified ", "fixed ")
    ):
        blockers.append("narrative_progress")
        return {
            "durability_class": "progress_status",
            "statement": cleaned_statement,
            "promotion_blockers": blockers,
            "wiki_eligible": False,
        }

    if normalized_clause.startswith(
        ("i m ", "i am ", "i ll ", "i will ", "next i ll ", "next i will ", "we re ", "we are ")
    ) or any(
        term in normalized_clause for term in rules.progress_status_terms
    ):
        blockers.append("progress_status")
        return {
            "durability_class": "progress_status",
            "statement": cleaned_statement,
            "promotion_blockers": blockers,
            "wiki_eligible": False,
        }

    if any(term in normalized_clause for term in rules.one_off_imperative_terms):
        blockers.append("one_off_imperative")
        return {
            "durability_class": "session_instruction",
            "statement": cleaned_statement,
            "promotion_blockers": blockers,
            "wiki_eligible": False,
        }
    if (
        item_type != "communication_preference"
        and ("?" in cleaned_statement or INLINE_NUMBERED_LIST.search(cleaned_statement))
    ) or normalized_clause.startswith("to make sure "):
        return {
            "durability_class": "session_instruction",
            "statement": cleaned_statement,
            "promotion_blockers": ["prompt_scaffold"],
            "wiki_eligible": False,
        }
    if NUMBERED_LIST_PREFIX.match(cleaned_statement) or cleaned_statement.endswith(":"):
        return {
            "durability_class": "schema_scaffold",
            "statement": cleaned_statement,
            "promotion_blockers": ["list_or_heading_scaffold"],
            "wiki_eligible": False,
        }
    if is_pipeline_orchestration_clause(normalized_cleaned := normalize_signature_text(cleaned_statement)):
        return {
            "durability_class": "schema_scaffold",
            "statement": cleaned_statement,
            "promotion_blockers": ["pipeline_orchestration_scaffold"],
            "wiki_eligible": False,
        }
    if item_type == "communication_preference" and contains_technical_identifier(cleaned_statement):
        return {
            "durability_class": "schema_scaffold",
            "statement": cleaned_statement,
            "promotion_blockers": ["technical_identifier_scaffold"],
            "wiki_eligible": False,
        }

    explicit_policy = any(term in normalized_cleaned for term in rules.stable_policy_terms)
    explicit_preference = item_type == "communication_preference" and any(
        term in normalized_cleaned for term in rules.explicit_preference_terms
    )

    if item_type == "communication_preference" and not explicit_preference and not has_meaningful_signal(cleaned_statement):
        return {
            "durability_class": "schema_scaffold",
            "statement": cleaned_statement,
            "promotion_blockers": ["schema_label_fragment"],
            "wiki_eligible": False,
        }
    return {
        "durability_class": "durable_policy",
        "statement": cleaned_statement,
        "promotion_blockers": blockers,
        "wiki_eligible": explicit_policy or explicit_preference,
    }


def remap_ruleish_item_type(clause: str, durability_class: str) -> str | None:
    normalized = normalize_signature_text(clause)
    if durability_class == "session_instruction":
        if normalized.startswith(("next step", "next steps", "then ", "follow up", "follow-up")):
            return "next_step"
        return "task_request"
    if durability_class == "progress_status":
        if any(term in normalized for term in ("completed", "done", "finished", "resolved", "fixed")):
            return "outcome"
        return "current_state"
    return None


def derive_provisional_wiki_eligibility(
    item_type: str,
    match: dict[str, object],
    durability_payload: dict[str, object] | None,
) -> bool:
    if durability_payload is not None:
        return bool(durability_payload["wiki_eligible"])
    if item_type in RULEISH_ITEM_TYPES:
        return False
    return True


def extract_segment_observations(
    context: SegmentExtractionContext,
    rules: ExtractionRulesConfig,
    run_id: str,
) -> tuple[list[dict[str, object]], list[ExtractionNotice]]:
    observations: list[dict[str, object]] = []
    notices: list[ExtractionNotice] = []
    segment_id = str(context.classified_segment["segment_id"])
    skipped_weak_notice_emitted = False

    for clause in context.candidate_clauses:
        if is_runtime_only_clause(clause):
            continue
        rule_matches = match_rules(clause, rules)
        code_location = detect_code_location(clause, rules)
        if code_location is not None:
            rule_matches.setdefault(
                "code_location",
                {
                    "rule_ids": ["code_location.detected"],
                    "confidence": "explicit",
                },
            )
        if not rule_matches:
            if has_meaningful_signal(clause) and not skipped_weak_notice_emitted:
                notices.append(
                    ExtractionNotice(
                        run_id=run_id,
                        source_id=context.source_id,
                        segment_id=segment_id,
                        severity="warning",
                        notice_type="skipped_weak_inference",
                        summary=f"skipped weak extraction candidate: {truncate_summary(clause)}",
                    )
                )
                skipped_weak_notice_emitted = True
            continue

        for item_type, match in sorted(rule_matches.items()):
            durability_payload: dict[str, object] | None = None
            effective_item_type = item_type
            effective_statement = normalize_clause(clause)
            if item_type == "code_location" and code_location is None:
                continue
            if item_type in RULEISH_ITEM_TYPES:
                durability_payload = classify_ruleish_clause(
                    clause=clause,
                    item_type=item_type,
                    context=context,
                    rules=rules,
                )
                effective_statement = str(durability_payload["statement"])
                durability_class = str(durability_payload["durability_class"])
                if durability_class == "schema_scaffold":
                    notices.append(
                        ExtractionNotice(
                            run_id=run_id,
                            source_id=context.source_id,
                            segment_id=segment_id,
                            severity="warning",
                            notice_type="schema_scaffold",
                            summary=f"skipped schema-like rule candidate: {truncate_summary(clause)}",
                        )
                    )
                    continue
                remapped_item_type = remap_ruleish_item_type(clause, durability_class)
                if remapped_item_type is not None:
                    effective_item_type = remapped_item_type
                    durability_payload = {
                        **durability_payload,
                        "wiki_eligible": False,
                    }
            domain_resolution = resolve_item_domains(
                item_type=effective_item_type,
                clause=effective_statement,
                classified_segment=context.classified_segment,
                normalized_session=context.normalized_session,
                rules=rules,
            )
            if domain_resolution is None:
                notices.append(
                    ExtractionNotice(
                        run_id=run_id,
                        source_id=context.source_id,
                        segment_id=segment_id,
                        severity="warning",
                        notice_type="taxonomy_gap",
                        summary=f"insufficient domain evidence for {effective_item_type}: {truncate_summary(clause)}",
                    )
                )
                continue

            target_page_key = rules.target_page_keys.get(effective_item_type)
            if not target_page_key:
                notices.append(
                    ExtractionNotice(
                        run_id=run_id,
                        source_id=context.source_id,
                        segment_id=segment_id,
                        severity="warning",
                        notice_type="unmapped_target",
                        summary=f"missing target page mapping for {effective_item_type}",
                    )
                )
                continue

            statement = effective_statement
            statement_signature = normalize_signature_text(statement)
            normalized_signature = (
                f"{effective_item_type}:{statement_signature}"
                if effective_item_type != "code_location"
                else build_code_location_signature(code_location, statement_signature)
            )
            subject_key = derive_subject_key(
                item_type=effective_item_type,
                statement=statement,
                code_location=code_location,
                target_page_key=target_page_key,
            )
            supporting_session_count = count_supporting_sessions_and_days(
                build_provenance_refs(context, statement, match["rule_ids"])
            )

            observations.append(
                {
                    "observation_id": "",
                    "source_id": context.source_id,
                    "segment_id": segment_id,
                    "item_type": effective_item_type,
                    "primary_domain": domain_resolution["primary_domain"],
                    "secondary_domains": domain_resolution["secondary_domains"],
                    "confidence": match["confidence"],
                    "statement": statement,
                    "normalized_signature": normalized_signature,
                    "subject_key": subject_key,
                    "temporal_status": default_temporal_status(effective_item_type, rules),
                    "first_seen_at": str(context.classified_segment.get("start_timestamp") or ""),
                    "last_seen_at": str(context.classified_segment.get("end_timestamp") or ""),
                    "recurrence_count": 1,
                    "target_namespace": domain_to_target_namespace(domain_resolution["primary_domain"]),
                    "target_page_key": target_page_key,
                    "code_location": code_location,
                    "provenance_refs": build_provenance_refs(context, statement, match["rule_ids"]),
                    "durability_class": (
                        str(durability_payload["durability_class"])
                        if durability_payload is not None
                        else ("durable_policy" if effective_item_type in RULEISH_ITEM_TYPES else "event_observation")
                    ),
                    "wiki_eligible": derive_provisional_wiki_eligibility(
                        effective_item_type,
                        match,
                        durability_payload,
                    ),
                    "promotion_blockers": (
                        list(durability_payload["promotion_blockers"]) if durability_payload is not None else []
                    ),
                    "supporting_session_count": supporting_session_count["sessions"],
                    "supporting_day_count": supporting_session_count["days"],
                    "classification_context": {
                        "primary_label": str(context.classified_segment.get("primary_label")),
                        "secondary_labels": [
                            str(item) for item in context.classified_segment.get("secondary_labels", [])
                        ],
                        "confidence": str(context.classified_segment.get("confidence", "")),
                        "classification_flags": [
                            str(item) for item in context.classified_segment.get("classification_flags", [])
                        ],
                    },
                    "extraction_rule_ids": dedupe_preserving_order(
                        [
                            *match["rule_ids"],
                            (
                                f"durability.{durability_payload['durability_class']}"
                                if durability_payload is not None
                                else ""
                            ),
                        ]
                    ),
                    "conflict_candidate_key": None,
                }
            )

    return observations, notices


def match_rules(clause: str, rules: ExtractionRulesConfig) -> dict[str, dict[str, object]]:
    normalized = normalize_signature_text(clause)
    matches: dict[str, dict[str, object]] = {}
    for rule in rules.rules:
        if any(term and term in normalized for term in rule.terms):
            current = matches.get(rule.item_type)
            if current is None:
                matches[rule.item_type] = {
                    "confidence": rule.confidence,
                    "rule_ids": [rule.rule_id],
                }
                continue
            current["rule_ids"] = dedupe_preserving_order([*current["rule_ids"], rule.rule_id])
            if confidence_rank(rule.confidence) > confidence_rank(str(current["confidence"])):
                current["confidence"] = rule.confidence
    return matches


def resolve_item_domains(
    item_type: str,
    clause: str,
    classified_segment: dict[str, object],
    normalized_session: dict[str, object],
    rules: ExtractionRulesConfig,
) -> dict[str, object] | None:
    clause_domains = detect_project_mentions(clause)
    segment_primary = str(classified_segment.get("primary_label", ""))
    segment_secondaries = [
        str(item) for item in classified_segment.get("secondary_labels", []) if str(item)
    ]
    segment_projects = [label for label in [segment_primary, *segment_secondaries] if label in PROJECT_LABELS]
    session_projects = detect_session_project_mentions(normalized_session)
    has_global_segment_context = segment_primary == GLOBAL_LABEL or GLOBAL_LABEL in segment_secondaries
    prefers_project_scope = (
        item_type in RULEISH_ITEM_TYPES
        and (segment_projects or session_projects)
        and not has_global_segment_context
        and not clause_has_global_scope(clause, rules)
    )

    if item_type in rules.global_default_item_types:
        if len(clause_domains) > 1:
            return {
                "primary_domain": CROSS_PROJECT_LABEL,
                "secondary_domains": clause_domains,
            }
        if len(clause_domains) == 1:
            return {
                "primary_domain": clause_domains[0],
                "secondary_domains": [GLOBAL_LABEL] if GLOBAL_LABEL in segment_secondaries else [],
            }
        if prefers_project_scope:
            scoped_projects = segment_projects or session_projects
            if len(scoped_projects) > 1:
                return {
                    "primary_domain": CROSS_PROJECT_LABEL,
                    "secondary_domains": dedupe_preserving_order(scoped_projects),
                }
            return {
                "primary_domain": scoped_projects[0],
                "secondary_domains": [],
            }
        return {
            "primary_domain": GLOBAL_LABEL,
            "secondary_domains": [],
        }

    if len(clause_domains) > 1:
        return {
            "primary_domain": CROSS_PROJECT_LABEL,
            "secondary_domains": clause_domains,
        }
    if len(clause_domains) == 1:
        secondary_domains = [GLOBAL_LABEL] if GLOBAL_LABEL in segment_secondaries else []
        return {
            "primary_domain": clause_domains[0],
            "secondary_domains": dedupe_preserving_order(secondary_domains),
        }
    if segment_primary in PROJECT_LABELS:
        secondary_domains = [GLOBAL_LABEL] if GLOBAL_LABEL in segment_secondaries else []
        return {
            "primary_domain": segment_primary,
            "secondary_domains": secondary_domains,
        }
    if segment_primary == CROSS_PROJECT_LABEL:
        project_secondaries = [label for label in segment_secondaries if label in PROJECT_LABELS]
        if len(project_secondaries) >= 2:
            return {
                "primary_domain": CROSS_PROJECT_LABEL,
                "secondary_domains": dedupe_preserving_order(project_secondaries),
            }
    if len(segment_projects) >= 2:
        return {
            "primary_domain": CROSS_PROJECT_LABEL,
            "secondary_domains": dedupe_preserving_order(segment_projects),
        }
    if len(segment_projects) == 1:
        return {
            "primary_domain": segment_projects[0],
            "secondary_domains": [GLOBAL_LABEL] if GLOBAL_LABEL in segment_secondaries else [],
        }
    if item_type == "code_location":
        if segment_primary in {GLOBAL_LABEL, *PROJECT_LABELS}:
            return {
                "primary_domain": segment_primary,
                "secondary_domains": [label for label in segment_secondaries if label == GLOBAL_LABEL],
            }
        if segment_primary == CROSS_PROJECT_LABEL and segment_projects:
            return {
                "primary_domain": CROSS_PROJECT_LABEL,
                "secondary_domains": dedupe_preserving_order(segment_projects),
            }
        return {
            "primary_domain": UNCLASSIFIED_LABEL,
            "secondary_domains": [],
        }
    return None


def clause_has_global_scope(clause: str, rules: ExtractionRulesConfig) -> bool:
    normalized = normalize_signature_text(clause)
    return any(term in normalized for term in rules.global_scope_terms)


def detect_session_project_mentions(normalized_session: dict[str, object]) -> list[str]:
    meta_fields = normalized_session.get("session_meta_fields", {})
    if not isinstance(meta_fields, dict):
        return []
    cwd = str(meta_fields.get("cwd", "")).strip()
    return detect_project_mentions(cwd)


def detect_project_mentions(clause: str) -> list[str]:
    normalized = normalize_signature_text(clause)
    mentions: list[str] = []
    mention_map = {
        "ai-trader": ("ai trader", "ai-trader", "aitrader", "openclaw"),
        "open-brain": ("open brain", "open-brain", "openbrain", "sessionmemory"),
        "ai-scientist": ("ai scientist", "ai-scientist", "aiscientist"),
    }
    for label, terms in mention_map.items():
        if any(term in normalized for term in terms):
            mentions.append(label)
    return mentions


def detect_code_location(clause: str, rules: ExtractionRulesConfig) -> dict[str, str] | None:
    normalized = normalize_signature_text(clause)
    if is_example_only_clause(normalized):
        return None
    path_match = PATH_PATTERN.search(clause)
    module_candidates = [
        match.group("module")
        for match in MODULE_PATTERN.finditer(clause)
        if is_plausible_module_name(match.group("module"))
    ]
    preferred_module = next(
        (
            candidate
            for candidate in module_candidates
            if "." in candidate and not candidate.lower().endswith(".py")
        ),
        module_candidates[-1] if module_candidates else None,
    )
    has_indicator = any(indicator in normalized for indicator in rules.code_location_indicators)
    if path_match is None and (preferred_module is None or not has_indicator):
        return None

    payload: dict[str, str] = {}
    if path_match is not None and is_plausible_path(path_match.group("path"), normalized):
        payload["path"] = path_match.group("path")
    if preferred_module is not None and (has_indicator or "path" not in payload):
        payload["module"] = preferred_module
    return payload or None


def is_example_only_clause(normalized_clause: str) -> bool:
    return any(marker in normalized_clause for marker in EXAMPLE_MARKERS)


def is_plausible_module_name(module_name: str) -> bool:
    normalized = module_name.lower()
    if normalized in {"e.g", "i.e"}:
        return False
    parts = [part for part in normalized.split(".") if part]
    if len(parts) < 2:
        return False
    if any(len(part) == 1 for part in parts):
        return False
    if parts[-1] in COMMON_TLDS:
        return False
    return any(len(part) >= 3 for part in parts)


def is_plausible_path(path_value: str, normalized_clause: str) -> bool:
    normalized_path = path_value.lower()
    if "http://" in normalized_clause or "https://" in normalized_clause:
        return False
    if any(marker in normalized_clause for marker in EXAMPLE_MARKERS):
        return False
    if "/" in normalized_path or "\\" in normalized_path:
        return True
    return normalized_path.endswith(
        (
            ".py",
            ".ts",
            ".tsx",
            ".js",
            ".jsx",
            ".json",
            ".md",
            ".sql",
            ".yaml",
            ".yml",
            ".toml",
            ".rs",
            ".go",
        )
    )


def build_code_location_signature(code_location: dict[str, str] | None, statement_signature: str) -> str:
    if not code_location:
        return f"code_location:{statement_signature}"
    path = code_location.get("path")
    module = code_location.get("module")
    location_bits = [bit for bit in [path, module] if bit]
    if location_bits:
        return f"code_location:{'|'.join(location_bits).lower()}"
    return f"code_location:{statement_signature}"


def derive_subject_key(
    item_type: str,
    statement: str,
    code_location: dict[str, str] | None,
    target_page_key: str,
) -> str:
    if code_location is not None:
        for key in ("path", "module"):
            value = code_location.get(key)
            if value:
                return normalize_signature_text(value)

    cleaned = normalize_signature_text(strip_leading_item_cues(item_type, statement))
    if item_type in {"open_question", "next_step"} and cleaned:
        return cleaned
    if "=" in cleaned:
        left = cleaned.split("=", 1)[0].strip()
        if left:
            return left
    for separator in (" is ", " are ", " using ", " uses "):
        if separator in cleaned:
            left = cleaned.split(separator, 1)[0].strip()
            if left:
                return left
    tokens = [token for token in TOKEN_PATTERN.findall(cleaned) if token not in STOPWORDS]
    if not tokens:
        return target_page_key
    subject_key = " ".join(tokens[:6])
    normalized_subject_key = subject_key.strip("- ").strip()
    if item_type == "current_state" and normalized_subject_key in GENERIC_SUBJECT_KEYS and cleaned:
        return cleaned
    return subject_key


def strip_leading_item_cues(item_type: str, statement: str) -> str:
    text = LEADING_CUE_PATTERN.sub("", statement).strip()
    cue_map = {
        "communication_preference": ("communication preference", "communication preferences"),
        "workflow_rule": ("workflow rule", "workflow rules"),
        "do_rule": ("please", "always", "make sure"),
        "dont_rule": ("do not", "don't", "never"),
        "decision": ("decision:", "we decided", "decided to"),
        "current_state": ("current state", "currently", "right now"),
        "next_step": ("next step", "next steps", "follow up", "follow-up"),
        "open_question": ("question:",),
    }
    for cue in cue_map.get(item_type, ()):
        lowered = text.lower()
        if lowered.startswith(cue):
            return text[len(cue) :].lstrip(" :-")
    return text


def default_temporal_status(item_type: str, rules: ExtractionRulesConfig) -> str:
    if item_type in rules.durable_item_types:
        return "durable"
    if item_type in {"current_state", "task_request", "next_step", "open_question"}:
        return "active"
    return "historical"


def domain_to_target_namespace(domain: str) -> str:
    if domain == GLOBAL_LABEL:
        return GLOBAL_LABEL
    if domain == CROSS_PROJECT_LABEL:
        return "projects/cross-project"
    if domain in PROJECT_LABELS:
        return f"projects/{domain}"
    return UNCLASSIFIED_LABEL


def build_provenance_refs(
    context: SegmentExtractionContext,
    statement: str,
    rule_ids: list[str],
) -> list[dict[str, object]]:
    segment = context.classified_segment
    return [
        {
            "source_id": context.source_id,
            "session_id": context.session_id,
            "segment_id": str(segment["segment_id"]),
            "start_event_id": str(segment["start_event_id"]),
            "end_event_id": str(segment["end_event_id"]),
            "start_line_no": int(segment["start_line_no"]),
            "end_line_no": int(segment["end_line_no"]),
            "start_timestamp": segment.get("start_timestamp"),
            "end_timestamp": segment.get("end_timestamp"),
            "statement": statement,
            "rule_ids": list(rule_ids),
        }
    ]


def count_supporting_sessions_and_days(provenance_refs: list[dict[str, object]]) -> dict[str, int]:
    session_ids = {
        str(ref.get("session_id", "")).strip()
        for ref in provenance_refs
        if str(ref.get("session_id", "")).strip()
    }
    day_keys = {
        str(timestamp).split("T", 1)[0]
        for ref in provenance_refs
        for timestamp in (ref.get("start_timestamp") or ref.get("end_timestamp"),)
        if str(timestamp).strip()
    }
    return {
        "sessions": max(1, len(session_ids)) if provenance_refs else 0,
        "days": max(1, len(day_keys)) if provenance_refs else 0,
    }


def merge_source_observation(target: dict[str, object], incoming: dict[str, object]) -> None:
    target["first_seen_at"] = min_non_empty(str(target["first_seen_at"]), str(incoming["first_seen_at"]))
    target["last_seen_at"] = max_non_empty(str(target["last_seen_at"]), str(incoming["last_seen_at"]))
    target["secondary_domains"] = dedupe_preserving_order(
        [*target["secondary_domains"], *incoming["secondary_domains"]]
    )
    target["provenance_refs"] = dedupe_dict_list([*target["provenance_refs"], *incoming["provenance_refs"]])
    target["extraction_rule_ids"] = dedupe_preserving_order(
        [*target["extraction_rule_ids"], *incoming["extraction_rule_ids"]]
    )
    target["promotion_blockers"] = dedupe_preserving_order(
        [
            *(str(item) for item in target.get("promotion_blockers", [])),
            *(str(item) for item in incoming.get("promotion_blockers", [])),
        ]
    )
    target["classification_context"]["secondary_labels"] = dedupe_preserving_order(
        [
            *target["classification_context"].get("secondary_labels", []),
            *incoming["classification_context"].get("secondary_labels", []),
        ]
    )
    if confidence_rank(str(incoming["confidence"])) > confidence_rank(str(target["confidence"])):
        target["confidence"] = incoming["confidence"]
    target["wiki_eligible"] = bool(target.get("wiki_eligible")) or bool(incoming.get("wiki_eligible"))
    support_counts = count_supporting_sessions_and_days(target["provenance_refs"])
    target["supporting_session_count"] = support_counts["sessions"]
    target["supporting_day_count"] = support_counts["days"]


def assign_observation_ids(observations: list[dict[str, object]]) -> None:
    counters: Counter[tuple[str, str]] = Counter()
    for observation in observations:
        key = (str(observation["segment_id"]), str(observation["item_type"]))
        counters[key] += 1
        observation["observation_id"] = f"{observation['segment_id']}:{observation['item_type']}:{counters[key]}"


def apply_temporal_supersession(observations: list[dict[str, object]], rules: ExtractionRulesConfig) -> None:
    grouped: dict[tuple[str, str, str, str], list[dict[str, object]]] = defaultdict(list)
    for observation in observations:
        if observation["temporal_status"] == "durable":
            continue
        grouped[
            (
                str(observation["primary_domain"]),
                str(observation["item_type"]),
                str(observation["target_page_key"]),
                str(observation["subject_key"]),
            )
        ].append(observation)

    for group in grouped.values():
        group.sort(
            key=lambda item: (
                str(item["first_seen_at"]),
                str(item["last_seen_at"]),
                1
                if any(
                    cue in normalize_signature_text(str(item["statement"]))
                    for cue in rules.replacement_cues
                )
                else 0,
                str(item["statement"]).lower(),
            )
        )
        for index, observation in enumerate(group):
            normalized_statement = normalize_signature_text(str(observation["statement"]))
            if not any(cue in normalized_statement for cue in rules.replacement_cues):
                continue
            for prior in group[:index]:
                if prior["normalized_signature"] != observation["normalized_signature"]:
                    prior["temporal_status"] = "superseded"


def assign_conflict_candidates(
    observations: list[dict[str, object]],
    run_id: str,
    source_id: str,
) -> list[ExtractionNotice]:
    notices: list[ExtractionNotice] = []
    grouped: dict[tuple[str, str, str, str], list[dict[str, object]]] = defaultdict(list)
    for observation in observations:
        grouped[
            (
                str(observation["primary_domain"]),
                str(observation["item_type"]),
                str(observation["target_page_key"]),
                str(observation["subject_key"]),
            )
        ].append(observation)

    for key, group in grouped.items():
        if str(key[1]) == "code_location":
            continue
        signatures = {str(item["normalized_signature"]) for item in group}
        if len(signatures) < 2:
            continue
        conflict_key = build_conflict_candidate_key(key)
        for observation in group:
            observation["conflict_candidate_key"] = conflict_key
            if observation["temporal_status"] == "superseded":
                continue
            notices.append(
                ExtractionNotice(
                    run_id=run_id,
                    source_id=source_id,
                    segment_id=str(observation["segment_id"]),
                    severity="warning",
                    notice_type="conflict_candidate",
                    summary=f"conflicting {observation['item_type']} items share subject {observation['subject_key']}",
                )
            )
    return dedupe_notices(notices)


def build_conflict_candidate_key(key: tuple[str, str, str, str]) -> str:
    digest = hashlib.sha1("|".join(key).encode("utf-8")).hexdigest()[:16]
    return f"conflict:{digest}"


def rebuild_touched_domains(
    domains: list[str],
    staging_root: Path,
    extracted_dir: Path,
    changed_source_ids: list[str],
) -> int:
    total_items = 0
    for domain in domains:
        observations = load_domain_observations(
            domain=domain,
            staging_root=staging_root,
            extracted_dir=extracted_dir,
            changed_source_ids=changed_source_ids,
        )
        domain_items = build_domain_items(observations)
        validate_domain_items(domain, domain_items)
        staged_domain_dir = staging_root / "domains" / domain
        ensure_directory(staged_domain_dir)
        write_text_file(staged_domain_dir / "items.jsonl", render_jsonl(domain_items))
        total_items += len(domain_items)
    return total_items


def load_domain_observations(
    domain: str,
    staging_root: Path,
    extracted_dir: Path,
    changed_source_ids: list[str],
) -> list[dict[str, object]]:
    observations: list[dict[str, object]] = []
    seen_sources: set[str] = set()
    for source_id in changed_source_ids:
        staged_path = staging_root / "sources" / source_id / "items.jsonl"
        if staged_path.exists():
            for item in read_jsonl_required(staged_path):
                if str(item.get("primary_domain")) == domain:
                    observations.append(item)
            seen_sources.add(source_id)

    sources_dir = extracted_dir / "sources"
    if not sources_dir.exists():
        return observations
    for source_dir in sorted(path for path in sources_dir.iterdir() if path.is_dir()):
        source_id = source_dir.name
        if source_id in seen_sources:
            continue
        items_path = source_dir / "items.jsonl"
        if not items_path.exists():
            continue
        for item in read_jsonl_required(items_path):
            if str(item.get("primary_domain")) == domain:
                observations.append(item)
    return observations


def build_domain_items(observations: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str, str], list[dict[str, object]]] = defaultdict(list)
    for observation in observations:
        grouped[
            (
                str(observation["primary_domain"]),
                str(observation["item_type"]),
                str(observation["normalized_signature"]),
            )
        ].append(observation)

    domain_items: list[dict[str, object]] = []
    for key, group in sorted(grouped.items()):
        primary_domain, item_type, normalized_signature = key
        base = sorted(
            group,
            key=lambda item: (
                str(item["first_seen_at"]),
                str(item["source_id"]),
                str(item["observation_id"]),
            ),
        )[0]
        provenance_refs = dedupe_dict_list(
            [ref for item in group for ref in item.get("provenance_refs", [])]
        )
        support_counts = count_supporting_sessions_and_days(provenance_refs)
        observation_ids = sorted(
            {str(item["observation_id"]) for item in group},
            key=lambda item: item,
        )
        secondary_domains = dedupe_preserving_order(
            [domain for item in group for domain in item.get("secondary_domains", [])]
        )
        temporal_status = select_merged_temporal_status(group)
        domain_item = {
            **base,
            "item_key": build_item_key(primary_domain, item_type, normalized_signature),
            "observation_ids": observation_ids,
            "first_seen_at": min_non_empty(*(str(item["first_seen_at"]) for item in group)),
            "last_seen_at": max_non_empty(*(str(item["last_seen_at"]) for item in group)),
            "recurrence_count": len(observation_ids),
            "provenance_refs": provenance_refs,
            "supporting_source_ids": sorted({str(item["source_id"]) for item in group}),
            "supporting_session_count": support_counts["sessions"],
            "supporting_day_count": support_counts["days"],
            "secondary_domains": secondary_domains,
            "temporal_status": temporal_status,
            "promotion_blockers": dedupe_preserving_order(
                [str(blocker) for item in group for blocker in item.get("promotion_blockers", []) if str(blocker)]
            ),
        }
        domain_item["wiki_eligible"] = determine_domain_item_wiki_eligibility(domain_item)
        domain_items.append(domain_item)

    assign_domain_conflict_candidates(domain_items)
    return domain_items


def select_merged_temporal_status(observations: list[dict[str, object]]) -> str:
    statuses = [str(item.get("temporal_status", "")) for item in observations]
    for candidate in ("durable", "active", "historical", "superseded"):
        if candidate in statuses:
            return candidate
    return "historical"


def assign_domain_conflict_candidates(domain_items: list[dict[str, object]]) -> None:
    grouped: dict[tuple[str, str, str, str], list[dict[str, object]]] = defaultdict(list)
    for item in domain_items:
        grouped[
            (
                str(item["primary_domain"]),
                str(item["item_type"]),
                str(item["target_page_key"]),
                str(item["subject_key"]),
            )
        ].append(item)
    for key, group in grouped.items():
        if len({str(item["normalized_signature"]) for item in group}) < 2:
            continue
        conflict_key = build_conflict_candidate_key(key)
        for item in group:
            item["conflict_candidate_key"] = conflict_key


def determine_domain_item_wiki_eligibility(item: dict[str, object]) -> bool:
    if any(str(blocker).strip() for blocker in item.get("promotion_blockers", [])):
        return False
    if str(item.get("durability_class", "")) == "schema_scaffold":
        return False
    item_type = str(item.get("item_type", ""))
    if item_type in RULEISH_ITEM_TYPES:
        eligible = bool(item.get("wiki_eligible")) or (
            int(item.get("supporting_session_count", 0)) >= 2
            and int(item.get("supporting_day_count", 0)) >= 2
        )
        if str(item.get("primary_domain", "")) == GLOBAL_LABEL and item_type in {"do_rule", "dont_rule"}:
            return eligible and (
                int(item.get("recurrence_count", 0)) >= 2
                or int(item.get("supporting_session_count", 0)) >= 2
            )
        return eligible
    return bool(item.get("wiki_eligible", True))


def build_item_key(primary_domain: str, item_type: str, normalized_signature: str) -> str:
    digest = hashlib.sha1(normalized_signature.encode("utf-8")).hexdigest()[:16]
    return f"{primary_domain}:{item_type}:{digest}"


def validate_processed_source(
    source_id: str,
    classification_state_record: ClassificationStateRecord,
    rules: ExtractionRulesConfig,
    processed: SourceExtractionArtifacts,
    staged_source_dir: Path,
) -> None:
    items = read_jsonl_required(staged_source_dir / "items.jsonl")
    stats_payload = read_json_required(staged_source_dir / "stats.json")
    if len(items) != len(processed.observations):
        raise ExtractionError(f"Extracted observation count mismatch for source {source_id}")
    if int(stats_payload["classified_segment_count"]) != classification_state_record.segment_count:
        raise ExtractionError(f"Classified segment count mismatch in extraction stats for source {source_id}")
    if int(stats_payload["observation_count"]) != len(items):
        raise ExtractionError(f"Observation count mismatch in extraction stats for source {source_id}")
    if int(stats_payload["extraction_rules_version"]) != rules.extraction_rules_version:
        raise ExtractionError(f"Extraction rules version mismatch in stats for source {source_id}")

    notice_segment_ids = {
        notice.segment_id
        for notice in processed.notices
        if notice.notice_type in {"skipped_weak_inference", "taxonomy_gap", "conflict_candidate", "unmapped_target"}
    }
    for observation in items:
        item_type = str(observation.get("item_type", ""))
        if item_type not in rules.all_item_types:
            raise ExtractionError(f"Unknown extracted item type for source {source_id}: {item_type}")
        confidence = str(observation.get("confidence", ""))
        if confidence not in VALID_CONFIDENCE:
            raise ExtractionError(f"Invalid extracted confidence for source {source_id}: {confidence}")
        temporal_status = str(observation.get("temporal_status", ""))
        if temporal_status not in VALID_TEMPORAL_STATUS:
            raise ExtractionError(f"Invalid temporal status for source {source_id}: {temporal_status}")
        if not observation.get("target_namespace") or not observation.get("target_page_key"):
            raise ExtractionError(f"Missing target hints for source {source_id}")
        if not observation.get("provenance_refs"):
            raise ExtractionError(f"Missing provenance refs for source {source_id}")
        secondary_domains = [str(item) for item in observation.get("secondary_domains", [])]
        if str(observation.get("primary_domain", "")) in secondary_domains:
            raise ExtractionError(f"Secondary domains duplicate primary domain for source {source_id}")
        if str(observation.get("durability_class", "")) not in {
            "durable_policy",
            "session_instruction",
            "progress_status",
            "schema_scaffold",
            "event_observation",
        }:
            raise ExtractionError(f"Invalid durability_class for source {source_id}")
        if not isinstance(observation.get("wiki_eligible"), bool):
            raise ExtractionError(f"Invalid wiki_eligible flag for source {source_id}")
        if int(observation.get("supporting_session_count", 0)) < 1:
            raise ExtractionError(f"Missing supporting_session_count for source {source_id}")
        if int(observation.get("supporting_day_count", 0)) < 1:
            raise ExtractionError(f"Missing supporting_day_count for source {source_id}")
        if (
            observation.get("conflict_candidate_key")
            and str(observation.get("temporal_status")) != "superseded"
            and str(observation.get("segment_id")) not in notice_segment_ids
        ):
            raise ExtractionError(f"Missing conflict notice for conflicting extracted observation in source {source_id}")


def validate_state_against_classification(
    classification_state: dict[str, ClassificationStateRecord],
    extraction_state: dict[str, ExtractionStateRecord],
) -> None:
    for source_id, classification_state_record in classification_state.items():
        state_record = extraction_state.get(source_id)
        if state_record is None:
            raise ExtractionError(f"Missing extraction state for source {source_id}")
        if classification_state_record.status == "tombstoned":
            if state_record.status != "tombstoned":
                raise ExtractionError(f"Tombstoned source not marked tombstoned in extraction state: {source_id}")
            continue
        if state_record.status != "extracted":
            raise ExtractionError(f"Active source not marked extracted in extraction state: {source_id}")
        if state_record.classified_segment_count != classification_state_record.segment_count:
            raise ExtractionError(f"Extraction segment count mismatch for source {source_id}")
        if state_record.classification_schema_version != classification_state_record.classification_schema_version:
            raise ExtractionError(f"Classification schema mismatch in extraction state for source {source_id}")
        if state_record.taxonomy_version != classification_state_record.taxonomy_version:
            raise ExtractionError(f"Taxonomy version mismatch in extraction state for source {source_id}")
        if state_record.classification_last_run_id != classification_state_record.last_run_id:
            raise ExtractionError(f"Classification run linkage mismatch in extraction state for source {source_id}")


def validate_domain_items(domain: str, domain_items: list[dict[str, object]]) -> None:
    seen_item_keys: set[str] = set()
    for item in domain_items:
        item_key = str(item.get("item_key", ""))
        if not item_key:
            raise ExtractionError(f"Missing domain item key for domain {domain}")
        if item_key in seen_item_keys:
            raise ExtractionError(f"Duplicate domain item key for domain {domain}: {item_key}")
        seen_item_keys.add(item_key)
        observation_ids = [str(obs) for obs in item.get("observation_ids", [])]
        if int(item.get("recurrence_count", 0)) != len(observation_ids):
            raise ExtractionError(f"Domain recurrence_count mismatch for domain {domain}")
        if not item.get("supporting_source_ids"):
            raise ExtractionError(f"Missing supporting_source_ids for domain {domain}")
        if not item.get("provenance_refs"):
            raise ExtractionError(f"Missing provenance refs for domain {domain}")
        if int(item.get("supporting_session_count", 0)) < 1:
            raise ExtractionError(f"Missing supporting_session_count for domain {domain}")
        if int(item.get("supporting_day_count", 0)) < 1:
            raise ExtractionError(f"Missing supporting_day_count for domain {domain}")
        if not isinstance(item.get("wiki_eligible"), bool):
            raise ExtractionError(f"Invalid wiki_eligible flag for domain {domain}")


def tombstone_state_record(
    source_id: str,
    classification_state_record: ClassificationStateRecord,
    prior_state: ExtractionStateRecord | None,
    rules_version: int,
    run_id: str,
) -> ExtractionStateRecord:
    touched_domains = prior_state.touched_domains if prior_state is not None else ()
    segment_count = (
        prior_state.classified_segment_count if prior_state is not None else classification_state_record.segment_count
    )
    return ExtractionStateRecord(
        source_id=source_id,
        extraction_schema_version=EXTRACTION_SCHEMA_VERSION,
        extraction_rules_version=rules_version,
        classification_schema_version=classification_state_record.classification_schema_version,
        taxonomy_version=classification_state_record.taxonomy_version,
        classification_last_run_id=classification_state_record.last_run_id,
        classified_segment_count=segment_count,
        status="tombstoned",
        touched_domains=touched_domains,
        last_extracted_at=utc_now(),
        last_run_id=run_id,
    )


def build_state_payload(state_records: dict[str, ExtractionStateRecord]) -> dict[str, object]:
    return {
        "schema_version": STATE_SCHEMA_VERSION,
        "extraction_schema_version": EXTRACTION_SCHEMA_VERSION,
        "generated_at": utc_now(),
        "source_count": len(state_records),
        "sources": [state_records[source_id].to_dict() for source_id in sorted(state_records)],
    }


def source_artifacts_exist(source_output_dir: Path) -> bool:
    return (
        (source_output_dir / "items.jsonl").exists()
        and (source_output_dir / "stats.json").exists()
    )


def read_json_required(path: Path) -> dict[str, object]:
    payload = read_json_file(path)
    if payload is None:
        raise ExtractionError(f"Missing or invalid JSON artifact: {path}")
    return payload


def read_jsonl_required(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        raise ExtractionError(f"Missing JSONL artifact: {path}")
    records: list[dict[str, object]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ExtractionError(f"Invalid JSONL artifact line {line_no}: {path}") from exc
        if not isinstance(payload, dict):
            raise ExtractionError(f"JSONL artifact line {line_no} is not an object: {path}")
        records.append(payload)
    return records


def render_jsonl(records: list[dict[str, object]]) -> str:
    if not records:
        return ""
    return "".join(json.dumps(record, separators=(",", ":"), sort_keys=True) + "\n" for record in records)


def promote_staged_sources(staging_root: Path, extracted_dir: Path, changed_source_ids: list[str]) -> None:
    for source_id in changed_source_ids:
        staged_source_dir = staging_root / "sources" / source_id
        if not staged_source_dir.exists():
            continue
        target_source_dir = extracted_dir / "sources" / source_id
        if target_source_dir.exists():
            shutil.rmtree(target_source_dir)
        ensure_directory(target_source_dir.parent)
        shutil.move(str(staged_source_dir), str(target_source_dir))


def promote_staged_domains(staging_root: Path, extracted_dir: Path, domains: list[str]) -> None:
    for domain in domains:
        staged_domain_dir = staging_root / "domains" / domain
        if not staged_domain_dir.exists():
            continue
        target_domain_dir = extracted_dir / "domains" / domain
        if target_domain_dir.exists():
            shutil.rmtree(target_domain_dir)
        ensure_directory(target_domain_dir.parent)
        shutil.move(str(staged_domain_dir), str(target_domain_dir))


def cleanup_staging_root(staging_root: Path) -> None:
    if staging_root.exists():
        shutil.rmtree(staging_root, ignore_errors=True)


def normalize_clause(text: str) -> str:
    return WHITESPACE_PATTERN.sub(" ", str(text)).strip(" \t\r\n;")


def normalize_signature_text(text: str) -> str:
    lowered = normalize_clause(text).lower()
    lowered = SIGNATURE_PUNCTUATION.sub(" ", lowered)
    return WHITESPACE_PATTERN.sub(" ", lowered).strip()


def confidence_rank(confidence: str) -> int:
    return {"inferred": 1, "strong": 2, "explicit": 3}.get(confidence, 0)


def has_meaningful_signal(clause: str) -> bool:
    tokens = [token for token in TOKEN_PATTERN.findall(normalize_signature_text(clause)) if token not in STOPWORDS]
    return len(tokens) >= 3


def is_runtime_only_clause(clause: str) -> bool:
    normalized = normalize_signature_text(clause)
    if not normalized:
        return True
    return any(normalized.startswith(prefix) for prefix in RUNTIME_ONLY_PREFIXES)


def dedupe_preserving_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        ordered.append(item)
    return ordered


def dedupe_dict_list(items: list[dict[str, object]]) -> list[dict[str, object]]:
    seen: set[str] = set()
    deduped: list[dict[str, object]] = []
    for item in items:
        signature = json.dumps(item, sort_keys=True, separators=(",", ":"))
        if signature in seen:
            continue
        seen.add(signature)
        deduped.append(item)
    return deduped


def dedupe_notices(notices: list[ExtractionNotice]) -> list[ExtractionNotice]:
    seen: set[tuple[str, str, str | None, str, str]] = set()
    deduped: list[ExtractionNotice] = []
    for notice in notices:
        key = (
            notice.source_id,
            notice.segment_id,
            notice.notice_type,
            notice.severity,
            notice.summary,
        )
        if key in seen:
            continue
        seen.add(key)
        deduped.append(notice)
    return deduped


def min_non_empty(*values: str) -> str:
    populated = sorted(value for value in values if value)
    return populated[0] if populated else ""


def max_non_empty(*values: str) -> str:
    populated = sorted(value for value in values if value)
    return populated[-1] if populated else ""


def truncate_summary(text: str, limit: int = 120) -> str:
    cleaned = normalize_clause(text)
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: limit - 3].rstrip() + "..."
