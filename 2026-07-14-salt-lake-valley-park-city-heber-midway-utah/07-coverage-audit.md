# Phase 7 — Coverage audit

Audit date: 2026-07-14 (America/Denver). Comparison keys: normalized name, address, domain, phone, alias, and successor relationship. This is an omission challenge, not an exhaustive-census claim.

## Pass C1 — fresh omission challenge

All queries used the web search index on 2026-07-14. Direct result sources were opened where identity or current status needed confirmation.

| family | exact query | representative source(s) | comparison outcome |
|---|---|---|---|
| visible head | `best bakeries Salt Lake City Utah local guide 2026` | https://www.axios.com/local/salt-lake-city/2026/06/01/magnolia-bakery-utah-locations-holladay-first | Magnolia matched A-144/P3-002; other visible hits present |
| visible head | `best bakery Park City Utah Heber Midway local guide` | https://www.parkcitymag.com/eat-and-drink/park-city-bakeries | named venues matched ledger |
| ambition | `artisan sourdough microbakery Salt Lake Valley baker owned` | producer/result set | no new identity |
| recent | `new bakery Salt Lake City Utah opening 2025 2026` | Axios Magnolia/current-opening results | Magnolia matched; no new retail identity |
| marker | `canelé bakery Salt Lake City Utah` | https://canelabakeryutah.com/; marker index | Canela matched A-028; no new venue |
| marker | `kouign amann bakery Salt Lake City Utah Park City` | Park City Magazine; https://cheznibs.com/pastries/ | all named venues matched |
| marker | `"Paris-Brest" bakery Utah Salt Lake` | Beaumont Toast menu | matched A-018 |
| marker | `"pain suisse" bakery Salt Lake City Utah` | Salt Lake Tribune All Purpose result | matched A-006 |
| successor | `Hruska's Kolaches West Jordan Utah current bakery` | https://www.restaurantji.com/ut/west-jordan/hruskas-kolaches-/ | The Kolache Place/Hruska matched A-218 |
| market | `Volker's Bakery Salt Lake City Utah current farmers market` | https://volkersbakery.wordpress.com/ | **COV-001 added** |
| informal | `bakery farmers market pop up cottage Salt Lake City Utah 2026` | https://www.slcfarmersmarket.org/packaged-prepared-food; https://www.sugarhoodfarmersmarket.com/ | no additional attributable vendor identity |
| east geography | `microbakery sourdough East Millcreek Holladay Cottonwood Heights Utah` | result set | no new identity |
| Spanish | `panadería artesanal Salt Lake City Utah pan dulce 2026` | Canela/local results | existing panaderías matched |
| Spanish/geography | `pastelería West Valley City Utah panadería Heber Midway` | local directory/producer results | existing identities matched |
| specialist | `tortillería nixtamal Salt Lake City Utah hecha a mano` | Axios Mi Casa/House of Corn | matched T-020/T-021 |
| specialist | `baklava phyllo handmade bakery Salt Lake City Utah` | Sheer Ambrosia; Sweets by Steph; https://www.bohemianbaklava.com/ | first two matched; **COV-002 added** |
| recent/Wasatch Back | `new bakery Park City Heber Midway Utah opened 2025 2026` | TownLift/Park City Magazine | later confirmed COV-005 |
| geography | `bakery Snyderville Kimball Junction Utah sourdough pastry` | https://www.visitparkcity.com/listing/the-bake-shop/29859/ | matched T-024 |
| geography | `bakery Draper Sandy Riverton Herriman Utah artisan 2026` | result set | no new identity |
| Spanish/geography | `bakery West Valley Kearns Magna Utah new artisan panaderia` | https://hicrunchy.com/; https://www.bucketsbakery.com/ | **COV-003/COV-004 added** |
| awards | `award winning baker pastry chef bakery Salt Lake City Utah 2026` | Axios James Beard/Fillings & Emulsions | matched A-098 |
| known-example | `chocolatier pastry laminated bakery Salt Lake City Utah local` | producer set | all attributable producers present |
| specialist | `"Bohemian Baklava" Salt Lake City bakery` | official site; MenuPix | COV-002 distinct from host Kahve A-125 |
| Spanish/lamination | `"Hi Crunchy" "La Panería" West Valley bakery` | https://hicrunchy.com/ | COV-003; exposed separate COV-006 host |
| host identity | `"La Paneria" "West Valley City" Utah` | Apple Maps/directories | COV-006 confirmed |
| host identity | `"La Panería" Utah bakery address` | https://maps.apple.com/place?place-id=I1538FD528409A093; Chamber listing | COV-006; relocation conflict preserved |
| recent/Wasatch Back | `"Olive Press Cafe" Midway bakery rating` | https://www.parkrecord.com/2025/11/07/the-olive-press-cafe-creates-a-new-social-eatery-cafe-in-midway/ | **COV-005 added** |
| current specialist | `"Bohemian Baklava" Kahve Cafe current 2026` | https://www.bohemianbaklava.com/ | COV-002 current/production confirmed |
| detail | `site:hicrunchy.com contact address "La Panería"` | https://hicrunchy.com/ | no stable address; host wording retained |
| detail | `site:bucketsbakery.com West Valley contact menu reviews` | https://www.bucketsbakery.com/ | COV-004 home format confirmed |
| detail | `site:volkersbakery.wordpress.com markets products contact` | Volker official site | COV-001 markets/Kamas base confirmed |
| adjacent | `site:ledepotpc.com Union Patisserie Park City bakery` | https://www.ledepotpc.com/about/ | Union matched A-229; Le Depot not separate bakery identity |
| adjacent | `"The Dainty Pear" Midway Utah bakery pastries` | Park Record + official pages | host boutique not added; distinct cafe is COV-005 |
| detail | `"La Paneria" "West Valley City" Utah` and `"La Panería" Utah bakery address` | Apple Maps + Chamber | COV-006 current/older address forms |
| recent cafe | `"Olive Press Cafe" Midway bakery rating` and `"The Dainty Pear" Midway Utah bakery pastries` | Park Record; first-party Toast | COV-005 distinct cafe/rotating bakery |

