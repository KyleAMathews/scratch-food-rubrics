# Interactive Results Skill Design

**Date:** 2026-07-18
**Status:** Approved for implementation planning
**Scope:** A separate post-run skill that converts completed bakery and restaurant rubric runs into validated, local, interactive place-finder websites

## Goal

Create a reusable `/interactive-results <RUN_DIR>` skill that consumes a completed bakery or restaurant run, guides the user through a market-specific facet design checkpoint, and deterministically generates a validated single-file `index.html` explorer without changing the run’s evidence, decisions, scores, or recommendations.

## Product boundary

The canonical rubric output remains the completed run and its reader-facing report. The website is a derived snapshot explorer.

The skill is separate from the bakery and restaurant rubric skills. After Phase 8 completes, each rubric may suggest `/interactive-results <RUN_DIR>`, but website generation begins only after explicit user approval. It never runs automatically.

Local generation is the default outcome. Public publication is a separate explicit action through `/gisthost`; successful local generation does not authorize publication.

The first version supports both bakery and restaurant runs through one shared interaction model, shared schemas, and category-specific labels, facet defaults, and restrained visual theming.

## Repository structure

Add one self-contained skill directory:

```text
interactive-results/
├── SKILL.md
├── decision-schema.json
├── interactive-schema.json
├── generate.py
├── template.html
└── tests/
```

Responsibilities:

- `SKILL.md` orchestrates run validation, legacy migration, projection design, the required user facet checkpoint, generation, browser validation, and the optional publication handoff.
- `decision-schema.json` defines the canonical Phase 6 machine-readable decision ledger shared by bakery and restaurant runs.
- `interactive-schema.json` defines the derived website projection and approved facet configuration.
- `generate.py` validates schemas and cross-record invariants, safely serializes data, injects declarative category configuration into the template, and emits one self-contained HTML file.
- `template.html` owns all stable HTML, CSS, and JavaScript interactions. Agents do not rewrite its application code per run.
- `tests/` contains schema fixtures, generator tests, migration fixtures, and browser-level interaction tests or test guidance appropriate to the repository runtime.

Do not split this feature across shared reference directories before another consumer exists. The only core-rubric changes are the canonical decision-ledger handoff and a Phase 8 suggestion for the optional skill.

## Invocation and lifecycle

The explicit invocation is:

```text
/interactive-results <RUN_DIR>
```

If no run directory is provided, ask for it. Do not guess a run from the current directory when multiple candidate runs exist.

The skill executes this lifecycle:

1. Validate that the directory is a completed bakery or restaurant run.
2. Load canonical `06-decisions.json`, or migrate a legacy Markdown run once.
3. Verify the canonical decision ledger and its relation to the manifest and evidence artifacts.
4. Build a proposed Practical/Audit website projection without fresh research.
5. Inspect the corpus and propose controlled market-specific facets.
6. Stop for the required user facet-design checkpoint.
7. Write and validate `interactive-results-data.json` after approval.
8. Deterministically generate `{RUN_DIR}/index.html`.
9. Serve and browser-test the site locally at desktop and mobile sizes.
10. Write `interactive-results-validation.json` and update the run manifest.
11. Report the local artifact and offer, but do not invoke, `/gisthost`.

The skill must stop at any failed validation. It must not silently omit ambiguous or invalid records to produce a visually complete page.

## Snapshot-only evidence rule

Version 1 is snapshot-only.

The skill uses accepted evidence already present in the completed run. It performs no fresh web lookup and may not change:

- identity decisions;
- accepted business addresses or coordinates;
- current-access evidence;
- scores or score provenance;
- ratings or rating provenance;
- dispositions or tiers;
- occasion or rare-find decisions;
- recommendation rationale.

Missing accepted coordinates produce an unpinned but searchable record. Missing current-access evidence routes the record out of Practical mode rather than triggering research. If the snapshot is too stale for the user’s purpose, recommend refreshing the underlying rubric run before generating the website.

Every generated page shows the run snapshot date and relevant evidence/access dates so the user can judge freshness.

## Canonical Phase 6 decision ledger

### Authority

`06-decisions.json` becomes the canonical Phase 6 decision ledger for both bakery and restaurant runs.

`06-decisions.md` is optional and generated from JSON when a human-readable audit view is useful. It is never independently authored as a second source of truth. Phase 8 and the interactive-results skill consume JSON only.

The run manifest records:

- `06-decisions.json` as canonical;
- its schema version and content hash;
- `06-decisions.md` as derived when present;
- the validator result and generation timestamp.

