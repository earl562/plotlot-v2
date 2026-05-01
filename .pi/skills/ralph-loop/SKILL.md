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

At the end of your response, include **exactly one** status line:

- `RALPH_STATUS: COMPLETE` — goal fully met + verified
- `RALPH_STATUS: CONTINUE` — more work remains (or needs another verification pass)
- `RALPH_STATUS: BLOCKED` — needs user decision/credentials/destructive confirmation
- `RALPH_STATUS: MAXED` — iteration budget exhausted

Do **not** ask “Continue?” — the harness will decide whether to enqueue another iteration.

## One-iteration steps

1. Restate the goal as **acceptance criteria** (tight, verifiable).
2. Plan the **smallest increment** you can complete now.
3. Execute changes.
4. Verify with the tightest checks available.
5. Summarize what changed + what remains.
6. Emit `RALPH_STATUS`.

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
