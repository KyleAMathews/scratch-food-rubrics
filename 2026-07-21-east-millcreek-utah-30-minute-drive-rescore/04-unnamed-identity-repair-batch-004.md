# Unnamed OSM identity repair — batch 004

Access date: 2026-07-15. Identity repair only; no quality scoring or Phase 4 completion claim.

## R-2582 — OSM way/616844680
- Input: 1356 S State St, Salt Lake City; 40.7402569,-111.8886029.
- Resolved identity: **Little World Chinese Restaurant**, 1356 S State St, Salt Lake City, UT 84115; (801) 467-5213.
- Exact sources: Visit Salt Lake matches name/address/phone: https://www.visitsaltlake.com/listing/little-world-chinese-restaurant/61177/. OpenTable independently matches name/address/phone: https://www.opentable.com/r/little-world-chinese-restaurant-salt-lake-city. Waze matches the same fields: https://www.waze.com/live-map/directions/little-world-chinese-restaurant-s-state-st-1356-salt-lake-city?to=place.w.162595223.1626017770.3100451.
- Final state: **ready**.

## R-2630 — OSM way/675431715
- Input: 1021 N Catherine St, Salt Lake City; 40.7916419,-111.932972.
- Conflicting identities: official-social result **Los Girasoles Homemade Mexican Food**, address 1021 N Catherine St, phone 801-300-9401: https://www.facebook.com/losgirasolesmexicanfood/. Yellow Pages lists **La Margarita Restaurant**, same address, phone (801) 924-8594: https://www.yellowpages.com/rose-park-salt-lake-city-ut/mexican-restaurants. Another directory lists **El Cabrito**, same address, phone (801) 363-2645.
- The address has multiple historical/current names and the way lacks a name/phone/domain. Exact tenant chronology and geometry continuity were not established.
- Needed: OSM way history/name tags plus current business-license or official current address/phone confirmation.
- Final state: **still-quarantined**.

## R-2634 — OSM way/691138791
- Input: 40.9845213,-111.8947194; no tags beyond food-service quarantine context.
- Exact-coordinate, OSM-ID, nearby restaurant/business and reverse-area searches did not produce a named current public venue tied to the geometry.
- Needed: reverse-geocoded parcel/address, OSM way history and official/map tenant corroboration.
- Final state: **still-quarantined**.

## R-2686 — OSM way/856930729
- Input: 2701 S Main St, South Salt Lake; 40.7124345,-111.8909111.
- Resolved identity: **Cafe on Main / Café On Main**, 2701 S Main St, South Salt Lake, UT 84115; (801) 487-9434; https://www.cafeonmainslc.com/.
- Exact sources: official site matches name/address and identifies a family-owned Balkan restaurant: https://www.cafeonmainslc.com/. Official Facebook matches address: https://www.facebook.com/Cafeonmainslc/. Seamless matches name/address/phone: https://www.seamless.com/menu/caf-on-main-2701-s-main-st-south-salt-lake/2207139. A 2013 Salt Lake Tribune archive confirms the same name/address/phone historically: https://archive.sltrib.com/article.php?id=54928105&itype=cmsid.
- Final state: **ready**.

## R-2716 — OSM way/984963402
- Input: 265 W 7200 S, Midvale; fast_food; 40.620269,-111.8989153.
- Resolved identity: **Mi Rico Burrito**, 265 W 7200 S, Midvale, UT 84047; official current site phone (385) 245-1299; https://miricoburritout.com/.
- Exact sources: official site matches name/address/phone: https://miricoburritout.com/. Grubhub matches name/address but displays (801) 566-5107 and 272 ratings: https://www.grubhub.com/restaurant/mi-rico-burrito-265-w-7200-s-midvale/2046074. Another ordering provider displays (801) 856-2733, preserving phone drift: https://fromtherestaurant.com/mi-rico-burrito/menu/265-W-7200-S/. Tripadvisor matches name/address: https://www.tripadvisor.com/Restaurant_Review-g57062-d19424657-Reviews-Mi_Rico_Burrito-Midvale_Utah.html.
- Final state: **ready**; preserve conflicting published phones for later identity/evidence review.

## Batch result
- Ready: R-2582 Little World Chinese Restaurant; R-2686 Cafe on Main; R-2716 Mi Rico Burrito.
- Duplicate-of-existing-ID: none established.
- Non-public/non-food: none established.
- Still-quarantined: R-2630, R-2634.
