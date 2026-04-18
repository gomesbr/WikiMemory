from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .discovery import DiscoveryError, atomic_write_text, ensure_directory, utc_now
from .memory_generation import slugify
from .normalization import append_jsonl_text
from .product_config import load_product_config

STATE_SCHEMA_VERSION = 1
AGENT_BOOTSTRAP_SCHEMA_VERSION = 1


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
        if config.agent_platform.bootstrap_renderer != "codex_agents_md":
            raise AgentBootstrapError(
                f"Unsupported agent bootstrap renderer: {config.agent_platform.bootstrap_renderer}"
            )
        target_path = resolve_target_path(output_path, config.environment.repo_root, config.agent_platform.bootstrap_target_path)
        items = load_memory_items(memory_dir, project_filter)
        markdown, selected_item_count = render_codex_agents_md(items)
        ensure_directory(target_path.parent)
        atomic_write_text(target_path, markdown)

        state_payload = {
            "schema_version": STATE_SCHEMA_VERSION,
            "agent_bootstrap_schema_version": AGENT_BOOTSTRAP_SCHEMA_VERSION,
            "last_run_id": run_id,
            "last_rendered_at": utc_now(),
            "target_path": str(target_path),
            "selected_item_count": selected_item_count,
            "rendered_char_count": len(markdown),
        }
        atomic_write_text(state_path, json.dumps(state_payload, indent=2))
        finished_at = utc_now()
        report = AgentBootstrapRunReport(
            run_id=run_id,
            started_at=started_at,
            finished_at=finished_at,
            target_path=str(target_path),
            selected_item_count=selected_item_count,
            rendered_char_count=len(markdown),
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


def render_codex_agents_md(items: list[dict[str, object]]) -> tuple[str, int]:
    grouped: defaultdict[str, list[dict[str, object]]] = defaultdict(list)
    projects = sorted({str(item.get("project")) for item in items if item.get("project")})
    for item in sorted(items, key=bootstrap_sort_key):
        grouped[str(item["memory_class"])].append(item)

    lines = [
        "# Agent Bootstrap",
        "",
        "This file is generated by WikiMemory from compact derived memory. Treat linked memory files as the source of truth for details.",
        "",
        "## Read First",
        "",
        "- `memory/global/user-rules.md` for durable user-wide rules.",
    ]
    for project in projects[:8]:
        lines.append(
            f"- `memory/projects/{project}/project.md`, `memory/projects/{project}/rules.md`, "
            f"and `memory/projects/{project}/recent.md` for `{project}`."
        )

    selected_item_count = append_section(lines, "Global Rules", grouped["global_user_rules"], 8)
    for project in projects[:8]:
        project_rules = [item for item in grouped["project_rules"] if item.get("project") == project]
        project_lessons = [item for item in grouped["project_lessons"] if item.get("project") == project]
        selected_item_count += append_section(lines, f"{project} Rules", project_rules, 6)
        selected_item_count += append_section(lines, f"{project} Lessons", project_lessons, 3)

    lines.extend(
        [
            "## Operating Rule",
            "",
            "- Keep this bootstrap tiny. Load the referenced memory files when the task needs detail.",
            "",
        ]
    )
    return "\n".join(lines), selected_item_count


def append_section(lines: list[str], title: str, items: list[dict[str, object]], cap: int) -> int:
    if not items:
        return 0
    lines.extend(["", f"## {title}", ""])
    for item in items[:cap]:
        statement = str(item["statement"]).replace("\n", " ").strip()
        lines.append(f"- {statement}")
    return min(len(items), cap)


def bootstrap_sort_key(item: dict[str, object]) -> tuple[int, int, str]:
    confidence_rank = {"explicit": 0, "strong": 1, "candidate": 2}.get(str(item.get("confidence")), 3)
    promotion_rank = {"explicit": 0, "durable": 1, "repeated": 2, "candidate": 3}.get(
        str(item.get("promotion_state")), 4
    )
    return confidence_rank, promotion_rank, str(item.get("statement", ""))
