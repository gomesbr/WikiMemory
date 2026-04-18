from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from uuid import uuid4

from wikimemory.bootstrap import run_bootstrap
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


class BootstrapTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="wikimemory-bootstrap-"))
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
        self.wiki_config_path = self.temp_dir / "wiki_config.json"
        self.bootstrap_config_path = self.temp_dir / "bootstrap_config.json"
        repo_root = Path(__file__).resolve().parents[1]
        self.schema_path = repo_root / "schema" / "normalization_catalog.json"
        self.taxonomy_path = repo_root / "config" / "classification_taxonomy.json"
        self.rules_path = repo_root / "config" / "extraction_rules.json"
        self.base_wiki_config_path = repo_root / "config" / "wiki_config.json"
        self.base_bootstrap_config_path = repo_root / "config" / "bootstrap_config.json"

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

    def write_bootstrap_config(
        self,
        *,
        prompt_version: int = 1,
        selection_version: int = 1,
        global_max_chars: int | None = None,
        project_max_chars: int | None = None,
        cross_project_max_chars: int | None = None,
    ) -> Path:
        payload = json.loads(self.base_bootstrap_config_path.read_text(encoding="utf-8"))
        payload["synthesis_prompt_version"] = prompt_version
        payload["selection_version"] = selection_version
        for domain in payload["domains"]:
            if domain["domain"] == "global" and global_max_chars is not None:
                domain["max_chars"] = global_max_chars
            if domain["kind"] == "project" and project_max_chars is not None:
                domain["max_chars"] = project_max_chars
            if domain["domain"] == "cross-project" and cross_project_max_chars is not None:
                domain["max_chars"] = cross_project_max_chars
        self.bootstrap_config_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return self.bootstrap_config_path

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

    def run_wiki_with_fake_llm(self, *, config_path: Path, source_ids: list[str] | None = None):
        with patch("wikimemory.wiki.call_openai_structured_json", side_effect=self.make_fake_wiki_synthesizer()):
            return run_wiki(
                config_path=config_path,
                state_dir=self.state_dir,
                extracted_dir=self.extracted_dir,
                wiki_dir=self.wiki_dir,
                audits_dir=self.audits_dir,
                source_ids=source_ids,
            )

    def run_bootstrap_with_fake_llm(
        self,
        *,
        config_path: Path,
        source_ids: list[str] | None = None,
        prefix: str = "Boot",
        invalid: bool = False,
        verbose: bool = False,
    ):
        side_effect = self.make_invalid_bootstrap_synthesizer() if invalid else self.make_fake_bootstrap_synthesizer(prefix, verbose=verbose)
        with patch("wikimemory.bootstrap.call_openai_structured_json", side_effect=side_effect):
            return run_bootstrap(
                config_path=config_path,
                state_dir=self.state_dir,
                extracted_dir=self.extracted_dir,
                wiki_dir=self.wiki_dir,
                bootstrap_dir=self.bootstrap_dir,
                audits_dir=self.audits_dir,
                source_ids=source_ids,
            )

    def make_fake_wiki_synthesizer(self):
        def fake_structured_json(*, config, system_prompt, user_prompt, schema):
            packet = json.loads(user_prompt)
            input_item_keys = [str(item) for item in packet.get("input_item_keys", [])]
            if not input_item_keys:
                return {"page_intro_claims": [], "section_summaries": []}
            return {
                "page_intro_claims": [
                    {
                        "text": f"Synth summary for {packet['title']}.",
                        "latent_type": "human_readable_synthesis_prose",
                        "confidence": "strong",
                        "supporting_item_ids": input_item_keys[: min(2, len(input_item_keys))],
                    }
                ],
                "section_summaries": [],
            }

        return fake_structured_json

    def make_fake_bootstrap_synthesizer(self, prefix: str, *, verbose: bool = False):
        def fake_structured_json(*, config, system_prompt, user_prompt, schema):
            packet = json.loads(user_prompt)
            sections = []
            for section in packet.get("sections", []):
                bullets = []
                for item in section.get("items", []):
                    text = f"{prefix} {section['title']}: {item['statement']}"
                    if verbose:
                        text += " " + ("extra context " * 12)
                    bullets.append(
                        {
                            "text": text,
                            "supporting_item_keys": [str(item["item_key"])],
                            "supporting_claim_ids": [],
                        }
                    )
                if not bullets and section.get("claims"):
                    claim = section["claims"][0]
                    bullets.append(
                        {
                            "text": f"{prefix} {section['title']}: {claim['text']}",
                            "supporting_item_keys": [str(item) for item in claim["supporting_item_ids"]],
                            "supporting_claim_ids": [str(claim["claim_id"])],
                        }
                    )
                sections.append({"section_id": str(section["section_id"]), "bullets": bullets})
            return {"sections": sections}

        return fake_structured_json

    def make_invalid_bootstrap_synthesizer(self):
        def invalid_structured_json(*, config, system_prompt, user_prompt, schema):
            packet = json.loads(user_prompt)
            section_id = str(packet["sections"][0]["section_id"]) if packet.get("sections") else "interaction_style"
            return {
                "sections": [
                    {
                        "section_id": section_id,
                        "bullets": [
                            {
                                "text": "Invalid bootstrap bullet.",
                                "supporting_item_keys": ["missing:item:key"],
                                "supporting_claim_ids": [],
                            }
                        ],
                    }
                ]
            }

        return invalid_structured_json

    def make_mixed_invalid_bootstrap_synthesizer(self):
        def mixed_structured_json(*, config, system_prompt, user_prompt, schema):
            packet = json.loads(user_prompt)
            sections = []
            for section in packet.get("sections", []):
                items = section.get("items", [])
                if not items:
                    sections.append({"section_id": str(section["section_id"]), "bullets": []})
                    continue
                valid_item_key = str(items[0]["item_key"])
                sections.append(
                    {
                        "section_id": str(section["section_id"]),
                        "bullets": [
                            {
                                "text": "Keep the valid part of a mixed-reference bullet.",
                                "supporting_item_keys": [valid_item_key, "missing:item:key"],
                                "supporting_claim_ids": ["missing:claim:id"],
                            },
                            {
                                "text": "Drop fully unsupported bullet.",
                                "supporting_item_keys": ["missing:item:key"],
                                "supporting_claim_ids": [],
                            },
                        ],
                    }
                )
            return {"sections": sections}

        return mixed_structured_json

    def make_duplicate_bootstrap_synthesizer(self):
        def duplicate_structured_json(*, config, system_prompt, user_prompt, schema):
            packet = json.loads(user_prompt)
            sections = []
            for section in packet.get("sections", []):
                items = section.get("items", [])
                if not items:
                    sections.append({"section_id": str(section["section_id"]), "bullets": []})
                    continue
                item_key = str(items[0]["item_key"])
                sections.append(
                    {
                        "section_id": str(section["section_id"]),
                        "bullets": [
                            {
                                "text": "Shared duplicate bullet.",
                                "supporting_item_keys": [item_key],
                                "supporting_claim_ids": [],
                            },
                            {
                                "text": "Shared duplicate bullet.",
                                "supporting_item_keys": [item_key],
                                "supporting_claim_ids": [],
                            },
                        ],
                    }
                )
            return {"sections": sections}

        return duplicate_structured_json

    def read_json(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def read_state_map(self) -> dict[str, dict]:
        payload = self.read_json(self.state_dir / "bootstrap_state.json")
        return {str(item["domain"]): item for item in payload["domains"]}

    def test_bootstrap_generates_files_and_manifests(self) -> None:
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
                        "message": "Communication preference: prefer concise answers. Workflow rule: validate before moving phases. Never refactor unrelated files.",
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
                        "message": "Current state: AI Trader broker integration is in progress. Decision: use Tradier first. Next step: implement rate limit handling. Open question: keep Alpaca as fallback? Update the AI Trader strategy.",
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
        self.assertTrue(self.run_wiki_with_fake_llm(config_path=self.write_wiki_config()).report.success)

        result = self.run_bootstrap_with_fake_llm(config_path=self.write_bootstrap_config())
        self.assertTrue(result.report.success)

        global_path = self.bootstrap_dir / "global.md"
        ai_trader_path = self.bootstrap_dir / "projects" / "ai-trader.md"
        cross_project_path = self.bootstrap_dir / "projects" / "cross-project.md"
        global_manifest = self.bootstrap_dir / "_meta" / "global.json"
        ai_trader_manifest = self.bootstrap_dir / "_meta" / "projects" / "ai-trader.json"
        self.assertTrue(global_path.exists())
        self.assertTrue(ai_trader_path.exists())
        self.assertTrue(cross_project_path.exists())
        self.assertTrue(global_manifest.exists())
        self.assertTrue(ai_trader_manifest.exists())

        manifest = self.read_json(ai_trader_manifest)
        self.assertTrue(manifest["bullets"])
        self.assertTrue(all(bullet["bullet_id"].startswith("B") for bullet in manifest["bullets"]))
        self.assertTrue(
            all(
                set(bullet["supporting_item_keys"]).issubset(set(manifest["packet"]["input_item_keys"]))
                for bullet in manifest["bullets"]
            )
        )

    def test_budget_enforcement_trims_low_priority_sections(self) -> None:
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
                        "message": "Communication preference: be concise. Always preserve provenance. Never refactor unrelated files. Workflow rule: validate before moving phases. Failure: previous bootstrap drifted.",
                    },
                }
            ],
        )
        self.write_source_config()
        self.run_until_extracted()
        self.assertTrue(self.run_wiki_with_fake_llm(config_path=self.write_wiki_config()).report.success)

        config_path = self.write_bootstrap_config(global_max_chars=240)
        result = self.run_bootstrap_with_fake_llm(config_path=config_path, verbose=True)
        self.assertTrue(result.report.success)

        markdown = (self.bootstrap_dir / "global.md").read_text(encoding="utf-8")
        self.assertLessEqual(len(markdown), 240)
        self.assertIn("## Interaction Style", markdown)
        self.assertNotIn("## Active Risks", markdown)

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
                    "payload": {"type": "user_message", "message": "Update the AI Trader strategy."},
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
                    "payload": {"type": "user_message", "message": "Open Brain architecture uses a memory pipeline component."},
                }
            ],
        )
        self.write_source_config()
        self.run_until_extracted()
        self.assertTrue(self.run_wiki_with_fake_llm(config_path=self.write_wiki_config(prompt_version=1)).report.success)

        first_result = self.run_bootstrap_with_fake_llm(config_path=self.write_bootstrap_config(prompt_version=1), prefix="Alpha")
        self.assertTrue(first_result.report.success)
        first_state = self.read_state_map()

        second_result = self.run_bootstrap_with_fake_llm(
            config_path=self.write_bootstrap_config(prompt_version=2),
            source_ids=[ai_trader_id],
            prefix="Beta",
        )
        self.assertTrue(second_result.report.success)
        second_state = self.read_state_map()

        self.assertNotEqual(first_state["ai-trader"]["last_run_id"], second_state["ai-trader"]["last_run_id"])
        self.assertEqual(first_state["open-brain"]["last_run_id"], second_state["open-brain"]["last_run_id"])

    def test_empty_domain_placeholder_is_stable(self) -> None:
        session_id = str(uuid4())
        make_source_file(
            self.source_path(session_id, "ai-trader"),
            session_id,
            cwd="C:\\repos\\ai-trader",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:06:00.000Z",
                    "type": "event_msg",
                    "payload": {"type": "user_message", "message": "Update the AI Trader strategy."},
                }
            ],
        )
        self.write_source_config()
        self.run_until_extracted()
        self.assertTrue(self.run_wiki_with_fake_llm(config_path=self.write_wiki_config()).report.success)

        result = self.run_bootstrap_with_fake_llm(config_path=self.write_bootstrap_config())
        self.assertTrue(result.report.success)

        cross_project_markdown = (self.bootstrap_dir / "projects" / "cross-project.md").read_text(encoding="utf-8")
        self.assertIn("No high-signal bootstrap memory selected yet.", cross_project_markdown)

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
                        "message": "Communication preference: prefer concise answers. Workflow rule: validate before moving phases.",
                    },
                }
            ],
        )
        self.write_source_config()
        self.run_until_extracted()
        self.assertTrue(self.run_wiki_with_fake_llm(config_path=self.write_wiki_config()).report.success)

        first_result = self.run_bootstrap_with_fake_llm(config_path=self.write_bootstrap_config(prompt_version=1))
        self.assertTrue(first_result.report.success)
        state_before = (self.state_dir / "bootstrap_state.json").read_text(encoding="utf-8")
        markdown_before = (self.bootstrap_dir / "global.md").read_text(encoding="utf-8")

        failed_result = self.run_bootstrap_with_fake_llm(
            config_path=self.write_bootstrap_config(prompt_version=2),
            invalid=True,
        )
        self.assertFalse(failed_result.report.success)
        self.assertEqual((self.state_dir / "bootstrap_state.json").read_text(encoding="utf-8"), state_before)
        self.assertEqual((self.bootstrap_dir / "global.md").read_text(encoding="utf-8"), markdown_before)

    def test_mixed_invalid_synthesis_refs_are_filtered(self) -> None:
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
                        "message": "Communication preference: prefer concise answers. Workflow rule: validate before moving phases.",
                    },
                }
            ],
        )
        self.write_source_config()
        self.run_until_extracted()
        self.assertTrue(self.run_wiki_with_fake_llm(config_path=self.write_wiki_config()).report.success)

        with patch("wikimemory.bootstrap.call_openai_structured_json", side_effect=self.make_mixed_invalid_bootstrap_synthesizer()):
            result = run_bootstrap(
                config_path=self.write_bootstrap_config(),
                state_dir=self.state_dir,
                extracted_dir=self.extracted_dir,
                wiki_dir=self.wiki_dir,
                bootstrap_dir=self.bootstrap_dir,
                audits_dir=self.audits_dir,
            )

        self.assertTrue(result.report.success, result.report.fatal_error_summary)
        markdown = (self.bootstrap_dir / "global.md").read_text(encoding="utf-8")
        self.assertIn("Keep the valid part", markdown)
        self.assertNotIn("Drop fully unsupported", markdown)

    def test_duplicate_bullets_are_deduped(self) -> None:
        session_id = str(uuid4())
        make_source_file(
            self.source_path(session_id, "global"),
            session_id,
            cwd="C:\\repos\\shared-rag",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:08:00.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "Communication preference: be concise. Workflow rule: preserve provenance.",
                    },
                }
            ],
        )
        self.write_source_config()
        self.run_until_extracted()
        self.run_wiki_with_fake_llm(config_path=self.write_wiki_config())

        with patch("wikimemory.bootstrap.call_openai_structured_json", side_effect=self.make_duplicate_bootstrap_synthesizer()):
            result = run_bootstrap(
                config_path=self.write_bootstrap_config(),
                state_dir=self.state_dir,
                extracted_dir=self.extracted_dir,
                wiki_dir=self.wiki_dir,
                bootstrap_dir=self.bootstrap_dir,
                audits_dir=self.audits_dir,
            )

        self.assertTrue(result.report.success)
        markdown = (self.bootstrap_dir / "global.md").read_text(encoding="utf-8")
        self.assertEqual(markdown.count("Shared duplicate bullet."), 1)
