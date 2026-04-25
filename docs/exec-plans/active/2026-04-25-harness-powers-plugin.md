# Harness Powers Plugin Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `harness-execute` semantics to implement this plan task by task. Use `harness-dispatch` only for independent subtasks with disjoint write scopes. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first productized `Harness Powers` Codex App plugin under `plugins/harness-powers/`, integrating Superpowers workflow strengths into the Harness Engineering control model without publishing overlapping legacy skill names.

**Architecture:** The plugin is a self-contained distribution with its own `.codex-plugin/plugin.json`, README, assets, skill directories, references, and plugin-specific tests. Existing root `skills/harness-*` files are treated as source material for migration, while the installed Superpowers cache is read-only source material. Public skill ownership is unified under `harness-*`.

**Tech Stack:** Markdown skills, Codex App plugin metadata JSON, shell-based test runner, Python `unittest` content checks.

**Design Source:** `docs/exec-plans/specs/2026-04-25-harness-powers-plugin-design.md`

---

## Scope

Create and validate:

- `plugins/harness-powers/.codex-plugin/plugin.json`
- `plugins/harness-powers/README.md`
- `plugins/harness-powers/LICENSE`
- `plugins/harness-powers/assets/`
- `plugins/harness-powers/skills/`
- `plugins/harness-powers/tests/` if useful for plugin-local fixtures
- repository tests that validate plugin structure and content rules

Update:

- `docs/PLANS.md`
- this active execution plan as evidence is gathered
- root test suite wiring if new tests require it

Do not:

- modify `/Users/refinex/.codex/plugins/cache/openai-curated/superpowers`
- remove root `skills/` harness skills
- publish legacy Superpowers skill directories inside the new plugin
- implement a marketplace publishing workflow in this pass

## Acceptance Criteria

- `plugins/harness-powers/.codex-plugin/plugin.json` exists and points `skills` to `./skills/`.
- The plugin publishes exactly the approved first-pass `harness-*` skill surface.
- Legacy Superpowers skill directories are not present under `plugins/harness-powers/skills/`.
- Public plugin skills do not use `docs/superpowers/specs` or `docs/superpowers/plans` as default paths.
- `harness-using` is the sole global entry router.
- `harness-verify` is the sole success-claim evidence gate.
- TDD material is available through `harness-feat` references.
- Systematic debugging material is available through `harness-fix` references.
- Review request and review feedback handling are unified in `harness-review`.
- Subagent and parallel dispatch guidance are unified in `harness-dispatch`.
- `plugins/harness-powers/README.md` describes lifecycle, skill inventory, and relationship to Superpowers.
- `tests/run-all.sh` passes.

## Risk Notes

- The largest risk is mechanical concatenation that makes skills too long and hard to follow. Keep each `SKILL.md` focused on ownership, gates, and process; move deep technique material into `references/`.
- The second risk is accidental old-name drift. Add tests that fail if legacy skill directories are published or old default paths remain.
- The third risk is ambiguity between `harness-feat`, `harness-plan`, and `harness-execute`. Preserve ownership language from the design: lifecycle owner, plan generator, and plan progress owner.

---

## Task 1: Add Plugin Scaffold

**Files:**

- Create: `plugins/harness-powers/.codex-plugin/plugin.json`
- Create: `plugins/harness-powers/README.md`
- Create: `plugins/harness-powers/LICENSE`
- Create: `plugins/harness-powers/assets/harness-powers-small.svg`
- Copy or create: `plugins/harness-powers/assets/app-icon.png`

- [ ] **Step 1: Create plugin directory and metadata**

Create `plugin.json` with:

- `name`: `harness-powers`
- `version`: `0.1.0`
- `description`: Harness Engineering control plane plus planning, debugging, review, dispatch, and verification workflows.
- `skills`: `./skills/`
- interface display name: `Harness Powers`
- category: `Coding`
- capabilities: `Interactive`, `Read`, `Write`
- composer icon path: `./assets/harness-powers-small.svg`
- logo path: `./assets/app-icon.png`

- [ ] **Step 2: Add first README shell**

Create a concise README with:

- what Harness Powers is
- relationship to Superpowers
- relationship to the existing Harness suite
- first-pass skill inventory
- lifecycle overview
- installation note for local plugin use

- [ ] **Step 3: Add license and simple assets**

Use the repository's existing license posture where applicable. For the SVG, create a simple deterministic icon that does not reuse Superpowers branding as the final brand mark.

