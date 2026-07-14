# Phased Rubric Execution Hardening Design

**Date:** 2026-07-14  
**Repository:** `scratch-food-rubrics`  
**Status:** Approved for planning

## Purpose

Harden execution of the restaurant and bakery skills without changing either rubric.

The current skills contain the right retrieval, evidence, delegation, scoring, and completion principles, but they place too many instructions in one long context. In the unsuccessful Salt Lake Valley bakery run, those instructions decayed during execution: the orchestrator wrote its own weaker worker prompt, delegated scoring, accepted rows by cardinality rather than evidence quality, treated an OSM result set as a complete census, and converted thin evidence into negative craft judgments.

This refactor changes instruction architecture and retrieval procedure only. It does not change the rubrics' goals, axes, weights, thresholds, calibration cases, scoring formulas, occasion categories, rare-find logic, rating treatment, or presentation semantics.

## Mission grounding

Each root skill must remain strongly grounded in its existing purpose rather than becoming a sterile workflow router.

The skills exist to surface a hidden attribute that mainstream search and ratings do not capture: whether a restaurant or bakery is ambitious enough to produce food from raw components rather than primarily assemble, reheat, or par-bake it. They use involuntary, observable tells from menus, reviews, sites, and operational cadence rather than relying on optimized marketing claims.

The unchanged model is:

- Scratch production is an eligibility gate.
- Interestingness distinguishes survivors for a frequent diner or buyer.
- Ratings are a quality floor, not the ranking signal.
- Broad, popularity-neutral discovery protects obscure specialists and underrepresented formats.
- Targeted popularity and quality discovery protects against missing prominent, new, renamed, or poorly tagged venues.
- The output is a trustworthy shortlist, not a claim to identify an objective winner.
- Missing evidence is a research state, never negative evidence.

The restaurant root must emphasize ambitious, genuinely scratch-made kitchens that are interesting to a frequent diner. The bakery root must emphasize production from raw components on-site, serious applicable craft, and resistance to frozen/par-bake economics while remaining open to specialist formats.

## Design principles

1. **Just-in-time instruction loading:** Before executing each phase, the primary agent must read that phase's file in full. Root summaries are orientation only.
2. **Explicit phase gates:** A phase cannot close until its required actions and artifacts are attested with concrete evidence.
3. **Stable role boundaries:** Research workers extract evidence only. The primary orchestrator alone classifies, scores, routes occasions, reasons about scarcity, and renders results.
4. **Canonical prompts:** Workers receive the supplied category prompt verbatim. The orchestrator may not improvise a substitute.
5. **Complementary discovery:** Popularity-neutral enumeration and adaptive targeted search are both mandatory discovery inputs.
6. **Semantic acceptance:** Worker returns are checked for evidence quality, not merely row count or schema shape.
7. **Targeted repair first:** When possible, incomplete records are repaired by messaging the original worker with specific defects.
8. **No false completion:** A polished final result cannot be rendered before every phase gate passes.
9. **Rubric preservation:** Operational hardening must not alter calibrated judgment.

## File architecture

The repository will retain two independently invocable skills and add shared operational phase references.

```text
restaurant-rubric/
├── SKILL.md
├── phase-4-worker-prompt.md
├── phase-6-scoring.md
└── phase-8-rendering.md

bakery-rubric/
├── SKILL.md
├── phase-4-worker-prompt.md
├── phase-6-scoring.md
└── phase-8-rendering.md

reference/
├── phase-1-scope-and-catchment.md
├── phase-2-candidate-discovery.md
├── phase-3-discovery-convergence.md
├── phase-4-evidence-research.md
├── phase-5-evidence-acceptance.md
├── phase-7-coverage-audit.md
└── shared-status-and-provenance.md
```

Exact filenames may be adjusted during planning if needed for unambiguous links, but the shared/category boundary is fixed.

### Root skill responsibilities

Each `SKILL.md` will:

- preserve strong category-specific mission grounding;
- preserve the full unchanged rubric and calibration material, either in place or through lossless category references;
- identify the primary agent as the sole orchestration and judgment authority;
- show the complete phase map;
- require the relevant phase file to be read in full immediately before execution;
- state that phase summaries are insufficient for execution;
- prohibit skipping, combining, reordering, or prematurely rendering phases;
- require a completion-gate attestation before the next phase is loaded;
- link to category-specific worker, scoring, and rendering instructions at the phases where they are needed.

