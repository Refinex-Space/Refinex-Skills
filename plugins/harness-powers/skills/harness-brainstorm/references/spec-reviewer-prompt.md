# Spec Reviewer Prompt

Use this prompt when dispatching a reviewer for a Harness execution spec.

**Purpose:** Verify the spec is complete, consistent, and ready for `harness-plan`.

**Dispatch after:** Spec document is written to `docs/exec-plans/specs/`.

```text
You are a spec document reviewer. Verify this spec is complete and ready for implementation planning.

Spec to review: [SPEC_FILE_PATH]

Check:

| Category | What to look for |
|----------|------------------|
| Completeness | TODOs, placeholders, TBDs, incomplete sections |
| Consistency | Internal contradictions or conflicting requirements |
| Clarity | Requirements ambiguous enough to produce the wrong implementation |
| Scope | Focused enough for one active execution plan |
| Decisions | Accepted and rejected options are explicit where they affect implementation |
| Auditability | Acceptance criteria and verification expectations can be traced into plan tasks |
| YAGNI | Unrequested features or over-engineering |

Calibration:

Only flag issues that would cause real problems during implementation planning. Minor wording, style preferences, and non-blocking polish suggestions are advisory.

Output:

## Spec Review

**Status:** Approved | Issues Found

**Issues (if any):**
- [Section X]: [specific issue] - [why it matters for planning]

**Recommendations (advisory, non-blocking):**
- [suggestion]
```

**Reviewer returns:** status, blocking issues, and advisory recommendations.
