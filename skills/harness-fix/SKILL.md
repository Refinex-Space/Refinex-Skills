---
name: harness-fix
description: >-
  Plan and execute bug fixes, regression repair, incident remediation,
  flaky-path debugging, and evidence-driven investigation in repositories that
  already use Harness Engineering control plane artifacts such as
  `docs/PLANS.md`, `docs/exec-plans/active`, `docs/OBSERVABILITY.md`,
  `docs/generated/harness-manifest.md`, and repo-local `python3
  scripts/check_harness.py`. Use when the user reports a broken behavior and
  the agent should rewrite the bug report, run harness preflight, reproduce or
  bound the failure, create or update a fix plan, apply the smallest justified
  repair, add regression protection, sync `docs/PLANS.md`, and archive the plan
  deterministically. Especially relevant for prompts such as `$harness-fix`,
  `修复...`, `这个报错`, `为什么坏了`, or `排查回归`.
license: Proprietary. LICENSE.txt has complete terms
---

# harness-fix

Diagnose bugs, repair regressions, remediate incidents, and investigate flaky paths within a harnessed repository. While harness-feat builds new things, harness-fix diagnoses and repairs broken things — and it does so with the discipline of a scientific investigation, not a frantic code-patching spree.

This is a **low-medium freedom** skill. The seven-step diagnosis protocol is rigid (preflight → bug brief → reproduce → isolate root cause → minimal fix → verify → archive) and must be followed in order. The agent has latitude in investigation techniques — choosing which debugging tools to apply, how to narrow the search space, what kind of reproduction test to write — but the sequence of phases is non-negotiable, and skipping reproduction or root cause isolation is never acceptable.

---

## Why this skill exists

When an agent encounters a bug report, the natural impulse is to read the error message, guess the cause, and start editing code. This is the debugging equivalent of cowboy coding, and it produces the same outcome: changes that appear to work but mask the real problem, introduce new failure modes, or accumulate into an unrecoverable mess.

The primary risk this skill fights is **symptom whack-a-mole** — the agent patches the immediate symptom without understanding root cause. OpenAI's team discovered a critical insight: "when something failed, the fix was almost never 'try harder.'" The solution is always to change the approach — better reproduction, different isolation technique, more precise diagnosis — never to keep hammering at the same code hoping it works. This skill encodes that principle by requiring evidence at every stage before proceeding to the next.

A second risk is **fix sprawl**: the agent makes a change, it doesn't fix the bug, so it makes another change, and another, losing track of what was modified and why. After five rounds of this, the codebase has accumulated random mutations with no clear connection to the original problem. The fix scope guard (see below) prevents this by limiting the number of change attempts before requiring a structured replanning.

A third risk is **phantom fixes**: the agent makes a change that coincidentally makes the symptom disappear without actually addressing the root cause. Without reproduction evidence before AND verification evidence after, there's no way to distinguish a real fix from a phantom one. The reproduction → fix → verification sandwich is the only reliable way to confirm a bug is genuinely fixed.

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

Before touching any code, orient yourself within the control plane and establish the "known broken" baseline. This step is shared with harness-feat but has a critical difference: in a fix scenario, the test suite may already be failing — and you need to know exactly which tests fail BEFORE you start, so you can distinguish pre-existing failures from your changes.

### 1.1 Read the control plane

Read these files in order:

1. **Root AGENTS.md** — understand the repo map, architecture pointers, key patterns
2. **Relevant module AGENTS.md** — understand the target area's conventions and boundaries
3. **docs/PLANS.md** — check for active plans that might be related to the bug
4. **docs/ARCHITECTURE.md** — understand architectural constraints and dependency directions
5. **docs/OBSERVABILITY.md** — learn the build, test, lint, and run commands

### 1.2 Run preflight check

```bash
python3 scripts/check_harness.py
```

If the check fails, note the failures. Unlike harness-feat (which stops on a broken control plane), harness-fix proceeds with caution — the bug you're fixing might be the reason the control plane is unhealthy. Note the preflight failures in your fix plan.

If `check_harness.py` does not exist, the repo has no harness — suggest running `harness-bootstrap` first and stop.

### 1.3 Establish the "known broken" baseline

Run the existing test suite:

```bash
<test-command from docs/OBSERVABILITY.md>
```

