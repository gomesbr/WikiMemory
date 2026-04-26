from __future__ import annotations

import json
import platform
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .adapters import BOOTSTRAP_RENDERERS, LOG_ADAPTERS, MARKDOWN_RENDERERS, PROJECT_DELTA_ADAPTERS
from .discovery import DiscoveryError

PRODUCT_SCHEMA_VERSION = 1


class ProductConfigError(DiscoveryError):
    """Fatal product-config error."""


@dataclass(frozen=True)
class EnvironmentConfig:
    operating_system: str
    editor: str
    repo_root: str


@dataclass(frozen=True)
class AgentPlatformConfig:
    platform: str
    bootstrap_renderer: str
    bootstrap_target_path: str


@dataclass(frozen=True)
class MarkdownOutputConfig:
    mode: str
    root_dir: str
    enable_frontmatter: bool
    enable_tags: bool
    enable_wikilinks: bool


@dataclass(frozen=True)
class LogSourceConfig:
    adapter: str
    root_alias: str
    absolute_path: str
    include_glob: str


@dataclass(frozen=True)
class ProjectSourceConfig:
    adapter: str
    project_root: str
    include_untracked: bool


@dataclass(frozen=True)
class ProjectAliasConfig:
    slug: str
    aliases: tuple[str, ...]


@dataclass(frozen=True)
class RoutingProviderConfig:
    provider_type: str
    api_key_env: str
    base_url_env: str
    model_env: str
    default_model: str
    temperature: float


@dataclass(frozen=True)
class MemoryExtractionConfig:
    enabled: bool
    fallback_to_deterministic: bool
    window_record_limit: int
    window_overlap_records: int
    max_window_chars: int
    max_windows_per_run: int
    max_candidates_per_window: int
    provider: RoutingProviderConfig


@dataclass(frozen=True)
class ProjectRoutingConfig:
    enabled: bool
    unresolved_project: str
    min_confidence: str
    max_sources_per_run: int
    max_sample_records_per_source: int
    provider: RoutingProviderConfig


@dataclass(frozen=True)
class SchedulerConfig:
    mode: str
    scan_on_startup: bool
    tick_seconds: int
    project_delta_enabled: bool
    log_delta_enabled: bool
    allowed_weekdays: tuple[str, ...]
    run_hour_local: int
    run_minute_local: int
    ingest_interval_hours: int
    lint_interval_hours: int
    require_log_update_for_ingest: bool
    lint_autofix_enabled: bool
    lint_autofix_max_rounds: int
    consumer_profile_extraction_model: str
    consumer_profile_merge_model: str
    consumer_profile_window_max_chars: int


@dataclass(frozen=True)
class PolicyConfig:
    require_confirmation_for_inferred_rule_promotion: bool
    include_failed_attempts_in_recent_only_if_state_changes: bool
    ignore_agent_reasoning_for_durable_memory: bool
    explicit_promotion_has_priority: bool


@dataclass(frozen=True)
class ProductConfig:
    schema_version: int
    product_schema_version: int
    environment: EnvironmentConfig
    agent_platform: AgentPlatformConfig
    markdown_output: MarkdownOutputConfig
    log_sources: tuple[LogSourceConfig, ...]
    project_sources: tuple[ProjectSourceConfig, ...]
    project_aliases: tuple[ProjectAliasConfig, ...]
    project_routing: ProjectRoutingConfig
    memory_extraction: MemoryExtractionConfig
    scheduler: SchedulerConfig
    policies: PolicyConfig

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "product_schema_version": self.product_schema_version,
            "environment": self.environment.__dict__,
            "agent_platform": self.agent_platform.__dict__,
            "markdown_output": self.markdown_output.__dict__,
            "log_sources": [source.__dict__ for source in self.log_sources],
            "project_sources": [source.__dict__ for source in self.project_sources],
            "project_aliases": [
                {"slug": alias.slug, "aliases": list(alias.aliases)}
                for alias in self.project_aliases
            ],
            "project_routing": {
                "enabled": self.project_routing.enabled,
                "unresolved_project": self.project_routing.unresolved_project,
                "min_confidence": self.project_routing.min_confidence,
                "max_sources_per_run": self.project_routing.max_sources_per_run,
                "max_sample_records_per_source": self.project_routing.max_sample_records_per_source,
                "provider": self.project_routing.provider.__dict__,
            },
            "memory_extraction": {
                "enabled": self.memory_extraction.enabled,
                "fallback_to_deterministic": self.memory_extraction.fallback_to_deterministic,
                "window_record_limit": self.memory_extraction.window_record_limit,
                "window_overlap_records": self.memory_extraction.window_overlap_records,
                "max_window_chars": self.memory_extraction.max_window_chars,
                "max_windows_per_run": self.memory_extraction.max_windows_per_run,
                "max_candidates_per_window": self.memory_extraction.max_candidates_per_window,
                "provider": self.memory_extraction.provider.__dict__,
            },
            "scheduler": self.scheduler.__dict__,
            "policies": self.policies.__dict__,
        }


