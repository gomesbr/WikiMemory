from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable

from .discovery import DiscoveryError, atomic_write_text, ensure_directory, utc_now
from .memory_extraction import extract_memory_artifacts
from .memory_model import MEMORY_FILE_DEFINITIONS
from .memory_v2 import call_llm_json
from .normalization import append_jsonl_text
from .product_config import MarkdownOutputConfig, load_product_config

STATE_SCHEMA_VERSION = 1
MEMORY_SCHEMA_VERSION = 1
MEMORY_RULE_OVERRIDE_SCHEMA_VERSION = 1
DEFAULT_CONTINUATIONS_MODEL = "gpt-4o-mini"
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
    r"(?:\.\.\.|iMPLEMENT THIS PLAN|IMPLEMENT THIS PLAN|PLEASE IMPLEMENT THIS PLAN|<environment_context>|open tabs:|context from my ide setup|current context:|single prompt to codex|copy/paste|source_count:|confidence:|user profile|senior software engineer|store/reports/|api\.fxtwitter|whatsapp group|hundreds of GB|persistent only for the user|video file md|openrouter|one more think|no_queued_strategies|analyze all memory files|^No .* extracted yet\.?$|^No .* selected yet\.?$|^No .* items extracted yet\.?$|^No .* rules selected yet\.?$)",
    re.IGNORECASE,
)
RAW_FIRST_PERSON_PATTERN = re.compile(
    r"\b(?:i think|i keep|i close|i reopen|i don't|i do not|i'll|i will|i need|i'm|i am|i want|i requested|i ran|i found|i never|i can|i've|i only|i have|we don't|my question|my inputs|one question|this is what)\b",
    re.IGNORECASE,
)
TRANSIENT_RENDER_PATTERN = re.compile(
    r"\b(?:what should you focus|what is next|phase \d+ should be treated as a checkpoint|full-load run|commit and merge|push to git|download obsidian|api key|env file|D drive|unclassified count|notices?:\s*\d+|current phase is complete)\b",
    re.IGNORECASE,
)
SCAFFOLD_CONTEXT_PATTERN = re.compile(
    r"(?:\bbelow is the list of skills that can be used\b|\bspecific skill\b|\btool integrations\b|\bassigned task as a single tracker item\b|\bimplementation plans or code-level guidance\b|\bdeveloper workflows\b|\bmaintain dashboards and platform code\b|\bthis skill should be used\b|\bextends codex'?s capabilities\b|\bsenior software engineer\b|\bresponsibilities:\b|\bconsistent ui design language across apps\b)",
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
PURPOSE_ACTION_PATTERN = re.compile(
    r"\b(?:make a change|developing|changing|building|implementing|do not|don't|never|always|must|should|treat .{0,80} as|compatibility|migration|version)\b",
    re.IGNORECASE,
)
PURPOSE_IDENTITY_PATTERN = re.compile(
    r"\b(?:is a|is an|build a|builds? a|designed to|built to|intended to|source of truth|purpose is|goal is|turns .{0,80} into|platform|system|service|tool|memory layer|trading system)\b",
    re.IGNORECASE,
)
ARCHITECTURE_ROLE_PATTERN = re.compile(
    r"\b(?:component|module|service|adapter|engine|pipeline|architecture|input|process|storage|output|database|queue|webhook|scaffold|orchestrates)\b",
    re.IGNORECASE,
)
CONSTRAINT_ROLE_PATTERN = re.compile(
    r"\b(?:constraint|must|only|blocks|strict|kill switch|safety limit|disabled|protect|prevent|avoid|single-user|minimum|maximum|cap|limit)\b",
    re.IGNORECASE,
)
OPEN_PROBLEM_PATTERN = re.compile(r"\b(?:open problem|unresolved|blocked|pending|still needs|todo|must decide|not yet)\b", re.IGNORECASE)
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
MEMORY_COMMAND_PREFIX = "memory command:"
ADD_GLOBAL_RULE_PATTERN = re.compile(r"^memory command:\s*add global rule:\s*(.+)$", re.IGNORECASE)
ADD_PROJECT_RULE_PATTERN = re.compile(
    r"^memory command:\s*add project rule(?: for (?P<project>[\w -]+))?:\s*(?P<statement>.+)$",
    re.IGNORECASE,
)
REMOVE_RULE_PATTERN = re.compile(r'^memory command:\s*remove rule:\s*"?(?P<statement>.+?)"?\s*$', re.IGNORECASE)
REPLACE_RULE_PATTERN = re.compile(
    r'^memory command:\s*replace rule:\s*"(?P<old>.+?)"\s*->\s*"(?P<new>.+?)"\s*$',
    re.IGNORECASE,
)
RECLASSIFY_RULE_PATTERN = re.compile(
    r'^memory command:\s*move rule to (?P<scope>global|project)(?: for (?P<project>[\w -]+))?:\s*"?(?P<statement>.+?)"?\s*$',
    re.IGNORECASE,
)
ONE_OFF_GLOBAL_EXCEPTION_PATTERN = re.compile(
    r"^memory command:\s*one-off global exception:\s*(.+)$",
    re.IGNORECASE,
)
ONE_OFF_PROJECT_EXCEPTION_PATTERN = re.compile(
    r"^memory command:\s*one-off project exception(?: for (?P<project>[\w -]+))?:\s*(?P<statement>.+)$",
    re.IGNORECASE,
)


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
    llm_client=None,
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
    override_state_path = state_dir / "memory_rule_overrides.json"
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
        override_commands = extract_rule_override_commands(evidence_records)
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
        memory_items = apply_rule_overrides(memory_items, override_commands)
        memory_items = prune_stale_recent_items(memory_items)
        memory_items = normalize_memory_item_roles(memory_items)
        rendered_files = render_memory_files(
            memory_dir,
            memory_items,
            config.markdown_output,
            continuations_model=resolve_continuations_model(config),
            llm_client=llm_client,
        )
        write_meta(memory_dir, memory_items, extraction_artifacts.windows, extraction_artifacts.candidates)
        write_rule_override_state(override_state_path, override_commands)
        rendered_files.extend(
            write_consumer_experience_pages(
                memory_dir,
                memory_items,
                evidence_records,
                override_commands,
                config.markdown_output,
                continuations_model=resolve_continuations_model(config),
                llm_client=llm_client,
            )
        )

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
            "override_command_count": len(override_commands),
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
        "memory_role": item_role({"memory_class": memory_class, "statement": statement}),
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


def render_memory_files(
    memory_dir: Path,
    items: list[dict[str, object]],
    markdown_output: MarkdownOutputConfig,
    *,
    continuations_model: str,
    llm_client=None,
) -> list[Path]:
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
            if key == "project_recent":
                project_items = [item for item in items if item.get("project") == project]
            else:
                project_items = [item for item in grouped[key] if item.get("project") == project]
            if definition.optional and not project_items:
                continue
            target = memory_dir / memory_relative_path(key, project)
            render_project_file(target, key, project, project_items, markdown_output)
            rendered.append(target)
    return rendered


def clear_generated_memory_tree(memory_dir: Path) -> None:
    owned_global_files = (
        memory_dir / "global" / "user-rules.md",
        memory_dir / "global" / "memory-change-log.md",
        memory_dir / "global" / "memory-health.md",
        memory_dir / "global" / "active-exceptions.md",
        memory_dir / "global" / "daily-conversations.md",
    )
    owned_meta_files = (
        memory_dir / "_meta" / "items.jsonl",
        memory_dir / "_meta" / "merged_items.jsonl",
        memory_dir / "_meta" / "extraction_windows.jsonl",
        memory_dir / "_meta" / "candidates.jsonl",
        memory_dir / "_meta" / "memory_health.json",
    )
    for path in owned_global_files + owned_meta_files:
        if path.exists():
            path.unlink()
    projects_dir = memory_dir / "projects"
    if projects_dir.exists():
        for project_dir in projects_dir.iterdir():
            if not project_dir.is_dir():
                continue
            for filename in ("project.md", "recent.md", "rules.md", "lessons.md", "continuations.md"):
                target = project_dir / filename
                if target.exists():
                    target.unlink()
    daily_dir = memory_dir / "daily-conversations"
    if daily_dir.exists():
        shutil.rmtree(daily_dir)


def render_global_rules(path: Path, items: list[dict[str, object]], markdown_output: MarkdownOutputConfig) -> None:
    ensure_directory(path.parent)
    lines = frontmatter("global-rules", None, ("memory", "rules", "global"), markdown_output, memory_role="directive")
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
    lines = frontmatter("project-memory", project, (f"project/{project}", "memory"), markdown_output, memory_role="descriptive")
    lines.extend([f"# {BRAIN} {title}", ""])
    used: set[str] = set()
    purpose_items = take_unseen([item for item in descriptive_items if is_purpose_item(item)], used, 3)
    append_section(lines, "PURPOSE", item_statements(purpose_items) or ["Short project purpose not extracted yet."])
    append_section(lines, "CORE COMPONENTS", item_statements(take_unseen([item for item in descriptive_items if is_architecture_item(item)] + filter_by_terms(descriptive_items, ("component", "module", "pipeline", "adapter", "renderer", "service", "engine")), used, 6)) or ["No stable component list extracted yet."])
    append_section(lines, "CURRENT ARCHITECTURE", item_statements(take_unseen([item for item in descriptive_items if is_architecture_item(item)] + filter_by_terms(descriptive_items, ("architecture", "input", "process", "storage", "output", "pipeline", "service", "engine")), used, 6)) or ["No stable architecture summary extracted yet."])
    append_section(lines, "DESIGN PRINCIPLES", item_statements(take_unseen(filter_by_terms(descriptive_items, ("deterministic", "traceable", "modular", "provenance", "incremental")), used, 6)) or ["No stable design principles extracted yet."])
    append_section(lines, "KEY CONSTRAINTS", item_statements(take_unseen([item for item in stable_items if is_constraint_item(item)] + filter_by_terms(stable_items, ("constraint", "must", "do not", "never", "only", "blocks", "disabled", "strict", "kill switch")), used, 6)) or ["No stable constraints extracted yet."])
    append_section(lines, "OPEN PROBLEMS", item_statements(take_unseen([item for item in descriptive_items if is_open_problem_item(item)], used, 5)) or ["No open project-level problems extracted yet."])
    append_related(lines, project, markdown_output)
    return lines


def render_project_recent(project: str, items: list[dict[str, object]], markdown_output: MarkdownOutputConfig) -> list[str]:
    title = f"{display_project(project)} - Recent Context"
    active_items = [
        item
        for item in items
        if str(item.get("memory_class") or "") == "recent_project_state"
        and str(item.get("item_type") or "") != "open_question"
        and is_renderable_item(item)
    ]
    ranked = sorted(active_items, key=lambda item: str(item.get("last_seen_at") or ""), reverse=True)[:PROJECT_RECENT_ITEM_CAP]
    fallback_ranked = sorted(
        [
            item
            for item in items
            if str(item.get("memory_class") or "") in {"stable_project_summary", "project_lessons"}
        ],
        key=lambda item: str(item.get("last_seen_at") or ""),
        reverse=True,
    )
    used: set[str] = set()
    lines = frontmatter("recent-context", project, (f"project/{project}", "recent"), markdown_output, memory_role="descriptive")
    lines.extend([f"# {FIRE} {title}", ""])
    focus_items = take_unseen([item for item in ranked if str(item.get("item_type")) == "current_state"], used, 4)
    if not focus_items:
        focus_items = take_unseen(
            [item for item in ranked if str(item.get("item_type")) in {"task", "next_step", "decision"}],
            used,
            3,
        )
    if not focus_items:
        focus_items = take_unseen(fallback_ranked, used, 2)
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
    lines = frontmatter("project-rules", project, (f"project/{project}", "rules"), markdown_output, memory_role="directive")
    lines.extend([f"# {GEAR} {title}", ""])
    append_rule_sections(lines, items, include_scope_notes=True)
    append_related(lines, project, markdown_output, include_global=False)
    return lines


def render_project_lessons(project: str, items: list[dict[str, object]], markdown_output: MarkdownOutputConfig) -> list[str]:
    title = f"{display_project(project)} - Lessons Learned"
    lines = frontmatter("lessons", project, (f"project/{project}", "lessons"), markdown_output, memory_role="guidance")
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
    memory_role: str,
) -> list[str]:
    if not markdown_output.enable_frontmatter:
        return []
    lines = ["---", f"type: {memory_type}"]
    if project:
        lines.append(f"project: {project}")
    lines.append(f"updated: {utc_now()}")
    lines.append(f"memory_role: {memory_role}")
    if markdown_output.enable_tags:
        lines.append("tags: [" + ", ".join(tags) + "]")
    lines.extend(["---", ""])
    return lines


