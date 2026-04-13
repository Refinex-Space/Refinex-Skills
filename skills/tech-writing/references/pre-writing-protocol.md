# Pre-writing protocol

The single most important part of this skill. Every piece starts here. If this protocol is skipped, the rest of the skill cannot save the draft.

The protocol produces an **Anchor Sheet** — a short internal document that contains the argument, the anchors, the reader model, the scope, and the chosen voice. The Anchor Sheet exists on paper (or in the chat) *before any prose is drafted*. Show it to the user before drafting so they can catch a weak argument or a missing anchor while it is still cheap to fix.

## The six steps

### 1. Central argument

Write **one sentence**. It must be:

- **Falsifiable.** A reader who disagreed with you should be able to point to specific evidence that would settle the disagreement.
- **Defensible.** You can name the evidence right now, from your anchors.
- **Sharper than the topic.** A topic is "let's talk about X". An argument is "X is Y, because Z, and the usual objection W is wrong for reason V".

Examples of non-arguments (reject these):

- "Spring AI is a powerful framework for building AI applications." (Empty. Not falsifiable. Says nothing.)
- "We will explore the tradeoffs of microservices vs monolith." (Topic, not argument. Commits to nothing.)
- "This post introduces our new caching layer." (Announcement, not argument. Gives the reader no reason to read on.)

Examples of real arguments (accept these):

- "Spring AI 的 `ChatClient` 在同步 chat 场景下是一个干净的抽象,但一旦进入 streaming + tool-call,`AdvisorChain` 的 `around` 语义就会暴露:它假设 advisor 是纯函数式的,而 tool-call 本质上是有状态的。这解释了我们生产环境里四种典型 bug 的根因。"
- "Our decision to move from PostgreSQL to CockroachDB for the ledger service was wrong. We underestimated two costs: the per-transaction latency hit at our p99 (12ms → 47ms), and the operational cost of rebuilding our observability stack for a distributed DB. Here is what we learned, and the conditions under which CockroachDB would actually be the right call."
- "Virtual threads do not replace reactive programming for I/O-bound services. They solve the thread-per-request cost problem, which is real, but they do not solve the backpressure problem, and any code that assumed reactive backpressure will break silently when ported."

Notice what all three have in common: a specific claim, a reason, and an implicit "and here is what you are probably wrong about". That is an argument.

**If you cannot write this sentence, stop.** Ask the user what they actually want to claim. Do not proceed to step 2 with a vague argument — it will poison every downstream step.

### 2. Technical anchors

At least one of each of these, preferably more:

**Real numbers.** "Fast" is not a number. "2.1ms p99, measured on 8-core ARM, JDK 21, with 200 RPS synthetic load" is a number. A rough target: at least three concrete numbers per 1000 words of final prose. Pieces that have no numbers are fine *only if* they are pure design or opinion pieces, and even then they usually benefit from at least one quantitative anchor.

Acceptable numeric anchors: latency (with percentile), throughput, memory (with heap/off-heap distinction), CPU, version numbers, error rates, code sizes (LOC, binary size), config defaults, cost ($/month, $/GB), thresholds, commit counts, file counts, record counts.

Unacceptable: "significant", "a lot", "much faster", "dramatically improved", "high performance", "scalable".

**Specific failure mechanisms.** A failure mechanism is a *causal chain*, not a category. Compare:

- Weak: "The cache can run out of memory under load."
- Strong: "`Caffeine` with `maximumSize(10_000)` plus our 4KB average value size sets an upper bound of ~40MB. But we pin large training prompts (up to 800KB each) in the same cache. Twelve concurrent pinned prompts push the cache past 10MB and trigger eviction of hot small entries. The hit rate collapses from 94% to 31%, and the downstream OpenAI latency budget blows out because every miss is a 2s+ call."

The strong version is a causal chain: config → data shape → concurrency → eviction behavior → observable symptom. You could *draw* it. That is the test.

**Rejected alternatives with reasons.** For any design decision in the piece, list at least two alternatives you considered and rejected, and for each one, the *specific* reason. "Too slow" is not a reason. "Too slow *because the cold-start path dominates our p99, and Option B's JIT warm-up is 4× ours*" is a reason.

For ADRs, design docs, and comparisons this is mandatory. For blog posts it is strongly recommended — it is the fastest way to prove to the reader that you have thought about the problem.

**Boundary conditions with thresholds.** Every strong technical claim has a boundary beyond which it stops being true. Finding the boundary and stating it explicitly is how you earn the reader's trust. "This works up to ~10k rows per partition; past that, Cassandra's tombstone scan costs overtake the read path, and you want a different data model." That one sentence is worth more than three paragraphs of hedging.

### 3. Visual explanation plan

Before drafting, ask whether the reader will have to simulate too many moving parts in their head. If the answer is yes, plan the diagram now instead of hoping to notice it later.

