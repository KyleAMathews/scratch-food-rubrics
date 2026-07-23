import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]

def text(path): return (ROOT/path).read_text().lower()

class SkillWorkflowTests(unittest.TestCase):
    def test_workflow_contract(self):
        value=text('interactive-results/SKILL.md')
        for phrase in ('/interactive-results <run_dir>','path is mandatory','never guess','phase 8 completion','snapshot-only','must not perform fresh web lookup','06-decisions.json','interactive-results-migration.json','consequential_ambiguities','use your defaults','required facet-design checkpoint','practical','audit','08-results.md','full evidence-supported suitability set','not only the three venues','interactive-occasion-assignment-audit.json','interactive-results/generate.py','python3 -m http.server 8765','browser validation is mandatory','interactive-results-validation.json','update the manifest','separate explicit request','no automatic publication'):
            self.assertIn(phrase,value)

    def test_readme_lists_optional_third_skill(self):
        value=text('README.md')
        for phrase in ('interactive results','/interactive-results <run_dir>','06-decisions.json','local-first','optional post-run'):
            self.assertIn(phrase,value)

class CoreIntegrationTests(unittest.TestCase):
    def test_shared_json_authority(self):
        value=text('reference/shared-status-and-provenance.md')
        for phrase in ('06-decisions.json','canonical','optional','generated','decision-schema.json'):
            self.assertIn(phrase,value)

    def test_phase6_and_phase8_contracts(self):
        for category in ('bakery','restaurant'):
            p6=text(f'{category}-rubric/phase-6-scoring.md')
            for phrase in ('06-decisions.json','../interactive-results/decision-schema.json','schema validation','content hash','manifest'):
                self.assertIn(phrase,p6)
            p8=text(f'{category}-rubric/phase-8-rendering.md')
            for phrase in ('06-decisions.json','canonical json','independently authored','/interactive-results {run_dir}','do not invoke'):
                self.assertIn(phrase,p8)

if __name__=='__main__': unittest.main()
