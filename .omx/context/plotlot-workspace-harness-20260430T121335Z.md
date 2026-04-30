# Ralph Context Snapshot — PlotLot Workspace Harness Clean Baseline

## Task statement

Create a clean, project-local PlotLot baseline and prepare a separate feature branch for implementing the workspace-native governed harness described in the user PRD.

## Desired outcome

- PlotLot is isolated from the parent `/Users/earlperry` Git repository.
- A safe root `.gitignore` protects secrets, virtualenvs, caches, local DBs, logs, MLflow runs, Playwright artifacts, and frontend build outputs.
- The current PlotLot codebase is committed as a clean baseline.
- Work continues on `feature/plotlot-workspace-harness` for harness implementation.
- Required Ralph planning-gate artifacts exist before implementation: PRD and test spec.

## Known facts / evidence

- Project root: `/Users/earlperry/Desktop/Projects/EP/plotlot`.
- Before isolation, `git rev-parse --show-toplevel` from PlotLot resolves to `/Users/earlperry`, not PlotLot.
- `git ls-files -- Desktop/Projects/EP/plotlot` from `/Users/earlperry` returned no tracked PlotLot files.
- Current backend includes FastAPI app, analysis routes, chat routes, portfolio, document, geometry, render, billing, property retrieval, clause generation, tests, and frontend.
- Existing plan artifact: `.omx/plans/plotlot-workspace-harness-20260430.md`.

## Constraints

- Do not use the parent home-directory Git repo for this feature branch.
- Do not commit secrets or local runtime artifacts.
- Preserve current MVP behavior before harness changes.
- Do not begin harness implementation until `.omx/plans/prd-*.md` and `.omx/plans/test-spec-*.md` exist.
- No new dependencies unless explicitly justified later.

## Unknowns / open questions

- Whether an external PlotLot remote exists. User chose a clean baseline, so local repo initialization is the default.
- Baseline tests may have existing failures; capture evidence rather than hiding failures.

## Likely codebase touchpoints after baseline

- `src/plotlot/harness/`
- `src/plotlot/workspace/`
- `src/plotlot/api/workspace.py`
- `src/plotlot/api/harness.py`
- `src/plotlot/api/chat.py`
- `src/plotlot/pipeline/lookup.py`
- `src/plotlot/storage/models.py`
- `alembic/versions/`
- `frontend/src/app/workspaces/`
- `frontend/src/app/projects/`
- `frontend/src/features/`
- `tests/unit/`, `tests/integration/`, `frontend/tests/`, `plotlot-bench/`
