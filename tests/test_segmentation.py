from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path
from uuid import uuid4

from sessionmemory.discovery import run_discovery
from sessionmemory.normalization import run_normalization
from sessionmemory.segmentation import run_segmentation


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


class SegmentationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="sessionmemory-segment-"))
        self.root = self.temp_dir / "sessions"
        self.state_dir = self.temp_dir / "state"
        self.normalized_dir = self.temp_dir / "normalized"
        self.segmented_dir = self.temp_dir / "segmented"
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

    def source_path(self, session_id: str) -> Path:
        return self.root / "2026" / "04" / "12" / f"rollout-2026-04-12T20-59-14-{session_id}.jsonl"

    def run_pipeline(self, source_ids: list[str] | None = None) -> tuple[object, object, object]:
        discovery_result = run_discovery(self.config_path, self.state_dir)
        normalization_result = run_normalization(
            config_path=self.config_path,
            state_dir=self.state_dir,
            schema_path=self.schema_path,
            normalized_dir=self.normalized_dir,
            audits_dir=self.audits_dir,
        )
        segmentation_result = run_segmentation(
            state_dir=self.state_dir,
            normalized_dir=self.normalized_dir,
            segmented_dir=self.segmented_dir,
            source_ids=source_ids,
        )
        return discovery_result, normalization_result, segmentation_result

    def read_json(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def read_jsonl(self, path: Path) -> list[dict]:
        return [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    def test_full_segmentation_and_idempotent_rerun(self) -> None:
        session_id = str(uuid4())
        make_source_file(
            self.source_path(session_id),
            session_id,
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:00:00.000Z",
                    "type": "event_msg",
                    "payload": {"type": "user_message", "message": "Inspect the runtime state"},
                },
                {
                    "timestamp": "2026-04-12T21:00:01.000Z",
                    "type": "response_item",
                    "payload": {
                        "type": "function_call",
                        "name": "shell_command",
                        "call_id": "call-1",
                        "arguments": "{\"command\":\"git status\"}",
                    },
                },
                {
                    "timestamp": "2026-04-12T21:00:02.000Z",
                    "type": "response_item",
                    "payload": {
                        "type": "function_call_output",
                        "call_id": "call-1",
                        "output": "Exit code: 0\nclean",
                    },
                },
                {
                    "timestamp": "2026-04-12T21:00:03.000Z",
                    "type": "event_msg",
                    "payload": {"type": "task_complete"},
                },
            ],
        )
        self.write_config()

        discovery_result, normalization_result, segmentation_result = self.run_pipeline()
        self.assertTrue(discovery_result.report.success)
        self.assertTrue(normalization_result.report.success)
        self.assertTrue(segmentation_result.report.success)

        segments = self.read_jsonl(self.segmented_dir / "sources" / session_id / "segments.jsonl")
        session_flow = self.read_json(self.segmented_dir / "sources" / session_id / "session_flow.json")
        self.assertEqual(len(segments), 2)
        self.assertEqual(session_flow["detected_call_chains"][0]["call_id"], "call-1")
        tool_segment = next(segment for segment in segments if "call-1" in segment["explicit_link_ids"].get("call_id", []))
        self.assertIn("git", " ".join(tool_segment["topic_hints"]))

        rerun = run_segmentation(
            state_dir=self.state_dir,
            normalized_dir=self.normalized_dir,
            segmented_dir=self.segmented_dir,
        )
        self.assertTrue(rerun.report.success)
        self.assertEqual(rerun.report.source_status_counts, {"unchanged": 1})

    def test_sample_scoped_run_and_guardrail_split(self) -> None:
        target_session_id = str(uuid4())
        skipped_session_id = str(uuid4())
        large_text = "memory " * 700

        make_source_file(
            self.source_path(target_session_id),
            target_session_id,
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:10:00.000Z",
                    "type": "response_item",
                    "payload": {
                        "type": "message",
                        "role": "assistant",
                        "content": [{"type": "output_text", "text": large_text}],
                    },
                },
                {
                    "timestamp": "2026-04-12T21:10:05.000Z",
                    "type": "event_msg",
                    "payload": {"type": "user_message", "message": "Switch to database indexing details"},
                },
            ],
        )
        make_source_file(
            self.source_path(skipped_session_id),
            skipped_session_id,
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:11:00.000Z",
                    "type": "event_msg",
                    "payload": {"type": "user_message", "message": "Keep this source unsegmented for now"},
                }
            ],
        )
        self.write_config()

        discovery_result, normalization_result, segmentation_result = self.run_pipeline(
            source_ids=[target_session_id]
        )
        self.assertTrue(discovery_result.report.success)
        self.assertTrue(normalization_result.report.success)
        self.assertTrue(segmentation_result.report.success)
        self.assertEqual(segmentation_result.report.source_status_counts, {"segmented": 1})

        target_segments = self.read_jsonl(self.segmented_dir / "sources" / target_session_id / "segments.jsonl")
        self.assertEqual(len(target_segments), 2)
        self.assertIn("forced_size_split", target_segments[0]["boundary_reasons"])
        self.assertFalse((self.segmented_dir / "sources" / skipped_session_id).exists())

    def test_incremental_normalization_change_triggers_resegmentation(self) -> None:
        session_id = str(uuid4())
        source_path = self.source_path(session_id)
        make_source_file(
            source_path,
            session_id,
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:20:00.000Z",
                    "type": "event_msg",
                    "payload": {"type": "user_message", "message": "Start with discovery indexing"},
                }
            ],
        )
        self.write_config()
        self.run_pipeline()

        with source_path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(
                json.dumps(
                    {
                        "timestamp": "2026-04-12T21:20:02.000Z",
                        "type": "response_item",
                        "payload": {
                            "type": "message",
                            "role": "assistant",
                            "content": [{"type": "output_text", "text": "Added more indexing detail"}],
                        },
                    },
                    separators=(",", ":"),
                )
                + "\n"
            )

        discovery_result, normalization_result, segmentation_result = self.run_pipeline()
        self.assertTrue(discovery_result.report.success)
        self.assertTrue(normalization_result.report.success)
        self.assertTrue(segmentation_result.report.success)
        self.assertEqual(segmentation_result.report.source_status_counts, {"segmented": 1})

        stats = self.read_json(self.segmented_dir / "sources" / session_id / "stats.json")
        self.assertEqual(stats["segment_count"], 1)

    def test_tombstoned_source_keeps_artifacts_and_marks_state(self) -> None:
        session_id = str(uuid4())
        source_path = self.source_path(session_id)
        make_source_file(source_path, session_id)
        self.write_config()
        self.run_pipeline()

        segmented_source_dir = self.segmented_dir / "sources" / session_id
        self.assertTrue((segmented_source_dir / "segments.jsonl").exists())

        source_path.unlink()
        discovery_result, normalization_result, segmentation_result = self.run_pipeline()
        self.assertTrue(discovery_result.report.success)
        self.assertTrue(normalization_result.report.success)
        self.assertTrue(segmentation_result.report.success)

        state_payload = self.read_json(self.state_dir / "segmentation_state.json")
        self.assertEqual(state_payload["sources"][0]["status"], "tombstoned")
        self.assertTrue((segmented_source_dir / "segments.jsonl").exists())


if __name__ == "__main__":
    unittest.main()
