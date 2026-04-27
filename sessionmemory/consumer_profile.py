from __future__ import annotations

import json
import os
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

from .discovery import DiscoveryError, atomic_write_text, ensure_directory, utc_now
from .memory_v2 import call_llm_json
from .normalization import append_jsonl_text

STATE_SCHEMA_VERSION = 1
CONSUMER_PROFILE_SCHEMA_VERSION = 1
DEFAULT_CONSUMER_PROFILE_MODEL = "gpt-5.3-codex"
DEFAULT_CONSUMER_PROFILE_EXTRACTION_MODEL = "gpt-4o-mini"
DEFAULT_CONSUMER_PROFILE_MERGE_MODEL = "gpt-5.3-codex"
DEFAULT_CONSUMER_PROFILE_WINDOW_MAX_CHARS = 40000
ALLOWED_SECTIONS = {
    "communication_preferences",
    "workflow_preferences",
    "technical_strengths",
    "active_domains",
    "current_goals",
    "persistent_constraints",
    "collaboration_style",
    "decision_preferences",
    "tool_preferences",
}
SKIP_TEXT_PATTERNS = [
    re.compile(r"^# AGENTS\.md instructions", re.IGNORECASE),
    re.compile(r"^<environment_context>", re.IGNORECASE),
    re.compile(r"^<permissions instructions>", re.IGNORECASE),
    re.compile(r"^## Available skills", re.IGNORECASE),
    re.compile(r"^### Available skills", re.IGNORECASE),
]


class ConsumerProfileError(DiscoveryError):
    """Fatal consumer-profile error."""


@dataclass(frozen=True)
class ConsumerProfileRunReport:
    run_id: str
    started_at: str
    finished_at: str
    model: str
    source_snippet_count: int
    candidate_count: int
    section_count: int
    success: bool
    fatal_error_summary: str | None

    def to_dict(self) -> dict[str, object]:
        return {
            "run_id": self.run_id,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "model": self.model,
            "source_snippet_count": self.source_snippet_count,
            "candidate_count": self.candidate_count,
            "section_count": self.section_count,
            "success": self.success,
            "fatal_error_summary": self.fatal_error_summary,
        }


@dataclass(frozen=True)
class ConsumerProfileResult:
    report: ConsumerProfileRunReport
    profile_path: Path
    profile_json_path: Path
    candidates_path: Path
    run_log_path: Path


