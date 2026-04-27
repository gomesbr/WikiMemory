from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path
from uuid import uuid4

from sessionmemory.discovery import run_discovery
from sessionmemory.normalization import run_normalization
from sessionmemory.raw_event_resolver import RawEventResolver


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


class NormalizationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="sessionmemory-normalize-"))
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

    def run_discovery_and_normalize(self) -> tuple[object, object]:
        discovery_result = run_discovery(self.config_path, self.state_dir)
        normalization_result = run_normalization(
            config_path=self.config_path,
            state_dir=self.state_dir,
            schema_path=self.schema_path,
            normalized_dir=self.normalized_dir,
            audits_dir=self.audits_dir,
        )
        return discovery_result, normalization_result

    def read_json(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def read_jsonl(self, path: Path) -> list[dict]:
        return [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    def source_paths(self, session_id: str) -> tuple[Path, Path]:
        relative = Path("2026/04/12") / f"rollout-2026-04-12T20-59-14-{session_id}.jsonl"
        return self.root / relative, relative

    def test_full_normalization_and_idempotent_rerun(self) -> None:
        session_id = str(uuid4())
        source_path, _ = self.source_paths(session_id)
        make_source_file(
            source_path,
            session_id,
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:00:00.000Z",
                    "type": "event_msg",
                    "payload": {"type": "agent_message", "message": "Planning phase."},
                },
                {
                    "timestamp": "2026-04-12T21:00:10.000Z",
                    "type": "response_item",
                    "payload": {
                        "type": "message",
                        "role": "assistant",
                        "content": [
                            {"type": "output_text", "text": "Hello"},
                            {"type": "output_text", "text": "World"},
                        ],
                    },
                },
                {
                    "timestamp": "2026-04-12T21:00:20.000Z",
                    "type": "turn_context",
                    "payload": {
                        "turn_id": "turn-1",
                        "cwd": "C:\\repo",
                        "approval_policy": "never",
                        "model": "gpt-5.4",
                        "personality": "warm",
                        "effort": "medium",
                        "summary": "auto",
                    },
                },
            ],
        )
        self.write_config()

        discovery_result, normalization_result = self.run_discovery_and_normalize()
        self.assertTrue(discovery_result.report.success)
        self.assertTrue(normalization_result.report.success)
        source_dir = self.normalized_dir / "sources" / session_id
        session_payload = self.read_json(source_dir / "session.json")
        stats_payload = self.read_json(source_dir / "stats.json")
        events = self.read_jsonl(source_dir / "events.jsonl")

        self.assertEqual(session_payload["committed_line_count"], 4)
        self.assertEqual(stats_payload["normalized_event_count"], 4)
        self.assertEqual(len(events), 4)
        self.assertIn("session_meta_ref", session_payload)
        self.assertNotIn("session_meta_raw", session_payload)
        self.assertTrue(all("raw_event" not in event for event in events))
        message_event = next(event for event in events if event["canonical_kind"] == "response_item.message")
        self.assertEqual(message_event["role"], "assistant")
        self.assertEqual([item["text"] for item in message_event["text_surfaces"]], ["Hello", "World"])
        self.assertFalse(message_event["text_surface_truncated"])
        self.assertTrue(message_event["event_digest"])

        rerun = run_normalization(
            config_path=self.config_path,
            state_dir=self.state_dir,
            schema_path=self.schema_path,
            normalized_dir=self.normalized_dir,
            audits_dir=self.audits_dir,
        )
        self.assertTrue(rerun.report.success)
        self.assertEqual(rerun.report.source_status_counts, {"unchanged": 1})

    def test_incremental_append_and_function_call_fields(self) -> None:
        session_id = str(uuid4())
        source_path, _ = self.source_paths(session_id)
        make_source_file(
            source_path,
            session_id,
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:00:00.000Z",
                    "type": "response_item",
                    "payload": {
                        "type": "function_call",
                        "name": "shell_command",
                        "call_id": "call-1",
                        "arguments": "{\"command\":\"echo hi\"}",
                    },
                },
                {
                    "timestamp": "2026-04-12T21:00:01.000Z",
                    "type": "response_item",
                    "payload": {
                        "type": "function_call_output",
                        "call_id": "call-1",
                        "output": "Exit code: 0\nhi",
                    },
                },
            ],
        )
        self.write_config()
        self.run_discovery_and_normalize()

        with source_path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(
                json.dumps(
                    {
                        "timestamp": "2026-04-12T21:00:02.000Z",
                        "type": "event_msg",
                        "payload": {"type": "user_message", "message": "Append-only update"},
                    },
                    separators=(",", ":"),
                )
                + "\n"
            )

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
        self.assertEqual(normalization_result.report.source_status_counts, {"normalized": 1})

        events = self.read_jsonl(self.normalized_dir / "sources" / session_id / "events.jsonl")
        function_call = next(event for event in events if event["canonical_kind"] == "response_item.function_call")
        function_output = next(event for event in events if event["canonical_kind"] == "response_item.function_call_output")
        self.assertEqual(function_call["call_id"], "call-1")
        self.assertEqual(function_output["call_id"], "call-1")
        self.assertIn("echo hi", [item["text"] for item in function_call["text_surfaces"]])
        self.assertIn("Exit code: 0\nhi", [item["text"] for item in function_output["text_surfaces"]])
        self.assertEqual(len(events), 4)

    def test_incremental_falls_back_to_full_when_artifacts_disagree_with_state(self) -> None:
        session_id = str(uuid4())
        source_path, _ = self.source_paths(session_id)
        make_source_file(
            source_path,
            session_id,
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:00:00.000Z",
                    "type": "event_msg",
                    "payload": {"type": "user_message", "message": "First"},
                }
            ],
        )
        self.write_config()
        self.run_discovery_and_normalize()

        stats_path = self.normalized_dir / "sources" / session_id / "stats.json"
        stats_payload = self.read_json(stats_path)
        stats_payload["normalized_event_count"] = int(stats_payload["normalized_event_count"]) + 1
        stats_path.write_text(json.dumps(stats_payload, indent=2), encoding="utf-8")

        with source_path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(
                json.dumps(
                    {
                        "timestamp": "2026-04-12T21:00:02.000Z",
                        "type": "event_msg",
                        "payload": {"type": "user_message", "message": "Second"},
                    },
                    separators=(",", ":"),
                )
                + "\n"
            )

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
        events = self.read_jsonl(self.normalized_dir / "sources" / session_id / "events.jsonl")
        self.assertEqual(len(events), 3)

    def test_schema_version_bump_forces_full_renormalization(self) -> None:
        session_id = str(uuid4())
        source_path, _ = self.source_paths(session_id)
        make_source_file(source_path, session_id)
        self.write_config()
        self.run_discovery_and_normalize()

        bumped_schema_path = self.temp_dir / "bumped_schema.json"
        schema_payload = self.read_json(self.schema_path)
        schema_payload["normalization_schema_version"] = int(schema_payload["normalization_schema_version"]) + 1
        bumped_schema_path.write_text(json.dumps(schema_payload, indent=2), encoding="utf-8")

        normalization_result = run_normalization(
            config_path=self.config_path,
            state_dir=self.state_dir,
            schema_path=bumped_schema_path,
            normalized_dir=self.normalized_dir,
            audits_dir=self.audits_dir,
        )
        self.assertTrue(normalization_result.report.success)
        self.assertEqual(normalization_result.report.source_status_counts, {"normalized": 1})
        state_payload = self.read_json(self.state_dir / "normalization_state.json")
        self.assertEqual(state_payload["normalization_schema_version"], schema_payload["normalization_schema_version"])

    def test_unknown_signatures_and_compacted_are_preserved(self) -> None:
        session_id = str(uuid4())
        source_path, _ = self.source_paths(session_id)
        make_source_file(
            source_path,
            session_id,
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:00:00.000Z",
                    "type": "compacted",
                    "payload": {"message": "", "replacement_history": []},
                },
                {
                    "timestamp": "2026-04-12T21:00:01.000Z",
                    "type": "response_item",
                    "payload": {"type": "mystery_tool", "call_id": "call-x", "output": "??"},
                },
                {
                    "timestamp": "2026-04-12T21:00:02.000Z",
                    "type": "mystery_outer",
                    "payload": {"type": "something", "message": "unknown"},
                },
            ],
        )
        self.write_config()

        _, normalization_result = self.run_discovery_and_normalize()
        self.assertTrue(normalization_result.report.success)
        events = self.read_jsonl(self.normalized_dir / "sources" / session_id / "events.jsonl")
        notices = self.read_jsonl(self.audits_dir / "normalization_notices.jsonl")

        self.assertTrue(any(event["outer_type"] == "compacted" for event in events))
        self.assertTrue(any(notice["notice_type"] == "unknown_payload_type" for notice in notices))
        self.assertTrue(any(notice["notice_type"] == "unknown_outer_type" for notice in notices))

    def test_malformed_committed_json_preserves_prior_normalized_state(self) -> None:
        session_id = str(uuid4())
        source_path, _ = self.source_paths(session_id)
        make_source_file(
            source_path,
            session_id,
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:00:00.000Z",
                    "type": "event_msg",
                    "payload": {"type": "task_started"},
                }
            ],
        )
        self.write_config()
        self.run_discovery_and_normalize()

        prior_state_text = (self.state_dir / "normalization_state.json").read_text(encoding="utf-8")
        prior_events_text = (self.normalized_dir / "sources" / session_id / "events.jsonl").read_text(encoding="utf-8")

        with source_path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write('{"timestamp":"2026-04-12T21:00:02.000Z","type":"event_msg","payload":\n')

        discovery_result = run_discovery(self.config_path, self.state_dir)
        normalization_result = run_normalization(
            config_path=self.config_path,
            state_dir=self.state_dir,
            schema_path=self.schema_path,
            normalized_dir=self.normalized_dir,
            audits_dir=self.audits_dir,
        )
        self.assertTrue(discovery_result.report.success)
        self.assertFalse(normalization_result.report.success)
        self.assertEqual((self.state_dir / "normalization_state.json").read_text(encoding="utf-8"), prior_state_text)
        self.assertEqual(
            (self.normalized_dir / "sources" / session_id / "events.jsonl").read_text(encoding="utf-8"),
            prior_events_text,
        )

    def test_tombstoned_source_keeps_artifacts_and_marks_state(self) -> None:
        session_id = str(uuid4())
        source_path, _ = self.source_paths(session_id)
        make_source_file(source_path, session_id)
        self.write_config()
        self.run_discovery_and_normalize()

        source_output_dir = self.normalized_dir / "sources" / session_id
        self.assertTrue((source_output_dir / "session.json").exists())
        source_path.unlink()

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
        state_payload = self.read_json(self.state_dir / "normalization_state.json")
        self.assertEqual(state_payload["sources"][0]["status"], "tombstoned")
        self.assertTrue((source_output_dir / "session.json").exists())

    def test_bounded_text_surfaces_are_truncated_but_hydratable(self) -> None:
        session_id = str(uuid4())
        source_path, _ = self.source_paths(session_id)
        long_text = "A" * 6000
        make_source_file(
            source_path,
            session_id,
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:00:00.000Z",
                    "type": "response_item",
                    "payload": {
                        "type": "message",
                        "role": "assistant",
                        "content": [
                            {"type": "output_text", "text": long_text},
                            {"type": "output_text", "text": "tail"},
                        ],
                    },
                }
            ],
        )
        self.write_config()
        self.run_discovery_and_normalize()

        source_dir = self.normalized_dir / "sources" / session_id
        events = self.read_jsonl(source_dir / "events.jsonl")
        truncated_event = next(event for event in events if event["canonical_kind"] == "response_item.message")
        self.assertTrue(truncated_event["text_surface_truncated"])
        self.assertLessEqual(sum(len(item["text"]) for item in truncated_event["text_surfaces"]), 4096)
        self.assertTrue(all("raw_event" not in event for event in events))

        resolver = RawEventResolver.from_paths(
            registry_path=self.state_dir / "source_registry.json",
            source_roots_config_path=self.config_path,
        )
        hydrated = resolver.hydrate_normalized_event(truncated_event)
        self.assertEqual(hydrated.raw_event["payload"]["content"][0]["text"], long_text)


if __name__ == "__main__":
    unittest.main()
