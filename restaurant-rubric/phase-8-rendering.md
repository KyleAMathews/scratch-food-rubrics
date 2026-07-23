# Phase 8 — Restaurant Rendering

**Read this file in full only after Phases 1–7 have passed. Do not render recommendations early.**

#### Rare-finds layer — dish-ranked, not venue-ranked (a distinct output mode)

A separate output from the occasion lists. Those rank **venues** ("best places"); this ranks **dishes** ("rare things worth a detour, and where"). The unit is the dish; the venue is almost incidental. Built for the diner who'll make a 15-min detour for an unusual regional/ethnic dish or a pastry some shop is weirdly obsessed with.

**Construction:**
1. **Scratch is a HARD prerequisite gate** (not a ranking input). A rare dish done from frozen/imported product is a novelty trap — you make the detour and it's reheated. Gate on the venue's scratch bar first; only survivors are eligible.
2. **Rank the survivors by market-scarcity (A_scarcity), reasoned not scraped.** The model must reason: *what is this dish, what region is it from, and is it rare/absent in THIS metro?* (Buddhist no-onion/garlic vegetarian is common in much of Asia, near-absent in the US; canelé is a Bordeaux specialty; kouign-amann a Breton one; a specific regional pastry a shop is obsessed with.) This is knowledge+reasoning about the local baseline, not a review scrape.
3. **Threshold = rare-in-city or rarer** (against the local baseline, which self-adjusts to market size):
   - **Only place in the metro** — strongest find; "if you're near, go."
   - **Rare in the city** — a handful of places at most; worth a detour.
   - *Uncommon-but-findable is cut* — if ten places make it well, it's dinner, not a find.
4. **Output format per entry:** *the rare dish* + *venue & cross-street* + *one line on why it's rare here*. Cross-cuts cuisines and both scorecards (a regional stew and a regional pastry sit on the same list); ignores the occasion framing.

**Hard boundary (the overclaim seam):** this layer claims **"rare in THIS market,"** NEVER "rare in the world / best anywhere." A single-market run can honestly say "only canelé in SLC"; it cannot say "world-class canelé" — that's the deferred cross-market layer. Within-market scarcity is safe; global superlatives need the multi-city corpus.

**Retrieval note — use a places/map directory, not a web search, to pin rare-finds venues.** This layer reaches into the long tail, which is exactly where web-search *prominence bias* hurts most: a query for a rare regional dish returns the nationally-famous chain of that cuisine and recipe blogs, not the unassuming neighborhood storefront you want. A **map/places directory** (storefront-indexed: Google Maps/Places, Yelp, or equivalent) returns actual local addresses and surfaces the hidden spot. Rule of thumb: **web search for the *pattern & scarcity reasoning* (what is this dish, where's it from, is it rare here); a places/map directory for the *specific venue* (name, address, hours, review text confirming scratch).** The two prior coverage misses (a 55-yr institution; a neighborhood Xi'an spot) both failed on web search and were caught by a places lookup.

## Presentation model — foodie occasions → top 3 (scores demoted to audit)

**We filter for scratch, so industry occasion sets (celebration/social/business/convenience) don't apply** — they're built for a mass market where "reheated but done well" is a valid celebration answer. That whole tier is filtered out at the door. Our audience is foodies who treat *how it's made* as table stakes, so occasions must slice the *scratch* population the way a food-obsessive actually decides. Keep the industry *structure* (occasion × format, venues appear in multiple cells) but use foodie-native intent labels:

**Restaurant occasions (intents):**
- **"The best meal in town"** — pilgrimage/special; top scratch + chef-driven kitchens (the foodie framing of "celebration" — they want the best *kitchen*, not just a nice room)
- **"Something I can't get elsewhere"** — novelty/discovery; high menu-turnover, chef's-choice, unusual cuisine
- **"Great casual scratch meal"** — everyday-excellent; humble format, serious kitchen (taquería nixtamalizing its own masa, a proper ramen-ya)
- **"Who's doing [cuisine] right"** — the cuisine-specialist lookup

