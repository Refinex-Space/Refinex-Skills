---
name: harness-feat
description: >-
  Plan and execute new feature work, capability delivery, and structured
  refactors in repositories that already use Harness Engineering control plane
  artifacts such as `docs/PLANS.md`, `docs/exec-plans/active`,
  `docs/OBSERVABILITY.md`, `docs/generated/harness-manifest.md`, and repo-local
  `python3 scripts/check_harness.py`. Use when the user gives a rough
  implementation goal and the agent should rewrite the task, run harness
  preflight, create or update a live execution plan, execute in small validated
  slices, sync `docs/PLANS.md`, and archive the plan deterministically.
  Especially relevant for prompts such as `$harness-feat`, `任务：实现...`,
  `新增...`, `重构...`, or `做这个功能`.
license: Proprietary. LICENSE.txt has complete terms
---

# harness-feat

Implement features, deliver capabilities, and perform structured refactoring within a harnessed repository. The agent works WITHIN the control plane established by harness-bootstrap and maintained by harness-garden — reading it before coding, updating it during coding, and leaving it accurate after coding.

This is a **medium-freedom** skill. The five-step workflow is rigid (preflight → plan → implement → verify → archive) and must be followed in order. Within each step, the agent has latitude in HOW it accomplishes the work — choosing implementation strategies, test approaches, and refactoring patterns — but every decision must be recorded in the execution plan.

**Announce at start:** `I'm using harness-feat to deliver this work inside the Harness control plane.`

---

## Why this skill exists

Without a structured workflow, the agent starts coding the moment it sees the user's request. It writes code that works in isolation but breaks architectural coherence, doesn't update the control plane, leaves no record of decisions, and produces a codebase where the next agent has to re-discover everything from scratch.

The primary risk this skill fights is **cowboy coding**: jumping straight to implementation without reading the control plane, creating a plan, or establishing verification evidence. OpenAI's team discovered that progress comes not from "trying harder" but from asking "what capability is missing, and how do we make it legible and enforceable?" The execution plan is what makes work legible; the preflight and verification steps are what make constraints enforceable.

A secondary risk is **premature victory** — one of the four failure modes Anthropic identified in long-running agents. The agent declares success after writing code that compiles, without verifying that it actually meets the acceptance criteria or that it doesn't break existing functionality. The verification step and sprint contract address this directly.

A third risk is **scope drift**: the agent discovers something interesting mid-implementation and pivots without updating the plan. This produces untracked changes that confuse future agents and humans. Every deviation from the plan must be recorded before acting on it.

---

## Shared terminology

All four Harness skills (harness-bootstrap, harness-garden, harness-feat, harness-fix) use these terms consistently:

| Term               | Definition                                                                                 |
| ------------------ | ------------------------------------------------------------------------------------------ |
| **Control plane**  | The set of AGENTS.md, docs/, scripts/, and manifest that guide agent work                  |
| **Execution plan** | A versioned, checkpointed plan in docs/exec-plans/                                         |
| **Managed doc**    | A doc created and maintained under harness lifecycle                                       |
| **Unmanaged doc**  | An existing team doc the harness must NOT overwrite                                        |
| **Manifest**       | Machine-readable inventory of control plane artifacts (docs/generated/harness-manifest.md) |
| **Preflight**      | Verification check run before starting any task (scripts/check_harness.py)                 |
| **Drift**          | When control plane artifacts no longer reflect repo reality                                |

---

## Step 1 — Harness Preflight

Before writing any code, orient yourself within the control plane and establish a healthy baseline. This step exists because Anthropic found that "verify before building" is the single most effective pattern for preventing broken state carryover.

Read `references/preflight-checklist.md` for the complete checklist. Summary:

### 1.1 Read the control plane

Read these files in order — each one adds context for the next:

