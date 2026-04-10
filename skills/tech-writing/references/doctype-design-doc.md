# Doctype: Architecture Design Document

A design document proposes a new system or a significant change to an existing one. It is written before implementation begins, circulated for review, and used to align stakeholders on the plan before code is written. The canonical reference is the Google-style design doc, which is the model this file follows.

Unlike an ADR, which captures a single decision, a design document describes a whole system or subsystem. It is longer, more detailed, and aimed at a wider audience that typically includes engineers who will implement the system, reviewers from adjacent teams, and senior engineers or managers who need to approve the approach.

## The purpose of a design document

A design document exists to pull coordination overhead forward in time. The cost of finding a design flaw during review is low; the cost of finding the same flaw during implementation is higher; the cost of finding it in production is highest. The design document is the venue where flaws are found cheaply, and its structure is tuned to surface them.

This framing has a consequence that often surprises writers: the design document is not primarily a record of what will be built. It is primarily an invitation to be critiqued. A design document that sails through review with no comments is almost always a design document that was not read carefully; the writer should be suspicious rather than pleased.

## Required structure

The Google-style design document has the following sections. The order is approximately fixed; deviations are allowed but should be deliberate.

**Title, authors, status, and date.** The metadata block at the top. Status is one of: Draft, In Review, Approved, Implemented, Obsolete. The date is the last-updated date, not the creation date. Authors are listed as primary contacts.

**Context and scope.** A short section, usually one to three paragraphs, that establishes why the design is necessary. The context answers "what is the situation that made this design worth doing", and the scope answers "what aspect of that situation are we addressing here". The scope is narrow by design; it is the writer's first chance to say what the document is *not* about.

**Goals.** An explicit list of the goals the design must achieve. Each goal should be concrete enough that a reviewer can tell, at the end of the review, whether the design achieves it. "Improve latency" is too abstract; "reduce p99 latency on the profile-view endpoint from 2.1s to under 1s" is concrete.

**Non-goals.** This section is as important as the Goals section, and it is often underweighted. Non-goals are things that could reasonably be goals but have been explicitly set aside. They are not absurdities ("the system shouldn't crash"); they are real, plausible objectives that have been deprioritized for specific reasons. Stating non-goals prevents the reviewer from asking "but what about X?" and lets the writer say "yes, we thought about X and chose not to pursue it in this design, because of reason Y."

**Overview.** A short, high-level description of the proposed design. One to three paragraphs. The overview should give the reader enough to decide whether to read the detailed design, and enough context to understand the detailed design when they get to it. Diagrams are common in this section and earn their keep if they carry information that prose cannot carry efficiently — a system context diagram, a sequence diagram, or a data flow diagram.

**Detailed design.** The longest section of the document. It describes the proposed system in enough detail that a reviewer can find flaws and an implementer can build it without further design work. The structure of this section varies by the kind of system being designed; there is no single right layout. For most systems, the detailed design breaks into subsections by component, by phase, or by layer, and each subsection describes the proposed behavior, the data structures, the interfaces, and the failure handling.

The level of detail should match the reviewers' need to catch design flaws. Too little detail and the reviewers cannot evaluate the design; too much detail and the document becomes an implementation manual that no one will read. A useful heuristic: include a design or implementation decision if it could provoke significant discussion in code review. Decisions that would not provoke discussion can be left to implementation.

**Alternatives considered.** Every design document must include this section, and it must be substantive. For each alternative, describe what the option would have looked like in practice, and explain the specific tradeoffs that led to the chosen design. Alternatives should include both "do nothing" (because sometimes the best move is to not build anything) and at least one meaningful alternative architecture, not just straw versions of the chosen design.

A design document without alternatives considered is not a design document; it is an implementation manual. It is missing the step where the author justifies the chosen path against other plausible paths.

**Cross-cutting concerns.** Sections that cover concerns which affect the whole system rather than a specific component. The standard list includes security, privacy, observability, testing, operations, and cost. Not every design needs all of these sections, but the writer should explicitly consider each one and include the sections that apply. For a design that touches user data, privacy is not optional. For a design that runs in production, observability and operations are not optional.