The primary agent reads and executes phases. It does not spawn a fresh orchestrator for each phase. Subagents are used only for bounded research work explicitly assigned by a phase.

### Shared responsibilities

Shared references own mechanics that are identical across both domains:

- geographic scope and catchment declaration;
- multi-source discovery;
- adaptive local and multilingual query generation;
- candidate union, identity normalization, and deduplication;
- evidence states and provenance;
- worker-return acceptance and repair;
- coverage auditing and completion semantics.

### Category-specific responsibilities

Category files own:

- what scratch and ambition mean in that domain;
- category-specific involuntary tells and production vocabulary;
- relevant evidence sources and search variants;
- the exact worker prompt;
- scoring and disqualification rules;
- occasion routing, rare finds, and rendering.

## Phase execution model

The root skill must prominently state:

> Before executing each phase, you MUST read its phase file in full. The summaries in this root skill are orientation only and do not contain enough detail to execute correctly. Do not read all phase files once at the beginning and rely on memory; load each one fresh immediately before its phase.

Before advancing, the orchestrator must run that phase's completion gate. Each gate enumerates required actions, marks them complete or incomplete, and cites concrete counts, ledger states, queries, sources, or artifacts. A failed gate means continue the current phase.

### Phase 1 — Scope and catchment

Define the requested market using a real geographic boundary appropriate to the place: an administrative polygon, named neighborhoods, or an explicit derived catchment. Distinguish the requested market from adjacent markets.

**Gate:** Record the included area, exclusions, boundary method, and uncertainty.

### Phase 2 — Candidate discovery

Build a candidate union from complementary discovery tracks.

#### Track A: broad, popularity-neutral survey

Use OSM/Overpass or an equivalent broad map/place index across the full catchment. Retain full metadata and include category-adjacent tags so mistagged specialists are not lost. Partition large markets geographically when useful, then union the partitions.

#### Track B: adaptive targeted discovery

Generate queries using locally appropriate languages, scripts, neighborhoods, cuisine or bakery traditions, formats, regional specialties, marker items, production techniques, and words corresponding to quality, scratch production, ambition, artisan practice, chef- or baker-led work, awards, guides, and recent openings.

Required query families are universal; their wording is adaptive. The skill must not impose an English-only fixed query list on every market.

Targeted results are candidate leads only. A “best” list or search rank is never evidence that a venue qualifies.

#### Track C: visible-head challenge

Check reputable local food publications, major place-directory results, local guides and awards, roundups, and recent-opening coverage. This catches prominent or newly opened venues absent from the broad survey.

**Gate:** Confirm all required tracks ran, log sources and query families, and place every in-scope result in the candidate ledger.

### Phase 3 — Discovery convergence

Normalize names, addresses, domains, phones, aliases, renamed businesses, relocations, and branches. Deduplicate the union while preserving source provenance.

Inspect coverage across:

- geography and neighborhoods;
- languages and scripts;
- cuisines or bakery traditions;
- service formats;
- specialist and broad-format venues;
- established and recently opened businesses.

An empty coverage cell triggers a targeted query or an explicit explanation; it is not automatically populated or treated as failure.

Run an additional adaptive gap pass. Discovery may freeze only when that pass yields no new in-scope candidates or a concrete access/source limitation is recorded.

**Gate:** Report source counts, union size, duplicate count, new candidates found by each pass, last-pass yield, and remaining limitations.

### Phase 4 — Evidence research

Split candidates into bounded batches. Every worker receives the category's canonical prompt verbatim. Only placeholders explicitly declared in the prompt—such as catchment and candidate batch—may be substituted.

Workers extract evidence and provenance. They do not apply the rubric, score, classify, disqualify, rank, assign confidence verdicts, route occasions, or render recommendations.

**Gate:** Every candidate has a returned evidence record. This gate establishes return coverage, not acceptance.

### Phase 5 — Evidence acceptance and repair

The primary orchestrator personally inspects every record against the evidence contract. Acceptance is semantic, not a row-count check.

Reject records containing unsupported summaries, worker verdicts, missing quotations, asserted ratings, generic marketing adjectives used as production evidence, menu nouns mislabeled as process evidence, undocumented “none found” claims, or omitted source stages.

For each rejected venue, create a concrete defect list.

