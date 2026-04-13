---
name: tech-rewrite
description: Transform existing technical material of any quality — rough notes, meeting minutes, AI-generated drafts, legacy wikis, code comments, email threads, chat exports — into high-quality technical documentation. Use this skill whenever the user asks to rewrite, restructure, clean up, polish, formalize, turn notes into an article, improve a draft, or extract documentation from existing material. Companion to the tech-writing skill — tech-writing handles the blank-page case, tech-rewrite handles the case where source material already exists. The two skills share identical quality standards, so a rewrite must be indistinguishable from a from-scratch piece on the same topic. Default output language is Chinese with technical terms in English. This skill enforces a mandatory extraction-before-composition firewall because low-quality sources contaminate AI-rewritten output through specific mechanisms when the source is treated as a template rather than as raw intelligence.
---

# tech-rewrite

A skill for transforming existing technical material into publication-quality documentation. The user has source material of some kind — notes, drafts, legacy docs, an AI-generated first pass — and wants it rewritten. This skill exists to prevent one category of failure: **style contamination**, the set of mechanisms by which low-quality source material degrades the output even when the writer intends to improve it.

The defense is not stylistic discipline during writing. By the time the writing phase begins, the contamination has usually already happened — it happened during reading, when the writer absorbed the source's structure, gaps, tone, and hedges and started to treat them as constraints. The defense is procedural: an extraction-before-composition firewall that separates reading the source from writing the output, with a Fact Register acting as the only permitted bridge between the two phases.

This skill is the companion to `tech-writing`. The two skills converge on identical quality standards. A document rebuilt from existing material must be indistinguishable from one written on the same topic from scratch. The shared standards live in files prefixed `shared-` in the references directory and are literal copies of the corresponding files in the `tech-writing` skill. If a quality gate applies to a tech-writing document, it applies to a tech-rewrite document in exactly the same form.

---

## The failure mode this skill fights

The pathology is counterintuitive. A careful reader who wants to improve a bad source ought to produce a good output. In practice, the careful reading is precisely what introduces the contamination. The reader absorbs the source's structure — its headings, its section order, its pacing — and starts to think of that structure as "the shape of the topic" rather than "one possible shape, and not a good one". The reader absorbs the source's vocabulary and starts to use it reflexively. The reader absorbs the source's gaps without noticing, because a gap is invisible by definition — the reader does not see the thing the source failed to cover. The reader absorbs the source's hedges and converts them into the output's assertions. None of this is intentional. All of it happens anyway.

Academic research documents the effect directly. LLM paraphrasing work has shown that when language models rewrite a source, the output preserves stylistic cues from the source at a level detectable by authorship-attribution classifiers, even when the rewrite was explicitly asked to change the style. Evaluation work on instruction-tuned models has shown that outputs can score well for style and structure while still being factually weak, because surface polish is easier for reviewers to assess than substance. These findings converge on the same practical conclusion: if the rewriter reads the source and then writes, the source leaks into the output. The only reliable defense is to interrupt that flow — to extract from the source into a structured intermediate, then put the source away and write from the intermediate alone.

This is how professional editors have always worked. Developmental editors produce a "summary document" from the manuscript and then make all structural decisions from the summary, with the manuscript physically set aside. The rationale is explicit: the language of the manuscript distracts the editor from the structure. A well-written chapter seems to work even when it does not; a poorly written chapter seems broken even when its structure is sound. The only way to see structure clearly is to see it without the language attached. The Fact Register in this skill plays the same role as the editor's summary document, and the extraction firewall plays the same role as the instruction to set the manuscript aside.

---

## Workflow

Every task under this skill follows four phases. The phase boundaries are firewalls, not suggestions. Do not draft while still extracting. Do not re-read the source while writing.

```
Phase 1: EXTRACTION        → produces a Fact Register
Phase 2: TARGET DEFINITION → produces an Anchor Sheet (from the Fact Register only)
Phase 3: WRITING           → produces a draft under tech-writing standards
Phase 4: VALIDATION        → runs shared quality gates plus rewrite-specific gates
```

### Phase 1 — Extraction

In Phase 1, read the source material with one and only one purpose: to populate the Fact Register. Do not yet think about structure, voice, or wording. Do not yet decide what the output will look like. Read only to extract.

