# Codebase Analysis Reference

This reference describes the systematic approach to analyzing an existing codebase for AGENTS.md control plane generation. The goal is to extract accurate, actionable intelligence about the project's real architecture, conventions, and boundaries — not what the README claims or what the original developers intended, but what the code actually does.

---

## Table of Contents

1. [Analysis Philosophy](#analysis-philosophy)
2. [Step-by-Step Analysis Protocol](#step-by-step-analysis-protocol)
3. [Pattern Recognition Heuristics](#pattern-recognition-heuristics)
4. [Handling Ambiguity](#handling-ambiguity)
5. [Output: The Architecture Brief](#output-the-architecture-brief)

---

## Analysis Philosophy

### Evidence Over Assumption

The codebase is the source of truth, not the README. READMEs go stale. Architecture docs describe intent, not reality. The code itself — including its inconsistencies, deviations, and workarounds — tells you what conventions are actually followed.

When analyzing, adopt the mindset of a new senior engineer joining the team on their first day. They don't know the history, but they can read code, recognize patterns, and identify boundaries. That's the intelligence you're extracting.

### Breadth Before Depth

Start with the project structure and package configuration before reading any source files. The directory tree tells you the architecture at a glance. Only after you have the macro picture should you dive into specific modules to extract patterns.

### Three-File Rule

For any convention you identify, verify it appears in at least three different files or modules. One occurrence is an instance. Two might be coincidence. Three is a pattern. This prevents encoding one developer's experiment as a project convention.

---

## Step-by-Step Analysis Protocol

### 1. Project Structure Scan

Run `find . -type f -name '*.md' -o -name '*.json' -o -name '*.toml' -o -name '*.yaml' -o -name '*.yml' | head -50` and `ls -la` at the root. This reveals:

- **Monorepo vs single-package:** Look for `packages/`, `apps/`, `libs/`, workspace config in package.json, or Nx/Turbo/Lerna config.
- **Language and framework:** The presence of `tsconfig.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `pom.xml`, etc.
- **Build system:** `webpack.config.js`, `vite.config.ts`, `next.config.js`, `Makefile`, `CMakeLists.txt`
- **Testing setup:** `jest.config.ts`, `vitest.config.ts`, `pytest.ini`, `cypress/`, `playwright.config.ts`
- **CI/CD:** `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`

### 2. Package Configuration Deep Read

Read the primary package manifest completely. For a Node.js project, `package.json` reveals:

- Scripts section → exact build, test, lint commands
- Dependencies → framework, ORM, HTTP library, state management
- DevDependencies → testing tools, linters, formatters, type checkers
- Engines → Node.js version constraints
- Workspaces → monorepo package structure

For Python, `pyproject.toml` serves the same role. For Rust, `Cargo.toml`. Read the equivalent for whatever language the project uses.

### 3. Entry Point Tracing

Find the main entry points and trace the boot sequence:

- **Backend:** Look for `main.ts`, `index.ts`, `app.ts`, `server.ts`, `main.py`, `app.py`, `main.go`, `Main.java`
- **Frontend:** Look for `main.tsx`, `App.tsx`, `index.html`, routing configuration
- **CLI:** Look for `bin/`, `cli.ts`, argument parsing setup
- **Libraries:** Look for the `main` or `exports` field in `package.json`, or `lib.rs`

Entry points reveal initialization order, dependency injection setup, middleware registration, and the overall application structure.

### 4. Architecture Boundary Detection

Identify architectural boundaries by looking for:

- **Directory-level separation:** `src/api/`, `src/domain/`, `src/infrastructure/` suggest layered architecture
- **Package-level separation:** Monorepo packages with explicit dependency declarations
- **Import restrictions:** Look for `.eslintrc` rules like `import/no-restricted-paths`, or Rust's `mod` visibility
- **Interface files:** `types.ts`, `interfaces/`, `ports/` suggest hexagonal/ports-and-adapters
- **Barrel exports:** `index.ts` files that re-export a controlled public API suggest deliberate encapsulation

### 5. Convention Extraction (The Three-File Rule)

Sample files across at least three different modules. For each, note:

- **Naming:** File names (`camelCase.ts`, `kebab-case.ts`, `PascalCase.tsx`), function names, variable names, class names
- **File structure:** Where do imports go? Is there a consistent section order? Are there standard file headers?
- **Error handling:** Try/catch vs Result types vs error callbacks vs middleware
- **Logging:** Is there a central logger? What format?
- **Testing patterns:** Are tests co-located (`__tests__/`) or in a separate `tests/` tree? What assertion style? What mocking approach?
- **State management:** (Frontend) Redux, Zustand, React Context, signals, etc.
- **Data access:** (Backend) ORM queries, raw SQL, repository pattern, query builders

Only record a convention if it appears consistently in 3+ locations. If you see two different patterns, note the inconsistency — this is valuable intelligence for the AGENTS.md ("the codebase uses both X and Y; prefer X for new code").

### 6. CI/CD Pipeline Analysis

Read the CI configuration files. They reveal:

- What checks must pass before merge (tests, lint, type check, build)
- Required test coverage thresholds
- Deploy targets and strategies
- Environment variable requirements
- Secret management approach

These translate directly into the "Build & Test Commands" and "Hard Invariants" sections of the root AGENTS.md.

### 7. Linter and Formatter Configuration

Read `.eslintrc.*`, `.prettierrc`, `biome.json`, `ruff.toml`, `clippy.toml`, etc. These are existing mechanical constraints. The AGENTS.md should reference them, not duplicate them. If a linter enforces something, the AGENTS.md says "enforced by ESLint rule X" rather than restating the rule.

---

## Pattern Recognition Heuristics

### Identifying Hard Invariants

Hard invariants are rules that, if violated, cause real damage. Look for evidence:

- **Wrapper types that centralize behavior:** If all API responses go through `ApiResponse<T>`, that's an invariant.
- **Access control patterns:** If env vars are only accessed through a config module, that's an invariant.
- **Import boundaries:** If the CI or linter fails on cross-boundary imports, that's an enforced invariant.
- **Error handling centralization:** If there's a global error handler or middleware, the error flow through it is an invariant.

The best hard invariants are ones already enforced mechanically (by linters, CI, type system). The next best are ones that are documented but not enforced. The worst are ones that are neither — these are aspirational and don't belong in AGENTS.md.

### Identifying Module Boundaries

A directory deserves its own AGENTS.md when:

1. It has its own distinct patterns (e.g., the API module uses Express middleware while the frontend uses React hooks)
2. It has its own hard rules (e.g., "never import from infrastructure in the API layer")
3. An agent working in that directory would be misled by the parent AGENTS.md alone
4. The directory has 10+ files and non-obvious conventions

A directory does NOT need its own AGENTS.md when:

1. It follows the same patterns as its parent
2. It has fewer than 10 files
3. Its purpose is self-evident from the file names and code

---

## Handling Ambiguity

### When Conventions Conflict

Real codebases have inconsistencies. When you find conflicting patterns:

1. Check which pattern appears in more recent commits (use `git log --oneline <file>`)
2. Check if one pattern appears in newer files vs older files
3. If unclear, ask the user which they prefer
4. Document the inconsistency in the AGENTS.md: "Historical code uses X. New code should use Y."

### When Documentation Contradicts Code

The code wins. Always. Document what the code does, not what the README says it does. You may note the discrepancy for the user's awareness, but the AGENTS.md must reflect reality.

### When You're Uncertain

If you can't determine a convention or rule with confidence after the analysis, leave it out. An AGENTS.md that's 80% complete and 100% accurate is far more valuable than one that's 100% complete and 80% accurate. Agents follow instructions literally — a wrong instruction causes damage.

---

## Output: The Architecture Brief

Before generating AGENTS.md files, compile your findings into a mental architecture brief. This isn't a file you write — it's a structured summary you present to the user for validation. It should cover:

1. **Project Identity** — What it is, who it serves, roughly how big (file count, LOC estimate)
2. **Tech Stack** — Language, framework, database, infra, key libraries
3. **Architecture Style** — Layered, hexagonal, microservices, modular monolith, etc.
4. **Major Domains** — The 3–8 functional areas of the codebase
5. **Dependency Direction** — Which layers may import from which
6. **Hard Invariants** — The 3–7 rules that are currently enforced or critical
7. **Key Conventions** — Naming, testing, error handling, file organization
8. **Proposed AGENTS.md Placement** — Where files will be created and why
9. **Open Questions** — Things you noticed but couldn't resolve from code alone

Present this to the user, get their corrections and additions, then generate the files.