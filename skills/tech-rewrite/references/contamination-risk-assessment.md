# Contamination risk assessment

This file is the diagnostic tool used at the end of Phase 1 of the tech-rewrite workflow. After the four sections of the Fact Register have been populated, the extractor runs the assessment to rate the source against each of the ten contamination mechanisms. Each rating has specific operational consequences in Phase 2 and Phase 3, and the assessment turns what would otherwise be a vague sense of contamination risk into a concrete list of defensive moves the writer must make.

The assessment is a judgment call, but it is not a free one. Each rating has to be supported by specific evidence drawn from the source or from the populated Fact Register. A rating of HIGH without evidence is meaningless. A rating of LOW that overlooks visible evidence is a failure of the diagnostic.

## The three-level scale

The assessment uses a three-level scale for each mechanism: LOW, MEDIUM, or HIGH. The levels correspond to three different defensive postures in the subsequent phases of the workflow.

A rating of LOW means the source shows little or no evidence of the mechanism's presence, and the standard discipline of the workflow is sufficient to defend against it. No special defensive moves are required beyond what the Fact Register and the shared quality checklist already enforce. Most well-written sources earn LOW ratings on most mechanisms.

A rating of MEDIUM means the source shows some evidence of the mechanism, and the writer needs to watch for it actively during Phase 2 and Phase 3. The defense is heightened attention, not a structural change to the workflow. The writer keeps the risk in mind when designing the target and sweeps for the specific contamination signature during the Phase 4 validation loop.

A rating of HIGH means the source is contaminated on this mechanism to a degree that requires a specific defensive move, documented per-mechanism below. HIGH ratings are not advisory; they are mandatory triggers for additional work. A rating of HIGH that is not followed by the corresponding defensive move has left the workflow in an unsafe state, and the resulting draft is likely to fail Phase 4.

## Per-mechanism assessment criteria

Each of the ten mechanisms has a rubric for rating the source, a short list of typical evidence for each rating level, and a defense playbook for the HIGH rating. The rubrics are intentionally concrete so that two extractors applying the assessment to the same source would tend to reach similar conclusions.

### 1. Structural Mirroring

The rubric for Structural Mirroring asks whether the source has a distinctive structure that would be tempting to copy during drafting. LOW ratings apply when the source has no discernible structure (notes, emails, transcripts), when the source's structure is clearly inappropriate for the target document type, or when the extractor is confident that the writing phase will not be tempted by the source's shape. MEDIUM ratings apply when the source has a reasonable structure that could survive into the output if the writer is not careful. HIGH ratings apply when the source has a polished, section-oriented structure that reads like a valid document shape — a wiki page with clear headings, a slide deck, or a previously-published article — because such sources are the ones most likely to be mirrored.

The defense when HIGH is a mandatory structural redesign step in Phase 2. Before beginning to draft, the writer produces a proposed structure for the target document from the Anchor Sheet alone. The writer then compares the proposed structure against the source's structure and verifies that they are substantially different in at least two of these three dimensions: the number of sections, the ordering, and the opening move. If the proposed structure matches the source on all three dimensions, the writer redesigns until it does not.

### 2. Void Inheritance

The rubric asks whether the source is missing load-bearing information that a strong document on the topic would need. LOW ratings are rare; they apply only when the source is unusually comprehensive and the MISSING section of the Fact Register is essentially empty. MEDIUM ratings apply when the source is missing a handful of items that the writer can resolve through research or targeted user input. HIGH ratings apply when the MISSING section has many entries, when the missing items are load-bearing for the likely central argument, or when the gaps suggest the source was written for a different purpose than what the user wants the target to be.

The defense when HIGH is to resolve the most load-bearing MISSING items before beginning Phase 2. The writer identifies which MISSING entries are required for the target document to be coherent, presents them to the user with specific questions, and waits for answers. The writer does not proceed to Phase 2 with unresolved load-bearing gaps; doing so guarantees that the output will inherit the source's blind spots.

### 3. Ambiguity Whitewashing

The rubric asks how many of the source's claims are vague, hedged-without-support, or evaluative without evidence. LOW ratings apply when the source's claims are almost all concrete and the DISCARDED section of the Fact Register is small. MEDIUM ratings apply when the source contains a moderate number of vague claims that have been cleanly captured in DISCARDED. HIGH ratings apply when the source is densely populated with vague claims, especially when those claims look like they would tempt a careless writer to polish them into confident prose.

