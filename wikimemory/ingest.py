from __future__ import annotations

import hashlib
import json
import subprocess
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Any

from .discovery import DiscoveryError, atomic_write_text, ensure_directory, utc_now
from .normalization import append_jsonl_text, read_json_file
from .product_config import ProductConfig, load_product_config

STATE_SCHEMA_VERSION = 1
INGEST_SCHEMA_VERSION = 1


class IngestError(DiscoveryError):
    """Fatal evidence ingest error."""


@dataclass(frozen=True)
class IngestRunReport:
    run_id: str
    started_at: str
    finished_at: str
    evidence_counts: dict[str, int]
    source_counts: dict[str, int]
    success: bool
    fatal_error_summary: str | None

    def to_dict(self) -> dict[str, object]:
        return {
            "run_id": self.run_id,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "evidence_counts": dict(sorted(self.evidence_counts.items())),
            "source_counts": dict(sorted(self.source_counts.items())),
            "success": self.success,
            "fatal_error_summary": self.fatal_error_summary,
        }


@dataclass(frozen=True)
class IngestResult:
    report: IngestRunReport
    state_path: Path
    run_log_path: Path
    notice_log_path: Path


def run_ingest(
    product_config_path: Path | str,
    state_dir: Path | str,
    normalized_dir: Path | str,
    evidence_dir: Path | str,
    audits_dir: Path | str,
    source_ids: Iterable[str] | None = None,
) -> IngestResult:
    product_config_path = Path(product_config_path)
    state_dir = Path(state_dir)
    normalized_dir = Path(normalized_dir)
    evidence_dir = Path(evidence_dir)
    audits_dir = Path(audits_dir)
    source_filter = set(source_ids or [])

    state_path = state_dir / "ingest_state.json"
    run_log_path = state_dir / "ingest_runs.jsonl"
    notice_log_path = audits_dir / "ingest_notices.jsonl"
    run_id = f"ingest-{utc_now().replace(':', '').replace('.', '').replace('-', '')}"
    started_at = utc_now()
    staging_root = evidence_dir / ".staging" / run_id

    ensure_directory(state_dir)
    ensure_directory(audits_dir)
    ensure_directory(evidence_dir)

    previous_run_log = run_log_path.read_text(encoding="utf-8") if run_log_path.exists() else ""
    previous_notice_log = notice_log_path.read_text(encoding="utf-8") if notice_log_path.exists() else ""

    try:
        config = load_product_config(product_config_path)
        ensure_directory(staging_root / "logs")
        ensure_directory(staging_root / "projects")

        records_by_path: dict[Path, list[dict[str, object]]] = {}
        notices: list[dict[str, object]] = []
        source_counts: Counter[str] = Counter()
        evidence_counts: Counter[str] = Counter()

        log_records = build_log_evidence_records(normalized_dir, source_filter)
        for relative_path, records in log_records.items():
            records_by_path[staging_root / relative_path] = records
            evidence_counts["log_event"] += len(records)
        source_counts["log_sources"] = len(log_records)

        project_records = build_project_delta_evidence_records(config, run_id, notices)
        for relative_path, records in project_records.items():
            records_by_path[staging_root / relative_path] = records
            for record in records:
                evidence_counts[str(record["evidence_type"])] += 1
        source_counts["project_sources"] = len(project_records)

        for path, records in records_by_path.items():
            write_jsonl(path, records)

        state_payload = {
            "schema_version": STATE_SCHEMA_VERSION,
            "ingest_schema_version": INGEST_SCHEMA_VERSION,
            "last_run_id": run_id,
            "last_ingested_at": utc_now(),
            "evidence_counts": dict(sorted(evidence_counts.items())),
            "source_counts": dict(sorted(source_counts.items())),
        }
        atomic_write_text(staging_root / "ingest_state.json", json.dumps(state_payload, indent=2))

        promote_staged_evidence(staging_root, evidence_dir)
        atomic_write_text(state_path, json.dumps(state_payload, indent=2))

        finished_at = utc_now()
        report = IngestRunReport(
            run_id=run_id,
            started_at=started_at,
            finished_at=finished_at,
            evidence_counts=dict(evidence_counts),
            source_counts=dict(source_counts),
            success=True,
            fatal_error_summary=None,
        )
        atomic_write_text(run_log_path, append_jsonl_text(previous_run_log, [report.to_dict()]))
        atomic_write_text(notice_log_path, append_jsonl_text(previous_notice_log, notices))
        return IngestResult(report, state_path, run_log_path, notice_log_path)
    except Exception as exc:
        finished_at = utc_now()
        report = IngestRunReport(
            run_id=run_id,
            started_at=started_at,
            finished_at=finished_at,
            evidence_counts={},
            source_counts={},
            success=False,
            fatal_error_summary=str(exc),
        )
        atomic_write_text(run_log_path, append_jsonl_text(previous_run_log, [report.to_dict()]))
        return IngestResult(report, state_path, run_log_path, notice_log_path)