def default_product_config(project_root: Path | str) -> ProductConfig:
    project_root = Path(project_root).resolve()
    os_name = detect_operating_system()
    return ProductConfig(
        schema_version=1,
        product_schema_version=PRODUCT_SCHEMA_VERSION,
        environment=EnvironmentConfig(
            operating_system=os_name,
            editor="cursor",
            repo_root=str(project_root),
        ),
        agent_platform=AgentPlatformConfig(
            platform="codex",
            bootstrap_renderer="codex_agents_md",
            bootstrap_target_path="AGENTS.md",
        ),
        markdown_output=MarkdownOutputConfig(
            mode="obsidian_markdown",
            root_dir="memory",
            enable_frontmatter=True,
            enable_tags=True,
            enable_wikilinks=True,
        ),
        log_sources=(
            LogSourceConfig(
                adapter="codex_jsonl",
                root_alias="codex_sessions",
                absolute_path="${WIKIMEMORY_CODEX_SESSIONS_ROOT}",
                include_glob="**/*.jsonl",
            ),
        ),
        project_sources=(
            ProjectSourceConfig(
                adapter="git_worktree",
                project_root=str(project_root),
                include_untracked=True,
            ),
        ),
        project_aliases=(
            ProjectAliasConfig(slug=slugify(project_root.name), aliases=(project_root.name,)),
        ),
        project_routing=default_project_routing_config(),
        memory_extraction=default_memory_extraction_config(enabled=False),
        scheduler=SchedulerConfig(
            mode="manual",
            scan_on_startup=True,
            tick_seconds=900,
            project_delta_enabled=True,
            log_delta_enabled=True,
            allowed_weekdays=("monday", "tuesday", "wednesday", "thursday", "friday"),
            run_hour_local=9,
            run_minute_local=0,
            ingest_interval_hours=24,
            lint_interval_hours=24,
            require_log_update_for_ingest=True,
            lint_autofix_enabled=False,
            lint_autofix_max_rounds=1,
            consumer_profile_extraction_model="gpt-4o-mini",
            consumer_profile_merge_model="gpt-5.3-codex",
            consumer_profile_window_max_chars=60000,
        ),
        policies=PolicyConfig(
            require_confirmation_for_inferred_rule_promotion=True,
            include_failed_attempts_in_recent_only_if_state_changes=True,
            ignore_agent_reasoning_for_durable_memory=True,
            explicit_promotion_has_priority=True,
        ),
    )


def detect_operating_system() -> str:
    system = platform.system().lower()
    if "windows" in system:
        return "windows"
    if "darwin" in system:
        return "macos"
    if "linux" in system:
        return "linux"
    return system or "unknown"


