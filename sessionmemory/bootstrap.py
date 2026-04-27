from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from .discovery import DiscoveryError, atomic_write_text, ensure_directory, utc_now
from .extraction import ExtractionStateRecord, append_jsonl_text, load_extraction_state
from .wiki import WikiProviderConfig, call_openai_structured_json, load_wiki_state

STATE_SCHEMA_VERSION = 1
BOOTSTRAP_SCHEMA_VERSION = 1
PROJECT_LABELS = {"ai-trader", "open-brain", "ai-scientist"}
VALID_CLAIM_CONFIDENCE = {"strong", "inferred"}
TEMPORAL_PRIORITY = {"durable": 4, "active": 3, "historical": 2, "superseded": 1}
CONFIDENCE_PRIORITY = {"explicit": 3, "strong": 2, "inferred": 1}
NORMALIZE_BULLET_PATTERN = re.compile(r"\s+")


class BootstrapError(DiscoveryError):
    """Fatal bootstrap generation error that must stop the run."""


@dataclass(frozen=True)
class BootstrapDefaults:
    exclude_unclassified: bool
    include_cross_project: bool
    include_conflicts_only_if_selected: bool


@dataclass(frozen=True)
class BootstrapDomainConfig:
    domain: str
    title: str
    path: str
    kind: str
    max_chars: int


@dataclass(frozen=True)
class BootstrapSectionConfig:
    section_id: str
    title: str
    max_items: int
    max_claims: int
    item_types: tuple[str, ...]
    claim_buckets: tuple[str, ...]


@dataclass(frozen=True)
class BootstrapConfig:
    schema_version: int
    bootstrap_schema_version: int
    renderer: str
    renderer_version: int
    selection_version: int
    synthesis_prompt_version: int
    synthesis_schema_version: int
    provider: WikiProviderConfig
    defaults: BootstrapDefaults
    domains: tuple[BootstrapDomainConfig, ...]
    sections: dict[str, tuple[BootstrapSectionConfig, ...]]

    @property
    def domain_map(self) -> dict[str, BootstrapDomainConfig]:
        return {domain.domain: domain for domain in self.domains}

    def sections_for_domain(self, domain_config: BootstrapDomainConfig) -> tuple[BootstrapSectionConfig, ...]:
        try:
            return self.sections[domain_config.kind]
        except KeyError as exc:
            raise BootstrapError(f"Missing bootstrap sections for domain kind {domain_config.kind}") from exc


