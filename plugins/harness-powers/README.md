# Harness Powers

Harness Powers is a Codex App plugin for agent-first software development. It combines the repository control-plane discipline of Harness Engineering with the strongest workflow ideas from Superpowers: brainstorming, planning, TDD, debugging, review, dispatch, worktree isolation, and evidence-backed completion.

This plugin is Harness-first. It does not publish legacy Superpowers skill names. Instead, it exposes one coherent `harness-*` skill surface where `harness-using` owns routing and `harness-verify` owns completion evidence.

## Relationship To Harness Engineering

Harness Powers keeps the Harness control plane as the primary source of truth:

- `AGENTS.md` and module `AGENTS.md` files describe repository rules.
- `docs/PLANS.md` indexes active and completed work.
- `docs/exec-plans/specs/` stores approved design specs.
- `docs/exec-plans/active/` stores live execution plans.
- `docs/exec-plans/completed/` stores archived plans.
- `docs/OBSERVABILITY.md` records proving commands.

## Relationship To Superpowers

Harness Powers absorbs proven Superpowers workflows without preserving overlapping public entry points. The original concepts are mapped into Harness-owned skills:

- brainstorming -> `harness-brainstorm`
- writing plans -> `harness-plan`
- executing plans -> `harness-execute`
- verification before completion -> `harness-verify`
- code review request and response -> `harness-review`
- subagent and parallel execution -> `harness-dispatch`
- worktree setup -> `harness-worktree`
- branch completion -> `harness-finish`

TDD and systematic debugging become references inside `harness-feat` and `harness-fix`.

## Lifecycle

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

Direct feature work normally routes through:

```text
harness-using -> harness-feat -> harness-verify -> harness-finish
```

Bug, regression, incident, and flaky-path work normally routes through:

```text
harness-using -> harness-fix -> harness-verify -> harness-finish
```

## Skills

The first Harness Powers release publishes:

| Skill | Role |
| --- | --- |
| `harness-using` | Global entry router and process-before-domain discipline |
| `harness-brainstorm` | Requirements clarification, options, and approved design specs |
| `harness-plan` | Active execution plan generation |
| `harness-execute` | Checkpointed active plan execution |
| `harness-bootstrap` | Repository control-plane initialization |
| `harness-garden` | Control-plane drift audit and repair |
| `harness-feat` | Feature and structured refactor lifecycle |
| `harness-fix` | Bug, regression, incident, and flaky-path lifecycle |
| `harness-verify` | Completion evidence gate |
| `harness-review` | Diff, plan, PR, and feedback review |
| `harness-dispatch` | Subagent and parallel task orchestration |
| `harness-worktree` | Isolated worktree and branch preparation |
| `harness-finish` | Merge, PR, keep, or discard finishing flow |
| `harness-frontend` | Frontend domain workflow under Harness lifecycle |

## Non-Published Legacy Skills

Harness Powers intentionally does not publish:

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

## Local Development

Edit the plugin in place under:

```bash
plugins/harness-powers/
```

During local iteration, keep source material read-only:

```bash
# Inspect upstream Superpowers source material only
ls /Users/refinex/.codex/plugins/cache/openai-curated/superpowers

# Inspect this plugin's public skill surface
find plugins/harness-powers/skills -maxdepth 2 -name SKILL.md | sort

# Validate plugin metadata
python3 -m json.tool plugins/harness-powers/.codex-plugin/plugin.json >/dev/null
```

To test a local install in Codex App, point the app or plugin marketplace entry at `plugins/harness-powers/`. Do not edit the installed cache copy directly; make changes in this repository and reinstall or relink from here.

## Local Validation

From the repository root:

```bash
tests/run-all.sh
```

For plugin-specific tests:

```bash
python3 -m unittest tests.content.test_harness_powers_plugin -v
```
