---
name: plotlot-verify-app
description: Run and observe PlotLot locally with Playwright or CDP when verifying a UI, API, or user-reported behavior; distinguish fixture checks from live evidence.
---

# Verify PlotLot through the app

1. Read `docs/agent-workflows/FEATURE_MAP.md` and
   `docs/agent-workflows/VERIFICATION.md` from the repository root. Confirm the
   current branch and affected feature before choosing a lane.
2. Use the exact local ports: frontend dev `127.0.0.1:3000`, API
   `127.0.0.1:8000`, Playwright's isolated server `127.0.0.1:3003` by default.
   Read `plotlot/frontend/playwright.config.ts` if the setup changes.
3. For Playwright, prefer a focused existing spec and inspect its fixtures.
   For exploratory CDP, confirm the actual tab URL and use stable role or
   test-id locators from the feature map. Observe console and network errors.
4. Reproduce the reported behavior, make the smallest correction if this is a
   repair task, and run the same path again. Save relevant trace/screenshot or
   command output and report the exact scenario observed.
5. Label evidence `fixture`, `local service`, or `live external source`.
   A screenshot or successful UI test never upgrades an unverified sale,
   ordinance, or parcel claim.

For a quick browser smoke check from a fresh worktree, install frontend
dependencies with `cd plotlot/frontend && npm ci`, then run
`npm run test:e2e:no-db`. Its Playwright config builds and starts a local
frontend on port 3003. Keep generated reports out of the commit.
