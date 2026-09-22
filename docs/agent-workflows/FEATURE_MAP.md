# PlotLot feature map

Checked against the code and Playwright tests at the branch baseline noted in
[README.md](README.md). These are navigation hints, not proof that a feature
works against live services. Before using a selector after a UI change, inspect
the current page and update this map if it has drifted.

| User goal | Entry point and path | Locator or expected surface | Code or test |
| --- | --- | --- | --- |
| View public landing page | `/` | heading `See What Fits.`; `Analyze a Lot` link | `frontend/src/app/page.tsx`; `tests/smoke.no-db.spec.ts` |
| Look up a site | `/workspace?mode=lookup` | `data-testid=lookup-input`; `send-button` | `frontend/src/app/(workspace)/workspace/page.tsx`; `tests/smoke.no-db.spec.ts` |
| Open agent workspace | `/workspace?mode=agent` or sidebar `harness-workspace` | `data-testid=agent-input`; `send-button` | `frontend/src/components/Sidebar.tsx`; `tests/sidebar-navigation.spec.ts` |
| Browse analyses | Sidebar `analyses` → `/analyses` | heading `Analyses` | `tests/sidebar-navigation.spec.ts` |
| Browse connectors | Sidebar `connectors` → `/connectors` | `data-testid=connectors-page` | `tests/sidebar-navigation.spec.ts` |
| Open intelligence console | `/analyze` | heading `Land-use intelligence console.`; `analyze-evidence-card` | `frontend/src/app/analyze/page.tsx`; `tests/smoke.no-db.spec.ts` |
| Check API health | backend `/health` | HTTP response and capability details | `src/plotlot/api/main.py` |

Frontend source and tests in the table are relative to `plotlot/`. The workspace
also has `/projects`, `/evidence`, `/reports`, and `/billing` routes. Their
authentication, test fixtures, and stable locators still need a joint walkthrough
before this map gives click instructions for them.

Use Playwright's role or test-id locators first. For an exploratory CDP session,
connect only to the local app instance you started and confirm the browser tab's
URL before acting. CDP is a control mechanism, not an independent source of real
estate truth. Record the actual URL, browser observation, console/network errors,
and screenshots or traces relevant to the scenario.
