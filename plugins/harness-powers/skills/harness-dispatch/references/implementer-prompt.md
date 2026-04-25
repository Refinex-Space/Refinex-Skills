# Implementer Worker Prompt Template

Use this template when dispatching a fresh implementation worker for one Harness task or independent domain.

```markdown
You are implementing: [task or domain name]

## Task Description

[Paste the full task text or focused failure description. Do not make the worker rediscover the assignment from conversation history.]

## Context

- Worktree: [absolute path]
- Plan: [plan path]
- Spec/source: [relevant excerpt or path]
- Read-only context: [files the worker may inspect]
- Allowed write scope: [exact files/directories]
- Out of scope: [files/directories/features not to touch]

## Before You Begin

Ask before editing if:

- requirements or acceptance criteria are unclear
- the allowed write scope is insufficient
- the task requires architectural judgment not settled by the plan
- another worker appears to have changed your files
- you cannot verify safely with the provided commands

## Your Job

Once the requirements are clear:

1. Implement exactly the assigned task.
2. Add or update focused tests when the task requires behavior changes.
3. Follow existing project patterns.
4. Run the required verification commands.
5. Self-review against the task, scope, and tests.
6. Report back using the required output contract.

Do not commit unless the user explicitly requested commits.

## Code Organization

- Keep edits inside the allowed write scope.
- Keep files focused on one responsibility.
- Do not restructure unrelated code.
- If a file is too large or tangled to change confidently, report `DONE_WITH_CONCERNS` or `BLOCKED`.
- If your implementation needs a broader design choice, stop and ask.

## Stop And Escalate

Return `NEEDS_CONTEXT` when missing information prevents a safe choice.

Return `BLOCKED` when the task cannot be completed inside the scope or verification constraints.

Return `DONE_WITH_CONCERNS` when the work is complete but you have doubts about correctness, coverage, risk, or maintainability.

## Self-Review

Before reporting:

- Did I implement every assigned requirement?
- Did I avoid extra features?
- Did I stay inside scope?
- Did tests verify behavior rather than implementation details?
- Did verification run in this worktree?
- Are any risks or deviations documented?

## Required Output Contract

Status: DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED

Changed files:
- `path`: created/modified/deleted, with one-line purpose

Verification:
- Command: `...`
  Result: passed/failed/not run
  Evidence: short output summary

Residual risks:
- security, correctness, performance, migration, concurrency, or test gaps

Plan deviations:
- any requirement not implemented exactly as written
- any extra work added
- any file touched outside the expected scope

Notes:
- questions, blockers, or review-worthy context
```
