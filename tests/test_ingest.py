from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from wikimemory.discovery import run_discovery
from wikimemory.ingest import run_ingest
from wikimemory.normalization import run_normalization
from wikimemory.product_config import default_product_config


class IngestTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="wikimemory-ingest-"))
        self.sessions_root = self.temp_dir / "sessions"
        self.project_root = self.temp_dir / "project"
        self.state_dir = self.temp_dir / "state"
        self.normalized_dir = self.temp_dir / "normalized"
        self.evidence_dir = self.temp_dir / "evidence"
        self.audits_dir = self.temp_dir / "audits"
        self.source_config = self.temp_dir / "source_roots.json"
        self.product_config = self.temp_dir / "product_config.json"
        repo_root = Path(__file__).resolve().parents[1]
        self.schema_path = repo_root / "schema" / "normalization_catalog.json"
        self.example_log = repo_root / "examples" / "source-logs" / "representative-session.jsonl"

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def write_source_config(self) -> None:
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

    def write_product_config(self) -> None:
        payload = default_product_config(self.project_root).to_dict()
        payload["log_sources"][0]["root_alias"] = "example_sessions"
        payload["log_sources"][0]["absolute_path"] = str(self.sessions_root)
        payload["project_sources"][0]["project_root"] = str(self.project_root)
        self.product_config.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def init_git_project(self) -> None:
        self.project_root.mkdir(parents=True)
        subprocess.run(["git", "-C", str(self.project_root), "init"], check=True, capture_output=True, text=True)
        (self.project_root / "README.md").write_text("# Example\n", encoding="utf-8")

    def read_jsonl(self, path: Path) -> list[dict]:
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

    def test_ingest_builds_log_and_project_evidence_from_real_sample(self) -> None:
        target_log = (
            self.sessions_root
            / "2026"
            / "02"
            / "26"
            / "rollout-2026-02-26T21-48-04-019c9cff-0337-77e0-9ba6-a4f6dc75a92e.jsonl"
        )
        target_log.parent.mkdir(parents=True)
        shutil.copyfile(self.example_log, target_log)
        self.init_git_project()
        self.write_source_config()
        self.write_product_config()

        discovery_result = run_discovery(self.source_config, self.state_dir)
        self.assertTrue(discovery_result.report.success)
        normalization_result = run_normalization(
            config_path=self.source_config,
            state_dir=self.state_dir,
            schema_path=self.schema_path,
            normalized_dir=self.normalized_dir,
            audits_dir=self.audits_dir,
        )
        self.assertTrue(normalization_result.report.success)

        result = run_ingest(
            product_config_path=self.product_config,
            state_dir=self.state_dir,
            normalized_dir=self.normalized_dir,
            evidence_dir=self.evidence_dir,
            audits_dir=self.audits_dir,
        )
        self.assertTrue(result.report.success)
        self.assertGreater(result.report.evidence_counts["log_event"], 0)
        self.assertGreater(result.report.evidence_counts["git_head"], 0)
        self.assertGreater(result.report.evidence_counts["git_status_item"], 0)

        log_files = list((self.evidence_dir / "logs").glob("*.jsonl"))
        project_files = list((self.evidence_dir / "projects").glob("*.jsonl"))
        self.assertEqual(len(log_files), 1)
        self.assertEqual(len(project_files), 1)

        log_record = self.read_jsonl(log_files[0])[0]
        self.assertEqual(log_record["source_adapter"], "codex_jsonl")
        self.assertIn("source_byte_start", log_record["provenance"])
        self.assertIn("content_surfaces", log_record)

        project_records = self.read_jsonl(project_files[0])
        self.assertTrue(any(record["evidence_type"] == "git_status_item" for record in project_records))

    def test_source_scoped_ingest_filters_log_evidence(self) -> None:
        self.init_git_project()
        self.write_product_config()
        (self.normalized_dir / "sources" / "source-a").mkdir(parents=True)
        (self.normalized_dir / "sources" / "source-b").mkdir(parents=True)
        for source_id in ("source-a", "source-b"):
            session_payload = {"source_id": source_id, "session_meta_fields": {"cwd": str(self.project_root)}}
            (self.normalized_dir / "sources" / source_id / "session.json").write_text(
                json.dumps(session_payload),
                encoding="utf-8",
            )
            event_payload = {
                "event_id": f"{source_id}:1",
                "source_id": source_id,
                "source_line_no": 1,
                "source_byte_start": 0,
                "source_byte_end": 10,
                "event_digest": source_id,
                "canonical_kind": "event_msg.user_message",
                "outer_type": "event_msg",
                "payload_type": "user_message",
                "role": "user",
                "timestamp": "2026-04-18T00:00:00Z",
                "text_surface_truncated": False,
                "text_surfaces": [{"path": "payload.message", "text": f"Message {source_id}"}],
            }
            (self.normalized_dir / "sources" / source_id / "events.jsonl").write_text(
                json.dumps(event_payload) + "\n",
                encoding="utf-8",
            )

        result = run_ingest(
            product_config_path=self.product_config,
            state_dir=self.state_dir,
            normalized_dir=self.normalized_dir,
            evidence_dir=self.evidence_dir,
            audits_dir=self.audits_dir,
            source_ids=["source-b"],
        )
        self.assertTrue(result.report.success)
        self.assertFalse((self.evidence_dir / "logs" / "source-a.jsonl").exists())
        self.assertTrue((self.evidence_dir / "logs" / "source-b.jsonl").exists())

    def test_project_aliases_map_workspace_cwd_to_real_project_slug(self) -> None:
        self.init_git_project()
        payload = default_product_config(self.project_root).to_dict()
        payload["project_sources"][0]["project_root"] = str(self.project_root)
        payload["project_aliases"] = [
            {"slug": "open-brain", "aliases": ["OpenBrain", "open_brain"]},
        ]
        self.product_config.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        source_id = "source-open-brain"
        (self.normalized_dir / "sources" / source_id).mkdir(parents=True)
        session_payload = {
            "source_id": source_id,
            "session_meta_fields": {"cwd": r"C:\Users\Fabio\Cursor AI projects\Projects\OpenBrain"},
        }
        (self.normalized_dir / "sources" / source_id / "session.json").write_text(
            json.dumps(session_payload),
            encoding="utf-8",
        )
        event_payload = {
            "event_id": f"{source_id}:1",
            "source_id": source_id,
            "source_line_no": 1,
            "source_byte_start": 0,
            "source_byte_end": 10,
            "event_digest": source_id,
            "canonical_kind": "event_msg.user_message",
            "outer_type": "event_msg",
            "payload_type": "user_message",
            "role": "user",
            "timestamp": "2026-04-18T00:00:00Z",
            "text_surface_truncated": False,
            "text_surfaces": [{"path": "payload.message", "text": "OpenBrain memory context"}],
        }
        (self.normalized_dir / "sources" / source_id / "events.jsonl").write_text(
            json.dumps(event_payload) + "\n",
            encoding="utf-8",
        )

        result = run_ingest(
            product_config_path=self.product_config,
            state_dir=self.state_dir,
            normalized_dir=self.normalized_dir,
            evidence_dir=self.evidence_dir,
            audits_dir=self.audits_dir,
        )

        self.assertTrue(result.report.success)
        record = self.read_jsonl(self.evidence_dir / "logs" / f"{source_id}.jsonl")[0]
        self.assertEqual(record["project_hint"], "open-brain")

    def test_project_aliases_use_event_text_when_cwd_is_generic_workspace(self) -> None:
        self.init_git_project()
        payload = default_product_config(self.project_root).to_dict()
        payload["project_sources"][0]["project_root"] = str(self.project_root)
        payload["project_aliases"] = [
            {"slug": "wikimemory", "aliases": ["WikiMemory"]},
        ]
        self.product_config.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        source_id = "source-wikimemory"
        (self.normalized_dir / "sources" / source_id).mkdir(parents=True)
        (self.normalized_dir / "sources" / source_id / "session.json").write_text(
            json.dumps({"source_id": source_id, "session_meta_fields": {"cwd": r"C:\Users\Fabio\Projects"}}),
            encoding="utf-8",
        )
        event_payload = {
            "event_id": f"{source_id}:1",
            "source_id": source_id,
            "source_line_no": 1,
            "source_byte_start": 0,
            "source_byte_end": 10,
            "event_digest": source_id,
            "canonical_kind": "event_msg.user_message",
            "outer_type": "event_msg",
            "payload_type": "user_message",
            "role": "user",
            "timestamp": "2026-04-18T00:00:00Z",
            "text_surface_truncated": False,
            "text_surfaces": [{"path": "payload.message", "text": "Open tabs: WikiMemory/wikimemory/ingest.py"}],
        }
        (self.normalized_dir / "sources" / source_id / "events.jsonl").write_text(
            json.dumps(event_payload) + "\n",
            encoding="utf-8",
        )

        result = run_ingest(
            product_config_path=self.product_config,
            state_dir=self.state_dir,
            normalized_dir=self.normalized_dir,
            evidence_dir=self.evidence_dir,
            audits_dir=self.audits_dir,
        )

        self.assertTrue(result.report.success)
        record = self.read_jsonl(self.evidence_dir / "logs" / f"{source_id}.jsonl")[0]
        self.assertEqual(record["project_hint"], "wikimemory")

    def test_project_aliases_use_prefixed_path_mentions_before_session_hint(self) -> None:
        self.init_git_project()
        payload = default_product_config(self.project_root).to_dict()
        payload["project_sources"][0]["project_root"] = str(self.project_root)
        payload["project_aliases"] = [
            {"slug": "wikimemory", "aliases": ["WikiMemory"]},
            {"slug": "ai-trader", "aliases": ["AITrader", "ai-trader"]},
        ]
        self.product_config.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        source_id = "source-mixed"
        (self.normalized_dir / "sources" / source_id).mkdir(parents=True)
        (self.normalized_dir / "sources" / source_id / "session.json").write_text(
            json.dumps({"source_id": source_id, "session_meta_fields": {"cwd": r"C:\Users\Fabio\Projects\AITrader"}}),
            encoding="utf-8",
        )
        event_payload = {
            "event_id": f"{source_id}:1",
            "source_id": source_id,
            "source_line_no": 1,
            "source_byte_start": 0,
            "source_byte_end": 10,
            "event_digest": source_id,
            "canonical_kind": "response_item.message",
            "outer_type": "response_item",
            "payload_type": "message",
            "role": "user",
            "timestamp": "2026-04-18T00:00:00Z",
            "text_surface_truncated": False,
            "text_surfaces": [
                {
                    "path": "payload.content[0].text",
                    "text": "Open tabs:\n- workflow-rules.json: WikiMemory/wiki/_meta/pages/global/workflow-rules.json\n\nFix the wiki memory output.",
                }
            ],
        }
        (self.normalized_dir / "sources" / source_id / "events.jsonl").write_text(
            json.dumps(event_payload) + "\n",
            encoding="utf-8",
        )

        result = run_ingest(
            product_config_path=self.product_config,
            state_dir=self.state_dir,
            normalized_dir=self.normalized_dir,
            evidence_dir=self.evidence_dir,
            audits_dir=self.audits_dir,
        )

        self.assertTrue(result.report.success)
        record = self.read_jsonl(self.evidence_dir / "logs" / f"{source_id}.jsonl")[0]
        self.assertEqual(record["project_hint"], "wikimemory")

    def test_project_delta_ignores_generated_and_temp_paths(self) -> None:
        self.init_git_project()
        payload = default_product_config(self.project_root).to_dict()
        payload["project_sources"][0]["project_root"] = str(self.project_root)
        self.product_config.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        (self.project_root / "README.md").write_text(
            "# Example Project\n\nExample Project turns raw logs into compact memory files.\n",
            encoding="utf-8",
        )
        (self.project_root / ".tmp").mkdir()
        (self.project_root / ".tmp" / "scratch.md").write_text("temp", encoding="utf-8")
        (self.project_root / "memory").mkdir()
        (self.project_root / "memory" / "generated.md").write_text("generated", encoding="utf-8")
        (self.project_root / "src.py").write_text("print('real')\n", encoding="utf-8")

        result = run_ingest(
            product_config_path=self.product_config,
            state_dir=self.state_dir,
            normalized_dir=self.normalized_dir,
            evidence_dir=self.evidence_dir,
            audits_dir=self.audits_dir,
        )

        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        records = self.read_jsonl(next((self.evidence_dir / "projects").glob("*.jsonl")))
        texts = [surface["text"] for record in records for surface in record.get("content_surfaces", [])]
        self.assertTrue(any("src.py" in text for text in texts))
        self.assertFalse(any(".tmp" in text or "memory/generated.md" in text for text in texts))
        self.assertTrue(any(record["evidence_type"] == "project_overview_file" for record in records))

    def test_project_source_slug_uses_configured_alias(self) -> None:
        self.init_git_project()
        alias_root = self.temp_dir / "AITrader"
        alias_root.mkdir()
        (alias_root / ".git").mkdir()
        (alias_root / "README.md").write_text("# AI Trader\n\nAI Trader manages trading automation.\n", encoding="utf-8")
        payload = default_product_config(self.project_root).to_dict()
        payload["project_sources"] = [{"adapter": "git_worktree", "project_root": str(alias_root), "include_untracked": True}]
        payload["project_aliases"] = [{"slug": "ai-trader", "aliases": ["AITrader", "ai-trader"]}]
        self.product_config.write_text(json.dumps(payload, indent=2), encoding="utf-8")

        with patch("wikimemory.ingest.run_git_optional", return_value="abc123"), patch(
            "wikimemory.ingest.run_git",
            side_effect=lambda root, *args: "main" if args == ("branch", "--show-current") else "",
        ):
            result = run_ingest(
                product_config_path=self.product_config,
                state_dir=self.state_dir,
                normalized_dir=self.normalized_dir,
                evidence_dir=self.evidence_dir,
                audits_dir=self.audits_dir,
            )

        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        self.assertTrue((self.evidence_dir / "projects" / "ai-trader.jsonl").exists())

    def test_llm_project_routing_rewrites_unresolved_source_records(self) -> None:
        self.init_git_project()
        payload = default_product_config(self.project_root).to_dict()
        payload["project_sources"][0]["project_root"] = str(self.project_root)
        payload["project_aliases"] = [
            {"slug": "open-brain", "aliases": ["OpenBrain"]},
            {"slug": "ai-trader", "aliases": ["AITrader"]},
        ]
        payload["project_routing"]["enabled"] = True
        self.product_config.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        source_id = "source-ambiguous"
        (self.normalized_dir / "sources" / source_id).mkdir(parents=True)
        (self.normalized_dir / "sources" / source_id / "session.json").write_text(
            json.dumps({"source_id": source_id, "session_meta_fields": {"cwd": r"C:\Users\Fabio\Projects"}}),
            encoding="utf-8",
        )
        event_payload = {
            "event_id": f"{source_id}:1",
            "source_id": source_id,
            "source_line_no": 1,
            "source_byte_start": 0,
            "source_byte_end": 10,
            "event_digest": source_id,
            "canonical_kind": "event_msg.user_message",
            "outer_type": "event_msg",
            "payload_type": "user_message",
            "role": "user",
            "timestamp": "2026-04-18T00:00:00Z",
            "text_surface_truncated": False,
            "text_surfaces": [{"path": "payload.message", "text": "Need to improve metadata retrieval loop quality."}],
        }
        (self.normalized_dir / "sources" / source_id / "events.jsonl").write_text(
            json.dumps(event_payload) + "\n",
            encoding="utf-8",
        )
        decision = {
            "source_id": source_id,
            "project_hint": "open-brain",
            "confidence": "high",
            "supporting_evidence_ids": [],
        }

        with patch("wikimemory.project_routing.call_project_router", return_value=decision):
            result = run_ingest(
                product_config_path=self.product_config,
                state_dir=self.state_dir,
                normalized_dir=self.normalized_dir,
                evidence_dir=self.evidence_dir,
                audits_dir=self.audits_dir,
            )

        self.assertTrue(result.report.success)
        record = self.read_jsonl(self.evidence_dir / "logs" / f"{source_id}.jsonl")[0]
        self.assertEqual(record["project_hint"], "open-brain")
        self.assertEqual(record["metadata"]["llm_project_routing"]["confidence"], "high")

    def test_llm_project_routing_keeps_low_confidence_records_unresolved(self) -> None:
        self.init_git_project()
        payload = default_product_config(self.project_root).to_dict()
        payload["project_sources"][0]["project_root"] = str(self.project_root)
        payload["project_aliases"] = [
            {"slug": "open-brain", "aliases": ["OpenBrain"]},
            {"slug": "ai-trader", "aliases": ["AITrader"]},
        ]
        payload["project_routing"]["enabled"] = True
        self.product_config.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        source_id = "source-low-confidence"
        (self.normalized_dir / "sources" / source_id).mkdir(parents=True)
        (self.normalized_dir / "sources" / source_id / "session.json").write_text(
            json.dumps({"source_id": source_id, "session_meta_fields": {"cwd": r"C:\Users\Fabio\Projects"}}),
            encoding="utf-8",
        )
        event_payload = {
            "event_id": f"{source_id}:1",
            "source_id": source_id,
            "source_line_no": 1,
            "source_byte_start": 0,
            "source_byte_end": 10,
            "event_digest": source_id,
            "canonical_kind": "event_msg.user_message",
            "outer_type": "event_msg",
            "payload_type": "user_message",
            "role": "user",
            "timestamp": "2026-04-18T00:00:00Z",
            "text_surface_truncated": False,
            "text_surfaces": [{"path": "payload.message", "text": "Review the state and keep going."}],
        }
        (self.normalized_dir / "sources" / source_id / "events.jsonl").write_text(
            json.dumps(event_payload) + "\n",
            encoding="utf-8",
        )
        decision = {
            "source_id": source_id,
            "project_hint": "open-brain",
            "confidence": "low",
            "supporting_evidence_ids": [],
        }

        with patch("wikimemory.project_routing.call_project_router", return_value=decision):
            result = run_ingest(
                product_config_path=self.product_config,
                state_dir=self.state_dir,
                normalized_dir=self.normalized_dir,
                evidence_dir=self.evidence_dir,
                audits_dir=self.audits_dir,
            )

        self.assertTrue(result.report.success)
        record = self.read_jsonl(self.evidence_dir / "logs" / f"{source_id}.jsonl")[0]
        self.assertEqual(record["project_hint"], "projects")
