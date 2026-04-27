from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from sessionmemory.onboarding import detect_environment, run_onboarding
from sessionmemory.product_config import default_product_config
from sessionmemory.onboarding import replace_bootstrap_renderer, replace_markdown_mode


class OnboardingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="sessionmemory-onboard-"))
        self.project_root = self.temp_dir / "project"
        (self.project_root / "wiki" / ".obsidian").mkdir(parents=True)
        (self.project_root / "config").mkdir(parents=True)
        (self.project_root / "AGENTS.md").write_text("# Bootstrap", encoding="utf-8")
        (self.project_root / "config" / "source_roots.json").write_text("{}", encoding="utf-8")

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_detect_environment_prefers_existing_obsidian_and_agents_file(self) -> None:
        detected = detect_environment(self.project_root)
        self.assertEqual(detected["likely_markdown_mode"], "obsidian_markdown")
        self.assertEqual(detected["likely_bootstrap_renderer"], "codex_agents_md")
        self.assertEqual(detected["likely_bootstrap_target_path"], "AGENTS.md")
        self.assertEqual(detected["likely_agent_platform"], "codex")
        self.assertIn("config/source_roots.json", detected["existing_config_files"])

    def test_run_onboarding_writes_recommended_product_config(self) -> None:
        target_config = self.project_root / "config" / "product_config.generated.json"
        brief_path = self.project_root / "config" / "agent_onboarding_brief.generated.md"
        report = run_onboarding(self.project_root, target_config, brief_path)
        self.assertTrue(target_config.exists())
        self.assertTrue(brief_path.exists())
        payload = json.loads(target_config.read_text(encoding="utf-8"))
        self.assertEqual(payload["markdown_output"]["mode"], "obsidian_markdown")
        self.assertEqual(payload["agent_platform"]["bootstrap_target_path"], "AGENTS.md")
        self.assertEqual(report.questions[0].question_id, "agent_platform")
        self.assertEqual(report.agent_entry_file, "START_HERE_FOR_AGENT.md")
        self.assertTrue(report.inferred_options)
        self.assertTrue(payload["project_aliases"])
        self.assertIn("project_routing", payload)

    def test_onboarding_replacements_preserve_project_aliases_and_routing(self) -> None:
        config = default_product_config(self.project_root)
        markdown_config = replace_markdown_mode(config, "plain_markdown")
        bootstrap_config = replace_bootstrap_renderer(markdown_config, "claude_md", "CLAUDE.md")
        self.assertEqual(bootstrap_config.project_aliases, config.project_aliases)
        self.assertEqual(bootstrap_config.project_routing, config.project_routing)
        self.assertEqual(bootstrap_config.markdown_output.mode, "plain_markdown")
        self.assertEqual(bootstrap_config.agent_platform.bootstrap_target_path, "CLAUDE.md")
