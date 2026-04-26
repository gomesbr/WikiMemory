from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from wikimemory.consumer_profile import ConsumerProfileResult, ConsumerProfileRunReport
from wikimemory.memory_lint import MemoryLintResult, MemoryLintRunReport
from wikimemory.memory_refresh import run_memory_refresh
from wikimemory.product_config import default_product_config


class MemoryRefreshTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="wikimemory-memory-refresh-"))
        self.sessions_root = self.temp_dir / "sessions"
        self.project_root = self.temp_dir / "project"
        self.state_dir = self.temp_dir / "state"
        self.normalized_dir = self.temp_dir / "normalized"
        self.evidence_dir = self.temp_dir / "evidence"
        self.memory_dir = self.temp_dir / "memory"
        self.audits_dir = self.temp_dir / "audits"
        self.source_config = self.temp_dir / "source_roots.json"
        self.product_config = self.temp_dir / "product_config.json"
        self.bootstrap_path = self.temp_dir / "AGENTS.md"
        repo_root = Path(__file__).resolve().parents[1]
        self.schema_path = repo_root / "schema" / "normalization_catalog.json"
        self.example_log = repo_root / "examples" / "source-logs" / "representative-session.jsonl"

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def init_real_sample_environment(self) -> None:
        target_log = (
            self.sessions_root
            / "2026"
            / "02"
            / "26"
            / "rollout-2026-02-26T21-48-04-019c9cff-0337-77e0-9ba6-a4f6dc75a92e.jsonl"
        )
        target_log.parent.mkdir(parents=True)
        shutil.copyfile(self.example_log, target_log)
        self.project_root.mkdir(parents=True)
        subprocess.run(["git", "-C", str(self.project_root), "init"], check=True, capture_output=True, text=True)
        (self.project_root / "README.md").write_text("# Example\n", encoding="utf-8")
        self.source_config.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "roots": [
                        {
                            "root_alias": "example_sessions",
                            "absolute_path": str(self.sessions_root),
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
        payload = default_product_config(self.temp_dir).to_dict()
        payload["environment"]["repo_root"] = str(self.temp_dir)
        payload["log_sources"][0]["root_alias"] = "example_sessions"
        payload["log_sources"][0]["absolute_path"] = str(self.sessions_root)
        payload["project_sources"][0]["project_root"] = str(self.project_root)
        self.product_config.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def fake_consumer_profile_result(self) -> ConsumerProfileResult:
        return ConsumerProfileResult(
            report=ConsumerProfileRunReport(
                run_id="consumer-profile-test",
                started_at="2026-04-25T00:00:00Z",
                finished_at="2026-04-25T00:00:01Z",
                model="stub-model",
                source_snippet_count=2,
                candidate_count=2,
                section_count=2,
                success=True,
                fatal_error_summary=None,
            ),
            profile_path=self.memory_dir / "global" / "consumer-profile.md",
            profile_json_path=self.memory_dir / "_meta" / "consumer_profile.json",
            candidates_path=self.audits_dir / "consumer_profile_candidates.jsonl",
            run_log_path=self.state_dir / "consumer_profile_runs.jsonl",
        )

    def test_memory_refresh_runs_real_sample_path_end_to_end(self) -> None:
        self.init_real_sample_environment()

        with patch("wikimemory.memory_refresh.run_consumer_profile", return_value=self.fake_consumer_profile_result()):
            result = run_memory_refresh(
                source_roots_config_path=self.source_config,
                product_config_path=self.product_config,
                normalization_schema_path=self.schema_path,
                state_dir=self.state_dir,
                normalized_dir=self.normalized_dir,
                evidence_dir=self.evidence_dir,
                memory_dir=self.memory_dir,
                audits_dir=self.audits_dir,
                bootstrap_output_path=self.bootstrap_path,
            )

        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        self.assertEqual(result.report.last_completed_phase, "memory-lint")
        self.assertTrue((self.memory_dir / "_meta" / "items.jsonl").exists())
        self.assertTrue(self.bootstrap_path.exists())
        self.assertTrue((self.audits_dir / "memory_lint_findings.jsonl").exists())
        self.assertEqual([status.phase for status in result.report.phase_statuses], list(("discover", "normalize", "ingest", "memory", "consumer-profile", "agent-bootstrap", "memory-lint")))
        state_payload = json.loads(result.state_path.read_text(encoding="utf-8"))
        self.assertEqual(state_payload["last_successful_refresh_finished_at"], result.report.finished_at)
        self.assertEqual(state_payload["last_attempted_refresh_finished_at"], result.report.finished_at)

    def test_memory_refresh_stops_on_memory_lint_errors(self) -> None:
        self.init_real_sample_environment()

        fake_lint = MemoryLintResult(
            report=MemoryLintRunReport(
                run_id="lint-failed",
                started_at="2026-04-18T00:00:00Z",
                finished_at="2026-04-18T00:00:01Z",
                finding_count=1,
                warning_count=0,
                error_count=1,
                success=True,
                fatal_error_summary=None,
            ),
            findings_path=self.audits_dir / "memory_lint_findings.jsonl",
            state_path=self.state_dir / "memory_lint_state.json",
            run_log_path=self.state_dir / "memory_lint_runs.jsonl",
        )

        with patch("wikimemory.memory_refresh.run_consumer_profile", return_value=self.fake_consumer_profile_result()), patch("wikimemory.memory_refresh.run_memory_lint", return_value=fake_lint):
            result = run_memory_refresh(
                source_roots_config_path=self.source_config,
                product_config_path=self.product_config,
                normalization_schema_path=self.schema_path,
                state_dir=self.state_dir,
                normalized_dir=self.normalized_dir,
                evidence_dir=self.evidence_dir,
                memory_dir=self.memory_dir,
                audits_dir=self.audits_dir,
                bootstrap_output_path=self.bootstrap_path,
            )

        self.assertFalse(result.report.success)
        self.assertEqual(result.report.failed_phase, "memory-lint")
        self.assertEqual(result.report.error_count, 1)
        state_payload = json.loads(result.state_path.read_text(encoding="utf-8"))
        self.assertIsNone(state_payload["last_successful_refresh_finished_at"])
        self.assertEqual(state_payload["last_attempted_refresh_finished_at"], result.report.finished_at)

    def test_memory_refresh_defaults_to_lint_autofix(self) -> None:
        self.init_real_sample_environment()

        fake_lint = MemoryLintResult(
            report=MemoryLintRunReport(
                run_id="lint-clean",
                started_at="2026-04-18T00:00:00Z",
                finished_at="2026-04-18T00:00:01Z",
                finding_count=0,
                warning_count=0,
                error_count=0,
                success=True,
                fatal_error_summary=None,
            ),
            findings_path=self.audits_dir / "memory_lint_findings.jsonl",
            state_path=self.state_dir / "memory_lint_state.json",
            run_log_path=self.state_dir / "memory_lint_runs.jsonl",
        )

        with patch("wikimemory.memory_refresh.run_consumer_profile", return_value=self.fake_consumer_profile_result()), patch(
            "wikimemory.memory_refresh.run_memory_lint",
            return_value=fake_lint,
        ) as lint_mock:
            result = run_memory_refresh(
                source_roots_config_path=self.source_config,
                product_config_path=self.product_config,
                normalization_schema_path=self.schema_path,
                state_dir=self.state_dir,
                normalized_dir=self.normalized_dir,
                evidence_dir=self.evidence_dir,
                memory_dir=self.memory_dir,
                audits_dir=self.audits_dir,
                bootstrap_output_path=self.bootstrap_path,
            )

        self.assertTrue(result.report.success)
        self.assertTrue(lint_mock.call_args.kwargs["autofix"])

    def test_memory_refresh_can_disable_lint_autofix(self) -> None:
        self.init_real_sample_environment()

        fake_lint = MemoryLintResult(
            report=MemoryLintRunReport(
                run_id="lint-clean",
                started_at="2026-04-18T00:00:00Z",
                finished_at="2026-04-18T00:00:01Z",
                finding_count=0,
                warning_count=0,
                error_count=0,
                success=True,
                fatal_error_summary=None,
            ),
            findings_path=self.audits_dir / "memory_lint_findings.jsonl",
            state_path=self.state_dir / "memory_lint_state.json",
            run_log_path=self.state_dir / "memory_lint_runs.jsonl",
        )

        with patch("wikimemory.memory_refresh.run_consumer_profile", return_value=self.fake_consumer_profile_result()), patch(
            "wikimemory.memory_refresh.run_memory_lint",
            return_value=fake_lint,
        ) as lint_mock:
            result = run_memory_refresh(
                source_roots_config_path=self.source_config,
                product_config_path=self.product_config,
                normalization_schema_path=self.schema_path,
                state_dir=self.state_dir,
                normalized_dir=self.normalized_dir,
                evidence_dir=self.evidence_dir,
                memory_dir=self.memory_dir,
                audits_dir=self.audits_dir,
                bootstrap_output_path=self.bootstrap_path,
                lint_fix=False,
            )

        self.assertTrue(result.report.success)
        self.assertFalse(lint_mock.call_args.kwargs["autofix"])

    def test_memory_refresh_preserves_last_successful_timestamp_after_failure(self) -> None:
        self.init_real_sample_environment()
        self.state_dir.mkdir(parents=True, exist_ok=True)
        (self.state_dir / "memory_refresh_state.json").write_text(
            json.dumps(
                {
                    "last_successful_refresh_finished_at": "2026-04-24T12:00:00Z",
                },
                indent=2,
            ),
            encoding="utf-8",
        )

        fake_lint = MemoryLintResult(
            report=MemoryLintRunReport(
                run_id="lint-failed",
                started_at="2026-04-18T00:00:00Z",
                finished_at="2026-04-18T00:00:01Z",
                finding_count=1,
                warning_count=0,
                error_count=1,
                success=True,
                fatal_error_summary=None,
            ),
            findings_path=self.audits_dir / "memory_lint_findings.jsonl",
            state_path=self.state_dir / "memory_lint_state.json",
            run_log_path=self.state_dir / "memory_lint_runs.jsonl",
        )

        with patch("wikimemory.memory_refresh.run_consumer_profile", return_value=self.fake_consumer_profile_result()), patch("wikimemory.memory_refresh.run_memory_lint", return_value=fake_lint):
            result = run_memory_refresh(
                source_roots_config_path=self.source_config,
                product_config_path=self.product_config,
                normalization_schema_path=self.schema_path,
                state_dir=self.state_dir,
                normalized_dir=self.normalized_dir,
                evidence_dir=self.evidence_dir,
                memory_dir=self.memory_dir,
                audits_dir=self.audits_dir,
                bootstrap_output_path=self.bootstrap_path,
            )

        self.assertFalse(result.report.success)
        state_payload = json.loads(result.state_path.read_text(encoding="utf-8"))
        self.assertEqual(state_payload["last_successful_refresh_finished_at"], "2026-04-24T12:00:00Z")


if __name__ == "__main__":
    unittest.main()
