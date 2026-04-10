# Narrative voices

A narrative voice is a consistent stance — what the writer is doing with the material. Not tone (formal vs casual). Not person (first vs third). Stance.

**Pick one voice per document. Name it in the Anchor Sheet. Hold it for the whole piece.** Voice drift — starting as one voice and sliding into another — is one of the top causes of muddy technical writing, and it is the single most common failure mode in AI-generated drafts.

This file defines six voices. The first four are primary and cover most of the work; the last two are specialized.

---

## 1. Production War Story

**Stance.** "I lived through this incident. The docs said X. The system did Y. Here is why, and here is what you should do differently."

**When to use.** Post-mortems, operational lessons, "the time our cluster fell over" blog posts, retrospectives on a production bug that taught a general lesson.

**Opens with.** A symptom. A concrete moment. A log line. A page. A graph going the wrong way. Never with history.

**Ends with.** A structural lesson — something other teams can apply without having had the same incident.

**Authority comes from.** Specificity of the incident. Exact timestamps, exact error messages, exact graphs, exact config values. The reader should feel they were in the room.

**Forbidden moves.**
- Generic "lessons learned" that could apply to any incident ("monitoring is important").
- Blame narratives. The voice is diagnostic, not accusatory.
- Happy-ending framing ("and now we never have incidents"). Everyone has incidents.

### Before and after

**Generic AI output (no voice):**

> Database connection pools are a critical component of any high-traffic application. When misconfigured, they can lead to performance degradation and outages. In this post, we will explore best practices for configuring connection pools and share some lessons learned from our experience.

**Production War Story:**

> On March 14 at 02:47 UTC our checkout service started returning 503s at about 4% of requests. The on-call graph showed `HikariPool-1` timeout count climbing from a flat 0 to ~200/minute. The pool was sized at 20. Traffic was normal. Nothing had deployed in 9 hours. It took us four hours to find the cause, and the cause was not in our code — it was in how PgBouncer's transaction pooling interacts with Hibernate's `SESSION` scoped `FlushMode`. Here is the chain, and here is why every Hibernate shop on PgBouncer should go check their config right now.

Notice what changed. The second version commits to a specific incident (date, time, numbers, tool names), promises a specific causal chain, and tells the reader immediately why they should care ("every Hibernate shop on PgBouncer should go check their config").

---

## 2. Design Tribunal

**Stance.** "I am sitting in judgment of these options. I will name the alternatives, weigh them against specific criteria, and hand down a verdict. No hedging."

**When to use.** Architecture decisions, ADRs, technology comparisons (X vs Y), "should we adopt Z" pieces, any piece where the output is a recommendation.

**Opens with.** The decision being judged and the criteria. The reader should know in the first paragraph what is being compared and on what axes.

**Ends with.** A verdict. The verdict must name one option as the winner *for this specific context*. The context qualification is crucial — it is how you avoid the "best framework" fallacy. "CockroachDB is the right choice *for our ledger service, given our latency budget and multi-region requirement*" is a verdict. "CockroachDB is a powerful choice worth considering" is not.

**Authority comes from.** The quality of the criteria and the rigor of applying them. A Design Tribunal piece that uses the wrong criteria is worse than one that hedges — it is actively misleading.

**Forbidden moves.**
- "Both have pros and cons." This is the Design Tribunal's cardinal sin. If you cannot pick a winner, either your criteria are wrong or you do not have enough information to write the piece.
- Adjective soup ("X is modern and robust, Y is mature and reliable"). Adjectives are not criteria. Criteria are measurable.
- Listing features without weighing them against the criteria. A feature table is not a Design Tribunal.

### Before and after

**Generic AI output:**

> When choosing between PostgreSQL and MongoDB for your application, there are several factors to consider. PostgreSQL is a mature relational database with strong ACID guarantees and a rich SQL ecosystem. MongoDB is a popular document database that offers flexible schema design and horizontal scalability. Both have their strengths, and the right choice depends on your use case.

**Design Tribunal:**

