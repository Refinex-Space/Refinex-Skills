# Prompt template (tech-writing handoff format)

This file describes the format and content rules for the per-article prompts that tech-planner generates for consumption by the tech-writing skill. The prompt is the handoff payload between the planning skill and the writing skill, and its quality determines whether the downstream writing step can produce a high-quality article without additional context from the user. A thin prompt forces the user to supply missing details manually during the writing step, which defeats the purpose of having a separate planning phase; a complete prompt lets the user copy it straight into tech-writing and get a strong draft on the first pass.

The prompt format has two goals worth stating explicitly before the template is introduced. The first goal is completeness: the prompt must contain everything the tech-writing skill needs to populate its own Phase 1 Anchor Sheet. A reader of the prompt (or the tech-writing skill itself) should be able to construct an Anchor Sheet without referring back to the planner, the user, or any external material. The second goal is portability: the prompt must be formatted so it can be copied as a single unit, pasted into a chat session with the tech-writing skill, and executed without any modification. Any requirement that the user edit the prompt before use is a failure of the planning phase.

## The canonical wrapping format

Every per-article prompt is wrapped in the following format, which is designed for direct copy-paste into the tech-writing skill:

```
/tech-write
<prompt>
[complete prompt content in natural language]
</prompt>
```

The `/tech-write` token is the skill invocation. The `<prompt>` and `</prompt>` tags mark the content boundary. The content inside the tags is the Anchor Sheet in natural language form — not a structured YAML or table, but a paragraph-by-paragraph description of what the article should be. Natural language is preferred because the tech-writing skill's Phase 1 is already designed to accept natural-language specifications, and because natural language carries rationale and context that a structured format would strip.

The content inside the wrapping must cover nine specific pieces of information. Each piece corresponds to a field in the tech-writing Anchor Sheet or its drafting contract, and all nine must be present for the prompt to be considered complete.

## The nine required pieces

The first piece is the **central argument**, stated as a single falsifiable sentence. The central argument is the core claim the article will make, written in the form "X is Y, because Z, and the usual objection W is wrong for reason V" or a similar defensible construction. The argument should be specific enough that a reader who disagreed with it could point to specific evidence, and it should be sharp enough that a reader who has not read the article yet can tell what they will be asked to believe. A central argument like "Spring AI's `ChatClient` is a clean abstraction" is too vague and fails; "Spring AI's `ChatClient` is a clean abstraction in the synchronous case but leaks abstraction as soon as you enable streaming with tool calls, and the leak is specifically in `AdvisorChain`'s assumption that advisors are pure functions" passes.

The second piece is the **narrative voice**, selected explicitly from the tech-writing voice catalog. The voice options are Production War Story, Design Tribunal, Mechanism Autopsy, Migration Field Guide, Benchmarker's Notebook, and Reference Librarian. The planner picks the voice based on the article's argument and the phase's cognitive state — mechanism articles in the Master phase typically use Mechanism Autopsy, comparison articles in the Reconstruct phase typically use Design Tribunal, failure-mode articles in the Debug phase typically use Production War Story, and so on. The prompt names the voice explicitly so the downstream writing phase does not have to guess, and a single phase can mix voices if different articles in the phase serve different purposes.

The third piece is the **required technical anchors**, a list of the specific concrete things the article must contain. Anchors are the raw material the article will be built from: real numbers, specific API signatures, specific source file and line references, specific version numbers, specific error messages, specific commits or pull requests, specific conference talks or maintainer comments. The anchor list comes directly from the Phase 1 research notes — it is the subset of the research relevant to this particular article — and it is what the tech-writing skill's own Phase 1 will use to populate its Anchor Sheet. A prompt without a concrete anchor list is a prompt that expects the tech-writing skill to do the research itself, which is backward.

The fourth piece is the **reader profile**, a specific description of who the article is for. The reader profile comes from the series overview, but it can be refined for individual articles — an article in Phase 1 of the series has a reader who knows less about the framework than an article in Phase 3, and the prompt should reflect the difference. A good reader profile names the reader's existing knowledge ("backend engineer, 3+ years, familiar with Spring Boot and Hibernate, has used OpenAI's REST API directly but not a Java-side abstraction layer") rather than a demographic ("Java developers").

