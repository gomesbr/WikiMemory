from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from .discovery import DiscoveryError, atomic_write_text, ensure_directory, utc_now
from .extraction import ExtractionStateRecord, append_jsonl_text, load_extraction_state, read_json_file

STATE_SCHEMA_VERSION = 1
WIKI_SCHEMA_VERSION = 2
INDEX_PAGE_KEY = "index"
MAX_CITATION_PROVENANCE_REFS = 3
MAX_SYNTHESIS_ITEMS_PER_SECTION = 12
MAX_SYNTHESIS_STATEMENT_CHARS = 280
MAX_INDEX_STATEMENT_CHARS = 140
MAX_BUCKET_STATEMENT_CHARS = 260
VALID_CLAIM_CONFIDENCE = {"strong", "inferred"}
PROJECT_LABELS = {"ai-trader", "open-brain", "ai-scientist"}
TEMPORAL_BUCKETS = {"current-state", "next-steps", "open-questions", "tasks", "outcomes", "failures"}
GENERIC_CLAIM_PATTERN = re.compile(
    r"\b(?:important|essential|necessary|ongoing tasks?|clear communication)\b",
    re.IGNORECASE,
)


class WikiError(DiscoveryError):
    """Fatal wiki generation error that must stop the run."""


@dataclass(frozen=True)
class WikiDomainConfig:
    domain: str
    title: str
    path: str
    kind: str


@dataclass(frozen=True)
class WikiBucketConfig:
    page_key: str
    title: str
    item_types: tuple[str, ...]


@dataclass(frozen=True)
class WikiProviderConfig:
    provider_type: str
    api_key_env: str
    base_url_env: str
    model_env: str
    default_model: str
    temperature: float

    def resolve_model(self) -> str:
        return os.environ.get(self.model_env, "").strip() or self.default_model

    def resolve_base_url(self) -> str:
        return os.environ.get(self.base_url_env, "").strip() or "https://api.openai.com"

    def resolve_api_key(self) -> str:
        return os.environ.get(self.api_key_env, "").strip()


@dataclass(frozen=True)
class WikiConfig:
    schema_version: int
    wiki_schema_version: int
    renderer: str
    renderer_version: int
    page_config_version: int
    synthesis_prompt_version: int
    synthesis_schema_version: int
    provider: WikiProviderConfig
    approved_latent_types: tuple[str, ...]
    domains: tuple[WikiDomainConfig, ...]
    buckets: tuple[WikiBucketConfig, ...]
    bucket_item_limits: dict[str, int]
    index_preview_items: int
    page_size_caps: dict[str, int]
    generic_claim_banned_patterns: tuple[str, ...]

    @property
    def domain_map(self) -> dict[str, WikiDomainConfig]:
        return {domain.domain: domain for domain in self.domains}

    @property
    def bucket_map(self) -> dict[str, WikiBucketConfig]:
        return {bucket.page_key: bucket for bucket in self.buckets}


