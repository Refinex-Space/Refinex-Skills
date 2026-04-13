---
name: harness-bootstrap
description: >-
  Bootstrap or complete a repository's Harness Engineering control plane for
  agent-first development. Use when initializing or upgrading a new or existing
  frontend, backend, full-stack, monorepo, or library repository with root and
  local AGENTS.md, docs/ routing docs, docs/OBSERVABILITY.md,
  docs/exec-plans/tech-debt-tracker.md, execution-plan directories, generated
  Harness manifest files, and a repo-local `python3 scripts/check_harness.py`
  entrypoint. Especially relevant for prompts such as `初始化 Harness`,
  `为这个项目落地 Harness Engineering`, `搭建 AGENTS/docs/PLANS`,
  `给这个仓库建立 agent-first 控制面`, or `$harness-bootstrap`.
license: Proprietary. LICENSE.txt has complete terms
---

# harness-bootstrap

Initialize the Harness Engineering control plane for a repository so that coding agents can work in it reliably — with cross-session continuity, verifiable progress, and mechanical drift detection.

This is a **low-freedom** skill. Harness initialization must be precise, deterministic, and mechanically verifiable. Follow the three phases below in order. Do not skip phases. Do not start creating files until Phase 1 (Reconnaissance) is complete.

**Announce at start:** `I'm using harness-bootstrap to establish the repository control plane.`

---

## Why this skill exists

Without a control plane, every agent session starts from scratch. The agent re-discovers the build system, re-invents conventions, and has no record of past decisions. Work drifts, gets duplicated, or contradicts earlier choices. The Harness Engineering control plane solves this by encoding everything an agent needs into the repository itself — versioned, auditable, and always current.

The primary risk this skill fights is **cargo cult scaffolding**: generating a `docs/` structure and `AGENTS.md` that _looks_ like the patterns from OpenAI and Anthropic but contains no real substance. A `docs/ARCHITECTURE.md` that says "This project uses a modular architecture" is worse than no file — it teaches agents to trust documentation that means nothing. Every generated file must be grounded in the actual repository's code, architecture, and conventions.

A secondary risk is **overwrite violence**: blindly replacing existing documentation the team already maintains. The bootstrap must DETECT what already exists and augment, not destroy.

---

## Shared terminology

All four Harness skills (harness-bootstrap, harness-garden, harness-feat, harness-fix) use these terms consistently:

| Term               | Definition                                                                                 |
| ------------------ | ------------------------------------------------------------------------------------------ |
| **Control plane**  | The set of AGENTS.md, docs/, scripts/, and manifest that guide agent work                  |
| **Execution plan** | A versioned, checkpointed plan in docs/exec-plans/                                         |
| **Managed doc**    | A doc created and maintained under harness lifecycle                                       |
| **Unmanaged doc**  | An existing team doc the harness must NOT overwrite                                        |
| **Manifest**       | Machine-readable inventory of control plane artifacts (docs/generated/harness-manifest.md) |
| **Preflight**      | Verification check run before starting any task (scripts/check_harness.py)                 |
| **Drift**          | When control plane artifacts no longer reflect repo reality                                |

---

## Phase 1 — Repository Reconnaissance

Before creating ANY file, survey the repo. This phase produces a mental model that grounds everything in Phase 2. Do not create files during this phase.

### 1.1 Read existing documentation

Scan for and read these files if they exist:

- `README.md` / `README.rst` / `README`
- `CONTRIBUTING.md` / `CONTRIBUTING`
- `.editorconfig`, `LICENSE` / `LICENSE.md`
- `CHANGELOG.md`
- Any existing `AGENTS.md` files (root and nested)
- Any existing `docs/` directory and its contents

Record which of these exist. They are **unmanaged docs** — the harness will link to them but never overwrite them.

### 1.2 Detect tech stack

Read configuration files to identify the tech stack. See `references/reconnaissance-heuristics.md` for the full detection matrix. Summary:

| File                                               | Indicates                                                                   |
| -------------------------------------------------- | --------------------------------------------------------------------------- |
| `package.json`                                     | Node.js ecosystem (check for framework: React, Vue, Next.js, Express, etc.) |
| `pom.xml` / `build.gradle(.kts)`                   | Java / Maven / Gradle                                                       |
| `Cargo.toml`                                       | Rust / Cargo                                                                |
| `pyproject.toml` / `setup.py` / `requirements.txt` | Python ecosystem                                                            |
| `go.mod`                                           | Go modules                                                                  |
| `*.csproj` / `*.sln`                               | C# / .NET                                                                   |

