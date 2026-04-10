---
name: tech-writing
description: Write technical blog posts, architecture design docs, Architecture Decision Records (ADRs), technology comparisons (X vs Y), source code and mechanism deep-dives, API documentation, and migration guides — the blank-page case where the user has a technical argument or decision to document but no existing draft. Use this skill whenever the user asks for writing like "write a blog post about", "draft an ADR for", "compare X and Y", "deep-dive into the source of", "write a design doc for", "author an API reference", "write up a post-mortem / migration guide", or similar — even if they do not name the skill. Default output language is Chinese with technical terms kept in English; switch to English only when the user explicitly requests it. This skill enforces a mandatory pre-writing anchor-gathering protocol before any prose is generated, because AI technical writing fails by sliding into encyclopedic description when it lacks concrete numbers, specific failure mechanisms, and rejected alternatives.
---

# tech-writing

A skill for blank-page technical writing. The user has a topic, argument, or decision in their head, but no existing draft. This skill exists to stop one failure mode: **anchor hunger** — the default AI slide into encyclopedic prose that describes _what things are_ and never judges _what they mean_.

The cure is not stylistic. It is procedural. Anchors are gathered **before** drafting, a narrative voice is locked in **before** drafting, and the draft is then checked against non-negotiable quality gates **before** delivery.

---

## The failure mode this skill fights

Without this skill, given "write a blog post about Spring AI's `ChatClient`", a model typically produces: a history paragraph, a "what is" paragraph, a feature list, a hello-world example, and a "conclusion" that says both old and new approaches have pros and cons. Nothing in that output requires having ever used `ChatClient` in production. Nothing is falsifiable. The reader learns no more than they would from the README.

The pattern has a name here: **encyclopedic drift**. It happens when the writer (human or model) has not gathered enough concrete technical material to have an argument, so the writing compensates by becoming comprehensive instead of sharp. This skill's job is to prevent that — by forcing the argument and the anchors to exist _on paper_ before the first sentence of prose.

---

## Workflow

Every task under this skill follows the same three phases. Do not skip ahead. Do not start drafting during Phase 1.

```
Phase 1: PRE-WRITING PROTOCOL   → produces an Anchor Sheet
Phase 2: DRAFTING               → produces a draft under one locked voice
Phase 3: VALIDATION LOOP        → checks against gates, revises, repeats
```

### Phase 1 — Pre-writing protocol (MANDATORY; do not skip)

Before writing any prose, produce an **Anchor Sheet**. This is an internal working document — show it to the user at the start so they can correct missing or wrong anchors. The five steps:

1. **Central argument.** Write one sentence. It must be falsifiable and defensible. "Spring AI's `ChatClient` is a thoughtful abstraction" is not an argument — it cannot be falsified. "Spring AI's `ChatClient` improves ergonomics for synchronous chat but leaks abstraction the moment you need tool-call streaming, and the leak is in `AdvisorChain`, not in the fluent API" is an argument. If you cannot write the sentence, you do not yet have a piece to write — ask the user for more context before proceeding.

2. **Technical anchors.** Gather at least:
   - **Real numbers**: latency, throughput, memory, version numbers, error rates, code sizes, config values, thresholds. "A lot" and "significantly" are not numbers.
   - **Specific failure mechanisms**: not "it can fail under load" but "under >200 concurrent requests, the default `SimpleVectorStore` rebuilds its in-memory index on every insert, which is O(n) per write and dominates CPU by ~40%".
   - **Rejected alternatives with reasons**: what else was considered, and precisely why each was set aside.
   - **Boundary conditions with thresholds**: where does the claim stop being true? ("This pattern holds up to ~10k rows per partition; beyond that, Cassandra's tombstone scan cost overtakes the read path.")

