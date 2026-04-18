from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .bootstrap import (
    BootstrapPacket,
    BootstrapStateRecord,
    build_bootstrap_plan,
    load_bootstrap_config,
    load_bootstrap_state,
    load_domain_claims,
    packet_digest,
)
from .discovery import DiscoveryError, atomic_write_text, ensure_directory, utc_now
from .extraction import ExtractionStateRecord, load_extraction_state
from .normalization import append_jsonl_text
from .wiki import WikiStateRecord, load_wiki_state

STATE_SCHEMA_VERSION = 1
AUDIT_SCHEMA_VERSION = 2
VALID_SEVERITIES = {"info", "warning", "error"}
FAMILY_FILENAMES = {
    "contradictions": "contradictions.jsonl",
    "duplicates": "duplicates.jsonl",
    "stale_items": "stale_items.jsonl",
    "provenance_gaps": "provenance_gaps.jsonl",
    "wiki_bootstrap_drift": "wiki_bootstrap_drift.jsonl",
    "wiki_quality": "wiki_quality.jsonl",
}
NORMALIZE_TEXT_PATTERN = re.compile(r"\s+")
GENERIC_SUBJECT_KEYS = {"", "it", "this", "that"}
EXCLUSIVE_CONTRADICTION_ITEM_TYPES = {
    "communication_preference",
    "do_rule",
    "dont_rule",
    "workflow_rule",
    "decision",
    "current_state",
}


class AuditError(DiscoveryError):
    """Fatal audit error that must stop the run."""


@dataclass(frozen=True)
class AuditConfig:
    schema_version: int
    audit_schema_version: int
    rules_version: int
    bootstrap_config_path: str
    stale_windows_days: dict[str, int]
    strong_confidences: frozenset[str]
    near_stale_enabled: bool
    near_stale_ratio: float
    transient_rule_item_types: frozenset[str]
    generic_claim_patterns: tuple[str, ...]
    page_size_caps: dict[str, int]


