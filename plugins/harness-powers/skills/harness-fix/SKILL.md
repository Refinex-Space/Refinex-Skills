---
name: harness-fix
description: >-
  Own bug, regression, incident, and flaky-path repair inside a Harness Powers
  control plane. Use when repository work requires a bug brief, reproduction
  evidence, root-cause isolation, minimal fix, regression protection, plan
  archival, and handoff through harness-verify.
license: MIT
---

# harness-fix

Diagnose and repair broken behavior with evidence. This skill is the Harness Powers lifecycle owner for bugs, regressions, incidents, build failures, and flaky paths.

**Announce at start:** `I'm using harness-fix to reproduce, isolate, and repair this failure.`

---

## Iron Laws

```text
NO FIX WITHOUT REPRODUCTION EVIDENCE
NO ROOT CAUSE CLAIM WITHOUT EXPLICIT EVIDENCE
THREE FAILED FIX ATTEMPTS MEAN STOP AND REPLAN
```

If any rule is violated, the workflow has degraded into guessing.

---

## Ownership

Use `harness-fix` when:

- the user reports broken behavior, a failing test, a regression, or an incident
- behavior is flaky, timing-dependent, or environment-specific
- an implementation attempt introduced unexpected failures
- root cause and regression protection matter

Do not use it for:

- new feature work -> use `harness-feat`
- unclear product/design intent -> use `harness-brainstorm`
- code review only -> use `harness-review`
- completion claims -> use `harness-verify`

---

## Required Flow

Follow these steps in order.

1. **Preflight**
   - Read root `AGENTS.md`.
   - Read relevant module `AGENTS.md` files when present.
   - Read `docs/PLANS.md`, `docs/ARCHITECTURE.md`, and `docs/OBSERVABILITY.md` when present.
   - Run `python3 scripts/check_harness.py` when available and record failures.
   - Establish the known-broken baseline with the documented test command.

2. **Bug Brief**
   - Capture symptom, expected behavior, reproduction, affected scope, severity, type, and assumptions.
   - Use `references/bug-brief-template.md`.
   - Ask for missing reproduction or expected behavior when the report is too vague.

3. **Reproduction**
   - Write or identify a reproduction that fails now.
   - Prefer an automated test; use precise manual steps when automation is not practical.
   - Record the failing command, output, and reason in the fix plan.
   - Create an active fix plan under `docs/exec-plans/active/` and register it in `docs/PLANS.md`.

4. **Root Cause Isolation**
   - Use `references/systematic-debugging.md` and `references/root-cause-techniques.md`.
   - Use `references/root-cause-tracing.md` when the symptom is deep in a call stack.
   - Use `references/condition-based-waiting.md` for timing or flaky behavior.
   - Write falsifiable hypotheses and test one variable at a time.
   - Record refuted hypotheses; they are evidence, not waste.

5. **Minimal Fix**
   - Apply the smallest change that addresses the documented root cause.
   - Do not bundle opportunistic refactors.
   - Every changed line must trace to root cause evidence or regression protection.
   - If a fix attempt fails, isolate or revert it before the next attempt.

6. **Regression Protection And Verification**
   - Run the reproduction and confirm it now passes.
   - Add or preserve a regression test where practical.
   - Run relevant suite/lint/type checks and compare against the known-broken baseline.
   - Use `harness-review` for risky or broad fixes.

7. **Archive And Handoff**
   - Complete the root-cause, fix, regression, and evidence sections in the plan.
   - Move the fix plan to `docs/exec-plans/completed/` when done.
   - Update `docs/PLANS.md`.
   - Use `harness-verify` before any final success claim.
   - Use `harness-finish` for merge, PR, keep, or discard decisions.

---

## Diagnostic Guardrails

- **Explicit assumptions:** environment, input, state, and timing assumptions must be written down.
- **Falsifiable hypotheses:** each suspected cause must be testable.
- **Surgical repair:** fix the mechanism, not adjacent symptoms.
- **Proof-matched verification:** final evidence must prove the bug is fixed, not merely that nearby code still passes.

---

## Escalation

Stop and replan when:

- three fix attempts fail
- reproduction cannot be established or bounded
- the apparent fix requires broad architecture changes
- evidence contradicts the current root-cause theory
- the fix would conflict with an active plan in `docs/PLANS.md`

---

## Reference Index

| Reference | Use |
| --- | --- |
| `references/bug-brief-template.md` | Structuring the bug report |
| `references/fix-plan-template.md` | Active fix plan shape |
| `references/hypothesis-log-template.md` | Recording hypothesis loops |
| `references/systematic-debugging.md` | Root-cause investigation discipline |
| `references/root-cause-techniques.md` | Choosing diagnosis techniques |
| `references/root-cause-tracing.md` | Backward tracing from symptom to source |
| `references/condition-based-waiting.md` | Flaky/timing investigation |
| `references/defense-in-depth.md` | Follow-up hardening after root cause |
| `references/regression-test-patterns.md` | Regression protection |
