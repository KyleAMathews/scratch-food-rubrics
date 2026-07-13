# Scratch-Kitchen Scorecard & Travel Prompt (v8.8)

A model for finding restaurants that are **scratch-made AND interesting to a frequent diner** — using only signals scrapeable online (menu, website, reviews) before you go.

*Versioning: this and the bakery scorecard share one version line (both at **v8.8**) and bump together, since they share the retrieval, presentation, scarcity, and execution machinery. Each file's changelog tracks its own feature history; the headline version is shared.*

**Changelog:** **v8.8** — model tiering: research/extraction leaves run on cheap/fast models (constrained checklist extraction is a cheap-model strength AND fans out wider for less); orchestration/scoring stays smart; the evidence floor is what makes cheap workers safe, making the orchestrator's reject-thin-returns enforcement load-bearing. **v8.7** — third evidence state "exhausted-unavailable" (searched-and-provably-absent, terminal, requires a stated search trail) so runs can close instead of looping on missing ratings; a documented rating is a filter not an absolute gate — scratch-verified + rating-exhausted venues route to a "scratch-verified, rating-unconfirmed" tier (surfaced with caveat, not dropped). **v8.6** — recursive subagent fan-out: a worker with too large a batch re-splits and spawns children (leaf ~10-15 venues, depth cap ~3) instead of grinding serially and inferring; the embedded evidence-floor brief propagates verbatim to every level, thin child-returns rejected at each level. **v8.5** — embeddable standard subagent brief (inline the full evidence floor verbatim — a subagent can't see the rubric, so "follow v8.2" does nothing); enumerates what counts as production nouns vs. marketing adjectives, bans rating-inference and format-DQs, requires an explicit "unresolved" token; orchestrator rejects thin returns. **v8.4** — boundary method: prefer a named place's real OSM admin polygon via rel→map_to_area (the id-offset area() form silently returns 0; verify non-zero, fall through LOUDLY to a derived box, never silently shrink); radius calibrated by market type (standalone town r≈12km to catch the rural tail; town-in-dense-metro → admin polygon + ~2-3km ring, since a 12km circle annexes neighbouring towns). **v8.3** — parallelize resolution with subagents when available (the structural fix for completion resistance: fan the tail out so cheap-inference pressure never accumulates); subagents inherit the v8.2 evidence floor and thin returns are rejected. **v8.2** — minimum-evidence floor: disqualify only on positive evidence (a missing OSM food tag is null signal, not a cut); R must be pulled not asserted to count as passing its gate; per-number provenance (documented/estimated/unverified) with reader-facing output rendered only from documented-R + opened-menu-S rows. **v8.1** — completion is a GATE not a report: full census resolution is a precondition for rendering the occasion matrix; permission-seeking hand-off of the un-opened tail banned; cuisine/format-parity tripwire (a whole un-opened category = format-prejudice zeroing, open it first). **v8** — **completion discipline (anti-laziness):** post-census "done" = every enumerated venue has a positive disqualifier OR an opened menu; zeroing-by-unheard-of banned; tag-mine free Overpass signal before searching; hard-count recall ledger with "unresolved" ≠ "excluded"; region-pin every query. **v7** — retrieval is now an **executable census**: `curl` → OpenStreetMap/Overpass API returns every tagged venue in the catchment bbox (popularity-neutral, category-blind), replacing the aspirational "enumerate first" language; web/places search demoted to enrichment-only; honest "per-OSM, not reality" boundary + explicit fallback when no census API is available. **v6** — retrieval: resident drive-time **catchment** (countryside included) + **exhaustive places-directory enumeration first, web-filter second** + **category hygiene** (bakeries route to the bakery scorecard, never leak here); reader output reordered (occasions top, S/I/G audit bottom); Home/Trip retired from reader output. **v5** — **market-scarcity (A_scarcity)** split from menu-turnover (δ) on the I-axis (a static menu can be maximally interesting on rarity alone); **rare-finds layer** (dish-ranked, scratch-gated). **v4** — **foodie-occasion presentation model** (occasions → top-3, scores demoted to audit; presentation-jargon and private anchors stripped from reader output). **v3.5** — **Home/Trip dual-rank** + **E (execution) axis** with variance tie-break. **v3** — added the **I (interestingness)** axis and G = √(S·I). **v1–2** — base scratch rubric (base-prep/K, volatility, sourcing, coherence, operator).

**Three orthogonal axes** (the star rating collapses all three into one lossy scalar):
1. **S_scratch** — production intensity (the rubric below), 0–100.
2. **I** — interestingness / novelty (turnover δ + market-scarcity A_scarcity), 0–100.
3. **R** — star rating ≈ E[satisfaction | visit 1]; used as a **quality filter (θ ≈ 4.0★)**, not an objective.