Also detect:

- **Test framework**: JUnit, pytest, vitest, jest, go test, cargo test, etc.
- **Linter/formatter**: ESLint, Prettier, Checkstyle, Spotless, ruff, clippy, etc.
- **CI system**: `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, `.circleci/`
- **Package manager**: from lock files (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `Cargo.lock`, `poetry.lock`, `uv.lock`)
- **Container**: `Dockerfile`, `docker-compose.yml`, `compose.yml`

### 1.3 Map directory structure

Run `find . -maxdepth 2 -type d` (excluding `.git`, `node_modules`, `target`, `build`, `dist`, `__pycache__`, `.venv`, `vendor`) to map the top-level structure. Identify:

- Source directories (`src/`, `lib/`, `app/`, `pkg/`, `cmd/`, `internal/`)
- Test directories (`test/`, `tests/`, `__tests__/`, `spec/`)
- Config directories (`config/`, `.config/`)
- Documentation (`docs/`, `doc/`, `documentation/`)

For monorepos, identify package/module boundaries (each entry with its own build config).

### 1.4 Identify module boundaries

A "module" warrants its own AGENTS.md when ANY of these is true:

- It has its OWN build config (its own `package.json`, `pom.xml`, `Cargo.toml`, etc.)
- OR it has >20 source files AND a distinct domain boundary
- OR it already has its own README

For single-package repos with clear internal domains (e.g., `src/auth/`, `src/orders/`), create module AGENTS.md only if each domain has >15 source files and distinct patterns.

Small utility repos (<500 LOC) typically need zero module AGENTS.md files.

### 1.5 Establish test baseline

If tests exist, run them before making any changes:

```bash
# Record the green/red state BEFORE any harness changes
<detected-test-command>
```

If tests fail: record the failures but proceed. The bootstrap does not fix pre-existing test failures — note them in `docs/exec-plans/tech-debt-tracker.md` instead.

If no tests exist: note this. It is a data point, not a blocker.

---

## Phase 2 — Control Plane Initialization

Create the control plane artifacts below, in this order. Each file must be grounded in Phase 1 findings — never use placeholder content that doesn't reflect the actual repo.

### 2.1 Root AGENTS.md

If no `AGENTS.md` exists, create one. If one exists, evaluate it:

- If it's a short TOC-style file: augment with missing sections, preserve existing content.
- If it's a large encyclopedia (>200 lines): ask the user before refactoring — it may contain tribal knowledge that shouldn't be discarded.

The root `AGENTS.md` must be a **table of contents, not an encyclopedia** (~100 lines max). Read `references/agents-md-guide.md` for the complete template and examples.

Required sections:

1. **Header comment**: `<!-- Generated by harness-bootstrap. Safe to edit. Audited by harness-garden. -->`
2. **Project overview**: 1-2 sentences describing what the project does (grounded in README/code)
3. **Quick reference table**: build, test, lint, run commands (from Phase 1.2)
4. **Architecture pointer**: link to `docs/ARCHITECTURE.md`
5. **Documentation index**: links to all docs/ files
6. **Key patterns**: 3-5 architectural constraints or conventions discovered from actual code — not hypothetical rules
7. **Module guide** (if applicable): table of modules with links to their AGENTS.md

### 2.2 Module-level AGENTS.md files

Only create these for modules identified in Phase 1.4. Each is ~30-50 lines. Read `references/module-agents-md-guide.md` for the template.

Contents:

1. Header comment (same as root)
2. What this module owns (its domain boundary)
3. What it does NOT own (explicit exclusions)
4. Key patterns specific to this module
5. Testing approach for this module
6. Link back to root AGENTS.md

### 2.3 docs/ directory structure

Create the docs/ structure. Read `references/docs-structure.md` for the complete specification.

```
docs/
├── PLANS.md                        # Active plans index
├── ARCHITECTURE.md                 # Top-level architecture map
├── OBSERVABILITY.md                # Build/test/lint commands + CI config
├── exec-plans/
│   ├── active/                     # Active execution plans
│   │   └── .gitkeep
│   ├── completed/                  # Archived completed plans
│   │   └── .gitkeep
│   └── tech-debt-tracker.md        # Known technical debt registry
├── generated/
│   └── harness-manifest.md         # Control plane inventory
└── references/                     # External references for agents
    └── .gitkeep
