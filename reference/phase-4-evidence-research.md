# Phase 4 — Evidence Research

Read `shared-status-and-provenance.md` and the invoked category's `phase-4-worker-prompt.md` in full immediately before dispatching any worker.

## Input

`{RUN_DIR}/03-candidate-ledger.md` and the exact category worker-prompt file named by the root skill.

## Primary-agent responsibility

The primary agent remains the orchestrator. Workers are bounded evidence retrievers, not alternate orchestrators.

## Mandatory dispatch protocol

1. Split candidates into leaf batches of approximately 10–15 venues.
2. When parallel workers are available, dispatch independent batches concurrently.
3. Copy the category prompt's canonical block verbatim. Substitute only the placeholders declared by that category prompt: `{CATCHMENT}`, `{ACCESS_DATE}`, and `{CANDIDATE_BATCH}` for restaurants; those three plus `{OUTPUT_PATH}` for bakeries. `{OUTPUT_PATH}` MUST be a unique leaf-batch file under `{RUN_DIR}/04-worker-returns/`, never a directory or a path shared by concurrent workers.
4. Do not summarize, paraphrase, shorten, improve, or append requirements to the canonical block.
5. If the runtime separates system and user messages, use the split printed in the category prompt file exactly.
6. Record each worker reference on every assigned candidate row.
7. Workers MUST NOT recursively split assigned batches. The primary orchestrator alone creates leaf batches. For bakeries, assign each leaf batch a unique worker output path. For restaurants, which have no `{OUTPUT_PATH}` placeholder, assign each leaf batch a unique orchestrator-saved return filename. Never assign concurrent batches to the same artifact.
8. If subagents are unavailable, execute the same canonical procedure serially. Their absence never permits inference.

## Forbidden delegation

Never ask a worker to apply the rubric, score, rank, decide eligibility, assign DQ, label scratch/par-bake/assembly, reason about scarcity, route occasions, assign final confidence, or render recommendations.

## Artifact handling

- Give workers `{RUN_DIR}` only as an output destination when they can write files; otherwise the orchestrator saves their returned message there.
- Save each raw, unedited return under `{RUN_DIR}/04-worker-returns/` with a stable filename containing batch ID and worker reference.
- Record dispatch time, candidate IDs, worker reference, prompt-version/category, return filename, and status in `{RUN_DIR}/04-worker-returns/index.md`.
- Never let a worker write elsewhere in the project.

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
- [ ] Every raw return and dispatch index entry is under `{RUN_DIR}/04-worker-returns/`; no Phase 4 artifact is outside the run directory.
