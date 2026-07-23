# Phase 2 Query Log

Retrieval date/time window: 2026-07-14 22:35–22:43 America/Denver. Region pin on every query: Utah, United States; subarea/county names as shown. Search inclusion is candidate discovery only.

## Track A — broad popularity-neutral survey

Source: OpenStreetMap via Overpass API (`https://overpass-api.de/api/interpreter`, with `https://overpass.kumi.systems/api/interpreter` attempted as fallback). Language/script: OSM native tags; locally used English and Spanish name strings retained.

Selectors used in the full query family:

```text
nwr["shop"~"^(bakery|pastry|confectionery|chocolate)$"](AREA);
nwr["craft"~"bakery|confectionery",i](AREA);
nwr["cuisine"~"bakery|pastry|dessert|bagel|donut|chocolate",i](AREA);
nwr["name"~"bakery|bakes|bread|panader|pasteler|patisserie|boulanger|chocolat|bagel|tortilla|sourdough|pastry|croissant|cake",i](AREA);
out center tags;
```

| query_id | exact area expression | validated returned elements | raw source | candidates added to raw union |
|---|---|---:|---|---:|
| A-SLC | `area(3601744366)->.a; ... (area.a)` | 222 | `02-source-data/track-a-salt-lake-county-overpass.json` | 222 before cross-component deduplication |
| A-PC-CORE | bbox `40.58,-111.66,40.80,-111.40`; shop + cuisine selectors | 7 | `02-source-data/track-a-park-city-snyderville-core-overpass.json` | 7 before cross-component deduplication |
| A-PC-ADJ | bbox `40.58,-111.66,40.80,-111.40`; craft + name selectors | 9 | `02-source-data/track-a-park-city-snyderville-adjacent-overpass.json` | 9 before cross-component deduplication |
| A-HEBER | bbox `40.40,-111.56,40.61,-111.29`; full selector family | 7 | `02-source-data/track-a-heber-valley-overpass.json` | 7 before cross-component deduplication |

Validated deduplicated result: 241 unique OSM identities (`track-a-union.json`). Failed HTML/timeout responses from preliminary county/tile calls are preserved but not counted.

## Track B — adaptive targeted discovery

Source: web search. The API returned pooled results for each four-query batch and did not expose a stable per-query hit count. To avoid inventing counts, `results inspected` below is the exact distinct named in-scope lead count for the whole batch; candidate identities and source URLs are preserved in `track-b-c-search-results.md`. Retrieval language is English except B3's Spanish queries. Net-new addition means not already resolved to the same OSM identity at discovery time.

| batch | exact queries | language/script | distinct named in-scope results inspected | net-new identity leads |
|---|---|---|---:|---:|
| B1 | `best bakery Salt Lake City Utah Salt Lake Valley`; `best scratch bakery Salt Lake City Utah`; `best artisan baker led bakery Salt Lake City Utah`; `new bakery Salt Lake City Utah 2025 2026` | English/Latin | 28 | 7 |
| B2 | `best bakery Park City Utah artisan baker scratch`; `new bakery Park City Utah 2025 2026`; `best bakery Heber City Midway Utah`; `artisan bakery Heber City Midway Utah scratch` | English/Latin | 31 | 16 |
| B3 | `mejor panadería artesanal Salt Lake City Utah pan dulce`; `panadería mexicana West Valley City Utah conchas artesanal`; `bakery Millcreek Holladay Murray Utah artisan`; `bakery West Valley West Jordan South Jordan Utah artisan` | Spanish and English/Latin | 16 | 0 |
| B4 | `artisan bakery Sandy Draper Cottonwood Heights Utah`; `microbakery cottage bakery preorder Salt Lake City Utah`; `farmers market artisan bread baker Salt Lake City Utah`; `gluten free craft bakery Salt Lake City Park City Utah` | English/Latin | 19 | 5 |
| B5 | `canele bakery Salt Lake City Utah`; `kouign amann bakery Salt Lake City Park City Utah`; `naturally leavened sourdough bakery Salt Lake City Utah`; `Paris Brest pastry Salt Lake City Utah` | English with French marker terms/Latin | 14 | 2 |
| B6 | `house made phyllo bakery Salt Lake City Utah`; `pain suisse laminated brioche bakery Salt Lake City Utah`; `fresh stroopwafel Salt Lake City Utah bakery`; `artisan chocolatier pastry Salt Lake City Utah bonbon` | English with specialist terms/Latin | 13 | 7 |
| B7 | `fresh tortilla tortilleria Salt Lake City Utah made on site`; `tortillería artesanal West Valley City Utah tortillas frescas`; `bagel shop hand rolled boiled Salt Lake City Utah`; `baker owned bakery Salt Lake City Utah chef owner` | English and Spanish/Latin | 15 | 5 |
| B8 | `"grey rabbit" bakery Salt Lake City farmers market`; `"Bedlam" bakery Salt Lake City Stockist`; `"Cinnful Buns" Salt Lake City bakery`; `"Chubby Baker" Salt Lake City bakery` | English/Latin | 6 | 4 |

Track B total: 142 named in-scope lead occurrences inspected across batches; 46 net-new raw identity leads were recorded initially, then four obvious overlaps/aliases were consolidated to 42 Track B/C addition rows in the discovery ledger.

Local-language rationale: English is the dominant local business/search language and Utah place names use Latin script. Spanish is materially relevant to the Salt Lake Valley's panadería and tortillería traditions, so natural Spanish queries were run. French, Dutch, Greek, German, Arabic, Polish, Korean, Chinese, and Japanese traditions were searched through locally used romanized specialist/product terms; forcing non-local scripts would not reflect how these Utah businesses publish their identities.

## Track C — visible-head challenge

| batch | exact queries | source classes | named in-scope results inspected | additions |
|---|---|---|---:|---:|
| C1 | `site:gastronomicslc.com bakery Salt Lake City best bakery new`; `site:slmag.com bakery Salt Lake City Utah bakery`; `site:cityweekly.net bakery Salt Lake City bakery`; `site:parkcitymag.com "bakery" Park City new opening` | Gastronomic SLC, Salt Lake Magazine search, City Weekly search, Park City Magazine | 21 | 3 net-new/renamed identities; other results corroborated existing leads |

Additional visible-head sources checked during B batches: KSL/Deseret News, Salt Lake Tribune, Axios Salt Lake City, City Cast Salt Lake, Visit Utah/Heber Valley tourism, Park City Magazine, local Reddit community roundups, Restaurantji/Tripadvisor directory heads, and official producer sites. `cityweekly.net` blocked access by robots.txt; the failed source is logged rather than treated as checked content.

## Phase 2 count summary

- Track A: 245 returned elements across validated component responses; 241 unique OSM identities after source union.
- Track B: 142 named in-scope lead occurrences inspected; 42 retained net-new/identity-thin addition rows after immediate overlap consolidation.
- Track C: 21 named in-scope visible-head results inspected; three net-new or renamed identities, already included in the 42 addition rows.
- Discovery ledger total before Phase 3 semantic normalization: 283 rows (241 Track A + 42 Track B/C additions). Fourteen Track A rows are explicitly preserved as literal non-bakery regex collisions or non-retail industrial facilities and were not promoted to the candidate ledger; 269 raw in-category/category-adjacent leads entered `03-candidate-ledger.md` as `candidate-discovered`.
- Qualification/scoring actions performed: 0.
