# Hypothesis Log Template

A structured journal for recording investigation cycles during root cause
isolation (Step 4). Each entry documents one hypothesis → experiment → conclusion
cycle, creating a searchable audit trail of the investigation.

The hypothesis log serves three audiences:
1. **You (now)**: keeps investigation focused and prevents circular reasoning
2. **You (later)**: when you revisit a stalled investigation after a context reset
3. **Future agents**: when a similar bug appears and someone wants to know what
   was already tried

---

## Template

```markdown
# Hypothesis Log: <Bug Brief Title>

Fix plan: docs/exec-plans/active/YYYY-MM-DD-fix-short-description.md

## Investigation Summary

Started: YYYY-MM-DD HH:MM
Hypotheses tested: <N>
Root cause found: Yes / No / Partial

---

### Hypothesis #1

**Timestamp**: HH:MM
**Hypothesis**: <specific, falsifiable claim about the cause>
**Confidence**: Low / Medium / High
**Based on**: <what evidence or reasoning led to this hypothesis>

**Prediction**: If this hypothesis is correct, then <observable consequence>
**Experiment**: <exact steps to test — commands, tests, code inspections>

**Result**:
```
<paste exact output, log lines, or observations>
```

**Conclusion**: CONFIRMED / REFUTED / INCONCLUSIVE
**Reasoning**: <why the result supports/refutes the hypothesis>
**Next**: <what to investigate next based on this result>

---

### Hypothesis #2

**Timestamp**: HH:MM
**Hypothesis**:
**Confidence**:
**Based on**: <what from hypothesis #1 led here>

**Prediction**:
**Experiment**:

**Result**:
```
```

**Conclusion**:
**Reasoning**:
**Next**:

---

## Investigation Notes

<Free-form notes, observations, and connections spotted during investigation>

## Dead Ends

<List of approaches that were tried and definitively ruled out, to prevent
future investigators from re-treading the same ground>

- <approach 1>: ruled out because <reason>
- <approach 2>: ruled out because <reason>
```

---

## Guidelines for writing hypotheses

### Good hypotheses are:

- **Specific**: "the authentication check fails because it uses `==` instead
  of constant-time comparison" — not "something is wrong with auth"
- **Falsifiable**: there must be an experiment that could disprove it
- **Based on evidence**: connect it to something you observed, not a hunch
- **One thing at a time**: test one variable per hypothesis

### Bad hypothesis patterns:

| Pattern                        | Problem                                        | Better                                         |
| ------------------------------ | ---------------------------------------------- | ---------------------------------------------- |
| "Something is wrong with X"   | Too vague to test                              | "X fails when input contains Y because Z"     |
| "It might be A or B or C"     | Multiple variables, can't isolate              | Test A first, then B, then C                   |
| "The code is broken"          | Not a hypothesis, just a restatement           | "The code breaks because assumption P is wrong"|
| Confirming what you already know | No new information                           | Focus on what you DON'T know yet               |

### Connecting hypotheses

Each new hypothesis should build on the results of previous ones. This creates
a logical investigation chain:

```
H1: "The crash is in module A" → CONFIRMED (stack trace)
H2: "Module A crashes because function F receives null" → CONFIRMED (log)
H3: "F receives null because caller G doesn't check the DB result" → CONFIRMED
Root cause: G assumes the DB query always returns a result, but it can return
null when the record was soft-deleted.
```

### When to stop

- **Root cause found**: you've identified a specific, actionable mechanism
- **3 cycles with no progress**: time to escalate (see SKILL.md escalation rules)
- **Circular reasoning**: you're testing the same area repeatedly — step back
  and look at the problem from a different angle

---

## Using the log for escalation

When you hit the escalation threshold (3 cycles with no progress), the
hypothesis log becomes the escalation artifact. It shows:

- What was investigated and in what order
- Which hypotheses were confirmed vs refuted
- Where the investigation is stuck
- What the remaining unexplored hypotheses are

This information lets the user (or a more specialized agent) pick up exactly
where you left off, without re-doing work that's already been done.
