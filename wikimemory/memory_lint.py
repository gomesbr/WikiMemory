from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .agent_bootstrap import resolve_target_path
from .discovery import DiscoveryError, atomic_write_text, ensure_directory, utc_now
from .memory_v2 import PROTECTED_TOKEN_REPLACEMENTS, has_explicit_global_scope, infer_project_from_statement, purpose_statement_is_rule
from .normalization import append_jsonl_text
from .product_config import load_product_config

STATE_SCHEMA_VERSION = 1
MEMORY_LINT_SCHEMA_VERSION = 1
STALE_RECENT_DAYS = 30
RULE_CLASSES = {"global_user_rules", "project_rules", "global_rule", "project_rule"}
GLOBAL_RULE_CLASSES = {"global_user_rules", "global_rule"}
PROJECT_RULE_CLASSES = {"project_rules", "project_rule"}
V2_ACTIVE_RECENT_CLASSES = {"current_state", "decision", "next_step", "open_question", "failure_risk", "backlog_item"}
NOISE_PATTERN = re.compile(
    r"(?:please implement this plan|context from my ide setup|open tabs:|<permissions instructions>|<collaboration_mode>|localhost|ctrl\+f5)",
    re.IGNORECASE,
)
ONE_OFF_RULE_PATTERN = re.compile(
    r"\b(?:please|can you|fix this|run this|open this|show me|hard refresh now|restart now|stop (?:doing|asking|explaining|spitting))\b",
    re.IGNORECASE,
)
VERBATIM_LEAK_PATTERN = re.compile(r"^(?:nah|ok|okay|great|please|can you|go|agreed|correct|yes)[,.\s:!-]+", re.IGNORECASE)
AGENT_REASONING_PATTERN = re.compile(r"\b(?:i'm doing|i am doing|i'll|i will|i don't|i do not|next i'll|i’m fixing)\b", re.IGNORECASE)
RUNTIME_PURPOSE_PATTERN = re.compile(r"\b(?:localhost|https?://|\.env|BROKER_ADAPTER_MODE|ctrl\+f5|hard refresh)\b", re.IGNORECASE)
PURPOSE_RULE_PATTERN = re.compile(
    r"\b(?:make a change|developing|changing|building|implementing|do not|don't|never|always|must|should|treat .{0,80} as|compatibility|migration|version)\b",
    re.IGNORECASE,
)
VAGUE_STATEMENT_PATTERN = re.compile(
    r"\b(?:think about the system as new|this system|that system|it should|this should|do that|fix it|make it better)\b",
    re.IGNORECASE,
)
SUBJECT_ACTION_PATTERN = re.compile(
    r"\b(?:is|are|was|were|has|have|had|can|may|includes?|supports?|provides?|runs?|coordinates?|exposes?|requires?|uses?|contains?|tracks?|models?|build|generate|ingest|extract|render|lint|validate|preserve|avoid|prevent|support|treat|do not|don't|never|always|must|should|keep|use|route|classify|store|read|write|notify|provide|show|place|attach|track|resolve|improve|complete|send|perform|evolve|implement|adopt|address|monitor|verify|focuses?|maintain|prioritize|enforce|block|produced?|launched?|open|scope)\b",
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
    autofix: bool = False,
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
        candidates = load_optional_jsonl(memory_dir / "_meta" / "candidates.jsonl")
        windows = load_optional_jsonl(memory_dir / "_meta" / "extraction_windows.jsonl")
        if autofix:
            apply_safe_bootstrap_fixes(target_path)
        findings = lint_items(run_id, items)
        findings.extend(lint_memory_quality(run_id, items, candidates, windows))
        findings.extend(lint_bootstrap(run_id, target_path, items))
        findings.extend(lint_v2_rendered_memory(run_id, memory_dir, items))
        findings.extend(lint_page_quality_review(run_id, memory_dir))
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
        statement = str(item.get("statement") or item.get("agent_facing_statement") or "")
        project = str(item.get("project") or ("global" if memory_class in GLOBAL_RULE_CLASSES else "unknown"))
        if not statement.strip():
            findings.append(finding(run_id, "error", "structure", "empty_statement", item_id, "Memory item has an empty statement."))
        has_evidence = bool(item.get("evidence_ids") or item.get("evidence_refs"))
        has_provenance = bool(item.get("provenance_refs") or item.get("evidence_refs"))
        if not has_evidence or not has_provenance:
            findings.append(finding(run_id, "error", "provenance", "missing_provenance", item_id, "Memory item has missing evidence or provenance refs."))
        if memory_class in RULE_CLASSES:
            if NOISE_PATTERN.search(statement):
                findings.append(finding(run_id, "error", "rule_quality", "schema_noise_rule", item_id, "Durable rule contains scaffold/runtime noise."))
            if ONE_OFF_RULE_PATTERN.search(statement):
                findings.append(finding(run_id, "warning", "rule_quality", "one_off_rule", item_id, "Durable rule may be a one-off instruction."))
            if memory_class in GLOBAL_RULE_CLASSES and project not in {"", "None", "global"}:
                findings.append(finding(run_id, "error", "scope", "global_rule_has_project", item_id, "Global rule is carrying a project value."))
            if memory_class in GLOBAL_RULE_CLASSES:
                forced_project = infer_project_from_statement(statement)
                if forced_project and not has_explicit_global_scope(statement):
                    findings.append(finding(run_id, "error", "scope", "global_scope_leak", item_id, "Global rule appears to contain project-specific guidance."))
            if memory_class in PROJECT_RULE_CLASSES and project in {"", "None", "unknown"}:
                findings.append(finding(run_id, "error", "scope", "project_rule_missing_project", item_id, "Project rule is missing project scope."))
        if project == "unknown" and memory_class not in GLOBAL_RULE_CLASSES:
            findings.append(finding(run_id, "error", "scope", "unknown_project_item", item_id, "Memory item has unresolved project scope."))
        if any(wrong.lower() in statement.lower() for wrong in PROTECTED_TOKEN_REPLACEMENTS):
            findings.append(finding(run_id, "error", "quality", "known_token_typo", item_id, "Memory item contains a suspicious mutation of a protected token."))
        if memory_class == "recent_project_state" and is_stale(item.get("last_seen_at")):
            stale_recent_by_project[project] = stale_recent_by_project.get(project, 0) + 1
        if memory_class == "recent_project_state" and str(item.get("temporal_status") or "active") != "active":
            findings.append(finding(run_id, "error", "freshness", "resolved_temporal_rendered", item_id, "Resolved or superseded temporal memory is still in rendered memory items."))
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


def lint_memory_quality(
    run_id: str,
    items: list[dict[str, object]],
    candidates: list[dict[str, object]],
    windows: list[dict[str, object]],
) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    seen: dict[tuple[str, str, str], str] = {}
    project_item_counts: dict[str, int] = {}
    project_window_counts: dict[str, int] = {}
    project_rule_candidate_counts: dict[str, int] = {}
    project_rule_item_counts: dict[str, int] = {}

    for window in windows:
        project = str(window.get("project") or "unknown")
        project_window_counts[project] = project_window_counts.get(project, 0) + 1
    for candidate in candidates:
        if str(candidate.get("memory_class")) == "project_rules":
            project = str(candidate.get("project") or "unknown")
            project_rule_candidate_counts[project] = project_rule_candidate_counts.get(project, 0) + 1

    for item in items:
        item_id = str(item.get("item_id") or "unknown")
        statement = str(item.get("agent_facing_statement") or item.get("statement") or "")
        project = str(item.get("project") or "global")
        memory_class = str(item.get("memory_class") or "")
        project_item_counts[project] = project_item_counts.get(project, 0) + 1
        if memory_class == "project_rules":
            project_rule_item_counts[project] = project_rule_item_counts.get(project, 0) + 1
        if VERBATIM_LEAK_PATTERN.search(statement) or "got even more complicated" in statement.lower():
            findings.append(finding(run_id, "warning", "quality", "verbatim_user_comment", item_id, "Memory statement appears to leak a raw user comment instead of agent-facing guidance."))
        if AGENT_REASONING_PATTERN.search(statement):
            findings.append(finding(run_id, "error", "quality", "agent_reasoning_memory", item_id, "Memory statement appears to contain agent reasoning or progress narration."))
        if memory_class == "stable_project_summary" and str(item.get("item_type") or "") in {"project_summary", "purpose"} and RUNTIME_PURPOSE_PATTERN.search(statement):
            findings.append(finding(run_id, "warning", "quality", "runtime_fact_in_project_purpose", item_id, "Project purpose contains runtime/config details that should be routed to constraints or recent context."))
        role = str(item.get("memory_role") or "")
        if (
            (memory_class == "stable_project_summary" and str(item.get("item_type") or "") in {"project_summary", "purpose"})
            or (memory_class == "project_summary" and role == "purpose")
        ) and (PURPOSE_RULE_PATTERN.search(statement) or purpose_statement_is_rule(statement)):
            findings.append(finding(run_id, "error", "quality", "purpose_contains_rule", item_id, "Project purpose contains behavior guidance that belongs in project rules."))
        if memory_class in {"stable_project_summary", "project_summary"} and role == "rule":
            findings.append(finding(run_id, "error", "quality", "section_mismatch", item_id, "Rule-role item is still classified as project summary."))
        if VAGUE_STATEMENT_PATTERN.search(statement):
            findings.append(finding(run_id, "warning", "quality", "vague_memory_statement", item_id, "Memory statement needs hidden conversation context to be useful."))
        if len(statement.split()) >= 4 and not SUBJECT_ACTION_PATTERN.search(statement):
            findings.append(finding(run_id, "warning", "quality", "missing_subject_or_action", item_id, "Memory statement may lack a clear actionable subject or behavior."))
        duplicate_key = (project, memory_class, normalize_statement(statement))
        prior = seen.get(duplicate_key)
        if prior and prior != item_id:
            findings.append(finding(run_id, "warning", "quality", "duplicate_memory_statement", item_id, "Duplicate memory statement appears in the same scope and class."))
        seen[duplicate_key] = item_id

    for project, window_count in sorted(project_window_counts.items()):
        if project == "global":
            continue
        item_count = project_item_counts.get(project, 0)
        if window_count >= 5 and item_count <= 2:
            findings.append(finding(run_id, "warning", "coverage", "shallow_project_memory", project, "Project has substantial evidence windows but very few memory items."))
    for project, candidate_count in sorted(project_rule_candidate_counts.items()):
        if candidate_count >= 2 and project_rule_item_counts.get(project, 0) == 0:
            findings.append(finding(run_id, "warning", "coverage", "rules_page_suspiciously_empty", project, "Project has rule candidates but no rendered project rules."))
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
        if str(item.get("memory_class")) == "recent_project_state" and len(statement) >= 12 and statement in content:
            findings.append(finding(run_id, "warning", "structure", "recent_state_inlined", str(item.get("item_id")), "Agent bootstrap should link recent context, not inline it."))
    return findings


def lint_v2_rendered_memory(run_id: str, memory_dir: Path, items: list[dict[str, object]]) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    latest_active_by_project: dict[str, str] = {}
    for item in items:
        project = str(item.get("project") or "")
        if project in {"", "global", "unknown"}:
            continue
        if str(item.get("memory_class")) not in V2_ACTIVE_RECENT_CLASSES or str(item.get("temporal_status") or "active") != "active":
            continue
        latest = latest_source_day(item)
        if latest and latest > latest_active_by_project.get(project, ""):
            latest_active_by_project[project] = latest

    for project, latest_day in sorted(latest_active_by_project.items()):
        recent_path = memory_dir / "projects" / project / "recent.md"
        if not recent_path.exists():
            findings.append(finding(run_id, "error", "freshness", "recent_missing_latest_work", project, "Project has active recent evidence but no recent.md page."))
            continue
        title = next((line.strip() for line in recent_path.read_text(encoding="utf-8").splitlines() if line.startswith("# ")), "")
        expected = display_date(latest_day)
        if expected and expected not in title:
            findings.append(finding(run_id, "error", "freshness", "recent_date_mismatch", project, f"Recent page title does not reflect latest active evidence date {latest_day}."))
    return findings


def lint_page_quality_review(run_id: str, memory_dir: Path) -> list[dict[str, object]]:
    path = memory_dir / "_meta" / "page_quality_review.json"
    if not path.exists():
        return [finding(run_id, "error", "quality", "missing_page_quality_review", str(path), "Fresh-agent page quality review was not generated.")]
    payload = json.loads(path.read_text(encoding="utf-8"))
    findings: list[dict[str, object]] = []
    for line in payload.get("lines", []):
        if not isinstance(line, dict) or line.get("status") != "bad":
            continue
        scope = f"{line.get('page')}:{line.get('line_number')}"
        findings.append(
            finding(
                run_id,
                "error",
                "quality",
                "bad_fresh_agent_line",
                scope,
                f"Rendered memory line failed fresh-agent rubric: {line.get('reason')}",
            )
        )
    return findings


def latest_source_day(item: dict[str, object]) -> str:
    days = [
        str(ref.get("source_day") or "")
        for ref in item.get("evidence_refs", [])
        if isinstance(ref, dict) and re.match(r"^\d{4}-\d{2}-\d{2}$", str(ref.get("source_day") or ""))
    ]
    return max(days) if days else ""


def display_date(day: str) -> str:
    try:
        parsed = datetime.fromisoformat(day)
    except ValueError:
        return day
    return parsed.strftime("%B %d %Y")


def apply_safe_bootstrap_fixes(target_path: Path) -> None:
    if not target_path.exists():
        return
    content = target_path.read_text(encoding="utf-8")
    additions: list[str] = []
    if "memory/global/user-rules.md" not in content:
        additions.extend(["", "## Memory Entry Points", "", "- `memory/global/user-rules.md` for durable user-wide rules."])
    if "Keep this bootstrap tiny" not in content:
        additions.extend(["", "## Operating Rule", "", "- Keep this bootstrap tiny. Load referenced memory files when the task needs detail."])
    if additions:
        atomic_write_text(target_path, content.rstrip() + "\n" + "\n".join(additions) + "\n")


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
    if items_path.exists():
        return [json.loads(line) for line in items_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    merged_path = memory_dir / "_meta" / "merged_items.json"
    if merged_path.exists():
        payload = json.loads(merged_path.read_text(encoding="utf-8"))
        items = payload.get("items", [])
        if isinstance(items, list):
            return [item for item in items if isinstance(item, dict)]
    raise MemoryLintError(f"Missing memory item manifest: {items_path}")


def load_optional_jsonl(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    atomic_write_text(
        path,
        "".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in rows),
    )


def normalize_statement(text: str) -> str:
    return " ".join(text.lower().split())


def stable_id(*parts: object) -> str:
    return hashlib.sha256("|".join(str(part) for part in parts).encode("utf-8")).hexdigest()[:16]
