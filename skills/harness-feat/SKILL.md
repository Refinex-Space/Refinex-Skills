---
name: harness-feat
description: >
  Plan and execute new feature work, capability delivery, and structured
  refactors in repositories that already use Harness Engineering control
  plane artifacts such as `docs/PLANS.md`, `docs/exec-plans/active`,
  `docs/OBSERVABILITY.md`, `docs/generated/harness-manifest.md`, and
  repo-local `python3 scripts/check_harness.py`. Use when the user gives
  a rough implementation goal and Codex should rewrite the task, run
  harness preflight, create or update a live execution plan, execute in
  small validated slices, sync `docs/PLANS.md`, and archive the plan
  deterministically. Especially relevant for prompts such as
  `$harness-feat`, `任务：实现...`, `新增...`, `重构...`, or `做这个功能`.
---

# Harness Feat

Turn rough net-new work into a constrained, auditable execution loop
that is driven by the repository's Harness control plane instead of
human reminder text.

## Core Commitments

- Rewrite the user's task before taking action.
- Run harness preflight before substantive coding.
- Keep repository invariants stricter than implementation details.
- Execute in small slices with explicit validation evidence.
- Close the loop with deterministic plan sync and archive steps.

## Authority Ladder

Use this order whenever inputs conflict:

1. The user's real goal and business intent
2. Repository hard constraints such as root and local `AGENTS.md`,
   architecture docs, security rules, observability docs, and harness checks
3. Current source code, tests, generated facts, logs, and runtime evidence
4. Existing execution plans and design documents
5. Primary external documentation for unstable facts
6. Your assumptions

Treat user implementation suggestions as hypotheses, not binding
instructions, when they conflict with higher-authority sources.

## Start Sequence

1. Read the repository root `AGENTS.md`.
2. Read `docs/PLANS.md`.
3. If present, run or inspect `python3 scripts/check_harness.py`.
4. If present, read `docs/generated/harness-manifest.md`.
5. Use the root routing table to read only the relevant docs, especially:
   - `docs/OBSERVABILITY.md`
   - task-type docs
   - the closest local `AGENTS.md`
6. Inspect the relevant code before deciding implementation.
7. Load these references and scripts when needed:
   - `references/prompt-optimization-rubric.md`
   - `references/refinex-harness-contract.md`
   - `references/feature-exec-plan-template.md`
   - `scripts/init_exec_plan.py`
   - `scripts/sync_plan_state.py`
   - `scripts/archive_exec_plan.py`

## Workflow

### 1. Rewrite the Task Before Acting

Create an optimized task brief before coding. Preserve user intent while
removing ambiguity, accidental implementation bias, and scope drift.

Include:

- outcome
- why it matters
- scope
- non-goals
- hard constraints and invariants
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

### 3. Create or Update the Active Plan

- If an active execution plan already covers the work, extend it.
- Otherwise initialize a plan with `scripts/init_exec_plan.py`.
- Sync `docs/PLANS.md` with `scripts/sync_plan_state.py` unless the file
  is unmanaged.
- Keep `docs/PLANS.md` short. The execution plan holds the real work log.

Preferred commands:

```bash
python3 scripts/init_exec_plan.py --repo <repo-root> --title "<short task title>"
python3 scripts/sync_plan_state.py --repo <repo-root>
```

### 4. Execute in Small Validated Slices

- Prefer the smallest slice that improves the repository while keeping
  the task moving.
- After each slice, update the active plan with progress, decisions,
  risks, and evidence.
- When behavior, runtime surfaces, or public interfaces change, sync the
  corresponding docs or generated-fact workflow.

### 5. Verify as a Distinct Pass

Review and validate in this order:

1. Security
2. Correctness
3. Performance
4. Readability

### 6. Close the Loop Deterministically

- Archive only when acceptance criteria are satisfied and validation
  evidence is recorded.
- Use `scripts/archive_exec_plan.py` to prepend the completion header,
  move the file into `completed/`, and resync `docs/PLANS.md`.
- If `docs/PLANS.md` is unmanaged, preserve it and surface the required
  manual update instead of forcing a rewrite.

## Preferred Commands

```bash
python3 scripts/init_exec_plan.py --repo <repo-root> --title "<short task title>"
python3 scripts/sync_plan_state.py --repo <repo-root>
python3 scripts/archive_exec_plan.py --repo <repo-root> --plan <active-plan> --summary "<done>"
python3 scripts/run_fixture_tests.py
```

## Guardrails

- Do not start substantive coding before there is a current plan artifact unless the task is obviously trivial.
- Do not let a plan become a diary. Record only decisions, progress, risks, and evidence that reduce future rediscovery.
- Do not trust stale docs over source code, tests, logs, and generated facts.
- Do not modify generated files by hand when the repository expects them to be script-generated.
- Do not use broad web search as a substitute for reading the repo.
- When a failure reveals missing harness capacity, record it in the active plan or `docs/exec-plans/tech-debt-tracker.md`.

## Not for This Skill

Use `harness-fix` instead when the primary job is debugging,
reproducing, or repairing a bug, regression, flaky path, or incident.
