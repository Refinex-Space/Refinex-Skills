# Rewrite-specific checklist

This file contains the rewrite-specific validation gates that run in Phase 4 of the tech-rewrite workflow. The gates here are in addition to the shared quality checklist in `shared-quality-standards.md`, not a replacement for it. Every rewritten draft must pass both checklists before delivery. A draft that passes the rewrite-specific gates but fails the shared gates is still a failed draft; a draft that passes the shared gates but fails the rewrite-specific gates still carries contamination that will be visible to a careful reader.

The gates below are designed to catch the specific signatures of the ten contamination mechanisms as they appear in a finished draft. They run as a diagnostic pass, after the writer believes the draft is complete. Each gate has a detection procedure and a fix procedure; the fix procedure is almost always "return to Phase 2 and redefine the target from the Fact Register", because contamination is structural and cannot reliably be patched at the prose level.

The gates are numbered to continue from the shared checklist, which runs Gates 0 through 12. The rewrite-specific gates begin at Gate R1 to make them unambiguously distinguishable from the shared gates when the writer reports which gates failed.

## Running the loop

The validation loop for a rewrite runs in a specific order. First, the writer runs the full shared quality checklist against the draft, from Gate 0 through Gate 12, fixing failures as they go. Only after the shared checklist passes does the writer run the rewrite-specific checklist. Running the rewrite-specific gates first is wasteful because a draft that fails the shared checklist will often be rewritten in a way that also fixes the rewrite-specific issues.

When a rewrite-specific gate fails, the fix usually involves returning to the Fact Register, identifying the contaminated material, and redrafting the affected section from the Fact Register without consulting the source or the contaminated draft. This is a stronger fix than editing the prose in place because editing leaves the contamination's structural footprint intact even when the surface language changes.

A clean pass through both checklists is the signal that the draft is ready for delivery. A draft that requires three or four iterations through the combined loop is normal for a contaminated source. A draft that requires seven or more iterations is a signal that the Fact Register was insufficient and the extraction phase should be revisited — continuing to iterate on the draft while the underlying Fact Register is thin is wasted effort.

## Gate R1 — Structure differs from the source

This gate defends against Structural Mirroring, the first and most common contamination mechanism. The check is straightforward and produces a clear pass or fail signal.

The writer lists the headings of the draft in order, then lists the headings of the source in order. For the gate to pass, the two lists must differ in at least two of three dimensions: the number of top-level sections must differ, the ordering of shared topics must differ, and the opening move must differ. If the draft matches the source on all three dimensions, the draft has inherited the source's structure and fails this gate.

The fix is a structural redesign in Phase 2. The writer closes the contaminated draft, opens the Fact Register, and designs a new structure from the central argument and the reader audit. The new structure is drafted before the writer returns to prose work. Rewriting headings in place is not a sufficient fix because the prose underneath the headings will usually still carry the old structure's pacing and emphasis.

A subtle failure mode of this gate is cosmetic differentiation — the writer renames the headings but preserves the underlying order and count. For example, if the source has four sections titled History, Features, Configuration, Troubleshooting, and the draft has four sections titled Background, Capabilities, Setup, and Common Issues, the surface looks different but the structure is identical. The gate test must look past the heading text to the information flow; a reader who read only the section titles of both documents should not be able to map them one-to-one.

## Gate R2 — All KEPT claims traceable, no untraceable claims introduced

This gate defends against Pseudoanchor Import and against the more general failure of the writer introducing unsourced claims during drafting. The check operates on concrete claims in the draft — numbers, named behaviors, specific versions, decisions, rejected alternatives, and any other claim that would be treated as a fact by a reader.

For every such claim in the draft, the writer traces it back to a KEPT entry in the Fact Register. The traceback succeeds when the draft claim corresponds to a KEPT entry at the same level of specificity. If the draft claims "4.2 million requests per second" and KEPT says "millions of requests, exact figure not stated", the traceback fails — the draft has added specificity that is not in the source, which is a Pseudoanchor Import violation.

Traceback can fail for three reasons, each of which has a different fix. The first is that the claim is in the source but was missed during extraction and not added to KEPT. The fix is to add it to KEPT with appropriate provenance and move on. The second is that the claim was invented during drafting. The fix is to cut the claim or replace it with a measured value from the user. The third is that the claim is a reasonable inference from multiple KEPT entries but was not itself in the source. The fix is to decide whether the inference is sound enough to stand in the draft, and if so, to add it to KEPT as a derived claim with the underlying entries cited.

The gate also fails if the draft introduces numbers that were not in KEPT, even when the surrounding prose is otherwise faithful to the source. This is the specific Pseudoanchor Import signature and is the most common form of gate R2 failure.

