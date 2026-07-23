# Cheap-heuristics study: second random sample of 20

Date: 2026-07-15

This is a fresh reproducible sample from the same 1,680-candidate population, excluding the first 20. Selection used the lowest SHA-256 hashes under salt `cheap-heuristics-sample-2026-07-15-v2`. Root performed the research directly.

## Results

| ID | Venue | Cheap finding | Disposition/lesson |
|---|---|---|---|
| R-1006 | Fuji Sushi | Exact-address independent sushi restaurant; current direct ordering page. | Retain unresolved. Generic ordering-site prose says little about production. |
| R-1131 | Cliff Dining Pub | Locally founded; official menu repeatedly documents house-made sauces, breading, flatbread, biscuits, pickles, and dressings. | Advance. Broad American menu is compatible with substantial in-house work. |
| R-0347 | Ahh Sushi | Exact venue belongs to the local O'Shucks/Ahh Sushi concept rather than an obvious broad US chain. | Retain unresolved; concept-level packet may be reusable locally. |
| R-1471 | Del Barrio Cafe | Same Midvale concept as first-sample R-2910 “Cafe del Barrio”; exact official address and domain match. | **Duplicate/alias merge.** Word-order normalization missed it. |
| R-1990 | Bix | Local bakery/cafe, opened as an offshoot of South Jordan's Biscotts, with baked goods and hot plates. | Retain/advance; related local concepts are not low-novelty chains. |
| R-1557 | Space Tea | Local boba/dessert shop; direct menu says taiyaki batter and soft serve are made in house. | Retain. Category and configurable drink menu would have produced a false exclusion. |
| R-0018 | Harvest Restaurant | Public Thanksgiving Point restaurant using local ingredients and several house-made components. | Retain; institutional ownership is not institutional-only access. |
| R-0380 | The Farm | Seasonal Park City Mountain restaurant; official resort page says no lift or skier access required. | Retain; seasonal operation and resort ownership are not ordinary-access failures. |
| R-0365 | Francisco's Mexican Grill | Exact address resolves to a small Farmington restaurant; current delivery/order presence. | Retain unresolved. Thin official evidence is not a reason to remove. |
| R-2384 | Sharon's Cafe | Long-running family diner with a current exact-address menu/listing. | Retain unresolved. Familiar diner format remains an unsafe proxy. |
| R-2461 | Cotton Bottom Inn | Current local Bar X Group restaurant; compact menu centered on fresh ground-chuck garlic burgers. | Retain. Restaurant-group ownership and a narrow familiar menu do not imply industrial standardization. |
| R-0503 | Tornado Crepe | Current delivery listing, but weak exact identity evidence. | Identity repair; no exclusion without positive closure/replacement evidence. |
| R-0247 | White Tomato | New Draper Italian venue; current business identity but weak searchable menu evidence. | Retain unresolved. New/low-evidence venues need research, not filtering. |
| R-1236 | Scion Cider | Official site explicitly says “21+ only bar” and “outside food welcome.” | **Remove from restaurant evidence set: positive no-food evidence.** It may belong in a beverage rubric. |
| R-1337 | Chunga's | Local two-location Mexican restaurant centered on tacos al pastor. | Retain; small branch count and specialization are not chain-standardization failures. |
| R-0182 | Kaneo | Current Park City Mediterranean/North Macedonian restaurant at a different resolved street address than sparse OSM record. | Repair address, then retain/advance. |
| R-1316 | Fajita Grill ToGo | Current single-area Sandy identity; no broad corporate footprint surfaced. | Retain unresolved; “ToGo” is not a production signal. |
| R-1081 | Hero Hotpot | Current restaurant in Salt Lake Chinatown with a large Chinese hotpot menu. | Retain. Service model shifts some cooking to the diner but is not low-ambition evidence. |
| R-1360 | Han Bowls | Single food-court Chinese “gourmet express” venue with current official location page. | Retain unresolved. Food-court location and steam-table-style menu are insufficient alone. |
| R-2047 | Ooh Pho | Newly opened local Vietnamese restaurant; city profile reports pho broth stewed in house for 20 hours and Utah-specific dishes. | Advance; cheap strong production evidence. |

Representative direct sources: [Cliff Dining Pub](https://cliffdiningpub.com/), [Del Barrio Cafe](https://delbarriocafe.com/home), [Harvest](https://thanksgivingpoint.org/dine/harvest-restaurant/), [The Farm](https://www.parkcitymountain.com/explore-the-resort/during-your-stay/dining/the-farm-restaurant.aspx), [Cotton Bottom](https://thecottonbottom.com/), [Scion Cider](https://www.scionciderbar.com/), [Chunga's](https://chungasslc.com/), [Hero Hotpot](https://www.saltlakechinatown.com/hero-hotpot), [Han Bowls](https://hanbowls.com/location/), and [Taylorsville's Ooh Pho profile](https://www.taylorsvilleut.gov/Home/Components/News/News/872/265).

## What this sample changes

The first study over-weighted corporate footprint. The user correctly noted that its examples were not common enough to remove much work and that Great Harvest has unusually substantial scratch production for a chain. Corporate footprint should therefore be only a *familiarity candidate generator*. It cannot establish either low scratch production or exclusion by itself.

No venue in this second sample was a persuasive low-novelty national-chain exclusion. The useful reductions were instead:

1. **One definite alias duplicate (5% of this sample).** Domain, phone, address, and token-set name comparison would have merged `Cafe del Barrio` and `Del Barrio Cafe`. Exact normalized-name branch collapse is too weak. This check may scale because the source union contains many spelling and word-order variants.
2. **One definite non-food venue (5%).** The venue's own site explicitly invited outside food. A cheap official-menu/substance check can remove bars, taprooms, coffee roasters, and similar records only when positive evidence shows they do not prepare food.
3. **Two identity/address repairs.** These prevent evidence from being researched under stale or ambiguous identities, but do not necessarily reduce the final population.
4. **Several immediate advances.** Cliff Dining Pub, Space Tea, and Ooh Pho surfaced concrete in-house production cheaply. These again show why format-based filters are counterproductive.

## Revised cheap heuristics worth applying

### A. Stronger entity clustering

Before any more evidence packets, cluster on combinations of:

- identical domain or phone;
- exact or near-exact address/coordinates;
- token-set names so word order does not matter;
- aliases and old names; and
- shared official location pages.

Only merge when identity evidence is strong. Preserve separate branches, then apply the already approved nearest-branch rule. This is likely the best remaining bulk reduction because it repairs the union itself rather than predicting food quality.

### B. Positive food-substance check

For records tagged bar, pub, brewery, taproom, winery, coffee roaster, or similarly ambiguous, look for an official food menu. Remove only on positive evidence such as “outside food welcome,” “no kitchen,” drinks-only menu, or explicit reliance on food trucks/pop-ups. Scion is the clean sample example.

Do not infer no-food status from the category. Kaneo, Cliff, Cotton Bottom, and Space Tea demonstrate the false-positive risk.

### C. Corporate familiarity is separate from scratch

Corporate footprint may identify concepts to compare against the user's familiarity preference, but the decision must incorporate actual prevalence and production. Great Harvest should not have been presented as an obvious exclusion: it is franchised, but its bread production is materially scratch-oriented. Rare regional franchises also save little work.

## Bottom line

After 40 sampled restaurants, there is still no newly discovered menu-shape, cuisine, format, or ownership heuristic that safely removes a large fraction. The defensible cheap work is data hygiene: stronger deduplication, positive no-food/non-operating checks, and identity repair. Anything more aggressive begins selecting against exactly the small, informal, specialist, or poorly indexed restaurants the rubric is meant to find.
