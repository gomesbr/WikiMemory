from __future__ import annotations

import argparse
import json
from pathlib import Path

from .agent_bootstrap import AgentBootstrapResult, run_agent_bootstrap
from .audit import AuditResult, run_audit
from .bootstrap import BootstrapResult, run_bootstrap
from .classification import ClassificationResult, run_classification
from .consumer_profile import ConsumerProfileResult, run_consumer_profile
from .discovery import DiscoveryResult, run_discovery
from .env_loader import load_project_env
from .extraction import ExtractionResult, run_extraction
from .full_load import FullLoadResult, run_full_load
from .ingest import IngestResult, run_ingest
from .memory_generation import MemoryResult, run_memory_generation
from .memory_inspection import MemoryInspectionResult, run_memory_inspection
from .memory_lint import MemoryLintResult, run_memory_lint
from .memory_review import MemoryReviewResult, run_memory_review
from .memory_refresh import MemoryRefreshResult, run_memory_refresh
from .memory_v2 import MemoryV2Result, run_memory_v2
from .normalization import NormalizationResult, run_normalization
from .onboarding import OnboardingReport, run_onboarding
from .product_config import load_product_config
from .refresh import RefreshResult, run_refresh
from .scheduler import (
    SchedulerPlanResult,
    last_refresh_checkpoint_finished_at,
    last_successful_refresh_finished_at,
    latest_active_log_update,
    load_json,
    parse_iso,
    run_scheduler_plan,
)
from .segmentation import SegmentationResult, run_segmentation
from .wiki import WikiResult, run_wiki


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SessionMemory discovery tools")
    subparsers = parser.add_subparsers(dest="command", required=True)

    discover_parser = subparsers.add_parser(
        "discover",
        help="Discover and index external Codex session logs.",
    )
    discover_parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/source_roots.json"),
        help="Path to source root configuration JSON.",
    )
    discover_parser.add_argument(
        "--state-dir",
        type=Path,
        default=Path("state"),
        help="Directory where derived state files are written.",
    )
    discover_parser.add_argument(
        "--json",
        action="store_true",
        help="Print the final run report as JSON.",
    )

    normalize_parser = subparsers.add_parser(
        "normalize",
        help="Normalize committed Codex session logs into canonical artifacts.",
    )
    normalize_parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/source_roots.json"),
        help="Path to source root configuration JSON.",
    )
    normalize_parser.add_argument(
        "--state-dir",
        type=Path,
        default=Path("state"),
        help="Directory containing discovery state and normalization state.",
    )
    normalize_parser.add_argument(
        "--schema",
        type=Path,
        default=Path("schema/normalization_catalog.json"),
        help="Path to the normalization schema catalog JSON.",
    )
    normalize_parser.add_argument(
        "--normalized-dir",
        type=Path,
        default=Path("normalized"),
        help="Directory where normalized source artifacts are written.",
    )
    normalize_parser.add_argument(
        "--audits-dir",
        type=Path,
        default=Path("audits"),
        help="Directory where audit logs are written.",
    )
    normalize_parser.add_argument(
        "--json",
        action="store_true",
        help="Print the final run report as JSON.",
    )

    segment_parser = subparsers.add_parser(
        "segment",
        help="Reconstruct session flow and emit non-overlapping normalized segments.",
    )
    segment_parser.add_argument(
        "--state-dir",
        type=Path,
        default=Path("state"),
        help="Directory containing normalization state and segmentation state.",
    )
    segment_parser.add_argument(
        "--normalized-dir",
        type=Path,
        default=Path("normalized"),
        help="Directory containing normalized source artifacts.",
    )
    segment_parser.add_argument(
        "--segmented-dir",
        type=Path,
        default=Path("segmented"),
        help="Directory where segmented source artifacts are written.",
    )
    segment_parser.add_argument(
        "--source-id",
        dest="source_ids",
        action="append",
        help="Optional source_id to segment. Repeat to segment multiple explicit sources.",
    )
    segment_parser.add_argument(
        "--json",
        action="store_true",
        help="Print the final run report as JSON.",
    )

    classify_parser = subparsers.add_parser(
        "classify",
        help="Classify segmented source artifacts into domain labels.",
    )
    classify_parser.add_argument(
        "--taxonomy",
        type=Path,
        default=Path("config/classification_taxonomy.json"),
        help="Path to the classification taxonomy JSON.",
    )
    classify_parser.add_argument(
        "--state-dir",
        type=Path,
        default=Path("state"),
        help="Directory containing segmentation state and classification state.",
    )
    classify_parser.add_argument(
        "--normalized-dir",
        type=Path,
        default=Path("normalized"),
        help="Directory containing normalized source artifacts.",
    )
    classify_parser.add_argument(
        "--segmented-dir",
        type=Path,
        default=Path("segmented"),
        help="Directory containing segmented source artifacts.",
    )
    classify_parser.add_argument(
        "--classified-dir",
        type=Path,
        default=Path("classified"),
        help="Directory where classified source artifacts are written.",
    )
    classify_parser.add_argument(
        "--audits-dir",
        type=Path,
        default=Path("audits"),
        help="Directory where audit logs are written.",
    )
    classify_parser.add_argument(
        "--source-roots-config",
        type=Path,
        default=Path("config/source_roots.json"),
        help="Path to the source roots configuration JSON for optional raw-event hydration.",
    )
    classify_parser.add_argument(
        "--source-id",
        dest="source_ids",
        action="append",
        help="Optional source_id to classify. Repeat to classify multiple explicit sources.",
    )
    classify_parser.add_argument(
        "--json",
        action="store_true",
        help="Print the final run report as JSON.",
    )

    extract_parser = subparsers.add_parser(
        "extract",
        help="Extract structured knowledge items from classified segments.",
    )
    extract_parser.add_argument(
        "--rules",
        type=Path,
        default=Path("config/extraction_rules.json"),
        help="Path to the extraction rules JSON.",
    )
    extract_parser.add_argument(
        "--state-dir",
        type=Path,
        default=Path("state"),
        help="Directory containing classification state and extraction state.",
    )
    extract_parser.add_argument(
        "--normalized-dir",
        type=Path,
        default=Path("normalized"),
        help="Directory containing normalized source artifacts.",
    )
    extract_parser.add_argument(
        "--classified-dir",
        type=Path,
        default=Path("classified"),
        help="Directory containing classified source artifacts.",
    )
    extract_parser.add_argument(
        "--extracted-dir",
        type=Path,
        default=Path("extracted"),
        help="Directory where extracted knowledge artifacts are written.",
    )
    extract_parser.add_argument(
        "--audits-dir",
        type=Path,
        default=Path("audits"),
        help="Directory where audit logs are written.",
    )
    extract_parser.add_argument(
        "--source-roots-config",
        type=Path,
        default=Path("config/source_roots.json"),
        help="Path to the source roots configuration JSON for optional raw-event hydration.",
    )
    extract_parser.add_argument(
        "--source-id",
        dest="source_ids",
        action="append",
        help="Optional source_id to extract. Repeat to extract multiple explicit sources.",
    )
    extract_parser.add_argument(
        "--json",
        action="store_true",
        help="Print the final run report as JSON.",
    )

    wiki_parser = subparsers.add_parser(
        "wiki",
        help="Generate hybrid wiki pages from extracted knowledge items.",
    )
    wiki_parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/wiki_config.json"),
        help="Path to the wiki generation config JSON.",
    )
    wiki_parser.add_argument(
        "--state-dir",
        type=Path,
        default=Path("state"),
        help="Directory containing extraction state and wiki state.",
    )
    wiki_parser.add_argument(
        "--extracted-dir",
        type=Path,
        default=Path("extracted"),
        help="Directory containing extracted knowledge artifacts.",
    )
    wiki_parser.add_argument(
        "--wiki-dir",
        type=Path,
        default=Path("wiki"),
        help="Directory where rendered wiki pages are written.",
    )
    wiki_parser.add_argument(
        "--audits-dir",
        type=Path,
        default=Path("audits"),
        help="Directory where wiki audit logs are written.",
    )
    wiki_parser.add_argument(
        "--source-id",
        dest="source_ids",
        action="append",
        help="Optional source_id to rebuild affected wiki pages from. Repeat to target multiple sources.",
    )
    wiki_parser.add_argument(
        "--json",
        action="store_true",
        help="Print the final run report as JSON.",
    )

    bootstrap_parser = subparsers.add_parser(
        "bootstrap",
        help="Generate compact agent bootstrap memory from extracted items and wiki manifests.",
    )
    bootstrap_parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/bootstrap_config.json"),
        help="Path to the bootstrap generation config JSON.",
    )
    bootstrap_parser.add_argument(
        "--state-dir",
        type=Path,
        default=Path("state"),
        help="Directory containing extraction state, wiki state, and bootstrap state.",
    )
    bootstrap_parser.add_argument(
        "--extracted-dir",
        type=Path,
        default=Path("extracted"),
        help="Directory containing extracted knowledge artifacts.",
    )
    bootstrap_parser.add_argument(
        "--wiki-dir",
        type=Path,
        default=Path("wiki"),
        help="Directory containing wiki manifests.",
    )
    bootstrap_parser.add_argument(
        "--bootstrap-dir",
        type=Path,
        default=Path("bootstrap"),
        help="Directory where bootstrap artifacts are written.",
    )
    bootstrap_parser.add_argument(
        "--audits-dir",
        type=Path,
        default=Path("audits"),
        help="Directory where bootstrap audit logs are written.",
    )
    bootstrap_parser.add_argument(
        "--source-id",
        dest="source_ids",
        action="append",
        help="Optional source_id to rebuild affected bootstrap domains from. Repeat to target multiple sources.",
    )
    bootstrap_parser.add_argument(
        "--json",
        action="store_true",
        help="Print the final run report as JSON.",
    )

    audit_parser = subparsers.add_parser(
        "audit",
        help="Run deterministic validation and drift audits over extracted, wiki, and bootstrap artifacts.",
    )
    audit_parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/audit_config.json"),
        help="Path to the audit config JSON.",
    )
    audit_parser.add_argument(
        "--state-dir",
        type=Path,
        default=Path("state"),
        help="Directory containing extraction, wiki, bootstrap, and audit state.",
    )
    audit_parser.add_argument(
        "--extracted-dir",
        type=Path,
        default=Path("extracted"),
        help="Directory containing extracted knowledge artifacts.",
    )
    audit_parser.add_argument(
        "--wiki-dir",
        type=Path,
        default=Path("wiki"),
        help="Directory containing wiki manifests.",
    )
    audit_parser.add_argument(
        "--bootstrap-dir",
        type=Path,
        default=Path("bootstrap"),
        help="Directory containing bootstrap manifests.",
    )
    audit_parser.add_argument(
        "--audits-dir",
        type=Path,
        default=Path("audits"),
        help="Directory where audit findings are written.",
    )
    audit_parser.add_argument(
        "--source-id",
        dest="source_ids",
        action="append",
        help="Optional source_id to recompute findings for. Repeat to target multiple sources.",
    )
    audit_parser.add_argument(
        "--json",
        action="store_true",
        help="Print the final run report as JSON.",
    )

    refresh_parser = subparsers.add_parser(
        "refresh",
        help="Run the full daily incremental refresh orchestration across phases 1-8.",
    )
    refresh_parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/refresh_config.json"),
        help="Path to the refresh orchestration config JSON.",
    )
    refresh_parser.add_argument(
        "--state-dir",
        type=Path,
        default=Path("state"),
        help="Directory containing phase state and refresh state.",
    )
    refresh_parser.add_argument(
        "--audits-dir",
        type=Path,
        default=Path("audits"),
        help="Directory where refresh notices are written.",
    )
    refresh_parser.add_argument(
        "--source-id",
        dest="source_ids",
        action="append",
        help="Optional source_id to manually scope downstream refresh phases. Repeat to target multiple sources.",
    )
    refresh_parser.add_argument(
        "--json",
        action="store_true",
        help="Print the final run report as JSON.",
    )

    full_load_parser = subparsers.add_parser(
        "full-load",
        help="Run the full phase-by-phase corpus load with strict gates and derived-disk budget checks.",
    )
    full_load_parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/full_load_config.json"),
        help="Path to the full-load orchestration config JSON.",
    )
    full_load_parser.add_argument(
        "--state-dir",
        type=Path,
        default=Path("state"),
        help="Directory containing phase state and full-load state.",
    )
    full_load_parser.add_argument(
        "--audits-dir",
        type=Path,
        default=Path("audits"),
        help="Directory where full-load notices and issue bundles are written.",
    )
    full_load_parser.add_argument(
        "--json",
        action="store_true",
        help="Print the final run report as JSON.",
    )

    onboard_parser = subparsers.add_parser(
        "onboard",
        help="Detect environment defaults and write a draft product config for the redesigned memory platform.",
    )
    onboard_parser.add_argument(
        "--project-root",
        type=Path,
        default=Path("."),
        help="Project root to inspect for environment detection.",
    )
    onboard_parser.add_argument(
        "--config-out",
        type=Path,
        default=Path("config/product_config.json"),
        help="Path where the recommended product config should be written.",
    )
    onboard_parser.add_argument(
        "--brief-out",
        type=Path,
        default=Path("config/agent_onboarding_brief.generated.md"),
        help="Path where the agent-facing onboarding brief should be written.",
    )
    onboard_parser.add_argument(
        "--json",
        action="store_true",
        help="Print the onboarding report as JSON.",
    )

    ingest_parser = subparsers.add_parser(
        "ingest",
        help="Build canonical evidence records from normalized logs and project deltas.",
    )
    ingest_parser.add_argument(
        "--product-config",
        type=Path,
        default=Path("config/product_config.json"),
        help="Path to unified product configuration JSON.",
    )
    ingest_parser.add_argument(
        "--state-dir",
        type=Path,
        default=Path("state"),
        help="Directory where ingest state and run logs are written.",
    )
    ingest_parser.add_argument(
        "--normalized-dir",
        type=Path,
        default=Path("normalized"),
        help="Directory containing normalized source artifacts.",
    )
    ingest_parser.add_argument(
        "--evidence-dir",
        type=Path,
        default=Path("evidence"),
        help="Directory where canonical evidence artifacts are written.",
    )
    ingest_parser.add_argument(
        "--audits-dir",
        type=Path,
        default=Path("audits"),
        help="Directory where ingest notices are written.",
    )
    ingest_parser.add_argument(
        "--source-id",
        dest="source_ids",
        action="append",
        help="Optional source_id to ingest from normalized logs. Repeat to target multiple sources.",
    )
    ingest_parser.add_argument(
        "--json",
        action="store_true",
        help="Print the final run report as JSON.",
    )

    memory_parser = subparsers.add_parser(
        "memory",
        help="Generate compact operational memory files from canonical evidence records.",
    )
    memory_parser.add_argument(
        "--product-config",
        type=Path,
        default=Path("config/product_config.json"),
        help="Path to unified product configuration JSON.",
    )
    memory_parser.add_argument(
        "--state-dir",
        type=Path,
        default=Path("state"),
        help="Directory where memory generation state and run logs are written.",
    )
    memory_parser.add_argument(
        "--evidence-dir",
        type=Path,
        default=Path("evidence"),
        help="Directory containing canonical evidence artifacts.",
    )
    memory_parser.add_argument(
        "--memory-dir",
        type=Path,
        default=Path("memory"),
        help="Directory where compact memory files are written.",
    )
    memory_parser.add_argument(
        "--audits-dir",
        type=Path,
        default=Path("audits"),
        help="Directory where memory generation notices are written.",
    )
    memory_parser.add_argument(
        "--project",
        dest="projects",
        action="append",
        help="Optional project slug to render. Repeat to target multiple projects.",
    )
    memory_parser.add_argument(
        "--json",
        action="store_true",
        help="Print the final run report as JSON.",
    )

    memory_inspect_parser = subparsers.add_parser(
        "memory-inspect",
        help="Inspect generated memory state, rules, freshness, health, and continuation artifacts.",
    )
    memory_inspect_parser.add_argument(
        "--action",
        required=True,
        choices=("active-rules", "project-rules", "why-rule", "recent-changes", "freshness", "health", "continuations"),
        help="Inspection action to run.",
    )
    memory_inspect_parser.add_argument(
        "--memory-dir",
        type=Path,
        default=Path("memory"),
        help="Directory containing generated memory artifacts.",
    )
    memory_inspect_parser.add_argument(
        "--state-dir",
        type=Path,
        default=Path("state"),
        help="Directory containing memory state files.",
    )
    memory_inspect_parser.add_argument(
        "--project",
        type=str,
        help="Optional project slug for project-scoped inspection actions.",
    )
    memory_inspect_parser.add_argument(
        "--rule-query",
        type=str,
        help="Rule substring to explain for why-rule.",
    )
    memory_inspect_parser.add_argument(
        "--json",
        action="store_true",
        help="Print the inspection payload as JSON.",
    )

    memory_v2_parser = subparsers.add_parser(
        "memory-v2",
        help="Run the LLM-first V2 memory pipeline from daily Codex chat markdown exports.",
    )
    memory_v2_parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path("experimental_exports/codex_chat_by_day"),
        help="Directory containing daily *-codex-chat.md files.",
    )
    memory_v2_parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("memory_v2_pilot"),
        help="Directory where V2 pilot memory output is written.",
    )
    memory_v2_parser.add_argument(
        "--state-dir",
        type=Path,
        default=Path("state"),
        help="Directory where memory-v2 run logs are written.",
    )
    memory_v2_parser.add_argument(
        "--project-root-dir",
        type=Path,
        default=None,
        help="Directory containing project repositories used for README/tree context. Defaults to the parent of SessionMemory.",
    )
    memory_v2_parser.add_argument(
        "--day",
        dest="days",
        action="append",
        help="Daily export date to process, e.g. 2026-03-13. Repeat for multiple days.",
    )
    memory_v2_parser.add_argument(
        "--all-days",
        action="store_true",
        help="Process all daily chat exports in the input directory.",
    )
    memory_v2_parser.add_argument(
        "--model",
        default=None,
        help="OpenAI model id. Defaults to SESSIONMEMORY_MEMORY_V2_MODEL or gpt-5.3-codex.",
    )
    memory_v2_parser.add_argument(
        "--json",
        action="store_true",
        help="Print the final run report as JSON.",
    )

    agent_bootstrap_parser = subparsers.add_parser(
        "agent-bootstrap",
        help="Generate the configured agent bootstrap file from compact memory artifacts.",
    )
    agent_bootstrap_parser.add_argument(
        "--product-config",
        type=Path,
        default=Path("config/product_config.json"),
        help="Path to unified product configuration JSON.",
    )
    agent_bootstrap_parser.add_argument(
        "--state-dir",
        type=Path,
        default=Path("state"),
        help="Directory where agent-bootstrap state and run logs are written.",
    )
    agent_bootstrap_parser.add_argument(
        "--memory-dir",
        type=Path,
        default=Path("memory"),
        help="Directory containing compact memory files.",
    )
    agent_bootstrap_parser.add_argument(
        "--audits-dir",
        type=Path,
        default=Path("audits"),
        help="Directory where agent-bootstrap notices are written.",
    )
    agent_bootstrap_parser.add_argument(
        "--output-path",
        type=Path,
        default=None,
        help="Optional output path override. Defaults to product_config agent_platform.bootstrap_target_path.",
    )
    agent_bootstrap_parser.add_argument(
        "--project",
        dest="projects",
        action="append",
        help="Optional project slug to include. Repeat to target multiple projects.",
    )
    agent_bootstrap_parser.add_argument(
        "--json",
        action="store_true",
        help="Print the final run report as JSON.",
    )

    memory_lint_parser = subparsers.add_parser(
        "memory-lint",
        help="Run LLM-backed lint checks over compact memory and agent bootstrap artifacts.",
    )
    memory_lint_parser.add_argument(
        "--product-config",
        type=Path,
        default=Path("config/product_config.json"),
        help="Path to unified product configuration JSON.",
    )
    memory_lint_parser.add_argument(
        "--state-dir",
        type=Path,
        default=Path("state"),
        help="Directory where memory-lint state and run logs are written.",
    )
    memory_lint_parser.add_argument(
        "--memory-dir",
        type=Path,
        default=Path("memory"),
        help="Directory containing compact memory files.",
    )
    memory_lint_parser.add_argument(
        "--audits-dir",
        type=Path,
        default=Path("audits"),
        help="Directory where memory-lint findings are written.",
    )
    memory_lint_parser.add_argument(
        "--bootstrap-path",
        type=Path,
        default=None,
        help="Optional agent bootstrap path override.",
    )
    memory_lint_parser.add_argument(
        "--fix",
        action="store_true",
        help="Apply canonical item fixes and rerender memory before the final lint pass.",
    )
    memory_lint_parser.add_argument(
        "--max-fix-rounds",
        type=int,
        default=1,
        help="Maximum autofix+rerlint rounds when --fix is enabled.",
    )
    memory_lint_parser.add_argument(
        "--model",
        default=None,
        help="OpenAI model id. Defaults to SESSIONMEMORY_MEMORY_LINT_MODEL or the memory-v2 default.",
    )
    memory_lint_parser.add_argument(
        "--json",
        action="store_true",
        help="Print the final run report as JSON.",
    )

    memory_review_parser = subparsers.add_parser(
        "memory-review",
        help="List or record review decisions for inferred durable memory candidates.",
    )
    memory_review_parser.add_argument(
        "--memory-dir",
        type=Path,
        default=Path("memory"),
        help="Directory containing compact memory files.",
    )
    memory_review_parser.add_argument(
        "--state-dir",
        type=Path,
        default=Path("state"),
        help="Directory where memory-review decisions and run logs are written.",
    )
    memory_review_parser.add_argument(
        "--audits-dir",
        type=Path,
        default=Path("audits"),
        help="Directory where review item snapshots are written.",
    )
    memory_review_parser.add_argument(
        "--approve",
        action="append",
        default=None,
        help="Memory item id to approve. Repeat for multiple items.",
    )
    memory_review_parser.add_argument(
        "--reject",
        action="append",
        default=None,
        help="Memory item id to reject. Repeat for multiple items.",
    )
    memory_review_parser.add_argument(
        "--json",
        action="store_true",
        help="Print the final run report as JSON.",
    )

    consumer_profile_parser = subparsers.add_parser(
        "consumer-profile",
        help="Build a review-first consumer working profile from evidence-backed user conversation snippets.",
    )
    consumer_profile_parser.add_argument(
        "--evidence-dir",
        type=Path,
        default=Path("evidence"),
        help="Directory containing evidence artifacts.",
    )
    consumer_profile_parser.add_argument(
        "--memory-dir",
        type=Path,
        default=Path("memory"),
        help="Directory where the rendered consumer profile should be written.",
    )
    consumer_profile_parser.add_argument(
        "--state-dir",
        type=Path,
        default=Path("state"),
        help="Directory where consumer-profile state and run logs are written.",
    )
    consumer_profile_parser.add_argument(
        "--audits-dir",
        type=Path,
        default=Path("audits"),
        help="Directory where consumer-profile candidate artifacts are written.",
    )
    consumer_profile_parser.add_argument(
        "--policy",
        type=Path,
        default=Path("config/consumer_profile_policy.json"),
        help="Path to the consumer-profile policy JSON.",
    )
    consumer_profile_parser.add_argument(
        "--model",
        default="gpt-5.3-codex",
        help="Fallback model id for consumer-profile phases when phase-specific models are not provided.",
    )
    consumer_profile_parser.add_argument(
        "--extraction-model",
        default="gpt-4o-mini",
        help="Model id for extraction windows.",
    )
    consumer_profile_parser.add_argument(
        "--merge-model",
        default="gpt-5.3-codex",
        help="Model id for final profile merge.",
    )
    consumer_profile_parser.add_argument(
        "--window-max-chars",
        type=int,
        default=None,
        help="Maximum snippet-text characters per extraction window. Higher values reduce API call count.",
    )
    consumer_profile_parser.add_argument(
        "--json",
        action="store_true",
        help="Print the final run report as JSON.",
    )

    memory_refresh_parser = subparsers.add_parser(
        "memory-refresh",
        help="Run the redesigned memory pipeline: discover, normalize, ingest, memory, agent-bootstrap, memory-lint.",
    )
    memory_refresh_parser.add_argument(
        "--source-config",
        type=Path,
        default=Path("config/source_roots.json"),
        help="Path to source root configuration JSON.",
    )
    memory_refresh_parser.add_argument(
        "--product-config",
        type=Path,
        default=Path("config/product_config.json"),
        help="Path to unified product configuration JSON.",
    )
    memory_refresh_parser.add_argument(
        "--schema",
        type=Path,
        default=Path("schema/normalization_catalog.json"),
        help="Path to the normalization schema catalog JSON.",
    )
    memory_refresh_parser.add_argument(
        "--state-dir",
        type=Path,
        default=Path("state"),
        help="Directory where state and run logs are written.",
    )
    memory_refresh_parser.add_argument(
        "--normalized-dir",
        type=Path,
        default=Path("normalized"),
        help="Directory where normalized artifacts are written.",
    )
    memory_refresh_parser.add_argument(
        "--evidence-dir",
        type=Path,
        default=Path("evidence"),
        help="Directory where evidence artifacts are written.",
    )
    memory_refresh_parser.add_argument(
        "--memory-dir",
        type=Path,
        default=Path("memory"),
        help="Directory where compact memory artifacts are written.",
    )
    memory_refresh_parser.add_argument(
        "--audits-dir",
        type=Path,
        default=Path("audits"),
        help="Directory where notices and lint findings are written.",
    )
    memory_refresh_parser.add_argument(
        "--bootstrap-output-path",
        type=Path,
        default=None,
        help="Optional agent bootstrap output path override.",
    )
    memory_refresh_parser.add_argument(
        "--source-id",
        dest="source_ids",
        action="append",
        help="Optional source_id to scope evidence ingest. Repeat to target multiple sources.",
    )
    memory_refresh_parser.add_argument(
        "--lint-fix",
        action="store_true",
        default=None,
        help="Explicitly enable memory-lint autofix during memory-refresh. This is already the default.",
    )
    memory_refresh_parser.add_argument(
        "--no-lint-fix",
        dest="lint_fix",
        action="store_false",
        help="Disable the default memory-lint autofix pass and run verification only.",
    )
    memory_refresh_parser.add_argument(
        "--lint-fix-rounds",
        type=int,
        default=1,
        help="Maximum autofix+rerlint rounds when lint autofix is enabled.",
    )
    memory_refresh_parser.add_argument(
        "--lint-model",
        default=None,
        help="Optional model override for the memory-lint phase.",
    )
    memory_refresh_parser.add_argument(
        "--consumer-profile-model",
        default=None,
        help="Fallback model id for the consumer-profile phase when phase-specific models are not provided.",
    )
    memory_refresh_parser.add_argument(
        "--consumer-profile-extraction-model",
        default=None,
        help="Optional model override for consumer-profile extraction windows.",
    )
    memory_refresh_parser.add_argument(
        "--consumer-profile-merge-model",
        default=None,
        help="Optional model override for the consumer-profile final merge.",
    )
    memory_refresh_parser.add_argument(
        "--consumer-profile-window-max-chars",
        type=int,
        default=None,
        help="Optional extraction window size override for consumer-profile generation.",
    )
    memory_refresh_parser.add_argument(
        "--json",
        action="store_true",
        help="Print the final run report as JSON.",
    )

    scheduler_plan_parser = subparsers.add_parser(
        "scheduler-plan",
        help="Prepare dry-run scheduler artifacts and compute whether ingest/lint would be due right now.",
    )
    scheduler_plan_parser.add_argument(
        "--product-config",
        type=Path,
        default=Path("config/product_config.json"),
        help="Path to unified product configuration JSON.",
    )
    scheduler_plan_parser.add_argument(
        "--state-dir",
        type=Path,
        default=Path("state"),
        help="Directory containing discovery and run state.",
    )
    scheduler_plan_parser.add_argument(
        "--scripts-dir",
        type=Path,
        default=Path("scripts"),
        help="Directory where the prepared activation script will be written.",
    )
    scheduler_plan_parser.add_argument(
        "--json",
        action="store_true",
        help="Print the scheduler plan report as JSON.",
    )
    scheduler_run_parser = subparsers.add_parser(
        "scheduler-run",
        help="Run memory-refresh only when the scheduler determines new logs make ingest due.",
    )
    scheduler_run_parser.add_argument(
        "--source-config",
        type=Path,
        default=Path("config/source_roots.json"),
        help="Path to source root configuration JSON.",
    )
    scheduler_run_parser.add_argument(
        "--product-config",
        type=Path,
        default=Path("config/product_config.json"),
        help="Path to unified product configuration JSON.",
    )
    scheduler_run_parser.add_argument(
        "--schema",
        type=Path,
        default=Path("schema/normalization_catalog.json"),
        help="Path to the normalization schema catalog JSON.",
    )
    scheduler_run_parser.add_argument(
        "--state-dir",
        type=Path,
        default=Path("state"),
        help="Directory containing discovery and refresh state.",
    )
    scheduler_run_parser.add_argument(
        "--normalized-dir",
        type=Path,
        default=Path("normalized"),
        help="Directory where normalized artifacts are written.",
    )
    scheduler_run_parser.add_argument(
        "--evidence-dir",
        type=Path,
        default=Path("evidence"),
        help="Directory where evidence artifacts are written.",
    )
    scheduler_run_parser.add_argument(
        "--memory-dir",
        type=Path,
        default=Path("memory"),
        help="Directory where compact memory artifacts are written.",
    )
    scheduler_run_parser.add_argument(
        "--audits-dir",
        type=Path,
        default=Path("audits"),
        help="Directory where notices and lint findings are written.",
    )
    scheduler_run_parser.add_argument(
        "--scripts-dir",
        type=Path,
        default=Path("scripts"),
        help="Directory where scheduler helper artifacts are written.",
    )
    scheduler_run_parser.add_argument(
        "--bootstrap-output-path",
        type=Path,
        default=None,
        help="Optional agent bootstrap output path override.",
    )
    scheduler_run_parser.add_argument(
        "--json",
        action="store_true",
        help="Print the scheduler run result as JSON.",
    )
    return parser


