# Anti-Patterns Reference

This file documents specific writing patterns that must be avoided. Each entry shows the
problematic pattern, explains why it fails, and provides a correction strategy.

---

## Category 1: AI-Smell Phrases

These phrases appear almost exclusively in AI-generated text. Their presence immediately signals
to a technical reader that the document was produced without genuine thought. Eliminate all of
them.

### The False Hedge
**Pattern:** "It depends on your use case." / "There are trade-offs to consider." /
"Each approach has its pros and cons."

**Why it fails:** This is the AI equivalent of a non-answer. Every engineering decision depends
on context. The reader already knows this. Your job is to enumerate the conditions and reach a
recommendation for each — or at minimum, state the key variable that drives the decision.

**Fix:** "It depends on your connection cardinality. Below 200 concurrent connections, MVC with
virtual threads is simpler and performs equivalently. Above 500 concurrent connections, WebFlux
avoids pool exhaustion entirely. There is no middle ground worth debating."

---

### The Hollow Superlative
**Pattern:** "high performance", "highly scalable", "extremely powerful", "robust solution",
"best practice", "industry-standard"

**Why it fails:** These phrases carry no information. They describe a property without
quantifying it or explaining its mechanism.

**Fix:** Replace with the specific claim: "sustains 10,000 concurrent SSE connections on 4
vCPUs", "throughput degrades by < 3% between 100 and 2,000 concurrent users (benchmarked on
JVM 21, 8GB heap)".

---

### The Obvious Transition
**Pattern:** "In this section, we will explore...", "As we have seen...", "Having covered X,
we now turn to Y...", "It is worth noting that...", "It is important to understand..."

**Why it fails:** These are the written equivalent of a presenter saying "Next slide." They
consume words without conveying anything. Readers can see the section heading.

**Fix:** Begin the section with the substance directly. If you need a transition, make it an
argumentative bridge: state the logical connection between the previous point and this one.

---

### The Fake Balance
**Pattern:** Presenting two options with equal positive and negative framing, then declining to
choose. "Option A is better in some scenarios while Option B excels in others. Both are valid
approaches depending on your requirements."

**Why it fails:** This mimics the structure of an analysis without performing one. Technical
readers read this as "the author has not made a decision."

**Fix:** Make the decision. State the conditions. If genuinely context-dependent: "If your
constraint is X, use A. If your constraint is Y, use B. If you have both constraints, X is
the tiebreaker because [mechanism]."

---

### The Background Stall
**Pattern:** Opening with 3–5 paragraphs of background/history before getting to the argument.
"Microservices emerged in the early 2010s as a response to the limitations of monolithic
architectures..."

**Why it fails:** The reader arrived at this document for a specific reason. They do not need
to be told the history of a technology they are already using. This pattern buries the value
and signals that the author is padding to reach a length target.

**Fix:** State the argument in paragraph one. If background is genuinely needed for the reader
to understand the argument, include one short "Context" block after the opening, labeled as
prerequisite knowledge.

---

### The Rhetorical Question Hook
**Pattern:** "Have you ever wondered why your application slows down under heavy load?",
"Are you struggling to decide between WebFlux and Spring MVC?"

**Why it fails:** This is a cargo-cult of copywriting, imported into technical writing where
it does not belong. It is condescending and wastes the reader's first few seconds.

**Fix:** Name the problem directly. "Thread pool exhaustion is the failure mode that kills most
reactive rewrites — not because reactive programming is wrong, but because engineers port their
thread-per-request assumptions into an event-loop architecture."

---

### The Passive Responsibility Evasion
**Pattern:** "It should be noted...", "Care must be taken...", "Consideration should be given..."

**Why it fails:** This construction removes the agent — the person who must do the noting,
taking, considering. It is grammatically passive in a situation that requires a direct
instruction.

**Fix:** "Note that...", "You must...", "Check whether..." Or restructure as a recommendation:
"Before deploying, verify that your thread pool size matches your expected concurrent connection
count."

---

## Category 2: Structural Anti-Patterns

### The Listicle Collapse
**Pattern:** Converting every analytical section into a bullet list. "Benefits of WebFlux:
• Non-blocking I/O • Event-loop model • Better resource utilization • ..."

**Why it fails:** Lists present items as coordinate — equally important, equivalent in
relationship to the topic. Technical arguments have hierarchy and dependency. Collapsing
reasoning into bullets destroys the logical structure.

