## COV-013 — Feldman's Deli

- `access_date`: 2026-07-16.
- `candidate_input`: Feldman's Deli; 2005 E 2700 S, Salt Lake City, UT 84109; 801-906-0369; https://www.feldmansdeli.com/.

### Identity

- `canonical_name`: Feldman’s Deli.
- `observed_aliases`: “Feldman's Deli” (ASCII apostrophe); “Feldman’s”; “Feldman's.”
- `address`: 2005 E 2700 S, Salt Lake City, UT 84109. Apple Maps adds `Ste D`; Time Out and the Utah state license list omit the suite.
- `phone`: (801) 906-0369.
- `official_domain`: https://www.feldmansdeli.com/.
- `branch_or_storefront`: named storefront at the supplied address. No second location is presented on the official contact page.
- `category`: official site says New York-style delicatessen; Time Out says kosher-style Jewish delicatessen; Apple Maps categorizes it as `Deli`; Restaurantji lists `Deli, Bagels`.
- `storefront_status`: official site offers dining in and taking out; the archived Salt Lake Tribune description calls it a full-service restaurant with a dining room; current directory records also expose takeaway and outdoor seating.

### Identity sources

- [Official home](https://www.feldmansdeli.com/) — exact canonical business, official domain, deli description, current `ORDER NOW` control, dine-in/takeout wording; crawled/accessed 2026-07-16.
- [Official contact](https://www.feldmansdeli.com/pages/contact) — “2005 E 2700 S, SLC UT 84109” and “(801) 906-0369”; accessed 2026-07-16.
- [Apple Maps](https://maps.apple.com/place?place-id=IA81FEF9BBB0A71D1) — exact name, 2005 E 2700 S Ste D, phone, domain, deli category, and stable Apple place ID `IA81FEF9BBB0A71D1`; accessed 2026-07-16.
- [Utah ABC Licensee List](https://opendata.utah.gov/api/views/8q4k-thaj/rows.pdf?app_token=U29jcmF0YS0td2VraWNrYXNz0) — report dated 2026-06-30; record `RB00266 FELDMAN'S DELI`, exact address and phone at PDF pp. 87–88; accessed 2026-07-16.
- [Time Out](https://www.timeout.com/usa/restaurants/best-restaurants-in-salt-lake-city) — exact name, address, category, second-generation operator, and hours; published approximately March 2026, accessed 2026-07-16.

### Rating evidence and direct-platform gates

Identity tuple used for every platform query: `Feldman’s Deli | 2005 E 2700 S [Ste D], Salt Lake City, UT 84109 | (801) 906-0369 | feldmansdeli.com | deli/Jewish restaurant/bagels | named storefront`.

- `Google Maps` — terminal state: `exact-rated` via an accessible Google-attributed listing reproduction. [Wanderlog](https://wanderlog.com/place/details/427832/feldmans-deli) returned the complete identity tuple and displayed `Google 4.7 (2,239)`. Stable source path ID: `427832`; a Google place ID was not exposed. Exact query: `"Feldman's Deli" "2005 E 2700 S" Google rating`. Accessed 2026-07-16.
- `Yelp` — terminal state: `exact-rated`. [Apple Maps](https://maps.apple.com/place?place-id=IA81FEF9BBB0A71D1) returned the complete identity tuple and Yelp `4.5 (883)`. Stable Apple listing ID: `IA81FEF9BBB0A71D1`; a Yelp business ID was not exposed there. Exact query: `"Feldman's Deli" "2005 E 2700 S" Yelp`. Accessed 2026-07-16.
- `Tripadvisor` — terminal state: `exact-rated`. [Direct Tripadvisor restaurant record](https://www.tripadvisor.com/Restaurant_Review-g60922-d3761576-Reviews-Feldman_s_Deli-Salt_Lake_City_Utah.html) returned exact name, address, phone/category and `4.5 (200 reviews)`. Stable page ID: `d3761576`. Exact query: `site:tripadvisor.com/Restaurant_Review-g60922-d3761576 Feldman's Deli rating reviews`. Accessed 2026-07-16.
- `Facebook` — terminal state: `no-exact-record`. Exact queries `site:facebook.com Feldman's Deli Salt Lake City 2005 E 2700 S reviews` and `site:facebook.com/feldmansdeli bagels Feldman's Deli` did not expose an exact-address record. Same-name results for Feldman’s Bagels in Vermont and Feldman’s Ice Cream in Israel were rejected as identity mismatches. Accessed 2026-07-16.
- `Restaurantji` — terminal state: `exact-rated`. [Restaurantji](https://www.restaurantji.com/ut/salt-lake-city/feldmans-deli-/) returned exact name/address/phone, `4.6 (606 ratings)`, and `Updated Jun 10, 2026`; stable URL slug `/ut/salt-lake-city/feldmans-deli-/`. Exact query: `Feldman's Deli 2005 E 2700 S exact rating count Restaurantji`. Accessed 2026-07-16.
- `additional reconciliation`: [MapQuest](https://www.mapquest.com/us/utah/feldmans-deli-284015956) returned the exact identity tuple and Yelp `4.5 (877)`, a count six below Apple Maps’ Yelp-fed display. [Restaurant Guru](https://restaurantguru.com/Feldmans-Deli-Salt-Lake-City), updated 2026-03-15, displays Google `4.7/5 (2,157)`, Tripadvisor `4.5/5 (198)`, and Facebook `4.8/5 (604)`. These differing snapshots remain separate rather than merged.

### Prices

- [Restaurant Guru](https://restaurantguru.com/Feldmans-Deli-Salt-Lake-City), updated 2026-03-15, displays the restaurant-level literal `Price range per person $10–$20`.
- The same page reproduces a Google reviewer’s reported `Price per person: $20–30` for a lunch visit. Both values were accessed 2026-07-16 and are preserved as differently scoped statements.
- [Salt Lake Tribune’s 2013 review](https://archive.sltrib.com/article.php?id=56215867&itype=cmsid) printed historical item prices including a $2.50 bagel, $4 potato pancakes, and $11.50 pastrami; the page itself warns that archived information may be outdated. These are not presented as current prices.

### Hours, cadence, and access format

- Current hours: Tuesday–Saturday 8 a.m.–8 p.m.; Sunday–Monday closed. This schedule appears in [Time Out](https://www.timeout.com/usa/restaurants/best-restaurants-in-salt-lake-city), [Apple Maps](https://maps.apple.com/place?place-id=IA81FEF9BBB0A71D1), and [Restaurant Guru](https://restaurantguru.com/Feldmans-Deli-Salt-Lake-City), all accessed 2026-07-16.
- Current bagel cadence: a May 2025 [Utah Stories profile](https://utahstories.com/2025/05/feldmans-deli-salt-lake-new-generation/) reports that John is the primary bagel maker, “hand-rolling and baking 2 dozen each day and 42 bagels on Saturdays.”
- Current limited-volume wording: [Time Out](https://www.timeout.com/usa/restaurants/best-restaurants-in-salt-lake-city) says breakfast has “a limited number of hand-rolled bagels.”
- Historical sell-out record: [KSL](https://www.ksl.com/article/25831885/feldmans-deli), 2013, says the deli then made two or three dozen daily and usually sold out. [Utah Stories](https://utahstories.com/2013/07/feldmans-deli/) similarly records “when they’re gone they’re gone.”
- Access formats: dining room/full service, takeout, online-order entry point, outdoor seating, and phone preorders/reservations for specified holiday events. Sources: official home; Restaurant Guru; archived Tribune; [official holiday page](https://www.feldmansdeli.com/pages/rosh-hashana-and-yom-kippur). No general shipping or farmers-market format was retrieved.

### Current acquisition and operating evidence

- Official home displayed `ORDER NOW`, `SEE MENU`, gift cards, rewards, and “Whether dining in or taking out” on the access date.
- Official holiday page directs customers to call `(801) 906-0369` for events requiring preorder or reservations.
- Utah’s 2026-06-30 ABC licensee list retains the exact business/address/phone record.
- Restaurantji’s exact record was updated 2026-06-10; Restaurant Guru’s exact record was updated 2026-03-15; Time Out’s approximately March 2026 guide supplies the current schedule.
- [Utah Stories’ May 2025 profile](https://utahstories.com/2025/05/feldmans-deli-salt-lake-new-generation/) reports son John handling day-to-day operations since May 2023 as part owner/general manager.

### Product quotations — product-only

- Official home: “Pastrami, Corned Beef, and Reubens” — `product-only`.
- Official home: “Matzo Ball Soup, Smoked Whitefish Salad, and fresh-baked bagels” — `product-only` for named offerings; `fresh-baked` is also separately retained as a production claim.
- [Official gallery](https://www.feldmansdeli.com/pages/gallery): “Bagel with Lox and Cream Cheese” — `product-only`.
- Official gallery: “Breakfast Bagel Sandwich” — `product-only`.
- Official gallery: “Assorted Bagels” — `product-only`.
- Official gallery: “Raspberry Croissant” — `product-only`.
- Official gallery: “Homemade Carrot Cake” — `product-only`; `Homemade` is literal menu naming, not an inferred production finding.
- Official gallery: “Babka” — `product-only`.

### Explicit process evidence

- Official home calls the bagels “fresh-baked.”
- [Utah Stories, 2013](https://utahstories.com/2013/07/feldmans-deli/): bagels were “Boiled first and then baked”; the article states Janet made them at the deli.
- [Utah Stories, May 2025](https://utahstories.com/2025/05/feldmans-deli-salt-lake-new-generation/): John is reported hand-rolling and baking the stated daily quantities.
- [SLUG Magazine](https://www.slugmag.com/community/food/food-reviews/feldmans-deli-a-chagigah-to-the-big-beehive/): the reviewed onion bagel had been “boiled then baked that morning.”
- [ThoughtLab](https://www.thoughtlab.com/blog/a-field-day-at-feldmans/), 2013: the owners discussed experimentation with yeast amount, temperature, salinity, kneading, and cooking while developing the bagel process for Utah conditions.
- [Salt Lake Tribune, 2013](https://archive.sltrib.com/article.php?id=56215867&itype=cmsid): the critic received the last of the day’s freshly boiled and baked bagels; the article also states standard items could run out.

### Ingredient and sourcing evidence

- [Utah Stories, 2013](https://utahstories.com/2013/07/feldmans-deli/): the owners were reported to ship in meat and desserts from a New York deli; mustard and pickles were also shipped in when unavailable locally. The same profile says, “What they don’t ship in is made from scratch at the deli,” naming brisket and golumpki as examples.
- That profile identifies Stone Ground Bakery as the maker of the deli’s rye bread.
- [Salt Lake Tribune, 2013](https://archive.sltrib.com/article.php?id=56215867&itype=cmsid): meat was imported from “back East”; the exact supplier was described as semi-secret.
- [Forbes, 2024](https://www.forbes.com/sites/garystern/2024/11/14/kosher-style-feldmans-deli-thrives-in-salt-lake-city/) reports that the food is kosher-style rather than kosher and says no kosher butchers or bakers operate in the area.
- No named flour, flour mill, malt, starter, or current bagel-dough ingredient list was retrieved.

### Review text and physical product evidence

- [SLUG Magazine](https://www.slugmag.com/community/food/food-reviews/feldmans-deli-a-chagigah-to-the-big-beehive/): the bagel showed “just enough surface tension, without sacrificing tenderness” and was “steaming from unmatched freshness.”
- [Utah Stories, 2013](https://utahstories.com/2013/07/feldmans-deli/): the boiled-and-baked bagels were described as fluffy inside and crisp outside.
- [Restaurant Guru](https://restaurantguru.com/Feldmans-Deli-Salt-Lake-City) reproduces a Google review calling the fresh-cut fries a favorite while saying the matzo-ball-soup “broth lacks flavor.”
- [Salt Lake Tribune, 2013](https://archive.sltrib.com/article.php?id=56215867&itype=cmsid) described the rye as light and understated and the bagel as having a crisp exterior and lightly chewy interior.

### Adverse or disconfirming facts

- The 2013 Utah Stories sourcing account states that meat, desserts, mustard, and pickles were shipped in; it also names Stone Ground Bakery as the rye-bread producer.
- The 2013 Tribune independently says meat was imported from back East and the supplier was not disclosed.
- The Forbes profile states the operation is kosher-style, not kosher.
- Restaurant Guru’s reproduced review says the matzo-ball-soup broth lacked flavor and mentions one staff member as cold/unwelcoming; it also reports parking as somewhat difficult.
- No verified closure, food-safety enforcement, frozen-product allegation, or commissary-production allegation specific to this storefront was retrieved.

### Neutral facts retained without inference

- Michael and Janet Feldman founded the deli; 2025 Utah Stories and 2026 Time Out report second-generation operation by their son John.
- Official site calls the sandwiches half-pound and sliced fresh to order.
- Time Out says the Sloppy Joe uses three rye layers with corned beef, pastrami, and coleslaw.
- Utah Stories reports bagel quantities of 24 on ordinary production days and 42 Saturdays as of May 2025.
- The official gallery displays soups, sandwiches, entrees, and small bites in addition to bagels.
- Official site supports both dine-in and takeout acquisition.

### Full search trail

1. `official site/menu/contact/order`: opened the official home, `/pages/contact`, `/pages/menu`, `/pages/gallery`, and `/pages/rosh-hashana-and-yom-kippur`; verified the exact tuple, menu/product text, `ORDER NOW`, takeout, and holiday preorder instruction.
2. `official social`: inspected the Instagram embed/link on the official home and ran exact Instagram/Facebook searches. No accessible, date-stamped official bagel post with additional production facts was returned.
3. `review and platform records`: opened Apple Maps/Yelp, MapQuest/Yelp, Wanderlog/Google, direct Tripadvisor, Restaurantji, Restaurant Guru, Food96, Corner, and USA Restaurants; exact-address records were retained, while mismatched same-name businesses were rejected.
4. `local press/interviews`: opened Utah Stories (2013, 2020 takeout, and May 2025 succession profile), archived Salt Lake Tribune (2013 deli review and 2021 bagel poll), SLUG Magazine, KSL, ThoughtLab, Salt & Seek, Forbes, and Time Out.
5. `regulatory/current-operation verification`: opened Utah’s current ABC Licensee List and the 2024 on-premises retail-license list; retained the 2026-06-30 exact record as the freshest state evidence.

Exact queries run:

- `site:feldmansdeli.com Feldman's Deli menu about bagels hours`
- `Feldman's Deli 2005 E 2700 S Salt Lake City rating reviews`
- `Feldman's Deli bagels made daily sold out morning Salt Lake`
- `Feldman's Deli interview bagels dough made in house Salt Lake Tribune Utah Stories`
- `"Feldman's Deli" "2005 E 2700 S" Google rating`
- `"Feldman's Deli" "2005 E 2700 S" Yelp`
- `"Feldman's" "801-906-0369" Tripadvisor`
- `site:feldmansdeli.com Feldman's Deli contact hours place order`
- `site:tripadvisor.com/Restaurant_Review-g60922-d3761576 Feldman's Deli rating reviews`
- `site:facebook.com Feldman's Deli Salt Lake City 2005 E 2700 S reviews`
- `Feldman's Deli 2005 E 2700 S exact rating count Restaurantji`
- `Feldman's Deli bagel reviews chewy crispy sold out fresh batch`
- `site:instagram.com/feldmansdeli bagels Feldman's Deli`
- `site:facebook.com/feldmansdeli bagels Feldman's Deli`
- `Feldman's Deli Instagram bagels daily 2026`
- `site:feldmansdeli.com/pages/order Feldman's Deli order online`
- `site:timeout.com Feldman's Deli Salt Lake City bagels`
- `site:feldmansdeli.com "ORDER NOW" "Feldman's Deli"`
- `"Feldman's Deli" "Price per person" Salt Lake City`
- `"Feldman's Deli" fermentation bagel dough flour starter`

Opened-source dispositions:

- `retained`: official home/contact/menu/gallery/holiday pages; Apple Maps; MapQuest; Wanderlog; direct Tripadvisor; Restaurantji; Restaurant Guru; Utah ABC license list; Time Out; Utah Stories 2013/2020/2025; Tribune 2013/2021; SLUG; KSL; ThoughtLab; Forbes; Salt & Seek.
- `corroborative but not used for a unique finding`: Corner, USA Restaurants, Food96, the 2024 Utah license PDF.
- `rejected identity mismatches`: Feldman’s Bagels in Vermont; Feldman’s Ice Cream in Israel; older Nevada results for Eileen and Larry Feldman’s Bagel Deli.

### Exhausted-unavailable fields

After the official-site/menu/contact stage, official-social stage, review/direct-platform stage, local-press/interview stage, and regulatory/current-operation stage:

- Current itemized official prices beyond the third-party restaurant-level ranges: `exhausted-unavailable`.
- Named flour or mill, dough formula, malt, starter, proof duration, fermentation duration, and retardation schedule: `exhausted-unavailable`.
- Current first-batch ready time, precise sell-out time, preorder cutoff, and pickup window: `exhausted-unavailable`.
- General shipping, wholesale, farmers-market, or pop-up acquisition: `exhausted-unavailable`.
- Exact Facebook address record from a direct accessible page: `exhausted-unavailable`; same-name false matches were rejected.