Record:

- **Exit code**: 0 or non-zero
- **Total tests**: count of all tests
- **Failing tests**: list every failing test by name — these are the "known broken" baseline
- **Passing tests**: count of passing tests

This baseline serves two purposes: (1) it may contain the reproduction of the bug you're about to fix, and (2) it establishes which failures are pre-existing so you don't inadvertently claim credit for fixing them or introduce new failures without noticing.

### 1.4 Check for related active plans

Read `docs/PLANS.md`. If there's an active plan touching the same area as the bug:

- The bug may have been introduced by in-progress work — note this in the bug brief
- Coordinate: the fix might belong as a step in the existing plan rather than a new one

---

## Step 2 — Bug Brief

Rewrite the user's bug report into a structured, precise format. Users describe bugs informally — "it's broken", "this doesn't work", "I'm getting an error." The bug brief transforms this into actionable intelligence.

Read `references/bug-brief-template.md` for the complete template.

### 2.1 Extract and structure the report

| Field              | Description                                                                |
| ------------------ | -------------------------------------------------------------------------- |
| **Symptom**        | Exact observable behavior — the error message, the wrong output, the crash |
| **Expected**       | What should happen instead                                                 |
| **Reproduction**   | Steps to trigger the bug (may be incomplete — will be verified in Step 3)  |
| **Affected scope** | Which modules, files, or components are involved                           |
| **Severity**       | Blocking / Degraded / Cosmetic (see severity table below)                  |
| **Type**           | Regression / New bug / Flaky / Environment-specific                        |

### 2.2 Classify severity

| Severity     | Definition                                                               | Response                       |
| ------------ | ------------------------------------------------------------------------ | ------------------------------ |
| **Blocking** | Core functionality broken, no workaround                                 | Fix immediately, full protocol |
| **Degraded** | Feature works but with errors, performance issues, or edge-case failures | Fix with full protocol         |
| **Cosmetic** | Visual or minor behavioral issue, functionality intact                   | Lightweight fix protocol       |

### 2.3 Classify type

The type determines which investigation techniques are most effective:

| Type                     | Investigation approach                                         |
| ------------------------ | -------------------------------------------------------------- |
| **Regression**           | Git bisect to find the introducing commit, then analyze change |
| **New bug**              | Scientific debugging: hypothesis → experiment cycle            |
| **Flaky**                | Non-deterministic path — see the flaky test protocol below     |
| **Environment-specific** | Compare environments, isolate the differentiating factor       |

### 2.4 Present to user

Present the structured bug brief. Ask the user to confirm or correct. If the report is too vague to create a meaningful brief (no error message, no reproduction steps, no description of expected behavior), ask specific questions before proceeding.

---

## Step 3 — Reproduction

Reproduction is the foundation of the entire fix. Without a reliable way to trigger the bug, you cannot verify that any fix actually works — you can only hope. Hope is not engineering.

### 3.1 Write a reproduction test

The ideal reproduction is a test that:

- **Fails now** (confirms the bug exists)
- **Will pass after the fix** (confirms the fix works)
- **Stays in the test suite forever** (prevents regression)

```
Reproduction test written: test_name
Result: FAIL (expected — confirms bug exists)
Error: <exact error output>
```

If the bug can't be captured in a unit or integration test (e.g., it's a timing issue, a UI rendering problem, or requires a running server), document the manual reproduction steps precisely enough that another agent could follow them:

```
Manual reproduction:
1. Start the server: <command>
2. Navigate to: <URL>
3. Click: <element>
4. Observe: <symptom>
```

### 3.2 Handle reproduction failure

If you cannot reproduce the bug:

1. **Verify the reproduction steps**: re-read the user's report, try variations
2. **Check environment differences**: versions, configurations, OS, dependencies
3. **Ask the user**: "I was unable to reproduce this bug. Here's what I tried: [list]. Can you provide more details about your environment or steps?"

Do NOT proceed to fix without reproduction evidence. A fix without reproduction is a guess — and guesses have a poor track record of actually solving problems.

The one exception: if the bug is visible in the test baseline from Step 1.3 (a test is already failing), that IS your reproduction evidence. Note which test captures the bug and proceed.

### 3.3 Create the fix plan

