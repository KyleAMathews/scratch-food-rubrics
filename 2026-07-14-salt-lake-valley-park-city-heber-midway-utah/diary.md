# Bakery Rubric v8.9 Test-Run Diary

Purpose: record what happened after each phase, what the user corrected, what the orchestrator had to infer or troubleshoot, and concrete improvements that may belong in the skill itself. This is observational test-run material, not qualification evidence.

## Phase 1 — Scope, run directory, and catchment

### What happened

- Read `phase-1-scope-and-catchment.md`, then re-read the required shared status/provenance contract immediately before execution.
- Created the unique run directory and all standard placeholders before any venue research.
- Interpreted the request as a multi-component resident/day-trip market with East Millcreek as the origin: populated Salt Lake Valley, Park City/Snyderville Basin, Heber Valley (Heber–Midway plus immediately continuous settlements), and the connecting I-80/US-40/UT-113 corridor.
- Used OSM/Nominatim and Overpass to resolve Salt Lake County, Park City, Midway, and Millcreek. `map_to_area` returned non-zero areas for Salt Lake County, Park City, and Millcreek. Midway's relation existed but its area was unavailable; Heber City resolved only as a node. Official municipal GIS/map pages were used as documented fallbacks.
- Recorded adjacent exclusions, fuzzy functional-market edges, and tool limitations in `01-scope.md`; verified every Phase 1 gate item before advancing.

### User corrections or interventions

- None after Phase 1 execution. The user's original wording supplied an intentionally broad general area rather than a strict radius; no later narrowing correction was needed.

### Things the orchestrator had to figure out

- The phase says to prefer a real OSM administrative polygon, but the requested geography is not one administrative place. The component-list rule was the decisive instruction.
- "Salt Lake Valley" cannot be represented cleanly by Salt Lake County: the county polygon includes mountain watersheds and west-desert land. The scope needed a reproducible county outer bound plus an explicit populated-valley component list.
- Park City's resident-normal market clearly extends outside municipal limits into Snyderville Basin/Kimball Junction. Heber and Midway similarly need a functional rural ring.
- Overpass area materialization can fail even when a valid boundary relation and non-zero bbox exist. The skill's fallback language was sufficient, but the exact verification workflow was not specified.

### Possible skill improvements

1. Add an example for a user-named multi-market corridor (home neighborhood + metro valley + day-trip towns), showing that the correct artifact is a component list rather than one polygon or radius.
2. Define an explicit `map_to_area` verification fallback sequence: relation lookup → `map_to_area` → direct area-ID check → official municipal GIS/map → documented bbox/component fallback.
3. Clarify whether a county polygon may be used as an outer verification bound when the requested vernacular region (such as a valley) is smaller, provided the controlling populated-component list is explicit.
4. State whether obvious route-adjacent resort enclaves should default in or out for a resident-normal market; this run excluded destination-only canyon ski markets while including Snyderville Basin.

### Phase outcome

Passed all Phase 1 completion-gate items. No recommendations were rendered.

## Phase 2 — Candidate discovery

### What happened

- Re-read the phase instructions, bakery discovery reference, and shared status/provenance contract immediately before discovery.
- Ran Track A with bakery, pastry, confectionery, chocolate, craft, cuisine, name, panadería, bagel, tortillería, and other adjacent signals. Four validated raw component responses contained 245 elements and deduplicated to 241 unique OSM identities.
- Ran eight adaptive targeted batches (32 exact queries) covering broad best-of, scratch, artisan/baker-led, recent openings, every catchment component, Spanish-language panadería/tortillería terminology, cottage/preorder and market formats, gluten-free production, and every rubric marker family.
- Ran a visible-head challenge against local/editorial sources including Gastronomic SLC, KSL/Deseret News, Salt Lake Tribune, Axios Salt Lake City, City Cast, Visit Utah, Park City Magazine, tourism/directory heads, and recent community roundups.
- Added 42 non-OSM or identity-thin targeted leads. Preserved 283 discovery rows total. Fourteen literal name-regex collisions/non-retail industrial facilities were kept in the discovery ledger but not promoted; 269 in-category or category-adjacent rows entered the candidate ledger.
- Preserved every validated raw response, the derived OSM union, a targeted-source summary, exact query log, provenance, and explicit zero scoring count.

### User corrections or interventions

- The user identified this as a test run of the new skill version and requested a phase-by-phase `diary.md`. This changed the run artifacts, not the bakery scope or discovery judgments. The diary was created inside the existing Phase 1 run directory to respect artifact containment.
- No discovery candidate, query, boundary, or classification was corrected by the user.

### Things the orchestrator had to figure out

- A full Overpass county-area query was slow and initially appeared to return nothing; it later produced valid JSON. Smaller bbox queries worked quickly, while several parallel calls returned HTML error pages. Valid JSON had to be tested semantically rather than assuming that a created file was a successful response.
- The shell's `status` variable is read-only in zsh, which aborted one connectivity-test wrapper after the download. This was runtime friction, not a research limitation.
- The web-search tool pools results from four queries and does not expose a stable result count per individual query. The log therefore records exact distinct named in-scope leads inspected per batch and explicitly avoids inventing hit counts.
- The broad name regex necessarily surfaced literal non-food collisions (`Break Bread Barber`, a clothing shop named `Cake`, a nail salon, a pet bakery) plus industrial bakery plants not accessible as buyer venues. These were preserved in discovery but excluded by literal category hygiene without making scratch or quality judgments.
- The map union is highly branch-heavy (national cookie/bagel chains, multiple locations) and includes stale/renamed/closed identities. Phase 3 must do significant semantic normalization; raw row count is a poor proxy for meaningful candidate count.
- Current-date browsing materially changed the head: All Purpose Bakehouse opened in February 2026, Magnolia opened in Holladay in June 2026, Union Patisserie is current in Park City, and Chubby Baker closed in November 2025.

### Possible skill improvements

1. Specify how to log `result count` when a search API pools several exact queries and exposes no per-query count. A recommended field pair such as `returned_count_unavailable` plus `distinct_named_leads_inspected` would remove ambiguity.
2. Require JSON/content-type validation before a broad response is counted, and explicitly say whether failed HTML/timeout responses should be preserved, renamed as failures, or deleted.
3. Provide an Overpass fallback threshold: after an area query exceeds a stated time or fails once/twice, switch to a printed non-overlapping tile plan. The current text says partition when needed but not when to stop retrying.
4. Clarify the category-hygiene disposition vocabulary for literal regex collisions and non-retail factories. The candidate-state contract has no explicit `not-a-category-candidate` state, so this run preserved them only in discovery and omitted them from the candidate ledger.
5. State whether every branch of a national chain must remain a distinct evidence candidate or may share a brand-level evidence record while retaining branch rows. This matters greatly in a metro-scale run.
6. Add `diary.md` as an optional standardized test artifact for rubric-development runs, with a rule that it lives under `{RUN_DIR}` and never counts as evidence.

### Phase outcome

Passed all Phase 2 completion-gate items. No qualification, disqualification, scoring, or recommendations were produced.

## Phase 3 — Discovery convergence

### What happened

- Re-read the Phase 3 instructions and shared contract immediately before execution.
- Normalized the 269 Phase 2 candidates and merged three true duplicate rows while retaining their source identities and provenance. Distinct branches were deliberately not collapsed.
- Inspected the full coverage grid across geography, language/script, tradition, service format, specialist/broad format, and established/new status.
- Ran eight fresh adaptive gap passes. The first seven added 47 candidates, taking the post-deduplication set from 266 to 313. The eighth complete pass added zero current in-scope candidates, allowing the ledger to be frozen.
- The most consequential repairs were Spanish-language western-valley panaderías, low-visibility cottage/preorder bakers, Midway resort/farm-store bakeries, and scratch bakery departments inside Harmons and Lee's stores.
- Reported 313 frozen IDs, 3 duplicate merges, 114 rows with aliases/local names, and a conservative 30 multi-location groups containing 98 branch rows.

### User corrections or interventions

- None during Phase 3. The user did not correct a candidate, merge, boundary, or interpretation.
- The previously requested test diary continued to shape the artifact set; it did not change discovery decisions.

### Things the orchestrator had to figure out