1. When the runtime supports messaging or resuming the original worker, request targeted repair from that worker first.
2. Ask for patches to affected venues only; preserve evidence already accepted.
3. Use a fresh worker when the original cannot be reached, failed or timed out, repeatedly violates the contract, or independent conflict verification is needed.
4. Fresh workers receive the canonical prompt verbatim.
5. Follow-up requests may identify missing evidence but may never ask workers to judge or score.

Records use explicit states such as `returned`, `repair-requested`, `conflict-verification`, `accepted`, and `exhausted-unavailable`.

**Gate:** Every candidate is evidence-accepted or legitimately exhausted-unavailable with a documented search trail. No thin record remains eligible for scoring.

### Phase 6 — Orchestrator scoring

The primary orchestrator reads the category scoring phase immediately before scoring and applies the unchanged rubric.

The orchestrator alone decides:

- scope and positive disqualification;
- scratch eligibility;
- S, I, E, R handling, G, and G′ as currently defined;
- scarcity and rare finds;
- tiers, ties, confidence, and occasions;
- final inclusion and rationale.

Every decision must link to accepted evidence. Unknown evidence must not become a zero or low craft score. A worker-produced score or verdict is invalid even if plausible.

**Gate:** Every decision has evidentiary support, no missing evidence was converted into a negative score, and no judgment was delegated.

### Phase 7 — Coverage audit

Challenge the frozen candidate set after scoring. Repeat adaptive targeted searches for visible favorites, scratch/ambitious venues, local-language terms, specialties, neighborhoods, relevant guides, and known-example patterns.

If a new venue appears, loop it through evidence research, acceptance, and scoring. Repeat the coverage audit until a pass yields no new in-scope candidate or a documented limitation prevents convergence.

**Gate:** Record audit queries and sources, additions found, resolution of every addition, last-pass yield, and limitations.

### Phase 8 — Rendering

Only after all prior gates pass may the orchestrator read the category rendering phase and produce the existing reader-facing output.

Rendering preserves the current occasion model, rare-find layer, audit material, rating treatment, ties, and plain-language presentation. Completion language distinguishes broad-survey coverage, targeted-search coverage, convergence evidence, and unavoidable limitations. It never equates “all OSM rows processed” with a complete real-world census.

**Gate:** Confirm all prior phases are closed, every rendered claim rests on accepted evidence, and limitations are stated at the correct level.

## Canonical worker contract

Each category's Phase 4 materials contain one exact prompt. The orchestrator must copy the prompt verbatim and substitute only declared variables. Recursive child workers receive the same canonical prompt verbatim.

The orchestrator must not:

- paraphrase or shorten the prompt;
- write a substitute brief;
- add `DQ`, eligibility, scores, rankings, tiers, or confidence verdicts;
- ask a worker to apply the rubric;
- delegate final interpretation or rendering.

If a runtime separates system and user prompts, the category file must state exactly which canonical block belongs in each.

### Required worker evidence

For every venue, workers return neutral, quotation-level evidence and provenance, including applicable fields for:

- canonical identity and address;
- source URL, source type, and access date;
- exact quotation and the neutral factual claim it supports;
- menu or product evidence;
- process and production evidence;
- ingredient and sourcing evidence;
- cadence, batching, seasonality, or sell-out evidence;
- review-text evidence using physical or operational descriptors;
- rating and count exactly as displayed, with platform;
- price and hours exactly as displayed;
- potentially adverse facts such as chain affiliation, commissary production, frozen product, closure, or wholesale operation—as quotations, not conclusions;
- sources and queries searched when a field is unavailable.

The category prompts supply domain-specific production vocabulary, anti-signals, source sequence, and controlled review lexicon.

### Forbidden worker output

Workers may not return:

- qualify/fail, `DQ`, or eligibility judgments;
- scratch, par-bake, assembly, ambition, or format conclusions;
- dessert-only or cuisine exclusions;
- S, I, E, G, G′, tiers, occasions, rankings, or final confidence;
- inferred ratings or counts;
- marketing adjectives presented as production evidence;
- “none found” without a search trail;
- unsupported summaries in place of quotations.

## Evidence semantics

The shared status/provenance reference defines the distinction between:

- evidence present and documented;
- evidence thin and requiring repair;
- evidence conflict requiring verification;
- evidence exhausted-unavailable after a demonstrated search trail;
- candidate unresolved because required research was not completed.

A menu or product noun can show what is sold but does not by itself establish how it is produced. It must be labeled product-only unless paired with process, physical, operational, or other rubric-permitted evidence.

