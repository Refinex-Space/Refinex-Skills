---
name: tech-planner
description: Plan a comprehensive, multi-article technical blog series about a framework, library, protocol, or broad technical topic. Use this skill whenever the user names a technical target such as "Spring AI", "Project Reactor", "Kubernetes Operators", or similar, and asks for a series plan, learning roadmap, article sequence, or content outline. The skill conducts exhaustive primary-source research, constructs a prerequisite-respecting knowledge graph, designs a cognitively-sequenced series architecture, and emits a detailed outline with one ready-to-paste tech-writing prompt per article. This skill is the strategic layer above tech-writing and tech-rewrite — tech-planner produces the plan, and the per-article prompts feed directly into tech-writing for drafting. Default output is Chinese with technical terms in English. Enforces a mandatory three-phase research protocol because AI series plans fail by mirroring official docs instead of reflecting how knowledge builds in a reader's head.
---

# tech-planner

A skill for planning multi-article technical blog series. The user names a technical target — a framework, library, protocol, or topic — and wants a comprehensive, cognitively sequenced plan for writing a series of high-quality articles about it. This skill exists to prevent one category of failure: **surface skating**, the set of shortcuts by which an AI-generated series plan looks comprehensive while actually doing very little useful thinking about the topic.

The defense is a three-phase research protocol that must be completed before any outline is produced. Phase 1 is source exhaustion, the systematic consumption of official documentation, source code, release notes, issue trackers, and authoritative secondary sources. Phase 2 is knowledge graph construction, the mapping of concepts, prerequisite relationships, and the gaps between the official narrative and how the topic actually works. Phase 3 is series architecture design, the translation of the knowledge graph into a cognitively ordered sequence of articles, each with a concise editorial title, a specific central thesis, and a ready-to-paste tech-writing prompt. The title or phase name is not where the whole thesis lives; the thesis lives in the thesis line and the prompt.

This skill sits above `tech-writing` and `tech-rewrite`. It produces the strategic plan; the per-article prompts are then fed into `tech-writing` for actual drafting. The three skills form a pipeline: tech-planner yields the outline, the outline yields per-article prompts, and the prompts yield articles. Every prompt this skill generates is formatted for direct copy-paste into `tech-writing`, and every prompt must be complete enough to produce a high-quality article without additional context — including the article's visual-explanation plan, the instruction to use `mermaid-diagrams` when a diagram is required, and its depth/completeness contract — because the user will run them one at a time, days or weeks apart, and should not have to remember what the series was about.

---

## The failure mode this skill fights

Surface skating is easy to produce and hard to notice. A model asked to "plan a Spring AI blog series" can generate something that looks like a plan in seconds: a list of ten article titles organized into sections, each title referring to a concept from the Spring AI documentation. The output has the shape of a plan. It has the right keywords. It even has the right number of articles. What it does not have is any evidence that the planner actually understood the topic.

The failure modes cluster into eight specific patterns. The first is **documentation mirroring**, where the outline's structure matches the official documentation's table of contents. If the Spring AI docs have sections titled "ChatClient", "ChatModel", "Prompts", "Embeddings", "Vector Stores", "RAG", and "Tools", the skating outline will have seven articles with essentially the same titles. Nothing has been added, nothing has been reorganized, and the reader gets no benefit over just reading the docs.

The second is **title theater**, where article titles either collapse into empty topic tags or over-expand into AI-scented rhetorical constructions. "Introduction to Spring AI" is a topic tag; "ChatClient → AdvisorChain → ChatModel 三层夹心——你的第一次 API 调用背后发生了什么" is overloaded in the opposite direction. A strong title is short, technically accurate, and editorially natural. It may carry a light claim, but it must not try to hold the full central thesis, teaser, contrast, and payoff. Examples in the desired style: `版本基线`, `配置绑定`, `事务边界`, `Consumer Group`, `GC 日志`, `生产清单`.

The third is **phase taxonomy theater**, where phases are named either as generic difficulty buckets ("Basics", "Intermediate", "Advanced") or as inflated abstractions and verb slogans ("认知重建", "驯服配置", "拆开魔法", "穿透 Web", "走向异步") that sound more like generated taxonomy than editorial judgment. A strong phase name is short, natural, and specific enough to orient the reader: `建立入口`, `配置管理`, `自动配置`, `SQL 基础`, `事务并发`, `观测排障`. The phase goal paragraph then carries the fuller cognitive move.

The fourth is **foundation skip**, where the series jumps into mechanism autopsy, architecture critique, or source-level reconstruction before the reader has a runnable first project, a version boundary, basic terminology, or a Hello World path. Many framework outlines fail here: they are written by someone already inside the framework, for readers who are not.

