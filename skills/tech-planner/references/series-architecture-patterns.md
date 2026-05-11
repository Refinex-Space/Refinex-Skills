# Series Architecture Patterns

## Purpose

This document catalogs proven structural patterns for organizing a technical blog series. Select the pattern (or pattern combination) that best matches the topic's nature and the reader's learning journey.

Mixed-mode is supported and often optimal: different phases of a series can use different patterns. When mixing, state the pattern for each phase and explain why the transition occurs.

---

## Pattern Catalog

### 1. Core-Outward (洋葱模式)

**Structure**: Start from the framework's innermost abstraction and peel outward layer by layer toward peripheral features and integrations.

**Best for**: Technologies with a clear layered architecture where understanding the core unlocks everything else. The core is conceptually small but deep.

**Examples**: Spring Boot (IoC Container → Auto-configuration → Starters → Actuator → Deployment), Linux networking stack (socket → TCP/IP → netfilter → iptables → eBPF).

**Cognitive progression**: "What is the kernel of this technology?" → "How does the next layer build on the kernel?" → "How do the outer layers compose?"

**Risk**: Can feel abstract in early articles if the core is too far removed from practical tasks. Mitigate by grounding each layer in a concrete use case immediately after explaining the abstraction.

**Phase transition signal**: When you've exhausted the layered architecture and need to shift to cross-cutting concerns (performance, testing, deployment), consider switching to Problem-Solution Chain or Decision-Tree for the remaining phase.

---

### 2. Problem-Solution Chain (问题驱动模式)

**Structure**: Each article poses a concrete engineering problem. The solution to problem N naturally raises problem N+1.

**Best for**: Practice-oriented topics where the reader's goal is solving real problems, not understanding a framework's internal structure. Also excellent for infrastructure topics (Redis, message queues, monitoring) where use cases are more salient than abstractions.

**Examples**: Redis applied patterns (cache miss storm → distributed locking → message queuing → rate limiting → geospatial queries), production debugging (log aggregation → trace correlation → anomaly detection → root cause analysis).

**Cognitive progression**: "I have this problem" → "This solution works but introduces a new problem" → "The chain of problems reveals the technology's design space."

**Risk**: Can feel disconnected if the chain is artificial — each problem must genuinely emerge from the previous solution, not be arbitrarily sequenced. Test by asking: "Would a developer encounter problem N+1 after solving problem N in real life?"

**Phase transition signal**: When the problem chain reaches a decision point where multiple solutions are valid, consider switching to Decision-Tree for that phase.

---

### 3. Mental Model Reconstruction (心智模型重建模式)

**Structure**: Begin by identifying and dismantling the reader's likely incorrect mental model, then progressively build the correct one.

**Best for**: Technologies where readers arrive with strong but wrong priors from adjacent experience. The "unlearning" is as important as the learning.

**Examples**: Project Reactor ("reactive = async callbacks" → signal-driven model → backpressure → schedulers), Kubernetes ("it's just Docker on multiple machines" → desired state reconciliation → control loops → the API server as the real abstraction).

**Cognitive progression**: "What you think you know is wrong in these specific ways" → "Here is the actual mental model" → "Now apply the correct model to increasingly complex scenarios."

**Risk**: Can feel condescending if the reader doesn't hold the assumed wrong model. Mitigate by framing Phase 1 as "common starting points" rather than "your mistakes." Also, this pattern is front-loaded — the reconstruction must happen in the first 2-3 articles, then the series needs to switch to another pattern for the build-out phase.

**Phase transition signal**: Once the correct mental model is established (typically 2-3 articles), switch to Core-Outward or Problem-Solution Chain to build fluency on top of the corrected model.

---

### 4. Evolutionary Timeline (演进时间线模式)

**Structure**: Follow the technology's historical evolution, with each article explaining one major evolutionary step: what problem motivated it, what was tried, what succeeded, and what it means for today's users.

**Best for**: Technologies with rich version histories where each evolutionary step has teaching value, and where understanding the *why* behind the current design requires knowing the history.

**Examples**: Java concurrency (Thread → Executor → ForkJoinPool → CompletableFuture → Virtual Thread), HTTP protocols (HTTP/1.0 → 1.1 → 2 → 3), CSS layout (floats → flexbox → grid).

**Cognitive progression**: "This was the original design and its limitation" → "This evolution addressed that limitation but introduced new trade-offs" → "The current state of the art reflects accumulated lessons."

**Risk**: Can become a history lesson that readers don't see the practical value of. Every historical step must connect to a *current* practical implication. If a step is only historically interesting, merge it into the next step's introduction rather than giving it a full article.

**Phase transition signal**: When the timeline reaches the present, switch to Problem-Solution Chain or Decision-Tree for practical application.

---

### 5. Decision-Tree (决策树模式)

**Structure**: Each article analyzes one major decision point — presenting the options, the trade-offs, the evaluation criteria, and a recommended path with explicit conditions.

**Best for**: Technologies where the primary challenge is choosing among many valid configurations or architectural approaches. The reader's goal is making informed decisions, not just understanding mechanisms.

**Examples**: Kubernetes deployment strategies (Deployment vs StatefulSet vs DaemonSet, ingress controller selection, storage class choices), Spring Cloud component selection (service discovery: Eureka vs Consul vs Nacos; config: Config Server vs Nacos vs Apollo).

**Cognitive progression**: "Here is a decision you must make" → "Here are the options and what matters for each" → "Here is how to evaluate for your context" → "This decision constrains your next decisions."

**Risk**: Can feel like a comparison blog rather than a teaching series if the analysis is shallow. Each article must go beyond feature matrices into architectural implications and second-order effects.

**Phase transition signal**: When the major decision points are covered, switch to Problem-Solution Chain for integration and production concerns.

---

## Pattern Selection Heuristic

When choosing a pattern, ask these questions in order:

1. **Does the reader likely arrive with a strong but incorrect mental model?** → Start with Mental Model Reconstruction for the first phase.
2. **Does the technology have a clear layered architecture?** → Use Core-Outward as the primary or secondary pattern.
3. **Is the topic more about solving practical problems than understanding internals?** → Use Problem-Solution Chain.
4. **Does the technology's history illuminate its current design in ways that docs don't?** → Use Evolutionary Timeline for the first phase.
5. **Is the primary challenge choosing among alternatives?** → Use Decision-Tree.

If multiple patterns seem equally valid, prefer the one whose cognitive progression best matches the identified entry points and high-fanout nodes in the knowledge graph.

---

## Mixed-Mode Guidelines

When combining patterns across phases:

- State the pattern for each phase explicitly in the series header.
- The transition between patterns should feel natural. The last article of phase N should set up the cognitive shift required by phase N+1's pattern.
- A common effective combination: Mental Model Reconstruction (Phase 1, 2-3 articles) → Core-Outward or Problem-Solution Chain (Phase 2, main body) → Decision-Tree (Phase 3, production readiness).
- Avoid switching patterns mid-phase. A phase should use one pattern consistently.
- Maximum 3 patterns in a single series. More than that creates structural incoherence.