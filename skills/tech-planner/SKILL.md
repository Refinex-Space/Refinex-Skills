---
name: tech-planner
description: >
  Plan a complete technical blog series with cognitively sequenced articles, each containing a self-sufficient writing prompt.
  Use this skill whenever the user asks to plan, outline, or architect a multi-article technical blog series on any technology topic
  (frameworks, languages, databases, infrastructure tools, protocols, design patterns, etc.).
  Also trigger when the user mentions "系列博客规划", "技术系列文章", "blog series planning", "article series outline",
  or asks to break a broad technical topic into a structured sequence of articles.
  This skill covers the full pipeline from research through knowledge graph construction to series architecture design.
  Do NOT use for writing a single article (that is tech-writing's job), for general content calendars, or for non-technical blog planning.
---

# Tech Planner — 技术博客系列规划

## Mission

Given a technical topic, produce a complete blog series plan: cognitively sequenced articles, each with a self-sufficient writing prompt that can be handed to a downstream writing skill (tech-writing) without any additional context.

## Language Defaults

Default output: Chinese. Preserve English for technical terms (framework names, class names, method names, config keys, protocol names, CLI flags). The generated tech-writing Prompts are also in Chinese. Phase 1 research uses source materials in their original language.

---

## Five Anti-Patterns to Defeat

Every planning decision must be checked against these failure modes. The SKILL.md body gives concise definitions and detection signals. For detailed positive/negative examples and boundary cases, read `references/anti-patterns.md`.

### 1. Documentation Mirroring

The series structure copies the official docs' table of contents. Detection signal: article titles map 1:1 to doc chapters; no reordering, no opinion injection. The series must be structured around cognitive progression, not documentation chapters.

### 2. Topic-Tag Titling

Titles are noun phrases ("Spring AI 简介") instead of precise claims. But overcorrection into clickbait ("揭秘 Spring AI 的三大致命陷阱") is equally wrong. Target style: Meituan Tech Blog / Anthropic Engineering Blog — concise, accurate, editorial. Banned patterns: "揭秘", "一文读懂", "保姆级", "吊打", "颠覆认知", and all sensationalist phrasing.

### 3. Phase-as-Difficulty-Label

Phases named "基础篇 / 进阶篇 / 高级篇" describe assumed reader experience, not cognitive activity. Phases must describe what the reader is _doing_ in that stage. Read `references/phase-naming-guide.md` for naming methodology and examples.

### 4. Prerequisite Amnesia

An article references a concept not yet introduced, or the same concept is re-introduced from scratch in multiple articles. Defense: the explicit knowledge graph from Phase 2 makes dependencies visible and auditable.

### 5. Pseudo-Spiral

The series "revisits" a concept without adding complexity — that is a loop, not a spiral. Per Bruner's spiral curriculum theory, each revisit must add a new layer of complexity that the reader can feel as cognitive ascent.

---

## Mandatory Four-Phase Protocol

Phases are sequential and non-skippable. Compressing Phase 1 almost guarantees Documentation Mirroring; skipping Phase 2 almost guarantees Prerequisite Amnesia.

### Phase 1: Source Exhaustion （源头穷尽）

Systematically digest primary sources for the target technology. This is not "getting familiar" — it is exhaustive ingestion.

**You MUST use web_search and web_fetch to conduct real research.** Do not fabricate a research dossier from training data alone. Search for: official documentation, GitHub release notes, GitHub Issues/Discussions (high-frequency pain points), official blog posts and conference talks, Stack Overflow high-vote Q&A, and notable community blog posts.

Read `references/research-protocol.md` for the detailed search strategy, source priority ranking, and Research Dossier template.

**Output**: A Research Dossier listing all discovered concepts, APIs, design decisions, documented behaviors, known limitations, undocumented behaviors, version history differences, and community pain points.

**Pause point**: If research reveals version divergence or framework changes the user has not specified (e.g., Spring AI M6 vs GA), pause and ask which version to target.

### Phase 2: Knowledge Graph Construction （知识图谱构建）

Transform the Research Dossier into a concept dependency graph.

Read `references/knowledge-graph-spec.md` for node type definitions, edge type definitions, dependency annotation rules, and gap analysis methodology.

**Output**: A Concept Dependency Map with nodes (concepts), directed edges (prerequisites), and annotations marking gaps between official narrative and actual behavior.

**Pause point**: If the graph reveals prerequisite knowledge the user has not mentioned (e.g., planning a Spring AI series requires understanding of Spring Boot auto-configuration that the user may or may not want to assume), pause and ask about reader prerequisite assumptions.

### Phase 3: Series Architecture Design （系列架构设计）

Transform the knowledge graph into a cognitively sequenced article series.

Steps:

1. **Select architecture pattern(s)**: Read `references/series-architecture-patterns.md` and select the pattern (or pattern combination) best suited to the topic. Mixed patterns across phases are supported — explain the rationale for each phase's pattern choice.
2. **Define phases with cognitive-action names**: Use `references/phase-naming-guide.md`. Each phase gets a name describing the reader's cognitive activity in that stage, plus a capability statement (what the reader can do after completing the phase).
3. **Sequence articles within phases**: Respect the dependency edges from the knowledge graph. Each article introduces no more than 3-4 new core concepts.
4. **Write article specifications**: For each article, produce all required fields (see Output Specification below).
5. **Generate tech-writing Prompts**: For each article, produce a complete, self-sufficient prompt following the template in `references/prompt-template.md`. Every field is mandatory. The prompt must work in isolation — a user copying it weeks later to a writing skill should need zero additional context.

### Phase 4: Validation （质量校验）

Run the output through the quality gate checklist before delivering to the user.

Read `references/validation-checklist.md` for the complete checklist. At minimum, verify: no Documentation Mirroring, no Topic-Tag Titling, no Phase-as-Difficulty-Label, no Prerequisite Amnesia, no Pseudo-Spiral, all Prompts self-sufficient with every template field filled, all core knowledge graph nodes covered, cognitive jumps between adjacent articles within threshold, series boundary consistency, and title style consistency.

If any gate fails, revise the affected articles and re-validate before delivery.

---

## Output Specification

The delivered planning document must contain these sections:

### Series Header

- Topic name and version (if applicable)
- Total scope and explicit boundaries (what is covered, what is not)
- Target reader profile and prerequisite knowledge assumptions
- Estimated total article count and phase breakdown

### Per-Phase Block

- Phase number and cognitive-action name (never "基础/进阶/高级")
- Architecture pattern used in this phase (from the pattern library)
- Capability statement: what the reader can do after completing this phase

### Per-Article Block

- Article number and concise thesis-driven title (Chinese, Meituan Tech Blog style)
- Central thesis: one falsifiable claim
- Key technical anchors: what real data, failure mechanisms, rejected alternatives, or boundary conditions are needed
- Prerequisite article dependencies: which prior articles are required and which concepts from them
- Visual plan: which mechanisms need diagrams, recommended Mermaid diagram types, what each diagram should reveal
- Complete tech-writing Prompt: formatted per `references/prompt-template.md`, ready to copy-paste

---

## When to Pause and Ask the User

Three situations require stopping and asking:

1. **Topic too broad**: "Kubernetes" needs narrowing to a subsystem (networking, scheduling, storage, etc.). "Spring Boot" needs narrowing to a specific concern (auto-configuration, testing strategy, production readiness, etc.).
2. **Topic too narrow**: A single annotation or utility class does not warrant a series. Suggest single-article treatment or scope expansion.
3. **Ambiguous version or prerequisite**: Research reveals version splits the user did not address, or the knowledge graph requires prerequisite knowledge the user did not mention.

When pausing, state the specific ambiguity, present concrete options, and recommend one. Do not ask open-ended questions.

---

## Reference Files

Read these as needed during execution. Do not preload all of them at once.

| File                                         | When to read                                  |
| -------------------------------------------- | --------------------------------------------- |
| `references/research-protocol.md`            | At the start of Phase 1                       |
| `references/knowledge-graph-spec.md`         | At the start of Phase 2                       |
| `references/series-architecture-patterns.md` | At the start of Phase 3, step 1               |
| `references/phase-naming-guide.md`           | At Phase 3, step 2                            |
| `references/prompt-template.md`              | At Phase 3, step 5                            |
| `references/validation-checklist.md`         | At Phase 4                                    |
| `references/anti-patterns.md`                | Whenever an anti-pattern boundary case arises |
| `references/examples/spring-ai-excerpt.md`   | When you need a concrete output example       |
