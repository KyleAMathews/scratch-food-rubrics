# Phase 8 — Bakery Rendering

**Read this file in full only after Phases 1–7 have passed. Do not render recommendations early.**

#### Rare-finds layer — item-ranked, not venue-ranked (a distinct output mode)

Separate from the occasion lists (which rank *bakeries*); this ranks *baked goods* — rare regional items worth a detour, and where. Built for the buyer who'll detour 15 min for a pastry only made in one region of France that some shop is obsessed with.

**Construction:**
1. **Scratch is a HARD prerequisite gate.** A rare item done from frozen/par-bake is a novelty trap. Gate on the bakery's scratch bar first; only survivors are eligible.
2. **Rank survivors by market-scarcity, reasoned not scraped:** what is this item, what region is it from, is it rare/absent in THIS metro? (Canelé = Bordeaux; kouign-amann = Brittany; a specific regional bread/pastry a shop specializes in; Buddhist/ethnic specialties absent locally.) Knowledge+reasoning about the local baseline.
3. **Threshold = rare-in-city or rarer** (self-adjusts to market size): *only place in the metro* (strongest) > *rare in the city* (worth a detour). Cut *uncommon-but-findable*.
4. **Per entry:** *the rare item* + *bakery & cross-street* + *one line on why it's rare here*. Cross-cuts both scorecards.

