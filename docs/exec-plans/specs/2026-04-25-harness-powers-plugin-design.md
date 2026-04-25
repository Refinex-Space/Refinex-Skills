# Harness Powers Plugin Design

Date: 2026-04-25

## Objective

Build **Harness Powers** as a Codex App plugin maintained under this repository's `plugins/` directory. The plugin should absorb the strongest parts of Superpowers while preserving Harness Engineering as the primary control model: repository control plane, execution plans, preflight, drift repair, verification evidence, and cross-session continuity.

This is not a destructive Superpowers fork. It is a Harness-first enhancement distribution that reuses Superpowers ideas where they are strongest, then removes duplicated public entry points so agents see one coherent workflow.

## Background

Superpowers is strong at session-level engineering discipline:

- brainstorming before implementation
- writing detailed implementation plans
- executing plans with checkpoints
- TDD discipline
- systematic debugging
- subagent and parallel execution
- code review and branch finishing workflows

The existing Harness suite is stronger at repository-level control:

- `AGENTS.md` and docs as a control plane
- `docs/PLANS.md` and `docs/exec-plans/`
- `scripts/check_harness.py` preflight
- drift detection and repair
- feature and fix lifecycle ownership
- verification evidence before success claims

Harness Powers should merge these strengths without publishing two overlapping workflow systems.

## Chosen Approach

Use the **Harness-controlled fusion** model.

Harness Powers exposes a unified `harness-*` skill surface. Superpowers concepts are either renamed into Harness-owned skills, merged into existing Harness skills, or internalized as references. The plugin does not publish legacy Superpowers skill names, which avoids future content drift.

Rejected alternatives:

- **Superpowers-compatible enhancement:** low migration cost, but keeps too many competing entry points.
- **Two-layer plugin split:** theoretically clean, but heavier to install, search, and trigger.

## Plugin Identity

Plugin name:

- `harness-powers`

Display name:

- `Harness Powers`

Repository location:

- `plugins/harness-powers/`

The plugin should be a new productized artifact. It should not directly modify the installed cache at `/Users/refinex/.codex/plugins/cache/openai-curated/superpowers`.

## Public Skill Surface

The first version should publish these skills:

| Skill | Ownership |
| --- | --- |
| `harness-using` | Global entry router, skill selection, process-before-domain discipline |
| `harness-brainstorm` | Requirements clarification, approach comparison, design document |
| `harness-plan` | Convert approved design into active execution plan |
| `harness-execute` | Execute an active plan with checkpoints |
| `harness-bootstrap` | Initialize repository control plane |
| `harness-garden` | Audit and repair control plane drift |
| `harness-feat` | Feature and structured refactor lifecycle |
| `harness-fix` | Bug, regression, incident, and flaky-path lifecycle |
| `harness-verify` | Unique completion evidence gate |
| `harness-review` | Code review requests and review feedback handling |
| `harness-dispatch` | Subagent and parallel task orchestration |
| `harness-worktree` | Isolated worktree and branch preparation |
| `harness-finish` | Merge, PR, keep, or discard branch completion flow |
| `harness-frontend` | Frontend domain workflow layered under Harness lifecycle |

Do not publish these legacy Superpowers skill names:

- `using-superpowers`
- `brainstorming`
- `writing-plans`
- `executing-plans`
- `test-driven-development`
- `systematic-debugging`
- `verification-before-completion`
- `requesting-code-review`
- `receiving-code-review`
- `subagent-driven-development`
- `dispatching-parallel-agents`
- `using-git-worktrees`
- `finishing-a-development-branch`

## Lifecycle

The default lifecycle is:

```text
harness-using
  -> harness-bootstrap / harness-garden
  -> harness-brainstorm
  -> harness-plan
  -> harness-worktree
  -> harness-execute
       -> harness-dispatch
       -> harness-review
  -> harness-verify
  -> harness-finish
```

For direct feature work:

```text
harness-using -> harness-feat -> harness-verify -> harness-finish
```

For bug or regression work:

```text
harness-using -> harness-fix -> harness-verify -> harness-finish
```

`harness-using` owns routing. `harness-verify` owns success claims. No other skill should bypass those boundaries.

## Design And Plan Storage

