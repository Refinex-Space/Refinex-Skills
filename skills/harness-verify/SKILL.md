---
name: harness-verify
description: >-
  Use when about to claim that repository work is complete, fixed, passing, or
  ready, especially after Harness feature work, bug fixes, drift repairs, or
  control plane updates. Require fresh verification evidence before any success
  claim, commit summary, or handoff message. Especially relevant for prompts
  such as `现在算完成了吗`, `确认修好了`, `测试应该过了`, `可以提交了吗`, or `帮我确认能不能宣称 ready`.
license: Proprietary. LICENSE.txt has complete terms
---

# harness-verify

Prevent false completion claims by requiring fresh verification evidence before the agent says work is done, fixed, passing, or ready. This skill is the final honesty gate for the Harness family.

This is a **low-freedom** skill. Verification discipline is mandatory.

**Announce at start:** `I'm using harness-verify to confirm the claim with fresh evidence.`

---

## The iron law

```text
NO COMPLETION CLAIM WITHOUT FRESH VERIFICATION EVIDENCE
```

If you have not run the command that proves the claim in the current turn, you do not have the right to make the claim.

---

## When to use

Apply this skill before:

- saying a feature is complete
- saying a bug is fixed
- saying tests pass
- saying a repo is healthy
- saying a plan step is done
- creating a final summary that implies success

This skill is normally paired with:

- `harness-feat` for acceptance criteria, tests, lint, and control plane updates
- `harness-fix` for reproduction tests, regression tests, and full-suite safety checks
- `harness-garden` for post-repair validator runs
- `harness-bootstrap` for initial control plane validation

---

## Verification gate

Before making any success claim:

1. **Name the claim**
   - Example: "the bug is fixed"
   - Example: "the new skill set is ready"

2. **Name the proving command**
   - test command
   - validator command
   - lint/typecheck command
   - targeted reproduction command

3. **Run the command now**
   - no cached output
   - no earlier run from another turn
   - no extrapolation from partial evidence

4. **Read the output**
   - exit code
   - failed tests or warnings
   - whether the output actually proves the claim

5. **State the result with evidence**
   - if PASS: make the claim and cite the proof
   - if FAIL: state the actual status and the blocking evidence

Skipping any step is verification theater.

---

## Common claims and required evidence

| Claim | Minimum evidence |
| --- | --- |
| "Tests pass" | Fresh test command with zero failing tests |
| "Bug is fixed" | Reproduction now passes and full suite does not regress |
| "Feature is complete" | Acceptance criteria checked plus relevant tests/lint pass |
| "Control plane is healthy" | `python3 scripts/check_harness.py` run successfully |
| "Ready to commit / hand off" | Fresh verification for the work plus a clean understanding of residual risks |

---

## Special handling by workflow

### Feature work

When paired with `harness-feat`, confirm:

- acceptance criteria are checked one by one
- relevant tests pass
- lint/type checks pass when applicable
- control plane updates are reflected if scope changed

### Fix work

When paired with `harness-fix`, confirm:

- the reproduction now passes
- the regression test exists and passes
- the full test suite is not worse than baseline

### Drift repair or bootstrap

When paired with `harness-bootstrap` or `harness-garden`, confirm:

- validator output is fresh
- manifest, links, and managed files are in the expected state

---

## Red flags

Stop immediately if you are about to say any variant of:

- "should be fixed now"
- "looks done"
- "probably passes"
- "I think we're good"
- "ready"
- "all set"

These phrases are only allowed after fresh evidence, not before it.

---

## Reporting contract

A valid verification summary contains:

1. the claim being checked
2. the command that was run
3. the observed result
4. the conclusion

Example:

```text
Claim: control plane is healthy
Command: python3 scripts/check_harness.py
Result: exit 0, no errors
Conclusion: control plane validation passed
```

If you cannot produce this structure, you have not verified the claim.