> We needed a primary data store for the ledger service with three non-negotiable constraints: strict serializable isolation across multi-row updates (regulatory), p99 write latency under 30ms at 2k TPS (product), and a single-writer operational model (team capacity — we are four engineers). Against those three constraints, MongoDB loses on the first. PostgreSQL passes all three, with 6ms headroom on latency. CockroachDB passes the first two and fails the third at our scale — we ran it for six weeks in staging; the operational overhead (distributed backups, zone configs, schema change coordination) would eat 25% of our team's time, which we cannot spend. PostgreSQL wins. We will revisit CockroachDB when the team is larger than eight, or when the multi-region requirement becomes real.

The second version uses three explicit criteria, applies them, and names a winner *plus* the conditions under which the winner would change. That last sentence is what separates a professional judgment from a dogmatic one.

---

## 3. Mechanism Autopsy

**Stance.** "I have opened this thing up. I am going to walk you through the internals. You will see what I see. When I point at a line of code, you will trust that I have read it, because I will give you the path."

**When to use.** Source code deep-dives, protocol analysis, "how X actually works under the hood", kernel or framework internals pieces, performance investigations that end at a specific code path.

**Opens with.** A misconception the reader probably holds, or a surprising observable behavior. Then: "let's find out why".

**Ends with.** A mental model the reader can reuse to predict future behavior of the system — not just understand the specific case.

**Authority comes from.** Specificity at the code level. File paths with line numbers. Function signatures quoted verbatim. Exact version tags. Reproducible commands. The reader should be able to follow your steps on their own machine and land on the same lines.

**Forbidden moves.**
- Summary paragraphs that are not backed by a code reference. If you are claiming behavior, show the code.
- Hand-waving ("under the hood, Spring does some magic"). Magic is the absence of a mechanism. Mechanism Autopsy's entire job is to delete that word.
- Refusing to name version. "Recent versions of Spring" is a tell that the writer did not actually check. Name the version.

### Before and after

**Generic AI output:**

> Spring Boot's auto-configuration is a powerful feature that automatically configures your application based on the dependencies on the classpath. It uses a combination of conditional annotations and configuration classes to determine which beans to create. This magic is enabled by the `@EnableAutoConfiguration` annotation.

**Mechanism Autopsy:**

> Everyone says Spring Boot auto-configuration is "magic". It is not. It is a specific, boring mechanism that lives in two files, and once you have seen it, you can predict exactly what will and will not auto-configure in any given setup.
>
> The entry point is `spring-boot-autoconfigure/src/main/resources/META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` (Spring Boot 3.2.0; earlier versions used `spring.factories`). Open it. It is just a text file with ~140 fully-qualified class names, one per line. Every line in that file is an `@AutoConfiguration` class that Spring will *consider* loading.
>
> The word "consider" is load-bearing. Each of those 140 classes is gated by `@Conditional` annotations — most commonly `@ConditionalOnClass`, `@ConditionalOnMissingBean`, and `@ConditionalOnProperty`. The logic for evaluating these lives in `AutoConfigurationImportSelector.getAutoConfigurationEntries()` at `spring-boot-autoconfigure/src/main/java/org/springframework/boot/autoconfigure/AutoConfigurationImportSelector.java:138`. Let's walk that method...

Notice the move from "magic" to "two files". The Mechanism Autopsy voice exists to do that conversion over and over.

---

## 4. Migration Field Guide

**Stance.** "I have done this migration. I am handing you the map. I will mark every pit I fell into so you do not fall into it."

**When to use.** Upgrade guides, adoption playbooks, "how to move from X to Y" pieces, framework migration write-ups.

**Opens with.** Who should do this migration and who should not. The reader needs to know in 60 seconds whether to keep reading.

**Ends with.** A rollback plan. Every Migration Field Guide ends with "and here is how to undo it if it goes wrong". Pieces that assume the migration will succeed are not field guides, they are marketing.

**Authority comes from.** Having actually done the migration. The tell is the pits — a genuine field guide lists the traps in detail, because the writer walked into them.

**Forbidden moves.**
- Treating the migration as linear. Real migrations fork and back up. The field guide acknowledges this.
- Skipping the "don't do this migration if..." section. Not every reader should migrate. Saying so builds trust.
- Marketing tone ("X is the future, so you should move now"). The reader is migrating for a concrete reason, not because a framework is trendy.

