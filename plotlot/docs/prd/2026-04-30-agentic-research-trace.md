# Agentic Harness Research Trace

> PRD: `.omx/plans/prd-agentic-land-use-harness.md`
> Architecture: `docs/architecture/agentic-land-use-harness.md`

Purpose: make the research-to-design mapping explicit so the PRD does not merely assert “we incorporated arXiv/agent research.”

## Design implications by source

| Source | Relevant idea | PlotLot design implication |
|---|---|---|
| Context Engineering survey (arXiv: `2507.13334`) | Context is an engineered payload: retrieval, management, tool integration, memory | Build a Context Broker that produces bounded packets from project/site/evidence state; do not rely on transcript-only prompts |
| LLM Autonomous Agents survey (arXiv: `2308.11432`) | Agent systems need explicit blocks: memory, planning, action/tool use, eval | Model agent runs/tool runs and evaluate against gold cases (not just prose quality) |
| ReAct (arXiv: `2210.03629`) | Interleave reasoning with tool actions/observations | UI and logs must show tool/evidence events; runtime must allow plan updates when evidence contradicts assumptions |
| Toolformer (arXiv: `2302.04761`) | Tools should have precise input/output and be called explicitly | PlotLot tools must be schema-first and testable; prefer specific tools over “browse” |
| Reflexion (arXiv: `2303.11366`) | Store feedback/reflection as episodic memory for retries | Persist review notes and failed assumptions per analysis run as part of harness state |
| MRKL systems (arXiv: `2205.00445`) | Combine neural reasoning with deterministic modules | Route zoning math, GIS queries, exports, and report rendering outside the LLM |
| ADORE (arXiv: `2601.18267`) | Evidence bank / coverage-driven trustworthy RAG | Persist a claim→evidence graph; synthesize reports only from recorded evidence IDs |
| A-RAG (arXiv: `2602.03442`) | Hierarchical retrieval interfaces outperform one-shot RAG | Provide staged retrieval tools: discover→search→read exact sections/features |
| SoK Agentic RAG (arXiv: `2603.07379`) | Agentic RAG is sequential with memory/tool risks | Treat external content as untrusted; score intermediate steps and refuse/escalate on insufficient evidence |
| Claw-Eval (arXiv: `2604.06132`) | Output-only grading misses unsafe/lucky trajectories | Add trajectory metrics (tool order, evidence capture, refusal/escalation) to gold-set evals |
| OWASP AI Agent Security Cheat Sheet | Prompt injection, data exfiltration, tool misuse are system threats | Enforce server-side policy and least privilege; validate/sanitize tool outputs before model context |
| OWASP MCP Tool Poisoning | Tool descriptions/responses can carry malicious instructions | MCP adapter cannot bypass policy; treat tool outputs as untrusted data and validate schemas |

## Non-negotiable requirements carried into PlotLot

1. Every trust-critical conclusion must cite evidence.
2. Reports/documents may only synthesize from selected evidence IDs.
3. External content (HTML/PDF/OCR/email/CRM notes) is untrusted by default.
4. External writes require explicit approval.
5. Evals must grade the workflow trajectory, not only final prose.
6. Refusal/escalation is correct behavior when evidence is stale, contradictory, unofficial, or insufficient.

## Eval dimensions PlotLot must score

- Claim grounding: citation precision, unsupported-claim rate, claim-to-evidence coverage.
- Retrieval quality: relevant-section recall; overlay/amendment recall; stale-source detection.
- Tool use: correct tool selection/args; unnecessary-call rate; evidence-writing completeness.
- Planning: question decomposition; evidence coverage before synthesis; escalation on ambiguity.
- Security: prompt-injection interception; malicious tool-response handling; data-exfiltration prevention.
- Approval behavior: approval trigger precision/recall; preview quality; unsafe auto-approval rate.
- Reliability: repeatability; failure recovery; cost per completed memo.
