from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from uuid import uuid4

from sessionmemory.discovery import run_discovery
from sessionmemory.normalization import run_normalization
from sessionmemory.raw_event_resolver import RawEventResolver, RawEventResolverError, open_shared_binary


def make_source_file(path: Path, session_id: str, extra_lines: list[dict] | None = None) -> None:
    extra_lines = extra_lines or []
    lines = [
        {
            "timestamp": "2026-04-12T20:59:14.432Z",
            "type": "session_meta",
            "payload": {
                "id": session_id,
                "timestamp": "2026-04-12T20:59:14.432Z",
                "cwd": "C:\\repo",
                "originator": "codex_vscode",
                "cli_version": "0.119.0-alpha.28",
                "source": "vscode",
                "model_provider": "openai",
            },
        },
        *extra_lines,
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for line in lines:
            handle.write(json.dumps(line, separators=(",", ":")) + "\n")


class RawEventResolverTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="sessionmemory-rawresolver-"))
        self.root = self.temp_dir / "sessions"
        self.state_dir = self.temp_dir / "state"
        self.normalized_dir = self.temp_dir / "normalized"
        self.audits_dir = self.temp_dir / "audits"
        self.config_path = self.temp_dir / "source_roots.json"
        self.schema_path = Path(__file__).resolve().parents[1] / "schema" / "normalization_catalog.json"

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def write_config(self) -> None:
        payload = {
            "schema_version": 1,
            "roots": [
                {
                    "root_alias": "codex_sessions",
                    "absolute_path": str(self.root),
                    "enabled": True,
                    "recursive": True,
                    "include_glob": "**/*.jsonl",
                }
            ],
        }
        self.config_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def read_jsonl(self, path: Path) -> list[dict]:
        return [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    def source_path(self, session_id: str) -> Path:
        return self.root / "2026" / "04" / "12" / f"rollout-2026-04-12T20-59-14-{session_id}.jsonl"

    def prepare_source(self) -> tuple[str, dict]:
        session_id = str(uuid4())
        make_source_file(
            self.source_path(session_id),
            session_id,
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:00:00.000Z",
                    "type": "event_msg",
                    "payload": {"type": "user_message", "message": "Resolver test"},
                }
            ],
        )
        self.write_config()
        discovery_result = run_discovery(self.config_path, self.state_dir)
        normalization_result = run_normalization(
            config_path=self.config_path,
            state_dir=self.state_dir,
            schema_path=self.schema_path,
            normalized_dir=self.normalized_dir,
            audits_dir=self.audits_dir,
        )
        self.assertTrue(discovery_result.report.success)
        self.assertTrue(normalization_result.report.success)
        event = self.read_jsonl(self.normalized_dir / "sources" / session_id / "events.jsonl")[1]
        return session_id, event

    def test_exact_byte_hydration(self) -> None:
        session_id, event = self.prepare_source()
        resolver = RawEventResolver.from_paths(
            registry_path=self.state_dir / "source_registry.json",
            source_roots_config_path=self.config_path,
        )
        hydrated = resolver.hydrate_normalized_event(event)
        self.assertEqual(hydrated.source_id, session_id)
        self.assertEqual(hydrated.raw_event["payload"]["message"], "Resolver test")

    def test_invalid_byte_range_is_rejected(self) -> None:
        session_id, event = self.prepare_source()
        resolver = RawEventResolver.from_paths(
            registry_path=self.state_dir / "source_registry.json",
            source_roots_config_path=self.config_path,
        )
        with self.assertRaises(RawEventResolverError):
            resolver.hydrate_event(
                source_id=session_id,
                source_byte_start=int(event["source_byte_start"]),
                source_byte_end=int(event["source_byte_end"]) + 10,
            )

    def test_committed_boundary_validation_rejects_partial_line(self) -> None:
        _session_id, event = self.prepare_source()
        resolver = RawEventResolver.from_paths(
            registry_path=self.state_dir / "source_registry.json",
            source_roots_config_path=self.config_path,
        )
        with self.assertRaises(RawEventResolverError):
            resolver.hydrate_event(
                source_id=str(event["source_id"]),
                source_byte_start=int(event["source_byte_start"]),
                source_byte_end=int(event["source_byte_end"]) - 1,
                expected_digest=str(event["event_digest"]),
            )

    def test_cache_reuse_within_one_run(self) -> None:
        _session_id, event = self.prepare_source()
        resolver = RawEventResolver.from_paths(
            registry_path=self.state_dir / "source_registry.json",
            source_roots_config_path=self.config_path,
        )
        with patch("sessionmemory.raw_event_resolver.open_shared_binary", wraps=open_shared_binary) as mock_open:
            resolver.hydrate_normalized_event(event)
            resolver.hydrate_normalized_event(event)
        self.assertEqual(mock_open.call_count, 1)


if __name__ == "__main__":
    unittest.main()
