---
name: mermaid-diagrams
description: Design, repair, and standardize Markdown-embedded Mermaid diagrams with syntax-safe, renderer-portable authoring and restrained visual taste. Use when Codex needs to create or fix Mermaid code for flowcharts, sequence diagrams, state diagrams, class diagrams, ER diagrams, timelines, or other Mermaid-backed technical visuals in Markdown, docs, ADRs, blog posts, architecture notes, or any writing workflow. Also use when another skill already decided that a diagram is needed and the remaining task is to turn that visual plan into clean Mermaid that avoids parser breakage, crowding, awkward layout, and decorative styling.
---

# mermaid-diagrams

This skill exists for one narrow job: turn a diagram idea into Mermaid that is correct, readable, and portable across common Markdown renderers. The standard is not fancy Mermaid. The standard is question-first modeling, lowest-common-denominator syntax, and restrained aesthetics.

The skill is intentionally downstream of diagram selection. If another workflow has already decided that the document needs a `sequenceDiagram` or `flowchart`, do not reopen that decision unless it is clearly wrong. Your job is to make the chosen diagram type work cleanly.

## Working stance

Prioritize these goals in order:

1. Question fit: the diagram answers one explicit reader question.
2. Syntax safety: the Mermaid parses in common Markdown environments.
3. Layout hygiene: the diagram is not crowded, tangled, or forced to do two jobs at once.
4. Visual restraint: beauty comes from structure, spacing, and emphasis, not decorative color.

When these goals conflict, cut complexity before adding styling.

## Workflow

Follow this sequence every time.

### 1. Lock the diagram job

Write four internal lines before emitting Mermaid:

- Reader question: what the diagram must make obvious
- Diagram type: `flowchart`, `sequenceDiagram`, `stateDiagram-v2`, `classDiagram`, `erDiagram`, `timeline`, or another Mermaid type only when justified
- Primary direction: `LR`, `RL`, `TB`, or `BT` when the type supports it
- Split decision: whether one diagram is enough or the idea needs two smaller diagrams

If the request mixes temporal order, static structure, and branching logic in one picture, split it. One diagram should answer one question.

### 2. Design the geometry before the syntax

Choose a layout that keeps cognitive load low:

- Prefer 6-10 nodes for a load-bearing diagram. Go above 12 only when the relationships are still visually obvious.
- Prefer 3-5 actors in `sequenceDiagram`.
- Prefer at most 2 subgraphs in `flowchart`, and only one nesting level.
- Prefer short labels. If a label needs a full sentence, the prose is carrying the wrong burden.
- Prefer multiple small diagrams over one system-map poster.

Good Mermaid aesthetics come mostly from node budgeting, direction choice, and label discipline.

### 3. Write in the portable subset first

Default to the most portable Markdown-safe subset unless the user explicitly asks for renderer-specific features and the environment is known to support them.

Portable defaults:

- Use plain Mermaid fences: ```` ```mermaid ````.
- Use standard diagram declarations such as `flowchart LR`, `sequenceDiagram`, `stateDiagram-v2`, `classDiagram`, `erDiagram`, `timeline`.
- Use stable shapes and syntax; do not reach for exotic syntax to look clever.
- Use explicit IDs when the diagram benefits from readable edges or later styling.
- Quote labels when special characters may be parsed as syntax.

Avoid by default:

- HTML labels
- icons, callbacks, `click`, or interactive behavior
- renderer-specific theme tricks
- deeply nested subgraphs
- excessive `style`, `linkStyle`, and `classDef` combinations
- comments that mimic directive syntax

Read `references/authoring-standard.md` for the exact safe-authoring rules and parser pitfalls.

### 4. Apply restrained styling only when it pays rent

The default output should already look good without custom colors. Use styling only when it clarifies semantic roles.

Strong default:

- No custom theme block
- One neutral default node style
- One accent role if needed for the diagram's argument
- One muted role if needed for external systems, failures, or optional paths

If styling is added, keep it sparse and consistent. Read `references/styling-standard.md` before using `classDef`, `style`, or theme variables.

### 5. Run the self-check before delivery

Before returning Mermaid:

- Verify that the diagram answers exactly one reader question.
- Verify that every label is short and domain-true.
- Verify that the syntax stays inside the portable subset unless a wider feature set was explicitly justified.
- Verify that any use of `subgraph`, `direction`, `classDef`, or quoted labels is syntactically correct.
- Verify that the diagram is not carrying both mechanism and ownership in one picture.

Run `references/final-checklist.md` as the last pass.

## Integration with writing skills

When this skill is used from `tech-writing`, `tech-rewrite`, or `tech-planner`:

- Treat the upstream visual plan as binding input.
- Keep the upstream reader question and central argument visible in the diagram.
- Prefer the simplest Mermaid that discharges the writing obligation.
- Return Mermaid that the writing workflow can paste directly into Markdown without extra cleanup.

If the upstream plan says a diagram is required but the selected type is clearly mismatched, fix the type briefly and say why. Otherwise, do not reopen the higher-level writing workflow.

## Reference map

Read only what the current task needs:

- `references/authoring-standard.md` — portable syntax rules, parser pitfalls, and layout discipline
- `references/styling-standard.md` — restrained color and styling rules for Markdown Mermaid
- `references/pattern-cookbook.md` — per-diagram-type authoring defaults and compact examples
- `references/final-checklist.md` — last-pass validation loop before delivery

## Final reminder

The safest way to make Mermaid diagrams look better is usually not to decorate them. It is to ask a sharper question, remove half a layer of detail, shorten three labels, and split one overloaded picture into two. When in doubt, simplify.
