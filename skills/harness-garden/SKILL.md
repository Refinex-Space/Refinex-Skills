---
name: harness-garden
description: >-
  Audit, repair, and continuously correct Harness Engineering drift in
  repositories that already have some form of agent control plane. Use when
  inspecting root and local AGENTS.md, docs/PLANS.md, docs/OBSERVABILITY.md,
  docs/exec-plans, generated Harness manifests, and repo-local
  `python3 scripts/check_harness.py`; then auto-fix low-risk drift, refresh
  stale managed files, and create a remediation execution plan for high-risk
  semantic rewrites. Especially relevant for prompts such as
  `检查这个项目的 Harness 是否健康`, `修复文档索引和 AGENTS 偏离`,
  `纠正 Harness 漂移`, `做 doc-gardening`, `做 Harness audit`,
  or `$harness-garden`.
license: Proprietary. LICENSE.txt has complete terms
---

# harness-garden

Detect and repair drift between the Harness Engineering control plane and the actual repository. The control plane is only useful when it tells the truth — this skill makes sure it does.

This is a **low-freedom** skill. Drift detection must be systematic and exhaustive. Remediation must be conservative and mechanically verifiable. Follow the four phases below in order. Do not skip phases. Do not auto-fix anything until Phase 2 (Semantic Drift Audit) is complete and all findings are triaged.

---

## Why this skill exists

A control plane that doesn't reflect reality is worse than no control plane at all. Agents trust `AGENTS.md` and `docs/` to navigate the codebase. When those files describe deleted modules, reference renamed paths, or list outdated build commands, agents make confident but wrong decisions. OpenAI calls this "a graveyard of stale rules" — and it's how monolithic manuals fail.

The primary risk this skill fights is **false confidence**: the control plane _looks_ healthy (files exist, structure is intact, `check_harness.py` passes) but the _content_ no longer reflects reality. A manifest check tells you the control plane exists; a garden audit tells you it's still true.

A secondary risk is **harness over-complexity**. Per Anthropic's observation, every harness component encodes an assumption about what the model can't do — and those assumptions go stale fast. A module AGENTS.md created when the codebase had three modules may be unnecessary overhead after a refactor consolidated them into one. The garden should strip harness complexity that no longer pulls its weight.

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

## Phase 1 — Manifest Integrity Check

Start every garden audit with the mechanical checks. These are fast, deterministic, and surface the most obvious problems.

### 1.1 Run preflight

```bash
python3 scripts/check_harness.py
```

Record the output. This catches:

- Missing or empty managed files
- Broken cross-links in AGENTS.md
- Stale artifacts past the freshness threshold

If `check_harness.py` does not exist, the repo has no harness — suggest running `harness-bootstrap` instead and stop.

### 1.2 Verify manifest completeness

Read `docs/generated/harness-manifest.md`. For every entry in the Control Plane Artifacts table:

1. **Existence**: file or directory must exist at the listed path
2. **Non-emptiness**: files must have content (>0 bytes)
3. **Type match**: the artifact type must be correct (e.g., a file listed as `directory` is actually a directory)
4. **Date validity**: Created and Last Verified dates must be valid ISO dates, and Created ≤ Last Verified

### 1.3 Check for untracked artifacts

Scan the repo for harness-related files that are NOT in the manifest:

- Any `AGENTS.md` files (root or nested) not listed
- Any `docs/exec-plans/active/*.md` files not tracked
- Any files in `docs/generated/` not listed
- Any `scripts/check_harness.py` variant not listed

Untracked artifacts are a sign of manual edits that bypassed the harness lifecycle. They need to be added to the manifest or removed.

### 1.4 Cross-link verification

Check all markdown links in ALL managed docs (not just root AGENTS.md):

- Every `[text](path)` where path is a relative file reference must resolve to an existing file
- Internal anchor links (`#section-name`) should reference existing headings in the target file
- External links (http/https) are noted but not verified (network calls are expensive and unreliable)

Record all broken links with their source file and line.

---

## Phase 2 — Semantic Drift Audit