The defense when HIGH is heightened DISCARDED discipline during extraction and an explicit review pass during Phase 4. Before delivering the draft, the writer walks through the DISCARDED section and verifies that no claim from it has survived into the draft in polished form. This check is in addition to the shared Gate 9 anti-pattern sweep; it is specifically looking for the signature of Ambiguity Whitewashing, which is prose that reads authoritatively but has no corresponding KEPT entry backing it.

### 4. Tone Infiltration

The rubric asks how distinctive and pervasive the source's tone is. LOW ratings apply when the source's tone is already appropriate for the target (for example, a source written in Design Tribunal voice being rewritten into another Design Tribunal document). MEDIUM ratings apply when the source has a moderate stylistic lean that the writer must actively resist — a slightly marketing-ish internal wiki, a mildly tutorial-voiced README. HIGH ratings apply when the source has a strong, distinctive, pervasive voice that is inappropriate for the target: marketing whitepapers being rewritten into technical blog posts, academic papers being rewritten into engineering documentation, bureaucratic memos being rewritten into any engineer-facing document, or stream-of-consciousness transcripts being rewritten into any polished document.

The defense when HIGH has three parts. First, the target voice is named explicitly in Phase 2 before any drafting, even if it would otherwise be implicit. Second, the writer consults the forbidden-moves list for the target voice in `shared-narrative-voices.md` and commits to sweeping for those moves during Phase 4. Third, the writer runs a specific residual-language check after drafting, scanning for signal words from the source's voice — marketing vocabulary, tutorial vocabulary, academic vocabulary, bureaucratic vocabulary — and cutting any that survived.

### 5. Rationale Vacuum

The rubric asks how many decisions or recommendations in the source are stated without supporting reasons. LOW ratings apply when the source is primarily descriptive and contains few decisions, or when the decisions are consistently accompanied by clear rationale. MEDIUM ratings apply when the source contains some unjustified decisions that the writer can plausibly justify through research or user input. HIGH ratings apply when the source is full of asserted decisions with no reasons given, especially when the target document type is an ADR, a design document, or a comparison — all of which require rationale to pass the shared quality checklist.

The defense when HIGH is to treat every unjustified decision as a MISSING item that must be resolved before Phase 2. The writer lists the decisions, asks the user for the reasons behind each, and records the reasons in KEPT with appropriate provenance. Decisions for which no rationale can be obtained are either scoped out of the target document or explicitly labeled as "undocumented decisions from the original source" so the reader knows they lack justification.

### 6. False Completeness

The rubric asks whether the source's scope matches the target's scope. LOW ratings apply when the source and target have essentially the same scope. MEDIUM ratings apply when the source's scope is narrower than the target's but the gap is small and fillable through research. HIGH ratings apply when the source's scope is substantially narrower than the target's, especially when the source's title or framing suggests a breadth it does not actually deliver — a two-paragraph "strategy document", a "comprehensive guide" with four sections, a "design document" that omits half the standard sections.

The defense when HIGH is to narrow the target's scope to match what the source actually covers, or to broaden the source's coverage with material from other sources before proceeding to Phase 2. The writer does not proceed with a target title that promises breadth the Fact Register cannot support. The title is either narrowed or the gaps are filled; there is no third option.

### 7. Scope Inflation

The rubric asks whether the source covers multiple distinct topics that should be separate documents. LOW ratings apply when the source is focused on a single topic. MEDIUM ratings apply when the source has a primary topic and some tangential material that the writer can cleanly excise. HIGH ratings apply when the source contains two or more topics of comparable importance, each of which could justify its own document — a meeting transcript covering three different decisions, a weekly status update covering five separate projects, a wiki page that has accreted unrelated sections over time.

The defense when HIGH is to propose a split to the user before beginning Phase 2. The writer identifies the distinct topics, names which one is the strongest candidate for the current rewrite, and asks the user to confirm either that this rewrite will focus on one topic (with others deferred or handled separately) or that the user wants a status-report-style synthesis rather than an argued piece. The writer does not silently pick one topic and drop the rest, because that may not match the user's intent, and does not silently include all topics in one document, because that produces Scope Inflation.

### 8. Confidence Upgrade

The rubric asks how many of the source's factual claims are hedged with qualifiers that look like they could be polished out. LOW ratings apply when the source's claims are either clearly measured or clearly speculative, with no ambiguous middle ground. MEDIUM ratings apply when the source contains some casual hedges that preserve honest uncertainty and that a careless writer might remove. HIGH ratings apply when the source is heavily hedged, especially when the hedges are on claims that the target document might want to make definitively — for example, a post-mortem source that hedges the root-cause identification, being rewritten into a blog post that wants to assert the root cause.