### Top-level contract

The decision ledger includes:

```json
{
  "schema_version": "1.0",
  "category": "bakery",
  "run_id": "2026-07-14-salt-lake-valley-park-city-heber-midway-utah",
  "generated_at": "2026-07-18T00:00:00Z",
  "source_artifacts": {
    "manifest": "00-run-manifest.md",
    "evidence": "05-evidence-ledger.md"
  },
  "records": []
}
```

`category` is exactly `bakery` or `restaurant`. Source paths are run-directory-relative and must not escape the run directory.

### Record contract

Each canonical record contains fields appropriate to its disposition, including:

- canonical candidate ID;
- canonical display name;
- aliases and branch label when present;
- accepted business address;
- accepted latitude and longitude when present;
- disposition and primary reason;
- normalized score values and provenance when scoreable;
- rating value, count or count state, platform, and direct/provisional provenance;
- tier and ranking eligibility;
- occasion memberships and rare-find memberships when decided;
- access format, current acquisition state, and evidence date;
- canonical merge target when applicable;
- structured rationale;
- source references into accepted run artifacts.

The schema uses conditional requirements by disposition rather than requiring every field to be filled with meaningless nulls. A merge target must resolve to exactly one canonical record.

The ledger does not contain website summaries, facet labels, styling, generated badges, or shortlist state.

### Phase 6 validation

Before Phase 6 closes:

- every canonical candidate appears exactly once;
- all required Phase 7 additions appear;
- merge targets resolve;
- score and disposition invariants pass;
- rating and access provenance is structurally valid;
- source references resolve inside the run directory;
- JSON schema validation passes;
- the run-local Phase 6 integrity validation and JSON population agree.

The rubric cannot advance to Phase 8 if the canonical JSON is absent or invalid.

### Optional Markdown audit view

A deterministic formatter may generate `06-decisions.md` from JSON. The view may contain tables and narrative rationale, but all values derive from JSON. Regeneration replaces the view; manual edits are not authoritative.

## Legacy-run migration

Older completed runs without `06-decisions.json` are supported through a one-time migration.

The migration reads existing decision, evidence, report, and correction artifacts and produces:

- a candidate `06-decisions.json`;
- a migration report listing parsed records, unresolved fields, duplicate or missing IDs, and ambiguous dispositions, scores, ratings, access states, identities, or locations.

Migration behavior:

1. Parse only supported facts present in the existing artifacts.
2. Preserve source references for every migrated decision field.
3. Stop on consequential ambiguity rather than infer a value.
4. Ask the user only about ambiguities that affect identity, disposition, practical eligibility, score/rating display, or map location.
5. Validate the completed JSON against the canonical schema and population invariants.
6. Save the canonical JSON and record the migration in the manifest.

Migration performs no fresh research. It cannot repair stale facts by searching the web. Once migration succeeds, all later website runs use the canonical JSON path.

## Reader-facing description source

`08-results.md` is the preferred source for concise reader-facing descriptions because it already translates internal rubric decisions into plain language.

When a Practical record has no usable description in `08-results.md`, the agent may write a short summary during website projection using only accepted evidence and canonical decisions. The summary must:

- state why the venue is useful or interesting;
- include the most important practical caveat when applicable;
- avoid internal rubric jargon;
- avoid unsupported superlatives;
- remain traceable to source decision IDs and accepted evidence.

Generated summaries live only in `interactive-results-data.json`; they do not become canonical Phase 6 decisions.

Audit mode does not require a promotional summary.

## Website projection contract

The derived `{RUN_DIR}/interactive-results-data.json` contains:

- schema version;
- source run ID, category, and canonical decision-ledger hash;
- run, rating, and access snapshot dates;
- approved facet definitions and controlled values;
- Practical and Audit record arrays;
- category theme configuration;
- declared counts and mapped counts;
- source decision ID for every projected record;
- reader-facing summaries and display labels;
- occasion and rare-find memberships;
- accepted location fields copied from the canonical ledger.

The projection never becomes a decision authority. Regenerating it cannot change `06-decisions.json`.

### Practical mode

Practical mode includes every qualifying venue with an explicit current dining or buying path in the canonical snapshot. Valid paths may include:

- walk-in storefront;
- recurring public market;
- active preorder or pickup;
- delivery or service area;
- verified stockist;
- home-based sale or pickup;
- another explicitly accepted current acquisition path.

Home-based format is not a reason for exclusion. Use the accepted business address and coordinates already established by the research workflow. The website skill does not add a separate residential-address classification or search for alternate addresses.

