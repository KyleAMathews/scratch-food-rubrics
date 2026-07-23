# frozen_string_literal: true

run_dir = File.expand_path(__dir__)
decisions = File.read(File.join(run_dir, "06-decisions.md"), encoding: "UTF-8")

scores = decisions.lines.map do |line|
  match = line.match(/^\| (R-\d+ .+?) \| scoreable([^|]*) \| `([0-9]+)\/([0-9]+)\/([0-9]+)\/([0-9]+)\/([0-9]+) = S([0-9]+(?:\.[0-9]+)?)`; `([0-9]+)\/([0-9]+)\/([0-9]+)\/([0-9]+)\/([0-9]+) = I([0-9]+(?:\.[0-9]+)?)`; `G([0-9]+(?:\.[0-9]+)?)`/)
  if match
    {
      name: match[1],
      note: match[2].strip,
      s: match[8].to_f,
      i: match[14].to_f,
      g: match[15].to_f
    }
  else
    calibrated = line.match(/^\| (R-\d+ .+?) \| scoreable([^|]*) \| (?:calibrated )?`S([0-9]+(?:\.[0-9]+)?)`; `I([0-9]+(?:\.[0-9]+)?)`; `G([0-9]+(?:\.[0-9]+)?)`/)
    next unless calibrated

    {
      name: calibrated[1],
      note: calibrated[2].strip,
      s: calibrated[3].to_f,
      i: calibrated[4].to_f,
      g: calibrated[5].to_f
    }
  end
end.compact.sort_by { |row| [-row[:g], -row[:s], -row[:i], row[:name]] }

def fmt(number)
  number == number.to_i ? number.to_i.to_s : format("%.1f", number)
end

audit_rows = scores.map.with_index(1) do |row, index|
  caveat = row[:note].empty? ? "—" : row[:note].sub(/^—\s*/, "")
  "| #{index} | #{row[:name]} | #{fmt(row[:s])}/#{fmt(row[:i])}/#{fmt(row[:g])} | #{caveat} |"
end.join("\n")

