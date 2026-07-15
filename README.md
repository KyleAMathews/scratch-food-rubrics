# Scratch Food Rubrics

AI-powered rubrics for finding restaurants and bakeries that make food from scratch.

These are phased skills for coding agents (Claude Code, Codex, or similar). Each combines a popularity-neutral place survey with adaptive local-language targeted discovery, gathers quotation-level evidence, and applies a calibrated rubric to surface ambitious scratch kitchens while filtering par-bake or reheated operations.

## Rubrics

### Restaurant Rubric

Finds restaurants that are **scratch-made AND interesting to a frequent diner**.

```text
/restaurant-rubric [location]
```

Scores on three axes:

- **S (scratch)** — production intensity (0–100)
- **I (interestingness)** — novelty/turnover plus market scarcity (0–100)
- **R (rating)** — a quality filter only, not the ranking signal

### Bakery Rubric

Finds bakeries that are **made from raw components on-site AND interesting to a frequent buyer**, screening out par-bake (frozen partially baked dough finished on-site).

```text
/bakery-rubric [location]
```

It uses the same S/I/R structure, tuned for bakery signals such as lamination, bake cadence, and wholesale pressure.

## How It Works

The primary agent stays in charge for the entire run and loads each phase's instructions immediately before executing it:

1. **Create the run workspace and scope:** Create a unique `<YYYY-MM-DD>-<location-slug>/` directory, then define the actual local catchment and its limits. Every ledger, source export, worker return, decision, audit, and result for that run stays inside this directory.
2. **Discover broadly:** Survey OpenStreetMap or another popularity-neutral place index.
3. **Discover deliberately:** Run adaptive local-language searches for prominent, scratch-focused, ambitious, specialist, new, renamed, and poorly tagged venues.
4. **Converge:** Union and deduplicate candidates, inspect neighborhood, language, and category gaps, and require a no-new-candidate pass.
5. **Retrieve evidence:** Subagents receive an exact evidence-only prompt and quote menus, sites, reviews, press, and literal ratings. They never score.
6. **Accept and repair:** The primary agent checks every record. When possible, it messages the original worker for targeted missing evidence.
7. **Score and audit:** The primary agent applies the unchanged rubric, then challenges the candidate set again before rendering.
8. **Output:** Results are organized by foodie occasions, rare finds, and an audit ranking, with honest discovery limits.

Broad and targeted discovery are complementary. Map enumeration protects obscure specialists from popularity bias; targeted searches recover prominent, new, renamed, unlisted, and category-adjacent venues that map data misses.

Each run is self-contained. Repeating a location on the same date creates a suffixed directory such as `2026-07-14-salt-lake-valley-2`; prior runs are never reused or overwritten.

## Key Concepts

**Involuntary tells:** Signals businesses reveal without intending to. “Fresh baked all day!” can confess par-bake economics, while physical descriptors such as “shattering layers” and “open crumb” survive regardless of marketing.

**Register-independent signals:** Weight observable physics over process vocabulary. A par-bake café can say “fresh baked” (technically true), but “sells out by 11am” physically contradicts the frozen-inventory model.

**Market scarcity:** A static menu can be maximally interesting if it is the only place in town doing that cuisine. Novelty has two sources: menu turnover and local rarity.

## Usage

Install or link the **whole repository layout**, not a lone `SKILL.md`: each root skill loads shared files from `reference/` and category files from its own directory just in time.

```text
scratch-food-rubrics/
├── reference/
├── restaurant-rubric/
│   └── SKILL.md
└── bakery-rubric/
    └── SKILL.md
```

Then invoke:

```text
/restaurant-rubric [location]
/bakery-rubric [location]
```

If your agent's skill installer expects one self-contained directory per skill, preserve the relative shared-reference paths by installing or linking the repository as a unit rather than copying only the root file.

## License

MIT
