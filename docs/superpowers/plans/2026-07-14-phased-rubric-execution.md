# Phased Rubric Execution Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refactor both food-search skills into mission-grounded roots plus just-in-time phases, add broad-plus-targeted multilingual discovery, and enforce verbatim evidence-only worker prompts without changing either calibrated rubric.

**Architecture:** Shared references own Phases 1–5 and 7. Each category owns discovery vocabulary, its canonical worker prompt, unchanged scoring/calibration material, and unchanged rendering rules. The primary agent loads each phase immediately before use, attests its gate, and remains the sole judgment layer.

**Tech Stack:** Markdown, Python migration/assertion snippets, shell, Git, Prettier.

## Global Constraints

- Preserve every scoring definition, weight, threshold, formula, gate, band, calibration conclusion, occasion, rare-find rule, rating rule, confidence semantic, and tie behavior.
- No executable harness, JSON schema, dependency, or `scratch-food-finder` change.
- Primary agent remains orchestrator; workers retrieve evidence only.
- Canonical prompts are verbatim; only declared placeholders change.
- Broad popularity-neutral and adaptive targeted discovery are both mandatory.
- Missing evidence never becomes negative evidence.
- Prefer messaging/resuming the original worker for repair when supported.
- No reader-facing recommendations until every earlier gate passes.
- Both skills move together to `v8.9`.
- Leave the untracked design PDF alone.

## File Map

Create shared files `reference/shared-status-and-provenance.md`, `reference/phase-{1-scope-and-catchment,2-candidate-discovery,3-discovery-convergence,4-evidence-research,5-evidence-acceptance,7-coverage-audit}.md`.

Create in both category directories: `discovery-reference.md`, `phase-4-worker-prompt.md`, `phase-6-scoring.md`, `phase-8-rendering.md`. Modify both `SKILL.md` roots and `README.md`. Create `docs/superpowers/reports/2026-07-14-phased-rubric-regression-check.md`.

---

### Task 1: Shared status and phase-gate contract

**Files:**

- Create: `reference/shared-status-and-provenance.md`

**Interfaces:**

- Produces shared ledger/state vocabulary used by every phase.

- [ ] **Step 1: Create the contract**

Write these exact sections:

```markdown
# Shared Status, Provenance, and Completion Contract

## Non-negotiable semantics

Missing evidence is a research state, never evidence against scratch. Product nouns establish what is sold, not how it was produced. DQ requires positive evidence. Search rank, popularity, format, cuisine, language, and directory category do not establish scratch. Preserve URL, source type, access date, and quotation.

## Candidate ledger

One canonical row: `candidate_id`, identity/address/phone/domain, aliases/local-script names, category, all discovery sources and exact queries, coverage dimensions, state, original `worker_ref`, evidence record, orchestrator decision. Deduplication merges provenance.

## Candidate states

`candidate-discovered`, `evidence-researching`, `evidence-returned`, `repair-requested`, `conflict-verification`, `evidence-accepted`, `evidence-exhausted-unavailable`, `orchestrator-decided`, `coverage-addition`, `rendered`. `unresolved`, `thin`, or blank is non-terminal.

## Per-field evidence states

`documented`, `product-only`, `thin-repair-required`, `conflicting`, `exhausted-unavailable`, `unsearched`. Define each literally; exhaustion requires completed source sequence and trail.

## Number provenance

Every number is `documented`, `estimated` by the primary orchestrator where permitted, or `unverified`. Never average conflicting ratings; preserve value, count, platform, and date.

## Worker-return rule

A row proves only response, not acceptance. Primary orchestrator checks every venue semantically. Row-count acceptance is forbidden.

## Completion-gate protocol

Enumerate every printed item; mark ✅/❌; cite counts, queries, candidate IDs, worker refs, records, or decisions; remain if any ❌; show concise checklist without recommendations. A limitation waives only an item that explicitly permits it.
```

- [ ] **Step 2: Format, verify, commit**

```bash
prettier --write reference/shared-status-and-provenance.md
rg -n '^## (Candidate states|Per-field evidence states|Number provenance|Completion-gate protocol)$' reference/shared-status-and-provenance.md
! rg -n 'missing evidence.*(low score|zero)|row count.*accepted' reference/shared-status-and-provenance.md
git add reference/shared-status-and-provenance.md
git -c commit.gpgsign=false commit -m "docs: define rubric evidence and completion contract"
```

