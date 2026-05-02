# arXiv Abstracts (from Obsidian vault)

Generated from: `arxiv-abstracts.json`
Count: **109**

## 2311.02018v1 — Active Reasoning in an Open-World Environment

- URL: https://arxiv.org/abs/2311.02018v1
- Primary category: `cs.AI`
- Published: 2023-11-03T16:24:34Z

### Abstract

Recent advances in vision-language learning have achieved notable success on complete-information question-answering datasets through the integration of extensive world knowledge. Yet, most models operate passively, responding to questions based on pre-stored knowledge. In stark contrast, humans possess the ability to actively explore, accumulate, and reason using both newfound and existing information to tackle incomplete-information questions. In response to this gap, we introduce $Conan$, an interactive open-world environment devised for the assessment of active reasoning. $Conan$ facilitates active exploration and promotes multi-round abductive inference, reminiscent of rich, open-world settings like Minecraft. Diverging from previous works that lean primarily on single-round deduction via instruction following, $Conan$ compels agents to actively interact with their surroundings, amalgamating new evidence with prior knowledge to elucidate events from incomplete observations. Our analysis on $Conan$ underscores the shortcomings of contemporary state-of-the-art models in active exploration and understanding complex scenarios. Additionally, we explore Abduction from Deduction, where agents harness Bayesian rules to recast the challenge of abduction as a deductive process. Through $Conan$, we aim to galvanize advancements in active reasoning and set the stage for the next generation of artificial intelligence agents adept at dynamically engaging in environments.

## 2408.01667v2 — Automated Phishing Detection Using URLs and Webpages

- URL: https://arxiv.org/abs/2408.01667v2
- Primary category: `cs.CR`
- Published: 2024-08-03T05:08:27Z

### Abstract

Phishing detection is a critical cybersecurity task that involves the identification and neutralization of fraudulent attempts to obtain sensitive information, thereby safeguarding individuals and organizations from data breaches and financial loss. In this project, we address the constraints of traditional reference-based phishing detection by developing an LLM agent framework. This agent harnesses Large Language Models to actively fetch and utilize online information, thus providing a dynamic reference system for more accurate phishing detection. This innovation circumvents the need for a static knowledge base, offering a significant enhancement in adaptability and efficiency for automated security measures. The project report includes an initial study and problem analysis of existing solutions, which motivated us to develop a new framework. We demonstrate the framework with LLMs simulated as agents and detail the techniques required for construction, followed by a complete implementation with a proof-of-concept as well as experiments to evaluate our solution's performance against other similar solutions. The results show that our approach has achieved with accuracy of 0.945, significantly outperforms the existing solution(DynaPhish) by 0.445. Furthermore, we discuss the limitations of our approach and suggest improvements that could make it more effective. Overall, the proposed framework has the potential to enhance the effectiveness of current reference-based phishing detection approaches and could be adapted for real-world applications.

## 2410.12475 — Aegis:An Advanced LLM-Based Multi-Agent for Intelligent Functional Safety Engineering

- URL: https://arxiv.org/abs/2410.12475

### Abstract

Functional safety is a critical aspect of automotive engineering, encompassing all phases of a vehicle's lifecycle, including design, development, production, operation, and decommissioning. This domain involves highly knowledge-intensive tasks. This paper introduces Aegis: An Advanced LLM-Based Multi-Agent for Intelligent Functional Safety Engineering. Aegis is specifically designed to support complex functional safety tasks within the automotive sector. It is tailored to perform Hazard Analysis and Risk Assessment(HARA), document Functional Safety Requirements(FSR), and plan test cases for Automatic Emergency Braking(AEB) systems. The most advanced version, Aegis-Max, leverages Retrieval-Augmented Generation(RAG) and reflective mechanisms to enhance its capability in managing complex, knowledge-intensive tasks. Additionally, targeted prompt refinement by professional functional safety practitioners can significantly optimize Aegis's performance in the functional safety domain. This paper demonstrates the potential of Aegis to improve the efficiency and effectiveness of functional safety processes in automotive engineering.

## 2503.13577 — When Should We Orchestrate Multiple Agents?

- URL: https://arxiv.org/abs/2503.13577

### Abstract

Strategies for orchestrating the interactions between multiple agents, both human and artificial, can wildly overestimate performance and underestimate the cost of orchestration. We design a framework to orchestrate agents under realistic conditions, such as inference costs or availability constraints. We show theoretically that orchestration is only effective if there are performance or cost differentials between agents. We then empirically demonstrate how orchestration between multiple agents can be helpful for selecting agents in a simulated environment, picking a learning strategy in the infamous Rogers' Paradox from social science, and outsourcing tasks to other agents during a question-answer task in a user study.

## 2504.19413v1 — Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory

- URL: https://arxiv.org/abs/2504.19413v1
- Primary category: `cs.CL`
- Published: 2025-04-28T01:46:35Z

### Abstract

Large Language Models (LLMs) have demonstrated remarkable prowess in generating contextually coherent responses, yet their fixed context windows pose fundamental challenges for maintaining consistency over prolonged multi-session dialogues. We introduce Mem0, a scalable memory-centric architecture that addresses this issue by dynamically extracting, consolidating, and retrieving salient information from ongoing conversations. Building on this foundation, we further propose an enhanced variant that leverages graph-based memory representations to capture complex relational structures among conversational elements. Through comprehensive evaluations on LOCOMO benchmark, we systematically compare our approaches against six baseline categories: (i) established memory-augmented systems, (ii) retrieval-augmented generation (RAG) with varying chunk sizes and k-values, (iii) a full-context approach that processes the entire conversation history, (iv) an open-source memory solution, (v) a proprietary model system, and (vi) a dedicated memory management platform. Empirical results show that our methods consistently outperform all existing memory systems across four question categories: single-hop, temporal, multi-hop, and open-domain. Notably, Mem0 achieves 26% relative improvements in the LLM-as-a-Judge metric over OpenAI, while Mem0 with graph memory achieves around 2% higher overall score than the base configuration. Beyond accuracy gains, we also markedly reduce computational overhead compared to full-context method. In particular, Mem0 attains a 91% lower p95 latency and saves more than 90% token cost, offering a compelling balance between advanced reasoning capabilities and practical deployment constraints. Our findings highlight critical role of structured, persistent memory mechanisms for long-term conversational coherence, paving the way for more reliable and efficient LLM-driven AI agents.

## 2505.02279v2 — A survey of agent interoperability protocols: Model Context Protocol (MCP), Agent Communication Protocol (ACP), Agent-to-Agent Protocol (A2A), and Agent Network Protocol (ANP)

- URL: https://arxiv.org/abs/2505.02279v2
- Primary category: `cs.AI`
- Published: 2025-05-04T22:18:27Z

### Abstract

Large language model powered autonomous agents demand robust, standardized protocols to integrate tools, share contextual data, and coordinate tasks across heterogeneous systems. Ad-hoc integrations are difficult to scale, secure, and generalize across domains. This survey examines four emerging agent communication protocols: Model Context Protocol (MCP), Agent Communication Protocol (ACP), Agent-to-Agent Protocol (A2A), and Agent Network Protocol (ANP), each addressing interoperability in deployment contexts. MCP provides a JSON-RPC client-server interface for secure tool invocation and typed data exchange. ACP defines a general-purpose communication protocol over RESTful HTTP, supporting MIME-typed multipart messages and synchronous and asynchronous interactions. Its lightweight and runtime-independent design enables scalable agent invocation, while features like session management, message routing, and integration with role-based and decentralized identifiers (DIDs). A2A enables peer-to-peer task delegation using capability-based Agent Cards, supporting secure and scalable collaboration across enterprise agent workflows. ANP supports open network agent discovery and secure collaboration using W3C decentralized identifiers DIDs and JSON-LD graphs. The protocols are compared across multiple dimensions, including interaction modes, discovery mechanisms, communication patterns, and security models. Based on the comparative analysis, a phased adoption roadmap is proposed: beginning with MCP for tool access, followed by ACP for structured, multimodal messaging session-aware interaction and both online and offline agent discovery across scalable, HTTP-based deployments A2A for collaborative task execution, and extending to ANP for decentralized agent marketplaces. This work provides a comprehensive foundation for designing secure, interoperable, and scalable ecosystems of LLM-powered agents.

## 2506.08119v2 — SOP-Bench: Complex Industrial SOPs for Evaluating LLM Agents

- URL: https://arxiv.org/abs/2506.08119v2
- Primary category: `cs.AI`
- Published: 2025-06-09T18:20:12Z

### Abstract

LLM-based agents struggle to execute complex, multi-step Standard Operating Procedures (SOPs) that are fundamental to industrial automation. Existing benchmarks fail to capture the procedural complexity and tool orchestration demands of real-world workflows. We introduce SOP-Bench, a benchmark of 2,000+ tasks from human expert-authored SOPs across 12 business domains (healthcare, logistics, finance, content moderation, etc.). Using a human-AI collaborative framework, experts crafted authentic SOPs while AI generated artifacts (tools, APIs, datasets), all human-validated, yielding realistic tasks with executable interfaces and ground-truth outputs. SOP-Bench serves as a research enabler for systematically investigating agent architectures, model capabilities, and deployment considerations across diverse procedural tasks. We demonstrate its utility through illustrative experiments with a subset of frontier models across Function-Calling (FC) and ReAct agents, revealing critical insights. For example, (1) newer models do not guarantee better performance - Claude 4 family outperforms Claude 4.5 family on ReAct tasks (Claude 4 Opus: 72.4% vs. Claude 4.5 Sonnet: 63.3% task success rate), demonstrating that production upgrades require validation; (2) no single model-agent combination dominates: best performances range from 57% to 100% depending on domain. These examples illustrate how SOP-Bench enables isolating and studying specific dimensions of agent performance without costly production experiments. Our goal is not to rank model capabilities or build optimal agents, but to provide a rigorous evaluation framework that enables the researchers and practitioners to systematically investigate agent design choices, model selection, and deployment strategies. We release the benchmark at https://github.com/amazon-science/sop-bench.

## 2507.11633 — General Modular Harness for LLM Agents in Multi-Turn Gaming Environments

- URL: https://arxiv.org/abs/2507.11633

### Abstract

We introduce a modular harness design for LLM agents that composes of perception, memory, and reasoning components, enabling a single LLM or VLM backbone to tackle a wide spectrum of multi turn gaming environments without domain-specific engineering. Using classic and modern game suites as low-barrier, high-diversity testbeds, our framework provides a unified workflow for analyzing how each module affects performance across dynamic interactive settings. Extensive experiments demonstrate that the harness lifts gameplay performance consistently over un-harnessed baselines and reveals distinct contribution patterns, for example, memory dominates in long-horizon puzzles while perception is critical in vision noisy arcades. These findings highlight the effectiveness of our modular harness design in advancing general-purpose agent, given the familiarity and ubiquity of games in everyday human experience.

## 2507.18755v1 — Agentic Program Repair from Test Failures at Scale: A Neuro-symbolic approach with static analysis and test execution feedback

- URL: https://arxiv.org/abs/2507.18755v1
- Primary category: `cs.SE`
- Published: 2025-07-24T19:12:32Z

### Abstract

Aim: With the advent of LLMs, sophisticated agentic program repair has become viable at large organizations with large codebases. In this work, we develop an Engineering Agent that fixes the source code based on test failures at scale across diverse software offerings internally. Method: Using Llama as the base, we employ the ReAct harness to develop an agent. We start with a test failure that was triaged by a rule-based test failure bot. We then set up an agentic harness and allow the agent to reason and run a set of 15 actions from reading a file to generating a patch. We provide feedback to the agent through static analysis and test failures so it can refine its solution. We leverage an LLM-as-a-Judge to ensure that the patch conforms to the standards followed by a human review to land fixes. Benchmark Findings: We curated offline benchmarks for our patch generator, the Engineering Agent loop, and the LLM-as-a-Judge. In offline evaluations we found that a specialized 70B model is highly competitive with the much larger but vanilla Llama-405B. In an ablation study, we found that the ReAct harness (neural model) benefited from the symbolic information from static analysis tools and test execution traces. A model that strikes a balance between the solve rate and error rate vs the cost and latency has a benchmark solve rate of 42.3% using an average 11.8 feedback iterations. Production Findings: In a three month period, 80% of the generated fixes were reviewed, of which 31.5% were landed (25.5% of the total number of generated fixes). Feedback from Engineers: We used open coding to extract qualitative themes from engineers' feedback. We saw positive feedback in the form of quick approvals, gratitude, and surprise. We also found mixed feedback when the Engineering Agent's solution was partially correct and it served as a good starting point.

## 2507.23361v2 — SWE-Exp: Experience-Driven Software Issue Resolution

- URL: https://arxiv.org/abs/2507.23361v2
- Primary category: `cs.SE`
- Published: 2025-07-31T09:13:42Z

### Abstract

Recent advances in large language model (LLM) agents have shown remarkable progress in software issue resolution, leveraging advanced techniques such as multi-agent collaboration and Monte Carlo Tree Search (MCTS). However, current agents act as memoryless explorers - treating each problem separately without retaining or reusing knowledge from previous repair experiences. This leads to redundant exploration of failed trajectories and missed chances to adapt successful issue resolution methods to similar problems. To address this problem, we introduce SWE-Exp, an experience-enhanced approach that distills concise and actionable experience from prior agent trajectories, enabling continuous learning across issues. Our method introduces a multi-faceted experience bank that captures both successful and failed repair attempts. Specifically, it extracts reusable issue resolution knowledge at different levels - from high-level problem comprehension to specific code changes. Experiments show that SWE-Exp achieves a Pass@1 resolution rate of 73.0% on SWE-Bench Verified using the state-of-the-art LLM Claude 4 Sonnet, significantly outperforming prior results under other agent frameworks. Our approach establishes a new paradigm in which automated software engineering agents systematically accumulate and leverage repair expertise, fundamentally shifting from trial-and-error exploration to strategic, experience-driven issue resolution.

## 2508.00007v1 — Agent Network Protocol Technical White Paper

- URL: https://arxiv.org/abs/2508.00007v1
- Primary category: `cs.NI`
- Published: 2025-07-18T05:04:43Z

### Abstract

With the development of large models and autonomous decision-making AI, agents are rapidly becoming the new entities of the internet, following mobile apps. However, existing internet infrastructure is primarily designed for human interaction, creating data silos, unfriendly interfaces, and high collaboration costs among agents, making it difficult to support the needs for large-scale agent interconnection and collaboration. The internet is undergoing a profound transformation, showing four core trends: agents replacing traditional software, universal agent interconnection, native protocol-based connections, and autonomous agent organization and collaboration. To align with these trends, Agent Network Protocol (ANP) proposes a new generation of communication protocols for the Agentic Web. ANP adheres to AI-native design, maintains compatibility with existing internet protocols, adopts a modular composable architecture, follows minimalist yet extensible principles, and enables rapid deployment based on existing infrastructure. Through a three-layer protocol system--identity and encrypted communication layer, meta-protocol negotiation layer, and application protocol layer--ANP. systematically solves the problems of agent identity authentication, dynamic negotiation, and capability discovery interoperability.

## 2508.00828v1 — Finance Agent Benchmark: Benchmarking LLMs on Real-world Financial Research Tasks

- URL: https://arxiv.org/abs/2508.00828v1
- Primary category: `cs.CE`
- Published: 2025-05-20T18:22:10Z

### Abstract

Artificial Intelligence (AI) technology has emerged as a transformative force in financial analysis and the finance industry, though significant questions remain about the full capabilities of Large Language Model (LLM) agents in this domain. We present the Finance Agent Benchmark, featuring challenging and diverse real-world finance research problems that require LLMs to perform complex analysis using recent SEC filings. We construct the benchmark using a taxonomy of nine financial task categories, developed in consultation with experts from banks, hedge funds, and private equity firms. The dataset includes 537 expert-authored questions covering tasks from information retrieval to complex financial modeling, each validated through a rigorous review process to ensure accuracy and relevance. Moreover, we implement an agentic harness that equips LLMs with tools sufficient to produce accurate responses, including Google Search and EDGAR database access. Overall, the Finance Agent Benchmark provides a comprehensive testbed for measuring the progress of LLM-driven finance agents. Our evaluation reveals significant limitations in current AI capabilities - even the best-performing model (OpenAI o3) achieved only 46.8% accuracy at an average cost of $3.79 per query. This underscores the need for further advancements before reliable deployment in high-stakes finance settings.

## 2508.20465v1 — On the possibility of deep alignment

- URL: https://arxiv.org/abs/2508.20465v1
- Primary category: `q-bio.NC`
- Published: 2025-08-28T06:33:58Z

### Abstract

I consider motivation and value-alignment in AI systems from the perspective of (constrained) entropy maximization. Though the structures encoding knowledge in any physical system can be understood as energetic constraints, only living agents harness entropy in the endogenous generation of actions. I argue that this exploitation of "mortal" or thermodynamic computation, in which cognitive and physical dynamics are inseparable, is of the essence of desire, motivation, and value, while the lack of true endogenous motivation in simulated "agents" predicts pathologies like reward hacking.

## 2509.19349v1 — ShinkaEvolve: Towards Open-Ended And Sample-Efficient Program Evolution

- URL: https://arxiv.org/abs/2509.19349v1
- Primary category: `cs.CL`
- Published: 2025-09-17T17:49:02Z

### Abstract

We introduce ShinkaEvolve: a new open-source framework leveraging large language models (LLMs) to advance scientific discovery with state-of-the-art performance and unprecedented efficiency. Recent advances in scaling inference time compute of LLMs have enabled significant progress in generalized scientific discovery. These approaches rely on evolutionary agentic harnesses that leverage LLMs as mutation operators to generate candidate solutions. However, current code evolution methods suffer from critical limitations: they are sample inefficient, requiring thousands of samples to identify effective solutions, and remain closed-source, hindering broad adoption and extension. ShinkaEvolve addresses these limitations, introducing three key innovations: a parent sampling technique balancing exploration and exploitation, code novelty rejection-sampling for efficient search space exploration, and a bandit-based LLM ensemble selection strategy. We evaluate ShinkaEvolve across diverse tasks, demonstrating consistent improvements in sample efficiency and solution quality. ShinkaEvolve discovers a new state-of-the-art circle packing solution using only 150 samples, designs high-performing agentic harnesses for AIME mathematical reasoning tasks, identifies improvements to ALE-Bench competitive programming solutions, and discovers novel mixture-of-expert load balancing loss functions that illuminate the space of optimization strategies. Our results demonstrate that ShinkaEvolve achieves broad applicability with exceptional sample efficiency. By providing open-source accessibility and cost-efficiency, this work democratizes open-ended discovery across diverse computational problems.