def build_log_evidence_records(normalized_dir: Path, source_filter: set[str]) -> dict[Path, list[dict[str, object]]]:
    sources_dir = normalized_dir / "sources"
    if not sources_dir.exists():
        return {}

    result: dict[Path, list[dict[str, object]]] = {}
    for source_dir in sorted(path for path in sources_dir.iterdir() if path.is_dir()):
        source_id = source_dir.name
        if source_filter and source_id not in source_filter:
            continue
        events_path = source_dir / "events.jsonl"
        session_path = source_dir / "session.json"
        if not events_path.exists() or not session_path.exists():
            continue
        session = read_json_file(session_path)
        if session is None:
            continue
        project_hint = project_hint_from_session(session)
        records = []
        for event in read_jsonl(events_path):
            record = log_event_to_evidence(event, project_hint)
            if record is not None:
                records.append(record)
        result[Path("logs") / f"{source_id}.jsonl"] = records
    return result


def log_event_to_evidence(event: dict[str, object], project_hint: str | None) -> dict[str, object] | None:
    text_surfaces = [
        {
            "path": str(surface.get("path", "")),
            "text": str(surface.get("text", "")),
        }
        for surface in event.get("text_surfaces", [])
        if isinstance(surface, dict) and str(surface.get("text", "")).strip()
    ]
    if not text_surfaces:
        return None

    event_id = str(event["event_id"])
    actor_type = actor_type_for_event(event)
    return {
        "evidence_id": stable_id("log_event", event_id),
        "ingest_schema_version": INGEST_SCHEMA_VERSION,
        "evidence_type": "log_event",
        "source_adapter": "codex_jsonl",
        "source_id": str(event["source_id"]),
        "project_hint": project_hint,
        "actor_type": actor_type,
        "timestamp": event.get("timestamp"),
        "content_surfaces": text_surfaces,
        "provenance": {
            "event_id": event_id,
            "source_id": str(event["source_id"]),
            "source_line_no": int(event["source_line_no"]),
            "source_byte_start": int(event["source_byte_start"]),
            "source_byte_end": int(event["source_byte_end"]),
            "event_digest": str(event["event_digest"]),
        },
        "metadata": {
            "outer_type": event.get("outer_type"),
            "payload_type": event.get("payload_type"),
            "canonical_kind": event.get("canonical_kind"),
            "role": event.get("role"),
            "text_surface_truncated": bool(event.get("text_surface_truncated")),
        },
    }


def build_project_delta_evidence_records(
    config: ProductConfig,
    run_id: str,
    notices: list[dict[str, object]],
) -> dict[Path, list[dict[str, object]]]:
    result: dict[Path, list[dict[str, object]]] = {}
    for source in config.project_sources:
        if source.adapter != "git_worktree":
            continue
        project_root = Path(source.project_root).expanduser().resolve()
        slug = slugify(project_root.name or "project")
        if not project_root.exists():
            notices.append(
                notice(run_id, "warning", "missing_project_root", f"Project root does not exist: {project_root}")
            )
            continue
        if not (project_root / ".git").exists():
            notices.append(
                notice(run_id, "warning", "not_git_repo", f"Project root is not a git repository: {project_root}")
            )
            continue
        records = git_worktree_records(project_root, slug)
        result[Path("projects") / f"{slug}.jsonl"] = records
    return result


