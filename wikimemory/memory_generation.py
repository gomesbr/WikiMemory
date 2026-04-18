from __future__ import annotations

import hashlib
import json
import re
import shutil
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from .discovery import DiscoveryError, atomic_write_text, ensure_directory, utc_now
from .memory_model import MEMORY_FILE_DEFINITIONS
from .normalization import append_jsonl_text
from .product_config import MarkdownOutputConfig, load_product_config

STATE_SCHEMA_VERSION = 1
MEMORY_SCHEMA_VERSION = 1
RECENT_MEMORY_MAX_DAYS = 30
PROJECT_RECENT_ITEM_CAP = 25
BRAIN = "\U0001f9e0"
FIRE = "\U0001f525"
GEAR = "\u2699\ufe0f"
USER_RULE_PATTERN = re.compile(r"\b(?:add this to global rules|global rule)\b", re.IGNORECASE)
GLOBAL_OPERATING_RULE_PATTERN = re.compile(
    r"\b(?:narrate your process|step commentary|short updates|response style|token limits|ask for it|outside the plan|real data|github|git|api key|always add it|do not ask|don't ask)\b",
    re.IGNORECASE,
)
DIRECTIVE_PATTERN = re.compile(r"^(?:always\b|never\b|do not\b|don't\b|must\b)", re.IGNORECASE)
PROJECT_RULE_PATTERN = re.compile(
    r"^(?:add this to project rules:?|project rule:?|for this project,?|always\b|never\b|do not\b|don't\b|must\b|nothing\b.*\bshould\b|the .{0,80}\balways\b)",
    re.IGNORECASE,
)
PROJECT_SUMMARY_PATTERN = re.compile(
    r"\b(?:project is|repo is|repository is|goal is|architecture|design decision|we decided|scope is|built to|intended to)\b",
    re.IGNORECASE,
)
LESSON_PATTERN = re.compile(r"\b(?:lesson learned|next time|avoid repeating|root cause|postmortem)\b", re.IGNORECASE)
ONE_OFF_PATTERN = re.compile(r"\b(?:please|can you|do this|fix this|run this|open this|show me|what|why|how)\b", re.IGNORECASE)
SCAFFOLD_PATTERN = re.compile(
    r"(?:please implement this plan|context from my ide setup|open tabs:|<permissions instructions>|</permissions instructions>|<collaboration_mode>|</collaboration_mode>)",
    re.IGNORECASE,
)
RUNTIME_LOCAL_PATTERN = re.compile(
    r"\b(?:restart (?:the )?(?:app|application|server|service)|hard refresh|localhost|ctrl\+f5|browser refresh)\b",
    re.IGNORECASE,
)
RECENT_NOISE_PATTERN = re.compile(
    r"(?:single prompt to codex|copy/paste|important operating style|you are helping redesign|context from my ide setup|github\.com/|what is next\??$|^pending\b|^are you\b|^recommendation\b|^push to git\b|^commit\b|api key|env file|\.env|download obsidian|can you see|test it$|sample log file|give status|full run|move storage to d|plan the change|github app|how .*space wise|loop until all is done)",
    re.IGNORECASE,
)
AGENT_DURABLE_EXCLUDED_ACTORS = {"assistant", "agent_reasoning", "tool", "unknown", "developer", "system"}


class MemoryGenerationError(DiscoveryError):
    """Fatal memory generation error."""


@dataclass(frozen=True)
class MemoryRunReport:
    run_id: str
    started_at: str
    finished_at: str
    item_counts: dict[str, int]
    rendered_file_count: int
    success: bool
    fatal_error_summary: str | None

    def to_dict(self) -> dict[str, object]:
        return {
            "run_id": self.run_id,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "item_counts": dict(sorted(self.item_counts.items())),
            "rendered_file_count": self.rendered_file_count,
            "success": self.success,
            "fatal_error_summary": self.fatal_error_summary,
        }


@dataclass(frozen=True)
class MemoryResult:
    report: MemoryRunReport
    state_path: Path
    run_log_path: Path
    notice_log_path: Path


