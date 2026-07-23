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


class GeneratorValidationTests(unittest.TestCase):
    def setUp(self):
        self.module = load_module()
        self.decisions = json.loads((FIXTURES / "valid-decisions.json").read_text())
        self.projection = json.loads((FIXTURES / "valid-projection.json").read_text())
        self.projection["source"]["decision_hash"] = self.module.sha256_uri(self.decisions)

    def test_valid_documents_pass(self):
        self.assertEqual(self.module.validate_decisions(self.decisions), [])
        self.assertEqual(self.module.validate_projection(self.projection, self.decisions), [])

    def test_rating_floor_matches_category(self):
        self.projection["theme"]["rating_floor"] = 4.0
        self.assertIn("rating_floor must be 4.3", "\n".join(self.module.validate_projection(self.projection, self.decisions)))

    def test_duplicate_decision_id_fails(self):
        self.decisions["records"].append(copy.deepcopy(self.decisions["records"][0]))
        self.assertIn("duplicate decision id", "\n".join(self.module.validate_decisions(self.decisions)))

    def test_merge_target_must_resolve(self):
        self.decisions["records"][0]["merge_target"] = "MISSING"
        self.assertIn("merge target", "\n".join(self.module.validate_decisions(self.decisions)))

    def test_practical_requires_access_and_populations_do_not_overlap(self):
        self.projection["audit"].append(copy.deepcopy(self.projection["practical"][0]))
        errors = "\n".join(self.module.validate_projection(self.projection, self.decisions))
        self.assertIn("overlap", errors)

    def test_undeclared_facet_value_fails(self):
        self.projection["practical"][0]["facet_values"]["region"] = ["invented"]
        self.assertIn("undeclared facet value", "\n".join(self.module.validate_projection(self.projection, self.decisions)))

    def test_coordinate_and_count_mismatches_fail(self):
        self.projection["practical"][0]["coordinates"]["lat"] = 200
        self.projection["counts"]["mapped"] = 99
        errors = "\n".join(self.module.validate_projection(self.projection, self.decisions))
        self.assertIn("coordinate", errors)
        self.assertIn("mapped count", errors)

    def test_non_finite_number_is_rejected(self):
        self.decisions["records"][0]["score"]["s"] = math.nan
        self.assertIn("finite", "\n".join(self.module.validate_decisions(self.decisions)))

    def test_partial_scores_validate_without_normalization(self):
        partial = self.decisions["records"][1]
        self.assertEqual(partial["score"]["state"], "partial")
        self.assertEqual(self.module.validate_decisions(self.decisions), [])
        partial["score"]["s_coverage"] = 0.9
        self.assertIn("coverage", "\n".join(self.module.validate_decisions(self.decisions)))

    def test_partial_score_must_be_positive(self):
        partial = self.decisions["records"][1]
        partial["score"]["criteria"]["core_craft"] = 0
        partial["score"]["s_earned"] = 0
        self.assertIn("earned score out of range", "\n".join(self.module.validate_decisions(self.decisions)))

    def test_restaurant_partial_scores_validate(self):
        decisions = json.loads((FIXTURES / "valid-restaurant-decisions.json").read_text())
        partial = decisions["records"][1]
        self.assertEqual(partial["score"]["state"], "partial")
        self.assertEqual(self.module.validate_decisions(decisions), [])
        partial["score"]["criteria"]["production"] = 41
        self.assertIn("production out of range", "\n".join(self.module.validate_decisions(decisions)))

    def test_build_payload_joins_canonical_fields_and_map_links(self):
        payload = self.module.build_payload(self.decisions, self.projection)
        mapped = payload["practical"][0]
        unpinned = payload["practical"][1]
        audit = payload["audit"][0]
        self.assertEqual(mapped["score"]["s"], 82)
        self.assertEqual(unpinned["score"]["state"], "partial")
        self.assertIn("maps/search", mapped["map_url"])
        self.assertEqual(mapped["map_action"], "Directions")
        self.assertIn("maps/search", unpinned["map_url"])
        self.assertIn("Moonrise+Microbakery", unpinned["map_url"])
        self.assertIn("Example+metro", unpinned["map_url"])
        self.assertEqual(audit["map_action"], "Find on Google Maps")
        self.assertNotIn("sources", mapped)
        self.assertNotIn("rationale", mapped)

    def test_build_payload_uses_name_and_address_query(self):
        payload = self.module.build_payload(self.decisions, self.projection)
        url = payload["practical"][0]["map_url"]
        self.assertIn("North+Star+Bread", url)
        self.assertIn("123+Main+St", url)


