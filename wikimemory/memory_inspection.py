from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .discovery import DiscoveryError


class MemoryInspectionError(DiscoveryError):
    """Fatal memory-inspection error."""


@dataclass(frozen=True)
class MemoryInspectionReport:
    action: str
    match_count: int
    success: bool
    fatal_error_summary: str | None

    def to_dict(self) -> dict[str, object]:
        return {
            "action": self.action,
            "match_count": self.match_count,
            "success": self.success,
            "fatal_error_summary": self.fatal_error_summary,
        }


@dataclass(frozen=True)
class MemoryInspectionResult:
    report: MemoryInspectionReport
    payload: dict[str, object]


def run_memory_inspection(
    *,
    action: str,
    memory_dir: Path | str,
    state_dir: Path | str,
    project: str | None = None,
    rule_query: str | None = None,
) -> MemoryInspectionResult:
    memory_dir = Path(memory_dir)
    state_dir = Path(state_dir)
    try:
        items = load_items(memory_dir)
        overrides = load_override_state(state_dir)
        if action == "active-rules":
            payload = inspect_active_rules(items)
        elif action == "project-rules":
            payload = inspect_project_rules(items, project)
        elif action == "why-rule":
            payload = inspect_why_rule(items, rule_query)
        elif action == "recent-changes":
            payload = inspect_recent_changes(overrides)
        elif action == "freshness":
            payload = load_json(memory_dir / "global" / "memory-freshness.md")
        elif action == "health":
            payload = load_json(memory_dir / "_meta" / "memory_health.json")
        elif action == "continuations":
            payload = inspect_continuations(memory_dir, project)
        else:
            raise MemoryInspectionError(f"Unsupported inspection action: {action}")
        match_count = int(payload.get("match_count", len(payload.get("items", [])) if isinstance(payload.get("items"), list) else 1))
        return MemoryInspectionResult(MemoryInspectionReport(action=action, match_count=match_count, success=True, fatal_error_summary=None), payload)
    except Exception as exc:
        return MemoryInspectionResult(
            MemoryInspectionReport(action=action, match_count=0, success=False, fatal_error_summary=str(exc)),
            {"error": str(exc)},
        )


def inspect_active_rules(items: list[dict[str, object]]) -> dict[str, object]:
    rules = [item for item in items if str(item.get("memory_role") or "") == "rule"]
    return {
        "items": [
            {
                "scope": item.get("scope"),
                "project": item.get("project"),
                "statement": item.get("statement"),
                "authority": item.get("authority") or "memory",
                "locked_by_consumer": bool(item.get("locked_by_consumer")),
            }
            for item in sorted(rules, key=lambda item: (str(item.get("scope") or ""), str(item.get("project") or ""), str(item.get("statement") or "")))
        ],
        "match_count": len(rules),
    }


def inspect_project_rules(items: list[dict[str, object]], project: str | None) -> dict[str, object]:
    if not project:
        raise MemoryInspectionError("project is required for project-rules")
    selected = [
        item
        for item in items
        if str(item.get("memory_role") or "") == "rule" and str(item.get("project") or "") == project
    ]
    return {
        "project": project,
        "items": [
            {
                "statement": item.get("statement"),
                "authority": item.get("authority") or "memory",
                "locked_by_consumer": bool(item.get("locked_by_consumer")),
            }
            for item in selected
        ],
        "match_count": len(selected),
    }


def inspect_why_rule(items: list[dict[str, object]], rule_query: str | None) -> dict[str, object]:
    if not rule_query:
        raise MemoryInspectionError("rule_query is required for why-rule")
    query = rule_query.lower()
    matches = [
        item
        for item in items
        if str(item.get("memory_role") or "") == "rule" and query in str(item.get("statement") or "").lower()
    ]
    if not matches:
        raise MemoryInspectionError(f"No rule matched query: {rule_query}")
    item = matches[0]
    return {
        "statement": item.get("statement"),
        "scope": item.get("scope"),
        "project": item.get("project"),
        "authority": item.get("authority") or "memory",
        "locked_by_consumer": bool(item.get("locked_by_consumer")),
        "evidence_ids": list(item.get("evidence_ids", [])),
        "provenance_refs": list(item.get("provenance_refs", [])),
        "match_count": 1,
    }


def inspect_recent_changes(overrides: dict[str, object]) -> dict[str, object]:
    commands = [command for command in overrides.get("commands", []) if isinstance(command, dict)]
    commands.sort(key=lambda item: str(item.get("timestamp") or ""), reverse=True)
    return {"items": commands[:20], "match_count": len(commands[:20])}


def inspect_continuations(memory_dir: Path, project: str | None) -> dict[str, object]:
    if not project:
        raise MemoryInspectionError("project is required for continuations")
    path = memory_dir / "projects" / project / "continuations.md"
    if not path.exists():
        raise MemoryInspectionError(f"Missing continuations page for project: {project}")
    return {"project": project, "path": str(path), "content": path.read_text(encoding="utf-8"), "match_count": 1}


def load_items(memory_dir: Path) -> list[dict[str, object]]:
    path = memory_dir / "_meta" / "items.jsonl"
    if not path.exists():
        raise MemoryInspectionError(f"Missing memory item manifest: {path}")
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_override_state(state_dir: Path) -> dict[str, object]:
    return load_json(state_dir / "memory_rule_overrides.json")


def load_json(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8-sig")
    if path.suffix == ".md":
        return {"content": text}
    return json.loads(text)