- [ ] **Step 4: Verify scaffold**

Run:

```bash
test -f plugins/harness-powers/.codex-plugin/plugin.json
test -d plugins/harness-powers/assets
python3 -m json.tool plugins/harness-powers/.codex-plugin/plugin.json >/dev/null
```

Expected: all commands exit 0.

---

## Task 2: Add Plugin Structure Tests First

**Files:**

- Create: `tests/content/test_harness_powers_plugin.py`

- [ ] **Step 1: Write failing tests for plugin metadata and skill inventory**

Add Python `unittest` coverage for:

- `plugin.json` exists and parses as JSON
- `plugin.json["name"] == "harness-powers"`
- `plugin.json["skills"] == "./skills/"`
- expected public skill directories exist
- each expected skill has `SKILL.md`
- no legacy Superpowers skill directory exists under the plugin

Expected public skill directories:

```python
EXPECTED_SKILLS = {
    "harness-using",
    "harness-brainstorm",
    "harness-plan",
    "harness-execute",
    "harness-bootstrap",
    "harness-garden",
    "harness-feat",
    "harness-fix",
    "harness-verify",
    "harness-review",
    "harness-dispatch",
    "harness-worktree",
    "harness-finish",
    "harness-frontend",
}
```

Legacy directory denylist:

```python
LEGACY_SKILLS = {
    "using-superpowers",
    "brainstorming",
    "writing-plans",
    "executing-plans",
    "test-driven-development",
    "systematic-debugging",
    "verification-before-completion",
    "requesting-code-review",
    "receiving-code-review",
    "subagent-driven-development",
    "dispatching-parallel-agents",
    "using-git-worktrees",
    "finishing-a-development-branch",
}
```

- [ ] **Step 2: Write failing tests for frontmatter consistency**

For every expected skill, parse the `---` frontmatter block and assert:

- `name: <directory-name>` appears
- `description:` appears

- [ ] **Step 3: Write failing tests for forbidden default paths**

Assert no plugin `SKILL.md` contains:

- `docs/superpowers/specs`
- `docs/superpowers/plans`

- [ ] **Step 4: Run tests and confirm they fail before implementation**

Run:

```bash
python3 -m unittest tests.content.test_harness_powers_plugin -v
```

Expected: failure because the plugin skills have not been created yet.

---

## Task 3: Migrate Existing Harness Skills Into Plugin

**Files:**

- Create directory tree under: `plugins/harness-powers/skills/`
- Copy/adapt from: `skills/harness-bootstrap/`
- Copy/adapt from: `skills/harness-garden/`
- Copy/adapt from: `skills/harness-feat/`
- Copy/adapt from: `skills/harness-fix/`
- Copy/adapt from: `skills/harness-using/`
- Copy/adapt from: `skills/harness-verify/`
- Copy/adapt from: `skills/harness-frontend/`

- [ ] **Step 1: Copy current Harness-owned skill directories**

Copy the seven existing Harness skill directories into the plugin:

- `harness-bootstrap`
- `harness-garden`
- `harness-feat`
- `harness-fix`
- `harness-using`
- `harness-verify`
- `harness-frontend`

- [ ] **Step 2: Preserve references and scripts**

Ensure each copied skill keeps its `references/` and `scripts/` subdirectories when present.

- [ ] **Step 3: Adjust plugin-local frontmatter only where needed**

Keep names unchanged. Descriptions may mention Harness Powers when it improves routing clarity, but do not rewrite content heavily in this task.

- [ ] **Step 4: Verify copied skill frontmatter**

Run:

```bash
python3 -m unittest tests.content.test_harness_powers_plugin -v
```

Expected: tests still fail because new Superpowers-derived `harness-*` skills are not present, but copied Harness skills pass frontmatter checks.

---

## Task 4: Create harness-brainstorm, harness-plan, and harness-execute

**Files:**

- Create: `plugins/harness-powers/skills/harness-brainstorm/SKILL.md`
- Create: `plugins/harness-powers/skills/harness-brainstorm/references/spec-reviewer-prompt.md`
- Create: `plugins/harness-powers/skills/harness-plan/SKILL.md`
- Create: `plugins/harness-powers/skills/harness-plan/references/plan-reviewer-prompt.md`
- Create: `plugins/harness-powers/skills/harness-execute/SKILL.md`

- [ ] **Step 1: Adapt brainstorming into harness-brainstorm**

