# Prompt Optimization Rubric

Use this rubric before creating or updating any execution plan. The goal
is to convert a rough request into a brief that is easier to execute
without widening scope.

## Rewrite Rules

1. Preserve user intent. Do not silently change the outcome.
2. Remove accidental implementation bias unless the repository or the
   user explicitly requires it.
3. Separate must-haves from optional ideas and follow-ups.
4. Add repository-derived constraints that are clearly relevant.
5. Make assumptions explicit and keep them minimal.
6. Define validation early so "done" is testable.
7. Split multi-task prompts into one primary task and explicit follow-up
   items when necessary.

## Optimized Task Brief Template

Use this structure in your notes, plan, or opening status update:

- **Outcome**: What should exist or behave differently when the task is done?
- **Problem**: What user, product, or engineering problem is being solved?
- **Scope**: What is included in this task?
- **Non-goals**: What should not be expanded in this task?
- **Constraints**: Architecture, security, schema, workflow, or product invariants.
- **Affected surfaces**: Files, modules, commands, docs, or runtime paths likely to change.
- **Validation**: Tests, manual flows, benchmarks, or review criteria.
- **Doc sync**: Which planning or design artifacts must be updated?
- **Harness preflight**: Which harness surfaces must be checked first?
- **Open assumptions**: Only the assumptions you cannot avoid.

## Scope-Control Heuristics

- If the user asks for a feature and a cleanup, keep the feature as the
  main task and demote cleanup unless it is required.
- If the user suggests a library or design pattern, keep it only if it
  fits higher-authority repository constraints.
- If the prompt is very short, infer from the repository before asking.
- If the prompt contains unstable external facts, verify them from
  primary sources before turning them into plan requirements.

## Short Example

Raw request:

`任务：给 provider 设置页加一个健康检查视图。`

Optimized brief:

- **Outcome**: The settings UI exposes a provider health view with clear
  status and failure reasons.
- **Problem**: Users cannot tell whether the current provider config is
  valid without a full request failure.
- **Scope**: Settings UI, command boundary, provider health query path,
  relevant docs.
- **Non-goals**: Full observability dashboard, historical analytics,
  background polling unless already required by current architecture.
- **Constraints**: Keep frontend behind Tauri commands; use Rust for
  provider/network work; do not bypass Keychain conventions.
- **Validation**: Unit/integration coverage for the health command and a
  manual UI verification path.
