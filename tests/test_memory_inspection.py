from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from sessionmemory.memory_inspection import run_memory_inspection


class MemoryInspectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="sessionmemory-memory-inspection-"))
        self.memory_dir = self.temp_dir / "memory"
        self.state_dir = self.temp_dir / "state"
        meta_dir = self.memory_dir / "_meta"
        meta_dir.mkdir(parents=True)
        (meta_dir / "items.jsonl").write_text(
            "".join(
                [
                    json.dumps(
                        {
                            "item_id": "rule-1",
                            "memory_role": "rule",
                            "memory_class": "project_rules",
                            "scope": "project",
                            "project": "alpha",
                            "statement": "Always show backlog items as options before starting work.",
                            "evidence_ids": ["e1"],
                            "provenance_refs": [{"source_id": "s1"}],
                            "authority": "consumer_override",
                            "locked_by_consumer": True,
                        }
                    )
                    + "\n"
                ]
            ),
            encoding="utf-8",
        )
        self.state_dir.mkdir(parents=True)
        (self.state_dir / "memory_rule_overrides.json").write_text(
            json.dumps({"commands": [{"action": "add_rule", "statement": "Always show backlog items as options before starting work."}]}, indent=2),
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_memory_inspection_explains_rule(self) -> None:
        result = run_memory_inspection(
            action="why-rule",
            memory_dir=self.memory_dir,
            state_dir=self.state_dir,
            rule_query="backlog items",
        )
        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        self.assertEqual(result.payload["authority"], "consumer_override")
        self.assertTrue(result.payload["locked_by_consumer"])


if __name__ == "__main__":
    unittest.main()
