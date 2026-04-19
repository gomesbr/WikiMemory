from __future__ import annotations

import hashlib
import json
import os
import re
import urllib.error
import urllib.request
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable

from .discovery import DiscoveryError, utc_now
from .product_config import ProductConfig

MEMORY_EXTRACTION_SCHEMA_VERSION = 1
TEMPORAL_ITEM_TYPES = {"current_state", "next_step", "open_question", "task", "failure_risk"}
PROJECT_SUMMARY_TYPES = {"project_summary", "architecture", "constraint", "decision", "purpose"}
RULE_ITEM_TYPES = {"global_rule", "project_rule"}
LESSON_TYPES = {"lesson"}
USER_ACTORS = {"user", "human"}
AGENT_ACTORS = {"assistant", "agent_reasoning", "tool", "developer", "system"}

GLOBAL_RULE_PATTERN = re.compile(
    r"\b(?:global rule|add this to global rules|for all projects|always|never|do not|don't|must|real data|concise|token|explanation|ask|github|outside the plan)\b",
    re.IGNORECASE,
)
PROJECT_RULE_PATTERN = re.compile(
    r"\b(?:project rule|add this to project rules|for this project|always|never|do not|don't|must)\b|^no\b.{0,80}\bshould\b",
    re.IGNORECASE,
)
PROJECT_SUMMARY_PATTERN = re.compile(
    r"\b(?:project is|repo is|repository is|purpose|goal is|architecture|pipeline|component|system|designed to|built to|source of truth)\b",
    re.IGNORECASE,
)
LESSON_PATTERN = re.compile(r"\b(?:lesson learned|root cause|postmortem|next time|avoid repeating)\b", re.IGNORECASE)
OPEN_QUESTION_PATTERN = re.compile(r"\?|open question|unclear|need to decide|not sure|should we", re.IGNORECASE)
NEXT_STEP_PATTERN = re.compile(r"\b(?:next step|next,|todo|remaining|continue|implement|fix|follow up)\b", re.IGNORECASE)
RESOLUTION_PATTERN = re.compile(
    r"\b(?:done|fixed|resolved|closed|cleared|implemented|decided|agreed|no longer|not needed|obsolete|superseded)\b",
    re.IGNORECASE,
)
EXPLICIT_PROMOTION_PATTERN = re.compile(
    r"\b(?:add this to global rules|add this to project rules|global rule|project rule|always|never|do not|don't|must)\b",
    re.IGNORECASE,
)
VERBATIM_PREFIX_PATTERN = re.compile(r"^(?:nah|ok|okay|great|please|can you|go|next|agreed|correct|yes)[,.\s:!-]+", re.IGNORECASE)
NOISE_PATTERN = re.compile(
    r"(?:context from my ide setup|open tabs:|active file:|single prompt to codex|copy/paste|<permissions instructions>|</permissions instructions>|<collaboration_mode>|</collaboration_mode>|api key|\.env|github app|download obsidian|where are the dos|what'?s next\??|create the plan|plan next phase|push to git|do the work.*don'?t explain|notices?:\s*\d+|are you testing|^next$|^go$|^ok$)",
    re.IGNORECASE,
)
RUNTIME_LOCAL_PATTERN = re.compile(
    r"\b(?:localhost|ctrl\+f5|hard refresh|browser refresh|restart (?:the )?(?:app|application|server|service))\b",
    re.IGNORECASE,
)
FIRST_PERSON_LOCAL_PATTERN = re.compile(r"\b(?:i'll|i will|i don't|i do not|i need|i'm|i am|i keep|i close|i reopen|i think|my life's|my agents)\b", re.IGNORECASE)
SINGLE_USER_PATTERN = re.compile(r"\b(?:i'll be the only one using|i will be the only one using|only one using this|my agents)\b", re.IGNORECASE)
LONG_PLAN_PATTERN = re.compile(r"\b(?:please implement this plan|implement this plan|implementation plan|execution-ready)\b", re.IGNORECASE)
PROMPT_SCAFFOLD_PATTERN = re.compile(
    r"\b(?:i will answer like|question format requirement|important operating style|reference output|mandatory|primary goal|expected phases|phase\s+\d+\s+plan|single prompt to codex)\b",
    re.IGNORECASE,
)
CODE_ARTIFACT_PATTERN = re.compile(
    r"(?:file:\s*[A-Z]:/|[A-Z]:\\|\.codex/skills|^\s*m\s+(?:config|tests|wikimemory)/|tests/test_|pyproject\.toml|\.env\b)",
    re.IGNORECASE,
)
TRANSIENT_REQUEST_PATTERN = re.compile(
    r"(?:<environment_context>|what is next|next phase|one more question|send me the full report|do i need|can i add|how do i|if i decide|is the process|how is .* adding information|should have mentioned|you are helping redesign|implements all remaining|no,? that.?s .*problem|create the plan|phase \d+ should be treated as a checkpoint|full-load run|commit and merge|download obsidian)",
    re.IGNORECASE,
)


class MemoryExtractionError(DiscoveryError):
    """Fatal memory extraction error."""


@dataclass(frozen=True)
class MemoryExtractionArtifacts:
    items: list[dict[str, object]]
    windows: list[dict[str, object]]
    candidates: list[dict[str, object]]
    notices: list[dict[str, object]]


