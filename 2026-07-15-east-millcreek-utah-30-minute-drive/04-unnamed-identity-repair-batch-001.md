# Unnamed OSM identity repair — batch 001

Access date: 2026-07-15. Identity repair only; no Phase 4 evidence completion or restaurant-quality judgment is claimed.

## R-0424 — OSM node/3728547726

- Input: 2130 S Highland Dr; 40.7242341,-111.859843; `cuisine=thai`.
- Resolved identity: **Taste Of Thai Sugar House**, 2130 S Highland Dr, Salt Lake City, UT 84106; +1 (385) 420-4141; https://tasteofthaisugarhouse.com/.
- Exact corroboration: Apple Maps matches name, address, phone and website: https://maps.apple.com/place?place-id=IB98D8E4738861AE9. MapQuest matches name/address/phone: https://www.mapquest.com/us/utah/taste-of-thai-sugar-house-776268884. Salt Lake City’s October 2024 approved-business-license list names **TASTE OF THAI** at **2130 S HIGHLAND DR**: https://www.slcdocs.com/business/new_bus_list_2024_oct.pdf.
- Historical alternative: older directories still attach **Cubby’s**, (801) 467-2980, to the same address, indicating address turnover rather than the current Thai record being Cubby’s: https://www.menupix.com/saltlakecity/restaurants/27198833/Cubbys-Salt-Lake-City-UT.
- Existing-candidate check: the structured population contains `R-1331 | Taste of Thai` at 1241 Center Drive, Park City, a different physical branch/address; it is not this venue.
- Final state: **ready** — rename R-0424 to `Taste Of Thai Sugar House` and retain its original OSM provenance.

## R-0954 — OSM node/6620807150

- Input: 40.7650978,-111.845872; `juice`, `fast_food`; no address, phone or domain.
- Searches: exact-coordinate web search; nearby Salt Lake juice/smoothie searches; official Juice Shop, Jamba and Roxberry location searches. Sources checked include https://www.thejuiceshopslc.com/, https://locations.jamba.com/, and https://threebestrated.com/juice-bars-in-salt-lake-city-ut.
- Alternatives found were spatially different: The Juice Shop is documented at 888 S 200 E; Roxberry City Creek at 28 State St; Just Organic Juice at 2030 S 900 E. None matches the supplied coordinate closely enough to transfer identity.
- Evidence needed: reverse-geocoded parcel/address or a current map place ID at the coordinate, followed by an official address/phone match. A cuisine tag alone is insufficient.
- Final state: **still-quarantined**.

## R-0985 — OSM node/7185013217

- Input: 40.6599242,-111.5082097; `bar`; no address, phone or domain.
- Searches: exact-coordinate search, Park City bar maps/directories, official/tourism records for No Name Saloon, The Spur, Old Town Cellars, Park City Roadhouse and resort bar listings. Sources include https://www.visitparkcity.com/listing/the-spur-bar-%26-grill/15331/ and https://www.parkcitylodging.com/area/directory/dining/no-name-saloon.
- No opened source matched this coordinate to a named establishment. The coordinate is east of central Park City; prominent Main Street bar identities were not transferred based on city/category proximity.
- Evidence needed: reverse-geocoded street/building/resort parcel, OSM node history or nearby-feature query, then official/map corroboration of name and current public operation.
- Final state: **still-quarantined**.

## R-1288 — OSM node/9991792225

- Input: 11486 S District Dr; (801) 285-9099; villagebakerfood.com; 40.542384,-111.982017.
- Resolved identity: **Village Baker - District**, 11486 S District Dr Ste 300, South Jordan, UT 84095; +1 801-285-9099; http://villagebakerfood.com/.
- Exact corroboration: Tripadvisor matches name/address/phone/domain: https://www.tripadvisor.com/Restaurant_Review-g57131-d13798666-Reviews-Village_Baker_District-South_Jordan_Utah.html. Waze independently matches all identity fields: https://www.waze.com/live-map/directions/village-baker-s-district-dr-11486-south-jordan?to=place.w.162529685.1625427926.5350495. MapQuest matches suite/address/phone/domain: https://www.mapquest.com/us/utah/village-baker-380364439.
- Existing-candidate check: the structured population includes `R-0732 | Village Baker` at 1658 W 9000 S, West Jordan, a distinct branch. No existing named candidate for the District address was found.
- Final state: **ready** — rename R-1288 to `Village Baker - District` and retain its original OSM provenance.

## R-1401 — OSM node/10749321081

- Input: 40.7759458,-112.0276056; `pub`; no address, phone or domain.
- Searches: exact-coordinate search; west/northwest Salt Lake pub, bar, brewery and airport-area searches; local pub directories and direct official queries. Search results for downtown venues (Poplar Street Pub, Green Pig, Piper Down) and airport Jamba were spatially unrelated and were not assigned.
- No source matched the coordinate to a named current public pub. No evidence established that the node is public-facing food service rather than an amenity inside another facility.
- Evidence needed: OSM node history/changeset and nearby-feature query, reverse-geocoded parcel/facility name, liquor-license/business-license match, and current official/map identity corroboration.
- Final state: **still-quarantined**.

## Batch result

- Ready: R-0424 → Taste Of Thai Sugar House; R-1288 → Village Baker - District.
- Duplicate-of-existing-ID: none. Same-name records found were different physical branches.
- Non-public/non-food: none established.
- Still-quarantined: R-0954, R-0985, R-1401.
