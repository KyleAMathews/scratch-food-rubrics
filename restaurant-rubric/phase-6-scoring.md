# Phase 6 — Restaurant Scoring and Classification

**Read this file in full immediately before Phase 6. The primary orchestrator makes every decision; workers never score.**

**Three orthogonal axes** (the star rating collapses all three into one lossy scalar):
1. **S_scratch** — production intensity (the rubric below), 0–100.
2. **I** — interestingness / novelty (turnover δ + market-scarcity A_scarcity), 0–100.
3. **R** — star rating ≈ E[satisfaction | visit 1]; used as a **quality filter (θ ≈ 4.0★)**, not an objective.

**Price** is carried as neutral metadata ($, Google's 1–4 quantile bucket) — displayed, never scored.

Decision rule: filter {R ≥ 4.0 ∧ S ≥ 60}, rank by **G = √(S × I)** (novelty tilt: G′ = S^0.4·I^0.6).

S_scratch latent variable: **on-site production intensity × proprietary-vs-commodity inputs**. Orthogonal to ownership (chain-ness is magnitude, not direction), so operator status is weighted low.

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

## Operational decision invariants (moved from v8.2–v8.7)

- **Positive evidence only for disqualification.** Every DQ requires an affirmative source citation and exactly one controlled subtype: `explicit_closed`, `explicit_no_food`, `external_food_only`, `offsite_all_production`, `uncooked_retail_only`, or `confirmed_snack_only`. `exhausted-unavailable` must not support a DQ. Missing process language, weak web presence, category, format, generic menu appearance, chain or franchise status, and absent food-program evidence are not DQ evidence.
- **Service format is orthogonal to production.** Counter service, takeaway, delivery, breakfast/lunch-only operation, market stalls, and informal rooms remain eligible; only accepted production evidence determines the scratch decision.
- **Evidence domains and scopes do not transfer silently.** Daily production is not menu turnover. Opening hours, dayparts, seasonal drinks, promotions, events, sourcing/delivery schedules, and food-hall tenant changes do not establish `food-menu-turnover` without separate literal evidence. Non-food production cannot inflate a food scratch score. Company-wide, commissary/shared-kitchen, external-supplier, and predecessor/historical evidence cannot silently become current `branch-local` production.
- **Per-number provenance remains mandatory.** Treat every S, I, E, R, and price value as documented, estimated, or unverified. Reader-facing rated tiers require documented R and an S decision grounded in accepted evidence.
- **Rating exhaustion is terminal, not negative.** A scratch-verified restaurant whose rating is `exhausted-unavailable` after the required search trail goes to the explicit **scratch-verified, rating-unconfirmed** tier. It is surfaced with that caveat, neither silently dropped nor promoted into a rating-gated tier. Estimated or unverified ratings remain non-terminal.
- **Conflicts remain visible.** Preserve each literal rating, count, source, and date; prefer a direct source when resolving under the rating hierarchy, flag material discrepancies, and never synthesize a rating.

## Controlled decision dispositions

Use `evidence-exhausted-no-score` when required research completed without a defensible scoring packet. Use `score-unresolved` when accepted positive evidence exists but one or more required scoring dimensions remain too uncertain. Both are non-negative states: neither implies low quality, ineligibility, or DQ, and neither may be converted into a low numeric score.

Each no-score decision records the candidate ID, accepted-evidence citation, disposition, primary missing field or reason, and any positive scratch markers worth retaining. Mechanically generated rows are valid only when every row preserves its individual citation and reason.

## Deterministic integrity validation

Before Phase 6 closes, run deterministic integrity validation over the complete decision ledger and save its machine-readable result inside `{RUN_DIR}`. Validate:

- population equality between frozen candidates plus accepted Phase 7 additions and decisions;
- exactly one decision per canonical candidate and no duplicate decision IDs;
- every canonical merge target exists and is resolved;
- every criterion respects its criterion maxima, criterion sums and total S are internally consistent, and the recomputed geometric mean G matches the existing formula and rounding rule;
- every ranked row satisfies the current scratch and rating gates;
- every DQ has a permitted positive-evidence subtype and citation;
- unresolved and exhausted rows are absent from ranked tiers;
- summary disposition counts equal the decision population.

The phase gate fails on any validation defect. Link the machine-readable result from canonical `06-decisions.json` and `00-run-manifest.md`. A run-local deterministic validator is sufficient; a universal repository parser is not required.

## Phase 6 artifact

Write every orchestrator decision to canonical `{RUN_DIR}/06-decisions.json`: stable ID and identity, disposition and reason, structured rationale and source references, score/rating/access provenance, merge target, tier, ranking eligibility, occasions, and category-specific decisions. Validate it against `../interactive-results/decision-schema.json`, run all category integrity checks, compute its canonical SHA-256 content hash, and link the schema version, validator result, hash, and JSON path from `00-run-manifest.md`. Write atomically, then update the manifest to `phase-6-complete` only after schema validation and all gates pass.

`06-decisions.md` is an optional deterministic audit view generated from canonical JSON. Never author or repair it independently, and never use it as an authority. Do not write decisions into worker-return files.

## Phase 6 completion gate

- [ ] Every candidate decision cites accepted evidence.
- [ ] Every disqualification has an affirmative source citation and exactly one permitted DQ subtype; exhausted or absent evidence never supports DQ.
- [ ] Every `score-unresolved` and `evidence-exhausted-no-score` row has its accepted-evidence citation, primary missing field/reason, and retained positive scratch markers.
- [ ] Missing or process-sparse evidence was not converted to a low score.
- [ ] Every score, scarcity, tier, tie, confidence, and occasion decision was made by the primary orchestrator.
- [ ] Product-only evidence and service format were not treated as production verdicts.
- [ ] Deterministic integrity validation passed every invariant, and its machine-readable result is linked from the decision ledger and manifest.
