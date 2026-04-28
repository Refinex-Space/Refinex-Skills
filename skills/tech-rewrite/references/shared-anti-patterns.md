# Anti-patterns

A catalog of AI-scented and generally-bad patterns in technical writing. Each entry has a name, a description, an example, the underlying cause, and a detection heuristic you can run mechanically against a draft.

These are the patterns the quality checklist sweeps for in Gate 9. This file is the reference for what the sweep is looking for.

---

## 1. False balance

**What it is.** Presenting two options as roughly equal when the writer is either (a) genuinely unable to pick a winner because the anchors are thin, or (b) avoiding picking a winner because picking one feels impolite.

**Example.** "PostgreSQL and MongoDB both have their strengths. PostgreSQL offers strong ACID guarantees, while MongoDB provides flexible schema design. Ultimately, the right choice depends on your specific use case."

**Cause.** Almost always a missing or weak Anchor Sheet. If the writer had concrete criteria, the comparison would produce a verdict for those criteria. False balance is a symptom of "I have no criteria".

**Detection.** Search the draft for: "both have", "pros and cons", "it depends", "ultimately, the right choice", "varies based on", "no one-size-fits-all", "each has its merits". Any hit is a candidate. Confirm by checking whether the surrounding paragraphs name specific criteria and apply them; if not, it is false balance.

**Fix.** Return to the Anchor Sheet and name the criteria. Then apply them. If they cannot be applied because the user has not specified a context, ask the user: "For which context are we comparing these?"

---

## 2. Empty superlatives

**What it is.** Adjectives that promise a lot and deliver nothing. They function as signals of enthusiasm rather than statements of fact.

**Examples.** "powerful", "robust", "cutting-edge", "elegant", "seamless", "world-class", "industry-leading", "state-of-the-art", "battle-tested", "production-grade" (without context), "performant", "lightning-fast", "rock-solid".

**Cause.** Writing that has no measurements reaches for adjectives to feel substantial.

**Detection.** Grep for the words above. For each hit, ask: "what number would change if the opposite adjective were true?" If no number would change, the adjective is empty and should be cut or replaced.

**Fix.** Replace with a number, a mechanism, or a specific behavior. "Powerful" → "supports streaming tool-call with per-turn interception". "Robust" → "recovers from network partition within 200ms with at most one dropped message". If you cannot replace, the claim is probably untrue.

---

## 3. Background stuffing

**What it is.** Multiple paragraphs of context, history, or definition before the piece's actual claim appears. The writer is warming up in public.

**Example.** A blog post about a specific Spring AI bug that opens with three paragraphs on the history of AI, the rise of LLMs, the emergence of frameworks like LangChain, and the introduction of Spring AI, before finally getting to the bug on paragraph four.

**Cause.** Writer nervousness, or a belief that "context sets the stage". It does not set the stage; it delays the piece. The stage is set by the argument itself.

**Detection.** Read the first three paragraphs. If the central argument is not in them, background stuffing is present. Alternatively, count sentences until the first concrete claim. More than six is a smell; more than ten is a failure.

**Fix.** Cut until the first paragraph *is* the first claim. Context that the reader actually needs can appear later, woven in at the point of use, where it is relevant rather than prefatory.

---

## 4. Passive responsibility avoidance

**What it is.** Using passive voice or abstract subjects to avoid naming who did what. Common in post-mortems and in contexts where the writer is uncomfortable with the truth.

**Examples.**
- "Mistakes were made." (Who made them?)
- "The system failed to properly validate inputs." (Did the system write itself?)
- "It was determined that..." (By whom?)
- "An oversight in the deployment process led to..." (The deployment process is not a person.)

**Cause.** Social discomfort with assigning responsibility, or inherited style from corporate communications.

**Detection.** Search for passive constructions with vague or absent agents: "was decided", "was determined", "led to", "resulted in", "failed to". For each, ask "who is the subject?" If the answer is "the system" or "the process" or nobody, rewrite.

**Fix.** Name the agent. "We did not validate the input format on POST /orders before hashing it, and that caused..." The piece immediately becomes more honest and more useful — the reader learns what an actual human overlooked, which is actionable.

In a Production War Story the voice is specifically diagnostic, not accusatory. "We did not validate X" is diagnostic. "Bob did not validate X" is accusatory and almost always wrong for a public piece. The point is to name the action, not the person.

---

## 5. Hedge stacking

**What it is.** Multiple hedging words stacked on a single claim, each one reducing the claim's force until nothing is left.

