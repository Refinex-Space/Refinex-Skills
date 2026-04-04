# Scaffold Matrix

Use this matrix to decide which Harness artifacts are mandatory and
which are conditional.

## Always Create or Maintain

- `AGENTS.md`
- `ARCHITECTURE.md`
- `docs/README.md`
- `docs/PLANS.md`
- `docs/SECURITY.md`
- `docs/RELIABILITY.md`
- `docs/OBSERVABILITY.md`
- `docs/QUALITY_SCORE.md`
- `docs/exec-plans/tech-debt-tracker.md`
- `docs/exec-plans/completed/README.md`
- `docs/generated/README.md`
- `docs/generated/harness-manifest.md`
- `docs/references/index.md`
- `scripts/check_harness.py`

## Frontend or UI Signal

Create when the repo contains strong frontend indicators such as
workspace apps, `src/`, `app/`, `components/`, framework configs, or
browser-facing packages.

- `docs/FRONTEND.md`
- `docs/PRODUCT_SENSE.md`
- `docs/product-specs/index.md`

## Complex Architecture Signal

Create when the repo is a monorepo, full-stack app, multi-service repo,
or already exhibits multiple major subsystems.

- `docs/DESIGN.md`
- `docs/design-docs/index.md`
- `docs/design-docs/core-beliefs.md`

## Local AGENTS Strategy

Create local `AGENTS.md` when a directory is a meaningful handoff
boundary for future agents:

- real app or service workspaces
- workspace roots that coordinate multiple children
- shared library clusters
- backend/frontend split boundaries

Do not spam local `AGENTS.md` into every folder. Prefer clear boundaries
over exhaustive coverage.

## Merge-First Behavior

For existing repositories:

- create missing files
- regenerate managed files
- skip unsafe rewrites of unmanaged strategic docs
- record skipped high-risk corrections in the active bootstrap plan
