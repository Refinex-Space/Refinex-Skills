# Quality checklist

Run this checklist against every draft before delivering it to the user. It is an **executable loop**, not a guideline. For each gate, actually read the draft and verify; do not merely "consider" the gate. When a gate fails, fix the draft and re-run the checklist from the top — fixes often create new failures elsewhere.

A first draft will typically fail two to four gates. That is expected. The loop is the point.

---

## Gate 0 — The Anchor Sheet exists and is honest

Before anything else, look at the Anchor Sheet from Phase 1. If it is thin — if the argument is actually a topic, the anchors are adjectives, the rejected alternatives are empty — **go back to Phase 1**. Do not try to fix a thin-anchor draft with prose polishing. It will not work.

- [ ] Central argument is one falsifiable sentence, not a topic.
- [ ] At least three concrete numbers are present in the anchors (or the piece is explicitly non-quantitative and the user has confirmed this).
- [ ] At least one rejected alternative is named with a specific reason, for any piece that makes a design recommendation.
- [ ] Any mechanism-, topology-, state-, or timeline-heavy section has an explicit visual plan when prose alone would overload the reader.
- [ ] Reader audit names one reader type, not two.
- [ ] Voice is named and matches the document type.

If any of these fails, stop the validation loop and return to Phase 1.

---

## Gate 1 — Title carries the argument

The title states the claim, not the topic.

- [ ] The title is not a noun phrase like "Spring AI ChatClient 实战" or "Understanding Kubernetes Networking".
- [ ] The title tells the reader what they will *learn* or what claim will be *proved*, not what will be *discussed*.
- [ ] The title makes one clean claim. If it is trying to hold thesis, teaser, metaphor, and payoff at the same time, it is probably overloaded and should be shortened.
- [ ] If the title contains "guide", "overview", "introduction to", or "exploring", justify it or change it. Those words are acceptable only in tutorials and reference material; for blog posts, comparisons, and deep-dives they are usually a tell.

**Fix pattern.** Take the Anchor Sheet's central argument and compress it into one clean claim. If the compressed title loses the edge, the title is too bland — try again with a sharper verb. If the title reads like a mini-outline, the title is too crowded — cut the second claim and keep the load-bearing one.

---

## Gate 2 — Header info block present

Every piece (except pure Reference Librarian documents) has a short header block that tells the reader the scope, the prior knowledge assumed, and the central argument. It is usually two or three short sentences or a small table at the top.

- [ ] Reader can tell from the first 30 seconds: who this is for, what they should already know, and what the piece will claim.
- [ ] For ADRs and design docs, the header includes status, date, and authors.
- [ ] For blog posts and deep-dives, the header can be prose, but it must exist and must be concrete.

---

## Gate 3 — 60-second rule

A reader who stops after one minute should still know what the piece is claiming.

- [ ] The central argument (or a direct paraphrase) appears in the opening paragraph.
- [ ] The opening does not begin with history ("In recent years, as AI has become..."), with a definition ("X is a framework for..."), or with a restatement of the question ("How should we choose between X and Y?").
- [ ] The opening does not contain the words "comprehensive", "in-depth exploration", "dive deep into", or "everything you need to know".

**Fix pattern.** If the opening fails, the usual cause is that the writer did not believe the argument enough to lead with it. Cut the first two paragraphs. The third paragraph is usually the real opening.

---

## Gate 4 — Every comparison ends with a verdict

Any section that compares two or more options must conclude with a named winner and the conditions under which the winner holds.

- [ ] No section ends with "both have pros and cons", "it depends on your use case", or "the right choice varies".
- [ ] Where the piece genuinely recommends neither option, it says so explicitly — "neither of these fits our constraints; we built a third thing, and here is why" — rather than hedging.
- [ ] The winner is qualified with context ("for our ledger service, given the 30ms p99 budget"), not stated as universal.

**Fix pattern.** If a comparison cannot be given a verdict, one of two things is true: (a) the criteria are wrong (too abstract, or missing), or (b) the writer does not have enough information to decide. Either fix the criteria or go back to Phase 1.