### Required-family coverage

| family | coverage result |
|---|---|
| visible/prominent | Park City Magazine, Axios, Visit Park City, current community discussions, producer pages |
| scratch/ambition/award | artisan sourdough, baker-owned, James Beard, handmade lamination, scratch, current openings |
| language/script | locally natural Spanish `panadería`, `pastelería`, `tortillería`, `hecha a mano`, accent-preserving La Panería; no locally used non-Latin business script identified |
| geography | East Millcreek/east side, central SLC, west valley, south valley, Park City/Snyderville/Kimball Junction, Heber/Midway |
| specialist/adjacent | baklava/phyllo, chocolatier, nixtamal/tortilla, croissanterie, GF/sugar-free, markets, cottage/preorder, cafe-hosted producer |
| marker | canelé, kouign-amann, Paris-Brest, pain suisse, naturally leavened sourdough; stroopwafel and phyllo specialists challenged through known examples |
| recent/successor | 2025–2026 openings, Magnolia branches, Hruska's→Kolache Place, La Paneria relocation, new markets and cafe-inside-boutique |

### Pass C1 yield and loop-back state

- New in-scope candidates: **6** — COV-001 through COV-006.
- Hruska's matched A-217/A-218; Magnolia matched A-144/P3-002; Midway Bakery's new address/phone is T-029; Union Patisserie is A-229; Dainty Pear is only the host for COV-005.
- All six are `coverage-addition`, awaiting Phases 4–6.
- A second full omission pass is required after loop-back; Phase 7 remains open.

## Pass C2 — repeated full omission challenge

Pass C2 was run only after COV-001–COV-006 completed Phases 4–6. It used new exact queries rather than treating C1 as sufficient.