class RenderTests(unittest.TestCase):
    def setUp(self):
        self.module=load_module()
        self.decisions=json.loads((FIXTURES/"valid-decisions.json").read_text())
        self.projection=json.loads((FIXTURES/"valid-projection.json").read_text())
        self.projection["source"]["decision_hash"]=self.module.sha256_uri(self.decisions)

    def test_render_is_deterministic_and_script_safe(self):
        payload=self.module.build_payload(self.decisions,self.projection)
        payload["practical"][0]["summary"]='</script><b>&\u2028"\''
        template='<script type="application/json">__INTERACTIVE_RESULTS_PAYLOAD__</script>'
        first=self.module.render(template,payload)
        second=self.module.render(template,payload)
        self.assertEqual(first,second)
        self.assertNotIn('</script><b>',first)
        self.assertIn('\\u003c/script\\u003e',first)
        self.assertIn('\\u0026',first)

    def test_render_requires_exactly_one_marker(self):
        with self.assertRaises(ValueError): self.module.render('none',{})
        with self.assertRaises(ValueError): self.module.render('__INTERACTIVE_RESULTS_PAYLOAD____INTERACTIVE_RESULTS_PAYLOAD__',{})

    def test_failed_generation_preserves_existing_output(self):
        with tempfile.TemporaryDirectory() as td:
            td=Path(td); out=td/'index.html'; out.write_text('sentinel')
            bad=copy.deepcopy(self.projection); bad['counts']['mapped']=99
            p=td/'projection.json'; p.write_text(json.dumps(bad))
            with self.assertRaises(ValueError):
                self.module.generate(FIXTURES/'valid-decisions.json',p,td/'missing-template.html',out,td/'validation.json','2026-07-18T00:00:00Z')
            self.assertEqual(out.read_text(),'sentinel')

    def test_successful_generation_is_deterministic_and_reports_hashes(self):
        with tempfile.TemporaryDirectory() as td:
            td=Path(td); template=td/'template.html'; template.write_text('<script type="application/json">__INTERACTIVE_RESULTS_PAYLOAD__</script>')
            projection=td/'projection.json'; projection.write_text(json.dumps(self.projection))
            decisions=td/'decisions.json'; decisions.write_text(json.dumps(self.decisions))
            (td/'00-run-manifest.md').write_text('fixture'); (td/'05-evidence-ledger.md').write_text('fixture')
            out=td/'index.html'; report=td/'validation.json'
            result=self.module.generate(decisions,projection,template,out,report,'2026-07-18T00:00:00Z')
            first=out.read_bytes()
            self.module.generate(decisions,projection,template,out,report,'2026-07-18T00:00:00Z')
            self.assertEqual(first,out.read_bytes())
            self.assertEqual(result['status'],'static-pass')
            self.assertTrue(all(v.startswith('sha256:') for v in result['hashes'].values()))
            self.assertNotIn(str(td),out.read_text())


class TemplateContractTests(unittest.TestCase):
    def setUp(self):
        self.template=(SKILL_DIR/'template.html').read_text()

    def test_payload_marker_and_leaflet_contract(self):
        self.assertEqual(self.template.count('__INTERACTIVE_RESULTS_PAYLOAD__'),1)
        self.assertIn('leaflet@1.9.4',self.template)
        self.assertIn('tile.openstreetmap.org',self.template)

    def test_stable_dom_hooks_exist(self):
        for hook in ('search','mode-practical','mode-audit','sort','facet-panel','results','map-panel','map','filters-toggle','map-toggle','result-count','mapped-count','saved-only'):
            self.assertIn(f'id="{hook}"',self.template)
        self.assertIn('data-record-id',self.template)

    def test_interaction_and_layout_contract(self):
        for phrase in ('localStorage','showCard','alternateFacetCounts','scoreMetrics','Scratch evidence','defaultRatingFloor','state.rating=defaultRatingFloor','scrollIntoView','.focus(','minmax(0, 1fr)','min-height: 0','overflow: hidden','overflow: auto','@media (max-width: 1050px)','@media (max-width: 720px)'):
            self.assertIn(phrase,self.template)
        self.assertNotIn('>Any</strong>', self.template)
        self.assertNotIn('onclick=',self.template.lower())

    def test_only_leaflet_is_external_application_dependency(self):
        self.assertEqual(self.template.count('<script src='),1)
        self.assertEqual(self.template.count('<link rel="stylesheet" href='),1)
