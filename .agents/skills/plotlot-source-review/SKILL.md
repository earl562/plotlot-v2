---
name: plotlot-source-review
description: Review provenance and conflicts for a PlotLot parcel, zoning, site, or transaction claim before it is used in acquisition analysis.
---

# Review property evidence

Start with a parcel identity and jurisdiction. For each material claim, record
the source URL, issuing authority, record ID, effective or sale date, retrieval
time, exact field observed, and any conflicting source. Reconcile the address
to the parcel before applying its zoning or sale record. Use the jurisdiction's
official zoning and property records for legal/site claims, and county
appraiser plus recorder/deed records or an authorized transaction export for
closed-sale claims.

Keep listing pages, photos, AVMs, and vision output in a discovery/context lane.
They cannot establish a closed transfer, sale amount, at-sale property size,
legal use, or parcel identity on their own. Preserve `unknown`, `partial`,
`unsupported`, `timeout`, and conflicting states. Ask a human reviewer to resolve
material conflicts; do not fill gaps with current property attributes or a
model's guess. Do not call a result verified merely because the app rendered it.

Before completing the review, run the relevant app path using
`plotlot-verify-app`, then state separately what the UI showed and what the
official record proves. Do not initiate outreach or assert investment approval.
