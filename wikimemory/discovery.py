from __future__ import annotations

import hashlib
import json
import os
import re
from collections import Counter
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import BinaryIO

SCHEMA_VERSION = 1
SAMPLED_HASH_BYTES = 64 * 1024
ENV_PATTERN = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)(?::-([^}]*))?\}")
SESSION_ID_PATTERN = re.compile(
    r"([0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12})\.jsonl$"
)


class DiscoveryError(RuntimeError):
    """Fatal discovery error that must stop the run."""


@dataclass(frozen=True, order=True)
class LocatorRef:
    root_alias: str
    relative_path: str

    def to_dict(self) -> dict[str, str]:
        return {
            "root_alias": self.root_alias,
            "relative_path": self.relative_path,
        }

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "LocatorRef":
        return cls(
            root_alias=data["root_alias"],
            relative_path=data["relative_path"],
        )


@dataclass
class SourceRootConfig:
    root_alias: str
    absolute_path: str
    enabled: bool = True
    recursive: bool = True
    include_glob: str = "**/*.jsonl"

    @property
    def resolved_path(self) -> Path:
        expanded = expand_env_template(self.absolute_path)
        return Path(expanded).expanduser()

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "SourceRootConfig":
        return cls(
            root_alias=str(data["root_alias"]),
            absolute_path=str(data["absolute_path"]),
            enabled=bool(data.get("enabled", True)),
            recursive=bool(data.get("recursive", True)),
            include_glob=str(data.get("include_glob", "**/*.jsonl")),
        )


@dataclass
class SourceLocator:
    root_alias: str
    relative_path: str
    first_seen_at: str
    last_seen_at: str
    locator_state: str

    def ref(self) -> LocatorRef:
        return LocatorRef(self.root_alias, self.relative_path)

    def to_dict(self) -> dict[str, str]:
        return {
            "root_alias": self.root_alias,
            "relative_path": self.relative_path,
            "first_seen_at": self.first_seen_at,
            "last_seen_at": self.last_seen_at,
            "locator_state": self.locator_state,
        }

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "SourceLocator":
        return cls(
            root_alias=data["root_alias"],
            relative_path=data["relative_path"],
            first_seen_at=data["first_seen_at"],
            last_seen_at=data["last_seen_at"],
            locator_state=data["locator_state"],
        )