@dataclass(frozen=True)
class WikiStateRecord:
    page_id: str
    domain: str
    bucket: str
    page_type: str
    wiki_schema_version: int
    renderer: str
    renderer_version: int
    page_config_version: int
    synthesis_prompt_version: int
    synthesis_schema_version: int
    provider_type: str
    provider_model: str
    input_digest: str
    input_item_count: int
    claim_count: int
    status: str
    relative_page_path: str
    relative_manifest_path: str
    last_rendered_at: str
    last_run_id: str

    def to_dict(self) -> dict[str, object]:
        return {
            "page_id": self.page_id,
            "domain": self.domain,
            "bucket": self.bucket,
            "page_type": self.page_type,
            "wiki_schema_version": self.wiki_schema_version,
            "renderer": self.renderer,
            "renderer_version": self.renderer_version,
            "page_config_version": self.page_config_version,
            "synthesis_prompt_version": self.synthesis_prompt_version,
            "synthesis_schema_version": self.synthesis_schema_version,
            "provider_type": self.provider_type,
            "provider_model": self.provider_model,
            "input_digest": self.input_digest,
            "input_item_count": self.input_item_count,
            "claim_count": self.claim_count,
            "status": self.status,
            "relative_page_path": self.relative_page_path,
            "relative_manifest_path": self.relative_manifest_path,
            "last_rendered_at": self.last_rendered_at,
            "last_run_id": self.last_run_id,
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "WikiStateRecord":
        return cls(
            page_id=str(data["page_id"]),
            domain=str(data["domain"]),
            bucket=str(data["bucket"]),
            page_type=str(data["page_type"]),
            wiki_schema_version=int(data["wiki_schema_version"]),
            renderer=str(data["renderer"]),
            renderer_version=int(data["renderer_version"]),
            page_config_version=int(data["page_config_version"]),
            synthesis_prompt_version=int(data["synthesis_prompt_version"]),
            synthesis_schema_version=int(data["synthesis_schema_version"]),
            provider_type=str(data["provider_type"]),
            provider_model=str(data["provider_model"]),
            input_digest=str(data["input_digest"]),
            input_item_count=int(data["input_item_count"]),
            claim_count=int(data["claim_count"]),
            status=str(data["status"]),
            relative_page_path=str(data["relative_page_path"]),
            relative_manifest_path=str(data["relative_manifest_path"]),
            last_rendered_at=str(data["last_rendered_at"]),
            last_run_id=str(data["last_run_id"]),
        )


@dataclass(frozen=True)
class WikiNotice:
    run_id: str
    page_id: str
    severity: str
    notice_type: str
    summary: str

    def to_dict(self) -> dict[str, object]:
        return {
            "run_id": self.run_id,
            "page_id": self.page_id,
            "severity": self.severity,
            "notice_type": self.notice_type,
            "summary": self.summary,
        }


@dataclass(frozen=True)
class WikiRunReport:
    run_id: str
    started_at: str
    finished_at: str
    page_status_counts: dict[str, int]
    rendered_page_count: int
    synthesized_claim_count: int
    notice_count: int
    success: bool
    fatal_error_summary: str | None

    def to_dict(self) -> dict[str, object]:
        return {
            "run_id": self.run_id,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "page_status_counts": self.page_status_counts,
            "rendered_page_count": self.rendered_page_count,
            "synthesized_claim_count": self.synthesized_claim_count,
            "notice_count": self.notice_count,
            "success": self.success,
            "fatal_error_summary": self.fatal_error_summary,
        }


@dataclass(frozen=True)
class WikiResult:
    report: WikiRunReport
    state_path: Path
    run_log_path: Path
    notice_log_path: Path


@dataclass(frozen=True)
class WikiPage:
    page_id: str
    page_type: str
    domain: str
    bucket: str
    title: str
    relative_page_path: str
    relative_manifest_path: str
    namespace: str
    tags: tuple[str, ...]
    related_pages: tuple[dict[str, str], ...]
    related_domains: tuple[str, ...]
    input_item_keys: tuple[str, ...]
    deterministic_sections: tuple[dict[str, object], ...]
    source_count: int
    conflict_count: int

    def to_dict(self) -> dict[str, object]:
        return {
            "page_id": self.page_id,
            "page_type": self.page_type,
            "domain": self.domain,
            "bucket": self.bucket,
            "title": self.title,
            "relative_page_path": self.relative_page_path,
            "relative_manifest_path": self.relative_manifest_path,
            "namespace": self.namespace,
            "tags": list(self.tags),
            "related_pages": [dict(item) for item in self.related_pages],
            "related_domains": list(self.related_domains),
            "input_item_keys": list(self.input_item_keys),
            "deterministic_sections": [dict(item) for item in self.deterministic_sections],
            "source_count": self.source_count,
            "conflict_count": self.conflict_count,
        }


def run_wiki(
    config_path: Path | str,
    state_dir: Path | str,
    extracted_dir: Path | str,
    wiki_dir: Path | str,
    audits_dir: Path | str,
    source_ids: Iterable[str] | None = None,
) -> WikiResult:
    config_path = Path(config_path)
    state_dir = Path(state_dir)
    extracted_dir = Path(extracted_dir)
    wiki_dir = Path(wiki_dir)
    audits_dir = Path(audits_dir)

    extraction_state_path = state_dir / "extraction_state.json"
    state_path = state_dir / "wiki_state.json"
    run_log_path = state_dir / "wiki_runs.jsonl"
    notice_log_path = audits_dir / "wiki_notices.jsonl"

    ensure_directory(state_dir)
    ensure_directory(audits_dir)
    ensure_directory(wiki_dir)
    ensure_directory(wiki_dir / "_meta" / "pages")

    run_id = f"wiki-{utc_now().replace(':', '').replace('.', '').replace('-', '')}"
    started_at = utc_now()
    staging_root = wiki_dir / ".staging" / run_id

    previous_state_text = state_path.read_text(encoding="utf-8") if state_path.exists() else None
    previous_run_log_text = run_log_path.read_text(encoding="utf-8") if run_log_path.exists() else ""
    previous_notice_log_text = notice_log_path.read_text(encoding="utf-8") if notice_log_path.exists() else ""

    try:
        config = load_wiki_config(config_path)
        extraction_state = load_extraction_state(extraction_state_path)
        previous_state = load_wiki_state(state_path)
        target_domains = resolve_target_domains(source_ids, extraction_state, config, extracted_dir)
        page_plan = build_page_plan(target_domains, config, extracted_dir)
        next_state: dict[str, WikiStateRecord] = {} if source_ids is None else dict(previous_state)
        stale_page_ids = sorted(set(previous_state) - {page.page_id for page in page_plan}) if source_ids is None else []

        page_status_counts: Counter[str] = Counter()
        notices_for_run: list[WikiNotice] = []
        changed_page_ids: list[str] = []
        rendered_page_count = 0
        synthesized_claim_count = 0
        provider_model = config.provider.resolve_model()

        for page in page_plan:
            prior_state = previous_state.get(page.page_id)
            mode = determine_wiki_mode(page, prior_state, config, provider_model, wiki_dir)
            if mode == "unchanged":
                next_state[page.page_id] = previous_state[page.page_id]
                page_status_counts["unchanged"] += 1
                continue

            page_artifacts = build_page_artifacts(
                page=page,
                config=config,
                staged_root=staging_root,
            )
            validate_page_artifacts(page, page_artifacts, config)
            next_state[page.page_id] = build_state_record(
                page=page,
                config=config,
                provider_model=provider_model,
                input_digest=page_digest(page),
                claim_count=len(page_artifacts["manifest"]["synthesized_claims"]),
                run_id=run_id,
            )
            notices_for_run.extend(build_page_notices(page, page_artifacts, run_id))
            changed_page_ids.append(page.page_id)
            page_status_counts["rendered"] += 1
            rendered_page_count += 1
            synthesized_claim_count += len(page_artifacts["manifest"]["synthesized_claims"])

        if source_ids is None:
            validate_state_against_page_plan(page_plan, next_state, config, provider_model)

        report = WikiRunReport(
            run_id=run_id,
            started_at=started_at,
            finished_at=utc_now(),
            page_status_counts=dict(sorted(page_status_counts.items())),
            rendered_page_count=rendered_page_count,
            synthesized_claim_count=synthesized_claim_count,
            notice_count=len(notices_for_run),
            success=True,
            fatal_error_summary=None,
        )

        staged_state_path = staging_root / "wiki_state.json"
        staged_run_log_path = staging_root / "wiki_runs.jsonl"
        staged_notice_log_path = staging_root / "wiki_notices.jsonl"
        write_text(staged_state_path, json.dumps(build_state_payload(next_state), indent=2, sort_keys=True) + "\n")
        write_text(staged_run_log_path, append_jsonl_text(previous_run_log_text, report.to_dict()))
        write_text(
            staged_notice_log_path,
            append_jsonl_text(previous_notice_log_text, [notice.to_dict() for notice in notices_for_run]),
        )

        promote_staged_pages(staging_root, wiki_dir, changed_page_ids, page_plan, previous_state, stale_page_ids)
        os.replace(staged_state_path, state_path)
        ensure_directory(run_log_path.parent)
        os.replace(staged_run_log_path, run_log_path)
        ensure_directory(notice_log_path.parent)
        os.replace(staged_notice_log_path, notice_log_path)
        cleanup_staging_root(staging_root)
        return WikiResult(report=report, state_path=state_path, run_log_path=run_log_path, notice_log_path=notice_log_path)
    except Exception as exc:
        cleanup_staging_root(staging_root)
        failure_report = WikiRunReport(
            run_id=run_id,
            started_at=started_at,
            finished_at=utc_now(),
            page_status_counts={},
            rendered_page_count=0,
            synthesized_claim_count=0,
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
        return WikiResult(report=failure_report, state_path=state_path, run_log_path=run_log_path, notice_log_path=notice_log_path)


def load_wiki_config(config_path: Path) -> WikiConfig:
    try:
        payload = json.loads(config_path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError as exc:
        raise WikiError(f"Missing wiki config: {config_path}") from exc
    except json.JSONDecodeError as exc:
        raise WikiError(f"Invalid wiki config JSON: {config_path}") from exc

    domains_payload = payload.get("domains")
    buckets_payload = payload.get("buckets")
    provider_payload = payload.get("provider")
    latent_payload = payload.get("approved_latent_types")
    bucket_item_limits = payload.get("bucket_item_limits")
    page_size_caps = payload.get("page_size_caps")
    if not isinstance(domains_payload, list) or not domains_payload:
        raise WikiError("Wiki config must define domains")
    if not isinstance(buckets_payload, list) or not buckets_payload:
        raise WikiError("Wiki config must define buckets")
    if not isinstance(provider_payload, dict):
        raise WikiError("Wiki config must define provider")
    if not isinstance(latent_payload, list) or not latent_payload:
        raise WikiError("Wiki config must define approved_latent_types")
    if not isinstance(bucket_item_limits, dict):
        raise WikiError("Wiki config must define bucket_item_limits")
    if not isinstance(page_size_caps, dict):
        raise WikiError("Wiki config must define page_size_caps")

    domains = tuple(
        WikiDomainConfig(
            domain=str(item["domain"]),
            title=str(item["title"]),
            path=str(item["path"]),
            kind=str(item["kind"]),
        )
        for item in domains_payload
    )
    buckets = tuple(
        WikiBucketConfig(
            page_key=str(item["page_key"]),
            title=str(item["title"]),
            item_types=tuple(str(value) for value in item.get("item_types", [])),
        )
        for item in buckets_payload
    )
    if len({domain.domain for domain in domains}) != len(domains):
        raise WikiError("Wiki config domains must be unique")
    if len({bucket.page_key for bucket in buckets}) != len(buckets):
        raise WikiError("Wiki config bucket page_key values must be unique")

    provider = WikiProviderConfig(
        provider_type=str(provider_payload["type"]),
        api_key_env=str(provider_payload["api_key_env"]),
        base_url_env=str(provider_payload["base_url_env"]),
        model_env=str(provider_payload["model_env"]),
        default_model=str(provider_payload["default_model"]),
        temperature=float(provider_payload.get("temperature", 0.2)),
    )
    if provider.provider_type != "openai":
        raise WikiError(f"Unsupported wiki provider type: {provider.provider_type}")

    return WikiConfig(
        schema_version=int(payload["schema_version"]),
        wiki_schema_version=int(payload["wiki_schema_version"]),
        renderer=str(payload["renderer"]),
        renderer_version=int(payload["renderer_version"]),
        page_config_version=int(payload["page_config_version"]),
        synthesis_prompt_version=int(payload["synthesis_prompt_version"]),
        synthesis_schema_version=int(payload["synthesis_schema_version"]),
        provider=provider,
        approved_latent_types=tuple(str(item) for item in latent_payload),
        domains=domains,
        buckets=buckets,
        bucket_item_limits={str(key): int(value) for key, value in bucket_item_limits.items()},
        index_preview_items=int(payload.get("index_preview_items", 5)),
        page_size_caps={str(key): int(value) for key, value in page_size_caps.items()},
        generic_claim_banned_patterns=tuple(
            normalize_text(str(item))
            for item in payload.get("generic_claim_banned_patterns", [])
            if normalize_text(str(item))
        ),
    )


def load_wiki_state(state_path: Path) -> dict[str, WikiStateRecord]:
    if not state_path.exists():
        return {}
    try:
        payload = json.loads(state_path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise WikiError(f"Invalid wiki state JSON: {state_path}") from exc
    if int(payload.get("schema_version", -1)) != STATE_SCHEMA_VERSION:
        raise WikiError(f"Unsupported wiki state schema version in {state_path}: {payload.get('schema_version')}")
    records = [WikiStateRecord.from_dict(item) for item in payload.get("pages", [])]
    return {record.page_id: record for record in records}


def resolve_target_domains(
    source_ids: Iterable[str] | None,
    extraction_state: dict[str, ExtractionStateRecord],
    config: WikiConfig,
    extracted_dir: Path,
) -> list[str]:
    configured_domains = [domain.domain for domain in config.domains]
    existing_domains = sorted(
        path.name for path in (extracted_dir / "domains").iterdir()
        if (extracted_dir / "domains").exists() and path.is_dir()
    )
    if source_ids is None:
        return dedupe_preserving_order([*configured_domains, *existing_domains])
    target_source_ids = sorted(dict.fromkeys(str(source_id) for source_id in source_ids))
    missing = [source_id for source_id in target_source_ids if source_id not in extraction_state]
    if missing:
        raise WikiError(f"Requested source_ids are missing from extraction state: {', '.join(missing)}")
    touched_domains: list[str] = []
    for source_id in target_source_ids:
        touched_domains.extend(extraction_state[source_id].touched_domains)
    return dedupe_preserving_order([domain for domain in touched_domains if domain])


def build_page_plan(domains: list[str], config: WikiConfig, extracted_dir: Path) -> list[WikiPage]:
    domain_items_map = load_domain_items(domains, extracted_dir)
    pages: list[WikiPage] = []
    for domain in domains:
        domain_config = config.domain_map.get(domain)
        if domain_config is None:
            continue
        items = domain_items_map.get(domain, [])
        pages.extend(build_domain_pages(domain_config, items, config))
    return pages


def load_domain_items(domains: list[str], extracted_dir: Path) -> dict[str, list[dict[str, object]]]:
    domain_items_map: dict[str, list[dict[str, object]]] = {}
    for domain in domains:
        items_path = extracted_dir / "domains" / domain / "items.jsonl"
        if not items_path.exists():
            domain_items_map[domain] = []
            continue
        domain_items_map[domain] = read_jsonl_required(items_path)
    return domain_items_map


def build_domain_pages(
    domain_config: WikiDomainConfig,
    domain_items: list[dict[str, object]],
    config: WikiConfig,
) -> list[WikiPage]:
    eligible_items = [item for item in domain_items if bool(item.get("wiki_eligible", False))]
    if not eligible_items:
        return []
    bucket_map = {bucket.page_key: [] for bucket in config.buckets}
    for item in eligible_items:
        bucket_key = str(item.get("target_page_key", ""))
        if bucket_key in bucket_map:
            bucket_map[bucket_key].append(item)

    pages: list[WikiPage] = []
    index_page = build_wiki_page(
        domain_config=domain_config,
        bucket=None,
        items=eligible_items,
        config=config,
        bucket_items_map=bucket_map,
    )
    if index_page is not None:
        pages.append(index_page)
    for bucket in config.buckets:
        bucket_page = build_wiki_page(
            domain_config=domain_config,
            bucket=bucket,
            items=bucket_map.get(bucket.page_key, []),
            config=config,
            bucket_items_map=bucket_map,
        )
        if bucket_page is not None:
            pages.append(bucket_page)
    return pages


def build_wiki_page(
    domain_config: WikiDomainConfig,
    bucket: WikiBucketConfig | None,
    items: list[dict[str, object]],
    config: WikiConfig,
    bucket_items_map: dict[str, list[dict[str, object]]],
) -> WikiPage | None:
    page_key = INDEX_PAGE_KEY if bucket is None else bucket.page_key
    page_type = "domain_index" if bucket is None else "bucket_page"
    if bucket is None:
        if not any(bucket_items_map.get(configured_bucket.page_key, []) for configured_bucket in config.buckets):
            return None
    elif not items:
        return None
    title = domain_config.title if bucket is None else f"{domain_config.title} - {bucket.title}"
    relative_page_path = f"{domain_config.path}/{page_key}.md"
    relative_manifest_path = f"_meta/pages/{domain_config.path}/{page_key}.json"
    page_id = relative_page_path.removesuffix(".md")
    namespace = domain_config.path
    related_pages = build_related_pages(domain_config, config, current_page_key=page_key)
    related_domains = tuple(
        sorted(
            {
                str(secondary)
                for item in items
                for secondary in item.get("secondary_domains", [])
                if str(secondary)
            }
        )
    )
    deterministic_sections = (
        build_index_sections(domain_config, bucket_items_map, config)
        if bucket is None
        else build_bucket_sections(bucket, items, config)
    )
    if not deterministic_sections:
        return None
    input_item_keys = tuple(
        str(item["item_key"])
        for section in deterministic_sections
        for item in section.get("items", [])
    )
    source_count = len({str(source_id) for item in items for source_id in item.get("supporting_source_ids", [])})
    conflict_count = sum(1 for item in items if item.get("conflict_candidate_key"))
    tags = build_page_tags(domain_config, bucket)
    return WikiPage(
        page_id=page_id,
        page_type=page_type,
        domain=domain_config.domain,
        bucket=page_key,
        title=title,
        relative_page_path=relative_page_path,
        relative_manifest_path=relative_manifest_path,
        namespace=namespace,
        tags=tags,
        related_pages=related_pages,
        related_domains=related_domains,
        input_item_keys=input_item_keys,
        deterministic_sections=deterministic_sections,
        source_count=source_count,
        conflict_count=conflict_count,
    )


def build_related_pages(
    domain_config: WikiDomainConfig,
    config: WikiConfig,
    current_page_key: str,
) -> tuple[dict[str, str], ...]:
    related: list[dict[str, str]] = []
    related.append(
        {
            "page_key": INDEX_PAGE_KEY,
            "title": domain_config.title,
            "wikilink": obsidian_wikilink(f"{domain_config.path}/{INDEX_PAGE_KEY}", domain_config.title),
        }
    )
    for bucket in config.buckets:
        if bucket.page_key == current_page_key:
            continue
        related.append(
            {
                "page_key": bucket.page_key,
                "title": f"{domain_config.title} - {bucket.title}",
                "wikilink": obsidian_wikilink(
                    f"{domain_config.path}/{bucket.page_key}",
                    f"{domain_config.title} - {bucket.title}",
                ),
            }
        )
    return tuple(related)


def build_page_tags(domain_config: WikiDomainConfig, bucket: WikiBucketConfig | None) -> tuple[str, ...]:
    tags = ["sessionmemory", domain_config.kind, domain_config.domain]
    if bucket is None:
        tags.append("index")
    else:
        tags.extend(["bucket", bucket.page_key])
    return tuple(tags)


def build_index_sections(
    domain_config: WikiDomainConfig,
    bucket_items_map: dict[str, list[dict[str, object]]],
    config: WikiConfig,
) -> tuple[dict[str, object], ...]:
    sections: list[dict[str, object]] = []
    for bucket in config.buckets:
        bucket_items = sort_items_for_bucket(bucket.page_key, bucket_items_map.get(bucket.page_key, []))
        preview_items = [
            build_item_view(item, max_statement_chars=MAX_INDEX_STATEMENT_CHARS)
            for item in bucket_items[: config.index_preview_items]
        ]
        if not preview_items:
            continue
        sections.append(
            {
                "section_id": bucket.page_key,
                "title": bucket.title,
                "page_link": obsidian_wikilink(
                    f"{domain_config.path}/{bucket.page_key}",
                    f"{domain_config.title} - {bucket.title}",
                ),
                "item_count": len(bucket_items),
                "items": preview_items,
            }
        )
    return tuple(sections)


def build_bucket_sections(
    bucket: WikiBucketConfig,
    items: list[dict[str, object]],
    config: WikiConfig,
) -> tuple[dict[str, object], ...]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for item in sort_items_for_bucket(bucket.page_key, items):
        grouped[str(item.get("item_type", ""))].append(item)
    sections: list[dict[str, object]] = []
    limit = config.bucket_item_limits.get(bucket.page_key, config.bucket_item_limits.get("default", 50))
    for item_type in bucket.item_types:
        section_items = grouped.get(item_type, [])[:limit]
        if not section_items:
            continue
        sections.append(
            {
                "section_id": item_type,
                "title": humanize_item_type(item_type),
                "item_count": len(section_items),
                "items": [build_item_view(item, max_statement_chars=MAX_BUCKET_STATEMENT_CHARS) for item in section_items],
            }
        )
    return tuple(sections)


def build_item_view(item: dict[str, object], *, max_statement_chars: int | None = None) -> dict[str, object]:
    statement = str(item["statement"])
    if max_statement_chars is not None and len(statement) > max_statement_chars:
        statement = statement[: max_statement_chars - 3].rstrip() + "..."
    return {
        "item_key": str(item["item_key"]),
        "item_type": str(item["item_type"]),
        "statement": statement,
        "confidence": str(item["confidence"]),
        "temporal_status": str(item["temporal_status"]),
        "recurrence_count": int(item["recurrence_count"]),
        "subject_key": str(item["subject_key"]),
        "supporting_source_ids": [str(source_id) for source_id in item.get("supporting_source_ids", [])],
        "supporting_session_count": int(item.get("supporting_session_count", 0)),
        "supporting_day_count": int(item.get("supporting_day_count", 0)),
        "wiki_eligible": bool(item.get("wiki_eligible", False)),
        "durability_class": str(item.get("durability_class", "")),
        "promotion_blockers": [str(blocker) for blocker in item.get("promotion_blockers", [])],
        "conflict_candidate_key": item.get("conflict_candidate_key"),
        "provenance_refs": [
            dict(provenance) for provenance in item.get("provenance_refs", [])[:MAX_CITATION_PROVENANCE_REFS]
        ],
    }


def sort_items_for_bucket(bucket_key: str, items: list[dict[str, object]]) -> list[dict[str, object]]:
    return sorted(
        items,
        key=lambda item: (
            1 if item.get("conflict_candidate_key") else 0,
            temporal_rank(item, bucket_key),
            confidence_sort_rank(str(item.get("confidence"))),
            -int(item.get("supporting_session_count", 0)) if bucket_key not in TEMPORAL_BUCKETS else 0,
            -int(item.get("supporting_day_count", 0)) if bucket_key not in TEMPORAL_BUCKETS else 0,
            -int(item.get("recurrence_count", 0)),
            invert_timestamp_sort_key(str(item.get("last_seen_at", ""))),
            str(item.get("statement", "")).lower(),
        ),
    )


def temporal_rank(item: dict[str, object], bucket_key: str) -> int:
    if bucket_key not in TEMPORAL_BUCKETS:
        return 0
    status = str(item.get("temporal_status", ""))
    return {"active": 0, "historical": 1, "superseded": 2, "durable": 3}.get(status, 4)


def confidence_sort_rank(confidence: str) -> int:
    return {"explicit": 0, "strong": 1, "inferred": 2}.get(confidence, 3)


def invert_timestamp_sort_key(value: str) -> str:
    return "".join(chr(255 - ord(char)) for char in value)


def humanize_item_type(item_type: str) -> str:
    return item_type.replace("_", " ").title()


def determine_wiki_mode(
    page: WikiPage,
    prior_state: WikiStateRecord | None,
    config: WikiConfig,
    provider_model: str,
    wiki_dir: Path,
) -> str:
    if prior_state is None:
        return "render"
    if prior_state.status != "rendered":
        return "render"
    if prior_state.wiki_schema_version != WIKI_SCHEMA_VERSION:
        return "render"
    if prior_state.renderer != config.renderer:
        return "render"
    if prior_state.renderer_version != config.renderer_version:
        return "render"
    if prior_state.page_config_version != config.page_config_version:
        return "render"
    if prior_state.synthesis_prompt_version != config.synthesis_prompt_version:
        return "render"
    if prior_state.synthesis_schema_version != config.synthesis_schema_version:
        return "render"
    if prior_state.provider_type != config.provider.provider_type:
        return "render"
    if prior_state.provider_model != provider_model:
        return "render"
    if prior_state.input_digest != page_digest(page):
        return "render"
    if not (wiki_dir / prior_state.relative_page_path).exists():
        return "render"
    if not (wiki_dir / prior_state.relative_manifest_path).exists():
        return "render"
    return "unchanged"


def page_digest(page: WikiPage) -> str:
    payload = json.dumps(page.to_dict(), sort_keys=True, separators=(",", ":"))
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()


def build_page_artifacts(
    page: WikiPage,
    config: WikiConfig,
    staged_root: Path,
) -> dict[str, object]:
    synthesized = synthesize_page_packet(page, config)
    enriched_claims, citations = enrich_synthesized_claims(page, synthesized)
    markdown, rendered_citations = render_markdown(page, enriched_claims, citations, config)
    manifest = build_page_manifest(page, enriched_claims, rendered_citations, config)

    staged_page_path = staged_root / page.relative_page_path
    staged_manifest_path = staged_root / page.relative_manifest_path
    write_text(staged_page_path, markdown)
    write_text(staged_manifest_path, json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    return {
        "markdown": markdown,
        "manifest": manifest,
        "rendered_citations": rendered_citations,
        "page_path": staged_page_path,
        "manifest_path": staged_manifest_path,
    }


def synthesize_page_packet(page: WikiPage, config: WikiConfig) -> dict[str, object]:
    if not page.input_item_keys:
        return {
            "page_intro_claims": [],
            "section_summaries": [],
        }
    prompt_payload, support_id_map = build_synthesis_payload(page, config)
    system_prompt = (
        "You synthesize wiki claims from extracted evidence. "
        "Use only the provided support ids and evidence. "
        "Never invent facts, projects, dates, or provenance. "
        "Return concise JSON only."
    )
    user_prompt = json.dumps(prompt_payload, indent=2, sort_keys=True)
    raw_output = call_openai_structured_json(
        config=config,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        schema=build_synthesis_schema(config, sorted(support_id_map)),
    )
    return validate_synthesis_output(page, raw_output, config, support_id_map)


def build_synthesis_payload(page: WikiPage, config: WikiConfig) -> tuple[dict[str, object], dict[str, list[str]]]:
    payload = {
        "page_id": page.page_id,
        "page_type": page.page_type,
        "domain": page.domain,
        "bucket": page.bucket,
        "title": page.title,
        "namespace": page.namespace,
        "related_pages": [dict(item) for item in page.related_pages],
        "related_domains": list(page.related_domains),
        "source_count": page.source_count,
        "conflict_count": page.conflict_count,
    }
    support_id_map: dict[str, list[str]] = {}
    support_counter = 1
    synthesis_sections: list[dict[str, object]] = []
    prompt_input_item_keys: list[str] = []
    for section in page.deterministic_sections:
        section_id = str(section["section_id"])
        section_payload = {
            key: value
            for key, value in dict(section).items()
            if key not in {"page_link", "items"}
        }
        section_items: list[dict[str, object]] = []
        section_support_ids: list[str] = []
        for item in list(section.get("items", []))[:MAX_SYNTHESIS_ITEMS_PER_SECTION]:
            support_id = f"I{support_counter:03d}"
            support_counter += 1
            support_id_map[support_id] = [str(item["item_key"])]
            prompt_input_item_keys.append(support_id)
            section_support_ids.append(support_id)
            section_items.append(build_synthesis_item_view(item, support_id))
        section_payload["items"] = section_items
        allowed_support_ids = list(section_support_ids)
        if page.page_type == "domain_index" and section_support_ids:
            section_support_id = f"SEC_{normalize_support_fragment(section_id)}"
            support_id_map[section_support_id] = [
                item_id
                for support_id in section_support_ids
                for item_id in support_id_map.get(support_id, [])
            ]
            allowed_support_ids.append(section_support_id)
        section_payload["allowed_support_ids"] = allowed_support_ids
        synthesis_sections.append(section_payload)
    payload["deterministic_sections"] = synthesis_sections
    payload["input_item_keys"] = prompt_input_item_keys
    payload["allowed_support_ids"] = sorted(support_id_map)
    payload["approved_latent_types"] = list(config.approved_latent_types)
    payload["instructions"] = {
        "page_intro_claim_limit": 4,
        "section_claim_limit": 3,
        "claim_style": "one sentence per claim, supporting_item_ids must come only from allowed_support_ids",
        "confidence_allowed": sorted(VALID_CLAIM_CONFIDENCE),
        "index_page_rule": "do not cite empty sections, page links, or any support id outside allowed_support_ids",
    }
    return payload, support_id_map


def build_synthesis_item_view(item: dict[str, object], support_id: str) -> dict[str, object]:
    statement = str(item.get("statement", ""))
    if len(statement) > MAX_SYNTHESIS_STATEMENT_CHARS:
        statement = statement[: MAX_SYNTHESIS_STATEMENT_CHARS - 3].rstrip() + "..."
    return {
        "support_id": support_id,
        "item_key": str(item["item_key"]),
        "item_type": str(item["item_type"]),
        "statement": statement,
        "confidence": str(item["confidence"]),
        "temporal_status": str(item["temporal_status"]),
        "recurrence_count": int(item["recurrence_count"]),
        "subject_key": str(item["subject_key"]),
        "conflict_candidate_key": item.get("conflict_candidate_key"),
    }


def build_synthesis_schema(config: WikiConfig, allowed_support_ids: list[str]) -> dict[str, object]:
    support_id_item_schema: dict[str, object] = {"type": "string", "enum": allowed_support_ids}
    claim_schema: dict[str, object] = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "text": {"type": "string"},
            "latent_type": {"type": "string", "enum": list(config.approved_latent_types)},
            "confidence": {"type": "string", "enum": sorted(VALID_CLAIM_CONFIDENCE)},
            "supporting_item_ids": {
                "type": "array",
                "items": support_id_item_schema,
                "minItems": 1,
            },
        },
        "required": ["text", "latent_type", "confidence", "supporting_item_ids"],
    }
    return {
        "name": "sessionmemory_wiki_page",
        "schema": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "page_intro_claims": {
                    "type": "array",
                    "items": claim_schema,
                },
                "section_summaries": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "section_id": {"type": "string"},
                            "claims": {
                                "type": "array",
                                "items": claim_schema,
                            },
                        },
                        "required": ["section_id", "claims"],
                    },
                },
            },
            "required": ["page_intro_claims", "section_summaries"],
        },
    }


