# Phase 1 — Scope and Catchment

## Canonical request

- User wording: "salt lake valley & park city / midway / heber city -- we're in east millcreek so this is the general area we're in"
- Canonical location: Salt Lake Valley and the Wasatch Back corridor of Park City, Heber City, and Midway, Utah, United States
- Home base and travel origin: East Millcreek, within Millcreek, Salt Lake County
- Country/region pin for every discovery query: Utah, United States (`UT`, `US`); county pins as appropriate: Salt Lake County, Summit County, or Wasatch County
- Canonical/local-script names: Salt Lake Valley; East Millcreek; Park City; Heber City; Midway. English Latin-script names are the local names; no alternate local script applies.

## Market type and calibration

This is a user-named, multi-component resident-and-day-trip market rather than one municipality. A universal radius would incorrectly annex Davis, Tooele, and Utah County markets while missing the Park City–Heber corridor. The catchment therefore uses an explicit component list: the populated Salt Lake Valley, the resident-normal Park City/Snyderville market, the Heber Valley communities named by the user, and the connecting travel corridors.

## Included area

### A. Salt Lake Valley component

The populated valley-floor portion of Salt Lake County, including the municipalities and census communities normally treated as the Salt Lake Valley market:

- Salt Lake City, South Salt Lake, Millcreek (including East Millcreek/Canyon Rim), Holladay, Murray, Midvale, Cottonwood Heights, Sandy, and the Salt Lake County portion of Draper;
- West Valley City, Taylorsville, Kearns, Magna, West Jordan, South Jordan, Riverton, Herriman, Bluffdale, White City, Granite, and Copperton;
- the continuous East Bench/foothill neighborhoods and valley commercial strips connecting those places.

Salt Lake County's OSM administrative polygon is the outer verification boundary, but discovery is limited to its populated valley component; the polygon's mountain watersheds and west-desert acreage do not silently enlarge the market.

### B. Park City resident-normal component

- Park City municipal limits; and
- the continuous Snyderville Basin market used by Park City-area residents: Summit Park, Jeremy Ranch, Pinebrook, Kimball Junction, Canyons Village, Snyderville, Silver Creek/Silver Summit, and immediately continuous developed nodes.

This extension is deliberate because municipal Park City excludes major everyday commercial nodes such as Kimball Junction. It is a component-list extension, not a radial annexation of all Summit County.

### C. Heber Valley component

- Heber City and Midway municipal limits; and
- the immediately continuous Heber Valley settlements of Daniel, Charleston, North Fields, and developed areas between Heber City and Midway.

This is the resident-normal rural ring for the paired Heber/Midway market. It includes a roughly 15–20-minute local-drive countryside ring where settlement is continuous, but not all of Wasatch County.

### D. Connecting corridor

Venues physically on the normal route from East Millcreek through Parley's Canyon on I-80 to the Snyderville/Park City component, then US-40 to Heber City and UT-113 to Midway, are in scope when they serve one of the named components. A highway location alone does not pull a separate town into scope.

## Adjacent markets excluded as separate runs

- Davis County communities, including North Salt Lake, Bountiful, and Woods Cross;
- Tooele Valley and Tooele County outside Salt Lake County's populated-valley edge;
- Utah County, including Lehi, Alpine, American Fork, and Provo/Orem;
- Ogden/Weber County and Morgan County;
- eastern Summit County towns and rural markets including Kamas, Francis, Oakley, Coalville, and Echo;
- Wasatch County beyond the Heber Valley resident-normal ring, including distant Jordanelle developments and US-40 south/east beyond the continuous Heber market;
- destination-only canyon/ski markets at Alta, Snowbird, Brighton, and Solitude. A bakery with a valley-floor production storefront remains eligible at that storefront.

## Boundary method, sources, and verification

Boundary method: explicit component list, with OSM administrative areas used where they exist and official city GIS/map sources used as fallbacks.

- OpenStreetMap/Nominatim resolved Salt Lake County to relation `1744366`, bbox `40.4141690,-112.2602160` to `40.9218470,-111.5531880`; Park City to relation `198864`, bbox `40.5992976,-111.5590250` to `40.7033812,-111.4607004`; Midway to relation `198866`, bbox `40.4865318,-111.5014098` to `40.5410729,-111.4509870`; and Millcreek to relation `9166755`, bbox `40.6590836,-111.9211040` to `40.7143706,-111.7768096`. Accessed 2026-07-14 via `https://nominatim.openstreetmap.org/search`.
- Overpass `map_to_area` returned non-zero areas `3601744366` (Salt Lake County), `3600198864` (Park City), and `3609166755` (Millcreek), accessed 2026-07-14 via `https://overpass-api.de/api/interpreter`.
- Midway relation `198866` exists with a non-zero bounding box, but Overpass did not return area `3600198866`. Fallback: the official [Midway zoning map](https://midwaycityut.org/wp-content/uploads/2022/05/Midway-Zoning-Map-2019-Jan-31.pdf), which explicitly maps the Midway City Boundary and growth boundary.
- Nominatim returned Heber City only as place node `150952081`, bbox `40.4664630,-111.4532963` to `40.5464630,-111.3732963`, not an administrative polygon. Fallback: [Heber City GIS](https://heberut.gov/425/GIS) and its official zoning/municipal-boundary map. The city's planning guidance states that its GIS zoning map is the address-level source for whether a parcel lies within Heber City boundaries.
- [Park City GIS](https://www.parkcity.org/departments/gis) is the official municipal corroboration for the Park City boundary; OSM provides the usable administrative polygon.

## Uncertainty and tool limits

- "Salt Lake Valley" has no single incorporated administrative polygon. Salt Lake County is a reproducible outer boundary but includes mountains and non-valley land, so the explicit populated-component list controls.
- OSM lacks a usable administrative area for Heber City and did not materialize Midway's relation as an Overpass area at access time. Official city maps are the documented fallback; candidate addresses near those boundaries will be checked individually.
- Snyderville Basin and Heber Valley are functional markets with fuzzy edges. The named communities above control inclusion; ambiguous edge candidates will be recorded rather than silently discarded.
- Research tools may miss cottage/preorder bakers and businesses without indexed websites. Later phases must use social, local-language/adjacent-category, and specialist discovery and document any access limitation.

## Phase status

`phase-1-complete`