def extract_memory_artifacts(
    records: list[dict[str, object]],
    *,
    config: ProductConfig,
    project_filter: set[str],
    require_inferred_rule_review: bool,
    unresolved_project: str,
    run_id: str,
) -> MemoryExtractionArtifacts:
    windows = build_extraction_windows(records, config, project_filter)
    notices: list[dict[str, object]] = []
    candidates = extract_deterministic_candidates(windows, require_inferred_rule_review)

    if config.memory_extraction.enabled:
        llm_windows = windows[: config.memory_extraction.max_windows_per_run]
        try:
            candidates.extend(extract_llm_candidates(llm_windows, config))
        except Exception as exc:
            if not config.memory_extraction.fallback_to_deterministic:
                raise
            notices.append(
                notice(
                    run_id,
                    "warning",
                    "memory_llm_fallback",
                    f"Memory LLM extraction fell back to deterministic extraction: {exc}",
                )
            )

    candidates = dedupe_candidates(resolve_candidate_lifecycle(candidates))
    items = merge_candidates(
        candidates,
        require_inferred_rule_review=require_inferred_rule_review,
        unresolved_project=unresolved_project,
    )
    return MemoryExtractionArtifacts(items=items, windows=windows, candidates=candidates, notices=notices)


def build_extraction_windows(
    records: list[dict[str, object]],
    config: ProductConfig,
    project_filter: set[str],
) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for record in records:
        project = slugify(str(record.get("project_hint") or record.get("source_id") or "project"))
        if project_filter and project not in project_filter:
            continue
        prepared = prepare_record(record, project, config.memory_extraction.max_window_chars)
        if not prepared:
            continue
        grouped[(project, str(record.get("source_id") or "source"))].append(prepared)

    windows: list[dict[str, object]] = []
    limit = config.memory_extraction.window_record_limit
    step = max(1, limit - config.memory_extraction.window_overlap_records)
    for (project, source_id), prepared_records in sorted(grouped.items()):
        prepared_records.sort(key=lambda item: (str(item.get("timestamp") or ""), str(item.get("evidence_id") or "")))
        for index in range(0, len(prepared_records), step):
            chunk = prepared_records[index : index + limit]
            if not chunk:
                continue
            window_id = stable_id("window", project, source_id, index, ",".join(str(item["evidence_id"]) for item in chunk))
            windows.append(
                {
                    "window_id": window_id,
                    "memory_extraction_schema_version": MEMORY_EXTRACTION_SCHEMA_VERSION,
                    "project": project,
                    "source_id": source_id,
                    "start_timestamp": first_non_empty(item.get("timestamp") for item in chunk),
                    "end_timestamp": last_non_empty(item.get("timestamp") for item in chunk),
                    "records": chunk,
                }
            )
            if index + limit >= len(prepared_records):
                break
    return windows


def prepare_record(record: dict[str, object], project: str, max_chars: int) -> dict[str, object] | None:
    evidence_type = str(record.get("evidence_type") or "")
    actor_type = str(record.get("actor_type") or "")
    if evidence_type in {"git_head", "git_status_item"}:
        return None
    raw_text = strip_code_blocks(extract_request_text(evidence_text(record)))
    text = raw_text.strip() if evidence_type == "project_overview_file" else normalize_statement(raw_text)
    if not text:
        return None
    if evidence_type.startswith("git_") or evidence_type == "project_overview_file":
        pass
    elif actor_type not in USER_ACTORS:
        return None
    if actor_type in AGENT_ACTORS:
        return None
    if is_runtime_or_scaffold_only(text):
        return None
    if len(text) > max_chars:
        text = text[: max_chars - 3].rstrip() + "..."
    return {
        "evidence_id": str(record.get("evidence_id") or stable_id(record.get("source_id"), text)),
        "evidence_type": evidence_type,
        "actor_type": actor_type,
        "timestamp": record.get("timestamp"),
        "project": project,
        "text": text,
        "provenance": record.get("provenance", {}),
        "metadata": record.get("metadata", {}),
    }


def extract_deterministic_candidates(
    windows: list[dict[str, object]],
    require_inferred_rule_review: bool,
) -> list[dict[str, object]]:
    candidates: list[dict[str, object]] = []
    for window in windows:
        for record in window["records"]:
            text = str(record["text"])
            evidence_type = str(record.get("evidence_type") or "")
            if evidence_type == "project_overview_file":
                for clause in project_overview_clauses(text):
                    item_type = classify_clause_type(clause) or "project_summary"
                    statement = guide_statement(clause, item_type)
                    if statement:
                        candidates.append(make_candidate(window, record, item_type, statement, "strong", "project_overview_file"))
                continue
            for clause in candidate_clauses(text):
                item_type = classify_clause_type(clause)
                if not item_type:
                    continue
                if item_type in RULE_ITEM_TYPES and is_one_off_instruction(clause):
                    item_type = "next_step"
                statement = guide_statement(clause, item_type)
                if not statement:
                    continue
                confidence = "explicit" if EXPLICIT_PROMOTION_PATTERN.search(clause) else "medium"
                candidate = make_candidate(window, record, item_type, statement, confidence, "deterministic")
                candidate["needs_review"] = bool(
                    require_inferred_rule_review
                    and item_type in RULE_ITEM_TYPES
                    and candidate["promotion_reason"] != "explicit_user_instruction"
                )
                candidates.append(candidate)
    return candidates


def make_candidate(
    window: dict[str, object],
    record: dict[str, object],
    item_type: str,
    statement: str,
    confidence: str,
    extraction_rule: str,
) -> dict[str, object]:
    mapped = map_item_type(item_type, str(window["project"]))
    timestamp = record.get("timestamp")
    promotion_reason = "explicit_user_instruction" if confidence == "explicit" else "candidate_signal"
    candidate_id = stable_id("candidate", window["window_id"], record.get("evidence_id"), item_type, normalize_for_key(statement))
    return {
        "candidate_id": candidate_id,
        "memory_extraction_schema_version": MEMORY_EXTRACTION_SCHEMA_VERSION,
        "source_window_id": window["window_id"],
        "source_window_ids": [window["window_id"]],
        "evidence_refs": [
            {
                "evidence_id": record.get("evidence_id"),
                "timestamp": timestamp,
                "provenance": record.get("provenance", {}),
            }
        ],
        "evidence_ids": [record.get("evidence_id")],
        "project": mapped["project"],
        "scope": mapped["scope"],
        "memory_class": mapped["memory_class"],
        "item_type": mapped["item_type"],
        "temporal_status": mapped["temporal_status"],
        "subject_key": subject_key(statement),
        "agent_facing_statement": statement,
        "statement": statement,
        "confidence": confidence if confidence in {"explicit", "strong", "medium", "low"} else "low",
        "promotion_reason": promotion_reason,
        "needs_review": False,
        "valid_from": timestamp,
        "valid_to": None,
        "resolved_by": None,
        "extraction_rule_ids": [extraction_rule],
    }


