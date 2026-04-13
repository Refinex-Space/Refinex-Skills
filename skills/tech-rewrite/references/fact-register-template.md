# Fact Register template

This file contains the canonical template for the Fact Register produced during Phase 1 of the tech-rewrite workflow. The template is the working document — fill it in as extraction proceeds — and it is the only permitted bridge between the source material and the writing phase.

The template has four sections and a contamination risk assessment. Every Fact Register uses this format, regardless of the source type or target document type. The uniformity matters because it lets the writer treat the Fact Register as an interface: the writing phase operates on a Fact Register of the expected shape, without needing to know what kind of source produced it.

## The template

```
# Fact Register: <working title or topic>

Source: <identifier — file name, URL, meeting date, etc.>
Extracted by: <name or identifier>
Extraction date: <YYYY-MM-DD>
Target document type (tentative): <blog-post | adr | design-doc | comparison | deep-dive | api-doc | migration-guide>

## KEPT

Every concrete, verifiable, load-bearing claim from the source, stated in
the extractor's own words. Strip all stylistic cues from the source.

Each entry uses this format:

N. [source: <provenance>] <the claim, stated plainly>
   - Hedge level: <flat | approximate | hedged | uncertain>
   - Relevance: <load-bearing | supporting | background>
   - Notes: <optional — units, caveats, related entries>

Examples:

1. [source: para 3, code block] The cache uses an off-heap allocator
   (sun.misc.Unsafe) to avoid GC pressure.
   - Hedge level: flat
   - Relevance: load-bearing

2. [source: Alice in meeting, 2026-03-14] p99 latency is approximately
   180ms, up from ~80ms in the previous quarter.
   - Hedge level: approximate (casual numbers, not measured formally)
   - Relevance: load-bearing
   - Notes: the 80ms baseline is from memory; 180ms is from current dashboards

3. [source: README section "Limitations"] The cache supports a maximum
   key size of 512 bytes.
   - Hedge level: flat
   - Relevance: supporting

## DISCARDED

Every vague, unsubstantiated, hedged-without-support, or evaluative claim
from the source, with a specific reason for rejection. These claims are
unavailable to the writing phase.

Each entry uses this format:

- "<exact or paraphrased claim>" [source: <provenance>] — <reason for rejection>

Examples:

- "The cache delivers blazing-fast performance." [source: para 1] —
  evaluative, no number, no baseline
- "The team has been working hard on this." [source: para 4] —
  irrelevant, not a technical claim
- "It should scale well." [source: para 6] — hedged ("should"),
  no load figure, no scale threshold
- "Most users will be happy with the defaults." [source: para 8] —
  evaluative ("happy"), no user research cited

## MISSING

Every load-bearing piece of information that a strong document on this
topic would need but that the source does not supply. Each entry names
the gap and (where possible) suggests how it might be filled.

Each entry uses this format:

- <the gap, named specifically>
  - Why it matters: <load-bearing role it would play in the target document>
  - How to fill it: <user input | research | scope out | lookup tool>

Examples:

- The failure mode under network partition between the L1 and L2 cache tiers.
  - Why it matters: the target is a design document; failure modes are
    a required section, and this specific failure mode is load-bearing
    because the design depends on L2 for consistency.
  - How to fill it: ask user (this is an internal design decision they
    must know) or scope out (narrow the target to L1 behavior only).

- Benchmark numbers comparing the custom cache to Redis at the same
  workload.
  - Why it matters: the proposed central argument is that the custom
    cache is worth the operational cost; without numbers, the argument
    cannot be made.
  - How to fill it: user input (if measured), research (if benchmark
    published), or scope out (drop the performance comparison from the
    target and recommend the cache on non-performance grounds only).

- Rejected alternatives considered during the original design.
  - Why it matters: the target is an ADR; rejected alternatives are a
    mandatory section.
  - How to fill it: ask user.

## AMBIGUOUS

Every claim in the source that the extractor cannot interpret without
guessing. Each entry records both plausible interpretations and notes the
impact of the ambiguity on the target document.

Each entry uses this format:

- "<exact or paraphrased claim>" [source: <provenance>]
  - Interpretation A: <...>
  - Interpretation B: <...>
  - Impact: <how much the target depends on picking the right interpretation>
  - Resolution: <pending user input | dropped as non-material | resolved by cross-reference>

Examples:

- "The worker handles retries automatically." [source: para 5]
  - Interpretation A: the job-worker processes (from earlier in the source)
    retry failed jobs automatically
  - Interpretation B: the inference-worker processes (introduced mid-document)
    retry failed inference requests automatically
  - Impact: high — the two worker types have different retry semantics,
    and claims about retries need to be associated with the right one
  - Resolution: pending user input

## Contamination risk assessment

Rate the source against each of the ten contamination mechanisms. For each
rating, name specific evidence from the source. Ratings are low, medium,
or high. A rating of HIGH triggers a specific defensive move in Phase 2
or Phase 3 — see contamination-risk-assessment.md for the playbook.

1. Structural Mirroring: <LOW | MEDIUM | HIGH>
   Evidence: <...>
   Defense if HIGH: <...>

2. Void Inheritance: <LOW | MEDIUM | HIGH>
   Evidence: <...>
   Defense if HIGH: <...>

3. Ambiguity Whitewashing: <LOW | MEDIUM | HIGH>
   Evidence: <...>
   Defense if HIGH: <...>

4. Tone Infiltration: <LOW | MEDIUM | HIGH>
   Evidence: <...>
   Defense if HIGH: <...>

5. Rationale Vacuum: <LOW | MEDIUM | HIGH>
   Evidence: <...>
   Defense if HIGH: <...>

6. False Completeness: <LOW | MEDIUM | HIGH>
   Evidence: <...>
   Defense if HIGH: <...>

7. Scope Inflation: <LOW | MEDIUM | HIGH>
   Evidence: <...>
   Defense if HIGH: <...>

8. Confidence Upgrade: <LOW | MEDIUM | HIGH>
   Evidence: <...>
   Defense if HIGH: <...>

9. Terminology Drift: <LOW | MEDIUM | HIGH>
   Evidence: <...>
   Defense if HIGH: <...>

10. Pseudoanchor Import: <LOW | MEDIUM | HIGH>
    Evidence: <...>
    Defense if HIGH: <...>

## Handoff note to Phase 2

Short summary of what the writer needs to know before drafting:

- Unresolved MISSING items that block progress: <...>
- Unresolved AMBIGUOUS items that block progress: <...>
- HIGH contamination risks with required defensive moves: <...>
- Proposed central argument (if clear from extraction): <...>
- Proposed target voice (if clear from extraction): <...>
- Visual candidates worth planning in Phase 2: <mechanism / topology / state / timeline + why prose alone would be expensive>
- Source is now CLOSED. All further work proceeds from the Fact Register alone.
```

