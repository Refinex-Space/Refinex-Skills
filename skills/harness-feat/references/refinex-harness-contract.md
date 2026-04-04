# Refinex Harness Contract

This reference encodes the repository-side rules that should outrank a
rough feature prompt when using `harness-feat`.

## Progressive Discovery Path

Read in this order unless the task clearly needs a narrower slice:

1. Root `AGENTS.md`
2. `docs/PLANS.md`
3. `python3 scripts/check_harness.py` and `docs/generated/harness-manifest.md`, when available
4. Only the task-type docs from the root routing table
5. The closest local `AGENTS.md` files
6. The relevant code, tests, logs, and generated facts
7. External primary sources, only when facts are unstable or explicitly required

## Planning Artifact Lifecycle

- `docs/PLANS.md`: short roadmap entry point; keep it brief.
- `docs/exec-plans/active/*.md`: live work artifact; update during execution.
- `docs/exec-plans/completed/`: archive only after verification and completion summary.
- `docs/exec-plans/tech-debt-tracker.md`: systemic harness, design, or observability debt.

Use `scripts/init_exec_plan.py`, `scripts/sync_plan_state.py`, and
`scripts/archive_exec_plan.py` to keep this lifecycle deterministic
whenever the repository's `docs/PLANS.md` is managed.

Those lifecycle scripts are bundled with `harness-feat` itself. They are
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

- the fact is unstable or external to the repository
- the user explicitly asks for web verification
- high-stakes correctness requires current primary documentation

Prefer official documentation and authoritative primary sources.

## Distilled Harness Principles

Use these as workflow constraints:

- Give the agent a map and leave breadcrumbs for the next pass.
- Do not ask the agent to do too much at once; prefer small validated increments.
- Keep structured artifacts current so progress is resumable.
- Separate implementation from evaluation with a distinct verification pass.
- When a task fails because the environment is weak, strengthen the harness instead of relying on repeated manual reminders.
