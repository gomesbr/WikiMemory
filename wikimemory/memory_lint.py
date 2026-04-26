from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .agent_bootstrap import resolve_target_path
from .discovery import DiscoveryError, atomic_write_text, ensure_directory, utc_now
from .memory_generation import render_memory_files, resolve_continuations_model, write_meta
from .memory_v2 import (
    DEFAULT_MODEL,
    PROTECTED_TOKEN_REPLACEMENTS,
    apply_protected_token_replacements,
    call_llm_json,
    dedupe_quality_operations,
    infer_project_from_statement,
    purpose_statement_is_rule,
    quality_gate_items,
    quality_operation,
    render_memory_v2,
    write_memory_v2_meta,
)
from .normalization import append_jsonl_text
from .product_config import load_product_config

STATE_SCHEMA_VERSION = 1
MEMORY_LINT_SCHEMA_VERSION = 1
STALE_RECENT_DAYS = 30
RULE_CLASSES = {"global_user_rules", "project_rules", "global_rule", "project_rule"}
GLOBAL_RULE_CLASSES = {"global_user_rules", "global_rule"}
PROJECT_RULE_CLASSES = {"project_rules", "project_rule"}
V2_ACTIVE_RECENT_CLASSES = {"current_state", "decision", "next_step", "open_question", "failure_risk", "backlog_item"}
MEMORY_LINT_MODEL = "WIKIMEMORY_MEMORY_LINT_MODEL"
MEMORY_LINT_MAX_ITEMS = 400
MEMORY_LINT_MAX_PAGES = 80
MEMORY_LINT_MAX_PAGE_CHARS = 12000


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
    llm_client=None,
    model: str | None = None,
    max_fix_rounds: int = 1,
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
            items = apply_memory_autofixes(
                run_id=run_id,
                product_config_path=product_config_path,
                memory_dir=memory_dir,
                items=items,
                candidates=candidates,
                windows=windows,
                model=model,
                llm_client=llm_client,
                max_fix_rounds=max_fix_rounds,
            )
        findings = lint_items(run_id, items)
        findings.extend(lint_memory_quality_with_llm(run_id, memory_dir, items, candidates, windows, model, llm_client))
        findings.extend(lint_bootstrap(run_id, target_path, items))
        findings.extend(lint_v2_rendered_memory(run_id, memory_dir, items))
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
            if memory_class in GLOBAL_RULE_CLASSES and project not in {"", "None", "global"}:
                findings.append(finding(run_id, "error", "scope", "global_rule_has_project", item_id, "Global rule is carrying a project value."))
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


def apply_memory_autofixes(
    *,
    run_id: str,
    product_config_path: Path,
    memory_dir: Path,
    items: list[dict[str, object]],
    candidates: list[dict[str, object]],
    windows: list[dict[str, object]],
    model: str | None,
    llm_client,
    max_fix_rounds: int,
) -> list[dict[str, object]]:
    current_items = [dict(item) for item in items]
    for _ in range(max(1, max_fix_rounds)):
        findings = lint_items(run_id, current_items)
        findings.extend(lint_memory_quality_with_llm(run_id, memory_dir, current_items, candidates, windows, model, llm_client))
        findings.extend(lint_v2_rendered_memory(run_id, memory_dir, current_items))
        operations = plan_autofix_operations(memory_dir, current_items, findings, model, llm_client)
        if not operations:
            break
        next_items = apply_fix_operations(current_items, operations)
        if serialize_items(next_items) == serialize_items(current_items):
            break
        current_items = next_items
        rerender_memory_from_items(product_config_path, memory_dir, current_items, operations)
    return current_items


def plan_autofix_operations(
    memory_dir: Path,
    items: list[dict[str, object]],
    findings: list[dict[str, object]],
    model: str | None,
    llm_client,
) -> list[dict[str, object]]:
    planned = heuristic_fix_operations(items, findings, memory_dir)
    llm_operations = lint_fix_operations_with_llm(memory_dir, items, findings, model, llm_client)
    return dedupe_fix_operations(planned + llm_operations)


