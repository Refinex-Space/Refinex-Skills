# Worked example: Spring AI deep-dive series

This file demonstrates the complete tech-planner workflow applied to a real framework, from the initial research notes through the final deliverable. The example is intentionally concrete — it uses actual Spring AI concepts, actual file paths, and actual design decisions rather than abstract placeholders — because the point is to show what a thorough pass through each phase looks like in practice. A planner following the workflow on a different framework should produce a deliverable of similar depth and shape, adapted to that framework's specifics.

The example is in English for readability in this reference file, but in production the deliverable would be in Chinese with technical terms kept in English, matching the default output language of the skill.

## Phase 1 — Source exhaustion (abbreviated research notes)

A full Phase 1 pass on Spring AI would produce several thousand words of research notes. The abbreviated version below shows the key findings that drive the rest of the example; a real pass would have considerably more detail on each section.

**Framework overview**: Spring AI is a Spring-ecosystem abstraction for LLM-backed applications, released as an incubating project in 2024 and reaching its first milestone releases in 2025. Its core value proposition is consistency with the Spring programming model — beans, dependency injection, configuration properties, auto-configuration — applied to the LLM domain. It positions itself against direct use of provider SDKs (where each provider has a different API surface) and against Python-ecosystem tools like LangChain (which have no Java-native equivalent that integrates cleanly with Spring).

**Core abstractions**: `ChatModel` is the lowest-level abstraction, representing a single LLM provider. `ChatClient` is the fluent facade most users interact with, built on top of `ChatModel`. `Advisor` is the extension point for cross-cutting concerns — logging, retry, memory, RAG, safety checks — and `AdvisorChain` is the mechanism that composes advisors into a pipeline. `Prompt`, `Message`, and the role hierarchy (`SystemMessage`, `UserMessage`, `AssistantMessage`, `ToolResponseMessage`) model the conversation state. `ToolCallback` and the tool schema system model function calling. `EmbeddingModel`, `Document`, and `VectorStore` model retrieval-augmented generation.

**API surface**: `ChatClient` is fluent, with a `.prompt()` entry point that returns a request-specification builder, which terminates in `.call()` or `.stream()` depending on whether the request is synchronous or streaming. The fluent API hides the advisor chain, which is actually the mechanism through which most behavior is customized. The builder-to-advisor translation happens at request construction time.

**Extension points**: The primary extension point is `Advisor`, which comes in two variants — `CallAroundAdvisor` for synchronous requests and `StreamAroundAdvisor` for streaming — both implementing an `around` method that wraps the next stage in the chain. Custom advisors plug in via `ChatClient.builder().defaultAdvisors(...)` or per-request via `.advisors(...)`. Secondary extension points include `ToolCallback` implementations for custom tool wiring, `OutputConverter` for response parsing, and `VectorStore` for retrieval backends.

**Documented limitations**: The docs acknowledge that streaming tool calls are "experimental" in M6 and recommend synchronous mode for production use cases that require tool calls. The docs also note that the `Advisor` interface may evolve before 1.0.0 GA, and that code using `defaultAdvisors` may need to be updated.

**Undocumented limitations (from source code and issue tracker)**: Four significant undocumented issues exist in the M6 timeframe. First, `AdvisorChain.nextAroundStream` returns a `Flux` that is constructed once at the start of the request, which means tool-call re-invocation inside `OpenAiChatModel`'s internal loop does not re-enter the advisor chain. This breaks logging advisors (they see only the first turn), token-counting advisors (they count only the first turn), retry advisors (they do not re-run on tool-call failures), and context-propagation advisors (MDC/TraceId do not survive tool-call turns). Second, the default `MessageChatMemoryAdvisor` stores all messages including large tool responses, causing memory bloat in long conversations. Third, the `JsonOutputConverter` has a silent failure mode when the LLM returns valid JSON inside a Markdown code fence. Fourth, the `FunctionCallback` name, while still present in public API, is deprecated in favor of `ToolCallback`, but the deprecation notice is only in the release notes, not in Javadoc.

**Evolution narrative**: The most notable evolution between M5 and M6 was the rename from `FunctionCallback` to `ToolCallback`, which reflects a design shift from the OpenAI "function calling" terminology to the provider-agnostic "tool" terminology used by Anthropic and later OpenAI versions. The rename was non-breaking — the old name still works but is deprecated. M6 also introduced the current shape of the `Advisor` interface after several iterations in earlier milestones; the interface is stable as of M6 but may still evolve before 1.0.0 GA.

