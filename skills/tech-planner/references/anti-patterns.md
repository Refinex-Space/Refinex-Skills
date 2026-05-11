# Anti-Patterns — Detailed Examples and Boundary Cases

## Purpose

This document provides detailed positive/negative comparisons for each anti-pattern. Consult this when facing a boundary case — when it is unclear whether a particular choice constitutes an anti-pattern violation.

---

## 1. Documentation Mirroring

### What It Looks Like

Suppose the Spring AI official documentation has these chapters: Getting Started, Chat Models, Prompts, Embeddings, Vector Stores, Retrieval Augmented Generation, Function Calling.

**Mirroring (BAD)**:
1. Spring AI 入门与环境搭建
2. Chat Models 的配置与使用
3. Prompt 模板系统详解
4. Embedding 模型与文本向量化
5. Vector Store 集成指南
6. RAG 实现方案
7. Function Calling 机制

This sequence copies the documentation structure. Each article maps to a chapter. There is no reordering, no merging, no opinion.

**Cognitive Restructuring (GOOD)**:
1. Spring AI 的分层抽象设计与请求管道的实际装配过程
2. ChatClient 与 ChatModel 的职责分离及其对可测试性的影响
3. Prompt 模板中的变量解析时序与类型安全边界
4. 从文本到向量：Embedding 维度选择对检索精度的量化影响
5. RAG 管道中的五个可干预点与调优策略
6. Function Calling 的序列化约束与异常传播路径

The restructured sequence merges Getting Started into the first article's context, reorders based on dependency (ChatClient before Prompts because understanding the client's builder pattern is prerequisite), and gives each article an opinion.

### Boundary Case: Partial Overlap

If 3 out of 7 articles happen to cover the same topics as documentation chapters but in a different order and with distinct theses, that is acceptable. The test is whether the series *structure* (ordering, grouping, framing) shows independent cognitive design, not whether individual topics happen to match.

---

## 2. Topic-Tag Titling

### The Spectrum

Topic-tag titles and sensationalist titles are two ends of a bad spectrum. The target is the precise middle.

**Topic-Tag (BAD)**:
- "Spring AI 简介"
- "Redis 数据结构"
- "Kubernetes 网络模型"

These are labels, not claims. They tell the reader what area the article is in, but not what it argues or what value it delivers.

**Sensationalist / Clickbait (EQUALLY BAD)**:
- "揭秘 Spring AI 的三大致命陷阱"
- "Redis 数据结构的颠覆认知用法"
- "一文读懂 Kubernetes 网络模型的全部秘密"
- "Spring AI 的分层抽象隐藏了三个你第一次调用 ChatClient 时会后悔的决定"

These use emotional manipulation, false urgency, or dramatic framing. They are characteristic of social media marketing, not technical writing.

**Editorial Precision (GOOD)**:
- "Spring AI 请求管道的装配过程与可干预点"
- "Redis Sorted Set 在排行榜与延迟队列中的复用模式"
- "Kubernetes Service 的四种类型及其流量路径差异"
- "领域驱动设计在互联网业务开发中的实践"
- "可验证过程奖励在提升大模型推理效率中的探索与实践"

These titles precisely describe what the article covers and what value the reader gets. They are informative without being manipulative.

### The Test

Read the title and ask: "Do I know exactly what this article will teach me?" If yes, and the title does not use emotional manipulation, it passes. If no (too vague) or if it uses dramatic framing (too sensational), it fails.

---

## 3. Phase-as-Difficulty-Label

### The Problem

"基础篇 / 进阶篇 / 高级篇" describes the reader's assumed experience level but says nothing about what they will *do* cognitively during that phase. Two series on different topics could both have phases named "基础篇 / 进阶篇 / 高级篇" and the names would tell you nothing about how the series differ.

**Difficulty Labels (BAD)**:
- Phase 1: 基础篇 — Spring AI 的基本概念和简单使用
- Phase 2: 进阶篇 — 深入理解 Spring AI 的核心机制
- Phase 3: 高级篇 — 生产级 Spring AI 应用开发

**Cognitive-Action Names (GOOD)**:
- Phase 1: 认知重建 — 卸载 LangChain 的心智模型，理解 Spring AI 的设计意图
- Phase 2: 机制掌握 — 请求管道的实际装配过程与可干预点
- Phase 3: 承重决策 — 无法轻易回滚的架构选择与权衡分析

### Boundary Case: "Foundations" Phrasing

"概念基础" as a phase name is borderline. If the subtitle makes the cognitive activity concrete (e.g., "概念基础 — 建立请求-响应-模型三层心智模型"), it can pass. But "概念基础 — 学习基本概念" fails because the subtitle adds nothing.

When in doubt, prefer a name that would be meaningless if applied to a different technology. "认知重建" for Spring AI is specific because it implies there is something to *un*learn. "基础篇" could apply to anything.

---

## 4. Prerequisite Amnesia

### Detection Method

Walk through the series in order. Maintain a running set of "concepts introduced so far." For each article, check whether every concept it references is either in the running set or declared as a series-level prerequisite.

**Amnesia (BAD)**:
- Article 3 discusses "Advisor chain 的拦截顺序" but the Advisor concept was never formally introduced — it was only mentioned in passing in Article 1's code example.
- Article 5 explains "向量检索的 top-k 召回" but Article 4 (which covers Vector Stores) did not explain similarity metrics or the concept of k-nearest-neighbor search.

**Proper Dependency Management (GOOD)**:
- Article 2 formally introduces the Advisor concept, its role, and its interface. Article 3 declares "依赖第 2 篇中的 Advisor 概念" and proceeds directly to chaining behavior.
- Article 4 introduces similarity metrics and k-NN as part of its Vector Store coverage. Article 5 declares the dependency and builds on it.

### Boundary Case: Common Knowledge

Concepts that are genuinely common knowledge for the declared target audience (e.g., "HTTP request" for a series targeting backend developers) do not need explicit introduction. The judgment call is: would the series' declared target reader already know this concept? If uncertain, err on the side of declaring it as a series-level prerequisite.

---

## 5. Pseudo-Spiral

### The Distinction

**Loop (BAD)**: Article 2 introduces ChatClient basics. Article 6 "revisits" ChatClient but only shows another usage example at the same complexity level. The reader does not ascend.

**True Spiral (GOOD)**: Article 2 introduces ChatClient at the API usage level (how to build a request, send it, parse the response). Article 6 revisits ChatClient at the mechanism level (how the Advisor chain transforms the request before it reaches the model, how streaming responses are assembled from SSE events). The new complexity layer (internal mechanism) is explicitly marked as the spiral dimension.

### The Test

For each revisit, ask: "If I removed the first visit, would this article still make sense at the same depth?" If yes, the revisit is adding genuine new complexity. If the later article would be *easier* without the first visit (because it repeats the same ground), that's a pseudo-spiral.

### Common Spiral Dimensions

When revisiting a concept, the new complexity should come from one of these dimensions:
- **Depth escalation**: API usage → internal mechanism → source code implementation
- **Failure modes**: Happy path → edge cases → production failure scenarios
- **Scale implications**: Single instance → distributed → high-throughput
- **Composition**: Concept in isolation → concept composed with others → emergent behaviors from composition
- **Trade-off visibility**: "How it works" → "Why it was designed this way" → "What was sacrificed for this design"