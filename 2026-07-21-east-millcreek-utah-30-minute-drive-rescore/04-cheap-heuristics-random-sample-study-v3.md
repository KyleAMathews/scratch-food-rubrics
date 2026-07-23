# Cheap-heuristics study: third random sample of 20

Date: 2026-07-15

This reproducible sample was drawn from the 1,644-candidate post-clustering population and excludes the first 40 sampled records. Root researched it directly.

## Results

| ID | Venue | Cheap finding | Implication |
|---|---|---|---|
| R-2213 | Lone Star Taqueria | Family-held single-location taqueria since 1994; official site describes daily fish, long-tenured staff, pressed tortillas, and house salsa. | Advance; a compact configurable menu is not standardized-chain evidence. |
| R-0367 | Amelia's Grill & Bar | Public restaurant inside an airport-area hotel, advertising homemade American food. | Retain unresolved; hotel co-location does not imply restricted access or no kitchen. |
| R-0373 | Este Pizza | Candidate domain is stale/problematic and current operating status is unclear; search results include closure discussion. | Current-operation/domain repair before evidence. Do not attach similarly named out-of-state menu evidence. |
| R-0952 | Leprechaun Inn | Local bar with food references, but exact current food substance was not established cheaply. | Food-substance repair queue; bar tag alone cannot decide. |
| R-2923 | 'Mina | New Sicilian restaurant with handmade pasta, house bread, and gelato. | Immediate advance on direct production evidence. |
| R-0293 | Butcher's Chop House | Current locally owned Park City steakhouse with a public dining room. | Retain; local restaurant-group membership is not exclusion evidence. |
| R-0676 | Sala Thai Kitchen | Exact current independent Thai restaurant and ordering menu. | Retain unresolved. Generic ordering prose is not production evidence. |
| R-1984 | Caracas Dog | Exact coordinates/menu resolve to the Woodbine Venezuelan hot-dog concept; current branding appears to be Caracas Grill at the same address. | Identity/rebrand repair. Fuzzy matching cannot compare against a name absent from the candidate union. |
| R-0285 | Gracie's | Current downtown bar with an extensive substantive food menu. | Retain; positive food menu defeats a bar-format shortcut. |
| R-0849 | SLABpizza | Lehi record has conflicting current-operation signals; reporting says other branches closed. | Current-operation repair; only positive closure evidence may remove it. |
| R-2763 | Casa Frida Mexican Grill | New single-location West Valley restaurant with chicken, tacos, burritos, and catering. | Retain unresolved; drive-through/fast-food tagging is uninformative. |
| R-1729 | Fratelli Ristorante | Family-owned; official site explicitly documents scratch food and house-made gelato. | Immediate advance. |
| R-2481 | Unnamed OSM food-service element | No restaurant identity exists in the record; it was already part of an unresolved unnamed-geometry pair. | Quarantine for spatial identity repair before evidence batching. |
| R-0348 | Hi Sushi | Exact current local sushi menu/listing, but no cheap production evidence. | Retain unresolved. |
| R-2900 | Makam's Indian Restaurant | Current Millcreek restaurant; official site says prepared-to-order bowls, wraps, plates, breads, and salads. | Retain; fast-casual assembly structure coexists with fresh preparation claims. |
| R-0152 | Spice Bistro | Current state license evidence at the exact address; Indian-American bistro identity. | Retain unresolved; older editorial material is useful discovery context, not current proof. |
| R-0012 | El Chubasco | Current single-location Park City Mexican restaurant with a large salsa bar and fresh-menu claims. | Retain unresolved; counter service is not a negative signal. |
| R-1731 | Sukiya Sushi & Japanese Buffet | Two-location Utah concept; official site describes chef-led sushi, made-to-order rolls, and frequent imported seafood shipments. | Advance; buffet and multi-location formats can contain high production/ingredient ambition. |
| R-0009 | All Chay | Family-owned vegan Vietnamese restaurant. Candidate domain is an unaffiliated SEO/menu domain rather than a trustworthy official source. | Retain, but repair source provenance. |
| R-1483 | V Burger | Single-location Venezuelan restaurant with current official identity and made-to-order food. | Retain; “burger” and fast format remain unsafe proxies. |

Representative sources: [Lone Star](https://lstaq.com/), ['Mina](https://www.minaslc.com/), [Butcher's Chop House](https://www.butcherschophouse.com/), [Gracie's menu](https://www.graciesslc.com/menu?menu=lunch--dinner), [Fratelli](https://fratelliutah.com/about-us), [Makam's](https://makamsindianrestaurant.com/), [El Chubasco](https://elchubascoparkcity.com/menu), [Sukiya](https://sukiyautslc.net/), and [V Burger](https://vburgerutah.com/).

## Findings after 60 sampled restaurants

This sample found **zero safe broad-format or chain exclusions**. It found no new duplicate among two surviving candidate rows, so it does not expose a failure in the reviewed fuzzy clustering. It did expose three cheaper data-quality problems:

1. **Unresolved unnamed geometries.** An unnamed OSM object is a lead, not a restaurant identity. It should be spatially joined to nearby named records and current map/address sources before entering an evidence batch. If still unresolved, quarantine it outside the packet count rather than ask a worker to research an object ID.
2. **Unvalidated domains.** Candidate URLs may be stale, unrelated, redirected, or third-party SEO sites. Before treating a URL as official, code can fetch its title/canonical host and compare the venue name, address, or phone. A mismatch discards the URL as official provenance and triggers exact identity search.
3. **Current-operation uncertainty.** Este Pizza and SLABpizza illustrate records where cheap signals conflict. These belong in the existing identity/current-operation repair queue. Missing ordering or social activity is not closure; removal still requires positive evidence.

Caracas Dog also reveals a boundary of fuzzy deduplication: algorithms can cluster only records already present. Current-name lookup can discover a rebrand even when the new name is absent from the union.

## Recommended codeful addition

Add a pre-evidence **identity readiness validator** with machine-checkable fields:

- non-placeholder name;
- usable coordinates or exact address;
- validated domain provenance, if a domain is present;
- current-name/address consistency; and
- `ready`, `repair`, or `quarantine` state.

Only `ready` identities consume evidence-worker tokens. `repair` records receive a bounded identity search; unresolved unnamed geometries enter `quarantine` and remain auditable. This is workload control through data correctness, not a prediction about restaurant quality.
