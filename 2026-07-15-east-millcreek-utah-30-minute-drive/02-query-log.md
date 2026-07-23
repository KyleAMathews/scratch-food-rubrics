# Phase 2 query log

Retrieval date: 2026-07-15 (America/Denver). Search-result inclusion creates candidates only.

## Track A — broad popularity-neutral map survey

- Time: approximately 16:27 MDT.
- Source: `https://overpass-api.de/api/interpreter` (Overpass API 0.7.62.11).
- Exact query: `[out:json][timeout:240];nwr["amenity"~"^(restaurant|cafe|fast_food|pub|bar)$"](40.396699,-112.282774,41.062062,-111.401008);out center tags;`
- Returned: 3,128 elements in the isochrone bbox. Point-in-polygon filtering against the saved Phase 1 isochrone retained 2,886 elements (2,863 named, 23 unnamed).
- Candidates added: 2,886 source-union rows.
- Raw data: `02-source-data/overpass-food-venues-bbox.json` and `02-source-data/overpass-food-venues-isochrone.json`.

## Tracks B/C — exact web queries

The search tool returns capped, mixed web-result pages rather than a declared total-result count. “Result count” below is therefore the number of result records returned on the inspected page, not the search engine's estimated universe. Across all targeted pages, 70 distinct lead rows were preserved; duplicates with Track A remain for Phase 3.

### Universal quality, scratch, ambition, and recency families (English, 16:30 MDT)

Source: web search. Returned page: 44 mixed result records across four queries; candidates added to the union included Alpenglow Table, Table X, Monte, HSL, Hub & Spoke Diner, From Scratch, Urban Hill, Veneto, Franck's, and Cucina Wine Bar.

1. `best restaurants Salt Lake City Utah 2026 Gastronomic SLC new openings`
2. `scratch kitchen house made restaurant Salt Lake City Utah`
3. `chef driven seasonal tasting menu restaurants Salt Lake City Utah`
4. `new restaurants Salt Lake City Utah 2025 2026 openings`

### Category markers (English, 16:32 MDT)

Source: web search. Returned page: 26 mixed result records across four queries; leads included Basta Pasteria, Guisados Home Style Mexican Cooking, El Asadero, El Puerto, Copal, PastaNito, and La Lola Taco.

1. `soufflé OR "pâté en croûte" OR "house charcuterie" Salt Lake City restaurant`
2. `"house-made pasta" OR "fresh pasta" restaurant Salt Lake City Utah`
3. `nixtamal OR "handmade tortillas" OR "mole" restaurant Salt Lake City Utah`
4. `"house-made dashi" OR "hand-cut soba" OR tempura omakase Salt Lake City Utah`

### Spanish-language and cuisine/format challenge (16:34 MDT)

Source: web search. Returned page: 45 mixed result records across four queries; leads included El Asadero, La Lola Taco, Taquería La Auténtica, Cafe Anh Hong, Drunken Kitchen, Little World, One More Noodle House, Noodle and Dumpling, and Zhu Ting Ji.

1. `mejores restaurantes comida mexicana auténtica tortillas hechas a mano Salt Lake City Utah`
2. `mejor restaurante mole nixtamal Salt Lake City Utah`
3. `best Ethiopian Afghan Nepalese Vietnamese restaurant Salt Lake City Utah local food guide`
4. `best Chinese handmade noodles dumplings restaurant Salt Lake City Utah`

Spanish was used because it is locally important to the market and surfaced Spanish-language Mexican-food results. Chinese-script queries were not used because local venue discovery and publication results overwhelmingly use English names or bilingual menu strings; cuisine-indexed English searches surfaced Chinese specialists. No other local script has broad civic use in this English-majority market.

### Awards, guides, local publications, and omakase (16:36 MDT)

Source: web search. Returned page: 21 result records across four queries. Visible-head additions/challenges included Junah, Arlo, Oquirrh, Felt Bar & Eatery, The Pearl, Urban Hill, Brownstone 22, Koyoté, Takashi, Itto Sushi, Mint, Sushi by Bou, Monte, Table X, Rouser, and Caffe Molise.

1. `site:jamesbeard.org Salt Lake City Utah restaurants 2026 semifinalists finalists`
2. `site:gastronomicslc.com best restaurants Salt Lake City chef 2026`
3. `site:slmag.com dining awards Salt Lake City restaurants 2025 2026`
4. `site:axios.com/local/salt-lake-city omakase restaurant 2026`

Inspected visible-head/recent-opening sources:

