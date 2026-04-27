from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from sessionmemory.consumer_profile import run_consumer_profile


class ConsumerProfileTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="sessionmemory-consumer-profile-"))
        self.models_seen = []
        self.evidence_dir = self.temp_dir / "evidence"
        self.memory_dir = self.temp_dir / "memory"
        self.state_dir = self.temp_dir / "state"
        self.audits_dir = self.temp_dir / "audits"
        self.policy_path = self.temp_dir / "consumer_profile_policy.json"
        (self.evidence_dir / "logs").mkdir(parents=True)
        self.policy_path.write_text(
            json.dumps(
                {
                    "enabled": False,
                    "mode": "review_first",
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        records = [
            {
                "evidence_id": "e1",
                "actor_type": "user",
                "source_id": "source-1",
                "timestamp": "2026-04-25T10:00:00Z",
                "project_hint": "sessionmemory",
                "provenance": {"source_id": "source-1", "source_line_no": 11},
                "content_surfaces": [{"text": "Please keep responses concise and go implement instead of over-planning."}],
            },
            {
                "evidence_id": "e2",
                "actor_type": "user",
                "source_id": "source-1",
                "timestamp": "2026-04-25T10:02:00Z",
                "project_hint": "sessionmemory",
                "provenance": {"source_id": "source-1", "source_line_no": 12},
                "content_surfaces": [{"text": "I want the setup to infer defaults before asking me questions."}],
            },
        ]
        (self.evidence_dir / "logs" / "source-1.jsonl").write_text(
            "".join(json.dumps(record) + "\n" for record in records),
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def fake_llm(self, system_prompt: str, payload: dict[str, object], model: str) -> dict[str, object]:
        self.models_seen.append((str(payload.get("task") or ""), model))
        if "Extract candidate consumer working-profile facts" in str(payload.get("task")):
            return {
                "candidates": [
                    {
                        "section": "communication_preferences",
                        "trait": "status_update_style",
                        "summary": "Prefers concise progress updates.",
                        "confidence": "high",
                        "evidence_ids": ["e1"],
                        "project_hint": "sessionmemory",
                    },
                    {
                        "section": "workflow_preferences",
                        "trait": "default_agent_behavior",
                        "summary": "Prefers the agent to infer defaults before asking follow-up questions.",
                        "confidence": "high",
                        "evidence_ids": ["e2"],
                        "project_hint": "sessionmemory",
                    },
                ]
            }
        candidates = payload.get("candidates", [])
        communication_id = str(candidates[0]["candidate_id"]) if len(candidates) > 0 else ""
        workflow_id = str(candidates[1]["candidate_id"]) if len(candidates) > 1 else ""
        return {
            "summary": "Draft profile based on repeated collaboration requests.",
            "sections": {
                "communication_preferences": [
                    {
                        "trait": "status_update_style",
                        "preference": "Prefers concise progress updates.",
                        "confidence": "high",
                        "candidate_ids": [communication_id],
                    }
                ],
                "workflow_preferences": [
                    {
                        "trait": "default_agent_behavior",
                        "preference": "Prefers the agent to infer defaults before asking follow-up questions.",
                        "confidence": "high",
                        "candidate_ids": [workflow_id],
                    }
                ],
            },
        }

    def fake_llm_section_shape(self, system_prompt: str, payload: dict[str, object], model: str) -> dict[str, object]:
        if "Extract candidate consumer working-profile facts" in str(payload.get("task")):
            return {
                "communication_preferences": [
                    {
                        "trait": "status_update_style",
                        "preference": "Prefers concise progress updates.",
                        "confidence": "high",
                        "evidence": {"snippet_id": "e1"},
                    }
                ],
                "workflow_preferences": [
                    {
                        "trait": "default_agent_behavior",
                        "preference": "Prefers the agent to infer defaults before asking follow-up questions.",
                        "confidence": "high",
                        "evidence": {"snippet_id": "e2"},
                    }
                ],
            }
        return self.fake_llm(system_prompt, payload, model)

    def test_consumer_profile_builds_draft_profile(self) -> None:
        result = run_consumer_profile(
            evidence_dir=self.evidence_dir,
            memory_dir=self.memory_dir,
            state_dir=self.state_dir,
            audits_dir=self.audits_dir,
            policy_path=self.policy_path,
            model="stub-model",
            llm_client=self.fake_llm,
        )
        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        self.assertTrue(result.profile_path.exists())
        self.assertTrue(result.profile_json_path.exists())
        self.assertTrue((self.memory_dir / "_meta" / "consumer_style.json").exists())
        payload = json.loads(result.profile_json_path.read_text(encoding="utf-8"))
        self.assertEqual(payload["profile_status"], "draft")
        self.assertIn("communication_preferences", payload["sections"])
        style_payload = json.loads((self.memory_dir / "_meta" / "consumer_style.json").read_text(encoding="utf-8"))
        self.assertIn("tone", style_payload)
        self.assertIn("personalization_lines", style_payload)
        markdown = result.profile_path.read_text(encoding="utf-8")
        self.assertIn("memory_role: preference", markdown)
        self.assertNotIn("(`high`)", markdown)
        self.assertNotIn("Review-first", markdown)
        progress_payload = json.loads((self.state_dir / "consumer_profile_progress.json").read_text(encoding="utf-8"))
        self.assertEqual(progress_payload["stage"], "completed")
        self.assertTrue(progress_payload["success"])

    def test_consumer_profile_accepts_section_shaped_extractor_output(self) -> None:
        result = run_consumer_profile(
            evidence_dir=self.evidence_dir,
            memory_dir=self.memory_dir,
            state_dir=self.state_dir,
            audits_dir=self.audits_dir,
            policy_path=self.policy_path,
            model="stub-model",
            llm_client=self.fake_llm_section_shape,
        )
        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        self.assertGreater(result.report.candidate_count, 0)

    def test_consumer_profile_uses_phase_specific_models(self) -> None:
        result = run_consumer_profile(
            evidence_dir=self.evidence_dir,
            memory_dir=self.memory_dir,
            state_dir=self.state_dir,
            audits_dir=self.audits_dir,
            policy_path=self.policy_path,
            extraction_model="cheap-model",
            merge_model="strong-model",
            llm_client=self.fake_llm,
        )
        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        extract_models = [model for task, model in self.models_seen if "Extract candidate consumer working-profile facts" in task]
        merge_models = [model for task, model in self.models_seen if "Merge consumer working-profile candidates" in task]
        self.assertEqual(extract_models, ["cheap-model"])
        self.assertEqual(merge_models, ["strong-model"])


if __name__ == "__main__":
    unittest.main()
