from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .audit import AuditResult, run_audit
from .bootstrap import BootstrapResult, run_bootstrap
from .classification import ClassificationResult, run_classification
from .discovery import DiscoveryError, atomic_write_text, ensure_directory, run_discovery, utc_now
from .extraction import ExtractionResult, run_extraction
from .normalization import NormalizationResult, append_jsonl_text, run_normalization
from .refresh import hash_file, summarize_phase_result
from .segmentation import SegmentationResult, run_segmentation
from .wiki import WikiResult, run_wiki

STATE_SCHEMA_VERSION = 1
FULL_LOAD_SCHEMA_VERSION = 1
PHASE_ORDER = (
    "discover",
    "normalize",
    "segment",
    "classify",
    "extract",
    "wiki",
    "bootstrap",
    "audit",
)


class FullLoadError(DiscoveryError):
    """Fatal full-load orchestration error."""


@dataclass(frozen=True)
class FullLoadPaths:
    source_roots_config: str
    normalization_schema: str
    classification_taxonomy: str
    extraction_rules: str
    wiki_config: str
    bootstrap_config: str
    audit_config: str
    live_control_sample_manifest: str


@dataclass(frozen=True)
class DiskBudgetConfig:
    max_derived_bytes: int
    tracked_dirs: tuple[str, ...]


@dataclass(frozen=True)
class RetryPolicy:
    max_phase_repair_loops: int
    repeated_non_improving_limit: int


@dataclass(frozen=True)
class FullLoadConfig:
    schema_version: int
    full_load_schema_version: int
    rules_version: int
    paths: FullLoadPaths
    disk_budget: DiskBudgetConfig
    retry_policy: RetryPolicy
    phase_gates: dict[str, dict[str, object]]


@dataclass(frozen=True)
class DiskSnapshot:
    total_bytes: int
    per_dir_bytes: dict[str, int]
    delta_bytes: int
    budget_exceeded: bool

    def to_dict(self) -> dict[str, object]:
        return {
            "total_bytes": self.total_bytes,
            "per_dir_bytes": dict(sorted(self.per_dir_bytes.items())),
            "delta_bytes": self.delta_bytes,
            "budget_exceeded": self.budget_exceeded,
        }


@dataclass(frozen=True)
class FullLoadPhaseStatus:
    phase: str
    started_at: str
    finished_at: str
    success: bool
    summary: dict[str, object]
    gate_passed: bool
    gate_reason: str | None
    disk_snapshot: DiskSnapshot
    issue_bundle_path: str | None

    def to_dict(self) -> dict[str, object]:
        return {
            "phase": self.phase,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "success": self.success,
            "summary": self.summary,
            "gate_passed": self.gate_passed,
            "gate_reason": self.gate_reason,
            "disk_snapshot": self.disk_snapshot.to_dict(),
            "issue_bundle_path": self.issue_bundle_path,
        }


