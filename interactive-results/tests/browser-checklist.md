# Interactive Results Browser Validation

Generate bakery and restaurant fixture sites with a fixed `--generated-at`, then serve the parent directory using `python3 -m http.server 8765 --directory <dir>`.

## Desktop — 1440×900

- Fail on any `pageerror` or console error.
- Assert Practical, Audit, result, mapped, and saved counts.
- Exercise text search, every facet value, OR within one facet, AND across facets, alternate-facet counts, rating floor, all sort modes, reset, and empty state.
- Add/remove a shortlist item, reload, confirm persistence, and exercise saved-only mode.
- Select a card and assert marker/popup selection; activate `Show card` and assert card focus and visible center-pane bounds.
- Scroll `#results`; assert its `scrollTop` changes while `window.scrollY`, `#map-panel` top, and map height remain unchanged.
- Capture and inspect a screenshot for overlap, clipping, illegible controls, and clear Practical/Audit distinction.

## Mobile — 390×844

- Assert results are the default and separate Filters and Map buttons are visible.
- Exercise the facet drawer, backdrop, Escape close, focus restoration, map overlay, and Back to list.
- Activate popup `Show card`; assert overlay closes and matching card is selected, visible, and focused.
- Repeat search, shortlist, mode switch, empty state, and screenshot inspection.

## No-coordinate fixture

- Generate a variant with all Practical coordinates null and mapped count zero.
- Assert `body.list-only`, no map control/pane exposure, and functional results/filtering.

Record viewport assertions, screenshot paths, expected/observed counts, page-error results, and final status in `interactive-results-validation.json`.