- The phase requires convergence, but a broad metro search can keep exposing increasingly marginal directory entries. I treated “new candidate” as a genuinely named, in-scope producer/venue lead returned by the adaptive query, not every unrelated bakery in a directory's automatically generated “nearby” list.
- Harmons and Lee's were not captured by bakery-focused OSM tags because their top-level format is supermarket. Their official pages nevertheless describe scratch/fresh in-store bakery work. The skill's format-neutral and adjacent-category rules required promoting each in-scope branch rather than dismissing the chains as groceries.
- Branch retention creates a large evidence burden: 98 rows sit in 30 multi-location groups. The phase says production may differ by branch, so I kept separate IDs even where discovery-level brand evidence is shared.
- A current-looking search result can point to an old archive. West Valley City's Panadería del Rancho result was published/crawled recently but the underlying list covered January 2017. It did not count as a new current candidate in the zero-yield pass.
- A literal alias count needed an operational definition. I counted rows with an actual alias, prior/local name, handle, or branch label and excluded `none found`, blank, and `unverified`.
- “Branch count” was also underspecified. I reported both normalized multi-location groups and participating branch rows, using a conservative canonical-name normalization rather than pretending the raw repeated-name count was exact semantic identity.

### Possible skill improvements

1. Define what counts as a `new lead` during convergence when a result page contains a primary match plus dozens of auto-generated nearby listings. Without this, exhaustive metro runs can expand indefinitely.
2. Define `alias count` and `branch count` precisely for the Phase 3 gate—for example, alias strings versus rows containing aliases, and branch groups versus branch rows.
3. Add explicit guidance for bakery departments within supermarkets, hotels, resorts, farm stores, and restaurants. The current format-neutral principle implies inclusion, but does not say whether all branches must enter discovery once scratch production is claimed at brand level.
4. State whether a branch family may share a Phase 4 brand-level process source while still requiring branch-specific status/address research. This run's 98 branch rows will otherwise duplicate large amounts of evidence work.
5. Add a staleness rule for discovery-only business-license and directory records. A recently indexed page can describe a decade-old list; the underlying record date must control.
6. Recommend a structured coverage-grid schema in the candidate ledger so geography, language, tradition, service format, specialist/broad, and established/new fields do not have to be reconstructed from combined prose columns.
7. Consider a bounded “directory-neighbor expansion” rule, such as inspecting only named primary results and a fixed number of category-nearby entries, followed by a zero-yield targeted pass.

### Phase outcome

Passed all Phase 3 completion-gate items and froze 313 candidate IDs for evidence research. No qualification, disqualification, scoring, or recommendations were produced.

## Phase 4 — Evidence research

### What happened

- Re-read the Phase 4 instructions, canonical worker prompt, and shared status/provenance contract immediately before dispatch.
- Split the 313 frozen candidates into 24 immutable batches: 23 batches of 13 and one final batch of 14. Three evidence-retrieval workers processed the batches in parallel and were reused only after their preceding raw return had been preserved.
- Sent the canonical worker block without adding scoring, eligibility, disqualification, confidence, or output-path fields. Only the declared catchment, access date, and candidate-batch placeholders were substituted.
- Preserved 24 raw Markdown returns totaling 890,486 bytes and indexed every dispatch, worker, batch membership, artifact filename, and returned state.
- Marked all 313 frozen candidates `evidence-returned`. No return was called accepted, no repair was performed, and no bakery was scored or classified.
- Ran a semantic coverage audit rather than relying on line counts. All 313 target records were present. B04 also repeated the 13 B01 records before its 13 target records; the duplicate material was retained verbatim and excluded from the frozen-candidate count.

### User corrections or interventions

- None during Phase 4. The user did not correct candidate membership, worker behavior, evidence interpretation, or the catchment.
- The user's earlier request for a phase diary continued to add this execution record, but did not change evidence research.

### Things the orchestrator had to figure out

- The canonical prompt permits substitution of only three placeholders and provides no output-path placeholder. Raw preservation therefore required a separate artifact-only follow-up turn after every research return.
- A 13-candidate response commonly ran tens of kilobytes; the complete raw corpus reached about 0.89 MB. The orchestration cost was dominated by repeated canonical prompt transmission, long returns, and separate preservation turns.
- Branch-level retention produced repeated brand evidence for Harmons, Lee's, Einstein Bros., Kneaders, Nothing Bundt Cakes, See's, and other multi-location groups. Workers still had to retrieve branch-specific identity, hours, ratings, and reviews.
- Workers did not format every return identically. Some used level-three headings, some shortened the canonical field names, and some wrote `Unavailable` instead of literal `exhausted-unavailable`. Phase 4's gate certifies only return and preservation; Phase 5 must decide acceptance and repair.
- B04 contained its 13 requested target records plus an exact carryover of 13 records from the worker's earlier B01 response. Because preservation had to remain verbatim, the right treatment was to retain the duplication, document it, and count only the semantically matched B04 targets.
- Direct Google/Yelp-style pages were not always retrievable. Workers frequently preserved literal ratings from Restaurantji, Restaurant Guru, Apple Maps, Wanderlog, Birdeye, DoorDash, or other aggregators. Phase 5 must verify whether each source satisfies acceptance requirements.
- Several workers called a field exhausted after a compressed search description rather than a fully enumerated five-stage trail. Those records are returned, not accepted.

### Possible skill improvements

1. Add a declared `{OUTPUT_PATH}` placeholder to the canonical worker prompt, or explicitly require workers to write the raw return to an orchestrator-supplied path. This would remove one artifact-only turn per batch.
2. Define a shared-evidence model for branch families: one brand/process evidence packet plus mandatory branch-specific identity, status, hours, rating, and review records. This would reduce duplication without collapsing branches.
3. Require the candidate ID in every record heading. Name-only headings make semantic coverage auditing needlessly manual when aliases, rebrands, and duplicate names exist.
4. Specify whether field-label and heading-level deviations make a return malformed in Phase 4 or merely trigger Phase 5 repair. The current gate distinguishes returned from accepted but leaves structural minimums implicit.
5. State whether an accumulated or duplicated worker response should be re-requested immediately or preserved and deferred to Phase 5. This run retained the complete B04 raw return because target coverage was intact.
6. Add a machine-readable per-batch manifest or JSON sidecar containing candidate IDs, worker, dispatch time, return time, raw path, and section count. The Markdown index works, but validation requires custom parsing.
7. Clarify the evidentiary role of rating/review aggregators when direct platform pages are inaccessible, including whether literal values from Apple Maps, Birdeye, Restaurant Guru, or Wanderlog can be accepted or must always be repaired.
8. Give workers an explicit minimum search-trail syntax for each of the five source stages, including a required query-or-URL entry even when unavailable. This would make exhaustion claims auditable.
9. Consider an output-size or source-count budget per candidate. The current full sequence across 313 candidates is thorough but operationally expensive, especially for obvious duplicate branches and identity-thin directory collisions.

### Phase outcome

Passed all Phase 4 completion-gate items: every frozen candidate has a returned record, all 24 raw returns are preserved, and the dispatch/coverage audits are complete. No evidence return was accepted yet, and no qualification, disqualification, scoring, or recommendations were produced.

## Phase 5 — Evidence acceptance and repair

### What happened

- Re-read the Phase 5 instructions, canonical worker prompt, and shared status/provenance contract immediately before acceptance work.
- Semantically inspected all 313 returned venue records in frozen-ledger order. Every original record contained useful material, but every record also had at least one acceptance defect under the strict contract: compressed search trails, non-adjacent provenance, implicit product-only treatment, nonterminal exhaustion, or unverified conflicts. B09–B24 also showed more structural label/heading drift.
- Recorded a concrete field-level defect profile for every candidate and moved all 313 to `repair-requested` before dispatching bounded repairs.
- Sent 24 repairs to the original Phase 4 workers, preserving returned facts and forbidding scoring, eligibility, disqualification, or rewriting accepted material. Each repair added adjacent provenance, explicit product-only labels, all five source stages, field-specific terminal exhaustion, and direct/independent conflict verification.
- Changed the artifact-handling pattern after the first wave: workers wrote repair returns directly to declared run-directory paths and returned only the verified path. This eliminated the separate copy-only turn required during Phase 4.
- Primary-orchestrator re-review accepted 304 candidates and marked 9 genuinely unresolved identities `evidence-exhausted-unavailable`: T-005, T-042, A-008, A-017, A-020, A-033, A-058, A-064, and A-199.
- Preserved 24 raw repair files totaling 606,722 bytes. Together with the original corpus, every candidate now has a durable original return, repair patch, ledger state, worker attribution, and orchestrator acceptance decision.
- Preserved conflicts instead of averaging or silently choosing: current versus historical addresses/hours/status, platform-specific ratings, official versus directory phone numbers, chain-level versus branch-level process, and factory versus store-local production.