def call_openai_structured_json(
    config: WikiConfig,
    system_prompt: str,
    user_prompt: str,
    schema: dict[str, object],
) -> dict[str, object]:
    api_key = config.provider.resolve_api_key()
    if not api_key:
        raise WikiError(
            f"Missing OpenAI API key in environment variable {config.provider.api_key_env}"
        )
    payload = {
        "model": config.provider.resolve_model(),
        "temperature": config.provider.temperature,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": str(schema["name"]),
                "strict": True,
                "schema": schema["schema"],
            },
        },
    }
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url=f"{config.provider.resolve_base_url().rstrip('/')}/v1/chat/completions",
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            response_payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body_text = exc.read().decode("utf-8", errors="replace")
        raise WikiError(f"OpenAI wiki synthesis request failed: {exc.code} {body_text}") from exc
    except urllib.error.URLError as exc:
        raise WikiError(f"OpenAI wiki synthesis request failed: {exc.reason}") from exc

    try:
        message = response_payload["choices"][0]["message"]
    except (KeyError, IndexError, TypeError) as exc:
        raise WikiError("OpenAI wiki synthesis response was missing choices[0].message") from exc
    if message.get("refusal"):
        raise WikiError(f"OpenAI wiki synthesis refusal: {message['refusal']}")
    content = message.get("content")
    content_text = coerce_message_content_to_text(content)
    try:
        payload_dict = json.loads(content_text)
    except json.JSONDecodeError as exc:
        raise WikiError("OpenAI wiki synthesis response did not contain valid JSON") from exc
    if not isinstance(payload_dict, dict):
        raise WikiError("OpenAI wiki synthesis response root must be an object")
    return payload_dict