def run_consumer_profile(
    *,
    evidence_dir: Path | str,
    memory_dir: Path | str,
    state_dir: Path | str,
    audits_dir: Path | str,
    policy_path: Path | str = Path("config/consumer_profile_policy.json"),
    model: str | None = None,
    extraction_model: str | None = None,
    merge_model: str | None = None,
    window_max_chars: int | None = None,
    llm_client=None,
) -> ConsumerProfileResult:
    evidence_dir = Path(evidence_dir)
    memory_dir = Path(memory_dir)
    state_dir = Path(state_dir)
    audits_dir = Path(audits_dir)
    policy_path = Path(policy_path)
    ensure_directory(memory_dir / "_meta")
    ensure_directory(state_dir)
    ensure_directory(audits_dir)
    run_id = f"consumer-profile-{utc_now().replace(':', '').replace('.', '').replace('-', '')}"
    started_at = utc_now()
    model_id = model or os.environ.get("SESSIONMEMORY_CONSUMER_PROFILE_MODEL", "").strip() or DEFAULT_CONSUMER_PROFILE_MODEL
    extraction_model_id = (
        extraction_model
        or os.environ.get("SESSIONMEMORY_CONSUMER_PROFILE_EXTRACTION_MODEL", "").strip()
        or (model_id if model is not None else DEFAULT_CONSUMER_PROFILE_EXTRACTION_MODEL)
    )
    merge_model_id = (
        merge_model
        or os.environ.get("SESSIONMEMORY_CONSUMER_PROFILE_MERGE_MODEL", "").strip()
        or model_id
        or DEFAULT_CONSUMER_PROFILE_MERGE_MODEL
    )
    profile_path = memory_dir / "global" / "consumer-profile.md"
    profile_json_path = memory_dir / "_meta" / "consumer_profile.json"
    style_json_path = memory_dir / "_meta" / "consumer_style.json"
    candidates_path = audits_dir / "consumer_profile_candidates.jsonl"
    state_path = state_dir / "consumer_profile_state.json"
    progress_path = state_dir / "consumer_profile_progress.json"
    run_log_path = state_dir / "consumer_profile_runs.jsonl"
    previous_run_log = run_log_path.read_text(encoding="utf-8") if run_log_path.exists() else ""
    resolved_window_max_chars = window_max_chars or int(
        os.environ.get("SESSIONMEMORY_CONSUMER_PROFILE_WINDOW_MAX_CHARS", DEFAULT_CONSUMER_PROFILE_WINDOW_MAX_CHARS)
    )

    try:
        policy = load_json(policy_path)
        snippets = load_profile_source_snippets(evidence_dir)
        if not snippets:
            raise ConsumerProfileError("No eligible user conversation snippets found in evidence/logs.")
        write_progress(
            progress_path,
            {
                "run_id": run_id,
                "stage": "load-snippets",
                "started_at": started_at,
                "model": model_id,
                "extraction_model": extraction_model_id,
                "merge_model": merge_model_id,
                "source_snippet_count": len(snippets),
                "window_max_chars": resolved_window_max_chars,
            },
        )
        candidates = extract_candidates(
            snippets,
            extraction_model_id,
            llm_client,
            window_max_chars=resolved_window_max_chars,
            progress_callback=lambda payload: write_progress(progress_path, {"run_id": run_id, **payload}),
        )
        write_progress(
            progress_path,
            {
                "run_id": run_id,
                "stage": "merge-profile",
                "candidate_count": len(candidates),
                "merge_model": merge_model_id,
            },
        )
        merged_profile = merge_profile(candidates, merge_model_id, llm_client, policy)
        merged_profile["schema_version"] = CONSUMER_PROFILE_SCHEMA_VERSION
        merged_profile["profile_status"] = "draft"
        merged_profile["updated_at"] = utc_now()
        merged_profile["consumer_id"] = "local-consumer"
        merged_profile["source_snippet_count"] = len(snippets)
        style_profile = compile_consumer_style_profile(merged_profile)
        render_consumer_profile(profile_path, merged_profile)
        atomic_write_text(profile_json_path, json.dumps(merged_profile, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
        atomic_write_text(style_json_path, json.dumps(style_profile, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
        write_jsonl(candidates_path, candidates)
        state_payload = {
            "schema_version": STATE_SCHEMA_VERSION,
            "consumer_profile_schema_version": CONSUMER_PROFILE_SCHEMA_VERSION,
            "last_run_id": run_id,
            "last_profiled_at": utc_now(),
            "model": model_id,
            "extraction_model": extraction_model_id,
            "merge_model": merge_model_id,
            "source_snippet_count": len(snippets),
            "candidate_count": len(candidates),
            "profile_status": merged_profile["profile_status"],
            "style_profile_path": str(style_json_path),
        }
        atomic_write_text(state_path, json.dumps(state_payload, indent=2, sort_keys=True) + "\n")
        write_progress(
            progress_path,
            {
                "run_id": run_id,
                "stage": "completed",
                "finished_at": utc_now(),
                "candidate_count": len(candidates),
                "section_count": len(merged_profile.get("sections", {})),
                "success": True,
            },
        )
        report = ConsumerProfileRunReport(
            run_id=run_id,
            started_at=started_at,
            finished_at=utc_now(),
            model=model_id,
            source_snippet_count=len(snippets),
            candidate_count=len(candidates),
            section_count=len(merged_profile.get("sections", {})),
            success=True,
            fatal_error_summary=None,
        )
        atomic_write_text(run_log_path, append_jsonl_text(previous_run_log, [report.to_dict()]))
        return ConsumerProfileResult(report, profile_path, profile_json_path, candidates_path, run_log_path)
    except Exception as exc:
        write_progress(
            progress_path,
            {
                "run_id": run_id,
                "stage": "failed",
                "finished_at": utc_now(),
                "success": False,
                "fatal_error_summary": str(exc),
            },
        )
        report = ConsumerProfileRunReport(
            run_id=run_id,
            started_at=started_at,
            finished_at=utc_now(),
            model=model_id,
            source_snippet_count=0,
            candidate_count=0,
            section_count=0,
            success=False,
            fatal_error_summary=str(exc),
        )
        atomic_write_text(run_log_path, append_jsonl_text(previous_run_log, [report.to_dict()]))
        return ConsumerProfileResult(report, profile_path, profile_json_path, candidates_path, run_log_path)


def load_profile_source_snippets(evidence_dir: Path) -> list[dict[str, object]]:
    snippets: list[dict[str, object]] = []
    for path in sorted((evidence_dir / "logs").glob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            record = json.loads(line)
            if str(record.get("actor_type") or "") != "user":
                continue
            text = clean_source_text(record_text(record))
            if not text:
                continue
            provenance = dict(record.get("provenance") or {})
            snippet = {
                "snippet_id": str(record.get("evidence_id") or ""),
                "source_id": str(record.get("source_id") or provenance.get("source_id") or ""),
                "source_day": str(record.get("timestamp") or "")[:10],
                "message_index": int(provenance.get("source_line_no") or 0),
                "timestamp": str(record.get("timestamp") or ""),
                "project_hint": str(record.get("project_hint") or ""),
                "text": text,
            }
            snippets.append(snippet)
    return snippets


def record_text(record: dict[str, object]) -> str:
    parts: list[str] = []
    for surface in record.get("content_surfaces", []):
        if isinstance(surface, dict):
            text = str(surface.get("text") or "").strip()
            if text:
                parts.append(text)
    return "\n".join(parts).strip()


def clean_source_text(text: str) -> str:
    stripped = text.strip()
    if not stripped:
        return ""
    for pattern in SKIP_TEXT_PATTERNS:
        if pattern.search(stripped):
            return ""
    stripped = re.sub(r"^# Context from my IDE setup:\s*", "", stripped, flags=re.IGNORECASE)
    if len(stripped) > 4000:
        stripped = stripped[:4000].rstrip() + "..."
    return stripped


def extract_candidates(
    snippets: list[dict[str, object]],
    model: str,
    llm_client,
    *,
    window_max_chars: int = DEFAULT_CONSUMER_PROFILE_WINDOW_MAX_CHARS,
    progress_callback=None,
) -> list[dict[str, object]]:
    windows = build_windows(snippets, max_chars=window_max_chars)
    all_candidates: list[dict[str, object]] = []
    for window_index, window in enumerate(windows, 1):
        if progress_callback:
            progress_callback(
                {
                    "stage": "extract-candidates",
                    "window_index": window_index,
                    "window_count": len(windows),
                    "window_snippet_count": len(window),
                    "candidates_collected_so_far": len(all_candidates),
                }
            )
        payload = {
            "task": "Extract candidate consumer working-profile facts from these user messages. Return JSON only.",
            "window_index": window_index,
            "window_count": len(windows),
            "allowed_sections": sorted(ALLOWED_SECTIONS),
            "output_contract": {
                "root_key": "candidates",
                "required_fields": ["section", "summary", "confidence", "evidence_ids"],
                "evidence_rule": "Each candidate must include one or more snippet_id values from the provided snippets in evidence_ids. Do not use prose evidence instead of snippet_id references.",
            },
            "rules": [
                "Only extract collaboration-relevant traits.",
                "Do not infer IQ, psychology, diagnosis, or sensitive personal traits.",
                "Prefer repeated requests, explicit preferences, goals, domains, and work habits.",
                "Use soft evidence-backed wording.",
                "Return an object with a top-level candidates array.",
                "Each candidate must cite snippet_id values from this window in evidence_ids.",
                "Do not return candidates if you cannot anchor them to specific snippet_id values from the provided snippets.",
            ],
            "snippets": window,
        }
        response = call_llm_json(consumer_profile_extract_prompt(), payload, model, llm_client)
        for raw in iter_raw_candidates(response):
            if isinstance(raw, dict):
                normalized = normalize_candidate(raw, window)
                if normalized:
                    all_candidates.append(normalized)
        if progress_callback:
            progress_callback(
                {
                    "stage": "extract-candidates",
                    "window_index": window_index,
                    "window_count": len(windows),
                    "window_snippet_count": len(window),
                    "candidates_collected_so_far": len(all_candidates),
                    "window_completed": True,
                }
            )
    return dedupe_candidates(all_candidates)


def merge_profile(candidates: list[dict[str, object]], model: str, llm_client, policy: dict[str, object]) -> dict[str, object]:
    payload = {
        "task": "Merge consumer working-profile candidates into a single review-first profile. Return JSON only.",
        "allowed_sections": sorted(ALLOWED_SECTIONS),
        "policy": policy,
        "candidate_count": len(candidates),
        "candidates": candidates,
        "project_counts": top_project_counts(candidates),
    }
    response = call_llm_json(consumer_profile_merge_prompt(), payload, model, llm_client)
    return normalize_profile(response, candidates)


def build_windows(snippets: list[dict[str, object]], max_chars: int = DEFAULT_CONSUMER_PROFILE_WINDOW_MAX_CHARS) -> list[list[dict[str, object]]]:
    windows: list[list[dict[str, object]]] = []
    current: list[dict[str, object]] = []
    current_chars = 0
    for snippet in snippets:
        snippet_chars = len(str(snippet["text"])) + 80
        if current and current_chars + snippet_chars > max_chars:
            windows.append(current)
            current = current[-3:]
            current_chars = sum(len(str(item["text"])) + 80 for item in current)
        current.append(snippet)
        current_chars += snippet_chars
    if current:
        windows.append(current)
    return windows


def consumer_profile_extract_prompt() -> str:
    return (
        "You extract a consumer working profile for future coding-agent collaboration. "
        "Only infer work-relevant collaboration traits from the user's own messages. "
        "Do not infer IQ, psychology, diagnosis, or sensitive traits. "
        "Return a JSON object with a top-level 'candidates' array. "
        "Each candidate must include: section, trait, summary, confidence, evidence_ids, and optional project_hint. "
        "Every evidence_ids entry must be a snippet_id copied exactly from the provided snippets. "
        "Do not use free-text evidence in place of snippet_id references. "
        "Return only JSON."
    )


def consumer_profile_merge_prompt() -> str:
    return (
        "You merge evidence-backed consumer working-profile candidates into a review-first profile. "
        "Keep only collaboration-relevant traits with soft wording and evidence references. "
        "Do not include sensitive traits or intelligence scoring. "
        "Return a JSON object with optional summary plus section keys named from the allowed sections. "
        "Each section value must be an array of items. "
        "Each item must include trait and evidence_refs. "
        "Each evidence_refs entry must preserve source_id, source_day, message_index, and snippet_id. "
        "Return only JSON."
    )


def iter_raw_candidates(response: dict[str, object]) -> list[dict[str, object]]:
    raw_candidates = response.get("candidates")
    if isinstance(raw_candidates, list):
        return [item for item in raw_candidates if isinstance(item, dict)]
    flattened: list[dict[str, object]] = []
    for section in sorted(ALLOWED_SECTIONS):
        raw_items = response.get(section, [])
        if not isinstance(raw_items, list):
            continue
        for raw_item in raw_items:
            if not isinstance(raw_item, dict):
                continue
            evidence = raw_item.get("evidence") if isinstance(raw_item.get("evidence"), dict) else {}
            evidence_ids = []
            if evidence.get("snippet_id"):
                evidence_ids.append(str(evidence.get("snippet_id")))
            elif raw_item.get("snippet_id"):
                evidence_ids.append(str(raw_item.get("snippet_id")))
            summary = str(
                raw_item.get("summary")
                or raw_item.get("preference")
                or raw_item.get("notes")
                or raw_item.get("goal")
                or raw_item.get("constraint")
                or raw_item.get("trait")
                or ""
            ).strip()
            flattened.append(
                {
                    "section": section,
                    "trait": str(raw_item.get("trait") or "observed_preference").strip(),
                    "summary": summary,
                    "confidence": raw_item.get("confidence"),
                    "evidence_ids": evidence_ids,
                    "evidence_quote": str(evidence.get("quote") or raw_item.get("quote") or "").strip(),
                    "project_hint": raw_item.get("project_hint") or "",
                }
            )
    return flattened


def normalize_candidate(raw: dict[str, object], window: list[dict[str, object]]) -> dict[str, object] | None:
    section = str(raw.get("section") or "").strip()
    if section not in ALLOWED_SECTIONS:
        return None
    evidence_ids = [str(item) for item in raw.get("evidence_ids", []) if str(item)]
    snippet_map = {str(snippet["snippet_id"]): snippet for snippet in window}
    if not evidence_ids:
        evidence_ids = infer_evidence_ids_from_quote(str(raw.get("evidence_quote") or ""), window)
    evidence_refs = []
    for evidence_id in evidence_ids:
        snippet = snippet_map.get(evidence_id)
        if snippet:
            evidence_refs.append(
                {
                    "source_id": snippet["source_id"],
                    "source_day": snippet["source_day"],
                    "message_index": snippet["message_index"],
                    "snippet_id": snippet["snippet_id"],
                }
            )
    if not evidence_refs:
        return None
    return {
        "candidate_id": stable_id(section, raw.get("trait"), raw.get("summary"), ",".join(evidence_ids)),
        "section": section,
        "trait": str(raw.get("trait") or "").strip() or "observed_preference",
        "summary": str(raw.get("summary") or "").strip(),
        "confidence": normalize_confidence(raw.get("confidence")),
        "project_hint": str(raw.get("project_hint") or ""),
        "evidence_refs": evidence_refs,
    }


def infer_evidence_ids_from_quote(quote: str, window: list[dict[str, object]]) -> list[str]:
    cleaned = quote.strip().strip("\"'").strip()
    if not cleaned:
        return [str(window[0]["snippet_id"])] if len(window) == 1 else []
    matches = [str(snippet["snippet_id"]) for snippet in window if cleaned.lower() in str(snippet["text"]).lower()]
    if matches:
        return matches[:1]
    return [str(window[0]["snippet_id"])] if len(window) == 1 else []


def normalize_confidence(value: object) -> str:
    text = str(value or "medium").lower()
    return text if text in {"low", "medium", "high"} else "medium"


def dedupe_candidates(candidates: list[dict[str, object]]) -> list[dict[str, object]]:
    seen: set[str] = set()
    unique: list[dict[str, object]] = []
    for candidate in candidates:
        key = stable_id(candidate["section"], candidate["trait"], candidate["summary"])
        if key in seen:
            continue
        seen.add(key)
        unique.append(candidate)
    return unique


def top_project_counts(candidates: list[dict[str, object]]) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for candidate in candidates:
        project = str(candidate.get("project_hint") or "")
        if project and project != "projects":
            counts[project] += 1
    return dict(counts.most_common(10))


def normalize_profile(response: dict[str, object], candidates: list[dict[str, object]]) -> dict[str, object]:
    sections: dict[str, dict[str, object]] = {}
    for section in sorted(ALLOWED_SECTIONS):
        raw_items = []
        if isinstance(response.get("sections"), dict):
            raw_items = response.get("sections", {}).get(section, [])
        elif isinstance(response.get(section), list):
            raw_items = response.get(section, [])
        items: list[dict[str, object]] = []
        for raw_item in raw_items if isinstance(raw_items, list) else []:
            if not isinstance(raw_item, dict):
                continue
            evidence_refs = normalize_profile_item_evidence(raw_item, candidates)
            if not evidence_refs:
                continue
            item = {
                "trait": str(raw_item.get("trait") or raw_item.get("domain") or raw_item.get("tool") or raw_item.get("goal") or raw_item.get("strength") or raw_item.get("constraint") or "").strip() or "observed_trait",
                "preference": str(raw_item.get("preference") or raw_item.get("notes") or raw_item.get("goal") or raw_item.get("constraint") or raw_item.get("observed_level") or raw_item.get("trait") or raw_item.get("strength") or "").strip(),
                "confidence": normalize_confidence(raw_item.get("confidence")),
                "evidence_refs": evidence_refs,
            }
            if raw_item.get("status") not in (None, ""):
                item["status"] = str(raw_item.get("status"))
            if raw_item.get("type") not in (None, ""):
                item["type"] = str(raw_item.get("type"))
            items.append(item)
        if items:
            sections[section] = {"items": items}
    summary = str(response.get("summary") or "Consumer working profile inferred from prior user conversations.").strip()
    return {"summary": summary, "sections": sections}


def normalize_profile_item_evidence(raw_item: dict[str, object], candidates: list[dict[str, object]]) -> list[dict[str, object]]:
    direct_refs = raw_item.get("evidence_refs", [])
    if isinstance(direct_refs, list):
        normalized_direct: list[dict[str, object]] = []
        seen_direct: set[str] = set()
        for ref in direct_refs:
            if not isinstance(ref, dict):
                continue
            source_id = str(ref.get("source_id") or "").strip()
            source_day = str(ref.get("source_day") or "").strip()
            snippet_id = str(ref.get("snippet_id") or "").strip()
            message_index = ref.get("message_index")
            if not snippet_id or message_index in (None, ""):
                continue
            normalized_ref = {
                "source_id": source_id,
                "source_day": source_day,
                "message_index": int(message_index),
                "snippet_id": snippet_id,
            }
            key = stable_id(source_id, source_day, normalized_ref["message_index"], snippet_id)
            if key in seen_direct:
                continue
            seen_direct.add(key)
            normalized_direct.append(normalized_ref)
        if normalized_direct:
            return normalized_direct
    by_id = {str(candidate["candidate_id"]): candidate for candidate in candidates}
    refs: list[dict[str, object]] = []
    for candidate_id in raw_item.get("candidate_ids", []):
        candidate = by_id.get(str(candidate_id))
        if candidate:
            refs.extend(candidate.get("evidence_refs", []))
    deduped: list[dict[str, object]] = []
    seen: set[str] = set()
    for ref in refs:
        key = stable_id(ref.get("source_id"), ref.get("source_day"), ref.get("message_index"), ref.get("snippet_id"))
        if key in seen:
            continue
        seen.add(key)
        deduped.append(ref)
    return deduped


def render_consumer_profile(path: Path, profile: dict[str, object]) -> None:
    ensure_directory(path.parent)
    lines = [
        "---",
        "type: consumer-working-profile",
        f"updated: {profile.get('updated_at')}",
        "memory_role: preference",
        "tags: [memory, consumer-profile]",
        "---",
        "",
        "# Consumer Working Profile",
        "",
        str(profile.get("summary") or ""),
        "",
    ]
    for section, payload in sorted(profile.get("sections", {}).items()):
        items = payload.get("items", []) if isinstance(payload, dict) else []
        if not items:
            continue
        lines.extend([f"## {display_section(section)}", ""])
        for item in items:
            sentence = str(item.get("preference") or item.get("trait") or "").strip()
            lines.append(f"- {sentence}")
        lines.append("")
    atomic_write_text(path, "\n".join(lines).rstrip() + "\n")


def display_section(section: str) -> str:
    return section.replace("_", " ").title()


def compile_consumer_style_profile(profile: dict[str, object]) -> dict[str, object]:
    text = " ".join(
        str(item.get("preference") or item.get("trait") or "")
        for payload in profile.get("sections", {}).values()
        if isinstance(payload, dict)
        for item in payload.get("items", [])
        if isinstance(item, dict)
    ).lower()
    tone = "calm_direct"
    if "warm" in text or "collaborative" in text:
        tone = "warm_collaborative"
    elif "concise" in text or "direct" in text:
        tone = "calm_direct"
    verbosity = "concise" if any(term in text for term in ("concise", "brief", "short")) else "standard"
    structure = "structured" if any(term in text for term in ("structured", "organized", "plan", "clear")) else "flexible"
    decision_style = "proactive" if any(term in text for term in ("infer defaults", "go implement", "avoid over-planning", "low-friction")) else "collaborative"
    reassurance_level = "high" if any(term in text for term in ("avoid repeat", "continuation", "low-friction", "concise progress")) else "medium"
    personalization_lines = build_personalization_lines(text)
    return {
        "generated_at": utc_now(),
        "tone": tone,
        "verbosity": verbosity,
        "structure": structure,
        "decision_style": decision_style,
        "reassurance_level": reassurance_level,
        "personalization_lines": personalization_lines,
    }


def build_personalization_lines(text: str) -> list[str]:
    lines: list[str] = []
    if any(term in text for term in ("concise", "brief", "short")):
        lines.append("Keep this practical, concise, and low-friction.")
    if any(term in text for term in ("structured", "organized", "clear")):
        lines.append("Stay clear and structured so the next step is easy to pick.")
    if any(term in text for term in ("infer defaults", "proactive", "go implement")):
        lines.append("Use proactive defaults and preserve momentum instead of making the consumer rebuild context.")
    if not lines:
        lines.append("Match the consumer's usual working style and avoid unnecessary re-explanation.")
    return lines[:4]


def load_json(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    atomic_write_text(path, "".join(json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n" for row in rows))


def write_progress(path: Path, payload: dict[str, object]) -> None:
    atomic_write_text(path, json.dumps({**payload, "updated_at": utc_now()}, indent=2, ensure_ascii=False, sort_keys=True) + "\n")


def stable_id(*parts: object) -> str:
    import hashlib

    return hashlib.sha256("|".join(str(part) for part in parts).encode("utf-8")).hexdigest()[:16]
