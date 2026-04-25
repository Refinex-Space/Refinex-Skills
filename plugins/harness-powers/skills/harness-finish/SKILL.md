---
name: harness-finish
description: >-
  Use when Harness implementation work is complete and the agent must verify,
  archive the plan, update docs/PLANS.md, and offer exactly four finish options:
  local merge, push and PR, keep branch, or discard work. Requires `harness-verify`
  before presenting finish options and requires discard confirmation before any
  destructive cleanup.
license: MIT
---

# harness-finish

Complete a Harness implementation branch with evidence, plan bookkeeping, and a clear integration choice.

This is a **low-freedom** skill. Verification and user choice are mandatory.

**Announce at start:** `I'm using harness-finish to verify the work and present finish options.`

---

## Mandatory verification gate

Before presenting finish options, run `harness-verify`.

The verification evidence must include:

- the exact command or commands run
- exit codes or pass/fail results
- relevant test/check counts when available
- any residual warnings or known failures
- confirmation that the evidence matches the completion claim

If verification fails or does not prove the completion claim, stop and report the actual status. Do not offer merge, PR, keep, or discard options as a "finished" workflow until the verification gap is resolved.

---

## Plan archival and index update

Before merge or PR handoff, update Harness plan bookkeeping:

1. Mark the active plan complete with final verification evidence.
2. Move the completed plan from `docs/exec-plans/active/` to the repository's completed/archive plan location used by that project.
3. Update `docs/PLANS.md` so the plan status, archived path, branch, and verification evidence are current.
4. If the repository uses a generated Harness manifest or plan index, run the documented refresh command.

If no active plan exists, record that explicitly in the finish summary and PR body instead of inventing one.

---

## Determine branch context

Collect branch and base information:

```bash
git branch --show-current
git status --short
git worktree list
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

If the working tree has unrelated user changes, do not stage, revert, or discard them. Report the scope and ask before any operation that would affect them.

---

## Present exactly four options

After `harness-verify` passes and plan bookkeeping is ready, present exactly:

```text
Implementation verified. What would you like to do?

1. Merge back to <base-branch> locally
2. Push branch and create a Pull Request
3. Keep the branch/worktree as-is
4. Discard this work

Which option?
```

Do not add hidden defaults. Wait for the user's choice.

---

## Option 1: local merge

Use when the user chooses local merge. First identify where the base branch can be safely checked out:

```bash
git worktree list
git branch --show-current
```

If `<base-branch>` is already checked out in another worktree, run the merge from that base worktree instead of trying to check it out inside the feature worktree. Git normally rejects the same branch being checked out in two worktrees, and forcing around that guard risks operating in the wrong directory.

From the base worktree:

```bash
git pull --ff-only
git merge <feature-branch>
```

If no base worktree exists, create or switch to a clean base worktree first, then run the merge there. After merge, run the verification command again on the merged result. If it passes, remove only the completed feature branch and feature worktree when safe:

```bash
git worktree remove <worktree-path>
git branch -d <feature-branch>
```

If merged verification fails, stop and report the failure. Do not delete the branch or worktree.

---

## Option 2: push branch and create PR

Use when the user chooses PR handoff.

```bash
git push -u origin <feature-branch>
```

The PR body must reference the plan and verification evidence:

```markdown
## Summary
- <what changed>

## Plan
- Active/archived plan: <plan path or "No active plan">
- docs/PLANS.md updated: <yes/no plus reason>

## Verification
- `<command>`: <result>
- Residual risk: <risk or none known>
```

Keep the branch and worktree unless the user explicitly asks for cleanup after PR creation.

---

## Option 3: keep branch/worktree

Use when the user wants to continue later.

Report:

```text
Keeping branch <feature-branch>.
Worktree preserved at <worktree-path>.
Latest verification: <command and result>.
Plan status: <active or archived path>.
```

Do not remove the worktree or delete the branch.

---

## Option 4: discard work

Discard is destructive and requires confirmation.

Before deleting anything, show:

```text
This will permanently discard:
- Branch: <feature-branch>
- Worktree: <worktree-path>
- Commits not on <base-branch>: <short commit list>
- Plan/archive changes: <what will remain or be reverted>

Type "discard" to confirm.
```

Only proceed after the user types exactly `discard`.

Then remove the worktree and branch with the least destructive commands that work:

```bash
git worktree remove <worktree-path>
git branch -D <feature-branch>
```

Do not discard unrelated user changes.

---

## Red flags

Stop if you are about to:

- present finish options before running `harness-verify`
- merge, push, or create a PR without plan archival and `docs/PLANS.md` status updates when a plan exists
- create a PR body without plan and verification references
- discard work without exact typed confirmation
- delete a branch or worktree that contains unrelated user changes
- route users through legacy skill entry names
