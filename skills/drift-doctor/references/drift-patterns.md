# Drift Detection Patterns Reference

Common drift signatures organized by what triggers them. Use this to recognize drift quickly during audits.

---

## Trigger: Directory Restructuring

**Symptoms:**
- Module map in root AGENTS.md lists directories that don't exist
- AGENTS.md files exist in directories that have been moved or renamed
- Cross-references between AGENTS.md files point to wrong locations
- "See `src/old-name/`" when the directory is now `src/new-name/`

**Detection:** Compare the module map table against `find . -maxdepth 2 -type d`. Any mismatch is structural drift.

**Fix priority:** Critical — agents literally cannot navigate to non-existent paths.

---

## Trigger: Package Manager Migration

**Symptoms:**
- Commands section says `npm run test` but `package-lock.json` is gone and `pnpm-lock.yaml` exists
- CI config uses a different package manager than AGENTS.md documents
- `engines` field in `package.json` has changed

**Detection:** Check which lockfile exists (`package-lock.json` vs `yarn.lock` vs `pnpm-lock.yaml` vs `bun.lockb`). Compare against documented commands.

**Fix priority:** Critical — running the wrong package manager can install different dependency versions.

---

## Trigger: Framework Major Version Upgrade

**Symptoms:**
- API patterns described don't match current framework API (e.g., Next.js Pages Router described but App Router is used)
- Import paths in examples no longer work
- Deprecated patterns documented as current

**Detection:** Read the framework version in the manifest, then spot-check 2-3 examples from the AGENTS.md against actual current code.

**Fix priority:** High — agents will generate code using outdated APIs.

---

## Trigger: New Module Added

**Symptoms:**
- A substantial new directory (10+ files) exists with no AGENTS.md coverage
- Root module map is missing the new entry
- No dependency direction rules cover the new module

**Detection:** Compare directories at depth 2 against the module map. New directories with 10+ files that aren't listed are gaps.

**Fix priority:** Medium — agents won't break existing code, but they won't understand the new module's patterns either.

---

## Trigger: Convention Evolution

**Symptoms:**
- Recent files use a different pattern than what AGENTS.md describes
- Two competing patterns exist, with the newer one more common in recent commits
- Linter/formatter config has changed but AGENTS.md still references old rules

**Detection:** Use `git log --diff-filter=A --since="60 days ago" --name-only` to find recent files. Compare their patterns against AGENTS.md descriptions. If >50% of recent files deviate, the convention has shifted.

**Fix priority:** High if the old pattern causes linter failures; Medium otherwise.

---

## Trigger: CI Pipeline Changes

**Symptoms:**
- AGENTS.md documents checks that no longer run in CI
- New CI checks exist that agents should know about but aren't documented
- Test coverage thresholds have changed

**Detection:** Read current CI config and compare against AGENTS.md's build/test section.

**Fix priority:** Medium — agents may not run required checks, leading to CI failures on PRs.

---

## Trigger: Hard Invariant Violations in Codebase

**Symptoms:**
- An invariant documented in AGENTS.md is violated in recent code (within last 30 days)
- The violation is not in legacy code — it's in new, actively maintained code
- The invariant may have been intentionally relaxed

**Detection:** For each documented invariant, construct a grep/search that would find violations. If violations exist in recent code, the invariant has drifted.

**Fix priority:** Critical if the invariant is wrong (remove or correct it). Medium if the codebase has violations that should be fixed.

---

## Healthy Control Plane Indicators

A control plane is healthy when:
- Every path referenced in any AGENTS.md exists on disk
- Every command documented actually runs without error
- Every convention described matches what 80%+ of recent files do
- Every hard invariant can be verified against current code
- No AGENTS.md file exceeds the recommended line limits
- Module AGENTS.md files don't duplicate root content
- New significant directories (10+ files, added in last 60 days) have appropriate coverage