Once reproduction succeeds, create a fix plan in `docs/exec-plans/active/` using the naming convention `YYYY-MM-DD-fix-short-description.md`. Read `references/fix-plan-template.md` for the template.

The fix plan differs from a feature execution plan in that it includes:

- The bug brief (from Step 2)
- Reproduction evidence (from Step 3)
- A hypothesis log (updated during Step 4)
- Root cause analysis (filled in Step 4)
- The fix itself (planned in Step 5)

Register the plan in `docs/PLANS.md` and commit:

```bash
git add docs/exec-plans/active/YYYY-MM-DD-fix-*.md docs/PLANS.md
git commit -m "plan(harness): add fix plan for <short-description>"
```

---

## Step 4 — Root Cause Isolation

This is where diagnosis separates from guessing. The goal is to narrow the failure to the smallest possible scope and identify the exact mechanism — not just WHAT is failing, but WHY.

Read `references/root-cause-techniques.md` for the complete toolkit.

### 4.1 Choose an investigation technique

Select based on bug type and available information:

| Situation                                  | Primary technique        | Fallback                 |
| ------------------------------------------ | ------------------------ | ------------------------ |
| Bug appeared after a known change          | Git bisect               | Manual commit review     |
| Bug in logic/computation                   | Scientific debugging     | Code path tracing        |
| Bug in data flow                           | Input/output tracing     | Delta debugging          |
| Bug in integration between components      | Interface contract check | Dependency analysis      |
| Intermittent failure                       | Flaky test protocol      | Statistical reproduction |
| Bug with clear error message + stack trace | Stack trace analysis     | Breakpoint debugging     |

### 4.2 Apply the chosen technique

The reference file covers each technique in full. Here's the essential logic:

- **Scientific debugging**: Observe → Hypothesize → Predict → Experiment → Conclude. Form a specific, falsifiable hypothesis. Test one variable at a time. Record each cycle in the hypothesis log (`references/hypothesis-log-template.md`). Refuted hypotheses are progress — they narrow the search space.

- **Git bisect**: binary search through commits between a known-good and known-bad to find the introducing commit in $O(\log N)$ steps. Read the introducing commit to understand WHY it broke.

- **Five Whys**: ask "why" iteratively to trace the causal chain from symptom to root cause. Stop when you reach a cause that's directly actionable.

### 4.5 Document root cause

Update the fix plan with:

```markdown
## Root Cause

**Mechanism**: <exact explanation of why the bug occurs>
**Introduced by**: <commit hash, change, or condition>
**Why it wasn't caught**: <missing test, uncovered edge case, etc.>
```

The root cause documentation serves two purposes: it guides the minimal fix (Step 5), and it helps future agents understand the failure mode when reading the archived plan.

---

## Step 5 — Minimal Fix

Apply the smallest change that addresses the root cause — not the symptom, but the underlying mechanism identified in Step 4. Minimality is a design constraint, not a suggestion: every line of change beyond the minimum creates risk of introducing new bugs and makes the fix harder to review and understand.

### 5.1 Plan the fix

Before writing code, describe the fix in the plan:

```markdown
## Fix

**Strategy**: <what will change and why>
**Files**: <list of files to modify>
**Risk**: <what could go wrong with this approach>
```

### 5.2 Implement the fix

- Change ONLY what is necessary to fix the root cause
- Do NOT refactor surrounding code — file a separate tech debt item if refactoring is needed
- Do NOT add features — even if the broken code reveals a missing capability
- Do NOT fix other bugs you discover along the way — log them in `docs/exec-plans/tech-debt-tracker.md`

### 5.3 Commit the fix

```bash
git add <changed-files>
git commit -m "fix(<scope>): <description>

refs plan: <plan-filename> step 5

Root cause: <one-line root cause summary>"
```

### 5.4 The fix scope guard

The fix scope guard prevents fix sprawl. Track these metrics during Step 5:

| Metric              | Threshold         | Action when exceeded                                               |
| ------------------- | ----------------- | ------------------------------------------------------------------ |
| Files modified      | ≤ 5               | Stop, replan — the fix may be in the wrong layer                   |
| Fix attempts        | ≤ 3               | Stop, write hypothesis log, ask user for guidance                  |
| Unrelated changes   | 0                 | Revert unrelated changes immediately                               |
| Lines changed (net) | Context-dependent | Larger than expected? Verify you're fixing root cause, not symptom |