@dataclass(frozen=True)
class BootstrapStateRecord:
    domain: str
    bootstrap_schema_version: int
    renderer: str
    renderer_version: int
    selection_version: int
    synthesis_prompt_version: int
    synthesis_schema_version: int
    provider_type: str
    provider_model: str
    input_digest: str
    bullet_count: int
    status: str
    relative_path: str
    relative_manifest_path: str
    last_rendered_at: str
    last_run_id: str

    def to_dict(self) -> dict[str, object]:
        return {
            "domain": self.domain,
            "bootstrap_schema_version": self.bootstrap_schema_version,
            "renderer": self.renderer,
            "renderer_version": self.renderer_version,
            "selection_version": self.selection_version,
            "synthesis_prompt_version": self.synthesis_prompt_version,
            "synthesis_schema_version": self.synthesis_schema_version,
            "provider_type": self.provider_type,
            "provider_model": self.provider_model,
            "input_digest": self.input_digest,
            "bullet_count": self.bullet_count,
            "status": self.status,
            "relative_path": self.relative_path,
            "relative_manifest_path": self.relative_manifest_path,
            "last_rendered_at": self.last_rendered_at,
            "last_run_id": self.last_run_id,
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "BootstrapStateRecord":
        return cls(
            domain=str(data["domain"]),
            bootstrap_schema_version=int(data["bootstrap_schema_version"]),
            renderer=str(data["renderer"]),
            renderer_version=int(data["renderer_version"]),
            selection_version=int(data["selection_version"]),
            synthesis_prompt_version=int(data["synthesis_prompt_version"]),
            synthesis_schema_version=int(data["synthesis_schema_version"]),
            provider_type=str(data["provider_type"]),
            provider_model=str(data["provider_model"]),
            input_digest=str(data["input_digest"]),
            bullet_count=int(data["bullet_count"]),
            status=str(data["status"]),
            relative_path=str(data["relative_path"]),
            relative_manifest_path=str(data["relative_manifest_path"]),
            last_rendered_at=str(data["last_rendered_at"]),
            last_run_id=str(data["last_run_id"]),
        )


@dataclass(frozen=True)
class BootstrapNotice:
    run_id: str
    domain: str
    severity: str
    notice_type: str
    summary: str

    def to_dict(self) -> dict[str, object]:
        return {
            "run_id": self.run_id,
            "domain": self.domain,
            "severity": self.severity,
            "notice_type": self.notice_type,
            "summary": self.summary,
        }


@dataclass(frozen=True)
class BootstrapRunReport:
    run_id: str
    started_at: str
    finished_at: str
    domain_status_counts: dict[str, int]
    rendered_domain_count: int
    bullet_count: int
    notice_count: int
    success: bool
    fatal_error_summary: str | None

    def to_dict(self) -> dict[str, object]:
        return {
            "run_id": self.run_id,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "domain_status_counts": self.domain_status_counts,
            "rendered_domain_count": self.rendered_domain_count,
            "bullet_count": self.bullet_count,
            "notice_count": self.notice_count,
            "success": self.success,
            "fatal_error_summary": self.fatal_error_summary,
        }


@dataclass(frozen=True)
class BootstrapResult:
    report: BootstrapRunReport
    state_path: Path
    run_log_path: Path
    notice_log_path: Path


@dataclass(frozen=True)
class BootstrapPacket:
    domain: str
    title: str
    kind: str
    relative_path: str
    relative_manifest_path: str
    max_chars: int
    sections: tuple[dict[str, object], ...]
    input_item_keys: tuple[str, ...]
    input_claim_ids: tuple[str, ...]
    source_count: int
    conflict_count: int

    def to_dict(self) -> dict[str, object]:
        return {
            "domain": self.domain,
            "title": self.title,
            "kind": self.kind,
            "relative_path": self.relative_path,
            "relative_manifest_path": self.relative_manifest_path,
            "max_chars": self.max_chars,
            "sections": [sanitize_section_for_prompt(section) for section in self.sections],
            "input_item_keys": list(self.input_item_keys),
            "input_claim_ids": list(self.input_claim_ids),
            "source_count": self.source_count,
            "conflict_count": self.conflict_count,
        }


def run_bootstrap(
    config_path: Path | str,
    state_dir: Path | str,
    extracted_dir: Path | str,
    wiki_dir: Path | str,
    bootstrap_dir: Path | str,
    audits_dir: Path | str,
    source_ids: Iterable[str] | None = None,
) -> BootstrapResult:
    config_path = Path(config_path)
    state_dir = Path(state_dir)
    extracted_dir = Path(extracted_dir)
    wiki_dir = Path(wiki_dir)
    bootstrap_dir = Path(bootstrap_dir)
    audits_dir = Path(audits_dir)

    extraction_state_path = state_dir / "extraction_state.json"
    wiki_state_path = state_dir / "wiki_state.json"
    state_path = state_dir / "bootstrap_state.json"
    run_log_path = state_dir / "bootstrap_runs.jsonl"
    notice_log_path = audits_dir / "bootstrap_notices.jsonl"

    ensure_directory(state_dir)
    ensure_directory(audits_dir)
    ensure_directory(bootstrap_dir)
    ensure_directory(bootstrap_dir / "_meta")

    run_id = f"bootstrap-{utc_now().replace(':', '').replace('.', '').replace('-', '')}"
    started_at = utc_now()
    staging_root = bootstrap_dir / ".staging" / run_id

    previous_state_text = state_path.read_text(encoding="utf-8") if state_path.exists() else None
    previous_run_log_text = run_log_path.read_text(encoding="utf-8") if run_log_path.exists() else ""
    previous_notice_log_text = notice_log_path.read_text(encoding="utf-8") if notice_log_path.exists() else ""

    try:
        if not wiki_state_path.exists():
            raise BootstrapError(f"Missing wiki state: {wiki_state_path}")

        config = load_bootstrap_config(config_path)
        extraction_state = load_extraction_state(extraction_state_path)
        load_wiki_state(wiki_state_path)
        previous_state = load_bootstrap_state(state_path)
        target_domains = resolve_target_domains(source_ids, extraction_state, config)
        packet_plan = build_bootstrap_plan(target_domains, config, extracted_dir, wiki_dir)
        next_state = dict(previous_state)

        domain_status_counts: Counter[str] = Counter()
        notices_for_run: list[BootstrapNotice] = []
        changed_domains: list[str] = []
        rendered_domain_count = 0
        bullet_count = 0
        provider_model = config.provider.resolve_model()

        for packet in packet_plan:
            prior_state = previous_state.get(packet.domain)
            mode = determine_bootstrap_mode(packet, prior_state, config, provider_model, bootstrap_dir)
            if mode == "unchanged":
                next_state[packet.domain] = previous_state[packet.domain]
                domain_status_counts["unchanged"] += 1
                continue

            artifacts = build_bootstrap_artifacts(packet, config, staging_root)
            validate_bootstrap_artifacts(packet, artifacts, config)
            next_state[packet.domain] = build_state_record(
                packet=packet,
                config=config,
                provider_model=provider_model,
                input_digest=packet_digest(packet),
                bullet_count=len(artifacts["manifest"]["bullets"]),
                run_id=run_id,
            )
            notices_for_run.extend(build_bootstrap_notices(packet, artifacts, run_id))
            changed_domains.append(packet.domain)
            domain_status_counts["rendered"] += 1
            rendered_domain_count += 1
            bullet_count += len(artifacts["manifest"]["bullets"])

        if source_ids is None:
            validate_state_against_packet_plan(packet_plan, next_state, config, provider_model)

        report = BootstrapRunReport(
            run_id=run_id,
            started_at=started_at,
            finished_at=utc_now(),
            domain_status_counts=dict(sorted(domain_status_counts.items())),
            rendered_domain_count=rendered_domain_count,
            bullet_count=bullet_count,
            notice_count=len(notices_for_run),
            success=True,
            fatal_error_summary=None,
        )

        staged_state_path = staging_root / "bootstrap_state.json"
        staged_run_log_path = staging_root / "bootstrap_runs.jsonl"
        staged_notice_log_path = staging_root / "bootstrap_notices.jsonl"
        write_text(staged_state_path, json.dumps(build_state_payload(next_state), indent=2, sort_keys=True) + "\n")
        write_text(staged_run_log_path, append_jsonl_text(previous_run_log_text, report.to_dict()))
        write_text(
            staged_notice_log_path,
            append_jsonl_text(previous_notice_log_text, [notice.to_dict() for notice in notices_for_run]),
        )

        promote_staged_bootstrap(staging_root, bootstrap_dir, changed_domains, packet_plan)
        os.replace(staged_state_path, state_path)
        ensure_directory(run_log_path.parent)
        os.replace(staged_run_log_path, run_log_path)
        ensure_directory(notice_log_path.parent)
        os.replace(staged_notice_log_path, notice_log_path)
        cleanup_staging_root(staging_root)
        return BootstrapResult(
            report=report,
            state_path=state_path,
            run_log_path=run_log_path,
            notice_log_path=notice_log_path,
        )
    except Exception as exc:
        cleanup_staging_root(staging_root)
        failure_report = BootstrapRunReport(
            run_id=run_id,
            started_at=started_at,
            finished_at=utc_now(),
            domain_status_counts={},
            rendered_domain_count=0,
            bullet_count=0,
            notice_count=0,
            success=False,
            fatal_error_summary=str(exc),
        )
        atomic_write_text(run_log_path, append_jsonl_text(previous_run_log_text, failure_report.to_dict()))
        if previous_state_text is None and state_path.exists():
            state_path.unlink(missing_ok=True)
        if previous_state_text is not None and state_path.exists():
            atomic_write_text(state_path, previous_state_text)
        if previous_notice_log_text:
            atomic_write_text(notice_log_path, previous_notice_log_text)
        return BootstrapResult(
            report=failure_report,
            state_path=state_path,
            run_log_path=run_log_path,
            notice_log_path=notice_log_path,
        )


def load_bootstrap_config(config_path: Path) -> BootstrapConfig:
    try:
        payload = json.loads(config_path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError as exc:
        raise BootstrapError(f"Missing bootstrap config: {config_path}") from exc
    except json.JSONDecodeError as exc:
        raise BootstrapError(f"Invalid bootstrap config JSON: {config_path}") from exc

    domains_payload = payload.get("domains")
    sections_payload = payload.get("sections")
    provider_payload = payload.get("provider")
    defaults_payload = payload.get("defaults")
    if not isinstance(domains_payload, list) or not domains_payload:
        raise BootstrapError("Bootstrap config must define domains")
    if not isinstance(sections_payload, dict):
        raise BootstrapError("Bootstrap config must define sections")
    if not isinstance(provider_payload, dict):
        raise BootstrapError("Bootstrap config must define provider")
    if not isinstance(defaults_payload, dict):
        raise BootstrapError("Bootstrap config must define defaults")

    provider = WikiProviderConfig(
        provider_type=str(provider_payload["type"]),
        api_key_env=str(provider_payload["api_key_env"]),
        base_url_env=str(provider_payload["base_url_env"]),
        model_env=str(provider_payload["model_env"]),
        default_model=str(provider_payload["default_model"]),
        temperature=float(provider_payload.get("temperature", 0.2)),
    )
    if provider.provider_type != "openai":
        raise BootstrapError(f"Unsupported bootstrap provider type: {provider.provider_type}")

    domains = tuple(
        BootstrapDomainConfig(
            domain=str(item["domain"]),
            title=str(item["title"]),
            path=str(item["path"]),
            kind=str(item["kind"]),
            max_chars=int(item["max_chars"]),
        )
        for item in domains_payload
    )
    if len({domain.domain for domain in domains}) != len(domains):
        raise BootstrapError("Bootstrap config domains must be unique")

    sections: dict[str, tuple[BootstrapSectionConfig, ...]] = {}
    for kind, section_list in sections_payload.items():
        if not isinstance(section_list, list) or not section_list:
            raise BootstrapError(f"Bootstrap config sections for {kind} must be a non-empty list")
        parsed = tuple(
            BootstrapSectionConfig(
                section_id=str(item["section_id"]),
                title=str(item["title"]),
                max_items=int(item["max_items"]),
                max_claims=int(item.get("max_claims", 0)),
                item_types=tuple(str(value) for value in item.get("item_types", [])),
                claim_buckets=tuple(str(value) for value in item.get("claim_buckets", [])),
            )
            for item in section_list
        )
        if len({section.section_id for section in parsed}) != len(parsed):
            raise BootstrapError(f"Bootstrap config section ids must be unique for {kind}")
        sections[str(kind)] = parsed

    defaults = BootstrapDefaults(
        exclude_unclassified=bool(defaults_payload.get("exclude_unclassified", True)),
        include_cross_project=bool(defaults_payload.get("include_cross_project", True)),
        include_conflicts_only_if_selected=bool(defaults_payload.get("include_conflicts_only_if_selected", True)),
    )
    return BootstrapConfig(
        schema_version=int(payload["schema_version"]),
        bootstrap_schema_version=int(payload["bootstrap_schema_version"]),
        renderer=str(payload["renderer"]),
        renderer_version=int(payload["renderer_version"]),
        selection_version=int(payload["selection_version"]),
        synthesis_prompt_version=int(payload["synthesis_prompt_version"]),
        synthesis_schema_version=int(payload["synthesis_schema_version"]),
        provider=provider,
        defaults=defaults,
        domains=domains,
        sections=sections,
    )


def load_bootstrap_state(state_path: Path) -> dict[str, BootstrapStateRecord]:
    if not state_path.exists():
        return {}
    try:
        payload = json.loads(state_path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise BootstrapError(f"Invalid bootstrap state JSON: {state_path}") from exc
    if int(payload.get("schema_version", -1)) != STATE_SCHEMA_VERSION:
        raise BootstrapError(
            f"Unsupported bootstrap state schema version in {state_path}: {payload.get('schema_version')}"
        )
    records = [BootstrapStateRecord.from_dict(item) for item in payload.get("domains", [])]
    return {record.domain: record for record in records}


def resolve_target_domains(
    source_ids: Iterable[str] | None,
    extraction_state: dict[str, ExtractionStateRecord],
    config: BootstrapConfig,
) -> list[str]:
    configured_domains = [domain.domain for domain in config.domains]
    if source_ids is None:
        return [
            domain
            for domain in configured_domains
            if domain != "unclassified"
            and (config.defaults.include_cross_project or domain != "cross-project")
        ]

    target_source_ids = sorted(dict.fromkeys(str(source_id) for source_id in source_ids))
    missing = [source_id for source_id in target_source_ids if source_id not in extraction_state]
    if missing:
        raise BootstrapError(f"Requested source_ids are missing from extraction state: {', '.join(missing)}")
    touched_domains: list[str] = []
    for source_id in target_source_ids:
        touched_domains.extend(extraction_state[source_id].touched_domains)
    return [
        domain
        for domain in dedupe_preserving_order(touched_domains)
        if domain in config.domain_map
        and domain != "unclassified"
        and (config.defaults.include_cross_project or domain != "cross-project")
    ]


def build_bootstrap_plan(
    domains: list[str],
    config: BootstrapConfig,
    extracted_dir: Path,
    wiki_dir: Path,
) -> list[BootstrapPacket]:
    domain_items_map = load_domain_items(domains, extracted_dir)
    domain_claims_map = load_domain_claims(domains, wiki_dir)
    packets: list[BootstrapPacket] = []
    for domain in domains:
        domain_config = config.domain_map.get(domain)
        if domain_config is None:
            continue
        packets.append(
            build_bootstrap_packet(
                domain_config=domain_config,
                domain_items=domain_items_map.get(domain, []),
                domain_claims=domain_claims_map.get(domain, []),
                config=config,
            )
        )
    return packets


def load_domain_items(domains: list[str], extracted_dir: Path) -> dict[str, list[dict[str, object]]]:
    domain_items_map: dict[str, list[dict[str, object]]] = {}
    for domain in domains:
        items_path = extracted_dir / "domains" / domain / "items.jsonl"
        if not items_path.exists():
            domain_items_map[domain] = []
            continue
        domain_items_map[domain] = read_jsonl_required(items_path)
    return domain_items_map


def load_domain_claims(domains: list[str], wiki_dir: Path) -> dict[str, list[dict[str, object]]]:
    manifests_root = wiki_dir / "_meta" / "pages"
    if not manifests_root.exists():
        raise BootstrapError(f"Missing wiki manifests: {manifests_root}")
    domain_claims: dict[str, list[dict[str, object]]] = {domain: [] for domain in domains}
    for manifest_path in sorted(manifests_root.rglob("*.json")):
        manifest = read_json_required(manifest_path)
        domain = str(manifest.get("domain", ""))
        if domain not in domain_claims:
            continue
        page_id = str(manifest.get("page_id", ""))
        bucket = str(manifest.get("bucket", ""))
        for claim in manifest.get("synthesized_claims", []):
            if not isinstance(claim, dict):
                continue
            claim_id = str(claim.get("claim_id", "")).strip()
            if not claim_id:
                continue
            domain_claims[domain].append(
                {
                    "claim_id": f"{page_id}#{claim_id}",
                    "page_id": page_id,
                    "bucket": bucket,
                    "text": str(claim.get("text", "")).strip(),
                    "confidence": str(claim.get("confidence", "")).strip(),
                    "supporting_item_ids": [str(item) for item in claim.get("supporting_item_ids", []) if str(item)],
                    "provenance_refs": [dict(ref) for ref in claim.get("provenance_refs", []) if isinstance(ref, dict)],
                }
            )
    return domain_claims


def build_bootstrap_packet(
    domain_config: BootstrapDomainConfig,
    domain_items: list[dict[str, object]],
    domain_claims: list[dict[str, object]],
    config: BootstrapConfig,
) -> BootstrapPacket:
    section_configs = config.sections_for_domain(domain_config)
    selected_sections: list[dict[str, object]] = []
    selected_item_keys: list[str] = []
    selected_source_ids: set[str] = set()
    conflict_count = 0

    for section_config in section_configs:
        candidates = [item for item in domain_items if str(item.get("item_type", "")) in section_config.item_types]
        ranked_items = sorted(candidates, key=item_rank_key, reverse=True)
        selected_items: list[dict[str, object]] = []
        for item in ranked_items:
            item_view = build_item_view(item)
            selected_items.append(item_view)
            selected_item_keys.append(item_view["item_key"])
            selected_source_ids.update(item_view["supporting_source_ids"])
            if item_view.get("conflict_candidate_key"):
                conflict_count += 1
            if len(selected_items) >= section_config.max_items:
                break
        selected_sections.append(
            {
                "section_id": section_config.section_id,
                "title": section_config.title,
                "max_items": section_config.max_items,
                "max_claims": section_config.max_claims,
                "item_types": list(section_config.item_types),
                "claim_buckets": list(section_config.claim_buckets),
                "items": selected_items,
                "claims": [],
            }
        )

    all_selected_item_keys = set(selected_item_keys)
    selected_claim_ids: list[str] = []
    seen_claim_ids: set[str] = set()
    for section in selected_sections:
        eligible_claims = [
            claim
            for claim in domain_claims
            if claim["bucket"] in section["claim_buckets"]
            and claim["confidence"] in VALID_CLAIM_CONFIDENCE
            and claim["supporting_item_ids"]
            and set(claim["supporting_item_ids"]).issubset(all_selected_item_keys)
        ]
        for claim in sorted(eligible_claims, key=claim_rank_key, reverse=True):
            if claim["claim_id"] in seen_claim_ids:
                continue
            section["claims"].append(build_claim_view(claim, section["items"]))
            selected_claim_ids.append(claim["claim_id"])
            seen_claim_ids.add(claim["claim_id"])
            if len(section["claims"]) >= int(section["max_claims"]):
                break

    relative_path = domain_config.path
    return BootstrapPacket(
        domain=domain_config.domain,
        title=f"{domain_config.title} Bootstrap",
        kind=domain_config.kind,
        relative_path=relative_path,
        relative_manifest_path=build_manifest_path(relative_path),
        max_chars=domain_config.max_chars,
        sections=tuple(selected_sections),
        input_item_keys=tuple(dedupe_preserving_order(selected_item_keys)),
        input_claim_ids=tuple(dedupe_preserving_order(selected_claim_ids)),
        source_count=len(selected_source_ids),
        conflict_count=conflict_count,
    )


def build_manifest_path(relative_path: str) -> str:
    if relative_path.endswith(".md"):
        return f"_meta/{relative_path[:-3]}.json"
    return f"_meta/{relative_path}.json"


def build_item_view(item: dict[str, object]) -> dict[str, object]:
    return {
        "item_key": str(item["item_key"]),
        "item_type": str(item["item_type"]),
        "statement": str(item["statement"]),
        "confidence": str(item["confidence"]),
        "temporal_status": str(item["temporal_status"]),
        "recurrence_count": int(item["recurrence_count"]),
        "last_seen_at": str(item.get("last_seen_at", "")),
        "supporting_source_ids": [str(source_id) for source_id in item.get("supporting_source_ids", [])],
        "conflict_candidate_key": item.get("conflict_candidate_key"),
        "provenance_refs": [dict(ref) for ref in item.get("provenance_refs", []) if isinstance(ref, dict)],
    }


def build_claim_view(claim: dict[str, object], section_items: list[dict[str, object]]) -> dict[str, object]:
    section_item_map = {str(item["item_key"]): item for item in section_items}
    supporting_source_ids = sorted(
        {
            source_id
            for item_key in claim["supporting_item_ids"]
            for source_id in section_item_map.get(item_key, {}).get("supporting_source_ids", [])
        }
    )
    return {
        "claim_id": str(claim["claim_id"]),
        "page_id": str(claim["page_id"]),
        "bucket": str(claim["bucket"]),
        "text": str(claim["text"]),
        "confidence": str(claim["confidence"]),
        "supporting_item_ids": [str(item) for item in claim["supporting_item_ids"]],
        "supporting_source_ids": supporting_source_ids,
        "conflict_flag": any(section_item_map.get(item_key, {}).get("conflict_candidate_key") for item_key in claim["supporting_item_ids"]),
        "provenance_refs": [dict(ref) for ref in claim.get("provenance_refs", []) if isinstance(ref, dict)],
    }


def item_rank_key(item: dict[str, object]) -> tuple[int, int, int, str, int, str]:
    return (
        CONFIDENCE_PRIORITY.get(str(item.get("confidence", "")), 0),
        TEMPORAL_PRIORITY.get(str(item.get("temporal_status", "")), 0),
        int(item.get("recurrence_count", 0)),
        str(item.get("last_seen_at", "")),
        1 if not item.get("conflict_candidate_key") else 0,
        str(item.get("item_key", "")),
    )


def claim_rank_key(claim: dict[str, object]) -> tuple[int, int, str]:
    return (
        CONFIDENCE_PRIORITY.get(str(claim.get("confidence", "")), 0),
        len(claim.get("supporting_item_ids", [])),
        str(claim.get("claim_id", "")),
    )


def determine_bootstrap_mode(
    packet: BootstrapPacket,
    prior_state: BootstrapStateRecord | None,
    config: BootstrapConfig,
    provider_model: str,
    bootstrap_dir: Path,
) -> str:
    if prior_state is None:
        return "render"
    if prior_state.status != "rendered":
        return "render"
    if prior_state.bootstrap_schema_version != BOOTSTRAP_SCHEMA_VERSION:
        return "render"
    if prior_state.renderer != config.renderer:
        return "render"
    if prior_state.renderer_version != config.renderer_version:
        return "render"
    if prior_state.selection_version != config.selection_version:
        return "render"
    if prior_state.synthesis_prompt_version != config.synthesis_prompt_version:
        return "render"
    if prior_state.synthesis_schema_version != config.synthesis_schema_version:
        return "render"
    if prior_state.provider_type != config.provider.provider_type:
        return "render"
    if prior_state.provider_model != provider_model:
        return "render"
    if prior_state.input_digest != packet_digest(packet):
        return "render"
    if not (bootstrap_dir / prior_state.relative_path).exists():
        return "render"
    if not (bootstrap_dir / prior_state.relative_manifest_path).exists():
        return "render"
    return "unchanged"


def packet_digest(packet: BootstrapPacket) -> str:
    payload = json.dumps(packet.to_dict(), sort_keys=True, separators=(",", ":"))
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()


def build_bootstrap_artifacts(
    packet: BootstrapPacket,
    config: BootstrapConfig,
    staged_root: Path,
) -> dict[str, object]:
    synthesized = synthesize_bootstrap_packet(packet, config)
    validated_sections = validate_synthesis_output(packet, synthesized)
    trimmed_sections, trimmed = trim_sections_to_budget(packet, validated_sections)
    markdown, rendered_bullets = render_bootstrap_markdown(packet, trimmed_sections)
    manifest = build_bootstrap_manifest(packet, rendered_bullets, trimmed, config)

    staged_markdown_path = staged_root / packet.relative_path
    staged_manifest_path = staged_root / packet.relative_manifest_path
    write_text(staged_markdown_path, markdown)
    write_text(staged_manifest_path, json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    return {
        "markdown": markdown,
        "manifest": manifest,
        "trimmed": trimmed,
    }


def synthesize_bootstrap_packet(packet: BootstrapPacket, config: BootstrapConfig) -> dict[str, object]:
    if not packet.input_item_keys and not packet.input_claim_ids:
        return {"sections": []}
    system_prompt = (
        "You compress selected project memory into compact startup bullets. "
        "Use only the provided items and claims. "
        "Do not invent facts, sections, or labels. "
        "Return concise JSON only."
    )
    raw_output = call_openai_structured_json(
        config=config,
        system_prompt=system_prompt,
        user_prompt=build_synthesis_prompt(packet),
        schema=build_synthesis_schema(packet),
    )
    return raw_output


def build_synthesis_prompt(packet: BootstrapPacket) -> str:
    payload = packet.to_dict()
    payload["instructions"] = {
        "style": "short bullets, no paragraphs",
        "section_order": [section["section_id"] for section in payload["sections"]],
        "conflicts": "only include conflict context when directly supported",
    }
    return json.dumps(payload, indent=2, sort_keys=True)


def build_synthesis_schema(packet: BootstrapPacket) -> dict[str, object]:
    section_ids = [str(section["section_id"]) for section in packet.sections]
    bullet_schema: dict[str, object] = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "text": {"type": "string"},
            "supporting_item_keys": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 1,
            },
            "supporting_claim_ids": {
                "type": "array",
                "items": {"type": "string"},
            },
        },
        "required": ["text", "supporting_item_keys", "supporting_claim_ids"],
    }
    return {
        "name": "sessionmemory_bootstrap",
        "schema": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "sections": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "section_id": {"type": "string", "enum": section_ids},
                            "bullets": {
                                "type": "array",
                                "items": bullet_schema,
                            },
                        },
                        "required": ["section_id", "bullets"],
                    },
                }
            },
            "required": ["sections"],
        },
    }


