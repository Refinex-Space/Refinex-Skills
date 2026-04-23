# Output template

This file defines the exact outer structure that `tech-planner` should emit. It exists for one reason: the outer outline and the inner `tech-writing` prompt serve different jobs, and mixing them creates duplication.

The outer outline is for navigation and series architecture review. The inner prompt is the handoff payload for `tech-writing`.

## Rule zero

Put detailed writing metadata in one place only: the inner prompt.

If the outer outline repeats the prompt's central argument, voice, prerequisites, scope, source references, visual plan, and depth contract, the deliverable becomes longer without becoming better. It also becomes harder to maintain, because every article now has two copies of the same truth.

## Series overview

The document starts with a series overview containing:

- topic and version boundary
- target reader and entry-state assumptions
- reader ladder from beginner/junior entry to intermediate/senior payoff
- series argument
- scope and explicit exclusions
- phase/article count
- divergence note explaining how the structure differs from the official docs

## Coherence notes

The document ends with a short `Coherence Notes` section containing:

- the key prerequisite chains that were checked
- any intentional spiral revisits and what changes on each revisit
- any overlaps that were deliberately allowed
- the phase-to-phase transition logic

This section is brief but mandatory. It is the planner's proof that the series is not just shaped well, but internally consistent.

## Phase section

Each phase uses this shape:

```markdown
## Phase N — [concise phase name]

[one short paragraph stating the phase goal, the reader state at start,
the reader state at end, and the concrete benefit unlocked in this phase]
```

The phase name should be short and natural. The paragraph carries the fuller transformation.

## Article section

Each article uses this shape:

````markdown
### Article N.M — [concise claim-carrying title]

Thesis: [one sentence]

Note: [optional; only when the article is a foundation / bridge /
aha-moment / synthesis article]

```text
/tech-write
<prompt>
[complete self-contained prompt]
</prompt>
```
````

## What stays out of the outer outline

Do not add separate outer blocks for:

- voice
- prerequisite knowledge
- in-scope / out-of-scope
- reference links
- visual plan
- depth contract

Those belong inside the prompt. The outer outline already has the thesis line for scanning; duplicating the rest is noise.

## Title guidance

The article title should make one clean claim.

Good:

- `ChatClient 不是 HTTP wrapper`
- `Embedding 需要单独成篇`
- `RAG 的瓶颈通常不在检索`

Bad:

- `Introduction to ChatClient`
- `理解 Spring AI`
- `ChatClient → AdvisorChain → ChatModel 三层夹心——你的第一次 API 调用背后发生了什么`

The bad examples fail for opposite reasons: some say nothing, others try to say everything.