Harness Powers should not use Superpowers storage paths.

Use:

- design/spec files: `docs/exec-plans/specs/YYYY-MM-DD-<topic>-design.md`
- active execution plans: `docs/exec-plans/active/YYYY-MM-DD-<topic>.md`
- completed execution plans: `docs/exec-plans/completed/YYYY-MM-DD-<topic>.md`
- plan index: `docs/PLANS.md`

Do not use:

- `docs/superpowers/specs/`
- `docs/superpowers/plans/`

## Skill Integration Details

### harness-using

Merge current `harness-using` with the useful discipline from `using-superpowers`.

It should:

- run before substantive repository work
- respect user and repo instructions above Harness rules
- check whether any Harness Powers skill applies
- prefer process skills before domain skills
- route missing control plane work to `harness-bootstrap`
- route suspected drift to `harness-garden`
- route unclear requirements to `harness-brainstorm`
- route design-to-plan work to `harness-plan`
- route existing-plan execution to `harness-execute`
- route feature work to `harness-feat`
- route bug work to `harness-fix`
- route review work to `harness-review`
- route completion claims to `harness-verify`

### harness-brainstorm

Rename and adapt Superpowers `brainstorming`.

It should:

- explore repository context before asking design questions
- read `AGENTS.md`, `docs/ARCHITECTURE.md`, and `docs/PLANS.md` when present
- ask one clarifying question at a time
- propose two or three approaches with trade-offs
- present design sections for approval
- write the approved design to `docs/exec-plans/specs/`
- hand off only to `harness-plan`

It must not implement code.

### harness-plan

Rename and adapt Superpowers `writing-plans`.

It should:

- create active execution plans under `docs/exec-plans/active/`
- update `docs/PLANS.md`
- use bite-sized tasks with exact paths, verification commands, and expected results
- keep plans decision-complete and audit-oriented
- avoid forcing full implementation code into every step when that would create a second source of truth
- include TDD steps where behavior changes require them
- hand off to `harness-execute` or ask for execution mode

### harness-execute

Rename and adapt Superpowers `executing-plans`.

It should:

- load and review an active plan before executing
- update checkboxes and evidence as work progresses
- stop on unclear or unsafe instructions
- update the plan before intentional deviations
- invoke `harness-dispatch` for parallel or subagent work
- invoke `harness-review` at review checkpoints
- invoke `harness-verify` before any completion claim

### harness-feat

Keep current `harness-feat` as the feature lifecycle owner and internalize Superpowers TDD discipline.

It should:

- keep the preflight -> sprint contract -> plan -> implement -> verify -> archive flow
- include RED/GREEN/REFACTOR guidance in references
- require goal-evidence pairing for plan steps
- require equivalent verification for non-TDD work
- keep plan state in `docs/exec-plans/`

### harness-fix

Keep current `harness-fix` as the bug lifecycle owner and internalize Superpowers systematic debugging.

It should:

- keep the preflight -> bug brief -> reproduction -> root cause -> minimal fix -> regression -> archive flow
- require reproduction evidence before fixes
- require falsifiable hypotheses during diagnosis
- require explicit evidence before root-cause claims
- stop and replan after repeated failed fix attempts
- keep systematic debugging references under `harness-fix/references/`

### harness-verify

Merge current `harness-verify` with `verification-before-completion`.

It should be the only evidence gate for claims such as:

- complete
- fixed
- ready
- passing
- healthy

Its report format should remain:

```text
Claim: <claim>
Command: <command>
Result: <observed result>
Conclusion: <conclusion>
```

### harness-review

Merge `requesting-code-review` and `receiving-code-review`.

It should:

- review current diffs, active plan output, or PRs
- handle review feedback item by item
- verify feedback against codebase reality before implementing
- prioritize security, correctness, performance, then readability
- avoid performative agreement
- hand off to `harness-verify` after review fixes

### harness-dispatch

Merge `subagent-driven-development` and `dispatching-parallel-agents`.

It should:

- identify independent task domains
- dispatch focused subagents where available
- keep the primary agent as plan owner
- require worker outputs to list changed files, verification, and residual risks
- use two-stage review for delegated work: spec compliance, then code quality

### harness-worktree

