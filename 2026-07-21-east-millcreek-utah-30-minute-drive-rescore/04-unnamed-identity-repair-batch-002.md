# Unnamed OSM identity repair — batch 002

Access date: 2026-07-15. Identity repair only; no restaurant-quality judgment or Phase 4 completion is claimed.

## R-1473 — OSM node/11177832046

- Input: 40.7159123,-111.8898543; `fast_food`; no address, phone or domain.
- Spatial alternative: the point is near the State Street/2700 South commercial corridor. Nearby fast-food searches surfaced multiple businesses; no opened primary/current source matched the exact point or OSM identifier.
- Sources/searches: exact coordinate, OSM ID, nearby fast-food and State Street/2700 South business searches; current map/directory results. No stable address/place ID was recovered.
- Required evidence: OSM node history/changeset or reverse-geocoded parcel, then an exact current business address/phone/domain match.
- Final state: **still-quarantined**.

## R-1848 — OSM node/12634034763

- Input: 40.6196259,-111.8933539; `sandwich`, `fast_food`; no address, phone or domain.
- Spatial alternative: the point lies on/near the State Street commercial corridor around Midvale. Searches exposed several sandwich chains but no source tied one exact tenant to this coordinate.
- Sources/searches: exact coordinate and OSM ID; nearby sandwich/fast-food, State Street Midvale, Subway, Jersey Mike’s, Jimmy John’s and deli searches. No exact address/phone match was recovered.
- Required evidence: OSM node history or reverse-geocoded suite/address and a current official locator match.
- Final state: **still-quarantined**.

## R-1944 — OSM node/12943651571

- Input: 40.7679227,-111.8872767; `coffee_shop`, `cafe`; no address, phone or domain.
- Spatial alternative: the point is in central Salt Lake City east of Main Street. Nearby coffee searches returned several plausible cafes, but none was supported by an exact coordinate/address match.
- Sources/searches: exact coordinate and OSM ID; downtown coffee-shop/cafe map searches; official Starbucks, local cafe and directory searches. No exact current tenant was established.
- Required evidence: reverse-geocoded building/suite, OSM history/nearby-feature query, then official locator or current business-license corroboration.
- Final state: **still-quarantined**.

## R-2156 — OSM way/34686285

- Input: 400 W Parrish Ln, Centerville; dairyqueen.com menu; 40.9217918,-111.8850269.
- Resolved identity: **Dairy Queen Grill & Chill**, 400 W Parrish Ln, Centerville, UT 84014; (801) 295-1319; official store locator ID 6115.
- Exact sources: current locator-linked directory matches name/address/phone and official store URL: https://usarestaurants.info/explore/united-states/utah/davis-county/centerville/dairy-queen-grill-chill-801-295-1319.htm; Yellow Pages independently matches name/address/phone/domain: https://www.yellowpages.com/centerville-ut/dairy-queen; City-Data matches address, phone, domain and services: https://www.city-data.com/locations/DairyQueen/Davis-County-UT.html.
- Status alternative: AutoReserve displays every weekday “Closed,” conflicting with current directory/official-locator-linked hours; this is retained as a status conflict, not closure resolution: https://autoreserve.com/en/restaurants/AEq36NDN9HvzPUkjryso.
- Final state: **ready** — rename R-2156 to `Dairy Queen Grill & Chill — Centerville` and retain OSM provenance.

## R-2313 — OSM way/348020920

- Input: 130 W 10600 S, Sandy; `American`, `restaurant`; 40.5593104,-111.8943536.
- Resolved identity: **Potbelly Sandwich Shop** / current listing **Potbelly**, 130 W 10600 S Ste B, Sandy, UT 84070; (801) 307-4830.
- Exact source: Restaurantji matches address and current tenant, phone, category and hours: https://www.restaurantji.com/ut/sandy/potbelly-sandwich-shop-/.
- Co-address alternative: Starbucks also lists 130 W 10600 S, but the OSM way is tagged `American restaurant`, and Potbelly’s suite-B record is an exact restaurant/address match; Starbucks remains a separate co-located unit: https://www.restaurantji.com/ut/sandy/starbucks-4/.
- Final state: **ready** — rename R-2313 to `Potbelly Sandwich Shop — Sandy` and preserve the way ID/address provenance.

## Batch result

- Ready: R-2156 → Dairy Queen Grill & Chill — Centerville; R-2313 → Potbelly Sandwich Shop — Sandy.
- Duplicate-of-existing-ID: none established.
- Non-public/non-food: none established.
- Still-quarantined: R-1473, R-1848, R-1944.