def run_memory_generation(
    product_config_path: Path | str,
    state_dir: Path | str,
    evidence_dir: Path | str,
    memory_dir: Path | str,
    audits_dir: Path | str,
    projects: Iterable[str] | None = None,
) -> MemoryResult:
    product_config_path = Path(product_config_path)
    state_dir = Path(state_dir)
    evidence_dir = Path(evidence_dir)
    memory_dir = Path(memory_dir)
    audits_dir = Path(audits_dir)
    project_filter = {slugify(project) for project in projects or []}

    state_path = state_dir / "memory_state.json"
    run_log_path = state_dir / "memory_runs.jsonl"
    notice_log_path = audits_dir / "memory_notices.jsonl"
    run_id = f"memory-{utc_now().replace(':', '').replace('.', '').replace('-', '')}"
    started_at = utc_now()

    ensure_directory(state_dir)
    ensure_directory(audits_dir)
    ensure_directory(memory_dir)

    previous_run_log = run_log_path.read_text(encoding="utf-8") if run_log_path.exists() else ""
    previous_notice_log = notice_log_path.read_text(encoding="utf-8") if notice_log_path.exists() else ""

    try:
        config = load_product_config(product_config_path)
        evidence_records = load_evidence_records(evidence_dir)
        memory_items = build_memory_items(
            evidence_records,
            project_filter,
            require_inferred_rule_review=config.policies.require_confirmation_for_inferred_rule_promotion,
        )
        memory_items = apply_review_decisions(memory_items, state_dir)
        memory_items = prune_stale_recent_items(memory_items)
        rendered_files = render_memory_files(memory_dir, memory_items, config.markdown_output)
        write_meta(memory_dir, memory_items)

        item_counts: defaultdict[str, int] = defaultdict(int)
        for item in memory_items:
            item_counts[str(item["memory_class"])] += 1
        state_payload = {
            "schema_version": STATE_SCHEMA_VERSION,
            "memory_schema_version": MEMORY_SCHEMA_VERSION,
            "last_run_id": run_id,
            "last_rendered_at": utc_now(),
            "item_counts": dict(sorted(item_counts.items())),
            "rendered_file_count": len(rendered_files),
        }
        atomic_write_text(state_path, json.dumps(state_payload, indent=2))
        finished_at = utc_now()
        report = MemoryRunReport(
            run_id=run_id,
            started_at=started_at,
            finished_at=finished_at,
            item_counts=dict(item_counts),
            rendered_file_count=len(rendered_files),
            success=True,
            fatal_error_summary=None,
        )
        atomic_write_text(run_log_path, append_jsonl_text(previous_run_log, [report.to_dict()]))
        atomic_write_text(notice_log_path, append_jsonl_text(previous_notice_log, []))
        return MemoryResult(report, state_path, run_log_path, notice_log_path)
    except Exception as exc:
        finished_at = utc_now()
        report = MemoryRunReport(
            run_id=run_id,
            started_at=started_at,
            finished_at=finished_at,
            item_counts={},
            rendered_file_count=0,
            success=False,
            fatal_error_summary=str(exc),
        )
        atomic_write_text(run_log_path, append_jsonl_text(previous_run_log, [report.to_dict()]))
        return MemoryResult(report, state_path, run_log_path, notice_log_path)


def load_evidence_records(evidence_dir: Path) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for path in sorted((evidence_dir / "logs").glob("*.jsonl")) + sorted((evidence_dir / "projects").glob("*.jsonl")):
        records.extend(read_jsonl(path))
    return records


def build_memory_items(
    records: list[dict[str, object]],
    project_filter: set[str],
    require_inferred_rule_review: bool = True,
) -> list[dict[str, object]]:
    items: dict[str, dict[str, object]] = {}
    for record in records:
        project = slugify(str(record.get("project_hint") or record.get("source_id") or "project"))
        if project_filter and project not in project_filter:
            continue
        actor_type = str(record.get("actor_type") or "")
        text = evidence_text(record)
        if not text:
            continue
        candidates = classify_evidence(record, text, actor_type, project, require_inferred_rule_review)
        for candidate in candidates:
            if not str(candidate.get("statement") or "").strip():
                continue
            item_id = candidate["item_id"]
            if item_id not in items:
                items[item_id] = candidate
            else:
                merge_item(items[item_id], candidate)
    return sorted(items.values(), key=lambda item: (str(item["scope"]), str(item.get("project") or ""), str(item["memory_class"]), str(item["statement"])))