### User corrections or interventions

- None during Phase 5. The user did not correct an evidence fact, acceptance decision, worker assignment, or conflict treatment.
- I posted an incorrect running count of 115 processed / 110 accepted, immediately recalculated it as 117 / 112, corrected the user-facing update, and verified subsequent counts directly from both ledgers rather than mental arithmetic.

### Things the orchestrator had to figure out

- The strict rule requiring every opened source and every query, plus all five source stages before terminal exhaustion, made every one of the 313 original returns repairable even when its substantive bakery facts were sound. Phase 5 therefore nearly duplicated Phase 4's corpus rather than acting as a selective exception path.
- Evidence acceptance needed a practical distinction between a fully unresolved candidate and a partially documented candidate. A record was terminally exhausted only when no attributable identity/location evidence survived all five stages; a branch with valid chain-level facts but missing branch-specific fields remained evidence-accepted with those limits explicit.
- Frozen-ledger integrity and late identity discovery can conflict. A-001 was phone-matched to T-007 Cinnful Buns during repair. I preserved the linkage for downstream duplicate handling rather than silently merging or mutating the Phase 3 frozen set during evidence acceptance.
- Multi-location brands required three evidence scopes: company-wide process facts, branch-specific identity/status/rating facts, and explicit unknowns where production allocation differed by branch. Without that distinction, chain marketing could be incorrectly presented as local production evidence.
- Current official pages can themselves be stale or internally contradictory: `COMING SOON` pages for operating stores, order pages with all days closed, simultaneously displayed incompatible hours, placeholder phones, and sites still showing locations after announced closure. These required preserved conflicts rather than source-precedence shortcuts.
- Direct-to-file repair output was both reliable and substantially cheaper than response-then-copy. It preserved the worker response while avoiding a duplicate artifact-only turn and preventing very long repair text from flooding orchestration context.
- The acceptance ledger's useful unit is the candidate, but the field-state summary still needs compact prose because a single candidate may simultaneously contain documented, conflicting, and exhausted-unavailable fields. A scalar evidence state cannot express that without losing detail.

### Possible skill improvements

1. Define a bounded search-trail contract. Requiring every opened source and every query across five stages for every field turns acceptance into a near-complete rewrite. A compact per-candidate audit trail with one or more representative URLs/queries per stage would preserve auditability at much lower cost.
2. Permit or require a declared repair output path in Phase 5, and add `{OUTPUT_PATH}` to the Phase 4 canonical prompt. Direct-to-file returns removed one full turn per batch and kept large artifacts out of the conversation context.
3. Require candidate ID headings and exact field labels in the canonical worker response. Structural normalization should not consume a repair wave when the substantive evidence is already usable.
4. Define candidate-level `evidence-exhausted-unavailable` precisely: no independently attributable identity/location evidence after the full trail. Distinguish that from an evidence-accepted candidate with only chain-level facts and branch-specific unknowns.
5. Add explicit evidence-scope labels such as `company-wide`, `branch-specific`, `historical`, `factory`, and `store-local`. This would prevent chain process or centralized manufacturing evidence from leaking into branch claims.
6. Specify how late duplicate/identity discoveries interact with a frozen Phase 3 ledger. Recommended behavior: preserve the frozen ID, add a `possible_duplicate_of` or `identity_match` field, and defer merge/exclusion to the next decision phase.
7. Add guidance for stale-but-official pages and internally contradictory first-party sites. Official source precedence should not force silent resolution when the direct source is plainly stale or inconsistent with current independent evidence.
8. Provide a structured evidence-ledger schema with per-field state columns or a JSON sidecar. The current mixed field-state prose is auditable but difficult to aggregate mechanically.
9. Add a gate command/checklist for exact counts: candidate rows, accepted, exhausted, repair-requested, repair files, section totals, original-worker mapping, and premature judgment terms. This run caught and corrected a transient status-count arithmetic error by querying the ledgers directly.
10. Clarify whether an identity-thin mapped place with a verified name/address but no other facts is evidence-accepted or candidate-level exhausted. The current wording leaves a judgment call between partial identity evidence and terminal unavailability.

### Phase outcome

Passed all Phase 5 completion-gate items: all 313 returned records were semantically inspected, every rejected field received a specific repair request to the original worker, all repairs were re-reviewed by the primary orchestrator, conflicts remain preserved, and final states are 304 evidence-accepted plus 9 legitimately exhausted-unavailable. No qualification, disqualification, scoring, tiers, or recommendations were produced.

## Phase 6 — Scoring and classification

### What happened

- Re-read the Phase 6 scoring reference in full and kept all scoring, filtering, disqualification, tie, occasion, and confidence decisions with the primary orchestrator.
- Wrote a complete 313-ID disposition ledger to `06-decisions.md`. The mutually exclusive final dispositions are 43 rated survivors, 19 scratch-verified/rating-unconfirmed records, 6 scored-but-filtered records, 39 positive-evidence disqualifications, 7 status deferrals, 9 evidence-exhausted identities, and 190 not-scoreable records.
- Also retained Tous les Jours as a seventh scored calibration example while assigning its mutually exclusive final disposition to DQ because accepted evidence directly documents the franchise bake-off model.
- Scored S and I only where accepted evidence supported affirmative production/process and a defensible rating gate. Computed G mechanically, labeled every R/E/price datum as documented, estimated, contaminated, conflicting, or unverified, and did not average conflicting ratings.
- Created four presentation tiers for the 43 rated survivors and treated near-neighbors as tie bands rather than exact ranks. Kept home mode (G/rotation) separate from trip mode (S/variance), which elevates traditional and wholesale-standardized producers.
- At Phase 6 completion, applied the terminal rating-exhaustion rule rather than borrowing an older calibration rating, leaving All Purpose Bakehouse scratch-verified/rating-unconfirmed. The later user-triggered direct Maps re-review overturned the exhaustion finding with current evidence; see the post-run correction below.
- Used only positive adverse evidence for DQs: confirmed closure, manufacturer/resale status, documented centralized frozen/par-bake production, a proven duplicate/non-store record, or a verified out-of-catchment address. Temporary closures and status conflicts were deferred.
- Ran a count and uniqueness audit: the complete disposition section contains exactly 313 unique frozen candidate IDs, and every row cites its accepted original-plus-repair evidence packet.

### User corrections or interventions

- None during Phase 6. The user did not correct a score, tier, rating choice, disqualification, branch resolution, or occasion assignment.
- The ongoing diary request remained the only user-authored execution constraint added to the rubric workflow.

### Things the orchestrator had to figure out

- The rubric does not define a disposition for the very common case where Phase 5 accepts identity/menu evidence but neither process depth nor a usable rating supports scoring. I introduced `not-scoreable` and explicitly made it non-negative; 190 of 313 records landed there.
- The Phase 6 calibration table can conflict with the run-specific evidence state. The terminal rating-exhaustion invariant had to take precedence over an older calibration rating, while the calibration S/I anchor could still inform a clearly labeled estimate.
- A record can be analytically useful as a low-S calibration case and also meet a positive-evidence DQ rule. Tous les Jours exposed this overlap. I retained the calibration row but made DQ the single final disposition.
- Branch-level process leakage remained a major risk. Company-wide claims were not automatically assigned to every Harmons, Lee's, Great Harvest, Kneaders, hotel, resort, or confectionery branch; only branches with sufficient accepted branch-specific support were scored.
- `R≈4.3` is not operationally exact. I treated 4.3 as passing, preserved literal source conflicts, and used the direct/primary rating rather than averaging when a 4.1/4.4 conflict straddled the gate.
- Aggregate R contamination requires a status beyond documented/unverified. Ballerina Farm's rating covers the whole brand/store experience, and Tulie's café/service complaints contaminate aggregate R; both needed explicit contamination annotations rather than silent adjustment.
- The accepted evidence excerpts often support S/I better than E. I left E unverified rather than manufacturing a number when product-specific review text was too thin. This makes the trip-mode variance annotation structurally useful but still hypothesis-grade.
- A fixed numerical tier boundary and the rubric's ±8 G resolution rule are not the same thing. The top tier spans about 9 G points, so it is best described as a practical overlapping tie band, not an exact seven-way equality.

### Possible skill improvements