## 2509.21766 — UltraHorizon: Benchmarking Agent Capabilities in Ultra Long-Horizon Scenarios

- URL: https://arxiv.org/abs/2509.21766

### Abstract

Autonomous agents have recently achieved remarkable progress across diverse domains, yet most evaluations focus on short-horizon, fully observable tasks. In contrast, many critical real-world tasks, such as large-scale software development, commercial investment, and scientific discovery, unfold in long-horizon and partially observable scenarios where success hinges on sustained reasoning, planning, memory management, and tool use. Existing benchmarks rarely capture these long-horizon challenges, leaving a gap in systematic evaluation. To bridge this gap, we introduce \textbf{UltraHorizon} a novel benchmark that measures the foundational capabilities essential for complex real-world challenges. We use exploration as a unifying task across three distinct environments to validate these core competencies. Agents are designed in long-horizon discovery tasks where they must iteratively uncover hidden rules through sustained reasoning, planning, memory and tools management, and interaction with environments. Under the heaviest scale setting, trajectories average \textbf{200k+} tokens and \textbf{400+} tool calls, whereas in standard configurations they still exceed \textbf{35k} tokens and involve more than \textbf{60} tool calls on average. Our extensive experiments reveal that LLM-agents consistently underperform in these settings, whereas human participants achieve higher scores, underscoring a persistent gap in agents' long-horizon abilities. We also observe that simple scaling fails in our task. To better illustrate the failure of agents, we conduct an in-depth analysis of collected trajectories. We identify eight types of errors and attribute them to two primary causes: in-context locking and functional fundamental capability gaps. \href{[this https URL](https://github.com/StarDewXXX/UltraHorizon)}{Our code will be available here.}

## 2509.23206v3 — PARL-MT: Learning to Call Functions in Multi-Turn Conversation with Progress Awareness

- URL: https://arxiv.org/abs/2509.23206v3
- Primary category: `cs.CL`
- Published: 2025-09-27T09:32:27Z

### Abstract

Large language models (LLMs) have achieved impressive success in single-turn function calling, yet real-world applications such as travel planning or multi-stage data analysis typically unfold across multi-turn conversations. In these settings, LLMs must not only issue accurate function calls at each step but also maintain progress awareness, the ability to summarize past interactions and plan future actions to ensure coherent, long-horizon task execution. Existing approaches, however, either reduce multi-turn training to isolated single-turn samples, which neglects task-level planning, or employ end-to-end reinforcement learning (RL) that struggles with redundancy and lacks explicit integration of progress awareness. To overcome these limitations, we introduce PARL-MT, a framework that explicitly incorporates progress awareness into LLM training for multi-turn function calling. PARL-MT combines (i) a Progress Awareness Generation (PAG) pipeline, which automatically constructs datasets coupling conversation summaries with future task planning, and (ii) a Progress Awareness-Guided Reinforcement Learning (PAG-RL) algorithm, which integrates progress awareness into RL training to reduce contextual redundancy and improve alignment between local actions and global task completion. Empirical results on two public benchmarks demonstrate that PARL-MT significantly outperforms existing methods, highlighting the effectiveness of progress awareness in enabling robust and efficient multi-turn function calling.

## 2511.07568v1 — Procedural Knowledge Improves Agentic LLM Workflows

- URL: https://arxiv.org/abs/2511.07568v1
- Primary category: `cs.AI`
- Published: 2025-11-10T19:27:57Z

### Abstract

Large language models (LLMs) often struggle when performing agentic tasks without substantial tool support, prom-pt engineering, or fine tuning. Despite research showing that domain-dependent, procedural knowledge can dramatically increase planning efficiency, little work evaluates its potential for improving LLM performance on agentic tasks that may require implicit planning. We formalize, implement, and evaluate an agentic LLM workflow that leverages procedural knowledge in the form of a hierarchical task network (HTN). Empirical results of our implementation show that hand-coded HTNs can dramatically improve LLM performance on agentic tasks, and using HTNs can boost a 20b or 70b parameter LLM to outperform a much larger 120b parameter LLM baseline. Furthermore, LLM-created HTNs improve overall performance, though less so. The results suggest that leveraging expertise--from humans, documents, or LLMs--to curate procedural knowledge will become another important tool for improving LLM workflows.

## 2512.03420 — HarnessAgent: Scaling Automatic Fuzzing Harness Construction with Tool-Augmented LLM Pipelines

- URL: https://arxiv.org/abs/2512.03420
- Published: Fri, 12 Dec 2025 01:20:39 GMT

### Abstract

Large language model (LLM)-based techniques have achieved notable progress in generating harnesses for program fuzzing. However, applying them to arbitrary functions (especially internal functions) \textit{at scale} remains challenging due to the requirement of sophisticated contextual information, such as specification, dependencies, and usage examples. State-of-the-art methods heavily rely on static or incomplete context provisioning, causing failure of generating functional harnesses. Furthermore, LLMs tend to exploit harness validation metrics, producing plausible yet logically useless code. % Therefore, harness generation across large and diverse projects continues to face challenges in reliable compilation, robust code retrieval, and comprehensive validation. To address these challenges, we present HarnessAgent, a tool-augmented agentic framework that achieves fully automated, scalable harness construction over hundreds of OSS-Fuzz targets. HarnessAgent introduces three key innovations: 1) a rule-based strategy to identify and minimize various compilation errors; 2) a hybrid tool pool for precise and robust symbol source code retrieval; and 3) an enhanced harness validation pipeline that detects fake definitions. We evaluate HarnessAgent on 243 target functions from OSS-Fuzz projects (65 C projects and 178 C++ projects). It improves the three-shot success rate by approximately 20\% compared to state-of-the-art techniques, reaching 87\% for C and 81\% for C++. Our one-hour fuzzing results show that more than 75\% of the harnesses generated by HarnessAgent increase the target function coverage, surpassing the baselines by over 10\%. In addition, the hybrid tool-pool system of HarnessAgent achieves a response rate of over 90\% for source code retrieval, outperforming Fuzz Introspector by more than 30\%.

## 2512.03627v1 — MemVerse: Multimodal Memory for Lifelong Learning Agents

- URL: https://arxiv.org/abs/2512.03627v1
- Primary category: `cs.AI`
- Published: 2025-12-03T10:06:14Z

### Abstract

Despite rapid progress in large-scale language and vision models, AI agents still suffer from a fundamental limitation: they cannot remember. Without reliable memory, agents catastrophically forget past experiences, struggle with long-horizon reasoning, and fail to operate coherently in multimodal or interactive environments. We introduce MemVerse, a model-agnostic, plug-and-play memory framework that bridges fast parametric recall with hierarchical retrieval-based memory, enabling scalable and adaptive multimodal intelligence. MemVerse maintains short-term memory for recent context while transforming raw multimodal experiences into structured long-term memories organized as hierarchical knowledge graphs. This design supports continual consolidation, adaptive forgetting, and bounded memory growth. To handle real-time demands, MemVerse introduces a periodic distillation mechanism that compresses essential knowledge from long-term memory into the parametric model, allowing fast, differentiable recall while preserving interpretability. Extensive experiments demonstrate that MemVerse significantly improves multimodal reasoning and continual learning efficiency, empowering agents to remember, adapt, and reason coherently across extended interactions.

## 2512.04535v2 — GTM: Simulating the World of Tools for AI Agents

- URL: https://arxiv.org/abs/2512.04535v2
- Primary category: `cs.AI`
- Published: 2025-12-04T07:33:04Z

### Abstract

The integration of external tools is pivotal for empowering Large Language Model (LLM) agents with real-world capabilities. However, training these agents through direct, continuous interaction with diverse tools is often prohibitively expensive, slow, and introduces additional development and maintenance overhead. To address this challenge, we introduce the Generalist Tool Model (GTM), a 1.5-billion-parameter model that learns to act as a universal tool simulator. With only prompt-level configuration, GTM accesses tool functionalities along with input arguments and generates outputs that faithfully mimic real tool execution, providing a fast and cost-effective solution that eliminates development overhead. To build GTM, we propose the Context-Aware Response Generation (CARG) pipeline, which synthesizes comprehensive training data covering over 20,000 tools across 300 domains including physics, medicine, robotics, and finance. Through this pipeline, GTM learns to produce not only syntactically correct outputs but also logically coherent and contextually appropriate responses. Experiments demonstrate that GTM produces high-quality outputs with strong consistency and reliability. Besides when used in real reinforcement learning scenarios for agent training, GTM exhibits significantly faster simulation speed compared to real tools while maintaining comparable output quality, along with remarkable generalization and domain adaptability. Our results establish GTM as a foundational component for developing future AI agents, enabling efficient and scalable training of tool-augmented systems.

## 2512.16301v3 — Adaptation of Agentic AI: A Survey of Post-Training, Memory, and Skills

- URL: https://arxiv.org/abs/2512.16301v3
- Primary category: `cs.AI`
- Published: 2025-12-18T08:38:51Z

### Abstract

Large language model (LLM) agents are moving beyond prompting alone. ChatGPT marked the rise of general-purpose LLM assistants, DeepSeek showed that on-policy reinforcement learning with verifiable rewards can improve reasoning and tool use, and OpenClaw highlights a newer direction in which agents accumulate persistent memory and reusable skills. Yet the research landscape remains fragmented across post-training, retrieval, memory, and skill systems. This survey studies these developments under a single notion of \emph{adaptation}: improving an agent, its tools, or their interaction after pretraining. We organize the field with a four-paradigm framework spanning agent adaptation and tool adaptation. On the agent side, A1 (tool-execution-signaled) and A2 (agent-output-signaled) improve the agent itself through supervised fine-tuning, preference optimization, and reinforcement learning with verifiable rewards. On the tool side, T1 (agent-agnostic) provides reusable pre-trained modules any agent can call, while T2 (agent-supervised) uses the agent's outputs to train memory systems, skill libraries, or lightweight subagents. Using this framework, we review post-training methods, adaptive memory architectures, and agent skills; compare their trade-offs in cost, flexibility, and generalization; and summarize evaluation practices across deep research, software development, computer use, and drug discovery. We conclude by outlining open problems in agent-tool co-adaptation, continual learning, safety, and efficient deployment.

## 2512.24601v1 — Recursive Language Models

- URL: https://arxiv.org/abs/2512.24601v1
- Primary category: `cs.AI`
- Published: 2025-12-31T03:43:41Z

### Abstract

We study allowing large language models (LLMs) to process arbitrarily long prompts through the lens of inference-time scaling. We propose Recursive Language Models (RLMs), a general inference strategy that treats long prompts as part of an external environment and allows the LLM to programmatically examine, decompose, and recursively call itself over snippets of the prompt. We find that RLMs successfully handle inputs up to two orders of magnitude beyond model context windows and, even for shorter prompts, dramatically outperform the quality of base LLMs and common long-context scaffolds across four diverse long-context tasks, while having comparable (or cheaper) cost per query.

## 2601.03192v2 — MemRL: Self-Evolving Agents via Runtime Reinforcement Learning on Episodic Memory

- URL: https://arxiv.org/abs/2601.03192v2
- Primary category: `cs.CL`
- Published: 2026-01-06T17:14:50Z

### Abstract

The hallmark of human intelligence is the self-evolving ability to master new skills by learning from past experiences. However, current AI agents struggle to emulate this self-evolution: fine-tuning is computationally expensive and prone to catastrophic forgetting, while existing memory-based methods rely on passive semantic matching that often retrieves noise. To address these challenges, we propose MemRL, a non-parametric approach that evolves via reinforcement learning on episodic memory. By decoupling stable reasoning from plastic memory, MemRL employs a Two-Phase Retrieval mechanism to filter noise and identify high-utility strategies through environmental feedback. Extensive experiments on HLE, BigCodeBench, ALFWorld, and Lifelong Agent Bench demonstrate that MemRL significantly outperforms state-of-the-art baselines, confirming that MemRL effectively reconciles the stability-plasticity dilemma, enabling continuous runtime improvement without weight updates. Code is available at https://github.com/MemTensor/MemRL.

## 2601.03204v1 — InfiAgent: An Infinite-Horizon Framework for General-Purpose Autonomous Agents

- URL: https://arxiv.org/abs/2601.03204v1
- Primary category: `cs.AI`
- Published: 2026-01-06T17:35:57Z

### Abstract

LLM agents can reason and use tools, but they often break down on long-horizon tasks due to unbounded context growth and accumulated errors. Common remedies such as context compression or retrieval-augmented prompting introduce trade-offs between information fidelity and reasoning stability. We present InfiAgent, a general-purpose framework that keeps the agent's reasoning context strictly bounded regardless of task duration by externalizing persistent state into a file-centric state abstraction. At each step, the agent reconstructs context from a workspace state snapshot plus a fixed window of recent actions. Experiments on DeepResearch and an 80-paper literature review task show that, without task-specific fine-tuning, InfiAgent with a 20B open-source model is competitive with larger proprietary systems and maintains substantially higher long-horizon coverage than context-centric baselines. These results support explicit state externalization as a practical foundation for stable long-horizon agents. Github Repo:https://github.com/ChenglinPoly/infiAgent

## 2601.07372v1 — Conditional Memory via Scalable Lookup: A New Axis of Sparsity for Large Language Models

- URL: https://arxiv.org/abs/2601.07372v1
- Primary category: `cs.CL`
- Published: 2026-01-12T09:54:49Z

### Abstract

While Mixture-of-Experts (MoE) scales capacity via conditional computation, Transformers lack a native primitive for knowledge lookup, forcing them to inefficiently simulate retrieval through computation. To address this, we introduce conditional memory as a complementary sparsity axis, instantiated via Engram, a module that modernizes classic $N$-gram embedding for O(1) lookup. By formulating the Sparsity Allocation problem, we uncover a U-shaped scaling law that optimizes the trade-off between neural computation (MoE) and static memory (Engram). Guided by this law, we scale Engram to 27B parameters, achieving superior performance over a strictly iso-parameter and iso-FLOPs MoE baseline. Most notably, while the memory module is expected to aid knowledge retrieval (e.g., MMLU +3.4; CMMLU +4.0), we observe even larger gains in general reasoning (e.g., BBH +5.0; ARC-Challenge +3.7) and code/math domains~(HumanEval +3.0; MATH +2.4). Mechanistic analyses reveal that Engram relieves the backbone's early layers from static reconstruction, effectively deepening the network for complex reasoning. Furthermore, by delegating local dependencies to lookups, it frees up attention capacity for global context, substantially boosting long-context retrieval (e.g., Multi-Query NIAH: 84.2 to 97.0). Finally, Engram establishes infrastructure-aware efficiency: its deterministic addressing enables runtime prefetching from host memory, incurring negligible overhead. We envision conditional memory as an indispensable modeling primitive for next-generation sparse models.

## 2601.08670v1 — Parallel Context-of-Experts Decoding for Retrieval Augmented Generation

- URL: https://arxiv.org/abs/2601.08670v1
- Primary category: `cs.AI`
- Published: 2026-01-13T15:46:59Z

### Abstract

Retrieval Augmented Generation faces a trade-off: concatenating documents in a long prompt enables multi-document reasoning but creates prefill bottlenecks, while encoding document KV caches separately offers speed but breaks cross-document interaction. We propose Parallel Context-of-Experts Decoding (Pced), a training-free framework that shifts evidence aggregation from the attention mechanism to the decoding. Pced treats retrieved documents as isolated "experts", synchronizing their predictions via a novel retrieval-aware contrastive decoding rule that weighs expert logits against the model prior. This approach recovers cross-document reasoning capabilities without constructing a shared attention across documents.

## 2601.08773v1 — Reliable Graph-RAG for Codebases: AST-Derived Graphs vs LLM-Extracted Knowledge Graphs

- URL: https://arxiv.org/abs/2601.08773v1
- Primary category: `cs.SE`
- Published: 2026-01-13T18:03:41Z

### Abstract

Retrieval-Augmented Generation for software engineering often relies on vector similarity search, which captures topical similarity but can fail on multi-hop architectural reasoning such as controller to service to repository chains, interface-driven wiring, and inheritance. This paper benchmarks three retrieval pipelines on Java codebases (Shopizer, with additional runs on ThingsBoard and OpenMRS Core): (A) vector-only No-Graph RAG, (B) an LLM-generated knowledge graph RAG (LLM-KB), and (C) a deterministic AST-derived knowledge graph RAG (DKB) built with Tree-sitter and bidirectional traversal. Using 15 architecture and code-tracing queries per repository, we measure indexing time, query latency, corpus coverage, cost, and answer correctness. DKB builds its graph in seconds, while LLM-KB requires much longer graph generation. LLM-KB also shows indexing incompleteness: on Shopizer, 377 files are skipped or missed, reducing embedded chunk coverage and graph size compared to DKB. End-to-end cost is modest for DKB relative to the vector-only baseline but much higher for LLM-KB, especially as repository scale increases. Query latency is similar for No-Graph and DKB, while LLM-KB is slower and more variable. On the Shopizer question suite, DKB achieves the highest correctness, LLM-KB is close behind, and the vector-only baseline performs worst on upstream architectural queries and has the highest hallucination risk. Overall, deterministic AST-derived graphs provide more reliable coverage and multi-hop grounding than LLM-extracted graphs at substantially lower indexing cost.

## 2601.10338v1 — Agent Skills in the Wild: An Empirical Study of Security Vulnerabilities at Scale

- URL: https://arxiv.org/abs/2601.10338v1
- Primary category: `cs.CR`
- Published: 2026-01-15T12:31:52Z

### Abstract

The rise of AI agent frameworks has introduced agent skills, modular packages containing instructions and executable code that dynamically extend agent capabilities. While this architecture enables powerful customization, skills execute with implicit trust and minimal vetting, creating a significant yet uncharacterized attack surface. We conduct the first large-scale empirical security analysis of this emerging ecosystem, collecting 42,447 skills from two major marketplaces and systematically analyzing 31,132 using SkillScan, a multi-stage detection framework integrating static analysis with LLM-based semantic classification. Our findings reveal pervasive security risks: 26.1% of skills contain at least one vulnerability, spanning 14 distinct patterns across four categories: prompt injection, data exfiltration, privilege escalation, and supply chain risks. Data exfiltration (13.3%) and privilege escalation (11.8%) are most prevalent, while 5.2% of skills exhibit high-severity patterns strongly suggesting malicious intent. We find that skills bundling executable scripts are 2.12x more likely to contain vulnerabilities than instruction-only skills (OR=2.12, p<0.001). Our contributions include: (1) a grounded vulnerability taxonomy derived from 8,126 vulnerable skills, (2) a validated detection methodology achieving 86.7% precision and 82.5% recall, and (3) an open dataset and detection toolkit to support future research. These results demonstrate an urgent need for capability-based permission systems and mandatory security vetting before this attack vector is further exploited.

