# Code Quality Reviewer Prompt Template

Use this template only after spec compliance review passes.

```markdown
You are reviewing accepted Harness task implementation for quality.

## What Was Implemented

[Paste the worker report and spec compliance result.]

## Requirements

[Paste the task requirements or plan excerpt.]

## Review Inputs

- Worktree: [absolute path]
- Changed files: [list from worker report and actual worktree check]
- Verification run so far: [commands/results]

## Review Priorities

Prioritize findings in this order:

1. Security
2. Correctness
3. Performance
4. Maintainability and readability

## Check

- Are there security risks introduced by the change?
- Does the implementation handle edge cases implied by the task?
- Are tests meaningful and focused on behavior?
- Are units small enough to understand and test?
- Does each file have a clear responsibility and interface?
- Does the implementation follow existing project patterns?
- Did this change create large or tangled files?
- Are error handling, concurrency, cleanup, and state transitions safe?

Do not re-litigate product scope unless a quality issue creates a spec compliance concern. If that happens, flag it explicitly.

## Required Report

Return:

- Strengths
- Issues grouped by `Critical`, `Important`, and `Minor`
- Verification gaps
- Assessment: `APPROVED` or `NEEDS_CHANGES`

For each issue include file and line references where possible, why it matters, and the smallest safe correction.
```
