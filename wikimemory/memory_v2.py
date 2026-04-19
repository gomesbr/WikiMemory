from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import time
import urllib.error
import urllib.request
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable

from .discovery import DiscoveryError, atomic_write_text, ensure_directory, utc_now
from .normalization import append_jsonl_text

MEMORY_V2_SCHEMA_VERSION = 1
MEMORY_V2_EXTRACTION_VERSION = 1
DEFAULT_MODEL = "gpt-5.3-codex"
DEFAULT_WINDOW_MAX_CHARS = 60000
DEFAULT_WINDOW_OVERLAP_MESSAGES = 8
DEFAULT_PROJECT_README_MAX_CHARS = 4000
DEFAULT_PROJECT_TREE_DEPTH = 2
DEFAULT_PROJECT_TREE_MAX_ENTRIES = 80
ALLOWED_CLASSES = {
    "global_rule",
    "project_rule",
    "project_summary",
    "architecture",
    "current_state",
    "decision",
    "next_step",
    "open_question",
    "failure_risk",
    "lesson",
}
ALLOWED_ROLES = {"purpose", "architecture", "constraint", "rule", "recent_state", "decision", "lesson", "discard"}
ALLOWED_CONFIDENCE = {"explicit", "strong", "medium", "low"}
ALLOWED_TEMPORAL = {"active", "historical", "resolved", "superseded", "durable"}
PROJECT_SLUGS = {"global", "ai-trader", "open-brain", "ai-scientist", "codexclaw", "wikimemory", "cross-project", "unknown"}
PROJECT_DIRECTORY_ALIASES = {
    "ai-trader": ("AITrader", "ai-trader"),
    "open-brain": ("OpenBrain", "open-brain"),
    "ai-scientist": ("AIScientist", "ai-scientist"),
    "codexclaw": ("CodexClaw", "codexclaw"),
    "wikimemory": ("WikiMemory", "wikimemory"),
}
TREE_EXCLUDED_DIRS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
}

LlmClient = Callable[[str, dict[str, object], str], dict[str, object]]


class MemoryV2Error(DiscoveryError):
    """Fatal memory-v2 error."""


@dataclass(frozen=True)
class ChatMessage:
    message_index: int
    timestamp: str
    actor: str
    text: str
    source_day: str
    source_file: str
    source_ref: str | None

    def to_llm_dict(self) -> dict[str, object]:
        return {
            "message_index": self.message_index,
            "timestamp": self.timestamp,
            "actor": self.actor,
            "text": self.text,
        }

    def to_meta_dict(self) -> dict[str, object]:
        return {
            "message_index": self.message_index,
            "timestamp": self.timestamp,
            "actor": self.actor,
            "text": self.text,
            "source_day": self.source_day,
            "source_file": self.source_file,
            "source_ref": self.source_ref,
        }


@dataclass(frozen=True)
class MemoryV2Report:
    run_id: str
    started_at: str
    finished_at: str
    model: str
    output_dir: str
    day_count: int
    message_count: int
    candidate_count: int
    item_count: int
    rendered_file_count: int
    success: bool
    fatal_error_summary: str | None

    def to_dict(self) -> dict[str, object]:
        return {
            "run_id": self.run_id,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "model": self.model,
            "output_dir": self.output_dir,
            "day_count": self.day_count,
            "message_count": self.message_count,
            "candidate_count": self.candidate_count,
            "item_count": self.item_count,
            "rendered_file_count": self.rendered_file_count,
            "success": self.success,
            "fatal_error_summary": self.fatal_error_summary,
        }


@dataclass(frozen=True)
class MemoryV2Result:
    report: MemoryV2Report
    output_dir: Path
    run_log_path: Path


def run_memory_v2(
    *,
    input_dir: Path | str,
    output_dir: Path | str,
    state_dir: Path | str,
    days: Iterable[str] | None = None,
    all_days: bool = False,
    model: str | None = None,
    project_root_dir: Path | str | None = None,
    llm_client: LlmClient | None = None,
) -> MemoryV2Result:
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    state_dir = Path(state_dir)
    started_at = utc_now()
    run_id = f"memory-v2-{started_at.replace(':', '').replace('.', '').replace('-', '')}"
    model_id = model or os.environ.get("WIKIMEMORY_MEMORY_V2_MODEL", "").strip() or DEFAULT_MODEL
    run_log_path = state_dir / "memory_v2_runs.jsonl"
    previous_run_log = run_log_path.read_text(encoding="utf-8") if run_log_path.exists() else ""
    ensure_directory(state_dir)
    daily_payloads: list[dict[str, object]] = []
    all_candidates: list[dict[str, object]] = []
    merged_payload: dict[str, object] | None = None

    try:
        day_files = resolve_day_files(input_dir, days=days, all_days=all_days)
        if not day_files:
            raise MemoryV2Error("No daily chat files selected. Use --day YYYY-MM-DD or --all-days.")
        prepare_memory_v2_output_dir(output_dir)

        message_count = 0
        for day_file in day_files:
            source_day = day_file.name[:10]
            cached_payload = read_cached_daily_payload(output_dir, source_day, day_file, model_id)
            if cached_payload:
                daily_payloads.append(cached_payload)
                all_candidates.extend([candidate for candidate in cached_payload.get("candidates", []) if isinstance(candidate, dict)])
                message_count += int(cached_payload.get("message_count", 0))
                continue
            messages = parse_daily_chat_markdown(day_file)
            message_count += len(messages)
            payload = extract_daily_candidates(source_day, day_file, messages, model_id, llm_client)
            candidates = []
            seen_candidate_ids: set[str] = set()
            for raw_index, raw_candidate in enumerate(payload.get("candidates", []), 1):
                if not isinstance(raw_candidate, dict):
                    continue
                candidate = normalize_candidate(raw_candidate, source_day)
                if not candidate["evidence_refs"]:
                    continue
                if candidate["candidate_id"] in seen_candidate_ids:
                    candidate["candidate_id"] = stable_id(source_day, raw_index, candidate["candidate_id"], candidate["agent_facing_statement"])
                seen_candidate_ids.add(str(candidate["candidate_id"]))
                candidates.append(candidate)
            candidates = assign_unknown_projects(candidates)
            daily_payloads.append(
                {
                    "schema_version": MEMORY_V2_SCHEMA_VERSION,
                    "extraction_version": MEMORY_V2_EXTRACTION_VERSION,
                    "model": model_id,
                    "source_day": source_day,
                    "source_file": str(day_file),
                    "source_mtime_ns": day_file.stat().st_mtime_ns,
                    "source_size": day_file.stat().st_size,
                    "message_count": len(messages),
                    "windows": payload.get("windows", []),
                    "messages": [message.to_meta_dict() for message in messages],
                    "candidates": candidates,
                }
            )
            write_daily_payload(output_dir, daily_payloads[-1])
            all_candidates.extend(candidates)

        project_contexts = collect_project_contexts(project_slugs_from_candidates(all_candidates), project_root_dir)
        candidate_lookup = {str(candidate.get("candidate_id")): candidate for candidate in all_candidates}
        merged_payload = merge_memory_candidates(all_candidates, model_id, llm_client, project_contexts=project_contexts)
        items = [normalize_item(item, candidate_lookup=candidate_lookup) for item in merged_payload.get("items", []) if isinstance(item, dict)]
        validate_items(items)
        rendered = render_memory_v2(output_dir, items, project_contexts=project_contexts)
        write_memory_v2_meta(output_dir, daily_payloads, items, project_contexts)

        report = MemoryV2Report(
            run_id=run_id,
            started_at=started_at,
            finished_at=utc_now(),
            model=model_id,
            output_dir=str(output_dir),
            day_count=len(day_files),
            message_count=message_count,
            candidate_count=len(all_candidates),
            item_count=len(items),
            rendered_file_count=len(rendered),
            success=True,
            fatal_error_summary=None,
        )
        atomic_write_text(run_log_path, append_jsonl_text(previous_run_log, [report.to_dict()]))
        return MemoryV2Result(report=report, output_dir=output_dir, run_log_path=run_log_path)
    except Exception as exc:
        write_memory_v2_failure_debug(output_dir, daily_payloads, all_candidates, merged_payload, str(exc))
        report = MemoryV2Report(
            run_id=run_id,
            started_at=started_at,
            finished_at=utc_now(),
            model=model_id,
            output_dir=str(output_dir),
            day_count=0,
            message_count=0,
            candidate_count=0,
            item_count=0,
            rendered_file_count=0,
            success=False,
            fatal_error_summary=str(exc),
        )
        atomic_write_text(run_log_path, append_jsonl_text(previous_run_log, [report.to_dict()]))
        return MemoryV2Result(report=report, output_dir=output_dir, run_log_path=run_log_path)