- James Beard Foundation, `https://www.jamesbeard.org/stories/james-beard-award-semifinalists-2026`
- Visit Salt Lake, `https://www.visitsaltlake.com/blog/stories/post/roundup-of-new-and-notable-restaurants/`
- Gastronomic SLC recent openings, `https://gastronomicslc.com/2026/03/18/all-the-latest-restaurants-to-open-in-utah-and-a-peek-at-whats-next/`
- Gastronomic SLC fine dining, `https://gastronomicslc.com/best-fine-dining-salt-lake-city/`
- Axios omakase, `https://www.axios.com/local/salt-lake-city/2026/05/11/salt-lake-city-omakase-sushi-takashi-itto-bou-uchi`
- Axios 2026 James Beard coverage, `https://www.axios.com/local/salt-lake-city/2026/01/21/2026-james-beard-semifinalists-utah-salt-lake-chefs-restuarants`

### Metro sub-area adaptive queries (English, approximately 16:40 MDT)

For each query below, `{AREAS}` was substituted literally with `("Salt Lake City" OR Millcreek OR Holladay OR Murray OR "South Salt Lake" OR "West Valley City" OR Taylorsville OR Midvale OR Sandy OR "Cottonwood Heights" OR "West Jordan" OR "South Jordan" OR Bountiful OR Draper) Utah`. This covers the principal restaurant-bearing sub-areas inside the irregular drive-time polygon in a single search family without replacing the polygon boundary. The two four-query batches returned 29 and 28 mixed records respectively.

1. `best top award guide restaurant {AREAS}`
2. `scratch "house-made" "from scratch" restaurant {AREAS}`
3. `chef-led artisan seasonal creative restaurant {AREAS}`
4. `new restaurant opening renamed relocated pop-up {AREAS} 2025 2026`
5. `tasting menu farm-to-table local sourcing restaurant {AREAS}`
6. `traditional regional Ethiopian Afghan Nepali Vietnamese Peruvian Georgian restaurant {AREAS}`
7. `soufflé hollandaise "house charcuterie" "pâté en croûte" restaurant {AREAS}`
8. `"fresh pasta" "house-pulled mozzarella" "multi-hour ragu" restaurant {AREAS}`

This pass added/challenged informal and long-tail leads including Namash Swahili Cuisine, Makam's Indian Restaurant, MakanMakan, Sauce Boss Southern Kitchen, 17 Oromian, Wild Peru, Mahider, El Paisa, Rubi's Peruvian Taste, Puro Peru, Thyme and Seasons, Noor Somali Restaurant, El Rocoto, Alhambra Shawarma, Rainbow Kitchen, Ve La Thai, Cafe del Barrio, El Morelense, El Dorado Seafood, Mountain City Chinese, Teru Sushi, and Mom's Kitchen.

## Counts and handling

- Track A rows: 2,886.
- Track B/C targeted and visible-head lead rows retained: 70.
- Phase 2 source-union rows before deduplication: 2,956.
- No qualification, scratch inference, disqualification, score, tier, or ranking was applied.

## Phase 3 convergence queries

Fresh gap pass, 2026-07-15:

1. `Salt Lake County food truck pop-up supper club private dining restaurant 2026`
2. `Salt Lake City lunch-only counter-service hidden gem restaurant 2026`
3. `Salt Lake City Somali Oromo Georgian Filipino Burmese regional restaurant 2026`
4. `new restaurant Bountiful West Valley Sandy Draper Utah July 2026`

This pass added or identity-merged 16 leads spanning mobile/private formats, counter/lunch specialists, Somali and other regional cuisines, and current openings.

Convergence pass:

1. `"new restaurant" "Salt Lake City" opened July 2026 food`
2. `"new restaurant" Millcreek Holladay Murray Utah 2026`
3. `"new restaurant" West Valley City Taylorsville Midvale Sandy Utah 2026`
4. `"new restaurant" Bountiful West Jordan South Jordan Draper Utah 2026`

The second identical execution of this complete four-query set returned the same result page and yielded zero new in-scope identities after the first execution's additions were merged.
## Phase 7 coverage audit — pass 1 — 2026-07-17

Fresh web challenge; retrieval date 2026-07-17. Search rank created candidates only and was not used as qualification evidence.

### Visible-head / guide / award / prominent

1. `best restaurants Salt Lake City Utah 2026 Eater`
2. `site:gastronomicslc.com new restaurants Salt Lake City 2026 openings`
3. `Salt Lake Magazine dining awards restaurants 2026 Utah`
4. `best restaurants Park City Utah 2026 chef`

Sources inspected included Eater's current SLC map, Salt Lake Magazine's 2026 Dining Awards, Time Out's March 2026 list, Visit Park City/Park City Magazine, Axios tasting-menu and James Beard coverage. All visible-head identities matched the canonical ledger.

### Scratch / ambition / chef-led / artisan

