---
name: drift-doctor
description: Detect and fix drift in project AGENTS.md files and agent control plane. Use this skill whenever the user wants to audit, recalibrate, refresh, update, or fix their existing AGENTS.md files, or when they mention "drift", "stale AGENTS.md", "outdated agent instructions", "recalibrate", "sync agents", "audit control plane", "AGENTS.md is wrong/old/broken", or when they suspect their agent harness has fallen out of sync with the codebase. Also trigger when a user says things like "my agents keep making wrong assumptions", "Claude doesn't understand the new structure", "we refactored but the AGENTS.md is old", "check if my AGENTS.md is still accurate", or "update my agent docs". This skill is the companion to init-deep — init-deep creates the control plane from scratch, drift-doctor maintains it over time. Do NOT use for initial creation of AGENTS.md (use init-deep instead). Do NOT use for general code review or documentation updates unrelated to agent context.
---

# Drift-Doctor: Control Plane Recalibration

AGENTS.md files go stale. Codebases evolve — modules get added, deleted, renamed, and refactored. Conventions shift as the team makes new decisions. Dependencies get updated. Architecture boundaries move. But the AGENTS.md files that describe all of this stay frozen at whatever point they were last written.

Stale AGENTS.md is worse than no AGENTS.md. Agents follow outdated instructions with full confidence, producing code that violates current conventions, targets deleted modules, or ignores new patterns. This is the architectural entropy problem that OpenAI's harness engineering team addressed with recurring "garbage collection" agents that scan for drift and submit fixes.

Drift-Doctor is that garbage collector for your control plane. It systematically audits every AGENTS.md file against the actual codebase, identifies drift, and proposes precise corrections.

---

## When to Use Drift-Doctor

- **After a significant refactoring** — renamed modules, changed directory structure, migrated frameworks
- **Periodically** — every 2–4 weeks on active projects, or monthly on stable ones
- **When agents behave poorly** — if agents keep making the same wrong assumptions, stale AGENTS.md is often the cause
- **After a dependency major version upgrade** — framework migrations change patterns and conventions
- **When a new team member reports confusion** — if humans find the docs stale, agents definitely will too
- **After merging a large feature branch** — new code may introduce new patterns not reflected in AGENTS.md

---

## Phase 1: Inventory

### Step 1: Discover All Control Plane Files

Find every AGENTS.md, CLAUDE.md, and related control file in the project:

```bash
find . -name 'AGENTS.md' -o -name 'CLAUDE.md' -o -name '.claude' -type d | grep -v node_modules | grep -v .git
```

Also check for supporting documentation referenced by these files:

```bash
# Extract all file references from AGENTS.md files
grep -rh '\`docs/\|\.md\`\|See \`' */AGENTS.md AGENTS.md 2>/dev/null
```

### Step 2: Map the Current File Tree

Get the actual current project structure (2–3 levels):

```bash
find . -type d -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/dist/*' -not -path '*/.next/*' -maxdepth 3 | sort
```

This becomes the reference against which we check all structural claims in AGENTS.md files.

---

## Phase 2: Drift Detection

For each AGENTS.md file found, perform a systematic audit. Read the file, then verify each claim against the actual codebase. Track every discrepancy.

### Category 1: Structural Drift

These are the most dangerous because agents use them for navigation.

Checks:

- **Module map accuracy** — Does every directory listed in the module map still exist? Are there new directories that should be listed but aren't?
- **File references** — Does every file path referenced in the AGENTS.md still exist at that path? (e.g., `src/core/types/api.ts`, `docs/architecture.md`)
- **AGENTS.md coverage** — Are there directories with AGENTS.md files that no longer exist? Are there new substantial directories that should have AGENTS.md files but don't?

How to check:

```bash
# Extract all file/directory paths from an AGENTS.md
grep -oE '`[a-zA-Z0-9_./-]+`' AGENTS.md | tr -d '`' | while read path; do
  [ ! -e "$path" ] && echo "MISSING: $path"