def append_rule_sections(lines: list[str], items: list[dict[str, object]], include_scope_notes: bool) -> None:
    eligible = dedupe_render_items([item for item in items if is_renderable_item(item)])
    always = [item for item in eligible if rule_bucket(item) == "always"][:RULE_BUCKET_CAP]
    never = [item for item in eligible if rule_bucket(item) == "never"][:RULE_BUCKET_CAP]
    conditional = [item for item in eligible if rule_bucket(item) == "conditional"][:RULE_BUCKET_CAP]
    visible_explicit = [item for item in always + never + conditional if str(item.get("promotion_state")) == "explicit"]
    inferred = [item for item in eligible if str(item.get("promotion_state")) != "explicit"][:INFERRED_RULE_CAP]
    append_section(lines, "ALWAYS DO", item_statements(always))
    append_section(lines, "NEVER DO", item_statements(never))
    append_section(lines, "CONDITIONAL RULES", item_statements(conditional))
    header = "PROMOTED RULES (EXPLICIT)" if include_scope_notes else "CONFIRMED RULES (EXPLICIT)"
    append_section(lines, header, confirmation_summary(visible_explicit))
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
    project = str(item.get("project") or "")
    if project and "new project version" in statement:
        statement = statement.replace("new project version", f"new {display_project(project)} version")
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