def format_result(result: DiscoveryResult) -> str:
    status_counts = ", ".join(
        f"{status}={count}" for status, count in sorted(result.report.status_counts.items())
    )
    outcome = "succeeded" if result.report.success else "failed"
    return (
        f"Discovery {outcome}: scanned_files={result.report.scanned_file_count}; "
        f"statuses[{status_counts or 'none'}]; "
        f"registry={result.registry_path}; run_log={result.run_log_path}"
    )


def format_normalization_result(result: NormalizationResult) -> str:
    source_counts = ", ".join(
        f"{status}={count}" for status, count in sorted(result.report.source_status_counts.items())
    )
    outcome = "succeeded" if result.report.success else "failed"
    return (
        f"Normalization {outcome}: sources[{source_counts or 'none'}]; "
        f"events={result.report.normalized_event_count}; "
        f"state={result.state_path}; run_log={result.run_log_path}; notices={result.notice_log_path}"
    )


def format_segmentation_result(result: SegmentationResult) -> str:
    source_counts = ", ".join(
        f"{status}={count}" for status, count in sorted(result.report.source_status_counts.items())
    )
    outcome = "succeeded" if result.report.success else "failed"
    return (
        f"Segmentation {outcome}: sources[{source_counts or 'none'}]; "
        f"segments={result.report.segment_count}; "
        f"state={result.state_path}; run_log={result.run_log_path}"
    )


