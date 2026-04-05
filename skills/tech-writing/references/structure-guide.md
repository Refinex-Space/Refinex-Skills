# Structure Guide: Document Type Templates

Load the relevant section for the document type you are producing. Each template specifies
the mandatory sections, their purpose, and the questions each section must answer.

---

## Template 1: Technical Deep-Dive / Analysis Blog Post

**When to use:** A long-form article explaining how a technology works, when to use it,
or what happens internally. The reader wants depth, not a tutorial.

**Mandatory structure:**

```
[Title — encodes the argument]
[Header block: type, date, scope, prerequisites, reading time, central argument]

## Opening (1–2 paragraphs)
  Purpose: State the tension and the verdict.
  Must answer: What problem are we solving? What will the reader believe after reading?

## [Problem / Context Section]
  Purpose: Establish why this is non-trivial. Not background — the specific difficulty.
  Must answer: What assumption causes engineers to get this wrong?

## [Mechanism Section(s)]
  Purpose: Explain how it actually works, at the level needed to predict behavior.
  Must answer: What happens internally? What is the sequence? Where are the failure points?
  Required: At least one diagram with an explanatory note.

## [Decision / Recommendation Section]
  Purpose: Apply the mechanism understanding to a real choice.
  Must answer: Given the mechanism, what should the reader do? Under what conditions?
  Required: A decision table with a Verdict column.

## Failure Modes and Production Risks
  Purpose: What breaks, how it manifests, how to recover.
  Must answer: What does this look like in logs/metrics? What is the default misconfiguration?

## Known Limitations / When This Doesn't Apply
  Purpose: Bound the recommendation. Every recommendation has a scope.
  Must answer: For what constraints, scale, or context does this advice break down?

## What to Read Next
  Purpose: Give the reader a directed learning path.
  Must answer: What is the logical next step? Why that topic specifically?
```

---

## Template 2: Architecture Decision Record (ADR)

**When to use:** Documenting a specific architectural decision, its context, and the
reasoning behind it. The audience is future engineers who will inherit this decision.

**Mandatory structure:**

```
# ADR-[N]: [Decision title — use a verb phrase]
Status: [Proposed / Accepted / Deprecated / Superseded by ADR-N]
Date: [YYYY-MM-DD]
Deciders: [names or roles]

## Context
  What is the problem this decision addresses?
  What constraints or forces are in play?
  What happens if no decision is made?
  (2–4 paragraphs. This is the only background section permitted.)

## Decision
  State the decision in one sentence.
  Then explain the mechanism by which this decision addresses the context.
  (Not just "we chose X" — explain the causal chain.)

## Considered Alternatives
  For each alternative considered:
  - What it is (one sentence)
  - Why it was rejected (one sentence with a specific reason, not a vague concern)
  Required format: A table with columns [Alternative | Key Strength | Rejection Reason]

## Consequences
  Positive: what this decision enables or resolves.
  Negative: what this decision forecloses or makes harder. Be honest here.
  Risks: what could cause this decision to be wrong in the future (state the condition,
         not just "requirements may change").

## Implementation Notes (optional)
  Non-obvious implementation details the decision implies.
  Configuration values with rationale.
  Known gotchas.
```

---

## Template 3: Technology Comparison / Selection Guide

**When to use:** Comparing two or more technologies, frameworks, or approaches to help
the reader make a specific selection decision.

**Mandatory structure:**

```
[Title — must indicate the selection context, not just the options]
[Header block]

## Opening
  Name the specific scenario that makes this comparison necessary.
  State the winner upfront (or the decision framework if it's genuinely conditional).

## Evaluation Framework
  List the criteria used in this comparison. For each criterion, explain:
  - Why this criterion matters in the specific scenario
  - How it was assessed
  This section makes the comparison defensible and replicable.

## [Per-Criterion Analysis Sections]
  For each major criterion:
  - How each option performs on this criterion
  - The mechanism behind the difference (not just the surface behavior)
  - A mini-verdict: which option wins on this criterion and why
  Required: A table for each criterion showing the comparison.

## Decision Matrix
  Required: A single summary table covering all criteria with a Verdict column.
  The final row of the table should be "Overall Recommendation" with a clear winner.

## When to Choose Each Option
  Even if one option wins overall, the other option wins under some conditions.
  State those conditions precisely.

## Migration Considerations (if applicable)
  What does moving from one to the other require?
  What are the non-obvious migration traps?

## Failure Modes and Known Limitations (per option)
## What to Read Next
```

---

## Template 4: Module / Component Design Document

**When to use:** Documenting the design of a software module, service, or subsystem.
The audience is engineers who will implement it, extend it, or debug it.

**Mandatory structure:**

```
[Component Name — Design Document]
[Header block: version, status, scope, authors]

## Purpose and Scope
  What problem does this component solve?
  What is explicitly out of scope?
  What are the invariants this component must maintain under all conditions?

## Design Constraints
  What external constraints shaped this design?
  (Latency requirements, consistency model, upstream/downstream interface contracts)

## Architecture Overview
  Required: A component diagram showing this module's place in the system.
  Required: A sequence diagram for the primary use case with at least one failure branch.

## Key Design Decisions
  For each major decision embedded in the design:
  - The decision (one sentence)
  - The alternatives considered
  - The reason this approach was selected
  (Use ADR format for each sub-decision if complex)

## Interface Contract
  Public API: method signatures, semantics, error conditions, idempotency guarantees.
  Events emitted: schema, conditions, ordering guarantees.
  Dependencies: what this component requires from its dependencies, expressed as contracts.

## Failure Modes and Recovery
  For each failure mode:
  - Trigger condition
  - System behavior
  - Recovery path
  - Observable signal (metric, log pattern)

## Known Limitations and Future Work
  What does this design not solve? What is explicitly deferred?

## Runbook Notes (optional)
  Non-obvious operational characteristics.
  Common misconfiguration patterns.
  Diagnostic starting points.
```

---

## Template 5: API Reference Documentation

**When to use:** Reference documentation for an HTTP API, SDK, or library.
The reader is an implementer who needs to build against this interface.

**Principles for API docs:**
- State the semantics, not just the syntax. "This endpoint is idempotent" is more valuable
  than 50 words about the request schema.
- Document errors with the same depth as success cases. Engineers spend more time debugging
  errors than implementing happy paths.
- Show the non-obvious case. The obvious case is covered by the schema. The value is in
  showing the edge cases the schema allows but the implementation rejects.

**Per-endpoint structure:**

```
### [METHOD] /path/to/resource

[One sentence: what this endpoint does and its key semantic property]

**Request**
  Parameters: [table: name | type | required | description]
  Body schema: [annotated example, not just a schema table]
  Authentication: [what credentials, what scope]

**Response**
  Success: [status code + semantic meaning]
  Body: [annotated example]

**Errors**
  [Table: error code | condition | recovery action]
  Note: "recovery action" is mandatory. Do not document an error code without specifying
  what the caller should do when they encounter it.

**Behavior Notes**
  Idempotency: [yes/no + the key]
  Rate limits: [specific limits, not "subject to rate limiting"]
  Ordering guarantees: [if relevant]
  Non-obvious edge cases: [what the schema allows but you should not do]

**Example**
  Show the non-obvious use case, not the hello-world case.
  The hello-world case is obvious from the schema.
```