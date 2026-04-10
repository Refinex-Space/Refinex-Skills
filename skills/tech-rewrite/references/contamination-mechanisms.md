# Contamination mechanisms

This file catalogs the ten specific mechanisms by which low-quality source material degrades an AI-rewritten output. Each mechanism has a name, a definition, an explanation of why it happens, a concrete before/after example, a detection heuristic that can be run mechanically, and a defense strategy.

The first seven mechanisms are drawn from the original design brief. The last three are additions grounded in research on LLM paraphrasing behavior, where academic work has documented that language models preserve stylistic and structural cues from source material in ways the writer does not consciously intend. All ten mechanisms are distinct enough to warrant separate detection, and defending against each one requires a different move during the extraction and target-definition phases.

---

## 1. Structural Mirroring

Structural Mirroring is the mechanism by which the output silently copies the source's section structure, ordering, and pacing, even when a completely different structure would serve the reader better. It is the most common contamination pattern and the default failure mode for any rewrite that does not enforce an extraction firewall. It happens whenever the writer reads the source from beginning to end and then begins drafting, because the writer's mental model of "what this topic looks like" has been shaped by the source's shape during the reading pass.

The mechanism is subtle because it does not require the writer to consciously decide to preserve the source's structure. The source's structure becomes the default, and defaults are invisible. A source that opens with three paragraphs of history, covers the topic in feature-by-feature order, and closes with a one-paragraph summary will tend to produce an output that opens with history, covers the topic feature-by-feature, and closes with a summary — even if the writer's central argument would be better served by opening with a specific failure and working backward through the mechanism that produced it.

Academic research on LLM paraphrasing has measured this effect directly. Even in zero-shot settings where the model is given no examples of the source's style, the rewritten text retains enough structural and topical overlap with the source to be attributed to the same author by classifiers. Content overlap alone leaks authorship. Structure is one of the loudest signals in that content overlap.

### Before and after

**Source material (an internal wiki page titled "Introduction to Our Caching Layer"):**

> ## History
> Our caching layer was introduced in Q2 2023 to address growing latency concerns. It was originally built on Redis, but we moved to a custom solution in Q4 2024.
>
> ## Features
> - Supports both read-through and write-through caching
> - Automatic key expiration based on TTL
> - Configurable eviction policies
> - Built-in metrics for observability
>
> ## Configuration
> The cache can be configured via `cache.yml`. Common options include...
>
> ## Troubleshooting
> If you experience cache misses, check the TTL settings and verify...

