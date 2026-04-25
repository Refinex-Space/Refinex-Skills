# Bug Brief Template

Use this template when structuring the user's bug report in Step 2. The bug brief
transforms informal "it's broken" reports into actionable investigation artifacts.

---

```markdown
# Bug Brief: <Short Title>

Created: YYYY-MM-DD
Reporter: <user / CI / monitoring>
Status: Investigating

## Symptom

<Exact observable behavior. Include the full error message, stack trace, or
screenshot description. Be specific — "the API returns 500" is better than
"the API doesn't work.">

```
<paste exact error output here>
```

## Expected Behavior

<What should happen instead. Be specific — "the API returns 200 with a JSON
array of users" is better than "the API should work.">

## Reproduction Steps

<Steps to trigger the bug. Number them. Include commands, URLs, inputs.>

1. <step>
2. <step>
3. Observe: <symptom>

Reproducible: Yes / No / Intermittent
Reproduction test: <test name, if exists> / None yet

## Affected Scope

- **Module(s)**: <which modules are involved>
- **File(s)**: <specific files if known>
- **Component(s)**: <API, UI, database, etc.>

## Classification

| Field    | Value                                           |
| -------- | ----------------------------------------------- |
| Severity | Blocking / Degraded / Cosmetic                  |
| Type     | Regression / New bug / Flaky / Environment-specific |
| Priority | Fix now / Fix soon / Fix eventually             |

## Context

<Any additional context that might help diagnosis:>

- When did this start happening? <date or commit if known>
- Was anything recently changed in the affected area?
- Does it happen in all environments or only specific ones?
- Is there a workaround?

## Related

- Active plans in the same area: <links or "none">
- Related past fixes: <links or "none">
- Tech debt entries: <links or "none">
```

---

## Severity guide

| Severity     | Criteria                                                                     | Examples                                        |
| ------------ | ---------------------------------------------------------------------------- | ----------------------------------------------- |
| **Blocking** | Core functionality unusable, no workaround, affects all/most users           | Login broken, data loss, crash on startup        |
| **Degraded** | Feature works but impaired — errors in edge cases, performance regression, partial failure | Slow response, wrong format on specific input   |
| **Cosmetic** | Visual or minor behavioral issue, functionality intact                       | Typo in message, misaligned UI element           |

## Type classification guide

| Type                     | How to identify                                                         |
| ------------------------ | ----------------------------------------------------------------------- |
| **Regression**           | It worked before, now it doesn't. A specific change introduced the bug  |
| **New bug**              | The feature never handled this case correctly — it's a missing behavior |
| **Flaky**               | Sometimes works, sometimes doesn't — non-deterministic                  |
| **Environment-specific** | Works in environment A, fails in environment B                          |

The type determines which investigation technique to use in Step 4 — regressions
use git bisect, new bugs use scientific debugging, flaky tests use statistical
reproduction, and environment-specific bugs use differential analysis.

## When the user's report is too vague

If you can't fill in the template meaningfully, ask these specific questions:

1. "What exact error message or behavior do you see?"
2. "What were you trying to do when it happened?"
3. "Did this work before? If so, when did it stop working?"
4. "Can you share the command or steps that trigger the issue?"

Don't guess at fields you can't fill. Empty fields are better than wrong fields —
they tell you what to investigate.
