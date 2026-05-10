---
name: init-deep
description: Deep initialization of project AGENTS.md hierarchy and control plane for AI coding agents. Use this skill whenever the user wants to set up, initialize, bootstrap, or create AGENTS.md / CLAUDE.md files for their project, or when they mention "init-deep", "harness setup", "control plane", "agent context", "project initialization for agents", or want to make their codebase agent-ready. Also trigger when a user says things like "set up my repo for Claude Code", "make this project work better with agents", "create agent instructions", "bootstrap harness", or "initialize agent docs". This skill handles both existing large codebases (where hierarchical, module-scoped AGENTS.md files are needed) and new/small projects (where brainstorming with the user comes first). Do NOT use this skill for routine code changes, bug fixes, or general documentation — it is specifically for creating the structured agent control plane.
---

# Init-Deep: Project Control Plane Initialization

This skill deeply initializes a project's agent control plane — the structured hierarchy of AGENTS.md files and supporting documentation that enables AI coding agents to work effectively across the codebase. The philosophy draws from three converging insights in the harness engineering discipline:

1. **AGENTS.md is a table of contents, not an encyclopedia.** A single monolithic file becomes stale, unverifiable, and bloated. The root AGENTS.md should be ~80–120 lines and function as a map with pointers to deeper sources of truth (OpenAI's harness engineering finding).

2. **Hierarchical, scope-local context injection.** Each module or subdirectory gets its own lean AGENTS.md containing only what an agent working in that scope needs to know. Agents auto-read the relevant files for their working directory without loading the entire repo into context (oh-my-openagent's `/init-deep` design).

3. **Progressive disclosure with mechanical enforcement.** The harness should guide agents through layered information: metadata first, then module-specific rules, then deep references. Constraints should be enforceable, not aspirational (Anthropic's harness design principles).

---

## Phase 0: Read References Before Anything Else

Before starting any work, read the appropriate reference files:

- **Always read:** `references/agents-md-patterns.md` — canonical patterns, anti-patterns, and structural templates for AGENTS.md files
- **For existing projects:** Also read `references/codebase-analysis.md` — the systematic approach to analyzing a codebase for control plane generation

These references contain hard-won patterns. Do not skip them.

---

## Phase 1: Classify the Project

Determine which path to follow based on the project's maturity:

### Path A — Existing Project (substantial codebase exists)

Indicators: the repo has multiple directories, established patterns, significant code, existing README, package configs, CI setup, etc. Proceed to **Phase 2A**.

### Path B — New/Early Project (little or no code yet)

Indicators: empty or near-empty repo, only a README or skeleton, the user is still deciding architecture. Proceed to **Phase 2B**.

### Path C — Partial Initialization (some AGENTS.md files exist but are incomplete/stale)

Indicators: existing AGENTS.md files that are bloated, monolithic, outdated, or poorly structured. Recommend the user run the companion `drift-doctor` skill instead, which is purpose-built for recalibrating an existing control plane. If the user insists on starting fresh, treat as Path A.

---

## Phase 2A: Existing Project — Deep Codebase Analysis

This is the most common and most valuable path. The goal is to understand the project deeply enough to generate a hierarchical AGENTS.md structure that accurately reflects the codebase's real architecture, conventions, and boundaries.

### Step 1: Reconnaissance

Systematically explore the project structure. Do this methodically — rushing leads to generic, useless AGENTS.md files.

1. **Directory tree** — Map the full project structure (2–3 levels deep). Identify major domains, modules, packages.
2. **Entry points** — Find main entry files, routing, configuration, and bootstrapping logic.
3. **Package configuration** — Read `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `pom.xml`, etc. Identify the tech stack, dependencies, and build tools.
4. **Existing documentation** — Read README.md, CONTRIBUTING.md, architecture docs, ADRs, any existing CLAUDE.md or AGENTS.md files.
5. **CI/CD configuration** — Read `.github/workflows/`, `Jenkinsfile`, `.gitlab-ci.yml`, etc. Understand the test, lint, and deploy pipeline.
6. **Code conventions** — Sample 3–5 representative source files from different modules. Identify naming conventions, error handling patterns, import styles, test patterns.
7. **Dependency layering** — Identify which modules depend on which. Look for clear boundaries (types → config → repo → service → runtime → UI, or similar).

### Step 2: Architecture Extraction

From the reconnaissance, extract:

- **Domain map**: What are the major functional domains? (e.g., auth, billing, API, frontend, infrastructure)
- **Layer model**: What are the architectural layers and their dependency directions?
- **Key patterns**: What recurring patterns does the codebase use? (e.g., repository pattern, event sourcing, MVC, hexagonal)
- **Conventions**: Naming, file organization, test placement, error handling idioms
- **Hard rules**: Things that must never be violated (e.g., "never import from `internal/` outside the package", "all API responses use the `Result<T>` wrapper")
- **Tooling constraints**: Linter rules, formatter config, type strictness settings

### Step 3: Determine AGENTS.md Placement

Decide where AGENTS.md files should be placed. The principle: **place an AGENTS.md wherever an agent might start working and need scope-specific context that differs from the parent.**

Typical placement for a medium-to-large project:

```
project/
├── AGENTS.md              ← Root: project-wide map, ~80-120 lines
├── docs/
│   ├── architecture.md    ← Deep architectural reference (linked from root)
│   └── conventions.md     ← Coding conventions reference (linked from root)
├── src/
│   ├── AGENTS.md          ← Source-level: common patterns across all source
│   ├── api/
│   │   └── AGENTS.md      ← API module: routes, middleware, response format
│   ├── core/
│   │   └── AGENTS.md      ← Core domain: business logic rules, model invariants
│   ├── infrastructure/
│   │   └── AGENTS.md      ← Infra: database, caching, external service patterns
│   └── frontend/
│       └── AGENTS.md      ← Frontend: component patterns, state management, styling
├── tests/
│   └── AGENTS.md          ← Testing: test conventions, fixture patterns, coverage rules
└── scripts/
    └── AGENTS.md          ← Scripts: deployment, migration, utility script conventions
```

Rules for placement:

- **Do NOT** create an AGENTS.md for every single directory. Only where context meaningfully differs.
- **Do NOT** create AGENTS.md files with fewer than 15 lines — if there's not enough to say, the parent's context is sufficient.
- **Do NOT** duplicate information across levels. Each file should add only what's new at that scope.
- **DO** err on the side of fewer files. You can always add more later; removing bloat is harder.

### Step 4: Generate the AGENTS.md Files

Generate each file following the templates in `references/agents-md-patterns.md`. Key principles for every file:

**Root AGENTS.md must contain:**

- Project identity (one sentence: what this project is)
- Tech stack summary (languages, frameworks, key dependencies)
- Architecture map with pointers to deeper docs
- Dependency direction rules (which layers may import from which)
- Hard invariants (the 3–7 rules that must never be broken)
- Build/test/lint commands (the exact commands, not just "run tests")
- Pointers to module-specific AGENTS.md files

**Module-level AGENTS.md must contain:**

- Module purpose (one sentence)
- Key patterns specific to this module
- File naming and organization conventions for this module
- Common pitfalls or traps specific to this area
- Testing approach for this module
- Cross-references to related modules

### Step 5: Present and Confirm

Present the proposed AGENTS.md hierarchy to the user. Show:

1. The file tree showing where each AGENTS.md will be placed
2. A summary of what each file will cover
3. The full content of the root AGENTS.md

Ask for confirmation before writing files. The user may know things about the project that the analysis missed. Be open to feedback — the goal is accuracy, not speed.

---

## Phase 2B: New/Early Project — Brainstorm and Scaffold

For new projects, the codebase itself can't tell us much. Instead, engage the user in a structured brainstorming session to understand their intent, then scaffold a lightweight initial control plane that will grow with the project.

### Step 1: Understand What Exists

Read everything available: README, any skeleton code, config files, design docs. Even a sparse README reveals architectural intent.

### Step 2: Structured Brainstorming

Engage the user with focused questions. Do not ask all at once — this is a conversation, not a form. Group questions by theme and ask 2–3 at a time:

**Project Identity:**

- What does this project do in one sentence?
- Who is the primary user/consumer? (end users, developers, internal team, API consumers)

**Architecture Intent:**

- What's the tech stack? (language, framework, database, deployment target)
- Is this a monolith, microservices, monorepo, library, CLI tool, or something else?
- What are the major functional domains you foresee? (e.g., auth, payments, content)

**Conventions and Principles:**

- Do you have strong opinions about code style, patterns, or approaches? (e.g., "always use functional components", "no ORMs", "event-driven")
- Are there things you explicitly want to avoid? (e.g., "no class inheritance", "no global state")
- What testing philosophy? (TDD, integration-first, E2E-focused, minimal)

**Growth Direction:**

- What does the first milestone look like?
- What does the project look like in 6 months?

### Step 3: Synthesize and Propose

Based on the brainstorm, propose an initial AGENTS.md structure. For a new project, this is typically just:

```
project/
├── AGENTS.md              ← Root: project identity, stack, principles, conventions
└── docs/
    └── architecture.md    ← Initial architecture decisions (even if brief)
```

The root AGENTS.md for a new project is shorter (40–80 lines) and more principle-focused than convention-focused, since conventions haven't solidified yet. It should capture:

- Project identity and purpose
- Tech stack and key dependencies
- Architectural principles and hard rules (even if few)
- Initial directory structure intent
- Build/test/lint commands (even if just "npm test" for now)
- A note that this file should be updated as the project grows

### Step 4: Confirm and Write

Present the proposed content to the user. For new projects, be explicit that this is a living foundation — it will need updating as the codebase grows. Recommend running the `drift-doctor` skill periodically as the project matures.

---

## Phase 3: Write the Files

After user confirmation, write all AGENTS.md files and any supporting documentation. Use the `create_file` tool for each file.

After writing, provide a concise summary:

- How many AGENTS.md files were created and where
- What supporting docs were created
- A recommendation to run `drift-doctor` after the next significant architectural change

---

## Anti-Patterns to Avoid

These are the most common failure modes. Internalize them:

1. **The Encyclopedia** — A single 500+ line AGENTS.md that tries to document everything. Agents can't use this effectively; context windows fill with irrelevant information. Break it up hierarchically.

2. **The Aspirational Doc** — Rules that describe how the code _should_ work rather than how it _does_ work. Every statement in AGENTS.md must be true right now. Aspirational rules go in a separate "roadmap" or "principles" doc.

3. **The Copy-Paste** — Multiple AGENTS.md files that repeat the same content. Each file should only contain what's unique to its scope. Shared context belongs in the nearest common ancestor.

4. **The Stale Map** — An AGENTS.md that was accurate when written but hasn't been updated. This is actively worse than no file, because agents will follow outdated instructions confidently. This is why the `drift-doctor` companion skill exists.

5. **The Vague Guide** — Instructions like "follow best practices" or "write clean code". These add no value. Be specific: "All API handlers must return `ApiResponse<T>` with proper error codes" is actionable; "handle errors properly" is not.

6. **The Style Police** — Over-specifying formatting, naming, or style when a linter/formatter already enforces it. If `prettier` handles formatting, don't repeat those rules in AGENTS.md. Instead, say "run `npx prettier --write` before committing" and link to the config.
