# Commit Conventions

Commit messages within a harnessed workflow serve two audiences: humans reading
git log, and agents reconstructing what happened from the commit history. Every
commit must be traceable back to a plan step.

---

## Message format

```
<type>(<scope>): <short description>

refs plan: <plan-filename> step <N>

<optional body — explain WHY, not WHAT>
```

### Type prefixes

| Type       | When to use                                                    |
| ---------- | -------------------------------------------------------------- |
| `feat`     | New functionality visible to users or consumers                |
| `fix`      | Bug fix                                                        |
| `refactor` | Code change that neither fixes a bug nor adds a feature        |
| `test`     | Adding or updating tests only                                  |
| `docs`     | Documentation changes (including AGENTS.md, ARCHITECTURE.md)   |
| `chore`    | Maintenance tasks (dependency updates, config changes)         |
| `plan`     | Creating or updating an execution plan                         |

### Scope

The scope is the module or area affected. Use the directory name or a short
identifier:

```
feat(api): add user endpoint
fix(auth): correct token expiration check
refactor(db): extract connection pooling
plan(harness): add execution plan for user-endpoint
docs(harness): update control plane after user-endpoint
```

### Plan reference

Every code commit includes a `refs plan:` line in the body, linking it to the
execution plan step it implements:

```
feat(api): add GET /users endpoint

refs plan: 2024-01-15-user-endpoint.md step 3

Implements the users list endpoint using the shared pagination
pattern from the orders module.
```

This makes it possible to:
- Trace any commit back to WHY it was made
- Reconstruct the implementation sequence from git log
- Identify orphan commits (no plan reference = unplanned change)

---

## Special commit types

### Plan creation commit

```
plan(harness): add execution plan for <short-description>
```

No `refs plan:` line — this IS the plan.

### Plan archival commit

```
chore(harness): archive execution plan for <short-description>
```

### Control plane update commit

```
docs(harness): update control plane after <short-description>
```

### Rollback commit

```
revert(<scope>): revert step <N> — <reason>

refs plan: <plan-filename> step <N>
reverted due to: <explanation>
```

---

## Commit granularity

| Principle                                  | Example                                       |
| ------------------------------------------ | --------------------------------------------- |
| One commit per plan step                   | Step 3 → one commit                           |
| Plan changes committed separately          | Plan update → separate commit from code        |
| Control plane updates committed separately | AGENTS.md update → separate commit from code   |
| Tests can be with or separate from code    | Prefer together when they're for the same step |

### What NOT to do

- **Mega-commit**: all changes in one commit ("implement feature X")
- **WIP commits**: "wip", "save progress", "temp" — every commit should be meaningful
- **Mixed concerns**: code changes + plan changes + control plane updates in one commit

---

## Reading commit history

When an agent needs to understand what happened in a previous task, it can:

```bash
git log --oneline --grep="refs plan:"
```

This shows all plan-linked commits. To see commits for a specific plan:

```bash
git log --oneline --grep="refs plan: 2024-01-15-user-endpoint.md"
```

This traceability is why the `refs plan:` line matters — it makes the git history
a navigable record of harnessed work.