## Gate R3 — No DISCARDED material survived into the draft

This gate defends against Ambiguity Whitewashing. The check is a targeted sweep: the writer reads the DISCARDED section of the Fact Register and, for each entry, searches the draft for the corresponding claim in polished form.

The search is not for the exact words — those were left behind during extraction — but for the underlying vague claim reappearing as an assertion. If the DISCARDED section contains "our platform handles significant traffic" (rejected for vagueness) and the draft contains "our platform is built to handle high-volume workloads", the DISCARDED material has survived in paraphrased form and the gate fails. The paraphrase has preserved the vague claim's content while polishing its surface, which is Ambiguity Whitewashing.

The fix is to cut the paraphrased claim from the draft, or to replace it with a specific claim drawn from KEPT. The rewriter does not try to salvage the paraphrase; once a claim has been placed in DISCARDED it is unavailable as material, and attempting to preserve it in any form breaches the firewall.

A practical aid for this gate is to search the draft for any specific vocabulary that appeared in the DISCARDED entries, even after paraphrasing. DISCARDED entries often leave fingerprints — a specific adjective the source used, a specific framing, a specific comparison — that survive rewriting. These fingerprints are the easiest way to spot surviving DISCARDED material.

## Gate R4 — All load-bearing MISSING items addressed

This gate defends against Void Inheritance. The check is a walkthrough of the MISSING section of the Fact Register, with each entry categorized as either resolved, scoped out, or unresolved.

A MISSING entry is resolved if the information has been added to the draft, sourced either from user input or from research performed during Phase 2. A MISSING entry is scoped out if the target document's scope has been narrowed so the entry is no longer load-bearing, and the scope narrowing is visible in the draft's framing. A MISSING entry is unresolved if neither of the above has happened — the information is still missing, and the draft proceeds as if it were not.

The gate fails if any load-bearing MISSING entry is unresolved. Non-load-bearing MISSING entries may be left unresolved, but the writer should still document the decision so the reader has visibility into what was chosen.

The fix for an unresolved load-bearing MISSING entry depends on why it is unresolved. If the writer forgot about it, the fix is to address it now — either by asking the user, by research, or by scope narrowing. If the writer tried to address it and could not, the fix is to narrow the draft's scope so the entry is no longer load-bearing. If the scope cannot be narrowed because the argument depends on the missing information, the draft is fundamentally incomplete and needs user input before it can be delivered.

## Gate R5 — Rationale present for every decision

This gate defends against Rationale Vacuum. It overlaps with shared Gate 5 (rejected alternatives required) but is more stringent: where shared Gate 5 asks whether rejected alternatives are listed for design decisions, this gate asks whether every asserted decision in the draft is accompanied by a reason.

The check proceeds by scanning the draft for sentences that assert a decision, a recommendation, or a choice. For each such assertion, the writer verifies that a reason is given, either immediately adjacent to the assertion or in a clearly linked section. Assertions without reasons are candidates for Rationale Vacuum and must be addressed before delivery.

The fix is to add the reason from the Fact Register, to add it from user input if the Fact Register does not have it, or to remove the assertion from the draft entirely. The option of restating the assertion more confidently is never the right fix — confident assertion without rationale is the failure mode, not the solution to it.

## Gate R6 — Draft confidence matches KEPT hedge levels

This gate defends against Confidence Upgrade. The check compares the confidence level of claims in the draft against the hedge level recorded in KEPT.

For every confident or definitive claim in the draft, the writer locates the corresponding KEPT entry and reads its hedge level. If the KEPT entry is flagged as "approximate", "hedged", or "uncertain", the draft's confident version represents a Confidence Upgrade and fails the gate. The draft must be revised to preserve the hedge — either by restoring explicit hedging language, by attributing the claim to its original uncertain source, or by scoping the claim out of the draft.

A common failure mode of this gate is partial hedge preservation. The draft keeps one hedge from the source and drops another, or preserves the hedge on a less-central claim while upgrading the confidence on the load-bearing one. The check must be run on every confident claim in the draft, not sampled, because the writer's instinct to polish tends to upgrade confidence on the most important claims rather than the trivial ones.

## Gate R7 — Scope is equal or tighter than the source

This gate defends against Scope Inflation. The check compares the scope of the draft against the scope of the source: the list of topics the draft covers should be a subset of (or equal to) the list of topics the source covers, not a superset. A draft that covers more ground than the source is not necessarily wrong, but it is outside the rewrite workflow — adding topics means adding material that did not come from extraction, which violates the firewall.

