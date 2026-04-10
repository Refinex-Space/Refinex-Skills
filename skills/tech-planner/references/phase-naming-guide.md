# Phase naming guide

Phase names in a tech-planner series outline carry more weight than they might seem to at first. A phase name is the first thing a reader sees when they scan the series, and it is the label that organizes the reader's mental model of the series as a whole. A weak phase name like "Basics" or "Advanced Topics" teaches the reader nothing about what the phase will do for them and leaves them no reason to read the phase in order rather than skipping around. A strong phase name declares a cognitive transition that the reader will undergo during the phase, and it gives the reader a reason to commit to the phase as a unit.

This guide describes the naming discipline for phases, with concrete good and bad examples across a range of framework topics. The discipline is enforced by Gate 3 of the outline quality checklist, which rejects topic-grouping phase names and requires cognitive-progression phase names.

## The core principle

A phase name reflects cognitive progression, not topic grouping. The distinction is subtle but load-bearing. A topic-grouping name describes what the phase is about. A cognitive-progression name describes what the phase does to the reader. "Spring AI Fundamentals" is a topic grouping. "Rebuilding Your Mental Model: Why Spring AI Is Not Just Another LangChain" is a cognitive progression. The second name tells the reader what will be different about them after they finish the phase — their mental model will have been rebuilt — and that is a promise the reader can evaluate the phase against.

Cognitive progression names are harder to write than topic grouping names, which is why topic grouping is the default. The payoff for the extra work is that cognitive progression names make the series' structure legible. A reader who reads only the phase names should be able to understand the arc of the series: where it starts the reader, where it takes the reader, and how the intermediate stops move the reader along that arc. A series whose phase names are "Basics", "Intermediate", "Advanced", "Expert" has no arc and communicates no movement; it is just a pile of material sorted by difficulty.

## The four verbs of cognitive progression

Most cognitive progression names contain, explicitly or implicitly, one of four verbs: reconstruct, master, extend, or debug. These verbs correspond to the four cognitive states that experienced readers typically pass through when learning a new framework, and together they cover the common arc of a series targeted at professional engineers.

**Reconstruct** is the first cognitive state, where the reader is replacing a prior mental model with a new one. A reader approaching Spring AI from LangChain, or Project Reactor from imperative Java, or Kubernetes Operators from generic cloud automation, is in the reconstruct state. The phase that serves them is not "introduction" or "basics" — it is "unlearn the old model and build the new one". Phase names for the reconstruct state often include the words reconstruct, rethink, reframe, unlearn, rebuild, or shift. A strong example: "Phase 1: Reconstructing the Request-Response Model — Why Reactor Streams Are Not Just Lazy Iterators".

**Master** is the second cognitive state, where the reader has the new mental model and needs to deepen their command of the framework's mechanism. This is the phase where internal details, core abstractions, and execution models are taught. Phase names for the master state often include the words master, internalize, mechanism, anatomy, or dissect. A strong example: "Phase 2: Mastering the Advisor Chain — How Spring AI Composes Pipeline Behavior from Pure Functions".

**Extend** is the third cognitive state, where the reader wants to customize or extend the framework. This is where extension points, plugin systems, and framework hooks become the focus. The reader in this state already knows the framework's mechanism and is now looking for the leverage points. Phase names for the extend state often include the words extend, customize, hook, plug, or shape. A strong example: "Phase 3: Extending Spring AI — Writing Advisors, Tools, and Custom Memory".

**Debug** is the fourth cognitive state, where the reader is trying to understand why the framework is not behaving as they expected. This is the production-issues phase, covering failure modes, debugging techniques, and operational concerns. The reader in this state needs specific diagnostic help, not general overview. Phase names for the debug state often include the words debug, diagnose, investigate, failure, incident, or trace. A strong example: "Phase 4: When It Goes Wrong — Diagnosing Spring AI Production Failures from Symptoms to Root Causes".

Not every series needs all four phases, and some series benefit from phases that do not map cleanly to any of the four verbs. The four verbs are a starting point for naming, not a template that must be followed.

## Three tests for a phase name

Before accepting a phase name as final, run three tests against it. A name that passes all three is strong; a name that fails any of the three should be rewritten before the outline is delivered.

The first test is the **transformation test**. Read the phase name and ask: what will be different about the reader after they finish this phase that is not different now? If the answer is "they will know more about X", the name is failing the test — that answer applies to every phase of every series and tells the reader nothing. If the answer is specific — "they will be able to predict the behavior of operators they have not seen before", "they will understand why their first event-handler-based operator was wrong", "they will be able to write a reconciler that survives partial failure" — the name is doing its job. The transformation test forces the planner to commit to a specific change in the reader's capabilities.

The second test is the **falsifiability test**. Read the phase name and ask: could this phase fail to deliver what the name promises? If the name is so vague that no possible execution could fail to fulfill it, the name is making no promise. "Phase 1: Introduction to Spring AI" cannot fail because "introduction" can mean anything; "Phase 1: Why Spring AI's First-Class Bean Treatment Changes How You Structure Prompt Code" can fail if the phase does not actually demonstrate the change. Falsifiability is the property that distinguishes a promise from a label.

The third test is the **argument test**. Read the phase name and ask: does it contain a claim, even an implicit one? "Mastering the Pipeline" contains the implicit claim that there is a pipeline worth mastering and that the phase will make it masterable. "Reconstructing the Mental Model" contains the implicit claim that the reader's current mental model needs reconstruction. "Basics" contains no claim at all. The argument test catches the difference between a name that says something and a name that just sits in the slot where a name belongs.

## Good and bad examples

