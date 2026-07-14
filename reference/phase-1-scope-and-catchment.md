# Phase 1 — Scope and Catchment

Read `shared-status-and-provenance.md` in full immediately before executing this phase.

## Input

The user's requested location and the category selected by the invoked root skill.

## Required actions

1. Resolve the intended place, country, region/state/county, and local-script name. Region-pin every later query.
2. Define the resident-normal market rather than blindly using municipal limits or a universal radius.
3. Prefer a real OSM administrative polygon for a named incorporated place. Use `map_to_area`, verify that the result is non-zero, and fall through loudly if it fails.
4. Calibrate extensions by market type:
   - For a standalone town with countryside, include the resident-normal rural ring, approximately a 15–20 minute drive where appropriate.
   - For a town embedded in a contiguous metro, use the place plus immediately adjacent neighborhoods, not a radius that annexes other towns.
   - For a user-named corridor, valley, or neighborhood set, record an explicit polygon, bounding box, or component list.
5. Record included areas, adjacent markets excluded as separate runs, boundary method and source, and uncertainty.
6. If the requested scope cannot be researched completely with available tools, narrow it explicitly before discovery. Never narrow it silently later to make completion easier.

## Prohibited

- Do not begin candidate discovery before the scope record exists.
- Do not use a universal 12 km radius.
- Do not exclude countryside venues merely because they lie outside a town core.
- Do not annex neighboring incorporated markets merely because they fall inside a geometric circle.

## Output

Record the canonical and local-script place names, country and region pin, boundary or component list, boundary source and method, center/radius if used, included rural or adjacent areas, excluded markets, uncertainty, and tool limitations.

## Completion gate

- [ ] Exact included area recorded.
- [ ] Adjacent exclusions recorded.
- [ ] Boundary method and source recorded.
- [ ] Non-zero boundary verified or fallback documented.
- [ ] Market-type calibration explained.
- [ ] Uncertainty and tool limits stated.
