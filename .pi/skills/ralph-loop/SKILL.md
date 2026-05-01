---
name: ralph-loop
description: Persistence-oriented continuous dev loop (Ralph Wiggum style). Use to iteratively plan/execute/verify changes toward a goal, with explicit stop conditions and mandatory verification.
---

# Ralph Loop (dev-only)

This skill is a **single-iteration** runbook used by a harness/controller (human, extension, or script) to keep working until the goal is complete.

## Safety + governance

- Never run destructive commands without asking for confirmation.
- Do **not** push to remotes unless the user explicitly asks.
- Each iteration must end with a **verification step** (tests/lint/build/script).
- If verification fails, switch to fixing and re-verify before proceeding.

## Inputs

The user supplies a `goal` (and the harness may provide an iteration counter).

## Output contract (required)

At the top of your response:

- `[RALPH ITERATION <i>/<max>]`

Then include the following sections (in this order):

1) `## Current task`
- The single concrete task you are completing *this* iteration.

2) `## Spec-driven plan`
- A short, checklist-style plan referencing the relevant spec/contract/tests/docs you’re driving from.

3) `## Reasoning summary`
- A brief, high-level explanation of why this step is the right next step.
- Do **not** include hidden chain-of-thought; keep it to decisions + tradeoffs.

4) `## Execution details`
- Bullet list of the concrete actions taken (commands run, files edited, key outputs).

5) `## Verification`
- Exactly what you ran/checked and the result.

6) `## Deltas`
- Paths changed this iteration.

At the end of your response, include **exactly one** status line:

- `RALPH_STATUS: COMPLETE` — goal fully met + verified
- `RALPH_STATUS: CONTINUE` — more work remains (or needs another verification pass)
- `RALPH_STATUS: BLOCKED` — needs user decision/credentials/destructive confirmation
- `RALPH_STATUS: MAXED` — iteration budget exhausted

Do **not** ask “Continue?” — the harness will decide whether to enqueue another iteration.

## One-iteration steps

1. Pick **one** small task that meaningfully advances the goal.
2. Write a **spec-driven plan** (checklist) tied to contracts/tests/docs.
3. Execute changes with concrete, inspectable steps.
4. Verify with the tightest checks available.
5. Record deltas (paths changed) and what remains.
6. Emit `RALPH_STATUS`.

## Steering

When the user provides steering (via `/ralph steer ...`), incorporate it into the **Spec-driven plan** for the next iteration.
If steering conflicts with safety/governance rules, emit `RALPH_STATUS: BLOCKED` and ask for clarification.

## Research-specific rule (arXiv)

If the iteration involves “reviewing an arXiv paper”, do **not** rely only on the abstract. Use:
- the full PDF text in `docs/research/_cache/arxiv/<id>.txt` (regenerate via `download_arxiv_papers.mjs`), and/or
- the arXiv HTML view when available.

## Verification defaults

Choose the narrowest verification that matches what you changed:

- Backend / Python (default fast lane):

```bash
cd plotlot && make lint && uv run pytest tests/unit/ -v
```

- Backend / Python (full suite; includes live/integration/eval — use intentionally):

```bash
cd plotlot && make test
```

- Frontend-only:

```bash
cd plotlot/frontend && npm test
```

- Docs / research artifact updates only (no code):

```bash
node .pi/skills/autoresearch/scripts/list_unreviewed_notes.mjs
node .pi/skills/autoresearch/scripts/prioritize_arxiv_notes.mjs
```