def item_role(item: dict[str, object]) -> str:
    role = str(item.get("memory_role") or "").strip().lower()
    statement = clean_render_statement(str(item.get("agent_facing_statement") or item.get("statement") or ""))
    if role == "purpose" and PURPOSE_ACTION_PATTERN.search(statement):
        return "rule"
    if role == "purpose" and not PURPOSE_IDENTITY_PATTERN.search(statement):
        return "discard"
    if role:
        return role
    memory_class = str(item.get("memory_class") or "")
    item_type = str(item.get("item_type") or "")
    if memory_class in {"global_user_rules", "project_rules"}:
        return "rule"
    if memory_class == "project_lessons" or item_type == "lesson":
        return "lesson"
    if memory_class == "recent_project_state":
        return "decision" if item_type == "decision" else "recent_state"
    if item_type == "purpose":
        return "purpose"
    if item_type == "architecture":
        return "architecture"
    if item_type == "constraint":
        return "constraint"
    if item_type == "decision":
        return "decision"
    if PURPOSE_ACTION_PATTERN.search(statement):
        return "rule"
    if CONSTRAINT_ROLE_PATTERN.search(statement):
        return "constraint"
    if PURPOSE_IDENTITY_PATTERN.search(statement):
        return "purpose"
    if ARCHITECTURE_ROLE_PATTERN.search(statement):
        return "architecture"
    return "discard"


def is_purpose_item(item: dict[str, object]) -> bool:
    statement = clean_render_statement(str(item.get("agent_facing_statement") or item.get("statement") or ""))
    return item_role(item) == "purpose" and bool(PURPOSE_IDENTITY_PATTERN.search(statement)) and not PURPOSE_ACTION_PATTERN.search(statement)


def is_architecture_item(item: dict[str, object]) -> bool:
    return item_role(item) == "architecture"


def is_constraint_item(item: dict[str, object]) -> bool:
    return item_role(item) == "constraint"


def is_open_problem_item(item: dict[str, object]) -> bool:
    statement = clean_render_statement(str(item.get("agent_facing_statement") or item.get("statement") or ""))
    return item_role(item) == "recent_state" and OPEN_PROBLEM_PATTERN.search(statement)


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


def render_rank(item: dict[str, object]) -> tuple[int, int, int, str]:
    confidence = {"explicit": 0, "strong": 1, "medium": 2, "low": 3, "candidate": 4}.get(str(item.get("confidence") or ""), 4)
    support = -len(item.get("evidence_ids", []))
    statement = clean_render_statement(str(item.get("agent_facing_statement") or item.get("statement") or ""))
    priority = -1 if re.search(r"\b(?:backward compatibility|clean system|previous version|new version)\b", statement, re.IGNORECASE) else 0
    return (priority, confidence, support, str(item.get("last_seen_at") or ""))


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
    if re.search(r"\b(?:every time you make a change,?\s*)?think about the system as new\b", statement, re.IGNORECASE):
        statement = "When developing a new project version that is not yet in production use, do not preserve backward compatibility with the previous version by default. Treat the new version as a clean system unless the user explicitly asks for migration or compatibility support."
    statement = rewrite_phase_references(statement)
    statement = re.sub(r"\bGitHub Project\b", "remote project board", statement, flags=re.IGNORECASE)
    statement = re.sub(r"\bGitHub account\b", "remote repository account", statement, flags=re.IGNORECASE)
    statement = re.sub(r"\bGitHub namespace\b", "remote repository namespace", statement, flags=re.IGNORECASE)
    statement = re.sub(r"\bGitHub access\b", "remote repository access", statement, flags=re.IGNORECASE)
    statement = re.sub(r"\bGitHub\b", "the remote repository", statement, flags=re.IGNORECASE)
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
    role = item_role(item)
    if role == "discard":
        return False
    if memory_class == "global_user_rules" and item.get("project"):
        return False
    if memory_class == "global_user_rules" and looks_project_specific(statement):
        return False
    project = str(item.get("project") or "")
    if project and mentions_other_project(statement, project):
        return False
    if memory_class == "project_rules" and str(item.get("promotion_state") or "") not in {"explicit", "repeated", "durable"}:
        if role == "rule" and re.search(r"\b(?:compatibility|migration|clean system|previous version|new version)\b", statement, re.IGNORECASE):
            return True
        return len(item.get("evidence_ids", [])) >= 2 or bool(re.match(r"^(?:no|do not|don't|never|always|must)\b", statement, re.IGNORECASE))
    return True


