# Phase Naming Guide

## Purpose

Guide the naming of series phases so that each name describes a cognitive activity the reader performs, not a difficulty label.

---

## The Rule

A phase name must answer: "What is the reader *doing* cognitively during this phase?" The name should be a verb-noun phrase or a metaphorical label that immediately communicates the type of intellectual work involved.

**Forbidden patterns**: 基础篇, 进阶篇, 高级篇, 入门, Beginner, Intermediate, Advanced, Fundamentals, Deep Dive. These describe the reader's assumed experience level, not their cognitive activity.

---

## Naming Structure

Each phase has two components:

1. **Cognitive-action name** (2-6 Chinese characters or equivalent English): A compact label for the phase.
2. **Subtitle** (one sentence): Expands the name into a concrete description of what the reader is doing.

Format: `Phase N: {认知动作名} — {副标题}`

---

## Example Names (Positive)

These are illustrative, not prescriptive. Every series needs its own phase names tailored to the subject matter.

**For a Spring AI series:**
- Phase 1: 认知重建 — 卸载 LangChain 的心智模型，理解 Spring AI 的分层抽象设计意图
- Phase 2: 机制掌握 — 请求管道的实际装配过程与可干预点
- Phase 3: 承重决策 — 无法轻易回滚的架构选择与权衡分析

**For a Redis applied patterns series:**
- Phase 1: 结构直觉 — 从数据结构特性推导适用场景
- Phase 2: 工程组装 — 用基础结构组合解决复合业务问题
- Phase 3: 故障预判 — 识别和防御生产环境中的退化模式

**For a Kubernetes networking series:**
- Phase 1: 模型校准 — 重新理解 Pod 网络的扁平地址空间
- Phase 2: 链路追踪 — 一个请求从 Ingress 到 Pod 的完整旅程
- Phase 3: 策略编织 — NetworkPolicy 的组合语义与安全边界设计

---

## Naming Process

1. Look at the articles assigned to each phase.
2. Ask: "What single cognitive verb captures what all these articles require the reader to do?" Common cognitive verbs: 重建 (reconstruct), 掌握 (master), 组装 (assemble), 校准 (calibrate), 拆解 (deconstruct), 预判 (anticipate), 编织 (weave), 迁移 (migrate), 抉择 (decide).
3. Pair the verb with a noun that grounds it in the subject matter.
4. Write the subtitle to make the cognitive activity concrete and specific.

---

## Capability Statement

Each phase also requires a capability statement: a sentence describing what the reader can *do* after completing this phase that they could not do before.

Format: "完成本阶段后，读者能够 {具体能力描述}。"

**Good**: "完成本阶段后，读者能够阅读 Spring AI 的 auto-configuration 源码并预测给定配置下哪些 Bean 会被注册。"

**Bad**: "完成本阶段后，读者对 Spring AI 有了更深入的了解。" (Unfalsifiable and vague.)

The capability statement must be concrete enough that a reader could verify whether they've achieved it.