def classify_evidence(
    record: dict[str, object],
    text: str,
    actor_type: str,
    project: str,
    require_inferred_rule_review: bool = True,
) -> list[dict[str, object]]:
    items: list[dict[str, object]] = []
    evidence_type = str(record.get("evidence_type") or "")
    if evidence_type == "git_head":
        items.append(make_item(record, "stable_project_summary", "project", project, "durable", "repeated", text))
        return items
    if evidence_type == "git_status_item":
        items.append(make_item(record, "recent_project_state", "project", project, "recent", "candidate", text))
        return items

    if actor_type in AGENT_DURABLE_EXCLUDED_ACTORS:
        return items

    clauses = candidate_clauses(text)
    if not clauses:
        return items
    durable_found = False
    for clause in clauses:
        if is_global_rule_text(clause):
            state = promotion_state(clause)
            items.append(
                make_item(
                    record,
                    "global_user_rules",
                    "global",
                    None,
                    "durable",
                    state,
                    clause,
                    review_required=require_inferred_rule_review and state == "candidate",
                )
            )
            durable_found = True
        elif is_project_rule_text(clause):
            state = promotion_state(clause)
            items.append(
                make_item(
                    record,
                    "project_rules",
                    "project",
                    project,
                    "durable",
                    state,
                    clause,
                    review_required=require_inferred_rule_review and state == "candidate",
                )
            )
            durable_found = True
        elif LESSON_PATTERN.search(clause):
            items.append(make_item(record, "project_lessons", "project", project, "durable", "candidate", clause))
            durable_found = True
        elif is_project_summary_text(clause):
            items.append(make_item(record, "stable_project_summary", "project", project, "durable", "candidate", clause))
            durable_found = True
    if actor_type == "user" and not durable_found and is_recent_context_candidate(clauses[0]):
        items.append(make_item(record, "recent_project_state", "project", project, "recent", "candidate", clauses[0]))
    return items


def make_item(
    record: dict[str, object],
    memory_class: str,
    scope: str,
    project: str | None,
    durability: str,
    promotion_state_value: str,
    statement: str,
    review_required: bool = False,
) -> dict[str, object]:
    evidence_id = str(record["evidence_id"])
    timestamp = record.get("timestamp")
    item_id = stable_id(memory_class, scope, project or "", normalize_statement(statement))
    return {
        "item_id": item_id,
        "memory_schema_version": MEMORY_SCHEMA_VERSION,
        "memory_class": memory_class,
        "scope": scope,
        "project": project,
        "promotion_state": promotion_state_value,
        "durability": durability,
        "statement": statement,
        "source_actor_types": [str(record.get("actor_type") or "")],
        "evidence_ids": [evidence_id],
        "provenance_refs": [record.get("provenance", {})],
        "first_seen_at": timestamp,
        "last_seen_at": timestamp,
        "confidence": "explicit" if promotion_state_value == "explicit" else "candidate",
        "review_required": review_required,
        "review_reason": "inferred_rule_requires_confirmation" if review_required else None,
    }


def merge_item(target: dict[str, object], incoming: dict[str, object]) -> None:
    target["evidence_ids"] = sorted(set(target["evidence_ids"]) | set(incoming["evidence_ids"]))
    target["source_actor_types"] = sorted(set(target["source_actor_types"]) | set(incoming["source_actor_types"]))
    existing_refs = list(target.get("provenance_refs", []))
    for ref in incoming.get("provenance_refs", []):
        if ref not in existing_refs:
            existing_refs.append(ref)
    target["provenance_refs"] = existing_refs
    target["first_seen_at"] = earliest_timestamp(target.get("first_seen_at"), incoming.get("first_seen_at"))
    target["last_seen_at"] = latest_timestamp(target.get("last_seen_at"), incoming.get("last_seen_at"))
    if incoming["promotion_state"] == "explicit":
        target["promotion_state"] = "explicit"
        target["confidence"] = "explicit"
        target["review_required"] = False
        target["review_reason"] = None
    elif len(target["evidence_ids"]) > 1 and target["promotion_state"] == "candidate":
        target["promotion_state"] = "repeated"
        target["confidence"] = "strong"
    if incoming.get("review_required"):
        target["review_required"] = bool(target.get("review_required", False) or incoming.get("review_required"))