**Contaminated rewrite (keeps the source's shape, polishes the prose):**

> ## A Brief History of Our Caching Layer
> Our caching infrastructure has an interesting history. Introduced in Q2 2023 to address mounting latency concerns, the initial implementation leveraged Redis. However, in Q4 2024, we transitioned to a custom-built solution better suited to our scale.
>
> ## Key Features
> Our caching layer offers a rich set of capabilities: read-through and write-through patterns, TTL-based key expiration, configurable eviction policies, and comprehensive metrics for observability.
>
> ## Configuring the Cache
> ...

The contaminated rewrite inherits the source's four-section structure (History, Features, Configuration, Troubleshooting), the source's ordering (history first, features second, troubleshooting last), and the source's feature-tour framing. The writer has changed the words and nothing else. The structure is still a generic wiki page, not a piece that argues anything.

**Clean rewrite from the Fact Register (target argument: "our custom cache's TTL semantics differ from Redis in one load-bearing way that bit us in production"):**

> # Why our cache's TTL is not the TTL you think it is
>
> Three months after we replaced Redis with our custom cache, a production incident traced to a single assumption that no one had written down: our TTL field semantically means "maximum age since last write", not "maximum age since last access" as Redis's TTL does. The difference does not matter for caches with stable write patterns. It matters enormously for caches that front slow backends with bursty reads, which is exactly what our payment service does.
>
> This post walks through the incident, the semantic gap between the two TTL models, and the specific workloads where the distinction flips from irrelevant to load-bearing.
>
> ...

The clean rewrite shares almost no structural DNA with the source. It opens with an incident, not a history. It has no "features" section. It argues one thing. The source was an input to the writer's thinking, not a template.

### Why it happens

The writer reads the source and forms a mental representation of the topic. That representation is shaped by the source's structure — sections become mental buckets, ordering becomes mental precedence, pacing becomes mental emphasis. When the writer sits down to draft, the mental representation is what gets committed to the page, and the structure of the representation leaks into the structure of the draft.

The only reliable defense is the firewall. The Fact Register strips structure from facts. A sentence in the KEPT section does not know what section of the source it came from; it just knows the fact. When the writer builds the target from the Fact Register, there is no source structure left to mirror.

### Detection heuristic

Compare the headings of the draft against the headings of the source side by side. Do the two lists share a common order? Do the counts roughly match? Would a reader who had seen both be able to tell, from structure alone, that one was derived from the other? If yes to any of these, the draft has Structural Mirroring. The fix is to go back to Phase 2 and redesign the structure from the Anchor Sheet without consulting the source's headings.

### Defense

The Fact Register. Populate it in Phase 1. Close the source in Phase 2. Design the structure from the central argument and the reader, not from the source's shape. When in doubt about structure, ask what a blank-page writer with only the Fact Register would produce.

---

## 2. Void Inheritance

Void Inheritance is the mechanism by which the source's gaps become the output's gaps. The source fails to cover some aspect of the topic — a load-bearing consideration, a standard cross-cutting concern, a failure mode the reader would expect to see addressed — and the output silently fails to cover the same aspect, because the writer never noticed the absence. The mechanism is insidious in a way that Structural Mirroring is not, because a gap is invisible by definition. The writer does not see the thing the source did not write.

A common concrete case: a legacy design document that was written before observability was a standard concern. The document discusses data models, APIs, and components in detail, but says nothing about metrics, tracing, or logging. A writer rewriting that document in 2026 may absorb the document's framing of the topic — "this is a design document, and these are the sections a design document covers" — and produce a polished rewrite that similarly says nothing about observability, even though any modern design document would have an observability section. The source's blind spot has become the output's blind spot.

### Before and after

**Source (an email from a tech lead to their team, proposing a cache invalidation strategy):**

> Team,
>
> I've been thinking about our cache invalidation problem. Here's my proposal:
>
> 1. On any write to the user table, emit an event to our event bus
> 2. A cache-invalidator worker listens on the event bus and deletes the corresponding cache keys
> 3. The worker processes events in FIFO order to maintain consistency
>
> This should keep our cache fresh without requiring every writer to know about the cache.
>
> Thoughts?

**Contaminated rewrite (Void Inheritance — silently inherits every gap):**

> ## Cache Invalidation via Event Bus
>
> We propose an event-driven cache invalidation strategy. On any write to the user table, the writing service emits an event to our event bus. A dedicated cache-invalidator worker subscribes to these events and deletes the corresponding cache keys. The worker processes events in FIFO order to maintain consistency.
>
> This decoupled approach keeps cache freshness without requiring every writer to know about the cache.
>
> ### Benefits
> - Decoupled from writers
> - Event-driven and scalable
> - Maintains consistency through ordered processing

The contaminated rewrite has polished the email into prose and added a benefits section, but it has inherited every gap in the original. What happens if the event bus loses an event? What happens if the invalidator worker falls behind? What is the staleness bound the reader should expect? How is the invalidator itself made highly available? What are the failure modes of FIFO processing when events fan out to millions of keys? None of these questions is answered, because none of them was asked in the source, and the rewriter never noticed the absences.

**Clean rewrite after Void Inheritance is addressed:**

Before any rewriting begins, the Fact Register's MISSING section would catalog the gaps:

> **MISSING:**
> - Failure mode for dropped events (no at-least-once delivery guarantee stated)
> - Behavior under invalidator lag (no staleness SLO)
> - Invalidator HA model (single worker? Multiple? Coordination?)
> - Behavior when an event cascades to >1 key (fan-out semantics)
> - Ordering across multiple writers (is global FIFO required, or only per-key?)
> - Observability hooks (no metrics mentioned)

Each MISSING item would then be resolved in Phase 2 before drafting: some by asking the user, some by research, some by explicit scope-out ("this doc covers the event-emission side only; the invalidator worker design is a separate doc"). The resulting draft would address the gaps that matter for the document's argument and explicitly scope out the rest.

### Why it happens

Writers scan sources for content that is present, not for content that is absent. A careful read of the source answers the question "what does this source say?" — not the question "what would a strong document on this topic need to say that this source does not say?" The second question is the defense against Void Inheritance, and it is only reliably asked when the extraction protocol requires a MISSING section.

### Detection heuristic

For any rewritten draft, mentally generate the list of standard cross-cutting concerns for its document type — for design documents, this includes observability, security, privacy, failure modes, rollout, cost. For blog posts, it includes limitations, edge cases, rejected alternatives. For each concern on the list, check whether the draft addresses it. An absence is a candidate for Void Inheritance, confirmed if the source also fails to address the same concern.

### Defense

The MISSING section of the Fact Register. Populating it requires the extractor to ask, for each standard expectation of the target document type, "does the source provide this?" — and when the answer is no, to record the gap explicitly. Every MISSING item becomes a visible decision in Phase 2 rather than an invisible gap in the output.

---

## 3. Ambiguity Whitewashing

Ambiguity Whitewashing is the mechanism by which a vague, hedged, or unsubstantiated claim in the source is polished into confident prose in the output, without any new substance being added. The claim appears to improve — the sentence is better constructed, the vocabulary is tighter, the hedges are gone — but the underlying vagueness has not been replaced with anything. It has been hidden. A reader of the rewrite cannot tell that the claim is vague, which is worse than the source version, where the hedges were at least honest.

The mechanism is particularly harmful because the polish looks like improvement. The writer feels they have done good work; the reader trusts the polished prose because it reads authoritatively. But the factual content has not advanced, and in fact has regressed because the reader has lost the epistemic warning that the hedges provided.

### Before and after

**Source:**

> We think our service is probably faster than the old one, maybe by a noticeable amount in most cases. It seems to handle the load well, though we haven't done formal benchmarking.

**Contaminated rewrite (Ambiguity Whitewashing — polishes the hedges out):**

> Our service delivers significantly improved performance over the legacy system. It handles production load efficiently, providing a noticeable speedup for our users.

The contaminated rewrite reads as an authoritative performance claim. It has no hedges. A reader will come away believing the service is measurably faster. But the source said the opposite: the team *thinks* it is probably faster, has not actually measured it, and has no quantitative evidence. The rewrite is not just imprecise — it is less honest than the source.

**Clean rewrite after Ambiguity Whitewashing is addressed:**

Before rewriting, the extraction phase would place the vague claim in the DISCARDED section of the Fact Register:

> **DISCARDED:**
> - "probably faster than the old one" — no measurement, no baseline, no benchmark; hedged in source; cannot be converted to a KEPT fact without new data
> - "handle the load well" — no load figure, no success criterion, no SLO; ditto

In Phase 2, the writer would either (a) scope the output to exclude the performance claim entirely, (b) ask the user to supply benchmark numbers, or (c) note in the draft that the team believes the service is faster but has not formally benchmarked, preserving the honest hedge. Any of these is better than polishing a rumor into a fact.

### Why it happens

Polishing prose is what writers are trained to do. When a writer encounters a sentence with hedges and an unsupported claim, the instinct is to tighten the sentence — to cut the hedges and sharpen the language. That instinct is correct when the sentence's content is solid and the hedges are stylistic padding. It is wrong when the hedges are honest signals of uncertainty and cutting them produces a false assertion.

The only reliable way to tell the difference is to ask, during extraction, whether the claim is backed by something the writer would want to cite. If the answer is yes, the claim goes in KEPT (and the hedges can be tightened or cut). If the answer is no, the claim goes in DISCARDED, and the writing phase never sees it as available material.

### Detection heuristic

For any confident-sounding factual claim in the draft, locate the corresponding claim in the source. Does the source make the same claim with the same confidence? If the source hedged and the draft did not, the claim has been Ambiguity-Whitewashed. Fix by restoring the hedge, citing a real source, or cutting the claim.

### Defense

The DISCARDED section of the Fact Register. Vague claims from the source are cataloged explicitly and labeled as unavailable for the writing phase. They cannot drift into the output because they are not in the KEPT section, which is the only section the writing phase draws from.

---

## 4. Tone Infiltration

Tone Infiltration is the mechanism by which the source's tone — marketing, tutorial, academic, bureaucratic, stream-of-consciousness — leaks into the output even when the writer intends a different tone. It is the contamination mechanism with the strongest academic evidence behind it. Research on LLM paraphrasing has shown directly that rewritten text preserves stylistic cues from the source at a level detectable by authorship-attribution classifiers, even when the rewrite was explicitly asked to change the style. The writer cannot simply "try harder" to change the tone; the stylistic cues are below the level of conscious intent.

In practice, Tone Infiltration shows up as phrasings, rhythms, and signal words that the source used and that the output unconsciously imitates. A source written in marketing voice will produce a rewrite with faint marketing undertones — an occasional "powerful", an occasional "seamless", a rhythm of sentences that sells rather than explains. A source written in tutorial voice will produce a rewrite with residual "let us" and "as we can see". A source written in academic voice will produce a rewrite with residual "it is worth noting" and "one might argue".

### Before and after

**Source (marketing-voice whitepaper excerpt):**

> Our revolutionary new caching engine harnesses the power of cutting-edge memory architecture to deliver blazing-fast performance at scale. With seamless integration and enterprise-grade reliability, it empowers organizations to unlock unprecedented levels of responsiveness across their entire technology stack.

**Contaminated rewrite (Tone Infiltration — marketing vocabulary and rhythms survive):**

> Our caching engine is built on a modern memory architecture to deliver high performance at scale. With smooth integration and solid reliability, it helps teams achieve strong levels of responsiveness across their stack.

The contaminated rewrite has removed the most obvious marketing words but has inherited the sentence rhythm, the "X delivers Y at Z" construction, and the soft evaluative adjectives ("high", "smooth", "solid", "strong"). A reader does not immediately notice the marketing voice, but it is still there. The piece still feels like a whitepaper, not like a senior engineer explaining to a peer.

**Clean rewrite with tone reset:**

> The cache sits between the application tier and the database, with an in-process L1 backed by a networked L2. L1 is per-instance and uses off-heap memory to avoid GC pressure; L2 is shared across instances and uses a Redis-compatible wire protocol so existing clients work without changes. The design's only unusual move is that L2 writes go through a serializer that enforces schema compatibility, which is the reason we built this instead of running Redis directly.

The clean rewrite has none of the marketing residue. The sentence rhythm is different. The vocabulary is concrete. The evaluative adjectives are gone. A reader would not mistake this for a marketing whitepaper.

### Why it happens

Stylistic cues operate below the level of conscious editing. Sentence rhythm, metaphor choice, evaluative adjective frequency, and connective word patterns are absorbed during reading and reproduced during writing without the writer noticing. The Ship of Theseus paper on LLM paraphrasing documented this effect quantitatively: LLM-rewritten text retains enough of the source's style to be attributed to the source's author by classifiers, even when the LLM was asked to change the style.

### Detection heuristic

Read the rewrite out loud and listen for rhythmic echoes of the source. Also check for residual signal words from the source's voice: marketing words ("powerful", "seamless", "unlock", "empower"), tutorial words ("let us", "as we can see", "now we will"), academic words ("it is worth noting", "one might argue", "in this regard"), bureaucratic words ("stakeholders", "alignment", "going forward"). Each residual is a signal that tone has leaked.

### Defense

Name the target voice explicitly in Phase 2, from the catalog in `shared-narrative-voices.md`, before writing begins. Do not leave the voice implicit. When drafting, consult the voice's "forbidden moves" list and sweep for violations after drafting. If the source has a particularly strong or distinctive voice, the contamination risk assessment should rate Tone Infiltration as high, which triggers extra discipline during the sweep.

---

## 5. Rationale Vacuum

Rationale Vacuum is the mechanism by which the source states a decision without giving a reason, and the output repeats the decision without giving a reason. The output looks authoritative because the decision is asserted confidently, but a senior reader can tell that no one has justified the choice. The piece reads as "we decided X", not "we decided X because Y, after considering Z and rejecting it for reason W".

Rationale Vacuum is the contamination mechanism that most directly breaks the shared quality standards. The quality checklist requires every design decision to list rejected alternatives with specific reasons. A source that does not provide those reasons cannot pass the gate on its own; the writer must either extract the reasons from the user, research them, or scope the decision out of the output. Rewrites that fail to do this produce polished-looking pieces that fail Gate 5 of the shared quality checklist.

### Before and after

**Source (a meeting note):**

> Decision: use Kafka for the event bus. Start with 3 brokers.

**Contaminated rewrite:**

> ## Event Bus Architecture
>
> For our event bus, we will be using Kafka. Our initial deployment will consist of 3 brokers, providing a solid foundation for our event-driven architecture.

The contaminated rewrite has dressed up a decision in professional prose but has not added a single reason. Why Kafka and not RabbitMQ, NATS, Pulsar, or SQS? Why 3 brokers and not 5 or 9? What is the workload that informs the sizing? Why does the team believe this is the right call? None of this is in the source, and none of it has made it into the output. A senior reader will see through the prose immediately.

**Clean rewrite after Rationale Vacuum is addressed:**

In extraction, the Fact Register would flag the rationale gap:

> **MISSING:**
> - Why Kafka over alternatives (RabbitMQ, NATS, Pulsar, SQS)
> - Why 3 brokers (what workload, what throughput target, what failure tolerance)

In Phase 2, the writer asks the user: "The meeting note says Kafka with 3 brokers, but does not say why. Can you share the reasoning, or should I look up typical sizing guidance for our scale?" Depending on the user's answer, the decision is either justified with specific reasons or scoped out of the draft entirely. What is not acceptable is repeating the unjustified decision as if it were self-evident.

### Why it happens

Writers often treat the source as authoritative even when it is not. If the source asserts a decision, the writer assumes someone had a reason, and assumes the reason is not their job to supply. This assumption is wrong for rewrites: the writer's job is to produce a document that meets the shared quality standards, and the standards require rationale. The source's silence on rationale is a gap the writer must fill.

### Detection heuristic

For every decision in the draft, look for an accompanying reason. If the reason is missing, check whether the source provided one. If neither the source nor the draft has a reason, the draft has a Rationale Vacuum and fails the shared quality checklist's Gate 5. Either supply a reason (from research or user input) or cut the decision from the draft.

### Defense

Phase 2 inherits Gate 5 from the shared quality standards. The writer, when designing the target from the Fact Register, checks whether each decision in KEPT has an accompanying rationale. Missing rationales go into MISSING and are resolved before drafting.

---

## 6. False Completeness

False Completeness is the mechanism by which the writer assumes the source covers the full topic, and the output inherits that assumption. The writer's scoping decisions are made by reference to the source's scope rather than by reference to the reader's actual needs. A source that covers two of the four aspects of a topic produces an output that covers the same two aspects, because the writer never questioned whether there might be other aspects the source omitted.

The defense overlaps with Void Inheritance — both mechanisms turn on the source's gaps — but the two are distinct. Void Inheritance is about specific missing items within an acknowledged scope. False Completeness is about the scope itself: the writer treats the source's scope as the topic's scope and fails to consider that the topic might be larger.

### Before and after

**Source (a two-paragraph internal note titled "Our Database Strategy"):**

> We use PostgreSQL for all primary storage. The main reason is strong consistency for financial data. We run on RDS with read replicas for reporting workloads.

**Contaminated rewrite:**

> ## Our Database Strategy
>
> Our database strategy centers on PostgreSQL, chosen for its strong consistency guarantees which are essential for handling financial data. We run PostgreSQL on Amazon RDS, leveraging read replicas to handle our reporting workloads efficiently.

The contaminated rewrite has treated a two-paragraph note as a complete statement of "our database strategy". But a real database strategy would address many topics the source does not mention: backup and recovery policy, disaster recovery, encryption at rest and in flight, schema change process, capacity planning, cost model, failover procedure, monitoring and alerting thresholds, retention policy, access control. The source's silence on all of these does not mean the strategy excludes them — it means the source was not a database strategy at all, only a fragment of one.

**Clean handling:**

The extractor would flag the scope mismatch in the contamination risk assessment:

> **False Completeness: HIGH**
> - Source is two paragraphs titled "Our Database Strategy"; real database strategy documents address at least 10 standard topics; source addresses 3
> - Defense: narrow the output's title and scope to match what the source actually covers ("Why we chose PostgreSQL on RDS for our primary storage"), and explicitly flag the other topics as out of scope or covered elsewhere

The Phase 2 output would be a different document with a narrower title, or a document that explicitly acknowledges the source only covers part of the strategy and treats the rest as scoped out.

### Why it happens

The writer takes the source at face value. If the source is titled "Our X Strategy", the writer treats the source as a statement of X strategy. The title creates an implicit contract — "this is what X strategy is" — and the writer honors the contract without noticing that the contract is false.

### Detection heuristic

For any rewrite, list the topics a strong document on the same subject would cover. Compare against the topics the source covers. If the source covers substantially fewer topics, the source is incomplete, and the draft must either (a) fill the gaps or (b) narrow its scope to match what the source actually covers. Producing a draft that inherits the source's narrow scope while keeping a broad title is the failure.

### Defense

In Phase 1, run the contamination risk assessment. False Completeness is one of the explicit risk categories. When flagged, the defense is to narrow the title in Phase 2 or to expand the KEPT section with material from sources other than the original (research, user input) before drafting.

---

## 7. Scope Inflation

Scope Inflation is the inverse of False Completeness. The source covers too much ground — loose notes that wander across five topics, a meeting transcript that touches three different decisions, a legacy wiki page that accreted sections for years without pruning — and the output covers the same too-much ground, because the writer did not exercise the option to narrow.

Scope Inflation produces rewrites that feel professional but lack a central argument. They cover many topics, none of them deeply. They are the "comprehensive guide" anti-pattern from the shared anti-pattern catalog, triggered by a source that imposed its breadth on the writer rather than by a writer who chose breadth.

### Before and after

**Source (a loose note from a weekly architecture meeting):**

> Notes from arch review:
> - Discussed moving to k8s. Consensus: not now, too much ops work. Revisit Q3.
> - Cache invalidation still flaky. Action: Alice to investigate
> - Payment service p99 is over budget at 180ms. Target is 100ms. No root cause yet.
> - Need to deprecate legacy oauth flow. Blocked on customer X still using it.
> - New observability stack rollout delayed to Q4.
> - Interns start Monday.

**Contaminated rewrite (Scope Inflation — tries to cover all six topics):**

> ## Architecture Review Summary
>
> ### Kubernetes Migration
> The team evaluated a potential migration to Kubernetes and determined that the operational overhead would be prohibitive at this time...
>
> ### Cache Invalidation Issues
> Recurring issues with cache invalidation have been flagged for investigation...
>
> ### Payment Service Performance
> The payment service currently exceeds its latency budget, with p99 measurements around 180ms against a target of 100ms...
>
> ### Legacy OAuth Deprecation
> ...

The contaminated rewrite is not a document; it is six documents compressed into one. Each topic gets a paragraph that cannot cover its topic adequately. The reader cannot tell what the document is *about*. A senior engineer reading the rewrite will conclude that the writer did not know what they were trying to say.

**Clean rewrite after Scope Inflation is addressed:**

In Phase 1, the extractor would note:

> **Scope Inflation: HIGH**
> - Source covers 6 distinct topics
> - None receives enough depth to be an argued piece
> - Defense: pick ONE topic for this rewrite; if the user wants multiple documents, propose splitting and confirm

In Phase 2, the writer would propose to the user: "The meeting notes cover six different topics. I recommend writing the payment-service latency investigation as a standalone piece since it has the clearest open question and the most concrete numbers. The Kubernetes decision and the OAuth deprecation could be separate ADRs. The other items are status updates that do not warrant standalone documents. Does that split work, or should I pick a different topic?"

### Why it happens

The writer treats the source as an indivisible unit. "Rewrite these notes" is interpreted as "rewrite all of these notes into one document", when the correct interpretation is often "pick the strongest thread and write a document about that". The writer's deference to the source's boundaries produces a piece that inherits the source's lack of focus.

### Detection heuristic

Apply the one-central-idea test from the shared blog-post doctype: can the draft's central argument be stated in a single tweet-length sentence? If not, the draft is trying to do too much. If the source also could not be summarized in a single sentence, the draft has inherited the source's Scope Inflation.

### Defense

In Phase 1, the contamination risk assessment explicitly rates Scope Inflation. When the risk is high, the writer proposes a split before beginning Phase 2. The user either picks one topic for this rewrite, commissions separate documents for the others, or confirms that a broader synthesis is genuinely what they want (rare, and usually a signal that the user needs a status report rather than a technical piece).

---

## 8. Confidence Upgrade

Confidence Upgrade is the mechanism by which hedges in the source — "we think", "probably", "seems to be", "might", "in some cases" — are polished out of the output, turning cautious statements into unsupported assertions. The mechanism is related to Ambiguity Whitewashing but is distinct in an important way: the claims that undergo Confidence Upgrade are often claims the source is hedging for good reason. The writer cannot tell the difference between a hedge that was stylistic padding (safe to remove) and a hedge that was an honest epistemic warning (dangerous to remove), and tends to remove both indiscriminately.

The result is that the rewritten output is *less* factually accurate than the source — the source's hedged version was correct (the writer really did only "think" it was probably true) and the rewrite's confident version is wrong (asserted as true when it is not known to be true). The polish has moved the document backward on the honesty axis while appearing to move it forward on the quality axis.

### Before and after

**Source (a team post-mortem draft):**

> We think the root cause was probably a race condition in the connection pool initialization. The spike in errors seems to correlate with deployments that restart multiple instances in quick succession, though we haven't been able to reproduce it reliably. It's possible other factors are involved.

**Contaminated rewrite (Confidence Upgrade — hedges stripped out):**

> ## Root Cause
>
> The root cause was a race condition in the connection pool initialization. The error spike correlated with deployments that restart multiple instances in quick succession.

The contaminated rewrite has converted three hedges ("we think", "probably", "seems to correlate", "possible other factors") into flat assertions. A reader of the rewrite will take away a definitive root-cause identification. But the source said the team had not reliably reproduced the issue and was not sure other factors were not involved. The rewrite has misrepresented the team's actual epistemic state. In a post-mortem, this is a significant error — post-mortems exist to be honest about what is known and what is not.

**Clean rewrite preserving appropriate uncertainty:**

> ## Suspected root cause
>
> Our working hypothesis is a race condition in connection pool initialization, triggered by deployments that restart multiple instances in quick succession. The evidence: [specific evidence from Fact Register]. We have not reproduced the race under controlled conditions, so we cannot rule out contributing factors — the remediation below is designed to address both the suspected race and two plausible alternative causes we identified during the investigation.

The clean rewrite keeps the uncertainty visible, names it as a "working hypothesis", and describes the evidential state honestly. The reader can calibrate their confidence appropriately. The rewrite is polished — the sentences are well-constructed, the prose is tight — but the epistemic content has been preserved rather than inflated.

### Why it happens

Hedges look like stylistic weakness. A writer trained to tighten prose sees "we think the root cause was probably" as five wasted words, and cuts them. The cut is correct in contexts where the hedges are padding and incorrect in contexts where the hedges are epistemic signals. The only way to tell is to ask whether the writer would be willing to defend the unhedged version in a room of experts, and a rewriter who has not lived through the original investigation cannot answer that question.

### Detection heuristic

For every assertive claim in the draft, locate the corresponding claim in the source. Compare the confidence level. If the source hedged and the draft did not, run the defensive question: "Would the draft's confident version be defensible to an expert audience?" If the answer is no, the draft has Confidence Upgrade and the hedges must be restored.

### Defense

During extraction, transcribe the source's hedges into the Fact Register along with the facts. The KEPT section should record the hedge level: "source claims p99 latency is 180ms [measured]" versus "source claims p99 latency is probably around 180ms [unmeasured estimate, hedged in source]". The writing phase then uses the hedge level to decide whether the output can state the claim flatly or must preserve the uncertainty. Confidence Upgrade is impossible if the hedges are preserved in the Fact Register from the start.

---

## 9. Terminology Drift

Terminology Drift is the mechanism by which inconsistent terminology in the source becomes inconsistent or silently wrong terminology in the output. The source uses a term — say, "service", "component", "module", or a project-specific name — in two or more slightly different ways across its text. The rewriter, working without a disambiguation step, either perpetuates the inconsistency (so the output is as confusing as the source) or silently picks one meaning and uses it throughout (so the claims the source made about a different sense of the term are now wrong).

Terminology Drift is especially common with acronyms, product names, and domain-specific jargon where the same string refers to multiple things. It is also common when sources have been written over long periods and the meanings of terms have evolved — an early paragraph uses "worker" to mean one thing, a later paragraph uses "worker" to mean something else, and the rewriter misses the shift.

### Before and after

**Source (a wiki page written over two years by multiple authors):**

> [Paragraph 1, written in 2023:] Our "worker" processes handle all background jobs.
>
> [Paragraph 3, written in 2024 after an architecture change:] The new "worker" tier is a separate set of machines dedicated to ML inference, with its own scaling model.
>
> [Paragraph 5, written in 2025:] Workers are now configured via the central config service, which controls timeouts, retries, and resource limits.

**Contaminated rewrite (Terminology Drift — silently resolves "worker" to one meaning):**

> Our workers handle both background jobs and ML inference on a dedicated tier of machines. They are configured via the central config service, which controls timeouts, retries, and resource limits for all workers.

The contaminated rewrite has conflated two distinct things — background-job workers and ML inference workers — into a single "workers" entity. The claim about central config may be true of background-job workers and false of ML inference workers, or vice versa. The reader cannot tell. The rewriter has silently changed the meaning of claims from the source without noticing.

**Clean rewrite after Terminology Drift is addressed:**

In extraction, the Fact Register would flag the terminology issue in the AMBIGUOUS section:

> **AMBIGUOUS:**
> - "worker" is used in at least two distinct senses in the source: (a) background-job worker processes, (b) ML inference dedicated machines. Claims made about "worker" need to be disambiguated before being placed in KEPT.

The writer would either ask the user to disambiguate, or (if the distinction is clear from context) split the term: the Fact Register's KEPT section would use "job-worker" and "inference-worker" as unambiguous labels, and the draft would follow suit. The central-config claim would only be associated with whichever worker type it actually applies to.

### Why it happens

Writers scan for content, not for linguistic consistency. When a term appears multiple times, the writer unconsciously treats the appearances as referring to the same thing, even when the text does not warrant that assumption. The bias is strong enough that writers often fail to notice terminology drift even when re-reading their own work.

### Detection heuristic

Build a small glossary of project-specific terms during extraction. For each term, record every sense it is used in across the source, with evidence. Any term with more than one sense is a candidate for Terminology Drift and must be either disambiguated (by renaming or by explicit scope tags) or resolved (by consolidating the senses, if the user confirms they are intended to be the same thing).

### Defense

The AMBIGUOUS section of the Fact Register captures terminology conflicts as they are discovered during extraction. The writing phase is forbidden from drawing on an ambiguous term without a resolution from the user. This prevents the silent collapsing of multiple senses into one.

---

## 10. Pseudoanchor Import

Pseudoanchor Import is the mechanism by which a vague quantitative claim in the source — "handles a lot of traffic", "about a million users", "scales to millions of requests" — becomes a specific-looking number in the output. The number is invented in exactly the sense that it was not measured; it was generated to fill a slot that the polish pass felt should contain a number. The fake anchor is dressed up as a real one, and the reader cannot tell the difference.

Pseudoanchor Import is the most dangerous contamination mechanism in terms of factual accuracy, because the resulting claims look rigorous. A reader who sees "our cache handles 2.3 million requests per second with p99 latency under 8 milliseconds" will take the numbers at face value. A reader who sees "our cache is fast and handles a lot of traffic" will at least know that the author has not provided evidence. The polish has converted a recognizably vague claim into an unrecognizably false one.

### Before and after

**Source (a sales deck):**

> Our platform handles millions of requests with blazing-fast response times.

**Contaminated rewrite (Pseudoanchor Import — invented numbers that look real):**

> Our platform processes 4.2 million requests per second with an average response time of 6ms and p99 latency under 20ms.

The contaminated rewrite has generated three specific-looking numbers (4.2M/sec, 6ms average, p99 under 20ms) that do not appear in the source. The numbers are plausible — they are in the range that a real platform might have — but they were not measured. A reader trusts them because they are specific, and they turn out to be wrong.

**Clean handling:**

The extractor would place the source's claim in the DISCARDED section:

> **DISCARDED:**
> - "handles millions of requests with blazing-fast response times" — no specific numbers, no measurement methodology, no workload description; sales deck tone

In Phase 2, the writer has three options. Option one: scope the output to exclude quantitative claims entirely. Option two: ask the user for real benchmark numbers and include them in KEPT. Option three: mark the performance claim as "unverified" in the draft, with a note that the team has not published benchmarks. Any of these is better than inventing numbers.

### Why it happens

Two pressures combine to produce Pseudoanchor Import. First, vague claims look weak, and the writer wants to improve them. Second, specific numbers are the fastest way to make a claim look strong. The writer's mind fills the gap with plausible numbers without consciously registering that the numbers were not measured. The internal model offers a "reasonable-looking" number; the polish pass accepts it; the number is now in the draft with no trace of its invented origin.

### Detection heuristic

For every specific number in the draft, trace it back to a source in the Fact Register. If the number does not appear in KEPT with a citation, it is a candidate for Pseudoanchor Import. Confirm by asking: where did this number come from? If the answer is "I made it up because it sounded right", cut the number or replace it with a measured value.

### Defense

The KEPT section of the Fact Register records the provenance of every number. A number with no provenance cannot be used in the draft. The writing phase is forbidden from introducing new numbers that were not in KEPT, regardless of how plausible they sound. This rule closes the channel through which Pseudoanchor Import enters the output.

---

## Cross-cutting observations

The ten mechanisms are distinct in what they do, but they share a common cause: the writer reading the source and then writing, without a firewall between the two activities. When the firewall is enforced — when the writer reads only to populate the Fact Register, then closes the source and writes from the register alone — all ten mechanisms are greatly reduced, though not eliminated entirely. Tone Infiltration and Terminology Drift require additional discipline during the writing phase because they are harder to catch during extraction. The other eight are almost entirely defeated by strict extraction.

The contamination risk assessment in `contamination-risk-assessment.md` is the diagnostic tool that makes the mechanisms visible before the writing begins. It forces the extractor to rate the source against each mechanism and name specific evidence, which turns the abstract risk of contamination into a concrete list of defensive moves that must be made in Phase 2.

The rewrite-specific checklist in `rewrite-checklist.md` runs a second detection pass after the draft is complete, catching contamination that slipped through the extraction phase. The two tools — risk assessment before writing, checklist after writing — are designed to work together as a validation loop. A draft that passes the checklist without triggering a revision is rare on the first pass; a draft that passes on the third or fourth pass is normal and is the point at which delivery becomes appropriate.