@dataclass(frozen=True)
class AuditStateRecord:
    scope_kind: str
    scope_key: str
    audit_schema_version: int
    rules_version: int
    input_digest: str
    finding_counts: dict[str, int]
    severity_counts: dict[str, int]
    status: str
    last_audited_at: str
    last_run_id: str

    @property
    def record_key(self) -> str:
        return f"{self.scope_kind}:{self.scope_key}"

    def to_dict(self) -> dict[str, object]:
        return {
            "scope_kind": self.scope_kind,
            "scope_key": self.scope_key,
            "audit_schema_version": self.audit_schema_version,
            "rules_version": self.rules_version,
            "input_digest": self.input_digest,
            "finding_counts": dict(sorted(self.finding_counts.items())),
            "severity_counts": dict(sorted(self.severity_counts.items())),
            "status": self.status,
            "last_audited_at": self.last_audited_at,
            "last_run_id": self.last_run_id,
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "AuditStateRecord":
        return cls(
            scope_kind=str(data["scope_kind"]),
            scope_key=str(data["scope_key"]),
            audit_schema_version=int(data["audit_schema_version"]),
            rules_version=int(data["rules_version"]),
            input_digest=str(data["input_digest"]),
            finding_counts={str(key): int(value) for key, value in dict(data.get("finding_counts", {})).items()},
            severity_counts={str(key): int(value) for key, value in dict(data.get("severity_counts", {})).items()},
            status=str(data["status"]),
            last_audited_at=str(data["last_audited_at"]),
            last_run_id=str(data["last_run_id"]),
        )


@dataclass(frozen=True)
class AuditFinding:
    finding_id: str
    family: str
    severity: str
    scope_kind: str
    scope_key: str
    check_type: str
    summary: str
    supporting_refs: tuple[dict[str, object], ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "finding_id": self.finding_id,
            "family": self.family,
            "severity": self.severity,
            "scope_kind": self.scope_kind,
            "scope_key": self.scope_key,
            "check_type": self.check_type,
            "summary": self.summary,
            "supporting_refs": [dict(ref) for ref in self.supporting_refs],
        }


@dataclass(frozen=True)
class AuditRunReport:
    run_id: str
    started_at: str
    finished_at: str
    target_status_counts: dict[str, int]
    finding_count: int
    warning_finding_count: int
    error_finding_count: int
    success: bool
    fatal_error_summary: str | None

    def to_dict(self) -> dict[str, object]:
        return {
            "run_id": self.run_id,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "target_status_counts": self.target_status_counts,
            "finding_count": self.finding_count,
            "warning_finding_count": self.warning_finding_count,
            "error_finding_count": self.error_finding_count,
            "success": self.success,
            "fatal_error_summary": self.fatal_error_summary,
        }


@dataclass(frozen=True)
class AuditResult:
    report: AuditRunReport
    state_path: Path
    run_log_path: Path
    family_paths: dict[str, Path]


def run_audit(
    config_path: Path | str,
    state_dir: Path | str,
    extracted_dir: Path | str,
    wiki_dir: Path | str,
    bootstrap_dir: Path | str,
    audits_dir: Path | str,
    source_ids: Iterable[str] | None = None,
) -> AuditResult:
    config_path = Path(config_path)
    state_dir = Path(state_dir)
    extracted_dir = Path(extracted_dir)
    wiki_dir = Path(wiki_dir)
    bootstrap_dir = Path(bootstrap_dir)
    audits_dir = Path(audits_dir)

    extraction_state_path = state_dir / "extraction_state.json"
    wiki_state_path = state_dir / "wiki_state.json"
    bootstrap_state_path = state_dir / "bootstrap_state.json"
    state_path = state_dir / "audit_state.json"
    run_log_path = state_dir / "audit_runs.jsonl"
    family_paths = {family: audits_dir / filename for family, filename in FAMILY_FILENAMES.items()}

    ensure_directory(state_dir)
    ensure_directory(audits_dir)

    run_id = f"audit-{utc_now().replace(':', '').replace('.', '').replace('-', '')}"
    started_at = utc_now()
    staging_root = audits_dir / ".staging" / run_id

    previous_state_text = state_path.read_text(encoding="utf-8") if state_path.exists() else None
    previous_run_log_text = run_log_path.read_text(encoding="utf-8") if run_log_path.exists() else ""
    previous_family_texts = {
        family: path.read_text(encoding="utf-8") if path.exists() else ""
        for family, path in family_paths.items()
    }

    try:
        if not extraction_state_path.exists():
            raise AuditError(f"Missing extraction state: {extraction_state_path}")
        if not wiki_state_path.exists():
            raise AuditError(f"Missing wiki state: {wiki_state_path}")
        if not bootstrap_state_path.exists():
            raise AuditError(f"Missing bootstrap state: {bootstrap_state_path}")

        config = load_audit_config(config_path)
        extraction_state = load_extraction_state(extraction_state_path)
        wiki_state = load_wiki_state(wiki_state_path)
        bootstrap_state = load_bootstrap_state(bootstrap_state_path)
        previous_state = load_audit_state(state_path)

        scope = resolve_audit_scope(source_ids, extraction_state, wiki_state, bootstrap_state, extracted_dir)
        domain_items_map = load_audit_domain_items(scope["domains"], extracted_dir)
        page_manifests = load_page_manifests(scope["pages"], wiki_state, wiki_dir)
        page_markdown_map = load_page_markdown(scope["pages"], wiki_state, wiki_dir)
        bootstrap_manifests = load_bootstrap_manifests(scope["bootstrap_domains"], bootstrap_state, bootstrap_dir)

        bootstrap_config_path = resolve_bootstrap_config_path(config, config_path)
        bootstrap_config = load_bootstrap_config(bootstrap_config_path)
        planned_bootstrap_domains = [domain for domain in scope["bootstrap_domains"] if domain in bootstrap_config.domain_map]
        current_packets = {
            packet.domain: packet
            for packet in build_bootstrap_plan(planned_bootstrap_domains, bootstrap_config, extracted_dir, wiki_dir)
        }
        current_domain_claims = load_domain_claims(planned_bootstrap_domains, wiki_dir)

        findings_by_family: dict[str, list[AuditFinding]] = {family: [] for family in FAMILY_FILENAMES}

        for domain in scope["domains"]:
            items = domain_items_map.get(domain, [])
            findings_by_family["contradictions"].extend(audit_domain_contradictions(domain, items, config))
            findings_by_family["duplicates"].extend(audit_domain_duplicates(domain, items))
            findings_by_family["stale_items"].extend(audit_domain_staleness(domain, items, config))
            findings_by_family["provenance_gaps"].extend(audit_domain_provenance(domain, items))
            findings_by_family["wiki_quality"].extend(audit_domain_wiki_quality(domain, items, config))

        for page_id in scope["pages"]:
            manifest = page_manifests[page_id]
            findings_by_family["duplicates"].extend(audit_page_duplicates(page_id, manifest))
            findings_by_family["provenance_gaps"].extend(audit_page_provenance(page_id, manifest))
            findings_by_family["wiki_quality"].extend(
                audit_page_quality(page_id, manifest, page_markdown_map.get(page_id, ""), wiki_state[page_id], config)
            )

        for domain in scope["bootstrap_domains"]:
            manifest = bootstrap_manifests[domain]
            current_packet = current_packets.get(domain)
            current_items = domain_items_map.get(domain, [])
            current_claims = current_domain_claims.get(domain, [])
            state_record = bootstrap_state[domain]
            findings_by_family["duplicates"].extend(audit_bootstrap_duplicates(domain, manifest))
            findings_by_family["provenance_gaps"].extend(
                audit_bootstrap_provenance(domain, manifest, current_items, current_claims)
            )
            findings_by_family["wiki_bootstrap_drift"].extend(
                audit_bootstrap_drift(domain, manifest, state_record, current_packet, current_items, current_claims, config)
            )

        for family in findings_by_family:
            findings_by_family[family] = dedupe_findings(findings_by_family[family])

        scoped_keys = {
            *(("domain", domain) for domain in scope["domains"]),
            *(("page", page_id) for page_id in scope["pages"]),
            *(("bootstrap_domain", domain) for domain in scope["bootstrap_domains"]),
        }
        merged_findings = merge_findings(previous_family_texts, findings_by_family, scoped_keys, full_run=source_ids is None)
        next_state = {} if source_ids is None else dict(previous_state)
        for record in build_scope_state_records(
            scope=scope,
            config=config,
            domain_items_map=domain_items_map,
            page_manifests=page_manifests,
            bootstrap_manifests=bootstrap_manifests,
            merged_findings=merged_findings,
            current_packets=current_packets,
            run_id=run_id,
        ):
            next_state[record.record_key] = record

        if source_ids is None:
            validate_audit_state(next_state, merged_findings, scope)

        staged_state_path = staging_root / "audit_state.json"
        staged_run_log_path = staging_root / "audit_runs.jsonl"
        staged_family_paths = {family: staging_root / path.name for family, path in family_paths.items()}

        report = AuditRunReport(
            run_id=run_id,
            started_at=started_at,
            finished_at=utc_now(),
            target_status_counts={"audited": len(scoped_keys)},
            finding_count=sum(len(findings) for findings in merged_findings.values()),
            warning_finding_count=sum(
                1
                for findings in merged_findings.values()
                for finding in findings
                if finding.severity == "warning"
            ),
            error_finding_count=sum(
                1
                for findings in merged_findings.values()
                for finding in findings
                if finding.severity == "error"
            ),
            success=True,
            fatal_error_summary=None,
        )

        write_text(staged_state_path, json.dumps(build_state_payload(next_state), indent=2, sort_keys=True) + "\n")
        write_text(staged_run_log_path, append_jsonl_text(previous_run_log_text, report.to_dict()))
        for family, staged_path in staged_family_paths.items():
            write_text(staged_path, render_findings_jsonl(merged_findings[family]))

        validate_family_and_state_alignment(merged_findings, next_state)

        ensure_directory(run_log_path.parent)
        os.replace(staged_state_path, state_path)
        os.replace(staged_run_log_path, run_log_path)
        for family, path in family_paths.items():
            os.replace(staged_family_paths[family], path)
        cleanup_staging_root(staging_root)
        return AuditResult(
            report=report,
            state_path=state_path,
            run_log_path=run_log_path,
            family_paths=family_paths,
        )
    except Exception as exc:
        cleanup_staging_root(staging_root)
        failure_report = AuditRunReport(
            run_id=run_id,
            started_at=started_at,
            finished_at=utc_now(),
            target_status_counts={},
            finding_count=0,
            warning_finding_count=0,
            error_finding_count=0,
            success=False,
            fatal_error_summary=str(exc),
        )
        atomic_write_text(run_log_path, append_jsonl_text(previous_run_log_text, failure_report.to_dict()))
        if previous_state_text is None and state_path.exists():
            state_path.unlink(missing_ok=True)
        if previous_state_text is not None:
            atomic_write_text(state_path, previous_state_text)
        for family, path in family_paths.items():
            previous_text = previous_family_texts[family]
            if previous_text:
                atomic_write_text(path, previous_text)
            elif path.exists():
                path.unlink(missing_ok=True)
        return AuditResult(
            report=failure_report,
            state_path=state_path,
            run_log_path=run_log_path,
            family_paths=family_paths,
        )


def load_audit_config(config_path: Path) -> AuditConfig:
    try:
        payload = json.loads(config_path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError as exc:
        raise AuditError(f"Missing audit config: {config_path}") from exc
    except json.JSONDecodeError as exc:
        raise AuditError(f"Invalid audit config JSON: {config_path}") from exc

    stale_windows = dict(payload.get("stale_windows_days", {}))
    if not stale_windows:
        raise AuditError("Audit config must define stale_windows_days")
    strong_confidences = frozenset(str(value) for value in payload.get("strong_confidences", ["explicit", "strong"]))
    return AuditConfig(
        schema_version=int(payload["schema_version"]),
        audit_schema_version=int(payload["audit_schema_version"]),
        rules_version=int(payload["rules_version"]),
        bootstrap_config_path=str(payload.get("bootstrap_config_path", "config/bootstrap_config.json")),
        stale_windows_days={str(key): int(value) for key, value in stale_windows.items()},
        strong_confidences=strong_confidences,
        near_stale_enabled=bool(payload.get("near_stale_enabled", False)),
        near_stale_ratio=float(payload.get("near_stale_ratio", 0.9)),
        transient_rule_item_types=frozenset(
            str(item) for item in payload.get("transient_rule_item_types", [])
        ),
        generic_claim_patterns=tuple(
            normalize_text(str(item))
            for item in payload.get("generic_claim_patterns", [])
            if normalize_text(str(item))
        ),
        page_size_caps={str(key): int(value) for key, value in dict(payload.get("page_size_caps", {})).items()},
    )


def load_audit_state(state_path: Path) -> dict[str, AuditStateRecord]:
    if not state_path.exists():
        return {}
    try:
        payload = json.loads(state_path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise AuditError(f"Invalid audit state JSON: {state_path}") from exc
    if int(payload.get("schema_version", -1)) != STATE_SCHEMA_VERSION:
        raise AuditError(f"Unsupported audit state schema version in {state_path}: {payload.get('schema_version')}")
    records = [AuditStateRecord.from_dict(item) for item in payload.get("targets", [])]
    return {record.record_key: record for record in records}


def resolve_bootstrap_config_path(config: AuditConfig, config_path: Path) -> Path:
    path = Path(config.bootstrap_config_path)
    if path.is_absolute():
        return path
    return (config_path.parent / path).resolve()


def resolve_audit_scope(
    source_ids: Iterable[str] | None,
    extraction_state: dict[str, ExtractionStateRecord],
    wiki_state: dict[str, WikiStateRecord],
    bootstrap_state: dict[str, BootstrapStateRecord],
    extracted_dir: Path,
) -> dict[str, list[str]]:
    if source_ids is None:
        domains = sorted(
            path.name for path in (extracted_dir / "domains").iterdir()
            if path.is_dir()
        ) if (extracted_dir / "domains").exists() else []
        return {
            "domains": domains,
            "pages": sorted(wiki_state),
            "bootstrap_domains": sorted(bootstrap_state),
        }

    requested = sorted(dict.fromkeys(str(source_id) for source_id in source_ids))
    missing = [source_id for source_id in requested if source_id not in extraction_state]
    if missing:
        raise AuditError(f"Requested source_ids are missing from extraction state: {', '.join(missing)}")
    domains = dedupe_preserving_order(
        [domain for source_id in requested for domain in extraction_state[source_id].touched_domains]
    )
    return {
        "domains": domains,
        "pages": sorted(page_id for page_id, record in wiki_state.items() if record.domain in domains),
        "bootstrap_domains": sorted(domain for domain in bootstrap_state if domain in domains),
    }


def load_audit_domain_items(domains: list[str], extracted_dir: Path) -> dict[str, list[dict[str, object]]]:
    domain_items: dict[str, list[dict[str, object]]] = {}
    for domain in domains:
        path = extracted_dir / "domains" / domain / "items.jsonl"
        domain_items[domain] = read_jsonl_required(path) if path.exists() else []
    return domain_items


def load_page_manifests(
    page_ids: list[str],
    wiki_state: dict[str, WikiStateRecord],
    wiki_dir: Path,
) -> dict[str, dict[str, object]]:
    manifests: dict[str, dict[str, object]] = {}
    for page_id in page_ids:
        if page_id not in wiki_state:
            raise AuditError(f"Missing wiki state for page {page_id}")
        manifests[page_id] = read_json_required(wiki_dir / wiki_state[page_id].relative_manifest_path)
    return manifests


def load_page_markdown(
    page_ids: list[str],
    wiki_state: dict[str, WikiStateRecord],
    wiki_dir: Path,
) -> dict[str, str]:
    markdown_map: dict[str, str] = {}
    for page_id in page_ids:
        if page_id not in wiki_state:
            raise AuditError(f"Missing wiki state for page {page_id}")
        markdown_map[page_id] = (wiki_dir / wiki_state[page_id].relative_page_path).read_text(encoding="utf-8")
    return markdown_map


def load_bootstrap_manifests(
    domains: list[str],
    bootstrap_state: dict[str, BootstrapStateRecord],
    bootstrap_dir: Path,
) -> dict[str, dict[str, object]]:
    manifests: dict[str, dict[str, object]] = {}
    for domain in domains:
        if domain not in bootstrap_state:
            raise AuditError(f"Missing bootstrap state for domain {domain}")
        manifests[domain] = read_json_required(bootstrap_dir / bootstrap_state[domain].relative_manifest_path)
    return manifests


def audit_domain_contradictions(domain: str, items: list[dict[str, object]], config: AuditConfig) -> list[AuditFinding]:
    grouped: dict[tuple[str, str, str, str], list[dict[str, object]]] = defaultdict(list)
    for item in items:
        grouped[
            (
                str(item.get("primary_domain", domain)),
                str(item.get("item_type", "")),
                str(item.get("target_page_key", "")),
                str(item.get("subject_key", "")),
            )
        ].append(item)

    findings: list[AuditFinding] = []
    for key, group in grouped.items():
        active_items = [item for item in group if str(item.get("temporal_status", "")) == "active"]
        relevant = [item for item in group if str(item.get("temporal_status", "")) != "superseded"] if active_items else list(group)
        signatures = {str(item.get("normalized_signature", "")) for item in relevant}
        if len(signatures) < 2:
            continue
        strong_active = [
            item for item in active_items
            if str(item.get("confidence", "")) in config.strong_confidences
        ]
        severity = "error" if len({str(item.get('normalized_signature', '')) for item in strong_active}) >= 2 else "warning"
        _, item_type, target_page_key, subject_key = key
        normalized_subject_key = normalize_subject_key(subject_key)
        if item_type not in EXCLUSIVE_CONTRADICTION_ITEM_TYPES:
            severity = "warning"
        elif normalized_subject_key in GENERIC_SUBJECT_KEYS:
            severity = "warning"
        findings.append(
            make_finding(
                family="contradictions",
                severity=severity,
                scope_kind="domain",
                scope_key=domain,
                check_type="conflicting_domain_items",
                summary=(
                    f"conflicting {item_type} items exist for subject {subject_key or 'unknown'} "
                    f"on {target_page_key or 'unknown-page'}"
                ),
                supporting_refs=[
                    build_item_ref(item)
                    for item in sorted(
                        relevant,
                        key=lambda entry: (
                            str(entry.get("last_seen_at", "")),
                            str(entry.get("item_key", "")),
                        ),
                    )
                ],
            )
        )
    return findings


def audit_domain_duplicates(domain: str, items: list[dict[str, object]]) -> list[AuditFinding]:
    grouped: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for item in items:
        grouped[(str(item.get("item_type", "")), str(item.get("normalized_signature", "")))].append(item)
    findings: list[AuditFinding] = []
    for key, group in grouped.items():
        if len(group) < 2:
            continue
        item_type, normalized_signature = key
        findings.append(
            make_finding(
                family="duplicates",
                severity="warning",
                scope_kind="domain",
                scope_key=domain,
                check_type="duplicate_domain_items",
                summary=f"duplicate canonical {item_type} items remain for signature {normalized_signature[:60]}",
                supporting_refs=[build_item_ref(item) for item in sorted(group, key=lambda entry: str(entry.get("item_key", "")))],
            )
        )
    return findings


def audit_domain_staleness(domain: str, items: list[dict[str, object]], config: AuditConfig) -> list[AuditFinding]:
    findings: list[AuditFinding] = []
    now = datetime.now(timezone.utc)
    for item in items:
        if str(item.get("temporal_status", "")) != "active":
            continue
        item_type = str(item.get("item_type", ""))
        window_days = config.stale_windows_days.get(item_type)
        if window_days is None:
            continue
        last_seen_at = str(item.get("last_seen_at") or item.get("first_seen_at") or "")
        timestamp = parse_iso_timestamp(last_seen_at)
        if timestamp is None:
            continue
        age_days = (now - timestamp).days
        if age_days > window_days:
            findings.append(
                make_finding(
                    family="stale_items",
                    severity="warning",
                    scope_kind="domain",
                    scope_key=domain,
                    check_type="stale_active_item",
                    summary=f"active {item_type} item is stale at {age_days} days old",
                    supporting_refs=[build_item_ref(item)],
                )
            )
    return findings


def audit_domain_provenance(domain: str, items: list[dict[str, object]]) -> list[AuditFinding]:
    findings: list[AuditFinding] = []
    for item in items:
        if item.get("provenance_refs"):
            continue
        findings.append(
            make_finding(
                family="provenance_gaps",
                severity="error",
                scope_kind="domain",
                scope_key=domain,
                check_type="missing_item_provenance",
                summary=f"extracted item {item.get('item_key', 'unknown')} is missing provenance_refs",
                supporting_refs=[build_item_ref(item)],
            )
        )
    return findings


def audit_domain_wiki_quality(domain: str, items: list[dict[str, object]], config: AuditConfig) -> list[AuditFinding]:
    findings: list[AuditFinding] = []
    for item in items:
        item_type = str(item.get("item_type", ""))
        blockers = [str(blocker) for blocker in item.get("promotion_blockers", []) if str(blocker)]
        if item_type in config.transient_rule_item_types and bool(item.get("wiki_eligible")) and blockers:
            findings.append(
                make_finding(
                    family="wiki_quality",
                    severity="error",
                    scope_kind="domain",
                    scope_key=domain,
                    check_type="transient_rule_item",
                    summary=f"wiki-eligible {item_type} item still carries transient blockers",
                    supporting_refs=[build_item_ref(item)],
                )
            )
        if item_type in config.transient_rule_item_types and (
            "schema_label_fragment" in blockers or str(item.get("durability_class", "")) == "schema_scaffold"
        ):
            findings.append(
                make_finding(
                    family="wiki_quality",
                    severity="warning",
                    scope_kind="domain",
                    scope_key=domain,
                    check_type="schema_noise_item",
                    summary=f"{item_type} item appears to be schema or formatting noise",
                    supporting_refs=[build_item_ref(item)],
                )
            )
    return findings


def audit_page_duplicates(page_id: str, manifest: dict[str, object]) -> list[AuditFinding]:
    claims = [claim for claim in manifest.get("synthesized_claims", []) if isinstance(claim, dict)]
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for claim in claims:
        grouped[normalize_text(str(claim.get("text", "")))].append(claim)
    findings: list[AuditFinding] = []
    for normalized_text, group in grouped.items():
        if len(group) < 2 or not normalized_text:
            continue
        findings.append(
            make_finding(
                family="duplicates",
                severity="warning",
                scope_kind="page",
                scope_key=page_id,
                check_type="duplicate_page_claims",
                summary=f"page contains duplicate synthesized claims for text {normalized_text[:60]}",
                supporting_refs=[
                    {"page_id": page_id, "claim_id": str(claim.get("claim_id", ""))}
                    for claim in sorted(group, key=lambda entry: str(entry.get("claim_id", "")))
                ],
            )
        )
    return findings


def audit_page_provenance(page_id: str, manifest: dict[str, object]) -> list[AuditFinding]:
    valid_item_ids = {str(item) for item in manifest.get("input_item_keys", [])}
    findings: list[AuditFinding] = []
    for claim in manifest.get("synthesized_claims", []):
        if not isinstance(claim, dict):
            continue
        claim_id = str(claim.get("claim_id", ""))
        supporting_item_ids = [str(item) for item in claim.get("supporting_item_ids", []) if str(item)]
        unknown_items = sorted(set(supporting_item_ids) - valid_item_ids)
        if not supporting_item_ids or unknown_items or not claim.get("provenance_refs"):
            findings.append(
                make_finding(
                    family="provenance_gaps",
                    severity="error",
                    scope_kind="page",
                    scope_key=page_id,
                    check_type="invalid_page_claim_provenance",
                    summary=f"wiki claim {claim_id or 'unknown'} has unresolved supporting items or provenance",
                    supporting_refs=[
                        {"page_id": page_id, "claim_id": claim_id, "unknown_item_ids": unknown_items}
                    ],
                )
            )
    return findings


def audit_page_quality(
    page_id: str,
    manifest: dict[str, object],
    markdown: str,
    state_record: WikiStateRecord,
    config: AuditConfig,
) -> list[AuditFinding]:
    findings: list[AuditFinding] = []
    canonical_item_count = len(manifest.get("input_item_keys", []))
    if canonical_item_count == 0:
        findings.append(
            make_finding(
                family="wiki_quality",
                severity="error",
                scope_kind="page",
                scope_key=page_id,
                check_type="empty_wiki_page",
                summary="rendered wiki page has zero canonical items",
                supporting_refs=[{"page_id": page_id}],
            )
        )
    page_size = len(markdown.encode("utf-8"))
    page_cap = page_size_cap_for(state_record, config)
    if page_cap and page_size > page_cap:
        findings.append(
            make_finding(
                family="wiki_quality",
                severity="error" if page_size > (page_cap * 2) else "warning",
                scope_kind="page",
                scope_key=page_id,
                check_type="oversized_wiki_page",
                summary=f"rendered wiki page exceeds size cap at {page_size} bytes",
                supporting_refs=[{"page_id": page_id, "page_size": page_size, "page_cap": page_cap}],
            )
        )
    for claim in manifest.get("synthesized_claims", []):
        if not isinstance(claim, dict):
            continue
        normalized = normalize_text(str(claim.get("text", "")))
        if any(pattern in normalized for pattern in config.generic_claim_patterns):
            findings.append(
                make_finding(
                    family="wiki_quality",
                    severity="warning",
                    scope_kind="page",
                    scope_key=page_id,
                    check_type="generic_wiki_claim",
                    summary=f"wiki claim {claim.get('claim_id', 'unknown')} looks generic or filler-like",
                    supporting_refs=[{"page_id": page_id, "claim_id": str(claim.get("claim_id", ""))}],
                )
            )
    return findings


def audit_bootstrap_duplicates(domain: str, manifest: dict[str, object]) -> list[AuditFinding]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for bullet in manifest.get("bullets", []):
        if not isinstance(bullet, dict):
            continue
        grouped[normalize_text(str(bullet.get("text", "")))].append(bullet)
    findings: list[AuditFinding] = []
    for normalized_text, group in grouped.items():
        if len(group) < 2 or not normalized_text:
            continue
        findings.append(
            make_finding(
                family="duplicates",
                severity="warning",
                scope_kind="bootstrap_domain",
                scope_key=domain,
                check_type="duplicate_bootstrap_bullets",
                summary=f"bootstrap contains duplicate bullets for text {normalized_text[:60]}",
                supporting_refs=[
                    {"domain": domain, "bullet_id": str(bullet.get("bullet_id", ""))}
                    for bullet in sorted(group, key=lambda entry: str(entry.get("bullet_id", "")))
                ],
            )
        )
    return findings


def audit_bootstrap_provenance(
    domain: str,
    manifest: dict[str, object],
    current_items: list[dict[str, object]],
    current_claims: list[dict[str, object]],
) -> list[AuditFinding]:
    valid_item_ids = {str(item.get("item_key", "")) for item in current_items}
    valid_claim_ids = {str(claim.get("claim_id", "")) for claim in current_claims}
    findings: list[AuditFinding] = []
    for bullet in manifest.get("bullets", []):
        if not isinstance(bullet, dict):
            continue
        bullet_id = str(bullet.get("bullet_id", ""))
        supporting_item_keys = [str(item) for item in bullet.get("supporting_item_keys", []) if str(item)]
        supporting_claim_ids = [str(item) for item in bullet.get("supporting_claim_ids", []) if str(item)]
        unknown_item_ids = sorted(set(supporting_item_keys) - valid_item_ids)
        unknown_claim_ids = sorted(set(supporting_claim_ids) - valid_claim_ids)
        if not supporting_item_keys or unknown_item_ids or unknown_claim_ids:
            findings.append(
                make_finding(
                    family="provenance_gaps",
                    severity="error",
                    scope_kind="bootstrap_domain",
                    scope_key=domain,
                    check_type="invalid_bootstrap_bullet_refs",
                    summary=f"bootstrap bullet {bullet_id or 'unknown'} references missing current inputs",
                    supporting_refs=[
                        {
                            "domain": domain,
                            "bullet_id": bullet_id,
                            "unknown_item_ids": unknown_item_ids,
                            "unknown_claim_ids": unknown_claim_ids,
                        }
                    ],
                )
            )
    return findings


def audit_bootstrap_drift(
    domain: str,
    manifest: dict[str, object],
    state_record: BootstrapStateRecord,
    current_packet: BootstrapPacket | None,
    current_items: list[dict[str, object]],
    current_claims: list[dict[str, object]],
    config: AuditConfig,
) -> list[AuditFinding]:
    findings: list[AuditFinding] = []
    current_item_map = {str(item.get("item_key", "")): item for item in current_items}
    current_claim_map = {str(claim.get("claim_id", "")): claim for claim in current_claims}
    if current_packet is None:
        findings.append(
            make_finding(
                family="wiki_bootstrap_drift",
                severity="warning",
                scope_kind="bootstrap_domain",
                scope_key=domain,
                check_type="bootstrap_domain_not_in_current_plan",
                summary="bootstrap domain no longer resolves under the current bootstrap configuration",
                supporting_refs=[{"domain": domain}],
            )
        )
        return findings

    current_digest = packet_digest(current_packet)
    if state_record.input_digest != current_digest:
        findings.append(
            make_finding(
                family="wiki_bootstrap_drift",
                severity="warning",
                scope_kind="bootstrap_domain",
                scope_key=domain,
                check_type="bootstrap_packet_digest_mismatch",
                summary="bootstrap manifest is out of sync with the current selection packet",
                supporting_refs=[{"domain": domain, "stored_digest": state_record.input_digest, "current_digest": current_digest}],
            )
        )

    manifest_input_item_keys = {str(item) for item in dict(manifest.get("packet", {})).get("input_item_keys", [])}
    omitted_item_keys = sorted(set(current_packet.input_item_keys) - manifest_input_item_keys)
    if omitted_item_keys:
        findings.append(
            make_finding(
                family="wiki_bootstrap_drift",
                severity="warning",
                scope_kind="bootstrap_domain",
                scope_key=domain,
                check_type="bootstrap_missing_ranked_items",
                summary=f"bootstrap is missing {len(omitted_item_keys)} current high-priority packet items",
                supporting_refs=[{"domain": domain, "item_key": item_key} for item_key in omitted_item_keys[:10]],
            )
        )

    for bullet in manifest.get("bullets", []):
        if not isinstance(bullet, dict):
            continue
        bullet_id = str(bullet.get("bullet_id", ""))
        supporting_claim_ids = [str(item) for item in bullet.get("supporting_claim_ids", []) if str(item)]
        missing_claim_ids = [claim_id for claim_id in supporting_claim_ids if claim_id not in current_claim_map]
        if missing_claim_ids:
            findings.append(
                make_finding(
                    family="wiki_bootstrap_drift",
                    severity="error",
                    scope_kind="bootstrap_domain",
                    scope_key=domain,
                    check_type="bootstrap_references_removed_claim",
                    summary=f"bootstrap bullet {bullet_id or 'unknown'} references removed wiki claims",
                    supporting_refs=[{"domain": domain, "bullet_id": bullet_id, "missing_claim_ids": missing_claim_ids}],
                )
            )
        for claim_id in supporting_claim_ids:
            claim = current_claim_map.get(claim_id)
            if claim is None:
                continue
            supporting_item_ids = [str(item) for item in claim.get("supporting_item_ids", []) if str(item)]
            if not set(supporting_item_ids).issubset(set(current_item_map)):
                findings.append(
                    make_finding(
                        family="wiki_bootstrap_drift",
                        severity="error",
                        scope_kind="bootstrap_domain",
                        scope_key=domain,
                        check_type="bootstrap_claim_support_missing_items",
                        summary=f"bootstrap bullet {bullet_id or 'unknown'} references a wiki claim with missing supporting items",
                        supporting_refs=[{"domain": domain, "bullet_id": bullet_id, "claim_id": claim_id}],
                    )
                )

        supporting_items = [
            current_item_map[item_key]
            for item_key in bullet.get("supporting_item_keys", [])
            if item_key in current_item_map
        ]
        if supporting_items and all(str(item.get("confidence", "")) == "inferred" for item in supporting_items):
            stronger_replacement = False
            for item in supporting_items:
                item_type = str(item.get("item_type", ""))
                subject_key = str(item.get("subject_key", ""))
                for candidate in current_items:
                    if str(candidate.get("item_type", "")) != item_type:
                        continue
                    if str(candidate.get("subject_key", "")) != subject_key:
                        continue
                    if str(candidate.get("confidence", "")) not in config.strong_confidences:
                        continue
                    if str(candidate.get("item_key", "")) in bullet.get("supporting_item_keys", []):
                        continue
                    if str(candidate.get("item_key", "")) not in current_packet.input_item_keys:
                        continue
                    stronger_replacement = True
                    break
                if stronger_replacement:
                    break
            if stronger_replacement:
                findings.append(
                    make_finding(
                        family="wiki_bootstrap_drift",
                        severity="warning",
                        scope_kind="bootstrap_domain",
                        scope_key=domain,
                        check_type="inferred_bootstrap_replaced_by_stronger_item",
                        summary=f"bootstrap bullet {bullet_id or 'unknown'} is inferred-only while stronger current evidence now exists",
                        supporting_refs=[{"domain": domain, "bullet_id": bullet_id}],
                    )
                )
    return findings


def build_scope_state_records(
    scope: dict[str, list[str]],
    config: AuditConfig,
    domain_items_map: dict[str, list[dict[str, object]]],
    page_manifests: dict[str, dict[str, object]],
    bootstrap_manifests: dict[str, dict[str, object]],
    merged_findings: dict[str, list[AuditFinding]],
    current_packets: dict[str, BootstrapPacket],
    run_id: str,
) -> list[AuditStateRecord]:
    records: list[AuditStateRecord] = []
    for domain in scope["domains"]:
        records.append(
            build_scope_record(
                scope_kind="domain",
                scope_key=domain,
                config=config,
                input_digest=hash_payload(domain_items_map.get(domain, [])),
                findings=scope_findings(merged_findings, "domain", domain),
                run_id=run_id,
            )
        )
    for page_id in scope["pages"]:
        records.append(
            build_scope_record(
                scope_kind="page",
                scope_key=page_id,
                config=config,
                input_digest=hash_payload(page_manifests[page_id]),
                findings=scope_findings(merged_findings, "page", page_id),
                run_id=run_id,
            )
        )
    for domain in scope["bootstrap_domains"]:
        payload = {
            "manifest": bootstrap_manifests[domain],
            "packet_digest": packet_digest(current_packets[domain]) if domain in current_packets else "",
        }
        records.append(
            build_scope_record(
                scope_kind="bootstrap_domain",
                scope_key=domain,
                config=config,
                input_digest=hash_payload(payload),
                findings=scope_findings(merged_findings, "bootstrap_domain", domain),
                run_id=run_id,
            )
        )
    return records


def build_scope_record(
    scope_kind: str,
    scope_key: str,
    config: AuditConfig,
    input_digest: str,
    findings: list[AuditFinding],
    run_id: str,
) -> AuditStateRecord:
    return AuditStateRecord(
        scope_kind=scope_kind,
        scope_key=scope_key,
        audit_schema_version=AUDIT_SCHEMA_VERSION,
        rules_version=config.rules_version,
        input_digest=input_digest,
        finding_counts=dict(sorted(Counter(finding.family for finding in findings).items())),
        severity_counts=dict(sorted(Counter(finding.severity for finding in findings).items())),
        status="audited",
        last_audited_at=utc_now(),
        last_run_id=run_id,
    )


def merge_findings(
    previous_family_texts: dict[str, str],
    current_findings: dict[str, list[AuditFinding]],
    scoped_keys: set[tuple[str, str]],
    *,
    full_run: bool,
) -> dict[str, list[AuditFinding]]:
    merged: dict[str, list[AuditFinding]] = {}
    for family in FAMILY_FILENAMES:
        previous = [] if full_run else parse_findings_jsonl(previous_family_texts[family])
        preserved = [
            finding
            for finding in previous
            if (finding.scope_kind, finding.scope_key) not in scoped_keys
        ]
        merged[family] = sorted(
            dedupe_findings([*preserved, *current_findings[family]]),
            key=lambda finding: (finding.scope_kind, finding.scope_key, finding.finding_id),
        )
    return merged


def validate_audit_state(
    audit_state: dict[str, AuditStateRecord],
    merged_findings: dict[str, list[AuditFinding]],
    scope: dict[str, list[str]],
) -> None:
    expected_keys = {
        *(f"domain:{domain}" for domain in scope["domains"]),
        *(f"page:{page_id}" for page_id in scope["pages"]),
        *(f"bootstrap_domain:{domain}" for domain in scope["bootstrap_domains"]),
    }
    missing = sorted(expected_keys - set(audit_state))
    if missing:
        raise AuditError(f"Audit state is missing targets: {', '.join(missing[:5])}")
    validate_family_and_state_alignment(merged_findings, audit_state)


def validate_family_and_state_alignment(
    merged_findings: dict[str, list[AuditFinding]],
    audit_state: dict[str, AuditStateRecord],
) -> None:
    findings_by_scope: dict[tuple[str, str], list[AuditFinding]] = defaultdict(list)
    for findings in merged_findings.values():
        for finding in findings:
            findings_by_scope[(finding.scope_kind, finding.scope_key)].append(finding)
    for record in audit_state.values():
        scoped_findings = findings_by_scope.get((record.scope_kind, record.scope_key), [])
        family_counts = dict(sorted(Counter(finding.family for finding in scoped_findings).items()))
        severity_counts = dict(sorted(Counter(finding.severity for finding in scoped_findings).items()))
        if family_counts != dict(sorted(record.finding_counts.items())):
            raise AuditError(f"Audit state family counts mismatch for {record.record_key}")
        if severity_counts != dict(sorted(record.severity_counts.items())):
            raise AuditError(f"Audit state severity counts mismatch for {record.record_key}")


def build_state_payload(state_records: dict[str, AuditStateRecord]) -> dict[str, object]:
    return {
        "schema_version": STATE_SCHEMA_VERSION,
        "audit_schema_version": AUDIT_SCHEMA_VERSION,
        "generated_at": utc_now(),
        "target_count": len(state_records),
        "targets": [state_records[key].to_dict() for key in sorted(state_records)],
    }


def render_findings_jsonl(findings: list[AuditFinding]) -> str:
    if not findings:
        return ""
    return "".join(json.dumps(finding.to_dict(), sort_keys=True) + "\n" for finding in findings)


def parse_findings_jsonl(text: str) -> list[AuditFinding]:
    records: list[AuditFinding] = []
    for line in text.splitlines():
        if not line.strip():
            continue
        payload = json.loads(line)
        records.append(
            AuditFinding(
                finding_id=str(payload["finding_id"]),
                family=str(payload["family"]),
                severity=str(payload["severity"]),
                scope_kind=str(payload["scope_kind"]),
                scope_key=str(payload["scope_key"]),
                check_type=str(payload["check_type"]),
                summary=str(payload["summary"]),
                supporting_refs=tuple(dict(ref) for ref in payload.get("supporting_refs", []) if isinstance(ref, dict)),
            )
        )
    return records


def read_json_required(path: Path) -> dict[str, object]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError as exc:
        raise AuditError(f"Missing JSON artifact: {path}") from exc
    except json.JSONDecodeError as exc:
        raise AuditError(f"Invalid JSON artifact: {path}") from exc
    if not isinstance(payload, dict):
        raise AuditError(f"JSON artifact root must be an object: {path}")
    return payload


def read_jsonl_required(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        raise AuditError(f"Missing JSONL artifact: {path}")
    records: list[dict[str, object]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError as exc:
            raise AuditError(f"Invalid JSONL artifact line {line_no}: {path}") from exc
        if not isinstance(payload, dict):
            raise AuditError(f"JSONL artifact line {line_no} is not an object: {path}")
        records.append(payload)
    return records


def scope_findings(
    merged_findings: dict[str, list[AuditFinding]],
    scope_kind: str,
    scope_key: str,
) -> list[AuditFinding]:
    return [
        finding
        for findings in merged_findings.values()
        for finding in findings
        if finding.scope_kind == scope_kind and finding.scope_key == scope_key
    ]


def make_finding(
    *,
    family: str,
    severity: str,
    scope_kind: str,
    scope_key: str,
    check_type: str,
    summary: str,
    supporting_refs: list[dict[str, object]],
) -> AuditFinding:
    if severity not in VALID_SEVERITIES:
        raise AuditError(f"Unsupported audit severity: {severity}")
    payload = {
        "family": family,
        "severity": severity,
        "scope_kind": scope_kind,
        "scope_key": scope_key,
        "check_type": check_type,
        "summary": summary,
        "supporting_refs": supporting_refs,
    }
    digest = hashlib.sha1(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()[:16]
    return AuditFinding(
        finding_id=f"{family}:{digest}",
        family=family,
        severity=severity,
        scope_kind=scope_kind,
        scope_key=scope_key,
        check_type=check_type,
        summary=summary,
        supporting_refs=tuple(supporting_refs),
    )


def build_item_ref(item: dict[str, object]) -> dict[str, object]:
    return {
        "item_key": str(item.get("item_key", "")),
        "item_type": str(item.get("item_type", "")),
        "subject_key": str(item.get("subject_key", "")),
        "confidence": str(item.get("confidence", "")),
        "temporal_status": str(item.get("temporal_status", "")),
        "last_seen_at": str(item.get("last_seen_at", "")),
    }


def hash_payload(payload: Any) -> str:
    return hashlib.sha1(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def parse_iso_timestamp(value: str) -> datetime | None:
    if not value:
        return None
    normalized = value.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def normalize_text(text: str) -> str:
    return NORMALIZE_TEXT_PATTERN.sub(" ", str(text).strip().lower())


def normalize_subject_key(text: str) -> str:
    return normalize_text(text).strip("- ").strip()


def page_size_cap_for(state_record: WikiStateRecord, config: AuditConfig) -> int:
    if state_record.page_type == "domain_index":
        return int(config.page_size_caps.get("index", 25 * 1024))
    return int(
        config.page_size_caps.get(
            state_record.bucket,
            config.page_size_caps.get("default_bucket", 200 * 1024),
        )
    )


def dedupe_preserving_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        ordered.append(item)
    return ordered


def dedupe_findings(findings: list[AuditFinding]) -> list[AuditFinding]:
    seen: set[str] = set()
    deduped: list[AuditFinding] = []
    for finding in findings:
        if finding.finding_id in seen:
            continue
        seen.add(finding.finding_id)
        deduped.append(finding)
    return deduped


def write_text(path: Path, text: str) -> None:
    ensure_directory(path.parent)
    path.write_text(text, encoding="utf-8", newline="\n")


def cleanup_staging_root(staging_root: Path) -> None:
    if staging_root.exists():
        shutil.rmtree(staging_root, ignore_errors=True)
