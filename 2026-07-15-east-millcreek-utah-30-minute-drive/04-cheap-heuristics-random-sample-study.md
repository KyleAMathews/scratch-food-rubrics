# Cheap-heuristics study: reproducible random sample of 20

Date: 2026-07-15

Population: 1,680 candidates remaining after the user-approved rules 1–3.

Sampling: the 20 candidates with the lexicographically lowest SHA-256 hash of `cheap-heuristics-sample-2026-07-15-v1` plus the canonical candidate record. The exact sample and hash keys are preserved in `02-source-data/cheap-heuristics-random-sample-20.json`.

Purpose: find inexpensive *workflow* and exclusion heuristics that reduce full evidence packets without treating fast service, familiar dish names, broad menus, low web visibility, or chain membership itself as evidence against ambitious scratch cooking.

## Results

| ID | Venue | Cheap research result | Implication |
|---|---|---|---|
| R-2910 | Cafe del Barrio | Official site describes an immigrant-founded local concept with Midvale and Draper locations and fresh ingredients. | Retain. Multiple locations alone is not a low-novelty corporate signal. |
| R-0275 | Sakura Express | Direct ordering menu shows a large, configurable Japanese/teriyaki/sushi/boba menu and mentions house-made teriyaki. | Retain unresolved. Menu breadth or configuration alone is too ambiguous. |
| R-1115 | My Sugar's Donut Shoppe | Exact local identity surfaced weakly and no useful official site appeared quickly. | Route to identity repair; missing web presence is not exclusion evidence. |
| R-1320 | Fortune Cuisine | Broad familiar Chinese menu, but direct menu language includes homemade sauce. | Retain unresolved. A commodity-looking menu creates false positives. |
| R-0051 | Cafe Anh Hong | Official site describes family ownership, handmade dim sum, and fresh noodles made daily. | Immediate retain/advance; demonstrates why cuisine and menu breadth cannot filter. |
| R-0019 | Mountain Grill | Name plus coordinates produced several plausible but mismatched businesses. | Route to identity repair before spending on a full packet. |
| R-1643 | Ten Seconds Yunnan Rice Noodle | Official/franchise footprint exists, but the concept is a culturally specific foreign-origin noodle chain. | Do not exclude from chain status alone; apply the US-familiarity exception conservatively. |
| R-1850 | Koino Poke | Official menu is predominantly a configurable base/protein/topping/sauce grid. | Assembly format is only a supporting signal when corporate standardization is independently proven. |
| R-2888 | Old Tbilisi Kitchen | Direct ordering menu documents fresh dough and hand-crafted Georgian dumplings and breads. | Immediate retain/advance on positive production evidence. |
| R-1516 | Umbrella Cafe | Cafe is associated with Under the Umbrella bookstore/community space and advertises specialty coffee. | Retail co-location is not enough to remove; verify whether it has substantive food if relevant. |
| R-0127 | Great Steak | Official pages expose a numbered store, large US/international footprint, proprietary standardized product, and franchising. | Exclude under the existing US-standardized-chain preference; static name matching missed it. |
| R-2420 | Jim's | Local family-restaurant/diner identity with a broad menu; no strong corporate footprint found cheaply. | Retain unresolved. Generic diner names and menus are unsafe filters. |
| R-1898 | Carmine's | Exact local identity was thin and search results did not confidently resolve the candidate. | Route to identity repair/current-operation check. |
| R-0607 | Shabu Shabu House | Exact search returned several similarly named but mismatched restaurants. | Route to identity repair; avoid attaching another venue's evidence. |
| R-0563 | Burger Express | Official site advertises multiple locations and franchise opportunities with standardized brand infrastructure. | Exclude under the existing US-standardized-chain preference. |
| R-1402 | Fortune Cookie | Official site describes a family-owned Chinese/sushi restaurant despite a very broad menu. | Retain unresolved. Breadth is not proof of low ambition or standardization. |
| R-0073 | Courchevel Bistro | Official site identifies a named executive chef, an inventive French menu, and public service at 201 Heber Avenue. | Retain/advance; ownership by a club does not mean access is private. |
| R-2134 | Great Harvest Bread Company | Official corporate sites expose a rewards app, location system, franchise agreement/training, and national franchise development. | Exclude under the existing US-standardized-chain preference; another naming/ontology miss. |
| R-2544 | Olympian Greek & American | Official site says family-owned, operating since 1980, with homemade meals at the exact address. | Retain/advance; a familiar diner format can still have strong local production evidence. |
| R-1973 | Boiler Room | Current official site places it at 32 Exchange Place, while the candidate says 16; it appears to be an upstairs bar associated with Heat. | Repair identity/address and verify substantive public food before a full restaurant packet. |

