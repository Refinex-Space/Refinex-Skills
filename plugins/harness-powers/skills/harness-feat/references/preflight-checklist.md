# Preflight Checklist

Run this checklist before any feature work begins. Every item must pass before
proceeding to Step 2 (Task Rewriting). The purpose is to establish a known-good
baseline and orient the agent within the control plane.

---

## Checklist

### 1. Control plane artifacts exist

| Check                                          | Pass condition                              | If missing → action                  |
| ---------------------------------------------- | ------------------------------------------- | ------------------------------------- |
| Root `AGENTS.md` exists                         | File present at repo root                   | Stop. Suggest `harness-bootstrap`.    |
| `docs/PLANS.md` exists                          | File present                                | Stop. Suggest `harness-bootstrap`.    |
| `docs/OBSERVABILITY.md` exists                  | File present                                | Stop. Suggest `harness-bootstrap`.    |
| `docs/generated/harness-manifest.md` exists     | File present                                | Stop. Suggest `harness-bootstrap`.    |
| `scripts/check_harness.py` exists               | File present and executable                 | Stop. Suggest `harness-bootstrap`.    |

If ANY of these are missing, the repository does not have a functioning harness.
Do not attempt to create them during a feature task — that's harness-bootstrap's job.

### 2. Preflight script passes

```bash
python3 scripts/check_harness.py
```

| Result      | Action                                                              |
| ----------- | ------------------------------------------------------------------- |
| All checks pass | Proceed                                                         |
| Warnings only   | Proceed. Note warnings in the execution plan under Risk Notes   |
| Errors          | Stop. Report errors. Suggest `harness-garden` to repair drift   |
| Script crash    | Stop. Report the error. The harness itself needs repair         |

### 3. Read the control plane

Read these files and extract key information:

| File                       | Extract                                                     |
| -------------------------- | ----------------------------------------------------------- |
| Root `AGENTS.md`           | Repo map, key patterns, module guide, documentation index   |
| Target module `AGENTS.md`  | Module-specific conventions, boundaries, test commands       |
| `docs/PLANS.md`            | Active plans list — check for conflicts                     |
| `docs/ARCHITECTURE.md`     | Architectural constraints, dependency directions            |
| `docs/OBSERVABILITY.md`    | Build, test, lint, run commands                             |

### 4. Establish test baseline

Run the test command from `docs/OBSERVABILITY.md`:

```bash
<test-command>
```

Record:
- **Exit code**: 0 = green, non-zero = tests already failing
- **Test count**: total tests, passed, failed, skipped
- **Failing tests** (if any): list them — these are pre-existing and not your fault

This baseline is referenced throughout the implementation to ensure no regressions.

### 5. Check for conflicting active plans

Read the "Active Plans" section of `docs/PLANS.md`.

| Situation                                  | Action                                        |
| ------------------------------------------ | --------------------------------------------- |
| No active plans                            | Proceed                                       |
| Active plans in unrelated modules          | Proceed. Note them in your plan               |
| Active plans in overlapping modules        | Adjust scope to avoid shared files, or wait   |
| Active plans targeting the same files      | Stop. Report the conflict to the user         |

### 6. Verify build health

If `docs/OBSERVABILITY.md` defines a build command, run it:

```bash
<build-command>
```

A failing build blocks feature work. Report the failure and stop.

---

## Quick-reference pass/fail summary

All six checks must pass (or be noted as acceptable) before proceeding:

```
[ ] 1. Control plane artifacts exist
[ ] 2. Preflight script passes
[ ] 3. Control plane read and understood
[ ] 4. Test baseline recorded
[ ] 5. No conflicting active plans
[ ] 6. Build health verified
```

If any check fails with a "Stop" action, do not proceed to Step 2. Report the
failure to the user with a clear recommendation (typically: run harness-bootstrap
or harness-garden first).

---

## Common failure patterns

| Symptom                                  | Likely cause                        | Fix                                      |
| ---------------------------------------- | ----------------------------------- | ---------------------------------------- |
| `check_harness.py` not found             | Repo never bootstrapped             | Run `harness-bootstrap`                  |
| `check_harness.py` reports many errors   | Control plane drifted               | Run `harness-garden`                     |
| Tests fail before any changes            | Pre-existing failures               | Record baseline; proceed with caution    |
| Build command not in OBSERVABILITY.md    | Incomplete bootstrap                | Check manually; consider garden pass     |
| Multiple active plans on same files      | Parallel work collision             | Coordinate with user                     |
| AGENTS.md references stale modules       | Repo restructured without update    | Run `harness-garden`                     |
