# Scratch Food Rubrics

AI-powered rubrics for finding restaurants and bakeries that make food from scratch.

These are skills you can run in a coding agent (Claude Code, Codex, or similar). Each rubric pulls venues from OpenStreetMap, then scores them against criteria designed to surface scratch kitchens and filter out par-bake/reheated operations.

## Rubrics

### Restaurant Rubric

Finds restaurants that are **scratch-made AND interesting to a frequent diner**.

```
/restaurant-rubric [location]
```

Scores on three axes:
- **S (scratch)** — production intensity (0-100)
- **I (interestingness)** — novelty/turnover + market scarcity (0-100)  
- **R (rating)** — used as quality filter only, not ranking

### Bakery Rubric

Finds bakeries that are **made from raw components on-site AND interesting to a frequent buyer** — screening out par-bake (frozen partially-baked dough finished on-site).

```
/bakery-rubric [location]
```

Same S/I/R scoring structure, tuned for bakery-specific signals like lamination quality, bake cadence, and wholesale pressure.

## How It Works

1. **Retrieval**: Pulls every tagged venue from OpenStreetMap (popularity-neutral, no ranking bias)
2. **Scoring**: Subagents read menus, reviews, and websites looking for involuntary tells
3. **Output**: Ranked list organized by foodie occasions (best meal, something new, casual scratch, etc.)

## Key Concepts

**Involuntary tells**: Signals businesses reveal without intending to. "Fresh baked all day!" confesses par-bake (scratch bakeries sell out). Physical descriptors like "shattering layers, open crumb" survive regardless of marketing.

**Register-independent signals**: Weight observable physics over process vocabulary. A par-bake cafe can say "fresh baked" (technically true). But "sells out by 11am" physically contradicts the frozen-inventory model.

**Market scarcity**: A static menu can be maximally interesting if it's the only place in town doing that cuisine. Novelty has two sources: menu turnover AND local rarity.

## Usage

Add this repo to your coding agent's skills directory, or copy the SKILL.md files to your `.claude/commands/` folder.

## License

MIT