def load_product_config(config_path: Path | str) -> ProductConfig:
    config_path = Path(config_path)
    try:
        payload = json.loads(config_path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError as exc:
        raise ProductConfigError(f"Missing product config: {config_path}") from exc
    except json.JSONDecodeError as exc:
        raise ProductConfigError(f"Invalid product config JSON: {config_path}") from exc
    return parse_product_config(payload)


def parse_product_config(payload: dict[str, Any]) -> ProductConfig:
    if int(payload.get("product_schema_version", -1)) != PRODUCT_SCHEMA_VERSION:
        raise ProductConfigError(
            f"Unsupported product_schema_version: {payload.get('product_schema_version')}"
        )

    environment_payload = dict(payload.get("environment", {}))
    agent_payload = dict(payload.get("agent_platform", {}))
    markdown_payload = dict(payload.get("markdown_output", {}))
    scheduler_payload = dict(payload.get("scheduler", {}))
    policies_payload = dict(payload.get("policies", {}))
    project_routing_payload = dict(payload.get("project_routing", {}))
    memory_extraction_payload = dict(payload.get("memory_extraction", {}))

    log_sources = tuple(
        LogSourceConfig(
            adapter=str(item["adapter"]),
            root_alias=str(item["root_alias"]),
            absolute_path=str(item["absolute_path"]),
            include_glob=str(item.get("include_glob", "**/*.jsonl")),
        )
        for item in payload.get("log_sources", [])
    )
    project_sources = tuple(
        ProjectSourceConfig(
            adapter=str(item["adapter"]),
            project_root=str(item["project_root"]),
            include_untracked=bool(item.get("include_untracked", True)),
        )
        for item in payload.get("project_sources", [])
    )
    project_aliases = tuple(
        ProjectAliasConfig(
            slug=slugify(str(item["slug"])),
            aliases=tuple(str(alias) for alias in item.get("aliases", [])),
        )
        for item in payload.get("project_aliases", [])
    )

    config = ProductConfig(
        schema_version=int(payload.get("schema_version", 1)),
        product_schema_version=int(payload["product_schema_version"]),
        environment=EnvironmentConfig(
            operating_system=str(environment_payload["operating_system"]),
            editor=str(environment_payload["editor"]),
            repo_root=str(environment_payload["repo_root"]),
        ),
        agent_platform=AgentPlatformConfig(
            platform=str(agent_payload["platform"]),
            bootstrap_renderer=str(agent_payload["bootstrap_renderer"]),
            bootstrap_target_path=str(agent_payload["bootstrap_target_path"]),
        ),
        markdown_output=MarkdownOutputConfig(
            mode=str(markdown_payload["mode"]),
            root_dir=str(markdown_payload["root_dir"]),
            enable_frontmatter=bool(markdown_payload["enable_frontmatter"]),
            enable_tags=bool(markdown_payload["enable_tags"]),
            enable_wikilinks=bool(markdown_payload["enable_wikilinks"]),
        ),
        log_sources=log_sources,
        project_sources=project_sources,
        project_aliases=project_aliases,
        project_routing=parse_project_routing_config(project_routing_payload),
        memory_extraction=parse_memory_extraction_config(memory_extraction_payload),
        scheduler=SchedulerConfig(
            mode=str(scheduler_payload["mode"]),
            scan_on_startup=bool(scheduler_payload["scan_on_startup"]),
            tick_seconds=int(scheduler_payload["tick_seconds"]),
            project_delta_enabled=bool(scheduler_payload["project_delta_enabled"]),
            log_delta_enabled=bool(scheduler_payload["log_delta_enabled"]),
            allowed_weekdays=tuple(
                normalize_weekday(str(day))
                for day in scheduler_payload.get(
                    "allowed_weekdays",
                    ["monday", "tuesday", "wednesday", "thursday", "friday"],
                )
            ),
            run_hour_local=int(scheduler_payload.get("run_hour_local", 9)),
            run_minute_local=int(scheduler_payload.get("run_minute_local", 0)),
            ingest_interval_hours=int(scheduler_payload.get("ingest_interval_hours", 24)),
            lint_interval_hours=int(scheduler_payload.get("lint_interval_hours", 24)),
            require_log_update_for_ingest=bool(scheduler_payload.get("require_log_update_for_ingest", True)),
            lint_autofix_enabled=bool(scheduler_payload.get("lint_autofix_enabled", False)),
            lint_autofix_max_rounds=int(scheduler_payload.get("lint_autofix_max_rounds", 1)),
            consumer_profile_extraction_model=str(scheduler_payload.get("consumer_profile_extraction_model", "gpt-4o-mini")),
            consumer_profile_merge_model=str(scheduler_payload.get("consumer_profile_merge_model", "gpt-5.3-codex")),
            consumer_profile_window_max_chars=int(scheduler_payload.get("consumer_profile_window_max_chars", 60000)),
        ),
        policies=PolicyConfig(
            require_confirmation_for_inferred_rule_promotion=bool(
                policies_payload["require_confirmation_for_inferred_rule_promotion"]
            ),
            include_failed_attempts_in_recent_only_if_state_changes=bool(
                policies_payload["include_failed_attempts_in_recent_only_if_state_changes"]
            ),
            ignore_agent_reasoning_for_durable_memory=bool(
                policies_payload["ignore_agent_reasoning_for_durable_memory"]
            ),
            explicit_promotion_has_priority=bool(policies_payload["explicit_promotion_has_priority"]),
        ),
    )
    validate_product_config(config)
    return config


def validate_product_config(config: ProductConfig) -> None:
    if config.markdown_output.mode not in MARKDOWN_RENDERERS:
        raise ProductConfigError(f"Unsupported markdown mode: {config.markdown_output.mode}")
    if config.agent_platform.bootstrap_renderer not in BOOTSTRAP_RENDERERS:
        raise ProductConfigError(
            f"Unsupported bootstrap renderer: {config.agent_platform.bootstrap_renderer}"
        )
    if not config.log_sources:
        raise ProductConfigError("Product config must define at least one log source")
    if not config.project_sources:
        raise ProductConfigError("Product config must define at least one project source")
    for source in config.log_sources:
        if source.adapter not in LOG_ADAPTERS:
            raise ProductConfigError(f"Unsupported log adapter: {source.adapter}")
    for source in config.project_sources:
        if source.adapter not in PROJECT_DELTA_ADAPTERS:
            raise ProductConfigError(f"Unsupported project delta adapter: {source.adapter}")
    for alias in config.project_aliases:
        if not alias.slug:
            raise ProductConfigError("Project alias slug must be non-empty")
        if not alias.aliases:
            raise ProductConfigError(f"Project alias {alias.slug} must define at least one alias")
    if config.scheduler.mode not in {"manual", "interval", "cron_like"}:
        raise ProductConfigError(f"Unsupported scheduler mode: {config.scheduler.mode}")
    if config.scheduler.tick_seconds <= 0:
        raise ProductConfigError("scheduler.tick_seconds must be positive")
    if not config.scheduler.allowed_weekdays:
        raise ProductConfigError("scheduler.allowed_weekdays must define at least one day")
    for day in config.scheduler.allowed_weekdays:
        normalize_weekday(day)
    if not 0 <= config.scheduler.run_hour_local <= 23:
        raise ProductConfigError("scheduler.run_hour_local must be between 0 and 23")
    if not 0 <= config.scheduler.run_minute_local <= 59:
        raise ProductConfigError("scheduler.run_minute_local must be between 0 and 59")
    if config.scheduler.ingest_interval_hours <= 0:
        raise ProductConfigError("scheduler.ingest_interval_hours must be positive")
    if config.scheduler.lint_interval_hours <= 0:
        raise ProductConfigError("scheduler.lint_interval_hours must be positive")
    if config.scheduler.lint_autofix_max_rounds <= 0:
        raise ProductConfigError("scheduler.lint_autofix_max_rounds must be positive")
    if config.project_routing.min_confidence not in {"high", "medium", "low"}:
        raise ProductConfigError(f"Unsupported project routing min_confidence: {config.project_routing.min_confidence}")
    if config.project_routing.max_sources_per_run <= 0:
        raise ProductConfigError("project_routing.max_sources_per_run must be positive")
    if config.project_routing.max_sample_records_per_source <= 0:
        raise ProductConfigError("project_routing.max_sample_records_per_source must be positive")
    if config.memory_extraction.window_record_limit <= 0:
        raise ProductConfigError("memory_extraction.window_record_limit must be positive")
    if config.memory_extraction.window_overlap_records < 0:
        raise ProductConfigError("memory_extraction.window_overlap_records cannot be negative")
    if config.memory_extraction.window_overlap_records >= config.memory_extraction.window_record_limit:
        raise ProductConfigError("memory_extraction.window_overlap_records must be smaller than window_record_limit")
    if config.memory_extraction.max_window_chars <= 0:
        raise ProductConfigError("memory_extraction.max_window_chars must be positive")
    if config.memory_extraction.max_windows_per_run <= 0:
        raise ProductConfigError("memory_extraction.max_windows_per_run must be positive")
    if config.memory_extraction.max_candidates_per_window <= 0:
        raise ProductConfigError("memory_extraction.max_candidates_per_window must be positive")


def parse_project_routing_config(payload: dict[str, Any]) -> ProjectRoutingConfig:
    if not payload:
        return default_project_routing_config()
    provider_payload = dict(payload.get("provider", {}))
    provider = RoutingProviderConfig(
        provider_type=str(provider_payload.get("type", "openai")),
        api_key_env=str(provider_payload.get("api_key_env", "OPENAI_API_KEY")),
        base_url_env=str(provider_payload.get("base_url_env", "WIKIMEMORY_OPENAI_BASE_URL")),
        model_env=str(provider_payload.get("model_env", "WIKIMEMORY_OPENAI_MODEL")),
        default_model=str(provider_payload.get("default_model", "gpt-5.4-mini")),
        temperature=float(provider_payload.get("temperature", 0)),
    )
    if provider.provider_type != "openai":
        raise ProductConfigError(f"Unsupported project routing provider: {provider.provider_type}")
    return ProjectRoutingConfig(
        enabled=bool(payload.get("enabled", False)),
        unresolved_project=slugify(str(payload.get("unresolved_project", "projects"))),
        min_confidence=str(payload.get("min_confidence", "high")),
        max_sources_per_run=int(payload.get("max_sources_per_run", 200)),
        max_sample_records_per_source=int(payload.get("max_sample_records_per_source", 8)),
        provider=provider,
    )


def parse_memory_extraction_config(payload: dict[str, Any]) -> MemoryExtractionConfig:
    if not payload:
        return default_memory_extraction_config(enabled=False)
    provider_payload = dict(payload.get("provider", {}))
    provider = RoutingProviderConfig(
        provider_type=str(provider_payload.get("type", "openai")),
        api_key_env=str(provider_payload.get("api_key_env", "OPENAI_API_KEY")),
        base_url_env=str(provider_payload.get("base_url_env", "WIKIMEMORY_OPENAI_BASE_URL")),
        model_env=str(provider_payload.get("model_env", "WIKIMEMORY_OPENAI_MODEL")),
        default_model=str(provider_payload.get("default_model", "gpt-5.4-mini")),
        temperature=float(provider_payload.get("temperature", 0)),
    )
    if provider.provider_type != "openai":
        raise ProductConfigError(f"Unsupported memory extraction provider: {provider.provider_type}")
    return MemoryExtractionConfig(
        enabled=bool(payload.get("enabled", False)),
        fallback_to_deterministic=bool(payload.get("fallback_to_deterministic", True)),
        window_record_limit=int(payload.get("window_record_limit", 8)),
        window_overlap_records=int(payload.get("window_overlap_records", 2)),
        max_window_chars=int(payload.get("max_window_chars", 6000)),
        max_windows_per_run=int(payload.get("max_windows_per_run", 1000)),
        max_candidates_per_window=int(payload.get("max_candidates_per_window", 12)),
        provider=provider,
    )


def default_memory_extraction_config(enabled: bool = False) -> MemoryExtractionConfig:
    return MemoryExtractionConfig(
        enabled=enabled,
        fallback_to_deterministic=True,
        window_record_limit=8,
        window_overlap_records=2,
        max_window_chars=6000,
        max_windows_per_run=1000,
        max_candidates_per_window=12,
        provider=RoutingProviderConfig(
            provider_type="openai",
            api_key_env="OPENAI_API_KEY",
            base_url_env="WIKIMEMORY_OPENAI_BASE_URL",
            model_env="WIKIMEMORY_OPENAI_MODEL",
            default_model="gpt-5.4-mini",
            temperature=0,
        ),
    )


def default_project_routing_config() -> ProjectRoutingConfig:
    return ProjectRoutingConfig(
        enabled=False,
        unresolved_project="projects",
        min_confidence="high",
        max_sources_per_run=200,
        max_sample_records_per_source=8,
        provider=RoutingProviderConfig(
            provider_type="openai",
            api_key_env="OPENAI_API_KEY",
            base_url_env="WIKIMEMORY_OPENAI_BASE_URL",
            model_env="WIKIMEMORY_OPENAI_MODEL",
            default_model="gpt-5.4-mini",
            temperature=0,
        ),
    )


def slugify(value: str) -> str:
    slug = "".join(char.lower() if char.isalnum() else "-" for char in value).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug or "project"


def normalize_weekday(value: str) -> str:
    normalized = value.strip().lower()
    aliases = {
        "mon": "monday",
        "tue": "tuesday",
        "tues": "tuesday",
        "wed": "wednesday",
        "thu": "thursday",
        "thur": "thursday",
        "thurs": "thursday",
        "fri": "friday",
        "sat": "saturday",
        "sun": "sunday",
    }
    normalized = aliases.get(normalized, normalized)
    if normalized not in {"monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"}:
        raise ProductConfigError(f"Unsupported scheduler weekday: {value}")
    return normalized