**Common pitfalls**: The top five pitfalls, gathered from the Spring AI GitHub issues and the Spring community forum, are: (1) silently broken advisors under streaming + tool calls, as described above; (2) memory advisor bloat from unchecked tool response storage; (3) prompt template injection when user input is interpolated into templates without escaping; (4) token counting that excludes system prompts because the default advisor only counts user messages; (5) streaming responses that appear to work in development but drop chunks in production when the downstream consumer is slow — a Reactor backpressure issue that Spring AI does not surface clearly.

**Planner's judgments**: Spring AI's core insight is that `ChatClient` is a fluent facade over an advisor pipeline, and understanding the pipeline is the key to extending the framework. The official docs introduce `ChatClient` as a convenient API without emphasizing this — they treat the advisor system as an advanced feature rather than as the central mechanism. A series that frames the advisor pipeline as the core and the fluent API as a facade over the core will teach the framework better than the docs do. This is the series' aha moment.

## Phase 2 — Knowledge graph (abbreviated)

The full knowledge graph for Spring AI would contain roughly twenty-five nodes. The abbreviated version below shows the load-bearing concepts, their prerequisite relationships, their cluster assignments, and the aha-moment flags.

Core concepts and their prerequisites: `ChatModel` has no prerequisite inside Spring AI; it is the foundation node. `ChatClient` depends on understanding `ChatModel` at surface level. `Prompt` and the message-role hierarchy depend on nothing specific to Spring AI; they are background concepts. `Advisor` depends on `ChatClient` and on understanding that `ChatClient` is not the lowest-level API. `AdvisorChain` depends on `Advisor`. The aha-moment concept — "`ChatClient` is a fluent facade over `AdvisorChain`" — depends on both `ChatClient` and `Advisor` being understood at surface level but does not depend on `AdvisorChain`'s internals (which come later).

Tool-calling concepts: `ToolCallback` depends on `ChatClient` and `AdvisorChain`. The tool-call internal loop in `OpenAiChatModel` depends on `ToolCallback` and on `ChatModel`. The specific "streaming + tool call breaks advisor chain" failure mode depends on the tool-call loop and on `AdvisorChain`'s stream semantics.

Retrieval concepts: `EmbeddingModel`, `Document`, and `VectorStore` are a separate cluster with weak dependencies on the core concepts. `QuestionAnswerAdvisor` (the RAG advisor) depends on `Advisor` and on the vector store concepts.

Clusters identified: (1) core invocation (`ChatModel`, `ChatClient`, `Prompt`, messages); (2) advisor system (`Advisor`, `AdvisorChain`, built-in advisors, custom advisors); (3) tool calling (`ToolCallback`, tool-call loop, streaming + tool-call failure); (4) retrieval and memory (`EmbeddingModel`, `VectorStore`, `QuestionAnswerAdvisor`, `MessageChatMemoryAdvisor`); (5) production concerns (backpressure, observability, token counting, memory management).

Aha-moment flags: two aha-moment concepts are identified. The first is "`ChatClient` is a fluent facade over `AdvisorChain`" — this is the primary aha moment, and the article that delivers it should be positioned as early in the series as its prerequisites allow. The second is "Streaming and tool-call combine in a way that breaks the advisor abstraction, and this reveals the hidden assumption that advisors are pure functions" — this is a secondary aha moment, positioned in the middle of the series, that reframes everything the reader learned in earlier articles.

Gaps and silences: the docs do not cover the streaming + tool-call advisor break at all, the docs do not explain why `FunctionCallback` was renamed, the docs do not discuss backpressure in streaming, and the docs do not explain how token counting is supposed to be done for system prompts. Each of these is a gap the series can fill.

## Phase 3 — Series architecture

The architecture is designed from the knowledge graph and uses the spiral pattern with cognitive-state phase names. The pattern choice is justified because Spring AI has a small central concept (the advisor pipeline) that benefits from being revisited at increasing depth, and the target reader (a senior Java backend engineer) has the patience and motivation for a longer series with multiple passes over the same territory. The total series length is thirteen articles across four phases.

**Phase 1 — Rebuilding the LLM Integration Mental Model: Three Articles**

The first phase contains three articles aimed at getting the reader's mental model into shape. The reader arrives with assumptions from adjacent technologies (direct provider SDKs, LangChain, or generic REST client usage) that will get in the way of understanding Spring AI. The phase exists to unseat those assumptions.