Expected: four headings; forbidden scan empty.

---

### Task 2: Shared scope, discovery, and convergence phases

**Files:** Create `reference/phase-1-scope-and-catchment.md`, `phase-2-candidate-discovery.md`, `phase-3-discovery-convergence.md`.

**Interfaces:** Consume category `discovery-reference.md`; produce frozen deduplicated ledger.

- [ ] **Step 1: Write Phase 1**

Include `# Phase 1 — Scope and Catchment`, input, required actions, prohibitions, output, completion gate. Required actions: resolve country/region/local script and region pin; resident-normal catchment; prefer real OSM polygon via `map_to_area` and verify non-zero; standalone town may use 15–20-minute rural ring; metro town must not annex neighboring towns; corridor/valley gets explicit components; record exclusions/method/uncertainty; narrow infeasible scope explicitly now. Gate checks each item.

- [ ] **Step 2: Write Phase 2**

Include `# Phase 2 — Candidate Discovery`; require fresh reading of shared status and category discovery file. Define:

```markdown
## Track A — Broad popularity-neutral survey (MUST run)

Whole catchment via OSM/Overpass or equivalent, full tags, adjacent categories, partition/union large markets; systematic fallback logged and never called census.

## Track B — Adaptive targeted discovery (MUST run)

Derive local languages/scripts and natural terms. Log queries for best/top/award/guide; scratch/house-made/raw; ambitious/chef-/baker-led/artisan/seasonal/technical; neighborhoods; cuisines/traditions/formats; marker items and techniques; recent/new/renamed/moved/pop-up/market/cottage/preorder/informal. Use relevant local scripts. Results create candidates only.

## Track C — Visible-head challenge (MUST run)

Local publications, major place results, guides/awards, roundups, recent openings.
```

Candidate handling adds all leads and provenance but never DQs/scores. Gate checks all tracks, languages, marker queries, ledger counts, and no scoring.

- [ ] **Step 3: Write Phase 3**

Include normalization by names/local scripts/address/coordinates/phone/domain/branches/renames/relocations; preserve all provenance. Coverage grid: geography, language/script, cuisine/tradition, format, specialist/broad, established/new. Empty cells trigger query or explanation. Require a fresh gap pass and repeat until zero new candidates or precise source limit; forbid “complete census.” Gate reports union, duplicates, grid, last-pass yield, limitation, frozen IDs.

- [ ] **Step 4: Format, verify, commit**

```bash
prettier --write reference/phase-{1-scope-and-catchment,2-candidate-discovery,3-discovery-convergence}.md
for f in reference/phase-{1-scope-and-catchment,2-candidate-discovery,3-discovery-convergence}.md; do rg -q '^## Completion gate$' "$f"; done
rg -n 'Track A|Track B|Track C|languages/scripts|zero new' reference/phase-{2-candidate-discovery,3-discovery-convergence}.md
git add reference/phase-1-scope-and-catchment.md reference/phase-2-candidate-discovery.md reference/phase-3-discovery-convergence.md
git -c commit.gpgsign=false commit -m "docs: add phased multi-source venue discovery"
```

---

### Task 3: Shared evidence, repair, and coverage phases

**Files:** Create `reference/phase-4-evidence-research.md`, `phase-5-evidence-acceptance.md`, `phase-7-coverage-audit.md`.

**Interfaces:** Consume frozen candidates/category prompt/worker refs; produce accepted evidence and audited coverage.

- [ ] **Step 1: Write Phase 4**

Require reading shared status + category prompt. Batch 10–15; parallelize; copy whole canonical block verbatim; substitute only `{CATCHMENT}`, `{ACCESS_DATE}`, `{CANDIDATE_BATCH}`; no paraphrase/additions; follow exact system/user split; record worker refs; recursive children pass same prompt; serial fallback retains rules. Forbid rubric/scoring/ranking/DQ/scratch labels/scarcity/occasions/confidence/rendering. Raw returns become `evidence-returned`, never accepted here. Gate checks assignment, prompt identity, refs, every record, no judgment, returned count.