body = <<~MARKDOWN
  # Scratch-made restaurants within a 30-minute drive of East Millcreek

  Research completed July 17, 2026 from the 2958 S 2520 E origin. These are the shortlists I would actually use; hours and operating formats can change, so verify before leaving—especially for pop-ups, tasting menus, and lunch-only places.

  ## Pick by mood

  ### The best meal in town

  **[Ramen Ichizu](https://www.instagram.com/ramen_ichizu/) · [Monte](https://monteslc.com/) · Table X**

  Ichizu makes noodles from flour and builds tare, oils, dashi and layered broths in-house; Monte brings fermentation, curing, koji, live-fire work and frequent seasonal change to a tasting format; Table X builds a daily-responsive seasonal menu around handmade bread, its garden, local farms and a named mill. These are all excellent—choose by ramen counter, experimental tasting menu, or seasonal tasting dinner rather than treating tiny score differences as meaningful.

  ### Something I can't get elsewhere

  **[Prime Corn](https://www.primecornfood.com/) · Navajo Hogan · [Laan Na Thai](https://spicekitchenincubator.org/chefs/laan-na-thai)**

  Prime Corn works through nixtamalization, metate-ground corn, fermented masa and pre-Hispanic dishes, but is primarily preorder/catering/events rather than dependable walk-in dining. Navajo Hogan is a rare Diné specialist making frybread, beans and Saturday mutton stew; posted-hours reliability has drawn occasional complaints. Laan Na Thai's owners cook Northern Thai dishes such as hung lay pork and kao soi in a tiny counter-service kitchen, with daily-changing lunch specials.

  ### Great casual scratch meal

  **[Cafe Anh Hong](https://www.cafeanhhong.com/) · [Curry Fried Chicken](https://www.curryfriedchickenutah.com/) · Sri Annapoorani**

  Choose daily handmade dim sum and morning hand-pulled noodles; chicken built from toasted/ground spices, a 24-hour brine and careful dredge-and-fry technique; or fermented rice-lentil batters, steamed idli, house chutneys and rotating daily South Indian dishes. These are serious kitchens in unfussy formats.

  ### Who's doing a cuisine right

  **[Stoneground Italian Kitchen](https://stonegrounditalian.com/) (Italian) · Koyote (Japanese) · Rincon Salvadoreño (Salvadoran)**

  Each has concrete technique behind the label: Stoneground's fresh pasta, cheese, sausage and focaccino; Koyote's extensive house-made, braised and smoked preparations with limited and seasonal items; and Rincon Salvadoreño's scratch masa work, hand-shaped pupusas and traditional stews. These three broaden the cuisine lookup without reusing any venue from the other occasion lists.

  ## Rare dishes worth a detour

  These are dish finds, not claims that one restaurant is globally “best.” Availability can be event- or day-specific.

  - **Binchotan-grilled chicken hearts or pork-wrapped enoki — Bar Nohm, 165 W 900 S.** A visible binchotan grill and daily-changing menu make these proper charcoal skewers unusually hard to match locally; availability follows the day's menu.
  - **Khao soi tonkatsu — The Big Mango, 4182 W 13400 S, Riverton.** Northern Thai curry noodles paired with fresh handmade panko tonkatsu are a restaurant-specific hybrid in this metro, backed by the same kitchen's slow-simmered curry and wok work.
  - **Paneer savory puff — Biscotts, 1098 W South Jordan Pkwy.** Indian bakery-style paneer filling inside the shop's house-made puff pastry is rare locally; the South Jordan bakery makes its pastry and cakes from scratch daily.
  - **House-made vegan shawarma — Mazza, 1515 S 1500 E.** Shawarma made in-house from vital wheat gluten, rather than a purchased plant-based meat, is a scarce Levantine vegetarian preparation here; Mazza also grinds its own spice blends.
  - **Taco on white, blue or red nixtamalized corn — House of Corn, 414 E 200 S.** The owner cooks whole corn with calcium hydroxide to make the masa foundation for the restaurant's multicolor tortillas; very few local taco shops perform that process in-house.

  ## Scratch dessert places in the east-side corridor

  This is the complete deduplicated corridor subset surfaced from the classified population: Millcreek/East Millcreek, Sugar House, 9th & 9th/9th Avenue, 15th & 15th, Harvard–Yale, Foothill, nearby Holladay, and a few clearly marked geographic-edge places. “At 8” means the published first-party hours encompassed 8 p.m. on at least some days when checked July 15–17.

  ### Strongest 8 p.m. dessert bets

  | Place | Scratch evidence | 8 p.m. availability |
  |---|---|---|
  | [Parfé Diem](https://parfediem.com/), 2040 S 1000 E | Scratch-baked wafers; monthly and seasonal parfaits | Daily, published to 11 |
  | [The Dodo](https://www.thedodorestaurant.com/), 1355 E 2100 S | Pastry chef bakes the rotating pies, cakes and other desserts in-house daily | Yes, published to 10/11 |
  | [’mina](https://www.minaslc.com/), 439 E 900 S | Handmade pastries, filled-to-order cannoli and daily gelato | Yes, published to 9:30/10 |
  | [Per Noi](https://pernoitrattoria.com/), 3005 Highland Dr | Homemade tiramisu, panna cotta, cannoli, budino and daily cake | Mon–Sat; Sunday closed |
  | [Hearth and Hill](https://hearth-hill.com/sugar-house/), 2188 S Highland | Desserts made daily by its pastry team; house sorbet | Daily, published to 9 |
  | [Franco's Churro House](https://francoschurrohouse.com/contact-us/), 2236 S 1300 E | Handmade, made-to-order churros | Daily hours encompass 8 |
  | [Matcha Cafe Kyoto](https://www.matchacafekyoto.com/home), 2223 S Highland | Mochi, ice cream, red bean and jellies made in-house daily | Yes, published to 9/10 |
  | [Harbor Seafood & Steak](https://harborslc.com/), 2302 E Parleys Way | House salted-caramel ice cream with warm chocolate cake | Yes; to 9/10, Sunday 8:30 |
  | [Thirst Millcreek](https://www.thirstdrinks.com/locations), 3063 E 3300 S | Store-made scratch pretzels and beignets; weekly features | Mon–Sat; Sunday closes 5 |
  | [Rawtopia](https://rawtopia.com/), 3961 S Wasatch | Handcrafted scratch raw desserts and cheesecake | Safest Fri–Sat; 8 is closing time on other open days |
  | [Log Haven](https://log-haven.com/dining-menu/), Millcreek Canyon | Daily house ice creams/sorbets and composed desserts | Dinner daily, published to 9 |
  | [Magnolia Bakery Holladay](https://www.magnoliabakery.com/blogs/stores/holladay-hills) | Small-batch scratch pudding, cakes, cupcakes and cookies; branch rating remains unconfirmed | Mon–Sat to 9; Sunday closes 4 |
  | [MiaoMiao Cafe](https://www.hellomiaomiaolisa.com/), 808 S 200 E (edge) | Officially handmade desserts and fresh-baked croissants | Mon–Sat to 9; Sunday 7 |
  | [VENETO](https://venetoslc.com/%C3%A0-la-carte), 370 E 900 S (edge) | Homemade fruit tart and changing seasonal desserts | Tue–Sun to 10; Monday closed |
  | [Salt & Olive](https://saltnolive.com/), 270 S 300 E (edge) | Official house-made dessert program | Published to 10/10:30 |
  | Nomad East, 1675 E 1300 S | House biscuit with strawberry-rhubarb compote and cream; narrower dessert proof | Published to 9/10 |

  ### Scratch dessert places that close earlier

  - Sidecar Doughnuts, 701 E 2100 S — full scratch doughnut, filling, glaze and custard production; closes by 7.
  - Tulie Bakery, 1510 S 1500 E — house brioche, ricotta and jam plus cakes, tarts, cookies and croissants; closes 5.
  - Table X Bakery, 1457 E 3350 S — handmade daily bread and scratch pastry; bakery closes 3.
  - Finn's Cafe, 1624 S 1100 E — scratch-daily danishes, Jule Kake and breads; closes 2:30.
  - All Purpose Bakehouse, 779 S 200 E (edge) — owner-made, fresh-daily laminated pastry; closes 2.
  - Picnic Cafe, 1329 S 500 E — in-house cookies, scones, hand pies, brioche and bagels; only Friday evening service reaches 8.
  - Hill's Kitchen Sugar House, 2188 S Highland — explicit house-made ice cream and a changing pastry case; 8/8:30 closing boundary.
  - Hub & Spoke, 1291 S 1100 E — narrower, third-party “homemade” donut-hole evidence; closes before 8.

  **Uncertain, not promoted:** Layla in Holladay has only third-party “homemade” proof for its chocolate-macadamia pie. Monkeywrench Sugar House is a verified branch, but the scratch ice-cream/add-in evidence and hours recovered were not branch-specific. Supplier-made/off-site desserts and places with scratch proof only for savory food were excluded.

  ## Coverage and limits

  The broad survey processed **2,886** map-derived rows; targeted discovery retained **70** additional visible-head and long-tail leads, for a **2,956-row source union before deduplication**. Phase 3 canonicalization and the user-approved U.S.-only standardized-chain novelty screen produced the research population. Phase 7 found **6** omissions, routed all six back through evidence and scoring, then repeated the entire 24-query coverage challenge with a **last-pass yield of 0**. The final evidence and decision universes each contain **1,650 records**, exactly once.

  This is a source-converged market survey, not a claim that OpenStreetMap or the public web is a complete real-world census. Mobile operators, private/cottage formats, very new openings, businesses without a stable web footprint, hour changes, and places beyond the irregular 30-minute drive polygon remain the main blind spots. “Unresolved” means the searches exhausted without enough evidence for a responsible number; it does not mean bad food.

  ## Combined score audit

  The reader-facing lists above intentionally show only three places per intent. This table retains every numerically scoreable venue for audit and future aggregation. `S` summarizes demonstrated scratch production; `I` summarizes return/discovery interest; `G` is their combined score. These are evidence estimates, not false-precision claims about subjective taste. Equal and near-equal values should be read as ties.

  | # | Venue | S / I / G | Caveat |
  |---:|---|---:|---|
  #{audit_rows}

  Full unresolved, evidence-exhausted, preference-screened, duplicate and disqualification decisions remain in [06-decisions.md](./06-decisions.md); accepted evidence provenance is in [05-evidence-ledger.md](./05-evidence-ledger.md).
MARKDOWN

File.write(File.join(run_dir, "08-results.md"), body, encoding: "UTF-8")
puts "wrote 08-results.md with #{scores.length} numeric audit rows"
