---
name: ralph-loop
description: Continuous dev loop runbook (Ralph Wiggum style). Use to iteratively plan/execute/verify changes toward a goal with tight test+eval gates.
---

# Ralph Loop (dev-only)

Use this skill when running a continuous improvement loop on the current repo.

## Safety + governance

- Never run destructive commands without asking for confirmation.
- Do **not** push to remotes unless the user explicitly asks.
- Each iteration must end with a **verification step** (tests/lint/build).
- If verification fails, stop and present the failure + a minimal fix plan.

## Inputs

The user supplies a `goal`.

## Loop

Repeat until the user stops you:

1. Clarify the goal into acceptance criteria.
2. Plan the smallest PR-sized increment.
3. Execute changes.
4. Verify with the tightest tests available.
5. Summarize what changed + what remains.
6. Ask: Continue?

## Verification defaults

From repo root:

```bash
cd plotlot && make test
```

If frontend-only changes:

```bash
cd plotlot/frontend && npm test
```
