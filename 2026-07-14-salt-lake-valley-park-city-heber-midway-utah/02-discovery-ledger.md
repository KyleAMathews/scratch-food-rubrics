# Phase 2 Discovery Ledger

Status: discovery union only. No scratch qualification, disqualification, scoring, or ranking has occurred.

## Source inventory

- Track A raw responses: `02-source-data/track-a-salt-lake-county-overpass.json` (222 elements), `track-a-park-city-snyderville-core-overpass.json` (7), `track-a-park-city-snyderville-adjacent-overpass.json` (9), and `track-a-heber-valley-overpass.json` (7).
- Track A deduplicated raw union: `02-source-data/track-a-union.json` (241 unique OSM elements; 240 named, 1 unnamed).
- Track B/C reusable source summary: `02-source-data/track-b-c-search-results.md`.
- Failed/partial Overpass responses are preserved in `02-source-data/` and are not counted as results.

## Track B/C named additions not already resolved as an OSM identity

| discovery_id | name | geography / format | track/query batch | discovery source | discovery state |
|---|---|---|---|---|---|
| T-001 | Salt Lake Sourdough | Salt Lake City; home microbakery | B1/B4/B5 | https://saltlakesourdough.com/ | raw named lead |
| T-002 | Mims Bakery | Salt Lake City; preorder/wholesale microbakery | B1/B4/B7 | https://www.lokicoffeeco.com/loki-partners | raw named lead |
| T-003 | Tomodachi Bake Shoppe | Salt Lake City; wholesale microbakery | B1/B7 | https://www.lokicoffeeco.com/loki-partners | raw named lead |
| T-004 | Bedlam | Salt Lake City; weekend stand | B1/B8 | https://www.reddit.com/r/SaltLakeCity/comments/1mhvjom/best_bakeries_in_the_valley/ | identity-thin raw lead |
| T-005 | Slice of Delight | Salt Lake area; cottage cake-slice specialist | B1 | https://www.reddit.com/r/SaltLakeCity/comments/1th8xvh/best_cake_by_the_slice/ | identity-thin raw lead |
| T-006 | Bix Bakery & Cafe | Salt Lake City; cafe/bakery | B1/C1 | https://www.axios.com/local/salt-lake-city/2023/09/19/bix-bakery-cafe-2100-east-sugar-house | raw named lead |
| T-007 | Cinnful Buns | Salt Lake City; vegan bun specialist | B1/B8 | https://www.happycow.net/reviews/cinnful-buns-salt-lake-city-463993 | raw named lead |
| T-008 | The Grey Rabbit Bakery | Millcreek farmers market vendor | B4/B8 | https://utahstories.com/2025/08/millcreek-farmers-market-wednesday/ | raw named lead |
| T-009 | Crumb Collective | Salt Lake City; preorder sourdough microbakery | B4/B5 | https://crumbcollective.co/ | raw named lead |
| T-010 | Doughlene Bakes SLC | Salt Lake area; sourdough microbakery | B4/B5 | https://www.doughlenebakesslc.com/ | raw named lead |
| T-011 | The Salted Loaf | Salt Lake-area identity not yet fixed | B5 | https://www.thesaltedloaf.com/order/p/traditional-sourdough | identity/geography repair needed |
| T-012 | Petite Orangerie | Salt Lake City; planned glacerie/pâtisserie | B6 | https://orangeriepetite.com/ | planned-status raw lead |
| T-013 | The Chocolate Palette | Holladay; commercial-kitchen chocolatier | B6 | https://thechocolatepalette.com/ | raw named lead |
| T-014 | Aroma Chocolates | East Millcreek/Salt Lake City; small-batch chocolatier | B6 | https://www.aromachoco.com/ | raw named lead |
| T-015 | Crown Chocolate | Salt Lake City; chocolatier/manufacturer | B6 | https://crownchocolate.com/ | format repair needed |
| T-016 | Amsterdam Delicious | Salt Lake City; Dutch bakery/stroopwafel specialist | B6 | https://utahsown.org/member-directory/listing/amsterdam-delicious/ | raw named lead |
| T-017 | Sheer Ambrosia Bakery | Salt Lake City; baklava specialist | B6 | https://sheerambrosiabakery.com/wp-content/uploads/2025/06/Sheer-Ambrosias-Media-Kit.pdf | raw named lead |
| T-018 | Sweets by Steph SLC | Sugar House; preorder Greek sweets | B6 | https://sweetsbystephslc.com/ | raw named lead |
| T-019 | Nano's Bagels | Sandy; bagel specialist | B7 | https://nanosbagels.com/ | raw named lead |
| T-020 | Mi Casa Tortilleria | West Valley City; tortillería | B7 | https://www.axios.com/local/salt-lake-city/2023/06/13/west-valley-city-mi-casa-tortilleria-corn-tortilleria | raw named lead |
| T-021 | House of Corn | Salt Lake City; restaurant with nixtamal/tortilla production | B7 | https://www.axios.com/newsletters/axios-salt-lake-city-c7252f10-e873-11ee-9c7b-e1bbf8b6ab08 | category-adjacent raw lead |
| T-022 | El Asadero | Salt Lake City; restaurant claiming homemade tortillas | B7 | https://elasaderomexicanfood.com/ | category-adjacent raw lead |
| T-023 | Auntie Em's | Park City; bakery | B2/C1 | https://www.parkcitymag.com/eat-and-drink/park-city-bakeries | raw named lead |
| T-024 | The Bake Shop | Kimball Junction; artisan bakery/cafe | B2/C1 | https://www.visitparkcity.com/listing/the-bake-shop/29859/ | raw named lead |
| T-025 | Hawk & Sparrow | Heber City; bread bakery | B2/C1 | https://www.parkcitymag.com/eat-and-drink/park-city-bakeries | raw named lead |
| T-026 | Park City Desserts | Park City; gluten-free dessert bakery | B2/C1 | https://www.parkcitymag.com/eat-and-drink/park-city-bakeries | raw named lead |
| T-027 | Red Bicycle Breadworks | Park City; wholesale/market bread bakery | B2/C1 | https://www.parkcitymag.com/eat-and-drink/park-city-bakeries | raw named lead |
| T-028 | Süss Cookie Company | Midway; cookie specialist | B2/C1 | https://www.parkcitymag.com/eat-and-drink/park-city-bakeries | raw named lead |
| T-029 | Midway Bakery on Main | Midway; bakery | B2 | https://www.visitutah.com/articles/heber-eats | raw named lead |
| T-030 | Dottie's Kolaches | Heber City; kolache specialist | B2 | https://www.visitutah.com/articles/heber-eats | raw named lead |
| T-031 | Judy's Donuts | Midway; doughnut specialist | B2 | https://www.visitutah.com/articles/heber-eats | raw named lead |
| T-032 | Hungry Bunny Bakery | Heber/Park City; custom/preorder bakery | B2 | https://www.hungrybunnybakery.com/ | raw named lead |
| T-033 | Panaderia y Pasteleria Santa Cruz | Heber City; panadería | B2 | https://www.panaderiaypasteleriasantacruz.com/en/about | raw named lead |
| T-034 | The Pretzel Connection | Heber City; preorder pretzel specialist | B2 | https://www.restaurantji.com/ut/midway/bakery/ | raw named lead |
| T-035 | Tina's Bakery | Park City; Argentine bakery/empanada specialist | B2 | https://www.restaurantji.com/ut/midway/bakery/ | raw named lead |
| T-036 | CC Sweet Crumbs | Heber; pastry business | B2/C1 | https://www.parkcitymag.com/eat-and-drink/2025/01/french-dining-chef-zamarra | raw named lead |
| T-037 | Luna's Kitchen & Juicery | Park City; dedicated GF kitchen/bakery | B2/B4/C1 | https://www.visitparkcity.com/listing/lunas-kitchen-%26-juicery/22779/ | category-adjacent raw lead |
| T-038 | Bagel Coop | Park City; bagel specialist | B7 | https://www.reddit.com/r/SaltLakeCity/comments/1pzxq9y/i_want_to_try_every_bagel_in_the_valley/ | identity-thin raw lead |
| T-039 | Pie Party | Salt Lake City; pie specialist | B1/B8 | https://www.reddit.com/r/SaltLakeCity/comments/1j82apn/best_cakespastriesbakeries/ | identity repair needed |
| T-040 | Love & Light Bakery | Salt Lake City; bakery sharing 556 E 2100 S listing | B8 | https://www.happycow.net/reviews/cinnful-buns-salt-lake-city-463993 | possible alias/co-location |
| T-041 | Doki Doki Dessert Cafe | Salt Lake City; Japanese dessert specialist | B1 | https://www.dokidessert.com/best-desserts-slc | category-adjacent raw lead |
| T-042 | Gluten Free by Kassie | Salt Lake area; informal GF baker | B4 | https://www.reddit.com/r/SaltLakeCity/comments/1gaa4ub/gluten_free_bakery/ | identity-thin raw lead |

