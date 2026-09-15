# Site readiness — first implementation slice

## What is implemented
A deterministic, draft land-feasibility workflow for a supplied site, proposed use,
scenario, checklist, and structured source records. It produces a decision memo,
risk register, source references, and dependency-aware next actions.

- `hold`: at least one critical requirement is uncertain or contradictory.
- `do_not_proceed`: supplied source-checked evidence conflicts with a critical
  requirement under this scenario. This is not a professional finding by PlotLot.
- `ready_for_review`: the supplied critical requirements are supported by the
  supplied checks. It never means approved, permitted, or certified buildable.

Site, parcel, scenario, proposed use, units, freshness, source availability,
source locators, and review status are checked. Unknowns do not become passes.
Screening/proximity observations and broker/user notes cannot clear a requirement.
Changing a proposed use does not reassign old source evidence to the new use.
Numeric inputs are finite and bounded to magnitude 1e15; no unit conversion is inferred.

The residential, industrial, and data-center checklists are starters, not an
exhaustive statement of a jurisdiction's diligence or permitting requirements.
Scope is always explicitly `supplied_requirements_only`.

## Run the internal workbench
From `plotlot/`, in an environment with the application's Python dependencies:

```bash
PYTHONPATH=src python scripts/readiness_demo.py --port 8765
```

Open `http://127.0.0.1:8765/api/v1/readiness/workbench`.
The demo is loopback-only and needs no API key. It neither grants a tenant identity
nor bypasses saved-case authentication. Synthetic examples are labeled accordingly.
Case JSON imports and exports are supported. The page does not use localStorage.

This workbench is a backend-internal review surface, not a completed integration
into the main Next.js workspace UI.

## Main application integration
`api/workspaces.py` includes the new router under the existing `/api/v1` prefix.
Existing tenant/capability middleware remains in force. Saved-case routes also
check the server-derived actor; caller-supplied reviewer IDs are not accepted.

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/v1/readiness/playbooks/{kind}` | Starter checklist |
| POST | `/api/v1/readiness/preview` | Evaluate a `ReadinessCase`; no DB or network |
| GET | `/api/v1/readiness/workbench` | Internal workbench |
| GET | `/api/v1/workspaces/{workspace_id}/sites/{site_id}/readiness` | Load latest saved version |
| PUT | `/api/v1/workspaces/{workspace_id}/sites/{site_id}/readiness` | Save `{case, expected_revision}` |

For a new saved case, use `expected_revision: 0`. Subsequent saves require the
last loaded revision. The stored site's parcel must match the input. Cross-tenant
access is denied; conflicts return 409 rather than silently overwriting work.

## Storage and audit
Uses existing `sites.facts_json.site_readiness` for the latest version. Every save
also inserts a new `analysis_runs` row containing the supplied case and resulting
memo. Unrelated site facts are preserved. Both changes commit together or roll
back together. PostgreSQL SELECT FOR UPDATE serializes site saves; a revision
check detects stale clients. No schema migration is introduced or executed.

The latest version includes before/after memo changes. These snapshots are not
an independent professional review history. Source-check flags remain attributed
to the supplied input; the saving actor is recorded separately.

## Repeat the build/test loop
From the repository root:

```bash
PYTHONPATH=plotlot/src python -m pytest -c /dev/null --rootdir=. --noconftest \
  plotlot/tests/unit/test_readiness_engine.py \
  plotlot/tests/unit/test_readiness_store.py \
  plotlot/tests/unit/test_readiness_api.py -v
python -m compileall -q plotlot/src/plotlot/land_use/readiness \
  plotlot/src/plotlot/api/readiness.py
python -m playwright install chromium
PYTHONPATH=plotlot/src python plotlot/tests/readiness_browser.py
```

`READINESS_CHROMIUM_EXECUTABLE` optionally selects an already installed Chromium.
`READINESS_BROWSER_OUTPUT` selects the output folder. Browser checks use the actual
local preview API; no provider or decision responses are mocked.

The dedicated GitHub workflow runs targeted tests and the browser suite with
read-only repository permissions. It does not deploy, migrate, or merge anything.

## Validation boundaries
Local work used an isolated git worktree of a partial connector snapshot because
this runner could not clone the repository. The original workspace-router file
was hash-verified against cpt-pro. Targeted persistence tests use a real SQLite DB
with an async adapter; they do not prove PostgreSQL concurrency behavior.

The local Chromium environment blocked localhost navigation. A local browser
pass is therefore not claimed; inspect the dedicated branch CI run separately.
Full-project dependency installation, Next.js build, production authentication,
PostgreSQL concurrency, and live-property/provider evaluation remain release gates.

Raw PDF extraction, automated GIS ingestion, utility capacity verification,
professional sign-off, external messages, consultant procurement, and production
rollout are not included in this slice.