def git_worktree_records(project_root: Path, project_slug: str) -> list[dict[str, object]]:
    now = utc_now()
    records: list[dict[str, object]] = []
    head = run_git_optional(project_root, "rev-parse", "--verify", "HEAD") or "<unborn>"
    branch = run_git(project_root, "branch", "--show-current")
    status_lines = run_git(project_root, "status", "--porcelain=v1").splitlines()
    changed_files = run_git(project_root, "diff", "--name-only").splitlines()

    records.append(
        {
            "evidence_id": stable_id("git_head", str(project_root), head),
            "ingest_schema_version": INGEST_SCHEMA_VERSION,
            "evidence_type": "git_head",
            "source_adapter": "git_worktree",
            "source_id": project_slug,
            "project_hint": project_slug,
            "actor_type": "project_delta",
            "timestamp": now,
            "content_surfaces": [
                {
                    "path": "git.head",
                    "text": f"branch={branch or '<detached>'}; head={head}",
                }
            ],
            "provenance": {
                "project_root": str(project_root),
                "git_ref": head,
                "branch": branch,
            },
            "metadata": {"changed_file_count": len(changed_files), "status_count": len(status_lines)},
        }
    )
    for index, line in enumerate(status_lines, start=1):
        status = line[:2].strip() or "?"
        path = line[3:].strip()
        records.append(
            {
                "evidence_id": stable_id("git_status", str(project_root), line),
                "ingest_schema_version": INGEST_SCHEMA_VERSION,
                "evidence_type": "git_status_item",
                "source_adapter": "git_worktree",
                "source_id": project_slug,
                "project_hint": project_slug,
                "actor_type": "project_delta",
                "timestamp": now,
                "content_surfaces": [{"path": path, "text": f"{status} {path}"}],
                "provenance": {"project_root": str(project_root), "status_line": line, "ordinal": index},
                "metadata": {"status": status, "path": path},
            }
        )
    return records


def actor_type_for_event(event: dict[str, object]) -> str:
    role = str(event.get("role") or "")
    canonical_kind = str(event.get("canonical_kind") or "")
    payload_type = str(event.get("payload_type") or "")
    if role in {"user", "developer", "system", "assistant"}:
        return role
    if "user_message" in canonical_kind:
        return "user"
    if "agent_message" in canonical_kind or role == "assistant":
        return "assistant"
    if "reasoning" in payload_type or "reasoning" in canonical_kind:
        return "agent_reasoning"
    if "function_call" in payload_type or "tool" in canonical_kind:
        return "tool"
    return "unknown"


def project_hint_from_session(session: dict[str, object]) -> str | None:
    fields = session.get("session_meta_fields")
    if not isinstance(fields, dict):
        return None
    cwd = str(fields.get("cwd", "")).strip()
    if not cwd:
        return None
    return slugify(Path(cwd).name)


def run_git(project_root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(project_root), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def run_git_optional(project_root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(project_root), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip() if completed.returncode == 0 else ""


def read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, records: list[dict[str, object]]) -> None:
    ensure_directory(path.parent)
    path.write_text(
        "".join(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n" for record in records),
        encoding="utf-8",
    )


def promote_staged_evidence(staging_root: Path, evidence_dir: Path) -> None:
    for child_name in ("logs", "projects"):
        target = evidence_dir / child_name
        staged = staging_root / child_name
        if target.exists():
            for old_file in target.glob("*.jsonl"):
                old_file.unlink()
        ensure_directory(target)
        if staged.exists():
            for staged_file in staged.glob("*.jsonl"):
                target_file = target / staged_file.name
                target_file.write_text(staged_file.read_text(encoding="utf-8"), encoding="utf-8")


def notice(run_id: str, severity: str, notice_type: str, summary: str) -> dict[str, object]:
    return {"run_id": run_id, "severity": severity, "notice_type": notice_type, "summary": summary}


def stable_id(*parts: Any) -> str:
    digest = hashlib.sha256("|".join(str(part) for part in parts).encode("utf-8")).hexdigest()[:16]
    return digest


def slugify(value: str) -> str:
    slug = "".join(char.lower() if char.isalnum() else "-" for char in value).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug or "project"