Practical mode contains the full currently obtainable qualifying corpus, not only the top occasion recommendations. Occasion and rare-find recommendations are highlighted and available as facets.

### Audit mode

Audit mode contains compact rows for unavailable, unresolved, filtered, closed, conflicted, or otherwise non-actionable records retained by the run.

Each row may show:

- canonical venue name;
- disposition;
- primary reason;
- scores when available;
- last-known access state and date;
- `Check current place record` when an accepted business address exists.

The Google Maps link uses canonical name plus accepted address. It is a reconnaissance action, not a claim that the venue is currently visitable. Audit rows have no `Directions` or other visit-oriented CTA.

An Audit record without an accepted address receives no Maps link. Audit records do not appear as pins on the Practical map.

### Practical/Audit integrity

Generation fails when:

- a projected record lacks a valid canonical decision ID;
- Practical and Audit populations overlap;
- a Practical record lacks explicit current-access evidence;
- declared projection counts differ from actual counts;
- a map link lacks an accepted address;
- a coordinate falls outside valid latitude/longitude ranges;
- a controlled facet value is undeclared;
- an occasion or rare-find reference does not resolve;
- a dataset value cannot be safely serialized.

Records omitted from both modes must be listed explicitly with a reason; silent loss is forbidden.

## Required facet-design checkpoint

Before rendering, the agent inspects the completed corpus and proposes a controlled taxonomy.

### Shared facets

Offer shared facets when supported by the run:

- text search;
- Practical/Audit mode;
- region or subarea;
- current access format;
- occasion;
- rating floor;
- evidence or rating status;
- shortlist-only;
- sort order.

### Bakery defaults

Candidate bakery specialty values include:

- bread;
- pastry and pâtisserie;
- doughnuts;
- bagels and savory baking;
- pies;
- cookies and sweets;
- cakes and cheesecake;
- regional specialty;
- gluten-free or vegan.

These are defaults, not a mandatory universal taxonomy.

### Restaurant defaults

Restaurant facets may include:

- locally meaningful cuisine groups;
- service or experience format;
- notable production strengths or specialist formats;
- rare-dish membership.

Cuisine grouping must reflect how people navigate the specific market rather than imposing one universal global taxonomy.

### User checkpoint

The agent presents:

- proposed regions and their intended boundaries;
- proposed category-specific values;
- representative venues for each value;
- possible local extensions;
- aliases to normalize together;
- values rejected as too sparse, ambiguous, or overlapping.

The skill asks how the user thinks about the market and what they want to filter by. Generation waits until the user approves, revises, or explicitly says `use your defaults`.

The approved taxonomy is stored in `interactive-results-data.json`. `generate.py` rejects undeclared record values rather than creating one-off facets.

## Interface design

The site uses one consistent food-finder identity and interaction model. Bakery and restaurant variants adjust typography, colors, category terminology, and declared facet configuration without changing application code.

### Desktop layout

Use a persistent header containing:

- title and scope;
- snapshot date;
- search;
- result count;
- sort control;
- Practical/Audit switch;
- mobile controls when relevant.

Below it, use three panes:

1. independently scrolling facets;
2. independently scrolling result cards;
3. a fixed map of currently filtered Practical records.

The result pane must scroll without changing `window.scrollY` or moving/resizing the map pane.

### Mobile layout

Results are the default view. Two separate visible controls open:

- a facet drawer;
- a full-screen map overlay.

Responsive hiding must always have a visible inverse action. Activating `Show card` from a map popup closes the map overlay, restores the map-toggle label, reveals the matching card, scrolls it into view, and moves keyboard focus to it.

### Filtering

- Text search covers name, accepted location label, summary, region, and category-specific values.
- Use OR within one facet and AND across different facets.
- Recalculate alternate-facet counts by applying all active filters except the facet being counted.
- A nonzero rating floor excludes records without an accepted rating; missing ratings are never coerced to zero.
- Practical and Audit mode maintain clearly separate presentation and controls.

### Sorting

Provide:

- combined score descending when supported;
- rating descending with combined-score tie-break;
- alphabetical order;
- category-relevant approved options where deterministic fields exist.

Default to combined score for qualifying Practical records unless the approved projection declares another default.

### Cards and audit rows

Practical cards show:

- name and accepted public location label;
- category, access, occasion, and specialty/cuisine badges;
- concise plain-language summary;
- rating and provenance;
- appropriate public-facing metrics without internal rubric jargon;
- shortlist action;
- `Directions` using canonical name plus accepted address, or a no-location label.

