from __future__ import annotations

import hashlib
import json
import re
import shutil
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .discovery import DiscoveryError, atomic_write_text, ensure_directory, utc_now
from .memory_model import MEMORY_FILE_DEFINITIONS
from .normalization import append_jsonl_text
from .product_config import load_product_config

STATE_SCHEMA_VERSION = 1
MEMORY_SCHEMA_VERSION = 1
USER_RULE_PATTERN = re.compile(r"\b(?:add this to global rules|global rule)\b", re.IGNORECASE)
PROJECT_RULE_PATTERN = re.compile(
    r"^(?:add this to project rules:?|project rule:?|for this project,?|always\b|never\b|do not\b|don't\b|must\b|nothing\b.*\bshould\b|the .{0,80}\balways\b)",
    re.IGNORECASE,
)
LESSON_PATTERN = re.compile(r"\b(?:lesson learned|next time|avoid repeating|root cause|postmortem)\b", re.IGNORECASE)
ONE_OFF_PATTERN = re.compile(r"\b(?:please|can you|do this|fix this|run this|open this|show me|what|why|how)\b", re.IGNORECASE)
SCAFFOLD_PATTERN = re.compile(
    r"(?:please implement this plan|context from my ide setup|open tabs:|<permissions instructions>|</permissions instructions>|<collaboration_mode>|</collaboration_mode>)",
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
        memory_items = build_memory_items(evidence_records, project_filter)
        rendered_files = render_memory_files(memory_dir, memory_items, config.markdown_output.mode)
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


def build_memory_items(records: list[dict[str, object]], project_filter: set[str]) -> list[dict[str, object]]:
    items: dict[str, dict[str, object]] = {}
    for record in records:
        project = slugify(str(record.get("project_hint") or record.get("source_id") or "project"))
        if project_filter and project not in project_filter:
            continue
        actor_type = str(record.get("actor_type") or "")
        text = evidence_text(record)
        if not text:
            continue
        candidates = classify_evidence(record, text, actor_type, project)
        for candidate in candidates:
            if not str(candidate.get("statement") or "").strip():
                continue
            item_id = candidate["item_id"]
            if item_id not in items:
                items[item_id] = candidate
            else:
                merge_item(items[item_id], candidate)
    return sorted(items.values(), key=lambda item: (str(item["scope"]), str(item.get("project") or ""), str(item["memory_class"]), str(item["statement"])))


def classify_evidence(record: dict[str, object], text: str, actor_type: str, project: str) -> list[dict[str, object]]:
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
            items.append(make_item(record, "global_user_rules", "global", None, "durable", promotion_state(clause), clause))
            durable_found = True
        elif is_project_rule_text(clause):
            items.append(make_item(record, "project_rules", "project", project, "durable", promotion_state(clause), clause))
            durable_found = True
        elif LESSON_PATTERN.search(clause):
            items.append(make_item(record, "project_lessons", "project", project, "durable", "candidate", clause))
            durable_found = True
    if actor_type == "user" and not durable_found:
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
    elif len(target["evidence_ids"]) > 1 and target["promotion_state"] == "candidate":
        target["promotion_state"] = "repeated"
        target["confidence"] = "strong"


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


def render_memory_files(memory_dir: Path, items: list[dict[str, object]], markdown_mode: str) -> list[Path]:
    clear_generated_memory_tree(memory_dir)
    grouped: defaultdict[str, list[dict[str, object]]] = defaultdict(list)
    for item in items:
        key = memory_file_key(item)
        if key:
            grouped[key].append(item)

    rendered: list[Path] = []
    global_target = memory_dir / memory_relative_path("global_user_rules")
    render_file(global_target, "Global User Rules", grouped["global_user_rules"], markdown_mode)
    rendered.append(global_target)

    projects = sorted({str(item["project"]) for item in items if item.get("project")})
    for project in projects:
        for key in ("project_summary", "project_recent", "project_rules", "project_lessons"):
            definition = MEMORY_FILE_DEFINITIONS[key]
            project_items = [item for item in grouped[key] if item.get("project") == project]
            if definition.optional and not project_items:
                continue
            target = memory_dir / memory_relative_path(key, project)
            render_file(target, title_for_memory_file(key, project), project_items, markdown_mode)
            rendered.append(target)
    return rendered


def clear_generated_memory_tree(memory_dir: Path) -> None:
    for child_name in ("global", "projects", "_meta"):
        target = memory_dir / child_name
        if target.exists():
            shutil.rmtree(target)


def render_file(path: Path, title: str, items: list[dict[str, object]], markdown_mode: str) -> None:
    ensure_directory(path.parent)
    lines: list[str] = []
    if markdown_mode == "obsidian_markdown":
        lines.extend(["---", f'title: "{title}"', "tags:", "  - wikimemory", "  - memory", "---", ""])
    lines.append(f"# {title}")
    lines.append("")
    if not items:
        lines.append("- No high-signal memory selected yet.")
    else:
        for item in items[:80]:
            marker = str(item["promotion_state"])
            lines.append(f"- [{marker}] {item['statement']} <!-- {item['item_id']} -->")
    lines.append("")
    atomic_write_text(path, "\n".join(lines))


def write_meta(memory_dir: Path, items: list[dict[str, object]]) -> None:
    meta_dir = memory_dir / "_meta"
    ensure_directory(meta_dir)
    content = "".join(json.dumps(item, sort_keys=True, separators=(",", ":")) + "\n" for item in items)
    atomic_write_text(meta_dir / "items.jsonl", content)


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
        return [normalize_statement(extract_request_text(text))]
    text = extract_request_text(text)
    text = re.sub(r"<image>\s*</image>|<image>|</image>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"^\s*[-*]\s+", "", text, flags=re.MULTILINE)
    raw_parts = re.split(r"(?:\r?\n|;|(?<=[.!?])\s+)", text)
    clauses: list[str] = []
    for part in raw_parts:
        clause = normalize_statement(part.strip(" -\t\r\n"))
        if not clause or len(clause) < 8:
            continue
        if clause.startswith("#") or clause.lower().startswith(("open tabs", "active file")):
            continue
        clauses.append(clause)
    return clauses[:8]


def extract_request_text(text: str) -> str:
    marker = "My request for Codex:"
    if marker in text:
        return text.split(marker)[-1].strip()
    return text.strip()


def is_global_rule_text(text: str) -> bool:
    return bool(USER_RULE_PATTERN.search(text)) and ("global rule" in text.lower() or "add this to global rules" in text.lower())


def is_project_rule_text(text: str) -> bool:
    if len(text) > 260:
        return False
    if SCAFFOLD_PATTERN.search(text):
        return False
    if ONE_OFF_PATTERN.search(text) and not re.search(r"\b(?:always|never|do not|don't|must)\b", text, re.IGNORECASE):
        return False
    return bool(PROJECT_RULE_PATTERN.search(text))


def promotion_state(text: str) -> str:
    lowered = text.lower()
    if "add this to global rules" in lowered or "add this to project rules" in lowered:
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
