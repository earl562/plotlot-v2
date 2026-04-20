# Distinguished E2E Walkthrough Report

Date: 2026-04-14
App: PlotLot frontend + local backend
Runner: Playwright Chromium

## Scope

This walkthrough exercised:

- Lookup welcome state
- Invalid-input validation
- Deal-type gating
- Pipeline approval
- Live pipeline start
- Agent-mode welcome state
- Agent SSE error handling
- Agent connection-failure handling
- Cross-mode state clearing
- Lookup timeout + retry affordance

## Environment Reality

- Frontend served locally at `http://localhost:3000`
- Backend served locally at `http://localhost:8000`
- Backend health during walkthrough: `degraded`
- Root cause: local Postgres on `localhost:5433` was unavailable, so full report-generation paths were not validated in this run

## Screenshot Evidence

- [Lookup welcome](./screenshots/distinguished/01-lookup-welcome.png)
- [Lookup invalid input](./screenshots/distinguished/02-lookup-invalid-input.png)
- [Deal type selector](./screenshots/distinguished/03-deal-type-selector.png)
- [Pipeline approval](./screenshots/distinguished/04-pipeline-approval.png)
- [Pipeline running](./screenshots/distinguished/05-pipeline-running.png)
- [Agent welcome](./screenshots/distinguished/07-agent-welcome.png)
- [Agent SSE error](./screenshots/distinguished/08-agent-sse-error.png)
- [Agent connection failure](./screenshots/distinguished/09-agent-connection-failure.png)
- [Pending lookup before mode switch](./screenshots/distinguished/10-pending-lookup-before-switch.png)
- [Agent after mode switch](./screenshots/distinguished/11-agent-after-switch.png)
- [Lookup after switch back](./screenshots/distinguished/12-lookup-after-switch-back.png)
- [Lookup timeout retry state](./screenshots/distinguished/13-lookup-timeout-retry.png)

## What Works

- Welcome-state UX is coherent and renders reliably.
- Lookup mode correctly rejects non-address text before opening the pipeline.
- Address submission correctly enters the deal-type selection gate.
- Pipeline approval appears consistently after deal-type selection.
- Live pipeline start is visible and understandable.
- Agent mode loads a distinct UX with the expected prompt and controls.
- Agent error states render instead of silently failing.
- Cross-mode switching clears pending lookup state instead of leaking stale UI.
- Timeout handling exposes a visible retry path.

## What Does Not Work Yet

- Full local end-to-end report completion is blocked by the degraded backend environment.
- A “healthy backend required” assumption still exists in parts of the broader suite and needs env-aware handling.
- Some older screenshot/spec files are stale and still reference pre-refactor placeholders and flows.
- Frontend lint is currently failing on pre-existing issues outside this walkthrough spec, which increases noise when validating changes.

## Highest-Value Optimizations

1. Restore a healthy local database path so full report rendering, follow-up analysis, and persistence can be exercised in CI and local dev.
2. Consolidate legacy Playwright specs around the current lookup/agent split to remove stale placeholder and selector drift.
3. Add a first-class “degraded backend” banner in the UI so the user understands why full analysis stops early.
4. Standardize pipeline step selectors with stable test ids; repeated “Geocoding” text currently makes strict locators brittle.
5. Move the best mutation scenarios into a dedicated smoke lane in CI so timeout, connection-failure, and SSE-error handling are always covered.
6. Burn down the existing frontend lint debt so walkthrough failures are easier to trust as product regressions rather than baseline noise.

## Test Runs

- `npx playwright test tests/distinguished-walkthrough.spec.ts --project=chromium`
- `npx playwright test tests/e2e-visual.spec.ts --project=chromium`

## Outcome

The current frontend interaction model is stronger than the local backend readiness story. The UX around gating, state transitions, and failure messaging is in decent shape; the main blocker to a truly “full” walkthrough is infrastructure readiness, not the top-level client flow.
