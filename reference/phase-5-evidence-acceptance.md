# Phase 5 — Evidence Acceptance and Repair

Read `shared-status-and-provenance.md` and the invoked category's `phase-4-worker-prompt.md` in full immediately before reviewing returns.

## Input

Every raw return under `{RUN_DIR}/04-worker-returns/` and `{RUN_DIR}/03-candidate-ledger.md` with original worker references.

## Semantic acceptance review (primary orchestrator only)

Inspect every venue, not a sample and not merely row counts. For each required field verify:

- exact quotation or literal value where available;
- neutral factual claim fidelity to the quotation;
- source URL, source type, and access date;
- required source sequence and search trail;
- literal rating, count, and platform rather than an assertion;
- product nouns labeled `product-only` unless separate process, physical, or operational evidence supports more;
- no worker verdict, score, DQ, eligibility, scarcity, tier, occasion, or final confidence;
- unavailable fields have a demonstrated search trail rather than a bare “none found.”

A generic adjective such as `artisan`, `homemade`, `authentic`, `fresh`, or `traditional` is a quotation but not production evidence. Preserve it without promoting it.

## Identity-first direct-place rating verification

Before any rating is accepted or declared exhausted, build an identity tuple: canonical name, aliases, exact address, phone, branch, category, and storefront or service-area status. Then:

1. Open the direct platform place record and query exact name; name + exact address; alias + address or phone; and, for service-area producers, name + locality.
2. Record the returned identity, category, literal rating, count, stable place ID, exact query, URL, and access date.
3. Identity-gate the result before attaching it to the candidate. Classify each checked platform as `exact-rated`, `exact-no-rating`, `no-exact-record`, or `identity-conflict`.
4. If an exact record has no rating, run a secondary exact-identity rating search. Check current operating status separately; never infer status from rating presence.
5. `exhausted-unavailable` is valid only after the full query, identity, and rejection log is complete. Immediately before Phase 8, rerun this sweep for every scratch-verified, rating-unconfirmed candidate.

A generic web query described as “Google/Maps-oriented” is not a direct-place check.

## Evidence scope for branch families

Label reusable evidence `company-wide`; label address, hours, rating, availability, production, or menu evidence `branch-specific` or `store-local` as appropriate. `historical` and `factory` are separate scopes. Company-wide evidence may be referenced from multiple branch records rather than copied, but it cannot establish a branch-specific fact. Preserve distinct candidate IDs and require branch-local identity and rating verification.

## Defect list

For every non-accepted venue, write concrete defects keyed by field, for example:

- `production`: product noun only; review/local-press process pass absent;
- `rating`: count or platform missing;
- `search_trail`: “none found” lists no sources or queries;
- `role_boundary`: worker supplied a DQ or score instead of raw facts;
- `provenance`: quotation lacks URL or access date.

## Repair routing

1. **Original worker first when available:** message or resume the worker recorded on the venue. Request patches only for named venues and defects. Preserve already accepted fields.
2. A repair message may identify defects and requested evidence fields. It must not ask for judgment or rewrite the canonical role.
3. **Fresh worker fallback:** use a new worker only when the runtime cannot message or resume the original, the original failed or timed out, repeated repair still violates the contract, or independent conflict verification is required.
4. A fresh worker receives the full category canonical prompt verbatim, with only declared substitutions.
5. For source conflicts, preserve both claims and dates, mark `conflict-verification`, and obtain targeted independent or direct-source evidence. Never average or silently choose.
6. `exhausted-unavailable` is terminal only after the category prompt's required source sequence is demonstrated in the search trail.
7. Review every patch again. A patch is not self-accepting.

Write accepted evidence and per-field states to `{RUN_DIR}/05-evidence-ledger.md`. Append every defect, repair message, worker response reference, conflict action, and acceptance result to `{RUN_DIR}/05-repair-log.md`. Update the manifest to `phase-5-complete` only after the gate passes.

## Completion gate

- [ ] Every returned record was inspected semantically by the primary orchestrator.
- [ ] Every rejected venue has a field-specific defect list.
- [ ] Original workers were messaged or resumed first wherever supported.
- [ ] Every fresh-worker dispatch used the canonical prompt verbatim.
- [ ] Conflicts preserve both claims and received verification.
- [ ] Every accepted claim has required provenance.
- [ ] Every exhausted field has the required source and query trail.
- [ ] No `product-only`, thin, conflicting, unsearched, or worker-verdict row is treated as scoring evidence.
- [ ] Every candidate is `evidence-accepted` or legitimately `evidence-exhausted-unavailable`.
- [ ] `05-evidence-ledger.md` and `05-repair-log.md` contain the complete Phase 5 history inside `{RUN_DIR}`.
