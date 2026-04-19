from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from wikimemory.memory_v2 import parse_daily_chat_markdown, render_memory_v2, rule_bucket, run_memory_v2


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

    def test_rule_bucket_keeps_positive_boundary_rules_in_always_do(self) -> None:
        statement = "Enforce role boundaries: strategist orchestrates but does not code/execute trades; research provides analysis only."

        self.assertEqual(rule_bucket(statement), "always")
        self.assertEqual(rule_bucket("Do not execute trades from research role."), "never")


if __name__ == "__main__":
    unittest.main()
