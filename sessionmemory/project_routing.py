from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path
from typing import Any

from .discovery import DiscoveryError, atomic_write_text, ensure_directory, utc_now
from .normalization import append_jsonl_text
from .product_config import ProductConfig, ProjectAliasConfig


class ProjectRoutingError(DiscoveryError):
    """Fatal LLM project-routing error."""


def apply_llm_project_routing(
    records_by_path: dict[Path, list[dict[str, object]]],
    config: ProductConfig,
    state_dir: Path,
    audits_dir: Path,
    run_id: str,
) -> list[dict[str, object]]:
    routing_config = config.project_routing
    unresolved = routing_config.unresolved_project
    if not routing_config.enabled:
        return []
    if not config.project_aliases:
        return []

    ensure_directory(state_dir)
    ensure_directory(audits_dir)
    state_path = state_dir / "project_routing_state.json"
    run_log_path = state_dir / "project_routing_runs.jsonl"
    decisions = load_decision_state(state_path)
    notices: list[dict[str, object]] = []
    routed_count = 0
    candidate_sources = build_source_packets(records_by_path, unresolved, config)

    for source_id, packet in list(candidate_sources.items())[: routing_config.max_sources_per_run]:
        digest = stable_packet_digest(packet)
        cached = decisions.get(source_id)
        if cached and cached.get("input_digest") == digest:
            decision = cached
        else:
            decision = call_project_router(packet, config)
            decision["input_digest"] = digest
            decisions[source_id] = decision
        chosen_project = str(decision.get("project_hint") or unresolved)
        confidence = str(decision.get("confidence") or "low")
        if chosen_project != unresolved and confidence_rank(confidence) <= confidence_rank(routing_config.min_confidence):
            routed_count += rewrite_records_for_source(records_by_path, source_id, chosen_project, confidence)
        elif chosen_project == unresolved:
            notices.append(
                notice(run_id, "warning", "unresolved_project_routing", f"LLM kept source {source_id} unresolved")
            )

    atomic_write_text(state_path, json.dumps({"schema_version": 1, "decisions": decisions}, indent=2, sort_keys=True) + "\n")
    previous_run_log = run_log_path.read_text(encoding="utf-8") if run_log_path.exists() else ""
    atomic_write_text(
        run_log_path,
        append_jsonl_text(
            previous_run_log,
            {
                "run_id": run_id,
                "finished_at": utc_now(),
                "candidate_source_count": len(candidate_sources),
                "routed_record_count": routed_count,
                "notice_count": len(notices),
            },
        ),
    )
    return notices


