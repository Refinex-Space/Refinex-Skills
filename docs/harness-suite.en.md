## Harness Engineering Suite

The Harness Engineering Suite is a repository control plane for agent-first software development inside real repositories. Its stable core is four workflow skills, now reinforced by two cross-cutting skills for routing and completion verification. Together they turn ad-hoc coding into a governed loop with explicit preflight checks, versioned execution plans, verification evidence, and archive-ready handoff artifacts.

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

## Core Four + Cross-Cutting Two

| Skill | Primary mission | Typical trigger |
| --- | --- | --- |
| `harness-bootstrap` | Initialize or complete a repository control plane | New repo, legacy repo without harness |
| `harness-garden` | Audit and repair control plane drift | Stale docs, broken links, outdated commands |
| `harness-feat` | Deliver new features and structured refactors | New capability, planned enhancement |
| `harness-fix` | Diagnose and repair bugs, regressions, incidents | Failing tests, production bug, flaky path |
| `harness-using` | Route repository work into the correct Harness workflow | Start of repo task, ambiguous workflow ownership |
| `harness-verify` | Enforce fresh evidence before success claims | "done", "fixed", "passing", "ready" moments |

---

## Workflow Positioning

Think of the suite as one operating model:

1. `harness-using` routes the task.
2. `harness-bootstrap` creates the baseline control plane when needed.
3. `harness-garden` keeps that baseline truthful over time.
4. `harness-feat` executes planned feature delivery inside the control plane.
5. `harness-fix` executes evidence-driven diagnosis and minimal repair inside the control plane.
6. `harness-verify` gates completion claims with fresh evidence.

Recommended lifecycle:

```text
$harness-using      -> route the task
$harness-bootstrap  -> establish control plane
$harness-garden     -> keep control plane accurate
$harness-feat       -> build new capabilities safely
$harness-fix        -> repair failures with root-cause evidence
$harness-verify     -> validate claims before handoff
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

The core four (`bootstrap`, `garden`, `feat`, `fix`) remain the primary lifecycle owners. `harness-using` and `harness-verify` are horizontal controls that improve routing discipline and honesty of completion claims without stealing ownership from the core workflow.

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

## Best Use Cases

Use the suite as a composed operating pattern, not as isolated commands. The following scenarios are high-leverage defaults.

| Use case | Recommended sequence | Why this works | Expected outcome |
| --- | --- | --- | --- |
| Legacy repo with inconsistent docs and no reliable agent context | `harness-bootstrap` -> `harness-garden` | Bootstrap establishes a control plane; garden immediately removes stale assumptions | Stable control plane, trustworthy AGENTS/docs, preflight-ready repository |
| Team starts a feature sprint in a previously harnessed repo | `harness-garden` -> `harness-feat` | Garden prevents stale-command failures before implementation begins | Predictable feature delivery with versioned plan and verification evidence |
| CI started failing after a recent merge and cause is unclear | `harness-fix` (optionally preceded by `harness-garden` if docs look stale) | Fix protocol enforces reproduce -> isolate -> minimal repair -> regression guard | Root-cause-backed fix plan, minimal patch, new regression protection |
| Monorepo with multiple modules and frequent agent handoffs | `harness-bootstrap` -> periodic `harness-garden` -> task-level `harness-feat`/`harness-fix` | Shared control plane vocabulary plus periodic drift correction preserves cross-session continuity | Low handoff friction and consistent execution quality across modules |
| Flaky test path causing intermittent release delays | `harness-fix` with flaky-path protocol | Statistical reproduction and hypothesis logging prevent symptom-level patching | Deterministic test behavior or explicit bounded diagnosis with escalation artifact |
| New project kickoff where autonomous coding is planned from day one | `harness-bootstrap` -> `harness-feat` -> ongoing `harness-garden` | Governance is created before code volume explodes; drift is managed continuously | Faster scaling of agent work without losing maintainability |

### Practical rollout pattern

For most teams, this rollout order gives the best cost-benefit profile:

1. Apply `harness-bootstrap` once per repository baseline.
2. Schedule `harness-garden` as recurring maintenance.
3. Route all build work through `harness-feat`.
4. Route all repair work through `harness-fix`.

This keeps execution standards consistent while minimizing process overhead.

---

## Recommended Usage Templates

### Template 1: Bootstrap a New or Legacy Repository

```text
Set up Harness Engineering control plane for this repository.

Context:
- Repository type: [frontend/backend/full-stack/monorepo/library]
- Current state: [new repo / partial docs / no AGENTS.md]
- Constraints: [security/compliance/performance/team conventions]

Expected outcome:
- Root + module AGENTS.md (where justified)
- docs/ control plane files and execution-plan directories
- Generated manifest
- Working scripts/check_harness.py
```

Use this when the repository has no reliable control plane, or its current control plane is incomplete.

### Template 2: Run a Drift Audit and Repair

```text
Run a Harness drift audit and repair low-risk issues.

Focus areas:
- AGENTS.md accuracy
- docs link/path validity
- command freshness in OBSERVABILITY
- manifest completeness

Output requirements:
- Drift findings summary
- Auto-fixed items list
- High-risk remediation plan for manual review
```

Use this when agent outputs suggest stale instructions, broken links, or outdated command references.

### Template 3: Deliver a New Feature Safely

```text
Implement this feature using Harness workflow.

Feature request:
[paste user requirement]

Requirements:
- Preflight first
- Rewrite into task brief + sprint contract
- Create execution plan in docs/exec-plans/active
- Implement in small verified steps
- Archive plan and update docs/PLANS.md
```

Use this for feature development, capability delivery, and structured refactoring.

### Template 4: Diagnose and Fix a Bug or Regression

```text
Diagnose and fix this issue using Harness fix protocol.

Bug report:
[paste symptom / error / failing test]

Requirements:
- Capture known-broken baseline
- Produce structured bug brief
- Reproduce before fixing
- Isolate root cause with evidence
- Apply minimal fix with scope guard
- Add regression protection and archive fix plan
```

Use this for bug fixes, regression repair, incidents, and flaky test paths.

### Template 5: End-to-End Sprint Pattern (Build + Repair)

```text
Run a full Harness sprint for this repository iteration.

Phase order:
1) Validate control plane health
2) Execute planned feature work
3) Diagnose and fix any regressions introduced or discovered
4) Archive all plans and summarize outcomes

Deliverables:
- Completed plan links
- Verification evidence summary
- Remaining risk/tech-debt notes
```

Use this when a team wants a single, governed cycle from planned delivery to verified stabilization.

---

## Quality Model

The suite enforces five invariants:

1. Verify before change.
2. Plan before implementation.
3. Evidence before declaring done.
4. Archive before handoff.
5. Keep control plane synchronized with repository reality.

This gives teams a practical way to scale autonomous coding while preserving maintainability and operational confidence.
