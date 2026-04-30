# PRD — Agentic Land-Use and Site-Feasibility Consultant Harness

Date: 2026-04-30  
Branch: `feature/opencode-visual-ralph`  
Owner: PlotLot Ralph loop  
Status: Draft implementation charter  
Related local plans: `.omx/plans/prd-plotlot-workspace-harness.md`, `.omx/plans/test-spec-plotlot-workspace-harness.md`
Research trace: `docs/prd/2026-04-30-agentic-research-trace.md`  
Connector contracts: `docs/connector-contracts/municode.md`, `docs/connector-contracts/opendata-arcgis-socrata.md`, `docs/connector-contracts/workspace-connectors.md`

## 1. Product thesis

PlotLot should evolve from an AI zoning identification app into an **agentic land-use and site-feasibility consultant harness**: a governed workspace where users evaluate sites, assemble evidence, reason through ordinances/open data, and produce defensible reports/documents.

The primitive is not “chat with a zoning bot.” The primitive is:

```text
Workspace -> Project -> Site -> Analysis -> Evidence -> Report -> Document
```

This matters because users are not only asking “what zoning is this?” They are deciding whether a location works for a use case such as multifamily, self-storage, retail, industrial, or data centers. That work requires parcel facts, ownership, zoning, ordinance text, utilities/infrastructure, environmental constraints, incentives, schedule risk, permitting path, and source-backed recommendations.

## 2. Strategic decision: API vs MCP vs tools vs skills

### Recommendation

Build a **Land-Use Evidence Kernel** first, then expose it through three adapters:

1. **Internal typed service/tool contracts** — the canonical implementation boundary used by the PlotLot backend and agent runtime.
2. **REST/JSON API** — the stable product/platform boundary for the frontend, customer integrations, jobs, reports, and deterministic batch workflows.
3. **MCP server adapter** — the agent-native boundary so PlotLot tools can be used by the PlotLot agent and, later, by external AI clients that support MCP.

Use **skills/playbooks** for workflow instructions and repeatable procedures, not as the only integration boundary.

### Why not choose only one?

| Option | Best for | Weakness if used alone | PlotLot role |
| --- | --- | --- | --- |
| API | Product backend, frontend, customer integrations, auth, rate limits, logs, batch jobs, deterministic contracts | An agent still needs tool descriptions, affordance metadata, and context-routing patterns | Required stable platform boundary |
| MCP | Agent-native tool discovery and standardized connection to data/tools/workflows | Not the best primary product API; ecosystem and security models still require app-side tenancy/governance | Agent adapter over the same core services |
| Tool contracts | Agent harness internals, typed schema, replayable tool calls, eval parity | Not externally interoperable by itself | Canonical source of truth |
| Skills/playbooks | Procedural know-how: “run data-center screen,” “write rezoning memo,” “compile owner outreach list” | Not enough for multi-tenant auth, auditing, provenance, or public integrations | Workflow layer above tools |

### Direct answer to the user’s latest question

Yes: for Municode and OpenData, the **best route for programmatic agent reasoning is an API/MCP-style tool layer**, but the durable move is **not** “API or MCP.” It is:

```text
Municode/OpenData connectors
    -> normalized evidence services
    -> typed tool contracts
    -> REST API adapter + MCP adapter + PlotLot skills
```

The agent should never reason over raw scraped HTML when a structured tool result can provide:

- jurisdiction identity,
- source URL,
- retrieval timestamp,
- ordinance path,
- section text/snippet,
- field mapping confidence,
- geometry query parameters,
- cited evidence IDs,
- and replayable request/response metadata.

## 3. External research and reference-app inputs

### Research corpus note

The prior ChatGPT conversation refers to pasted arXiv URLs, but those exact URLs were not present in this repository context. This PRD therefore incorporates the currently accessible, relevant research sources reviewed for this Ralph iteration and leaves a research intake slot for the missing pasted corpus.

### Applied research takeaways

