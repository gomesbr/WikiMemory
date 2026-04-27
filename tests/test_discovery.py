from __future__ import annotations

import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from uuid import uuid4

from sessionmemory.discovery import run_discovery


def make_source_file(path: Path, session_id: str, extra_lines: list[dict] | None = None) -> None:
    extra_lines = extra_lines or []
    payloads = [
        {
            "timestamp": "2026-04-12T20:59:14.432Z",
            "type": "session_meta",
            "payload": {
                "id": session_id,
                "timestamp": "2026-04-12T20:59:14.432Z",
                "cwd": "C:\\repo",
            },
        },
        *extra_lines,
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for payload in payloads:
            handle.write(json.dumps(payload, separators=(",", ":")) + "\n")


class DiscoveryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="sessionmemory-tests-"))
        self.root_a = self.temp_dir / "sessions-a"
        self.root_b = self.temp_dir / "sessions-b"
        self.state_dir = self.temp_dir / "state"
        self.config_path = self.temp_dir / "source_roots.json"

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def write_config(self, template: str) -> None:
        payload = {
            "schema_version": 1,
            "roots": [
                {
                    "root_alias": "codex_sessions",
                    "absolute_path": template,
                    "enabled": True,
                    "recursive": True,
                    "include_glob": "**/*.jsonl",
                }
            ],
        }
        self.config_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def read_registry(self) -> dict:
        return json.loads((self.state_dir / "source_registry.json").read_text(encoding="utf-8"))

    def read_run_log(self) -> list[dict]:
        run_log = self.state_dir / "discovery_runs.jsonl"
        return [
            json.loads(line)
            for line in run_log.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    def test_initial_discovery_and_idempotent_rerun(self) -> None:
        session_id = str(uuid4())
        file_path = self.root_a / "2026/04/12" / f"rollout-2026-04-12T20-59-14-{session_id}.jsonl"
        make_source_file(
            file_path,
            session_id,
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:00:00.000Z",
                    "type": "event_msg",
                    "payload": {"type": "task_started"},
                }
            ],
        )
        self.write_config(str(self.root_a))

        first_result = run_discovery(self.config_path, self.state_dir)
        self.assertTrue(first_result.report.success)
        first_registry = self.read_registry()
        self.assertEqual(first_registry["source_count"], 1)
        self.assertEqual(first_registry["sources"][0]["status"], "new")

        second_result = run_discovery(self.config_path, self.state_dir)
        self.assertTrue(second_result.report.success)
        second_registry = self.read_registry()
        self.assertEqual(second_registry["sources"][0]["status"], "stable")
        self.assertEqual(second_registry["sources"][0]["committed_line_count"], 2)
        self.assertEqual(len(self.read_run_log()), 2)

    def test_append_complete_and_partial_lines(self) -> None:
        session_id = str(uuid4())
        file_path = self.root_a / "2026/04/12" / f"rollout-2026-04-12T20-59-14-{session_id}.jsonl"
        make_source_file(file_path, session_id)
        self.write_config(str(self.root_a))

        run_discovery(self.config_path, self.state_dir)
        with file_path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(
                json.dumps(
                    {
                        "timestamp": "2026-04-12T21:00:00.000Z",
                        "type": "event_msg",
                        "payload": {"type": "token_count"},
                    },
                    separators=(",", ":"),
                )
                + "\n"
            )
            handle.write('{"timestamp":"2026-04-12T21:01:00.000Z","type":"response_item"')

        growing_result = run_discovery(self.config_path, self.state_dir)
        self.assertTrue(growing_result.report.success)
        registry = self.read_registry()
        record = registry["sources"][0]
        self.assertEqual(record["status"], "growing")
        self.assertEqual(record["committed_line_count"], 2)
        self.assertGreater(record["uncommitted_tail_bytes"], 0)

        with file_path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(',"payload":{"type":"message"}}' + "\n")

        completed_result = run_discovery(self.config_path, self.state_dir)
        self.assertTrue(completed_result.report.success)
        registry = self.read_registry()
        record = registry["sources"][0]
        self.assertEqual(record["status"], "growing")
        self.assertEqual(record["committed_line_count"], 3)
        self.assertEqual(record["uncommitted_tail_bytes"], 0)

    def test_duplicate_identical_and_conflicting_copy(self) -> None:
        session_id = str(uuid4())
        relative_path = Path("2026/04/12") / f"rollout-2026-04-12T20-59-14-{session_id}.jsonl"
        original_path = self.root_a / relative_path
        duplicate_path = self.root_a / "archive" / relative_path.name
        make_source_file(
            original_path,
            session_id,
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:00:00.000Z",
                    "type": "event_msg",
                    "payload": {"type": "task_started"},
                }
            ],
        )
        duplicate_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(original_path, duplicate_path)
        self.write_config(str(self.root_a))

        success_result = run_discovery(self.config_path, self.state_dir)
        self.assertTrue(success_result.report.success)
        registry = self.read_registry()
        record = registry["sources"][0]
        locator_states = {locator["locator_state"] for locator in record["locators"]}
        self.assertEqual(locator_states, {"active", "duplicate"})

        with duplicate_path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(
                json.dumps(
                    {
                        "timestamp": "2026-04-12T21:05:00.000Z",
                        "type": "event_msg",
                        "payload": {"type": "user_message"},
                    },
                    separators=(",", ":"),
                )
                + "\n"
            )

        failed_result = run_discovery(self.config_path, self.state_dir)
        self.assertFalse(failed_result.report.success)
        registry_after_failure = self.read_registry()
        self.assertEqual(registry_after_failure, registry)
        self.assertIn("Conflicting duplicate", failed_result.report.fatal_error_summary)

    def test_tombstone_and_root_move_with_same_alias(self) -> None:
        session_id = str(uuid4())
        relative_path = Path("2026/04/12") / f"rollout-2026-04-12T20-59-14-{session_id}.jsonl"
        source_path = self.root_a / relative_path
        make_source_file(source_path, session_id)

        os.environ["SESSIONMEMORY_TEST_ROOT"] = str(self.root_a)
        self.addCleanup(os.environ.pop, "SESSIONMEMORY_TEST_ROOT", None)
        self.write_config("${SESSIONMEMORY_TEST_ROOT}")

        run_discovery(self.config_path, self.state_dir)
        source_path.unlink()

        tombstoned_result = run_discovery(self.config_path, self.state_dir)
        self.assertTrue(tombstoned_result.report.success)
        tombstoned_registry = self.read_registry()
        self.assertEqual(tombstoned_registry["sources"][0]["status"], "tombstoned")

        restored_path = self.root_b / relative_path
        make_source_file(restored_path, session_id)
        os.environ["SESSIONMEMORY_TEST_ROOT"] = str(self.root_b)

        moved_result = run_discovery(self.config_path, self.state_dir)
        self.assertTrue(moved_result.report.success)
        moved_registry = self.read_registry()
        self.assertEqual(moved_registry["sources"][0]["status"], "stable")
        self.assertEqual(
            moved_registry["sources"][0]["preferred_locator"]["relative_path"],
            relative_path.as_posix(),
        )

    def test_invalid_first_line_does_not_replace_registry(self) -> None:
        valid_session_id = str(uuid4())
        valid_path = self.root_a / "2026/04/12" / f"rollout-2026-04-12T20-59-14-{valid_session_id}.jsonl"
        make_source_file(valid_path, valid_session_id)
        self.write_config(str(self.root_a))

        run_discovery(self.config_path, self.state_dir)
        registry_before_failure = self.read_registry()

        invalid_session_id = str(uuid4())
        invalid_path = self.root_a / "2026/04/13" / f"rollout-2026-04-13T20-59-14-{invalid_session_id}.jsonl"
        invalid_path.parent.mkdir(parents=True, exist_ok=True)
        invalid_path.write_text('{"type":"event_msg"}\n', encoding="utf-8")

        failed_result = run_discovery(self.config_path, self.state_dir)
        self.assertFalse(failed_result.report.success)
        self.assertEqual(self.read_registry(), registry_before_failure)
        self.assertIn("First line is not session_meta", failed_result.report.fatal_error_summary)


if __name__ == "__main__":
    unittest.main()
