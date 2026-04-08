# ${title}

## Metadata

- **Status**: 🟡 Active
- **Owner**: ${owner}
- **Created**: ${date}
- **Severity**: ${severity}
- **Goal**: ${goal}
- **Impact**: ${impact}
- **Rollback**: ${rollback}
- **Roadmap entry**: `docs/PLANS.md`
- **Plan path**: `${plan_path}`

## Harness Preflight

- **Repo check**: ${HARNESS_CHECK_STATUS}
- **Harness surfaces**:
${HARNESS_SURFACES}

## Symptom and Context

- **Expected**: ${expected}
- **Observed**: ${observed}
- **Impact**: ${impact}
- **Evidence**:
${evidence}

## Optimized Bug Brief

- **Reproduction**:
${reproduction}
- **Likely surfaces**:
${likely_surfaces}
- **Hypotheses**:
${hypotheses}
- **Validation**:
${validation}
- **Docs to sync**:
${docs_sync}

## Investigation and Repair Slices

### Slice 1 — Reproduce or bound the failure

- [ ] Reproduce / collect evidence
- [ ] Record findings

### Slice 2 — Isolate root cause

- [ ] Isolate
- [ ] Record findings

### Slice 3 — Repair, add regression protection, and verify

- [ ] Repair
- [ ] Regression protection
- [ ] Validate
- [ ] Archive the active plan and refresh Harness generated surfaces

## Risks and Rollback

${risk_summary}
- ${rollback}

## Decision Log

| Date | Decision | Why |
| ---- | -------- | --- |

## Validation Log

- ${initial_validation_note}

## Archive Notes

- Add completion date, summary, duration, and key learnings before archiving
- Confirm the plan moved into `docs/exec-plans/completed/` after archiving
- If `docs/generated/harness-manifest.md` exists, confirm it was refreshed after archiving
