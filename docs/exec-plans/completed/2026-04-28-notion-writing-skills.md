# Notion Writing Skills

**Goal:** Create Notion-native versions of the write suite's three core writing workflows and document how to configure and use them in Notion.

**Scope:**
- Create a `notion/` directory with copy-pasteable Notion Skill pages for planning, writing, and rewriting.
- Add optional Notion Agent Instructions that make the three Skills work consistently as a workspace writing system.
- Add `docs/reference/notion/` documentation describing official Notion Skill support, configuration, usage, and the relationship to the existing `tech-planner`, `tech-writing`, and `tech-rewrite` skills.
- Add content tests that guard the Notion artifacts against drifting into Codex-only `SKILL.md` assumptions.
- Update public documentation indexes where needed.

**Non-scope:**
- Do not create or modify a live Notion workspace page through the Notion connector.
- Do not replace the existing Codex `skills/tech-*` implementations.
- Do not introduce a Codex plugin or marketplace entry for the Notion pages.

**Constraints and source rules:**
- Official Notion guidance is the source of truth for Notion-specific behavior: Skills are on-demand Notion pages, Instructions are persistent defaults, and Custom Agents are autonomous/background agents with their own instructions and connections.
- Notion Skill pages should stay concise enough to be operational in Notion. Long rationale belongs in repository docs or linked references, not in the skill trigger surface.
- The three Notion Skills must preserve the existing write suite's core defenses: source exhaustion plus knowledge graph for planning, Anchor Sheet before blank-page drafting, and Fact Register before rewriting.
- Repository preflight is degraded: the repo currently has `docs/PLANS.md` but no root `AGENTS.md`, `docs/OBSERVABILITY.md`, or root-level `scripts/check_harness.py`. Baseline verification uses `tests/run-all.sh`.

## Acceptance Criteria

- [ ] `notion/skills/` contains exactly three writing Skill page templates: `tech-planner.md`, `tech-writing.md`, and `tech-rewrite.md`.
- [ ] `notion/instructions/writing-agent.md` defines optional persistent Notion Agent instructions and clearly separates always-on rules from on-demand Skills.
- [ ] `notion/README.md` explains the local Notion artifact layout and how to import the pages into Notion.
- [ ] `docs/reference/notion/README.md` documents Notion Skill support, configuration steps, usage prompts, sharing/permission expectations, and three writing workflows.
- [ ] Public indexes mention the Notion writing artifacts without implying they are Codex `SKILL.md` skills.
- [ ] Content tests verify the three expected Notion Skill pages, their required workflow gates, and official Notion terminology.
- [ ] `tests/run-all.sh` passes after the change.

## Implementation Steps

- [x] **Step 1: Research existing and official sources**
  - Read `skills/tech-planner/SKILL.md`, `skills/tech-writing/SKILL.md`, `skills/tech-rewrite/SKILL.md`, and the most relevant reference templates.
  - Read Notion's official Skill and Instructions help pages.
  - Verify the Context7 Notion Help source for setup/configuration facts.
  - Verification: local notes in this plan and subsequent artifacts reflect the official distinction between Skills, Instructions, and Custom Agents.

- [x] **Step 2: Create Notion artifact directory**
  - Create `notion/README.md`.
  - Create `notion/skills/tech-planner.md`, `notion/skills/tech-writing.md`, and `notion/skills/tech-rewrite.md`.
  - Create `notion/instructions/writing-agent.md`.
  - Verification: files exist and use Notion-native language rather than Codex frontmatter.

- [x] **Step 3: Write reference documentation**
  - Create `docs/reference/notion/README.md`.
  - Cover official behavior, configuration, import flow, usage examples, and the three writing Skills.
  - Include first-use prompts that prove the setup in Notion.
  - Verification: doc mentions official Notion source URLs and the three local artifact paths.

- [x] **Step 4: Update indexes**
  - Update root README files and write suite docs to point to the Notion reference.
  - Keep wording clear that Notion pages are companion artifacts, not native Codex skills.
  - Verification: links are present in English and Chinese indexes.

- [x] **Step 5: Add content tests**
  - Add a focused content test for `notion/` and `docs/reference/notion/`.
  - Validate expected files, Notion official terminology, workflow gates, and first-use prompts.
  - Verification: `python3 -m unittest tests.content.test_notion_writing_skills -v` passes.

- [x] **Step 6: Final verification and archive plan**
  - Run `tests/run-all.sh`.
  - Update this plan with verification evidence.
  - Move this plan to `docs/exec-plans/completed/` and update `docs/PLANS.md`.
  - Verification: completed plan records commands, results, and residual risks.

## Risk Notes

- **Notion docs can change:** cite the official URLs and avoid overfitting to UI labels where possible.
- **Skill vs Instruction confusion:** keep all always-on preferences in `notion/instructions/` and task-specific workflows in `notion/skills/`.
- **Overlong Skill pages:** keep Notion page templates operational and push deep rationale into docs.

## Verification Evidence

- Baseline `tests/run-all.sh`: exit 0; 26 tests passed; live tests skipped because `HARNESS_RUN_LIVE` is not set.
- New focused test `python3 -m unittest tests.content.test_notion_writing_skills -v`: exit 0; 6 tests passed.
- Final `tests/run-all.sh`: exit 0; 32 tests passed; live tests skipped because `HARNESS_RUN_LIVE` is not set.

## Completion Notes

- Created Notion-native writing artifacts under `notion/` for planning, blank-page writing, and rewriting.
- Added optional always-on Notion Agent Instructions while keeping task-specific workflows in Skill pages.
- Added `docs/reference/notion/README.md` with official Notion setup, usage, sharing, and smoke-test guidance.
- Updated repository indexes and write suite docs to expose the Notion companion artifacts.
- Added content tests to prevent Notion pages from drifting into Codex-only `SKILL.md` conventions.
