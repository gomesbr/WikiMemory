from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path
from uuid import uuid4

from sessionmemory.classification import run_classification
from sessionmemory.discovery import run_discovery
from sessionmemory.extraction import run_extraction
from sessionmemory.normalization import run_normalization
from sessionmemory.segmentation import run_segmentation


def make_source_file(
    path: Path,
    session_id: str,
    extra_lines: list[dict] | None = None,
    cwd: str = "C:\\repo",
) -> None:
    extra_lines = extra_lines or []
    lines = [
        {
            "timestamp": "2026-04-12T20:59:14.432Z",
            "type": "session_meta",
            "payload": {
                "id": session_id,
                "timestamp": "2026-04-12T20:59:14.432Z",
                "cwd": cwd,
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


class ExtractionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="sessionmemory-extract-"))
        self.root = self.temp_dir / "sessions"
        self.state_dir = self.temp_dir / "state"
        self.normalized_dir = self.temp_dir / "normalized"
        self.segmented_dir = self.temp_dir / "segmented"
        self.classified_dir = self.temp_dir / "classified"
        self.extracted_dir = self.temp_dir / "extracted"
        self.audits_dir = self.temp_dir / "audits"
        self.config_path = self.temp_dir / "source_roots.json"
        repo_root = Path(__file__).resolve().parents[1]
        self.schema_path = repo_root / "schema" / "normalization_catalog.json"
        self.taxonomy_path = repo_root / "config" / "classification_taxonomy.json"
        self.rules_path = repo_root / "config" / "extraction_rules.json"

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

    def source_path(self, session_id: str, *subdirs: str) -> Path:
        base = self.root / "2026" / "04" / "12"
        for part in subdirs:
            base /= part
        return base / f"rollout-2026-04-12T20-59-14-{session_id}.jsonl"

    def run_until_classified(self) -> tuple[object, object, object, object]:
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
        )
        classification_result = run_classification(
            taxonomy_path=self.taxonomy_path,
            state_dir=self.state_dir,
            normalized_dir=self.normalized_dir,
            segmented_dir=self.segmented_dir,
            classified_dir=self.classified_dir,
            audits_dir=self.audits_dir,
            source_roots_config_path=self.config_path,
        )
        return discovery_result, normalization_result, segmentation_result, classification_result

    def run_full_pipeline(
        self,
        source_ids: list[str] | None = None,
        rules_path: Path | None = None,
    ) -> tuple[object, object, object, object, object]:
        discovery_result, normalization_result, segmentation_result, classification_result = (
            self.run_until_classified()
        )
        extraction_result = run_extraction(
            rules_path=rules_path or self.rules_path,
            state_dir=self.state_dir,
            normalized_dir=self.normalized_dir,
            classified_dir=self.classified_dir,
            extracted_dir=self.extracted_dir,
            audits_dir=self.audits_dir,
            source_ids=source_ids,
            source_roots_config_path=self.config_path,
        )
        return (
            discovery_result,
            normalization_result,
            segmentation_result,
            classification_result,
            extraction_result,
        )

    def read_json(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def read_jsonl(self, path: Path) -> list[dict]:
        return [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    def source_items(self, session_id: str) -> list[dict]:
        return self.read_jsonl(self.extracted_dir / "sources" / session_id / "items.jsonl")

    def domain_items(self, domain: str) -> list[dict]:
        return self.read_jsonl(self.extracted_dir / "domains" / domain / "items.jsonl")

    def test_segment_emits_global_workflow_rule_and_project_task(self) -> None:
        session_id = str(uuid4())
        make_source_file(
            self.source_path(session_id, "ai-trader"),
            session_id,
            cwd="C:\\repos\\ai-trader",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:00:00.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "Workflow rule: be concise and do not refactor unrelated files. Update the AI Trader broker integration.",
                    },
                }
            ],
        )
        self.write_config()

        *_, extraction_result = self.run_full_pipeline()
        self.assertTrue(extraction_result.report.success)
        items = self.source_items(session_id)
        workflow_rule = next(item for item in items if item["item_type"] == "workflow_rule")
        task_request = next(item for item in items if item["item_type"] == "task_request")
        self.assertEqual(workflow_rule["primary_domain"], "global")
        self.assertEqual(workflow_rule["target_namespace"], "global")
        self.assertEqual(workflow_rule["target_page_key"], "workflow-rules")
        self.assertEqual(task_request["primary_domain"], "ai-trader")
        self.assertEqual(task_request["target_namespace"], "projects/ai-trader")
        self.assertEqual(task_request["target_page_key"], "tasks")

    def test_one_off_imperative_does_not_become_durable_rule(self) -> None:
        session_id = str(uuid4())
        make_source_file(
            self.source_path(session_id, "global"),
            session_id,
            cwd="C:\\repos\\shared-rag",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:00:10.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "PLEASE IMPLEMENT THIS PLAN: add the reporting section.",
                    },
                }
            ],
        )
        self.write_config()

        *_, extraction_result = self.run_full_pipeline()
        self.assertTrue(extraction_result.report.success)
        items = self.source_items(session_id)
        self.assertFalse(any(item["item_type"] in {"do_rule", "dont_rule", "workflow_rule"} for item in items))

    def test_schema_header_fragment_is_skipped_for_preferences(self) -> None:
        session_id = str(uuid4())
        make_source_file(
            self.source_path(session_id, "global"),
            session_id,
            cwd="C:\\repos\\shared-rag",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:00:20.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "### Response style",
                    },
                }
            ],
        )
        self.write_config()

        *_, extraction_result = self.run_full_pipeline()
        self.assertTrue(extraction_result.report.success)
        items = self.source_items(session_id)
        self.assertFalse(any(item["item_type"] == "communication_preference" for item in items))

    def test_repeated_observations_merge_into_domain_item(self) -> None:
        first_id = str(uuid4())
        second_id = str(uuid4())
        for session_id, timestamp in [
            (first_id, "2026-04-12T21:01:00.000Z"),
            (second_id, "2026-04-12T21:02:00.000Z"),
        ]:
            make_source_file(
                self.source_path(session_id, "shared"),
                session_id,
                cwd="C:\\repos\\shared-rag",
                extra_lines=[
                    {
                        "timestamp": timestamp,
                        "type": "event_msg",
                        "payload": {
                            "type": "user_message",
                            "message": "Workflow rule: be concise and do not refactor unrelated files.",
                        },
                    }
                ],
            )
        self.write_config()

        *_, extraction_result = self.run_full_pipeline()
        self.assertTrue(extraction_result.report.success)
        items = self.domain_items("global")
        merged = next(item for item in items if item["item_type"] == "workflow_rule")
        self.assertEqual(merged["recurrence_count"], 2)
        self.assertEqual(len(merged["supporting_source_ids"]), 2)
        self.assertEqual(len(merged["provenance_refs"]), 2)
        self.assertLessEqual(merged["first_seen_at"], merged["last_seen_at"])

    def test_cross_project_operational_segment_emits_cross_project_item(self) -> None:
        session_id = str(uuid4())
        make_source_file(
            self.source_path(session_id, "shared"),
            session_id,
            cwd="C:\\repos\\shared-rag",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:03:00.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "Connect Open Brain memory system with AI Scientist optimization loop.",
                    },
                }
            ],
        )
        self.write_config()

        *_, extraction_result = self.run_full_pipeline()
        self.assertTrue(extraction_result.report.success)
        item = next(item for item in self.source_items(session_id) if item["item_type"] == "task_request")
        self.assertEqual(item["primary_domain"], "cross-project")
        self.assertIn("open-brain", item["secondary_domains"])
        self.assertIn("ai-scientist", item["secondary_domains"])

    def test_explicit_code_path_emits_code_location_item(self) -> None:
        session_id = str(uuid4())
        make_source_file(
            self.source_path(session_id, "shared"),
            session_id,
            cwd="C:\\repos\\shared-rag",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:04:00.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "Update file sessionmemory/cli.py and the sessionmemory.segmentation module path.",
                    },
                }
            ],
        )
        self.write_config()

        *_, extraction_result = self.run_full_pipeline()
        self.assertTrue(extraction_result.report.success)
        code_item = next(item for item in self.source_items(session_id) if item["item_type"] == "code_location")
        self.assertEqual(code_item["target_page_key"], "code-map")
        self.assertIn("sessionmemory/cli.py", code_item["code_location"].get("path", ""))
        self.assertIn("sessionmemory.segmentation", code_item["code_location"].get("module", ""))

    def test_truncated_event_uses_lazy_raw_hydration_for_code_location(self) -> None:
        session_id = str(uuid4())
        long_prefix = "A" * 5000
        make_source_file(
            self.source_path(session_id, "shared"),
            session_id,
            cwd="C:\\repos\\shared-rag",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:04:10.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": f"{long_prefix} update file sessionmemory/cli.py and inspect sessionmemory.segmentation.",
                    },
                }
            ],
        )
        self.write_config()

        *_, extraction_result = self.run_full_pipeline()
        self.assertTrue(extraction_result.report.success)
        code_item = next(item for item in self.source_items(session_id) if item["item_type"] == "code_location")
        self.assertIn("sessionmemory/cli.py", code_item["code_location"].get("path", ""))
        normalized_events = self.read_jsonl(self.normalized_dir / "sources" / session_id / "events.jsonl")
        self.assertTrue(any(event.get("text_surface_truncated") for event in normalized_events))

    def test_example_prose_does_not_emit_code_location_item(self) -> None:
        session_id = str(uuid4())
        make_source_file(
            self.source_path(session_id, "shared"),
            session_id,
            cwd="C:\\repos\\shared-rag",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:04:30.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "When exploring, e.g. use examples like src/app.ts or package.json in documentation, but do not treat them as actual code map entries.",
                    },
                }
            ],
        )
        self.write_config()

        *_, extraction_result = self.run_full_pipeline()
        self.assertTrue(extraction_result.report.success)
        self.assertFalse(any(item["item_type"] == "code_location" for item in self.source_items(session_id)))

    def test_global_segment_code_location_inherits_global_domain(self) -> None:
        session_id = str(uuid4())
        make_source_file(
            self.source_path(session_id, "shared"),
            session_id,
            cwd="C:\\repos\\shared-rag",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:04:40.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "Workflow rule: use file AGENTS.md as the main reference before editing.",
                    },
                }
            ],
        )
        self.write_config()

        *_, extraction_result = self.run_full_pipeline()
        self.assertTrue(extraction_result.report.success)
        code_items = [item for item in self.source_items(session_id) if item["item_type"] == "code_location"]
        self.assertTrue(code_items)
        self.assertTrue(all(item["primary_domain"] == "global" for item in code_items))

    def test_code_location_items_do_not_emit_conflict_notices(self) -> None:
        session_id = str(uuid4())
        make_source_file(
            self.source_path(session_id, "shared"),
            session_id,
            cwd="C:\\repos\\shared-rag",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:04:45.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "Workflow rule: inspect AGENTS.md and AGENTS.md before editing.",
                    },
                }
            ],
        )
        self.write_config()

        *_, extraction_result = self.run_full_pipeline()
        self.assertTrue(extraction_result.report.success)
        notices = self.read_jsonl(self.audits_dir / "extraction_notices.jsonl")
        self.assertFalse(any(notice["notice_type"] == "conflict_candidate" for notice in notices))

    def test_weak_candidate_is_skipped_and_logged(self) -> None:
        session_id = str(uuid4())
        make_source_file(
            self.source_path(session_id, "shared"),
            session_id,
            cwd="C:\\repos\\shared-rag",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:05:00.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "Context around general behavior later.",
                    },
                }
            ],
        )
        self.write_config()

        *_, extraction_result = self.run_full_pipeline()
        self.assertTrue(extraction_result.report.success)
        self.assertEqual(self.source_items(session_id), [])
        notices = self.read_jsonl(self.audits_dir / "extraction_notices.jsonl")
        self.assertTrue(any(notice["notice_type"] == "skipped_weak_inference" for notice in notices))

    def test_conflicting_items_keep_shared_conflict_key(self) -> None:
        session_id = str(uuid4())
        make_source_file(
            self.source_path(session_id, "open-brain"),
            session_id,
            cwd="C:\\repos\\sessionmemory",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:06:00.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "Current state: storage backend = sqlite. Current state: storage backend = postgres.",
                    },
                }
            ],
        )
        self.write_config()

        *_, extraction_result = self.run_full_pipeline()
        self.assertTrue(extraction_result.report.success)
        current_state_items = [item for item in self.source_items(session_id) if item["item_type"] == "current_state"]
        self.assertEqual(len(current_state_items), 2)
        conflict_keys = {item["conflict_candidate_key"] for item in current_state_items}
        self.assertEqual(len(conflict_keys), 1)
        self.assertNotIn(None, conflict_keys)

    def test_replacement_cue_marks_older_temporal_item_superseded(self) -> None:
        session_id = str(uuid4())
        make_source_file(
            self.source_path(session_id, "open-brain"),
            session_id,
            cwd="C:\\repos\\sessionmemory",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:07:00.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "Current state: storage backend = sqlite. Current state: storage backend = postgres now instead.",
                    },
                }
            ],
        )
        self.write_config()

        *_, extraction_result = self.run_full_pipeline()
        self.assertTrue(extraction_result.report.success)
        current_state_items = [item for item in self.source_items(session_id) if item["item_type"] == "current_state"]
        statuses = {item["statement"]: item["temporal_status"] for item in current_state_items}
        self.assertEqual(statuses["Current state: storage backend = sqlite."], "superseded")
        self.assertEqual(statuses["Current state: storage backend = postgres now instead."], "active")

    def test_sample_scoped_extraction_only_writes_requested_source(self) -> None:
        target_id = str(uuid4())
        skipped_id = str(uuid4())
        make_source_file(
            self.source_path(target_id, "ai-trader"),
            target_id,
            cwd="C:\\repos\\ai-trader",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:08:00.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "Update the AI Trader strategy.",
                    },
                }
            ],
        )
        make_source_file(
            self.source_path(skipped_id, "shared"),
            skipped_id,
            cwd="C:\\repos\\shared-rag",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:08:30.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "Workflow rule: be concise.",
                    },
                }
            ],
        )
        self.write_config()

        self.run_until_classified()
        extraction_result = run_extraction(
            rules_path=self.rules_path,
            state_dir=self.state_dir,
            normalized_dir=self.normalized_dir,
            classified_dir=self.classified_dir,
            extracted_dir=self.extracted_dir,
            audits_dir=self.audits_dir,
            source_ids=[target_id],
        )
        self.assertTrue(extraction_result.report.success)
        self.assertTrue((self.extracted_dir / "sources" / target_id / "items.jsonl").exists())
        self.assertFalse((self.extracted_dir / "sources" / skipped_id).exists())

    def test_rules_version_bump_forces_reextract(self) -> None:
        session_id = str(uuid4())
        make_source_file(
            self.source_path(session_id, "shared"),
            session_id,
            cwd="C:\\repos\\shared-rag",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:09:00.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "Workflow rule: be concise.",
                    },
                }
            ],
        )
        self.write_config()
        self.run_full_pipeline()

        bumped_rules_path = self.temp_dir / "extraction_rules.bumped.json"
        bumped_payload = self.read_json(self.rules_path)
        bumped_payload["extraction_rules_version"] = int(bumped_payload["extraction_rules_version"]) + 1
        bumped_rules_path.write_text(json.dumps(bumped_payload, indent=2), encoding="utf-8")

        extraction_result = run_extraction(
            rules_path=bumped_rules_path,
            state_dir=self.state_dir,
            normalized_dir=self.normalized_dir,
            classified_dir=self.classified_dir,
            extracted_dir=self.extracted_dir,
            audits_dir=self.audits_dir,
        )
        self.assertTrue(extraction_result.report.success)
        self.assertEqual(extraction_result.report.source_status_counts, {"extracted": 1})
        state_payload = self.read_json(self.state_dir / "extraction_state.json")
        self.assertEqual(
            state_payload["sources"][0]["extraction_rules_version"],
            bumped_payload["extraction_rules_version"],
        )

    def test_tombstoned_source_keeps_artifacts_and_marks_state(self) -> None:
        session_id = str(uuid4())
        source_path = self.source_path(session_id, "shared")
        make_source_file(
            source_path,
            session_id,
            cwd="C:\\repos\\shared-rag",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:10:00.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "Workflow rule: be concise.",
                    },
                }
            ],
        )
        self.write_config()
        self.run_full_pipeline()
        extracted_source_dir = self.extracted_dir / "sources" / session_id
        self.assertTrue((extracted_source_dir / "items.jsonl").exists())

        source_path.unlink()
        self.run_until_classified()
        extraction_result = run_extraction(
            rules_path=self.rules_path,
            state_dir=self.state_dir,
            normalized_dir=self.normalized_dir,
            classified_dir=self.classified_dir,
            extracted_dir=self.extracted_dir,
            audits_dir=self.audits_dir,
        )
        self.assertTrue(extraction_result.report.success)
        self.assertEqual(extraction_result.report.source_status_counts, {"tombstoned": 1})
        self.assertTrue((extracted_source_dir / "items.jsonl").exists())
        state_payload = self.read_json(self.state_dir / "extraction_state.json")
        self.assertEqual(state_payload["sources"][0]["status"], "tombstoned")

    def test_invalid_rules_config_fails_without_replacing_prior_state(self) -> None:
        session_id = str(uuid4())
        make_source_file(
            self.source_path(session_id, "shared"),
            session_id,
            cwd="C:\\repos\\shared-rag",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:11:00.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "Workflow rule: be concise.",
                    },
                }
            ],
        )
        self.write_config()
        self.run_full_pipeline()
        prior_state_text = (self.state_dir / "extraction_state.json").read_text(encoding="utf-8")

        invalid_rules_path = self.temp_dir / "extraction_rules.invalid.json"
        invalid_rules_path.write_text("{}", encoding="utf-8")
        extraction_result = run_extraction(
            rules_path=invalid_rules_path,
            state_dir=self.state_dir,
            normalized_dir=self.normalized_dir,
            classified_dir=self.classified_dir,
            extracted_dir=self.extracted_dir,
            audits_dir=self.audits_dir,
        )
        self.assertFalse(extraction_result.report.success)
        self.assertEqual(
            (self.state_dir / "extraction_state.json").read_text(encoding="utf-8"),
            prior_state_text,
        )
