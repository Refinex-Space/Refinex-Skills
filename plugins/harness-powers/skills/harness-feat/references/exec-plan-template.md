# Execution Plan Template

Use this template when creating a new execution plan in Step 2. Copy the structure
below into `docs/exec-plans/active/YYYY-MM-DD-short-description.md` and fill in
each section.

---

```markdown
# Execution Plan: <Short Description>

Created: YYYY-MM-DD
Status: Active
Author: agent

## Objective

<One sentence: what will be different when this task is done?>

## Scope

**In scope:**
- <module or directory 1>
- <module or directory 2>

**Out of scope:**
- <explicitly excluded concern 1>
- <explicitly excluded concern 2>

## Constraints

<Architectural rules from AGENTS.md that apply to this task>

- <constraint 1>
- <constraint 2>

## Acceptance Criteria

Each criterion must be objectively verifiable. "Works correctly" is not a criterion.
"GET /api/users returns 200 with a JSON array" is.

- [ ] AC-1: <specific, testable condition>
- [ ] AC-2: <specific, testable condition>
- [ ] AC-3: <specific, testable condition>

## Risk Notes

| Risk                         | Likelihood | Mitigation                      |
| ---------------------------- | ---------- | ------------------------------- |
| <what could go wrong>        | Low/Med/Hi | <what to do if it happens>      |

## Implementation Steps

### Step 1: <action verb + object>

**Files:** `path/to/file1`, `path/to/file2`
**Verification:** <how to confirm this step worked>

Status: ⬜ Not started
Evidence:
Deviations:

### Step 2: <action verb + object>

**Files:** `path/to/file3`
**Verification:** <how to confirm this step worked>

Status: ⬜ Not started
Evidence:
Deviations:

### Step N: <action verb + object>

**Files:** `path/to/fileN`
**Verification:** <how to confirm this step worked>

Status: ⬜ Not started
Evidence:
Deviations:

## Progress Log

| Step | Status | Evidence                        | Notes        |
| ---- | ------ | ------------------------------- | ------------ |
| 1    | ⬜     |                                 |              |
| 2    | ⬜     |                                 |              |

## Decision Log

Record any decisions made during implementation that deviated from or clarified the
original plan.

| Decision | Context                          | Alternatives Considered | Rationale |
| -------- | -------------------------------- | ----------------------- | --------- |

## Completion Summary

<!-- Fill in when archiving the plan -->

Completed:
Duration: <N> steps
All acceptance criteria: PASS / FAIL

Summary:
```

---

## Status icons

Use these consistently in the plan:

| Icon | Meaning     |
| ---- | ----------- |
| ⬜   | Not started |
| 🔄   | In progress |
| ✅   | Done        |
| ❌   | Failed      |
| ⏪   | Reverted    |

## Step sizing guidance

A well-sized step:

- **Touches 1-5 files** — more than 5 files suggests the step should be split
- **Has one verification criterion** — if you need multiple checks, consider splitting
- **Takes 2-5 minutes of focused agent work** — shorter is fine; longer means split
- **Can be committed alone without breaking the repo** — if reverting this step would leave things broken, it was too big or not atomic enough

## Lightweight plan (for trivial tasks)

For 1-2 file changes, use this minimal format:

```markdown
# Execution Plan: <Short Description>

Created: YYYY-MM-DD
Status: Active

## Objective

<One sentence>

## Acceptance Criteria

- [ ] AC-1: <criterion>

## Steps

1. <what to do> → verify: <how>
2. <what to do> → verify: <how>

## Completion Summary
```

Even trivial tasks get a plan file — it creates the audit trail.
