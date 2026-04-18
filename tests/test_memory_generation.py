from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from wikimemory.discovery import run_discovery
from wikimemory.ingest import run_ingest
from wikimemory.memory_generation import run_memory_generation
from wikimemory.normalization import run_normalization
from wikimemory.product_config import default_product_config


class MemoryGenerationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="wikimemory-memory-"))
        self.evidence_dir = self.temp_dir / "evidence"
        self.memory_dir = self.temp_dir / "memory"
        self.state_dir = self.temp_dir / "state"
        self.audits_dir = self.temp_dir / "audits"
        self.project_root = self.temp_dir / "project"
        self.product_config = self.temp_dir / "product_config.json"
        self.write_product_config()

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def write_product_config(self) -> None:
        payload = default_product_config(self.project_root).to_dict()
        payload["project_sources"][0]["project_root"] = str(self.project_root)
        self.product_config.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def write_evidence(self, relative_path: str, records: list[dict[str, object]]) -> None:
        path = self.evidence_dir / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "".join(json.dumps(record, sort_keys=True) + "\n" for record in records),
            encoding="utf-8",
        )

    def read_items(self) -> list[dict[str, object]]:
        path = self.memory_dir / "_meta" / "items.jsonl"
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

    def evidence_record(self, evidence_id: str, actor_type: str, text: str) -> dict[str, object]:
        return {
            "evidence_id": evidence_id,
            "evidence_type": "log_event",
            "source_adapter": "codex_jsonl",
            "source_id": "sample-source",
            "project_hint": "example-project",
            "actor_type": actor_type,
            "timestamp": "2026-04-18T00:00:00Z",
            "content_surfaces": [{"path": "payload.message", "text": text}],
            "provenance": {"source_id": "sample-source", "source_line_no": 1},
            "metadata": {},
        }

    def test_memory_generation_prioritizes_user_durable_intent(self) -> None:
        self.write_evidence(
            "logs/sample-source.jsonl",
            [
                self.evidence_record(
                    "e1",
                    "user",
                    "Add this to global rules: Always inspect real data before changing extraction.",
                ),
                self.evidence_record(
                    "e2",
                    "assistant",
                    "Add this to global rules: Always trust generated summaries.",
                ),
                self.evidence_record("e3", "user", "Please fix this now."),
                self.evidence_record(
                    "e4",
                    "user",
                    "For this project, do not commit generated memory outputs.",
                ),
                self.evidence_record(
                    "e5",
                    "user",
                    "PLEASE IMPLEMENT THIS PLAN: The command must write files and never fail silently.",
                ),
                self.evidence_record("e6", "user", '""'),
                self.evidence_record("e7", "user", "# Context from my IDE setup:\n\n## My request for Codex:\nNext"),
            ],
        )

        result = run_memory_generation(
            product_config_path=self.product_config,
            state_dir=self.state_dir,
            evidence_dir=self.evidence_dir,
            memory_dir=self.memory_dir,
            audits_dir=self.audits_dir,
        )

        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        items = self.read_items()
        global_rules = [item for item in items if item["memory_class"] == "global_user_rules"]
        project_rules = [item for item in items if item["memory_class"] == "project_rules"]
        recent_items = [item for item in items if item["memory_class"] == "recent_project_state"]
        summaries = [item for item in items if item["memory_class"] == "stable_project_summary"]

        self.assertEqual(len(global_rules), 1)
        self.assertIn("real data", global_rules[0]["statement"])
        self.assertFalse(any("generated summaries" in item["statement"] for item in items))
        self.assertEqual(len(project_rules), 1)
        self.assertIn("do not commit", project_rules[0]["statement"])
        self.assertFalse(any("never fail silently" in item["statement"] for item in project_rules))
        self.assertFalse(project_rules[0]["review_required"])
        self.assertFalse(any(not item["statement"] for item in items))
        self.assertFalse(any(item["statement"] == "Next" for item in items))
        self.assertTrue(any("Please fix this now" in item["statement"] for item in recent_items))
        self.assertFalse(summaries)
        self.assertTrue((self.memory_dir / "global" / "user-rules.md").exists())
        self.assertTrue((self.memory_dir / "projects" / "example-project" / "rules.md").exists())
        self.assertTrue((self.memory_dir / "_meta" / "promotion_review.jsonl").exists())
        global_content = (self.memory_dir / "global" / "user-rules.md").read_text(encoding="utf-8")
        self.assertIn("type: global-rules", global_content)
        self.assertIn("## ALWAYS DO", global_content)
        self.assertIn("## NEVER DO", global_content)

    def test_memory_generation_extracts_project_summary_and_applies_review_decisions(self) -> None:
        self.write_evidence(
            "logs/sample-source.jsonl",
            [
                self.evidence_record("e1", "user", "The project is a compact memory layer for coding agents."),
                self.evidence_record("e2", "user", "For this project, prefer generated memory outputs in temp paths."),
            ],
        )

        first = run_memory_generation(
            product_config_path=self.product_config,
            state_dir=self.state_dir,
            evidence_dir=self.evidence_dir,
            memory_dir=self.memory_dir,
            audits_dir=self.audits_dir,
        )
        self.assertTrue(first.report.success, first.report.fatal_error_summary)
        items = self.read_items()
        rule = next(item for item in items if item["memory_class"] == "project_rules")
        self.assertTrue(rule["review_required"])
        self.assertTrue(any(item["memory_class"] == "stable_project_summary" for item in items))
        (self.state_dir / "memory_review_decisions.json").write_text(
            json.dumps({"decisions": {rule["item_id"]: {"decision": "approved"}}}),
            encoding="utf-8",
        )

        second = run_memory_generation(
            product_config_path=self.product_config,
            state_dir=self.state_dir,
            evidence_dir=self.evidence_dir,
            memory_dir=self.memory_dir,
            audits_dir=self.audits_dir,
        )

        self.assertTrue(second.report.success, second.report.fatal_error_summary)
        approved_rule = next(item for item in self.read_items() if item["item_id"] == rule["item_id"])
        self.assertFalse(approved_rule["review_required"])
        self.assertEqual(approved_rule["confidence"], "strong")

    def test_project_overview_file_populates_project_memory(self) -> None:
        self.write_evidence(
            "projects/example-project.jsonl",
            [
                {
                    "evidence_id": "overview-1",
                    "evidence_type": "project_overview_file",
                    "source_adapter": "git_worktree",
                    "source_id": "example-project",
                    "project_hint": "example-project",
                    "actor_type": "project_delta",
                    "timestamp": "2026-04-18T00:00:00Z",
                    "content_surfaces": [
                        {
                            "path": "README.md",
                            "text": "# Example Project\n\nExample Project turns raw logs into:\n\n- compact memory files\n- adapter pipeline\n- renderer config",
                        }
                    ],
                    "provenance": {"path": "README.md"},
                    "metadata": {},
                },
                {
                    "evidence_id": "head-1",
                    "evidence_type": "git_head",
                    "source_adapter": "git_worktree",
                    "source_id": "example-project",
                    "project_hint": "example-project",
                    "actor_type": "project_delta",
                    "timestamp": "2026-04-18T00:00:00Z",
                    "content_surfaces": [{"path": "git.head", "text": "branch=main; head=abc"}],
                    "provenance": {},
                    "metadata": {},
                },
            ],
        )

        result = run_memory_generation(
            product_config_path=self.product_config,
            state_dir=self.state_dir,
            evidence_dir=self.evidence_dir,
            memory_dir=self.memory_dir,
            audits_dir=self.audits_dir,
        )

        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        content = (self.memory_dir / "projects" / "example-project" / "project.md").read_text(encoding="utf-8")
        self.assertIn("turns raw logs into compact memory files", content)
        self.assertNotIn("branch=main", content)

    def test_operating_directives_route_to_global_without_review(self) -> None:
        self.write_evidence(
            "logs/sample-source.jsonl",
            [
                self.evidence_record("e1", "user", "Do not narrate your process."),
                self.evidence_record("e2", "user", "Always add it to github, no need to ask."),
            ],
        )

        result = run_memory_generation(
            product_config_path=self.product_config,
            state_dir=self.state_dir,
            evidence_dir=self.evidence_dir,
            memory_dir=self.memory_dir,
            audits_dir=self.audits_dir,
        )

        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        items = self.read_items()
        global_rules = [item for item in items if item["memory_class"] == "global_user_rules"]
        self.assertEqual(len(global_rules), 2)
        self.assertTrue(all(item["scope"] == "global" for item in global_rules))
        self.assertTrue(all(not item["review_required"] for item in global_rules))

    def test_runtime_local_directive_does_not_become_project_rule(self) -> None:
        self.write_evidence(
            "logs/sample-source.jsonl",
            [
                self.evidence_record("e1", "user", "Don't try to restart the application anymore. I can do that"),
            ],
        )

        result = run_memory_generation(
            product_config_path=self.product_config,
            state_dir=self.state_dir,
            evidence_dir=self.evidence_dir,
            memory_dir=self.memory_dir,
            audits_dir=self.audits_dir,
        )

        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        items = self.read_items()
        self.assertFalse(any(item["memory_class"] == "project_rules" for item in items))
        self.assertTrue(any(item["memory_class"] == "recent_project_state" for item in items))

    def test_clause_cleanup_normalizes_common_transcription_noise(self) -> None:
        self.write_evidence(
            "logs/sample-source.jsonl",
            [self.evidence_record("e1", "user", "don't do anything ouside the plan!")],
        )

        result = run_memory_generation(
            product_config_path=self.product_config,
            state_dir=self.state_dir,
            evidence_dir=self.evidence_dir,
            memory_dir=self.memory_dir,
            audits_dir=self.audits_dir,
        )

        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        statement = self.read_items()[0]["statement"]
        self.assertEqual(statement, "don't do anything outside the plan!")

    def test_memory_generation_prunes_stale_recent_context(self) -> None:
        stale = self.evidence_record("e1", "user", "Please fix this now.")
        stale["timestamp"] = "2026-01-01T00:00:00Z"
        current = self.evidence_record("e2", "user", "Please continue this active task.")
        self.write_evidence("logs/sample-source.jsonl", [stale, current])

        result = run_memory_generation(
            product_config_path=self.product_config,
            state_dir=self.state_dir,
            evidence_dir=self.evidence_dir,
            memory_dir=self.memory_dir,
            audits_dir=self.audits_dir,
        )

        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        statements = [item["statement"] for item in self.read_items()]
        self.assertNotIn("Please fix this now.", statements)
        self.assertIn("Please continue this active task.", statements)

    def test_memory_generation_filters_long_prompt_noise_from_recent_context(self) -> None:
        noisy = self.evidence_record(
            "e1",
            "user",
            "Use this as your single prompt to Codex. IMPORTANT OPERATING STYLE " + ("do not narrate " * 40),
        )
        useful = self.evidence_record("e2", "user", "Please continue implementing the renderer cleanup.")
        self.write_evidence("logs/sample-source.jsonl", [noisy, useful])

        result = run_memory_generation(
            product_config_path=self.product_config,
            state_dir=self.state_dir,
            evidence_dir=self.evidence_dir,
            memory_dir=self.memory_dir,
            audits_dir=self.audits_dir,
        )

        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        content = (self.memory_dir / "projects" / "example-project" / "recent.md").read_text(encoding="utf-8")
        self.assertNotIn("single prompt to Codex", content)
        self.assertIn("renderer cleanup", content)
        self.assertLess(len(content), 5000)

    def test_memory_generation_filters_low_signal_recent_chatter(self) -> None:
        self.write_evidence(
            "logs/sample-source.jsonl",
            [
                self.evidence_record("e1", "user", "Are you testing with real data ?"),
                self.evidence_record("e2", "user", "push to git please"),
                self.evidence_record("e3", "user", "OK, create the plan"),
                self.evidence_record("e4", "user", "Where are the dos and don'ts located?"),
                self.evidence_record("e5", "user", "Should have a llm second pass for records under projects"),
                self.evidence_record("e7", "user", "Ok, plan next phase"),
                self.evidence_record("e8", "user", "notices: 754 down from 758 - is this supposed to be good progress?"),
                self.evidence_record("e9", "user", "do the work, don't explain it. Just output final result, go"),
                self.evidence_record("e10", "user", "whats next?"),
                self.evidence_record("e6", "user", "Please continue implementing the renderer cleanup."),
            ],
        )

        result = run_memory_generation(
            product_config_path=self.product_config,
            state_dir=self.state_dir,
            evidence_dir=self.evidence_dir,
            memory_dir=self.memory_dir,
            audits_dir=self.audits_dir,
        )

        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        content = (self.memory_dir / "projects" / "example-project" / "recent.md").read_text(encoding="utf-8")
        self.assertNotIn("Are you testing", content)
        self.assertNotIn("push to git", content)
        self.assertNotIn("create the plan", content)
        self.assertNotIn("dos and don'ts located", content)
        self.assertNotIn("llm second pass", content)
        self.assertNotIn("plan next phase", content)
        self.assertNotIn("754 down", content)
        self.assertNotIn("don't explain", content)
        self.assertNotIn("whats next", content)
        self.assertIn("renderer cleanup", content)

    def test_memory_generation_does_not_count_duplicate_log_shapes_as_repetition(self) -> None:
        repeated_text = "Please continue implementing the renderer cleanup."
        first = self.evidence_record("e1", "user", repeated_text)
        second = self.evidence_record("e2", "user", repeated_text)
        first["timestamp"] = "2026-04-18T00:00:00.001Z"
        second["timestamp"] = "2026-04-18T00:00:00.002Z"
        first["provenance"]["source_id"] = "same-source"
        second["provenance"]["source_id"] = "same-source"
        self.write_evidence("logs/sample-source.jsonl", [first, second])

        result = run_memory_generation(
            product_config_path=self.product_config,
            state_dir=self.state_dir,
            evidence_dir=self.evidence_dir,
            memory_dir=self.memory_dir,
            audits_dir=self.audits_dir,
        )

        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        items = [item for item in self.read_items() if item["statement"] == repeated_text]
        self.assertEqual(len(items), 1)
        self.assertEqual(len(items[0]["evidence_ids"]), 1)
        self.assertEqual(items[0]["promotion_state"], "candidate")

    def test_memory_generation_skips_unresolved_project_bucket(self) -> None:
        self.write_evidence(
            "logs/unresolved.jsonl",
            [dict(self.evidence_record("e1", "user", "Please continue implementing the renderer cleanup."), project_hint="projects")],
        )

        result = run_memory_generation(
            product_config_path=self.product_config,
            state_dir=self.state_dir,
            evidence_dir=self.evidence_dir,
            memory_dir=self.memory_dir,
            audits_dir=self.audits_dir,
        )

        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        self.assertFalse((self.memory_dir / "projects" / "projects").exists())

    def test_memory_generation_keeps_global_rules_from_unresolved_project_records(self) -> None:
        self.write_evidence(
            "logs/unresolved.jsonl",
            [
                dict(
                    self.evidence_record("e1", "user", "Do not narrate your process."),
                    project_hint="projects",
                )
            ],
        )

        result = run_memory_generation(
            product_config_path=self.product_config,
            state_dir=self.state_dir,
            evidence_dir=self.evidence_dir,
            memory_dir=self.memory_dir,
            audits_dir=self.audits_dir,
        )

        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        content = (self.memory_dir / "global" / "user-rules.md").read_text(encoding="utf-8")
        self.assertIn("Do not narrate your process", content)

    def test_stop_explanation_preference_becomes_global_rule(self) -> None:
        self.write_evidence(
            "logs/sample-source.jsonl",
            [self.evidence_record("e1", "user", "stop spitting explanation texts, it is killing my token limits")],
        )

        result = run_memory_generation(
            product_config_path=self.product_config,
            state_dir=self.state_dir,
            evidence_dir=self.evidence_dir,
            memory_dir=self.memory_dir,
            audits_dir=self.audits_dir,
        )

        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        content = (self.memory_dir / "global" / "user-rules.md").read_text(encoding="utf-8")
        self.assertIn("stop spitting explanation texts", content)

    def test_no_fallback_should_exist_becomes_project_rule_not_recent(self) -> None:
        self.write_evidence(
            "logs/sample-source.jsonl",
            [self.evidence_record("e1", "user", "No fallback should exist as answers have to be evidence based.")],
        )

        result = run_memory_generation(
            product_config_path=self.product_config,
            state_dir=self.state_dir,
            evidence_dir=self.evidence_dir,
            memory_dir=self.memory_dir,
            audits_dir=self.audits_dir,
        )

        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        rules = (self.memory_dir / "projects" / "example-project" / "rules.md").read_text(encoding="utf-8")
        recent = (self.memory_dir / "projects" / "example-project" / "recent.md").read_text(encoding="utf-8")
        self.assertIn("No fallback should exist", rules)
        self.assertNotIn("No fallback should exist", recent)

    def test_memory_generation_respects_plain_markdown_renderer_flags(self) -> None:
        payload = json.loads(self.product_config.read_text(encoding="utf-8"))
        payload["markdown_output"]["mode"] = "plain_markdown"
        payload["markdown_output"]["enable_frontmatter"] = False
        payload["markdown_output"]["enable_tags"] = False
        payload["markdown_output"]["enable_wikilinks"] = False
        self.product_config.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        self.write_evidence(
            "logs/sample-source.jsonl",
            [
                self.evidence_record(
                    "e1",
                    "user",
                    "Add this to global rules: Always inspect real data before changing extraction.",
                ),
            ],
        )

        result = run_memory_generation(
            product_config_path=self.product_config,
            state_dir=self.state_dir,
            evidence_dir=self.evidence_dir,
            memory_dir=self.memory_dir,
            audits_dir=self.audits_dir,
        )

        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        content = (self.memory_dir / "global" / "user-rules.md").read_text(encoding="utf-8")
        self.assertFalse(content.startswith("---"))
        self.assertNotIn("[[", content)

    def test_memory_generation_consumes_real_sample_ingest_path(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        sessions_root = self.temp_dir / "sessions"
        source_config = self.temp_dir / "source_roots.json"
        normalized_dir = self.temp_dir / "normalized"
        schema_path = repo_root / "schema" / "normalization_catalog.json"
        example_log = repo_root / "examples" / "source-logs" / "representative-session.jsonl"
        target_log = (
            sessions_root
            / "2026"
            / "02"
            / "26"
            / "rollout-2026-02-26T21-48-04-019c9cff-0337-77e0-9ba6-a4f6dc75a92e.jsonl"
        )
        target_log.parent.mkdir(parents=True)
        shutil.copyfile(example_log, target_log)

        self.project_root.mkdir(parents=True)
        subprocess.run(["git", "-C", str(self.project_root), "init"], check=True, capture_output=True, text=True)
        (self.project_root / "README.md").write_text("# Example\n", encoding="utf-8")
        source_config.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "roots": [
                        {
                            "root_alias": "example_sessions",
                            "absolute_path": str(sessions_root),
                            "enabled": True,
                            "recursive": True,
                            "include_glob": "**/*.jsonl",
                        }
                    ],
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        payload = json.loads(self.product_config.read_text(encoding="utf-8"))
        payload["log_sources"][0]["root_alias"] = "example_sessions"
        payload["log_sources"][0]["absolute_path"] = str(sessions_root)
        self.product_config.write_text(json.dumps(payload, indent=2), encoding="utf-8")

        self.assertTrue(run_discovery(source_config, self.state_dir).report.success)
        self.assertTrue(
            run_normalization(
                config_path=source_config,
                state_dir=self.state_dir,
                schema_path=schema_path,
                normalized_dir=normalized_dir,
                audits_dir=self.audits_dir,
            ).report.success
        )
        self.assertTrue(
            run_ingest(
                product_config_path=self.product_config,
                state_dir=self.state_dir,
                normalized_dir=normalized_dir,
                evidence_dir=self.evidence_dir,
                audits_dir=self.audits_dir,
            ).report.success
        )

        result = run_memory_generation(
            product_config_path=self.product_config,
            state_dir=self.state_dir,
            evidence_dir=self.evidence_dir,
            memory_dir=self.memory_dir,
            audits_dir=self.audits_dir,
        )

        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        self.assertGreater(sum(result.report.item_counts.values()), 0)
        self.assertTrue((self.memory_dir / "global" / "user-rules.md").exists())
        self.assertTrue(list((self.memory_dir / "projects").glob("*/recent.md")))


if __name__ == "__main__":
    unittest.main()