3. **Reader audit.** Who is the reader? What do they already know (so you don't waste their time)? What do they probably *mis*know (so you correct it early)? A Java backend engineer reading a Spring AI post already knows what a bean is — spending two paragraphs explaining IoC is an insult to their time and a tell that you have nothing to say.

4. **Scope boundary.** Write two lists: "in scope" and "explicitly not in scope". The second list is the more important one. It is how you earn the right to ignore things without the reader feeling cheated.

5. **Voice selection.** Pick exactly one narrative voice from the catalog in `references/narrative-voices.md` and commit to it for the whole piece. Voice is not tone; it is the stance from which the piece is argued.

If any of the five is thin — especially real numbers or rejected alternatives — **stop and tell the user**. Say what is missing. Offer options: (a) the user supplies the missing anchors, (b) you run specific lookups with tools, (c) the piece is narrowed so the missing anchor is no longer needed. Never paper over a missing anchor with generic prose.

For the detailed protocol with worked examples, read `references/pre-writing-protocol.md`.

### Phase 2 — Drafting

Only after the Anchor Sheet is complete and any gaps have been resolved:

1. **Pick the document type** and read the corresponding reference file (see the table below). Each doc type has its own required structure — do not improvise structure for ADRs, design docs, or API reference. For blog posts and deep-dives the structure is more flexible but still anchored.
2. **Write in the selected voice only.** If you feel the voice shifting mid-draft (for example, from "Design Tribunal" into "Mechanism Autopsy" because you got interested in the internals), stop and decide: either the piece is actually a different voice and you restart the draft, or this is drift and you rein it back in. Voice drift is a leading cause of muddy technical writing.
3. **Apply the 60-second rule**: the opening paragraph must state the central argument. A reader who stops after 60 seconds should still know what you are claiming. No throat-clearing. No "In recent years, as AI has grown in importance…". No background stuffing.
4. **Apply the title rule**: the title carries the argument, not a topic tag. "Spring AI ChatClient 实战" is a topic. "Spring AI ChatClient 的抽象只在同步场景成立:AdvisorChain 在流式 tool-call 下的四种裂缝" is an argument.

### Phase 3 — Validation loop

Before delivering the draft to the user, run it against the checklist in `references/quality-checklist.md`. This is an **executable** loop: read each gate, check the draft, and fix what fails before moving on. Do not merely "consider" the gates — actually verify each one against the prose. The gates are tight enough that a first draft will usually fail two or three of them; that is expected and is the point of the loop. Revise and re-run until the draft passes every gate.

If you deliver a draft without running the checklist, you have not used this skill. It is the checklist that makes the skill work.

---

## Document type selection

Pick the type first; structure follows. When in doubt between types, ask the user — do not blend structures.

| The user wants to…                                                       | Document type                      | Reference file                          |
| ------------------------------------------------------------------------ | ---------------------------------- | --------------------------------------- |
| Publish a technical argument or war story to a general engineer audience | Technical blog post                | `references/doctype-blog-post.md`       |
| Record a specific architecture choice with its rationale                 | ADR (Architecture Decision Record) | `references/doctype-adr.md`             |
| Propose a new system or major change for review                          | Design document                    | `references/doctype-design-doc.md`      |
| Compare two or more technologies and recommend one                       | Technology comparison              | `references/doctype-comparison.md`      |
| Walk through source code, protocol internals, or a mechanism             | Deep-dive / mechanism autopsy      | `references/doctype-deep-dive.md`       |
| Document an API for developers consuming it                              | API reference                      | `references/doctype-api-doc.md`         |
| Guide readers through an upgrade, migration, or adoption                 | Migration field guide              | `references/doctype-migration-guide.md` |

Each reference file contains the required sections, ordering rules, examples, and type-specific quality rules. Read the relevant file before drafting — do not rely on memory of "what an ADR usually looks like".

The Diátaxis four-quadrant distinction (tutorial / how-to / reference / explanation) is a useful cross-cutting lens: before picking a doc type, ask yourself which quadrant the reader is in. API reference is reference. A migration guide is a how-to. A deep-dive is explanation. Blending quadrants in one document is a reliable way to make it good at nothing. More on this in `references/doctype-blog-post.md` and `references/doctype-api-doc.md`.

---

## Narrative voices (pick exactly one per document)

A voice is a consistent stance — what the writer is doing with the material. Voice drift is a top anti-pattern. Pick one and commit. The four primary voices:

- **Production War Story** — post-mortem, operational lesson. The writer lived through an incident and is teaching the reader what the system actually did, not what the docs said it would do. Opens with a symptom, ends with a structural lesson.
- **Design Tribunal** — architecture decisions and technology comparisons. The writer is sitting in judgment. Every claim must be falsifiable. Every alternative must be named and set aside for a specific reason. No "both have pros and cons" verdicts.
- **Mechanism Autopsy** — source code deep-dives, protocol analysis. The writer has opened the thing up and is walking the reader through the internals. Authority comes from specificity: exact file paths, exact line numbers, exact call chains.
- **Migration Field Guide** — upgrade guides, adoption playbooks. The writer has done the migration and is handing the reader a map, complete with the pits they fell into. Tense is imperative; scope is ruthlessly bounded.

Two secondary voices for completeness:

- **Benchmarker's Notebook** — for performance comparison pieces where the whole point is the numbers and the methodology. Authority comes from reproducibility.
- **Reference Librarian** — for pure API reference and spec documentation. Authority comes from completeness and consistency, not argument. This is the only voice where "just describe what the thing does" is acceptable, because the reader is not looking for an argument.

For each voice, a before/after example showing generic AI output vs. output in that voice is in `references/narrative-voices.md`. Read that file whenever you are unsure which voice fits, or you suspect your draft has drifted.

---

## Non-negotiable quality gates (summary)

These are enforced by `references/quality-checklist.md`. The summary is here so you know the bar before you start drafting.

**Structure:**

- Title states the argument, not the topic.
- Header info block present: scope, prior knowledge assumed, central argument.
- 60-second rule: the central argument appears in the opening paragraph.
- Every comparison section ends with a clear verdict. "Both have pros and cons" is a failure.
- Every design decision includes rejected alternatives and specific reasons.

**Depth:**

- Failure modes name specific mechanisms, not general categories.
- A limitations / boundary section exists with concrete thresholds.
- **Senior-engineer test**: for every section, ask "does this teach a senior engineer anything they couldn't get from the official docs in five minutes?" If no, cut or deepen the section. There is no third option.

**Language:**

- For Chinese output: technical terms (class names, config keys, protocol names, CLI flags, metric names) stay in English. Tone is _senior engineer explaining to a peer in a design review_, not "小白教程". Argument-first sentence structure. No 引言式废话 ("在当今这个…的时代").
- For English output: prefer Anglo-Saxon vocabulary over Latinate ("use" not "utilize", "start" not "commence"). Active voice by default. Present tense for behavior. Precision over concision — if the precise version is longer, ship the precise version.

**Anti-patterns (kill on sight):** false balance, empty superlatives, background stuffing, passive responsibility avoidance, hedge stacking, bullet-point avoidance-of-prose, Wikipedia-voice opening, restating the question, "comprehensive guide" framing. Full catalog with examples in `references/anti-patterns.md`.

---

## When to stop and ask the user

This skill is high-freedom for _how_ to write, but strict about _what to write about_. Stop and ask the user, before drafting, when any of the following is true:

1. You cannot state the central argument in one falsifiable sentence.
2. You have no real numbers, and the piece claims anything about performance, cost, or scale.
3. You can name the chosen solution but not the rejected alternatives, and the piece is an ADR, design doc, or comparison.
4. The user's request is actually two pieces glued together (for example, "compare X and Y and also walk through the source code of X") — propose splitting it.
5. The reader is ambiguous — a piece aimed at both beginners and senior engineers will serve neither.

Asking is not a failure. Papering over the gap with generic prose is the failure.

---

## Output language defaults

- Default: **Chinese**, with all technical terms kept in English (class names, method names, protocol names, config keys, CLI flags, metric names, library names, error codes, HTTP status codes).
- Switch to English only when the user explicitly asks for English, or the document type is "API reference for an English-speaking audience".
- Never machine-translate technical terms into Chinese (不要写"弹簧 AI 聊天客户端"). Never mix — if the output is Chinese, headings, prose, and captions are Chinese; only technical tokens stay English.
- Full language conventions, including punctuation, spacing between Chinese and English, and quotation rules, in `references/language-conventions.md`.

---

## Reference file map

All reference files are one level below `SKILL.md`. Read the file when its topic is relevant to the current task — don't read them all upfront.

- `references/pre-writing-protocol.md` — detailed Anchor Sheet protocol with worked examples
- `references/narrative-voices.md` — six voices, before/after examples per voice, drift diagnostics
- `references/anti-patterns.md` — full AI-scented anti-pattern catalog with detection heuristics
- `references/quality-checklist.md` — executable validation loop; run before every delivery
- `references/language-conventions.md` — Chinese and English writing conventions
- `references/doctype-blog-post.md` — technical blog post structure
- `references/doctype-adr.md` — ADR structure (Nygard + MADR variants)
- `references/doctype-design-doc.md` — architecture design document structure (Google-style)
- `references/doctype-comparison.md` — X vs Y technology comparison structure
- `references/doctype-deep-dive.md` — source code / mechanism autopsy structure
- `references/doctype-api-doc.md` — API reference structure
- `references/doctype-migration-guide.md` — migration and upgrade guide structure

---

## Final reminder

The entire skill rests on one load-bearing claim: **anchors first, prose second**. If a draft is weak, the fix is almost never "rewrite the prose". The fix is almost always "the Anchor Sheet was thin; go back and fill it in". When the anchors are real, the prose almost writes itself. When the anchors are fake, no amount of prose polish will save the piece.