def earliest_timestamp(left: object, right: object) -> object:
    if not left:
        return right
    if not right:
        return left
    return min(str(left), str(right))


def latest_timestamp(left: object, right: object) -> object:
    if not left:
        return right
    if not right:
        return left
    return max(str(left), str(right))


def render_memory_files(memory_dir: Path, items: list[dict[str, object]], markdown_output: MarkdownOutputConfig) -> list[Path]:
    clear_generated_memory_tree(memory_dir)
    grouped: defaultdict[str, list[dict[str, object]]] = defaultdict(list)
    for item in items:
        key = memory_file_key(item)
        if key:
            grouped[key].append(item)

    rendered: list[Path] = []
    global_target = memory_dir / memory_relative_path("global_user_rules")
    render_global_rules(global_target, grouped["global_user_rules"], markdown_output)
    rendered.append(global_target)

    projects = sorted({str(item["project"]) for item in items if item.get("project")})
    for project in projects:
        for key in ("project_summary", "project_recent", "project_rules", "project_lessons"):
            definition = MEMORY_FILE_DEFINITIONS[key]
            project_items = [item for item in grouped[key] if item.get("project") == project]
            if definition.optional and not project_items:
                continue
            target = memory_dir / memory_relative_path(key, project)
            render_project_file(target, key, project, project_items, markdown_output)
            rendered.append(target)
    return rendered


def clear_generated_memory_tree(memory_dir: Path) -> None:
    for child_name in ("global", "projects", "_meta"):
        target = memory_dir / child_name
        if target.exists():
            shutil.rmtree(target)


def render_global_rules(path: Path, items: list[dict[str, object]], markdown_output: MarkdownOutputConfig) -> None:
    ensure_directory(path.parent)
    lines = frontmatter("global-rules", None, ("memory", "rules", "global"), markdown_output)
    lines.extend([f"# {BRAIN} Global User Rules", ""])
    append_rule_sections(lines, items, include_scope_notes=False)
    lines.extend(["## PROVENANCE", "", "- Derived from clear or repeated user instructions.", ""])
    atomic_write_text(path, "\n".join(lines))


def render_project_file(
    path: Path,
    key: str,
    project: str,
    items: list[dict[str, object]],
    markdown_output: MarkdownOutputConfig,
) -> None:
    ensure_directory(path.parent)
    if key == "project_summary":
        lines = render_project_summary(project, items, markdown_output)
    elif key == "project_recent":
        lines = render_project_recent(project, items, markdown_output)
    elif key == "project_rules":
        lines = render_project_rules(project, items, markdown_output)
    elif key == "project_lessons":
        lines = render_project_lessons(project, items, markdown_output)
    else:
        raise MemoryGenerationError(f"Unsupported memory file key: {key}")
    atomic_write_text(path, "\n".join(lines))


def render_project_summary(project: str, items: list[dict[str, object]], markdown_output: MarkdownOutputConfig) -> list[str]:
    title = f"{display_project(project)} - Project Memory"
    lines = frontmatter("project-memory", project, (f"project/{project}", "memory"), markdown_output)
    lines.extend([f"# {BRAIN} {title}", ""])
    purpose_items = items[:3]
    append_section(lines, "PURPOSE", item_statements(purpose_items) or ["Short project purpose not extracted yet."])
    append_section(lines, "CORE COMPONENTS", select_by_terms(items, ("component", "module", "pipeline", "adapter", "renderer", "config")) or ["No stable component list extracted yet."])
    append_section(lines, "CURRENT ARCHITECTURE", select_by_terms(items, ("architecture", "input", "process", "storage", "output", "pipeline")) or item_statements(items[3:6]) or ["No stable architecture summary extracted yet."])
    append_section(lines, "DESIGN PRINCIPLES", select_by_terms(items, ("deterministic", "traceable", "modular", "provenance", "incremental")) or ["No stable design principles extracted yet."])
    append_section(lines, "KEY CONSTRAINTS", select_by_terms(items, ("constraint", "must", "do not", "never", "only")) or ["No stable constraints extracted yet."])
    append_section(lines, "OPEN PROBLEMS", select_by_terms(items, ("open", "problem", "blocked", "pending", "todo")) or ["No open project-level problems extracted yet."])
    append_related(lines, project, markdown_output)
    return lines


