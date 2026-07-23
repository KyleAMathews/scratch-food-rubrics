---
name: restaurant-rubric
description: Find ambitious scratch-made restaurants, resist prominence and format bias, and return an evidence-grounded shortlist for a requested location.
---

# Scratch-Kitchen Scorecard & Travel Prompt (v8.14)

Find restaurants that are **scratch-made AND interesting to a frequent diner**. The hidden attribute is ambition: is this a kitchen making meaningful components from raw materials, or a business primarily assembling and reheating commodity inputs?

Scratch production is the eligibility gate. Interestingness distinguishes survivors. Ratings are a quality floor, not the ranking signal. The goal is a trustworthy shortlist—not an objective winner and not paperwork that merely looks complete.

## What this skill must resist

- **Assembly invisibility:** polished menus, photographs, and generic fresh or authentic claims do not establish production.
- **Prominence bias:** broad popularity-neutral discovery protects obscure cuisines, specialists, and informal formats.
- **Map incompleteness:** targeted quality, scratch, local-language, recent-opening, cuisine, and visible-head searches recover prominent or unlisted misses.
- **Format and cuisine prejudice:** counter service, takeaway, lunch-only, rural inns, and unfamiliar cuisines are judged from production evidence.
- **Missing-evidence collapse:** absent process language is a research state, never a low scratch score.
- **Delegation drift:** workers retrieve quotations and literal values; the primary orchestrator makes every judgment.

## Version line

This skill and the bakery skill share one version and bump together.

**v8.14:** both rubrics preserve credible attributable current production evidence through provenance-labeled partial scores; unknown criteria never score zero. Restaurant partial S reports earned/observed-possible, coverage, provenance, and confidence, while turnover is removed from S and remains only in I. The ≈4.0★ restaurant quality gate and rating-unconfirmed tier are unchanged.

**v8.13:** canonical schema-validated `06-decisions.json` is the Phase 6 handoff; optional generated Markdown is non-authoritative; completed runs may offer the separate local-first `/interactive-results` skill. The calibrated rubrics and rating floors are unchanged.

**v8.12:** explicit travel-time scope; identity-readiness routing; adaptive durable evidence dispatch; restaurant production/cadence scoping; honest no-score states; typed positive DQs; deterministic decision/render validation; and large-run cross-layer recommendation diversity. The calibrated rubrics and rating floors are unchanged.

**v8.11:** bounded identity reconciliation for locally relevant item roundups and targeted falsification of user-reported omissions. Bakery-only product × format and provisional-rating rules do not alter the restaurant evidence or scoring contract.

**v8.10:** operational contract hardening; primary-orchestrator-only leaf batching; category-conditional shared acceptance gates; pytest-compatible contract validation; and synchronized workflow metadata. Bakery-only rating, access, and rendered-export additions do not alter the restaurant evidence contract.

**v8.9:** phased execution; just-in-time phase loading and visible completion gates; mandatory broad-survey plus adaptive multilingual targeted discovery; a canonical verbatim evidence-only worker prompt; semantic return acceptance; original-worker targeted repair when available; orchestrator-only scoring; and a post-score coverage audit. The calibrated rubric is unchanged.

**v8.8 and earlier:** model tiering; exhausted-unavailable; recursive fan-out; embedded evidence floor; boundary standardization; completion gating; popularity-neutral enumeration; K-based scratch scoring; market scarcity; execution; and register-independent evidence. Their full unchanged definitions and calibration history are in `phase-6-scoring.md`.

## Primary-orchestrator authority (MUST)

You are the sole orchestrator and judgment layer for the entire run.

- You MUST personally perform classification, positive disqualification, S/I/E/R handling, G/G′, scarcity, tiers, ties, occasions, final confidence, and rendering.
- You MUST NOT delegate scoring or ask a worker to “apply the rubric.” A worker verdict is invalid even when plausible.
- You MUST use `phase-4-worker-prompt.md` verbatim and may substitute only its declared placeholders.
- You MUST inspect every returned venue semantically. Row counts never establish evidence quality.
- You MUST message or resume the original worker for targeted repairs when the runtime supports it; use a fresh worker only under the Phase 5 fallback rules.
- You MUST NOT render recommendations before Phases 1–7 pass.

## Just-in-time phase rule (CRITICAL)

Before executing each phase, you MUST read the named phase file or files in full immediately before doing that work. The summaries below are orientation only and are insufficient for execution. Do not read all phase files once at the beginning and rely on memory. Do not skip, combine, reorder, or silently narrow phases.

Before advancing, run the printed completion gate, mark every item `✅` or `❌` with concrete evidence, and show the concise checklist to the user. Any `❌` means remain in the current phase.

## Phase map

1. **Scope, run directory, and catchment** Read `../reference/phase-1-scope-and-catchment.md`. Before any research, create the unique `<YYYY-MM-DD>-<location-slug>` run directory and manifest; every later artifact stays there.
2. **Candidate discovery** Read `../reference/phase-2-candidate-discovery.md` and `discovery-reference.md`. Run broad, targeted, visible-head, multilingual, cuisine/format, and marker-item discovery.
3. **Discovery convergence** Read `../reference/phase-3-discovery-convergence.md`. Union, normalize, deduplicate, inspect gaps, and require a zero-new-candidate pass or a precise limitation.
4. **Evidence research** Read `../reference/phase-4-evidence-research.md` and `phase-4-worker-prompt.md`. Dispatch the canonical prompt verbatim.
5. **Evidence acceptance and repair** Read `../reference/phase-5-evidence-acceptance.md`, `../reference/shared-status-and-provenance.md`, and `phase-4-worker-prompt.md`. Inspect every record and repair defects.
6. **Restaurant scoring and classification** Read `phase-6-scoring.md`. Apply the current eligibility and partial-scoring policy yourself.
7. **Coverage audit** Read `../reference/phase-7-coverage-audit.md` and `discovery-reference.md`. Newly found restaurants loop through Phases 4–6; repeat until the audit converges.
8. **Rendering** Read `phase-8-rendering.md` only after every earlier gate passes.

## Global hard stops

- No single-source “complete census” claim.
- No targeted search result treated as qualification evidence.
- No missing evidence converted to a low score or disqualification.
- No worker-created DQ, score, tier, ranking, or confidence accepted.
- No service format, cuisine, popularity, or product noun substituted for production evidence.
- No final occasion matrix or ranked shortlist before the Phase 7 gate passes.
- No permission-seeking handoff of unfinished candidates.
- No durable run artifact outside the Phase 1 `{RUN_DIR}` and no reuse or overwrite of an earlier run directory.

Begin with Phase 1 for the location supplied by the user.
