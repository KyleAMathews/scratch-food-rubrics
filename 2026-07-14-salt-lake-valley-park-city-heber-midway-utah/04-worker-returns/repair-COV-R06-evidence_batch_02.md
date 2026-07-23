## COV-013 — Feldman's Deli

- `repair_scope`: `rating/google_direct_place` only. Every other field in the prior COV-013 return remains unchanged.
- `access_date`: 2026-07-16.
- `terminal_direct_place_state`: `exact-rated`.
- `direct_place_object`:
  - Returned name: `Feldman's Deli`.
  - Returned address: `2005 E 2700 S, Salt Lake City, UT 84109`.
  - Returned phone: `(801) 906-0369`.
  - Returned category: `Deli`.
  - Returned storefront identity: `Floor 1 · Millcreek Corners`.
  - Literal rating: `4.7` (`aria-label="4.7 stars"`).
  - Literal review count: `count-unavailable`; Google Maps’ directly rendered limited-view place object did not expose a review-count value.
  - Stable Google identifier: CID `6572009753018553191`.
  - Stable direct URL: https://www.google.com/maps?cid=6572009753018553191.

### Required direct-place queries

1. `exact canonical name`
   - Exact query: `Feldman's Deli`.
   - Direct query URL: https://www.google.com/maps/search/?api=1&query=Feldman%27s%20Deli.
   - Returned name/address/phone/category/storefront: `Feldman's Deli`; `2005 E 2700 S, Salt Lake City, UT 84109`; `(801) 906-0369`; `Deli`; `Floor 1 · Millcreek Corners`.
   - Literal rating: `4.7`.
   - Literal count: `count-unavailable` in the directly rendered place object.
   - Stable Google identifier: CID `6572009753018553191`.
   - Rejected mismatches: none returned; the query opened the single exact-address place object above.
   - Accessed 2026-07-16.

2. `canonical name + exact address`
   - Exact query: `Feldman's Deli, 2005 E 2700 S, Salt Lake City, UT 84109`.
   - Direct query URL: https://www.google.com/maps/search/?api=1&query=Feldman%27s%20Deli%2C%202005%20E%202700%20S%2C%20Salt%20Lake%20City%2C%20UT%2084109.
   - Returned name/address/phone/category/storefront: `Feldman's Deli`; `2005 E 2700 S, Salt Lake City, UT 84109`; `(801) 906-0369`; `Deli`; `Floor 1 · Millcreek Corners`.
   - Literal rating: `4.7`.
   - Literal count: `count-unavailable` in the directly rendered place object.
   - Stable Google identifier: CID `6572009753018553191`.
   - Rejected mismatches: none returned; the query opened the same exact-address place object.
   - Accessed 2026-07-16.

3. `verified alias + phone`
   - Exact query: `Feldmans Deli, 801-906-0369`.
   - Direct query URL: https://www.google.com/maps/search/?api=1&query=Feldmans%20Deli%2C%20801-906-0369.
   - Returned name/address/phone/category/storefront: `Feldman's Deli`; `2005 E 2700 S, Salt Lake City, UT 84109`; `(801) 906-0369`; `Deli`; `Floor 1 · Millcreek Corners`.
   - Literal rating: `4.7`.
   - Literal count: `count-unavailable` in the directly rendered place object.
   - Stable Google identifier: CID `6572009753018553191`.
   - Rejected mismatches: none returned; the query opened the same exact-address place object.
   - Accessed 2026-07-16.

- `replacement_for_prior_google_line`: Google Maps direct place — terminal state `exact-rated`; exact returned identity `Feldman's Deli | 2005 E 2700 S, Salt Lake City, UT 84109 | (801) 906-0369 | Deli | Floor 1 · Millcreek Corners`; literal rating `4.7`; literal count `count-unavailable`; stable Google CID `6572009753018553191`; direct URL https://www.google.com/maps?cid=6572009753018553191; accessed 2026-07-16. The earlier Wanderlog Google-attributed value is preserved only in its existing aggregator field and is not used for this direct-place result.
