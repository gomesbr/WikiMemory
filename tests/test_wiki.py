from __future__ import annotations

import json
import re
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from uuid import uuid4

from wikimemory.classification import run_classification
from wikimemory.discovery import run_discovery
from wikimemory.extraction import run_extraction
from wikimemory.normalization import run_normalization
from wikimemory.segmentation import run_segmentation
from wikimemory.wiki import run_wiki


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


class WikiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="wikimemory-wiki-"))
        self.root = self.temp_dir / "sessions"
        self.state_dir = self.temp_dir / "state"
        self.normalized_dir = self.temp_dir / "normalized"
        self.segmented_dir = self.temp_dir / "segmented"
        self.classified_dir = self.temp_dir / "classified"
        self.extracted_dir = self.temp_dir / "extracted"
        self.wiki_dir = self.temp_dir / "wiki"
        self.audits_dir = self.temp_dir / "audits"
        self.source_config_path = self.temp_dir / "source_roots.json"
        self.wiki_config_path = self.temp_dir / "wiki_config.json"
        repo_root = Path(__file__).resolve().parents[1]
        self.schema_path = repo_root / "schema" / "normalization_catalog.json"
        self.taxonomy_path = repo_root / "config" / "classification_taxonomy.json"
        self.rules_path = repo_root / "config" / "extraction_rules.json"
        self.base_wiki_config_path = repo_root / "config" / "wiki_config.json"

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def write_source_config(self) -> None:
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
        self.source_config_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def write_wiki_config(self, prompt_version: int = 1) -> Path:
        payload = json.loads(self.base_wiki_config_path.read_text(encoding="utf-8"))
        payload["synthesis_prompt_version"] = prompt_version
        self.wiki_config_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return self.wiki_config_path

    def source_path(self, session_id: str, *subdirs: str) -> Path:
        base = self.root / "2026" / "04" / "12"
        for part in subdirs:
            base /= part
        return base / f"rollout-2026-04-12T20-59-14-{session_id}.jsonl"

    def run_until_extracted(self, source_ids: list[str] | None = None) -> None:
        run_discovery(self.source_config_path, self.state_dir)
        run_normalization(
            config_path=self.source_config_path,
            state_dir=self.state_dir,
            schema_path=self.schema_path,
            normalized_dir=self.normalized_dir,
            audits_dir=self.audits_dir,
        )
        run_segmentation(
            state_dir=self.state_dir,
            normalized_dir=self.normalized_dir,
            segmented_dir=self.segmented_dir,
        )
        run_classification(
            taxonomy_path=self.taxonomy_path,
            state_dir=self.state_dir,
            normalized_dir=self.normalized_dir,
            segmented_dir=self.segmented_dir,
            classified_dir=self.classified_dir,
            audits_dir=self.audits_dir,
        )
        run_extraction(
            rules_path=self.rules_path,
            state_dir=self.state_dir,
            normalized_dir=self.normalized_dir,
            classified_dir=self.classified_dir,
            extracted_dir=self.extracted_dir,
            audits_dir=self.audits_dir,
            source_ids=source_ids,
        )

    def run_wiki_with_fake_llm(
        self,
        *,
        config_path: Path,
        source_ids: list[str] | None = None,
        prefix: str = "Synth",
        invalid: bool = False,
    ):
        side_effect = self.make_invalid_synthesizer() if invalid else self.make_fake_synthesizer(prefix)
        with patch("wikimemory.wiki.call_openai_structured_json", side_effect=side_effect):
            return run_wiki(
                config_path=config_path,
                state_dir=self.state_dir,
                extracted_dir=self.extracted_dir,
                wiki_dir=self.wiki_dir,
                audits_dir=self.audits_dir,
                source_ids=source_ids,
            )

    def make_fake_synthesizer(self, prefix: str):
        def fake_structured_json(*, config, system_prompt, user_prompt, schema):
            packet = json.loads(user_prompt)
            input_item_keys = [str(item) for item in packet.get("input_item_keys", [])]
            if not input_item_keys:
                return {
                    "page_intro_claims": [],
                    "section_summaries": [],
                }

            first_section = next((section for section in packet.get("deterministic_sections", []) if section.get("items")), None)
            first_item = first_section["items"][0] if first_section else None
            intro_text = (
                f"{prefix}: {first_item['statement']}"
                if first_item is not None
                else f"{prefix} summary for {packet['title']}."
            )
            bucket = str(packet.get("bucket", ""))
            page_type = str(packet.get("page_type", ""))
            intro_claim = {
                "text": intro_text,
                "latent_type": self.latent_type_for_page(bucket, page_type),
                "confidence": "strong",
                "supporting_item_ids": input_item_keys[: min(2, len(input_item_keys))],
            }
            section_summaries = []
            for section in packet.get("deterministic_sections", []):
                section_items = section.get("items", [])
                if not section_items:
                    continue
                supporting_item_ids = [
                    str(item["support_id"]) for item in section_items[: min(2, len(section_items))]
                ]
                section_summaries.append(
                    {
                        "section_id": str(section["section_id"]),
                        "claims": [
                            {
                                "text": f"{prefix}: {section_items[0]['statement']}",
                                "latent_type": self.latent_type_for_section(str(section["section_id"])),
                                "confidence": "strong",
                                "supporting_item_ids": supporting_item_ids,
                            }
                        ],
                    }
                )
            return {
                "page_intro_claims": [intro_claim],
                "section_summaries": section_summaries,
            }

        return fake_structured_json

    def make_index_alias_synthesizer(self, prefix: str):
        def fake_structured_json(*, config, system_prompt, user_prompt, schema):
            packet = json.loads(user_prompt)
            input_item_keys = [str(item) for item in packet.get("input_item_keys", [])]
            if not input_item_keys:
                return {
                    "page_intro_claims": [],
                    "section_summaries": [],
                }

            if str(packet.get("page_type")) != "domain_index":
                return self.make_fake_synthesizer(prefix)(
                    config=config,
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    schema=schema,
                )

            intro_claims = []
            section_summaries = []
            for section in packet.get("deterministic_sections", []):
                if not section.get("items"):
                    continue
                allowed_ids = [str(item) for item in section.get("allowed_support_ids", [])]
                bucket_page_id = next((item for item in allowed_ids if item.startswith("SEC_")), allowed_ids[0])
                supporting_item = section["items"][0]
                intro_claims.append(
                    {
                        "text": f"{prefix}: {supporting_item['statement']}",
                        "latent_type": "segment_theme_consolidation",
                        "confidence": "strong",
                        "supporting_item_ids": [bucket_page_id],
                    }
                )
                section_summaries.append(
                    {
                        "section_id": str(section["section_id"]),
                        "claims": [
                            {
                                "text": f"{prefix}: {supporting_item['statement']}",
                                "latent_type": self.latent_type_for_section(str(section["section_id"])),
                                "confidence": "strong",
                                "supporting_item_ids": [bucket_page_id],
                            }
                        ],
                    }
                )
            return {
                "page_intro_claims": intro_claims[:1],
                "section_summaries": section_summaries,
            }

        return fake_structured_json

    def make_invalid_synthesizer(self):
        def invalid_structured_json(*, config, system_prompt, user_prompt, schema):
            packet = json.loads(user_prompt)
            input_item_keys = [str(item) for item in packet.get("input_item_keys", [])]
            if not input_item_keys:
                return {
                    "page_intro_claims": [],
                    "section_summaries": [],
                }
            return {
                "page_intro_claims": [
                    {
                        "text": "Invalid synthesized claim.",
                        "latent_type": "segment_theme_consolidation",
                        "confidence": "strong",
                        "supporting_item_ids": ["missing:item:key"],
                    }
                ],
                "section_summaries": [],
            }

        return invalid_structured_json

    def latent_type_for_page(self, bucket: str, page_type: str) -> str:
        if page_type == "domain_index":
            return "segment_theme_consolidation"
        mapping = {
            "communication-preferences": "communication_preferences",
            "workflow-rules": "workflow_norms",
            "architecture": "architecture_synthesis",
            "code-map": "codebase_map_abstractions",
            "current-state": "current_state_synthesis",
            "tasks": "implicit_next_steps",
            "outcomes": "temporal_evolution",
            "failures": "recurring_failure_patterns",
            "decisions": "decision_synthesis",
            "next-steps": "implicit_next_steps",
            "open-questions": "partially_explicit_open_questions",
        }
        return mapping.get(bucket, "human_readable_synthesis_prose")

    def latent_type_for_section(self, section_id: str) -> str:
        mapping = {
            "communication-preferences": "communication_preferences",
            "workflow-rules": "workflow_norms",
            "communication_preference": "communication_preferences",
            "workflow_rule": "workflow_norms",
            "do_rule": "implicit_dos_and_donts",
            "dont_rule": "implicit_dos_and_donts",
            "architecture_note": "architecture_synthesis",
            "code_location": "codebase_map_abstractions",
            "current_state": "current_state_synthesis",
            "task_request": "implicit_next_steps",
            "outcome": "temporal_evolution",
            "failure": "recurring_failure_patterns",
            "decision": "decision_synthesis",
            "next_step": "implicit_next_steps",
            "open_question": "partially_explicit_open_questions",
        }
        return mapping.get(section_id, "segment_theme_consolidation")

    def read_json(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def read_jsonl(self, path: Path) -> list[dict]:
        return [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    def read_state_map(self) -> dict[str, dict]:
        payload = self.read_json(self.state_dir / "wiki_state.json")
        return {str(page["page_id"]): page for page in payload["pages"]}

    def extract_summary_block(self, markdown: str) -> str:
        match = re.search(r"## Summary\n(.*?)(?:\n## |\Z)", markdown, re.DOTALL)
        self.assertIsNotNone(match)
        return match.group(1).strip()

    def extract_canonical_items_block(self, markdown: str) -> str:
        match = re.search(r"### Canonical Items\n(.*?)(?:\n## Sources|\Z)", markdown, re.DOTALL)
        self.assertIsNotNone(match)
        return match.group(1).strip()

    def test_wiki_generates_pages_manifests_and_obsidian_output(self) -> None:
        global_id = str(uuid4())
        ai_trader_id = str(uuid4())
        cross_project_id = str(uuid4())
        make_source_file(
            self.source_path(global_id, "global"),
            global_id,
            cwd="C:\\repos\\shared-rag",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:00:00.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "Communication preference: prefer concise answers. Workflow rule: do not refactor unrelated files.",
                    },
                }
            ],
        )
        make_source_file(
            self.source_path(ai_trader_id, "ai-trader"),
            ai_trader_id,
            cwd="C:\\repos\\ai-trader",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:01:00.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "Update the AI Trader strategy.",
                    },
                }
            ],
        )
        make_source_file(
            self.source_path(cross_project_id, "shared"),
            cross_project_id,
            cwd="C:\\repos\\shared-rag",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:02:00.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "Connect Open Brain memory system with AI Scientist optimization loop.",
                    },
                }
            ],
        )
        self.write_source_config()
        self.run_until_extracted()

        result = self.run_wiki_with_fake_llm(config_path=self.write_wiki_config())
        self.assertTrue(result.report.success)

        global_index_path = self.wiki_dir / "global" / "index.md"
        ai_trader_tasks_path = self.wiki_dir / "projects" / "ai-trader" / "tasks.md"
        cross_project_index_path = self.wiki_dir / "projects" / "cross-project" / "index.md"
        self.assertTrue(global_index_path.exists())
        self.assertTrue(ai_trader_tasks_path.exists())
        self.assertTrue(cross_project_index_path.exists())

        global_markdown = global_index_path.read_text(encoding="utf-8")
        self.assertTrue(global_markdown.startswith("---\n"))
        self.assertIn("[[", global_markdown)
        self.assertIn("## Sources", global_markdown)

        global_manifest = self.read_json(self.wiki_dir / "_meta" / "pages" / "global" / "index.json")
        self.assertEqual(global_manifest["page_id"], "global/index")
        self.assertTrue(global_manifest["input_item_keys"])
        self.assertTrue(global_manifest["synthesized_claims"])
        input_item_keys = set(global_manifest["input_item_keys"])
        for claim in global_manifest["synthesized_claims"]:
            self.assertTrue(set(claim["supporting_item_ids"]).issubset(input_item_keys))
            self.assertTrue(claim["provenance_refs"])

    def test_empty_bucket_pages_are_not_rendered(self) -> None:
        session_id = str(uuid4())
        make_source_file(
            self.source_path(session_id, "global"),
            session_id,
            cwd="C:\\repos\\shared-rag",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:00:00.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "Communication preference: prefer concise answers.",
                    },
                }
            ],
        )
        self.write_source_config()
        self.run_until_extracted()

        result = self.run_wiki_with_fake_llm(config_path=self.write_wiki_config())
        self.assertTrue(result.report.success)
        self.assertTrue((self.wiki_dir / "global" / "communication-preferences.md").exists())
        self.assertFalse((self.wiki_dir / "global" / "architecture.md").exists())
        self.assertFalse((self.wiki_dir / "unclassified" / "index.md").exists())

    def test_synthesized_claims_reference_manifest_backed_items(self) -> None:
        session_id = str(uuid4())
        make_source_file(
            self.source_path(session_id, "global"),
            session_id,
            cwd="C:\\repos\\shared-rag",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:03:00.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "Communication preference: prefer concise answers. Workflow rule: be concise.",
                    },
                }
            ],
        )
        self.write_source_config()
        self.run_until_extracted()

        result = self.run_wiki_with_fake_llm(config_path=self.write_wiki_config(), prefix="Latent")
        self.assertTrue(result.report.success)

        page_path = self.wiki_dir / "global" / "communication-preferences.md"
        manifest_path = self.wiki_dir / "_meta" / "pages" / "global" / "communication-preferences.json"
        markdown = page_path.read_text(encoding="utf-8")
        manifest = self.read_json(manifest_path)

        self.assertIn("[latent:", markdown)
        self.assertIn("Latent:", markdown)
        input_item_keys = set(manifest["input_item_keys"])
        for claim in manifest["synthesized_claims"]:
            self.assertTrue(set(claim["supporting_item_ids"]).issubset(input_item_keys))
            self.assertTrue(claim["provenance_refs"])

    def test_index_page_can_resolve_bucket_page_support_aliases(self) -> None:
        session_id = str(uuid4())
        make_source_file(
            self.source_path(session_id, "global"),
            session_id,
            cwd="C:\\repos\\shared-rag",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:03:00.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "Communication preference: prefer concise answers. Workflow rule: be concise.",
                    },
                }
            ],
        )
        self.write_source_config()
        self.run_until_extracted()

        with patch("wikimemory.wiki.call_openai_structured_json", side_effect=self.make_index_alias_synthesizer("Alias")):
            result = run_wiki(
                config_path=self.write_wiki_config(),
                state_dir=self.state_dir,
                extracted_dir=self.extracted_dir,
                wiki_dir=self.wiki_dir,
                audits_dir=self.audits_dir,
            )
        self.assertTrue(result.report.success)

        manifest = self.read_json(self.wiki_dir / "_meta" / "pages" / "global" / "index.json")
        input_item_keys = set(manifest["input_item_keys"])
        self.assertTrue(manifest["synthesized_claims"])
        for claim in manifest["synthesized_claims"]:
            self.assertTrue(set(claim["supporting_item_ids"]).issubset(input_item_keys))

    def test_deterministic_item_block_stays_stable_when_synthesis_changes(self) -> None:
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
                        "message": "Update the AI Trader strategy.",
                    },
                }
            ],
        )
        self.write_source_config()
        self.run_until_extracted()

        first_config = self.write_wiki_config(prompt_version=1)
        first_result = self.run_wiki_with_fake_llm(config_path=first_config, prefix="Alpha")
        self.assertTrue(first_result.report.success)

        page_path = self.wiki_dir / "projects" / "ai-trader" / "tasks.md"
        first_markdown = page_path.read_text(encoding="utf-8")
        first_summary = self.extract_summary_block(first_markdown)
        first_items = self.extract_canonical_items_block(first_markdown)

        second_config = self.write_wiki_config(prompt_version=2)
        second_result = self.run_wiki_with_fake_llm(config_path=second_config, prefix="Beta")
        self.assertTrue(second_result.report.success)

        second_markdown = page_path.read_text(encoding="utf-8")
        second_summary = self.extract_summary_block(second_markdown)
        second_items = self.extract_canonical_items_block(second_markdown)

        self.assertEqual(first_items, second_items)
        self.assertNotEqual(first_summary, second_summary)

    def test_source_scoped_rebuild_only_updates_touched_domains(self) -> None:
        ai_trader_id = str(uuid4())
        open_brain_id = str(uuid4())
        make_source_file(
            self.source_path(ai_trader_id, "ai-trader"),
            ai_trader_id,
            cwd="C:\\repos\\ai-trader",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:05:00.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "Update the AI Trader strategy.",
                    },
                }
            ],
        )
        make_source_file(
            self.source_path(open_brain_id, "open-brain"),
            open_brain_id,
            cwd="C:\\repos\\wikimemory",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:05:30.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "Open Brain architecture uses a memory pipeline component.",
                    },
                }
            ],
        )
        self.write_source_config()
        self.run_until_extracted()

        first_config = self.write_wiki_config(prompt_version=1)
        first_result = self.run_wiki_with_fake_llm(config_path=first_config, prefix="Alpha")
        self.assertTrue(first_result.report.success)
        first_state = self.read_state_map()

        second_config = self.write_wiki_config(prompt_version=2)
        second_result = self.run_wiki_with_fake_llm(
            config_path=second_config,
            source_ids=[ai_trader_id],
            prefix="Beta",
        )
        self.assertTrue(second_result.report.success)
        second_state = self.read_state_map()

        self.assertNotEqual(
            first_state["projects/ai-trader/index"]["last_run_id"],
            second_state["projects/ai-trader/index"]["last_run_id"],
        )
        self.assertNotEqual(
            first_state["projects/ai-trader/tasks"]["last_run_id"],
            second_state["projects/ai-trader/tasks"]["last_run_id"],
        )
        self.assertEqual(
            first_state["projects/open-brain/index"]["last_run_id"],
            second_state["projects/open-brain/index"]["last_run_id"],
        )
        self.assertEqual(
            first_state["projects/open-brain/architecture"]["last_run_id"],
            second_state["projects/open-brain/architecture"]["last_run_id"],
        )

    def test_conflicts_and_inferred_items_render_inline_and_log_notices(self) -> None:
        ai_trader_id = str(uuid4())
        open_brain_id = str(uuid4())
        make_source_file(
            self.source_path(ai_trader_id, "ai-trader"),
            ai_trader_id,
            cwd="C:\\repos\\ai-trader",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:06:00.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "Update the AI Trader strategy.",
                    },
                }
            ],
        )
        make_source_file(
            self.source_path(open_brain_id, "open-brain"),
            open_brain_id,
            cwd="C:\\repos\\wikimemory",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:06:30.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "Current state: storage backend = sqlite. Current state: storage backend = postgres.",
                    },
                }
            ],
        )
        self.write_source_config()
        self.run_until_extracted()

        result = self.run_wiki_with_fake_llm(config_path=self.write_wiki_config())
        self.assertTrue(result.report.success)

        ai_trader_markdown = (self.wiki_dir / "projects" / "ai-trader" / "tasks.md").read_text(encoding="utf-8")
        open_brain_markdown = (self.wiki_dir / "projects" / "open-brain" / "current-state.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("[confidence: inferred]", ai_trader_markdown)
        self.assertIn("[conflict]", open_brain_markdown)

        notices = self.read_jsonl(self.audits_dir / "wiki_notices.jsonl")
        self.assertTrue(
            any(
                notice["page_id"] == "projects/ai-trader/tasks"
                and notice["notice_type"] == "low_confidence_items"
                for notice in notices
            )
        )
        self.assertTrue(
            any(
                notice["page_id"] == "projects/open-brain/current-state"
                and notice["notice_type"] == "conflict_items"
                for notice in notices
            )
        )

    def test_invalid_synthesis_output_preserves_prior_state(self) -> None:
        session_id = str(uuid4())
        make_source_file(
            self.source_path(session_id, "global"),
            session_id,
            cwd="C:\\repos\\shared-rag",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:07:00.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "Workflow rule: be concise.",
                    },
                }
            ],
        )
        self.write_source_config()
        self.run_until_extracted()

        first_result = self.run_wiki_with_fake_llm(config_path=self.write_wiki_config(prompt_version=1), prefix="Good")
        self.assertTrue(first_result.report.success)

        state_before = (self.state_dir / "wiki_state.json").read_text(encoding="utf-8")
        page_path = self.wiki_dir / "global" / "workflow-rules.md"
        page_before = page_path.read_text(encoding="utf-8")

        failed_result = self.run_wiki_with_fake_llm(
            config_path=self.write_wiki_config(prompt_version=2),
            invalid=True,
        )
        self.assertFalse(failed_result.report.success)
        self.assertEqual((self.state_dir / "wiki_state.json").read_text(encoding="utf-8"), state_before)
        self.assertEqual(page_path.read_text(encoding="utf-8"), page_before)
