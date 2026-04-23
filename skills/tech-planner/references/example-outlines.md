# Example outlines

This file contains worked examples of series outlines, paired so the difference between a weak outline and a strong outline on the same topic is visible side by side. The examples are not exhaustive — they cover three frameworks chosen because they are common subjects for technical blog series and because each one illustrates a distinct failure pattern that the strong version explicitly addresses.

The point of paired examples is that the difference between weak and strong is rarely obvious in isolation. A weak outline often looks reasonable when read by itself, because the failure patterns it embodies are the patterns that an inattentive reader would also miss. The pairing makes the failures visible by giving the reader something concrete to compare against. Reading both versions of each example, in order, is the fastest way to internalize what the quality checklist is actually checking for.

## Example 1 — Spring AI

### The weak outline

The weak version of a Spring AI series might look like this:

```
# Spring AI: A Comprehensive Guide

## Phase 1: Basics
- Article 1.1: Introduction to Spring AI
- Article 1.2: Setting Up Your First Spring AI Project
- Article 1.3: Understanding ChatClient
- Article 1.4: Working with Prompts

## Phase 2: Intermediate Topics
- Article 2.1: Embeddings and Vector Stores
- Article 2.2: Implementing RAG with Spring AI
- Article 2.3: Function Calling and Tool Use
- Article 2.4: Memory and Conversation State

## Phase 3: Advanced Topics
- Article 3.1: Custom Advisors
- Article 3.2: Multi-Model Orchestration
- Article 3.3: Production Deployment

## Phase 4: Conclusion
- Article 4.1: Spring AI Best Practices and Resources
```

This outline has a dozen failures from the quality checklist, and naming them is more useful than a vague critique.

The phase names "Basics", "Intermediate Topics", "Advanced Topics", "Conclusion" are difficulty labels rather than cognitive progressions. They tell the reader nothing about what each phase will do for them, and they fail Gate 3 of the quality checklist automatically. The structure of the phases also mirrors the official Spring AI documentation's table of contents almost exactly — Spring AI's docs have sections on ChatClient, Prompts, Embeddings, Vector Stores, RAG, Tools, Memory, and Advisors, in roughly the same order — which fails Gate 4 (structural divergence from official documentation).

The article titles are all topic tags. "Introduction to Spring AI" makes no claim. "Working with Prompts" makes no claim. "Understanding ChatClient" makes no claim. Every title fails Gate 2. A reader who saw only the titles would learn nothing about what the series argues, and the series itself is committed to nothing because none of the titles takes a position.

The phase transitions are unmotivated. Why does Phase 1 end where it does and Phase 2 begin where it does? The answer is "because the topics in Phase 2 are slightly harder than the topics in Phase 1", which is not a cognitive transition but a difficulty gradient. The structure now also fails the newer ramp checks, because it does not provide a real beginner-to-mid path.

The final article is a recap. "Spring AI Best Practices and Resources" delivers no cumulative payoff that depends on the earlier articles; it could have been written as the first article instead of the last, and nothing would change. The newer synthesis/payoff gate fails here too.

The outline does not visibly use the knowledge graph from Phase 2. No prerequisite dependencies are noted between articles. There is no acknowledgment that, for example, Article 2.2 (RAG) depends on both Article 2.1 (Embeddings and Vector Stores) and material from Phase 1, or that Article 2.3 (Function Calling) interacts with Article 3.1 (Custom Advisors) in important ways. The current checklist would fail this under Gate 6, because the prerequisite structure is invisible and the entry ramp is under-specified.

The weak outline is not the worst possible outline. Its phases are roughly in a sensible order, and it does cover most of the major Spring AI topics. But it would not produce a series that is meaningfully better than the official documentation, and the reader who followed the entire series would not have learned anything that they could not have learned by reading the docs themselves. The outline has done no useful planning work; it has simply reproduced the docs in a different layout.

### The strong outline

A strong version of the same series might look like this:

