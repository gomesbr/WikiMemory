from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from uuid import uuid4

from sessionmemory.audit import run_audit
from sessionmemory.bootstrap import run_bootstrap
from sessionmemory.classification import run_classification
from sessionmemory.discovery import run_discovery
from sessionmemory.extraction import run_extraction
from sessionmemory.normalization import run_normalization
from sessionmemory.segmentation import run_segmentation
from sessionmemory.wiki import run_wiki


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


class AuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="sessionmemory-audit-"))
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
        self.audit_config_path = self.temp_dir / "audit_config.json"
        repo_root = Path(__file__).resolve().parents[1]
        self.schema_path = repo_root / "schema" / "normalization_catalog.json"
        self.taxonomy_path = repo_root / "config" / "classification_taxonomy.json"
        self.rules_path = repo_root / "config" / "extraction_rules.json"
        self.base_wiki_config_path = repo_root / "config" / "wiki_config.json"
        self.base_bootstrap_config_path = repo_root / "config" / "bootstrap_config.json"
        self.base_audit_config_path = repo_root / "config" / "audit_config.json"

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

    def write_wiki_config(self) -> Path:
        payload = json.loads(self.base_wiki_config_path.read_text(encoding="utf-8"))
        self.wiki_config_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return self.wiki_config_path

    def write_bootstrap_config(self) -> Path:
        payload = json.loads(self.base_bootstrap_config_path.read_text(encoding="utf-8"))
        self.bootstrap_config_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return self.bootstrap_config_path

    def write_audit_config(self) -> Path:
        payload = json.loads(self.base_audit_config_path.read_text(encoding="utf-8"))
        payload["bootstrap_config_path"] = str(self.bootstrap_config_path)
        self.audit_config_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return self.audit_config_path

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

    def run_wiki_with_fake_llm(self) -> None:
        with patch("sessionmemory.wiki.call_openai_structured_json", side_effect=self.make_fake_wiki_synthesizer()):
            result = run_wiki(
                config_path=self.write_wiki_config(),
                state_dir=self.state_dir,
                extracted_dir=self.extracted_dir,
                wiki_dir=self.wiki_dir,
                audits_dir=self.audits_dir,
            )
        self.assertTrue(result.report.success)

    def run_bootstrap_with_fake_llm(self) -> None:
        with patch("sessionmemory.bootstrap.call_openai_structured_json", side_effect=self.make_fake_bootstrap_synthesizer()):
            result = run_bootstrap(
                config_path=self.write_bootstrap_config(),
                state_dir=self.state_dir,
                extracted_dir=self.extracted_dir,
                wiki_dir=self.wiki_dir,
                bootstrap_dir=self.bootstrap_dir,
                audits_dir=self.audits_dir,
            )
        self.assertTrue(result.report.success)

    def run_full_pipeline(self, source_ids: list[str] | None = None) -> None:
        self.run_until_extracted(source_ids=source_ids)
        self.run_wiki_with_fake_llm()
        self.run_bootstrap_with_fake_llm()

    def run_audit(self, source_ids: list[str] | None = None):
        return run_audit(
            config_path=self.write_audit_config(),
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

    def read_jsonl(self, path: Path) -> list[dict]:
        return [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    def read_audit_state_map(self) -> dict[str, dict]:
        payload = self.read_json(self.state_dir / "audit_state.json")
        return {f"{item['scope_kind']}:{item['scope_key']}": item for item in payload["targets"]}

    def test_stale_warnings_do_not_fail_audit(self) -> None:
        session_id = str(uuid4())
        make_source_file(
            self.source_path(session_id, "global"),
            session_id,
            cwd="C:\\repos\\shared-rag",
            session_timestamp="2020-01-01T00:00:00.000Z",
            extra_lines=[
                {
                    "timestamp": "2020-01-01T00:00:00.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "Next step: refresh the bootstrap memory.",
                    },
                }
            ],
        )
        self.write_source_config()
        self.run_full_pipeline()

        result = self.run_audit()
        self.assertTrue(result.report.success)
        self.assertEqual(result.report.error_finding_count, 0)
        stale_findings = self.read_jsonl(self.audits_dir / "stale_items.jsonl")
        self.assertTrue(any(finding["check_type"] == "stale_active_item" for finding in stale_findings))

    def test_conflicting_active_current_state_emits_error(self) -> None:
        session_id = str(uuid4())
        make_source_file(
            self.source_path(session_id, "open-brain"),
            session_id,
            cwd="C:\\repos\\sessionmemory",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:00:00.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "Open Brain current state: storage backend = sqlite. Open Brain current state: storage backend = postgres.",
                    },
                }
            ],
        )
        self.write_source_config()
        self.run_full_pipeline()

        result = self.run_audit()
        self.assertTrue(result.report.success)
        self.assertGreater(result.report.error_finding_count, 0)
        contradiction_findings = self.read_jsonl(self.audits_dir / "contradictions.jsonl")
        self.assertTrue(any(finding["severity"] == "error" for finding in contradiction_findings))

    def test_superseded_conflict_does_not_error(self) -> None:
        session_id = str(uuid4())
        make_source_file(
            self.source_path(session_id, "open-brain"),
            session_id,
            cwd="C:\\repos\\sessionmemory",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:00:00.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": "Open Brain current state: storage backend = sqlite. Open Brain current state: storage backend = postgres.",
                    },
                }
            ],
        )
        self.write_source_config()
        self.run_full_pipeline()

        items_path = self.extracted_dir / "domains" / "open-brain" / "items.jsonl"
        items = self.read_jsonl(items_path)
        current_state_items = [item for item in items if item["item_type"] == "current_state"]
        self.assertGreaterEqual(len(current_state_items), 2)
        current_state_items[0]["temporal_status"] = "superseded"
        current_state_items[0]["last_seen_at"] = "2026-04-11T00:00:00.000Z"
        items_path.write_text("".join(json.dumps(item, sort_keys=True) + "\n" for item in items), encoding="utf-8")

        result = self.run_audit()
        self.assertTrue(result.report.success)
        contradiction_findings = self.read_jsonl(self.audits_dir / "contradictions.jsonl")
        self.assertFalse(any(finding["severity"] == "error" for finding in contradiction_findings))

    def test_conflicting_next_steps_warn_but_do_not_error(self) -> None:
        session_id = str(uuid4())
        make_source_file(
            self.source_path(session_id, "open-brain"),
            session_id,
            cwd="C:\\repos\\sessionmemory",
            extra_lines=[
                {
                    "timestamp": "2026-04-12T21:00:00.000Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "user_message",
                        "message": (
                            "Next step: update src/ui/server.ts to add query caching. "
                            "Next step: update src/ui/server.ts to simplify route wiring."
                        ),
                    },
                }
            ],
        )
        self.write_source_config()
        self.run_full_pipeline()

        result = self.run_audit()
        self.assertTrue(result.report.success)
        contradiction_findings = self.read_jsonl(self.audits_dir / "contradictions.jsonl")
        self.assertTrue(any(finding["severity"] == "warning" for finding in contradiction_findings))
        self.assertFalse(any(finding["severity"] == "error" for finding in contradiction_findings))

    def test_provenance_gap_and_duplicate_bootstrap_bullet_are_reported(self) -> None:
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
                        "message": "Current state: AI Trader broker integration is in progress. Next step: implement rate limit handling.",
                    },
                }
            ],
        )
        self.write_source_config()
        self.run_full_pipeline()

        page_manifest_path = self.wiki_dir / "_meta" / "pages" / "projects" / "ai-trader" / "current-state.json"
        page_manifest = self.read_json(page_manifest_path)
        page_manifest["synthesized_claims"][0]["supporting_item_ids"] = ["missing:item:key"]
        page_manifest_path.write_text(json.dumps(page_manifest, indent=2), encoding="utf-8")

        bootstrap_manifest_path = self.bootstrap_dir / "_meta" / "projects" / "ai-trader.json"
        bootstrap_manifest = self.read_json(bootstrap_manifest_path)
        first_bullet = dict(bootstrap_manifest["bullets"][0])
        duplicate_bullet = dict(first_bullet)
        duplicate_bullet["bullet_id"] = "B99"
        bootstrap_manifest["bullets"].append(duplicate_bullet)
        bootstrap_manifest_path.write_text(json.dumps(bootstrap_manifest, indent=2), encoding="utf-8")

        result = self.run_audit()
        self.assertTrue(result.report.success)
        self.assertGreater(result.report.error_finding_count, 0)
        provenance_findings = self.read_jsonl(self.audits_dir / "provenance_gaps.jsonl")
        duplicate_findings = self.read_jsonl(self.audits_dir / "duplicates.jsonl")
        self.assertTrue(any(finding["scope_kind"] == "page" for finding in provenance_findings))
        self.assertTrue(any(finding["scope_kind"] == "bootstrap_domain" for finding in duplicate_findings))

    def test_transient_rule_item_is_reported(self) -> None:
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
                        "message": "Workflow rule: do not refactor unrelated files.",
                    },
                }
            ],
        )
        self.write_source_config()
        self.run_full_pipeline()

        items_path = self.extracted_dir / "domains" / "global" / "items.jsonl"
        items = self.read_jsonl(items_path)
        workflow_item = next(item for item in items if item["item_type"] in {"workflow_rule", "dont_rule"})
        workflow_item["wiki_eligible"] = True
        workflow_item["promotion_blockers"] = ["one_off_imperative"]
        items_path.write_text("".join(json.dumps(item, sort_keys=True) + "\n" for item in items), encoding="utf-8")

        result = self.run_audit()
        self.assertTrue(result.report.success)
        wiki_quality_findings = self.read_jsonl(self.audits_dir / "wiki_quality.jsonl")
        self.assertTrue(any(finding["check_type"] == "transient_rule_item" for finding in wiki_quality_findings))

    def test_scoped_audit_updates_only_touched_targets_and_detects_drift(self) -> None:
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
        self.write_source_config()
        self.run_full_pipeline()

        first_result = self.run_audit()
        self.assertTrue(first_result.report.success)
        first_state = self.read_audit_state_map()

        items_path = self.extracted_dir / "domains" / "ai-trader" / "items.jsonl"
        items = self.read_jsonl(items_path)
        items.append(
            {
                **items[0],
                "item_key": "ai-trader:next_step:manualextra",
                "item_type": "next_step",
                "statement": "Implement rate limit handling next.",
                "normalized_signature": "implement rate limit handling next",
                "subject_key": "rate-limit-handling",
                "temporal_status": "active",
                "confidence": "strong",
                "recurrence_count": 1,
                "provenance_refs": [{"source_id": ai_trader_id, "segment_id": "manual"}],
                "supporting_source_ids": [ai_trader_id],
                "primary_domain": "ai-trader",
                "target_page_key": "next-steps",
            }
        )
        items_path.write_text("".join(json.dumps(item, sort_keys=True) + "\n" for item in items), encoding="utf-8")

        second_result = self.run_audit(source_ids=[ai_trader_id])
        self.assertTrue(second_result.report.success)
        second_state = self.read_audit_state_map()
        self.assertNotEqual(
            first_state["domain:ai-trader"]["last_run_id"],
            second_state["domain:ai-trader"]["last_run_id"],
        )
        self.assertEqual(
            first_state["domain:open-brain"]["last_run_id"],
            second_state["domain:open-brain"]["last_run_id"],
        )
        drift_findings = self.read_jsonl(self.audits_dir / "wiki_bootstrap_drift.jsonl")
        self.assertTrue(any(finding["scope_key"] == "ai-trader" for finding in drift_findings))
