# Restaurant Workflow Reliability Design

**Date:** 2026-07-17
**Status:** Approved for implementation planning
**Scope:** Focused contract-level refinements derived from the completed East Millcreek restaurant rubric test run

## Goal

Improve restaurant recommendation correctness and execution reliability at large candidate volumes without changing the calibrated scoring rubric, rating threshold, or the principle that service format and chain status are not scratch-production proxies.

## Context

The restaurant v8.10 test run completed all eight phases over a 30-minute drive-time catchment. It produced 2,927 frozen discovery candidates and 1,650 final evidence and decision records after auditable triage, identity repair, and Phase 7 additions. The run succeeded, but it exposed nine gaps in the current workflow:

1. Explicit travel-time requests lack a reproducible scope contract.
2. Candidates can enter evidence research before their identities are research-ready.
3. Fixed evidence-worker leaf sizes and conversational-only returns cause truncation and duplicated work.
4. Restaurant scoring lacks first-class non-negative no-score dispositions.
5. Food production and menu-turnover evidence can be contaminated by other domains and scopes.
6. The positive-evidence DQ rule is not mechanically constrained.
7. Phase 6 lacks a mandatory deterministic integrity validation.
8. Phase 8 lacks a normalized rendering boundary and score-row count assertion.
9. Large runs can waste reader-facing recommendation slots through repeated venues across occasion and rare-find layers.

Three related concerns are already handled on current `main` and are not part of this design: bounded roundup reconciliation and omission falsification, direct Phase 7 file mapping, and the existing rule that chain magnitude and service format do not establish scratch quality.

## Architecture

Make focused changes to the existing phase contracts rather than introducing a generalized research platform:

- Shared Phase 1 defines explicit travel-time scope behavior.
- Shared Phases 3 and 4 add identity readiness and adaptive durable dispatch.
- The restaurant Phase 4 prompt adds lightweight production and cadence scope labels.
- Restaurant Phase 6 adds honest no-score states, controlled DQ evidence, and integrity validation.
- Restaurant Phase 8 normalizes score rows and jointly allocates reader-facing recommendation slots on large runs.

The implementation remains Markdown-contract driven with static contract tests. It does not ship a universal clustering utility, scheduler, validator parser, or renderer in this pass.

## 1. Explicit travel-time scope

When a user explicitly requests a travel-time boundary, that request overrides the default administrative-boundary or resident-normal-market heuristic.

Phase 1 must record:

- exact origin;
- requested duration;
- travel mode;
- routing provider and profile;
- live, typical, departure-time, or reproducible routing assumption;
- retrieval time;
- saved isochrone geometry;
- point-in-polygon method;
- known routing or map-data limitations.

The contract remains provider-neutral. It does not mandate Valhalla or any other service.

A venue near the generalized polygon edge requires a destination-specific route check before its scope status is finalized. The run must preserve the route result and assumptions.

Before discovery proceeds, Phase 1 reports the modeled geographic extent. After the broad survey, Phase 2 reports candidate volume and records a feasibility checkpoint. An unexpectedly large result changes tiling and downstream batching; it does not silently narrow the user’s requested boundary.

## 2. Identity readiness before evidence research

After Phase 3 convergence and before Phase 4 dispatch, every candidate receives one identity-readiness state:

- `ready`: the named identity and provenance are sufficient for evidence research;
- `repair`: the venue is likely real, but its name, address, branch, domain, successor, or catchment identity needs bounded correction;
- `quarantine`: no researchable venue identity exists yet, such as an unresolved unnamed map object.

A claimed official domain is accepted only when it matches the candidate through the venue name plus address, phone, or another strong identity field. Domain presence alone is not domain correctness.

Shared domains, shared phones, similar names, common addresses, and proximity may propose a relationship. They never authorize a merge without primary-orchestrator review. The relationship model distinguishes:

- same physical venue;
- same concept, different branch;
- successor or historical identity;
- different venue;
- unresolved.

Successful repair returns a candidate to `ready`. Quarantined records remain auditable but do not consume full evidence packets. Neither `repair` nor `quarantine` is a DQ or negative quality judgment.

## 3. Adaptive and durable evidence dispatch