def format_classification_result(result: ClassificationResult) -> str:
    source_counts = ", ".join(
        f"{status}={count}" for status, count in sorted(result.report.source_status_counts.items())
    )
    outcome = "succeeded" if result.report.success else "failed"
    return (
        f"Classification {outcome}: sources[{source_counts or 'none'}]; "
        f"segments={result.report.classified_segment_count}; "
        f"state={result.state_path}; run_log={result.run_log_path}; notices={result.notice_log_path}"
    )


def format_extraction_result(result: ExtractionResult) -> str:
    source_counts = ", ".join(
        f"{status}={count}" for status, count in sorted(result.report.source_status_counts.items())
    )
    outcome = "succeeded" if result.report.success else "failed"
    return (
        f"Extraction {outcome}: sources[{source_counts or 'none'}]; "
        f"observations={result.report.extracted_observation_count}; "
        f"state={result.state_path}; run_log={result.run_log_path}; notices={result.notice_log_path}"
    )


def format_wiki_result(result: WikiResult) -> str:
    page_counts = ", ".join(
        f"{status}={count}" for status, count in sorted(result.report.page_status_counts.items())
    )
    outcome = "succeeded" if result.report.success else "failed"
    return (
        f"Wiki {outcome}: pages[{page_counts or 'none'}]; "
        f"rendered={result.report.rendered_page_count}; "
        f"claims={result.report.synthesized_claim_count}; "
        f"state={result.state_path}; run_log={result.run_log_path}; notices={result.notice_log_path}"
    )


