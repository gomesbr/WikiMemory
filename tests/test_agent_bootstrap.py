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
        self.assertIn("memory/global/user-rules.md", content)
        self.assertIn("Always inspect real data first", content)
        self.assertIn("Do not commit generated memory outputs", content)
        self.assertIn("memory/projects/alpha/recent.md", content)
        self.assertNotIn("M README.md", content)

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
        self.assertIn("Always inspect real data first", content)
        self.assertNotIn("Do not commit generated memory outputs", content)

    def test_agent_bootstrap_supports_claude_and_generic_renderers(self) -> None:
        self.write_memory_items()
        for renderer, target_name, expected_title in (
            ("claude_md", "CLAUDE.md", "# Claude Memory Bootstrap"),
            ("generic_bootstrap_md", "MEMORY.md", "# AI Agent Memory Bootstrap"),
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
            self.assertIn(expected_title, content)
            self.assertIn("memory/global/user-rules.md", content)
            self.assertIn("Keep this bootstrap tiny", content)


if __name__ == "__main__":
    unittest.main()
