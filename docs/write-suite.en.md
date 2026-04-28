# Write Skills — Technical Writing Suite

## Design Background: Why Three Skills, Not One

Technical writing fails in more than one way, and each failure mode requires its own procedural defense.

It seems reasonable to handle "write me a technical blog post" and "rewrite these meeting notes into a technical blog post" with the same skill — after all, both produce the same deliverable. But the core risk of each task is entirely different. In the first case, the risk is **anchor hunger**: without concrete technical anchors (real numbers, specific failure mechanisms, rejected alternatives), AI output slides into encyclopedic description that tells the reader what things are without ever judging what they mean. In the second case, the risk is **style contamination**: the source material's structure, tone, gaps, and hedges leak into the output through specific, measurable mechanisms, even when the writer explicitly intends to improve the source.

A third scenario — "I want to write a series about Spring AI, help me plan it" — introduces a third risk: **surface skating**, where the generated series outline looks comprehensive but actually mirrors the official documentation's table of contents rather than reflecting how the knowledge actually builds in a reader's head.

Three skills address three distinct problems, but they share a single set of quality standards. That standard now also has a dedicated `mermaid-diagrams` layer for turning visual plans into stable, restrained, Markdown-portable Mermaid. This is the central design decision: regardless of which path produced the content, the final document must be indistinguishable in quality, and its diagrams must not drift into separate house styles.

---

## The Three Skills and Their Roles

### mermaid-diagrams — Shared diagram execution layer

The problem it solves: once a document decides that it needs a Mermaid diagram, the hard part is no longer "pick a Mermaid type". The hard part is writing Mermaid that stays syntax-correct, renderer-portable, visually restrained, and free of crowding.

The core defense is the Portable Authoring Standard. The skill locks the reader question and diagram type first, designs the geometry and node budget second, writes in a lowest-risk Markdown Mermaid subset third, and only then adds minimal semantic styling when it materially helps. Good-looking diagrams come primarily from structure, direction, label discipline, and split decisions, not decorative color.

### tech-writing — Blank-Page Composition

The problem it solves: the user has a technical argument or decision to document but no existing draft. This is the from-scratch case.

The core defense is the Pre-writing Protocol. Before any prose is generated, the skill requires an Anchor Sheet containing five elements: a central argument (one falsifiable sentence), technical anchors (real numbers, specific failure mechanisms, rejected alternatives with reasons, boundary conditions with thresholds), a reader audit (who the reader is, what they already know, what they probably misunderstand), scope boundaries (what is covered and what is explicitly not covered), and a narrative voice selection. When the Anchor Sheet is thin, the skill refuses to proceed to the drafting phase instead of papering over the gap with generic prose.

Supported document types: technical blog posts, Architecture Decision Records (ADRs), architecture design documents, technology comparisons, source code deep-dives, API reference documentation, and migration guides.

### tech-rewrite — Reconstruction from Existing Material

The problem it solves: the user has existing material of any quality — internal notes, meeting minutes, AI-generated drafts, legacy wiki pages, code comments — that needs to be transformed into high-quality technical documentation.