The Fact Register has four sections. The first section is **KEPT**, containing every concrete, verifiable, specific claim the source makes. A fact is eligible for the KEPT section only if it is concrete enough to survive being stated without the source's words around it. "The service handles about a million requests per day on a t3.medium instance, with p99 latency around 180ms" is a KEPT fact. "The service is fast and scalable" is not.

The second section is **DISCARDED**, containing every vague, unsubstantiated, or hedged claim the source makes, each with a short reason for the rejection. The DISCARDED section is the skill's defense against Ambiguity Whitewashing — by explicitly cataloging the vague claims and labeling them as rejected, the extraction phase prevents those claims from drifting into the output as polished prose.

The third section is **MISSING**, containing every piece of information the reader would expect to find in a strong document on this topic but which the source does not contain. The MISSING section is the skill's defense against Void Inheritance — the source's gaps become visible as a list of named absences, which forces a decision about each one in Phase 3. Some MISSING items will be filled by research, some by asking the user, some by scoping the output more tightly to exclude them.

The fourth section is **AMBIGUOUS**, containing every claim that the source makes unclearly enough that the reader cannot tell what is meant without guessing. Ambiguous claims are neither KEPT (they are not concrete) nor DISCARDED (they might be valuable once clarified). They are held in AMBIGUOUS until the user confirms the intended meaning, at which point they move to KEPT or DISCARDED.

A contamination risk assessment is run after the four sections are populated. For each of the ten contamination mechanisms, the extractor rates the source's risk as low, medium, or high, with specific evidence from the source. The risk assessment is not decorative. High-risk ratings trigger specific defensive moves in Phase 3 — for example, a high Structural Mirroring risk triggers a mandatory structural redesign step before writing begins.

The detailed extraction protocol is in `references/extraction-protocol.md`. The Fact Register template is in `references/fact-register-template.md`. The contamination risk assessment procedure is in `references/contamination-risk-assessment.md`. All three should be read before the first Phase 1 of any task.

### Phase 2 — Target definition

Phase 2 is where the firewall does its work. At the start of Phase 2, put the source away. Do not look at it again. Work only from the Fact Register.

From the Fact Register, define the target document as if it were a blank-page piece. Write a central argument (falsifiable, defensible, one sentence). Identify the reader. Choose the document type. Select the narrative voice. Bound the scope. Decide which MISSING items will be addressed, which will be scoped out, and which require lookups or user input.

The output of Phase 2 is an Anchor Sheet in the same format as the `tech-writing` skill's Anchor Sheet. The two skills share this format deliberately — it is the point at which the two paths converge. A rewrite's Anchor Sheet should be identical in form to a blank-page Anchor Sheet, and a reader looking only at the Anchor Sheet should not be able to tell which path produced it. The Anchor Sheet format is described in full in the extraction protocol file.

The critical rule of Phase 2 is that the structure of the target document is designed from the Fact Register and the reader, not inherited from the source. If the source had three sections in order A-B-C, the target may have five sections in order D-E-B-F-A — or two sections, or ten — depending on what the argument requires. The source's ordering is not a signal of anything; it is the shape the previous writer happened to use. Let it go.

### Phase 3 — Writing

Phase 3 is identical to tech-writing's drafting phase. The writer uses the Anchor Sheet from Phase 2, picks up the relevant document-type reference file (`shared-doctype-*`), writes in the locked narrative voice, and follows the same drafting discipline. The source is still not being consulted. If the writer feels the urge to re-open the source to "check something", the something should be added to the Fact Register's MISSING list and resolved by lookup or user input, not by re-reading.

Because the writing phase uses the exact same standards as tech-writing, its guidance lives in the shared reference files. The writer consults `references/shared-narrative-voices.md` for voice discipline, `references/shared-anti-patterns.md` for the anti-pattern sweep, `references/shared-language-conventions.md` for Chinese and English conventions, and the appropriate `references/shared-doctype-*.md` file for the document type's specific structure.

### Phase 4 — Validation

Phase 4 runs two checklists in sequence. The first is the shared quality checklist from tech-writing, applied without modification. Any gate that applies to a blank-page document applies to a rewritten document. If the draft fails a shared gate, it fails — the fact that the draft came from a source is not an excuse. The shared checklist is in `references/shared-quality-standards.md`.

