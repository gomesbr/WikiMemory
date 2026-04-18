from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .agent_bootstrap import run_agent_bootstrap
from .discovery import DiscoveryError, atomic_write_text, ensure_directory, run_discovery, utc_now
from .ingest import run_ingest
from .memory_generation import run_memory_generation
from .memory_lint import run_memory_lint
from .normalization import append_jsonl_text, run_normalization

STATE_SCHEMA_VERSION = 1
MEMORY_REFRESH_SCHEMA_VERSION = 1
PHASE_ORDER = ("discover", "normalize", "ingest", "memory", "agent-bootstrap", "memory-lint")


class MemoryRefreshError(DiscoveryError):
    """Fatal redesigned memory refresh error."""


@dataclass(frozen=True)
class MemoryRefreshPhaseStatus:
    phase: str
    started_at: str
    finished_at: str
    success: bool
    summary: dict[str, object]
    fatal_error_summary: str | None

    def to_dict(self) -> dict[str, object]:
        return {
            "phase": self.phase,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "success": self.success,
            "summary": self.summary,
            "fatal_error_summary": self.fatal_error_summary,
        }


@dataclass(frozen=True)
class MemoryRefreshRunReport:
    run_id: str
    started_at: str
    finished_at: str
    phase_statuses: tuple[MemoryRefreshPhaseStatus, ...]
    success: bool
    last_completed_phase: str | None
    failed_phase: str | None
    warning_count: int
    error_count: int
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
            "warning_count": self.warning_count,
            "error_count": self.error_count,
            "fatal_error_summary": self.fatal_error_summary,
        }


@dataclass(frozen=True)
class MemoryRefreshResult:
    report: MemoryRefreshRunReport
    state_path: Path
    run_log_path: Path


def run_memory_refresh(
    *,
    source_roots_config_path: Path | str,
    product_config_path: Path | str,
    normalization_schema_path: Path | str,
    state_dir: Path | str,
    normalized_dir: Path | str,
    evidence_dir: Path | str,
    memory_dir: Path | str,
    audits_dir: Path | str,
    bootstrap_output_path: Path | str | None = None,
    source_ids: Iterable[str] | None = None,
) -> MemoryRefreshResult:
    source_roots_config_path = Path(source_roots_config_path)
    product_config_path = Path(product_config_path)
    normalization_schema_path = Path(normalization_schema_path)
    state_dir = Path(state_dir)
    normalized_dir = Path(normalized_dir)
    evidence_dir = Path(evidence_dir)
    memory_dir = Path(memory_dir)
    audits_dir = Path(audits_dir)
    source_filter = tuple(str(source_id) for source_id in source_ids or ())

    ensure_directory(state_dir)
    ensure_directory(audits_dir)
    state_path = state_dir / "memory_refresh_state.json"
    run_log_path = state_dir / "memory_refresh_runs.jsonl"
    previous_run_log = run_log_path.read_text(encoding="utf-8") if run_log_path.exists() else ""
    run_id = f"memory-refresh-{utc_now().replace(':', '').replace('.', '').replace('-', '')}"
    started_at = utc_now()

    phase_statuses: list[MemoryRefreshPhaseStatus] = []
    last_completed_phase: str | None = None
    warning_count = 0
    error_count = 0
    failed_phase: str | None = None
    fatal_error_summary: str | None = None

    phase_callbacks = {
        "discover": lambda: run_discovery(config_path=source_roots_config_path, state_dir=state_dir),
        "normalize": lambda: run_normalization(
            config_path=source_roots_config_path,
            state_dir=state_dir,
            schema_path=normalization_schema_path,
            normalized_dir=normalized_dir,
            audits_dir=audits_dir,
        ),
        "ingest": lambda: run_ingest(
            product_config_path=product_config_path,
            state_dir=state_dir,
            normalized_dir=normalized_dir,
            evidence_dir=evidence_dir,
            audits_dir=audits_dir,
            source_ids=source_filter or None,
        ),
        "memory": lambda: run_memory_generation(
            product_config_path=product_config_path,
            state_dir=state_dir,
            evidence_dir=evidence_dir,
            memory_dir=memory_dir,
            audits_dir=audits_dir,
        ),
        "agent-bootstrap": lambda: run_agent_bootstrap(
            product_config_path=product_config_path,
            state_dir=state_dir,
            memory_dir=memory_dir,
            audits_dir=audits_dir,
            output_path=bootstrap_output_path,
        ),
        "memory-lint": lambda: run_memory_lint(
            product_config_path=product_config_path,
            state_dir=state_dir,
            memory_dir=memory_dir,
            audits_dir=audits_dir,
            bootstrap_path=bootstrap_output_path,
        ),
    }

    try:
        for phase in PHASE_ORDER:
            status, result = execute_phase(phase, phase_callbacks[phase])
            phase_statuses.append(status)
            if phase == "memory-lint":
                warning_count += int(getattr(result.report, "warning_count", 0))
                error_count += int(getattr(result.report, "error_count", 0))
            if not status.success:
                failed_phase = phase
                fatal_error_summary = status.fatal_error_summary or f"{phase} failed"
                break
            if phase == "memory-lint" and error_count > 0:
                failed_phase = phase
                fatal_error_summary = f"memory-lint produced {error_count} error finding(s)"
                break
            last_completed_phase = phase
        success = failed_phase is None
        report = MemoryRefreshRunReport(
            run_id=run_id,
            started_at=started_at,
            finished_at=utc_now(),
            phase_statuses=tuple(phase_statuses),
            success=success,
            last_completed_phase=last_completed_phase,
            failed_phase=failed_phase,
            warning_count=warning_count,
            error_count=error_count,
            fatal_error_summary=fatal_error_summary,
        )
    except Exception as exc:
        report = MemoryRefreshRunReport(
            run_id=run_id,
            started_at=started_at,
            finished_at=utc_now(),
            phase_statuses=tuple(phase_statuses),
            success=False,
            last_completed_phase=last_completed_phase,
            failed_phase=failed_phase,
            warning_count=warning_count,
            error_count=error_count,
            fatal_error_summary=str(exc),
        )

    state_payload = {
        "schema_version": STATE_SCHEMA_VERSION,
        "memory_refresh_schema_version": MEMORY_REFRESH_SCHEMA_VERSION,
        "last_run_id": run_id,
        "last_result_status": "succeeded" if report.success else "failed",
        "last_completed_phase": report.last_completed_phase,
        "last_failed_phase": report.failed_phase,
        "warning_count": report.warning_count,
        "error_count": report.error_count,
    }
    atomic_write_text(state_path, json.dumps(state_payload, indent=2, sort_keys=True) + "\n")
    atomic_write_text(run_log_path, append_jsonl_text(previous_run_log, report.to_dict()))
    return MemoryRefreshResult(report=report, state_path=state_path, run_log_path=run_log_path)


def execute_phase(phase: str, callback) -> tuple[MemoryRefreshPhaseStatus, object]:
    started_at = utc_now()
    result = callback()
    finished_at = utc_now()
    status = MemoryRefreshPhaseStatus(
        phase=phase,
        started_at=started_at,
        finished_at=finished_at,
        success=bool(result.report.success),
        summary=summarize_result(result),
        fatal_error_summary=result.report.fatal_error_summary,
    )
    return status, result


def summarize_result(result: object) -> dict[str, object]:
    report = getattr(result, "report", None)
    if report is None:
        return {}
    payload = report.to_dict()
    return {
        key: value
        for key, value in payload.items()
        if key not in {"run_id", "started_at", "finished_at", "success", "fatal_error_summary"}
    }
