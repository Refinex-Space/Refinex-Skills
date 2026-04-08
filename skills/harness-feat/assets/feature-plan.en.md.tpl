# ${title}

## Metadata

- **Status**: 🟡 Active
- **Owner**: ${owner}
- **Created**: ${date}
- **Goal**: ${goal}
- **Scope**: ${scope}
- **Non-goals**: ${non_goals}
- **Rollback**: ${rollback}
- **Roadmap entry**: `docs/PLANS.md`
- **Plan path**: `${plan_path}`

## Harness Preflight

- **Repo check**: ${HARNESS_CHECK_STATUS}
- **Harness surfaces**:
${HARNESS_SURFACES}

## Background

${problem}

## Optimized Task Brief

- **Outcome**: ${goal}
- **Problem**: ${problem}
- **Scope**: ${scope}
- **Non-goals**: ${non_goals}
- **Constraints**:
${constraints}
- **Affected surfaces**:
${affected_surfaces}
- **Validation**:
${validation}
- **Docs to sync**:
${docs_sync}
- **Open assumptions**:
${open_assumptions}

## Incremental Slices

### Slice 1 — Establish context and the smallest viable change

- [ ] Implement
- [ ] Validate

### Slice 2 — Deliver the core implementation

- [ ] Implement
- [ ] Validate

### Slice 3 — Documentation, observability, and finish-up

- [ ] Sync docs and generated surfaces
- [ ] Final validation
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