def render_project_recent(project: str, items: list[dict[str, object]], markdown_output: MarkdownOutputConfig) -> list[str]:
    title = f"{display_project(project)} - Recent Context"
    ranked = sorted(items, key=lambda item: str(item.get("last_seen_at") or ""), reverse=True)[:PROJECT_RECENT_ITEM_CAP]
    used: set[str] = set()
    lines = frontmatter("recent-context", project, (f"project/{project}", "recent"), markdown_output)
    lines.extend([f"# {FIRE} {title}", ""])
    focus_items = take_unseen([item for item in ranked if "project_delta" in item.get("source_actor_types", [])], used, 3)
    append_section(lines, "CURRENT FOCUS", item_statements(focus_items, max_chars=180) or ["No current focus extracted yet."])
    decision_items = take_unseen(filter_by_terms(ranked, ("decided", "decision", "agreed", "architecture")), used, 6)
    append_section(lines, "ACTIVE DECISIONS", item_statements(decision_items, max_chars=180) or ["No active decisions extracted yet."])
    progress_items = take_unseen(filter_by_terms(ranked, ("implement", "fix", "continue", "working", "in progress", "go")), used, 8)
    append_section(lines, "IN PROGRESS", item_statements(progress_items, max_chars=180) or ["No active work items extracted yet."])
    failed_items = take_unseen(filter_by_terms(ranked, ("failed", "avoid", "did not work", "error", "broken")), used, 6)
    append_section(lines, "FAILED / AVOID", item_statements(failed_items, max_chars=180) or ["No recent failures extracted yet."])
    next_items = take_unseen(filter_by_terms(ranked, ("next", "todo", "should", "plan", "remaining")), used, 6)
    append_numbered_section(lines, "NEXT STEPS", item_statements(next_items, max_chars=180) or ["Review current project memory before starting new work."])
    backlog_items = take_unseen(ranked, used, 6)
    append_section(lines, "BACKLOG", item_statements(backlog_items, max_chars=180) or ["No backlog items extracted yet."])
    note_items = take_unseen(filter_by_terms(ranked, ("prefer", "constraint", "remember", "important")), used, 6)
    append_section(lines, "NOTES", item_statements(note_items, max_chars=180) or ["Keep this file small; it is a rolling window only."])
    lines.extend(["IMPORTANT:", "- This file must stay SMALL.", "- No history dumping.", "- Rolling window only.", ""])
    return lines


def render_project_rules(project: str, items: list[dict[str, object]], markdown_output: MarkdownOutputConfig) -> list[str]:
    title = f"{display_project(project)} - Project Rules"
    lines = frontmatter("project-rules", project, (f"project/{project}", "rules"), markdown_output)
    lines.extend([f"# {GEAR} {title}", ""])
    append_rule_sections(lines, items, include_scope_notes=True)
    append_related(lines, project, markdown_output, include_global=False)
    return lines


def render_project_lessons(project: str, items: list[dict[str, object]], markdown_output: MarkdownOutputConfig) -> list[str]:
    title = f"{display_project(project)} - Lessons Learned"
    lines = frontmatter("lessons", project, (f"project/{project}", "lessons"), markdown_output)
    lines.extend([f"# {BRAIN} {title}", ""])
    append_section(lines, "MEMORY DESIGN", select_by_terms(items, ("memory", "lesson", "next time")) or item_statements(items[:6]) or ["No high-signal memory-design lessons extracted yet."])
    append_section(lines, "SYSTEM DESIGN", select_by_terms(items, ("system", "architecture", "root cause", "postmortem")) or ["No high-signal system-design lessons extracted yet."])
    lines.extend(["ONLY INCLUDE HIGH-SIGNAL CONTENT", ""])
    return lines


