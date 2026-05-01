# PRD (North Star) — PlotLot Agentic Land‑Use & Site‑Feasibility Harness

- Date: 2026-04-30
- Scope: North-star product framing (not a single sprint)
- Execution slice PRD: `.omx/plans/prd-plotlot-workspace-harness.md`
- Architecture: `docs/architecture/agentic-land-use-harness.md`

## Executive summary

PlotLot is evolving from an **AI zoning lookup application** into a **workspace-native, agentic land-use and site-feasibility consultant harness**.

The bigger product is not just zoning identification. The bigger product is a system that helps users answer:

> Where can I build this, what blocks me, what evidence supports that, and what should I do next?

The core shift:

```text
Old PlotLot:
Address → Zoning Lookup → Report

New PlotLot:
Workspace → Project → Site → Analysis → Evidence → Report → Action
```

The model is not the product. The **harness** is the product.

## 1) Product vision

PlotLot should become:

> A workspace-native land-use and site-feasibility consultant harness that helps investors, developers, consultants, brokers, and businesses find, evaluate, document, and act on development opportunities.

PlotLot should support:

- Zoning research
- Parcel analysis
- Site selection
- Data-center site screening
- Multifamily feasibility
- Industrial/warehouse feasibility
- Environmental risk screening
- Utility and infrastructure screening
- Entitlement roadmap generation
- CRM-connected outreach
- Gmail and Calendar workflow integration
- Drive/document ingestion
- Consultant-grade report generation
- Evidence-backed decision-making

## 2) Core product model

Primary abstractions:

```text
Workspace
  → Project
    → Site
      → Analysis
        → Evidence
        → Report
        → Document
```

Definitions:

- **Workspace**: tenant + collaboration boundary; owns members, projects, connections, memories, governance settings.
- **Project**: an initiative (e.g., “NC Data Center Site Search”).
- **Site**: a parcel/assemblage candidate; holds address, parcel IDs, geometry, zoning, evidence.
- **Analysis**: a workflow run (zoning, site selection, environmental screening, outreach prep).
- **Evidence**: a source-backed fact with provenance and timestamps.
- **Report**: a generated deliverable with cited evidence.
- **Document**: saved/exportable artifact (PDF, Google Doc, spreadsheet, etc.).

## 3) Strategic reframing

PlotLot should not be framed as:

```text
AI zoning lookup
```

It should be framed as:

```text
AI site-feasibility intelligence
```

or:

```text
Agentic land-use and zoning consultant harness
```

The core primitive:

```text
Location-constrained development feasibility
```

This applies to:

- Data centers
- Warehouses
- Multifamily
- Industrial outdoor storage
- Self-storage
- EV charging
- Cold storage
- Manufacturing
- Renewable energy
- Retail expansion
- Cell towers
- Infill housing

## 4) Core research insight

The future of reliable AI agents is not just stronger models; it is better harnesses around models.

Principles:

1. Externalize cognition into memory, tools, skills, and protocols.
2. Use deterministic code for facts, calculations, and validation.
3. Use LLMs for reasoning, synthesis, explanation, and strategy.
4. Keep context small and specific.
5. Decompose work into bounded stages.
6. Test each stage with gold datasets.
7. Keep memory and skills app-owned (repo-owned), not provider-owned.
8. Govern tool execution at runtime.
9. Use evidence ledgers for trust.
10. Avoid giant prompts and unbounded tool catalogs.

```text
Model + Prompt = fragile
Model + Harness + Skills + Tools + Memory + Evidence + Tests = product
```

## 5) Architecture overview (conceptual)

```text
User / Client
  → Web UI / API / MCP
    → API Gateway
      → Workspace Service
        → Harness Runtime
          → Router
          → Context Broker
          → Skill Registry
          → Tool Executor
          → Governance Middleware
          → Memory Service
          → Evidence Ledger
          → Report Service
```

Layering:

- **Product API** is the stable product/integration boundary.
- **MCP** is an interoperability adapter (not the internal architecture).
- **Tools** are deterministic functions.
- **Skills** are workflows/playbooks that orchestrate tools.

## 6) Municode / ordinance strategy

Build a PlotLot **ordinance intelligence layer** that uses Municode as one source, rather than exposing raw Municode browsing as the primary mechanism.

Example internal endpoints:

```text
POST /api/v1/ordinances/search
GET  /api/v1/ordinances/sections/:section_id
POST /api/v1/ordinances/extract-rules
GET  /api/v1/zoning-rules
POST /api/v1/evidence/validate-claim
```

## 7) Runtime governance

Tool execution must be governed.

Risk classes:

```text
READ_ONLY
EXPENSIVE_READ
WRITE_INTERNAL
WRITE_EXTERNAL
EXECUTION
```

Approval required for:

- Sending emails
- Creating calendar events
- Updating CRM
- Exporting client-facing reports
- Running expensive searches
- Running sandbox code with network access

## 8) Evidence-backed reporting

Rules:

- Every factual claim needs evidence.
- Unsupported claims become assumptions or open questions.
- Numerical values require citations.
- Contradictions are surfaced.

Suggested report sections:

- Executive summary
- Site facts
- Zoning findings
- Utility findings
- Environmental constraints
- Entitlement pathway
- Risk register
- Open questions
- Recommendation
- Source appendix

## 9) Data-center site selection wedge

For data centers, never confirm deliverable MW capacity unless there is utility evidence. If unconfirmed, record as an open question.

Workflow:

```text
1. Parse requirements
2. Build site profile
3. Generate/search candidate parcels
4. Resolve parcel facts
5. Screen zoning
6. Screen utilities
7. Screen environmental risk
8. Score sites
9. Build risk register
10. Produce consultant memo
```

## 10) What PlotLot should not do

- Become just a chatbot.
- Depend on giant prompts.
- Depend on model-provider memory.
- Expose raw Municode directly as the product surface.
- Trust model outputs without validation.
- Store serious workspace state only in browser local storage.
- Allow high-risk actions without approval.

## 11) One-sentence summary

PlotLot is evolving from an AI zoning lookup app into a workspace-native, evidence-backed, agentic land-use and site-feasibility harness that combines zoning intelligence, GIS data, connected CRM/workflow systems, deterministic tools, repo-owned skills, sandboxed execution, and multi-agent reasoning to help users find, evaluate, document, and act on development opportunities.