The fifth is **benefit blindness**, where the planner organizes the series around concepts but never around what the reader is trying to gain in each phase. A strong series does not only answer "what concept comes next"; it answers "what can the reader do after this phase that they could not do before?" If the planner cannot state that benefit concretely, the phase is probably taxonomy, not teaching.

The sixth is **theory-first intimidation**, where the series puts the reader into deep mechanism, internal architecture, or design philosophy before the reader has felt the problem, used the API once, or built any working intuition. Deep mechanism has value, but value is not the same as placement. Many topics become easier only after the reader has a little practical friction to hang the mechanism on.

The seventh is **prerequisite amnesia**, where articles reference concepts before those concepts have been introduced in earlier articles, or where the same concept is re-introduced in multiple articles because the planner lost track of what the reader already knows. The defense against prerequisite amnesia is the explicit knowledge graph built in Phase 2, which makes dependencies visible and checkable.

The eighth is **loop-disguised-as-spiral**, the most subtle failure. A series that revisits concepts repeatedly without adding new complexity or depth is a loop, not a spiral. Jerome Bruner's work on the spiral curriculum makes the distinction explicit: a genuine spiral revisits concepts at increasing levels of complexity, while a loop just repeats. Loop-shaped series give the reader a false sense of progression — they feel like they are learning because they keep seeing new articles, but the articles are not advancing the reader's mental model in a way the reader can feel a few months later.

---

## The spiral, not the loop

The skill's organizing principle comes from Bruner's 1960 work on cognitive progression in education. A spiral curriculum revisits topics at increasing complexity, with each revisit requiring and reinforcing the prior visits. A well-designed blog series is a spiral in exactly this sense: early articles lay conceptual foundations, middle articles build mechanisms on top of those foundations, and later articles use the mechanisms to make load-bearing decisions or perform deep analyses that would have been incomprehensible in the early articles.

The difference between a spiral and a loop is the single most useful diagnostic for a series plan. A loop revisits a concept and does roughly the same thing with it; a spiral revisits a concept and does something harder with it that depends on the earlier visit. A series that introduces "prompts" in article two, uses "prompts" in article five, and uses "prompts" in article nine has done nothing useful unless each use deepens the reader's understanding of prompts beyond the previous use. The planner's job is to verify, for every revisited concept, that the revisit advances the reader's model. When the revisit does not advance the model, the revisit is either cut or restructured to add the missing complexity.

This principle has a practical consequence for article ordering. Articles cannot be reordered freely; they have prerequisites, and the prerequisites are what turn the sequence into a spiral rather than a list. The knowledge graph from Phase 2 is what makes these prerequisites visible. An article that depends on three earlier articles cannot be published before any of them, and an article that revisits a concept must be positioned so the revisit adds depth to the earlier introduction. The ordering is not aesthetic — it is causal.

---

## Workflow

Every tech-planner task follows the same three research phases, then produces the outline. The phases cannot be compressed or skipped; a plan produced without Phase 1 is almost always a documentation mirror, and a plan produced without Phase 2 is almost always a prerequisite-amnesic list.

```
Phase 1: SOURCE EXHAUSTION     → produces a Research Dossier
Phase 2: KNOWLEDGE GRAPH       → produces a Concept Dependency Map
Phase 3: SERIES ARCHITECTURE   → produces the final Series Outline
Phase 4: VALIDATION            → runs the outline through the quality checklist
```

### Phase 1 — Source exhaustion

Phase 1 is the systematic consumption of primary sources for the target framework or topic. The goal is not to "get a feel for" the topic but to build an exhaustive list of concepts, APIs, design decisions, documented behaviors, known limitations, undocumented behaviors, release history, and community pain points. The output is a Research Dossier — a structured working document that will feed into Phase 2.

The order of sources matters. The skill starts with the official documentation because it defines the terminology the rest of the research will use. It then moves to source code because source code reveals the architecture the documentation often obscures. Release notes and changelogs come next because they reveal the evolutionary narrative of the project. GitHub issues and discussions follow because they reveal community pain points and maintainer design intent that the documentation does not capture. Finally, the skill consumes authoritative secondary sources — conference talks by maintainers, official blog posts, RFC/JEP-style design proposals — to triangulate the research against multiple perspectives.

Throughout Phase 1, the reader must resist the temptation to treat the official documentation's structure as the outline's structure. The documentation is structured for reference, not for learning. The outline will diverge from it. That divergence is only possible if the planner has extracted the underlying concepts from the documentation, not the documentation's chapter headings.

