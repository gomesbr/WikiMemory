from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from sessionmemory.discovery import run_discovery
from sessionmemory.ingest import run_ingest
from sessionmemory.memory_generation import run_memory_generation
from sessionmemory.normalization import run_normalization
from sessionmemory.product_config import default_product_config


class MemoryGenerationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="sessionmemory-memory-"))
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
        self.assertTrue(any("fix this now" in item["statement"] for item in recent_items))
        self.assertFalse(summaries)
        self.assertTrue((self.memory_dir / "global" / "user-rules.md").exists())
        self.assertTrue((self.memory_dir / "projects" / "example-project" / "rules.md").exists())
        self.assertTrue((self.memory_dir / "global" / "memory-health.md").exists())
        self.assertTrue((self.memory_dir / "global" / "memory-change-log.md").exists())
        self.assertTrue((self.memory_dir / "projects" / "example-project" / "continuations.md").exists())
        self.assertTrue((self.memory_dir / "_meta" / "promotion_review.jsonl").exists())
        global_content = (self.memory_dir / "global" / "user-rules.md").read_text(encoding="utf-8")
        self.assertIn("type: global-rules", global_content)
        self.assertIn("memory_role: directive", global_content)
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

    def test_confirmed_rule_count_matches_rendered_global_buckets(self) -> None:
        statements = [
            "Add this to global rules: Always verify evidence before changing memory logic.",
            "Add this to global rules: Always keep provenance attached to extracted memory.",
            "Add this to global rules: Always check real data before promoting a memory fix.",
            "Add this to global rules: Always explain how the fix generalizes.",
            "Add this to global rules: Do not remove source linkage from evidence rows.",
            "Add this to global rules: Do not auto-start backlog items without confirmation.",
            "Add this to global rules: Do not hide unresolved quality issues.",
            "Add this to global rules: Do not treat mock data as production truth.",
            "Add this to global rules: Ask for clarification if the request is materially ambiguous.",
            "Add this to global rules: Keep project backlog items as options, not commands.",
            "Add this to global rules: If confidence is low, preserve uncertainty in the output.",
            "Add this to global rules: Use project memory as context only until the consumer confirms direction.",
            "Add this to global rules: Always validate the smallest relevant path first.",
        ]
        records = [
            self.evidence_record(f"e{index + 1}", "user", statement)
            for index, statement in enumerate(statements)
        ]
        self.write_evidence("logs/sample-source.jsonl", records)

        result = run_memory_generation(
            product_config_path=self.product_config,
            state_dir=self.state_dir,
            evidence_dir=self.evidence_dir,
            memory_dir=self.memory_dir,
            audits_dir=self.audits_dir,
        )

        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        global_content = (self.memory_dir / "global" / "user-rules.md").read_text(encoding="utf-8")
        self.assertIn("13 explicit rule(s) are listed above by behavior bucket.", global_content)

    def test_memory_generation_applies_consumer_rule_override_commands(self) -> None:
        self.write_evidence(
            "logs/sample-source.jsonl",
            [
                self.evidence_record("e1", "user", "Do not narrate your process."),
                self.evidence_record(
                    "e2",
                    "user",
                    'Memory command: replace rule: "Do not narrate your process." -> "Keep narration brief unless I ask for more detail."',
                ),
                self.evidence_record(
                    "e3",
                    "user",
                    "Memory command: add project rule: Always show backlog items as options before starting work.",
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
        items = self.read_items()
        self.assertFalse(any(item["statement"] == "Do not narrate your process." for item in items))
        replaced = next(item for item in items if "Keep narration brief" in item["statement"])
        self.assertEqual(replaced["memory_class"], "project_rules")
        self.assertTrue(replaced["locked_by_consumer"])
        self.assertEqual(replaced["authority"], "consumer_override")
        added = next(
            item
            for item in items
            if "Always show backlog items as options" in item["statement"] and item.get("authority") == "consumer_override"
        )
        self.assertEqual(added["memory_class"], "project_rules")
        self.assertTrue(added["locked_by_consumer"])
        override_state = json.loads((self.state_dir / "memory_rule_overrides.json").read_text(encoding="utf-8"))
        self.assertEqual(override_state["command_count"], 2)

    def test_memory_generation_tracks_one_off_exceptions(self) -> None:
        self.write_evidence(
            "logs/sample-source.jsonl",
            [
                self.evidence_record(
                    "e1",
                    "user",
                    "Memory command: one-off project exception: Ignore the normal backlog ordering and only review the bugfix thread today.",
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
        exceptions = (self.memory_dir / "global" / "active-exceptions.md").read_text(encoding="utf-8")
        self.assertIn("Ignore the normal backlog ordering", exceptions)

    def test_memory_generation_renders_daily_conversation_pages(self) -> None:
        first = self.evidence_record("e1", "user", "Please continue implementing the renderer cleanup.")
        first["timestamp"] = "2026-04-18T10:00:00Z"
        second = self.evidence_record("e2", "assistant", "I updated the cleanup flow and validated the narrow path.")
        second["timestamp"] = "2026-04-18T10:05:00Z"
        third = self.evidence_record("e3", "user", "Now fix the retry behavior too.")
        third["timestamp"] = "2026-04-19T09:00:00Z"
        self.write_evidence("logs/sample-source.jsonl", [first, second, third])

        result = run_memory_generation(
            product_config_path=self.product_config,
            state_dir=self.state_dir,
            evidence_dir=self.evidence_dir,
            memory_dir=self.memory_dir,
            audits_dir=self.audits_dir,
        )

        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        index_content = (self.memory_dir / "global" / "daily-conversations.md").read_text(encoding="utf-8")
        day_one = (self.memory_dir / "daily-conversations" / "2026-04-18.md").read_text(encoding="utf-8")
        day_two = (self.memory_dir / "daily-conversations" / "2026-04-19.md").read_text(encoding="utf-8")
        self.assertIn("memory/daily-conversations/2026-04-18.md", index_content)
        self.assertIn("memory/daily-conversations/2026-04-19.md", index_content)
        self.assertIn("10:00 User: Please continue implementing the renderer cleanup.", day_one)
        self.assertIn("10:05 Assistant: I updated the cleanup flow and validated the narrow path.", day_one)
        self.assertIn("09:00 User: Now fix the retry behavior too.", day_two)

    def test_memory_generation_uses_llm_to_render_continuations(self) -> None:
        self.write_evidence(
            "logs/sample-source.jsonl",
            [
                self.evidence_record("e1", "user", "Point the agent to START_HERE_FOR_AGENT.md and finish bootstrap configuration."),
                self.evidence_record("e2", "user", "Understand the refresh and lint failures holistically, then propose the fix plan."),
                self.evidence_record("e3", "user", "Add robust real-data tests so larger datasets can be validated safely."),
            ],
        )

        def fake_llm_client(system_prompt: str, payload: dict[str, object], model: str) -> dict[str, object]:
            self.assertIn("threads", system_prompt)
            self.assertEqual(payload["project"], "example-project")
            return {
                "threads": [
                    "Finish bootstrap and agent configuration flow for SessionMemory onboarding.",
                    "Stabilize the refresh-plus-lint workflow and validate it on real data.",
                    "Expand robust real-data test coverage for larger memory corpora.",
                ]
            }

        result = run_memory_generation(
            product_config_path=self.product_config,
            state_dir=self.state_dir,
            evidence_dir=self.evidence_dir,
            memory_dir=self.memory_dir,
            audits_dir=self.audits_dir,
            llm_client=fake_llm_client,
        )

        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        continuations = (self.memory_dir / "projects" / "example-project" / "continuations.md").read_text(encoding="utf-8")
        self.assertIn("Finish bootstrap and agent configuration flow", continuations)
        self.assertIn("Stabilize the refresh-plus-lint workflow", continuations)
        self.assertNotIn("understand the refresh and lint failures holistically", continuations.lower())

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
                            "text": "# Example Project\n\napproval_ui/\n\nExample Project turns raw logs into:\n\n- compact memory files\n- adapter pipeline\n- renderer config",
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
        self.assertIn("memory_role: descriptive", content)
        self.assertIn("turns raw logs into compact memory files", content)
        self.assertNotIn("approval_ui/", content)
        self.assertNotIn("branch=main", content)

    def test_project_summary_sections_do_not_treat_config_or_constraints_as_purpose(self) -> None:
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
                            "text": "# Example Project\n\nDeterministic trading system scaffold with scoring engine.\n\nSet BROKER_ADAPTER_MODE=mock in `.env`.\n\nGlobal kill switch blocks trading.",
                        }
                    ],
                    "provenance": {"path": "README.md"},
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
        purpose = content.split("## PURPOSE", 1)[1].split("## CORE COMPONENTS", 1)[0]
        constraints = content.split("## KEY CONSTRAINTS", 1)[1].split("## OPEN PROBLEMS", 1)[0]
        self.assertIn("Deterministic trading system", purpose)
        self.assertNotIn("BROKER_ADAPTER_MODE", purpose)
        self.assertNotIn("kill switch", purpose)
        self.assertIn("kill switch", constraints)

    def test_conversational_goal_correction_does_not_become_project_purpose(self) -> None:
        self.write_evidence(
            "logs/sample-source.jsonl",
            [
                self.evidence_record(
                    "e1",
                    "user",
                    "Nah, this got even more complicated. This should be simple. Goal is to have the agent stop before more damage is done.",
                ),
                self.evidence_record("e2", "user", "Goal is to avoid wash sale at all costs."),
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
        self.assertIn("avoid wash sale", content)
        self.assertNotIn("got even more complicated", content)

    def test_clean_slate_compatibility_guidance_becomes_project_rule_not_purpose(self) -> None:
        self.write_evidence(
            "logs/sample-source.jsonl",
            [
                self.evidence_record(
                    "e1",
                    "user",
                    "The previous v1 system was not in use while v2 was being developed, so no compatibility is needed. Treat the system as new.",
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
        project = (self.memory_dir / "projects" / "example-project" / "project.md").read_text(encoding="utf-8")
        rules = (self.memory_dir / "projects" / "example-project" / "rules.md").read_text(encoding="utf-8")
        expected = (
            "When developing a new Example Project version that is not yet in production use, do not preserve backward "
            "compatibility with the previous version by default. Treat the new version as a clean system unless "
            "the user explicitly asks for migration or compatibility support."
        )
        self.assertNotIn("Treat the system as new", project)
        self.assertNotIn("compatibility with the previous version", project)
        self.assertIn(expected, rules)

    def test_vague_project_summary_is_not_rendered_as_purpose(self) -> None:
        self.write_evidence(
            "logs/sample-source.jsonl",
            [self.evidence_record("e1", "user", "Every time you make a change, think about the system as new.")],
        )

        result = run_memory_generation(
            product_config_path=self.product_config,
            state_dir=self.state_dir,
            evidence_dir=self.evidence_dir,
            memory_dir=self.memory_dir,
            audits_dir=self.audits_dir,
        )

        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        project = (self.memory_dir / "projects" / "example-project" / "project.md").read_text(encoding="utf-8")
        rules = (self.memory_dir / "projects" / "example-project" / "rules.md").read_text(encoding="utf-8")
        self.assertNotIn("Every time you make a change", project)
        self.assertNotIn("think about the system as new", project)
        self.assertIn("do not preserve backward compatibility", rules)

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
        self.assertEqual(statement, "Stay inside the agreed plan unless the user explicitly changes scope.")

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
        self.assertTrue(any("continue this active task" in statement for statement in statements))

    def test_memory_generation_keeps_latest_project_recent_even_if_old(self) -> None:
        stale = self.evidence_record("e1", "user", "Please continue the last known aitrader work thread.")
        stale["timestamp"] = "2025-01-01T00:00:00Z"
        self.write_evidence("logs/sample-source.jsonl", [stale])

        result = run_memory_generation(
            product_config_path=self.product_config,
            state_dir=self.state_dir,
            evidence_dir=self.evidence_dir,
            memory_dir=self.memory_dir,
            audits_dir=self.audits_dir,
        )

        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        recent = (self.memory_dir / "projects" / "example-project" / "recent.md").read_text(encoding="utf-8")
        self.assertIn("continue the last known aitrader work thread", recent.lower())
        self.assertNotIn("No current focus extracted yet.", recent)

    def test_memory_generation_preserves_consumer_profile_artifacts(self) -> None:
        self.write_evidence("logs/sample-source.jsonl", [self.evidence_record("e1", "user", "Please continue implementing the renderer cleanup.")])
        global_dir = self.memory_dir / "global"
        meta_dir = self.memory_dir / "_meta"
        global_dir.mkdir(parents=True, exist_ok=True)
        meta_dir.mkdir(parents=True, exist_ok=True)
        (global_dir / "consumer-profile.md").write_text("# Consumer Profile\n", encoding="utf-8")
        (meta_dir / "consumer_profile.json").write_text('{"ok": true}\n', encoding="utf-8")
        (meta_dir / "consumer_style.json").write_text('{"tone": "direct"}\n', encoding="utf-8")

        result = run_memory_generation(
            product_config_path=self.product_config,
            state_dir=self.state_dir,
            evidence_dir=self.evidence_dir,
            memory_dir=self.memory_dir,
            audits_dir=self.audits_dir,
        )

        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        self.assertTrue((global_dir / "consumer-profile.md").exists())
        self.assertTrue((meta_dir / "consumer_profile.json").exists())
        self.assertTrue((meta_dir / "consumer_style.json").exists())

    def test_timeline_resolution_removes_resolved_open_question_from_recent(self) -> None:
        question = self.evidence_record("e1", "user", "Should the memory pipeline use LLM extraction for project records?")
        question["timestamp"] = "2026-04-01T00:00:00Z"
        decision = self.evidence_record("e2", "user", "We decided the memory pipeline should use LLM extraction for project records.")
        decision["timestamp"] = "2026-04-18T00:00:00Z"
        self.write_evidence("logs/sample-source.jsonl", [question, decision])

        result = run_memory_generation(
            product_config_path=self.product_config,
            state_dir=self.state_dir,
            evidence_dir=self.evidence_dir,
            memory_dir=self.memory_dir,
            audits_dir=self.audits_dir,
        )

        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        recent = (self.memory_dir / "projects" / "example-project" / "recent.md").read_text(encoding="utf-8")
        self.assertNotIn("Track this unresolved question", recent)
        candidates = [
            json.loads(line)
            for line in (self.memory_dir / "_meta" / "candidates.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertTrue(any(candidate["item_type"] == "open_question" and candidate["temporal_status"] == "resolved" for candidate in candidates))

    def test_low_confidence_candidates_are_retained_in_metadata(self) -> None:
        self.write_evidence(
            "logs/sample-source.jsonl",
            [self.evidence_record("e1", "user", "Maybe the project memory should include a review queue for inferred rules?")],
        )

        result = run_memory_generation(
            product_config_path=self.product_config,
            state_dir=self.state_dir,
            evidence_dir=self.evidence_dir,
            memory_dir=self.memory_dir,
            audits_dir=self.audits_dir,
        )

        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        candidates = [
            json.loads(line)
            for line in (self.memory_dir / "_meta" / "candidates.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertTrue(candidates)
        self.assertTrue(any(candidate["confidence"] in {"medium", "low"} for candidate in candidates))

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
        self.assertIn("llm second pass", content)
        self.assertNotIn("plan next phase", content)
        self.assertNotIn("754 down", content)
        self.assertNotIn("don't explain", content)
        self.assertNotIn("whats next", content)
        self.assertIn("renderer cleanup", content)

    def test_memory_generation_filters_scaffold_context_from_recent(self) -> None:
        self.write_evidence(
            "logs/sample-source.jsonl",
            [
                self.evidence_record("e1", "user", "Current context: below is the list of skills that can be used."),
                self.evidence_record(
                    "e2",
                    "user",
                    "Current context: each entry includes a name, description, and file path so you can open the source for full instructions when using a specific skill.",
                ),
                self.evidence_record(
                    "e3",
                    "user",
                    "Current context: provide implementation plans or code-level guidance for requested build tasks.",
                ),
                self.evidence_record("e4", "user", "Please continue implementing the ingest retry cleanup."),
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
        self.assertNotIn("list of skills", content)
        self.assertNotIn("specific skill", content)
        self.assertNotIn("implementation plans or code-level guidance", content)
        self.assertIn("ingest retry cleanup", content)

    def test_memory_generation_filters_cross_project_recent_noise(self) -> None:
        self.write_evidence(
            "logs/sample-source.jsonl",
            [
                self.evidence_record("e1", "user", "Current context: reuse for CodexClaw UI work."),
                self.evidence_record("e2", "user", "Current context: keep a consistent UI design language across apps."),
                self.evidence_record("e3", "user", "Please continue implementing the aitrader execution retry cleanup."),
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
        self.assertNotIn("CodexClaw UI work", content)
        self.assertNotIn("design language across apps", content)
        self.assertIn("aitrader execution retry cleanup", content)

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
        items = [item for item in self.read_items() if "renderer cleanup" in item["statement"]]
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
        self.assertIn("process narration", content)

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
        self.assertIn("process narration", content)

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
        self.assertIn("memory_role: directive", rules)
        self.assertIn("memory_role: descriptive", recent)
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
        (self.project_root / "README.md").write_text(
            "# Example\n\nExample Project is a compact memory validation fixture for real sample ingest tests.\n",
            encoding="utf-8",
        )
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
