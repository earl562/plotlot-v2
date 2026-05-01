# 2026-05-01 — Architect approval (spec drift resolved)

Branch: `codex/dev-branch-pipeline`  
Approval checkpoint: `adb18bc`

## What was blocking

An architect review flagged a “two sources of truth” problem where PRD/test-spec copies existed in:

- `plotlot/.omx/plans/*` (PlotLot app root)
- `.omx/plans/*` (repo root; gitignored but present in local OMX sessions)

The root copies were outdated (old endpoints + prefixed tool names), which made reviews ambiguous.

## What we changed

- PRD + test spec now explicitly state:
  - **All paths are relative to the PlotLot app root (`plotlot/` in this repo)**.
- Root `.omx/plans` PRD/test-spec are now **exact mirrors** of `plotlot/.omx/plans` to prevent drift in local OMX workflows.
- Connector expectations in the test spec were aligned with the current runtime posture:
  - write tools without handlers are **not listed** and return `status=unavailable` (fail-closed) until implemented.

## Outcome

Architect verdict: **APPROVED** (no remaining blocking spec/implementation/governance mismatches).