The detailed procedures for each source type, including anti-skim techniques and concrete checklists, live in `references/research-methodology.md`. That file should be read at the start of every Phase 1, even when the planner has done research before, because it catches the specific shortcuts that lead to surface skating.

### Phase 2 — Knowledge graph construction

Phase 2 turns the Research Dossier into a Concept Dependency Map. The map is a graph structure where each node is a concept the reader must understand and each edge is a prerequisite relationship: "to understand node B, the reader must already understand node A". The graph makes the topic's cognitive structure visible in a way that lets the planner order articles without guessing.

The graph is built in four steps: extract concepts as nodes, draw prerequisite edges, identify clusters that become candidate articles, and find the aha-moment dependencies — the specific concepts whose first correct understanding unlocks the rest of the topic. The graph also captures the gap between the official narrative and the real-world usage patterns, because the early articles in a strong series should address early real-world pain points rather than the early chapters of the documentation.

The detailed procedure for building the graph lives in `references/knowledge-graph-construction.md`. That file includes techniques for identifying concepts, rules for drawing edges, heuristics for clustering, and a worked example on a real framework.

### Phase 3 — Series architecture design

Phase 3 is the synthesis step. The planner takes the Concept Dependency Map from Phase 2 and produces a Series Outline that respects the graph's ordering constraints, groups concept clusters into phases, and decides five things explicitly before naming anything: whether the series needs a Foundation/Onboarding pass, what the reader-benefit ladder is from phase to phase, whether the early phases should be use-first before theory-first, whether it needs a late synthesis/architecture pass for senior readers, and how much article decomposition the topic actually needs. Only then does the planner assign phase names. The outline is then validated against the quality checklist in `references/outline-quality-checklist.md` and, if all gates pass, delivered to the user.

The design proceeds in five layers. The first is benefit design: the planner states the reader's start state, the intermediate usable states, and the end state, and decides what each phase lets the reader do. The second is phase identification: the planner looks at the knowledge graph and identifies natural cognitive progression stages, picking a series architecture pattern from `references/series-patterns.md` that matches the topic, the reader profile, and the benefit ladder. The third is article placement within phases: the planner groups concept clusters from Phase 2 into individual articles, with each article carrying a single argument and a clear role in the ramp from first use to deeper understanding. The fourth is per-article specification: the planner writes a central argument, lists the key concepts, names prerequisite articles, lists reference links, and generates a tech-writing prompt using the template in `references/prompt-template.md`. The fifth is coherence verification: the planner runs the full quality checklist before delivery.

### Phase 4 — Validation

Phase 4 runs the completed outline through the full quality checklist in `references/outline-quality-checklist.md`. The gates catch the specific signatures of surface skating — documentation mirroring, topic-tag titles, difficulty-label phase names, prerequisite amnesia, theory-first intimidation, loop-shaped revisits, and the rest. A draft that passes the checklist is delivered to the user. A draft that fails any gate is corrected, and the checklist is re-run from the top, because fixes sometimes break earlier gates that had previously passed.

A first-pass outline almost never passes cleanly — expect two or three iterations through the loop. Outlines that require more than five iterations are a signal that Phase 1, Phase 2, or Phase 3 was insufficient and that the planner should return to the earlier phase rather than continuing to iterate on the outline itself.

---

## Output specification

The skill's output is a single Markdown document that follows the structure in `references/output-template.md`. The structure is not decorative — it is the format the user's downstream tooling expects, and deviations break the pipeline into `tech-writing`.

The document begins with a series overview that names the framework or topic, defines the version boundary, describes the total scope and exclusions, identifies the target reader profile and entry-state prerequisite knowledge, states the series argument, defines the reader ladder from entry state to end state, and explains why the structure diverges from the official docs.

The document then contains one section per phase. Each phase section begins with a concise heading in the form "Phase N — Name". The name should be short and editorially natural. The cognitive move belongs in the phase goal paragraph, which explains what the reader will be able to do by the end of the phase that they could not do before.

Within each phase, the document contains one subsection per article. Each article subsection contains only the article number and title, a one-sentence central thesis for navigation, an optional note when the article is a foundation article, aha-moment article, bridge article, or synthesis article, and the complete tech-writing prompt formatted for direct copy-paste. Do **not** repeat the prompt's detailed metadata outside the prompt. Central argument, voice, reader profile, prerequisite knowledge, scope, source references, visual plan, and depth contract belong inside the prompt and should appear once there, not twice in the outer outline.

