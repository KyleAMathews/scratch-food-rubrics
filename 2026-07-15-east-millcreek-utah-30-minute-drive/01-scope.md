# Phase 1 — Scope and catchment

## Requested place and origin

- Original request: all restaurants within a 30-minute drive of the user's house in East MillCreek, as pinned in the supplied screenshot.
- Canonical origin: **2958 South 2520 East, Millcreek, Utah 84109, United States**.
- Geocoded OSM form: **2958, 2520 East, Canyon Rim, Millcreek, Salt Lake County, Utah, 84109, United States**.
- Origin coordinate: **40.7067859, -111.8192536**.
- Country/region pin for every query: **United States — Utah — Salt Lake County / Wasatch Front**.
- Local-script name: English uses the same Latin-script name; no distinct local-script form applies.

## Exact included area

The inclusion boundary is the polygon in `02-source-data/30-minute-auto-isochrone.geojson`: the 30-minute automobile isochrone routed from the origin coordinate by the public Valhalla instance using OpenStreetMap road data. Request parameters were `costing=auto`, `contours=[{"time":30}]`, `polygons=true`, `denoise=1`, and `generalize=100`.

The returned non-zero polygon has 1,566 vertices and bounding box **longitude -112.282774 to -111.401008; latitude 40.396699 to 41.062062**. Candidate coordinates must fall inside this polygon. Borderline candidates will receive a destination-specific route check from the same origin; a modeled drive time of 30:00 or less is included.

Sources retrieved 2026-07-15:

- Nominatim/OpenStreetMap geocoder: `https://nominatim.openstreetmap.org/search?q=2958%20South%202520%20East%2C%20Millcreek%2C%20Utah%2084109%2C%20United%20States&format=jsonv2&addressdetails=1&limit=5`; literal response preserved as `02-source-data/origin-geocode.json`.
- Valhalla isochrone service: `https://valhalla1.openstreetmap.de/isochrone` with the request parameters above; literal GeoJSON response preserved as `02-source-data/30-minute-auto-isochrone.geojson`.

## Market calibration and exclusions

This is a user-defined metropolitan drive-time catchment, not a municipal-place request. The boundary intentionally crosses Millcreek into every part of the contiguous Wasatch Front reachable within the modeled 30 minutes; municipal limits and a universal radius would contradict the request. It can include portions of Salt Lake City, South Salt Lake, Murray, Holladay, Cottonwood Heights, Midvale, Sandy, West Valley City, Taylorsville, and other communities where the routed polygon reaches them.

Excluded as separate/out-of-scope markets are **all coordinates outside the saved isochrone**, even when a search result labels them “Salt Lake City.” This excludes the main cores of Ogden, Provo/Orem, Park City, and Tooele unless an individual venue point and route unexpectedly satisfy the explicit 30-minute boundary. A venue whose point falls in a generalized edge lobe but whose destination route exceeds 30 minutes is also excluded.

## Uncertainty and tool limits

- The Valhalla public endpoint models automobile travel from its current OpenStreetMap-derived routing graph; it does **not** reproduce live traffic, departure-time congestion, weather, temporary closures, private-road constraints, parking, or the user's personal driving speed.
- “30-minute drive” is therefore operationalized as a reproducible off-peak routing estimate at research time, not a guarantee for every departure time.
- The polygon was generalized by 100 meters. Borderline venues require point-specific routing to avoid polygon-edge artifacts.
- Restaurant completeness is not implied by the routing source. Candidate discovery will use multiple independent and targeted sources in later phases.
