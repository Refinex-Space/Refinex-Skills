# Learning ramp guide

This file exists to stop one specific failure: building a conceptually correct series that still feels brutal to read.

A technical series is not only a dependency graph. It is also a learning slope. Readers do not experience "correct order" abstractly; they experience friction, confidence, confusion, and payoff.

## Core rule

For every series, design an explicit reader ladder:

- what the reader knows at the start
- what the reader can do after the first usable phase
- what the reader can do after the middle phases
- what the reader can reason about after the deep phases

If the planner cannot name these four states, the sequence is probably concept-first and reader-blind.

## Prefer use-first when the topic is a framework

Framework series should usually begin with:

1. what the thing is for
2. how versions match
3. how to start a minimal project
4. what the core terms mean
5. one runnable path that works
6. the first best-practice path that avoids obvious mistakes

Only after this should the series escalate into mechanism, internals, tradeoffs, or design philosophy.

This is not anti-theory. It is correct placement of theory.

## Three common ramp shapes

### Shape 1 — Use, then explain

Best for frameworks, SDKs, application platforms.

Typical flow:

- positioning and terminology
- Hello World / first runnable path
- the recommended happy path
- common mistakes and their fixes
- internals and design rationale
- production and tradeoffs

### Shape 2 — Feel the pain, then explain

Best for systems where the core insight only lands after a concrete surprise.

Typical flow:

- a small broken or confusing example
- the minimal fix
- the hidden rule that explains the fix
- deeper mechanism
- advanced implications

### Shape 3 — Decision, then depth

Best for adoption or architecture series.

Typical flow:

- what problem this technology solves
- when not to use it
- minimal successful adoption path
- the internal model needed to avoid misuse
- long-term tradeoffs and architecture consequences

## Beginner-to-mid rule

If the series claims to serve beginners or junior engineers, it must contain a genuine beginner-to-mid path, not just a short glossary before advanced material.

A genuine beginner-to-mid path includes:

- a first success experience
- a recommended default workflow
- a basic but complete mental map of the area
- explicit boundaries on what is not yet being taught
- a bridge from usage to internals

Without that bridge, the series creates knowledge holes that get larger with each later article.

## The bridge article

Many strong series need at least one bridge article between "I can use it" and "I understand how it works".

A bridge article usually does one of these:

- explains why the recommended default works
- maps user-facing API to internal abstractions at a high level
- shows one common failure and traces it to a hidden rule

This is often the article that makes the later deep-dive phase feel earned rather than abrupt.

## Depth placement test

Before placing a deep mechanism article early, ask:

1. Has the reader used the thing once?
2. Has the reader seen the recommended default path?
3. Has the reader learned the basic vocabulary?
4. Has the reader felt at least one practical question that the deep dive will answer?

If two or more answers are no, the deep dive is probably too early.

## Benefit-writing discipline

For each phase, write this sentence:

`After this phase, the reader can ...`

Good:

- `After this phase, the reader can bootstrap a correct Spring AI project and know which abstractions they are actually touching.`
- `After this phase, the reader can build a basic RAG pipeline without confusing embedding, indexing, and retrieval.`
- `After this phase, the reader can explain why streaming + tool calling breaks this extension point.`

Bad:

- `After this phase, the reader knows more about Spring AI.`

If the sentence is weak, the phase is weak.
