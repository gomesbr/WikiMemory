from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from wikimemory.memory_lint import run_memory_lint
from wikimemory.product_config import default_product_config


class MemoryLintTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="wikimemory-memory-lint-"))
        self.memory_dir = self.temp_dir / "memory"
        self.state_dir = self.temp_dir / "state"
        self.audits_dir = self.temp_dir / "audits"
        self.product_config = self.temp_dir / "product_config.json"
        payload = default_product_config(self.temp_dir).to_dict()
        payload["environment"]["repo_root"] = str(self.temp_dir)
        self.product_config.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def write_items(self, items: list[dict[str, object]]) -> None:
        meta_dir = self.memory_dir / "_meta"
        meta_dir.mkdir(parents=True)
        (meta_dir / "items.jsonl").write_text(
            "".join(json.dumps(item, sort_keys=True) + "\n" for item in items),
            encoding="utf-8",
        )

    def read_findings(self) -> list[dict[str, object]]:
        return [
            json.loads(line)
            for line in (self.audits_dir / "memory_lint_findings.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    def base_item(self, **overrides: object) -> dict[str, object]:
        item = {
            "item_id": "item-1",
            "memory_class": "project_rules",
            "scope": "project",
            "project": "alpha",
            "statement": "Do not commit generated memory outputs.",
            "evidence_ids": ["e1"],
            "provenance_refs": [{"source_id": "s1"}],
            "last_seen_at": "2026-04-18T00:00:00Z",
        }
        item.update(overrides)
        return item

    def test_memory_lint_flags_rule_noise_and_missing_provenance(self) -> None:
        self.write_items(
            [
                self.base_item(
                    item_id="bad-rule",
                    statement="PLEASE IMPLEMENT THIS PLAN: restart localhost and hard refresh",
                    evidence_ids=[],
                )
            ]
        )
        (self.temp_dir / "AGENTS.md").write_text(
            "# Agent Bootstrap\n\n- `memory/global/user-rules.md`\n- Keep this bootstrap tiny.\n",
            encoding="utf-8",
        )

        result = run_memory_lint(
            product_config_path=self.product_config,
            state_dir=self.state_dir,
            memory_dir=self.memory_dir,
            audits_dir=self.audits_dir,
        )

        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        findings = self.read_findings()
        self.assertTrue(any(finding["check_type"] == "schema_noise_rule" for finding in findings))
        self.assertTrue(any(finding["check_type"] == "missing_provenance" for finding in findings))
        self.assertGreater(result.report.error_count, 0)

    def test_memory_lint_flags_stale_recent_and_inlined_bootstrap_recent(self) -> None:
        self.write_items(
            [
                self.base_item(
                    item_id="recent-1",
                    memory_class="recent_project_state",
                    statement="Old active task",
                    last_seen_at="2020-01-01T00:00:00Z",
                )
            ]
        )
        (self.temp_dir / "AGENTS.md").write_text(
            "# Agent Bootstrap\n\n- `memory/global/user-rules.md`\n- Keep this bootstrap tiny.\n- Old active task\n",
            encoding="utf-8",
        )

        result = run_memory_lint(
            product_config_path=self.product_config,
            state_dir=self.state_dir,
            memory_dir=self.memory_dir,
            audits_dir=self.audits_dir,
        )

        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        findings = self.read_findings()
        self.assertTrue(any(finding["check_type"] == "stale_recent_state" for finding in findings))
        self.assertTrue(any(finding["check_type"] == "recent_state_inlined" for finding in findings))

    def test_memory_lint_safe_fix_repairs_bootstrap_structure(self) -> None:
        self.write_items(
            [
                {
                    "item_id": "global-1",
                    "memory_class": "global_user_rules",
                    "scope": "global",
                    "project": None,
                    "statement": "Always inspect real data first.",
                    "evidence_ids": ["e1"],
                    "provenance_refs": [{"source_id": "s1"}],
                }
            ]
        )
        bootstrap_path = self.temp_dir / "AGENTS.md"
        bootstrap_path.write_text("# Agent Bootstrap\n", encoding="utf-8")

        result = run_memory_lint(
            product_config_path=self.product_config,
            state_dir=self.state_dir,
            memory_dir=self.memory_dir,
            audits_dir=self.audits_dir,
            bootstrap_path=bootstrap_path,
            autofix=True,
        )

        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        content = bootstrap_path.read_text(encoding="utf-8")
        self.assertIn("memory/global/user-rules.md", content)
        self.assertIn("Keep this bootstrap tiny", content)

    def test_memory_lint_flags_empty_statement(self) -> None:
        self.write_items([self.base_item(item_id="empty-1", statement="")])
        (self.temp_dir / "AGENTS.md").write_text(
            "# Agent Bootstrap\n\n- `memory/global/user-rules.md`\n- Keep this bootstrap tiny.\n",
            encoding="utf-8",
        )

        result = run_memory_lint(
            product_config_path=self.product_config,
            state_dir=self.state_dir,
            memory_dir=self.memory_dir,
            audits_dir=self.audits_dir,
        )

        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        self.assertTrue(any(finding["check_type"] == "empty_statement" for finding in self.read_findings()))

    def test_memory_lint_flags_purpose_rule_and_vague_statement(self) -> None:
        self.write_items(
            [
                self.base_item(
                    item_id="purpose-rule",
                    memory_class="stable_project_summary",
                    memory_role="purpose",
                    item_type="purpose",
                    statement="Every time you make a change, think about the system as new.",
                )
            ]
        )
        (self.temp_dir / "AGENTS.md").write_text(
            "# Agent Bootstrap\n\n- `memory/global/user-rules.md`\n- Keep this bootstrap tiny.\n",
            encoding="utf-8",
        )

        result = run_memory_lint(
            product_config_path=self.product_config,
            state_dir=self.state_dir,
            memory_dir=self.memory_dir,
            audits_dir=self.audits_dir,
        )

        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        findings = self.read_findings()
        self.assertTrue(any(finding["check_type"] == "purpose_contains_rule" for finding in findings))
        self.assertTrue(any(finding["check_type"] == "vague_memory_statement" for finding in findings))

    def test_memory_lint_flags_v2_scope_and_token_quality(self) -> None:
        self.write_items(
            [
                self.base_item(
                    item_id="unknown-v2",
                    memory_class="project_rule",
                    project="unknown",
                    statement="Build lineage from real lifecycle records only; do not fabricate synthetic order/fill nodes.",
                    evidence_refs=[{"source_day": "2026-03-13", "message_index": 1}],
                    provenance_refs=[{"source_day": "2026-03-13", "message_index": 1}],
                ),
                self.base_item(
                    item_id="global-leak",
                    memory_class="global_rule",
                    scope="global",
                    project="global",
                    statement="Enforce trade lifecycle integrity via explicit DB key lineage (intent -> order -> fill -> position).",
                    evidence_refs=[{"source_day": "2026-03-13", "message_index": 2}],
                    provenance_refs=[{"source_day": "2026-03-13", "message_index": 2}],
                ),
                self.base_item(
                    item_id="token-typo",
                    memory_class="backlog_item",
                    project="codexclaw",
                    statement="Document TRACKER_TASKS/TACKER_UPDATES directive usage.",
                    evidence_refs=[{"source_day": "2026-03-13", "message_index": 3}],
                    provenance_refs=[{"source_day": "2026-03-13", "message_index": 3}],
                ),
            ]
        )
        (self.memory_dir / "_meta" / "page_quality_review.json").write_text(
            json.dumps({"lines": [{"page": "global/user-rules.md", "line_number": 10, "status": "bad", "reason": "global_scope_leak"}]}),
            encoding="utf-8",
        )
        (self.temp_dir / "AGENTS.md").write_text(
            "# Agent Bootstrap\n\n- `memory/global/user-rules.md`\n- Keep this bootstrap tiny.\n",
            encoding="utf-8",
        )

        result = run_memory_lint(
            product_config_path=self.product_config,
            state_dir=self.state_dir,
            memory_dir=self.memory_dir,
            audits_dir=self.audits_dir,
        )

        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        findings = self.read_findings()
        self.assertTrue(any(finding["check_type"] == "unknown_project_item" for finding in findings))
        self.assertTrue(any(finding["check_type"] == "global_scope_leak" for finding in findings))
        self.assertTrue(any(finding["check_type"] == "known_token_typo" for finding in findings))
        self.assertTrue(any(finding["check_type"] == "bad_fresh_agent_line" for finding in findings))


if __name__ == "__main__":
    unittest.main()
