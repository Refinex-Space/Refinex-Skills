---
name: harness-review
description: >-
  Use when requesting or performing review of the current diff, active Harness
  plan output, or a pull request, and when receiving review feedback that must
  be verified, evaluated, answered, and implemented item by item.
license: MIT
---

# harness-review

Review code changes and review feedback with technical rigor. This skill covers
both sides of the loop: asking for a findings-first review of work in progress,
and handling review comments without blind agreement or unverified fixes.

**Priority order:** security > correctness > performance > readability.

---

## When to use

Use this skill for:

- reviewing the current diff before handoff
- reviewing output from an active plan task or batch
- reviewing a pull request before merge
- requesting an external or delegated code review
- processing review feedback from a human reviewer, PR comment, CI-adjacent
  review bot, or delegated reviewer
- confirming review fixes before moving to `harness-verify`

Review early enough that issues can be fixed while the implementation context is
still fresh.

---

## Inputs to gather

Before requesting or performing review, collect only the context needed to judge
the work product:

- current diff or explicit git range
- active Harness plan task, acceptance criteria, or requirements
- PR title, description, and changed files when reviewing a PR
- relevant test results, lint/typecheck output, migrations, or screenshots
- architectural constraints from local instructions and nearby code

Do not rely on session memory as review evidence. Use repository state,
commands, files, and plan artifacts.

---

## Review request workflow

1. **Define the review target**
   - current working tree diff
   - active plan output
   - PR branch or explicit base/head range

2. **Define expected behavior**
   - quote or summarize the plan, issue, acceptance criteria, or PR intent
   - identify explicit exclusions to avoid scope creep

3. **Inspect the actual change**
   - read the diff
   - inspect touched files in context
   - check tests and verification evidence

4. **Review findings first**
   - lead with issues, not praise or summaries
   - order findings by severity
   - include file and line references whenever possible
   - explain impact and the smallest credible fix

5. **Use severity consistently**
   - Critical: exploitable security issue, data loss, broken core behavior,
     migration hazard, or release blocker
   - Important: correctness gap, missing required behavior, serious test gap,
     poor error handling, compatibility issue, or maintainability risk likely
     to matter soon
   - Minor: readability, documentation, naming, small simplification, or
     non-blocking optimization

6. **Give a readiness verdict**
   - Ready
   - Ready with minor follow-up
   - Needs fixes before proceeding
   - Blocked pending clarification or evidence

Use `references/code-reviewer-prompt.md` when delegating a focused review.

---

## Review checklist

Apply the priority order before considering style:

- **Security**
  - input validation, authz/authn, secrets, injection, path traversal, SSRF
  - unsafe defaults, logging sensitive data, dependency or supply-chain risk

- **Correctness**
  - requirements met, edge cases handled, error paths tested
  - migrations and compatibility safe
  - concurrency, time zones, ordering, idempotency, and rollback behavior

- **Performance**
  - avoid avoidable N+1 work, unbounded memory growth, blocking hot paths
  - check algorithmic cost and external call behavior

- **Readability**
  - local patterns followed
  - names and boundaries clear
  - comments explain non-obvious decisions

Tests matter most when they prove behavior. Prefer real assertions over mocks
that only verify implementation shape.

---

## Feedback reception workflow

When receiving review feedback:

1. **Read**
   - read every item before editing
   - identify whether items depend on each other

2. **Understand**
   - restate the technical requirement to yourself
   - ask for clarification before implementing if any item is ambiguous

3. **Verify**
   - inspect the code, tests, and local constraints
   - check whether the feedback is true for this codebase
   - confirm whether existing behavior depends on the current implementation

4. **Evaluate**
   - accept technically sound feedback
   - reject or narrow feedback that is wrong, unnecessary, harmful, or outside
     scope
   - involve the human owner before overriding architectural decisions

5. **Respond**
   - answer with technical facts, not performative agreement
   - explain pushback with code, tests, constraints, or product requirements
   - for accepted items, state the fix made and where it landed

6. **Implement**
   - handle one item at a time
   - prioritize security and blocking correctness issues first
   - test each meaningful fix
   - track every item as fixed, intentionally rejected, deferred, or blocked

Do not say the reviewer is right before checking. External feedback is evidence
to evaluate, not an order to follow blindly.

---

## Multi-item handling

For a list of review comments:

1. Clarify all unclear items before editing.
2. Group related comments only when they require the same change.
3. Fix in this order:
   - security and release-blocking correctness
   - simple mechanical fixes
   - larger logic changes or refactors
   - readability and documentation improvements
4. Keep a short ledger:
   - item
   - disposition
   - files changed
   - verification evidence
5. Re-read the diff after all fixes to catch accidental regressions.

Avoid partial understanding. A fast wrong fix creates more review debt.

---

## Pushback rules

Push back when feedback:

- weakens security or correctness
- conflicts with established local architecture
- breaks supported compatibility
- adds unused scope or speculative features
- misunderstands the active plan or PR goal
- cannot be verified with available evidence

Good pushback is concise and technical:

```text
Checked the current call sites and this endpoint is not used. Adding the
suggested pagination would expand scope without a consumer. I recommend either
removing the endpoint now or tracking pagination in a separate follow-up.
```

If you cannot verify an item, say what evidence is missing and ask whether to
investigate, defer, or proceed with a constrained change.

---

## Required handoff

After review fixes are complete, hand the work to `harness-verify`.

The handoff must include:

- review items handled and dispositions
- files changed for fixes
- verification commands already run
- remaining risks or explicitly deferred items
- the specific claim that `harness-verify` must prove

Review fixes are not complete until the verification gate has fresh evidence.
