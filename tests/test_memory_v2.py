from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from wikimemory.memory_v2 import correct_project_from_statement, parse_daily_chat_markdown, render_memory_v2, rule_bucket, split_rule_statement, run_memory_v2


class MemoryV2Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="wikimemory-memory-v2-"))
        self.input_dir = self.temp_dir / "daily"
        self.output_dir = self.temp_dir / "memory_v2_pilot"
        self.state_dir = self.temp_dir / "state"
        self.project_root_dir = self.temp_dir / "projects"
        self.input_dir.mkdir(parents=True)
        ai_trader_root = self.project_root_dir / "AITrader"
        (ai_trader_root / "src").mkdir(parents=True)
        (ai_trader_root / "README.md").write_text("# AITrader\n\nDeterministic trading research app.\n", encoding="utf-8")
        (ai_trader_root / "src" / "main.py").write_text("print('ok')\n", encoding="utf-8")
        self.day_file = self.input_dir / "2026-03-13-codex-chat.md"
        self.day_file.write_text(
            """# Codex Chat Export - 2026-03-13

## 2026-03-13T10:00:00.000Z - User

<!-- source: raw.jsonl:10 -->

```text
Add this to global rules: always validate memory changes with real data.
```

## 2026-03-13T10:01:00.000Z - Agent

<!-- source: raw.jsonl:11 -->

```text
I will validate with the real sample before changing the renderer.
```

## 2026-03-13T10:02:00.000Z - User

<!-- source: raw.jsonl:12 -->

```text
For Ai Trader, the project is a deterministic autonomous trading system.
```
""",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def fake_llm(self, system_prompt: str, payload: dict[str, object], model: str) -> dict[str, object]:
        if "messages" in payload:
            messages = payload["messages"]
            self.assertTrue(any("real data" in message["text"] for message in messages))
            self.assertFalse(any("source:" in message["text"] for message in messages))
            return {
                "candidates": [
                    {
                        "source_day": "2026-03-13",
                        "project": "global",
                        "memory_class": "global_rule",
                        "memory_role": "rule",
                        "agent_facing_statement": "Always validate memory changes with real data before treating them as correct.",
                        "confidence": "explicit",
                        "temporal_status": "durable",
                        "evidence_refs": [{"source_day": "2026-03-13", "message_index": 1, "timestamp": "2026-03-13T10:00:00.000Z", "actor": "User"}],
                    },
                    {
                        "source_day": "2026-03-13",
                        "project": "ai-trader",
                        "memory_class": "project_summary",
                        "memory_role": "purpose",
                        "agent_facing_statement": "Ai Trader is a deterministic autonomous trading system.",
                        "confidence": "strong",
                        "temporal_status": "durable",
                        "evidence_refs": [{"source_day": "2026-03-13", "message_index": 3, "timestamp": "2026-03-13T10:02:00.000Z", "actor": "User"}],
                    },
                ]
            }
        return {"items": payload["candidates"]}

    def test_parse_daily_chat_markdown_preserves_verbatim_messages_without_source_comments(self) -> None:
        messages = parse_daily_chat_markdown(self.day_file)

        self.assertEqual(len(messages), 3)
        self.assertEqual(messages[0].actor, "User")
        self.assertIn("Add this to global rules", messages[0].text)
        self.assertEqual(messages[0].source_ref, "raw.jsonl:10")
        self.assertFalse(any("source:" in message.text for message in messages))

    def test_memory_v2_generates_pilot_memory_with_metadata(self) -> None:
        result = run_memory_v2(
            input_dir=self.input_dir,
            output_dir=self.output_dir,
            state_dir=self.state_dir,
            days=["2026-03-13"],
            llm_client=self.fake_llm,
            model="stub-model",
        )

        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        self.assertEqual(result.report.item_count, 2)
        global_rules = (self.output_dir / "global" / "user-rules.md").read_text(encoding="utf-8")
        project_memory = (self.output_dir / "projects" / "ai-trader" / "project.md").read_text(encoding="utf-8")
        daily_meta = json.loads((self.output_dir / "_meta" / "daily" / "2026-03-13.json").read_text(encoding="utf-8"))

        self.assertIn("Always validate memory changes with real data", global_rules)
        self.assertNotIn("Add this to global rules", global_rules)
        self.assertIn("Ai Trader is a deterministic autonomous trading system", project_memory)
        self.assertIn("[[projects/ai-trader/recent|Ai Trader Recent]]", project_memory)
        self.assertIn("[[projects/ai-trader/rules|Ai Trader Rules]]", project_memory)
        self.assertIn("[[global/user-rules|Global User Rules]]", project_memory)
        self.assertNotIn("[[Ai Trader Recent]]", project_memory)
        self.assertEqual(daily_meta["messages"][0]["text"], "Add this to global rules: always validate memory changes with real data.")

    def test_memory_v2_normalizes_llm_schema_variants(self) -> None:
        def variant_llm(system_prompt: str, payload: dict[str, object], model: str) -> dict[str, object]:
            if "messages" in payload:
                return {
                    "candidates": [
                        {
                            "candidate_id": "candidate-1",
                            "source_day": "2026-03-13",
                            "project": "OpenBrain",
                            "memory_class": "workflow_preference",
                            "memory_role": "instruction",
                            "agent_facing_statement": "Use evidence-family-first mining before assigning taxonomy labels.",
                            "confidence": 0.99,
                            "temporal_status": "active",
                            "evidence_refs": [1],
                        }
                    ]
                }
            return {
                "items": [
                    {
                        "item_id": "item-1",
                        "project": "OpenBrain",
                        "memory_class": "workflow_preference",
                        "memory_role": "instruction",
                        "agent_facing_statement": "Use evidence-family-first mining before assigning taxonomy labels.",
                        "confidence": 0.99,
                        "temporal_status": "active",
                        "supporting_candidate_ids": ["candidate-1"],
                    }
                ]
            }

        result = run_memory_v2(
            input_dir=self.input_dir,
            output_dir=self.output_dir,
            state_dir=self.state_dir,
            days=["2026-03-13"],
            llm_client=variant_llm,
            model="stub-model",
        )

        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        self.assertEqual(result.report.candidate_count, 1)
        rules = (self.output_dir / "projects" / "open-brain" / "rules.md").read_text(encoding="utf-8")
        merged = json.loads((self.output_dir / "_meta" / "merged_items.json").read_text(encoding="utf-8"))["items"][0]

        self.assertIn("Use evidence-family-first mining", rules)
        self.assertEqual(merged["project"], "open-brain")
        self.assertEqual(merged["memory_class"], "project_rule")
        self.assertEqual(merged["confidence"], "strong")
        self.assertEqual(merged["evidence_refs"][0]["message_index"], 1)

    def test_memory_v2_uses_project_readme_and_tree_in_merge_and_render(self) -> None:
        def context_llm(system_prompt: str, payload: dict[str, object], model: str) -> dict[str, object]:
            if "messages" in payload:
                return {
                    "candidates": [
                        {
                            "candidate_id": "candidate-project",
                            "source_day": "2026-03-13",
                            "project": "ai-trader",
                            "memory_class": "project_summary",
                            "memory_role": "purpose",
                            "agent_facing_statement": "Ai Trader is a trading project.",
                            "confidence": "strong",
                            "temporal_status": "durable",
                            "evidence_refs": [3],
                        }
                    ]
                }
            contexts = payload["project_contexts"]
            self.assertIn("ai-trader", contexts)
            self.assertIn("Deterministic trading research app", contexts["ai-trader"]["readmes"][0]["content"])
            self.assertIn("src/", "\n".join(contexts["ai-trader"]["directory_tree"]))
            return {
                "items": [
                    {
                        "item_id": "item-project",
                        "project": "ai-trader",
                        "memory_class": "project_summary",
                        "memory_role": "purpose",
                        "agent_facing_statement": "Ai Trader is a deterministic trading research app.",
                        "confidence": "strong",
                        "temporal_status": "durable",
                        "supporting_candidate_ids": ["candidate-project"],
                    }
                ]
            }

        result = run_memory_v2(
            input_dir=self.input_dir,
            output_dir=self.output_dir,
            state_dir=self.state_dir,
            days=["2026-03-13"],
            project_root_dir=self.project_root_dir,
            llm_client=context_llm,
            model="stub-model",
        )

        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        project_memory = (self.output_dir / "projects" / "ai-trader" / "project.md").read_text(encoding="utf-8")
        project_contexts = json.loads((self.output_dir / "_meta" / "project_contexts.json").read_text(encoding="utf-8"))

        self.assertIn("Ai Trader is a deterministic trading research app", project_memory)
        self.assertIn("## DIRECTORY TREE", project_memory)
        self.assertIn("src/", project_memory)
        self.assertIn("main.py", project_memory)
        self.assertIn("README.md", "\n".join(project_contexts["ai-trader"]["directory_tree"]))

    def test_project_tree_is_not_truncated(self) -> None:
        ai_trader_root = self.project_root_dir / "AITrader"
        for index in range(120):
            path = ai_trader_root / "src" / "scripts" / f"script_{index:03}.ts"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("export {}\n", encoding="utf-8")

        def no_item_llm(system_prompt: str, payload: dict[str, object], model: str) -> dict[str, object]:
            if "messages" in payload:
                return {"candidates": []}
            return {"items": []}

        result = run_memory_v2(
            input_dir=self.input_dir,
            output_dir=self.output_dir,
            state_dir=self.state_dir,
            days=["2026-03-13"],
            project_root_dir=self.project_root_dir,
            llm_client=no_item_llm,
            model="stub-model",
        )

        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        project_memory = (self.output_dir / "projects" / "ai-trader" / "project.md").read_text(encoding="utf-8")
        self.assertIn("script_119.ts", project_memory)
        self.assertNotIn("tree truncated", project_memory)

    def test_render_suppresses_project_rules_already_global(self) -> None:
        items = [
            {
                "item_id": "global-completion",
                "project": "global",
                "memory_class": "global_rule",
                "memory_role": "rule",
                "agent_facing_statement": "For task deliverable outputs, always include a Completion Matrix mapping each acceptance criterion to concrete evidence in pass/fail form.",
                "confidence": "strong",
                "temporal_status": "durable",
                "evidence_refs": [{"source_day": "2026-03-13", "message_index": 1}],
            },
            {
                "item_id": "project-completion",
                "project": "codexclaw",
                "memory_class": "project_rule",
                "memory_role": "rule",
                "agent_facing_statement": "Task delivery responses must include a Completion Matrix mapping each acceptance criterion to concrete evidence.",
                "confidence": "strong",
                "temporal_status": "durable",
                "evidence_refs": [{"source_day": "2026-03-13", "message_index": 2}],
            },
            {
                "item_id": "project-specific",
                "project": "codexclaw",
                "memory_class": "project_rule",
                "memory_role": "rule",
                "agent_facing_statement": "Strip internal tracker payload blocks from CodexClaw user-facing responses.",
                "confidence": "strong",
                "temporal_status": "durable",
                "evidence_refs": [{"source_day": "2026-03-13", "message_index": 3}],
            },
        ]

        render_memory_v2(self.output_dir, items)
        rules = (self.output_dir / "projects" / "codexclaw" / "rules.md").read_text(encoding="utf-8")

        self.assertNotIn("Completion Matrix", rules)
        self.assertIn("tracker payload blocks", rules)

    def test_recent_page_uses_latest_active_temporal_project_evidence_only(self) -> None:
        items = [
            {
                "item_id": "old-state",
                "project": "ai-trader",
                "memory_class": "current_state",
                "memory_role": "recent_state",
                "agent_facing_statement": "Older AITrader work focused on a previous risk model.",
                "confidence": "strong",
                "temporal_status": "active",
                "evidence_refs": [{"source_day": "2026-04-01", "message_index": 1}],
            },
            {
                "item_id": "ai-summary",
                "project": "ai-trader",
                "memory_class": "project_summary",
                "memory_role": "purpose",
                "agent_facing_statement": "AITrader is a deterministic autonomous trading system.",
                "confidence": "strong",
                "temporal_status": "durable",
                "evidence_refs": [{"source_day": "2026-04-05", "message_index": 1}],
            },
            {
                "item_id": "ai-rule",
                "project": "ai-trader",
                "memory_class": "project_rule",
                "memory_role": "rule",
                "agent_facing_statement": "Treat new AITrader versions as clean-slate unless compatibility is requested.",
                "confidence": "strong",
                "temporal_status": "durable",
                "evidence_refs": [{"source_day": "2026-04-05", "message_index": 2}],
            },
            {
                "item_id": "latest-state",
                "project": "ai-trader",
                "memory_class": "current_state",
                "memory_role": "recent_state",
                "agent_facing_statement": "Latest AITrader work focused on validating the approval UI.",
                "confidence": "strong",
                "temporal_status": "active",
                "evidence_refs": [{"source_day": "2026-04-05", "message_index": 3}],
            },
        ]

        render_memory_v2(self.output_dir, items)
        recent = (self.output_dir / "projects" / "ai-trader" / "recent.md").read_text(encoding="utf-8")

        self.assertIn("# Ai Trader - Recent Context - April 05 2026", recent)
        self.assertIn("Latest AITrader work focused on validating the approval UI.", recent)
        self.assertNotIn("AITrader is a deterministic autonomous trading system", recent)
        self.assertNotIn("Treat new AITrader versions as clean-slate", recent)
        self.assertNotIn("previous risk model", recent)

    def test_project_backlog_items_render_in_project_and_recent_pages(self) -> None:
        items = [
            {
                "item_id": "backlog-1",
                "project": "ai-trader",
                "memory_class": "backlog_item",
                "memory_role": "recent_state",
                "agent_facing_statement": "Later, add portfolio-level drawdown controls to AITrader.",
                "confidence": "medium",
                "temporal_status": "active",
                "evidence_refs": [{"source_day": "2026-04-05", "message_index": 1}],
            },
            {
                "item_id": "backlog-2",
                "project": "ai-trader",
                "memory_class": "backlog_item",
                "memory_role": "recent_state",
                "agent_facing_statement": "Resolved backlog item should not render.",
                "confidence": "medium",
                "temporal_status": "resolved",
                "evidence_refs": [{"source_day": "2026-04-05", "message_index": 2}],
            },
        ]

        render_memory_v2(self.output_dir, items)
        project_memory = (self.output_dir / "projects" / "ai-trader" / "project.md").read_text(encoding="utf-8")
        recent = (self.output_dir / "projects" / "ai-trader" / "recent.md").read_text(encoding="utf-8")

        self.assertIn("## BACKLOG", project_memory)
        self.assertIn("Later, add portfolio-level drawdown controls", project_memory)
        self.assertIn("## BACKLOG", recent)
        self.assertIn("Later, add portfolio-level drawdown controls", recent)
        self.assertNotIn("Resolved backlog item should not render", project_memory)

    def test_recent_page_does_not_fallback_to_durable_project_items(self) -> None:
        items = [
            {
                "item_id": "ai-summary",
                "project": "ai-trader",
                "memory_class": "project_summary",
                "memory_role": "purpose",
                "agent_facing_statement": "AITrader is a deterministic autonomous trading system.",
                "confidence": "strong",
                "temporal_status": "durable",
                "evidence_refs": [{"source_day": "2026-04-05", "message_index": 1}],
            }
        ]

        render_memory_v2(self.output_dir, items)
        recent = (self.output_dir / "projects" / "ai-trader" / "recent.md").read_text(encoding="utf-8")

        self.assertIn("# Ai Trader - Recent Context", recent)
        self.assertNotIn("April 05 2026", recent)
        self.assertNotIn("AITrader is a deterministic autonomous trading system", recent)

    def test_ai_trader_example_in_memory_page_discussion_routes_to_wikimemory(self) -> None:
        def attribution_llm(system_prompt: str, payload: dict[str, object], model: str) -> dict[str, object]:
            if "messages" in payload:
                return {
                    "candidates": [
                        {
                            "candidate_id": "example-attribution",
                            "source_day": "2026-03-13",
                            "project": "ai-trader",
                            "memory_class": "project_rule",
                            "memory_role": "rule",
                            "agent_facing_statement": "Move the Ai Trader clean-slate compatibility guidance out of project.md PURPOSE and into rules.md during memory page rendering.",
                            "confidence": "strong",
                            "temporal_status": "durable",
                            "evidence_refs": [3],
                        }
                    ]
                }
            return {
                "items": [
                    {
                        "item_id": "example-attribution",
                        "project": "ai-trader",
                        "memory_class": "project_rule",
                        "memory_role": "rule",
                        "agent_facing_statement": "Move the Ai Trader clean-slate compatibility guidance out of project.md PURPOSE and into rules.md during memory page rendering.",
                        "confidence": "strong",
                        "temporal_status": "durable",
                        "supporting_candidate_ids": ["example-attribution"],
                    }
                ]
            }

        result = run_memory_v2(
            input_dir=self.input_dir,
            output_dir=self.output_dir,
            state_dir=self.state_dir,
            days=["2026-03-13"],
            llm_client=attribution_llm,
            model="stub-model",
        )

        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        self.assertFalse((self.output_dir / "projects" / "ai-trader" / "recent.md").exists())
        self.assertNotIn("clean-slate", (self.output_dir / "projects" / "ai-trader" / "rules.md").read_text(encoding="utf-8"))
        self.assertTrue((self.output_dir / "projects" / "wikimemory" / "rules.md").exists())

    def test_ai_trader_mention_in_wikimemory_evidence_routes_merged_item_to_wikimemory(self) -> None:
        self.day_file.write_text(
            """# Codex Chat Export - 2026-04-19

## 2026-04-19T12:41:37.137Z - User

<!-- source: raw.jsonl:10 -->

```text
# Context from my IDE setup:

## Open tabs:
- project.md: WikiMemory/memory/projects/ai-trader/project.md

## My request for Codex:
The context of that line was, the agent was maintaining compatibility with v1 of the system while building v2. How would you rewrite this rule, which should not be in Purpose?
```
""",
            encoding="utf-8",
        )

        def attribution_llm(system_prompt: str, payload: dict[str, object], model: str) -> dict[str, object]:
            if "messages" in payload:
                return {
                    "candidates": [
                        {
                            "candidate_id": "ai-example",
                            "source_day": "2026-04-19",
                            "project": "ai-trader",
                            "memory_class": "project_rule",
                            "memory_role": "rule",
                            "agent_facing_statement": "For new AITrader versions that are not yet in production, default to clean-slate design.",
                            "confidence": "strong",
                            "temporal_status": "durable",
                            "evidence_refs": [1],
                        }
                    ]
                }
            return {
                "items": [
                    {
                        "item_id": "ai-example",
                        "project": "ai-trader",
                        "memory_class": "project_rule",
                        "memory_role": "rule",
                        "agent_facing_statement": "For new AITrader versions that are not yet in production, default to clean-slate design.",
                        "confidence": "strong",
                        "temporal_status": "durable",
                        "supporting_candidate_ids": ["ai-example"],
                    }
                ]
            }

        result = run_memory_v2(
            input_dir=self.input_dir,
            output_dir=self.output_dir,
            state_dir=self.state_dir,
            days=["2026-03-13"],
            llm_client=attribution_llm,
            model="stub-model",
        )

        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        merged = json.loads((self.output_dir / "_meta" / "merged_items.json").read_text(encoding="utf-8"))["items"][0]
        self.assertEqual(merged["project"], "wikimemory")
        self.assertFalse((self.output_dir / "projects" / "ai-trader" / "recent.md").exists())
        self.assertNotIn("clean-slate", (self.output_dir / "projects" / "ai-trader" / "rules.md").read_text(encoding="utf-8"))

    def test_known_project_with_readme_renders_project_page_even_without_log_items(self) -> None:
        def no_item_llm(system_prompt: str, payload: dict[str, object], model: str) -> dict[str, object]:
            if "messages" in payload:
                return {"candidates": []}
            return {"items": []}

        result = run_memory_v2(
            input_dir=self.input_dir,
            output_dir=self.output_dir,
            state_dir=self.state_dir,
            days=["2026-03-13"],
            project_root_dir=self.project_root_dir,
            llm_client=no_item_llm,
            model="stub-model",
        )

        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        self.assertTrue((self.output_dir / "projects" / "ai-trader" / "project.md").exists())
        self.assertTrue((self.output_dir / "projects" / "ai-trader" / "rules.md").exists())
        self.assertFalse((self.output_dir / "projects" / "ai-trader" / "recent.md").exists())

    def test_ai_trader_subject_statement_routes_to_ai_trader(self) -> None:
        self.assertEqual(
            correct_project_from_statement(
                "AITrader is a monorepo trading platform with services for ingest, worker orchestration, execution, and approval UI.",
                "unknown",
            ),
            "ai-trader",
        )
        self.assertEqual(
            correct_project_from_statement(
                "High risk of repeated delivery failure persists until filesystem write access is enabled in AITrader workspace.",
                "codexclaw",
            ),
            "ai-trader",
        )
        self.assertEqual(
            correct_project_from_statement(
                "CodexClaw git routing behavior was fixed so paths like AITrader/docs are recognized as explicit targeting.",
                "codexclaw",
            ),
            "codexclaw",
        )

    def test_rule_bucket_keeps_positive_boundary_rules_in_always_do(self) -> None:
        statement = "Enforce role boundaries: strategist orchestrates but does not code/execute trades; research provides analysis only."

        self.assertEqual(rule_bucket(statement), "always")
        self.assertEqual(rule_bucket("Do not execute trades from research role."), "never")

    def test_rule_split_handles_mixed_must_do_and_must_not_guidance(self) -> None:
        statement = "Strategist should follow interview-first clarification for ambiguous asks, but must not re-ask already-answered confirmations; once user routing/ownership is explicit for the turn, proceed."

        self.assertEqual(
            split_rule_statement(statement),
            [
                "Strategist should follow interview-first clarification for ambiguous asks",
                "must not re-ask already-answered confirmations",
                "once user routing/ownership is explicit for the turn, proceed.",
            ],
        )
        self.assertEqual(rule_bucket("Strategist should follow interview-first clarification for ambiguous asks"), "always")
        self.assertEqual(rule_bucket("must not re-ask already-answered confirmations"), "never")
        self.assertEqual(rule_bucket("once user routing/ownership is explicit for the turn, proceed."), "conditional")

        render_memory_v2(
            self.output_dir,
            [
                {
                    "item_id": "mixed-rule",
                    "project": "codexclaw",
                    "memory_class": "project_rule",
                    "memory_role": "rule",
                    "agent_facing_statement": statement,
                    "confidence": "strong",
                    "temporal_status": "durable",
                    "evidence_refs": [{"source_day": "2026-03-13", "message_index": 1}],
                }
            ],
        )
        rules = (self.output_dir / "projects" / "codexclaw" / "rules.md").read_text(encoding="utf-8")
        self.assertIn("- Strategist should follow interview-first clarification for ambiguous asks.", rules)
        self.assertIn("- Do not re-ask already-answered confirmations.", rules)
        self.assertIn("- Once user routing/ownership is explicit for the turn, proceed.", rules)

    def test_rule_split_keeps_positive_semicolon_enumerations_together(self) -> None:
        statement = "Enforce role boundaries: strategist orchestrates but does not code/execute trades; research provides analysis only; execution handles monitoring/risk adjustments."

        self.assertEqual(split_rule_statement(statement), [statement])
        self.assertEqual(rule_bucket(statement), "always")


if __name__ == "__main__":
    unittest.main()