def coerce_message_content_to_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, dict):
                if isinstance(item.get("text"), str):
                    parts.append(str(item["text"]))
                elif item.get("type") == "text" and isinstance(item.get("text"), str):
                    parts.append(str(item["text"]))
        return "".join(parts)
    raise WikiError("OpenAI wiki synthesis message content was not a supported text shape")


def validate_synthesis_output(
    page: WikiPage,
    raw_output: dict[str, object],
    config: WikiConfig,
    support_id_map: dict[str, list[str]],
) -> dict[str, object]:
    intro_claims = raw_output.get("page_intro_claims")
    section_summaries = raw_output.get("section_summaries")
    if not isinstance(intro_claims, list) or not isinstance(section_summaries, list):
        raise WikiError(f"Invalid wiki synthesis payload for page {page.page_id}")
    valid_section_ids = {str(section["section_id"]) for section in page.deterministic_sections}
    page_item_map = build_page_item_map(page)
    validated_intro = []
    for claim in intro_claims:
        validated = validate_claim(claim, support_id_map, config, page.page_id)
        if claim_is_renderable(page, validated, page_item_map, section_id="summary", config=config):
            validated_intro.append(validated)
    validated_sections: list[dict[str, object]] = []
    for section in section_summaries:
        if not isinstance(section, dict):
            raise WikiError(f"Invalid section summary payload for page {page.page_id}")
        section_id = str(section.get("section_id", ""))
        if section_id not in valid_section_ids:
            raise WikiError(f"Unknown section_id in wiki synthesis for page {page.page_id}: {section_id}")
        claims_payload = section.get("claims")
        if not isinstance(claims_payload, list):
            raise WikiError(f"Invalid claims array for page {page.page_id} section {section_id}")
        validated_claims: list[dict[str, object]] = []
        for claim in claims_payload:
            validated = validate_claim(claim, support_id_map, config, page.page_id)
            if claim_is_renderable(page, validated, page_item_map, section_id=section_id, config=config):
                validated_claims.append(validated)
        validated_sections.append(
            {
                "section_id": section_id,
                "claims": validated_claims,
            }
        )
    return {
        "page_intro_claims": validated_intro,
        "section_summaries": validated_sections,
    }


