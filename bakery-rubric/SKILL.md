# Scratch-Bakery Scorecard & Travel Prompt (v8.8)

Companion to the restaurant scorecard. Finds bakeries that are **made from raw components on-site AND interesting to a frequent buyer** — screening out **par-bake** (partially-baked frozen dough units, finished on-site) and commissary/frozen-dough café cases.

*Versioning: this and the restaurant scorecard share one version line (both at **v8.8**) and bump together, since they share the retrieval, presentation, scarcity, and execution machinery. Per-file changelogs below track each instrument's own feature history; the headline version is shared.*

**v8.8 change (model tiering):** research leaves run on cheap/fast models (constrained extraction is a cheap-model strength); orchestration stays smart; evidence floor makes cheap workers safe, so orchestrator enforcement is load-bearing. **v8.7 change (exhausted-unavailable state):** third terminal state (searched-and-absent, with a stated search trail) lets runs close instead of looping; scratch-verified + rating-exhausted bakeries route to a "scratch-verified, rating-unconfirmed" tier rather than being dropped. **v8.6 change (recursive fan-out):** subagents with large batches re-split and spawn children (leaf ~10-15, depth ~3) rather than grind serially; embedded brief propagates verbatim to every level. **v8.5 change (embeddable subagent brief):** inline the full evidence floor into the subagent prompt verbatim (workers can't see the rubric); enumerate production nouns vs. marketing adjectives; ban rating-inference and format-DQs; orchestrator rejects thin returns. **v8.4 change (boundary method):** prefer real OSM admin polygon (rel→map_to_area, not id-offset area() which silently returns 0; verify non-zero, loud fallback); radius calibrated by market type (standalone→12km; town-in-metro→polygon+small ring). **v8.3 change (subagents):** parallelize tail resolution with subagents when available (biggest reducer of completion resistance); subagents inherit the evidence floor, thin returns rejected. **v8.2 change (minimum-evidence floor):** disqualify only on positive evidence (missing OSM tag ≠ cut); R pulled not asserted; per-number provenance, reader output only from documented rows. **v8.1 change (completion is a gate):** full census resolution now a precondition for rendering output; no permission-seeking hand-off of the tail; cuisine/format-parity tripwire. **v8 change (completion discipline / anti-laziness):** post-census "done" = every enumerated bakery has a positive disqualifier OR an opened check; no zeroing-by-unheard-of; tag-mine before searching; hard-count recall ledger ("unresolved" ≠ "excluded"); region-pin queries.

**v7 change (executable census — Millcreek-tested):** retrieval is now a real `curl` → OpenStreetMap/Overpass census returning every tagged bakery in the catchment bbox (popularity-neutral), replacing aspirational "enumerate first"; web/places search demoted to enrichment-only; honest per-OSM boundary + fallback when no census API. Millcreek: 29 bakeries vs. ~12 keyword.

**v6 change (retrieval — user-flagged on Shrewsbury):** market redefined as a **resident drive-time catchment** (~15–20 min, countryside included; excludes other towns' catchments); discovery moved to **exhaustive places-directory enumeration first, web-filter second** (fixes non-retrieval misses where runs surfaced different venues). Reader output reordered (occasions top, audit bottom); **Home/Trip toggle retired from reader output** into methods only.

**v5 change (market-scarcity axis — user-validated on Enjoy Vegetarian):** interest split into two independent novelty sources — **δ (menu turnover, flow)** and **A_scarcity (market rarity of the offering, stock)**. A static-menu place can be maximally interesting on scarcity alone; δ no longer dominates. Added the **rare-finds layer** (item-ranked, scratch-gated, within-market scarcity) and the **foodie-occasion presentation model** (occasions → top-3, scores demoted to audit).

**v4 change (user-validated on Acme):** the v3 "presume capacity from volume" rule is now bounded — it applies to *retail* volume only. **Wholesale volume (supplying stores/restaurants) suppresses I via standardization pressure, while S stays high.** Corrected Acme Bread (over-scored G 76.7 → ~65.0: kept S≈92, dropped I 64→46). Wholesale/retail ratio is now an explicit I-axis input.

**v3 change (register-independence, user-validated on Jane vs. Fort Negen):** the S-core-craft and I-ambition criteria were partly measuring *whether reviews use artisan/process vocabulary* — a signal confounded by marketing register, reviewer selection, and possibly review language/country. Fix: **weight register-independent physical descriptors (shatter, open crumb, crust, "fresh from oven," sell-out) over process vocabulary; absence of process language is NOT evidence of par-bake; presume production capacity from revealed review volume.** This corrected Jane the Bakery (G 66.6 → ~75.1).

**v2:** added the E (execution) axis with cadence-deconfounding + café-bakery R-decomposition. **v1:** category-conditional core-craft (bread/lamination/pâtisserie tracks) + input sourcing.

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

---

## Why the bakery model differs from the restaurant one

The enemy isn't reheating — it's **par-bake**. Industrial suppliers (Bridor, Rich's, Dawn Foods, Aryzta/La Brea, General Mills & Pillsbury frozen, Otis Spunkmeyer for cookies) ship frozen par-baked or frozen-raw dough that a café thaws, proofs, and finishes. The output is visually indistinguishable from scratch. Consequences:

- **Photos carry ~0 information.** A gorgeous croissant case can be 100% Bridor. Never score on images.
- **Sell-out cadence inverts to a top signal.** Par-bake's economic purpose is deep frozen inventory → all-day availability that never runs out. A bakery that posts daily quantities and sells out by ~11am physically cannot be doing that. Cadence + fermentation language are the two strongest scrapeable tells.
- **The "everything case" is a strong negative.** A small scratch bakery specializes because you cannot mix, laminate, proof, and bake croissants + bagels + cakes + macarons + donuts + pies + bread all daily. Breadth across unrelated categories implies multiple frozen supply streams.

---

## S_bakery (0–100)

| # | Criterion | Wt | Bands |
|---|---|--:|---|
| 1 | **Core production craft** (score MAX of the 3 tracks) | 30 | **Bread track:** levain (natural sourdough culture), long/cold fermentation, named hydration %, "takes days," mixed & shaped in-house. **Lamination track:** house-laminated viennoiserie (butter block folded in-house, NOT frozen dough sheets) — croissant/kouign-amann/cruffin/escargot range. **Pâtisserie track:** from-scratch components — macaronage, entremets (layered mousse cakes), tempered couverture (real chocolate), house pastry cream/curds/jams, sugar work. Deep in ≥1 track → 30 · competent but shallow → 18 · "fresh/artisan," no process → 8 · uniform units, zero process (par-bake signature) → 0. Rationale: prevents the bread-only bias that under-scores elite pâtisseries; a no-levain macaron/entremet shop scores on the pâtisserie track. |
| 2 | **Input sourcing** | 20 | flour (stone-milled/named mill: Central Milling, Hayden, Lehi Roller, King Arthur; heritage grains) AND/OR named non-flour inputs (single-origin couverture, named local dairy, real vanilla vs. flavoring, local seasonal fruit) → 20 · some named/organic inputs → 13 · "quality ingredients," unnamed → 5 · none → 2. Broadened from flour-only so pâtisseries get credit for chocolate/dairy/fruit sourcing. |
| 3 | **Breadth ÷ production capacity** | 20 | Score breadth *relative to demonstrated production capacity*, NOT raw breadth (a large operation with visible production kitchen, multi-shift staff, and per-category process evidence can legitimately make 100+ SKUs in-house). Specialist (few base doughs/components → many SKUs) OR large-with-visible-multi-line-production + per-category scratch evidence → 18–20 · coherent focused shop → 14 · broad but plausibly in-house → 8 · wide case in a small footprint with NO per-category process evidence (par-bake signature) → 0–3. The tell is the breadth-to-production-evidence ratio, not width alone. |
| 4 | **Bake cadence / perishability** | 20 | documented sell-out / IG-announced daily batches / morning-only / "get there early" → 20 · "baked fresh daily," some sellout → 13 · full-day availability, restocked → 6 · all-day identical availability, never out (par-bake signature) → 0 |
| 5 | **Operator / format** | 10 | baker-owned, 1–2 locations, visible bakeshop → 10 · independent single café-bakery → 7 · regional chain that mills/bakes in-house (e.g., Great Harvest) → 5 · multi-unit café with display case, no visible production → 0–2 |

**Bands:** 80–100 near-certain scratch · 60–79 scratch-leaning · 40–59 mixed (scratch + par-bake) · <40 likely par-bake/commissary.

### Register-independence rule (v3)

Criteria 1 (core craft) and I-ambition must be scored on **physical/textural product descriptors, not vocabulary presence**, because process-language density is confounded by three things independent of actual craft:
- **Marketing/positioning register:** an artisan-positioned shop advertises "levain, 20-hr ferment"; a broad-popular shop of equal craft says "so many options, all fresh."
- **Reviewer selection:** high-volume popular bakeries attract casual reviewers (physical descriptors, no jargon); small artisan shops attract enthusiasts (process jargon).
- **Review language/country (hypothesis, weak evidence):** in a small n≈5/venue sample, Amsterdam bakeries showed ~3× the explicit "sourdough/naturally-leavened" density vs. US large-popular bakeries — origin uncertain (Dutch *zuurdesem* is common-register; OR English-language NL reviews skew to food-travelers; OR translation artifact). Bound as "a register gap exists, mechanism unresolved," not a clean cultural fact.

**Scoring rules that follow:**
1. **Physical descriptors are load-bearing evidence.** "Shattering/flaky layers" = lamination (criterion 1, lamination track). "Open irregular crumb, blistered crust" = high-hydration natural leavening. "Sells out by 11am" = cadence. These are register-independent and survive the popularity confound. Weight them ≥ explicit process vocabulary.
2. **Absence of process vocabulary is NOT evidence of par-bake.** Do not dock a bakery for reviewers not saying "levain." Par-bake is indicated by *positive* anti-signals (uniform units, never-sells-out, "tasted frozen"), not by the *absence* of jargon.
3. **Presume production capacity from revealed volume.** A bakery with >1,000 reviews + broad selection + "shattering-fresh" product demonstrably has the throughput to make it in-house — you cannot fake that volume of fresh product. Apply the breadth÷capacity criterion by presuming capacity, not requiring it to be stated.

**Worked case — Jane the Bakery (SF):** originally G=66.6 (core craft ~19 for "shattering croissants, fresh baguettes, dark breads" read as non-technical; breadth docked to ~12). Corrected: "shattering" credited as a lamination signal (core craft ~25), breadth presumed from 1,363-review volume (~16), ambition credited for the actual range (I ~67). **S≈84, G≈75.1** — vs. Fort Negen 77.8, matching the user's "very similar vibes" read (Δ was ~90% measurement artifact, ~0% real production difference).

### Retail vs. wholesale volume (v4) — bounds the register/capacity rule

The v3 "presume capacity from volume" rule applies to **retail** volume only. Volume must be split by *who it serves*, because the two have opposite implications:

- **Retail volume** (walk-in customers; high review count): → presume production capacity, do NOT penalize S. Popularity confound (Jane).
- **Wholesale volume** (supplies grocery/restaurant accounts): → **suppress I, keep S.** A bakery shipping a consistent SKU to hundreds of accounts is under standardization pressure: δ (turnover) → low, per-item execution optimizes for *consistency across accounts*, not *peak*. High S (still scratch), low I (not interesting for a frequent buyer). This is the **Great Harvest pattern** (S=74/I=40).

**Add wholesale/retail ratio as an explicit I-axis input:** heavy wholesale → cap δ and A regardless of scratch quality.

**Worked case — Acme Bread (Berkeley):** originally scored S≈92 / I≈64 / **G=76.7 (#1)** — over-scored by letting wholesale scale read as capability. User ground-truth: "good but nothing special, big industrial producer supplying stores/restaurants." Correction keeps **S≈92** (genuinely naturally-leavened, Sullivan/Chez Panisse lineage — the scratch call was right) but drops **I 64→~46** (wholesale standardization suppresses novelty). **G=√(92×46)≈65.0**, moving it from #1 to ~#4 — "high-S, mid-I" = "good but nothing special," exactly matching the read. Acme is Great Harvest with better bread.

Note: criteria 1, 2, and 4 all load partially on one "on-premise production" factor (effective independent dimensionality ~3). Weights put the direct process/cadence signals (1+4 = 50) ahead of the input proxy (flour, 2) so a bakery that mills great flour but finishes frozen dough still scores low.

---

## I_bakery (0–100)

| Proxy | Wt | Scrape method / bands |
|---|--:|---|
| **δ rotation** | 25 | seasonal galettes/tarts, laminated special of the week, monthly flavor rotations, "this week's bake." Weekly/seasonal → 25, static year-round case → 0. Only realized by frequent buyers. |
| **A_scarcity — market rarity** | 25 | *Can you get this bake elsewhere in this market?* Rare regional/traditional item with no local peer (a specific hand-made specialty absent elsewhere) → 25; uncommon → 15; widely available → 5. **Independent of δ** — a fixed offering nobody else makes stays maximally rare. The dining analog of a frozen-incompatible marker. |
| **A_technique — ambition** | 20 | viennoiserie beyond plain croissant (kouign-amann, cruffin, bostock), high-hydration/heritage-grain breads, laminated brioche, complex inclusions → 20 · plain-only → 5 |
| **ν flavor novelty** | 18 | review terms creative/unique/"never had"/"can't get elsewhere" ÷ classic/standard/traditional |
| **π polarization** | 12 | rating-histogram dispersion; fat low-star tail = ambition. Hypothesis-grade, weakest |

**Two kinds of traditional-excellence (both static-menu, opposite occasions):** *perfected-common* (low A_scarcity — a supremely-made common item → "reliable standby / best [item] in the city") vs. *rare-cuisine/rare-item* (high A_scarcity — a hand-made specialty with no local peer → "the one thing worth crossing town for," even though it never changes). The δ/A_scarcity split routes them correctly.

---

## Decision rule
1. **Filter:** R ≥ θ (**≈4.3★** — bakery ratings inflate ~0.2–0.3★ vs. restaurants, so 4.0 is non-discriminating) AND S ≥ 55.
2. **Rank** survivors by G = √(S × I). Novelty tilt: G′ = S^0.4 · I^0.6.
3. **Price** displayed, not scored. **Surface hours + sell-out timing** (a 4pm arrival at a sells-out-by-11 bakery is a miss regardless of score).

### Dual-rank: Home vs. Trip mode (compute both, toggle on trip-frequency)

The correct data model is **two rankings, not one** — a venue's rank depends on whether you'll visit repeatedly or once. Feldman's Deli is the canonical case: user verdict "very good but always exactly the same → not motivated to return, but would definitely recommend to an out-of-town visitor." Those are two correct-but-opposite ranks (Millcreek #10 home / #4 trip) for one venue.

- **Home mode (frequent visitor):** rank by **G = √(S·I)**. Novelty is live — you'll sample the menu over ~N/s visits, so δ/ambition (I) matters.
- **Trip mode (one-shot):** rank by **S**, gate {R ≥ θ}, tie-break on **low E-variance**. Rationale: (a) I is noise for a single draw; (b) the **S–E floor effect** — in the validated sample, S ≥ 75 → E ≈ 87–95 (~8-pt band), so mean-E is redundant with S and stops discriminating. What remains is *variance*: which high-S place is least likely to hand you one bad draw. Favor all-day-fresh > sells-out-by-11, un-rushed > throughput-bottlenecked, specialist > broad-case. (E-variance is currently a **flagged annotation from structural proxies** — pop-up / sell-out-window / broad-case / chef's-choice — not a fitted term; mean-E known for ~6 venues, variance for ~0.)

**Two signals sign-flip with mode** (auto-invert on toggle):

| Signal | Home | Trip |
|---|---|---|
| Wholesale scale | −I (standardization kills novelty; Acme) | **+** (lowest single-draw variance = safest one-shot) |
| Sell-out cadence | +S (fresh limited batches; criterion 4) | **−** (freshness-variance if you can't time the AM window) |

**Effect:** the two modes converge where S and I are coupled (fine-dining scratch scenes — top places are both scratch *and* novel), and diverge only for the two I-decoupled classes — traditional-excellence (Feldman's, Red Iguana, Antica) and wholesale-standardization (Acme, Hartog's). Trip mode re-elevates exactly the venues home-mode I-penalties demoted. Worked reorder (Berkeley bakeries): Acme #4 home (G 65.0) → **#1 trip** (S 92, wholesale = lowest variance).

**Worked case — Ballerina Farm Store, Midway (largest trip-swing in dataset, ▲3).** Farm-store bakery/café (opened June 2025; Ballymaloe-trained chef Catherine Clark; owners' 10M-follower brand). **S≈71** — driven by near-max input sourcing (~19/20: raise/grow/mill most inputs + Gracie's Farm partner) and real in-house daily sourdough/focaccia/croissant, register-discounted hard given the maximum-marketing brand. **I≈39** — deliberately traditional/nostalgic menu (low δ, low A). G_home = √(71·39) ≈ **52.6 → #7 of 8 in Midway**; trip-S = **71 → #4**. The ▲3 swing is the traditional-excellence signature, amplified because Midway's S values cluster tightly (64–82), so a high-S/low-I venue leapfrogs several mid-pack spots on the sort-key switch.

Three flags on this case: (1) **R≈4.3★ (Google, n≈290)** — clears θ but *low relative to 10M-follower reach*; bimodal π (superfan 5★ tail + "overhyped/overpriced" 1–2★ tail), so the mean carries little resolution. (2) **R_baked under-determined** — grocery/experience/soft-serve reviews contaminate the food signal; can't isolate bread/pastry sentiment at this n (the brand-halo cousin of café-service R-contamination). (3) **E unmeasured** — <1-yr operation; S is production-signal, not eaten-quality, and trip-mode E-variance is structurally *high* (brand-tourism crowds, all-day grocery model, new kitchen) — the one place a high S doesn't protect a single draw. Illustrates that **maximum brand register + maximum sourcing still yields a mid G** when I is low — the register-independence rule (v3) refusing to let 10M followers move the score.

### Top-tier resolution & the E→return finding (v5, Thessaloniki-validated)

First dataset case of an **actual return-visit choice between two rubric-scored venues** (Grandma Sofia's G 72.9 vs. Bougatsa TO NEON G 68.9). Findings:

1. **Resolution floor:** a G-gap of **4.0 < the ±8 I-error band = a statistical tie**, not an ordering. Rule: **present venues within ~8 G of each other as a tier, not a rank.** The rubric cannot resolve differences below its own I-axis error.
2. **N vs. δ are distinct and use-conditioned.** TO NEON had higher **N** (instantaneous menu breadth); Sofia's had higher **δ** (recipe turnover). δ is *only realized by a frequent buyer* over ~N/s visits — a one-shot/few-visit patron experiences **N**, not δ. **Rule:** trip/few-visit → score I on N (realized breadth); home/frequent → score I on δ. Do not credit δ to a visitor who won't return enough to experience the rotation (the error made scoring Sofia's I via "dozens of rotating pites" for a 1-visit patron).
3. **E — not I — drives returns at the top tier.** Both the user's return choice (Sofia's, on "spectacularness of flavor," small gap) and locals' habitual default (TO NEON's single perfected bougatsa) were execution/consistency-driven, not novelty-driven. At the top tier S saturates (~87–90), E saturates (~90–92), and the I-gap falls inside its error band — so the operative decision variable collapses onto **E**, which the model relegates to annotation. **Mastery override (hypothesis-grade, n=1 support):** elite fixed item (E ≳ 92) caps the δ penalty — mastery substitutes for novelty in driving repeat visits.
4. **⚠ Open architectural question (not encoded):** should E enter the *home objective* as a top-tier tie-break (within a G-tie band, order by E not I)? The one return choice says yes, but n=1 comparison is insufficient to rebuild the objective. Watching for the next return-visit data point.



---

## E — execution axis (v2 addition; separate column, NOT folded into G)

**Why separate from G:** G = √(S×I) answers "is this my kind of place?"; R was supposed to be the execution proxy but lacks resolution — at n≈50–70 reviews a 0.2★ gap (e.g., Beaucoup 4.5 vs. Table X Bread 4.7) is only ~2 SE (SE ≈ SD/√n ≈ 0.8/√67 ≈ 0.10★) and can't separate "scratch and good" from "scratch and world-class." Execution lives in review **text**, which is higher-resolution and independent of the star scalar. A high-G / B-execution place is still worth surfacing, so E annotates rather than re-ranks.

**E (0–100)** = clamp( 100·[1 − α·D_A − β·(1−c)·D_B + γ·D_C] , 0, 100 ), classifying each **product** mention (exclude service/price/parking/ambiance):
- **Class A — intrinsic defects** (timing-independent): gummy, dense, underbaked/raw, bland, "needed more [X]", artificial, unbalanced, greasy, burnt. Weight α≈1.0.
- **Class B — freshness/timing-confounded**: dry, stale, hard, "day-old", "older". Weight β≈0.2, **cadence-immunized by (1−c)**.
- **Class C — positive markers**: "perfect crust", "shattering", "the star", "melt-in-mouth", "exquisite", "best I've had". Credit γ≈0.3.
- c = cadence factor ∈ [0,1] from criterion 4/20. **α, β, γ are design choices, not fitted.**

**The cadence-deconfound (key insight):** selling out → staler late-day remainder → more "dry/older" reviews. Staleness thus *correlates positively with scratch*; naive defect-density would penalize the most scratch bakeries. The (1−c) term zeroes out Class-B penalties for high-sellout shops. Worked example — Beaucoup at 5pm sold-out: naive E ≈ 82, deconfounded (c≈0.6) E ≈ 87, matching user ground-truth ("really good, B+, wouldn't ding hard").

**Optional secondary filter:** flag E < 85. **Caveat:** E computed from ~5 review snippets is a category-3 approximation (±5–8); it needs a full-corpus text-mine before the flag is trustworthy — one burnt-crust review currently drives Eva's E=84 entirely.

### R-contamination for café-bakeries (v2, user-validated on Tulie)

Aggregate R conflates **three products** at a café-bakery: (1) baked goods, (2) coffee/drinks program, (3) service/throughput. A broad drinks menu + high traffic mechanically depresses R via (2)+(3) even when (1) is elite — and crowding correlates with being *good*, so popularity generates the complaints that lower R. This is the R-side twin of the sell-out→staleness confound.

**Rule:** when a bakery is also a high-volume café (coffee program + broad menu + crowding/wait mentions), do NOT gate on aggregate R. Instead:
- Compute **R_baked** = rating sentiment scoped to baked-goods mentions only, and apply θ to that; or
- Gate on **E_baked** (text-scoped execution) directly.

**Worked case — Tulie:** aggregate R=4.4 (Google) / 4.3 (Restaurant Guru, n=1,489). In a ~20-statement critical sample (non-random, category-3), complaints split ≈ 60% service/price/seating, ≈ 22% coffee/drinks, ≈ 15–18% baked goods — and ~½ of the baked-goods dings are freshness-timing (Class B). Net: **R_baked ≈ 4.7–4.8 (est.), E_baked ≈ 90 (±5).** One reviewer ranks it on par with Tartine (SF) / Levain (NY). The earlier R-vs-E disagreement resolves in E's favor: aggregate R was service+coffee-contaminated, not a product signal. **Ports to the restaurant tool:** popular restaurants with big bar programs / long waits get the same R drag independent of food quality.

---

## SLC calibration set (v1, 16-bakery survey; user-validated)

S/I are estimates; process signals read off sites/reviews. R/price/hours documented from Google. Confidence: High = process signal documented; Med = review-inferred; Low = thin data / low review count. **User ground-truth anchor:** Table X Bread rated by owner as "as good as bread anywhere in the world" → the S≈85 / world-class calibration point.

| Bakery | S | I | **G** | R★ | $ | Conf | Track / signal |
|---|--:|--:|--:|--:|:--:|---|---|
| House of Bread SLC | 95 | 70 | **81.5** | 5.0 (n=7) | – | S-High/R-Low | Bread; all naturally leavened, Sat 9–12 only, sells out |
| Leavity Bread | 87 | 67 | **76.4** | 4.9 | ~$$ | High | Bread; 20-hr cold ferment, wholesales to Caputo's/Tulie |
| Table X Bread | 85 | 66 | **74.9** | 4.7 | ~$$ | Med-High | Bread+lamination; Central Milling — **world-class anchor** |
| All Purpose Bakehouse | 81 | 65 | **72.6** | 4.8 (n=128) | – | Med-High | Lamination specialist; "amazing lamination," pain suisse; Wed–Sun 8–2 |
| Fillings & Emulsions | 75 | 70 | **72.5** | 4.7 | $$ | Med | Pâtisserie track (v1 fix, was 62.0); award-winning entremets/macarons |
| Chez Nibs | 75 | 64 | **69.3** | 4.8 (n=46) | – | Med | Pâtisserie/chocolatier; kouign-amann + tempered bonbons; Wed–Sat |
| Beaucoup Bakery | 75 | 63 | **68.7** | 4.5 (n=67) | $$ | Med | Pâtisserie (entremets, Paris-Brest) + sourdough; two tracks |
| Tulie Bakery | 76 | 59 | **67.0** | 4.4 | $$ | Med | Pâtisserie track (v1 fix, was 62.0); seasonal, named dairy/chocolate |
| Vosen's Bread Paradise | 73 | 59 | **65.6** | 4.6 | $ | High | Bread; Certified Master Baker (Meisterbrief), German breads |
| Eva's Bakery | 74 | 57 | **65.0** | 4.7 | $$ | Med-High | Bread+lamination; locally-sourced flour, scratch French |
| Forty Three Bakery | 67 | 57 | **61.8** | 4.7 | $$ | Med | Lamination + café; croissants, chocolate-entremet "pinecone"; Wed–Mon |
| The Daily Dough | 72 | 55 | **62.9** | 5.0 (n=17) | – | Med | Bread; cottage sourdough/focaccia, home op + delivery |
| French Bakehouse (Holladay) | 66 | 58 | **61.9** | 5.0 (n=86) | – | Med | Lamination; sells out fast, French viennoiserie |
| Stone Ground Bakery | 78 | 43 | **57.9** | 4.5 | $ | Med | Bread; stone-milled, but wholesale + pre-order (no walk-in) |
| Good Food Gluten Free | 56 | 44 | **49.6** | 4.6 | – | Low-Med | Scratch GF niche |
| Carol's Pastry Shop | 60 | 37 | **47.1** | 4.8 | $ | Med | Pâtisserie, but static classic (low craft-depth, low δ) — v1 does NOT rescue |

**Filtered out** (fail S≥55 or R<4.3): Délice French Bakery (S≈47 — a review reports the cookie "tasted like it came out of the freezer and dethawed," par-bake tell) · Gourmandise (S≈39, broad case + full restaurant) · TOUS les JOURS (S≈18 — Korean-French franchise, frozen-dough bake-off) · Salt City Baking (S≈38, wholesale + FDA sanitation citation).

**Removed — permanently closed:** Les Madeleines (kouign-amann pioneer; shut ~2 years ago).

**Validation lessons:**
- **v1 pastry track works:** it lifts high-craft pâtisseries (F&E +10.5 G, Tulie +5.0) but leaves the static classic flat (Carol's 47.1 unchanged) — rewarding craft-depth, not merely no-bread.
- **S-axis is 3/3 on user ground-truth:** Table X Bread ✓ (world-class), Tulie ✓, Beaucoup ✓ (all confirmed scratch). The scratch detector is holding.
- **Beaucoup (user-validated):** scratch confirmed, execution "B+" — but observed at 5pm sold-out, so the staleness was a timing artifact, not a baking defect. Drove the v2 E cadence-deconfound. E ≈ 87 (deconfounded) vs. 82 (naive).
- **E-axis resolved — Tulie (user-validated):** the R=4.4 vs. positive-text disagreement is a café-bakery R-contamination artifact, NOT product unevenness. In a ~20-statement critical sample, ~60% of complaints are service/throughput/price and ~22% are the coffee program; baked goods draw only ~15–18%, half of that freshness-timing. R_baked ≈ 4.7–4.8, E_baked ≈ 90. Confirms text-E > aggregate R for café-bakeries.
- **User's favorites land #3 (Table X Bread) and #8 (Tulie)** post-fix; three untried predictions (House of Bread, Leavity, All Purpose) scored above the world-class anchor remain the top falsification test.
- **Cottage/access caveats:** House of Bread (Sat 9–12 only, n=7), Daily Dough (home op, n=17), Stone Ground (pre-order, no walk-in) carry high S but low accessibility and/or thin R.

---

## Multi-city bakery calibration (SF · Berkeley · Amsterdam)

Runs from user's decade-of-experience cities. R/$/hours documented (Google, this session); S/I/G are estimates (I-axis ±8, softer than S); ◆ = marker-item find, ★ = canonical reference; corrections from v3/v4 applied. Confidence tags omitted for brevity — treat all S/I as Med unless noted.

### San Francisco (θ≥4.3, rank by G)

| Bakery | S | I | **G** | R | $ | Note |
|---|--:|--:|--:|--:|:--:|---|
| Tartine ★◆ | 90 | 72 | **80.5** | 4.5 | $$ | Naturally-leavened reference; R café-dragged (R_baked higher) |
| b. patisserie ◆ | 85 | 74 | **79.3** | 4.7 | $$ | KA + canelé (Leong); closed Mon/Tue |
| **Arsicault** ★◆ | 88 | 68 | **77.4** | n/a | – | **User: ≥ Tartine.** E≈95 (user anchor); R not pulled. Croissant specialist |
| Neighbor Bakehouse | 84 | 70 | **76.7** | 4.7 | $$ | Bostock, twice-baked; closed Mon |
| Rize Up ◆ | 85 | 68 | **76.0** | 4.5ⁿ⁼⁸⁶ | – | Naturally-leavened, experimental; pop-up/TGTG |
| **Jane the Bakery** | 84 | 67 | **75.1** | 4.6 | $$ | **v3 corrected (was 66.6);** "shattering" = lamination signal, capacity presumed from volume |
| Sol Bakery | 76 | 66 | **70.8** | 4.4ⁿ⁼⁶² | – | ⚠ E-flag: focaccia "underbaked/raw, gummy"; weekend-only |
| Dandelion Chocolate ◆ | 68 | 64 | **66.0** | 4.7 | $ | Bean-to-bar + canelé — user's bean-to-bar interest |
| Boudin (spot-check) | 62 | 38 | **48.5** | 4.4 | $$ | Real 1849 mother-dough, but tourist-static (low I) |

### Berkeley / East Bay (θ≥4.3)

| Bakery | S | I | **G** | R | $ | Note |
|---|--:|--:|--:|--:|:--:|---|
| Pâtisserie Rotha ◆ | 84 | 66 | **74.5** | 4.9ⁿ⁼³⁸⁹ | $$ | Canelé, far breton; *Albany*; Thu–Sun 7:30–11am, extreme sellout |
| Fournée ◆ | 80 | 62 | **70.4** | 4.7 | $$ | "Best croissant in Bay" (contested); closed Mon/Tue |
| Belmo Café | 70 | 62 | **65.9** | 4.8 | – | Algerian/French, baklava, alfajor |
| **Acme Bread** ★◆ | 92 | 46 | **65.0** | 4.8 | $ | **v4 corrected (was 76.7);** S high (Sullivan levain) but wholesale → I-suppression. User: "good but nothing special" |
| La Farine (spot-check) | 64 | 50 | **56.6** | 4.6 | $$ | ⚠ E-flag: "croissants barely better than Safeway"; *Oakland* |

### Amsterdam (θ≥4.3)

| Bakery | S | I | **G** | R | $ | Note |
|---|--:|--:|--:|--:|:--:|---|
| **Patisserie Linnick** ◆ | 84 | 74 | **78.9** | 4.9ⁿ⁼⁶⁴⁵ | €€ | **User's favorite patisserie.** Pâtisserie track; origin-blended vanilla (Indonesia/Comoros/Tahiti); low-sugar → fruit clarity (E≈90). Macaron E-variance flagged |
| Fort Negen ◆ | 84 | 72 | **77.8** | 4.7 | – | Naturally-leavened farmer sourdough + creative cruffins |
| Olafbrood | 86 | 64 | **74.2** | 4.9ⁿ⁼¹⁷³ | – | Sourdough + madeleines, open bake, gives starter away |
| Brothers Niemeijer ★◆ | 85 | 64 | **73.8** | 4.5 | – | Naturally-leavened + laminated (Gebroeders N.); R café-dragged |
| Hartog's ◆ | 88 | 60 | **72.7** | 4.8 | € | **Mills its own grain**; wholegrain sourdough + appeltaart; sells out ~4pm |
| Craft Coffee & Pastry ◆ | 78 | 66 | **71.7** | 4.9 | – | 100% GF *laminated* croissant (no frozen-GF supply = strong scratch signal); Wed–Sat |
| Le Fournil de Sébastien ◆ | 82 | 62 | **71.3** | 4.8 | $$ | Authentic French, canelé, "alveoli" croissant; closed Sun |
| Rise Bakery | 76 | 66 | **70.8** | 4.8 | – | Italian-owned, creative laminated cruffins |
| Petit Gâteau ◆ | 76 | 64 | **69.7** | 4.7 | $$ | Pâtisserie (Gerkens): tarts, Parisian flan, entremets |

**Cross-city validation:** references self-sort to the top (Tartine #1 SF, Chez Panisse tops Berkeley restaurants, Linnick tops Amsterdam by user's own call). Two user-caught misses both hit the **I-axis, not S**: Jane (under, register bias → v3) and Acme (over, wholesale I-suppression → v4). The S-axis (scratch detection) has 6/6 on user ground-truth; residual error concentrates in I (interestingness), which is inherently softer to infer from text.

---

## Thessaloniki calibration (hand-phyllo city; user firsthand-validated)

Foreign-market run. **Dominant marker = hand-stretched phyllo** (P≈0.90) — but note phyllo has a *universal industrial substitute* (unlike copper-mold canelé), so "serves bougatsa" is insufficient; the signal is **hand-stretched, verified/observed** (Bantis "in the air," Sofia's rolled in view, TO NEON "δικό μας χειροποίητο φύλλο"). Register-independence (v3) is load-bearing: Greek reviews are ~pure physical/cadence descriptors, near-zero levain jargon — absence ≠ par-bake. R mostly sentiment-estimated (unverified-numeric) **except TO NEON (4.7★, n=895, RG+Google — documented).**

| Bakery | S | I | **G** | R | Note |
|---|--:|--:|--:|--:|---|
| Choureál (choux specialist) | 88 | 66 | **76.2** | ~4.6 est | Paris-Brest ◆; à-la-minute (lowest E-variance); S+I coupled → #1 both modes. *Untested by user* |
| MLRT Sourdough microbakery | 85 | 66 | **74.9** | ~4.7 est | Naturally-leavened, 18-hr ferment; House-of-Bread analog, thin n |
| **Grandma Sofia's** ◆ | 87 | 61 | **72.9** | ~4.6 est | Hand village-phyllo à la minute + προζύμι breads. **User firsthand: "very amazing"; chose for return visit on flavor (E), small gap** |
| **Bougatsa TO NEON** ◆ | 88 | 54 | **68.9** | **4.7 (n=895)** | 3rd-gen (1970), own handmade phyllo. **User firsthand: "very amazing"; locals' habitual downtown default** |
| Bougatsa Bantis ◆ | 90 | 55 | **70.4** | ~4.7 est | Hand-phyllo, stretched "in the air," 3-gen since 1969; traditional-excellence (high-S/low-I, trip-swing) |
| ERGON 72H Artisanal | 76 | 63 | **69.2** | ~4.5 est | 72-hr cold-ferment; mild group-standardization docks operator |
| Elenidis (Trigona) ◆ | 83 | 46 | **61.8** | ~4.5 est | Hand-phyllo since 1956; single perfected item (Feldman's pattern) |

**Filtered/trip-elevated:** Terkenlis (iconic tsoureki, but chain + intl shipping = wholesale-standardization → I~40, G~47 home; re-elevates trip mode as the reliable shippable souvenir — the Acme inversion).

**Sofia's vs. TO NEON — the validated top-tier tie (see v5 findings above):** G-gap 4.0 < ±8 error = **tie, not an ordering**. User confirmed both "very amazing"; return choice (Sofia's) was **E-driven (flavor), not I-driven** — and TO NEON actually had higher **N** (realized breadth for a single visit) while Sofia's higher **δ** (rotation) was latent/unrealized for a 1-visit patron. The rubric's I-based ordering coincided with the user's choice but was not its cause. **Coverage note:** TO NEON (55-yr institution) was *missed entirely* in the first-pass search — the failure mode was non-retrieval, not mis-scoring, arguing for a mandatory marker-item coverage pass (`χειροποίητο φύλλο` + city).

---

## Marker-item seed search (bakery)

Complement to the rubric: search for items with **no viable par-bake/frozen substitute**, so P(scratch | serves it) → 1 (see restaurant scorecard for the likelihood-ratio derivation). High precision, low recall — seeds candidates, doesn't bound them.

**Bakery marker items** (category-3 personal priors, ±0.1):

| Marker | Why frozen-incompatible | P(scratch) |
|---|---|--:|
| Canelé | copper molds + beeswax, same-day custard interior | ~0.90 |
| House-made phyllo | almost nobody sheets it; commercial is universal | ~0.90 |
| Kouign-amann (verified lamination) | caramelized laminated dough, hours-fresh | ~0.85 |
| Naturally-leavened open-crumb sourdough | par-bake can't fake irregular high-hydration crumb | ~0.82 |
| Fresh stroopwafel (pressed to order) | Dutch marker — batter griddled à la minute | ~0.88 |
| Laminated brioche / pain suisse | in-house butter block, not frozen sheet | ~0.80 |
| Paris-Brest / choux to order | craquelin choux + praline cream, no frozen version | ~0.80 |

**Anti-markers (P~0.4–0.5, these ARE the par-bake regime):** plain croissant with no lamination claim (Bridor), muffins from batter pails, generic bagels, cookie-dough-tub cookies, sheet-cake with piped roses, "brownies."

**As queries:** `canelé [city]`, `house-made phyllo [city]`, `kouign-amann [city]`, `naturally leavened sourdough [city]`, `stroopwafel fresh made [city]`, `Paris-Brest [city]`.

---

## Size-gate, catchment & exhaustive enumeration (mandatory pre-step)

**Step 0 — market = a resident's catchment, not town limits.** Everywhere a resident would reasonably drive to (~15–20 min, resident-normal), **including standalone countryside venues**; exclude only what falls into a *different town's* catchment.

**Step 1 — census the catchment from OpenStreetMap/Overpass BEFORE scoring (executable, not aspirational).** Discovery must be popularity-neutral. Keyword search silently drops venues; the Overpass census returns every tagged bakery in the box. Reachable via `curl` (`web_fetch` cannot — provenance-locked, no headers):

```
BBOX="south,west,north,east"          # drive-time catchment
Q='[out:json][timeout:120];(nwr["shop"~"^(bakery|pastry|confectionery)$"]('"$BBOX"');nwr["cuisine"~"bakery|pastry|dessert"]('"$BBOX"'););out center tags;'
for ep in https://maps.mail.ru/osm/tools/overpass/api/interpreter \
          https://overpass-api.de/api/interpreter https://overpass.osm.ch/api/interpreter; do
  curl -s --max-time 90 -A "scorecard/1.0 (contact)" "$ep" --data-urlencode "data=$Q" -o census.json -w "%{http_code}\n"
  head -c1 census.json | grep -q '{' && break; sleep 3
done
```
Returns every tagged bakery/patisserie (name, shop-type, cuisine, address, hours) unranked — a Millcreek catchment returned **29** vs. ~12 for a keyword union, surfacing Argentine-empanada, Levantine, and Korean bakeries keyword search missed. It also cleanly tags the par-bake chains (85°C, Tous les Jours, Corner Bakery) for correct filtering.

**Standardized boundary (v8.4 — tested):** **User-Agent mandatory** (blank UA → 406); **for a named place prefer its real OSM admin polygon** over a hand/derived circle (reproducible + correctly shaped) — look up the relation and `map_to_area` it (NOT the `area(3600…+id)` id-offset form, which silently returns 0 on some boundaries; verify non-zero and fall through *loudly* to a derived box on failure, never silently shrink). **Radius is not a universal constant:** standalone town w/ countryside → r≈12 km (grabs the rural tail admin-area misses); town in a dense contiguous metro → 12 km over-reaches into other towns, so use **admin polygon + a ~2–3 km ring** (e.g. Millcreek proper = 101 vs. 12 km circle = 1,138 = most of the valley). Rule: ring lands in other towns → shrink; ring lands in countryside → keep 12 km. Record method/polygon/center/radius in the ledger. Full command in the restaurant scorecard.

**Step 2 — triage + enrich + score.** Strip chains/par-bake, then pull process/cadence signals per survivor and run S/I/E. Web/places search = enrichment only, never discovery.

**Honest boundary — census ≠ reality.** OSM misses new/unlisted/home/stall/pre-order bakers (exactly the microbakery tail). Report "N per OSM; M scored; tail = untagged/new/unlisted/cottage." **No `curl`/Overpass access** → say so; treat output as a bounded keyword-union approximation, not a census.

### Completion discipline (anti-laziness) — post-census, "done" = every enumerated venue has a positive disqualifying signal OR an opened check

The census makes the tail visible; shortcuts around it silently re-introduce prominence bias. Rules:
1. **Zeroing needs a positive disqualifier, not absence-of-prominence.** "Never heard of it" is not a cut — it's the census working. Cut only on a real tell: par-bake/frozen chain (85°C, Tous les Jours, Corner Bakery — website domain reveals these), all-day-never-sells-out café case, confectionery/dessert-only format.
2. **Tag-mine before searching.** Keep the full Overpass tag set (`shop`, `cuisine`, `website`, `opening_hours`, `description`) — website domains disqualify chains at zero search cost; open the rest.
3. **Hard-count recall ledger; "unresolved" ≠ "excluded."** Report enumerated → chains stripped → tag-mine disqualified → opened → scored. Never present a search-first shortlist as the scratch population.
4. **Region-pin every query** (country + county/state or postcode; bare town names default to the higher-traffic homonym).

**v8.1 — completion is a GATE, not a report.** The ledger makes non-completion visible but not forbidden. (a) **Full resolution is a precondition for rendering the occasion output** — a run with any enumerated bakery neither disqualified-with-reason nor opened is INCOMPLETE and must continue, not "complete with caveats." (b) **No permission-seeking hand-off** — never end with "want me to open the rest?" for census venues; opening the tail is the deliverable, not an optional extra. (c) **Cuisine/format-parity tripwire** — if a whole category is un-opened or zeroed (e.g. all Asian/ethnic bakeries, all "dessert cafés"), that's format-prejudice zeroing; a shop hand-making an ethnic specialty clears the gate on production alone, and the non-obvious tail is where rare-finds hide — highest priority to open.

**v8.2 — minimum-evidence floor (resolution and scoring aren't lazy glances).** (a) **A DQ needs POSITIVE evidence of not-scratch, never a null signal** — absence of an OSM `shop`/`cuisine`/`food` tag is absence of evidence (OSM undertags badly), so it can't disqualify; missing-tag-only → *unresolved (must open)*, not cut. Valid cuts: par-bake chain by domain, opened case showing frozen/all-day-never-out, confectionery-only on inspection. (b) **R is a gate, so it must be pulled, not asserted** — "clears 4.3★" without a retrieved number → unresolved. (c) **Per-number provenance; render only VERIFIED rows** — every S/I/E/R/$ tagged documented / estimated / unverified; a bakery appears in the reader-facing output only with documented R + opened-process S (estimated I is fine). Thin-evidence bakeries stay in the audit ledger, not the recommendation. (d) **If budget can't verify the shortlist, narrow the catchment** — narrow-and-verified beats wide-and-asserted. (e) **Three states, not two — "exhausted-unavailable" is terminal.** A bakery where the researcher did the work but the evidence genuinely isn't on the pullable web (common for under-reviewed microbakeries) needs an exit, or the run loops forever. **exhausted-unavailable** = searched the standard sources, provably absent → valid and terminal, distinguished from lazy-unresolved by **demonstrated search effort (list where you looked)**; exhaustion without a search trail is laziness relabeled — reject it. (f) **Documented rating is a filter, not an absolute gate, for scratch-verified bakeries:** a bakery with documented process (levain/lamination confirmed) but R exhausted-unavailable is under-reviewed, not disqualified — it goes to a **"scratch-verified, rating-unconfirmed" tier**, surfaced with that explicit caveat rather than dropped. (Estimated/unverified R still can't render; only documented or exhausted-unavailable is terminal.)

**v8.3 — parallelize with subagents (preferred when available).** Full-tail resolution collapses into inference because it's one serial slog against a budget; **fan resolution out to subagents whenever the environment supports them** (biggest reducer of completion resistance). Split surviving unresolved bakeries into ~10–20-venue batches, one subagent each, opening + verifying in parallel; orchestrator merges and renders only verified rows. **Recursive fan-out:** a subagent handed too large a batch must **re-split and spawn children** rather than grind serially (a big list hits the same accumulation-of-effort pressure that drives inference); split until batches ≤ ~10–15, cap depth ~3. **Discipline propagates:** a spawning subagent passes the *identical embedded brief* (below) to its children verbatim and rejects thin child-returns — the floor holds at every level or none. **Model tiering:** research leaves run on **cheap/fast models** (the role is constrained extraction against a fixed checklist — open URL, pull rating, match the production-noun list — a cheap-model strength); **orchestration stays smart** (scoring, scarcity, tiers, completion gate never drop to cheap). The evidence floor is what makes cheap workers safe (rigid contract, not free-form judgment) — so the orchestrator's reject-thin-returns step becomes load-bearing: enforce the noun-list + search-trail on every row a weaker worker returns. **Subagents inherit the v8.2 evidence floor (mandatory):** each returns, per bakery, the **specific production nouns** that set S (levain/lamination/house-milled — not "fresh-baked"), a **pulled rating with n**, and shop-type; orchestrator **rejects thin returns** and re-dispatches. Also parallelize the census fan-out (per-neighbourhood) and rare-finds verification. **Fallback (no subagents):** resolve serially and let "narrow the catchment" bind harder — never let absence of subagents reauthorize inference.

**Standard subagent brief — EMBED verbatim (a subagent can't see this file; "follow v8.2" does nothing):**

```
You are a scratch-bakery evidence researcher. For each bakery below, open its official
site/menu/Instagram and pull its rating. Return ONLY the structured table — no prose, no guessing.

PER BAKERY (every field required; use "unavailable"/"none found"/"unresolved" — never infer):
  bakery | rating (number + count + source) or "unavailable" | price or "-" | hours + sell-out
    timing or "-" | PRODUCTION NOUNS (concrete, from site) or "none found" | DQ (positive only) or "-"
    | URLs

PRODUCTION NOUNS — what counts: naturally leavened / levain / sourdough starter; long/overnight
cold ferment; hydration %; house lamination (butter block folded in-house), kouign-amann,
croissant/viennoiserie made on-site; stone-milled / house-milled / named mill + heritage grains;
macaronage, entremets, tempered couverture, house pastry cream/curds/jams; sells-out/daily-batch
cadence; physical texture tells from reviews ("shattering layers", "open blistered crumb").
  DO NOT accept as evidence (MARKETING): "fresh-baked", "artisan", "homemade", "traditional",
  photos of nice pastries. Par-bake looks identical to scratch in photos — never score on images.

RULES:
  1. Never infer a rating; "unavailable" if not retrieved.
  2. Disqualify ONLY on positive evidence: par-bake/frozen-dough chain (by website domain — e.g.
     85°C, Tous les Jours, Corner Bakery); an opened case confirmed all-day-never-sells-out with
     no process language; confectionery/dessert-only format; permanently closed.
  3. Missing info is NOT a fail — mark "unresolved" for re-dispatch (absence of evidence ≠
     evidence of absence; OSM/sites undertag small bakers badly).
  3b. But don't loop forever: if you searched the standard sources (Google/Yelp/TripAdvisor/site/
     Instagram) and no rating is retrievable, mark rating "exhausted-unavailable" AND list where you
     looked — a valid TERMINAL answer. Exhaustion without a search trail = laziness.
  3c. If process is confirmed (levain/lamination real) but rating is exhausted-unavailable, tag
     "scratch-verified, rating-unconfirmed" — surfaced with caveat, not dropped.
  4. Region-pin ambiguous names (county/state + country or postcode).
  6. If your list is larger than ~10-15 venues, SPLIT it and spawn child researchers,
     passing THIS BRIEF verbatim; verify their returns the same way. Do not grind a long list
     serially. Only return rows with a pulled rating + real production nouns; mark the rest "unresolved".
```
Orchestrator rejects & re-dispatches any return with an asserted rating, adjective-only nouns, or a missing-info DQ. Only pulled-rating + real-production-noun rows enter scoring.

**Size-gate** sets partition, not whether to enumerate: small town → one catchment sweep; medium → sweep + sub-areas; metro → **partition by neighbourhood**, enumerate each. Enumeration-first is mandatory at every size.

---

## Copy-paste travel prompt

> **Step 0 — catchment:** everywhere a resident would drive ~15–20 min (incl. countryside), minus other towns' catchments.
> **Step 1 — enumerate first:** census the catchment from a places/map directory swept by category (high recall, type-tagged) BEFORE scoring — don't use ad-hoc web search for discovery (it truncates to the prominence head; runs miss known venues). Then web-search only for scratch/process signals on candidates. Report recall (enumerated N / scored M / tail).
>
> **Completion discipline (do NOT be lazy):** never zero a bakery for being unheard-of — cut only on a positive disqualifier (par-bake chain by website domain, all-day-never-out café case, dessert-only format). Tag-mine the raw census (website/shop/opening_hours) before spending searches; open every unresolved venue by name; report hard funnel counts with un-opened venues listed as *unresolved*, never silently excluded; region-pin every query (county/state + country or postcode — bare town names default to the wrong homonym).
>
> **Completion is a GATE, not a caveat:** do not render the occasion output until EVERY census bakery is disqualified-with-reason or opened. Never ship a finished-looking list with an un-opened tail appended, and never end by asking "want me to open the rest?" for census venues. If a whole category (ethnic/Asian bakeries, dessert cafés) is un-opened, open it FIRST — that's where rare-finds hide.
>
> **Minimum-evidence floor:** (1) disqualify only on POSITIVE evidence (par-bake chain by domain, all-day-never-out case, dessert-only) — a missing OSM tag is null signal, so missing-tag-only means *open it*, don't cut it. (2) R is a filter, so PULL it (asserted "clears 4.3" = unresolved). (3) Per-number provenance (documented/estimated/unverified); render a bakery in the reader output only with documented R + opened-process S. Thin-evidence stays in the audit ledger. (4) If budget can't verify the shortlist, narrow the catchment.
>
> **Use subagents whenever available (the fix for completion resistance):** split unresolved bakeries into ~10–20-venue batches, one subagent each, open + verify in parallel, render only verified rows. Each MUST return per bakery the production nouns setting S (levain/lamination/house-milled — not "fresh-baked"), a pulled rating with n, and shop-type; reject thin returns.  Subagents with large batches re-split and spawn children (leaf ~10-15, passing the same brief down). Research leaves run on CHEAP/fast models (constrained extraction against the fixed checklist); orchestration/scoring stays smart. The evidence floor makes cheap workers safe, so the orchestrator MUST enforce noun-list + search-trail on every returned row. No subagent support → resolve serially and narrow the catchment.
>
> I'm visiting **[CITY]** and want bakeries that make dough from scratch on-site (NOT par-bake/frozen) and are interesting to a frequent buyer. Using web search (bakery sites, menus, reviews, Instagram), score candidates on two axes, filter, and rank.
>
> **The enemy is par-bake** (frozen dough finished on-site — Bridor, Rich's, Dawn, Aryzta). Photos are useless — score on process language and cadence, never images. The two strongest positive tells: (a) fermentation language (naturally leavened, levain, poolish, biga, overnight/cold-retard, hydration %), and (b) sell-out cadence (posts daily quantities, sells out by late morning, morning-only) — par-bake never sells out.
>
> **Score on physical descriptors, not vocabulary (register-independence).** Weight register-independent textural evidence — "shattering/flaky" (lamination), "open irregular crumb/blistered crust" (natural leavening), "sells out by late morning" (cadence) — OVER explicit process jargon ("levain," "20-hr ferment"). Absence of process vocabulary is NOT evidence of par-bake; a broad-popular bakery of equal craft just gets described casually. Presume production capacity from review volume (>1,000 reviews + broad + fresh product = has the throughput). Par-bake is flagged by positive anti-signals (uniform units, never sells out, "tasted frozen"), not by missing jargon.
>
> **S_bakery (0–100):** (1) Core production craft /30 — score the MAX of three tracks so no-bread pâtisseries aren't penalized: **bread** (levain, long/cold ferment, hydration %, OR physical: open crumb/blistered crust), **lamination** (house-laminated viennoiserie, OR physical: shattering/visible butter layers), or **pâtisserie** (macaronage, entremets, tempered couverture). Deep in ≥1 track → 30, competent-shallow → 18, generic "artisan" → 8, uniform case no process → 0. (2) Input sourcing /20 — flour (stone-milled/named mill + heritage grains) AND/OR named non-flour inputs (single-origin chocolate, named dairy, real vanilla, local fruit) → 20, unnamed → 5. (3) Breadth ÷ production capacity /20 — specialist OR large-with-demonstrated-volume + fresh product → 18–20, wide case in small footprint with no per-category evidence → 0–3. (4) Bake cadence/perishability /20 — sells out / daily batches / morning-only → 20, all-day never-out → 0. (5) Operator/format /10 — baker-owned bakeshop → 10, multi-unit café case → 0–2.
>
> **I (0–100):** (δ) rotation /35 — seasonal/weekly specials → 35, static → 0. (A) technique & grain ambition /30 — viennoiserie beyond plain croissant (kouign-amann, cruffin, bostock), high-hydration/heritage breads, laminated brioche → 30, plain-only → 8. (ν) flavor novelty /20. (π) rating polarization /15 (weak).
>
> **R is a filter, not a score** (bakery ratings inflate; use θ ≈ 4.3★). **Decision:** filter {R ≥ 4.3 ∧ S ≥ 55}, rank by G = √(S × I).
>
> **Output:** ranked table — Bakery | S | I | G | R★ | $ | Hours + sell-out timing | one-line rationale | confidence (High/Med/Low). Surface sell-out/morning-only timing explicitly. Show filtered-out venues with the reason (failed θ vs. S-floor). Flag any specialist (one-item shops — bagels, cinnamon rolls, kouign-amann) that scores low on breadth but is genuinely scratch. Don't invent hydration %, batch counts, or ratings — estimate and mark low-confidence when data isn't visible.