def format_bootstrap_result(result: BootstrapResult) -> str:
    domain_counts = ", ".join(
        f"{status}={count}" for status, count in sorted(result.report.domain_status_counts.items())
    )
    outcome = "succeeded" if result.report.success else "failed"
    return (
        f"Bootstrap {outcome}: domains[{domain_counts or 'none'}]; "
        f"rendered={result.report.rendered_domain_count}; "
        f"bullets={result.report.bullet_count}; "
        f"state={result.state_path}; run_log={result.run_log_path}; notices={result.notice_log_path}"
    )


def format_audit_result(result: AuditResult) -> str:
    target_counts = ", ".join(
        f"{status}={count}" for status, count in sorted(result.report.target_status_counts.items())
    )
    outcome = "succeeded" if result.report.success else "failed"
    return (
        f"Audit {outcome}: targets[{target_counts or 'none'}]; "
        f"findings={result.report.finding_count}; "
        f"warnings={result.report.warning_finding_count}; "
        f"errors={result.report.error_finding_count}; "
        f"state={result.state_path}; run_log={result.run_log_path}"
    )


def format_refresh_result(result: RefreshResult) -> str:
    executed = ",".join(
        f"{status.phase}:{status.scope_mode}"
        for status in result.report.phase_statuses
        if not status.skipped
    )
    outcome = "succeeded" if result.report.success else "failed"
    return (
        f"Refresh {outcome}: phases[{executed or 'none'}]; "
        f"changed_sources={len(result.report.changed_source_ids)}; "
        f"touched_domains={len(result.report.touched_domains)}; "
        f"warnings={result.report.warning_count}; "
        f"errors={result.report.error_count}; "
        f"state={result.state_path}; run_log={result.run_log_path}"
    )