Absence of process vocabulary is not evidence against scratch production. Missing evidence remains a research state. Positive disqualification requires positive evidence under the unchanged category rubric.

## Discovery semantics

The revised skills remove the operational claim that web/places search is “enrichment only, never discovery.” Instead:

- broad survey protects the long tail from popularity bias;
- targeted search protects the visible head, recent openings, renames, OSM omissions, and adjacent-category specialists;
- specialist, multilingual, neighborhood, marker-item, and local-list queries supplement both;
- union and deduplication precede evidence research;
- a post-scoring coverage challenge tests the frozen set again.

Neither track bounds reality alone. The final report states what each contributed and what limitations remain.

## Failure handling

- **Broad map source unavailable:** use alternate broad directories or partitioned queries, record the limitation, and do not call the result a census.
- **Local vocabulary uncertain:** derive terms from local sources and scripts rather than mechanically translating English.
- **Worker return thin:** message the original worker with venue-specific defects when possible; otherwise dispatch a fresh worker with the canonical prompt.
- **Sources conflict:** retain both claims with provenance and dates, then request targeted verification. Do not average or silently choose.
- **Evidence genuinely unavailable:** preserve `exhausted-unavailable` after a real search trail. Do not assign a low score from absence.
- **Coverage audit finds a venue:** reopen the necessary phases for that venue and repeat the audit.
- **Context or budget pressure:** reduce batch size or explicitly narrow scope. Never skip phases, infer the tail, or render prematurely.

## Regression scenarios

### Shared

1. A prominent venue absent from OSM is recovered by targeted discovery.
2. An obscure specialist absent from “best of” results survives broad enumeration.
3. A worker-created score or `DQ` is rejected.
4. A product-only return triggers targeted repair rather than a low scratch score.
5. Missing evidence remains unresolved or exhausted-unavailable, never negative evidence.
6. No polished final output is permitted before every phase gate passes.
7. A worker follow-up uses the original worker when messaging/resumption is available.
8. English-only discovery is rejected in a market where other local languages/scripts are relevant.

### Bakery

- **Chez Nibs:** category-adjacent and targeted discovery recover it despite a chocolate-shop classification; a worker cannot category-disqualify it.
- **All Purpose Bakehouse:** product nouns alone trigger evidence repair and review/press research; they do not reduce S.
- **Vosen's Bread Paradise:** sparse marketing jargon does not imply low craft, and rating conflicts are preserved and reconciled.
- **Ethnic or single-item specialist:** evaluated on the applicable production track rather than directory label or format.

### Restaurant

- A well-known ambitious scratch restaurant missing from OSM is recovered by targeted quality and scratch searches.
- A low-prominence ethnic or counter-service venue is not excluded because of format.
- A broad menu is judged from opened production evidence rather than reputation or cuisine prejudice.
- Local-language discovery adds candidates missed by English queries.

## Preservation constraints

The implementation must not change:

- S, I, E, R, G, or G′ definitions;
- weights, thresholds, formulas, or gates;
- calibration cases or their conclusions;
- occasion categories;
- rare-find logic;
- rating treatment;
- scoring bands, confidence semantics, or tie behavior;
- category-specific production criteria.

Moving rubric text to a category phase/reference must be lossless. Operational contradictions are corrected only where necessary to implement the approved multi-track discovery and phased execution model.

## Validation plan

Because the deliverables are instruction files, validation is structural and semantic:

1. Verify every root phase link resolves to an existing file.
2. Verify every phase defines inputs, mandatory actions, prohibitions, outputs, and a completion gate.
3. Verify both skills invoke shared phases in the same order.
4. Verify each category's canonical worker prompt contains no scoring or DQ request.
5. Verify root and phase instructions prohibit prompt paraphrase and delegated judgment.
6. Verify original-worker follow-up is preferred when messaging/resumption is available.
7. Verify no remaining operational text permits single-source completion or says targeted search is enrichment-only.
8. Diff all scoring and calibration material to confirm no semantic rubric change.
9. Tabletop the diary's regression scenarios against the phase gates.
10. Confirm rendering remains impossible until all gates have closed.

## Out of scope

- Changing the rubric or recalibrating scores.
- Adding executable validators, JSON-schema enforcement, or a software harness.
- Changing the consumer application in `scratch-food-finder`.
- Claiming exhaustive real-world discovery.
- Replacing the primary orchestrator with one agent per phase.
