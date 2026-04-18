from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from uuid import uuid4

from wikimemory.full_load import run_full_load


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


class FullLoadTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="wikimemory-full-load-"))
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
        self.full_load_config_path = self.temp_dir / "full_load_config.json"
        repo_root = Path(__file__).resolve().parents[1]
        self.schema_path = repo_root / "schema" / "normalization_catalog.json"
        self.base_taxonomy_path = repo_root / "config" / "classification_taxonomy.json"
        self.base_rules_path = repo_root / "config" / "extraction_rules.json"
        self.base_wiki_config_path = repo_root / "config" / "wiki_config.json"
        self.base_bootstrap_config_path = repo_root / "config" / "bootstrap_config.json"
        self.base_audit_config_path = repo_root / "config" / "audit_config.json"
        self.live_manifest_path = repo_root / "tests" / "fixtures" / "live_corpus_manifest.json"

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def write_configs(self, *, max_derived_bytes: int = 10 * 1024 * 1024 * 1024, max_retries: int = 5) -> None:
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

        full_load_payload = {
            "schema_version": 1,
            "full_load_schema_version": 1,
            "rules_version": 1,
            "paths": {
                "source_roots_config": str(self.source_config_path),
                "normalization_schema": str(self.schema_path),
                "classification_taxonomy": str(self.taxonomy_path),
                "extraction_rules": str(self.rules_path),
                "wiki_config": str(self.wiki_config_path),
                "bootstrap_config": str(self.bootstrap_config_path),
                "audit_config": str(self.audit_config_path),
                "live_control_sample_manifest": str(self.live_manifest_path),
            },
            "disk_budget": {
                "max_derived_bytes": max_derived_bytes,
                "tracked_dirs": [
                    "normalized",
                    "segmented",
                    "classified",
                    "extracted",
                    "wiki",
                    "bootstrap",
                    "state",
                    "audits",
                ],
            },
            "retry_policy": {
                "max_phase_repair_loops": max_retries,
                "repeated_non_improving_limit": 2,
            },
            "phase_gates": {
                "discover": {"require_success": True},
                "normalize": {"require_success": True},
                "segment": {"require_success": True},
                "classify": {"require_success": True, "require_zero_unclassified": True, "blocking_notice_types": ["taxonomy_gap"]},
                "extract": {"require_success": True, "require_zero_unclassified": True},
                "wiki": {"require_success": True},
                "bootstrap": {"require_success": True},
                "audit": {"require_success": True, "require_zero_errors": True},
            },
        }
        self.full_load_config_path.write_text(json.dumps(full_load_payload, indent=2), encoding="utf-8")

    def source_path(self, session_id: str, *subdirs: str) -> Path:
        base = self.root / "2026" / "04" / "12"
        for part in subdirs:
            base /= part
        return base / f"rollout-2026-04-12T20-59-14-{session_id}.jsonl"

    def run_full_load_with_fake_llm(self):
        with patch("wikimemory.wiki.call_openai_structured_json", side_effect=self.make_fake_wiki_synthesizer()), patch(
            "wikimemory.bootstrap.call_openai_structured_json",
            side_effect=self.make_fake_bootstrap_synthesizer(),
        ):
            return run_full_load(
                config_path=self.full_load_config_path,
                state_dir=self.state_dir,
                audits_dir=self.audits_dir,
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

    def test_full_load_happy_path(self) -> None:
        session_id = str(uuid4())
        make_source_file(
            self.source_path(session_id, "ai-trader"),
            session_id,
            cwd="C:\\repos\\ai-trader",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:00:00.000Z",
                    "type": "event_msg",
                    "payload": {"type": "user_message", "message": "Current state: AI Trader broker integration is in progress."},
                }
            ],
        )
        self.write_configs()

        result = self.run_full_load_with_fake_llm()
        self.assertTrue(result.report.success)
        self.assertEqual(result.report.last_completed_phase, "audit")
        self.assertIsNone(result.report.failed_phase)

    def test_classification_gate_writes_issue_bundle(self) -> None:
        session_id = str(uuid4())
        make_source_file(
            self.source_path(session_id, "misc"),
            session_id,
            cwd="C:\\repos\\misc",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:00:00.000Z",
                    "type": "event_msg",
                    "payload": {"type": "user_message", "message": "Please check this thing and maybe adjust it later."},
                }
            ],
        )
        self.write_configs()

        result = self.run_full_load_with_fake_llm()
        self.assertFalse(result.report.success)
        self.assertEqual(result.report.failed_phase, "classify")
        self.assertEqual(result.report.stop_reason, "repair_required")
        issue_path = self.audits_dir / "full_load_issues" / result.report.run_id / "classify" / "issue.json"
        issue_payload = self.read_json(issue_path)
        self.assertIn("source_ids", issue_payload["gate"]["details"]["recommended_scope"])

    def test_disk_budget_stop(self) -> None:
        session_id = str(uuid4())
        make_source_file(self.source_path(session_id, "ai-trader"), session_id)
        self.write_configs(max_derived_bytes=1)

        result = self.run_full_load_with_fake_llm()
        self.assertFalse(result.report.success)
        self.assertEqual(result.report.stop_reason, "disk_budget_exceeded")
        self.assertTrue(any(not status.gate_passed for status in result.report.phase_statuses))

    def test_repeated_non_improving_failure_stops_on_second_run(self) -> None:
        session_id = str(uuid4())
        make_source_file(
            self.source_path(session_id, "misc"),
            session_id,
            cwd="C:\\repos\\misc",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:00:00.000Z",
                    "type": "event_msg",
                    "payload": {"type": "user_message", "message": "Please check this thing and maybe adjust it later."},
                }
            ],
        )
        self.write_configs()

        first = self.run_full_load_with_fake_llm()
        self.assertFalse(first.report.success)
        self.assertEqual(first.report.stop_reason, "repair_required")

        second = self.run_full_load_with_fake_llm()
        self.assertFalse(second.report.success)
        self.assertEqual(second.report.stop_reason, "repeated_non_improving_failure")
