# Phase 1 — Scope and Catchment

Read `shared-status-and-provenance.md` in full immediately before executing this phase.

## Input

The user's requested location and the category selected by the invoked root skill.

## Required actions

1. Before any research, create the mandatory run directory from `shared-status-and-provenance.md`: `<YYYY-MM-DD>-<location-slug>/` in the current working directory. If it exists, use the next numeric suffix. Create every standard subdirectory and initial artifact.
2. Create it concretely before calling any research tool. First derive `LOCATION_SLUG` according to the shared contract, then run the equivalent of:

   ```bash
   base="$(date +%F)-${LOCATION_SLUG}"
   run="$base"
   suffix=2
   while [ -e "$run" ]; do
     run="${base}-${suffix}"
     suffix=$((suffix + 1))
   done
   mkdir -p "$run/02-source-data" "$run/04-worker-returns"
   touch "$run/00-run-manifest.md" "$run/01-scope.md" \
     "$run/02-discovery-ledger.md" "$run/02-query-log.md" \
     "$run/03-candidate-ledger.md" "$run/04-worker-returns/index.md" \
     "$run/05-evidence-ledger.md" "$run/05-repair-log.md" \
     "$run/06-decisions.md" "$run/07-coverage-audit.md" "$run/08-results.md"
   RUN_DIR="$(cd "$run" && pwd -P)"
   ```

   Keep the resulting absolute path as `{RUN_DIR}` for every subsequent phase. If the runtime does not preserve shell variables between commands, recover it from the manifest rather than creating another directory.

3. Write `{RUN_DIR}/00-run-manifest.md` immediately with: invoked category, original user request, canonical requested location if known, creation date/time, run-directory absolute path, and status `phase-1-in-progress`. This manifest is the authoritative pointer for the rest of the run.
4. Resolve the intended place, country, region/state/county, and local-script name. Region-pin every later query.
5. Define the resident-normal market rather than blindly using municipal limits or a universal radius.
6. Prefer a real OSM administrative polygon for a named incorporated place. Use `map_to_area`, verify that the result is non-zero, and fall through loudly if it fails.
7. Calibrate extensions by market type:
   - For a standalone town with countryside, include the resident-normal rural ring, approximately a 15–20 minute drive where appropriate.
   - For a town embedded in a contiguous metro, use the place plus immediately adjacent neighborhoods, not a radius that annexes other towns.
   - For a user-named corridor, valley, or neighborhood set, record an explicit polygon, bounding box, or component list.
8. Record included areas, adjacent markets excluded as separate runs, boundary method and source, and uncertainty.
9. If the requested scope cannot be researched completely with available tools, narrow it explicitly before discovery. Never narrow it silently later to make completion easier.

## Prohibited

- Do not begin research before the run directory and manifest exist.
- Do not begin candidate discovery before `{RUN_DIR}/01-scope.md` exists.
- Do not use a universal 12 km radius.
- Do not exclude countryside venues merely because they lie outside a town core.
- Do not annex neighboring incorporated markets merely because they fall inside a geometric circle.

## Output

Write `{RUN_DIR}/01-scope.md` with the canonical and local-script place names, country and region pin, boundary or component list, boundary source and method, center/radius if used, included rural or adjacent areas, excluded markets, uncertainty, and tool limitations. Update `00-run-manifest.md` with the canonical location, final `{RUN_DIR}` name, and status `phase-1-complete`.

## Completion gate

- [ ] A new, non-reused `<YYYY-MM-DD>-<location-slug>` run directory exists.
- [ ] `00-run-manifest.md` contains the request, category, date/time, absolute run path, and Phase 1 status.
- [ ] Every standard artifact directory or placeholder exists inside `{RUN_DIR}` and no run artifact exists outside it.
- [ ] `01-scope.md` exists and records the exact included area.
- [ ] Adjacent exclusions recorded.
- [ ] Boundary method and source recorded.
- [ ] Non-zero boundary verified or fallback documented.
- [ ] Market-type calibration explained.
- [ ] Uncertainty and tool limits stated.
