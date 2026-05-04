---
url: https://ucp.dev/documentation/ucp-and-ap2/
status: reviewed
retrieved_at: 2026-05-04
---

# UCP — UCP and AP2

## What it is

A short doc page describing **UCP** compatibility with **Agent Payments Protocol (AP2)**, positioning AP2 as a trust layer for agent-led transactions.

## Key ideas worth copying

- **Verifiable, scoped authorizations**: use cryptographic binding so an authorization applies to a specific cart/session state (prevents replay / mutation).
- **Evidence of agreement**: both sides have proof of what was offered and accepted.
- **Agentic readiness**: enable autonomous agents to act within verifiable boundaries.

## How it maps to PlotLot

- Directly analogous to **tool governance**:
  - tool calls should be bound to the specific inputs/evidence set
  - outputs should be signed/hashed and auditable when used to justify downstream actions

## Source URLs

- https://ucp.dev/documentation/ucp-and-ap2/
