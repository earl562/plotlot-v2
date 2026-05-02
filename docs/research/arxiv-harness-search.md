# Paperclip-style arXiv search report

Generated: 2026-05-02T00:21:29.277Z
Profile: harness-agents
Queries: 8

> Note: this is a Paperclip-style workflow for arXiv. The actual Paperclip product currently targets biomedical corpora (bioRxiv/medRxiv/PMC), so this report reproduces the search/discovery pattern against PlotLot's arXiv corpus and the arXiv API.

## Existing arXiv papers already in the vault/repo

### Top aggregate matches

- [2505.02279v2](https://arxiv.org/abs/2505.02279v2) — A survey of agent interoperability protocols: Model Context Protocol (MCP), Agent Communication Protocol (ACP), Agent-to-Agent Protocol (A2A), and Agent Network Protocol (ANP) — score 720 — reviewed
  - matched queries: agent harness, multi-agent systems, agent orchestration, agent runtime governance, agent memory skills
  - matched terms: agent, multi, systems, runtime
  - category: cs.AI
- [2604.13346v1](https://arxiv.org/abs/2604.13346v1) — AgentSPEX: An Agent SPecification and EXecution Language — score 686 — reviewed
  - matched queries: harness engineering agents, agent harness, long-horizon agents, terminal agents, multi-agent systems, agent orchestration, agent runtime governance, agent memory skills
  - matched terms: harness, agents, agent, long, systems, orchestration
  - category: cs.CL
- [2603.20380v1](https://arxiv.org/abs/2603.20380v1) — ALARA for Agents: Least-Privilege Context Engineering Through Portable Composable Multi-Agent Teams — score 594 — reviewed
  - matched queries: agent harness, multi-agent systems, agent orchestration, agent runtime governance, agent memory skills
  - matched terms: agent, harness, multi, systems
  - category: cs.MA
- [2512.16301v3](https://arxiv.org/abs/2512.16301v3) — Adaptation of Agentic AI: A Survey of Post-Training, Memory, and Skills — score 503 — reviewed
  - matched queries: agent harness, multi-agent systems, agent orchestration, agent runtime governance, agent memory skills
  - matched terms: agent, systems, memory, skills
  - category: cs.AI
- [2601.21123v2](https://arxiv.org/abs/2601.21123v2) — CUA-Skill: Develop Skills for Computer Using Agent — score 304 — stub
  - matched queries: multi-agent systems, agent orchestration, agent runtime governance, agent memory skills
  - matched terms: agent, systems, memory, skills
  - category: cs.AI
- [2602.12430v3](https://arxiv.org/abs/2602.12430v3) — Agent Skills for Large Language Models: Architecture, Acquisition, Security, and the Path Forward — score 302 — reviewed
  - matched queries: multi-agent systems, agent orchestration, agent runtime governance, agent memory skills
  - matched terms: agent, systems, governance, skills
  - category: cs.MA
- [2604.19572v2](https://arxiv.org/abs/2604.19572v2) — A Self-Evolving Framework for Efficient Terminal Agents via Observational Context Compression — score 259 — stub
  - matched queries: long-horizon agents, terminal agents
  - matched terms: long, horizon, agents, terminal
  - category: cs.CL
- [2603.25723v1](https://arxiv.org/abs/2603.25723v1) — Natural-Language Agent Harnesses — score 258 — reviewed
  - matched queries: harness engineering agents, agent harness
  - matched terms: harness, engineering, agent
  - category: cs.CL
- [2602.19672v1](https://arxiv.org/abs/2602.19672v1) — SkillOrchestra: Learning to Route Agents via Skill Transfer — score 248.6 — reviewed
  - matched queries: long-horizon agents, terminal agents, multi-agent systems, agent orchestration
  - matched terms: long, horizon, agents, multi, agent, systems, orchestration
  - category: cs.AI
- [2603.27813v1](https://arxiv.org/abs/2603.27813v1) — MuSEAgent: A Multimodal Reasoning Agent with Stateful Experiences — score 241 — stub
  - matched queries: multi-agent systems, agent orchestration, agent runtime governance
  - matched terms: multi, agent
  - category: cs.CV
- [2603.08616v1](https://arxiv.org/abs/2603.08616v1) — Coverage-Guided Multi-Agent Harness Generation for Java Library Fuzzing — score 234 — stub
  - matched queries: harness engineering agents, agent harness
  - matched terms: harness, agents, agent
  - category: cs.SE
- [2601.03204v1](https://arxiv.org/abs/2601.03204v1) — InfiAgent: An Infinite-Horizon Framework for General-Purpose Autonomous Agents — score 227 — stub
  - matched queries: long-horizon agents, agent orchestration, agent runtime governance
  - matched terms: long, horizon, agents, agent
  - category: cs.AI

### Query: harness engineering agents

- [2604.11548v1](https://arxiv.org/abs/2604.11548v1) — SemaClaw: A Step Towards General-Purpose Personal AI Agents through Harness Engineering — score 100 — reviewed
  - category: cs.AI
  - The rise of OpenClaw in early 2026 marks the moment when millions of users began deploying personal AI agents into their daily lives, delegating tasks ranging from travel planning to multi-step research. This scale of adoption signals that two parallel arcs of development have re
- [2604.21003v2](https://arxiv.org/abs/2604.21003v2) — The Last Harness You'll Ever Build — score 80 — stub
  - category: cs.AI
  - AI agents are increasingly deployed on complex, domain-specific workflows -- navigating enterprise web applications that require dozens of clicks and form fills, orchestrating multi-step research pipelines that span search, extraction, and synthesis, automating code review across
- [2603.28052v1](https://arxiv.org/abs/2603.28052v1) — Meta-Harness: End-to-End Optimization of Model Harnesses — score 76 — reviewed
  - category: cs.AI
  - The performance of large language model (LLM) systems depends not only on model weights, but also on their harness: the code that determines what information to store, retrieve, and present to the model. Yet harnesses are still designed largely by hand, and existing text optimize
- [2604.08224v1](https://arxiv.org/abs/2604.08224v1) — Externalization in LLM Agents: A Unified Review of Memory, Skills, Protocols and Harness Engineering — score 75 — reviewed
  - category: cs.SE
  - Large language model (LLM) agents are increasingly built less by changing model weights than by reorganizing the runtime around them. Capabilities that earlier systems expected the model to recover internally are now externalized into memory stores, reusable skills, interaction p
- [2603.03329v1](https://arxiv.org/abs/2603.03329v1) — AutoHarness: improving LLM agents by automatically synthesizing a code harness — score 68 — stub
  - category: cs.CL
  - Despite significant strides in language models in the last few years, when used as agents, such models often try to perform actions that are not just suboptimal for a given state, but are strictly prohibited by the external environment. For example, in the recent Kaggle GameArena
- [2603.08616v1](https://arxiv.org/abs/2603.08616v1) — Coverage-Guided Multi-Agent Harness Generation for Java Library Fuzzing — score 65 — stub
  - category: cs.SE
  - Coverage-guided fuzzing has proven effective for software testing, but targeting library code requires specialized fuzz harnesses that translate fuzzer-generated inputs into valid API invocations. Manual harness creation is time-consuming and requires deep understanding of API se
- [2603.02239v1](https://arxiv.org/abs/2603.02239v1) — Engineering Reasoning and Instruction (ERI) Benchmark: A Large Taxonomy-driven Dataset for Foundation Models and Agents — score 64 — stub
  - category: cs.AI
  - The Engineering Reasoning and Instruction (ERI) benchmark is a taxonomy-driven instruction dataset designed to train and evaluate engineering-capable large language models (LLMs) and agents. This dataset spans nine engineering fields (namely: civil, mechanical, electrical, chemic
- [2603.25723v1](https://arxiv.org/abs/2603.25723v1) — Natural-Language Agent Harnesses — score 62 — reviewed
  - category: cs.CL
  - Agent performance increasingly depends on \emph{harness engineering}, yet harness design is usually buried in controller code and runtime-specific conventions, making it hard to transfer, compare, and study as a scientific object. We ask whether the high-level control logic of an
- [2604.13630v1](https://arxiv.org/abs/2604.13630v1) — SafeHarness: Lifecycle-Integrated Security Architecture for LLM-based Agent Deployment — score 62 — reviewed
  - category: cs.CR
  - The performance of large language model (LLM) agents depends critically on the execution harness, the system layer that orchestrates tool use, context management, and state persistence. Yet this same architectural centrality makes the harness a high-value attack surface: a single
- [2603.05344v3](https://arxiv.org/abs/2603.05344v3) — Building Effective AI Coding Agents for the Terminal: Scaffolding, Harness, Context Engineering, and Lessons Learned — score 58 — stub
  - category: cs.AI
  - The landscape of AI coding assistance is undergoing a fundamental shift from complex IDE plugins to versatile, terminal-native agents. Operating directly where developers manage source control, execute builds, and deploy environments, CLI-based agents offer unprecedented autonomy
- [2604.13346v1](https://arxiv.org/abs/2604.13346v1) — AgentSPEX: An Agent SPecification and EXecution Language — score 57 — reviewed
  - category: cs.CL
  - Language-model agent systems commonly rely on reactive prompting, in which a single instruction guides the model through an open-ended sequence of reasoning and tool-use steps, leaving control flow and intermediate state implicit and making agent behavior potentially difficult to
- [2604.03610v1](https://arxiv.org/abs/2604.03610v1) — DebugHarness: Emulating Human Dynamic Debugging for Autonomous Program Repair — score 52 — reviewed
  - category: cs.SE
  - Patching severe security flaws in complex software remains a major challenge. While automated tools like fuzzers efficiently discover bugs, fixing deep-rooted low-level faults (e.g., use-after-free and memory corruption) still requires labor-intensive manual analysis by experts. 

### Query: agent harness

- [2603.25723v1](https://arxiv.org/abs/2603.25723v1) — Natural-Language Agent Harnesses — score 196 — reviewed
  - category: cs.CL
  - Agent performance increasingly depends on \emph{harness engineering}, yet harness design is usually buried in controller code and runtime-specific conventions, making it hard to transfer, compare, and study as a scientific object. We ask whether the high-level control logic of an
- [2603.08616v1](https://arxiv.org/abs/2603.08616v1) — Coverage-Guided Multi-Agent Harness Generation for Java Library Fuzzing — score 169 — stub
  - category: cs.SE
  - Coverage-guided fuzzing has proven effective for software testing, but targeting library code requires specialized fuzz harnesses that translate fuzzer-generated inputs into valid API invocations. Manual harness creation is time-consuming and requires deep understanding of API se
- [2604.18071v1](https://arxiv.org/abs/2604.18071v1) — Architectural Design Decisions in AI Agent Harnesses — score 141 — reviewed
  - category: cs.AI
  - AI agent systems increasingly rely on reusable non-LLM engineering infrastructure that packages tool mediation, context handling, delegation, safety control, and orchestration. Yet the architectural design decisions in this surrounding infrastructure remain understudied. This pap
- [2505.02279v2](https://arxiv.org/abs/2505.02279v2) — A survey of agent interoperability protocols: Model Context Protocol (MCP), Agent Communication Protocol (ACP), Agent-to-Agent Protocol (A2A), and Agent Network Protocol (ANP) — score 138 — reviewed
  - category: cs.AI
  - Large language model powered autonomous agents demand robust, standardized protocols to integrate tools, share contextual data, and coordinate tasks across heterogeneous systems. Ad-hoc integrations are difficult to scale, secure, and generalize across domains. This survey examin
- [2604.13346v1](https://arxiv.org/abs/2604.13346v1) — AgentSPEX: An Agent SPecification and EXecution Language — score 136 — reviewed
  - category: cs.CL
  - Language-model agent systems commonly rely on reactive prompting, in which a single instruction guides the model through an open-ended sequence of reasoning and tool-use steps, leaving control flow and intermediate state implicit and making agent behavior potentially difficult to
- [2603.20380v1](https://arxiv.org/abs/2603.20380v1) — ALARA for Agents: Least-Privilege Context Engineering Through Portable Composable Multi-Agent Teams — score 131 — reviewed
  - category: cs.MA
  - Industry practitioners and academic researchers regularly use multi-agent systems to accelerate their work, yet the frameworks through which these systems operate do not provide a simple, unified mechanism for scalably managing the critical aspects of the agent harness, impacting
- [2603.19347v3](https://arxiv.org/abs/2603.19347v3) — Exploring the Agentic Frontier of Verilog Code Generation — score 100 — stub
  - category: cs.AR
  - Large language models (LLMs) have made rapid advancements in code generation for popular languages such as Python and C++. Many of these recent gains can be attributed to the use of ``agents'' that wrap domain-relevant tools alongside LLMs. Hardware design languages such as Veril
- [2512.16301v3](https://arxiv.org/abs/2512.16301v3) — Adaptation of Agentic AI: A Survey of Post-Training, Memory, and Skills — score 87 — reviewed
  - category: cs.AI
  - Large language model (LLM) agents are moving beyond prompting alone. ChatGPT marked the rise of general-purpose LLM assistants, DeepSeek showed that on-policy reinforcement learning with verifiable rewards can improve reasoning and tool use, and OpenClaw highlights a newer direct
- [2604.03610v1](https://arxiv.org/abs/2604.03610v1) — DebugHarness: Emulating Human Dynamic Debugging for Autonomous Program Repair — score 87 — reviewed
  - category: cs.SE
  - Patching severe security flaws in complex software remains a major challenge. While automated tools like fuzzers efficiently discover bugs, fixing deep-rooted low-level faults (e.g., use-after-free and memory corruption) still requires labor-intensive manual analysis by experts. 
- [2604.11548v1](https://arxiv.org/abs/2604.11548v1) — SemaClaw: A Step Towards General-Purpose Personal AI Agents through Harness Engineering — score 86 — reviewed
  - category: cs.AI
  - The rise of OpenClaw in early 2026 marks the moment when millions of users began deploying personal AI agents into their daily lives, delegating tasks ranging from travel planning to multi-step research. This scale of adoption signals that two parallel arcs of development have re
- [2604.13630v1](https://arxiv.org/abs/2604.13630v1) — SafeHarness: Lifecycle-Integrated Security Architecture for LLM-based Agent Deployment — score 86 — reviewed
  - category: cs.CR
  - The performance of large language model (LLM) agents depends critically on the execution harness, the system layer that orchestrates tool use, context management, and state persistence. Yet this same architectural centrality makes the harness a high-value attack surface: a single
- [2603.28088v1](https://arxiv.org/abs/2603.28088v1) — GEMS: Agent-Native Multimodal Generation with Memory and Skills — score 85 — stub
  - category: cs.CV
  - Recent multimodal generation models have achieved remarkable progress on general-purpose generation tasks, yet continue to struggle with complex instructions and specialized downstream tasks. Inspired by the success of advanced agent frameworks such as Claude Code, we propose \te

### Query: long-horizon agents

- [2601.03204v1](https://arxiv.org/abs/2601.03204v1) — InfiAgent: An Infinite-Horizon Framework for General-Purpose Autonomous Agents — score 99 — stub
  - category: cs.AI
  - LLM agents can reason and use tools, but they often break down on long-horizon tasks due to unbounded context growth and accumulated errors. Common remedies such as context compression or retrieval-augmented prompting introduce trade-offs between information fidelity and reasonin
- [2604.13018v1](https://arxiv.org/abs/2604.13018v1) — Toward Autonomous Long-Horizon Engineering for ML Research — score 79 — stub
  - category: cs.CL
  - Autonomous AI research has advanced rapidly, but long-horizon ML research engineering remains difficult: agents must sustain coherent progress across task comprehension, environment setup, implementation, experimentation, and debugging over hours or days. We introduce AiScientist
- [2512.03627v1](https://arxiv.org/abs/2512.03627v1) — MemVerse: Multimodal Memory for Lifelong Learning Agents — score 64 — stub
  - category: cs.AI
  - Despite rapid progress in large-scale language and vision models, AI agents still suffer from a fundamental limitation: they cannot remember. Without reliable memory, agents catastrophically forget past experiences, struggle with long-horizon reasoning, and fail to operate cohere
- [2602.22680v2](https://arxiv.org/abs/2602.22680v2) — Toward Personalized LLM-Powered Agents: Foundations, Evaluation, and Future Directions — score 55 — stub
  - category: cs.AI
  - Large language models have enabled agentic systems that reason, plan, and interact with tools and environments to accomplish complex tasks. As these agents operate over extended interaction horizons, their effectiveness increasingly depends on adapting behavior to individual user
- [2604.13346v1](https://arxiv.org/abs/2604.13346v1) — AgentSPEX: An Agent SPecification and EXecution Language — score 52 — reviewed
  - category: cs.CL
  - Language-model agent systems commonly rely on reactive prompting, in which a single instruction guides the model through an open-ended sequence of reasoning and tool-use steps, leaving control flow and intermediate state implicit and making agent behavior potentially difficult to
- [2604.19572v2](https://arxiv.org/abs/2604.19572v2) — A Self-Evolving Framework for Efficient Terminal Agents via Observational Context Compression — score 50 — stub
  - category: cs.CL
  - As terminal agents scale to long-horizon, multi-turn workflows, a key bottleneck is not merely limited context length, but the accumulation of noisy terminal observations in the interaction history. Retaining raw observations preserves useful environment feedback, but also leads 
- [2602.19672v1](https://arxiv.org/abs/2602.19672v1) — SkillOrchestra: Learning to Route Agents via Skill Transfer — score 47.6 — reviewed
  - category: cs.AI
  - Compound AI systems promise capabilities beyond those of individual models, yet their success depends critically on effective orchestration. Existing routing approaches face two limitations: (1) input-level routers make coarse query-level decisions that ignore evolving task requi
- [2602.16069v2](https://arxiv.org/abs/2602.16069v2) — The Limits of Long-Context Reasoning in Automated Bug Fixing — score 47 — reviewed
  - category: cs.SE
  - Rapidly increasing context lengths have led to the assumption that large language models (LLMs) can directly reason over entire codebases. Concurrently, recent advances in LLMs have enabled strong performance on software engineering benchmarks, particularly when paired with agent
- [2504.19413v1](https://arxiv.org/abs/2504.19413v1) — Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory — score 44 — stub
  - category: cs.CL
  - Large Language Models (LLMs) have demonstrated remarkable prowess in generating contextually coherent responses, yet their fixed context windows pose fundamental challenges for maintaining consistency over prolonged multi-session dialogues. We introduce Mem0, a scalable memory-ce
- [2512.04535v2](https://arxiv.org/abs/2512.04535v2) — GTM: Simulating the World of Tools for AI Agents — score 40 — stub
  - category: cs.AI
  - The integration of external tools is pivotal for empowering Large Language Model (LLM) agents with real-world capabilities. However, training these agents through direct, continuous interaction with diverse tools is often prohibitively expensive, slow, and introduces additional d
- [2604.11784v1](https://arxiv.org/abs/2604.11784v1) — ClawGUI: A Unified Framework for Training, Evaluating, and Deploying GUI Agents — score 40 — stub
  - category: cs.LG
  - GUI agents drive applications through their visual interfaces instead of programmatic APIs, interacting with arbitrary software via taps, swipes, and keystrokes, reaching a long tail of applications that CLI-based agents cannot. Yet progress in this area is bottlenecked less by m
- [2602.20867v1](https://arxiv.org/abs/2602.20867v1) — SoK: Agentic Skills -- Beyond Tool Use in LLM Agents — score 37 — reviewed
  - category: cs.CR
  - Agentic systems increasingly rely on reusable procedural capabilities, \textit{a.k.a., agentic skills}, to execute long-horizon workflows reliably. These capabilities are callable modules that package procedural knowledge with explicit applicability conditions, execution policies

### Query: terminal agents

- [2604.19572v2](https://arxiv.org/abs/2604.19572v2) — A Self-Evolving Framework for Efficient Terminal Agents via Observational Context Compression — score 209 — stub
  - category: cs.CL
  - As terminal agents scale to long-horizon, multi-turn workflows, a key bottleneck is not merely limited context length, but the accumulation of noisy terminal observations in the interaction history. Retaining raw observations preserves useful environment feedback, but also leads 
- [2603.05344v3](https://arxiv.org/abs/2603.05344v3) — Building Effective AI Coding Agents for the Terminal: Scaffolding, Harness, Context Engineering, and Lessons Learned — score 49 — stub
  - category: cs.AI
  - The landscape of AI coding assistance is undergoing a fundamental shift from complex IDE plugins to versatile, terminal-native agents. Operating directly where developers manage source control, execute builds, and deploy environments, CLI-based agents offer unprecedented autonomy
- [2604.13346v1](https://arxiv.org/abs/2604.13346v1) — AgentSPEX: An Agent SPecification and EXecution Language — score 47 — reviewed
  - category: cs.CL
  - Language-model agent systems commonly rely on reactive prompting, in which a single instruction guides the model through an open-ended sequence of reasoning and tool-use steps, leaving control flow and intermediate state implicit and making agent behavior potentially difficult to
- [2602.22680v2](https://arxiv.org/abs/2602.22680v2) — Toward Personalized LLM-Powered Agents: Foundations, Evaluation, and Future Directions — score 40 — stub
  - category: cs.AI
  - Large language models have enabled agentic systems that reason, plan, and interact with tools and environments to accomplish complex tasks. As these agents operate over extended interaction horizons, their effectiveness increasingly depends on adapting behavior to individual user
- [2602.19672v1](https://arxiv.org/abs/2602.19672v1) — SkillOrchestra: Learning to Route Agents via Skill Transfer — score 38 — reviewed
  - category: cs.AI
  - Compound AI systems promise capabilities beyond those of individual models, yet their success depends critically on effective orchestration. Existing routing approaches face two limitations: (1) input-level routers make coarse query-level decisions that ignore evolving task requi
- [2603.10664v1](https://arxiv.org/abs/2603.10664v1) — Terminal Is All You Need: Design Properties for Human-AI Agent Collaboration — score 35 — stub
  - category: cs.HC
  - While research on AI agents focuses on enabling them to operate graphical user interfaces, the most effective and widely adopted agent tools in practice are terminal-based. We argue that this convergence is not coincidental. It reflects three design properties central to effectiv
- [2604.11784v1](https://arxiv.org/abs/2604.11784v1) — ClawGUI: A Unified Framework for Training, Evaluating, and Deploying GUI Agents — score 35 — stub
  - category: cs.LG
  - GUI agents drive applications through their visual interfaces instead of programmatic APIs, interacting with arbitrary software via taps, swipes, and keystrokes, reaching a long tail of applications that CLI-based agents cannot. Yet progress in this area is bottlenecked less by m
- [2603.07670v1](https://arxiv.org/abs/2603.07670v1) — Memory for Autonomous LLM Agents:Mechanisms, Evaluation, and Emerging Frontiers — score 32 — reviewed
  - category: cs.AI
  - Large language model (LLM) agents increasingly operate in settings where a single context window is far too small to capture what has happened, what was learned, and what should not be repeated. Memory -- the ability to persist, organize, and selectively recall information across
- [2604.11548v1](https://arxiv.org/abs/2604.11548v1) — SemaClaw: A Step Towards General-Purpose Personal AI Agents through Harness Engineering — score 32 — reviewed
  - category: cs.AI
  - The rise of OpenClaw in early 2026 marks the moment when millions of users began deploying personal AI agents into their daily lives, delegating tasks ranging from travel planning to multi-step research. This scale of adoption signals that two parallel arcs of development have re
- [2506.08119v2](https://arxiv.org/abs/2506.08119v2) — SOP-Bench: Complex Industrial SOPs for Evaluating LLM Agents — score 30 — stub
  - category: cs.AI
  - LLM-based agents struggle to execute complex, multi-step Standard Operating Procedures (SOPs) that are fundamental to industrial automation. Existing benchmarks fail to capture the procedural complexity and tool orchestration demands of real-world workflows. We introduce SOP-Benc
- [2512.03627v1](https://arxiv.org/abs/2512.03627v1) — MemVerse: Multimodal Memory for Lifelong Learning Agents — score 30 — stub
  - category: cs.AI
  - Despite rapid progress in large-scale language and vision models, AI agents still suffer from a fundamental limitation: they cannot remember. Without reliable memory, agents catastrophically forget past experiences, struggle with long-horizon reasoning, and fail to operate cohere
- [2512.04535v2](https://arxiv.org/abs/2512.04535v2) — GTM: Simulating the World of Tools for AI Agents — score 30 — stub
  - category: cs.AI
  - The integration of external tools is pivotal for empowering Large Language Model (LLM) agents with real-world capabilities. However, training these agents through direct, continuous interaction with diverse tools is often prohibitively expensive, slow, and introduces additional d

### Query: multi-agent systems

- [2603.20380v1](https://arxiv.org/abs/2603.20380v1) — ALARA for Agents: Least-Privilege Context Engineering Through Portable Composable Multi-Agent Teams — score 175 — reviewed
  - category: cs.MA
  - Industry practitioners and academic researchers regularly use multi-agent systems to accelerate their work, yet the frameworks through which these systems operate do not provide a simple, unified mechanism for scalably managing the critical aspects of the agent harness, impacting
- [2505.02279v2](https://arxiv.org/abs/2505.02279v2) — A survey of agent interoperability protocols: Model Context Protocol (MCP), Agent Communication Protocol (ACP), Agent-to-Agent Protocol (A2A), and Agent Network Protocol (ANP) — score 163 — reviewed
  - category: cs.AI
  - Large language model powered autonomous agents demand robust, standardized protocols to integrate tools, share contextual data, and coordinate tasks across heterogeneous systems. Ad-hoc integrations are difficult to scale, secure, and generalize across domains. This survey examin
- [2604.02334v1](https://arxiv.org/abs/2604.02334v1) — Holos: A Web-Scale LLM-Based Multi-Agent System for the Agentic Web — score 123 — stub
  - category: cs.AI
  - As large language models (LLM)-driven agents transition from isolated task solvers to persistent digital entities, the emergence of the Agentic Web, an ecosystem where heterogeneous agents autonomously interact and co-evolve, marks a pivotal shift toward Artificial General Intell
- [2603.27813v1](https://arxiv.org/abs/2603.27813v1) — MuSEAgent: A Multimodal Reasoning Agent with Stateful Experiences — score 103 — stub
  - category: cs.CV
  - Research agents have recently achieved significant progress in information seeking and synthesis across heterogeneous textual and visual sources. In this paper, we introduce MuSEAgent, a multimodal reasoning agent that enhances decision-making by extending the capabilities of res
- [2604.13346v1](https://arxiv.org/abs/2604.13346v1) — AgentSPEX: An Agent SPecification and EXecution Language — score 101 — reviewed
  - category: cs.CL
  - Language-model agent systems commonly rely on reactive prompting, in which a single instruction guides the model through an open-ended sequence of reasoning and tool-use steps, leaving control flow and intermediate state implicit and making agent behavior potentially difficult to
- [2512.16301v3](https://arxiv.org/abs/2512.16301v3) — Adaptation of Agentic AI: A Survey of Post-Training, Memory, and Skills — score 97 — reviewed
  - category: cs.AI
  - Large language model (LLM) agents are moving beyond prompting alone. ChatGPT marked the rise of general-purpose LLM assistants, DeepSeek showed that on-policy reinforcement learning with verifiable rewards can improve reasoning and tool use, and OpenClaw highlights a newer direct
- [2603.22148v1](https://arxiv.org/abs/2603.22148v1) — OpenEarth-Agent: From Tool Calling to Tool Creation for Open-Environment Earth Observation — score 87 — reviewed
  - category: cs.CV
  - Earth Observation (EO) is essential for perceiving dynamic land surface changes, yet deploying autonomous EO in open environments is hindered by the immense diversity of multi-source data and heterogeneous tasks. While remote sensing agents have emerged to streamline EO workflows
- [2603.21019v1](https://arxiv.org/abs/2603.21019v1) — SkillProbe: Security Auditing for Emerging Agent Skill Marketplaces via Multi-Agent Collaboration — score 85 — reviewed
  - category: cs.CR
  - With the rapid evolution of Large Language Model (LLM) agent ecosystems, centralized skill marketplaces have emerged as pivotal infrastructure for augmenting agent capabilities. However, these marketplaces face unprecedented security challenges, primarily stemming from semantic-b
- [2603.28088v1](https://arxiv.org/abs/2603.28088v1) — GEMS: Agent-Native Multimodal Generation with Memory and Skills — score 84 — stub
  - category: cs.CV
  - Recent multimodal generation models have achieved remarkable progress on general-purpose generation tasks, yet continue to struggle with complex instructions and specialized downstream tasks. Inspired by the success of advanced agent frameworks such as Claude Code, we propose \te
- [2602.19672v1](https://arxiv.org/abs/2602.19672v1) — SkillOrchestra: Learning to Route Agents via Skill Transfer — score 77 — reviewed
  - category: cs.AI
  - Compound AI systems promise capabilities beyond those of individual models, yet their success depends critically on effective orchestration. Existing routing approaches face two limitations: (1) input-level routers make coarse query-level decisions that ignore evolving task requi
- [2601.21123v2](https://arxiv.org/abs/2601.21123v2) — CUA-Skill: Develop Skills for Computer Using Agent — score 75 — stub
  - category: cs.AI
  - Computer-Using Agents (CUAs) aim to autonomously operate computer systems to complete real-world tasks. However, existing agentic systems remain difficult to scale and lag behind human performance. A key limitation is the absence of reusable and structured skill abstractions that
- [2602.12430v3](https://arxiv.org/abs/2602.12430v3) — Agent Skills for Large Language Models: Architecture, Acquisition, Security, and the Path Forward — score 72 — reviewed
  - category: cs.MA
  - The transition from monolithic language models to modular, skill-equipped agents marks a defining shift in how large language models (LLMs) are deployed in practice. Rather than encoding all procedural knowledge within model weights, agent skills -- composable packages of instruc

### Query: agent orchestration

- [2505.02279v2](https://arxiv.org/abs/2505.02279v2) — A survey of agent interoperability protocols: Model Context Protocol (MCP), Agent Communication Protocol (ACP), Agent-to-Agent Protocol (A2A), and Agent Network Protocol (ANP) — score 138 — reviewed
  - category: cs.AI
  - Large language model powered autonomous agents demand robust, standardized protocols to integrate tools, share contextual data, and coordinate tasks across heterogeneous systems. Ad-hoc integrations are difficult to scale, secure, and generalize across domains. This survey examin
- [2604.13346v1](https://arxiv.org/abs/2604.13346v1) — AgentSPEX: An Agent SPecification and EXecution Language — score 101 — reviewed
  - category: cs.CL
  - Language-model agent systems commonly rely on reactive prompting, in which a single instruction guides the model through an open-ended sequence of reasoning and tool-use steps, leaving control flow and intermediate state implicit and making agent behavior potentially difficult to
- [2603.20380v1](https://arxiv.org/abs/2603.20380v1) — ALARA for Agents: Least-Privilege Context Engineering Through Portable Composable Multi-Agent Teams — score 96 — reviewed
  - category: cs.MA
  - Industry practitioners and academic researchers regularly use multi-agent systems to accelerate their work, yet the frameworks through which these systems operate do not provide a simple, unified mechanism for scalably managing the critical aspects of the agent harness, impacting
- [2512.16301v3](https://arxiv.org/abs/2512.16301v3) — Adaptation of Agentic AI: A Survey of Post-Training, Memory, and Skills — score 87 — reviewed
  - category: cs.AI
  - Large language model (LLM) agents are moving beyond prompting alone. ChatGPT marked the rise of general-purpose LLM assistants, DeepSeek showed that on-policy reinforcement learning with verifiable rewards can improve reasoning and tool use, and OpenClaw highlights a newer direct
- [2602.19672v1](https://arxiv.org/abs/2602.19672v1) — SkillOrchestra: Learning to Route Agents via Skill Transfer — score 86 — reviewed
  - category: cs.AI
  - Compound AI systems promise capabilities beyond those of individual models, yet their success depends critically on effective orchestration. Existing routing approaches face two limitations: (1) input-level routers make coarse query-level decisions that ignore evolving task requi
- [2604.20779v1](https://arxiv.org/abs/2604.20779v1) — SWE-chat: Coding Agent Interactions From Real Users in the Wild — score 70 — stub
  - category: cs.AI
  - AI coding agents are being adopted at scale, yet we lack empirical evidence on how people actually use them and how much of their output is useful in practice. We present SWE-chat, the first large-scale dataset of real coding agent sessions collected from open-source developers i
- [2603.27813v1](https://arxiv.org/abs/2603.27813v1) — MuSEAgent: A Multimodal Reasoning Agent with Stateful Experiences — score 69 — stub
  - category: cs.CV
  - Research agents have recently achieved significant progress in information seeking and synthesis across heterogeneous textual and visual sources. In this paper, we introduce MuSEAgent, a multimodal reasoning agent that enhances decision-making by extending the capabilities of res
- [2603.22148v1](https://arxiv.org/abs/2603.22148v1) — OpenEarth-Agent: From Tool Calling to Tool Creation for Open-Environment Earth Observation — score 67 — reviewed
  - category: cs.CV
  - Earth Observation (EO) is essential for perceiving dynamic land surface changes, yet deploying autonomous EO in open environments is hindered by the immense diversity of multi-source data and heterogeneous tasks. While remote sensing agents have emerged to streamline EO workflows
- [2601.21123v2](https://arxiv.org/abs/2601.21123v2) — CUA-Skill: Develop Skills for Computer Using Agent — score 65 — stub
  - category: cs.AI
  - Computer-Using Agents (CUAs) aim to autonomously operate computer systems to complete real-world tasks. However, existing agentic systems remain difficult to scale and lag behind human performance. A key limitation is the absence of reusable and structured skill abstractions that
- [2601.03204v1](https://arxiv.org/abs/2601.03204v1) — InfiAgent: An Infinite-Horizon Framework for General-Purpose Autonomous Agents — score 64 — stub
  - category: cs.AI
  - LLM agents can reason and use tools, but they often break down on long-horizon tasks due to unbounded context growth and accumulated errors. Common remedies such as context compression or retrieval-augmented prompting introduce trade-offs between information fidelity and reasonin
- [2604.02334v1](https://arxiv.org/abs/2604.02334v1) — Holos: A Web-Scale LLM-Based Multi-Agent System for the Agentic Web — score 64 — stub
  - category: cs.AI
  - As large language models (LLM)-driven agents transition from isolated task solvers to persistent digital entities, the emergence of the Agentic Web, an ecosystem where heterogeneous agents autonomously interact and co-evolve, marks a pivotal shift toward Artificial General Intell
- [2602.12430v3](https://arxiv.org/abs/2602.12430v3) — Agent Skills for Large Language Models: Architecture, Acquisition, Security, and the Path Forward — score 62 — reviewed
  - category: cs.MA
  - The transition from monolithic language models to modular, skill-equipped agents marks a defining shift in how large language models (LLMs) are deployed in practice. Rather than encoding all procedural knowledge within model weights, agent skills -- composable packages of instruc

### Query: agent runtime governance

- [2505.02279v2](https://arxiv.org/abs/2505.02279v2) — A survey of agent interoperability protocols: Model Context Protocol (MCP), Agent Communication Protocol (ACP), Agent-to-Agent Protocol (A2A), and Agent Network Protocol (ANP) — score 143 — reviewed
  - category: cs.AI
  - Large language model powered autonomous agents demand robust, standardized protocols to integrate tools, share contextual data, and coordinate tasks across heterogeneous systems. Ad-hoc integrations are difficult to scale, secure, and generalize across domains. This survey examin
- [2604.07833v2](https://arxiv.org/abs/2604.07833v2) — Harnessing Embodied Agents: Runtime Governance for Policy-Constrained Execution — score 130 — reviewed
  - category: cs.RO
  - Embodied agents are evolving from passive reasoning systems into active executors that interact with tools, robots, and physical environments. Once granted execution authority, the central challenge becomes how to keep actions governable at runtime. Existing approaches embed safe
- [2603.20380v1](https://arxiv.org/abs/2603.20380v1) — ALARA for Agents: Least-Privilege Context Engineering Through Portable Composable Multi-Agent Teams — score 96 — reviewed
  - category: cs.MA
  - Industry practitioners and academic researchers regularly use multi-agent systems to accelerate their work, yet the frameworks through which these systems operate do not provide a simple, unified mechanism for scalably managing the critical aspects of the agent harness, impacting
- [2604.13346v1](https://arxiv.org/abs/2604.13346v1) — AgentSPEX: An Agent SPecification and EXecution Language — score 96 — reviewed
  - category: cs.CL
  - Language-model agent systems commonly rely on reactive prompting, in which a single instruction guides the model through an open-ended sequence of reasoning and tool-use steps, leaving control flow and intermediate state implicit and making agent behavior potentially difficult to
- [2512.16301v3](https://arxiv.org/abs/2512.16301v3) — Adaptation of Agentic AI: A Survey of Post-Training, Memory, and Skills — score 87 — reviewed
  - category: cs.AI
  - Large language model (LLM) agents are moving beyond prompting alone. ChatGPT marked the rise of general-purpose LLM assistants, DeepSeek showed that on-policy reinforcement learning with verifiable rewards can improve reasoning and tool use, and OpenClaw highlights a newer direct
- [2604.20779v1](https://arxiv.org/abs/2604.20779v1) — SWE-chat: Coding Agent Interactions From Real Users in the Wild — score 70 — stub
  - category: cs.AI
  - AI coding agents are being adopted at scale, yet we lack empirical evidence on how people actually use them and how much of their output is useful in practice. We present SWE-chat, the first large-scale dataset of real coding agent sessions collected from open-source developers i
- [2603.27813v1](https://arxiv.org/abs/2603.27813v1) — MuSEAgent: A Multimodal Reasoning Agent with Stateful Experiences — score 69 — stub
  - category: cs.CV
  - Research agents have recently achieved significant progress in information seeking and synthesis across heterogeneous textual and visual sources. In this paper, we introduce MuSEAgent, a multimodal reasoning agent that enhances decision-making by extending the capabilities of res
- [2602.12430v3](https://arxiv.org/abs/2602.12430v3) — Agent Skills for Large Language Models: Architecture, Acquisition, Security, and the Path Forward — score 67 — reviewed
  - category: cs.MA
  - The transition from monolithic language models to modular, skill-equipped agents marks a defining shift in how large language models (LLMs) are deployed in practice. Rather than encoding all procedural knowledge within model weights, agent skills -- composable packages of instruc
- [2603.22148v1](https://arxiv.org/abs/2603.22148v1) — OpenEarth-Agent: From Tool Calling to Tool Creation for Open-Environment Earth Observation — score 67 — reviewed
  - category: cs.CV
  - Earth Observation (EO) is essential for perceiving dynamic land surface changes, yet deploying autonomous EO in open environments is hindered by the immense diversity of multi-source data and heterogeneous tasks. While remote sensing agents have emerged to streamline EO workflows
- [2602.20867v1](https://arxiv.org/abs/2602.20867v1) — SoK: Agentic Skills -- Beyond Tool Use in LLM Agents — score 66 — reviewed
  - category: cs.CR
  - Agentic systems increasingly rely on reusable procedural capabilities, \textit{a.k.a., agentic skills}, to execute long-horizon workflows reliably. These capabilities are callable modules that package procedural knowledge with explicit applicability conditions, execution policies
- [2601.21123v2](https://arxiv.org/abs/2601.21123v2) — CUA-Skill: Develop Skills for Computer Using Agent — score 65 — stub
  - category: cs.AI
  - Computer-Using Agents (CUAs) aim to autonomously operate computer systems to complete real-world tasks. However, existing agentic systems remain difficult to scale and lag behind human performance. A key limitation is the absence of reusable and structured skill abstractions that
- [2601.03204v1](https://arxiv.org/abs/2601.03204v1) — InfiAgent: An Infinite-Horizon Framework for General-Purpose Autonomous Agents — score 64 — stub
  - category: cs.AI
  - LLM agents can reason and use tools, but they often break down on long-horizon tasks due to unbounded context growth and accumulated errors. Common remedies such as context compression or retrieval-augmented prompting introduce trade-offs between information fidelity and reasonin

### Query: agent memory skills

- [2512.16301v3](https://arxiv.org/abs/2512.16301v3) — Adaptation of Agentic AI: A Survey of Post-Training, Memory, and Skills — score 145 — reviewed
  - category: cs.AI
  - Large language model (LLM) agents are moving beyond prompting alone. ChatGPT marked the rise of general-purpose LLM assistants, DeepSeek showed that on-policy reinforcement learning with verifiable rewards can improve reasoning and tool use, and OpenClaw highlights a newer direct
- [2505.02279v2](https://arxiv.org/abs/2505.02279v2) — A survey of agent interoperability protocols: Model Context Protocol (MCP), Agent Communication Protocol (ACP), Agent-to-Agent Protocol (A2A), and Agent Network Protocol (ANP) — score 138 — reviewed
  - category: cs.AI
  - Large language model powered autonomous agents demand robust, standardized protocols to integrate tools, share contextual data, and coordinate tasks across heterogeneous systems. Ad-hoc integrations are difficult to scale, secure, and generalize across domains. This survey examin
- [2602.20867v1](https://arxiv.org/abs/2602.20867v1) — SoK: Agentic Skills -- Beyond Tool Use in LLM Agents — score 120 — reviewed
  - category: cs.CR
  - Agentic systems increasingly rely on reusable procedural capabilities, \textit{a.k.a., agentic skills}, to execute long-horizon workflows reliably. These capabilities are callable modules that package procedural knowledge with explicit applicability conditions, execution policies
- [2602.02474v1](https://arxiv.org/abs/2602.02474v1) — MemSkill: Learning and Evolving Memory Skills for Self-Evolving Agents — score 115 — reviewed
  - category: cs.CL
  - Most Large Language Model (LLM) agent memory systems rely on a small set of static, hand-designed operations for extracting memory. These fixed procedures hard-code human priors about what to store and how to revise memory, making them rigid under diverse interaction patterns and
- [2602.12670v3](https://arxiv.org/abs/2602.12670v3) — SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks — score 108 — stub
  - category: cs.AI
  - Agent Skills are structured packages of procedural knowledge that augment LLM agents at inference time. Despite rapid adoption, there is no standard way to measure whether they actually help. We present SkillsBench, a benchmark of 86 tasks across 11 domains paired with curated Sk
- [2602.12430v3](https://arxiv.org/abs/2602.12430v3) — Agent Skills for Large Language Models: Architecture, Acquisition, Security, and the Path Forward — score 101 — reviewed
  - category: cs.MA
  - The transition from monolithic language models to modular, skill-equipped agents marks a defining shift in how large language models (LLMs) are deployed in practice. Rather than encoding all procedural knowledge within model weights, agent skills -- composable packages of instruc
- [2604.08224v1](https://arxiv.org/abs/2604.08224v1) — Externalization in LLM Agents: A Unified Review of Memory, Skills, Protocols and Harness Engineering — score 100 — reviewed
  - category: cs.SE
  - Large language model (LLM) agents are increasingly built less by changing model weights than by reorganizing the runtime around them. Capabilities that earlier systems expected the model to recover internally are now externalized into memory stores, reusable skills, interaction p
- [2601.21123v2](https://arxiv.org/abs/2601.21123v2) — CUA-Skill: Develop Skills for Computer Using Agent — score 99 — stub
  - category: cs.AI
  - Computer-Using Agents (CUAs) aim to autonomously operate computer systems to complete real-world tasks. However, existing agentic systems remain difficult to scale and lag behind human performance. A key limitation is the absence of reusable and structured skill abstractions that
- [2603.07670v1](https://arxiv.org/abs/2603.07670v1) — Memory for Autonomous LLM Agents:Mechanisms, Evaluation, and Emerging Frontiers — score 96 — reviewed
  - category: cs.AI
  - Large language model (LLM) agents increasingly operate in settings where a single context window is far too small to capture what has happened, what was learned, and what should not be repeated. Memory -- the ability to persist, organize, and selectively recall information across
- [2603.20380v1](https://arxiv.org/abs/2603.20380v1) — ALARA for Agents: Least-Privilege Context Engineering Through Portable Composable Multi-Agent Teams — score 96 — reviewed
  - category: cs.MA
  - Industry practitioners and academic researchers regularly use multi-agent systems to accelerate their work, yet the frameworks through which these systems operate do not provide a simple, unified mechanism for scalably managing the critical aspects of the agent harness, impacting
- [2604.13346v1](https://arxiv.org/abs/2604.13346v1) — AgentSPEX: An Agent SPecification and EXecution Language — score 96 — reviewed
  - category: cs.CL
  - Language-model agent systems commonly rely on reactive prompting, in which a single instruction guides the model through an open-ended sequence of reasoning and tool-use steps, leaving control flow and intermediate state implicit and making agent behavior potentially difficult to
- [2602.08004v1](https://arxiv.org/abs/2602.08004v1) — Agent Skills: A Data-Driven Analysis of Claude Skills for Extending Large Language Model Functionality — score 93 — stub
  - category: cs.SE
  - Agent skills extend large language model (LLM) agents with reusable, program-like modules that define triggering conditions, procedural logic, and tool interactions. As these skills proliferate in public marketplaces, it is unclear what types are available, how users adopt them, 

## New arXiv discovery candidates

Remote matches considered: 87
Since: 2024-01-01

### Top new candidates not already in the vault

- [2604.27358v1](https://arxiv.org/abs/2604.27358v1) — Safe Bilevel Delegation (SBD): A Formal Framework for Runtime Delegation Safety in Multi-Agent Systems — score 174
  - updated: 2026-04-30T03:15:05Z
  - category: cs.AI
  - matched queries: multi-agent systems
  - As large language model (LLM) agents are deployed in high-stakes environments, the question of how safely to delegate subtasks to specialized sub-agents becomes critical. Existing work addresses multi-agent architecture selection at design time or provides broad empirical guideli
- [2604.25917v1](https://arxiv.org/abs/2604.25917v1) — Recursive Multi-Agent Systems — score 174
  - updated: 2026-04-28T17:59:34Z
  - category: cs.AI
  - matched queries: multi-agent systems
  - Recursive or looped language models have recently emerged as a new scaling axis by iteratively refining the same model computation over latent states to deepen reasoning. We extend such scaling principle from a single model to multi-agent systems, and ask: Can agent collaboration
- [2604.24477v1](https://arxiv.org/abs/2604.24477v1) — GAMMAF: A Common Framework for Graph-Based Anomaly Monitoring Benchmarking in LLM Multi-Agent Systems — score 174
  - updated: 2026-04-27T13:45:14Z
  - category: cs.CR
  - matched queries: multi-agent systems
  - The rapid integration of Large Language Models (LLMs) into Multi-Agent Systems (MAS) has significantly enhanced their collaborative problem-solving capabilities, but it has also expanded their attack surfaces, exposing them to vulnerabilities such as prompt infection and compromi
- [2604.25850v3](https://arxiv.org/abs/2604.25850v3) — Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses — score 162
  - updated: 2026-04-30T17:34:17Z
  - category: cs.CL
  - matched queries: agent harness
  - Harnesses are now central to coding-agent performance, mediating how models interact with tools and execution environments. Yet harness engineering remains a manual craft, because automating it faces a heterogeneous action space across editable components, voluminous trajectories
- [2604.26053v1](https://arxiv.org/abs/2604.26053v1) — I Would If I Could: Reasoning about Dynamics of Actions in Multi-Agent Systems — score 162
  - updated: 2026-04-28T18:43:23Z
  - category: cs.LO
  - matched queries: multi-agent systems
  - Autonomous agents acting in realistic Multi-Agent Systems (MAS) should be able to adapt during their execution. Standard strategic logics, such as Alternating-time Temporal Logic (ATL), model agents' state- or history-dependent behaviour. However, the dynamic treatment of agents'
- [2604.07236v4](https://arxiv.org/abs/2604.07236v4) — How Much Heavy Lifting Can an Agent Harness Do?: Measuring the LLM's Residual Role in a Planning Agent — score 158
  - updated: 2026-04-28T14:27:47Z
  - category: cs.AI
  - matched queries: agent harness
  - Agent harnesses -- the stateful programs that wrap a language model and decide what it sees at each step -- are now known to change end-to-end performance on a fixed model by as much as six times. That raises a question asked less often than it should be: how much of an agent's c
- [2604.19856v1](https://arxiv.org/abs/2604.19856v1) — ChipCraftBrain: Validation-First RTL Generation via Multi-Agent Orchestration — score 150
  - updated: 2026-04-21T17:20:24Z
  - category: cs.AR
  - matched queries: agent orchestration
  - Large Language Models (LLMs) show promise for generating Register-Transfer Level (RTL) code from natural language specifications, but single-shot generation achieves only 60-65% functional correctness on standard benchmarks. Multi-agent approaches such as MAGE reach 95.9% on Veri
- [2604.25602v2](https://arxiv.org/abs/2604.25602v2) — OxyGent: Making Multi-Agent Systems Modular, Observable, and Evolvable via Oxy Abstraction — score 146
  - updated: 2026-04-29T14:40:10Z
  - category: cs.AI
  - matched queries: multi-agent systems
  - Deploying production-ready multi-agent systems (MAS) in complex industrial environments remains challenging due to limitations in scalability, observability, and autonomous evolution. We present OxyGent, an open-source framework driven by two core novelties: a unified Oxy abstrac
- [2604.20801v1](https://arxiv.org/abs/2604.20801v1) — Synthesizing Multi-Agent Harnesses for Vulnerability Discovery — score 142
  - updated: 2026-04-22T17:27:40Z
  - category: cs.CR
  - matched queries: agent harness
  - LLM agents have begun to find real security vulnerabilities that human auditors and automated fuzzers missed for decades, in source-available targets where the analyst can build and instrument the code. In practice the work is split among several agents, wired together by a harne
- [2604.00073v2](https://arxiv.org/abs/2604.00073v2) — Terminal Agents Suffice for Enterprise Automation — score 142
  - updated: 2026-04-03T15:48:53Z
  - category: cs.SE
  - matched queries: terminal agents
  - There has been growing interest in building agents that can interact with digital platforms to execute meaningful enterprise tasks autonomously. Among the approaches explored are tool-augmented agents built on abstractions such as Model Context Protocol (MCP) and web agents that 
- [2601.16443v3](https://arxiv.org/abs/2601.16443v3) — Endless Terminals: Scaling RL Environments for Terminal Agents — score 138
  - updated: 2026-02-14T09:14:28Z
  - category: cs.LG
  - matched queries: terminal agents
  - Environments are the bottleneck for self-improving agents. Current terminal benchmarks were built for evaluation, not training; reinforcement learning requires a scalable pipeline, not just a dataset. We introduce Endless Terminals, a fully autonomous pipeline that procedurally g
- [2604.06392v1](https://arxiv.org/abs/2604.06392v1) — Qualixar OS: A Universal Operating System for AI Agent Orchestration — score 138
  - updated: 2026-04-07T19:22:20Z
  - category: cs.AI
  - matched queries: agent orchestration
  - We present Qualixar OS, the first application-layer operating system for universal AI agent orchestration. Unlike kernel-level approaches (AIOS) or single-framework tools (AutoGen, CrewAI), Qualixar OS provides a complete runtime for heterogeneous multi-agent systems spanning 10 

### Strong remote hits already in the vault

- [2604.19572v2](https://arxiv.org/abs/2604.19572v2) — A Self-Evolving Framework for Efficient Terminal Agents via Observational Context Compression — score 174
  - category: cs.CL
  - matched queries: terminal agents
- [2604.18071v1](https://arxiv.org/abs/2604.18071v1) — Architectural Design Decisions in AI Agent Harnesses — score 162
  - category: cs.AI
  - matched queries: agent harness, agent orchestration
- [2603.25723v1](https://arxiv.org/abs/2603.25723v1) — Natural-Language Agent Harnesses — score 162
  - category: cs.CL
  - matched queries: agent harness
- [2604.13346v1](https://arxiv.org/abs/2604.13346v1) — AgentSPEX: An Agent SPecification and EXecution Language — score 108
  - category: cs.CL
  - matched queries: agent harness
- [2604.07833v2](https://arxiv.org/abs/2604.07833v2) — Harnessing Embodied Agents: Runtime Governance for Policy-Constrained Execution — score 104
  - category: cs.RO
  - matched queries: agent runtime governance
- [2604.21003v2](https://arxiv.org/abs/2604.21003v2) — The Last Harness You'll Ever Build — score 68
  - category: cs.AI
  - matched queries: agent harness
- [2604.03610v1](https://arxiv.org/abs/2604.03610v1) — DebugHarness: Emulating Human Dynamic Debugging for Autonomous Program Repair — score 68
  - category: cs.SE
  - matched queries: agent harness
- [2604.03088v3](https://arxiv.org/abs/2604.03088v3) — SkVM: Revisiting Language VM for Skills across Heterogenous LLMs and Harnesses — score 60
  - category: cs.SE
  - matched queries: agent harness
- [2603.29199v1](https://arxiv.org/abs/2603.29199v1) — AEC-Bench: A Multimodal Benchmark for Agentic Systems in Architecture, Engineering, and Construction — score 60
  - category: cs.AI
  - matched queries: agent harness
- [2604.00362v1](https://arxiv.org/abs/2604.00362v1) — In harmony with gpt-oss — score 44
  - category: cs.AI
  - matched queries: agent harness
- [2603.26996v1](https://arxiv.org/abs/2603.26996v1) — FormalProofBench: Can Models Write Graduate Level Math Proofs That Are Formally Verified? — score 8
  - category: cs.AI
  - matched queries: agent harness