1. Add an explicit `not-scoreable` disposition for accepted identity/menu evidence that cannot support process scoring or the R gate. State that it is neither a low score nor a DQ.
2. Define precedence when a candidate is both a scored calibration case and positively disqualified. Recommended: retain the analytic score in a calibration appendix, but give the candidate one final DQ disposition.
3. State whether run-specific terminal rating exhaustion overrides ratings embedded in the rubric's historical calibration table. It should, unless the calibration rating is imported into Phase 5 with current source/date provenance.
4. Turn `R≈4.3` into an operational rule: specify inclusivity, decimal precision, direct-versus-aggregator hierarchy at the gate, and how to handle a source conflict that straddles the threshold.
5. Define a rating-contamination vocabulary and gate: `documented-aggregate-but-contaminated`, `R_baked estimated`, and `R_baked documented` should be distinct states rather than prose exceptions.
6. Add a branch-scoring matrix that separates brand-level process, branch-local production allocation, branch status, and branch rating. This would prevent both evidence leakage and needless duplication.
7. Specify the minimum evidence needed to estimate E. When Phase 5 captures only one or two product-review excerpts, `E unverified` should be the default rather than an approximate number.
8. Clarify how tier boundaries interact with the ±8 G resolution floor. A useful model would permit overlapping tie bands or require tiers to be formed from uncertainty intervals rather than fixed cut points.
9. Provide a standard decision-ledger schema and disposition enum. A machine-checkable table should include candidate ID, final disposition, positive DQ basis if any, S/I/G/R/E provenance states, home/trip occasion, confidence, and accepted evidence reference.
10. Add an explicit duplicate/non-store resolution rule for identities discovered after the Phase 3 freeze. Preserve the ID, cite the match, assign one final disposition, and never silently delete it.
11. Distinguish temporary closure, permanent closure, planned/not-yet-open, and live-page/status-conflict outcomes. Only confirmed permanent closure should be a closure DQ; the others need deferral states.
12. Consider a scoring-candidate prefilter after Phase 5 acceptance. Requiring a full hand-authored disposition for hundreds of identity-only directory leads is auditable, but a structured rule could classify the 190 non-scoreable records consistently before detailed S/I work.

### Phase outcome

Passed every Phase 6 completion-gate item. All 313 candidates have evidence-linked decisions; every DQ rests on positive evidence; sparse evidence was not converted to a low score; the primary orchestrator made every judgment; and product-only text was not used as process proof. The run is ready for report assembly.

## Phase 7 — Coverage audit and loop-backs

### What happened

- Re-read the Phase 7 audit and discovery/status references, then ran six fresh full omission challenges. Their yields were 6, 1, 1, 3, 1, and finally 0.
- Froze twelve additions as COV-001 through COV-012 and routed them through five Phase 4 evidence batches, Phase 5 semantic inspection, and primary-orchestrator Phase 6 decisions before each next audit pass. Eleven packets were accepted and Hearth & Crust ended legitimately evidence-exhausted; none required repair.
- The additions materially changed the result: Bohemian Baklava and Empanada.Co became rated survivors; Hi Crunchy Utah and High Altitude Bakeshop became scratch-verified/rating-unconfirmed; Argentina's Best Empanadas was scored but filtered below the rating gate. The remaining additions were not-scoreable or evidence-exhausted without adverse inference.
- The population was 325 unique IDs. At this intermediate correction point it contained 45 rated, 20 scratch-verified/rating-unconfirmed, 7 scored-but-filtered, 40 positive-evidence DQs, 7 deferred, 10 evidence-exhausted, and 196 not-scoreable. The later direct-place sweep changed these dispositions without changing the population.
- Kept the run's July 14 directory/date stable after midnight while recording sources with their actual July 15 access date where applicable.

### User corrections or interventions

- None during Phase 7. The user did not correct a candidate identity, omission decision, evidence state, score, or convergence decision.

### Things the orchestrator had to figure out

- A single repeat pass was nowhere near enough here: five successive audits still found legitimate omissions. Convergence needed to mean “repeat a genuinely full challenge until one whole fresh pass yields zero,” not merely “do a second pass.”
- The original discovery families under-covered filled pastries. One explicit empanada query exposed three current specialists together, showing that empanadas, pastelitos, kolaches, burek, meat pies, and hand pies need their own discovery family.
- Cultural-tradition queries also needed more granularity. High Altitude Bakeshop appeared only when Filipino terms such as ensaymada and pandesal were used, despite broad Asian and bakery searches earlier.
- A named market listing is enough to preserve a plausible producer identity and prevent silent omission, but not enough to establish process, ratings, or an independent current identity. Hearth & Crust correctly entered the loop and then terminally exhausted without a negative inference.
- The cafe/restaurant boundary needed an attributable-producer test. A venue selling pastries is not automatically a bakery producer when the baked goods are sourced or production cannot be assigned to it.
- Current-looking hosts and official pages can conflict with positive closure evidence; Moon Bakery illustrated why “official-looking” must not automatically mean current. Planned/crowdfunded concepts likewise are not operating additions.
- Phase 7 loop-backs require delta accounting across the candidate ledger, evidence ledger, batch index, repair log, decision totals, and manifest. The skill states the conceptual loop but not a compact artifact/status update recipe.
- Exact query wording must change on each pass. Repeating the same searches would test index stability, not challenge the discovery model from a new angle.

### Possible skill improvements

1. Add a required filled-pastry discovery family: empanada, pastelito, kolache, burek, meat pie, hand pie, samosa, and related local-language variants.
2. Add a cultural-tradition matrix that explicitly includes Filipino ensaymada/pandesal, Korean and Japanese pastry terms, Middle Eastern phyllo breads, and Spanish/Venezuelan/Argentine variants rather than relying on broad “ethnic bakery” queries.
3. Require at least one current-year local-press query and one exact specialist query per underrepresented family during Phase 2 and every coverage challenge.
4. State explicitly that a stable named market-vendor listing is sufficient to freeze a lead, followed by the normal terminal-exhaustion route if no independent identity survives.
5. Define the minimum public producer identity and the cafe/restaurant adjacency rule: include when bakery production is attributable; do not infer production from menu presence alone.
6. Provide a standard loop-back delta checklist covering candidate count, batch index, acceptance state, decision disposition, total-count reconciliation, audit yield, and manifest status.
7. Replace any implication of a single “second pass” with an explicit loop: run fresh full passes until one returns zero additions after all prior additions complete Phases 4–6.
8. Specify that the run date/path remains stable across midnight while individual source access dates use the actual access date.
9. Warn that broad maps/directories and OSM are strong starting sets but do not substitute for culture-, item-, market-, and current-press-specific discovery.

### Phase outcome

Passed the Phase 7 gate after six complete challenges. The final pass produced zero additions, all twelve earlier additions completed the required loop-back, every count reconciles at 325, and the limitations are stated as source convergence rather than an exhaustive census claim.

## Phase 8 — Reader-facing rendering

### What happened

- Read the Phase 8 rendering reference only after Phase 7 passed, then wrote the final result to `08-results.md`.
- Put four foodie occasions first and limited each to exactly three picks: bread, pastry-and-coffee, gift/showpiece, and one-item detour. Repeated a venue where its fit genuinely crossed occasions rather than forcing twelve unique names.
- Added a separate three-item rare-finds layer for Filipino ensaymada, Pacific-style meat pies/kekepua'a, and Mexican baklava. Each venue passed the scratch prerequisite; rarity was stated only for this surveyed market, never as a world or national superlative.
- Added practical timing/status cautions for House of Bread, Hawk & Sparrow, Empanada.Co, and small-producer sell-outs.
- Initially put a 45-venue rated ranking at the bottom; the first post-render correction removed Cumming's Studio Chocolates, and the second promoted All Purpose Bakehouse after direct rating verification, returning the corrected total to 45 bakery-qualified venues. The remaining 20 rating-unconfirmed producers are now visible in a separate unranked table.
- Included the required coverage statement: 283 raw discovery identities, 269 initial candidates, 44 targeted gap additions, a 313-ID freeze, 12 audit additions, and a final zero-yield pass at 325.
- Updated the manifest to `complete` and linked every standard artifact plus this diary.

### User corrections or interventions

- None during Phase 8. The user did not ask for a different occasion set, correct a venue fact, or request a rendering change before completion.

### Things the orchestrator had to figure out