Audit mode uses compact rows as defined above.

### Shortlist

Persist the shortlist as canonical decision IDs in `localStorage`.

Provide:

- add/remove actions;
- saved count;
- saved-only filter;
- persistence across reloads;
- graceful removal of IDs no longer in a regenerated dataset.

Shortlist state remains browser-local and is never published or transmitted.

## Map behavior

Use Leaflet and OpenStreetMap assets and tiles from public CDNs. The output remains a single generated HTML file; map rendering requires network access.

Map rules:

- render only accepted canonical coordinates;
- leave records without coordinates searchable and unpinned;
- show the map whenever at least one currently filtered Practical record has coordinates;
- use a polished list-only layout when the complete Practical corpus has none;
- rebuild markers from the filtered Practical set;
- show filtered and mapped counts;
- fit bounds only when no record is actively selected;
- preserve selected context during filtering and list scrolling;
- use declared category/tier/status marker styling;
- never add Audit records to the Practical marker layer.

Card-to-map behavior:

- clicking a Practical card with a pin selects and emphasizes its marker;
- the map flies or pans to the marker and opens its popup;
- card controls stop propagation so shortlist and Maps actions do not trigger selection.

Map-to-card behavior:

- each popup includes a real keyboard-accessible `Show card` button;
- activating it selects the canonical ID, reveals the matching card, scrolls it into the center of the result pane, and moves focus;
- mobile activation closes the map overlay before revealing the card.

## Deterministic template and generator

Agents make judgment-heavy choices—legacy ambiguity resolution, Practical/Audit projection, facets, and missing summaries—but do not hand-edit application JavaScript per run.

`generate.py` accepts validated decision and projection paths, validates both schemas and cross-file invariants, safely serializes all values, and injects declarative data/config into `template.html`.

The generator must:

- produce byte-identical HTML for identical template, schema, and projection inputs, excluding an explicitly supplied generation timestamp if present;
- escape data for both HTML and JavaScript embedding contexts;
- reject non-finite numbers and invalid Unicode or unsafe path values;
- include no run-directory absolute paths in the public page;
- emit `{RUN_DIR}/index.html` atomically;
- avoid external application dependencies beyond declared CDN map assets;
- never mutate canonical decisions or the approved projection.

Category adaptation is declarative. The template contains stable tested interactions and CSS; configuration chooses labels, palette tokens, typography class, facet order, badge vocabulary, and metric labels.

## Local validation

### Static validation

Before browser testing:

- validate both JSON documents against their schemas;
- validate cross-file counts and IDs;
- parse generated HTML;
- extract and syntax-check inline JavaScript;
- scan output for secrets, absolute local paths, and unsupported data;
- verify declared CDN URLs and integrity/cross-origin configuration when used.

### Browser validation

Serve the run directory over local HTTP. Do not rely on opening `file://` directly.

At desktop and mobile viewports, fail on any page error and test:

- declared Practical, Audit, and mapped counts;
- text search;
- every declared facet value;
- OR-within and AND-across behavior;
- alternate-facet counts;
- all sort modes;
- Practical/Audit switching;
- shortlist add/remove, persistence, saved count, and saved-only mode;
- reset and empty-result states;
- no-coordinate and all-no-coordinate behavior;
- card-to-marker selection;
- popup-to-card navigation;
- selected styling and keyboard focus;
- independent center-pane scrolling;
- mobile facet drawer and backdrop;
- mobile map overlay and return-to-card flow;
- accessible names and keyboard operation.

Visually inspect desktop and mobile screenshots for overlap, clipping, unreadable controls, inaccessible drawers, map overlays hiding required navigation, and unclear Practical/Audit distinction.

### Validation artifact

Write `{RUN_DIR}/interactive-results-validation.json` containing:

- schema and generator versions;
- hashes of canonical decisions, projection, template, and generated HTML;
- generation timestamp;
- snapshot dates;
- expected and observed counts;
- static checks;
- browser viewport results;
- interaction assertions;
- screenshot paths when retained;
- final pass/fail status.

The manifest links all derived artifacts and source hashes. A failed validation cannot be recorded as complete.

## Publication boundary

After successful local validation, report the local `index.html` and offer `/gisthost`.

Do not publish automatically. A separate explicit user request is required because publication is externally visible and may expose the accepted corpus.

Before publication:

- regenerate from the current approved projection;
- rerun validation;
- inspect the final HTML for secrets and unsupported data;
- use the existing `reference/gisthost.md` workflow.