The second is the rewrite-specific checklist, which adds gates that only apply when the writing has a source. These gates check for the specific contamination signatures — structural mirroring, surviving DISCARDED items, unresolved MISSING items, inherited hedges, inherited tone, and scope inflation. If the draft fails any rewrite-specific gate, the fix is almost always to return to Phase 2 and redefine the target, not to patch the draft in place. Contamination is structural; the fix is structural. The rewrite-specific checklist is in `references/rewrite-checklist.md`.

A draft that passes both checklists is the deliverable.

---

## The ten contamination mechanisms (summary)

These are the mechanisms by which a source degrades the output when the firewall fails. Each mechanism is defined fully in `references/contamination-mechanisms.md` with before/after examples and detection heuristics. The summary here is intended as a mental map, not a substitute for the full file.

The first seven mechanisms match the original brief. The last three are additions based on research into LLM paraphrasing behavior and real-world examples of AI rewriting that preserved source flaws.

**1. Structural Mirroring** — the output silently copies the source's section structure, ordering, and pacing, even when a different structure would serve the argument better. The default failure mode; triggered whenever the writer reads the source from front to back and then writes.

**2. Void Inheritance** — the source fails to cover some aspect of the topic, and the output silently fails to cover it too, because the writer never noticed the absence. The most insidious mechanism because a gap is invisible by definition.

**3. Ambiguity Whitewashing** — the source contains a vague or hedged claim, and the output polishes the claim into confident prose without adding substance. The polish looks like improvement but is actually a degradation, because the reader can no longer tell the claim is vague.

**4. Tone Infiltration** — the source's tone (marketing, tutorial, academic, bureaucratic) bleeds into the output despite the writer's intent to change it. Measurable by authorship-attribution classifiers; not something the writer can fix by "trying harder".

**5. Rationale Vacuum** — the source states decisions without reasons, and the output repeats the decisions without reasons. The output looks authoritative because decisions have been asserted, but a senior reader can tell that no one has justified them.

**6. False Completeness** — the writer assumes the source covers the full topic, and the output inherits that assumption. Scoping decisions are made by reference to the source's scope rather than to the reader's actual needs.

**7. Scope Inflation** — the source covers too much ground, and the output covers the same too-much ground, because the writer did not exercise the option to narrow.

**8. Confidence Upgrade** — the source hedges a claim ("we think", "probably", "seems to be"), and the output polishes the hedge out, turning a cautious guess into an unsupported assertion. The output is now _less_ accurate than the source, even though it reads as more polished.

**9. Terminology Drift** — the source uses a term inconsistently or with drift in meaning. The output either perpetuates the drift or silently picks one meaning and uses it throughout, sometimes changing the meaning of claims the source was making about a different sense of the term.

**10. Pseudoanchor Import** — the source contains a vague quantitative claim ("handles a lot of traffic", "about a million users"), and the output polishes it into a specific-looking number. The number is invented in exactly the sense that it was not measured, it was polished; it is a fake anchor dressed up as a real one.

---

## Writing standards (unchanged from tech-writing)

This section is deliberately short because the standards are unchanged from tech-writing. Every rule that applies to a blank-page piece applies to a rewritten piece. The full rules live in the shared files.

The non-negotiable quality gates — title carries the argument, header info block, 60-second rule, verdict in comparisons, rejected alternatives for design decisions, failure modes as mechanisms, limitations with thresholds, visual explanations where they materially reduce cognitive load, Anchor-Sheet completeness, and the senior-engineer test — are enforced by `references/shared-quality-standards.md`.

The narrative voice catalog — Production War Story, Design Tribunal, Mechanism Autopsy, Migration Field Guide, Benchmarker's Notebook, Reference Librarian — is in `references/shared-narrative-voices.md`. The voice is chosen during Phase 2 from the Fact Register, not inherited from the source. A source written in Tutorial Voice does not constrain the output to Tutorial Voice.

The anti-pattern catalog — false balance, empty superlatives, background stuffing, passive responsibility avoidance, hedge stacking, Wikipedia-voice opening, and the rest of the twenty entries — is in `references/shared-anti-patterns.md` and is swept as Gate 9 of the shared quality checklist.

The Chinese and English conventions — technical terms in English, senior-engineer register, no marketing vocabulary, no tutorial voice, Anglo-Saxon over Latinate — are in `references/shared-language-conventions.md`.

The diagram selection rules — when a rewritten piece needs Mermaid support and which diagram type to choose — are in `references/shared-diagram-selection-guide.md`. The rewritten output does not inherit the source's visuals; it earns its own visual plan from the Fact Register and Anchor Sheet.

