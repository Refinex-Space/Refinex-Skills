# Phase naming guide

Phase names matter, but not in the way many generated outlines assume. The job of a phase name is to orient the reader quickly. The job of the phase goal paragraph is to explain the cognitive move in full.

Weak outlines usually fail phase naming in one of two opposite ways:

- they use empty buckets like `Basics`, `Intermediate`, `Advanced`
- they overcorrect into taxonomy theater like `认知重建`, `机制精通`, `能力扩展`

Both are bad. One says too little. The other sounds like a model trying to sound important.

## Core rule

Treat a phase label as a pair:

1. a **concise phase name**
2. a **phase goal paragraph**

The concise name should be easy to scan and sound like something an editor would actually publish. The goal paragraph carries the richer transformation: what the reader can do after the phase, what misconceptions are being corrected, and why this phase exists in the series.

Good pair:

- Phase name: `入门与术语`
- Goal paragraph: by the end of this phase, the reader can create a first runnable project, match the framework version correctly, and understand the terms used in the rest of the series

Bad pair:

- Phase name: `认知重建`
- Goal paragraph: vague repetition of the title with no concrete reader change

## What a strong phase name does

A strong phase name is:

- short enough to scan
- concrete enough to orient
- natural enough to sound edited rather than generated

It does **not** need to carry the entire argument of the phase by itself. That is what the phase goal paragraph is for.

## Three tests

### 1. Scan test

If a reader skims all phase names in five seconds, can they tell the broad arc of the series?

Names like `入门与术语`, `核心抽象`, `RAG 管线`, `生产化`, `架构取舍` pass.
Names like `Phase 2: Mechanism Mastery: how the request pipeline actually wires together` are usually doing too much in the label itself.

### 2. Naturalness test

Would a human editor choose this phrase for a section header?

If the answer is "probably not, but it sounds grand", rewrite it.

Generated-feeling patterns to avoid:

- abstract noun inflation
- paired theatrical clauses
- slogan-like wording
- stage-language such as `最后一公里`, `真实代价`, `背后发生了什么`

### 3. Transformation test

Read the phase name **together with** the goal paragraph and ask: what changes for the reader after this phase?

If the answer is still vague, the phase is under-specified.

This test applies to the pair, not the title alone. The title can stay compact.

## The four verbs are planning aids, not naming mandates

The classic planning verbs — reconstruct, master, extend, debug — are still useful. They help the planner reason about the phase's role in the series.

But they do not need to appear literally in the phase name.

Useful:

- use `reconstruct` when deciding that the phase corrects a wrong mental model
- use `master` when deciding that the phase opens up the mechanism
- use `extend` when deciding that the phase covers extension points or composition
- use `debug` when deciding that the phase is about failure modes or diagnostics

Not useful:

- forcing every visible phase name to spell out the verb category

## Recommended naming patterns

For framework series, these patterns are usually enough:

- onboarding: `入门与术语`, `第一条链路`, `版本与启动`
- mechanism: `核心抽象`, `调用链`, `执行模型`
- application: `RAG 管线`, `Tool Calling`, `Memory`
- production: `生产化`, `诊断与观测`, `故障模式`
- synthesis: `架构取舍`, `设计哲学`, `什么时候该绕开它`

These are examples, not a fixed vocabulary. The point is the level of compression.

## Good and bad examples

### Spring AI

Bad:

- `认知重建`
- `机制精通`
- `能力扩展`

Better:

- `入门与术语`
- `核心抽象`
- `Tool Calling`
- `生产化`
- `架构取舍`

### Project Reactor

Bad:

- `Reactive Basics`
- `Advanced Operators`

Better:

- `发布与订阅`
- `Operator 分类`
- `执行模型`
- `生产问题`

### Kubernetes Operators

Bad:

- `Introduction`
- `Core Concepts`
- `Advanced Patterns`

Better:

- `控制器心智模型`
- `Reconcilers`
- `CRD 演化`
- `故障与恢复`

## Workflow

1. Define the phase purpose in one sentence.
2. Decide whether the phase is onboarding, mechanism, application, production, or synthesis.
3. Draft a short name that a human editor would plausibly use.
4. Write the phase goal paragraph.
5. Run the three tests.

If the phase only works when the title itself becomes a mini-essay, the problem is usually the phase design, not the title wording.