**Example.** "It might potentially be possible that, in some cases, this approach could perhaps lead to improved performance under certain conditions."

**Cause.** The writer is afraid of being wrong, so they hedge. The hedges compound and destroy the claim.

**Detection.** Search for: "might", "may", "could", "potentially", "possibly", "perhaps", "in some cases", "under certain conditions", "generally", "typically", "tends to", "sometimes", "often". A sentence with more than one hedge is a candidate. A sentence with three or more is a failure.

**Fix.** Pick the strongest hedge the evidence supports and drop the rest. Or, better: replace the hedges with a specific condition. "This approach improves p99 by ~30% *when the cache hit rate is above 80%*" is stronger than any hedged version, and it is honest about the boundary.

---

## 6. Wikipedia-voice opening

**What it is.** Opening with a definition in the "X is a Y that was created in Z by W" pattern. It treats the piece as if it were an encyclopedia entry.

**Example.** "Kubernetes is an open-source container orchestration platform that was originally developed by Google and released in 2014. It is now maintained by the Cloud Native Computing Foundation..."

**Cause.** Default model behavior when the writer has no argument and is reaching for a familiar shape.

**Detection.** Does the first sentence follow "<Topic> is a <category> that <passive history>"? If yes, this is Wikipedia voice.

**Fix.** Replace with the argument. The reader can look up what Kubernetes is elsewhere; the reader came here because your piece promised something Wikipedia does not have.

---

## 7. Restating the question

**What it is.** The opening paragraph echoes the reader's (or the writer's own) question as if to prove it is a legitimate question to ask. It is the prose equivalent of throat-clearing.

**Example.** "When it comes to choosing a database for your application, there are many factors to consider. How do you decide between PostgreSQL and MongoDB? This is a question many engineers grapple with. In this post, we will explore..."

**Cause.** Default opening pattern for essays in high school. It has no place in technical writing.

**Detection.** The opening paragraph contains any variant of: "when it comes to", "this is a question many", "in this post we will explore", "we will dive into", "many engineers wonder". All of these are throat-clearing.

**Fix.** Cut everything before the first real claim. If the first real claim is in paragraph three, delete paragraphs one and two.

---

## 8. "Comprehensive guide" framing

**What it is.** The piece positions itself as an exhaustive treatment of a topic. Titles contain "comprehensive", "complete", "ultimate", "everything you need to know", "the definitive guide to". Almost always a lie, and almost always a tell that the piece has no sharp argument.

**Cause.** The writer is afraid the reader will bounce if the piece is narrow. This is backwards — readers bounce from comprehensive guides because they cannot find the specific thing they came for. Narrow, argued pieces retain readers because the reader can tell in 30 seconds whether the piece is for them.

**Detection.** Title or opening contains one of the flag words above.

**Fix.** Pick one specific claim from the "comprehensive guide" and make that the piece. Use the rest of the material for future pieces. It is almost always better to have ten sharp 1500-word pieces than one bloated 15,000-word comprehensive guide.

---

## 9. Title theater

**What it is.** A title that tries to perform depth by becoming a sentence, a contrast, a teaser, and a mini-outline at once. It often uses `不是 X，而是 Y`, `先 X，再 Y`, `从 X 到 Y`, `把 X 变成 Y`, arrows, stacked punctuation, or a clever metaphor.

**Examples.**
- `配置优先级不是记忆题，而是 ConfigData 构建出的搜索路径`
- `穿透 Servlet Web：从端口监听到错误响应都能解释`
- `ChatClient → AdvisorChain → ChatModel 三层夹心——你的第一次 API 调用背后发生了什么`

**Cause.** Misreading "title should carry an argument" as "title should contain the whole argument". The result sounds generated because the prose is trying to prove seriousness before the article starts.

**Detection.** If the title needs more than one clause, more than one punctuation mark, or a rhetorical contrast to work, it is a candidate. If it would look silly in a sober table of contents next to `事务边界`, `配置绑定`, or `GC 日志`, rewrite it.

**Fix.** Compress the visible title to a precise editorial label, then move the full claim into the opening paragraph or header block. `配置优先级` is the title; `配置优先级不是记忆题，而是 ConfigData 构建出的搜索路径` is the opening claim.

---

## 10. Bullet-point avoidance of prose

**What it is.** Using bullet lists to avoid having to write an actual argumentative paragraph. Bullets are great for genuinely list-shaped content (steps, options, enumerations); they are poison for argument, because an argument is a flow between ideas and bullets break the flow.

