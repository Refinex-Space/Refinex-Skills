# TDD Workflow

Guidance on when and how to apply test-driven development within harnessed
feature work. TDD is preferred but not universally applicable — this document
clarifies when to use it, when to skip it, and how to adapt it.

---

## When TDD applies

Use TDD (RED → GREEN → REFACTOR) when you are writing code that has **observable
behavior** — meaning you can write a test that fails before you implement and passes
after.

| Situation                            | TDD? | Reasoning                                       |
| ------------------------------------ | ---- | ----------------------------------------------- |
| New function, method, or class       | Yes  | Behavior is clearly specifiable                 |
| New API endpoint                     | Yes  | Input → output contract is testable             |
| Bug fix with reproducible steps      | Yes  | Write the failing test that captures the bug    |
| Data transformation or parsing       | Yes  | Input → output mapping is directly testable     |
| Business rule implementation         | Yes  | Rules translate directly to test cases          |
| Algorithm implementation             | Yes  | Known inputs → expected outputs                 |
| Configuration changes                | No   | No behavioral contract to test against          |
| Infrastructure/DevOps changes        | No   | Side effects often not unit-testable            |
| Documentation updates                | No   | Not executable                                  |
| Dependency version bumps             | No   | Existing tests cover behavior                   |
| UI layout changes (no logic)         | No   | Visual verification, not assertion-based        |
| Database migration scripts           | Maybe| Test the migration's effect on schema/data      |
| Refactoring (no behavior change)     | No   | Existing tests should already cover the behavior|

---

## The RED → GREEN → REFACTOR cycle

### RED — Write a failing test

Write one test that describes the expected behavior. The test must:
- **Fail for the right reason** — it should fail because the behavior doesn't
  exist yet, not because of a syntax error or import problem
- **Be specific** — test one thing, not "the whole feature"
- **Name itself clearly** — the test name describes the behavior being verified

```python
# Example: testing a new utility function
def test_parse_duration_converts_seconds():
    assert parse_duration("30s") == 30

def test_parse_duration_converts_minutes():
    assert parse_duration("5m") == 300
```

Run the test and confirm it fails:

```bash
<test-command> -k test_parse_duration
```

Record the failure in the plan step evidence: "RED: test_parse_duration fails with
NameError (function not yet defined)"

### GREEN — Write minimal code to pass

Write the simplest implementation that makes the test pass. Do not anticipate
future requirements — solve only what the current test demands.

Run the test and confirm it passes:

```bash
<test-command> -k test_parse_duration
```

Record in the plan step evidence: "GREEN: test_parse_duration passes (2 tests)"

### REFACTOR — Clean up without changing behavior

Now that you have a passing test, you can safely refactor the implementation.
The test acts as a safety net — if you break behavior during refactoring, the test
catches it.

Common refactoring moves:
- Extract helper functions
- Rename for clarity
- Remove duplication
- Simplify conditionals

After refactoring, run the test again to confirm nothing broke.

---

## Test placement

Follow the repo's existing test conventions (found in AGENTS.md or by examining
the test directory structure). Common patterns:

| Convention                | Where to put tests                           |
| ------------------------- | -------------------------------------------- |
| Mirror structure          | `tests/` mirrors `src/` directory structure  |
| Co-located                | `__tests__/` next to source files            |
| Module-level              | One test file per source module              |
| Feature-level             | One test file per feature or user story       |

If the repo has no tests yet, create a `tests/` directory that mirrors the source
structure. Document this decision in the execution plan.

---

## When TDD doesn't apply — alternative verification

For changes where TDD doesn't fit, you still need verification evidence. Choose
the most appropriate method:

| Change type          | Verification method                                         |
| -------------------- | ----------------------------------------------------------- |
| Configuration        | Run the application/build and confirm it starts correctly   |
| Infrastructure       | Verify the deployed/configured resource works as expected   |
| Documentation        | Verify links work, code examples run (if applicable)        |
| Dependency updates   | Run existing test suite — if it passes, the update is safe  |
| Refactoring          | Run existing test suite — no behavior change means same results |
| UI layout            | Generate a screenshot or describe the visual change         |

The key principle: **every change needs evidence that it works**. TDD produces
that evidence as a side effect of the workflow. When you skip TDD, you must
produce the evidence some other way.

---

## Testing patterns to avoid

| Anti-pattern                    | Problem                                         | Instead                                 |
| ------------------------------- | ----------------------------------------------- | --------------------------------------- |
| Testing implementation details  | Tests break when you refactor                   | Test observable behavior (inputs/outputs)|
| Giant test methods              | Hard to know what failed and why                | One assertion (or closely related group) per test |
| Tests with no assertions        | They always pass — they prove nothing           | Every test must assert something        |
| Mocking everything              | Tests pass but real code might not work         | Mock at boundaries, not internals       |
| Tests that depend on order      | Fail randomly, hard to run in isolation         | Each test sets up its own state         |
| Copy-paste test code            | Maintenance burden, masks patterns              | Extract fixtures or test helpers        |

---

## Recording test evidence in the plan

After each step that involves testing, update the plan with concrete evidence:

```markdown
### Step 3: Add parse_duration utility

**Files:** `src/utils/duration.py`, `tests/utils/test_duration.py`
**Verification:** All duration parsing tests pass

Status: ✅ Done
Evidence: RED → GREEN cycle complete. 4 tests pass (test_seconds, test_minutes,
          test_hours, test_invalid_input). Full suite: 147 pass, 0 fail.
Deviations: None
```

The evidence should be specific enough that another agent can verify it without
re-running the tests — it should say WHICH tests, HOW MANY, and what they cover.
