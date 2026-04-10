# Extraction protocol

This file describes how to read a source and turn it into a Fact Register. The protocol is the operational core of Phase 1 of the tech-rewrite workflow, and it is the single point at which the skill either succeeds or fails — if the extraction is thorough and disciplined, the rest of the workflow follows almost mechanically; if the extraction is sloppy, no amount of care in the writing phase will rescue the output.

The extraction protocol has two load-bearing principles. The first is that reading and writing are separate activities, to be performed at separate times, with a firewall between them. The reader reads. The writer writes. The Fact Register is the only permitted bridge. The second is that the reader is actively skeptical of the source, not deferential to it. The source is raw intelligence from a past investigation; it is not a template, not an authority, and not a shape for the output to fit into. Every claim in the source is treated as a candidate for the KEPT section, and the default is that it does not make it in unless it meets the KEPT criteria.

## The Fact Register

The Fact Register is a structured document with four sections: KEPT, DISCARDED, MISSING, and AMBIGUOUS. A short contamination risk assessment follows the four sections. The full template is in `fact-register-template.md`. This file explains what each section is for and how to populate it.

### KEPT

KEPT contains every concrete, verifiable, specific claim that the source makes and that the writer would want to cite. A claim qualifies for KEPT if it meets three conditions simultaneously. The first condition is concreteness — the claim refers to a specific thing, a specific number, a specific behavior, or a specific decision. Vague claims do not qualify. The second condition is verifiability — the claim is grounded in evidence the writer can point to, whether that evidence is a source document, a measurement, a piece of code, or a named human's confirmation. Unsubstantiated claims do not qualify. The third condition is load-bearing potential — the claim is the kind of thing a strong document on this topic would cite. Trivia does not qualify, even when it is concrete and verifiable.

The KEPT section is not a summary of the source. It is a selective extraction of the source's highest-value content. A source with ten pages may produce a KEPT section with fifteen entries; a source with two pages may produce a KEPT section with twenty entries. The size of KEPT is determined by the source's density of concrete claims, not by the source's length.

Each entry in KEPT has a standardized format. The claim is stated in the writer's own words, stripped of the source's structure and phrasing. A provenance tag records where the claim came from in the source — a paragraph reference, a line number, a section title — so the writer can trace any later question back to the original. A hedge level records whether the source stated the claim flatly or with qualification, which is essential for defending against Confidence Upgrade in the writing phase. A relevance tag indicates whether the claim is load-bearing for the likely argument, supporting material, or background.

The rewrite of claims into the writer's own words is a non-negotiable step. Copying the source's phrasing into the Fact Register is the first breach of the firewall — it imports the source's vocabulary and rhythm into the register, and from there into the writing phase. The rewrite must strip all stylistic cues from the source while preserving the factual content. A sentence from the source that reads "our revolutionary caching engine harnesses cutting-edge memory architecture to deliver blazing-fast performance" becomes a KEPT entry like "the cache uses an off-heap memory allocation strategy (source para 2), unmeasured performance claim". The marketing language is gone. Only the content survives.

### DISCARDED

DISCARDED is the skill's defense against Ambiguity Whitewashing. It contains every vague, unsubstantiated, hedged, or otherwise unusable claim from the source, each annotated with a short reason for the rejection. The DISCARDED section is not a list of things the writer disagrees with; it is a list of things that fail the KEPT criteria and are therefore unavailable as material for the writing phase.

Populating DISCARDED is an active discipline, not a passive one. The extractor scans the source for claims that are marketing adjectives dressed up as statements, for hedges that were left unsupported, for evaluative language without evidence, for numbers that lack measurement methodology, and for comparative claims that lack a baseline. Each such claim goes into DISCARDED with a reason: "vague — no number", "hedged — no evidence", "evaluative — no criterion", "comparative — no baseline". The reason is important because it reminds the writer during Phase 2 why the claim is unusable, which prevents the claim from drifting back into the draft.

A common mistake during extraction is to leave DISCARDED empty when the source is reasonably well-written. This is almost always wrong. Even high-quality sources contain some vague claims that could not survive rigorous extraction; the only exception is a source that has already been through a disciplined writing process, in which case the rewriter is probably doing unnecessary work and should ask the user whether a rewrite is actually needed. A DISCARDED section with zero entries is a signal that the extractor has been too deferential to the source.