## Rules for populating the template

Four rules govern how the template is filled in. The rules exist to prevent the template from becoming a checkbox exercise — the template is only valuable if the extractor follows the rules with discipline.

The first rule is that claims in KEPT are rewritten in the extractor's own words, not copied from the source. The rewrite strips stylistic residue, marketing vocabulary, and sentence rhythm. The rewrite is factually faithful but stylistically neutral. A KEPT entry that preserves the source's phrasing has already imported contamination into the register, and the contamination will propagate from there into the writing phase.

The second rule is that provenance is mandatory. Every KEPT entry, every DISCARDED entry, every AMBIGUOUS entry records where it came from in the source. The provenance tag is how the writer later traces a question back to the original context if needed, and how any post-hoc verification is possible. A Fact Register without provenance is an untraceable document and fails its role as an intermediate.

The third rule is that the hedge level in KEPT is recorded at the level the source stated the claim, not at the level the extractor wishes the source had stated it. If the source said "about 40%", the hedge level is "approximate", not "measured". If the source said "probably", the hedge level is "uncertain". Preserving the hedge level during extraction is the defense against Confidence Upgrade during writing — the writer cannot flatten a hedge that is not in the KEPT entry.

The fourth rule is that MISSING is populated by reference to the target document type, not by reference to the source. The extractor consults the shared doctype file for the tentative target type and uses its expected sections and quality gates as a checklist. Items the source does not supply are added to MISSING. This is the only way to catch Void Inheritance — the extractor has to be thinking about the target, not about the source, at the moment MISSING is being populated.

## When to produce a shorter Fact Register

The template is the maximum shape. Some Fact Registers can be shorter. The minimum is a Fact Register with all four sections and a risk assessment; the four sections can be short but must not be skipped. A Fact Register that omits the DISCARDED section, or leaves MISSING empty without evidence that the source was comprehensive, or skips the risk assessment, has failed its role.

A short Fact Register is appropriate when the source is itself short and dense with concrete facts. A 200-word source with mostly measured claims might produce a Fact Register with six KEPT entries, one or two DISCARDED, three or four MISSING, no AMBIGUOUS, and a risk assessment. That is a complete register.

A long Fact Register is appropriate when the source is long, loose, or contaminated. A 5000-word source with many vague claims, inconsistent terminology, and multiple distinct topics might produce a Fact Register with thirty KEPT entries, fifteen DISCARDED, twenty MISSING, and five AMBIGUOUS, plus a risk assessment with several HIGH ratings. That is also a complete register, just for a harder source.

The size of the Fact Register is determined by the source, not by the extractor's patience. A Fact Register that feels "too short" for a long source is almost always incomplete. A Fact Register that feels "too long" for a short source is either fine (the source was dense) or a sign that the extractor is copying from the source rather than selecting.