- “Top three per occasion” requires fresh venue-by-occasion judgment; the combined score cannot simply be copied four times. Bread process, cafe suitability, gift presentation, and single-item distinctiveness reward different evidence.
- The rare-finds layer can legitimately include a scratch-verified venue without a usable aggregate rating, but it must be labeled as an adventurous item lead rather than smuggled into the quality-filtered recommendation list. High Altitude Bakeshop is the concrete case.
- The rendering rules simultaneously request a bottom S/I/G audit and prohibit internal rubric vocabulary in outward prose. I resolved that by retaining the numbers but translating the columns to `Scratch`, `Variety`, and `Combined`, with a short plain-language explanation.
- “Worth lingering” is partly an experience claim, while the evidence collection is strongly production-focused. I kept the language modest and chose venues with documented coffee/cafe formats rather than inventing atmosphere details.
- The rare-find address rule says to use a places/map directory, but accepted evidence already contained current producer and mapped-directory identities. Reusing that accepted evidence avoided introducing unreviewed Phase 8 facts.
- The final report needed status conflicts near the recommendations, not buried in the audit machinery. Same-day verification warnings are more useful to a reader than attempting to resolve contradictions that the evidence could not resolve.

### Possible skill improvements

1. Provide an explicit venue-by-occasion worksheet with recommended evidence fields for bread, cafe/linger, gift, and single-item-specialist fit. This would make the top-three selection reproducible without reducing it to the combined score.
2. Clarify whether rating-unconfirmed scratch producers are eligible for the rare-finds section. Recommended rule: yes, but label them as unranked item leads and disclose the missing quality filter.
3. Resolve the vocabulary tension by specifying reader-safe audit column labels while retaining the numerical axes. `Scratch`, `Repeat variety`, and `Combined estimate` work without exposing internal shorthand.
4. Add cafe-experience fields to evidence collection if “worth lingering” remains a required occasion: seating, coffee program, counter format, and review evidence about atmosphere. Do not infer these from a bakery name.
5. State whether the Phase 8 map/directory lookup may add address-only evidence after Phase 7, or whether all rare-find location pins must already exist in accepted evidence. The latter is cleaner for evidence immutability.
6. Provide a standard “before you drive” block for sell-out cadence, preorder requirements, conflicting hours, temporary-status conflicts, and pickup-location uncertainty.
7. Define whether the bottom audit table should include only rating-qualified survivors or also rating-unconfirmed scratch leads. At this stage the report displayed 45 rated bakery survivors plus 20 unranked leads; the later direct-place sweep updated those sections to 55 and 8.
8. Add a manifest template with the exact standard artifact names and link expectations. The current rule requires links to every artifact but does not provide a canonical list or Markdown-link format.

### Phase outcome

Passed the Phase 8 completion gate. All prior gates passed; every recommendation and caution is traceable to accepted evidence; the occasion, rare-find, timing, tie, audit, plain-language, and coverage rules are represented; and the run is complete.

## Post-run correction — category adjacency versus final eligibility

### What happened

- The user asked why Cumming's Studio Chocolates appeared in the final bakery audit table. Re-checking the accepted packet showed handmade small-batch chocolates, brittle, caramels, dipped fruit, and named chocolate inputs, but no bread, pastry, laminated goods, or other bakery production.
- I had correctly preserved it during broad adjacent-category discovery but incorrectly treated its strong confectionery process as sufficient for final bakery eligibility. I reclassified A-059 from rated survivor to positive-evidence category exclusion, removed it from `08-results.md`, and reconciled the final counts to 44 rated and 40 DQ across 325 candidates.
- Regenerated the PDF after correcting the Markdown report.

### User correction

- The user identified the category error directly: a chocolate shop without bakery production should not appear in the bakery ranking merely because its confectionery work is handmade and ambitious.

### Skill lesson

- Discovery inclusion and final eligibility are different gates. Adjacent categories should be researched generously to avoid missing a chocolatier that also makes serious pastry, but final bakery survival requires affirmative bakery production. Strong craft in an adjacent category is not a substitute.

### Possible skill improvement

- Add an explicit post-evidence category gate before scoring: `adjacent-category lead → verify bread, pastry, lamination, pâtisserie, or another defined bakery product produced in-house → only then score`. If absent, retain the research record as `category-adjacent exclusion`, not a low score and not a generic production DQ.

## Post-run correction — rating retrieval and visibility for new bakeries

### What happened

- The user asked where All Purpose Bakehouse was and then reported that its live Google Maps listing showed 129 reviews. The original evidence packet had checked Google/Maps-oriented search results but never successfully opened or extracted the direct place record, yet it declared rating exhaustion.
- A direct Google Maps place search on July 15 resolved the exact address and exposed a 4.8 rating; the user verified the live 129-review count. A separate current page displayed 5.0 from 32 Google-derived reviews. I preserved those as source-specific displays rather than averaging them.
- The rerun also recovered substantially better current process evidence than the original packet: a three-day croissant workflow with overnight fermentation, shaping and butter lamination; daily fresh production; physical descriptions of a shattering exterior and soft interior; and repeated early sell-outs.
- Promoted A-006 from scratch-verified/rating-unconfirmed to an A-tier rated survivor at S 81, I 65 and G 72.6. Updated the then-current counts to 45 rated and 20 rating-unconfirmed across 325 candidates; the later batch sweep superseded those counts.
- Added All Purpose to the pastry-and-coffee and single-item-detour top-three lists. Added a visible 20-entry unranked section for every remaining strong scratch producer without a dependable rating, then regenerated the PDF.

### User corrections

- The user supplied the missing direct-platform observation: Google Maps displayed 129 reviews.
- The user also corrected the rendering policy: strong new places with affirmative scratch evidence should not disappear merely because no rating can be found. Missing ratings may prevent a quality rank, but must not prevent visibility.

### Things the orchestrator had to figure out

- “Google/Maps-oriented search” is not equivalent to opening the exact Google Maps place. A terminal exhaustion claim is invalid when the search never reaches the direct record and the place is readily accessible by exact name and address.
- Search engines returned no rating result for several exact queries, while Google's map-search endpoint immediately exposed 4.8. Rating research needs a direct place-path fallback rather than treating ordinary web-search silence as exhaustion.
- New-business evidence changes quickly. All Purpose opened in early 2026 and accumulated enough reviews to clear the gate before this July run, but the first evidence pass missed the live state.
- Quality filtering and report visibility are separate decisions. A missing rating can block placement in a ranked top three, but a strong scratch producer belongs in a clearly labeled unranked watchlist.

### Possible skill improvements

1. Require direct place-record retrieval for Google Maps, Apple Maps, Yelp, or another primary rating platform before declaring rating exhaustion; “oriented” web queries do not count as opening the platform.
2. For new or highly visible venues, require a second exact-name-plus-address rating pass during Phase 7 or immediately before rendering because rating counts can change quickly.
3. Add a `rating-pending / strong scratch` reader section. Never make a rating threshold an invisibility gate; use it only to distinguish ranked recommendations from unranked leads.
4. Record direct platform place IDs and literal access dates in the evidence packet so rating checks are reproducible.
5. If a user supplies a live platform observation, record it explicitly as user-verified evidence and independently verify every field the available tools can expose.

## Post-run correction — direct-place sweep of every remaining unconfirmed bakery

### What happened

- The user asked for the All Purpose direct-place method to be applied to every other scratch-verified/rating-unconfirmed bakery. I queried all 20 by exact name, then retried unresolved candidates with their accepted address, locality, alias, or branch identity.
- The direct map-search place objects exposed exact ratings that ordinary Maps-oriented web searches had missed: Le Pain de Charlie 5.0, Flour Box 4.8, Mims 4.8, AmsterDam Delicious 5.0, Great Harvest Draper 4.4, JD Flannel Foothill 4.9, Nano's 4.8, City Cakes Midvale 4.4, and Eats 4.7.
- The Bakery at Zermatt still produced no distinct direct Google place object, but the required secondary exact-identity ranking search found a current 4.3/117 display at the correct 784 W Resort Dr identity. It also clears the gate.
- High Altitude Bakeshop returned an exact 2.3 rating. Its strong scratch evidence remains valid and visible, but the rating now positively fails the ranking gate.
- Flourish returned an exact 4.6 place record, but a current exact-address directory marks it closed. A rating record is not current-open evidence, so Flourish moved to status-deferred rather than into the rated set.
- Eight candidates remain rating-unconfirmed. Doughlene has an exact place record with no displayed rating. Salt Lake Sourdough, Tomodachi, Hi Crunchy, Sourdough Bruh, the current Salt Lake Argentina's Café branch, Artisan Bakery Utah, and Mad Dough did not return an attributable direct record. Unrelated, host, former-branch, and near-name results were explicitly rejected.
- Final counts are now 55 rated, 8 rating-unconfirmed, 8 scored-but-filtered, 40 positive-evidence DQs, 8 deferred, 10 evidence-exhausted, and 196 not-scoreable, totaling 325.