Rename and adapt `using-git-worktrees`.

It should:

- create isolated worktrees for plan execution when needed
- verify project-local worktree directories are ignored
- use `codex/` branch prefix unless the user specifies otherwise
- run setup and baseline checks when possible
- avoid executing plans on `main` or `master` unless explicitly allowed

### harness-finish

Rename and adapt `finishing-a-development-branch`.

It should:

- run `harness-verify` before presenting finish options
- offer local merge, push PR, keep branch, or discard
- require explicit confirmation before destructive discard
- archive completed plans and update `docs/PLANS.md`
- include plan and verification evidence in PR bodies

### harness-bootstrap And harness-garden

Keep existing Harness behavior and add Harness Powers awareness:

- generated control planes should mention Harness Powers lifecycle where useful
- `harness-garden` should audit `specs/`, `active/`, `completed/`, and `docs/PLANS.md`
- manifest checks should understand plugin-era plan layout

### harness-frontend

Keep as a domain skill.

In repository mode, it must run under `harness-brainstorm`, `harness-feat`, or `harness-fix`. It owns frontend discovery, visual thesis, rule packs, and design litmus checks, but it does not replace plan ownership or verification evidence.

## Plugin Directory Layout

Target layout:

```text
plugins/
└── harness-powers/
    ├── .codex-plugin/
    │   └── plugin.json
    ├── README.md
    ├── LICENSE
    ├── assets/
    │   ├── app-icon.png
    │   └── harness-powers-small.svg
    ├── skills/
    │   ├── harness-using/
    │   ├── harness-brainstorm/
    │   ├── harness-plan/
    │   ├── harness-execute/
    │   ├── harness-bootstrap/
    │   ├── harness-garden/
    │   ├── harness-feat/
    │   ├── harness-fix/
    │   ├── harness-verify/
    │   ├── harness-review/
    │   ├── harness-dispatch/
    │   ├── harness-worktree/
    │   ├── harness-finish/
    │   └── harness-frontend/
    └── tests/
```

## Migration Order

1. Scaffold `plugins/harness-powers/` with plugin metadata, README, license, and assets.
2. Copy existing Harness skills into the plugin with minimal path fixes.
3. Import and rename the three Superpowers core skills as `harness-brainstorm`, `harness-plan`, and `harness-execute`.
4. Merge overlapping Superpowers skills into `harness-using`, `harness-verify`, `harness-review`, `harness-dispatch`, `harness-worktree`, and `harness-finish`.
5. Move TDD material into `harness-feat/references/`.
6. Move systematic debugging material into `harness-fix/references/`.
7. Update all old names and paths.
8. Add tests that prevent drift.

## Validation

The plugin is acceptable when:

- `plugin.json` exists and points to `./skills/`
- every public skill directory contains a `SKILL.md`
- every public skill frontmatter name matches its directory
- no legacy Superpowers skill directory is published
- no plugin skill references `docs/superpowers/specs`
- no plugin skill references `docs/superpowers/plans`
- README skill inventory matches the actual skill directories
- internal references to deleted skill names have been replaced
- TDD and debugging content remain available through Harness references
- `tests/run-all.sh` passes

## Risks And Controls

| Risk | Control |
| --- | --- |
| Mechanical file concatenation creates oversized skills | Move deep material into `references/` and keep `SKILL.md` focused on ownership and gates |
| Old Superpowers names or paths remain | Add grep-based tests that fail on legacy names and paths in published plugin skills |
| `harness-feat` and `harness-plan` overlap | Define `harness-feat` as lifecycle owner and `harness-plan` as plan generator |
| `harness-execute` and `harness-dispatch` overlap | Define `harness-execute` as plan progress owner and `harness-dispatch` as delegation mechanism |
| Root `skills/` and plugin `skills/` drift | Treat plugin as new productized artifact first; decide later whether root skills become source, legacy, or generated copies |
| Process becomes too heavy for small work | Keep `harness-using` able to route non-repository or direct-answer tasks lightly |
| Frontend work bypasses Harness control | Require repository-mode frontend work to run under brainstorm, feat, or fix ownership |

## Open Decisions

None for the first implementation pass.

Brand artwork can be improved later without blocking the plugin architecture.
