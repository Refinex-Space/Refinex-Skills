---
name: harness-bootstrap
description: >
  Bootstrap or complete a repository's Harness Engineering control plane
  for agent-first development. Use when Codex needs to initialize or
  upgrade a new or existing frontend, backend, full-stack, monorepo, or
  library repository with root and local `AGENTS.md`, `docs/` routing
  docs, `docs/OBSERVABILITY.md`, `docs/exec-plans/tech-debt-tracker.md`,
  execution-plan directories, generated Harness manifest files, and a
  repo-local `python3 scripts/check_harness.py` entrypoint. Especially
  relevant for prompts such as `初始化 Harness`, `为这个项目落地 Harness
  Engineering`, `搭建 AGENTS/docs/PLANS`, `给这个仓库建立 agent-first 控制面`,
  or `$harness-bootstrap`.
---

# Harness Bootstrap

Profile a repository, choose an adaptive Harness scaffold, and install a
production-grade control plane without blindly overwriting strategic
docs.

## Core Commitments

- Treat the real repository as the source of truth.
- Keep root routing short; push detail into `docs/` and local `AGENTS.md`.
- Externalize continuity into plans, generated facts, and stable docs.
- Install mechanical checks and manifests so future drift is inspectable.
- Prefer preserving unmanaged strategy docs over forcing unsafe rewrites.

## Authority Ladder

Use this order when signals conflict:

1. Real repository structure and existing boundaries
2. `references/harness-principles.md`
3. `references/scaffold-matrix.md`
4. `references/agents-topology-rules.md`
5. User preferences that do not violate repository truth

## Start Sequence

1. Run `scripts/profile_repo.py` on the target repository.
2. Infer documentation language from the repo unless the user explicitly overrides it.
3. Read these references as needed:
   - `references/harness-principles.md`
   - `references/scaffold-matrix.md`
   - `references/agents-topology-rules.md`
4. Use `scripts/bootstrap_harness.py` as the main installer.
5. Use `scripts/init_repo_harness_check.py` only when reinstalling the mechanical manifest and repo-local check.

## Workflow

### 1. Profile Before You Scaffold

Infer:

- project type
- language and framework signals
- real workspace boundaries
- existing Harness coverage
- required route docs
- missing critical files

Do not ask the user for structure the repository already reveals.

### 2. Scaffold Adaptively

- Always create or maintain the core Harness files.
- Always include `docs/OBSERVABILITY.md` and `docs/exec-plans/tech-debt-tracker.md`.
- Add frontend or design docs only when repository signals justify them.
- Create local `AGENTS.md` only at real handoff boundaries.
- Generate a managed active plan at `docs/exec-plans/active/harness-bootstrap.md`.

### 3. Preserve Unmanaged Strategic Files

- If a critical file already exists and is unmanaged, do not blindly rewrite it.
- Skip unsafe rewrites, record the reason in the bootstrap plan, and leave the repo in a safe partial state.
- Files marked with `<!-- HARNESS:MANAGED FILE -->` or `# HARNESS:MANAGED FILE` may be regenerated.

### 4. Install Mechanical Entry Points

- Always install:
  - `scripts/check_harness.py`
  - `docs/generated/harness-manifest.md`
- The repo-local check must be able to flag missing routes, oversized routing docs, archive-header drift, and manifest fingerprint drift.

### 5. Validate Immediately

- Run the repo-local check after bootstrapping.
- Confirm the generated manifest, route docs, and local `AGENTS.md` coverage reflect the post-bootstrap repository state, not the pre-bootstrap snapshot.
- Keep the bootstrap plan active if unmanaged strategic files still require manual remediation.

## Preferred Commands

```bash
python3 scripts/profile_repo.py --repo <repo> --format md
python3 scripts/bootstrap_harness.py --repo <repo> --language auto
python3 scripts/init_repo_harness_check.py --repo <repo> --language auto
python3 scripts/run_fixture_tests.py
```

Use `--dry-run` first when bootstrapping an existing repository with
substantial unmanaged documentation.

## Guardrails

- `AGENTS.md` must stay a routing map, not a handbook.
- Do not install CI, linter, or workflow mutations by default.
- Do not overwrite unmanaged root `AGENTS.md`, unmanaged `docs/PLANS.md`, or other unmanaged strategic docs unless the rewrite is obviously safe.
- Keep observability, tech-debt tracking, and generated facts as first-class harness surfaces.
- Prefer leaving a bootstrap plan with explicit follow-up over forcing a risky rewrite.
- Keep generated files mechanical and reproducible.
