# Post-run direct-place re-review — rating-unconfirmed bakeries

Re-review date: 2026-07-15; user-triggered exact-place correction: 2026-07-16. Primary orchestrator: `/root`.

## Why this re-review happened

The All Purpose correction showed that the original worker procedure treated ordinary web searches aimed at Maps as if they were direct place-record checks. The user asked for the same direct-place query to be run against every other scratch-verified bakery that had been left `rating-unconfirmed`.

## Reproducible retrieval algorithm

For each candidate:

1. Start from the accepted identity packet and collect the exact current name, address, phone, aliases, service-area status, and branch distinction.
2. Query the Google map-search surface with the exact name. If unresolved, retry exact name plus address, then a verified alias or phone/locality.
3. Inspect the returned place object itself. Record its displayed name, address or service-area state, category, rating, and stable place identifier.
4. Accept a rating only when the returned identity matches the candidate. Reject near-name results, host kitchens, former branches, and unrelated businesses even when they have ratings.
5. Record one of four literal outcomes: `exact-rated`, `exact-no-rating`, `no-exact-record`, or `identity-conflict`. Do not call a rating exhausted until these variants have been attempted.
6. If the direct record is absent, perform exact-identity secondary-platform searches. Preserve platform values separately; never average them.
7. Recheck current operating status independently. A rating record is not proof that a business remains open.

The endpoint used was Google's map-search response for `tbm=map`, with US English localization. Place identifiers below are the stable identifiers returned by that response. The response exposed star values but generally omitted review counts, so no count was invented.

## Results for all 20 formerly unconfirmed candidates

| ID | Candidate | Direct-place identity result | Literal rating result | Decision |
|---|---|---|---:|---|
| P3-008 | Le Pain de Charlie | exact bakery, 3758 S Maple Vw Dr; `0x2d080822b552a0eb:0x47e5e949e9a4ac2e` | 5.0 | promote to rated survivor |
| P3-038 | The Flour Box Bakery LLC | exact bakery, 7103 W 8090 S; `0x875291dd38eaa28f:0xbb8d760ac8097277` | 4.8 | promote to rated survivor |
| T-001 | Salt Lake Sourdough | no exact business record; the address query returned a different bakery | unavailable | retain visible, rating-unconfirmed |
| T-003 | Tomodachi Bake Shoppe | no exact business record after Salt Lake/Cottonwood Heights variants | unavailable | retain visible, rating-unconfirmed |
| T-010 | Doughlene Bakes SLC | exact bakery, 2220 E Murray Holladay Rd; `0x875263c6423da561:0x85082c446bbf5c37` | no rating displayed | retain visible, rating-unconfirmed |
| COV-003 | Hi Crunchy Utah | no exact business record; address/name variants returned an unrelated chicken restaurant | unavailable | retain visible, rating-unconfirmed |
| COV-012 | High Altitude Bakeshop | exact bakery, 751 W 800 S; `0x8752f5567d95acaf:0xd9583940c2a11b4a` | 2.3 | scored but filtered below rating gate |
| P3-041 | Sourdough Bruh | no exact business record after Herriman/name variants | unavailable | retain visible, rating-unconfirmed |
| T-002 | Mims Bakery | exact bakery service-area record; `0x8752899d417ab577:0xab57c7265c6a6d83` | 4.8 | promote to rated survivor |
| T-016 | AmsterDam Delicious | exact bakery service-area record; `0xcbb4e06fc7a34f:0x5d7e4ba49243d8da` | 5.0 | promote to rated survivor |
| P3-004 | Argentina's Café — Salt Lake branch | exact current place card reached by canonical name + `655 E 400 S`; user-provided screenshot confirms `Argentinas Cafe`, coffee-shop category, and current price band; distinct from the former `357 S 200 E` business | 4.5 (336) | promote to rated survivor; use the current-place value, not the rejected former-branch rating |
| P3-042 | Artisan Bakery Utah | no exact business record after exact-name and LLC variants | unavailable | retain visible, rating-unconfirmed |
| P3-028 | Mad Dough | no exact business record after exact-name and Central Ninth variants | unavailable | retain visible, rating-unconfirmed; verify current activity before ordering |
| A-117 | Great Harvest Bread Company — Draper | exact branch, 217 E 12300 S J5; `0x875287147861dd17:0xfa2acdc0c390038f` | 4.4 | promote to rated survivor |
| P3-003 | JD Flannel Donuts — Foothill | exact branch, 1400 S Foothill Dr #112; `0x87526153c5dde16d:0x6bbc320bfc8f91` | 4.9 | promote to rated survivor |
| T-019 | Nano's Bagels | exact shop, 668 E Union Square; `0x87528704f089b143:0xe42a3c763f973fd1` | 4.8 | promote to rated survivor |
| P3-033 | The Bakery at Zermatt Utah | no distinct direct place record after exact name/address variants | unavailable directly; exact current Restaurantji identity displays 4.3/117 | promote using current exact-identity secondary rating; [source](https://www.restaurantji.com/ut/midway/the-bakery-at-zermatt-utah-/) |
| A-040 | City Cakes & Cafe — Midvale | exact branch, 7009 High Tech Dr; `0x875287143e709139:0x9628619e221c92de` | 4.4 | promote to rated survivor |
| A-240 | Eats Bakery & Coffee | exact shop, 248 E 100 S; `0x8a7756486b53469d:0xbf93166f0f13c67b` | 4.7 | promote to rated survivor |
| P3-027 | Flourish Bakery | exact bakery, 752 W Center St; `0x8752892cce8d8fc5:0x2ee00ae9c3ffd95d` | 4.6 | defer: direct rating conflicts with a current exact-address `CLOSED` record; [status source](https://www.restaurantji.com/ut/midvale/flourish-bakery-/) |

## Disposition effect

Eleven candidates are promoted to rated survivors after the July 16 Argentina's Café correction. High Altitude Bakeshop moves to scored-but-filtered because its direct 2.3 rating is below the gate. Flourish Bakery moves to deferred status because a live rating record and a current closure record conflict. Seven remain visible and unranked because the direct-place procedure found no attributable rating.

This changes the 325-candidate disposition totals to **56 rated survivors, 7 scratch-verified/rating-unconfirmed, 8 scored-but-filtered, 40 positive-evidence DQs, 8 deferred, 10 evidence-exhausted, and 196 not-scoreable**.

Postscript: the separate 2026-07-16 Feldman's Deli coverage addition later changed the canonical population to 326 and the rated-survivor count to 57. See `04-worker-returns/batch-COV-B06-evidence_batch_02.md`, `04-worker-returns/repair-COV-R06-evidence_batch_02.md`, `05-evidence-ledger.md`, and `06-decisions.md`.
