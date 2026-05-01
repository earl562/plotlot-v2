# 2026-05-01 — Chat tool contract alignment (open-data state required)

Branch: `codex/dev-branch-pipeline`  
Delivery commit: `f848a65` (“Fail closed when open-data state is missing in chat tool”)

## Why this was needed

The harness tool registry (`plotlot/src/plotlot/harness/tool_registry.py`) requires `state` for
`discover_open_data_layers`, but the chat tool schema previously:

- marked `state` as optional, and
- silently defaulted to `FL`.

That drift makes tool contracts inconsistent across adapters (chat vs harness runtime) and can cause
silent mis-scoping when the agent is working outside Florida.

## What changed

- `discover_open_data_layers` chat tool schema now **requires** `state`.
- Chat open-data discovery now **fails closed** with a clear error if `state` is missing (no default).
- Updated unit tests to assert the required field list includes `state`.

## Verification

- Ruff: `./.venv/bin/ruff check plotlot/src plotlot/tests`
- Unit tests: `env PYTHONPATH=plotlot/src MLFLOW_TRACKING_URI=file:///tmp/plotlot-mlruns ./.venv/bin/python -m pytest plotlot/tests/unit -q`
  - Result: `780 passed, 1 warning`