### User corrections and prompts

- The user required the direct-place query to be applied systematically to the other excluded bakeries rather than treating All Purpose as a one-off correction.
- During the sweep, the user observed that workers need a much tighter information-finding algorithm. This is correct: the worker phrase “search for ratings” permitted inconsistent stopping points and allowed ordinary result-page silence to masquerade as direct-platform exhaustion.

### Things the orchestrator had to figure out

- Exact identity must precede rating capture. A Salt Lake Sourdough address query returned The Daily Dough; a Hi Crunchy query returned Krispy Krunchy Chicken; and an Argentina's query returned a distinct former branch. All three ratings had to be rejected despite superficially plausible query matches.
- Service-area businesses can have valid direct place records without street addresses. Mims and AmsterDam Delicious therefore required name/category identity checks rather than an impossible address match.
- An exact place record can exist but contain no rating. Doughlene is different from `no exact record`, and the evidence state should preserve that distinction.
- Direct-place absence is not the end of rating research. The Zermatt case required a current exact-name/address secondary ranking query, which recovered a qualifying rating.
- A live rating and current operating status are separate fields. Flourish demonstrated why a worker must perform a status check after finding a rating rather than assuming the place object proves the bakery is open.
- Review counts are not always exposed by the direct response. Workers must record the literal star value and `count unavailable`, not infer a count or silently discard the rating.

### Possible skill improvement: mandatory identity-first rating algorithm

1. Build an identity tuple from accepted evidence: canonical name, aliases, exact address, phone, branch, category, and service-area/storefront state.
2. Query the direct platform in this order: exact name; exact name plus address; verified alias plus address or phone; exact name plus locality for service-area businesses.
3. For every returned object, record returned name, address/service-area state, category, rating, count if literally shown, stable place ID, query, and access date.
4. Apply an identity gate before copying any rating. Exact branch/address is strongest; service-area records require exact name/category corroboration. Reject host venues, former branches, near names, and unrelated categories explicitly.
5. Use four distinct terminal direct states: `exact-rated`, `exact-no-rating`, `no-exact-record`, and `identity-conflict`. A generic `not found` is inadequate.
6. When direct rating is absent, run exact-identity secondary ranking searches using name plus address/phone. Preserve each platform value independently and do not average.
7. Run a separate current-status check. A rating record cannot establish that the business is open; status conflicts produce deferral, not promotion or automatic DQ.
8. A worker may declare rating exhaustion only after returning the complete query/identity/rejection log. The orchestrator should reject packets that merely list “Google Maps-oriented” web queries.
9. Before rendering, rerun this sequence for every scratch-verified/rating-unconfirmed candidate as a batch invariant, not only for prominent or user-mentioned businesses.

### Render and validation note

- The first regenerated PDF exposed a separate rendering failure: the 55-row audit table remained inside an HTML `<details>` block, and the Typst path treated the table as an unbreakable object. The lower rows overlapped at the page footer even though text extraction and Markdown row counts looked correct.
- I removed the disclosure wrapper, divided the audit into three continued tables, regenerated the PDF, and visually inspected all three audit pages. The final PDF is seven letter-size pages with 55 rated rows and 8 unconfirmed rows rendered without overlap.
- Skill/command lesson: PDF validation cannot stop at successful compilation or text extraction. Long tables require rendered-page inspection, and HTML disclosure wrappers should be removed or split before Typst conversion.

## Post-run correction — storefront access versus craft score

### What happened

- The user pointed out that microbakeries without storefronts should not occupy the main bread or other practical top lists. They are difficult to obtain, may operate only through occasional drops or preorders, and sometimes stop baking without their static web pages changing.
- The concrete failure was House of Bread: it ranked first in the bread list from craft evidence, but the user reported that it is currently on hiatus. Its static first-party page still describes weekend Instagram drops and therefore looked operational when read without a current social/status check.
- I removed House of Bread and Le Pain de Charlie from the main bread list and restored three reliably visitable choices: Leavity Bread & Coffee, Hawk & Sparrow, and Table X Bread.
- I removed service-area AmsterDam Delicious from the main rare-finds list and replaced it with a stable storefront item, fresh flatbread at Middle Eastern Bakery & Groceries.
- Added a dedicated availability-sensitive section for House of Bread, Le Pain de Charlie, Flour Box, Mims, AmsterDam Delicious, Pie Party, Dough Lady, Auntie Em's, and Red Bicycle Breadworks. Their craft/rating records remain in the audit, but they are no longer presented as spontaneous destinations.

### User correction

- House of Bread is currently on hiatus, user-verified July 15, 2026.
- More broadly, the user corrected the presentation rule: a high craft score does not make a no-storefront producer a useful “go here” recommendation.

### Things the orchestrator had to figure out

- `Current identity` and `current purchasability` are separate evidence fields. A live site, valid rating, and excellent process evidence can coexist with no active bake.
- Access format is not a quality penalty. Microbakeries should keep their evidence-based S/I/G and rating disposition, but presentation must separate them from stable walk-in businesses.
- The practical recommendation gate needs at least one dependable acquisition path: public storefront hours, a current recurring market schedule, a currently open preorder window, or a verified active stockist. A mapped home address or service-area place record is not enough.
- Static producer instructions are especially dangerous for intermittent businesses. The final check must inspect the latest dated operating channel, and an inaccessible or stale channel should produce an availability warning rather than an assumption of normal operation.

### Possible skill improvements

1. Add an `access format` field to every accepted packet: `storefront`, `recurring market`, `active preorder`, `service-area/delivery`, `wholesale/stockist`, `home microbakery`, or `unknown`.
2. Add a separate `current acquisition evidence` field with source, literal date, and state: `walk-in active`, `drop active`, `preorder active`, `hiatus`, `closed`, `conflicting`, or `unverified`.
3. Gate main occasion/top-three lists on stable customer access, not craft score alone. No-storefront, wholesale, and irregular producers belong in an availability-sensitive watchlist unless a current recurring acquisition path is verified.
4. Require a latest-post/status check for microbakeries immediately before rendering. Static websites and old market calendars cannot establish current activity.
5. Keep access out of S/I/G. Report it as an orthogonal practical constraint so difficult availability does not get mislabeled as inferior baking.

## Post-run interactive website

### What happened

- The user requested a three-pane website: faceted search at left, matching bakeries in the center, and a map of the filtered/selected set at right. I loaded the user's `gisthost` command and built a self-contained `index.html` inside the run directory.
- Embedded 65 visible records: 55 rated survivors, 8 scratch-verified/rating-unconfirmed leads, High Altitude's below-gate record, and Flourish's status-conflict record. The interface supports text search, status/area/access/specialty facets, minimum-rating filtering, three sort modes, persistent browser-local shortlisting, and synchronized list/map selection.
- Direct place records supplied coordinates for public storefronts and mapped public pickup/stockist locations. I intentionally omitted private home-microbakery addresses and invalid service-area coordinates; those records remain searchable and explicitly show `No public map pin`.
- Added responsive behavior after browser testing exposed that the initial mobile layout hid the facets without an opener. The final version has separate mobile `Filters` and `Map/List` controls.
- Published the validated HTML as a public GitHub Gist and verified the rendered Gist Host page: https://gisthost.github.io/?2c51f1ba56360b4f8f0ecd6a2990a4d9

### Validation

- HTML parsing and inline JavaScript syntax checks passed.
- Playwright loaded all 65 cards with zero page errors; 52 public map pins rendered. Searching `croissant` returned 3 matches, filtering Park City returned 4, and shortlist persistence updated correctly.
- Desktop and mobile screenshots were visually inspected. Mobile filter-drawer and map/list switching were exercised programmatically. The published Gist Host page returned HTTP 200 and matched the validated local rendering.

### Skill/command lesson

- Interactive output needs a privacy-aware map contract: map public customer locations, not inferred home-production addresses. Service-area coordinate centroids can be wildly invalid and must be rejected.
- Browser validation should cover both rendering and interaction. Static HTML/JavaScript parsing would not have caught the missing mobile facet opener.

### User correction: directions place identity

- The initial `Directions` links searched Google Maps using only the street address. The user pointed out that an address-only location search may open the location without loading the bakery's Google Maps place card.
- Updated each mapped bakery link to search for the canonical bakery name and address together. Interactive location links should carry place identity, not coordinates or address alone, when the intended destination is a business listing.

### User correction: map-to-list navigation