@dataclass(frozen=True)
class SampledFingerprint:
    algorithm: str
    committed_length: int
    prefix_length: int
    suffix_length: int
    digest: str

    def to_dict(self) -> dict[str, object]:
        return {
            "algorithm": self.algorithm,
            "committed_length": self.committed_length,
            "prefix_length": self.prefix_length,
            "suffix_length": self.suffix_length,
            "digest": self.digest,
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "SampledFingerprint":
        return cls(
            algorithm=str(data["algorithm"]),
            committed_length=int(data["committed_length"]),
            prefix_length=int(data["prefix_length"]),
            suffix_length=int(data["suffix_length"]),
            digest=str(data["digest"]),
        )


@dataclass
class SourceRecord:
    source_id: str
    filename_session_id: str
    status: str
    preferred_locator: LocatorRef
    first_seen_at: str
    last_seen_at: str
    size_bytes: int
    mtime_utc: str
    sampled_fingerprint: SampledFingerprint
    committed_byte_end: int
    committed_line_count: int
    uncommitted_tail_bytes: int
    first_line_verified: bool
    last_error: str | None
    locators: list[SourceLocator] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return {
            "source_id": self.source_id,
            "filename_session_id": self.filename_session_id,
            "status": self.status,
            "preferred_locator": self.preferred_locator.to_dict(),
            "first_seen_at": self.first_seen_at,
            "last_seen_at": self.last_seen_at,
            "size_bytes": self.size_bytes,
            "mtime_utc": self.mtime_utc,
            "sampled_fingerprint": self.sampled_fingerprint.to_dict(),
            "committed_byte_end": self.committed_byte_end,
            "committed_line_count": self.committed_line_count,
            "uncommitted_tail_bytes": self.uncommitted_tail_bytes,
            "first_line_verified": self.first_line_verified,
            "last_error": self.last_error,
            "locators": [locator.to_dict() for locator in sorted(self.locators, key=_locator_sort_key)],
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "SourceRecord":
        locators = [
            SourceLocator.from_dict(locator)
            for locator in data.get("locators", [])
        ]
        return cls(
            source_id=str(data["source_id"]),
            filename_session_id=str(data["filename_session_id"]),
            status=str(data["status"]),
            preferred_locator=LocatorRef.from_dict(data["preferred_locator"]),
            first_seen_at=str(data["first_seen_at"]),
            last_seen_at=str(data["last_seen_at"]),
            size_bytes=int(data["size_bytes"]),
            mtime_utc=str(data["mtime_utc"]),
            sampled_fingerprint=SampledFingerprint.from_dict(data["sampled_fingerprint"]),
            committed_byte_end=int(data["committed_byte_end"]),
            committed_line_count=int(data["committed_line_count"]),
            uncommitted_tail_bytes=int(data["uncommitted_tail_bytes"]),
            first_line_verified=bool(data["first_line_verified"]),
            last_error=data.get("last_error"),
            locators=locators,
        )


@dataclass
class DiscoveryRunReport:
    run_id: str
    started_at: str
    finished_at: str
    scanned_file_count: int
    status_counts: dict[str, int]
    success: bool
    fatal_error_summary: str | None

    def to_dict(self) -> dict[str, object]:
        return {
            "run_id": self.run_id,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "scanned_file_count": self.scanned_file_count,
            "status_counts": self.status_counts,
            "success": self.success,
            "fatal_error_summary": self.fatal_error_summary,
        }


@dataclass
class DiscoveryResult:
    report: DiscoveryRunReport
    registry_path: Path
    run_log_path: Path


@dataclass(frozen=True)
class FileObservation:
    source_id: str
    filename_session_id: str
    locator: LocatorRef
    absolute_path: Path
    size_bytes: int
    mtime_utc: str


@dataclass(frozen=True)
class MaterializedState:
    status: str
    size_bytes: int
    mtime_utc: str
    committed_byte_end: int
    committed_line_count: int
    uncommitted_tail_bytes: int
    sampled_fingerprint: SampledFingerprint
    first_line_verified: bool


def run_discovery(config_path: Path | str, state_dir: Path | str) -> DiscoveryResult:
    config_path = Path(config_path)
    state_dir = Path(state_dir)
    registry_path = state_dir / "source_registry.json"
    run_log_path = state_dir / "discovery_runs.jsonl"

    ensure_directory(state_dir)

    run_id = datetime.now(UTC).strftime("run-%Y%m%dT%H%M%S-%fZ")
    started_at = utc_now()

    try:
        roots = load_source_roots(config_path)
        previous_registry = load_registry(registry_path)
        current_registry, scanned_file_count = build_registry(roots, previous_registry)
        validate_registry(current_registry)

        status_counts = dict(sorted(Counter(record.status for record in current_registry.values()).items()))
        report = DiscoveryRunReport(
            run_id=run_id,
            started_at=started_at,
            finished_at=utc_now(),
            scanned_file_count=scanned_file_count,
            status_counts=status_counts,
            success=True,
            fatal_error_summary=None,
        )
        write_registry_atomic(registry_path, current_registry)
        append_run_report_atomic(run_log_path, report)
        return DiscoveryResult(report=report, registry_path=registry_path, run_log_path=run_log_path)
    except DiscoveryError as exc:
        report = DiscoveryRunReport(
            run_id=run_id,
            started_at=started_at,
            finished_at=utc_now(),
            scanned_file_count=0,
            status_counts={},
            success=False,
            fatal_error_summary=str(exc),
        )
        append_run_report_atomic(run_log_path, report)
        return DiscoveryResult(report=report, registry_path=registry_path, run_log_path=run_log_path)


def build_registry(
    roots: list[SourceRootConfig],
    previous_registry: dict[str, SourceRecord],
) -> tuple[dict[str, SourceRecord], int]:
    observations_by_source: dict[str, list[FileObservation]] = {}
    scanned_file_count = 0

    for root in roots:
        resolved_root = root.resolved_path
        if not resolved_root.exists():
            raise DiscoveryError(
                f"Configured source root '{root.root_alias}' does not exist: {resolved_root}"
            )
        if not resolved_root.is_dir():
            raise DiscoveryError(
                f"Configured source root '{root.root_alias}' is not a directory: {resolved_root}"
            )

        for absolute_path in sorted(resolved_root.rglob("*.jsonl")):
            if not absolute_path.is_file():
                continue
            relative_path = absolute_path.relative_to(resolved_root).as_posix()
            source_id, filename_session_id = read_and_verify_first_line(absolute_path)
            stat = absolute_path.stat()
            observation = FileObservation(
                source_id=source_id,
                filename_session_id=filename_session_id,
                locator=LocatorRef(root_alias=root.root_alias, relative_path=relative_path),
                absolute_path=absolute_path,
                size_bytes=stat.st_size,
                mtime_utc=to_utc(stat.st_mtime),
            )
            observations_by_source.setdefault(source_id, []).append(observation)
            scanned_file_count += 1

    now = utc_now()
    next_registry: dict[str, SourceRecord] = {}

    for source_id, observations in sorted(observations_by_source.items()):
        previous = previous_registry.get(source_id)
        preferred = choose_preferred_observation(observations, previous)
        preferred_state = materialize_state(
            observation=preferred,
            previous=previous,
            allow_fast_path=True,
        )

        duplicate_locators: list[SourceLocator] = []
        for observation in observations:
            if observation.locator == preferred.locator:
                continue
            duplicate_state = materialize_state(
                observation=observation,
                previous=previous,
                allow_fast_path=False,
            )
            ensure_duplicate_compatibility(
                source_id=source_id,
                preferred_state=preferred_state,
                duplicate_state=duplicate_state,
            )
            duplicate_locators.append(
                SourceLocator(
                    root_alias=observation.locator.root_alias,
                    relative_path=observation.locator.relative_path,
                    first_seen_at=first_seen_at_for_locator(previous, observation.locator, now),
                    last_seen_at=now,
                    locator_state="duplicate",
                )
            )

        locators = merge_locators(previous, preferred.locator, duplicate_locators, now)
        next_registry[source_id] = SourceRecord(
            source_id=source_id,
            filename_session_id=preferred.filename_session_id,
            status=preferred_state.status,
            preferred_locator=preferred.locator,
            first_seen_at=previous.first_seen_at if previous else now,
            last_seen_at=now,
            size_bytes=preferred_state.size_bytes,
            mtime_utc=preferred_state.mtime_utc,
            sampled_fingerprint=preferred_state.sampled_fingerprint,
            committed_byte_end=preferred_state.committed_byte_end,
            committed_line_count=preferred_state.committed_line_count,
            uncommitted_tail_bytes=preferred_state.uncommitted_tail_bytes,
            first_line_verified=preferred_state.first_line_verified,
            last_error=None,
            locators=locators,
        )

    missing_source_ids = sorted(set(previous_registry) - set(observations_by_source))
    for source_id in missing_source_ids:
        previous = previous_registry[source_id]
        tombstoned_locators = [
            SourceLocator(
                root_alias=locator.root_alias,
                relative_path=locator.relative_path,
                first_seen_at=locator.first_seen_at,
                last_seen_at=locator.last_seen_at,
                locator_state="missing",
            )
            for locator in previous.locators
        ]
        next_registry[source_id] = SourceRecord(
            source_id=previous.source_id,
            filename_session_id=previous.filename_session_id,
            status="tombstoned",
            preferred_locator=previous.preferred_locator,
            first_seen_at=previous.first_seen_at,
            last_seen_at=previous.last_seen_at,
            size_bytes=previous.size_bytes,
            mtime_utc=previous.mtime_utc,
            sampled_fingerprint=previous.sampled_fingerprint,
            committed_byte_end=previous.committed_byte_end,
            committed_line_count=previous.committed_line_count,
            uncommitted_tail_bytes=previous.uncommitted_tail_bytes,
            first_line_verified=previous.first_line_verified,
            last_error=previous.last_error,
            locators=sorted(tombstoned_locators, key=_locator_sort_key),
        )

    return next_registry, scanned_file_count


def choose_preferred_observation(
    observations: list[FileObservation],
    previous: SourceRecord | None,
) -> FileObservation:
    if previous:
        for observation in observations:
            if observation.locator == previous.preferred_locator:
                return observation
    return min(observations, key=lambda item: (item.locator.root_alias, item.locator.relative_path))


def materialize_state(
    observation: FileObservation,
    previous: SourceRecord | None,
    allow_fast_path: bool,
) -> MaterializedState:
    if previous is None:
        size_bytes, committed_byte_end, committed_line_count, uncommitted_tail_bytes = scan_complete_lines(
            observation.absolute_path,
            start_offset=0,
            start_line_count=0,
        )
        sampled_fingerprint = compute_sampled_fingerprint(
            observation.absolute_path,
            committed_length=committed_byte_end,
        )
        return MaterializedState(
            status="new",
            size_bytes=size_bytes,
            mtime_utc=observation.mtime_utc,
            committed_byte_end=committed_byte_end,
            committed_line_count=committed_line_count,
            uncommitted_tail_bytes=uncommitted_tail_bytes,
            sampled_fingerprint=sampled_fingerprint,
            first_line_verified=True,
        )

    if observation.size_bytes < previous.size_bytes:
        raise DiscoveryError(
            f"File shrank for source {previous.source_id}: {observation.locator.relative_path}"
        )
    if observation.size_bytes < previous.committed_byte_end:
        raise DiscoveryError(
            f"Committed checkpoint exceeds current size for source {previous.source_id}: "
            f"{observation.locator.relative_path}"
        )

    unchanged_locator = observation.locator == previous.preferred_locator
    if (
        allow_fast_path
        and unchanged_locator
        and observation.size_bytes == previous.size_bytes
        and observation.mtime_utc == previous.mtime_utc
    ):
        return MaterializedState(
            status="stable",
            size_bytes=previous.size_bytes,
            mtime_utc=previous.mtime_utc,
            committed_byte_end=previous.committed_byte_end,
            committed_line_count=previous.committed_line_count,
            uncommitted_tail_bytes=previous.uncommitted_tail_bytes,
            sampled_fingerprint=previous.sampled_fingerprint,
            first_line_verified=previous.first_line_verified,
        )

    current_fingerprint = compute_sampled_fingerprint(
        observation.absolute_path,
        committed_length=previous.committed_byte_end,
    )
    if current_fingerprint != previous.sampled_fingerprint:
        raise DiscoveryError(
            f"Committed content drift detected for source {previous.source_id}: "
            f"{observation.locator.relative_path}"
        )

    if observation.size_bytes == previous.size_bytes:
        return MaterializedState(
            status="stable",
            size_bytes=observation.size_bytes,
            mtime_utc=observation.mtime_utc,
            committed_byte_end=previous.committed_byte_end,
            committed_line_count=previous.committed_line_count,
            uncommitted_tail_bytes=previous.uncommitted_tail_bytes,
            sampled_fingerprint=previous.sampled_fingerprint,
            first_line_verified=True,
        )

    size_bytes, committed_byte_end, committed_line_count, uncommitted_tail_bytes = scan_complete_lines(
        observation.absolute_path,
        start_offset=previous.committed_byte_end,
        start_line_count=previous.committed_line_count,
    )
    sampled_fingerprint = compute_sampled_fingerprint(
        observation.absolute_path,
        committed_length=committed_byte_end,
    )
    return MaterializedState(
        status="growing",
        size_bytes=size_bytes,
        mtime_utc=observation.mtime_utc,
        committed_byte_end=committed_byte_end,
        committed_line_count=committed_line_count,
        uncommitted_tail_bytes=uncommitted_tail_bytes,
        sampled_fingerprint=sampled_fingerprint,
        first_line_verified=True,
    )


def ensure_duplicate_compatibility(
    source_id: str,
    preferred_state: MaterializedState,
    duplicate_state: MaterializedState,
) -> None:
    comparable_preferred = (
        preferred_state.size_bytes,
        preferred_state.committed_byte_end,
        preferred_state.committed_line_count,
        preferred_state.uncommitted_tail_bytes,
        preferred_state.sampled_fingerprint,
    )
    comparable_duplicate = (
        duplicate_state.size_bytes,
        duplicate_state.committed_byte_end,
        duplicate_state.committed_line_count,
        duplicate_state.uncommitted_tail_bytes,
        duplicate_state.sampled_fingerprint,
    )
    if comparable_preferred != comparable_duplicate:
        raise DiscoveryError(f"Conflicting duplicate detected for source {source_id}")


def merge_locators(
    previous: SourceRecord | None,
    preferred_locator: LocatorRef,
    duplicate_locators: list[SourceLocator],
    now: str,
) -> list[SourceLocator]:
    previous_map = {
        locator.ref(): locator
        for locator in previous.locators
    } if previous else {}

    merged = [
        SourceLocator(
            root_alias=preferred_locator.root_alias,
            relative_path=preferred_locator.relative_path,
            first_seen_at=first_seen_at_for_locator(previous, preferred_locator, now),
            last_seen_at=now,
            locator_state="active",
        )
    ]
    merged.extend(sorted(duplicate_locators, key=_locator_sort_key))

    seen_refs = {preferred_locator, *(locator.ref() for locator in duplicate_locators)}
    for ref, locator in sorted(previous_map.items(), key=lambda item: (item[0].root_alias, item[0].relative_path)):
        if ref in seen_refs:
            continue
        merged.append(
            SourceLocator(
                root_alias=locator.root_alias,
                relative_path=locator.relative_path,
                first_seen_at=locator.first_seen_at,
                last_seen_at=locator.last_seen_at,
                locator_state="missing",
            )
        )
    return merged


def first_seen_at_for_locator(
    previous: SourceRecord | None,
    locator_ref: LocatorRef,
    default_timestamp: str,
) -> str:
    if previous:
        for locator in previous.locators:
            if locator.ref() == locator_ref:
                return locator.first_seen_at
    return default_timestamp


def read_and_verify_first_line(path: Path) -> tuple[str, str]:
    filename_session_id = session_id_from_filename(path)
    with open_shared_binary(path) as handle:
        first_line = handle.readline()

    if not first_line:
        raise DiscoveryError(f"Empty source file: {path}")
    if not first_line.endswith(b"\n"):
        raise DiscoveryError(f"First line is incomplete: {path}")

    try:
        payload = json.loads(first_line.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise DiscoveryError(f"Invalid JSON in first line for {path}: {exc}") from exc

    if payload.get("type") != "session_meta":
        raise DiscoveryError(f"First line is not session_meta: {path}")
    session_id = payload.get("payload", {}).get("id")
    if not session_id:
        raise DiscoveryError(f"session_meta.payload.id is missing: {path}")
    if session_id.lower() != filename_session_id:
        raise DiscoveryError(
            f"Filename session id mismatch for {path}: {filename_session_id} != {session_id}"
        )
    return session_id.lower(), filename_session_id


def scan_complete_lines(path: Path, start_offset: int, start_line_count: int) -> tuple[int, int, int, int]:
    committed_byte_end = start_offset
    committed_line_count = start_line_count

    with open_shared_binary(path) as handle:
        handle.seek(start_offset)
        while True:
            line = handle.readline()
            if not line:
                break
            line_end = handle.tell()
            if line.endswith(b"\n"):
                committed_byte_end = line_end
                committed_line_count += 1
                continue
            handle.seek(0, os.SEEK_END)
            break
        file_size = handle.seek(0, os.SEEK_END)

    uncommitted_tail_bytes = file_size - committed_byte_end
    return file_size, committed_byte_end, committed_line_count, uncommitted_tail_bytes


def compute_sampled_fingerprint(path: Path, committed_length: int) -> SampledFingerprint:
    if committed_length < 0:
        raise DiscoveryError(f"Committed length cannot be negative: {path}")

    with open_shared_binary(path) as handle:
        prefix_length = min(SAMPLED_HASH_BYTES, committed_length)
        prefix = handle.read(prefix_length) if prefix_length else b""

        suffix_length = min(SAMPLED_HASH_BYTES, committed_length)
        if suffix_length:
            handle.seek(committed_length - suffix_length)
            suffix = handle.read(suffix_length)
        else:
            suffix = b""

    digest = hashlib.sha256()
    digest.update(str(committed_length).encode("ascii"))
    digest.update(b"\0")
    digest.update(prefix)
    digest.update(b"\0")
    digest.update(suffix)
    return SampledFingerprint(
        algorithm="sha256",
        committed_length=committed_length,
        prefix_length=prefix_length,
        suffix_length=suffix_length,
        digest=digest.hexdigest(),
    )


def validate_registry(registry: dict[str, SourceRecord]) -> None:
    seen_active_locators: dict[LocatorRef, str] = {}
    for source_id, record in registry.items():
        if record.source_id != source_id:
            raise DiscoveryError(f"Registry key mismatch for source {source_id}")
        if not record.first_line_verified:
            raise DiscoveryError(f"Unverified first line for source {source_id}")
        if record.committed_byte_end > record.size_bytes:
            raise DiscoveryError(f"Committed byte end exceeds size for source {source_id}")
        if record.uncommitted_tail_bytes != record.size_bytes - record.committed_byte_end:
            raise DiscoveryError(f"Uncommitted tail mismatch for source {source_id}")

        locator_refs = set()
        active_locator_count = 0
        for locator in record.locators:
            ref = locator.ref()
            if ref in locator_refs:
                raise DiscoveryError(f"Duplicate locator entry for source {source_id}: {ref}")
            locator_refs.add(ref)
            if locator.locator_state == "active":
                active_locator_count += 1
                if ref in seen_active_locators:
                    raise DiscoveryError(f"Active locator resolves to multiple sources: {ref}")
                seen_active_locators[ref] = source_id

        if record.status == "tombstoned":
            if active_locator_count != 0:
                raise DiscoveryError(f"Tombstoned source still has an active locator: {source_id}")
        elif active_locator_count != 1:
            raise DiscoveryError(f"Active locator cardinality mismatch for source {source_id}")


def load_source_roots(config_path: Path) -> list[SourceRootConfig]:
    try:
        payload = json.loads(config_path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError as exc:
        raise DiscoveryError(f"Missing config file: {config_path}") from exc
    except json.JSONDecodeError as exc:
        raise DiscoveryError(f"Invalid config JSON in {config_path}: {exc}") from exc

    roots = [SourceRootConfig.from_dict(root) for root in payload.get("roots", [])]
    enabled_roots = [root for root in roots if root.enabled]
    if not enabled_roots:
        raise DiscoveryError("No enabled source roots were configured")

    seen_aliases: set[str] = set()
    for root in enabled_roots:
        if root.root_alias in seen_aliases:
            raise DiscoveryError(f"Duplicate root alias detected: {root.root_alias}")
        seen_aliases.add(root.root_alias)
    return enabled_roots


def load_registry(registry_path: Path) -> dict[str, SourceRecord]:
    if not registry_path.exists():
        return {}

    try:
        payload = json.loads(registry_path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise DiscoveryError(f"Invalid registry JSON in {registry_path}: {exc}") from exc

    if payload.get("schema_version") != SCHEMA_VERSION:
        raise DiscoveryError(
            f"Unsupported registry schema version in {registry_path}: {payload.get('schema_version')}"
        )

    records = [
        SourceRecord.from_dict(record)
        for record in payload.get("sources", [])
    ]
    return {record.source_id: record for record in records}


def write_registry_atomic(registry_path: Path, registry: dict[str, SourceRecord]) -> None:
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "source_count": len(registry),
        "sources": [registry[source_id].to_dict() for source_id in sorted(registry)],
    }
    atomic_write_text(
        registry_path,
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
    )


def append_run_report_atomic(run_log_path: Path, report: DiscoveryRunReport) -> None:
    existing = ""
    if run_log_path.exists():
        existing = run_log_path.read_text(encoding="utf-8")
    line = json.dumps(report.to_dict(), sort_keys=True)
    if existing and not existing.endswith("\n"):
        existing += "\n"
    atomic_write_text(run_log_path, existing + line + "\n")


def atomic_write_text(path: Path, content: str) -> None:
    ensure_directory(path.parent)
    temp_path = path.with_suffix(path.suffix + ".tmp")
    temp_path.write_text(content, encoding="utf-8")
    os.replace(temp_path, path)


def ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def expand_env_template(value: str) -> str:
    def replace(match: re.Match[str]) -> str:
        variable_name = match.group(1)
        fallback = match.group(2)
        environment_value = os.environ.get(variable_name)
        if environment_value:
            return environment_value
        if fallback is not None:
            return fallback
        raise DiscoveryError(f"Missing required environment variable: {variable_name}")

    return ENV_PATTERN.sub(replace, value)


def session_id_from_filename(path: Path) -> str:
    match = SESSION_ID_PATTERN.search(path.name)
    if not match:
        raise DiscoveryError(f"Filename does not contain a valid session id: {path}")
    return match.group(1).lower()


def utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def to_utc(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp, UTC).isoformat().replace("+00:00", "Z")


def open_shared_binary(path: Path) -> BinaryIO:
    if os.name != "nt":
        return path.open("rb")

    import ctypes
    import msvcrt

    generic_read = 0x80000000
    file_share_read = 0x00000001
    file_share_write = 0x00000002
    file_share_delete = 0x00000004
    open_existing = 3
    file_attribute_normal = 0x00000080
    invalid_handle_value = ctypes.c_void_p(-1).value

    handle = ctypes.windll.kernel32.CreateFileW(
        str(path),
        generic_read,
        file_share_read | file_share_write | file_share_delete,
        None,
        open_existing,
        file_attribute_normal,
        None,
    )
    if handle == invalid_handle_value:
        raise DiscoveryError(f"Unable to open source file with shared-read access: {path}")

    try:
        file_descriptor = msvcrt.open_osfhandle(handle, os.O_RDONLY)
    except OSError as exc:
        ctypes.windll.kernel32.CloseHandle(handle)
        raise DiscoveryError(f"Unable to bridge source handle into Python IO: {path}") from exc
    return os.fdopen(file_descriptor, "rb", closefd=True)


def _locator_sort_key(locator: SourceLocator) -> tuple[str, str]:
    return locator.root_alias, locator.relative_path