def validate_claim(
    claim: object,
    support_id_map: dict[str, list[str]],
    config: WikiConfig,
    page_id: str,
) -> dict[str, object]:
    if not isinstance(claim, dict):
        raise WikiError(f"Invalid synthesized claim payload for page {page_id}")
    text = str(claim.get("text", "")).strip()
    latent_type = str(claim.get("latent_type", "")).strip()
    confidence = str(claim.get("confidence", "")).strip()
    supporting_item_ids = claim.get("supporting_item_ids")
    if not text:
        raise WikiError(f"Synthesized claim text was empty for page {page_id}")
    if latent_type not in config.approved_latent_types:
        raise WikiError(f"Unsupported latent_type in wiki synthesis for page {page_id}: {latent_type}")
    if confidence not in VALID_CLAIM_CONFIDENCE:
        raise WikiError(f"Unsupported synthesized claim confidence for page {page_id}: {confidence}")
    if not isinstance(supporting_item_ids, list) or not supporting_item_ids:
        raise WikiError(f"Synthesized claim had no supporting_item_ids for page {page_id}")
    requested_support_ids = [str(item_id) for item_id in supporting_item_ids]
    unknown = [item_id for item_id in requested_support_ids if item_id not in support_id_map]
    if unknown:
        raise WikiError(
            f"Synthesized claim referenced unknown item ids for page {page_id}: {', '.join(sorted(unknown))}"
        )
    item_ids = dedupe_preserving_order(
        [
            item_id
            for support_id in requested_support_ids
            for item_id in support_id_map.get(support_id, [])
        ]
    )
    if not item_ids:
        raise WikiError(f"Synthesized claim resolved to no supporting items for page {page_id}")
    return {
        "text": text,
        "latent_type": latent_type,
        "confidence": confidence,
        "supporting_item_ids": item_ids,
    }