Use Superpowers `brainstorming` as source material, then change:

- frontmatter name to `harness-brainstorm`
- design output path to `docs/exec-plans/specs/`
- terminal handoff to `harness-plan`
- repository exploration to prefer `AGENTS.md`, `docs/ARCHITECTURE.md`, and `docs/PLANS.md`
- implementation bans to mention Harness Powers flow

- [ ] **Step 2: Adapt writing-plans into harness-plan**

Use Superpowers `writing-plans` as source material, then change:

- frontmatter name to `harness-plan`
- plan output path to `docs/exec-plans/active/`
- index update to `docs/PLANS.md`
- handoff to `harness-execute`
- plan style to decision-complete and audit-oriented
- remove requirement that every step inline full implementation code

- [ ] **Step 3: Adapt executing-plans into harness-execute**

Use Superpowers `executing-plans` as source material, then change:

- frontmatter name to `harness-execute`
- required plan source to `docs/exec-plans/active/`
- checkpoint ownership to active plan checkboxes/evidence
- delegated work handoff to `harness-dispatch`
- completion handoff to `harness-verify` and then `harness-finish`

- [ ] **Step 4: Move reviewer prompts into references**

Move and rename:

- Superpowers `brainstorming/spec-document-reviewer-prompt.md` to `harness-brainstorm/references/spec-reviewer-prompt.md`
- Superpowers `writing-plans/plan-document-reviewer-prompt.md` to `harness-plan/references/plan-reviewer-prompt.md`

- [ ] **Step 5: Verify three core skills**

Run:

```bash
python3 -m unittest tests.content.test_harness_powers_plugin -v
```

Expected: metadata, frontmatter, and missing-core-skill checks pass. Tests may still fail for remaining new skills.

---

## Task 5: Merge Entry And Verification Gates

**Files:**

- Modify: `plugins/harness-powers/skills/harness-using/SKILL.md`
- Modify: `plugins/harness-powers/skills/harness-verify/SKILL.md`

- [ ] **Step 1: Merge using-superpowers discipline into harness-using**

Add concise sections covering:

- skill check before substantive work
- user and repo instructions above Harness rules
- process skills before domain skills
- routing for `harness-brainstorm`, `harness-plan`, `harness-execute`, `harness-review`, `harness-dispatch`, `harness-worktree`, and `harness-finish`
- direct-action bans for unclear ownership

- [ ] **Step 2: Merge verification-before-completion into harness-verify**

Ensure `harness-verify` covers:

- no completion claim without fresh evidence
- claim / command / result / conclusion format
- claim-evidence alignment
- workflow-specific minimum evidence
- red flags for unsupported success language

- [ ] **Step 3: Verify no legacy entry or exit skill is published**

Run:

```bash
python3 -m unittest tests.content.test_harness_powers_plugin -v
```

Expected: tests for absence of `using-superpowers` and `verification-before-completion` pass.

---

## Task 6: Create harness-review

**Files:**

- Create: `plugins/harness-powers/skills/harness-review/SKILL.md`
- Create: `plugins/harness-powers/skills/harness-review/references/code-reviewer-prompt.md`

- [ ] **Step 1: Merge review request workflow**

Adapt Superpowers `requesting-code-review` into sections for:

- reviewing current diff
- reviewing active plan output
- reviewing PRs
- findings-first output
- severity ordering

- [ ] **Step 2: Merge review feedback workflow**

Adapt Superpowers `receiving-code-review` into sections for:

- read feedback completely
- restate or clarify requirements
- verify against codebase reality
- implement, reject, or escalate with evidence
- handle multiple items in priority order

- [ ] **Step 3: Apply Harness review priorities**

Make the priority order explicit:

```text
security > correctness > performance > readability
```

- [ ] **Step 4: Add completion handoff**

Require `harness-verify` after review fixes before any success claim.

- [ ] **Step 5: Verify review skill**

Run:

```bash
python3 -m unittest tests.content.test_harness_powers_plugin -v
```

Expected: `harness-review` exists, frontmatter is valid, and legacy review skill directories remain absent.

---

## Task 7: Create harness-dispatch

**Files:**

- Create: `plugins/harness-powers/skills/harness-dispatch/SKILL.md`
- Create: `plugins/harness-powers/skills/harness-dispatch/references/implementer-prompt.md`
- Create: `plugins/harness-powers/skills/harness-dispatch/references/spec-reviewer-prompt.md`
- Create: `plugins/harness-powers/skills/harness-dispatch/references/code-quality-reviewer-prompt.md`

