# Garden Checklist

Use this checklist when auditing a repository Harness.

## Route Integrity

- Does root `AGENTS.md` route to the current docs?
- Are key docs discoverable from the route table?
- Are indexes present and linked from the expected entry points?

## Progressive Disclosure

- Is root `AGENTS.md` acting as a map rather than a handbook?
- Are detailed rules pushed into `docs/` or local `AGENTS.md`?
- Do local `AGENTS.md` files exist at real boundaries?

## Plan Lifecycle

- Does `docs/PLANS.md` point to active work?
- Do active plans exist when work is in flight?
- Do completed plans have archive headers?

## Generated Facts

- Does `docs/generated/harness-manifest.md` exist?
- Does it still match the current structure?
- Does `python3 scripts/check_harness.py` exist and run?
- Are the manifest and repo-local check script fresh, not only present?

## Runtime Visibility

- Does `docs/OBSERVABILITY.md` exist?
- Are runtime debugging entry points discoverable?
- Are recurring blind spots tracked in `docs/exec-plans/tech-debt-tracker.md`?

## Drift Signals

- Overgrown root `AGENTS.md`
- Missing or stale indexes
- Missing local `AGENTS.md` at workspace boundaries
- Files that should be managed but are now hand-diverged