Article 1.1 — "Spring AI Is Not a LangChain Port: Four Design Decisions That Make Spring AI a Spring-Native Framework". The article argues that Spring AI was designed from the ground up for the Spring programming model, and that readers who expect it to be a Java version of LangChain will be confused by its shape. The article walks through four specific design decisions: bean-based provider configuration, auto-configuration-driven client construction, the advisor model versus LangChain's chain model, and the absence of LangChain-style "agent" abstractions. Voice: Design Tribunal.

Article 1.2 — "ChatClient Is a Fluent Facade, Not an API: Why Your First Spring AI Call Hides Three Abstraction Layers You Will Regret Ignoring". This is the primary aha-moment article for the series. The argument is that `ChatClient` is a convenient entry point but not where the interesting work happens, and that understanding this up front will save the reader from mistakes later. The article walks through a single `ChatClient.prompt().user(...).call()` call, shows the intermediate builder, shows the request-specification object, shows the advisor chain construction, and shows where the actual HTTP call happens. Voice: Mechanism Autopsy.

Article 1.3 — "The Advisor Contract: What Spring AI Assumes About Your Extension Code (And What That Means When the Assumption Breaks)". This article introduces the `Advisor` interface at the specification level — not its implementation, not custom advisors, just the contract. The argument is that the contract embeds a specific assumption about purity and statelessness, and that this assumption will be load-bearing for everything the reader does later in the series. Voice: Design Tribunal.

**Phase 2 — Mastering the Advisor Pipeline: Four Articles**

The second phase dives into the mechanism that the first phase introduced. Each article covers one aspect of the advisor system at source-code depth.

Article 2.1 — "AdvisorChain Internals: How the Pipeline Is Assembled, Called, and Terminated". This is a Mechanism Autopsy walk through `AdvisorChain.java`, showing how the chain is constructed, how `nextAround` and `nextAroundStream` are implemented, and how the chain terminates when it reaches the `ChatModel`. Voice: Mechanism Autopsy.

Article 2.2 — "The Built-in Advisors: What Spring AI Ships, When to Use Each, and When to Replace Them". This article surveys the stock advisors (`MessageChatMemoryAdvisor`, `QuestionAnswerAdvisor`, `SimpleLoggerAdvisor`) with a Design Tribunal voice, evaluating each one against the criteria the reader now has from Phases 1 and 2. Voice: Design Tribunal.

Article 2.3 — "Writing Your First Custom Advisor: A Token Counter That Actually Counts System Prompts". This article is practical — it walks through building a custom advisor that fixes one of the known gaps in the default behavior (system prompts being excluded from default token counting). The article teaches the advisor-writing pattern through a specific example that also addresses a real pitfall. Voice: mostly Mechanism Autopsy, with a small Production War Story element for the motivating pitfall.

Article 2.4 — "Advisor Ordering, State, and the Difference Between Pre- and Post-Call Work". This article covers the nuances of advisor composition — what happens when advisor A does work before calling the next advisor and advisor B does work after, how to propagate state between advisors, and why some advisor orderings produce surprising results. Voice: Mechanism Autopsy.

**Phase 3 — The Streaming and Tool-Call Revelation: Three Articles**

The third phase is where the secondary aha moment lands. The reader has spent Phase 2 building a clean mental model of the advisor pipeline, and Phase 3 shows them that the mental model breaks in a specific, important case. The reveal is calculated — the earlier phases have to establish the mental model before Phase 3 can dismantle it, because dismantling a model the reader does not yet hold has no effect.

Article 3.1 — "How Spring AI Implements Streaming: Flux, Subscription, and the Reactor Integration You Did Not Ask For". This article explains how `ChatClient.stream()` works, what `Flux<ChatResponse>` means in practice, and how the backpressure and lifetime semantics interact with the rest of the Spring AI machinery. The article sets up the Phase 3 reveal without yet spoiling it. Voice: Mechanism Autopsy.

Article 3.2 — "How Spring AI Implements Tool Calls: The Internal Loop Inside ChatModel That Bypasses Everything You Have Learned". This is the secondary aha-moment article. The argument is that tool-call re-invocation happens inside `OpenAiChatModel` (and equivalent classes for other providers) in a loop that does not re-enter `AdvisorChain`. The article walks through the source code of the loop and shows the specific point where the abstraction violation happens. Voice: Mechanism Autopsy.

