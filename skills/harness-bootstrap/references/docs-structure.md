# docs/ Directory Structure

The `docs/` directory is the system of record for the Harness Engineering control plane. Agents start from `AGENTS.md` (table of contents), follow links into `docs/`, and find everything they need to understand, plan, and verify their work.

## Required Structure

```
docs/
├── PLANS.md                        # Index of active and completed work
├── ARCHITECTURE.md                 # Top-level architecture map
├── OBSERVABILITY.md                # Build/test/lint/CI commands
├── exec-plans/
│   ├── active/                     # Live execution plans (one .md per plan)
│   │   └── .gitkeep
│   ├── completed/                  # Archived plans (moved here on completion)
│   │   └── .gitkeep
│   └── tech-debt-tracker.md        # Registry of known technical debt
├── generated/
│   └── harness-manifest.md         # Machine-readable control plane inventory
└── references/                     # External reference material for agents
    └── .gitkeep
```

## File Descriptions

### PLANS.md

The active plans index. Links to execution plans in `exec-plans/active/`. When a plan is completed, its link moves to the "Completed Plans" section, and the plan file moves to `exec-plans/completed/`.

This file is the first thing an agent reads when starting a new task — it tells the agent what work is in progress and what has been done.

### ARCHITECTURE.md

A structural map of the codebase. Not a feature description (that's the README's job), but a map of how the code is organized: modules, layers, dependency directions, key abstractions.

Requirements:
- Every directory or package mentioned must actually exist
- Dependency directions should reflect actual imports, not aspirational architecture
- Include the technology stack with specific version numbers
- If the project has architectural constraints (e.g., "no cross-domain service calls"), state them here with the reasoning

### OBSERVABILITY.md

The operational handbook for the repo. Contains the exact commands needed to build, test, lint, and run the project. This is the equivalent of Anthropic's `init.sh` pattern — the first thing any agent needs to orient itself.

Requirements:
- Every command listed must actually work when run from the repo root
- Include expected outcomes (exit codes, output patterns)
- Document required environment variables and SDK versions
- Reference the CI config path so agents can understand what CI checks

### exec-plans/

Execution plans are versioned, checkpointed plans for feature work or bug fixes. They live in `active/` while in progress and move to `completed/` when done.

An execution plan is a first-class artifact — it gets committed to git, reviewed, and updated as work progresses. The plan records WHAT was decided, WHY, what the checkpoints are, and what the verification criteria are. This gives cross-session continuity: a new agent instance can read the plan and pick up where the previous one left off.

Naming convention: `YYYY-MM-DD-short-description.md` (e.g., `2026-04-12-add-payment-module.md`)

### exec-plans/tech-debt-tracker.md

A registry of known technical debt. Each entry has:
- **ID**: sequential (TD-001, TD-002, etc.)
- **Severity**: low / medium / high / critical
- **Area**: which module or system area is affected
- **Description**: what the debt is and why it matters
- **Detected**: date when the debt was identified

This file is populated during bootstrap (pre-existing test failures, known issues) and maintained during ongoing development.

### generated/

Machine-generated documentation. Files here are NOT meant to be hand-edited — they are produced by scripts or agents and can be regenerated.

Currently contains:
- `harness-manifest.md` — the control plane inventory (see `references/manifest-schema.md`)

Future additions might include: auto-generated API schema docs, dependency graphs, coverage reports.

### references/

External reference material that agents might need during their work. Examples:
- LLM-optimized documentation for key dependencies (the `.txt` or `.md` versions)
- Design system references
- API specifications for external services the project integrates with

Files here are informational — they describe things outside the repo, not things inside it (which belong in ARCHITECTURE.md or module AGENTS.md files).

## Optional Extensions

For larger repos, additional `docs/` subdirectories may be warranted:

| Directory | When to add | Contents |
|-----------|------------|----------|
| `docs/design-docs/` | When the project has formal design proposals | Design documents with status tracking |
| `docs/product-specs/` | When product requirements are tracked in-repo | Feature specs, user stories |
| `docs/runbooks/` | When the project has operational procedures | Incident response, deployment procedures |

Do NOT create these preemptively. Add them when the first document of that type is needed.

## Merge Rules for Existing docs/

If the repo already has a `docs/` directory:

1. **Never delete or move existing files.** The team put them there for a reason.
2. **Create missing harness files alongside existing content.** If `docs/api.md` already exists, fine — create `docs/PLANS.md` next to it.
3. **If there's a naming conflict** (e.g., the repo already has `docs/ARCHITECTURE.md`): read the existing file. If it serves the same purpose as the harness version, use it as-is and list it in the manifest. If it serves a different purpose, choose a non-conflicting name like `docs/HARNESS-ARCHITECTURE.md`.
4. **Record existing docs as unmanaged** in the manifest's "Unmanaged Documentation" section.
