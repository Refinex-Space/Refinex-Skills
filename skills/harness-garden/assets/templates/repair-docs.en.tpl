@@ AGENTS.md
<!-- HARNESS:MANAGED FILE -->
# ${PROJECT_NAME}

${PROJECT_SUMMARY}

## Start Here

1. Read this file first
2. Then read [Plans](docs/PLANS.md)
3. Route into the focused docs by task type
4. Read the closest local `AGENTS.md` before editing code

## Task Routing

| Task | Read first | Then |
| --- | --- | --- |
| Architecture / boundaries | `ARCHITECTURE.md` | `docs/DESIGN.md` |
| Planning / progress | `docs/PLANS.md` | `docs/exec-plans/active/` |
| Security / permissions | `docs/SECURITY.md` | related code and constraints |
| Reliability / rollback | `docs/RELIABILITY.md` | runtime docs and implementation |
| Observability / runtime debugging | `docs/OBSERVABILITY.md` | `docs/generated/` |
| Quality / evaluation | `docs/QUALITY_SCORE.md` | `docs/generated/` |
${EXTRA_ROUTES}

## Ground Rules

- `AGENTS.md` is a routing map, not an encyclopedia
- Keep the root route short, current, and mechanically checkable
- Use progressive disclosure: root map -> focused docs -> local `AGENTS.md` -> source code
- Active work belongs in `docs/exec-plans/active/`
- Completed work belongs in `docs/exec-plans/completed/`
- Structural debt belongs in `docs/exec-plans/tech-debt-tracker.md`
- Structured facts and indexes must remain checkable and current

## Local AGENTS Coverage

${LOCAL_AGENT_HINTS}

## Mechanical Entry Points

- Repo check: `python3 scripts/check_harness.py`
- Harness manifest: `docs/generated/harness-manifest.md`
@@ AGENTS.md.extra.frontend
| Frontend / UX / product behavior | `docs/FRONTEND.md` | `docs/PRODUCT_SENSE.md` |
@@ AGENTS.md.extra.design
| Design evolution / multi-module coordination | `docs/DESIGN.md` | `docs/design-docs/index.md` |
@@ ARCHITECTURE.md
<!-- HARNESS:MANAGED FILE -->
# ${PROJECT_NAME} Architecture

## Purpose

Define the stable system boundaries, dependency flow, and interfaces
that should not drift casually.

## Architecture Invariants

- Parse data at boundaries before passing it inward
- Avoid dependency flow reversal
- Turn high-risk constraints into checks, scripts, or generated facts
- Sync docs, plans, and generated facts when public behavior changes

## Current Structure Summary

${STRUCTURE_SUMMARY}

## Stable Boundaries

- directory boundaries for workspaces and services
- documentation boundaries between root `AGENTS.md` and `docs/`
- execution-plan boundaries under `docs/exec-plans/`
- generated-fact boundaries under `docs/generated/`
@@ docs/README.md
<!-- HARNESS:MANAGED FILE -->
# Docs

This directory is the repository knowledge system used by agents through
progressive disclosure.

## Recommended Read Path

1. root `AGENTS.md`
2. `docs/PLANS.md`
3. focused domain docs
4. the closest local `AGENTS.md`

## Contents

- `PLANS.md`: high-level plan entry point
- `SECURITY.md`: security baseline
- `RELIABILITY.md`: reliability constraints and rollback posture
- `OBSERVABILITY.md`: logs, metrics, traces, and runtime debugging surfaces
- `QUALITY_SCORE.md`: evaluation rubric
- `exec-plans/`: active and completed execution plans
- `exec-plans/tech-debt-tracker.md`: tracked entropy and deferred structural work
- `generated/`: generated facts
- `references/`: stable references
${DOCS_EXTRA_INDEX}
@@ docs/README.md.extra.frontend
- `FRONTEND.md`: frontend boundaries and quality expectations
- `PRODUCT_SENSE.md`: product tradeoff rules
- `product-specs/`: behavior and acceptance references
@@ docs/README.md.extra.design
- `DESIGN.md`: cross-module design constraints
- `design-docs/`: long-lived design decisions and beliefs
@@ docs/PLANS.md
<!-- HARNESS:MANAGED FILE -->
# Development Plans

> Read this file before starting work so the current active plan and
> priority are known.

## Current State

- **Active plan**: `${ACTIVE_PLAN_PATH}`
- **Harness status**: maintained via `scripts/check_harness.py`
- **Structural debt**: `docs/exec-plans/tech-debt-tracker.md`

## Active Plan Entry Point

- [${ACTIVE_PLAN_LABEL}](${ACTIVE_PLAN_PATH})

## Rules

1. New work should create or reuse an active plan under `docs/exec-plans/active/`
2. Completed plans move to `docs/exec-plans/completed/`
3. Structural debt and deferred cleanup belong in `docs/exec-plans/tech-debt-tracker.md`
4. `PLANS.md` stays short and points to detailed execution plans
@@ docs/SECURITY.md
<!-- HARNESS:MANAGED FILE -->
# Security Baseline

## Purpose

Encode the minimum security expectations so agents do not erode
important boundaries while moving quickly.

