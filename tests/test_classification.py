from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path
from uuid import uuid4

from wikimemory.classification import run_classification
from wikimemory.discovery import run_discovery
from wikimemory.normalization import run_normalization
from wikimemory.segmentation import run_segmentation


def make_source_file(
    path: Path,
    session_id: str,
    extra_lines: list[dict] | None = None,
    cwd: str = "C:\\repo",
) -> None:
    extra_lines = extra_lines or []
    lines = [
        {
            "timestamp": "2026-04-12T20:59:14.432Z",
            "type": "session_meta",
            "payload": {
                "id": session_id,
                "timestamp": "2026-04-12T20:59:14.432Z",
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


class ClassificationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="wikimemory-classify-"))
        self.root = self.temp_dir / "sessions"
        self.state_dir = self.temp_dir / "state"
        self.normalized_dir = self.temp_dir / "normalized"
        self.segmented_dir = self.temp_dir / "segmented"
        self.classified_dir = self.temp_dir / "classified"
        self.audits_dir = self.temp_dir / "audits"
        self.config_path = self.temp_dir / "source_roots.json"
        repo_root = Path(__file__).resolve().parents[1]
        self.schema_path = repo_root / "schema" / "normalization_catalog.json"
        self.taxonomy_path = repo_root / "config" / "classification_taxonomy.json"

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def write_config(self) -> None:
        payload = {
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
        }
        self.config_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def source_path(self, session_id: str, *subdirs: str) -> Path:
        base = self.root / "2026" / "04" / "12"
        for part in subdirs:
            base /= part
        return base / f"rollout-2026-04-12T20-59-14-{session_id}.jsonl"

    def run_until_segmented(self) -> tuple[object, object, object]:
        discovery_result = run_discovery(self.config_path, self.state_dir)
        normalization_result = run_normalization(
            config_path=self.config_path,
            state_dir=self.state_dir,
            schema_path=self.schema_path,
            normalized_dir=self.normalized_dir,
            audits_dir=self.audits_dir,
        )
        segmentation_result = run_segmentation(
            state_dir=self.state_dir,
            normalized_dir=self.normalized_dir,
            segmented_dir=self.segmented_dir,
        )
        return discovery_result, normalization_result, segmentation_result

    def run_full_pipeline(
        self,
        taxonomy_path: Path | None = None,
        source_ids: list[str] | None = None,
    ) -> tuple[object, object, object, object]:
        discovery_result, normalization_result, segmentation_result = self.run_until_segmented()
        classification_result = run_classification(
            taxonomy_path=taxonomy_path or self.taxonomy_path,
            state_dir=self.state_dir,
            normalized_dir=self.normalized_dir,
            segmented_dir=self.segmented_dir,
            classified_dir=self.classified_dir,
            audits_dir=self.audits_dir,
            source_ids=source_ids,
        )
        return discovery_result, normalization_result, segmentation_result, classification_result

    def read_json(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def read_jsonl(self, path: Path) -> list[dict]:
        return [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    def classified_segments(self, session_id: str) -> list[dict]:
        return self.read_jsonl(self.classified_dir / "sources" / session_id / "segments.jsonl")

    def test_ai_trader_segment_classifies_from_repo_and_domain_signals(self) -> None:
        session_id = str(uuid4())
        make_source_file(
            self.source_path(session_id, "ai-trader"),
            session_id,
            cwd="C:\\repos\\ai-trader",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:00:00.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "Update the AI Trader backtest strategy and market data broker integration.",
                    },
                }
            ],
        )
        self.write_config()

        _, _, _, classification_result = self.run_full_pipeline()
        self.assertTrue(classification_result.report.success)

        segment = self.classified_segments(session_id)[0]
        self.assertEqual(segment["primary_label"], "ai-trader")
        self.assertEqual(segment["confidence"], "explicit")
        self.assertTrue(any(signal["rule_id"].startswith("ai-trader.") for signal in segment["matched_signals"]))

    def test_aitrader_spelling_and_finance_terms_classify_project(self) -> None:
        session_id = str(uuid4())
        make_source_file(
            self.source_path(session_id, "shared"),
            session_id,
            cwd="C:\\repos\\AITrader",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:00:00.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "For the AITrader project, evaluate Alpaca, Tradier, Finnhub, VIX, SPY, QQQ, earnings, and options chains for market data ingestion.",
                    },
                }
            ],
        )
        self.write_config()

        _, _, _, classification_result = self.run_full_pipeline()
        self.assertTrue(classification_result.report.success)

        segment = self.classified_segments(session_id)[0]
        self.assertEqual(segment["primary_label"], "ai-trader")
        self.assertIn(segment["confidence"], {"explicit", "strong", "inferred"})

    def test_low_signal_reasoning_segment_keeps_project_context(self) -> None:
        session_id = str(uuid4())
        make_source_file(
            self.source_path(session_id, "shared"),
            session_id,
            cwd="C:\\repos\\shared-rag",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:00:00.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "For the AITrader project, evaluate Alpaca and Tradier market data providers.",
                    },
                },
                {
                    "timestamp": "2026-04-12T21:00:01.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "agent_reasoning",
                        "text": "Planning the inspection of provider docs before scoring the ingestion options.",
                    },
                },
                {
                    "timestamp": "2026-04-12T21:00:01.100Z",
                    "type": "response_item",
                    "payload": {
                        "type": "reasoning",
                        "summary": [
                            {
                                "text": "Preparing documentation review for the same provider evaluation.",
                                "type": "summary_text",
                            }
                        ],
                    },
                },
            ],
        )
        self.write_config()

        _, _, _, classification_result = self.run_full_pipeline()
        self.assertTrue(classification_result.report.success)

        segments = self.classified_segments(session_id)
        self.assertTrue(segments)
        self.assertTrue(all(segment["primary_label"] == "ai-trader" for segment in segments))
        self.assertFalse(any(segment["primary_label"] == "unclassified" for segment in segments))

    def test_low_signal_agent_message_segment_keeps_project_context(self) -> None:
        session_id = str(uuid4())
        make_source_file(
            self.source_path(session_id, "shared"),
            session_id,
            cwd="C:\\repos\\shared-rag",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:00:00.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "For the AITrader project, evaluate Alpaca and Tradier market data providers.",
                    },
                },
                {
                    "timestamp": "2026-04-12T21:00:01.000Z",
                    "type": "response_item",
                    "payload": {
                        "type": "message",
                        "role": "assistant",
                        "content": [
                            {
                                "type": "output_text",
                                "text": "environment mode default collaboration_mode workspace metadata",
                            }
                        ],
                    },
                },
                {
                    "timestamp": "2026-04-12T21:00:02.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "agent_message",
                        "message": "Next, compare those providers against the current broker ingestion code.",
                    },
                },
            ],
        )
        self.write_config()

        _, _, _, classification_result = self.run_full_pipeline()
        self.assertTrue(classification_result.report.success)

        segments = self.classified_segments(session_id)
        self.assertTrue(segments)
        self.assertFalse(any(segment["primary_label"] == "unclassified" for segment in segments))
        self.assertTrue(any("contextual_inheritance" in segment.get("classification_flags", []) for segment in segments))

    def test_contextual_override_cascades_across_low_signal_chain(self) -> None:
        session_id = str(uuid4())
        make_source_file(
            self.source_path(session_id, "shared"),
            session_id,
            cwd="C:\\repos\\shared-rag",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:00:00.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "For the AITrader project, inspect Tradier option chain endpoints.",
                    },
                },
                {
                    "timestamp": "2026-04-12T21:00:01.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "agent_reasoning",
                        "text": "Adjusting search approach for endpoint discovery.",
                    },
                },
                {
                    "timestamp": "2026-04-12T21:00:02.000Z",
                    "type": "response_item",
                    "payload": {
                        "type": "reasoning",
                        "summary": [{"type": "summary_text", "text": "Testing direct URL variations."}],
                    },
                },
                {
                    "timestamp": "2026-04-12T21:00:03.000Z",
                    "type": "response_item",
                    "payload": {
                        "type": "web_search_call",
                        "query": "Tradier options endpoint documentation",
                    },
                },
                {
                    "timestamp": "2026-04-12T21:00:04.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "agent_message",
                        "message": "The Tradier docs list the option chains endpoint under market data.",
                    },
                },
            ],
        )
        self.write_config()

        _, _, _, classification_result = self.run_full_pipeline()
        self.assertTrue(classification_result.report.success)

        segments = self.classified_segments(session_id)
        self.assertTrue(segments)
        self.assertFalse(any(segment["primary_label"] == "unclassified" for segment in segments))

    def test_global_segment_classifies_from_workflow_preferences(self) -> None:
        session_id = str(uuid4())
        make_source_file(
            self.source_path(session_id, "shared"),
            session_id,
            cwd="C:\\repos\\shared-rag",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:01:00.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "Communication preference: be concise and do not refactor unrelated files. Workflow rules apply everywhere.",
                    },
                }
            ],
        )
        self.write_config()

        _, _, _, classification_result = self.run_full_pipeline()
        self.assertTrue(classification_result.report.success)
        segment = self.classified_segments(session_id)[0]
        self.assertEqual(segment["primary_label"], "global")
        self.assertEqual(segment["confidence"], "explicit")

    def test_weak_meta_segment_inherits_source_dominant_label(self) -> None:
        session_id = str(uuid4())
        make_source_file(
            self.source_path(session_id, "shared"),
            session_id,
            cwd="C:\\repos\\shared-rag",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T20:59:15.000Z",
                    "type": "response_item",
                    "payload": {
                        "type": "message",
                        "role": "assistant",
                        "content": [
                            {
                                "type": "output_text",
                                "text": " ".join(["mode", "default", "collaboration_mode"] * 200),
                            }
                        ],
                    },
                },
                {
                    "timestamp": "2026-04-12T20:59:16.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "turn_aborted",
                    },
                },
                {
                    "timestamp": "2026-04-12T20:59:17.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "task_started",
                    },
                },
                {
                    "timestamp": "2026-04-12T21:01:00.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "For AI Trader, update the broker integration and backtest ingestion pipeline.",
                    },
                },
            ],
        )
        self.write_config()

        _, _, _, classification_result = self.run_full_pipeline()
        self.assertTrue(classification_result.report.success)
        segments = self.classified_segments(session_id)
        self.assertFalse(any(segment["primary_label"] == "unclassified" for segment in segments))
        self.assertTrue(any("contextual_inheritance" in segment.get("classification_flags", []) for segment in segments))

    def test_weak_conversational_followup_inherits_project_context(self) -> None:
        session_id = str(uuid4())
        make_source_file(
            self.source_path(session_id, "open-brain"),
            session_id,
            cwd="C:\\repos\\open-brain",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:00:00.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "For Open Brain, update the memory wiki retrieval pipeline and bootstrap flow.",
                    },
                },
                {
                    "timestamp": "2026-04-12T21:00:02.000Z",
                    "type": "turn_context",
                    "payload": {
                        "cwd": "C:\\repos\\open-brain",
                        "notes": "looks great please",
                    },
                },
                {
                    "timestamp": "2026-04-12T21:00:03.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "Looks great please continue.",
                    },
                },
            ],
        )
        self.write_config()

        _, _, _, classification_result = self.run_full_pipeline()
        self.assertTrue(classification_result.report.success)
        segments = self.classified_segments(session_id)
        self.assertFalse(any(segment["primary_label"] == "unclassified" for segment in segments))
        self.assertTrue(any(segment["primary_label"] == "open-brain" for segment in segments))

    def test_open_brain_and_ai_scientist_disambiguate_inside_shared_repo(self) -> None:
        open_brain_id = str(uuid4())
        ai_scientist_id = str(uuid4())
        shared_cwd = "C:\\repos\\shared-rag"

        make_source_file(
            self.source_path(open_brain_id, "shared"),
            open_brain_id,
            cwd=shared_cwd,
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:02:00.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "Open Brain memory system bootstrap memory wiki retrieval pipeline.",
                    },
                }
            ],
        )
        make_source_file(
            self.source_path(ai_scientist_id, "shared"),
            ai_scientist_id,
            cwd=shared_cwd,
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:02:30.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "AI Scientist hypothesis loop for rag optimization benchmark precision and recall.",
                    },
                }
            ],
        )
        self.write_config()

        _, _, _, classification_result = self.run_full_pipeline()
        self.assertTrue(classification_result.report.success)
        self.assertEqual(self.classified_segments(open_brain_id)[0]["primary_label"], "open-brain")
        self.assertEqual(self.classified_segments(ai_scientist_id)[0]["primary_label"], "ai-scientist")

    def test_mixed_open_brain_and_ai_scientist_becomes_cross_project(self) -> None:
        session_id = str(uuid4())
        make_source_file(
            self.source_path(session_id, "shared"),
            session_id,
            cwd="C:\\repos\\shared-rag",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:03:00.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "Connect Open Brain memory system with AI Scientist optimization loop for rag benchmark evaluation.",
                    },
                }
            ],
        )
        self.write_config()

        _, _, _, classification_result = self.run_full_pipeline()
        self.assertTrue(classification_result.report.success)
        segment = self.classified_segments(session_id)[0]
        self.assertEqual(segment["primary_label"], "cross-project")
        self.assertIn("open-brain", segment["secondary_labels"])
        self.assertIn("ai-scientist", segment["secondary_labels"])

    def test_project_work_plus_global_rules_keeps_project_primary(self) -> None:
        session_id = str(uuid4())
        make_source_file(
            self.source_path(session_id, "ai-trader"),
            session_id,
            cwd="C:\\repos\\ai-trader",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:04:00.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "For AI Trader, workflow rule: be concise and do not refactor unrelated files while updating the broker integration.",
                    },
                }
            ],
        )
        self.write_config()

        _, _, _, classification_result = self.run_full_pipeline()
        self.assertTrue(classification_result.report.success)
        segment = self.classified_segments(session_id)[0]
        self.assertEqual(segment["primary_label"], "ai-trader")
        self.assertIn("global", segment["secondary_labels"])

    def test_weak_evidence_falls_back_to_unclassified_with_notice(self) -> None:
        session_id = str(uuid4())
        make_source_file(
            self.source_path(session_id, "shared"),
            session_id,
            cwd="C:\\repos\\shared-rag",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:05:00.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "Look into the current issue later.",
                    },
                }
            ],
        )
        self.write_config()

        _, _, _, classification_result = self.run_full_pipeline()
        self.assertTrue(classification_result.report.success)
        segment = self.classified_segments(session_id)[0]
        self.assertEqual(segment["primary_label"], "unclassified")
        notices = self.read_jsonl(self.audits_dir / "classification_notices.jsonl")
        self.assertTrue(any(notice["segment_id"] == segment["segment_id"] for notice in notices))

    def test_taxonomy_version_bump_forces_full_reclassification(self) -> None:
        session_id = str(uuid4())
        make_source_file(
            self.source_path(session_id, "ai-trader"),
            session_id,
            cwd="C:\\repos\\ai-trader",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:06:00.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "AI Trader backtest strategy refresh.",
                    },
                }
            ],
        )
        self.write_config()
        self.run_full_pipeline()

        bumped_taxonomy_path = self.temp_dir / "classification_taxonomy.bumped.json"
        taxonomy_payload = self.read_json(self.taxonomy_path)
        taxonomy_payload["taxonomy_version"] = 2
        bumped_taxonomy_path.write_text(json.dumps(taxonomy_payload, indent=2), encoding="utf-8")

        result = run_classification(
            taxonomy_path=bumped_taxonomy_path,
            state_dir=self.state_dir,
            normalized_dir=self.normalized_dir,
            segmented_dir=self.segmented_dir,
            classified_dir=self.classified_dir,
            audits_dir=self.audits_dir,
        )
        self.assertTrue(result.report.success)
        self.assertEqual(result.report.source_status_counts, {"classified": 1})
        state_payload = self.read_json(self.state_dir / "classification_state.json")
        self.assertEqual(state_payload["sources"][0]["taxonomy_version"], 2)

    def test_sample_scoped_classification_only_writes_requested_sources(self) -> None:
        target_id = str(uuid4())
        skipped_id = str(uuid4())
        make_source_file(
            self.source_path(target_id, "ai-trader"),
            target_id,
            cwd="C:\\repos\\ai-trader",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:07:00.000Z",
                    "type": "event_msg",
                    "payload": {"type": "user_message", "message": "AI Trader broker refresh."},
                }
            ],
        )
        make_source_file(
            self.source_path(skipped_id, "shared"),
            skipped_id,
            cwd="C:\\repos\\shared-rag",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:07:10.000Z",
                    "type": "event_msg",
                    "payload": {"type": "user_message", "message": "Communication preference: be concise."},
                }
            ],
        )
        self.write_config()
        self.run_until_segmented()

        result = run_classification(
            taxonomy_path=self.taxonomy_path,
            state_dir=self.state_dir,
            normalized_dir=self.normalized_dir,
            segmented_dir=self.segmented_dir,
            classified_dir=self.classified_dir,
            audits_dir=self.audits_dir,
            source_ids=[target_id],
        )
        self.assertTrue(result.report.success)
        self.assertEqual(result.report.source_status_counts, {"classified": 1})
        self.assertTrue((self.classified_dir / "sources" / target_id / "segments.jsonl").exists())
        self.assertFalse((self.classified_dir / "sources" / skipped_id).exists())

    def test_tombstoned_source_keeps_artifacts_and_marks_state(self) -> None:
        session_id = str(uuid4())
        source_path = self.source_path(session_id, "ai-trader")
        make_source_file(
            source_path,
            session_id,
            cwd="C:\\repos\\ai-trader",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:08:00.000Z",
                    "type": "event_msg",
                    "payload": {"type": "user_message", "message": "AI Trader backtest strategy update."},
                }
            ],
        )
        self.write_config()
        self.run_full_pipeline()

        classified_source_dir = self.classified_dir / "sources" / session_id
        self.assertTrue((classified_source_dir / "segments.jsonl").exists())

        source_path.unlink()
        discovery_result, normalization_result, segmentation_result, classification_result = self.run_full_pipeline()
        self.assertTrue(discovery_result.report.success)
        self.assertTrue(normalization_result.report.success)
        self.assertTrue(segmentation_result.report.success)
        self.assertTrue(classification_result.report.success)

        state_payload = self.read_json(self.state_dir / "classification_state.json")
        self.assertEqual(state_payload["sources"][0]["status"], "tombstoned")
        self.assertTrue((classified_source_dir / "segments.jsonl").exists())

    def test_invalid_taxonomy_preserves_prior_state(self) -> None:
        session_id = str(uuid4())
        make_source_file(
            self.source_path(session_id, "ai-trader"),
            session_id,
            cwd="C:\\repos\\ai-trader",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:09:00.000Z",
                    "type": "event_msg",
                    "payload": {"type": "user_message", "message": "AI Trader market data update."},
                }
            ],
        )
        self.write_config()
        self.run_full_pipeline()

        prior_state_text = (self.state_dir / "classification_state.json").read_text(encoding="utf-8")
        prior_segments_text = (
            self.classified_dir / "sources" / session_id / "segments.jsonl"
        ).read_text(encoding="utf-8")

        invalid_taxonomy_path = self.temp_dir / "classification_taxonomy.invalid.json"
        invalid_taxonomy_path.write_text("{invalid json", encoding="utf-8")

        result = run_classification(
            taxonomy_path=invalid_taxonomy_path,
            state_dir=self.state_dir,
            normalized_dir=self.normalized_dir,
            segmented_dir=self.segmented_dir,
            classified_dir=self.classified_dir,
            audits_dir=self.audits_dir,
        )
        self.assertFalse(result.report.success)
        self.assertEqual((self.state_dir / "classification_state.json").read_text(encoding="utf-8"), prior_state_text)
        self.assertEqual(
            (self.classified_dir / "sources" / session_id / "segments.jsonl").read_text(encoding="utf-8"),
            prior_segments_text,
        )


if __name__ == "__main__":
    unittest.main()