The key move is to write the **reader question** first and choose the Mermaid type from that question:

- "Who calls whom, and in what order?" → `sequenceDiagram`
- "Where does the pipeline branch or loop?" → `flowchart`
- "What state transitions are legal?" → `stateDiagram-v2`
- "How do these components or types relate statically?" → `classDiagram`
- "How do these entities relate in storage?" → `erDiagram`
- "What changed across releases or over incident time?" → `timeline`

Use `references/diagram-selection-guide.md` when the choice is not obvious. Do not default to `flowchart` out of habit. Flowcharts are for branching flow, not for every technical problem.

The visual plan is part of the Anchor Sheet, not a decoration added during editing. For each planned diagram, record:

1. The question the diagram answers.
2. The Mermaid type.
3. The specific claim the reader should understand after seeing it.

If prose can do the job more clearly, skip the diagram. If prose cannot, make the diagram mandatory before drafting starts.

### 4. Reader audit

Answer three questions in writing:

1. **Who is the reader?** Be specific. "Java backend engineer, 3+ years, familiar with Spring Boot, never used Spring AI." Not: "developers interested in AI".
2. **What do they already know?** List it. You will use this list to cut paragraphs that re-explain things the reader already knows. A Spring Boot engineer does not need a paragraph on what a bean is.
3. **What do they probably *mis*know?** This is the most valuable of the three. These are the misconceptions you get to correct — and correcting a misconception is almost always more useful than introducing a new concept. If your piece does not correct any misconception, ask whether it is teaching anything at all.

If the reader audit describes two very different readers ("beginners and experts"), you have two pieces, not one. Pick one and write it. The "accessible to both" piece is a myth; it always turns into a piece that bores the experts and confuses the beginners.

### 5. Scope boundary

Two lists.

**In scope.** What you will cover. Keep it tight. A blog post should cover one central thing. A design doc can cover one system. An ADR covers exactly one decision.

**Explicitly out of scope.** This is the load-bearing list. Every item here is something a reader might expect you to cover but you are choosing not to — and you are saying so upfront so the reader doesn't feel cheated when it doesn't appear. Example:

> Out of scope: benchmarks against LangChain (different language, different runtime; comparing them fairly would require a separate piece); deployment on Kubernetes (we run on ECS; a Kubernetes guide would need its own operational anchors); fine-tuning (`ChatClient` is purely an inference-side abstraction).

Writing out-of-scope lists well is a senior skill. It is how you turn "I ran out of time" into "I made a deliberate choice about what this piece is".

### 6. Voice selection

Pick exactly one voice from `narrative-voices.md` and name it in the Anchor Sheet. Do not leave this implicit. Naming it up front is what lets you catch drift later. If during drafting you find yourself writing in a different voice, you have two choices: revert, or scrap the draft and restart in the new voice. You do not get to blend.

## The Anchor Sheet — template

Use this as a working document at the top of every piece. Keep it short; a full page is usually too much.

```
# Anchor Sheet: <working title>

## Central argument (1 sentence, falsifiable)
<...>

## Anchors
- Numbers:
  - <metric>: <value> (<context: hardware, load, version>)
  - ...
- Failure mechanisms:
  - <causal chain>
  - ...
- Rejected alternatives:
  - <option>: rejected because <specific reason>
  - ...
- Boundaries:
  - <condition under which claim stops holding>

## Reader
- Who: <...>
- Knows already: <...>
- Misknows: <...>

## Visual explanation plan
- Diagram: <question the diagram answers>
  - Type: <sequenceDiagram | flowchart | stateDiagram-v2 | classDiagram | erDiagram | timeline | none>
  - Why this type: <...>
  - Reader payoff: <what becomes predictable after seeing it>

## Scope
- In: <...>
- Out: <...>

## Voice
<one of: Production War Story | Design Tribunal | Mechanism Autopsy |
         Migration Field Guide | Benchmarker's Notebook | Reference Librarian>

## Document type
<one of: blog post | ADR | design doc | comparison | deep-dive | API doc | migration guide>
```

## Worked example — a Spring AI deep-dive