@dataclass(frozen=True)
class FullLoadPhaseRecord:
    phase: str
    input_fingerprint: str
    last_result_status: str
    last_successful_run_id: str | None
    last_attempted_at: str | None
    last_failure_signature: str | None
    consecutive_failure_count: int
    last_failure_metric: int | None
    last_issue_bundle_path: str | None

    def to_dict(self) -> dict[str, object]:
        return {
            "phase": self.phase,
            "input_fingerprint": self.input_fingerprint,
            "last_result_status": self.last_result_status,
            "last_successful_run_id": self.last_successful_run_id,
            "last_attempted_at": self.last_attempted_at,
            "last_failure_signature": self.last_failure_signature,
            "consecutive_failure_count": self.consecutive_failure_count,
            "last_failure_metric": self.last_failure_metric,
            "last_issue_bundle_path": self.last_issue_bundle_path,
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "FullLoadPhaseRecord":
        return cls(
            phase=str(data["phase"]),
            input_fingerprint=str(data["input_fingerprint"]),
            last_result_status=str(data["last_result_status"]),
            last_successful_run_id=str(data["last_successful_run_id"]) if data.get("last_successful_run_id") else None,
            last_attempted_at=str(data["last_attempted_at"]) if data.get("last_attempted_at") else None,
            last_failure_signature=str(data["last_failure_signature"]) if data.get("last_failure_signature") else None,
            consecutive_failure_count=int(data.get("consecutive_failure_count", 0)),
            last_failure_metric=int(data["last_failure_metric"]) if data.get("last_failure_metric") is not None else None,
            last_issue_bundle_path=str(data["last_issue_bundle_path"]) if data.get("last_issue_bundle_path") else None,
        )


@dataclass(frozen=True)
class FullLoadStateRecord:
    full_load_schema_version: int
    rules_version: int
    last_run_id: str
    last_successful_run_id: str | None
    last_result_status: str
    last_completed_phase: str | None
    last_failed_phase: str | None
    last_stop_reason: str | None
    phase_records: tuple[FullLoadPhaseRecord, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "full_load_schema_version": self.full_load_schema_version,
            "rules_version": self.rules_version,
            "last_run_id": self.last_run_id,
            "last_successful_run_id": self.last_successful_run_id,
            "last_result_status": self.last_result_status,
            "last_completed_phase": self.last_completed_phase,
            "last_failed_phase": self.last_failed_phase,
            "last_stop_reason": self.last_stop_reason,
            "phase_records": [record.to_dict() for record in self.phase_records],
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "FullLoadStateRecord":
        return cls(
            full_load_schema_version=int(data["full_load_schema_version"]),
            rules_version=int(data["rules_version"]),
            last_run_id=str(data["last_run_id"]),
            last_successful_run_id=str(data["last_successful_run_id"]) if data.get("last_successful_run_id") else None,
            last_result_status=str(data["last_result_status"]),
            last_completed_phase=str(data["last_completed_phase"]) if data.get("last_completed_phase") else None,
            last_failed_phase=str(data["last_failed_phase"]) if data.get("last_failed_phase") else None,
            last_stop_reason=str(data["last_stop_reason"]) if data.get("last_stop_reason") else None,
            phase_records=tuple(FullLoadPhaseRecord.from_dict(item) for item in data.get("phase_records", [])),
        )

    @property
    def phase_record_map(self) -> dict[str, FullLoadPhaseRecord]:
        return {record.phase: record for record in self.phase_records}


@dataclass(frozen=True)
class FullLoadNotice:
    run_id: str
    severity: str
    notice_type: str
    summary: str

    def to_dict(self) -> dict[str, object]:
        return {
            "run_id": self.run_id,
            "severity": self.severity,
            "notice_type": self.notice_type,
            "summary": self.summary,
        }


@dataclass(frozen=True)
class FullLoadRunReport:
    run_id: str
    started_at: str
    finished_at: str
    phase_statuses: tuple[FullLoadPhaseStatus, ...]
    success: bool
    last_completed_phase: str | None
    failed_phase: str | None
    stop_reason: str | None
    fatal_error_summary: str | None

    def to_dict(self) -> dict[str, object]:
        return {
            "run_id": self.run_id,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "phase_statuses": [status.to_dict() for status in self.phase_statuses],
            "success": self.success,
            "last_completed_phase": self.last_completed_phase,
            "failed_phase": self.failed_phase,
            "stop_reason": self.stop_reason,
            "fatal_error_summary": self.fatal_error_summary,
        }


@dataclass(frozen=True)
class FullLoadResult:
    report: FullLoadRunReport
    state_path: Path
    run_log_path: Path
    notice_log_path: Path


def run_full_load(
    config_path: Path | str,
    state_dir: Path | str,
    audits_dir: Path | str,
    *,
    normalized_dir: Path | str = Path("normalized"),
    segmented_dir: Path | str = Path("segmented"),
    classified_dir: Path | str = Path("classified"),
    extracted_dir: Path | str = Path("extracted"),
    wiki_dir: Path | str = Path("wiki"),
    bootstrap_dir: Path | str = Path("bootstrap"),
) -> FullLoadResult:
    config_path = Path(config_path)
    state_dir = Path(state_dir)
    audits_dir = Path(audits_dir)
    normalized_dir = Path(normalized_dir)
    segmented_dir = Path(segmented_dir)
    classified_dir = Path(classified_dir)
    extracted_dir = Path(extracted_dir)
    wiki_dir = Path(wiki_dir)
    bootstrap_dir = Path(bootstrap_dir)

    state_path = state_dir / "full_load_state.json"
    run_log_path = state_dir / "full_load_runs.jsonl"
    notice_log_path = audits_dir / "full_load_notices.jsonl"

    ensure_directory(state_dir)
    ensure_directory(audits_dir)

    run_id = f"full-load-{utc_now().replace(':', '').replace('.', '').replace('-', '')}"
    started_at = utc_now()
    previous_state_text = state_path.read_text(encoding="utf-8") if state_path.exists() else None
    previous_run_log_text = run_log_path.read_text(encoding="utf-8") if run_log_path.exists() else ""
    previous_notice_log_text = notice_log_path.read_text(encoding="utf-8") if notice_log_path.exists() else ""

    config = load_full_load_config(config_path)
    paths = resolve_full_load_paths(config, config_path)
    previous_state = load_full_load_state(state_path)
    phase_fingerprints = build_phase_fingerprints(paths)
    tracked_dirs = resolve_tracked_dirs(
        config=config,
        state_dir=state_dir,
        audits_dir=audits_dir,
        normalized_dir=normalized_dir,
        segmented_dir=segmented_dir,
        classified_dir=classified_dir,
        extracted_dir=extracted_dir,
        wiki_dir=wiki_dir,
        bootstrap_dir=bootstrap_dir,
    )

    notices: list[FullLoadNotice] = []
    phase_statuses: list[FullLoadPhaseStatus] = []
    last_completed_phase: str | None = None
    failed_phase: str | None = None
    stop_reason: str | None = None
    fatal_error_summary: str | None = None
    previous_total_bytes = measure_derived_disk_usage(tracked_dirs, config.disk_budget.max_derived_bytes).total_bytes

    try:
        for phase in PHASE_ORDER:
            started_phase_at = utc_now()
            result = run_phase(
                phase=phase,
                paths=paths,
                state_dir=state_dir,
                audits_dir=audits_dir,
                normalized_dir=normalized_dir,
                segmented_dir=segmented_dir,
                classified_dir=classified_dir,
                extracted_dir=extracted_dir,
                wiki_dir=wiki_dir,
                bootstrap_dir=bootstrap_dir,
            )
            finished_phase_at = utc_now()
            disk_snapshot = measure_derived_disk_usage(
                tracked_dirs,
                config.disk_budget.max_derived_bytes,
                previous_total_bytes=previous_total_bytes,
            )
            previous_total_bytes = disk_snapshot.total_bytes
            gate = evaluate_phase_gate(
                phase=phase,
                result=result,
                config=config,
                audits_dir=audits_dir,
                classified_dir=classified_dir,
                extracted_dir=extracted_dir,
            )
            issue_bundle_path: str | None = None

            if disk_snapshot.budget_exceeded:
                failed_phase = phase
                stop_reason = "disk_budget_exceeded"
                issue_bundle_path = write_issue_bundle(
                    run_id=run_id,
                    phase=phase,
                    audits_dir=audits_dir,
                    paths=paths,
                    stop_reason=stop_reason,
                    result=result,
                    gate=gate,
                    disk_snapshot=disk_snapshot,
                )
                phase_statuses.append(
                    FullLoadPhaseStatus(
                        phase=phase,
                        started_at=started_phase_at,
                        finished_at=finished_phase_at,
                        success=False,
                        summary=summarize_phase_result(result),
                        gate_passed=False,
                        gate_reason="derived artifact footprint exceeded configured budget",
                        disk_snapshot=disk_snapshot,
                        issue_bundle_path=issue_bundle_path,
                    )
                )
                fatal_error_summary = "Derived artifact footprint exceeded configured budget"
                break

            if not bool(result.report.success) or not gate["passed"]:
                failed_phase = phase
                failure_signature = build_failure_signature(phase, result, gate)
                failure_metric = int(gate.get("metric", 1))
                prior_record = previous_state.phase_record_map.get(phase) if previous_state is not None else None
                same_signature = prior_record is not None and prior_record.last_failure_signature == failure_signature
                no_improvement = (
                    same_signature
                    and prior_record.last_failure_metric is not None
                    and failure_metric >= prior_record.last_failure_metric
                )
                consecutive_failure_count = prior_record.consecutive_failure_count + 1 if no_improvement else 1
                if consecutive_failure_count >= config.retry_policy.max_phase_repair_loops:
                    stop_reason = "retry_exhausted"
                elif consecutive_failure_count >= config.retry_policy.repeated_non_improving_limit:
                    stop_reason = "repeated_non_improving_failure"
                else:
                    stop_reason = "repair_required"
                issue_bundle_path = write_issue_bundle(
                    run_id=run_id,
                    phase=phase,
                    audits_dir=audits_dir,
                    paths=paths,
                    stop_reason=stop_reason,
                    result=result,
                    gate=gate,
                    disk_snapshot=disk_snapshot,
                    failure_signature=failure_signature,
                    failure_metric=failure_metric,
                    consecutive_failure_count=consecutive_failure_count,
                )
                phase_statuses.append(
                    FullLoadPhaseStatus(
                        phase=phase,
                        started_at=started_phase_at,
                        finished_at=finished_phase_at,
                        success=False,
                        summary=summarize_phase_result(result),
                        gate_passed=False,
                        gate_reason=str(gate["reason"]),
                        disk_snapshot=disk_snapshot,
                        issue_bundle_path=issue_bundle_path,
                    )
                )
                fatal_error_summary = result.report.fatal_error_summary or str(gate["reason"])
                break

            phase_statuses.append(
                FullLoadPhaseStatus(
                    phase=phase,
                    started_at=started_phase_at,
                    finished_at=finished_phase_at,
                    success=True,
                    summary=summarize_phase_result(result),
                    gate_passed=True,
                    gate_reason=None,
                    disk_snapshot=disk_snapshot,
                    issue_bundle_path=None,
                )
            )
            last_completed_phase = phase

        success = failed_phase is None and stop_reason is None
        report = FullLoadRunReport(
            run_id=run_id,
            started_at=started_at,
            finished_at=utc_now(),
            phase_statuses=tuple(phase_statuses),
            success=success,
            last_completed_phase=last_completed_phase,
            failed_phase=failed_phase,
            stop_reason=stop_reason,
            fatal_error_summary=fatal_error_summary,
        )
        next_state = build_full_load_state(
            previous_state=previous_state,
            config=config,
            phase_fingerprints=phase_fingerprints,
            phase_statuses=phase_statuses,
            run_id=run_id,
            success=success,
            last_completed_phase=last_completed_phase,
            failed_phase=failed_phase,
            stop_reason=stop_reason,
        )
        persist_full_load_snapshot(
            state_path=state_path,
            run_log_path=run_log_path,
            notice_log_path=notice_log_path,
            previous_run_log_text=previous_run_log_text,
            previous_notice_log_text=previous_notice_log_text,
            report=report,
            state=next_state,
            notices=notices,
        )
        return FullLoadResult(report=report, state_path=state_path, run_log_path=run_log_path, notice_log_path=notice_log_path)
    except Exception as exc:
        failure_report = FullLoadRunReport(
            run_id=run_id,
            started_at=started_at,
            finished_at=utc_now(),
            phase_statuses=tuple(phase_statuses),
            success=False,
            last_completed_phase=last_completed_phase,
            failed_phase=failed_phase,
            stop_reason=stop_reason or "fatal_error",
            fatal_error_summary=str(exc),
        )
        if previous_state_text is not None:
            atomic_write_text(state_path, previous_state_text)
        atomic_write_text(run_log_path, append_jsonl_text(previous_run_log_text, failure_report.to_dict()))
        if previous_notice_log_text:
            atomic_write_text(notice_log_path, previous_notice_log_text)
        return FullLoadResult(report=failure_report, state_path=state_path, run_log_path=run_log_path, notice_log_path=notice_log_path)


def load_full_load_config(config_path: Path) -> FullLoadConfig:
    try:
        payload = json.loads(config_path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError as exc:
        raise FullLoadError(f"Missing full-load config: {config_path}") from exc
    except json.JSONDecodeError as exc:
        raise FullLoadError(f"Invalid full-load config JSON: {config_path}") from exc

    paths_payload = payload.get("paths")
    disk_payload = payload.get("disk_budget")
    retry_payload = payload.get("retry_policy")
    gates_payload = payload.get("phase_gates")
    if not isinstance(paths_payload, dict):
        raise FullLoadError("Full-load config must define paths")
    if not isinstance(disk_payload, dict):
        raise FullLoadError("Full-load config must define disk_budget")
    if not isinstance(retry_payload, dict):
        raise FullLoadError("Full-load config must define retry_policy")
    if not isinstance(gates_payload, dict):
        raise FullLoadError("Full-load config must define phase_gates")

    return FullLoadConfig(
        schema_version=int(payload["schema_version"]),
        full_load_schema_version=int(payload["full_load_schema_version"]),
        rules_version=int(payload["rules_version"]),
        paths=FullLoadPaths(
            source_roots_config=str(paths_payload["source_roots_config"]),
            normalization_schema=str(paths_payload["normalization_schema"]),
            classification_taxonomy=str(paths_payload["classification_taxonomy"]),
            extraction_rules=str(paths_payload["extraction_rules"]),
            wiki_config=str(paths_payload["wiki_config"]),
            bootstrap_config=str(paths_payload["bootstrap_config"]),
            audit_config=str(paths_payload["audit_config"]),
            live_control_sample_manifest=str(paths_payload["live_control_sample_manifest"]),
        ),
        disk_budget=DiskBudgetConfig(
            max_derived_bytes=int(disk_payload["max_derived_bytes"]),
            tracked_dirs=tuple(str(item) for item in disk_payload["tracked_dirs"]),
        ),
        retry_policy=RetryPolicy(
            max_phase_repair_loops=int(retry_payload["max_phase_repair_loops"]),
            repeated_non_improving_limit=int(retry_payload["repeated_non_improving_limit"]),
        ),
        phase_gates={str(key): dict(value) for key, value in gates_payload.items()},
    )


def load_full_load_state(state_path: Path) -> FullLoadStateRecord | None:
    if not state_path.exists():
        return None
    try:
        payload = json.loads(state_path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise FullLoadError(f"Invalid full-load state JSON: {state_path}") from exc
    if int(payload.get("schema_version", -1)) != STATE_SCHEMA_VERSION:
        raise FullLoadError(f"Unsupported full-load state schema version in {state_path}: {payload.get('schema_version')}")
    full_load_payload = payload.get("full_load")
    if not isinstance(full_load_payload, dict):
        raise FullLoadError(f"Missing full_load payload in {state_path}")
    return FullLoadStateRecord.from_dict(full_load_payload)


def resolve_full_load_paths(config: FullLoadConfig, config_path: Path) -> dict[str, Path]:
    base = config_path.parent
    resolved: dict[str, Path] = {}
    for key, value in {
        "source_roots": config.paths.source_roots_config,
        "normalization_schema": config.paths.normalization_schema,
        "classification_taxonomy": config.paths.classification_taxonomy,
        "extraction_rules": config.paths.extraction_rules,
        "wiki_config": config.paths.wiki_config,
        "bootstrap_config": config.paths.bootstrap_config,
        "audit_config": config.paths.audit_config,
        "live_control_sample_manifest": config.paths.live_control_sample_manifest,
    }.items():
        path = Path(value)
        resolved[key] = path if path.is_absolute() else (base / path).resolve()
    return resolved


def resolve_tracked_dirs(
    *,
    config: FullLoadConfig,
    state_dir: Path,
    audits_dir: Path,
    normalized_dir: Path,
    segmented_dir: Path,
    classified_dir: Path,
    extracted_dir: Path,
    wiki_dir: Path,
    bootstrap_dir: Path,
) -> dict[str, Path]:
    directory_map = {
        "normalized": normalized_dir,
        "segmented": segmented_dir,
        "classified": classified_dir,
        "extracted": extracted_dir,
        "wiki": wiki_dir,
        "bootstrap": bootstrap_dir,
        "state": state_dir,
        "audits": audits_dir,
    }
    missing = [name for name in config.disk_budget.tracked_dirs if name not in directory_map]
    if missing:
        raise FullLoadError(f"Unknown tracked dirs in full-load config: {', '.join(missing)}")
    return {name: directory_map[name] for name in config.disk_budget.tracked_dirs}


def build_phase_fingerprints(paths: dict[str, Path]) -> dict[str, str]:
    return {
        "discover": hash_payload({"config": hash_file(paths["source_roots"])}),
        "normalize": hash_payload({"config": hash_file(paths["source_roots"]), "schema": hash_file(paths["normalization_schema"])}),
        "segment": hash_payload({"phase": "segment"}),
        "classify": hash_payload({"taxonomy": hash_file(paths["classification_taxonomy"])}),
        "extract": hash_payload({"rules": hash_file(paths["extraction_rules"])}),
        "wiki": hash_payload({"config": hash_file(paths["wiki_config"])}),
        "bootstrap": hash_payload({"config": hash_file(paths["bootstrap_config"])}),
        "audit": hash_payload({"config": hash_file(paths["audit_config"])}),
    }


def run_phase(
    *,
    phase: str,
    paths: dict[str, Path],
    state_dir: Path,
    audits_dir: Path,
    normalized_dir: Path,
    segmented_dir: Path,
    classified_dir: Path,
    extracted_dir: Path,
    wiki_dir: Path,
    bootstrap_dir: Path,
) -> object:
    if phase == "discover":
        return run_discovery(config_path=paths["source_roots"], state_dir=state_dir)
    if phase == "normalize":
        return run_normalization(
            config_path=paths["source_roots"],
            state_dir=state_dir,
            schema_path=paths["normalization_schema"],
            normalized_dir=normalized_dir,
            audits_dir=audits_dir,
        )
    if phase == "segment":
        return run_segmentation(state_dir=state_dir, normalized_dir=normalized_dir, segmented_dir=segmented_dir)
    if phase == "classify":
        return run_classification(
            taxonomy_path=paths["classification_taxonomy"],
            state_dir=state_dir,
            normalized_dir=normalized_dir,
            segmented_dir=segmented_dir,
            classified_dir=classified_dir,
            audits_dir=audits_dir,
            source_roots_config_path=paths["source_roots"],
        )
    if phase == "extract":
        return run_extraction(
            rules_path=paths["extraction_rules"],
            state_dir=state_dir,
            normalized_dir=normalized_dir,
            classified_dir=classified_dir,
            extracted_dir=extracted_dir,
            audits_dir=audits_dir,
            source_roots_config_path=paths["source_roots"],
        )
    if phase == "wiki":
        return run_wiki(
            config_path=paths["wiki_config"],
            state_dir=state_dir,
            extracted_dir=extracted_dir,
            wiki_dir=wiki_dir,
            audits_dir=audits_dir,
        )
    if phase == "bootstrap":
        return run_bootstrap(
            config_path=paths["bootstrap_config"],
            state_dir=state_dir,
            extracted_dir=extracted_dir,
            wiki_dir=wiki_dir,
            bootstrap_dir=bootstrap_dir,
            audits_dir=audits_dir,
        )
    if phase == "audit":
        return run_audit(
            config_path=paths["audit_config"],
            state_dir=state_dir,
            extracted_dir=extracted_dir,
            wiki_dir=wiki_dir,
            bootstrap_dir=bootstrap_dir,
            audits_dir=audits_dir,
        )
    raise FullLoadError(f"Unsupported phase: {phase}")


def measure_derived_disk_usage(
    tracked_dirs: dict[str, Path],
    max_derived_bytes: int,
    *,
    previous_total_bytes: int = 0,
) -> DiskSnapshot:
    per_dir_bytes: dict[str, int] = {}
    total_bytes = 0
    for name, path in tracked_dirs.items():
        size_bytes = measure_path_bytes(path)
        per_dir_bytes[name] = size_bytes
        total_bytes += size_bytes
    return DiskSnapshot(
        total_bytes=total_bytes,
        per_dir_bytes=per_dir_bytes,
        delta_bytes=total_bytes - previous_total_bytes,
        budget_exceeded=total_bytes > max_derived_bytes,
    )


def measure_path_bytes(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(file_path.stat().st_size for file_path in path.rglob("*") if file_path.is_file())


def evaluate_phase_gate(
    *,
    phase: str,
    result: object,
    config: FullLoadConfig,
    audits_dir: Path,
    classified_dir: Path,
    extracted_dir: Path,
) -> dict[str, object]:
    gate_config = config.phase_gates.get(phase, {})
    if not bool(getattr(result, "report", None).success):
        return {
            "passed": False,
            "reason": getattr(result.report, "fatal_error_summary", None) or f"{phase} failed",
            "metric": 1,
            "details": {
                "blocking_issue_types": ["phase_failure"],
                "representative_examples": [getattr(result.report, "fatal_error_summary", None) or f"{phase} failed"],
            },
        }

    if phase == "classify" and gate_config.get("require_zero_unclassified"):
        return evaluate_classification_gate(result, audits_dir, classified_dir, gate_config)
    if phase == "extract" and gate_config.get("require_zero_unclassified"):
        return evaluate_extraction_gate(extracted_dir)
    if phase == "audit" and gate_config.get("require_zero_errors"):
        return evaluate_audit_gate(result, audits_dir)
    return {"passed": True, "reason": None, "metric": 0, "details": {}}


def evaluate_classification_gate(
    result: ClassificationResult,
    audits_dir: Path,
    classified_dir: Path,
    gate_config: dict[str, object],
) -> dict[str, object]:
    blocking_notice_types = {str(item) for item in gate_config.get("blocking_notice_types", [])}
    notice_path = audits_dir / "classification_notices.jsonl"
    notices = [
        notice
        for notice in read_jsonl_if_exists(notice_path)
        if str(notice.get("run_id", "")) == result.report.run_id
    ]
    notice_counts: dict[str, int] = {}
    representative_examples: list[dict[str, object]] = []
    failing_source_ids: set[str] = set()
    for notice in notices:
        notice_type = str(notice.get("notice_type", ""))
        notice_counts[notice_type] = notice_counts.get(notice_type, 0) + 1
        if len(representative_examples) < 10:
            representative_examples.append(notice)
        if notice_type in blocking_notice_types or notice_type == "taxonomy_gap":
            source_id = str(notice.get("source_id", ""))
            if source_id:
                failing_source_ids.add(source_id)

    unclassified_count = 0
    taxonomy_gap_count = 0
    for stats_path in sorted((classified_dir / "sources").glob("*/stats.json")):
        stats_payload = read_json_required(stats_path)
        primary_label_counts = dict(stats_payload.get("primary_label_counts", {}))
        source_unclassified_count = int(primary_label_counts.get("unclassified", 0))
        unclassified_count += source_unclassified_count
        source_taxonomy_gap_count = int(dict(stats_payload.get("notice_counts", {})).get("taxonomy_gap", 0))
        taxonomy_gap_count += source_taxonomy_gap_count
        if source_unclassified_count > 0 or source_taxonomy_gap_count > 0:
            source_id = str(stats_payload.get("source_id", ""))
            if source_id:
                failing_source_ids.add(source_id)
            if len(representative_examples) < 10:
                representative_examples.append(
                    {
                        "source_id": source_id,
                        "primary_label_counts": primary_label_counts,
                        "notice_counts": dict(stats_payload.get("notice_counts", {})),
                    }
                )
    metric = unclassified_count + taxonomy_gap_count
    if metric == 0:
        return {"passed": True, "reason": None, "metric": 0, "details": {}}
    blocking_issue_types: list[str] = []
    if unclassified_count > 0:
        blocking_issue_types.append("unclassified")
    if taxonomy_gap_count > 0:
        blocking_issue_types.append("taxonomy_gap")
    source_ids = sorted(failing_source_ids)
    return {
        "passed": False,
        "reason": "classification gate failed",
        "metric": metric,
        "details": {
            "blocking_issue_types": blocking_issue_types,
            "failing_source_ids": source_ids,
            "top_notice_types": dict(sorted(notice_counts.items())),
            "representative_examples": representative_examples,
            "recommended_scope": {"source_ids": source_ids},
        },
    }


def evaluate_extraction_gate(extracted_dir: Path) -> dict[str, object]:
    unclassified_observations: list[dict[str, object]] = []
    for items_path in sorted((extracted_dir / "sources").glob("*/items.jsonl")):
        for record in read_jsonl_if_exists(items_path):
            if str(record.get("primary_domain", "")) == "unclassified":
                unclassified_observations.append(record)
                if len(unclassified_observations) >= 10:
                    break
        if len(unclassified_observations) >= 10:
            break
    if not unclassified_observations:
        return {"passed": True, "reason": None, "metric": 0, "details": {}}
    source_ids = sorted({str(item.get("source_id", "")) for item in unclassified_observations if str(item.get("source_id", ""))})
    return {
        "passed": False,
        "reason": "extraction gate failed",
        "metric": len(unclassified_observations),
        "details": {
            "blocking_issue_types": ["unclassified"],
            "failing_source_ids": source_ids,
            "representative_examples": unclassified_observations,
            "recommended_scope": {"source_ids": source_ids},
        },
    }


def evaluate_audit_gate(result: AuditResult, audits_dir: Path) -> dict[str, object]:
    if int(result.report.error_finding_count) == 0:
        return {"passed": True, "reason": None, "metric": 0, "details": {}}
    findings: list[dict[str, object]] = []
    family_counts: dict[str, int] = {}
    for filename in ("contradictions.jsonl", "duplicates.jsonl", "stale_items.jsonl", "provenance_gaps.jsonl", "wiki_bootstrap_drift.jsonl"):
        family = filename.removesuffix(".jsonl")
        for finding in read_jsonl_if_exists(audits_dir / filename):
            if str(finding.get("severity", "")) != "error":
                continue
            family_counts[family] = family_counts.get(family, 0) + 1
            if len(findings) < 10:
                findings.append(finding)
    recommended_scope: dict[str, list[str]] = {"domains": [], "pages": [], "bootstrap_domains": []}
    for finding in findings:
        scope_kind = str(finding.get("scope_kind", ""))
        scope_key = str(finding.get("scope_key", ""))
        if scope_kind == "domain":
            recommended_scope["domains"].append(scope_key)
        elif scope_kind == "page":
            recommended_scope["pages"].append(scope_key)
        elif scope_kind == "bootstrap_domain":
            recommended_scope["bootstrap_domains"].append(scope_key)
    filtered_scope = {key: sorted(dict.fromkeys(values)) for key, values in recommended_scope.items() if values}
    return {
        "passed": False,
        "reason": "audit gate failed",
        "metric": int(result.report.error_finding_count),
        "details": {
            "blocking_issue_types": sorted(family_counts),
            "top_finding_families": dict(sorted(family_counts.items())),
            "representative_examples": findings,
            "recommended_scope": filtered_scope,
        },
    }


def write_issue_bundle(
    *,
    run_id: str,
    phase: str,
    audits_dir: Path,
    paths: dict[str, Path],
    stop_reason: str,
    result: object,
    gate: dict[str, object],
    disk_snapshot: DiskSnapshot,
    failure_signature: str | None = None,
    failure_metric: int | None = None,
    consecutive_failure_count: int | None = None,
) -> str:
    issue_dir = audits_dir / "full_load_issues" / run_id / phase
    ensure_directory(issue_dir)
    issue_path = issue_dir / "issue.json"
    payload = {
        "run_id": run_id,
        "phase": phase,
        "stop_reason": stop_reason,
        "phase_report": getattr(result.report, "to_dict", lambda: {})(),
        "phase_summary": summarize_phase_result(result),
        "gate": gate,
        "disk_snapshot": disk_snapshot.to_dict(),
        "failure_signature": failure_signature,
        "failure_metric": failure_metric,
        "consecutive_failure_count": consecutive_failure_count,
        "control_sample_manifest_path": str(paths["live_control_sample_manifest"]),
        "required_validation_sequence": [
            "targeted regression test",
            "live control sample suite",
            "failing slice rerun",
            "full current phase rerun",
        ],
    }
    atomic_write_text(issue_path, json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return str(issue_path)


def build_failure_signature(phase: str, result: object, gate: dict[str, object]) -> str:
    payload = {
        "phase": phase,
        "success": bool(result.report.success),
        "fatal_error_summary": getattr(result.report, "fatal_error_summary", None),
        "reason": gate.get("reason"),
        "blocking_issue_types": list(gate.get("details", {}).get("blocking_issue_types", [])),
    }
    return hashlib.sha1(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()[:16]


def build_full_load_state(
    *,
    previous_state: FullLoadStateRecord | None,
    config: FullLoadConfig,
    phase_fingerprints: dict[str, str],
    phase_statuses: list[FullLoadPhaseStatus],
    run_id: str,
    success: bool,
    last_completed_phase: str | None,
    failed_phase: str | None,
    stop_reason: str | None,
) -> FullLoadStateRecord:
    previous_phase_records = previous_state.phase_record_map if previous_state is not None else {}
    status_by_phase = {status.phase: status for status in phase_statuses}
    phase_records: list[FullLoadPhaseRecord] = []
    for phase in PHASE_ORDER:
        previous_record = previous_phase_records.get(phase)
        status = status_by_phase.get(phase)
        if status is None:
            phase_records.append(
                previous_record
                or FullLoadPhaseRecord(
                    phase=phase,
                    input_fingerprint=phase_fingerprints.get(phase, ""),
                    last_result_status="never_ran",
                    last_successful_run_id=None,
                    last_attempted_at=None,
                    last_failure_signature=None,
                    consecutive_failure_count=0,
                    last_failure_metric=None,
                    last_issue_bundle_path=None,
                )
            )
            continue
        if status.success:
            phase_records.append(
                FullLoadPhaseRecord(
                    phase=phase,
                    input_fingerprint=phase_fingerprints.get(phase, ""),
                    last_result_status="succeeded",
                    last_successful_run_id=run_id,
                    last_attempted_at=status.finished_at,
                    last_failure_signature=None,
                    consecutive_failure_count=0,
                    last_failure_metric=None,
                    last_issue_bundle_path=None,
                )
            )
            continue
        issue_payload = read_json_required(Path(status.issue_bundle_path)) if status.issue_bundle_path else {}
        failure_signature = str(issue_payload.get("failure_signature", "")) or None
        failure_metric = int(issue_payload["failure_metric"]) if issue_payload.get("failure_metric") is not None else None
        consecutive_failure_count = int(issue_payload["consecutive_failure_count"]) if issue_payload.get("consecutive_failure_count") is not None else 1
        phase_records.append(
            FullLoadPhaseRecord(
                phase=phase,
                input_fingerprint=phase_fingerprints.get(phase, ""),
                last_result_status="failed",
                last_successful_run_id=previous_record.last_successful_run_id if previous_record else None,
                last_attempted_at=status.finished_at,
                last_failure_signature=failure_signature,
                consecutive_failure_count=consecutive_failure_count,
                last_failure_metric=failure_metric,
                last_issue_bundle_path=status.issue_bundle_path,
            )
        )

    return FullLoadStateRecord(
        full_load_schema_version=FULL_LOAD_SCHEMA_VERSION,
        rules_version=config.rules_version,
        last_run_id=run_id,
        last_successful_run_id=run_id if success else (previous_state.last_successful_run_id if previous_state else None),
        last_result_status="succeeded" if success else "failed",
        last_completed_phase=last_completed_phase,
        last_failed_phase=failed_phase,
        last_stop_reason=stop_reason,
        phase_records=tuple(phase_records),
    )


def persist_full_load_snapshot(
    *,
    state_path: Path,
    run_log_path: Path,
    notice_log_path: Path,
    previous_run_log_text: str,
    previous_notice_log_text: str,
    report: FullLoadRunReport,
    state: FullLoadStateRecord,
    notices: list[FullLoadNotice],
) -> None:
    payload = {
        "schema_version": STATE_SCHEMA_VERSION,
        "generated_at": utc_now(),
        "full_load": state.to_dict(),
    }
    atomic_write_text(state_path, json.dumps(payload, indent=2, sort_keys=True) + "\n")
    atomic_write_text(run_log_path, append_jsonl_text(previous_run_log_text, report.to_dict()))
    atomic_write_text(notice_log_path, append_jsonl_text(previous_notice_log_text, [notice.to_dict() for notice in notices]))


def read_json_required(path: Path) -> dict[str, object]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError as exc:
        raise FullLoadError(f"Missing JSON artifact: {path}") from exc
    except json.JSONDecodeError as exc:
        raise FullLoadError(f"Invalid JSON artifact: {path}") from exc
    if not isinstance(payload, dict):
        raise FullLoadError(f"JSON artifact root must be an object: {path}")
    return payload


def read_jsonl_if_exists(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        return []
    records: list[dict[str, object]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        payload = json.loads(line)
        if isinstance(payload, dict):
            records.append(payload)
    return records


def hash_payload(payload: Any) -> str:
    return hashlib.sha1(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
