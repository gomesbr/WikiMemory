from __future__ import annotations

import hashlib
import json
from collections import OrderedDict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .discovery import DiscoveryError, SourceRecord, load_registry, load_source_roots, open_shared_binary

EVENT_DIGEST_ALGORITHM = "sha256"
DEFAULT_CACHE_SIZE = 512


class RawEventResolverError(DiscoveryError):
    """Fatal raw-event resolution error."""


@dataclass(frozen=True)
class ResolvedRawEvent:
    source_id: str
    source_byte_start: int
    source_byte_end: int
    event_digest: str
    raw_bytes: bytes
    raw_event: dict[str, Any]


def compute_event_digest(raw_bytes: bytes) -> str:
    return hashlib.sha256(raw_bytes).hexdigest()


class RawEventResolver:
    def __init__(
        self,
        *,
        registry: dict[str, SourceRecord],
        source_roots: dict[str, Path],
        max_cache_entries: int = DEFAULT_CACHE_SIZE,
    ) -> None:
        self._registry = dict(registry)
        self._source_roots = dict(source_roots)
        self._max_cache_entries = max(1, int(max_cache_entries))
        self._cache: OrderedDict[tuple[str, int, int], ResolvedRawEvent] = OrderedDict()

    @classmethod
    def from_paths(
        cls,
        *,
        registry_path: Path,
        source_roots_config_path: Path,
        max_cache_entries: int = DEFAULT_CACHE_SIZE,
    ) -> "RawEventResolver":
        registry = load_registry(registry_path)
        source_roots = {
            root.root_alias: root.resolved_path
            for root in load_source_roots(source_roots_config_path)
            if root.enabled
        }
        return cls(
            registry=registry,
            source_roots=source_roots,
            max_cache_entries=max_cache_entries,
        )

    def resolve_path(self, source_id: str) -> Path:
        source = self._registry.get(source_id)
        if source is None:
            raise RawEventResolverError(f"Unknown source_id for raw-event resolution: {source_id}")
        root_path = self._source_roots.get(source.preferred_locator.root_alias)
        if root_path is None:
            raise RawEventResolverError(
                f"Missing source root for alias {source.preferred_locator.root_alias}"
            )
        return root_path / Path(source.preferred_locator.relative_path)

    def hydrate_event(
        self,
        *,
        source_id: str,
        source_byte_start: int,
        source_byte_end: int,
        expected_digest: str | None = None,
    ) -> ResolvedRawEvent:
        key = (source_id, int(source_byte_start), int(source_byte_end))
        cached = self._cache.get(key)
        if cached is not None:
            self._cache.move_to_end(key)
            self._validate_expected_digest(cached.event_digest, expected_digest, source_id, source_byte_start, source_byte_end)
            return cached

        source = self._registry.get(source_id)
        if source is None:
            raise RawEventResolverError(f"Unknown source_id for raw-event resolution: {source_id}")
        if source_byte_start < 0 or source_byte_end <= source_byte_start:
            raise RawEventResolverError(
                f"Invalid raw-event byte range for source {source_id}: {source_byte_start}-{source_byte_end}"
            )
        if source_byte_end > source.committed_byte_end:
            raise RawEventResolverError(
                f"Raw-event byte range exceeds committed boundary for source {source_id}: {source_byte_end} > {source.committed_byte_end}"
            )

        raw_path = self.resolve_path(source_id)
        try:
            with open_shared_binary(raw_path) as handle:
                handle.seek(source_byte_start)
                raw_bytes = handle.read(source_byte_end - source_byte_start)
        except FileNotFoundError as exc:
            raise RawEventResolverError(f"Missing raw-event source file for {source_id}: {raw_path}") from exc

        if len(raw_bytes) != source_byte_end - source_byte_start:
            raise RawEventResolverError(
                f"Incomplete raw-event read for source {source_id}: {len(raw_bytes)} != {source_byte_end - source_byte_start}"
            )
        if not raw_bytes.endswith(b"\n"):
            raise RawEventResolverError(
                f"Resolved raw-event range does not end on a newline for source {source_id}: {source_byte_start}-{source_byte_end}"
            )

        event_digest = compute_event_digest(raw_bytes)
        self._validate_expected_digest(event_digest, expected_digest, source_id, source_byte_start, source_byte_end)

        payload_bytes = raw_bytes[:-1]
        try:
            raw_event = json.loads(payload_bytes.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise RawEventResolverError(
                f"Resolved raw-event bytes are not valid JSON for source {source_id}: {source_byte_start}-{source_byte_end}"
            ) from exc
        if not isinstance(raw_event, dict):
            raise RawEventResolverError(
                f"Resolved raw-event bytes did not decode to an object for source {source_id}: {source_byte_start}-{source_byte_end}"
            )

        resolved = ResolvedRawEvent(
            source_id=source_id,
            source_byte_start=source_byte_start,
            source_byte_end=source_byte_end,
            event_digest=event_digest,
            raw_bytes=raw_bytes,
            raw_event=raw_event,
        )
        self._cache[key] = resolved
        self._cache.move_to_end(key)
        while len(self._cache) > self._max_cache_entries:
            self._cache.popitem(last=False)
        return resolved

    def hydrate_normalized_event(self, event: dict[str, Any]) -> ResolvedRawEvent:
        return self.hydrate_event(
            source_id=str(event["source_id"]),
            source_byte_start=int(event["source_byte_start"]),
            source_byte_end=int(event["source_byte_end"]),
            expected_digest=str(event.get("event_digest", "")) or None,
        )

    def collect_text_surfaces(self, event: dict[str, Any]) -> list[dict[str, str]]:
        if not bool(event.get("text_surface_truncated")):
            return [dict(item) for item in event.get("text_surfaces", []) if isinstance(item, dict)]
        resolved = self.hydrate_normalized_event(event)
        from .normalization import extract_text_surfaces

        return extract_text_surfaces(resolved.raw_event)

    def _validate_expected_digest(
        self,
        actual_digest: str,
        expected_digest: str | None,
        source_id: str,
        source_byte_start: int,
        source_byte_end: int,
    ) -> None:
        if expected_digest and actual_digest != expected_digest:
            raise RawEventResolverError(
                f"Resolved raw-event digest mismatch for source {source_id}: {source_byte_start}-{source_byte_end}"
            )
