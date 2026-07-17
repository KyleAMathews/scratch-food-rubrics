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
