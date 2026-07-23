# Unnamed OSM identity repair — batch 003

Access date: 2026-07-15. Identity repair only; no scoring or Phase 4 completion claim.

## R-2327 — OSM way/357488914
- Input: 40.6941656,-111.9575726; pizza restaurant; no identity fields.
- Searches: exact coordinate/OSM ID, nearby pizza/business directories and official locators. Multiple west-valley pizza alternatives appeared, but no exact address or place-ID match was recovered.
- Needed: OSM way history or reverse-geocoded parcel/address followed by official name/address corroboration.
- Final state: **still-quarantined**.

## R-2387 — OSM way/422029992
- Input: 40.7419108,-111.9385888; Mexican restaurant; no identity fields.
- Searches: exact coordinate/OSM ID, nearby Mexican restaurant/map/business-license records. No current tenant was tied exactly to the point.
- Needed: OSM history, parcel/suite address and exact official/map match.
- Final state: **still-quarantined**.

## R-2473 — OSM way/503688439
- Input: 2274 E 3900 S, Holladay; fast_food; 40.6868384,-111.8254769.
- Current candidate identity: **SWIZZLE**, 2274 E 3900 S, Holladay, UT 84124; (801) 428-9119. Restaurantji matches address/category/phone and shows current 2026 listing: https://www.restaurantji.com/ut/holladay/the-park-5-/.
- Continuity: current listing retains the historic URL slug `the-park-5`; **The Park 5** used the same address, phone and `thepark5.com`: https://usarestaurants.info/explore/united-states/utah/salt-lake-county/holladay/the-park-5-801-428-9119.htm.
- Historical alternatives at the parcel: **Holy Mole WackyMole** is marked closed at the address: https://www.mapquest.com/us/utah/holy-mole-wackymole-443393431. **Beto’s** is marked “may be permanently closed,” phone (801) 274-8896: https://es.restaurantguru.com/Betos-Salt-Lake-City-3. Papa Murphy’s, Subway and Arby’s are also co-located/adjacent businesses in the larger parcel, so address alone cannot identify every geometry.
- Geometry-to-tenant caveat: the OSM way predates the current Swizzle listing and the property contains multiple businesses. Same phone/address continuity between The Park 5 and Swizzle is stronger than address-only alternatives, but an OSM way-history/name tag is still needed to prove which building/unit geometry way/503688439 denotes.
- Final state: **still-quarantined** pending OSM way-history/unit match; leading identity alternative is `SWIZZLE (formerly The Park 5)`.

## R-2481 — OSM way/514896583
- Input: 40.7407061,-111.8915875; restaurant; no identity fields.
- Searches: exact coordinate/OSM ID, reverse-area restaurant and current map/business records. No exact named tenant was corroborated.
- Needed: reverse-geocoded address/building and OSM history, then official/current place match.
- Final state: **still-quarantined**.

## R-2487 — OSM way/522750580
- Input: 40.6880491,-111.8451474; cafe; no identity fields.
- Searches: exact coordinate/OSM ID and nearby Millcreek/Holladay cafe and coffee-shop records. No exact coordinate/address match was recovered.
- Needed: OSM history or parcel/suite address plus official locator/business-license corroboration.
- Final state: **still-quarantined**.

## Batch result
- Ready: none.
- Duplicate-of-existing-ID: none established.
- Non-public/non-food: none established.
- Still-quarantined: R-2327, R-2387, R-2473, R-2481, R-2487. R-2473 has a documented leading identity and tenant-history chain but still lacks geometry-to-unit proof.
