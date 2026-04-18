from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .agent_bootstrap import resolve_target_path
from .discovery import DiscoveryError, atomic_write_text, ensure_directory, utc_now
from .normalization import append_jsonl_text
from .product_config import load_product_config

STATE_SCHEMA_VERSION = 1
MEMORY_LINT_SCHEMA_VERSION = 1
STALE_RECENT_DAYS = 30
RULE_CLASSES = {"global_user_rules", "project_rules"}
NOISE_PATTERN = re.compile(
    r"(?:please implement this plan|context from my ide setup|open tabs:|<permissions instructions>|<collaboration_mode>|localhost|ctrl\+f5)",
    re.IGNORECASE,
)
ONE_OFF_RULE_PATTERN = re.compile(
    r"\b(?:please|can you|fix this|run this|open this|show me|hard refresh|restart)\b",
    re.IGNORECASE,
)


class MemoryLintError(DiscoveryError):
    """Fatal memory lint error."""


@dataclass(frozen=True)
class MemoryLintRunReport:
    run_id: str
    started_at: str
    finished_at: str
    finding_count: int
    warning_count: int
    error_count: int
    success: bool
    fatal_error_summary: str | None

    def to_dict(self) -> dict[str, object]:
        return {
            "run_id": self.run_id,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "finding_count": self.finding_count,
            "warning_count": self.warning_count,
            "error_count": self.error_count,
            "success": self.success,
            "fatal_error_summary": self.fatal_error_summary,
        }


@dataclass(frozen=True)
class MemoryLintResult:
    report: MemoryLintRunReport
    findings_path: Path
    state_path: Path
    run_log_path: Path


def run_memory_lint(
    product_config_path: Path | str,
    state_dir: Path | str,
    memory_dir: Path | str,
    audits_dir: Path | str,
    bootstrap_path: Path | str | None = None,
) -> MemoryLintResult:
    product_config_path = Path(product_config_path)
    state_dir = Path(state_dir)
    memory_dir = Path(memory_dir)
    audits_dir = Path(audits_dir)
    findings_path = audits_dir / "memory_lint_findings.jsonl"
    state_path = state_dir / "memory_lint_state.json"
    run_log_path = state_dir / "memory_lint_runs.jsonl"
    run_id = f"memory-lint-{utc_now().replace(':', '').replace('.', '').replace('-', '')}"
    started_at = utc_now()

    ensure_directory(state_dir)
    ensure_directory(audits_dir)
    previous_run_log = run_log_path.read_text(encoding="utf-8") if run_log_path.exists() else ""

    try:
        config = load_product_config(product_config_path)
        target_path = resolve_target_path(
            bootstrap_path,
            config.environment.repo_root,
            config.agent_platform.bootstrap_target_path,
        )
        items = load_memory_items(memory_dir)
        findings = lint_items(run_id, items)
        findings.extend(lint_bootstrap(run_id, target_path, items))
        findings.sort(key=lambda item: str(item["finding_id"]))
        write_jsonl(findings_path, findings)

        warning_count = sum(1 for finding in findings if finding["severity"] == "warning")
        error_count = sum(1 for finding in findings if finding["severity"] == "error")
        state_payload = {
            "schema_version": STATE_SCHEMA_VERSION,
            "memory_lint_schema_version": MEMORY_LINT_SCHEMA_VERSION,
            "last_run_id": run_id,
            "last_linted_at": utc_now(),
            "finding_count": len(findings),
            "warning_count": warning_count,
            "error_count": error_count,
        }
        atomic_write_text(state_path, json.dumps(state_payload, indent=2))
        finished_at = utc_now()
        report = MemoryLintRunReport(
            run_id=run_id,
            started_at=started_at,
            finished_at=finished_at,
            finding_count=len(findings),
            warning_count=warning_count,
            error_count=error_count,
            success=True,
            fatal_error_summary=None,
        )
        atomic_write_text(run_log_path, append_jsonl_text(previous_run_log, [report.to_dict()]))
        return MemoryLintResult(report, findings_path, state_path, run_log_path)
    except Exception as exc:
        finished_at = utc_now()
        report = MemoryLintRunReport(
            run_id=run_id,
            started_at=started_at,
            finished_at=finished_at,
            finding_count=0,
            warning_count=0,
            error_count=0,
            success=False,
            fatal_error_summary=str(exc),
        )
        atomic_write_text(run_log_path, append_jsonl_text(previous_run_log, [report.to_dict()]))
        return MemoryLintResult(report, findings_path, state_path, run_log_path)


