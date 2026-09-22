# PlotLot agent workflows

This is the starting point for the next PlotLot iteration. Lauren Tan's supplied
talk motivates three practices: let an agent operate the real product, give it a
map of product features, and turn repeated failures into skills and hard checks.
This repository's source code and observed behavior determine the actual
PlotLot workflow. This is a foundation for Phat and Earl to review and extend,
not a claim that P-stack has been installed or that PlotLot is production ready.

## How to use this folder

1. Read `AGENTS.md`, then the relevant skill in `.agents/skills/`.
2. Use [FEATURE_MAP.md](FEATURE_MAP.md) to find a feature and a stable UI locator.
3. Use [VERIFICATION.md](VERIFICATION.md) to select a test lane and record what
   was actually observed. A mocked browser test proves UI behavior under its
   fixture; it cannot prove a live county record or an acquisition decision.
4. For real estate claims, follow `plotlot-source-review` before `plotlot-comp-review`.
   Preserve the sequence: property identity → zoning and site evidence →
   qualifying closed-sale comps → underwriting → independent check → human
   approval → outreach.
5. Use [WORKFLOW_TEMPLATE.md](WORKFLOW_TEMPLATE.md) when Phat and Earl specify a
   new repeatable workflow. Keep the skill short; add a check to CI only after a
   failure mode and an executable invariant are understood.

See [the first executed baseline](BASELINE-2026-09-22.md) for the checks run on
this scaffold and their limits.

## Skill inventory

| Skill | State | What it gives the agent |
| --- | --- | --- |
| `plotlot-verify-app` | Usable starting procedure | Browser, Playwright, API, port and evidence instructions |
| `plotlot-source-review` | Usable review rubric | Claim provenance and authority hierarchy |
| `plotlot-comp-review` | Usable review rubric | Current comp qualification boundary and abstention |
| `plotlot-zoning-review` | Draft | Jointly complete source and address scenarios |
| `plotlot-underwriting-review` | Draft | Jointly complete assumptions and independent review |

The source-review and comp-review skills describe how to inspect and evaluate
evidence. They do not add a data provider, certify a county, or authorize an
agent to make a final investment or outreach decision.

## Growing the system

For each workflow, choose one real scenario and one failure scenario. Observe
the agent using the product locally, save the source links or redacted artifacts,
and record whether the skill changed the outcome. Update the feature map when
routes, labels, or selectors change. Promote a recurring rule to a test or lint
only when its expected behavior is precise. Review every skill change against
its scenarios before relying on it.

The branch starts at `origin/cpt-pro` commit
`4047bbdc6c717be0973351151cd6ab40f9570fb3`. The original `cpt-pro`
checkout's uncommitted work was not copied into this worktree. Recheck this
baseline when the branch moves.
