# Contamination Patterns Reference

This file documents the specific mechanisms by which source material contaminates a
reconstructed document. Each pattern has a name, a description of the mechanism, signals
to detect it, and a concrete countermeasure.

These patterns are distinct from the anti-patterns in `tech-writing/references/anti-patterns.md`,
which covers bad writing choices. These patterns cover how *good* writing intent gets corrupted
by *bad* source material. Load both files when doing quality gates on reconstructed documents.

---

## Pattern 1: Structural Mirroring

**Mechanism:** The model sees the source organized as Section A → B → C → D and reproduces
that sequence, because the source's sequence was the most recently processed structure. The
model's prior for "what comes next" is set by the source, not by the reader's learning curve.

**Detection signals:**
- The output's section order roughly matches the source's section order.
- The output opens with the same type of content the source opens with (background, history,
  definitions) rather than with the argument.
- Sections that were thin in the source are thin in the output; sections that were padded in
  the source are padded in the output.

**Countermeasure:** After completing the annotated outline in Phase 1 Step 1.3, compare it
against the source's structure. If more than two sections appear in the same position as the
source, it is likely mirroring has occurred. Ask: "What order would maximize comprehension for
a reader who knows nothing about this source?" Rebuild from that question.

**Test:** Cover the source. Could you justify this section order purely by the reader's
learning curve? If any section's position requires "because the source had it here" as a
justification, move it.

---

## Pattern 2: Void Inheritance

**Mechanism:** The source glosses over a topic (failure modes, rationale, mechanism details).
The model also glosses over it — not because it lacks knowledge, but because the source
provided no scaffolding for that section. In a long reconstruction, the model's attention
shifts toward generating text that coheres with what came before it. Where the source was
thin, the model's generation budget drifts to other sections.

**Detection signals:**
- A section exists in the output but is noticeably shorter and less specific than adjacent
  sections, without a clear reason.
- The failure modes section (if present) is one paragraph while mechanism sections are four.
- A design decision is stated in one sentence with no alternatives discussed.

**Countermeasure:** Use the Gap Inventory from Phase 0 Step 0.2. Before writing each section,
check whether it was identified as a gap. If so, that section should receive proportionally
*more* development than the source gave it, not less. The gap is a writing obligation, not
an absence to be reproduced.

**Test:** Rank the output's sections by word count. If the ranking correlates with the source's
implicit emphasis, void inheritance has occurred. Depth should be determined by the topic's
complexity and the reader's need, not by the source's attention distribution.

---

## Pattern 3: Vagueness Laundering

**Mechanism:** The source contains a vague claim ("the system is highly scalable"). The model
cannot verify this claim, so it does not substantiate it. But it also does not drop it,
because dropping a claim feels like a larger intervention than rewriting it. The result is
the claim reproduced in cleaner prose: "The architecture enables horizontal scaling."

The information content of this output sentence is identical to the source: zero. The only
change is surface quality, which makes the problem harder to detect because the output
looks better than the source.

**Detection signals:**
- Claims about performance, scalability, reliability, or security without numeric bounds
  or mechanism explanations.
- Comparative claims ("more efficient than", "better suited for") without the comparison
  baseline stated.
- "Designed for" or "optimized for" without stating what specifically was designed or optimized.

**Countermeasure:** For every claim in the output about a system property (performance,
scale, reliability, fault tolerance), ask: "Could I predict the system's behavior under
specific conditions from this sentence?" If not, either substantiate or drop. The Fact
Register Action column is the enforcement mechanism — if a fact was marked DROP, it must
not appear in any form.

**Test:** Search the output for the words: fast, scalable, reliable, robust, efficient,
powerful, optimal, high-performance, high-availability. For each occurrence, verify it has
a numeric bound, a mechanism explanation, or a specific comparison. Any occurrence without
one of these is vagueness laundering.

---

## Pattern 4: Tone Osmosis

