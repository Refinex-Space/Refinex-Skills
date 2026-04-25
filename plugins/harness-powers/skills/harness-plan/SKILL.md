---
name: harness-plan
description: Use after an approved Harness spec to create a decision-complete, audit-oriented execution plan under docs/exec-plans/active/.
license: MIT
---

# Harness Plan

Create an active execution plan that an implementer can follow, audit, and verify without rediscovering the design.

## Overview

Use this skill when a spec or approved requirements exist and implementation has not started. Plans are saved under `docs/exec-plans/active/` and indexed in `docs/PLANS.md`.

Harness plans are decision-complete and audit-oriented:

- every task has clear ownership, scope, files, and verification
- decisions that affect implementation are recorded, not implied
- steps are actionable, but they do not need to inline full implementation code
- evidence can be added during execution without rewriting the plan structure

## Inputs

Before writing a plan, read:

- approved spec from `docs/exec-plans/specs/`
- `AGENTS.md` and nested instructions relevant to touched files
- `docs/ARCHITECTURE.md`
- `docs/PLANS.md`
- relevant source and test files

If the spec covers independent subsystems that cannot be implemented coherently in one plan, stop and ask to split it into separate specs or plans.

## Output Path

Save the plan to:

```text
docs/exec-plans/active/YYYY-MM-DD-<feature-name>.md
```

Then update `docs/PLANS.md` with the active plan entry, status, and link.

## Plan Header

Every plan starts with:

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `harness-execute` semantics to implement this plan task by task. Use `harness-dispatch` only for independent subtasks with disjoint write scopes. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** [One sentence describing the outcome]

**Architecture:** [2-3 sentences about approach and boundaries]

**Tech Stack:** [Key technologies, frameworks, storage, tooling]

**Design Source:** `docs/exec-plans/specs/<spec-file>.md`

---
```

## Plan Structure

Before task decomposition, include:

- **Scope** - what will be created, changed, and explicitly excluded.
- **Decisions** - implementation choices, rejected alternatives, and reasons.
- **Files** - expected creates/modifies/tests/docs with responsibilities.
- **Verification Strategy** - commands and expected evidence.
- **Risks** - security, correctness, migration, concurrency, or compatibility risks.

Each task should include:

````markdown
## Task N: [Outcome]

**Files:**

- Create: `path`
- Modify: `path`
- Test: `path`

**Decision Trace:** [Spec section or decision this task implements]

- [ ] **Step 1: [Concrete action]**

Do [specific work]. Use [local pattern/API] from `path`.

- [ ] **Step 2: [Verification]**

Run:

```bash
[command]
```

Expected: [observable result]

**Evidence:** [filled by implementer during harness-execute]
```
````

## Granularity

Prefer tasks that can be reviewed independently:

- write or update tests before behavior changes when practical
- keep file ownership clear
- avoid shared write scopes across parallel tasks
- include exact commands and expected results
- cite source patterns instead of embedding long code copies

Inline code is useful when it removes ambiguity, but it is not mandatory for every implementation step. Prefer precise references, APIs, invariants, and acceptance checks over bulky copied code.

## No Placeholders

Plan failures:

- `TBD`, `TODO`, `fill in later`, or unresolved alternatives
- vague steps like "add validation" without naming the validation rules
- verification without commands or expected outcomes
- references to nonexistent functions, files, or tasks
- tasks that cannot be audited back to the spec

## Self-Review

After writing the plan:

1. **Spec coverage** - every requirement maps to one or more tasks.
2. **Decision completeness** - important trade-offs are explicit.
3. **Buildability** - a skilled implementer can proceed without guessing.
4. **Auditability** - checkboxes and evidence fields support later review.
5. **Placeholder scan** - remove vague or incomplete instructions.
6. **Dispatch safety** - identify tasks with independent write scopes.

Use `references/plan-reviewer-prompt.md` when dispatching a reviewer.

## Handoff

After saving the plan and updating `docs/PLANS.md`, hand off to `harness-execute`.

Offer the execution mode:

```text
Plan complete at `docs/exec-plans/active/<filename>.md` and indexed in `docs/PLANS.md`.

Execution options:

1. Inline execution with `harness-execute`
2. Delegated execution for independent tasks through `harness-dispatch`

Which path should we use?
```