| family | exact query | representative source(s) | comparison outcome |
|---|---|---|---|
| visible/scratch | `Salt Lake City bakery favorites 2026 sourdough pastry local` | Crumb Collective; Délice; Beaucoup; official producer results | Crumb matched T-009; others matched ledger; Sweet and Savory Pies surfaced for confirmation |
| Wasatch Back/recent | `Park City Heber Midway bakery 2026 pastries bread new` | Park City Magazine Midway guide; current producer results | all attributable venues matched |
| recent/press | `site:sltrib.com bakery Salt Lake 2025 2026 pastry opening` | Salt Lake Tribune Hruska's coverage | successor matched A-217/A-218 |
| Spanish | `panadería pastelería Salt Lake Utah 2026 artesanal` | Cakes By Edith; Canela Bakery | matched A-027/P3-044 and A-028 |
| cottage/geography | `microbakery cottage bakery West Jordan Sandy Draper Utah sourdough preorder` | producer/result set | no new attributable identity |
| marker | `canele kouign amann paris brest pain suisse bakery Salt Lake Utah` | Chez Nibs; Beaucoup; local discussions | named venues matched A-031/A-016 and existing ledger |
| specialist | `baklava chocolatier croissanterie tortilleria Salt Lake Utah artisan` | Bohemian Baklava; Sheer Ambrosia; Mi Casa; Chez Nibs | matched COV-002, T-017, T-020/T-021, A-031 |
| specialist detail | `"Sweet and Savory Pies" Salt Lake City Utah bakery reviews address` | https://www.sweetandsavorypies.org/; Restaurant Guru | **COV-007 added**; current official producer and 1377 E Emerson directory identity |
| markets | `2026 farmers market bakery vendor Salt Lake City Park City Utah bread pastry` | Park City Farmers Market; KPCW; SugarHood | Volker matched COV-001; other named bakery hits matched |
| east geography | `new bakery East Millcreek Holladay Cottonwood Heights Utah 2026` | Axios Magnolia/results | Magnolia matched A-144/P3-002; no other new identity |
| west geography/informal | `bakery Kearns Magna West Valley Utah cottage popup pastry 2026` | local results | no new attributable identity beyond COV-003/COV-004/COV-006 |
| Wasatch Back/geography | `bakery Snyderville Kimball Junction Heber Midway Utah artisan dessert 2026` | Visit Park City; Park City Magazine; producer set | all named venues matched |

### Pass C2 yield and loop-back state

- New in-scope candidates: **1** — COV-007 Sweet and Savory Pies.
- C2 did not converge. COV-007 was frozen immediately and routed through Phases 4–6; a fresh C3 audit will be required afterward.

## Pass C3 — third fresh omission challenge

C3 began after COV-007 completed Phases 4–6 and again used new exact queries.

| family | exact query | representative source(s) | comparison outcome |
|---|---|---|---|
| visible | `best independent bakeries Salt Lake Valley Utah 2026 bread pastry pie` | KSL/Deseret News; Salt Lake Tribune; producer set | All Purpose matched A-006; other identities matched |
| recent | `new pastry shop bakery opened 2026 Salt Lake County Utah` | KSL; Tribune; Utah Business; Axios | All Purpose, Magnolia, JD Flannel matched existing IDs |
| Spanish/geography | `panaderia reposteria pasteles West Valley Taylorsville Kearns Utah local` | Colombian Baker; Cakes By Edith; local discussions | Colombian Baker matched A-042; other identities matched |
| ambition | `natural leaven bakery chef owned Salt Lake City Utah handmade pastry` | Red Bicycle; Fillings & Emulsions; current producers | matched T-027/A-098 and ledger |
| marker | `handmade croissant danish laminated pastry Salt Lake Utah bakery not All Purpose` | KSL; Tribune; Lone Pine; Tulie | matched A-006/A-141/A-226 |
| east geography/informal | `home bakery pie bread pastry Millcreek Holladay Cottonwood Heights Salt Lake Utah preorder` | producer/result set | no new attributable identity |
| Wasatch Back/markets | `Park City Kamas Heber Midway microbakery farmers market bread pastries 2026 vendor` | KPCW; Park City market; Park City Magazine | Volker and other named venues matched |
| specialist | `Utah Salt Lake bakery phyllo baklava mochi Asian pastry specialist local` | Sheer Ambrosia; Sweets by Steph; Moon/Kyung results | Sheer/Kyung/Steph matched; Moon resolved as historical closure conflict, not a current addition |
| marker/rarity | `unusual pastry bakery Salt Lake City Utah canele stroopwafel mochi 2026` | local producer set | all attributable current identities matched |
| Wasatch Back/social | `Heber City Midway Park City bakery pie cake bread site:instagram.com 2026` | result set | no new attributable identity |
| markets/informal | `Salt Lake farmers market bakery vendor sourdough pie pastry Instagram Utah 2026` | SugarHood Farmers Market; Crumb Collective | Crumb matched T-009; **COV-008 surfaced** |
| identity detail | `"Hearth & Crust" "Salt Lake City" sourdough bakery` | SugarHood Farmers Market | only market attribution found |
| identity detail | `"Hearth & Crust" SugarHood Farmers Market Utah Instagram` | SugarHood Farmers Market | listed as SLC sourdough bakery with three products; no independent identity |
| current/status | `"Moon Bakery" Salt Lake Chinatown 2026 current open` | Chinatown host; Restaurant Guru; current/old directories | positive permanent-closure evidence and stale host conflict; not added as current |