### Before and after

**Generic AI output:**

> Migrating from Spring Boot 2 to Spring Boot 3 is a straightforward process. You will need to update your dependencies, migrate from `javax.*` to `jakarta.*`, and make a few configuration changes. This guide will walk you through the steps.

**Migration Field Guide:**

> Do this migration if: you are on Spring Boot 2.7.x, you are on JDK 17 or can get there, and you have more than three months before your current line goes out of OSS support. Do *not* do this migration if: your app depends on any library that still ships `javax.servlet` types in its public API and has not released a Jakarta-EE-10-compatible version — check your dependency tree before you start. I will show you how in step 1.
>
> The migration has four phases, and the order matters. Phase 2 is where every team I have helped has gotten stuck, and the cause is almost always the same: a transitive dependency on an old `spring-security-oauth2` shim that is no longer published. Phase 4 is where your observability will break in a silent way — the Micrometer registry stays up, but `http.server.requests` loses its `uri` tag unless you explicitly opt in. Both are covered below.
>
> Rollback plan, because you will need it: ... (three paragraphs of actual rollback steps, including the database-side gotchas) ...

The second version commits to pits. That is the voice.

---

## 5. Benchmarker's Notebook (specialized)

**Stance.** "I ran the experiment. Here is the setup, here are the numbers, here are the caveats. Reproduce it yourself if you don't trust me."

**When to use.** Performance comparison pieces, "is X faster than Y" investigations, capacity-planning write-ups. Any piece where the whole point is a quantitative result.

**Opens with.** The question being measured and the specific hypothesis.

**Ends with.** A conclusion *and* a list of conditions under which the result would flip.

**Authority comes from.** Reproducibility. The reader can copy the commands, run them, and land on the same numbers (within noise). The full setup — hardware, OS, JDK version, JVM flags, warmup strategy, measurement window — is listed explicitly.

**Forbidden moves.**
- Reporting a single number without noise characterization. "42ms" is useless; "42ms p99, σ=3ms over 5 runs of 60s each" is a measurement.
- Omitting the setup. "On my laptop" is not a setup.
- Cherry-picking the run that supports the narrative.
- Comparing against a default configuration of the losing side without saying so. If Option B loses only because you used its defaults, that is a relevant caveat.

---

## 6. Reference Librarian (specialized)

**Stance.** "I am not arguing with you. I am telling you what the thing does. Precisely, completely, and in the same shape every time."

**When to use.** Pure API reference. Spec documentation. The "Reference" quadrant in Diátaxis.

**Opens with.** The thing being documented and its signature. No preamble.

**Ends with.** Nothing. Reference material does not conclude. It terminates when the information is complete.

**Authority comes from.** Completeness, consistency, accuracy. Every endpoint has the same sections in the same order. Every type has its fields listed with the same schema. The reader trusts the document because it never surprises them with a missing field or a different layout.

**Forbidden moves.**
- Arguing. The Reference Librarian does not have opinions about the API.
- Tutorial-style prose. "First, you will want to..." is wrong here. The reader is not learning; the reader is looking something up.
- Mixing with explanation. If the reader needs to know *why* the API is designed a certain way, that goes in a separate explanation document. Reference answers *what*, not *why*.

This is the one voice where "just describe what the thing does" is correct, because the reader has come for exactly that.

---

## Voice drift — how to catch it

Drift is what happens when a draft starts as one voice and slides into another. The usual slide is *into* Reference Librarian, because describing things is easier than judging them. A Design Tribunal draft that starts with a crisp verdict statement and then spends 2000 words describing features without weighing them has drifted into Reference Librarian and must be rescued.

Three questions to check for drift, to be run against any draft:

1. **Does the last third of the piece still feel like the voice I picked?** If not, drift.
2. **Would the original voice's "forbidden moves" catch anything in the draft?** If yes, drift.
3. **Is the verdict/lesson/mental-model from the ending still consistent with the stance from the opening?** If not, drift.

The fix for drift is almost never "add a concluding paragraph that restates the argument". The fix is to go back and cut the drifted section, or to commit to the new voice and restart. Half-voice pieces read as muddled even when the reader cannot say why.