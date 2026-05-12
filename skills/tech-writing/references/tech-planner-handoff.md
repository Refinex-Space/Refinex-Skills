# Tech Planner Handoff

`tech-planner` produces prompts that are already close to an Anchor Sheet. Do not discard that work or restart series planning.

## Compressed Phase 1

When the input comes from `tech-planner`:

1. Parse the prompt into the six Anchor Sheet dimensions.
2. Mark each dimension as `已满足`, `部分满足`, or `缺失`.
3. Do targeted research only for version ambiguity, current API behavior, missing anchors, or user-requested citations.
4. Present the compressed Anchor Sheet.
5. Ask for confirmation before drafting.

## Mapping

- `Article title` -> title candidate, but still validate title quality.
- `Central thesis` -> central thesis.
- `Key technical anchors` -> technical anchors and depth contract.
- `Prerequisite article dependencies` -> reader profile and assumed knowledge.
- `Visual plan` -> visual plan.
- `Scope` or `boundaries` -> scope boundary.
- `Recommended structure` or `writing strategy` -> narrative strategy.

## What Not To Do

- Do not rebuild the whole series.
- Do not add unrelated topics because the larger series contains them.
- Do not skip confirmation.
- Do not treat the provided prompt as automatically sufficient; still expose missing anchors.

## Confirmation Copy

Use concise language:

```markdown
我把 tech-planner 的 Prompt 压缩成了本文 Anchor Sheet。大部分写作约束已经明确；目前只需要确认两个点：版本范围和是否保留第二张图。

以上是本文的写作蓝图，是否可以开始撰写？
```