def validate_synthesis_output(packet: BootstrapPacket, raw_output: dict[str, object]) -> list[dict[str, object]]:
    sections_payload = raw_output.get("sections")
    if not isinstance(sections_payload, list):
        raise BootstrapError(f"Invalid bootstrap synthesis payload for {packet.domain}")

    section_map = {str(section["section_id"]): section for section in packet.sections}
    valid_item_ids = set(packet.input_item_keys)
    valid_claim_ids = set(packet.input_claim_ids)
    claim_support_map = {
        str(claim["claim_id"]): [str(item) for item in claim.get("supporting_item_ids", []) if str(item) in valid_item_ids]
        for section in packet.sections
        for claim in section.get("claims", [])
        if isinstance(claim, dict)
    }
    seen_bullets: set[str] = set()
    validated_sections: list[dict[str, object]] = []
    dropped_invalid_bullet_count = 0
    kept_bullet_count = 0

    for section_payload in sections_payload:
        if not isinstance(section_payload, dict):
            raise BootstrapError(f"Invalid bootstrap section payload for {packet.domain}")
        section_id = str(section_payload.get("section_id", ""))
        if section_id not in section_map:
            raise BootstrapError(f"Unknown bootstrap section_id for {packet.domain}: {section_id}")
        bullets_payload = section_payload.get("bullets")
        if not isinstance(bullets_payload, list):
            raise BootstrapError(f"Invalid bootstrap bullets payload for {packet.domain} section {section_id}")
        validated_bullets: list[dict[str, object]] = []
        for bullet in bullets_payload:
            if not isinstance(bullet, dict):
                raise BootstrapError(f"Invalid bootstrap bullet payload for {packet.domain} section {section_id}")
            text = str(bullet.get("text", "")).strip()
            supporting_item_keys = [str(item) for item in bullet.get("supporting_item_keys", []) if str(item)]
            supporting_claim_ids = [str(item) for item in bullet.get("supporting_claim_ids", []) if str(item)]
            if not text:
                raise BootstrapError(f"Empty bootstrap bullet text for {packet.domain} section {section_id}")
            supporting_claim_ids = [claim_id for claim_id in supporting_claim_ids if claim_id in valid_claim_ids]
            supporting_item_keys = [item_id for item_id in supporting_item_keys if item_id in valid_item_ids]
            for claim_id in supporting_claim_ids:
                supporting_item_keys.extend(claim_support_map.get(claim_id, []))
            supporting_item_keys = dedupe_preserving_order(supporting_item_keys)
            if not supporting_item_keys:
                dropped_invalid_bullet_count += 1
                continue
            normalized_text = normalize_bullet_text(text)
            if normalized_text in seen_bullets:
                continue
            seen_bullets.add(normalized_text)
            kept_bullet_count += 1
            validated_bullets.append(
                {
                    "text": text,
                    "supporting_item_keys": supporting_item_keys,
                    "supporting_claim_ids": dedupe_preserving_order(supporting_claim_ids),
                }
            )
        validated_sections.append(
            {
                "section_id": section_id,
                "title": str(section_map[section_id]["title"]),
                "bullets": validated_bullets,
            }
        )

    present_section_ids = {str(section["section_id"]) for section in validated_sections}
    for section in packet.sections:
        if str(section["section_id"]) not in present_section_ids:
            validated_sections.append(
                {
                    "section_id": str(section["section_id"]),
                    "title": str(section["title"]),
                    "bullets": [],
                }
            )
    if dropped_invalid_bullet_count and kept_bullet_count == 0:
        raise BootstrapError(f"Bootstrap bullet referenced unknown item ids for {packet.domain}")
    validated_sections.sort(key=lambda section: section_order_index(packet, section["section_id"]))
    return validated_sections


