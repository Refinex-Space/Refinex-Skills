# Diagram selection guide

Use diagrams to remove cognitive load, not to decorate the page. A diagram is required when the reader would otherwise have to simulate too many moving parts in working memory at once. A diagram is noise when the same point can be made more clearly in two or three precise sentences.

The discipline is simple: every diagram must answer one explicit question. Write that question down before choosing the diagram type. "What happens first, second, and third across these components?" is a real question. "Can I add a diagram here?" is not.

## The selection rule

Pick the diagram type from the question, not from habit.

- Use `sequenceDiagram` when the reader needs to understand **call order across actors over time**. Typical use cases: request lifecycle, interceptor chains, retry loops, tool-call round-trips, RPC choreography. If time order is the point, sequence beats flowchart.
- Use `flowchart` when the reader needs to understand **branching control flow, staged pipelines, or decision points**. Typical use cases: ingestion pipelines, request routing, validation branches, fallback logic. If "if/else", fan-out, or pipeline stages are the point, flowchart beats sequence.
- Use `stateDiagram-v2` when the reader needs to understand **state transitions**. Typical use cases: connection lifecycle, cache state, job status transitions, saga state machines. If the same object changes state over time, state diagrams beat flowcharts.
- Use `classDiagram` when the reader needs to understand **static type or component relationships**. Typical use cases: interface hierarchies, extension points, adapter layers, strategy objects. If the question is "what depends on what" in a static structure, class diagrams fit.
- Use `erDiagram` when the reader needs to understand **data entities and cardinality**. Typical use cases: schema design, persistence models, ownership boundaries, join shape. If the question is "how is the data shaped", ER beats class diagrams.
- Use `timeline` when the reader needs to understand **versioned change over time**. Typical use cases: API evolution, migration history, deprecation windows, incident chronology. If the reader must track what changed in which release or at what date, timeline fits.
- Use `mindmap` sparingly, only when the reader needs a **concept map** rather than a mechanism. This is usually for planner artifacts or overview sections, not for load-bearing mechanism explanation.

## Strong defaults for technical writing

If you are unsure, prefer these defaults:

- Mechanism with multiple actors and a temporal story: `sequenceDiagram`
- Branching logic or request pipeline: `flowchart`
- Stateful behavior or lifecycle bugs: `stateDiagram-v2`
- Source-level architecture or extension surface: `classDiagram`
- Schema or storage relationships: `erDiagram`
- Release and migration evolution: `timeline`

Do not default to `flowchart` for everything. That is the diagram equivalent of writing every article in the same voice.

## Diagram quality rules

Every diagram that survives into the draft obeys these rules:

- One diagram, one job. If a diagram is trying to show both call order and static ownership, split it.
- Labels are short, precise, and domain-true. Do not write sentence fragments in every node.
- The diagram is referenced in prose. The text tells the reader what to look at and why it matters.
- The diagram carries an argument. It is not a screenshot substitute and not a summary of the section heading.
- The diagram shows only the moving parts needed for the current claim. Extra boxes are a form of hand-waving.

## Failure patterns

Three failures are common.

The first is the **flowchart monoculture** failure. Every article gets a flowchart because flowcharts are familiar. The result is usually a vague diagram that hides time order, which is exactly what a sequence diagram would have clarified.

The second is the **decorative diagram** failure. The diagram restates the paragraph above it in boxes and arrows, adding no new clarity. If deleting the diagram would lose nothing, the diagram should not exist.

The third is the **kitchen-sink diagram** failure. The writer tries to explain the whole system in one picture. The reader learns less because the diagram is dense enough to require its own walkthrough. Split the diagram by question.

## Minimal process

Before drafting, write a short visual plan:

1. Name the mechanism, topology, lifecycle, or timeline that is hard to hold in prose alone.
2. Write the reader question the diagram must answer.
3. Choose the Mermaid type that matches the question.
4. State what the reader should be able to predict after reading the diagram.

If you cannot do these four steps, you are not ready to draw the diagram yet.
