import copy
import importlib.util
import json
import math
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = ROOT / "interactive-results"
FIXTURES = SKILL_DIR / "tests" / "fixtures"


def load_module():
    spec = importlib.util.spec_from_file_location("interactive_generate", SKILL_DIR / "generate.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SchemaContractTests(unittest.TestCase):
    def test_schema_files_and_valid_fixtures_exist(self):
        for name in (
            "decision-schema.json", "interactive-schema.json",
            "tests/fixtures/valid-decisions.json", "tests/fixtures/valid-projection.json",
            "tests/fixtures/valid-restaurant-decisions.json", "tests/fixtures/valid-restaurant-projection.json",
        ):
            self.assertTrue((SKILL_DIR / name).is_file(), name)

    def test_schema_documents_are_draft_2020_12(self):
        for name in ("decision-schema.json", "interactive-schema.json"):
            doc = json.loads((SKILL_DIR / name).read_text())
            self.assertEqual(doc["$schema"], "https://json-schema.org/draft/2020-12/schema")
            self.assertEqual(doc["type"], "object")

    def test_fixtures_cover_both_categories_and_modes(self):
        bakery = json.loads((FIXTURES / "valid-decisions.json").read_text())
        restaurant = json.loads((FIXTURES / "valid-restaurant-decisions.json").read_text())
        projection = json.loads((FIXTURES / "valid-projection.json").read_text())
        self.assertEqual(bakery["category"], "bakery")
        self.assertEqual(restaurant["category"], "restaurant")
        self.assertGreaterEqual(len(projection["practical"]), 2)
        self.assertGreaterEqual(len(projection["audit"]), 1)
        self.assertTrue(any(row["coordinates"] is None for row in projection["practical"]))
