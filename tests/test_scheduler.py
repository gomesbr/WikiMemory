from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from wikimemory.product_config import default_product_config
from wikimemory.scheduler import run_scheduler_plan


class SchedulerPlanTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="wikimemory-scheduler-"))
        self.state_dir = self.temp_dir / "state"
        self.scripts_dir = self.temp_dir / "scripts"
        self.product_config = self.temp_dir / "product_config.json"
        payload = default_product_config(self.temp_dir).to_dict()
        payload["scheduler"]["allowed_weekdays"] = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        payload["scheduler"]["run_hour_local"] = 0
        payload["scheduler"]["run_minute_local"] = 0
        payload["scheduler"]["lint_autofix_enabled"] = True
        payload["scheduler"]["lint_autofix_max_rounds"] = 2
        payload["scheduler"]["consumer_profile_extraction_model"] = "gpt-4o-mini"
        payload["scheduler"]["consumer_profile_merge_model"] = "gpt-5.3-codex"
        payload["scheduler"]["consumer_profile_window_max_chars"] = 60000
        self.product_config.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        self.state_dir.mkdir(parents=True)

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_scheduler_plan_marks_ingest_due_after_new_log_update(self) -> None:
        (self.state_dir / "source_registry.json").write_text(
            json.dumps(
                {
                    "sources": [
                        {
                            "source_id": "source-1",
                            "status": "stable",
                            "mtime_utc": "2026-04-25T12:00:00Z",
                        }
                    ]
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        (self.state_dir / "memory_refresh_runs.jsonl").write_text(
            json.dumps(
                {
                    "success": True,
                    "finished_at": "2026-04-24T12:00:00Z",
                }
            )
            + "\n",
            encoding="utf-8",
        )
        (self.state_dir / "memory_lint_runs.jsonl").write_text(
            json.dumps(
                {
                    "success": True,
                    "finished_at": "2026-04-24T12:00:00Z",
                }
            )
            + "\n",
            encoding="utf-8",
        )

        result = run_scheduler_plan(
            product_config_path=self.product_config,
            state_dir=self.state_dir,
            scripts_dir=self.scripts_dir,
        )

        self.assertTrue(result.report.ingest_due)
        self.assertTrue(result.report.lint_due)
        self.assertTrue(result.activation_script_path.exists())
        self.assertIn("--consumer-profile-extraction-model gpt-4o-mini", result.report.refresh_command)
        self.assertIn("--consumer-profile-merge-model gpt-5.3-codex", result.report.refresh_command)
        self.assertIn("--consumer-profile-window-max-chars 60000", result.report.refresh_command)
        self.assertIn("--lint-fix --lint-fix-rounds 2", result.activation_script_path.read_text(encoding="utf-8"))

    def test_scheduler_plan_prefers_explicit_last_successful_refresh_state(self) -> None:
        (self.state_dir / "source_registry.json").write_text(
            json.dumps(
                {
                    "sources": [
                        {
                            "source_id": "source-1",
                            "status": "stable",
                            "mtime_utc": "2026-04-25T12:00:00Z",
                        }
                    ]
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        (self.state_dir / "memory_refresh_state.json").write_text(
            json.dumps(
                {
                    "last_successful_refresh_finished_at": "2026-04-25T11:30:00Z",
                },
                indent=2,
            ),
            encoding="utf-8",
        )

        result = run_scheduler_plan(
            product_config_path=self.product_config,
            state_dir=self.state_dir,
            scripts_dir=self.scripts_dir,
        )

        self.assertEqual(result.report.last_refresh_at, "2026-04-25T11:30:00Z")


if __name__ == "__main__":
    unittest.main()
