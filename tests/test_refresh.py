from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch
from uuid import uuid4

from sessionmemory.classification import ClassificationResult, ClassificationRunReport
from sessionmemory.refresh import run_refresh


def make_source_file(
    path: Path,
    session_id: str,
    extra_lines: list[dict] | None = None,
    cwd: str = "C:\\repo",
    session_timestamp: str = "2026-04-12T20:59:14.432Z",
) -> None:
    extra_lines = extra_lines or []
    lines = [
        {
            "timestamp": session_timestamp,
            "type": "session_meta",
            "payload": {
                "id": session_id,
                "timestamp": session_timestamp,
                "cwd": cwd,
                "originator": "codex_vscode",
                "cli_version": "0.119.0-alpha.28",
                "source": "vscode",
                "model_provider": "openai",
            },
        },
        *extra_lines,
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for line in lines:
            handle.write(json.dumps(line, separators=(",", ":")) + "\n")


class RefreshTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="sessionmemory-refresh-"))
        self.root = self.temp_dir / "sessions"
        self.state_dir = self.temp_dir / "state"
        self.normalized_dir = self.temp_dir / "normalized"
        self.segmented_dir = self.temp_dir / "segmented"
        self.classified_dir = self.temp_dir / "classified"
        self.extracted_dir = self.temp_dir / "extracted"
        self.wiki_dir = self.temp_dir / "wiki"
        self.bootstrap_dir = self.temp_dir / "bootstrap"
        self.audits_dir = self.temp_dir / "audits"
        self.source_config_path = self.temp_dir / "source_roots.json"
        self.taxonomy_path = self.temp_dir / "classification_taxonomy.json"
        self.rules_path = self.temp_dir / "extraction_rules.json"
        self.wiki_config_path = self.temp_dir / "wiki_config.json"
        self.bootstrap_config_path = self.temp_dir / "bootstrap_config.json"
        self.audit_config_path = self.temp_dir / "audit_config.json"
        self.refresh_config_path = self.temp_dir / "refresh_config.json"
        repo_root = Path(__file__).resolve().parents[1]
        self.schema_path = repo_root / "schema" / "normalization_catalog.json"
        self.base_taxonomy_path = repo_root / "config" / "classification_taxonomy.json"
        self.base_rules_path = repo_root / "config" / "extraction_rules.json"
        self.base_wiki_config_path = repo_root / "config" / "wiki_config.json"
        self.base_bootstrap_config_path = repo_root / "config" / "bootstrap_config.json"
        self.base_audit_config_path = repo_root / "config" / "audit_config.json"

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def write_configs(self) -> None:
        self.source_config_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "roots": [
                        {
                            "root_alias": "codex_sessions",
                            "absolute_path": str(self.root),
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
        shutil.copyfile(self.base_taxonomy_path, self.taxonomy_path)
        shutil.copyfile(self.base_rules_path, self.rules_path)
        shutil.copyfile(self.base_wiki_config_path, self.wiki_config_path)
        shutil.copyfile(self.base_bootstrap_config_path, self.bootstrap_config_path)

        audit_payload = json.loads(self.base_audit_config_path.read_text(encoding="utf-8"))
        audit_payload["bootstrap_config_path"] = str(self.bootstrap_config_path)
        self.audit_config_path.write_text(json.dumps(audit_payload, indent=2), encoding="utf-8")

        refresh_payload = {
            "schema_version": 1,
            "refresh_schema_version": 1,
            "rules_version": 1,
            "paths": {
                "source_roots_config": str(self.source_config_path),
                "normalization_schema": str(self.schema_path),
                "classification_taxonomy": str(self.taxonomy_path),
                "extraction_rules": str(self.rules_path),
                "wiki_config": str(self.wiki_config_path),
                "bootstrap_config": str(self.bootstrap_config_path),
                "audit_config": str(self.audit_config_path),
            },
            "lock": {
                "lock_path": "refresh.lock.json",
                "stale_after_minutes": 180,
            },
        }
        self.refresh_config_path.write_text(json.dumps(refresh_payload, indent=2), encoding="utf-8")

    def source_path(self, session_id: str, *subdirs: str) -> Path:
        base = self.root / "2026" / "04" / "12"
        for part in subdirs:
            base /= part
        return base / f"rollout-2026-04-12T20-59-14-{session_id}.jsonl"

    def run_refresh_with_fake_llm(self, source_ids: list[str] | None = None):
        with patch("sessionmemory.wiki.call_openai_structured_json", side_effect=self.make_fake_wiki_synthesizer()), patch(
            "sessionmemory.bootstrap.call_openai_structured_json",
            side_effect=self.make_fake_bootstrap_synthesizer(),
        ):
            return run_refresh(
                config_path=self.refresh_config_path,
                state_dir=self.state_dir,
                audits_dir=self.audits_dir,
                source_ids=source_ids,
                normalized_dir=self.normalized_dir,
                segmented_dir=self.segmented_dir,
                classified_dir=self.classified_dir,
                extracted_dir=self.extracted_dir,
                wiki_dir=self.wiki_dir,
                bootstrap_dir=self.bootstrap_dir,
            )

    def make_fake_wiki_synthesizer(self):
        def fake_structured_json(*, config, system_prompt, user_prompt, schema):
            packet = json.loads(user_prompt)
            item_ids = [str(item) for item in packet.get("input_item_keys", [])]
            if not item_ids:
                return {"page_intro_claims": [], "section_summaries": []}
            return {
                "page_intro_claims": [
                    {
                        "text": f"Synth summary for {packet['title']}.",
                        "latent_type": "human_readable_synthesis_prose",
                        "confidence": "strong",
                        "supporting_item_ids": item_ids[: min(2, len(item_ids))],
                    }
                ],
                "section_summaries": [],
            }

        return fake_structured_json

    def make_fake_bootstrap_synthesizer(self):
        def fake_structured_json(*, config, system_prompt, user_prompt, schema):
            packet = json.loads(user_prompt)
            sections = []
            for section in packet.get("sections", []):
                bullets = []
                for item in section.get("items", []):
                    bullets.append(
                        {
                            "text": f"Boot {section['title']}: {item['statement']}",
                            "supporting_item_keys": [str(item["item_key"])],
                        }
                    )
                if not bullets and section.get("claims"):
                    claim = section["claims"][0]
                    bullets.append(
                        {
                            "text": f"Boot {section['title']}: {claim['text']}",
                            "supporting_item_keys": [str(item) for item in claim["supporting_item_ids"]],
                            "supporting_claim_ids": [str(claim["claim_id"])],
                        }
                    )
                sections.append({"section_id": str(section["section_id"]), "bullets": bullets})
            return {"sections": sections}

        return fake_structured_json

    def read_json(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def read_phase_status_map(self, result) -> dict[str, dict]:
        return {status.phase: status.to_dict() for status in result.report.phase_statuses}

    def read_refresh_state(self) -> dict:
        return self.read_json(self.state_dir / "refresh_state.json")["refresh"]

    def test_no_op_rerun_skips_downstream_phases(self) -> None:
        session_id = str(uuid4())
        make_source_file(
            self.source_path(session_id, "ai-trader"),
            session_id,
            cwd="C:\\repos\\ai-trader",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:00:00.000Z",
                    "type": "event_msg",
                    "payload": {"type": "user_message", "message": "Update the AI Trader strategy."},
                }
            ],
        )
        self.write_configs()

        first = self.run_refresh_with_fake_llm()
        self.assertTrue(first.report.success)
        second = self.run_refresh_with_fake_llm()
        self.assertTrue(second.report.success)
        status_map = self.read_phase_status_map(second)
        self.assertFalse(status_map["discover"]["skipped"])
        self.assertFalse(status_map["normalize"]["skipped"])
        for phase in ("segment", "classify", "extract", "wiki", "bootstrap", "audit"):
            self.assertTrue(status_map[phase]["skipped"])

    def test_new_source_only_fans_out_to_affected_domain(self) -> None:
        ai_trader_id = str(uuid4())
        open_brain_id = str(uuid4())
        make_source_file(
            self.source_path(ai_trader_id, "ai-trader"),
            ai_trader_id,
            cwd="C:\\repos\\ai-trader",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:01:00.000Z",
                    "type": "event_msg",
                    "payload": {"type": "user_message", "message": "Current state: AI Trader broker integration is in progress."},
                }
            ],
        )
        self.write_configs()
        first = self.run_refresh_with_fake_llm()
        self.assertTrue(first.report.success)
        wiki_state_before = self.read_json(self.state_dir / "wiki_state.json")
        page_runs_before = {item["page_id"]: item["last_run_id"] for item in wiki_state_before["pages"]}

        make_source_file(
            self.source_path(open_brain_id, "open-brain"),
            open_brain_id,
            cwd="C:\\repos\\sessionmemory",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:02:00.000Z",
                    "type": "event_msg",
                    "payload": {"type": "user_message", "message": "Open Brain architecture uses a memory pipeline component."},
                }
            ],
        )

        second = self.run_refresh_with_fake_llm()
        self.assertTrue(second.report.success)
        self.assertIn(open_brain_id, second.report.changed_source_ids)
        wiki_state_after = self.read_json(self.state_dir / "wiki_state.json")
        page_runs_after = {item["page_id"]: item["last_run_id"] for item in wiki_state_after["pages"]}
        self.assertEqual(page_runs_before["projects/ai-trader/current-state"], page_runs_after["projects/ai-trader/current-state"])
        self.assertNotEqual(page_runs_before.get("projects/open-brain/architecture"), page_runs_after["projects/open-brain/architecture"])

    def test_taxonomy_change_forces_classify_through_audit_full(self) -> None:
        session_id = str(uuid4())
        make_source_file(
            self.source_path(session_id, "ai-trader"),
            session_id,
            cwd="C:\\repos\\ai-trader",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:03:00.000Z",
                    "type": "event_msg",
                    "payload": {"type": "user_message", "message": "Update the AI Trader strategy."},
                }
            ],
        )
        self.write_configs()
        first = self.run_refresh_with_fake_llm()
        self.assertTrue(first.report.success)

        taxonomy_payload = self.read_json(self.taxonomy_path)
        taxonomy_payload["taxonomy_version"] = int(taxonomy_payload["taxonomy_version"]) + 1
        self.taxonomy_path.write_text(json.dumps(taxonomy_payload, indent=2), encoding="utf-8")

        second = self.run_refresh_with_fake_llm()
        self.assertTrue(second.report.success)
        status_map = self.read_phase_status_map(second)
        self.assertEqual(status_map["classify"]["scope_mode"], "full")
        self.assertEqual(status_map["extract"]["scope_mode"], "full")
        self.assertEqual(status_map["wiki"]["scope_mode"], "full")
        self.assertEqual(status_map["bootstrap"]["scope_mode"], "full")
        self.assertEqual(status_map["audit"]["scope_mode"], "full")

    def test_manual_scoped_refresh_only_updates_requested_slice(self) -> None:
        ai_trader_id = str(uuid4())
        open_brain_id = str(uuid4())
        make_source_file(
            self.source_path(ai_trader_id, "ai-trader"),
            ai_trader_id,
            cwd="C:\\repos\\ai-trader",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:04:00.000Z",
                    "type": "event_msg",
                    "payload": {"type": "user_message", "message": "Update the AI Trader strategy."},
                }
            ],
        )
        make_source_file(
            self.source_path(open_brain_id, "open-brain"),
            open_brain_id,
            cwd="C:\\repos\\sessionmemory",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:04:30.000Z",
                    "type": "event_msg",
                    "payload": {"type": "user_message", "message": "Open Brain architecture uses a memory pipeline component."},
                }
            ],
        )
        self.write_configs()
        first = self.run_refresh_with_fake_llm()
        self.assertTrue(first.report.success)
        wiki_state_before = self.read_json(self.state_dir / "wiki_state.json")
        page_runs_before = {item["page_id"]: item["last_run_id"] for item in wiki_state_before["pages"]}

        second = self.run_refresh_with_fake_llm(source_ids=[ai_trader_id])
        self.assertTrue(second.report.success)
        status_map = self.read_phase_status_map(second)
        self.assertEqual(status_map["segment"]["scope_mode"], "scoped")
        self.assertEqual(status_map["classify"]["scope_mode"], "scoped")
        self.assertEqual(status_map["wiki"]["scope_mode"], "scoped")
        wiki_state_after = self.read_json(self.state_dir / "wiki_state.json")
        page_runs_after = {item["page_id"]: item["last_run_id"] for item in wiki_state_after["pages"]}
        self.assertEqual(page_runs_before["projects/open-brain/architecture"], page_runs_after["projects/open-brain/architecture"])

    def test_fresh_lock_fails_fast(self) -> None:
        self.write_configs()
        self.state_dir.mkdir(parents=True, exist_ok=True)
        lock_path = self.state_dir / "refresh.lock.json"
        lock_path.write_text(
            json.dumps(
                {
                    "run_id": "other-run",
                    "pid": 123,
                    "hostname": "test-host",
                    "started_at": datetime.now(timezone.utc).isoformat(),
                    "heartbeat_at": datetime.now(timezone.utc).isoformat(),
                    "command": "python -m sessionmemory refresh",
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        result = run_refresh(
            config_path=self.refresh_config_path,
            state_dir=self.state_dir,
            audits_dir=self.audits_dir,
            normalized_dir=self.normalized_dir,
            segmented_dir=self.segmented_dir,
            classified_dir=self.classified_dir,
            extracted_dir=self.extracted_dir,
            wiki_dir=self.wiki_dir,
            bootstrap_dir=self.bootstrap_dir,
        )
        self.assertFalse(result.report.success)
        self.assertIn("already active", result.report.fatal_error_summary or "")

    def test_phase_failure_records_partial_progress(self) -> None:
        session_id = str(uuid4())
        make_source_file(
            self.source_path(session_id, "ai-trader"),
            session_id,
            cwd="C:\\repos\\ai-trader",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:05:00.000Z",
                    "type": "event_msg",
                    "payload": {"type": "user_message", "message": "Update the AI Trader strategy."},
                }
            ],
        )
        self.write_configs()
        good = self.run_refresh_with_fake_llm()
        self.assertTrue(good.report.success)

        def failed_classification(*args, **kwargs):
            return ClassificationResult(
                report=ClassificationRunReport(
                    run_id="classify-failed",
                    started_at="2026-04-13T00:00:00Z",
                    finished_at="2026-04-13T00:00:01Z",
                    source_status_counts={},
                    classified_segment_count=0,
                    primary_label_counts={},
                    confidence_counts={},
                    notice_count=0,
                    success=False,
                    fatal_error_summary="classification boom",
                ),
                state_path=self.state_dir / "classification_state.json",
                run_log_path=self.state_dir / "classification_runs.jsonl",
                notice_log_path=self.audits_dir / "classification_notices.jsonl",
            )

        with patch("sessionmemory.refresh.run_classification", side_effect=failed_classification), patch(
            "sessionmemory.wiki.call_openai_structured_json",
            side_effect=self.make_fake_wiki_synthesizer(),
        ), patch(
            "sessionmemory.bootstrap.call_openai_structured_json",
            side_effect=self.make_fake_bootstrap_synthesizer(),
        ):
            failed = run_refresh(
                config_path=self.refresh_config_path,
                state_dir=self.state_dir,
                audits_dir=self.audits_dir,
                source_ids=[session_id],
                normalized_dir=self.normalized_dir,
                segmented_dir=self.segmented_dir,
                classified_dir=self.classified_dir,
                extracted_dir=self.extracted_dir,
                wiki_dir=self.wiki_dir,
                bootstrap_dir=self.bootstrap_dir,
            )

        self.assertFalse(failed.report.success)
        self.assertEqual(failed.report.failed_phase, "classify")
        refresh_state = self.read_refresh_state()
        self.assertEqual(refresh_state["last_result_status"], "failed")
        self.assertEqual(refresh_state["last_failed_phase"], "classify")
