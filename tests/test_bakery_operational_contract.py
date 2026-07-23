from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def text(path):
    return (ROOT / path).read_text().lower()

def test_category_gate():
    value = text('bakery-rubric/phase-6-scoring.md')
    assert 'affirmative bakery production' in value and 'confectionery alone' in value

def test_identity_first_rating_contract():
    value = text('bakery-rubric/phase-4-worker-prompt.md') + text('reference/phase-5-evidence-acceptance.md')
    for phrase in ('identity tuple', 'exact-no-rating', 'no-exact-record', 'identity-conflict', 'stable place id', 'rejection log'):
        assert phrase in value

def test_visible_unconfirmed_and_access_routing():
    value = text('bakery-rubric/phase-8-rendering.md')
    for phrase in ('rating-unconfirmed', 'access format', 'current acquisition evidence', 'availability-sensitive watchlist'):
        assert phrase in value

def test_worker_artifact_contract():
    worker = text('bakery-rubric/phase-4-worker-prompt.md')
    shared = text('reference/phase-4-evidence-research.md')
    assert '{output_path}' in worker and 'candidate id' in worker
    assert '{output_path}' in shared and 'unique leaf-batch file' in shared
    assert 'do not delegate or recursively split' in worker

def test_acceptance_and_rendering_gates():
    phase5 = text('reference/phase-5-evidence-acceptance.md').split('## completion gate', 1)[1]
    phase8 = text('bakery-rubric/phase-8-rendering.md').split('## phase 8 completion gate', 1)[1]
    for phrase in ('direct-place', 'rejection log', 'access format', 'current acquisition evidence'):
        assert phrase in phase5
    for phrase in ('availability-sensitive watchlist', 'direct-place rating rerun', 'visual inspection', 'long tables'):
        assert phrase in phase8

def test_branch_scope():
    value = text('reference/phase-3-discovery-convergence.md') + text('reference/phase-5-evidence-acceptance.md')
    for phrase in ('company-wide', 'branch-specific', 'store-local'):
        assert phrase in value

def test_not_scoreable_disposition():
    value = text('bakery-rubric/phase-6-scoring.md')
    assert 'not-scoreable' in value and 'non-negative' in value

def test_bakery_partial_score_contract():
    scoring = text('bakery-rubric/phase-6-scoring.md')
    rendering = text('bakery-rubric/phase-8-rendering.md')
    for phrase in (
        'missing criteria are `unknown`, never zero',
        '`s_bakery partial = earned/observed-possible`',
        'user-ground-truth',
        'narrowly proven component',
        'scratch-eligible-partial',
        'never apply the complete-score s floor to a partial denominator',
    ):
        assert phrase in scoring
    for phrase in ('scratch-eligible, partial evidence', 'fillings made in house; dough and lamination unknown'):
        assert phrase in rendering

def test_cultural_discovery_terms():
    value = text('bakery-rubric/discovery-reference.md')
    for phrase in ('empanada', 'pastelito', 'kolache', 'burek', 'ensaymada', 'pandesal'):
        assert phrase in value

def test_multi_component_boundary_fallback():
    value = text('reference/phase-1-scope-and-catchment.md')
    for phrase in ('corridor', 'component', 'fallback'):
        assert phrase in value

def test_coverage_repeats_to_zero():
    value = text('reference/phase-7-coverage-audit.md')
    assert 'zero' in value and ('repeat' in value or 'loop' in value), 'coverage repeats to zero'

def test_shared_contract_category_consistency():
    """shared-contract consistency across category and shared phases."""
    shared = text('reference/phase-4-evidence-research.md') + text('reference/phase-5-evidence-acceptance.md')
    bakery = text('bakery-rubric/phase-4-worker-prompt.md')
    restaurant = text('restaurant-rubric/phase-4-worker-prompt.md')
    assert 'for bakery runs only' in shared
    assert 'do not delegate or recursively split' in bakery
    assert 'do not delegate or recursively split' in restaurant
    assert 'exact-rated-count-unavailable' in bakery and 'count-unavailable' in shared

def test_roundup_identity_reconciliation():
    value = text('reference/phase-2-candidate-discovery.md') + text('reference/phase-7-coverage-audit.md')
    for phrase in ('matched identity', 'candidate id', 'controlled exclusion reason', 'zero new identities'):
        assert phrase in value


def test_product_by_adjacent_format_discovery():
    value = text('bakery-rubric/discovery-reference.md')
    for phrase in ('product × adjacent-format', 'bagel', 'deli'):
        assert phrase in value


def test_user_reported_miss_falsification_pass():
    value = text('reference/phase-7-coverage-audit.md')
    for phrase in ('user-reported omission', 'discovery route', 'phases 4–6', 'zero new'):
        assert phrase in value


def test_aggregator_attributed_provisional_rating_contract():
    worker = text('bakery-rubric/phase-4-worker-prompt.md')
    acceptance = text('reference/phase-5-evidence-acceptance.md')
    scoring = text('bakery-rubric/phase-6-scoring.md')
    rendering = text('bakery-rubric/phase-8-rendering.md')
    for phrase in ('aggregator-attributed', 'attributed platform', 'matched identity', 'access date'):
        assert phrase in worker + acceptance
    assert 'provisional rating' in scoring
    assert 'near-tie' in rendering and 'direct' in rendering


def test_v814_metadata_is_synchronized():
    bakery = text('bakery-rubric/SKILL.md')
    restaurant = text('restaurant-rubric/SKILL.md')
    assert 'prompt (v8.14)' in bakery and '**v8.14:**' in bakery
    assert 'prompt (v8.14)' in restaurant and '**v8.14:**' in restaurant
    assert 'scratch-food-rubrics/8.14 (research)' in text('bakery-rubric/discovery-reference.md')
    assert 'scratch-food-rubrics/8.14 (research)' in text('restaurant-rubric/discovery-reference.md')