- [ ] **Step 1: Merge subagent-driven development workflow**

Adapt Superpowers `subagent-driven-development` into:

- fresh subagent per task
- primary agent keeps plan ownership
- implementer scope boundaries
- spec compliance review
- code quality review

- [ ] **Step 2: Merge parallel dispatch workflow**

Adapt Superpowers `dispatching-parallel-agents` into:

- independent domain detection
- one worker per independent domain
- no shared write scope unless explicitly coordinated
- integration review after workers return

- [ ] **Step 3: Define worker output contract**

Require workers to report:

- changed files
- verification commands and results
- residual risks
- any plan deviations

- [ ] **Step 4: Verify dispatch skill**

Run:

```bash
python3 -m unittest tests.content.test_harness_powers_plugin -v
```

Expected: `harness-dispatch` exists, frontmatter is valid, and legacy dispatch skill directories remain absent.

---

## Task 8: Create harness-worktree And harness-finish

**Files:**

- Create: `plugins/harness-powers/skills/harness-worktree/SKILL.md`
- Create: `plugins/harness-powers/skills/harness-finish/SKILL.md`

- [ ] **Step 1: Adapt worktree workflow**

Adapt Superpowers `using-git-worktrees` into `harness-worktree` with:

- `.worktrees/` then `worktrees/` then explicit user preference
- ignored-directory verification
- `codex/` branch prefix by default
- setup and baseline commands where detectable
- warning against plan execution on `main` or `master` without explicit permission

- [ ] **Step 2: Adapt finishing workflow**

Adapt Superpowers `finishing-a-development-branch` into `harness-finish` with:

- mandatory `harness-verify` before finish options
- four options: local merge, push PR, keep branch, discard
- explicit confirmation before discard
- plan archival and `docs/PLANS.md` update
- PR body references to plan and verification evidence

- [ ] **Step 3: Verify worktree and finish skills**

Run:

```bash
python3 -m unittest tests.content.test_harness_powers_plugin -v
```

Expected: `harness-worktree` and `harness-finish` exist, frontmatter is valid, and legacy worktree/finish directories remain absent.

---

## Task 9: Internalize TDD And Systematic Debugging

**Files:**

- Modify: `plugins/harness-powers/skills/harness-feat/SKILL.md`
- Create: `plugins/harness-powers/skills/harness-feat/references/tdd-discipline.md`
- Create or update: `plugins/harness-powers/skills/harness-feat/references/testing-anti-patterns.md`
- Modify: `plugins/harness-powers/skills/harness-fix/SKILL.md`
- Create: `plugins/harness-powers/skills/harness-fix/references/systematic-debugging.md`
- Create or update: `plugins/harness-powers/skills/harness-fix/references/root-cause-techniques.md`

- [ ] **Step 1: Move TDD material into harness-feat references**

Use Superpowers `test-driven-development` and its testing anti-patterns reference as source material. Preserve:

- RED/GREEN/REFACTOR
- failing test before production behavior changes
- watch the test fail
- minimal implementation
- refactor while green
- testing anti-patterns

- [ ] **Step 2: Reference TDD from harness-feat**

Keep the main `SKILL.md` concise:

- feature workflow remains preflight -> plan -> implement -> verify -> archive
- TDD applies when behavior changes
- non-TDD work needs equivalent verification
- details live in `references/tdd-discipline.md`

- [ ] **Step 3: Move systematic debugging material into harness-fix references**

Use Superpowers `systematic-debugging` and related references as source material. Preserve:

- reproduce consistently
- read errors carefully
- falsifiable hypotheses
- one variable per experiment
- root cause before fix
- condition-based waiting where relevant
- defense in depth where relevant

- [ ] **Step 4: Reference debugging from harness-fix**

Keep the main `SKILL.md` concise:

- bug workflow remains preflight -> brief -> reproduce -> isolate -> fix -> regression -> archive
- root cause claim requires evidence
- three failed fix attempts means stop and replan
- details live in `references/systematic-debugging.md`

- [ ] **Step 5: Verify TDD and debugging are internalized**

Run:

```bash
python3 -m unittest tests.content.test_harness_powers_plugin -v
```

Expected: plugin contains no `test-driven-development` or `systematic-debugging` skill directories, but TDD and debugging reference content exists under Harness-owned skills.

---