The primary orchestrator remains the only layer that creates leaf batches. It begins with a modest runtime-appropriate leaf size, never exceeding the current 10–15 venue ceiling, and adapts from observed durable throughput.

Dispatch behavior:

1. Measure completed and durably saved candidate records, not assigned count or conversational claims.
2. A partial return triggers a smaller continuation containing only missing candidate IDs.
3. A zero-progress return triggers immediate shrinkage or reassignment.
4. Repeated zero progress at the minimum useful leaf size suspends that worker from new evidence assignments until a later explicit probe.
5. Every failed or incomplete candidate is automatically requeued to a healthy worker or retained in a visible repair queue.

A candidate progresses through two distinct states:

- `evidence-returned`: the worker produced a record;
- `raw-saved`: the unedited record is confirmed in the run directory and indexed.

Conversational content alone is not durable completion. The orchestrator must not give a worker a new batch until the prior return is confirmed `raw-saved` or explicitly requeued. Raw-return defects, including section-count mismatches, are preserved rather than edited away.

This contract is adaptive. It does not hard-code four candidates for every runtime.

## 4. Domain-scoped production and cadence evidence

Restaurant evidence workers add lightweight descriptive labels without judging or scoring.

### Production domain

- `food`
- `beverage`
- `roastery`
- `bakery`

### Production location or scope

- `branch-local`
- `company-wide`
- `commissary/shared-kitchen`
- `external-supplier`
- `predecessor/historical`
- `unknown`

### Cadence domain

- `food-menu-turnover`
- `daily-production`
- `availability/daypart`
- `beverage`
- `promotion`
- `event`
- `sourcing/delivery`

Every label remains tied to its literal quotation, source, identity, and date. A worker may use `unknown` rather than infer scope.

Phase 6 may use accepted `food-menu-turnover` evidence for the existing turnover criterion. It must not promote any of the following into food-menu turnover without separate literal evidence:

- daily preparation or production;
- opening hours or dayparts;
- seasonal drinks;
- promotions;
- entertainment or events;
- supplier delivery schedules;
- food-hall tenant rotation.

Non-food production cannot inflate a food scratch score. Company-wide, commissary, supplier, and predecessor evidence stays in its accepted scope and cannot silently become branch-local current production.

## 5. Non-negative no-score dispositions

Restaurant Phase 6 adds two controlled dispositions:

- `evidence-exhausted-no-score`: the required evidence search completed, but the accepted record does not support a defensible scoring packet;
- `score-unresolved`: accepted positive evidence exists, potentially including meaningful scratch markers, but one or more required scoring dimensions remain too uncertain for a numeric decision.

Each decision records:

- candidate ID;
- accepted-evidence citation;
- disposition;
- primary missing field or reason;
- any positive scratch markers worth retaining.

Neither disposition implies low quality, ineligibility, or DQ. Missing evidence must not become a low numeric score. Mechanically generated decision rows are allowed only when every row preserves its individual evidence citation and reason.

## 6. Controlled positive-evidence DQs

Every restaurant DQ requires an affirmative source citation and one controlled evidence subtype:

- `explicit_closed`
- `explicit_no_food`
- `external_food_only`
- `offsite_all_production`
- `uncooked_retail_only`
- `confirmed_snack_only`

The subtype records why the venue falls outside the restaurant producer set; it does not assert general quality.

The following cannot support a DQ on their own:

- `exhausted-unavailable`;
- missing process language;
- weak web presence;
- service category or format;
- generic menu appearance;
- chain or franchise status;
- absence of food-program evidence.

If affirmative DQ evidence is absent, the record remains unresolved or exhausted rather than being removed.

## 7. Phase 6 deterministic integrity validation

Before Phase 6 closes, run a deterministic validation over the complete decision ledger and save the machine-readable result inside the run directory.

Required invariants:

- frozen plus accepted Phase 7 additions equals the decision population;
- every canonical candidate has exactly one decision;
- no duplicate decision IDs exist;
- every canonical merge target exists and is not itself unresolved;
- each criterion stays within its printed maximum;
- criterion values and total S are internally consistent;
- G is recomputed with the existing formula and rounding rule;
- ranked records satisfy the existing scratch and rating gates;
- every DQ has a permitted positive-evidence subtype and citation;
- unresolved and exhausted records do not enter ranked tiers;
- summary disposition counts sum to the decision population.