The more common failure is the opposite direction: a draft that covers the same too-much ground as the source, because the writer did not narrow during Phase 2. The check catches both.

The writer lists the distinct topics the draft covers and compares against the distinct topics the source covered (which was recorded in the Fact Register's handoff note). If the draft's list is longer than necessary — if multiple distinct topics appear without a unifying central argument — the draft has Scope Inflation and the fix is to narrow the scope and cut the material outside the narrowed scope. If the draft's list adds topics not in the source, the additions need to be either removed or traced back to explicit research or user input that was added to the Fact Register.

## Gate R8 — Tone fully reset

This gate defends against Tone Infiltration. The check is a residual-language sweep that looks for vocabulary, rhythm, and stylistic markers from the source's voice that survived into the draft.

The writer identifies the source's dominant voice (marketing, tutorial, academic, bureaucratic, stream-of-consciousness) and lists the specific vocabulary and phrasings characteristic of that voice. The sweep then searches the draft for any of these signal elements. Any hit is a candidate for Tone Infiltration and must be either removed or justified.

The specific signal lists to check for each source voice are as follows. For a marketing source, the writer searches for words like powerful, seamless, unlock, harness, empower, revolutionary, cutting-edge, and for sentence rhythms of the form "X delivers Y at Z". For a tutorial source, the writer searches for phrases like let us, as we can see, now we will, and for the second-person address that tutorials use. For an academic source, the writer searches for hedges like it is worth noting, one might argue, in this regard, and for the nominalization patterns academic writing favors. For a bureaucratic source, the writer searches for words like stakeholders, alignment, going forward, and for the passive-voice responsibility avoidance that bureaucratic writing produces.

The fix when the sweep finds hits is to rewrite the affected sentences in the target voice, without consulting the source. Rewriting in place while the source is still mentally present will often just produce different surface words in the same underlying rhythm; the reliable fix is to close the draft's affected section, consult the target voice's reference in `shared-narrative-voices.md`, and rewrite the section from the Fact Register with the target voice explicitly in mind.

## Gate R9 — Terminology consistent and disambiguated

This gate defends against Terminology Drift. The check asks whether every key term in the draft has exactly one meaning, and whether that meaning is consistent with the resolution recorded in the Fact Register's AMBIGUOUS section.

The writer lists the key terms used in the draft — domain terms, project-specific names, acronyms, component names — and verifies that each is used in one sense throughout. For any term that appeared in the AMBIGUOUS section of the Fact Register, the writer additionally verifies that the draft uses the disambiguated form (for example, "job-worker" and "inference-worker" rather than the overloaded "worker"), and that no claim from the source has silently attached to the wrong sense of the term.

The fix for inconsistent usage is to pick one meaning and rewrite the affected passages. The fix for a claim attached to the wrong sense is more serious — it is a factual error that must be corrected by returning to the user with the disambiguation and reconfirming which sense the original claim referred to.

## Gate R10 — The Anchor Sheet test

The final rewrite-specific gate is a meta-check that verifies the two skills have converged on identical quality standards. The writer extracts the Anchor Sheet that was used to produce the draft and asks a counterfactual question: if a writer using the `tech-writing` skill had been given only this Anchor Sheet with no knowledge of the source, would they have produced a draft substantially similar to this one in argument, structure, voice, and depth?

If the answer is yes, the draft has successfully converged on the blank-page skill's output. The two skills have produced the same quality of work from different starting points, which is the shared-standards property the skill was designed to enforce. If the answer is no — if the draft has properties that betray its rewrite origin — the writer identifies which properties and traces them back to the contamination mechanism that produced them, then returns to Phase 2 or Phase 3 to correct the specific issue.

The Anchor Sheet test is a high-level check, and it catches contamination the more specific gates sometimes miss, especially subtle Structural Mirroring and residual Tone Infiltration that survives the word-level sweeps. It is the last gate run before delivery, after all the specific gates have passed.

## A draft that passes all gates

A draft that passes every gate of the shared checklist and every gate of the rewrite-specific checklist is ready for delivery. It should be indistinguishable in quality from a draft written on the same topic from scratch. The reader should be able to tell what the draft argues, why the argument is sound, and where the boundaries of the claim are. The reader should not be able to tell — from structure, tone, vocabulary, or the shape of the gaps — that the draft was rewritten from a source rather than composed from the Fact Register as an independent effort.

This is the goal of the skill. Every procedure in the workflow, every section of the Fact Register, every gate in the two checklists, exists to produce that specific outcome: a rewrite that meets the same quality bar as blank-page writing on the same topic, because the rewrite was performed with enough discipline to treat the source as raw intelligence rather than as a writing template.