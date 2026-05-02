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
- Versioned agent snapshot
- Budget-gated evaluator
- Structured observation interface
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
- File-as-Bus workspace
- Progressive disclosure workspace map
- Explore/exploit error ledger
- Frontier + activatable-state summary
- Output survival metric
- User pushback telemetry
- Clarification gate

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

---

## VeRO (2602.22480)

- **Versioned agent snapshot**: capture each optimization/eval state as a discrete version with diffable changes, rollback, and replay semantics.
- **Budget-gated evaluator**: make evaluation itself a controlled resource; the harness should block or surface over-budget runs instead of silently allowing extra search.
- **Structured observation interface**: expose per-sample inputs, outputs, traces, errors, and scores in a consistent schema so different optimizers/scaffolds see the same evidence.
- **Instruction-sensitive optimization**: expect optimizer guidance to interact with target-agent maturity; more prescription can help simpler agents and constrain stronger ones.

PlotLot mapping:
- Every site-feasibility quality run should emit a manifest with git commit, prompt versions, dataset slice, thresholds, and observed metrics.
- Offline evals should support deterministic sample budgets now, then grow into tool/runtime/token budgets for future optimizer loops.
- Parcel facts, ordinance citations, calculator outputs, and failure labels should be saved as structured observations so retrieval/extraction/report changes can be compared fairly.
- PlotLot should distinguish prompt-only improvements from structural harness improvements and validate both against holdout jurisdictions.

---

## AiScientist (2604.13018v1)

- **File-as-Bus workspace**: use durable files as the coordination substrate instead of relying on conversational handoffs to carry project state.
- **Progressive disclosure workspace map**: let the orchestrator operate on a compact map/index of the workspace, while specialists read deeper artifacts on demand.
- **Thin control over thick state**: keep stage control small and stable, but persist large evolving state in analyses, code, plans, logs, and experiment outputs.
- **Permission-scoped artifact roles**: split paper understanding, runnable code, and execution logs into distinct writable regions to reduce interference and improve traceability.
- **Evidence-driven research loop**: implement → run → diagnose → patch → revalidate, with each round writing durable evidence for later refinement.

PlotLot mapping:
- Give every site-feasibility case a durable workspace with folders/artifacts for intake, authority discovery, ordinance retrieval, extraction, calculator outputs, review notes, and report drafts.
- Keep the PlotLot orchestrator focused on stage summaries, open questions, and evidence gaps; let specialists drill into raw zoning texts, GIS outputs, and calculation artifacts only when needed.
- Optimize PlotLot for later-round refinement: most hard cases will be won by preserving intermediate state and iterating, not by restarting with a bigger transcript.

---

## Exploration and Exploitation Errors Are Measurable for Language Model Agents (2604.13151v1)

- **Explore/exploit error ledger**: classify trajectory mistakes into exploration errors, exploitation errors, or both instead of scoring only end success.
- **Exploration-first under partial observability**: low exploration error is a much stronger predictor of success than low exploitation error when decisive information must first be discovered.
- **Frontier + activatable-state summary**: externalize visited space, reachable frontier, discovered entities, prerequisites, and ready-to-act states into explicit memory.
- **Behavioral eval over outcome-only eval**: agents with similar success can still have qualitatively different strategies, so traces need their own scoring vocabulary.
- **Semantic-prior stress test**: domain semantics can help or hurt depending on the model, so harnesses should gate conclusions on evidence rather than intuition-like priors.

PlotLot mapping:
- Maintain an explicit PlotLot frontier summary: verified official hosts, unresolved likely hosts, discovered ordinance sections, unresolved dimensional questions, and claims whose prerequisites are satisfied.
- Score land-use traces separately for search quality and synthesis quality so we can tell whether a failure came from missed discovery or bad reasoning after discovery.
- Treat report-ready feasibility claims as activatable states: they only advance once the official source, citation, unit normalization, and conflict checks are satisfied.

---

## SWE-chat (2604.20779v1)

- **Output survival metric**: judge agent usefulness by what survives human review into the final artifact, not by gross generated output.
- **User pushback telemetry**: corrections, rejections, failure reports, and interruptions are structured supervision signals about where the harness created friction.
- **Clarification gate**: when uncertainty is high, the harness should stop and ask the user before spending more autonomous effort on a likely-wrong trajectory.
- **Real-workflow trajectory benchmark**: evaluate on multi-turn, tool-using, human-steered sessions instead of only curated one-shot tasks.

PlotLot mapping:
- Measure which generated zoning claims, citations, and calculations survive into the final site-feasibility memo, and record whether losses came from analyst deletion, overwrite, or agent self-rewrite.
- Treat analyst pushback as a first-class improvement signal: unsupported setback claim, bad jurisdiction source, wrong unit normalization, premature conclusion, or poor report framing.
- Add explicit clarification gates whenever PlotLot lacks a verified authority source, sees conflicting ordinance evidence, or cannot justify a dimensional conclusion with citations.
- Build evals from real analyst review loops so the harness learns collaborative land-use work, not only synthetic benchmark completion.