The best way to internalize the discipline is to see the same content named in both a bad (topic-grouping) way and a good (cognitive-progression) way across several frameworks. The pairs below walk through five examples, each showing the cost of the topic-grouping approach and the benefit of the cognitive-progression alternative.

**Example 1 — Spring AI**

A topic-grouping series might name its phases: "Phase 1: Spring AI Basics; Phase 2: Advanced Features; Phase 3: Production Deployment". These names are true but useless. They tell the reader nothing about what the series is actually doing, and a reader scanning the phase list has no reason to read Phase 1 before Phase 2 beyond the implicit "basics come first" convention.

A cognitive-progression version of the same content might name the phases: "Phase 1: Rebuilding Your LLM Mental Model — Why Spring AI Is Not LangChain-for-Java; Phase 2: Mastering the Advisor Pipeline — How Spring AI Composes Behavior; Phase 3: Extending the Framework — Custom Advisors, Tools, and Memory". Each name declares what the reader will experience during the phase and gives them a reason to read it in order. The arc is visible: the reader starts confused about Spring AI's place in the ecosystem, masters its mechanism, and learns to extend it.

**Example 2 — Project Reactor**

Topic-grouping: "Phase 1: Reactive Basics; Phase 2: Operators; Phase 3: Advanced Topics". The word "basics" is doing a lot of work here, and the work is hiding a problem — Reactor's "basics" include some of its most counterintuitive concepts, and a phase labeled "basics" will not prepare the reader for the cognitive jump they need to make.

Cognitive-progression: "Phase 1: Unlearning Iterators — The Publisher Contract and Why Nothing Happens Until Subscription; Phase 2: Operator Fluency — The Four Categories of Transformations and Why Most of Reactor Fits Them; Phase 3: Schedulers, Backpressure, and the Rest of the Execution Model". This version prepares the reader for the specific cognitive work each phase requires, and the reader who reads the phase names alone already has the skeleton of a Reactor mental model.

**Example 3 — Kubernetes Operators**

Topic-grouping: "Phase 1: Introduction to Operators; Phase 2: Writing Your First Operator; Phase 3: Advanced Patterns". This is a hands-on tutorial framing, which is fine for some series, but it does not describe the series' argument or its intellectual move.

Cognitive-progression: "Phase 1: The Controller Pattern — Why Kubernetes Is a Reconciliation Loop, Not a State Machine; Phase 2: Building Reconcilers That Survive Real Clusters — Idempotence, Finalizers, and the Cache; Phase 3: CRDs as Contracts — Versioning, Conversion, and the Long Arc of Operator Evolution". Notice that each phase name contains a claim — the controller pattern is a reconciliation loop, not a state machine; real reconcilers require idempotence and finalizers; CRDs are contracts, not data schemas — and each claim is arguable and defensible. The phase names are arguments in miniature.

**Example 4 — gRPC internals**

Topic-grouping: "Phase 1: gRPC Overview; Phase 2: Protocol Details; Phase 3: Performance Tuning". The overview-details-tuning shape is the default for any protocol deep-dive and tells the reader nothing about what makes gRPC specifically worth understanding.

Cognitive-progression: "Phase 1: HTTP/2 Is the Substrate, Not the Protocol — Why gRPC's Streaming Semantics Come from Frames, Not from RPC; Phase 2: The Four Call Types Are One Call Type with Different Subscription Patterns; Phase 3: Where gRPC Falls Off the Cliff — Headers, Trailers, and the Failure Modes the Tutorials Skip". Each phase names a specific aha moment about gRPC that the reader will reach by the end of the phase.

**Example 5 — Rust async runtime**

Topic-grouping: "Phase 1: Introduction to Async Rust; Phase 2: Tokio Fundamentals; Phase 3: Advanced Patterns". The shape is borrowed from every other "introduction to async" guide, none of which addresses the specific confusions Rust async causes.

Cognitive-progression: "Phase 1: Futures Are Not Promises — Why Polling Is the Whole Game; Phase 2: The Executor Decides When You Run, and the Decision Is Encoded in Pin and Waker; Phase 3: Cancellation Is Just Drop, and That Is Both the Power and the Trap". The names commit to specific claims about Rust async that the phases must then defend, and the reader who finishes the series will have internalized those claims as their working mental model.

## The trap of cosmetic renaming

The most common failure when writers first apply this discipline is cosmetic renaming. The writer reads the principle, looks at their topic-grouping names, and adds a colon and a clause that gestures at cognitive progression without actually committing to one. "Phase 1: Basics" becomes "Phase 1: Basics — Getting Started with the Fundamentals", which fails all three tests just as badly as the original. The cosmetic version is sometimes worse than the original because it looks like the writer has done the work when they have not.

The fix for cosmetic renaming is to drop the topic-grouping name entirely and start over from the cognitive transition the phase produces. The writer asks: what is this phase actually for? What will the reader be able to do after reading it that they cannot do now? The answer to those questions is the basis for the new name. The original topic-grouping name plays no role in the new name — it is discarded, not extended.

## A short workflow for naming

The workflow for naming a phase is short. First, write the phase's central cognitive transition in one sentence. Second, identify the verb category from the four verbs above (reconstruct, master, extend, debug) that most closely matches the transition. Third, draft a phase name that uses the verb category's vocabulary and that contains a specific claim about the topic. Fourth, run the three tests against the draft and revise until all three pass. Fifth, check the name against the rest of the series — the names should form a visible arc when read in order, and any name that breaks the arc should be reconsidered.

Most strong phase names emerge from this workflow on the second or third draft. The first draft is usually too generic; the revisions sharpen the claim and tighten the language until the name is doing real work. A planner who finds themselves on the seventh draft of a phase name should consider whether the phase itself is well-defined, because phase names that resist sharpening are usually phase names whose underlying purpose is unclear.