```
# Spring AI Beyond the Hello World — A Field Guide for Engineers Who Have
# Already Tried LangChain

## Series Overview
- Scope: Spring AI 1.0.0-RC1, focused on production usage in Java
  backend services
- Reader: Java backend engineer (3+ years), Spring Boot experience,
  has used OpenAI's REST API directly or via LangChain, has not used
  Spring AI in production
- Series voice: Design Tribunal (primary) with Mechanism Autopsy
  for the deep-dive articles
- Article count: 9 across 4 phases

## Phase 1 — Onboarding and Terms

This phase is for the reader who is approaching Spring AI with assumptions
imported from LangChain or from direct REST usage. By the end of the phase,
the reader will have replaced those assumptions with the actual Spring AI
mental model and will understand which problems Spring AI solves and which
it does not.

- Article 1.1: ChatClient is not an HTTP wrapper
- Article 1.2: Spring AI follows Spring's IoC rules, not LangChain's

## Phase 2 — Advisor Pipeline

This phase opens up the AdvisorChain and the surrounding mechanism. By
the end of the phase, the reader will understand how requests actually
flow through a Spring AI ChatClient invocation, which will give them the
mental model needed for the production decisions in Phase 3 and the
debugging in Phase 4.

- Article 2.1: AdvisorChain.around() runs once per call
- Article 2.2: Spring AI's Prompt is not LangChain's Prompt
- Article 2.3: The `ToolCallback` rename exposed a deeper API shift

## Phase 3 — Production Choices

This phase covers the decisions that are hardest to undo once the service
is in production. By the end of the phase, the reader will have a defensible
position on each of the load-bearing choices and will know what would have
to be true for them to revisit each decision.

- Article 3.1: ChatMemory leaks at the tool-call boundary
- Article 3.2: VectorStore choice depends on deployment shape

## Phase 4 — Diagnostics

This phase is the operational payoff. The reader who has finished phases
1-3 has the mental model to understand the failure modes covered here,
and the article in this phase delivers the cumulative insight that the
series has been building toward.

- Article 4.1: Streaming + tool calls break AdvisorChain assumptions
```

This outline differs from the weak version on every gate the checklist checks for. The phase names are concise and editorially natural, while the paragraphs under them carry the cognitive transition. The phases together form an arc that the reader can feel: start by replacing the wrong mental model, master the right one, use the mastery to make decisions, then use everything to diagnose production failures.

Every article title carries an argument. Article 1.1 argues that ChatClient is a state machine, not an HTTP wrapper. Article 2.1 argues that AdvisorChain.around() runs exactly once per call, with a specific consequence. Article 3.2 commits to a verdict on VectorStore choice for specific contexts. None of the titles is a topic tag; all of them are claims the article must defend.

The structure does not mirror the official Spring AI documentation. Spring AI's docs cover ChatClient, Prompts, Embeddings, Vector Stores, RAG, Tools, Memory, and Advisors as parallel sections in roughly that order. The strong outline organizes the same material around a cognitive arc — recalibration, mastery, decisions, diagnostics — that does not appear anywhere in the docs. A reader of the strong outline gets a different organization of the same material, which is the point of writing a series rather than just linking to the docs.

The final article is a cumulative payoff, not a recap. Article 4.1 explicitly requires the material from every earlier article and would be incomprehensible without them. A reader who skipped to Article 4.1 would not understand it; a reader who read the series in order would arrive at it with all the pieces in place. This is what the spiral curriculum looks like in practice.

The series has nine articles because it is a deliberately narrow production-usage slice, not because low article counts are inherently superior. For this scope, nine is enough. For a full-framework Spring AI series serving junior, intermediate, and senior readers, the planner should usually add an onboarding phase, split dense areas like embedding/vector store/RAG into separate articles, and add a late synthesis phase; totals above twenty are often justified. The right count follows scope and reader ladder, not a blanket preference for fewer articles.

## Example 2 — Project Reactor

### The weak outline

```
# Mastering Project Reactor

## Phase 1: Reactive Programming Fundamentals
- Article 1.1: What is Reactive Programming?
- Article 1.2: Introduction to Project Reactor
- Article 1.3: Understanding Mono and Flux
- Article 1.4: Basic Operators

## Phase 2: Advanced Operators
- Article 2.1: Combining Publishers
- Article 2.2: Error Handling
- Article 2.3: Backpressure
- Article 2.4: Schedulers and Threading

## Phase 3: Real World Applications
- Article 3.1: Using Reactor with Spring WebFlux
- Article 3.2: Testing Reactive Code
- Article 3.3: Performance and Best Practices
```

The weak Reactor outline has the same failure patterns as the weak Spring AI outline, but one failure deserves special attention. Article 1.4 ("Basic Operators") and Article 2.1 ("Combining Publishers") draw a distinction between "basic" and "advanced" operators that does not actually exist in Reactor. There are no "basic" operators and "advanced" operators; there are operators that transform values, operators that combine streams, operators that handle errors, operators that control timing, and operators that change schedulers. The "basic vs advanced" framing is a planning shortcut that ducks the work of actually understanding the operator categories, and a reader who finishes the series will be unable to predict which category a new operator they encounter belongs to.

