# TDD Discipline

Use this reference when a Harness feature, refactor, or behavior change needs executable proof before implementation.

## Core Rule

```text
NO PRODUCTION BEHAVIOR CHANGE WITHOUT A FAILING TEST OR EQUIVALENT PROOF FIRST
```

For behavior changes, the default proof is a failing automated test. For generated code, configuration, documentation, or infrastructure changes where a failing test does not fit, write an equivalent verification step before changing implementation.

## Red / Green / Refactor

1. **RED:** write one focused test that describes the desired behavior.
2. **Verify RED:** run it and confirm it fails for the expected reason.
3. **GREEN:** write the smallest implementation that passes.
4. **Verify GREEN:** run the targeted test and relevant suite.
5. **REFACTOR:** clean up while keeping tests green.

## Good Test Requirements

- Tests one behavior.
- Has a clear behavior name.
- Exercises real code rather than mock behavior.
- Fails before implementation.
- Protects an acceptance criterion or regression risk from the active plan.

## When Not To Force TDD

Record an explicit verification substitute when the work is documentation-only, generated code, static configuration, repository scaffolding, or a pure mechanical move with no behavior change.

The substitute must still prove the plan step, such as a validator command, schema check, link check, smoke command, or rendered artifact inspection.

## Red Flags

- "I'll add tests after."
- "This is too small to test."
- "The test passed immediately."
- "I changed production code first, but I remember why."
- "The mock was easier to assert."

If the test passes immediately, it is not proving missing behavior. Fix the test before implementing.
