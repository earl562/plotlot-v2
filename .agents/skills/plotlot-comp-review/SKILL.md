---
name: plotlot-comp-review
description: Review PlotLot comparable sale candidates and qualification results when a user needs reliable closed-sale comps for a parcel.
---

# Review comparable sales

First apply `plotlot-source-review` to the subject and each candidate. The
current decision contract is `plotlot/src/plotlot/comps/models.py`,
`qualification_rules.py`, and `qualification.py`. Inspect those files before
assuming a policy value still applies. Do not substitute an agent's preferred
comp list for the deterministic `qualify_comps()` result.

At this branch baseline, `CompPolicy` defaults to three required comps, up to
five selected, within three miles and twelve months, with a 30% size tolerance.
The code also checks closed status, qualification, jurisdiction, parcel identity,
sale date and amount, category and property type, source reference, conflicts,
and other comparability factors. County, recorder, and attested user-reviewed
records may qualify if their required fields are present. Listing-only and
unknown sources do not. Keep every rejection reason visible.

If fewer than the minimum qualify, report `insufficient_evidence` and no
valuation range. Identify whether missing records, source access, timeouts,
or real mismatches caused it. Underwriting may consume only qualified comps;
it must not choose or manufacture them. Run a relevant app scenario with
`plotlot-verify-app` and separate the browser result from source verification.
