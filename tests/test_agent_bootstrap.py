from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from wikimemory.agent_bootstrap import run_agent_bootstrap
from wikimemory.product_config import default_product_config


class AgentBootstrapTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="wikimemory-agent-bootstrap-"))
        self.memory_dir = self.temp_dir / "memory"
        self.state_dir = self.temp_dir / "state"
        self.audits_dir = self.temp_dir / "audits"
        self.product_config = self.temp_dir / "product_config.json"
        self.write_product_config()

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def write_product_config(self) -> None:
        payload = default_product_config(self.temp_dir).to_dict()
        payload["environment"]["repo_root"] = str(self.temp_dir)
        payload["agent_platform"]["bootstrap_target_path"] = "AGENTS.md"
        self.product_config.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def write_memory_items(self) -> None:
        items = [
            {
                "item_id": "global-1",
                "memory_class": "global_user_rules",
                "scope": "global",
                "project": None,
                "promotion_state": "explicit",
                "confidence": "explicit",
                "statement": "Add this to global rules: Always inspect real data first.",
            },
            {
                "item_id": "rule-1",
                "memory_class": "project_rules",
                "scope": "project",
                "project": "alpha",
                "promotion_state": "durable",
                "confidence": "candidate",
                "statement": "Do not commit generated memory outputs.",
            },
            {
                "item_id": "recent-1",
                "memory_class": "recent_project_state",
                "scope": "project",
                "project": "alpha",
                "promotion_state": "candidate",
                "confidence": "candidate",
                "statement": "M README.md",
            },
        ]
        meta_dir = self.memory_dir / "_meta"
        meta_dir.mkdir(parents=True)
        (meta_dir / "items.jsonl").write_text(
            "".join(json.dumps(item, sort_keys=True) + "\n" for item in items),
            encoding="utf-8",
        )

    def test_agent_bootstrap_renders_codex_agents_md_from_memory_manifest(self) -> None:
        self.write_memory_items()
        (self.temp_dir / "AGENTS.md").write_text("# User Rules\n\nDo not delete this.\n", encoding="utf-8")

        result = run_agent_bootstrap(
            product_config_path=self.product_config,
            state_dir=self.state_dir,
            memory_dir=self.memory_dir,
            audits_dir=self.audits_dir,
        )

        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        target = self.temp_dir / "AGENTS.md"
        self.assertTrue(target.exists())
        content = target.read_text(encoding="utf-8")
        self.assertIn("Do not delete this.", content)
        self.assertIn("<!-- WIKIMEMORY:START -->", content)
        self.assertIn("<!-- WIKIMEMORY:END -->", content)
        self.assertIn("first line of the first real reply", content)
        self.assertIn("Your workspace memory is already loaded here.", content)
        self.assertIn("latest durable workspace memory is using both relative time and absolute time", content)
        self.assertIn("copy/paste ready", content)
        self.assertIn("no brackets, no placeholders", content)
        self.assertIn("only what changed after the stated timestamp", content)
        self.assertIn("without mentioning durable memory", content)
        self.assertIn("memory/global/user-rules.md", content)
        self.assertIn("memory/global/consumer-profile.md", content)
        self.assertIn("memory/_meta/consumer_style.json", content)
        self.assertIn("memory/global/memory-health.md", content)
        self.assertIn("memory/global/memory-change-log.md", content)
        self.assertIn("directive = follow", content)
        self.assertIn("consumer-profile.md contains inferred preferences", content)
        self.assertIn("If the user asks to do something that conflicts with saved rules", content)
        self.assertIn("Memory command: add global rule", content)
        self.assertIn("# 🧠 Agent Memory Index", content)
        self.assertIn("Read on startup", content)
        self.assertIn("Do not load any project-specific pages until the user picks a project", content)
        self.assertIn("Available projects:", content)
        self.assertIn("alpha", content)
        self.assertIn("Project routing rule:", content)
        self.assertIn("map it to the closest matching available project", content)
        self.assertIn("After project selection, load in order", content)
        self.assertIn("memory/projects/<selected-project>/recent.md", content)
        self.assertIn("memory/projects/<selected-project>/continuations.md", content)
        self.assertIn("memory/projects/<selected-project>/lessons.md", content)
        self.assertIn("memory/projects/<selected-project>/project.md", content)
        self.assertIn("memory/daily-conversations/YYYY-MM-DD.md", content)
        self.assertIn("Never load these by default", content)
        self.assertIn("Never read daily conversation pages unless the user explicitly asks for them", content)
        self.assertIn("continue an existing project or start a new one", content)
        self.assertIn("never assume the next task or start work until the user chooses a direction", content)
        self.assertNotIn("M README.md", content)
        self.assertNotIn("Do not commit generated memory outputs", content)

    def test_agent_bootstrap_updates_only_managed_block(self) -> None:
        self.write_memory_items()
        target = self.temp_dir / "AGENTS.md"
        target.write_text(
            "# User Rules\n\nKeep this paragraph.\n\n<!-- WIKIMEMORY:START -->\nold generated text\n<!-- WIKIMEMORY:END -->\n\nKeep this footer.\n",
            encoding="utf-8",
        )

        result = run_agent_bootstrap(
            product_config_path=self.product_config,
            state_dir=self.state_dir,
            memory_dir=self.memory_dir,
            audits_dir=self.audits_dir,
        )

        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        content = target.read_text(encoding="utf-8")
        self.assertIn("Keep this paragraph.", content)
        self.assertIn("Keep this footer.", content)
        self.assertNotIn("old generated text", content)
        self.assertIn("Agent Memory Index", content)

    def test_agent_bootstrap_project_filter_keeps_global_and_selected_project(self) -> None:
        self.write_memory_items()

        result = run_agent_bootstrap(
            product_config_path=self.product_config,
            state_dir=self.state_dir,
            memory_dir=self.memory_dir,
            audits_dir=self.audits_dir,
            output_path=self.temp_dir / "filtered.md",
            projects=["other"],
        )

        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        content = (self.temp_dir / "filtered.md").read_text(encoding="utf-8")
        self.assertIn("memory/global/user-rules.md", content)
        self.assertIn("memory/global/consumer-profile.md", content)
        self.assertNotIn("Do not commit generated memory outputs", content)

    def test_agent_bootstrap_supports_claude_and_generic_renderers(self) -> None:
        self.write_memory_items()
        for renderer, target_name in (
            ("claude_md", "CLAUDE.md"),
            ("generic_bootstrap_md", "MEMORY.md"),
        ):
            payload = default_product_config(self.temp_dir).to_dict()
            payload["environment"]["repo_root"] = str(self.temp_dir)
            payload["agent_platform"]["bootstrap_renderer"] = renderer
            payload["agent_platform"]["bootstrap_target_path"] = target_name
            self.product_config.write_text(json.dumps(payload, indent=2), encoding="utf-8")

            result = run_agent_bootstrap(
                product_config_path=self.product_config,
                state_dir=self.state_dir,
                memory_dir=self.memory_dir,
                audits_dir=self.audits_dir,
            )

            self.assertTrue(result.report.success, result.report.fatal_error_summary)
            content = (self.temp_dir / target_name).read_text(encoding="utf-8")
            self.assertIn("# 🧠 Agent Memory Index", content)
            self.assertIn("memory/global/user-rules.md", content)
            self.assertIn("memory/global/consumer-profile.md", content)
            self.assertIn("Keep this bootstrap tiny", content)


if __name__ == "__main__":
    unittest.main()