The fifth piece is the **prerequisite knowledge**, a specific list of what the reader is assumed to already know at the point of reading this article. For the first article in the series, the prerequisites are whatever the series overview declared as the reader's entry state. For later articles, the prerequisites include both the series' entry-state assumptions and the cumulative learning from all earlier articles in the series. The prerequisites must be explicit, because the tech-writing skill will use them to decide what to skip rather than re-explain. An article that re-explains every concept from scratch is a waste of the reader's time; an article that assumes knowledge the reader does not have will be incomprehensible.

The sixth piece is the **scope boundary**, with both "in scope" and "explicitly out of scope" components. The out-of-scope list is the more important of the two, because it is how the article earns the right to not cover topics the reader might expect. For a series, the out-of-scope list also helps prevent overlap with other articles in the series — the prompt can say "the `Advisor` lifecycle and ordering semantics are covered in Article 2.3; this article only covers the `Advisor` interface itself" and the downstream writing phase will know to defer the other topic.

The seventh piece is the **source references**, a list of specific links or pointers to the primary sources the writing phase should consult. These are the same reference links that appear in the Markdown outline's article section, reproduced in the prompt so the writing phase has them at hand. Each reference is specific (a URL to a documentation page, a source file path, a conference talk timestamp) and annotated (what to extract from it).

The eighth piece is the **visual explanation plan**. When the article's central claim depends on a mechanism, topology, lifecycle, or timeline that would be expensive to track in prose alone, the prompt specifies the reader question the diagram must answer and the Mermaid type that best fits it. The planner chooses the type from the question rather than by habit: `sequenceDiagram` for temporal call order, `flowchart` for branching pipelines, `stateDiagram-v2` for state transitions, `classDiagram` or `erDiagram` for static relationships, and `timeline` for change over time. The prompt also tells the downstream writer to use `mermaid-diagrams` for the actual Mermaid authoring so the diagram follows the write suite's shared syntax, layout, and styling standard. A planner that omits this field for a mechanism-heavy article is silently pushing cognitive work onto the downstream writer.

The ninth piece is the **depth and completeness contract**. This is the downstream writing instruction that prevents the article from turning into a short, nervous summary. The contract states that the writer must not stop because the piece is already "long enough"; they stop only after every load-bearing anchor, mechanism, rejected alternative, and boundary promised by the prompt has been discharged or explicitly scoped out. This is not permission for padding. It is a guard against premature stopping.

## Template

The nine pieces are assembled into a natural-language paragraph form. The template below shows the structure with placeholders; a filled-in example follows in the next section.

```
/tech-write
<prompt>
Write Article [N.M] of the [framework] series, titled "[argument-carrying
title]".

[Central argument paragraph: one or two sentences stating the article's
falsifiable thesis. The argument should be specific, defensible, and sharp
enough that a reader can tell what they will be asked to believe.]

[Voice paragraph: name the narrative voice explicitly, with one sentence on
why this voice fits this article. Voice options: Production War Story,
Design Tribunal, Mechanism Autopsy, Migration Field Guide, Benchmarker's
Notebook, Reference Librarian.]

[Technical anchors paragraph: list the specific concrete anchors the article
must contain. Real numbers with measurement context. Specific class names,
method signatures, file paths, line numbers. Specific version numbers.
Specific error messages, commits, pull requests, or conference talks.
Each anchor is named, not gestured at.]

[Reader profile paragraph: who this article is for, including their existing
knowledge and the misconceptions they probably hold. Be specific about
experience level and prior frameworks.]

[Prerequisite knowledge paragraph: what the reader has internalized from
earlier articles in the series. Reference the earlier articles by number
and state the specific concepts they introduced.]

[Scope paragraph: in-scope topics and out-of-scope topics. The out-of-scope
list is the more important one. Reference other articles in the series
that cover the out-of-scope material.]

[Source references paragraph: list the specific URLs, file paths, and
other references the writing phase should consult, each annotated with
what to extract from it.]

[Visual explanation paragraph: if the article needs one or more diagrams,
state the question each diagram answers, the Mermaid type, and the reader
payoff. Example: "Include a sequenceDiagram showing how X calls Y and how
the retry loop re-enters Z; the point is to make the once-per-request
interceptor boundary visible."]

[Depth/completeness paragraph: instruct the writer to continue until every
load-bearing anchor, mechanism, rejected alternative, and boundary in this
prompt has been paid off or explicitly scoped out. Make it clear that
brevity is not a stopping condition and padding is not allowed.]

Follow the full tech-writing skill workflow: Phase 1 pre-writing protocol,
Phase 2 drafting in the specified voice, Phase 3 validation against the
shared quality checklist. Output language is [Chinese with technical terms
in English | English].
</prompt>
```