### MISSING

MISSING is the skill's defense against Void Inheritance. It contains every piece of information that a strong document on this topic would need but that the source does not supply. Populating MISSING requires the extractor to think about what the target document needs, not about what the source provides, which is a different and harder cognitive move.

The practical technique is to use the shared document-type reference as a checklist. Before reading the source in detail, the extractor opens the likely target document type's reference file (`shared-doctype-*.md`) and notes the expected sections, the standard quality gates, and the cross-cutting concerns. Each expected item becomes a question during the extraction: does the source supply what is needed for this section? When the answer is no, the item goes into MISSING.

MISSING is not a list of trivia the source omits. It is a list of load-bearing absences — things the writer cannot proceed without. A design document's MISSING section might include observability, cost, security review, and the specific failure mode under partition. A comparison document's MISSING section might include the criteria by which the options are being compared. An ADR's MISSING section might include the rejected alternatives and the specific reasons for rejection. Each MISSING item will force a decision in Phase 2: research, ask the user, or scope out.

A MISSING section with zero entries is extremely rare and almost always a sign that the extractor has not thought rigorously about what the target document requires. The default state of MISSING is "has entries"; an empty MISSING should trigger a review.

### AMBIGUOUS

AMBIGUOUS contains claims that are neither unambiguously concrete (KEPT) nor unambiguously vague (DISCARDED), but unclear enough that the extractor cannot tell what the source means without guessing. Ambiguous claims might be valuable once clarified, so they are held in AMBIGUOUS pending resolution rather than discarded outright.

Typical AMBIGUOUS entries include: terms used inconsistently across the source (the Terminology Drift pattern), claims that could refer to different subsystems depending on how a pronoun is resolved, numbers that could be throughput or latency depending on how the unit is interpreted, and decisions that could be either proposals or accepted standards depending on the context. For each ambiguous entry, the extractor records both possible interpretations and the specific ambiguity that needs to be resolved.

AMBIGUOUS entries must be resolved before Phase 2 can proceed on any claim whose interpretation depends on the ambiguity. Resolution comes from one of three sources: the user confirms the intended meaning; additional source material resolves the ambiguity; or the extractor determines that the ambiguity is not material to the target document and the claim can be dropped. The one move that is not permitted is silently picking one interpretation during the writing phase — that is exactly the Terminology Drift failure mode.

### Contamination risk assessment

After the four sections are populated, the extractor runs the contamination risk assessment. This is a structured diagnostic that rates the source against each of the ten contamination mechanisms on a three-level scale (low, medium, high) with specific evidence for each rating. The assessment is not a formality. Each rating has operational consequences in Phase 2 and Phase 3, documented in `contamination-risk-assessment.md`.

The assessment happens at the end of extraction, not at the beginning, because the extractor needs the four sections to be populated before they can see the contamination patterns clearly. A source's Tone Infiltration risk, for example, is easier to assess after the extractor has rewritten several KEPT claims and noticed how much of the source's vocabulary needed to be stripped.

## The firewall

The firewall between extraction and composition is the non-negotiable core of the skill. The firewall has three specific rules.

The first rule is that during Phase 1, the extractor does not draft. Not a title. Not an opening sentence. Not a section heading. Not a piece of prose in the target document's voice. Phase 1 is exclusively for populating the Fact Register. Drafting during Phase 1 is the single fastest way to introduce Structural Mirroring, because any draft produced while the source is still open will inherit the source's shape without the writer noticing.

The second rule is that during Phase 2 and Phase 3, the writer does not re-open the source. Once the Fact Register is complete and the extractor has handed off to the writer (even when the two are the same person), the source is closed. Any question that arises during writing — "what did the source say about X?" — is treated as a MISSING item to be resolved by looking at the Fact Register, not by re-reading. If the Fact Register does not contain the answer, the answer is unavailable, and the writer must either ask the user, do research, or scope the missing item out of the draft.

This rule feels restrictive. It is. The restriction is the point. The writer who allows themselves to re-open the source "just to check" will almost always end up absorbing more of the source's structure, tone, and phrasing than they intended. The firewall exists because the writer cannot be trusted to make small exceptions without compounding the contamination.