Visible naming has its own contract. Phase names and article names are navigation, not a performance of depth. Prefer compact professional labels like `版本基线`, `配置优先级`, `DataSource 装配`, `事务边界`, `GC 日志`, or `架构决策`. Reject titles that read like generated mini-essays, especially forms such as `从 X 到 Y 都要 Z`, `先 X 再 Y`, `不是 X 而是 Y`, `把 X 变成 Y`, `X 背后的真实代价`, and any title that needs multiple commas, arrows, or stacked clauses to work. If the title feels less like a table of contents entry and more like ad copy for the article, rewrite it.

A complete worked example of the deliverable format, applied to a Spring AI series, is in `references/worked-example.md`. New planners should read that file before producing their first deliverable to see what the expected level of detail looks like.

---

## When to stop and ask the user

Three situations should stop the workflow and trigger a question to the user before proceeding.

The first is when the target topic is too broad or too narrow for a single series. A request for a "Kubernetes" series is too broad — Kubernetes has dozens of subsystems, each of which could be its own series — and the planner should ask the user to narrow the target before running Phase 1. A request for a "Spring AI's `ChatOptions` builder" series is too narrow — a single class does not need a multi-article series — and the planner should ask whether the user wants to scope up.

The second is when the Research Dossier reveals that the topic has major version differences or framework flux that the user has not specified. Spring AI 1.0.0-M6 and Spring AI 1.0.0-RC1 have different tool-calling implementations; a series that straddles the version boundary produces articles that go stale in different ways for different readers. The planner should ask the user which version to target and scope the series accordingly.

The third is when the knowledge graph reveals that the topic requires prerequisite knowledge the user has not mentioned. A series on Kubernetes Operators assumes familiarity with Kubernetes primitives like Deployments and ConfigMaps; a series on Project Reactor assumes familiarity with functional composition. If the user has not indicated whether the reader has the prerequisites, the planner should ask, because the answer determines whether the series starts at the prerequisite level or assumes it.

In all three cases, the question is asked once, with specific options, before committing to Phase 1. Guessing at the scope and rewriting the outline later is more expensive than asking.

---

## Output language defaults

The default output language is Chinese with technical terms in English, following the conventions from the tech-writing skill. Generated tech-writing prompts match the user's preferred language — a Chinese-language series produces Chinese-language prompts, so the tech-writing skill then produces Chinese articles. Technical terms stay in English throughout: framework names, class names, method names, configuration keys, protocol names, and CLI flags are never machine-translated.

The research phase (Phase 1) operates in the source's native language, which for most Western frameworks is English. The planner reads English documentation, English source code, English issue threads, and English conference talks, and then produces a Chinese outline with concise Chinese titles. Translating concepts into Chinese during Phase 2 is a deliberate step: the Chinese title should sound like an editor chose it, not like a taxonomy generator expanded it. When depth and brevity conflict, put the depth in the prompt's `中心论点`, not in the visible title.

---

## Reference file map

All reference files are one level below `SKILL.md`. Read the file relevant to the current phase of work rather than all of them upfront.

- `references/research-methodology.md` — Phase 1 detailed fact-finding protocol for each source type
- `references/knowledge-graph-construction.md` — Phase 2 procedure for mapping concepts and dependencies
- `references/learning-ramp-guide.md` — how to design reader ladders, use-first sequencing, and smooth learning slopes
- `references/series-patterns.md` — six common series architecture patterns with selection rules
- `references/phase-naming-guide.md` — cognitive-progression phase naming conventions and the four verbs
- `references/output-template.md` — exact outer deliverable structure and anti-duplication rules
- `references/prompt-template.md` — tech-writing prompt template with required fields and worked example
- `references/outline-quality-checklist.md` — the full validation checklist for the completed outline
- `references/example-outlines.md` — paired weak and strong outline examples on three frameworks
- `references/worked-example.md` — complete walkthrough of the workflow on a Spring AI series

---

## Final reminder

The skill's value comes from the research protocol, not the formatting. A well-formatted outline built on thin research is worse than a rough outline built on deep research, because the formatting hides the thinness from the user and from the downstream writing workflow. The research protocol is not optional. Phase 1 takes significant time on a serious topic — hours of reading, not minutes of skimming — and the output of Phase 1 is the raw material from which everything else is built. Compressing Phase 1 to save time produces the exact failure mode the skill exists to prevent, and no amount of clever outline formatting in Phase 3 will rescue a thin Phase 1. Depth does not require verbose metadata, stacked-clause titles, or inflated phase names. A good planner prompt should never force the user to append "please be deeper" or "please add Mermaid diagrams"; those obligations should already be inside the prompt.