def format_full_load_result(result: FullLoadResult) -> str:
    executed = ",".join(status.phase for status in result.report.phase_statuses)
    outcome = "succeeded" if result.report.success else "failed"
    return (
        f"Full-load {outcome}: phases[{executed or 'none'}]; "
        f"last_completed={result.report.last_completed_phase or 'none'}; "
        f"failed_phase={result.report.failed_phase or 'none'}; "
        f"stop_reason={result.report.stop_reason or 'none'}; "
        f"state={result.state_path}; run_log={result.run_log_path}"
    )


def format_onboarding_report(report: OnboardingReport) -> str:
    detected = report.detected
    return (
        f"Onboarding draft ready: root={report.project_root}; "
        f"os={detected.get('operating_system', 'unknown')}; "
        f"editor={detected.get('likely_editor', 'unknown')}; "
        f"agent={detected.get('likely_agent_platform', 'unknown')}; "
        f"markdown={detected.get('likely_markdown_mode', 'unknown')}; "
        f"bootstrap={detected.get('likely_bootstrap_target_path', 'unknown')}; "
        f"questions={len(report.questions)}; "
        f"entry={report.agent_entry_file}"
    )


def format_ingest_result(result: IngestResult) -> str:
    evidence_counts = ", ".join(
        f"{kind}={count}" for kind, count in sorted(result.report.evidence_counts.items())
    )
    outcome = "succeeded" if result.report.success else "failed"
    return (
        f"Ingest {outcome}: evidence[{evidence_counts or 'none'}]; "
        f"state={result.state_path}; run_log={result.run_log_path}; notices={result.notice_log_path}"
    )