The third rule is that when Phase 1 turns out to be insufficient — when the writer reaches Phase 2 or Phase 3 and discovers the Fact Register is missing something important — the correct move is to return to Phase 1 and re-extract, not to re-read the source in an ad-hoc way. A formal return to Phase 1 preserves the firewall. An ad-hoc re-read breaches it.

## Walking through an extraction

The best way to understand the protocol is to walk through a concrete example. The example below uses a short source so the mechanics are visible; real sources are often longer, but the procedure is the same.

### The source

Imagine the user has provided the following rough notes from an internal meeting:

> Meeting notes — payment service latency investigation
>
> Alice: p99 is way over budget. We were at 80ms last quarter, now it's like 180ms. Target is 100ms. Ops is getting paged a lot.
>
> Bob: I think it's the new fraud check. It talks to the ML service, which is kinda slow. We're blocking on it in the request path.
>
> Alice: Could be. We should measure. But also, didn't we add that database migration last month? Could be the index changes.
>
> Bob: Good point. Two suspects.
>
> Chen: I looked at the traces yesterday. Most of the time is in the fraud check — looks like around 120ms on average when it fires. The DB stuff is under 10ms.
>
> Alice: So it's the fraud check. What do we do?
>
> Bob: We could do the fraud check async, but that means we let the payment through and then reverse it if it fails. Product doesn't love that.
>
> Chen: Or cache the fraud results for repeat customers. Maybe 40% of our traffic is repeats.
>
> Alice: Like the cache idea. Let's prototype it. Meeting over.

### The Fact Register after extraction

```
# Fact Register: payment service latency investigation

## KEPT

1. [source: para 1] Payment service p99 latency target is 100ms.
   - Hedge level: flat (stated as a known target)
   - Relevance: load-bearing

2. [source: para 1] Current p99 latency is approximately 180ms.
   - Hedge level: approximate ("like 180ms" — casual phrasing, treat as rough)
   - Relevance: load-bearing

3. [source: para 1] Previous-quarter p99 latency was approximately 80ms.
   - Hedge level: approximate
   - Relevance: load-bearing (establishes regression)

4. [source: para 5] Fraud check latency averages ~120ms when the check fires,
   per trace inspection by Chen.
   - Hedge level: measured (trace evidence)
   - Relevance: load-bearing (identifies the bottleneck)

5. [source: para 5] Database-related time is under 10ms, per trace inspection.
   - Hedge level: measured
   - Relevance: load-bearing (rules out the DB migration hypothesis)

6. [source: para 5] Fraud check runs synchronously in the request path.
   - Hedge level: flat
   - Relevance: load-bearing (explains why fraud-check latency becomes p99 latency)

7. [source: para 7] Cache idea: repeat customers are approximately 40% of traffic
   (per Chen, source of number not stated)
   - Hedge level: approximate, unsourced
   - Relevance: load-bearing for one proposed solution

## DISCARDED

- "Ops is getting paged a lot" (para 1) — vague, no page count, no timeframe
- "ML service is kinda slow" (para 2) — vague, no measurement; superseded by
  Chen's trace measurement of 120ms in KEPT #4
- "Product doesn't love that" (para 6) — vague, no specific product concern
  stated; cannot be used as a rejection reason without more detail

## MISSING

- What is the SLO / impact of the 180ms vs 100ms gap? (business cost? user
  impact? page frequency is "a lot" but not quantified)
- Is the 120ms fraud check latency stable or variable? (average only; no
  percentiles, no distribution, no tail)
- Fire rate of the fraud check: what percentage of requests trigger it?
  (affects whether caching is the right fix)
- Hit rate a cache would achieve: the 40% repeat-customer number is a lower
  bound on hit rate, not the hit rate itself; depends on cache key design
- Rejected alternatives beyond async and cache: what about parallelizing
  the fraud check with other request work? Speeding up the ML service?
- ML service owner and their view: is the fraud check slow by design or
  is there a known performance issue on their side?
- What does the fraud check actually check for? (affects whether caching
  would return stale results that let fraud through)

## AMBIGUOUS

- "the DB stuff" (para 5) — refers to the database migration from para 3 OR
  to any DB work in the request path? Resolution: probably the former but
  should confirm; low impact either way because "under 10ms" rules out DB
  as a significant contributor in both interpretations

## Contamination risk assessment

- Structural Mirroring: LOW — source is a chronological meeting transcript,
  not a document structure; no temptation to mirror it directly.
- Void Inheritance: HIGH — source lacks multiple load-bearing items (see
  MISSING section). Defense: resolve MISSING before Phase 2.
- Ambiguity Whitewashing: HIGH — source contains multiple vague claims
  ("kinda slow", "a lot", "doesn't love that"). Defense: enforce DISCARDED
  discipline.
- Tone Infiltration: MEDIUM — source is informal meeting-transcript voice;
  if the writer drifts, the output may inherit a casual register
  inappropriate for a technical write-up. Defense: name target voice
  explicitly (Design Tribunal or Production War Story).
- Rationale Vacuum: MEDIUM — the fraud-check-as-bottleneck conclusion
  is well-supported, but the choice of caching as the proposed solution
  is under-justified (async alternative dismissed with "product doesn't
  love that"; parallelization not considered). Defense: either strengthen
  rationale via user input, or scope the output to the diagnosis rather
  than the proposed solution.
- False Completeness: LOW — source is clearly a meeting note, not a
  complete investigation; no risk of treating it as exhaustive.
- Scope Inflation: LOW — source is focused on one problem.
- Confidence Upgrade: MEDIUM — casual approximations ("like 180ms",
  "kinda slow") will tempt polishing into flat assertions. Defense:
  preserve hedge levels from KEPT in the draft.
- Terminology Drift: LOW — terms are used consistently.
- Pseudoanchor Import: MEDIUM — the 40% repeat-customer number is
  unsourced and could be polished into a specific-looking claim. Defense:
  preserve provenance tag; if the number appears in the draft, it must
  carry the "per Chen, source of number not stated" qualifier, or be
  replaced with a measured number from the user.
```