**Fix:** Use prose for arguments. Use tables for comparisons. Use lists only for genuinely
enumerable, coordinate items (configuration options, dependency lists, step sequences).

---

### The Unconditional Code Block
**Pattern:** Code examples with only "happy path" implementations and no configuration
context, failure scenario, or rationale for specific choices.

**Why it fails:** Any code that appears in a technical document should teach something a reader
couldn't infer from the official documentation. If it doesn't, cut it or replace it with
something that shows the non-obvious part.

**Fix:** Show the failure case alongside the working case. Document the non-obvious
configuration choice. Add a comment that explains why this specific value, not just what it does.

---

### The Wikipedia Introduction
**Pattern:** "Reactive programming is a programming paradigm oriented around data flows and the
propagation of change. The concept was formalized by..."

**Why it fails:** The reader does not need a definition from you. If they don't know what the
concept is, they should not be reading this document (and you said so in Prerequisite Knowledge).
If they do know, you have wasted their time.

**Fix:** Skip the definition. Open with the mechanism or the argument. "The event loop processes
I/O callbacks on a single thread, which means blocking that thread — even for 1ms — starves all
other connections for the duration of that block."

---

## Category 3: Depth Anti-Patterns

### Mechanism Avoidance
**Pattern:** Describing what something does without explaining how it does it, at a level
that would allow the reader to predict its behavior under non-standard conditions.

**Example:** "Virtual threads are lightweight threads managed by the JVM. They allow you to
write blocking-style code without consuming a platform thread."

**Why it fails:** This tells the reader what to use and what to expect, but not why the system
behaves this way. They cannot reason about failure modes, edge cases, or interactions with other
systems.

**Fix:** "Virtual threads park on blocking operations by yielding their carrier platform thread
back to the scheduler pool. This means that at any moment, N virtual threads can be 'alive'
while only M carrier threads (M << N) are actually scheduled — the JVM's scheduler queues
continuations, not threads, in the classic sense. The implication: blocking a virtual thread is
cheap. Blocking its carrier thread (e.g., via a synchronized block holding a monitor) pins it
and reintroduces the original problem."

---

### The Missing Failure Mode
**Pattern:** Describing an architecture or approach without covering what happens when it fails.

**Why it fails:** Production systems fail. An engineer who has implemented your recommendation
without understanding its failure modes will be debugging blind at 3am.

**Fix:** For every architectural recommendation, answer: "What does failure look like? How does
it manifest in metrics or logs? What is the recovery path?" This does not need to be a long
section — two to four sentences per failure mode is sufficient.

---

### The Unexplained Diagram
**Pattern:** Sequence or architecture diagrams that are self-explanatory at the surface level
but contain one or more elements that appear for structural reasons the reader would not infer.

**Fix:** Always follow a diagram with at least one sentence pointing to the least obvious
design element: "Note that the retry loop bypasses the circuit breaker — this is intentional.
A circuit breaker that trips on retried-timeout errors would amplify cascading failure rather
than containing it."

---

## Category 4: Chinese-Specific Anti-Patterns

### 过度客套开场 (Excessive Formality in Opening)
**Pattern:** "随着云原生技术的蓬勃发展，越来越多的企业开始关注..." / "在当今数字化转型的大背景下..."

**Why it fails:** This is the Chinese technical writing equivalent of the Wikipedia Introduction.
It delays the argument and signals that the author is filling space.

**Fix:** 直接进入论点。第一段应该描述具体的技术张力或失败场景，不应以宏观趋势铺垫。

---

### 翻译腔 (Translation Register Leakage)
**Pattern:** Sentence structure that feels like a translated English technical document.
"它提供了一种非阻塞的方式来处理I/O操作，这使得它在高并发场景下具有显著优势。"

**Why it fails:** This is grammatically correct Chinese but reads as translated. The
`它...这使得它` construction is symptomatic.

**Fix:** 用工程师向同事解释问题的方式写。"核心原因是线程不是免费的——一个平台线程的默认栈大小是 1MB，
开 1000 个就是 1GB 堆外内存，还没开始做任何业务逻辑。"

---

### 结论埋底 (Buried Conclusion)
**Pattern:** Chinese rhetoric traditionally builds to a conclusion. Technical writing must not.

**Fix:** 结论放在第一段，证据放在后面。读者在第 30 秒内就应该知道你的核心观点。