1. **Root AGENTS.md** — understand the repo map, architecture pointers, key patterns, module guide
2. **Relevant module AGENTS.md** — understand the target area's conventions and boundaries
3. **docs/PLANS.md** — check for active plans that might conflict with this task. If a related plan is already active, either extend it or coordinate to avoid conflicting changes
4. **docs/ARCHITECTURE.md** — understand architectural constraints and dependency directions
5. **docs/OBSERVABILITY.md** — learn the build, test, lint, and run commands

### 1.2 Run preflight check

```bash
python3 scripts/check_harness.py
```

If the check fails, the control plane is unhealthy. Do NOT proceed with feature work on a broken control plane — report the failures and suggest running `harness-garden` first to repair the drift.

If `check_harness.py` does not exist, the repo has no harness — suggest running `harness-bootstrap` first and stop.

### 1.3 Establish test baseline

Run the existing test suite before making any changes:

```bash
<test-command from docs/OBSERVABILITY.md>
```

Record the exit code and summary (number of tests, pass/fail). This is the green baseline. If tests are already failing, record which ones — you must not make failing tests worse, and you must not claim credit for fixing pre-existing failures.

### 1.4 Check for conflicting work

Read `docs/PLANS.md`. If another agent or human has an active plan touching the same modules or files:

- **Non-overlapping**: proceed, but note the parallel work in your plan
- **Partially overlapping**: adjust your plan to avoid the shared files, or wait
- **Directly conflicting**: stop and report the conflict to the user

---

## Step 2 — Task Rewriting and Sprint Contract

Before any code is written, establish exactly what "done" means. Anthropic's sprint contract pattern eliminates the premature victory failure mode by negotiating the definition of completion before work begins.

### 2.1 Rewrite the user's request

The user's request is usually informal and incomplete. Rewrite it into a precise task brief:

- **Objective**: one sentence describing what will be different when this is done
- **Scope**: which modules/files/directories are in play
- **Non-scope**: what this task explicitly does NOT include (prevents drift)
- **Constraints**: architectural rules from AGENTS.md that apply

Present the rewritten task to the user. Wait for confirmation before proceeding. If the user adjusts the scope, update the brief.

### 2.2 Create the execution plan

Create a new file in `docs/exec-plans/active/` following the naming convention `YYYY-MM-DD-short-description.md`. Read `references/exec-plan-template.md` for the complete template.

The execution plan must include:

1. **Header**: objective, scope, constraints (from 2.1)
2. **Acceptance criteria**: specific, verifiable conditions that define "done"
3. **Implementation steps**: ordered sequence of small, testable changes
4. **Risk notes**: known risks and mitigation strategies

#### Step sizing

Each implementation step should be 2-5 minutes of focused agent work (aligned with the Superpowers task decomposition pattern). A well-sized step:

- Touches a small number of files (1-5)
- Has a clear verification criterion (a test passes, a command works, a file exists)
- Can be committed independently without leaving the repo in a broken state
- References specific file paths it will modify

If a step seems bigger than that, break it down further. If a step seems trivially small (rename a variable), consider merging it with the next step.

#### Plan quality bar: no placeholders

Execution plans are audit artifacts, not wishful outlines. Do not write:

- `TODO`, `TBD`, `implement later`, or other placeholders
- vague steps like "handle edge cases" without naming the edge cases
- "write tests" without naming the test target or verification command
- alternate planning directories such as `docs/superpowers/plans/`

Keep all plan state in `docs/exec-plans/active/` and `docs/PLANS.md`.

#### Plan detail model

Harness plans must be **decision-complete**, but they remain audit-oriented:

- include exact paths, acceptance criteria, and verification commands
- name the architectural constraints that matter
- break work into verifiable steps
- do **not** inline full implementation code for every step unless the change genuinely requires that precision

The goal is an executable plan without creating a second source of truth that competes with the code.

### 2.3 Register the plan

Add the plan to `docs/PLANS.md` under "Active Plans":

```markdown
## Active Plans

- [Short description](exec-plans/active/YYYY-MM-DD-short-description.md) — started YYYY-MM-DD
```