## Task 10: Update harness-bootstrap, harness-garden, and harness-frontend For Plugin Awareness

**Files:**

- Modify: `plugins/harness-powers/skills/harness-bootstrap/SKILL.md`
- Modify: `plugins/harness-powers/skills/harness-garden/SKILL.md`
- Modify: `plugins/harness-powers/skills/harness-frontend/SKILL.md`

- [ ] **Step 1: Update harness-bootstrap**

Add Harness Powers awareness:

- control plane docs should route design/specs to `docs/exec-plans/specs/`
- execution plan docs should use active/completed layout
- generated guidance should mention `harness-using` and `harness-verify`

- [ ] **Step 2: Update harness-garden**

Add drift checks for:

- `docs/exec-plans/specs/`
- active plans
- completed plans
- `docs/PLANS.md` links
- stale references to old Superpowers default paths

- [ ] **Step 3: Update harness-frontend**

Clarify repository mode:

- frontend work must run under `harness-brainstorm`, `harness-feat`, or `harness-fix`
- frontend owns visual thesis and rule packs
- verification and plan ownership remain Harness lifecycle responsibilities

- [ ] **Step 4: Verify plugin-aware Harness skills**

Run:

```bash
python3 -m unittest tests.content.test_harness_powers_plugin -v
```

Expected: structure tests pass and content tests for plugin-aware routing pass.

---

## Task 11: Complete README And Add Content Drift Tests

**Files:**

- Modify: `plugins/harness-powers/README.md`
- Modify: `tests/content/test_harness_powers_plugin.py`

- [ ] **Step 1: Finalize README**

README must include:

- plugin purpose
- relationship to Superpowers
- relationship to Harness Engineering
- skill table
- lifecycle diagrams as text
- non-published legacy skill list
- local development and validation commands

- [ ] **Step 2: Add README inventory test**

Test that every expected public skill appears in the README.

- [ ] **Step 3: Add content ownership tests**

Add tests that assert:

- `harness-using` mentions `harness-brainstorm`, `harness-plan`, `harness-execute`, `harness-review`, and `harness-verify`
- `harness-verify` contains the claim / command / result / conclusion contract
- `harness-review` contains security > correctness > performance > readability
- `harness-dispatch` contains changed files, verification, and residual risks
- `harness-feat` references TDD discipline
- `harness-fix` references systematic debugging

- [ ] **Step 4: Run plugin tests**

Run:

```bash
python3 -m unittest tests.content.test_harness_powers_plugin -v
```

Expected: all plugin content tests pass.

---

## Task 12: Final Verification And Plan Archival

**Files:**

- Modify: `docs/exec-plans/active/2026-04-25-harness-powers-plugin.md`
- Modify: `docs/PLANS.md`
- Move when complete: `docs/exec-plans/active/2026-04-25-harness-powers-plugin.md` to `docs/exec-plans/completed/2026-04-25-harness-powers-plugin.md`

- [ ] **Step 1: Run full repository tests**

Run:

```bash
tests/run-all.sh
```

Expected: all non-live tests pass; live tests may skip when `HARNESS_RUN_LIVE` is unset.

- [ ] **Step 2: Run targeted plugin inspections**

Run:

```bash
python3 -m unittest tests.content.test_harness_powers_plugin -v
rg -n "docs/superpowers/(specs|plans)" plugins/harness-powers/skills && exit 1 || true
find plugins/harness-powers/skills -maxdepth 1 -type d | sort
```

Expected:

- unittest exits 0
- forbidden path grep exits with no matches
- skill directory list contains only approved `harness-*` public skills plus the parent directory

- [ ] **Step 3: Update evidence log in this plan**

Record:

- command
- result
- conclusion
- residual risks

- [ ] **Step 4: Archive plan**

Move the plan to completed:

```bash
mv docs/exec-plans/active/2026-04-25-harness-powers-plugin.md docs/exec-plans/completed/2026-04-25-harness-powers-plugin.md
```

Update `docs/PLANS.md`:

- remove from Active Plans
- add under Completed Plans with completion date

- [ ] **Step 5: Final commit**

Stage and commit the implementation:

```bash
git add plugins/harness-powers tests/content/test_harness_powers_plugin.py docs/PLANS.md docs/exec-plans
git commit -m "feat: 新增 Harness Powers 插件"
```

Expected: commit succeeds after verification evidence has been recorded.

---

## Evidence Log

No implementation evidence yet. This plan is ready for execution after review.