```
# Anchor Sheet: Spring AI ChatClient 在流式 tool-call 下的四种裂缝

## Central argument
Spring AI 的 ChatClient 在同步 chat 下是干净的抽象,但一旦进入 streaming +
tool-call,AdvisorChain 的 around 语义就会暴露:它假设 advisor 是纯函数式
的,而 tool-call 本质上是有状态的。这解释了四种生产 bug 的根因。

## Anchors
- Numbers:
  - Spring AI 1.0.0-M6, spring-ai-openai 1.0.0-M6
  - 复现 bug 的最小 heap:~200MB
  - 流式 tool-call 下 AdvisorChain 的 around 调用次数:1 次(应为 N 次,N=tool-call 轮数)
- Failure mechanisms:
  - Bug 1: Logging advisor 只记录第一轮 tool-call 的 prompt,后续全部丢失
    — 因为 AdvisorChain.nextAroundStream() 只 hold 一次 Flux,tool-call
    触发的 re-invoke 没走 chain
  - Bug 2: Token counting advisor 计数为 0 —— 同上,re-invoke 路径绕过
  - Bug 3: 自定义 retry advisor 在 tool-call 失败后不重试 —— 因为 retry
    逻辑挂在 around,但 tool-call 的重入走的是 StreamingChatModel 内部循环
  - Bug 4: 最致命 —— context propagation(MDC / TraceId)在 tool-call
    第 2 轮开始丢失
- Rejected alternatives:
  - "改用同步 API 绕开": 失去 streaming UX,产品不接受
  - "直接用 OpenAI SDK": 失去 Spring AI 的 prompt template + output parser,
    项目已有 40+ 处使用,迁移代价 > 修 bug
  - "写自定义 ChatModel 绕过 ChatClient": 等于放弃整个 advisor 生态
- Boundaries:
  - 这个问题仅在 streaming + tool-call *同时* 出现时触发
  - 纯同步 chat + tool-call: AdvisorChain 工作正常
  - streaming 无 tool-call: AdvisorChain 工作正常
  - Spring AI 1.0.0-RC1 修复了 Bug 1 和 Bug 2;Bug 3 和 Bug 4 截至写作时仍存在

## Reader
- Who: 用 Spring Boot 3 + Spring AI 做生产 LLM 集成的 Java 后端工程师
- Knows already: Spring Boot, bean lifecycle, Reactor Flux 基础
- Misknows:
  - 以为 AdvisorChain 像 Servlet Filter 一样每个请求跑一次 —— 错,
    在 tool-call 场景下它只跑一次
  - 以为 streaming 是 ChatClient 层的抽象 —— 错,真正的 streaming 循环
    在 ChatModel 实现类里
  - 以为 spring-ai-openai 的 tool-call 是基于 function_call 协议 —— 错,
    M5 开始已经切到 tools 协议,命名仍保留 function 是历史原因

## Visual explanation plan
- Diagram: `ChatClient.call()` 到 tool-call re-entry 的完整调用顺序到底是怎样的?
  - Type: sequenceDiagram
  - Why this type: 这里的难点是时间顺序和跨组件 re-entry,不是静态结构
  - Reader payoff: 读者看完后能准确指出 `AdvisorChain.around()` 被调用的时点,
    以及为什么后续 tool-call 轮次绕过了它
- Diagram: 哪些场景会触发 bug,哪些不会?
  - Type: flowchart
  - Why this type: 这里的核心是 branching 条件,即 sync / streaming /
    tool-call 的组合空间
  - Reader payoff: 读者看完后能快速判断自己的调用路径是否落在 bug
    触发区间

## Scope
- In: AdvisorChain 的 around 语义 + 四个 bug 的源码级根因 + 可用的 workaround
- Out:
  - Spring AI 的 vector store / RAG(是独立话题)
  - 其他 provider(Anthropic / Ollama)的 tool-call 实现(结论可能不同,
    需要单独验证)
  - Spring AI 1.0.0-RC2 之后的修复状态(文章以 M6 为基准,RC1 的修复点会提到)

## Voice
Mechanism Autopsy

## Document type
deep-dive
```

That Anchor Sheet is about 40 lines. The resulting piece would be a strong 2000–3000 word deep-dive with real source references. Notice that *almost every sentence in the final piece is already implied by the Anchor Sheet*. That is the sign of a strong Anchor Sheet: the drafting phase becomes mechanical.

## What a thin Anchor Sheet looks like (and what to do)

A thin Anchor Sheet has any of these smells:

- Argument is actually a topic ("探讨 Spring AI 的设计").
- Anchors are adjectives ("fast", "robust").
- Rejected alternatives section is empty or says "none considered".
- Mechanism-heavy piece has no visual plan, even though the reader would have to hold multiple actors, states, or branches in working memory.
- Reader audit is "developers".
- "Out of scope" is empty.
- Voice is unclear.

When you see a thin Anchor Sheet, **do not proceed to drafting**. Instead, tell the user which specific anchors are missing, and offer concrete ways to fill them in. Examples:

- "I don't have real numbers for the p99 latency claim. Can you share the measurement, or should I use tools to look up published benchmarks?"
- "You've named CockroachDB as the chosen solution but haven't said what you rejected. The piece will be weak without at least two rejected alternatives — what else did you consider?"
- "The reader is ambiguous — this will either be aimed at engineers evaluating Spring AI for the first time or at engineers already using it in production. Which one? They need different pieces."

Asking these questions is the work of the skill. It is not a detour from the writing; it *is* the writing.
