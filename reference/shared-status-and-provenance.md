# Shared Status, Provenance, and Completion Contract

This file defines the shared ledger vocabulary for both food rubrics. Category scoring semantics remain in each category's Phase 6 file.

## Run workspace (mandatory)

Phase 1 creates exactly one dedicated directory for the run in the agent's current working directory:

```text
<YYYY-MM-DD>-<location-slug>/
```

Use the agent's local current date and a filesystem-safe slug derived from the user's requested location. Preserve enough geography to disambiguate the place (for example, `2026-07-14-salt-lake-valley-utah`). Lowercase, collapse whitespace and punctuation to hyphens, trim repeated hyphens, and retain Unicode characters when transliteration would lose identity. If that directory already exists, create `-2`, then `-3`, and so on. **Never reuse or overwrite a prior run directory.**

Every durable artifact produced during the run MUST live inside this directory. Temporary tool files may use system temporary storage only while a command runs; copy any evidence, result, log, or data needed later into the run directory immediately. Do not scatter run files through the repository or current working directory.

The standard layout is:

```text
<run-directory>/
├── 00-run-manifest.md
├── 01-scope.md
├── 02-discovery-ledger.md
├── 02-query-log.md
├── 02-source-data/
├── 03-candidate-ledger.md
├── 04-worker-returns/
├── 05-evidence-ledger.md
├── 05-repair-log.md
├── 06-decisions.md
├── 07-coverage-audit.md
└── 08-results.md
```

A phase may add clearly named supporting files under the same directory, but it MUST NOT rename or omit the standard artifact for that phase. All phase files refer to this path as `{RUN_DIR}`.

## Non-negotiable semantics

- Missing evidence is a research state, never evidence against scratch production.
- A product or menu noun says what is sold; it does not establish how it was produced.
- A disqualification requires positive evidence under the unchanged category rubric.
- Search rank, guide inclusion, popularity, service format, cuisine, language, and directory category never establish scratch production.
- Every factual claim retains its source URL, source type, access date, and exact quotation when one is available.

## Candidate ledger

Keep one canonical row per venue with: `candidate_id`; canonical name; address; phone; domain; aliases and local-script names; category; every discovery source and exact query; geography; language or script; cuisine or tradition; service format; specialist or broad format; established or new status; candidate and evidence states; original `worker_ref`; evidence record; and orchestrator-only decision record. Deduplication merges provenance; it never discards it.

## Candidate states

- `candidate-discovered`: in scope and awaiting evidence research.
- `evidence-researching`: assigned to a worker or being researched serially.
- `evidence-returned`: a record exists but has not passed acceptance.
- `repair-requested`: the original worker has been asked for a venue-specific patch.
- `conflict-verification`: contradictory sources need targeted verification.
- `evidence-accepted`: required evidence is documented or legitimately exhausted.
- `evidence-exhausted-unavailable`: required evidence is absent after the required source sequence, with the full search trail recorded.
- `orchestrator-decided`: the primary orchestrator applied the unchanged rubric.
- `coverage-addition`: discovered after the initial freeze and looping through Phases 4–6.
- `rendered`: included after every gate passed.

`unresolved`, `thin`, and a blank field are non-terminal states.

## Per-field evidence states

- `documented`: a literal value or quotation was retrieved from a named source.
- `product-only`: what is sold is known, but process inference is forbidden.
- `thin-repair-required`: quotation, provenance, or source-stage requirements failed.
- `conflicting`: current sources materially disagree; preserve both pending verification.
- `exhausted-unavailable`: the required source sequence was completed and the search trail recorded.
- `unsearched`: required work was not completed; this is never terminal.

## Number provenance

Every numeric value is `documented`, `estimated` by the primary orchestrator where the unchanged rubric permits estimation, or `unverified`. Never average conflicting ratings. Preserve each literal value, count, platform, and retrieval date.

## Worker-return rule

A returned row proves only that a worker responded. The primary orchestrator checks every venue semantically. Row-count validation is forbidden.

## Completion-gate protocol

Before opening the next phase:

1. Enumerate every item in the current phase's printed gate.
2. Mark each item `✅` or `❌`.
3. Cite concrete evidence: counts, queries, candidate IDs, worker references, records, or decisions.
4. If any item is `❌`, remain in the current phase and finish or repair it.
5. Show the concise checklist to the user without rendering recommendations.

A documented limitation satisfies only a gate item that explicitly permits one. It never silently waives another requirement.