```

If a `docs/` directory already exists with team-maintained content, **merge** — create the missing structure alongside existing files. Never move or overwrite existing documentation.

#### docs/PLANS.md

```markdown
<!-- Generated by harness-bootstrap. Safe to edit. Audited by harness-garden. -->

# Plans

Active and planned work for this repository.

## Active Plans

_No active execution plans._

## Completed Plans

_No completed plans yet._
```

#### docs/ARCHITECTURE.md

Ground this in the actual repo structure from Phase 1. Include:

- High-level description of the system (1-2 paragraphs)
- Module/package map with dependency directions (ASCII diagram or list)
- Key architectural constraints observed in the actual code
- Technology stack summary with specific versions

This is NOT a repeat of the README. It is the structural map an agent needs to understand where code lives and how it connects. Every path mentioned must exist in the repo.

#### docs/OBSERVABILITY.md

This captures the commands and configs an agent needs to build, test, and verify the project. It serves as the repository's "init.sh" equivalent from Anthropic's long-running agent harness pattern — the first thing any agent reads to orient itself.

```markdown
<!-- Generated by harness-bootstrap. Safe to edit. Audited by harness-garden. -->

# Observability

## Build & Run

| Task                 | Command          | Expected               |
| -------------------- | ---------------- | ---------------------- |
| Install dependencies | `<from Phase 1>` | Exit 0                 |
| Build                | `<from Phase 1>` | Exit 0                 |
| Run tests            | `<from Phase 1>` | Exit 0, all tests pass |
| Lint / format check  | `<from Phase 1>` | Exit 0, no violations  |
| Start dev server     | `<from Phase 1>` | Server on port XXXX    |

## CI Configuration

- CI system: <detected system>
- Config path: `<path to CI config>`
- Key jobs: <list main CI jobs and what they check>

## Environment Setup

<Required SDK versions, environment variables, system dependencies>

## Verify Before Building

Before starting any feature or fix work, run this baseline check:

    <test-command>

If this fails, investigate BEFORE making additional changes.
```

#### docs/exec-plans/tech-debt-tracker.md

```markdown
<!-- Generated by harness-bootstrap. Safe to edit. Audited by harness-garden. -->

# Technical Debt Tracker

Known technical debt items. Each entry has an ID, severity, and description.

| ID  | Severity | Area | Description | Detected |
| --- | -------- | ---- | ----------- | -------- |
```

If pre-existing test failures were found in Phase 1.5, add entries here.

### 2.4 Harness manifest

Create `docs/generated/harness-manifest.md` — the machine-readable inventory of all control plane artifacts. Read `references/manifest-schema.md` for the complete format specification.

The manifest lists every managed artifact with its path, type, creation date, and last verification date. This is the verification target for `scripts/check_harness.py` and the `harness-garden` skill.

### 2.5 Validation script

Copy the bundled validation script to the target repo:

```bash
mkdir -p scripts
cp <this-skill-path>/scripts/check_harness.py scripts/check_harness.py
chmod +x scripts/check_harness.py
```

The `<this-skill-path>` is the directory containing this SKILL.md file. The script validates:

- All manifest entries exist as files/directories
- No managed docs exceed the staleness threshold (default: 30 days)
- AGENTS.md cross-links resolve to existing files
- Basic structural integrity of the control plane

Run it immediately after copying to verify: `python3 scripts/check_harness.py`

---

## Phase 3 — Baseline Verification

After creating all artifacts:

### 3.1 Run the validation script

```bash
python3 scripts/check_harness.py
```

Fix any issues it reports. The script must pass cleanly before bootstrap is complete.

### 3.2 Re-run existing tests

If tests existed in Phase 1.5, run them again. Compare exit code with the Phase 1 baseline. If tests that previously passed now fail, investigate and fix — the bootstrap must not break existing functionality.

### 3.3 Generate bootstrap report

Print a summary to the user:

```
=== Harness Bootstrap Report ===

Repository: <repo name>
Date: <today>