## 2601.10971v2 — AJAR: Adaptive Jailbreak Architecture for Red-teaming

- URL: https://arxiv.org/abs/2601.10971v2
- Primary category: `cs.CR`
- Published: 2026-01-16T03:30:40Z

### Abstract

Large language model (LLM) safety evaluation is moving from content moderation to action security as modern systems gain persistent state, tool access, and autonomous control loops. Existing jailbreak frameworks still leave a gap between adaptive multi-turn attacks and agentic runtimes: attack algorithms are usually packaged as monolithic scripts, while agent harnesses rarely expose explicit abstractions for rollback, tool simulation, or strategy switching. We present AJAR, a red-teaming framework that exposes multi-turn jailbreak algorithms as callable MCP services and lets an Auditor Agent orchestrate them inside a tool-aware runtime built on Petri. AJAR integrates three representative attacks, namely Crescendo, ActorAttack, and X-Teaming, under a shared service interface for planning, prompt generation, optimization, evaluation, and context control. On 200 HarmBench validation behaviors, AJAR improves X-Teaming from 65.0% to 76.0% attack success rate (ASR), reaches 80% cumulative success one turn earlier than the native implementation, and reproduces Crescendo more effectively than PyRIT (91.0% vs. 87.5% ASR). Behavior-level analysis shows that these gains are concentrated in hard categories and frequently depend on rollback-enabled transcript repair. We further show that tool access reshapes rather than uniformly enlarges the attack surface: ActorAttack rises from 51.0% to 56.0% ASR with tools, whereas Crescendo drops from 91.0% to 78.0% and X-Teaming from 76.0% to 55.5%, with the sharpest declines appearing in categories that rely on long semantic buildup. These results position AJAR as a practical foundation for evaluating multi-turn jailbreaks under realistic agent constraints. Code and data are available at https://github.com/douyipu/ajar.

## 2601.11868 — Terminal-Bench: Benchmarking Agents on Hard, Realistic Tasks in Command Line Interfaces

- URL: https://arxiv.org/abs/2601.11868
- Published: Sun, 01 Mar 2026 03:34:48 GMT

### Abstract