def heuristic_fix_operations(
    items: list[dict[str, object]],
    findings: list[dict[str, object]],
    memory_dir: Path,
) -> list[dict[str, object]]:
    project_contexts = load_project_contexts(memory_dir)
    gated_items, quality_ops = quality_gate_items(items, project_contexts=project_contexts)
    operations = [memory_fix_operation_from_quality(op) for op in quality_ops]
    item_map = {str(item.get("item_id")): item for item in items}
    for finding_payload in findings:
        item_id = str(finding_payload.get("item_id") or finding_payload.get("scope_key") or "")
        item = item_map.get(item_id)
        if not item:
            continue
        if item.get("locked_by_consumer"):
            continue
        check_type = str(finding_payload.get("check_type") or "")
        statement = statement_value(item)
        if check_type == "known_token_typo":
            rewritten = apply_protected_token_replacements(statement)
            if rewritten != statement:
                operations.append(
                    {
                        "op": "rewrite_statement",
                        "item_id": item_id,
                        "statement": rewritten,
                        "reason": "protected_token_correction",
                    }
                )
        elif check_type in {"global_scope_leak", "global_rule_has_project"}:
            forced_project = infer_project_from_statement(statement, project_contexts)
            if forced_project:
                operations.append(
                    {
                        "op": "convert_to_project_rule",
                        "item_id": item_id,
                        "project": forced_project,
                        "reason": "project_specific_rule_removed_from_global",
                    }
                )
        elif check_type == "purpose_contains_rule":
                operations.append(
                    {
                        "op": "move_to_project_rule",
                        "item_id": item_id,
                        "reason": "purpose_rule_moved_to_rules",
                    }
                )
        elif check_type == "unknown_project_item":
            forced_project = infer_project_from_statement(statement, project_contexts)
            if forced_project:
                operations.append(
                    {
                        "op": "move_project",
                        "item_id": item_id,
                        "project": forced_project,
                        "reason": "resolved_unknown_project_from_statement",
                    }
                )
        elif check_type == "resolved_temporal_rendered":
            operations.append(
                {
                    "op": "drop_item",
                    "item_id": item_id,
                    "reason": "drop_resolved_temporal_item",
                }
            )
    for item in items:
        if item.get("locked_by_consumer"):
            continue
        if str(item.get("memory_role") or "") == "purpose" and purpose_statement_is_rule(statement_value(item)):
            operations.append(
                {
                    "op": "move_to_project_rule",
                    "item_id": str(item.get("item_id") or ""),
                    "reason": "purpose_rule_moved_to_rules",
                }
            )
    if gated_items and serialize_items(gated_items) != serialize_items(items):
        return dedupe_fix_operations(operations)
    return dedupe_fix_operations(operations)


def lint_fix_operations_with_llm(
    memory_dir: Path,
    items: list[dict[str, object]],
    findings: list[dict[str, object]],
    model: str | None,
    llm_client,
) -> list[dict[str, object]]:
    if llm_client is None:
        return []
    payload = {
        "task": "Convert memory lint findings into safe structured fix operations. Return JSON only.",
        "schema": {
            "required_top_level_key": "operations",
            "allowed_ops": [
                "rewrite_statement",
                "move_project",
                "convert_to_global_rule",
                "convert_to_project_rule",
                "move_to_project_rule",
                "drop_item",
            ],
        },
        "findings": findings[:80],
        "items": [lint_item_view(item) for item in items[:MEMORY_LINT_MAX_ITEMS]],
        "rendered_pages": rendered_page_views(memory_dir),
    }
    response = call_llm_json(memory_lint_fix_prompt(), payload, model or os.environ.get(MEMORY_LINT_MODEL, "").strip() or DEFAULT_MODEL, llm_client)
    operations = response.get("operations", [])
    if not isinstance(operations, list):
        return []
    return [normalize_fix_operation(operation) for operation in operations if isinstance(operation, dict)]


def memory_lint_fix_prompt() -> str:
    return (
        "You repair canonical memory items for an AI coding-agent memory system. "
        "Use only the allowed structured operations. "
        "Prefer minimal repairs on canonical items, not broad rewrites. "
        "Never invent projects not already implied by the evidence or rendered pages. "
        "Return only JSON matching the schema."
    )


