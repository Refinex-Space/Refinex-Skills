---
name: harness-garden
description: >
  Audit, repair, and continuously correct Harness Engineering drift in
  repositories that already have some form of agent control plane. Use
  when Codex needs to inspect root and local `AGENTS.md`, `docs/PLANS.md`,
  `docs/OBSERVABILITY.md`, `docs/exec-plans`, generated Harness manifests,
  and repo-local `python3 scripts/check_harness.py`; then auto-fix
  low-risk drift, refresh stale managed files, and create a remediation
  execution plan for high-risk semantic rewrites. Especially relevant for
  prompts such as `检查这个项目的 Harness 是否健康`, `修复文档索引和 AGENTS 偏离`,
  `纠正 Harness 漂移`, `做 doc-gardening`, `做 Harness audit`, or
  `$harness-garden`.
---

# Harness Garden

Audit a repository's Harness health, repair low-risk drift, and route
unsafe semantic corrections into an explicit remediation plan instead of
rewriting strategic docs blindly.

## Core Commitments

- Separate safe repair from risky semantic change.
- Reuse repo-local mechanical checks when available, but do not trust them blindly.
- Refresh stale managed Harness files, not only missing ones.
- Preserve unmanaged strategic docs unless drift is trivial.
- Leave the harness more indexable, more resumable, and more observable after each pass.

## Authority Ladder

Use this order when deciding whether to auto-fix or escalate:

1. Real repository state and current drift
2. `references/repair-policy.md`
3. `references/garden-checklist.md`
4. `references/harness-principles.md`
5. User preferences that do not increase risk

## Start Sequence

1. Run `scripts/audit_harness.py` against the target repository.
2. Treat the repo-local `scripts/check_harness.py` as an input signal, not the whole truth.
3. Classify findings with `references/repair-policy.md`.
4. Run `scripts/repair_harness.py` in `safe-fix` mode for low-risk issues.
5. When high-risk issues remain, create or update a date-prefixed remediation plan such as `docs/exec-plans/active/2026-04-05-harness-garden-remediation.md`.

## Workflow

### 1. Audit First

Inspect:

- required Harness files and conditional route docs
- local `AGENTS.md` coverage at real workspace boundaries
- root `AGENTS.md` and `docs/PLANS.md` size and route quality
- plan lifecycle integrity and archive headers
- manifest freshness and repo-local check freshness
- observability and tech-debt tracking surfaces

Treat stale managed files as real drift, not style nits.

### 2. Auto-Fix Only Low-Risk Drift

- create missing low-risk Harness docs
- regenerate managed files
- refresh stale `harness-manifest.md` and `check_harness.py`
- create missing local `AGENTS.md`
- add archive headers to completed plans

### 3. Escalate Risky Semantic Drift

- unmanaged root `AGENTS.md` routing drift
- unmanaged `docs/PLANS.md` structural rewrite
- language-wide doc migration
- conflicting architecture or design constraints
- any rewrite that would replace strategic human-authored intent

Do not blindly fix those. Create or update a remediation plan instead.

### 4. Re-Audit After Repair

- After safe fixes, rerun the audit.
- The repo should end with fresher indexes, mechanical checks, and generated facts than it started with.
- If only unmanaged strategic drift remains, stop and leave the remediation plan as the active handoff surface.

## Preferred Commands

```bash
python3 scripts/audit_harness.py --repo <repo> --format md
python3 scripts/repair_harness.py --repo <repo> --mode safe-fix
python3 scripts/repair_harness.py --repo <repo> --mode report-only --dry-run
python3 scripts/run_fixture_tests.py
```

## Guardrails

- Do not silently rewrite unmanaged strategic docs with semantic drift.
- Do not treat every missing file as equally urgent; use severity and repair policy.
- Do not remove working local `AGENTS.md` just to normalize style.
- Execution plan filenames under `docs/exec-plans/` must use `YYYY-MM-DD-short-task-title.md`; bare-slug filenames are Harness drift that should be repaired or escalated explicitly.
- Refresh mechanical files after repair so the next audit sees current facts.
- Keep remediation plans explicit when the repo still needs human-level semantic decisions.

## Not for This Skill

Use `harness-bootstrap` instead when the repository lacks a meaningful
Harness baseline and primarily needs first-time installation rather than
drift correction.