**Rollout plan.** How the design will be deployed. This section is most valuable for changes to existing systems, where the rollout itself is a source of risk. It includes the migration steps, the rollback plan, the feature flags or gradual rollout mechanism, and the criteria for declaring the rollout successful or rolling back.

**References.** Links to related documents, prior discussions, relevant ADRs, external standards, and any other material the reviewer might need to read to evaluate the design.

## Voice

Design documents use a neutral, professional register. The stance is Design Tribunal applied to the writer's own proposal: the writer is presenting a design for critique and must weigh it against alternatives with the same rigor they would apply to an outside proposal.

First-person plural is standard. The writer is speaking for the team even if only one person wrote the document. Hedging and conditional language are acceptable in the Alternatives Considered section (where the writer is describing paths that could have been taken) but should be firm in the Decision-equivalent parts of the Detailed Design section (where the writer is committing to the chosen path).

## Length

Design documents are usually several pages. Ten to thirty pages is typical for a moderately complex system; a design for a major new subsystem can run longer. The length should match the scope of what is being designed, not the writer's desire to look thorough.

A design document that is too short usually indicates that the writer has not done enough design work before writing. A design document that is too long usually indicates that the writer has included material that belongs elsewhere: implementation details that belong in code, API contracts that belong in a separate spec, or extensive background that belongs in a separate orientation document.

## Gates specific to design documents

Before delivering a design document, verify each of the following. These gates check structural and substantive properties that are easy to miss.

First, verify that the Goals section lists goals that are measurable or at least verifiable. A reviewer should be able to look at the finished system and determine whether each goal was achieved. Goals that are too abstract to verify are signals that the writer has not thought the scope through.

Second, verify that the Non-Goals section is not empty, and that the non-goals are plausible objectives rather than absurdities. If the non-goals are things no one would have expected, they are padding. Good non-goals are things a reviewer might actually have asked about.

Third, verify that the Alternatives Considered section names at least two substantive alternatives, and that each alternative is described specifically enough that a reviewer could evaluate whether the rejection was reasonable. Vague dismissals ("this would be too slow") are insufficient; the reasons must be concrete.

Fourth, verify that the cross-cutting concerns relevant to the system have been addressed. For systems that handle user data, check for a privacy section. For systems that run in production, check for observability and operations sections. For systems that are externally exposed, check for security. A missing cross-cutting section for a relevant concern is a red flag that the writer has not thought about that dimension.

Fifth, verify that the Detailed Design section is at the right level of abstraction. It should be specific enough that an implementer could start without further design work, but not so specific that the document becomes a line-by-line code plan. The test is whether a careful reviewer would be able to find design flaws — if the level of detail is too high, flaws hide; if it is too low, flaws are masked by implementation noise.

Sixth, verify that the Rollout Plan section exists for any design that modifies an existing production system. A design without a rollout plan has assumed a clean deployment, which is almost never realistic for non-trivial changes.

## Common failure patterns

The most common failure is the **implementation manual masquerading as a design document**. The document describes how to build the system in extensive detail but does not justify the architectural choices against alternatives. It is useful to an implementer who has already accepted the design, but it does not serve as a vehicle for critique. The fix is to step back and add the missing justification — the Alternatives Considered section, the reasoning behind the component boundaries, the explicit tradeoffs the writer accepted.

The second most common failure is the **sales pitch**. The document describes the proposed design entirely in positive terms and treats alternatives as straw versions of the chosen design. It reads as if the writer has already decided and is asking for rubber-stamp approval rather than genuine review. The fix is to rewrite the Alternatives Considered section with alternatives described in their own best form — a reviewer should be able to tell that the writer understood the alternatives and weighed them honestly.

The third failure is the **missing non-goals section**. The writer has listed goals but has not said what is out of scope. Reviewers then spend cycles asking about things the writer never intended to cover, and the review becomes less efficient than it could have been. The fix is to write the non-goals section deliberately, not as an afterthought — it should reflect real decisions the writer made about what this design does and does not attempt.

The fourth failure is **level-of-detail drift across sections**. Some sections of the detailed design are highly specific; others are hand-wavy. The uneven level of detail usually reflects the writer's comfort level — they went deep where they had strong opinions and stayed shallow where they did not. The fix is to level out the depth, which often means doing additional design work for the hand-wavy sections before finalizing the document.