The phase gate fails when any invariant fails. The implementation initially requires a run-local deterministic validator and preserved result; it does not require a universal parser in the repository until the artifact schema is stable enough to justify one.

## 8. Phase 8 normalized rendering boundary

Before rendering, transform every scoreable Phase 6 decision into one normalized audit-row schema. This includes ordinary vector-form decisions and calibration-backed scalar-form decisions.

The normalized row contains at least:

- canonical candidate ID;
- canonical venue name;
- disposition;
- criterion or accepted scalar score representation;
- total S;
- I;
- rating value and provenance;
- computed G;
- tier and ranking eligibility;
- canonical merge target when applicable.

Rendering fails when:

- a scoreable decision cannot be normalized;
- an ID appears more than once;
- a canonical merge target is missing;
- a normalized score violates Phase 6 validation;
- rendered audit-row count differs from the Phase 6 scoreable-decision count.

The final report records both counts. Successful Markdown, HTML, or PDF generation is not proof of complete rendering.

## 9. Large-run reader-facing diversity

When at least 12 eligible venues exist, allocate occasion and rare-find recommendations as one reader-facing discovery budget.

Selection order:

1. Choose all occasion slots jointly while preserving evidence strength, occasion fit, scratch eligibility, rating rules, and honest near-ties.
2. Prefer a distinct restaurant in each occasion slot.
3. Choose rare finds against the already-used venue set while preserving the rare-item scratch and scarcity gates.
4. Repeat a venue only when a specific occasion or rare-item requirement lacks a credible distinct alternative.
5. Record the reason for every exception.

Diversity is a presentation constraint, not a scoring input. It never changes the numeric audit, lowers the evidence threshold, invents rarity, or promotes a weak venue solely to avoid repetition. Completeness-oriented appendices may repeat venues because they are not scarce recommendation slots.

## Error handling

- If a travel-time provider fails, record the failure and ask the user before substituting a materially different boundary model.
- If an edge route cannot be checked, retain explicit scope uncertainty rather than silently including or excluding the venue.
- If identity repair remains ambiguous, quarantine the record; do not attach uncertain evidence.
- If a worker repeatedly returns zero durable records, suspend and requeue rather than treating dispatch intent as completion.
- If production or cadence scope is unknown, preserve `unknown`; do not infer the scoring domain.
- If a DQ lacks affirmative evidence, reject the DQ.
- If Phase 6 validation or Phase 8 normalization fails, stop the phase and repair the ledger before rendering.
- If diversity constraints leave fewer than three credible choices for an occasion, reuse the strongest eligible venue and record the exception.

## Testing strategy

Contract tests must demonstrate each confirmed gap before implementation and pass afterward:

1. explicit travel-time scope and feasibility metadata;
2. identity-readiness states and official-domain validation;
3. adaptive leaf sizing, durable-save gating, requeue behavior, and worker suspension;
4. first-class `score-unresolved` and `evidence-exhausted-no-score` dispositions;
5. domain-scoped production and cadence labels plus anti-promotion rules;
6. controlled positive-DQ subtypes and rejection of absence-based DQs;
7. Phase 6 machine-validation invariants;
8. Phase 8 normalized score schema and rendered-count equality;
9. joint occasion and rare-find diversity for large runs.

Existing contract tests must remain green, especially those covering:

- broad and targeted discovery convergence;
- bounded roundup reconciliation and user-omission falsification;
- chain and service-format neutrality;
- category and branch scope;
- rating provenance;
- bakery workflow behavior.

## Non-goals

This refinement does not:

- change calibrated restaurant scoring criteria, weights, maxima, formula, or rating floor;
- add a universal fuzzy-clustering utility;
- add a generalized task scheduler or worker-health service;
- ship a universal Phase 6 validator parser;
- ship a reusable Phase 8 renderer;
- create a new anti-chain, anti-franchise, anti-fast-food, anti-dessert, or anti-counter-service filter;
- add a broad confidence ontology;
- redesign current availability states;
- implement the interactive website skill.

The website workflow remains the next independent design and implementation effort after these restaurant-contract refinements are complete.
