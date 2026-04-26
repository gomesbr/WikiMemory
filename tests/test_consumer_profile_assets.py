from __future__ import annotations

import json
import unittest
from pathlib import Path


class ConsumerProfileAssetTests(unittest.TestCase):
    def test_consumer_profile_schema_declares_safe_boundaries(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        payload = json.loads((repo_root / "schema" / "consumer_working_profile.schema.json").read_text(encoding="utf-8"))
        self.assertIn("communication_preferences", payload["rules"]["allowed_inference_scope"])
        self.assertIn("iq_or_intelligence_scores", payload["rules"]["disallowed_inference_scope"])

    def test_consumer_profile_policy_defaults_to_review_first(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        payload = json.loads((repo_root / "config" / "consumer_profile_policy.json").read_text(encoding="utf-8"))
        self.assertFalse(payload["enabled"])
        self.assertEqual(payload["mode"], "review_first")
        self.assertTrue(payload["require_consumer_review_before_activation"])


if __name__ == "__main__":
    unittest.main()