### Observations about the example

A few points are worth noting. First, the Fact Register is longer than the source. Seven KEPT entries, three DISCARDED, seven MISSING, one AMBIGUOUS, plus a risk assessment, for a source that was fewer than 200 words. The length is not padding — it reflects the active work of extraction, which surfaces things (especially MISSING) that are invisible in the source.

Second, the MISSING section carries most of the investigative value. The source claims to be a latency investigation, but the Fact Register reveals that the investigation is actually incomplete: the team identified the bottleneck but did not finish analyzing the solution. A rewrite based on this source would either need to complete the investigation (via user input or additional research) or scope itself to "here is what we know so far; the next steps are [MISSING items]". Both of those are honest. Polishing the source's premature conclusion into a confident recommendation would be Rationale Vacuum plus Void Inheritance in combination.

Third, the contamination risk assessment turns up two HIGH ratings (Void Inheritance and Ambiguity Whitewashing) and three MEDIUM ratings. None are LOW across the board, which is typical of real-world sources. The HIGH ratings are the ones that trigger specific defensive moves in Phase 2 — in this case, the writer would need to resolve the MISSING items with the user before proceeding, and enforce DISCARDED discipline during drafting.

Fourth, the KEPT section is written entirely in the extractor's own words. None of the source's phrasing has survived. The claims are factually identical to what the source said, but the vocabulary and rhythm are gone. This is the anti-Tone-Infiltration discipline in action. A writer drafting from this KEPT section would not have any stylistic residue from the meeting transcript to inherit.

## Handoff to Phase 2

The handoff between Phase 1 and Phase 2 is the moment the firewall closes. At this point the extractor produces two things: the completed Fact Register, and a short handoff note summarizing what the writer needs to decide before drafting. The handoff note typically includes the highest-priority MISSING items that need user input, any HIGH contamination risks that require specific defensive moves, and any AMBIGUOUS items that block progress.

The handoff note is the last time the source is referenced. After the handoff, the source is closed, and all further work proceeds from the Fact Register and the handoff note alone. Phase 2 begins with an explicit act of closing the source — whether that means scrolling away from it, closing the file, or physically setting the document aside — because the act is a commitment. Once the source is closed, the writer is committed to the firewall, and any later re-opening requires a formal return to Phase 1.