def lint_memory_quality_with_llm(
    run_id: str,
    memory_dir: Path,
    items: list[dict[str, object]],
    candidates: list[dict[str, object]],
    windows: list[dict[str, object]],
    model: str | None,
    llm_client,
) -> list[dict[str, object]]:
    payload = {
        "task": "Review generated agent memory for quality, scope, freshness, and usefulness. Return JSON only.",
        "schema": memory_lint_review_schema(),
        "rubric": memory_lint_rubric(),
        "items": [lint_item_view(item) for item in items[:MEMORY_LINT_MAX_ITEMS]],
        "candidate_counts": candidate_counts(candidates),
        "window_counts": window_counts(windows),
        "rendered_pages": rendered_page_views(memory_dir),
    }
    response = call_llm_json(memory_lint_prompt(), payload, model or os.environ.get(MEMORY_LINT_MODEL, "").strip() or DEFAULT_MODEL, llm_client)
    raw_findings = response.get("findings", [])
    if not isinstance(raw_findings, list):
        return []
    item_ids = {str(item.get("item_id") or "") for item in items}
    return [normalize_llm_finding(run_id, raw, item_ids) for raw in raw_findings if isinstance(raw, dict)]


def candidate_counts(candidates: list[dict[str, object]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for candidate in candidates:
        project = str(candidate.get("project") or "unknown")
        memory_class = str(candidate.get("memory_class") or "unknown")
        key = f"{project}:{memory_class}"
        counts[key] = counts.get(key, 0) + 1
    return counts


def window_counts(windows: list[dict[str, object]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for window in windows:
        project = str(window.get("project") or "unknown")
        counts[project] = counts.get(project, 0) + 1
    return counts


def lint_item_view(item: dict[str, object]) -> dict[str, object]:
    return {
        "item_id": item.get("item_id"),
        "project": item.get("project"),
        "scope": item.get("scope"),
        "memory_class": item.get("memory_class"),
        "memory_role": item.get("memory_role"),
        "item_type": item.get("item_type"),
        "temporal_status": item.get("temporal_status"),
        "statement": item.get("statement") or item.get("agent_facing_statement"),
        "evidence_refs": item.get("evidence_refs") or item.get("provenance_refs") or item.get("evidence_ids"),
    }


def rendered_page_views(memory_dir: Path) -> list[dict[str, object]]:
    pages: list[dict[str, object]] = []
    for path in sorted(memory_dir.rglob("*.md")):
        if "_meta" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        pages.append({"path": str(path.relative_to(memory_dir)), "text": text[:MEMORY_LINT_MAX_PAGE_CHARS]})
        if len(pages) >= MEMORY_LINT_MAX_PAGES:
            break
    return pages


def normalize_llm_finding(run_id: str, raw: dict[str, object], item_ids: set[str]) -> dict[str, object]:
    severity = normalize_severity(raw.get("severity"))
    family = normalize_finding_token(raw.get("family"), "quality")
    check_type = normalize_finding_token(raw.get("check_type"), "llm_memory_quality")
    scope_key = str(raw.get("scope_key") or raw.get("item_id") or raw.get("page") or "memory")
    if scope_key in item_ids and raw.get("item_id") is None:
        raw = {**raw, "item_id": scope_key}
    summary = str(raw.get("summary") or "LLM memory lint finding.").strip()
    normalized = finding(run_id, severity, family, check_type, scope_key, summary)
    for key in ("item_id", "page", "line", "evidence", "recommendation"):
        value = raw.get(key)
        if value not in (None, "", []):
            normalized[key] = value
    return normalized


def normalize_severity(value: object) -> str:
    text = str(value or "warning").lower()
    return text if text in {"warning", "error"} else "warning"


def normalize_finding_token(value: object, default: str) -> str:
    text = re.sub(r"[^a-z0-9_]+", "_", str(value or default).strip().lower()).strip("_")
    return text or default


def memory_lint_prompt() -> str:
    return (
        "You are a strict memory quality reviewer for an AI coding-agent memory system. "
        "Use the supplied memory items, candidates/windows summary, and rendered pages. "
        "Find semantic problems that deterministic regex lint cannot judge well. "
        "Return only JSON matching the requested schema. Do not invent missing evidence."
    )


def memory_lint_rubric() -> list[str]:
    return [
        "Flag raw conversational comments promoted as durable memory.",
        "Flag project purpose that is actually a rule, task, runtime fact, or one-off correction.",
        "Flag global rules that are actually project-specific unless explicit global scope is present.",
        "Flag project rules or recent state under the wrong project.",
        "Flag vague statements that need hidden chat context to be useful.",
        "Flag duplicate or near-duplicate memory statements in the same scope.",
        "Flag missing coverage when substantial candidate/window evidence yields suspiciously sparse memory.",
        "Do not flag style differences, harmless wording, or intentionally compact memory.",
    ]


def memory_lint_review_schema() -> dict[str, object]:
    return {
        "required_top_level_key": "findings",
        "finding_fields": ["severity", "family", "check_type", "scope_key", "summary", "item_id", "page", "line", "evidence", "recommendation"],
        "severity_values": ["warning", "error"],
        "families": ["quality", "scope", "coverage", "freshness"],
    }


def normalize_fix_operation(raw: dict[str, object]) -> dict[str, object]:
    op = normalize_finding_token(raw.get("op"), "review_only")
    normalized = {
        "op": op,
        "item_id": str(raw.get("item_id") or ""),
        "reason": str(raw.get("reason") or "llm_autofix"),
    }
    if raw.get("project") not in (None, ""):
        normalized["project"] = str(raw.get("project"))
    if raw.get("statement") not in (None, ""):
        normalized["statement"] = str(raw.get("statement")).strip()
    return normalized


def dedupe_fix_operations(operations: list[dict[str, object]]) -> list[dict[str, object]]:
    seen: set[str] = set()
    unique: list[dict[str, object]] = []
    for operation in operations:
        fingerprint = json.dumps(operation, sort_keys=True, ensure_ascii=False)
        if fingerprint in seen:
            continue
        seen.add(fingerprint)
        unique.append(operation)
    return unique


def memory_fix_operation_from_quality(operation: dict[str, object]) -> dict[str, object]:
    action = str(operation.get("action") or "")
    item_id = str(operation.get("item_id") or "")
    reason = str(operation.get("reason") or "quality_gate")
    if action == "rewrite":
        return {"op": "rewrite_statement", "item_id": item_id, "reason": reason}
    if action == "move_project":
        return {"op": "move_project", "item_id": item_id, "project": str(operation.get("to_project") or ""), "reason": reason}
    if action == "move_scope" and str(operation.get("to_project") or "") == "global":
        return {"op": "convert_to_global_rule", "item_id": item_id, "reason": reason}
    if action == "move_scope":
        return {"op": "convert_to_project_rule", "item_id": item_id, "project": str(operation.get("to_project") or ""), "reason": reason}
    if action == "move_section":
        return {"op": "move_to_project_rule", "item_id": item_id, "reason": reason}
    return {"op": "review_only", "item_id": item_id, "reason": reason}


def apply_fix_operations(items: list[dict[str, object]], operations: list[dict[str, object]]) -> list[dict[str, object]]:
    updated = [dict(item) for item in items]
    index = {str(item.get("item_id") or ""): position for position, item in enumerate(updated)}
    dropped: set[str] = set()
    for operation in operations:
        item_id = str(operation.get("item_id") or "")
        if item_id not in index or item_id in dropped:
            continue
        item = dict(updated[index[item_id]])
        if item.get("locked_by_consumer"):
            updated[index[item_id]] = item
            continue
        op = str(operation.get("op") or "")
        if op == "rewrite_statement":
            statement = str(operation.get("statement") or "").strip() or apply_protected_token_replacements(statement_value(item))
            if statement:
                write_statement(item, statement)
        elif op == "move_project":
            project = str(operation.get("project") or "").strip()
            if project:
                item["project"] = project
                set_scope_fields(item, project=project, global_rule=False)
        elif op == "convert_to_global_rule":
            item["project"] = "global"
            set_scope_fields(item, project="global", global_rule=True)
        elif op == "convert_to_project_rule":
            project = str(operation.get("project") or item.get("project") or "").strip()
            if project and project != "global":
                item["project"] = project
                set_scope_fields(item, project=project, global_rule=False)
        elif op == "move_to_project_rule":
            project = str(item.get("project") or "").strip()
            if project and project not in {"global", "unknown"}:
                set_scope_fields(item, project=project, global_rule=False)
        elif op == "drop_item":
            dropped.add(item_id)
            continue
        updated[index[item_id]] = item
    return [item for item in updated if str(item.get("item_id") or "") not in dropped]


def set_scope_fields(item: dict[str, object], *, project: str, global_rule: bool) -> None:
    if "memory_role" in item:
        item["memory_role"] = "rule"
    if "item_type" in item:
        item["item_type"] = "global_rule" if global_rule else "project_rule"
    if "scope" in item:
        item["scope"] = "global" if global_rule else "project"
    if "memory_class" in item:
        memory_class = str(item.get("memory_class") or "")
        if memory_class in {"global_user_rules", "project_rules", "stable_project_summary"}:
            item["memory_class"] = "global_user_rules" if global_rule else "project_rules"
        elif memory_class in {"global_rule", "project_rule", "project_summary"} or item.get("memory_role") == "rule":
            item["memory_class"] = "global_rule" if global_rule else "project_rule"
    if "temporal_status" in item:
        item["temporal_status"] = "durable"
    if "durability" in item:
        item["durability"] = "durable"


def rerender_memory_from_items(product_config_path: Path, memory_dir: Path, items: list[dict[str, object]], operations: list[dict[str, object]]) -> None:
    meta_dir = memory_dir / "_meta"
    if (meta_dir / "manifest.json").exists() or any("agent_facing_statement" in item for item in items):
        project_contexts = load_project_contexts(memory_dir)
        daily_payloads = load_daily_payloads(memory_dir)
        prior_operations = load_quality_operations(memory_dir)
        render_memory_v2(memory_dir, items, project_contexts=project_contexts)
        write_memory_v2_meta(
            memory_dir,
            daily_payloads,
            items,
            project_contexts,
            dedupe_quality_operations(prior_operations + fix_operations_as_quality_operations(items, operations)),
        )
        return
    config = load_product_config(product_config_path)
    render_memory_files(
        memory_dir,
        items,
        config.markdown_output,
        continuations_model=resolve_continuations_model(config),
    )
    write_meta(memory_dir, items)


def fix_operations_as_quality_operations(items: list[dict[str, object]], operations: list[dict[str, object]]) -> list[dict[str, object]]:
    item_map = {str(item.get("item_id") or ""): item for item in items}
    quality_ops: list[dict[str, object]] = []
    for operation in operations:
        item_id = str(operation.get("item_id") or "")
        if not item_id or operation.get("op") == "review_only":
            continue
        item = item_map.get(item_id, {"item_id": item_id})
        adjusted = dict(item)
        if operation.get("op") == "rewrite_statement" and operation.get("statement"):
            adjusted["agent_facing_statement"] = operation.get("statement")
            adjusted["statement"] = operation.get("statement")
        if operation.get("op") == "move_project" and operation.get("project"):
            adjusted["project"] = operation.get("project")
        if operation.get("op") == "convert_to_global_rule":
            adjusted["project"] = "global"
            adjusted["memory_class"] = "global_rule"
            adjusted["memory_role"] = "rule"
        if operation.get("op") == "convert_to_project_rule" and operation.get("project"):
            adjusted["project"] = operation.get("project")
            adjusted["memory_class"] = "project_rule"
            adjusted["memory_role"] = "rule"
        if operation.get("op") == "move_to_project_rule":
            adjusted["memory_class"] = "project_rule"
            adjusted["memory_role"] = "rule"
        quality_ops.append(quality_operation(str(operation.get("op")), item, adjusted, str(operation.get("reason") or "memory_lint_fix")))
    return quality_ops


def load_project_contexts(memory_dir: Path) -> dict[str, dict[str, object]]:
    path = memory_dir / "_meta" / "project_contexts.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def load_daily_payloads(memory_dir: Path) -> list[dict[str, object]]:
    daily_dir = memory_dir / "_meta" / "daily"
    if not daily_dir.exists():
        return []
    payloads: list[dict[str, object]] = []
    for path in sorted(daily_dir.glob("*.json")):
        payloads.append(json.loads(path.read_text(encoding="utf-8")))
    return payloads


def load_quality_operations(memory_dir: Path) -> list[dict[str, object]]:
    path = memory_dir / "_meta" / "quality_operations.json"
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    operations = payload.get("operations", [])
    return [operation for operation in operations if isinstance(operation, dict)]


def write_statement(item: dict[str, object], statement: str) -> None:
    if "statement" in item:
        item["statement"] = statement
    if "agent_facing_statement" in item:
        item["agent_facing_statement"] = statement


def statement_value(item: dict[str, object]) -> str:
    return str(item.get("statement") or item.get("agent_facing_statement") or "")


def serialize_items(items: list[dict[str, object]]) -> str:
    return json.dumps(items, sort_keys=True, ensure_ascii=False)


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


def stable_id(*parts: object) -> str:
    return hashlib.sha256("|".join(str(part) for part in parts).encode("utf-8")).hexdigest()[:16]
