## Harness Engineering Suite

The Harness Engineering Suite is a four-skill control plane for agent-first software development inside real repositories. It turns ad-hoc coding into a governed loop with explicit preflight checks, versioned execution plans, verification evidence, and archive-ready handoff artifacts.

This suite is designed for teams that want agents to deliver production code continuously without losing architectural coherence, auditability, or cross-session continuity.

---

## Why This Suite Exists

Long-running coding agents fail in predictable ways when no repository-level harness is present:

- Work starts without a baseline, so regressions are misattributed.
- Changes are made without plans, so intent is lost.
- Control plane docs drift, so future sessions trust stale instructions.
- Bug fixes patch symptoms instead of root causes.

The Harness suite addresses these risks with four focused skills that map to the full software change lifecycle: initialize, maintain, build, and repair.

---

## The Four Skills

| Skill | Primary mission | Typical trigger |
| --- | --- | --- |
| `harness-bootstrap` | Initialize or complete a repository control plane | New repo, legacy repo without harness |
| `harness-garden` | Audit and repair control plane drift | Stale docs, broken links, outdated commands |
| `harness-feat` | Deliver new features and structured refactors | New capability, planned enhancement |
| `harness-fix` | Diagnose and repair bugs, regressions, incidents | Failing tests, production bug, flaky path |

---

## Workflow Positioning

Think of the suite as one operating model:

1. `harness-bootstrap` creates the baseline control plane.
2. `harness-garden` keeps that baseline truthful over time.
3. `harness-feat` executes planned feature delivery inside the control plane.
4. `harness-fix` executes evidence-driven diagnosis and minimal repair inside the control plane.

Recommended lifecycle:

```text
$harness-bootstrap  -> establish control plane
$harness-garden     -> keep control plane accurate
$harness-feat       -> build new capabilities safely
$harness-fix        -> repair failures with root-cause evidence
```

---

## Shared Control Plane Concepts

All four skills use shared terminology and artifacts:

- Control plane: AGENTS.md + docs + scripts + manifest
- Preflight: `python3 scripts/check_harness.py`
- Execution plans: `docs/exec-plans/active/` and `docs/exec-plans/completed/`
- Global index: `docs/PLANS.md`
- Drift tracking and generated state: `docs/generated/harness-manifest.md`

This shared vocabulary lets teams switch between skills without translation cost.

---

## Skill Detail

### 1. harness-bootstrap

Purpose:
- Install or complete the repository harness control plane.

Core behavior:
- Recon the repository first.
- Generate deterministic control plane artifacts.
- Preserve unmanaged team docs (no overwrite violence).
- Verify with `scripts/check_harness.py`.

Use when:
- You have a fresh repository.
- You have an existing repository with partial or no harness.

Outputs:
- Root and module AGENTS.md files where justified.
- docs routing and governance files.
- Manifest and preflight script.

### 2. harness-garden

Purpose:
- Continuously detect and repair control plane drift.

Core behavior:
- Run manifest integrity checks.
- Run semantic drift audit (commands, paths, claims, links).
- Auto-fix low-risk drift.
- Produce remediation plans for high-risk changes.

Use when:
- Agents report confusing or stale instructions.
- Docs no longer match code structure.
- Harness health is uncertain.

Outputs:
- Drift findings and remediation changes.
- Updated control plane documents.
- Garden report and audit trail.

### 3. harness-feat

Purpose:
- Deliver feature work and structured refactors safely.

Core behavior:
- Preflight before coding.
- Rewrite request into a sprint contract.
- Create a versioned execution plan.
- Implement in small validated steps.
- Archive plan and update `docs/PLANS.md`.

Use when:
- The user asks for new functionality.
- A refactor must be planned and verified.

Outputs:
- Feature execution plan with evidence log.
- Incremental commits tied to plan steps.
- Archived completion artifact.

### 4. harness-fix

Purpose:
- Repair bugs, regressions, incidents, and flaky paths with evidence.

Core behavior:
- Capture known-broken baseline.
- Produce a structured bug brief.
- Reproduce before fixing.
- Isolate root cause with explicit hypotheses.
- Apply minimal fix with scope guard.
- Add regression protection and archive fix plan.

Use when:
- Tests fail unexpectedly.
- A reported bug needs diagnosis.
- A path is flaky or an incident needs remediation.

Outputs:
- Fix plan with root-cause documentation.
- Hypothesis and evidence trail.
- Regression test coverage.

---

## Decision Guide

Use this quick routing table:

| Situation | Skill |
| --- | --- |
| Repo has no harness or incomplete harness | `harness-bootstrap` |
| Harness exists but may be stale | `harness-garden` |
| Need to build a new capability | `harness-feat` |
| Need to diagnose and repair broken behavior | `harness-fix` |

If multiple situations apply, sequence them:

- Missing harness first: run `harness-bootstrap`, then the work skill.
- Drift suspected first: run `harness-garden`, then `harness-feat` or `harness-fix`.

---

## Quality Model

The suite enforces five invariants:

1. Verify before change.
2. Plan before implementation.
3. Evidence before declaring done.
4. Archive before handoff.
5. Keep control plane synchronized with repository reality.

This gives teams a practical way to scale autonomous coding while preserving maintainability and operational confidence.
