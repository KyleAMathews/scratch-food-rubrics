# Phase 7 — Coverage Audit

Read `shared-status-and-provenance.md`, `phase-2-candidate-discovery.md`, and the invoked category's `discovery-reference.md` in full immediately before executing this phase.

## Input

`{RUN_DIR}/03-candidate-ledger.md`, `{RUN_DIR}/06-decisions.md`, and `{RUN_DIR}/02-query-log.md`.

## Mandatory challenge

Run a new omission challenge; do not merely assert that Phase 2 was broad. Include:

- visible favorites and locally prominent venues;
- locally natural best, scratch, ambitious, chef-led or baker-led, artisan, guide, and award terms;
- relevant local languages and scripts;
- neighborhoods, cuisines or bakery traditions, specialists, adjacent categories, and marker items;
- recent openings, renames, relocations, markets, pop-ups, cottage/preorder, and informal formats where relevant;
- known-example challenges from the category discovery reference.

Compare every result to the canonical ledger by name, address, domain, phone, alias, and successor relationship. Repeat the bounded item-roundup reconciliation from Phase 2 for relevant current sources and record the final source that adds zero new identities.

## User-reported omission falsification

Treat a user-reported omission or locally known missing venue as a falsification signal, not a one-off insertion:

1. Add the named in-scope venue with discovery provenance and run it through Phases 4–6.
2. Identify the discovery route that should have found it, including the relevant product × adjacent-format family, local terms, and item-roundup family.
3. Rerun that targeted route and reconcile every identity named by the relevant qualifying sources.
4. Loop every resulting addition through Phases 4–6, then resume the full Phase 7 challenge until a complete pass yields zero new in-scope candidates.

Record the miss, failed route, rerun queries and sources, reconciliation actions, and resulting additions in the coverage audit.

## Loop-back rule

For each new in-scope venue:

1. Add it as `coverage-addition` with discovery provenance.
2. Run it through Phase 4 evidence research.
3. Run Phase 5 acceptance and repair.
4. Run category Phase 6 scoring.
5. Repeat this Phase 7 audit after resolving every addition.

Stop only when a full audit pass yields zero new in-scope candidates or a precise source/access limitation prevents completion. Never call this an exhaustive real-world census. Write every audit pass, exact query and source, candidate addition, loop-back status, last-pass yield, and limitation to `{RUN_DIR}/07-coverage-audit.md`. Update the manifest to `phase-7-complete` only after the gate passes.

## Completion gate

- [ ] Fresh challenge queries and sources are logged.
- [ ] Visible-head, scratch/ambition, multilingual, geographic, specialist, marker, and recent-opening families were covered.
- [ ] Every new candidate looped through Phases 4–6.
- [ ] Every qualifying item-roundup venue was identity-reconciled, and the final independent qualifying source added zero new identities or a precise limitation is recorded.
- [ ] Every user-reported omission received a documented discovery-route falsification pass and all resulting additions looped through Phases 4–6.
- [ ] Last full audit-pass yield is reported.
- [ ] Last pass yielded zero new candidates, or a precise limitation is stated.
- [ ] No recommendation has been rendered before this gate closes.
- [ ] The complete audit history is in `{RUN_DIR}/07-coverage-audit.md`; no Phase 7 artifact is outside the run directory.
