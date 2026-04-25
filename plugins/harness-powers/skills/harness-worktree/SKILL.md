---
name: harness-worktree
description: >-
  Use when starting Harness implementation work that needs an isolated git
  worktree, especially before executing an approved plan or beginning a scoped
  feature/fix branch. Select the repository's worktree directory, verify ignored
  project-local directories, create a `codex/`-prefixed branch by default, run
  setup and baseline checks, and prevent plan execution on main/master unless
  the user explicitly allows it.
license: MIT
---

# harness-worktree

Create an isolated workspace for Harness implementation work before changing code.

This is a **low-freedom** skill. Isolation and baseline evidence are mandatory.

**Announce at start:** `I'm using harness-worktree to create an isolated implementation workspace.`

---

## Hard gates

- Do not execute an implementation plan on `main` or `master` unless the user explicitly says to work there.
- Do not create a project-local worktree until the chosen worktree directory is verified as ignored.
- Do not treat a worktree as ready until setup and baseline commands have been run or explicitly ruled out.
- Do not overwrite or delete existing worktrees while choosing a location.

---

## Directory selection

Choose the worktree parent directory in this exact order:

1. `.worktrees/`
   - If it exists, use it.
   - If both `.worktrees/` and `worktrees/` exist, `.worktrees/` wins.

2. `worktrees/`
   - If `.worktrees/` does not exist and `worktrees/` exists, use `worktrees/`.

3. Explicit user preference
   - If neither directory exists, honor an explicit user or repository preference from the current request, root `AGENTS.md`, nearby `AGENTS.md`, or project docs.
   - Only ask the user when no existing directory and no explicit preference can be found.

Prompt when needed:

```text
No worktree directory preference was found. Where should I create the worktree?

1. .worktrees/ (project-local, hidden)
2. worktrees/ (project-local, visible)
3. A path you specify
```

---

## Ignored-directory verification

For project-local directories, verify the exact parent directory is ignored before creating the worktree:

```bash
git check-ignore -q .worktrees/
git check-ignore -q worktrees/
```

Use the command that matches the selected directory.

If the selected directory is not ignored:

1. Stop before creating the worktree.
2. Report that tracking the worktree parent would pollute `git status`.
3. Ask for permission to add the directory to `.gitignore` or for an alternate location.

External absolute paths outside the repository do not need repository ignore verification, but still require a clear user or repository preference.

---

## Branch naming

Use a `codex/` branch prefix by default unless the user gives a different branch name or repository rules require another prefix.

Examples:

```bash
git worktree add .worktrees/codex-task-8 -b codex/task-8-harness-worktree-finish
git worktree add worktrees/codex-login-fix -b codex/login-fix
```

Prefer short, lowercase, hyphenated names that identify the task.

---

## Setup workflow

Run these discovery commands from the repository root:

```bash
git rev-parse --show-toplevel
git branch --show-current
git status --short
git worktree list
```

If the current branch is `main` or `master`, create or switch into a worktree before executing any plan unless the user explicitly allowed direct work there.

Create the worktree:

```bash
git worktree add <worktree-path> -b <branch-name>
cd <worktree-path>
```

Run one project setup command per ecosystem, using the repository's documented command when it exists in `AGENTS.md`, `README`, package scripts, Makefiles, or project docs.

For Node.js projects, select exactly one package manager from lockfiles before installing:

| Evidence | Setup command |
| --- | --- |
| `pnpm-lock.yaml` | `pnpm install` |
| `yarn.lock` | `yarn install` |
| `package-lock.json` | `npm ci` |
| `package.json` only | ask or use the documented command; if none exists, `npm install` is the fallback |

Do not run `npm install` before checking for `pnpm-lock.yaml` or `yarn.lock`; that can create the wrong lockfile and invalidate the baseline.

Common non-Node setup commands:

```bash
test -f requirements.txt && python3 -m pip install -r requirements.txt
test -f pyproject.toml && python3 -m pip install -e .
test -f Cargo.toml && cargo build
test -f go.mod && go mod download
```

---

## Baseline verification

Run a baseline command before implementation so later failures can be compared against a known starting state.

Prefer repository-specific commands. Common fallbacks:

```bash
npm test
pnpm test
yarn test
python3 -m unittest
pytest
cargo test
go test ./...
make test
```

If baseline fails:

1. Capture the command, exit code, and failing summary.
2. Do not start plan execution automatically.
3. Ask whether to investigate baseline failures or proceed with the known failing baseline.

If baseline passes, report the worktree path, branch name, setup commands run, and verification command result.

---

## Output contract

When ready, report:

```text
Worktree: <absolute-path>
Branch: <branch-name>
Base branch: <base-branch>
Setup: <commands run or skipped with reason>
Baseline: <command and result>
Ready for: <plan or task name>
```

---

## Red flags

Stop if you are about to:

- run a plan from `main` or `master` without explicit user permission
- skip ignored-directory verification for `.worktrees/` or `worktrees/`
- create a branch without the default `codex/` prefix when no alternate was requested
- proceed after a failing baseline without user approval
- create a legacy skill directory or route users through old skill entry names
