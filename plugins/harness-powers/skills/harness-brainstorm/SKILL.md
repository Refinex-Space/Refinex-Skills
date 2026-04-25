---
name: harness-brainstorm
description: Use before creative or behavioral changes to explore intent, constraints, options, and produce an approved Harness execution spec before planning.
license: MIT
---

# Harness Brainstorm

Turn an idea into an approved, implementation-ready design without starting implementation.

<HARD-GATE>
Do NOT implement, scaffold, edit production files, or invoke implementation skills while using this skill. Harness brainstorm ends only after an approved spec is saved under `docs/exec-plans/specs/` and the next handoff is `harness-plan`.
</HARD-GATE>

## Checklist

Create a task for each item and complete them in order:

1. **Explore project context** - prefer `AGENTS.md`, `docs/ARCHITECTURE.md`, and `docs/PLANS.md`, then inspect relevant source, tests, and recent changes.
2. **Assess scope** - identify whether the request is one coherent project or needs decomposition into separate specs.
3. **Ask clarifying questions** - one at a time, focused on purpose, constraints, and success criteria.
4. **Propose 2-3 approaches** - include trade-offs, risks, and your recommendation.
5. **Present design** - validate architecture, components, data flow, error handling, migration, and test strategy in sections scaled to complexity.
6. **Write the spec** - save to `docs/exec-plans/specs/YYYY-MM-DD-<topic>-design.md`.
7. **Review the spec** - check for placeholders, contradictions, ambiguity, missing decisions, and scope creep. Use `references/spec-reviewer-prompt.md` when dispatching a reviewer.
8. **User review gate** - ask the user to review the spec and wait for approval.
9. **Transition to planning** - hand off to `harness-plan`.

## Process

### Explore Context

Start with repository guidance before asking detailed questions:

- `AGENTS.md` and nested instruction files for local rules.
- `docs/ARCHITECTURE.md` for system boundaries and design vocabulary.
- `docs/PLANS.md` for active, planned, and completed work.
- Relevant source files, tests, package metadata, and recent git history.

If the request spans independent subsystems, stop and propose a decomposition. Each coherent subsystem gets its own spec, plan, and execution cycle.

### Clarify Requirements

Ask one question per message. Prefer multiple-choice questions when they reduce user effort, but use open-ended questions when the answer space is genuinely unknown.

Focus on:

- user-visible behavior and success criteria
- security, data, compatibility, and operational constraints
- integration points and ownership boundaries
- what should explicitly stay out of scope

### Compare Approaches

Present 2-3 viable approaches. For each, include:

- what changes
- why it fits or does not fit the codebase
- primary risks
- verification strategy

Lead with the recommended approach and the reason it best satisfies the constraints.

### Present The Design

Once requirements are clear, present the design in reviewable sections. Keep simple designs short. For larger designs, cover:

- architecture and boundaries
- file/module responsibilities
- data flow and state changes
- error handling and rollback behavior
- testing and verification
- migration or rollout concerns

Ask for confirmation after each major section. Revise until the user approves.

## Spec Document

After approval, write the validated design to:

```text
docs/exec-plans/specs/YYYY-MM-DD-<topic>-design.md
```

The spec should be decision-complete enough for `harness-plan`:

- no `TBD`, `TODO`, or unresolved alternatives
- explicit accepted and rejected choices where they matter
- clear acceptance criteria
- clear out-of-scope items
- concrete verification expectations

## Spec Review

Review the written spec before asking the user to proceed:

1. **Placeholder scan** - remove incomplete text and vague requirements.
2. **Consistency check** - ensure the architecture, behavior, and acceptance criteria agree.
3. **Scope check** - ensure one plan can implement it coherently.
4. **Ambiguity check** - resolve requirements that could be implemented multiple ways.
5. **Audit check** - ensure later implementers can trace plan tasks back to spec decisions.

Fix issues inline before the user review gate.

## User Review Gate

After the spec review passes, ask the user to review the file:

```text
Spec written to `docs/exec-plans/specs/<filename>.md`. Please review it and tell me what should change before I create the implementation plan.
```

If the user requests changes, update the spec and repeat the review. Continue only after approval.

## Handoff

The terminal state is `harness-plan`. Do not invoke implementation, dispatch, verification, or finish skills from this skill.

## Key Principles

- Design first, implementation later.
- One question at a time.
- Prefer concrete choices over open-ended drift.
- Keep scope small enough to plan and audit.
- Follow existing repository patterns.
- Preserve Harness Powers lifecycle ownership: brainstorm -> plan -> execute -> verify -> finish.
