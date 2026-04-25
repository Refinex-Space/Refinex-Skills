# Garden Report Template

The complete format for the harness-garden audit report. The report serves as both an audit trail and an actionable remediation plan.

## Full Template

````markdown
=== Harness Garden Report ===

Repository: <repo name>
Audit date: <YYYY-MM-DD>
Previous audit: <date of last manifest verification, or "first audit">
Triggered by: <"scheduled" | "post-refactor" | "manual" | "pre-release">

---

## Health Score

| Metric               | Value                         |
| -------------------- | ----------------------------- |
| Control plane health | <X>% (<N>/<M> checks passed) |
| Total checks         | <M>                           |
| Passed               | <N>                           |
| Auto-fixed           | <count>                       |
| Proposed fixes       | <count>                       |
| Flagged for human    | <count>                       |
| Complexity candidates| <count>                       |

### Health Score Breakdown

| Category           | Checks | Passed | Drift Found |
| ------------------ | ------ | ------ | ----------- |
| Manifest integrity | <n>    | <n>    | <n>         |
| Cross-links        | <n>    | <n>    | <n>         |
| Semantic accuracy  | <n>    | <n>    | <n>         |
| Lifecycle hygiene  | <n>    | <n>    | <n>         |
| Complexity         | <n>    | <n>    | <n>         |

---

## Auto-fixes Applied

<If none: "No auto-fixes needed.">

<For each auto-fix, one line:>
- **[<drift-id>]** `<path>`: <brief description> *(evidence: <how drift was detected>)*

Example:
- **[STR-003]** `AGENTS.md`: Fixed link `docs/old-name.md` → `docs/new-name.md` *(evidence: git rename detected via `git log --diff-filter=R`)*
- **[LCY-001]** `docs/exec-plans/active/2026-03-15-add-auth.md`: Moved to `completed/` *(evidence: branch `feat/add-auth` merged 2026-04-01)*
- **[LCY-002]** `docs/PLANS.md`: Added missing entry for `2026-04-05-refactor-db.md` *(evidence: file exists in active/ but not listed)*

---

## Proposed Fixes

<If none: "No proposed fixes.">

<For each proposed fix:>

### PF-<N>: <Title> [<drift-id>]

**Impact**: <Critical | High | Medium>
**Certainty**: <Proven | High | Medium>

**What**: <What specifically needs to change>

**Why**: <Evidence that this is drift, not intentional>

**Risk**: <What could go wrong if this fix is applied incorrectly>

**Proposed change**:
```diff
- <old content>
+ <new content>
```

<Or for larger changes:>
**Proposed change**: <prose description of what to write>

---

## Flagged for Human Review

<If none: "No items flagged.">

<For each flag:>

### FL-<N>: <Title> [<drift-id>]

**Impact**: <Critical | High | Medium | Low>
**Certainty**: <Medium | Low>

**Concern**: <What might be wrong>

**Evidence**: <What triggered this finding — specific code paths, search results, or observations>

**Suggestion**: <Starting point for resolution — not a prescription>

---

## Complexity Audit

<If none: "No complexity reduction candidates found.">

<For each candidate:>

### CA-<N>: <Title> [<drift-id>]

**Component**: `<path>`
**Observation**: <Why this might be over-complex>
**Recommendation**: <What to consider — keep, simplify, or remove>

---

## Manifest Update

Refreshed Last Verified date to <today> for:

<Bulleted list of artifact paths that were verified>

Not refreshed (verification incomplete):

<Bulleted list of artifact paths that could not be fully verified, with reason>

---

## Next Audit

Recommended next garden audit: <YYYY-MM-DD>
Basis: <explain — typically the shortest freshness threshold among artifacts, or "post-refactor" if a major refactor is upcoming>

Critical artifacts to watch:
- <any artifacts that were close to their freshness threshold>
- <any artifacts with proposed fixes that were deferred>
````

## Report Generation Rules

1. **Include every finding.** Even if the finding was auto-fixed, it appears in the report. The report is an audit trail.

2. **Use drift IDs.** Reference the taxonomy IDs (STR-001, SEM-001, etc.) so findings can be cross-referenced with `references/drift-taxonomy.md`.

3. **Evidence must be concrete.** "This might be outdated" is not evidence. "The path `src/legacy-auth/` referenced in AGENTS.md line 42 does not exist. `git log` shows it was renamed to `src/auth/` in commit abc1234 on 2026-03-20" is evidence.

4. **Proposed changes should be applicable.** If the fix is a text change, show a diff. If it's a file move, show the mv command. If it's new content, show the draft.

5. **Health score is calculated after auto-fixes.** Auto-fixed items count as "passed" in the health score because they were both detected and resolved.

6. **Print summary to user.** After generating the full report, print a brief summary:

```
Garden audit complete.
  Health: 87% (26/30 checks passed)
  Auto-fixed: 3 items
  Proposed: 2 fixes (review needed)
  Flagged: 1 item for human review
  
  Full report: see above
  Manifest updated: docs/generated/harness-manifest.md
  Commit: chore(harness): garden audit auto-fixes
```
