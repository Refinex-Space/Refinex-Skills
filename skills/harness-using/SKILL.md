---
name: harness-using
description: >-
  Use when starting any repository-work conversation that may involve Harness
  Engineering routing, control plane setup, drift repair, feature delivery, bug
  fixing, or completion verification. Invoke before clarifying questions or
  code changes whenever there is any reasonable chance a Harness skill applies.
  Especially relevant for prompts such as `初始化 Harness`, `控制面坏了`,
  `文档漂移了`, `做这个功能`, `修复这个 bug`, `排查回归`, or `确认现在能不能宣称完成`.
license: Proprietary. LICENSE.txt has complete terms
---

# harness-using

Route repository work into the correct Harness Engineering skill before doing anything else. This skill is the entry discipline for the Harness family: it decides which skill should take control, in what order, and when direct action is forbidden.

This is a **low-freedom** skill. Its job is routing and guardrails, not implementation.

**Announce at start:** `I'm using harness-using to route this repository task.`

---

## Instruction priority

Apply instructions in this order:

1. **User and repo instructions** (`AGENTS.md`, direct user constraints, local policies)
2. **Harness skills**
3. **Default system behavior**

If the repo says "don't create new plans" or "don't touch docs/", follow the repo. Harness does not override explicit repository or user constraints.

---

## The routing rule

Before any substantive reply, exploration, or code change, ask:

1. Does this task belong to the Harness family at all?
2. If yes, which Harness skill owns the primary workflow?
3. Is there a prerequisite Harness skill that must run first?
4. Will `harness-verify` be required before any success claim?

If the answer to (1) is "maybe", inspect the routing table below before acting.

---

## Primary routing table

| Situation | Primary skill | Why |
| --- | --- | --- |
| Repo has no control plane or the control plane is obviously incomplete | `harness-bootstrap` | Build the baseline before any repo-scale work |
| Control plane exists but may be stale, broken, or misleading | `harness-garden` | Restore truth before trusting docs |
| Need to deliver a feature, enhancement, or structured refactor | `harness-feat` | Feature work belongs inside execution plans |
| Need to diagnose a bug, regression, flaky path, or incident | `harness-fix` | Fix work requires reproduction and root cause discipline |
| About to claim "done", "fixed", "passing", or "ready" | `harness-verify` | Completion claims require fresh evidence |

`harness-verify` is **cross-cutting**. It does not replace the primary workflow; it gates completion inside that workflow.

---

## Sequencing rules

Use these combinations when multiple conditions apply:

1. **Missing control plane + any other work**
   - Run `harness-bootstrap` first.
   - Then route to `harness-feat` or `harness-fix`.

2. **Suspected drift + feature or fix work**
   - Run `harness-garden` first unless the user explicitly wants diagnosis on the broken state.
   - Then continue with `harness-feat` or `harness-fix`.

3. **Feature or fix work nearing completion**
   - Keep the primary workflow in control.
   - Apply `harness-verify` before declaring success.

4. **User asks for a general explanation of the suite**
   - Explain the family briefly.
   - Route to a concrete skill only when the task becomes operational.

---

## Direct-action bans

Do **not** jump straight into implementation when:

- the repo has no Harness baseline
- the docs may be lying
- the task is clearly a bug fix without reproduction evidence
- the task is clearly a feature request without a plan
- you are about to claim success without fresh verification evidence

These are routing failures, not productivity wins.

---

## Process before domain

When both process skills and domain skills could apply:

1. Route through the appropriate Harness skill first
2. Then bring in domain skills for implementation details

Example:

- "Implement Stripe subscription retry flow" -> `harness-feat` first, then Stripe-specific guidance
- "Fix flaky PDF export" -> `harness-fix` first, then PDF-specific guidance
- "Build a landing page, redesign onboarding, or create an admin dashboard" -> `harness-feat` first, then `harness-frontend`, then `harness-verify`

---

## Red flags

If you catch yourself thinking any of these, stop and route correctly:

- "I'll inspect the repo first and decide later"
- "This is probably just a small fix"
- "I can answer the question before checking workflow ownership"
- "The user only wants a quick status update"
- "I'll declare it done after this one command"
- "The docs look mostly right, good enough"

Each of these thoughts is how control planes get bypassed.

---

## Ambiguity discipline

Routing is where silent bad assumptions start. Before choosing a workflow:

- If multiple interpretations route to different workflows, do not pick silently.
- State the competing interpretations and the evidence for each.
- If one unresolved assumption could change ownership, ask a targeted clarification before handing off.
- If a simpler interpretation avoids unnecessary process overhead, say so explicitly.

The routing step is allowed to be brief, but it is not allowed to be vague.

---

## Output contract

When this skill triggers:

1. State which Harness skill will own the task
2. State any prerequisite skill that must run first
3. State whether `harness-verify` will be required at the end
4. State any material assumptions that are still unresolved, or ask the blocking clarification
5. Hand off immediately to the owning workflow

Do not linger in routing mode once ownership is clear.
