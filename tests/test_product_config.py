from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from wikimemory.memory_model import MEMORY_CLASS_TO_FILE_KEY, MEMORY_FILE_DEFINITIONS
from wikimemory.product_config import (
    PRODUCT_SCHEMA_VERSION,
    ProductConfigError,
    default_product_config,
    load_product_config,
    parse_product_config,
)


class ProductConfigTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="wikimemory-product-config-"))
        self.config_path = self.temp_dir / "product_config.json"

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_default_product_config_matches_memory_first_shape(self) -> None:
        config = default_product_config(self.temp_dir)
        self.assertEqual(config.product_schema_version, PRODUCT_SCHEMA_VERSION)
        self.assertEqual(config.markdown_output.root_dir, "memory")
        self.assertEqual(config.agent_platform.bootstrap_target_path, "AGENTS.md")
        self.assertTrue(config.policies.require_confirmation_for_inferred_rule_promotion)
        self.assertEqual(config.project_sources[0].adapter, "git_worktree")

    def test_load_product_config_validates_supported_adapters(self) -> None:
        payload = default_product_config(self.temp_dir).to_dict()
        payload["log_sources"][0]["adapter"] = "unknown_adapter"
        self.config_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        with self.assertRaises(ProductConfigError):
            load_product_config(self.config_path)

    def test_parse_product_config_accepts_repo_relative_shape(self) -> None:
        payload = default_product_config(self.temp_dir).to_dict()
        payload["environment"]["repo_root"] = "."
        payload["project_sources"][0]["project_root"] = "."
        config = parse_product_config(payload)
        self.assertEqual(config.environment.repo_root, ".")
        self.assertEqual(config.project_sources[0].project_root, ".")

    def test_memory_file_definitions_cover_all_primary_memory_classes(self) -> None:
        for memory_class, file_key in MEMORY_CLASS_TO_FILE_KEY.items():
            self.assertIn(file_key, MEMORY_FILE_DEFINITIONS, memory_class)
