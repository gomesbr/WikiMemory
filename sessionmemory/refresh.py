from __future__ import annotations

import hashlib
import json
import os
import socket
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from . import audit, bootstrap, classification, discovery, extraction, normalization, segmentation, wiki
from .audit import AuditResult, run_audit
from .bootstrap import BootstrapResult, run_bootstrap
from .classification import ClassificationResult, run_classification
from .discovery import DiscoveryError, atomic_write_text, ensure_directory, load_registry, run_discovery, utc_now
from .extraction import ExtractionResult, load_extraction_state, run_extraction
from .normalization import NormalizationResult, append_jsonl_text, run_normalization
from .segmentation import SegmentationResult, run_segmentation
from .wiki import WikiResult, run_wiki

STATE_SCHEMA_VERSION = 1
REFRESH_SCHEMA_VERSION = 1
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
SCOPABLE_PHASES = {"segment", "classify", "extract", "wiki", "bootstrap", "audit"}


class RefreshError(DiscoveryError):
    """Fatal refresh orchestration error."""


class PhaseFailure(RefreshError):
    def __init__(self, phase: str, message: str) -> None:
        super().__init__(message)
        self.phase = phase


@dataclass(frozen=True)
class RefreshPaths:
    source_roots_config: str
    normalization_schema: str
    classification_taxonomy: str
    extraction_rules: str
    wiki_config: str
    bootstrap_config: str
    audit_config: str


@dataclass(frozen=True)
class RefreshLockConfig:
    lock_path: str
    stale_after_minutes: int


@dataclass(frozen=True)
class RefreshConfig:
    schema_version: int
    refresh_schema_version: int
    rules_version: int
    paths: RefreshPaths
    lock: RefreshLockConfig


@dataclass(frozen=True)
class RefreshPhaseStatus:
    phase: str
    scope_mode: str
    source_ids: tuple[str, ...]
    started_at: str
    finished_at: str
    success: bool
    skipped: bool
    summary: dict[str, object]
    fatal_error_summary: str | None

    def to_dict(self) -> dict[str, object]:
        return {
            "phase": self.phase,
            "scope_mode": self.scope_mode,
            "source_ids": list(self.source_ids),
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "success": self.success,
            "skipped": self.skipped,
            "summary": self.summary,
            "fatal_error_summary": self.fatal_error_summary,
        }