Article 3.3 — "When Streaming and Tool Calls Combine: Four Production Bugs That Expose Spring AI's Hidden Assumption". This article is the payoff. It walks through the four specific bugs identified in Phase 1 research — logging advisor missing turns, token counter missing turns, retry advisor not re-running, context propagation loss — and shows how each one traces back to the same root cause: the `AdvisorChain.nextAroundStream` `Flux` is constructed once, and tool-call re-invocation happens below it. Voice: Production War Story (the writer presents it as a post-mortem of four bugs encountered in production, with the diagnostic path that led to the root cause).

**Phase 4 — Production Realities: Three Articles**

The fourth phase handles the production concerns that were bracketed during the earlier phases. These articles do not build on each other — they are parallel specialty pieces — and the reader can read them in any order after finishing Phase 3.

Article 4.1 — "Memory Advisors in Long Conversations: Why `MessageChatMemoryAdvisor` Bloats and How to Bound It". Voice: Production War Story.

Article 4.2 — "Backpressure in Streaming Responses: What Happens When Your HTTP Client Is Slow and Why It Is Silent Until Production". Voice: Production War Story.

Article 4.3 — "Observability for Spring AI: Tracing, Metrics, and the Specific Metric the Default Setup Is Wrong About". Voice: Design Tribunal (the writer argues that the default observability setup is correct about most things but wrong about one specific metric, and explains why).

## Phase 4 — The deliverable (abbreviated)

The deliverable for this example would be a Markdown document following the format in `output-template.md`, approximately twenty pages long. Rather than reproducing the full deliverable, this section shows the series overview section and one representative article section in full, so the format is concrete.

