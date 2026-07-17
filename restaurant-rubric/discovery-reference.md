# Restaurant Discovery Reference

**Read this file in full during Phases 2 and 7. It finds candidates; it never qualifies or scores them.**

## Broad-survey category coverage

Survey restaurant, café, and fast-food tags and, where locally relevant, food-serving pubs and bars, inns, market stalls, food halls, pop-ups, and informal or preorder operations. Retain full tags. Service format is orthogonal to scratch: counter, takeaway, delivery, lunch-only, and rural-inn formats stay discoverable. Route a primary bakery-café to the bakery skill; a restaurant that bakes bread remains a restaurant.

## Executable broad-survey template

Use the Phase 1 polygon or box; never silently substitute a smaller boundary. With a bounding box:

```bash
BBOX="south,west,north,east"
Q='[out:json][timeout:120];nwr["amenity"~"^(restaurant|cafe|fast_food|pub|bar)$"]('"$BBOX"');out center tags;'
for ep in https://overpass-api.de/api/interpreter https://overpass.kumi.systems/api/interpreter https://overpass.osm.ch/api/interpreter; do
  curl -sS --max-time 120 -A "scratch-food-rubrics/8.11 (research)" "$ep" --data-urlencode "data=$Q" -o restaurant-candidates.json
  python3 -c 'import json; json.load(open("restaurant-candidates.json"))' 2>/dev/null && break
done
```

For an administrative polygon, replace `($BBOX)` with `(area.a)` after the Phase 1 `map_to_area->.a` statement. Verify valid JSON and record the returned element count. Pubs and bars are candidates only when food service is plausible; retain their full tags and resolve them from positive evidence rather than tag absence. Add locally relevant market, stall, food-hall, or other sources outside OSM as required.

## Adaptive targeted families

Generate locally natural, local-language and local-script variants for restaurant, scratch, house-made, production from raw ingredients, chef-owned or chef-led, seasonal or daily-changing, farm-to-table and local sourcing, tasting menu, ambitious or creative cooking, best/top/award/guide, rare regional cuisine, recent opening, local techniques and formats, and serious traditional cooking. Combine them with every sub-area. This English list seeds concepts; it is not a literal universal query list.

## Marker-item seed search (likelihood-ratio method)

A complementary way to *find* candidates (the rubric *ranks* them). The scorecard estimates P(scratch | venue features); a marker search estimates P(scratch | serves item X). Pick items X with no viable industrial/frozen substitute and the posterior → 1 by construction:

P(scratch | X) = P(X | scratch) / [P(X | scratch) + P(X | ¬scratch)·prior-odds(¬scratch)]

Even at low recall (P(X|scratch) small — few scratch places serve soufflé), P(X | ¬scratch) → 0 (a reheat kitchen *cannot* produce it), so the ratio → 1. **High precision, low recall — a seeding strategy, not a scoring one.** Blind spot: misses scratch places whose menu lacks a marker; use to seed the candidate set, never to bound it.

**Three physical mechanisms that make a food frozen-incompatible:**
1. **Ice-crystal rupture** — slow commercial freezing through the −1 to −5°C (30–23°F) zone grows extracellular crystals → ~5–15% drip loss + texture collapse on thaw. Kills custards, foams, fresh cheese, delicate crumb.
2. **Starch retrogradation** — amylopectin recrystallizes fastest at ~4°C (39°F), so refrigeration *accelerates* staling; gives fresh bread/tortilla/pasta an hours-long window no thaw-hold chain can serve.
3. **Emulsion/foam thermal fragility** — hollandaise stable only ~52–63°C (126–145°F); breaks on freeze/thaw, must be built minutes before service.

**Marker items ranked by P(scratch | serves it)** — *these are category-3 personal priors, ±0.1, ordinal not measured:*

| Marker | Mechanism | P(scratch) |
|---|---|--:|
| Soufflé | foam collapse ~2–5 min | ~0.98 |
| Hollandaise/béarnaise to order | emulsion window | ~0.92 |
| House-pulled mozzarella/burrata | casein peak in hours | ~0.90 |
| House charcuterie / pâté en croûte / terrine | no supply exists | ~0.88 |
| Real multi-day mole | 20–30 components | ~0.85 |
| Fresh tempura | crust window <5 min | ~0.85 |
| Plated-to-order composed dessert | assembly + custard | ~0.83 |
| Naturally-leavened open-crumb sourdough | fermentation + crumb | ~0.82 |
| Nixtamalized masa / fresh-pressed tortilla | retrogradation | ~0.80 |
| Fresh rolled/extruded egg pasta | ice damage + texture | ~0.78 |

**Cuisine-indexed markers** (best 2–3 per cuisine — doubles as a way to find scratch *within a target cuisine*):
- **French:** soufflé, hollandaise to order, canelé, pâté en croûte
- **Italian:** house mozzarella/burrata, fresh egg pasta, multi-hour ragù
- **Mexican:** nixtamalized masa / tortilla pressed to order, multi-day mole, tlacoyos/sopes
- **Greek/Mediterranean:** house-made phyllo (~0.9 — almost nobody sheets their own; commercial is universal), pita puffed to order, house spanakopita
- **Japanese:** fresh tempura, house dashi, hand-cut soba
- **Chinese:** hand-pulled/hand-cut noodles, xiao long bao (hand-folded), dry-fried wings
- **New American:** plated-to-order composed dessert, house charcuterie, whole-animal butchery

**Anti-markers (LR < 1 — presence is neutral-to-negative, these *are* the frozen regime):** molten lava cake, cheesecake wedge, crème brûlée (Sysco sells a gelatin-set frozen version → weak marker, P~0.5), calamari rings, mozzarella sticks, "crispy chicken," wings, generic dinner rolls. Croissants ambiguous (Bridor par-bake, P~0.45) unless lamination verified.

**As search queries:** the *item* is the filter — `soufflé [city]`, `house-pulled mozzarella [city]`, `nixtamal masa tortillas [city]`, `pâté en croûte [city]`, `eggs benedict scratch hollandaise [city]`.

---

## Known-example challenges

- A widely recognized ambitious scratch restaurant absent from OSM must enter through targeted quality and scratch sources.
- Counter, takeaway, and lunch-only formats never exclude without production evidence.
- Local-language discovery must be able to add a venue that English queries missed.
- A broad menu is judged only from opened production evidence and the unchanged K/coherence rubric.