If you hit any threshold, stop and reassess:

1. Re-read the root cause analysis — is it correct?
2. Is this the right layer to fix? Would a fix upstream or downstream be smaller?
3. Are you fixing root cause or symptom?

---

## Step 6 — Verification and Regression Protection

This step confirms the fix works and protects against the bug recurring. Both halves are mandatory — verification without regression protection leaves the codebase vulnerable to the same failure mode reappearing.

### 6.1 Run the reproduction test

```bash
<test-command targeting the reproduction test>
```

The reproduction test from Step 3 must now PASS. If it still fails, the fix is incorrect — go back to Step 4 and re-examine the root cause.

### 6.2 Add a regression test

If the reproduction test was manual (not an automated test), convert it to a permanent test now:

```
Regression test: test_<descriptive_name>
Purpose: Prevents recurrence of <bug brief title>
Covers: <the specific failure mode>
```

The regression test should:

- Be named to describe the bug, not the fix (e.g., `test_auth_rejects_expired_token`, not `test_fix_token_check`)
- Test the failure mode directly, not the implementation detail
- Include a comment referencing the fix plan for traceability

Read `references/regression-test-patterns.md` for patterns by bug type.

### 6.3 Run the full test suite

```bash
<test-command from docs/OBSERVABILITY.md>
```

Compare with the baseline from Step 1.3:

- All previously-passing tests must still pass (no regressions introduced)
- The previously-failing test that captured the bug must now pass
- The new regression test must pass
- Pre-existing failures unrelated to this bug should remain unchanged

### 6.4 Run lint and type checks

```bash
<lint-command from docs/OBSERVABILITY.md>
```

Fix any violations introduced by the fix. Do not fix pre-existing violations.

### 6.5 Self-review and control plane update

Review your own diff (`git diff <baseline-commit>..HEAD`). Check for: changes outside fix scope (fix sprawl), debug code left in, accidentally broad changes, and that the diff matches the root cause description in the plan.

If the fix changed behavior documented in AGENTS.md, ARCHITECTURE.md, or OBSERVABILITY.md, update those files. Commit control plane updates separately:

```bash
git commit -m "docs(harness): update control plane after <fix-description>"
```

---

## Step 7 — Plan Archival

The fix is done when the plan is archived, not when the code is changed. This step is shared with harness-feat.

### 7.1 Complete the fix plan

Add a completion summary with: completion date, root cause (one-line), fix summary (one-line), regression test name, PASS/FAIL status, and a paragraph covering the bug, root cause, fix, and any broader implications.

### 7.2 Move to completed and update PLANS.md

```bash
git mv docs/exec-plans/active/YYYY-MM-DD-fix-*.md \
       docs/exec-plans/completed/YYYY-MM-DD-fix-*.md
```

Update `docs/PLANS.md`: move the entry from "Active Plans" to "Completed Plans."

### 7.3 Log patterns and final commit

If the bug reveals a systemic pattern, add an entry to `docs/exec-plans/tech-debt-tracker.md` with severity, area, description, and detection source.

```bash
git add docs/exec-plans/ docs/PLANS.md
git commit -m "chore(harness): archive fix plan for <short-description>"
```

Report to the user:

```
=== Fix Complete ===

Bug: <symptom from bug brief>
Root cause: <mechanism>
Fix: <what changed>
Plan: docs/exec-plans/completed/YYYY-MM-DD-fix-short-description.md
Regression test: <test name>
Tests: <baseline count> → <new count> (added <diff>)
Previously failing: <N tests> → Now passing: <M tests>

Commits:
  1. plan(harness): add fix plan for <short-description>
  2. fix(<scope>): <fix description>
  3. chore(harness): archive fix plan for <short-description>
```

---

## Flaky test protocol

Flaky tests (non-deterministic failures) require a different diagnosis path. Suspect a flake when: the test passes sometimes and fails others on the same code, fails in CI but passes locally, or started failing without a relevant code change.

**Diagnosis approach:**

