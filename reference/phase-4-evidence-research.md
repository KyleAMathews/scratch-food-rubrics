# Phase 4 — Evidence Research

Read `shared-status-and-provenance.md` and the invoked category's `phase-4-worker-prompt.md` in full immediately before dispatching any worker.

## Input

The frozen candidate ledger and the exact category worker-prompt file named by the root skill.

## Primary-agent responsibility

The primary agent remains the orchestrator. Workers are bounded evidence retrievers, not alternate orchestrators.

## Mandatory dispatch protocol

1. Split candidates into leaf batches of approximately 10–15 venues.
2. When parallel workers are available, dispatch independent batches concurrently.
3. Copy the category prompt's canonical block verbatim. Substitute only `{CATCHMENT}`, `{ACCESS_DATE}`, and `{CANDIDATE_BATCH}`.
4. Do not summarize, paraphrase, shorten, improve, or append requirements to the canonical block.
5. If the runtime separates system and user messages, use the split printed in the category prompt file exactly.
6. Record each worker reference on every assigned candidate row.
7. If a worker recursively splits an oversized batch, it passes the same canonical block verbatim and substitutes only the declared placeholders.
8. If subagents are unavailable, execute the same canonical procedure serially. Their absence never permits inference.

## Forbidden delegation

Never ask a worker to apply the rubric, score, rank, decide eligibility, assign DQ, label scratch/par-bake/assembly, reason about scarcity, route occasions, assign final confidence, or render recommendations.

## Return handling

- Store raw returns without silently correcting them.
- Mark a candidate `evidence-returned` when its record arrives.
- Do not call a row accepted in this phase.
- A missing or malformed row remains incomplete and must be obtained before closing the return-coverage gate.

## Completion gate

- [ ] Every frozen candidate was assigned exactly once or included in one recorded shared batch.
- [ ] Every dispatch used the canonical block verbatim with only declared substitutions.
- [ ] Worker references are recorded.
- [ ] Every candidate has a returned record.
- [ ] No worker was asked to judge, score, DQ, rank, or render.
- [ ] Returned count equals frozen candidate count; acceptance has not been claimed.
