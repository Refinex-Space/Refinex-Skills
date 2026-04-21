# Mermaid final checklist

Run this before returning Mermaid to the user or to another skill.

## Gate 1 — The question is singular

- [ ] The diagram answers one reader question.
- [ ] If a second question remains, it was moved to a second diagram or to prose.

## Gate 2 — The type is correct

- [ ] `sequenceDiagram` for temporal actor flow
- [ ] `flowchart` for branching or pipeline logic
- [ ] `stateDiagram-v2` for state transitions
- [ ] `classDiagram` for static relationships
- [ ] `erDiagram` for entity/cardinality shape
- [ ] `timeline` for ordered change over time

## Gate 3 — The syntax is portable

- [ ] No unnecessary renderer-specific features
- [ ] Risky labels are quoted
- [ ] `end` is quoted if used as label text
- [ ] Comments do not imitate directive syntax
- [ ] Subgraphs are shallow and justified

## Gate 4 — The layout is clean

- [ ] Node or actor count stays within a human-scannable range
- [ ] Labels are short
- [ ] The chosen direction matches the reading motion
- [ ] The diagram is not doing two jobs at once

## Gate 5 — Styling is restrained

- [ ] The diagram is already readable without custom styling
- [ ] Any color use has semantic purpose
- [ ] Styling is sparse and consistent

## Gate 6 — The prose contract is preserved

- [ ] The diagram supports a specific argument in the surrounding text
- [ ] The diagram can be pasted into Markdown without cleanup
- [ ] The reader can tell what to notice in the diagram
