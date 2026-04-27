from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from sessionmemory.memory_review import run_memory_review


class MemoryReviewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="sessionmemory-review-"))
        self.memory_dir = self.temp_dir / "memory"
        self.state_dir = self.temp_dir / "state"
        self.audits_dir = self.temp_dir / "audits"
        meta_dir = self.memory_dir / "_meta"
        meta_dir.mkdir(parents=True)
        (meta_dir / "promotion_review.jsonl").write_text(
            json.dumps(
                {
                    "item_id": "rule-1",
                    "memory_class": "project_rules",
                    "statement": "Do not commit generated memory outputs.",
                    "review_required": True,
                },
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_memory_review_records_approve_and_reject_decisions(self) -> None:
        result = run_memory_review(
            memory_dir=self.memory_dir,
            state_dir=self.state_dir,
            audits_dir=self.audits_dir,
            approve=["rule-1"],
            reject=["rule-2"],
        )

        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        self.assertEqual(result.report.approved_count, 1)
        self.assertEqual(result.report.rejected_count, 1)
        payload = json.loads(result.decisions_path.read_text(encoding="utf-8"))
        self.assertEqual(payload["decisions"]["rule-1"]["decision"], "approved")
        rows = [
            json.loads(line)
            for line in result.review_items_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(rows[0]["review_decision"], "approved")


if __name__ == "__main__":
    unittest.main()