def format_memory_result(result: MemoryResult) -> str:
    item_counts = ", ".join(
        f"{kind}={count}" for kind, count in sorted(result.report.item_counts.items())
    )
    outcome = "succeeded" if result.report.success else "failed"
    return (
        f"Memory {outcome}: items[{item_counts or 'none'}]; "
        f"rendered={result.report.rendered_file_count}; "
        f"state={result.state_path}; run_log={result.run_log_path}; notices={result.notice_log_path}"
    )


def format_memory_inspection_result(result: MemoryInspectionResult) -> str:
    outcome = "succeeded" if result.report.success else "failed"
    return f"Memory-inspect {outcome}: action={result.report.action}; matches={result.report.match_count}"


def format_memory_v2_result(result: MemoryV2Result) -> str:
    outcome = "succeeded" if result.report.success else "failed"
    return (
        f"Memory-v2 {outcome}: days={result.report.day_count}; "
        f"messages={result.report.message_count}; candidates={result.report.candidate_count}; "
        f"items={result.report.item_count}; rendered={result.report.rendered_file_count}; "
        f"output={result.output_dir}; run_log={result.run_log_path}"
    )


def format_agent_bootstrap_result(result: AgentBootstrapResult) -> str:
    outcome = "succeeded" if result.report.success else "failed"
    return (
        f"Agent-bootstrap {outcome}: target={result.target_path}; "
        f"items={result.report.selected_item_count}; chars={result.report.rendered_char_count}; "
        f"state={result.state_path}; run_log={result.run_log_path}; notices={result.notice_log_path}"
    )


def format_memory_lint_result(result: MemoryLintResult) -> str:
    outcome = "succeeded" if result.report.success else "failed"
    return (
        f"Memory-lint {outcome}: findings={result.report.finding_count}; "
        f"warnings={result.report.warning_count}; errors={result.report.error_count}; "
        f"state={result.state_path}; run_log={result.run_log_path}"
    )


def format_memory_review_result(result: MemoryReviewResult) -> str:
    outcome = "succeeded" if result.report.success else "failed"
    return (
        f"Memory-review {outcome}: pending={result.report.pending_count}; "
        f"approved={result.report.approved_count}; rejected={result.report.rejected_count}; "
        f"decisions={result.decisions_path}; review_items={result.review_items_path}"
    )


def format_consumer_profile_result(result: ConsumerProfileResult) -> str:
    outcome = "succeeded" if result.report.success else "failed"
    return (
        f"Consumer-profile {outcome}: snippets={result.report.source_snippet_count}; "
        f"candidates={result.report.candidate_count}; sections={result.report.section_count}; "
        f"profile={result.profile_path}; json={result.profile_json_path}"
    )


def format_memory_refresh_result(result: MemoryRefreshResult) -> str:
    phases = ",".join(status.phase for status in result.report.phase_statuses)
    outcome = "succeeded" if result.report.success else "failed"
    return (
        f"Memory-refresh {outcome}: phases[{phases or 'none'}]; "
        f"last_completed={result.report.last_completed_phase or 'none'}; "
        f"failed_phase={result.report.failed_phase or 'none'}; "
        f"warnings={result.report.warning_count}; errors={result.report.error_count}; "
        f"state={result.state_path}; run_log={result.run_log_path}"
    )


def format_scheduler_plan_result(result: SchedulerPlanResult) -> str:
    report = result.report
    return (
        f"Scheduler-plan ready: ingest_due={report.ingest_due}; "
        f"lint_due={report.lint_due}; "
        f"window={report.within_schedule_window}; "
        f"latest_log_update={report.latest_log_update_at or 'none'}; "
        f"activation_script={result.activation_script_path}; plan={result.plan_path}"
    )


