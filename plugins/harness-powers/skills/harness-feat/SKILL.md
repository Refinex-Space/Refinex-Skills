---
name: harness-feat
description: >-
  Own feature delivery, capability work, and structured refactors inside a
  Harness Powers control plane. Use when repository work needs preflight,
  sprint contract, active execution plan ownership, incremental implementation,
  TDD-informed verification, plan archival, and handoff through harness-verify.
license: MIT
---

# harness-feat

Deliver features and structured refactors inside the Harness Powers control plane.

This is a lifecycle owner, not a domain skill. It keeps repository work tied to `AGENTS.md`, `docs/PLANS.md`, `docs/exec-plans/`, preflight evidence, and final verification. Domain skills such as `harness-frontend` may support implementation, but they do not own the feature lifecycle.

**Announce at start:** `I'm using harness-feat to deliver this work inside the Harness Powers control plane.`

---

## Ownership

Use `harness-feat` when:

- the user asks for a new feature, enhancement, or structured refactor
- the work changes repository behavior or architecture
- acceptance criteria need to be negotiated before implementation
- the work should leave an auditable execution plan

Do not use it for:

- unclear product/design intent -> use `harness-brainstorm`
- plan-only work -> use `harness-plan`
- existing plan execution -> use `harness-execute`
- bugs, regressions, flaky paths, or incidents -> use `harness-fix`
- completion claims -> use `harness-verify`

---

## Required Flow

Follow these steps in order.

1. **Preflight**
   - Read root `AGENTS.md`.
   - Read relevant module `AGENTS.md` files when present.
   - Read `docs/PLANS.md`, `docs/ARCHITECTURE.md`, and `docs/OBSERVABILITY.md` when present.
   - Run `python3 scripts/check_harness.py` when available.
   - Establish the current test baseline using the documented command.

2. **Sprint Contract**
   - Rewrite the user's request into objective, scope, non-scope, constraints, assumptions, and acceptance criteria.
   - Surface material ambiguity before planning.
   - Prefer the smallest design that satisfies the objective.
   - Get confirmation when the contract changes user-visible scope.

3. **Execution Plan**
   - Create or update an active plan under `docs/exec-plans/active/`.
   - Register it in `docs/PLANS.md`.
   - Make each step small, scoped, and evidence-backed.
   - Do not use alternate planning directories.
   - Commit or otherwise version the plan before implementation when the repository workflow allows it.

4. **Incremental Implementation**
   - Execute one plan step at a time.
   - Use `references/tdd-discipline.md` for behavior changes.
   - Use `references/testing-anti-patterns.md` before adding mocks or test-only hooks.
   - If TDD does not fit, define an equivalent verification before editing.
   - Keep every changed line traceable to an acceptance criterion, plan step, or required regression protection.
   - If delegated, keep the active plan as the single source of truth and use `harness-dispatch`.

5. **Verification**
   - Check acceptance criteria one by one.
   - Run targeted tests and relevant suite/lint/type checks.
   - Update the control plane if the work changed architecture, commands, modules, or docs.
   - Use `harness-review` for review checkpoints when risk or plan size warrants it.

6. **Archive And Handoff**
   - Complete the active plan evidence log.
   - Move the plan to `docs/exec-plans/completed/` when the work is complete.
   - Update `docs/PLANS.md`.
   - Use `harness-verify` before any final success claim.
   - Use `harness-finish` for merge, PR, keep, or discard decisions.

---

## Behavioral Guardrails

- **Assumption ledger:** write down assumptions that affect scope, architecture, or acceptance criteria.
- **Simplicity checkpoint:** avoid speculative abstractions, extra configurability, and broad refactors.
- **Surgical diff discipline:** every changed line should map to a plan step or proof obligation.
- **Goal-evidence pairing:** every meaningful task needs a proving command, test, inspection, or artifact check.

---

## Failure Handling

Stop and reroute when:

- `scripts/check_harness.py` fails in a way that makes the control plane untrustworthy -> use `harness-garden`
- the request is actually a bug or regression -> use `harness-fix`
- implementation reveals a different design is needed -> update the sprint contract and plan before continuing
- verification fails repeatedly -> stop, record evidence, and ask whether to switch to `harness-fix`

---

## Reference Index

| Reference | Use |
| --- | --- |
| `references/preflight-checklist.md` | Control-plane orientation and baseline checks |
| `references/exec-plan-template.md` | Active execution plan shape |
| `references/tdd-discipline.md` | RED/GREEN/REFACTOR discipline for behavior changes |
| `references/testing-anti-patterns.md` | Mocking and test-design traps |
| `references/commit-conventions.md` | Commit message and staging guidance |