def claim_is_renderable(
    page: WikiPage,
    claim: dict[str, object],
    item_map: dict[str, dict[str, object]],
    *,
    section_id: str,
    config: WikiConfig,
) -> bool:
    text = normalize_text(str(claim["text"]))
    if not text:
        return False
    if any(pattern in text for pattern in config.generic_claim_banned_patterns):
        return False
    if GENERIC_CLAIM_PATTERN.search(str(claim["text"])) and not claim_has_concrete_overlap(claim, item_map):
        return False
    if section_id != "summary" and not any(str(section["section_id"]) == section_id and section.get("items") for section in page.deterministic_sections):
        return False
    return claim_has_concrete_overlap(claim, item_map)


def claim_has_concrete_overlap(claim: dict[str, object], item_map: dict[str, dict[str, object]]) -> bool:
    claim_tokens = {
        token
        for token in re.findall(r"[a-z0-9][a-z0-9._/-]*", normalize_text(str(claim["text"])))
        if len(token) >= 4 and token not in {"that", "with", "from", "there", "clear", "ongoing", "important"}
    }
    if not claim_tokens:
        return False
    supporting_tokens = {
        token
        for item_id in claim["supporting_item_ids"]
        for token in re.findall(
            r"[a-z0-9][a-z0-9._/-]*",
            normalize_text(str(item_map.get(item_id, {}).get("statement", ""))),
        )
        if len(token) >= 4
    }
    return bool(claim_tokens & supporting_tokens)


