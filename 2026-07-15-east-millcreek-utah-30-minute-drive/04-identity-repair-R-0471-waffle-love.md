# Identity repair memo — R-0471 Waffle Love

- Access date: 2026-07-15
- Candidate as dispatched: `R-0471 | Waffle Love`
- Defect: the candidate has no address, phone, coordinates, branch alias, source URL, or source-record identifier. Waffle Love is a multi-location restaurant/food-truck/franchise brand, so the supplied record does not select a physical venue.
- Scope of this memo: identity repair only. It does not complete Phase 4 evidence research and makes no quality, eligibility, scoring, or classification judgment.

## Recovered Utah identities and operating-status facts

### West Jordan restaurant

- Official current location label: **WEST JORDAN RESTAURANT**.
- Official recurring hours: **“Mon - Thur 8AM - 10PM | fRI & Sat 8am-11pm | closed sundays.”**
- Address/phone recovered from a City of West Jordan restaurant directory: **7612 S Campus View Dr**, **801-923-3588**.
- Current official location source: https://wafflelove.com/waffle-love-utah-restaurants
- Municipal directory source: https://assets.westjordan.utah.gov/ugd/41b712_159fd3df574d483d80976a7776b075a3.pdf
- Status: represented as a current restaurant on the official Waffle Love Utah locations page at access time.

### West Valley location

- Listing label: **Waffle Love - West Valley**.
- Phone: **(801) 981-8395**.
- Address: not exposed in the accessible Wanderlog result used during the repair search.
- Status: **“Permanently Closed”**; every weekday field also displays “Permanently closed.”
- Rating attached specifically to this closed listing: **3.5 (204)**.
- Source: https://wanderlog.com/place/details/1993715/waffle-love-west-valley
- Status note: this is a third-party status, not an official closure announcement.

### Draper location

- Listing label: **Waffle Love - Draper**; search result locality renders **Sandy, UT**.
- Source: https://wanderlog.com/place/details/1993710/waffle-love-draper
- Address, phone, literal rating value/count, and current operating status were not exposed in the accessible search result and remain unresolved.

### Utah food trucks / catering

- The official site describes the brand as **“sweet & savory, catering, and food trucks!”**
- The official menu says: **“Click below to find the food truck menu near you!”**
- Official sources: https://wafflelove.com/ and https://wafflelove.com/menu
- These are mobile/service identities rather than a uniquely addressable restaurant branch. No truck schedule or event location was attached to R-0471.

### Other Utah brand/location signals

- The official Utah restaurant page was searched for all current Utah storefronts, but the accessible result exposed only the West Jordan location block quoted above.
- Official contact copy asks applicants to identify **“which location(s)”**, confirming plural operations, and identifies Waffle Love HQ in **Springville, UT**. HQ is not treated as a restaurant without a restaurant listing.
- Source: https://wafflelove.com/contact
- Search discussions mention historic Orem and Ogden locations, including user statements that locations closed. These were not promoted into verified branch records because no official/current address-and-status source was recovered during this bounded repair.

## Catchment relationship

- The run catchment is the 30-minute automobile isochrone from 2958 South 2520 East, Millcreek, Utah 84109.
- The existing structured candidate/catchment population admitted R-0471 but supplied no coordinates or address in the dispatch record. That admission alone does not identify which Waffle Love branch or mobile record generated the candidate.
- **West Jordan, 7612 S Campus View Dr:** an exact branch identity is recovered, but this memo does not have a preserved route-duration/catchment-membership record tying that address to R-0471. Its inside/outside status is therefore unresolved here.
- **West Valley:** no address was recovered from the opened source, so catchment membership cannot be tested from this evidence.
- **Draper/Sandy listing:** no exact address was recovered, so catchment membership cannot be tested from this evidence.
- **Food truck/catering:** mobile and event-dependent; catchment membership cannot be assigned without the originating event or truck coordinates/date.
- No branch is claimed inside the catchment solely from city name, brand membership, or the parent candidate's presence.

## Exact evidence needed to repair R-0471

Use one of these auditable paths:

1. **Select one physical branch:** recover R-0471's originating discovery row with its source URL, map feature/place ID, coordinates, address, phone, or official-location URL. Match at least one stable field to an official/current branch record, then attach R-0471 to that branch.
2. **Split a brand-level discovery row:** if the originating row is genuinely brand-level rather than a place record, enumerate every current physical Waffle Love branch whose address falls inside the saved isochrone. Create one candidate ID per physical branch and preserve the brand-level R-0471 record as the split provenance parent.
3. **Represent a mobile venue:** if the origin is a food-truck record, recover the truck identifier and a dated recurring service location inside the catchment. Do not substitute a storefront's ratings, hours, or reviews for the truck.
4. **Quarantine if unresolved:** if the origin supplies no selector and current official pages do not expose a matching branch, retain R-0471 in identity quarantine rather than combining branch evidence.

For any physical branch selected or created, the minimum identity packet is: official displayed branch name, full street address, phone if published, official branch URL, coordinates or a geocodable address, current operating status, and a stored isochrone inclusion result. Branch-specific Phase 4 rating, hours, and review evidence must then be researched separately.

## Search trail

- Opened/searched official home, Utah restaurant locations, menu, contact, catering, Liege-waffle process blog, online dough FAQ/store, KSL interview, Utah Business interview, Wanderlog West Valley, Wanderlog Draper, City of West Jordan directory, Reddit closure/history discussions, and targeted location/closure queries.
- Queries: `Waffle Love Salt Lake City official locations menu`; `Waffle Love Salt Lake City reviews rating`; `Waffle Love Utah dough made from scratch liege waffle interview`; `Waffle Love closed Salt Lake City locations`.
- Additional official sources retained for later evidence retrieval, not identity selection: https://wafflelove.com/blog/belgian-liege-waffles-at-waffle-love, https://waffle-love.square.site/dough, https://www.ksl.com/article/35289692, and https://www.utahbusiness.com/archive/2015/10/19/utah-food-truck-brings-waffles-with-love/.

## Repair status

`identity-unresolved`: R-0471 cannot yet be selected or split because its originating address/coordinates/source record are absent. Phase 4 evidence completion is not claimed.