The seven document types — blog post, ADR, design document, comparison, deep-dive, API reference, migration guide — each have a dedicated file in `references/shared-doctype-*.md`. The writer reads the relevant file in Phase 3 before drafting.

---

## When to stop and ask the user

There are five situations in which Phase 1 or Phase 2 should stop and ask the user before proceeding. Each of them reflects a case where the cost of guessing is higher than the cost of asking.

The first is when the Fact Register's MISSING section contains items that are load-bearing for the argument. If the target document needs a number and the source does not supply it, the writer should ask whether the user has the number, whether the writer should look it up, or whether the argument should be scoped to avoid needing it. Inventing the number is never acceptable.

The second is when the AMBIGUOUS section contains items that materially affect the argument. An ambiguous claim in the source must be resolved before Phase 2, because Phase 2 depends on knowing what the central argument actually is. The resolution comes from the user, from research, or from a decision to drop the ambiguous item entirely.

The third is when the contamination risk assessment rates Tone Infiltration high and the user has not yet named the target voice. High Tone Infiltration risk means the source has a strong, distinctive tone that will leak into the output by default. The writer should propose a voice explicitly and confirm with the user before drafting, rather than hoping the tone will naturally reset during writing.

The fourth is when the contamination risk assessment rates Scope Inflation high and the source covers multiple distinct topics. The source may actually be two or three different documents glued together. The writer should propose a split and confirm with the user before proceeding, rather than trying to rewrite the conflation into a single coherent piece.

The fifth is when the source is fundamentally misaligned with the user's stated intent. The user asked for an ADR but the source is a tutorial; the user asked for a deep-dive but the source is a feature announcement. The extracted Fact Register will be insufficient for the requested document type, and the writer should raise the mismatch with the user before spending further effort.

In all five cases, the right move is to ask once, clearly, with specific options. Papering over the gap produces output that will fail Phase 4, which is more expensive than asking.

---

## Output language defaults

The defaults are identical to tech-writing. The output language is Chinese with technical terms kept in English, unless the user explicitly requests English. A source written in one language does not constrain the output to that language — a Chinese source can be rewritten into an English deliverable and vice versa, but translation is not done sentence by sentence. The source is extracted into the language-independent Fact Register, and then the output is re-drafted in the target language from the register, following the conventions in `references/shared-language-conventions.md`.

---

## Reference file map

All reference files are one level below `SKILL.md`. The files prefixed `shared-` are literal copies of the corresponding files in the `tech-writing` skill and enforce identical quality standards across both skills. The files without the prefix are rewrite-specific.

Rewrite-specific files:

- `references/contamination-mechanisms.md` — full catalog of the ten mechanisms with before/after examples
- `references/extraction-protocol.md` — detailed Fact Register methodology with worked examples
- `references/fact-register-template.md` — the working template for the Fact Register
- `references/contamination-risk-assessment.md` — diagnostic tool for Phase 1
- `references/rewrite-checklist.md` — rewrite-specific gates for Phase 4

Shared files (copies from tech-writing):

- `references/shared-quality-standards.md` — the full quality checklist
- `references/shared-narrative-voices.md` — the six narrative voices
- `references/shared-anti-patterns.md` — the anti-pattern catalog
- `references/shared-language-conventions.md` — Chinese and English conventions
- `references/shared-diagram-selection-guide.md` — choose the right Mermaid diagram for mechanisms, topology, state, or time
- `references/shared-doctype-blog-post.md` — technical blog post structure
- `references/shared-doctype-adr.md` — ADR structure
- `references/shared-doctype-design-doc.md` — design document structure
- `references/shared-doctype-comparison.md` — technology comparison structure
- `references/shared-doctype-deep-dive.md` — source code / mechanism deep-dive structure
- `references/shared-doctype-api-doc.md` — API reference structure
- `references/shared-doctype-migration-guide.md` — migration guide structure

---

## Final reminder

The entire skill rests on one load-bearing claim: **the firewall between extraction and composition must not be crossed**. Every failure mode of AI rewriting — every mechanism in the catalog — traces back to the writer reading the source and then writing, without a strict intermediate that breaks the source's hold on the output's shape. The Fact Register is the intermediate. Once it exists, the source can and must be set aside. If the writer finds themselves re-reading the source during writing, the skill has been bypassed and the output is now contaminated regardless of how polished it looks.