- [ ] **Step 2: Write Phase 5**

Require semantic review of every venue: literal quotes/values; neutral claim fidelity; URL/type/date; source sequence; rating/count/platform; product-only labeling; no verdict; demonstrated unavailable trail. Write field-specific defects. Repair routing must state:

```markdown
1. Original worker first when available: message/resume its recorded reference; request patches for named venues/fields; preserve accepted fields.
2. Repair message names defects but asks no judgment.
3. Fresh worker only if resume unsupported, failed/timed out, repeated violation, or independent conflict check.
4. Fresh worker receives canonical prompt verbatim.
5. Preserve both conflicting claims/dates; verify; never average.
6. Exhausted-unavailable is terminal only with required trail.
7. Review every patch again.
```

Gate checks every semantic review, defect list, original-worker preference, canonical fallback, conflicts, provenance, exhaustion, and no thin/product-only/verdict evidence scoring.

- [ ] **Step 3: Write Phase 7**

Require fresh reading of status, Phase 2, category discovery. Run new visible favorite, best/scratch/ambitious, local-language, neighborhood, cuisine/tradition/format, specialist/adjacent/marker, recent/renamed/moved/informal queries plus known-example challenges. Each addition loops through Phases 4–6; repeat Phase 7 to a zero-new pass or precise limit. Gate checks logs, all families, resolved additions, last-pass yield, and no early rendering.

- [ ] **Step 4: Format, verify, commit**

```bash
prettier --write reference/phase-{4-evidence-research,5-evidence-acceptance,7-coverage-audit}.md
rg -n 'verbatim|Original worker first|zero-new|zero new' reference/phase-{4-evidence-research,5-evidence-acceptance,7-coverage-audit}.md
git add reference/phase-4-evidence-research.md reference/phase-5-evidence-acceptance.md reference/phase-7-coverage-audit.md
git -c commit.gpgsign=false commit -m "docs: add phased evidence and coverage gates"
```

---

### Task 4: Split bakery category material and harden worker prompt

**Files:** Create bakery `discovery-reference.md`, `phase-4-worker-prompt.md`, `phase-6-scoring.md`, `phase-8-rendering.md`.

**Interfaces:** Consume baseline root; preserve rubric blocks byte-for-byte.

- [ ] **Step 1: Extract unchanged blocks before root replacement**

```bash
python3 - <<'PY'
from pathlib import Path
s=Path('bakery-rubric/SKILL.md').read_text()
def b(a,z): return s[s.index(a):s.index(z)].rstrip()+'\n'
score=b('**Three axes**','## Marker-item seed search (bakery)')
markers=b('## Marker-item seed search (bakery)','## Size-gate, catchment & exhaustive enumeration')
render=b('#### Rare-finds layer','**Three axes**')
sharing=s[s.index('## Sharing Results'):].rstrip()+'\n'
for p,v in [('/tmp/bakery-score',score),('/tmp/bakery-markers',markers),('/tmp/bakery-render',render),('/tmp/bakery-sharing',sharing)]: Path(p).write_text(v)
Path('bakery-rubric/phase-6-scoring.md').write_text('# Phase 6 — Bakery Scoring and Classification\n\n**Read in full immediately before Phase 6. Primary orchestrator makes every decision.**\n\n'+score+'\n## Completion gate\n- [ ] Every decision cites accepted evidence.\n- [ ] Every DQ rests on positive evidence.\n- [ ] Missing evidence was not converted to a low score.\n- [ ] All scores, scarcity, tiers, ties, confidence, and occasions were decided by primary orchestrator.\n- [ ] Product-only was not treated as process.\n')
Path('bakery-rubric/discovery-reference.md').write_text('# Bakery Discovery Reference\n\n**Read in Phases 2 and 7; discovery never qualifies.**\n\n## Broad-survey coverage\nSurvey bakery/pastry/confectionery plus locally relevant café, chocolate, dessert, bread, tortillería, bagel, market, cottage, preorder, and regional equivalents. Category never decides eligibility. Preserve full tags.\n\n## Adaptive families\nGenerate local-language/script concepts for bakery, bread, patisserie/boulangerie/viennoiserie/panadería/tortillería, bagel, lamination, sourdough, natural leavening, house phyllo, chocolatier/bonbon, GF craft, microbakery, baker-owned, artisan, scratch/raw, best/top/award/guide, recent opening, and local traditions; combine with sub-areas. English terms are conceptual, not universal literal queries.\n\n'+markers+'\n## Known-example challenges\n- Adjacent-category chocolatier with serious pastry enters research.\n- Product-only croissant/viennoiserie triggers repair.\n- Sparse-jargon traditional bakery gets review/press/cadence search.\n- Ethnic/single-item specialist is judged only on applicable production evidence.\n')
Path('bakery-rubric/phase-8-rendering.md').write_text('# Phase 8 — Bakery Rendering\n\n**Read only after Phases 1–7 pass.**\n\n'+render+'\n## Coverage statement\nReport broad count, targeted additions, union, audit additions, last-pass yield, and limitations. Never call OSM rows complete census.\n\n## Completion gate\n- [ ] Prior gates passed.\n- [ ] Reader claims use accepted evidence.\n- [ ] Occasion, rare-find, tie, audit, timing, and plain-language rules followed.\n- [ ] Limits stated at source-convergence level.\n\n'+sharing)
PY
```

