# Phase 2 — Candidate Discovery

Read `shared-status-and-provenance.md` and the invoked category's `discovery-reference.md` in full immediately before executing this phase. Do not rely on marker terms remembered from the root skill.

## Input

The completed Phase 1 scope record and the category discovery reference named by the root skill.

## Purpose

Build a union. Broad survey protects the obscure long tail; targeted search protects prominent, new, renamed, poorly tagged, and category-adjacent venues. Neither track bounds reality alone.

## Track A — Broad popularity-neutral survey (MUST run)

1. Query OSM/Overpass or an equivalent broad, unranked map/place index across the entire catchment using the category reference's tags.
2. Retain full tags and source metadata, not only name and category.
3. Include category-adjacent tags from the category reference so specialists are not erased by directory classification.
4. Partition large markets by non-overlapping neighborhoods or tiles when needed, then union every partition.
5. If the broad source is unavailable, use at least one alternate broad directory or systematic category sweep, log the failure, and state the limitation. Never rename the fallback a census.

## Track B — Adaptive targeted discovery (MUST run)

1. Identify locally used languages, scripts, and terminology from local sources. Do not mechanically translate an English checklist where local usage differs.
2. Generate and run locally natural query families for:
   - best, top, award, guide, and editorial recognition;
   - scratch, house-made, and production from raw components;
   - ambitious, chef-led, baker-led, artisan, seasonal, and technical craft;
   - every relevant neighborhood or sub-area;
   - locally important cuisines, bakery traditions, and service formats;
   - specialists, marker items, and production techniques from the category reference;
   - recent openings, new or renamed venues, relocations, pop-ups, markets, cottage/preorder, and informal formats where locally relevant.
3. Include local-language and local-script queries whenever those languages or scripts matter in the market.
4. Record exact queries and result sources. Search rank and “best” inclusion create candidates only; they never qualify a venue.

## Track C — Visible-head challenge (MUST run)

Check the market's reputable local food publications, major place-directory results, relevant guides and awards, local roundups, and recent-opening coverage. Add every in-scope venue not already present. This track prevents omission of a widely known venue that broad map data missed.

## Candidate handling

- Add every in-scope lead to the candidate ledger as `candidate-discovered`.
- Preserve track, source URL, exact query, identity and address as shown, and local-script spelling.
- Do not chain-strip, disqualify, score, or infer scratch during discovery.
- Follow the category reference's category-hygiene rule while keeping category-adjacent leads discoverable.

## Completion gate

- [ ] Track A covered the declared catchment or its precise fallback limitation is recorded.
- [ ] Track B ran every universal query family with locally generated terms.
- [ ] Relevant local languages/scripts were used or their non-use is explained.
- [ ] Track C checked visible-head and recent-opening sources.
- [ ] Category-specific marker and specialist queries from the discovery reference ran.
- [ ] Every in-scope result entered the ledger with source and query provenance.
- [ ] Counts by track are reported; no qualification or scoring occurred.