```markdown
# Spring AI Deep Dive Series — Creation Outline

## Series Overview

**Series argument**: Spring AI's central design decision is that ChatClient
is a fluent facade over an advisor pipeline, not a standalone API — and
understanding this, including one specific case where the advisor abstraction
breaks down under streaming plus tool calls, is the difference between a
Spring AI user who writes safe production code and one who hits the four
documented bug patterns during their first streaming-plus-tool-call
deployment.

**Target reader**: Senior Java backend engineer, 5+ years, fluent in Spring
Boot and reactive programming, has used OpenAI's REST API or its direct
SDK and is evaluating whether to adopt Spring AI for a production application
that involves streaming chat with tool calls. Already familiar with Spring's
dependency injection and configuration property system; comfortable reading
Java source code.

**Prerequisite knowledge**: Spring Boot 3.x (beans, auto-configuration,
application properties), Java 17+, basic Reactor (Flux and Mono), the concept
of LLM chat completion and tool calling at a REST API level.

**Series narrative voice**: Predominantly Mechanism Autopsy and Design
Tribunal, with Production War Story voice used for the Phase 3 failure-mode
article and the Phase 4 production-concerns articles. Voice selection per
article is specified in each article's metadata.

**Series pattern**: Spiral with cognitive-state phase naming. The primary
aha-moment concept (ChatClient as a facade over AdvisorChain) is introduced
in Phase 1 at surface level, revisited at source-code depth in Phase 2, and
revisited again in Phase 3 with the hidden-assumption break. The secondary
aha-moment concept (streaming plus tool calls breaks the advisor abstraction)
is the Phase 3 payoff.

**Scope**:
- In scope: ChatClient, Advisor, AdvisorChain, streaming, tool calling,
  the four production bugs from the research, memory advisors, backpressure,
  observability.
- Explicitly out of scope: Vector stores and retrieval-augmented generation
  (deserves its own series; the current series is already long), provider-
  specific configuration for non-OpenAI providers (the principles generalize
  but the specifics vary), prompt engineering (not a Spring AI concern, and
  covered well elsewhere).

**Structure summary**:
- Phase 1: Rebuilding the LLM Integration Mental Model — 3 articles
- Phase 2: Mastering the Advisor Pipeline — 4 articles
- Phase 3: The Streaming and Tool-Call Revelation — 3 articles
- Phase 4: Production Realities — 3 articles
- Total: 13 articles

**Divergence note**: The Spring AI official documentation is organized
around features — chat, image, audio, embedding, vector store, each as a
separate section — with ChatClient and Advisor appearing under chat. This
series deliberately does not follow that structure. Instead, it centers on
the advisor pipeline as the unifying mechanism, treats ChatClient as a
facade rather than as a first-class feature, and ignores image/audio/
embedding entirely because they dilute the focus. The series' Phase 1
argues explicitly that the docs' framing is misleading and that the
advisor-centric framing is more productive.

---

## Phase 1: Rebuilding the LLM Integration Mental Model

**Phase goal**: Replace the reader's existing mental model of LLM integration
(whether that model comes from direct SDK use, LangChain, or REST client
usage) with the Spring AI model centered on ChatClient as a facade over
AdvisorChain.

**Phase reader state at start**: The reader knows LLMs at the API level,
has used an LLM provider directly through HTTP or SDK, may have seen
LangChain or similar Python frameworks, and has not yet used Spring AI.

**Phase reader state at end**: The reader has a working mental model of
Spring AI's core architecture — ChatClient as a fluent facade, Advisor as
the extension point, AdvisorChain as the pipeline — and can predict at a
high level how the framework will behave in new situations.

### Article 1.2: ChatClient Is a Fluent Facade, Not an API

**Central argument**: ChatClient is a convenient entry point, but the
interesting work happens in the advisor pipeline it constructs on your
behalf, and a Spring AI user who treats ChatClient as the "real API" will
miss the extension surface that makes the framework powerful. This article
demonstrates the distinction by walking through a single ChatClient call
and identifying the three abstraction layers between the fluent API and
the HTTP request.

**Key concepts to cover**:
- ChatClient.prompt() and the request-specification builder pattern:
  surface-level coverage, because the reader needs it to follow the example
- Advisor construction from fluent configuration: medium depth, because
  this is where the first abstraction layer becomes visible
- AdvisorChain assembly: surface-level mention, because Article 2.1 will
  cover it at depth
- The ChatModel layer underneath AdvisorChain: surface-level mention for
  context
- The path from ChatClient.call() to the provider's HTTP endpoint: mid-depth
  walk, covering all three layers

**Prerequisite knowledge**: The reader has read Article 1.1 (which
established that Spring AI is Spring-native rather than LangChain-like)
and knows Spring Boot bean/DI concepts and Java fluent-builder patterns.

**Must-research areas**: Verify current ChatClient source location and the
specific class names in Spring AI 1.0.0-M6. Confirm the three-layer structure
is the same in the current version as in research notes.

**Reference links**:
- https://docs.spring.io/spring-ai/reference/1.0/api/chatclient.html —
  the official ChatClient reference; extract the public API surface and
  the official description of how ChatClient relates to ChatModel
- spring-ai-core/src/main/java/org/springframework/ai/chat/client/
  ChatClient.java — the ChatClient interface; extract the method signatures
  and the builder pattern
- spring-ai-core/src/main/java/org/springframework/ai/chat/client/
  DefaultChatClient.java — the default implementation; extract the advisor
  chain construction in the prompt() and call() methods
- spring-ai-core/src/main/java/org/springframework/ai/chat/client/advisor/
  DefaultChatClientBuilder.java — the builder; extract how defaultAdvisors
  are composed with per-request advisors

**Narrative voice**: Mechanism Autopsy. The article walks through source
code; authority comes from specific file paths and specific method references.

**Scope**:
- In: The three abstraction layers between ChatClient.prompt().call() and
  the provider HTTP request, with specific source-code anchors
- Out: Custom advisor writing (Article 2.3), the internal loop inside
  ChatModel (Article 3.2), streaming specifics (Article 3.1)

**tech-writing prompt**:

```
/tech-write
<prompt>
Write a technical blog post with the following specification.

**Central argument**: Spring AI's ChatClient is a convenient fluent entry
point, but the interesting work happens in the advisor pipeline it constructs
on your behalf. A Spring AI user who treats ChatClient as the "real API"
misses the actual extension surface, because that surface is AdvisorChain.
This article proves the claim by walking through a single ChatClient call
and showing the three abstraction layers between the fluent API and the
HTTP request.

**Narrative voice**: Mechanism Autopsy. The article walks through source
code; authority comes from specific file paths, class names, and method
references. The reader should feel they are looking over the writer's
shoulder at the Spring AI source.

**Reader profile**: Senior Java backend engineer, 5+ years, fluent in
Spring Boot. Has read Article 1.1 of this series (which argued that Spring
AI is Spring-native, not a LangChain port). Has not yet used Spring AI but
knows Spring Boot bean and dependency-injection patterns and Java fluent-
builder patterns.