def section_order_index(packet: BootstrapPacket, section_id: str) -> int:
    for index, section in enumerate(packet.sections):
        if str(section["section_id"]) == section_id:
            return index
    return len(packet.sections)


def trim_sections_to_budget(
    packet: BootstrapPacket,
    sections: list[dict[str, object]],
) -> tuple[list[dict[str, object]], bool]:
    working = [
        {
            "section_id": str(section["section_id"]),
            "title": str(section["title"]),
            "bullets": [dict(bullet) for bullet in section.get("bullets", [])],
        }
        for section in sections
    ]
    trimmed = False
    while True:
        markdown, _ = render_bootstrap_markdown(packet, working)
        if len(markdown) <= packet.max_chars:
            return working, trimmed
        total_bullets = sum(len(section["bullets"]) for section in working)
        if total_bullets > 1 and remove_lowest_priority_bullet(working):
            trimmed = True
            continue
        if shorten_lowest_priority_bullet(working, len(markdown) - packet.max_chars):
            trimmed = True
            continue
        if not remove_lowest_priority_bullet(working):
            raise BootstrapError(f"Bootstrap output could not fit within budget for {packet.domain}")
        trimmed = True


def remove_lowest_priority_bullet(sections: list[dict[str, object]]) -> bool:
    for section in reversed(sections):
        if section["bullets"]:
            section["bullets"].pop()
            return True
    return False


