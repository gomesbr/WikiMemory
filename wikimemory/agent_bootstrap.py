from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable

from .discovery import DiscoveryError, atomic_write_text, ensure_directory, utc_now
from .memory_generation import slugify
from .normalization import append_jsonl_text
from .product_config import load_product_config

STATE_SCHEMA_VERSION = 1
AGENT_BOOTSTRAP_SCHEMA_VERSION = 1
BOOTSTRAP_BLOCK_START = "<!-- WIKIMEMORY:START -->"
BOOTSTRAP_BLOCK_END = "<!-- WIKIMEMORY:END -->"
BRAIN = "\U0001f9e0"


class AgentBootstrapError(DiscoveryError):
    """Fatal memory-backed agent bootstrap error."""


@dataclass(frozen=True)
class AgentBootstrapRunReport:
    run_id: str
    started_at: str
    finished_at: str
    target_path: str
    selected_item_count: int
    rendered_char_count: int
    success: bool
    fatal_error_summary: str | None

    def to_dict(self) -> dict[str, object]:
        return {
            "run_id": self.run_id,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "target_path": self.target_path,
            "selected_item_count": self.selected_item_count,
            "rendered_char_count": self.rendered_char_count,
            "success": self.success,
            "fatal_error_summary": self.fatal_error_summary,
        }


@dataclass(frozen=True)
class AgentBootstrapResult:
    report: AgentBootstrapRunReport
    target_path: Path
    state_path: Path
    run_log_path: Path
    notice_log_path: Path


def run_agent_bootstrap(
    product_config_path: Path | str,
    state_dir: Path | str,
    memory_dir: Path | str,
    audits_dir: Path | str,
    output_path: Path | str | None = None,
    projects: Iterable[str] | None = None,
) -> AgentBootstrapResult:
    product_config_path = Path(product_config_path)
    state_dir = Path(state_dir)
    memory_dir = Path(memory_dir)
    audits_dir = Path(audits_dir)
    project_filter = {slugify(project) for project in projects or []}
    run_id = f"agent-bootstrap-{utc_now().replace(':', '').replace('.', '').replace('-', '')}"
    started_at = utc_now()
    state_path = state_dir / "agent_bootstrap_state.json"
    run_log_path = state_dir / "agent_bootstrap_runs.jsonl"
    notice_log_path = audits_dir / "agent_bootstrap_notices.jsonl"

    ensure_directory(state_dir)
    ensure_directory(audits_dir)

    previous_run_log = run_log_path.read_text(encoding="utf-8") if run_log_path.exists() else ""
    previous_notice_log = notice_log_path.read_text(encoding="utf-8") if notice_log_path.exists() else ""
    target_path = Path(output_path) if output_path is not None else Path("AGENTS.md")

    try:
        config = load_product_config(product_config_path)
        target_path = resolve_target_path(output_path, config.environment.repo_root, config.agent_platform.bootstrap_target_path)
        freshness_path = write_memory_freshness_page(memory_dir, state_dir)
        items = load_memory_items(memory_dir, project_filter)
        markdown, selected_item_count = render_agent_bootstrap(items, config.agent_platform.bootstrap_renderer, memory_dir=memory_dir, state_dir=state_dir, freshness_path=freshness_path)
        ensure_directory(target_path.parent)
        final_markdown = append_or_update_managed_block(target_path, markdown)
        atomic_write_text(target_path, final_markdown)

        state_payload = {
            "schema_version": STATE_SCHEMA_VERSION,
            "agent_bootstrap_schema_version": AGENT_BOOTSTRAP_SCHEMA_VERSION,
            "last_run_id": run_id,
            "last_rendered_at": utc_now(),
            "target_path": str(target_path),
            "selected_item_count": selected_item_count,
            "rendered_char_count": len(final_markdown),
        }
        atomic_write_text(state_path, json.dumps(state_payload, indent=2))
        finished_at = utc_now()
        report = AgentBootstrapRunReport(
            run_id=run_id,
            started_at=started_at,
            finished_at=finished_at,
            target_path=str(target_path),
            selected_item_count=selected_item_count,
            rendered_char_count=len(final_markdown),
            success=True,
            fatal_error_summary=None,
        )
        atomic_write_text(run_log_path, append_jsonl_text(previous_run_log, [report.to_dict()]))
        atomic_write_text(notice_log_path, append_jsonl_text(previous_notice_log, []))
        return AgentBootstrapResult(report, target_path, state_path, run_log_path, notice_log_path)
    except Exception as exc:
        finished_at = utc_now()
        report = AgentBootstrapRunReport(
            run_id=run_id,
            started_at=started_at,
            finished_at=finished_at,
            target_path=str(target_path),
            selected_item_count=0,
            rendered_char_count=0,
            success=False,
            fatal_error_summary=str(exc),
        )
        atomic_write_text(run_log_path, append_jsonl_text(previous_run_log, [report.to_dict()]))
        return AgentBootstrapResult(report, target_path, state_path, run_log_path, notice_log_path)


