# Test Cases

Use these prompts for forward-testing the skill. The expected behavior is not immediate drafting; the skill should produce and seek confirmation on an Anchor Sheet first.

## Case 1: Tech Planner Handoff

```text
Use $tech-writing to write the article from this tech-planner prompt:

Title: Spring AI ChatClient 的抽象边界
Central thesis: ChatClient 的价值不在于把大模型调用包装成 fluent API，而在于把 prompt assembly、advisor chain、model invocation 和 response mapping 的边界显式化；理解这些边界后，团队才能判断哪些横切逻辑应该进入 Advisor，哪些必须留在业务层。
Target reader: Java 后端工程师，熟悉 Spring Boot 和基本 LLM API 调用，不需要解释 IoC、Bean、REST。
Key anchors: Spring AI 当前版本的 ChatClient/Advisor/ChatModel 调用关系；一次调用链路；Advisor 适合处理的横切逻辑；不适合放入 Advisor 的业务决策；至少一个 sequenceDiagram。
Scope: 写单次 ChatClient 调用的抽象边界，不写 RAG 全流程，不写模型选型。
```

Expected: compressed Anchor Sheet, version ambiguity callout, confirmation gate.

## Case 2: Short User Intent

```text
Use $tech-writing to write a technical blog about Redis distributed locks.
```

Expected: asks for or researches scope, proposes falsifiable thesis candidates, names weak anchors, does not start with generic Redis history.

## Case 3: Technology Comparison

```text
Use $tech-writing to compare RocketMQ and Kafka for order-system message queue selection.
```

Expected: chooses comparison-decision strategy, defines workload assumptions, rejects false balance, asks for confirmation before drafting.
