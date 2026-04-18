from __future__ import annotations

import argparse
import json
from pathlib import Path

from .agent_bootstrap import AgentBootstrapResult, run_agent_bootstrap
from .audit import AuditResult, run_audit
from .bootstrap import BootstrapResult, run_bootstrap
from .classification import ClassificationResult, run_classification
from .discovery import DiscoveryResult, run_discovery
from .env_loader import load_project_env
from .extraction import ExtractionResult, run_extraction
from .full_load import FullLoadResult, run_full_load
from .ingest import IngestResult, run_ingest
from .memory_generation import MemoryResult, run_memory_generation
from .memory_lint import MemoryLintResult, run_memory_lint
from .normalization import NormalizationResult, run_normalization
from .onboarding import OnboardingReport, run_onboarding
from .refresh import RefreshResult, run_refresh
from .segmentation import SegmentationResult, run_segmentation
from .wiki import WikiResult, run_wiki


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="WikiMemory discovery tools")
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
        help="Run deterministic lint checks over compact memory and agent bootstrap artifacts.",
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
        "--json",
        action="store_true",
        help="Print the final run report as JSON.",
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
        f"markdown={detected.get('likely_markdown_mode', 'unknown')}; "
        f"bootstrap={detected.get('likely_bootstrap_target_path', 'unknown')}; "
        f"questions={len(report.questions)}"
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
        result = run_onboarding(project_root=args.project_root, config_path=args.config_out)
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
        )
        if args.json:
            print(json.dumps(result.report.to_dict(), indent=2, sort_keys=True))
        else:
            print(format_memory_lint_result(result))
            if result.report.fatal_error_summary:
                print(result.report.fatal_error_summary)
        return 0 if result.report.success and result.report.error_count == 0 else 1

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