The defense when HIGH is to populate the hedge-level field in every KEPT entry with extra care and to run an explicit hedge-preservation check during Phase 4. For every confident claim in the draft, the writer locates the corresponding KEPT entry and confirms that the hedge level supports the draft's confidence. Draft confidence that exceeds the KEPT hedge level is a Confidence Upgrade violation and must be rolled back.

### 9. Terminology Drift

The rubric asks whether the source uses key terms consistently. LOW ratings apply when the source has a stable, consistent vocabulary. MEDIUM ratings apply when the source has some terminology inconsistencies that are easy to spot and disambiguate. HIGH ratings apply when the source has significant terminology drift — terms used in two or more different senses without marking the transition, inherited jargon from multiple authors, or project-specific names whose meanings have evolved over time.

The defense when HIGH is to build a small disambiguation glossary during extraction and to record ambiguous terms in the AMBIGUOUS section of the Fact Register. The writer does not proceed to Phase 2 with unresolved terminology conflicts on load-bearing terms; the user is asked to confirm the intended meaning, and the Fact Register is updated with unambiguous labels (for example, renaming one sense of "worker" to "job-worker" and another to "inference-worker") before drafting begins.

### 10. Pseudoanchor Import

The rubric asks how many of the source's quantitative claims are vague enough to be tempting to polish into specific numbers. LOW ratings apply when the source's quantitative claims are either specific and sourced or clearly non-quantitative. MEDIUM ratings apply when the source contains a few vague quantities that a writer might be tempted to sharpen ("about a million users", "handles significant traffic"). HIGH ratings apply when the source makes multiple quantitative claims without measurement methodology, especially in a register that implies rigor the source does not actually have — marketing materials, executive summaries, sales decks.

The defense when HIGH is strict numerical provenance tracking. Every number in KEPT carries a provenance tag, and the writing phase is forbidden from introducing numbers that do not appear in KEPT. The writer also runs an explicit pseudoanchor sweep during Phase 4, checking every number in the draft against KEPT and cutting or flagging any number that was not in the source at the specificity level claimed by the draft.

## Running the assessment

The assessment is run in sequence through all ten mechanisms, not in parallel. The sequential order matters because the ratings for later mechanisms sometimes depend on observations made while assessing earlier mechanisms. For example, a high Scope Inflation rating often reveals multiple distinct voices in the source, which in turn raises the Tone Infiltration rating. A high Terminology Drift rating often reveals ambiguous claims that change the Ambiguity Whitewashing rating.

The extractor writes each rating with its evidence in the Fact Register template's risk assessment section. The writing is brief but specific. "HIGH — the source is a marketing whitepaper with sentence-level residue of evaluative vocabulary throughout" is acceptable. "HIGH — the source is stylistically challenging" is not, because it does not say what the defender is defending against.

After all ten ratings are written, the extractor composes the handoff note to Phase 2, which lists the HIGH ratings and their required defensive moves as a short checklist the writer must address before drafting. The handoff note is the last thing produced in Phase 1 and the first thing the writer reads in Phase 2.

## What LOW across the board means

If the assessment returns LOW on all ten mechanisms, one of two things is true. The first possibility is that the source is unusually high quality and the rewrite is more of a formatting pass than a rescue job. In that case, the writer should ask the user whether the rewrite is actually needed — a high-quality source may not benefit from rewriting, and the effort may be better spent elsewhere. The second possibility is that the extractor has been insufficiently skeptical of the source and has missed contamination that is present. This is the more common case. The extractor should review the source once more with a specifically adversarial mindset before accepting the all-LOW assessment.

All-LOW ratings should be rare. A realistic rate is perhaps one in ten sources. Any higher rate suggests the assessment is being run pro forma rather than genuinely.

## What HIGH on many mechanisms means

If the assessment returns HIGH on four or more mechanisms, the source is heavily contaminated and the rewrite will require substantial additional work. In such cases, the writer should consider whether the rewrite is the right approach at all. Sometimes the better move is to use the source as raw intelligence for a from-scratch piece — in which case the workflow switches to the `tech-writing` skill, with the Fact Register's KEPT section serving as the anchor list for a blank-page effort. This is a legitimate escape hatch when the source is too contaminated to rewrite cleanly: extract what is salvageable, set the rest aside, and write from scratch.

The decision to switch from rewrite to blank-page is made at the end of Phase 1, before any drafting has begun. The writer presents the situation to the user, explains why the source is too contaminated for a conventional rewrite, and proposes using the Fact Register's KEPT section as input to a `tech-writing` workflow instead. The user either agrees (and the workflow continues under the other skill) or asks the writer to proceed with the heavy-contamination rewrite (and the writer applies all the HIGH defensive moves rigorously).