---
name: interactive-results
description: Turn a completed bakery or restaurant rubric run into a validated local faceted list-and-map website; use only after Phase 8 and publish only on a separate explicit request.
---

# Interactive Results

Invoke as `/interactive-results <RUN_DIR>`. The path is mandatory: if it is missing, ask the user for the exact run directory and stop. Never guess, infer, auto-select, or create a run directory.

This workflow is **snapshot-only**. It transforms an already completed bakery or restaurant run; it must not perform fresh web lookup, research, scoring, rating, access, location, recommendation, or evidence work. Never change an orchestrator decision. If the snapshot cannot support a field, leave it null, omit it with a recorded reason, or ask about a consequential ambiguity as defined below.

## Hard-gated lifecycle

1. Resolve the user-supplied path and keep every durable output inside it.
2. Read `00-run-manifest.md`. Require Phase 8 completion (`complete`) and required artifacts `05-evidence-ledger.md`, canonical `06-decisions.json`, and `08-results.md`. Reject an incomplete or category-unknown run.
3. Validate `06-decisions.json` against `decision-schema.json`, its source references, IDs, merge targets, and manifest metadata. It is the only canonical decision ledger.
4. For a legacy completed run without JSON, perform the one-time migration below. Never treat independently authored `06-decisions.md` as a second authority.
5. Build a snapshot projection accounting for every canonical ID as Practical, Audit, or omitted with a reason. Prefer descriptions already written in `08-results.md`; otherwise make a faithful concise summary only from canonical rationale and accepted evidence.
6. Present the required facet-design checkpoint and stop for approval, revision, or the exact instruction `use your defaults`.
7. Write the approved `interactive-results-projection.json`, validate it against `interactive-schema.json`, then run the deterministic generator. Do not rewrite `template.html` or application JavaScript per run.
8. Serve locally and complete static plus browser validation at desktop and mobile sizes.
9. Write `interactive-results-validation.json`, then update the manifest with artifact paths, schema versions, hashes, generation timestamp, browser results, and final status. A failure cannot be recorded as complete.
10. Return local paths and a validation summary. Publication is a separate permission boundary.

## Legacy migration

If `06-decisions.json` is absent but the manifest proves a completed legacy run, transform `06-decisions.md`, `05-evidence-ledger.md`, `08-results.md`, and the manifest once. This is an agent-guided migration, not a claim that arbitrary Markdown has a deterministic parser.

First write `{RUN_DIR}/interactive-results-migration.json` containing parsed rows, source references, unresolved fields, duplicate or missing IDs, and a `consequential_ambiguities` list. Stop and ask only when ambiguity affects identity, disposition, Practical eligibility, score/rating display, or accepted map location. Do not research the answer. After resolution, write canonical JSON atomically only when schema and cross-record invariant validation pass, then record the migration report and canonical hash in the manifest.

## Practical, Audit, and location rules

- **Practical** contains all currently obtainable qualifying records in the canonical snapshot, including stable walk-in, preorder, market, delivery, or other accepted acquisition paths. It is not merely a top-three display.
- **Audit** contains non-Practical canonical records useful for transparency: filtered, disqualified, unavailable, unresolved, unconfirmed, or duplicate dispositions. Use compact rows. Use `Directions` only for Practical records with an accepted address. Otherwise, `Find on Google Maps` may search by canonical name plus run scope; label it as a search, never as an accepted location.
- **Omitted** is allowed only with a per-ID reason; populations must not overlap.
- Use only accepted business addresses and coordinates from `06-decisions.json`. Never geocode, repair, or guess coordinates. A no-coordinate corpus must render as list-only.
- Ratings, scores, access, names, and dispositions must match the canonical snapshot exactly.

## Required facet-design checkpoint

Before generation, show a proposed facet table with each facet, controlled values, representative venues, aliases/normalization, local extensions, and rejected sparse or overlapping values. Cover shared region, access, occasion, and status dimensions, plus evidence-supported category dimensions such as specialty for bakeries or cuisine/format for restaurants. Do not invent unsupported labels.

Ask the user to approve, revise, or reply **`use your defaults`**, and stop. Approval is required even when the defaults appear obvious. After approval, account explicitly for every canonical ID and freeze the projection; no fresh research follows.

## Deterministic generation

From the repository root, run:

```bash
python3 interactive-results/generate.py \
  --decisions "$RUN_DIR/06-decisions.json" \
  --projection "$RUN_DIR/interactive-results-projection.json" \
  --template interactive-results/template.html \
  --output "$RUN_DIR/index.html" \
  --validation-output "$RUN_DIR/interactive-results-validation.json" \
  --generated-at '<ISO-8601 timestamp>'
```

The initial report is a static validation result. Regenerate with the same inputs/timestamp and verify an identical output hash. Syntax-check the inline application script with Node and parse the HTML with Python's `html.parser`.

## Local browser validation

Serve the generated file over HTTP, not `file://`:

```bash
python3 -m http.server 8765 --directory "$RUN_DIR"
```

Follow `interactive-results/tests/browser-checklist.md`. Browser validation is mandatory at 1440×900 and 390×844 and must test real search, facets, alternate counts, rating floor, sorts, Practical/Audit modes, localStorage shortlist persistence, map/list navigation, drawers, keyboard close/focus behavior, independent scrolling, and list-only fallback. Capture page errors and screenshots. HTTP 200 alone is insufficient.

Merge browser outcomes into `interactive-results-validation.json`, set final status only after every required assertion passes, and include canonical decision, projection, template, and output SHA-256 hashes. Update `00-run-manifest.md` only afterward.

## Publication boundary

Default delivery is local `index.html`; there is no automatic publication, gist creation, upload, or network sharing. At completion, you may offer:

```text
/gisthost "$RUN_DIR/index.html"
```

Do not invoke `/gisthost` unless the user makes a new, separate explicit request.