Go beyond file existence — check if the CONTENT matches the actual repository. This is the core of what makes a garden audit valuable beyond `check_harness.py`.

Read `references/drift-taxonomy.md` for the complete catalog of drift types. The summary below covers the most critical checks.

### 2.1 AGENTS.md accuracy

For the root AGENTS.md and every module-level AGENTS.md:

- **Quick Reference table**: run each listed command (build, test, lint) in a dry-run or `--help` mode to verify they exist. If a command mentions a specific binary (e.g., `./gradlew`, `pnpm`), confirm the binary exists.
- **Architecture pointers**: every path referenced (e.g., "the auth module at `src/auth/`") must exist.
- **Module Guide table**: every module listed must still exist. Every module that exists should be listed (check for new modules that appeared since last audit).
- **Key Patterns**: these are semantic claims about the code. Flag patterns that reference specific files, classes, or conventions — they are verifiable. Flag generic patterns as low-priority.
- **Documentation Index links**: every linked doc must exist and be non-empty.

### 2.2 Architecture doc accuracy

Read `docs/ARCHITECTURE.md` and cross-reference against the actual directory structure:

- Every module or package mentioned must exist at its stated path
- Dependency direction claims (e.g., "A depends on B but not vice versa") can be spot-checked by searching for import statements
- Technology stack versions can be cross-checked against `package.json` / `pom.xml` / `pyproject.toml` / `Cargo.toml`
- ASCII diagrams or structural descriptions should match the current directory layout

### 2.3 Observability doc accuracy

Read `docs/OBSERVABILITY.md`:

- Every command in the Build & Run table should be runnable (dry-run check where possible)
- CI system and config path must match the actual CI configuration
- SDK versions and environment requirements should match the current project configuration

### 2.4 Execution plan hygiene

Scan `docs/exec-plans/active/`:

- Active plans that reference features already merged (check git log) should be moved to `completed/`
- Active plans that reference code patterns or file paths that no longer exist should be flagged
- Plans older than 30 days in `active/` should be reviewed for abandonment

Scan `docs/exec-plans/completed/`:

- Completed plans need no content audit, but their links from `docs/PLANS.md` should be valid

Check `docs/PLANS.md`:

- Every plan listed under "Active Plans" must have a corresponding file in `exec-plans/active/`
- Every plan listed under "Completed Plans" must have a corresponding file in `exec-plans/completed/`
- Plans present in the filesystem but not listed in PLANS.md need entries added

### 2.5 New module discovery

Search for new directories or packages that look like modules but have no AGENTS.md and are not mentioned in the root AGENTS.md:

- Directories with their own `package.json`, `pom.xml`, `Cargo.toml`, `go.mod`, etc.
- Directories with >20 source files and a distinct domain boundary
- Directories that had significant commits since the last garden audit (use git log with `--since`)

Each discovered module should be evaluated against the same criteria from harness-bootstrap Phase 1.4 to decide if it warrants its own AGENTS.md.

### 2.6 Orphaned module detection

Check for module-level AGENTS.md files that reference modules which have been:

- Deleted entirely (directory no longer exists)
- Renamed (directory exists at a different path)
- Merged into another module (files consolidated elsewhere)

These are high-confidence drift — the AGENTS.md is provably stale.

### 2.7 Harness complexity audit

Evaluate whether current harness components are still load-bearing. Per Anthropic's rippable harness principle, every harness component encodes an assumption about what the model can't do — and those assumptions go stale as models improve or the codebase evolves.

Check for:

- **Module AGENTS.md inflation**: modules with their own AGENTS.md that now have <10 source files (threshold dropped below the creation criteria)
- **Redundant docs**: `docs/ARCHITECTURE.md` that essentially duplicates what's already in the README
- **Over-specified patterns**: Key Patterns in AGENTS.md that describe things any decent model would infer from the code (e.g., "use camelCase for variables" in a TypeScript project)
- **Empty structure**: directories like `docs/references/` or `docs/exec-plans/completed/` that contain only `.gitkeep` after months of use — are they still needed?

