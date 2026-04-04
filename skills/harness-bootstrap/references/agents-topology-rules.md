# AGENTS Topology Rules

Use these rules when deciding where to place `AGENTS.md` files.

## Root `AGENTS.md`

Responsibilities:

- Explain how to start
- Route by task type
- State minimal hard rules
- Point to plans, indexes, and generated facts

Do not turn the root file into a full handbook.

## Local `AGENTS.md`

Responsibilities:

- Describe the role of that subtree
- State local constraints and commands
- Point to the next docs or code boundaries

Local files should assume the reader has already seen the root
`AGENTS.md`.

## Placement Heuristics

Prefer local `AGENTS.md` at:

- workspace boundaries
- app/service boundaries
- shared library boundaries
- backend/frontend split boundaries

Avoid placing them in:

- shallow folders with no distinct policy
- data-only folders
- directories that would only repeat the parent file

## Progressive Disclosure

The expected path is:

1. Root `AGENTS.md`
2. Task-specific docs under `docs/`
3. Closest local `AGENTS.md`
4. Code and generated facts

If a file would break this path by duplicating large amounts of detail,
trim it and move detail into `docs/`.