def lint_items(run_id: str, items: list[dict[str, object]]) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    stale_recent_by_project: dict[str, int] = {}
    for item in items:
        item_id = str(item.get("item_id") or "unknown")
        memory_class = str(item.get("memory_class") or "")
        statement = str(item.get("statement") or "")
        if not statement.strip():
            findings.append(finding(run_id, "error", "structure", "empty_statement", item_id, "Memory item has an empty statement."))
        if not item.get("evidence_ids") or not item.get("provenance_refs"):
            findings.append(finding(run_id, "error", "provenance", "missing_provenance", item_id, "Memory item has missing evidence or provenance refs."))
        if memory_class in RULE_CLASSES:
            if NOISE_PATTERN.search(statement):
                findings.append(finding(run_id, "error", "rule_quality", "schema_noise_rule", item_id, "Durable rule contains scaffold/runtime noise."))
            if ONE_OFF_RULE_PATTERN.search(statement):
                findings.append(finding(run_id, "warning", "rule_quality", "one_off_rule", item_id, "Durable rule may be a one-off instruction."))
            if memory_class == "global_user_rules" and item.get("project"):
                findings.append(finding(run_id, "error", "scope", "global_rule_has_project", item_id, "Global rule is carrying a project value."))
            if memory_class == "project_rules" and not item.get("project"):
                findings.append(finding(run_id, "error", "scope", "project_rule_missing_project", item_id, "Project rule is missing project scope."))
        if memory_class == "recent_project_state" and is_stale(item.get("last_seen_at")):
            project = str(item.get("project") or "unknown")
            stale_recent_by_project[project] = stale_recent_by_project.get(project, 0) + 1
    for project, count in sorted(stale_recent_by_project.items()):
        findings.append(
            finding(
                run_id,
                "warning",
                "freshness",
                "stale_recent_state",
                project,
                f"{count} recent project-state item(s) are older than the configured freshness window.",
            )
        )
    return findings


def lint_bootstrap(run_id: str, target_path: Path, items: list[dict[str, object]]) -> list[dict[str, object]]:
    if not target_path.exists():
        return [finding(run_id, "warning", "structure", "missing_agent_bootstrap", str(target_path), "Configured agent bootstrap file does not exist.")]
    content = target_path.read_text(encoding="utf-8")
    findings: list[dict[str, object]] = []
    if "memory/global/user-rules.md" not in content:
        findings.append(finding(run_id, "error", "structure", "missing_global_rules_link", str(target_path), "Agent bootstrap does not link global user rules."))
    if "Keep this bootstrap tiny" not in content:
        findings.append(finding(run_id, "warning", "structure", "missing_tiny_bootstrap_rule", str(target_path), "Agent bootstrap is missing the compactness operating rule."))
    for item in items:
        statement = str(item.get("statement") or "")
        if str(item.get("memory_class")) == "recent_project_state" and statement and statement in content:
            findings.append(finding(run_id, "warning", "structure", "recent_state_inlined", str(item.get("item_id")), "Agent bootstrap should link recent context, not inline it."))
    return findings


def is_stale(value: object) -> bool:
    if not value:
        return False
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return False
    age = datetime.now(timezone.utc) - parsed.astimezone(timezone.utc)
    return age.days > STALE_RECENT_DAYS


def finding(run_id: str, severity: str, family: str, check_type: str, scope_key: str, summary: str) -> dict[str, object]:
    finding_id = stable_id(family, check_type, scope_key, summary)
    return {
        "finding_id": finding_id,
        "run_id": run_id,
        "severity": severity,
        "family": family,
        "check_type": check_type,
        "scope_key": scope_key,
        "summary": summary,
    }


def load_memory_items(memory_dir: Path) -> list[dict[str, object]]:
    items_path = memory_dir / "_meta" / "items.jsonl"
    if not items_path.exists():
        raise MemoryLintError(f"Missing memory item manifest: {items_path}")
    return [json.loads(line) for line in items_path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    atomic_write_text(
        path,
        "".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in rows),
    )


def stable_id(*parts: object) -> str:
    return hashlib.sha256("|".join(str(part) for part in parts).encode("utf-8")).hexdigest()[:16]