## A filled-in example

The template above is abstract; the example below shows a filled-in prompt for a specific article from a Spring AI series. The article is "Article 2.1: AdvisorChain.around() is invoked exactly once per ChatClient.call(), regardless of how many tool-call iterations follow — and this single fact explains four common production bugs", from a hypothetical series titled "Spring AI Beyond the Hello World".

```
/tech-write
<prompt>
Write Article 2.1 of the Spring AI series, titled "AdvisorChain.around() is
invoked exactly once per ChatClient.call(), regardless of how many tool-call
iterations follow — and this single fact explains four common production
bugs".

Central argument: Spring AI's AdvisorChain interceptor model assumes that
each ChatClient invocation is a single bounded operation, but the streaming
+ tool-call combination breaks this assumption silently. The around() method
of every advisor in the chain runs exactly once per ChatClient.call() —
not once per tool-call iteration — which means any advisor that tries to
log, count, retry, or propagate context across tool-call iterations will
fail in ways the docs do not warn about.

Voice: Mechanism Autopsy. The article is opening up the AdvisorChain source
code and walking the reader through the around() invocation path, showing
the specific line at which the once-per-call semantics are established and
the four user-visible bugs that follow from it. Mechanism Autopsy is the
right voice because the authority of the article comes from specific source
references rather than from opinion.

Required technical anchors: (1) the file
spring-ai-core/src/main/java/org/springframework/ai/chat/client/advisor/api/AdvisorChain.java
in Spring AI 1.0.0-RC1, specifically the nextAroundCall method around line
60-80; (2) the four specific bugs visible in production — logging advisor
records only the first tool-call's prompt; token-counting advisor returns
0 for tool-call follow-up turns; retry advisor does not re-trigger after
tool-call failures; MDC/TraceId context propagation breaks at the second
tool-call iteration; (3) the relevant GitHub issues #1234, #1289, #1301
where these bugs have been reported; (4) the workaround pattern (manual
context propagation in the tool callback) with code example; (5) the fix
that landed in 1.0.0-RC2 for two of the four bugs and the status of the
other two as of writing.

Reader profile: backend Java engineer with 3+ years of Spring Boot
experience, currently using Spring AI 1.0.0-RC1 in production for a
chat-style feature, has hit at least one of the four bugs and is looking
for an explanation that goes beyond the workarounds.

Prerequisite knowledge: the reader has read Article 1.1 (ChatClient is a
state machine, not an HTTP wrapper), Article 1.2 (Spring AI's IoC opinions),
and the series overview. They know what AdvisorChain is, that advisors
have around/before/after methods, and that tool-calling works via
ChatClient. They have NOT yet seen the internal flow of how AdvisorChain
sequences advisors, which this article will explain.

In scope: AdvisorChain.around() invocation count semantics, the four bug
patterns and their root cause, the workaround for unfixed bugs as of
1.0.0-RC1, the relationship between the around() lifecycle and the
internal tool-call iteration loop in StreamingChatModel.

Out of scope: the Advisor interface itself (covered in Article 1.3), the
ordering semantics of the AdvisorChain (covered in Article 2.3), and the
distinction between sync and streaming ChatClient (covered in Article 1.1).
Reference the other articles when these topics come up rather than
re-explaining them.

Source references: (1)
https://github.com/spring-projects/spring-ai/blob/1.0.0-RC1/spring-ai-core/src/main/java/org/springframework/ai/chat/client/advisor/api/AdvisorChain.java
— extract the around() invocation chain and the line at which the
once-per-call semantics are committed; (2)
https://github.com/spring-projects/spring-ai/issues/1234 — extract the
user's symptom description and the maintainer's response; (3)
https://docs.spring.io/spring-ai/reference/api/advisors.html — extract
the documented advisor lifecycle and note the absence of any mention of
tool-call iteration; (4) the Spring AI 1.0.0-RC2 release notes — extract
the two bug fixes that landed.

Visual explanation plan: use `mermaid-diagrams` to author a
`sequenceDiagram` showing one
`ChatClient.call()` from advisor entry to the first provider response, then
the internal tool-call iteration and the point at which control re-enters
the model without re-entering `AdvisorChain.around()`. The reader should be
able to see, at a glance, why the once-per-call boundary creates the four
bugs. Also use `mermaid-diagrams` to author a small `flowchart` showing the three execution modes
(sync without tools, streaming without tools, streaming with tools) and
highlight that only one branch crosses the broken path.

Depth and completeness contract: do not stop after naming the four bugs.
For each bug, pay off the full chain: trigger condition, internal cause,
observable symptom, evidence in source or issue tracker, workaround, and
version boundary if the fix status changed. If any one of the four cannot
be discharged with the available evidence, say so explicitly rather than
compressing it into a vague paragraph.

Follow the full tech-writing skill workflow: Phase 1 pre-writing protocol,
Phase 2 drafting in the specified voice, Phase 3 validation against the
shared quality checklist. The article should end on a reusable mental
model — specifically, the rule "if your advisor needs to react to anything
that happens during a tool-call iteration, the advisor's around() method
is the wrong extension point, and the right extension point is a custom
ToolCallback wrapper". This rule is the payoff that the technical
walkthrough is building toward.

Output language is Chinese with technical terms in English.
</prompt>
```

