# Bakery Discovery Reference

**Read this file in full during Phases 2 and 7. It finds candidates; it never qualifies or scores them.**

## Broad-survey category coverage

Survey bakery, pastry, and confectionery tags plus locally relevant adjacent categories such as café, chocolate shop, dessert shop, bread shop, tortillería, bagel shop, market stall, cottage/preorder bakery, and regional equivalents. Directory category never decides eligibility. Preserve full tags.

## Executable broad-survey template

Use the Phase 1 polygon or box; never silently substitute a smaller boundary. With a bounding box:

```bash
BBOX="south,west,north,east"
Q='[out:json][timeout:120];(nwr["shop"~"^(bakery|pastry|confectionery)$"]('"$BBOX"');nwr["cuisine"~"bakery|pastry|dessert",i]('"$BBOX"'););out center tags;'
for ep in https://overpass-api.de/api/interpreter https://overpass.kumi.systems/api/interpreter https://overpass.osm.ch/api/interpreter; do
  curl -sS --max-time 120 -A "scratch-food-rubrics/8.11 (research)" "$ep" --data-urlencode "data=$Q" -o bakery-candidates.json
  python3 -c 'import json; json.load(open("bakery-candidates.json"))' 2>/dev/null && break
done
```

For an administrative polygon, replace each `($BBOX)` selector with `(area.a)` after the Phase 1 `map_to_area->.a` statement. Verify valid JSON and record the returned element count. Expand the query with locally relevant adjacent tags rather than treating this minimal template as complete.

## Adaptive targeted families

Generate locally natural, local-language and local-script variants for bakery, bread, patisserie, boulangerie, viennoiserie, pastry, panadería, tortillería, bagel, laminated pastry, sourdough/natural leavening, house-made phyllo, chocolatier/bonbon production, gluten-free craft bakery, microbakery, baker-owned, artisan, scratch/from raw ingredients, best/top/award/guide, recent opening, and the market’s own traditions. Combine them with every sub-area. Explicitly expand filled-pastry and cultural-tradition synonym families when locally plausible—for example empanada, pastelito, kolache, burek, meat pie, hand pie, samosa, ensaymada, and pandesal—plus local-language and local-script equivalents. These are discovery terms, not automatic bakery eligibility. This English list seeds concepts; it is not a literal universal query list.

## Product × adjacent-format discovery

Cross locally relevant products and production terms with venue formats that may hide bakery work behind another primary identity. Adaptive examples include bagel × deli, pastry or pâtisserie × café, bread × restaurant, filled pastry × cultural market or grocer, and laminated goods × chocolatier. Run the locally natural and local-language equivalents rather than treating these examples as a fixed universal list. Record every in-scope identity as a discovery candidate; neither the product nor the adjacent format establishes bakery eligibility.

## Marker-item seed search (bakery)

Complement to the rubric: search for items with **no viable par-bake/frozen substitute**, so P(scratch | serves it) → 1 (see restaurant scorecard for the likelihood-ratio derivation). High precision, low recall — seeds candidates, doesn't bound them.

**Bakery marker items** (category-3 personal priors, ±0.1):

| Marker | Why frozen-incompatible | P(scratch) |
|---|---|--:|
| Canelé | copper molds + beeswax, same-day custard interior | ~0.90 |
| House-made phyllo | almost nobody sheets it; commercial is universal | ~0.90 |
| Kouign-amann (verified lamination) | caramelized laminated dough, hours-fresh | ~0.85 |
| Naturally-leavened open-crumb sourdough | par-bake can't fake irregular high-hydration crumb | ~0.82 |
| Fresh stroopwafel (pressed to order) | Dutch marker — batter griddled à la minute | ~0.88 |
| Laminated brioche / pain suisse | in-house butter block, not frozen sheet | ~0.80 |
| Paris-Brest / choux to order | craquelin choux + praline cream, no frozen version | ~0.80 |

**Anti-markers (P~0.4–0.5, these ARE the par-bake regime):** plain croissant with no lamination claim (Bridor), muffins from batter pails, generic bagels, cookie-dough-tub cookies, sheet-cake with piped roses, "brownies."

**As queries:** `canelé [city]`, `house-made phyllo [city]`, `kouign-amann [city]`, `naturally leavened sourdough [city]`, `stroopwafel fresh made [city]`, `Paris-Brest [city]`.

---

## Known-example challenges

- A category-adjacent chocolatier producing serious pastry or laminated goods must enter research.
- A menu listing croissants or viennoiserie without process evidence remains product-only and requires repair.
- A traditional bakery with sparse jargon receives review, local-press, and cadence research.
- An ethnic or single-item specialist is judged only on its applicable production evidence.