Created:
  ✓ AGENTS.md (root)
  ✓ docs/PLANS.md
  ✓ docs/ARCHITECTURE.md
  ✓ docs/OBSERVABILITY.md
  ✓ docs/exec-plans/active/
  ✓ docs/exec-plans/completed/
  ✓ docs/exec-plans/tech-debt-tracker.md
  ✓ docs/generated/harness-manifest.md
  ✓ scripts/check_harness.py

Preserved (unmanaged):
  → README.md
  → CONTRIBUTING.md

Validation: scripts/check_harness.py PASSED
Test baseline: <PASS/FAIL/NO TESTS>

Next steps:
  - Run `harness-garden` periodically to detect and repair drift
  - Use `harness-feat` for new feature work with execution plans
  - Use `harness-fix` for evidence-driven bug fixes
```

---

## Idempotency — Re-running bootstrap

Bootstrap can be safely re-run on a repo that already has partial harness artifacts. The behavior:

- **Existing managed files**: read and augment if incomplete, do not overwrite if already well-formed
- **Missing managed files**: create them
- **Existing unmanaged files**: always preserve, never touch
- **Manifest**: regenerate to reflect the current state
- **Validation script**: overwrite with the latest version (it has no repo-specific state)

When re-running, Phase 1 still executes fully — the repo may have changed since the last bootstrap.

---

## Critical design constraints

These are load-bearing rules. Violating them produces cargo cult scaffolding.

1. **Never overwrite unmanaged docs.** README, CONTRIBUTING, architecture docs the team already maintains — link to them from AGENTS.md, don't replace them.

2. **AGENTS.md is a map, not a manual.** Keep it under 100 lines. If content is growing past that, it belongs in `docs/`.

3. **Every generated doc references actual code paths.** "The auth module handles authentication" is cargo cult. "The auth module (`src/main/java/com/example/auth/`) implements JWT-based authentication via `AuthService` and exposes `/api/auth/*` endpoints" is grounded. If you cannot name a real file path, do not make a claim about the code.

4. **The docs/ structure reflects what actually exists.** Don't create `product-specs/` for a library with no product specs. Don't create `design-docs/` for a 200-line utility. Scale the control plane to the repo.

5. **Module AGENTS.md files earn their existence.** A module gets its own AGENTS.md only when it has enough complexity to warrant one (see Phase 1.4 criteria). A `utils/` directory with 3 files does not need an AGENTS.md.

6. **All managed files carry a header comment.** `<!-- Generated by harness-bootstrap. Safe to edit. Audited by harness-garden. -->` This tells future agents and humans that the file is part of the control plane.

7. **The manifest is the source of truth.** If a file is not in the manifest, it is not managed by the harness. If it IS in the manifest, `check_harness.py` will verify it exists and track its freshness.

8. **Commit atomically.** All bootstrap artifacts should be committed in a single commit with message: `chore: initialize Harness Engineering control plane`. This makes the bootstrap a single reviewable, revertable unit of work.

---

## Adapting to repo size

Not every repo needs the full control plane. Scale to what's appropriate:

| Repo type                      | What to create                                                  | What to skip                                   |
| ------------------------------ | --------------------------------------------------------------- | ---------------------------------------------- |
| Small utility (<500 LOC)       | Root AGENTS.md, docs/OBSERVABILITY.md, scripts/check_harness.py | Module AGENTS.md, exec-plans/, ARCHITECTURE.md |
| Standard project (500-50k LOC) | Full control plane                                              | Unnecessary module AGENTS.md files             |
| Large monorepo (>50k LOC)      | Full control plane + module AGENTS.md for major packages        | Nothing — large repos need everything          |

The validation script (`scripts/check_harness.py`) is always created regardless of repo size, because any repository benefits from mechanical verification of its control plane.

---

## Reference index

| File                                      | When to read                              |
| ----------------------------------------- | ----------------------------------------- |
| `references/docs-structure.md`            | Creating or verifying the docs/ layout    |
| `references/agents-md-guide.md`           | Writing the root AGENTS.md                |
| `references/module-agents-md-guide.md`    | Writing module-level AGENTS.md files      |
| `references/manifest-schema.md`           | Creating or updating the harness manifest |
| `references/reconnaissance-heuristics.md` | During Phase 1 tech stack detection       |