def extract_llm_candidates(windows: list[dict[str, object]], config: ProductConfig) -> list[dict[str, object]]:
    api_key = os.environ.get(config.memory_extraction.provider.api_key_env, "").strip()
    if not api_key:
        raise MemoryExtractionError(f"Missing OpenAI API key in {config.memory_extraction.provider.api_key_env}")
    candidates: list[dict[str, object]] = []
    batch_size = 6
    for offset in range(0, len(windows), batch_size):
        batch = windows[offset : offset + batch_size]
        if not batch:
            continue
        payload = call_openai_memory_extractor(batch, config)
        for raw in payload.get("candidates", []):
            if isinstance(raw, dict):
                candidate = validate_llm_candidate(raw, batch)
                if candidate:
                    candidates.append(candidate)
    return candidates


def call_openai_memory_extractor(windows: list[dict[str, object]], config: ProductConfig) -> dict[str, object]:
    provider = config.memory_extraction.provider
    system_prompt = (
        "Extract operational memory candidates for AI coding agents from timeline windows. "
        "Return JSON only. Prefer recall at candidate stage: include useful low/medium candidates, "
        "but label confidence accurately. Do not copy the user's words verbatim; rewrite intent as "
        "clear guidance to a future coding agent. Do not store agent reasoning, tool output, or one-off "
        "commands as durable rules. Temporal items must remain temporal."
    )
    user_payload = {
        "task": "Extract memory candidates from these windows.",
        "allowed_memory_classes": [
            "global_rule",
            "project_rule",
            "project_summary",
            "architecture",
            "constraint",
            "current_state",
            "decision",
            "next_step",
            "open_question",
            "failure_risk",
            "lesson",
        ],
        "required_output": {
            "candidates": [
                {
                    "source_window_id": "window id from input",
                    "evidence_ids": ["evidence ids from the window"],
                    "project": "project slug or global",
                    "memory_class": "one allowed class",
                    "subject_key": "short stable subject",
                    "agent_facing_statement": "rewritten guidance, not a quote",
                    "confidence": "explicit|strong|medium|low",
                    "temporal_status": "active|historical|resolved|superseded|durable",
                    "promotion_reason": "explicit_user_instruction|repeated_signal|candidate_signal|project_evidence",
                    "needs_review": True,
                    "valid_from": "timestamp or null",
                    "valid_to": None,
                    "resolved_by": None,
                }
            ]
        },
        "windows": compact_windows_for_llm(windows, config.memory_extraction.max_candidates_per_window),
    }
    request_payload = {
        "model": os.environ.get(provider.model_env, "").strip() or provider.default_model,
        "temperature": provider.temperature,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": json.dumps(user_payload, sort_keys=True)},
        ],
    }
    request = urllib.request.Request(
        url=f"{(os.environ.get(provider.base_url_env, '').strip() or 'https://api.openai.com').rstrip('/')}/v1/chat/completions",
        data=json.dumps(request_payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {os.environ[provider.api_key_env]}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            response_payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise MemoryExtractionError(f"OpenAI memory extraction failed: {exc.code} {body}") from exc
    except urllib.error.URLError as exc:
        raise MemoryExtractionError(f"OpenAI memory extraction failed: {exc.reason}") from exc
    try:
        content = response_payload["choices"][0]["message"]["content"]
        parsed = json.loads(content)
    except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
        raise MemoryExtractionError("OpenAI memory extraction response was invalid") from exc
    if not isinstance(parsed, dict):
        raise MemoryExtractionError("OpenAI memory extraction response root must be an object")
    return parsed


def compact_windows_for_llm(windows: list[dict[str, object]], max_candidates_per_window: int) -> list[dict[str, object]]:
    compact = []
    for window in windows:
        compact.append(
            {
                "window_id": window["window_id"],
                "project": window["project"],
                "source_id": window["source_id"],
                "start_timestamp": window.get("start_timestamp"),
                "end_timestamp": window.get("end_timestamp"),
                "max_candidates": max_candidates_per_window,
                "records": [
                    {
                        "evidence_id": record.get("evidence_id"),
                        "actor_type": record.get("actor_type"),
                        "evidence_type": record.get("evidence_type"),
                        "timestamp": record.get("timestamp"),
                        "text": record.get("text"),
                    }
                    for record in window["records"]
                ],
            }
        )
    return compact


def validate_llm_candidate(raw: dict[str, object], windows: list[dict[str, object]]) -> dict[str, object] | None:
    windows_by_id = {str(window["window_id"]): window for window in windows}
    window_id = str(raw.get("source_window_id") or "")
    window = windows_by_id.get(window_id)
    if not window:
        return None
    allowed_evidence = {str(record["evidence_id"]): record for record in window["records"]}
    evidence_ids = [str(item) for item in raw.get("evidence_ids", []) if str(item) in allowed_evidence]
    if not evidence_ids:
        return None
    item_type = normalize_item_type(str(raw.get("memory_class") or raw.get("item_type") or ""))
    if not item_type:
        return None
    project = slugify(str(raw.get("project") or window["project"]))
    mapped = map_item_type(item_type, project)
    statement = normalize_statement(str(raw.get("agent_facing_statement") or raw.get("statement") or ""))
    statement = guide_statement(statement, mapped["item_type"])
    if not statement:
        return None
    refs = []
    timestamps = []
    for evidence_id in evidence_ids:
        record = allowed_evidence[evidence_id]
        timestamps.append(record.get("timestamp"))
        refs.append({"evidence_id": evidence_id, "timestamp": record.get("timestamp"), "provenance": record.get("provenance", {})})
    confidence = str(raw.get("confidence") or "low")
    if confidence not in {"explicit", "strong", "medium", "low"}:
        confidence = "low"
    temporal_status = str(raw.get("temporal_status") or mapped["temporal_status"])
    if temporal_status not in {"active", "historical", "resolved", "superseded", "durable"}:
        temporal_status = mapped["temporal_status"]
    if mapped["memory_class"] in {"global_user_rules", "project_rules", "stable_project_summary", "project_lessons"}:
        temporal_status = "durable"
    candidate_id = stable_id("llm-candidate", window_id, ",".join(evidence_ids), item_type, normalize_for_key(statement))
    return {
        "candidate_id": candidate_id,
        "memory_extraction_schema_version": MEMORY_EXTRACTION_SCHEMA_VERSION,
        "source_window_id": window_id,
        "source_window_ids": [window_id],
        "evidence_refs": refs,
        "evidence_ids": evidence_ids,
        "project": mapped["project"],
        "scope": mapped["scope"],
        "memory_class": mapped["memory_class"],
        "item_type": mapped["item_type"],
        "temporal_status": temporal_status,
        "subject_key": normalize_for_key(str(raw.get("subject_key") or subject_key(statement))),
        "agent_facing_statement": statement,
        "statement": statement,
        "confidence": confidence,
        "promotion_reason": str(raw.get("promotion_reason") or "candidate_signal"),
        "needs_review": bool(raw.get("needs_review", confidence not in {"explicit", "strong"})),
        "valid_from": raw.get("valid_from") or first_non_empty(timestamps),
        "valid_to": raw.get("valid_to"),
        "resolved_by": raw.get("resolved_by"),
        "extraction_rule_ids": ["llm_windowed_extraction"],
    }


def resolve_candidate_lifecycle(candidates: list[dict[str, object]]) -> list[dict[str, object]]:
    ordered = sorted(candidates, key=lambda item: (str(item.get("project") or ""), parse_time(item.get("valid_from")), str(item["candidate_id"])))
    for index, candidate in enumerate(ordered):
        if str(candidate.get("item_type")) not in TEMPORAL_ITEM_TYPES:
            continue
        if str(candidate.get("temporal_status")) not in {"active", ""}:
            continue
        for later in ordered[index + 1 :]:
            if candidate.get("project") != later.get("project"):
                continue
            if parse_time(later.get("valid_from")) < parse_time(candidate.get("valid_from")):
                continue
            if not lifecycle_overlap(candidate, later):
                continue
            later_text = str(later.get("agent_facing_statement") or later.get("statement") or "")
            if RESOLUTION_PATTERN.search(later_text) or str(later.get("item_type")) in {"decision", "current_state"}:
                candidate["temporal_status"] = "resolved" if str(candidate.get("item_type")) == "open_question" else "superseded"
                candidate["valid_to"] = later.get("valid_from")
                candidate["resolved_by"] = later.get("candidate_id")
                break
    return ordered


def lifecycle_overlap(left: dict[str, object], right: dict[str, object]) -> bool:
    if left.get("subject_key") and left.get("subject_key") == right.get("subject_key"):
        return True
    left_terms = set(str(left.get("subject_key") or "").split("-"))
    right_terms = set(str(right.get("subject_key") or "").split("-"))
    if not left_terms or not right_terms:
        return False
    shared = left_terms & right_terms
    return len(shared) / max(len(left_terms), len(right_terms)) >= 0.45


def dedupe_candidates(candidates: list[dict[str, object]]) -> list[dict[str, object]]:
    deduped: dict[str, dict[str, object]] = {}
    for candidate in candidates:
        key = stable_id(
            candidate.get("scope"),
            candidate.get("project"),
            candidate.get("memory_class"),
            candidate.get("item_type"),
            candidate.get("subject_key"),
            normalize_for_key(str(candidate.get("agent_facing_statement") or candidate.get("statement") or "")),
        )
        if key not in deduped:
            deduped[key] = candidate
        else:
            merge_candidate_refs(deduped[key], candidate)
    return sorted(deduped.values(), key=lambda item: (str(item.get("project") or ""), str(item.get("memory_class") or ""), str(item.get("subject_key") or "")))


def merge_candidate_refs(target: dict[str, object], incoming: dict[str, object]) -> None:
    target_fingerprints = evidence_ref_fingerprints(target.get("evidence_refs", []), str(target.get("statement") or ""))
    incoming_refs = list(incoming.get("evidence_refs", []))
    unique_incoming_refs = [
        ref for ref in incoming_refs if evidence_ref_fingerprint(ref, str(incoming.get("statement") or "")) not in target_fingerprints
    ]
    target["evidence_ids"] = sorted(
        set(str(item) for item in target.get("evidence_ids", []))
        | {str(ref.get("evidence_id")) for ref in unique_incoming_refs if isinstance(ref, dict)}
    )
    existing_refs = list(target.get("evidence_refs", []))
    for ref in unique_incoming_refs:
        if ref not in existing_refs:
            existing_refs.append(ref)
    target["evidence_refs"] = existing_refs
    target["source_window_ids"] = sorted(set(str(item) for item in target.get("source_window_ids", [])) | set(str(item) for item in incoming.get("source_window_ids", [])))
    target["valid_from"] = earliest_timestamp(target.get("valid_from"), incoming.get("valid_from"))
    if confidence_rank(str(incoming.get("confidence") or "")) < confidence_rank(str(target.get("confidence") or "")):
        target["confidence"] = incoming.get("confidence")


def merge_candidates(
    candidates: list[dict[str, object]],
    *,
    require_inferred_rule_review: bool,
    unresolved_project: str,
) -> list[dict[str, object]]:
    merged: dict[str, dict[str, object]] = {}
    for candidate in candidates:
        if candidate.get("scope") == "project" and candidate.get("project") == unresolved_project:
            continue
        key = stable_id(candidate.get("scope"), candidate.get("project"), candidate.get("memory_class"), candidate.get("item_type"), candidate.get("subject_key"))
        if key not in merged:
            item = candidate_to_item(key, candidate)
            merged[key] = item
        else:
            merge_item(merged[key], candidate)
    for item in merged.values():
        finalize_promotion(item, require_inferred_rule_review)
    return sorted(merged.values(), key=lambda item: (str(item["scope"]), str(item.get("project") or ""), str(item["memory_class"]), str(item.get("item_type") or ""), str(item["statement"])))


def candidate_to_item(item_id: str, candidate: dict[str, object]) -> dict[str, object]:
    refs = list(candidate.get("evidence_refs", []))
    timestamps = [ref.get("timestamp") for ref in refs if isinstance(ref, dict)]
    return {
        "item_id": item_id,
        "memory_schema_version": 2,
        "memory_extraction_schema_version": MEMORY_EXTRACTION_SCHEMA_VERSION,
        "memory_class": candidate["memory_class"],
        "item_type": candidate.get("item_type"),
        "scope": candidate["scope"],
        "project": candidate.get("project"),
        "promotion_state": "explicit" if candidate.get("promotion_reason") == "explicit_user_instruction" else "candidate",
        "durability": "durable" if candidate.get("memory_class") != "recent_project_state" else "recent",
        "temporal_status": candidate.get("temporal_status"),
        "statement": candidate.get("agent_facing_statement") or candidate.get("statement"),
        "agent_facing_statement": candidate.get("agent_facing_statement") or candidate.get("statement"),
        "subject_key": candidate.get("subject_key"),
        "source_actor_types": ["user"],
        "evidence_ids": list(candidate.get("evidence_ids", [])),
        "provenance_refs": [ref.get("provenance", {}) for ref in refs if isinstance(ref, dict)],
        "evidence_refs": refs,
        "source_window_ids": list(candidate.get("source_window_ids", [])),
        "first_seen_at": first_non_empty(timestamps) or candidate.get("valid_from"),
        "last_seen_at": last_non_empty(timestamps) or candidate.get("valid_from"),
        "confidence": candidate.get("confidence") or "low",
        "review_required": bool(candidate.get("needs_review")),
        "review_reason": "inferred_rule_requires_confirmation" if candidate.get("needs_review") else None,
        "supporting_session_count": supporting_session_count(refs),
        "supporting_day_count": supporting_day_count(refs),
        "resolved_by": candidate.get("resolved_by"),
        "valid_to": candidate.get("valid_to"),
        "extraction_rule_ids": list(candidate.get("extraction_rule_ids", [])),
    }


def merge_item(target: dict[str, object], candidate: dict[str, object]) -> None:
    target_fingerprints = evidence_ref_fingerprints(target.get("evidence_refs", []), str(target.get("statement") or ""))
    refs = [
        ref
        for ref in list(candidate.get("evidence_refs", []))
        if evidence_ref_fingerprint(ref, str(candidate.get("statement") or "")) not in target_fingerprints
    ]
    target["evidence_ids"] = sorted(
        set(str(item) for item in target.get("evidence_ids", []))
        | {str(ref.get("evidence_id")) for ref in refs if isinstance(ref, dict)}
    )
    existing_refs = list(target.get("evidence_refs", []))
    for ref in refs:
        if ref not in existing_refs:
            existing_refs.append(ref)
    target["evidence_refs"] = existing_refs
    target["provenance_refs"] = [ref.get("provenance", {}) for ref in existing_refs if isinstance(ref, dict)]
    target["source_window_ids"] = sorted(set(str(item) for item in target.get("source_window_ids", [])) | set(str(item) for item in candidate.get("source_window_ids", [])))
    target["first_seen_at"] = earliest_timestamp(target.get("first_seen_at"), candidate.get("valid_from"))
    target["last_seen_at"] = latest_timestamp(target.get("last_seen_at"), candidate.get("valid_from"))
    target["supporting_session_count"] = supporting_session_count(existing_refs)
    target["supporting_day_count"] = supporting_day_count(existing_refs)
    if confidence_rank(str(candidate.get("confidence") or "")) < confidence_rank(str(target.get("confidence") or "")):
        target["confidence"] = candidate.get("confidence")
        target["statement"] = candidate.get("agent_facing_statement") or candidate.get("statement")
        target["agent_facing_statement"] = target["statement"]
    if candidate.get("promotion_reason") == "explicit_user_instruction":
        target["promotion_state"] = "explicit"
        target["review_required"] = False
        target["review_reason"] = None
    if candidate.get("temporal_status") in {"resolved", "superseded"}:
        target["temporal_status"] = candidate.get("temporal_status")
        target["resolved_by"] = candidate.get("resolved_by")
        target["valid_to"] = candidate.get("valid_to")


def finalize_promotion(item: dict[str, object], require_inferred_rule_review: bool) -> None:
    memory_class = str(item.get("memory_class") or "")
    if memory_class not in {"global_user_rules", "project_rules"}:
        return
    if item.get("promotion_state") == "explicit":
        item["confidence"] = "explicit"
        item["review_required"] = False
        item["review_reason"] = None
        return
    if int(item.get("supporting_session_count") or 0) >= 2 and int(item.get("supporting_day_count") or 0) >= 2:
        item["promotion_state"] = "repeated"
        item["confidence"] = "strong"
    if require_inferred_rule_review:
        item["review_required"] = True
        item["review_reason"] = "inferred_rule_requires_confirmation"


def map_item_type(item_type: str, project: str) -> dict[str, object]:
    normalized = normalize_item_type(item_type) or "current_state"
    if normalized == "global_rule":
        return {"scope": "global", "project": None, "memory_class": "global_user_rules", "item_type": "global_rule", "temporal_status": "durable"}
    if normalized == "project_rule":
        return {"scope": "project", "project": project, "memory_class": "project_rules", "item_type": "project_rule", "temporal_status": "durable"}
    if normalized in PROJECT_SUMMARY_TYPES:
        return {"scope": "project", "project": project, "memory_class": "stable_project_summary", "item_type": normalized, "temporal_status": "durable"}
    if normalized in LESSON_TYPES:
        return {"scope": "project", "project": project, "memory_class": "project_lessons", "item_type": "lesson", "temporal_status": "durable"}
    return {"scope": "project", "project": project, "memory_class": "recent_project_state", "item_type": normalized, "temporal_status": "active"}


def normalize_item_type(value: str) -> str | None:
    value = value.strip().lower().replace("-", "_").replace(" ", "_")
    aliases = {
        "global_user_rules": "global_rule",
        "global_rules": "global_rule",
        "global_preference": "global_rule",
        "project_rules": "project_rule",
        "stable_project_summary": "project_summary",
        "summary": "project_summary",
        "task_request": "task",
        "failure": "failure_risk",
        "risk": "failure_risk",
        "outcome": "current_state",
    }
    value = aliases.get(value, value)
    allowed = RULE_ITEM_TYPES | PROJECT_SUMMARY_TYPES | TEMPORAL_ITEM_TYPES | LESSON_TYPES | {"decision"}
    return value if value in allowed else None


def classify_clause_type(clause: str) -> str | None:
    lowered = clause.lower()
    if LESSON_PATTERN.search(clause):
        return "lesson"
    if is_global_rule_text(clause):
        return "global_rule"
    if is_project_rule_text(clause):
        return "project_rule"
    if OPEN_QUESTION_PATTERN.search(clause):
        return "open_question"
    if RESOLUTION_PATTERN.search(clause):
        return "current_state"
    if any(term in lowered for term in ("constraint", "must", "do not", "never", "only", "blocks", "kill switch", "disabled", "strict")):
        return "constraint"
    if PROJECT_SUMMARY_PATTERN.search(clause) and not conversational_or_one_off_prefix(clause):
        if "architecture" in lowered or "pipeline" in lowered:
            return "architecture"
        return "project_summary"
    if NEXT_STEP_PATTERN.search(clause) and is_recent_context_candidate(clause):
        return "next_step"
    if is_recent_context_candidate(clause):
        return "current_state"
    return None


def is_global_rule_text(text: str) -> bool:
    if len(text) > 420 or RUNTIME_LOCAL_PATTERN.search(text):
        return False
    if not GLOBAL_RULE_PATTERN.search(text):
        return False
    if "for this project" in text.lower() or "project rule" in text.lower():
        return False
    return bool(EXPLICIT_PROMOTION_PATTERN.search(text) or re.search(r"\b(?:concise|real data|github|outside the plan|token|explanation)\b", text, re.IGNORECASE))


def is_project_rule_text(text: str) -> bool:
    if len(text) > 420 or RUNTIME_LOCAL_PATTERN.search(text):
        return False
    if is_global_rule_text(text):
        return False
    return bool(PROJECT_RULE_PATTERN.search(text))


def is_one_off_instruction(text: str) -> bool:
    lowered = text.lower()
    if EXPLICIT_PROMOTION_PATTERN.search(text) and not lowered.startswith(("please", "can you")):
        return False
    return bool(re.search(r"^(?:please|can you|could you|run|fix|implement|show|open|create|commit|push|merge|go|next)\b", lowered))


def guide_statement(text: str, item_type: str) -> str:
    text = normalize_statement(clean_clause(text))
    text = strip_explicit_prefix(text)
    text = VERBATIM_PREFIX_PATTERN.sub("", text).strip()
    if not text:
        return ""
    if (LONG_PLAN_PATTERN.search(text) and len(text) > 300) or PROMPT_SCAFFOLD_PATTERN.search(text):
        return ""
    lowered = text.lower()
    if item_type in RULE_ITEM_TYPES:
        text = rewrite_rule_statement(text)
    elif item_type == "project_summary":
        text = rewrite_summary_statement(text)
    elif item_type == "architecture":
        text = ensure_sentence(f"Use this architecture context: {lower_first(text)}")
    elif item_type == "constraint":
        if SINGLE_USER_PATTERN.search(text):
            text = "Assume a single-user deployment and optimize the memory system for the owner and their coding agents."
        else:
            text = ensure_sentence(f"Respect this constraint: {lower_first(text)}")
    elif item_type == "open_question":
        text = ensure_sentence(f"Track this unresolved question: {lower_first(text).rstrip('?')}")
    elif item_type == "next_step":
        text = ensure_sentence(f"Continue with: {lower_first(text)}")
    elif item_type == "current_state":
        text = rewrite_current_state(text)
    elif item_type == "failure_risk":
        text = ensure_sentence(f"Avoid repeating this failure or risk: {lower_first(text)}")
    elif item_type == "lesson":
        text = ensure_sentence(f"Carry forward this lesson: {lower_first(text)}")
    if len(text) < 8 or is_runtime_or_scaffold_only(text):
        return ""
    text = rewrite_remaining_first_person(text)
    if reject_memory_statement(text, item_type):
        return ""
    if item_type == "project_summary" and conversational_or_one_off_prefix(lowered):
        return ""
    return normalize_statement(text)


def rewrite_remaining_first_person(text: str) -> str:
    lowered = text.lower()
    if ("wash sale" in lowered or ("position" in lowered and re.search(r"\b(?:nov|feb|oct|jan)\b", lowered))) and re.search(
        r"\b(?:i keep|i close|i reopen|i think|i don't want|i do not want)\b",
        lowered,
    ):
        return "For wash-sale management, preserve tax-window context around when positions should be closed, held, or reopened."
    if SINGLE_USER_PATTERN.search(text):
        return "Assume a single-user deployment and optimize the memory system for the owner and their coding agents."
    return text


def reject_memory_statement(text: str, item_type: str) -> bool:
    lowered = text.lower()
    if not text.strip():
        return True
    if PROMPT_SCAFFOLD_PATTERN.search(text) or LONG_PLAN_PATTERN.search(text) or CODE_ARTIFACT_PATTERN.search(text):
        return True
    if TRANSIENT_REQUEST_PATTERN.search(text):
        return True
    if re.search(r"^(?:current context|continue with|track this unresolved question):\s*\d+[\.)]\s+", text, re.IGNORECASE):
        return True
    if re.search(r"\b(?:maxime lable|add p/l|click a button|open tabs)\b", lowered):
        return True
    if re.search(r"^(?:respect this constraint|continue with|current context|track this unresolved question):\s*\d+\)", text, re.IGNORECASE):
        return True
    if item_type == "open_question" and re.search(r"^(?:track this unresolved question:\s*)?(?:do i|did everything|what is|what went|how do|how .*space|can i|is there|if we go|where are)\b", lowered):
        return True
    if item_type in RULE_ITEM_TYPES and FIRST_PERSON_LOCAL_PATTERN.search(text):
        return True
    return False


def rewrite_rule_statement(text: str) -> str:
    lowered = text.lower()
    if FIRST_PERSON_LOCAL_PATTERN.search(text) and not re.search(r"\b(?:prefer|want you to|be concise|real data|github)\b", lowered):
        return ""
    if "explanation" in lowered or "token" in lowered or "narrate" in lowered:
        return "Keep responses concise by default and avoid unnecessary process narration when token budget matters."
    if "real data" in lowered:
        return "Validate memory and extraction changes against real data before treating them as correct."
    if "outside the plan" in lowered:
        return "Stay inside the agreed plan unless the user explicitly changes scope."
    if "github" in lowered or "git" in lowered:
        return "When the user asks for repository changes, commit and push without asking again unless credentials or conflicts block the action."
    if lowered.startswith("no ") and "evidence" in lowered:
        return ensure_sentence(text)
    if lowered.startswith(("do not", "don't", "never", "always", "must")):
        return ensure_sentence(text)
    if "no fallback" in lowered and "evidence" in lowered:
        return "Require evidence-backed answers; do not invent fallback conclusions when evidence is missing."
    return ensure_sentence(f"Follow this operating rule: {lower_first(text)}")


def rewrite_summary_statement(text: str) -> str:
    lowered = text.lower()
    if FIRST_PERSON_LOCAL_PATTERN.search(text):
        if "domain" in lowered and "data" in lowered:
            return "Design the system to handle future expansion into additional personal-data domains and analysis lenses."
        if SINGLE_USER_PATTERN.search(text):
            return "Assume a single-user deployment optimized for the owner and their coding agents."
        return ""
    if "goal is" in lowered:
        text = re.sub(r"(?i)^goal is to\s+", "The project goal is to ", text)
    if lowered.startswith("the project is") or lowered.startswith("project is"):
        return ensure_sentence(text)
    return ensure_sentence(f"Project context: {text}")


def rewrite_current_state(text: str) -> str:
    if RESOLUTION_PATTERN.search(text):
        return ensure_sentence(f"Latest state: {lower_first(text)}")
    return ensure_sentence(f"Current context: {lower_first(text)}")


def strip_explicit_prefix(text: str) -> str:
    return re.sub(
        r"(?i)^(?:add this to global rules|add this to project rules|global rule|project rule)\s*:?\s*",
        "",
        text,
    ).strip()


def candidate_clauses(text: str) -> list[str]:
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
    return clauses[:12]


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
        if pending_prefix and is_bullet:
            pending_items.append(clause.rstrip("."))
            continue
        if pending_prefix:
            clauses.append(compose_colon_clause(pending_prefix, pending_items))
            pending_prefix = None
            pending_items = []
            if len(clauses) >= 12:
                break
        if clause.endswith(":"):
            pending_prefix = clause.rstrip(":")
            pending_items = []
            continue
        if is_overview_fragment_noise(clause):
            continue
        clauses.append(clause)
        if len(clauses) >= 12:
            break
    if pending_prefix and len(clauses) < 12:
        clauses.append(compose_colon_clause(pending_prefix, pending_items))
    return [clause for clause in clauses if clause]


def compose_colon_clause(prefix: str, items: list[str]) -> str:
    if not items:
        return prefix
    return normalize_statement(f"{prefix} {', '.join(items[:8])}.")


def is_overview_fragment_noise(text: str) -> bool:
    stripped = text.strip()
    lowered = stripped.lower()
    if stripped.endswith("/") or re.search(r"^[\w.-]+/$", stripped):
        return True
    if len(stripped) < 40 and not re.search(r"\b(?:system|service|pipeline|engine|scaffold|memory|agent|trading|architecture|turns|built|designed)\b", lowered):
        return True
    return False


def clean_clause(text: str) -> str:
    clause = text.strip(" -\t\r\n\"'`")
    clause = re.sub(r"\bstrep by step\b", "step-by-step", clause, flags=re.IGNORECASE)
    clause = re.sub(r"\bouside\b", "outside", clause, flags=re.IGNORECASE)
    clause = re.sub(r"\bwrinting\b", "writing", clause, flags=re.IGNORECASE)
    clause = re.sub(r"\btthe\b", "the", clause, flags=re.IGNORECASE)
    return normalize_statement(clause)


def is_meaningful_clause(clause: str) -> bool:
    if not clause or len(clause) < 8:
        return False
    if clause.lower() in {"yes", "next", "go", "ok", "done", "agreed", "continue"}:
        return False
    if clause.count("/") > 8 and " " not in clause:
        return False
    return True


def is_recent_context_candidate(text: str) -> bool:
    if len(text) > 600:
        return False
    if NOISE_PATTERN.search(text):
        return False
    if text.lower() in {"what is next ?", "what is next?", "next", "go", "ok, continue", "continue"}:
        return False
    return True


def is_runtime_or_scaffold_only(text: str) -> bool:
    if RUNTIME_LOCAL_PATTERN.search(text) and not re.search(r"\b(?:always|never|do not|don't|must)\b", text, re.IGNORECASE):
        return True
    if NOISE_PATTERN.search(text) and len(text) < 120:
        return True
    return False


def conversational_or_one_off_prefix(text: str) -> bool:
    return bool(VERBATIM_PREFIX_PATTERN.search(text) or re.match(r"^(?:what|why|how|where)\b", text, re.IGNORECASE))


def evidence_text(record: dict[str, object]) -> str:
    surfaces = record.get("content_surfaces", [])
    texts = []
    if isinstance(surfaces, list):
        for surface in surfaces[:8]:
            if isinstance(surface, dict):
                text = str(surface.get("text", "")).strip()
                if text:
                    texts.append(text)
    return "\n".join(texts).strip()


def extract_request_text(text: str) -> str:
    marker = "My request for Codex:"
    if marker in text:
        return text.split(marker)[-1].strip()
    return text.strip()


def strip_code_blocks(text: str) -> str:
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    text = re.sub(r"`[^`]{20,}`", " ", text)
    return text


def subject_key(text: str) -> str:
    normalized = normalize_for_key(text)
    terms = [term for term in normalized.split("-") if term not in STOPWORDS and len(term) > 2]
    return "-".join(terms[:8]) or normalized[:80] or "memory"


STOPWORDS = {
    "the",
    "and",
    "for",
    "this",
    "that",
    "with",
    "from",
    "into",
    "should",
    "must",
    "always",
    "never",
    "agent",
    "project",
    "memory",
    "current",
    "context",
    "continue",
    "latest",
}


def normalize_for_key(text: str) -> str:
    slug = "".join(char.lower() if char.isalnum() else "-" for char in text)
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug.strip("-")[:120] or "memory"


def normalize_statement(text: str) -> str:
    text = " ".join(str(text).split())
    if len(text) > 700:
        text = text[:697].rstrip() + "..."
    return text


def ensure_sentence(text: str) -> str:
    text = normalize_statement(text)
    if text and text[-1] not in ".!?":
        text += "."
    return text


def lower_first(text: str) -> str:
    text = text.strip()
    if not text:
        return text
    return text[0].lower() + text[1:]


def supporting_session_count(refs: Iterable[object]) -> int:
    sessions = set()
    for ref in refs:
        if not isinstance(ref, dict):
            continue
        provenance = ref.get("provenance", {})
        if isinstance(provenance, dict):
            sessions.add(str(provenance.get("source_id") or ref.get("evidence_id") or "unknown"))
    return len(sessions)


def supporting_day_count(refs: Iterable[object]) -> int:
    days = set()
    for ref in refs:
        if not isinstance(ref, dict):
            continue
        timestamp = str(ref.get("timestamp") or "")
        if timestamp:
            days.add(timestamp[:10])
    return len(days)


def evidence_ref_fingerprints(refs: Iterable[object], statement: str) -> set[str]:
    return {evidence_ref_fingerprint(ref, statement) for ref in refs if isinstance(ref, dict)}


def evidence_ref_fingerprint(ref: object, statement: str) -> str:
    if not isinstance(ref, dict):
        return ""
    provenance = ref.get("provenance", {})
    source_id = ""
    if isinstance(provenance, dict):
        source_id = str(provenance.get("source_id") or "")
    timestamp = str(ref.get("timestamp") or "").split(".", 1)[0]
    return "|".join([source_id, timestamp, normalize_for_key(statement)])


def first_non_empty(values: Iterable[object]) -> object:
    present = [value for value in values if value]
    return min(present) if present else None


def last_non_empty(values: Iterable[object]) -> object:
    present = [value for value in values if value]
    return max(present) if present else None


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


def parse_time(value: object) -> datetime:
    if not value:
        return datetime.min.replace(tzinfo=timezone.utc)
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError:
        return datetime.min.replace(tzinfo=timezone.utc)


def confidence_rank(value: str) -> int:
    return {"explicit": 0, "strong": 1, "medium": 2, "low": 3, "candidate": 3}.get(value, 3)


def slugify(value: str) -> str:
    slug = "".join(char.lower() if char.isalnum() else "-" for char in value).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug or "project"


def stable_id(*parts: object) -> str:
    return hashlib.sha256("|".join(str(part) for part in parts).encode("utf-8")).hexdigest()[:16]


def notice(run_id: str, severity: str, notice_type: str, summary: str) -> dict[str, object]:
    return {"run_id": run_id, "severity": severity, "notice_type": notice_type, "summary": summary, "created_at": utc_now()}