**Example.** A "comparison" section that is three bullet lists stacked on top of each other ("Pros of X: ...; Cons of X: ...; Pros of Y: ..."), with no connective prose. The writer has avoided the work of weighing the options against each other; they have merely laid them side by side.

**Cause.** Bullets feel "structured" and "organized" to write. But the structure is fake — the work of argumentation has been skipped.

**Detection.** Count the ratio of prose paragraphs to bullet blocks in the piece. If bullets dominate, and any of the bullet blocks contain arguments rather than enumerations, this is the pattern.

**Fix.** For any bullet block that carries an argument, rewrite as prose. Bullets stay only for material that is genuinely list-shaped: step-by-step instructions, option enumerations, field definitions, configuration references. If the content is "first this, then that, because of this" — that is prose, not bullets.

ADRs and design documents are exceptions: they can use more lists because parts of them (goals, non-goals, alternatives) are genuinely enumerative. But even in those, the Context, Decision, and Consequences sections should be prose.

---

## 11. Encyclopedic drift

**What it is.** The piece is shaped like an encyclopedia entry on its topic: what it is, its history, its major features, its usage, its ecosystem. The piece describes without judging. There is no argument; there is only description.

**Cause.** The main failure mode this skill fights. The writer did not gather enough concrete anchors to have an opinion, so the draft slides into comprehensive description as a substitute.

**Detection.** For each section, ask: "what claim does this section make?" If the answer is "none, it just describes", that is encyclopedic drift. A whole piece that fails this test is a piece that should be thrown out and restarted from Phase 1, not edited.

**Fix.** Return to the Anchor Sheet. The Anchor Sheet is almost certainly thin. Strengthen the central argument, gather real numbers, and the encyclopedic drift will not recur on the rewrite.

---

## 12. Missing rejected alternatives

**What it is.** A design piece that names a chosen solution but does not say what was rejected or why. The reader has no way to calibrate whether the choice was thoughtful.

**Cause.** Laziness, or the writer never actually considered alternatives and is retroactively justifying a default choice.

**Detection.** For every design recommendation, look for "we considered X but chose not to because Y". If absent, the gate fails.

**Fix.** Name at least two alternatives and give specific reasons for rejecting each. If you cannot, you do not yet have a position worth publishing — go back to Phase 1.

---

## 13. "Under the hood, magic happens"

**What it is.** The writer gestures at internals without actually explaining them. "Under the hood, Spring does some magic to wire everything together." Magic is the absence of a mechanism; writing "magic" is the writer telling you they did not look.

**Detection.** Search for: "under the hood", "magic", "magically", "behind the scenes", "somehow", "automatically handles", "just works". Each one is a candidate for investigation.

**Fix.** If the piece is in Mechanism Autopsy voice, open the actual source and replace the hand-wave with a file path and a function name. If the piece is in a different voice and genuinely does not need the mechanism, cut the hand-wave sentence entirely — the reader does not need to be told that something is magic.

---

## 14. Tutorial voice in a non-tutorial piece

**What it is.** "Let's dive in!", "Now we will explore...", "As you can see...", "Let's take a look at...", "Don't worry — we'll cover that in the next section!". These are tutorial cues. They belong in tutorials. They do not belong in blog posts, ADRs, design docs, deep-dives, or reference material.

**Cause.** Default model behavior, or imitation of bad online tutorials.

**Detection.** Search for "let's", "we will explore", "dive in", "take a look", "as you can see", "don't worry". Every hit is suspect.

**Fix.** Cut. Tutorial voice is conversational filler; the argumentative piece does not need it. A blog post does not walk the reader somewhere; it makes a claim and backs it up.

---

## 15. The restating conclusion

**What it is.** The final paragraph restates the opening paragraph in slightly different words. It is there because the writer was taught that "a good essay has an introduction, body, and conclusion", and the conclusion slot must be filled.

**Example.** Opening: "We migrated from MySQL to Postgres and learned three things about connection pooling." Closing: "In this post, we discussed our migration from MySQL to Postgres and the three things we learned about connection pooling."

**Cause.** Muscle memory from essay writing. It is worse than useless — it signals to the reader that the middle taught nothing, because the ending had to restate the opening.

**Detection.** Compare the opening and closing paragraphs. If the closing could be produced by lightly rewording the opening, the piece has a restating conclusion.

**Fix.** Replace the closing with something only a reader who got through the middle could understand. The closing should carry the *weight* of the middle — the mental model, the structural lesson, the verdict — not the words of the opening.

