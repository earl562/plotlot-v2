---
name: plotlot-zoning-review
description: Draft workflow for jointly validating PlotLot zoning and site constraints against an official jurisdiction source and a real parcel.
---

# Zoning review draft

This skill is a review scaffold. Phat and Earl still need to select real parcel
scenarios, official municipal sources, expected citations, and failure cases.
Until then, use `plotlot-source-review` to establish identity and provenance,
then `plotlot-verify-app` to observe the zoning UI. Mark unresolved zoning or
site claims as incomplete and ask a human to compare the cited ordinance and
parcel facts. Do not treat a retrieved excerpt or plausible density calculation
as an approved legal interpretation.

To complete this skill, fill out `docs/agent-workflows/WORKFLOW_TEMPLATE.md`
with one address in each supported launch jurisdiction and a negative case
where an ordinance citation or parcel identity is missing.