**Prerequisite knowledge**: Spring Boot bean configuration, Java fluent
builders, basic understanding of LLM chat completion APIs. From Article 1.1
of this series: the argument that Spring AI is a Spring-native framework
with design decisions that prioritize Spring's programming model.

**Technical anchors to include**:
- Spring AI version: 1.0.0-M6
- File: spring-ai-core/src/main/java/org/springframework/ai/chat/client/
  ChatClient.java — the ChatClient interface declaration
- File: spring-ai-core/src/main/java/org/springframework/ai/chat/client/
  DefaultChatClient.java — the default implementation, specifically the
  prompt() and call() methods where the advisor chain is constructed
- File: spring-ai-core/src/main/java/org/springframework/ai/chat/client/
  advisor/DefaultChatClientBuilder.java — the builder, specifically the
  composition of defaultAdvisors with per-request advisors
- A minimal example: a ChatClient.prompt().user("hello").call() call,
  traced through the three abstraction layers to the final HTTP request

**Scope**:
- In: The three abstraction layers between ChatClient.prompt().call() and
  the provider HTTP request, with specific source-code anchors; the
  construction of the advisor chain from builder configuration; the
  terminal call site where AdvisorChain delegates to ChatModel
- Explicitly out of scope: Custom advisor writing (covered in Article 2.3
  of this series), the internal loop inside ChatModel for tool calls
  (covered in Article 3.2), streaming specifics (covered in Article 3.1),
  provider-specific details for non-OpenAI providers

**Source references to consult**:
- https://docs.spring.io/spring-ai/reference/1.0/api/chatclient.html —
  extract the public API surface and the official description of the
  ChatClient-ChatModel relationship
- Spring AI GitHub repository, main branch as of 1.0.0-M6 tag — extract
  the source files listed in the anchors section

**Additional guidance**: The article should end with a mental model the
reader can reuse: given a ChatClient call they have not seen before, they
should be able to predict which parts of its behavior live in the fluent
API, which live in the advisor chain, and which live in the ChatModel.
The mental model is the primary aha moment for this phase of the series.

Follow the full tech-writing skill workflow. Output language is Chinese
with technical terms in English.
</prompt>
```

[The remaining articles in the phase would follow in the same format.
The remaining phases would follow the same overall structure.]
```

## Phase 4 — Validation summary for this example

The deliverable above passes the outline quality checklist on the following bases. Gate 1 passes because the series argument is falsifiable and the individual article arguments collectively support it. Gate 2 passes because every article title states a claim rather than a topic. Gate 3 passes because the phase names reflect cognitive transitions (Rebuilding, Mastering, Revelation, Realities). Gate 4 passes because the series structure diverges from the official docs' feature-tour structure, with the divergence made explicit in the overview. Gate 5 passes because the article dependency order is verified — each article's prerequisites are covered by earlier articles. Gate 6 passes because overlapping revisits (the ChatClient-facade concept introduced in 1.2 and revisited in 2.1 and 3.2) are spiral revisits with distinct aspects. Gate 7 passes because the reference links are specific and annotated. Gate 8 passes because each prompt contains the seven required pieces. Gate 9 passes because each phase contains three or four articles. Gate 10 passes because the total of thirteen articles is appropriate for a medium-length spiral series. Gate 11 passes because two aha-moment articles are present (1.2 and 3.2). Gate 12 passes because the coherence notes are substantive.

A planner running Phase 4 on a real series would produce a similar validation summary, grouping any gate failures by the phase they need to return to and re-running the loop until the outline passes cleanly.

## What this example demonstrates

This example is intentionally detailed because the skill's value is in the detail. A thin example would show the format but not the work, and the work is what separates a good series plan from surface skating. The concrete anchors in Phase 1 (specific file paths, specific bug patterns, specific version numbers), the concrete prerequisites and aha-moment flags in Phase 2, the concrete voice and scope decisions in Phase 3, and the concrete tech-writing prompt in Phase 4 are all necessary for the series to be producible without further research from the writer.

A planner applying the workflow to a different framework should aim for the same level of concreteness at each phase. If the research notes in Phase 1 are vague ("Spring AI has advisors"), the knowledge graph in Phase 2 will be vague, the architecture in Phase 3 will be vague, and the deliverable in Phase 4 will fail the quality checklist. If the research notes in Phase 1 are specific (file paths, bug patterns, version numbers), the downstream phases become tractable and the deliverable comes out strong on the first or second validation pass.