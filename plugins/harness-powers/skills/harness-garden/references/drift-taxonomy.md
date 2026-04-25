# Drift Taxonomy

A comprehensive catalog of drift types that can occur between the Harness control plane and the actual repository state. Organized by where the drift originates.

## Table of Contents

1. [Structural Drift](#structural-drift)
2. [Semantic Drift](#semantic-drift)
3. [Lifecycle Drift](#lifecycle-drift)
4. [Complexity Drift](#complexity-drift)
5. [Shadow Drift](#shadow-drift)

---

## Structural Drift

Drift in the physical structure of the control plane — files, paths, and references.

### STR-001: Missing Artifact

**Description**: A manifest entry points to a file or directory that no longer exists.
**Detection**: `check_harness.py` catches this automatically.
**Cause**: File was deleted or moved without updating the manifest.
**Severity**: Critical (if AGENTS.md or OBSERVABILITY.md) / High (other managed docs)
**Certainty**: Proven
**Remediation**: Auto-fix — remove manifest entry; or restore the file if deletion was accidental.

### STR-002: Empty Artifact

**Description**: A managed file exists but has no content (0 bytes).
**Detection**: `check_harness.py` catches this automatically.
**Cause**: File was truncated by a bad merge, accidental overwrite, or failed generation.
**Severity**: Critical
**Certainty**: Proven
**Remediation**: Flag for human — the correct content needs to be regenerated or restored from git history.

### STR-003: Broken Cross-Link

**Description**: A markdown link `[text](path)` in a managed doc points to a non-existent file.
**Detection**: Parse all `[text](path)` patterns, resolve relative to the file's directory, check existence.
**Cause**: Target file was renamed, moved, or deleted.
**Severity**: High
**Certainty**: Proven
**Remediation**: Auto-fix if the file was renamed and the new path is unambiguous (single candidate in `git log --diff-filter=R`). Otherwise, propose fix.

### STR-004: Untracked Artifact

**Description**: A harness-related file exists that is not in the manifest.
**Detection**: Scan for `AGENTS.md`, `docs/**/*.md`, `scripts/check_harness.py`.
**Cause**: File was created manually or by another skill but not added to the manifest.
**Severity**: Medium
**Certainty**: Proven
**Remediation**: Auto-fix — add the artifact to the manifest with today's date.

### STR-005: Orphaned Manifest Entry

**Description**: A manifest entry's type doesn't match reality (e.g., listed as `directory` but is a file).
**Detection**: Compare file system type against manifest type.
**Cause**: Path was replaced with a different type (directory became a file or vice versa).
**Severity**: Medium
**Certainty**: Proven
**Remediation**: Auto-fix — update the type in the manifest, or flag if the change suggests a larger refactor.

### STR-006: Stale Dates

**Description**: The Last Verified date exceeds the staleness threshold.
**Detection**: `check_harness.py` catches this as a warning.
**Cause**: No garden audit has run recently.
**Severity**: Low
**Certainty**: Proven
**Remediation**: Auto-fix — refresh the date after verifying the content is still accurate.

---

## Semantic Drift

Drift in the meaning of control plane content — what the docs SAY vs. what the code DOES.

### SEM-001: Stale Build Commands

**Description**: Commands in AGENTS.md Quick Reference or OBSERVABILITY.md don't work.
**Detection**: Try running the command with `--help` or `--version` or dry-run equivalent.
**Cause**: Build tooling changed (e.g., migrated from npm to pnpm, or from Maven to Gradle).
**Severity**: Critical
**Certainty**: Proven (command not found) / High (command exists but behavior changed)
**Remediation**: Propose fix — if the correct new command is discoverable from package.json / build files, suggest it. Otherwise flag.

### SEM-002: Deleted Module Referenced

**Description**: AGENTS.md or ARCHITECTURE.md references a module path that no longer exists.
**Detection**: Extract all path references from docs, check each against the filesystem.
**Cause**: Module was deleted, renamed, or merged.
**Severity**: High
**Certainty**: Proven
**Remediation**: Auto-fix if the module was renamed (single candidate by git log). Propose fix if merged. Flag if deleted with no clear replacement.

### SEM-003: New Module Undocumented

**Description**: A new module/package exists that has no mention in AGENTS.md or ARCHITECTURE.md.
**Detection**: Compare directory structure against documented modules. Look for directories with their own build config or >20 source files.
**Cause**: New module was added without updating the harness.
**Severity**: Medium
**Certainty**: High
**Remediation**: Propose fix — draft a module entry for AGENTS.md and evaluate whether a module-level AGENTS.md is warranted.

### SEM-004: Version Mismatch

**Description**: Technology versions documented in ARCHITECTURE.md don't match the actual project.
**Detection**: Parse version from `package.json` (engines, dependencies), `pom.xml`, `pyproject.toml`, `Cargo.toml`, etc. Compare against documented versions.
**Cause**: Dependency upgrade without doc update.
**Severity**: Low (minor version) / Medium (major version)
**Certainty**: Proven
**Remediation**: Auto-fix for version string updates in ARCHITECTURE.md when the new version is deterministic.

### SEM-005: Stale Architectural Claim

**Description**: An architectural constraint or pattern described in docs no longer holds.
**Detection**: Search for counter-examples in the code. E.g., if docs say "no raw SQL outside repository classes," search for SQL strings outside repository files.
**Cause**: Convention was relaxed, code accrued exceptions, or architecture evolved.
**Severity**: High
**Certainty**: Medium (found counter-examples, but they may be intentional exceptions)
**Remediation**: Flag for human — requires design judgment to determine if the convention changed or if the code has bugs.

### SEM-006: CI Configuration Mismatch

**Description**: OBSERVABILITY.md describes CI jobs or config paths that don't match actual CI configuration.
**Detection**: Read the actual CI config files and compare against OBSERVABILITY.md.
**Cause**: CI config was updated without updating OBSERVABILITY.md.
**Severity**: Medium
**Certainty**: High
**Remediation**: Propose fix — draft updated CI section based on actual config.

### SEM-007: Key Pattern Contradiction

**Description**: A Key Pattern in AGENTS.md contradicts actual code behavior.
**Detection**: Search for the specific pattern described and check if the codebase follows it.
**Cause**: Convention evolved, exception crept in, or pattern was aspirational rather than descriptive.
**Severity**: High
**Certainty**: Medium (depends on the specificity of the pattern)
**Remediation**: Flag for human — the team needs to decide if the code or the pattern is wrong.

---

## Lifecycle Drift

Drift in the lifecycle management of execution plans and ongoing work.

### LCY-001: Completed Plan in Active

**Description**: An execution plan in `exec-plans/active/` describes work that has been merged.
**Detection**: Read the plan, identify the feature or branch it describes, check git log for merge.
**Cause**: Plan was not archived after completion.
**Severity**: Medium
**Certainty**: High (if the branch is merged) / Medium (if work appears complete but no explicit merge)
**Remediation**: Auto-fix — move the plan file to `exec-plans/completed/` and update PLANS.md.

### LCY-002: PLANS.md Out of Sync

**Description**: PLANS.md doesn't match the actual contents of `exec-plans/active/` and `exec-plans/completed/`.
**Detection**: List files in both directories and compare against PLANS.md entries.
**Cause**: Plans were created or moved without updating the index.
**Severity**: Medium
**Certainty**: Proven
**Remediation**: Auto-fix — update PLANS.md to reflect the actual filesystem.

### LCY-003: Abandoned Active Plan

**Description**: An active plan hasn't been updated in >30 days and shows no recent git activity related to its scope.
**Detection**: Check file modification date and search git log for related commits.
**Cause**: Work was paused, abandoned, or completed without updating the plan.
**Severity**: Low
**Certainty**: Medium
**Remediation**: Flag for human — needs decision: resume, abandon, or archive.

### LCY-004: Tech Debt Tracker Stale

**Description**: `tech-debt-tracker.md` has entries that have been resolved but are still listed.
**Detection**: For each entry, check if the described issue still exists (search for relevant code patterns, test failures, etc.)
**Cause**: Debt was resolved without updating the tracker.
**Severity**: Low
**Certainty**: Medium
**Remediation**: Propose fix — suggest marking resolved entries or removing them.

---

## Complexity Drift

Drift where the harness has become more complex than the repo needs. Per Anthropic's "rippable harness" principle, harness components should be stripped when they stop pulling their weight.

### CMP-001: Shrunken Module with AGENTS.md

**Description**: A module has its own AGENTS.md but has shrunk below the creation threshold (<10 source files, or <15 files for internal domains).
**Detection**: Count source files in the module.
**Cause**: Module was refactored, simplified, or partially merged.
**Severity**: Low
**Certainty**: High
**Remediation**: Flag as complexity reduction candidate — suggest removing the module AGENTS.md and folding any unique guidance into the root AGENTS.md.

### CMP-002: Redundant Documentation

**Description**: A managed doc substantially duplicates content from another doc or from the README.
**Detection**: Compare content across docs. Look for >50% overlap in key sections.
**Cause**: Content was added to multiple places over time, or bootstrap generated docs that duplicate existing team docs.
**Severity**: Low
**Certainty**: Medium
**Remediation**: Flag as complexity reduction candidate — suggest consolidating.

### CMP-003: Over-Specified Patterns

**Description**: Key Patterns in AGENTS.md describe things the model would infer from the code itself.
**Detection**: Evaluate whether the pattern conveys information beyond what's obvious from the codebase (e.g., "use TypeScript" in a TypeScript project is over-specified).
**Cause**: Bootstrap was overly thorough, or patterns became self-evident as the codebase matured.
**Severity**: Low
**Certainty**: Low (requires judgment)
**Remediation**: Flag as complexity reduction candidate — suggest removal to free AGENTS.md space for higher-value guidance.

### CMP-004: Empty Harness Structure

**Description**: Harness directories exist but are unused (`docs/references/` with only `.gitkeep` for months).
**Detection**: Check directory contents and git log for when the directory was created.
**Cause**: Bootstrap created the structure speculatively, but it was never populated.
**Severity**: Low
**Certainty**: High (if >60 days old and still empty)
**Remediation**: Flag as complexity reduction candidate — suggest removing empty directories.

---

## Shadow Drift

Drift caused by changes happening outside the harness lifecycle — team edits, external tools, or CI changes.

### SHD-001: Externally Modified Managed Doc

**Description**: A managed doc was edited without going through the harness workflow, potentially introducing content that conflicts with the harness header comment or structure.
**Detection**: Check git log for the file — if recent commits don't include harness-tagged messages (`chore(harness):`, `docs(harness):`), the doc may have been hand-edited.
**Cause**: Team member edited a managed doc directly.
**Severity**: Low (if edits are additive) / Medium (if edits conflict with harness structure)
**Certainty**: Medium
**Remediation**: Assess the edits. If they improve the doc, incorporate them and refresh the verification date. If they conflict with harness patterns, flag for human review.

### SHD-002: Unmanaged Doc Referencing Harness

**Description**: An unmanaged doc (e.g., README) contains links to harness artifacts that are now broken.
**Detection**: Scan unmanaged docs listed in the manifest for links to managed paths.
**Cause**: Harness artifact was moved or renamed.
**Severity**: Medium
**Certainty**: Proven (broken link)
**Remediation**: Flag for human — the garden cannot edit unmanaged docs, but should report the broken link so the team can fix it.