def is_renderable_text(statement: str) -> bool:
    if not statement or len(statement.strip()) < 12:
        return False
    if RENDER_REJECT_PATTERN.search(statement):
        return False
    if TRANSIENT_RENDER_PATTERN.search(statement):
        return False
    if SCAFFOLD_CONTEXT_PATTERN.search(statement):
        return False
    if RAW_FIRST_PERSON_PATTERN.search(statement):
        return False
    if statement.strip().endswith("?"):
        return False
    if re.search(r"\b(?:maybe|etc\.?|not only the)\b", statement, re.IGNORECASE):
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
            r"\b(?:trade card|lineage|openbrain|sessionmemory|codexclaw|ai trader|wash-sale|whatsapp|ibkr|phase \d+|database|ui|screen|button|graph|actor|benchmark)\b",
            lowered,
        )
    )


def mentions_other_project(statement: str, project: str) -> bool:
    lowered = statement.lower()
    project_terms = {
        "aitrader": ("openbrain", "open brain", "codexclaw", "sessionmemory"),
        "ai-trader": ("openbrain", "open brain", "codexclaw", "sessionmemory"),
        "open-brain": ("ai trader", "aitrader", "codexclaw", "sessionmemory"),
        "codexclaw": ("ai trader", "aitrader", "openbrain", "open brain", "sessionmemory"),
        "sessionmemory": ("ai trader", "aitrader", "openbrain", "open brain", "codexclaw"),
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


def extract_rule_override_commands(records: list[dict[str, object]]) -> list[dict[str, object]]:
    commands: list[dict[str, object]] = []
    for record in records:
        if str(record.get("actor_type") or "") != "user":
            continue
        text = evidence_text(record)
        if MEMORY_COMMAND_PREFIX not in text.lower():
            continue
        for raw_line in text.splitlines():
            line = raw_line.strip()
            if not line.lower().startswith(MEMORY_COMMAND_PREFIX):
                continue
            command = parse_rule_override_command(line, record)
            if command:
                commands.append(command)
    deduped: dict[str, dict[str, object]] = {}
    for command in commands:
        deduped[str(command["command_id"])] = command
    return sorted(deduped.values(), key=lambda item: str(item.get("timestamp") or ""))


def parse_rule_override_command(line: str, record: dict[str, object]) -> dict[str, object] | None:
    project_hint = slugify(str(record.get("project_hint") or record.get("source_id") or "project"))
    timestamp = str(record.get("timestamp") or "")
    evidence_id = str(record.get("evidence_id") or "")
    provenance = dict(record.get("provenance") or {})
    source_id = str(record.get("source_id") or provenance.get("source_id") or "")
    message_index = int(provenance.get("source_line_no") or 0)

    add_global = ADD_GLOBAL_RULE_PATTERN.match(line)
    if add_global:
        statement = normalize_statement(add_global.group(1))
        return override_command(
            action="add_rule",
            scope="global",
            project=None,
            statement=statement,
            record=record,
            timestamp=timestamp,
            evidence_id=evidence_id,
            source_id=source_id,
            message_index=message_index,
        )
    add_project = ADD_PROJECT_RULE_PATTERN.match(line)
    if add_project:
        statement = normalize_statement(str(add_project.group("statement") or ""))
        target_project = slugify(str(add_project.group("project") or project_hint))
        return override_command(
            action="add_rule",
            scope="project",
            project=target_project,
            statement=statement,
            record=record,
            timestamp=timestamp,
            evidence_id=evidence_id,
            source_id=source_id,
            message_index=message_index,
        )
    remove_rule = REMOVE_RULE_PATTERN.match(line)
    if remove_rule:
        return override_command(
            action="remove_rule",
            scope="project" if project_hint not in {"", "project"} else "global",
            project=None if project_hint in {"", "project"} else project_hint,
            target_statement=normalize_statement(str(remove_rule.group("statement") or "")),
            record=record,
            timestamp=timestamp,
            evidence_id=evidence_id,
            source_id=source_id,
            message_index=message_index,
        )
    replace_rule = REPLACE_RULE_PATTERN.match(line)
    if replace_rule:
        return override_command(
            action="replace_rule",
            scope="project" if project_hint not in {"", "project"} else "global",
            project=None if project_hint in {"", "project"} else project_hint,
            statement=normalize_statement(str(replace_rule.group("new") or "")),
            target_statement=normalize_statement(str(replace_rule.group("old") or "")),
            record=record,
            timestamp=timestamp,
            evidence_id=evidence_id,
            source_id=source_id,
            message_index=message_index,
        )
    reclassify = RECLASSIFY_RULE_PATTERN.match(line)
    if reclassify:
        scope = str(reclassify.group("scope") or "global").lower()
        target_project = slugify(str(reclassify.group("project") or project_hint)) if scope == "project" else None
        return override_command(
            action="reclassify_rule_scope",
            scope=scope,
            project=target_project,
            target_statement=normalize_statement(str(reclassify.group("statement") or "")),
            record=record,
            timestamp=timestamp,
            evidence_id=evidence_id,
            source_id=source_id,
            message_index=message_index,
        )
    one_off_global = ONE_OFF_GLOBAL_EXCEPTION_PATTERN.match(line)
    if one_off_global:
        return override_command(
            action="mark_one_off_exception",
            scope="global",
            project=None,
            statement=normalize_statement(str(one_off_global.group(1) or "")),
            record=record,
            timestamp=timestamp,
            evidence_id=evidence_id,
            source_id=source_id,
            message_index=message_index,
            mode="one_off",
        )
    one_off_project = ONE_OFF_PROJECT_EXCEPTION_PATTERN.match(line)
    if one_off_project:
        target_project = slugify(str(one_off_project.group("project") or project_hint))
        return override_command(
            action="mark_one_off_exception",
            scope="project",
            project=target_project,
            statement=normalize_statement(str(one_off_project.group("statement") or "")),
            record=record,
            timestamp=timestamp,
            evidence_id=evidence_id,
            source_id=source_id,
            message_index=message_index,
            mode="one_off",
        )
    return None


def override_command(
    *,
    action: str,
    scope: str,
    project: str | None,
    record: dict[str, object],
    timestamp: str,
    evidence_id: str,
    source_id: str,
    message_index: int,
    statement: str | None = None,
    target_statement: str | None = None,
    mode: str = "durable",
) -> dict[str, object]:
    expires_at = None
    if mode == "one_off" and timestamp:
        try:
            expires_at = (datetime.fromisoformat(timestamp.replace("Z", "+00:00")) + timedelta(days=30)).isoformat().replace("+00:00", "Z")
        except ValueError:
            expires_at = None
    payload = {
        "schema_version": MEMORY_RULE_OVERRIDE_SCHEMA_VERSION,
        "command_id": stable_id(action, scope, project or "global", statement or "", target_statement or "", evidence_id),
        "action": action,
        "scope": scope,
        "project": project,
        "statement": statement,
        "target_statement": target_statement,
        "mode": mode,
        "expires_at": expires_at,
        "timestamp": timestamp,
        "origin": {
            "source_id": source_id,
            "snippet_id": evidence_id,
            "message_index": message_index,
        },
        "source_text": evidence_text(record),
    }
    return payload


def apply_rule_overrides(items: list[dict[str, object]], commands: list[dict[str, object]]) -> list[dict[str, object]]:
    updated = [dict(item) for item in items]
    for command in commands:
        action = str(command.get("action") or "")
        if action == "add_rule":
            updated = add_override_rule(updated, command)
        elif action == "remove_rule":
            updated = remove_override_rule(updated, command)
        elif action == "replace_rule":
            updated = remove_override_rule(updated, command)
            updated = add_override_rule(updated, command)
        elif action == "reclassify_rule_scope":
            updated = reclassify_override_rule(updated, command)
    return updated


def add_override_rule(items: list[dict[str, object]], command: dict[str, object]) -> list[dict[str, object]]:
    statement = normalize_statement(str(command.get("statement") or ""))
    if not statement:
        return items
    scope = str(command.get("scope") or "global")
    project = str(command.get("project") or "")
    memory_class = "global_user_rules" if scope == "global" else "project_rules"
    durable_project = None if scope == "global" else project
    item_id = stable_id("consumer_override", scope, durable_project or "global", statement)
    new_item = {
        "item_id": item_id,
        "memory_schema_version": MEMORY_SCHEMA_VERSION,
        "memory_class": memory_class,
        "memory_role": "rule",
        "scope": "global" if scope == "global" else "project",
        "project": durable_project,
        "promotion_state": "explicit",
        "durability": "durable",
        "temporal_status": "durable",
        "statement": statement,
        "source_actor_types": ["user"],
        "evidence_ids": [str(command.get("origin", {}).get("snippet_id") or "")],
        "provenance_refs": [dict(command.get("origin") or {})],
        "first_seen_at": command.get("timestamp"),
        "last_seen_at": command.get("timestamp"),
        "confidence": "explicit",
        "review_required": False,
        "review_reason": None,
        "authority": "consumer_override",
        "locked_by_consumer": True,
        "override_command_id": str(command.get("command_id") or ""),
    }
    updated: list[dict[str, object]] = []
    matched = False
    for item in items:
        if (
            str(item.get("memory_role") or "") == "rule"
            and str(item.get("scope") or "") == new_item["scope"]
            and str(item.get("project") or "") == str(new_item.get("project") or "")
            and normalize_statement(str(item.get("statement") or "")) == statement
        ):
            merged = dict(item)
            merged.update(new_item)
            merged["evidence_ids"] = sorted(set(item.get("evidence_ids", [])) | set(new_item["evidence_ids"]))
            merged["provenance_refs"] = list(item.get("provenance_refs", [])) + [
                ref for ref in new_item["provenance_refs"] if ref not in item.get("provenance_refs", [])
            ]
            updated.append(merged)
            matched = True
            continue
        updated.append(item)
    if not matched:
        updated.append(new_item)
    return updated


def remove_override_rule(items: list[dict[str, object]], command: dict[str, object]) -> list[dict[str, object]]:
    target_statement = normalize_statement(str(command.get("target_statement") or ""))
    scope = str(command.get("scope") or "")
    project = str(command.get("project") or "")
    return [
        item
        for item in items
        if not (
            str(item.get("memory_role") or "") == "rule"
            and normalize_statement(str(item.get("statement") or "")) == target_statement
            and (not scope or str(item.get("scope") or "") == ("global" if scope == "global" else "project"))
            and (scope != "project" or not project or str(item.get("project") or "") == project)
        )
    ]


def reclassify_override_rule(items: list[dict[str, object]], command: dict[str, object]) -> list[dict[str, object]]:
    target_statement = normalize_statement(str(command.get("target_statement") or ""))
    scope = str(command.get("scope") or "global")
    project = str(command.get("project") or "")
    updated: list[dict[str, object]] = []
    for item in items:
        if str(item.get("memory_role") or "") != "rule":
            updated.append(item)
            continue
        if normalize_statement(str(item.get("statement") or "")) != target_statement:
            updated.append(item)
            continue
        rewritten = dict(item)
        rewritten["scope"] = "global" if scope == "global" else "project"
        rewritten["project"] = None if scope == "global" else project
        rewritten["memory_class"] = "global_user_rules" if scope == "global" else "project_rules"
        rewritten["authority"] = "consumer_override"
        rewritten["locked_by_consumer"] = True
        rewritten["override_command_id"] = str(command.get("command_id") or "")
        updated.append(rewritten)
    return updated


def write_rule_override_state(path: Path, commands: list[dict[str, object]]) -> None:
    payload = {
        "schema_version": MEMORY_RULE_OVERRIDE_SCHEMA_VERSION,
        "last_updated_at": utc_now(),
        "command_count": len(commands),
        "active_exception_count": len(active_exception_commands(commands)),
        "commands": commands,
    }
    atomic_write_text(path, json.dumps(payload, indent=2, sort_keys=True) + "\n")


def write_consumer_experience_pages(
    memory_dir: Path,
    items: list[dict[str, object]],
    evidence_records: list[dict[str, object]],
    commands: list[dict[str, object]],
    markdown_output: MarkdownOutputConfig,
    *,
    continuations_model: str,
    llm_client=None,
) -> list[Path]:
    rendered: list[Path] = []
    health_payload = build_memory_health_payload(items, commands)
    meta_dir = memory_dir / "_meta"
    ensure_directory(meta_dir)
    atomic_write_text(meta_dir / "memory_health.json", json.dumps(health_payload, indent=2, sort_keys=True) + "\n")

    change_log_path = memory_dir / "global" / "memory-change-log.md"
    render_memory_change_log(change_log_path, commands, markdown_output)
    rendered.append(change_log_path)

    health_path = memory_dir / "global" / "memory-health.md"
    render_memory_health(health_path, health_payload, markdown_output)
    rendered.append(health_path)

    exceptions_path = memory_dir / "global" / "active-exceptions.md"
    render_active_exceptions(exceptions_path, active_exception_commands(commands), markdown_output)
    rendered.append(exceptions_path)

    daily_paths = render_daily_conversation_pages(memory_dir, evidence_records, markdown_output)
    rendered.extend(daily_paths)

    projects = sorted({str(item.get("project") or "") for item in items if item.get("project")})
    for project in projects:
        continuation_path = memory_dir / "projects" / project / "continuations.md"
        render_project_continuations(
            continuation_path,
            project,
            [item for item in items if str(item.get("project") or "") == project],
            [command for command in active_exception_commands(commands) if str(command.get("project") or "") == project],
            markdown_output,
            continuations_model=continuations_model,
            llm_client=llm_client,
        )
        rendered.append(continuation_path)
    return rendered


def render_daily_conversation_pages(
    memory_dir: Path,
    evidence_records: list[dict[str, object]],
    markdown_output: MarkdownOutputConfig,
) -> list[Path]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for record in evidence_records:
        day = str(record.get("timestamp") or "")[:10]
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", day):
            continue
        if not is_daily_conversation_record(record):
            continue
        grouped[day].append(record)

    rendered: list[Path] = []
    daily_dir = memory_dir / "daily-conversations"
    ensure_directory(daily_dir)
    for day in sorted(grouped):
        path = daily_dir / f"{day}.md"
        render_daily_conversation_page(path, day, grouped[day], markdown_output)
        rendered.append(path)

    index_path = memory_dir / "global" / "daily-conversations.md"
    render_daily_conversation_index(index_path, sorted(grouped), markdown_output)
    rendered.append(index_path)
    return rendered


def is_daily_conversation_record(record: dict[str, object]) -> bool:
    if str(record.get("evidence_type") or "") != "log_event":
        return False
    actor_type = str(record.get("actor_type") or "")
    if actor_type not in {"user", "assistant"}:
        return False
    text = clean_daily_conversation_text(evidence_text(record))
    return bool(text)


def clean_daily_conversation_text(text: str) -> str:
    cleaned = " ".join(str(text or "").split()).strip()
    if not cleaned:
        return ""
    reject_prefixes = (
        "# AGENTS.md instructions",
        "<environment_context>",
        "<permissions instructions>",
        "<collaboration_mode>",
        "## Available skills",
        "### Available skills",
    )
    if any(cleaned.startswith(prefix) for prefix in reject_prefixes):
        return ""
    cleaned = re.sub(r"^# Context from my IDE setup:\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"^## Active file:.*$", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"^## Open tabs:.*$", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"^## My request for Codex:\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = cleaned.strip(" -")
    if len(cleaned) > 280:
        cleaned = cleaned[:277].rstrip() + "..."
    return cleaned


def render_daily_conversation_page(path: Path, day: str, records: list[dict[str, object]], markdown_output: MarkdownOutputConfig) -> None:
    ensure_directory(path.parent)
    lines = frontmatter("daily-conversation-history", None, ("memory", "daily-conversations"), markdown_output, memory_role="descriptive")
    lines.extend([f"# {BRAIN} Daily Conversation History - {day}", ""])
    append_section(
        lines,
        "SUMMARY",
        [
            f"{len(records)} conversation event(s) captured for this day.",
            "This is a compact readable history derived from artifacts, not a verbatim transcript.",
        ],
    )
    entries: list[str] = []
    for record in sorted(records, key=lambda item: str(item.get("timestamp") or "")):
        text = clean_daily_conversation_text(evidence_text(record))
        if not text:
            continue
        actor = "User" if str(record.get("actor_type") or "") == "user" else "Assistant"
        timestamp = str(record.get("timestamp") or "")
        time_label = timestamp[11:16] if len(timestamp) >= 16 else "unknown"
        entries.append(f"{time_label} {actor}: {text}")
    append_numbered_section(lines, "CONVERSATION", entries or ["No readable conversation content extracted for this day."])
    atomic_write_text(path, "\n".join(lines))


def render_daily_conversation_index(path: Path, days: list[str], markdown_output: MarkdownOutputConfig) -> None:
    ensure_directory(path.parent)
    lines = frontmatter("daily-conversation-index", None, ("memory", "daily-conversations", "global"), markdown_output, memory_role="descriptive")
    lines.extend([f"# {BRAIN} Daily Conversations", ""])
    append_section(
        lines,
        "USAGE",
        [
            "Daily conversation pages are available for Obsidian browsing.",
            "They are not part of the default agent bootstrap and should only be read when explicitly requested.",
        ],
    )
    entries = [f"memory/daily-conversations/{day}.md" for day in reversed(days)]
    append_section(lines, "AVAILABLE DAYS", entries or ["No daily conversation pages generated yet."])
    atomic_write_text(path, "\n".join(lines))


def resolve_continuations_model(config) -> str:
    return (
        os.environ.get("SESSIONMEMORY_CONTINUATIONS_MODEL", "").strip()
        or os.environ.get(config.memory_extraction.provider.model_env, "").strip()
        or config.memory_extraction.provider.default_model
        or DEFAULT_CONTINUATIONS_MODEL
    )


def active_exception_commands(commands: list[dict[str, object]]) -> list[dict[str, object]]:
    active: list[dict[str, object]] = []
    now = datetime.now(timezone.utc)
    for command in commands:
        if str(command.get("action") or "") != "mark_one_off_exception":
            continue
        expires_at = str(command.get("expires_at") or "")
        if expires_at:
            try:
                if datetime.fromisoformat(expires_at.replace("Z", "+00:00")) < now:
                    continue
            except ValueError:
                pass
        active.append(command)
    return active


def build_memory_health_payload(items: list[dict[str, object]], commands: list[dict[str, object]]) -> dict[str, object]:
    projects = sorted({str(item.get("project") or "") for item in items if item.get("project")})
    explicit_rules = sum(1 for item in items if str(item.get("memory_role") or "") == "rule" and str(item.get("confidence") or "") == "explicit")
    review_queue = sum(1 for item in items if item.get("review_required"))
    locked_rules = sum(1 for item in items if item.get("locked_by_consumer"))
    stale_recent = sum(
        1
        for item in items
        if str(item.get("memory_class") or "") == "recent_project_state" and is_older_than_days(item.get("last_seen_at"), RECENT_MEMORY_MAX_DAYS)
    )
    project_summaries = sum(1 for project in projects if any(str(item.get("project") or "") == project and str(item.get("memory_class") or "") == "stable_project_summary" for item in items))
    project_recent = sum(1 for project in projects if any(str(item.get("project") or "") == project and str(item.get("memory_class") or "") == "recent_project_state" for item in items))
    penalties = review_queue * 6 + stale_recent * 8 + max(0, len(projects) - project_summaries) * 10 + max(0, len(projects) - project_recent) * 6
    score = max(0, min(100, 100 - penalties))
    return {
        "generated_at": utc_now(),
        "score": score,
        "project_count": len(projects),
        "explicit_rule_count": explicit_rules,
        "review_queue_count": review_queue,
        "locked_rule_count": locked_rules,
        "active_exception_count": len(active_exception_commands(commands)),
        "stale_recent_count": stale_recent,
        "coverage": {
            "projects_with_summary": project_summaries,
            "projects_with_recent": project_recent,
        },
    }


def render_memory_change_log(path: Path, commands: list[dict[str, object]], markdown_output: MarkdownOutputConfig) -> None:
    ensure_directory(path.parent)
    lines = frontmatter("memory-change-log", None, ("memory", "changes", "global"), markdown_output, memory_role="descriptive")
    lines.extend([f"# {BRAIN} Memory Change Log", ""])
    append_section(
        lines,
        "SUMMARY",
        [
            f"{len(commands)} consumer-authored memory change command(s) are currently recorded.",
            "Durable override commands are protected from automatic lint rewrites.",
        ],
    )
    entries = []
    for command in sorted(commands, key=lambda item: str(item.get("timestamp") or ""), reverse=True)[:20]:
        action = str(command.get("action") or "")
        mode = str(command.get("mode") or "durable")
        scope = str(command.get("scope") or "")
        project = str(command.get("project") or "")
        statement = str(command.get("statement") or command.get("target_statement") or "").strip()
        timestamp = str(command.get("timestamp") or "")
        qualifier = f"{scope} {project}".strip()
        entries.append(f"{timestamp}: {action} ({mode}, {qualifier}) -> {statement}")
    append_section(lines, "RECENT CHANGES", entries)
    atomic_write_text(path, "\n".join(lines))


def render_memory_health(path: Path, payload: dict[str, object], markdown_output: MarkdownOutputConfig) -> None:
    ensure_directory(path.parent)
    lines = frontmatter("memory-health", None, ("memory", "health", "global"), markdown_output, memory_role="descriptive")
    lines.extend([f"# {BRAIN} Memory Health", ""])
    append_section(
        lines,
        "STATUS",
        [
            f"Overall memory health score: {payload.get('score')}/100.",
            f"Projects tracked: {payload.get('project_count')}.",
            f"Explicit rules: {payload.get('explicit_rule_count')}.",
            f"Locked consumer overrides: {payload.get('locked_rule_count')}.",
        ],
    )
    append_section(
        lines,
        "WATCH LIST",
        [
            f"Review queue items: {payload.get('review_queue_count')}.",
            f"Active one-off exceptions: {payload.get('active_exception_count')}.",
            f"Stale recent items: {payload.get('stale_recent_count')}.",
            f"Projects with summary coverage: {payload.get('coverage', {}).get('projects_with_summary', 0)}.",
            f"Projects with recent coverage: {payload.get('coverage', {}).get('projects_with_recent', 0)}.",
        ],
    )
    atomic_write_text(path, "\n".join(lines))


def render_active_exceptions(path: Path, commands: list[dict[str, object]], markdown_output: MarkdownOutputConfig) -> None:
    ensure_directory(path.parent)
    lines = frontmatter("active-exceptions", None, ("memory", "exceptions", "global"), markdown_output, memory_role="descriptive")
    lines.extend([f"# {FIRE} Active Exceptions", ""])
    bullets = []
    for command in sorted(commands, key=lambda item: str(item.get("timestamp") or ""), reverse=True):
        scope = str(command.get("scope") or "")
        project = str(command.get("project") or "")
        statement = str(command.get("statement") or "").strip()
        expires_at = str(command.get("expires_at") or "")
        label = f"{scope} {project}".strip()
        bullets.append(f"{label}: {statement} (expires {expires_at or 'unknown'})")
    append_section(lines, "ACTIVE", bullets)
    atomic_write_text(path, "\n".join(lines))


def render_project_continuations(
    path: Path,
    project: str,
    items: list[dict[str, object]],
    exceptions: list[dict[str, object]],
    markdown_output: MarkdownOutputConfig,
    *,
    continuations_model: str,
    llm_client=None,
) -> None:
    ensure_directory(path.parent)
    lines = frontmatter("project-continuations", project, (f"project/{project}", "continuations"), markdown_output, memory_role="descriptive")
    lines.extend([f"# {FIRE} {display_project(project)} - Continuation Threads", ""])
    continuations = synthesize_project_continuations(project, items, exceptions, continuations_model, llm_client)
    append_numbered_section(lines, "LIKELY CONTINUATION THREADS", continuations[:6] or ["No strong continuation thread extracted yet."])
    append_section(lines, "PROJECT WORKSTYLE HINTS", project_workstyle_hints(items))
    append_section(
        lines,
        "ACTIVE EXCEPTIONS",
        [str(command.get("statement") or "").strip() for command in exceptions if str(command.get("statement") or "").strip()],
    )
    append_section(lines, "USAGE", ["Use these as continuation options only. Do not start work on them until the consumer chooses one."])
    atomic_write_text(path, "\n".join(lines))


def synthesize_project_continuations(
    project: str,
    items: list[dict[str, object]],
    exceptions: list[dict[str, object]],
    model: str,
    llm_client=None,
) -> list[str]:
    recent_items = [
        item
        for item in items
        if str(item.get("memory_class") or "") == "recent_project_state" and is_renderable_item(item)
    ]
    if not recent_items:
        return []
    payload = {
        "task": "Summarize current project continuation options for a new chat bootstrap. Return JSON only.",
        "project": project,
        "requirements": {
            "max_threads": 6,
            "style": [
                "Each thread must be a clear resumable option, not a copied chat fragment.",
                "Do not use second-person commands like 'implement this' or 'do that'.",
                "Name the workstream or decision clearly enough that the consumer can recognize it.",
                "Keep each thread concise, ideally one sentence under 140 characters.",
                "Use only evidence-backed active work, pending decisions, open problems, or next-step clusters.",
            ],
        },
        "recent_items": [serialize_continuation_item(item) for item in sorted(recent_items, key=continuation_rank, reverse=True)[:18]],
        "project_rules": [clean_render_statement(str(item.get("statement") or "")) for item in items if str(item.get("memory_class") or "") == "project_rules"][:6],
        "active_exceptions": [str(command.get("statement") or "").strip() for command in exceptions if str(command.get("statement") or "").strip()][:4],
    }
    try:
        response = call_llm_json(continuations_prompt(), payload, model, llm_client)
    except Exception:
        return []
    threads = response.get("threads")
    if not isinstance(threads, list):
        return []
    normalized: list[str] = []
    seen: set[str] = set()
    for thread in threads:
        if isinstance(thread, dict):
            statement = str(thread.get("summary") or thread.get("title") or "").strip()
        else:
            statement = str(thread).strip()
        statement = clean_render_statement(statement)
        normalized_statement = normalize_statement(statement)
        if not statement or normalized_statement in seen:
            continue
        if RENDER_REJECT_PATTERN.search(statement) or RECENT_NOISE_PATTERN.search(statement):
            continue
        seen.add(normalized_statement)
        normalized.append(statement)
    return normalized[:6]


def continuations_prompt() -> str:
    return (
        "You turn recent project memory into continuation options for a returning consumer. "
        "Return a JSON object with a 'threads' array. "
        "Each thread should be a short, concrete resumable option describing a workstream, unresolved problem, or pending decision. "
        "Do not copy raw imperative chat fragments. "
        "Do not invent work that is not supported by the evidence. "
        "Do not assume the consumer wants any thread started automatically."
    )


def serialize_continuation_item(item: dict[str, object]) -> dict[str, object]:
    return {
        "item_type": str(item.get("item_type") or ""),
        "statement": clean_render_statement(str(item.get("statement") or item.get("agent_facing_statement") or "")),
        "last_seen_at": str(item.get("last_seen_at") or ""),
        "confidence": str(item.get("confidence") or ""),
        "temporal_status": str(item.get("temporal_status") or ""),
    }


def continuation_rank(item: dict[str, object]) -> tuple[int, str]:
    item_type = str(item.get("item_type") or "")
    priority = {
        "current_state": 0,
        "task": 1,
        "next_step": 1,
        "decision": 2,
        "failure_risk": 3,
        "open_question": 4,
    }.get(item_type, 5)
    return (-priority, str(item.get("last_seen_at") or ""))


def project_workstyle_hints(items: list[dict[str, object]]) -> list[str]:
    rules = [item for item in items if str(item.get("memory_class") or "") == "project_rules"]
    hints = []
    for item in rules:
        statement = clean_render_statement(str(item.get("statement") or ""))
        if re.search(r"\b(?:prefer|always|never|do not|must|show|ask|confirm)\b", statement, re.IGNORECASE):
            hints.append(statement)
    return hints[:5]


def prune_stale_recent_items(items: list[dict[str, object]]) -> list[dict[str, object]]:
    latest_recent_by_project: dict[str, str] = {}
    for item in items:
        if str(item.get("memory_class")) != "recent_project_state":
            continue
        project = str(item.get("project") or "")
        last_seen_at = str(item.get("last_seen_at") or "")
        if last_seen_at and last_seen_at > latest_recent_by_project.get(project, ""):
            latest_recent_by_project[project] = last_seen_at
    return [
        item
        for item in items
        if str(item.get("memory_class")) != "recent_project_state"
        or (
            str(item.get("last_seen_at") or "") == latest_recent_by_project.get(str(item.get("project") or ""), "")
            or (
                str(item.get("temporal_status") or "active") == "active"
                and not is_older_than_days(item.get("last_seen_at"), RECENT_MEMORY_MAX_DAYS)
            )
        )
    ]


def normalize_memory_item_roles(items: list[dict[str, object]]) -> list[dict[str, object]]:
    normalized: list[dict[str, object]] = []
    for item in items:
        item = dict(item)
        role = item_role(item)
        item["memory_role"] = role
        if role == "rule" and item.get("project") and item.get("memory_class") != "global_user_rules":
            item["memory_class"] = "project_rules"
            item["item_type"] = "project_rule"
            item["scope"] = "project"
            item["durability"] = "durable"
            item["temporal_status"] = "durable"
        elif role == "purpose" and item.get("memory_class") == "stable_project_summary":
            item["item_type"] = "purpose"
        elif role == "architecture" and item.get("memory_class") == "stable_project_summary":
            item["item_type"] = "architecture"
        elif role == "constraint" and item.get("memory_class") == "stable_project_summary":
            item["item_type"] = "constraint"
        normalized.append(item)
    return normalized


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
    role = item_role(item)
    if role == "discard":
        return None
    if role == "rule" and item.get("project") and memory_class != "global_user_rules":
        return "project_rules"
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
        if clause.lower().startswith(MEMORY_COMMAND_PREFIX):
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
        if clause.lower() in {"sessionmemory", "why this exists", "end-to-end pipeline"}:
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