- [ ] **Step 2: Verify byte-preservation**

```bash
python3 - <<'PY'
from pathlib import Path
for a,z in [('/tmp/bakery-score','bakery-rubric/phase-6-scoring.md'),('/tmp/bakery-markers','bakery-rubric/discovery-reference.md'),('/tmp/bakery-render','bakery-rubric/phase-8-rendering.md'),('/tmp/bakery-sharing','bakery-rubric/phase-8-rendering.md')]: assert Path(a).read_text() in Path(z).read_text(),a
print('bakery blocks preserved')
PY
```

- [ ] **Step 3: Create canonical bakery prompt**

`bakery-rubric/phase-4-worker-prompt.md` must say the orchestrator MUST copy its fenced block verbatim and may substitute only the three declared placeholders. Canonical block:

```text
You are a scratch-bakery EVIDENCE RETRIEVER. Collect raw quotation-level evidence. MUST NOT judge, score, classify, disqualify, rank, assign confidence, or decide scratch/par-bake/ambition.
CATCHMENT: {CATCHMENT}
ACCESS DATE: {ACCESS_DATE}
CANDIDATES: {CANDIDATE_BATCH}

For each bakery return identity/address/phone/domain/aliases + sources; every literal rating/count/platform/URL/date; price; hours/cadence quotes; menu quotes labeled product-only unless process stated; process quotes for leavening, fermentation, hydration, shaping, house lamination, milling/grain, pâtisserie/chocolate and local techniques; named sourcing; physical/cadence/frozen review quotes; adverse factual quotes for frozen/par-bake/commissary/resale/chain/wholesale/closure; neutral claim per quote; full search trail; exhausted-unavailable only after named searches.

Required sequence: official site/menu/about; official social for process/cadence; reviews for physical/cadence; local press/interviews; direct rating platforms.

HARD PROHIBITIONS: no S/I/E/G/G′, pass/fail, DQ, eligibility, ranking, tier, occasion, scarcity, final confidence, scratch/par-bake/dessert-only conclusion, photo/category/product/format/popularity/missing-jargon inference, inferred ratings, or omitted adverse facts. Marketing adjectives remain quotes only.

If >15 candidates and children exist, split 10–15 and pass THIS ENTIRE PROMPT verbatim, changing only placeholders.
```

After the block state response is only `evidence-returned`; Phase 5 accepts/repairs.

- [ ] **Step 4: Format, audit, commit**

```bash
prettier --write bakery-rubric/{discovery-reference,phase-4-worker-prompt,phase-6-scoring,phase-8-rendering}.md
rg -n 'MUST copy|HARD PROHIBITIONS|product-only|adverse' bakery-rubric/phase-4-worker-prompt.md
! rg -n '\| DQ|return.*score|decide.*scratch' bakery-rubric/phase-4-worker-prompt.md
git add bakery-rubric/discovery-reference.md bakery-rubric/phase-4-worker-prompt.md bakery-rubric/phase-6-scoring.md bakery-rubric/phase-8-rendering.md
git -c commit.gpgsign=false commit -m "docs: split bakery rubric into execution phases"
```