def shorten_lowest_priority_bullet(sections: list[dict[str, object]], overflow: int) -> bool:
    if overflow <= 0:
        return False
    for section in reversed(sections):
        if not section["bullets"]:
            continue
        bullet = section["bullets"][-1]
        text = str(bullet.get("text", "")).strip()
        if len(text) <= 24:
            continue
        target_length = max(20, len(text) - overflow - 3)
        if target_length >= len(text):
            target_length = len(text) - 4
        if target_length < 20:
            target_length = 20
        shortened = text[:target_length].rstrip(" .,:;")
        if not shortened:
            continue
        bullet["text"] = f"{shortened}..."
        return True
    return False


def render_bootstrap_markdown(
    packet: BootstrapPacket,
    sections: list[dict[str, object]],
) -> tuple[str, list[dict[str, object]]]:
    lines = [f"# {packet.title}", ""]
    rendered_bullets: list[dict[str, object]] = []
    bullet_index = 0

    if not any(section["bullets"] for section in sections):
        lines.append("- No high-signal bootstrap memory selected yet.")
        lines.append("")
        return "\n".join(lines).rstrip() + "\n", rendered_bullets

    for section in sections:
        if not section["bullets"]:
            continue
        lines.append(f"## {section['title']}")
        for bullet in section["bullets"]:
            bullet_index += 1
            bullet_id = f"B{bullet_index:02d}"
            rendered_text = str(bullet["text"]).strip()
            conflict_flag = bool(bullet.get("conflict_flag"))
            if conflict_flag and not rendered_text.endswith("(conflict)"):
                rendered_text = f"{rendered_text} (conflict)"
            lines.append(f"- [{bullet_id}] {rendered_text}")
            rendered_bullets.append(
                {
                    "bullet_id": bullet_id,
                    "section_id": str(section["section_id"]),
                    "text": rendered_text,
                    "supporting_item_keys": list(bullet["supporting_item_keys"]),
                    "supporting_claim_ids": list(bullet.get("supporting_claim_ids", [])),
                    "conflict_flag": conflict_flag,
                    "provenance_refs": [dict(ref) for ref in bullet.get("provenance_refs", [])],
                    "supporting_source_ids": list(bullet.get("supporting_source_ids", [])),
                }
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n", rendered_bullets


def build_bootstrap_manifest(
    packet: BootstrapPacket,
    bullets: list[dict[str, object]],
    trimmed: bool,
    config: BootstrapConfig,
) -> dict[str, object]:
    markdown, _ = render_bootstrap_markdown(packet, rebuild_sections_from_bullets(packet, bullets))
    return {
        "domain": packet.domain,
        "title": packet.title,
        "renderer": config.renderer,
        "versions": {
            "bootstrap_schema_version": BOOTSTRAP_SCHEMA_VERSION,
            "renderer_version": config.renderer_version,
            "selection_version": config.selection_version,
            "synthesis_prompt_version": config.synthesis_prompt_version,
            "synthesis_schema_version": config.synthesis_schema_version,
        },
        "packet": {
            "relative_path": packet.relative_path,
            "relative_manifest_path": packet.relative_manifest_path,
            "max_chars": packet.max_chars,
            "input_item_keys": list(packet.input_item_keys),
            "input_claim_ids": list(packet.input_claim_ids),
            "source_count": packet.source_count,
            "conflict_count": packet.conflict_count,
            "trimmed_to_budget": trimmed,
        },
        "bullets": bullets,
        "rendered_bootstrap_metadata": {
            "bullet_count": len(bullets),
            "char_count": len(markdown),
        },
    }


def rebuild_sections_from_bullets(packet: BootstrapPacket, bullets: list[dict[str, object]]) -> list[dict[str, object]]:
    section_titles = {str(section["section_id"]): str(section["title"]) for section in packet.sections}
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for bullet in bullets:
        grouped[str(bullet["section_id"])].append(
            {
                "text": str(bullet["text"]),
                "supporting_item_keys": list(bullet["supporting_item_keys"]),
                "supporting_claim_ids": list(bullet.get("supporting_claim_ids", [])),
                "conflict_flag": bool(bullet.get("conflict_flag")),
                "provenance_refs": [dict(ref) for ref in bullet.get("provenance_refs", [])],
                "supporting_source_ids": list(bullet.get("supporting_source_ids", [])),
            }
        )
    return [
        {
            "section_id": str(section["section_id"]),
            "title": section_titles[str(section["section_id"])],
            "bullets": grouped.get(str(section["section_id"]), []),
        }
        for section in packet.sections
    ]


def validate_bootstrap_artifacts(
    packet: BootstrapPacket,
    artifacts: dict[str, object],
    config: BootstrapConfig,
) -> None:
    markdown = str(artifacts["markdown"])
    manifest = dict(artifacts["manifest"])
    if manifest["domain"] != packet.domain:
        raise BootstrapError(f"Bootstrap manifest domain mismatch for {packet.domain}")
    if sorted(manifest["packet"]["input_item_keys"]) != sorted(packet.input_item_keys):
        raise BootstrapError(f"Bootstrap manifest input_item_keys mismatch for {packet.domain}")
    if sorted(manifest["packet"]["input_claim_ids"]) != sorted(packet.input_claim_ids):
        raise BootstrapError(f"Bootstrap manifest input_claim_ids mismatch for {packet.domain}")
    if len(markdown) > packet.max_chars:
        raise BootstrapError(f"Bootstrap markdown exceeded budget for {packet.domain}")

    bullet_ids_in_markdown = re.findall(r"\[B\d{2}\]", markdown)
    manifest_bullet_ids = [str(bullet["bullet_id"]) for bullet in manifest["bullets"]]
    if sorted(item.strip("[]") for item in bullet_ids_in_markdown) != sorted(manifest_bullet_ids):
        raise BootstrapError(f"Bootstrap markdown bullet ids mismatch for {packet.domain}")
    valid_item_ids = set(packet.input_item_keys)
    valid_claim_ids = set(packet.input_claim_ids)
    seen_texts: set[str] = set()
    for bullet in manifest["bullets"]:
        if any(item_id not in valid_item_ids for item_id in bullet["supporting_item_keys"]):
            raise BootstrapError(f"Bootstrap manifest referenced unknown item ids for {packet.domain}")
        if any(claim_id not in valid_claim_ids for claim_id in bullet.get("supporting_claim_ids", [])):
            raise BootstrapError(f"Bootstrap manifest referenced unknown claim ids for {packet.domain}")
        normalized_text = normalize_bullet_text(str(bullet["text"]))
        if normalized_text in seen_texts:
            raise BootstrapError(f"Duplicate bootstrap bullet text in manifest for {packet.domain}")
        seen_texts.add(normalized_text)
    if config.renderer != "compact_markdown":
        raise BootstrapError(f"Unsupported bootstrap renderer for validation: {config.renderer}")


def build_state_record(
    packet: BootstrapPacket,
    config: BootstrapConfig,
    provider_model: str,
    input_digest: str,
    bullet_count: int,
    run_id: str,
) -> BootstrapStateRecord:
    return BootstrapStateRecord(
        domain=packet.domain,
        bootstrap_schema_version=BOOTSTRAP_SCHEMA_VERSION,
        renderer=config.renderer,
        renderer_version=config.renderer_version,
        selection_version=config.selection_version,
        synthesis_prompt_version=config.synthesis_prompt_version,
        synthesis_schema_version=config.synthesis_schema_version,
        provider_type=config.provider.provider_type,
        provider_model=provider_model,
        input_digest=input_digest,
        bullet_count=bullet_count,
        status="rendered",
        relative_path=packet.relative_path,
        relative_manifest_path=packet.relative_manifest_path,
        last_rendered_at=utc_now(),
        last_run_id=run_id,
    )


def build_bootstrap_notices(
    packet: BootstrapPacket,
    artifacts: dict[str, object],
    run_id: str,
) -> list[BootstrapNotice]:
    notices: list[BootstrapNotice] = []
    manifest = dict(artifacts["manifest"])
    if manifest["packet"]["trimmed_to_budget"]:
        notices.append(
            BootstrapNotice(
                run_id=run_id,
                domain=packet.domain,
                severity="warning",
                notice_type="budget_trimmed",
                summary="bootstrap bullets were trimmed to fit the configured budget",
            )
        )
    if any(bullet.get("conflict_flag") for bullet in manifest["bullets"]):
        notices.append(
            BootstrapNotice(
                run_id=run_id,
                domain=packet.domain,
                severity="warning",
                notice_type="conflict_included",
                summary="bootstrap includes conflict-marked bullets",
            )
        )
    if any(
        str(item.get("confidence", "")) == "inferred"
        for section in packet.sections
        for item in section.get("items", [])
    ) or any(
        str(claim.get("confidence", "")) == "inferred"
        for section in packet.sections
        for claim in section.get("claims", [])
    ):
        notices.append(
            BootstrapNotice(
                run_id=run_id,
                domain=packet.domain,
                severity="warning",
                notice_type="low_confidence_included",
                summary="bootstrap includes inferred source content",
            )
        )
    return notices


def validate_state_against_packet_plan(
    packet_plan: list[BootstrapPacket],
    bootstrap_state: dict[str, BootstrapStateRecord],
    config: BootstrapConfig,
    provider_model: str,
) -> None:
    expected_domains = {packet.domain for packet in packet_plan}
    for packet in packet_plan:
        state_record = bootstrap_state.get(packet.domain)
        if state_record is None:
            raise BootstrapError(f"Missing bootstrap state for domain {packet.domain}")
        if state_record.status != "rendered":
            raise BootstrapError(f"Bootstrap state did not mark domain rendered: {packet.domain}")
        if state_record.renderer != config.renderer:
            raise BootstrapError(f"Bootstrap renderer mismatch in state for {packet.domain}")
        if state_record.provider_model != provider_model:
            raise BootstrapError(f"Bootstrap provider model mismatch in state for {packet.domain}")
        if state_record.input_digest != packet_digest(packet):
            raise BootstrapError(f"Bootstrap input digest mismatch in state for {packet.domain}")
    stale = sorted(set(bootstrap_state) - expected_domains)
    if stale:
        raise BootstrapError(f"Bootstrap state contains domains outside the current plan: {', '.join(stale[:5])}")


def build_state_payload(state_records: dict[str, BootstrapStateRecord]) -> dict[str, object]:
    return {
        "schema_version": STATE_SCHEMA_VERSION,
        "bootstrap_schema_version": BOOTSTRAP_SCHEMA_VERSION,
        "generated_at": utc_now(),
        "domain_count": len(state_records),
        "domains": [state_records[domain].to_dict() for domain in sorted(state_records)],
    }


def promote_staged_bootstrap(
    staging_root: Path,
    bootstrap_dir: Path,
    changed_domains: list[str],
    packet_plan: list[BootstrapPacket],
) -> None:
    packet_map = {packet.domain: packet for packet in packet_plan}
    for domain in changed_domains:
        packet = packet_map[domain]
        staged_markdown_path = staging_root / packet.relative_path
        staged_manifest_path = staging_root / packet.relative_manifest_path
        target_markdown_path = bootstrap_dir / packet.relative_path
        target_manifest_path = bootstrap_dir / packet.relative_manifest_path
        ensure_directory(target_markdown_path.parent)
        ensure_directory(target_manifest_path.parent)
        os.replace(staged_markdown_path, target_markdown_path)
        os.replace(staged_manifest_path, target_manifest_path)


def cleanup_staging_root(staging_root: Path) -> None:
    if staging_root.exists():
        shutil.rmtree(staging_root, ignore_errors=True)


def sanitize_section_for_prompt(section: dict[str, object]) -> dict[str, object]:
    return {
        "section_id": str(section["section_id"]),
        "title": str(section["title"]),
        "items": [
            {
                "item_key": str(item["item_key"]),
                "item_type": str(item["item_type"]),
                "statement": str(item["statement"]),
                "confidence": str(item["confidence"]),
                "temporal_status": str(item["temporal_status"]),
                "recurrence_count": int(item["recurrence_count"]),
                "last_seen_at": str(item.get("last_seen_at", "")),
                "conflict_candidate_key": item.get("conflict_candidate_key"),
            }
            for item in section.get("items", [])
        ],
        "claims": [
            {
                "claim_id": str(claim["claim_id"]),
                "text": str(claim["text"]),
                "confidence": str(claim["confidence"]),
                "supporting_item_ids": list(claim["supporting_item_ids"]),
            }
            for claim in section.get("claims", [])
        ],
    }


def read_json_required(path: Path) -> dict[str, object]:
    payload = read_json_file(path)
    if payload is None:
        raise BootstrapError(f"Missing or invalid JSON artifact: {path}")
    return payload


def read_json_file(path: Path) -> dict[str, object] | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as exc:
        raise BootstrapError(f"Invalid JSON artifact: {path}") from exc
    if not isinstance(payload, dict):
        raise BootstrapError(f"JSON artifact root must be an object: {path}")
    return payload


def read_jsonl_required(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        raise BootstrapError(f"Missing JSONL artifact: {path}")
    records: list[dict[str, object]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError as exc:
            raise BootstrapError(f"Invalid JSONL artifact line {line_no}: {path}") from exc
        if not isinstance(payload, dict):
            raise BootstrapError(f"JSONL artifact line {line_no} is not an object: {path}")
        records.append(payload)
    return records


def write_text(path: Path, text: str) -> None:
    ensure_directory(path.parent)
    path.write_text(text, encoding="utf-8", newline="\n")


def dedupe_preserving_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        ordered.append(item)
    return ordered


def normalize_bullet_text(text: str) -> str:
    return NORMALIZE_BULLET_PATTERN.sub(" ", text.strip().lower())
