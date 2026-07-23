# Fuzzy entity clustering: code proposes, orchestrator decides

## Contract

`02-source-data/propose-identity-clusters.rb` is a deterministic candidate generator. It never merges records. Its output provides pairwise signals and empty `review_decision` / `review_note` fields for orchestrator adjudication.

Allowed decisions:

- `same-venue`: duplicate records for one physical venue; merge identity and provenance.
- `same-concept-branches`: share concept-level evidence and retain the closest branch unless local variation is documented.
- `different`: similar records that must remain separate.
- `unresolved`: repair identity before evidence work.

## Algorithm

1. Normalize Unicode, punctuation, case, `&`/`and`, and low-information venue suffixes.
2. Build order-independent name token sets from names and aliases.
3. Normalize phone numbers and domains; retain address and coordinates.
4. Block comparisons by shared token signature, phone, domain, address, or uncommon name token. This avoids all-pairs comparison.
5. Calculate token-set Dice similarity and geographic distance.
6. Propose a pair only when supported by name agreement, or by a similar name plus strong phone/domain/address/proximity evidence.
7. Sort the review queue by confidence; do not auto-merge even `high` pairs.

## Prototype result

Input: 1,680 evidence candidates.

- Initial permissive pass: 344 proposals. This was rejected as too noisy; shared domains frequently represented hotels, resorts, restaurant groups, or generic infrastructure.
- Tightened pass: **53 proposals**: 1 high, 44 medium, and 8 review.
- The queue includes the known `Cafe del Barrio` / `Del Barrio Cafe` duplicate, showing that the blocking strategy recovers the motivating case.
- The queue also deliberately includes likely same-concept branches and false positives for manual distinction. For example, `Copper Common` / `The Copper Onion` share an address but are distinct concepts; a merge based only on location would be wrong.

The 53-pair queue is small enough for manual adjudication and far cheaper than giving all 1,680 records to a model for pairwise comparison. The script's JSON output is reproducible from the frozen input and can be piped to a review artifact after decisions are filled.

## Adjudication result

All 53 proposed pairs were reviewed by the primary orchestrator:

- 8 same-venue pairs, including one verified relocation;
- 28 same-concept branch-pair relationships, forming 27 concept clusters because three Roxberry records were connected;
- 14 false-positive/different-venue pairs; and
- 3 unresolved pairs involving unnamed OSM records.

The reviewed relationships removed 36 redundant records and reduced the Phase 4 evidence population from **1,680 to 1,644**. No unresolved or different pair was removed. Full decisions are in `04-reviewed-identity-clusters.json`; the revised population is `02-source-data/evidence-candidates-after-reviewed-clustering.json`.

This is a modest 2.1% population reduction, but it is reusable, deterministic preprocessing and prevents duplicated evidence packets without introducing cuisine or format bias.

## Invocation

```sh
ruby 02-source-data/propose-identity-clusters.rb \
  02-source-data/evidence-candidates-after-rules-1-3.json
```

Run from the run directory. Output is JSON on stdout.

## General skill improvement

Phase 3 should specify this separation of responsibilities:

- code performs normalization, blocking, similarity calculation, and proposal generation;
- the primary orchestrator reviews every proposal and assigns the relationship type;
- only reviewed `same-venue` and `same-concept-branches` decisions change the canonical/evidence population;
- the review artifact preserves reasons, distances, similarity values, and the decision.

This reduces tokens without delegating judgment or allowing a fuzzy matcher to silently erase unusual venues.