The core defense is the Extraction Firewall. Reading the source material and writing the output are strictly separated activities. The Fact Register serves as the only permitted bridge between the two phases. It has four sections: KEPT (every concrete, verifiable claim from the source, rewritten in the extractor's own words), DISCARDED (every vague or unsupported claim, with a specific reason for rejection), MISSING (every piece of information a strong document would need but the source does not supply), and AMBIGUOUS (every claim whose meaning cannot be determined without guessing). After extraction, the source is closed and all further work proceeds from the Fact Register alone.

The skill identifies and defends against ten contamination mechanisms: Structural Mirroring, Void Inheritance, Ambiguity Whitewashing, Tone Infiltration, Rationale Vacuum, False Completeness, Scope Inflation, Confidence Upgrade, Terminology Drift, and Pseudoanchor Import. Each mechanism has its own detection heuristic and defense strategy.

### tech-planner — Series Strategy

The problem it solves: the user names a technical target (a framework, library, protocol, or broad topic) and needs a comprehensive, cognitively sequenced plan for writing a series of high-quality articles about it.

The core defense is the Three-Phase Research Protocol. Phase 1 is Source Exhaustion — the systematic consumption of official documentation, source code, release notes, GitHub issues, and authoritative secondary sources. Phase 2 is Knowledge Graph Construction — mapping concepts, prerequisite relationships, aha-moment dependencies, and the gaps between the official narrative and real-world usage patterns. Phase 3 is Series Architecture Design — translating the knowledge graph into a cognitively ordered sequence of articles, each with an argument-carrying title and a ready-to-paste prompt for tech-writing.

The series architecture follows Bruner's spiral curriculum principle: a genuine spiral revisits concepts at increasing levels of complexity, while a loop merely repeats. The skill's twelve-gate quality checklist verifies before delivery that the outline does not mirror the official documentation, that every article title carries an argument rather than a topic tag, that phase names reflect cognitive progression rather than difficulty labels, and that prerequisite dependencies are respected across the article sequence.

---

## How the Three Skills Work Together: The Pipeline

The three skills form a pipeline where each stage's output is the next stage's input, with `mermaid-diagrams` acting as a shared execution layer wherever a visual plan needs to become actual Mermaid:

```
tech-planner
    │  Output: Series outline + one tech-writing prompt per article
    ▼
tech-writing (blank page)  ◄─or─►  tech-rewrite (existing material)
    │                                   │
    │  Output: Publication-quality       │  Output: Publication-quality
    │          technical document        │          technical document
    │                                   │
    └───── Shared quality standards ────┘
                     │
                     ▼
             mermaid-diagrams
        executes any Mermaid visual plan
```

The convergence point is the Anchor Sheet. The tech-writing skill's Phase 1 produces the Anchor Sheet directly. The tech-rewrite skill's Phase 2 produces the Anchor Sheet from the Fact Register. The tech-planner's per-article prompts contain enough information for the tech-writing skill's Phase 1 to populate its Anchor Sheet automatically. All three paths converge at the same format, and from that point forward, the writing and validation workflow is identical.

This means that if you only need to write a single article, you use tech-writing or tech-rewrite directly — tech-planner is not needed. If you are planning a series, you start with tech-planner and then execute each article through tech-writing or tech-rewrite. If you are unsure which skill to use, consult the selection guide below.

## Notion Agent Version

The repository also includes Notion-native page versions for running the same writing workflows inside Notion Agent:

- `notion/skills/tech-planner.md`
- `notion/skills/tech-writing.md`
- `notion/skills/tech-rewrite.md`
- `notion/instructions/writing-agent.md`

These files are not Codex `SKILL.md` files. They are pages you copy into Notion and mark as AI Skills or AI Instructions. Setup and usage docs: [docs/reference/notion/README.md](reference/notion/README.md).

---

## Skill Selection Guide

| Your scenario | Skill to use |
|---------------|-------------|
| You have a technical argument but no draft, and you want one article | tech-writing |
| You have existing notes, drafts, or docs that need transformation | tech-rewrite |
| You want to plan a multi-article blog series | tech-planner |
| You have a prompt from tech-planner and want to start writing | tech-writing |
| You have a prompt from tech-planner plus existing material on the topic | tech-rewrite |
| You already know what the diagram should explain and only need to turn the visual plan into stable Mermaid | mermaid-diagrams |
| You have a published article and want to rewrite it based on reader feedback | tech-rewrite |
| You want to compare two technologies and reach a verdict | tech-writing |
| You have an old comparison document and need to update it for new versions | tech-rewrite |
| You want to write a post-mortem | tech-writing |
| You have an incident report draft and want to turn it into a post-mortem blog | tech-rewrite |

The decision rule happens in two layers. First ask whether you are writing or simply rendering a Mermaid visual plan. If the job is only the Mermaid diagram, use `mermaid-diagrams`. If you are writing, then ask whether you already have source material: if yes, use `tech-rewrite`; if no, use `tech-writing`; if you need to plan a series, use `tech-planner` first.

---

## Shared Quality Standards

The three skills share a single set of quality rules. tech-writing defines them, tech-rewrite inherits them through literal copies of the `shared-*` reference files, and tech-planner ensures downstream quality by generating prompts that conform to the same standards. `mermaid-diagrams` then owns the shared Mermaid syntax, layout, and restrained styling standard so the writing skills do not each invent their own diagram habits.

Every document produced by any skill must pass the following non-negotiable gates:

**Structural standards.** The title carries the argument, not a topic label. A header info block is present, stating scope, assumed prior knowledge, and central argument. The 60-second rule applies: the opening paragraph states the central argument. Every comparison section ends with a clear verdict — "both have pros and cons" is a failure. Every design decision includes rejected alternatives with specific reasons for rejection.

**Depth standards.** Failure modes describe specific causal mechanisms, not general categories. A limitations section exists with concrete thresholds and boundary conditions. The senior-engineer test applies to every section: if a section does not teach a senior engineer in the target domain anything beyond what the official docs provide in five minutes, it is either deepened or deleted.

**Language standards.** For Chinese output, technical terms (class names, method names, configuration keys, protocol names, CLI flags, metric names) remain in English. The register is a senior engineer explaining to a peer in a design review — not a tutorial, not marketing, not a beginner's guide. For English output, Anglo-Saxon vocabulary is preferred over Latinate (use, not utilize; start, not commence), active voice is the default, and present tense is used for describing behavior.

**Anti-pattern defense.** A catalog of twenty AI-characteristic anti-patterns is swept against every draft: false balance, empty superlatives, background stuffing, passive responsibility avoidance, hedge stacking, Wikipedia-voice opening, restating the question, "comprehensive guide" framing, bullet-point avoidance of prose, encyclopedic drift, missing rejected alternatives, hand-waving internals, tutorial voice in non-tutorial pieces, the restating conclusion, meta-references to the piece itself, unsynthesized tradeoff lists, present-tense-about-the-future, context-free best practices, invented precision, and the senior-engineer-insulting paragraph.

---

## The Six Narrative Voices

Every document must select a single narrative voice before drafting begins, and the voice must be maintained consistently throughout. A voice is not tone (formal versus casual) — it is stance, the relationship between the writer and the material.

**Production War Story** — post-mortems and operational lessons. Opens with a symptom, ends with a structural lesson. Authority comes from the specificity of the incident.

**Design Tribunal** — architecture decisions and technology comparisons. Weighs options against explicit criteria and delivers a verdict. The cardinal sin of this voice is "both have pros and cons."

**Mechanism Autopsy** — source code deep-dives and protocol analysis. Walks the reader through internals with code-level precision: file paths, line numbers, version tags. Authority comes from specificity.

**Migration Field Guide** — upgrade guides and adoption playbooks. Written in imperative mood, centered on the pits the writer fell into. Every migration guide ends with a rollback plan.

**Benchmarker's Notebook** — performance comparisons where the whole point is the numbers. Authority comes from reproducibility: the reader can copy the commands and land on the same results.

**Reference Librarian** — pure API reference and spec documentation. No arguments, no opinions. Authority comes from completeness and consistency. The only voice where "just describe what the thing does" is correct.

---

## Recommended Usage Templates

### Template 1: Writing a Single Article from Scratch

```
Write a technical blog post about [topic].

Central argument: [one falsifiable sentence]
Target reader: [specific description including existing knowledge and likely misconceptions]
Narrative voice: [one of the six voices]
```

The tech-writing skill will produce an Anchor Sheet first, show it to you for confirmation, and only then proceed to drafting. If the argument is not sharp enough or the anchors are insufficient, the skill will tell you what is missing and propose options for filling the gap.

### Template 2: Rewriting Existing Material

```
Rewrite the following material into a [document type]:

[paste source material]

Target reader: [specific description]
Target document type: [blog post / ADR / design doc / comparison / deep-dive / API doc / migration guide]
```

The tech-rewrite skill will produce a Fact Register first, showing you exactly what was kept, what was discarded and why, what is missing, and what is ambiguous. You confirm or adjust before the writing phase begins.

### Template 3: Planning a Blog Series

```
Plan a technical blog series about [framework/library/protocol name].

Target version: [specific version number]
Target reader: [specific description including the technical background they are coming from]
Series goal: [what the reader should be able to do after finishing the series]
```

The tech-planner skill will conduct deep research, build a knowledge graph, and produce a detailed series outline. Each article in the outline comes with a complete tech-writing prompt that can be copied directly into the tech-writing skill to begin drafting.

### Template 4: Executing a Series Article

Once tech-planner produces an outline, execute each article by copying the prompt block directly:

```
[paste the prompt block from the outline — it starts with /tech-write and includes <prompt> tags]
```

Each prompt block contains the central argument, narrative voice, technical anchors, reader profile, prerequisite knowledge, scope boundaries, and reference links. No editing is needed before pasting.

---

## Seven Document Types and Their Structures

The three skills share structural definitions for seven document types. Each type has its own required sections, ordering rules, and type-specific quality gates.

| Document Type | Typical Voice | Core Structural Requirements |
|--------------|---------------|------------------------------|
| Technical blog post | Any except Reference Librarian | Argument-carrying title, hook opening, 60-second rule, one of four ending moves |
| ADR | Design Tribunal | Title / Status / Context / Decision / Consequences, "We will..." voice in Decision |
| Design document | Design Tribunal (neutral) | Goals / Non-goals, Detailed Design, Alternatives Considered, Cross-cutting Concerns |
| Technology comparison | Design Tribunal | Explicit criteria list, per-criterion evaluation, qualified verdict, flip conditions |
| Source code deep-dive | Mechanism Autopsy | Version tagging, code anchors (file path + line number), ends on a reusable mental model |
| API reference | Reference Librarian | Identical layout across all endpoints, exhaustive error listing, working examples |
| Migration guide | Migration Field Guide | "Do not migrate if..." section, pit list, rollback plan, verification steps |

---

## A Note on Quality Consistency

The quality consistency across the three skills is not aspirational — it is structural. The mechanism is worth understanding because it explains why the guarantee holds.

**A single quality checklist.** The tech-writing skill defines thirteen quality gates (Gate 0 through Gate 12). The tech-rewrite skill inherits the same checklist through a literal file copy (`shared-quality-standards.md`). Both skills run physically the same validation loop in their respective Phase 3 / Phase 4.

**A single anti-pattern catalog.** Twenty AI-characteristic anti-patterns are cataloged in `shared-anti-patterns.md`, and both skills sweep the same catalog in Gate 9.

**A single voice catalog.** Six narrative voices are defined in `shared-narrative-voices.md` with before/after examples and drift diagnostics. Both skills reference the same file.

**A single language convention set.** Chinese and English writing conventions are defined in `shared-language-conventions.md`. The rules for keeping technical terms in English, for spacing between Chinese and English text, for punctuation, and for register are the same in both skills.

**A single set of document-type definitions.** Seven document types are defined in seven `shared-doctype-*.md` files. Both tech-writing and tech-rewrite read the same set of files.

**The Anchor Sheet as the convergence point.** The tech-writing skill's Phase 1 produces the Anchor Sheet directly. The tech-rewrite skill's Phase 2 produces the Anchor Sheet from the Fact Register. The tech-planner's prompts contain enough information for the tech-writing Phase 1 to fill its Anchor Sheet automatically. All three paths converge on the same format. From that point forward, the writing and validation workflow is identical. A reader who sees only the Anchor Sheet cannot tell which skill produced it, and that is by design.

The practical implication: if you are satisfied with the quality of an article produced by tech-writing, you can expect the same quality from tech-rewrite on the same topic, and vice versa. The two skills differ only in their input stage — one starts from scratch, the other starts from source material — and they converge entirely in their output stage.

---

## Skill File Inventory

### mermaid-diagrams (6 files)

```
mermaid-diagrams/
├── SKILL.md                              # Entry point: shared Mermaid execution standard
├── agents/
│   └── openai.yaml                       # UI metadata and default invocation prompt
└── references/
    ├── authoring-standard.md             # Portable syntax subset and parser-risk rules
    ├── styling-standard.md               # Restrained palette and minimal styling discipline
    ├── pattern-cookbook.md               # Per-diagram-type defaults
    └── final-checklist.md                # Last-pass validation gates
```

### tech-writing (14 files)

```
tech-writing/
├── SKILL.md                              # Entry point: workflow, pre-writing protocol, quality summary
└── references/
    ├── pre-writing-protocol.md           # Anchor Sheet protocol with worked examples
    ├── narrative-voices.md               # Six voices with before/after examples
    ├── quality-checklist.md              # Thirteen quality gates (executable validation loop)
    ├── anti-patterns.md                  # Twenty AI-characteristic anti-pattern catalog
    ├── language-conventions.md           # Chinese and English writing conventions
    ├── doctype-blog-post.md             # Blog post structure
    ├── doctype-adr.md                   # ADR structure (Nygard + MADR)
    ├── doctype-design-doc.md            # Design document structure (Google-style)
    ├── doctype-comparison.md            # Technology comparison structure
    ├── doctype-deep-dive.md             # Source code deep-dive structure
    ├── doctype-api-doc.md               # API reference structure
    └── doctype-migration-guide.md       # Migration guide structure
```

### tech-rewrite (18 files)

```
tech-rewrite/
├── SKILL.md                              # Entry point: extraction workflow, contamination, standards
└── references/
    ├── contamination-mechanisms.md       # Ten mechanisms with before/after examples
    ├── extraction-protocol.md           # Fact Register methodology with worked examples
    ├── fact-register-template.md        # Working template for the Fact Register
    ├── contamination-risk-assessment.md # Diagnostic tool for Phase 1
    ├── rewrite-checklist.md             # Rewrite-specific gates (Gate R1–R10)
    ├── shared-quality-standards.md      # ← literal copy from tech-writing
    ├── shared-narrative-voices.md       # ← literal copy from tech-writing
    ├── shared-anti-patterns.md          # ← literal copy from tech-writing
    ├── shared-language-conventions.md   # ← literal copy from tech-writing
    ├── shared-diagram-selection-guide.md # ← literal copy from tech-writing
    ├── shared-doctype-blog-post.md      # ← literal copy from tech-writing
    ├── shared-doctype-adr.md            # ← literal copy from tech-writing
    ├── shared-doctype-design-doc.md     # ← literal copy from tech-writing
    ├── shared-doctype-comparison.md     # ← literal copy from tech-writing
    ├── shared-doctype-deep-dive.md      # ← literal copy from tech-writing
    ├── shared-doctype-api-doc.md        # ← literal copy from tech-writing
    └── shared-doctype-migration-guide.md # ← literal copy from tech-writing
```

### tech-planner (9 files)

```
tech-planner/
├── SKILL.md                              # Entry point: three-phase research protocol, architecture
└── references/
    ├── research-methodology.md          # Phase 1 fact-finding protocol for each source type
    ├── knowledge-graph-construction.md  # Phase 2 concept dependency mapping
    ├── series-patterns.md               # Six series architecture patterns with selection rules
    ├── phase-naming-guide.md            # Cognitive-progression naming conventions and four verbs
    ├── prompt-template.md               # tech-writing prompt template with worked example
    ├── outline-quality-checklist.md     # Twelve outline validation gates
    ├── example-outlines.md              # Paired weak/strong outlines for three frameworks
    └── worked-example.md                # Complete Spring AI series walkthrough
```