## Baseline

- never commit plaintext secrets
- validate inputs at boundaries
- constrain high-risk external operations explicitly
- sync docs and validation when security-sensitive behavior changes

## Review Priority

1. secrets and credentials
2. permission boundaries
3. input validation
4. logging and sensitive data exposure
@@ docs/RELIABILITY.md
<!-- HARNESS:MANAGED FILE -->
# Reliability

## Purpose

Define the default reliability expectations, rollback awareness, and
failure-management posture for this repository.

## Defaults

- key paths should have a validation strategy
- failures should leave diagnosable evidence
- changes should have a rollback thought process and bounded blast radius
- execution plans should record risk and validation evidence
- runtime visibility requirements should be kept in `docs/OBSERVABILITY.md`
@@ docs/OBSERVABILITY.md
<!-- HARNESS:MANAGED FILE -->
# Observability

## Purpose

Make runtime behavior legible to future agents instead of relying on
tribal knowledge.

## Required Surfaces

- relevant logs and error evidence
- important metrics or timing signals
- traces or request-flow breadcrumbs when available
- browser or end-to-end verification surfaces for UI work when supported

## Defaults

- prefer scriptable inspection over manual narration
- keep commands, dashboards, and debugging entry points discoverable
- when isolated worktrees or per-task environments exist, document how to use them
- record recurring blind spots in `docs/exec-plans/tech-debt-tracker.md`
@@ docs/QUALITY_SCORE.md
<!-- HARNESS:MANAGED FILE -->
# Quality Score

## Purpose

Turn quality into a structured rubric that evaluators and maintainers
can reuse.

## Review Order

1. Security
2. Correctness
3. Performance
4. Readability

## Harness Quality Dimensions

- route clarity
- document indexability
- plan lifecycle integrity
- generated-fact freshness
- runtime legibility and verification evidence
- local `AGENTS.md` coverage at real boundaries
@@ docs/FRONTEND.md
<!-- HARNESS:MANAGED FILE -->
# Frontend Guide

## Purpose

Provide focused routing and constraints for frontend and UI work.

## Focus Areas

- component and state boundaries
- experience consistency
- accessibility and performance
- respecting service and backend boundaries
- runtime verification through browser or end-to-end checks when available

## Suggested Next Reads

- `docs/PRODUCT_SENSE.md`
- `docs/product-specs/index.md`
- `docs/OBSERVABILITY.md`
@@ docs/PRODUCT_SENSE.md
<!-- HARNESS:MANAGED FILE -->
# Product Sense

## Purpose

Capture product judgment rules so feature work does not drift into local
optimizations with weak user value.

## Defaults

- make the main path usable before broadening scope
- improve verifiability before adding complexity
- connect new capability to clear user value and acceptance criteria
@@ docs/product-specs/index.md
<!-- HARNESS:MANAGED FILE -->
# Product Specs Index

Add concrete product behavior specs and acceptance references here.

## Suggested Content

- core user journeys
- critical state flows
- failure and edge conditions
- non-functional requirements
@@ docs/DESIGN.md
<!-- HARNESS:MANAGED FILE -->
# Design Guide

## Purpose

Capture cross-module design constraints and shared decisions so separate
parts of the repo evolve coherently.

## Applies To

- multi-module coordination
- interface changes
- responsibility shifts
- long-lived design consensus
@@ docs/design-docs/index.md
<!-- HARNESS:MANAGED FILE -->
# Design Docs Index

Index the long-lived design decisions and deeper architecture notes
here.

## Suggested Entries

- `core-beliefs.md`
- major boundary decisions
- important technology choices and tradeoffs
@@ docs/design-docs/core-beliefs.md
<!-- HARNESS:MANAGED FILE -->
# Core Beliefs

Record engineering beliefs that should not change every time one feature
is implemented.

## Examples

- preserve clear boundaries first
- encode lessons into the system, not memory
- keep plans and indexes resumable for the next agent
@@ docs/exec-plans/tech-debt-tracker.md
<!-- HARNESS:MANAGED FILE -->
# Tech Debt Tracker

Track recurring harness drift, deferred structural cleanup, and
instrumentation gaps here.

## Suggested Fields

- debt item
- impact or risk
- current workaround
- preferred fix
- owner or next checkpoint
@@ docs/exec-plans/completed/README.md
<!-- HARNESS:MANAGED FILE -->
# Completed Plans

> Archive completed execution plans here.

## Archive Header

Add this block to the top of completed plans:

```markdown
> ✅ Completed: YYYY-MM-DD
> Summary: <one-line summary>
> Duration: <actual duration>
> Key learnings: <important learning>
```
@@ docs/generated/README.md
<!-- HARNESS:MANAGED FILE -->
# Generated Facts

This directory stores mechanical facts maintained by scripts.

## Default Generated Files

- `harness-manifest.md`: current harness coverage and entry points
- future generated facts such as schema snapshots, route maps, or inventories
@@ docs/references/index.md
<!-- HARNESS:MANAGED FILE -->
# References Index

Use this directory for stable references that agents will need
repeatedly.

## Good Fits

- runbooks
- domain glossaries
- integration notes
- repetitive debugging commands