Notice the specificity of the filled-in version. Every anchor is concrete enough to be verifiable. Every reference link names a specific resource, not a homepage. The scope is bounded in both directions. The central argument is falsifiable — a reader who disagreed with it would know what evidence would settle the question. The prerequisites are explicit and cumulative, referring to earlier articles in the series by number. The visual plan is explicit, and the depth contract prevents the downstream writer from silently collapsing the article into a shallow summary.

A prompt that looks like this can be copied into tech-writing without modification and will produce a draft that needs no further input from the user. That is the target the template is designed to hit.

## Two common failures

The first common failure in prompt generation is vague anchor lists. A prompt that says "include relevant code examples" is not specifying anchors — it is deferring the anchor selection to the writing phase, which does not have the research context to pick the right ones. The fix is to list anchors by name and location during Phase 3 of the planner, using the research notes from Phase 1. Every anchor in the list should be identifiable: a specific method, a specific line, a specific commit, a specific metric.

The second common failure is inheriting the prompt format from one article to another without updating the context. Two articles in the same series share the reader profile and the series overview, but they do not share the prerequisite knowledge (which is cumulative), the central argument, the scope, or most of the anchors. A prompt copied from an earlier article and minimally edited is almost always wrong for the current article, even when the two articles are closely related. The fix is to generate each prompt from scratch using the template, filling in each field based on the specific article's place in the series.

## Language switching

When the user has requested Chinese output (the default), the prompt is generated in Chinese for the natural-language sections (central argument, voice rationale, reader profile, prerequisite knowledge, scope statements) while keeping technical terms — class names, method names, file paths, configuration keys, library names, version numbers, and so on — in English. The closing "Output language" instruction names Chinese with technical terms in English.

When the user has requested English output, the entire prompt is in English and the closing instruction names English. The prompt structure does not change between languages; only the natural-language sections switch.

The nine required pieces remain the same in either language. A prompt that is short or vague in one language will be short or vague in the translation. The work of filling in the nine pieces with specific content happens in Phase 3 regardless of the output language, and the language choice affects only the surface form of the result.