done
```

### Category 2: Convention Drift

These cause agents to write code that doesn't match current patterns.

Checks:

- **Naming conventions** — Do recent files still follow the naming patterns described? Sample 3 files created in the last month.
- **Import patterns** — Do the dependency direction rules still hold? Check for violations.
- **Error handling** — Is the described error handling pattern still the dominant one?
- **Test patterns** — Are tests still organized and written as described?

How to check: Sample recent files (use `git log --diff-filter=A --since="30 days ago" --name-only` to find recently added files) and compare their patterns against what the AGENTS.md describes.

### Category 3: Command Drift

These cause build/test failures when agents run stale commands.

Checks:

- **Build commands** — Do all listed build/test/lint commands still work?
- **Scripts** — Do the package.json scripts (or equivalent) still match what's documented?
- **Init scripts** — If an `init.sh` or setup script is referenced, does it still exist and work?

How to check: Read the current `package.json` scripts section (or equivalent) and compare against documented commands.

### Category 4: Dependency Drift

These cause agents to use outdated APIs or missing libraries.

Checks:

- **Tech stack** — Are the framework versions and key dependencies still as described?
- **Removed dependencies** — Are any documented libraries no longer in the dependency list?
- **New major dependencies** — Are there significant new dependencies not reflected in the AGENTS.md?

### Category 5: Invariant Drift

These are the most subtle — hard invariants that are no longer enforced or no longer true.

Checks:

- **Stated invariants vs reality** — For each hard invariant, grep for at least one current example that confirms it. If you can't find one, or if you find violations, the invariant may have drifted.
- **New invariants** — Are there patterns that have become universal since the last update but aren't documented as invariants?

---

## Phase 3: Drift Report

After the audit, compile a structured drift report. Present it to the user organized by severity:

### Severity Levels

**Critical** — Will actively mislead agents into producing broken code:

- References to files/directories that no longer exist
- Commands that no longer work
- Invariants that are no longer true
- Tech stack claims that are wrong (e.g., "uses Express" when migrated to Fastify)

**High** — Will cause agents to write inconsistent or non-idiomatic code:

- Convention descriptions that no longer match the codebase majority
- Missing documentation for new major modules
- Dependency direction rules that have been violated/changed

**Medium** — Reduces agent effectiveness but doesn't cause breakage:

- New directories that should have AGENTS.md files but don't
- Incomplete or missing cross-references
- Minor convention drift (e.g., new naming pattern emerging but not yet dominant)

**Low** — Cosmetic or minor improvements:

- Stale version numbers in stack description
- Slightly imprecise wording
- Missing links to new documentation

### Report Format

Present the report as a concise summary with one section per audited file:

```
## Drift Report — [Date]

### Root AGENTS.md
- **CRITICAL:** Module map references `src/legacy/` which was deleted in commit abc123
- **HIGH:** Build command `npm test` should be `pnpm test` (migrated package manager)
- **MEDIUM:** No mention of new `src/notifications/` module (added 3 weeks ago)

### src/api/AGENTS.md
- **HIGH:** Error handling section describes try/catch pattern but recent handlers use Result<T>
- **MEDIUM:** Missing mention of rate limiting middleware added to all routes

### src/frontend/AGENTS.md
- **LOW:** React version listed as 18.x but is now 19.x
```

---

## Phase 4: Remediation

After the user reviews the drift report, apply fixes. The remediation strategy depends on severity:

### For Critical and High Drift

Fix immediately. These are actively harmful. For each fix:

1. Read the current state of the relevant code/config
2. Write the corrected AGENTS.md content
3. Present the diff to the user for confirmation

### For Medium Drift

Propose fixes but let the user prioritize. Some medium items (like adding AGENTS.md to new modules) may require running a mini version of init-deep's Phase 2A analysis for that specific module.

### For Low Drift

Batch into a single update. Present all low-severity changes together for quick approval.

### When Drift is Severe

If more than 40% of the content in any AGENTS.md file is stale, recommend a full regeneration of that file rather than incremental patching. Use the init-deep skill's analysis approach for the relevant scope. Patching a fundamentally stale file leads to Frankenstein documentation — technically updated but structurally incoherent.

---

## Phase 5: Prevention Recommendations

After remediation, suggest preventive measures to the user:

1. **Add AGENTS.md to PR review checklists** — When a PR changes module structure, conventions, or hard invariants, the reviewer should check if AGENTS.md needs updating.

2. **Schedule periodic drift-doctor runs** — Suggest a cadence based on how active the project is (weekly for fast-moving projects, monthly for stable ones).

3. **Use CI checks for structural drift** — A simple CI script can verify that all file paths referenced in AGENTS.md actually exist:

```bash
# .github/workflows/agents-md-check.yml
grep -roE '`[a-zA-Z0-9_./-]+\.(ts|js|py|md|json|yaml|toml)`' **/AGENTS.md |
  tr -d '`' | while read ref; do
    [ ! -e "$ref" ] && echo "::warning::Stale reference: $ref" && exit 1
  done
```

4. **Keep AGENTS.md files short** — The shorter the file, the less there is to go stale. If a file has grown past the recommended limits (root ≤ 120 lines, module ≤ 80 lines), it probably contains content that belongs in dedicated docs.

5. **Link, don't inline** — When AGENTS.md points to `docs/architecture.md` instead of inlining architecture details, the architecture doc can be updated independently. AGENTS.md only drifts when the file it points to moves or disappears — which is a much smaller surface area than keeping the content in sync.

---

## Special Cases

### Monorepo Drift

In monorepos, each package may have its own AGENTS.md. Check that:

- The root AGENTS.md correctly lists all current packages
- Cross-package dependency rules are still accurate
- Package-level AGENTS.md files don't contradict the root

### Post-Migration Drift

After a major migration (framework, language, architecture), the control plane likely needs near-complete regeneration. Recommend running init-deep on the affected areas rather than trying to patch.

### Partial Control Planes

If the project has some AGENTS.md files but they're incomplete or poorly structured (e.g., a single monolithic root file with no module-level files), this is a "structural deficiency" rather than "drift." Recommend init-deep for the areas without coverage, and drift-doctor for the areas with existing (but possibly stale) coverage.