### The strong outline

```
# Reactor for Engineers Who Have Lost Patience with Callback Hell

## Series Overview
- Scope: Project Reactor 3.6, focused on its use as the foundation for
  Spring WebFlux services
- Reader: Java backend engineer (3+ years), comfortable with Spring Boot,
  has hit the limits of CompletableFuture or has tried RxJava and bounced
  off it
- Series voice: Mechanism Autopsy with Production War Story for Phase 4
- Article count: 8 across 4 phases

## Phase 1 — Unlearning Iterators: The Publisher Contract and Why Nothing Happens Until Subscription

By the end of this phase, the reader will have replaced their iterator-based
mental model of streams with the publish-subscribe model that Reactor
implements. The single most common confusion in Reactor — that a chain of
operators is a description of work, not the work itself — is addressed
in this phase.

- Article 1.1: Reactor publishers are recipes, not actions: the
  one-sentence mental model that explains why your operators are not
  running and how to make them run
- Article 1.2: Mono and Flux are not "single value" and "multiple values"
  — they are "at most one notification" and "any number of notifications",
  and the distinction is not pedantic

## Phase 2 — Operator Fluency: The Four Categories and Why Almost Everything in Reactor Fits Them

By the end of this phase, the reader will have a categorization of Reactor's
operators that lets them predict the behavior of operators they have not
seen before. The categories — transformation, combination, side effect,
control flow — are not explicitly named in the Reactor documentation, which
is exactly why the series needs to name them.

- Article 2.1: Reactor's transformation operators are pure functions on
  publishers; the dozen or so you actually need and how they compose
- Article 2.2: Combining publishers is hard because of timing, not because
  of the API: zip, merge, concat, switchMap, flatMap, and the one question
  that decides which one you want
- Article 2.3: Side-effect operators (doOnNext, doOnError, doOnSubscribe)
  exist because Reactor is functional in a world that is not, and using
  them wrong creates the exact bugs they exist to prevent

## Phase 3 — The Execution Model: Schedulers, Backpressure, and the Things That Make Reactor Hard to Reason About

By the end of this phase, the reader will understand what determines which
thread Reactor's code runs on and what happens when the producer is faster
than the consumer. These two questions are the hardest to answer without
opening the source.

- Article 3.1: Schedulers in Reactor are not the same as Java's
  ExecutorService — and the difference explains why subscribeOn and
  publishOn behave differently than you expect
- Article 3.2: Backpressure is not flow control; it is a contract between
  the producer and consumer about how much the consumer is willing to
  receive — and Reactor's default backpressure strategies hide bugs

## Phase 4 — Reactor in Production: Where Reactor Bends and Where It Breaks

By the end of the series, the reader will know the failure modes that
Reactor introduces in production and how to recognize them. This phase
delivers the operational payoff that the earlier phases set up.

- Article 4.1: The three failure modes of mixing blocking calls into a
  Reactor pipeline, why each one is hard to detect, and the one tool
  (BlockHound) that catches them all
```

The strong Reactor outline rejects the "basic vs advanced operators" framing in favor of the four-category model in Phase 2. The four categories are not arbitrary — they are the categories that emerge from actually thinking about what Reactor's operators do — and the act of naming them is one of the series' most useful contributions. The reader who finishes Phase 2 can pick up an operator they have never seen before and predict which category it belongs to and roughly what it does, which is a transferable understanding that the weak outline's "basic" and "advanced" framing does not deliver.

The strong outline also addresses the Phase 3 material that the weak outline glosses over. Schedulers and backpressure are the hardest parts of Reactor to understand, and they deserve their own phase rather than being lumped into "Advanced Operators". The strong outline gives them a phase named for what they actually are: the execution model, the things that make Reactor hard to reason about. A reader who has the execution-model mental model can debug Reactor problems; a reader who has only seen "advanced operators" cannot.

## Example 3 — Kubernetes Operators

### The weak outline

```
# Building Kubernetes Operators

## Phase 1: Introduction
- Article 1.1: What are Kubernetes Operators?
- Article 1.2: Setting Up Your Development Environment

## Phase 2: Core Concepts
- Article 2.1: Custom Resource Definitions (CRDs)
- Article 2.2: Controllers and Reconciliation
- Article 2.3: The Operator Pattern

## Phase 3: Building an Operator
- Article 3.1: Hello World Operator
- Article 3.2: Adding More Features
- Article 3.3: Testing Your Operator

## Phase 4: Production
- Article 4.1: Deploying to Production
- Article 4.2: Best Practices
```