def resolve_target_path(output_path: Path | str | None, repo_root: str, configured_target: str) -> Path:
    target = Path(output_path) if output_path is not None else Path(configured_target)
    if target.is_absolute():
        return target
    return Path(repo_root).expanduser().resolve() / target


def load_memory_items(memory_dir: Path, project_filter: set[str]) -> list[dict[str, object]]:
    items_path = memory_dir / "_meta" / "items.jsonl"
    if not items_path.exists():
        raise AgentBootstrapError(f"Missing memory item manifest: {items_path}")
    items = [json.loads(line) for line in items_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not project_filter:
        return items
    return [
        item
        for item in items
        if str(item.get("scope")) == "global" or slugify(str(item.get("project") or "")) in project_filter
    ]


def render_agent_bootstrap(items: list[dict[str, object]], renderer: str, *, memory_dir: Path, state_dir: Path, freshness_path: Path) -> tuple[str, int]:
    if renderer == "codex_agents_md":
        return render_bootstrap_markdown(items, "Codex", memory_dir=memory_dir, state_dir=state_dir, freshness_path=freshness_path)
    if renderer == "claude_md":
        return render_bootstrap_markdown(items, "Claude", memory_dir=memory_dir, state_dir=state_dir, freshness_path=freshness_path)
    if renderer == "generic_bootstrap_md":
        return render_bootstrap_markdown(items, "agent", memory_dir=memory_dir, state_dir=state_dir, freshness_path=freshness_path)
    raise AgentBootstrapError(f"Unsupported agent bootstrap renderer: {renderer}")


def append_or_update_managed_block(target_path: Path, generated_markdown: str) -> str:
    managed_block = f"{BOOTSTRAP_BLOCK_START}\n{generated_markdown.strip()}\n{BOOTSTRAP_BLOCK_END}\n"
    if not target_path.exists():
        return managed_block
    existing = target_path.read_text(encoding="utf-8")
    start_index = existing.find(BOOTSTRAP_BLOCK_START)
    end_index = existing.find(BOOTSTRAP_BLOCK_END)
    if start_index != -1 and end_index != -1 and end_index > start_index:
        end_index += len(BOOTSTRAP_BLOCK_END)
        return existing[:start_index].rstrip() + "\n\n" + managed_block + existing[end_index:].lstrip()
    return existing.rstrip() + "\n\n" + managed_block


def render_codex_agents_md(items: list[dict[str, object]]) -> tuple[str, int]:
    return render_bootstrap_markdown(items, "Codex", memory_dir=Path("memory"), state_dir=Path("state"), freshness_path=Path("memory/global/memory-freshness.md"))


def render_bootstrap_markdown(items: list[dict[str, object]], agent_label: str, *, memory_dir: Path, state_dir: Path, freshness_path: Path) -> tuple[str, int]:
    projects = sorted({str(item.get("project")) for item in items if item.get("project")})
    style_config_path = memory_dir / "_meta" / "consumer_style.json"
    freshness_summary = bootstrap_freshness_summary(state_dir)
    lines = [
        f"# {BRAIN} Agent Memory Index",
        "",
        f"Generated WikiMemory entry map for {agent_label}. Keep user-written content outside the managed block.",
        "",
        "## Startup behavior",
        "",
        "- The first line of the first real reply must explicitly reassure the user that the needed memory is already loaded here.",
        "- Use this exact first line: `Your workspace memory is already loaded here.`",
        "- Start new chats with a calm direct opener, but do not mention internal memory artifacts such as consumer-profile, rules files, or page names in the first message.",
        "- Phrase the opener in the user's style using ./memory/global/user-rules.md and ./memory/global/consumer-profile.md.",
        "- The first message must state exactly how old the latest durable workspace memory is using both relative time and absolute time.",
        "- A good first-line pattern is: `Your workspace memory is already loaded here.`",
        "- The next line can say: `Latest durable workspace memory update: about <relative-age> ago (<absolute-time>).`",
        "- Ask whether the user wants to continue an existing project or start a new one before loading project-specific work.",
        "- Mention that if work happened in another chat after that timestamp, you can provide a copy/paste prompt to pull only the missing newer context into this chat.",
        "- If asked for that handoff prompt, write it as a prompt addressed to the other chat, not to the user here.",
        "- The handoff prompt must be copy/paste ready with no brackets, no placeholders, and no fields for the user to fill in manually.",
        "- The handoff prompt must ask the other chat to summarize only what changed after the stated timestamp, without mentioning durable memory, workspace memory, or this system's internal storage model.",
        "- If the user selects a project, send a follow-up summary of that project's direction, backlog, preferences, recent context, and lessons.",
        "- Treat backlog and open threads as options only; never assume the next task or start work until the user chooses a direction.",
        "- Interpret page roles explicitly: directive = follow, preference = adapt tone/work style to, descriptive = use for context, guidance = use as heuristic guidance unless contradicted by directives or the user.",
        "- If the user asks to do something that conflicts with saved rules, name the conflicting page/rule and ask whether it is a one-off exception or a memory change.",
        '- For durable rule changes, ask the user to confirm with a single line starting with `Memory command:` such as `Memory command: add global rule: ...`, `Memory command: add project rule: ...`, `Memory command: replace rule: "old" -> "new"`, or `Memory command: remove rule: "..."`.',
        "",
        "## Freshness",
        "",
        f"- Latest durable refresh: {freshness_summary['last_refresh_at']}.",
        f"- Relative age: {freshness_summary['last_refresh_age']}.",
        f"- Layer status: {freshness_summary['layer_summary']}.",
        f"- Detailed freshness page: ./{freshness_path.relative_to(memory_dir.parent).as_posix()}",
        "",
        "## Read on startup:",
        "",
        "1. Global rules:",
        "   -> ./memory/global/user-rules.md",
        "   -> ./memory/global/consumer-profile.md",
        f"   -> ./{style_config_path.relative_to(memory_dir.parent).as_posix()}",
        f"   -> ./{freshness_path.relative_to(memory_dir.parent).as_posix()}",
        "   -> ./memory/global/memory-health.md",
        "   -> ./memory/global/memory-change-log.md",
        "   -> ./memory/global/active-exceptions.md",
        "",
        "2. Do not load any project-specific pages until the user picks a project.",
        "",
        "Available projects:",
    ]
    for project in projects[:8]:
        lines.append(f"   - {project}")
    lines.extend(
        [
        "",
        "Project routing rule:",
        "- If the user refers to a project indirectly, approximately, or by description instead of exact name, map it to the closest matching available project before loading project pages.",
        "- Ask one short clarification only if multiple projects are plausible or the match is weak.",
        "",
        "## After project selection, load in order:",
        "",
        "1. Project memory:",
        "   -> ./memory/projects/<selected-project>/project.md",
        "",
        "2. Recent context (highest priority):",
        "   -> ./memory/projects/<selected-project>/recent.md",
        "   -> ./memory/projects/<selected-project>/continuations.md",
        "",
        "3. Project rules:",
        "   -> ./memory/projects/<selected-project>/rules.md",
        "",
        "4. Project lessons:",
        "   -> ./memory/projects/<selected-project>/lessons.md",
        "",
        "5. Daily conversation pages:",
        "   -> ./memory/daily-conversations/YYYY-MM-DD.md",
        "   -> Never load these by default.",
        "   -> Only read them if the user explicitly asks for a daily conversation history page or asks to inspect a specific date.",
        ]
    )

    lines.extend(
        [
            "",
            "## Instructions",
            "",
            "- Treat these files as source of truth.",
            "- user-rules.md and project rules.md contain directive agent behavior; follow them.",
        "- consumer-profile.md contains inferred preferences; mirror style and workflow without presenting them as hard rules.",
            "- project.md and recent.md provide state/context; summarize them, but do not treat them as authorization to act.",
            "- lessons.md contains reusable heuristics; apply them when relevant, but let directives and current user requests win.",
            "- consumer_style.json is a compiled style config; use it to keep bootstrap phrasing and follow-up tone aligned with the user.",
            "- Prefer recent.md for current direction after the user picks a project.",
            "- Never read daily conversation pages unless the user explicitly asks for them.",
            "- Do not infer durable rules from one-off instructions.",
            "- Do not auto-resume saved backlog items without explicit confirmation from the user.",
        "- User-confirmed `Memory command:` lines are authoritative memory edits and should be preserved as explicit overrides.",
            "- Keep this bootstrap tiny; load linked memory files for detail.",
            "",
        ]
    )
    return "\n".join(lines), 7


def write_memory_freshness_page(memory_dir: Path, state_dir: Path) -> Path:
    path = memory_dir / "global" / "memory-freshness.md"
    ensure_directory(path.parent)
    summary = bootstrap_freshness_summary(state_dir)
    lines = [
        "---",
        "type: memory-freshness",
        f"updated: {utc_now()}",
        "memory_role: descriptive",
        "tags: [memory, freshness, global]",
        "---",
        "",
        "# Memory Freshness",
        "",
        f"- Latest durable refresh: {summary['last_refresh_at']}",
        f"- Layer status: {summary['layer_summary']}",
        f"- Global memory: {summary['memory_at']}",
        f"- Consumer profile: {summary['consumer_profile_at']}",
        f"- Agent bootstrap: {summary['bootstrap_at']}",
        "",
    ]
    atomic_write_text(path, "\n".join(lines))
    return path


def bootstrap_freshness_summary(state_dir: Path) -> dict[str, str]:
    refresh_state = load_json(state_dir / "memory_refresh_state.json")
    memory_state = load_json(state_dir / "memory_state.json")
    profile_state = load_json(state_dir / "consumer_profile_state.json")
    bootstrap_state = load_json(state_dir / "agent_bootstrap_state.json")
    last_refresh_at = str(refresh_state.get("last_successful_refresh_finished_at") or "") or latest_successful_finished_at(
        state_dir / "memory_refresh_runs.jsonl"
    ) or "unknown"
    memory_at = str(memory_state.get("last_rendered_at") or "unknown")
    consumer_profile_at = str(profile_state.get("last_profiled_at") or "unknown")
    bootstrap_at = str(bootstrap_state.get("last_rendered_at") or "unknown")
    layer_summary = ", ".join(
        [
            f"memory={freshness_label(memory_at)}",
            f"profile={freshness_label(consumer_profile_at)}",
            f"bootstrap={freshness_label(bootstrap_at)}",
        ]
    )
    return {
        "last_refresh_at": last_refresh_at,
        "last_refresh_age": relative_age(last_refresh_at),
        "memory_at": memory_at,
        "consumer_profile_at": consumer_profile_at,
        "bootstrap_at": bootstrap_at,
        "layer_summary": layer_summary,
    }


def freshness_label(value: str) -> str:
    if not value or value == "unknown":
        return "unknown"
    try:
        age = datetime.now(timezone.utc) - datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return "unknown"
    if age < timedelta(hours=6):
        return "fresh"
    if age < timedelta(hours=48):
        return "aging"
    return "stale"


def relative_age(value: str) -> str:
    if not value or value == "unknown":
        return "unknown"
    try:
        age = datetime.now(timezone.utc) - datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return "unknown"
    if age < timedelta(minutes=1):
        return "less than a minute"
    if age < timedelta(hours=1):
        minutes = max(1, int(age.total_seconds() // 60))
        return f"{minutes} minute{'s' if minutes != 1 else ''}"
    if age < timedelta(days=1):
        hours = max(1, int(age.total_seconds() // 3600))
        return f"{hours} hour{'s' if hours != 1 else ''}"
    days = max(1, age.days)
    if days < 14:
        return f"{days} day{'s' if days != 1 else ''}"
    weeks = max(1, days // 7)
    return f"{weeks} week{'s' if weeks != 1 else ''}"


def latest_successful_finished_at(path: Path) -> str | None:
    if not path.exists():
        return None
    latest = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        payload = json.loads(line)
        if not payload.get("success"):
            continue
        finished_at = str(payload.get("finished_at") or "")
        if finished_at > latest:
            latest = finished_at
    return latest or None


def load_json(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8-sig"))
