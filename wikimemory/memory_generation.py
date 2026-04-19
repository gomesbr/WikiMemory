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
from .memory_extraction import extract_memory_artifacts
from .memory_model import MEMORY_FILE_DEFINITIONS
from .normalization import append_jsonl_text
from .product_config import MarkdownOutputConfig, load_product_config

STATE_SCHEMA_VERSION = 1
MEMORY_SCHEMA_VERSION = 1
RECENT_MEMORY_MAX_DAYS = 30
PROJECT_RECENT_ITEM_CAP = 25
RULE_BUCKET_CAP = 12
INFERRED_RULE_CAP = 6
BRAIN = "\U0001f9e0"
FIRE = "\U0001f525"
GEAR = "\u2699\ufe0f"
RENDER_PREFIX_PATTERN = re.compile(
    r"^(?:Follow this operating rule|Project context|Use this architecture context|Respect this constraint|Current context|Continue with|Track this unresolved question|Carry forward this lesson):\s*",
    re.IGNORECASE,
)
RENDER_REJECT_PATTERN = re.compile(
    r"(?:\.\.\.|iMPLEMENT THIS PLAN|IMPLEMENT THIS PLAN|PLEASE IMPLEMENT THIS PLAN|<environment_context>|open tabs:|context from my ide setup|single prompt to codex|copy/paste|source_count:|confidence:|^No .* extracted yet\.?$|^No .* selected yet\.?$|^No .* items extracted yet\.?$|^No .* rules selected yet\.?$)",
    re.IGNORECASE,
)
RAW_FIRST_PERSON_PATTERN = re.compile(
    r"\b(?:i think|i keep|i close|i reopen|i don't|i do not|i'll|i will|i need|i'm|i am|my question|my inputs)\b",
    re.IGNORECASE,
)
TRANSIENT_RENDER_PATTERN = re.compile(
    r"\b(?:what should you focus|what is next|phase \d+ should be treated as a checkpoint|full-load run|commit and merge|push to git|download obsidian|api key|env file|D drive|unclassified count|notices?:\s*\d+|current phase is complete)\b",
    re.IGNORECASE,
)
USER_RULE_PATTERN = re.compile(r"\b(?:add this to global rules|global rule)\b", re.IGNORECASE)
GLOBAL_OPERATING_RULE_PATTERN = re.compile(
    r"\b(?:narrate your process|step commentary|short updates|response style|token limits|explanations?|explanation texts|wasting tokens|concise|ask for it|outside the plan|real data|github|git|api key|always add it|do not ask|don't ask)\b",
    re.IGNORECASE,
)
DIRECTIVE_PATTERN = re.compile(r"^(?:always\b|never\b|do not\b|don't\b|must\b|stop\b)", re.IGNORECASE)
PROJECT_RULE_PATTERN = re.compile(
    r"^(?:add this to project rules:?|project rule:?|for this project,?|always\b|never\b|do not\b|don't\b|must\b|no\b.{0,80}\bshould\b|nothing\b.*\bshould\b|the .{0,80}\balways\b)",
    re.IGNORECASE,
)
PROJECT_SUMMARY_PATTERN = re.compile(
    r"^(?:the\s+)?(?:project|repo|repository)\s+is\b|^(?:goal|purpose|scope)\s+is\b|^(?:we\s+decided|design\s+decision|architecture:|built\s+to|intended\s+to)\b",
    re.IGNORECASE,
)
CONVERSATIONAL_SUMMARY_PREFIX_PATTERN = re.compile(
    r"^(?:nah\b|no[,.\s]|wait\b|ok[,.\s]|yes[,.\s]|agreed\b|correct\b|great\b|this\b|please\b|can you\b)",
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
    r"(?:single prompt to codex|copy/paste|important operating style|you are helping redesign|context from my ide setup|github\.com/|what is next\??|whats next\??|what should you focus|good enough to go to next phase|^pending\b|^are you\b|^recommendation\b|^push to git\b|^commit\b|commit and merge|api key|env file|\.env|download obsidian|can you see|test it$|sample log file|give status|full run|full load|move storage to d|plan the change|github app|github app|inside cursor|how do i run this|how .*space wise|loop until all is done|where .* located\??$|create the plan$|^ok,? create the plan$|\bplan (?:it|phase|next phase)\b|^next$|^go$|^continue$|^correct\.? fix it$|^done,? check$|^in node\.?js$|installed,? variables|send me a text msg|go and do a full .*analysis|read .* and tell me|implements? all remaining steps|should have a llm second pass|readme file with more details|notices?:\s*\d+|stop wasting tokens|do the work,? don'?t explain)",
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
        extraction_artifacts = extract_memory_artifacts(
            evidence_records,
            config=config,
            project_filter=project_filter,
            require_inferred_rule_review=config.policies.require_confirmation_for_inferred_rule_promotion,
            unresolved_project=config.project_routing.unresolved_project,
            run_id=run_id,
        )
        memory_items = extraction_artifacts.items
        memory_items = apply_review_decisions(memory_items, state_dir)
        memory_items = prune_stale_recent_items(memory_items)
        rendered_files = render_memory_files(memory_dir, memory_items, config.markdown_output)
        write_meta(memory_dir, memory_items, extraction_artifacts.windows, extraction_artifacts.candidates)

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
            "extraction_window_count": len(extraction_artifacts.windows),
            "extraction_candidate_count": len(extraction_artifacts.candidates),
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
        atomic_write_text(notice_log_path, append_jsonl_text(previous_notice_log, extraction_artifacts.notices))
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
    unresolved_project: str = "projects",
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
            if candidate.get("scope") == "project" and project == slugify(unresolved_project):
                continue
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
    if evidence_type == "project_overview_file":
        for clause in project_overview_clauses(text):
            items.append(make_item(record, "stable_project_summary", "project", project, "durable", "explicit", clause))
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
    incoming_fingerprints = evidence_fingerprints(incoming)
    target_fingerprints = set(evidence_fingerprints(target))
    duplicate_same_message = bool(incoming_fingerprints & target_fingerprints)
    if not duplicate_same_message:
        target["evidence_ids"] = sorted(set(target["evidence_ids"]) | set(incoming["evidence_ids"]))
    target["source_actor_types"] = sorted(set(target["source_actor_types"]) | set(incoming["source_actor_types"]))
    existing_refs = list(target.get("provenance_refs", []))
    for ref in incoming.get("provenance_refs", []):
        if ref not in existing_refs and not duplicate_same_message:
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


def evidence_fingerprints(item: dict[str, object]) -> set[str]:
    statement = normalize_statement(str(item.get("statement") or "")).lower()
    fingerprints: set[str] = set()
    for ref in item.get("provenance_refs", []):
        if not isinstance(ref, dict):
            continue
        fingerprints.add(
            "|".join(
                [
                    str(ref.get("source_id") or ""),
                    evidence_time_bucket(item.get("last_seen_at") or item.get("first_seen_at") or ""),
                    statement,
                ]
            )
        )
    return fingerprints


def evidence_time_bucket(value: object) -> str:
    text = str(value or "")
    return text.split(".", 1)[0]


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
    stable_items = sorted(
        [item for item in items if not is_git_head_statement(str(item.get("statement") or ""))],
        key=project_summary_rank,
    )
    descriptive_items = [item for item in stable_items if not is_config_instruction_statement(str(item.get("statement") or ""))]
    lines = frontmatter("project-memory", project, (f"project/{project}", "memory"), markdown_output)
    lines.extend([f"# {BRAIN} {title}", ""])
    used: set[str] = set()
    purpose_items = take_unseen(
        [
            item
            for item in descriptive_items
            if str(item.get("item_type")) in {"purpose", "project_summary"}
            or (str(item.get("item_type") or "") not in {"constraint", "architecture", "decision"} and project_summary_rank(item)[0] <= 2)
        ],
        used,
        3,
    )
    append_section(lines, "PURPOSE", item_statements(purpose_items) or ["Short project purpose not extracted yet."])
    append_section(lines, "CORE COMPONENTS", item_statements(take_unseen(filter_by_terms(descriptive_items, ("component", "module", "pipeline", "adapter", "renderer", "service", "engine")), used, 6)) or ["No stable component list extracted yet."])
    append_section(lines, "CURRENT ARCHITECTURE", item_statements(take_unseen([item for item in descriptive_items if str(item.get("item_type")) == "architecture"] + filter_by_terms(descriptive_items, ("architecture", "input", "process", "storage", "output", "pipeline", "service", "engine")), used, 6)) or ["No stable architecture summary extracted yet."])
    append_section(lines, "DESIGN PRINCIPLES", item_statements(take_unseen(filter_by_terms(descriptive_items, ("deterministic", "traceable", "modular", "provenance", "incremental")), used, 6)) or ["No stable design principles extracted yet."])
    append_section(lines, "KEY CONSTRAINTS", item_statements(take_unseen([item for item in stable_items if str(item.get("item_type")) == "constraint"] + filter_by_terms(stable_items, ("constraint", "must", "do not", "never", "only", "blocks", "disabled", "strict", "kill switch")), used, 6)) or ["No stable constraints extracted yet."])
    append_section(lines, "OPEN PROBLEMS", item_statements(take_unseen(filter_by_terms(descriptive_items, ("open", "problem", "blocked", "pending", "todo")), used, 5)) or ["No open project-level problems extracted yet."])
    append_related(lines, project, markdown_output)
    return lines


def render_project_recent(project: str, items: list[dict[str, object]], markdown_output: MarkdownOutputConfig) -> list[str]:
    title = f"{display_project(project)} - Recent Context"
    active_items = [item for item in items if str(item.get("item_type") or "") != "open_question"]
    ranked = sorted(active_items, key=lambda item: str(item.get("last_seen_at") or ""), reverse=True)[:PROJECT_RECENT_ITEM_CAP]
    used: set[str] = set()
    lines = frontmatter("recent-context", project, (f"project/{project}", "recent"), markdown_output)
    lines.extend([f"# {FIRE} {title}", ""])
    focus_items = take_unseen([item for item in ranked if str(item.get("item_type")) == "current_state"], used, 4)
    append_section(lines, "CURRENT FOCUS", item_statements(focus_items, max_chars=180) or ["No current focus extracted yet."])
    decision_items = take_unseen([item for item in ranked if str(item.get("item_type")) == "decision"] + filter_by_terms(ranked, ("decided", "decision", "agreed", "architecture")), used, 6)
    append_section(lines, "ACTIVE DECISIONS", item_statements(decision_items, max_chars=180) or ["No active decisions extracted yet."])
    progress_items = take_unseen([item for item in ranked if str(item.get("item_type")) == "task"] + filter_by_terms(ranked, ("implement", "fix", "continue", "working", "in progress")), used, 8)
    append_section(lines, "IN PROGRESS", item_statements(progress_items, max_chars=180) or ["No active work items extracted yet."])
    failed_items = take_unseen([item for item in ranked if str(item.get("item_type")) == "failure_risk"] + filter_by_terms(ranked, ("failed", "avoid", "did not work", "error", "broken")), used, 6)
    append_section(lines, "FAILED / AVOID", item_statements(failed_items, max_chars=180) or ["No recent failures extracted yet."])
    next_items = take_unseen([item for item in ranked if str(item.get("item_type")) == "next_step"] + filter_by_terms(ranked, ("next", "todo", "should", "plan", "remaining")), used, 6)
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
    eligible = dedupe_render_items([item for item in items if is_renderable_item(item)])
    always = [item for item in eligible if rule_bucket(item) == "always"][:RULE_BUCKET_CAP]
    never = [item for item in eligible if rule_bucket(item) == "never"][:RULE_BUCKET_CAP]
    conditional = [item for item in eligible if rule_bucket(item) == "conditional"][:RULE_BUCKET_CAP]
    explicit = [item for item in eligible if str(item.get("promotion_state")) == "explicit"]
    inferred = [item for item in eligible if str(item.get("promotion_state")) != "explicit"][:INFERRED_RULE_CAP]
    append_section(lines, "ALWAYS DO", item_statements(always))
    append_section(lines, "NEVER DO", item_statements(never))
    append_section(lines, "CONDITIONAL RULES", item_statements(conditional))
    header = "PROMOTED RULES (EXPLICIT)" if include_scope_notes else "CONFIRMED RULES (EXPLICIT)"
    append_section(lines, header, confirmation_summary(explicit))
    append_section(lines, "INFERRED RULES" if include_scope_notes else "INFERRED RULES (REVIEWABLE)", inferred_rule_lines(inferred))
    if include_scope_notes:
        append_section(lines, "SCOPE NOTES", ["Applies only to this project."])


def append_section(lines: list[str], title: str, bullets: list[str]) -> None:
    lines.extend([f"## {title}", ""])
    clean_bullets = [bullet for bullet in bullets if is_renderable_text(bullet)]
    if not clean_bullets:
        lines.extend(["_None currently extracted._", ""])
        return
    for bullet in clean_bullets:
        lines.append(f"- {bullet}")
    lines.append("")


def append_numbered_section(lines: list[str], title: str, entries: list[str]) -> None:
    lines.extend([f"## {title}", ""])
    clean_entries = [entry for entry in entries if is_renderable_text(entry)]
    if not clean_entries:
        lines.extend(["_None currently extracted._", ""])
        return
    for index, entry in enumerate(clean_entries, start=1):
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
    statements = [format_item_statement(item, max_chars=max_chars) for item in items if is_renderable_item(item)]
    return [statement for statement in statements if is_renderable_text(statement)]


def format_item_statement(item: dict[str, object], max_chars: int | None = None) -> str:
    statement = str(item.get("agent_facing_statement") or item.get("statement") or "").strip()
    statement = clean_render_statement(statement)
    if max_chars is not None and len(statement) > max_chars:
        return ""
    return statement


def inferred_rule_lines(items: list[dict[str, object]]) -> list[str]:
    if not items:
        return []
    lines = []
    for item in items:
        if not is_renderable_item(item):
            continue
        statement = clean_render_statement(str(item.get("agent_facing_statement") or item.get("statement") or ""))
        if not is_renderable_text(statement):
            continue
        confidence = str(item.get("confidence") or "candidate")
        source_count = len(item.get("evidence_ids", []))
        lines.append(f"{statement} (confidence: {confidence}; sources: {source_count})")
    return lines


def confirmation_summary(items: list[dict[str, object]]) -> list[str]:
    if not items:
        return []
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
            rendered = format_item_statement(item, max_chars=max_chars)
            if is_renderable_text(rendered):
                selected.append(rendered)
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
        if not is_renderable_item(item):
            continue
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


def dedupe_render_items(items: list[dict[str, object]]) -> list[dict[str, object]]:
    seen: set[str] = set()
    selected: list[dict[str, object]] = []
    for item in sorted(items, key=render_rank):
        statement = clean_render_statement(str(item.get("agent_facing_statement") or item.get("statement") or ""))
        key = normalize_render_key(statement)
        if not key or key in seen:
            continue
        seen.add(key)
        selected.append(item)
    return selected


def render_rank(item: dict[str, object]) -> tuple[int, int, str]:
    confidence = {"explicit": 0, "strong": 1, "medium": 2, "low": 3, "candidate": 4}.get(str(item.get("confidence") or ""), 4)
    support = -len(item.get("evidence_ids", []))
    return (confidence, support, str(item.get("last_seen_at") or ""))


def clean_render_statement(statement: str) -> str:
    statement = RENDER_PREFIX_PATTERN.sub("", " ".join(statement.split())).strip()
    replacements = {
        "idependent": "independent",
        "post there": "posted there",
        "compatubility": "compatibility",
        "beuiding": "building",
        "videa": "video",
        "iddile": "idle",
        "iddle": "idle",
        "tha...": "that",
    }
    for bad, good in replacements.items():
        statement = re.sub(re.escape(bad), good, statement, flags=re.IGNORECASE)
    if statement.lower().startswith("the user wants "):
        statement = "Prioritize " + statement[15:]
    if statement.lower().startswith("the user expects "):
        statement = "Expect " + statement[17:]
    if "repository to be visible" in statement.lower() and "repository" in statement.lower():
        statement = "Keep the repository visible under the user's remote repository namespace."
    if "support notifications" in statement.lower() and "important events" in statement.lower():
        statement = "Notify the user about notable pipeline events so maintenance work happens at appropriate times."
    statement = rewrite_phase_references(statement)
    statement = re.sub(r"\bGitHub Project\b", "remote project board", statement, flags=re.IGNORECASE)
    statement = re.sub(r"\bGitHub account\b", "remote repository account", statement, flags=re.IGNORECASE)
    statement = re.sub(r"\bGitHub namespace\b", "remote repository namespace", statement, flags=re.IGNORECASE)
    statement = re.sub(r"\bfull-load\b", "load", statement, flags=re.IGNORECASE)
    if statement and statement[-1] not in ".!?":
        statement += "."
    return statement


def rewrite_phase_references(statement: str) -> str:
    replacements = {
        "phase 1": "the source-discovery stage",
        "phase 2": "the normalization stage",
        "phase 3": "the segmentation stage",
        "phase 4": "the domain-classification stage",
        "phase 5": "the knowledge-extraction stage",
        "phase 6": "the wiki-synthesis stage",
        "phase 7": "the bootstrap-memory stage",
        "phase 8": "the audit stage",
        "phase 9": "the daily-refresh stage",
        "phase 10": "the autonomous corpus-load stage",
    }
    for source, target in replacements.items():
        statement = re.sub(rf"\b{re.escape(source)}\b", target, statement, flags=re.IGNORECASE)
    return statement


def is_renderable_item(item: dict[str, object]) -> bool:
    statement = clean_render_statement(str(item.get("agent_facing_statement") or item.get("statement") or ""))
    if not is_renderable_text(statement):
        return False
    memory_class = str(item.get("memory_class") or "")
    if memory_class == "global_user_rules" and item.get("project"):
        return False
    if memory_class == "global_user_rules" and looks_project_specific(statement):
        return False
    project = str(item.get("project") or "")
    if project and mentions_other_project(statement, project):
        return False
    if memory_class == "project_rules" and str(item.get("promotion_state") or "") not in {"explicit", "repeated", "durable"}:
        return len(item.get("evidence_ids", [])) >= 2 or bool(re.match(r"^(?:no|do not|don't|never|always|must)\b", statement, re.IGNORECASE))
    return True


def is_renderable_text(statement: str) -> bool:
    if not statement or len(statement.strip()) < 12:
        return False
    if RENDER_REJECT_PATTERN.search(statement):
        return False
    if TRANSIENT_RENDER_PATTERN.search(statement):
        return False
    if RAW_FIRST_PERSON_PATTERN.search(statement):
        return False
    if re.match(r"^\d+[\.)]\s+", statement):
        return False
    if statement.count("|") >= 2:
        return False
    return True


def looks_project_specific(statement: str) -> bool:
    lowered = statement.lower()
    return bool(
        re.search(
            r"\b(?:trade card|lineage|openbrain|wikimemory|codexclaw|ai trader|wash-sale|whatsapp|ibkr|phase \d+|database|ui|screen|button|graph|actor|benchmark)\b",
            lowered,
        )
    )


def mentions_other_project(statement: str, project: str) -> bool:
    lowered = statement.lower()
    project_terms = {
        "ai-trader": ("openbrain", "open brain", "codexclaw", "wikimemory"),
        "open-brain": ("ai trader", "aitrader", "codexclaw", "wikimemory"),
        "codexclaw": ("ai trader", "aitrader", "openbrain", "open brain", "wikimemory"),
        "wikimemory": ("ai trader", "aitrader", "openbrain", "open brain", "codexclaw"),
    }
    return any(term in lowered for term in project_terms.get(project, ()))


def normalize_render_key(statement: str) -> str:
    cleaned = re.sub(r"\([^)]*\)", "", statement.lower())
    cleaned = re.sub(r"[^a-z0-9]+", " ", cleaned)
    return " ".join(cleaned.split())[:160]


def write_meta(
    memory_dir: Path,
    items: list[dict[str, object]],
    windows: list[dict[str, object]] | None = None,
    candidates: list[dict[str, object]] | None = None,
) -> None:
    meta_dir = memory_dir / "_meta"
    ensure_directory(meta_dir)
    content = "".join(json.dumps(item, sort_keys=True, separators=(",", ":")) + "\n" for item in items)
    atomic_write_text(meta_dir / "items.jsonl", content)
    atomic_write_text(meta_dir / "merged_items.jsonl", content)
    window_content = "".join(json.dumps(item, sort_keys=True, separators=(",", ":")) + "\n" for item in (windows or []))
    atomic_write_text(meta_dir / "extraction_windows.jsonl", window_content)
    candidate_content = "".join(json.dumps(item, sort_keys=True, separators=(",", ":")) + "\n" for item in (candidates or []))
    atomic_write_text(meta_dir / "candidates.jsonl", candidate_content)
    manifest = {
        "schema_version": 1,
        "item_count": len(items),
        "window_count": len(windows or []),
        "candidate_count": len(candidates or []),
        "rendered_at": utc_now(),
    }
    atomic_write_text(meta_dir / "render_manifest.json", json.dumps(manifest, indent=2, sort_keys=True) + "\n")
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
            item["confidence"] = "strong" if item.get("confidence") in {"candidate", "medium", "low"} else item.get("confidence")
        filtered.append(item)
    return filtered


def prune_stale_recent_items(items: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        item
        for item in items
        if str(item.get("memory_class")) != "recent_project_state"
        or (
            str(item.get("temporal_status") or "active") == "active"
            and not is_older_than_days(item.get("last_seen_at"), RECENT_MEMORY_MAX_DAYS)
        )
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
    if memory_class == "recent_project_state" and str(item.get("temporal_status") or "active") != "active":
        return None
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


def project_overview_clauses(text: str) -> list[str]:
    clauses: list[str] = []
    pending_prefix: str | None = None
    pending_items: list[str] = []
    for line in text.splitlines():
        raw = line.strip()
        is_bullet = raw.startswith("- ")
        clause = clean_clause(raw.lstrip("#").removeprefix("- ").strip())
        if not is_meaningful_clause(clause):
            continue
        if clause.lower() in {"wikimemory", "why this exists", "end-to-end pipeline"}:
            continue
        if pending_prefix and is_bullet:
            pending_items.append(clause.rstrip("."))
            continue
        if pending_prefix:
            clauses.append(compose_colon_clause(pending_prefix, pending_items))
            pending_prefix = None
            pending_items = []
            if len(clauses) >= 8:
                break
        if clause.endswith(":"):
            pending_prefix = clause.rstrip(":")
            pending_items = []
            continue
        if is_overview_fragment_noise(clause):
            continue
        clauses.append(clause)
        if len(clauses) >= 8:
            break
    if pending_prefix and len(clauses) < 8:
        clauses.append(compose_colon_clause(pending_prefix, pending_items))
    return clauses


def compose_colon_clause(prefix: str, items: list[str]) -> str:
    if not items:
        return prefix
    return normalize_statement(f"{prefix} {', '.join(items[:6])}.")


def is_overview_fragment_noise(text: str) -> bool:
    stripped = text.strip()
    lowered = stripped.lower()
    if stripped.endswith("/") or re.search(r"^[\w.-]+/$", stripped):
        return True
    if len(stripped) < 40 and not re.search(r"\b(?:system|service|pipeline|engine|scaffold|memory|agent|trading)\b", lowered):
        return True
    return False


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
    if CONVERSATIONAL_SUMMARY_PREFIX_PATTERN.search(text):
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


def is_git_head_statement(text: str) -> bool:
    return text.strip().startswith("branch=")


def is_config_instruction_statement(text: str) -> bool:
    return bool(re.match(r"^(?:set|export|configure|install|run)\b", text.strip(), re.IGNORECASE))


def project_summary_rank(item: dict[str, object]) -> tuple[int, str]:
    text = str(item.get("statement") or "").strip().lower()
    if re.match(r"^\d+\.", text):
        return (8, text)
    if re.search(r"\b(?:is a|is an|its job is|designed to|source of truth|solves that)\b", text):
        return (0, text)
    if re.search(r"\b(?:pipeline|architecture|input|output|component|adapter|renderer|config|system|service|engine|scaffold)\b", text):
        return (1, text)
    if re.search(r"\b(?:goal is|purpose|built to|intended to)\b", text):
        return (2, text)
    return (4, text)


def stable_id(*parts: object) -> str:
    return hashlib.sha256("|".join(str(part) for part in parts).encode("utf-8")).hexdigest()[:16]


def slugify(value: str) -> str:
    slug = "".join(char.lower() if char.isalnum() else "-" for char in value).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug or "project"


def read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