The Kubernetes Operators weak outline has all the standard failures plus one specific to this topic: it treats CRDs and Controllers as parallel concepts in Phase 2, when in fact the relationship between them is the entire point of the operator pattern. A CRD is a contract; a controller is the thing that enforces the contract. Treating them as two parallel concepts to learn separately misses what makes the pattern work, and a reader who finishes the weak series will be able to write a CRD and a controller without understanding why they exist together.

### The strong outline

```
# Kubernetes Operators: When the Reconciliation Loop Is the Architecture

## Series Overview
- Scope: Kubernetes 1.30+ Operator development in Go using Kubebuilder,
  focused on production operators rather than tutorial demos
- Reader: backend engineer who has used Kubernetes as a platform user
  (kubectl apply, Deployments, ConfigMaps) but has not built an operator
- Series voice: Mechanism Autopsy with Design Tribunal for the
  CRD-as-contract material
- Article count: 7 across 3 phases

## Phase 1 — The Reconciliation Loop Is Not a Side Detail: It Is the Architecture

By the end of this phase, the reader will understand that Kubernetes
operators are not "scripts that watch for events" — they are reconciliation
loops that compare desired state to actual state and converge the two,
and that this single property determines everything about how operators
must be built.

- Article 1.1: Reconciliation, not events: why your first operator should
  not subscribe to add/update/delete and what it should do instead
- Article 1.2: The CRD is a contract between the operator author and
  every future version of the operator — and the contract is harder to
  change than you think

## Phase 2 — Building Reconcilers That Survive Real Clusters

By the end of this phase, the reader will be able to write a reconciler
that is idempotent under retry, correct under partial failure, safe
under concurrent execution, and predictable under cluster restart.
These four properties are not optional — operators that lack any of them
are bombs waiting to go off in production.

- Article 2.1: Idempotence in reconcilers is harder than it looks: the
  three patterns that look idempotent and are not, with the fix for each
- Article 2.2: Finalizers and the deletion path: the part of operator
  development that the tutorials skip and that breaks every operator
  in production at least once
- Article 2.3: The cache is not the cluster: why your operator's view
  of the world is stale, by how much, and what to do about it

## Phase 3 — CRDs Across Time: Versioning, Conversion, and the Long Arc of Operator Evolution

By the end of this phase, the reader will be able to evolve a CRD across
versions without breaking existing users. This is where most operator
projects fail in their second year, and the series cannot be complete
without addressing it.

- Article 3.1: CRD versioning is not API versioning: the conversion
  webhook is the only safe upgrade path and writing one is harder than
  writing the operator itself
- Article 3.2: When the CRD becomes a liability: the four signs your
  operator's contract is wrong and what to do about each one
```

The strong Kubernetes Operators outline restructures the topic around the load-bearing claim that operators are reconciliation loops, not event handlers. This claim is the aha moment for the topic — until a reader internalizes it, every other concept in operator development feels arbitrary; once they internalize it, the rest of the framework falls into place. The series puts this claim at the center of Phase 1 and lets the rest of the series build on it.

The strong outline also addresses CRD versioning in its own phase, which the weak outline omits entirely. CRD versioning is the topic that breaks operator projects in their second year, and the absence of any treatment of it in the weak outline is a Void Inheritance failure — the planner missed a load-bearing topic because the documentation tutorials do not emphasize it. The strong outline catches the gap because Phase 1 of the planner's research methodology specifically directs the planner to look for "what the docs do not tell you", and CRD versioning is exactly the kind of topic that the official tutorials gloss over but that production users need.

## Reading the examples

The three pairs above are not meant to be templates. The structures of the strong outlines vary by topic — Spring AI's strong outline is a narrow four-phase operational slice, Reactor's strong outline has four phases following Mechanism Mastery, and Kubernetes Operators' strong outline has three phases following a pattern that is closest to Mechanism Mastery with elements of Decision Tribunal in Phase 3. The right pattern was chosen for each topic based on the reader profile, the intended breadth, and the topic's structural complexity, not by applying a template.

What the three strong outlines share is the application of the quality checklist's principles. Every phase name declares a cognitive transition. Every article title carries an argument. Every series structure differs visibly from the official documentation's structure. Every series ends with a cumulative payoff that depends on the earlier articles. The principles are constant; the structures that implement them vary.

A planner who reads only the strong outlines may miss the point. The strong outlines are easier to evaluate against the weak outlines than against an idealized notion of "good", because the failure patterns in the weak outlines are concrete and identifiable. Reading both versions of each example is the most efficient way to internalize the difference between surface skating and substantive planning.
