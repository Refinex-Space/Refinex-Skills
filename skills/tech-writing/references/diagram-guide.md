# Diagram Guide

Use diagrams only for load-bearing explanation. A diagram should make one relationship obvious faster than prose.

## When a Diagram Is Required

Draw a diagram when the Anchor Sheet promises one, or when the article explains:

- call chains or execution lifecycles;
- data flow across components;
- state transitions;
- failure propagation;
- topology or ownership boundaries;
- timing windows, retry loops, or consistency gaps;
- technology comparison across decision axes.

Use the `mermaid-diagrams` skill to author Mermaid. Treat the visual plan as binding input.

## Diagram Type Selection

- `flowchart`: component relationships, data flow, decision flow, ownership boundaries.
- `sequenceDiagram`: request lifecycle, async interaction, retry path, transaction/message coordination.
- `stateDiagram-v2`: lock states, job states, order states, circuit breaker states.
- `timeline`: API evolution, migration phases, incident chronology.
- `classDiagram`: type relationships only when source-level structure matters.
- `erDiagram`: storage schema or domain entity relationships.

## Diagram Quality Rules

- One diagram answers one reader question.
- Prefer 6-10 nodes. Split before making a poster.
- Labels should be short and domain-specific.
- The prose must explain what the reader should notice in the diagram.
- Do not use diagrams as decoration.

## Visual Plan Format

In the Anchor Sheet, describe each diagram like this:

```markdown
- 图 1: sequenceDiagram，回答 "锁过期后业务为什么仍会继续执行？"，展示 client、Redis、business operation、TTL window。
- 图 2: flowchart LR，回答 "RocketMQ 事务消息减少了哪些应用层补偿？"，展示 local transaction、half message、checkback、commit/rollback。
```