def build_source_packets(
    records_by_path: dict[Path, list[dict[str, object]]],
    unresolved: str,
    config: ProductConfig,
) -> dict[str, dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for path, records in records_by_path.items():
        if path.parts[-2:-1] != ("logs",):
            continue
        for record in records:
            if str(record.get("project_hint") or "") == unresolved:
                grouped[str(record["source_id"])].append(record)

    packets: dict[str, dict[str, object]] = {}
    for source_id, records in grouped.items():
        samples = []
        for record in select_sample_records(records, config.project_routing.max_sample_records_per_source):
            samples.append(
                {
                    "evidence_id": record.get("evidence_id"),
                    "actor_type": record.get("actor_type"),
                    "timestamp": record.get("timestamp"),
                    "text": sample_text(record),
                }
            )
        if samples:
            packets[source_id] = {
                "source_id": source_id,
                "allowed_projects": allowed_projects(config.project_aliases, config.project_routing.unresolved_project),
                "samples": samples,
            }
    return packets


def select_sample_records(records: list[dict[str, object]], limit: int) -> list[dict[str, object]]:
    user_records = [record for record in records if record.get("actor_type") == "user"]
    selected = user_records[:limit]
    if len(selected) < limit:
        selected.extend(records[: limit - len(selected)])
    return selected[:limit]


def sample_text(record: dict[str, object]) -> str:
    surfaces = record.get("content_surfaces", [])
    texts = []
    if isinstance(surfaces, list):
        for surface in surfaces[:3]:
            if isinstance(surface, dict):
                text = str(surface.get("text", "")).strip()
                if text:
                    texts.append(text)
    return " ".join(texts)[:1200]


def call_project_router(packet: dict[str, object], config: ProductConfig) -> dict[str, object]:
    routing_config = config.project_routing
    api_key = os.environ.get(routing_config.provider.api_key_env, "").strip()
    if not api_key:
        raise ProjectRoutingError(f"Missing OpenAI API key in {routing_config.provider.api_key_env}")
    system_prompt = (
        "You route AI coding log evidence to exactly one configured project. "
        "Return JSON only. If evidence is weak, choose the unresolved fallback."
    )
    user_payload = {
        "task": "Select the best project for this source.",
        "allowed_projects": packet["allowed_projects"],
        "source_id": packet["source_id"],
        "samples": packet["samples"],
        "required_output": {
            "project_hint": "one allowed project slug",
            "confidence": "high|medium|low",
            "supporting_evidence_ids": ["evidence ids from samples"],
        },
    }
    payload = {
        "model": os.environ.get(routing_config.provider.model_env, "").strip()
        or routing_config.provider.default_model,
        "temperature": routing_config.provider.temperature,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": json.dumps(user_payload, sort_keys=True)},
        ],
    }
    request = urllib.request.Request(
        url=f"{os.environ.get(routing_config.provider.base_url_env, '').strip() or 'https://api.openai.com'}/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            response_payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise ProjectRoutingError(f"OpenAI project routing failed: {exc.code}") from exc
    except urllib.error.URLError as exc:
        raise ProjectRoutingError(f"OpenAI project routing failed: {exc.reason}") from exc
    try:
        content = response_payload["choices"][0]["message"]["content"]
        decision = json.loads(content)
    except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
        raise ProjectRoutingError("OpenAI project routing response was invalid") from exc
    return validate_decision(decision, packet)


def validate_decision(decision: dict[str, object], packet: dict[str, object]) -> dict[str, object]:
    allowed = set(str(item) for item in packet["allowed_projects"])
    project_hint = str(decision.get("project_hint") or "")
    confidence = str(decision.get("confidence") or "low")
    if project_hint not in allowed:
        project_hint = str(packet["allowed_projects"][-1])
        confidence = "low"
    if confidence not in {"high", "medium", "low"}:
        confidence = "low"
    sample_ids = {str(item["evidence_id"]) for item in packet["samples"]}
    support = [str(item) for item in decision.get("supporting_evidence_ids", []) if str(item) in sample_ids]
    return {
        "source_id": packet["source_id"],
        "project_hint": project_hint,
        "confidence": confidence,
        "supporting_evidence_ids": support,
        "decided_at": utc_now(),
    }


def rewrite_records_for_source(
    records_by_path: dict[Path, list[dict[str, object]]],
    source_id: str,
    project_hint: str,
    confidence: str,
) -> int:
    count = 0
    for records in records_by_path.values():
        for record in records:
            if str(record.get("source_id")) != source_id:
                continue
            if str(record.get("project_hint")) != "projects":
                continue
            record["project_hint"] = project_hint
            metadata = dict(record.get("metadata", {}))
            metadata["llm_project_routing"] = {"confidence": confidence}
            record["metadata"] = metadata
            count += 1
    return count


def allowed_projects(aliases: tuple[ProjectAliasConfig, ...], unresolved: str) -> list[str]:
    projects = []
    for alias in aliases:
        if alias.slug not in projects:
            projects.append(alias.slug)
    if unresolved not in projects:
        projects.append(unresolved)
    return projects


def load_decision_state(path: Path) -> dict[str, dict[str, object]]:
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    return {str(key): dict(value) for key, value in dict(payload.get("decisions", {})).items()}


def stable_packet_digest(packet: dict[str, object]) -> str:
    import hashlib

    return hashlib.sha256(json.dumps(packet, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def confidence_rank(value: str) -> int:
    return {"high": 0, "medium": 1, "low": 2}.get(value, 2)


def notice(run_id: str, severity: str, notice_type: str, summary: str) -> dict[str, object]:
    return {"run_id": run_id, "severity": severity, "notice_type": notice_type, "summary": summary}