def resolve_day_files(input_dir: Path, *, days: Iterable[str] | None, all_days: bool) -> list[Path]:
    if all_days:
        return sorted(input_dir.glob("*-codex-chat.md"))
    selected = []
    for day in days or []:
        path = input_dir / f"{day}-codex-chat.md"
        if not path.exists():
            raise MemoryV2Error(f"Missing daily chat file: {path}")
        selected.append(path)
    return selected


def prepare_memory_v2_output_dir(output_dir: Path) -> None:
    ensure_directory(output_dir)
    for child_name in ("global", "projects"):
        child = output_dir / child_name
        if child.exists():
            shutil.rmtree(child)
    for meta_name in ("merged_items.json", "manifest.json"):
        meta_file = output_dir / "_meta" / meta_name
        if meta_file.exists():
            meta_file.unlink()


def read_cached_daily_payload(output_dir: Path, source_day: str, source_file: Path, model: str) -> dict[str, object] | None:
    path = output_dir / "_meta" / "daily" / f"{source_day}.json"
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    if payload.get("schema_version") != MEMORY_V2_SCHEMA_VERSION:
        return None
    if payload.get("extraction_version") != MEMORY_V2_EXTRACTION_VERSION:
        return None
    if payload.get("model") != model:
        return None
    if payload.get("source_mtime_ns") != source_file.stat().st_mtime_ns:
        return None
    if payload.get("source_size") != source_file.stat().st_size:
        return None
    return payload


def write_daily_payload(output_dir: Path, payload: dict[str, object]) -> None:
    daily_dir = output_dir / "_meta" / "daily"
    ensure_directory(daily_dir)
    atomic_write_text(daily_dir / f"{payload['source_day']}.json", json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True))


def parse_daily_chat_markdown(path: Path) -> list[ChatMessage]:
    text = path.read_text(encoding="utf-8")
    source_day = path.name[:10]
    lines = text.splitlines()
    messages: list[ChatMessage] = []
    index = 0
    current_timestamp: str | None = None
    current_actor: str | None = None
    current_source_ref: str | None = None
    in_fence = False
    fence_marker: str | None = None
    buffer: list[str] = []

    def flush() -> None:
        nonlocal index, current_timestamp, current_actor, current_source_ref, buffer
        if current_timestamp and current_actor and buffer:
            body = "\n".join(buffer).strip("\n")
            if body:
                index += 1
                messages.append(
                    ChatMessage(
                        message_index=index,
                        timestamp=current_timestamp,
                        actor=current_actor,
                        text=body,
                        source_day=source_day,
                        source_file=str(path),
                        source_ref=current_source_ref,
                    )
                )
        buffer = []

    for line in lines:
        heading = re.match(r"^##\s+(.+?)\s+-\s+(User|Agent)\s*$", line)
        if heading and not in_fence:
            flush()
            current_timestamp = heading.group(1).strip()
            current_actor = heading.group(2).strip()
            current_source_ref = None
            continue
        if not in_fence and line.startswith("<!-- source:"):
            current_source_ref = line.removeprefix("<!-- source:").removesuffix("-->").strip()
            continue
        if line.startswith("```"):
            marker = "```"
            if not in_fence:
                in_fence = True
                fence_marker = marker
                continue
            if marker == fence_marker:
                in_fence = False
                fence_marker = None
                continue
        if in_fence and current_timestamp and current_actor:
            buffer.append(line)
    flush()
    return messages


def extract_daily_candidates(
    source_day: str,
    source_file: Path,
    messages: list[ChatMessage],
    model: str,
    llm_client: LlmClient | None,
) -> dict[str, object]:
    system_prompt = daily_extraction_prompt()
    all_candidates: list[dict[str, object]] = []
    windows = build_message_windows(messages)
    window_summaries: list[dict[str, object]] = []
    for window_index, window in enumerate(windows, 1):
        payload = {
            "source_day": source_day,
            "source_file": str(source_file),
            "window_index": window_index,
            "window_count": len(windows),
            "message_index_range": [window[0].message_index, window[-1].message_index],
            "task": "Extract broad operational memory candidates from this bounded daily chat window. Return JSON only.",
            "schema": candidate_schema(),
            "messages": [message.to_llm_dict() for message in window],
        }
        response = call_llm_json(system_prompt, payload, model, llm_client)
        candidates = response.get("candidates", [])
        if isinstance(candidates, list):
            all_candidates.extend(candidate for candidate in candidates if isinstance(candidate, dict))
        window_summaries.append(
            {
                "window_index": window_index,
                "message_index_range": [window[0].message_index, window[-1].message_index],
                "message_count": len(window),
                "candidate_count": len(candidates) if isinstance(candidates, list) else 0,
            }
        )
    return {"candidates": all_candidates, "windows": window_summaries}