1. **Statistical reproduction**: run the test 10-20 times and record the failure rate
2. **Categorize**: timing/race condition, order-dependent, resource leak, nondeterministic input, or environment-specific
3. **Fix with determinism**: the goal is to remove non-determinism, not make it "less flaky." Accept follow-up runs for validation (as OpenAI does), but always aim for a deterministic test

---

## Diagnosis timeout and escalation

Investigation doesn't always converge. These rules prevent infinite debugging loops.

### Escalation triggers

| Trigger                                                | Action                                               |
| ------------------------------------------------------ | ---------------------------------------------------- |
| 3 hypothesis cycles with no progress                   | Write a structured hypothesis log, present to user   |
| Root cause spans multiple modules you don't understand | Ask user for domain guidance                         |
| Reproduction requires infrastructure you can't access  | Document what you need, ask user to set up           |
| Fix requires architectural change beyond bug scope     | File as tech debt, propose interim workaround        |
| Total diagnosis time exceeds reasonable bounds         | Summarize findings so far, present partial diagnosis |

### The structured escalation report

When escalating, provide: the symptom, number of hypothesis cycles attempted, confirmed findings, ruled-out hypotheses, remaining untested hypotheses with reasons they're blocked, and a specific recommendation for next steps. This ensures no investigation effort is wasted — even an incomplete diagnosis narrows the search space for whoever picks up next.

---

## Critical design constraints

These rules encode the lessons from systematic debugging research and real-world agent failure modes.

1. **Never fix without reproduction evidence.** A fix without reproduction is a guess. Even if the guess is correct, there's no way to verify it, and no way to protect against regression. The reproduction test is the foundation everything else rests on.

2. **Never fix by reverting without understanding.** Reverting to a previous working state removes the symptom but doesn't explain WHY the regression occurred. Without understanding, the same mistake will be made again. Revert is a valid temporary measure, but the investigation must continue to root cause.

3. **Minimal fix only.** Do not refactor, do not add features, do not "improve" adjacent code during a fix. Each of these activities has its own risk profile and deserves its own plan. Mixing them with a fix makes the fix harder to review, harder to revert, and harder to understand.

4. **Root cause in the plan, not just the patch.** The fix plan must document the root cause mechanism, not just the code change. "Changed line 42 from X to Y" is a patch description, not a root cause. "The comparison used `<` instead of `<=` because the boundary condition was added in commit abc123 without updating the existing check" is a root cause.

5. **Regression test is mandatory.** Every fix must leave behind a test that will fail if the bug recurs. The test is the permanent record of the failure mode — it protects the codebase after the humans and agents who understand the bug have moved on.

6. **Respect the fix scope guard.** If you're modifying more than 5 files or making more than 3 fix attempts, stop and reassess. Either the root cause analysis is wrong, or the fix belongs at a different level of abstraction.

7. **Log everything even if diagnosis fails.** A hypothesis that was tested and refuted is valuable information. Future agents who encounter the same bug will benefit from knowing what was already tried and eliminated. The hypothesis log is as important as the fix itself.

8. **Distinguish pre-existing failures from new ones.** The "known broken" baseline from Step 1.3 is your reference. If a test was failing before you started, you don't own it. If a test starts failing during your fix, you do.

---

## Adapting to bug severity

Scale the ceremony to the severity:

| Severity | Bug brief | Reproduction | Root cause    | Fix plan    | Regression test |
| -------- | --------- | ------------ | ------------- | ----------- | --------------- |
| Blocking | Full      | Required     | Full protocol | Full        | Required        |
| Degraded | Full      | Required     | Full protocol | Full        | Required        |
| Cosmetic | Brief     | Lightweight  | Targeted      | Lightweight | Recommended     |

Even cosmetic fixes get a plan file — it creates the audit trail, and the naming convention (`YYYY-MM-DD-fix-*.md`) makes fix plans distinguishable from feature plans in the archive.

---

## Reference index

| File                                     | When to read                              |
| ---------------------------------------- | ----------------------------------------- |
| `references/bug-brief-template.md`       | Step 2: structuring the bug report        |
| `references/root-cause-techniques.md`    | Step 4: choosing investigation techniques |
| `references/fix-plan-template.md`        | Step 3: creating the fix plan             |
| `references/regression-test-patterns.md` | Step 6: writing the regression test       |
| `references/hypothesis-log-template.md`  | Step 4: recording investigation cycles    |