**Mechanism:** Over a long reconstruction, the model's register gradually converges toward
the source's register. This is most pronounced when the source has a consistent but wrong
register: bureaucratic ("the aforementioned components facilitate the processing of"),
sycophantic ("this innovative and powerful system"), or pseudo-academic ("it can be observed
that the utilization of").

The contamination is cumulative. The first few paragraphs are usually cleanest. By the
middle of a long document, the tone has drifted toward the source.

**Detection signals:**
- The output's opening sections read significantly differently (crisper, more direct) than
  the later sections.
- Bureaucratic constructions appear only in sections that had dense source material.
- The sentence length distribution shifts as the document progresses.

**Countermeasure:** Explicitly select a voice in Phase 1 Step 1.5 and bind all writing to
it. Before writing each major section, re-read the voice description and the Contamination
Flags. Do not write sections in continuous sequence without a register reset between them.

**Test:** Read the first paragraph of the document and the last paragraph. If they sound
like they were written by different authors, tone osmosis has occurred. The document should
have a single consistent register throughout.

---

## Pattern 5: Rationale Elision

**Mechanism:** The source states a decision without its rationale (e.g., "We use Redis for
caching"). The model reconstructs this statement, possibly with elaboration, but does not
supply the rationale — because the source did not provide it, and the model is in reconstruction
mode rather than analysis mode.

The result is a document that is cleaner than the source but still fails the senior engineer
test: it states what was decided without enabling the reader to evaluate the decision or
extend it to new contexts.

**Detection signals:**
- Technology choices stated without alternatives considered.
- Configuration values presented without explanation of why that specific value.
- Architecture patterns named without the problem they solve stated.
- "We chose X" without "We considered Y and Z, which were rejected because..."

**Countermeasure:** For every design decision in the Fact Register (any fact of the form
"Component X is used for purpose Y"), the reconstruction must attempt to supply:
1. The mechanism by which X serves purpose Y.
2. At least one alternative and why it was not chosen (or an explicit "alternatives not
   documented" flag if this cannot be derived).

If the rationale cannot be derived from first principles, mark it `[rationale not in source
— verify]`. Never let an undocumented decision pass through the reconstruction unmarked.

**Test:** For every "we use X" or "the system does Y via Z" statement in the output, ask:
"Could the reader understand why this choice was made?" If not, either add the rationale
or mark it for verification.

---

## Pattern 6: False Completeness

**Mechanism:** The source covers a topic partially. The model, having reconstructed the
covered portion well, implicitly signals to the reader that the topic has been fully addressed.
This is worse than an explicit gap — a reader who sees a polished, complete-looking section
will not know to seek additional information.

This pattern most commonly affects:
- Failure modes sections that cover one or two scenarios while missing the most dangerous one
- Decision rationale sections that cover the technical criteria while ignoring operational
  or security criteria
- Architecture diagrams that show the happy path but omit the error handling flows

**Detection signals:**
- A section appears complete and well-structured but has fewer failure scenarios than the
  technology actually has.
- A comparison table has clean rows but is missing a criterion that would change the outcome.
- An architecture diagram shows only forward flows with no error branches.

**Countermeasure:** For each section type in the Gap Inventory, ask not just "is this section
present?" but "is this section complete?" Use the section templates in
`tech-writing/references/structure-guide.md` as a completeness checklist: what must a
failure modes section contain? What must a decision rationale contain?

**Test:** For the failure modes section specifically: are at least two failure modes
documented with mechanism, detection signal, and recovery path? If only one is covered,
the section is likely incomplete regardless of how well that one is written.

---

## Pattern 7: Scope Inflation from Source Sprawl

**Mechanism:** The source covers multiple topics loosely stitched together. The model,
trying to be faithful to the source, attempts to cover all of them. The result is a document
that is technically accurate but unfocused — it answers multiple questions without answering
any of them fully.

This is particularly common when the source is internal notes, meeting summaries, or early
drafts where the scope was never disciplined.

**Detection signals:**
- The annotated outline has more than 7–8 sections.
- Two or more sections could each be the "main topic" of a different document.
- The Central Argument in Step 1.1 required qualifications ("X, but also Y, and also Z...").

**Countermeasure:** Apply the scope boundary declaration from `tech-writing` Step 0.4 with
extra strictness for reconstructions. Be willing to split the source into two documents if
the topics are genuinely independent. A focused 1,200-word document is more useful than a
sprawling 3,000-word document that covers three topics at 60% depth each.

**Test:** Can you state the Central Argument in one sentence without using "and" to connect
two independent claims? If not, the scope may need splitting.

---

## Quick Reference: Pre-Writing Contamination Check

Before beginning Phase 1, confirm each item:

```
PRE-WRITING CONTAMINATION CHECK
─────────────────────────────────────────────────────────────────
[ ] Fact Register is complete — no claims extracted verbatim, all assessed for confidence
[ ] Structural Mirroring: source section order is NOT the default for output
[ ] Void Inheritance: gaps identified in Quality Audit are now writing obligations, not omissions
[ ] Vagueness Laundering: all DROP items from Fact Register have zero representation in output
[ ] Tone Osmosis: voice is selected and will be re-checked at each major section boundary
[ ] Rationale Elision: every design decision has either a stated rationale or a verification flag
[ ] False Completeness: section templates will be used as completeness checklists
[ ] Scope Inflation: Central Argument is stated in one sentence; scope split considered if needed
─────────────────────────────────────────────────────────────────
```