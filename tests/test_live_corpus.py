from __future__ import annotations

import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from sessionmemory.audit import run_audit
from sessionmemory.bootstrap import run_bootstrap
from sessionmemory.classification import run_classification
from sessionmemory.discovery import run_discovery
from sessionmemory.extraction import run_extraction
from sessionmemory.normalization import run_normalization
from sessionmemory.raw_event_resolver import RawEventResolver
from sessionmemory.segmentation import run_segmentation
from sessionmemory.wiki import run_wiki


def real_sessions_root() -> Path:
    return Path(os.environ.get("SESSIONMEMORY_CODEX_SESSIONS_ROOT", r"C:\Users\Fabio\.codex\sessions"))


@unittest.skipUnless(os.environ.get("SESSIONMEMORY_RUN_LIVE_TESTS") == "1", "live corpus tests disabled")
class LiveCorpusTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="sessionmemory-live-"))
        self.sample_root = self.temp_dir / "sessions"
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
        repo_root = Path(__file__).resolve().parents[1]
        self.schema_path = repo_root / "schema" / "normalization_catalog.json"
        self.base_taxonomy_path = repo_root / "config" / "classification_taxonomy.json"
        self.base_rules_path = repo_root / "config" / "extraction_rules.json"
        self.base_wiki_config_path = repo_root / "config" / "wiki_config.json"
        self.base_bootstrap_config_path = repo_root / "config" / "bootstrap_config.json"
        self.base_audit_config_path = repo_root / "config" / "audit_config.json"
        self.manifest_path = Path(__file__).with_name("fixtures") / "live_corpus_manifest.json"
        self.copy_manifest_sources()
        self.write_configs()

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def copy_manifest_sources(self) -> None:
        manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        root = real_sessions_root()
        for item in manifest["samples"]:
            relative_path = Path(item["relative_path"])
            source_path = root / relative_path
            if not source_path.exists():
                raise unittest.SkipTest(f"Missing live sample source: {source_path}")
            target_path = self.sample_root / relative_path
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_path, target_path)

    def write_configs(self) -> None:
        self.source_config_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "roots": [
                        {
                            "root_alias": "codex_sessions",
                            "absolute_path": str(self.sample_root),
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

    def read_json(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def read_jsonl(self, path: Path) -> list[dict]:
        return [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

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

    def test_live_sample_pipeline_is_pointer_first_and_stable(self) -> None:
        manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        golden_source_id = "019cbacf-74e5-7411-a1ab-6595d49c26a2"

        discovery_result = run_discovery(self.source_config_path, self.state_dir)
        self.assertTrue(discovery_result.report.success)
        normalization_result = run_normalization(
            config_path=self.source_config_path,
            state_dir=self.state_dir,
            schema_path=self.schema_path,
            normalized_dir=self.normalized_dir,
            audits_dir=self.audits_dir,
        )
        self.assertTrue(normalization_result.report.success)

        segmentation_result = run_segmentation(
            state_dir=self.state_dir,
            normalized_dir=self.normalized_dir,
            segmented_dir=self.segmented_dir,
        )
        self.assertTrue(segmentation_result.report.success)

        classification_result = run_classification(
            taxonomy_path=self.taxonomy_path,
            state_dir=self.state_dir,
            normalized_dir=self.normalized_dir,
            segmented_dir=self.segmented_dir,
            classified_dir=self.classified_dir,
            audits_dir=self.audits_dir,
            source_roots_config_path=self.source_config_path,
        )
        self.assertTrue(classification_result.report.success)

        extraction_result = run_extraction(
            rules_path=self.rules_path,
            state_dir=self.state_dir,
            normalized_dir=self.normalized_dir,
            classified_dir=self.classified_dir,
            extracted_dir=self.extracted_dir,
            audits_dir=self.audits_dir,
            source_roots_config_path=self.source_config_path,
        )
        self.assertTrue(extraction_result.report.success)

        with patch("sessionmemory.wiki.call_openai_structured_json", side_effect=self.make_fake_wiki_synthesizer()):
            wiki_result = run_wiki(
                config_path=self.wiki_config_path,
                state_dir=self.state_dir,
                extracted_dir=self.extracted_dir,
                wiki_dir=self.wiki_dir,
                audits_dir=self.audits_dir,
            )
        self.assertTrue(wiki_result.report.success)

        with patch("sessionmemory.bootstrap.call_openai_structured_json", side_effect=self.make_fake_bootstrap_synthesizer()):
            bootstrap_result = run_bootstrap(
                config_path=self.bootstrap_config_path,
                state_dir=self.state_dir,
                extracted_dir=self.extracted_dir,
                wiki_dir=self.wiki_dir,
                bootstrap_dir=self.bootstrap_dir,
                audits_dir=self.audits_dir,
            )
        self.assertTrue(bootstrap_result.report.success)

        audit_result = run_audit(
            config_path=self.audit_config_path,
            state_dir=self.state_dir,
            extracted_dir=self.extracted_dir,
            wiki_dir=self.wiki_dir,
            bootstrap_dir=self.bootstrap_dir,
            audits_dir=self.audits_dir,
        )
        self.assertTrue(audit_result.report.success)
        self.assertEqual(audit_result.report.error_finding_count, 0)

        resolver = RawEventResolver.from_paths(
            registry_path=self.state_dir / "source_registry.json",
            source_roots_config_path=self.source_config_path,
        )
        raw_sample_bytes = 0
        sampled_hydrations = 0
        for item in manifest["samples"]:
            relative_path = Path(item["relative_path"])
            raw_sample_bytes += (self.sample_root / relative_path).stat().st_size
            events_path = self.normalized_dir / "sources" / item["source_id"] / "events.jsonl"
            events = self.read_jsonl(events_path)
            self.assertTrue(events)
            self.assertTrue(all("raw_event" not in event for event in events))
            candidates = [events[0]]
            truncated = next((event for event in events if event.get("text_surface_truncated")), None)
            if truncated is not None and truncated is not candidates[0]:
                candidates.append(truncated)
            for event in candidates:
                hydrated = resolver.hydrate_normalized_event(event)
                self.assertIsInstance(hydrated.raw_event, dict)
                sampled_hydrations += 1
        self.assertGreater(sampled_hydrations, 0)

        normalized_bytes = sum(
            path.stat().st_size
            for path in self.normalized_dir.rglob("*")
            if path.is_file()
        )
        self.assertLessEqual(normalized_bytes, int(raw_sample_bytes * 0.25))

        golden_classified_stats = self.read_json(self.classified_dir / "sources" / golden_source_id / "stats.json")
        self.assertEqual(golden_classified_stats["primary_label_counts"].get("unclassified", 0), 0)
        golden_extracted_stats = self.read_json(self.extracted_dir / "sources" / golden_source_id / "stats.json")
        self.assertEqual(golden_extracted_stats["domain_counts"].get("unclassified", 0), 0)


if __name__ == "__main__":
    unittest.main()