Flag these as "complexity reduction candidates" — suggestions, not auto-fixes.

---

## Phase 3 — Triage and Remediation

Classify every finding from Phases 1 and 2 by risk level. Then apply fixes in order of confidence.

Read `references/auto-fix-rules.md` for the complete list of what can be safely auto-fixed.

### Severity classification

Each finding gets a severity based on two axes:

**Impact** — how much damage does this drift cause to agent accuracy?

| Level    | Description                                                                     |
| -------- | ------------------------------------------------------------------------------- |
| Critical | Agent will make materially wrong decisions (wrong build commands, deleted APIs) |
| High     | Agent will be confused or misled (broken links, stale architecture)             |
| Medium   | Agent may waste time (outdated patterns, missing index entries)                 |
| Low      | Cosmetic or informational (stale dates, trivial naming)                         |

**Certainty** — how confident are we that this is actually drift?

| Level  | Description                                                              |
| ------ | ------------------------------------------------------------------------ |
| Proven | Mechanically verified (file doesn't exist, command not found)            |
| High   | Strong evidence from code search (imports don't match, path renamed)     |
| Medium | Inferential evidence (pattern seems outdated, module looks consolidated) |
| Low    | Suspicion only (semantic claim is hard to verify)                        |

### Remediation tiers

#### Tier 1: Auto-fix (apply immediately)

Apply only when Impact ≤ Medium AND Certainty = Proven:

- Broken cross-links where the target was renamed (and the new path is unambiguous)
- Missing manifest entries for artifacts that exist
- Orphaned manifest entries for artifacts that don't exist
- Update Last Verified dates in the manifest for artifacts that pass all checks
- Move completed execution plans from `active/` to `completed/`
- Add missing entries to PLANS.md for plans that exist in the filesystem
- Fix trivial path renames in AGENTS.md when the new path is unambiguous (single candidate)

After applying auto-fixes, re-run `python3 scripts/check_harness.py` to verify the fixes didn't introduce new issues.

#### Tier 2: Propose fix (present for confirmation)

Apply when Certainty ≥ High but Impact = High or the fix requires content rewriting:

- New modules needing AGENTS.md — draft the content, present for review
- Architecture doc sections describing deleted or reorganized modules — draft updated sections
- OBSERVABILITY.md commands that need updating — propose the corrected commands
- Module AGENTS.md that should be deleted (orphaned module) — propose deletion

For each proposed fix, include:

1. **What**: the specific change
2. **Why**: the evidence that it's drift
3. **Risk**: what could go wrong if the fix is wrong

#### Tier 3: Flag for human (report only)

Apply when Certainty ≤ Medium OR Impact = Critical:

- Semantic contradictions between docs and code that require domain knowledge to resolve
- Architectural changes not reflected in docs where the correct new documentation is unclear
- Key Patterns that may be outdated but require design judgment to update
- Harness complexity reduction candidates
- Any finding where the correct fix is ambiguous

For each flag, include:

1. **What**: the specific concern
2. **Evidence**: what triggered the finding
3. **Suggestion**: a starting point for resolution (not a prescription)

### Commit strategy

- Auto-fixes: commit in a single atomic commit with message `chore(harness): garden audit auto-fixes`
- Proposed fixes, if accepted: commit in a separate commit with message `docs(harness): garden audit remediation`
- Do not commit flagged items — they require human decisions first

---

## Phase 4 — Garden Report

Produce a structured report that summarizes the audit. Read `references/garden-report-template.md` for the complete format.

### Report structure

```
=== Harness Garden Report ===

Repository: <repo name>
Audit date: <today>
Previous audit: <last manifest verification date, or "first audit">

## Health Score

Control plane health: <X>% (<N> of <M> artifacts current)
Checked: <number of checks performed>
Auto-fixed: <number of auto-fixes applied>
Proposed fixes: <number of proposed fixes>
Flagged for human: <number of flags>

## Auto-fixes Applied

<For each auto-fix:>
- [path] <description of fix>  (evidence: <brief evidence>)

## Proposed Fixes

<For each proposed fix:>
### <title>
- What: <description>
- Why: <evidence>
- Risk: <what could go wrong>
- Proposed change: <diff or description>

## Flagged for Human Review

<For each flag:>
### <title>
- Concern: <description>
- Evidence: <what triggered this>
- Suggestion: <starting point>

## Manifest Update

Updated Last Verified dates for all passing artifacts.
<List of artifacts with updated dates>

## Complexity Audit

<If any complexity reduction candidates were found:>
- <description of candidate and recommendation>

## Next Audit

Recommended next garden audit: <date, based on freshness thresholds>
```

### Health score calculation

The health score measures what percentage of the control plane is current and accurate:

```
health_score = (passing_checks / total_checks) * 100
```

Where:

- Each manifest artifact existence check = 1 check
- Each cross-link verification = 1 check
- Each semantic accuracy check (command exists, path exists, module listed) = 1 check
- A check "passes" if no drift was found OR drift was auto-fixed

### Post-report actions

After generating the report:

1. Update `docs/generated/harness-manifest.md` — set Last Verified to today's date for all artifacts that passed or were auto-fixed
2. Commit the manifest update along with any auto-fixes
3. If proposed fixes were accepted by the user, commit those separately
4. Print the health score and summary to the user

---

## Idempotency — Re-running garden

Garden audits are safe to re-run at any time. The behavior:

- **No drift found**: manifest dates are refreshed, health score is 100%, report confirms health
- **Drift found**: same findings will be reported each time until fixed
- **After fixes**: re-running immediately should show improved health score and no regression
- **Auto-fixes are idempotent**: applying the same auto-fix twice has no additional effect

---

## Critical design constraints

These rules protect the repo from well-intentioned but harmful automation.

1. **Never modify unmanaged docs.** README, CONTRIBUTING, team-maintained docs — report on them if they contain broken links to harness artifacts, but never edit them.

2. **Auto-fixes must be mechanically certain.** If there's any ambiguity about the correct fix, it's a proposed fix or a flag, not an auto-fix. The threshold for auto-fix is: a script could do it deterministically.

3. **Semantic drift detection uses code search, not guessing.** To verify "the auth module uses JWT tokens", search for JWT-related imports or code in the auth module. Do not guess based on the module name.

4. **Preserve git history.** Garden changes are atomic commits with clear messages. Never force-push, rebase, or squash garden commits into unrelated work.

5. **The manifest is the source of truth for what the harness manages.** If a file isn't in the manifest, the garden doesn't audit its content (only notes it as potentially untracked).

6. **Don't fix what you can't verify.** If you can't determine whether a semantic claim is still accurate, flag it — don't rewrite it based on inference.

7. **Log everything.** Every finding, every auto-fix, every skip — the garden report is the audit trail. Another agent or human should be able to reconstruct exactly what happened.

8. **Freshness refresh is not content validation.** Updating the Last Verified date means the artifact was checked and found accurate (or fixed). Do not refresh dates for artifacts you couldn't fully verify.

---

## Adapting to repo context

| Repo state                     | Garden behavior                                                   |
| ------------------------------ | ----------------------------------------------------------------- |
| Freshly bootstrapped (<7 days) | Light audit: manifest check + cross-links only                    |
| Active development             | Full audit with emphasis on semantic drift in ARCHITECTURE/AGENTS |
| Post-major-refactor            | Deep audit: expect high drift, prioritize module-level accuracy   |
| Stable / maintenance mode      | Focus on staleness and complexity reduction                       |
| Monorepo with many modules     | Audit module boundaries carefully; look for new/deleted modules   |

---

## Reference index

| File                                   | When to read                                       |
| -------------------------------------- | -------------------------------------------------- |
| `references/drift-taxonomy.md`         | Phase 2: understanding all drift types             |
| `references/auto-fix-rules.md`         | Phase 3: determining what can be safely auto-fixed |
| `references/garden-report-template.md` | Phase 4: generating the final report               |
| `references/freshness-thresholds.md`   | Deciding staleness thresholds by artifact type     |