### Pass C3 yield and loop-back state

- New plausible in-scope candidate: **1** — COV-008 Hearth & Crust.
- The single market listing is sufficient to preserve a plausible named producer lead, but not to score or verify it. It was routed through Phases 4–6; Phase 7 will require a fresh C4 pass afterward.

## Pass C4 — fourth fresh omission challenge

C4 began after COV-008 completed the loop-back. New queries again covered every required family.

| family | exact query | representative source(s) | comparison outcome |
|---|---|---|---|
| visible/directory | `Salt Lake County Utah bakery directory artisan bread pastry independent current 2026` | current producer and directory set | all attributable bakery identities matched |
| recent/press | `site:ksl.com bakery pastry Salt Lake Park City Heber Midway 2025 2026` | KSL All Purpose/Magnolia coverage | matched A-006/A-144/P3-002 |
| Spanish/geography | `pastelería panadería artesanal Murray Midvale West Jordan South Jordan Utah` | Sagato/Cakes by Edith/local set | named venues matched |
| cottage/market | `Salt Lake Utah cottage bakery popup sourdough croissant farmers market 2026` | Downtown market; SugarHood; producer set | Hearth & Crust matched COV-008; no additional named producer |
| market/marker | `bakery vendor Salt Lake City 2026 sourdough rye pretzel croissant market` | SugarHood; Forty Three; All Purpose | matched COV-008/A-102/A-006 |
| Park City geography | `Park City Snyderville bakery dessert chocolatier bread local current 2026` | Visit Park City; producer set | all named venues matched |
| Heber/Midway geography | `Heber City Midway Kamas bakery cakes pies sourdough local current 2026` | current guides/producers | all named venues matched |
| specialist/adjacent | `Salt Lake City specialty bakery empanada baklava tortilleria chocolatier pastry chef owned` | Empanada.Co; Empanadas801; Sheer Ambrosia; Fillings & Emulsions | **COV-009 surfaced**; others matched |
| identity detail | `Empanada.Co Salt Lake City Utah address reviews current` | https://empanada.co/; Restaurantji | COV-009 distinct/current |
| identity detail | `site:empanada.co Salt Lake City locations menu` | official site | COV-009 distinct/current |
| related specialist | `"Argentina's Best Empanadas" Salt Lake City current address` | https://www.argentinasbestslc.com/; Apple Maps | **COV-010 added** |
| related specialist | `"Pastelitos Pipo Utah" current bakery address reviews` | Restaurantji; city license result | **COV-011 added** |
| informal/no identity | current KSL Classifieds sourdough listing surfaced during the specialist pass | KSL Classifieds listing 80469448 | not added: no producer/business name or stable identity key |

### Pass C4 yield and loop-back state

- New in-scope candidates: **3** — COV-009 Empanada.Co, COV-010 Argentina's Best Empanadas, and COV-011 Pastelitos Pipo Utah.
- This clustered yield demonstrates an under-covered filled-pastry specialist family. All three were frozen together and routed through Phases 4–6; a new C5 audit will be required.

