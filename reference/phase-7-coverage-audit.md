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

Compare every result to the canonical ledger by name, address, domain, phone, alias, and successor relationship.

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
- [ ] Last full audit-pass yield is reported.
- [ ] Last pass yielded zero new candidates, or a precise limitation is stated.
- [ ] No recommendation has been rendered before this gate closes.
- [ ] The complete audit history is in `{RUN_DIR}/07-coverage-audit.md`; no Phase 7 artifact is outside the run directory.
