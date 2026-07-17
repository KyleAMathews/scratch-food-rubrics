# Phase 3 — Discovery Convergence

Read `shared-status-and-provenance.md` in full immediately before executing this phase.

## Input

`{RUN_DIR}/02-discovery-ledger.md`, `{RUN_DIR}/02-query-log.md`, and `{RUN_DIR}/01-scope.md`.

## Normalize and deduplicate

1. Normalize names without discarding original or local-script forms.
2. Compare address, coordinates, phone, domain, branch, aliases, and known prior names.
3. Merge true duplicates into one canonical row while preserving every discovery source and query.
4. Keep distinct branches separate where production may differ.
5. Record closures, renames, relocations, and successors as identity facts only. Phase 6 owns decisions.
6. For branch families, create one shared brand packet plus distinct branch rows. Tag reusable facts `company-wide`; tag address, hours, rating, availability, production, or menu facts `branch-specific` or `store-local`; keep `historical` and `factory` scopes separate. Company-wide facts may be referenced, not duplicated, and never substitute for branch-local verification.

## Identity readiness before evidence research

Every frozen candidate receives one identity-readiness state before Phase 4:

- `ready`: named identity and provenance are sufficient for evidence research;
- `repair`: a likely venue whose name, address, branch, domain, successor, or catchment identity needs bounded correction;
- `quarantine`: no researchable identity yet, including an unresolved unnamed map object.

Validate a claimed official domain against the venue name plus address, phone, or another strong identity field; domain presence alone is not domain correctness. Shared domains, phones, addresses, similar names, and proximity may propose but never authorize a merge. The primary orchestrator records one relationship: `same physical venue`, `same concept, different branch`, `successor or historical identity`, `different venue`, or `unresolved`.

Successful repair returns a row to `ready`. Quarantine remains auditable, consumes no full evidence packet, and is neither a DQ nor a quality judgment.

## Coverage grid

Inspect the deduplicated union across:

- geography and neighborhood;
- language and script;
- cuisine or bakery tradition;
- service format;
- specialist versus broad format;
- established versus recently opened.

An empty cell is not proof that a venue exists. It triggers one targeted gap query or an explicit market-grounded explanation.

## Convergence pass

1. Run a fresh adaptive gap pass after deduplication; do not merely reread Phase 2 results.
2. Add every new in-scope candidate and repeat normalization.
3. Repeat until one complete pass yields zero new in-scope candidates, or a named source/access limitation prevents another pass.
4. Freeze the set for evidence research while allowing Phase 7 to reopen it later.

Do not use “complete census.” Describe the source convergence actually achieved. Write the canonical, deduplicated, frozen ledger to `{RUN_DIR}/03-candidate-ledger.md`, including aliases and all discovery provenance. Update the manifest to `phase-3-complete` only after the gate passes.

## Completion gate

- [ ] Canonical union count reported.
- [ ] Duplicate, alias, and branch count reported.
- [ ] All discovery provenance survived merges.
- [ ] Every coverage-grid dimension was inspected.
- [ ] Empty or suspicious cells received a query or explanation.
- [ ] Last complete gap-pass yield is reported.
- [ ] Last pass yielded zero new candidates, or a precise source/access limitation is recorded.
- [ ] Frozen candidate IDs are in `03-candidate-ledger.md`.
- [ ] Every frozen row has an identity-readiness state; all `repair` work is resolved or recorded, and every `quarantine` row remains auditable without entering Phase 4.
- [ ] Every Phase 3 artifact is inside `{RUN_DIR}`.