def enrich_synthesized_claims(
    page: WikiPage,
    synthesized: dict[str, object],
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    item_map = build_page_item_map(page)
    enriched_claims: list[dict[str, object]] = []
    citations: list[dict[str, object]] = []
    claim_index = 0

    for claim in synthesized["page_intro_claims"]:
        claim_index += 1
        claim_id = f"claim-{claim_index}"
        enriched_claim = enrich_claim(claim_id, claim, item_map, section_id="summary")
        enriched_claims.append(enriched_claim)
        citations.append(build_claim_citation(enriched_claim))

    for section in synthesized["section_summaries"]:
        section_id = str(section["section_id"])
        for claim in section["claims"]:
            claim_index += 1
            claim_id = f"claim-{claim_index}"
            enriched_claim = enrich_claim(claim_id, claim, item_map, section_id=section_id)
            enriched_claims.append(enriched_claim)
            citations.append(build_claim_citation(enriched_claim))
    return enriched_claims, citations


def build_page_item_map(page: WikiPage) -> dict[str, dict[str, object]]:
    item_map: dict[str, dict[str, object]] = {}
    for section in page.deterministic_sections:
        for item in section.get("items", []):
            item_map[str(item["item_key"])] = dict(item)
    return item_map


def normalize_support_fragment(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return normalized or "section"


def enrich_claim(
    claim_id: str,
    claim: dict[str, object],
    item_map: dict[str, dict[str, object]],
    section_id: str,
) -> dict[str, object]:
    supporting_items = [item_map[item_id] for item_id in claim["supporting_item_ids"]]
    provenance_refs = dedupe_dict_list(
        [
            dict(ref)
            for item in supporting_items
            for ref in item.get("provenance_refs", [])[:MAX_CITATION_PROVENANCE_REFS]
        ]
    )
    return {
        "claim_id": claim_id,
        "section_id": section_id,
        "text": claim["text"],
        "latent_type": claim["latent_type"],
        "confidence": claim["confidence"],
        "supporting_item_ids": list(claim["supporting_item_ids"]),
        "provenance_refs": provenance_refs,
    }


def build_claim_citation(claim: dict[str, object]) -> dict[str, object]:
    return {
        "citation_id": claim["claim_id"],
        "kind": "synthesized_claim",
        "label": claim["claim_id"],
        "item_keys": list(claim["supporting_item_ids"]),
        "provenance_refs": list(claim["provenance_refs"]),
    }


def render_markdown(
    page: WikiPage,
    enriched_claims: list[dict[str, object]],
    claim_citations: list[dict[str, object]],
    config: WikiConfig,
) -> tuple[str, list[dict[str, object]]]:
    lines: list[str] = []
    all_citations: list[dict[str, object]] = list(claim_citations)
    synthesized_by_section: dict[str, list[dict[str, object]]] = defaultdict(list)
    for claim in enriched_claims:
        synthesized_by_section[str(claim["section_id"])].append(claim)

    lines.extend(render_frontmatter(page, enriched_claims, config))
    lines.append(f"# {page.title}")
    lines.append("")
    lines.extend(render_navigation_block(page))
    lines.append("")

    summary_claims = synthesized_by_section.get("summary", [])
    lines.append("## Summary")
    if summary_claims:
        for claim in summary_claims:
            lines.append(
                f"- {claim['text']} [latent: {claim['latent_type']}] [confidence: {claim['confidence']}][^{claim['claim_id']}]"
            )
    else:
        lines.append("- No synthesized summary yet.")
    lines.append("")

    for section in page.deterministic_sections:
        section_id = str(section["section_id"])
        lines.append(f"## {section['title']}")
        if "page_link" in section:
            lines.append(f"Related page: {section['page_link']}")
        section_claims = synthesized_by_section.get(section_id, [])
        if section_claims:
            for claim in section_claims:
                lines.append(
                    f"- {claim['text']} [latent: {claim['latent_type']}] [confidence: {claim['confidence']}][^{claim['claim_id']}]"
                )
        else:
            lines.append("- No synthesized section summary yet.")
        lines.append("")
        lines.append("### Canonical Items" if page.page_type != "domain_index" else "### Preview Items")
        section_items = section.get("items", [])
        if section_items:
            for index, item in enumerate(section_items, start=1):
                if page.page_type == "domain_index":
                    lines.append(render_index_preview_bullet(item))
                    continue
                citation_id = f"item-{section_id}-{index}"
                all_citations.append(build_item_citation(citation_id, item))
                lines.append(render_item_bullet(item, citation_id))
        else:
            lines.append("- No evidence collected for this page yet.")
        lines.append("")

    lines.append("## Sources")
    if all_citations:
        for citation in all_citations:
            lines.append(render_citation_footnote(citation))
    else:
        lines.append("- No sources available yet.")
    lines.append("")
    return "\n".join(lines), all_citations


def render_frontmatter(page: WikiPage, enriched_claims: list[dict[str, object]], config: WikiConfig) -> list[str]:
    lines = [
        "---",
        f'title: "{page.title}"',
        f'page_id: "{page.page_id}"',
        f'domain: "{page.domain}"',
        f'bucket: "{page.bucket}"',
        f'page_type: "{page.page_type}"',
        f'renderer: "{config.renderer}"',
        f"generated_at: {utc_now()}",
        f"source_count: {page.source_count}",
        f"claim_count: {len(enriched_claims)}",
        "tags:",
    ]
    for tag in page.tags:
        lines.append(f"  - {tag}")
    lines.append("---")
    return lines


def render_navigation_block(page: WikiPage) -> list[str]:
    nav_links = [item["wikilink"] for item in page.related_pages]
    if page.related_domains:
        domain_links = ", ".join(
            obsidian_wikilink(domain_to_path(domain), domain_title(domain)) for domain in page.related_domains
        )
        return [f"Navigation: {' | '.join(nav_links)}", f"Related Domains: {domain_links}"]
    return [f"Navigation: {' | '.join(nav_links)}"]


def render_item_bullet(item: dict[str, object], citation_id: str) -> str:
    markers: list[str] = [f"confidence: {item['confidence']}"]
    if item["temporal_status"] != "durable":
        markers.append(f"status: {item['temporal_status']}")
    markers.append(f"recurrence: {item['recurrence_count']}")
    if item.get("conflict_candidate_key"):
        markers.append("conflict")
    marker_text = " ".join(f"[{marker}]" for marker in markers)
    return f"- {item['statement']} {marker_text}[^{citation_id}]"


def render_index_preview_bullet(item: dict[str, object]) -> str:
    markers = [f"confidence: {item['confidence']}", f"recurrence: {item['recurrence_count']}"]
    return f"- {item['statement']} {' '.join(f'[{marker}]' for marker in markers)}"


def render_citation_footnote(citation: dict[str, object]) -> str:
    item_keys = ", ".join(citation.get("item_keys", []))
    refs = []
    for provenance in citation.get("provenance_refs", []):
        source_id = str(provenance.get("source_id", ""))
        line_span = f"{provenance.get('start_line_no')}-{provenance.get('end_line_no')}"
        refs.append(f"{source_id} lines {line_span}")
    ref_text = "; ".join(refs) if refs else "no provenance refs"
    return f"[^{citation['citation_id']}]: items {item_keys}; {ref_text}"


def build_item_citation(citation_id: str, item: dict[str, object]) -> dict[str, object]:
    return {
        "citation_id": citation_id,
        "kind": "deterministic_item",
        "label": citation_id,
        "item_keys": [str(item["item_key"])],
        "provenance_refs": [dict(ref) for ref in item.get("provenance_refs", [])],
    }


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", str(text).strip().lower())


def build_page_manifest(
    page: WikiPage,
    synthesized_claims: list[dict[str, object]],
    rendered_citations: list[dict[str, object]],
    config: WikiConfig,
) -> dict[str, object]:
    return {
        "page_id": page.page_id,
        "page_type": page.page_type,
        "domain": page.domain,
        "bucket": page.bucket,
        "renderer": config.renderer,
        "versions": {
            "wiki_schema_version": WIKI_SCHEMA_VERSION,
            "renderer_version": config.renderer_version,
            "page_config_version": config.page_config_version,
            "synthesis_prompt_version": config.synthesis_prompt_version,
            "synthesis_schema_version": config.synthesis_schema_version,
        },
        "input_item_keys": list(page.input_item_keys),
        "synthesized_claims": synthesized_claims,
        "citations": rendered_citations,
        "rendered_page_metadata": {
            "title": page.title,
            "relative_page_path": page.relative_page_path,
            "related_pages": [dict(item) for item in page.related_pages],
            "related_domains": list(page.related_domains),
            "source_count": page.source_count,
            "claim_count": len(synthesized_claims),
            "conflict_count": page.conflict_count,
        },
    }


def validate_page_artifacts(page: WikiPage, artifacts: dict[str, object], config: WikiConfig) -> None:
    markdown = str(artifacts["markdown"])
    manifest = dict(artifacts["manifest"])
    if manifest["page_id"] != page.page_id:
        raise WikiError(f"Page manifest id mismatch for {page.page_id}")
    if sorted(manifest["input_item_keys"]) != sorted(page.input_item_keys):
        raise WikiError(f"Page manifest input_item_keys mismatch for {page.page_id}")
    citations_by_id = {str(citation["citation_id"]): citation for citation in manifest["citations"]}
    for claim in manifest["synthesized_claims"]:
        for item_id in claim["supporting_item_ids"]:
            if item_id not in page.input_item_keys:
                raise WikiError(f"Synthesized claim referenced unknown item in manifest for {page.page_id}")
    markdown_citation_ids = set(re.findall(r"\[\^([A-Za-z0-9._-]+)\]", markdown))
    if page.input_item_keys and not markdown_citation_ids and page.page_type != "domain_index":
        raise WikiError(f"No inline citations were rendered for {page.page_id}")
    unknown_citations = sorted(markdown_citation_ids - set(citations_by_id))
    if unknown_citations:
        raise WikiError(f"Unknown inline citations in markdown for {page.page_id}: {', '.join(unknown_citations)}")
    if not markdown.startswith("---\n"):
        raise WikiError(f"Missing frontmatter for {page.page_id}")
    if "[[" not in markdown:
        raise WikiError(f"Missing wikilinks in rendered markdown for {page.page_id}")
    if "## Sources" not in markdown:
        raise WikiError(f"Missing Sources section for {page.page_id}")
    page_size_cap = page_size_cap_for(page, config)
    if page_size_cap and len(markdown.encode("utf-8")) > page_size_cap:
        raise WikiError(f"Rendered page exceeds configured size cap for {page.page_id}")
    if config.renderer != "obsidian_markdown":
        raise WikiError(f"Unsupported renderer for page validation: {config.renderer}")


def build_state_record(
    page: WikiPage,
    config: WikiConfig,
    provider_model: str,
    input_digest: str,
    claim_count: int,
    run_id: str,
) -> WikiStateRecord:
    return WikiStateRecord(
        page_id=page.page_id,
        domain=page.domain,
        bucket=page.bucket,
        page_type=page.page_type,
        wiki_schema_version=WIKI_SCHEMA_VERSION,
        renderer=config.renderer,
        renderer_version=config.renderer_version,
        page_config_version=config.page_config_version,
        synthesis_prompt_version=config.synthesis_prompt_version,
        synthesis_schema_version=config.synthesis_schema_version,
        provider_type=config.provider.provider_type,
        provider_model=provider_model,
        input_digest=input_digest,
        input_item_count=len(page.input_item_keys),
        claim_count=claim_count,
        status="rendered",
        relative_page_path=page.relative_page_path,
        relative_manifest_path=page.relative_manifest_path,
        last_rendered_at=utc_now(),
        last_run_id=run_id,
    )


def build_page_notices(page: WikiPage, artifacts: dict[str, object], run_id: str) -> list[WikiNotice]:
    notices: list[WikiNotice] = []
    manifest = dict(artifacts["manifest"])
    if manifest["rendered_page_metadata"]["conflict_count"] > 0:
        notices.append(
            WikiNotice(
                run_id=run_id,
                page_id=page.page_id,
                severity="warning",
                notice_type="conflict_items",
                summary="page contains conflict candidate items",
            )
        )
    if any(claim["confidence"] == "inferred" for claim in manifest["synthesized_claims"]):
        notices.append(
            WikiNotice(
                run_id=run_id,
                page_id=page.page_id,
                severity="warning",
                notice_type="low_confidence_claims",
                summary="page contains inferred synthesized claims",
            )
        )
    if any(
        "[confidence: inferred]" in line for line in str(artifacts["markdown"]).splitlines()
    ):
        notices.append(
            WikiNotice(
                run_id=run_id,
                page_id=page.page_id,
                severity="warning",
                notice_type="low_confidence_items",
                summary="page contains inferred deterministic items",
            )
        )
    if not page.input_item_keys:
        notices.append(
            WikiNotice(
                run_id=run_id,
                page_id=page.page_id,
                severity="warning",
                notice_type="empty_page",
                summary="page rendered with no canonical items",
            )
        )
    return notices


def page_size_cap_for(page: WikiPage, config: WikiConfig) -> int:
    if page.page_type == "domain_index":
        return int(config.page_size_caps.get("index", 25 * 1024))
    return int(
        config.page_size_caps.get(
            page.bucket,
            config.page_size_caps.get("default_bucket", 200 * 1024),
        )
    )


def validate_state_against_page_plan(
    page_plan: list[WikiPage],
    wiki_state: dict[str, WikiStateRecord],
    config: WikiConfig,
    provider_model: str,
) -> None:
    expected_page_ids = {page.page_id for page in page_plan}
    for page in page_plan:
        state_record = wiki_state.get(page.page_id)
        if state_record is None:
            raise WikiError(f"Missing wiki state for page {page.page_id}")
        if state_record.status != "rendered":
            raise WikiError(f"Wiki state did not mark page rendered: {page.page_id}")
        if state_record.renderer != config.renderer:
            raise WikiError(f"Renderer mismatch in wiki state for page {page.page_id}")
        if state_record.provider_model != provider_model:
            raise WikiError(f"Provider model mismatch in wiki state for page {page.page_id}")
        if state_record.input_digest != page_digest(page):
            raise WikiError(f"Input digest mismatch in wiki state for page {page.page_id}")
    stale = sorted(set(wiki_state) - expected_page_ids)
    if stale:
        raise WikiError(f"Wiki state contains pages outside the current page plan: {', '.join(stale[:5])}")


def build_state_payload(state_records: dict[str, WikiStateRecord]) -> dict[str, object]:
    return {
        "schema_version": STATE_SCHEMA_VERSION,
        "wiki_schema_version": WIKI_SCHEMA_VERSION,
        "generated_at": utc_now(),
        "page_count": len(state_records),
        "pages": [state_records[page_id].to_dict() for page_id in sorted(state_records)],
    }


def promote_staged_pages(
    staging_root: Path,
    wiki_dir: Path,
    changed_page_ids: list[str],
    page_plan: list[WikiPage],
    previous_state: dict[str, WikiStateRecord],
    stale_page_ids: list[str],
) -> None:
    page_map = {page.page_id: page for page in page_plan}
    for page_id in changed_page_ids:
        page = page_map[page_id]
        staged_page_path = staging_root / page.relative_page_path
        staged_manifest_path = staging_root / page.relative_manifest_path
        target_page_path = wiki_dir / page.relative_page_path
        target_manifest_path = wiki_dir / page.relative_manifest_path
        ensure_directory(target_page_path.parent)
        ensure_directory(target_manifest_path.parent)
        os.replace(staged_page_path, target_page_path)
        os.replace(staged_manifest_path, target_manifest_path)
    for page_id in stale_page_ids:
        previous_record = previous_state.get(page_id)
        if previous_record is None:
            continue
        (wiki_dir / previous_record.relative_page_path).unlink(missing_ok=True)
        (wiki_dir / previous_record.relative_manifest_path).unlink(missing_ok=True)


def cleanup_staging_root(staging_root: Path) -> None:
    if staging_root.exists():
        shutil.rmtree(staging_root, ignore_errors=True)


def read_jsonl_required(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        raise WikiError(f"Missing JSONL artifact: {path}")
    records: list[dict[str, object]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError as exc:
            raise WikiError(f"Invalid JSONL artifact line {line_no}: {path}") from exc
        if not isinstance(payload, dict):
            raise WikiError(f"JSONL artifact line {line_no} is not an object: {path}")
        records.append(payload)
    return records


def write_text(path: Path, text: str) -> None:
    ensure_directory(path.parent)
    path.write_text(text, encoding="utf-8", newline="\n")


def obsidian_wikilink(target: str, label: str) -> str:
    return f"[[{target}|{label}]]"


def page_id_for_namespace(namespace: str, page_key: str) -> str:
    return f"{namespace}/{page_key}"


def domain_to_path(domain: str) -> str:
    if domain == "global":
        return "global/index"
    if domain == "cross-project":
        return "projects/cross-project/index"
    if domain in PROJECT_LABELS:
        return f"projects/{domain}/index"
    return f"{domain}/index"


def domain_title(domain: str) -> str:
    title_map = {
        "global": "Global",
        "ai-trader": "AI Trader",
        "open-brain": "Open Brain",
        "ai-scientist": "AI Scientist",
        "cross-project": "Cross-Project",
        "unclassified": "Unclassified",
    }
    return title_map.get(domain, domain.replace("-", " ").title())


def dedupe_preserving_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        ordered.append(item)
    return ordered


def dedupe_dict_list(items: list[dict[str, object]]) -> list[dict[str, object]]:
    seen: set[str] = set()
    deduped: list[dict[str, object]] = []
    for item in items:
        signature = json.dumps(item, sort_keys=True, separators=(",", ":"))
        if signature in seen:
            continue
        seen.add(signature)
        deduped.append(item)
    return deduped