**Hard boundary:** claims **"rare in THIS market,"** NEVER "rare in the world / best anywhere" (that's the deferred cross-market layer). "Only canelé in town" = safe; "world's best canelé" = needs the corpus.

**Retrieval note — use a places/map directory, not a web search, to pin rare-finds venues.** The long tail is where web-search *prominence bias* hurts most: a query for a rare regional bake returns the famous brand of that item + recipe blogs, not the neighborhood specialist. A **map/places directory** (storefront-indexed: Google Maps/Places, Yelp, or equivalent) returns real local addresses. Rule of thumb: **web search for the *pattern & scarcity reasoning*; a places/map directory for the *specific venue* (name, address, hours, review text confirming scratch).**

## Presentation model — foodie occasions → top 3 (scores demoted to audit)

**We filter for scratch, so mass-market occasion sets don't apply.** Our audience is foodies who treat *how it's made* as table stakes, so occasions slice the *scratch* population by how a food-obsessive decides. Foodie-native bakery intents:

- **"Best bread in the city"** — the naturally-leavened bread pilgrimage
- **"Weekend pastry + coffee, worth lingering"** — sit-down viennoiserie/pâtisserie experience
- **"Showpiece to bring / gift"** — the impress-someone bake
- **"The one thing worth crossing town for"** — single-item specialists (the canelé, kouign-amann, hand-phyllo). *This is a foodie-only category no mass-market occasion set has a slot for — it maps directly onto the marker-item work (single-item mastery).*

**Presentation rules:**
1. **Show top 3 per occasion, nothing else.** ~10–15 candidates → ~5–6 scratch → display **top 3**; omission is information.
2. **A bakery appears in multiple occasions**, standing differing by occasion (a traditional-excellence specialist is top-3 for "gift" and "best bread," absent from "something new"). Venue×occasion matrix, not one list.
3. **Score everything, keep everything, show three.** Display is lossy; retained data must not be — the deferred city-aggregation layer needs full scores to roll up. This invariant keeps the second layer buildable without a re-run.
4. No rubric jargon, no anchor names, near-ties as ties.

**Constraints are post-filters, not occasions:** late-night, open-now, sells-out-timing, price — narrow any occasion's list, don't define an intent.

**Output order (reader-facing):** occasion lists (top-3 per intent) at the TOP; rare-finds next; the combined S/I/G ranking at the BOTTOM as a collapsed audit table. **Retire "Home vs. Trip" from reader output** — internal scaffolding that muddled the UX; a traditional-excellence bakery is great regardless of whether you live there. Keep Home/Trip in the methods/audit section only.

### Deferred layers (out of scope for a single-market run — noted, not built)

- **City aggregation:** "top 3 in the city" across neighborhood partitions using retained scores.
- **Cross-market superlatives:** "only place in the world for this / worth a trip" requires a multi-city corpus + global rarity×quality ranking. **The rubric is geographically scoped to one market per run**; a single-city run must NOT claim a global superlative (the dangerous overclaim). The second layer consumes retained scores; it does not re-run scoring.

## Presentation rule (audience-facing summaries)

Named calibration anchors (specific bakeries) are **private reference points** for building/validating the rubric — meaningless to a stranger reading a shared summary. When presenting a **structural summary, explanation, or ranking to any audience other than the author**, name the *pattern*, not the *exemplar*:

- "the Great Harvest / Acme pattern" → **"a wholesale-standardization bakery"** (scratch, but consistency pressure caps novelty)
- "the Feldman's pattern" → **"a traditional-excellence specialist"** (high-S, low-I; single perfected item)
- "the House of Bread anchor" → **"an IG-only sell-out microbakery"**
- "the Tulie case" → **"a café-bakery with service/coffee-contaminated R"**
- "the Ballerina Farm case" → **"a maximum-brand-register, maximum-sourcing, low-novelty bakery"**

Every concept is defined independently of its exemplar (traditional-excellence, wholesale-standardization, register-independence, par-bake, resolution floor, trip-swing, N-vs-δ), so summaries read cleanly with zero named venues. **Keep named anchors only in the calibration tables** (they are the validation evidence); strip them from portable prose.

### Two audiences, two vocabularies

Distinguish **internal method-terminology** (how the rubric was built) from **external verdicts** (what a reader wants). Terms like *register-independence, resolution floor, S/I/E axes, par-bake, N-vs-δ, trip-swing, wholesale-standardization, cadence-deconfound* are internal scaffolding — they should **never appear in an outward-facing writeup**. Keep the *behavior*, drop the *label*:

- **Resolution floor** → don't name it; **present near-ties as ties** ("both are exceptional — go to whichever's convenient"), never a false rank within the error band.
- **Register-independence** → don't explain it; **give physical evidence, not methodology** ("the layers shatter, the crumb is open and blistered"), never "lamination score / physical descriptor."
- **S/I/E, G, trip-mode, par-bake** → plain verdicts: S→"made from scratch, not frozen/par-baked," I→"worth going back for / would get repetitive," E→"reliably well-made," trip-mode→"best single stop if you're only there once."

Rule of thumb: an external summary should read like a knowledgeable friend's tip — concrete sensory evidence + clear verdict + honest ties — with **zero rubric vocabulary and zero private anchor names**. The machinery stays behind the curtain.

**Three axes** (same structure as the restaurant tool):
1. **S_bakery** — production/scratch intensity, 0–100.
2. **I** — interestingness / novelty, 0–100.
3. **R** — star rating, used as a **quality filter (θ ≈ 4.3★)**, not an objective.

**Price** = neutral metadata ($, Google 1–4 bucket), displayed not scored. **Day-part neutral** — bakeries are morning/lunch by nature; never penalize for it.

Decision rule: filter {R ≥ 4.3 ∧ S ≥ 55}, rank by **G = √(S × I)**.

A valid provisional rating follows the same floor and ranking rule, but reader-facing results must label it as secondary-source/provisional and name the attributed platform. Never imply that it was observed directly. Under the existing near-tie rule, provisional rating evidence cannot break a near-tie against directly observed rating evidence.

---

## Rating-unconfirmed and current-access presentation

After the rated occasion lists, render a separate, visible, unranked **Scratch-verified, rating-unconfirmed** section. Include every candidate with accepted scratch evidence whose rating remains terminally unavailable after the identity-first sweep. State that omission from rated rankings reflects missing rating evidence, not a negative quality judgment.

Before that section, render a visible, unranked **Scratch-eligible, partial evidence** section for rating-confirmed bakeries whose positive bakery-production evidence covers fewer than all S criteria. Show `earned/observed-possible`, coverage, confidence, and the exact proven production scope in plain language. Never show a percentage-like normalized S or G for a partial. A narrow component claim must say what remains unknown—for example, “fillings made in house; dough and lamination unknown.”

For every otherwise eligible producer record:
- **Access format:** `storefront`, `recurring market`, `active preorder`, `service-area/delivery`, `wholesale/stockist`, `home microbakery`, or `unknown`.
- **Current acquisition evidence:** `walk-in active`, `drop active`, `preorder active`, `hiatus`, `closed`, `conflicting`, or `unverified`, with latest dated source.
- Main “go here” occasion lists require a stable current acquisition path. Immediately before rendering, recheck intermittent, preorder, market, service-area, and microbakery producers.
- Keep craft scores unchanged when access is unstable. Put `hiatus`, `conflicting`, `unverified`, and irregular/non-walk-in producers without a currently verified purchase path in a separate **availability-sensitive watchlist**, with the last known way to buy and date. Do not present them as spontaneous walk-in recommendations.

## Coverage statement

Report broad-survey count, targeted additions, deduplicated union, coverage-audit additions, last-pass yield, and precise limitations. Never call processed OSM rows a complete real-world census.

## Canonical rendering input

Read decisions exclusively from canonical `{RUN_DIR}/06-decisions.json`; do not consume an independently authored `06-decisions.md`. The JSON is the only decision authority. Verify every reader-facing membership and count against canonical JSON while keeping `08-results.md` as reader-facing prose.

## Phase 8 artifact

Write the final reader-facing result to `{RUN_DIR}/08-results.md`. Any generated HTML, PDF, export, or sharing payload MUST also live inside `{RUN_DIR}`. For every generated HTML or PDF export, inspect the rendered pages visually—not only compilation or extracted text. Check for overlap, clipping, illegible wrapping, and broken pagination. Split or redesign any long table or disclosure block that cannot paginate cleanly, then inspect the regenerated export. Update `00-run-manifest.md` to `complete` with links to every standard artifact.

## Phase 8 completion gate

- [ ] All prior phase gates passed.
- [ ] Every reader-facing claim rests on accepted evidence.
- [ ] Occasion, rare-find, tie, audit, timing, and plain-language rules above were followed.
- [ ] Discovery limitations are stated at the source-convergence level.
- [ ] Access format and current acquisition evidence are shown for every otherwise eligible producer; unstable or unverified paths are routed to the availability-sensitive watchlist.
- [ ] The pre-render direct-place rating rerun is reflected in the rated lists and the visible rating-unconfirmed section.
- [ ] Every partial score is visible in the correct partial or rating-unconfirmed section, remains non-normalized, and states its proven production scope and unknown criteria.
- [ ] Every provisional rating is visibly labeled as secondary-source evidence with its attributed platform and was not used to break a near-tie against direct evidence.
- [ ] Every generated HTML/PDF export received rendered-page visual inspection; long tables and disclosure blocks paginate without overlap or clipping.

## Optional interactive follow-up

After the Phase 8 completion gate passes and the manifest is `complete`, suggest exactly one optional next step: `/interactive-results {RUN_DIR}`. Do not invoke it, generate a website, or publish anything without the user's subsequent explicit approval.

## Sharing Results

Want to share your results? Generate an HTML page with the occasion matrix and ranked tables, then use `/gisthost` to publish it as a shareable website. See `reference/gisthost.md` for details.