### 2.4 Commit the plan

```bash
git add docs/exec-plans/active/YYYY-MM-DD-short-description.md docs/PLANS.md
git commit -m "plan(harness): add execution plan for <short-description>"
```

The plan is now a versioned artifact. Its creation is separate from its implementation — this lets another agent pick up the plan if the current session is interrupted.

---

## Step 3 — Incremental Implementation

Execute the plan one step at a time. Resist the urge to batch multiple steps together — incremental progress with verification is slower per-step but faster overall because it catches mistakes early and creates clean rollback points.

### Delegated execution protocol

If implementation is delegated to subagents or worker sessions, the controller keeps ownership of the plan and review loop:

1. Provide the current step text, constraints, and relevant file paths directly
2. Require the implementer to self-review before reporting completion
3. Run **spec compliance review first**
4. Run **code quality review second**
5. Loop until approved or escalate with evidence

Do not make delegated workers discover the plan on their own from some alternate file tree. The active execution plan remains the only planning source of truth.

### For each plan step:

#### 3.1 Read the step

Re-read the current step from the execution plan. Confirm you understand what it requires and what files it touches.

#### 3.2 Write tests first (when applicable)

TDD is preferred but not always mandatory. Read `references/tdd-workflow.md` for guidance on when TDD applies.

When it applies:

- Write the test that describes the expected behavior
- Run it — it should fail (RED)
- Implement the code to make it pass (GREEN)
- Refactor if needed (REFACTOR)

When TDD doesn't apply (infrastructure changes, configuration, documentation):

- Implement the change
- Write a verification check (could be a test, a smoke command, or a structural assertion)

#### 3.3 Run tests

After implementing each step, run the relevant test suite:

```bash
<test-command from docs/OBSERVABILITY.md>
```

The test suite must stay green after every step. If tests break:

- If the break is caused by your change: fix it within this step
- If the break is pre-existing (matches the baseline from Step 1.3): note it but proceed
- If the break is unrelated to your change: investigate briefly, then note it in the plan and proceed. Do not derail the current task for unrelated issues — log them in `docs/exec-plans/tech-debt-tracker.md`

#### 3.4 Commit with a descriptive message

Read `references/commit-conventions.md` for the full message format. Each commit should:

- Reference the plan step it implements
- Describe WHAT changed and WHY
- Be atomic — it implements one step, not a batch

```bash
git add <changed-files>
git commit -m "<type>(<scope>): <description>

refs plan: <plan-filename> step <N>"
```

#### 3.5 Update the execution plan

Mark the completed step in the plan. Record:

- ✅ Status (done)
- Evidence of verification (e.g., "all 47 tests pass", "endpoint returns 200")
- Any deviations from the original plan (and why)
- If the step took longer than expected, note why — this helps future sizing

#### 3.6 Check for scope drift

After each step, ask: "Am I still on plan?" Scope drift happens when:

- You discover something interesting and start working on it without updating the plan
- The implementation reveals a prerequisite that wasn't in the plan
- You start "cleaning up" code that isn't part of the task

If you need to deviate from the plan:

1. **Stop coding**
2. **Update the plan** — add the new step, or modify existing steps
3. **Commit the plan update** separately from code changes
4. **Then resume implementation**

The execution plan is the source of truth. If it's not in the plan, it shouldn't be in the code.

---

## Step 4 — Post-Implementation Verification

After all plan steps are complete, verify the work holistically. Individual step verification confirms each piece works; this step confirms they work together.

### 4.1 Run full test suite

```bash
<test-command from docs/OBSERVABILITY.md>
```

Compare the result with the baseline from Step 1.3. The test suite should pass with at least as many tests as before, plus any new tests you added.

### 4.2 Verify acceptance criteria

Go through each acceptance criterion from the execution plan. For each one:

- Record the evidence (test output, command result, file state)
- Mark it as PASS or FAIL in the plan
- If any criterion fails, go back to Step 3 and add a step to address it

Apply `harness-verify` discipline here: no completion claim is valid until the proving commands have been run in the current turn and their output actually supports the claim.

### 4.3 Run lint and type checks

```bash
<lint-command from docs/OBSERVABILITY.md>
```

Fix any violations introduced by your changes. Do not fix pre-existing violations unless they're in files you modified (and even then, consider whether that's in scope).

### 4.4 Self-review the diff

Review your own changes as if you were a code reviewer:

```bash
git diff <baseline-commit>..HEAD
```

Check for:

- Debug code left in (console.log, print statements, TODO comments)
- Accidentally committed files (build artifacts, IDE config)
- Files that changed but shouldn't have (unintended side effects)
- Sufficient test coverage for new code paths
- Consistency with patterns described in AGENTS.md

### 4.5 Update the control plane

If your changes affected the repo structure or conventions:

- **New module created**: consider whether it needs a module AGENTS.md (apply the criteria from harness-bootstrap Phase 1.4)
- **Architecture changed**: update `docs/ARCHITECTURE.md` to reflect the new structure
- **New commands or dependencies**: update `docs/OBSERVABILITY.md`
- **Root AGENTS.md**: update the Module Guide or Documentation Index if new modules or docs were added
- **Manifest**: add new managed artifacts to `docs/generated/harness-manifest.md`

Commit control plane updates separately from code changes:

```bash
git commit -m "docs(harness): update control plane after <short-description>"
```

---

## Step 5 — Plan Archival and Handoff

The task is done when the plan is archived, not when the code is written. This step ensures the repo is left in a state where another agent or human can understand exactly what happened.

### 5.1 Complete the execution plan

Add a completion summary to the plan:

```markdown
## Completion Summary

Completed: YYYY-MM-DD
Duration: <number of steps completed> steps
All acceptance criteria: PASS

Summary: <one paragraph describing what was built, key decisions made, and any
deviations from the original plan>
```

### 5.2 Move the plan to completed

```bash
git mv docs/exec-plans/active/YYYY-MM-DD-short-description.md \
       docs/exec-plans/completed/YYYY-MM-DD-short-description.md
```

### 5.3 Update PLANS.md

Move the plan entry from "Active Plans" to "Completed Plans":

```markdown
## Completed Plans

- [Short description](exec-plans/completed/YYYY-MM-DD-short-description.md) — completed YYYY-MM-DD
```

### 5.4 Final commit

```bash
git add docs/exec-plans/ docs/PLANS.md
git commit -m "chore(harness): archive execution plan for <short-description>"
```

### 5.5 Print summary

Report to the user:

```
=== Feature Complete ===

Task: <objective from plan>
Plan: docs/exec-plans/completed/YYYY-MM-DD-short-description.md
Steps completed: <N>
Acceptance criteria: <all PASS / N of M PASS>
Tests: <baseline count> → <new count> (added <diff>)
Control plane updates: <list of updated harness files>

Commits:
  1. plan(harness): add execution plan for <short-description>
  2. feat(<scope>): <step 1 description>
  ...
  N. chore(harness): archive execution plan for <short-description>
```

---

## Rollback protocol

When implementation goes wrong and you can't fix it within the current step:

### Soft rollback (preferred)

If the problem is contained to the current step:

1. `git stash` or `git checkout -- .` to discard uncommitted changes
2. Update the plan: mark the step as FAILED with notes on what went wrong
3. Rewrite the step (maybe break it smaller) and retry

### Hard rollback

If committed changes broke things and you can't fix forward:

1. Identify the last known-good commit (the one from the previous step)
2. `git revert <bad-commits>` (never `git reset --hard` — preserve history)
3. Update the plan: mark affected steps as REVERTED with explanation
4. Replan and retry from the reverted state

### Abort

If the task itself is misconceived (wrong approach, missing prerequisites):