def frontmatter(
    memory_type: str,
    project: str | None,
    tags: tuple[str, ...],
    markdown_output: MarkdownOutputConfig,
) -> list[str]:
    if not markdown_output.enable_frontmatter:
        return []
    lines = ["---", f"type: {memory_type}"]
    if project:
        lines.append(f"project: {project}")
    lines.append(f"updated: {utc_now()}")
    if markdown_output.enable_tags:
        lines.append("tags: [" + ", ".join(tags) + "]")
    lines.extend(["---", ""])
    return lines


def append_rule_sections(lines: list[str], items: list[dict[str, object]], include_scope_notes: bool) -> None:
    always = [item for item in items if rule_bucket(item) == "always"]
    never = [item for item in items if rule_bucket(item) == "never"]
    conditional = [item for item in items if rule_bucket(item) == "conditional"]
    explicit = [item for item in items if str(item.get("promotion_state")) == "explicit"]
    inferred = [item for item in items if str(item.get("promotion_state")) != "explicit"]
    append_section(lines, "ALWAYS DO", item_statements(always) or ["No always-do rules selected yet."])
    append_section(lines, "NEVER DO", item_statements(never) or ["No never-do rules selected yet."])
    append_section(lines, "CONDITIONAL RULES", item_statements(conditional) or ["No conditional rules selected yet."])
    header = "PROMOTED RULES (EXPLICIT)" if include_scope_notes else "CONFIRMED RULES (EXPLICIT)"
    append_section(lines, header, confirmation_summary(explicit))
    append_section(lines, "INFERRED RULES" if include_scope_notes else "INFERRED RULES (REVIEWABLE)", inferred_rule_lines(inferred))
    if include_scope_notes:
        append_section(lines, "SCOPE NOTES", ["Applies only to this project."])


def append_section(lines: list[str], title: str, bullets: list[str]) -> None:
    lines.extend([f"## {title}", ""])
    for bullet in bullets:
        lines.append(f"- {bullet}")
    lines.append("")


def append_numbered_section(lines: list[str], title: str, entries: list[str]) -> None:
    lines.extend([f"## {title}", ""])
    for index, entry in enumerate(entries, start=1):
        lines.append(f"{index}. {entry}")
    lines.append("")


def append_related(lines: list[str], project: str, markdown_output: MarkdownOutputConfig, include_global: bool = True) -> None:
    if markdown_output.enable_wikilinks:
        related = [f"[[{display_project(project)} Recent]]", f"[[{display_project(project)} Rules]]"]
        if include_global:
            related.append("[[Global User Rules]]")
    else:
        related = [f"memory/projects/{project}/recent.md", f"memory/projects/{project}/rules.md"]
        if include_global:
            related.append("memory/global/user-rules.md")
    append_section(lines, "RELATED", related)


def item_statements(items: list[dict[str, object]], max_chars: int | None = None) -> list[str]:
    return [format_item_statement(item, max_chars=max_chars) for item in items if str(item.get("statement") or "").strip()]


def format_item_statement(item: dict[str, object], max_chars: int | None = None) -> str:
    statement = str(item.get("statement") or "").strip()
    if max_chars is not None and len(statement) > max_chars:
        statement = statement[: max_chars - 3].rstrip() + "..."
    item_id = str(item.get("item_id") or "")
    return f"{statement} <!-- {item_id} -->" if item_id else statement


def inferred_rule_lines(items: list[dict[str, object]]) -> list[str]:
    if not items:
        return ["No inferred rules pending review."]
    lines = []
    for item in items:
        confidence = str(item.get("confidence") or "candidate")
        source_count = len(item.get("evidence_ids", []))
        lines.append(f"{item.get('statement')} (confidence: {confidence}; source_count: {source_count}) <!-- {item.get('item_id')} -->")
    return lines


def confirmation_summary(items: list[dict[str, object]]) -> list[str]:
    if not items:
        return ["No explicit rules selected yet."]
    return [f"{len(items)} explicit rule(s) are listed above by behavior bucket."]


def rule_bucket(item: dict[str, object]) -> str:
    text = str(item.get("statement") or "").strip().lower()
    if text.startswith(("never", "do not", "don't")):
        return "never"
    if text.startswith(("always", "must")):
        return "always"
    return "conditional"


