---
name: plotlot-underwriting-review
description: Draft workflow for jointly reviewing PlotLot underwriting assumptions after parcel, zoning, and qualifying comparable sale evidence exists.
---

# Underwriting review draft

This skill is a review scaffold. Phat and Earl still need to define example
deals, acceptable assumptions, independent checks, and the approval owner.
Do not start from a model-generated price. Establish the subject with
`plotlot-source-review`, review zoning with `plotlot-zoning-review`, and use
only the qualified output described by `plotlot-comp-review`. Record each
assumption with its origin, date, and sensitivity. If a necessary input is
unverified or comps are insufficient, leave the affected estimate incomplete.

To complete this skill, fill out `docs/agent-workflows/WORKFLOW_TEMPLATE.md`
with a real deal, an insufficient-evidence case, and an independent reviewer.
Human approval is required before investment action or outreach.