When updating an existing gist, preserve its URL when possible. Verify the hosted page with targeted browser assertions; HTTP 200 alone is insufficient.

## Core rubric integration

Both root rubric skills retain synchronized versions and add the shared canonical JSON requirement.

Phase 6 changes:

- write and validate `06-decisions.json` as canonical;
- optionally generate `06-decisions.md` from JSON;
- update the manifest with schema/hash/validation information.

Phase 8 changes:

- consume JSON only for decisions;
- keep `08-results.md` as the reader-facing report;
- verify report counts and memberships against canonical JSON;
- after successful completion, suggest `/interactive-results <RUN_DIR>` as an optional next step.

Neither rubric auto-generates a website or performs website facet design during the canonical run.

## Error handling

- **Missing run directory:** ask for a path.
- **Incomplete run:** stop and identify missing or invalid canonical artifacts.
- **Legacy ambiguity:** write the migration report and ask only consequential questions; do not guess.
- **Invalid canonical JSON:** stop before projection and report exact schema/invariant failures.
- **Stale snapshot:** show dates and let the user decide whether to refresh the underlying run; do not research during website generation.
- **Missing coordinates:** retain searchable unpinned records; use list-only mode when none exist.
- **Missing accepted address:** omit Maps actions without inventing a location.
- **Unapproved facets:** wait for approval or `use your defaults`.
- **Projection overlap or count mismatch:** stop and repair the projection.
- **Template or JavaScript failure:** do not emit a successful validation artifact.
- **Browser test failure:** retain diagnostics, repair, regenerate, and rerun the complete affected validation matrix.
- **Publication failure:** keep the validated local artifact and report the external failure honestly.

## Testing strategy

### Schema fixtures

Include valid and invalid bakery and restaurant decision fixtures covering:

- scored/ranked records;
- rating-unconfirmed or provisional ratings;
- unresolved and exhausted dispositions;
- filtered or DQ records;
- merge targets;
- storefront, preorder, market, delivery, stockist, and home-based access;
- records with and without accepted coordinates.

Projection fixtures cover:

- Practical and Audit records;
- occasion and rare-find facets;
- category-specific facet extensions;
- accepted and rejected map links;
- list-only fallback;
- declared-count mismatches and overlap failures.

### Migration tests

Test:

- a valid legacy bakery run;
- a valid legacy restaurant run;
- mixed vector/scalar score forms;
- duplicate and missing IDs;
- ambiguous dispositions and merge targets;
- missing access and coordinate fields;
- migration reports that block consequential ambiguity.

### Generator tests

Test:

- deterministic output;
- schema and cross-file validation;
- HTML and JavaScript escaping;
- invalid coordinate and non-finite-number rejection;
- undeclared facet rejection;
- source decision resolution;
- atomic output;
- no absolute-path leakage;
- bakery and restaurant theme configuration;
- no-coordinate list-only behavior.

### Browser tests

Use a local HTTP server and browser automation for desktop and mobile interaction assertions defined in Local validation. Tests must exercise real generated fixtures rather than only inspecting source strings.

### Core-contract tests

Extend repository contract tests to verify:

- both rubrics require canonical `06-decisions.json`;
- optional Markdown is generated rather than independently authoritative;
- Phase 8 consumes JSON and suggests the optional skill;
- synchronized rubric versions and discovery user agents;
- the website skill never performs fresh research or automatic publication.

## Non-goals

Version 1 does not:

- refresh an old corpus from the web;
- change canonical decisions, evidence, ratings, scores, or recommendations;
- infer missing coordinates or addresses;
- automatically publish;
- support arbitrary non-food research runs;
- provide server-side accounts, shared shortlists, analytics, or telemetry;
- build a multi-file hosted application;
- expose complete evidence quotations and repair history in Audit mode;
- let agents rewrite application JavaScript for each market;
- replace `08-results.md` as the canonical reader-facing report.

## Success criteria

The design succeeds when a completed bakery or restaurant run can produce a deterministic, validated, single-file explorer that:

- faithfully reflects canonical JSON decisions;
- exposes the full currently obtainable qualifying corpus in Practical mode;
- keeps non-actionable records visible but clearly separate in Audit mode;
- supports user-approved local facets and occasion filtering;
- synchronizes list and map navigation on desktop and mobile;
- preserves a browser-local shortlist;
- handles missing coordinates gracefully;
- remains snapshot-only and traceable to source hashes;
- requires separate explicit consent for public publication.
