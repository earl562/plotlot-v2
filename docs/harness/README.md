# PlotLot Agentic Harness (Vertical: land-use / site-feasibility)

PlotLot’s product goal is **fast, trustworthy site feasibility** for builders/developers/investors.

This repo is evolving PlotLot v2 into an **agentic harness**: the surrounding infrastructure that makes an agent controllable, auditable, and reliable (tools, memory, evidence, governance, orchestration, evaluation).

## Non-negotiables

- **Backend is authoritative** (system of record for runs, memory, evidence, governance decisions).
- CLI/TUI + web UI are **clients**.
- Default posture is **least privilege** + **auditability by default**.

## Harness modules (target shape)

1. **Run + event ledger** (append-only)
   - records: user inputs, tool calls, tool results, policy decisions, compaction, errors
   - supports replay/debug + evidence attribution
2. **Evidence ledger**
   - every trust-critical claim should link to evidence (ordinance chunks, parcel sources, maps)
3. **Governance middleware**
   - tool permission modes, admission control, policy checks at boundaries
   - bounded recovery + rollback/degradation when anomalies accumulate
4. **Memory system**
   - write/manage/read loop across working + episodic + semantic + procedural memory
   - durable, inspectable, deletable
5. **Orchestration**
   - move from ad-hoc loops to explicit DAGs for repeatable feasibility workflows
6. **Evaluation + red-teaming**
   - harness-level security tests (prompt injection, tool tampering, memory poisoning)
   - vertical task evals (zoning accuracy, constraint completeness, provenance coverage)

## What’s implemented so far (backend)

- Harness runtime seam + APIs:
  - `POST /api/v1/harness/run` (routes + runs repo-owned skills via `HarnessRuntime`)
  - `GET /api/v1/mcp/tools` + `POST /api/v1/mcp/invoke` (thin MCP-style adapter over internal tools)
  - Ordinance intelligence endpoints:
    - `POST /api/v1/ordinances/search`
    - `GET /api/v1/ordinances/sections/{section_id}`
    - `POST /api/v1/ordinances/extract-rules`
    - `POST /api/v1/evidence/validate-claim`
- Durable chat transcript persistence:
  - `chat_messages` table + hydration on session resume
- Tool-call audit trail:
  - `chat_tool_calls` table + writes on each tool execution
- Tool governance (deny-by-default external writes):
  - `PLOTLOT_TOOL_PERMISSION_MODE=read_only|allow_writes`
- Retrieval endpoints (backend source of truth):
  - `GET /api/v1/chat/sessions/{session_id}/transcript`
  - `GET /api/v1/chat/sessions/{session_id}/tool-calls`
- “Live tools” for web-client use (agent mode):
  - `search_municode_live` (live Municode fallback when indexed chunks are weak/stale)
  - `discover_open_data_layers` (live ArcGIS/Hub dataset discovery by county + lat/lng)
- VeRO-style offline eval manifests for site-feasibility quality checks:
  - `apps/plotlot/src/plotlot/pipeline/eval_flow.py`
  - logs git commit, prompt versions, dataset path, thresholds, metrics, and sample budget as eval artifacts

## Research → implementation map

These reviewed notes drive design decisions:

- **Externalization** (why practical agents shift capability into memory/skills/protocols/harness):
  - `docs/research/arxiv-notes/2604.08224v1.md`
- **Claude Code design space** (permissions, compaction, extensibility):
  - `docs/research/arxiv-notes/2604.14228v1.md`
- **SafeHarness** (lifecycle-integrated defenses; rollback/degradation):
  - `docs/research/arxiv-notes/2604.13630v1.md`
- **ACP admission control** (deterministic, history-aware tool governance):
  - `docs/research/arxiv-notes/2603.18829v9.md`
- **Skills as procedural memory** (skill lifecycle + metadata; “skills as repo artifacts”):
  - `docs/research/vendor-notes/techrxiv__176857932_cloudfront.md`
- **Skill marketplace security** (supply-chain, auditing, trust tiers):
  - `docs/research/arxiv-notes/2601.10338v1.md`
  - `docs/research/arxiv-notes/2603.21019v1.md`
  - `docs/research/arxiv-notes/2602.20867v1.md`
- **Memory survey** (write–manage–read loop; eval metric stack):
  - `docs/research/arxiv-notes/2603.07670v1.md`
- **SemaClaw** (PermissionBridge, DAG Teams, three-tier context):
  - `docs/research/arxiv-notes/2604.11548v1.md`
- **SGH structured DAG harness** (immutable plans + bounded recovery escalation):
  - `docs/research/arxiv-notes/2604.11378v1.md`

## How we work (dev harness)

Use the pi dev extension Ralph loop (max 50 iters by default):

- In pi interactive: `/ralph <goal>`
- In headless RPC: `scripts/pi-ralph.sh --max 50 -- "<goal>"`

See also: `docs/research/arxiv-topdown-queue.md` for the next papers to review.