Key direct sources: [Cafe Anh Hong](https://cafeanhhong.com/), [Old Tbilisi Kitchen ordering](https://www.toasttab.com/local/order/old-tbilisi-kitchen), [Ten Seconds](https://www.tensecondsricenoodle.com/), [Courchevel Bistro](https://www.courchevelbistro.com/), [Olympian](https://www.olympianeats.com/), [Great Harvest franchising](https://franchising.greatharvest.com/), and [Boiler Room](https://theboilerslc.com/). Search evidence and direct menus were checked as a heuristic study, not treated as complete Phase 4 evidence packets.

## Recommended cheap checks

### 1. Corporate-footprint enrichment for the existing US-standardized-chain rule

Before full evidence research, run one exact-name search aimed at the official domain and test for a combination of positive signals:

- franchise opportunities, franchise disclosure/application, or franchise training;
- a corporate location finder, numbered stores, rewards app, or national ordering platform;
- an explicitly broad US footprint; and
- evidence that the menu or operating model is standardized across locations.

Require at least one footprint fact and one standardization fact. This is not a new anti-chain rule; it repairs misses in the existing user-approved preference. It caught Great Steak, Burger Express, and Great Harvest in this sample. It must retain the already stated foreign-chain and store-local-variation exceptions.

### 2. Identity-resolution queue before evidence packets

Use name + coordinates/address + phone/domain to seek an exact current match. If one or two cheap searches cannot confidently attach the candidate to a current venue, move it to a small identity-repair queue instead of researching a full packet under a possibly wrong identity. Mountain Grill, Carmine's, Shabu Shabu House, and My Sugar's triggered this in the sample.

This is a staging rule, not an exclusion. Removal still requires positive evidence of closure, replacement, duplication, or non-public operation.

### 3. Stale-address and current-operation check

Compare the candidate address/coordinates with the current official page or ordering page before deeper research. Mismatches trigger identity repair; confirmed closure/replacement can use the already approved non-operating reason code. Boiler Room demonstrates the value of this check.

### 4. Positive-production short circuit

When the first official page directly documents meaningful in-house production—handmade noodles or dumplings, fresh dough, house baking, a named chef with a changing menu—stop cheap elimination work and advance the venue to normal evidence research. This does not qualify the restaurant by itself; it prevents wasting time trying to eliminate promising candidates. Cafe Anh Hong and Old Tbilisi are the clearest sample cases.

### 5. Compound evidence only for assembly concepts

A base/protein/topping/sauce grid may support a corporate-standardization finding, but it must never trigger exclusion alone. Koino Poke shows the cheap signal; Sakura Express and the broad Chinese menus show why menu structure by itself is unreliable.

## Heuristics the sample argues against

- generic or familiar restaurant names;
- broad menus or familiar American-Chinese/diner dishes;
- `fast_food`, cafe, bar, bakery, counter-service, or retail-co-location categories;
- multiple locations without corporate standardization evidence;
- no official website or weak search results;
- configurable menus by themselves;
- club ownership by itself; and
- “novel cuisine” as the primary positive criterion.

## Estimated utility from this sample

- **3/20** were additional standardized-chain misses suitable for the existing preference filter.
- **4/20** clearly needed identity repair before a full packet; **1/20** additionally showed a current-address mismatch.
- **4/20** had cheap positive local/production evidence strong enough to stop elimination work early.
- The remaining cases mostly demonstrated false-positive risks rather than safe eliminations.

This is a small exploratory sample, so those proportions should not be extrapolated as population estimates. The useful result is the decision structure: corporate evidence can exclude; identity checks can defer or positively clean up; production evidence can advance; menu/category proxies cannot safely decide.
