# Tech Rewrite - Notion Skill

Use this Skill to turn existing material into a publication-quality technical document. It is for rough notes, meeting notes, legacy wiki pages, AI drafts, code comments, research notes, transcripts, and partial drafts.

## When To Use

Run this Skill when the user selects text or points to an existing Notion page that should be rewritten, restructured, cleaned up, formalized, or turned into a stronger article.

If there is no source material, use `Tech Writing - Notion Skill` instead.

## Required Inputs

Ask for missing load-bearing inputs before rewriting:

- Source material: selected text, current page, linked page, or pasted notes.
- Target document type: blog post, ADR, design doc, comparison, deep-dive, API doc, or migration guide.
- Target reader.
- Desired outcome: polished rewrite, structural review first, shortened version, expanded version, or publish-ready page.
- Whether the original wording must be preserved for legal, compliance, or authorship reasons.

## Workflow

1. Build a Fact Register before designing the new document.
   - KEPT: concrete, verifiable claims from the source, rewritten neutrally and with provenance.
   - DISCARDED: vague, unsupported, irrelevant, or purely stylistic claims, with reasons.
   - MISSING: load-bearing information the target document needs but the source lacks.
   - AMBIGUOUS: claims that cannot be interpreted without guessing.
2. Assess contamination risk.
   - Structural Mirroring.
   - Void Inheritance.
   - Ambiguity Whitewashing.
   - Tone Infiltration.
   - Rationale Vacuum.
   - False Completeness.
   - Scope Inflation.
   - Confidence Upgrade.
   - Terminology Drift.
   - Pseudoanchor Import.
3. Close the source.
   - Do not draft by re-reading the source from top to bottom.
   - Work from the Fact Register as the bridge between source and output.
   - If something is missing, add it to MISSING and resolve it by asking, researching, or scoping it out.
4. Produce an Anchor Sheet from the Fact Register.
   - Central argument.
   - Anchors.
   - Reader audit.
   - Visual explanation plan.
   - Scope.
   - Voice.
   - Document type.
5. Draft and validate under the same standards as `Tech Writing - Notion Skill`.
   - Do not inherit the source structure unless it is justified by the target argument.
   - Do not upgrade hedged claims into confident claims.
   - Do not keep vague claims merely because they sound polished.
   - Pay off every KEPT load-bearing claim or explicitly scope it out.

## Output Format

Create or update a Notion page with this structure:

```text
# Fact Register
## KEPT
## DISCARDED
## MISSING
## AMBIGUOUS

# Contamination Risk Assessment

# Anchor Sheet
## Central argument
## Anchors
## Reader
## Visual explanation plan
## Scope
## Voice
## Document type

# Rebuilt Draft
[Full document.]

# Validation Notes
- Shared writing gates passed:
- Rewrite-specific gates passed:
- Remaining gaps:
```

When the user asks for a final clean page, keep the Fact Register in a collapsed section or a linked evidence page when traceability matters; otherwise leave only the polished document.

## Stop Rules

Stop and ask before drafting when:

- MISSING items are required for the target argument.
- AMBIGUOUS items materially change the claim.
- The source combines multiple documents that should be split.
- The requested target type does not match the available evidence.
- The user expects preservation of wording, but the rewrite would need structural redesign.
