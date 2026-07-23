# Restaurant rubric run manifest

- Invoked category: restaurant
- Original user request: "let's run restaurant-rubric/SKILL.md against all restaurants within a 30 minute drive of my house in East MillCreek [Image #1]"
- Canonical requested location: 2958 South 2520 East, Millcreek, Utah 84109, United States
- Created from frozen 2026-07-15 evidence: 2026-07-21
- Run directory: `/Users/kylemathews/programs/scratch-food-rubrics/2026-07-21-east-millcreek-utah-30-minute-drive-rescore`
- Status: v8.14 rescore complete

## Standard artifacts

- Scope and drive-time boundary: [01-scope.md](./01-scope.md)
- Discovery queries and coverage history: [02-query-log.md](./02-query-log.md)
- Raw discovery ledger: [02-discovery-ledger.md](./02-discovery-ledger.md)
- Canonical candidate ledger: [03-candidate-ledger.md](./03-candidate-ledger.md)
- User-approved novelty triage: [03-user-novelty-triage.md](./03-user-novelty-triage.md)
- Evidence-return index: [04-worker-returns/index.md](./04-worker-returns/index.md)
- Accepted/exhausted evidence ledger: [05-evidence-ledger.md](./05-evidence-ledger.md)
- Evidence repair log: [05-repair-log.md](./05-repair-log.md)
- Canonical v8.14 decision ledger: [06-decisions.json](./06-decisions.json)
- Legacy v8.10 decision ledger: [06-decisions.legacy-v8.10.json](./06-decisions.legacy-v8.10.json)
- Rescore validator result: [06-rescore-validation.json](./06-rescore-validation.json)
- Identity and projection repair result: [06-interactive-repair-validation.json](./06-interactive-repair-validation.json)
- Coverage audit and zero-yield gate: [07-coverage-audit.md](./07-coverage-audit.md)
- Reader-facing results: [08-results.md](./08-results.md)
- Interactive faceted website: [index.html](./index.html)
- Static and browser validation: [interactive-results-validation.json](./interactive-results-validation.json)
- Test-run diary: [diary.md](./diary.md)
- Reproducible v8.14 migration: [rescore_v814.rb](./rescore_v814.rb)
- Reproducible identity/projection repair: [repair_interactive_v814.py](./repair_interactive_v814.py)
- Reproducible v8.14 audit renderer: [render_rescore_v814.rb](./render_rescore_v814.rb)

## Final verified counts

- Broad map-derived survey rows: 2,886
- Targeted discovery rows: 70
- Source union before canonical deduplication: 2,956
- Coverage-audit additions: 6
- Final evidence records: 1,650 unique IDs
- Final decisions: 1,650 unique IDs
- Complete new-basis score rows: 207
- Complete rows eligible for the G ranking: 190
- Complete rows kept outside the G ranking: 17
- Scratch-eligible partial score rows: 444
- Evidence-exhausted/no-score rows: 906
- Legacy scalar-only rows moved to partial pending criterion-level re-review: 19
- Last full coverage-pass yield: 0
- Interactive practical records: 224
- Interactive audit records: 1,426
- Practical records with map coordinates: 221

## v8.14 rescore basis

- Menu turnover was removed from `S_scratch` and retained only in `I`.
- The 207 recoverable legacy criterion vectors were remapped from the retained 20/30/15/10 axes to the new 25/40/20/15 axes; the retired 25-point volatility criterion was discarded.
- Accepted current production evidence now earns a non-normalized criterion-level partial score when other criteria remain unknown.
- The 19 legacy scalar-only anchors were not carried forward as complete scores because their turnover contribution could not be separated defensibly.
- Canonical identity fields were restored from the frozen candidate source for 1,644 of 1,650 decisions; the six later coverage additions retain their accepted evidence identity.
- Validator hashes and deterministic results are recorded in `06-rescore-validation.json`, `06-interactive-repair-validation.json`, and `interactive-results-validation.json`.