---

## 16. "In this post" / "In this article"

**What it is.** A meta-reference to the piece itself. It almost always marks a sentence that is saying nothing. "In this post, we will explore Spring AI's ChatClient" is an announcement, not content.

**Detection.** Search for "in this post", "in this article", "throughout this guide", "we will examine", "this piece will cover".

**Fix.** Delete the meta-reference and replace with the actual content. Not "In this post, we will explore why X is broken", but "X is broken, and here is why". The reader knows they are in a post; you do not need to tell them.

---

## 17. Bullet-list tabulation of tradeoffs without synthesis

**What it is.** A "tradeoffs" section that consists of a bullet list of good things and a bullet list of bad things, with no synthesis step that weighs them against each other.

**Example.** "Advantages: fast, mature, widely supported. Disadvantages: verbose, steep learning curve, limited async support." This is a list, not an analysis. It is the writer refusing to do the work of weighing.

**Fix.** The tradeoff only matters *relative to the criteria*. Go back to the criteria and say: "given that our priorities are latency and async support, the async limitation costs us more than the verbosity costs us, so on balance we reject this option."

---

## 18. Present-tense-about-the-future

**What it is.** Writing "Spring AI *provides* tool-call support" when what you mean is "Spring AI *plans to provide* tool-call support in a future version". The reader walks away believing the feature exists.

**Cause.** Reading roadmaps and forgetting that the roadmap is not the product.

**Detection.** Any claim about a feature that you cannot, right now, point to in a released version. Check the version numbers in the Anchor Sheet.

**Fix.** Be explicit: "As of Spring AI 1.0.0-M6, tool-call is supported for OpenAI only; Anthropic support is on the roadmap for 1.0.0-RC2 but not yet released at the time of writing."

---

## 19. "Best practices" without a context

**What it is.** Writing "best practices" as if they were universal. They are not. A best practice is the solution to a specific class of problem in a specific context; stripped of context, it becomes a platitude.

**Example.** "Best practice: always use connection pooling." In what context? For what load? With what pool sizing? Against what failure mode? Without the context, this is a platitude.

**Fix.** Replace with a specific recommendation tied to a specific context. "For a web service with >50 RPS against a relational database, configure HikariCP with `maximumPoolSize` ≤ `(core_count_of_db * 2) + effective_spindle_count`, and monitor the pool's `PendingConnections` metric — climbing values there are a leading indicator of the pool running out of headroom under load."

---

## 20. Invented precision

**What it is.** Specific-looking numbers that are not actually measured — they are vibes dressed up as measurements. "This improves latency by 37%." From where? Measured how?

**Cause.** The writer knows "specific numbers good" but has not actually measured. The numbers are a performance of rigor rather than rigor itself.

**Detection.** For every number in the piece, ask: "where did this number come from, and could the reader reproduce it?" If the answer is "I made it up because it sounded right", cut the number.

**Fix.** Either measure and cite, or replace with honest qualitative language. "Noticeably faster in our internal benchmarks; we have not published the methodology yet" is better than a fake 37%.

This anti-pattern is particularly insidious because it looks like the opposite of "empty superlatives". But invented numbers are worse than empty adjectives — at least adjectives signal their own vagueness. Fake numbers pretend to be measurements.

---

## 21. The senior-engineer-insulting paragraph

**What it is.** A paragraph that explains something every member of the target audience already knows. "A database is a system for storing and retrieving data. There are two main types: relational and non-relational." If the piece is for engineers, every one of them knows this, and the paragraph is insulting to their time.

**Cause.** The writer is unsure of the reader and defaults to defining terms. A good reader audit (Phase 1, step 3) makes this impossible.

**Detection.** For each definitional paragraph, ask: "would my reader, as specified in the Anchor Sheet, already know this?" If yes, cut the paragraph.

**Fix.** Cut. The reader audit is what lets you cut — it is the authorization slip for deleting basic material.

---

## How to sweep

The easy way: grep the draft for the detection keywords in each entry. Fast to run, catches 60%.

The hard way: read the draft slowly, in one pass, with this catalog in hand, asking "which of these is this paragraph doing?" Catches the structural patterns (encyclopedic drift, missing rejected alternatives, the restating conclusion) that grep cannot see.

Do both. The sweep is the last thing between a weak draft and a strong one, and it is the cheapest step in the whole skill — a strong pre-writing protocol followed by a strong sweep produces pieces that require almost no further editing.