## Pass C5 — fifth fresh omission challenge

C5 began only after COV-009–COV-011 completed Phases 4–6.

| family | exact query | representative source(s) | comparison outcome |
|---|---|---|---|
| visible | `Salt Lake Valley bakery pastry bread pie independent "2026" local guide` | Cakes by Edith; Canela; Fillings & Emulsions; current producer set | named venues matched |
| Wasatch Back | `Park City Heber Midway Kamas bakery "2026" local pastry bread` | Park City Magazine; current producers | named venues matched |
| Spanish | `panadería pastelería pan dulce pastelitos empanadas Salt Lake Utah negocio local` | Panaderia Flores; Alicia's; Empanadas801; High Altitude | existing IDs matched; COV-012 surfaced for confirmation |
| filled-pastry specialist | `Salt Lake Utah bakery specialist burek kolache meat pie hand pie empanada current` | Sagato; existing empanada/kolache set | named venues matched |
| language/tradition | `Salt Lake Utah Filipino Korean Middle Eastern European bakery pastry local ensaymada baklava rye` | High Altitude; Moon; Sheer Ambrosia | **COV-012 added**; Moon is a closure conflict; Sheer matched T-017 |
| marker | `Salt Lake City bakery canele kouign amann pain suisse Paris Brest laminated 2026` | current marker-item producers | all matched |
| informal | `Salt Lake Valley microbakery bread drop pop up preorder Instagram 2026 local` | House of Bread; other producer set | all attributable identities matched |
| recent | `new bakery Salt Lake Park City Heber Midway opened June July 2026` | KSL; TownLift; current news | All Purpose/Magnolia matched; Jordanelle Ridge is a general cafe without attributable bakery production |
| identity detail | `High Altitude Bakeshop Salt Lake City reviews current 751 W 800 S` | official site; Restaurantji | COV-012 current/distinct |
| adjacent detail | `Friendly Flour Bakery Utah location contact` | Friendly Flour official site | Lehi/Utah County, outside catchment; not added |
| adjacent detail | `Jordanelle Ridge Barn Cafe Heber bakery pastries menu` | TownLift/result set | general cafe, no distinct bakery producer identified |
| recent Korean | Salt Lake Tribune Kyookie result surfaced in C5 | Tribune | planned/crowdfunding dessert-cafe concept, no operating venue; not added |
| current Argentine | Axios Argentina's Café result surfaced in C5 | Axios | matched P3-004 |

### Pass C5 yield and loop-back state

- New in-scope candidate: **1** — COV-012 High Altitude Bakeshop.
- COV-012 was frozen and routed through Phases 4–6. Phase 7 remains open for a new C6 audit.

## Pass C6 — convergence challenge

C6 began only after COV-012 completed Phases 4–6. It used twelve new exact queries spanning recency, geography, cultural traditions, informal producers, and marker items. Every attributable current producer matched the 325-ID ledger; this was the first zero-addition full pass.