@dataclass(frozen=True)
class RefreshPhaseRecord:
    phase: str
    input_fingerprint: str
    last_scope_mode: str
    last_result_status: str
    last_successful_run_id: str | None
    last_completed_at: str | None

    def to_dict(self) -> dict[str, object]:
        return {
            "phase": self.phase,
            "input_fingerprint": self.input_fingerprint,
            "last_scope_mode": self.last_scope_mode,
            "last_result_status": self.last_result_status,
            "last_successful_run_id": self.last_successful_run_id,
            "last_completed_at": self.last_completed_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "RefreshPhaseRecord":
        return cls(
            phase=str(data["phase"]),
            input_fingerprint=str(data["input_fingerprint"]),
            last_scope_mode=str(data["last_scope_mode"]),
            last_result_status=str(data["last_result_status"]),
            last_successful_run_id=str(data["last_successful_run_id"]) if data.get("last_successful_run_id") else None,
            last_completed_at=str(data["last_completed_at"]) if data.get("last_completed_at") else None,
        )


@dataclass(frozen=True)
class RefreshStateRecord:
    refresh_schema_version: int
    rules_version: int
    last_run_id: str
    last_successful_run_id: str | None
    last_result_status: str
    last_completed_phase: str | None
    last_failed_phase: str | None
    last_changed_source_ids: tuple[str, ...]
    last_touched_domains: tuple[str, ...]
    phase_records: tuple[RefreshPhaseRecord, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "refresh_schema_version": self.refresh_schema_version,
            "rules_version": self.rules_version,
            "last_run_id": self.last_run_id,
            "last_successful_run_id": self.last_successful_run_id,
            "last_result_status": self.last_result_status,
            "last_completed_phase": self.last_completed_phase,
            "last_failed_phase": self.last_failed_phase,
            "last_changed_source_ids": list(self.last_changed_source_ids),
            "last_touched_domains": list(self.last_touched_domains),
            "phase_records": [record.to_dict() for record in self.phase_records],
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "RefreshStateRecord":
        return cls(
            refresh_schema_version=int(data["refresh_schema_version"]),
            rules_version=int(data["rules_version"]),
            last_run_id=str(data["last_run_id"]),
            last_successful_run_id=str(data["last_successful_run_id"]) if data.get("last_successful_run_id") else None,
            last_result_status=str(data["last_result_status"]),
            last_completed_phase=str(data["last_completed_phase"]) if data.get("last_completed_phase") else None,
            last_failed_phase=str(data["last_failed_phase"]) if data.get("last_failed_phase") else None,
            last_changed_source_ids=tuple(str(item) for item in data.get("last_changed_source_ids", [])),
            last_touched_domains=tuple(str(item) for item in data.get("last_touched_domains", [])),
            phase_records=tuple(
                RefreshPhaseRecord.from_dict(item)
                for item in data.get("phase_records", [])
            ),
        )

    @property
    def phase_record_map(self) -> dict[str, RefreshPhaseRecord]:
        return {record.phase: record for record in self.phase_records}


@dataclass(frozen=True)
class RefreshNotice:
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
class RefreshRunReport:
    run_id: str
    started_at: str
    finished_at: str
    phase_statuses: tuple[RefreshPhaseStatus, ...]
    changed_source_ids: tuple[str, ...]
    touched_domains: tuple[str, ...]
    warning_count: int
    error_count: int
    success: bool
    last_completed_phase: str | None
    failed_phase: str | None
    fatal_error_summary: str | None

    def to_dict(self) -> dict[str, object]:
        return {
            "run_id": self.run_id,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "phase_statuses": [status.to_dict() for status in self.phase_statuses],
            "changed_source_ids": list(self.changed_source_ids),
            "touched_domains": list(self.touched_domains),
            "warning_count": self.warning_count,
            "error_count": self.error_count,
            "success": self.success,
            "last_completed_phase": self.last_completed_phase,
            "failed_phase": self.failed_phase,
            "fatal_error_summary": self.fatal_error_summary,
        }


@dataclass(frozen=True)
class RefreshResult:
    report: RefreshRunReport
    state_path: Path
    run_log_path: Path
    notice_log_path: Path


def run_refresh(
    config_path: Path | str,
    state_dir: Path | str,
    audits_dir: Path | str,
    source_ids: Iterable[str] | None = None,
    *,
    normalized_dir: Path | str = Path("normalized"),
    segmented_dir: Path | str = Path("segmented"),
    classified_dir: Path | str = Path("classified"),
    extracted_dir: Path | str = Path("extracted"),
    wiki_dir: Path | str = Path("wiki"),
    bootstrap_dir: Path | str = Path("bootstrap"),
) -> RefreshResult:
    config_path = Path(config_path)
    state_dir = Path(state_dir)
    audits_dir = Path(audits_dir)
    normalized_dir = Path(normalized_dir)
    segmented_dir = Path(segmented_dir)
    classified_dir = Path(classified_dir)
    extracted_dir = Path(extracted_dir)
    wiki_dir = Path(wiki_dir)
    bootstrap_dir = Path(bootstrap_dir)

    state_path = state_dir / "refresh_state.json"
    run_log_path = state_dir / "refresh_runs.jsonl"
    notice_log_path = audits_dir / "refresh_notices.jsonl"

    ensure_directory(state_dir)
    ensure_directory(audits_dir)

    run_id = f"refresh-{utc_now().replace(':', '').replace('.', '').replace('-', '')}"
    started_at = utc_now()

    previous_state_text = state_path.read_text(encoding="utf-8") if state_path.exists() else None
    previous_run_log_text = run_log_path.read_text(encoding="utf-8") if run_log_path.exists() else ""
    previous_notice_log_text = notice_log_path.read_text(encoding="utf-8") if notice_log_path.exists() else ""

    config = load_refresh_config(config_path)
    paths = resolve_refresh_paths(config, config_path)
    lock_path = resolve_lock_path(config, state_dir)
    previous_refresh_state = load_refresh_state(state_path)
    notices: list[RefreshNotice] = []
    phase_statuses: list[RefreshPhaseStatus] = []
    changed_source_ids: tuple[str, ...] = ()
    touched_domains: tuple[str, ...] = ()
    warning_count = 0
    error_count = 0
    last_completed_phase: str | None = None
    failed_phase: str | None = None

    lock_acquired = False
    try:
        notices.extend(acquire_refresh_lock(lock_path=lock_path, run_id=run_id, stale_after_minutes=config.lock.stale_after_minutes))
        lock_acquired = True

        registry_path = state_dir / "source_registry.json"
        registry_before = load_registry(registry_path) if registry_path.exists() else {}

        discover_status, discover_result = execute_phase(
            phase="discover",
            scope_mode="full",
            source_ids=(),
            callback=lambda: run_discovery(config_path=paths["source_roots"], state_dir=state_dir),
        )
        phase_statuses.append(discover_status)
        if not discover_status.success:
            raise PhaseFailure("discover", discover_status.fatal_error_summary or "discover failed")
        last_completed_phase = "discover"
        heartbeat_refresh_lock(lock_path, run_id)

        registry_after = load_registry(registry_path)
        changed_source_ids = tuple(resolve_changed_source_ids(registry_before, registry_after))

        requested_source_ids = tuple(sorted(dict.fromkeys(str(source_id) for source_id in source_ids))) if source_ids else ()
        if requested_source_ids:
            missing_requested = [source_id for source_id in requested_source_ids if source_id not in registry_after]
            if missing_requested:
                raise RefreshError(f"Requested source_ids are missing from discovery registry: {', '.join(missing_requested)}")

        normalize_status, normalize_result = execute_phase(
            phase="normalize",
            scope_mode="full",
            source_ids=(),
            callback=lambda: run_normalization(
                config_path=paths["source_roots"],
                state_dir=state_dir,
                schema_path=paths["normalization_schema"],
                normalized_dir=normalized_dir,
                audits_dir=audits_dir,
            ),
        )
        phase_statuses.append(normalize_status)
        if not normalize_status.success:
            raise PhaseFailure("normalize", normalize_status.fatal_error_summary or "normalize failed")
        last_completed_phase = "normalize"
        heartbeat_refresh_lock(lock_path, run_id)

        phase_fingerprints = build_phase_fingerprints(paths)
        phase_modes, scoped_source_ids = resolve_phase_modes(
            previous_refresh_state=previous_refresh_state,
            phase_fingerprints=phase_fingerprints,
            state_dir=state_dir,
            requested_source_ids=requested_source_ids,
            changed_source_ids=changed_source_ids,
        )

        downstream_results = execute_downstream_phases(
            phase_modes=phase_modes,
            scoped_source_ids=scoped_source_ids,
            paths=paths,
            state_dir=state_dir,
            audits_dir=audits_dir,
            normalized_dir=normalized_dir,
            segmented_dir=segmented_dir,
            classified_dir=classified_dir,
            extracted_dir=extracted_dir,
            wiki_dir=wiki_dir,
            bootstrap_dir=bootstrap_dir,
            run_id=run_id,
            lock_path=lock_path,
        )
        phase_statuses.extend(downstream_results["phase_statuses"])
        warning_count += downstream_results["warning_count"]
        error_count += downstream_results["error_count"]
        if downstream_results["last_completed_phase"] is not None:
            last_completed_phase = downstream_results["last_completed_phase"]

        audit_result = downstream_results["results"].get("audit")
        if isinstance(audit_result, AuditResult) and audit_result.report.error_finding_count > 0:
            error_count += audit_result.report.error_finding_count
            failed_phase = "audit"
            raise PhaseFailure("audit", f"audit produced {audit_result.report.error_finding_count} error findings")

        touched_domains = collect_touched_domains(
            state_dir=state_dir,
            requested_source_ids=requested_source_ids,
            changed_source_ids=changed_source_ids,
            full_extract=phase_modes["extract"] == "full",
        )
        report = RefreshRunReport(
            run_id=run_id,
            started_at=started_at,
            finished_at=utc_now(),
            phase_statuses=tuple(phase_statuses),
            changed_source_ids=changed_source_ids,
            touched_domains=touched_domains,
            warning_count=warning_count,
            error_count=error_count,
            success=True,
            last_completed_phase=last_completed_phase,
            failed_phase=None,
            fatal_error_summary=None,
        )
        next_state = build_refresh_state(
            previous_state=previous_refresh_state,
            config=config,
            phase_fingerprints=phase_fingerprints,
            phase_statuses=phase_statuses,
            run_id=run_id,
            success=True,
            last_completed_phase=last_completed_phase,
            failed_phase=None,
            changed_source_ids=changed_source_ids,
            touched_domains=touched_domains,
        )
        persist_refresh_snapshot(
            state_path=state_path,
            run_log_path=run_log_path,
            notice_log_path=notice_log_path,
            previous_run_log_text=previous_run_log_text,
            previous_notice_log_text=previous_notice_log_text,
            report=report,
            state=next_state,
            notices=notices,
        )
        return RefreshResult(report=report, state_path=state_path, run_log_path=run_log_path, notice_log_path=notice_log_path)
    except PhaseFailure as exc:
        failed_phase = exc.phase
        report = RefreshRunReport(
            run_id=run_id,
            started_at=started_at,
            finished_at=utc_now(),
            phase_statuses=tuple(phase_statuses),
            changed_source_ids=changed_source_ids,
            touched_domains=touched_domains,
            warning_count=warning_count,
            error_count=error_count,
            success=False,
            last_completed_phase=last_completed_phase,
            failed_phase=failed_phase,
            fatal_error_summary=str(exc),
        )
        next_state = build_refresh_state(
            previous_state=previous_refresh_state,
            config=config,
            phase_fingerprints=build_phase_fingerprints(paths),
            phase_statuses=phase_statuses,
            run_id=run_id,
            success=False,
            last_completed_phase=last_completed_phase,
            failed_phase=failed_phase,
            changed_source_ids=changed_source_ids,
            touched_domains=touched_domains,
        )
        persist_refresh_snapshot(
            state_path=state_path,
            run_log_path=run_log_path,
            notice_log_path=notice_log_path,
            previous_run_log_text=previous_run_log_text,
            previous_notice_log_text=previous_notice_log_text,
            report=report,
            state=next_state,
            notices=notices,
        )
        return RefreshResult(report=report, state_path=state_path, run_log_path=run_log_path, notice_log_path=notice_log_path)
    except Exception as exc:
        failure_report = RefreshRunReport(
            run_id=run_id,
            started_at=started_at,
            finished_at=utc_now(),
            phase_statuses=tuple(phase_statuses),
            changed_source_ids=changed_source_ids,
            touched_domains=touched_domains,
            warning_count=warning_count,
            error_count=error_count,
            success=False,
            last_completed_phase=last_completed_phase,
            failed_phase=failed_phase,
            fatal_error_summary=str(exc),
        )
        if previous_state_text is not None:
            atomic_write_text(state_path, previous_state_text)
        atomic_write_text(run_log_path, append_jsonl_text(previous_run_log_text, failure_report.to_dict()))
        if previous_notice_log_text:
            atomic_write_text(notice_log_path, previous_notice_log_text)
        return RefreshResult(report=failure_report, state_path=state_path, run_log_path=run_log_path, notice_log_path=notice_log_path)
    finally:
        if lock_acquired:
            release_refresh_lock(lock_path=lock_path, run_id=run_id)


def load_refresh_config(config_path: Path) -> RefreshConfig:
    try:
        payload = json.loads(config_path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError as exc:
        raise RefreshError(f"Missing refresh config: {config_path}") from exc
    except json.JSONDecodeError as exc:
        raise RefreshError(f"Invalid refresh config JSON: {config_path}") from exc
    paths_payload = payload.get("paths")
    lock_payload = payload.get("lock")
    if not isinstance(paths_payload, dict):
        raise RefreshError("Refresh config must define paths")
    if not isinstance(lock_payload, dict):
        raise RefreshError("Refresh config must define lock")
    return RefreshConfig(
        schema_version=int(payload["schema_version"]),
        refresh_schema_version=int(payload["refresh_schema_version"]),
        rules_version=int(payload["rules_version"]),
        paths=RefreshPaths(
            source_roots_config=str(paths_payload["source_roots_config"]),
            normalization_schema=str(paths_payload["normalization_schema"]),
            classification_taxonomy=str(paths_payload["classification_taxonomy"]),
            extraction_rules=str(paths_payload["extraction_rules"]),
            wiki_config=str(paths_payload["wiki_config"]),
            bootstrap_config=str(paths_payload["bootstrap_config"]),
            audit_config=str(paths_payload["audit_config"]),
        ),
        lock=RefreshLockConfig(
            lock_path=str(lock_payload["lock_path"]),
            stale_after_minutes=int(lock_payload["stale_after_minutes"]),
        ),
    )


def resolve_refresh_paths(config: RefreshConfig, config_path: Path) -> dict[str, Path]:
    base_dir = config_path.parent
    return {
        "source_roots": resolve_config_path(base_dir, config.paths.source_roots_config),
        "normalization_schema": resolve_config_path(base_dir, config.paths.normalization_schema),
        "classification_taxonomy": resolve_config_path(base_dir, config.paths.classification_taxonomy),
        "extraction_rules": resolve_config_path(base_dir, config.paths.extraction_rules),
        "wiki_config": resolve_config_path(base_dir, config.paths.wiki_config),
        "bootstrap_config": resolve_config_path(base_dir, config.paths.bootstrap_config),
        "audit_config": resolve_config_path(base_dir, config.paths.audit_config),
    }


def resolve_config_path(base_dir: Path, value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return (base_dir / path).resolve()


def resolve_lock_path(config: RefreshConfig, state_dir: Path) -> Path:
    path = Path(config.lock.lock_path)
    if path.is_absolute():
        return path
    if path.parts and path.parts[0].lower() == "state":
        path = Path(*path.parts[1:])
    return state_dir / path


def load_refresh_state(state_path: Path) -> RefreshStateRecord | None:
    if not state_path.exists():
        return None
    try:
        payload = json.loads(state_path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise RefreshError(f"Invalid refresh state JSON: {state_path}") from exc
    if int(payload.get("schema_version", -1)) != STATE_SCHEMA_VERSION:
        raise RefreshError(f"Unsupported refresh state schema version in {state_path}: {payload.get('schema_version')}")
    return RefreshStateRecord.from_dict(payload["refresh"])


def acquire_refresh_lock(lock_path: Path, run_id: str, stale_after_minutes: int) -> list[RefreshNotice]:
    ensure_directory(lock_path.parent)
    notices: list[RefreshNotice] = []
    if lock_path.exists():
        try:
            lock_payload = read_json_file(lock_path)
        except RefreshError:
            lock_payload = {}
        heartbeat_at = parse_iso_timestamp(str(lock_payload.get("heartbeat_at", "")))
        if heartbeat_at is not None:
            age_minutes = max(0, int((parse_iso_timestamp(utc_now()) - heartbeat_at).total_seconds() // 60))
            if age_minutes < stale_after_minutes:
                raise RefreshError("another refresh run is already active")
            notices.append(
                RefreshNotice(
                    run_id=run_id,
                    severity="warning",
                    notice_type="stale_lock_replaced",
                    summary=f"replaced stale refresh lock older than {age_minutes} minutes",
                )
            )
        else:
            notices.append(
                RefreshNotice(
                    run_id=run_id,
                    severity="warning",
                    notice_type="invalid_lock_replaced",
                    summary="replaced invalid refresh lock payload",
                )
            )
    write_lock_payload(lock_path=lock_path, run_id=run_id)
    return notices


def heartbeat_refresh_lock(lock_path: Path, run_id: str) -> None:
    if not lock_path.exists():
        return
    payload = read_json_file(lock_path)
    if str(payload.get("run_id", "")) != run_id:
        raise RefreshError("refresh lock was replaced during execution")
    write_lock_payload(lock_path=lock_path, run_id=run_id, started_at=str(payload.get("started_at", "")))


def release_refresh_lock(lock_path: Path, run_id: str) -> None:
    if not lock_path.exists():
        return
    try:
        payload = read_json_file(lock_path)
    except RefreshError:
        lock_path.unlink(missing_ok=True)
        return
    if str(payload.get("run_id", "")) == run_id:
        lock_path.unlink(missing_ok=True)


def write_lock_payload(lock_path: Path, run_id: str, started_at: str | None = None) -> None:
    now = utc_now()
    payload = {
        "run_id": run_id,
        "pid": os.getpid(),
        "hostname": socket.gethostname(),
        "started_at": started_at or now,
        "heartbeat_at": now,
        "command": "python -m sessionmemory refresh",
    }
    atomic_write_text(lock_path, json.dumps(payload, indent=2, sort_keys=True) + "\n")


def read_json_file(path: Path) -> dict[str, object]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise RefreshError(f"Invalid JSON file: {path}") from exc
    if not isinstance(payload, dict):
        raise RefreshError(f"JSON file root must be an object: {path}")
    return payload


def build_phase_fingerprints(paths: dict[str, Path]) -> dict[str, str]:
    return {
        "discover": hash_payload(
            {
                "config": hash_file(paths["source_roots"]),
                "schema_version": discovery.SCHEMA_VERSION,
            }
        ),
        "normalize": hash_payload(
            {
                "config": hash_file(paths["source_roots"]),
                "schema": hash_file(paths["normalization_schema"]),
                "state_schema_version": normalization.STATE_SCHEMA_VERSION,
            }
        ),
        "segment": hash_payload(
            {
                "segmentation_schema_version": segmentation.SEGMENTATION_SCHEMA_VERSION,
                "state_schema_version": segmentation.STATE_SCHEMA_VERSION,
            }
        ),
        "classify": hash_payload(
            {
                "taxonomy": hash_file(paths["classification_taxonomy"]),
                "classification_schema_version": classification.CLASSIFICATION_SCHEMA_VERSION,
                "state_schema_version": classification.STATE_SCHEMA_VERSION,
            }
        ),
        "extract": hash_payload(
            {
                "rules": hash_file(paths["extraction_rules"]),
                "extraction_schema_version": extraction.EXTRACTION_SCHEMA_VERSION,
                "state_schema_version": extraction.STATE_SCHEMA_VERSION,
            }
        ),
        "wiki": hash_payload(
            {
                "config": hash_file(paths["wiki_config"]),
                "wiki_schema_version": wiki.WIKI_SCHEMA_VERSION,
                "state_schema_version": wiki.STATE_SCHEMA_VERSION,
            }
        ),
        "bootstrap": hash_payload(
            {
                "config": hash_file(paths["bootstrap_config"]),
                "bootstrap_schema_version": bootstrap.BOOTSTRAP_SCHEMA_VERSION,
                "state_schema_version": bootstrap.STATE_SCHEMA_VERSION,
            }
        ),
        "audit": hash_payload(
            {
                "config": hash_file(paths["audit_config"]),
                "audit_schema_version": audit.AUDIT_SCHEMA_VERSION,
                "state_schema_version": audit.STATE_SCHEMA_VERSION,
            }
        ),
    }


def resolve_phase_modes(
    *,
    previous_refresh_state: RefreshStateRecord | None,
    phase_fingerprints: dict[str, str],
    state_dir: Path,
    requested_source_ids: tuple[str, ...],
    changed_source_ids: tuple[str, ...],
) -> tuple[dict[str, str], tuple[str, ...]]:
    scoped_source_ids = requested_source_ids or changed_source_ids
    previous_phase_records = previous_refresh_state.phase_record_map if previous_refresh_state else {}

    direct_full = {
        "segment": phase_requires_full("segment", phase_fingerprints, previous_phase_records, state_dir / "segmentation_state.json")
        or phase_fingerprint_changed("normalize", phase_fingerprints, previous_phase_records),
        "classify": phase_requires_full("classify", phase_fingerprints, previous_phase_records, state_dir / "classification_state.json"),
        "extract": phase_requires_full("extract", phase_fingerprints, previous_phase_records, state_dir / "extraction_state.json"),
        "wiki": phase_requires_full("wiki", phase_fingerprints, previous_phase_records, state_dir / "wiki_state.json"),
        "bootstrap": phase_requires_full("bootstrap", phase_fingerprints, previous_phase_records, state_dir / "bootstrap_state.json"),
        "audit": phase_requires_full("audit", phase_fingerprints, previous_phase_records, state_dir / "audit_state.json"),
    }

    phase_modes: dict[str, str] = {"discover": "full", "normalize": "full"}
    force_full = False
    for phase in ("segment", "classify", "extract", "wiki", "bootstrap", "audit"):
        force_full = force_full or direct_full[phase]
        if force_full:
            phase_modes[phase] = "full"
            continue
        if scoped_source_ids:
            phase_modes[phase] = "scoped"
        else:
            phase_modes[phase] = "skipped"
    return phase_modes, scoped_source_ids


def phase_requires_full(
    phase: str,
    phase_fingerprints: dict[str, str],
    previous_phase_records: dict[str, RefreshPhaseRecord],
    required_state_path: Path,
) -> bool:
    if not required_state_path.exists():
        return True
    return phase_fingerprint_changed(phase, phase_fingerprints, previous_phase_records)


def phase_fingerprint_changed(
    phase: str,
    phase_fingerprints: dict[str, str],
    previous_phase_records: dict[str, RefreshPhaseRecord],
) -> bool:
    prior = previous_phase_records.get(phase)
    if prior is None:
        return True
    return prior.input_fingerprint != phase_fingerprints[phase]


def execute_downstream_phases(
    *,
    phase_modes: dict[str, str],
    scoped_source_ids: tuple[str, ...],
    paths: dict[str, Path],
    state_dir: Path,
    audits_dir: Path,
    normalized_dir: Path,
    segmented_dir: Path,
    classified_dir: Path,
    extracted_dir: Path,
    wiki_dir: Path,
    bootstrap_dir: Path,
    run_id: str,
    lock_path: Path,
) -> dict[str, object]:
    statuses: list[RefreshPhaseStatus] = []
    results: dict[str, object] = {}
    warning_count = 0
    error_count = 0
    last_completed_phase: str | None = None

    phase_callbacks = {
        "segment": lambda source_ids: run_segmentation(state_dir=state_dir, normalized_dir=normalized_dir, segmented_dir=segmented_dir, source_ids=source_ids),
        "classify": lambda source_ids: run_classification(
            taxonomy_path=paths["classification_taxonomy"],
            state_dir=state_dir,
            normalized_dir=normalized_dir,
            segmented_dir=segmented_dir,
            classified_dir=classified_dir,
            audits_dir=audits_dir,
            source_ids=source_ids,
            source_roots_config_path=paths["source_roots"],
        ),
        "extract": lambda source_ids: run_extraction(
            rules_path=paths["extraction_rules"],
            state_dir=state_dir,
            normalized_dir=normalized_dir,
            classified_dir=classified_dir,
            extracted_dir=extracted_dir,
            audits_dir=audits_dir,
            source_ids=source_ids,
            source_roots_config_path=paths["source_roots"],
        ),
        "wiki": lambda source_ids: run_wiki(
            config_path=paths["wiki_config"],
            state_dir=state_dir,
            extracted_dir=extracted_dir,
            wiki_dir=wiki_dir,
            audits_dir=audits_dir,
            source_ids=source_ids,
        ),
        "bootstrap": lambda source_ids: run_bootstrap(
            config_path=paths["bootstrap_config"],
            state_dir=state_dir,
            extracted_dir=extracted_dir,
            wiki_dir=wiki_dir,
            bootstrap_dir=bootstrap_dir,
            audits_dir=audits_dir,
            source_ids=source_ids,
        ),
        "audit": lambda source_ids: run_audit(
            config_path=paths["audit_config"],
            state_dir=state_dir,
            extracted_dir=extracted_dir,
            wiki_dir=wiki_dir,
            bootstrap_dir=bootstrap_dir,
            audits_dir=audits_dir,
            source_ids=source_ids,
        ),
    }

    for phase in ("segment", "classify", "extract", "wiki", "bootstrap", "audit"):
        mode = phase_modes[phase]
        heartbeat_refresh_lock(lock_path, run_id)
        if mode == "skipped":
            status = build_skipped_phase_status(phase, ())
            statuses.append(status)
            continue
        phase_source_ids = () if mode == "full" else scoped_source_ids
        status, result = execute_phase(
            phase=phase,
            scope_mode=mode,
            source_ids=phase_source_ids,
            callback=lambda callback=phase_callbacks[phase], phase_source_ids=phase_source_ids if mode == "scoped" else None: callback(phase_source_ids),
        )
        statuses.append(status)
        results[phase] = result
        if not status.success:
            raise PhaseFailure(phase, status.fatal_error_summary or f"{phase} failed")
        last_completed_phase = phase
        if phase in {"bootstrap", "audit"}:
            warning_count += extract_warning_count(result)
            error_count += extract_error_count(result)
        heartbeat_refresh_lock(lock_path, run_id)
    return {
        "phase_statuses": statuses,
        "results": results,
        "warning_count": warning_count,
        "error_count": error_count,
        "last_completed_phase": last_completed_phase,
    }


def execute_phase(
    *,
    phase: str,
    scope_mode: str,
    source_ids: tuple[str, ...],
    callback,
) -> tuple[RefreshPhaseStatus, object]:
    started_at = utc_now()
    result = callback()
    finished_at = utc_now()
    status = RefreshPhaseStatus(
        phase=phase,
        scope_mode=scope_mode,
        source_ids=source_ids,
        started_at=started_at,
        finished_at=finished_at,
        success=bool(result.report.success),
        skipped=False,
        summary=summarize_phase_result(result),
        fatal_error_summary=result.report.fatal_error_summary,
    )
    return status, result


def build_skipped_phase_status(phase: str, source_ids: tuple[str, ...]) -> RefreshPhaseStatus:
    now = utc_now()
    return RefreshPhaseStatus(
        phase=phase,
        scope_mode="skipped",
        source_ids=source_ids,
        started_at=now,
        finished_at=now,
        success=True,
        skipped=True,
        summary={},
        fatal_error_summary=None,
    )


def summarize_phase_result(result: object) -> dict[str, object]:
    report = getattr(result, "report", None)
    if report is None:
        return {}
    if isinstance(result, discovery.DiscoveryResult):
        return {
            "scanned_file_count": report.scanned_file_count,
            "status_counts": dict(report.status_counts),
        }
    if isinstance(result, normalization.NormalizationResult):
        return {
            "normalized_event_count": report.normalized_event_count,
            "source_status_counts": dict(report.source_status_counts),
        }
    if isinstance(result, segmentation.SegmentationResult):
        return {
            "segmented_source_count": report.segmented_source_count,
            "segment_count": report.segment_count,
            "source_status_counts": dict(report.source_status_counts),
        }
    if isinstance(result, classification.ClassificationResult):
        return {
            "classified_segment_count": report.classified_segment_count,
            "notice_count": report.notice_count,
            "primary_label_counts": dict(report.primary_label_counts),
        }
    if isinstance(result, extraction.ExtractionResult):
        return {
            "extracted_observation_count": report.extracted_observation_count,
            "domain_item_count": report.domain_item_count,
            "notice_count": report.notice_count,
        }
    if isinstance(result, wiki.WikiResult):
        return {
            "rendered_page_count": report.rendered_page_count,
            "synthesized_claim_count": report.synthesized_claim_count,
            "notice_count": report.notice_count,
        }
    if isinstance(result, bootstrap.BootstrapResult):
        return {
            "rendered_domain_count": report.rendered_domain_count,
            "bullet_count": report.bullet_count,
            "notice_count": report.notice_count,
        }
    if isinstance(result, audit.AuditResult):
        return {
            "finding_count": report.finding_count,
            "warning_finding_count": report.warning_finding_count,
            "error_finding_count": report.error_finding_count,
        }
    return {}


def resolve_changed_source_ids(
    before: dict[str, discovery.SourceRecord],
    after: dict[str, discovery.SourceRecord],
) -> list[str]:
    changed: list[str] = []
    steady_states = {"new", "growing", "stable"}
    for source_id in sorted(set(before) | set(after)):
        prior = before.get(source_id)
        current = after.get(source_id)
        if prior is None or current is None:
            changed.append(source_id)
            continue
        if (
            prior.status != current.status
            and (prior.status not in steady_states or current.status not in steady_states)
        ):
            changed.append(source_id)
            continue
        if prior.committed_byte_end != current.committed_byte_end:
            changed.append(source_id)
            continue
        if prior.committed_line_count != current.committed_line_count:
            changed.append(source_id)
            continue
        if prior.sampled_fingerprint.digest != current.sampled_fingerprint.digest:
            changed.append(source_id)
    return changed


def collect_touched_domains(
    *,
    state_dir: Path,
    requested_source_ids: tuple[str, ...],
    changed_source_ids: tuple[str, ...],
    full_extract: bool,
) -> tuple[str, ...]:
    extraction_state_path = state_dir / "extraction_state.json"
    if not extraction_state_path.exists():
        return ()
    extraction_state = load_extraction_state(extraction_state_path)
    if full_extract:
        return tuple(sorted({domain for record in extraction_state.values() for domain in record.touched_domains}))
    source_ids = requested_source_ids or changed_source_ids
    return tuple(
        dedupe_preserving_order(
            [domain for source_id in source_ids if source_id in extraction_state for domain in extraction_state[source_id].touched_domains]
        )
    )


def extract_warning_count(result: object) -> int:
    if isinstance(result, bootstrap.BootstrapResult):
        return int(result.report.notice_count)
    if isinstance(result, audit.AuditResult):
        return int(result.report.warning_finding_count)
    return 0


def extract_error_count(result: object) -> int:
    if isinstance(result, audit.AuditResult):
        return int(result.report.error_finding_count)
    return 0


def build_refresh_state(
    *,
    previous_state: RefreshStateRecord | None,
    config: RefreshConfig,
    phase_fingerprints: dict[str, str],
    phase_statuses: list[RefreshPhaseStatus],
    run_id: str,
    success: bool,
    last_completed_phase: str | None,
    failed_phase: str | None,
    changed_source_ids: tuple[str, ...],
    touched_domains: tuple[str, ...],
) -> RefreshStateRecord:
    previous_phase_records = previous_state.phase_record_map if previous_state else {}
    status_by_phase = {status.phase: status for status in phase_statuses}
    phase_records: list[RefreshPhaseRecord] = []
    for phase in PHASE_ORDER:
        previous_record = previous_phase_records.get(phase)
        status = status_by_phase.get(phase)
        if status is None:
            phase_records.append(
                previous_record
                or RefreshPhaseRecord(
                    phase=phase,
                    input_fingerprint=phase_fingerprints.get(phase, ""),
                    last_scope_mode="skipped",
                    last_result_status="never_ran",
                    last_successful_run_id=None,
                    last_completed_at=None,
                )
            )
            continue
        successful_run_id = previous_record.last_successful_run_id if previous_record else None
        if status.success and not status.skipped:
            successful_run_id = run_id
        phase_records.append(
            RefreshPhaseRecord(
                phase=phase,
                input_fingerprint=phase_fingerprints.get(phase, ""),
                last_scope_mode=status.scope_mode,
                last_result_status="skipped" if status.skipped else ("succeeded" if status.success else "failed"),
                last_successful_run_id=successful_run_id,
                last_completed_at=None if status.skipped else status.finished_at,
            )
        )
    return RefreshStateRecord(
        refresh_schema_version=REFRESH_SCHEMA_VERSION,
        rules_version=config.rules_version,
        last_run_id=run_id,
        last_successful_run_id=run_id if success else (previous_state.last_successful_run_id if previous_state else None),
        last_result_status="succeeded" if success else "failed",
        last_completed_phase=last_completed_phase,
        last_failed_phase=failed_phase,
        last_changed_source_ids=changed_source_ids,
        last_touched_domains=touched_domains,
        phase_records=tuple(phase_records),
    )


def persist_refresh_snapshot(
    *,
    state_path: Path,
    run_log_path: Path,
    notice_log_path: Path,
    previous_run_log_text: str,
    previous_notice_log_text: str,
    report: RefreshRunReport,
    state: RefreshStateRecord,
    notices: list[RefreshNotice],
) -> None:
    payload = {
        "schema_version": STATE_SCHEMA_VERSION,
        "generated_at": utc_now(),
        "refresh": state.to_dict(),
    }
    atomic_write_text(state_path, json.dumps(payload, indent=2, sort_keys=True) + "\n")
    atomic_write_text(run_log_path, append_jsonl_text(previous_run_log_text, report.to_dict()))
    atomic_write_text(notice_log_path, append_jsonl_text(previous_notice_log_text, [notice.to_dict() for notice in notices]))


def hash_file(path: Path) -> str:
    if not path.exists():
        raise RefreshError(f"Missing configured file: {path}")
    return hashlib.sha1(path.read_bytes()).hexdigest()


def hash_payload(payload: Any) -> str:
    return hashlib.sha1(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def parse_iso_timestamp(value: str) -> Any:
    if not value:
        return None
    normalized = value.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def dedupe_preserving_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        ordered.append(item)
    return ordered