---

### Task 5: Split restaurant category material and harden worker prompt

**Files:** Create restaurant equivalents.

**Interfaces:** Same as Task 4 for restaurant.

- [ ] **Step 1: Extract unchanged blocks**

```bash
python3 - <<'PY'
from pathlib import Path
s=Path('restaurant-rubric/SKILL.md').read_text()
def b(a,z): return s[s.index(a):s.index(z)].rstrip()+'\n'
score=b('**Three orthogonal axes**','## Marker-item seed search (likelihood-ratio method)')
markers=b('## Marker-item seed search (likelihood-ratio method)','## Size-gate, catchment & exhaustive enumeration')
render=b('#### Rare-finds layer','**v2 change:**')
sharing=s[s.index('## Sharing Results'):].rstrip()+'\n'
for p,v in [('/tmp/restaurant-score',score),('/tmp/restaurant-markers',markers),('/tmp/restaurant-render',render),('/tmp/restaurant-sharing',sharing)]: Path(p).write_text(v)
Path('restaurant-rubric/phase-6-scoring.md').write_text('# Phase 6 — Restaurant Scoring and Classification\n\n**Read in full immediately before Phase 6. Primary orchestrator makes every decision.**\n\n'+score+'\n## Completion gate\n- [ ] Every decision cites accepted evidence.\n- [ ] Every DQ rests on positive evidence.\n- [ ] Missing evidence was not converted to low score.\n- [ ] All scores, scarcity, tiers, ties, confidence, occasions decided by primary orchestrator.\n- [ ] Product-only and format were not production verdicts.\n')
Path('restaurant-rubric/discovery-reference.md').write_text('# Restaurant Discovery Reference\n\n**Read in Phases 2 and 7; discovery never qualifies.**\n\n## Broad-survey coverage\nSurvey restaurant/café/fast-food and locally relevant food pubs/bars, inns, markets, food halls, pop-ups, informal/preorder. Preserve full tags. Counter, takeaway, delivery, lunch-only, rural inn stay discoverable. Primary bakery-café routes bakery; restaurant baking bread stays restaurant.\n\n## Adaptive families\nGenerate local-language/script concepts for restaurant, scratch/house-made/raw, chef-owned/led, seasonal/daily-changing, farm-to-table/local sourcing, tasting menu, ambitious/creative, best/top/award/guide, rare regional cuisine, recent opening, local techniques/formats and serious traditional cooking; combine with sub-areas. English terms are conceptual, not universal literal queries.\n\n'+markers+'\n## Known-example challenges\n- Recognized scratch restaurant absent OSM enters targeted search.\n- Counter/takeaway/lunch-only never excludes without production evidence.\n- Local-language search can add English-query miss.\n- Broad menu judged only with opened evidence and unchanged K/coherence.\n')
Path('restaurant-rubric/phase-8-rendering.md').write_text('# Phase 8 — Restaurant Rendering\n\n**Read only after Phases 1–7 pass.**\n\n'+render+'\n## Coverage statement\nReport broad count, targeted additions, union, audit additions, last-pass yield, limitations. Never call OSM rows complete census.\n\n## Completion gate\n- [ ] Prior gates passed.\n- [ ] Reader claims use accepted evidence.\n- [ ] Occasion, rare-find, tie, audit, day-part and plain-language rules followed.\n- [ ] Limits stated at source-convergence level.\n\n'+sharing)
PY
```

- [ ] **Step 2: Verify preservation**

```bash
python3 - <<'PY'
from pathlib import Path
for a,z in [('/tmp/restaurant-score','restaurant-rubric/phase-6-scoring.md'),('/tmp/restaurant-markers','restaurant-rubric/discovery-reference.md'),('/tmp/restaurant-render','restaurant-rubric/phase-8-rendering.md'),('/tmp/restaurant-sharing','restaurant-rubric/phase-8-rendering.md')]: assert Path(a).read_text() in Path(z).read_text(),a
print('restaurant blocks preserved')
PY
```

