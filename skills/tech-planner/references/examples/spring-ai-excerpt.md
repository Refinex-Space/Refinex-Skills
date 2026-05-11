# Example Output Excerpt — Spring AI Series (2 Articles)

## Purpose

This file demonstrates what a completed tech-planner output looks like. It shows the series header, one phase header, and two fully specified articles with complete tech-writing prompts. This is a reference for format and quality — not a prescriptive content template.

---

## Series Header (Excerpt)

**主题**: Spring AI 的分层抽象设计与工程实践
**版本**: Spring AI 1.0 GA (基于 Spring Boot 3.3+)
**总范围**: 覆盖 Spring AI 的核心抽象层设计、请求管道机制、模型集成策略、RAG 管道构建、Function Calling 机制及生产环境部署考量。不覆盖具体模型的训练与微调、LangChain/LlamaIndex 等非 Spring 生态框架的对比评测、前端集成方案。
**目标读者**: 有 1-2 年 Spring Boot 开发经验的后端工程师，熟悉 Spring 的依赖注入和自动配置机制，但对 LLM 应用开发没有系统经验。可能接触过 LangChain 或 OpenAI API 的简单调用，但未深入理解框架抽象层设计。
**预估文章总数**: 8 篇，分 3 个阶段
**阶段划分**:
- Phase 1: 认知重建（第 1-3 篇）— 模式: 心智模型重建
- Phase 2: 机制掌握（第 4-6 篇）— 模式: 洋葱模式
- Phase 3: 承重决策（第 7-8 篇）— 模式: 决策树模式

---

## Phase 1: 认知重建 — 卸载直接调用 API 的心智模型，理解 Spring AI 为何要在 HTTP 客户端之上再建三层抽象

**架构模式**: 心智模型重建

**能力声明**: 完成本阶段后，读者能够解释 Spring AI 的 Model → Client → Advisor 三层抽象各自的职责边界，能够预测在给定配置下 auto-configuration 会注册哪些 Bean，并能识别"直接用 RestTemplate 调 OpenAI API"这一做法在可测试性、可移植性和可观测性三个维度上的具体代价。

---

### Article 1

**编号**: 第 1 篇 / 共 8 篇
**标题**: Spring AI 的三层抽象设计及其对可移植性与可测试性的影响

**中心论点**: Spring AI 在 HTTP 客户端之上构建 Model、Client、Advisor 三层抽象，其核心收益不是简化 API 调用（实际上代码量可能更多），而是将模型供应商绑定、提示工程逻辑和横切关注点分别隔离到不同层次，使得每一层可以独立测试和替换。

**关键技术锚点**:
- ChatModel 与 ChatClient 的接口定义差异 — 需要: 源码分析
- auto-configuration 注册 Bean 的条件判断链 — 需要: 源码分析 + 边界条件测试
- 使用 MockChatModel 进行单元测试 vs 直接 Mock HTTP 的代码量对比 — 需要: 代码示例对比

**前序依赖**: 无前序依赖——本文是系列入口点。

**视觉说明计划**:
- 图表 1: Model → Client → Advisor 三层抽象的职责边界与数据流 — 推荐类型: flowchart
- 图表 2: auto-configuration 的 Bean 注册决策树 — 推荐类型: flowchart

**tech-writing Prompt**:

```markdown
# Tech-Writing Prompt

## 系列上下文 [REQUIRED]
- **系列名称**: Spring AI 的分层抽象设计与工程实践
- **当前位置**: 第 1 篇 / 共 8 篇
- **系列总目标读者**: 有 1-2 年 Spring Boot 开发经验的后端工程师，熟悉依赖注入和自动配置，对 LLM 应用开发无系统经验

## 文章标题 [REQUIRED]
Spring AI 的三层抽象设计及其对可移植性与可测试性的影响

## 中心论点 [REQUIRED]
Spring AI 在 HTTP 客户端之上构建 Model、Client、Advisor 三层抽象，其核心收益不是简化 API 调用（实际上代码量可能更多），而是将模型供应商绑定、提示工程逻辑和横切关注点分别隔离到不同层次，使得每一层可以独立测试和替换。

## 目标读者状态 [REQUIRED]
- **读者此刻知道什么**: Spring Boot 的依赖注入机制、@Configuration 和 @Bean 的工作方式、@ConditionalOn* 注解的基本含义、可能使用过 RestTemplate 或 WebClient 调用过 OpenAI API
- **读者此刻不知道什么**: Spring AI 的分层抽象设计意图、ChatModel 与 ChatClient 的职责分离、Advisor 链的存在和作用、Spring AI auto-configuration 的 Bean 注册条件
- **读者可能持有的误解**: "Spring AI 就是对 OpenAI API 的 Java 封装"、"框架抽象层只是增加了不必要的复杂度"、"我用 RestTemplate 直接调 API 也能实现同样功能"

## 关键技术锚点 [REQUIRED]
- 锚点 1: ChatModel 接口与 ChatClient 接口的方法签名和职责差异 — 需要: 源码分析（展示两个接口的实际定义，分析为何要分成两层）
- 锚点 2: OpenAiAutoConfiguration 中的 @ConditionalOnProperty 和 @ConditionalOnMissingBean 判断链 — 需要: 源码分析 + 边界条件测试（展示当缺少 API key 配置时的行为）
- 锚点 3: 使用 MockChatModel 的单元测试 vs Mock HTTP 层的测试代码量和可维护性对比 — 需要: 代码示例对比（两种方式各写一个测试，量化代码行数和断言精度的差异）

## 范围边界 [REQUIRED]
- **本文覆盖**: Spring AI 的三层抽象（Model / Client / Advisor）设计意图与职责边界、auto-configuration 的 Bean 注册机制、三层抽象对可移植性和可测试性的具体影响
- **本文不覆盖**: Advisor 链的详细配置和自定义（第 4 篇处理）、具体模型供应商的配置细节（第 2 篇处理）、Prompt 模板系统（第 3 篇处理）、RAG 和 Function Calling（Phase 2 处理）

## 前序依赖 [REQUIRED]
无前序依赖——本文是系列入口点。

## 视觉说明计划 [REQUIRED]
- 图表 1: Model → Client → Advisor 三层抽象的职责边界与请求数据流向 — 推荐类型: flowchart — 要揭示: 一个用户请求如何依次经过 Advisor 预处理、Client 组装、Model 发送，以及响应的反向路径
- 图表 2: auto-configuration 的 Bean 注册决策树 — 推荐类型: flowchart — 要揭示: 在不同配置条件下（有无 API key、有无自定义 Bean）auto-configuration 的分支行为

## 深度契约 [REQUIRED]
- [x] API 使用层面：教读者正确使用 API，理解参数含义和返回值
- [x] 内部机制层面：解释 API 背后的工作原理，读者能预测边界行为
- [x] 源码实现层面：深入关键源码路径，读者能阅读和调试框架代码
- [ ] 架构决策层面：分析设计权衡，读者能评估该技术是否适合自己的场景

## 写作约束 [REQUIRED]
- **目标字数**: 4000-5500 字
- **代码示例要求**: 关键路径需要。需要 Java 代码，风格为关键片段（不是完整可运行项目，但每个片段需有足够上下文让读者理解其在项目中的位置）。
- **性能数据**: 不需要
- **方案对比**: 需要与"直接使用 RestTemplate/WebClient 调用 OpenAI API"对比

## 常见误解 [CONDITIONAL]
- 误解 1: "Spring AI 只是 OpenAI Java SDK 的 Spring 封装" — 实际情况: Spring AI 的抽象层设计允许在不修改业务代码的情况下切换模型供应商（OpenAI → Ollama → Anthropic），这是单一 SDK 封装做不到的
- 误解 2: "框架抽象层增加了不必要的间接层，降低了性能" — 实际情况: 抽象层的开销在 LLM 调用场景下可以忽略（网络延迟 >> 框架开销），但抽象层带来的可测试性收益在大型项目中非常显著

## 调研指引 [CONDITIONAL]
- Spring AI 官方文档 — Concepts 章节: https://docs.spring.io/spring-ai/reference/
- Spring AI GitHub 仓库 — auto-configuration 模块: 搜索 "spring-ai-autoconfigure" 目录下的 *AutoConfiguration.java 文件
```

---

### Article 2

**编号**: 第 2 篇 / 共 8 篇
**标题**: ChatClient 构建器模式与多模型配置下的 Bean 消歧策略

**中心论点**: ChatClient 的 Builder 注入模式在单模型场景下实现了零配置即用，但在多模型共存场景下（如 GPT-4o 处理复杂推理、GPT-4o-mini 处理简单分类），Spring AI 的 auto-configuration 会因 Bean 类型冲突而失败，开发者必须理解 @Qualifier 和自定义 ChatClientBuilder 工厂的消歧策略。

**关键技术锚点**:
- ChatClient.Builder 的自动注入机制 — 需要: 源码分析
- 多 ChatModel Bean 共存时的冲突错误信息与根因 — 需要: 失败机制演示
- @Qualifier vs 自定义 Builder 工厂两种消歧方案的权衡 — 需要: 被否方案对比

**前序依赖**: 依赖第 1 篇《Spring AI 的三层抽象设计及其对可移植性与可测试性的影响》中的: Model / Client / Advisor 三层职责分离概念、auto-configuration 的 Bean 注册机制 — 可直接引用，无需重新解释

**视觉说明计划**:
- 图表 1: 单模型 vs 多模型场景下的 Bean 注册与注入路径对比 — 推荐类型: flowchart
- 图表 2: ChatClient.Builder 从创建到发送请求的方法调用序列 — 推荐类型: sequence

*(完整的 tech-writing Prompt 此处省略以控制示例长度，实际产出中每篇文章都必须包含完整 Prompt)*

---

## Notes

This example demonstrates: thesis-driven titles in Meituan Tech Blog style, concrete reader state descriptions referencing prior articles by number, technical anchors specifying evidence types, and a complete self-sufficient prompt for the first article. The actual planning output would include all 8 articles with full prompts.