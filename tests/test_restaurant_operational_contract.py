from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def text(path):
    return (ROOT / path).read_text().lower()


def test_explicit_travel_time_scope_contract():
    scope = text('reference/phase-1-scope-and-catchment.md')
    discovery = text('reference/phase-2-candidate-discovery.md')
    for phrase in (
        'travel-time request overrides',
        'isochrone',
        'routing provider and profile',
        'traffic or departure-time assumption',
        'destination-specific route check',
        'modeled geographic extent',
    ):
        assert phrase in scope
    assert 'candidate-volume feasibility checkpoint' in discovery
    assert 'must not silently narrow' in discovery


def test_identity_readiness_precedes_phase4():
    convergence = text('reference/phase-3-discovery-convergence.md')
    research = text('reference/phase-4-evidence-research.md')
    for phrase in (
        'identity-readiness',
        '`ready`',
        '`repair`',
        '`quarantine`',
        'unnamed map object',
        'domain presence alone is not domain correctness',
        'same physical venue',
        'same concept, different branch',
        'successor or historical identity',
    ):
        assert phrase in convergence
    assert 'dispatch only `ready` candidates' in research


def test_adaptive_leaf_size_and_durable_return_gate():
    value = text('reference/phase-4-evidence-research.md')
    for phrase in (
        'adaptive leaf size',
        'durably saved throughput',
        'partial return',
        'only missing candidate ids',
        'zero-progress return',
        'minimum useful leaf size',
        'worker-health circuit breaker',
        '`evidence-returned`',
        '`raw-saved`',
        'before assigning that worker another batch',
        'automatically requeue',
    ):
        assert phrase in value


def test_restaurant_evidence_domains_and_scope():
    worker = text('restaurant-rubric/phase-4-worker-prompt.md')
    scoring = text('restaurant-rubric/phase-6-scoring.md')
    for phrase in (
        '`food`', '`beverage`', '`roastery`', '`bakery`',
        '`branch-local`', '`company-wide`', '`commissary/shared-kitchen`',
        '`external-supplier`', '`predecessor/historical`', '`unknown`',
        '`food-menu-turnover`', '`daily-production`',
        '`availability/daypart`', '`promotion`', '`event`', '`sourcing/delivery`',
    ):
        assert phrase in worker
    assert 'daily production is not menu turnover' in scoring
    assert 'non-food production cannot inflate' in scoring


def test_restaurant_no_score_dispositions():
    scoring = text('restaurant-rubric/phase-6-scoring.md')
    for phrase in ('`score-unresolved`', '`evidence-exhausted-no-score`', 'non-negative'):
        assert phrase in scoring
    for phrase in ('accepted-evidence citation', 'primary missing field or reason', 'positive scratch markers'):
        assert phrase in scoring


def test_positive_dq_subtypes_are_required():
    scoring = text('restaurant-rubric/phase-6-scoring.md')
    for phrase in (
        '`explicit_closed`', '`explicit_no_food`', '`external_food_only`',
        '`offsite_all_production`', '`uncooked_retail_only`', '`confirmed_snack_only`',
    ):
        assert phrase in scoring
    assert '`exhausted-unavailable` must not support a dq' in scoring
    assert 'affirmative source citation' in scoring


def test_phase6_deterministic_integrity_validation():
    scoring = text('restaurant-rubric/phase-6-scoring.md')
    for phrase in (
        'deterministic integrity validation',
        'machine-readable result',
        'population equality',
        'exactly one decision',
        'duplicate decision ids',
        'canonical merge target',
        'criterion maxima',
        'geometric mean',
        'summary disposition counts',
    ):
        assert phrase in scoring
    assert 'the phase gate fails' in scoring


def test_phase8_normalized_rendering_boundary():
    rendering = text('restaurant-rubric/phase-8-rendering.md')
    for phrase in (
        'normalized audit-row schema',
        'vector-form',
        'scalar-form',
        'scoreable decision count',
        'rendered audit-row count',
        'rendering fails',
        'canonical merge target',
    ):
        assert phrase in rendering


def test_large_run_cross_layer_diversity():
    rendering = text('restaurant-rubric/phase-8-rendering.md')
    for phrase in (
        'at least 12 eligible venues',
        'reader-facing discovery budget',
        'occasion slots jointly',
        'distinct restaurant',
        'rare finds',
        'credible distinct alternative',
        'record the exception',
    ):
        assert phrase in rendering
    assert 'diversity is a presentation constraint' in rendering


def test_already_covered_invariants_remain_intact():
    discovery = text('reference/phase-2-candidate-discovery.md')
    audit = text('reference/phase-7-coverage-audit.md')
    scoring = text('restaurant-rubric/phase-6-scoring.md')
    root = text('restaurant-rubric/SKILL.md')
    for phrase in ('matched identity', 'controlled exclusion reason', 'zero new identities'):
        assert phrase in discovery + audit
    assert 'user-reported omission' in audit
    assert '../reference/phase-7-coverage-audit.md' in root
    assert 'service format is orthogonal to production' in scoring
    assert 'chain-ness is magnitude, not direction' in scoring


def test_v812_metadata_is_synchronized():
    bakery = text('bakery-rubric/SKILL.md')
    restaurant = text('restaurant-rubric/SKILL.md')
    assert 'prompt (v8.12)' in bakery and '**v8.12:**' in bakery
    assert 'prompt (v8.12)' in restaurant and '**v8.12:**' in restaurant
    assert 'scratch-food-rubrics/8.12 (research)' in text('bakery-rubric/discovery-reference.md')
    assert 'scratch-food-rubrics/8.12 (research)' in text('restaurant-rubric/discovery-reference.md')