- [ ] **Step 3: Create canonical restaurant prompt**

Use same wrapper and placeholders as bakery. Canonical block requires identity/sources; literal rating/count/platform; price; hours/day-part; menu grammar quotes without K/N estimate; production quotes for pasta/noodles/bread/masa/tortillas/dashi/sauces/charcuterie/cheese/desserts/fermentation/milling/butchery/spice/live fire/long cooking/local techniques; turnover; sourcing; food review quotes separated from nonfood; adverse facts for frozen/pre-made/commissary/assembly/chain/bar-snacks/closure/commodity breadth; literal cuisine/format; neutral claim; full trail. Required sequence: official current/dated menus/about; social/archive; reviews; local press/chef interviews; direct ratings. Prohibit every score/K/N/DQ/eligibility/rank/tier/occasion/scarcity/confidence/scratch/assembly/authentic verdict and all photo/category/cuisine/format/popularity/missing-language inference. Recursive children get exact prompt.

- [ ] **Step 4: Format, audit, commit**

```bash
prettier --write restaurant-rubric/{discovery-reference,phase-4-worker-prompt,phase-6-scoring,phase-8-rendering}.md
rg -n 'MUST copy|HARD PROHIBITIONS|menu grammar|adverse' restaurant-rubric/phase-4-worker-prompt.md
! rg -n '\| DQ|return.*score|decide.*scratch' restaurant-rubric/phase-4-worker-prompt.md
git add restaurant-rubric/discovery-reference.md restaurant-rubric/phase-4-worker-prompt.md restaurant-rubric/phase-6-scoring.md restaurant-rubric/phase-8-rendering.md
git -c commit.gpgsign=false commit -m "docs: split restaurant rubric into execution phases"
```

---

### Task 6: Replace roots with mission-rich v8.9 phase routers

**Files:** Modify both `SKILL.md`.

**Interfaces:** Links every phase and establishes orchestrator authority.

- [ ] **Step 1: Record baseline hashes**

```bash
printf '%s\n' 'e4317f125471e70cd9e76293423bd6b23707a70e6343c764852211722ee746d9 bakery' 'dd23c45b54610eb8480fd2c44e0c331d23dbf3a3976c33535c56f714a620c061 restaurant' >/tmp/pre-refactor-skill-hashes.txt
```

- [ ] **Step 2: Write bakery root**

Include YAML name/description, title v8.9, and strong mission: raw-component onsite production + interesting frequent-buyer bakery, production ambition across bread/lamination/pâtisserie/chocolate/local specialist, scratch eligibility, interestingness survivor ranking, ratings floor, trustworthy shortlist. Name resistance to par-bake invisibility, prominence bias, map omissions, category/register prejudice, missing-evidence collapse, delegation drift.

Add v8.9 changelog exactly covering phased JIT loading/gates, broad+adaptive multilingual discovery, verbatim evidence prompt, semantic acceptance, original-worker repair, orchestrator-only scoring, coverage audit, unchanged rubric.

Add MUST authority: orchestrator personally does DQ/S/I/E/R/G/G′/scarcity/ties/tiers/occasions/confidence/render; never delegates; uses verbatim prompt; checks every row; original worker first; no early output.

Add CRITICAL JIT rule: read named phase files in full immediately before each phase, summaries insufficient, no preload/skip/combine/reorder/silent narrowing, show ✅/❌ gate with evidence.

Add exact ordered links:

1. `../reference/phase-1-scope-and-catchment.md`
2. `../reference/phase-2-candidate-discovery.md` + `discovery-reference.md`
3. `../reference/phase-3-discovery-convergence.md`
4. `../reference/phase-4-evidence-research.md` + `phase-4-worker-prompt.md`
5. `../reference/phase-5-evidence-acceptance.md` + `../reference/shared-status-and-provenance.md` + `phase-4-worker-prompt.md`
6. `phase-6-scoring.md`
7. `../reference/phase-7-coverage-audit.md` + `discovery-reference.md`, additions loop 4–6
8. `phase-8-rendering.md` only after gates

