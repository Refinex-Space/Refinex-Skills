# Repair Policy

This file defines what `harness-garden` may auto-repair and what should
be escalated into an active remediation plan.

## Safe Auto-Fixes

- create missing low-risk Harness docs
- regenerate managed files
- regenerate stale `docs/generated/harness-manifest.md`
- regenerate stale repo-local `scripts/check_harness.py`
- create missing local `AGENTS.md` at suggested workspace boundaries
- create missing `docs/exec-plans/completed/README.md`
- add archive headers to completed plans that lack them
- recreate missing observability and tech-debt tracking surfaces

## Escalate Instead of Blindly Rewriting

- unmanaged root `AGENTS.md` with routing drift
- unmanaged `docs/PLANS.md` that needs structural rewrite
- language migration across the documentation set
- large semantic changes to architecture or design docs
- conflicting constraints between multiple existing docs
- any change that would replace human strategic intent with generated prose

## Remediation Plan Expectations

When escalation is needed:

1. Create or update a date-prefixed remediation plan such as `docs/exec-plans/active/2026-04-05-harness-garden-remediation.md`
2. Summarize findings by priority
3. Record skipped risky files explicitly
4. Keep low-risk repairs separate from high-risk semantic rewrites
5. Leave the next agent with a clear active handoff surface
