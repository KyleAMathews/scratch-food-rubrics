# Execution diary — restaurant rubric v8.10 test run

This diary is maintained after every completed phase. It records what happened, user corrections, and operational knowledge that could have been encoded in the skill.

## Phase 1 — Scope and catchment

### What happened

- Interpreted the screenshot pin as `2958 South 2520 East, Millcreek, Utah 84109, United States` and verified it through Nominatim/OpenStreetMap at `40.7067859, -111.8192536` (OSM labels the neighborhood Canyon Rim).
- Created the mandatory unique run directory and all standard artifacts before research.
- Operationalized “within a 30 minute drive” as a Valhalla/OpenStreetMap 30-minute `auto` isochrone, because a radius would not satisfy the request.
- Saved the literal geocoder response and 1,566-vertex GeoJSON isochrone. The modeled polygon is surprisingly broad along freeways: bbox longitude `-112.282774…-111.401008`, latitude `40.396699…41.062062`.
- Defined point-in-polygon inclusion plus destination-specific routing for generalized boundary cases. Recorded that the public routing model is not live traffic.

### Corrections the user needed to make

- After Phase 1 had completed and Phase 2 had begun, the user clarified that this is a test of a new skill version and required a `diary.md` entry after every phase. This requirement was not in the original request or skill, so the diary was created and Phase 1 was backfilled.

### What had to be figured out that could be encoded in the skill

- The skill says to define a resident-normal market and prefers administrative polygons for named places, but does not explicitly specify precedence when the user supplies an exact **drive-time** catchment. A rule should state that an explicit travel-time constraint overrides municipal-market heuristics and should prescribe an isochrone workflow.
- The skill does not define whether drive time means live traffic, typical traffic, departure-time traffic, or reproducible free-flow routing. The implementation chose a reproducible current routing graph and documented the limitation.
- The skill does not name an isochrone provider, required routing profile/options, polygon generalization tolerance, or how to validate polygon-edge venues. Those decisions were made locally.
- A 30-minute isochrone around a freeway-connected metro can cover a much larger and more irregular market than a map screenshot suggests. The skill offers no size/feasibility checkpoint or batching guidance tied to candidate volume.
- The repository has no top-level `AGENTS.md`; only the root skill and referenced phase contracts governed execution.

## Phase 2 — Candidate discovery

### What has happened so far

- The broad Overpass bbox sweep returned 3,128 food-service elements; filtering them against the saved isochrone retained 2,886 elements, 2,863 of them named.
- Targeted web searches have begun across quality, scratch, chef-led, recent-opening, cuisine, Spanish-language, marker-item, award, guide, and visible-head families.
- Early targeted searches exposed new or potentially OSM-missed formats including a private tasting table, food trucks/pop-ups, 2026 openings, relocations/reopenings, and specialist hand-roll, dumpling, pasta, tortilla, mole, and noodle venues.
- Completed the universal targeted families, a Spanish-language challenge, cuisine/format searches, every restaurant marker family, visible-head guide/award checks, and combined sub-area searches covering the principal restaurant-bearing metro components.
- Phase 2 froze a source union of **2,956 rows**: 2,886 broad-map rows plus 70 targeted/visible-head lead rows. Duplicates were deliberately retained for Phase 3.
- Full OSM tags and coordinates were preserved in reusable JSON; exact targeted queries, sources, result-page counts, and candidate-addition notes were preserved in the query log.

### Corrections the user needed to make

- The user added the per-phase diary requirement during this phase. No discovery-scope correction has been made.

### What had to be figured out that could be encoded in the skill

- The skill requires every universal query family combined with every relevant sub-area but gives no rule for a drive-time polygon spanning dozens of municipalities and neighborhoods. This run used a literal OR-list of the principal restaurant-bearing metro sub-areas so each family covered them without hundreds of near-duplicate searches. The skill should define whether this satisfies “combine with every sub-area,” and provide a partitioning/query-budget rule.
- The search tool returns a capped page of mixed results and does not expose the engine's estimated total count. The query log had to define “result count” as returned records on the inspected page. The skill should define this for capped search APIs.
- Search engines handled long OR-list sub-area queries poorly, often returning SEO service-area pages and irrelevant documents. The skill could require smaller sub-area batches when relevance falls below a threshold and define that threshold.
- The skill names OSM tags for restaurants, cafés, fast food, pubs, and bars but provides no executable supplemental source for food trucks, pop-ups, private dining, caterers, market stalls, or preorder operations. These were recovered opportunistically through targeted web results.
- The full isochrone bbox produced 3,128 Overpass elements and 2,886 polygon-internal elements. The skill gives no candidate-volume trigger for tiling, downstream worker batching, or feasibility reporting. This is likely the dominant execution problem for later phases.
- OSM supplied 23 unnamed food-service elements. The skill does not say whether unnamed map elements should remain candidates, be identity-repaired before Phase 3, or be excluded as non-venue geometry. They were retained because discovery cannot silently discard in-scope leads.
- The category-hygiene rule says primary bakery-cafés should route to the bakery skill, but Phase 2 forbids qualification/disqualification and does not specify when cross-category routing occurs. Bakery-like OSM cafés remained in the union for Phase 3 identity/category normalization.

## Phase 3 — Discovery convergence

### What happened

- Normalized names while retaining original spellings and OSM alias fields.
- Merged 5 co-located same-name OSM element duplicates within 40 meters and merged targeted provenance into 35 uniquely matched map identities.
- Kept distinct branches separate. There are 257 normalized-name groups with multiple branch or unresolved identity rows.
- Added 35 targeted identities not uniquely matchable to an OSM row and 11 genuinely new gap-pass identities; five additional gap leads merged into existing identities.
- Inspected geography, language/script, cuisine/tradition, service format, specialist/broad, and established/new coverage dimensions.
- Ran a fresh gap pass for informal/mobile/private dining, lunch/counter formats, underrepresented regional cuisines, and outer-suburb openings. After incorporating its additions, an identical full recent-opening pass produced zero new in-scope identities.
- Froze **2,927 canonical candidate IDs** for evidence research. This is source convergence, not a census claim.

### Corrections the user needed to make

- No new correction during Phase 3.

### What had to be figured out that could be encoded in the skill

- The skill requires comparison across name, address, coordinates, phone, domain, branch, aliases, and prior names but provides no deterministic matching hierarchy or distance tolerance. This run used normalized exact names plus a 40-meter co-location rule for OSM node/way duplicates and otherwise preserved ambiguity.
- Targeted web leads frequently named a brand or venue without a precise branch address. When multiple same-name OSM branches existed, the lead could not be safely assigned to one branch. The skill requires a shared brand packet but gives no canonical packet schema, whether packets consume candidate IDs, or how generic discovery provenance should attach to branch rows.
- The skill's mandatory candidate schema is too wide for a 2,927-row Markdown ledger. A structured JSON companion was created for lossless arrays and coordinates, while Markdown carries the canonical review table. The skill could explicitly authorize/require this pattern above a row threshold.
- OSM metadata is too sparse to populate specialist/broad and established/new reliably. The phase requires coverage inspection but does not say whether `unverified` cells trigger identity research now or remain for evidence workers. They remained unverified and gap searches addressed category-level suspicious cells.
- “Repeat until one complete pass yields zero” needed an operational definition. This run defined a complete convergence pass as the four outer-area/current-opening queries, reran the exact set after additions, and observed zero new identities.
- A phase-level convergence pass can reach zero while the broader candidate universe still changes daily. The skill correctly avoids a census claim, but could require a freeze timestamp and freshness horizon.

## Phase 4 — Evidence research (pre-dispatch correction)

### User correction

- The user clarified that the desired pre-evidence exclusion is **not fast food**. Informal and fast formats can be excellent and novel.
- The unwanted class is **low-novelty, highly standardized US chains**: businesses whose experience and menu are deliberately similar across a broad US footprint and which the user has almost certainly encountered already. McDonald's is the canonical example: acceptable food for its occasion, but outside what this rubric is trying to discover.
- This preference is explicitly **country-conditional**. It applies to a run in the United States and must not become a global anti-chain rule. In another country, a chain may be unfamiliar, culturally informative, locally distinctive, and capable of meaningful in-house production.

### Skill-design implication

- Add a pre-evidence **familiarity/novelty triage**, separate from scratch eligibility and format. Its reason code should be something like `US-standardized-chain-low-novelty`, never `fast-food`, `low-quality`, or `not-scratch`.
- The gate should rely on positive brand-scope facts: a broadly replicated US footprint plus strong menu/operating standardization. Service format, cuisine, price, popularity, or the word “chain” alone must not trigger it.
- Local mini-chains, chef-led restaurant groups, culturally distinctive regional chains, newly arrived foreign chains, and branches with documented store-local production should remain unless the user's familiarity preference clearly covers them.
- The rule must be disabled or recalibrated outside the United States. Novelty is relative to the diner's home market, not an intrinsic property of chains.
- Company-wide evidence should be researched once and referenced across branches. This simultaneously addresses the skill's current scale failure without pretending that branch count is evidence against scratch production.
- The current skill has no authorized phase for this triage. Applying it in this test run is a direct user override and should be represented explicitly in the run artifacts rather than silently folded into Phase 6 disqualification.

### Triage execution

- Applied a conservative exact-brand rule to the frozen US candidate set, with all affected IDs preserved in `03-user-novelty-triage.md`.
- Excluded **948 branches across 111 displayed brand spellings** under `US-standardized-chain-low-novelty`.
- Preserved **1,979 candidates** for evidence research. The original 2,927-candidate freeze remains unchanged for auditability.
- The reduction is substantial but still leaves roughly 132–198 canonical 10–15-venue evidence batches. This confirms that company-wide packet reuse and user-preference triage need to be first-class workflow concepts rather than ad hoc additions.

### Additional heuristic candidates discussed during Phase 4

- **Concept/branch collapse:** research a repeated concept once, then retain only the nearest in-catchment branch for the user's shortlist unless there is positive evidence of store-local menu or production variation. The revised evidence set contains 1,979 rows but only 1,702 normalized displayed names, so exact-name collapse alone could avoid roughly 277 redundant branch packets.
- **Positive non-restaurant cleanup:** remove permanently closed, not-yet-open, duplicate/ghost, private-event-only, catering-only, institutional cafeteria, drink-only, and retail-counter records after a cheap identity/access check. Do not use the OSM `cafe`, `bar`, or `fast_food` tag alone.
- **Access-friction preference:** separately flag airport-security, private-club, ticketed-resort, employee/institution-only, and event-only venues. These are not quality failures; they may be irrelevant to an ordinary drive-from-home dining request.
- **Meal-versus-treat preference:** optionally route primary bakeries to the bakery rubric and suppress drink-only, dessert-only, smoothie, snack, and candy concepts when the user asked for restaurants. Mixed cafes with meaningful savory cooking remain.
- **Cheap novelty screen before full evidence:** open the official menu/about page first. Advance immediately on any positive novelty signal (uncommon regional cuisine, specialist technique, house production, chef-led seasonal menu, unusual format, local variation). Defer a venue only when positive menu evidence shows an overwhelmingly standardized commodity template and no distinguishing feature was found. Missing pages or absent process language must remain unresolved, not excluded.
- **Familiarity memory:** a user-maintained “already tried / already know / never recommend” list is the most accurate novelty heuristic and should override brand-size proxies.
- Risky proxies rejected as hard filters: `fast_food`/`cafe` tags, burgers/pizza/tacos as product nouns, low prominence, missing process language, unfamiliar cuisine, counter service, and rating alone.

### User correction to the additional heuristics

- User accepted only: (1) concept/branch collapse, (2) positive non-public/non-operating record cleanup, and (3) ordinary-access filtering.
- User rejected the meal-versus-treat filter. Dessert, coffee, snack, or similar format is not itself outside the desired search.
- User rejected the cheap “novelty” screen because novelty is not the objective or the only positive signal. The actual target remains ambitious scratch cooking; novelty language distorted that objective.
- User judged a personal familiarity list unlikely to remove enough candidates to justify adding it to this run.
- Execution correction: rules 4–6 from the brainstorm will not be applied. Only rules 1–3 may reduce the evidence set, with explicit auditable reason codes.

### Execution of user-approved rules 1–3

- Started from the 1,979 candidates remaining after standardized-US-chain triage.
- Collapsed 266 redundant same-concept branches, retaining the geographically closest in-catchment representative when no store-local variation evidence was available.
- Removed 3 positively verified non-operating venue records: the closed Park City Coffee Roaster retail café, UGURT, and the closed downtown branch of Market Street Grill. Other operating Market Street Grill branches remained eligible before branch collapse.
- Removed 2 records positively described as private-chef/catering-only rather than ordinary public dining venues.
- Removed 28 venue points inside the Salt Lake City International Airport passenger-terminal/concourse cluster under the ordinary-access preference.
- Revised Phase 4 evidence set: **1,680 candidates**. The complete audit is `03-user-approved-heuristics-1-3.md`; the machine-readable set is `02-source-data/evidence-candidates-after-rules-1-3.json`.
- No meal-versus-treat, novelty, rating, cuisine, product-noun, service-format, or missing-evidence filter was applied.

### Random-sample study for additional cheap heuristics

- At the user's request, root researched a reproducible random sample of 20 candidates personally rather than delegating it to evidence workers.
- Sampling used the lowest 20 SHA-256 hashes with salt `cheap-heuristics-sample-2026-07-15-v1` from the 1,680-candidate population. This makes the ostensibly random selection reproducible and auditable.
- The detailed results are in `04-cheap-heuristics-random-sample-study.md`; the exact sampled records and hash keys are in `02-source-data/cheap-heuristics-random-sample-20.json`.
- Three further US-standardized-chain misses appeared: Great Steak, Burger Express, and Great Harvest. Exact brand-name lists are therefore insufficient. Official franchise pages, store numbers/location systems, rewards infrastructure, broad US footprint, and cross-location standardization should enrich the existing chain preference.
- Four records could not be confidently identity-resolved in one or two searches, and Boiler Room had a stale/mismatched address. A cheap identity/current-operation stage can defer these to identity repair without confusing missing evidence with exclusion.
- Cafe Anh Hong, Old Tbilisi Kitchen, Courchevel Bistro, and Olympian surfaced cheap positive local-production or chef evidence. A positive-production short circuit would stop elimination research and advance them; it would not substitute for the rubric's evidence gate.
- The sample produced repeated counterexamples to menu/category filtering: family-owned and scratch-signaling restaurants can have broad, generic-looking Chinese, diner, cafe, or fast-service menus. Configurable assembly menus are usable only as supporting evidence after an independent corporate-footprint finding.
- A foreign-origin franchise such as Ten Seconds Yunnan Rice Noodle confirmed the user's country-conditional warning: franchise or multi-location status alone cannot implement the US low-familiarity preference.

### What the skill could encode from this study

- Add a cheap pre-packet identity stage with three outcomes: exact current identity, identity-repair queue, or positively evidenced non-operating/non-public removal.
- Replace static standardized-chain name lists with a compound official-footprint test requiring both replication/footprint evidence and operating/menu-standardization evidence, while preserving foreign-chain and store-local-variation exceptions.
- Add an explicit positive-production short circuit: once direct evidence of substantial in-house production appears, stop trying cheap elimination heuristics and send the venue into the normal evidence workflow.
- State explicitly that menu breadth, generic names, familiar dishes, service category, weak web presence, configurability, and multiple locations are not standalone exclusion evidence.

### User correction after the first random sample

- The user noted that Great Steak, Burger Express, and Great Harvest are not common enough to create much workload reduction.
- More importantly, Great Harvest is relatively scratch-oriented for a chain. The first study conflated corporate replication with low scratch production too strongly.
- Correction: corporate-footprint detection can generate familiarity candidates, but it cannot establish low scratch production or exclusion. Prevalence and actual production must be considered separately.

### Second random sample of 20

- Root drew and personally researched a fresh non-overlapping reproducible sample using salt `cheap-heuristics-sample-2026-07-15-v2`.
- Results are recorded in `04-cheap-heuristics-random-sample-study-v2.md`; sampled IDs are preserved in `02-source-data/cheap-heuristics-random-sample-20-v2.json`.
- No persuasive common low-novelty national-chain exclusion appeared.
- The sample found a definite alias duplicate: R-1471 `Del Barrio Cafe` is the same Midvale concept as first-sample R-2910 `Cafe del Barrio`. Exact normalized-name collapse missed a word-order/name-variant identity despite official-domain and address evidence.
- The sample found a definite non-food record: Scion Cider's official site says it is a 21+ bar and welcomes outside food. This supports a positive food-substance check for ambiguous venue categories, never a category-only filter.
- The sample also produced strong counterexamples: Space Tea makes taiyaki batter and soft serve in house; Cliff documents many house-made components; Ooh Pho reports 20-hour in-house broth. Fast, drink-led, broad-menu, and new venues can all carry meaningful production signals.

### Skill-design implication from sample two

- Strong entity clustering—domain, phone, address/coordinates, token-set name comparison, aliases, and shared official pages—is more promising than predictive menu heuristics.
- Add a positive food-substance check for ambiguous categories, requiring explicit no-kitchen/outside-food/drinks-only evidence before removal.
- Separate three axes explicitly: corporate footprint, user familiarity/prevalence, and scratch production. None is a valid proxy for either of the others.

### Codeful fuzzy entity-clustering prototype

- The user proposed a high-recall algorithm that identifies possible clusters followed by a final orchestrator check. This cleanly separates cheap mechanical comparison from consequential identity judgment.
- Added `02-source-data/propose-identity-clusters.rb`. It normalizes names/aliases, phones, domains, addresses, and coordinates; blocks plausible pairs; computes token-set Dice similarity and geographic distance; and emits reviewable JSON without merging anything.
- The first permissive pass returned 344 pairs. Inspection showed that a shared domain alone was extremely noisy because hotels, resorts, restaurant groups, and generic web infrastructure can host distinct concepts.
- Tightened the proposal condition so shared domain/phone/address infrastructure requires name agreement, unless names independently match or a similar name occupies essentially the same place.
- The revised run produced **53 proposed pairs** from 1,680 candidates: 1 high, 44 medium, and 8 review. It successfully recovered the motivating `Cafe del Barrio` / `Del Barrio Cafe` pair.
- The decision vocabulary is `same-venue`, `same-concept-branches`, `different`, and `unresolved`. Even high-confidence proposals require primary-orchestrator review.
- Design and prototype results are documented in `04-fuzzy-entity-clustering-design.md`.

### What the skill could encode from the clustering prototype

- Phase 3 should require deterministic blocking/similarity code above a candidate-count threshold, followed by an auditable primary-orchestrator review queue.
- Shared domains, phones, addresses, or proximity must be treated as candidate-generation signals, not merge authority.
- The canonical relationship model needs to distinguish duplicate physical venue from same concept/different branch; a binary duplicate flag loses evidence-reuse opportunities.
- Require a noise inspection/tuning step. The 344-to-53 reduction showed that evaluating proposal precision before spending model tokens is essential.

### Final adjudication and application of fuzzy clusters

- The primary orchestrator reviewed all 53 proposed relationships.
- Decisions: 8 same-venue pairs; 28 same-concept branch relationships forming 27 connected concept clusters; 14 different/false-positive pairs; and 3 unresolved unnamed-OSM pairs.
- Verified through current sources that Baan Thai's Park City and Lehi records are branches of the same concept, and that Cafe El Barril moved from Sandy to South Salt Lake rather than representing simultaneous branches.
- Applied only reviewed same-venue and same-concept decisions. Same-concept clusters retained the branch geographically closest to the home origin; the verified Cafe El Barril relocation explicitly retained the current South Salt Lake location.
- Removed 36 redundant records. Phase 4 evidence population changed from **1,680 to 1,644**.
- Preserved all 14 false positives and all 3 unresolved relationships. Similar names, co-location, and shared domains never became silent deletion authority.
- Audit: `04-reviewed-identity-clusters.json`. Revised structured population: `02-source-data/evidence-candidates-after-reviewed-clustering.json`. Reproducible application script: `02-source-data/apply-reviewed-identity-clusters.rb`.

### Third random sample of 20

- Drew a third reproducible non-overlapping sample from the 1,644-candidate post-clustering population using salt `cheap-heuristics-sample-2026-07-15-v3`; root researched it directly.
- Full results: `04-cheap-heuristics-random-sample-study-v3.md`. Sample IDs: `02-source-data/cheap-heuristics-random-sample-20-v3.json`.
- No safe broad-format or chain exclusion appeared. The sample again produced counterexamples: a buffet with made-to-order sushi and frequent imported seafood, a boba-like fast format with preparation claims, a burger specialist serving Venezuelan food, and several family/single-location scratch signals.
- One of 20 was an unnamed OSM geometry rather than a researchable restaurant identity. It had survived into the evidence population despite already being part of an unresolved fuzzy pair.
- Several candidate domains were stale, misleading, or third-party rather than validated official provenance. Search engines can then attach an unrelated same-name restaurant's menu, a serious evidence-integrity risk.
- Caracas Dog appears to have current Caracas Grill branding at the same Woodbine address. This is a rebrand/identity repair case that pairwise clustering could not discover because no separate Caracas Grill candidate existed.
- Este Pizza and SLABpizza produced conflicting current-operation signals and belong in bounded identity/current-operation repair, not automatic closure removal.

### Skill-design implication from sample three

- Add a codeful pre-evidence identity-readiness validator. Required states: `ready`, `repair`, and `quarantine`.
- Unnamed map objects should be spatially identity-repaired before they count as evidence candidates. If unresolved, preserve them in quarantine rather than spending a restaurant evidence packet on an object ID.
- Validate a claimed official domain against name plus address/phone before accepting it as provenance. Domain presence is not domain correctness.
- Add current-name lookup for possible rebrands; fuzzy deduplication only compares identities already in the union.

### Phase 4 resumed in subagent research mode

- With the user's confirmation, resumed canonical Phase 4 evidence dispatch using the three existing evidence workers.
- Applied the proposed identity-readiness rule conservatively: 23 records whose names are only `Unnamed OSM food-service element ...` were quarantined from evidence packets pending spatial identity repair. They remain in the auditable population and were not disqualified.
- The ready named dispatch population is 1,621 of the 1,644 post-clustering records.
- Dispatched batches 004–006, 15 candidates each, with the restaurant Phase 4 canonical block copied verbatim and only catchment, access date, and candidate batch substituted.
- Batches 001–003 are preserved because they were dispatched before the user-directed population reductions; later reconciliation must count only candidate IDs surviving in the reviewed population and must not redispatch a surviving candidate that already has a usable return.

### Phase 4 wave 004–006 return status

- All 45 assigned candidates produced records after bounded continuations: batch 004 returned 11 then 4; batch 005 returned 4 then 11; batch 006 returned 15 directly.
- Batch 005 raw returns are saved in continuation files 2 and 3. Batch 006 is saved as `batch-006-evidence_batch_003.md`.
- Batch 004 initially existed only in worker messages despite the Phase 4 artifact requirement. A separate no-research persistence task was issued to concatenate its unchanged 11- and 4-candidate returns into `batch-004-evidence_batch_001.md` before the next dispatch wave.
- No semantic acceptance has been claimed; these are evidence-returned records only.

### Phase 4 wave restart and artifact-contract correction

- The batch 004 worker could not reconstruct its earlier 11-candidate return because that text existed only in the parent transcript. Root therefore dispatched a complete batch 004 redo rather than treating non-durable conversational content as accepted evidence.
- Dispatched batches 007 and 008 for 30 new named candidates while batch 004 is repaired. All three existing evidence workers are active.
- Root initially appended a persistence instruction to the canonical worker block, then immediately withdrew it because Phase 4 permits substitution of only catchment, access date, and candidate batch. The worker was explicitly told to execute only the canonical block.
- This exposes a skill-level contract gap: evidence must be durably saved, but the canonical prompt cannot instruct the worker to save it. The skill should encode a separate, mandatory post-return persistence operation and prohibit dispatching the next batch to that worker until the raw return is confirmed on disk.
- The ledger now distinguishes `evidence-returned` from `raw saved`; conversational returns alone do not count toward durable coverage.
- Batch 004's full redo completed with all 15 records saved, resolving the transcript-only artifact gap.
- Batch 007 reached 8 of 15 durably saved records through two bounded returns; its final seven-candidate canonical continuation was dispatched. The returns preserved address and branch conflicts rather than silently resolving them.
- Batch 008 returned all 15 records conversationally and immediately received a separate no-research persistence task, exercising the corrected two-step evidence/persistence workflow.
- Batch 009 returned a conversational partial with an internal count mismatch: it said eight processed, contained seven restaurant sections, and listed eight unprocessed candidates. Root requested unchanged persistence plus an external audit note; raw worker text must not be edited to hide return defects.
- The batch 009 worker cannot access its immediately preceding message for post-return persistence and did not create the separately requested working copy. Its transcript-only research is preserved conversationally but is not counted as durable acceptance; batch 009 requires a later durable redo.
- Batch 010 returned and persisted four sections plus an 11-candidate unprocessed list; the exact canonical continuation was dispatched.
- Batch 011 returned and saved four sections plus an 11-candidate unprocessed list. Repeated four-record cutoffs show that 15-candidate leaf batches are too large for some worker retrieval windows; the skill should recommend a smaller adaptive leaf size or require automatic bounded continuations.
- Batch 009 completed conversational research for all 15 candidates across 7-, 4-, and 4-section returns, but none was durably written. The worker was reassigned from new coverage to reconstruct the complete batch into a file, reopening sources as necessary. Transcript-only completion is not sufficient for later acceptance or scoring.
- Batch 010's 11-candidate continuation saved four more records, then a seven-candidate continuation made zero progress because its retrieval window ended. Root adapted both active continuations to four-candidate leaf batches. The skill should make leaf size responsive to observed worker throughput and treat zero-progress returns as a signal to shrink immediately.
- The same batch 010 worker then made zero progress on a four-candidate leaf and again on a one-candidate leaf. Because two other workers were still progressing, this was not a run-level blocker; the worker was moved to local coverage-audit tooling instead of consuming further external-retrieval turns.
- After a cooldown, the stalled worker recovered on two-candidate leaves. Batch 010 was repaired from 8/15 to 15/15 through durable 2-, 2-, and 1-candidate returns. This supports cooldown plus smaller-leaf retry before treating a worker as permanently unavailable.
- Batch 009 reconstruction reached 11 durable sections and continued with the final four. This confirms artifact repair is possible when framed as an explicit reconstruction with source re-opening, although it duplicates work and should be a fallback rather than the normal path.
- Batch 011 reached 12 saved sections after a four-candidate continuation; its final three were dispatched as a smaller canonical leaf.
- Batches 009, 011, 012, 013, and 014 are now fully durable. New dispatches 015 and 016 use four-candidate leaves, the first leaf size that both productive runtimes have repeatedly completed without continuation.
- The batch 013 worker still required a separate reconstruction pass after its canonical return, while the batch 014 worker saved during the evidence turn. This runtime-specific persistence mismatch remains the dominant avoidable duplication.
- The full batch 004 redo completed with all 15 records saved, resolving the transcript-only artifact gap without relying on reconstructed evidence.
- Batch 007 returned a durable 4-of-15 partial and explicitly identified 11 unprocessed candidates; the canonical prompt was immediately reissued for exactly those 11. Batch 009 was dispatched to the freed worker, so repair work did not stall new coverage.

### Phase 4 batch 028 — resort identity and seasonal-state conflicts

- Researched and durably saved all four assigned candidates: Libertango Steakhouse, Red Tail Grill, The Farm, and Bistro at Canyons.
- Libertango exposed unusually strong literal process wording on its official menu (wood/fire cooking, house-made pasta, sausage, sauce, empanada, and handmade croquetas), while its rating counts varied substantially across current aggregators. All literal conflicts were preserved.
- Red Tail Grill and The Farm demonstrated why resort restaurants need two separate time dimensions: published daily service windows and current seasonal operating status. Third-party directories showed year-round-looking hours while official resort material showed seasonal framing or closure.
- Bistro required an identity-continuity correction during research. Current search results route the old Bistro OpenTable URL to Prime At Canyon's, described as a “reboot,” at a different street number. Prime's production quotations were therefore recorded as successor/reboot evidence and not silently attributed to the historical Bistro record.
- No user correction was required during this leaf. The main fact that had to be figured out was that shared listing URLs and successor language do not establish menu continuity across a rebrand/reboot.

### What the skill could encode from batch 028

- For resort venues, require separate fields for `published recurring hours`, `seasonal operating status`, and `status date`; never let directory hours override an official “closed for the season” statement.
- Add a successor/reboot identity rule: evidence from a successor may document continuity or adverse identity facts, but its menu/process claims cannot transfer to the predecessor without an explicit same-kitchen/menu statement.
- Rating collection should preserve access-time count drift even within one platform-facing directory page; search-result count and opened-page count can differ on the same day.

### Phase 4 batch 031 — underspecified branches and archival ghosts

- Saved all four records. Tsunami arrived without an address and has at least two plausible in-catchment branches; evidence was kept branch-labeled rather than forcing a match.
- Beans & Brews showed that a chain can have genuine central production evidence (“roasts every bean”) while exact-branch food-production and rating evidence remain unavailable. Chain scale and production quotations were both preserved.
- Huckleberry Grill yielded unusually concrete official process wording: hickory cold-smoked, seared, sous-vide tri-tip; mushroom duxelles; port reduction; and a house-made romesco.
- Liberty Park Grill appears chiefly as an archival/directory ghost: an old menu PDF and 2022 directory record coexist with “May be permanently closed.” No current operation was asserted.
- No user correction was required. The key research correction was to stop an address-free brand candidate from absorbing evidence across branches.

### What the skill could encode from batch 031

- Identity readiness should reject or repair a multi-branch candidate lacking an address before evidence dispatch; otherwise branch-specific ratings, hours, and reviews cannot be canonicalized safely.
- Add an archival-ghost state for records supported only by old menus/directories plus possible-closure language. This is evidence provenance, not a scoring verdict.
- Chain status should be captured independently from central production facts; “multi-location” and “roasts every bean” are compatible literal facts that should not overwrite one another.

### Phase 4 batch 033 — format-neutral production evidence

- Saved four records. The buffet produced concrete made-throughout-day sushi and guest-customized Mongolian-grill evidence alongside adverse diner observations about holding temperature and sanitation; both were preserved without turning format into a verdict.
- Bandits supplied diner-observed wood-fire finishing and smoke intensity, including both favorable and strongly adverse execution reports.
- Red Corner's broad menu and family-owned claim were easy to recover, but no explicit staple/process claim appeared; delivery platforms supplied useful literal ratings and food-defect quotations.
- Pier 49's branch identity and ratings were recoverable, while its accessible sources did not substantiate how dough or sauce is produced. Praise for dough was retained only as product review evidence.
- No user correction was needed.

### Phase 4 continuation — second canonical-prompt transcription restart

- The first one-candidate R-2676 retry accidentally substituted noncanonical wording into required source-sequence item 2.
- The worker was interrupted immediately and restarted with the exact canonical prompt before its return could be accepted.
- No user correction was needed. This repeats the earlier evidence that manual prompt copying is error-prone; a generated, template-validated dispatch helper should be encoded in the skill.

### What the skill could encode from batch 033

- Buffets need explicit station-level retrieval: made-to-order grill/sushi evidence and hot-holding/replenishment evidence can coexist and should be captured separately.
- Health-related customer allegations must be labeled as diner reports unless an official inspection record is actually opened; mentioning a complaint does not establish agency findings.
- Product praise such as “great dough” must not be promoted into a production claim without explicit process language.

### Phase 4 continuation — durable-return reconciliation and adaptive throughput

- Batch 049 initially existed only in the worker transcript. A persistence-only follow-up saved the unchanged two-candidate return as `04-worker-returns/batch-049-evidence_batch_003.md`; the dispatch index now records it as returned.
- The dispatch index contained a duplicate pending row for batch 033 beneath its completed row. This was ledger duplication, not an additional dispatch, and was removed so exact-once coverage calculations do not falsely report an outstanding batch.
- Reliable throughput in this runtime remains below the skill's nominal 10–15 venue leaf size: four candidates per leaf for worker 002 and two per leaf for worker 003 have produced complete returns, whereas larger leaves repeatedly truncated. The skill could encode adaptive batch-size reduction after partial-return failures while retaining the primary-orchestrator-only batching rule.
- Unnamed OSM identity repair has resolved 7 of 20 reviewed records so far; 13 remain quarantined, and the final 3 records still require review. Identity repair is necessary before the canonical evidence prompt can be meaningfully applied, but Phase 4 does not define this pre-dispatch state or its completion semantics.
- Final unnamed batch review resolved R-2760 as La Autentica / La Autentica Taqueria. R-2850 remains quarantined because Papa John's and Big Hazy's share the 398 East Pages Lane address context without a geometry-to-suite link; R-2876 remains quarantined because no named current tenant matches the exact Parkway Drive footprint. Across all 23 unnamed records, 8 are now ready for evidence dispatch and 15 retain explicit identity-proof gaps.
- A concurrent worker appended its own batch number while the orchestrator was recording two other dispatches, producing duplicate batch 055 rows and a filename/ledger-number mismatch. The ledger was normalized to unique dispatch numbers without renaming or rewriting the raw worker return. The skill says the orchestrator assigns filenames, but the restaurant prompt lacks an output-path placeholder; a runtime-safe restaurant contract should include an orchestrator-declared unique output path, as the bakery contract already does.
- Worker 001 recovered from earlier retrieval exhaustion and completed a two-candidate leaf (batch 073) durably. Subsequent leaves for that worker were increased to two candidates; worker 002 remains reliable at four. This reinforces that adaptive batch sizing should be worker-specific and periodically re-probed upward after a stable streak.
- A local index/file coverage audit correctly caught batch 072's stale pending row after its durable return arrived. Automated reconciliation between the dispatch index, referenced files, and candidate IDs should be a required recurring Phase 4 control rather than an optional manual check.
- The R-0657/R-0658/R-0660/R-0662 canonical leaf was dispatched to worker 002 before its index row was appended; the omission was detected on the following continuation and backfilled as batch 098 before selecting new candidates. This is another argument for an atomic dispatch helper that writes the ledger row before sending the worker task.
- The later R-0673/R-0674/R-0675/R-0676 leaf repeated the same non-atomic dispatch/index omission and was backfilled as batch 102 on the next continuation. Batch 101 also produced useful transcript research but no complete durable record, so it remains a zero-return repair case rather than being credited from notes.
- Batch 106 repeated the transcript-without-durable-return failure for worker 001. Its two candidates were repaired by worker 002 in batch 108, and worker 001 was reduced to a one-candidate recovery probe. Adaptive sizing needs to respond to the worker's current reliability, not merely its historical best batch size.
- Nuan's Thai Kitchen exposed two additional identity hazards: a plausible exact-name domain can redirect to an unrelated business, and a restaurant move can leave old address/phone/domain combinations mixed into otherwise current directory records. The skill should require opening and validating claimed official domains, preserving redirects, and separately corroborating each current identity field while labeling old-location evidence historical.
- Nuan's also confirmed that “made fresh when you order” supports made-to-order preparation only; it does not establish that curry pastes, sauces, noodles, dumplings, or other components are produced from base ingredients. Platform-specific rating/count/date tuples were retained instead of collapsing conflicting crawl snapshots.
- A read-only durability audit found that many otherwise complete worker returns use restaurant-name headings without preserving the ledger candidate ID. Because the canonical prompt asks for `## [canonical restaurant name]` but not the ID, an automated file-to-ledger audit cannot distinguish a missing candidate from a correctly named section without doing a second fuzzy identity join. The worker contract should require an immutable candidate ID in every section heading or field.
- Donkey Tails showed that linked sibling-restaurant evidence can be relevant when the target's official page explicitly says the sibling's full menu is served there; that relationship must be quoted rather than inferred from co-location. It also exposed delivery-platform “closed” language that referred only to delivery availability, not venue closure, and a phone conflict resolved only by retaining both the candidate value and the matching official/state-license value.
- Donkey Tails' strongest process and seasonality evidence lived in Google Drive menu PDFs linked from official navigation, not in indexed page text. Phase 4 should explicitly follow and extract linked menu documents. Recurring weekday specials and a dish available “Oct - April” were kept as distinct turnover and seasonal evidence rather than collapsed into one signal.
- Worker 001 recovered after an audit cooldown when reduced to a single candidate and began writing its own durable ID-bearing returns. The recovery confirms that cooldown plus a conservative re-probe can restore useful capacity, but it does not justify immediately increasing that worker's batch size.
- Several later records reinforced domain validation as a required identity step: Jeeva's listed domain had been hijacked by unrelated gambling content, while Cutler Cookie Co. uses overlapping current family/location domains. Exact-name domains were opened and treated as evidence only after location and content validation.
- Cutler Cookie Co. demonstrated why historical process evidence needs an explicit date: a 2013 local profile documented scratch/handmade cookie production and daily volume, while current first-party language was much less specific. Independently family-owned locations share core recipes but vary menus, prices, and management, so process and menu claims remain location-bound.
- Black Sheep's image-based main menu and text-indexed specials showed that image-only menus and official specials can carry different evidence. Aggregator claims about bison/fry bread appeared contaminated by similarly named restaurants and were not merged into the West Jordan venue without location proof.
- Tinker's Cat Cafe supplied decisive first-party adverse production evidence (“All food items are made outside”) alongside named local suppliers. The skill should prioritize explicit off-site-production facts and preserve mixed attraction/cafe formats instead of assuming the restaurant is the venue's primary purpose.
- Water Moon required a pre-persistence correction when the worker noticed that two negative Restaurantji summary phrases were not literally present in the captured source text. Those phrases were removed before the durable artifact was credited. The worker contract should require quotation-to-captured-text traceability before return, especially for aggregator summaries, and the orchestrator should treat worker self-corrections as amendments rather than silently persisting the original transcript.
- Water Moon also showed two false-positive risks: “Autumn Roll” and “Xmas Roll” are standing item names, not proof of seasonal rotation, and “house special sauce” is a menu name, not proof of in-house sauce production. Season words and possessive/house labels need literal process or availability wording before they become evidence for those fields.
- Dasks' current HTML hours conflicted with an older official PDF. Current HTML was preserved separately and the PDF treated as time-bound evidence rather than allowed to overwrite it. A linked outside dessert vendor was likewise retained without inferring which listed desserts it supplies.
- Worker 003 failed two recent one-candidate leaves (R-0896 and R-0960) without producing an evidence packet; both were recorded as zero-return rather than credited from dispatch intent. R-0896 was subsequently repaired by reliable worker 002, and R-0960 entered the repair queue. The skill should encode a worker-health circuit breaker: repeated zero-output failures at the minimum leaf size should suspend new evidence assignments until a later explicit probe, with every failed candidate automatically requeued to a healthy worker.
- These failures also reinforce that an initial partial or narrative status is not evidence completion. A candidate becomes covered only when the required source sequence is represented in a durable return and the dispatch ledger points to that artifact.
- Worker 001 later entered the same minimum-leaf failure mode: R-0989 and R-0994 each returned 0/1 after a long reliable streak. R-0989 was immediately routed to worker 002, and R-0994 entered the next repair leaf; worker 001 was suspended after the consecutive failures. Worker health therefore needs both recovery and relapse semantics, not a one-time fixed reliability label.
- A read-only durability audit of dispatch rows 100–188 found no missing/nonempty-file failures, duplicate successful credits, stale pending rows with completed artifacts, or unusable successful file references. Keeping the audit separate from evidence retrieval let suspended workers contribute to control checks without treating them as healthy research lanes.
- The execution crossed midnight while Phase 4 was still running. The run retained its frozen `ACCESS DATE: 2026-07-15` instead of silently mixing retrieval-date semantics mid-population; the skill should state whether long-running continuation batches preserve a run-level access date or record the actual retrieval date per source. This test used the former because all existing artifacts and the canonical run identity were already anchored to July 15.
- After two audit cooldown tasks, worker 001 passed an explicit one-candidate recovery probe and then completed two further one-candidate leaves. This supports a circuit breaker with staged re-entry rather than permanent suspension after transient failures.
- Worker 002 encountered a model-capacity error before producing any evidence for R-1077–R-1080. The ledger stayed pending and the exact canonical batch was retried unchanged; the retry produced a complete durable return. Infrastructure-capacity failures should be distinguished from evidence-retrieval failures in worker health logic and should trigger an idempotent same-batch retry before batch-size reduction or candidate reassignment.
- A later capacity error on worker 001 arrived even though the worker had created the durable Ding Tea artifact before the error surfaced; the identical retry recognized the existing file and completed the ledger update without producing a second successful dispatch row. Capacity/error handling should first reconcile the expected output path and ledger state, then retry idempotently only if no valid artifact exists.
- While preparing dispatch rows 288–291, the orchestrator twice extrapolated contiguous candidate IDs across gaps introduced by reviewed filtering. Both pending rows were corrected before any worker received them, using the next untouched candidate objects from the canonical JSON ledger; the first correction also initially skipped real R-1351 because a lookup loop aborted on missing R-1350. A safe dispatch helper must select and serialize whole candidate records atomically; it must never manufacture the next batch by incrementing numeric IDs or let one absent lookup abort validation of later IDs.
- A conversational progress update reported 1,002 completions, but the authoritative unique-candidate-ID calculation from the durable index returned 1,000. The next sitrep corrected the number. Progress reporting should always run the canonical unique-ID coverage query immediately before stating a count; batch arithmetic and remembered counts are not reliable because repair rows, filtered ID gaps, and historical duplicate dispatches exist.

### User correction during Phase 4 — novelty, not fast-food format

- The user clarified that an early-removal heuristic should not target “fast food” as a format. Many fast-food restaurants can be good; the intended U.S.-specific shortcut is to skip **low-novelty chains** whose offering is highly standardized and which the user has almost certainly tried before.
- The user explicitly limited that assumption geographically: outside the United States, a chain may be novel and may do worthwhile cooking in-house, so chain status alone must not suppress it.
- This correction separates three independent facts the workflow should preserve: service format, chain/ownership identity, and user-relative novelty. None is a substitute for production evidence.
- The skill could encode a pre-research preference filter with an explicit locale condition and reversible “low novelty for this diner” reason. It should use known prior exposure and standardized ubiquity—not cuisine, speed, counter service, price, or chain status by itself—and retain an override path for chains with unusual local cooking or user interest.

### Phase 4 continuation — identity/format separation and dated-menu provenance

- The R-2243 record arrived under “Alpine Distilling,” while the current official venue identity is Park City Social Aid & Pleasure Club and a historical local identity is Alpine Pie Bar. The evidence return preserves all three names without assuming they describe identical food programs.
- Alpine’s menu is explicitly a light-bites accompaniment to a distillery/cocktail operation. This reinforces that bar format and a short food list are literal operational facts, not conclusions about how the listed foods are produced.
- Ruby River’s most detailed official process and prices were available only in a 2022 menu PDF. Those quotations were retained with their date instead of being presented as current prices, while current platform hours/ratings were kept separate.
- Bewilder’s official menu page provides unusually testable weekly process statements (cutting, grinding, casing, brining and patio smoking) and names its malt source. Trio combines a current explicit house-made brioche claim with a historical house-made-pasta claim; provenance dates prevent the older claim from silently becoming a current one.
- The skill could require an explicit `claim date/currentness` value beside every official-menu quotation and a `venue primary format` field separate from food-production evidence, especially for tasting rooms, cocktail lounges and breweries.

### Phase 4 continuation — chain/branch facts and literal frozen-item labels

- This leaf reinforced the user’s novelty correction: Java Jo’s, Ombu and Lucky’s have multi-location/sibling-location facts, but those facts coexist with distinct branch evidence and specific production claims. Chain status alone did not replace research.
- Ombu’s official site supplies a brand-wide daily house-made dipping-sauce claim, while its owner response says menus vary by location. The South Jordan record therefore preserves the brand claim and branch-specific “Frozen Meat Balls” label without transferring every menu fact across all six stores.
- Lucky’s candidate address used “Center Park Drive,” but all current sources use “Center View Way.” Branch identity repair should occur before scoring and should retain the supplied-vs-current address conflict.
- Java Jo’s exposes named packaged inputs and a reviewer-attributed bagel supplier, while accessible sources do not say who makes its other pastries. Named brands are useful literal sourcing/assembly facts but do not establish the entire production model.
- The skill could encode separate `brand-wide`, `branch-specific`, and `review-attributed` provenance scopes for every claim, plus a mandatory exact-address normalization check before evidence acceptance.

### Phase 4 continuation — isochrone-coordinate anomaly and co-located park stands

- All four address-free OSM candidates in this leaf resolve to food stands inside Lagoon Amusement Park at 375 North Lagoon Drive, Farmington. This conflicts with their discovery annotation “coordinate inside isochrone” for the East Millcreek 30-minute-drive catchment and should trigger a geometry/catchment recheck by the orchestrator rather than an evidence-worker verdict.
- Exact OSM-way identity was essential for Teriyaki Styx because current official Lagoon material no longer lists that name. The omission was preserved without being promoted to a closure claim.
- Olde Mill has both an OSM/historical spelling and a current official name, Old Mill Grill. Grandma Cristie’s similarly differs from current official “Grandma Christie’s.” Name normalization needs to preserve aliases instead of silently overwriting source identity.
- Park-level address, phone, hours and allergen statements do not automatically become stand-specific facts. This batch labels shared park context separately and records stand-level fields as exhausted-unavailable where appropriate.
- The skill could require coordinate-to-catchment recomputation for every address-free candidate before Phase 4 dispatch, plus explicit `parent venue` and `stand-specific versus venue-wide` provenance fields for amusement parks, food halls, stadiums and resorts.

### Phase 4 continuation — official redesign drift and branch-list conflicts

- Litzas’ current redesigned official site provides unusually clear process language and current hours but omits accessible prices. Currentness can vary field by field within one otherwise strong official source.
- Astro Burger’s address-free OSM feature resolved to the 39th & State branch, while the brand site says both “four locations” and “three locations” and lists neither that branch nor consistent hours for it. Branch-facing maps/reviews were therefore kept separate from brand-wide claims.
- SodaBoba’s listed domain did not provide usable current content, while Restaurantji explicitly labels the address closed and contains a one-review count conflict within the same page. Same-page literal conflicts should remain visible rather than being normalized away.
- Salt Lake Roasting shows another evidence-scope distinction: first-party identity as a roaster and grower relationships are current, while the accessible detailed food menu is archived and does not by itself establish current food-component production.
- The skill could require field-level currentness labels (`current`, `dated archive`, `status-conflicted`) and an internal-consistency check for official branch/location pages before transferring any brand claim to a candidate branch.

### Phase 4 continuation — food-truck dependency and nearby-branch closure contamination

- Umbrella Bar’s official description says “Food Truck Fare,” but accessible sources do not identify the truck/operator. A venue can sell/serve food without being the producer, so the external food provider should be treated as an unresolved identity dependency rather than inferred kitchen evidence.
- Market Street’s recent downtown closure appears prominently in search, while the Cottonwood branch remains current on official pages. Closure evidence must be location-bound; brand news cannot silently close a different branch.
- Market Street also exposed another address repair: the candidate says 2975 Cottonwood Parkway, while every current official source says 2985.
- Via 313’s live menu contained both “seasonal” and “monthly” special labels across crawl views, plus price drift between commission-free ordering and delivery. Literal channel/date provenance is necessary for prices and turnover.
- The skill could add an `external food operator` field for bars/taprooms/resorts and a mandatory location match before accepting closure, rating, price or process evidence from a multi-location brand.

### Phase 4 continuation — successor menus and inaccessible small-business evidence

- Myung Ga’s candidate identity is historical: the owners sold to Itto Sushi in 2023 and current sources display a combined Itto Sushi and Myung Ga operation. Current Japanese/sushi evidence was not silently attributed to the historical standalone restaurant.
- El Calor demonstrates an evidence-access floor: exact identity and one detailed Spanish complaint were recoverable, while the listed domain/menu/hours/process remained inaccessible. Missing indexed English evidence must not erase a small immigrant-business candidate or become a production conclusion.
- Hook & Reel provides clear chain/branch/hours evidence but little accessible base-production detail; seafood-boil customization describes service/cooking format, not who produces sauces or preps components.
- Asian Palace’s very broad cross-cuisine menu is a literal menu fact, while absence of broth/noodle production wording remains an unavailable field rather than a judgment.
- The skill could explicitly require local-language review queries and a `historical standalone / current successor-combination` identity state, keeping pre-sale and post-sale menu evidence separated by date.

### Phase 4 continuation — observed production timing and address delimiters

- Taqueria Fernandez’s candidate address contained a semicolon-delimited `499;497`; all current sources identify 499. Multi-value OSM address fields should be repaired before dispatch instead of passed through as one address string.
- Fresh Donut & Deli’s strongest process evidence came from customer observation of donuts being made for the next day, supplemented by business-info “fresh daily” wording. This is useful production-timing evidence but should retain its review/business-info provenance rather than become an inferred recipe.
- Best Chicken and Ribs has strong cooking-method observations (grilled, rotisserie, made to order) without explicit base-component claims. Cooking-to-order and component production remain separate evidence fields.
- Bruges demonstrates unusually complete first-party production/sourcing language: dough-based caramelization, daily hand peeling/made-to-order fries, in-house sauces, Belgian pearl sugar and a local bakery producing specified baguettes.
- The skill could normalize delimiter-contaminated OSM address values before Phase 4 and add a distinct `customer-observed production` provenance class alongside first-party process claims.

### Phase 4 continuation — historical process claims versus current operation

- Ab’s current official site combines a current menu with historical narrative about homemade pies from the 1951 Country Inn. The historical production statement was retained with its time scope and not transferred to today’s menu.
- Poplar Street provides a useful negative-input claim (“burgers never frozen”) alongside positive process claims (handmade pizzas, house vinaigrette) and recurring weekly/monthly specials.
- Mimi’s branch record shows that a national chain’s large menu and current ratings can be recovered while branch-level production remains unavailable; chain identity is context, not a substitute for component evidence.
- Nico’s demonstrates continued retrieval asymmetry for small operators: current press and high-volume ratings were available, but the Square menu/process/hours were not index-accessible.
- The skill could require every historical narrative claim to carry an explicit `historical-only` flag so founding-era production language cannot be mistaken for current practice.
## 2026-07-16 — Scratch-dessert corridor retrieval

- The user requested a subagent inventory of scratch dessert places already classified in Millcreek, Sugar House, 9th & 9th/9th South, and adjacent east-central neighborhoods.
- The existing `04-worker-returns/scratch-dessert-corridor-inventory.md` already matched that scope. It contains 12 qualifying places: seven dedicated dessert/bakery/cafe destinations and five restaurants with substantiated scratch dessert programs.
- Verification preserved a strict product-specific threshold. Nearby venues were not promoted merely because they are bakeries, display desserts, or make some savory components from scratch; six dessert-relevant candidates remain excluded because dessert production itself was not sufficiently established or was explicitly outsourced.
- No user correction was required during this retrieval pass. A useful skill-level encoding would be a reusable post-classification query/export step for filtering accepted venues by geography, product category, product-specific scratch evidence, and hours, since the current workflow makes this a manual artifact search.

### Phase 4 continuation — category contamination and brand-claim scope

- Karamba entered the candidate ledger as if it were a restaurant, but its current first-party site, government alcohol license and review corpus identify a nightclub/bar; no actual food menu was recovered. Phase 2 discovery needs a venue-type validation before expensive restaurant evidence work, while retaining ambiguous cases for review instead of silently deleting them.
- California Burgers and Millie’s illustrate the user’s novelty correction: counter-service burger format does not itself imply low novelty or low production effort. Both retained diner-attributed made-fresh/cooked-to-order evidence even though deeper component-production details were unavailable.
- Barbacoa’s strongest process language is brand-wide marketing about fresh, non-processed ingredients and guest-visible preparation. Those claims were not converted into branch-level proof that tortillas, salsas, beans or meats are produced in-house.
- California Burgers also exposed conflicting status evidence: a recent social rumor suggested closure while current directory hours/reviews suggested operation. The skill could require `venue type`, `food service verified`, `claim scope`, and `status confidence/conflict` fields before rubric scoring begins.

### Phase 4 continuation — stale geometry and item-specific manufacturing language

- Arella’s address-free OSM identity resolves to Bountiful, outside the stated East Millcreek catchment, and current platforms mark it temporarily closed. Address-free candidates need coordinate-to-current-address reconciliation and an isochrone recomputation before evidence dispatch.
- Trolley Wing’s Taylorsville branch similarly appears closed, with a planning document calling the site “previously Trolley Wing Company.” Current property/government evidence is more useful for status than an undated menu directory.
- Corner Bakery’s official material combines strong live-kitchen claims with item-specific labels that several sweets are manufactured in a facility. The two kinds of evidence must remain product-scoped; neither can be generalized to the entire menu.
- Blue Copper’s closure news applied only to its Marmalade cafe, not the 900 South Coffee Room. Multi-location closure matching and separate roastery-versus-cafe production scopes should be mandatory.
- The skill could add a pre-dispatch `current address + geometry + operating status` audit and require production claims to carry both location scope and product scope.

### Phase 4 continuation — operational format and parallel-menu scope

- Papa Murphy’s address-free, misspelled OSM record resolved cleanly to the 2100 South branch. Its defining fact is an uncooked, customer-baked product; the workflow should capture who performs final cooking separately from who produces or assembles each component.
- HandleBar maintains parallel animal-product and vegan menus, with explicit commercial substitutes alongside three named house-made components. Menu-path evidence should stay item-specific rather than turning a full vegan menu into a single production claim.
- Avenues Proper provides both general house-made language and concrete named house components, plus in-house beer and changing draft boards. The evidence model benefits from separating general venue claims, item-level claims and beverage-program turnover.
- Romano’s illustrates chain claim transfer: its menu and sourcing statements are brand-wide, while current branch identity/ratings come from branch platforms. The skill could require a `final cook location`, `parallel menu`, and `brand-to-branch transfer scope` field.

### Phase 4 continuation — baking location versus dough production

- Einstein’s official “fresh-baked every morning” claim coexists with a former-employee statement that dough arrives frozen. Baking location and dough-production location are separate facts and should never be collapsed into one bakery claim.
- China Chefs again exposes an address-free OSM geometry problem: the resolved venue is in Riverton and needs catchment recomputation before downstream use.
- Iggy’s record is historical and the current city map places a successor sports pub at its address. Replacement identity should be detected before spending a full menu-research pass.
- Carvers provides unusually concrete, product-specific evidence—hand cutting, house soups/BBQ sauce, eight-hour prime-rib roasting, daily fish variation and geographic ingredient claims—while exact hours/prices remain inaccessible.
- The skill could add separate `base-component production site`, `final transformation site`, and `successor venue at address` fields.

### Phase 4 continuation — commercial-input naming and domain collision

- Cotton Bottom’s official menu explicitly names Lamb Weston fries, Metro Deli ham and Nathan’s hot dogs while separately naming house chili and fresh ground-chuck patties. Commercial inputs and house components can coexist and must remain item-scoped.
- Rollz’s listed `freshrollz.com` produced search contamination from an unrelated San Francisco Freshroll with strong process claims. Exact address/phone matching must precede acceptance of any domain-level production statement.
- Proper Burger’s own group pages conflict between 857 and 865 Main Street. Even official internal address inconsistencies need preservation and repair.
- Kokopelli’s broad “makes food fresh” summary did not identify a produced component; adverse mold and service reports were retained as customer allegations.
- The skill could require domain/entity collision checks using address and phone, plus explicit commercial-input fields alongside house-component evidence.

### Phase 4 continuation — unresolved homonyms and food-service verification

- Sushirito could not be safely matched among several near-homonym businesses (Sushirrito, Zushirito and Sushi Burrito). A name-only OSM feature is insufficient for transferring any menu or closure fact.
- Sugar House Pub is current after a closure/ownership change, but accessible first-party evidence does not substantiate a regular food program beyond customized event menus. Restaurant discovery should verify recurring public food service rather than treating every bar as a restaurant.
- Toasters’ broad “fresh/local” description remained sourcing language because no named producer or component process was recovered.
- Tres Hombres provides detailed item composition but no accessible component-production wording; recipe ingredient lists and production claims need separate fields.
- The skill could require a `public recurring food service verified` gate and a homonym-resolution minimum of address, phone or exact official linkage before evidence attachment.

### Phase 4 continuation — diner freshness language versus production proof

- Vongole’s diners disagree: some describe fresh-tasting pasta while another explicitly compares tagliatelle to boxed pasta. Neither observation establishes production location, and no first-party pasta-making claim was recovered.
- The Dodo supplies unusually concrete pastry evidence: named pastry chef, onsite bakery, daily baking, twelve daily desserts and rotating specials. General restaurant claims were kept separate from this dessert-specific program.
- Sushi Groove’s strongest process phrase, “Fresh Cuts Daily,” comes from a dated 2012 local article and carries historical provenance rather than automatic current scope.
- Yanni’s “Fresh Cut Fries” is item-specific; menu breadth and longstanding family reputation do not extend that claim to pita, rice, sauces or meats.
- The skill could distinguish `sensory freshness review`, `customer-observed process`, and `operator production statement`, and require dated press claims to carry an explicit currentness flag.

### Phase 4 continuation — explicit reuse and oven-fuel precision

- Grub Steak’s chef profile explicitly documents use of meat scraps for meatloaf/burgers and transformation of overcooked prime rib into Cajun salad-bar bites. Reuse/upcycling facts should be preserved literally without automatic positive or adverse interpretation.
- Nomad East says all cooking happens in two large pizza ovens; reviewers call the pizza wood-fired, but the first-party text does not specify oven fuel. The workflow should distinguish equipment fact from review terminology.
- Caputo’s clearest preparation-location evidence is customer-attributed: turkey is not roasted onsite. A specialty market’s strong sourcing identity does not by itself establish deli-kitchen production.
- Billy Blanco’s and Grub Steak both resolve to Park City despite catchment annotations, adding to the address-free/stale-geometry audit backlog.
- The skill could include `reuse/upcycling process`, `equipment`, and `fuel source` as separate evidence fields, alongside mandatory catchment recomputation for Park City resolutions.

### Phase 4 continuation — beverage craft versus food-component evidence

- Tea Zaanti provides four explicit house-made food components while its 85-tea selection and knowledgeable service do not establish tea blending or processing onsite. Beverage selection, beverage preparation and ingredient production need separate scopes.
- Finn’s supplies unusually clear bakery language: breads and named pastries baked in-house from scratch every day. “Bakery” category alone, as with Red Moose, was not treated as equivalent evidence.
- Caffé Expresso and Red Moose expose rich beverage/review evidence but no roasting or baked-goods supplier facts; cafe quality observations do not identify production location.
- Tea Zaanti’s candidate phone was stale while current official/Restaurantji sources agree on a different number. Identity repair needs current first-party preference without erasing the supplied conflict.
- The skill could add distinct `roasts coffee`, `brews coffee`, `blends tea`, `bakes food`, and `retails sourced pastry` fields to prevent cafe evidence from collapsing into one production label.

### Phase 4 continuation — generic homemade wording versus enumerated processes

- Bricks Corner’s menu enumerates formula, proofing time, ovens and many house components, making claims directly traceable to products and transformations.
- Olympian’s “homemade meals” and family-recipe language is venue-wide and does not specify production for pita, soup, sauces or meats. Generic descriptor and enumerated process need separate evidence strength/provenance fields.
- Harbor combines a named Wagyu supplier, daily fish logistics, onsite garden and one explicit house-made dessert component. Sourcing/logistics and kitchen transformation should remain distinct.
- A search for Dee’s initially surfaced an unrelated Asian restaurant at `deesrestaurant.com`; exact address/domain validation prevented cross-entity menu contamination.
- The skill could automatically flag generic descriptors (`homemade`, `fresh`) for component follow-up and require address matching before accepting similarly named official domains.
## 2026-07-16 — Exhaustive classified-so-far scratch-dessert corridor audit

- Re-audited all currently durable Phase 4 Markdown returns as the candidate universe, without fresh general-web discovery, for Millcreek/East Millcreek, central Sugar House, 9th & 9th, 15th & 15th, and adjacent east-central neighborhoods.
- The venue universe remained stable. Eleven places have strong product- or program-specific dessert-production evidence. Hub & Spoke was separated into the plausible tier because its sole production wording is a third-party “homemade” description of donut holes. Six other nearby dessert-relevant venues remain insufficient or externally sourced.
- The new report adds a standardized dessert-type field, source/provenance, dedicated-versus-restaurant grouping, and explicit geography flags for All Purpose Bakehouse, Picnic Cafe, 'mina, and Salt & Olive.
- No user correction was required during this phase. The skill could encode a post-classification evidence export keyed by geography, product category, evidence source tier, and component-specific production language; this would avoid a manual full-return text audit for requests like this one.

### Phase 4 continuation — current contact conflicts and component gaps

- Mazza's submitted OSM phone and several platforms retain an older number, while the current first-party site displays a different phone. The return preserves both rather than silently normalizing to one.
- Mazza provides unusually direct first-party scratch, marination, braising, fresh-cut, twice-fried, and house-made vegan-meat language, plus reported in-house spice grinding. Those statements remain component-scoped despite the broad first-party scratch claim.
- The current official menu did not expose dessert items or production details, so no dessert-production inference was made from the restaurant's general scratch statement.
- No user correction was required. The skill could explicitly require a current first-party contact reconciliation step and prohibit extending a restaurant-wide scratch claim to unlisted categories such as desserts without category-specific evidence.

### Phase 4 continuation — dynamic rating surfaces and family-location scope

- Mi Ranchito Grill's direct Restaurantji page and its search surface exposed different rating counts and distributions on the same access date; both literal displays were preserved instead of selecting one.
- The official About page explicitly documents five family-managed locations and recipe consistency, which is a more precise ownership/replication fact than inferring chain status from shared naming.
- First-party evidence was item-specific: homemade corn chips, house salsa, lime cooking, deep frying, top-sirloin grilling, and fried-ice-cream assembly. A customer, not the operator, supplied the homemade-tortilla statement.
- No user correction was required. The skill could distinguish current direct-page values from search-index snapshots, and require ownership/replication facts to quote first-party location-count and control language when available.

### Phase 4 continuation — seasonal menu windows and branded pasta exceptions

- VENETO publishes unusually explicit calendar windows for spring and summer menus, alongside a seasonal tasting menu and a newsletter promise of first access to future seasonal menus. These facts make turnover directly auditable without inferring it from dish names.
- The current menu distinguishes homemade/fresh bigoli from a specifically branded Felicetti Monograno spaghetti dish and a gluten-free penne substitution. Production evidence therefore remains pasta-item-specific rather than restaurant-wide.
- Strong named-region ingredient detail coexists with only generic `finest local purveyors` wording; no named local farm, ranch, fishery, mill, or egg producer was recovered.
- No user correction was required. The skill could add structured fields for seasonal-menu effective dates and commercial pasta exceptions so both can be captured cheaply and without scope leakage.

### Phase 4 continuation — outside-food bars and event-food attribution

- Old Towne Tavern's clearest current food fact is Restaurantji's explicit statement that no food is made onsite and outside/delivered food is welcome. Other platform references to Costa Vida, wings, nachos, or car-show food cannot safely be converted into tavern-kitchen production.
- A customer described great food at an outdoor car-show/vendor event and then stopping inside for refreshments; the wording separates event food from tavern drinks and illustrates why event-food attribution must stay literal.
- Same-name taverns in several states heavily contaminated searches, making exact address/phone resolution necessary before using any menu evidence.
- No user correction was required. The skill could add an explicit `outside-food permitted / onsite kitchen denied` operational field and require event/vendor food to be attributed separately from venue production.

### Phase 4 continuation — broad operator claims and comparison wording

- Salazar's strongest operator-like text is a Restaurantji post stating homemade food made from scratch, but it provides no component or process detail. Customer tortilla wording is more specific but remains customer-attributed.
- A negative customer said a frozen dinner would have been better; this is comparative criticism, not evidence that the restaurant uses frozen dinners. The return makes that distinction explicit.
- The first-party domain is identified across platforms but was not retrievable, while a municipal publication supplies current identity, hours, and broad homemade wording.
- No user correction was required. The skill could explicitly separate comparative frozen/premade language from factual product claims and distinguish broad operator claims from component-level production evidence.

### Phase 4 continuation — process-like dish names and customer premade impressions

- New Golden Dragon's official menu contains many process-like dish names—baked, steamed, fried, salt-baked—but no claim that wrappers, buns, noodles, sauces, or stocks are produced in-house. Item labels were preserved without extending them into component production.
- A delivery customer said shrimp seemed premade rather than hand-dipped; this remains a customer impression, while a separate customer provided concrete doneness and gristle allegations for several dim-sum items.
- Weekend dim-sum timing differs by 30 minutes between the official menu and a customer/platform summary; the first-party 2:30 endpoint and review 2:00 endpoint were both retained.
- No user correction was required. The skill could distinguish process-named dishes from component-manufacturing claims and tag premade/frozen statements as operator fact, observed physical evidence, or customer impression.

### Phase 4 continuation — bakery/store production split

- Thirst documents a two-stage production model: cookies and Scotcharoos are made from scratch at its bakery and baked daily at stores, while store teams roll/cut/bake pretzels and rise/fry beignets. This is more precise than a binary house-made field.
- Pretzels carry explicit never-frozen wording, whereas the menu separately sells frozen-fruit drink add-ins and a customer describes personally freezing purchased goods; these distinct scopes must not be conflated.
- The drink program openly assembles commercial branded bases with syrups, purées, creams, fruit, citrus, and ice cream, alongside a weekly rotating feature.
- No user correction was required. The skill could encode staged central-production/store-finishing workflows and require frozen claims to attach to the exact component and actor.

### Phase 4 continuation — canonical-prompt transcription restart

- The first R-2527 dispatch accidentally collapsed spaces in the canonical `No S, I, E, G, G′` prohibition line.
- Because Phase 4 requires the initial worker prompt verbatim, the worker was interrupted before completing research and the leaf was restarted with the exact canonical text.
- No user correction was needed. The skill could ship a small prompt-rendering/validation command that substitutes only the three allowed placeholders and verifies the resulting prompt against the canonical template before dispatch, eliminating manual transcription risk.
### Phase 4 continuation — evidence asymmetry and historical/current separation

- Processed R-2550 Sushi Burrito on 8th, R-2552 HSL, R-2555 Blue Gene’s, and R-2562 Beer Bar as an evidence-only leaf batch.
- HSL’s official pages were unusually rich: the current menu, about copy, press archive and a first-party PDF collectively exposed frequent menu change, preservation/fermentation, local-regional sourcing and named ingredients. This reduced reliance on generic marketing language.
- Blue Gene’s demonstrated why the retrieval template needs a bar-food check: its current first-party menu literally contains only Cup Noodles, Tim’s Chips and a hot dog, though old reviews mention food no longer shown. I kept the current menu separate from historical review facts.
- Beer Bar’s current menu is image-only and its address/phone conflict across the candidate record, official site and directories. Historical opening coverage contains strong sausage-making detail, but it cannot safely be restated as current. The skill could explicitly require labeling every process quotation `current`, `dated historical`, or `date unknown`.
- Sushi Burrito has two apparently first-party ordering domains with the same address and phone. Review-count conflicts were preserved verbatim rather than reconciled.
- No user correction was needed during this continuation. The main correction I had to make internally was to distinguish the run’s nominal 2026-07-15 access date from the actual 2026-07-16 retrieval date and state that discrepancy explicitly.
### Phase 4 continuation — inaccessible menus and source-role labeling

- Processed R-2570 Francesco’s, R-2571 Veggie House, R-2575 BIG Willies, and R-2576 El Menos as raw evidence only.
- El Menos exposed a highly detailed current text menu with explicit house-made tortillas, chips, aguas frescas and tomato juice plus weekend-only soups and seasonal ingredients. Its candidate identity differed from the official name/address by both spelling and street number; both were preserved.
- Francesco’s and Big Willies use image/linked-menu structures that did not expose current text. Third-party archived menus and customer process claims were labeled by source role and were not presented as current first-party production facts.
- Veggie House’s supplied domain was not text-accessible. The evidence therefore came from delivery/menu/review sources; this makes the unavailable-field and search-trail discipline important.
- The skill could encode a compact source-role tag for every quotation (`official-current`, `official-dated`, `third-party-menu`, `critic`, `customer`) because the distinction repeatedly controls what may safely be claimed.
- No user correction was needed during this continuation.
### Phase 4 continuation — direct process language across bar, diner, and seasonal restaurant

- Processed R-2583 Aces High Saloon, R-2584 Sweet Lake, R-2586 Ruth’s Diner and R-2587 Emigration Brewing as raw evidence.
- Aces High’s official menu directly exposes 12-hour carnitas, house marinade/demi-glace/tomato soup and Vegan Daddy seitan.
- Ruth’s current dated PDF exposes in-house smoking, fresh-baked quiche, fresh-made bread and roasted turkey; outside critic language was kept separately attributed.
- Emigration Brewing states an unusually exact turnover cadence: four seasonal menus plus monthly specials, along with wood-fired ovens and local/regional grower partnerships, but does not name growers.
- Sweet Lake’s supplied official domain did not yield indexed text; production therefore remains unavailable despite extensive menu/review coverage.
- The skill could explicitly encourage preserving exact rotation cadence separately from generic seasonality language.
- No user correction was needed.
### Phase 4 continuation — missing official domains and review-only process gaps

- Processed R-2592 Rawbean, R-2593 Millcreek Cafe, R-2599 Koyo and R-2601 Seafood Bucket as raw evidence.
- Three candidate records lacked official domains. Directory research recovered probable domains/phones, but only source-accessible identity facts were asserted; inaccessible/historical domains were labeled.
- Rawbean, Millcreek Cafe and Koyo exposed menu/review facts but almost no first-party production or sourcing language. Seafood Bucket exposed a detailed current menu but only cooking-format words, not component provenance.
- The skill could add an identity-recovery branch for candidates without domains: exact address + phone search, state license lookup, then historical-domain verification.
- No user correction was needed.

### Phase 4 continuation — near-homonym identity quarantine

- The submitted `Mana Thai Diner` record resolves through its exact phone and street address to current `Mano Thai Diner` at 41 W 3300 S, ZIP 84115; the submitted ZIP 84123 and spelling were retained as source errors rather than silently normalized.
- Search results were heavily contaminated by a distinct `Mana Thai Cafe` at 2821 S 2300 E in Millcreek. Its Axios coverage, menu evidence, and production claims were excluded from the Mano Thai return.
- The official domain exposed no usable menu/about text. A restaurant-authored Tripadvisor About passage supplied cuisine orientation and chef tenure, but its broad freshness wording did not establish curry-paste, sauce, stock, noodle, wrapper, or dessert production.
- No user correction was required. The skill could require an exact phone/address identity lock plus a near-homonym quarantine before attaching menus or press, especially when one spelling variant has stronger search visibility than the submitted business.

### Phase 4 continuation — component-scoped house-production language

- Hog Wallow's current first-party menu exposes unusually specific but component-scoped process evidence: wood/house-smoked meats, freshly ground branded beef, and house-made salsa, hummus, pimento cheese, dressings, and sour mix.
- The same menu also openly names commercial components such as Impossible Burger, Ritz crackers, branded spirits, and packaged beer. Both sets of facts were retained without generalizing either across the whole menu.
- The menu distinguishes a noon–10PM main window, a 10–11PM late menu, and bar hours through 1AM; venue hours alone would overstate food availability.
- No user correction was required. The skill could require every production claim to attach to an exact component and could separately capture kitchen/menu hours versus venue hours.

### Phase 4 continuation — current-team and historical-chef separation

- Log Haven's current first-party page names Todd Hoffee as chef and Dave Jones as culinary advisor, while OpenTable still labels Jones executive chef. A detailed 2015 Jones interview therefore remains historical evidence rather than a current production claim.
- The current menu directly labels daily house-made ice creams and sorbets and several other house components; separate menu technique words were retained without assuming where those components were produced.
- Hours conflict even within the official dining page: its body says nightly dinner begins at 5:30, while its footer says weekdays begin at 5 and also exposes weekend brunch. All literal windows were preserved.
- No user correction was required. The skill could require role-and-date binding for chef interviews and flag internal first-party contradictions between page body, footer, structured data, and reservation widgets.

### Phase 4 continuation — owner responses as scoped production evidence

- Yellowfinn's current official menu supplies detailed dish construction but little component provenance. A current owner response to a rice complaint provides the narrow statement that its sushi rice is made fresh daily; it was retained without broadening it to fish, sauces, dashi, noodles, or gyoza.
- A 2010 report documents service-time roll construction and allergen-station sanitation, but its parent-restaurant and staffing facts were labeled historical rather than current.
- The official lunch schedule contains a malformed midnight rendering that conflicts with its clear 11:30AM–3PM heading. Both literals were preserved rather than silently repairing the embedded schedule.
- No user correction was required. The skill could treat verified owner responses as first-party evidence with exact component scope, while separately flagging malformed structured hours for review.

### Phase 4 continuation — closed entertainment venue with historical kitchen

- Golden Axe lacked a submitted phone/domain. Historical opening press, city licensing, and exact-address directories recovered its former phone and domain, while current aggregation marks it permanently closed.
- Food evidence was limited to a historical short bar/grill list and customer reports that the kitchen was closed on two 2019 visits. No detailed menu or production wording was retrievable from the defunct domain or image-only archived menus.
- Historical opening hours conflict substantially across the opening calendar, Tripadvisor, and a local guide; current closure status was kept separate from all former hours.
- No user correction was required. The skill could add an early closure/defunct-domain branch that recovers historical identity and menu facts but prevents them from being interpreted as current operations.

### Phase 4 continuation — venue hours versus food-service windows

- Barbary Coast's current official menu exposes separate food hours, weekend breakfast/brunch windows, and recurring weekday specials; review platforms list later daily closing times for the overall bar.
- First-party production language is narrowly scoped to several housemade dressings. Restaurantji's `fresh cut fries` wording was retained as platform summary evidence rather than promoted to first-party fact.
- The current menu openly lists many commercial-style or breaded bar components without saying whether they are purchased, frozen, or produced on site; item type alone was not treated as provenance.
- No user correction was required. The skill could require separate `venue hours`, `kitchen hours`, and `special-service windows`, plus source-role labels on every production phrase.

### Phase 4 continuation — bar identity without attributable food evidence

- The Pines SLC is permanently closed and its property is now listed for sale as a turn-key bar. Historical owner coverage and public records recovered the phone, LLC/DBA identity, group ownership, and former Tinwell lineage.
- Search aggregators exposed generic food-category links, but no attributable food menu or underlying review text. Those links were quarantined rather than treated as evidence that the bar operated a kitchen.
- Historical evidence supports cocktails, beer, events, games, DJs, and outdoor seating, but no cocktail ingredient or production details survived in retrievable text.
- No user correction was required. The skill could require source-backed menu-item text before treating aggregator `tasty dishes` or category links as venue-level food evidence.

### Phase 4 continuation — chain-wide claims versus location scope

- Taqueria 27's official About page makes chain-wide production, supplier, and daily-special statements, while the location page confirms that Lehi is one of five operating venues with its own culinary team.
- The shared current menu identifies specific house-made/fresh-cooked components. A more specific house-smoked pork-belly description appeared on the Downtown ordering page, so it was labeled Downtown-specific rather than silently transferred to Lehi.
- Hours conflict across the current official page and review aggregators, and the shared menu contains brunch items explicitly limited to Downtown and Eagle Mountain; location exclusions matter when attaching a shared menu.
- No user correction was required. The skill could require every multi-location claim to carry a scope tag (`group-wide`, `shared-menu`, `location-specific`, or `other-location-only`).
### Phase 4 continuation — branch specificity and testimonial leakage

- Processed R-2612 Mr. & Mrs. Crab, R-2614 Porcupine, R-2616 Lorena’s and R-2798 Rancherito’s as raw evidence.
- Multi-location sites repeatedly surfaced chain-wide menus, testimonials and hours that were not branch-specific. Those facts were labeled chain-wide or excluded from branch fields.
- Rancherito’s Redwood branch URL redirected to the homepage; exact-address searches surfaced a Riverton Redwood Road branch, which was excluded.
- Lorena’s identity was recovered through its inaccessible official domain plus state licensing and directories; a customer’s “frozen burrito” comparison was preserved without converting it into a factual frozen-product claim.
- The skill could explicitly warn that review similes/comparisons are not operational evidence and require branch-specificity tags for chains.
- No user correction was needed.
### Phase 4 continuation — concession identity and recovered-domain uncertainty

- Processed R-2631 El Cabrito, R-2635 Lagoon Biergarten, R-2638 High Point Coffee and R-2643 Mad Greek as raw evidence.
- Lagoon Biergarten was verified as an amusement-park venue at 375 Lagoon Drive; its OSM record lacked address/phone/domain. No standalone official page was found, so menu/critic/directory roles were explicit.
- El Cabrito had several recovered domain candidates but none text-accessible; handmade-tortilla wording remains directory/review evidence.
- High Point official home verifies identity but exposes little menu/process text. Mad Greek similarly relies on directories/reviews.
- The skill could add a concession/venue-parent identity field so restaurants inside parks, stadiums and markets are clearly tied to their operator.
- No user correction was needed.
### Phase 4 partial continuation — retrieval-window boundary

- Completed raw evidence for R-2661 Nuevo Machetes only.
- R-2662 Mariscos Ensanada, R-2676 Mom's Cafe and R-2682 Thieves Guild Cidery remain unprocessed and are explicitly listed for reassignment.
- Nuevo Machetes demonstrates why customer frozen/reheated allegations must remain attributed claims rather than operational facts.
- No user correction was needed.
### Phase 4 partial continuation — Mariscos identity recovery

- Completed R-2662 Mariscos Ensenada; recovered exact address/phone through restaurant and state-license sources.
- R-2676 Mom's Cafe and R-2682 Thieves Guild Cidery remain unprocessed for reassignment.
- No user correction was needed.
### Phase 4 continuation — coordinate-only indoor cafe identity

- Completed R-2676 Mom's Cafe as a sparse raw-evidence return.
- Exact phone/coordinate searches recovered only OSM-derived map directories: name, phone, coordinates, partial hours and `indoor=room` / no-drive-through attributes.
- No menu, official page, operator, rating or review could be tied to the identity; every unavailable field includes the searched source sequence.
- The skill could add a branch for `indoor=room` POIs, which may be institutional or building-interior cafes with little public web presence.
- No user correction was needed.
### Phase 4 continuation — beverage production versus external food provision

- Completed R-2682 Thieves Guild Cidery as raw evidence.
- Official menu explicitly separates house beverage/pickle production from a three-item light-snack list and rotating external food trucks.
- Named apple varietals and local beverage producers were recorded, while absent orchard and fermentation details remain unavailable.
- The skill could add a taproom-specific distinction between onsite beverage production, onsite food production and external food-truck provision.
- No user correction was needed.
### Phase 4 partial continuation — Prime process evidence

- Completed R-2706 Prime Steak House and Piano Bar; official source exposed custom aging, 1800-degree broiling and hot-plate service.
- R-2707 Warrens, R-2709 Millcreek Inn and R-2715 Tacos El Pariente remain unprocessed for reassignment.
- No user correction was needed.
### Phase 4 continuation — coordinate recovery for multi-location fast food

- Completed R-2707 Warrens; OSM coordinates matched the Plain City branch through map and municipal-license sources.
- Official sources exposed hand-spun shakes, daily home-cooked breakfast and a local-supplier policy, but no supplier names or component-production details.
- The skill could add municipal business-license records as an identity source for coordinate-only candidates.
- No user correction was needed.
### Phase 4 continuation — private-event venue recovered from an OSM restaurant candidate

- **Candidate:** R-2709, Millcreek Inn.
- **What happened:** The coordinate-only OSM candidate resolved to the official Millcreek Inn at 5802 East Mill Creek Canyon Road. The official site describes it as a private wedding/event/banquet facility and explicitly says it does not attend to restaurant guests. Its current discoverable food evidence is a detailed official 2024 event packet with plated, brunch, buffet, themed, reception, dessert and beverage packages.
- **Corrections from the user:** None during this leaf.
- **What required figuring out:** Restaurant-shaped discovery records can represent a food-producing private-event venue rather than public meal service. The evidence return therefore had to distinguish office hours and event windows from walk-in restaurant hours, and preserve package prices rather than treating them as ordinary menu prices. Rating sources also conflict materially: the official badge, WeddingWire, WeddingWire's embedded Google summary, Chamber and MapQuest/Yelp each expose different counts or values.
- **What could be encoded in the skill:** Add an identity/format branch for private caterers, banquet facilities and wedding venues discovered as restaurants. Require workers to record whether public walk-in dining exists; distinguish office, event and meal-service hours; preserve per-person package pricing and food/beverage minimums; and keep embedded third-party rating summaries labeled separately from direct-platform pages.

### Phase 4 continuation — historical freshness versus current production

- **Candidate:** R-2749, Virg's Fish & Chips.
- **What happened:** The official domain was recovered through current directories but exposed little usable text. A recent owner-uploaded Restaurant Guru menu supplied detailed current-ish items, prices and limited process wording. A 2008 exact-location critic report described fresh/moist cod or halibut and crunchy fish, but that dated observation cannot establish current fish sourcing or handling.
- **Corrections from the user:** None during this leaf.
- **What required figuring out:** Two business histories conflict on the founding and ownership-transition years (`1963`/`1991` versus `1981`/`1990`), so both were preserved rather than reconciled. The retrieved menu was operator-uploaded on an aggregator rather than hosted on the live official site and was labeled accordingly.
- **What could be encoded in the skill:** Require freshness and process evidence to retain its observation date and current-applicability scope. Add an explicit source class for owner-uploaded aggregator menus, distinct from live first-party menus, and require unresolved business-history conflicts to remain visible.

### Phase 4 continuation — historical lounge replaced at the exact address

- **Candidate:** R-2776, Bill's Lounge.
- **What happened:** The OSM candidate resolved to a historical Magna lounge established in 1964. Historical directories and an obituary recovered its identity, while a corporate-record mirror displays an expired 2011–2014 LLC and a government record documents activity in 2013. Current exact-address sources consistently identify Main Street Grill instead.
- **Corrections from the user:** None during this leaf.
- **What required figuring out:** Current ratings, menu and hours at the exact address belong to Main Street Grill and could not be transferred to Bill's Lounge. They were retained only as evidence of an address-level identity change. Search results also mixed in unrelated businesses with the same generic name and were excluded.
- **What could be encoded in the skill:** Add an exact-address successor-business branch: record the historical candidate separately, use current occupant evidence only to document identity turnover, and prohibit transferring successor ratings/menu/process evidence. Generic-name candidates should require address corroboration before any evidence is accepted.

### Phase 4 continuation — collision-prone short name and founder-process tense

- **Candidate:** R-2786, O-Ku Sushi & Poke.
- **What happened:** The coordinate-only short name resolved to the Sandy restaurant through official and Utah-license sources. Searches also surfaced a multi-state O-Ku group and an O-Ku Sushi & Ramen in Roy; both were excluded after address/phone corroboration. The Sandy official About page supplied unusually specific rice, Norwegian salmon, founder-preparation, sauce and robot-service statements.
- **Corrections from the user:** None during this leaf.
- **What required figuring out:** The About narrative shifts between opening-period past tense (`chose and prepared all of the ingredients myself`) and present tense (`I also prepare sauces by myself`). The evidence return preserves those tenses instead of generalizing the opening-period claim into a current all-component production fact.
- **What could be encoded in the skill:** For collision-prone short names, require address/phone or government-record corroboration before accepting evidence. Process quotations should retain tense and subject, distinguishing founder-era startup practices from explicit present-day practice.

### Phase 4 continuation — image-only official menu and dated local process reporting

- **Candidate:** R-2819, Hook & Ladder Co.
- **What happened:** The official Weebly site was current and identity-matched but exposed its menu only through images with no useful text. Current menu/rating platforms supplied menu structure and prices; a detailed 2015 SLUG profile supplied founder history and dated process/sourcing observations.
- **Corrections from the user:** None during this leaf.
- **What required figuring out:** Search surfaces exposed an unrelated domain as the website on one directory, while the consistently linked Weebly site matched the restaurant. Dated critic wording such as homemade fry sauce and local-distributor English chips was retained with date/source rather than promoted to current first-party fact.
- **What could be encoded in the skill:** Add an image-only official-menu branch that allows current structured menu platforms to supply transcription while preserving source class. Require dated critic process/sourcing claims to carry date and observer attribution, and treat directory-displayed domains as unverified until identity-matched.

### Phase 4 continuation — merchant ordering page without a standalone official site

- **Candidate:** R-2839, Golden Gyros.
- **What happened:** No identity-matched standalone site was recovered; the obvious domain belonged to a Wisconsin namesake. Current DoorDash and Grubhub merchant pages supplied extensive menu, price and limited production wording, while a Salt Lake City business list corroborated the 2020 identity.
- **Corrections from the user:** None during this leaf.
- **What required figuring out:** The ordering menu's `Our homemade marinara sauce` is merchant menu wording, while cooked/made-to-order statements came from customers and had to remain attributed. DoorDash's broad `freshest ingredients` marketing sentence was preserved literally without converting it into a component-level process fact.
- **What could be encoded in the skill:** Add a merchant-controlled ordering-page source class for restaurants without standalone sites. Distinguish merchant item descriptions, merchant marketing blurbs and customer review claims, and require exact-name domains to pass address/phone collision checks before being treated as official.

### Phase 4 continuation — seasonal attraction concession without outlet-level reviews

- **Candidate:** R-2848, Pirates Grill.
- **What happened:** The coordinate-only record resolved exactly to Cherry Hill Water Park's Pirates Grill in Kaysville. The park's official page supplied a complete concise menu, prices, summer/weather-dependent hours and explicit fire/flame-grilled cooked-to-order wording. Direct rating platforms did not expose a concession-specific listing.
- **Corrections from the user:** None during this leaf.
- **What required figuring out:** Park-wide ratings and reviews could not be transferred to an individual food outlet. Numerous strong same-name results belonged to Florida, Australia, Cayman, Alabama and other countries and were excluded through coordinate/address matching.
- **What could be encoded in the skill:** Add an attraction-concession branch: preserve seasonal/weather-dependent operation, use parent-venue contact data when the outlet has none, and prohibit transferring parent-attraction ratings/reviews to the concession. Generic concession names should require coordinate-level corroboration.

### Phase 4 continuation — customer packaging/holding allegations versus operator facts

- **Candidate:** R-2865, China Platter.
- **What happened:** The official site was a sparse identity/hours landing page. Merchant ordering pages supplied broad current menu grammar and a dated 2022 lunch menu; family ownership/history was recoverable through a 2009 KSL profile and merchant About text. Reviews included unusually specific packaged-patty, held-chicken, stale-noodle and burnt-item allegations.
- **Corrections from the user:** None during this leaf.
- **What required figuring out:** Customer wording that egg-foo-young patties `appeared to be packaged` and chicken seemed previously cooked/held is physical evidence but not an operator production admission. These claims were retained with attribution and not promoted into premade/holding facts.
- **What could be encoded in the skill:** Add explicit handling for customer packaging, reheating and holding allegations: quote the sensory/physical basis, preserve hedging such as `appeared` or `seemed`, and prohibit rewriting it as a confirmed operational method without corroboration.

### Phase 4 continuation — reopening creates an evidence-era boundary

- **Candidate:** R-2884, Grove Market and Deli.
- **What happened:** The business closed after longtime owner Jim Savas died, was sold in December, and reopened February 14, 2026. Current sources expose a new phone and broader hours, while Tripadvisor/Apple Maps retain the old phone/hours. Menu archives and most reviews span the previous operation.
- **Corrections from the user:** None during this leaf.
- **What required figuring out:** A June 2024 report of a premade display-cooler sandwich belongs to the pre-sale operator; a May 2026 report of changed bread/avocado/cheese belongs to the reopened operation. Aggregated ratings span both eras and cannot be partitioned from the displayed totals.
- **What could be encoded in the skill:** Add a reopening/ownership-change evidence boundary. Require every menu, process, review, phone and hours fact to be tagged pre-change, post-change or mixed/undated; prohibit carrying production allegations across the boundary; and flag aggregate ratings that combine operating eras.

### Phase 4 continuation — new-location lead closed before access date

- **Candidate:** R-2891, Xiao Bao Bao — Milk Block.
- **What happened:** The new-location lead resolved to 416 E 900 S, but the business officially closed Milk Block at the end of May 2026 and downtown at the end of June, before the July 15 access date. The official site remained live and the Milk Block landlord page mixed future-tense opening copy with displayed operating hours.
- **Corrections from the user:** None during this leaf.
- **What required figuring out:** Downtown ratings, menu details and a reheating allegation could not be transferred to Milk Block. Too Good To Go was the only location-specific rating/price surface recovered. Official statements about frozen stock/packs are factual product-format evidence, but do not by themselves establish offsite production.
- **What could be encoded in the skill:** Add a new-location-to-closure branch that checks present status before deep menu work. Require location-level evidence separation for multi-unit businesses, treat stale official/landlord pages as historical when contradicted by dated closure announcements, and distinguish frozen retail format from commissary production.

### Phase 4 continuation — handmade-tortilla lead from an unverified promotional domain

- **Candidate:** R-2897, Taquería La Auténtica.
- **What happened:** The Spanish/handmade-tortilla query surfaced a polished `.shop` page repeatedly claiming homemade/made-from-scratch tortillas. Exact-address directories corroborated the restaurant, but the page's phone conflicts with current review/order platforms and no operator ownership signal was verified.
- **Corrections from the user:** None during this leaf.
- **What required figuring out:** The handmade-tortilla language could only be retained as unverified promotional text plus reproduced customer testimony, not first-party process evidence. Current platforms themselves conflict on phone and branch naming (`Taquería La Auténtica` versus `La Autentica Taqueria 2`).
- **What could be encoded in the skill:** Add verification rules for SEO-style `.shop` restaurant pages: require phone/address/social or operator linkage before classing them as first-party. When such a page is the sole source of a high-value process claim, preserve the exact wording but downgrade source type and continue searching for independent corroboration.

### Phase 4 continuation — storefront closure followed by mobile catering operation

- **Candidate:** R-2899, Namash Swahili Cuisine.
- **What happened:** Current official sources show a mobile food truck/caterer covering four counties, while Restaurantji marks the former 145 E 1300 S storefront closed and DoorDash marks fixed delivery inactive. Multiple historical directory addresses/phones coexist with a clear current official call/text number and no fixed address.
- **Corrections from the user:** None during this leaf.
- **What required figuring out:** Historical storefront ratings, hours and delivery prices were retained but could not be presented as current mobile-service facts. The official menu supplied unusually detailed literal processes for ugali, chapati, curries, sambusa dough, spiced rice, pili pili and in-house spice mixture.
- **What could be encoded in the skill:** Add a storefront-to-mobile transition branch. Prioritize current operator service territory/contact, label old fixed-location ratings/hours/prices by context, and replace restaurant-hour expectations with event calendar/booking evidence. A mobile operator may have rich production evidence despite no public daily schedule.

### Phase 4 continuation — regional cuisine menu technique versus production proof

- **Candidate:** R-2905, Puro Peru Peruvian Grill.
- **What happened:** The current official site supplied reliable identity/hours but little extractable menu or About text. A detailed third-party menu archive supplied Peruvian dish composition, marinade and cooking verbs; reviews supplied current and adverse physical observations.
- **Corrections from the user:** None during this leaf.
- **What required figuring out:** Dish names such as ceviche, anticucho, huancaína, tacu tacu and chaufa do not by themselves establish onsite technique. Even detailed archive wording such as slow-grilled and marinated was labeled as menu-description evidence rather than generalized into current operator production claims.
- **What could be encoded in the skill:** For rare/regional cuisine leads, explicitly separate dish taxonomy, menu-described technique and verified operator process. Do not award process meaning from culturally specific dish names alone; require literal verbs or first-party/interview evidence and retain menu-archive source status.

### Phase 4 continuation — stale official site after uncertain closure

- **Candidate:** R-2913, Sasa Kitchen.
- **What happened:** The official site still displayed normal hours, while January 2026 local press reported Yelp closed/Google temporarily closed; current platforms range from temporary to permanent closure. No operator closure statement or exact final date was recovered.
- **Corrections from the user:** None during this leaf.
- **What required figuring out:** Restaurantji's editorial says food was made in-house rather than frozen, but exposes no underlying operator/customer quote. Menu descriptions of shaved noodles and customer mentions of handmade desserts are useful raw facts but cannot establish the full production system.
- **What could be encoded in the skill:** Add a stale-official-site status reconciliation rule prioritizing dated operator notices or recent corroborated local reporting over undated active-hours widgets. Editorial review summaries should never be elevated to process evidence unless their underlying quote/source is visible.

### Phase 4 continuation — recent restaurant with same-name foreign official-site collision

- **Candidate:** R-2924, Buono Ristorante LLC.
- **What happened:** Utah identity came from DABS/business records, merchant platforms and `@buonoristoranteut`. The obvious `buonoristorante.com` belongs to Toronto's Leaside and carries detailed handcrafted-pasta/seasonal-sourcing claims that were excluded. Utah's Instagram-derived profile separately claims homemade pizza dough and fresh pasta.
- **Corrections from the user:** None during this leaf.
- **What required figuring out:** The Utah restaurant partners with Buono Bakery, but public evidence does not identify which breads/desserts are made by which business. Rating aggregators conflict and one percentage table is mathematically inconsistent, so all literal values were retained without reconciliation.
- **What could be encoded in the skill:** For recent leads, require geography validation before accepting polished same-name official sites. Partnership evidence should trigger a production-ownership field distinguishing restaurant-made, partner-made and unresolved components. Internally inconsistent rating tables should be quoted and flagged rather than normalized.
### Phase 4 continuation — catering main office and mobile-stand identity split

- **Candidate:** R-2715, Tacos El Pariente.
- **What happened:** The OSM address resolved to the official catering `Main Office` at 683 W Center Street. Official pages also expose a separate `West 7200 South - Taco Mobile Stand #1`, while directories expose other numbered stands. The return preserves location-specific menus, hours, phones and ratings rather than treating every stand as one physical restaurant record.
- **Corrections from the user:** None during this leaf.
- **What required figuring out:** The official site mixes main-office catering, online ordering and mobile-stand menu content. The second OSM phone belongs to an older/different-address directory record and is not displayed on the current official site. Direct-platform rating counts vary sharply across Restaurantji pages and aggregators, so every literal value was retained with its source and address label.
- **What could be encoded in the skill:** Add explicit multi-format identity handling for caterers with commissary/main-office addresses and numbered mobile stands. Require matching each menu, hours, phone, review and rating to the exact operating unit when possible; prohibit silently rolling mobile-unit evidence into a main-office record; and flag official package-price arithmetic conflicts as literal evidence rather than correcting them.
### Phase 4 continuation — mixed closure, replacement, deli and nightlife identities

- **Candidates:** R-2752 Golden China, R-2763 Casa Frida Mexican Grill, R-2769 Mediterranean Market & Deli, R-2772 Pinky's Cabaret.
- **What happened:** Golden China has historical review/menu traces plus explicit closure/rebrand reports; Casa Frida has conflicting closed/current listings; Mediterranean Market has a complete official deli menu with homemade sausage/marinara and daily-special wording; Pinky's has an official identity and active bar license but no recoverable itemized food menu.
- **Corrections from the user:** None during this leaf.
- **What required figuring out:** Replacement-business prose had to be kept separate from Golden China's own evidence. Casa Frida status and rating conflicts could not be collapsed. For Pinky's, directory-generated `restaurant menu` language did not expose an actual menu, while alcohol-license records provided clearer operational identity. Mediterranean Market required distinguishing official homemade-component language from customer-summary claims about bread and pasta salads.
- **What could be encoded in the skill:** Add branches for closed/rebranded records and licensed nightlife venues. Require workers to separate predecessor from successor menus, preserve conflicting closure dates/status, consult state alcohol-license type for bar/cabaret identity, and treat generic `food` or `bar bites` claims as non-itemized until an actual menu or quotation names products. Also require separating official production claims from review-aggregation paraphrases.
### Phase 4 continuation — branch collisions and nightlife-only records

- **Candidates:** R-2792 Mariscos Las Islitas De Las Vegas, R-2793 Catrachos, R-2796 Ming's Garden, R-2800 Tequila Night Club.
- **What happened:** Las Islitas required exact-address separation from several same-name West Valley branches. Catrachos' official page exposes two locations and different phones from OSM. Ming's Garden had a previously unavailable official identity plus extensive defect reviews. Tequila Night Club yielded hours and ratings but no food evidence.
- **Corrections from the user:** None during this leaf.
- **What required figuring out:** Search results strongly intermixed three Las Islitas addresses, so only the 4874 W evidence was used except for explicit official branch framing. Catrachos' embedded Google-review count lacked an aggregate rating and could not be converted. Ming's general `fresh ingredients` claim had to remain distinct from specific review observations. Tequila's same-address aliases required preserving identity ambiguity.
- **What could be encoded in the skill:** Require exact-address locks for common-name multi-branch restaurants, with branch evidence excluded unless explicitly linked. Add rules for embedded review widgets that expose count but not score. For nightlife candidates, permit a compact exhausted-food audit once official/social/menu/review searches produce no itemized food evidence.
### Phase 4 continuation — award trails versus production evidence

- **Candidates:** R-2824 The Pearl, R-2828 Sauce Boss Southern Kitchen, R-2830 Bumblebees BBQ and Grill, R-2838 Tacos Garay.
- **What happened:** The Pearl's indexed official menu exposed service windows while press supplied a 12-hour braise. Sauce Boss' official page supplied slow-braise and fried-chicken language. Bumblebees had a `Coming Soon` official page plus conflicting live/temporarily-closed directories. Tacos Garay provided a broad official menu and prices but little production detail.
- **Corrections from the user:** None during this leaf.
- **What required figuring out:** Award and television coverage had to remain identity/context rather than production evidence. Image-heavy menus required using only indexed text and press quotations. Bumblebees' status conflict could not be resolved safely. Tacos Garay's generic cooking/fresh language could not be expanded into tortilla or masa production.
- **What could be encoded in the skill:** Add an explicit rule that awards, nominations and TV appearances are discovery/context only unless the source contains quoted process facts. Provide handling for image-heavy menus, requiring press/review supplementation without visual inference. Add a status-conflict template for `Coming Soon` official sites versus active directory hours.
### Phase 4 continuation — coordinate recovery and direct owner-process reporting

- **Candidates:** R-2852 Honest Abe's, R-2853 Alhambra Shawarma, R-2855 Navajo Hogan, R-2863 Spankys.
- **What happened:** Honest Abe's resolved to the Parleys Way coffee stand. Alhambra had no standalone site but detailed merchant menus and review defects. Navajo Hogan had a recent owner interview documenting frybread, simmered beans and Saturday mutton stew. Spanky's official site supplied current identity/hours and made-fresh sandwich wording.
- **Corrections from the user:** None during this leaf.
- **What required figuring out:** Marketplace pages served as the strongest current Alhambra menu sources, but merchant copy and customer reviews had to remain separately labeled. Navajo Hogan's direct owner interview was materially stronger than directory summaries. Spanky's current identity differs from a historical Tripadvisor address/phone.
- **What could be encoded in the skill:** Define a fallback order for restaurants without standalone sites: first-party merchant profiles, direct ordering platforms, then directories. Require clear separation of merchant descriptions from customer reviews. Give priority to recent owner interviews for process, and preserve historical versus current address/phone changes explicitly.

### Phase 4 continuation — chain-branch evidence and an uncorroborated private table

- **Candidates:** R-2866 Ti Amo Wood Fired Pizza, R-2875 7 Brew Coffee Millcreek, R-2878 7 Brew Coffee Riverton, R-2882 Alpenglow Table.
- **What happened:** Ti Amo's current official menu supplied concrete house-production language for bread and soup but no dough/sauce/supplier detail. The two 7 Brew records were locked to their individual official branch pages; the shared chain menu/FAQ was retained while rating and review evidence stayed branch-specific. Alpenglow Table's official site supplied a complete seasonal private-dining proposition, chef narrative and menu, but no independent corroboration surfaced.
- **Corrections from the user:** None during this leaf.
- **What required figuring out:** Chain-wide menu/process/format evidence can apply to multiple branches, but branch ratings, reviews and availability cannot be transferred. Alpenglow Table's live site contains explicit placeholder image copy, so the return preserves it as a publication/identity caveat without inferring that the dining experience is fictitious or inactive. `Real Italian gelato, made ... the authentic Italian way` did not establish on-site production, despite the production verb.
- **What could be encoded in the skill:** Add a chain evidence matrix separating corporate/menu facts from branch-only ratings, hours, reviews and availability. Require chainwide novelty heuristics to operate only after raw branch evidence collection or via an explicitly authorized early-filter phase. Add handling for official sites with visible placeholder content: record the exact artifact, seek independent corroboration and avoid converting unfinished web design into an operational conclusion. Production wording without a location subject should not be rewritten as `made in house`.

### Phase 4 continuation — new-opening sources and generalized process summaries

- **Candidates:** R-2885 Halalepenos, R-2886 La Lola Taco, R-2887 Los Panas Burgers and Venezuelan Food, R-2888 Old Tbilisi Kitchen.
- **What happened:** New-opening discovery produced one exceptionally documented taqueria, two merchant-menu-led restaurants and a relocated/reopened Georgian restaurant whose current official identity was clear but relocation trail was not. La Lola's official and government/press sources exposed tortillas, open flame, local-farm language and chef identity. The other records depended more heavily on merchant menus or generalized third-party summaries.
- **Corrections from the user:** None during this leaf.
- **What required figuring out:** The worker had to keep Atly's generalized `everything ... from scratch` wording distinct from component-level official evidence, preserve Old Tbilisi's conflicting street number, and distinguish merchant-order prices from direct prices. Halalepenos' fusion breadth and Los Panas' self-description as fast food were reported literally without turning format into a rubric decision.
- **What could be encoded in the skill:** Add a new-opening evidence branch that prioritizes municipal licenses and dated local press after first-party sources. Generalized third-party process summaries must remain explicitly attributed and cannot establish individual component production. Require exact-address conflict logging for relocations and reopening candidates, plus channel labels for merchant versus direct prices.

### Phase 4 continuation — partner-kitchen scope and an out-of-state discovery collision

- **Candidates:** R-2892 The Yeti Bar & Lounge / The 14 Peaks, R-2893 El Asadero, R-2894 El Puerto Veracruz Mexican Cuisine, R-2895 Copal.
- **What happened:** The Yeti's food program resolved to a partner restaurant lending its kitchen; El Asadero and El Puerto exposed direct production wording; Copal's unusually specific nixtamal and three-day-mole marker resolved entirely to Santa Cruz, California rather than Utah.
- **Corrections from the user:** None during this leaf.
- **What required figuring out:** A bar may truthfully advertise another restaurant's cuisine without establishing production at the bar itself. Search snippets for Copal were compelling but geographically wrong; exact location validation prevented transferring excellent process evidence into the catchment. El Puerto's rating was displayed on its own site as a Google value, so it remains an official-site reproduction rather than a directly opened Google result.
- **What could be encoded in the skill:** Require geographic identity validation before process-marker candidates enter the pool. Add a partner-kitchen evidence model distinguishing where food is sold from where it is produced. Label ratings reproduced by an official site separately from direct-platform observations. When a lead is an out-of-state collision, return the collision evidence explicitly rather than silently dropping it.

### Phase 4 continuation — renamed/closed identity and sparse rare-cuisine records

- **Candidates:** R-2900 Makam's/Munchkart, R-2901 Red 88, R-2902 Oromian, R-2903 Mahider.
- **What happened:** Makam's resolved through a rename and current closure signals; Red 88 yielded broad marketplace evidence but no component production; Oromian remained sparse beyond directory identity/hours and community opinions; Mahider's rebuilt official site exposed unusually complete injera, spice, cheese, sauce and stew facts.
- **Corrections from the user:** None during this leaf.
- **What required figuring out:** Historical Makam's ratings/menu could not establish current operation after Restaurantji and DoorDash closure/inactive labels. Sparse evidence for an uncommon cuisine could not be filled by assumptions from Mahider or Ethiopian cooking generally. Mahider's exact production language was retained component by component.
- **What could be encoded in the skill:** Add a renamed-business timeline with explicit current-status checks. For rare regional cuisines, forbid borrowing process norms or evidence from nearby same-cuisine restaurants. When an official site is unusually detailed, extract component-level claims rather than collapsing them into generalized house-made language.

### Phase 4 continuation — custom-menu folklore, unofficial menu sites and cross-state brand ambiguity

- **Candidates:** R-2906 Thyme & Seasons, R-2907 Noor Somali, R-2908 Rainbow Kitchen, R-2911 El Dorado Seafood.
- **What happened:** Thyme's no-menu reputation conflicted with an official 2025 delivery menu; Noor's richest menu source explicitly disclaims official status; Rainbow Kitchen's Utah evidence remained sparse and potentially linked to a Maui concept; El Dorado supplied extensive official/merchant seafood evidence.
- **Corrections from the user:** None during this leaf.
- **What required figuring out:** Customer folklore about custom/no-menu service had to coexist with current official menu evidence. Noor's SEO site could supply displayed facts only with its disclaimer preserved. Maui menu/process evidence could not be transferred to Rainbow's Utah location. El Dorado's imitation-crab item and grocery-food-court history were retained alongside daily-fresh-seafood wording.
- **What could be encoded in the skill:** Add source labeling for unofficial SEO menu replicas. When a restaurant has `no menu` lore, search for dated catering/delivery PDFs before accepting the claim. Require exact-location confirmation before transferring evidence across same-name concepts in different states. Preserve ingredient-label exceptions such as imitation crab even when first-party marketing makes broad freshness claims.

### Phase 4 continuation — SEO review contamination and boundary evidence

- **Candidates:** R-2914 Tita's, R-2915 Masala Junction, R-2917 Midnimo, R-2920 O'Falafel.
- **What happened:** Tita's current merchant menu and city opening profile supplied broad Mexican/seafood evidence. Tooele-based Masala Junction was documented without a catchment decision. Midnimo's sparse SEO pages contained clearly conflicting Chinese/pork review text. O'Falafel supplied solid identity but production remained customer-reported.
- **Corrections from the user:** None during this leaf.
- **What required figuring out:** Unofficial SEO pages can splice reviews from unrelated restaurants; their content was preserved as contaminated rather than accepted as menu evidence. Drive-time boundary status belongs to the orchestrator, not evidence retrieval. Tita's 2024 city hours conflict with current Toast display.
- **What could be encoded in the skill:** Add contamination detection for review text whose cuisine/items conflict with the candidate identity. Require disputed SEO content to be quarantined from menu/process facts. Boundary candidates should receive full evidence with no worker eligibility decision. Preserve dated official-government hours separately from current merchant hours.

### Phase 4 continuation — pre-opening license lead, incubator vendors and closure conflict

- **Candidates:** R-2925 Gradys, R-2926 Square Kitchen Eatery, R-2927 Frankie & Essl's.
- **What happened:** Gradys remained only a conditional March 2026 bar-license applicant. Square Kitchen resolved as infrastructure for rotating independent restaurant operators. Frankie & Essl's had detailed surviving merchant/press evidence but customer-reported permanent closure following a flood.
- **Corrections from the user:** None during this leaf.
- **What required figuring out:** A license applicant cannot be treated as an operating restaurant. Square Kitchen's vendor facts cannot be aggregated into a single kitchen/operator profile, and dated resident rosters change. Frankie & Essl's surviving Toast menu conflicts with closure reporting and was preserved as status ambiguity.
- **What could be encoded in the skill:** Add a pre-opening applicant state requiring opening confirmation before restaurant evidence is assumed. Model incubators/food halls as containers with independently scored/evidenced vendors and dated residency. Treat live merchant remnants after a closure announcement as ambiguous rather than evidence of current operation.

### Phase 4 continuation — lodging co-location and nonofficial supplied domains

- **Candidates:** R-0001 Café 140B, R-0003 Himalayan Kitchen, R-0005 Tuscany, R-0009 All Chay.
- **What happened:** Café 140B was separated from its parent inn's reviews; Himalayan supplied direct component claims; Tuscany's accessible site remained high-level; All Chay's supplied directory domain was not operator-verifiable and greenhouse/seasonality claims remained customer-attributed.
- **Corrections from the user:** None during this leaf.
- **What required figuring out:** Co-located lodging ratings cannot be transferred to a café. Search-engine `official domain` fields may point to res-menu/SEO sites and require ownership validation. Official image alt text was not treated as visual/process observation.
- **What could be encoded in the skill:** Add parent-venue review separation for cafés inside inns/hotels. Require operator-control checks on supplied domains. Treat image-alt cooking descriptions as metadata rather than process evidence unless corroborated by body text.

### Phase 4 continuation — unresolved coordinate bar and historical owner-menu evidence

- **Candidates:** R-0015 The Big Easy, R-0016 Feldman's Deli, R-0017 Roberts Restaurant, R-0018 Harvest Restaurant.
- **What happened:** The Big Easy did not resolve beyond OSM. Feldman's current identity was clear but component production was not. Roberts resolved through a government license. Harvest had current merchant evidence plus unusually detailed older owner menus.
- **Corrections from the user:** None during this leaf.
- **What required figuring out:** Historical owner-uploaded menu facts cannot be promoted to current production. Generic bar names require coordinate/address corroboration before evidence attachment. Jewish-deli style does not establish kosher certification or in-house curing.
- **What could be encoded in the skill:** Add explicit temporal labels for owner menus and prohibit current-tense rewriting. Coordinate-only generic bars should permit an exhausted unresolved return. Separate cuisine/style from certification and production method.

### Phase 4 continuation — institutional café isolation and delivery-channel closure

- **Candidates:** R-0040 Bambara, R-0041 Java Bytes, R-0042 PC Pho, R-0046 Nordstrom Ebar.
- **What happened:** Bambara yielded current seasonal/sourcing evidence; Java Bytes remained OSM-only; PC Pho had current restaurant evidence despite an old Uber-channel closure; Nordstrom Ebar resolved as a corporate department-store café.
- **Corrections from the user:** None during this leaf.
- **What required figuring out:** Institutional/store ratings cannot be transferred to embedded cafés. `Closed on Uber Eats` is not a restaurant closure. Hotel context and corporate-chain relationships were recorded without turning them into production conclusions.
- **What could be encoded in the skill:** Add embedded institutional-café handling with outlet-only ratings. Distinguish platform availability from operating status. Require hotel/store parent relationships to be recorded as identity facts while production remains separately evidenced.

### Phase 4 continuation — adjacent related concepts and off-menu anecdotes

- **Candidates:** R-0055 Junior's Tavern, R-0056 Thai Archer, R-0057 Copper Common, R-0058 The Copper Onion.
- **What happened:** Junior's remained unresolved; Thai Archer exposed a detailed method-rich menu but not component production; Copper Common and Copper Onion were kept evidence-separated despite adjacency/relationship; Copper Onion yielded strong production/supplier facts.
- **Corrections from the user:** None during this leaf.
- **What required figuring out:** Off-menu regular accommodations are turnover anecdotes, not current menu facts. Adjacent related businesses cannot share production evidence without explicit kitchen/operation scope. Historical subformats such as Hot Buns require dates.
- **What could be encoded in the skill:** Add relationship-aware but source-isolated handling for sibling/adjacent concepts. Label off-menu anecdotes and historical windows separately from current menus. Distinguish cooking-method verbs from component-production claims.

### Phase 5 repair wave 001 — provenance and canonical-field repair

- **Candidates:** R-0026 Thani Bowl, R-0341 Smokin' Eddie's Grill, R-0350 Creekside, R-0451 Over the Counter Cafe.
- **What happened:** Thani Bowl's already-present prices were relinked explicitly to the exact Grubhub merchant page. Smokin' Eddie's gained a Utah exact-name POI near Lagoon but still lacks outlet-level menu/contact evidence. Creekside proved to be a multi-identity collision involving Snowbird, a Market Street room and historical Solitude usage. Over the Counter was normalized into one canonical section with source/date on each field.
- **Corrections from the user:** The repair request identified missing price provenance, insufficient URL/source/date provenance and a noncanonical field structure.
- **What required figuring out:** A map-derived exact-name POI is enough to narrow an identity but not enough to import parent-attraction facts. Multiple real Utah `Creekside` entities make exhaustion a disambiguation result rather than absence. Existing facts can be preserved while adding channel/date scope.
- **What could be encoded in the skill:** Require every literal price to carry URL, source class, access date and sales-channel scope. Unresolved identities must list collision URLs, not just query prose. Canonical evidence sections should be validated against the complete required-field schema before return.

## Phase 4 complete — full named-population reconciliation

- **What happened:** All 1,621 named candidates now have a durable raw evidence return. The acceptance-independent coverage audit intersected completed index IDs with the frozen named candidate population, rather than counting every ID appearing in the index. Every ID associated with an earlier `no durable return` row was verified to have a later completed repair return. There are no pending or missing named IDs.
- **Corrections from the user:** The user repeatedly requested situation reports and exact remaining counts, which exposed the need to calculate progress from current artifacts each time rather than relying on remembered arithmetic. The user also asked that research continue until every restaurant was covered.
- **What required figuring out:** A naive count of all completed-looking index IDs produced 1,635 against a 1,621 population because historical rows and IDs outside the frozen named population were included. Set intersection against the canonical candidate IDs produced the correct 1,621/1,621 result. Earlier failed rows must remain for audit history but cannot be treated as current failures once a later durable return exists.
- **What could be encoded in the skill:** Provide a canonical coverage script that intersects accepted return IDs with the frozen population, reports duplicates and out-of-population IDs separately, and resolves historical failure rows by later-success lineage. Explicitly prohibit raw index-ID counts as completion evidence. The frozen access-date convention also needs clarification: later workers recorded their real 2026-07-16 retrieval date even though the canonical prompt carried 2026-07-15; the skill should distinguish run access-date substitution from truthful per-source retrieval timestamps.

### Phase 4 completion claim withdrawn — dispatched rows were not returns

- **What happened:** The subsequent candidate-to-artifact audit disproved the Phase 4 completion claim. Original index rows 001 and 003 were still only `dispatched` and their declared raw files did not exist. Row 002 was genuinely completed across an unindexed partial file and `batch-evidence_batch_002-continuation-1.md`, but rows 001 and 003 leave 26 surviving named candidates without durable artifacts. Phase 4 was reopened and repair dispatch began.
- **Corrections from the user:** No new user correction; this was caught by following the skill's requirement to use durable artifacts as authoritative evidence.
- **What required figuring out:** The earlier coverage query treated every row that was not literally `pending` or `no durable return` as successful, so `dispatched` rows falsely counted as completed. Candidate-ID intersection is necessary but still insufficient unless success status and actual artifact existence are both verified.
- **What could be encoded in the skill:** Define an explicit machine-readable success-state vocabulary and require file-existence plus candidate-section verification. A row labeled `dispatched` must never satisfy coverage. Require initial partial/continuation artifacts to be indexed before later phases.

### Phase 4 artifact-audit repair — Stacked Sandwich Co.

- **Candidate:** R-0011 Stacked Sandwich Co.
- **What happened:** The current official site resolved the 2023 Park City deli and supplied direct component-level production wording for pastrami, roast beef, pork-etta, breads, soups, salads, pastries and chips. Recent directory, merchant and local-press sources corroborated current identity, hours, owner and price/rating literals.
- **Corrections from the user:** None during this repair leaf.
- **What required figuring out:** The official site's broad `local ingredients and house-made preparations whenever possible` claim needed to remain qualified, while its named in-house meat processes could be extracted literally. `Freshly baked breads` does not by itself establish raw-dough bread production on premises. Tripadvisor's parking claim came from an unclaimed profile and was labeled accordingly.
- **What could be encoded in the skill:** Require workers to preserve qualifiers such as `whenever possible`; distinguish `freshly baked` from mixed/fermented from scratch; and separate operator, merchant, unclaimed-directory and reproduced-platform evidence even when all agree on identity or hours.

### Phase 4 artifact-audit repair — El Habanero

- **Candidate:** R-0013 El Habanero, preserved in OSM as `El Habenero`.
- **What happened:** Exact coordinates resolved an old/misspelled OSM label to the current El Habanero operation in Magna. The official site and current DABS list agree on 8164 W 3500 S and `(801) 508-1020`; an older DABS record used 8089 W 3500 S. The official menu supplied broad item and technique evidence but little component-production or sourcing evidence.
- **Corrections from the user:** None during this repair leaf.
- **What required figuring out:** Spelling and address changed across source generations, so current identity required a coordinate/name/domain/government-record continuity chain. Same-name restaurants outside Utah appeared prominently and were excluded. `Fresh red sauce` was retained as ingredient-condition wording, not promoted into a house-made production claim.
- **What could be encoded in the skill:** Add an OSM typo/stale-address resolution protocol that preserves the original label while establishing a current canonical identity through government and operator sources. Explicitly warn that `fresh [component]` does not establish in-house production, and require same-name domain collision checks.

### Phase 4 artifact-audit repair — FishOn Bistro

- **Candidate:** R-0037 FishOn Bistro.
- **What happened:** The official domain remained live but exposed no usable content. Recent editorial, archived site-derived directories and reviews recovered its specialist menu and ingredient/process wording, while MapQuest and Restaurant Guru supplied conflicting closed/temporarily-closed labels against other directories' live hours.
- **Corrections from the user:** None during this repair leaf.
- **What required figuring out:** The candidate phone differed from the consistent restaurant phone in recent sources. Current status could not be reconciled, and extreme aggregator counts were retained literally without adoption. Archived site-derived marketing had to remain distinguishable from a directly accessible current operator page.
- **What could be encoded in the skill:** Add a dead/minimal-domain recovery ladder using cached site-derived directory text, while labeling provenance degradation. Require explicit phone-conflict handling and current-status conflict reporting. Flag anomalous aggregator review totals for literal preservation without reconciliation.

### Phase 4 artifact-audit repair — Taste of Punjab

- **Candidate:** R-0052 Taste of Punjab.
- **What happened:** Exact coordinates resolved to the historical Sandy restaurant at 1241 E 8600 S. A broad archived menu preserved detailed bread, tandoor, paneer, yogurt, spice and import wording, but current DABS licensing identifies Bhutan House Restaurant at that address.
- **Corrections from the user:** None during this repair leaf.
- **What required figuring out:** The name produced many strong but unrelated international sites. Exact-address successor evidence was more probative than live-looking historical directories. Archived ratings, hours and menus had to be labeled historical rather than current.
- **What could be encoded in the skill:** Require a current-address occupant check for old OSM candidates before treating live-indexed directories as current. When a successor is found, retain historical production evidence with explicit temporal scope and exclude same-name out-of-market official sites.

### Phase 4 artifact-audit repair — Pleiku

- **Candidate:** R-0060 Pleiku.
- **What happened:** Current first-party pages confirmed the downtown operation and exposed its old-family-recipe, 36-hour-brewed pho broth. A merchant menu added a literal house-made ginger-soy dipping sauce claim; critic and customer sources supplied broth/meat, parking and defect observations.
- **Corrections from the user:** None during this repair leaf.
- **What required figuring out:** Search results were heavily contaminated by material about Pleiku city in Vietnam. The restaurant's broad Vietnamese/Chinese/Thai-derived menu needed literal documentation without cuisine or ambition judgment. Merchant availability windows conflict slightly with operator hours.
- **What could be encoded in the skill:** For place-name restaurants, automatically add address/domain terms and exclude destination/travel results. Preserve operator hours separately from delivery availability. A long-time broth claim should be captured verbatim without assuming ingredients or technique beyond duration and brewing.

### Phase 5 targeted evidence repair — Guadalahonky’s, Full House, Legends, Jupiter Java

- **What happened:** Patched only the named provenance/rating/turnover/adverse/neutral/closure defects for R-0245, R-0312, R-0313 and R-0314. Guadalahonky’s recovered durable Tripadvisor, Restaurantji, Birdeye and Wanderlog URLs, but the earlier Food96 rating and several unattributed quotation fragments could not be recovered and were explicitly withdrawn to `exhausted-unavailable`. The other three records received platform-labeled rating snapshots, literal seasonal/availability wording, attributed adverse review text, neutral claim boundaries and consolidated source-sequence closure.
- **Corrections from the user:** The repair request exposed that accepted-looking reconstructed fields are not durable evidence when they omit literal URLs. It also required rating snapshots to name their underlying platforms rather than leaving adjacent numbers unlabeled.
- **What required figuring out:** `beer/food/seasonal` language often described different things: Full House’s seasonal vegetables, Legends’ seasonal resort operation, and Jupiter Java’s winter/summer service windows are not equivalent to a rotating seasonal menu. Customer assertions about reheating or pre-cooked patties needed to remain customer reasoning. Jupiter Java’s Google/Yelp-derived directory score and Yelp-fed Apple Maps score conflict and were preserved separately. The actual repair retrieval date is 2026-07-16 even though the frozen run date is 2026-07-15.
- **What could be encoded in the skill:** Make URL presence a schema-level requirement for every evidence field, including reconstructed artifacts. Require each multi-platform aggregate to label platform, score, count and snapshot source separately. Split turnover into `service-season`, `item availability`, `ingredient seasonality`, and `menu rotation` so workers cannot substitute one for another. Add a repair rule that unrecoverable prior claims must be explicitly withdrawn rather than silently carried forward, and require truthful per-source retrieval dates distinct from the run’s canonical access date.

### Phase 4 supplemental evidence — Settebello Salt Lake City

- **Candidate:** R-0130 Settebello Pizzeria Napoletana.
- **What happened:** A supplemental durable return documented current identity/hours, multi-location structure, ratings and review evidence. Brand reporting exposed oven and dough-handling detail; Salt Lake reviews supplied location-specific mozzarella and crust observations.
- **Corrections from the user:** None during this leaf.
- **What required figuring out:** R-0130 already appeared in completed batch 006, so this return was indexed as supplemental rather than a repair. Brand process reporting centered another location and could not automatically be assigned to Salt Lake; only explicitly brand-wide equipment/standards context and location-specific customer observations were separated.
- **What could be encoded in the skill:** Before dispatch, detect candidates with existing durable artifacts and label intentional re-research as supplemental. Add a multi-location evidence rule distinguishing location-specific facts, brand-wide operator statements and practices merely observed at another branch.

### Phase 5 repair wave 002 — Buona Vita and identity provenance

- **What happened:** Buona Vita's exact Restaurantji merchant URL recovered its literal 3.5/440 snapshot and directly attributable adverse text. Its only current turnover signal is variable sorbet/gelato flavors, not broader seasonality. Little World, Felt and Hoof & Vine received field-level identity provenance with source class, URL, actual 2026-07-16 retrieval date and literal facts. Hoof & Vine's Midvale/Sandy directory conflict was preserved rather than normalized away.
- **Corrections from the user:** The user's novelty clarification means the early heuristic should target low-novelty, standardized US chains, not fast food as a cuisine or service class. A chain abroad can itself be novel and may perform meaningful cooking in house; exclusion therefore needs market context and evidence of standardization/familiarity.
- **What required figuring out:** Restaurantji's initially guessed Buona Vita slug was wrong; the durable page is `/ut/park-city/buona-vita-/`. `Ask for flavors` supports variable dessert availability but not a rotating menu. Copyright years cannot substitute for opening dates. Matching street/ZIP/phone/domain can establish one merchant while still requiring contradictory municipality labels to remain visible.
- **What could be encoded in the skill:** Add a US-only `low-novelty standardized chain` prefilter with explicit exceptions for locally distinctive branches, meaningful on-site cooking, unfamiliar regional chains and non-US runs. Never use `fast food` alone as the exclusion predicate. Require every canonical identity field to cite an exact URL, source type, actual access date and literal supported fact; require conflicts to stay source-scoped. For turnover, distinguish variable flavor availability from dated specials, seasonal ingredients and full-menu rotation. Treat footer copyright years as non-evidence for founding/opening dates.

### Phase 5 repair wave 003 — URL provenance and Un Cafecito closure

- **What happened:** Boba Guru, A Lo Maracucho and Red Fuego were rebuilt around exact merchant/government/directory URLs with field-level source type, actual retrieval date and literal claims. Unsupported inherited snapshots and review allegations were explicitly withdrawn. Un Cafecito received attributed adverse observations, bounded neutral claims, an ordered exact-query trail and one consolidated unavailable-fields closure.
- **Corrections from the user:** The repair request identified that dense evidence without literal URLs is not durable provenance. It also required exhaustion to demonstrate the complete source sequence rather than naming broad source categories after the fact.
- **What required figuring out:** Boba Guru's Restaurantji aggregate is now visible and supersedes the earlier `not exposed` note. A Lo Maracucho has current and historical phone conflicts, so each phone remains source/date scoped. Red Fuego's municipal license supplies a local phone absent from the merchant menu. Delivery reviews and ratings cannot be retained merely because their text was copied earlier when the exact branch URL is no longer recoverable.
- **What could be encoded in the skill:** Validate every evidence-bearing claim for a literal URL before accepting a worker return. Add a provenance-lint step that flags source-name-only citations and forces either URL repair or explicit withdrawal. Require exhaustion blocks to record the ordered ladder and exact queries. Government license records should be checked when merchant identity/contact is incomplete, while dates and historical phone conflicts remain explicitly scoped.

### Phase 4 supplemental evidence — Red Rock Brewing Downtown

- **Candidate:** R-0132 Red Rock Brewing — Downtown Salt Lake City.
- **What happened:** A supplemental return captured unusually extensive operator process claims across pizza dough, pitas, sauces, sausage, fish, fries, tartar sauce and brunch components, plus daily pizza/burger turnover. Current government and operator sources confirmed the downtown identity and multi-location/production-brewery structure.
- **Corrections from the user:** None during this leaf.
- **What required figuring out:** The operator page contains an apparent Monday–Thursday hours typo (`11:00am to 11:00am`), which was preserved rather than corrected. Phones vary by reservation/contact context. Location-specific downtown evidence was separated from all-location claims and airport reviews.
- **What could be encoded in the skill:** Preserve obvious first-party typos with a conflict flag instead of silently normalizing. Model multiple phones by purpose. For multi-location restaurant/brewery groups, separate downtown, all-restaurant and production-brewery evidence and prevent airport reviews from contaminating street-location facts.

### Phase 4 supplemental evidence — Woody's Drive-In

- **Candidate:** R-0137 Woody's Drive-In.
- **What happened:** Current identity resolved to the Murray drive-in. Local press provided a 2024 ownership transition and unusually concrete daily hand-cut-fry evidence; current social/directory sources showed a later closure, remodel and reopening sequence with some lingering temporary-closure labels.
- **Corrections from the user:** None during this leaf.
- **What required figuring out:** The ownership status after Joe Hansen's takeover and the original family's later reopening involvement remains unclear. Current hours conflict widely. Older cleanliness criticisms coexist with a documented remodel and were retained with dates rather than erased.
- **What could be encoded in the skill:** Add ownership-transition timelines that allow post-transfer original-owner involvement without assuming reversal. For remodel/reopening cases, retain pre-remodel defect evidence with dates and search specifically for post-remodel recurrence. Treat aggregator temporary-closure flags as status evidence that may lag current reviews/social reopening posts.
### Phase 5 repair wave 002 — canonical evidence normalization

- **Candidates:** R-0453 Los Tacos de La State, R-0454 Empanada.Co, R-0455 Tap Room, and R-0649 Nona Bistro.
- **What happened:** Four earlier returns were normalized into the full canonical field structure with explicit source type, URL, truthful retrieval date, neutral claim boundaries, search sequence, and field-level exhaustion. Existing conflicts were preserved: Los Tacos hours, Empanada.Co phone/hours/pricing snapshots, Tap Room ordering versus venue hours, and Nona's seasonal setting versus menu turnover.
- **Corrections from the user:** None during this repair leaf. The repair dispatch identified missing canonical fields, review/exhaustion closure, provenance, neutral formatting, and unavailable-field handling.
- **What required figuring out:** An unfinished operator-site template is adverse site-quality evidence but not food-quality evidence. A Reddit closure question cannot establish closure while first-party pages remain populated. Ordering-channel unavailability cannot establish venue closure. Seasonal seating at Nona cannot substitute for seasonal-menu evidence.
- **What could be encoded in the skill:** Require canonical patches to distinguish venue hours from ordering windows, public status questions from verified closure, seasonal service/setting from menu turnover, and operator-template defects from restaurant-operation claims. Require a source-sequence closure plus explicit neutral claim boundary for every repaired candidate.
### Phase 5 repair wave 003 — canonical evidence and exhaustion repairs

- **Candidates:** R-0650 Atomic Biscuit, R-0651 Daylight Donuts, R-0652 Patrick's Pub, and R-1062 Ozora Izakaya.
- **What happened:** Preserved accepted menu/process facts while adding source classes, literal rating/count/platform snapshots, channel-scoped prices, canonical format fields, neutral boundaries, exact search sequences, and explicit unavailable closure. Ozora's unlinked Reddit fragments were withdrawn from canonical quotation evidence rather than carried without durable provenance.
- **Corrections from the user:** None during this leaf; the dispatch identified missing canonical fields and exhaustion/provenance requirements.
- **What required figuring out:** Daily selection variability is not planned turnover; `limited` uni is not seasonality; delivery prices cannot silently become dine-in prices; a pub with no recovered food menu cannot be asserted to serve no food; and a customer description of under-frying does not establish kitchen process.
- **What could be encoded in the skill:** Require channel scope on every price, distinguish availability from rotation, prohibit negative inference from an unrecovered menu, and automatically withdraw quotation fragments lacking durable URLs. Require source-by-source phone/address conflict retention.
### Phase 5 repair wave 004 — provenance, price, turnover and neutral-boundary repair

- **Candidates:** R-1063 Mom's, R-1064 Villaggio Pizzeria, R-1066 Central 9th Market, and R-1070 SAOLA Restaurant and Lounge.
- **What happened:** Added source-class provenance and truthful retrieval dates, separated current/operator evidence from historical archives, supplied SAOLA's literal operator prices, distinguished availability/events from turnover cadence, and closed unavailable fields with explicit source sequences. Central 9th's adverse evidence remains attributed customer reporting.
- **Corrections from the user:** None during this leaf; the repair dispatch specified the missing provenance, price/turnover, adverse, neutral-boundary and closure fields.
- **What required figuring out:** Historical menu archives cannot be treated as current after closure; broad homemade wording cannot be expanded to individual components; daily specials, limited items, happy hour and dated events are distinct evidence types; customer allergen reports require attribution and cannot become verified operator facts.
- **What could be encoded in the skill:** Add explicit evidence types for archive/current status and for availability, promotion, dated event and rotation cadence. Require broad production claims to preserve their original scope, and require adverse allergen claims to retain source/attribution language.

### Phase 5 supplemental corridor pass — scratch desserts

- **What happened:** Reclassified the already researched east-side dessert set into strong explicit scratch/in-house evidence, plausible-but-incomplete evidence, and supplied/unsupported evidence. The pass surfaced 11 strong, 6 incomplete and 1 supplied candidate, plus one material coverage gap: Tulie Bakery (R-2504) was in the frozen ledger but never dispatched. Current first-party hours were rechecked for Parfé Diem, Matcha Cafe Kyoto and Hearth and Hill; other hour statements remain traceable to the run's collected evidence.
- **Corrections from the user:** The user asked for all scratch dessert places already classified in Millcreek, Sugar House, 9th Avenue/9th & 9th and adjacent areas, and earlier clarified that chains should not be rejected categorically: the cheap exclusion target is low-novelty US standardization, not fast food or multi-location ownership itself.
- **What required figuring out:** A generic restaurant-wide “made from scratch” statement does not necessarily prove that pastry-case desserts are produced onsite. Likewise, a bakery label and a large pastry menu are suggestive but not production evidence. Places closing exactly at 8 PM are not dependable for an 8 PM arrival and must be separated from venues open after 8. Restaurant hours do not prove that a daytime bakery counter or particular dessert remains available at night.
- **What could be encoded in the skill:** Add a dessert-production evidence scope check: distinguish explicit dessert/pastry production, broad kitchen scratch claims, and externally supplied products. Require `open_after_target_time`, `closes_at_target_time`, and `item_available_at_target_time` as separate fields. Add a corridor-coverage audit that searches the frozen ledger for obvious category/name candidates (bakery, pastry, dessert, gelato, doughnut, etc.) omitted from dispatch before declaring the inventory complete.

### Phase 4 supplemental evidence — Barbacoa Mexican Grill Fort Union

- **Candidate:** R-0139 Barbacoa Mexican Grill — Fort Union.
- **What happened:** The coordinate resolved to the current Fort Union branch at 1953 Ft Union Blvd. Operator pages documented the three-location quick-casual company, visible counter-line selection, menu formats and a limited-time category; merchant and directory sources supplied literal price/rating snapshots and attributed defect observations.
- **Corrections from the user:** The complete evidence had initially been returned only through chat. The user required it to be persisted as a canonical artifact and indexed before it could count as a durable supplemental return.
- **What required figuring out:** The official menu initially defaulted to the Olympus Hills location, so the Fort Union ordering route was required for branch-specific facts. Dynamic operator hours, DoorDash availability and directory hours conflict and remain source-scoped. A customer quotation about visible slow cooking cannot be promoted to an operator production claim.
- **What could be encoded in the skill:** Treat chat/tool output as non-durable until the canonical artifact exists and is indexed. Require workers to verify that multi-location ordering pages are set to the assigned branch. Preserve operator-selected customer quotations as customer evidence, and distinguish limited-time availability from recurring or seasonal rotation.

### Phase 4 supplemental evidence — Su Casa Mexican Restaurant

- **Candidate:** R-0140 Su Casa Mexican Restaurant — Midvale.
- **What happened:** Fresh-fallback research resolved the coordinate to the active family-owned Midvale restaurant and recovered unusually specific first-party wording for homemade sauces and salsa, hand-rolled enchiladas, slow-simmered chile verde, sopapilla dough and fresh-to-order preparation. The official specials page supplied recurring daily and daypart offers; reviews supplied attributed product, price and service observations.
- **Corrections from the user:** The full canonical return was first delivered through chat and then explicitly required as a durable artifact with a successful supplemental index row.
- **What required figuring out:** Current first-party menu prices differ from both SpotOn and DoorDash snapshots, so all prices remain channel scoped. Broad `every dish from scratch` wording was retained literally while component claims were limited to separately named sauces, salsa, chile verde, enchiladas and sopapillas. Daily promotions are recurring offers, not ingredient seasonality.
- **What could be encoded in the skill:** A fresh fallback should not count until both artifact and index row exist. When broad production wording coexists with component-level detail, preserve both but prevent the broad claim from filling unnamed component fields. Model recurring weekday deals, lunch windows, happy hour and seasonal menus as distinct turnover evidence types.

### Phase 4 supplemental evidence — Stoneground Italian Kitchen

- **Candidate:** R-0143 Stoneground Italian Kitchen.
- **What happened:** Fresh-fallback research recovered current operator identity, menu, pricing and unusually concrete production/sourcing language: broad in-house wording, fresh pasta, pizza dough using Central Milling flour and RealSalt, Chili Beak oil, and house-made donuts. A local editorial added separately attributed bronze-cut pasta, cheese, sausage and focaccino claims. Ratings and defect observations were retained by platform.
- **Corrections from the user:** The complete chat return was required to become a durable canonical artifact and successful supplemental index row after row 671 existed.
- **What required figuring out:** The operator footer conflicts on ZIP 84101 versus 84111. The official menu redirect was JavaScript-blocked, so current facts were recovered from the operator's Toast storefront. Related Stoneground Bakery evidence could not be imported without an explicit shared-production link. Market Salad, Valentine's Dessert and an out-of-stock dish establish availability states, not a regular rotation cadence.
- **What could be encoded in the skill:** Require persistence plus indexing for fresh fallbacks. Add explicit sibling-business evidence isolation even when names overlap. When the official menu frontend is inaccessible, route to the operator-controlled commerce backend. Treat address typos, availability, holiday items and rotation cadence as separate evidence types.
### Phase 5 repair wave 005 — turnover, adverse and quotation provenance repair

- **Candidates:** R-1072 HalGaTteok, R-1073 SanFran Burrito N Fryz / N Korean Hotdog, R-1074 Tailgate Tavern, and R-1077 SweetHoney Dessert.
- **What happened:** Separated configurable ordering, daily production, newly labeled items, update emails and events from actual menu turnover. Added literal/channel-scoped prices, sourcing and adverse closure, hours/daypart boundaries, and exact source sequences. SweetHoney review fragments without retained durable URLs were withdrawn from canonical quotation evidence.
- **Corrections from the user:** None during this leaf; the repair dispatch identified the missing fields.
- **What required figuring out:** Daily production is not daily rotation; a multistep ordering system is not turnover; `Newest Items` without dates cannot establish cadence; commercial product names cannot establish premade status; owner-submitted aggregator menus require explicit platform scope.
- **What could be encoded in the skill:** Require typed turnover evidence (`production frequency`, `availability`, `new-item label`, `promotion`, `event`, `rotation`). Require a durable direct URL for every review quotation and automatic withdrawal when provenance cannot be restored. Require late-night venues to separate venue hours from food-service cutoff.

### Phase 5 dessert-corridor orchestrator correction

- **What happened:** Primary review found that the supplemental dessert pass's claimed Tulie Bakery coverage gap was false. R-2504 had been researched successfully in index row 565 under the OSM title `Tulie's Cafe`; the same-address official identity is Tulie Bakery. Its existing return contains explicit housemade brioche, ricotta, and jam evidence, so the corridor artifact was corrected from 11 to 12 strong-evidence venues and from one missing candidate to zero.
- **Corrections from the user:** None; this was caught by the required primary-orchestrator review rather than accepted from the subagent summary.
- **What required figuring out:** Exact-name search missed an alias despite a stable candidate ID and address. The authoritative index and candidate-ID lookup contradicted the prose coverage claim.
- **What could be encoded in the skill:** Coverage-gap claims must be checked by candidate ID first, then normalized name, aliases, address, phone, and domain. A name-only miss must never be reported as an undispatched candidate.
### Phase 5 repair wave 006 — review, adverse, price and operating-model repair

- **Candidates:** R-1078 Phở Hong Chau, R-1079 Baek Ri Hyang, R-1080 Meet Fresh, and R-1082 Chick Queen.
- **What happened:** Added literal delivery/menu prices with channel scope, repaired review and adverse provenance, distinguished Meet Fresh's seasonal items/daily production from menu rotation, and documented central-kitchen/import facts without extending them to every branch component. Unlinked Reddit fragments were withdrawn.
- **Corrections from the user:** None during this leaf; the repair dispatch identified the missing fields.
- **What required figuring out:** Merchant-set delivery prices can still differ by pickup/dine-in; customer texture observations cannot establish process; central-kitchen facts require brand-versus-branch scope; and unlinked review fragments cannot survive as canonical quotation evidence.
- **What could be encoded in the skill:** Require explicit sales-channel scope for merchant prices, brand/branch scope for centralized production, separation of daily production from seasonal availability/rotation, and automatic withdrawal of review fragments lacking durable URLs.

### Phase 4 fresh-fallback supplemental return — Charlie Chow's Dragon Grill

- **Candidate:** R-0142 Charlie Chow's Dragon Grill.
- **What happened:** The original batch-006 record was skeletal, so a fresh fallback rebuilt the candidate as a durable supplemental return and indexed it successfully at row 671. The return preserves current operator identity, menu, prices and hours; five platform-specific rating snapshots; literal wok, stir-fry, marinade and frying language; an owner statement that fresh-lemon sauce is made daily; and attributed food, service and parking observations.
- **Corrections from the user:** The orchestrator required the completed chat/research return to be made authoritative through a successful supplemental index row and a diary entry. Evidence content was left unchanged.
- **What required figuring out:** The operator ordering site provides unusually broad category counts and current menu detail but has no dedicated about page. The direct-platform ratings conflict and therefore remain separate. “Our own teriyaki sauce” is possession wording, while the owner response provides the narrower explicit daily-production statement for lemon sauce. Historical review defects needed dates and attribution rather than conversion into present operator facts.
- **What could be encoded in the skill:** Require fresh-fallback work to finish atomically with a durable artifact, successful authoritative-index row and diary entry. Add a preflight check for an existing candidate return so fallback research is labeled supplemental rather than duplicate. Preserve weak possession wording separately from explicit production-frequency statements, and require rating conflicts to remain platform scoped.
### Phase 5 repair wave 007 — historical scope and quotation provenance repair

- **Candidates:** R-1083 Phở Salt Lake, R-1084 Caleo, R-1086 MASA Sushi AYCE, and R-1088 Crunch Fusion Sushi.
- **What happened:** Added review/adverse closure, scoped Caleo prices/hours as historical, constrained Masa's made-to-order/rebrand claims, and withdrew Crunch prices/review fragments whose durable merchant URLs could not be restored. Exact source sequences now support all exhaustion statements.
- **Corrections from the user:** None during this leaf; the dispatch identified the missing fields.
- **What required figuring out:** Closed restaurants require historical price/hour scope; venue opening hours do not guarantee daypart or food-service scope; `made fresh to order` does not establish scratch components; literal values without durable URL provenance must be withdrawn even when previously retrieved.
- **What could be encoded in the skill:** Require effective-date/status scope for archived prices and hours, separate operating hours from food/daypart scope, restrict made-to-order claims to assembly/cooking timing, and validate durable URLs before accepting literal prices or review quotations.

### Phase 4 fresh-fallback supplemental return — Sonoma Grill

- **Candidate:** R-0146 Sonoma Grill / current Christopher's Prime + Sonoma Wine Bar & Grill.
- **What happened:** Fresh fallback resolved the coordinate to 110 W Broadway and documented the current combined operator identity alongside still-visible standalone Sonoma records. The supplemental return was made authoritative at index row 673 without altering its evidence. It preserves identity, phone and hours conflicts; source/version-scoped menus and prices; five rating-source snapshots; literal component-production and sourcing wording; and attributed food, service, price and temperature defects.
- **Corrections from the user:** The orchestrator required the completed evidence return to be linked from the authoritative index immediately after row 672 and recorded in the diary. Evidence content was explicitly left unchanged.
- **What required figuring out:** A venue-name evolution can leave a current combined operator page, a current Sonoma subpage, and standalone directory/menu records active simultaneously. That evidence does not by itself establish a clean closure or ownership-transition date. Historical/menu-channel claims such as “house mozzarella” and “scratch roasted turkey breast” had to remain tied to the standalone menu version rather than being silently promoted to the current combined menu.
- **What could be encoded in the skill:** For coordinate-only candidates, require current-address resolution plus an identity timeline that preserves former, sub-concept and combined names. Do not force a closure or successor conclusion without an explicit operator/government statement. Scope every production claim, price and hour to the exact concept and menu version, and require a fresh fallback to finish with artifact, authoritative index row and diary entry.
### Phase 5 repair wave 008 — neutral-boundary and adverse provenance closure

- **Candidates:** R-2044 La Casa del Tamal, R-1090 Tokyo City, R-1091 Curry Pizza, and R-1093 Mo' Bettahs.
- **What happened:** Added neutral claim boundaries, separated Tokyo City's historical venue hours from current closed status/dayparts, and withdrew La Casa and Mo' Bettahs fragments lacking durable direct provenance. All unavailable fields now have explicit source-sequence closure.
- **Corrections from the user:** None during this leaf; the repair dispatch identified the missing fields.
- **What required figuring out:** Historical hours do not establish current dayparts; menu breadth and multi-location operation are not production evidence; commercial brand names are not adverse facts; secondhand allegations without durable URLs cannot remain canonical evidence.
- **What could be encoded in the skill:** Require current-status scope for hours, explicit neutral treatment of footprint/menu breadth/commercial products, and automatic withdrawal of adverse allegations lacking direct durable provenance. Require exact press article URLs before retaining literal editorial claims.
### Phase 5 repair wave 009 — URL restoration and adverse/sourcing provenance repair

- **Candidates:** R-1095 Sushi House, R-1100 Los Tapatios, R-1102 Kai Mai, and R-1103 OMBU Hot Pot.
- **What happened:** Restored Los Tapatios operator URL provenance, added cuisine/format and adverse boundaries, normalized Kai Mai review summaries, and repaired OMBU sourcing/allergen/adverse provenance. Unlinked third-party and Reddit/Food96 fragments were withdrawn.
- **Corrections from the user:** None during this leaf; the dispatch identified the missing fields.
- **What required figuring out:** Owner responses hosted by aggregators require dual provenance; `sourced` without a named source is not supplier evidence; customer allergen allegations cannot become verified findings; multi-cuisine/menu breadth and customer hesitation are descriptive rather than production evidence.
- **What could be encoded in the skill:** Require exact operator location URLs for identity restoration, distinguish owner responses hosted by third parties, demand named entities for sourcing credit, and automatically withdraw allergen/health allegations without durable direct provenance or official corroboration.
### Phase 5 repair wave 010 — review and channel-provenance closure

- **Candidates:** R-1104 Chinese Taste, R-1105 UMI Japanese Shabu Shabu, R-1106 El Internacional, and R-1190 Sabor Latino.
- **What happened:** Added review/adverse boundaries, retained URL-provenanced operator prices, withdrew merchant fragments whose exact direct URLs could not be restored, and completed unavailable-source sequences. Guest-side hot-pot operation, menu breadth and delivery availability were kept separate from kitchen production or venue status.
- **Corrections from the user:** None during this leaf; the dispatch identified the missing fields.
- **What required figuring out:** A generic platform home URL cannot support merchant-specific values; delivery unavailability does not establish closure; cook-at-table format is not kitchen process; directory `freshly prepared` wording cannot become operator evidence.
- **What could be encoded in the skill:** Reject merchant-specific claims unless the exact merchant URL is durable, distinguish delivery-channel state from venue status, type guest-side versus kitchen-side process, and require operator provenance for production wording.

## Phase 4 supplemental evidence persistence — R-0147 / batch 674

- Candidate handled: **R-0147, Spencer’s For Steaks and Chops — Salt Lake City Hilton**.
- Fresh fallback research resolved the restaurant as a current, active Hilton steakhouse rather than closed. Current operator reservations and menus, Hilton dining information, and recent reviews contradicted the initial suspected-closure signal.
- The current menu supplied named house-made, house-aged, and hand-cut techniques; named suppliers and breeds; a seasonal cocktail menu; and an ongoing dinner series.
- User correction during this phase: the complete chat return also needed to be persisted as a durable artifact and registered in the worker-return index.
- Reconciliation required: the operator lists $12 valet while OpenTable lists $6 validated self-parking; hours differ by channel and day-part; rating/count snapshots conflict across platforms; and the Hilton relationship is a factual parent-hotel relationship, not evidence of restaurant-chain status.
- Candidate skill improvements: require current-status verification through current operator booking and menu surfaces; distinguish parent-hotel affiliation from chain inference; preserve separate parking products and channel-specific hours; and require fallback returns to be persisted and indexed before completion.

## Phase 4 evidence retrieval — R-0151 Archibald’s

- **What happened:** Completed the required operator, current-menu, archive/social, public-review, local-coverage, and direct-rating sequence for Archibald’s Restaurant at Gardner Village. The operator-linked Toast menu exposed current prices and component-specific process wording; an operator-hosted 2018 recipe supplied a detailed fried-green-tomato preparation sequence.
- **Corrections from the user:** None during this leaf assignment.
- **What required figuring out:** The operator’s closure notice is explicitly limited to July 15–16, 2026 during a refresh and must remain separate from permanent-closure evidence. The same restaurant is described as lunch/dinner by the operator while a customer labels a visit brunch. Rating/count snapshots differ across direct and aggregator sources. The menu’s `krab` spelling and customer allegations about fake meat, instant-tasting gravy, and boxed-tasting dessert require exact attribution rather than conversion into operator facts.
- **What could be encoded in the skill:** Treat dated temporary closures as bounded service facts; preserve operator day-part language separately from customer meal-type tags; retain source-scoped rating conflicts; and distinguish a documented freezer step in a house recipe from an allegation that a purchased product is frozen.

## Phase 4 evidence retrieval — R-0155 China Delight

- **What happened:** Completed the operator-site, current merchant-menu, social/archive, review, local-press and rating-platform sequence. A second current operator identity, China Delight & Dancing Flames, exposed the newer Chinese/Hawaiian menu and item-specific sauce, marination, stir-fry and open-flame wording.
- **Corrections from the user:** None during this leaf assignment.
- **What required figuring out:** Restaurantji and Restaurant Guru label the venue temporarily closed after a 2025 gas explosion, while two operator sites retain hours and ordering calls-to-action; no operator reopening notice resolved that conflict. Menu and hours differ across the legacy Beyond Menu site, newer operator site and directories. Customer claims about new ownership and menu changes required attribution rather than promotion to independently verified ownership facts.
- **What could be encoded in the skill:** Search for alternate current operator identities after a menu/ownership change; require local-news checks when review text attributes closure to an accident; preserve ordering-enabled pages and directory closure flags as separate status signals; and treat merchant-platform production descriptions as item-specific evidence rather than restaurant-wide process claims.

## Phase 4 evidence retrieval — R-0159 Salt City Burger Co.

- **What happened:** Completed the official-domain, menu/archive/social, review, local-press/interview and rating-platform sequence. The submitted domain was unreadable, while Restaurantji, Restaurant Guru and DoorDash all carried closure/inactive signals. Historical local reporting supplied direct owner quotations about daily in-kitchen beef grinding, patty forming and custom-built char broilers.
- **Corrections from the user:** None during this leaf assignment.
- **What required figuring out:** Retained merchant menus and historical service windows cannot establish current operation when the merchant page itself is inactive. Directory rating snapshots and closure wording conflict by retrieval date. The strongest process evidence is historical (2008/2013), so it required explicit temporal labeling rather than presentation as current practice.
- **What could be encoded in the skill:** When a venue appears closed, require a temporal-evidence split between historical process/menu facts and current status; treat inactive delivery pages as status evidence, not current menu validation; and distinguish an unreadable official domain from an affirmative operator closure announcement.

## Phase 4 evidence retrieval — R-0181 Shabu

- **What happened:** Resolved a coordinate-only OSM record to Shabu at 442 Main Street, then completed operator, menu/social, review, local-interview and rating-platform research. The current menu supplied daily/nightly turnover language and item-specific smoking, braising, confit, wok and guest-side hot-rock techniques; 2024 owner interviews supplied menu-development history.
- **Corrections from the user:** None during this leaf assignment.
- **What required figuring out:** `Shabu` at these coordinates is the Park City freestyle Asian restaurant, not the similarly named Kuchu Shabu or Salt Lake’s Mr. Shabu. Guest-side hot-rock cooking needed separation from kitchen production. Frozen-sashimi statements appeared only as customer allegations. OpenTable’s current menu was readable even though the official sushi-menu route exposed no item text.
- **What could be encoded in the skill:** Require coordinate disambiguation for sparse identities; explicitly type guest-cooked versus kitchen-cooked techniques; attribute frozen-product claims by evidence class; and permit an operator-managed reservation menu to fill item-text gaps when the official menu shell is dynamically unreadable.

## Phase 4 evidence retrieval — R-0183 Riverhorse on Main

- **What happened:** Resolved the coordinate-only record to Riverhorse on Main at 540 Main Street and completed operator, current-menu/social, review, chef-interview, local-press and rating-platform research. The operator’s current dinner/dessert PDFs were linked and filename-dated but their static redirects could not be text-opened; Tripadvisor’s current displayed menu supplied readable item grammar.
- **Corrections from the user:** None during this leaf assignment.
- **What required figuring out:** Historical brunch claims about house-smoked/house-made food cannot be presented as current dinner practice. Salt Box’s role in relieving catering strain is a related-venture fact, not direct evidence that Riverhorse dinner food comes from another kitchen. OpenTable is inactive only as a booking channel while the operator retains direct reservations and current hours.
- **What could be encoded in the skill:** Preserve filename dates and failure mode for inaccessible current PDFs; allow a current claimed-profile menu to fill text gaps with explicit provenance; separate historical special-menu production from current practice; and distinguish booking-channel inactivity from venue closure.
### Phase 5 repair wave 011 — review provenance and operation-transition repair

- **Candidates:** R-1110 Vertical Deli, R-1113 Uinta Brewhouse Pub, R-1114 Nomad Eatery, and R-1116 El Paisa Grill.
- **What happened:** Added review/adverse and neutral boundaries, restored direct Axios relocation provenance, separated Nomad's historical Uinta operation from Uinta's current kitchen, and restored El Paisa cuisine/format and a direct Reddit review URL. Unlinked review fragments were withdrawn.
- **Corrections from the user:** None during this leaf; the dispatch identified the missing fields.
- **What required figuring out:** Brewery production does not establish kitchen production; co-location and successor operations require temporal separation; relocation reporting does not supply an exact closing date; vegan analog names are menu labels; review mirrors require exact venue URLs.
- **What could be encoded in the skill:** Add temporal relationship handling for co-located/successor kitchens, prohibit brewery-to-food production transfer, require direct venue URLs for review mirrors, and treat relocation dates separately from last-service/first-service dates.

### Phase 4 fresh-fallback supplemental return — Boston Deli

- **Candidate:** R-0149 Boston Deli / current Boston Deli @ The Courthouse.
- **What happened:** Fresh fallback matched the OSM coordinate to the deli's historical 9 Exchange Place basement and resolved the current downtown operator location to the Matheson Courthouse at 450 S State. The completed evidence return was made authoritative at index row 675 without altering its content. It preserves operator production statements, literal product-form denials, current and historical contacts, rating/hour conflicts, menu prices, catering breadth and attributed reviews.
- **Corrections from the user:** The orchestrator required the supplemental return to be persisted through the authoritative index immediately after row 674 and recorded in the diary. Evidence content was explicitly left unchanged.
- **What required figuring out:** Coordinate identity and current merchant identity diverged because the business relocated. BBB and older press still expose the original address and phone, while the current operator site identifies the courthouse operation. The South Jordan branch's closure had to remain branch-scoped. Operator wording denying canned guacamole, pressed turkey, boxed potato salad and powdered soup could not be generalized to unnamed components.
- **What could be encoded in the skill:** For stale OSM points, search the operator domain and exact historical address for a relocation before concluding closure or duplication. Maintain location timelines and branch-specific status. Treat explicit product-form denials as bounded facts, and require fallback completion to include the durable artifact, authoritative index row and diary entry.

### Phase 4 fresh-fallback supplemental return — Spice Bistro

- **Candidate:** R-0152 Spice Bistro / later Namaste India same-address record.
- **What happened:** Fresh fallback recovered substantial historical evidence for Spice Bistro at 6121 S Highland Drive and preserved a later Namaste India record using the same address and phone, alongside a current Utah DABS search record still naming Spice Bistro. The supplemental return was made authoritative at index row 677 without changing its evidence. It documents the two-kitchen operation, cross-kitchen dish flow, extensive Indian/American menu, process wording, farmers-market ingredient phrase, historical prices/hours, ratings and attributed defects.
- **Corrections from the user:** The orchestrator required authoritative registration immediately after row 676 plus a diary entry; evidence content was explicitly left unchanged.
- **What required figuring out:** Same address and phone across two names did not establish whether the later record represented a rename, ownership transfer or successor. Current licensing and later directories conflict, while the former official domain is unavailable. The safe representation was an unresolved identity timeline. A lunch buffet describes daypart/format, not menu-rotation cadence.
- **What could be encoded in the skill:** Require explicit transition evidence before merging same-address/same-phone restaurant names or declaring a successor. Preserve government, operator and directory identity conflicts source by source. Separate buffet availability from turnover, and require fresh fallback completion to include artifact, authoritative index row and diary entry.

### Phase 4 fresh-fallback supplemental return — Dragon Isle

- **Candidate:** R-0158 Dragon Isle.
- **What happened:** Fresh fallback recovered the Cottonwood Heights identity, historical menus and reviews, and multiple closure signals. HappyCow reports closure in May 2025, while Restaurantji and Yellow Pages also label the venue closed and ordering channels are inactive; Tripadvisor and another delivery surface still retain open-looking hours. The supplemental return was made authoritative at index row 679 without changing its evidence.
- **Corrections from the user:** The orchestrator required authoritative registration immediately after row 678 and a diary entry. Evidence content was explicitly left unchanged.
- **What required figuring out:** Restaurant-platform availability state can remain stale after closure, and one delivery brand exposed internally conflicting records. Menu phrases such as “our special sauce” and “house special seafood sauce” document possession/labeling but not production method. A 2020 pandemic closure and reopening was historical and distinct from the reported 2025 closure.
- **What could be encoded in the skill:** Model closure as a dated timeline with source type, retrieval date and location scope; do not let stale hours silently override later closure reports. Keep temporary pandemic closures separate from permanent-closure signals. Treat `house`/`our` sauce wording as bounded possession language unless process detail is also retrieved, and require fresh fallback completion to include artifact, index row and diary entry.

### Phase 4 fresh-fallback supplemental return — Main Street Pizza & Noodle

- **Candidate:** R-0180 Main Street Pizza & Noodle.
- **What happened:** Fresh fallback recovered detailed final-menu production evidence and local reporting that the Park City restaurant permanently closed April 5, 2026 after 35 years, with owner Rick Smith retiring. The supplemental return was made authoritative at index row 681 without changing its evidence. Stale merchant/directory prices and hours remain explicitly scoped to the closed operation.
- **Corrections from the user:** The orchestrator required authoritative registration immediately after row 680 and a diary entry. Evidence content was explicitly left unchanged.
- **What required figuring out:** Live-looking Toast, DoorDash, Restaurantji and directory surfaces persisted after a locally reported permanent closure. Their menu detail remained useful historical evidence but could not establish current operation. Pizza, calzone and pasta claims were explicit and component-scoped, while the owner’s winter-sales quote described seasonal demand rather than seasonal menu turnover.
- **What could be encoded in the skill:** After a closure signal, continue using merchant menus only with explicit pre-closure/version scope and check local government/press for a last-service date and owner statement. Separate seasonal sales volume from seasonal menu change. Require fresh fallback completion to include artifact, authoritative index row and diary entry.

### Phase 4 fresh-fallback supplemental return — KANEO

- **Candidate:** R-0182 KANEO Mediterranean Bar & Lounge.
- **What happened:** Fresh fallback established that the OSM bar record is also a full Mediterranean restaurant serving brunch, lunch and dinner. The return recovered current operator identity, menu/hours/about evidence, multiple house-made component statements, menu processes and ingredient origins, rating snapshots and attributed defects. It was made authoritative at index row 683 without changing its evidence.
- **Corrections from the user:** The orchestrator required authoritative registration immediately after row 682 and a diary entry. Evidence content was explicitly left unchanged.
- **What required figuring out:** Restaurant Guru labels the venue temporarily closed while the operator currently publishes hours, reservations, ordering, catering and winter hiring. A 2024 reviewer also described a multiweek closure. These facts required an unresolved temporary-status conflict, not permanent closure. Executive-chef evidence is time-dependent: 2023 press names Michael Josh Hart, while the current operator names Maja Atanasova.
- **What could be encoded in the skill:** Distinguish OSM service-format tags from the full current operating model. Model temporary closure as date/source-scoped and require operator activity plus recent reservation/order checks before status normalization. Preserve chef timelines rather than overwriting older names, and require fallback completion to include artifact, index row and diary entry.

### Phase 4 fresh-fallback supplemental return — Bangkok Thai on Main

- **Candidate:** R-0184 Bangkok Thai on Main; candidate spelling “Bankok Thai on Main.”
- **What happened:** Fresh fallback resolved the OSM misspelling to the active operator identity and recovered current menu, hours, ownership, cooking verbs, ingredient-market wording, seasonality language, ratings and attributed defects. The return was made authoritative at index row 685 without changing its evidence.
- **Corrections from the user:** The orchestrator required authoritative registration immediately after row 684 and a diary entry. Evidence content was explicitly left unchanged.
- **What required figuring out:** The typo also appears in an older municipal news record, while current operator/government DBA sources use Bangkok. The operator's “Summer Specials,” “New this summer,” and “seasonally-inspired menus” lack a year/cadence and could not establish a measured rotation. Generic sourcing from Salt Lake Asian markets names no merchant. A 2019 ownership change required historical separation from the original owners/head chef.
- **What could be encoded in the skill:** Canonicalize identity using current operator and government DBA sources while retaining source typos as aliases. Require dates and recurrence before seasonal language becomes turnover cadence. Keep generic market-class sourcing separate from named suppliers, preserve ownership timelines, and require fresh fallback completion to include artifact, index row and diary entry.
### Phase 5 repair wave 012 — nightlife food-scope and status-conflict repair

- **Candidates:** R-1117 Shades on State, R-1118 Chakra Lounge, R-1119 Jackalope Lounge, and R-1121 Varley.
- **What happened:** Restored Jackalope identity/food-format URLs, separated venue hours from food windows, added review/adverse boundaries, and normalized Varley's cuisine/format while isolating combined Ivy ratings. Unlinked review and old-menu fragments were withdrawn.
- **Corrections from the user:** None during this leaf; the dispatch identified the missing fields.
- **What required figuring out:** Nightlife venue operation does not establish kitchen operation; a directory closed label must be reconciled against current regulatory/operator evidence; adjacent sister concepts cannot share production by inference; entertainment variability is not food turnover.
- **What could be encoded in the skill:** Require separate venue/kitchen hours for bars, status-conflict resolution using regulatory/operator sources, strict isolation of combined sister-venue listings, and exact venue URLs for review mirrors and delivery-menu conflicts.
### Phase 5 repair wave 013 — identity-transition and review-URL repair

- **Candidates:** R-1123 Durango Bar, R-1124 Foodie & Sweetie DMarket, R-1126 Fácil Taquería, and R-1128 candidate Creole & Sliders Cafe/current Old Cuss Cafe.
- **What happened:** Restored government/directory provenance for Durango, restored SLUG provenance for Foodie & Sweetie, repaired review closure for Fácil, and clarified that the R-1128 candidate name/address resolves to a transitioned Old Cuss operation. Review fragments lacking exact venue URLs were withdrawn.
- **Corrections from the user:** None during this leaf; the dispatch identified missing URLs and canonical fields.
- **What required figuring out:** Nearby food references cannot create a bar menu; editorial house-made wording remains editorial; current operator identity can supersede a candidate's old name/address without proving legal continuity; historic-location reviews cannot transfer to a reopened location.
- **What could be encoded in the skill:** Require venue-specific menu provenance for bars, direct venue URLs for review platforms, explicit historic/current location scoping, and a legal-name/brand-transition field when candidate and current operator identities diverge.
### Phase 5 repair wave 014 — status and price-scope repair

- **Candidates:** R-1129 Les Bánh Mì, R-1130 Mr. Shabu, R-1131 Cliff Dining Pub, and R-1135 Soulful Sips.
- **What happened:** Withdrew unprovenanced Les Bánh Mì rebrand allegations, normalized Mr. Shabu cuisine/review/adverse boundaries, supplied Cliff's literal operator starter prices, and rebuilt Soulful Sips identity/status provenance around dated municipal opening and later platform temporary-closure evidence.
- **Corrections from the user:** None during this leaf; the dispatch identified the missing fields.
- **What required figuring out:** A platform temporary-closure label is not operator intent; municipal opening and later platform status are compatible dated snapshots; guest-side hot-pot cooking is not kitchen production; partial starter pricing cannot stand for all dayparts.
- **What could be encoded in the skill:** Require status timelines with source class/date, distinguish operator versus platform closure language, scope price completeness by menu/daypart, and require direct provenance for ownership/permitting allegations.
### Phase 5 repair wave 015 — identity, rating and brand-scope repair

- **Candidates:** R-1136 Spedelli's, R-1137 Kin Sen Thai, R-1138 Gurkhas, and R-1140 Ding Tea Taylorsville.
- **What happened:** Restored identity/source provenance, normalized platform-specific rating snapshots, closed missing price/turnover fields, and repaired review provenance. Ding Tea corporate process and footprint statements were explicitly separated from branch-level evidence.
- **Corrections from the user:** None during this leaf; the dispatch identified the missing fields.
- **What required figuring out:** Corporate SOP/process claims are not branch observations; similarly named Kin Sen locations/phones cannot be merged; directory preparation wording is not operator evidence; merchant ratings/prices require channel scope.
- **What could be encoded in the skill:** Require brand-versus-branch scope, collision handling for same-brand local locations, channel labels on ratings/prices, and direct operator provenance for production statements.
### Phase 5 repair wave 016 — review scope and unidentified-outlet closure

- **Candidates:** R-1141 Las Cazuelas, R-1142 Hidden Peaks, R-1143 Thai in Town, and R-1145 Swig Soda.
- **What happened:** Added review/adverse provenance and boundaries, isolated coffee roasting from cafe-food production, withdrew an unlinked Thai in Town Reddit fragment, and kept all Swig brand/other-outlet evidence separate from the unidentified candidate outlet.
- **Corrections from the user:** None during this leaf; the dispatch identified the missing fields.
- **What required figuring out:** Customer `everything made here` cannot expand operator claims; coffee roasting is not food production; review freshness is not sourcing; brand and nearby-outlet evidence cannot fill an unidentified outlet record.
- **What could be encoded in the skill:** Require entity resolution before outlet-level evidence, separate beverage production from food production, restrict customer production claims, and automatically quarantine brand/other-location reviews when outlet identity is unresolved.
### Phase 5 repair wave 017 — current-menu and prepared-meal scope repair

- **Candidates:** R-1146 Porch, R-1147 Fed Up Kitchen, R-1148 Vegan Bowl, and R-1151 K-Recipe.
- **What happened:** Added quotation-level review/adverse provenance, separated Porch's dated 2022 menu from 2026 reviews, constrained Fed Up's prepared-meal/weekly-menu claims, and repaired Vegan Bowl/K-Recipe review boundaries and exhaustion.
- **Corrections from the user:** None during this leaf; the dispatch identified the missing fields.
- **What required figuring out:** Old platform menus cannot silently support current claims; a `$0` trial is not ordinary pricing; ready-to-eat/reheating describes operating model rather than component production; customer authenticity/freshness statements do not establish process.
- **What could be encoded in the skill:** Require menu effective-date reconciliation, promotional-versus-ordinary price typing, prepared-meal model fields, and platform-summary versus individual-review distinction.
### Phase 5 repair wave 018 — review provenance and vendor-transition repair

- **Candidates:** R-1153 Ogie's Cafe, R-1157 Maria's Mexican Grill, R-1158 Grid City Beer Works, and R-1160 Lazy Day Cafe.
- **What happened:** Added review/adverse boundaries and exact exhaustion trails, withdrew unlinked review fragments, and kept Grid City's brewery processes separate from current Drunken Kitchen food while flagging unresolved online-menu transition evidence.
- **Corrections from the user:** None during this leaf; the dispatch identified the missing fields.
- **What required figuring out:** Directory review summaries are not individual quotations; brewery production does not transfer to a food vendor; unlinked local-review fragments cannot remain canonical; customer menu/daypart references do not establish current hours.
- **What could be encoded in the skill:** Require direct venue URLs for review mirrors, separate venue/vendor production, add current-menu transition reconciliation, and distinguish customer daypart observations from operator hours.
### Phase 5 repair wave 019 — identity-transition and adverse-currentness repair

- **Candidates:** R-1161 The Sushi/Umami, R-1163 Root'd Cafe, R-1164 El Pollo Royo, and R-1166 Ascent Kitchen.
- **What happened:** Separated legacy/current sushi identities, attributed Root'd delivery defects, constrained El Pollo Royo's raw/dog/fire claims to historical directory/review provenance, and fully closed Ascent's sparse-evidence record without negative inference.
- **Corrections from the user:** None during this leaf; the dispatch identified the missing fields.
- **What required figuring out:** Rename evidence does not establish ownership continuity; delivery mistakes are not necessarily kitchen recurrence; old adverse reports cannot establish current condition; exhaustive absence cannot prove a negative.
- **What could be encoded in the skill:** Add identity-transition review partitioning, adverse-currentness dates, merchant-order versus venue-operation defect typing, and explicit prohibition on negative inference from exhausted-unavailable fields.

### Phase 4 evidence retrieval — R-0185 Pine Cone Ridge

- **What happened:** Resolved the Park City candidate to the active Pine Cone Ridge operator and retrieved its December 2025 six-page menu, operator about page, local restaurant profile, local chef/anniversary coverage, and platform rating/review snapshots. The current menu supplied explicit handmade, house-made and homemade component wording, named products and suppliers, cooking descriptions, and full price examples; dated press supplied a seasonal-rotation statement and additional local sourcing history.
- **Corrections from the user:** None during this candidate pass. The standing user correction remains to screen for low-novelty chains rather than treating all fast food or all multi-location operators as unwanted. Pine Cone Ridge was therefore recorded as part of the local Bill White restaurant group without converting that relationship into a national-chain classification.
- **What required figuring out:** Restaurant Guru retains the former Wahso URL even though its content identifies Pine Cone Ridge. Hours conflict substantially among the local profile, Restaurant Guru and Restaurantji, so each remains source-scoped. Current production evidence had to be separated from explicitly dated 2023 menu reporting. OpenTable rating counts also differed across current and older snapshots and were preserved as time-varying observations.
- **What could be encoded in the skill:** Require inspection of linked operator PDFs rather than relying on HTML menus; add explicit handling for legacy-brand URLs that now resolve to a successor restaurant; distinguish local restaurant groups from low-novelty national chains; reconcile hours only when operator evidence supports it; and maintain separate current-versus-historical production fields for dated press coverage.

### Phase 4 fresh-fallback supplemental return — Pine Cone Ridge

- **Candidate:** R-0185 Pine Cone Ridge.
- **What happened:** Converted the completed evidence packet into the full canonical raw-evidence schema, added explicit neutral-claim boundaries and exhausted-unavailable closure, and registered the durable supplemental return at index row 686.
- **Corrections from the user:** The orchestrator required the complete canonical headings rather than the earlier compact evidence packet; evidence and source attribution were preserved without scoring or classification.
- **What required figuring out:** The Restaurant Guru page uses a legacy Wahso URL while displaying Pine Cone Ridge content; that is an identity artifact, not proof that all historic Wahso evidence transfers. Directory hours conflict and no retrieved current operator statement resolved them. The December 2025 operator menu is current-dated evidence for its own items, while November 2023 production wording remains historical.
- **What could be encoded in the skill:** Validate every return against a required-heading checklist before delivery; require neutral factual claims and an exhausted-unavailable statement after the documented source sequence; model legacy URLs separately from identity continuity; preserve unresolved hour conflicts; and require explicit effective-date scope for menus and production quotations.

### Phase 4 evidence retrieval — R-0474 Pizzeria Limone Downtown

- **What happened:** Retrieved the current operator menu, Downtown ordering page, locations/hours, values/about and nutrition language, then direct restaurant/delivery ratings, customer defects and dated local coverage. The packet preserves the operator's hand-stretched dough, house-made sauces, house-roasted/fresh marinara, fresh-baked crust and hand-shaken lemonade wording together with the nine-Utah-location statement.
- **Corrections from the user:** None during this candidate pass. The standing correction to treat low novelty rather than fast food itself as the screening target was respected by reporting the exact nine-location/local-chain facts without making any exclusion or novelty judgment.
- **What required figuring out:** The candidate phone, operator location page, operator ordering footer, Tripadvisor and directories publish several different phone numbers. Tripadvisor hours also conflict with the operator's current location hours. Brand-level process wording says preparation is fresh at every location but does not specify whether dough mixing or sauce manufacture occurs within the Downtown outlet; no kitchen-location inference was made. The avocado banner and general innovation language lack dates/cadence and therefore remain weaker than a current specials archive.
- **What could be encoded in the skill:** Add explicit brand-versus-outlet production scope, particularly for multi-location fast-casual concepts; require preservation of phone conflicts as well as hours conflicts; distinguish an undated featured-item banner from dated turnover evidence; and treat delivery-platform missing-item reports as channel-scoped unless the source identifies operational fault.

### Phase 4 fresh-fallback supplemental return — Pizzeria Limone Downtown

- **Candidate:** R-0474 Pizzeria Limone Downtown.
- **What happened:** Persisted the full canonical raw-evidence return and registered it as the successful supplemental row 688. Brand menu/process wording, outlet menu and hours, direct platform ratings, dated criticism and adverse multi-location facts remain source scoped.
- **Corrections from the user:** The orchestrator required the complete return to be durable rather than left only in the message stream; no evidence content or judgment was added.
- **What required figuring out:** `Prepared fresh at every location`, hand-stretched dough and house-made sauces do not say where dough is mixed or sauces are manufactured. The candidate phone, operator location page, operator order footer and Tripadvisor show conflicting phone numbers. Operator and Tripadvisor hours also differ.
- **What could be encoded in the skill:** Require an outlet-versus-brand production field for every multi-location candidate; audit identity across candidate, operator-location, order-system and review profiles; preserve each conflicting phone/hours value; and require a durable-return schema check before reporting completion.

### Phase 4 evidence retrieval — R-0202 Keys on Main

- **What happened:** Resolved the unnamed-coordinate bar candidate to the active Salt Lake City Keys on Main at 242 S Main, retrieved current operator hours/food scope/show policies, multi-location identity, rating snapshots, attributed customer reports and dated owner/opening coverage. The only current operator food description was `light bar fare like wings and nachos`; no itemized operator menu was found.
- **Corrections from the user:** None during this candidate pass. Raw nightlife and food-scope facts were returned without making a restaurant-eligibility or food-quality decision.
- **What required figuring out:** The operator's frequently changing schedule, audience song requests and special events describe entertainment turnover, not food turnover. Restaurant Guru supplies broad food tags, but those cannot replace an operator menu. Operator hours differ from Restaurant Guru hours. The brand has Salt Lake City, Seattle and Tacoma pages, but the FAQ explicitly says only Salt Lake City serves food while the other two allow delivered local options.
- **What could be encoded in the skill:** Add separate entertainment-versus-food turnover fields; require explicit kitchen/food-service scope for bars and music venues; prohibit directory dish tags from filling a missing operator menu; preserve location-specific food differences within a brand; and allow a canonical return to close with bar-fare scope plus itemized-menu exhausted-unavailable.

### Phase 4 fresh-fallback supplemental return — Keys on Main

- **Candidate:** R-0202 Keys on Main, Salt Lake City.
- **What happened:** Persisted the complete canonical raw-evidence packet and registered successful supplemental row 690. The operator's full retrieved food scope remains the exact `light bar fare like wings and nachos` statement; broad directory dish tags were not promoted to an operator menu.
- **Corrections from the user:** The orchestrator requested durable persistence of the complete return; no scoring, classification or expanded food claims were introduced.
- **What required figuring out:** Event schedules, audience requests and special-event covers describe entertainment change rather than food change. Salt Lake serves light food while the brand's Seattle/Tacoma venues do not. Operator and Restaurant Guru hours conflict, and no itemized operator food pricing exists in the retrieved sequence.
- **What could be encoded in the skill:** Require a bar/light-food scope field, explicit venue-level brand comparison, entertainment-versus-menu turnover typing, and an itemized-menu exhaustion path that prevents review/directory tags from filling operator evidence gaps.

### Phase 4 evidence retrieval — R-0205 Why Kiki

- **What happened:** Retrieved Why Kiki's current operator food menu, contact/hours, about and recurring event pages, plus rating platforms, attributed food/service reports and local opening/nightlife coverage. The menu explicitly labels house-made salsa, guacamole and coconut relish and names Salt City Baking buns/hoagies, Black Angus and Beyond Meat.
- **Corrections from the user:** None during this candidate pass. The venue's bar/nightlife category was not used to infer its food scope; the full operator menu was inspected.
- **What required figuring out:** The operator contact and about pages conflict on hours. Weekly dinner-show themes and recurring performances are entertainment turnover, not food-menu change. House-made wording applies only to salsa, guacamole and coconut relish; it cannot be spread to waffles, bread, sauces, desserts or fried snack formats. A Reddit claim of future closure/block redevelopment was not corroborated by operator, government or press sources.
- **What could be encoded in the skill:** Require menu inspection even for nightlife-category candidates; add component-boundary parsing for repeated `house-made` language; separate entertainment programming from food turnover; reconcile conflicting pages within the same operator site; and require corroboration before social-platform redevelopment claims become status evidence.

### Phase 4 persistence correction — R-0205 Why Kiki

- **What happened:** Persisted the already-completed full canonical return and registered it at supplemental index row 692. No evidence content was changed.
- **Correction:** The initial return existed in the message stream and diary but was not yet durable; this entry records that persistence repair.
- **Skill gap:** Require artifact existence and index-row verification before a retrieval phase is reported complete.

### Phase 4 evidence retrieval — R-0210 Café Trio Cottonwood

- **What happened:** Resolved the coordinate to the former 6405 S 3000 E Cottonwood outlet rather than the still-active Downtown Café Trio. Dated local reporting documents its formal September 28, 2019 closure; historic opening, menu/event/pricing, ratings and attributed defects were retrieved and source scoped.
- **Corrections from the user:** None during this candidate pass. Current Downtown Café Trio claims were explicitly quarantined from the closed Cottonwood outlet.
- **What required figuring out:** A Utah ABC license dataset dated May 30, 2026 still contains Café Trio at the closed address, while local closure reporting, Wanderlog and MapQuest identify the restaurant as closed. The license record establishes dataset presence only, not current operation. Park City franchise sourcing language and Downtown house-made-pasta claims could not transfer across outlets. Stale Birdeye hours similarly remain legacy directory data.
- **What could be encoded in the skill:** Require coordinate-level outlet resolution before brand research; add license-residue versus operation status typing; partition every menu, rating, production and sourcing claim by outlet; prioritize dated closure reporting over stale directory hours while preserving conflicts; and create an explicit historical-menu mode for permanently closed candidates.

### Phase 4 persistence correction — R-0210 Café Trio Cottonwood

- **What happened:** Persisted the completed full canonical closed-outlet return and registered supplemental index row 694 without changing its evidence.
- **Correction:** The initial research return and diary were complete but the durable worker artifact/index registration still had to be added.
- **Skill gap:** Require artifact existence, candidate-specific index registration and heading validation before phase completion is reported.

### Phase 4 evidence retrieval — R-0267 Top Thai Restaurant

- **What happened:** Retrieved the full current operator menu, direct-order endpoint, takeout hours/status notice, detailed price/process/menu grammar, rating snapshot and food-specific customer reports. Explicit process evidence includes marinated/grilled satay, steamed ginger rice/chicken, house ginger sauce and a 5–7-hour pork-shank braise.
- **Corrections from the user:** None during this candidate pass. No production or quality classification was made from the broad menu.
- **What required figuring out:** The operator says it does not offer delivery while Restaurant Guru links multiple delivery channels. Operator weekly takeout hours differ from directory hours, and undated `10/04`–`10/07 Closed` rows cannot be assigned to the current calendar. `House` wording applies to named ginger/sesame/curry sauces only and does not establish noodle, roti, curry-paste or broad sauce production.
- **What could be encoded in the skill:** Require channel-specific delivery status reconciliation; treat date fragments without a year as unresolved schedule exceptions; parse process duration and cooking verbs separately from house-made claims; and enforce component boundaries when `house` appears within a large menu.

### Phase 4 fresh-fallback supplemental return — Top Thai Restaurant

- **Candidate:** R-0267 Top Thai Restaurant.
- **What happened:** Persisted the full canonical return and registered successful supplemental row 696. The operator no-delivery statement, directory delivery links, conflicting hours and undated closure exceptions remain attributed rather than reconciled.
- **Corrections from the user:** The orchestrator requested durable persistence of the completed packet; evidence content remained raw and unchanged.
- **What required figuring out:** A service channel can be linked by a directory while the operator says it is unavailable. Date fragments without a year cannot modify current weekly hours. Named house sauces and a 5–7-hour braise are component-specific evidence, not proof about all sauces/curry pastes/noodles.
- **What could be encoded in the skill:** Add delivery-channel conflict typing, year-required schedule exceptions, process-duration extraction and component-scoped house-production parsing, plus artifact/index verification before completion.

### Phase 4 evidence retrieval — R-0269 Biscotts South Jordan Parkway

- **What happened:** Retrieved Biscotts' operator story, location-specific hours, complete bakery/café menus, outlet production statements, seasonal/turnover wording, owner interviews, rating snapshots and attributed defects. Operator evidence explicitly locates all cake production at South Jordan Parkway and daily from-scratch cake slices in the South Jordan bakery.
- **Corrections from the user:** None during this candidate pass. Shared ownership with Saffron Valley was reported without transferring Saffron Valley production claims to Biscotts.
- **What required figuring out:** Strong bakery production evidence is still component scoped: it covers cakes, puff pastry, macarons and named drink components, not every savory café sandwich. `Selections may vary by location` requires stock/availability caution, while the cake-production location is explicit. Operator, Toast and Tripadvisor hours conflict, and two Tripadvisor profiles appear to exist without a safe merge.
- **What could be encoded in the skill:** Capture production-location statements separately from brand-wide process claims; prevent shared-owner evidence transfer; model variable-by-location menus; require duplicate-profile quarantine; and distinguish generic local-vendor language from named supplier evidence.

### Phase 4 fresh-fallback supplemental return — Biscotts South Jordan Parkway

- **Candidate:** R-0269 Biscotts Bakery & Café — South Jordan Parkway.
- **What happened:** Persisted the completed canonical return unchanged and registered successful supplemental row 698 after the concurrently present row 697.
- **Corrections from the user:** The orchestrator required artifact/index persistence before another candidate; the evidence itself was unchanged.
- **What required figuring out:** The live index had to be checked immediately before patching so row 697 from another worker remained intact. Strong outlet-specific cake production still remains separate from unlocated savory-sandwich production and from shared-owner Saffron Valley claims.
- **What could be encoded in the skill:** Require live index conflict checks before insertion, artifact/headings/index verification after insertion, and explicit outlet-production/shared-owner isolation in durable returns.
### Phase 5 repair wave 020 — chain/brand and merchant-review scope repair

- **Candidates:** R-1167 Pacific Seas, R-2525 Honey Baked Ham, R-1169 LoLo Hawaiian BBQ, and R-1171 Señor Pollo.
- **What happened:** Added review provenance/exhaustion, withdrew delivery fragments lacking durable merchant URLs, separated corporate/brand processes from outlet kitchens, and constrained review ingredient/process claims to their sources.
- **Corrections from the user:** None during this leaf; the dispatch identified the missing fields.
- **What required figuring out:** Customer MSG speculation is not ingredient evidence; nonofficial mirrors need provenance caveats; corporate precooked/seasonal facts do not assign production to a branch; `freshly fried tortillas` does not mean tortillas made onsite.
- **What could be encoded in the skill:** Require exact merchant URLs for delivery reviews, branch scope for corporate production, mirror/operator distinction, and verb-level production parsing (`fried` versus `made`).
### Phase 5 repair wave 021 — review-summary and sparse-POI repair

- **Candidates:** R-1173 Vietopia Bistro, R-1174 Moki's Hawaiian Grill, R-1176 Blue Blue, and R-1181 Enfruta2.
- **What happened:** Added review/adverse provenance, constrained customer change/supplier claims, preserved Blue Blue identity conflicts, and fully closed Enfruta2's sparse map-only record without negative inference.
- **Corrections from the user:** None during this leaf; the dispatch identified the missing fields.
- **What required figuring out:** A question about broth duration supplies no duration; customer bakery claims are not operator sourcing; dated `new` review language is not current turnover; map cuisine labels cannot substitute for menus.
- **What could be encoded in the skill:** Reject unanswered marketing questions as evidence, require operator confirmation for customer supplier claims, date-scope novelty language, and enforce minimal-claim handling for map-only POIs.

### Phase 4 fresh-fallback supplemental return — Brio Italian Grille City Creek

- **Candidate:** R-0256 Brio Italian Grille — City Creek.
- **What happened:** Retrieved a fresh exact-branch evidence packet after the earlier candidate coverage required fallback, converted it into the full canonical raw-evidence schema, and registered the durable supplemental return at index row 687. Current operator, government, menu, rating, pricing, hours, production-language, seasonal-offer, review and adverse evidence were retained at quotation-level scope without scoring or classification.
- **Corrections from the user:** None during this candidate pass. The standing user correction remains to remove low-novelty U.S. chains rather than treating every chain or fast-food restaurant as categorically unwanted; this evidence-only return therefore records chain wording but does not apply the heuristic or classify the restaurant.
- **What required figuring out:** The candidate's older Brio Tuscan Grille alias had to be reconciled with the active Brio Italian Grille City Creek identity. Broad operator phrases such as “made from scratch family recipes” could not be expanded to every component. A 2017 in-house-preparation report concerned a different Brio location and could not be transferred to City Creek. Platform rating counts and hours had to remain source-scoped where snapshots differed.
- **What could be encoded in the skill:** Require alias/current-name resolution before evidence retrieval; distinguish exact-branch, brand-wide and other-location production claims; prevent broad scratch language from becoming component-level evidence; preserve platform snapshots independently; and keep chain/novelty heuristics outside the raw-evidence phase.
### Phase 5 repair wave 022 — automated-format and delivery-attribution repair

- **Candidates:** R-1182 Kura Sushi, R-1187 Quickly, R-1189 Crema, and R-1192 Guisados.
- **What happened:** Added review/adverse provenance, separated Kura's belt-management system from kitchen production, constrained Quickly/Crema brand and supplier claims, and preserved unresolved restaurant-versus-driver attribution for Guisados' missing order. Unlinked review fragments were withdrawn.
- **Corrections from the user:** None during this leaf; the dispatch identified the missing fields.
- **What required figuring out:** Automated freshness tracking is not scratch-production evidence; packaged menu breadth is descriptive; `locally made` is not named sourcing; delivery failure cannot automatically be assigned to restaurant or driver.
- **What could be encoded in the skill:** Add automated-service versus kitchen-process typing, named-supplier requirement for local claims, exact venue URL validation for review mirrors, and unresolved delivery-attribution fields.
### Phase 5 repair wave 023 — cross-entity review and catering-defect repair

- **Candidates:** R-1193 Thai Issan, R-1194 Canton Wok, R-1196 El Rocoto, and R-1197 ROCTACO.
- **What happened:** Removed a HappyCow review misassociated with Thai Issan, added review/adverse boundaries, withdrew El Rocoto fragments lacking durable Tripadvisor URL, and preserved ROCTACO's catering report as attributed customer evidence.
- **Corrections from the user:** None during this leaf; the dispatch identified the missing fields.
- **What required figuring out:** Same-cuisine review pages can be misattached across restaurants; menu labels such as homemade do not always identify source class; food-safety and catering allegations need direct provenance/operator follow-up.
- **What could be encoded in the skill:** Validate restaurant identity on every review URL, type menu-label versus operator claim, and require direct platform URL plus follow-up search for safety/catering allegations.

### Phase 4 fresh-fallback supplemental return — Santorini's Sandy

- **Candidate:** R-0199 Santorini's — Sandy.
- **What happened:** Resolved the sparse OSM candidate to the active Sandy outlet, retrieved the full canonical raw-evidence set, and registered the durable supplemental return at index row 689. The return preserves exact-outlet operator process wording, broader brand production statements, multi-location ownership/franchise facts, menu and price snapshots, rating conflicts, and attributed food/service defects without scoring or classification.
- **Corrections from the user:** None during this candidate pass. The standing user correction remains that the inexpensive heuristic should identify low-novelty U.S. chains rather than reject fast food or multi-location restaurants categorically; chain and fast-casual facts were therefore recorded as raw evidence only.
- **What required figuring out:** Current official pages use Santorini's while the OSM record and directories vary among Santorinis and Santorini's Greek Grill. The exact Sandy article supplies in-house tzatziki and cooked-to-order protein wording, while hand-cut chicken and other house-made sauces appear on a brand-wide page and had to remain separately scoped. Platform counts changed between snapshots, and customer claims such as “homemade” or “tastes canned” could not become operator production facts.
- **What could be encoded in the skill:** Require canonical-name/alias reconciliation; type every process quotation as outlet-specific, brand-wide or customer-reported; preserve historical platform snapshots rather than overwrite conflicts; prevent customer sensory language from becoming production evidence; and keep low-novelty-chain heuristics downstream of evidence retrieval.
### Phase 5 repair wave 024 — directory-summary and venue-policy repair

- **Candidates:** R-1198 Canyons Coffee, R-1199 Arigato Sushi, R-1200 Good Spirits, and R-1202 Taquería El Rey de Oros.
- **What happened:** Added review/adverse boundaries, withdrew Arigato review text lacking a durable direct URL, separated Good Spirits kitchen/venue policy, and preserved Taquería phone conflict without adverse inference.
- **Corrections from the user:** None during this leaf; the dispatch identified the missing fields.
- **What required figuring out:** Directory `house baked`/`homemade` wording is not operator evidence; venue 21+ policy is not adverse; menu breadth does not establish production; phone conflict alone is not an operational defect.
- **What could be encoded in the skill:** Type directory summary versus operator claims, separate venue policies/kitchen hours, require direct review URLs, and prohibit adverse inference from contact conflicts.
### Phase 5 repair wave 025 — historical-review and service-format repair

- **Candidates:** R-1203 Dee Garden, R-1204 BFF Turon, R-1205 Naivedhyam Cafe, and R-1207 Monarca.
- **What happened:** Added review/adverse provenance, separated delivery/customer process observations, treated turo-turo as service format, isolated historical SV Cafe reviews from current Naivedhyam, and preserved Monarca's dated turnover/review evidence.
- **Corrections from the user:** None during this leaf; the dispatch identified the missing fields.
- **What required figuring out:** Customer cooking observations are not operator process; held/display service does not prove production timing; predecessor reviews cannot transfer across rebrands; dated removal reviews complement but do not replace operator turnover claims.
- **What could be encoded in the skill:** Add service-format typing, predecessor/current review partitioning, customer-observation process limits, and dated review-based menu-change fields.

### Phase 4 fresh-fallback supplemental return — Ivy & Varley

- **Candidate:** R-0203 Ivy & Varley, candidate alias The Ivy.
- **What happened:** Resolved the candidate name to the current combined Ivy & Varley identity, retrieved the complete canonical raw-evidence set, and registered the durable supplemental return at index row 691. The packet preserves current menu component wording, dated menu and holiday-offer facts, review defects, connected-venue/shared-kitchen structure and operator-group links without scoring or classification.
- **Corrections from the user:** None during this candidate pass. The standing user correction remains to use low-novelty U.S. chain heuristics rather than categorical fast-food or multi-location exclusions; Realine/operator-group evidence was recorded factually and not converted into a heuristic result.
- **What required figuring out:** The OSM candidate says The Ivy while current operator material combines Ivy & Varley and separately addresses Varley Lounge. Food production evidence had to be distinguished from Varley cocktail sourcing. A “Summer Salmon” item name and dated menu update do not independently establish a recurring seasonal cadence. Connected spaces share a kitchen, but that does not make every room-specific claim interchangeable.
- **What could be encoded in the skill:** Require venue/room/shared-kitchen identity modeling; distinguish food and beverage production evidence; prevent seasonal item names from becoming rotation claims; type operator-group links separately from national-chain heuristics; and preserve candidate aliases alongside current canonical branding.
### Phase 5 repair wave 026 — nonrestaurant format and identity-transition repair

- **Candidates:** R-1208 IndieGo Coffee, R-1210 June's Southern Table, R-1211 Magpie, and R-1213 Tonkotsu.
- **What happened:** Added review/adverse closure, separated item ratings from prose reviews, constrained ghost-kitchen/farmers-market formats, and preserved Tonkotsu rename/suite conflicts without closure inference.
- **Corrections from the user:** None during this leaf; the dispatch identified the missing fields.
- **What required figuring out:** Item percentages are not review quotations; ghost-kitchen and packaged-market formats are not adverse; departure fragments need durable social URLs; merchant closed states do not prove venue closure.
- **What could be encoded in the skill:** Type numeric item feedback versus prose, add nonrestaurant-format fields, require durable social URLs for transitions, and separate delivery-channel state from business status.
### Phase 5 repair wave 027 — customer-process and identity-conflict repair

- **Candidates:** R-1214 Shanasheel, R-1215 Long Life, R-1216 Bhansa Ghar, and R-1218 Hot Oven Pizza.
- **What happened:** Added review/adverse provenance, withdrew unlinked merchant/mirror fragments, constrained customer fresh/house-made claims, and preserved phone/name conflicts without adverse inference.
- **Corrections from the user:** None during this leaf; the dispatch identified the missing fields.
- **What required figuring out:** Customer production claims require operator confirmation; legacy URL slugs do not establish current ownership; missing delivery components differ from cooking defects; contact conflicts are identity issues.
- **What could be encoded in the skill:** Require operator confirmation for customer process statements, type order-completeness versus food defects, track legacy-slug history, and prohibit adverse inference from phone conflicts.
### Phase 5 repair wave 028 — status, reaction and item-name repair

- **Candidates:** R-1219 Gordo's, R-1222 Habanero Express, R-1223 Tamarind, and R-1225 Alice's Kitchen.
- **What happened:** Added review/adverse provenance, separated closure/status and stockouts from turnover, constrained Tamarind reaction evidence to unclear-cause customer reporting, and treated homemade wording in Alice's item name as name-only evidence.
- **Corrections from the user:** None during this leaf; the dispatch identified the missing fields.
- **What required figuring out:** Platform closure labels lack cause/date; stockouts are not rotation; customer reactions require causation restraint; `homemade` in an item name is weaker than operator process wording.
- **What could be encoded in the skill:** Add closure-timeline fields, availability-versus-turnover typing, adverse-causation boundaries, and item-name versus description/operator-claim provenance.

### Phase 4 fresh-fallback supplemental return — The Green Pig Pub

- **Candidate:** R-0206 The Green Pig Pub.
- **What happened:** Retrieved and normalized the complete canonical raw-evidence set for the active downtown pub and registered the durable supplemental return at index row 693. The return captures current item-level production wording, daily soup and specials/seasonal-fruit language, menu breadth, owner/history facts, rating conflicts and attributed delivery/service defects without scoring or classification.
- **Corrections from the user:** None during this candidate pass. The standing user correction remains to target low-novelty U.S. chains rather than categorically reject pubs, fast food or multi-location restaurants; pub/bar format and menu breadth were recorded as facts only.
- **What required figuring out:** Strong production claims applied to specific items—egg rolls, sliders, fries, chips, croutons and daily soup—and could not be expanded to breads, tortillas, vegan substitutes or every sauce. A noncanonical GitHub mirror claimed the entire menu was made in house, but it lacked current operator provenance and was quarantined from canonical evidence. Official venue hours and directory closing hours differed, while kitchen and late-night menu cutoffs formed separate service windows.
- **What could be encoded in the skill:** Require component-level scope for every production verb; flag unofficial domain mirrors and prohibit their promotion without operator provenance; model venue, kitchen, delivery and late-night hours separately; distinguish daily availability language from broader turnover; and keep pub/bar format outside evidence-phase eligibility judgments.
### Phase 5 repair wave 029 — hosted-review and pre-opening-state repair

- **Candidates:** R-1226 Eggsburgh, R-1227 Kahve, R-1228 Tea's Memory, and R-1231 Beehive Bitez.
- **What happened:** Added review/adverse boundaries, withdrew unlinked mirror fragments, restored Tea's Memory relocation provenance, and constrained Beehive Bitez to its hiring/pre-opening evidence while isolating Provo sibling process claims.
- **Corrections from the user:** None during this leaf; the dispatch identified the missing fields.
- **What required figuring out:** Operator-hosted reviews are not independent; uncertain syrup statements must preserve uncertainty; relocation histories need current/legacy source separation; hiring ads establish pre-opening state, not opening failure.
- **What could be encoded in the skill:** Type hosted versus independent reviews, preserve uncertainty tokens, model relocation lineage, and distinguish pre-opening hiring from open/closed status.
### Phase 5 repair wave 030 — relocation/rebrand review partitioning

- **Candidates:** R-1232 Old Cuss, R-1233 Phở 9, R-1234 Red Basil, and R-1237 Muertos Cantina.
- **What happened:** Added review/adverse boundaries, withdrew unlinked merchant/mirror fragments, separated Old Cuss former/current location evidence and Muertos pre/post-rebrand reviews, and preserved Phở 9 ZIP conflict without status inference.
- **Corrections from the user:** None during this leaf; the dispatch identified the missing fields.
- **What required figuring out:** Reviews must be partitioned across moves/rebrands; customer from-scratch claims are not operator production evidence; ZIP conflicts do not imply closure; new/day soup labels need cadence restraint.
- **What could be encoded in the skill:** Require location/rebrand review time partitioning, direct merchant URL validation, contact-conflict neutrality, and typed new-item/daily-slot versus rotation evidence.

### Phase 4 fresh-fallback supplemental return — Greek Souvlaki Murray

- **Candidate:** R-0211 Greek Souvlaki — Murray.
- **What happened:** Resolved the OSM record to the active Murray outlet, retrieved the full canonical raw-evidence set and registered the durable supplemental return at index row 695. Current menu/rating/hour evidence, family ownership and multi-location history, historical production reporting, current item wording and attributed outlet-specific defects were preserved without scoring or classification.
- **Corrections from the user:** None during this candidate pass. The standing user correction remains to screen for low-novelty U.S. chains rather than reject every multi-location or fast-food business; the family chain and quick-bites labels were recorded as source facts only.
- **What required figuring out:** Current DoorDash calls rice pudding homemade, while broader homemade-food claims came from a 2007 family profile and could not be treated as current all-menu evidence. Operator hours say Sunday closed while Tripadvisor displays Sunday service. Platform rating counts shifted between snapshots. Piraeus is the concept's historical inspiration, not current ingredient sourcing.
- **What could be encoded in the skill:** Require effective-date scope for production claims; distinguish current item descriptions from historical operator profiles; preserve outlet/platform hour conflicts; type inspiration/origin stories separately from sourcing; and keep local-family chain facts separate from downstream low-novelty heuristics.
### Phase 5 repair wave 031 — review provenance and neutral-claim boundaries

- **Candidates:** R-1238 Rivas, R-1241 Chonchis Taco Shop, R-1244 Javier’s, R-1249 2 Row Brewing.
- **What happened:** Re-ran the required operator-first sequence, followed by merchant/review platforms, government records where relevant, and broader directory/community/search sources. Added exact review passages or close factual paraphrases, adverse attribution limits, neutral-claim boundaries, explicit search trails, and unavailable closure with actual 2026-07-16 access dates.
- **Corrections required from the user:** None during this wave.
- **What required interpretation:** Review-platform excerpts needed to remain customer allegations rather than verified defects; branch numbering did not prove a franchise relationship; “fresh/authentic” customer language did not prove production; Javier’s named-item process wording could not be generalized; and 2 Row’s “House made”/“food made in our kitchen” wording did not identify component-level processes.
- **What could be encoded in the skill:** Require durable exact provenance before retaining any review fragment; automatically withdraw fragments whose venue URL cannot be recovered; distinguish customer sensory/process impressions from operator claims; constrain named-item production language to that item; and require broad kitchen-location claims to be recorded separately from component-specific production.

### Phase 4 fresh-fallback supplemental return — Kokonut Hawaiian BBQ Salt Lake City

- **Candidate:** R-0268 Kokonut Hawaiian BBQ — Salt Lake City, candidate legacy name Kokonut Island Grill.
- **What happened:** Resolved the candidate to the active rebranded operator at the same address and phone, retrieved the full canonical raw-evidence set and registered the durable supplemental return at index row 697. The packet preserves current identity/menu/hours, legacy legal and brand names, multi-location/investment facts, rating conflicts, customer warmer observations and explicit production exhaustion without scoring or classification.
- **Corrections from the user:** None during this candidate pass. The standing user correction remains to identify low-novelty U.S. chains rather than categorically reject all fast-casual or multi-location restaurants; brand/chain facts were therefore recorded without applying the heuristic.
- **What required figuring out:** Current branding/domain changed from Kokonut Island Grill to Kokonut Hawaiian BBQ while directory and legal records retain the old name. A customer reported food held in warmers, but this could not be promoted to operator process. A different outlet's customer said everything was made in house, which could not transfer to Salt Lake City. Investment/fraud reporting concerned management and proposed restaurant financing, not food production.
- **What could be encoded in the skill:** Require same-address/phone rebrand resolution; partition legacy/current identities and reviews; type customer operational observations separately from operator methods; prohibit other-outlet process transfer; distinguish corporate/legal adverse facts from kitchen evidence; and keep chain heuristics downstream of evidence collection.
### Phase 5 repair wave 032 — durable review provenance and tenant separation

- **Candidates:** R-1250 Chabaar Beyond Thai, R-1251 Café Guanaco, R-1252 Bountiful Greek Cafe, R-1444 Houston TX Hot Chicken.
- **What happened:** Re-ran operator-first, merchant/review, and broader directory/editorial/community searches. Added durable review passages, source-type/access-date labels, adverse attribution limits, neutral boundaries, exact ordered trails, and explicit unavailable closure.
- **Corrections required from the user:** None during this wave.
- **What required interpretation:** Chabaar’s address/status sources conflict without proving closure; customer spoilage language at Café Guanaco is not a safety finding; Bountiful Greek’s aggregator freshness language does not establish component production; and Crack Shack predecessor evidence cannot transfer to Houston TX Hot Chicken.
- **What could be encoded in the skill:** Require current-tenant partitioning before review use; treat status/address disagreements as unresolved conflicts; distinguish customer sensory allegations from official findings; withdraw search snippets without durable venue passages; and scope “house made,” “fresh made,” or named cooking-method language to the specifically named component.

### Phase 5 repair wave 033 — parser vocabulary versus semantic evidence

- **What happened:** The original worker repaired R-1256, R-1257, R-1258, and R-1261 with attributed review/adverse passages, neutral boundaries, a literal five-stage source sequence, explicit unavailable closure, and withdrawals. The classified-only east-side dessert sweep also completed with 15 confirmed and 6 plausible/unproven places.
- **Corrections required from the user:** None.
- **What required interpretation:** The deterministic preflight rejected the heading `Exact required source sequence/search trail` even though its content met the semantic contract. I added that heading as an accepted parser alias and re-ran the audit; no evidence was altered or promoted.
- **What could be encoded in the skill:** If deterministic helpers validate required headings, define a canonical machine-readable heading set or require normalization before validation. Equivalent descriptive headings should not generate false evidence defects. A classified-only side inventory should also record omissions relative to prior summaries; that caught Banbury Cross, Greenhouse Effect, and Thirst.

### Phase 5 primary semantic review batch 001

- **What happened:** Directly read and evaluated the complete return sections for the first ten evidence-population records (R-0020, R-0021, R-0022, R-0023, R-0024, R-0026, R-0027, R-0030, R-0031, and R-0032). All ten meet the semantic evidence contract; the detailed decisions are durable in `05-primary-semantic-review.md`.
- **Corrections required from the user:** None.
- **What required interpretation:** In-record source nicknames such as “Official menus” are acceptable only when they resolve unambiguously to a linked source in the same venue section and the applicable access date is explicit. Generic “from-scratch,” “fresh,” and local language remained quotations with narrow scope. Historic and user-generated facts remained visibly typed and dated.
- **What could be encoded in the skill:** State whether provenance may be normalized at venue-section level or must repeat inline on every bullet. The current contract requires provenance for every accepted claim but does not explicitly say whether an unambiguous same-record linked-source reference is valid.

### Phase 5 primary semantic review batch 002

- **What happened:** Directly inspected the next ten population records (R-0033 through R-0070 in evidence order) across two raw-return artifacts. All ten were semantically accepted; cumulative primary review is 20 records.
- **Corrections required from the user:** None.
- **What required interpretation:** Closed and temporarily closed venues still require evidence acceptance even though operational disposition is deferred to Phase 6. Historic menu/product language cannot be transferred to a current state. A batch-level access-date declaration can supply the date for venue claims, but source identity and role still must resolve inside each venue section.
- **What could be encoded in the skill:** Explicitly distinguish evidence acceptance from operational eligibility for closed venues, and specify whether batch-level provenance declarations are valid normalization. This would reduce repeated judgment during large runs.

### Phase 5 primary semantic review batch 003

- **What happened:** Directly inspected records 21–30 in evidence-population order across three return artifacts. All ten were semantically accepted; cumulative direct review is 30 records.
- **Corrections required from the user:** None.
- **What required interpretation:** Government-building ratings/hours cannot establish a cafeteria operation; a BBB business grade is not a restaurant rating; off-site group production must stay attached to the named component; and multi-outlet or mail-distribution facts are adverse facts without becoming automatic verdicts in Phase 5.
- **What could be encoded in the skill:** Add explicit source-type exclusions for non-restaurant business ratings and stronger examples for parent-building evidence, off-site group production, and current-versus-historical operations.

### Phase 5 primary semantic review batch 004

- **What happened:** Directly inspected records 31–40. Eight were evidence-accepted and two identity/operation-poor records were accepted only as `evidence-exhausted-unavailable`; cumulative review is 40 records.
- **Corrections required from the user:** None.
- **What required interpretation:** An unresolved multi-branch identity can close only as exhausted, with all observed branch evidence quarantined from the candidate. Mall-wide hours and tenant labels cannot establish outlet hours or menu. National-brand context and guest-performed cooking remain raw adverse/operational facts rather than Phase 5 judgments.
- **What could be encoded in the skill:** Provide a formal `evidence-exhausted-unavailable` example for unresolved branch identity and another for tenant listings where parent-facility evidence is the only surviving source.

### Phase 5 primary semantic review batch 005

- **What happened:** Directly inspected records 41–50. Six were evidence-accepted and four identity- or branch-limited records closed as evidence-exhausted-unavailable; cumulative direct review is 50.
- **Corrections required from the user:** None.
- **What required interpretation:** Same-brand address changes without a rebrand/relocation link cannot be silently merged; unrelated national-chain results must be explicitly rejected; company-wide process may survive while every branch-local field remains unavailable; and mall hours remain parent-facility evidence.
- **What could be encoded in the skill:** Add reusable field states for `candidate-branch-unresolved`, `same-brand-address-conflict`, and `unrelated-chain-rejected`, so these common identity outcomes do not need prose-only normalization.

### Phase 5 primary semantic review batch 006

- **What happened:** Directly inspected records 51–60. Seven were evidence-accepted and three branch/field-poor records closed as evidence-exhausted-unavailable; cumulative direct review is 60.
- **Corrections required from the user:** None.
- **What required interpretation:** Customer-performed station or tableside cooking is valid operational evidence but not kitchen process breadth; reconstructed returns can pass when batch/record provenance resolves fully; longevity never substitutes for production evidence; and original-branch closure cannot resolve an unspecified current branch.
- **What could be encoded in the skill:** Add explicit examples for customer-configured cooking stations, reconstructed-return provenance, and group records where an original closure coexists with several current branches.

### Phase 5 primary semantic review batch 007

- **What happened:** Directly inspected records 61–70 in the reconstructed batch. Eight were evidence-accepted and two branch-unresolved records closed as evidence-exhausted-unavailable; cumulative direct review is 70.
- **Corrections required from the user:** None.
- **What required interpretation:** Customer “homemade” wording remains review evidence; user reports of same menus do not prove branch identity; weekly customer habits are not operator cadence; stockouts are not turnover; and company-wide production cannot fill missing branch identity.
- **What could be encoded in the skill:** Add concise negative examples for customer process adjectives, customer-habit cadence, same-menu identity inference, and stockout-versus-turnover separation.

### Phase 5 primary semantic review batch 008

- **What happened:** Directly inspected records 71–80. Six were evidence-accepted and four sparse or adjacent-operation records closed as evidence-exhausted-unavailable; cumulative direct review is 80.
- **Corrections required from the user:** None.
- **What required interpretation:** Connected or neighboring food operations cannot supply a bar’s kitchen evidence; press-level general scratch wording stays non-component-specific; generic names require explicit namesake rejection; “special sauce” and “authentic” are not process evidence; fixed menu structure is descriptive only.
- **What could be encoded in the skill:** Add examples for adjacent-business evidence isolation, generic-name collision closure, and general press scratch claims versus component-level process.

### Phase 5 primary semantic review batch 009

- **What happened:** Directly inspected records 81–90. Seven were evidence-accepted and three sparse/conflicted identities closed as evidence-exhausted-unavailable; cumulative direct review is 90.
- **Corrections required from the user:** None.
- **What required interpretation:** Hotel restaurant context must remain scoped; event packages are not recurring turnover; government co-listings do not prove ownership; customer crispness/freshness is not process evidence; negative ingredient claims do not establish scratch breadth; historical local ownership does not establish current operations.
- **What could be encoded in the skill:** Add formal examples for hotel-contained restaurants, event-only menus, government-record co-listing limits, and negative ingredient claims such as no MSG/lard.

### Phase 5 primary semantic review batch 010

- **What happened:** Directly inspected records 91–100. Six were evidence-accepted and four status/menu-sparse records closed as evidence-exhausted-unavailable; cumulative direct review is 100.
- **Corrections required from the user:** None.
- **What required interpretation:** Time-of-day “Closed Now” is not closure; a menu-update date is not cadence; projected openings are not current status; live-show schedules are not food turnover; cocktail mixing is not kitchen production; delivery temperature requires separate causation.
- **What could be encoded in the skill:** Add negative examples for platform `Closed Now`, projected openings, non-food event cadence, and bar-preparation evidence versus kitchen process.

### Phase 5 primary semantic review batch 011

- **What happened:** Directly inspected records 101–110. Eight were evidence-accepted and two sparse/lounge-coffee records closed as evidence-exhausted-unavailable; cumulative direct review is 110.
- **Corrections required from the user:** None.
- **What required interpretation:** Live sites can conflict with user closure threads; longevity is not turnover; seasonal operating labels are not component rotation; branded sauce is not house production; barista consistency/customer roasting claims remain customer evidence; group ownership is not production evidence.
- **What could be encoded in the skill:** Add examples for live-site/status conflict, operating-season versus menu-seasonality, and branded ingredients versus house-made components.

### Phase 5 primary semantic review batch 012

- **What happened:** Directly inspected records 111–120. Eight were evidence-accepted and two branch-unspecified company records closed as evidence-exhausted-unavailable; cumulative direct review is 120.
- **Corrections required from the user:** None.
- **What required interpretation:** A provisional nearest branch is not candidate identity; parent-resort coffee-brand conflicts remain unresolved; company-wide scratch claims can survive while candidate branch attachment fails; other-branch allergy complaints cannot transfer; customer pre-cooked/reheat statements remain allegations.
- **What could be encoded in the skill:** Add examples for provisional-nearest-branch rejection, parent-resort versus outlet sourcing conflicts, and company evidence retained alongside unresolved candidate identity.

### Phase 5 primary semantic review batch 013

- **What happened:** Directly inspected records 121–130. All ten were evidence-accepted; cumulative direct review is 130.
- **Corrections required from the user:** None.
- **What required interpretation:** Central group production must stay separately scoped; global fish origins are not fisheries; availability caveats are not turnover; platform changes are not menu changes; separate hotel bar menus cannot transfer to buffet; customer frozen/canned claims remain allegations.
- **What could be encoded in the skill:** Add examples for central-group bakery evidence, platform-change versus menu-change, and hotel buffet versus adjacent bar-menu partitioning.

### Phase 5 primary semantic review batch 014

- **What happened:** Directly inspected records 131–140. Six were evidence-accepted and four branch/identity/historical records closed as evidence-exhausted-unavailable; cumulative direct review is 140.
- **Corrections required from the user:** None.
- **What required interpretation:** Beer production does not transfer to food; platform ordering unavailability is not closure; family recipes are not process; historical operation is not current evidence; parent-amusement-park facts cannot supply stand details; near-name/out-of-state collisions require explicit rejection.
- **What could be encoded in the skill:** Add examples for brewery-process isolation, ordering-platform status, amusement-park stand evidence, and historical-versus-current identity closure.

### Phase 5 primary semantic review batch 015

- **What happened:** Directly inspected records 141–150. Eight were evidence-accepted and two identity/branch-unresolved records closed as evidence-exhausted-unavailable; cumulative direct review is 150.
- **Corrections required from the user:** None.
- **What required interpretation:** Frozen dessert names are not systemic frozen-food evidence; shipped beans do not establish roasting location; historical seasonal PDFs are not recurring cadence; “Made with care” is not process; central campus branding does not resolve branch identity; closure and wage allegations remain attributed conflicts.
- **What could be encoded in the skill:** Add examples for product-name false positives (`frozen pie`), roasting-location inference, historical-menu cadence, and multi-kiosk campus identity.

### Supplemental classified-only east-side scratch-dessert reconciliation

- **What happened:** Reconciled every already-classified dessert lead in Millcreek/East Millcreek, Sugar House, 9th & 9th, 15th & 15th, the Avenues and adjacent central-east neighborhoods. The resulting inventory separates 10 dedicated/dessert-forward producers, 5 restaurants with substantiated dessert programs, 6 plausible-but-unproven candidates and 1 explicit non-producer. It also reports already-collected day-specific 8 PM availability without doing new catchment discovery.
- **Corrections from the user:** The standing correction remains that chain or fast-food format is not itself a reason to exclude a place; the target is low-novelty standardization. Consequently Sidecar and Thirst remain confirmed because their in-house/store-level production is unusually explicit.
- **What required figuring out:** The earlier supplemental summary had omitted three completed returns—Banbury Cross (R-2290), Greenhouse Effect (R-2353) and Thirst (R-2589). Tulie required alias reconciliation from ledger name `Tulie's Cafe` to official identity Tulie Bakery. Thirst required separating central-bakery cookie production from store-level beignet and pretzel production. An 8 PM closing time was treated as a boundary rather than “open at 8.”
- **What could be encoded in the skill:** Build corridor inventories by querying structured candidate IDs/statuses and address coordinates rather than searching prior prose summaries; join aliases by candidate ID plus normalized address; require a completeness check against all successful returns; type production location as venue, branch, or central bakery; and represent late availability as after-8, closes-at-8 boundary, conditional service, or unavailable—not a single boolean.
### Phase 5 repair wave 033 — canonical source ordering and branch-local review scope

- **Candidates:** R-1256 Twisted Fern, R-1257 Silverlake Ramen, R-1258 Dirty Bird Fried Chxx, R-1261 Beirut Cafe.
- **What happened:** Read the Phase 5 acceptance contract, shared provenance contract, and full canonical restaurant worker prompt immediately before repair. Re-ran and documented the required five-stage source sequence, added durable review/adverse passages, neutral claim boundaries, and explicit exhausted-unavailable closures.
- **Corrections required from the user:** None during this wave.
- **What required interpretation:** Chain-level Silverlake allegations could not become Riverton facts; Dirty Bird’s Reddit closure discussion conflicts with a live merchant page; customer “fresh made” wording could not become operator process evidence; and Twisted Fern customer criticisms were meal-specific rather than recurring findings.
- **What could be encoded in the skill:** Make the five-stage source order a required enumerated return field; require branch-local gating for chain adverse evidence; automatically flag live-merchant versus community-closure conflicts; require vague aggregator fragments to be withdrawn when exact passages cannot be renewed; and force customer process adjectives into neutral review evidence rather than operator production.

### Phase 4 supplemental evidence — R-0425 Ramen Legend

- **What happened:** Followed the restaurant evidence sequence for Ramen Legend. The operator site and official-linked SpotOn menu supplied the current identity, hours, extensive menu, prices, and direct wording for traditional hand-made noodles and slow-cooked broths. Official social accounts were found but fetch-throttled. Public-review, local-publication/interview, and direct-rating searches supplied multiple literal rating snapshots, attributed product/defect observations, and explicit unavailable closure. The raw return was saved as batch 699 and indexed; no rubric judgment was made.
- **Corrections from the user:** None during this candidate pass. The standing correction remains to distinguish low-novelty U.S. chains from fast food or multi-location restaurants generally; the evidence pass therefore recorded menu breadth and searched for chain ownership without applying that heuristic.
- **What required figuring out:** The root skill points to `../reference/phase-4-evidence-research.md` relative to the `restaurant-rubric` directory, while the worker prompt remains inside `restaurant-rubric/`; trying both under `restaurant-rubric/reference/` failed. Rating and hours snapshots conflicted across official, Tripadvisor, Restaurantji, Google-attributed aggregators and delivery platforms. Customer references to frozen cheesecake and refrigerated toppings had to remain customer observations rather than operator process. Too Good To Go’s leftover-prepared-item language is a current sales fact but does not identify how the original items were produced.
- **What could be encoded in the skill:** State the mixed Phase 4 reference paths explicitly; require an ordered source-snapshot table when ratings/hours conflict; distinguish operator production language from customer storage/reheating observations; type surplus-rescue listings as end-of-day inventory evidence rather than production evidence; and make social fetch failure an explicit unavailable subtype rather than silently treating a found account as searched content.
### Phase 5 repair wave 034 — historical identity conflicts and fee-review attribution

- **Candidates:** R-1262 Jim’s Family Restaurant, R-1263 Murphy’s Cafe 126, R-1264 Maize, R-1266 Cosmica.
- **What happened:** Re-ran the canonical five-stage source sequence, retained venue-level review passages, added adverse attribution and neutral scope limits, documented exact queries, and closed unavailable fields only after the full sequence.
- **Corrections required from the user:** None during this wave.
- **What required interpretation:** Murphy’s older phone/address could not override current operator identity; customer fee complaints were historical reports rather than current pricing; Maize’s off-site tortilla fact did not identify a commissary or production kitchen; and Cosmica critic texture language did not become operator production evidence.
- **What could be encoded in the skill:** Require a historical/current identity partition for phone/address conflicts; date-gate customer price and fee reports; distinguish off-site production from unnamed commissary inference; scope critic cooking observations separately from operator process; and withdraw partial adverse fragments when the renewed page does not expose the exact passage.

### Phase 4 supplemental evidence — R-0441 Copper King

- **What happened:** Resolved the coordinate-only discovery record to 9071 W Magna Main Street and found Copper King in 2003/2011 press and historical licensing. Current government licensing, operator social pages and directories instead identify Copper Miner Saloon at that address. Historical Copper King facts were returned separately from current-tenant identity/status facts; current menu, ratings and reviews were not transferred. The full source sequence produced explicit exhausted-unavailable closures for historical food evidence, and batch 701 was saved/indexed without a rubric judgment.
- **Corrections from the user:** None during this candidate pass. The standing correction remains that bar or fast-service format is not itself exclusion evidence and that the downstream heuristic targets low-novelty U.S. chains; neither the historical bar format nor current tenant succession was judged here.
- **What required figuring out:** Untappd displays Copper King at 8979 W Magna Main while historical press, business records, licensing and the OSM coordinate resolve to 9071 W Magna Main. Current DABS naming is Copper Miner Saloon, but an older government dataset labels the license Copper King I. Separately named Adam’s Islandstyle Grill food ordering appears at the current saloon address. This required address-confidence weighting, current/historical tenant partitioning, and avoidance of menu/review transfer.
- **What could be encoded in the skill:** Require coordinate-to-parcel/address reconciliation when discovery lacks an address; treat government license-name changes at one address as a mandatory tenant-successor audit; prohibit successor/predecessor transfer of menu, rating and process evidence absent explicit continuity; type co-located pop-ups/food trucks separately from host-bar kitchens; and require conflicting-address quarantine for unverified check-in platforms.

### Phase 4 supplemental evidence — R-0447 Wing Coop

- **What happened:** Completed the five-stage source sequence for the Wasatch Boulevard Wing Coop. The official site supplied the sauce grammar and literal ingredient descriptions; current government/map/menu sources supplied identity, hours, prices and format; review and local-press sources supplied ratings, historical awards and attributed product defects. The former Marmalade branch was separated from the current Wasatch venue. Batch 704 was saved/indexed with all canonical fields and no rubric judgment. A concurrent worker claimed 703 between the pre-write check and verification, so this return was renumbered before handoff.
- **Corrections from the user:** None during this candidate pass. The standing correction remains that the heuristic targets low-novelty standardized U.S. chains rather than all fast food or multi-location operators; branch history and menu specialization were therefore recorded without a verdict.
- **What required figuring out:** The official site describes sauce ingredients but never says the sauces are made by the restaurant, so ingredient composition could not become production evidence. Yelp-derived scores differ across MapQuest, Apple Maps and Stacker snapshots. Uber Eats labels only its ordering relationship closed, while official ordering, licensing and current directories show the venue active. The Marmalade branch is closed and could not supply current Wasatch facts.
- **What could be encoded in the skill:** Explicitly distinguish recipe-description language from production-location/method language; type platform closure separately from venue closure; require branch-local handling of multi-outlet ratings and reviews; preserve dated award/menu claims without treating them as current turnover; and require a current-location inventory before applying any downstream novelty-chain heuristic.

### Phase 4 supplemental evidence — R-0459 Spitz Sugarhouse

- **What happened:** Completed the required source sequence. Operator sources supplied strong company-wide production claims, branch identity/hours, menu structure and seasonal drink language; founder press supplied the thirty-location chain fact; Tripadvisor supplied branch review text. All claims were scoped to company or branch as displayed. Batch 706 was saved/indexed without judgment; a concurrent return claimed 705 during the write, so this return was renumbered at verification.
- **Corrections from the user:** None during this pass. The standing correction remains that the downstream filter targets low-novelty standardized U.S. chains, not chains or fast-casual formats categorically; chain scale and local variation were recorded as separate facts.
- **What required figuring out:** The site asserts in-house sauces/daily prep company-wide while also saying breads/meats come from outside producers to proprietary recipes and items vary by location. Tripadvisor exposed 59 branch reviews but not a literal overall branch score, while a nearby Spitz listing had 240 reviews and could not be merged.
- **What could be encoded in the skill:** Require company-wide versus branch-local claim typing; treat proprietary supplier production separately from in-store production; prohibit merging same-brand Tripadvisor profiles; and include locally customized drinks/decor as typed variation evidence without letting it substitute for food-production evidence.

### Phase 4 supplemental evidence — R-0829 Curry Fried Chicken

- **What happened:** Resumed the partial fallback and completed all five source stages. Food Network’s restaurant-supplied professional recipe provided precise spice-toasting/grinding, 24-hour brine, dredging, frying, lentil-curry and onion-finish evidence. Official ordering, Tripadvisor, Axios, local press, halal directory and review sources completed identity, menu, hours, prices, ratings, ownership and adverse fields. Batch 708 was saved/indexed only after all 16 fields were present.
- **Corrections from the user:** The parent explicitly required completion rather than indexing the prior partial; no user factual correction occurred. The standing novelty-chain correction remains downstream and was not applied.
- **What required figuring out:** Official site has little process detail, but the Food Network recipe is explicitly attributed to the restaurant. Halal evidence names a visible sign/certificate but no certifier or supplier. Hours and rating snapshots conflict. Family ownership links Curry Fried Chicken and Curry in a Hurry without supporting transfer of production facts.
- **What could be encoded in the skill:** Search authoritative televised-recipe archives when operator sites omit process; type restaurant-supplied published recipes as operator-grade process evidence; require halal certifier/supplier names before elevating sourcing specificity; preserve split-shift hours; and prohibit process transfer across family-related concepts.

### Phase 4 fresh-fallback supplemental return — Laan Na Thai

- **Candidate:** R-0426 Laan Na Thai, 336 W 300 S, Salt Lake City.
- **What happened:** Completed the required operator/profile-first evidence sequence, preserved raw identity, hours, menu, daily-special, dish-level cooking, ratings, reviews and adverse evidence without rubric judgment, saved the return as `supplemental-R-0426-laan-na-thai.md`, and registered it as unique supplemental index row 700. Spice Kitchen Incubator and the archived Salt Lake Tribune supplied the strongest operator/history evidence; official Facebook was identified but its page text was not retrievable.
- **Corrections from the user:** None during this candidate pass. The standing correction remains to screen for low-novelty U.S. standardization rather than treating fast, casual, or multi-location formats as automatic exclusions; this evidence return made no such classification.
- **What required figuring out:** Restaurant Guru and Wanderlog linked `laannathai.top`, but operator control was not established, so it was not promoted to the official domain. Rating/review counts conflicted across platforms and were preserved literally. Customer “fresh to order” wording remained review evidence rather than operator production evidence. The assigned access date was retained as 2026-07-15 even though the fallback persistence occurred on 2026-07-16.
- **What could be encoded in the skill:** Require domain-ownership verification before promoting aggregator-linked sites; preserve a typed distinction between program/operator profiles and official restaurant domains; automatically retain platform rating conflicts; keep customer process observations separate from operator claims; and specify how assigned batch access dates relate to later persistence dates.
### Phase 5 repair wave 035 — customer process language and co-located sourcing

- **Candidates:** R-1267 Dough Miner, R-1268 Slackwater Pizzeria, R-1269 Logos Coffee Bar, R-1271 Jang Soo Jang.
- **What happened:** Re-ran the canonical five-stage source sequence, added durable customer/critic passages, adverse attribution, neutral boundaries, exact queries, and explicit exhausted-unavailable closure.
- **Corrections required from the user:** None during this wave.
- **What required interpretation:** Slackwater customer/employee-reported crust ingredients did not prove dough production; Logos co-located food and City Cakes products required external-supplier separation; Dough Miner frozen retail packs did not describe in-store holding; and Jang Soo Jang customer ownership wording did not establish a dated transition.
- **What could be encoded in the skill:** Separate employee-reported ingredient claims from operator process; add explicit co-location/external-supplier fields; prevent frozen retail formats from becoming service-format claims; require operator corroboration for ownership transitions; and require renewed exact passages before retaining terse adverse fragments.

### Phase 4 fresh-fallback supplemental return — Da Ming Express / Red Dragon Express

- **Candidate:** R-0442 Da Ming Express, discovered without an address at coordinate 40.710716, -112.095415.
- **What happened:** Resolved the coordinate to 8537 W 2700 S Ste A, Magna, completed the required source sequence, preserved raw identity/menu/hour/rating/review evidence without rubric judgment, saved the return as `supplemental-R-0442-da-ming-express.md`, and registered it as unique supplemental index row 702. Legacy merchant sources call the venue Da Ming Express or Da Ming; current Restaurantji calls the same-address, same-phone venue Red Dragon Express.
- **Corrections from the user:** None during this candidate pass. The standing correction remains to avoid treating restaurant format or multi-location status as an automatic exclusion; the evidence pass made no downstream classification.
- **What required figuring out:** The candidate lacked an address and required exact-coordinate reconciliation. The matching address and phone support continuity of the listing identity, but no operator statement supplied the name-change date or nature, so predecessor/successor details remain unresolved. Hours and rating counts conflict across current and legacy platforms. Yelp was robots-blocked, while Tripadvisor returned no matching venue record.
- **What could be encoded in the skill:** Require coordinate-first identity resolution for addressless candidates; trigger a same-address/same-phone rename audit; prohibit inferring a rebrand date or ownership continuity without operator/government evidence; partition legacy and current menu/rating snapshots; and record robots-blocked versus no-result platform outcomes separately.
### Phase 5 repair wave 036 — status conflict and delivery-causation boundaries

- **Candidates:** R-1272 Tang Huo Kung Fu, R-1275 Garage Grill, R-2070 Donut Star Cafe, R-1282 Don Daniel’s Mexican Grill & Cantina.
- **What happened:** Re-ran the five-stage source sequence, added durable venue-level review/adverse text, neutral scope, exact queries, and explicit exhausted-unavailable closures; withdrew unrenewed Reddit fragments.
- **Corrections required from the user:** None during this wave.
- **What required interpretation:** Tang Huo’s closure label conflicts with current operator/directory evidence; Garage Grill menu breadth is a literal format fact rather than a production inference; Donut Star sellout warnings do not describe process; and Don Daniel’s spilled-order review cannot assign causation between restaurant and courier.
- **What could be encoded in the skill:** Require explicit causation neutrality for delivery defects; separate aggregator closure labels from direct-source operating evidence; preserve breadth as descriptive menu evidence only; scope sellout/substitution language separately from production; and automatically withdraw chain/franchise claims that lack branch-specific documentation.

### Phase 4 fresh-fallback supplemental return — Toasters Deli 200 South

- **Candidate:** R-0450 Toaster's Cafe, resolved to official identity Toasters Deli — 200 South, 151 W 200 S, Salt Lake City.
- **What happened:** Completed the required source sequence, preserved raw identity/menu/hour/rating/review and multi-location evidence without rubric judgment, saved the return as `supplemental-R-0450-toasters-deli.md`, and registered it as unique supplemental index row 703. The official locations page reconciled the supplied `(888) 339-DELI` number with the branch-local `(801) 328-2928` number.
- **Corrections from the user:** None during this candidate pass. The standing correction remains to screen low-novelty standardization separately from fast/casual or multi-location format; this evidence pass recorded three active official locations without applying that heuristic.
- **What required figuring out:** The official page leaves its Sunday line blank while current directory platforms explicitly say Sunday closed. Historical/current menu prices conflict by source date. Exact `home-sliced` meat wording was retained at component scope, while generic fresh/local language was not expanded. A closure report concerned the separate 30 E 300 S branch and could not transfer to 151 W 200 S.
- **What could be encoded in the skill:** Reconcile shared vanity and branch-local phone numbers; represent blank official schedule fields separately from explicit third-party closure days; require location-level partitioning for multi-branch closure/review evidence; scope production verbs to named components; and attach effective-date uncertainty to menu-price snapshots.
### Phase 5 repair wave 037 — branch scope, sourcing nouns, and contaminant attribution

- **Candidates:** R-1811 Thai Better, R-1609 Protein Foundry, R-1298 Pizza Hut Delivery, R-1301 Janet’s Sunshine Cafe.
- **What happened:** Re-ran the five-stage source sequence, completed Thai Better ingredient/sourcing and cuisine/format, completed Janet’s cuisine/format, and added durable review/adverse passages, neutral boundaries, exact queries, and unavailable closures for all four.
- **Corrections required from the user:** None during this wave.
- **What required interpretation:** Ingredient nouns did not become sourcing evidence without a producer; multi-location status did not prove central production; Pizza Hut chain-level Reddit complaints could not become Kearns facts; and Janet’s hair/eggshell report remained a customer allegation rather than an inspection finding.
- **What could be encoded in the skill:** Distinguish ingredient lists from named sourcing; require branch-local gating for national chains; prohibit chain-level community complaints from branch adverse fields; add a contamination-allegation versus official-finding flag; and require cuisine/format completion independently of production evidence.
### Phase 5 repair wave 038 — generic production adjectives and adverse-field absence

- **Candidates:** R-1305 Beaumont Bakery & Cafe, R-1306 Dickey’s BBQ Pit, R-1307 Great India, R-1311 My Pie Pizza.
- **What happened:** Re-ran the five-stage sequence, added durable review text where required, adverse attribution, neutral scope, exact queries, and explicit unavailable closures. Great India’s adverse field was closed unavailable only after the full sequence.
- **Corrections required from the user:** None during this wave.
- **What required interpretation:** Beaumont’s house-made phrases required component-level scope; Dickey’s chain status did not establish branch production; Great India’s broad fresh/scratch/traditional language did not supply component methods; and My Pie’s family-recipe wording did not establish dough or sauce production.
- **What could be encoded in the skill:** Require named-component scoping for every house-made phrase; separate chain identity from branch process; permit an adverse field to close unavailable only with the exact sequence; flag generic production adjectives as quotations but not component proof; and preserve conflicting service summaries without choosing between them.

### Phase 4 fresh-fallback supplemental return — Franco’s Churro House Sugar House

- **Candidate:** R-0457 Franco’s Churro House, discovered without an address at coordinate 40.7222428, -111.8572636 and resolved to 2236 S 1300 E D5, Salt Lake City.
- **What happened:** Completed the required operator-first evidence sequence, preserved raw identity/menu/hour/rating/review/process and multi-location facts without rubric judgment, saved the return as `supplemental-R-0457-francos-churro-house.md`, and registered it as unique supplemental index row 705. Operator sources provide explicit handmade/fresh/made-to-order churro language, house-made pesto and freshly squeezed orange juice wording.
- **Corrections from the user:** None during this candidate pass. The standing correction remains to separate low-novelty standardization from fast-food or multi-location format itself; the evidence pass recorded the multi-location operation without applying the heuristic.
- **What required figuring out:** The addressless candidate needed coordinate resolution. Official phone and hours conflict across the home/contact/footer/Toast surfaces, and the official site simultaneously lists Saratoga Springs while one footer says `Coming Soon`. Customer process observations, an alleged automatic tip, delivery placement and translated “baking churros” wording required strict attribution rather than promotion to operator facts.
- **What could be encoded in the skill:** Require coordinate-first identity resolution for addressless candidates; detect contradictions within a single operator site across header/footer/contact/order surfaces; distinguish brand-wide production claims from branch-local evidence; preserve automatic-translation verbs literally with a translation flag; and type restaurant-versus-courier causation as unresolved for delivery defects.
### Phase 5 repair wave 039 — closed-branch conflicts and sensory-process allegations

- **Candidates:** R-1312 Roxberry Juice Co., R-1316 Fajita Grill ToGo, R-1317 Ginza, R-1320 Fortune Cuisine.
- **What happened:** Re-ran the five-stage sequence, preserved status conflicts, added durable customer/adverse passages where available, closed Roxberry review text unavailable after full search, and documented neutral scope, exact queries, and unavailable closures.
- **Corrections required from the user:** None during this wave.
- **What required interpretation:** Roxberry brand-wide specials could not become Holladay facts; Fajita Grill historical hours could not override closure labels; Ginza diner-controlled cooking did not establish component production; and Fortune customer reheated/smoky impressions were allegations rather than operator process evidence.
- **What could be encoded in the skill:** Require branch-participation evidence before applying company-wide promotions; distinguish historical hours from current status; separate diner-controlled final cooking from kitchen production; flag sensory process allegations as customer evidence; and allow review text to close unavailable only after a branch-specific query log.

### Phase 4 fresh-fallback supplemental return — Nuan’s Thai Kitchen

- **Candidate:** R-0684 Nuan’s Thai Kitchen, discovered at coordinate 40.6223847, -111.8234989 corresponding to the historical 2350 E Fort Union Blvd location.
- **What happened:** Completed the operator-first evidence sequence, preserved raw historical/current identity, menu, hours, ratings, reviews, process wording and relocation reporting without rubric judgment, saved the return as `supplemental-R-0684-nuans-thai-kitchen.md`, and registered it as unique supplemental index row 707. The same brand/domain currently operates at 1871 E Fort Union with a different phone.
- **Corrections from the user:** None during this candidate pass. The standing correction remains to apply low-novelty standardization independently of restaurant format; the evidence return made no heuristic or classification decision.
- **What required figuring out:** The coordinate pointed to the former address. A 2021 local report documented a planned closure and search for a new home, while the current operator site establishes the relocated venue; no operator move narrative/date was recovered. Current merchant wording labels homemade eggrolls, chicken satay and curry puffs, but other technique and ingredient descriptions required component-level scope. Several rating/distribution surfaces were internally malformed and had to be retained literally.
- **What could be encoded in the skill:** Trigger historical-address and relocation audits when coordinates disagree with current operator identity; model planned closure, actual closure and relocation as separate events; join continuity using brand/domain while preserving phone/address changes; validate rating-distribution arithmetic without silently correcting it; and scope merchant-set homemade/process language to named items.
### Phase 5 repair wave 040 — retail, prepared-meal, mall-kiosk, and closed-dessert scope

- **Candidates:** R-1321 1% Fitness Kitchen, R-1323 Rooster’s Gourmet Popcorn, R-1324 Hello Boba, R-1327 Louks Greek Baby Donuts.
- **What happened:** Re-ran the five-stage sequence, added durable review/adverse evidence, completed Louks cuisine/format, preserved location/status conflicts, and closed unavailable fields with exact queries.
- **Corrections required from the user:** None during this wave.
- **What required interpretation:** Microwave instructions did not prove freezing; popcorn hand-processing remained separate from current-location/ownership conflicts; customer fresh-made boba language did not become operator process; and Louks’ surviving menu did not prove an open storefront.
- **What could be encoded in the skill:** Separate reheating instructions from production/freezing; maintain a distinct retail-product process scope; treat surviving web menus as status-neutral; require same-branch review gating across states; and distinguish mall address reuse from confirmed same-suite tenancy.

### Phase 4 fresh-fallback supplemental return — Aubergine Kitchen Lehi

- **Candidate:** R-0848 Aubergine & Company, resolved to current official identity Aubergine Kitchen at 3430 Ashton Blvd Suite 100, Lehi.
- **What happened:** Completed the operator-first evidence sequence and saved raw identity, menu, hours, prices, ratings, reviews, process, sourcing and regional-chain facts as `batch-710-evidence_batch_001.md`, registered as unique supplemental index row 710. Operator evidence explicitly says the company makes from scratch every day, makes sauces in-house, bakes rather than fries and uses whole ingredients; the official order page lists at least 15 locations.
- **Corrections from the user:** The user clarified that fast food and chains must not be discarded as categories. The desired US-only heuristic is to skip **low-novelty chains**—places whose offering is highly standardized, broadly familiar and probably already tried—while preserving chains that perform interesting cooking in-house. No candidate-specific correction was required during retrieval.
- **What required figuring out:** The legacy candidate name differs from the current brand. Phones and Saturday hours conflict across direct merchant and directory sources. Company-wide scratch/in-house language does not establish which physical kitchen performs each task, and no commissary evidence was found. The brand is both regional fast-casual and explicitly scratch-oriented, making it a useful counterexample to chain/format exclusion.
- **What could be encoded in the skill:** Add a US-only low-novelty standardization screen after identity resolution, with no automatic penalty for fast-food, counter-service or multi-location status. Evaluate ubiquity/familiarity, menu standardization, evidence of branch or company scratch cooking, regional distinctiveness and likelihood the user has already tried the concept. Require an evidence note and reversible `deprioritize` disposition rather than deletion; disable or re-tune the heuristic outside the US. Preserve a separate uncertainty flag when company-wide production claims cannot be localized to the branch or commissary.

### Phase 5 repair wave 041 — review aggregation, service allegations, and cross-branch comparisons

- **Candidates:** R-1905 Hill's Kitchen, R-1859 Hearth and Hill, R-1331 Chop Shop, R-1532 Mochinut.
- **What happened:** Re-ran the five-stage sequence, supplied durable review/adverse text for all four, preserved customer-versus-editorial/operator attribution, and closed remaining fields with exact queries and exhausted-unavailable statements.
- **Corrections required from the user:** None during this wave. The standing correction remains to screen low-novelty U.S. standardization rather than treating fast food or multi-location status itself as undesirable; no classification was made here.
- **What required interpretation:** Hill's adverse material was exposed through an aggregator summary rather than underlying passages; Hearth and Hill had numerous discrete Yelp allegations that could not be treated as recurring defects; Chop Shop's strongest adverse evidence concerned owner/service conduct rather than food; and Mochinut's DoorDash comparison to Ogden could neither transfer evidence to Ogden nor assign delivery causation.
- **What could be encoded in the skill:** Type verbatim review passages separately from aggregator summaries; prevent multiple complaints in one review surface from becoming recurrence without independent-account counting; split food, service and official-adverse evidence; require explicit branch gating for comparisons; and mark restaurant-versus-courier causation unresolved for delivery texture defects.

### Phase 5 repair wave 042 — withdrawn fragments, successor partitioning, and renewed identity

- **Candidates:** R-1334 Toro Ramen, R-1335 So Grill Korean BBQ and Sushi, R-1336 Athena VII, R-1339 Kabul Kitchen.
- **What happened:** Re-ran the five-stage sequence, renewed durable review/adverse claims, supplied missing URL provenance, withdrew Toro fragments that could not be renewed, partitioned former So Grill from its reported successor, and replaced Kabul Kitchen's previously unavailable identity/menu/hour/rating fields with current URL-backed evidence while preserving conflicts.
- **Corrections required from the user:** None during this wave. The standing correction remains to distinguish low-novelty U.S. standardization from fast service or multi-location format; this evidence patch made no heuristic decision.
- **What required interpretation:** A restaurant response did not resolve Toro's customer complaint; stale So Grill hours conflicted with community closure/successor reports; Athena's daily-focaccia wording could not expand to all baking; Kabul's five current hour surfaces conflict, and delivery spoilage/texture allegations could not establish restaurant causation or official food-safety findings.
- **What could be encoded in the skill:** Require automatic withdrawal of unrenewed review fragments; model predecessor/successor evidence as separate identities; scope operator production adjectives to the exact named component; trigger identity-field renewal when formerly unavailable records surface; and require explicit medical/inspection corroboration flags for food-poisoning allegations.

### Phase 5 repair wave 043 — dietary-label allegations, map-entity isolation, and sellout scope

- **Candidates:** R-1714 Phở Saigon Noodle House 2, R-1341 Tuk Tuk’s of West Valley, R-1342 Ocean King Restaurant, R-1344 Donut Boy.
- **What happened:** Re-ran the five-stage sequence, renewed branch review/adverse text, supplied Ocean King's accepted URL provenance, recovered Pho Saigon phone/hours/rating and Donut Boy hours/rating, and explicitly withdrew Tuk Tuks' unrenewed long-wait fragment plus Ocean King's unrenewed market-closure fragment.
- **Corrections required from the user:** None during this wave. The standing correction remains to screen low-novelty U.S. standardization independently of fast service or multi-location status; no such classification occurred.
- **What required interpretation:** Pho Saigon vegan-label reports remained customer allegations without ingredient/operator corroboration; Tuk Tuks company-wide scratch language could not prove component details or identical branch execution; Ocean King's restaurant and supermarket map labels could not be merged; and Donut Boy sellout/customer handmade wording did not establish production methods or cadence.
- **What could be encoded in the skill:** Add dietary-label allegation and corroboration fields; distinguish company-wide production language from branch execution; require map-entity isolation before transferring adjacent-market evidence; model sellout separately from seasonality and production; and automatically reopen formerly unavailable identity/rating/hour fields when current direct records surface.

### Phase 5 repair wave 044 — hotel-venue boundaries and customer production inference

- **Candidates:** R-1345 Mar | Muntanya, R-1346 The Salt Republic, R-1347 Contribution Cocktail Lounge, R-1349 Lobby Lounge.
- **What happened:** Re-ran the five-stage sequence, added durable review/adverse passages, neutral claim boundaries and explicit closures while isolating each named hotel venue from adjacent restaurants, bars, markets, banquets and hotel-wide reviews.
- **Corrections required from the user:** None during this wave. The standing correction remains to evaluate low-novelty U.S. standardization independently of service format; no classification was made.
- **What required interpretation:** Mar customer “homemade” observations did not become operator process; a Salt Republic customer inferred industrial production from speed but supplied no production proof; unnamed Hyatt hotel food complaints could not transfer to Contribution; and historical/seasonal Lobby Lounge allegations could not establish current recurrence.
- **What could be encoded in the skill:** Require venue-level gating within hotels and food halls; distinguish customer production inference from sensory observation; attach currentness to adverse reviews; scope event-menu evidence separately from ordinary service; and treat hotel-wide reviews as unusable for a named outlet unless the outlet is explicit.

### Phase 5 repair wave 045 — generic map names, historical reviews, and branch gating

- **Candidates:** R-1355 The Spicy Corner, R-1356 Hot dog, R-1357 Edo Cafe, R-1358 Charleys Cheesesteaks Valley Fair.
- **What happened:** Re-ran the five-stage sequence, added durable review/adverse passages and closures, recovered the exact primary OSM object for `Hot dog`, preserved that object's unresolved real-world identity, and kept Charleys evidence gated to the Valley Fair address/phone/unit.
- **Corrections required from the user:** None during this wave. The standing correction remains to evaluate low-novelty U.S. standardization independently of fast service; no classification occurred.
- **What required interpretation:** Spicy Corner customer “made” language did not prove component production; an OSM node literally named `Hot dog` did not establish what it sells or whether it still operates; Edo's strongest detailed reviews were historical; and Charleys chain/operator claims required separation from branch customer reports and other franchise locations.
- **What could be encoded in the skill:** Require retrieval of primary OSM objects before declaring map provenance unavailable; flag generic map-object names as unresolved identities; attach review currentness; distinguish customer order assembly observations from component production; and require exact address/phone/unit gating for franchise review and adverse evidence.

### Phase 5 repair wave 046 — tenant separation, dated adverse evidence, and nightlife identity

- **Candidates:** R-1360 Han Bowls, R-1365 Sugar Space Play Cafe, R-1366 Tucanos Salt Lake City, R-1368 Eleven SLC.
- **What happened:** Re-ran the five-stage sequence, added durable review/adverse passages and closures, isolated Han Bowls from neighboring mall tenants, separated Sugar Space cafe/play/event scopes, dated Tucanos allegations, and supplied Eleven with municipal/map/concert URL provenance while preserving its Eleven/EVE/Club Verse branding conflict.
- **Corrections required from the user:** None during this wave. The standing correction remains to assess low-novelty U.S. standardization separately from format; no classification occurred.
- **What required interpretation:** Han Bowls sampling/order language did not prove component production; Sugar Space play-space criticism was not a food defect; Tucanos pandemic-era allegations could not establish current conditions; and Eleven's one-off catered fundraiser plus similarly named Venue One Eleven resource could not establish a resident kitchen.
- **What could be encoded in the skill:** Require suite-level mall tenant isolation; separate co-located cafe/play/event evidence; attach adverse-event dates and currentness; trigger municipal-license checks for nightlife entities; and reject one-off catering or similar-name venue evidence as proof of regular food operation.

### Phase 4 fresh-fallback supplemental return — Crimson View

- **Candidate:** R-0869 Crimson View, University of Utah A. Ray Olpin Student Union, Level 4, 200 Central Campus Drive.
- **What happened:** Resolved the coordinate to the university's active dine-in/seated-quick-serve restaurant and reservable event room, completed the required source sequence, preserved current/historical menu, hours, ratings, reviews, event-service and operating evidence without rubric judgment, saved the return as `supplemental-R-0869-crimson-view.md`, and registered it as unique supplemental index row 709.
- **Corrections from the user:** None during this candidate pass. The standing correction remains to evaluate low-novelty standardization independently from institutional, quick-service or multi-location format; this evidence return made no downstream classification.
- **What required figuring out:** University sources variously call Crimson View fine dining, full service, dine-in and seated quick serve, while current review material describes self-service. Historical menu wording includes house-made sauce, hand-breaded tenders, hand-cut fries and homemade beet ketchup, but current applicability is unknown. The University explicitly says Kahlert Village is the central commissary kitchen for most campus-dining items, yet does not enumerate which Crimson View items. Summer/2020 closure statements had to remain time-scoped because 2025–26 university sources call the venue active.
- **What could be encoded in the skill:** Model institutional venue format as multi-valued and time-versioned; require historical-menu effective-date warnings; record commissary scope separately at campus, venue and item levels; prohibit assigning non-enumerated items to a general commissary statement; and distinguish academic-calendar closures from permanent closure.

### Phase 4 fresh-fallback supplemental return — Tuk Tuk’s of Marmalade

- **Candidate:** R-1936 Tuk Tuk’s of Marmalade, 535 N 300 W Unit H103, Salt Lake City.
- **What happened:** Completed the operator-first source sequence, preserved branch identity, current menu/prices/hours, ratings, reviews, local editorial and multi-location facts without rubric judgment, saved the return as `supplemental-R-1936-tuk-tuks-marmalade.md`, and registered it as unique supplemental index row 711. The official menu explicitly labels homemade peanut sauce, homemade sweet Thai chili sauce and homemade Udon noodle soup.
- **Corrections from the user:** None during this candidate pass. The standing correction remains that multi-location or fast/casual format is not itself the target; this pass recorded four current official locations without applying the low-novelty heuristic.
- **What required figuring out:** Current official sources list four locations, while older Axios and current Time Out copy describe earlier three-location snapshots. Restaurant counts therefore required date scoping rather than choosing one. Critic descriptions of stir-frying, curry aromatics and vegetable texture remained editorial evidence, while homemade wording from the operator menu stayed component-specific. DoorDash delivery defects remained customer reports without process inference.
- **What could be encoded in the skill:** Version location counts by source date; separate operator production wording from critic technique observations; require component-level scope for homemade sauces/noodles; preserve delivery-texture allegations as customer evidence; and distinguish branch opening chronology from current chain size.

### Phase 5 repair wave 047 — rebrand continuity, ingredient allegations, and production boundaries

- **Candidates:** R-2465 Cilantree, R-1372 Everbowl, R-1373 Xing Fu Tang, R-1380 Urban Hill.
- **What happened:** Re-ran the exact five-stage sequence, added durable review/adverse passages and explicit closures, preserved Cilantree's same-address former-name history without making old reviews current, isolated Everbowl's Farmington evidence from non-Utah branches, withdrew Xing Fu Tang's unrenewed temperature fragment, and separated Urban Hill from sister-operation dessert production.
- **Corrections required from the user:** None during this wave. The standing correction remains to use a U.S.-only low-novelty standardization screen rather than treating fast food or chains as inherently unwanted; this repair made no classification or rubric decision.
- **What required interpretation:** Historical Saffron Valley allegations could transfer only as dated same-address identity evidence; Everbowl customer/aggregator guar-gum wording was not a verified ingredient list; Xing Fu Tang's global wok/torch practice and customer “made in house” language could not become exact-branch process facts; Urban Hill's credited Hill's Kitchen pastry production could not be relocated to the restaurant kitchen.
- **What could be encoded in the skill:** Model rebrands with address-level continuity and review-currentness gates; distinguish customer ingredient allegations from operator ingredient disclosures; require automatic withdrawal of unrenewed fragments; separate chain-wide demonstrations from branch execution; represent sister-company or tenant production as its own kitchen boundary; and require drive-time validation from the resolved address rather than a possibly mismatched discovery coordinate.

### Phase 5 repair wave 048 — map-only identity, renamed tenants, and closed-concept partitioning

- **Candidates:** R-1382 Yakuza Ramen, R-1384 Zapareco, R-1386 ACME Bar Co., R-1388 Emiliano's Taco Shop #1.
- **What happened:** Re-ran the exact five-stage sequence, supplied durable review/adverse passages and neutral boundaries for three records, gave Zapareco primary OSM and derivative-map URL provenance with explicit exhausted-unavailable closure, withdrew Yakuza's unrenewed Apple/Yelp fragments, partitioned ACME from predecessor/proposed successor concepts, and kept Emiliano's customer production wording from becoming operator fact.
- **Corrections required from the user:** None during this wave. The standing correction remains to evaluate U.S. low-novelty standardization rather than treating fast food, counter service or multiple locations as inherently unwanted; no classification occurred.
- **What required interpretation:** Yakuza's current Tosh's Ramen Express title may indicate a rename but does not prove a distinct kitchen; Zapareco survives only as a suite-level community-map object while the street address has other tenants; ACME's closure evidence does not establish the proposed Remora outcome; Emiliano's dish-soap report lacked corroboration and delivery packaging causation remained unresolved.
- **What could be encoded in the skill:** Require primary-map-object provenance for sparse discoveries; distinguish suite-level identity from street-address co-tenancy; model tenant renames separately from operator continuity; partition predecessor/current/proposed-successor concepts; automatically withdraw unrenewed fragments; prevent customer “homemade” wording from becoming operator process; and type delivery packaging causation as unresolved.

### Phase 5 repair wave 049 — relocation gating, hotel-event scope, and supplied-product boundaries

- **Candidates:** R-1389 Matteo Ristorante Italiano, R-1390 Adelaide Urban Brasserie, R-1391 Jollofology, R-1392 Renourish Kombucha Tap Room.
- **What happened:** Re-ran the exact five-stage sequence, renewed durable review/adverse passages or explicit review closure, resolved Matteo's current official address while isolating its former site, kept Adelaide holiday-event complaints scoped to those services, time-scoped Jollofology's 2023 Sunday reviews and stale 2024 menu copy, and added Renourish's September 2024 closure with taproom-versus-brewer production separation.
- **Corrections required from the user:** None during this wave. The standing correction remains to evaluate low-novelty U.S. standardization independently of fast/counter service or multiple locations; no rubric classification occurred.
- **What required interpretation:** Matteo reviews spanning a move could not automatically describe its new room/kitchen; Adelaide hotel and special-event evidence required named-outlet and service-date gating; Jollofology's shared kitchen did not establish component production; Renourish stocked and changed supplier kegs but did not thereby brew them.
- **What could be encoded in the skill:** Trigger relocation audits when official and directory addresses conflict; treat the former address's new tenant as decisive anti-merge evidence; attach holiday/event scope to adverse passages; flag stale future-dated operator copy; separate shared-kitchen tenancy from production; model taproom/retailer handling separately from supplier manufacturing; and reopen closure searches whenever current operation is unclear.

### Phase 5 repair wave 050 — sensory allegations, multi-branch isolation, and inaccessible review detail

- **Candidates:** R-1393 Urban Sailor Coffee, R-1402 Fortune Cookie, R-2269 La Frontera Midvale, R-1406 Mi Buena Vida.
- **What happened:** Re-ran the exact five-stage sequence, supplied durable review/adverse passages and neutral boundaries, preserved Urban Sailor's phone conflict, time-scoped Fortune Cookie's historical allegations, resolved La Frontera's phone while excluding other branches, and isolated Mi Buena Vida from its Express operation while retaining an inaccessible Tripadvisor title without inventing details.
- **Corrections required from the user:** None during this wave. The standing correction remains to assess U.S. low-novelty standardization rather than restaurant format itself; no rubric classification occurred.
- **What required interpretation:** Acidic coffee and dish-soap/fishy tastes remained sensory allegations; an oat-milk substitution allegation could be allergen-relevant without proving recurrence; La Frontera's vomiting report could not establish causation; an adverse review title without body text could be preserved only as opinion; aggregator/customer homemade-tortilla language could not become operator production.
- **What could be encoded in the skill:** Type allergen-relevant order substitutions separately from general service errors; require medical/inspection corroboration for illness causation; attach currentness to archived review platforms; permit title-only review evidence with a strict no-expansion rule; automatically isolate similarly named Express/branch entities; and distinguish operator item-specific handmade wording from aggregator or customer production claims.

### Phase 5 repair wave 051 — buffet temperature, dual-brand identity, and delivery causation

- **Candidates:** R-1407 Pizza Pie Cafe West Jordan, R-1408 Three Pines Coffee, R-1409 India Palace/Curry Pizza South Jordan, R-1411 Nami Lily Sushi & Ramen.
- **What happened:** Re-ran the exact five-stage sequence, renewed durable review/adverse passages and neutral boundaries, kept buffet replenishment distinct from menu rotation, time-scoped Three Pines' historical roaster evidence, preserved India Palace/Curry Pizza as an unresolved dual-name relationship, and retained Nami Lily's government address conflict plus unresolved delivery causation.
- **Corrections required from the user:** None during this wave. The standing correction remains to assess U.S. low-novelty standardization rather than treating buffet, counter service or multi-location format as inherently unwanted; no classification occurred.
- **What required interpretation:** Cold buffet pizza was a customer temperature allegation rather than recurrence; correctly prepared but unmemorable coffee was opinion rather than defect; missing-garam-masala language was a customer recipe inference; fresh-to-order pizza did not establish dough production; jumbled delivery packaging could not be assigned to restaurant or driver.
- **What could be encoded in the skill:** Separate buffet replenishment from rotation cadence; version supplier/roaster relationships; trigger dual-brand corporate-relationship audits for shared addresses; type customer ingredient-absence claims as recipe inference; require government-versus-commercial address conflict fields; and preserve delivery causation as unresolved when reviewers explicitly cannot assign it.

### Phase 5 repair wave 052 — brewery aliases, service-mode defects, and status conflicts

- **Candidates:** R-1412 Hunan Express Taylorsville, R-1413 Chappell Brewing, R-1417 Localz Bistro, R-1419 Shinobi Sushi Bar & Grill.
- **What happened:** Re-ran the exact five-stage sequence, renewed durable review/adverse passages and neutral boundaries, isolated Hunan from same-name restaurants, separated Chappell beer production from rotating food vendors while preserving Apex/Chappell identity conflict, scoped Localz defects to takeout where reported, and preserved Shinobi's map-closure/current-license conflict.
- **Corrections required from the user:** None during this wave. The standing correction remains to evaluate U.S. low-novelty standardization rather than restaurant or taproom format itself; no classification occurred.
- **What required interpretation:** Undercooked-dough and under-frying language remained customer allegations/inference; current DABS Apex naming could not silently supersede a live Chappell site; takeout defects could not transfer to dine-in; Shinobi's live official/current license/business-sale evidence outweighed but did not erase a closed map label; food-vendor evidence could not become brewery kitchen evidence.
- **What could be encoded in the skill:** Model legal-license, DBA and public brand as separate identity fields; require vendor/date attribution for food trucks; scope adverse evidence by service mode; treat ingredient/cook-time customer claims as inference; define conflict handling for stale map closure versus live government/operator evidence; and preserve business-for-sale status separately from closure.

### Phase 5 repair wave 053 — suite gating, event reservations, and provenance withdrawal

- **Candidates:** R-1420 Marmalade Brunch House, R-1421 Sunny Honey, R-1424 snowmoBAR/Snowmobile Pizza, R-1466 Sweet Churros.
- **What happened:** Re-ran the exact five-stage sequence, renewed durable review/adverse passages and neutral boundaries for the three suite-level venues, preserved event/date scope for snowmoBAR complaints, rebuilt Sweet Churros provenance from exact Grubhub/Loc8NearMe URLs and withdrew unrenewed Uber/Postmates/DoorDash fragments.
- **Corrections required from the user:** None during this wave. The standing correction remains to assess U.S. low-novelty standardization rather than service format; no rubric classification occurred.
- **What required interpretation:** House-made language remained component-specific; seasonal ingredients did not prove menu cadence; boba chew/ice reports were preference/texture evidence; an accepted holiday reservation while closed was event-operations evidence; a directory oil-change statement did not establish frying process or food-safety findings.
- **What could be encoded in the skill:** Require suite-level identity gating in mixed-use developments; distinguish seasonal ingredient labels from rotation cadence; type event-reservation failures separately; scope house-made claims to named components; require exact URL renewal for every accepted claim; and automatically withdraw platform fragments whose exact entity URL cannot be recovered.

### Phase 5 primary semantic review batch 016 — records 151–160

- **What happened:** The primary orchestrator directly inspected ten complete evidence sections spanning Sicilia Pizza, Alberto's, Tio's, Rawtopia, From Scratch, Yoshi's, Brew Monkey, Francisco's, Epic Brewing, and Amelia's. All ten were semantically complete as evidence: exact identity/scope, attribution, conflicts, the required search sequence, and explicit unavailable-field closure survived inspection. The cumulative primary review is now 160 records: 128 evidence-accepted and 32 evidence-exhausted-unavailable.
- **Corrections required from the user:** None. The user's standing correction still governs later classification: low novelty from standardized U.S. replication is the possible cheap exclusion signal, not chain status, fast service, or novelty by itself.
- **What required interpretation:** Crust comments did not prove dough production; customer menu similarity did not prove shared ownership; a sold-out special did not prove cadence; brewery production did not imply food production; and official generic “homemade” plus customer “frozen premade” language had to coexist without promoting either beyond its scope.
- **What could be encoded in the skill:** Add explicit semantic checks separating product reviews from production evidence, promotions/sellouts from recurring turnover, brewery/beverage process from kitchen process, customer chain-history statements from ownership facts, and generic operator scratch claims from component-level production claims.

### Phase 5 primary semantic review batch 017 — records 161–170

- **What happened:** The primary orchestrator directly inspected ten evidence sections spanning Melty through Atticus. Eight are semantically complete evidence returns; Fault Line Cafe and Bistro at Canyons are evidence-exhausted because current identity/continuity could not be established without transferring historical or successor facts. Cumulative direct review is 170 records: 136 accepted and 34 exhausted.
- **Corrections required from the user:** None. No scoring or low-novelty classification occurred.
- **What required interpretation:** Co-addressing did not prove virtual-brand ownership; downtown Este closure did not apply to Sugar House; parent Sawadee menu facts did not automatically belong to 2Go; resort seasonal closure was not permanent closure; and Prime reboot production evidence could not be assigned to the historical Bistro.
- **What could be encoded in the skill:** Add explicit gates for co-address virtual brands, branch-specific closure, subset-versus-parent menus, seasonal resort status, and successor/reboot identity continuity before any fact transfer.

### Phase 5 structural preflight correction after repair wave 048

- **What happened:** Three of four wave-048 records cleared immediately. Zapareco contained the required neutral evidence under the combined heading `Accepted URL provenance and neutral factual claims`, which the deterministic preflight did not recognize. The alias table was expanded and regeneration correctly cleared the record without changing its evidence.
- **Corrections required from the user:** None.
- **What required interpretation:** This was a heading-equivalence false negative, not a missing-evidence defect.
- **What could be encoded in the skill:** Either prescribe exact canonical field headings for repair artifacts or make the supplied validator recognize combined headings whose terminal canonical phrase is intact.

### Phase 5 primary semantic review batch 018 — records 171–180

- **What happened:** The primary orchestrator directly inspected ten records from Takashi through Liberty Park Grill. Seven are semantically accepted; Smart Cookie, Tsunami, and Liberty Park Grill are evidence-exhausted because branch selection or current operation could not be resolved. Cumulative direct review is 180 records: 143 accepted and 37 exhausted.
- **Corrections required from the user:** None. No scoring or low-novelty classification occurred.
- **What required interpretation:** User sourcing/sanitation claims stayed allegations; a closure review remained date-scoped against live hours; company coffee-release and roasting claims did not become branch food facts; and company scratch baking or multi-branch sushi evidence could not attach to addressless candidates.
- **What could be encoded in the skill:** Require a branch-selection gate before accepting company process, treat dated closure evidence as a conflict rather than a silent status overwrite, and make historical-menu currentness a required semantic field.

### Phase 5 primary semantic review batch 019 — records 181–190

- **What happened:** The primary orchestrator directly inspected ten records from four Hogle Zoo concessions through Simply Thai. All ten are semantically complete evidence returns; cumulative direct review is 190 records: 153 accepted and 37 exhausted.
- **Corrections required from the user:** None. No scoring or classification occurred.
- **What required interpretation:** Zoo-wide ratings could not attach to individual concessions; partner-creamery production stayed at the creamery; customer dough and wood-fire observations did not become operator process claims; and a customer-reported health-department complaint did not become an inspection finding.
- **What could be encoded in the skill:** Add explicit venue-within-attraction isolation, external-producer location fields, customer-process attribution checks, and complaint-versus-enforcement distinctions.

### Phase 5 primary semantic review batch 020 — records 191–200

- **What happened:** The primary orchestrator directly inspected ten records from Fuji Japanese Steakhouse through Urban Gyro. Nine are semantically accepted; historical Fuji is evidence-exhausted because Koi replaced it at the same address and current Fuji evidence cannot be renewed. Cumulative direct review is 200 records: 162 accepted and 38 exhausted.
- **Corrections required from the user:** None. No scoring or classification occurred.
- **What required interpretation:** Current successor ratings could not attach to Fuji; customer “home cooked” language did not prove process; company beer/sourcing claims did not become branch kitchen facts; and other-branch ratings stayed excluded even where the brand matched.
- **What could be encoded in the skill:** Add explicit successor replacement states, customer-production phrase typing, beverage-versus-food production separation, and automatic same-brand/different-branch rating rejection.

### Phase 5 primary semantic review batch 021 — records 201–210

- **What happened:** The primary orchestrator directly inspected ten records from Layla through Chile Verde. Four are semantically accepted; six historical, closed, bar-only, or identity-unresolved candidates are evidence-exhausted. Cumulative direct review is 210 records: 166 accepted and 44 exhausted.
- **Corrections required from the user:** None. No scoring or classification occurred.
- **What required interpretation:** Embedded concepts and successor occupants could not inherit facts; historical scratch evidence remained historical; a bar license was not kitchen evidence; dated inspection violations were not current; and a same-name menu site without address linkage could not attach to the candidate.
- **What could be encoded in the skill:** Add explicit embedded-concept lifecycle states, historical-process currentness flags, bar-versus-food-operation gates, inspection-age handling, and domain-to-address linkage requirements.

### Phase 5 primary semantic review batch 022 — records 211–220

- **What happened:** The primary orchestrator directly inspected ten records from Protagonist through Eva's Bakery. Nine are semantically accepted; Protagonist is evidence-exhausted because current operation and substantive food evidence could not be renewed. Cumulative direct review is 220 records: 175 accepted and 45 exhausted.
- **Corrections required from the user:** None. No scoring or classification occurred.
- **What required interpretation:** Historical production stayed time-scoped; website template instructions were rejected as menu content; order-platform unavailability did not establish closure; and area-sourced flour did not identify a mill.
- **What could be encoded in the skill:** Add webpage-template contamination detection, order-platform-versus-business-status typing, historical-process effective dates, and generic-origin-versus-named-supplier distinctions.

### Phase 5 primary semantic review batch 023 — records 221–230

- **What happened:** The primary orchestrator directly inspected ten records from The Spot through Ying's Thai-Sushi. Eight are semantically accepted; Salt Bistro and addressless Wallabys are evidence-exhausted. Cumulative direct review is 230 records: 183 accepted and 47 exhausted.
- **Corrections required from the user:** None. No scoring or classification occurred.
- **What required interpretation:** Generated dish terms were rejected; museum-ticket complaints were not food-price evidence; participating-location brand products were not assumed branch-local; commissary history did not establish present allocation; and company scratch claims did not attach to an unresolved branch.
- **What could be encoded in the skill:** Add generated-content rejection, host-venue lifecycle coupling, participating-location applicability checks, commissary allocation currentness, and mandatory branch resolution before company-process attachment.

### Phase 5 primary semantic review batch 024 — records 231–240

- **What happened:** The primary orchestrator directly inspected ten records from Rancherito's through a generic Valley Fair Mongolian Grill. Six are semantically accepted; four closed or current-identity-unresolved mall records are evidence-exhausted. Cumulative direct review is 240 records: 189 accepted and 51 exhausted.
- **Corrections required from the user:** None. No scoring or classification occurred.
- **What required interpretation:** Brand-transition facts did not renew a closed branch; guestbook halal wording was not certification; user-uploaded menus were not turnover; name words did not prove production; and generic cuisine-format practices were excluded.
- **What could be encoded in the skill:** Add closed-branch brand-transition rules, halal-claim provenance typing, user-uploaded-menu classification, name-only production rejection, and generic-format anti-transfer checks.

### Phase 5 primary semantic review batch 025 — records 241–250

- **What happened:** The primary orchestrator directly inspected ten records from Village Baker through El Rey Del Pollo. Nine are semantically accepted; Tornado Crepe is evidence-exhausted because the candidate node could not be linked to the separately documented business. Cumulative direct review is 250 records: 198 accepted and 52 exhausted.
- **Corrections required from the user:** None. No scoring or classification occurred.
- **What required interpretation:** Corporate packaging and bakery logistics stayed company-scoped; a job title did not prove production; externally supplied bread was not branch baking; reviewer “homey” language was not process; and a similar-name business was rejected without coordinate linkage.
- **What could be encoded in the skill:** Add corporate-versus-branch production scope, role-title non-evidence rules, supplied-versus-baked distinction, review-adjective process rejection, and coordinate linkage requirements for near-name businesses.

### Phase 5 primary semantic review batch 026 — records 251–260

- **What happened:** The primary orchestrator directly inspected ten records from Horn of Africa through Taqueria La Autentica. Eight are semantically accepted; former Freebirds and Togo's Utah records are evidence-exhausted. Cumulative direct review is 260 records: 206 accepted and 54 exhausted.
- **Corrections required from the user:** None. No scoring or classification occurred.
- **What required interpretation:** Platform summaries stayed separately scoped; paused ordering was not closure; current company content did not renew former branches; driver-attributed cold delivery was not a restaurant process defect; and similar-name handmade-tortilla evidence was rejected.
- **What could be encoded in the skill:** Add platform-summary provenance typing, ordering-pause status rules, former-branch renewal gates, delivery-causation fields, and same-name process anti-transfer checks.

### Phase 5 primary semantic review batch 027 — records 261–270

- **What happened:** The primary orchestrator directly inspected ten records from The Orange Peel through Royal India. Eight are semantically accepted; closed Orange Peel and possibly replaced Chow Time are evidence-exhausted. Cumulative direct review is 270 records: 214 accepted and 56 exhausted.
- **Corrections required from the user:** None. No scoring or classification occurred.
- **What required interpretation:** Active brand locations did not renew closed branches; corporate assembly language did not prove scratch production; historical-site prices stayed historical; successor identities were not merged; and a critic's scratch impression remained sensory opinion.
- **What could be encoded in the skill:** Add closed-brand branch isolation, corporate assembly claim typing, address-versioned price evidence, successor anti-merge gates, and sensory scratch-language classification.

### Phase 5 primary semantic review batch 028 — records 271–280

- **What happened:** The primary orchestrator directly inspected ten records from Split Leaf Coffee through Burger Express. Nine are semantically accepted; permanently closed My Thai is evidence-exhausted. Cumulative direct review is 280 records: 223 accepted and 57 exhausted.
- **Corrections required from the user:** None. No scoring or classification occurred.
- **What required interpretation:** User-uploaded menus were not turnover, customer cooking language stayed review evidence, cocktail process did not become food production, conflicting brioche sources remained unresolved, and neighboring park-concession facts were not transferred.
- **What could be encoded in the skill:** Add user-menu provenance, customer-process typing, beverage/food process separation, unresolved supplier conflicts, and attraction-concession neighbor isolation.

### Phase 5 primary semantic review batch 029 — records 281–290

- **What happened:** The primary orchestrator directly inspected ten records from Kobe through La Cevicheria. All ten are semantically complete evidence returns; cumulative direct review is 290 records: 233 accepted and 57 exhausted.
- **Corrections required from the user:** None. No scoring or classification occurred.
- **What required interpretation:** Aggregator sourcing stayed uncorroborated, general omakase seasonality did not become branch evidence, customer conveyor observations stayed customer evidence, separate same-name addresses were not merged, and a business-sale listing was not formal closure.
- **What could be encoded in the skill:** Add aggregator sourcing corroboration gates, generic-practice non-transfer, observation provenance, same-name address anti-merge, and sale-listing-versus-closure status typing.

### Phase 5 primary semantic review batch 030 — records 291–300

- **What happened:** The primary orchestrator directly inspected ten records from Taste of India through Vessel Kitchen. Seven are semantically accepted; closed Paradise Bakery and Junction plus identity-unresolved Shabu Shabu House are evidence-exhausted. Cumulative direct review is 300 records: 240 accepted and 60 exhausted.
- **Corrections required from the user:** None. No scoring or classification occurred.
- **What required interpretation:** Platform closure was separated from business closure, recurring lunch was not rotation, supplier facts did not prove branch fabrication, managed listing claims retained operator attribution, and company-wide scratch philosophy did not locate production at each branch.
- **What could be encoded in the skill:** Add platform-status scope, recurring-service versus turnover distinctions, supplier-versus-producer roles, managed-listing attribution, and company-claim production-site uncertainty.
### Phase 4/5 completeness audit — all confirmed scratch dessert in the east-side corridor

- **What happened:** Reconciled the worker index, every current Phase 4 dessert return, `05-scratch-dessert-eastside-classified.md`, `05-scratch-dessert-eastside-corridor.md`, the two corridor worker inventories, supplemental/repair returns, and alias/address matches. Wrote `05-scratch-dessert-millcreek-sugarhouse-avenues-all.md` with 16 confirmed producers: 11 dessert-forward businesses and five restaurants with meaningful scratch-dessert programs. Recorded weekday-specific after-8 status without treating an 8 PM closing as open after 8.
- **Corrections required from the user:** None during this extraction pass. The standing correction remains that fast food and multi-location status are not exclusions; only low-novelty standardization is a deprioritization signal. Sidecar and Thirst therefore remain included because their scratch processes are unusually explicit.
- **Corrections made by the audit:** Added R-0457 Franco's Churro House, whose completed indexed supplemental return postdated the earlier 15-place summary. Preserved the earlier corrections adding Banbury Cross, Greenhouse Effect and Thirst and resolving `Tulie's Cafe` to Tulie Bakery by candidate ID/address. Kept Hill's Kitchen and Hearth and Hill separate despite their shared address, and did not transfer Table X restaurant dinner hours to the bakery counter.
- **What required figuring out:** “All classified so far” required joining by candidate ID and address rather than exact display name; dessert-specific production had to be separated from broad scratch savory evidence; current hours had to distinguish after-8 service, an 8 PM boundary, and conditional Friday dessert availability; and geography needed an explicit core/edge/out-of-scope treatment. Nuan's, Tuk Tuk's Marmalade, and Crimson View were tested and excluded because their returns do not establish current scratch dessert production.
- **What could be encoded in the skill:** Require a completeness audit to union all indexed successful returns created after prior summaries; match entities by candidate ID + normalized address before name; maintain separate `dessert_forward` and `restaurant_dessert_program` types; require dessert-specific production evidence before promotion; represent hours as weekday intervals with `after_8`, `boundary_at_8`, and `conditional_menu_availability`; prevent co-located concepts and bakery/restaurant dayparts from sharing evidence automatically; and generate explicit borderline-geography and out-of-area appendices.

### Phase 5 repair wave 054 — accepted-URL provenance renewal

- **Candidates:** R-1518 Katsu City, R-1542 The Station Nutrition, R-1551 Jeeva's Greek Cafe at 1655 Campus Center Drive, and R-1552 Carolyn's Pantry.
- **What happened:** Audited every surviving field for an exact durable URL, source identity/type and 2026-07-16 access date. Katsu City renewed through municipal licenses, a lender's owner interview, H Mart, Restaurantji and DoorDash. The Station Nutrition narrowed to its dated city-license record. Jeeva's exact 1655 branch renewed through the city license and operator location page, while separately addressed downtown/1721 review evidence was removed. Carolyn's retained only the four literal fields on its exact LatLong POI page, explicitly directory-scoped.
- **Corrections required from the user:** None during this wave. No scoring, low-novelty classification, ranking or disqualification occurred.
- **What required interpretation:** A delivery platform's “temporarily closed” label could not establish business closure; 1387/1389 remained an address conflict even though two municipal records favor 1387; a company menu could establish concept-level offerings without proving branch-local production; and same-brand reviews at 28 S State or 1721 Campus Center could not attach to the 1655 candidate. A coordinate-directory field could survive only as an attributed map claim, not as proof of operation.
- **What could be encoded in the skill:** Require an accepted-URL column for every surviving field; prefer municipal address evidence without silently erasing candidate conflicts; model platform availability separately from business status; enforce address/phone branch gating before review transfer; distinguish company menu applicability from production-site proof; and provide a `directory_only_unverified` identity state for sparse coordinate POIs.

### Phase 5 repair wave 055 — accepted-URL provenance renewal

- **Candidates:** R-1565 Éclair French Cafe Daybreak, R-1568 Boba Tea Murray, R-1571 Premiere Bar and Lounge, and R-1572 Culture Coffee.
- **What happened:** Renewed every surviving field through exact durable pages and removed unsupported fragments. Éclair's exact branch now rests on South Jordan licensing while handmade/menu claims remain brand-scoped. Generic Boba Tea was address-gated to Apple Maps, Grubhub and Restaurantji, curing the missing-URL defect and withdrawing unrenewed Yelp/menu/process claims. Premiere retained operator menu, methods, address and event evidence while losing unrenewed platform aggregates and 21+ claims. Culture retained operator hours, KSL ownership/history and attributed Restaurantji/Corner claims.
- **Corrections required from the user:** None. No scoring, low-novelty classification, ranking or disqualification occurred.
- **What required interpretation:** Brand-level handmade language did not locate production at a newly licensed branch; a generic business name required exact unit/phone gating; a nightlife event's door time was not regular restaurant hours; and a guide's “house-made” or “locally made” wording remained guide provenance rather than operator confirmation or on-site baking proof.
- **What could be encoded in the skill:** Add mandatory branch-production-location fields for multi-shop bakeries; require generic-name candidates to have two exact identity keys before evidence attachment; distinguish event hours from recurring service hours; type guide-authored process statements separately from operator claims; and automatically withdraw any prior field lacking an accepted URL during provenance repair.

### Phase 5 repair wave 056 — accepted-URL provenance renewal

- **Candidates:** R-1573 House of Corn, R-2672 Level Crossing South Salt Lake, R-1579 Sri Annapoorani, and R-2035 Rio Acai Holladay.
- **What happened:** Renewed House of Corn's identity, nixtamalization and move/history through Axios plus exact-address directory/guide pages; renewed Level Crossing's exact branch, phone conflict, current menu/process and hours through operator, Toast and DABS pages; narrowed Sri Annapoorani to what its durable official menu endpoint actually exposes; and renewed Rio Acai's exact Holladay identity/menu/prices through Grubhub with directory-linked domain evidence. Every unrenewed rating, review, hours, supplier or process fragment was withdrawn.
- **Corrections required from the user:** None. No scoring, low-novelty classification, ranking or disqualification occurred.
- **What required interpretation:** Reproduced operator descriptions remained attributed rather than audited; a regional corn source did not become a named farm; brewery production did not automatically prove kitchen production; an official menu endpoint with sparse accessible text could renew identity without renewing the full earlier menu; and tapioca-flour bread wording did not locate dough mixing or baking.
- **What could be encoded in the skill:** Type reproduced business descriptions separately from direct operator pages; require named-producer granularity before supplier credit; isolate brewery and kitchen production fields; allow `official_endpoint_sparse` as a valid identity-only provenance state; distinguish ingredient composition from location of fabrication; and require explicit other-location isolation for multi-branch order pages.

### Phase 5 repair wave 057 — accepted-URL provenance renewal

- **Candidates:** R-1581 Crazy D's Hot Chicken South Jordan, R-1582 El Morelense South Jordan, R-1585 Bar à Vin, and R-1586 Nica Joe Espresso Bar.
- **What happened:** Grounded Crazy D's in municipal licensing plus exact-suite review/order pages while excluding Reno transfers; renewed El Morelense through its exact branch operator site and Restaurantji; renewed Bar à Vin through operator identity/hours/about/VIP pages plus an explicit Restaurantji Saturday conflict; and cured Nica Joe's missing-URL defect through exact LatLong, Mapcarta, OpenAlfa and SLUG pages while withdrawing all unsupported menu/process evidence.
- **Corrections required from the user:** None. No scoring, low-novelty classification, ranking or disqualification occurred.
- **What required interpretation:** A brand homepage centered on another state could not transfer company facts to Utah; item names did not prove trompo or tortilla production; a VIP promotion could renew limited food categories without becoming a full menu; OSM-derived partial hours remained directory claims; and cohabitation did not imply shared ownership, kitchen or food evidence. Nica Joe's 202/204 street-number conflict had to remain unresolved despite a precise coordinate.
- **What could be encoded in the skill:** Add out-of-state brand-page branch gates; reject cooking-method inference from dish names; type promotion-only menu evidence separately; represent partial third-party schedules without filling absent days; enforce co-tenant evidence isolation; and require address-number conflict preservation even when coordinates agree.

### Phase 5 repair wave 058 — accepted-URL provenance renewal

- **Candidates:** R-1588 Kimi's Chop & Oyster House, R-1589 The Peppered Vine, R-1591 Curry in a Hurry, and R-1593 Frostea.
- **What happened:** Renewed Kimi's current branch through OpenTable plus operator/menu pages; narrowed Peppered Vine to exact-address Restaurantji/Yahoo evidence after its claimed storefront could not be renewed; renewed Curry in a Hurry through its exact Uber branch while removing inaccessible operator/history assertions; and cured Frostea's missing-URL defect through exact Restaurantji, DoorDash and LatLong pages while adding a same-address Tea & Brown municipal conflict.
- **Corrections required from the user:** None. No scoring, low-novelty classification, ranking or disqualification occurred.
- **What required interpretation:** A catering phone was not necessarily a restaurant-phone conflict; a menu mirror stayed aggregator provenance; directory house-made wording was not an operator admission; a delivery menu could renew branch facts without proving brand history; and same-address Tea & Brown evidence could indicate rename, replacement or co-location but could not be silently attached to Frostea.
- **What could be encoded in the skill:** Add phone-purpose fields; distinguish operator menus from exact-venue mirrors; preserve author type for directory process summaries; separate order-platform branch evidence from company history; and automatically trigger predecessor/rename/co-location review when a municipal opening record and current exact-suite identity differ.

### Phase 5 repair wave 059 — accepted-URL provenance renewal

- **Candidates:** R-1594 SpudToddos, R-1595 Brown Bag Breakfast Co., R-2330 Los Tapatios Taco Grill West Valley, and R-1600 Coco's Neveria y Taqueria.
- **What happened:** Renewed SpudToddos through exact Restaurantji/Grubhub/order pages while withdrawing unrenewed process/review details; cured Brown Bag's missing-URL defect through exact directories, founder public post and Eventeny while exposing a phone conflict; renewed Los Tapatios through municipal licensing, exact Toast and Grubhub pages with branch isolation; and cured Coco's missing-URL defect through municipal licenses/directory plus exact Restaurantji/Waze pages.
- **Corrections required from the user:** None. No scoring, low-novelty classification, ranking or disqualification occurred.
- **What required interpretation:** An unavailable order menu did not establish closure; founder claims remained self-description; event participation did not prove storefront operation; historical license phones stayed date-scoped against current ordering phones; and municipal license/address evidence could establish identity without proving food production. Coco's 84084/84088 and hours differences remained unresolved source conflicts.
- **What could be encoded in the skill:** Distinguish platform-menu availability from business status; type founder-authored operational/sourcing claims; separate event-vendor and storefront states; add effective dates to phone evidence; let municipal identity evidence coexist with field-level production gaps; and preserve ZIP/locality variants rather than treating them as automatic identity failures.

### Phase 5 repair wave 060 — accepted-URL provenance renewal

- **Candidates:** R-1601 SLC Dhaba, R-1602 New Dragon Diner, R-1607 Keyaki Sushi, and R-1734 Dave's Hot Chicken Sugar House.
- **What happened:** Renewed SLC Dhaba's exact branch/contact/menu/process through operator and Toast pages; renewed New Dragon through operator, city directory and exact Restaurantji while preserving ZIP variation; narrowed Keyaki to identity/order presence because earlier detailed claims could not be renewed to accessible exact text; and renewed Dave's branch hours, halal chicken, heat levels and core formats through Salt Lake-specific operator pages while withdrawing corporate transfers.
- **Corrections required from the user:** None. No scoring, low-novelty classification, ranking or disqualification occurred.
- **What required interpretation:** Restaurant/catering phones were purpose-specific, not conflicts; monthly-menu headings did not establish a historical cadence; an active order endpoint could renew identity without exposing menu facts; ZIP variation did not force entity separation; and corporate menu/process evidence could not attach to a branch unless the branch page repeated it.
- **What could be encoded in the skill:** Add phone-purpose roles; require multiple dated snapshots before turnover claims; support identity-only renewal from sparse operator order endpoints; preserve postal variants; and enforce branch-page repetition before company-wide production or sourcing claims become branch evidence.

### Phase 5 repair wave 061 — canonical completion and provenance repair

- **Candidates:** R-1614 East-West Connection, R-1615 caffe d'bolla, R-1618 4111 Nutrition, and R-1619 Phở Biên Hòa Taylorsville.
- **What happened:** Added canonical field groupings, exact five-stage trails and explicit unavailable-field closure ledgers for all four. East-West now preserves a live-license/permanently-closed conflict; caffe d'bolla renews direct operator roasting/siphon evidence while shedding unrenewed price/review claims; 4111 Nutrition's missing-URL defect is cured with exact directory URLs and all unsupported product/phone claims withdrawn; Biên Hòa renews current operator menu/prices while preserving municipality/ZIP and hours conflicts.
- **Corrections required from the user:** None. No scoring, low-novelty classification, ranking or disqualification occurred.
- **What required interpretation:** A current liquor license did not conclusively prove operation; farm-specific sourcing did not name current farms; a business name did not establish nutrition-club products; and an operator footer's locality/ZIP could conflict with exact-address directories without creating a second restaurant.
- **What could be encoded in the skill:** Require explicit status-conflict objects, current named-farm fields separate from general sourcing method, reject menu inference from business names, preserve municipality/ZIP conflicts at identical address/phone, and prescribe an extractor-compatible canonical closure heading.
- **Post-phase semantic correction:** The generated audit revealed that `Unavailable fields / closure ledger` is accepted by the general field-label aliases but not by the audit's dedicated closure extractor, which requires `Unavailable fields:` (or one of its narrower enumerated alternatives). I normalized all four repair headings to `Unavailable fields:`. This exact heading should be encoded in the skill, or the audit regex and alias vocabulary should be made identical so a semantically valid label cannot pass one check and fail another.

### Phase 5 primary semantic review batch 031 — records 301–310

- **What happened:** The primary orchestrator directly inspected ten records from Park City Bread and Bagel through Corner Store Pub & Grill. Nine are semantically accepted; foodless nightclub Downstairs is evidence-exhausted. Cumulative direct review is 310 records: 249 accepted and 61 exhausted.
- **Corrections required from the user:** None. No scoring or classification occurred.
- **What required interpretation:** Customer freshness stayed customer evidence; generic local sourcing did not identify suppliers; a closed-arrival report and seasonal closure did not establish permanent closure; seasonal hours and rotating entertainment were not menu turnover; co-located concepts did not share production evidence; and the historical Handle Salt Lake name was versioned to HSL without merging Park City Handle.
- **What could be encoded in the skill:** Add customer-versus-operator freshness typing, generic-versus-named sourcing, closure-state taxonomy, operating-season-versus-menu-season distinctions, entertainment/food rotation separation, co-located-concept production isolation, and historical-name entity versioning.

### Phase 5 primary semantic review batch 032 — records 311–320

- **What happened:** The primary orchestrator directly inspected ten records from Legacy Café through Oh Mai. Nine are semantically accepted; closed downtown Padeli's is evidence-exhausted. Cumulative direct review is 320 records: 258 accepted and 62 exhausted.
- **Corrections required from the user:** None. No scoring or classification occurred.
- **What required interpretation:** Resort seasonal closure stayed distinct from permanent closure; wholesale frozen empanadas were not assigned to retail workflow; a named dish ingredient was not broader sourcing proof; predecessor evidence was isolated at SLC Pub; customer sourdough/nightly-recommendation language stayed customer evidence; a summer promotion was not general cadence; and a family baguette recipe did not prove on-site baking.
- **What could be encoded in the skill:** Add closure-state typing, channel-specific production workflows, dish-title sourcing limits, same-address predecessor isolation, customer-process typing, promotion-versus-cadence rules, and recipe-versus-production-location distinctions.

### Phase 5 primary semantic review batch 033 — records 321–330

- **What happened:** The primary orchestrator directly inspected ten records from The Glowbal Bite through The Wildflower. Six are semantically accepted; sparse Glowbal Bite, identity-transitioned Stephen's, retired-page Atrium, and current-status-unresolved Wildflower are evidence-exhausted. Cumulative direct review is 330 records: 264 accepted and 66 exhausted.
- **Corrections required from the user:** None. No scoring or classification occurred.
- **What required interpretation:** Hotel evidence was not transferred to outlets; hotel-centric reviews were separated; fresh-baked product naming did not prove branch production policy; a successor concept did not renew its predecessor; dated menu prices stayed dated; customer frozen-food claims stayed attributed; and resort seasonal status did not prove outlet closure.
- **What could be encoded in the skill:** Add hotel/outlet evidence isolation, review-pool contamination checks, product-name versus production-policy typing, successor/predecessor status rules, price-version dates, customer-process attribution, and resort-versus-outlet closure separation.

### Phase 5 primary semantic review batch 034 — records 331–340

- **What happened:** The primary orchestrator directly inspected ten records from Baked & Brewed through La Fountain. Eight are semantically accepted; current-status-unresolved Baked & Brewed and food-menu-silent Patrick's Pub are evidence-exhausted. Cumulative direct review is 340 records: 272 accepted and 68 exhausted.
- **Corrections required from the user:** None. No scoring or classification occurred.
- **What required interpretation:** Reported menu change was not cadence; curated testimonials stayed operator-selected; sister-concept food was not transferred; generic local sourcing stayed generic; chain status was not exclusion; bar amenities were not food evidence; shared kitchens did not establish component provenance; and promotional freshness was not process evidence.
- **What could be encoded in the skill:** Add reported-change versus recurring-cadence typing, curated-review provenance, sister-concept isolation, generic sourcing limits, chain non-exclusion, foodless-bar gates, shared-kitchen provenance uncertainty, and promotional-freshness claim typing.

### Phase 5 primary semantic review batch 035 — records 341–350

- **What happened:** The primary orchestrator directly inspected ten records from Salt Lake Coffee Break through Sicilia Mia. Nine are semantically accepted; closed downtown Cafe Trang is evidence-exhausted. Cumulative direct review is 350 records: 281 accepted and 69 exhausted.
- **Corrections required from the user:** None. No scoring or classification occurred.
- **What required interpretation:** Menu availability did not prove production; customer homemade wording stayed customer evidence; campus-outlet premade evidence was not transferred downtown; linked neighboring food service stayed explicitly scoped; local pasta was not house pasta; branded vegan product stayed external; stored-menu age remained visible; bakery and dinner hours were isolated; and sell-out hours were not production proof.
- **What could be encoded in the skill:** Add menu-versus-production separation, customer-process provenance, cross-outlet anti-transfer, linked-concept scope, local-supplier versus house-production typing, branded-component roles, menu-version dates, co-located daypart isolation, and sellout-versus-process distinctions.

### Phase 5 primary semantic review batch 036 — records 351–360

- **What happened:** The primary orchestrator directly inspected ten records from Sala Thai Kitchen through The Huddle. Nine are semantically accepted; the closed/replaced Midvale 1000 Degrees branch is evidence-exhausted. Cumulative direct review is 360 records: 290 accepted and 70 exhausted.
- **Corrections required from the user:** None. No scoring or classification occurred.
- **What required interpretation:** Generic sourcing did not identify farms; current chain claims did not renew a closed branch; tableside cooking did not prove scratch components; chain scale was not exclusion; slow-simmered broth did not prove noodles; customer noodle-production wording stayed attributed; directory baking wording stayed directory evidence; and drink deals were not food turnover.
- **What could be encoded in the skill:** Add promotional-sourcing granularity, closed-branch corporate non-transfer, visible-cooking limits, chain non-exclusion, component-specific process boundaries, customer/directory provenance classes, and beverage-versus-food cadence separation.

### Phase 5 primary semantic review batch 037 — records 361–370

- **What happened:** The primary orchestrator directly inspected ten records from Sushi Yah through Laziz Kitchen. Six are semantically accepted; historical J&J Sapor and Coronado Subs, ledger-only You're The Boss, and current-status-unresolved Thai Land are evidence-exhausted. Cumulative direct review is 370 records: 296 accepted and 74 exhausted.
- **Corrections required from the user:** None. No scoring or classification occurred.
- **What required interpretation:** Current tenants were not inferred as successors; persistent map points did not prove operation; historical sourcing stayed dated; attached-restaurant menu access required operator evidence; general seasonality was not cadence; a current DABS tenant was not merged; unofficial sourcing stayed unpromoted; and restaurant versus wholesale production channels remained explicit.
- **What could be encoded in the skill:** Add tenant/successor anti-inference, map-status limits, historical-source dating, attached-concept menu gates, seasonality-versus-cadence typing, current-tenant anti-merge, unofficial-source promotion limits, and production-channel separation.

### Phase 5 primary semantic review batch 038 — records 371–380

- **What happened:** The primary orchestrator directly inspected ten records from Penny Ann's through Tinker's Cat Cafe. Nine are semantically accepted; temporarily closed Asian Potato is evidence-exhausted. Cumulative direct review is 380 records: 305 accepted and 75 exhausted.
- **Corrections required from the user:** None. No scoring or classification occurred.
- **What required interpretation:** Signature batter did not generalize to other components; reopening was not menu rotation; market co-location did not prove sourcing; group-site evidence required branch scope; dynamic hours stayed conflicting; broad menu grammar was not process; promotional freshness stayed literal; temporary closure was not made permanent; themed menus were not process; and cat lounge/cafe evidence remained separated.
- **What could be encoded in the skill:** Add component-claim containment, reopening-versus-turnover typing, market/restaurant sourcing isolation, group-site branch scoping, dynamic-hour conflict handling, menu-grammar limits, promotional-claim typing, temporary-closure state, theme-versus-process distinction, and multi-space venue separation.

### Phase 5 primary semantic review batch 039 — records 381–390

- **What happened:** The primary orchestrator directly inspected ten records from The Dumplings Company through La Puente. Nine are semantically accepted; the closed Millcreek MunchKart branch is evidence-exhausted. Cumulative direct review is 390 records: 314 accepted and 76 exhausted.
- **Corrections required from the user:** None. No scoring or classification occurred.
- **What required interpretation:** Generic local wording stayed generic; archived process stayed dated; chain status was not exclusion; corporate location pages did not override exact-branch closure; company production claims retained site uncertainty; buffet availability was not rotation; technique labels did not prove scratch components; ordering-channel closure was not venue closure; and customer homemade wording stayed customer evidence.
- **What could be encoded in the skill:** Add generic sourcing limits, process-version dating, chain non-exclusion, exact-branch closure precedence, production-site uncertainty, buffet-versus-turnover distinction, technique-label limits, channel-status scoping, and customer-process provenance.

### Phase 5 primary semantic review batch 040 — records 391–400

- **What happened:** The primary orchestrator directly inspected ten records from Picnic Cafe through Ramblin Roads. All ten are semantically complete evidence returns. Cumulative direct review is 400 records: 324 accepted and 76 exhausted.
- **Corrections required from the user:** None. No scoring or classification occurred.
- **What required interpretation:** Pop-up/wholesale channels stayed distinct; legacy/current names remained versioned; corporate menus did not locate branch production; review-derived process stayed review evidence; other branches/allegations were not transferred; historical process remained dated; promotions were not cadence; take-and-bake process was not generalized; archived operator wording stayed dated; and customer freshness was not operator proof.
- **What could be encoded in the skill:** Add channel separation, entity-name versioning, corporate production-site uncertainty, review-process provenance, branch allegation isolation, historical-evidence dating, promotion-versus-cadence typing, process-scope containment, archive dating, and customer-versus-operator freshness rules.

### Phase 5 primary semantic review batch 041 — records 401–410

- **What happened:** The primary orchestrator directly inspected ten records from Plates & Palates through Christopher's. Seven are semantically accepted; foodless Water Witch, closed Bumblebee's West Valley, and external-food-truck Fisher are evidence-exhausted. Cumulative direct review is 410 records: 331 accepted and 79 exhausted.
- **Corrections required from the user:** None. No scoring or classification occurred.
- **What required interpretation:** Broad in-house claims did not attach to unmentioned components; adjacent kitchens were not transferred; AYCE windows were not rotation; platform synthesis remained non-operator; vendor ambiguity stayed unresolved; customization was not component production; beverage production was not food production; and a supplied unrelated URL was rejected.
- **What could be encoded in the skill:** Add broad-claim containment, adjacent-kitchen isolation, service-window versus turnover typing, platform-synthesis provenance, vendor ambiguity fields, customization/process separation, beverage/food production separation, and supplied-URL identity validation.

### Phase 5 primary semantic review batch 042 — records 411–420

- **What happened:** The primary orchestrator directly inspected ten records from Little Thai Kitchen through Mana Thai. Nine are semantically accepted; closed Taqueria Martini is evidence-exhausted. Cumulative direct review is 420 records: 340 accepted and 80 exhausted.
- **Corrections required from the user:** None. No scoring or classification occurred.
- **What required interpretation:** Same-name restaurants and historical NYPD claims were excluded; seasonal-sounding item names were not turnover; claims stayed dish/branch scoped; buffet service was not rotation; technique labels stayed item-specific; hotel/neighbor evidence was isolated; customer-reported server claims stayed attributed; and fresh-noodle/homemade-sauce claims remained component-specific.
- **What could be encoded in the skill:** Add namesake exclusion, predecessor-brand isolation, item-name versus cadence typing, dish/branch scope enforcement, buffet-versus-turnover rules, technique containment, neighbor/hotel isolation, second-hand process provenance, and component-specific production typing.

### Phase 5 primary semantic review batch 043 — records 421–430

- **What happened:** The primary orchestrator directly inspected ten records from Casot through The Pie Pizzeria. All ten are semantically complete evidence returns. Cumulative direct review is 430 records: 350 accepted and 80 exhausted.
- **Corrections required from the user:** None. No scoring or classification occurred.
- **What required interpretation:** Group scratch language was not transferred; adjacent-listing complaints were excluded; cuisine breadth stayed factual; customer process stayed attributed; branch/brand evidence stayed separated; other Oh Mai branches were not transferred; company evidence retained branch uncertainty; holiday opening was not turnover; planned relocation was not completion; and shared-company process remained first-party/shared-menu scoped.
- **What could be encoded in the skill:** Add group-claim non-transfer, adjacent-listing review isolation, format-versus-process typing, customer-process provenance, branch/brand separation, cross-branch anti-transfer, corporate branch uncertainty, holiday-versus-turnover distinction, relocation-state typing, and shared-menu process scope.

### Phase 5 primary semantic review batch 044 — records 431–440

- **What happened:** The primary orchestrator directly inspected ten records from Old Bridge Cafe through Lonestar Saloon. Seven are semantically accepted; closed Akasaka, displaced/omitted Sodalicious Midvale, and closed SLABpizza Lehi are evidence-exhausted. Cumulative direct review is 440 records: 357 accepted and 83 exhausted.
- **Corrections required from the user:** None. No scoring or classification occurred.
- **What required interpretation:** Attached retail did not prove restaurant sourcing; a fraudulent site was rejected; shop and roaster evidence stayed scoped; booking placeholders and historical licenses did not establish reopening; central bakery evidence did not prove branch baking; menu technique labels did not prove component production; group evidence did not fill branch fields; brewery evidence did not become food evidence; and a merged namesake description was excluded.
- **What could be encoded in the skill:** Add attached-retail boundaries, hostile/fraudulent-domain rejection, related-business scope typing, reopening-evidence thresholds, central-versus-branch production, cooking-label containment, group-to-branch field isolation, beverage-versus-food evidence separation, and merged-listing detection.

### Phase 5 primary semantic review batch 045 — records 441–450

- **What happened:** The primary orchestrator directly inspected ten records from Gaetano's through Matcha Cafe Kyoto. Nine are semantically accepted; Side of Aloha is evidence-exhausted because closure signals were not overcome by a live exact-entity source. Cumulative direct review is 450 records: 366 accepted and 84 exhausted.
- **Corrections required from the user:** None. No scoring or classification occurred.
- **What required interpretation:** A sale was not closure; a static menu did not prove current operation; seasonal fruit was not menu rotation; buffet variation stayed distinct from ingredient seasonality; drink assembly did not imply scratch inputs; roastery and cafe-food production stayed separate; customer patty reports stayed attributed; renamed concepts were versioned; event recurrence was not food turnover; and daily production was not menu rotation.
- **What could be encoded in the skill:** Add sale-versus-closure typing, static-page liveness limits, seasonal-garnish cadence limits, buffet/ingredient-seasonality separation, assembly-versus-fabrication typing, roastery/cafe process separation, customer-production provenance, concept-version rules, event-versus-food cadence, and production-frequency versus menu-turnover typing.

### Phase 5 primary semantic review batch 046 — records 451–460

- **What happened:** The primary orchestrator directly inspected ten records from Alchemy Coffee through H Bar. Eight are semantically accepted; closed Yoko Ramen and foodless/outside-food Dick N' Dixie's are evidence-exhausted. Cumulative direct review is 460 records: 374 accepted and 86 exhausted.
- **Corrections required from the user:** None. No scoring or classification occurred.
- **What required interpretation:** Gallery rotation and holiday buffets were not recurring food cadence; address variants were not branches; format breadth did not imply production breadth; cafe naming did not prove baking; broad menus did not broaden scratch claims; drink turnover did not become food turnover; live residue pages did not override reported closure; adjacent/carried food was not transferred; and hotel outlets/ratings plus wrong branches were isolated.
- **What could be encoded in the skill:** Add non-food-cadence exclusion, one-off-event typing, address-variant reconciliation, format/process separation, venue-name non-proof, scratch-scope containment, beverage/food cadence separation, stale-live-page handling, outside-food isolation, and hotel-outlet/branch scoping.

### Phase 5 primary semantic review batch 047 — records 461–470

- **What happened:** The primary orchestrator directly inspected ten records from Just Organic Juice through Annex Burger. Nine are semantically accepted; Aroma Fine Indian Cuisine is evidence-exhausted because closure evidence was not overcome by independently renewed live operation. Cumulative direct review is 470 records: 383 accepted and 87 exhausted.
- **Corrections required from the user:** None. No scoring or classification occurred.
- **What required interpretation:** Customer organic allegations stayed attributed; central bakery allocation stayed uncertain; ordering residue did not prove liveness; daypart breadth was not turnover; commercial assembly was not scratch fabrication; exact-location scope was retained; group process did not prove branch liveness; early-closing reports were not permanent closure; customer homemade wording stayed attributed; and sister-venue/historical claims were not transferred as current.
- **What could be encoded in the skill:** Add allegation-verification typing, centralized-production allocation, ordering-page liveness limits, daypart-versus-cadence rules, commercial-input assembly typing, exact-location enforcement, group-process/liveness separation, early-closing versus closure distinction, customer-process provenance, and sister-venue/currentness isolation.

### Phase 5 primary semantic review batch 048 — records 471–480

- **What happened:** The primary orchestrator directly inspected ten records from Hopkins Brewing through Donut House. Nine are semantically accepted; Mikado Cottonwood is evidence-exhausted after its documented 2012 closure and replacement. Cumulative direct review is 480 records: 392 accepted and 88 exhausted.
- **Corrections required from the user:** None. No scoring or classification occurred.
- **What required interpretation:** Beer rotation was not food turnover; replacement evidence was not transferred; broad sourcing stayed broad; closure and reopening were separate events; allegations/rebuttals stayed attributed; chain status was not automatic exclusion; customer sourcing stayed customer evidence; historical process stayed dated; venue naming did not prove production; and fresh-serving wording did not locate fabrication.
- **What could be encoded in the skill:** Add beverage/food turnover separation, replacement-entity isolation, broad-sourcing containment, status-event timelines, allegation/rebuttal pairing, chain non-exclusion, customer-sourcing provenance, historical-process dating, venue-name non-proof, and service-freshness versus fabrication rules.

### Phase 5 primary semantic review batch 049 — records 481–490

- **What happened:** The primary orchestrator directly inspected ten records from Apple Spice through Kung Fu Tea. Eight are semantically accepted; permanently closed Apple Spice Wells Fargo and Kung Fu Tea 600 East are evidence-exhausted. Cumulative direct review is 490 records: 400 accepted and 90 exhausted.
- **Corrections required from the user:** None. No scoring or classification occurred.
- **What required interpretation:** Current sibling menus were not transferred; other-branch menu additions stayed isolated; technique labels did not prove deeper production; shopping-center/menu-host sources retained type; relocations stayed versioned; shared-kitchen work was not inferred; cider evidence was not generalized to food; recommendation premises were not facts; public-listing freshness was not operator proof; and brand process was not current closed-branch evidence.
- **What could be encoded in the skill:** Add sibling-location anti-transfer, branch-menu isolation, technique-depth limits, source-role typing, move/version tracking, shared-kitchen labor uncertainty, beverage-to-food non-transfer, discussion-premise rejection, listing-versus-operator provenance, and closed-branch brand-process limits.

### Phase 5 primary semantic review batch 050 — records 491–500

- **What happened:** The primary orchestrator directly inspected ten records from Prohibition through Shane's Donuts. Nine are semantically accepted; Chedda Burger Gateway is evidence-exhausted after the documented 2023 closure of all locations. Cumulative direct review is 500 records: 409 accepted and 91 exhausted.
- **Corrections required from the user:** None. No scoring or classification occurred.
- **What required interpretation:** Menu breadth was not shallow-production proof; customer cooking stayed attributed; bar licensing did not negate food; cuisine breadth did not widen production claims; mall identity did not license invented operator evidence; historical process and removed items stayed dated; nightclub activity was not food cadence; other-location evidence was not transferred; chain status was not automatic exclusion; and mom-and-pop/shop labels did not prove scratch work.
- **What could be encoded in the skill:** Add breadth/process separation, customer-cooking provenance, license-versus-food coexistence, cuisine/process containment, mall-directory source limits, removed-item/currentness typing, entertainment/food-cadence separation, cross-location review isolation, chain non-exclusion, and ownership/venue-name non-proof.

### Phase 5 primary semantic review batch 051 — records 501–510

- **What happened:** The primary orchestrator directly inspected ten records from East Coast Subs through ShakeSmart. Eight are semantically accepted; outside-food-only X-Wife's Place and no-kitchen Quarters are evidence-exhausted. Cumulative direct review is 510 records: 417 accepted and 93 exhausted.
- **Corrections required from the user:** None. No scoring or classification occurred.
- **What required interpretation:** Customer batter claims stayed attributed; cocktail evolution was not food turnover; culinary philosophy was not item production; event cadence was not menu cadence; assembly did not prove upstream process; carried food was not venue food; archived menus stayed dated; aggregate food mentions did not override first-party no-kitchen evidence; review-platform homemade wording was not operator proof; and brand formulation did not prove branch sourcing.
- **What could be encoded in the skill:** Add customer-process provenance, beverage/food cadence separation, philosophy-versus-process typing, entertainment-versus-menu cadence, assembly/upstream separation, outside-food isolation, archive dating, first-party no-kitchen precedence, platform-summary provenance, and brand-to-branch sourcing limits.

### Phase 5 primary semantic review batch 052 — records 511–520

- **What happened:** The primary orchestrator directly inspected ten records from Skillets through Mira Mira. Nine are semantically accepted; temporarily closed/unrenewed Tappo is evidence-exhausted. Cumulative direct review is 520 records: 426 accepted and 94 exhausted.
- **Corrections required from the user:** None. No scoring or classification occurred.
- **What required interpretation:** Purchased inputs did not make all components purchased; business closure was not menu seasonality; publication process stayed publication evidence; historical concept names were not new branches; domain conflicts were not new entities; chef acclaim was not process proof; AYCE breadth was not fabrication proof; institutional/cafe naming was not production proof; directory hours did not prove liveness; and mixed predecessor/current ratings stayed mixed.
- **What could be encoded in the skill:** Add purchased-input containment, business-calendar versus menu-seasonality typing, publication provenance, concept-name versioning, domain-conflict reconciliation, acclaim-versus-process separation, AYCE non-inference, institution/venue-name non-proof, schedule-versus-liveness rules, and mixed-review inheritance typing.

### Phase 5 primary semantic review batch 053 — records 521–530

- **What happened:** The primary orchestrator directly inspected ten records from Harvest at the Base through Mid City Pub. All ten are semantically complete evidence returns. Cumulative direct review is 530 records: 436 accepted and 94 exhausted.
- **Corrections required from the user:** None. No scoring or classification occurred.
- **What required interpretation:** Exact geography conflict stayed for later eligibility; generic fresh sourcing stayed generic; fast-food description was not exclusion; customer handmade stayed attributed; brand production did not prove branch location; wrong-branch criticism was excluded; legacy-brand process retained uncertainty; menu descriptions did not prove fabrication; chain status was not exclusion; and customer batter/dayparts stayed distinct from operator process/turnover.
- **What could be encoded in the skill:** Add geography-conflict deferral, generic-sourcing containment, fast-food non-exclusion, customer-production provenance, brand-production location uncertainty, wrong-branch review isolation, legacy-brand scope, menu-description process limits, chain non-exclusion, and daypart-versus-turnover rules.

### Phase 5 primary semantic review batch 054 — records 531–540

- **What happened:** The primary orchestrator directly inspected ten records from Alpha Coffee through Pancho's. All ten are semantically complete evidence returns. Cumulative direct review is 540 records: 446 accepted and 94 exhausted.
- **Corrections required from the user:** None. No scoring or classification occurred.
- **What required interpretation:** Menu development did not prove all production; pre-COVID menu evidence was not current; catering claims did not cover all restaurant food; category labels did not prove fabrication; legacy identity stayed historical; chain scale was not exclusion; brunch was not seasonality; item names were not process proof; mail-order freezing was not local-order freezing; and homemade tortillas did not prove nixtamalization.
- **What could be encoded in the skill:** Add menu-development scope, predecessor-menu currentness, catering/restaurant scope separation, category-label process limits, legacy-identity versioning, chain non-exclusion, service-versus-seasonal cadence, item-name process limits, channel-specific freezing, and production-depth typing.

### Phase 5 primary semantic review batch 055 — records 541–550

- **What happened:** The primary orchestrator directly inspected ten records from Slice House through Carson Kitchen. All ten are semantically complete evidence returns. Cumulative direct review is 550 records: 456 accepted and 94 exhausted.
- **Corrections required from the user:** None. No scoring or classification occurred.
- **What required interpretation:** Franchise status was not exclusion; customer crust was not fermentation proof; fresh vegetables were not named sourcing; secret-menu labels were not cadence; seasonal event food was not a standing menu; cultural authenticity was not production proof; cocktail seasonality was not food turnover; disputed chain labeling stayed a conflict; and menu terminology did not prove unstated in-house work.
- **What could be encoded in the skill:** Add franchise non-exclusion, texture-versus-process typing, generic-freshness sourcing limits, secret-menu cadence limits, event-food/menu distinction, authenticity/process separation, beverage/food cadence separation, chain-label conflict handling, and menu-term production containment.

### Phase 5 primary semantic review batch 056 — records 551–560

- **What happened:** The primary orchestrator directly inspected ten records from Ramen 930 through Santo Taco. Eight are semantically accepted; food-truck-only SaltFire and permanently closed Santo Taco Holladay are evidence-exhausted. Cumulative direct review is 560 records: 464 accepted and 96 exhausted.
- **Corrections required from the user:** None. No scoring or classification occurred.
- **What required interpretation:** Co-location did not prove replacement; hand forming did not prove grinding; customer handmade stayed attributed; cafe format did not prove baking; historical locations stayed dated; crepe cooking did not prove fillings; brewery production was not food production; customer supplier allegations stayed unverified; ingredient seasonality was not dated cadence; and stale locators did not override closure.
- **What could be encoded in the skill:** Add co-location/replacement thresholds, forming-versus-grinding depth, customer-production provenance, venue-name non-proof, historical-location dating, assembly/component scope, beverage-versus-food production, allegation verification, ingredient-seasonality versus cadence, and exact-branch closure precedence.

### Phase 5 primary semantic review batch 057 — records 561–570

- **What happened:** The primary orchestrator directly inspected ten records from Bjorn's Brew through HalGaTteok. Nine are semantically accepted; permanently closed Mom's is evidence-exhausted. Cumulative direct review is 570 records: 473 accepted and 97 exhausted.
- **Corrections required from the user:** None. No scoring or classification occurred.
- **What required interpretation:** Grab-and-go breadth did not prove manufacture; airport-authority liveness outweighed a directory closure while company process stayed nonlocal; other branches were isolated; historical hours were not current; closed-day wording was not closure; retail/restaurant production stayed separate; brewing did not become food production; conflicting spirit claims stayed unresolved; holiday closure was not turnover; and configurable formats did not prove component production.
- **What could be encoded in the skill:** Add menu-format non-proof, authoritative-liveness precedence, company/stall production separation, cross-branch isolation, historical-schedule dating, closed-day versus closure parsing, retail/restaurant channel separation, beverage/food production separation, conflict preservation, holiday-status typing, and configurable-format process limits.

### Phase 5 primary semantic review batch 058 — records 571–580

- **What happened:** The primary orchestrator directly inspected ten records from Sanfran Burrito through Pho Salt Lake. All ten are semantically complete evidence returns. Cumulative direct review is 580 records: 483 accepted and 97 exhausted.
- **Corrections required from the user:** None. No scoring or classification occurred.
- **What required interpretation:** Customer scratch wording stayed attributed; new-item messaging was not seasonal cadence; modular assembly did not imply premade components; venue naming did not prove scratch work; customer freshness stayed attributed; menu labels did not prove fermentation; corporate process stayed corporate; frozen allegations stayed attributed and other venues isolated; item removal was not rotation policy; and platform freshness was not operator proof.
- **What could be encoded in the skill:** Add customer-process provenance, new-item versus seasonal-cadence typing, modular-assembly non-inference, venue-name non-proof, cuisine-label process limits, corporate-scope enforcement, frozen-allegation typing, cross-venue isolation, item-removal versus cadence, and platform-summary provenance.
### Phase 5 repair wave 062 — provenance and canonical-closure repair

- **Candidates:** R-1620 Healthy Vibes, R-1621 Thai Taylorsville, R-1623 Café Thảo Mi, and R-1624 Delicias Fruty Snacks.
- **What happened:** Added exact extractor-compatible unavailable-field closures and five-stage trails for all four. Healthy Vibes gained durable Mapcarta and municipal-report provenance while preserving the restaurant-tag/reception-center conflict. Thai Taylorsville was rebuilt around current Toast and exact-directory evidence. Café Thảo Mi retains current licensing/directory evidence while historical and unrenewed adverse claims are clearly versioned or withdrawn. Delicias retains exact social-linked directory identity, menu names and separate rating snapshots while unsupported production claims remain closed.
- **Corrections required from the user:** None. No scoring, low-novelty classification, ranking or disqualification occurred.
- **What required interpretation:** OSM cuisine/category tags did not establish current food operation; municipal event hours were not restaurant hours; literal menu verbs did not prove scratch production; historical editorial evidence did not become current workflow evidence; and separate platform ratings were not reconciled into one aggregate.
- **What could be encoded in the skill:** Prescribe `Unavailable fields:` as the exact canonical extractor heading; require business-use conflicts to be typed by source/date; distinguish event hours from food-service hours; version historical production/format evidence; and require platform ratings to remain source-specific unless reconciliation is explicit.
### Phase 5 repair wave 063 — provenance, succession and channel-scope repair

- **Candidates:** R-1625 Refreskeria Mi Fiesta Facil, R-1626 Mina's Polynesian Hut, R-1664 Tea Rose Thai Express, and R-1667 Celeste Bite.
- **What happened:** Added exact canonical closures and five-stage trails for all four, plus durable URL provenance for Tea Rose and Celeste. Refreskeria's food claims were sharply reduced because only entity/co-location and historical review evidence renewed. Mina's retains city-license and current exact-directory evidence without inferring production from freshness. Tea Rose preserves temporary closure and same-address/phone Hart Yai succession uncertainty. Celeste keeps restaurant and truck as separately licensed channels without inferring shared production.
- **Corrections required from the user:** None. No scoring, novelty classification, ranking or disqualification occurred.
- **What required interpretation:** Co-located legal entities could not share phones/functions; litigation unrelated to food could establish entity identity but not food quality; freshness language did not locate production; same-address/phone replacement evidence did not prove reopening; and dual restaurant/truck licenses did not establish a commissary workflow.
- **What could be encoded in the skill:** Require entity-versus-trade-function separation, permit non-food legal records for identity only, type same-address succession conflicts explicitly, distinguish generic freshness from production location, and require channel-specific production evidence for restaurant/food-truck hybrids.
### Phase 5 repair wave 064 — sparse-branch and venue-scope provenance repair

- **Candidates:** R-1668 Makizushi, R-1673 Freshëns, R-1678 Wakara Bar, and R-1712 Soy's Sushi Bar and Grill.
- **What happened:** Added durable URL provenance, canonical closures and five-stage trails for all four. Makizushi preserves three conflicting phones. Freshëns was reduced to a weak airport directory listing because the generic terminal address does not identify a stall or connect to the ledger coordinate. Wakara retains outlet identity while hotel-level evidence is kept out of food-process claims. Soy's gained current operator/city provenance and preserves legacy phone and MenuPix address/ZIP variants.
- **Corrections required from the user:** None. No scoring, novelty classification, ranking or disqualification occurred.
- **What required interpretation:** Generic airport addresses were not branch identifiers; current co-address businesses did not prove replacement; hotel evidence did not transfer to an outlet; government licensing established identity but not current menu; and customer sourcing claims remained customer evidence.
- **What could be encoded in the skill:** Require stall-level proof for airports/campuses, explicit confidence penalties for generic-address listings, hotel-property/outlet evidence isolation, typed multi-phone/address conflicts, and customer-versus-operator sourcing separation.
### Phase 5 repair wave 065 — channel, closure and provenance repair

- **Candidates:** R-1713 7Buddha Tea House and Desserts, R-1719 Cluck Truck, R-1760 Atlantis Burgers Kearns, and R-1763 Early Owl.
- **What happened:** Added durable URL provenance, exact five-stage trails and canonical closures for all four. 7Buddha renewed current order/directory evidence. Cluck Truck keeps former mobile and current fixed channels distinct and preserves phone conflict. Atlantis now carries explicit closed-directory/closed-delivery versus local-report-open conflict plus same-address succession uncertainty. Early Owl preserves the 8 p.m. operator-order versus 3 p.m. directory hours conflict.
- **Corrections required from the user:** None. No scoring, novelty classification, ranking or disqualification occurred.
- **What required interpretation:** Delivery closure did not necessarily prove business closure; a fixed storefront did not prove the truck stopped; same-address later businesses did not prove succession; ingredient seasonality did not establish menu turnover; and aggregator sourcing summaries did not become operator facts.
- **What could be encoded in the skill:** Add closure-state fields by channel, require mobile/fixed schedules to remain separate, type same-address succession uncertainty, distinguish ingredient seasonality from menu cadence, and prohibit aggregator summaries from upgrading sourcing provenance.
### Phase 5 repair wave 066 — collision-prone identity and channel repair

- **Candidates:** R-1784 The Bar, R-1797 PIKO Mexican Grill, R-1798 Best Ever Burgers, and R-1807 The Green Room.
- **What happened:** Added durable provenance, canonical closures and five-stage trails for all four. The Bar resolves only to its exact OSM node and remains otherwise unidentified. PIKO was renewed to an official exact-address domain while house-made claims stayed item-specific. Best Ever Burgers keeps license-base, event and mobile-service locations distinct. Green Room exact-address editorial/directory evidence renews its listening-bar identity without inventing a food program.
- **Corrections required from the user:** None. No scoring, novelty classification, ranking or disqualification occurred.
- **What required interpretation:** An OSM node could be durable provenance without a resolvable business; administrative truck addresses were not service locations; dated truck schedules were not hours or menu turnover; music programming was not food cadence; and same-name venue results required exact-address gating.
- **What could be encoded in the skill:** Permit exact OSM element URLs as sparse-identity provenance, distinguish mobile base/event/service locations, type schedule events separately from hours/turnover, separate venue programming from food cadence, and require exact-address gates for generic venue names.
### Classified scratch-dessert corridor — requested A/B/C deliverable

- **What happened:** Re-expressed the completed east-side dessert completeness audit in the requested durable artifact `05-scratch-dessert-corridor-classified.md`, using only already-classified records. Separated 11 dedicated/dessert-forward confirmed producers (A), five restaurants with genuine scratch-dessert programs (B), and six uncertain/partial records that remain outside the confirmed count (C). Added direct source URLs, record IDs, identity/location, evidence confidence, day-specific 8 PM caveats, exclusions and entity reconciliation.
- **Method:** Unioned the classified corridor summaries, completed worker returns, supplemental returns and index matches by candidate ID and normalized address. Rechecked the already-resolved operator identities and current hour pages where needed; did not perform place discovery or promote any unclassified entity.
- **Discoveries/corrections:** The confirmed total remains 16. R-0457 Franco's Churro House remains the material post-summary addition. Tulie's Cafe/Tulie Bakery remains one alias-resolved record; Hill's Kitchen and Hearth and Hill remain distinct co-located concepts; Table X restaurant dinner hours remain isolated from Table X Bread's bakery availability. The A/B/C version also corrects a common presentation hazard by keeping plausible dessert sellers visibly outside the confirmed count.
- **Ambiguities:** Hill's Kitchen has an 8 versus 8:30 closing conflict; Picnic's Friday dinner does not independently prove dessert-counter availability; Rawtopia's broad handcrafted-dessert wording is merchant copy hosted by OpenTable; Greenhouse Effect's current first-party site was unavailable; Tulie's strongest explicit evidence names components rather than every pastry.
- **Potential SKILL improvements:** Specify a required A/B/C evidence taxonomy; require candidate-universe provenance so “exhaustive” cannot trigger new discovery; generate URL-bearing evidence tables from return citations; model confidence at both program and named-item levels; distinguish `open_after_8`, `closes_at_8`, and `dessert_availability_unproven`; and require ID/address/alias deduplication plus co-located-concept and daypart evidence barriers.

## 2026-07-16 — Phase 5 primary semantic review batch 059

- Directly inspected records 581–590 in the canonical Phase 4 order across five return artifacts; eight had sufficiently scoped, traceable evidence and complete unavailable-field closure to become `evidence-accepted`.
- Caleo is explicitly closed, while Tokyo City is explicitly temporarily closed with no operator reopening date; both were retained historically but moved to `evidence-exhausted-unavailable` for the current restaurant run. This corrected the tempting shortcut of treating a temporary-closure directory record as an active restaurant merely because historic hours and menu evidence exist.
- Corporate or multi-location process language for Yummy's, Ding Tea, and Mo’ Bettahs remains group scoped unless the exact branch independently repeats it. The SKILL could encode a standard “brand claim localization” check so primary review does not have to rediscover this scope rule repeatedly.
- Cumulative primary review is now 590 inspected: 491 accepted, 99 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 060

- Directly inspected records 591–600; all ten passed semantic acceptance with traceable evidence and explicit closure of unresolved fields.
- The batch repeatedly required separating customer-side hot-pot cooking from back-kitchen production, directory/reviewer freshness or handmade language from operator claims, and supplied branded components from house production.
- Annie’s separately rated wedding-vendor scratch claim remained scoped away from the café absent a proven production relationship; this is another case the SKILL could handle with an explicit related-entity claim-transfer barrier.
- Cumulative primary review is now 600 inspected: 501 accepted, 99 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 061

- Directly inspected records 601–610; eight were accepted and two exhausted for the current restaurant population.
- Nomad's researched Fremont identity has been replaced by Uinta's own kitchen after a documented relocation, while Jackalope has no food service. Both retain historical or venue evidence without being treated as current restaurants.
- Durango demonstrates that a sparse record can still be semantically complete when the exact license identity is durable and every food field has a documented full-sequence exhaustion; sparse evidence is not the same as an incomplete search.
- The SKILL could encode explicit candidate-location continuity checks for relocations and a `venue_without_food` terminal state distinct from ordinary closure.
- Cumulative primary review is now 610 inspected: 509 accepted, 101 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 062

- Directly inspected records 611–620; nine were accepted and Soulful Sips was exhausted because the only current status evidence says temporarily closed with no operator reopening date.
- The legacy Creole & Sliders candidate required identity versioning to Old Cuss's current Pierpont operation rather than treating the former address/name as a separate restaurant or discarding the durable operator continuity.
- FAV's unusually strong group-wide scratch claims were retained because the owner explicitly applies them to all her kitchens; other group and customer claims remained venue- or source-scoped.
- The SKILL could provide a first-class identity-version record for same-operator relocation/rename continuity, including old/new address, effective evidence dates, and whether the catchment test must be rerun.
- Cumulative primary review is now 620 inspected: 518 accepted, 102 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 063

- Directly inspected records 621–630; eight were accepted and two exhausted.
- Don Joaquín's brand remains active, but brand activity cannot override exact-branch closure warnings and a recent exact-location closure report. Swig could not be localized at all because the candidate lacks a branch identity and several plausible outlets exist.
- Porch retains useful current-review evidence against an explicitly dated 2022 menu, but the old menu is not silently presented as current. This required evidence versioning rather than wholesale rejection.
- The SKILL could encode `brand_active_branch_unresolved`, `branch_identity_missing`, and `dated_menu_with_current_reviews` states to standardize these recurring cases.
- Cumulative primary review is now 630 inspected: 526 accepted, 104 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 064

- Directly inspected records 631–640; all ten passed semantic acceptance.
- Fed Up Kitchen's evidence is strong but describes a pickup/delivery prepared-meal plan meant for reheating, not conventional restaurant service. Phase 5 retains that literal model so Phase 6 can apply format rules without evidence loss.
- The Sushi/Umami required same-address rename preservation because ownership and effective date are unresolved. Grid City's brewery evidence and Sugar House food evidence likewise remained in separate production scopes.
- The SKILL could encode a `prepared_meal_reheat_service` format flag and a standard same-address rename tuple so these facts survive intact into scoring and disqualification.
- Cumulative primary review is now 640 inspected: 536 accepted, 104 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 065

- Directly inspected records 641–650; nine were accepted and Vicky's Peruvian was exhausted because fire-forced closure and current closed status remain unrebutted by the later construction approval.
- Ascent Kitchen again shows the valid sparse-record case: a current exact delivery identity exists, while all unavailable fields have a complete documented search. That differs materially from Vicky's, where strong evidence contradicts current operation.
- Pacific Seas required explicit independent-mirror provenance; Vietopia's operator page asks about broth duration without exposing the answer, which cannot be treated as affirmative process evidence.
- The SKILL could distinguish `current_sparse_active_channel` from `closure_with_rebuild_only` and warn that question-form operator copy is not evidence of its implied answer.
- Cumulative primary review is now 650 inspected: 545 accepted, 105 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 066

- Directly inspected records 651–660; nine were accepted and Yan Express was exhausted because its delivery channel is closed, another restaurant is now tied to the address, and no current exact-venue channel proves operation.
- Elements' current dinner-only hours were kept separate from older lunch evidence. Crema's operator copy explicitly distinguishes one house-made product from locally supplied pastries, a useful negative boundary rather than merely missing evidence.
- Guisados shows that a live exact delivery channel can prove current activity even when weekly storefront hours remain unavailable; Yan Express lacked that live channel and had contradictory occupancy evidence.
- The SKILL could define a channel-liveness hierarchy and require explicit temporal versioning whenever current official hours conflict with older reservation/hotel records.
- Cumulative primary review is now 660 inspected: 554 accepted, 106 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 067

- Directly inspected records 661–670; all ten passed semantic acceptance.
- Canton Wok is a valid fully exhausted sparse record: exact address and format survive, while every scoring-relevant field has a documented completed search. Good Spirits required separate venue and kitchen hour clocks.
- ROCTACO and Arigato each have recurring promotions, but promotion cadence is not the same as menu rotation. You & I's same-recipes-across-locations statement does not prove commissary or branch-local production.
- The SKILL could encode separate `promotion_cadence`, `menu_turnover`, `venue_hours`, and `kitchen_hours` fields to prevent these recurring category errors.
- Cumulative primary review is now 670 inspected: 564 accepted, 106 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 068

- Directly inspected records 671–680; eight were accepted and two exhausted.
- June's retains unusually strong historical scratch evidence but lacks current operational continuity after its departure announcement. Magpie's current official model is packaged market products and classes, not restaurant meal service.
- The Capital Grille is a useful counterexample to cheap chain exclusion: a national chain can still document branch-level dry-aging and on-premise butchery. Naivedhyam required separation of retail batter/meal kits from prepared dishes.
- The SKILL could add `historically_strong_process_but_inactive`, `packaged_market_vendor_not_restaurant`, and `retail_component_vs_prepared_dish` states.
- Cumulative primary review is now 680 inspected: 572 accepted, 108 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 069

- Directly inspected records 681–690; eight were accepted and two exhausted.
- Habanero Express is explicitly closed. The generic OSM “Indian Food” point preserves historical gas-station-counter evidence but cannot be proven as a distinct current restaurant; convenience-store hours and ratings were not transferred.
- Tamarind's every-morning hand-rolling evidence remains limited to egg rolls, while Eggsburgh's house-made claim remains limited to corned beef. This batch again required item-level scope discipline.
- The SKILL could encode a co-located-counter identity test and prohibit host-store ratings/hours from transferring unless the food operation is formally the same entity.
- Cumulative primary review is now 690 inspected: 580 accepted, 110 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 070

- Directly inspected records 691–700; nine were accepted and Beehive Bitez Station Park was exhausted because hiring for an arriving location does not prove it is open.
- Provo sibling-branch dough/menu evidence was not transferred to Station Park. Scion's in-house cider production was separated from its explicitly purchased/imported snack program.
- Old Cuss overlaps the earlier legacy Creole & Sliders candidate through the same relocation/rename chain; both evidence records remain durable, but the final ledger and ranking must merge them to one canonical entity.
- The SKILL could add `announced_or_hiring_not_open`, mandatory sibling-branch scope barriers, and an explicit semantic-review duplicate-entity register carried into ranking.
- Cumulative primary review is now 700 inspected: 589 accepted, 111 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 071

- Directly inspected records 701–710; nine were accepted and the generic OSM “sushi counter” was exhausted because no current public trade identity or operation could be verified.
- Chabaar's live official/group and ordering channels conflict with a temporary-closure directory label; liveness was retained while the conflict remains visible. Nearby named sushi venues were not attached to the generic OSM point.
- 2 Row's brewery production and kitchen-food evidence stayed separate; Baan Thai's occasional dessert unavailability was not promoted to a turnover cadence.
- The SKILL could encode a source-priority liveness matrix for `live merchant channel` versus `directory temporary closure`, while still requiring the conflict to survive in the ledger.
- Cumulative primary review is now 710 inspected: 598 accepted, 112 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 072

- Directly inspected records 711–720; nine were accepted and Silverlake Ramen Riverton was exhausted because exact-branch closure is explicit and the branch is absent from the current locator.
- Houston Hot Chicken required successor-tenant versioning with all Crack Shack process evidence excluded. Dirty Bird's live ordering and current license outweighed older user closure discussion while preserving the contradiction.
- Maize's tortillas are handmade but explicitly off site; that location fact must survive into scoring instead of being flattened into either “house-made” or “premade.”
- The SKILL could add `off_site_same-operator production` as a distinct process-location state and formalize current license plus live merchant-channel priority over older discussion posts.
- Cumulative primary review is now 720 inspected: 607 accepted, 113 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 073

- Directly inspected records 721–730; all ten passed semantic acceptance.
- Redmond's official FAQ locates its production kitchen in Springville, so the many house-made items are same-company off-site production rather than on-premises scratch. Logos similarly separates external City Cakes food from its beverage/roasting program.
- Tang Huo's active exact channels conflict with a weak “may be permanently closed” label; activity is retained with the conflict. Garage Grill's quarterly car rotation is decor turnover, not food turnover.
- The SKILL could require a three-valued production-location field: `on_premises`, `same_operator_off_site`, and `external_supplier`, plus a separate non-food-programming cadence field.
- Cumulative primary review is now 730 inspected: 617 accepted, 113 exhausted, 0 repair-routed.
### Phase 5 repair wave 067 — co-tenant and shared-hall provenance repair

- **Candidates:** R-1808 Mr. D's Instant Hot Pot, R-1809 Chengdu Hotpot & BBQ, R-1810 Heaya Ramen & Rice Bowl, and R-1881 Greek Tyrant by Aristo.
- **What happened:** Added durable provenance, canonical closures and five-stage trails for all four. Mr. D's was reduced to exact Grubhub merchant evidence. Chengdu's exact Suite 8 city/BBB/order identity replaces the erroneous ledger address. Heaya's Suite 2 temporary-closure versus active-order conflict is preserved. Greek Tyrant gains a current stall menu while shared hall ratings/hours remain explicitly shared.
- **Corrections required from the user:** None. No scoring, novelty classification, ranking or disqualification occurred.
- **What required interpretation:** Same street address did not permit cross-suite evidence; an active order page did not override temporary closure; shared food-hall ratings/hours were not stall-specific; daily sides were not entrée turnover; and platform format labels did not prove commissary production.
- **What could be encoded in the skill:** Require suite-level entity isolation, explicit closure-versus-order conflicts, shared-hall versus stall field typing, accompaniment-frequency versus menu-cadence separation, and platform-label non-proof for production location.
### Phase 5 repair wave 068 — seasonal stand and sparse-node provenance repair

- **Candidates:** R-1946 Recharge Pub & Grub, R-1948 Bob's Brainfreeze, R-1982 Billy Bob Joe Chuck's, and R-0015 The Big Easy.
- **What happened:** Added durable provenance, five-stage trails and canonical closures for all four. Recharge preserves three-way hours conflict and its bike-shop-offshoot scope. Bob's uses current-dated city coverage plus exact directory evidence while phone/current-season status remain unresolved. Billy Bob Joe Chuck's and The Big Easy now point to exact OSM nodes but remain otherwise exhausted. The Big Easy's hours, menu, process, turnover, sourcing and review fields are individually closed after the full sequence.
- **Corrections required from the user:** None. No scoring, novelty classification, ranking or disqualification occurred.
- **What required interpretation:** Toast “all closed” did not conclusively override active directories; seasonal city coverage did not prove current-day operation; sale notices did not prove closure; exact OSM nodes could preserve candidate provenance without corroborating business identity; and generic same-name results were excluded.
- **What could be encoded in the skill:** Add multi-source hours/status conflict objects, require season/year dating for seasonal stands, distinguish sale notices from closure, permit exact OSM-node provenance for exhausted identities, and require individually enumerated closure fields for sparse candidates.
### Phase 5 repair wave 069 — sparse café and sourcing-boundary repair

- **Candidates:** R-0017 Roberts Restaurant, R-0041 Java Bytes, R-0042 PC Pho, and R-0046 Nordstrom Ebar.
- **What happened:** Added canonical trails/closures for all four. Java Bytes now has durable exact OSM provenance and individually closed price, hours, menu, process, turnover, sourcing and review fields. Roberts, PC Pho and Ebar each have explicit sourcing closure after exact branch/operator sequences; dish ingredients and category text were not upgraded to suppliers.
- **Corrections required from the user:** None. No scoring, novelty classification, ranking or disqualification occurred.
- **What required interpretation:** Generic homemade wording did not prove components; menu ingredients did not identify suppliers; platform closure applied only to delivery; national brand menus/nutrition did not establish branch production; and nearby institutional cafés were not transferred to a sparse OSM node.
- **What could be encoded in the skill:** Require supplier identity separate from ingredient inventory, contain generalized homemade claims, type closure by channel, distinguish brand standards from branch execution, and prescribe exact OSM provenance plus individually enumerated closures for sparse cafés.
### Phase 5 repair wave 070 — final sparse-pub structural repair

- **Candidate:** R-0055 Junior's Tavern.
- **What happened:** Added durable exact-node provenance, an exact five-stage trail and canonical closure. Price, hours/day-part, menu, production/process, turnover, sourcing and review fields were each individually exhausted after the full source sequence. Same-name out-of-state and unrelated tavern results were excluded.
- **Corrections required from the user:** None. No scoring, novelty classification, ranking or disqualification occurred.
- **What required interpretation:** An exact OSM element preserves candidate provenance without corroborating a current business; a pub tag does not establish food service, hours or menu; and failure to corroborate operation does not prove closure.
- **What could be encoded in the skill:** Require exact OSM element links for sparse candidates, individually enumerated unavailable-field closures, explicit same-name exclusion logs, and a rule separating uncorroborated operation from closure evidence.

## 2026-07-16 — Tight east-side scratch-dessert subset

- **What happened:** A subagent rechecked the entire classified/researched candidate universe for Millcreek, East Millcreek/Foothill, Sugar House, 9th & 9th/9th South, 15th & 15th, and immediately touching east-side areas. It produced `05-scratch-dessert-eastside-subset.md`: 14 confirmed places, comprising 10 dedicated or dessert-forward producers and 4 restaurants with credible scratch-dessert programs. Eight have supported service after 8 PM on at least one normal evening; one additional place is a conditional Friday case and one has an 8 PM hours conflict.
- **Corrections required from the user:** None during this subtask.
- **What required interpretation:** Neighborhood edges are subjective without polygons; a whole-universe scan was necessary because category filtering misses restaurant pastry programs; production may be on-premises, at a same-operator commissary, externally supplied, or unknown; co-located concepts cannot inherit one another's evidence or hours; “after 8,” “closes at 8,” conflicting hours, and unproven dessert availability are different states; broad scratch claims cannot automatically promote desserts unless the evidence connects them; and alias/address deduplication is required before counting.
- **What could be encoded in the skill:** Define corridor inclusion with explicit polygons or a documented local-continuity rule; require a dessert scan over the whole classified universe rather than dessert-category names alone; model production location at item level as `on_premises`, `same_operator_off_site`, `external_supplier`, or `unknown`; prohibit evidence and hours inheritance across co-located concepts/dayparts; model evening availability with distinct after-8, boundary, conflict, and unproven states; require an explicit semantic link before broad scratch claims promote dessert items; and require candidate-ID plus normalized-address alias deduplication before totals are reported.

## 2026-07-16 — Phase 5 primary semantic review batch 074

- **What happened:** The primary agent directly inspected ten more evidence packages: Don Daniel's, Thai Better, Protein Foundry, Pizza Hut Delivery, Saigon Blossom, Janet's Sunshine Cafe, Beaumont Bakery & Cafe, Dickey's Barbecue Pit, Great India, and Seabird. All ten were evidence-accepted; none required repair or evidence-exhausted closure.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Menu cooking verbs do not prove component fabrication; “homemade” and “house” wording must stay source and item scoped; national-brand craft wording does not establish branch production; a broad operator scratch claim is useful but not automatically component-specific; pastry inventory does not prove every pastry's production; and cocktail craft/rotation cannot be transferred to a bar's food program.
- **What could be encoded in the skill:** Add explicit semantic guards separating final-cooking verbs from fabrication, item labels from program-wide production, brand standards from branch execution, broad scratch claims from component-specific facts, pastry-menu presence from pastry-process evidence, and beverage production/cadence from food production/cadence.
- **Progress:** Cumulative primary review is now 740 inspected: 627 accepted, 113 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 075

- **What happened:** The primary agent inspected ten more packages. Crown Burgers, My Pie, Ginza, Venezuela Mia, Fortune Cuisine, 1% Fitness Kitchen, and Rooster's Gourmet Popcorn were accepted. Roxberry Holladay, Fajita Grill ToGo, and Hello Boba were closed as evidence-exhausted because current operation could not be established or explicit closure evidence prevailed.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** A branch's removal from an official locator matters more than stale directory presence; brand-wide promotions cannot be assigned to an unverified former branch; explicit closure plus no reopening evidence prevails over stale menu hours; a newer same-address tenant strengthens but does not alone prove closure; cooking verbs do not establish component fabrication; weekly delivery cadence is not weekly menu cadence; and a current moved location can remain valid evidence while later geographic eligibility is handled separately.
- **What could be encoded in the skill:** Add a current-operation precedence ladder covering official-locator removal, explicit closure, stale directory hours, and replacement tenants; prohibit brand-wide cadence inheritance to unverified branches; distinguish delivery cadence from menu turnover; and preserve moved-outside-catchment identities for a separate eligibility decision rather than silently discarding them during evidence acceptance.
- **Progress:** Cumulative primary review is now 750 inspected: 634 accepted, 116 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 076

- **What happened:** The primary agent inspected ten more packages. Aroon Thai Kitchen, Hill's Kitchen, Hearth and Hill, Chop Shop, Taste of Thai, Mochinut, Toro Ramen, and Athena VII were accepted. Louks Greek Baby Donuts and So Grill were closed as exhausted because explicit closure/successor evidence established that the researched concepts no longer operate.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Co-located concepts cannot share production evidence; a pastry-selection change signal does not prove every pastry's production; program-level dessert claims stay dessert scoped; customer frozen/bottled allegations remain attributed; a special flavor or sellout does not prove cadence; and successor evidence must remain separate from the closed predecessor even when address and phone persist.
- **What could be encoded in the skill:** Require evidence isolation for co-located concepts and predecessor/successor entities; distinguish assortment variability from fabrication evidence and systematic turnover; and type adverse process statements by provenance so customer allegations cannot silently become operator facts.
- **Progress:** Cumulative primary review is now 760 inspected: 642 accepted, 118 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 077

- **What happened:** The primary agent inspected ten more packages. Darla's Donuts, Phở Saigon Noodle House 2, Tuk Tuks, Taqueria El Gallo Loco, Donut Boy, Mar Muntanya, The Salt Republic, and Contribution Cocktail Lounge were accepted. Kabul Kitchen and Ocean King were exhausted because current restaurant operation could not be corroborated beyond sparse identity fragments.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Fresh-tasting reviews do not establish production; similarly named restaurant process claims cannot cross branches; category labels cannot fill missing restaurant fields; related market and restaurant entities cannot be conflated; live ordering can outweigh a single closure label while preserving conflict; equipment proves capacity rather than universal fabrication; and beverage production or menu versioning does not establish food production or regular turnover.
- **What could be encoded in the skill:** Add minimum current-operation corroboration requirements for sparse identities; prohibit same-name and adjacent-market evidence transfer; distinguish production observations, equipment capacity, and customer freshness impressions; and enforce separate food-versus-beverage production and cadence fields.
- **Progress:** Cumulative primary review is now 770 inspected: 650 accepted, 120 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 078

- **What happened:** The primary agent inspected ten more packages. Nine were accepted; the generic “Hot dog” point was exhausted after entity resolution could not connect it to any exact local business.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Hotel bakery evidence cannot be transferred to a lounge dessert; a dated menu revision is not regular cadence; customer-visible preparation is item/visit scoped; branch-level brand standards require an exact branch source; weekly event-hours updates are not food turnover; broad ingredient-quality language does not identify suppliers; and historic branch expansion does not prove the current branch count.
- **What could be encoded in the skill:** Add explicit evidence-isolation rules among hotel outlets; type one-off menu changes separately from cadence; require scope metadata for customer-observed preparation; require branch localization for brand process claims; and separate operational schedule changes and historic expansion from menu turnover and current footprint.
- **Progress:** Cumulative primary review is now 780 inspected: 659 accepted, 121 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 079

- **What happened:** The primary agent inspected ten more packages. Cilantree, Xing Fu Tang, Franklin Avenue, Urban Hill, Yakuza Ramen, and Trolley Cottage Café were accepted. Eleven SLC lacked a food operation, Everbowl resolved only to an out-of-catchment branch, Zapareco could not be resolved, and ACME was closed; those four were exhausted.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Entertainment programming is not menu turnover; an out-of-catchment phone/address cannot repair an unmatched in-catchment candidate; ingredient seasonality is not menu cadence; sister-kitchen production needs explicit off-site attribution; editorial winter framing is not operator scheduling; and versioned menus establish change without establishing frequency.
- **What could be encoded in the skill:** Add non-food-venue closure handling; require coordinate/phone/address agreement before branch identity transfer; separate ingredient seasonality, editorial framing, one-time change, and systematic cadence; and represent same-operator/sister-kitchen production explicitly as off-premises rather than collapsing it into house-made.
- **Progress:** Cumulative primary review is now 790 inspected: 665 accepted, 125 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 080

- **What happened:** The primary agent inspected ten more packages and accepted all ten. This included standard restaurants plus a shared-kitchen preorder concept and a self-serve kombucha retailer; their unusual formats were preserved for later classification rather than discarded at evidence acceptance.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Customer/platform homemade wording is not operator fact; farm-to-table branding does not identify suppliers or prove scratch production; shared-kitchen production must not be labeled storefront production; supplier fermentation differs from retail keg handling; historical family-recipe sourcing is not current sourcing; and dated menu updates are change events rather than cadence.
- **What could be encoded in the skill:** Model evidence provenance and production location jointly; add explicit shared-kitchen and supplier-retailer formats; prevent broad sourcing brands and historical recipe narratives from becoming current supplier facts; and separate dated change events from systematic menu rotation.
- **Progress:** Cumulative primary review is now 800 inspected: 675 accepted, 125 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 081

- **What happened:** The primary agent inspected ten more packages and accepted all ten. Chappell Brewing's current brewery/food-truck format was retained for later classification while its lack of an in-house food program was explicitly closed.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Buffet replenishment is service cadence rather than menu turnover; brand/cuisine names do not prove component production; ordering-channel closure is not business closure; menu assembly is not fabrication; external food trucks are not a brewery kitchen; a named component supplier does not generalize across the menu; lapsed domains do not override strong current evidence; and geographic ingredient labels are not supplier identities.
- **What could be encoded in the skill:** Distinguish service replenishment, menu rotation, and channel status; prohibit production inference from brand/cuisine names and assembly language; model external food vendors separately from host venues; and separate geographic ingredient origin from a named producer or supplier.
- **Progress:** Cumulative primary review is now 810 inspected: 685 accepted, 125 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 082

- **What happened:** The primary agent inspected and accepted ten more packages. Paradise Biryani Pointe's uncertain equivalence to the contact-less candidate was preserved explicitly, while the best geospatial match and all retrieved evidence remained usable.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Ingredient seasonality differs from menu rotation; external dessert/bakery sales are supplier evidence; day-specific slots do not prove their cadence or fabrication; uncertain candidate equivalence belongs in mapping metadata; predecessor evidence cannot become successor evidence; uploaded menu versions do not prove operator cadence; and co-located businesses cannot inherit one another's production.
- **What could be encoded in the skill:** Add canonical-match confidence and unresolved-equivalence fields; separate ingredient seasonality, named day slots, and systematic rotation; require predecessor/successor provenance isolation; and enforce evidence boundaries for co-located vendors and externally supplied food.
- **Progress:** Cumulative primary review is now 820 inspected: 695 accepted, 125 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 083

- **What happened:** The primary agent inspected and accepted ten more packages, including hotel lounges, a seasonal walk-up window, an unusually sparse exact chain branch, and a shared-kitchen Filipino restaurant.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Entertainment and décor cadence differ from menu turnover; cultural/marketing language does not prove production; customer in-house claims remain attributed; other-location chain evidence cannot fill branch gaps; shared corporate menu facts require explicit scope; and seasonal operating windows and shared-kitchen locations need their own format metadata.
- **What could be encoded in the skill:** Model entertainment, décor, operating-season, food-menu, and beverage cadence separately; require source-provenance flags for production claims; enforce branch isolation while permitting explicitly scoped corporate-menu evidence; and add first-class seasonal-window and shared-kitchen formats.
- **Progress:** Cumulative primary review is now 830 inspected: 705 accepted, 125 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 084

- **What happened:** The primary agent inspected and accepted ten more packages. Rooster's Gourmet Popcorn R-1464 was identified as overlapping the previously reviewed R-1323 and was flagged for one canonical entity in the final ledger and ranking.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Shared brand recipes are not necessarily branch-observed practice; local/seasonal language does not identify suppliers; external component suppliers remain valid within broad scratch programs; labor allegations must stay separate from food evidence; co-located concepts cannot exchange production evidence; homemade-taste marketing is not fabrication; historical family harvesting is not current sourcing; former-menu process evidence cannot become current; and duplicate candidate IDs require canonical merging before counts.
- **What could be encoded in the skill:** Require canonical ID/address/phone deduplication before ledger counts; type brand standards, branch observations, historic practices, current sourcing, and non-food allegations separately; and enforce evidence boundaries for co-located virtual or physical concepts.
- **Progress:** Cumulative primary review is now 840 inspected: 715 accepted, 125 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 085

- **What happened:** The primary agent inspected ten more packages. Nine were accepted; Myungrang Hotdog was exhausted because exact branch sources establish closure and no reopening evidence was recovered.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Customer-observed expansion is not cadence; brand consistency and process claims need branch scope; illness causation stays unverified; customer-reported seasonal closure and ownership remain attributed; campus context cannot transfer institution-wide kitchen evidence; named outside producers remain component scoped; and broad freshly-made wording does not identify fabricated components.
- **What could be encoded in the skill:** Add claim-scope fields for brand, branch, institution, component, and customer attribution; require explicit causal-status handling for illness claims; and distinguish menu change events, operating-season reports, and systematic food turnover.
- **Progress:** Cumulative primary review is now 850 inspected: 724 accepted, 126 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 086

- **What happened:** The primary agent inspected and accepted ten more packages. Live official 2026 evidence outweighed weaker temporary/closed directory labels for Monsieur Crêpes, Poke Kings, and Citizens, with every conflict preserved.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Coffee and cocktail turnover cannot become food cadence; delivery-channel closure is not business closure; carefully prepared wording is not fabrication; fixed-menu frequency conflicts must remain literal; temporary co-location does not negate operation; house-spice wording does not identify a producer; farming homage is not sourcing; and live official dated activity can outweigh weaker directory closure labels without deleting the conflict.
- **What could be encoded in the skill:** Add a source-strength/currentness matrix for business-status conflicts; type closure by channel; keep cadence domain-specific; and prevent atmosphere/history/quality language from promoting production or sourcing claims.
- **Progress:** Cumulative primary review is now 860 inspected: 734 accepted, 126 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 087

- **What happened:** The primary agent inspected and accepted ten more packages, including two venues with directly documented limited bar-food programs and one restaurant with an unresolved current alias/canonical name.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Directory process claims stay attributed; franchise-wide operating facts do not become branch production; alias conflicts belong in canonical mapping; historic dish dates are lineage rather than cadence; cooking techniques do not prove component fabrication; generated summaries without underlying evidence must be rejected; entertainment programming is not food cadence; and group-level ingredient language cannot automatically localize to a branch.
- **What could be encoded in the skill:** Add explicit canonical-alias resolution objects; require underlying-source verification for generated summaries; preserve organizational scope for franchise/group claims; and separate historical lineage, entertainment schedules, and food-menu turnover.
- **Progress:** Cumulative primary review is now 870 inspected: 744 accepted, 126 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 088

- **What happened:** The primary agent inspected ten more packages. Nine were accepted; Coco Loco Sausages was exhausted because its evidence ended at a conflicted 2023 commissary report with no resolvable current operation.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** User allegations remain unverified; stale commissary reports cannot establish current operation; delivery-channel closure does not override current reviews/listings; external pastry and roasting partners must remain separate from cafe kitchen production; community/event programming is not food cadence; format names do not prove scratch; chef-choice offerings do not prove market turnover; and predecessor closure does not apply to a reopened successor identity.
- **What could be encoded in the skill:** Add recency minimums for unresolved commissary/virtual concepts; formalize channel-scoped closure precedence; require production-location isolation for outside partners; and separate event programming, chef choice, historic closure and current food cadence/status.
- **Progress:** Cumulative primary review is now 880 inspected: 753 accepted, 127 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 089

- **What happened:** The primary agent inspected and accepted ten more packages. Blatch's BBQ was retained as a current-but-transitional “2.0” operation with unresolved post-fire hours/cadence rather than forced into a binary status.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Archived specials are historical; dual truck/store formats need explicit representation; hijacked domains do not negate stronger current platform evidence; weekday offer structure is not seasonality; certification claims remain source scoped; customer brewing observations do not prove roasting; predecessor identity must remain separate; transitional/rebuilding status needs more than open/closed; and operational moves or footprint growth are not food turnover/process.
- **What could be encoded in the skill:** Add nonbinary operating states such as seasonal, transitional/rebuilding, channel-only, and schedule-unresolved; model multi-format operations; and keep domain health, predecessor identity, certification provenance, and operational changes separate from production/cadence.
- **Progress:** Cumulative primary review is now 890 inspected: 763 accepted, 127 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 090

- **What happened:** The primary agent inspected ten more packages. Eight were accepted; The Station Nutrition and Carolyn's Pantry were exhausted because neither could be corroborated as a current restaurant beyond stale license or map fragments.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Generic brand sourcing cannot automatically localize; menu sections and stockouts are not turnover; historic campus hours/menu cannot become current; former business-model cadence stays historical; generated summaries need exposed underlying support; limited and staffing-dependent hours need explicit states; placeholder expansion addresses cannot be counted; sibling branch facts cannot transfer; and generic map labels cannot establish restaurant format.
- **What could be encoded in the skill:** Add evidence-date/status fields for institutional outlets; validate announced/placeholder locations before footprint counts; require underlying support for generated summaries; and enforce strict branch isolation plus minimum current-operation corroboration for license/map-only candidates.
- **Progress:** Cumulative primary review is now 900 inspected: 771 accepted, 129 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 091

- **What happened:** The primary agent inspected ten more packages. Nine were accepted; England Hub Bistro was exhausted because its official page says temporarily closed and no current reopening evidence was recovered.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Nearby current customer evidence cannot conclusively name-link an OSM point; temporary closure without reopening is an evidence-exhausted state; artificial flavor disclosure is neutral evidence; broad scratch claims do not allocate production to each component; ingredient names are not producer identities; packaged market inventory is separate from deli production; class demonstrations may be brand/staff rather than branch practice; entertainment updates differ from food specials; and syrup-heavy reviews cannot generalize to every drink.
- **What could be encoded in the skill:** Add link-confidence for unnamed nearby corroboration; represent temporary-closed-without-reopening distinctly; require claim allocation by component/location; and separate retail inventory, instructional process, entertainment cadence, ingredient form and supplier identity.
- **Progress:** Cumulative primary review is now 910 inspected: 780 accepted, 130 exhausted, 0 repair-routed.
### Scratch-dessert east-side completeness delta — whole semantic-review scan

- **What happened:** Re-audited the full classified/researched universe through `05-primary-semantic-review.md`, then reopened relevant Phase 4 returns instead of relying only on the prior dessert summaries. Updated `05-scratch-dessert-eastside-subset.md` from 14 to 17 places with confirmed scratch-dessert presence: 11 dedicated/dessert-forward producers, four restaurants with credible dessert programs, and two deliberately separated limited-item cases.
- **Discoveries/corrections:** Added R-0828 Straw Market SLC in the Avenues. Its current cinnamon-roll baking observations corroborate older detailed daily-baker evidence, while the ownership change prevents generalizing the entire 2016 process. Added R-1189 Crema Foothill only for its house-made rice-krispie treat and preserved its other pastries/cookies as supplied. Added R-0908 Hopkins Brewing only for its official in-house cookie, without inflating one item into a broad dessert program. The strict core/program count is now 15; total confirmed scratch-dessert presence is 17.
- **Ambiguities preserved:** Straw Market's broader daily production is historical and current weekly hours conflict; Crema's supplied pastry boundary is explicit; Hopkins has a single supported dessert item. Existing Hill's Kitchen, Picnic, Rawtopia, Greenhouse Effect, Tulie, and geography caveats remain unchanged.
- **Skill gaps:** A dessert completeness filter must scan semantic production fields across every classified record, not only dessert-category names or prior summaries. It should represent `core dessert producer`, `credible restaurant dessert program`, and `confirmed limited dessert item` separately; encode current-versus-historical process and ownership continuity; retain explicit supplied-item boundaries; and compute after-8 availability independently from production classification.

## 2026-07-16 — Phase 5 primary semantic review batch 092

- **What happened:** The primary agent inspected and accepted ten more packages. The set includes a no-kitchen wine lounge, a frozen-yogurt branch whose core product is made at an unnamed dairy, a brewery with extensive scratch food, and several active restaurants with differing levels of production detail.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Historical process cannot automatically become current; entertainment transitions and bar events are not food cadence; locally made pastry is not necessarily on-premises; review-origin organic claims remain attributed; brewery production and releases differ from kitchen production and food rotation; explicit no-kitchen evidence must survive acceptance; same-company off-site dairy production cannot become shop production; daily-slot labels apply only to named dishes; assembled bowl formats do not prove component fabrication; and competitor comparisons do not establish entity relationships.
- **What could be encoded in the skill:** Add temporal scope to process claims; encode production site and domain-specific cadence; represent no-kitchen and off-site-same-company production as structured facts; allocate daily rotation to exact menu slots; and prohibit entity linkage from reviewer comparisons.
- **Progress:** Cumulative primary review is now 920 inspected: 790 accepted, 130 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 093

- **What happened:** The primary agent inspected and accepted ten more packages, including one unusually sparse exact coffee-counter identity and several operations with strong component-level production evidence.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Historical sibling-location format cannot transfer; packaged inventory differs from kitchen production; beverage rotation is not food cadence; co-tenant evidence must remain isolated; supplied bread cannot become house-made; preorder-only and sellout-limited are operating formats rather than closure; prior incubator kitchens are historical; fast service is neutral; ingredient lists do not prove component fabrication; and named commercial sauces must remain explicit rather than generalized.
- **What could be encoded in the skill:** Add strict co-tenant and historical-location isolation; distinguish sparse-but-corroborated active identities from evidence exhaustion; type cadence by beverage versus food; represent supplied and commercial components; and model preorder/sellout operations without forcing ordinary restaurant hours.
- **Progress:** Cumulative primary review is now 930 inspected: 800 accepted, 130 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 094

- **What happened:** The primary agent inspected and accepted ten more packages. One sparse breakfast storefront retained substantial founder/event evidence despite missing ordinary directory fields; the remainder ranged from an ingredient-driven fine-casual restaurant to local and national fast-casual branches.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Market-vendor and storefront phases need separation; restaurant-group siblings cannot share evidence; disputed microwave allegations remain attributed; repeated menu formats do not prove premade production; water-based frozen treats are not inherently a negative process inference; undated menu-section labels do not prove exact rotation; broad format is neutral; low-novelty chain status belongs in later scoring; chef choice is not market cadence; and national claims remain brand scoped.
- **What could be encoded in the skill:** Add operational-phase modeling; prohibit sibling-concept transfer; type disputed adverse allegations; keep menu repetition separate from production inference; require dates for rotation claims; and preserve branch-versus-brand scope for chain evidence and later novelty heuristics.
- **Progress:** Cumulative primary review is now 940 inspected: 810 accepted, 130 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 095

- **What happened:** The primary agent inspected ten more packages. Eight were accepted; 4111 Nutrition and Healthy Vibes were exhausted because only map/municipal identity fragments survived, with no corroborated current food operation or substantive evidence.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Cross-regional menu breadth is neutral; coffee production and cadence are beverage scoped; historical service modes do not become current; unrelated allegations should be excluded; similarly named nutrition clubs cannot fill exact-entity gaps; municipal nighttime-noise evidence does not establish food service; chef-whim updates have no fixed cadence; customer-stated predecessor ownership remains attributed; old inspections stay historical; and review claims of prepackaging/microwaving remain allegations.
- **What could be encoded in the skill:** Add a minimum-current-operation threshold for map-only nutrition concepts; prohibit municipal incident evidence from standing in for food-operation proof; type beverage versus food production/cadence; time-scope service modes and inspections; and structurally label disputed preparation allegations.
- **Progress:** Cumulative primary review is now 950 inspected: 818 accepted, 132 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 096

- **What happened:** The primary agent inspected ten more packages. Nine were accepted; Kompas Taqueria was exhausted because the researched Draper business could not be connected to the candidate's unspecified in-catchment coordinate.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Menu categories do not prove fabrication; co-address nonrestaurant businesses need identity isolation; customer food-safety claims remain allegations; limited service days are not turnover; predecessor-brand talk stays attributed; group context does not transfer process; flavor comparisons do not identify commercial inputs; combo-counter structure does not establish premade food; polished evidence for a different location cannot repair candidate identity; drink cadence does not become food cadence; and advance preparation does not imply commissary production.
- **What could be encoded in the skill:** Require coordinate-to-identity linkage before accepting a researched off-coordinate match; add co-address entity isolation; label allegation type and evidentiary status; keep service schedule and menu cadence separate; and prohibit format or advance-prep facts from automatically becoming centralized-production findings.
- **Progress:** Cumulative primary review is now 960 inspected: 827 accepted, 133 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 097

- **What happened:** The primary agent inspected ten more packages. Seven were accepted; the documented-closed Slapfish and Nékter Lehi branches and the unlinked Taqueria La Palapa coordinate candidate were exhausted.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Holiday items do not establish regular cadence; brand membership belongs in later novelty analysis; chef choice does not prove sourcing rotation; closed branches retain historical evidence but fail current operation; review freshness does not prove onsite baking; other-location defects cannot transfer; beverage production/cadence differs from intermittent food; a researched restaurant needs coordinate linkage; and an exact-address current successor can be canonical even when the ledger label is unsupported.
- **What could be encoded in the skill:** Add a canonical exact-address successor rule alongside the coordinate-linkage requirement; formalize current-closed versus historical evidence states; isolate branch-specific defects; and separate beverage and food production/cadence for taprooms.
- **Progress:** Cumulative primary review is now 970 inspected: 834 accepted, 136 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 098

- **What happened:** The primary agent inspected ten more packages. Seven were accepted; temporarily closed Tea Rose Thai Express, explicitly departed Uncle Sharkii Millcreek, and unlinked/currently unresolved Freshens were exhausted.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Related-operator restaurant facts cannot transfer; former-location specials remain historical; frozen-product customer reports remain attributed; commercial comparisons do not identify inputs; predecessor closure differs from current operation; nontraditional menu format is neutral; recurring promotions and event buffets are not ingredient cadence; corporate out-of-state facts cannot fill local gaps; virtual-brand labels do not negate a physical restaurant; and limited hotel-bar format belongs in later scoring.
- **What could be encoded in the skill:** Add operator-sibling isolation, former-location temporal scope, explicit departed-store handling, coordinate linkage for airport listings, physical-versus-virtual channel modeling, and separate promotion/event cadence from food-menu turnover.
- **Progress:** Cumulative primary review is now 980 inspected: 841 accepted, 139 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 099

- **What happened:** The primary agent inspected and accepted ten more packages, including a sparse but currently official nightclub food operation, a booking-based caterer/truck with legacy storefront hours, and several restaurants with strong item-level process evidence.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Holiday seatings are not seasonal rotation; former-address process stays historical; predecessor reopening does not transfer process; fresh wording is component scoped; broad menus do not imply scratch; sourcing standards do not identify producers; timed service menus differ from seasonality; truck-to-storefront changes are operational phases; booking and storefront channels need separation; and entertainment/event cadence is not food turnover.
- **What could be encoded in the skill:** Add operational-channel and phase objects; distinguish service programs, events and ingredient-driven turnover; require supplier identity beyond sourcing standards; and keep predecessor/former-address evidence temporally and organizationally isolated.
- **Progress:** Cumulative primary review is now 990 inspected: 851 accepted, 139 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 100

- **What happened:** The primary agent inspected and accepted ten more packages, bringing the semantic review to 1,000 records. The set included relocated and channel-shifting businesses, local and international chains, and several strong scratch-production records.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Prior-location fields stay historical; loyalty hidden menus are not cadence; product comparisons remain attributed; limited selection is neutral; shipment cadence differs from menu seasonality; virtual-brand tags do not negate licensed physical operation; off-site mix differs from onsite freezing; franchise processes remain brand scoped; sibling operators cannot share production evidence; and legal-name changes do not necessarily create new physical entities.
- **What could be encoded in the skill:** Add structured location-transition and channel-transition fields; distinguish supply cadence from menu cadence; preserve production stages by site; and formalize precedence between platform labels, municipal licenses and exact physical identity.
- **Progress:** Cumulative primary review is now 1,000 inspected: 861 accepted, 139 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 101

- **What happened:** The primary agent inspected ten more packages. Eight were accepted; El Sentin Zuliano was exhausted as a directory-only identity, and Liv Pure Acai was exhausted because its anonymous coordinate could not be assigned among distinct storefront/truck operations.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Sister and predecessor relationships do not transfer process; social mission is context; virtual-brand labels do not negate exact physical evidence; aggregate component labor differs from one cooking duration; directory categories do not establish operation; multiple active channels cannot be merged without coordinate linkage; broad menus are neutral; menu-version dates do not prove fixed cadence; and explicit rebranding does not preserve former chain membership.
- **What could be encoded in the skill:** Add multi-operation disambiguation for coordinate-only candidates; distinguish menu versioning from cadence; represent explicit rebrand lineage separately from current affiliation; and preserve component-labor versus cooking-duration semantics.
- **Progress:** Cumulative primary review is now 1,010 inspected: 869 accepted, 141 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 102

- **What happened:** The primary agent inspected ten more packages. Eight were accepted; coordinate-ambiguous Pretty Bird and documented-closed Atlantis Burgers Kearns were exhausted.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Service promotions are not seasonal turnover; customer supplier claims stay attributed; multi-branch facts cannot merge without linkage; family-group history stays source scoped; corporate process remains brand scoped; stray reviewer names do not create aliases; closure overrides historical menu detail; unofficial and unrelated brand sites must be excluded; scratch chains remain eligible for later scoring; and seasonal ingredients do not prove menu cadence.
- **What could be encoded in the skill:** Add automatic multi-location coordinate disambiguation; formalize authority precedence for self-disclaimed/unrelated sites; distinguish promotion, ingredient seasonality and menu turnover; and preserve chain novelty separately from scratch-production strength.
- **Progress:** Cumulative primary review is now 1,020 inspected: 877 accepted, 143 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 103

- **What happened:** The primary agent inspected and accepted ten more packages, including an active cocktail bar with unresolved cross-channel food availability and several unusually strong milling, bagel and nixtamal production records.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Conflicting live channels can remain unresolved without discarding identity; prior ownership stays attributed; current addresses need not imply a known relocation mechanism; adjacent venue ratings stay separate; menu breadth is neutral; daily flavor applies only to its slot; related ownership does not transfer process; incomplete rebrand lineage should not be invented; unsold-food donation is not menu turnover; and broad sides do not change production findings.
- **What could be encoded in the skill:** Add channel-specific food-availability states; exact-slot cadence allocation; adjacent-venue isolation; and explicit unknown-transition states for address/rebrand histories.
- **Progress:** Cumulative primary review is now 1,030 inspected: 887 accepted, 143 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 104

- **What happened:** The primary agent inspected ten more packages. Nine were accepted; generic, uniquely unresolvable “The Bar” was exhausted.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Fusion breadth is neutral; authoritative institutional evidence can establish operation without public ratings; seasonal sourcing does not prove cadence; shared-brand sibling pages cannot transfer process; organic labels do not identify producers; weekly-special claims need item archives; sourcing targets differ from suppliers; generic names need unique linkage; stale closure conflicts can lose to current official hours while remaining preserved; and undated specials boards do not establish cadence.
- **What could be encoded in the skill:** Add an institutional-source acceptance path; generic-name disambiguation gate; current-official-versus-stale-directory status precedence; and separate sourcing targets, ingredient labels, suppliers and menu cadence.
- **Progress:** Cumulative primary review is now 1,040 inspected: 896 accepted, 144 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 105

- **What happened:** The primary agent inspected and accepted ten more packages, including strong onsite bread/pretzel production records and several active but process-sparse restaurants.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Operational history differs from current process; early-close brunch is not closure; chain status is separate from production strength; announced changes are not completed turnover; lack of scratch evidence belongs in scoring; sparse fields do not negate active identity; weak closed-directory records can lose to stronger current channels; menu breadth is neutral; R&D tests are not guaranteed cadence; and generic specials do not prove rotation.
- **What could be encoded in the skill:** Add source-precedence rules for current merchant versus weak directory status; distinguish announced, tested and actually offered turnover; and make the separation between semantic acceptance, scratch strength and chain novelty explicit.
- **Progress:** Cumulative primary review is now 1,050 inspected: 906 accepted, 144 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 106

- **What happened:** The primary agent inspected and accepted ten more packages, including a sparsely documented licensed food truck, several beverage-first operations and a unique-name restaurant with a clearly erroneous ledger address.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Missing mobile schedules leave availability unresolved but do not erase identity; omitted closed days are not inferred; secret menus/events are not cadence; upstream brand processing differs from local extraction; music and beverage programming do not establish food; virtual labels do not prove commissaries; exact unique-name current sources can correct an address while preserving conflict; co-address businesses cannot share evidence; predecessor URL slugs are lineage; and beverage cadence remains scoped.
- **What could be encoded in the skill:** Add mobile-operation availability states; unique-name address-correction rules with conflict retention; upstream-versus-local production stages; and stronger co-address and beverage/food domain isolation.
- **Progress:** Cumulative primary review is now 1,060 inspected: 916 accepted, 144 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 107

- **What happened:** The primary agent inspected ten more packages. Eight were accepted; two coordinate-only restaurant names were exhausted because all resolved storefronts were outside the catchment and no candidate linkage survived.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Brand production remains distinct from branch production; distant/mobile identities cannot resolve an unlinked coordinate; food-hall neighbors cannot share evidence; composed drinks do not prove scratch components; malformed official hours can coexist with clearer sources; chain identity is independent of scratch strength; delivery-platform closure is not restaurant closure; predecessor domains are lineage; changing menu snapshots do not prove cadence; and distant same-name defects cannot attach to an unresolved candidate.
- **What could be encoded in the skill:** Add coordinate-to-mobile identity rules; explicit brand-versus-branch production allocation; platform-status-versus-business-status precedence; temporal-menu-state handling; and automatic geographic quarantine for same-name out-of-catchment results.
- **Progress:** Cumulative primary review is now 1,070 inspected: 924 accepted, 146 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 108

- **What happened:** The primary agent inspected ten more packages. Eight current identities were accepted; Bistró Carbón and Samurai Noodle were exhausted because multiple current closure signals lacked any verified reopening.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Broad scratch claims cannot be assigned to every component; broad cuisine is neutral; common group menus do not prove commissary production; current official/order channels can preserve an unresolved operation conflict; sparse records may still establish a merchant; temporary closure without reopening closes current fields; a lone stale closure can lose to several current sources; grab-and-go does not prove off-site production; sibling ownership does not transfer process; and stale corporate/license listings do not overcome several dated closure reports.
- **What could be encoded in the skill:** Add closure-evidence weighting by recency and channel multiplicity; distinguish broad scratch claims from component allocation; separate shared menus from shared production; and define when current merchant channels are sufficient to preserve rather than resolve a physical-operation conflict.
- **Progress:** Cumulative primary review is now 1,080 inspected: 932 accepted, 148 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 109

- **What happened:** The primary agent inspected and accepted ten more packages, ranging from process-sparse active merchants to cafes and grills with explicit handmade or house-made production evidence.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Broad menus are neutral; guest tabletop cooking is not kitchen scratch production; cat-lounge operations stay separate from food; predecessor/general chain menus cannot transfer wholesale through a rebrand; aggregated scratch text stays attributed; daily item availability is not turnover; a dated menu version is not cadence; sparse operation fields can still establish a current merchant; night-market branding does not imply rotating vendors; and assembly to order is distinct from scratch preparation.
- **What could be encoded in the skill:** Add explicit self-cook and assemble-to-order process categories; rebrand evidence-allocation rules; branding-versus-operating-format checks; and a formal distinction among availability, version evidence and recurring turnover.
- **Progress:** Cumulative primary review is now 1,090 inspected: 942 accepted, 148 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 110

- **What happened:** The primary agent inspected and accepted ten more packages, including strong Salvadoran scratch/bakery evidence, handmade-tortilla operations and several process-sparse but current cafes.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Related ownership cannot transfer process; reviewer process impressions remain attributed; community events are not menu turnover; sparse process evidence is for scoring; customer claims remain attributed beside operator evidence; food-truck and storefront labels may coexist; packaged ingredients stay explicit; other-location reviewer references do not prove group structure; menu size is neutral; and a single platform closure does not override multiple live merchant channels.
- **What could be encoded in the skill:** Add event-versus-menu cadence isolation; compatible multi-format identity states; packaged-component preservation; and a channel-weighted rule for platform-only closures.
- **Progress:** Cumulative primary review is now 1,100 inspected: 952 accepted, 148 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 111

- **What happened:** The primary agent inspected and accepted ten more packages, including four Sugar House Station stalls, a wine bar, a distillery and several restaurants with explicit house or off-site production evidence.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Branch hours cannot transfer; predecessor equipment does not transfer process; outside and neighbor food remain non-venue production; active non-food formats should survive until disqualification; historical ratings cannot transfer to a revived stall; hall-wide evidence is not stall evidence; a shared menu update does not prove every vendor changed; older off-site menus stay quarantined; same-company off-site production is not on-premises; and menu snapshots prove change rather than cadence.
- **What could be encoded in the skill:** Add formal shared-hall evidence scopes; revived-concept identity rules; active-nonrestaurant preservation through semantic review; and explicit onsite/same-company-offsite/third-party production locations.
- **Progress:** Cumulative primary review is now 1,110 inspected: 962 accepted, 148 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 112

- **What happened:** The primary agent inspected ten more packages. Nine were accepted; generic coordinate-only Coffee Corner was exhausted after no unique operating identity could be resolved.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Availability-driven change is not fixed cadence; fusion and menu breadth are neutral; missing mobile schedules do not erase established vendors; one rice-timing quote cannot establish the full sushi-rice process; generic labels require unique linkage; guest-chef menus are event scoped; omakase claims stay program scoped; customer reheating reports remain attributed; and customer scratch claims are not operator facts.
- **What could be encoded in the skill:** Add generic-map-label identity gates; explicit event/program evidence scopes; availability-driven versus scheduled cadence; and claim-authority typing for customer versus operator scratch/process wording.
- **Progress:** Cumulative primary review is now 1,120 inspected: 971 accepted, 149 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 113

- **What happened:** The primary agent inspected ten more packages. Nine current restaurants were accepted; Neptune’s Palace was exhausted as a repeatedly delayed investor concept with no operating footprint.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Remediated historical closures are not current; dated vacations with explicit reopening are not restaurant closure; licensing and current menus can establish operation despite sparse reviews; exact-name disambiguation matters; broad menus are neutral; customer ownership claims stay attributed; projected openings do not establish operation; entertainment and food evidence stay scoped; generic constant-addition wording is turnover mechanism; and shipped vacuum-sealed products must remain separate from restaurant-counter production.
- **What could be encoded in the skill:** Add never-opened/concept-only terminal states; explicit temporary-closure-with-reopening handling; historical-remediation status; and channelized production for restaurant counter versus shipped products.
- **Progress:** Cumulative primary review is now 1,130 inspected: 980 accepted, 150 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 114

- **What happened:** The primary agent inspected ten more packages. Eight were accepted; Smothered Burrito and Pepper Lunch were exhausted because current closure/rename states lacked verified operating successors or reopenings.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Bar format is a scoring fact; daily broth production is not menu turnover; weak promotional sourcing should be rejected; revived concepts cannot inherit predecessor evidence; same-brand locations do not prove shared production; old menus cannot transfer to an unverified successor; brand catalogs are not local availability; until-sold-out is not seasonal; classes do not prove production; and temporarily closed branches need reopening evidence.
- **What could be encoded in the skill:** Add rename/successor linkage gates; revived-predecessor evidence quarantine; catalog-versus-local availability; and a current-operation rule requiring reopening evidence after explicit temporary closure.
- **Progress:** Cumulative primary review is now 1,140 inspected: 988 accepted, 152 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 115

- **What happened:** The primary agent inspected ten more packages. Nine were accepted; historical HallPass vendor Blaze of Thunder was exhausted because it is absent from the current vendor roster and has no current merchant channel.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Corporate versus branch claims stay scoped; product ratings are not venue ratings; a platform closure can conflict with a current venue listing; food-hall rotation can prove departure; shared-kitchen facts are venue scoped; mixed local/in-house supply cannot be allocated without item evidence; menu breadth is neutral; event themes stay historical/location scoped; entertainment and food are separable; and customer production claims remain attributed.
- **What could be encoded in the skill:** Add current food-hall roster checks; product-versus-business rating typing; venue-roster precedence over platform-only closure; and mixed-source production allocation states.
- **Progress:** Cumulative primary review is now 1,150 inspected: 997 accepted, 153 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 116

- **What happened:** The primary agent inspected ten more packages. Eight were accepted; Black Rifle’s Salt Lake retail shop and Bob’s Brainfreeze were exhausted for unrefuted current closure and missing reopening evidence.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Select-location items cannot transfer; stock state is not cadence; stale corporate pages do not prove operation; assembly does not prove component production; guest trucks do not transfer process; grocery co-location does not weaken identity; themed events are not recurring cadence; hybrid limited-food formats survive to scoring; sparse process evidence can still be accepted; and seasonal businesses marked closed during season require continuity/reopening proof.
- **What could be encoded in the skill:** Add seasonal-business closure checks against current date; stale-corporate-page weighting; select-location menu allocation; and explicit component-versus-assembly production states.
- **Progress:** Cumulative primary review is now 1,160 inspected: 1,005 accepted, 155 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 117

- **What happened:** The primary agent inspected and accepted ten more packages, including several unusually strong bakery, fermentation, roasting and supplier records.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Branch process cannot transfer; related ownership cannot transfer; entertainment is not cadence; current official promotion can outweigh a directory closure while preserving conflict; ingredient formulas do not locate production; outside pastries remain outside; retail products stay separate from food; and supplier-made products are not café-made.
- **What could be encoded in the skill:** Add branch-level claim inheritance prohibition; stronger current-official-versus-directory conflict handling; ingredient-formulation versus production-location typing; and supplier-made component flags.
- **Progress:** Cumulative primary review is now 1,170 inspected: 1,015 accepted, 155 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 118

- **What happened:** The primary agent inspected and accepted ten more packages, including exceptionally detailed tasting-menu production and several current bars/fast-casual operations with sparse process evidence.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Sibling-branch process stays scoped; sourcing percentages remain claims; local collaboration does not identify suppliers; license history cannot be embellished; customer process claims remain attributed; business-name adjectives are not component evidence; cooking methods do not prove component fabrication; incubator origin is not current commissary evidence; format labels do not prove production; and co-located downstairs prices cannot transfer upstairs.
- **What could be encoded in the skill:** Add business-name claim suppression; current-versus-historical production-location states; license-history fact boundaries; and co-located vertical-venue evidence isolation.
- **Progress:** Cumulative primary review is now 1,180 inspected: 1,025 accepted, 155 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 119

- **What happened:** The primary agent inspected ten more packages. Nine were accepted; uncorroborated ledger-only Billy Bob Joe Chuck’s was exhausted after the complete identity sequence.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Sparse records can survive; customer scratch language remains attributed; address-only license snippets cannot establish identity; alias evolution does not merge branches; same-name branches and co-address businesses remain isolated; later current coverage can outweigh older directory closure while preserving conflict; former storefronts may become truck sites; customer refrigeration reports are not commissary findings; and frozen-food comparisons are not supplier confirmation.
- **What could be encoded in the skill:** Add address-only identity-evidence rejection; temporal closure-conflict ordering; storefront-to-mobile transition states; and explicit simile/comparison versus factual production-claim typing.
- **Progress:** Cumulative primary review is now 1,190 inspected: 1,034 accepted, 156 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 120

- **What happened:** The primary agent inspected ten more packages. Eight were accepted; stale/replaced Kava Bar and out-of-catchment-only Silver King Coffee were exhausted.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Seasonal décor is not menu cadence; adjacent units cannot merge; out-of-catchment same-name operation cannot resolve a candidate; sibling ratings stay branch scoped; local variation is not predictable cadence; soft-opening limitations are temporal; frozen serving is not premade production; brewery branding does not prove brewing location; national menus cannot transfer to a store café; and convenience-store format survives semantic review.
- **What could be encoded in the skill:** Add unit-level co-address disambiguation; geographic identity linkage gates; soft-opening evidence states; and brand-name-versus-location-production suppression.
- **Progress:** Cumulative primary review is now 1,200 inspected: 1,042 accepted, 158 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 121

- **What happened:** The primary agent inspected ten more packages. Seven were accepted; Dead Moon Coffee, Rocoto and El Timido were exhausted for unrefuted closure or non-corroborated/replaced identities.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Active no-food venues survive to disqualification; empty template sites do not refute current closure; current occupants cannot lend evidence to displaced candidates; menu breadth is neutral; delivery-platform closure alone is not business closure; co-addressed businesses stay separate; historical sibling-location process stays scoped; schedule changes are not menu turnover; inconsistent directory menus remain unresolved; and customer production claims stay attributed.
- **What could be encoded in the skill:** Add empty-template-site authority downgrades; current-occupant displacement states; explicit platform-closure insufficiency; and inconsistent-menu preservation rules.
- **Progress:** Cumulative primary review is now 1,210 inspected: 1,049 accepted, 161 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 122

- **What happened:** The primary agent inspected and accepted ten more packages, including a highly documented nixtamalization-focused caterer, several process-sparse merchants and two large/multi-location concepts.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Active no-food bars survive to disqualification; ghost-kitchen/catering format does not imply low scratch; sparse process evidence remains scoring evidence; cross-cuisine breadth is neutral; related concepts retain lineage without evidence transfer; exact merchant identity can survive sparse public fields; global-fusion breadth is neutral; chain scale is independent of production; conflicting candidate contacts stay unpromoted; and discounts/menu breadth are neutral.
- **What could be encoded in the skill:** Add exact-merchant sparse-evidence acceptance; production-kitchen/catering format typing; contact-conflict nonpromotion; and explicit scale-versus-production separation.
- **Progress:** Cumulative primary review is now 1,220 inspected: 1,059 accepted, 161 exhausted, 0 repair-routed.
### Scratch-dessert east-side revalidation — semantic phrase and geography join

- **Coverage:** Re-scanned every accepted/exhausted record in the current primary semantic review using dessert-production phrases, then joined hits back to Phase 4 identities/addresses and the tight east-side geography. Revalidated the existing dedicated, restaurant-program, limited-item, ambiguous, supplied-item and geographic-exclusion lists rather than repeating the prior shortlist.
- **Correction:** Added R-1777 City Edge Café at University of Utah Kahlert Village. Authoritative university sources explicitly state house-made gelato and freshly made pastries. The venue belongs in the campus/Foothill edge, but exact street address, current weekly hours, detailed methods and pastry production location are exhausted-unavailable. It is therefore confirmed for gelato production with hours unknown, not counted as open at 8 PM.
- **Result:** The tight subset now contains 12 dedicated/dessert-forward producers, four credible restaurant dessert programs, and two limited-item cases: 18 total confirmed scratch-dessert presences, or 16 under the stricter core/program count. The supported after-8 count remains nine, plus conditional Picnic and boundary/conflicting Hill's Kitchen.
- **Skill gaps:** Completeness needs a corpus-wide semantic phrase scan followed by address/geography joining, not name/category filtering. Institutional venues need authoritative-source identity without requiring public ratings, plus explicit `street_address_unknown`, `production_location_unknown`, and `hours_unknown` states. Never infer service hours from a host campus/building schedule.

## 2026-07-16 — Phase 5 primary semantic review batch 123

- **What happened:** The primary agent inspected ten more evidence packages. Nine were accepted; The Brick was exhausted because only a commercial-property tenant label survived and the candidate phone belongs to former Caffe Niche, with no verifiable current restaurant operation.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Sauce names do not prove production; current official/city evidence can outweigh historical platform closure while preserving conflict; recurring events are not ingredient-led cadence; purchased beans do not prove beverage fabrication; a single homemade condiment does not generalize; beverage production does not prove pastry production; property/tenant labels do not establish operating restaurants; seasonal item names prove change but not scratch; and discounts are not menu turnover.
- **What could be encoded in the skill:** Add property-tenant-label identity rejection; explicit category-bounded production inheritance; single-item claim non-generalization; and event/promotion-versus-menu-cadence typing.
- **Progress:** Cumulative primary review is now 1,230 inspected: 1,068 accepted, 162 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 124

- **What happened:** The primary agent inspected ten more packages. Eight were accepted; Which Wich was exhausted because no current Utah branch identity could be established, and Devil’s Gate was exhausted as an internal room within Eight Settlers rather than a separate restaurant.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Corporate evidence cannot instantiate an unidentified branch; broad menus and cross-cultural formats are neutral; protected-origin labels do not identify producers; a “special” label does not establish cadence; sparse but exact current identities survive; related distillery operation does not transfer food production; internal rooms cannot become separate merchants; localized chain process remains branch evidence; and cooking method does not prove component fabrication.
- **What could be encoded in the skill:** Add unidentified-brand-branch rejection; internal-room/subvenue deduplication; product-name-versus-venue collision handling; and explicit method-versus-component-fabrication typing.
- **Progress:** Cumulative primary review is now 1,240 inspected: 1,076 accepted, 164 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 125

- **What happened:** The primary agent inspected and accepted ten more packages, spanning a chain branch, a chef-driven seafood bar, a roaster, newly opened cafés and several process-sparse merchants.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Promotions and chain status are not semantic defects; sibling ownership does not transfer process; current customer activity can preserve operation despite an official-page omission; probable webpage typos remain literal; unclaimed directory hours are weak; occasional releases do not prove cadence; attached concepts stay separate; item-level meat process does not generalize; fusion format is neutral; and co-addressed merchant evidence cannot transfer.
- **What could be encoded in the skill:** Add official-location-page omission conflict handling; literal probable-typo preservation; attached-but-distinct concept isolation; and co-addressed platform-result contamination checks.
- **Progress:** Cumulative primary review is now 1,250 inspected: 1,086 accepted, 164 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 126

- **What happened:** The primary agent inspected and accepted ten more packages, including new chef-driven concepts, an omakase chain counter, sparse cafés, bars and an explicitly partner-supplied food program.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Shared-kitchen warnings do not prove commodity production; frozen retail products stay separate from restaurant preparation; broad handcrafted claims remain bounded; brand standardization does not erase local seasonal evidence; related concepts do not transfer process; reviewer production labels remain attributed; product identity does not prove fabrication; partner-supplied food is not venue production; predecessor menu evidence does not transfer; and beverage experimentation is not food cadence.
- **What could be encoded in the skill:** Add retail-versus-service product channel separation; partner-kitchen attribution states; predecessor-directory menu quarantine; and category-specific turnover boundaries.
- **Progress:** Cumulative primary review is now 1,260 inspected: 1,096 accepted, 164 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 127

- **What happened:** The primary agent inspected and accepted ten more packages, including a documented reopening, a chai-focused café, a bilingual regional-Chinese menu and a current successor-format merchant with historical predecessor evidence.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Soft openings and specials categories do not prove cadence; verified reopening can supersede closure without transferring old evidence; branch facts remain branch scoped; event sourcing is not ingredient sourcing; recurring category labels stay literal; conflicting official contact pages do not erase branch-specific merchant evidence; sibling menu reuse does not transfer process; seasonal ingredients are not menu turnover; and historical predecessor process remains quarantined absent continuity proof.
- **What could be encoded in the skill:** Add branch-versus-domain contact conflict states; reopening evidence boundaries; event-source exclusion from ingredient provenance; and predecessor-to-successor production continuity gates.
- **Progress:** Cumulative primary review is now 1,270 inspected: 1,106 accepted, 164 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 128

- **What happened:** The primary agent inspected ten more packages. Seven were accepted; Viva Mexico Carnitas was exhausted for an unresolved occupant conflict, Spritz for convergent current closure evidence, and Bon Fiyah for an approximate OSM nightclub label with no independently identifiable operation.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Conflicting address occupants cannot merge; another branch’s ratings and cadence remain scoped; external catering is not venue production; reviewer format descriptions do not erase an active identity; historical menus cannot prove current operation after closure; active beverage-only venues survive to disqualification; corporate origin marketing does not identify branch production; sparse coordinate linkage must remain qualified; approximate map labels are insufficient; and made-to-order cooking does not prove component fabrication.
- **What could be encoded in the skill:** Add licensed-occupant conflict handling; convergent closure-evidence thresholds; approximate-map-only terminal states; and branch roasting/production attribution rules.
- **Progress:** Cumulative primary review is now 1,280 inspected: 1,113 accepted, 167 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 129

- **What happened:** The primary agent inspected ten more packages. Nine were accepted; generic coordinate-only La Fondita was exhausted because multiple same-name Utah businesses remained and no coordinate, phone, domain or merchant channel resolved the candidate.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Third-party house-made claims remain qualified; product labels do not prove fabrication; drink variability does not transfer to full-menu cadence; sparse exact merchants survive; franchise scale does not negate local production; proposed co-address tenants do not prove displacement; explicit rebrands preserve continuity while suppliers stay external; multi-location status does not prove production; generic identities require unique linkage; and limited service days are not semantic defects.
- **What could be encoded in the skill:** Add proposed-tenant-versus-current-occupant handling; explicit rebrand continuity rules; generic-name coordinate resolution requirements; and third-party house-made claim localization states.
- **Progress:** Cumulative primary review is now 1,290 inspected: 1,122 accepted, 168 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 130

- **What happened:** The primary agent inspected and accepted ten more packages across franchise café, new döner shop, pop-up/incubator, poke chain, grocery kitchen, truck/takeaway kitchen, cart and legacy quick-service formats.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Brand social-impact claims are not branch process; supplied bread remains external; dated pop-up appearances are availability rather than menu rotation; multi-location scale is a scoring fact; grocery retail foods do not transfer to the restaurant; own-truck production can be same-operator off-site; customer illness/process claims remain attributed; fraudulent domains are not first-party; chain status is independent of local production; and quick-service format proves neither assembly nor scratch.
- **What could be encoded in the skill:** Add fraudulent-domain quarantine; same-operator truck/kitchen production channels; grocery-department evidence boundaries; and availability-calendar-versus-menu-turnover typing.
- **Progress:** Cumulative primary review is now 1,300 inspected: 1,132 accepted, 168 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 131

- **What happened:** The primary agent inspected ten more packages. Nine were accepted; Robintino’s was exhausted after a documented final service date and current closed status with no reopening.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Historical process remains date scoped; branch critic evidence cannot transfer; a single special is not cadence; bar format survives to scoring; related concepts and retail channels remain separate; sparse unique merchants survive; conflicting customer production claims stay attributed; cross-regional breadth is neutral; and missing process evidence is not negative evidence.
- **What could be encoded in the skill:** Add final-service-date closure handling; historical-process freshness states; conflicting customer-production-claim preservation; and retail-versus-dine-in product channel separation.
- **Progress:** Cumulative primary review is now 1,310 inspected: 1,141 accepted, 169 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 132

- **What happened:** The primary agent inspected and accepted ten more packages, including barbecue, fine dining, café, bar and an active performance venue without a recurring restaurant menu.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Conflicting tortilla claims remain attributed; broad menus are neutral; dated seasonal editions remain date scoped; entertainment turnover is not menu turnover; crawl-time closed labels are not closure; same-team concepts do not transfer; sparse unique merchants survive; assembly allegations remain attributed; item cadence does not generalize; private made-to-order menus are not public cadence; and active nonrestaurants survive to positive disqualification.
- **What could be encoded in the skill:** Add crawl-time status versus closure distinctions; event-menu versus recurring-menu states; attributed assembly-allegation handling; and private-menu versus public-menu cadence separation.
- **Progress:** Cumulative primary review is now 1,320 inspected: 1,151 accepted, 169 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 133

- **What happened:** The primary agent inspected ten more packages. Nine were accepted; Top of Main Brew Pub was exhausted after convergent current permanent-closure evidence despite stale published hours.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Bar-staple nouns do not prove frozen inputs; supplied bagels remain external; platform temporary closure can conflict with active official evidence; music turnover is not food cadence; stale hours do not rebut permanent closure; current reporting can outweigh a directory status while preserving conflict; sister businesses do not transfer process; retail sauce is a separate channel; spirit production does not transfer to food; and microwave allegations remain attributed.
- **What could be encoded in the skill:** Add stale-hours-versus-permanent-closure precedence; category-specific alcohol-versus-food production; retail-sauce channel boundaries; and current-reporting-versus-directory-status weighting.
- **Progress:** Cumulative primary review is now 1,330 inspected: 1,160 accepted, 170 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 134

- **What happened:** The primary agent inspected ten more packages. Nine were accepted; Teriyaki Styx was exhausted because only an OSM park feature survived and Lagoon’s current official food roster omitted it, with no corroborated current operation.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Legal bar status does not erase scratch work; historical process remains dated; guest cooking differs from fabrication; supplied branded goods remain external; location variation is not cadence; frozen labels stay item scoped; sibling process does not transfer; brewery-brand and restaurant ownership stay distinct; off-site distilling does not localize production; current official rosters matter for park stands; and park-calendar hours are not necessarily stand hours.
- **What could be encoded in the skill:** Add amusement-park current-roster checks; guest-cooking versus kitchen-fabrication states; item-specific frozen labels; and alcohol-production-site attribution rules.
- **Progress:** Cumulative primary review is now 1,340 inspected: 1,169 accepted, 171 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 135

- **What happened:** The primary agent inspected ten more packages. Nine were accepted; SodaBoba was exhausted after explicit current closure, an inactive merchant domain and no reopening evidence.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Current park rosters can establish sparse venues; names do not prove cuisine; historical pharmacy closure is not restaurant closure; multi-shop scale does not negate production; stability is not cadence; coffee production does not transfer to food; current branch evidence can outweigh brand-page omission; historical drinks do not prove current operation; founder death does not break documented continuity; and delivery-platform closure is not restaurant closure.
- **What could be encoded in the skill:** Add official-host-roster acceptance for sparse subvenues; historical-nonrestaurant-closure disambiguation; founder-death continuity handling; and brand-location-page omission conflict rules.
- **Progress:** Cumulative primary review is now 1,350 inspected: 1,178 accepted, 172 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 136

- **What happened:** The primary agent inspected ten more packages. Nine were accepted; New East Sea Restaurant on Redwood Road was exhausted because all branch-specific operation evidence was historical and different current businesses occupy the address, with no current merchant channel or reopening evidence.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Temporary online-order status is not closure; another branch's closure or health history does not transfer; current official seasonal resort presence can preserve a sparse quick-service venue; chain scale remains distinct from production; successor operation does not automatically inherit predecessor process; and broad cross-cuisine menus remain later scoring evidence rather than semantic rejection grounds.
- **What could be encoded in the skill:** Add an address-replacement rule for historical venues; require branch-specific transfer checks for closure and health evidence; distinguish successor identity continuity from production continuity; and formalize that active official seasonal listings can establish current operation even when item-level evidence is sparse.
- **Progress:** Cumulative primary review is now 1,360 inspected: 1,187 accepted, 173 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 137

- **What happened:** The primary agent inspected ten more packages; all ten were accepted. The batch preserved explicit in-house kimchi, crepe components, donut production, Belgian waffle/fry/sauce work, Mexican scratch testimony, Crown Burger prep and Poplar Street Pub production while retaining sparse active venues without inventing process.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Guest table cooking differs from kitchen fabrication; item-level frozen or reheated allegations stay item scoped; freshness and made-to-order wording do not prove component fabrication; daily production is not seasonal cadence; menu-version differences show change but not fixed rotation; customer-retold operator claims remain attributed; and publication-series titles are not venue specials.
- **What could be encoded in the skill:** Add publication-title-versus-venue-special safeguards; distinguish production freshness cadence from menu turnover; formalize customer-retold operator-claim provenance; and retain explicit named scratch components even when other individual items are alleged frozen or reheated.
- **Progress:** Cumulative primary review is now 1,370 inspected: 1,197 accepted, 173 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 138

- **What happened:** The primary agent inspected ten more packages. Eight were accepted; Trolley Wing Company Taylorsville was exhausted after convergent closure and former-tenant evidence, and Arella Pizzeria was exhausted because current closure/nonpayment signals had no reopening evidence while its resolved Bountiful address also contradicted the candidate's in-catchment annotation.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Historical homemade claims remain date scoped; undated seasonal-sounding items do not prove cadence; active first-party evidence can outweigh delivery closure; rumors alone do not establish closure; active non-food venues survive until positive disqualification; brand process remains brand scoped; and former-tenant/property evidence materially strengthens closure conclusions.
- **What could be encoded in the skill:** Add property-record/former-tenant evidence to closure precedence; require explicit geography reconciliation when resolved addresses contradict catchment annotations; distinguish closure rumors from convergent current closure evidence; and preserve active non-food candidates for the disqualification phase.
- **Progress:** Cumulative primary review is now 1,380 inspected: 1,205 accepted, 175 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 139

- **What happened:** The primary agent inspected ten more packages; all ten were accepted. This batch retained strong local scratch programs alongside national chains, an active bar and an uncooked take-and-bake store so format and novelty decisions remain reserved for Phase 6.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Item-specific facility-manufacturing labels do not generalize; another branch's closure does not transfer; unnamed local partners remain unnamed; brand production remains brand scoped; alcohol production differs from food production; take-and-bake format is a later disqualification fact; liquid eggs remain item/time scoped; and catchment conflicts require a geographic gate rather than semantic deletion.
- **What could be encoded in the skill:** Add an explicit geographic-reconciliation queue for resolved-address conflicts; formalize retention of active nonrestaurant/uncooked formats until Phase 6; and state that brand-level scratch claims and item-specific industrial-input evidence must each remain at their own scope.
- **Progress:** Cumulative primary review is now 1,390 inspected: 1,215 accepted, 175 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 140

- **What happened:** The primary agent inspected ten more packages. Nine were accepted; Iggy's Sports Grill in Sandy was exhausted after permanent-closure and replacement-tenant evidence with no reopening channel.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Frozen incoming dough can coexist with on-site baking; former-address closure does not transfer to a relocated business; first-party daily menu-change language is strong cadence evidence; commercial components remain bounded; nearby beer production does not transfer to food; similarly named unrelated businesses cannot share process; and exact current official identity outweighs an unrelated submitted domain.
- **What could be encoded in the skill:** Add compatible-process handling for frozen dough plus on-site baking; explicit relocated-business continuity rules; protection against same-name cross-business evidence transfer; and current canonical-domain resolution when submitted domains have changed ownership or purpose.
- **Progress:** Cumulative primary review is now 1,400 inspected: 1,224 accepted, 176 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 141

- **What happened:** The primary agent inspected ten more packages. Eight were accepted; Sushirito was exhausted because no exact entity could be resolved, and Charlotte's Italian was exhausted because only a historical label and qualified closure recollection survived while unrelated later businesses occupied the address.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** A newly operated in-bar kitchen does not inherit an older operator's process; reopened bars remain active despite sparse food evidence; spelling-similar businesses cannot be merged; outside food-truck work is not venue production; and current co-address businesses do not establish continuity with a historical candidate.
- **What could be encoded in the skill:** Add operator-transition boundaries for in-venue kitchens; formalize reopening evidence precedence; require collision checks for fuzzy-name matches; and explicitly separate outside-vendor food from host-venue production and scoring.
- **Progress:** Cumulative primary review is now 1,410 inspected: 1,232 accepted, 178 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 142

- **What happened:** The primary agent inspected ten more packages; all ten were accepted. The batch preserved several strong scratch programs and sparse but active cafés while queuing Park City geography conflicts for the catchment gate rather than conflating them with evidence quality.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Delivery-channel closure is not business closure; original-location ratings do not transfer to another branch; former branch closures do not transfer to the surviving original; retail and supplied inputs stay distinct from restaurant fabrication; review fuel descriptions do not override official wording; customer process assumptions are not facts; and category labels do not prove production.
- **What could be encoded in the skill:** Add explicit cross-branch rating isolation; distinguish retail/supplied ingredients from deli production; require source precedence for equipment/fuel descriptions; and maintain a dedicated catchment-reconciliation state independent of evidence acceptance.
- **Progress:** Cumulative primary review is now 1,420 inspected: 1,242 accepted, 178 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 143

- **What happened:** The primary agent inspected ten more packages; all ten were accepted. The batch included strong scratch bakeries, Mexican and Italian programs, sparse active venues, and Sara Thai Kitchen's explicitly temporary family-vacation closure with a dated reopening.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Production cadence differs from menu cadence; generic freshness does not identify maker/location; broad scratch claims do not prove unquoted techniques; harvest-linked gardens do not prove fixed turnover; commercial and scratch inputs can coexist; general homemade language stays general; and a dated closure with an explicit reopening is not permanent closure.
- **What could be encoded in the skill:** Add temporary-closure-with-reopening handling; separate production cadence from menu cadence; preserve broad scratch claims without decomposing them into unsupported component techniques; and allow mixed commercial/scratch programs with item-level evidence boundaries.
- **Progress:** Cumulative primary review is now 1,430 inspected: 1,252 accepted, 178 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 144

- **What happened:** The primary agent inspected ten more packages; all ten were accepted. The batch preserved strong scratch and seasonal programs, dated historical process evidence, sparse bars with no food kitchens, and active restaurants with limited public process detail.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Sister lineage does not transfer process; explicit packaged/no-food formats survive until Phase 6; historical sausage and Mexican production remains dated; outside-food recommendations are not host production; comparisons to frozen meals are not frozen-product facts; and apparent source typos stay preserved rather than silently repaired.
- **What could be encoded in the skill:** Add explicit no-kitchen semantic retention for later positive disqualification; require dated historical-process tagging; prevent outside-food attribution; distinguish comparisons from factual input claims; and define how to record obvious source-display errors without normalizing them.
- **Progress:** Cumulative primary review is now 1,440 inspected: 1,262 accepted, 178 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 145

- **What happened:** The primary agent inspected ten more packages; all ten were accepted. The batch preserved several substantial scratch programs, multi-location production splits, active bars with real kitchens, and sparse independent restaurants with only attributed production evidence.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Customer and third-party process claims stay attributed; literal cooking labels do not prove from-base components; another branch's service complaint does not transfer; item cadence remains item scoped; brewery partnerships are not onsite brewing; and post-purchase customer freezing is not venue production evidence.
- **What could be encoded in the skill:** Add clearer production-provenance labels for customer, directory, and first-party claims; formalize central-bakery versus store-finish splits; distinguish venue freezing from customer handling; and isolate branch-specific review defects by address.
- **Progress:** Cumulative primary review is now 1,450 inspected: 1,272 accepted, 178 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 146

- **What happened:** The primary agent inspected ten more packages; all ten were accepted. The batch ranged from sparse drive-through coffee and diners to current seafood chains and a Chinese restaurant explicitly selling handcrafted frozen potstickers.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Review freshness does not locate production; generated descriptions remain qualified; sensory descriptions do not prove fabrication; bagged seafood boil is not industrial boil-in-bag evidence; frozen and handcrafted can coexist for one item; spelling/address resolution must not pull evidence from a similarly named venue; and chain testimonials remain brand scoped.
- **What could be encoded in the skill:** Add a terminology guard separating seafood-in-a-serving-bag from industrial boil-in-bag; support compatible `handcrafted + frozen retail` states; formalize exact-phone/address entity resolution before fuzzy-name matching; and preserve brand testimonial scope.
- **Progress:** Cumulative primary review is now 1,460 inspected: 1,282 accepted, 178 exhausted, 0 repair-routed.

## 2026-07-16 — Phase 5 primary semantic review batch 147

- **What happened:** The primary agent inspected ten more packages; all ten were accepted. During drafting, six middle rows were accidentally populated from similarly positioned records in the preceding index block. The agent caught the mismatch before validation, reread `continuation-265.md`, `batch-593-evidence_batch_001.md`, and `batch-594-scratch_dessert_corridor.md`, and replaced every affected row with the correct candidate evidence.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Boxed and house-made tortilla items can coexist; amusement-park and no-kitchen bar formats remain for Phase 6; category labels do not prove production; relocation does not itself break current identity; review-topic tags do not establish menu items; literal frozen-dessert names are not industrial-input evidence; customer frozen/reheated allegations remain attributed; and temporary ordering unavailability is not closure.
- **What could be encoded in the skill:** Add a mandatory pre-append ID-to-source reconciliation check, ideally generated from the index; reject any semantic row whose candidate ID/name does not occur in its cited source file; and add explicit handling for review-topic tags, amusement-park venues, and frozen-format dessert names.
- **Progress:** Cumulative primary review is now 1,470 inspected: 1,292 accepted, 178 exhausted, 0 repair-routed.
### Scratch-dessert exhaustive classified-so-far refresh — indexed-return delta

- **Coverage:** Re-ran the dessert/process phrase scan across the current primary semantic-review checkpoint and joined every hit to its indexed Phase 4 return for exact address, production scope and hours. This phase performed retrieval/synthesis only; it did not change primary semantic acceptance or apply rubric scoring.
- **Correction:** Added R-1951 Tenet Sugarhouse, 1074 E 2100 S. Its official branch evidence says muffins and cookies are made entirely in house from scratch and baked fresh daily. It is a high-confidence dedicated/cafe producer but daytime-only. The corrected inventory is 13 dedicated/dessert-forward, four credible restaurant programs and two limited-item cases: 19 total scratch-dessert presences; strict core/program count 17.
- **Ambiguities/boundaries:** R-1799 Brabo Pizza in Millcreek has a dessert menu/category but no production evidence. R-1839 MiaoMiao Cafe has explicit handmade-dessert wording but its 200 East location is west of the documented tight corridor and remains a geographic-borderline exclusion. Crumbl Cottonwood has branch fresh-daily evidence but is Cottonwood Heights, outside this corridor. Institutional City Edge remains hours/address/production-location uncertain. The supported after-8 count remains nine.
- **Skill gaps:** Persist an explicit geographic rule with included/excluded edge coordinates; scan all indexed return production fields, not only semantic-summary category terms; distinguish branch-local evidence from brand claims; require `dessert menu only` versus `dessert production proven`; and make corpus delta audits rerunnable from the last reviewed/index row so newly accepted evidence cannot remain absent from derived inventories.
### Scratch-dessert inventory refresh — expanded classified checkpoint

- **Coverage:** Searched the current primary semantic-review checkpoint and every indexed durable return for dessert-production language, including restaurant records whose names/categories do not imply dessert. Joined candidates to exact address, current-status, hours and production-location evidence. This remained retrieval/synthesis only and did not alter primary semantic acceptance or rubric scoring.
- **Corrections:** Added five previously omitted classified records: R-2498 The Dodo (daily onsite bakery/dessert program), R-2659 Log Haven (daily house ice creams/sorbets and pastry chef), R-2519 Finn's Cafe (daily in-house-from-scratch breads and named pastries), R-2512 Nomad East (house-made biscuit/compote dessert only), and R-2535 Harbor (house-made salted-caramel ice cream only). Counts are now 14 dedicated/dessert-forward, six restaurant programs and four limited-item cases: 24 total; strict core/program count 20.
- **Hours/geography:** Dodo, Log Haven, Nomad East and Harbor are supported after 8; Finn's is daytime. Log Haven is explicitly retained as a Millcreek Canyon geographic edge. Harbor is Parleys/Sugar House edge; Nomad East is Harvard-Yale/15th-and-15th edge. The supported after-8 count rises to 13, plus conditional Picnic, boundary/conflicting Hill's Kitchen and unknown City Edge.
- **Skill gaps:** Derived inventories need automatic delta refresh as primary review advances; candidate-name/category filtering misses restaurant pastry programs; evidence must distinguish onsite bakery, restaurant pastry team, same-operator offsite production, and single named component; and geographic edges should be encoded as auditable include/exclude decisions rather than implicit judgment.

## 2026-07-16 — Phase 5 primary semantic review batch 148

- **What happened:** The primary agent inspected ten more packages. Six active, sufficiently resolved venues were accepted and four were exhausted: an OSM-only Lagoon snack stand, a sparse generic-name cafe, and two explicitly permanently closed bars. No repair routing was needed.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** An exact-address current platform cluster can establish a renamed/combined restaurant when a supplied domain points elsewhere; evidence from that conflicting domain cannot transfer. OSM-only amusement-park features omitted from the current official roster are not treated as current venues. Current permanent-closure evidence outweighs historical ratings/menu material absent reopening evidence. Food-truck reliance and a three-snack bar menu remain semantic facts for Phase 6. Venue closing hours do not extend kitchen hours, and seasonal patio hours do not prove menu turnover.
- **What could be encoded in the skill:** Add an explicit conflicting-domain entity rule keyed by exact address and phone; require current official-roster corroboration for amusement-park subvenues; formalize property-sale/license evidence in the permanent-closure sequence; separate venue hours from food-service hours; and keep food-truck-dependent/no-kitchen formats as positive later-stage disqualification facts.
- **Progress:** Cumulative primary review is now 1,480 inspected: 1,298 accepted, 182 exhausted, 0 repair-routed. 149 records remain in the 1,629-record population before quarantined geometries are reconciled.

## 2026-07-16 — Phase 5 primary semantic review batch 149

- **What happened:** The primary agent inspected ten more packages. Nine were accepted and the historical Golden China buffet was exhausted after current replacement/rebrand evidence and failure to recover a current operation. The batch included a low-novelty fast-food group, a private-event-only kitchen, mobile/catering operations, and two exact-address naming conflicts.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Low-novelty chains remain in the semantic corpus for later heuristics; a private-event kitchen is active but not a walk-in restaurant; dated process claims remain dated; branch-specific process does not transfer; mobile-stand and main-office evidence stays operationally scoped; exact-address co-brand evidence may preserve an unresolved dual identity; and a lone platform `CLOSED` flag does not establish permanent closure when later reviews and current-seeming hours survive.
- **What could be encoded in the skill:** Add explicit semantic states for private-event-only and mobile/catering formats; require dated-claim metadata; formalize co-brand/rename conflict retention; treat platform closure as weak unless corroborated by official/license/address evidence; and delay US low-novelty-chain elimination until the dedicated heuristic/scoring phase.
- **Progress:** Cumulative primary review is now 1,490 inspected: 1,307 accepted, 183 exhausted, 0 repair-routed. 139 records remain in the 1,629-record population before quarantined geometries are reconciled.

## 2026-07-16 — Phase 5 primary semantic review batch 150

- **What happened:** The primary agent inspected ten more packages. Nine current entities were accepted and historical Bill's Lounge was exhausted after business expiry and exact-address replacement by Main Street Grill. Active records included a deli/market, two no-kitchen nightlife venues, several restaurants, and a two-location Central American operation with incomplete public hours.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Packaged market goods can coexist with house sausage/sauce; generic bar-food claims remain weak but usable format evidence; successor-venue evidence cannot transfer backward; external food vendors and event BBQs are not host production; missing hours do not negate strong current official operation; summer popularity headings are not automatically menu rotation; and malformed ordering descriptions remain source defects rather than factual menu compositions.
- **What could be encoded in the skill:** Add explicit successor-venue non-transfer rules; separate external-vendor/event food from host kitchens; allow active semantic acceptance with exhausted hours when current operation is otherwise strong; distinguish seasonal marketing headings from ingredient/menu cadence; and require malformed-menu-text flags before extracting item facts.
- **Progress:** Cumulative primary review is now 1,500 inspected: 1,316 accepted, 184 exhausted, 0 repair-routed. 129 records remain in the 1,629-record population before quarantined geometries are reconciled.

## 2026-07-16 — Phase 5 primary semantic review batch 151

- **What happened:** The primary agent inspected ten more packages; all ten were accepted. The batch included two fast-food burger shops, two chef-led restaurants, an ambiguously temporarily closed Korean-fusion venue, a family pupusa restaurant, a seasonal water-park concession and a small coffee drive-through.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Dated critic production remains attributed; false official-domain matches must be excluded; recurring daypart menus are not seasonality; one sold-out report is not cadence; temporary-status conflicts are not permanent closure; self-declared unofficial sites cannot become first-party evidence; park-level ratings cannot transfer to a concession; and general craft/freshness language does not prove individual component fabrication.
- **What could be encoded in the skill:** Add automated domain-collision and self-disclaimer checks; distinguish recurring daypart from menu turnover; require corroboration before temporary closure becomes permanent; prevent parent-venue ratings from flowing to concessions; and label production assertions by operator, critic, customer and directory provenance.
- **Progress:** Cumulative primary review is now 1,510 inspected: 1,326 accepted, 184 exhausted, 0 repair-routed. 119 records remain in the 1,629-record population before quarantined geometries are reconciled.

## 2026-07-17 — Phase 5 primary semantic review batch 152

- **What happened:** The primary agent inspected ten more packages; all ten were accepted. The batch included three small independent counter-service venues, two burger/diner operations, a pizzeria, two branches of the same drive-through coffee chain, a private-home tasting menu and a discovery lead resolved through a spelling-error/dish fingerprint.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Customer frozen/packaged/held-food claims remain attributed; current operation supersedes historical temporary closure; menu versions do not establish cadence; authentic gelato language does not locate production; same-chain branch reviews do not transfer; private-home dining can be semantically active while retaining format/confidence concerns; and a misspelled discovery identity can be resolved by an exact unique menu-item fingerprint plus address evidence.
- **What could be encoded in the skill:** Add unique-dish fingerprinting to entity resolution; enforce branch-isolated reviews; distinguish authenticity claims from production location; formalize private-home dining as a separate later-stage format; and preserve customer production allegations without converting them into operator facts.
- **Progress:** Cumulative primary review is now 1,520 inspected: 1,336 accepted, 184 exhausted, 0 repair-routed. 109 records remain in the 1,629-record population before quarantined geometries are reconciled.

## 2026-07-17 — Phase 5 primary semantic review batch 153

- **What happened:** The primary agent inspected ten more packages. Nine current venues were accepted and Xiao Bao Bao's Milk Block location was exhausted after an explicit May 2026 closure with no reopening. The accepted set included a newly reopened deli, delivery-only sparse evidence, strong scratch taqueria and Veracruz programs, a Georgian restaurant, a downtown express branch and a partner-kitchen bar.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Pre-sale practices do not transfer to new ownership; delivery-platform identity can be sufficient when exact; daily production is not menu turnover; parent-brand production/rotation does not automatically localize to a branch; partner-kitchen food is not host production; and explicit location closure remains location scoped while sibling evidence is excluded.
- **What could be encoded in the skill:** Add ownership-era boundaries, minimum exactness rules for merchant-platform-only identities, branch-localization checks for brand claims, partner-kitchen production ownership, and location-scoped closure handling.
- **Progress:** Cumulative primary review is now 1,530 inspected: 1,345 accepted, 185 exhausted, 0 repair-routed. 99 records remain in the 1,629-record population before quarantined geometries are reconciled.

## 2026-07-17 — Phase 5 primary semantic review batch 154

- **What happened:** The primary agent inspected ten more packages. Seven were accepted; Copal and PastaNito were exhausted as out-of-state geographic collisions, while Makam's/Munchkart was exhausted after corroborated closed/inactive status. The accepted records included a mobile Swahili caterer whose storefront closed but operation continued, a sparse Oromo listing, and several substantial current restaurant corpora.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Distinctive process quotations cannot overcome wrong-state identity; franchise expansion language does not create an unlisted branch; corroborated platform closure without current continuity is exhaustion; a closed storefront does not erase a documented current mobile operation; and sparse exact directory evidence can survive while retaining low evidence confidence.
- **What could be encoded in the skill:** Add mandatory state/address checks before importing distinctive process evidence; forbid inferred franchise locations; separate entity closure from channel/storefront closure; model mobile continuation explicitly; and expose a confidence dimension independent of semantic acceptance.
- **Progress:** Cumulative primary review is now 1,540 inspected: 1,352 accepted, 188 exhausted, 0 repair-routed. 89 records remain in the 1,629-record population before quarantined geometries are reconciled.

## 2026-07-17 — Phase 5 primary semantic review batch 155

- **What happened:** The primary agent inspected ten more packages. Eight were accepted; Sasa Kitchen was exhausted after corroborated closure, and Midnimo was exhausted because its only unofficial corpus contained cuisine-incompatible review/menu material and no verified restaurant evidence. The accepted set included sparse but exact vegan and Somali venues, a seafood restaurant, and several conventional active restaurants.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Stale official hours do not outweigh corroborated closure; cuisine-incompatible SEO review text cannot establish a menu; a self-declared unofficial site remains non-first-party; parent/out-of-state menu evidence cannot fill a sparse local venue; current out-of-stock snapshots are not rotation; and daily ingredient arrival is sourcing cadence rather than menu cadence.
- **What could be encoded in the skill:** Add cuisine-compatibility checks for scraped reviews; rank stale official hours below current closure corroboration; separate availability, sourcing and menu cadence; and require local-branch evidence before borrowing from a same-name out-of-state venue.
- **Progress:** Cumulative primary review is now 1,550 inspected: 1,360 accepted, 190 exhausted, 0 repair-routed. 79 records remain in the 1,629-record population before quarantined geometries are reconciled.

## 2026-07-17 — Phase 5 primary semantic review batch 156

- **What happened:** The primary agent inspected ten more packages. Eight were accepted; Gradys was exhausted because a conditional license never developed into verifiable operation, and Frankie & Essl's was exhausted after a permanent-closure announcement and inactive ordering with no reopening evidence. The batch also entered the post-tail early-ID reconciliation set without assuming those records had already been reviewed.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** A conditional license is not proof of opening; an inactive ordering page plus a reported permanent-closure announcement can exhaust current operation; partner-bakery output does not automatically belong to a restaurant; shared-kitchen claims remain vendor scoped; inn ratings do not transfer to its café; image alt text is weak process evidence; and sister-property linkage does not establish shared production.
- **What could be encoded in the skill:** Add opening-proof gates for conditional licenses; require explicit partner/shared-kitchen production ownership; separate parent-property ratings; downgrade alt-text process claims; and ensure durable-return order, rather than record-number order, drives completeness.
- **Progress:** Cumulative primary review is now 1,560 inspected: 1,368 accepted, 192 exhausted, 0 repair-routed. 69 records remain in the 1,629-record population before quarantined geometries are reconciled.

## 2026-07-17 — Phase 5 primary semantic review batch 157

- **What happened:** The primary agent inspected ten more packages. Six active venues were accepted; Chez Betty, The Big Easy, Mountain Grill and FishOn Bistro were exhausted due to permanent historic closure, OSM-only noncorroboration, property-wide closure without restaurant continuity, and unresolved current closure without reopening evidence respectively.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Legacy rendered hours cannot revive a closed business; hotel/property reopening does not prove restaurant continuity; conflicting directory hours are weaker than multiple current closure signals plus inactive official content; coordinate records support identity lineage but not a current address; and historical production/supplier claims remain dated.
- **What could be encoded in the skill:** Add property-versus-restaurant continuity checks; rank active first-party content above passive directory hours; require reopening evidence for unresolved temporary-closure cases; and enforce temporal tagging for all process and supplier claims.
- **Progress:** Cumulative primary review is now 1,570 inspected: 1,374 accepted, 196 exhausted, 0 repair-routed. 59 records remain in the 1,629-record population before quarantined geometries are reconciled.

## 2026-07-17 — Phase 5 primary semantic review batch 158

- **What happened:** The primary agent inspected ten more packages. Seven were accepted; Java Bytes and Junior's Tavern were exhausted as OSM-only identities, and historical Taste of Punjab was exhausted after exact-address replacement by Bhutan House. The batch also preserved separation between adjacent/co-located concepts and between restaurant, retailer and delivery-channel status.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Delivery-channel closure is not entity closure; exact-address successors do not inherit predecessors; department-store/hotel ratings do not transfer to subvenues; historical aliases remain location scoped; accommodation for a regular is not public menu cadence; and adjacent concepts cannot share production evidence without an explicit link.
- **What could be encoded in the skill:** Add channel-versus-entity status labels; automate exact-address predecessor/successor isolation; forbid parent-property rating transfer; and require explicit co-located kitchen relationships before evidence sharing.
- **Progress:** Cumulative primary review is now 1,580 inspected: 1,381 accepted, 199 exhausted, 0 repair-routed. 49 records remain in the 1,629-record population before quarantined geometries are reconciled.

## 2026-07-17 — Phase 5 primary semantic review batch 159

- **What happened:** The primary agent inspected the next ten unique IDs from the authoritative set difference; all ten were accepted. This batch contained a no-kitchen pub, substantial scratch programs, multi-location brands, a reopened drive-in, and a combined restaurant identity with historical standalone evidence.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Neighbor/third-party food is not host production; brand process does not silently become branch-detail; literal source typos remain visible; temporary closure/reopening is a timeline; quick-casual chain status is delayed to later novelty treatment; `our own` does not document full method; and historical menu-version claims remain version scoped after a combined identity transition.
- **What could be encoded in the skill:** Add unique-ID set-difference batching as the required tail procedure; formalize host-versus-neighbor food ownership; add brand-to-branch scope labels; and require menu-version timestamps across identity mergers.
- **Progress:** Cumulative primary review is now 1,590 inspected: 1,391 accepted, 199 exhausted, 0 repair-routed. 39 unique records remain in the 1,629-record population before quarantined geometries are reconciled.
### Scratch-dessert focused east-side refresh — 1,590-record checkpoint

- **Coverage:** Re-audited the current 1,590-record primary semantic-review checkpoint and indexed returns for dessert production regardless of restaurant name/category. Joined new hits to address, operator/current status, production scope and supported closing time. Retrieval/synthesis only; no semantic acceptance or rubric scoring was made or changed.
- **Corrections:** Added R-0001 Café 140B in the Avenues for direct official housemade-English-scone evidence; R-2549 VENETO at 370 E 900 S for a first-party homemade fruit tart, kept limited to that item; and R-2643 Mad Greek in Millcreek for a Restaurantji-preserved “Homemade Pudding” label, marked medium-confidence/third-party rather than a broad program.
- **Result:** Inventory now contains 15 dedicated/dessert-forward producers, six credible restaurant programs, and six limited/source-qualified items: 27 total, with a stricter core/program count of 21. Supported after-8 count is 15; Café 140B is daytime, VENETO is after 8 Tue–Sun, and Mad Greek after 8 Mon–Sat.
- **Skill gaps:** Track the primary checkpoint/version in every derived inventory; scan item-level production phrases across all cuisines; distinguish first-party item claims from platform-preserved menu labels; keep B&B/hotel/institution subvenue evidence isolated; and retain consistent same-street geography decisions for adjacent edge venues.

## 2026-07-17 — Phase 5 primary semantic review batch 160

- **What happened:** The primary agent inspected the next ten unique IDs from the authoritative set difference. Six active/currently supported venues were accepted. Spice Bistro, Dragon Isle, Salt City Burger and Main Street Pizza & Noodle were exhausted because current identity continuity could not be established or permanent/current closure evidence controlled.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Historical coordinates do not override a verified relocation; a license under a legacy name does not prove a restaurant still operates; an explicitly temporary accident/remodeling closure is not permanent closure; stale platform hours cannot revive a closed venue; a directory temporary-closure label does not override strong current first-party operation; and historical scratch claims remain dated after closure.
- **What could be encoded in the skill:** Add explicit relocation lineage fields; require operational corroboration for legacy government licenses; distinguish accident/remodeling, seasonal, multweek and permanent closure; weight current transactional first-party signals above passive directory status; and automatically temporal-scope production evidence when a venue closes.
- **Progress:** Cumulative primary review is now 1,600 inspected: 1,397 accepted, 203 exhausted, 0 repair-routed. The authoritative population set difference must be recomputed before stating the next remaining count.

## 2026-07-17 — Phase 5 primary semantic review batch 161

- **What happened:** The primary agent inspected the next ten unique IDs from the authoritative set difference; all ten had sufficient current identity and field evidence for acceptance. The batch included fine dining, local restaurant groups, national/local multi-location fast-casual brands, a light-food entertainment venue and food-serving pubs.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Candidate typos remain aliases; legacy URLs do not transfer predecessor evidence; brand-wide process is distinct from outlet-specific process; current transactional evidence preserves active branches; national/local chain and fast-casual status belongs to later novelty treatment; entertainment rotation is not food rotation; and pub/bar/light-food formats remain semantically reviewable until Phase 6.
- **What could be encoded in the skill:** Add explicit alias-typo normalization, predecessor-URL detection, brand-versus-branch process fields, transactional branch-status weighting, a delayed novelty-chain gate, and separate entertainment/event versus food-menu turnover types.
- **Progress:** Cumulative primary review is now 1,610 inspected: 1,407 accepted, 203 exhausted, 0 repair-routed. The authoritative population set difference must be recomputed before stating the next remaining count.

## 2026-07-17 — Phase 5 primary semantic review batch 162

- **What happened:** The primary agent inspected ten more unique records. Eight were accepted. Café Trio Cottonwood was exhausted after a documented 2019 permanent closure, and Copper King was exhausted after the exact address transitioned to Copper Miner Saloon without evidence continuity.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Stale government license rows do not override documented permanent closure; active sibling locations do not revive a closed outlet; same-address/same-phone rebranding can preserve an entity thread while still leaving legal/date details unknown; successor tenants do not inherit predecessor evidence; customer made-in-house claims remain attributed; and delivery-channel closure is branch scoped.
- **What could be encoded in the skill:** Add license-staleness checks against transactional/current operator evidence; enforce sibling-outlet quarantine; model same-phone/address alias transitions separately from successor-tenancy transitions; and require explicit evidence inheritance rules across rebrands.
- **Progress:** Cumulative primary review is now 1,620 inspected: 1,415 accepted, 205 exhausted, 0 repair-routed. The authoritative population set difference must be recomputed before stating the final population batch.

## 2026-07-17 — Phase 5 primary semantic review batch 163

- **What happened:** The primary agent inspected the final nine unique IDs in the 1,629-record preflight population; all nine had sufficient current identity and evidence for acceptance. This completes primary semantic inspection of the structured population, pending reconciliation of the 15 quarantined unnamed geometries and construction of the Phase 5 evidence ledger.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Relocation with explicit brand continuity is not closure; company-wide process remains distinct from branch-local execution; related-family businesses do not share evidence; institutional commissary disclosures must be retained without guessing item mappings; historical and seasonal closures remain time scoped; and customer handmade/fresh-baked wording remains attributed.
- **What could be encoded in the skill:** Add relocation lineage objects; company/branch/commissary production-location fields; explicit institutional commissary item mapping; time-scoped closure-state resolution; and customer-versus-operator process provenance at the claim level.
- **Progress:** All 1,629 structured records have primary decisions and the authoritative ID set difference is zero. Exact state totals are deferred to the row-count integrity pass because the running prose counters require reconciliation.

## 2026-07-17 — Phase 5 unnamed-geometry quarantine reconciliation

- **What happened:** The primary agent inspected all five unnamed-identity repair batches and reconciled the 15 unresolved geometries individually. Each has a demonstrated exact-coordinate/OSM/address/official-locator search trail but lacks enough identity proof to attach a restaurant's evidence; all 15 were therefore recorded as legitimately evidence-exhausted-unavailable rather than silently dropped.
- **Corrections required from the user:** None. No scoring, novelty filtering, ranking, or disqualification occurred.
- **What required interpretation:** Nearby businesses cannot be assigned by category/proximity; co-address parcels require suite/footprint proof; a leading identity alternative is not a resolved identity; multiple historical tenants require chronology plus geometry continuity; and an unidentified geometry is a terminal identity-exhaustion state only after its search trail is explicit.
- **What could be encoded in the skill:** Require OSM history/changeset retrieval and reverse-geocoded parcel/suite checks during initial discovery; store geometry-to-unit confidence; distinguish `leading alternative` from `resolved identity`; and include unresolved-geometry terminal rows in the Phase 5 ledger rather than outside the reviewed universe.
- **Progress:** Combined Phase 5 universe is 1,644 inspected. The evidence ledger and completion gate remain before Phase 6.

## 2026-07-17 — Phase 5 ledger build and arithmetic correction

- **What happened:** Generated the mandatory `05-evidence-ledger.md` from every semantically inspected structured return, its worker/provenance mapping, primary acceptance note and all 15 identity-exhausted geometry records. The ledger's ID integrity check found 1,644 unique expected rows with zero missing, unexpected or duplicate IDs.
- **Correction:** Direct counting of the terminal-state rows gives 1,425 evidence-accepted and 219 evidence-exhausted-unavailable. Earlier running prose totals carried a one-record accepted/exhausted arithmetic drift beginning in an early batch; this was a counter error only, not a venue-state change. The final review summary and ledger now use the authoritative row count.
- **Corrections required from the user:** None.
- **What required interpretation:** A generated ledger may incorporate complete raw records by explicit source reference when each referenced record remains immutable, structurally clear and semantically inspected; running summaries are not authoritative when they disagree with unique-ID/state rows.
- **What could be encoded in the skill:** Require cumulative state totals to be computed from unique candidate rows after every batch, prohibit hand-carried counters, and ship a ledger builder/integrity checker that fails on missing, unexpected, duplicate or state-sum mismatches.
- **Progress:** Phase 5 ledger universe: 1,644 unique records; 1,425 accepted; 219 exhausted; zero missing, unexpected or duplicate IDs.

## 2026-07-17 — Phase 5 completion gate

- **What happened:** Evaluated every printed Phase 5 gate item against the current artifacts. All items passed. The structured preflight has 1,629 clear records and zero defects; the combined evidence ledger has 1,644 unique terminal rows with zero missing, unexpected or duplicate IDs; the repair log now includes the complete semantic-review and quarantine closeout.
- **Corrections required from the user:** None.
- **What required interpretation:** Bakery-only gate items are explicitly not applicable to a restaurant run; a fresh-worker canonical-prompt requirement is satisfied vacuously because all Phase 5 repairs used the original workers; and an unresolved geometry can be terminal only as identity-exhausted, never as evidence for its leading nearby alternative.
- **What could be encoded in the skill:** Provide a category-aware gate renderer with explicit N/A states, automatically reconcile ledger IDs and state counts, and require final repair-log closeout before the manifest can move to `phase-5-complete`.
- **Progress:** Phase 5 passed. Phase 6 restaurant scoring and classification is next.

## 2026-07-17 — Phase 6 primary scoring batch 001

- **What happened:** The primary orchestrator applied the restaurant scoring rubric to the first 20 evidence-accepted records. Four had enough positive production evidence for S/I estimates, two were positively disqualified on current closure/unsupported-operation evidence, and 14 remained explicitly score-unresolved rather than receiving artificially low values.
- **Corrections required from the user:** None. The user's standing correction was enforced: no fast-food, café, pub or multi-location format was treated as a low-novelty exclusion.
- **What required interpretation:** Evidence acceptance means the research record is complete, not that the venue is scoreable; exhausted process evidence cannot become a zero; turnover without production does not clear the scratch floor; historical production does not score a current venue; and recommendation percentages are not star ratings.
- **What could be encoded in the skill:** Add `score-unresolved` as an explicit Phase 6 terminal route, require numeric scores only when positive evidence spans enough criteria, and distinguish evidence completeness from scoreability in the decision artifact schema.
- **Progress:** 20 of 1,644 Phase 6 records decided: four scoreable, two positive DQ, 14 score-unresolved.

## 2026-07-17 — Phase 6 evidence-exhausted terminal decision batch

- **What happened:** The primary orchestrator assigned the explicit `evidence-exhausted-no-score` decision to all 219 Phase 5 exhausted records. Each decision is individually listed in `06-decisions.md` with its accepted evidence record and primary exhaustion reason.
- **Corrections required from the user:** None.
- **What required interpretation:** Evidence exhaustion is a terminal research outcome but not a low scratch score, DQ, or low-novelty inference; unresolved identities and closed historical records can both be excluded from numeric ranking without pretending their production score is zero.
- **What could be encoded in the skill:** Make `evidence-exhausted-no-score` a first-class Phase 6 disposition and allow a mechanically generated decision table only when every row retains an individual accepted-evidence citation and primary reason.
- **Progress:** 239 of 1,644 Phase 6 records now have primary decisions: 20 venue-specific decisions plus 219 individually cited evidence-exhausted/no-score decisions.

## 2026-07-17 — Phase 6 primary scoring batch 002

- **What happened:** The primary orchestrator decided 30 more accepted records: six scoreable, three positively disqualified, three reversibly excluded under the user-authorized U.S. standardized-chain familiarity screen, and 18 score-unresolved.
- **Corrections required from the user:** None. Kneaders, J Dawg's, CupBop and Apollo Burger were not excluded merely for being chains or fast/counter service; only records with positive standardized-familiarity evidence received the preference disposition.
- **What required interpretation:** Business ratings are not restaurant ratings; company-group off-site baking is not on-premises production; a menu update date is not recurring turnover; guest/table cooking is not component production; a single homemade item cannot support restaurant-wide S; and strong scratch markers can be preserved without fabricating a complete score.
- **What could be encoded in the skill:** Separate reversible user-preference exclusions from rubric DQs, require an explicit standardized-familiarity fact for the former, and support a `scratch marker retained / numeric score unresolved` state.
- **Progress:** 269 of 1,644 Phase 6 records decided.

## 2026-07-17 — Phase 6 primary scoring batch 003

- **What happened:** The primary orchestrator decided 40 more accepted records: five scoreable, one positively closed, and 34 score-unresolved. Nine unresolved venues retain explicit strong scratch markers so they remain visible for coverage/spot-check handling rather than disappearing.
- **Corrections required from the user:** None. No chain, buffet, bar, hotel, fast-casual or cuisine label was used as a verdict.
- **What required interpretation:** Buffet warming equipment does not prove assembly; a daily-changing single item is narrower than menu rotation; generic scratch headlines need component detail; user-attributed process remains user evidence; seasonal operation is not seasonal menu change; and strong isolated production markers can be retained without inventing complete numeric axes.
- **What could be encoded in the skill:** Add a structured scratch-marker register alongside numeric decisions, distinguish item-level turnover from menu-level volatility, and require production breadth plus positive volatility evidence before a complete S estimate.
- **Progress:** 309 of 1,644 Phase 6 records decided.

## 2026-07-17 — Phase 6 primary scoring batch 004

- **What happened:** The primary orchestrator decided 50 more accepted records: 14 scoreable, two positively disqualified, and 34 score-unresolved; eight unresolved records retain strong scratch markers.
- **Corrections required from the user:** None. Aubergine's multi-state scale did not trigger exclusion because its scratch/in-house evidence is substantive; hotel, buffet, coffee, bar and takeout formats remained neutral unless positive food-ineligibility evidence existed.
- **What required interpretation:** Company-wide scratch evidence can support a cautious branch score without proving branch-local execution; beer production is not food production; seasonal drink rotation is not food turnover; customer frozen/premade allegations cannot create DQ; and a calibrated scratch venue may still fail the documented rating floor.
- **What could be encoded in the skill:** Add calibrated-anchor lookup by candidate identity, explicit company-versus-branch confidence penalties, and a positive `food-ineligible` taxonomy for beer-only and wet-led external-food venues.
- **Progress:** 359 of 1,644 Phase 6 records decided.

## 2026-07-17 — Phase 6 primary scoring batch 005

- **What happened:** The primary orchestrator decided 50 more accepted records: six scoreable, one positive food-ineligibility DQ, four reversible standardized-chain preference exclusions, and 39 score-unresolved; 12 unresolved venues retain explicit scratch markers.
- **Corrections required from the user:** None. Regional coffee, local pizza, concessions, bakeries, a fermented-dough franchise and food-court businesses were not excluded by format or scale. The preference screen was limited to positively documented standardized U.S. formats.
- **What required interpretation:** Partner-creamery production is off-site; company roasting is not branch food production; historical scratch evidence cannot be assumed current; recurring daily/monthly specials can support turnover only when food-specific; and commissary uncertainty blocks an on-site score without proving assembly.
- **What could be encoded in the skill:** Add production-location values (`on_site`, `partner_off_site`, `company_commissary_unknown`) directly to scoring inputs and make reversible preference exclusions auditable separately from DQ.
- **Progress:** 409 of 1,644 Phase 6 records decided.

## 2026-07-17 — Phase 6 primary scoring batch 006

- **What happened:** The primary orchestrator decided 60 more accepted records: eight scoreable, three positive DQs, five reversible standardized-chain preference exclusions, and 44 score-unresolved; ten unresolved venues retain scratch markers.
- **Corrections required from the user:** None. Village Baker scored very highly despite franchise facts because on-site milling and daily scratch production outweigh format; no regional/local multi-location operation was excluded solely for scale.
- **What required interpretation:** On-site milling is a top-tier production signal; off-site food vendors and beer production cannot be counted as host food production; daily production is not menu turnover; sale listings are not formal closure; and company scratch claims support cautious branch scoring with a provenance confidence penalty.
- **What could be encoded in the skill:** Add high-weight milling/fermentation/live-fire marker extraction, explicit current-operation versus sale/seasonal closure states, and automatic separation of host, vendor and commissary food production.
- **Progress:** 469 of 1,644 Phase 6 records decided.

## 2026-07-17 — Phase 6 primary scoring batch 007

- **What happened:** The primary orchestrator decided 70 more accepted records: 11 scoreable, one positive off-site-food DQ, one reversible standardized-chain preference exclusion, and 57 score-unresolved; 29 unresolved records retain scratch markers.
- **Corrections required from the user:** None. Village Baker District scored near the top despite franchise facts because its branch-local milling/daily scratch evidence is exceptional; 85°C, Iceberg, Cubby's and other multi-location businesses were not excluded by scale.
- **What required interpretation:** Branch-local proof can sharply differentiate siblings under the same brand; wholesale frozen production does not prove retail reheating; customer holiday items do not establish cadence; partner/vendor off-site production fails on-site eligibility only when the boundary is explicit; and historical/operator-group evidence must remain scoped.
- **What could be encoded in the skill:** Add sibling-branch evidence inheritance controls, explicit retail-versus-wholesale production channels, and automatic score anchoring for calibration-set identities.
- **Progress:** 539 of 1,644 Phase 6 records decided.

## 2026-07-17 — Phase 6 primary scoring batch 008

- **What happened:** The primary orchestrator decided 40 more accepted records: six scoreable and 34 score-unresolved; 17 unresolved records retain explicitly scoped scratch, sourcing, historical or current-operation markers. The tupelo and Fuego identities were anchored to the rubric calibration set, while Plates and Palates, Roots Cafe, Straw Market and The Pie received criterion-level estimates from accepted production-plus-cadence evidence.
- **Corrections required from the user:** None. Mo' Bettahs, Cupbop, cafés, bars, a juice shop and multi-location pizza/bakery operators were not excluded by format or scale. Cupbop remained unresolved because this record lacks branch evidence; it was not converted into a familiarity exclusion merely because the brand is recognizable.
- **What required interpretation:** Historical scratch language cannot score a current branch; a sale listing is not closure; beverage rotation is not food turnover; named coffee origins are not food sourcing; an attached market is not automatically a restaurant supplier; a fraudulent site must be rejected; and calibration anchors can support explicit low-S classification without treating missing evidence as zero when the rubric itself provides the estimate.
- **What could be encoded in the skill:** Add automatic calibration-identity detection, distinguish historical/current/company/branch evidence in the scoring schema, and require each claimed cadence signal to carry a domain such as `food`, `beverage`, `event`, or `availability`.
- **Progress:** 579 of 1,644 Phase 6 records decided.

## 2026-07-17 — Phase 6 primary scoring batch 009

- **What happened:** The primary orchestrator decided 50 more accepted records: four scoreable, one canonical duplicate and 45 score-unresolved. Kathmandu Grill, Gourmandise Draper, Emigration Cafe and calibrated Caffe Molise received numeric decisions; R-0877 was later merged into the richer R-1179 Elements-at-35th current-concept record. High-signal but incomplete producers such as Matcha Cafe Kyoto, East Liberty Tap House, Hopkins, White Horse and Annex Burger retained visible markers without fabricated scores.
- **Corrections required from the user:** None. Bars with documented food remained eligible, while juice/coffee chains and fast-casual branches were not excluded merely for format or scale. CupBop and Zao remained unresolved rather than being turned into familiarity exclusions without positive branch-standardization evidence sufficient for the user's screen.
- **What required interpretation:** Roasting coffee and pressing/blending drinks are production but not necessarily restaurant-food fabrication; daily manufacture is not menu turnover; beer/cider/gallery/event cadence is not food cadence; a shared kitchen does not prove independent scratch labor; historical process must stay versioned; and a current successor concept must not inherit its hotel's former brand identity.
- **What could be encoded in the skill:** Type production domains (`food`, `beverage`, `roastery`, `bakery`) and cadence domains, add successor-concept versioning, and distinguish company-production strength from branch-local production confidence in numeric output.
- **Progress:** 629 of 1,644 Phase 6 records decided.

## 2026-07-17 — Phase 6 primary scoring batch 010

- **What happened:** The primary orchestrator decided 60 more accepted records: ten scoreable, two reversible U.S.-standardized-chain preference exclusions and 48 score-unresolved. Strong numeric results include Harvest at the Base, Cafe on Main, Finca, Central 9th Market and Pizza Nono; Harvest's geography conflict remains visible for the later eligibility gate.
- **Corrections required from the user:** None. Crumbl was scored rather than excluded because positive branch/company baking and weekly menu rotation make the scratch/novelty question substantive. Marie Callender's and Cafe Zupas received the separate reversible preference disposition only because their accepted records positively establish standardized multi-state U.S. branch models.
- **What required interpretation:** Corporate scratch can support a cautious score without proving branch-local fabrication; mail-order freezing does not transfer to local service; a successor concept and historical brand must remain versioned; daily specials can establish food cadence while weekly brunch cannot; and company-manufactured cheese is not airport-stall production.
- **What could be encoded in the skill:** Add explicit geography-conflict routing before final eligibility, formal company-versus-branch confidence fields, and a structured cadence classifier that distinguishes rotating dishes from dayparts, events, beverage programs and opening schedules.
- **Progress:** 689 of 1,644 Phase 6 records decided.

## 2026-07-17 — Phase 6 primary scoring batch 011

- **What happened:** The primary orchestrator decided 60 more accepted records: three scoreable, one reversible U.S.-standardized-chain preference exclusion and 56 score-unresolved. Oquirrh received its rubric calibration values, Old Cuss qualified for the scratch-verified/rating-unconfirmed tier, and Annie's Cafe received a criterion-level estimate.
- **Corrections required from the user:** None. Meet Fresh and Ding Tea were not swept into the U.S.-only chain-familiarity screen; Mo' Bettahs received the reversible preference disposition only because accepted evidence positively establishes its standardized multi-state U.S. model. Licensed bars with food remained eligible, and sparse bars were not DQ'd from missing evidence.
- **What required interpretation:** Daily baking/sellout is not turnover; a recurring buffet or event is not necessarily menu change; guest-side cooking is not back-kitchen production; coffee/beer/spirit manufacturing is not restaurant-food fabrication; a dated strong menu cannot be scored as current; and a prepared-meal pickup format needs an explicit production-location treatment rather than automatic exclusion.
- **What could be encoded in the skill:** Add international-versus-U.S. chain scope to preference rules, introduce production-location handling for prepared-meal kitchens, and create a formal historical-evidence decay/versioning rule for otherwise high-signal process records.
- **Progress:** 749 of 1,644 Phase 6 records decided.

## 2026-07-17 — Phase 6 primary scoring batch 012

- **What happened:** The primary orchestrator decided 70 more accepted records: four scoreable, one reversible U.S.-standardized-chain preference exclusion, one canonical duplicate and 64 score-unresolved. Mandarin Restaurant, Monarca, Kahve Cafe and Elements at 35th received numeric scores; R-1232 Old Cuss was merged into the already-scored R-1128 entity so it cannot rank twice.
- **Corrections required from the user:** None. International chains such as Kura, Meet Fresh, Quickly and Ding Tea were not subjected to the U.S.-only familiarity screen. The Capital Grille retained exceptional on-premise butchery/dry-aging evidence despite national-chain status, while Honey Baked Ham was reversibly screened only on positive standardized U.S. branch evidence.
- **What required interpretation:** Corporate production is not branch production; beverage fermentation/roasting is not food fabrication; a new item or promotion is not recurring turnover; current aliases and predecessor concepts must remain versioned; and duplicate candidate records require canonical merging rather than a second score or a false DQ.
- **What could be encoded in the skill:** Add a mandatory canonical-entity decision before ranking, formal duplicate-merger syntax, and domain-aware production/cadence fields that prevent beverage, event and promotion signals from leaking into food scores.
- **Progress:** 819 of 1,644 Phase 6 records decided.

## 2026-07-17 — Phase 6 primary scoring batch 013

- **What happened:** The primary orchestrator decided 70 more accepted records: 12 scoreable, five reversible U.S.-standardized-chain preference exclusions and 53 score-unresolved. Twisted Fern and Urban Hill used calibration anchors; Chop Shop, The Dough Miner, Janet's Sunshine Cafe, Hearth and Hill, Franklin Avenue and other evidence-rich kitchens received criterion estimates. The post-write verifier caught and corrected an initial 13/52 summary arithmetic error; the 70 row decisions themselves were complete.
- **Correction made:** R-0877 and R-1179 both resolve to current Elements at 35th. The earlier R-0877 score was converted to a canonical duplicate and R-1179 now carries the sole score. Batch 009 totals and diary prose were corrected; no user intervention was required.
- **Corrections required from the user:** None. International brands Mochinut and Xing Fu Tang were not put through the U.S.-only screen. Pizza Hut, Dickey's, Crown Burgers, Charleys and Tucanos were reversibly screened only on positive standardized U.S. evidence.
- **What required interpretation:** On-site branch butchery can outweigh chain scale for scratch evidence; off-site company kitchens stay location-scoped; promotions/decor changes are not food cadence; successor aliases require cross-batch reconciliation.
- **What could be encoded in the skill:** Require entity deduplication before scoring, add branch/on-site/company/off-site production fields, and provide a structured correction ledger when later evidence supersedes earlier decisions.
- **Progress:** 889 of 1,644 Phase 6 records decided.

## 2026-07-17 — Phase 6 primary scoring batch 014

- **What happened:** The primary orchestrator decided 70 more accepted records: ten scoreable, two reversible U.S.-standardized-chain preference exclusions, three positive DQs, one canonical duplicate and 54 score-unresolved. Harvest Park City, 'mina, The Nelson Cottage, Don Gallo and other evidence-rich programs received numeric decisions.
- **Corrections required from the user:** None. International/newer chains were not excluded by scale. La Frontera and Pizza Pie Cafe were reversibly screened only on positive evidence of familiar standardized Utah/U.S. models.
- **What required interpretation:** Supplier-made taproom beverages and visiting food trucks positively locate production off-site; an explicitly instant-ramen-only current menu supports an assembly DQ; missing food at other bars remains unresolved; daily deals are promotions rather than turnover; and the second Rooster's record must merge canonically.
- **What could be encoded in the skill:** Add explicit `supplier_only`, `external_vendor_only`, and `commodity_assembly_only` DQ categories, plus an entity-cluster check that runs before every scoring batch.
- **Progress:** 959 of 1,644 Phase 6 records decided.

## 2026-07-17 — Phase 6 primary scoring batch 015

- **What happened:** The primary orchestrator decided 70 more accepted records: 15 scoreable, one reversible U.S.-standardized-chain preference exclusion, two positive DQs and 52 score-unresolved. Bar Nohm, Koyote, Dollie's, Sri Annapoorani, The Peppered Vine, Pago and other evidence-rich kitchens received numeric decisions; Blatch's score retains its unresolved post-fire status.
- **Corrections required from the user:** None. DP Cheesesteaks was reversibly screened only on positive familiar standardized local-chain evidence. The Original Iceberg remained scoreable because documented branch production and monthly flavor change make it a substantive case despite franchise status.
- **What required interpretation:** Strong production can be scored while current status remains separately unresolved; daily vegetarian availability is not turnover; seasonal drinks do not establish food cadence; no-kitchen snack lounges and off-site yogurt production support positive DQs; historical processes do not silently become current.
- **What could be encoded in the skill:** Separate operating-status confidence from production-score confidence, add food-versus-drink cadence typing, and define when off-site finished-product retail is categorically outside the scratch-restaurant producer set.
- **Progress:** 1,029 of 1,644 Phase 6 records decided.

## 2026-07-17 — Phase 6 primary scoring batch 016

- **What happened:** The primary orchestrator decided 70 more accepted records: 11 scoreable, three reversible U.S.-standardized-chain preference exclusions, one positive DQ and 55 score-unresolved. Ramen Ichizu and Sidecar entered the highest tier; Blind Rabbit, Over the Cole's, Siragusa's and several other evidence-rich kitchens received numeric decisions.
- **Corrections required from the user:** None. CRISP & GREEN and Sidecar were scored because positive scratch/seasonal evidence outweighed format, while Dave's, Teriyaki Grill and Houston TX Hot Chicken were reversibly screened only on familiar standardized U.S. branch evidence. International bb.q remained outside the U.S.-only screen.
- **What required interpretation:** Beverage-only roasting can support a positive food-ineligibility DQ when the exact menu closes food; variable in-house/food-truck service cannot; corporate production can support a cautious score with branch confidence penalties; shipment cadence is not menu cadence; predecessor aliases do not inherit process.
- **What could be encoded in the skill:** Add explicit rating/status/production confidence dimensions to every numeric row and require a domain-scoped cadence field (`food_menu`, `beverage`, `sourcing_delivery`, `promotion`, `event`).
- **Progress:** 1,099 of 1,644 Phase 6 records decided.

## 2026-07-17 — Phase 6 primary scoring batch 017

- **What happened:** The primary orchestrator decided 70 more accepted records: eight scoreable, three reversible U.S.-standardized-chain preference exclusions, two positive DQs and 57 score-unresolved. Sal Y Limon, Cheryl's Bagels, Dangerous Pretzel and Rincon Salvadoreno entered the upper tier; Rouser used its rubric calibration.
- **Corrections required from the user:** None. Flower Child, MOOYAH and Seven Brothers were reversibly screened only on positive familiar standardized U.S. branch evidence. International tea/hot-pot chains remained outside the U.S.-only screen.
- **What required interpretation:** Exact drink-only menus can positively establish food ineligibility; a hotel bar's stale closure does not override current official beverage operation; daily one-item flavors are narrower than full-menu turnover; current aliases cannot inherit predecessor process; a menu revision is change evidence but not cadence.
- **What could be encoded in the skill:** Add separate breadth values for production and turnover, and require every status/alias conflict to identify the winning source without deleting the losing literal.
- **Progress:** 1,169 of 1,644 Phase 6 records decided.

## 2026-07-17 — Phase 6 primary scoring batch 018

- **What happened:** The primary orchestrator decided 70 more accepted records: 14 scoreable, three positive DQs and 53 score-unresolved. Engine Room, Flanker, LES BBQ, Mystique Dining, MOZZ, DeeLicious and Monte received high numeric decisions; North Italia was scored on positive production/cadence rather than screened by chain status.
- **Corrections required from the user:** None. No preference exclusions were applied; strong chain scratch evidence remained eligible. Sugar House Distillery, Happy Taps and Second Summit were DQ'd only on explicit non-restaurant or external-vendor-only evidence.
- **What required interpretation:** Availability-driven change is not fixed cadence; event menus remain scoped; daily preparation is not turnover; current service can outweigh a stale closure label without deleting it; high production can remain unresolved when no food cadence exists.
- **What could be encoded in the skill:** Add score eligibility examples for occasional versioned changes, require a distinct `availability_change` signal, and formalize non-restaurant versus external-vendor-only DQ subtypes.
- **Progress:** 1,239 of 1,644 Phase 6 records decided.

## 2026-07-17 — Phase 6 primary scoring batch 019

- **What happened:** The primary orchestrator decided 70 more accepted records: eight scoreable, three reversible U.S.-standardized-chain preference exclusions, two positive DQs and 57 score-unresolved. Parfe Diem, Prime Corn, Antica Sicilia, All Purpose Bakehouse and Soup & Sip entered high tiers.
- **Corrections required from the user:** None. Barnes & Noble Cafe, BonFire/Maverik and Taste of Philly were reversibly screened only on positive standardized U.S. branch evidence. Strong but incomplete chain production such as Fogo de Chao and Mountain Mike's remained visible rather than excluded.
- **What required interpretation:** Non-food concert venues and outside-food/no-kitchen bars can be positively DQ'd; seasonal beverage changes are not food cadence; a “special” menu label is not rotation; ghost-kitchen/catering format is neutral when production is explicit; retail frozen products stay separate from restaurant production.
- **What could be encoded in the skill:** Add first-class ghost-kitchen/mobile/catering production-location handling and require explicit breadth/cadence support before promoting broad scratch marketing into numeric scores.
- **Progress:** 1,309 of 1,644 Phase 6 records decided.

## 2026-07-17 — Phase 6 primary scoring batch 020

- **What happened:** The primary orchestrator decided 70 more accepted records: 11 scoreable, two reversible U.S.-standardized-chain preference exclusions, three positive DQs and 54 score-unresolved. Red Iguana, Firewood and The Eating Establishment used calibration anchors; Cafe Madrid, Lone Star Taqueria, Purple Sage and Java Cow received criterion estimates.
- **Corrections required from the user:** None. Bad Ass Coffee and Hires were reversibly screened only on positive familiar standardized U.S. branch evidence. Great Harvest retained exceptional branch-local milling/baking evidence and was not excluded by franchise status.
- **What required interpretation:** Calibration anchors can preserve a low S result despite isolated current scratch markers; daily one-item change is scoped cadence; beverage experimentation is not food turnover; current revival evidence cannot inherit predecessor favorites; explicit external-food/nonrestaurant boundaries support DQ.
- **What could be encoded in the skill:** Add a calibration-override audit note whenever current evidence appears stronger than a stored anchor, and require final output to show scratch-marker-rich but cadence-unresolved venues separately.
- **Progress:** 1,379 of 1,644 Phase 6 records decided.

## 2026-07-17 — Phase 6 primary scoring batch 021

- **What happened:** The primary orchestrator decided 70 more accepted records: 16 scoreable, seven reversible U.S.-standardized-chain preference exclusions, three positive DQs, one canonical duplicate and 43 score-unresolved. Bewilder, High West, Valter's, Per Noi, Market Street, Arlo, Franck's, Windy Ridge and the current Sidecar kitchen entered numeric tiers.
- **Corrections required from the user:** None. Franchise/local-chain scratch evidence remained visible; only positively familiar standardized U.S. branches received the reversible screen. The two Astro records were merged to one 39th & State entity.
- **What required interpretation:** A same-address/branch duplicate must not rank twice; current in-venue kitchens supersede historical no-food states without transferring operator continuity; external trucks remain outside host production; uncooked take-and-bake retail is not a prepared restaurant meal; a calibrated S anchor can coexist with newly estimated I.
- **What could be encoded in the skill:** Require fuzzy entity clustering before scoring, and add explicit prepared-meal eligibility examples for uncooked take-and-bake, amusement-park stands and in-venue independently branded kitchens.
- **Progress:** 1,449 of 1,644 Phase 6 records decided.

## 2026-07-17 — Phase 6 primary scoring batch 022

- **What happened:** The primary orchestrator decided 70 more accepted records: 11 scoreable, three reversible U.S.-standardized-chain preference exclusions, five positive DQs and 51 score-unresolved. VENETO and HSL entered elite tiers; Ruth's, Emigration Brewing, The Dodo, Tulie, Mazza, El Menos and others received numeric decisions.
- **Corrections required from the user:** None. Dee's, Rancherito's and Warrens were reversibly screened only on positive familiar standardized U.S. evidence. High-signal franchise/chain production such as Thirst's split bakery/store process remained scoreable.
- **What required interpretation:** Daily manufacture is not menu rotation; supplied/off-site products stay location scoped; packaged-snack/no-kitchen/outside-food bars support positive DQ; recurring offers are promotions unless item change is shown; historical process cannot score current production.
- **What could be encoded in the skill:** Add separate `production cadence`, `menu turnover`, `promotion cadence`, and `availability cadence` fields, plus a formal snack-only/external-food eligibility threshold.
- **Progress:** 1,519 of 1,644 Phase 6 records decided.

## 2026-07-17 — Phase 6 primary scoring batch 023

- **What happened:** The primary orchestrator decided 70 more accepted records: nine scoreable, two reversible U.S.-standardized-chain preference exclusions, three positive DQs, one canonical duplicate and 55 score-unresolved. Taqueria 27, Tin Roof, Navajo Hogan, Alpenglow Table and Sri Annapoorani Express received numeric decisions; the later 'mina record merged into R-1493.
- **Corrections required from the user:** None. Both 7 Brew branches were reversibly screened on positive standardized U.S. drive-through evidence. Private-event-only Millcreek Inn and explicit no-food nightclub records received positive DQs without discarding their production/operation evidence.
- **What required interpretation:** Private-event production can be strong yet ineligible as a walk-in restaurant; daily handcraft is not menu turnover; brand-level rotation can support a cautious branch score with confidence penalty; tenant turnover in an incubator is not menu cadence; repeated exact identities must merge.
- **What could be encoded in the skill:** Add public-access eligibility as a separate field, and require canonical-entity and company-versus-branch reconciliation before numeric scoring.
- **Progress:** 1,589 of 1,644 Phase 6 records decided.
## 2026-07-17 — Phase 6 primary scoring batch 024 (final 55)

- **What happened:** Reconciled the interrupted prior patch against the authoritative Phase 5 ledger, proving 1,589 unique decisions and deriving the exact 55-record set difference. Three evidence-only subagents reread every linked accepted record; the primary agent then independently applied the Phase 6 rating gate, scratch score, interest score, positive-DQ rule and reversible user-preference screen.
- **Corrections from the user:** The user's chain correction continued to control this batch: fast service and multi-location status were not treated as negatives by themselves. Pizzeria Limone, Franco's, Toasters, Tuk Tuk's, Settebello and several other small/local groups retained their cooking evidence instead of being cheaply excluded. Only positively evidenced familiar standardized U.S. formats were preference-screened.
- **What required interpretation:** Hotel and institutional affiliation cannot transfer ratings or prove standardization; entertainment cadence is not food cadence; daily production is not necessarily menu turnover; historical production remains version-scoped; a temporary remodel is not permanent closure; local multi-location businesses need evidence of repeatable low-novelty standardization before preference exclusion; and strong scratch evidence cannot bypass a missing direct rating gate.
- **What the SKILL could encode:** Add an explicit rating-source fallback hierarchy; distinguish `daily-production-cadence` from `menu-turnover-cadence`; provide a standardized-format evidence checklist that separates small local groups from nationally familiar concepts; and define how institutional commissary uncertainty affects scoring without automatically causing preference exclusion.
- **Progress:** 1,644 of 1,644 Phase 6 records now have a primary decision. Completion remains unclaimed pending the full ID, DQ-evidence, arithmetic, duplicate, preference and missing-evidence audits.

## 2026-07-17 — Phase 6 positive-DQ correction audit

- **What happened:** Audited every DQ rationale across all scoring batches against the positive-evidence invariant. Seven older rows—Salt Lake County Cafeteria, No. 119, The Green Room, Mono Tape Club, The Marquis Park City, Club Karamba and Tequila Night Club—rested on exhausted or absent food-program evidence rather than an affirmative closure, no-food statement, external-supplier boundary or snack-only menu. Each was corrected to `score-unresolved` with the uncertainty preserved.
- **Corrections needed:** This was an internal gate correction, not a user correction. The evidence research was adequate; the disposition had improperly converted absence into a negative verdict.
- **What the SKILL could encode:** Require a machine-checkable DQ evidence subtype such as `explicit_closed`, `explicit_no_food`, `external_food_only`, `offsite_all_production`, `uncooked_retail_only`, or `confirmed_snack_only`, and reject DQ rows whose only terminal state is `exhausted-unavailable`.
- **Progress:** The universe remains 1,644 exactly-once decisions. All remaining DQs now carry affirmative evidence; the rest of the Phase 6 gate is still being audited.

## 2026-07-17 — Phase 6 completion gate

- **What happened:** Completed exact ID reconciliation, disposition counting, score-vector bound checks, total checks, geometric-mean recomputation, S-floor/ranked-tier checks, all-DQ evidence review, preference-screen review and canonical-target verification. The audit corrected five G rounding errors, two criterion values that exceeded the printed maximum for coherence, and seven absence-based DQs.
- **Corrections needed:** Internal audit corrections only. No restaurant was dropped: the seven invalid DQs moved to unresolved, and score corrections retained the same qualifying status.
- **What required interpretation:** Calibration anchors may retain numeric S below 60 only when explicitly marked not ranked; rating-unconfirmed scratch tiers are distinct from rating-gated ranked tiers; a batch-level accepted-ledger declaration plus per-row scoped rationale provides the evidence link without duplicating long URLs in the decision ledger.
- **What the SKILL could encode:** Provide a bundled Phase 6 validator for population equality, category normalization, five-vector maxima/sums, G rounding, S-floor/ranked status, canonical target existence and enumerated positive-DQ subtypes. This audit found defects that prose review alone had missed.
- **Progress:** Phase 6 is complete: 1,644/1,644 exactly-once decisions and all printed gate items pass. Manifest advanced to `phase-6-complete`.
## 2026-07-17 — Phase 7 coverage audit pass 1

- **What happened:** The Phase 7 instructions were embedded in `SKILL.md` and `reference/phase-7-coverage-audit.md`, not in a category-local `phase-7-coverage.md`; after locating and reading all required files, a fresh multi-family web challenge found six in-scope omissions and entered them as coverage additions.
- **Corrections needed:** No user correction. The run's original convergence had missed an established airport hotel restaurant, two small Mexican/informal venues, two dessert openings and a new mobile Peruvian/Mexican operation.
- **What required interpretation:** Announced future concepts were not current candidates; primary bakery/dessert formats remain discovery-adjacent in the restaurant census but will retain their literal format; exact branch additions were separated from existing parent brands; search snippets created candidates only and did not qualify them.
- **What the SKILL could encode:** The phase map should point directly to every required Phase 7 file and avoid implying a category-local filename. A reusable identity-comparison helper and a recent-opening source checklist would reduce missed branch/opening rows.
- **Progress:** Phase 7 pass 1 yielded six additions; gate remains open until their Phase 4–6 loop completes and a repeat full challenge yields zero.
## 2026-07-17 — Phase 7 loop-back Phase 4–5, coverage additions 001

- **What happened:** Dispatched one six-record leaf batch using the v8.10 canonical restaurant evidence prompt verbatim, saved the raw return, and personally inspected every field of all six records. All passed semantic acceptance without repair.
- **Corrections needed:** None. Branch-scope discipline was especially important for Monkeywrench and Magnolia, while Casa del Pollo's possible Señor Pollo relationship remained an unresolved customer-signal conflict rather than an identity merge.
- **What required interpretation:** Sparse but fully exhausted records are acceptable; broad generic scratch claims remain scoped; a new branch cannot inherit another branch's ratings/hours; a food truck can be accepted with a dated press identity even when official channels and ratings exhaust.
- **What the SKILL could encode:** Coverage additions would benefit from an append-safe ledger helper that updates universe counts and candidate states atomically while preserving the original frozen-population audit.
- **Progress:** Phase 7 loop-back Phase 5 accepted 6/6 additions. Current evidence universe: 1,650; primary scoring for the six remains pending.
## 2026-07-17 — Phase 7 loop-back Phase 6, coverage additions 001

- **What happened:** The primary agent scored/classified all six accepted additions. Magnolia's documented scratch small-batch program cleared S60 but lacked a direct branch rating, so it entered the explicit rating-unconfirmed tier. The other five remained unresolved without low scores or DQ.
- **Corrections needed:** None. Magnolia was not cheaply preference-excluded merely because it is a franchise: its documented production is material, matching the user's correction that chain status is not the objective.
- **What required interpretation:** A broad hotel menu with several house components can remain below the qualifying evidence threshold; generic made-from-scratch language is weaker than component proof; new branches cannot inherit brand execution ratings; and scratch-verified/rating-unconfirmed is a surfaced tier rather than a ranked recommendation.
- **What the SKILL could encode:** Add a worked example for a genuinely scratch-producing franchise with no branch rating, demonstrating the separation between production scoring, user preference screening and the rating gate.
- **Progress:** All six pass-1 additions completed Phases 4–6. Current decision universe: 1,650. Phase 7 now requires a repeat full challenge with zero yield.

## 2026-07-17 — Phase 7 repeat challenge and completion gate

- **What happened:** Reran the complete 24-query, six-family omission challenge after the additions were researched and classified. Every plausible hit reconciled to a canonical row, a pass-1 addition, an existing user-approved novelty-screen row, a future/non-operating concept, a nonrestaurant format or an out-of-scope result. The last full pass yielded zero new identities.
- **Corrections needed:** None from the user. The repeat pass confirmed why chain status alone is insufficient: First Watch and Crispy Cones were handled through the already approved U.S.-standardized low-novelty preference screen, while scratch-producing Magnolia remained visible and scored despite being a franchise.
- **What required interpretation:** A current vendor directory does not create one restaurant identity for the host facility; retail tortilla/charcuterie production is not automatically a restaurant; announced future openings are not current operating candidates; and apparent new search results must be checked against branch, alias and successor relationships before being counted.
- **What the SKILL could encode:** Provide a small canonical-match utility that normalizes punctuation, address, phone/domain, branch labels and successor aliases, and have the Phase 7 gate emit a machine-readable disposition for every apparent new hit (`canonical`, `preference-screened`, `future`, `nonrestaurant`, `outside-scope`, or `new`).
- **Progress:** Phase 7 gate passes. Expanded universe remains 1,650 evidence records and 1,650 exactly-once decisions. Manifest advanced to `phase-7-complete`; Phase 8 rendering is next.

## 2026-07-17 — Phase 8 rendering and final completion audit

- **What happened:** Rendered the reader-facing occasion matrix, dish-ranked rare-find layer, east-side scratch-dessert corridor appendix, coverage statement and complete 226-row numeric audit table to `08-results.md`. The dessert appendix incorporated a delegated second-pass audit and distinguishes confirmed branch evidence, narrower/uncertain proof and day-specific 8 p.m. availability.
- **Corrections needed:** The first renderer execution exposed an older system Ruby without `filter_map`; the renderer was corrected to use `map` plus `compact`. The first successful parse captured only 207 vector-form numeric rows and omitted 19 calibrated scalar-form rows; a second parser branch restored all 226 scoreable decisions. No user correction was required.
- **What required interpretation:** The top combined scores cannot simply become the reader shortlist: Prime Corn's preorder/catering/event format needs an operational caveat, near-ties should remain ties, and occasion fit can favor a walk-in venue. Unresolved dessert venues can be surfaced when their scratch marker is strong, but they must not inherit a numeric verdict. Current branch hours and production must not transfer from a sibling branch.
- **What the SKILL could encode:** Ship a canonical Phase 8 renderer that parses both vector and calibrated score forms, validates the number of rendered rows against all `scoreable` decisions, and supports evidence-scoped appendices such as `open at 8pm` without transferring brand-level hours. A single normalized score schema would have prevented the 207-versus-226 omission.
- **Verification:** Evidence ledger 1,650 rows/1,650 unique IDs; decision ledger 1,650 rows/1,650 unique IDs; no missing or extra IDs; no duplicate decision IDs; 226 scoreable rows; zero score arithmetic defects; 226 contiguous unique audit rows; four top-three occasion rows; every standard artifact exists and is nonempty; Phase 7 last-pass yield is zero.
- **Progress:** All eight phases and every printed completion gate pass. Manifest advanced to `complete` with links to all standard artifacts.

## 2026-07-17 — Post-render occasion-diversity correction

- **What happened:** The initial four occasion lists reused Ramen Ichizu, Stoneground and Navajo Hogan across multiple cells. The user correctly identified that repetition wastes reader-facing slots in a 1,650-restaurant run. The occasion layer was re-optimized as one 12-slot set with 12 distinct venues while retaining three evidence-supported choices per intent.
- **Correction from the user:** Large runs should highlight different places in each occasion rather than repeatedly surfacing the same leaders.
- **What required interpretation:** Occasion fit remains primary, but once a run has many credible alternatives, the marginal benefit of repeating a top venue is lower than the discovery value of the next strong fit. The underlying combined-score audit remains unchanged and still exposes overall leaders.
- **What the SKILL now encodes:** Added a large-run diversity override to Phase 8: with at least 12 eligible venues, optimize all occasion cells jointly and use each venue once unless an occasion genuinely lacks three credible distinct choices.
- **Progress:** Reader results and PDF regenerated with 12 unique occasion recommendations; research decisions and scores are unchanged.

## 2026-07-17 — Post-render cross-layer diversity correction

- **What happened:** Although the occasion layer had been diversified, all five rare-find venues still repeated restaurants already used in those occasions. The rare-find list was rebuilt with five different scratch-qualified venues and dish-level scarcity evidence: Bar Nohm, The Big Mango, Biscotts, Mazza and House of Corn.
- **Correction from the user:** Rare dishes should not recycle the same restaurants already highlighted elsewhere when a large run has ample alternatives.
- **What required interpretation:** Diversity cannot override the rare-find scratch gate or manufacture scarcity. Replacement dishes therefore needed accepted venue-level production evidence plus a defensible local-market rarity claim, not merely unusual menu wording.
- **What the SKILL now encodes:** Large-run diversity applies across the occasion and rare-find layers as one reader-facing discovery budget. Cross-layer repetition requires a stated lack of credible alternatives.
- **Progress:** The top reader-facing occasion and rare-find layers now surface 17 distinct venues. The exhaustive dessert appendix may naturally mention some of them because completeness, rather than slot allocation, is its purpose.

## 2026-07-19 — Post-run scoring-conservatism finding

- **What happened:** A review of Arempas exposed that the run left some venues `score-unresolved` despite affirmative, attributable scratch evidence. Arempas had first-party statements that its meats are prepared and seasoned in-house and its arepas are handcrafted, fresh and never frozen, yet missing evidence for other components, sourcing and turnover prevented any numeric score.
- **Correction from the user:** Once credible scratch evidence exists, it should earn the venue at least some scratch score. Missing evidence may limit the score and lower confidence, but should not erase established production evidence or force the entire venue into an unresolved state.
- **Correction from the user:** Menu turnover is not evidence against scratch production. It measures how interesting repeated visits may be and belongs on the return-interest axis, not the scratch axis. A deeply scratch traditional kitchen with a static menu should retain a strong scratch score while receiving lower repeat-visit novelty where appropriate.
- **What required interpretation:** `Unknown` must remain distinct from both zero and disqualification at the criterion level. Partial affirmative evidence should produce a partial, provenance-labeled score with uncertainty, while genuinely unobserved subcomponents remain unknown. Separately, using volatility inside both `S_scratch` and `I` double-counts turnover and biases the eligibility gate against static traditional specialists.
- **What could be encoded in the SKILL:** Define criterion-level partial scoring and confidence so affirmative production evidence always contributes without imputing missing fields. Remove menu volatility from the scratch construct or make it non-penalizing there, and reserve turnover for the interest/repeat-visit construct. Recalibrate the `S >= 60` gate after separating these axes rather than mechanically applying the current threshold to a changed score definition.
- **Progress:** Diary updated only at the user's direction; the rubric and completed-run decisions remain unchanged.