def select_by_terms(items: list[dict[str, object]], terms: tuple[str, ...], max_chars: int | None = None) -> list[str]:
    selected = []
    for item in items:
        statement = str(item.get("statement") or "")
        lowered = statement.lower()
        if any(term in lowered for term in terms):
            selected.append(format_item_statement(item, max_chars=max_chars))
    return selected


def filter_by_terms(items: list[dict[str, object]], terms: tuple[str, ...]) -> list[dict[str, object]]:
    return [
        item
        for item in items
        if any(term in str(item.get("statement") or "").lower() for term in terms)
    ]


def take_unseen(items: list[dict[str, object]], used: set[str], limit: int) -> list[dict[str, object]]:
    selected = []
    for item in items:
        item_id = str(item.get("item_id") or "")
        if item_id in used:
            continue
        selected.append(item)
        used.add(item_id)
        if len(selected) >= limit:
            break
    return selected


def display_project(project: str) -> str:
    return " ".join(part.capitalize() for part in project.split("-"))


def write_meta(memory_dir: Path, items: list[dict[str, object]]) -> None:
    meta_dir = memory_dir / "_meta"
    ensure_directory(meta_dir)
    content = "".join(json.dumps(item, sort_keys=True, separators=(",", ":")) + "\n" for item in items)
    atomic_write_text(meta_dir / "items.jsonl", content)
    review_items = [item for item in items if item.get("review_required")]
    review_content = "".join(json.dumps(item, sort_keys=True, separators=(",", ":")) + "\n" for item in review_items)
    atomic_write_text(meta_dir / "promotion_review.jsonl", review_content)


def apply_review_decisions(items: list[dict[str, object]], state_dir: Path) -> list[dict[str, object]]:
    decisions_path = state_dir / "memory_review_decisions.json"
    if not decisions_path.exists():
        return items
    payload = json.loads(decisions_path.read_text(encoding="utf-8-sig"))
    decisions = dict(payload.get("decisions", {}))
    filtered: list[dict[str, object]] = []
    for item in items:
        item_id = str(item.get("item_id") or "")
        decision = str(decisions.get(item_id, {}).get("decision") or "")
        if decision == "rejected":
            continue
        if decision == "approved":
            item = dict(item)
            item["review_required"] = False
            item["review_reason"] = None
            item["promotion_state"] = "durable" if item.get("promotion_state") == "candidate" else item.get("promotion_state")
            item["confidence"] = "strong" if item.get("confidence") == "candidate" else item.get("confidence")
        filtered.append(item)
    return filtered


def prune_stale_recent_items(items: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        item
        for item in items
        if str(item.get("memory_class")) != "recent_project_state" or not is_older_than_days(item.get("last_seen_at"), RECENT_MEMORY_MAX_DAYS)
    ]


def is_older_than_days(value: object, days: int) -> bool:
    if not value:
        return False
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return False
    return (datetime.now(timezone.utc) - parsed.astimezone(timezone.utc)).days > days


def memory_file_key(item: dict[str, object]) -> str | None:
    memory_class = str(item["memory_class"])
    return {
        "global_user_rules": "global_user_rules",
        "project_rules": "project_rules",
        "stable_project_summary": "project_summary",
        "recent_project_state": "project_recent",
        "project_lessons": "project_lessons",
    }.get(memory_class)


def memory_relative_path(key: str, project: str | None = None) -> Path:
    rendered = MEMORY_FILE_DEFINITIONS[key].render_relative_path(project)
    path = Path(rendered)
    parts = path.parts
    if parts and parts[0] == "memory":
        return Path(*parts[1:])
    return path


def title_for_memory_file(key: str, project: str) -> str:
    titles = {
        "project_summary": f"{project} Project Memory",
        "project_recent": f"{project} Recent Context",
        "project_rules": f"{project} Project Rules",
        "project_lessons": f"{project} Lessons Learned",
    }
    return titles[key]


