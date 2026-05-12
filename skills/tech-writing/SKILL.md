---
name: tech-writing
description: >
  Write a single rigorous mid-to-long-form technical blog article from a user topic, writing intent, draft prompt, or tech-planner handoff.
  Use this skill for professional engineering articles, architecture explainers, mechanism deep dives, production postmortems, technology comparisons,
  framework/API analysis, and article drafting requests that require a falsifiable thesis, concrete technical anchors, diagrams, and anti-AI-slop validation.
  Do NOT use for multi-article series planning, general content calendars, marketing copy, API reference documentation, or short social posts.
---

# Tech Writing

## Mission

Write one professional technical blog article at the level of Meituan Tech Blog, Anthropic Engineering Blog, or OpenAI Developer Blog. The article must make a falsifiable technical claim, prove it with concrete anchors, and avoid encyclopedic, template-shaped, AI-flavored prose.

Default output is Chinese. Preserve English for technical terms, API names, class names, config keys, error names, protocol names, commands, and version identifiers.

## Hard Gate

Do not start Phase 2 drafting until Phase 1 has produced an Anchor Sheet and the user has explicitly confirmed it. A complete prompt from `tech-planner` may compress Phase 1, but it never removes the confirmation gate.

If the user asks to "just write it" before the Anchor Sheet is confirmed, explain that this skill requires a brief pre-writing confirmation and present the shortest viable Anchor Sheet.

## Three-Phase Workflow

### Phase 1: Collaborative Pre-Writing

Start by reading `references/prewriting-protocol.md`.

Produce an initial Anchor Sheet instead of asking generic open-ended questions. Use the user's request, any supplied `tech-planner` prompt, and targeted research to fill six dimensions:

1. Central thesis: one falsifiable judgment that can appear in the opening paragraph.
2. Technical anchors: concrete data, failure mechanisms, version behavior, rejected alternatives, trade-off thresholds, boundary conditions, source links, or code-level facts.
3. Reader profile: what the target reader already knows, what they may misunderstand, and what the article should not explain from scratch.
4. Scope boundary: in-scope and explicitly out-of-scope lists.
5. Visual plan: load-bearing mechanisms, topologies, lifecycles, timelines, or comparisons that need diagrams.
6. Narrative strategy: the selected strategy from `references/narrative-strategies.md`, or a justified hybrid.

Use current sources when facts may have changed, when library/API behavior matters, or when the article depends on version-specific details. Use Context7 MCP for library/API documentation when available; use web search/fetch for official docs, release notes, issue discussions, benchmarks, and primary sources.

Expose weak spots. If anchors are missing or the thesis is not falsifiable, do not hide the gap with confident prose. Offer three concrete options: user supplies missing facts, you run targeted research, or you narrow the scope.

End Phase 1 by showing the complete Anchor Sheet and asking: "以上是本文的写作蓝图，是否可以开始撰写？" Stop there until the user confirms.

### Phase 2: Drafting

Draft only from the confirmed Anchor Sheet.

Follow the selected narrative strategy. Do not silently switch strategies; if the strategy no longer fits, return to Phase 1 and ask for confirmation of the revised Anchor Sheet.

Apply these non-negotiables:

- State the central thesis in the opening paragraph. The reader should know the article's claim within 60 seconds.
- Let structure grow from the thesis. Do not force a fixed outline such as "background / concept / practice / summary".
- Use precise, editorial titles. Ban topic tags, clickbait, empty drama, and self-media phrasing.
- Fulfill every promised anchor. If the Anchor Sheet says a mechanism, rejected option, threshold, or boundary matters, the article must explain it or explicitly remove it through a confirmed scope change.
- Fulfill the visual plan. Use the `mermaid-diagrams` skill for Mermaid diagrams. Diagrams must answer specific reader questions, not decorate the article.
- Write like a senior engineer explaining a design review to peers: opinionated, evidence-based, direct, and technically specific.
- Keep the ending tied to the thesis. Do not end with cheerleading, "相信读者已经了解", or generic future-looking praise.

Read `references/language-standard.md` before drafting if tone, titles, or AI-flavored prose are at risk. Read `references/diagram-guide.md` before writing diagrams.

### Phase 3: Validation Loop

Before delivering the article, read `references/quality-checklist.md` and run the checklist as an executable loop:

1. Check the draft against every gate.
2. Revise any failing section.
3. Re-check the revised draft.
4. Deliver only when all gates pass, or clearly state the remaining risk if a user-imposed constraint prevents a fix.

Use `references/anti-patterns.md` whenever a language or structure problem is ambiguous. First drafts often fail two or three gates; treat that as normal and revise.

## Handoff From Tech Planner

If the input is a `tech-planner` prompt, read `references/tech-planner-handoff.md`.

Convert the prompt into an Anchor Sheet, mark which fields are already satisfied, call out missing anchors or version ambiguity, and request confirmation. Do not re-plan the whole series. Do not skip Phase 1.

## Reference Map

Read only what the current task needs:

- `references/prewriting-protocol.md` — Phase 1 Anchor Sheet protocol and confirmation rules.
- `references/narrative-strategies.md` — strategy library for non-template article structures.
- `references/anti-patterns.md` — AI writing symptoms, detection methods, fixes, and bad/good examples.
- `references/quality-checklist.md` — Phase 3 validation gates.
- `references/language-standard.md` — title, tone, transition, ending, and evidence language standards.
- `references/diagram-guide.md` — visual planning and Mermaid selection guidance.
- `references/tech-planner-handoff.md` — compressed Phase 1 for complete planning prompts.
- `references/test-cases.md` — representative forward-testing prompts.

## Final Output Shape

When delivering the article, include:

- The article itself in Markdown.
- A short validation note after the article listing the most important gates checked and any residual assumptions.

Do not include the full Anchor Sheet in the final article unless the user asks for it.