| family | exact query | representative source(s) | comparison outcome |
|---|---|---|---|
| visible/recent | `best bakery Salt Lake City 2026 local pastry bread not chain` | current producer sites and local guides | All Purpose, Crumb, Forty Three, and Salt Lake Sourdough matched existing IDs; Bread Riot was historical rather than a current producer |
| Wasatch Back | `best bakery Park City Heber Valley Midway Utah 2026 locals` | Park City Magazine; current producer set | Midway Bakery, Hawk & Sparrow, The Bake Shop, Windy Ridge, and other named venues matched |
| culture/tradition | `Filipino Mexican Korean Arab bakery Salt Lake City Utah local current` | current producer/results set | High Altitude, Canela, Sheer Ambrosia, and other attributable identities matched; Kyookie remains planned/not operating |
| process/recent | `Salt Lake City artisan bakery owner interview handmade pastry sourdough current` | local profiles and producer sites | existing ledger identities matched |
| markets/informal | `bakery microbakery farmers market vendor Salt Lake County Utah July 2026 bread pastry` | current markets and producer sites | all named, attributable producers matched; unnamed vendor references were not stable identities |
| west geography | `bakery West Valley Kearns Magna Taylorsville Utah current cakes bread pastry` | Cakes by Edith, Canela, Buckets, and current directory set | all matched existing IDs |
| south geography | `bakery Sandy Draper South Jordan Riverton Herriman Utah local sourdough pastry 2026` | producer and directory set | all named in-scope venues matched; Alpine Bakery and Friendly Flour were outside the catchment |
| marker/specialist | `canele croissant baklava ensaymada empanada pie specialist Salt Lake Utah bakery` | Beaucoup, Chez Nibs, Bohemian Baklava, High Altitude, Empanada.Co, and pie producers | all matched existing IDs |
| current press | `site:axios.com/local/salt-lake-city bakery dessert pastry opening 2026 Utah` | Axios Magnolia coverage and food archive | Magnolia matched A-144/P3-002; no new bakery producer |
| Wasatch press | `site:parkcitymag.com bakery pastry Park City Heber Midway Kamas` | Park City Magazine bakery roundup | all attributable venues matched |
| cottage/preorder | `Salt Lake Utah microbakery cottage baker preorder sourdough pastry current Instagram` | Tomodachi, House of Bread, Crumb Collective, Salt Lake Sourdough | matched T-003, P3-001, T-009, and T-001; Sugar Street was outside the catchment |
| tradition/marker | `Salt Lake Utah traditional bakery challah phyllo mochi concha ensaymada empanada current` | High Altitude, Sheer Ambrosia, Tomodachi, panadería and empanada producer sets | all attributable current identities matched; Moon Bakery retained as a closure conflict rather than a current addition |

### Pass C6 yield and final audit

- New in-scope candidates: **0**.
- Full-pass yields were **C1 6, C2 1, C3 1, C4 3, C5 1, C6 0**. All twelve additions were frozen immediately; eleven completed Phase 5 as evidence-accepted and one as evidence-exhausted-unavailable. No coverage repair was needed.
- At the time of C6, the canonical population was **325 unique IDs**. After the category correction, direct-place rating re-review, and July 16 Argentina's Café exact-place correction, mutually exclusive dispositions were **56 rated survivors, 7 scratch-verified/rating-unconfirmed, 8 scored-but-filtered, 40 positive-evidence DQs, 8 deferred, 10 evidence-exhausted, and 196 not-scoreable**; these summed to 325.
- The final challenge covered visible heads, recent openings, Salt Lake Valley sub-geographies, the Park City–Heber–Midway corridor, Spanish-language and cultural-tradition queries, cottage/market producers, filled-pastry specialists, and marker items.
- Coverage is source-converged, not a claim of a complete real-world census. Home kitchens without a stable public identity, unnamed market vendors, private social accounts, stale directory records, and very new or poorly indexed producers can still be absent.

## Phase 7 outcome

**PASS at original Phase 7 close.** Every omission was looped through Phases 4–6 before the next full challenge, the final full pass yielded zero new candidates, and all 325 then-known IDs had terminal evidence and decision states.

## Post-run user correction — COV-013 Feldman's Deli

- On 2026-07-16 the user identified Feldman's Deli as an omitted bagel producer. It was absent from the candidate ledger, so this is a genuine coverage addition rather than a retagging correction.
- COV-013 completed the canonical Phase 4 return, primary-orchestrator Phase 5 inspection, an original-worker direct-Google repair, and primary-orchestrator Phase 6 scoring. It is a rated D-tier survivor at S 74, I 42, G 55.7, and direct Google R 4.7 with `count-unavailable`.
- Updated canonical population: **326 unique IDs**. Updated mutually exclusive dispositions: **57 rated survivors, 7 scratch-verified/rating-unconfirmed, 8 scored-but-filtered, 40 positive-evidence DQs, 8 deferred, 10 evidence-exhausted, and 196 not-scoreable**; these sum to 326.
- This user-triggered addition falsifies the stronger interpretation that C6 proved a complete census. The defensible claim remains source convergence with a documented adjacent-category miss: a deli with qualifying limited daily bagel production escaped bakery-focused discovery.