**Price** is carried as neutral metadata ($, Google's 1–4 quantile bucket) — displayed, never scored.

Decision rule: filter {R ≥ 4.0 ∧ S ≥ 60}, rank by **G = √(S × I)** (novelty tilt: G′ = S^0.4·I^0.6).

S_scratch latent variable: **on-site production intensity × proprietary-vs-commodity inputs**. Orthogonal to ownership (chain-ness is magnitude, not direction), so operator status is weighted low.

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

## Why K, not N (the combinatorial correction)

Item count conflates two things. A menu is often a *grammar*: pick base × protein × sauce × format. Then:

- **N ≈ ∏ᵢ cᵢ** — orderable items scale multiplicatively with the axis cardinalities
- **K ≈ Σᵢ cᵢ + shared infra preps** — distinct base preparations scale additively
- **Combinatorial leverage ρ = N/K**

The perishability + labor budget binds on **K**, not N — each distinct fresh prep costs labor-hours and shelf-life; recombining existing preps into another line is ~free.

- Taquería / mole house / deli / poke / thali: ρ ≈ 3–4 (large N, small K) → high N is *cheap* and should NOT be penalized
- Cross-cuisine encyclopedia chain: ρ ≈ 1.3–1.5 (K ≈ N, ~150+ distinct components) → large N is *expensive*, implies pre-made SKUs

(ρ and K figures throughout are first-principles estimates from menus, not a sourced dataset. Recalibrate by counting actual base preps at known venues.)

**How to estimate K:** try to factor the menu into choice axes. If it expresses as (base) × (protein) × (format) × (sauce), K = sum of the axis sizes — small even when N is large. If items are heterogeneous one-offs that don't factor (a lasagna, a pad thai, a fish taco, a burger, orange chicken), K ≈ N → broadline dependency.

---

## The rubric (0–100)

| # | Criterion | Weight | Scoring |
|---|-----------|-------:|---------|
| 1 | **Base-prep load & grammar (K)** | 20 | Factors cleanly, K ≲ 20 → 20 · partial, K 20–35 → 14 · weak, K 35–55 → 8 · flat encyclopedia, K > ~55 → 0–3. High ρ over a coherent single-cuisine grammar is positive, not penalized. |
| 2 | **Menu volatility / seasonality** | 25 | Dated/weekly change + specials board → 25 · seasonal rotation ≥4×/yr → 18 · occasional → 10 · static laminated → 0 |
| 3 | **Sourcing & production intensity** | 30 | Named farms/breeds/mills + ≥3 house-made markers → 30 · some of one → 18 · vague "fresh/quality" + glossy photos → 6 · photo menu, zero specificity → 0 |
| 4 | **Cuisine coherence** | 15 | Single focus → 15 · two adjacent → 10 · broad "American" grab-bag → 5 · 3+ unrelated cuisines → 0 |
| 5 | **Operator / format** | 10 | Chef-owned, 1–3 locations, open kitchen → 10 · independent single-site → 7 · regional group (4–15) → 5 · national franchise → 0 |

**Bands:** 80–100 very likely scratch · 60–79 scratch-leaning (spot-check) · 40–59 mixed/assembly-heavy · <40 almost certainly reheat.

Note: criteria 1 (K) and 3 (production) are partially collinear — both load on a single "production intensity" factor — so effective independent dimensionality is ~3–4. Weights (1→20, 3→30) are set so the *direct* production signal outvotes the cardinality proxy, which is what discriminates small-K scratch (mole house) from small-K commissary (fast-casual chain).

### Where to find each signal
- **K / coherence:** the online menu — factor it mentally.
- **Volatility:** dated menus, "market/seasonal" items, specials board, IG dish-of-the-day; compare archive.org snapshots for drift.
- **Production/sourcing:** menu + "about" page. Named purveyors, breeds, cuts, "milled/baked/butchered/ground in house."
- **Operator:** location count, "chef/owner," open-kitchen mentions.

---

## Salt Lake Valley calibration set (v2, per-criterion)

Estimates from online signals, not kitchen audits. P=prep-load/20, V=volatility/25, S=sourcing/30, C=coherence/15, O=operator/10.

| Restaurant | P | V | S | C | O | **Total** | Notes |
|-----------|--:|--:|--:|--:|--:|----------:|-------|
| Table X (Millcreek) | 20 | 23 | 30 | 14 | 10 | **97** | Garden ~70% of produce, in-house bakery |
| Oquirrh | 19 | 25 | 25 | 13 | 10 | **92** | Weekly-changing, house pasta |
| HSL | 18 | 24 | 25 | 13 | 10 | **90** | Hyper-seasonal, wood-fired |
| Pago | 18 | 23 | 27 | 13 | 8 | **89** | Farm-to-table pioneer |
| Urban Hill | 18 | 20 | 29 | 13 | 9 | **89** | Elite sourcing; no longer breadth-penalized |
| Arlo | 18 | 20 | 22 | 13 | 9 | **82** | Seasonal farm-to-table |
| The Copper Onion | 16 | 18 | 22 | 12 | 9 | **77** | House dairy/charcuterie |
| Caffe Molise | 16 | 15 | 22 | 15 | 9 | **77** | Chef-owner, house pasta |
| Zest Kitchen & Bar | 17 | 16 | 18 | 14 | 8 | **73** | Local/organic |
| Cultivate Craft (Draper) | 15 | 18 | 18 | 12 | 8 | **71** | Seasonal contemporary |
| **Red Iguana** | 19 | 8 | 29 | 15 | 4 | **75** | Fixed structurally — no override needed |
| Log Haven | 14 | 18 | 18 | 12 | 8 | **70** | Seasonal, historic |
| Rouser | 14 | 16 | 20 | 13 | 7 | **70** | Josper grill, hotel |
| Cafe Rio | 18 | 3 | 12 | 14 | 2 | **49** | Small-K, but static + commissary |
| Olive Garden | 12 | 0 | 3 | 8 | 0 | **23** | Menu factors fine; production/volatility damn it |
| Old Spaghetti Factory | 10 | 0 | 4 | 8 | 0 | **22** | Static/commissary |
| Applebee's | 3 | 0 | 0 | 3 | 0 | **6** | Grab-bag, reheat |
| The Cheesecake Factory | 1 | 0 | 3 | 0 | 0 | **4** | 250+ items, K≈N, catalog desserts |

Key v2 effect: **Red Iguana 53 → 75** and **Urban Hill 78 → 89** without special-casing; low scorers now separate on production/volatility rather than breadth.

---

## Park City / Wasatch Back calibration set (v2, per-criterion)

Second worked example, resort-town context. Same axes. Confidence tags: High = named farms/house-made documented on the menu itself; Med = strong secondary signal; Low = thin data.

| Restaurant | P | V | S | C | O | **Total** | Conf | Notes |
|-----------|--:|--:|--:|--:|--:|----------:|------|-------|
| Twisted Fern | 18 | 23 | 29 | 12 | 9 | **91** | High | Off-Main; menu names Riverence/Ashton/Heber Valley/Drake's + house pasta |
| Firewood | 17 | 22 | 26 | 13 | 10 | **88** | High | All open-flame (no gas/electric); closed Sun+Mon |
| Handle | 18 | 22 | 25 | 12 | 10 | **87** | Med-High | Briar Handly (same DNA as HSL); off-Main |
| Tupelo | 16 | 20 | 24 | 12 | 9 | **81** | Med-High | Chef Matt Harris, farm-to-table |
| 350 Main | 16 | 20 | 22 | 11 | 9 | **78** | Med | Wasatch-sourced, seasonal |
| LOMA | 17 | 16 | 22 | 14 | 8 | **77** | Med | Ross sister-concept; house pasta, wood-fired |
| Pine Cone Ridge | 16 | 18 | 20 | 12 | 8 | **74** | Low-Med | Chef-driven, upstairs off the strip |
| **The Farm** (Canyons) | 15 | 19 | 22 | 11 | 7 | **74** | Med | Spot-check: rubric ~74 but 3.9★ execution |
| Riverhorse on Main | 14 | 15 | 22 | 11 | 7 | **69** | Med | Fine-dining institution, more stable menu |
| Fuego Bistro | 12 | 3 | 5 | 9 | 5 | **34** | Med | High-volume pizza/Italian |
| The Eating Establishment | 8 | 4 | 8 | 5 | 7 | **32** | Med | Main St institution, broad all-day menu |
| Versante | 12 | 3 | 6 | 5 | 4 | **30** | Med | Cross-cuisine tell: Szechuan shrimp linguine on an Italian menu |

**Structural pattern (resort towns):** the highest-visibility, walk-in-friendly Main Street spots skew tourist-grade (broad static menus); the genuine scratch kitchens are either **off the main drag** (Twisted Fern, Handle, Tupelo) or **reservation-gated** (Firewood, Riverhorse). Default heuristic when arriving cold in a resort town: distrust the easiest walk-in on the main strip; search one block off.

**The Farm caveat (scope limit):** the rubric predicts **scratch-likelihood, not meal quality**. The Farm scores ~74 (seasonal, farm-branded, open kitchen) yet rates 3.9★ — a place can source seasonally and still execute unevenly. Use the rubric to narrow the candidate field, not to guarantee the plate.

**Verified anchor — Midway Mercantile ≈ 82 (High conf):** named local purveyors on the menu (Van Wagoner beef, Heber Valley cheese, Drake's goat cheese, neighbor-raised bison) + house pasta + hearth oven; confirmed takeout/curbside/delivery. Useful as a documented mid-80s reference point.

---

## Second axis: Interestingness Index (I, 0–100)

Why needed: R estimates **E[satisfaction | visit 1]**, so it's structurally blind to repeat-visit novelty — a first-timer can't distinguish a rotating dish from a static signature one. For a frequent diner (revealed home churn δ≈1, ≈never repeat a dish), novelty is the objective and R is only a floor.

I is built from scrapeable proxies. **Weights are design choices, not empirically fit.** **v-next reweight (Enjoy-validated):** interest has TWO independent novelty sources, not one — *turnover* (do I get something new each visit?) and *market-scarcity* (can I get this food anywhere else?). A static-menu place can be maximally interesting on scarcity alone, so δ can no longer dominate:

| Proxy | Wt | Scrape method / bands |
|---|--:|---|
| **δ menu turnover** (flow novelty) | 25 | (items changed)/total/time — diff archive.org snapshots, count "menu changes/specials" mentions. Weekly/daily → 25, seasonal → 16, static → 0. **Only realized by frequent buyers** (a one-visit patron experiences N, not δ). |
| **A_scarcity — market rarity of the offering** (stock novelty) | 25 | *Can you get this food elsewhere in this market?* Cuisine/dishes rare-or-unavailable locally (regional tradition absent elsewhere, "hadn't seen this since [home country]," no local peer) → 25; uncommon → 15; widely available cuisine → 5. **Independent of δ** — a fixed menu of dishes nobody else makes stays maximally rare forever. This is the dining analog of a frozen-incompatible marker item: rarity = interest that a static menu does NOT decay. |
| **A_technique — ingredient/technique ambition** | 20 | IDF-weighted rare-lexeme density (koji, garum, verjus, 'nduja, black garlic, house-cultured…). Dense → 20, some → 12, conventional → 5, photo-menu → 0 |
| **ν review novelty ratio** | 18 | freq(creative/inventive/"never had"/"can't get elsewhere") ÷ freq(classic/comfort/consistent). >1.5 → 18, ~1 → 11, <0.5 → 4 |
| **π rating polarization** | 12 | histogram dispersion at fixed mean; fat 1–2★ tail = ambition. **Hypothesis-grade, weakest.** High σ w/ mean≥θ → 12, moderate → 7, consensus-tight → 3 |

**The δ vs. A_scarcity split resolves the two kinds of traditional-excellence** (both high-S, static-menu, but they route to *opposite* occasions):
- **Perfected-common** (Feldman's pastrami, TO NEON bougatsa): low δ, **low A_scarcity** — supreme execution of a dish available elsewhere → "reliable standby / who's doing [cuisine] right."
- **Rare-cuisine** (Enjoy Vegetarian: Buddhist no-onion/garlic dishes a Hong Kong native "hadn't seen since home"): low δ, **high A_scarcity** → **"something you can't get elsewhere" despite never changing** — a travel-across-town place. Mis-scored at I≈60 under the old δ-dominant weighting; corrects to ~73 with scarcity carried independently.

**Collinearity flag:** δ overlaps the scratch rubric's volatility axis (same observable, different latent: scratch="made fresh" vs. I="new each visit"), so G = √(S×I) partially double-counts churn. Known limitation; down-weight one side to correct.

**Novelty is marginal (flow) OR fixed (stock).** Flow novelty (δ) is exhausted in ~N/s visits; stock novelty (A_scarcity) never decays. Tourist objective (visit once) ≈ N; frequent-diner objective ≈ δ×technique **+ A_scarcity**. The star rating optimizes the tourist's and sees neither.

### Decision rule (v3)
1. **Filter:** R ≥ θ (≈4.0★) AND S_scratch ≥ 60 (scratch is the enabling capacity for novelty).
2. **Rank by** G = √(S_scratch × I), 0–100. Novelty tilt: G′ = S^0.4 · I^0.6.
3. **Price** = neutral metadata, displayed not scored. Optional value view: I per $ level.

### Dual-rank: Home vs. Trip mode (compute both, toggle on trip-frequency)

A venue's correct rank depends on visit frequency, so compute **two rankings, not one**. Canonical case: Feldman's Deli — "very good but always exactly the same → not motivated to return, but would recommend to an out-of-town visitor" = two correct-but-opposite ranks for one venue.

- **Home mode (frequent):** rank by **G = √(S·I)** — novelty is live, you'll sample the menu over ~N/s visits.
- **Trip mode (one-shot):** rank by **S**, gate {R ≥ θ}, tie-break on **low E-variance**. I is noise for a single draw, and the **S–E floor effect** (S ≥ 75 → E ≈ 87–95 in the validated n≈6 sample) makes mean-E redundant with S — what remains is variance: favor all-day-consistent > sells-out-window, un-rushed > throughput-bottlenecked, fixed-menu > chef's-choice/off-menu format. (E-variance = flagged annotation from structural proxies — pop-up / sell-out-window / broad-case / chef's-choice — not a fitted term; mean-E known for ~6 venues, variance for ~0.)

**Signals that sign-flip on toggle:** wholesale/standardized scale (−I home / **+** trip = lowest variance); sell-out or limited-window cadence (+ freshness home / **−** variance trip); chef's-choice/rotating format (+I home / **−** variance trip).

**Effect:** modes converge where S and I couple (fine-dining scratch — the SLC, Inner Sunset, and Berkeley restaurant sets barely reorder); they diverge only for I-decoupled venues — traditional-excellence (Red Iguana, Antica Sicilia, Feldman's: high-S/low-I → rise in trip mode) and I-inflated formats. Worked reorder (Provo): Oteo #1 home (G 79.8, chef's-choice format = higher single-draw variance, Med conf) → **Pizzeria 712 #1 trip** (S 88, fixed markers incl. hand-pulled mozzarella, all-day-consistent, High conf).

### Combined ranking — Park City (R and $ documented this session; S, I are estimates)

| Restaurant | S | I | **G** | R★ | $ | Status |
|---|--:|--:|--:|--:|:--:|---|
| Twisted Fern | 91 | 83 | **86.9** | 4.6 | $$ | PASS — top on both axes |
| Handle | 87 | 82 | **84.5** | 4.4 | $$$ | PASS |
| Firewood | 88 | 74 | **80.7** | 4.5 | $$$ | PASS (closed Sun+Mon) |
| Tupelo | 81 | 61 | **70.3** | 4.3 | $$$ | PASS |
| 350 Main | 78 | 57 | **66.7** | — | $$$ | PASS |
| Pine Cone Ridge | 74 | 60 | **66.6** | 4.5 | $$ | PASS |
| LOMA | 77 | 53 | **63.9** | 4.4 | $$–$$$ | PASS |
| The Farm | 74 | 58 | 65.5 | 3.9 | $$$ | **FAIL θ** (3.9 < 4.0) |
| Riverhorse | 69 | 50 | **58.7** | 4.5 | $$$$ | PASS (low-novelty institution) |
| Eating Establishment | 32 | 22 | 26.5 | 4.3 | $$ | **FAIL S-floor** (32 < 60) |
| Versante | 30 | 18 | 23.2 | 4.3 | $$ | FAIL S-floor; cross-cuisine |

The two filter-failures are the point: The Farm is scratch+interesting but below the quality gate; Eating Establishment clears quality but isn't a scratch kitchen. G alone would rank them above nothing useful — the filters remove them cleanly.

### Combined ranking — Salt Lake Valley (I estimates; SLC R/$ NOT refreshed this session → approximate)

| Restaurant | S | I | **G** | R★ (approx) | $ (approx) |
|---|--:|--:|--:|--:|:--:|
| Table X | 97 | 84 | **90.3** | ~4.4 | $$$–$$$$ |
| Oquirrh | 92 | 82 | **86.9** | ~4.6 | $$$ |
| HSL | 90 | 79 | **84.3** | ~4.4 | $$$ |
| Pago | 89 | 69 | **78.4** | ~4.5 | $$$ |
| Urban Hill | 89 | 61 | **73.7** | ~4.5 | $$$$ |
| **Red Iguana** | 75 | 39 | **54.1** | ~4.6 | $$ |
| Cafe Rio | 49 | 14 | 26.2 | ~4.2 | $ |
| The Cheesecake Factory | 4 | 10 | 6.3 | ~4.1 | $$ |

**The Red Iguana result is the v3 thesis in one row:** S=75 (elite scratch) but I≈39 (decades-stable menu, reviews cluster on "authentic/traditional" not "inventive") → G≈54, dropping it from #6 on the scratch axis to mid-pack. Scratch ≠ interesting; a repeat diner's objective and a tourist's diverge, and G captures the divergence.

---

## Multi-city restaurant calibration (Inner Sunset SF · Berkeley)

Runs from user's decade-of-experience areas. R/$/hours documented (Google, this session); S/I/G are estimates (S scored holistically here, not per-criterion P/V/S/C/O; I-axis ±8); ◆ = marker-item find, ★ = canonical reference.

### Inner Sunset, SF (θ≥4.0, rank by G)

| Venue | S | I | **G** | R | $ | Note |
|---|--:|--:|--:|--:|:--:|---|
| Arizmendi ★◆ | 80 | 72 | **75.9** | 4.7 | $ | Worker co-op; sourdough croissants + daily-rotating pizza (high δ). *Bakery-bridge* |
| San Tung ◆ | 78 | 72 | **74.9** | 4.4 | $$ | Iconic dry-fried wings + hand-made dumplings; closed Tue/Wed |
| Nopalito ◆ | 76 | 60 | **67.5** | 4.3 | $$ | Nixtamalized masa; *geo: NoPa, not Inner Sunset proper* |
| Lavash ◆ | 68 | 57 | **62.3** | 4.3 | $$ | House Persian dough/tahdig |
| Manna | 68 | 55 | **61.2** | 4.5 | $$ | Scratch Korean, seafood pancake |
| CyBelle's | 62 | 58 | **60.0** | 4.5 | $$ | House vegan cheese, full vegan menu |

Filtered (S<60): Pacific Catch, Crepevine (chains).

### Berkeley (θ≥4.0)

| Venue | S | I | **G** | R | $ | Note |
|---|--:|--:|--:|--:|:--:|---|
| Chez Panisse ★ | 95 | 80 | **87.2** | 4.6 | $$$$ | Origin of CA farm-to-table (Waters); daily-changing prix fixe |
| Cultured Pickle Shop ◆ | 78 | 72 | **74.9** | 4.8ⁿ⁼¹³⁶ | – | Fermentation specialist, in-flux seasonal — user's fermentation interest; wknd-limited |
| Gather | 74 | 62 | **67.7** | 4.4 | $$ | Seasonal CA, cashew-cream pizza |
| FAVA ◆ | 72 | 58 | **64.6** | 4.8 | – | House pita/bread, herb-forward; lunch |
| Farmhouse Thai | 66 | 58 | **61.9** | 4.7 | $$ | Elaborate Thai; ⚠ upsell/pricing complaints |
| Tarocco | 66 | 55 | **60.2** | 4.7 | – | Composed seasonal salads; lunch |
| Revival Bar+Kitchen | 64 | 54 | **58.8** | 4.3 | $$$ | ⚠ E-flag: "pizza sauce tasted out of a jar" |

**Note:** Chez Panisse (87.2) is the highest restaurant G recorded across all calibration sets — appropriate for the concept that *defines* the scratch/seasonal category. Marker-method wins: San Tung (hand-made dumplings), Nopalito (nixtamal masa), FAVA (house pita), Cultured Pickle (fermentation).

---

## Marker-item seed search (likelihood-ratio method)

A complementary way to *find* candidates (the rubric *ranks* them). The scorecard estimates P(scratch | venue features); a marker search estimates P(scratch | serves item X). Pick items X with no viable industrial/frozen substitute and the posterior → 1 by construction:

P(scratch | X) = P(X | scratch) / [P(X | scratch) + P(X | ¬scratch)·prior-odds(¬scratch)]

Even at low recall (P(X|scratch) small — few scratch places serve soufflé), P(X | ¬scratch) → 0 (a reheat kitchen *cannot* produce it), so the ratio → 1. **High precision, low recall — a seeding strategy, not a scoring one.** Blind spot: misses scratch places whose menu lacks a marker; use to seed the candidate set, never to bound it.

**Three physical mechanisms that make a food frozen-incompatible:**
1. **Ice-crystal rupture** — slow commercial freezing through the −1 to −5°C (30–23°F) zone grows extracellular crystals → ~5–15% drip loss + texture collapse on thaw. Kills custards, foams, fresh cheese, delicate crumb.
2. **Starch retrogradation** — amylopectin recrystallizes fastest at ~4°C (39°F), so refrigeration *accelerates* staling; gives fresh bread/tortilla/pasta an hours-long window no thaw-hold chain can serve.
3. **Emulsion/foam thermal fragility** — hollandaise stable only ~52–63°C (126–145°F); breaks on freeze/thaw, must be built minutes before service.

**Marker items ranked by P(scratch | serves it)** — *these are category-3 personal priors, ±0.1, ordinal not measured:*

| Marker | Mechanism | P(scratch) |
|---|---|--:|
| Soufflé | foam collapse ~2–5 min | ~0.98 |
| Hollandaise/béarnaise to order | emulsion window | ~0.92 |
| House-pulled mozzarella/burrata | casein peak in hours | ~0.90 |
| House charcuterie / pâté en croûte / terrine | no supply exists | ~0.88 |
| Real multi-day mole | 20–30 components | ~0.85 |
| Fresh tempura | crust window <5 min | ~0.85 |
| Plated-to-order composed dessert | assembly + custard | ~0.83 |
| Naturally-leavened open-crumb sourdough | fermentation + crumb | ~0.82 |
| Nixtamalized masa / fresh-pressed tortilla | retrogradation | ~0.80 |
| Fresh rolled/extruded egg pasta | ice damage + texture | ~0.78 |

**Cuisine-indexed markers** (best 2–3 per cuisine — doubles as a way to find scratch *within a target cuisine*):
- **French:** soufflé, hollandaise to order, canelé, pâté en croûte
- **Italian:** house mozzarella/burrata, fresh egg pasta, multi-hour ragù
- **Mexican:** nixtamalized masa / tortilla pressed to order, multi-day mole, tlacoyos/sopes
- **Greek/Mediterranean:** house-made phyllo (~0.9 — almost nobody sheets their own; commercial is universal), pita puffed to order, house spanakopita
- **Japanese:** fresh tempura, house dashi, hand-cut soba
- **Chinese:** hand-pulled/hand-cut noodles, xiao long bao (hand-folded), dry-fried wings
- **New American:** plated-to-order composed dessert, house charcuterie, whole-animal butchery

**Anti-markers (LR < 1 — presence is neutral-to-negative, these *are* the frozen regime):** molten lava cake, cheesecake wedge, crème brûlée (Sysco sells a gelatin-set frozen version → weak marker, P~0.5), calamari rings, mozzarella sticks, "crispy chicken," wings, generic dinner rolls. Croissants ambiguous (Bridor par-bake, P~0.45) unless lamination verified.

**As search queries:** the *item* is the filter — `soufflé [city]`, `house-pulled mozzarella [city]`, `nixtamal masa tortillas [city]`, `pâté en croûte [city]`, `eggs benedict scratch hollandaise [city]`.

---

## Size-gate, catchment & exhaustive enumeration (mandatory pre-step)

**Step 0 — define the market as a resident's catchment, not town limits.** The market is **anywhere a resident would reasonably drive to from home** — roughly a **15–20 min drive, resident-normal** — *including standalone countryside venues* (a kitchen-garden gastropub 4 miles out is IN). Exclude only when the drive crosses into a **different town's** catchment (that town is its own run). Do **not** filter out rural pubs/inns for being outside the town core — if locals would casually drive there for dinner, it counts.

**Step 1 — census the catchment from OpenStreetMap/Overpass BEFORE scoring (this is now executable, not aspirational).** Discovery must be **popularity-neutral and category-blind** — keyword/prominence search silently drops whole cuisines (no "Georgian" query → the Georgian place never appears). The census primitive that fixes this at the root is the Overpass API, reachable via `curl` (tested working; `web_fetch` cannot — it's provenance-locked and can't set headers):

```
BBOX="south,west,north,east"          # the drive-time catchment
Q='[out:json][timeout:120];nwr["amenity"~"^(restaurant|cafe|fast_food)$"]('"$BBOX"');out center tags;'
# mirrors — main endpoints are load-flaky (expect 504/406); fall through:
for ep in https://maps.mail.ru/osm/tools/overpass/api/interpreter \
          https://overpass-api.de/api/interpreter \
          https://overpass.osm.ch/api/interpreter; do
  curl -s --max-time 90 -A "scorecard/1.0 (contact)" "$ep" --data-urlencode "data=$Q" -o census.json -w "%{http_code}\n"
  head -c1 census.json | grep -q '{' && break; sleep 3
done
```

**Standardized boundary (v8.4 — tested; prevents run-to-run drift AND under/over-reach):** three fixes from live runs. (1) **User-Agent mandatory** (blank UA → 406). (2) **For a named incorporated place, prefer its real OSM admin polygon over any hand-drawn or derived circle** — it's reproducible *and* correctly shaped (follows the actual town sprawl, not a geometric circle). (3) **Radius is NOT a universal constant** — calibrate it to market type.

**Boundary method, in priority order:**

```
# A) NAMED PLACE → use its real admin polygon. Look up the relation, then map_to_area.
#    Do NOT use the area(3600000000+relid) id-offset form — it silently returns 0 on some
#    boundaries (observed: Millcreek id-offset = 0 venues; map_to_area = 101). Always verify non-zero.
UA="scratch-scorecard/8.4 (research; contact)"
cat > /tmp/q.txt <<'EOF'
[out:json][timeout:90];
rel["name"="Millcreek"]["boundary"="administrative"]["admin_level"="8"];
map_to_area->.a;
( nwr["amenity"~"^(restaurant|cafe|fast_food|pub|bar)$"](area.a); );
out center tags;
EOF
for ep in https://maps.mail.ru/osm/tools/overpass/api/interpreter \
          https://overpass-api.de/api/interpreter https://overpass.kumi.systems/api/interpreter; do
  curl -s -m 90 -A "$UA" -X POST "$ep" --data-urlencode "data@/tmp/q.txt" -o census.json -w "%{http_code}\n"
  head -c1 census.json | grep -q '{' && break; sleep 3
done
# VERIFY non-zero. If the area query returns 0 (unclosed boundary / bad admin_level), FALL THROUGH
# LOUDLY to the derived box below — never silently shrink to a hand-picked radius.

# B) DERIVED RADIUS BOX (fallback, or for markets that aren't a single named place):
python3 -c 'import math;lat,lon,r=40.6892,-111.8293,12;dla=r/111;dlo=r/(111*math.cos(math.radians(lat)));print(f"{lat-dla:.4f},{lon-dlo:.4f},{lat+dla:.4f},{lon+dlo:.4f}")'
```

**Radius calibration by market type (the r=12km default is NOT universal):**
- **Standalone town, countryside around it** (Shrewsbury, Midway): **r ≈ 12 km** — the ring is farmland + villages a resident drives to; the box correctly grabs the rural gastropub tail (admin-area *under*-reaches here, missing 67 rural venues in Shrewsbury).
- **Town embedded in a dense contiguous metro** (Millcreek in the SLC valley): a 12 km circle **over-reaches** — it annexes several *other* towns (12 km around Millcreek = 1,138 venues, most of the valley). Use **admin polygon + a small ~2–3 km ring** for the immediately-adjacent neighbourhoods only (Millcreek proper = 101). The catchment is "this town + what abuts it," not "everything within 12 km."
- **Rule:** if the radius ring lands mostly in *other incorporated towns*, shrink it (metro case); if it lands in *countryside*, keep 12 km (standalone case). Record method + polygon/center + radius in the ledger either way.
Returns **every** tagged venue in the box (name, `cuisine`, coords, hours, website), unranked — e.g. a Millcreek catchment returned **502 restaurants** vs. ~50–60 for a keyword union, surfacing Georgian/Balkan/Chilean/Polynesian/Navajo spots that keyword search structurally cannot. **Bakeries: swap** `["shop"~"^(bakery|pastry|confectionery)$"]` and route to the bakery scorecard (category hygiene).

**Step 2 — triage + enrich + score.** Strip chains (blocklist), then for each remaining independent pull menu/reviews and run S/I/E. Keyword/web/places search is now **enrichment only — judging named candidates, never discovering them.** The ~untagged bucket (venues with no `cuisine` tag) is where oddities hide (Georgian, Navajo, Polynesian all surfaced untagged) — it needs a **name-by-name scratch pass**, which is the residual precision work.

**Honest boundary — census ≠ reality.** OSM is near-complete for established venues but misses **new/unlisted/informal** spots, and some independents are untagged. Report: "N enumerated per OSM; M scored; tail = untagged/new/unlisted." This bounds the miss-rate to near-zero on *established* venues (the London failure mode) without claiming a true census. **If a run has no `curl`/Overpass access** (e.g. an assistant with only prominence-ranked search): say so explicitly and treat the output as a **bounded keyword-union approximation, not enumeration** — with the cuisine × geography grid as the miss-rate ledger.

### Completion discipline (anti-laziness) — the census changed what "done" means

The census makes the tail *visible*; the judgment steps around it are where shortcuts silently re-introduce prominence bias and turn enumeration back into approximation. **Post-census, "done" = every enumerated venue has either a positive disqualifying signal or an opened menu.** The failure is not trying-hard-enough; it's *non-completion masquerading as completion*. Hard rules:

1. **Zeroing requires a positive disqualifying signal, never the absence of prominence.** "Never heard of it / didn't surface in guides / not obviously chef-driven" is NOT grounds to cut a census venue — that's the exact bias the census exists to defeat (the whole point is finding what a "top restaurants [city]" search can't). A cut needs an actual tell: wet-led boozer (bar-snacks-only menu), confirmed chain, carvery/batch-format, or an assembly/frozen menu confirmed on inspection. **Service format is NOT a disqualifier — takeaway/counter-only is orthogonal to scratch** (hand-pulled-noodle counters, nixtamal taquerías, hole-in-the-wall Thai/Sichuan are often intensely scratch AND takeaway). Judge the production signal, never the service model — same as S is orthogonal to ownership. When ~40–55% of "obviously skip" untagged pubs turn out scratch on opening (observed), inspection-zeroing is disallowed for the untagged tail.

2. **Tag-mine before you search (exhaust free signal first).** The raw Overpass response carries far more than name/cuisine: `food=yes`, `microbrewery`/`brewery`, `real_ale`/`craft_beer` (wet-led tell), `diet:*`, `cuisine`, `website`/`contact:website` (domain reveals chains — Wetherspoon/Greene King/Chef&Brewer/tied-house groups), `description`, `opening_hours`. Keep the **full tag set**, not 5 fields. Website-domain + food-tag mining alone disqualifies chains and separates food-led from wet-led pubs at **zero search cost**. Only then spend searches on survivors.

3. **The recall ledger is hard counts, and "unresolved" ≠ "excluded."** Report the funnel as explicit numbers at every stage: *enumerated → chains stripped → tag-mine disqualified → opened-by-name → scored*. Any venue not individually opened is listed as **unresolved (named)**, never silently dropped. A shortlist "I'd search first" must be labeled as such — never presented as the scratch population. (Anti-pattern from the field: presenting "~15 scratch venues" when the true count was 25–40 and the 15 was just the search-first set.)

4. **Region-pin every enrichment query.** Ambiguous place names default to the higher-traffic homonym (bare "Shrewsbury" → Shrewsbury, Massachusetts). Always append country + county/state or a postcode/street token ("Shrewsbury Shropshire UK", "SY1").

5. **Batch the tail efficiently, but batch ≠ skip.** Use curated-list cross-referencing (`"best gastropubs [county]"`, Michelin/Bib/AA-Rosette lists) to resolve many untagged venues per search — but every unresolved name still gets resolved, by list-match or individual open, before the run is called complete.

### Completion is a GATE, not a report (v8.1 — the ledger is necessary but not sufficient)

v8's recall ledger made non-completion *visible*; it did not make it *forbidden*, and a run can cite the discipline while violating it — listing un-opened venues as "unresolved" and then shipping a finished-looking occasion matrix on top, or asking the user "want me to resolve the rest?". **That hand-off is outsourced laziness: authorizing an omission the rules already forbid.** Hard gates:

6. **Full resolution is a precondition for producing the occasion matrix — not a follow-up.** A run with *any* enumerated venue neither disqualified-with-a-positive-reason nor opened is **INCOMPLETE and must continue**, not "complete with caveats." Do not render the top-3-per-occasion output until the census is fully resolved. Rendering the polished layer early is what makes a run *feel* done and licenses parking the remainder — so the presentation layer is gated on completion. (Genuine census-misses — new/unlisted venues absent from OSM — are the *only* legitimate residual; everything the census returned must be resolved.)

7. **No permission-seeking hand-off for census venues.** Never end with "want me to resolve the unresolved Indian/Japanese/etc. cluster?" for anything already enumerated. Opening the tail is part of the deliverable, not an optional extra the user must authorize. (Legitimate to ask about genuinely *new scope* — a wider catchment, a different city — never about finishing the current census.)

8. **Cuisine/format-parity tripwire.** Before finishing, check the unresolved+disqualified buckets for skew: if an entire cuisine or format is un-opened or zeroed (e.g. "the ~15 Indian houses and ~5 Japanese — none audited," or "curry houses gated as takeaway-adjacent"), that is **format-prejudice zeroing** — the same absence-of-prominence cut v8 bans, applied to a whole category instead of one venue. A spice-grinding/live-tandoor Indian kitchen or a house-dashi sushi-ya clears S≥60 on production intensity alone. Any cuisine skew in the un-opened set must be resolved before completion, and the non-European/non-obvious tail is exactly where the "who's doing [cuisine] right" winners and rare-finds hide, so it is the *highest* priority to open, not the lowest.

### Minimum-evidence standard (v8.2 — "resolution" and "scoring" have an evidence floor)

The prior gates force every venue to be *resolved* and every score to be *rendered only when complete* — but they don't define what counts as resolution or a valid score, so both degrade into lazy glances: format-inference disqualifies, and scores get rendered on asserted (never-pulled) inputs. Fixes:

9. **A disqualification requires POSITIVE evidence of not-scratch — never a null signal.** Absence of an OSM `food`/`cuisine` tag is *absence of evidence*, not evidence of absence, and must NOT be used to cut (OSM undertags pub/café food badly — e.g. ~15/114 UK pubs food-tagged, so "no food tag" DQs the exact rural-gastropub tail where scratch hides). Valid disqualifiers are all *positive*: a chain confirmed by website domain; an opened menu showing assembly/reheat/frozen-commodity product; a wet-led signal (`real_ale`/`bar` with bar-snacks-only menu, confirmed). **Service format (takeaway/counter/delivery-only) is NOT a disqualifier** — it's orthogonal to production; a chippy frying fresh-battered whole fillets is scratch while a sit-down room microwaving commodity product is not. The tell is always the *production signal on the opened menu*, never the service model. If the only "signal" is a missing tag or the takeaway format, the venue is **unresolved (must open)**, not disqualified.

10. **R is a *filter*, so it must be *pulled*, not asserted.** The decision rule gates on R ≥ θ; a venue may only be marked as passing that gate if its rating was actually retrieved (documented, with n). "Clears 4.0★" without a pulled number is **unverified → the venue is unresolved**, not passing. Do not populate the scored table from asserted ratings.

11. **Per-number provenance; the scored/occasion output renders only from VERIFIED rows.** Every S/I/E/R/$ value carries a provenance tag: **documented** (pulled/opened this run), **estimated** (model inference from partial signal), or **unverified** (asserted, not checked). A venue may appear in the reader-facing occasion matrix / ranked output **only if its R is documented and its S rests on an opened menu** — estimated I/V is acceptable (the I-axis is inherently ±8) but R and the scratch call are not. Venues scored on a single blurb, asserted rating, or cuisine-nature reasoning stay in the audit ledger tagged *thin-evidence*, not in the recommendation. (This is the per-number version of the documented-vs-estimated discipline the whole rubric already demands: enforce it on each figure, not once per run.)

12. **Verification-completeness is part of the completion gate.** A run is not complete when every venue is *resolved*; it is complete when every venue in the *rendered output* has documented R + opened-menu S, and every *disqualification* rests on positive evidence. "Resolved by inference" is not resolved. If the search budget can't cover verifying the shortlist, **narrow the catchment** (smaller area, fully verified) rather than render a wide-but-inferred table — narrow-and-verified beats wide-and-asserted.

13. **Three states, not two — "exhausted-unavailable" is a terminal state, so runs can actually close.** The floor is documented / estimated / unverified — but that leaves no terminator for a venue where the researcher *did the work* and the evidence genuinely isn't on the pullable web (common for real under-reviewed scratch holes-in-the-wall). Without an exit, such venues loop forever ("audit unless a documented rating is found") and the run never completes. Add a terminal state:
   - **exhausted-unavailable** = the field was searched in the standard sources and is provably absent. This is **valid and terminal — not a failure, not a retry.** It is distinguished from lazy-unresolved (which stays forbidden) by **demonstrated search effort: the worker must list where it looked** (e.g. "no Google/Yelp/TripAdvisor rating found; searched name+city+‘reviews’"). Exhaustion without a documented search trail is just laziness wearing a new label — reject it.
14. **A documented rating is a filter, not an absolute gate, for scratch-verified venues.** The R≥θ gate exists to keep a scratch *dump* out of the recommendation — but a venue with **documented production nouns (S clears) and R exhausted-unavailable** is not a dump; it's under-reviewed, which for a genuine scratch hole-in-the-wall is common and even *correlates* with the find. Such venues go to a **"scratch-verified, rating-unconfirmed" tier**: surfaced in the output *with that explicit caveat*, neither silently dropped nor promoted into the rating-gated tiers. (Tres Hombres pattern: real sauce-prep evidence, no pullable ≥4.0 source → "we confirmed the scratch cooking; couldn't confirm a rating — your call," not deletion.) Estimated/unverified R still cannot enter any tier; only *documented* or *exhausted-unavailable* R is a terminal, renderable state.

### Parallelize resolution with subagents (v8.3 — preferred when available)

The completion gates keep collapsing into inference because full-tail resolution is one serial slog against a budget, and cheap-inference temptation accumulates as the context fills. **Fan the resolution stage out to subagents whenever the environment supports them** — each worker carries a small, verifiable load, so the effort never piles up in one place and the shortcut pressure that drives format-inference never builds. This is the single biggest reducer of completion resistance.

- **Orchestration:** after the census + chain-strip + tag-mine, split the surviving unresolved venues into batches (~10–20 each) and dispatch one subagent per batch to open + verify them in parallel; the orchestrator merges returns, applies scoring, and renders only verified rows.
- **Recursive fan-out — a subagent with too many venues re-splits instead of grinding.** A worker handed a large batch (e.g. 75 pubs) serially hits the *same* accumulation-of-effort pressure the split was meant to remove — it will start inferring around venue ~50. So **any subagent whose batch exceeds the leaf size (~10–15) must itself re-split and spawn children**, rather than working the list serially. Depth 2–3 covers thousands of venues (1 → ~10 batches → ~100 leaves) and is much faster (a 75-venue/15-min serial batch becomes ~6 parallel leaves finishing in ~2–3 min). **Discipline is inherited at every level:** a spawning subagent passes the *identical embedded standard brief* (below) to its children verbatim — never a paraphrase — and rejects thin child-returns exactly as the top orchestrator does. Floor propagates to every level or it holds at none. **Bounds:** split until batches ≤ ~10–15, then stop (don't over-fork); cap depth at ~3.
- **Model tiering — research leaves run on CHEAP/fast models; orchestration stays smart.** The researcher role is deliberately dumb work: open a URL, pull a number, match menu text against the fixed production-noun list, emit a structured row. That's constrained extraction against an explicit checklist — no scoring, no judgment — which is exactly where a cheap/fast model is reliable *and* lets you fan out wide for less. **The intelligence stays in the orchestrator** (S/I/E scoring, occasion routing, scarcity reasoning, tier assignment, completion gate) — those do NOT drop to a cheap model. **The evidence floor is what makes cheap workers safe:** the brief constrains them to a rigid contract (explicit tokens, fixed noun list) rather than free-form judgment, so they can't hallucinate ratings or accept adjectives — constrained extraction is a cheap-model strength. Consequence: the orchestrator's **reject-thin-returns step is now load-bearing, not a formality** — a weaker worker is likelier to slip a marketing adjective past or bare-stamp "unavailable," so the orchestrator must actually enforce the noun-list and the search-trail requirement on every returned row.
- **Subagents inherit the v8.2 evidence floor — this is mandatory, or you've merely parallelized the laziness.** Each worker's instruction must require, *per venue*: an opened menu/site with the **specific production nouns** that set S (house pasta / nixtamal masa / spice-grinding / live-fire — not vague "home-cooked"), a **pulled rating with n**, and cuisine/format. The orchestrator **rejects thin returns** (asserted ratings, adjective-only reads, missing-tag DQs) and re-dispatches — parallelism amplifies whatever discipline it's handed, so a lazy subagent brief produces fast, wide, *unverified* output.
- **Also parallelize the census fan-out** for large/partitioned metros (one subagent per neighbourhood bbox) and the marker-item / rare-finds tail-verification.
- **Fallback (no subagent support):** resolve serially, but then the "narrow the catchment" rule (11–12) binds harder — without parallelism, a fully-verified small area beats a partially-inferred large one. Never let absence of subagents become the excuse that reauthorizes inference.

**Standard subagent brief — EMBED this verbatim, do not just cite "v8.2".** A subagent is a fresh context with only the text you hand it; "follow the evidence floor" is a pointer to a document it cannot see and does zero work. Inline the whole floor, version-free:

```
You are a scratch-kitchen evidence RETRIEVER. Your job is to COLLECT raw evidence, NOT to
judge, score, categorize, or conclude. Return what the sources literally say; the orchestrator
does all analysis. Do not decide whether something "counts."

PER VENUE, return these RAW fields (quote/copy literally; never summarize into a verdict):
  venue name (+ address as listed)
  | RATING: the literal rating string(s) as found, each with source and count
      e.g. "Google 4.3 (812); TripAdvisor 4.0 (149)". If none found after searching, "none found".
  | PRICE: as shown ($/££/number) or "-"
  | HOURS: as shown or "-"
  | MENU/ABOUT QUOTES: copy the actual lines from the menu/website that describe how food is
      made or sourced — VERBATIM, 1–6 short quotes. Include whatever they say, flattering or not
      ("pasta made fresh in-house daily", "hand-rolled", "frozen", "we use fresh ingredients",
      "battered to order"). Do NOT filter, judge, or label these — just copy them. If the site
      has no such lines, "no production language found".
  | CUISINE / FORMAT: as listed (e.g. "Thai, takeaway") — descriptive only.
  | WEBSITE DOMAIN: the actual domain (lets the orchestrator spot chains).
  | SEARCH TRAIL: where you looked (which sites/queries), always.
  | SOURCE URLS.

DO NOT return any of these (they are the ORCHESTRATOR's job, not yours):
  - an S/scratch score or band, a pass/fail, a "confidence", or a "likely scratch: yes/no"
  - a decision about whether the menu quotes "count" as production evidence
  - a disqualification verdict. Instead, just report the raw facts (domain, "menu shows frozen X",
    "bar only serves crisps", "permanently closed per Google") and let the orchestrator decide.
  Reporting a fact ("website is greeneking.co.uk", "menu lists 'boil-in-bag'") is your job;
  concluding "DQ: chain" is not.

RULES:
  1. NEVER infer, estimate, or round a rating — copy the literal number+count+source, or "none found".
  2. Copy menu/about language exactly, including unflattering or marketing phrases — the orchestrator
     separates production nouns from adjectives, not you. Your job is to not LOSE any of it.
  3. Report format/cuisine descriptively; never treat takeaway/counter/delivery as disqualifying.
  4. Missing info after a genuine look = say so with your search trail ("no rating on Google/Yelp/
     TripAdvisor/site"). That is a valid terminal answer. Never fabricate to fill a field.
  5. Region-pin ambiguous names (county/state + country, or street/postcode).
  6. If your list is > ~10–15 venues, SPLIT and spawn child retrievers, passing THIS BRIEF verbatim;
     collect their raw returns. Do not grind a long list serially.
```
Orchestrator (the SMART model, sole judgment layer): from each raw return, apply the production-noun vs. marketing-adjective test to the verbatim quotes, band S, apply the R≥θ gate to the literal rating (or route to "scratch-verified, rating-unconfirmed" when quotes show scratch but rating = none-found-after-trail), decide DQs from the reported facts (domain→chain, quotes→assembly), and score. **Reject/re-dispatch any return that smuggled in a verdict instead of raw evidence, or that has an empty search trail.** Keep judgment at this level only; workers below never conclude.

**Size-gate (determines partition, not whether to enumerate):** Small town (one core + rural ring) → one catchment sweep. Medium city → sweep + a few sub-area passes. Large metro → **partition by neighbourhood** and enumerate each (a single metro-wide sweep still truncates to the prominence head). Enumeration-first is mandatory at every size; partition is what scales it.

**Category hygiene:** a venue surfaces in exactly one scorecard by its primary type. A bakery-café is a bakery; a restaurant that bakes its own bread is a restaurant. Never let bakeries leak into the restaurant ranking or vice-versa — the enumeration's type tags prevent this.

---

## Copy-paste travel prompt

> **Step 0 — catchment.** Define the market as everywhere a resident would reasonably drive to (~15–20 min, incl. standalone countryside venues); exclude only what falls into a *different town's* catchment.
> **Step 1 — enumerate first, filter second.** Census the catchment from a places/map directory swept by category (high recall, with type tags) BEFORE scoring — do not use ad-hoc web search for discovery (it truncates to the prominence head and misses institutions). Then web-search only for scratch/process signals on the enumerated candidates. Route bakeries to the bakery scorecard by their type tag. Report recall (enumerated N / scored M / tail).
>
> **Completion is a GATE, not a caveat (do NOT hand off the tail):** do not produce the occasion matrix until EVERY census venue is either disqualified-with-a-positive-reason or opened. A run with un-opened venues is incomplete and must continue — never ship a polished matrix with an "unresolved: ~15 Indian, ~5 Japanese…" list appended, and never end by asking "want me to resolve the rest?" for venues already in the census (that's outsourcing the omission the rules forbid). If a whole cuisine/format is sitting un-opened (curry houses, sushi, ethnic spots), that's format-prejudice zeroing — open them FIRST, because the non-obvious tail is where the "who's doing [cuisine] right" winners and rare-finds hide. Only genuinely new scope (wider area, different city) is a legitimate thing to ask about.
>
> **Minimum-evidence floor (a DQ or a score must not be a lazy glance):** (1) **disqualify only on POSITIVE evidence** of not-scratch — a missing OSM food/cuisine tag is NULL signal, not a disqualifier (OSM undertags pub/café food; "no food tag" cuts the exact rural tail where scratch hides) → missing-tag-only means *open it*, don't cut it. (2) **R is a hard filter, so PULL it** — a venue only "passes R≥4.0" if you retrieved the number (with n); asserted "clears 4.0" = unresolved. (3) **Per-number provenance:** tag every S/I/E/R/$ as documented / estimated / unverified, and put a venue in the reader-facing output ONLY if its R is documented and its scratch score rests on an opened menu (estimated I is fine). Thin-evidence venues stay in the audit ledger, never the recommendation. (4) If budget can't verify the shortlist, **narrow the catchment** — narrow-and-verified beats wide-and-asserted.
>
> **Use subagents whenever available (this is the fix for completion resistance):** after census + chain-strip + tag-mine, split the unresolved venues into ~10–20-venue batches and dispatch one subagent per batch to open + verify in parallel; merge and render only verified rows. Each subagent MUST inherit the evidence floor — return, per venue, the specific production nouns setting S (house pasta / nixtamal / spice-grinding — not "home-cooked"), a pulled rating with n, and format; reject thin returns and re-dispatch. Parallelize the census fan-out per-neighbourhood for metros too.  Subagents with large batches re-split and spawn children (leaf ~10-15 venues, depth ~3), passing the same embedded brief down verbatim. Research leaves run on CHEAP/fast models (constrained extraction against the fixed checklist); orchestration/scoring stays smart; the evidence floor makes cheap workers safe, so the orchestrator MUST enforce the noun-list + search-trail on every returned row. No subagent support → resolve serially and narrow the catchment; never let their absence reauthorize inference.
>
> I'm visiting **[CITY]** and want restaurants that are **scratch-made AND interesting to a frequent diner** — not assembly-and-reheat, and not a static menu I'd tire of by visit 2. Using web search (menus, sites, reviews, rating histograms), score candidates on two axes, filter, and rank.
>
> **Axis 1 — S_scratch (0–100).** Score menus by base-prep load, not item count: factor each menu into its grammar (base × protein × sauce × format); distinct base preps K = sum of the axis sizes even if orderable items N is large. High N/K over a coherent single cuisine (taquería, mole house, dim sum, deli, BBQ) is POSITIVE — don't penalize large N there.
> (1) Base-prep load/grammar /20 — K≲20 → 20, 20–35 → 14, 35–55 → 8, flat encyclopedia → 0–3. (2) Volatility/seasonality /25 — weekly/dated → 25, seasonal → 18, static → 0. (3) Sourcing/production /30 — named farms + ≥3 house-made markers → 30, some → 18, vague → 6, photo menu → 0. (4) Coherence /15 — single focus → 15, two adjacent → 10, grab-bag → 5, 3+ cuisines → 0. (5) Operator /10 — chef-owned 1–3 loc → 10, independent → 7, regional group → 5, franchise → 0.
>
> **Axis 2 — I, interestingness (0–100).** (δ) menu turnover /35 — weekly/daily change → 35, seasonal → 22, static → 0 (this is the strongest proxy). (A) ingredient ambition /30 — density of rare/high-effort techniques & ingredients (koji, garum, verjus, 'nduja, fermentation, house-cultured) → 30, conventional → 8. (ν) review novelty ratio /20 — freq(creative/inventive/"never had") ÷ freq(classic/comfort/consistent). (π) rating polarization /15 — a fat 1–2★ tail alongside 5★ signals ambition (weak proxy).
>
> **R is a filter, not a score.** The star rating only estimates first-visit satisfaction; it's blind to repeat novelty. Do NOT rank by it.
>
> **Decision rule:** (1) filter to {R ≥ 4.0★ AND S ≥ 60}; (2) rank survivors by G = √(S × I). If I want a novelty tilt, use G′ = S^0.4 · I^0.6.
>
> **Price:** include $ (Google 1–4 bucket) as a neutral display column — do NOT let it affect the score.
>
> **Resort/tourist-town heuristic:** the easiest main-strip walk-ins skew tourist-grade; real scratch kitchens are usually one block off the drag or reservation-gated. Surface off-strip options I'd miss.
>
> **Day-part neutrality:** breakfast/brunch/lunch-only is NOT a negative signal — score S and I on the food itself, never on when it's served. A lunch-only scratch kitchen ranks on the same S×I basis as a dinner spot. Include breakfast/lunch/deli/bakery-café candidates, not just dinner restaurants, and always surface each venue's hours and day-part (breakfast / brunch / lunch / dinner) plus closed days.
>
> **Output:** ranked table — Restaurant | S | I | G | R★ | $ | Hours/day-part | one-line rationale | confidence (High/Med/Low = how much menu/reviews actually revealed). Show filtered-out venues separately with the reason (failed θ vs. failed S-floor). Don't invent K, counts, δ, ratings, or hours — estimate and mark low-confidence when data isn't visible.

## Sharing Results

Want to share your results? Generate an HTML page with the occasion matrix and ranked tables, then use `/gisthost` to publish it as a shareable website. See `reference/gisthost.md` for details.
