# PlotLot UX Overhaul — Continue Implementation

Resume the UX Quality Overhaul from the audit plan.

## Context

Read the full plan and audit at:
- **Plan:** `/Users/earlperry/.claude/plans/fluttering-percolating-flute.md`
- **Audit report:** `plotlot/docs/superpowers/specs/2026-03-14-implementation-audit.md`
- **Design spec:** `plotlot/docs/superpowers/specs/2026-03-14-plotlot-ux-design.md`

## What's Done (Phases 1-4 partial + Tier 1 fixes)
- Phase 1: Research complete
- Phase 3: 4 bugs fixed (autocomplete z-index, parcel boundary, async Gemini, mode guard)
- Phase 4: Lookup mode — DealTypeSelector, TabbedReport (4 tabs), DealHeroCard
- Tier 1: All 4 deal type hero cards now have correct metrics (including user input forms for Creative Finance + Hybrid)
- ECC plugin fully installed

## What's Next (Execute in order)

### Tier 2: Agent Intelligence (Backend) — HIGHEST PRIORITY
1. **Pipeline approval gate** — `PipelineApproval.tsx` (NEW) + `routes.py` (add `skip_steps` param)
2. **Thinking transparency** — `ThinkingIndicator.tsx` (NEW) + stream `thinking` events from `routes.py`
3. **Intent parsing in chat.py** — classify intent + deal type before tool selection

### Tier 3: UX Polish
4. **Tool cards** — replace CapabilityChips with functional ToolCards in agent mode
5. **Inline citations** — link extracted params to source ordinance chunks
6. **Document canvas** — side panel for document generation

### Tier 4: Testing & Deploy
7. **Playwright E2E tests** — lookup flow, agent flow, mode switching, error recovery
8. **Stress test** — 10+ addresses across all 4 deal types
9. **Deploy** — merge to main

## Rules
- Use ECC for everything: `/ecc-tdd` for implementation, `/ecc-verify` before PR
- Execute autonomously — no "Ready?" or "Should I proceed?" gates
- Every change ships with tests
- Backend + frontend changes together (not frontend-only)

## Key Files
- `plotlot/frontend/src/app/page.tsx` — main page (lookup + agent flows)
- `plotlot/frontend/src/components/DealHeroCard.tsx` — deal type hero metrics
- `plotlot/frontend/src/components/TabbedReport.tsx` — 4-tab report
- `plotlot/frontend/src/components/DealTypeSelector.tsx` — deal type picker
- `plotlot/frontend/src/components/AnalysisStream.tsx` — pipeline progress
- `plotlot/src/plotlot/api/chat.py` — agentic chat (needs intent parsing)
- `plotlot/src/plotlot/api/routes.py` — /analyze/stream (needs skip_steps, thinking events)
- `plotlot/src/plotlot/api/schemas.py` — request/response models

$ARGUMENTS
