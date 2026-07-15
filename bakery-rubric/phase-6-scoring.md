# Phase 6 — Bakery Scoring and Classification

**Read this file in full immediately before Phase 6. The primary orchestrator makes every decision; workers never score.**



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

## Operational decision invariants (moved from v8.2–v8.7)

- **Positive evidence only for disqualification.** Valid adverse evidence includes a frozen/par-bake chain confirmed by its domain or documentation, an opened source confirming frozen or commissary production, resale rather than production, or a permanently closed venue. A directory label, missing tag, missing jargon, service format, product breadth by itself, or an all-day schedule by itself is not a disqualifier.
- **Specialist production remains eligible only after the bakery-category gate.** Broad discovery may include chocolate, dessert, confectionery, and other adjacent producers, but final bakery eligibility requires affirmative bakery production in house: bread, pastry, laminated dough, pâtisserie, or another defined baked product. Chocolate or confectionery production alone is not bakery production; confectionery alone is category-adjacent and must not enter bakery scoring or rankings. A single-item specialist remains eligible when that item passes the bakery-production gate. Retailing only finished or resold goods is out of scope only when positive evidence establishes that fact.
- Apply this gate after evidence acceptance and before S/I/E scoring. Record the exact qualifying baked product and its production evidence. If none is accepted, use `category-adjacent-exclusion`; do not manufacture a low S score.
- **Per-number provenance remains mandatory.** Treat every S, I, E, R, and price value as documented, estimated, or unverified. Reader-facing rated tiers require documented R and an S decision grounded in accepted evidence.
- **Rating exhaustion is terminal, not negative.** A scratch-verified bakery whose rating is `exhausted-unavailable` after the required search trail goes to the explicit **scratch-verified, rating-unconfirmed** tier. It is surfaced with that caveat, neither silently dropped nor promoted into a rating-gated tier. Estimated or unverified ratings remain non-terminal.
- **Conflicts remain visible.** Preserve each literal rating, count, source, and date; prefer a direct source when resolving under the rating hierarchy, flag material discrepancies, and never synthesize a rating.

## Controlled decision dispositions

Every candidate receives exactly one disposition: `category-adjacent-exclusion`, `not-scoreable`, `status-deferred`, `evidence-exhausted`, `disqualified`, `rated-survivor`, `rating-unconfirmed`, or `scored-filtered`. `not-scoreable` is a non-negative evidence state: accepted identity or menu facts exist, but evidence is insufficient to make a defensible process score. It is never shorthand for low craft. Preserve the reason and missing evidence fields.

## Phase 6 artifact

Write every orchestrator decision, supporting evidence reference, score and provenance, disqualification rationale, conflict resolution, tier, tie, scarcity, occasion, and confidence decision to `{RUN_DIR}/06-decisions.md`. Do not write decisions into worker-return files. Update `00-run-manifest.md` to `phase-6-complete` only after the gate passes.

## Phase 6 completion gate

- [ ] Every candidate decision cites accepted evidence.
- [ ] Every disqualification rests on positive evidence.
- [ ] Missing or process-sparse evidence was not converted to a low score.
- [ ] Every score, scarcity, tier, tie, confidence, and occasion decision was made by the primary orchestrator.
- [ ] Product-only evidence was not treated as process evidence.