- Selecting a map pin highlighted the corresponding result, but clicking its popup did not bring that result card into view. The user asked for the popup itself to show the card.
- Turned each popup into a keyboard-accessible `Show card` control. On desktop it selects, focuses, and scrolls the matching center card into view; on narrow/mobile layouts it also closes the map overlay and returns to the list before revealing the card.
- A synchronized map/list interface needs explicit two-way navigation. Shared selection state alone is insufficient when the selected record can remain off-screen or behind a mobile overlay.

### User correction: Argentina's Café rating in the screenshot

- The user supplied a screenshot of the current Google Maps place card for `Argentinas Cafe`, showing 4.5 stars from 336 reviews. I saw the screenshot while fixing map-to-list navigation but initially treated it only as confirmation that the name-plus-address link opened a business card; I failed to apply the rating evidence.
- The corrected Maps query used the canonical name plus `655 E 400 S`, resolving the current café rather than Argentina's Best Empanadas at the former `357 S 200 E` identity whose 3.9 result had correctly been rejected earlier.
- Promoted P3-004 from rating-unconfirmed to a Tier B rated survivor at S 68, I 61, G 64.4, R 4.5 (336). Current final counts are 56 rated, 7 rating-unconfirmed, 8 scored-but-filtered, 40 positive-evidence DQs, 8 deferred, 10 evidence-exhausted, and 196 not-scoreable, totaling 325.
- Visual user evidence must be read for all material fields, not merely the field relevant to the immediately preceding UI change. When a screenshot exposes exact identity, rating, count, category, and price band, each field should be checked against the current record before continuing.

## Interactive website implementation blueprint for later skill extraction

This is a reproducible handoff, not merely a description of the finished page. A later SKILL-authoring session should inspect this section together with `index.html`, `08-results.md`, `06-decisions.md`, and the two post-run rating correction files. The implementation used no build system: one static HTML file contains the markup, CSS, dataset, and JavaScript, while Leaflet and OpenStreetMap tiles are loaded from public CDNs.

### Inputs and inclusion boundary

- Build the website only after the final decision and access states are stable. The visible set is not every discovered candidate and is narrower than the report audit: include currently obtainable rated survivors, currently obtainable scratch-verified/rating-unconfirmed leads, and any explicitly useful currently open below-gate record. Exclude confirmed closure/hiatus, current-status conflicts, and records whose current activity cannot be verified.
- After the Feldman's addition and availability correction, this run's website contains 61 records: 55 currently obtainable rated survivors, 5 currently obtainable rating-unconfirmed leads, and one open below-rating-gate scratch lead. The full report still preserves all 57 rated survivors and 7 unconfirmed records, including unavailable audit rows.
- Treat `06-decisions.md` as the source for scores, rating disposition, and tier; use `08-results.md` for reader-facing descriptions and practical framing; use accepted evidence or explicit post-run corrections for address, current access, rating count, and map identity. Do not infer missing website facts during rendering.
- Preserve the full visible set in the embedded data even though the prose report shows only top-three occasion recommendations. The website is an explorer over the qualified audit set, not a graphical copy of only the short list.

### Embedded record contract

Each JavaScript record in `index.html` has these fields:

| Field | Meaning |
| --- | --- |
| `n` | Canonical display name, including branch label when needed for identity |
| `s` | Scratch/production score |
| `v` | Interestingness/variety score; named `v` in the page to avoid exposing rubric terminology in labels |
| `g` | Computed combined score |
| `r` | Literal accepted rating, or `null` when unconfirmed |
| `tier` | `A`, `B`, `C`, `D`, or `—` for non-tiered records |
| `status` | Underlying decision state such as `Rated`, `Rating unconfirmed`, `Below rating gate`, or `Status conflict`; current-status conflicts are filtered out before website embedding |
| `region` | One normalized geographic facet value |
| `access` | One normalized customer-access facet value |
| `type` | One normalized specialty facet value |
| `a` | Public-facing location text; use an omission label rather than a private address |
| `lat`, `lng` | Public customer-location coordinates, or `null`/`null` when no safe valid pin exists |
| `note` | Short plain-language reason to care plus the most important caveat |

Facet values are controlled vocabularies declared once in `options`: evidence status; region (`Salt Lake City`, `East bench`, `Salt Lake Valley`, `Park City`, `Heber & Midway`); access (`Walk-in`, `Preorder / market`, `Delivery / service area`, `Wholesale / stockist`); and specialty (`Bread`, `Pastry & patisserie`, `Doughnuts`, `Bagels & savory`, `Pies`, `Cookies & sweets`, `Cakes & cheesecake`, `Regional specialty`, `Gluten-free / vegan`). Normalize records into these values rather than creating near-duplicate facet labels. `Hiatus / unverified` may remain an audit vocabulary but must not be an interactive place-finder facet because those records are excluded before embedding.

### Page structure and visual layout

- Use a persistent header for title, short scope label, search, result count, and sort control.
- Use a three-column desktop grid: facet controls at left, a vertically scrolling result list in the center, and a map at right. Keep the map available while the center list scrolls so selection context is not lost.
- Give each card the bakery name, public location, tier or evidence-state badge, access badge, specialty badge, concise note, combined/scratch/rating metrics, shortlist control, and directions link or `No public map pin` label.
- Use a warm but restrained bakery visual system rather than generic dashboard styling: serif headings, warm off-white background, rust/gold/sage accents, clear selected-card border, and high-contrast controls. Keep the map visually quieter than the list.
- At widths below 1050 px, turn the map into a full-screen overlay opened by a `Map` button. At widths below 720 px, turn the facets into a drawer opened by a separate `Filters` button. The initial mobile version failed because it hid the facet column without providing an opener; responsive hiding must always have a visible inverse action.

### Filtering, sorting, and state

- Store selected facet values in `Set` objects. Apply OR within each facet and AND across different facets. Text search covers name, address/location label, note, specialty, and region.
- Recalculate the number beside every facet as an alternate-facet count: when counting one facet, apply all active filters except that facet. This lets the user see useful next choices rather than counts that collapse to zero merely because a sibling value is selected.
- Support a minimum-rating floor, but exclude `null` ratings when the floor is nonzero. Do not coerce missing ratings to zero in the visible record or presentation.
- Support combined-score descending, rating descending with combined-score tie-break, and alphabetical sorting. Default to combined score.
- Persist the shortlist as canonical bakery names in `localStorage`. Provide a shortlist-only filter and a visible saved count. This state is local to the browser and is not published or transmitted.
- Escape every dataset-derived string before inserting it into HTML. The implementation uses a small `esc()` function for `&`, `<`, `>`, quotes, and apostrophes.

### Map creation and privacy contract

- Use Leaflet with OpenStreetMap tiles. Render only coordinates for public customer destinations: storefronts, recurring public markets, or verified public stockists/pickup counters.
- Never map a private home-production address merely because a directory or direct-place record exposes it. Do not map service-area centroids; they can resolve far outside the actual service area. For either case, retain the searchable record with `lat:null`, `lng:null`, safe location text such as `Home microbakery — address omitted`, and the `No public map pin` UI.
- Obtain coordinates from an identity-matched direct place record or other accepted mapped identity. Coordinate retrieval is not permission to import a new rating, status, address, or branch identity without applying the normal evidence gate.
- Rebuild the marker layer from the currently filtered list. Show the filtered mapped count. Fit bounds only when no bakery is actively selected; otherwise preserve the user's selection context.
- Color pins by tier and use a neutral marker for unranked/caution states. A pin click selects the bakery and opens a popup; selection updates both pin size/color treatment and the corresponding card border.

### Two-way list/map interaction

- Clicking a result card with a public pin selects it, enlarges/highlights its marker, flies the map to it, and opens the popup. Card controls such as shortlist and directions must stop that selection behavior.
- Make the popup itself a real keyboard-accessible button with an explicit `Show card` affordance. Shared selected state is not enough: a selected card may be outside the center pane's viewport.
- Clicking `Show card` selects the record, finds the card by canonical name, scrolls it to the center of the results pane, and moves focus to it. Cards therefore use `tabindex="-1"` so programmatic focus works without adding every card to the normal tab sequence.
- On narrow/mobile layouts, popup activation first closes the map overlay, changes the toggle label back to `Map`, then scrolls and focuses the card in the list. Test this transition separately from the desktop scroll behavior.

### Directions identity rule

- Build Google Maps links with the Maps Search URL and the query `canonical bakery name, public address`, URL-encoded:

  `https://www.google.com/maps/search/?api=1&query=<NAME%2C%20ADDRESS>`

