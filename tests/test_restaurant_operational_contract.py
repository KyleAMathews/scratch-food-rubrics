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
