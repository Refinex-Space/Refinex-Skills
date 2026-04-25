# Root Cause Techniques

A toolkit of systematic debugging techniques for Step 4 — Root Cause Isolation.
Choose the technique that matches your situation; combine techniques when needed.

---

## 1. Scientific Debugging (Zeller)

The most general technique. Use when you don't know where to start, or when
other techniques haven't converged.

### The cycle

```
Observe → Hypothesize → Predict → Experiment → Conclude
```

1. **Observe**: gather all available evidence
   - Error messages and stack traces
   - Log output around the failure
   - Test output (which assertions failed, what values were actual vs expected)
   - Recent changes to the affected code

2. **Hypothesize**: form a specific, falsifiable hypothesis
   - Bad: "something is wrong with the auth module"
   - Good: "the auth middleware rejects valid tokens because it compares
     expiration time without accounting for clock skew"

3. **Predict**: if the hypothesis is correct, what observable consequence follows?
   - "If clock skew is the issue, tokens that expire within a 5-second window
     should sometimes pass and sometimes fail"

4. **Experiment**: design and run a test that checks the prediction
   - Run the test with a token expiring in 3 seconds, observe behavior

5. **Conclude**: does the evidence support or refute?
   - Supported → proceed to fix
   - Refuted → refine hypothesis or form a new one

### Key principles

- **One variable at a time**: change only one thing per experiment
- **Record everything**: write each cycle in the hypothesis log
- **Refuted hypotheses are progress**: they narrow the search space
- **If the hypothesis is vague, make it more specific before testing**

---

## 2. Git Bisect (Regression Isolation)

Use when you know the bug didn't exist at a previous point in time.
Finds the introducing commit in $O(\log N)$ steps.

### Prerequisites

- A reproduction test that reliably fails on the current HEAD
- A known-good commit where the test passes

### Procedure

```bash
git bisect start
git bisect bad HEAD                    # current commit has the bug
git bisect good <known-good-commit>    # this commit was clean

# Git checks out a midpoint. Run the reproduction test.
<test-command> -k <reproduction-test>

# If the test fails → the bug is present at this commit
git bisect bad

# If the test passes → the bug isn't present yet
git bisect good

# Repeat until git reports the first bad commit
# When done:
git bisect reset
```

### Automated bisect

If the reproduction test is a single command with a clear exit code:

```bash
git bisect start HEAD <known-good-commit>
git bisect run <test-command> -k <reproduction-test>
git bisect reset
```

### After bisect

Read the introducing commit carefully:
- What did it change?
- Why did that change break the behavior?
- Was the breakage an oversight, a missing edge case, or a design flaw?

Record the commit hash and analysis in the fix plan under Root Cause.

---

## 3. Five Whys (Causal Chain Analysis)

Use when the immediate cause is clear but you suspect a deeper systemic issue.
Ask "why" iteratively until you reach an actionable root cause.

### Procedure

```
Why did X happen?
→ Because Y.

Why did Y happen?
→ Because Z.

Why did Z happen?
→ Because W.

...continue until you reach a cause that's directly fixable.
```

### When to stop

- You've reached a cause that's directly actionable (you can fix it)
- You've reached an organizational or process cause (beyond the scope of code)
- You're going in circles (two causes that depend on each other)

### Common patterns

| Stopping point             | Action                                               |
| -------------------------- | ---------------------------------------------------- |
| Missing validation         | Add the validation                                   |
| Wrong assumption in code   | Fix the assumption, document why                     |
| Missing test coverage      | Fix the bug AND add the missing test                 |
| Architectural constraint   | Fix the immediate bug, file tech debt for the design |
| Process gap                | Fix the immediate bug, note the process issue        |

---

## 4. Delta Debugging (Input Minimization)

Use when a complex input triggers the bug but you need to find the minimal
failure-inducing input. Based on Andreas Zeller's automated approach.

### The manual version

1. Start with the full failure-inducing input
2. Remove half the input — does it still fail?
   - Yes → keep the smaller input, repeat
   - No → restore that half, remove the other half
3. Continue halving until removing any part makes the failure disappear
4. The remaining input is the minimal reproduction case

### When this is useful

- Large configuration files where "something in here" causes a crash
- Complex API payloads where a specific field combination triggers the bug
- Test fixtures with many setup steps where only some are relevant

### The result

A minimal reproduction case makes the root cause obvious — when the input
is small enough, there are very few things that could be going wrong.

---

## 5. Code Path Tracing

Use when you understand WHAT fails but not WHERE in the code path.

### Procedure

1. Start from the entry point (the function called, the endpoint hit)
2. Follow the execution path, noting branches and conditions
3. At each decision point, predict which branch should be taken for the failing input
4. Find the first point where actual behavior diverges from expected

### Tactical approaches

- **Log insertion**: add targeted log statements at key decision points
  (remove them after diagnosis — they're diagnostic, not permanent)
- **Debugger**: step through execution with breakpoints at suspected locations
- **Test narrowing**: if a high-level test fails, write narrower tests for
  sub-components until you find the component that misbehaves

---

## 6. Differential Analysis (Environment-Specific Bugs)

Use when the bug appears in one environment but not another.

### Procedure

1. List every difference between the working and failing environments:
   - Runtime version, OS, architecture
   - Dependency versions (exact, not ranges)
   - Configuration values
   - Environment variables
   - Filesystem state (permissions, paths)

2. Systematically eliminate differences:
   - Align one variable at a time between environments
   - After each alignment, test — does the bug appear/disappear?

3. The variable that makes the difference is the root cause (or leads to it)

---

## 7. Stack Trace Analysis

The most straightforward technique. Use when the error includes a stack trace.

### Procedure

1. Read the stack trace from bottom to top (most recent call last)
2. Identify the first frame that's in YOUR code (not library/framework code)
3. Read that code — what was it trying to do? What values did it have?
4. Look at the error type and message in context of that code location
5. Form a hypothesis from there

### Common traps

- **Don't assume the error location is the cause location.** An `AttributeError`
  on line 42 might be caused by incorrect initialization on line 10
- **Don't ignore the full chain.** The root cause is often several frames up
  from where the exception was raised
- **Check for swallowed exceptions.** The visible error might be a secondary
  failure triggered by a silently caught primary failure

---

## Technique selection flowchart

```
Is there a stack trace?
├── Yes → Start with Stack Trace Analysis
│         └── If cause isn't obvious → Scientific Debugging
└── No → Continue

Did this work before?
├── Yes (regression) → Git Bisect
│   └── If bisect finds the commit → read it, understand WHY
│   └── If bisect is inconclusive → Scientific Debugging
└── No / Unknown → Continue

Is the input complex?
├── Yes → Delta Debugging (minimize input first)
│         └── Then Scientific Debugging on the minimal case
└── No → Continue

Is it environment-specific?
├── Yes → Differential Analysis
└── No → Scientific Debugging (the general-purpose fallback)

Is it intermittent?
├── Yes → Flaky Test Protocol (in SKILL.md)
└── No → Scientific Debugging
```

When in doubt, Scientific Debugging is always a valid starting point. The
other techniques are optimizations for specific situations.
