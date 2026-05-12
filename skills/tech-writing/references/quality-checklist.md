# Quality Checklist

Run this as a validation loop before delivery. A failed gate requires revision, not a footnote, unless the user explicitly accepts the risk.

## Gate 1: Thesis

- The opening paragraph states the central thesis.
- The thesis is falsifiable, scoped, and useful.
- The title reflects the thesis or decision, not a generic topic.

## Gate 2: Anchor Fulfillment

- Every technical anchor in the Anchor Sheet is used in the article.
- Every promised mechanism is explained to the promised depth.
- Every rejected alternative has a concrete rejection reason.
- Every important boundary condition is named.
- Version-specific claims include version context or source uncertainty.

## Gate 3: Structure

- The section order follows the selected narrative strategy.
- The structure is not a fixed "intro/background/concepts/practice/summary" template.
- Each section advances the argument; no section exists only because a generic article would have it.
- The article has a clear limit/boundary discussion when the topic involves operational or architectural risk.

## Gate 4: Visual Plan

- Every diagram promised in the Anchor Sheet is present.
- Each diagram answers one reader question.
- Mermaid syntax is portable and readable.
- No diagram is decorative or overloaded.

## Gate 5: Language Credibility

- No background stuffing in the opening.
- No robotic transition chains.
- No false balance.
- No empty praise.
- No uplifting homework-style ending.
- No passive avoidance where a direct judgment is needed.
- No parallelism overload or slogan clusters.

## Gate 6: Senior Engineer Test

For each section, ask: does this teach a senior engineer something they would not get from five minutes of official docs?

If no, do one of two things:

- cut the section;
- deepen it with mechanism, evidence, boundary, or production implication.

There is no third option.

## Gate 7: Final Consistency

- The ending returns to the thesis and final judgment.
- The article does not introduce new major claims in the conclusion.
- The final article respects the confirmed scope and reader profile.
- Residual assumptions are listed in a short validation note after the article, not hidden in the prose.