1. `scratch made restaurant Salt Lake City Utah chef owned seasonal`
2. `farm to table restaurants Salt Lake City Millcreek Sugar House chef led`
3. `tasting menu omakase Salt Lake City Utah 2026`
4. `artisan restaurant house made pasta bread charcuterie Salt Lake City Utah`

These challenged Valter's, Strada, Bartolo's, 'mina, Table X, Franck's, Monte, Mar Muntanya, Veneto, Rouser, Antica Sicilia, BTG, Junah and other existing identities; they also surfaced Tuscan Bistro as COV-001.

### Geographic / recent opening

1. `new restaurant Millcreek Sugar House Holladay Utah 2026 opening`
2. `new restaurant Sandy Draper South Jordan Utah 2026 opening`
3. `new restaurant West Valley City Taylorsville Murray Utah 2026`
4. `new restaurant Lehi Riverton Utah 2026 chef local`

Sources included city ribbon-cutting pages, Axios opening coverage, Utah Business Holladay Hills coverage and current local press. Added COV-004 and COV-005; announced-but-not-open concepts were not added.

### Local-language / regional cuisine

1. `restaurante mexicano comida casera Salt Lake City Utah hecho a mano`
2. `nhà hàng Việt Nam Salt Lake City phở bún bò mới`
3. `盐湖城 中餐 手工面 餐厅 Salt Lake City`
4. `مطعم صومالي إثيوبي حلال سولت ليك سيتي Utah`

Spanish surfaced COV-002 and COV-003 plus numerous canonical matches. Vietnamese, Chinese-script and Arabic queries returned canonical matches or irrelevant/nonlocal pages and no other in-scope additions.

### Marker / specialist

1. `soufflé restaurant Salt Lake City Utah`
2. `house pulled mozzarella burrata Salt Lake City restaurant`
3. `nixtamal fresh pressed tortillas Salt Lake City restaurant`
4. `house charcuterie terrine pate Salt Lake City restaurant`

Results matched Log Haven, Spencer's, Red Rock, Caputo's, House of Corn, El Asadero, Strada, Osteria Amore and other canonical rows; no new identity.

### Informal / mobile / pop-up / relocation

1. `Salt Lake City restaurant pop up supper club chef 2026 Utah`
2. `Salt Lake City food truck market stall handmade restaurant 2026`
3. `Salt Lake City cottage food preorder chef dinner 2026`
4. `Salt Lake City restaurant relocation rename opening 2026 food`

Sources included Visit Salt Lake food trucks, ComCom Kitchen's current tenant list, SLC Food Trucks, market/festival sources, Utah Stories and Axios. Added COV-006; existing Alpenglow Table, Gossip Kitchen, ComCom tenants and renamed/relocated canonical identities were matched.

Pass-1 yield: **6 new in-scope identities**, all entered as coverage additions and routed to Phases 4–6.

## Phase 7 coverage audit — pass 2 — 2026-07-17

Full repeat challenge after all six pass-1 additions completed Phases 4–6. Retrieval date 2026-07-17. The same six required families and all 24 exact queries from pass 1 were rerun without narrowing.

### Results by family

- Visible-head / guide / award / prominent: canonical matches only; zero new identities.
- Scratch / ambition / chef-led / artisan: canonical matches only; zero new identities.
- Geographic / recent opening: First Watch Taylorsville matched the existing R-2922 reversible U.S.-standardized-chain novelty triage; Magnolia Holladay and Monkeywrench Sugar House matched pass-1 additions; Crispy Cones was a familiar standardized U.S. chain branch and did not reopen the user-preference-screened population; other results were canonical, announced-but-not-open, outside the drive-time scope, or nonrestaurant. Zero new in-scope identities.
- Local-language / regional cuisine: Casa del Pollo and TACOnTENTO matched pass-1 additions; Delicias Sofia, Sol & Sabor, El Asadero, House of Corn and other results matched canonical rows. Vietnamese, Chinese-script and Arabic searches produced canonical, irrelevant or nonlocal results. Zero new identities.
- Marker / specialist: Caputo's, Osteria Amore, Strada, House of Corn, El Asadero and other results matched canonical rows; retail-only tortilleria/charcuterie results did not create restaurant identities. Zero new identities.
- Informal / mobile / pop-up / relocation: Alpenglow Table, Gossip Kitchen, Square Kitchen/ComCom tenants, Latin Truck, Forty Three Bakery and relocation/opening results matched canonical rows or the pass-1 additions. Events, vendor directories without a distinct current prepared-food operator identity, future openings and outside-area results did not create candidates. Zero new identities.

Identity comparison used canonical name, address, domain, phone, alias, branch, predecessor/successor and user-approved novelty-screen state. Search rank and snippets were used only to challenge coverage, not to qualify or score restaurants.

Pass-2 yield: **0 new in-scope identities**. Coverage converged after the complete repeat challenge.
