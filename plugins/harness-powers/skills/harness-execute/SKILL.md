---
name: harness-execute
description: Use to execute an active Harness plan from docs/exec-plans/active/ while updating checkboxes, evidence, verification, and completion handoffs.
license: MIT
---

# Harness Execute

Execute an active plan while preserving audit evidence and respecting task ownership.

## Overview

Load a plan from `docs/exec-plans/active/`, review it critically, execute task by task, update checkbox state and evidence as work completes, then hand off to `harness-verify` and `harness-finish`.

Do not execute plans from unstated locations unless the user explicitly provides a different plan path.

## Step 1: Load And Review

1. Read the active plan from `docs/exec-plans/active/`.
2. Read linked spec, `AGENTS.md`, and relevant docs referenced by the plan.
3. Check for blockers:
   - missing files or source material
   - unclear task ownership
   - shared write scopes that require coordination
   - verification commands that cannot run
   - plan/spec contradictions
4. If blockers exist, stop and ask before editing.
5. If no blockers exist, create a working checklist from the plan tasks.

## Step 2: Execute Tasks

For each task:

1. Mark the task or step in progress in your working checklist.
2. Follow the plan steps in order.
3. Make only the changes in the task scope unless the plan or user updates the scope.
4. Run the specified verification commands.
5. Update the active plan checkbox from `- [ ]` to `- [x]` only after the step is actually complete.
6. Add evidence near the task or step:
   - command run
   - result
   - relevant output summary
   - known limitations
7. Continue to the next task only after the current task has evidence or an explicit blocker note.

## Delegation

Use `harness-dispatch` when work can be split into independent tasks with disjoint write scopes.

The primary agent keeps ownership of:

- active plan state
- task assignment boundaries
- integrating completed work
- checkbox and evidence updates
- final verification handoff

Delegated workers must receive:

- exact task name and plan path
- allowed write scope
- required verification command
- expected evidence format
- instruction not to commit unless explicitly requested

Do not dispatch tasks that modify the same files unless the plan explicitly coordinates ordering and ownership.

## Step 3: Keep The Plan Auditable

The active plan is the source of execution truth. Update it as evidence is gathered:

- completed checkboxes for completed steps only
- blocker notes for stopped work
- command evidence for tests, builds, lint, or manual checks
- links or paths to generated artifacts when relevant

Do not mark a task complete based on intent. Mark it complete only after implementation and verification evidence exist.

## Step 4: Stop Conditions

Stop immediately and ask for help when:

- a required plan instruction is unclear
- verification fails repeatedly
- the plan requires files outside the allowed write scope
- implementation reveals a security or correctness risk not covered by the plan
- another worker changed files in your task scope in a conflicting way
- a dependency or tool is missing and cannot be worked around safely

Record the blocker in the active plan if the plan is within your write scope. If not, report the blocker in your response.

## Step 5: Completion Handoff

After all assigned tasks are implemented and evidenced:

1. Invoke `harness-verify` before making any success claim.
2. Use fresh verification evidence from the current worktree.
3. If verification passes, hand off to `harness-finish` for integration, branch, PR, or cleanup decisions.
4. If verification does not pass, return to the relevant task or stop with the failure evidence.

## Remember

- Execute the plan, not a remembered version of it.
- Keep evidence attached to completed work.
- Use `harness-dispatch` for safe delegation, not ambiguous ownership.
- Use `harness-verify` before claiming completion.
- Use `harness-finish` after verified implementation work.
- Never commit unless the user explicitly asks.
