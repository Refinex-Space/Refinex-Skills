# Doctype: Architecture Decision Record (ADR)

An ADR captures one architecturally significant decision, its context, the alternatives considered, and the consequences. It is written to be read by future engineers — typically by someone joining the team six months from now who needs to understand why the current system is the way it is, without having been in the original meeting. The ADR is a letter to that future engineer.

## The two canonical formats

Two formats dominate and are both widely used. Pick one per project and stay consistent; do not mix formats in the same repository.

**Nygard format** (from Michael Nygard's original 2011 post) is the minimalist version and remains the most common. It has five required sections: Title, Status, Context, Decision, and Consequences. It is short, easy to write, and readable in under two minutes. Use it when the team wants a lightweight decision log and when the alternatives do not need detailed weighing.

**MADR format** (Markdown Architectural Decision Records) is the structured extension. It keeps Nygard's sections and adds explicit "Considered Options" and "Decision Outcome with rationale" sections. Use it when alternatives matter enough that the reader needs to see the weighing, which is often the case for decisions with multiple reasonable paths.

When in doubt, pick MADR. Making the alternatives explicit is the single most valuable thing an ADR can do for its future reader, and the extra structure helps enforce it.

## Nygard structure (required sections)

**Title.** A short noun phrase that describes the decision, not the problem. Number the ADR sequentially from the start of the project. "ADR 0017: Use PostgreSQL as the primary data store for the ledger service" is a good title. "ADR 0017: Database choice" is not — it does not say what was chosen. "ADR 0017: Why we need a database" is not — it describes a problem, not a decision.

**Status.** One of: Proposed, Accepted, Deprecated, Superseded by ADR NNNN. The status line is updated as the ADR moves through its lifecycle. A superseded ADR is never deleted; it is marked as superseded with a link to its replacement, so the reason for the original decision remains visible. This is the historical-record property of ADRs and it is load-bearing — deleting old decisions breaks the record.

**Context.** The forces at play. This section describes the technological, organizational, and project-local factors that made the decision necessary. The language is value-neutral: it describes facts, not opinions. The context answers the question "why did we have to make a decision at all". Good context sections are concrete and quantitative where possible — they name the load, the team size, the deadline, the regulatory requirement, the downstream dependency, whatever actually forced the decision. A context section that says "we needed to choose a database" is too abstract; it should say what specific constraints made the choice necessary.

**Decision.** The response to the forces in the Context. Written in full sentences, active voice, and the form "We will...". The decision section is short and direct: it names what will be done. Hedging and conditionals belong in Consequences, not in Decision. If the decision is "We will use PostgreSQL", that is the whole first sentence of this section, not the eighth.

**Consequences.** The resulting context after the decision is applied. This section describes what becomes easier, what becomes harder, and what new risks or obligations the decision creates. Consequences are neutral — they include both positive and negative effects. A Consequences section that lists only benefits is incomplete. The writer's goal is honesty, not salesmanship: the future reader needs to see the tradeoffs the current team accepted, not a sanitized version of them.

## MADR extensions

MADR adds two sections between Context and Decision, both of which make the decision reasoning visible rather than implicit.

**Considered Options.** A list of the alternatives that were genuinely evaluated. Each alternative gets at least one sentence. For alternatives that were seriously considered, include a short summary of what the option would have looked like in practice. For alternatives that were quickly set aside, state the reason for setting them aside.

**Decision Outcome.** The chosen option, followed by the rationale. The rationale explicitly weighs the chosen option against the considered alternatives — it says which criteria mattered, how each option performed against those criteria, and why the winner won. This section is where the ADR earns its keep, because it converts a decision from "trust us, this was the right call" into "here is the reasoning, judge it for yourself".

## Voice

ADRs use the Design Tribunal voice. The writer is stating a decision and defending it against alternatives. First-person plural is standard ("We will..."), and the tone is direct and judgmental in the best sense of the word — the writer has weighed options and picked one.

Avoid tutorial voice, marketing voice, and apologetic voice. The ADR is a professional communication between peers across time, not a sales pitch and not a confession.

## Length

Most ADRs fit on one or two pages. An ADR longer than three pages is usually a design document in disguise and should be split: the decision goes in the ADR, and the implementation detail goes in a separate design document that the ADR links to.

## Gates specific to ADRs (run in addition to the main checklist)

The following gates must pass before an ADR is delivered. They check properties that are easy to miss but critical to the document's long-term value.

First, confirm that the title names the decision, not the problem. A title like "Database choice" fails; "Use PostgreSQL for the ledger service" passes. The distinction matters because ADRs are indexed by title in the decision log, and a reader scanning the index should be able to tell from each title what was decided.

Second, confirm that the Status field is present and accurate. An ADR without a status is ambiguous — the reader cannot tell whether the decision is a proposal or an accepted standard. If the ADR is replacing an earlier one, verify that the earlier one has been marked as superseded with a link to the new ADR.

Third, check the Context section for concreteness. The section should name specific constraints, not abstract considerations. A context section that reads like a generic introduction to the problem domain is a failure; the reader should be able to tell from the Context alone why this particular team had to make this particular decision at this particular time.

Fourth, verify that the Decision section is written in the "We will..." form and is short. A Decision section that rambles has usually absorbed material that belongs in Consequences or in an implementation plan. Move that material and keep the Decision itself crisp.

Fifth, check that the Consequences section includes both positive and negative effects. A Consequences section that is entirely positive is incomplete and dishonest. The future reader needs to see the cost the current team accepted, not just the benefits the current team hoped for.

Sixth, if the ADR is in MADR format, verify that the Considered Options section names at least two alternatives other than the chosen one, and that each alternative has a specific reason for being set aside. "Not a good fit" is not a reason; "does not support strict serializable isolation across multi-row updates, which is a regulatory requirement for the ledger service" is a reason.

Seventh, verify that the ADR is written as prose with full sentences, not as a bullet-point outline. Nygard's original post is explicit on this point: bullets are acceptable for visual style but not as a substitute for sentences. An ADR that is entirely bullet-pointed has usually skipped the work of weighing the tradeoffs in connected prose.

## Common failure patterns

The most common failure is the **missing Context section**. The writer jumps straight to the Decision because "everyone on the team knows why we needed to make this choice". Six months later, when the original team has turned over, no one remembers why. The Context section exists to survive the team's memory loss.

The second most common failure is the **sales-pitch Consequences section** that lists only benefits. This pattern is usually unconscious — the writer has just made the decision and is feeling good about it, and the resulting Consequences section reflects that optimism. The fix is discipline: for every benefit, find the corresponding cost and write it down. An honest ADR reads as even-handed even when the decision is clearly correct.

The third failure is the **ADR that is actually a design document**. It has extensive technical detail, API contracts, data models, and sequence diagrams. That is all good material, but it does not belong in an ADR — it belongs in a design document that the ADR links to. An ADR is a compressed record of a decision; a design document is an extended treatment of a system. Mixing them produces a document that is too long to serve as a quick decision log and too shallow to serve as a full design spec.