---

## Gate 5 — Every design decision lists rejected alternatives

For each significant decision in the piece, at least two alternatives were named and set aside with specific reasons.

- [ ] "Specific reason" means it names a concrete failure mode or cost, not an adjective. "Too slow" fails this gate; "too slow because the cold-start path dominates our p99 at 2.1s" passes.
- [ ] "We considered X" followed by no actual engagement with X does not count. The engagement must be visible.
- [ ] The rejected alternatives are not strawmen. If a reader with the rejected option's perspective would recognize themselves in the description, the rejection is honest. If not, it is a strawman and must be rewritten or removed.

---

## Gate 6 — Failure modes are mechanisms, not categories

Any claim about how something fails must describe a causal chain, not a category.

- [ ] No sentences of the form "this can fail under load", "this is prone to errors", "this has performance issues". These are category-labels, not mechanisms.
- [ ] Every failure claim names: the triggering condition, the internal behavior that causes the failure, and the observable symptom.
- [ ] If the mechanism spans multiple actors, time steps, states, or branches, the draft uses the best-fit Mermaid diagram rather than forcing prose to carry the full load alone.
- [ ] Where a mechanism is not known, the piece says "we did not determine the root cause" rather than guessing. Honesty beats speculation.

**Fix pattern.** For every failure claim, ask "could I draw this as a flowchart?" If not, it is not a mechanism yet. Either dig deeper or soften the claim.

---

## Gate 7 — Limitations section with concrete boundaries

Every piece that makes a technical recommendation has a limitations section, and the limitations are quantitative where possible.

- [ ] The piece says "this approach works up to X, beyond which Y happens" at least once.
- [ ] The limitations section is not a generic "your mileage may vary" paragraph. It names the conditions under which the recommendation stops holding.
- [ ] If the piece claims a performance improvement, the limitations section specifies the workload shape under which the improvement exists (and, ideally, where it disappears).

---

## Gate 8 — The senior-engineer test

For every section of the piece, apply this test: **would a senior engineer in this domain learn something from this section that they could not get from skimming the official docs for five minutes?**

- [ ] Every section passes. Sections that do not pass are either deepened (add the insight that makes them worth reading) or deleted.
- [ ] The test is applied *per section*, not to the piece as a whole. A piece can have a great central insight and still waste the reader's time with padding sections; those sections must go.
- [ ] Every load-bearing item from the Anchor Sheet is discharged in the body. If the opening promises three mechanisms, the body actually proves three mechanisms.
- [ ] There is no third option between "deepen" and "cut". "Leave it in as background" is not permitted — background that does not teach is padding.

This is the sharpest gate in the checklist. It will cut a lot. Let it.

---

## Gate 9 — Anti-patterns swept

Run the anti-pattern catalog in `anti-patterns.md` against the draft. Every match must be fixed or deliberately accepted. "Deliberately accepted" means you can defend the specific instance; it does not mean "I'm tired and don't want to fix it".

- [ ] No false balance ("both have pros and cons", "there's no right answer", "ultimately it depends").
- [ ] No empty superlatives ("powerful", "robust", "cutting-edge", "elegant", "seamless", "world-class", "industry-leading").
- [ ] No background stuffing (multiple paragraphs of history or definition before the real content starts).
- [ ] No passive responsibility avoidance ("mistakes were made", "the system failed to...").
- [ ] No hedge stacking ("it might potentially be possible that, in some cases, this could perhaps...").
- [ ] No Wikipedia-voice opening ("X is a Y that was created in Z by...").
- [ ] No restating-the-question opening ("How do you choose between A and B? That's a great question.").
- [ ] No "comprehensive guide" framing.
- [ ] No bullet-points-instead-of-prose sections, where a paragraph was needed but bullets were used to avoid having to make the argument flow.

See `anti-patterns.md` for the full catalog and detection heuristics.

---

## Gate 10 — Language conventions

For Chinese output:

- [ ] Technical terms (class names, method names, config keys, CLI flags, protocol names, library names, HTTP status codes, error codes) are kept in English.
- [ ] No machine-translated technical terms (no "弹簧 AI", no "聊天客户端").
- [ ] Chinese and English are separated by a space in prose (`Spring AI 的 ChatClient`, not `Spring AI的ChatClient`).
- [ ] Punctuation is Chinese in Chinese prose and English in English quotations and code.
- [ ] Tone is senior-engineer-to-peer, not tutorial voice ("让我们一起来看看" / "接下来,我们将..." / "小伙伴们" are all wrong).

For English output:

- [ ] Anglo-Saxon vocabulary is preferred over Latinate where both work ("use" over "utilize", "start" over "commence", "help" over "facilitate", "show" over "demonstrate", "try" over "attempt").
- [ ] Active voice is the default; passive voice is used only where the actor is genuinely unknown or irrelevant.
- [ ] Present tense for behavior ("`ChatClient` sends a request", not "will send").
- [ ] Precision beats concision. If the precise sentence is longer, ship the precise sentence.

See `language-conventions.md` for the full rules.

---

## Gate 11 — The "so what" test

Read the last paragraph of the piece. Now read only the opening and the last paragraph, skipping everything in between.

- [ ] The last paragraph pays off the opening's claim. The reader who only read the opening and the ending gets a complete, if compressed, argument.
- [ ] The last paragraph does not restate the opening verbatim (that is a concession that the middle taught nothing). It states the opening's claim *with the weight of what the middle proved*.
- [ ] No load-bearing promise from the opening or header is left unresolved by the time the ending arrives.
- [ ] The last paragraph is not a recap. Recaps are for readers who stopped paying attention; pieces that earn the reader's attention do not need them.

A piece that fails this gate usually has a strong opening, a strong middle, and a weak ending — the writer ran out of steam. The fix is to write a real ending that takes responsibility for the argument.

---

## Gate 12 — Document-type-specific gates

Open the reference file for the document type and run its specific gates at the bottom of that file. Each doc type has extras:

- **Blog post**: check the hook, the single-central-idea rule, the ending move.
- **ADR**: check the five required sections (Title/Status/Context/Decision/Consequences), the superseded-link discipline, and the "we will" voice in the Decision section.
- **Design doc**: check goals/non-goals, alternatives-considered, cross-cutting concerns, and the reviewer-audience rule.
- **Comparison**: check the explicit criteria list, the per-criterion verdict, and the "conditions under which the winner flips" statement.
- **Deep-dive**: check that every code claim is anchored to a path/line/version, and that the piece ends on a reusable mental model rather than a summary.
- **API doc**: check endpoint consistency, error exhaustiveness, and the working-example rule.
- **Migration guide**: check the "don't do this if" section, the pit list, and the rollback plan.

---

## Running the loop

1. Read the draft top to bottom once, fast, making notes in the margin. No fixes yet.
2. Go through Gates 0–12 in order. For each one, mark PASS or FAIL with a one-line note on why.
3. Fix all FAILs, starting with Gate 0 (if it failed, stop and go back to Phase 1) and working down. Low-numbered gates often implicate higher-numbered ones; fixing a weak Gate 1 title sometimes forces a rewrite that fixes Gate 3 for free.
4. Re-run the full loop on the fixed draft. If all gates pass, deliver. If any gate newly fails, fix and re-run.
5. Stop after the draft has passed the full loop once cleanly. Do not over-polish — the gates are calibrated for the point at which further revision stops helping. Length is not a stopping condition; gate completion is.

A strong draft passes the loop on the second or third pass. A weak draft reveals the weakness during the first pass and triggers a return to Phase 1, which is expensive but correct.

If you find yourself unable to make the draft pass a gate without inventing content, **stop and tell the user**. "Gate 7 requires a concrete limitations boundary, and I don't have the data to name one. Can you confirm where the approach stops holding, or should I soften the recommendation?" That is the right move. Inventing boundaries to pass the gate is worse than failing the gate.
