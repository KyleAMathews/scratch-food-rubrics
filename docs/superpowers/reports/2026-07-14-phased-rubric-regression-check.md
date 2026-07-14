# Phased Rubric Regression Check

**Date:** 2026-07-14  
**Baseline:** `572f1d6`

## Structural audit

```text
bakery-rubric/SKILL.md: 8 phases; all links live
restaurant-rubric/SKILL.md: 8 phases; all links live
reference/phase-1-scope-and-catchment.md: completion gate present
reference/phase-2-candidate-discovery.md: completion gate present
reference/phase-3-discovery-convergence.md: completion gate present
reference/phase-4-evidence-research.md: completion gate present
reference/phase-5-evidence-acceptance.md: completion gate present
reference/phase-7-coverage-audit.md: completion gate present
```

## Role-boundary audit

```text
Canonical prompt controls:
bakery-rubric/phase-4-worker-prompt.md:3:The primary orchestrator MUST copy the canonical block below verbatim. It may substitute only `{CATCHMENT}`, `{ACCESS_DATE}`, and `{CANDIDATE_BATCH}`. Do not add a DQ, score, eligibility, confidence, tier, or ranking field. If a runtime has separate system and user prompts, use the entire block as the worker's initial user message; a system prompt may only state that the worker is a bounded evidence retriever and must follow the user message exactly.
bakery-rubric/phase-4-worker-prompt.md:5:## Canonical block — copy verbatim
bakery-rubric/phase-4-worker-prompt.md:39:HARD PROHIBITIONS:
bakery-rubric/phase-4-worker-prompt.md:47:If this batch has more than 15 candidates and child workers are available, split it into batches of 10–15 and pass THIS ENTIRE PROMPT verbatim, substituting only the three declared placeholders. Return all child records without adding judgments.
restaurant-rubric/phase-4-worker-prompt.md:3:The primary orchestrator MUST copy the canonical block below verbatim. It may substitute only `{CATCHMENT}`, `{ACCESS_DATE}`, and `{CANDIDATE_BATCH}`. Do not add a DQ, score, eligibility, confidence, tier, or ranking field. If a runtime has separate system and user prompts, use the entire block as the worker's initial user message; a system prompt may only state that the worker is a bounded evidence retriever and must follow the user message exactly.
restaurant-rubric/phase-4-worker-prompt.md:5:## Canonical block — copy verbatim
restaurant-rubric/phase-4-worker-prompt.md:41:HARD PROHIBITIONS:
restaurant-rubric/phase-4-worker-prompt.md:49:If this batch has more than 15 candidates and child workers are available, split it into batches of 10–15 and pass THIS ENTIRE PROMPT verbatim, substituting only the three declared placeholders. Return all child records without adding judgments.
Original-worker repair controls:
36:1. **Original worker first when available:** message or resume the worker recorded on the venue. Request patches only for named venues and defects. Preserve already accepted fields.
38:3. **Fresh worker fallback:** use a new worker only when the runtime cannot message or resume the original, the original failed or timed out, repeated repair still violates the contract, or independent conflict verification is required.
Obsolete discovery contradiction scan: clean
Placeholder scan: clean
Formatting of newly authored operational files:
Checking formatting...
All matched files use Prettier code style!
```

## Rubric-preservation audit

```text
PRESERVED: **Three axes**
PRESERVED: #### Rare-finds layer
PRESERVED: ## Why the bakery model differs from the restaurant one
PRESERVED: ## Marker-item seed search (bakery)
PRESERVED: **Three orthogonal axes**
PRESERVED: #### Rare-finds layer
PRESERVED: ## Why K, not N (the combinatorial correction)
PRESERVED: ## Marker-item seed search (likelihood-ratio method)
PRESERVED: bakery-rubric/SKILL.md sharing
PRESERVED: restaurant-rubric/SKILL.md sharing
```

## Tabletop regressions

| Scenario                                          | Required route                                                                       | Result |
| ------------------------------------------------- | ------------------------------------------------------------------------------------ | ------ |
| Prominent venue absent from OSM                   | Phase 2 Track B/C adds it                                                            | PASS   |
| Obscure specialist absent from best lists         | Phase 2 Track A preserves it                                                         | PASS   |
| Chez Nibs has a chocolate-shop label              | Bakery adjacent-category discovery adds it; worker cannot DQ by category             | PASS   |
| All Purpose returns only product nouns            | Phase 5 marks product-only and messages the original worker for review/press repair  | PASS   |
| Vosen's has sparse jargon and conflicting ratings | Missing jargon remains a research state; both ratings are preserved for verification | PASS   |
| Worker returns DQ or scores                       | Phase 5 rejects the record even when plausible                                       | PASS   |
| Original worker returned a thin row               | Phase 5 messages or resumes the original worker first when supported                 | PASS   |
| Counter-service ethnic restaurant                 | Restaurant discovery preserves format; only orchestrator production evidence decides | PASS   |
| Local-language venue absent from English search   | Phase 2 multilingual track and Phase 7 audit can add it                              | PASS   |
| Late candidate appears in coverage audit          | Phase 7 loops it through Phases 4–6 and repeats                                      | PASS   |
| Attempt to render with unfinished tail            | Root hard stop and Phase 8 prerequisite forbid output                                | PASS   |
| OSM processed but targeted pass skipped           | Phase 2 and Phase 7 gates fail                                                       | PASS   |

## Preservation conclusion

All extracted scoring, calibration, marker-item, occasion, rare-find, audience-vocabulary, and sharing blocks match the baseline byte for byte. v8.9 changes execution architecture and discovery only; the calibrated rubrics are unchanged.