1. Revert all changes to code
2. Update the plan with an "Aborted" status and explanation
3. Move the plan to `completed/` (completed plans include failed/aborted ones)
4. Update PLANS.md
5. Report to the user with the evidence for why the approach won't work

---

## Handling long tasks

For tasks that may exceed a single agent session (>20 steps or touching many modules):

### Checkpoint discipline

After every 5 completed steps, do a mini-verification:

- Run the full test suite (not just the affected tests)
- Review the plan — is the remaining work still accurately described?
- Consider whether the task should be split into multiple execution plans

### Cross-session continuity

Every execution plan is a handoff artifact. If the current session ends mid-task, the next agent can:

1. Read the plan to see which steps are done vs. remaining
2. Check git log to see the latest committed state
3. Run preflight to verify control plane health
4. Resume from the next incomplete step

This works because:

- Each step has explicit completion evidence
- Each commit references the plan step it implements
- The plan itself is versioned in git

---

## Critical design constraints

These rules prevent well-intentioned automation from producing architectural damage.

1. **Always do preflight before any code changes.** The control plane is the agent's map. Coding without reading it is navigating without a map — you might arrive somewhere, but probably not where you intended.

2. **Never skip plan creation, even for "small" changes.** A five-line bugfix still gets a lightweight plan (it just has fewer steps). The plan is the audit trail — without it, the change is invisible to future agents. The plan for a small change can be just a few lines, but it must exist.

3. **Every code change must be accompanied by test evidence.** "I looked at it and it seems fine" is not evidence. A test passing, a command succeeding, a log output showing correct behavior — that's evidence. Record it in the plan.

4. **The execution plan is the source of truth.** If it's not in the plan, it shouldn't be in the code. If you need to do something unplanned, update the plan first.

5. **Delegated review order is fixed.** When using delegated execution, review for spec compliance before reviewing for code quality. Quality review on the wrong spec is wasted work.

6. **Respect architectural constraints from AGENTS.md.** Key Patterns in AGENTS.md encode architectural decisions. If your implementation would violate a stated pattern, stop and discuss with the user rather than silently breaking the constraint.

7. **Leave the repo in a state where another agent can pick up seamlessly.** This means: all tests pass, the execution plan accurately reflects what was done, the control plane is updated, and there are no uncommitted changes.

8. **Git commits are checkpoints, not afterthoughts.** Each commit implements one plan step and references it. Avoid mega-commits that bundle many steps — they make rollback and understanding impossible.

9. **Log deviations, don't hide them.** When you deviate from the plan (and you will — plans never survive contact with implementation perfectly), record the deviation BEFORE acting on it. The deviation log is how future agents learn about the real complexity.

---

## Adapting to task size

Not every task needs the same weight of process. Scale the ceremony to the change:

| Task size             | Plan detail                           | Commit granularity       | Verification             |
| --------------------- | ------------------------------------- | ------------------------ | ------------------------ |
| Trivial (1-2 files)   | 2-3 steps, inline acceptance criteria | 1-2 commits              | Run affected tests       |
| Standard (3-10 files) | Full plan with all sections           | 1 commit per step        | Full test suite          |
| Large (>10 files)     | Full plan + checkpoint schedule       | 1 commit per step + tags | Full suite every 5 steps |
| Refactor              | Full plan + architectural impact doc  | Atomic commits per move  | Full suite + lint        |

Even trivial tasks still get a plan file in `docs/exec-plans/active/`. The plan may be only 20 lines, but it creates the audit trail.

---

## Reference index

| File                                | When to read                                 |
| ----------------------------------- | -------------------------------------------- |
| `references/exec-plan-template.md`  | Step 2: creating the execution plan          |
| `references/preflight-checklist.md` | Step 1: running harness preflight            |
| `references/commit-conventions.md`  | Step 3: writing commit messages              |
| `references/tdd-workflow.md`        | Step 3: deciding when and how to write tests |