def evidence_text(record: dict[str, object]) -> str:
    surfaces = record.get("content_surfaces", [])
    texts = []
    if isinstance(surfaces, list):
        for surface in surfaces[:4]:
            if isinstance(surface, dict):
                text = str(surface.get("text", "")).strip()
                if text:
                    texts.append(text)
    return " ".join(texts).strip()


def candidate_clauses(text: str) -> list[str]:
    if SCAFFOLD_PATTERN.search(text) and not USER_RULE_PATTERN.search(text):
        clause = clean_clause(extract_request_text(text))
        return [clause] if is_meaningful_clause(clause) else []
    text = extract_request_text(text)
    text = re.sub(r"<image>\s*</image>|<image>|</image>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"^\s*[-*]\s+", "", text, flags=re.MULTILINE)
    raw_parts = re.split(r"(?:\r?\n|;|(?<=[.!?])\s+)", text)
    clauses: list[str] = []
    for part in raw_parts:
        clause = clean_clause(part)
        if not is_meaningful_clause(clause):
            continue
        if clause.startswith("#") or clause.lower().startswith(("open tabs", "active file")):
            continue
        clauses.append(clause)
    return clauses[:8]


def clean_clause(text: str) -> str:
    clause = text.strip(" -\t\r\n\"'`")
    clause = re.sub(r"\bstrep by step\b", "step-by-step", clause, flags=re.IGNORECASE)
    clause = re.sub(r"\bouside\b", "outside", clause, flags=re.IGNORECASE)
    clause = re.sub(r"\s+please\.?$", ".", clause, flags=re.IGNORECASE)
    return normalize_statement(clause)


def is_meaningful_clause(clause: str) -> bool:
    if not clause or len(clause) < 8:
        return False
    if clause.lower() in {"yes", "next", "go", "ok", "done", "agreed"}:
        return False
    return True


def extract_request_text(text: str) -> str:
    marker = "My request for Codex:"
    if marker in text:
        return text.split(marker)[-1].strip()
    return text.strip()


def is_global_rule_text(text: str) -> bool:
    if bool(USER_RULE_PATTERN.search(text)) and ("global rule" in text.lower() or "add this to global rules" in text.lower()):
        return True
    if len(text) > 260 or SCAFFOLD_PATTERN.search(text) or RUNTIME_LOCAL_PATTERN.search(text):
        return False
    if not DIRECTIVE_PATTERN.search(text):
        return False
    return bool(GLOBAL_OPERATING_RULE_PATTERN.search(text))


def is_project_rule_text(text: str) -> bool:
    if len(text) > 260:
        return False
    if SCAFFOLD_PATTERN.search(text) or RUNTIME_LOCAL_PATTERN.search(text):
        return False
    if ONE_OFF_PATTERN.search(text) and not re.search(r"\b(?:always|never|do not|don't|must)\b", text, re.IGNORECASE):
        return False
    return bool(PROJECT_RULE_PATTERN.search(text))


def is_project_summary_text(text: str) -> bool:
    if len(text) > 360 or SCAFFOLD_PATTERN.search(text) or ONE_OFF_PATTERN.search(text):
        return False
    return bool(PROJECT_SUMMARY_PATTERN.search(text))


def is_recent_context_candidate(text: str) -> bool:
    if len(text) > 320:
        return False
    if RECENT_NOISE_PATTERN.search(text):
        return False
    if text.lower() in {"what is next ?", "what is next?", "next", "go", "ok, continue", "continue"}:
        return False
    return True


def promotion_state(text: str) -> str:
    lowered = text.lower()
    if "add this to global rules" in lowered or "add this to project rules" in lowered:
        return "explicit"
    if DIRECTIVE_PATTERN.search(text):
        return "explicit"
    if re.search(r"\b(?:always|never|do not|don't|must)\b", text, re.IGNORECASE):
        return "durable"
    return "candidate"


def normalize_statement(text: str) -> str:
    text = " ".join(text.split())
    if len(text) > 500:
        text = text[:497].rstrip() + "..."
    return text


def stable_id(*parts: object) -> str:
    return hashlib.sha256("|".join(str(part) for part in parts).encode("utf-8")).hexdigest()[:16]


def slugify(value: str) -> str:
    slug = "".join(char.lower() if char.isalnum() else "-" for char in value).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug or "project"


def read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
