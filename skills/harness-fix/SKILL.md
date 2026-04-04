---
name: harness-fix
description: >
  Plan and execute bug fixes, regression repair, incident remediation,
  flaky-path debugging, and evidence-driven investigation in
  repositories that already use Harness Engineering control plane
  artifacts such as `docs/PLANS.md`, `docs/exec-plans/active`,
  `docs/OBSERVABILITY.md`, `docs/generated/harness-manifest.md`, and
  repo-local `python3 scripts/check_harness.py`. Use when the user
  reports a broken behavior and Codex should rewrite the bug report,
  run harness preflight, reproduce or bound the failure, create or
  update a fix plan, apply the smallest justified repair, add
  regression protection, sync `docs/PLANS.md`, and archive the plan
  deterministically. Especially relevant for prompts such as
  `$harness-fix`, `修复...`, `这个报错`, `为什么坏了`, or `排查回归`.
---

# Harness Fix

Turn rough bug reports into evidence-driven repair work that stays
inside the repository's Harness control plane instead of devolving into
random patching.

## Core Commitments

- Rewrite the bug report before changing code.
- Run harness preflight before substantive repair work.
- Prefer reproduction and evidence over intuition.
- Fix the narrowest root cause that restores the broken invariant.
- Close the loop with deterministic plan sync and archive steps.

## Authority Ladder

Use this order whenever inputs conflict:

1. Observable user impact and intended behavior
2. Repository hard constraints such as root and local `AGENTS.md`,
   architecture docs, security rules, observability docs, and harness checks
3. Current source code, tests, logs, fixtures, generated facts, and runtime evidence
4. Existing fix history, execution plans, and design docs
5. Primary external documentation for unstable facts
6. Your assumptions

Treat the user's diagnosis as a hypothesis unless the evidence confirms
it.

## Start Sequence

1. Read the repository root `AGENTS.md`.
2. Read `docs/PLANS.md`.
3. If present, run or inspect `python3 scripts/check_harness.py`.
4. If present, read `docs/generated/harness-manifest.md`.
5. Use the root routing table to read only the failing surface docs,
   especially:
   - `docs/OBSERVABILITY.md`
   - task-type docs
   - the closest local `AGENTS.md`
6. Inspect the failing code path, tests, logs, and recent related files.
7. Load these references and scripts when needed:
   - `references/bug-brief-rubric.md`
   - `references/refinex-harness-contract.md`
   - `references/fix-exec-plan-template.md`
   - `scripts/init_exec_plan.py`
   - `scripts/sync_plan_state.py`
   - `scripts/archive_exec_plan.py`

## Workflow

### 1. Rewrite the Bug Report Before Acting

Convert the raw request into an evidence-oriented bug brief that keeps
the symptom precise and the repair target testable.

Include:

- symptom
- expected behavior
- observed behavior
- user impact
- reproduction path or strongest available evidence
- likely affected surfaces
- validation target
- docs and generated artifacts to update

### 2. Run Harness Preflight

Before coding, confirm whether the repository exposes:

- `scripts/check_harness.py`
- `docs/generated/harness-manifest.md`
- `docs/OBSERVABILITY.md`
- `docs/exec-plans/tech-debt-tracker.md`

If the harness baseline is missing or visibly broken, do not silently
work around it. Prefer invoking `harness-bootstrap` or `harness-garden`
first, or record the gap explicitly in the active plan.

### 3. Reproduce or Bound the Failure

- Prefer a deterministic reproduction, failing test, or traceable log.
- If full reproduction is impossible, document the best available
  evidence and the confidence level of the hypothesis.
- Do not apply a blind patch when the failure mode is still undefined
  unless you are performing an explicitly labeled mitigation.

### 4. Create or Update the Fix Plan

- If an active plan already covers the issue, update it.
- Otherwise initialize a plan with `scripts/init_exec_plan.py`.
- Sync `docs/PLANS.md` with `scripts/sync_plan_state.py` unless the file
  is unmanaged.

Preferred commands:

```bash
python3 scripts/init_exec_plan.py --repo <repo-root> --title "<bug title>"
python3 scripts/sync_plan_state.py --repo <repo-root>
```

### 5. Isolate Root Cause and Repair Narrowly

- Trace the broken invariant backward from the symptom.
- Prefer the smallest justified fix that restores correct behavior.
- Avoid bundling unrelated refactors or cleanup unless the evidence
  demands it.
- When the issue is really a harness weakness, record that in the plan
  or `docs/exec-plans/tech-debt-tracker.md`.

### 6. Add Regression Protection and Verify

- Add or update the strongest affordable guardrail: test, fixture,
  assertion, log check, or reproducible command.
- Review and validate in this order:
  1. Security
  2. Correctness
  3. Performance
  4. Readability

### 7. Close the Loop Deterministically

- Archive only when reproduction or validation evidence shows the issue
  is resolved.
- Use `scripts/archive_exec_plan.py` to prepend the completion header,
  move the file into `completed/`, and resync `docs/PLANS.md`.
- If `docs/PLANS.md` is unmanaged, preserve it and surface the required
  manual update instead of forcing a rewrite.

## Preferred Commands

```bash
python3 scripts/init_exec_plan.py --repo <repo-root> --title "<bug title>"
python3 scripts/sync_plan_state.py --repo <repo-root>
python3 scripts/archive_exec_plan.py --repo <repo-root> --plan <active-plan> --summary "<done>"
python3 scripts/run_fixture_tests.py
```

## Guardrails

- Do not accept a root-cause claim without evidence.
- Do not turn a fix task into a broad refactor unless the evidence demands it.
- Do not skip plan updates just because the code change is small.
- Do not archive a plan if the failure is only mitigated and not resolved.
- Do not trust stale documentation over current failing behavior, source code, and runtime evidence.

## Not for This Skill

Use `harness-feat` instead when the work is primarily new capability,
feature expansion, or structured refactor rather than debugging.
