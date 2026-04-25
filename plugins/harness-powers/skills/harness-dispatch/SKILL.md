---
name: harness-dispatch
description: Use when executing a Harness plan that has independent tasks or problem domains suitable for delegated workers in the current session.
license: MIT
---

# Harness Dispatch

Delegate independent Harness plan work to fresh workers while the primary agent keeps plan ownership, integration judgment, and final verification.

## Core Principle

Use one fresh worker per independent task or domain. Each worker gets only the context, write scope, and verification commands it needs. The primary agent owns the plan, coordinates boundaries, reviews returned work, integrates changes, updates evidence, and decides when to proceed.

## When To Use

Use this skill when:

- an active Harness plan has tasks with disjoint write scopes
- multiple failures belong to independent files, subsystems, or root causes
- work can proceed without workers sharing mutable state
- a task needs isolated implementation plus review before integration

Do not dispatch when:

- one fix may change the behavior another worker is investigating
- workers would edit the same files without an explicit ordering plan
- the work requires a single architectural decision across all tasks
- the plan/spec is unclear enough that delegation would amplify guessing

## Primary Agent Responsibilities

The primary agent never gives away execution ownership. It must:

1. Read the plan, spec, `AGENTS.md`, and relevant project instructions.
2. Extract task text, acceptance criteria, allowed files, and verification commands.
3. Identify independent domains and reject unsafe parallelism.
4. Dispatch workers with exact scope and stop conditions.
5. Review every returned report before trusting it.
6. Run integration review after workers return.
7. Update plan checkboxes and evidence only after verified completion.
8. Hand off to `harness-verify` before claiming the whole implementation is complete.

## Identify Independent Domains

Group work by ownership boundary:

- one feature task with its own files
- one failing test file with a likely isolated root cause
- one subsystem that can be changed without touching another worker's files
- one documentation or fixture update that does not depend on implementation edits

Before dispatch, write down:

- domain name
- exact allowed write scope
- read-only context paths
- verification command
- integration dependency, if any

Use one worker per independent domain. If two domains need the same file, either serialize them or define a clear coordination rule before dispatch.

## Worker Dispatch Rules

Every worker must be fresh. Do not rely on inherited conversation context. Include:

- exact task name and full task text
- plan path and relevant spec excerpt
- allowed write scope and explicit files not to touch
- required verification commands and expected result
- instruction not to commit unless the user explicitly requested commits
- stop conditions for unclear requirements, shared-scope conflicts, or risky design choices
- required output contract

Use `references/implementer-prompt.md` for implementation workers.

## Review Flow

For each worker result:

1. Check the worker status.
2. If status is `NEEDS_CONTEXT`, provide the missing context and redispatch.
3. If status is `BLOCKED`, decide whether to split the task, clarify the plan, or escalate to the user.
4. If status is `DONE_WITH_CONCERNS`, read the concerns before review and decide whether the work is reviewable.
5. Run spec compliance review with `references/spec-reviewer-prompt.md`.
6. If spec review fails, send the findings back to the same task scope for correction.
7. Run code quality review with `references/code-quality-reviewer-prompt.md` after spec compliance passes.
8. If quality review fails, send only the actionable findings back for correction.

Spec compliance answers: did the worker build exactly what was requested?

Code quality answers: is the accepted implementation secure, correct, maintainable, and tested?

## Integration Review After Return

After all workers for a batch return:

1. Compare changed files across reports and the actual worktree.
2. Look for overlapping edits, inconsistent patterns, duplicated helpers, or mismatched assumptions.
3. Run each worker's verification command if not already run in the current worktree.
4. Run the plan-level or suite-level verification command.
5. Update the active plan evidence with commands, results, and residual risks.
6. Do not mark a task complete if integration verification fails.

Parallel dispatch saves time only if integration is real. Never trust summaries without checking the resulting files and commands.

## Worker Output Contract

Workers must return this structure:

```markdown
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

Missing changed files, verification results, residual risks, or plan deviations are not acceptable for a completed worker report.

## Prompt References

- `references/implementer-prompt.md` - implementation worker prompt
- `references/spec-reviewer-prompt.md` - spec compliance reviewer prompt
- `references/code-quality-reviewer-prompt.md` - code quality reviewer prompt

## Remember

- Fresh worker per task or domain.
- Primary agent keeps plan ownership.
- One worker per independent domain.
- No shared write scope unless ordering and ownership are explicit.
- Review for spec compliance before code quality.
- Run integration review after workers return.
- Never commit unless the user explicitly asks.