AI agents may soon become capable of autonomously completing valuable, long-horizon tasks in diverse domains. Current benchmarks either do not measure real-world tasks, or are not sufficiently difficult to meaningfully measure frontier models. To this end, we present Terminal-Bench 2.0: a carefully curated hard benchmark composed of 89 tasks in computer terminal environments inspired by problems from real workflows. Each task features a unique environment, human-written solution, and comprehensive tests for verification. We show that frontier models and agents score less than 65\% on the benchmark and conduct an error analysis to identify areas for model and agent improvement. We publish the dataset and evaluation harness to assist developers and researchers in future work at [this https URL](https://www.tbench.ai/).

## 2601.20412v1 — Beyond Accuracy: A Cognitive Load Framework for Mapping the Capability Boundaries of Tool-use Agents

- URL: https://arxiv.org/abs/2601.20412v1
- Primary category: `cs.CL`
- Published: 2026-01-28T09:17:51Z

### Abstract

The ability of Large Language Models (LLMs) to use external tools unlocks powerful real-world interactions, making rigorous evaluation essential. However, current benchmarks primarily report final accuracy, revealing what models can do but obscuring the cognitive bottlenecks that define their true capability boundaries. To move from simple performance scoring to a diagnostic tool, we introduce a framework grounded in Cognitive Load Theory. Our framework deconstructs task complexity into two quantifiable components: Intrinsic Load, the inherent structural complexity of the solution path, formalized with a novel Tool Interaction Graph; and Extraneous Load, the difficulty arising from ambiguous task presentation. To enable controlled experiments, we construct ToolLoad-Bench, the first benchmark with parametrically adjustable cognitive load. Our evaluation reveals distinct performance cliffs as cognitive load increases, allowing us to precisely map each model's capability boundary. We validate that our framework's predictions are highly calibrated with empirical results, establishing a principled methodology for understanding an agent's limits and a practical foundation for building more efficient systems.

## 2601.21123v2 — CUA-Skill: Develop Skills for Computer Using Agent

- URL: https://arxiv.org/abs/2601.21123v2
- Primary category: `cs.AI`
- Published: 2026-01-28T23:38:25Z

### Abstract

Computer-Using Agents (CUAs) aim to autonomously operate computer systems to complete real-world tasks. However, existing agentic systems remain difficult to scale and lag behind human performance. A key limitation is the absence of reusable and structured skill abstractions that capture how humans interact with graphical user interfaces and how to leverage these skills. We introduce CUA-Skill, a computer-using agentic skill base that encodes human computer-use knowledge as skills coupled with parameterized execution and composition graphs. CUA-Skill is a large-scale library of carefully engineered skills spanning common Windows applications, serving as a practical infrastructure and tool substrate for scalable, reliable agent development. Built upon this skill base, we construct CUA-Skill Agent, an end-to-end computer-using agent that supports dynamic skill retrieval, argument instantiation, and memory-aware failure recovery. Our results demonstrate that CUA-Skill substantially improves execution success rates and robustness on challenging end-to-end agent benchmarks, establishing a strong foundation for future computer-using agent development. On WindowsAgentArena, CUA-Skill Agent achieves state-of-the-art 57.5% (best of three) successful rate while being significantly more efficient than prior and concurrent approaches. The project page is available at https://microsoft.github.io/cua_skill/.

## 2601.21545v1 — ShardMemo: Masked MoE Routing for Sharded Agentic LLM Memory

- URL: https://arxiv.org/abs/2601.21545v1
- Primary category: `cs.AI`
- Published: 2026-01-29T11:01:34Z

### Abstract

Agentic large language model (LLM) systems rely on external memory for long-horizon state and concurrent multi-agent execution, but centralized indexes and heuristic partitions become bottlenecks as memory volume and parallel access grow. We present ShardMemo, a budgeted tiered memory service with Tier A per-agent working state, Tier B sharded evidence with shard-local approximate nearest neighbor (ANN) indexes, and Tier C, a versioned skill library. Tier B enforces scope-before-routing: structured eligibility constraints mask ineligible shards before routing or ANN search. We cast shard probing as masked mixture-of-experts (MoE) routing over eligible shards, probing up to $B_{\mathrm{probe}}$ shards via Top-$B_{\mathrm{probe}}$ or adaptive Top-$P$, and use cost-aware gating over profile/observation/session shard families; the router is trained from evidence-to-shard supervision. On LoCoMo, ShardMemo improves over the strongest baseline (GAM) by +5.11 to +6.82 F1 across question categories. Under a fixed-budget routing setting ($B_{\mathrm{probe}}=3$), ShardMemo improves over cosine-to-prototype shard routing by +6.87 F1 while reducing retrieval work (VecScan 521->414, -20.5%) and p95 latency (95->76 ms). On long-context HotpotQA, ShardMemo achieves 63.41/61.88/57.95 F1 at 56K/224K/448K tokens. On ToolBench, Tier C reaches 0.97 Precision@3 and 1.94 StepRed (+10.2% and +7.2% over embedding-similarity retrieval).

## 2601.21684v1 — Do Not Waste Your Rollouts: Recycling Search Experience for Efficient Test-Time Scaling

- URL: https://arxiv.org/abs/2601.21684v1
- Primary category: `cs.CL`
- Published: 2026-01-29T13:18:36Z

### Abstract

Test-Time Scaling enhances the reasoning capabilities of Large Language Models by allocating additional inference compute to broaden the exploration of the solution space. However, existing search strategies typically treat rollouts as disposable samples, where valuable intermediate insights are effectively discarded after each trial. This systemic memorylessness leads to massive computational redundancy, as models repeatedly re-derive discovered conclusions and revisit known dead ends across extensive attempts. To bridge this gap, we propose \textbf{Recycling Search Experience (RSE)}, a self-guided, training-free strategy that turns test-time search from a series of isolated trials into a cumulative process. By actively distilling raw trajectories into a shared experience bank, RSE enables positive recycling of intermediate conclusions to shortcut redundant derivations and negative recycling of failure patterns to prune encountered dead ends. Theoretically, we provide an analysis that formalizes the efficiency gains of RSE, validating its advantage over independent sampling in solving complex reasoning tasks. Empirically, extensive experiments on HMMT24, HMMT25, IMO-Bench, and HLE show that RSE consistently outperforms strong baselines with comparable computational cost, achieving state-of-the-art scaling efficiency.

## 2601.22773v3 — A Structured Approach to Safety Case Construction for AI Systems

- URL: https://arxiv.org/abs/2601.22773v3
- Primary category: `cs.SE`
- Published: 2026-01-30T09:53:22Z

### Abstract

Safety cases, structured arguments that a system is acceptably safe, are becoming central to the governance of AI systems. Yet, traditional safety-case practices from aviation or nuclear engineering rely on well-specified system boundaries, stable architectures, and known failure modes. Modern AI systems, such as generative and agentic AI, are the opposite. Their capabilities emerge unpredictably from low-level training objectives, their behaviour varies with prompts, and their risk profiles shift through fine-tuning, scaffolding, or deployment context. This study examines how safety cases are currently constructed for AI systems and why classical approaches fail to capture these dynamics. This study introduces comprehensive taxonomies for AI-specific claim types (assertion-based, constraint-based, capability-based), argument types (demonstrative, comparative, causal/explanatory, risk-based, and normative), and evidence families (empirical, mechanistic, comparative, expert-driven, formal methods, operational/field data, and model-based). It then proposes a reusable safety-case template, each of which follows a predefined structure of claims, arguments, and evidence tailored for AI systems. Each template is illustrated by end-to-end patterns that address distinctive challenges, such as evaluation without ground truth, dynamic model updates, and threshold-based risk decisions. The result is a systematic, composable, and reusable approach to constructing and maintaining safety cases that are credible, auditable, and adaptive to the evolving behaviour of generative and frontier AI systems.

## 2602.02007v3 — Beyond RAG for Agent Memory: Retrieval by Decoupling and Aggregation

- URL: https://arxiv.org/abs/2602.02007v3
- Primary category: `cs.CL`
- Published: 2026-02-02T12:04:58Z

### Abstract

Agent memory systems often adopt the standard Retrieval-Augmented Generation (RAG) pipeline, yet its underlying assumptions differ in this setting. RAG targets large, heterogeneous corpora where retrieved passages are diverse, whereas agent memory is a bounded, coherent dialogue stream with highly correlated spans that are often duplicates. Under this shift, fixed top-$k$ similarity retrieval tends to return redundant context, and post-hoc pruning can delete temporally linked prerequisites needed for correct reasoning. We argue retrieval should move beyond similarity matching and instead operate over latent components, following decoupling to aggregation: disentangle memories into semantic components, organise them into a hierarchy, and use this structure to drive retrieval. We propose xMemory, which builds a hierarchy of intact units and maintains a searchable yet faithful high-level node organisation via a sparsity--semantics objective that guides memory split and merge. At inference, xMemory retrieves top-down, selecting a compact, diverse set of themes and semantics for multi-fact queries, and expanding to episodes and raw messages only when it reduces the reader's uncertainty. Experiments on LoCoMo and PerLTQA across the three latest LLMs show consistent gains in answer quality and token efficiency.

## 2602.02474v1 — MemSkill: Learning and Evolving Memory Skills for Self-Evolving Agents

- URL: https://arxiv.org/abs/2602.02474v1
- Primary category: `cs.CL`
- Published: 2026-02-02T18:53:28Z

### Abstract

Most Large Language Model (LLM) agent memory systems rely on a small set of static, hand-designed operations for extracting memory. These fixed procedures hard-code human priors about what to store and how to revise memory, making them rigid under diverse interaction patterns and inefficient on long histories. To this end, we present \textbf{MemSkill}, which reframes these operations as learnable and evolvable memory skills, structured and reusable routines for extracting, consolidating, and pruning information from interaction traces. Inspired by the design philosophy of agent skills, MemSkill employs a \emph{controller} that learns to select a small set of relevant skills, paired with an LLM-based \emph{executor} that produces skill-guided memories. Beyond learning skill selection, MemSkill introduces a \emph{designer} that periodically reviews hard cases where selected skills yield incorrect or incomplete memories, and evolves the skill set by proposing refinements and new skills. Together, MemSkill forms a closed-loop procedure that improves both the skill-selection policy and the skill set itself. Experiments on LoCoMo, LongMemEval, HotpotQA, and ALFWorld demonstrate that MemSkill improves task performance over strong baselines and generalizes well across settings. Further analyses shed light on how skills evolve, offering insights toward more adaptive, self-evolving memory management for LLM agents.

## 2602.03786 — AOrchestra: Automating Sub-Agent Creation for Agentic Orchestration

- URL: https://arxiv.org/abs/2602.03786

### Abstract

Language agents have shown strong promise for task automation. Realizing this promise for increasingly complex, long-horizon tasks has driven the rise of a sub-agent-as-tools paradigm for multi-turn task solving. However, existing designs still lack a dynamic abstraction view of sub-agents, thereby hurting adaptability. We address this challenge with a unified, framework-agnostic agent abstraction that models any agent as a tuple Instruction, Context, Tools, Model. This tuple acts as a compositional recipe for capabilities, enabling the system to spawn specialized executors for each task on demand. Building on this abstraction, we introduce an agentic system AOrchestra, where the central orchestrator concretizes the tuple at each step: it curates task-relevant context, selects tools and models, and delegates execution via on-the-fly automatic agent creation. Such designs enable reducing human engineering efforts, and remain framework-agnostic with plug-and-play support for diverse agents as task executors. It also enables a controllable performance-cost trade-off, allowing the system to approach Pareto-efficient. Across three challenging benchmarks (GAIA, SWE-Bench, Terminal-Bench), AOrchestra achieves 16.28% relative improvement against the strongest baseline when paired with Gemini-3-Flash. The code is available at: [this https URL](https://github.com/FoundationAgents/AOrchestra)

## 2602.06025v1 — Learning Query-Aware Budget-Tier Routing for Runtime Agent Memory

- URL: https://arxiv.org/abs/2602.06025v1
- Primary category: `cs.CL`
- Published: 2026-02-05T18:57:09Z

### Abstract

Memory is increasingly central to Large Language Model (LLM) agents operating beyond a single context window, yet most existing systems rely on offline, query-agnostic memory construction that can be inefficient and may discard query-critical information. Although runtime memory utilization is a natural alternative, prior work often incurs substantial overhead and offers limited explicit control over the performance-cost trade-off. In this work, we present \textbf{BudgetMem}, a runtime agent memory framework for explicit, query-aware performance-cost control. BudgetMem structures memory processing as a set of memory modules, each offered in three budget tiers (i.e., \textsc{Low}/\textsc{Mid}/\textsc{High}). A lightweight router performs budget-tier routing across modules to balance task performance and memory construction cost, which is implemented as a compact neural policy trained with reinforcement learning. Using BudgetMem as a unified testbed, we study three complementary strategies for realizing budget tiers: implementation (method complexity), reasoning (inference behavior), and capacity (module model size). Across LoCoMo, LongMemEval, and HotpotQA, BudgetMem surpasses strong baselines when performance is prioritized (i.e., high-budget setting), and delivers better accuracy-cost frontiers under tighter budgets. Moreover, our analysis disentangles the strengths and weaknesses of different tiering strategies, clarifying when each axis delivers the most favorable trade-offs under varying budget regimes.

## 2602.08004v1 — Agent Skills: A Data-Driven Analysis of Claude Skills for Extending Large Language Model Functionality

- URL: https://arxiv.org/abs/2602.08004v1
- Primary category: `cs.SE`
- Published: 2026-02-08T15:14:12Z

### Abstract

Agent skills extend large language model (LLM) agents with reusable, program-like modules that define triggering conditions, procedural logic, and tool interactions. As these skills proliferate in public marketplaces, it is unclear what types are available, how users adopt them, and what risks they pose. To answer these questions, we conduct a large-scale, data-driven analysis of 40,285 publicly listed skills from a major marketplace. Our results show that skill publication tends to occur in short bursts that track shifts in community attention. We also find that skill content is highly concentrated in software engineering workflows, while information retrieval and content creation account for a substantial share of adoption. Beyond content trends, we uncover a pronounced supply-demand imbalance across categories, and we show that most skills remain within typical prompt budgets despite a heavy-tailed length distribution. Finally, we observe strong ecosystem homogeneity, with widespread intent-level redundancy, and we identify non-trivial safety risks, including skills that enable state-changing or system-level actions. Overall, our findings provide a quantitative snapshot of agent skills as an emerging infrastructure layer for agents and inform future work on skill reuse, standardization, and safety-aware design.

## 2602.08603v1 — OSCAR: Optimization-Steered Agentic Planning for Composed Image Retrieval

- URL: https://arxiv.org/abs/2602.08603v1
- Primary category: `cs.AI`
- Published: 2026-02-09T12:44:56Z

### Abstract

Composed image retrieval (CIR) requires complex reasoning over heterogeneous visual and textual constraints. Existing approaches largely fall into two paradigms: unified embedding retrieval, which suffers from single-model myopia, and heuristic agentic retrieval, which is limited by suboptimal, trial-and-error orchestration. To this end, we propose OSCAR, an optimization-steered agentic planning framework for composed image retrieval. We are the first to reformulate agentic CIR from a heuristic search process into a principled trajectory optimization problem. Instead of relying on heuristic trial-and-error exploration, OSCAR employs a novel offline-online paradigm. In the offline phase, we model CIR via atomic retrieval selection and composition as a two-stage mixed-integer programming problem, mathematically deriving optimal trajectories that maximize ground-truth coverage for training samples via rigorous boolean set operations. These trajectories are then stored in a golden library to serve as in-context demonstrations for online steering of VLM planner at online inference time. Extensive experiments on three public benchmarks and a private industrial benchmark show that OSCAR consistently outperforms SOTA baselines. Notably, it achieves superior performance using only 10% of training data, demonstrating strong generalization of planning logic rather than dataset-specific memorization.

## 2602.10498v1 — When Skills Lie: Hidden-Comment Injection in LLM Agents

- URL: https://arxiv.org/abs/2602.10498v1
- Primary category: `cs.CR`
- Published: 2026-02-11T03:58:07Z

### Abstract

LLM agents often rely on Skills to describe available tools and recommended procedures. We study a hidden-comment prompt injection risk in this documentation layer: when a Markdown Skill is rendered to HTML, HTML comment blocks can become invisible to human reviewers, yet the raw text may still be supplied verbatim to the model. In experiments, we find that DeepSeek-V3.2 and GLM-4.5-Air can be influenced by malicious instructions embedded in a hidden comment appended to an otherwise legitimate Skill, yielding outputs that contain sensitive tool intentions. A short defensive system prompt that treats Skills as untrusted and forbids sensitive actions prevents these malicious tool calls and instead surfaces the suspicious hidden instructions.

## 2602.10652v1 — UMEM: Unified Memory Extraction and Management Framework for Generalizable Memory

- URL: https://arxiv.org/abs/2602.10652v1
- Primary category: `cs.CL`
- Published: 2026-02-11T08:58:41Z

### Abstract

Self-evolving memory serves as the trainable parameters for Large Language Models (LLMs)-based agents, where extraction (distilling insights from experience) and management (updating the memory bank) must be tightly coordinated. Existing methods predominately optimize memory management while treating memory extraction as a static process, resulting in poor generalization, where agents accumulate instance-specific noise rather than robust memories. To address this, we propose Unified Memory Extraction and Management (UMEM), a self-evolving agent framework that jointly optimizes a Large Language Model to simultaneous extract and manage memories. To mitigate overfitting to specific instances, we introduce Semantic Neighborhood Modeling and optimize the model with a neighborhood-level marginal utility reward via GRPO. This approach ensures memory generalizability by evaluating memory utility across clusters of semantically related queries. Extensive experiments across five benchmarks demonstrate that UMEM significantly outperforms highly competitive baselines, achieving up to a 10.67% improvement in multi-turn interactive tasks. Futhermore, UMEM maintains a monotonic growth curve during continuous evolution. Codes and models will be publicly released.

## 2602.11304v1 — CryptoAnalystBench: Failures in Multi-Tool Long-Form LLM Analysis

- URL: https://arxiv.org/abs/2602.11304v1
- Primary category: `cs.IR`
- Published: 2026-02-11T19:29:31Z

### Abstract

Modern analyst agents must reason over complex, high token inputs, including dozens of retrieved documents, tool outputs, and time sensitive data. While prior work has produced tool calling benchmarks and examined factuality in knowledge augmented systems, relatively little work studies their intersection: settings where LLMs must integrate large volumes of dynamic, structured and unstructured multi tool outputs. We investigate LLM failure modes in this regime using crypto as a representative high data density domain. We introduce (1) CryptoAnalystBench, an analyst aligned benchmark of 198 production crypto and DeFi queries spanning 11 categories; (2) an agentic harness equipped with relevant crypto and DeFi tools to generate responses across multiple frontier LLMs; and (3) an evaluation pipeline with citation verification and an LLM as a judge rubric spanning four user defined success dimensions: relevance, temporal relevance, depth, and data consistency. Using human annotation, we develop a taxonomy of seven higher order error types that are not reliably captured by factuality checks or LLM based quality scoring. We find that these failures persist even in state of the art systems and can compromise high stakes decisions. Based on this taxonomy, we refine the judge rubric to better capture these errors. While the judge does not align with human annotators on precise scoring across rubric iterations, it reliably identifies critical failure modes, enabling scalable feedback for developers and researchers studying analyst style agents. We release CryptoAnalystBench with annotated queries, the evaluation pipeline, judge rubrics, and the error taxonomy, and outline mitigation strategies and open challenges in evaluating long form, multi tool augmented systems.

## 2602.12430v3 — Agent Skills for Large Language Models: Architecture, Acquisition, Security, and the Path Forward

- URL: https://arxiv.org/abs/2602.12430v3
- Primary category: `cs.MA`
- Published: 2026-02-12T21:33:25Z

### Abstract

The transition from monolithic language models to modular, skill-equipped agents marks a defining shift in how large language models (LLMs) are deployed in practice. Rather than encoding all procedural knowledge within model weights, agent skills -- composable packages of instructions, code, and resources that agents load on demand -- enable dynamic capability extension without retraining. It is formalized in a paradigm of progressive disclosure, portable skill definitions, and integration with the Model Context Protocol (MCP). This survey provides a comprehensive treatment of the agent skills landscape, as it has rapidly evolved during the last few months. We organize the field along four axes: (i) architectural foundations, examining the SKILL$.$md specification, progressive context loading, and the complementary roles of skills and MCP; (ii) skill acquisition, covering reinforcement learning with skill libraries, autonomous skill discovery (SEAgent), and compositional skill synthesis; (iii) deployment at scale, including the computer-use agent (CUA) stack, GUI grounding advances, and benchmark progress on OSWorld and SWE-bench; and (iv) security, where recent empirical analyses reveal that 26.1% of community-contributed skills contain vulnerabilities, motivating our proposed Skill Trust and Lifecycle Governance Framework -- a four-tier, gate-based permission model that maps skill provenance to graduated deployment capabilities. We identify seven open challenges -- from cross-platform skill portability to capability-based permission models -- and propose a research agenda for realizing trustworthy, self-improving skill ecosystems. Unlike prior surveys that broadly cover LLM agents or tool use, this work focuses specifically on the emerging skill abstraction layer and its implications for the next generation of agentic systems. Project repo: https://github.com/scienceaix/agentskills

## 2602.12670v3 — SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks

- URL: https://arxiv.org/abs/2602.12670v3
- Primary category: `cs.AI`
- Published: 2026-02-13T07:06:06Z

### Abstract

Agent Skills are structured packages of procedural knowledge that augment LLM agents at inference time. Despite rapid adoption, there is no standard way to measure whether they actually help. We present SkillsBench, a benchmark of 86 tasks across 11 domains paired with curated Skills and deterministic verifiers. Each task is evaluated under three conditions: no Skills, curated Skills, and self-generated Skills. We test 7 agent-model configurations over 7,308 trajectories. Curated Skills raise average pass rate by 16.2 percentage points(pp), but effects vary widely by domain (+4.5pp for Software Engineering to +51.9pp for Healthcare) and 16 of 84 tasks show negative deltas. Self-generated Skills provide no benefit on average, showing that models cannot reliably author the procedural knowledge they benefit from consuming. Focused Skills with 2--3 modules outperform comprehensive documentation, and smaller models with Skills can match larger models without them.

## 2602.14878v2 — Model Context Protocol (MCP) Tool Descriptions Are Smelly! Towards Improving AI Agent Efficiency with Augmented MCP Tool Descriptions

- URL: https://arxiv.org/abs/2602.14878v2
- Primary category: `cs.SE`
- Published: 2026-02-16T16:10:11Z

### Abstract

The Model Context Protocol (MCP) introduces a standard specification that defines how Foundation Model (FM)-based agents should interact with external systems by invoking tools. However, to understand a tool's purpose and features, FMs rely on natural-language tool descriptions, making these descriptions a critical component in guiding FMs to select the optimal tool for a given (sub)task and to pass the right arguments to the tool. While defects or smells in these descriptions can misguide FM-based agents, their prevalence and consequences in the MCP ecosystem remain unclear. Hence, we examine 856 tools spread across 103 MCP servers empirically, assess their description quality, and their impact on agent performance. We identify six components of tool descriptions from the literature, develop a scoring rubric utilizing these components, and then formalize tool description smells based on this rubric. By operationalizing this rubric through an FM-based scanner, we find that 97.1% of the analyzed tool descriptions contain at least one smell, with 56% failing to state their purpose clearly. While augmenting these descriptions for all components improves task success rates by a median of 5.85 percentage points and improves partial goal completion by 15.12%, it also increases the number of execution steps by 67.46% and regresses performance in 16.67% of cases. These results indicate that achieving performance gains is not straightforward; while execution cost can act as a trade-off, execution context can also impact. Furthermore, component ablations show that compact variants of different component combinations often preserve behavioral reliability while reducing unnecessary token overhead, enabling more efficient use of the FM context window and lower execution costs.

## 2602.16069v2 — The Limits of Long-Context Reasoning in Automated Bug Fixing

- URL: https://arxiv.org/abs/2602.16069v2
- Primary category: `cs.SE`
- Published: 2026-02-17T22:51:40Z

### Abstract

Rapidly increasing context lengths have led to the assumption that large language models (LLMs) can directly reason over entire codebases. Concurrently, recent advances in LLMs have enabled strong performance on software engineering benchmarks, particularly when paired with agentic workflows. In this work, we systematically evaluate whether current LLMs can reliably perform long-context code debugging and patch generation. Using SWE-bench Verified as a controlled experimental setting, we first evaluate state-of-the-art models within an agentic harness (mini-SWE-agent), where performance improves substantially: GPT-5-nano achieves up to a 31\% resolve rate on 100 samples, and open-source models such as Deepseek-R1-0528 obtain competitive results. However, token-level analysis shows that successful agentic trajectories typically remain under 20k-30k tokens, and that longer accumulated contexts correlate with lower success rates, indicating that agentic success primarily arises from task decomposition into short-context steps rather than effective long-context reasoning. To directly test long-context capability, we construct a data pipeline where we artificially inflate the context length of the input by placing the relevant files into the context (ensuring perfect retrieval recall); we then study single-shot patch generation under genuinely long contexts (64k tokens). Despite this setup, performance degrades sharply: Qwen3-Coder-30B-A3B achieves only a 7\% resolve rate at 64k context, while GPT-5-nano solves none of the tasks. Qualitative analysis reveals systematic failure modes, including hallucinated diffs, incorrect file targets, and malformed patch headers. Overall, our findings highlight a significant gap between nominal context length and usable context capacity in current LLMs, and suggest that existing agentic coding benchmarks do not meaningfully evaluate long-context reasoning.

## 2602.19008v1 — Capable but Unreliable: Canonical Path Deviation as a Causal Mechanism of Agent Failure in Long-Horizon Tasks

- URL: https://arxiv.org/abs/2602.19008v1
- Primary category: `cs.CL`
- Published: 2026-02-22T02:37:57Z

### Abstract

Why do language agents fail on tasks they are capable of solving? We argue that many such failures are reliability failures caused by stochastic drift from a task's latent solution structure, not capability failures. Every well-defined tool-use task imposes a canonical solution path (i.e., a convergent set of tool invocations shared across successful runs) and agent success depends critically on whether a trajectory stays within this path's operating envelope. We establish this causally using a natural experiment that holds model capability and task difficulty fixed by construction. We analyze trajectories from the Toolathlon benchmark: 22 frontier models each attempt 108 real-world tool-use tasks across 3 independent runs, yielding 515 model$\times$task units where the same model succeeds on some runs and fails on others due to LLM sampling stochasticity alone. Within these units, successful runs adhere significantly more closely to the canonical solution path than failed runs ($+$0.060 Jaccard, $p<0.0001$, $n=488$ units, 95% CI [+0.043, +0.077]). This result survives six robustness checks including cross-model-family leave-one-out validation. Critically, the causal mechanism is gradual and self-reinforcing: the adherence gap is statistically indistinguishable from zero through the first 50% of the trajectory, ruling out early-branching selection bias, and each off-canonical tool call raises the probability that the next call is also off-canonical by 22.7 percentage points ($\hatβ=+0.227$, $p<0.0001$), more than doubling the baseline rate. These findings imply that agent reliability cannot be improved by capability scaling alone, but offer a highly actionable intervention: a simple monitor that restarts the bottom tercile of runs based on mid-trajectory canonical adherence lifts success rates by $+$8.8 percentage points among intervened runs.

## 2602.19672v1 — SkillOrchestra: Learning to Route Agents via Skill Transfer

- URL: https://arxiv.org/abs/2602.19672v1
- Primary category: `cs.AI`
- Published: 2026-02-23T10:17:25Z

### Abstract

Compound AI systems promise capabilities beyond those of individual models, yet their success depends critically on effective orchestration. Existing routing approaches face two limitations: (1) input-level routers make coarse query-level decisions that ignore evolving task requirements; (2) RL-trained orchestrators are expensive to adapt and often suffer from routing collapse, repeatedly invoking one strong but costly option in multi-turn scenarios. We introduce SkillOrchestra, a framework for skill-aware orchestration. Instead of directly learning a routing policy end-to-end, SkillOrchestra learns fine-grained skills from execution experience and models agent-specific competence and cost under those skills. At deployment, the orchestrator infers the skill demands of the current interaction and selects agents that best satisfy them under an explicit performance-cost trade-off. Extensive experiments across ten benchmarks demonstrate that SkillOrchestra outperforms SoTA RL-based orchestrators by up to 22.5% with 700x and 300x learning cost reduction compared to Router-R1 and ToolOrchestra, respectively. These results show that explicit skill modeling enables scalable, interpretable, and sample-efficient orchestration, offering a principled alternative to data-intensive RL-based approaches. The code is available at: https://github.com/jiayuww/SkillOrchestra.

## 2602.20867v1 — SoK: Agentic Skills -- Beyond Tool Use in LLM Agents

- URL: https://arxiv.org/abs/2602.20867v1
- Primary category: `cs.CR`
- Published: 2026-02-24T13:11:38Z

### Abstract

Agentic systems increasingly rely on reusable procedural capabilities, \textit{a.k.a., agentic skills}, to execute long-horizon workflows reliably. These capabilities are callable modules that package procedural knowledge with explicit applicability conditions, execution policies, termination criteria, and reusable interfaces. Unlike one-off plans or atomic tool calls, skills operate (and often do well) across tasks. This paper maps the skill layer across the full lifecycle (discovery, practice, distillation, storage, composition, evaluation, and update) and introduces two complementary taxonomies. The first is a system-level set of \textbf{seven design patterns} capturing how skills are packaged and executed in practice, from metadata-driven progressive disclosure and executable code skills to self-evolving libraries and marketplace distribution. The second is an orthogonal \textbf{representation $\times$ scope} taxonomy describing what skills \emph{are} (natural language, code, policy, hybrid) and what environments they operate over (web, OS, software engineering, robotics). We analyze the security and governance implications of skill-based agents, covering supply-chain risks, prompt injection via skill payloads, and trust-tiered execution, grounded by a case study of the ClawHavoc campaign in which nearly 1{,}200 malicious skills infiltrated a major agent marketplace, exfiltrating API keys, cryptocurrency wallets, and browser credentials at scale. We further survey deterministic evaluation approaches, anchored by recent benchmark evidence that curated skills can substantially improve agent success rates while self-generated skills may degrade them. We conclude with open challenges toward robust, verifiable, and certifiable skills for real-world autonomous agents.

## 2602.22480 — VeRO: An Evaluation Harness for Agents to Optimize Agents

- URL: https://arxiv.org/abs/2602.22480

### Abstract

An important emerging application of coding agents is agent optimization: the iterative improvement of a target agent through edit-execute-evaluate cycles. Despite its relevance, the community lacks a systematic understanding of coding agent performance on this task. Agent optimization differs fundamentally from conventional software engineering: the target agent interleaves deterministic code with stochastic LLM completions, requiring structured capture of both intermediate reasoning and downstream execution outcomes. To address these challenges, we introduce VERO (Versioning, Rewards, and Observations), which provides (1) a reproducible evaluation harness with versioned agent snapshots, budget-controlled evaluation, and structured execution traces, and (2) a benchmark suite of target agents and tasks with reference evaluation procedures. Using VERO, we conduct an empirical study comparing optimizer configurations across tasks and analyzing which modifications reliably improve target agent performance. We release VERO to support research on agent optimization as a core capability for coding agents.

## 2602.22680v2 — Toward Personalized LLM-Powered Agents: Foundations, Evaluation, and Future Directions

- URL: https://arxiv.org/abs/2602.22680v2
- Primary category: `cs.AI`
- Published: 2026-02-26T06:52:47Z

### Abstract

Large language models have enabled agentic systems that reason, plan, and interact with tools and environments to accomplish complex tasks. As these agents operate over extended interaction horizons, their effectiveness increasingly depends on adapting behavior to individual users and maintaining continuity across interactions, giving rise to personalized LLM-powered agents (PLAs). In such long-term, user-dependent settings, personalization permeates the entire decision pipeline rather than remaining confined to surface-level response generation. This survey provides a capability-oriented review of personalized LLM-powered agents. Existing work is organized around four interdependent capabilities: profile modeling, memory, planning, and action execution. Using this taxonomy, representative methods are synthesized and analyzed to illustrate how user signals are represented, propagated, and utilized across the agent pipeline, highlighting cross-component interactions and recurring design challenges. Evaluation metrics and benchmarking paradigms tailored to personalized agents are further examined, along with application scenarios ranging from conversational assistants to domain-specific expert systems. By clarifying the design space of personalization in agent systems, this survey provides a structured foundation for developing more user-aligned, adaptive, and deployable LLM-powered agents.

## 2603.01493v1 — PhotoBench: Beyond Visual Matching Towards Personalized Intent-Driven Photo Retrieval

- URL: https://arxiv.org/abs/2603.01493v1
- Primary category: `cs.IR`
- Published: 2026-03-02T06:02:40Z

### Abstract

Personal photo albums are not merely collections of static images but living, ecological archives defined by temporal continuity, social entanglement, and rich metadata, which makes the personalized photo retrieval non-trivial. However, existing retrieval benchmarks rely heavily on context-isolated web snapshots, failing to capture the multi-source reasoning required to resolve authentic, intent-driven user queries. To bridge this gap, we introduce PhotoBench, the first benchmark constructed from authentic, personal albums. It is designed to shift the paradigm from visual matching to personalized multi-source intent-driven reasoning. Based on a rigorous multi-source profiling framework, which integrates visual semantics, spatial-temporal metadata, social identity, and temporal events for each image, we synthesize complex intent-driven queries rooted in users' life trajectories. Extensive evaluation on PhotoBench exposes two critical limitations: the modality gap, where unified embedding models collapse on non-visual constraints, and the source fusion paradox, where agentic systems perform poor tool orchestration. These findings indicate that the next frontier in personal multimodal retrieval lies beyond unified embeddings, necessitating robust agentic reasoning systems capable of precise constraint satisfaction and multi-source fusion. Our PhotoBench is available.

## 2603.02176v1 — Organizing, Orchestrating, and Benchmarking Agent Skills at Ecosystem Scale

- URL: https://arxiv.org/abs/2603.02176v1
- Primary category: `cs.CL`
- Published: 2026-03-02T18:46:47Z

### Abstract

The rapid proliferation of Claude agent skills has raised the central question of how to effectively leverage, manage, and scale the agent skill ecosystem. In this paper, we propose AgentSkillOS, the first principled framework for skill selection, orchestration, and ecosystem-level management. AgentSkillOS comprises two stages: (i) Manage Skills, which organizes skills into a capability tree via node-level recursive categorization for efficient discovery; and (ii) Solve Tasks, which retrieves, orchestrates, and executes multiple skills through DAG-based pipelines. To evaluate the agent's ability to invoke skills, we construct a benchmark of 30 artifact-rich tasks across five categories: data computation, document creation, motion video, visual design, and web interaction. We assess the quality of task outputs using LLM-based pairwise evaluation, and the results are aggregated via a Bradley-Terry model to produce unified quality scores. Experiments across three skill ecosystem scales (200 to 200K skills) show that tree-based retrieval effectively approximates oracle skill selection, and that DAG-based orchestration substantially outperforms native flat invocation even when given the identical skill set. Our findings confirm that structured composition is the key to unlocking skill potential. Our GitHub repository is available at:https://github.com/ynulihao/AgentSkillOS.

## 2603.02239v1 — Engineering Reasoning and Instruction (ERI) Benchmark: A Large Taxonomy-driven Dataset for Foundation Models and Agents

- URL: https://arxiv.org/abs/2603.02239v1
- Primary category: `cs.AI`
- Published: 2026-02-16T12:38:08Z

### Abstract

The Engineering Reasoning and Instruction (ERI) benchmark is a taxonomy-driven instruction dataset designed to train and evaluate engineering-capable large language models (LLMs) and agents. This dataset spans nine engineering fields (namely: civil, mechanical, electrical, chemical, environmental, aerospace, materials, fire, and industrial engineering) and 55 subdomains, and is crossed with seven intent types (i.e., definition, explanation, calculation, comparison, design/synthesis, troubleshooting, and code-related) and three difficulty tiers (undergraduate, graduate, and professional), yielding 57,750 records with field/subdomain/type/difficulty metadata and solution formatting. We examined ERI via seven LLMs and report a statistically significant three-tier performance structure, with frontier models (GPT-5, Claude Sonnet 4, DeepSeek V3.1) achieving mean scores above 4.30 on a five-point scale, while mid-tier and smaller models exhibited progressively higher failure rates and steeper performance degradation on graduate-level questions. To address circularity concerns inherent in LLM benchmarks, we developed a convergent validation protocol that leverages cross-provider independence, multi-judge averaging, and frontier-model agreement analysis to empirically bound hallucination risk to 1.7%. ERI is released with taxonomy specifications, validation scripts, and an evaluation harness to enable reproducible comparisons and regression testing for instruction tuning, routing, retrieval-augmented evaluation, and agentic tool-use workflows in engineering settings.

## 2603.03212v1 — NeuroSkill(tm): Proactive Real-Time Agentic System Capable of Modeling Human State of Mind

- URL: https://arxiv.org/abs/2603.03212v1
- Primary category: `cs.AI`
- Published: 2026-03-03T18:06:42Z

### Abstract

Real-time proactive agentic system, capable of modeling Human State of Mind, using foundation EXG model and text embeddings model, running fully offline on the edge. Unlike all previously known systems, the NeuroSkill(tm) system leverages SKILL.md description of Human's State of Mind via API and CLI provided by the system, directly from the Brain-Computer Interface (BCI) devices, which records Human biophysical and brain signals. Our custom harness - NeuroLoop(tm) - utilizes all of the above to run agentic flow that manages to engage with the Human on multiple cognitive and affective levels of their State of Mind (e.g., empathy), by providing actionable tool calls and protocol execution with explicit or implicit requests from the Human. GPLv3 open-source software with ethically aligned AI100 licensing for the skill markdown.

## 2603.03329v1 — AutoHarness: improving LLM agents by automatically synthesizing a code harness

- URL: https://arxiv.org/abs/2603.03329v1
- Primary category: `cs.CL`
- Published: 2026-02-10T14:12:54Z

### Abstract

Despite significant strides in language models in the last few years, when used as agents, such models often try to perform actions that are not just suboptimal for a given state, but are strictly prohibited by the external environment. For example, in the recent Kaggle GameArena chess competition, 78% of Gemini-2.5-Flash losses were attributed to illegal moves. Often people manually write "harnesses" around LLMs to prevent such failures. In this paper, we demonstrate that Gemini-2.5-Flash can automatically synthesize such a code harness, using a small number of rounds of iterative code refinement given feedback from the (game) environment. The resulting harness prevents all illegal moves in 145 different TextArena games (both 1-player and 2-player), enabling the smaller Gemini-2.5-Flash model to outperform larger models, such as Gemini-2.5-Pro. Pushing our technique to the limit, we can get Gemini-2.5-Flash to generate the entire policy in code, thus eliminating the need to use the LLM at decision making time. The resulting code-policy receives a higher average reward than Gemini-2.5-Pro and GPT-5.2-High on 16 TextArena 1-player games. Our results show that using a smaller model to synthesize a custom code harness (or entire policy) can outperform a much larger model, while also being more cost effective.

## 2603.05344v3 — Building Effective AI Coding Agents for the Terminal: Scaffolding, Harness, Context Engineering, and Lessons Learned

- URL: https://arxiv.org/abs/2603.05344v3
- Primary category: `cs.AI`
- Published: 2026-03-05T16:21:08Z

### Abstract

The landscape of AI coding assistance is undergoing a fundamental shift from complex IDE plugins to versatile, terminal-native agents. Operating directly where developers manage source control, execute builds, and deploy environments, CLI-based agents offer unprecedented autonomy for long-horizon development tasks. In this paper, we present OPENDEV, an open-source, command-line coding agent written in Rust, engineered specifically for this new paradigm. Effective autonomous assistance requires strict safety controls and highly efficient context management to prevent context bloat and reasoning degradation. OPENDEV overcomes these challenges through a compound AI system architecture with workload-specialized model routing, a dual-agent architecture separating planning from execution, lazy tool discovery, and adaptive context compaction that progressively reduces older observations. Furthermore, it employs an automated memory system to accumulate project-specific knowledge across sessions and counteracts instruction fade-out through event-driven system reminders. By enforcing explicit reasoning phases and prioritizing context efficiency, OPENDEV provides a secure, extensible foundation for terminal-first AI assistance, offering a blueprint for robust autonomous software engineering.

## 2603.07379v1 — SoK: Agentic Retrieval-Augmented Generation (RAG): Taxonomy, Architectures, Evaluation, and Research Directions

- URL: https://arxiv.org/abs/2603.07379v1
- Primary category: `cs.AI`
- Published: 2026-03-07T23:38:57Z

### Abstract

Retrieval-Augmented Generation (RAG) systems are increasingly evolving into agentic architectures where large language models autonomously coordinate multi-step reasoning, dynamic memory management, and iterative retrieval strategies. Despite rapid industrial adoption, current research lacks a systematic understanding of Agentic RAG as a sequential decision-making system, leading to highly fragmented architectures, inconsistent evaluation methodologies, and unresolved reliability risks. This Systematization of Knowledge (SoK) paper provides the first unified framework for understanding these autonomous systems. We formalize agentic retrieval-generation loops as finite-horizon partially observable Markov decision processes, explicitly modeling their control policies and state transitions. Building upon this formalization, we develop a comprehensive taxonomy and modular architectural decomposition that categorizes systems by their planning mechanisms, retrieval orchestration, memory paradigms, and tool-invocation behaviors. We further analyze the critical limitations of traditional static evaluation practices and identify severe systemic risks inherent to autonomous loops, including compounding hallucination propagation, memory poisoning, retrieval misalignment, and cascading tool-execution vulnerabilities. Finally, we outline key doctoral-scale research directions spanning stable adaptive retrieval, cost-aware orchestration, formal trajectory evaluation, and oversight mechanisms, providing a definitive roadmap for building reliable, controllable, and scalable agentic retrieval systems.

## 2603.07670v1 — Memory for Autonomous LLM Agents:Mechanisms, Evaluation, and Emerging Frontiers

- URL: https://arxiv.org/abs/2603.07670v1
- Primary category: `cs.AI`
- Published: 2026-03-08T15:08:01Z

### Abstract

Large language model (LLM) agents increasingly operate in settings where a single context window is far too small to capture what has happened, what was learned, and what should not be repeated. Memory -- the ability to persist, organize, and selectively recall information across interactions -- is what turns a stateless text generator into a genuinely adaptive agent. This survey offers a structured account of how memory is designed, implemented, and evaluated in modern LLM-based agents, covering work from 2022 through early 2026. We formalize agent memory as a \emph{write--manage--read} loop tightly coupled with perception and action, then introduce a three-dimensional taxonomy spanning temporal scope, representational substrate, and control policy. Five mechanism families are examined in depth: context-resident compression, retrieval-augmented stores, reflective self-improvement, hierarchical virtual context, and policy-learned management. On the evaluation side, we trace the shift from static recall benchmarks to multi-session agentic tests that interleave memory with decision-making, analyzing four recent benchmarks that expose stubborn gaps in current systems. We also survey applications where memory is the differentiating factor -- personal assistants, coding agents, open-world games, scientific reasoning, and multi-agent teamwork -- and address the engineering realities of write-path filtering, contradiction handling, latency budgets, and privacy governance. The paper closes with open challenges: continual consolidation, causally grounded retrieval, trustworthy reflection, learned forgetting, and multimodal embodied memory.

## 2603.08616v1 — Coverage-Guided Multi-Agent Harness Generation for Java Library Fuzzing

- URL: https://arxiv.org/abs/2603.08616v1
- Primary category: `cs.SE`
- Published: 2026-03-09T16:59:30Z

### Abstract

Coverage-guided fuzzing has proven effective for software testing, but targeting library code requires specialized fuzz harnesses that translate fuzzer-generated inputs into valid API invocations. Manual harness creation is time-consuming and requires deep understanding of API semantics, initialization sequences, and exception handling contracts. We present a multi-agent architecture that automates fuzz harness generation for Java libraries through specialized LLM-powered agents. Five ReAct agents decompose the workflow into research, synthesis, compilation repair, coverage analysis, and refinement. Rather than preprocessing entire codebases, agents query documentation, source code, and callgraph information on demand through the Model Context Protocol, maintaining focused context while exploring complex dependencies. To enable effective refinement, we introduce method-targeted coverage that tracks coverage only during target method execution to isolate target behavior, and agent-guided termination that examines uncovered source code to distinguish productive refinement opportunities from diminishing returns. We evaluated our approach on seven target methods from six widely-deployed Java libraries totaling 115,000+ Maven dependents. Our generated harnesses achieve a median 26\% improvement over OSS-Fuzz baselines and outperform Jazzer AutoFuzz by 5\% in package-scope coverage. Generation costs average \$3.20 and 10 minutes per harness, making the approach practical for continuous fuzzing workflows. During a 12-hour fuzzing campaign, our generated harnesses discovered 3 bugs in projects that are already integrated into OSS-Fuzz, demonstrating the effectiveness of the generated harnesses.

## 2603.10664v1 — Terminal Is All You Need: Design Properties for Human-AI Agent Collaboration

- URL: https://arxiv.org/abs/2603.10664v1
- Primary category: `cs.HC`
- Published: 2026-03-11T11:24:31Z

### Abstract

While research on AI agents focuses on enabling them to operate graphical user interfaces, the most effective and widely adopted agent tools in practice are terminal-based. We argue that this convergence is not coincidental. It reflects three design properties central to effective human-AI-UI collaboration: representational compatibility between agent and interface, transparency of agent actions within the interaction medium, and low barriers to entry for human participants. We ground each property in established HCI theory, show how terminal-based tools satisfy them by default, and argue that any modality, including graphical and spatial interfaces, must be deliberately engineered to achieve them. Rather than a legacy artifact, the terminal serves as a design exemplar whose properties any agent-facing modality must replicate.

## 2603.12658v1 — Continual Learning in Large Language Models: Methods, Challenges, and Opportunities

- URL: https://arxiv.org/abs/2603.12658v1
- Primary category: `cs.CL`
- Published: 2026-03-13T05:01:25Z

### Abstract

Continual learning (CL) has emerged as a pivotal paradigm to enable large language models (LLMs) to dynamically adapt to evolving knowledge and sequential tasks while mitigating catastrophic forgetting-a critical limitation of the static pre-training paradigm inherent to modern LLMs. This survey presents a comprehensive overview of CL methodologies tailored for LLMs, structured around three core training stages: continual pre-training, continual fine-tuning, and continual alignment.Beyond the canonical taxonomy of rehearsal-, regularization-, and architecture-based methods, we further subdivide each category by its distinct forgetting mitigation mechanisms and conduct a rigorous comparative analysis of the adaptability and critical improvements of traditional CL methods for LLMs. In doing so, we explicitly highlight core distinctions between LLM CL and traditional machine learning, particularly with respect to scale, parameter efficiency, and emergent capabilities. Our analysis covers essential evaluation metrics, including forgetting rates and knowledge transfer efficiency, along with emerging benchmarks for assessing CL performance. This survey reveals that while current methods demonstrate promising results in specific domains, fundamental challenges persist in achieving seamless knowledge integration across diverse tasks and temporal scales. This systematic review contributes to the growing body of knowledge on LLM adaptation, providing researchers and practitioners with a structured framework for understanding current achievements and future opportunities in lifelong learning for language models.

## 2603.18829v9 — Agent Control Protocol: Admission Control for Agent Actions

- URL: https://arxiv.org/abs/2603.18829v9
- Primary category: `cs.CR`
- Published: 2026-03-19T12:28:28Z

### Abstract

Autonomous agents can produce harmful behavioral patterns from individually valid requests -- a threat class that per-request policy evaluation cannot address, because stateless engines evaluate each request in isolation and cannot enforce properties that depend on execution history. We present ACP, a temporal admission control protocol that enforces behavioral properties over execution traces by combining static risk scoring with stateful signals (anomaly accumulation, cooldown) through a LedgerQuerier abstraction separating decision logic from state management. ACP is not an anomaly detection system: it does not detect suspicious patterns and alert; it blocks execution based on deterministic, history-aware risk scoring, providing a hard enforcement boundary rather than an advisory signal. Under a 500-request workload where every request is individually valid (RS=35), a stateless engine approves all 500; ACP limits autonomous execution to 2/500 (0.4%), escalating after 3 actions and enforcing denial after 11. ACP-RISK-3.0 eliminates cross-context state-mixing by scoping signals to (agentID, capability, resource). BAR-Monitor detects deviation collapse three batches before it occurs; counterfactual evaluation confirms enforcement capacity is preserved (BAR_C=1.00). N agents accumulate risk independently; CW=2N confirms O(N) scaling (Exp. 13). Latency: 739-832 ns (p50); throughput: 1,720,000 req/s. TLA+: 11 invariants + 4 temporal properties, 0 violations; 4,294,930,695 states (two-agent). 73 signed conformance vectors. ACP is Paper 1 of a 4-paper Agent Governance Series: atomic decision boundaries (P0, 10.5281/zenodo.19642166), behavioral drift detection/IML (P2, 10.5281/zenodo.19643761), fair allocation (P3, 10.5281/zenodo.19643928), composition irreducibility (P4, 10.5281/zenodo.19643950). Specification: https://github.com/chelof100/acp-framework-en

## 2603.18897v1 — Act While Thinking: Accelerating LLM Agents via Pattern-Aware Speculative Tool Execution

- URL: https://arxiv.org/abs/2603.18897v1
- Primary category: `cs.DC`
- Published: 2026-03-19T13:36:50Z

### Abstract

LLM-powered agents are emerging as a dominant paradigm for autonomous task solving. Unlike standard inference workloads, agents operate in a strictly serial "LLM-tool" loop, where the LLM must wait for external tool execution at every step. This execution model introduces severe latency bottlenecks. To address this problem, we propose PASTE, a Pattern-Aware Speculative Tool Execution method designed to hide tool latency through speculation. PASTE is based on the insight that although agent requests are semantically diverse, they exhibit stable application level control flows (recurring tool-call sequences) and predictable data dependencies (parameter passing between tools). By exploiting these properties, PASTE improves agent serving performance through speculative tool execution. Experimental results against state of the art baselines show that PASTE reduces average task completion time by 48.5% and improves tool execution throughput by 1.8x.

## 2603.19347v3 — Exploring the Agentic Frontier of Verilog Code Generation

- URL: https://arxiv.org/abs/2603.19347v3
- Primary category: `cs.AR`
- Published: 2026-03-19T16:48:19Z

### Abstract

Large language models (LLMs) have made rapid advancements in code generation for popular languages such as Python and C++. Many of these recent gains can be attributed to the use of ``agents'' that wrap domain-relevant tools alongside LLMs. Hardware design languages such as Verilog have also seen improved code generation in recent years, but the impact of agentic frameworks on Verilog code generation tasks remains unclear. In this work, we present the first systematic evaluation of agentic LLMs for Verilog generation, using the recently introduced CVDP benchmark. We also introduce several open-source hardware design agent harnesses, providing a model-agnostic baseline for future work. Through controlled experiments across frontier models, we study how structured prompting and tool design affect performance, analyze agent failure modes and tool usage patterns, compare open-source and closed-source models, and provide qualitative examples of successful and failed agent runs. Our results show that naive agentic wrapping around frontier models can degrade performance (relative to standard forward passes with optimized prompts), but that structured harnesses meaningfully match and in some cases exceed non-agentic baselines. We find that the performance gap between open and closed source models is driven by both higher crash rates and weaker tool output interpretation. Our exploration illuminates the path towards designing special-purpose agents for verilog generation in the future.

## 2603.20075v1 — Agentic Harness for Real-World Compilers

- URL: https://arxiv.org/abs/2603.20075v1
- Primary category: `cs.SE`
- Published: 2026-03-20T15:56:43Z

### Abstract

Compilers are critical to modern computing, yet fixing compiler bugs is difficult. While recent large language model (LLM) advancements enable automated bug repair, compiler bugs pose unique challenges due to their complexity, deep cross-domain expertise requirements, and sparse, non-descriptive bug reports, necessitating compiler-specific tools. To bridge the gap, we introduce llvm-autofix, the first agentic harness designed to assist LLM agents in understanding and fixing compiler bugs. Our focus is on LLVM, one of the most widely used compiler infrastructures. Central to llvm-autofix are agent-friendly LLVM tools, a benchmark llvm-bench of reproducible LLVM bugs, and a tailored minimal agent llvm-autofix-mini for fixing LLVM bugs. Our evaluation demonstrates a performance decline of 60% in frontier models when tackling compiler bugs compared with common software bugs. Our minimal agent llvm-autofix-mini also outperforms the state-of-the-art by approximately 22%. This emphasizes the necessity for specialized harnesses like ours to close the loop between LLMs and compiler engineering. We believe this work establishes a foundation for advancing LLM capabilities in complex systems like compilers. GitHub: https://github.com/dtcxzyw/llvm-autofix

## 2603.20380v1 — ALARA for Agents: Least-Privilege Context Engineering Through Portable Composable Multi-Agent Teams

- URL: https://arxiv.org/abs/2603.20380v1
- Primary category: `cs.MA`
- Published: 2026-03-20T18:00:09Z

### Abstract

Industry practitioners and academic researchers regularly use multi-agent systems to accelerate their work, yet the frameworks through which these systems operate do not provide a simple, unified mechanism for scalably managing the critical aspects of the agent harness, impacting both the quality of individual human-agent interactions and the capacity for practitioners to coordinate toward common goals through shared agent infrastructure. Agent frameworks have enabled increasingly sophisticated multi-agent systems, but the behavioral specifications that define what these agents can do remain fragmented across prose instruction files, framework-internal configuration, and mechanisms like MCP servers that operate separately from individual agent definitions, making these specifications difficult to share, version, or collaboratively maintain across teams and projects. Applying the ALARA principle from radiation safety (exposures kept as low as reasonably achievable) to agent context, we introduce a declarative context-agent-tool (CAT) data layer expressed through interrelated files that scope each agent's tool access and context to the minimum its role requires, and \texttt{npcsh}, a command-line shell for executing it. Because the system parses and enforces these files structurally, modifying an agent's tool list produces a guaranteed behavioral change rather than a suggestion the model may or may not follow. We evaluate 22 locally-hosted models from 0.6B to 35B parameters across 115 practical tasks spanning file operations, web search, multi-step scripting, tool chaining, and multi-agent delegation, characterizing which model families succeed at which task categories and where they break down across $\sim$2500 total executions.

## 2603.20939v1 — User Preference Modeling for Conversational LLM Agents: Weak Rewards from Retrieval-Augmented Interaction

- URL: https://arxiv.org/abs/2603.20939v1
- Primary category: `cs.CL`
- Published: 2026-03-21T20:44:32Z

### Abstract

Large language models are increasingly used as personal assistants, yet most lack a persistent user model, forcing users to repeatedly restate preferences across sessions. We propose Vector-Adapted Retrieval Scoring (VARS), a pipeline-agnostic, frozen-backbone framework that represents each user with long-term and short-term vectors in a shared preference space and uses these vectors to bias retrieval scoring over structured preference memory. The vectors are updated online from weak scalar rewards from users' feedback, enabling personalization without per-user fine-tuning. We evaluate on \textsc{MultiSessionCollab}, an online multi-session collaboration benchmark with rich user preference profiles, across math and code tasks. Under frozen backbones, the main benefit of user-aware retrieval is improved interaction efficiency rather than large gains in raw task accuracy: our full VARS agent achieves the strongest overall performance, matches a strong Reflection baseline in task success, and reduces timeout rate and user effort. The learned long-term vectors also align with cross-user preference overlap, while short-term vectors capture session-specific adaptation, supporting the interpretability of the dual-vector design. Code, model, and data are available at https://github.com/YurenHao0426/VARS.

## 2603.21019v1 — SkillProbe: Security Auditing for Emerging Agent Skill Marketplaces via Multi-Agent Collaboration

- URL: https://arxiv.org/abs/2603.21019v1
- Primary category: `cs.CR`
- Published: 2026-03-22T02:31:27Z

### Abstract

With the rapid evolution of Large Language Model (LLM) agent ecosystems, centralized skill marketplaces have emerged as pivotal infrastructure for augmenting agent capabilities. However, these marketplaces face unprecedented security challenges, primarily stemming from semantic-behavioral inconsistency and inter-skill combinatorial risks, where individually benign skills induce malicious behaviors during collaborative invocation. To address these vulnerabilities, we propose SkillProbe, a multi-stage security auditing framework driven by multi-agent collaboration. SkillProbe introduces a "Skills-for-Skills" design paradigm, encapsulating auditing processes into standardized skill modules to drive specialized agents through a rigorous pipeline, including admission filtering, semantic-behavioral alignment detection, and combinatorial risk simulation. We conducted a large-scale evaluation using 8 mainstream LLM series across 2,500 real-world skills from ClawHub. Our results reveal a striking popularity-security paradox, where download volume is not a reliable proxy for security quality, as over 90% of high-popularity skills failed to pass rigorous auditing. Crucially, we discovered that high-risk skills form a single giant connected component within the risk-link dimension, demonstrating that cascaded risks are systemic rather than isolated occurrences. We hope that SkillProbe will inspire researchers to provide a scalable governance infrastructure for constructing a trustworthy Agentic Web. SkillProbe is accessible for public experience at skillhub.holosai.io.

## 2603.22148v1 — OpenEarth-Agent: From Tool Calling to Tool Creation for Open-Environment Earth Observation

- URL: https://arxiv.org/abs/2603.22148v1
- Primary category: `cs.CV`
- Published: 2026-03-23T16:14:15Z

### Abstract

Earth Observation (EO) is essential for perceiving dynamic land surface changes, yet deploying autonomous EO in open environments is hindered by the immense diversity of multi-source data and heterogeneous tasks. While remote sensing agents have emerged to streamline EO workflows, existing tool-calling agents are confined to closed environments. They rely on pre-defined tools and are restricted to narrow scope, limiting their generalization to the diverse data and tasks. To overcome these limitations, we introduce OpenEarth-Agent, the first tool-creation agent framework tailored for open-environment EO. Rather than calling predefined tools, OpenEarth-Agent employs adaptive workflow planning and tool creation to generalize to unseen data and tasks. This adaptability is bolstered by an open-ended integration of multi-stage tools and cross-domain knowledge bases, enabling robust execution in the entire EO pipeline across multiple application domains. To comprehensively evaluate EO agents in open environments, we propose OpenEarth-Bench, a novel benchmark comprising 596 real-world, full-pipeline cases across seven application domains, explicitly designed to assess agents' adaptive planning and tool creation capabilities. Only essential pre-trained model tools are provided in this benchmark, devoid of any other predefined task-specific tools. Extensive experiments demonstrate that OpenEarth-Agent successfully masters full-pipeline EO across multiple domains in the open environment. Notably, on the cross-benchmark Earth-Bench, our tool-creating agent equipped with 6 essential pre-trained models achieves performance comparable to tool-calling agents relying on 104 specialized tools, and significantly outperforms them when provided with the complete toolset. In several cases, the created tools exhibit superior robustness to data anomalies compared to human-engineered counterparts.

## 2603.25723v1 — Natural-Language Agent Harnesses

- URL: https://arxiv.org/abs/2603.25723v1
- Primary category: `cs.CL`
- Published: 2026-03-26T17:58:15Z

### Abstract

Agent performance increasingly depends on \emph{harness engineering}, yet harness design is usually buried in controller code and runtime-specific conventions, making it hard to transfer, compare, and study as a scientific object. We ask whether the high-level control logic of an agent harness can instead be externalized as a portable executable artifact. We introduce \textbf{Natural-Language Agent Harnesses} (NLAHs), which express harness behavior in editable natural language, and \textbf{Intelligent Harness Runtime} (IHR), a shared runtime that executes these harnesses through explicit contracts, durable artifacts, and lightweight adapters. Across coding and computer-use benchmarks, we conduct controlled evaluations of operational viability, module ablation, and code-to-text harness migration.

## 2603.26778v1 — TED: Training-Free Experience Distillation for Multimodal Reasoning

- URL: https://arxiv.org/abs/2603.26778v1
- Primary category: `cs.LG`
- Published: 2026-03-25T01:08:36Z

### Abstract

Knowledge distillation is typically realized by transferring a teacher model's knowledge into a student's parameters through supervised or reinforcement-based optimization. While effective, such approaches require repeated parameter updates and large-scale training data, limiting their applicability in resource-constrained environments. In this work, we propose TED, a training-free, context-based distillation framework that shifts the update target of distillation from model parameters to an in-context experience injected into the student's prompt. For each input, the student generates multiple reasoning trajectories, while a teacher independently produces its own solution. The teacher then compares the student trajectories with its reasoning and the ground-truth answer, extracting generalized experiences that capture effective reasoning patterns. These experiences are continuously refined and updated over time. A key challenge of context-based distillation is unbounded experience growth and noise accumulation. TED addresses this with an experience compression mechanism that tracks usage statistics and selectively merges, rewrites, or removes low-utility experiences. Experiments on multimodal reasoning benchmarks MathVision and VisualPuzzles show that TED consistently improves performance. On MathVision, TED raises the performance of Qwen3-VL-8B from 0.627 to 0.702, and on VisualPuzzles from 0.517 to 0.561 with just 100 training samples. Under this low-data, no-update setting, TED achieves performance competitive with fully trained parameter-based distillation while reducing training cost by over 5x, demonstrating that meaningful knowledge transfer can be achieved through contextual experience.

## 2603.26996v1 — FormalProofBench: Can Models Write Graduate Level Math Proofs That Are Formally Verified?

- URL: https://arxiv.org/abs/2603.26996v1
- Primary category: `cs.AI`
- Published: 2026-03-27T21:14:53Z

### Abstract

We present FormalProofBench, a private benchmark designed to evaluate whether AI models can produce formally verified mathematical proofs at the graduate level. Each task pairs a natural-language problem with a Lean~4 formal statement, and a model must output a Lean proof accepted by the Lean 4 checker. FormalProofBench targets advanced undergraduate and graduate mathematics, with problems drawn from qualifying exams and standard textbooks across topics including analysis, algebra, probability, and logic. We evaluate a range of frontier models with an agentic harness, and find that the best-performing foundation model achieves 33.5% accuracy, with performance dropping rapidly after that. In addition to the accuracy numbers, we also provide empirical analysis of tool-use, failure modes, cost and latency, thereby providing a thorough evaluation of the formal-theorem proving abilities of frontier models.

## 2603.27813v1 — MuSEAgent: A Multimodal Reasoning Agent with Stateful Experiences

- URL: https://arxiv.org/abs/2603.27813v1
- Primary category: `cs.CV`
- Published: 2026-03-29T18:54:31Z

### Abstract

Research agents have recently achieved significant progress in information seeking and synthesis across heterogeneous textual and visual sources. In this paper, we introduce MuSEAgent, a multimodal reasoning agent that enhances decision-making by extending the capabilities of research agents to discover and leverage stateful experiences. Rather than relying on trajectory-level retrieval, we propose a stateful experience learning paradigm that abstracts interaction data into atomic decision experiences through hindsight reasoning. These experiences are organized into a quality-filtered experience bank that supports policy-driven experience retrieval at inference time. Specifically, MuSEAgent enables adaptive experience exploitation through complementary wide- and deep-search strategies, allowing the agent to dynamically retrieve multimodal guidance across diverse compositional semantic viewpoints. Extensive experiments demonstrate that MuSEAgent consistently outperforms strong trajectory-level experience retrieval baselines on both fine-grained visual perception and complex multimodal reasoning tasks. These results validate the effectiveness of stateful experience modeling in improving multimodal agent reasoning.

## 2603.28052v1 — Meta-Harness: End-to-End Optimization of Model Harnesses

- URL: https://arxiv.org/abs/2603.28052v1
- Primary category: `cs.AI`
- Published: 2026-03-30T05:33:50Z

### Abstract

The performance of large language model (LLM) systems depends not only on model weights, but also on their harness: the code that determines what information to store, retrieve, and present to the model. Yet harnesses are still designed largely by hand, and existing text optimizers are poorly matched to this setting because they compress feedback too aggressively. We introduce Meta-Harness, an outer-loop system that searches over harness code for LLM applications. It uses an agentic proposer that accesses the source code, scores, and execution traces of all prior candidates through a filesystem. On online text classification, Meta-Harness improves over a state-of-the-art context management system by 7.7 points while using 4x fewer context tokens. On retrieval-augmented math reasoning, a single discovered harness improves accuracy on 200 IMO-level problems by 4.7 points on average across five held-out models. On agentic coding, discovered harnesses surpass the best hand-engineered baselines on TerminalBench-2. Together, these results show that richer access to prior experience can enable automated harness engineering.

## 2603.28088v1 — GEMS: Agent-Native Multimodal Generation with Memory and Skills

- URL: https://arxiv.org/abs/2603.28088v1
- Primary category: `cs.CV`
- Published: 2026-03-30T06:42:55Z

### Abstract

Recent multimodal generation models have achieved remarkable progress on general-purpose generation tasks, yet continue to struggle with complex instructions and specialized downstream tasks. Inspired by the success of advanced agent frameworks such as Claude Code, we propose \textbf{GEMS} (Agent-Native Multimodal \textbf{GE}neration with \textbf{M}emory and \textbf{S}kills), a framework that pushes beyond the inherent limitations of foundational models on both general and downstream tasks. GEMS is built upon three core components. Agent Loop introduces a structured multi-agent framework that iteratively improves generation quality through closed-loop optimization. Agent Memory provides a persistent, trajectory-level memory that hierarchically stores both factual states and compressed experiential summaries, enabling a global view of the optimization process while reducing redundancy. Agent Skill offers an extensible collection of domain-specific expertise with on-demand loading, allowing the system to effectively handle diverse downstream applications. Across five mainstream tasks and four downstream tasks, evaluated on multiple generative backends, GEMS consistently achieves significant performance gains. Most notably, it enables the lightweight 6B model Z-Image-Turbo to surpass the state-of-the-art Nano Banana 2 on GenEval2, demonstrating the effectiveness of agent harness in extending model capabilities beyond their original limits.

## 2603.29199v1 — AEC-Bench: A Multimodal Benchmark for Agentic Systems in Architecture, Engineering, and Construction

- URL: https://arxiv.org/abs/2603.29199v1
- Primary category: `cs.AI`
- Published: 2026-03-31T03:10:28Z

### Abstract

The AEC-Bench is a multimodal benchmark for evaluating agentic systems on real-world tasks in the Architecture, Engineering, and Construction (AEC) domain. The benchmark covers tasks requiring drawing understanding, cross-sheet reasoning, and construction project-level coordination. This report describes the benchmark motivation, dataset taxonomy, evaluation protocol, and baseline results across several domain-specific foundation model harnesses. We use AEC-Bench to identify consistent tools and harness design techniques that uniformly improve performance across foundation models in their own base harnesses, such as Claude Code and Codex. We openly release our benchmark dataset, agent harness, and evaluation code for full replicability at https://github.com/nomic-ai/aec-bench under an Apache 2 license.

## 2604.00073 — Terminal Agents Suffice for Enterprise Automation

- URL: https://arxiv.org/abs/2604.00073
- Published: Mon, 06 Apr 2026 00:47:11 GMT

### Abstract

There has been growing interest in building agents that can interact with digital platforms to execute meaningful enterprise tasks autonomously. Among the approaches explored are tool-augmented agents built on abstractions such as Model Context Protocol (MCP) and web agents that operate through graphical interfaces. Yet, it remains unclear whether such complex agentic systems are necessary given their cost and operational overhead. We argue that a coding agent equipped only with a terminal and a filesystem can solve many enterprise tasks more effectively by interacting directly with platform APIs. We evaluate this hypothesis across diverse real-world systems and show that these low-level terminal agents match or outperform more complex agent architectures. Our findings suggest that simple programmatic interfaces, combined with strong foundation models, are sufficient for practical enterprise automation.

## 2604.00362v1 — In harmony with gpt-oss

- URL: https://arxiv.org/abs/2604.00362v1
- Primary category: `cs.AI`
- Published: 2026-04-01T01:16:13Z

### Abstract

No one has independently reproduced OpenAI's published scores for gpt-oss-20b with tools, because the original paper discloses neither the tools nor the agent harness. We reverse-engineered the model's in-distribution tools: when prompted without tool definitions, gpt-oss still calls tools from its training distribution with high statistical confidence -- a strong prior, not a hallucination. We then built a native harmony agent harness (https://github.com/borislavmavrin/harmonyagent.git) that encodes messages in the model's native format, bypassing the lossy Chat Completions conversion. Together, these yield the first independent reproduction of OpenAI's published scores: 60.4% on SWE Verified HIGH (published 60.7%), 53.3% MEDIUM (53.2%), and 91.7% on AIME25 with tools (90.4%).

## 2604.02334v1 — Holos: A Web-Scale LLM-Based Multi-Agent System for the Agentic Web

- URL: https://arxiv.org/abs/2604.02334v1
- Primary category: `cs.AI`
- Published: 2026-01-18T13:09:25Z

### Abstract

As large language models (LLM)-driven agents transition from isolated task solvers to persistent digital entities, the emergence of the Agentic Web, an ecosystem where heterogeneous agents autonomously interact and co-evolve, marks a pivotal shift toward Artificial General Intelligence (AGI). However, LLM-based multi-agent systems (LaMAS) are hindered by open-world issues such as scaling friction, coordination breakdown, and value dissipation. To address these challenges, we introduce Holos, a web-scale LaMAS architected for long-term ecological persistence. Holos adopts a five-layer architecture, with core modules primarily featuring the Nuwa engine for high-efficiency agent generation and hosting, a market-driven Orchestrator for resilient coordination, and an endogenous value cycle to achieve incentive compatibility. By bridging the gap between micro-level collaboration and macro-scale emergence, Holos hopes to lay the foundation for the next generation of the self-organizing and continuously evolving Agentic Web. We have publicly released Holos (accessible at https://holosai.io), providing a resource for the community and a testbed for future research in large-scale agentic ecosystems.

## 2604.03088v3 — SkVM: Revisiting Language VM for Skills across Heterogenous LLMs and Harnesses

- URL: https://arxiv.org/abs/2604.03088v3
- Primary category: `cs.SE`
- Published: 2026-04-03T15:11:45Z

### Abstract

LLM agents increasingly adopt skills as a reusable unit of composition. While skills are shared across diverse agent platforms, current systems treat them as raw context, causing the same skill to behave inconsistently for different agents. This fragility undermines skill portability and execution efficiency. To address this challenge, we analyze 118,000 skills and draw inspiration from traditional compiler design. We treat skills as code and LLMs as heterogeneous processors. To make portability actionable, we decompose a skill's requirements into a set of primitive capabilities, and measure how well each model-harness pair supports them. Based on these capability profiles, we propose SkVM, a compilation and runtime system designed for portable and efficient skill execution. At compile time, SkVM performs capability-based compilation, environment binding, and concurrency extraction. At runtime, SkVM applies JIT code solidification and adaptive recompilation for performance optimization. We evaluate SkVM across eight LLMs of varying scales and three agent harnesses, covering SkillsBench and representative skill tasks. Results demonstrate that SkVM significantly improves task completion rates across different models and environments while reducing token consumption by up to 40%. In terms of performance, SkVM achieves up to 3.2x speedup with enhanced parallelism, and 19-50x latency reduction through code solidification.

## 2604.03610v1 — DebugHarness: Emulating Human Dynamic Debugging for Autonomous Program Repair

- URL: https://arxiv.org/abs/2604.03610v1
- Primary category: `cs.SE`
- Published: 2026-04-04T06:49:30Z

### Abstract

Patching severe security flaws in complex software remains a major challenge. While automated tools like fuzzers efficiently discover bugs, fixing deep-rooted low-level faults (e.g., use-after-free and memory corruption) still requires labor-intensive manual analysis by experts. Emerging Large Language Model (LLM) agents attempt to automate this pipeline, but they typically treat bug fixing as a purely static code-generation task. Relying solely on static artifacts, these methods miss the dynamic execution context strictly necessary for diagnosing intricate memory safety violations. To overcome these limitations, we introduce DebugHarness, an autonomous LLM-powered debugging agent harness that resolves complex vulnerabilities by emulating the interactive debugging practices of human systems engineers. Instead of merely examining static code, DebugHarness actively queries the live runtime environment. Driven by a reproducible crash, it utilizes a pattern-guided investigation strategy to formulate hypotheses, interactively probes program memory states and execution paths, and synthesizes patches via a closed-loop validation cycle. We evaluate DebugHarness on SEC-bench, a rigorous dataset of real-world C/C++ security vulnerabilities. DebugHarness successfully patches approximately 90% of the evaluated bugs. This yields a relative improvement of over 30% compared to state-of-the-art baselines, demonstrating that dynamic debugging significantly enhances LLM diagnostic capabilities. Overall, DebugHarness establishes a novel paradigm for automated program repair, bridging the gap between static LLM reasoning and the dynamic intricacies of low-level systems programming.

## 2604.07833v2 — Harnessing Embodied Agents: Runtime Governance for Policy-Constrained Execution

- URL: https://arxiv.org/abs/2604.07833v2
- Primary category: `cs.RO`
- Published: 2026-04-09T05:35:08Z

### Abstract

Embodied agents are evolving from passive reasoning systems into active executors that interact with tools, robots, and physical environments. Once granted execution authority, the central challenge becomes how to keep actions governable at runtime. Existing approaches embed safety and recovery logic inside the agent loop, making execution control difficult to standardize, audit, and adapt. This paper argues that embodied intelligence requires not only stronger agents, but stronger runtime governance. We propose a framework for policy-constrained execution that separates agent cognition from execution oversight. Governance is externalized into a dedicated runtime layer performing policy checking, capability admission, execution monitoring, rollback handling, and human override. We formalize the control boundary among the embodied agent, Embodied Capability Modules (ECMs), and runtime governance layer, and validate through 1000 randomized simulation trials across three governance dimensions. Results show 96.2% interception of unauthorized actions, reduction of unsafe continuation from 100% to 22.2% under runtime drift, and 91.4% recovery success with full policy compliance, substantially outperforming all baselines (p<0.001). By reframing runtime governance as a first-class systems problem, this paper positions policy-constrained execution as a key design principle for embodied agent systems.

## 2604.08224v1 — Externalization in LLM Agents: A Unified Review of Memory, Skills, Protocols and Harness Engineering

- URL: https://arxiv.org/abs/2604.08224v1
- Primary category: `cs.SE`
- Published: 2026-04-09T13:19:41Z

### Abstract

Large language model (LLM) agents are increasingly built less by changing model weights than by reorganizing the runtime around them. Capabilities that earlier systems expected the model to recover internally are now externalized into memory stores, reusable skills, interaction protocols, and the surrounding harness that makes these modules reliable in practice. This paper reviews that shift through the lens of externalization. Drawing on the idea of cognitive artifacts, we argue that agent infrastructure matters not merely because it adds auxiliary components, but because it transforms hard cognitive burdens into forms that the model can solve more reliably. Under this view, memory externalizes state across time, skills externalize procedural expertise, protocols externalize interaction structure, and harness engineering serves as the unification layer that coordinates them into governed execution. We trace a historical progression from weights to context to harness, analyze memory, skills, and protocols as three distinct but coupled forms of externalization, and examine how they interact inside a larger agent system. We further discuss the trade-off between parametric and externalized capability, identify emerging directions such as self-evolving harnesses and shared agent infrastructure, and discuss open challenges in evaluation, governance, and the long-term co-evolution of models and external infrastructure. The result is a systems-level framework for explaining why practical agent progress increasingly depends not only on stronger models, but on better external cognitive infrastructure.

## 2604.08590v1 — AlphaLab: Autonomous Multi-Agent Research Across Optimization Domains with Frontier LLMs

- URL: https://arxiv.org/abs/2604.08590v1
- Primary category: `cs.LG`
- Published: 2026-03-31T21:16:20Z

### Abstract

We present AlphaLab, an autonomous research harness that leverages frontier LLM agentic capabilities to automate the full experimental cycle in quantitative, computation-intensive domains. Given only a dataset and a natural-language objective, AlphaLab proceeds through three phases without human intervention: (1) it adapts to the domain and explores the data, writing analysis code and producing a research report; (2) it constructs and adversarially validates its own evaluation framework; and (3) it runs large-scale GPU experiments via a Strategist/Worker loop, accumulating domain knowledge in a persistent playbook that functions as a form of online prompt optimization. All domain-specific behavior is factored into adapters generated by the model itself, so the same pipeline handles qualitatively different tasks without modification. We evaluate AlphaLab with two frontier LLMs (GPT-5.2 and Claude Opus 4.6) on three domains: CUDA kernel optimization, where it writes GPU kernels that run 4.4x faster than torch.compile on average (up to 91x); LLM pretraining, where the full system achieves 22% lower validation loss than a single-shot baseline using the same model; and traffic forecasting, where it beats standard baselines by 23-25% after researching and implementing published model families from the literature. The two models discover qualitatively different solutions in every domain (neither dominates uniformly), suggesting that multi-model campaigns provide complementary search coverage. We additionally report results on financial time series forecasting in the appendix, and release all code at https://brendanhogan.github.io/alphalab-paper/.

## 2604.08756v1 — Artifacts as Memory Beyond the Agent Boundary

- URL: https://arxiv.org/abs/2604.08756v1
- Primary category: `cs.AI`
- Published: 2026-04-09T20:39:59Z

### Abstract

The situated view of cognition holds that intelligent behavior depends not only on internal memory, but on an agent's active use of environmental resources. Here, we begin formalizing this intuition within Reinforcement Learning (RL). We introduce a mathematical framing for how the environment can functionally serve as an agent's memory, and prove that certain observations, which we call artifacts, can reduce the information needed to represent history. We corroborate our theory with experiments showing that when agents observe spatial paths, the amount of memory required to learn a performant policy is reduced. Interestingly, this effect arises unintentionally, and implicitly through the agent's sensory stream. We discuss the implications of our findings, and show they satisfy qualitative properties previously used to ground accounts of external memory. Moving forward, we anticipate further work on this subject could reveal principled ways to exploit the environment as a substitute for explicit internal memory.

## 2604.11378v1 — From Agent Loops to Structured Graphs:A Scheduler-Theoretic Framework for LLM Agent Execution

- URL: https://arxiv.org/abs/2604.11378v1
- Primary category: `cs.AI`
- Published: 2026-04-13T12:16:45Z

### Abstract

The dominant paradigm for building LLM based agents is the Agent Loop, an iterative cycle where a single language model decides what to do next by reading an ever growing context window. This paradigm has three structural weaknesses: implicit dependencies between steps, unbounded recovery loops, and mutable execution history that complicates debugging. We characterize the Agent Loop as a single ready unit scheduler: at any moment, at most one executable unit is active, and the choice of which unit to activate comes from opaque LLM inference rather than an inspectable policy. This perspective places Agent Loops and graph based execution engines on a single semantic continuum. We propose SGH, Structured Graph Harness, which lifts control flow from implicit context into an explicit static DAG. SGH makes three commitments: execution plans are immutable within a plan version, planning execution and recovery are separated into three layers, and recovery follows a strict escalation protocol. These choices trade some expressiveness for controllability, verifiability, and implementability. Our contributions are fourfold: a scheduler unified framework that applies classical scheduling theory to LLM agent execution and identifies challenges introduced by non deterministic LLM nodes; a trade off analysis of controllability, expressiveness, and implementability across 70 surveyed systems; a formal specification including a node state machine with termination and soundness guarantees; and an attributable experimental framework with a seven group design for future validation. This is a position paper and design proposal. We provide a theoretical framework, design analysis, and experimental protocol, not a production implementation or empirical results.

## 2604.11535v1 — Problem Reductions at Scale: Agentic Integration of Computationally Hard Problems

- URL: https://arxiv.org/abs/2604.11535v1
- Primary category: `cs.AI`
- Published: 2026-04-13T14:32:08Z

### Abstract

Solving an NP-hard optimization problem often requires reformulating it for a specific solver -- quantum hardware, a commercial optimizer, or a domain heuristic. A tool for polynomial-time reductions between hard problems would let practitioners route any supported problem to any supported solver through a single interface. Building such a library at scale, however, has remained out of reach. We show that harness engineering, the practice of designing constraints, verification systems, and feedback loops that channel AI coding agents, can overcome this barrier. Our harness combines a no-code contribution route for domain experts, a multilayer verification stack ranging from type-level checks to agentic feature tests (AI agents role-playing as end users), and a fully automated implementation-review-integration pipeline. In about three months, we built a command-line tool backed by a library of 100+ problem types and 200+~reduction rules in over 170k lines of Rust. The result suggests that a well-engineered harness lets agents build well-tested software at a scale and pace beyond prior reduction-library efforts. Because the reduction graph composes transitively, a new solver registered for any single problem type instantly becomes available to every problem connected by a reduction path. The source code is available at https://github.com/CodingThrust/problem-reductions.

## 2604.11548v1 — SemaClaw: A Step Towards General-Purpose Personal AI Agents through Harness Engineering

- URL: https://arxiv.org/abs/2604.11548v1
- Primary category: `cs.AI`
- Published: 2026-04-13T14:37:53Z

### Abstract

The rise of OpenClaw in early 2026 marks the moment when millions of users began deploying personal AI agents into their daily lives, delegating tasks ranging from travel planning to multi-step research. This scale of adoption signals that two parallel arcs of development have reached an inflection point. First is a paradigm shift in AI engineering, evolving from prompt and context engineering to harness engineering-designing the complete infrastructure necessary to transform unconstrained agents into controllable, auditable, and production-reliable systems. As model capabilities converge, this harness layer is becoming the primary site of architectural differentiation. Second is the evolution of human-agent interaction from discrete tasks toward a persistent, contextually aware collaborative relationship, which demands open, trustworthy and extensible harness infrastructure. We present SemaClaw, an open-source multi-agent application framework that addresses these shifts by taking a step towards general-purpose personal AI agents through harness engineering. Our primary contributions include a DAG-based two-phase hybrid agent team orchestration method, a PermissionBridge behavioral safety system, a three-tier context management architecture, and an agentic wiki skill for automated personal knowledge base construction.

## 2604.11784v1 — ClawGUI: A Unified Framework for Training, Evaluating, and Deploying GUI Agents

- URL: https://arxiv.org/abs/2604.11784v1
- Primary category: `cs.LG`
- Published: 2026-04-13T17:52:04Z

### Abstract

GUI agents drive applications through their visual interfaces instead of programmatic APIs, interacting with arbitrary software via taps, swipes, and keystrokes, reaching a long tail of applications that CLI-based agents cannot. Yet progress in this area is bottlenecked less by modeling capacity than by the absence of a coherent full-stack infrastructure: online RL training suffers from environment instability and closed pipelines, evaluation protocols drift silently across works, and trained agents rarely reach real users on real devices. We present \textbf{ClawGUI}, an open-source framework addressing these three gaps within a single harness. \textbf{ClawGUI-RL} provides the first open-source GUI agent RL infrastructure with validated support for both parallel virtual environments and real physical devices, integrating GiGPO with a Process Reward Model for dense step-level supervision. \textbf{ClawGUI-Eval} enforces a fully standardized evaluation pipeline across 6 benchmarks and 11+ models, achieving 95.8\% reproduction against official baselines. \textbf{ClawGUI-Agent} brings trained agents to Android, HarmonyOS, and iOS through 12+ chat platforms with hybrid CLI-GUI control and persistent personalized memory. Trained end to end within this pipeline, \textbf{ClawGUI-2B} achieves 17.1\% Success Rate on MobileWorld GUI-Only, outperforming the same-scale MAI-UI-2B baseline by 6.0\%.

## 2604.11811v1 — M$^\star$: Every Task Deserves Its Own Memory Harness

- URL: https://arxiv.org/abs/2604.11811v1
- Primary category: `cs.PL`
- Published: 2026-04-10T03:22:26Z

### Abstract

Large language model agents rely on specialized memory systems to accumulate and reuse knowledge during extended interactions. Recent architectures typically adopt a fixed memory design tailored to specific domains, such as semantic retrieval for conversations or skills reused for coding. However, a memory system optimized for one purpose frequently fails to transfer to others. To address this limitation, we introduce M$^\star$, a method that automatically discovers task-optimized memory harnesses through executable program evolution. Specifically, M$^\star$ models an agent memory system as a memory program written in Python. This program encapsulates the data Schema, the storage Logic, and the agent workflow Instructions. We optimize these components jointly using a reflective code evolution method; this approach employs a population-based search strategy and analyzes evaluation failures to iteratively refine the candidate programs. We evaluate M$^\star$ on four distinct benchmarks spanning conversation, embodied planning, and expert reasoning. Our results demonstrate that M$^\star$ improves performance over existing fixed-memory baselines robustly across all evaluated tasks. Furthermore, the evolved memory programs exhibit structurally distinct processing mechanisms for each domain. This finding indicates that specializing the memory mechanism for a given task explores a broad design space and provides a superior solution compared to general-purpose memory paradigms.

## 2604.12064v1 — LLM-Redactor: An Empirical Evaluation of Eight Techniques for Privacy-Preserving LLM Requests

- URL: https://arxiv.org/abs/2604.12064v1
- Primary category: `cs.CR`
- Published: 2026-04-13T21:05:42Z

### Abstract

Coding agents and LLM-powered applications routinely send potentially sensitive content to cloud LLM APIs where it may be logged, retained, used for training, or subpoenaed. Existing privacy tooling focuses on network-level encryption and organization-level DLP, neither of which addresses the content of prompts themselves. We present a systematic empirical evaluation of eight techniques for privacy-preserving LLM requests: (A) local-only inference, (B) redaction with placeholder restoration, (C) semantic rephrasing, (D) Trusted Execution Environment hosted inference, (E) split inference, (F) fully homomorphic encryption, (G) secret sharing via multi-party computation, and (H) differential-privacy noise. We implement all eight (or a tractable research-stage subset where deployment is not yet feasible) in an open-source shim compatible with MCP and any OpenAI-compatible API. We evaluate the four practical options (A, B, C, H) and their combinations across four workload classes using a ground-truth-labelled leak benchmark of 1,300 samples with 4,014 annotations. Our headline finding is that no single technique dominates: the combination A+B+C (route locally when possible, redact and rephrase the rest) achieves 0.6% combined leak on PII and 31.3% on proprietary code, with zero exact leaks on PII across 500 samples. We present a decision rule that selects the appropriate option(s) from a threat-model budget and workload characterisation. Code, benchmarks, and evaluation harness are released at https://github.com/jayluxferro/llm-redactor.

## 2604.12162v1 — AlphaEval: Evaluating Agents in Production

- URL: https://arxiv.org/abs/2604.12162v1
- Primary category: `cs.CL`
- Published: 2026-04-14T00:43:20Z

### Abstract

The rapid deployment of AI agents in commercial settings has outpaced the development of evaluation methodologies that reflect production realities. Existing benchmarks measure agent capabilities through retrospectively curated tasks with well-specified requirements and deterministic metrics -- conditions that diverge fundamentally from production environments where requirements contain implicit constraints, inputs are heterogeneous multi-modal documents with information fragmented across sources, tasks demand undeclared domain expertise, outputs are long-horizon professional deliverables, and success is judged by domain experts whose standards evolve over time. We present AlphaEval, a production-grounded benchmark of 94 tasks sourced from seven companies deploying AI agents in their core business, spanning six O*NET (Occupational Information Network) domains. Unlike model-centric benchmarks, AlphaEval evaluates complete agent products -- Claude Code, Codex, etc. -- as commercial systems, capturing performance variations invisible to model-level evaluation. Our evaluation framework covers multiple paradigms (LLM-as-a-Judge, reference-driven metrics, formal verification, rubric-based assessment, automated UI testing, etc.), with individual domains composing multiple paradigms. Beyond the benchmark itself, we contribute a requirement-to-benchmark construction framework -- a systematic methodology that transforms authentic production requirements into executable evaluation tasks in minimal time. This framework standardizes the entire pipeline from requirement to evaluation, providing a reproducible, modular process that any organization can adopt to construct production-grounded benchmarks for their own domains.

## 2604.13018v1 — Toward Autonomous Long-Horizon Engineering for ML Research

- URL: https://arxiv.org/abs/2604.13018v1
- Primary category: `cs.CL`
- Published: 2026-04-14T17:55:16Z

### Abstract

Autonomous AI research has advanced rapidly, but long-horizon ML research engineering remains difficult: agents must sustain coherent progress across task comprehension, environment setup, implementation, experimentation, and debugging over hours or days. We introduce AiScientist, a system for autonomous long-horizon engineering for ML research built on a simple principle: strong long-horizon performance requires both structured orchestration and durable state continuity. To this end, AiScientist combines hierarchical orchestration with a permission-scoped File-as-Bus workspace: a top-level Orchestrator maintains stage-level control through concise summaries and a workspace map, while specialized agents repeatedly re-ground on durable artifacts such as analyses, plans, code, and experimental evidence rather than relying primarily on conversational handoffs, yielding thin control over thick state. Across two complementary benchmarks, AiScientist improves PaperBench score by 10.54 points on average over the best matched baseline and achieves 81.82 Any Medal% on MLE-Bench Lite. Ablation studies further show that File-as-Bus protocol is a key driver of performance, reducing PaperBench by 6.41 points and MLE-Bench Lite by 31.82 points when removed. These results suggest that long-horizon ML research engineering is a systems problem of coordinating specialized work over durable project state, rather than a purely local reasoning problem.

## 2604.13151v1 — Exploration and Exploitation Errors Are Measurable for Language Model Agents

- URL: https://arxiv.org/abs/2604.13151v1
- Primary category: `cs.AI`
- Published: 2026-04-14T17:59:57Z

### Abstract

Language Model (LM) agents are increasingly used in complex open-ended decision-making tasks, from AI coding to physical AI. A core requirement in these settings is the ability to both explore the problem space and exploit acquired knowledge effectively. However, systematically distinguishing and quantifying exploration and exploitation from observed actions without access to the agent's internal policy remains challenging. To address this, we design controllable environments inspired by practical embodied AI scenarios. Each environment consists of a partially observable 2D grid map and an unknown task Directed Acyclic Graph (DAG). The map generation can be programmatically adjusted to emphasize exploration or exploitation difficulty. To enable policy-agnostic evaluation, we design a metric to quantify exploration and exploitation errors from agent's actions. We evaluate a variety of frontier LM agents and find that even state-of-the-art models struggle on our task, with different models exhibiting distinct failure modes. We further observe that reasoning models solve the task more effectively and show both exploration and exploitation can be significantly improved through minimal harness engineering. We release our code \href{https://github.com/jjj-madison/measurable-explore-exploit}{here}.

## 2604.13282v1 — Agentic MR sequence development: leveraging LLMs with MR skills for automatic physics-informed sequence development

- URL: https://arxiv.org/abs/2604.13282v1
- Primary category: `physics.med-ph`
- Published: 2026-04-14T20:17:47Z

### Abstract

Purpose: Novel MR sequence developments still today allow generation of new diagnostic tools or novel imaging biomarkers. Programming MRI pulse sequences, however, is time-consuming and requires deep expertise in sequence design, restrictions by hardware constraints and MRI physics; even small modifications often require substantial debugging and validation. LLMs can assist when given structured prompts and error feedback, but many generated sequences still exhibit physical inconsistencies. We present Agent4MR, an agent-based framework that automatically generates and refines PyPulseq sequences using a structured, physics-aware validation report. These agents can perform also autonomous research. Methods: We evaluated Agent4MR on a spin-echo EPI task across three state-of-the-art LLMs and compared it to a context-only baseline (LLM4MR) and to a human developer with the same tools. We tested an MR autoresearch on a fluid-suppressed spin-echo EPI challenge for three different model generations. Results: Across all models, Agent4MR consistently produced artifact-free, physically valid sequences in a single user interaction, reducing the number of required interactions below the human baseline while maintaining correct timing and k-space coverage. Autonomous agents could then improve a sequence to match a given target contrast in an autoresearch approach. Conclusion: An appropriate agentic harness with physics-based validation can turn general-purpose LLMs into reliable MRI sequence developers and may ultimately enable non-experts to refine or innovate MR sequences guided by biological or clinical questions, or let swarms of agents realize sequence programming for them. Keywords: MRI; pulse sequence; PyPulseq; large language models; agents; autoresearch, sequence development.

## 2604.13318v1 — WebXSkill: Skill Learning for Autonomous Web Agents

- URL: https://arxiv.org/abs/2604.13318v1
- Primary category: `cs.AI`
- Published: 2026-04-14T21:48:15Z

### Abstract

Autonomous web agents powered by large language models (LLMs) have shown promise in completing complex browser tasks, yet they still struggle with long-horizon workflows. A key bottleneck is the grounding gap in existing skill formulations: textual workflow skills provide natural language guidance but cannot be directly executed, while code-based skills are executable but opaque to the agent, offering no step-level understanding for error recovery or adaptation. We introduce WebXSkill, a framework that bridges this gap with executable skills, each pairing a parameterized action program with step-level natural language guidance, enabling both direct execution and agent-driven adaptation. WebXSkill operates in three stages: skill extraction mines reusable action subsequences from readily available synthetic agent trajectories and abstracts them into parameterized skills, skill organization indexes skills into a URL-based graph for context-aware retrieval, and skill deployment exposes two complementary modes, grounded mode for fully automated multi-step execution and guided mode where skills serve as step-by-step instructions that the agent follows with its native planning. On WebArena and WebVoyager, WebXSkill improves task success rate by up to 9.8 and 12.9 points over the baseline, respectively, demonstrating the effectiveness of executable skills for web agents. The code is publicly available at https://github.com/aiming-lab/WebXSkill.

## 2604.13346v1 — AgentSPEX: An Agent SPecification and EXecution Language

- URL: https://arxiv.org/abs/2604.13346v1
- Primary category: `cs.CL`
- Published: 2026-04-14T23:16:25Z

### Abstract

Language-model agent systems commonly rely on reactive prompting, in which a single instruction guides the model through an open-ended sequence of reasoning and tool-use steps, leaving control flow and intermediate state implicit and making agent behavior potentially difficult to control. Orchestration frameworks such as LangGraph, DSPy, and CrewAI impose greater structure through explicit workflow definitions, but tightly couple workflow logic with Python, making agents difficult to maintain and modify. In this paper, we introduce AgentSPEX, an Agent SPecification and EXecution Language for specifying LLM-agent workflows with explicit control flow and modular structure, along with a customizable agent harness. AgentSPEX supports typed steps, branching and loops, parallel execution, reusable submodules, and explicit state management, and these workflows execute within an agent harness that provides tool access, a sandboxed virtual environment, and support for checkpointing, verification, and logging. Furthermore, we provide a visual editor with synchronized graph and workflow views for authoring and inspection. We include ready-to-use agents for deep research and scientific research, and we evaluate AgentSPEX on 7 benchmarks. Finally, we show through a user study that AgentSPEX provides a more interpretable and accessible workflow-authoring paradigm than a popular existing agent framework.

## 2604.13630v1 — SafeHarness: Lifecycle-Integrated Security Architecture for LLM-based Agent Deployment

- URL: https://arxiv.org/abs/2604.13630v1
- Primary category: `cs.CR`
- Published: 2026-04-15T08:59:00Z

### Abstract

The performance of large language model (LLM) agents depends critically on the execution harness, the system layer that orchestrates tool use, context management, and state persistence. Yet this same architectural centrality makes the harness a high-value attack surface: a single compromise at the harness level can cascade through the entire execution pipeline. We observe that existing security approaches suffer from structural mismatch, leaving them blind to harness-internal state and unable to coordinate across the different phases of agent operation. In this paper, we introduce \safeharness{}, a security architecture in which four proposed defense layers are woven directly into the agent lifecycle to address above significant limitations: adversarial context filtering at input processing, tiered causal verification at decision making, privilege-separated tool control at action execution, and safe rollback with adaptive degradation at state update. The proposed cross-layer mechanisms tie these layers together, escalating verification rigor, triggering rollbacks, and tightening tool privileges whenever sustained anomalies are detected. We evaluate \safeharness{} on benchmark datasets across diverse harness configurations, comparing against four security baselines under five attack scenarios spanning six threat categories. Compared to the unprotected baseline, \safeharness{} achieves an average reduction of approximately 38\% in UBR and 42\% in ASR, substantially lowering both the unsafe behavior rate and the attack success rate while preserving core task utility.

## 2604.13759v1 — The cognitive companion: a lightweight parallel monitoring architecture for detecting and recovering from reasoning degradation in LLM agents

- URL: https://arxiv.org/abs/2604.13759v1
- Primary category: `cs.AI`
- Published: 2026-04-15T11:44:20Z

### Abstract

Large language model (LLM) agents on multi-step tasks suffer reasoning degradation, looping, drift, stuck states, at rates up to 30% on hard tasks. Current solutions include hard step limits (abrupt) or LLM-as-judge monitoring (10-15% overhead per step). This paper introduces the Cognitive Companion, a parallel monitoring architecture with two implementations: an LLM-based Companion and a novel zero-overhead Probe-based Companion. We report a three-batch feasibility study centered on Gemma 4 E4B, with an additional exploratory small-model analysis on Qwen 2.5 1.5B and Llama 3.2 1B. In our experiments, the LLM-based Companion reduced repetition on loop-prone tasks by 52-62% with approximately 11% overhead. The Probe-based Companion, trained on hidden states from layer 28, showed a mean effect size of +0.471 at zero measured inference overhead; its strongest probe result achieved cross-validated AUROC 0.840 on a small proxy-labeled dataset. A key empirical finding is that companion benefit appears task-type dependent: companions are most helpful on loop-prone and open-ended tasks, while effects are neutral or negative on more structured tasks. Our small-model experiments also suggest a possible scale boundary: companions did not improve the measured quality proxy on 1B-1.5B models, even when interventions fired. Overall, the paper should be read as a feasibility study rather than a definitive validation. The results provide encouraging evidence that sub-token monitoring may be useful, identify task-type sensitivity as a practical design constraint, and motivate selective companion activation as a promising direction for future work.

## 2604.14004v1 — Memory Transfer Learning: How Memories are Transferred Across Domains in Coding Agents

- URL: https://arxiv.org/abs/2604.14004v1
- Primary category: `cs.AI`
- Published: 2026-04-15T15:50:29Z

### Abstract

Memory-based self-evolution has emerged as a promising paradigm for coding agents. However, existing approaches typically restrict memory utilization to homogeneous task domains, failing to leverage the shared infrastructural foundations, such as runtime environments and programming languages, that exist across diverse real-world coding problems. To address this limitation, we investigate \textbf{Memory Transfer Learning} (MTL) by harnessing a unified memory pool from heterogeneous domains. We evaluate performance across 6 coding benchmarks using four memory representations, ranging from concrete traces to abstract insights. Our experiments demonstrate that cross-domain memory improves average performance by 3.7\%, primarily by transferring meta-knowledge, such as validation routines, rather than task-specific code. Importantly, we find that abstraction dictates transferability; high-level insights generalize well, whereas low-level traces often induce negative transfer due to excessive specificity. Furthermore, we show that transfer effectiveness scales with the size of the memory pool, and memory can be transferred even between different models. Our work establishes empirical design principles for expanding memory utilization beyond single-domain silos. Project page: https://memorytransfer.github.io/

## 2604.14228v1 — Dive into Claude Code: The Design Space of Today's and Future AI Agent Systems

- URL: https://arxiv.org/abs/2604.14228v1
- Primary category: `cs.SE`
- Published: 2026-04-14T17:59:37Z

### Abstract

Claude Code is an agentic coding tool that can run shell commands, edit files, and call external services on behalf of the user. This study describes its comprehensive architecture by analyzing the publicly available TypeScript source code and further comparing it with OpenClaw, an independent open-source AI agent system that answers many of the same design questions from a different deployment context. Our analysis identifies five human values, philosophies, and needs that motivate the architecture (human decision authority, safety and security, reliable execution, capability amplification, and contextual adaptability) and traces them through thirteen design principles to specific implementation choices. The core of the system is a simple while-loop that calls the model, runs tools, and repeats. Most of the code, however, lives in the systems around this loop: a permission system with seven modes and an ML-based classifier, a five-layer compaction pipeline for context management, four extensibility mechanisms (MCP, plugins, skills, and hooks), a subagent delegation mechanism with worktree isolation, and append-oriented session storage. A comparison with OpenClaw, a multi-channel personal assistant gateway, shows that the same recurring design questions produce different architectural answers when the deployment context changes: from per-action safety classification to perimeter-level access control, from a single CLI loop to an embedded runtime within a gateway control plane, and from context-window extensions to gateway-wide capability registration. We finally identify six open design directions for future agent systems, grounded in recent empirical, architectural, and policy literature.

## 2604.15034v2 — Autogenesis: A Self-Evolving Agent Protocol

- URL: https://arxiv.org/abs/2604.15034v2
- Primary category: `cs.AI`
- Published: 2026-04-16T14:04:06Z

### Abstract

Recent advances in LLM based agent systems have shown promise in tackling complex, long horizon tasks. However, existing agent protocols (e.g., A2A and MCP) under specify cross entity lifecycle and context management, version tracking, and evolution safe update interfaces, which encourages monolithic compositions and brittle glue code. We introduce Autogenesis Protocol (AGP), a self evolution protocol that decouples what evolves from how evolution occurs. Its Resource Substrate Protocol Layer (RSPL) models prompts, agents, tools, environments, and memory as protocol registered resources with explicit state, lifecycle, and versioned interfaces. Its Self Evolution Protocol Layer (SEPL) specifies a closed loop operator interface for proposing, assessing, and committing improvements with auditable lineage and rollback. Building on AGP, we present Autogenesis System (AGS), a self-evolving multi-agent system that dynamically instantiates, retrieves, and refines protocol-registered resources during execution. We evaluate AGS on multiple challenging benchmarks that require long horizon planning and tool use across heterogeneous resources. The results demonstrate consistent improvements over strong baselines, supporting the effectiveness of agent resource management and closed loop self evolution. The code is available at https://github.com/DVampire/Autogenesis.

## 2604.18071v1 — Architectural Design Decisions in AI Agent Harnesses

- URL: https://arxiv.org/abs/2604.18071v1
- Primary category: `cs.AI`
- Published: 2026-04-20T10:39:34Z

### Abstract

AI agent systems increasingly rely on reusable non-LLM engineering infrastructure that packages tool mediation, context handling, delegation, safety control, and orchestration. Yet the architectural design decisions in this surrounding infrastructure remain understudied. This paper presents a protocol-guided, source-grounded empirical study of 70 publicly available agent-system projects, addressing three questions: which design-decision dimensions recur across projects, which co-occurrences structure those decisions, and which typical architectural patterns emerge. Methodologically, we contribute a transparent investigation procedure for analyzing heterogeneous agent-system corpora through source-code and technical-material reading. Empirically, we identify five recurring design dimensions (subagent architecture, context management, tool systems, safety mechanisms, and orchestration) and find that the corpus favors file-persistent, hybrid, and hierarchical context strategies; registry-oriented tool systems remain dominant while MCP- and plugin-oriented extensions are emerging; and intermediate isolation is common but high-assurance audit is rare. Cross-project co-occurrence analysis reveals that deeper coordination pairs with more explicit context services, stronger execution environments with more structured governance, and formalized tool-registration boundaries with broader ecosystem ambitions. We synthesize five recurring architectural patterns spanning lightweight tools, balanced CLI frameworks, multi-agent orchestrators, enterprise systems, and scenario-verticalized projects. The result provides an evidence-based account of architectural regularities in agent-system engineering, with grounded guidance for framework designers, selectors, and researchers.

## 2604.19572v2 — A Self-Evolving Framework for Efficient Terminal Agents via Observational Context Compression

- URL: https://arxiv.org/abs/2604.19572v2
- Primary category: `cs.CL`
- Published: 2026-04-21T15:25:54Z

### Abstract

As terminal agents scale to long-horizon, multi-turn workflows, a key bottleneck is not merely limited context length, but the accumulation of noisy terminal observations in the interaction history. Retaining raw observations preserves useful environment feedback, but also leads to context saturation and high token cost; conversely, naive compression may discard task-critical signals needed for subsequent actions. Because terminal environments are highly heterogeneous across repositories, commands, and execution states, heuristic-based or fixed-prompt compression methods are difficult to generalize. We propose TACO, a plug-and-play, training-free, self-evolving Terminal Agent Compression framework for existing terminal agents. TACO automatically discovers, refines, and reuses structured compression rules from interaction trajectories, enabling workflow-adaptive filtering of low-value terminal outputs while preserving task-relevant observations. Experiments on TerminalBench (TB 1.0 and TB 2.0) and four additional terminal-related benchmarks, including SWE-Bench Lite, CompileBench, DevEval, and CRUST-Bench, show that TACO consistently improves task performance and token efficiency across agent scaffolds and backbone models. On TerminalBench, TACO yields 1%-4% accuracy gains across strong agentic models and improves accuracy by around 2%-3% under the same token budget. On additional terminal-related benchmarks, it reduces total token consumption while maintaining or improving task success rates. These results suggest that self-evolving, workflow-adaptive observation compression is an effective path toward more reliable and efficient long-horizon terminal agents. The code is publicly available at https://github.com/multimodal-art-projection/TACO.

## 2604.20779v1 — SWE-chat: Coding Agent Interactions From Real Users in the Wild

- URL: https://arxiv.org/abs/2604.20779v1
- Primary category: `cs.AI`
- Published: 2026-04-22T17:08:19Z

### Abstract

AI coding agents are being adopted at scale, yet we lack empirical evidence on how people actually use them and how much of their output is useful in practice. We present SWE-chat, the first large-scale dataset of real coding agent sessions collected from open-source developers in the wild. The dataset currently contains 6,000 sessions, comprising more than 63,000 user prompts and 355,000 agent tool calls. SWE-chat is a living dataset; our collection pipeline automatically and continually discovers and processes sessions from public repositories. Leveraging SWE-chat, we provide an initial empirical characterization of real-world coding agent usage and failure modes. We find that coding patterns are bimodal: in 41% of sessions, agents author virtually all committed code ("vibe coding"), while in 23%, humans write all code themselves. Despite rapidly improving capabilities, coding agents remain inefficient in natural settings. Just 44% of all agent-produced code survives into user commits, and agent-written code introduces more security vulnerabilities than code authored by humans. Furthermore, users push back against agent outputs -- through corrections, failure reports, and interruptions -- in 44% of all turns. By capturing complete interaction traces with human vs. agent code authorship attribution, SWE-chat provides an empirical foundation for moving beyond curated benchmarks towards an evidence-based understanding of how AI agents perform in real developer workflows.

## 2604.21003v2 — The Last Harness You'll Ever Build

- URL: https://arxiv.org/abs/2604.21003v2
- Primary category: `cs.AI`
- Published: 2026-04-22T18:51:48Z

### Abstract

AI agents are increasingly deployed on complex, domain-specific workflows -- navigating enterprise web applications that require dozens of clicks and form fills, orchestrating multi-step research pipelines that span search, extraction, and synthesis, automating code review across unfamiliar repositories, and handling customer escalations that demand nuanced domain knowledge. \textbf{Each new task domain requires painstaking, expert-driven harness engineering}: designing the prompts, tools, orchestration logic, and evaluation criteria that make a foundation model effective. We present a two-level framework that automates this process. At the first level, the \textbf{Harness Evolution Loop} optimizes a worker agent's harness $\mathcal{H}$ for a single task: a Worker Agent $W_{\mathcal{H}}$ executes the task, an Evaluator Agent $V$ adversarially diagnoses failures and scores performance, and an Evolution Agent $E$ modifies the harness based on the full history of prior attempts. At the second level, the \textbf{Meta-Evolution Loop} optimizes the evolution blueprint $Λ= (W_{\mathcal{H}}, \mathcal{H}^{(0)}, V, E)$ itself across diverse tasks, \textbf{learning a blueprint $Λ^{(\text{best})}$ that enables rapid harness convergence on any new task -- so that adapting an agent to a novel domain requires no human harness engineering at all.} We formalize the correspondence to meta-learning and present both algorithms. The framework \textbf{shifts manual harness engineering into automated harness engineering}, and takes one step further -- \textbf{automating the design of the automation itself}.