**Presentation rules:**
1. **Show the top 3 per occasion, nothing else.** Ideal geographic scope has ~10–15 candidates → ~5–6 genuinely scratch → display **top 3**. Omission is information; a foodie wants the shortlist, not a census. At that funnel width the top 3 are separated enough to clear the resolution floor.
2. **A venue appears in multiple occasions**, and its standing can differ by occasion (a high-execution/low-novelty venue is top-3 for "best meal" but absent from "something new"). Presentation is a venue×occasion matrix, not one re-sorted list.
3. **Score everything, keep everything, show three.** The display is lossy (top-3, no numbers, tiers not ranks); the data underneath must NOT be — the deferred aggregation layer needs full retained scores to roll up. This invariant is what keeps the second layer buildable without a re-run.
4. **No rubric jargon, no private anchor names, near-ties shown as ties** (see below).

**Constraints are post-filters, not occasions:** late-night, open-now, takeout, price ceiling narrow any occasion's list — they don't define an intent (same discipline as price-as-neutral-metadata). Apply after occasion selection.

**Output order (the reader-facing run):** lead with the **occasion matrix (top-3 per intent)** at the TOP — that's what a reader wants first. The **combined S/I/G ranking goes at the BOTTOM as an audit table**, collapsed/secondary, for anyone who wants to see the working. Rare-finds layer sits between them. **Retire the "Home vs. Trip" toggle from reader output** — it was internal scaffolding and confused the UX (a traditional-excellence venue is obviously great whether you live there or are visiting). The single case it captured ("I'm only here once") is now just the catchment/occasion framing; if single-visit ordering is ever needed, note it as one line inside an occasion, not a parallel ranking. Home/Trip stays in the audit/methods section only.

### Deferred layers (out of scope for a single-market run — noted, not built)

- **City aggregation:** "top 3 in the city" rolled up across neighborhood partitions using retained scores.
- **Cross-market superlatives:** "best in the world / worth a trip for" requires a multi-city corpus and a global rarity×quality ranking. **The rubric is geographically scoped to one market per run**; a single-city run must NOT claim a global superlative it has no evidence for (the dangerous overclaim). This is a genuine architectural seam — the second layer consumes the first layer's retained scores; it does not re-run scoring.

## Presentation rule (audience-facing summaries)

The named calibration anchors (specific restaurants/bakeries) are **private reference points** used to build and validate the rubric — they mean nothing to a stranger. When presenting a **structural summary, explanation, or ranking to any audience other than the rubric's author**, name the *pattern*, not the *exemplar*:

- "the Feldman's / Red Iguana pattern" → **"a high-S / low-I traditional-excellence venue"** (scratch and excellent, but a fixed menu → low repeat-novelty)
- "the Acme / Great Harvest pattern" → **"a wholesale-standardization venue"** (scratch, but consistency pressure suppresses novelty)
- "the Table X Bread anchor" → **"a world-class reference point"** or just the score
- "the Cheesecake Factory case" → **"a broad cross-cuisine, high-N/low-K assembly operation"**
- "the Ballerina Farm case" → **"a maximum-brand-register, maximum-sourcing, low-novelty venue"**

Every structural concept in this system is defined independently of its exemplar (traditional-excellence, wholesale-standardization, register-independence, N-vs-δ, resolution floor, trip-swing), so summaries stay fully legible with zero named venues. **Keep named anchors only in the calibration tables** (they are the empirical evidence of validation); strip them from any portable prose.

### Two audiences, two vocabularies

Distinguish **internal method-terminology** (how the rubric was engineered) from **external verdicts** (what a reader wants). Terms like *register-independence, resolution floor, S/I/E axes, N-vs-δ, trip-swing, wholesale-standardization* are internal scaffolding — they should **never appear in an outward-facing writeup**. Keep the *behavior*, drop the *label*:

- **Resolution floor** → don't name it; just **present near-ties as ties** ("these three are all excellent — choose by convenience/mood"), never a false #1/#2/#3 within the error band.
- **Register-independence** → don't explain it; just **give the physical evidence, not the methodology** ("the crust blisters and the crumb is open and irregular"), never "high lamination score / register-independent descriptor."
- **S/I/E, G, trip-mode** → translate to plain verdicts: S→"genuinely made from scratch," I→"worth returning to / would get boring," E→"consistently well-executed," trip-mode→"best single-visit pick."

Rule of thumb: an external summary should read like a knowledgeable friend's recommendation — concrete sensory evidence + a clear verdict + honest ties — with **zero rubric vocabulary and zero private anchor names**. The scoring machinery stays behind the curtain.

**v2 change:** raw menu-item count (N) replaced by **base-preparation load (K)** after factoring the menu's combinatorial grammar. Rationale below.

---

## Large-run reader-facing diversity

When at least 12 eligible venues exist, treat all occasion slots and rare finds as one reader-facing discovery budget. Choose occasion slots jointly and prefer a distinct restaurant in every slot. Then choose rare finds against the already-used venue set while retaining scratch and market-scarcity gates. Repeat a venue only when a specific occasion or rare-item requirement lacks a credible distinct alternative, and record the exception.

Diversity is a presentation constraint, not a scoring input. It never changes the audit, lowers evidence or eligibility thresholds, invents rarity, or promotes a weak venue only to avoid repetition. Completeness-oriented appendices may repeat venues.

## Complete and partial rendering boundary

Before rendering, transform every scoreable Phase 6 decision—including ordinary vector-form and calibration-backed scalar-form decisions—into one canonical audit-row schema. Each row contains the canonical candidate ID and venue name, disposition, criterion or accepted scalar score representation, rating value and provenance, tier and ranking eligibility, and canonical merge target when applicable.

Complete scores include S, I, and G. Partial scores instead show `earned/observed-possible`, coverage, provenance, confidence, and the exact observed criteria. They remain unranked; never scale them to 100 or invent I or G. Rendering fails if a scoreable decision cannot be represented, an ID appears twice, a canonical merge target is missing, the row violates Phase 6 validation, or rendered audit-row count differs from scoreable decision count. Record both the scoreable decision count and rendered audit-row count in the final report. Successful Markdown, HTML, or PDF generation alone does not establish complete rendering.

## Coverage statement

Report broad-survey count, targeted additions, deduplicated union, coverage-audit additions, last-pass yield, and precise limitations. Never call processed OSM rows a complete real-world census.

## Canonical rendering input

Read decisions exclusively from canonical `{RUN_DIR}/06-decisions.json`; do not consume an independently authored `06-decisions.md`. The JSON is the only decision authority. Verify every reader-facing membership and count against canonical JSON while keeping `08-results.md` as reader-facing prose.

## Phase 8 artifact

Write the final reader-facing result to `{RUN_DIR}/08-results.md`. Any generated HTML, PDF, export, or sharing payload MUST also live inside `{RUN_DIR}`. Update `00-run-manifest.md` to `complete` with links to every standard artifact.

## Phase 8 completion gate

- [ ] All prior phase gates passed.
- [ ] Every reader-facing claim rests on accepted evidence.
- [ ] Occasion, rare-find, tie, audit, hours/day-part, and plain-language rules above were followed.
- [ ] For a large run, occasion and rare-find slots use distinct venues or every repetition records the lack of a credible distinct alternative.
- [ ] Discovery limitations are stated at the source-convergence level.
- [ ] Every scoreable decision rendered exactly once, all partial scores remain visibly partial and unranked, Phase 6 validation remains green, and rendered audit-row count equals scoreable decision count.

## Optional interactive follow-up

After the Phase 8 completion gate passes and the manifest is `complete`, suggest exactly one optional next step: `/interactive-results {RUN_DIR}`. Do not invoke it, generate a website, or publish anything without the user's subsequent explicit approval.

## Sharing Results

Want to share your results? Generate an HTML page with the occasion matrix and ranked tables, then use `/gisthost` to publish it as a shareable website. See `reference/gisthost.md` for details.
