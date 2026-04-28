# Tech Writing - Notion Skill

Use this Skill to write one high-quality technical document from a blank page. It is for technical blog posts, ADRs, design documents, technology comparisons, source or mechanism deep-dives, API docs, and migration guides.

## When To Use

Run this Skill when the user has a topic, argument, decision, or article prompt but no existing draft that should be preserved.

If the user selected an existing draft, notes, meeting transcript, wiki page, or AI-generated text, use `Tech Rewrite - Notion Skill` instead.

## Required Inputs

Ask for missing load-bearing inputs before drafting:

- Topic or working title.
- Document type: blog post, ADR, design doc, comparison, deep-dive, API doc, or migration guide.
- Target reader and what they already know.
- Central argument or decision. If the user only gives a topic, turn it into a falsifiable argument before writing.
- Technical anchors: source links, version numbers, numbers, failure mechanisms, examples, rejected alternatives, and boundaries.
- Desired output page or section, if the user wants the draft placed somewhere specific.

## Workflow

1. Produce an Anchor Sheet before writing prose.
   - Central argument: one falsifiable sentence.
   - Anchors: numbers, version boundaries, source links, concrete examples, failure mechanisms, rejected alternatives, and boundary conditions.
   - Reader audit: who the reader is, what they know, and what they likely misunderstand.
   - Visual explanation plan: reader question, diagram type, and payoff when a diagram is useful.
   - Scope: in scope and explicitly out of scope.
   - Voice: choose exactly one narrative voice.
   - Document type: choose exactly one structure.
2. Show the Anchor Sheet first.
   - If it is thin, say what is missing and ask for the missing input, run research, or narrow scope.
   - Do not fill missing measurements or source facts with invented precision.
3. Draft only after the Anchor Sheet is usable.
   - Put the central argument in the opening.
   - Use the selected voice consistently.
   - Follow the selected document type structure.
   - Add diagrams only when they answer a load-bearing reader question.
   - Pay off every anchor promised in the Anchor Sheet.
4. Validate and revise.
   - Title is concise and professional.
   - Opening passes the 60-second rule.
   - Every comparison ends with a verdict.
   - Every design decision names rejected alternatives.
   - Failure modes describe causal mechanisms.
   - Boundaries include thresholds where possible.
   - No false balance, empty superlatives, background stuffing, generic best practices, or restating conclusion.

## Narrative Voices

- Production War Story: incident, operational lesson, or post-mortem.
- Design Tribunal: ADR, design decision, or technology comparison.
- Mechanism Autopsy: source code, protocol, lifecycle, or internal mechanism.
- Migration Field Guide: upgrade, migration, adoption, rollback, and verification.
- Benchmarker's Notebook: performance comparison with reproducible method.
- Reference Librarian: pure API reference or spec documentation.

## Output Format

Create or update a Notion page with this structure:

```text
# Anchor Sheet
## Central argument
## Anchors
## Reader
## Visual explanation plan
## Scope
## Voice
## Document type

# Draft
[Full document.]

# Validation Notes
- Gates passed:
- Remaining gaps:
- Suggested next edit:
```

When the user asks for a final clean page, remove or collapse the working sections after validation and leave the polished document.

## Stop Rules

Stop and ask before drafting when:

- You cannot state a falsifiable central argument.
- Performance, cost, or scale claims have no numbers.
- ADR, design doc, or comparison work has no rejected alternatives.
- The request is actually two documents joined together.
- The target reader is ambiguous enough to change the structure.