def main(argv: list[str] | None = None) -> int:
    load_project_env()
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "discover":
        result = run_discovery(config_path=args.config, state_dir=args.state_dir)
        if args.json:
            print(json.dumps(result.report.to_dict(), indent=2, sort_keys=True))
        else:
            print(format_result(result))
            if result.report.fatal_error_summary:
                print(result.report.fatal_error_summary)
        return 0 if result.report.success else 1

    if args.command == "normalize":
        result = run_normalization(
            config_path=args.config,
            state_dir=args.state_dir,
            schema_path=args.schema,
            normalized_dir=args.normalized_dir,
            audits_dir=args.audits_dir,
        )
        if args.json:
            print(json.dumps(result.report.to_dict(), indent=2, sort_keys=True))
        else:
            print(format_normalization_result(result))
            if result.report.fatal_error_summary:
                print(result.report.fatal_error_summary)
        return 0 if result.report.success else 1

    if args.command == "segment":
        result = run_segmentation(
            state_dir=args.state_dir,
            normalized_dir=args.normalized_dir,
            segmented_dir=args.segmented_dir,
            source_ids=args.source_ids,
        )
        if args.json:
            print(json.dumps(result.report.to_dict(), indent=2, sort_keys=True))
        else:
            print(format_segmentation_result(result))
            if result.report.fatal_error_summary:
                print(result.report.fatal_error_summary)
        return 0 if result.report.success else 1

    if args.command == "classify":
        result = run_classification(
            taxonomy_path=args.taxonomy,
            state_dir=args.state_dir,
            normalized_dir=args.normalized_dir,
            segmented_dir=args.segmented_dir,
            classified_dir=args.classified_dir,
            audits_dir=args.audits_dir,
            source_ids=args.source_ids,
            source_roots_config_path=args.source_roots_config,
        )
        if args.json:
            print(json.dumps(result.report.to_dict(), indent=2, sort_keys=True))
        else:
            print(format_classification_result(result))
            if result.report.fatal_error_summary:
                print(result.report.fatal_error_summary)
        return 0 if result.report.success else 1

    if args.command == "extract":
        result = run_extraction(
            rules_path=args.rules,
            state_dir=args.state_dir,
            normalized_dir=args.normalized_dir,
            classified_dir=args.classified_dir,
            extracted_dir=args.extracted_dir,
            audits_dir=args.audits_dir,
            source_ids=args.source_ids,
            source_roots_config_path=args.source_roots_config,
        )
        if args.json:
            print(json.dumps(result.report.to_dict(), indent=2, sort_keys=True))
        else:
            print(format_extraction_result(result))
            if result.report.fatal_error_summary:
                print(result.report.fatal_error_summary)
        return 0 if result.report.success else 1

    if args.command == "wiki":
        result = run_wiki(
            config_path=args.config,
            state_dir=args.state_dir,
            extracted_dir=args.extracted_dir,
            wiki_dir=args.wiki_dir,
            audits_dir=args.audits_dir,
            source_ids=args.source_ids,
        )
        if args.json:
            print(json.dumps(result.report.to_dict(), indent=2, sort_keys=True))
        else:
            print(format_wiki_result(result))
            if result.report.fatal_error_summary:
                print(result.report.fatal_error_summary)
        return 0 if result.report.success else 1

    if args.command == "bootstrap":
        result = run_bootstrap(
            config_path=args.config,
            state_dir=args.state_dir,
            extracted_dir=args.extracted_dir,
            wiki_dir=args.wiki_dir,
            bootstrap_dir=args.bootstrap_dir,
            audits_dir=args.audits_dir,
            source_ids=args.source_ids,
        )
        if args.json:
            print(json.dumps(result.report.to_dict(), indent=2, sort_keys=True))
        else:
            print(format_bootstrap_result(result))
            if result.report.fatal_error_summary:
                print(result.report.fatal_error_summary)
        return 0 if result.report.success else 1

    if args.command == "audit":
        result = run_audit(
            config_path=args.config,
            state_dir=args.state_dir,
            extracted_dir=args.extracted_dir,
            wiki_dir=args.wiki_dir,
            bootstrap_dir=args.bootstrap_dir,
            audits_dir=args.audits_dir,
            source_ids=args.source_ids,
        )
        if args.json:
            print(json.dumps(result.report.to_dict(), indent=2, sort_keys=True))
        else:
            print(format_audit_result(result))
            if result.report.fatal_error_summary:
                print(result.report.fatal_error_summary)
        return 0 if result.report.success and result.report.error_finding_count == 0 else 1

    if args.command == "refresh":
        result = run_refresh(
            config_path=args.config,
            state_dir=args.state_dir,
            audits_dir=args.audits_dir,
            source_ids=args.source_ids,
        )
        if args.json:
            print(json.dumps(result.report.to_dict(), indent=2, sort_keys=True))
        else:
            print(format_refresh_result(result))
            if result.report.fatal_error_summary:
                print(result.report.fatal_error_summary)
        return 0 if result.report.success else 1

    if args.command == "onboard":
        result = run_onboarding(project_root=args.project_root, config_path=args.config_out, brief_path=args.brief_out)
        if args.json:
            print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
        else:
            print(format_onboarding_report(result))
        return 0

    if args.command == "ingest":
        result = run_ingest(
            product_config_path=args.product_config,
            state_dir=args.state_dir,
            normalized_dir=args.normalized_dir,
            evidence_dir=args.evidence_dir,
            audits_dir=args.audits_dir,
            source_ids=args.source_ids,
        )
        if args.json:
            print(json.dumps(result.report.to_dict(), indent=2, sort_keys=True))
        else:
            print(format_ingest_result(result))
            if result.report.fatal_error_summary:
                print(result.report.fatal_error_summary)
        return 0 if result.report.success else 1

    if args.command == "memory":
        result = run_memory_generation(
            product_config_path=args.product_config,
            state_dir=args.state_dir,
            evidence_dir=args.evidence_dir,
            memory_dir=args.memory_dir,
            audits_dir=args.audits_dir,
            projects=args.projects,
        )
        if args.json:
            print(json.dumps(result.report.to_dict(), indent=2, sort_keys=True))
        else:
            print(format_memory_result(result))
            if result.report.fatal_error_summary:
                print(result.report.fatal_error_summary)
        return 0 if result.report.success else 1

    if args.command == "memory-inspect":
        result = run_memory_inspection(
            action=args.action,
            memory_dir=args.memory_dir,
            state_dir=args.state_dir,
            project=args.project,
            rule_query=args.rule_query,
        )
        if args.json:
            print(json.dumps(result.payload, indent=2, sort_keys=True))
        else:
            print(format_memory_inspection_result(result))
            if result.report.success:
                print(json.dumps(result.payload, indent=2, sort_keys=True))
            elif result.report.fatal_error_summary:
                print(result.report.fatal_error_summary)
        return 0 if result.report.success else 1

    if args.command == "memory-v2":
        result = run_memory_v2(
            input_dir=args.input_dir,
            output_dir=args.output_dir,
            state_dir=args.state_dir,
            days=args.days,
            all_days=args.all_days,
            model=args.model,
            project_root_dir=args.project_root_dir,
        )
        if args.json:
            print(json.dumps(result.report.to_dict(), indent=2, sort_keys=True))
        else:
            print(format_memory_v2_result(result))
            if result.report.fatal_error_summary:
                print(result.report.fatal_error_summary)
        return 0 if result.report.success else 1

    if args.command == "agent-bootstrap":
        result = run_agent_bootstrap(
            product_config_path=args.product_config,
            state_dir=args.state_dir,
            memory_dir=args.memory_dir,
            audits_dir=args.audits_dir,
            output_path=args.output_path,
            projects=args.projects,
        )
        if args.json:
            print(json.dumps(result.report.to_dict(), indent=2, sort_keys=True))
        else:
            print(format_agent_bootstrap_result(result))
            if result.report.fatal_error_summary:
                print(result.report.fatal_error_summary)
        return 0 if result.report.success else 1

    if args.command == "memory-lint":
        result = run_memory_lint(
            product_config_path=args.product_config,
            state_dir=args.state_dir,
            memory_dir=args.memory_dir,
            audits_dir=args.audits_dir,
            bootstrap_path=args.bootstrap_path,
            autofix=args.fix,
            model=args.model,
            max_fix_rounds=args.max_fix_rounds,
        )
        if args.json:
            print(json.dumps(result.report.to_dict(), indent=2, sort_keys=True))
        else:
            print(format_memory_lint_result(result))
            if result.report.fatal_error_summary:
                print(result.report.fatal_error_summary)
        return 0 if result.report.success and result.report.error_count == 0 else 1

    if args.command == "memory-review":
        result = run_memory_review(
            memory_dir=args.memory_dir,
            state_dir=args.state_dir,
            audits_dir=args.audits_dir,
            approve=args.approve,
            reject=args.reject,
        )
        if args.json:
            print(json.dumps(result.report.to_dict(), indent=2, sort_keys=True))
        else:
            print(format_memory_review_result(result))
            if result.report.fatal_error_summary:
                print(result.report.fatal_error_summary)
        return 0 if result.report.success else 1

    if args.command == "consumer-profile":
        result = run_consumer_profile(
            evidence_dir=args.evidence_dir,
            memory_dir=args.memory_dir,
            state_dir=args.state_dir,
            audits_dir=args.audits_dir,
            policy_path=args.policy,
            model=args.model,
            extraction_model=args.extraction_model,
            merge_model=args.merge_model,
            window_max_chars=args.window_max_chars,
        )
        if args.json:
            print(json.dumps(result.report.to_dict(), indent=2, sort_keys=True))
        else:
            print(format_consumer_profile_result(result))
            if result.report.fatal_error_summary:
                print(result.report.fatal_error_summary)
        return 0 if result.report.success else 1

    if args.command == "memory-refresh":
        result = run_memory_refresh(
            source_roots_config_path=args.source_config,
            product_config_path=args.product_config,
            normalization_schema_path=args.schema,
            state_dir=args.state_dir,
            normalized_dir=args.normalized_dir,
            evidence_dir=args.evidence_dir,
            memory_dir=args.memory_dir,
            audits_dir=args.audits_dir,
            bootstrap_output_path=args.bootstrap_output_path,
            source_ids=args.source_ids,
            lint_fix=args.lint_fix,
            lint_fix_rounds=args.lint_fix_rounds,
            lint_model=args.lint_model,
            consumer_profile_model=args.consumer_profile_model,
            consumer_profile_extraction_model=args.consumer_profile_extraction_model,
            consumer_profile_merge_model=args.consumer_profile_merge_model,
            consumer_profile_window_max_chars=args.consumer_profile_window_max_chars,
        )
        if args.json:
            print(json.dumps(result.report.to_dict(), indent=2, sort_keys=True))
        else:
            print(format_memory_refresh_result(result))
            if result.report.fatal_error_summary:
                print(result.report.fatal_error_summary)
        return 0 if result.report.success else 1

    if args.command == "scheduler-plan":
        result = run_scheduler_plan(
            product_config_path=args.product_config,
            state_dir=args.state_dir,
            scripts_dir=args.scripts_dir,
        )
        if args.json:
            print(json.dumps(result.report.to_dict(), indent=2, sort_keys=True))
        else:
            print(format_scheduler_plan_result(result))
        return 0

    if args.command == "scheduler-run":
        config = load_product_config(args.product_config)
        plan = run_scheduler_plan(
            product_config_path=args.product_config,
            state_dir=args.state_dir,
            scripts_dir=args.scripts_dir,
        )
        registry = load_json(Path(args.state_dir) / "source_registry.json")
        latest_log_update_at = latest_active_log_update(registry)
        last_refresh_at = last_refresh_checkpoint_finished_at(
            Path(args.state_dir) / "memory_refresh_state.json",
            Path(args.state_dir) / "memory_refresh_runs.jsonl",
        )
        has_new_logs = bool(
            latest_log_update_at
            and (not last_refresh_at or parse_iso(latest_log_update_at) > parse_iso(last_refresh_at))
        )
        if not has_new_logs:
            payload = {
                "success": True,
                "executed": False,
                "reason": "no_new_logs",
                "latest_log_update_at": latest_log_update_at,
                "last_refresh_at": last_refresh_at,
                "within_schedule_window": plan.report.within_schedule_window,
            }
            if args.json:
                print(json.dumps(payload, indent=2, sort_keys=True))
            else:
                print(
                    "Scheduler run skipped: no new logs since the last successful refresh."
                )
            return 0

        result = run_memory_refresh(
            source_roots_config_path=args.source_config,
            product_config_path=args.product_config,
            normalization_schema_path=args.schema,
            state_dir=args.state_dir,
            normalized_dir=args.normalized_dir,
            evidence_dir=args.evidence_dir,
            memory_dir=args.memory_dir,
            audits_dir=args.audits_dir,
            bootstrap_output_path=args.bootstrap_output_path,
            lint_fix=config.scheduler.lint_autofix_enabled,
            lint_fix_rounds=config.scheduler.lint_autofix_max_rounds,
            consumer_profile_extraction_model=config.scheduler.consumer_profile_extraction_model,
            consumer_profile_merge_model=config.scheduler.consumer_profile_merge_model,
            consumer_profile_window_max_chars=config.scheduler.consumer_profile_window_max_chars,
        )
        if args.json:
            print(
                json.dumps(
                    {
                        "success": result.report.success,
                        "executed": True,
                        "reason": "ingest_due",
                        "refresh_report": result.report.to_dict(),
                    },
                    indent=2,
                    sort_keys=True,
                )
            )
        else:
            print(format_memory_refresh_result(result))
            if result.report.fatal_error_summary:
                print(result.report.fatal_error_summary)
        return 0 if result.report.success else 1

    result = run_full_load(
        config_path=args.config,
        state_dir=args.state_dir,
        audits_dir=args.audits_dir,
    )
    if args.json:
        print(json.dumps(result.report.to_dict(), indent=2, sort_keys=True))
    else:
        print(format_full_load_result(result))
        if result.report.fatal_error_summary:
            print(result.report.fatal_error_summary)
    return 0 if result.report.success else 1
