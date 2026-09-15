# Six-county benchmark checkpoint

Scope: a credential-free, repeatable SDK diagnostic for Miami-Dade, Broward,
Palm Beach, Lee, Mecklenburg and Gaston. San Diego, sign-in, deployment and the
larger unpublished application-pipeline changes are excluded.

## Executed verification

Source/test candidate tree: `d77e3f54722cda960208954a38c2acb338fb8d06`.
Isolated export: `/tmp/plotlot-benchmark-final-20260914.igGFjN`.

- Full isolated unit suite: **2,169 passed**, 16.76 seconds. One existing
  Starlette/httpx deprecation warning; no dependency replacement attempted.
- Ruff lint passed; 478 source/test files passed format checking.
- Project mypy passed across 259 source files, with existing untyped-body notes.
- LSP was unavailable and installation had been declined; no LSP claim is made.
- New benchmark behavior suite: 19 passing cases, including operational-error
  retention, programmer-error propagation, invalid/future review dates, changed
  evidence/warnings, URL validation and unsupported-provider abstention.
- Direct county-source suite: 49 passed. Existing pipeline-dependent retention
  tests remain intact outside this standalone-source publication scope.
- Public ArcGIS declarations were moved to a focused model module while keeping
  all 13 original imports identical. Function/host-policy AST SHA-256 stayed
  `cc8382dc0ddba4cf0f089bb8b62b63a18fe76de5d2fac04e80026dd510c3b2b1`.

## Observed runtime behavior

The [saved live baseline](2026-09-14-six-county-baseline.jsonl) contains actual
working-checkout output, two observations per county. Miami-Dade varied from
3,000 partial candidates to an unavailable timeout; the other five were stable.
All six were not ready and all accepted-comp sets were empty.

A subsequent isolated six-county run at tree
`5988d77d2a010e5852b5b04a5f58d4d5b07f7e49` completed with expected exit 1.
Miami-Dade recovered to two matching partial sets of 3,000; Broward returned
1,877 and Palm Beach 3,797, both partial. Lee, Mecklenburg and Gaston remained
unsupported for sales. Four supported identity lookups matched their seeds.
CLI help exited 0; invalid evaluation-date input exited 2.

The final source delta from that live-tested tree only narrows expected exception
handling so generic programming ValueErrors propagate; two failing-first tests
cover that change and are included in the final full-suite result above.

No AI-provider calls, database writes, auth changes or owned server processes were
needed. These results do not certify the browser application or production readiness.
The [benchmark guide](six-county-benchmark.md) records missing evidence and the
required expansion beyond one diagnostic property per county.