- Do not query only the address or only coordinates. An address-only search can open a location without loading the business place card; name plus address carries both destination and place identity.
- Omit the directions link when there is no safe public map location. Do not transform an omitted home address into directions through coordinates.

### Validation matrix

Run validation before first publication and after every material data or interaction change:

1. Parse the HTML and run `node --check` on the inline JavaScript.
2. Serve the run directory locally over HTTP; do not rely on opening the file directly because CDN, storage, and browser behavior can differ.
3. Load the page in a real headless browser and fail on any `pageerror`.
4. Assert the total visible record count and disposition facet counts against an explicit website-eligibility projection of the final decision ledger, not the full audit totals. After the Feldman's and availability corrections these checks are 61 total, 55 rated, 5 rating-unconfirmed, and 1 below-rating-gate.
5. Exercise text search with a known item, a region facet, minimum rating, all sort modes, shortlist add/remove and persistence, reset, and an empty-result state.
6. Confirm that the mapped count equals records with non-null safe coordinates; this run has 52 public pins.
7. Test list-to-map selection and popup-to-card navigation on desktop. Assert selected styling, popup state, card focus, and that the card is inside the visible center-pane bounds.
8. Repeat popup-to-card navigation at a mobile viewport. Assert that the map overlay closes, the toggle returns to `Map`, and the card is selected and focused. Exercise the facet drawer and its backdrop separately.
9. Visually inspect desktop and mobile screenshots for overlap, clipped controls, illegible cards, inaccessible drawers, and map overlays covering required navigation.
10. After publishing, run the same targeted browser assertion against the Gist Host URL. Do not equate HTTP 200 with a correct or current app.

When the user supplies a screenshot during validation, inspect every material field it reveals—identity, branch/address, rating, count, category, price band, status—not only the UI behavior currently under discussion. This run initially missed the Argentina's Café rating because the screenshot was read too narrowly as proof that the directions query opened a place card.

### Publication and update procedure

- Keep `index.html` inside the run directory and link it from `00-run-manifest.md`. Verify the file contains no secrets, private addresses, or unpublished data before creating a public gist.
- Follow `reference/gisthost.md`: verify `gh` is installed/authenticated, publish `index.html` as a public gist, return both the Gist Host URL and underlying gist URL, and verify the rendered host in a browser.
- For later revisions, update the existing gist rather than creating a new URL. `gh gist edit <GIST_ID> index.html` expects the local file to exist under that name in the current directory, so run it from the directory containing `index.html`.
- Expect brief Gist Host caching, but verify rather than assuming. In this run the Gist REST API returned repeated HTTP 503 responses during one update. The fallback was to clone the gist's Git repository, confirm its diff against the validated local file, commit the exact change, configure Git to use the existing authenticated `gh` credential helper with `gh auth setup-git`, push, and then re-run the hosted browser assertion.
- Record the published URL, validation results, privacy decisions, user corrections, and any deployment fallback in the diary. The website is a derived Phase 8 artifact and must remain traceable to the final evidence/disposition state.

### Candidate instructions for the future SKILL session

The future SKILL session should decide whether this belongs directly in `phase-8-rendering.md`, in a one-level reference loaded only when interactive HTML is requested, or partly in a reusable HTML asset/script. The fragile, low-freedom pieces are the website-eligibility projection, record contract, privacy gate, name-plus-address directions query, two-way popup/card behavior, count assertions, mobile validation, and hosted verification. Styling and exact facet taxonomy can remain adaptable to the market and user request.

## Post-run discovery correction: Feldman's Deli bagels

### User correction

- The user asked whether Feldman's has bagels. It does, and Feldman's Deli is absent from the entire candidate ledger rather than merely missing a bagel tag in the website.
- The current official site describes `fresh-baked bagels` and shows assorted bagels, a breakfast bagel sandwich, and bagel with lox and cream cheese. A Salt Lake Tribune bagel survey calls them house-made. Historical operator reporting says Janet Feldman made a limited daily batch at the deli, boiled first and then baked. Recent 2026 coverage describes a limited number of hand-rolled breakfast bagels.
- These sources make Feldman's a strong omitted discovery candidate with meaningful scratch evidence. They do not authorize silently adding a rated survivor: current direct-place rating/count, current branch identity, access, and the exact current production packet still need the normal Phase 4–6 acceptance and decision path.

### Skill lesson

- Adjacent-category discovery cannot stop at businesses labeled bakery, café, or bagel shop. A deli can contain qualifying scratch bakery production even when sandwiches dominate its identity and search results.
- Marker-item searches should combine the product with adjacent venue categories—for example `house-made bagels deli`, `boiled bagels Jewish deli`, and current local best-bagel coverage—then feed newly found venues through the full evidence gate.
- Coverage convergence failed here despite the rubric already naming adjacent-category searches. Future discovery checks need an explicit reconciliation against current local item roundups and reader/user-known category anchors, with every named venue either present in the ledger or recorded as an identity-level exclusion.

## Feldman's full loop-back and website availability correction

### What happened

- At the user's request, Feldman's became COV-013 and completed the same evidence path as other coverage additions. The canonical Phase 4 worker packet documented the exact storefront, current access/hours, multiple platform-specific ratings, current 2025 hand-rolling quantities, historical boil-and-bake/process development, physical review evidence, and adverse sourcing facts.
- Primary-orchestrator Phase 5 inspection rejected one field: the packet called a Google-attributed Wanderlog reproduction a direct Google result. The original worker repaired only that defect, resolving exact name, name-plus-address, and alias-plus-phone queries to Google CID `6572009753018553191`, direct rating 4.7, and explicit `count-unavailable`.
- I scored Feldman's as S 74, I 42, G 55.7, D tier. Only the limited daily bagel production passed the bakery gate; sandwiches, externally baked rye, and shipped desserts received no bakery-process credit. It entered the full audit as the 57th rated survivor and increased the canonical population from 325 to 326.
- The user then corrected the website's purpose: House of Bread and other not-open bakeries should not appear in an interactive place finder. I removed House of Bread (confirmed hiatus), Le Pain de Charlie (no verified current ordering cadence), Flourish (current closure conflict), Artisan Bakery Utah (current location/activity unverified), and Mad Dough (current activity unverified). Feldman's was added because current walk-in acquisition is verified.
- The website now contains 61 currently obtainable records rather than mirroring all 66 report-visible audit records. Its state counts are 55 rated, 5 rating-unconfirmed, and 1 below-rating-gate; the full report retains unavailable records for evidence transparency.

### Skill lessons

- Separate `audit visibility` from `interactive place-finder eligibility`. A record can remain an important scored or unconfirmed audit row while being excluded from a tool whose primary action is deciding where to go.
- Build a website eligibility projection before serialization: require current open/obtainable evidence; exclude `hiatus`, `closed`, `conflicting`, and `unverified current activity`; then assert website counts against that projection rather than against the full disposition ledger.
- Do not let a high score, valid historical process record, live static site, or surviving rating override current acquisition state. Availability is an orthogonal hard gate for a place-finder.
- Direct-place provenance must distinguish the direct platform object from an aggregator's attributed copy. An attributed count can remain secondary evidence, but it cannot satisfy a direct-place contract.

### User correction: independent list scrolling

- The result pane declared `overflow:auto`, but the outer app used `min-height:100%`. With the full result set, the grid could grow beyond the viewport, causing page-level scrolling and moving the map along with the list.
- Changed the app shell to `height:100%`, `min-height:0`, `overflow:hidden`, and grid rows `auto minmax(0,1fr)`. Added `overflow:hidden` to the layout row while retaining independent `overflow:auto` on the facets and result panes.
- A three-pane app must be validated behaviorally: scroll the center pane, then assert that its `scrollTop` changed while `window.scrollY`, the map pane's top coordinate, and the map pane's height remained unchanged. Merely seeing `overflow:auto` in CSS does not prove independent scrolling when an ancestor can expand.
- The final browser check passed at 1440×900: center-pane `scrollTop` changed from 0 to 1,100 while `window.scrollY` stayed 0 and the map remained fixed at top 83 px with height 817 px. A 390×844 regression also passed: the result pane scrolled 600 px, page scroll stayed 0, the mobile map remained closed by default, all 61 cards rendered, and there were no page errors.
- After deployment, the same behavioral check passed against the public Gist Host page: 61 cards rendered, Feldman's was present, all five unavailable or unverified businesses were absent, the center pane scrolled 900 px without moving or resizing the map, and no browser errors occurred.
