# Systematic Debugging

Use this reference inside `harness-fix` when diagnosing bugs, regressions, flaky paths, build failures, or unexpected behavior.

## Core Rules

```text
NO FIX WITHOUT REPRODUCTION EVIDENCE
NO ROOT CAUSE CLAIM WITHOUT EXPLICIT EVIDENCE
THREE FAILED FIX ATTEMPTS MEAN STOP AND REPLAN
```

## Phase 1: Root Cause Investigation

Before proposing fixes:

1. Read the full error message, stack trace, logs, and failing assertion.
2. Reproduce consistently or document why reproduction is currently bounded.
3. Check recent changes, environment differences, dependency changes, and configuration.
4. Trace data flow from symptom back to source.
5. Add diagnostic instrumentation at component boundaries when the system has multiple layers.

## Phase 2: Pattern Analysis

Find what works before changing what is broken:

- locate similar working code in the same repository
- compare broken and working paths
- list differences without dismissing small ones
- read relevant reference implementations completely when applying a known pattern

## Phase 3: Hypothesis Testing

Use a scientific loop:

1. Write one falsifiable hypothesis.
2. Predict what evidence would confirm or refute it.
3. Test one variable at a time.
4. Record the result in the fix plan.
5. If refuted, form a new hypothesis instead of stacking changes.

## Phase 4: Minimal Fix

Only after root cause evidence:

1. Create or identify the failing reproduction.
2. Implement one fix that addresses the root cause.
3. Run the reproduction.
4. Run relevant regression and suite checks.
5. If the fix fails, revert or isolate it before the next attempt.

## Escalation

After three failed fix attempts, stop and replan. Repeated failure often means the architecture, boundary, or initial diagnosis is wrong.

## Related References

- `root-cause-tracing.md`
- `condition-based-waiting.md`
- `defense-in-depth.md`