def build_message_windows(
    messages: list[ChatMessage],
    *,
    max_chars: int = DEFAULT_WINDOW_MAX_CHARS,
    overlap_messages: int = DEFAULT_WINDOW_OVERLAP_MESSAGES,
) -> list[list[ChatMessage]]:
    windows: list[list[ChatMessage]] = []
    current: list[ChatMessage] = []
    current_chars = 0
    for message in messages:
        message_chars = len(message.text) + len(message.timestamp) + len(message.actor) + 32
        if current and current_chars + message_chars > max_chars:
            windows.append(current)
            current = current[-overlap_messages:] if overlap_messages else []
            current_chars = sum(len(entry.text) + len(entry.timestamp) + len(entry.actor) + 32 for entry in current)
        current.append(message)
        current_chars += message_chars
    if current:
        windows.append(current)
    return windows


def project_slugs_from_candidates(candidates: list[dict[str, object]]) -> list[str]:
    return sorted({str(candidate.get("project")) for candidate in candidates if candidate.get("project") not in {"global", "unknown", "cross-project", None}})


def collect_project_contexts(projects: Iterable[str], project_root_dir: Path | str | None = None) -> dict[str, dict[str, object]]:
    search_root = Path(project_root_dir) if project_root_dir else default_project_search_root()
    contexts: dict[str, dict[str, object]] = {}
    for project in projects:
        root = resolve_project_directory(search_root, project)
        if not root:
            continue
        contexts[project] = {
            "project": project,
            "project_root": str(root),
            "readmes": read_project_readmes(root),
            "directory_tree": build_project_tree(root),
            "tree_command": f"cd {root}; tree /F /A",
        }
    return contexts


def default_project_search_root() -> Path:
    cwd = Path.cwd().resolve()
    return cwd.parent if cwd.name.lower() == "wikimemory" else cwd


def resolve_project_directory(search_root: Path, project: str) -> Path | None:
    candidates = PROJECT_DIRECTORY_ALIASES.get(project, (project,))
    for candidate in candidates:
        path = search_root / candidate
        if path.exists() and path.is_dir():
            return path
    normalized = project.replace("-", "").lower()
    for path in search_root.iterdir() if search_root.exists() else []:
        if path.is_dir() and path.name.replace("-", "").replace("_", "").lower() == normalized:
            return path
    return None


def read_project_readmes(root: Path) -> list[dict[str, object]]:
    readmes: list[dict[str, object]] = []
    seen_paths: set[Path] = set()
    for name in ("README.md", "README.MD", "readme.md"):
        path = root / name
        if not path.exists() or not path.is_file():
            continue
        resolved = path.resolve()
        if resolved in seen_paths:
            continue
        seen_paths.add(resolved)
        text = path.read_text(encoding="utf-8", errors="replace")[:DEFAULT_PROJECT_README_MAX_CHARS]
        readmes.append({"path": str(path), "content": text})
    return readmes


def build_project_tree(root: Path, *, max_depth: int = DEFAULT_PROJECT_TREE_DEPTH, max_entries: int = DEFAULT_PROJECT_TREE_MAX_ENTRIES) -> list[str]:
    lines = [f"{root.name}/"]
    count = 0

    def walk(path: Path, prefix: str, depth: int) -> None:
        nonlocal count
        if depth > max_depth or count >= max_entries:
            return
        try:
            children = sorted(path.iterdir(), key=lambda child: (child.is_file(), child.name.lower()))
        except OSError:
            return
        children = [child for child in children if include_tree_path(child)]
        for index, child in enumerate(children):
            if count >= max_entries:
                return
            connector = "`-- " if index == len(children) - 1 else "|-- "
            lines.append(f"{prefix}{connector}{child.name}{'/' if child.is_dir() else ''}")
            count += 1
            if child.is_dir():
                extension = "    " if index == len(children) - 1 else "|   "
                walk(child, prefix + extension, depth + 1)

    walk(root, "", 1)
    if count >= max_entries:
        lines.append("... tree truncated ...")
    return lines


def include_tree_path(path: Path) -> bool:
    if path.name in TREE_EXCLUDED_DIRS:
        return False
    if path.name.startswith(".") and path.name not in {".github"}:
        return False
    return True


def merge_memory_candidates(
    candidates: list[dict[str, object]],
    model: str,
    llm_client: LlmClient | None,
    *,
    project_contexts: dict[str, dict[str, object]] | None = None,
) -> dict[str, object]:
    if len(candidates) > 250:
        items: list[dict[str, object]] = []
        batches: list[dict[str, object]] = []
        grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
        for candidate in candidates:
            grouped[str(candidate.get("project") or "unknown")].append(candidate)
        for project, project_candidates in sorted(grouped.items()):
            contexts = {project: project_contexts[project]} if project_contexts and project in project_contexts else {}
            payload = merge_memory_candidate_batch(project_candidates, model, llm_client, project_contexts=contexts)
            batch_items = [item for item in payload.get("items", []) if isinstance(item, dict)]
            items.extend(batch_items)
            batches.append({"project": project, "candidate_count": len(project_candidates), "item_count": len(batch_items)})
        return {"items": items, "batches": batches}
    return merge_memory_candidate_batch(candidates, model, llm_client, project_contexts=project_contexts)


def merge_memory_candidate_batch(
    candidates: list[dict[str, object]],
    model: str,
    llm_client: LlmClient | None,
    *,
    project_contexts: dict[str, dict[str, object]] | None = None,
) -> dict[str, object]:
    system_prompt = merge_prompt()
    payload = {
        "task": "Merge, deduplicate, resolve lifecycle, and promote memory candidates into canonical wiki items. Return JSON only.",
        "schema": item_schema(),
        "candidates": candidates,
        "project_contexts": project_contexts or {},
    }
    return call_llm_json(system_prompt, payload, model, llm_client)


def call_llm_json(system_prompt: str, payload: dict[str, object], model: str, llm_client: LlmClient | None) -> dict[str, object]:
    if llm_client:
        return llm_client(system_prompt, payload, model)
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise MemoryV2Error("Missing OPENAI_API_KEY for memory-v2 LLM run.")
    request_payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False, sort_keys=True)},
        ],
        "response_format": {"type": "json_object"},
        "max_completion_tokens": 60000,
    }
    try:
        response = post_openai_chat(request_payload, api_key)
        content = response["choices"][0]["message"]["content"]
    except MemoryV2Error as exc:
        if "not a chat model" not in str(exc).lower():
            raise
        response = post_openai_response(system_prompt, payload, model, api_key)
        content = extract_responses_text(response)
    return parse_json_object(content)


