# Harness primitives (consolidated)

A running, paper-backed list of harness/agent engineering primitives we can reuse for PlotLot’s land-use / site-feasibility agents.

## Primitives index

- Signature-driven initialization / playbooks
- Interactive state introspection
- Deterministic replay / time-travel debugging
- Context compaction + sandboxed distillation
- Closed-loop validation
- Tool abstraction + guardrails
- Executable specification
- Step-bounded context
- Workflow module interface
- Replayable trajectory
- Workflow verification
- Agent-supervised tool adaptation
- Adaptation signal design
- Graduated subagent
- Skill handbook
- Competence-cost agent profile
- Contrastive skill discovery
- Granularity-aware handbook selection
- Context refresh + notes recall
- Failure manifestation catalog
- Controlled exploration discipline

---

## DebugHarness (2604.03610v1)

- **Signature-driven initialization**: parse incident/crash signature → inject type-specific troubleshooting heuristics + explicit rules of engagement.
- **Interactive state introspection**: live debugger/tool control plus deterministic replay to test hypotheses against real runtime state.
- **Static↔dynamic bridge**: map runtime frames/symbols to source locations/snippets.
- **Context compaction**: summarize verbose tool outputs; allow sandboxed scripts over raw outputs to extract signal.
- **Closed-loop validation**: patch → rebuild → rerun PoC/tests; distill failures back into context.
- **Tool abstraction + guardrails**: standardized tool protocol + command validation layers.

PlotLot mapping:
- Replace crash signature with an analysis signature.
- Replace debugger introspection with evidence introspection.
- Replace patch validation with report/evidence validation.

---

## AgentSPEX (2604.13346v1)

- **Executable specification**: keep workflow logic in repo-owned artifacts instead of burying it in controller code.
- **Step-bounded context**: decide explicitly when a stage gets a fresh context vs a persistent one.
- **Workflow module interface**: unify tools, skills, and subagents behind typed parameters and returns.
- **Replayable trajectory**: checkpoint each stage and support selective replay.
- **Workflow verification**: attach preconditions/postconditions to steps and verify the realized trajectory.

PlotLot mapping:
- Site-feasibility should run as a stage graph: intake → retrieve → extract → verify → calculate → report → review.
- Every stage boundary should become a replay and verification boundary.

---

## Adaptation of Agentic AI (2512.16301v3)

- **Agent-supervised tool adaptation**: freeze the orchestrator and improve peripheral specialists under its supervision.
- **Adaptation signal design**: separate dense execution-grounded signals from sparse end-to-end utility signals.
- **Graduated subagent**: once a specialist is reliable, freeze it behind a reusable interface and redeploy it as a stable module.
- **Frozen-core / adaptive-periphery**: mature systems trend toward a stable center with evolving retrieval, memory, review, and planning specialists.

PlotLot mapping:
- Default to T2-style adaptation for ordinance retrieval, zoning extraction, evidence review, and memory curation.
- Use dense signals where possible (citation resolution, parser correctness, calculator reproducibility) and holistic signals only for end-to-end report quality.

---

## SkillOrchestra (2602.19672v1)

- **Skill handbook**: keep routing knowledge in an explicit artifact with mode-selection insights, a skill registry, and per-agent profiles.
- **Competence-cost agent profile**: estimate per-skill success probability and mode-specific cost for each agent, then route on utility instead of raw model prestige.
- **Contrastive skill discovery**: learn new skills by contrasting successful vs failed trajectories at the same mode to isolate the missing capability.
- **Granularity-aware handbook selection**: more skills are not always better; select a coarser or finer handbook based on what the orchestrator can reliably distinguish.
- **Routing-collapse mitigation**: monitor whether the orchestrator degenerates to one expensive model/tool path and rebalance with explicit skill-conditioned routing.

PlotLot mapping:
- Build a PlotLot handbook over modes like authority discovery, ordinance retrieval, extraction/normalization, deterministic calculation, and report/review.
- Track agent profiles for specialist lanes such as parcel-authority resolution, ordinance section retrieval, table extraction, dimensional normalization, conflict arbitration, and citation-backed synthesis.
- Learn and refine skills from replayed site-feasibility traces instead of RL-tuning the orchestrator; start coarse, then split skills only when eval variance proves the distinction matters.

---

## UltraHorizon (2509.21766)

- **Context refresh + notes recall (CRNR)**: once a run approaches context limits, drop stale dialogue, keep the governing prompt, and reconstruct working state from durable notes.
- **Failure manifestation catalog**: diagnose long-horizon runs with explicit labels like repetitive looping, premature convergence, misaligned tool usage, memory issues, uncontrolled experiments, and environment mis-modeling.
- **Controlled exploration discipline**: more steps do not help unless the harness enforces hypothesis-testing structure and evidence thresholds.
- **Human-gap realism**: benchmark with partially observable, multi-tool tasks where humans still outperform agents; do not assume short-horizon wins transfer.

PlotLot mapping:
- Long site-feasibility runs should checkpoint evidence/notes aggressively, then refresh active context from those artifacts instead of hauling full transcripts forward.
- PlotLot evals should explicitly score premature commit, low-yield retrieval looping, conflicting-source confusion, and uncontrolled ordinance experimentation.
- Zoning ambiguity resolution should require single-variable-style testing: change one assumption at a time, record the result, and only then revise the site-feasibility hypothesis.
