# Fix Plan Template

Use this template when creating a fix plan in Step 3. Copy the structure below
into `docs/exec-plans/active/YYYY-MM-DD-fix-short-description.md`.

The fix plan differs from a feature execution plan because it includes diagnosis
artifacts: bug brief, reproduction evidence, hypothesis log, and root cause
analysis. These are not optional — they are the evidence chain that separates
an engineered fix from a lucky guess.

---

```markdown
# Fix Plan: <Short Description>

Created: YYYY-MM-DD
Status: Active
Author: agent
Type: fix

## Bug Brief

**Symptom**: <exact observable behavior>
**Expected**: <what should happen>
**Severity**: Blocking / Degraded / Cosmetic
**Type**: Regression / New bug / Flaky / Environment-specific

### Reproduction

<Steps to reproduce, or name of the reproduction test>

Reproduction evidence: <test name and output, or description of manual reproduction>

## Root Cause

<!-- Fill in during Step 4 -->

**Mechanism**: <why the bug occurs>
**Introduced by**: <commit, change, or condition>
**Why it wasn't caught**: <missing test, uncovered edge case, etc.>

## Hypothesis Log

<!-- Record each investigation cycle here -->

### Hypothesis #1: <description>

Prediction: <if this hypothesis is correct, then...>
Experiment: <what was done to test>
Result: <observation>
Conclusion: CONFIRMED / REFUTED

### Hypothesis #2: <description>

Prediction:
Experiment:
Result:
Conclusion:

## Fix

**Strategy**: <what will change and why>
**Files**: <list of files to modify>
**Risk**: <what could go wrong>

### Steps

#### Step 1: <action>

**Files:** `path/to/file`
**Verification:** <how to confirm>

Status: ⬜ Not started
Evidence:
Deviations:

#### Step 2: Write regression test

**Files:** `path/to/test_file`
**Verification:** Test passes after fix, would fail without it

Status: ⬜ Not started
Evidence:
Deviations:

## Verification

- [ ] Reproduction test now passes
- [ ] Regression test added and passes
- [ ] Full test suite passes (no new failures)
- [ ] Lint and type checks pass
- [ ] Diff reviewed — only fix-related changes present
- [ ] Pre-existing failures unchanged

## Progress Log

| Step       | Status | Evidence         | Notes |
| ---------- | ------ | ---------------- | ----- |
| Reproduce  | ⬜     |                  |       |
| Root cause | ⬜     |                  |       |
| Fix        | ⬜     |                  |       |
| Verify     | ⬜     |                  |       |
| Regression | ⬜     |                  |       |

## Completion Summary

<!-- Fill in when archiving -->

Completed:
Root cause: <one-line summary>
Fix: <one-line summary>
Regression test: <test name>
All verification criteria: PASS / FAIL

Summary:
```

---

## Status icons

| Icon | Meaning     |
| ---- | ----------- |
| ⬜   | Not started |
| 🔄   | In progress |
| ✅   | Done        |
| ❌   | Failed      |
| ⏪   | Reverted    |

## Lightweight fix plan (for cosmetic bugs)

For simple, low-severity fixes:

```markdown
# Fix Plan: <Short Description>

Created: YYYY-MM-DD
Status: Active
Type: fix

## Bug Brief

**Symptom**: <symptom>
**Expected**: <expected>
**Severity**: Cosmetic

## Root Cause

<Brief explanation>

## Steps

1. <what to do> → verify: <how>
2. Add regression test → verify: test passes

## Completion Summary
```

Even cosmetic fixes need a plan — the naming convention (`fix-` prefix) makes
them distinguishable from feature plans in the archive.