def post_openai_chat(payload: dict[str, object], api_key: str) -> dict[str, object]:
    base_url = os.environ.get("WIKIMEMORY_OPENAI_BASE_URL", "https://api.openai.com").rstrip("/")
    request = urllib.request.Request(
        url=f"{base_url}/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    return post_json_with_retries(request, "OpenAI memory-v2 request failed")


def post_openai_response(system_prompt: str, payload: dict[str, object], model: str, api_key: str) -> dict[str, object]:
    request_payload: dict[str, object] = {
        "model": model,
        "instructions": system_prompt,
        "input": json.dumps(payload, ensure_ascii=False, sort_keys=True),
        "text": {"format": {"type": "json_object"}},
        "max_output_tokens": 60000,
    }
    return post_openai_responses_payload(request_payload, api_key)


def post_openai_responses_payload(payload: dict[str, object], api_key: str) -> dict[str, object]:
    base_url = os.environ.get("WIKIMEMORY_OPENAI_BASE_URL", "https://api.openai.com").rstrip("/")
    request = urllib.request.Request(
        url=f"{base_url}/v1/responses",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    return post_json_with_retries(request, "OpenAI memory-v2 Responses request failed")


def post_json_with_retries(request: urllib.request.Request, failure_prefix: str, *, attempts: int = 4) -> dict[str, object]:
    last_error = ""
    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(request, timeout=1800) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            if "max_completion_tokens" in body or "max_output_tokens" in body:
                raise MemoryV2Error(f"{failure_prefix}: {exc.code} {body}") from exc
            last_error = f"{exc.code} {body}"
            if exc.code not in {408, 409, 429, 500, 502, 503, 504} or attempt == attempts:
                raise MemoryV2Error(f"{failure_prefix}: {last_error}") from exc
        except urllib.error.URLError as exc:
            last_error = str(exc.reason)
            if attempt == attempts:
                raise MemoryV2Error(f"{failure_prefix}: {last_error}") from exc
        time.sleep(min(30, 2 ** attempt))
    raise MemoryV2Error(f"{failure_prefix}: {last_error}")


def extract_responses_text(response: dict[str, object]) -> str:
    output_text = response.get("output_text")
    if isinstance(output_text, str) and output_text.strip():
        return output_text
    chunks: list[str] = []
    for item in response.get("output", []) if isinstance(response.get("output"), list) else []:
        if not isinstance(item, dict):
            continue
        content = item.get("content")
        if not isinstance(content, list):
            continue
        for part in content:
            if isinstance(part, dict) and isinstance(part.get("text"), str):
                chunks.append(part["text"])
    if not chunks:
        raise MemoryV2Error("OpenAI Responses output did not contain text.")
    return "\n".join(chunks)


def parse_json_object(text: str) -> dict[str, object]:
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise MemoryV2Error("LLM response did not contain a JSON object.")
        parsed = json.loads(match.group(0))
    if not isinstance(parsed, dict):
        raise MemoryV2Error("LLM response root must be a JSON object.")
    return parsed


def normalize_candidate(candidate: dict[str, object], source_day: str) -> dict[str, object]:
    statement = normalize_statement(str(candidate.get("agent_facing_statement") or candidate.get("statement") or ""))
    memory_class = normalize_memory_class(candidate.get("memory_class"), candidate.get("memory_role"), candidate.get("project"))
    memory_class = demote_transient_rule(statement, memory_class)
    memory_role = normalize_memory_role(candidate.get("memory_role"), memory_class)
    project = normalize_project(candidate.get("project"), memory_class)
    evidence_refs = normalize_evidence_refs(candidate.get("evidence_refs"), source_day)
    candidate_id = str(candidate.get("candidate_id") or stable_id(source_day, project, memory_class, memory_role, statement))
    temporal_status = normalize_temporal_status(candidate.get("temporal_status"), memory_class)
    return {
        "candidate_id": candidate_id,
        "source_day": str(candidate.get("source_day") or source_day),
        "project": project,
        "memory_class": memory_class,
        "memory_role": memory_role,
        "agent_facing_statement": statement,
        "confidence": normalize_confidence(candidate.get("confidence")),
        "temporal_status": temporal_status,
        "evidence_refs": evidence_refs,
        "valid_from": candidate.get("valid_from"),
        "valid_to": candidate.get("valid_to"),
        "resolved_by": candidate.get("resolved_by"),
        "needs_review": bool(candidate.get("needs_review", False)),
    }


def normalize_item(item: dict[str, object], candidate_lookup: dict[str, dict[str, object]] | None = None) -> dict[str, object]:
    statement = normalize_statement(str(item.get("agent_facing_statement") or item.get("statement") or ""))
    memory_class = normalize_memory_class(item.get("memory_class"), item.get("memory_role"), item.get("project"))
    memory_class = demote_transient_rule(statement, memory_class)
    memory_role = normalize_memory_role(item.get("memory_role"), memory_class)
    project = normalize_project(item.get("project"), memory_class)
    evidence_refs = normalize_evidence_refs(item.get("evidence_refs"), str(item.get("source_day") or ""))
    if not evidence_refs and candidate_lookup:
        evidence_refs = evidence_refs_from_candidates(item, candidate_lookup)
    item_id = str(item.get("item_id") or stable_id(project, memory_class, memory_role, statement))
    return {
        "item_id": item_id,
        "schema_version": MEMORY_V2_SCHEMA_VERSION,
        "project": project,
        "memory_class": memory_class,
        "memory_role": memory_role,
        "agent_facing_statement": statement,
        "confidence": normalize_confidence(item.get("confidence")),
        "temporal_status": normalize_temporal_status(item.get("temporal_status"), memory_class),
        "evidence_refs": evidence_refs,
        "valid_from": item.get("valid_from"),
        "valid_to": item.get("valid_to"),
        "resolved_by": item.get("resolved_by"),
        "needs_review": bool(item.get("needs_review", False)),
    }


def validate_items(items: list[dict[str, object]]) -> None:
    for item in items:
        if not item["agent_facing_statement"]:
            raise MemoryV2Error(f"Empty canonical memory item: {item.get('item_id')}")
        if not item["evidence_refs"]:
            raise MemoryV2Error(f"Memory item has no evidence refs: {item.get('item_id')}")


def render_memory_v2(output_dir: Path, items: list[dict[str, object]], project_contexts: dict[str, dict[str, object]] | None = None) -> list[Path]:
    rendered: list[Path] = []
    project_contexts = project_contexts or {}
    items = suppress_project_rules_repeated_globally(items)
    global_items = [item for item in items if item["memory_class"] == "global_rule" and item["project"] == "global"]
    rendered.append(write_global_rules(output_dir / "global" / "user-rules.md", global_items))
    projects = sorted({str(item["project"]) for item in items if item["project"] not in {"global", "unknown"}})
    for project in projects:
        project_items = [item for item in items if item["project"] == project]
        rendered.append(write_project_page(output_dir / "projects" / project / "project.md", project, project_items, project_contexts.get(project)))
        rendered.append(write_recent_page(output_dir / "projects" / project / "recent.md", project, project_items))
        rendered.append(write_rules_page(output_dir / "projects" / project / "rules.md", project, project_items))
        lessons = [item for item in project_items if item["memory_class"] == "lesson"]
        if lessons:
            rendered.append(write_lessons_page(output_dir / "projects" / project / "lessons.md", project, lessons))
    return rendered


def suppress_project_rules_repeated_globally(items: list[dict[str, object]]) -> list[dict[str, object]]:
    global_rules = [item for item in items if item.get("project") == "global" and item.get("memory_class") == "global_rule"]
    if not global_rules:
        return items
    global_tokens = [memory_statement_tokens(str(item.get("agent_facing_statement", ""))) for item in global_rules]
    filtered: list[dict[str, object]] = []
    for item in items:
        if item.get("project") != "global" and item.get("memory_class") == "project_rule":
            tokens = memory_statement_tokens(str(item.get("agent_facing_statement", "")))
            if any(memory_token_overlap(tokens, global_rule_tokens) >= 0.72 for global_rule_tokens in global_tokens):
                continue
        filtered.append(item)
    return filtered


def memory_statement_tokens(statement: str) -> set[str]:
    stopwords = {
        "a",
        "an",
        "and",
        "are",
        "as",
        "be",
        "by",
        "for",
        "if",
        "in",
        "into",
        "is",
        "of",
        "on",
        "or",
        "the",
        "to",
        "with",
    }
    return {token for token in re.findall(r"[a-z0-9_]+", statement.lower()) if len(token) > 2 and token not in stopwords}


def memory_token_overlap(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    return len(left & right) / min(len(left), len(right))


def write_global_rules(path: Path, items: list[dict[str, object]]) -> Path:
    lines = frontmatter("global-rules", None, ["memory", "rules", "global"])
    lines.extend(["# Global User Rules", ""])
    buckets = bucket_rule_items(items)
    append_section(lines, "ALWAYS DO", statements(buckets["always"]))
    append_section(lines, "NEVER DO", statements(buckets["never"]))
    append_section(lines, "CONDITIONAL RULES", statements(buckets["conditional"]))
    append_section(lines, "PROVENANCE", ["Detailed evidence is stored in `_meta/merged_items.json`."])
    write_lines(path, lines)
    return path


def write_project_page(path: Path, project: str, items: list[dict[str, object]], project_context: dict[str, object] | None = None) -> Path:
    lines = frontmatter("project-memory", project, [f"project/{project}", "memory"])
    architecture_items = [item for item in items if item["memory_class"] == "architecture"]
    component_items = [item for item in architecture_items if is_component_statement(str(item["agent_facing_statement"]))]
    flow_items = [item for item in architecture_items if item not in component_items]
    lines.extend([f"# {display_project(project)} - Project Memory", ""])
    append_section(lines, "PURPOSE", statements([item for item in items if item["memory_class"] == "project_summary" and item["memory_role"] == "purpose"], limit=4))
    append_section(lines, "CORE COMPONENTS", statements(component_items, limit=8))
    append_section(lines, "CURRENT ARCHITECTURE", statements(flow_items, limit=8))
    append_tree_section(lines, project_context)
    append_section(lines, "KEY CONSTRAINTS", statements([item for item in items if item["memory_role"] == "constraint" and item["memory_class"] in {"project_summary", "architecture"}], limit=8))
    append_section(lines, "OPEN PROBLEMS", [])
    append_section(lines, "RELATED", related_links(project))
    write_lines(path, lines)
    return path


def write_recent_page(path: Path, project: str, items: list[dict[str, object]]) -> Path:
    recent_classes = {"current_state", "decision", "next_step", "open_question", "failure_risk"}
    active = [item for item in items if item["memory_class"] in recent_classes and item["temporal_status"] == "active"]
    used_fallback = False
    if not active:
        active = latest_recent_fallback_items(items)
        used_fallback = True
    latest_date = latest_item_date(active or items)
    lines = frontmatter("recent-context", project, [f"project/{project}", "recent"])
    title = f"# {display_project(project)} - Recent Context"
    if latest_date:
        title += f" - {format_display_date(latest_date)}"
    lines.extend([title, ""])
    append_section(lines, "CURRENT FOCUS", statements(active if used_fallback else [item for item in active if item["memory_class"] == "current_state"], limit=5))
    append_section(lines, "ACTIVE DECISIONS", statements([item for item in active if item["memory_class"] == "decision"], limit=6))
    append_section(lines, "IN PROGRESS", statements([item for item in active if item["memory_class"] == "next_step"], limit=8))
    append_section(lines, "FAILED / AVOID", statements([item for item in active if item["memory_class"] == "failure_risk"], limit=6))
    append_numbered(lines, "OPEN QUESTIONS", statements([item for item in active if item["memory_class"] == "open_question"], limit=6))
    write_lines(path, lines)
    return path


def latest_recent_fallback_items(items: list[dict[str, object]], *, limit: int = 5) -> list[dict[str, object]]:
    candidates = [item for item in items if item.get("memory_class") in {"project_summary", "architecture", "project_rule", "decision"}]
    return sorted(candidates, key=lambda item: latest_item_date([item]) or "", reverse=True)[:limit]


def latest_item_date(items: list[dict[str, object]]) -> str | None:
    dates: list[str] = []
    for item in items:
        for ref in item.get("evidence_refs", []):
            if isinstance(ref, dict):
                source_day = str(ref.get("source_day") or "")
                if re.match(r"^\d{4}-\d{2}-\d{2}$", source_day):
                    dates.append(source_day)
    return max(dates) if dates else None


def format_display_date(day: str) -> str:
    try:
        from datetime import date

        parsed = date.fromisoformat(day)
        return parsed.strftime("%B %d %Y")
    except ValueError:
        return day


def write_rules_page(path: Path, project: str, items: list[dict[str, object]]) -> Path:
    rules = [item for item in items if item["memory_class"] == "project_rule"]
    lines = frontmatter("project-rules", project, [f"project/{project}", "rules"])
    lines.extend([f"# {display_project(project)} - Project Rules", ""])
    buckets = bucket_rule_items(rules)
    append_section(lines, "ALWAYS DO", statements(buckets["always"]))
    append_section(lines, "NEVER DO", statements(buckets["never"]))
    append_section(lines, "CONDITIONAL RULES", statements(buckets["conditional"]))
    append_section(lines, "SCOPE NOTES", [f"Applies only to `{project}` unless a rule explicitly says otherwise."])
    write_lines(path, lines)
    return path


def write_lessons_page(path: Path, project: str, items: list[dict[str, object]]) -> Path:
    lines = frontmatter("lessons", project, [f"project/{project}", "lessons"])
    lines.extend([f"# {display_project(project)} - Lessons Learned", ""])
    append_section(lines, "LESSONS", statements(items, limit=12))
    write_lines(path, lines)
    return path


def frontmatter(kind: str, project: str | None, tags: list[str]) -> list[str]:
    lines = ["---", f"type: {kind}"]
    if project:
        lines.append(f"project: {project}")
    lines.append(f"updated: {utc_now()}")
    lines.append("tags: [" + ", ".join(tags) + "]")
    lines.extend(["---", ""])
    return lines


def append_section(lines: list[str], title: str, bullets: list[str]) -> None:
    lines.extend([f"## {title}", ""])
    if not bullets:
        lines.extend(["_No selected items from this evidence._", ""])
        return
    for bullet in bullets:
        lines.append(f"- {bullet}")
    lines.append("")


def append_numbered(lines: list[str], title: str, entries: list[str]) -> None:
    lines.extend([f"## {title}", ""])
    if not entries:
        lines.extend(["_No selected items from this evidence._", ""])
        return
    for index, entry in enumerate(entries, 1):
        lines.append(f"{index}. {entry}")
    lines.append("")


def append_tree_section(lines: list[str], project_context: dict[str, object] | None) -> None:
    lines.extend(["## DIRECTORY TREE", ""])
    tree_lines = project_context.get("directory_tree") if project_context else None
    if not isinstance(tree_lines, list) or not tree_lines:
        lines.extend(["_No repository tree discovered._", ""])
        return
    command = project_context.get("tree_command") or "tree"
    lines.extend([f"`{command}`", "", "```text"])
    lines.extend(str(line) for line in tree_lines[:DEFAULT_PROJECT_TREE_MAX_ENTRIES])
    lines.extend(["```", ""])


def statements(
    items: list[dict[str, object]],
    *,
    include: tuple[str, ...] = (),
    limit: int = 12,
    exclude_used: bool = False,
) -> list[str]:
    selected: list[str] = []
    seen: set[str] = set()
    for item in sorted(items, key=item_rank):
        statement = str(item["agent_facing_statement"]).strip()
        lowered = statement.lower()
        if include and not any(term in lowered for term in include):
            continue
        if exclude_used and any(term in lowered for term in ("always", "must", "do not", "don't", "never")):
            continue
        key = re.sub(r"[^a-z0-9]+", " ", lowered).strip()
        if not key or key in seen:
            continue
        seen.add(key)
        selected.append(statement)
        if len(selected) >= limit:
            break
    return selected


def bucket_rule_items(items: list[dict[str, object]]) -> dict[str, list[dict[str, object]]]:
    buckets: dict[str, list[dict[str, object]]] = {"always": [], "never": [], "conditional": []}
    seen: set[str] = set()
    for item in sorted(items, key=item_rank):
        for statement in split_rule_statement(str(item["agent_facing_statement"]).strip()):
            key = re.sub(r"[^a-z0-9]+", " ", statement.lower()).strip()
            if not key or key in seen:
                continue
            seen.add(key)
            bucket_item = dict(item)
            bucket_item["agent_facing_statement"] = clean_split_rule_statement(statement)
            buckets[rule_bucket(statement)].append(bucket_item)
    return buckets


def split_rule_statement(statement: str) -> list[str]:
    if "but " not in statement.lower() or statement.lower().startswith("enforce "):
        return [statement]
    parts = [part.strip(" ;") for part in re.split(r";\s*", statement) if part.strip(" ;")]
    if len(parts) <= 1:
        return [statement]
    result: list[str] = []
    subject = extract_rule_subject(parts[0])
    for index, part in enumerate(parts):
        normalized = attach_rule_subject(part, subject) if index > 0 else part
        result.extend(split_once_by_contrast(normalized))
    return [part for part in result if part]


def clean_split_rule_statement(statement: str) -> str:
    cleaned = statement.strip()
    if cleaned.startswith("must not "):
        cleaned = "Do not " + cleaned.removeprefix("must not ")
    elif cleaned.startswith("should not "):
        cleaned = "Do not " + cleaned.removeprefix("should not ")
    elif cleaned.startswith("once "):
        cleaned = "Once " + cleaned.removeprefix("once ")
    if cleaned and cleaned[-1] not in ".!?":
        cleaned += "."
    return cleaned


def split_once_by_contrast(statement: str) -> list[str]:
    match = re.search(r"\bbut\s+(must not|should not|do not|does not|must|should|once\b)", statement, flags=re.IGNORECASE)
    if not match:
        return [statement]
    left = statement[: match.start()].strip(" ,;")
    right = statement[match.start() + 4 :].strip(" ,;")
    return [part for part in (left, right) if part]


def extract_rule_subject(statement: str) -> str | None:
    match = re.match(r"^([A-Z][A-Za-z0-9_ -]{1,40}?)\s+(?:should|must|handles?|provides?|orchestrates?|does|uses?)\b", statement)
    return match.group(1).strip() if match else None


def attach_rule_subject(statement: str, subject: str | None) -> str:
    if not subject:
        return statement
    lowered = statement.lower()
    if lowered.startswith(("must ", "must not ", "should ", "should not ", "do not ", "does not ")):
        return f"{subject} {statement}"
    return statement


def rule_bucket(statement: str) -> str:
    lowered = statement.strip().lower()
    if lowered.startswith(("enforce ", "treat ", "use ", "keep ", "preserve ", "maintain ", "ensure ", "prefer ", "prioritize ")):
        return "always"
    if lowered.startswith(("do not ", "don't ", "never ", "avoid ", "stop ", "must not ", "should not ")):
        return "never"
    if any(term in lowered for term in (" must not ", " should not ", " never ")):
        return "never"
    if lowered.startswith(("if ", "when ", "while ", "during ", "for ", "in ", "once ")):
        return "conditional"
    if " unless " in lowered or " when " in lowered:
        return "conditional"
    return "always"


def is_component_statement(statement: str) -> bool:
    lowered = statement.lower()
    return any(term in lowered for term in ("component", "hotspot", "implementation", "module", "supporting", "src/"))


def item_rank(item: dict[str, object]) -> tuple[int, str]:
    confidence = {"explicit": 0, "strong": 1, "medium": 2, "low": 3}.get(str(item.get("confidence")), 4)
    return confidence, str(item.get("valid_from") or "")


def write_lines(path: Path, lines: list[str]) -> None:
    ensure_directory(path.parent)
    atomic_write_text(path, "\n".join(lines).rstrip() + "\n")


def related_links(project: str) -> list[str]:
    display = display_project(project)
    return [
        f"[[projects/{project}/recent|{display} Recent]]",
        f"[[projects/{project}/rules|{display} Rules]]",
        "[[global/user-rules|Global User Rules]]",
    ]


def write_memory_v2_meta(
    output_dir: Path,
    daily_payloads: list[dict[str, object]],
    items: list[dict[str, object]],
    project_contexts: dict[str, dict[str, object]] | None = None,
) -> None:
    for payload in daily_payloads:
        write_daily_payload(output_dir, payload)
    atomic_write_text(output_dir / "_meta" / "merged_items.json", json.dumps({"items": items}, indent=2, ensure_ascii=False, sort_keys=True))
    project_contexts = project_contexts or {}
    atomic_write_text(output_dir / "_meta" / "project_contexts.json", json.dumps(project_contexts, indent=2, ensure_ascii=False, sort_keys=True))
    manifest = {
        "schema_version": MEMORY_V2_SCHEMA_VERSION,
        "rendered_at": utc_now(),
        "day_count": len(daily_payloads),
        "candidate_count": sum(len(payload["candidates"]) for payload in daily_payloads),
        "item_count": len(items),
        "project_context_count": len(project_contexts),
    }
    atomic_write_text(output_dir / "_meta" / "manifest.json", json.dumps(manifest, indent=2, sort_keys=True))


def write_memory_v2_failure_debug(
    output_dir: Path,
    daily_payloads: list[dict[str, object]],
    all_candidates: list[dict[str, object]],
    merged_payload: dict[str, object] | None,
    error: str,
) -> None:
    try:
        debug_dir = output_dir / "_meta" / "debug"
        ensure_directory(debug_dir)
        payload = {
            "error": error,
            "daily_payloads": daily_payloads,
            "candidate_count": len(all_candidates),
            "candidates": all_candidates,
            "merged_payload": merged_payload,
        }
        atomic_write_text(debug_dir / "last_failure.json", json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True))
    except Exception:
        return


def daily_extraction_prompt() -> str:
    return (
        "You extract operational memory candidates for AI coding workflows from a bounded daily chat window. "
        "Return a JSON object with key `candidates`. Favor recall: include useful medium-confidence candidates. "
        "Use only these memory_class values: global_rule, project_rule, project_summary, architecture, current_state, "
        "decision, next_step, open_question, failure_risk, lesson. Use only these memory_role values: purpose, "
        "architecture, constraint, rule, recent_state, decision, lesson, discard. Do not invent alternate enum values. "
        "Extract project identity and architecture when repeated terms/components reveal what a project is, even if this "
        "is inferred rather than explicitly stated. "
        "Rewrite user intent as clear future-agent guidance, never as raw pasted user fragments. "
        "Ignore agent reasoning, tool chatter, implementation progress unless it states an outcome the user needs. "
        "Every candidate must include evidence_refs with at least one exact message_index from the provided messages. "
        "Use evidence_refs like [{\"source_day\":\"YYYY-MM-DD\",\"message_index\":123,\"actor\":\"User\"}]. "
        "Never emit a candidate with empty evidence_refs; omit it instead. JSON only."
    )


def merge_prompt() -> str:
    return (
        "You merge operational memory candidates into canonical wiki items. Return a JSON object with key `items`. "
        "Use project_contexts read from repository README files and directory trees to improve project purpose, "
        "component, and architecture descriptions, but do not invent facts beyond candidates plus repository context. "
        "Optimize precision: merge semantic duplicates, remove one-off commands from durable rules, keep conflicts "
        "as context-dependent guidance when useful, and keep only active/latest temporal items. "
        "Every item must either copy supporting evidence_refs from candidates or include supporting_candidate_ids. "
        "If a project has enough evidence to infer identity, purpose, components, or architecture, keep concise "
        "project_summary and architecture items so project.md is useful to a fresh agent. "
        "Temporary work-loop constraints containing current run/current fix loop/for now belong in current_state or "
        "next_step, not durable project_rule. "
        "Every item must be understandable by a new coding agent without reading the source chat. JSON only."
    )


def candidate_schema() -> dict[str, object]:
    return {
        "required_keys": ["candidates"],
        "allowed_memory_class": sorted(ALLOWED_CLASSES),
        "allowed_memory_role": sorted(ALLOWED_ROLES),
        "allowed_confidence": sorted(ALLOWED_CONFIDENCE),
        "allowed_temporal_status": sorted(ALLOWED_TEMPORAL),
        "candidate_fields": sorted(["candidate_id", "source_day", "project", "memory_class", "memory_role", "agent_facing_statement", "confidence", "temporal_status", "evidence_refs", "valid_from", "valid_to", "resolved_by", "needs_review"]),
    }


def item_schema() -> dict[str, object]:
    return {
        "required_keys": ["items"],
        "allowed_memory_class": sorted(ALLOWED_CLASSES),
        "allowed_memory_role": sorted(ALLOWED_ROLES),
        "allowed_confidence": sorted(ALLOWED_CONFIDENCE),
        "allowed_temporal_status": sorted(ALLOWED_TEMPORAL),
        "item_fields": sorted(["item_id", "project", "memory_class", "memory_role", "agent_facing_statement", "confidence", "temporal_status", "evidence_refs", "supporting_candidate_ids", "valid_from", "valid_to", "resolved_by", "needs_review"]),
    }


def normalize_statement(text: str) -> str:
    return " ".join(text.split())


def normalize_choice(value: object, allowed: set[str], default: str) -> str:
    text = str(value or "").strip().lower().replace("-", "_")
    return text if text in allowed else default


def normalize_memory_class(value: object, role: object, project: object) -> str:
    text = str(value or "").strip().lower().replace("-", "_").replace(" ", "_")
    if text in ALLOWED_CLASSES:
        return text
    if text in {"workflow_preference", "operational_preference", "quality_bar", "debugging_strategy", "implementation_rule"}:
        return "global_rule" if normalize_project(project, "current_state") == "global" else "project_rule"
    if text in {"implementation_constraint", "requirement", "constraint", "policy"}:
        return "project_rule"
    if text in {"project_identity", "project_context", "project_purpose", "purpose", "summary"}:
        return "project_summary"
    if text in {"risk", "failure", "issue", "failure", "avoidance"}:
        return "failure_risk"
    if text in {"task", "todo", "action_item"}:
        return "next_step"
    if text in {"state", "status", "current_focus"}:
        return "current_state"
    role_text = str(role or "").strip().lower().replace("-", "_").replace(" ", "_")
    if role_text in {"instruction", "requirement", "policy"}:
        return "global_rule" if normalize_project(project, "current_state") == "global" else "project_rule"
    return "current_state"


def normalize_memory_role(value: object, memory_class: str) -> str:
    text = str(value or "").strip().lower().replace("-", "_").replace(" ", "_")
    if text in ALLOWED_ROLES:
        return text
    if text in {"instruction", "policy", "rule", "preference"}:
        return "rule"
    if text in {"requirement", "boundary", "constraint"}:
        return "constraint"
    if text in {"summary", "identity", "purpose"}:
        return "purpose"
    if text in {"status", "task", "todo"}:
        return "recent_state"
    return role_for_class(memory_class)


def normalize_confidence(value: object) -> str:
    if isinstance(value, (int, float)):
        if value >= 0.95:
            return "strong"
        if value >= 0.7:
            return "medium"
        return "low"
    text = str(value or "").strip().lower().replace("-", "_").replace(" ", "_")
    if text in ALLOWED_CONFIDENCE:
        return text
    if text in {"high", "certain"}:
        return "strong"
    return "low"


def normalize_temporal_status(value: object, memory_class: str) -> str:
    text = normalize_choice(value, ALLOWED_TEMPORAL, temporal_for_class(memory_class))
    if memory_class in {"global_rule", "project_rule", "project_summary", "architecture", "lesson"}:
        return "durable"
    return text


def demote_transient_rule(statement: str, memory_class: str) -> str:
    if memory_class not in {"global_rule", "project_rule"}:
        return memory_class
    lowered = statement.lower()
    transient_markers = (
        "current fix loop",
        "current run",
        "this run",
        "this session",
        "for now",
        "today's run",
        "today only",
    )
    return "current_state" if any(marker in lowered for marker in transient_markers) else memory_class


def assign_unknown_projects(candidates: list[dict[str, object]]) -> list[dict[str, object]]:
    known_projects = sorted({str(candidate["project"]) for candidate in candidates if candidate["project"] not in {"global", "unknown"}})
    if len(known_projects) != 1:
        return candidates
    inferred_project = known_projects[0]
    adjusted: list[dict[str, object]] = []
    for candidate in candidates:
        if candidate["project"] == "unknown" and candidate["memory_class"] != "global_rule":
            candidate = dict(candidate)
            candidate["project"] = inferred_project
        adjusted.append(candidate)
    return adjusted


def normalize_project(value: object, memory_class: str) -> str:
    if memory_class == "global_rule":
        return "global"
    text = str(value or "unknown").strip().lower().replace("_", "-").replace(" ", "-")
    while "--" in text:
        text = text.replace("--", "-")
    if text in {"openbrain", "open-brain"}:
        return "open-brain"
    if text in {"ai-scientist", "ai-scientists"}:
        return "ai-scientist"
    if text in {"wiki-memory", "wikimemory"}:
        return "wikimemory"
    return text if text in PROJECT_SLUGS else "unknown"


def normalize_evidence_refs(value: object, source_day: str) -> list[dict[str, object]]:
    refs = []
    if isinstance(value, list):
        for ref in value:
            if isinstance(ref, int):
                refs.append({"source_day": source_day, "message_index": ref, "timestamp": None, "actor": None})
                continue
            if isinstance(ref, str):
                match = re.search(r"\d+", ref)
                if match:
                    refs.append({"source_day": source_day, "message_index": int(match.group(0)), "timestamp": None, "actor": None})
                continue
            if not isinstance(ref, dict):
                continue
            message_indexes = evidence_message_indexes(ref)
            for message_index in message_indexes:
                refs.append(
                    {
                        "source_day": str(ref.get("source_day") or source_day),
                        "message_index": message_index,
                        "timestamp": ref.get("timestamp"),
                        "actor": ref.get("actor"),
                    }
                )
    return [ref for ref in refs if ref.get("message_index") is not None]


def evidence_message_indexes(ref: dict[str, object]) -> list[object]:
    indexes: list[object] = []
    for key in ("message_index", "message_id", "index"):
        if ref.get(key) is not None:
            indexes.append(ref[key])
    for key in ("message_indexes", "message_indices", "message_ids", "indexes", "indices", "messages"):
        value = ref.get(key)
        if isinstance(value, list):
            indexes.extend(entry for entry in value if isinstance(entry, (str, int)))
    return list(dict.fromkeys(indexes))


def evidence_refs_from_candidates(item: dict[str, object], candidate_lookup: dict[str, dict[str, object]]) -> list[dict[str, object]]:
    refs: list[dict[str, object]] = []
    for candidate_id in extract_candidate_ids(item):
        candidate = candidate_lookup.get(candidate_id)
        if not candidate:
            continue
        refs.extend(normalize_evidence_refs(candidate.get("evidence_refs"), str(candidate.get("source_day") or "")))
    seen: set[tuple[object, object, object]] = set()
    unique: list[dict[str, object]] = []
    for ref in refs:
        key = (ref.get("source_day"), ref.get("message_index"), ref.get("actor"))
        if key in seen:
            continue
        seen.add(key)
        unique.append(ref)
    return unique


def extract_candidate_ids(item: dict[str, object]) -> list[str]:
    ids: list[str] = []
    for key in ("candidate_id", "candidate_ids", "source_candidate_id", "source_candidate_ids", "supporting_candidate_ids"):
        value = item.get(key)
        if isinstance(value, str):
            ids.append(value)
        elif isinstance(value, list):
            ids.extend(str(entry) for entry in value if isinstance(entry, (str, int)))
    evidence_refs = item.get("evidence_refs")
    if isinstance(evidence_refs, list):
        for ref in evidence_refs:
            if isinstance(ref, str):
                ids.append(ref)
            elif isinstance(ref, dict):
                for key in ("candidate_id", "source_candidate_id"):
                    if ref.get(key):
                        ids.append(str(ref[key]))
    return list(dict.fromkeys(ids))


def role_for_class(memory_class: str) -> str:
    return {
        "global_rule": "rule",
        "project_rule": "rule",
        "project_summary": "purpose",
        "architecture": "architecture",
        "decision": "decision",
        "lesson": "lesson",
    }.get(memory_class, "recent_state")


def temporal_for_class(memory_class: str) -> str:
    return "durable" if memory_class in {"global_rule", "project_rule", "project_summary", "architecture", "lesson"} else "active"


def display_project(project: str) -> str:
    return " ".join(part.capitalize() for part in project.split("-"))


def stable_id(*parts: object) -> str:
    return hashlib.sha256("|".join(str(part) for part in parts).encode("utf-8")).hexdigest()[:16]
