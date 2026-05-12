# Pre-Writing Protocol

## Purpose

Phase 1 exists to prevent encyclopedic drift and template writing. The output is not a polite checklist; it is a working contract for the article.

## Default Interaction Depth

Use the "Anchor Sheet first" pattern:

1. Infer a first-pass Anchor Sheet from the user's request.
2. Run targeted research only where current or factual anchors matter.
3. Present the Anchor Sheet with strengths and weak spots.
4. Ask for confirmation or correction.
5. Do at most one focused follow-up round unless the user requests deeper collaboration.

Avoid long interrogations. Prefer giving the user something concrete to edit.

## Anchor Sheet Template

Use this shape in Phase 1:

```markdown
## Anchor Sheet

**中心论点**
- 候选 A:
- 候选 B:
- 推荐:

**技术锚点**
- 已有锚点:
- 需要补强:
- 可能来源:

**读者画像**
- 目标读者:
- 已知前提:
- 常见误解:

**范围边界**
- 范围内:
- 明确不写:

**视觉说明计划**
- 图 1:
- 图 2:

**叙事策略**
- 推荐策略:
- 为什么:
- 风险:

**薄弱环节**
- 问题:
- 选项: 用户补充 / 定向调研 / 收窄范围
```

Do not present three empty thesis candidates. If the request is underspecified, propose plausible candidates and label assumptions.

## Central Thesis Rules

A valid thesis is:

- falsifiable: a knowledgeable reader could disagree and test it;
- specific: tied to a version, system shape, workload, or failure mode when relevant;
- useful: changes how the reader would design, debug, or choose technology;
- early: can appear in the opening paragraph without a long preamble.

Weak thesis examples:

- "Redis distributed locks are important in modern systems."
- "Kafka and RocketMQ each have advantages and disadvantages."
- "Spring AI is a powerful framework."

Stronger thesis examples:

- "Redis 分布式锁只有在锁的语义被限定为互斥提示而非事务边界时才可靠；一旦把它当作强一致保护，续租、GC pause 和主从切换会同时暴露风险。"
- "订单系统选 Kafka 还是 RocketMQ，不应从吞吐量开始比较，而应从业务消息语义开始；当事务消息和延迟消息是主路径时，RocketMQ 的工程约束更少。"

## Technical Anchor Rules

Prefer anchors in this order:

1. Primary sources: official docs, release notes, RFCs, design docs, source code, official benchmark methodology.
2. Reproducible facts: code snippets, config defaults, error paths, latency/throughput measurements with context.
3. Production facts: incident details, known failure modes, operational thresholds, rejected alternatives.
4. Secondary sources: high-quality engineering blogs, issue discussions, conference talks.

Avoid unsupported anchors:

- "high performance", "scalable", "flexible";
- benchmark numbers without hardware, workload, version, or method;
- vague failure language such as "may fail under high load";
- invented production details.

## Research Triggers

Research is mandatory when:

- the article discusses a library, SDK, framework, cloud service, API, or version-specific behavior;
- facts may have changed recently;
- the thesis depends on benchmark numbers, defaults, release behavior, or issue history;
- the user asks for references or citations.

Use Context7 MCP for library/API documentation when available. Use web search/fetch for official docs, release notes, issue discussions, benchmark reports, and primary source material. Prefer primary sources over summaries.

## Confirmation Gate

After presenting the Anchor Sheet, ask exactly:

> 以上是本文的写作蓝图，是否可以开始撰写？

Do not draft until the user confirms. Confirmation can be explicit ("可以", "按这个写", "开始") or a correction plus approval ("把读者改成 SRE，然后开始写").

If the user rejects part of the sheet, revise only the affected dimensions and ask again.