Hard stops: no single-source census, targeted search never qualifies, no missing evidence to low/DQ, no worker verdict, no product noun process inference, no early output, no unfinished-tail permission handoff.

- [ ] **Step 3: Write restaurant root**

Mirror exact phase structure. Mission: scratch + interesting frequent diner; ambition is raw-material production vs commodity assembly/reheat. Resist assembly invisibility, prominence, map omissions, format/cuisine prejudice, missing evidence, delegation drift. Hard stop says format/cuisine/popularity never substitutes for production.

- [ ] **Step 4: Format, live-link and contradiction audit**

```bash
prettier --write bakery-rubric/SKILL.md restaurant-rubric/SKILL.md
python3 - <<'PY'
from pathlib import Path
import re
for r in map(Path,['bakery-rubric/SKILL.md','restaurant-rubric/SKILL.md']):
 t=r.read_text(); assert re.findall(r'^([1-8])\.',t,re.M)==list('12345678')
 for p in re.findall(r'`([^`]+\.md)`',t): assert (r.parent/p).resolve().exists(),(r,p)
print('phase order and links valid')
PY
rg -n 'MUST|original worker|immediately before|verbatim' {bakery-rubric,restaurant-rubric}/SKILL.md
! rg -n 'enrichment only.{0,30}never discovery|Standard subagent brief|\| DQ' {bakery-rubric,restaurant-rubric}/SKILL.md
```

- [ ] **Step 5: Commit**

```bash
git add bakery-rubric/SKILL.md restaurant-rubric/SKILL.md
git -c commit.gpgsign=false commit -m "docs: enforce phased rubric orchestration"
```

---

### Task 7: Update README installation and workflow

**Files:** Modify `README.md`.

**Interfaces:** Documents whole-layout installation and complementary discovery.

- [ ] **Step 1: Replace OSM-only opening**

Use: “These are phased skills for coding agents. Each combines a popularity-neutral place survey with adaptive local-language targeted discovery, gathers quotation-level evidence, and applies a calibrated rubric to surface ambitious scratch kitchens while filtering par-bake/reheated operations.”

- [ ] **Step 2: Replace How It Works**

Eight numbered steps: scope; broad discovery; targeted discovery; union/dedupe/converge; exact evidence-only worker prompt; primary acceptance + original-worker repair; primary scoring + coverage audit; occasion/rare-find/audit output. Explicitly explain broad protects obscure specialists, targeted recovers prominent/new/renamed/unlisted/adjacent-category misses.

- [ ] **Step 3: Replace Usage**

Require installation/linking whole repository, not lone `SKILL.md`, because roots load shared and category references JIT. Show repository tree and both slash commands. Tell self-contained installers to preserve relative paths by linking repo as a unit.

- [ ] **Step 4: Format, verify, commit**

```bash
prettier --write README.md
rg -n 'broad|targeted|whole repository|original worker' README.md
! rg -n 'Retrieval.*Pulls every tagged venue from OpenStreetMap' README.md
git add README.md
git -c commit.gpgsign=false commit -m "docs: document phased rubric workflow"
```

---

### Task 8: Preservation and regression validation

**Files:** Create `docs/superpowers/reports/2026-07-14-phased-rubric-regression-check.md`.

**Interfaces:** Validates links, preserved blocks, role boundaries, regressions.

- [ ] **Step 1: Structural audit**

```bash
python3 - <<'PY' >/tmp/structure.txt
from pathlib import Path
import re
for r in map(Path,['bakery-rubric/SKILL.md','restaurant-rubric/SKILL.md']):
 t=r.read_text(); assert re.findall(r'^([1-8])\.',t,re.M)==list('12345678')
 for p in re.findall(r'`([^`]+\.md)`',t): assert (r.parent/p).resolve().exists(),(r,p)
 print(r,'8 phases; links live')
for f in Path('reference').glob('phase-*.md'):
 assert '## Completion gate' in f.read_text(),f; print(f,'gate present')
PY
```

- [ ] **Step 2: Byte-preservation audit against `572f1d6`**

```bash
python3 - <<'PY' >/tmp/preservation.txt
from pathlib import Path
import subprocess
def old(p): return subprocess.check_output(['git','show',f'572f1d6:{p}'],text=True)
def b(s,a,z): return s[s.index(a):s.index(z)].rstrip()+'\n'
for src,dst,a,z in [('bakery-rubric/SKILL.md','bakery-rubric/phase-6-scoring.md','**Three axes**','## Marker-item seed search (bakery)'),('bakery-rubric/SKILL.md','bakery-rubric/discovery-reference.md','## Marker-item seed search (bakery)','## Size-gate, catchment & exhaustive enumeration'),('restaurant-rubric/SKILL.md','restaurant-rubric/phase-6-scoring.md','**Three orthogonal axes**','## Marker-item seed search (likelihood-ratio method)'),('restaurant-rubric/SKILL.md','restaurant-rubric/discovery-reference.md','## Marker-item seed search (likelihood-ratio method)','## Size-gate, catchment & exhaustive enumeration')]: assert b(old(src),a,z) in Path(dst).read_text(),a; print('PRESERVED',a)
for src,dst,a,z in [('bakery-rubric/SKILL.md','bakery-rubric/phase-8-rendering.md','#### Rare-finds layer','**Three axes**'),('restaurant-rubric/SKILL.md','restaurant-rubric/phase-8-rendering.md','#### Rare-finds layer','**v2 change:**')]:
 s=old(src); assert b(s,a,z) in Path(dst).read_text(); assert s[s.index('## Sharing Results'):].rstrip()+'\n' in Path(dst).read_text(); print('PRESERVED',src,'rendering')
PY
```

- [ ] **Step 3: Role/discovery/format audit**

```bash
{
rg -n 'MUST copy|verbatim|HARD PROHIBITIONS' {bakery-rubric,restaurant-rubric}/phase-4-worker-prompt.md
rg -n 'Original worker first|message/resume' reference/phase-5-evidence-acceptance.md
! rg -n 'web/places search.{0,30}enrichment only|judging named candidates, never discovering|\| DQ' reference bakery-rubric restaurant-rubric README.md
! rg -n '\b(TBD|TODO|FIXME)\b|\[placeholder\]|<placeholder>' reference bakery-rubric restaurant-rubric README.md
prettier --check README.md reference/*.md bakery-rubric/*.md restaurant-rubric/*.md
} >/tmp/role-audit.txt
```

- [ ] **Step 4: Write report with literal outputs and matrix**

Include literal contents of all three `/tmp` files—no paste placeholders—and this completed matrix:

| Scenario                              | Route                                | Result |
| ------------------------------------- | ------------------------------------ | ------ |
| Prominent venue absent OSM            | Phase 2 B/C                          | PASS   |
| Obscure specialist absent best lists  | Phase 2 A                            | PASS   |
| Chez Nibs chocolate-shop label        | Adjacent discovery; worker cannot DQ | PASS   |
| All Purpose product-only              | Original-worker review/press repair  | PASS   |
| Vosen's sparse jargon/rating conflict | Research state; preserve/verify both | PASS   |
| Worker gives DQ/score                 | Phase 5 rejects                      | PASS   |
| Thin worker return                    | Original worker first                | PASS   |
| Counter-service ethnic restaurant     | Format retained; evidence decides    | PASS   |
| Local-language English miss           | Phase 2/7 adds                       | PASS   |
| Late audit candidate                  | Loop Phases 4–6                      | PASS   |
| Early rendering                       | Root/Phase 8 stop                    | PASS   |
| OSM done, targeted skipped            | Gates fail                           | PASS   |

Conclude all extracted scoring, calibration, marker, occasion, rare-find, audience-vocabulary, and sharing blocks match baseline byte-for-byte; v8.9 changes architecture/discovery only.

- [ ] **Step 5: Validate and commit report**

```bash
prettier --write docs/superpowers/reports/2026-07-14-phased-rubric-regression-check.md
! rg -n '\[Paste|TBD|TODO|FIXME' docs/superpowers/reports/2026-07-14-phased-rubric-regression-check.md
git add docs/superpowers/reports/2026-07-14-phased-rubric-regression-check.md
git -c commit.gpgsign=false commit -m "test: document rubric execution regressions"
git status --short
git log --oneline -8
```

Expected: only pre-existing untracked design PDF remains.