| Source | Takeaway for PlotLot |
| --- | --- |
| [Context Engineering survey](https://arxiv.org/abs/2507.13334) | Treat context as an engineered payload: retrieval, processing, management, memory, tool-integrated reasoning, and multi-agent composition. PlotLot needs a context broker, not just longer prompts. |
| [LLM Autonomous Agents survey](https://arxiv.org/abs/2308.11432) | Agent systems need explicit construction blocks: profile/role, memory, planning, action/tool use, and evaluation. PlotLot should model agent runs and evaluate them with gold cases. |
| [ReAct](https://arxiv.org/abs/2210.03629) | Interleave reasoning/planning with tool actions and observations. PlotLot should show tool/evidence events and allow the model to update plans when evidence contradicts assumptions. |
| [Toolformer](https://arxiv.org/abs/2302.04761) | Tools should be simple APIs with clear arguments/results; models improve when the tool call decision and result incorporation are explicit. PlotLot tool schemas must be precise and testable. |
| [Reflexion](https://arxiv.org/abs/2303.11366) | Keep feedback and reflections as episodic memory for retry loops. PlotLot should store analysis critiques, failed assumptions, and reviewer notes per site/project. |
| [MRKL systems](https://arxiv.org/abs/2205.00445) | Combine neural reasoning with discrete knowledge/reasoning modules. PlotLot should route deterministic zoning math, GIS queries, and document rendering outside the LLM. |
| [MCP docs](https://modelcontextprotocol.io/docs/getting-started/intro) | MCP is an open standard for connecting AI applications to data, tools, and workflows. PlotLot should expose a governed MCP server once the internal contracts stabilize. |

### Kimi Web UI reference

Reference: [Kimi Web UI docs](https://moonshotai.github.io/kimi-cli/en/reference/kimi-web.html), [Kimi web repo](https://github.com/MoonshotAI/kimi-cli/tree/main/web)

Borrow:

- session list/search/fork/archive patterns;
- visible agent activity status;
- queued follow-up messages during long runs;
- context usage/status bar concept;
- file/change/evidence style side rails;
- strong local/public access-control distinction.

Do not copy:

- local working directory as the primary abstraction;
- “open in terminal/editor” mental model;
- code-diff-first UX.

PlotLot’s equivalent abstractions should be project/site/analysis/evidence/report/document, not workdir/file/diff.

### pi-mono web-ui reference

Reference: [pi-mono web-ui README/tree](https://github.com/badlogic/pi-mono/tree/main/packages/web-ui)

Borrow:

- an agent chat panel split from artifacts/evidence panel;
- event-based agent state updates;
- attachments and extraction as first-class inputs;
- artifacts as persisted message types;
- IndexedDB/local storage patterns for drafts/settings where safe;
- sandboxed artifacts for generated HTML/SVG/Markdown previews.

Adapt to PlotLot:

- “Artifacts” become feasibility artifacts: evidence cards, maps, zoning tables, underwriting tables, report sections, and documents.
- “Tools” become governed land-use actions: ordinance search, parcel lookup, layer discovery, site scoring, report generation, CRM update.
- “Sessions” become project-scoped analysis runs.

## 4. Current repo baseline

Existing capabilities in PlotLot that become the first harness seams:

- `src/plotlot/api/chat.py`
  - tool registry includes `search_municode_live`, `discover_open_data_layers`, `search_properties`, Google Docs/Sheets export, web search, property lookup, and zoning ordinance search.
  - SSE stream already emits `tool_use` events.
- `src/plotlot/ingestion/discovery.py`
  - currently observes `https://library.municode.com/api` and stores Municode configuration/discovery logic.
- `src/plotlot/ingestion/scraper.py`
  - uses Municode API host patterns for content retrieval.
- `src/plotlot/property/universal.py`, `src/plotlot/property/hub_discovery.py`
  - dynamic ArcGIS Hub dataset discovery and provider mapping.
- `src/plotlot/retrieval/property.py`, `src/plotlot/retrieval/bulk_search.py`
  - county property appraiser integrations and bulk property search.
- `frontend/src/app/page.tsx`, `frontend/src/lib/api.ts`, `frontend/src/components/ToolCards.tsx`
  - current frontend agent/lookup surface with SSE and visible tool cards.
- `docs/runbooks/authenticated-test-matrix.md`
  - deterministic vs live credential-backed verification ladder.

## 5. Personas and jobs-to-be-done

### Personas

1. **Site-selection consultant** — evaluates many possible locations and needs fast evidence-backed ranking.
2. **Developer/acquisitions lead** — needs feasibility, entitlement risk, ownership, comps, and a memo/LOI-ready package.
3. **Data-center / industrial expansion team** — needs zoning plus power, fiber, water, sewer, environmental, setback, noise, and political/permitting risk.
4. **Broker / owner outreach operator** — needs ownership, contact context, CRM sync, documents, follow-up tasks.
5. **Municipal/planning analyst** — needs defensible source citations, ordinance excerpts, and repeatable assumptions.

### Core jobs

- “Given this site, tell me what can be built and why.”
- “Find sites in this county/state that fit a use case.”
- “Compare three candidate sites with cited evidence.”
- “Generate a report I can send to a partner/investor.”
- “Create follow-up tasks, calendar holds, emails, and CRM records.”
- “Show me exactly which ordinance sections and open-data layers support the conclusion.”

## 6. Product requirements

### 6.1 Workspace/project/site model

- Users work inside a workspace.
- Each workspace has projects.
- Each project has one or more sites.
- Each site can have multiple analyses.
- Each analysis produces evidence items, tool runs, report sections, and documents.
- Reports/documents must link back to evidence IDs.

### 6.2 Agent harness

The agent must operate as a governed harness, not an unconstrained chatbot.

Required harness primitives:

- tool registry with typed schemas;
- tool risk classes;
- per-workspace/per-project policy;
- event stream for runs/tool calls/evidence/approvals;
- context broker that builds a bounded, source-backed context payload;
- memory/reflection ledger for retry loops and reviewer feedback;
- deterministic calculators for zoning/density/underwriting math;
- gold-set evaluation harness for regression testing.

### 6.3 Municode ordinance layer

Municode should be treated as an **Ordinance Evidence Service**.

Required capabilities:

- Discover jurisdiction publication from state/county/municipality.
- Search ordinance text and headings.
- Fetch table of contents / code path.
- Fetch section text/snippets by node/section ID.
- Normalize source citation:
  - publisher,
  - jurisdiction,
  - code title/chapter/article/section,
  - URL,
  - retrieval timestamp,
  - effective/supplement date when available,
  - caveat that online code may not be official/current.
- Return evidence objects, not just text blobs.
- Support cached read-through with freshness policy.
- Respect publisher terms, robots, rate limits, and licensing.

Legal/product note: Municode/CivicPlus terms and site notices indicate limitations on content use and warn that online codes may not be the official/legal copy. Commercial API/MCP use requires legal review or licensed/municipality-authorized access. The product must cite sources and encourage official confirmation before action.

### 6.4 OpenData / ArcGIS layer

OpenData should be treated as a **Geospatial Evidence Service**.

Required capabilities:

- Discover parcel, zoning, land-use, flood, wetlands, utilities, transit, power, permitting, and economic-development layers.
- Infer schema and map fields to canonical PlotLot fields.
- Query FeatureServer/MapServer endpoints by address, APN/folio, owner, geometry, bounding box, or filters.
- Support pagination using object IDs/result offsets where services cap records.
- Capture source metadata:
  - ArcGIS item/layer URL,
  - service URL/layer ID,
  - query params,
  - out fields,
  - spatial reference,
  - retrieved timestamp,
  - publisher/update cadence if available.
- Store normalized records and raw response excerpts sufficient for replay/debugging.

### 6.5 Connectors and workspace integrations

Future connectors must be separated from core land-use evidence services.

Connector categories:

- **Google Calendar** — meetings, due dates, entitlement schedule reminders.
- **Gmail** — draft outreach, summarize threads, identify replies/commitments.
- **Google Drive/Docs/Sheets** — source docs, report exports, spreadsheet exports.
- **CRM** — contacts, accounts, opportunities, owner outreach history.
- **Workspace CRM** — PlotLot-native contacts/deals when external CRM is absent.
- **Remote gateways** — controlled execution or data access through customer-approved network gateways.

Connector rules:

- OAuth scopes must be minimal and explicit.
- Read actions and write actions are separate permissions.
- External writes require user approval by default.
- Every connector call writes an audit/event record.
- Connector data is never silently mixed into reports without source/provenance labels.

Connector contract requirement (typed tool boundary):

- Connector actions must be exposed as **typed tool contracts** with explicit risk classes.
- Draft-first pattern is mandatory:
  - internal drafts: `WRITE_INTERNAL` (safe, auditable, no external side effects)
  - external commits/sends: `WRITE_EXTERNAL` (approval-gated)
- Canonical initial tools (see `docs/connector-contracts/workspace-connectors.md`):
  - `draft_email` → internal outreach draft
  - `gmail_send_draft` → external send (approval required)
  - `draft_google_doc` → internal doc draft
  - `create_document`, `create_spreadsheet`, `export_dataset` → external Google Workspace writes (approval required)

### 6.6 Frontend UX requirements

The web app should feel like a consultant workbench.

Required surfaces:

- left rail: workspace/project/site navigation;
- center: agent conversation and analysis timeline;
- right rail: evidence/report/artifact panel;
- map panel: parcel/layers/site constraints;
- tool activity cards: currently running/completed/failed tools;
- approval panel: external writes, expensive searches, report publishing, CRM updates;
- report builder: cited sections, editable assumptions, exported documents;
- connector status: authenticated/missing/limited/scopes.

### 6.7 Distribution and sandboxing

The system must support both local developer testing and hosted multi-tenant usage.

Requirements:

- tenant/workspace isolation;
- auth-aware API requests;
- per-tool risk classes;
- execution sandbox for code/repl/document artifacts;
- network allowlists for connector/gateway execution;
- rate and budget controls per workspace/project/run;
- prompt-injection boundaries between external source text and tool policy;
- audit log for every tool and connector action.

## 7. Non-goals

- Do not bypass Municode/CivicPlus licensing or terms.
- Do not scrape or bulk-republish forbidden ordinance content.
- Do not allow the model to send emails, modify CRM records, or publish docs without approval.
- Do not make MCP the only product boundary.
- Do not make skills a substitute for typed, tested services.
- Do not collapse project/site/evidence/report into generic chat sessions.

## 8. Milestone plan

### Phase 0 — Planning and gold-set lock

- Create this PRD, architecture spec, and test spec.
- Choose 5–10 canonical test jurisdictions/sites.
- Seed `tests/golden/land_use_cases.json` with the first consultant-harness gold cases.
- Freeze expected evidence/report outputs as gold cases.
- Add a mutation-testing lane (`mutmut`) for harness/tool correctness and test-strength validation.

### Phase 1 — Evidence kernel and tool contracts

- Add normalized models for evidence, citations, tool runs, agent runs.
- Wrap existing Municode/OpenData functions in typed service ports.
- Add replayable request/response metadata.
- Add API/tool parity tests for existing tools.

### Phase 2 — Workspace harness API

- Add workspace/project/site/analysis/evidence/report endpoints.
- Introduce event stream for run/tool/evidence/approval events.
- Keep current `/api/v1/analyze`, `/api/v1/analyze/stream`, and `/api/v1/chat` compatible.

### Phase 3 — MCP adapter

- Expose core read-only tools through an MCP server:
  - `plotlot.search_ordinances`
  - `plotlot.fetch_ordinance_section`
  - `plotlot.discover_open_data_layers`
  - `plotlot.query_property_layer`
  - `plotlot.create_site_analysis`
  - `plotlot.list_evidence`
- Gate write/execution tools behind explicit approval.
- Add API/MCP parity tests.

### Phase 4 — Consultant workflows / skills

- Add workflow playbooks:
  - zoning feasibility memo;
  - data-center siting screen;
  - owner outreach packet;
  - rezoning risk memo;
  - site comparison matrix;
  - due-diligence document checklist.

### Phase 5 — Frontend workbench

- Add project/site route tree and shell.
- Replace one-off chat session mental model with project-scoped analyses.
- Add evidence/report side rail and map/layer explorer.
- Add live e2e tests against served frontend + backend.

## 9. Acceptance criteria

A feature slice is successful when:

- Existing lookup/chat behavior remains compatible.
- A project/site/analysis can be created and replayed.
- Agent tool calls emit structured events and produce evidence IDs.
- Municode/OpenData results include citations and retrieval metadata.
- A generated report cites evidence IDs rather than uncited prose.
- API and MCP adapters return equivalent normalized payloads for the same query.
- External writes are approval-gated.
- The first gold-set suite passes locally without live credentials.
- Live e2e can run when the required credential groups are present.
- Mutation testing can be run locally and is used to identify missing assertions in the harness/tool layer.

## 10. Open questions

1. Which exact arXiv URLs from the prior pasted research should be treated as authoritative for the full research appendix?
2. What jurisdictions/sites should seed the first gold-set: South Florida only, Florida statewide, or one state plus data-center target markets?
3. Will Municode access be licensed/authorized, or should the first product slice use only small cited snippets + live links + local user-provided documents?
4. Which CRM should be first: HubSpot, Salesforce, Attio, or PlotLot-native workspace CRM only?
5. Do we want external MCP clients in the first release, or only an internal MCP adapter for local agent testing?
