# Refinex Harness Contract

This reference encodes the repository-side rules that should outrank a
rough bug-fix prompt when using `harness-fix`.

## Progressive Discovery Path

Read in this order unless the bug is already tightly localized:

1. Root `AGENTS.md`
2. `docs/PLANS.md`
3. `python3 scripts/check_harness.py` and `docs/generated/harness-manifest.md`, when available
4. Only the task-type docs from the root routing table
5. The closest local `AGENTS.md` files
6. Relevant code, tests, logs, and generated facts
7. External primary sources, only when facts are unstable or explicitly required

## Planning Artifact Lifecycle

- `docs/PLANS.md`: short roadmap entry point; keep it brief.
- `docs/exec-plans/active/*.md`: live work artifact; update during investigation and repair.
- `docs/exec-plans/completed/`: archive only after verified repair and completion summary.
- `docs/exec-plans/tech-debt-tracker.md`: systemic harness, design, or observability debt.

Use `scripts/init_exec_plan.py`, `scripts/sync_plan_state.py`, and
`scripts/archive_exec_plan.py` to keep this lifecycle deterministic
whenever the repository's `docs/PLANS.md` is managed.

Those lifecycle scripts are bundled with `harness-fix` itself. They are
not repository requirements and should not be reported as missing repo
files.

## Repository Invariants

These constraints come from the repository's Harness control plane and
are not optional unless the repository itself changes:

- Root `AGENTS.md` is a routing map, not a handbook.
- `docs/OBSERVABILITY.md` is the runtime entry point for debugging and verification.
- `docs/generated/harness-manifest.md` is a structural fact surface, not prose.
- Generated files should not be edited by hand when the repo expects script generation.
- Repeated harness weaknesses belong in `docs/exec-plans/tech-debt-tracker.md`.

## External Research Rule

Use web research only when:

- the failure depends on unstable external behavior or current provider docs
- the user explicitly asks for web verification
- high-stakes correctness requires current primary documentation

Prefer official documentation and authoritative primary sources.

## Distilled Harness Principles

Use these as workflow constraints:

- Start from observable behavior and leave breadcrumbs for the next pass.
- Do not debug too many hypotheses at once; narrow the failing invariant first.
- Keep structured repair artifacts current so debugging is resumable.
- Separate repair from evaluation with a distinct verification pass.
- When the same class of bug keeps recurring, strengthen the harness instead of repeatedly hand-fixing the symptom.