## Track A raw OSM union rows

These rows preserve every unique broad-survey result before semantic category hygiene and Phase 3 deduplication. `osm_tags` are discovery metadata only.

| discovery_id | OSM identity | name | shown address | osm_tags | discovery state |
|---|---|---|---|---|---|
| A-001 | node:11460525194 | [unnamed] | 3678 West 2100 South Salt Lake City | shop=chocolate | raw broad-survey result |
| A-002 | node:4543847111 | 85°C Bakery Cafe | 3390 South State Street South Salt Lake | shop=pastry; amenity=cafe; cuisine=coffee_shop;chinese | raw broad-survey result |
| A-003 | node:12724564689 | Alebrijes Candy Shop | 4936 West 3500 South West Valley City | shop=confectionery | raw broad-survey result |
| A-004 | node:12724564688 | Alicia's Panaderia | 4936 West 3500 South West Valley City | shop=bakery | raw broad-survey result |
| A-005 | node:13360544821 | Alicia's Panaderia | 2653 West 7800 South West Jordan | shop=bakery | raw broad-survey result |
| A-006 | node:13447180957 | All Purpose Bakehouse | 779 South 200 East Salt Lake City | amenity=cafe; cuisine=coffee_shop;bakery | raw broad-survey result |
| A-007 | node:13758777136 | Altojitos |  | amenity=fast_food; cuisine=mexican;dessert | raw broad-survey result |
| A-008 | node:12843245771 | Antojitos Luna | 4865 West 3500 South West Valley City | shop=confectionery | raw broad-survey result |
| A-009 | node:3625585827 | Atticus Coffee, Books, and Teahouse |  | shop=books; amenity=cafe; cuisine=coffee_shop;bakery | raw broad-survey result |
| A-010 | node:3738277586 | Auntie Rae's Sweets & Tea Parties | 4704 South Holladay Boulevard Holladay | shop=bakery | raw broad-survey result |
| A-011 | node:12563395901 | Avenue Bakery on Fourth | 376 East 4th Avenue Salt Lake City | shop=bakery | raw broad-survey result |
| A-012 | node:11040239394 | Baby's Bagels | 204 East 500 South Salt Lake City | shop=bakery | raw broad-survey result |
| A-013 | way:984111235 | Bagel Den | 570 North Main Street Heber City | shop=bakery | raw broad-survey result |
| A-014 | node:6569219699 | Bakers C & C |  | shop=chocolate | raw broad-survey result |
| A-015 | way:291855245 | Banbury Cross | 678 700 South Salt Lake City | amenity=restaurant; cuisine=donut | raw broad-survey result |
| A-016 | node:13002359687 | Beaucoup Boulangerie et Marche | 3939 South Wasatch Boulevard Millcreek | shop=bakery | raw broad-survey result |
| A-017 | way:1072033317 | Beaumont Bakery |  |  | raw broad-survey result |
| A-018 | node:10022696830 | Beaumont Bakery & Cafe | 3979 South Wasatch Boulevard Salt Lake City | amenity=restaurant; cuisine=regional | raw broad-survey result |
| A-019 | node:2460700082 | Bonne Vie |  | shop=bakery | raw broad-survey result |
| A-020 | node:4584427247 | Breads |  | shop=bakery | raw broad-survey result |
| A-021 | node:10939073390 | Break Bread Barber Co. | 14732 South Marketplace Drive Herriman | shop=hairdresser | excluded: literal non-bakery category collision |
| A-022 | node:8065670998 | Break Bread Barber Co. | 910 North 900 West Salt Lake City | shop=hairdresser | excluded: literal non-bakery category collision |
| A-023 | way:377643147 | Bruges Waffles & Frites | 2314 South Highland Drive Salt Lake City | shop=confectionery; amenity=cafe; cuisine=international | raw broad-survey result |
| A-024 | node:10062272944 | Buono Bakery | 662 Union Square Sandy | shop=bakery | raw broad-survey result |
| A-025 | node:13568770623 | Buzzed Coffeehouse | 265 South State Street Salt Lake City | amenity=cafe; cuisine=coffee_shop;ice_cream;pastry | raw broad-survey result |
| A-026 | node:2366146738 | Cake |  | shop=clothes | excluded: literal non-bakery category collision |
| A-027 | node:9438490307 | Cakes By Edith | 1736 West 5000 South Taylorsville | shop=bakery | raw broad-survey result |
| A-028 | node:13051329499 | Canela Bakery | 25 East Kensington Avenue Salt Lake City | shop=pastry | raw broad-survey result |
| A-029 | node:2344998584 | Carlucci's | 282 South 300 West Salt Lake City | shop=bakery; amenity=cafe | raw broad-survey result |
| A-030 | node:5271105172 | Carol's Pastry Shop |  | shop=bakery | raw broad-survey result |
| A-031 | node:11388299254 | Chez Nibs | 212 East 500 South Salt Lake City | shop=chocolate | raw broad-survey result |
| A-032 | node:11663776618 | Chip |  | shop=pastry | raw broad-survey result |
| A-033 | node:13205806303 | Chip |  | shop=pastry | raw broad-survey result |
| A-034 | node:11102308889 | Chip Cookies | 4578 West Partridge Hill Lane Riverton | shop=pastry | raw broad-survey result |
| A-035 | way:1134018865 | Chip Cookies | 2340 East 4500 South Holladay | shop=bakery | raw broad-survey result |
| A-036 | way:580736053 | Chip Cookies | 2180 South 700 East Salt Lake City | shop=pastry | raw broad-survey result |
| A-037 | node:13410395414 | Chocolate Cottage |  | shop=chocolate | raw broad-survey result |
| A-038 | node:12911144563 | Chocolate Covered Wagon - Trolley Taffy Stat | 1100 West 7800 South West Jordan | shop=confectionery | raw broad-survey result |
| A-039 | node:6805873030 | Cinnabon | 2025 South 900 West Salt Lake City | amenity=fast_food; cuisine=dessert | raw broad-survey result |
| A-040 | node:12818233991 | City Cakes | 7009 South High Tech Drive Midvale | shop=pastry | raw broad-survey result |
| A-041 | node:5935692028 | City Cakes | 1860 South 300 West Salt Lake City | shop=bakery | raw broad-survey result |
| A-042 | node:12959915948 | Colombian Baker | 2594 West 4700 South Taylorsville | shop=bakery | raw broad-survey result |
| A-043 | node:8060731366 | Condie's Candies | 1479 South Main Street Salt Lake City | shop=confectionery | raw broad-survey result |
| A-044 | way:439745494 | Corner Bakery | 610 South Foothill Drive Salt Lake City | amenity=cafe; cuisine=coffee_shop | raw broad-survey result |
| A-045 | node:3999437607 | Corner Bakery Cafe |  | shop=bakery; amenity=cafe; cuisine=coffee_shop | raw broad-survey result |
| A-046 | node:10940793043 | Crave |  | shop=pastry | raw broad-survey result |
| A-047 | node:11841905469 | Crave | 20 East 600 South Salt Lake City | shop=pastry | raw broad-survey result |
| A-048 | node:11842281449 | Crave | 1400 South Foothill Drive Salt Lake City | shop=pastry | raw broad-survey result |
| A-049 | node:3634690170 | Crave | 7386 Union Park Avenue Cottonwood Heights | shop=pastry | raw broad-survey result |
| A-050 | node:9646026425 | Crave Cookies | 2723 West 3500 South West Valley City | shop=pastry | raw broad-survey result |
| A-051 | node:10944787424 | Creme de Bakery | 5043 South State Street Murray | shop=bakery | raw broad-survey result |
| A-052 | node:12123324770 | Crumbl Cookies | 7626 South Campus View Drive West Jordan | shop=pastry | raw broad-survey result |
| A-053 | node:7801562400 | Crumbl Cookies | 1844 East Fort Union Boulevard | shop=pastry; amenity=restaurant; cuisine=dessert | raw broad-survey result |
| A-054 | node:9080763995 | Crumbl Cookies | 675 East 2100 South Salt Lake City | shop=pastry | raw broad-survey result |
| A-055 | node:9654029905 | Crumbl Cookies | 3515 West 3500 South West Valley City | shop=pastry | raw broad-survey result |
| A-056 | node:9962828798 | Crumbl Cookies |  | shop=pastry | raw broad-survey result |
| A-057 | node:12857804066 | Crust Club |  | shop=bakery | raw broad-survey result |
| A-058 | node:2211697127 | Cucina | 1026 East 2nd Avenue Salt Lake City | amenity=restaurant; cuisine=sandwich;american;seafood;breakfast;pastry;diner;fine_dining;wine;bar | raw broad-survey result |
| A-059 | way:292023896 | Cumming's Studio Chocolates | 679 East 900 South Salt Lake City | craft=confectionery | raw broad-survey result |
| A-060 | way:595951140 | Cupcake Nail & Beauty Bar | 218 South 300 East Salt Lake City | shop=beauty | excluded: literal non-bakery category collision |
| A-061 | node:10940423843 | Cupcakes by Kasthuri | 824 South 400 West Salt Lake City | shop=bakery | raw broad-survey result |
| A-062 | node:3738287139 | Daniel's Fine Chocolate |  | craft=confectionery | raw broad-survey result |
| A-063 | node:10136165864 | Darla's Doughnuts |  | amenity=fast_food; cuisine=donut | raw broad-survey result |
| A-064 | node:4379967604 | Daylight Donuts |  | amenity=fast_food; cuisine=donut | raw broad-survey result |
| A-065 | node:13910383258 | Dear Coco |  | shop=gift; amenity=cafe; cuisine=chocolate | raw broad-survey result |
| A-066 | node:11868093660 | Delicias Fruty Snacks | 1739 West 4160 South Taylorsville | amenity=restaurant; cuisine=mexican;dessert | raw broad-survey result |
| A-067 | node:10940754959 | Deseret Bakery Production |  |  | excluded: non-retail production facility |
| A-068 | node:12030016222 | Dirty Dough | 5462 South Redwood Road Taylorsville | shop=pastry | raw broad-survey result |
| A-069 | node:10136165883 | Donut Boy | 2194 West 3500 South West Valley City | amenity=fast_food; cuisine=donut | raw broad-survey result |
| A-070 | node:6434396394 | Donut House | 950 West 1000 North Salt Lake City | shop=donut; amenity=fast_food; cuisine=donut | raw broad-survey result |
| A-071 | node:13544374976 | Donut Star Cafe | 10522 South Redwood Road South Jordan | amenity=fast_food; cuisine=donut | raw broad-survey result |
| A-072 | node:9974905992 | Donut Star Cafe | 213 East 12300 South Draper | amenity=fast_food; cuisine=donut | raw broad-survey result |
| A-073 | node:13040399131 | Dough Lady | 3362 South 2300 East Millcreek | shop=pastry | raw broad-survey result |
| A-074 | node:9917679561 | Dough Miner | 945 South 300 West Salt Lake City | amenity=cafe; cuisine=pasty;donut;bagel | raw broad-survey result |
| A-075 | node:13006702347 | Dunkin' |  | amenity=fast_food; cuisine=donut;coffee_shop | raw broad-survey result |
| A-076 | way:1026199848 | Dunkin' | 1410 West 9000 South West Jordan | amenity=fast_food; cuisine=donut;coffee_shop | raw broad-survey result |
| A-077 | node:9750181485 | Délice | 2747 South State Street South Salt Lake | shop=bakery | raw broad-survey result |
| A-078 | node:9820715160 | Eclair French Pastry | 7948 Union Park Avenue | shop=bakery | raw broad-survey result |
| A-079 | node:3999878471 | Einstein Bagels |  | amenity=cafe; cuisine=american | raw broad-survey result |
| A-080 | node:11974193633 | Einstein Bros. Bagels | 5542 West 7800 South West Jordan | amenity=fast_food; cuisine=bagel | raw broad-survey result |
| A-081 | node:11974193640 | Einstein Bros. Bagels | 2353 East Fort Union Boulevard Salt Lake City | amenity=fast_food; cuisine=bagel | raw broad-survey result |
| A-082 | node:11974193646 | Einstein Bros. Bagels | 72 East 10600 South Sandy | amenity=fast_food; cuisine=bagel | raw broad-survey result |
| A-083 | node:11974193653 | Einstein Bros. Bagels | 11977 South Herriman Main Street Herriman | amenity=fast_food; cuisine=bagel | raw broad-survey result |
| A-084 | node:1402379970 | Einstein Bros. Bagels | 3292 South Richmond Street Salt Lake City | amenity=fast_food; cuisine=bagel | raw broad-survey result |
| A-085 | node:1834779446 | Einstein Bros. Bagels | 3923 South Wasatch Boulevard Salt Lake City | amenity=fast_food; cuisine=bagel | raw broad-survey result |
| A-086 | node:2462094417 | Einstein Bros. Bagels | 481 East South Temple Salt Lake City | amenity=fast_food; cuisine=bagel | raw broad-survey result |
| A-087 | node:4110086520 | Einstein Bros. Bagels | 5588 South Redwood Road Taylorsville | amenity=fast_food; cuisine=bagel | raw broad-survey result |
| A-088 | node:6620807151 | Einstein Bros. Bagels | 200 South Central Campus Drive Salt Lake City | amenity=fast_food; cuisine=bagel | raw broad-survey result |
| A-089 | way:346317288 | Einstein Bros. Bagels | 1297 East Draper Parkway Draper | amenity=fast_food; cuisine=bagel | raw broad-survey result |
| A-090 | way:465766319 | Einstein Bros. Bagels | 3638 West 13400 South Riverton | amenity=fast_food; cuisine=bagel | raw broad-survey result |
| A-091 | way:526380931 | Einstein Bros. Bagels | 1520 South 1500 East Salt Lake City | amenity=fast_food; cuisine=bagel | raw broad-survey result |
| A-092 | way:465432967 | Einstein's Bagels |  | amenity=cafe | raw broad-survey result |
| A-093 | way:659616036 | Einstein's Bagels | 2353 East Fort Union Boulevard Cottonwood Heights | amenity=fast_food; cuisine=american | raw broad-survey result |
| A-094 | node:9643436429 | El Bodegon Dulceria | 1728 West 5000 South Taylorsville | shop=confectionery | raw broad-survey result |
| A-095 | node:11212899342 | Empanadas801 | 465 East 3300 South South Salt Lake | shop=bakery | raw broad-survey result |
| A-096 | node:3836602257 | Eva's Bakery | 155 South Main Street Salt Lake City | amenity=restaurant; cuisine=sandwich;pastry;bakery | raw broad-survey result |
| A-097 | node:7801562401 | Fernwood Finest Candies |  | shop=confectionery | raw broad-survey result |
| A-098 | node:6478982367 | Fillings & Emulsions | 1391 South 300 West Salt Lake City | shop=bakery | raw broad-survey result |
| A-099 | node:8072353903 | Fillings & Emulsions |  | shop=bakery | raw broad-survey result |
| A-100 | node:11828697090 | Flake Pie Co. | 1665 West Towne Center Drive South Jordan | shop=pastry | raw broad-survey result |
| A-101 | node:6401415314 | Flores Bakery | 1625 West 700 North Salt Lake City | shop=bakery | raw broad-survey result |
| A-102 | node:9080763994 | Forty Three Bakery | 733 West Genesee Avenue Salt Lake City | shop=bakery | raw broad-survey result |
| A-103 | way:377640435 | Fresh Donut & Deli | 2699 South State Street South Salt Lake | amenity=cafe; cuisine=donut | raw broad-survey result |
| A-104 | node:7264309080 | Fudge Co | 13292 South Rosecrest Road Herriman | shop=bakery | raw broad-survey result |
| A-105 | node:7020864224 | Garden Gate | 928 East 900 South Salt Lake City | shop=chocolate | raw broad-survey result |
| A-106 | node:9902710846 | Good Food Gluten Free | 423 West 800 South Salt Lake City | shop=bakery | raw broad-survey result |
| A-107 | node:11156256827 | Goodly Cookies | 11429 South District Drive South Jordan | shop=bakery | raw broad-survey result |
| A-108 | node:6124016268 | Gourmandise |  | amenity=restaurant; cuisine=sandwich;bakery | raw broad-survey result |
| A-109 | way:152963645 | Gourmandise | 250 South 300 East Salt Lake City | shop=bakery | raw broad-survey result |
| A-110 | node:7986248981 | Granary Bakehouse |  | shop=bakery | raw broad-survey result |
| A-111 | way:531372369 | Granite Bakery | 902 East 2700 South Salt Lake City | shop=bakery | raw broad-survey result |
| A-112 | node:12485190615 | Great Harvest Bakery & Cafe | 2145 East 2100 South Salt Lake City | shop=bakery | raw broad-survey result |
| A-113 | node:4296767299 | Great Harvest Bread Co. |  | amenity=restaurant | raw broad-survey result |
| A-114 | node:12802962988 | Great Harvest Bread Company | 6357 South Redwood Road Taylorsville | shop=bakery | raw broad-survey result |
| A-115 | node:13818577893 | Great Harvest Bread Company |  | shop=bakery; amenity=fast_food; cuisine=sandwich | raw broad-survey result |
| A-116 | node:2336726852 | Great Harvest Bread Company |  | shop=bakery; cuisine=sandwich | raw broad-survey result |
| A-117 | node:3999811837 | Great Harvest Bread Company | 217 East 12300 South Draper | shop=bakery | raw broad-survey result |
| A-118 | node:12881557410 | Hall Patisserie | 153 South Rio Grande Street Salt Lake City | shop=pastry | raw broad-survey result |
| A-119 | node:12911144568 | Happy Camper Deli & Bakery | 1100 West 7800 South West Jordan | amenity=cafe; cuisine=sandwich;soup;salad;pizza | raw broad-survey result |
| A-120 | node:13082327897 | Happy Camper Deli & Bakery | 602 East 600 South Salt Lake City | amenity=restaurant; cuisine=sandwich;pizza;breakfast;salad | raw broad-survey result |
| A-121 | way:462965668 | Hatch Family Chocolates | 376 East 8th Avenue Salt Lake City | shop=chocolate | raw broad-survey result |
| A-122 | way:227961385 | Java Cow Cafe & Bakery | 402 Main Street Park City | amenity=cafe; cuisine=coffee_shop | raw broad-survey result |
| A-123 | node:9081052616 | Judy's Donuts and Coffee |  | shop=pastry; cuisine=donut;coffee | raw broad-survey result |
| A-124 | node:10102081888 | June Pie | 2175 West 3000 South | shop=bakery | raw broad-survey result |
| A-125 | node:9765598819 | Kahve Cafe |  | amenity=cafe; cuisine=turkish;tea;coffee;dessert | raw broad-survey result |
| A-126 | node:7613734589 | Karim Bakery | 2575 South State Street South Salt Lake | shop=bakery; cuisine=arab;mediterranean | raw broad-survey result |
| A-127 | way:375966630 | Kneaders | 2642 South High Commons Way West Valley City | shop=bakery | raw broad-survey result |
| A-128 | node:2327662164 | Kneaders Bakery & Cafe | 28 South State Street Salt Lake City | amenity=restaurant; cuisine=sandwich;pastry | raw broad-survey result |
| A-129 | way:1014522438 | Kneaders Bakery & Cafe | 1020 South Main Street Heber City | amenity=restaurant; cuisine=sandwich | raw broad-survey result |
| A-130 | way:161134878 | Kneaders Bakery & Cafe | 5083 West 13400 South Riverton | shop=bakery | raw broad-survey result |
| A-131 | node:11842281422 | Krispy Kreme |  | amenity=fast_food; cuisine=donut | raw broad-survey result |
| A-132 | way:1118923798 | Krispy Kreme | 3370 South 5600 West West Valley City | amenity=fast_food; cuisine=donut | raw broad-survey result |
| A-133 | way:1290128659 | Krispy Kreme | 48 W 10600 South Sandy | amenity=fast_food; cuisine=donut | raw broad-survey result |
| A-134 | node:3779011758 | Kyung's Bakery | 153 East 4370 South Murray | shop=bakery | raw broad-survey result |
| A-135 | node:12945750727 | La Espiga Dorada | 2292 West 5400 South Taylorsville | shop=bakery | raw broad-survey result |
| A-136 | node:8067158941 | La Flor de Salt Lake Tortillas |  | shop=bakery | raw broad-survey result |
| A-137 | node:12345185240 | Leavity Bread & Coffee | 1000 South Main Street Salt Lake City | shop=bakery | raw broad-survey result |
| A-138 | way:503509866 | Leslie's Pastries | 2308 East Murray Holladay Road Holladay | shop=bakery | raw broad-survey result |
| A-139 | node:12177433831 | Lisa's Passion for Popcorn | 602 East 500 South Salt Lake City | craft=confectionery | raw broad-survey result |
| A-140 | node:9646152960 | Local Cookie Co | 10384 South River Heights Drive South Jordan | shop=pastry | raw broad-survey result |
| A-141 | node:9791363008 | Lone Pine Bakery | 834 9400 South Sandy | shop=bakery | raw broad-survey result |
| A-142 | node:10082069598 | Louks Greek Baby Donuts |  | amenity=fast_food; cuisine=donut | raw broad-survey result |
| A-143 | node:10705358511 | Ma & Paws Bakery | 1127 East 3300 South Salt Lake City | shop=pet | excluded: literal non-bakery category collision |
| A-144 | node:13931812882 | Magnolia Bakery | 1895 E Rodeo Walk Dr Holladay | shop=bakery | raw broad-survey result |
| A-145 | way:240724203 | Maxim's Nutricare Inc. dba Papa Pita Bakery | 6208 West Dannon Way West Jordan |  | excluded: non-retail production facility |
| A-146 | node:9181476349 | Middle Eastern Bakery & Groceries |  | shop=supermarket | raw broad-survey result |
| A-147 | node:10102006222 | Mochinut | 1241 Center Drive Park City | amenity=fast_food; cuisine=donut;bubble_tea | raw broad-survey result |
| A-148 | node:11490033582 | Mochinut | 10497 South Redwood Road South Jordan | amenity=fast_food; cuisine=donut | raw broad-survey result |
| A-149 | node:9081052601 | Momo's Gourmet Cheesecake | 29 East 400 South Salt Lake City | shop=bakery | raw broad-survey result |
| A-150 | node:13025919972 | Mozz Sourdough Pizza | 416 East 900 South Salt Lake City | amenity=restaurant; cuisine=pizza | raw broad-survey result |
| A-151 | node:4303282416 | Mrs. Backer's Pastry Shop | 434 East South Temple Salt Lake City | shop=bakery | raw broad-survey result |
| A-152 | way:553841490 | Mrs. Call's Chocolates | 356 W 1000 S Heber City |  | raw broad-survey result |
| A-153 | node:9645711038 | Mrs. Hewitt's | 395 West Lawndale Drive South Salt Lake | shop=bakery | raw broad-survey result |
| A-154 | node:9217147215 | My Sugar's Donut Shoppe |  | amenity=fast_food; cuisine=donut | raw broad-survey result |
| A-155 | node:9523414857 | Napoli's Italian Restaurant | 7640 Union Park Avenue Sandy | amenity=restaurant; cuisine=italian;seafood;dessert;chicken;pasta | raw broad-survey result |
| A-156 | node:13712161379 | Nature's Bakery | 2331 North 2200 West Salt Lake City |  | excluded: non-retail production facility |
| A-157 | node:11842281430 | Nothing Bundt Cakes | 1354B South Foothill Drive Salt Lake City | shop=pastry | raw broad-survey result |
| A-158 | node:13604377578 | Nothing Bundt Cakes | 12271 South Herriman Main Street Herriman | shop=pastry | raw broad-survey result |
| A-159 | node:5360175064 | Nothing Bundt Cakes | 10389 South State Street Sandy | shop=pastry | raw broad-survey result |
| A-160 | node:8369676385 | Nothing Bundt Cakes | 5338 South Redwood Road Taylorsville | shop=pastry | raw broad-survey result |
| A-161 | node:9791175933 | Old Cuss Cafe | 325 West Pierpont Avenue | amenity=cafe; cuisine=breakfast;brunch;pastry | raw broad-survey result |
| A-162 | node:12167176411 | Panaderia Dulcinea Bakery |  | shop=bakery; cuisine=spanish | raw broad-survey result |
| A-163 | node:9983808823 | Panaderia Lizbeth | 1013 North 900 West Salt Lake City | shop=bakery | raw broad-survey result |
| A-164 | way:1313885164 | Panaderia Mexico | 5423 South 4015 West Taylorsville | shop=bakery; cuisine=mexican | raw broad-survey result |
| A-165 | way:1131057239 | Panderia Flores | 904 South 900 West Salt Lake City | shop=bakery | raw broad-survey result |
| A-166 | node:11490281092 | Panera Bread |  | amenity=fast_food; cuisine=sandwich;bakery | raw broad-survey result |
| A-167 | node:8072353908 | Panera Bread | 3920 West Terminal Drive Salt Lake City | amenity=fast_food; cuisine=sandwich;bakery | raw broad-survey result |
| A-168 | node:13206248359 | Parfé Diem | 2040 South 1000 East Salt Lake City | amenity=cafe; cuisine=dessert;pudding | raw broad-survey result |
| A-169 | node:12088012574 | Paris Baguette | 950 Fort Union Boulevard Midvale | shop=bakery | raw broad-survey result |
| A-170 | node:4296789376 | Park City Bread and Bagel |  | amenity=restaurant | raw broad-survey result |
| A-171 | node:5253317024 | Passion Flour Patisserie | 165 East 900 South Salt Lake City | shop=pastry | raw broad-survey result |
| A-172 | node:4725175593 | Picnic Cafe |  | amenity=cafe; cuisine=coffee_shop;pastry;sandwich;ice_cream | raw broad-survey result |
| A-173 | node:8125277503 | Pie Fight | 937 East 900 South Salt Lake City | shop=bakery | raw broad-survey result |
| A-174 | node:11967530153 | Pink Sweets Cafe | 1872 West 12600 South Riverton | shop=pastry | raw broad-survey result |
| A-175 | node:11205948044 | RISE Bakery & Market | 7872 South Old Bingham Highway West Jordan | shop=bakery; cuisine=polish | raw broad-survey result |
| A-176 | node:11868093663 | Refreskeria Mi Fiesta Facil |  | amenity=restaurant; cuisine=mexican;dessert | raw broad-survey result |
| A-177 | node:2468870399 | Rich's Bagels |  | amenity=cafe | raw broad-survey result |
| A-178 | node:5322812253 | Rich's Bagels | 8691 Highland Drive Sandy | amenity=cafe | raw broad-survey result |
| A-179 | node:10102081887 | Ritual Chocolate | 2175 West 3000 South | shop=chocolate | raw broad-survey result |
| A-180 | node:1695357156 | Rocket Fizz |  | shop=confectionery | raw broad-survey result |
| A-181 | node:5726247454 | Rocket Fizz | 51 South Rio Grande Street Salt Lake City | shop=confectionery | raw broad-survey result |
| A-182 | node:3634690192 | Rocky Mountain Chocolate Factory |  | shop=confectionery | raw broad-survey result |
| A-183 | node:4299141280 | Rocky Mountain Chocolate Factory |  | shop=confectionery | raw broad-survey result |
| A-184 | node:4468747090 | Rocky Mountain Chocolate Factory |  | shop=confectionery | raw broad-survey result |
| A-185 | way:1059426026 | Rocky Mountain Chocolate Factory |  | shop=confectionery | raw broad-survey result |
| A-186 | node:13002359681 | Rough Stone Bakery |  | shop=bakery | raw broad-survey result |
| A-187 | node:4167659584 | RubySnap Fresh Cookies | 770 South 300 West Salt Lake City | shop=pastry | raw broad-survey result |
| A-188 | node:12072645710 | Sagato's Bakery and Cafe | 44 West 7200 South Midvale | amenity=restaurant; cuisine=new_zealand;samoan | raw broad-survey result |
| A-189 | node:12924911470 | Salt City Che | 3585 South Redwood Road West Valley City | amenity=cafe; cuisine=dessert;vietnamese | raw broad-survey result |
| A-190 | node:11959382691 | Salt City Sweet Shop |  | craft=confectionery | raw broad-survey result |
| A-191 | node:13956033039 | Sapori | 3667 | shop=bakery | raw broad-survey result |
| A-192 | node:12964534972 | Schmidt's Pastry Cottage | 1133 West South Jordan Parkway South Jordan | shop=bakery | raw broad-survey result |
| A-193 | node:4110086526 | Schmidt's Pastry Cottage | 5664 South Redwood Road Taylorsville | shop=bakery | raw broad-survey result |
| A-194 | node:3681524449 | See's Candies | 2707 South 700 East Salt Lake City | shop=confectionery | raw broad-survey result |
| A-195 | node:3999722854 | See's Candies | 940 Fort Union Boulevard Midvale | shop=confectionery | raw broad-survey result |
| A-196 | node:4600674926 | See's Candies | 12423 South Minuteman Drive Draper | shop=confectionery | raw broad-survey result |
| A-197 | node:6603406513 | Shane's Donuts | 5471 South State Street Murray | amenity=fast_food; cuisine=donut | raw broad-survey result |
| A-198 | node:12713670559 | Shugarlandia | 3628 West 3500 South West Valley City | amenity=restaurant; cuisine=mexican;dessert | raw broad-survey result |
| A-199 | node:13772893400 | Shugarlandia |  | amenity=fast_food; cuisine=mexican;ice_cream;dessert;l | raw broad-survey result |
| A-200 | node:12190990757 | Sidecar Doughnuts & Coffee | 701 East 2100 South Salt Lake City | amenity=fast_food; cuisine=donut | raw broad-survey result |
| A-201 | node:9173321350 | So Cupcake |  | shop=bakery | raw broad-survey result |
| A-202 | node:9898708153 | Sprinkle's Cupcakes | 4488 West Teal Ridge Way Riverton |  | raw broad-survey result |
| A-203 | way:473864175 | Stone Ground Bakery | 1025 South 700 West Salt Lake City | shop=bakery | raw broad-survey result |
| A-204 | node:7928632809 | Stone Ground Bakery Facility #2 |  | shop=bakery | raw broad-survey result |
| A-205 | node:9108643276 | Sweet Corner Treats | 94 South Main Street Heber City | shop=confectionery | raw broad-survey result |
| A-206 | node:10200455388 | Sweet Hazel & Co. Grab & Go | 1000 South Main Street Salt Lake City | shop=snack; cuisine=breakfast;lunch;sandwich;dessert | raw broad-survey result |
| A-207 | node:11105050401 | Sweet Rolled Tacos | 13222 South Tree Sparrow Drive Riverton | shop=pastry | raw broad-survey result |
| A-208 | node:10062272945 | Sweet Spot Bakery & Cafe | 664 Union Square Sandy | shop=bakery; cuisine=brazilian | raw broad-survey result |
| A-209 | way:526378330 | Sweetaly Gelato & Custom Cakes | 1527 South 1500 East Salt Lake City | amenity=ice_cream | raw broad-survey result |
| A-210 | node:9102259105 | Sweethoney Dessert | 3390 South State Street South Salt Lake | amenity=cafe; cuisine=asian;dessert | raw broad-survey result |
| A-211 | node:9173321391 | Table X Bread |  | shop=bakery | raw broad-survey result |
| A-212 | node:2336726857 | The Bagel Project | 1919 East Murray Holladay Road Holladay | amenity=restaurant; cuisine=bagel | raw broad-survey result |
| A-213 | way:593160824 | The Bagel Project | 779 South 500 East Salt Lake City | shop=bakery; cuisine=bagel | raw broad-survey result |
| A-214 | node:2327662145 | The Cheesecake Factory | 65 South Regent Street Salt Lake City | amenity=restaurant; cuisine=american | excluded: literal non-bakery category collision |
| A-215 | node:2328396014 | The Cheesecake Factory |  | amenity=restaurant; cuisine=american | excluded: literal non-bakery category collision |
| A-216 | node:12346447127 | The Chocolate | 9120 South Redwood Road West Jordan | shop=pastry | raw broad-survey result |
| A-217 | node:13523237342 | The Kolache Place | 1751 South 1100 East Salt Lake City | shop=bakery | raw broad-survey result |
| A-218 | node:13763818558 | The Kolache Place | 7579 South Redwood Road West Jordan | shop=bakery | raw broad-survey result |
| A-219 | node:13555929366 | The Nut Garden |  | shop=confectionery | raw broad-survey result |
| A-220 | node:2974596082 | The Original Pancake House |  | amenity=restaurant; cuisine=breakfast;pancake | excluded: literal non-bakery category collision |
| A-221 | node:4100041855 | The Original Pancake House |  | amenity=restaurant; cuisine=breakfast;pancake | excluded: literal non-bakery category collision |
| A-222 | node:6088855134 | The Original Pancake House | 790 East 2100 South Salt Lake City | amenity=restaurant; cuisine=breakfast;pancake | excluded: literal non-bakery category collision |
| A-223 | way:157337541 | The Original Pancake House | 3843 West 13400 South Riverton | amenity=restaurant; cuisine=breakfast;pancake | excluded: literal non-bakery category collision |
| A-224 | node:12094299353 | The Other Side Donuts | 760 South Redwood Road Salt Lake City | amenity=fast_food; cuisine=donut | raw broad-survey result |
| A-225 | node:12376549622 | Tous les Jours |  | shop=bakery | raw broad-survey result |
| A-226 | way:292009563 | Tulie Bakery |  | shop=bakery | raw broad-survey result |
| A-227 | node:3999780434 | Twisted Sugar |  | amenity=restaurant; cuisine=dessert | raw broad-survey result |
| A-228 | node:9975110591 | U-Swirl & Rocky Mountain Chocolate Factory | 241 East 12300 South Draper | amenity=ice_cream | raw broad-survey result |
| A-229 | node:13204028658 | Union Patisserie |  | shop=pastry | raw broad-survey result |
| A-230 | node:4497644489 | V Chocolates | 850 South Main Street Salt Lake City | shop=confectionery | raw broad-survey result |
| A-231 | node:10062272928 | ValSof Bakery | 9486 Union Square Sandy | shop=bakery | raw broad-survey result |
| A-232 | node:1832066742 | Vosen's Bread Paradise | 328 West 200 South Salt Lake City | shop=bakery | raw broad-survey result |
| A-233 | node:11102308888 | Wanna Cinn | 4578 West Partridge Hill Lane Riverton | shop=pastry | raw broad-survey result |
| A-234 | node:2417990135 | Wasatch Bagel |  | amenity=cafe; cuisine=coffee_shop | raw broad-survey result |
| A-235 | node:1667621499 | Windy Ridge Bakery |  | shop=bakery | raw broad-survey result |
| A-236 | node:13683321736 | Wombat Bagels | 2273 West 7800 South West Jordan | amenity=fast_food; cuisine=bagel | raw broad-survey result |
| A-237 | node:2341511597 | Xiao Bao Bao | 216 East 500 South Salt Lake City | shop=bakery; cuisine=chinese | raw broad-survey result |
| A-238 | node:11820468273 | Yao Bakery | 3078 West 7800 South West Jordan | shop=bakery | raw broad-survey result |
| A-239 | node:12926602244 | Yonutz | 11078 S State Street Sandy | amenity=fast_food; cuisine=donut;ice_cream | raw broad-survey result |
| A-240 | node:12952553186 | eats | 248 East 100 South Salt Lake City | shop=pastry; cuisine=pastry;coffee | raw broad-survey result |
| A-241 | node:12264585597 | Éclair |  | shop=pastry | raw broad-survey result |
