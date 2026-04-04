# Harness Principles

This reference distills the hard constraints that `harness-bootstrap`
must preserve when scaffolding or upgrading a repository.

## Source Grounding

- Local anchor:
  `http://refinex.cn/blog/harness-engineering-the-control-plane-for-agent-first-software`
- External primary references:
  - OpenAI: `Harness engineering: leveraging Codex in an agent-first world`
  - Anthropic: `Effective harnesses for long-running agents`
  - Anthropic: `Harness design for long-running application development`

## Non-Negotiable Rules

1. Root `AGENTS.md` is a routing map, not an encyclopedia.
2. Use progressive disclosure:
   root map -> focused docs -> local `AGENTS.md` -> source code.
3. Externalize continuity into versioned artifacts instead of relying on chat history.
4. Keep execution plans versioned, resumable, and discoverable from `docs/PLANS.md`.
5. Treat observability and runtime debugging as first-class harness surfaces.
6. Prefer structural checks, generated facts, and deterministic scripts over tribal memory.
7. Track recurring entropy in `docs/exec-plans/tech-debt-tracker.md`.
8. Low-risk drift may be auto-repaired; high-risk semantic drift must go through an active remediation plan.

## Bootstrap Defaults

- Preserve good existing content whenever safe.
- Create missing scaffolding deterministically.
- Install `docs/OBSERVABILITY.md` and a tech-debt tracker by default.
- Mark generated files so future repair can distinguish managed from unmanaged content.
- Infer documentation language from the repository when possible.
- Avoid CI/lint/workflow mutation by default; create check entrypoints and documented integration points instead.

## Long-Running Agent Implications

- The harness must support cross-session handoff through files, not memory.
- Active work should be recoverable from plans, manifests, and generated facts.
- Root docs should remain small enough that future agents can load them cheaply.
- Runtime tools, logs, browser verification, and other feedback surfaces should be discoverable from the repo.

## Generated File Policy

Generated bootstrap files should include a managed marker:

```markdown
<!-- HARNESS:MANAGED FILE -->
```

Generated repo check scripts should include a managed comment:

```python
# HARNESS:MANAGED FILE
```

`harness-garden` may safely rewrite managed files. Unmanaged files with
semantic drift should be escalated into an active remediation plan.
