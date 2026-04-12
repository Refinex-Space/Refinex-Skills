# Auto-Fix Rules

Defines exactly what the harness-garden can fix automatically without human confirmation. The boundary is strict: if there's any ambiguity about the correct fix, it's NOT an auto-fix.

## The Auto-Fix Contract

An auto-fix must satisfy ALL of these criteria:

1. **Deterministic**: a script could produce the same fix — no inference or judgment involved
2. **Reversible**: can be cleanly reverted with `git revert` without side effects
3. **Impact ≤ Medium**: cannot cause an agent to make materially wrong decisions if the fix is subtly incorrect
4. **Certainty = Proven**: the drift is mechanically verified, not inferred

If any criterion is not met, the fix must be a Tier 2 (proposed) or Tier 3 (flag).

---

## Permitted Auto-Fixes

### AF-001: Remove Orphaned Manifest Entry

**Trigger**: Manifest artifact entry points to a file/directory that doesn't exist.
**Fix**: Remove the row from the Control Plane Artifacts table.
**Safety check**: Verify the file was intentionally deleted (exists in git history but not on disk). If it was never tracked in git, flag instead — it may indicate a path typo in the manifest.

### AF-002: Add Untracked Artifact to Manifest

**Trigger**: A harness-related file exists that is not in the manifest (AGENTS.md, docs/ managed files, scripts/).
**Fix**: Add a new row to the Control Plane Artifacts table with the correct type, today's date for Created, and today's date for Last Verified.
**Safety check**: Only add files that match known harness artifact patterns. Do not add arbitrary files in docs/.

### AF-003: Fix Renamed File Cross-Link

**Trigger**: A markdown link `[text](old-path)` points to a non-existent file, but a file with the same basename exists at a new path (confirmed via `git log --diff-filter=R -- old-path`).
**Fix**: Update the link to point to the new path.
**Safety check**: The rename must be unambiguous — exactly one candidate with the same basename. If multiple candidates exist, this becomes a proposed fix.

### AF-004: Refresh Manifest Verification Dates

**Trigger**: Artifact passed all checks (existence, non-empty, content verified).
**Fix**: Update the Last Verified date to today.
**Safety check**: Only refresh dates for artifacts where the garden has actually verified both structure AND content. If semantic verification was skipped (e.g., the artifact wasn't read due to scope limitations), don't refresh.

### AF-005: Move Completed Plan to Completed

**Trigger**: An execution plan in `exec-plans/active/` describes work whose branch has been merged (confirmed via `git branch --merged` or `git log`).
**Fix**: Move the file from `active/` to `completed/`. Update PLANS.md to reflect the move.
**Safety check**: The plan must explicitly reference a branch or PR that is merged. If the plan doesn't reference a specific branch/PR, it becomes a proposed fix.

### AF-006: Sync PLANS.md with Filesystem

**Trigger**: PLANS.md doesn't list all plans in `exec-plans/active/` and/or `exec-plans/completed/`.
**Fix**: Add missing entries to the appropriate section of PLANS.md.
**Safety check**: Preserve any existing entries and their descriptions. Only add, never remove (removal of a PLANS.md entry is a proposed fix).

### AF-007: Fix Manifest Type Mismatch

**Trigger**: A manifest entry's type doesn't match reality (e.g., `directory` but it's a file, or vice versa).
**Fix**: Update the type field in the manifest to match reality.
**Safety check**: This is auto-fix only if the path hasn't changed. If the path was replaced, flag for human review.

### AF-008: Update Version Strings

**Trigger**: `docs/ARCHITECTURE.md` mentions a specific version (e.g., "Java 17", "Node.js 18") but the project config shows a different version.
**Fix**: Update the version string in the doc.
**Safety check**: The version must be deterministic — read directly from `package.json` `engines`, `pom.xml` `<java.version>`, `pyproject.toml` `requires-python`, etc. Only change the exact version number, not surrounding prose.

---

## Explicitly NOT Auto-Fix

These are tempting to automate but carry too much risk:

### NAF-001: Rewriting Architectural Descriptions

Even if a module was renamed, the prose describing what it does may need updating beyond a simple find-and-replace. Rewriting architectural descriptions is a proposed fix.

### NAF-002: Updating Build Commands

Build command changes often involve more than swapping one command for another — there may be new flags, environment requirements, or pre-steps. Propose new commands; don't auto-apply.

### NAF-003: Creating New Module AGENTS.md

Creating a new AGENTS.md requires understanding the module's domain boundary, patterns, and testing approach. This is always a proposed fix.

### NAF-004: Deleting Module AGENTS.md

Even if a module has shrunk below the threshold, the AGENTS.md may contain tribal knowledge. Always flag and let a human decide.

### NAF-005: Modifying Key Patterns

Key Patterns represent design decisions. Even if a pattern appears to have counter-examples in the code, the correct resolution might be fixing the code, not updating the pattern. Always flag.

### NAF-006: Editing Unmanaged Docs

The garden never modifies unmanaged documentation, even if the fix is obviously correct (e.g., a broken link in README.md). Report it; don't fix it.

---

## Auto-Fix Execution Order

When multiple auto-fixes apply, execute in this order to avoid conflicts:

1. Remove orphaned manifest entries (AF-001)
2. Add untracked artifacts (AF-002)
3. Fix type mismatches (AF-007)
4. Fix cross-links (AF-003)
5. Move completed plans (AF-005)
6. Sync PLANS.md (AF-006)
7. Update version strings (AF-008)
8. Refresh verification dates (AF-004) — always last, after all other fixes verified

This order ensures that manifest changes happen before cross-link fixes (which may depend on correct manifest entries), and date refreshes happen last (reflecting the final verified state).
