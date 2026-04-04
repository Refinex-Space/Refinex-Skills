# Bug Brief Rubric

Use this rubric before creating or updating any fix plan. The goal is to
convert a vague bug report into a repair target that can be reproduced,
reasoned about, and verified.

## Rewrite Rules

1. Preserve the reported symptom exactly.
2. Distinguish observed behavior from the user's suspected cause.
3. Prefer evidence over interpretation.
4. State expected behavior explicitly.
5. Identify the narrowest likely failing surface before expanding scope.
6. Define what evidence would count as a real fix.
7. Call out missing evidence instead of pretending certainty.

## Optimized Bug Brief Template

Use this structure in your notes, plan, or opening status update:

- **Symptom**: What is broken?
- **Expected behavior**: What should happen instead?
- **Observed behavior**: What actually happens now?
- **Impact**: Who or what is affected?
- **Reproduction**: Steps, command, fixture, or log evidence.
- **Likely surfaces**: Files, modules, runtime boundaries, or recent changes.
- **Hypotheses**: Ranked possible causes with confidence levels.
- **Validation**: What check would prove the issue is fixed?
- **Doc sync**: Which planning or technical artifacts must be updated?
- **Harness preflight**: Which harness surfaces must be checked first?

## Investigation Heuristics

- Prefer making one failing check obvious before exploring multiple fix directions.
- If the bug cannot be reproduced, collect logs, stack traces, recent
  diffs, and invariant violations before changing code.
- If the user's diagnosis conflicts with the code or logs, keep the
  symptom report but revise the cause hypothesis.
- If a mitigation is necessary before root cause is proven, label it as
  a mitigation and record the residual risk.

## Short Example

Raw request:

`这个 provider 切换后聊天一直卡在 loading，帮我修。`

Optimized bug brief:

- **Symptom**: After switching providers, the chat UI remains in loading state.
- **Expected behavior**: The chat request should either stream normally
  or fail with a visible error.
- **Observed behavior**: The loading indicator persists without stream
  progress or terminal error.
- **Impact**: Provider switching makes the chat feature unreliable.
- **Reproduction**: Switch providers in settings, open a session, send a
  message, observe no completion event.
- **Likely surfaces**: Provider selection state, Tauri command boundary,
  stream completion handling, session-level config overrides.
- **Validation**: Reproduction flow completes with either successful
  response or explicit error; targeted tests cover the completion path.
