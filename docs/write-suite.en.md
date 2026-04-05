# Write Skills Suite

This suite consists of two companion skills designed to produce consistent, high-quality
technical documentation regardless of the starting point. Whether you are writing from a
blank page or reconstructing from low-quality source material, both skills apply identical
writing standards so that the output is indistinguishable in quality, voice, and structure.

---

## The Two Skills

### `tech-writing` — Write from Scratch

Use this skill when you have a topic, a thesis, or a technical decision to document, but
no existing material to work from. The skill runs a mandatory Pre-Writing Protocol before
generating any prose: it forces you (and the model) to articulate a central argument, collect
concrete technical anchors, audit the reader's existing beliefs, declare scope boundaries,
and select a narrative voice. Only after this brief is complete does writing begin.

The risk this skill guards against is **anchor starvation** — the tendency for AI writing
without a specific technical grounding to drift toward encyclopedic, opinion-free output
that describes what things are without making any judgment about what they mean.

**Trigger phrases:** "write a blog post about X", "draft an architecture doc for Y",
"compare X and Y", "write an ADR", "explain how X works in depth", "create API docs for Z".

---

### `tech-rewrite` — Reconstruct from Existing Material

Use this skill when you have source material of any quality — internal notes, meeting
summaries, AI-generated drafts, legacy wikis, code comments, or early-stage documents —
that needs to be transformed into high-quality technical documentation.

The skill enforces a strict quarantine between the extraction phase and the writing phase.
Source material is never treated as a writing template. It is processed as raw intelligence:
facts are extracted into a structured Fact Register, vague claims are explicitly discarded,
quality problems are diagnosed, and contamination risks are named before a single sentence
of output is written.

The risk this skill guards against is **style contamination** — the seven specific mechanisms
by which low-quality source material corrupts the output even when the writer intends to
improve it. These include structural mirroring, void inheritance, vagueness laundering,
tone osmosis, rationale elision, false completeness, and scope inflation.

**Trigger phrases:** "rewrite this doc", "clean up my notes", "this draft is bad, fix it",
"turn this into a proper article", "based on this material, write a doc about X",
"improve this documentation".

---

## Shared Standards

Both skills produce output governed by the same quality rules. A document produced by
`tech-rewrite` and a document produced by `tech-writing` on the same topic should be
indistinguishable in quality. The shared standards include:

**Structural standards.** Every document has an argument-bearing title, a header block with
scope and prerequisites, and an opening paragraph that states the central argument within
the first 60 seconds of reading. Every comparison section ends with a verdict. Every
architectural or design decision includes rejected alternatives and their reasons.

**Depth standards.** Every document contains a failure modes section with specific
mechanisms (not categories), and a limitations section that bounds the recommendation.
The senior engineer test applies: if a section teaches nothing that isn't already in the
official documentation, it is either deepened or cut.

**Voice standards.** Four narrative voices are defined (Production War Story, Design
Tribunal, Mechanism Autopsy, Migration Field Guide). One is selected per document and
maintained consistently throughout. AI-smell patterns — false balance, hollow superlatives,
background stalls, passive responsibility evasion — are explicitly prohibited with specific
detection and correction rules.

**Language standards.** For Chinese technical writing: technical proper nouns remain in
English, the register targets a senior engineer explaining a hard problem to a peer in
a design review (not bureaucratic, not casual), and conclusions lead (argument first,
evidence second). For English writing: Anglo-Saxon word choices are preferred, precision
takes precedence over brevity.

---

## Recommended Usage Templates

The following templates are the recommended starting points for each major document type.
Copy the relevant template, fill in the bracketed fields, and submit to the appropriate skill.

---

### Template A — Technical Blog Post / Deep-Dive Analysis
*Use with: `tech-writing`*

```
Write a technical blog post.

TOPIC: [specific technology, decision, or mechanism]

CENTRAL ARGUMENT: [one sentence — the claim the article will defend, not just the topic]
Example: "In SSE-heavy AI inference services, WebFlux is not merely an option — it is the
only architecture that avoids thread pool exhaustion at scale."

TARGET READER:
- Role: [e.g., Java backend engineer, platform architect]
- Experience level: [junior / mid / senior]
- What they already know: [prerequisite knowledge]
- What they probably believe now: [their current assumption this article may challenge]

DEPTH: [Surface / Standard / Deep]
- Surface: explain what and why, no implementation details
- Standard: key implementation patterns and configuration examples
- Deep: internal mechanism analysis, failure mode dissection, production configuration with rationale

REQUIRED COVERAGE (address all of these, with a judgment on each):
1. [topic 1]
2. [topic 2]
3. [topic 3]

EXPLICIT OUT OF SCOPE:
- [what to exclude]

LANGUAGE: [Chinese / English]
```

---

### Template B — Architecture Decision Record (ADR)
*Use with: `tech-writing`*

```
Write an Architecture Decision Record.

DECISION TITLE: [verb phrase — e.g., "Adopt WebFlux for AI inference service layer"]

CONTEXT:
[Describe the specific problem and constraints. What breaks if no decision is made?
What are the non-negotiable requirements? 2–4 sentences.]

THE DECISION: [state the chosen approach in one sentence]

ALTERNATIVES CONSIDERED:
- [Alternative 1]: [why considered, why rejected]
- [Alternative 2]: [why considered, why rejected]

KEY CONSTRAINTS THAT SHAPED THIS DECISION:
- [constraint 1: e.g., "must sustain 500 concurrent SSE connections on 4 vCPUs"]
- [constraint 2]

CONSEQUENCES TO DOCUMENT:
- Positive: [what this enables]
- Negative: [what this forecloses — be honest]
- Risks: [conditions that would make this decision wrong in the future]

LANGUAGE: [Chinese / English]
```

---

### Template C — Module / Component Design Document
*Use with: `tech-writing`*

```
Write a module design document.

MODULE NAME: [name]
SCOPE: [one sentence — what this module does and what it explicitly does not do]

TARGET READER: [role and experience level of the engineer who will implement or extend this]

DESIGN CONSTRAINTS (non-negotiable requirements that shaped this design):
- [constraint 1: e.g., "must be stateless — no local state between requests"]
- [constraint 2]
- [constraint 3]

KEY DESIGN DECISIONS TO DOCUMENT (for each, include rejected alternatives):
1. [decision 1]
2. [decision 2]

INTERFACE CONTRACT TO DOCUMENT:
- Public API: [method signatures or endpoint patterns]
- Events emitted: [if applicable]
- Dependencies: [what this module requires from others, as contracts]

FAILURE MODES TO COVER:
- [failure scenario 1]
- [failure scenario 2]

LANGUAGE: [Chinese / English]
```

---

### Template D — Technology Comparison / Selection Guide
*Use with: `tech-writing`*

```
Write a technology comparison and selection guide.

SELECTION CONTEXT: [the specific scenario that makes this comparison necessary]
Example: "Selecting a caching layer for a multi-region API with sub-10ms read latency
requirements and eventual consistency tolerance."

OPTIONS TO COMPARE:
- Option A: [name + one sentence on what it is]
- Option B: [name + one sentence on what it is]

EVALUATION CRITERIA (rank by importance for this context):
1. [criterion 1: e.g., "read latency under 1,000 concurrent requests"]
2. [criterion 2: e.g., "operational complexity for a team without dedicated infrastructure engineers"]
3. [criterion 3]

THE ANSWER I SUSPECT BUT WANT CHALLENGED OR CONFIRMED:
[e.g., "I think Redis is the obvious choice, but I want to know if there are scenarios
where Memcached wins enough to be worth the operational split."]

EXPLICIT OUT OF SCOPE: [what not to cover]
LANGUAGE: [Chinese / English]
```

---

### Template E — Rewrite / Reconstruction from Existing Material
*Use with: `tech-rewrite`*

```
Rewrite the following document.

DOCUMENT TYPE OF OUTPUT: [Technical Blog / Architecture Doc / ADR / Module Design / API Reference]

TARGET READER OF OUTPUT:
- Role: [e.g., mid-level Java engineer unfamiliar with reactive programming]
- What they need to be able to do after reading: [one sentence — specific capability or decision]

WHAT I KNOW IS WRONG WITH THE SOURCE (optional but helpful):
- [e.g., "The failure modes section is missing entirely"]
- [e.g., "The rationale for choosing Kafka is never explained"]
- [e.g., "The structure mirrors our internal ticket format, not a logical reading flow"]

CONSTRAINTS I WANT PRESERVED:
- [e.g., "The technology choices are final — do not question them, only explain them"]
- [e.g., "This must remain under 1,500 words"]

ADDITIONS I WANT CONSIDERED:
- [e.g., "Add a section on failure modes — I know the main ones are X and Y"]

LANGUAGE OF OUTPUT: [Chinese / English]

---

[PASTE SOURCE MATERIAL BELOW THIS LINE]
```

---

### Template F — Clean Up Notes / Rough Draft into Article
*Use with: `tech-rewrite`*

```
Turn the following notes into a technical blog post.

INTENDED ARGUMENT: [what you want the article to argue — even if the notes don't say it clearly]

TARGET READER: [who will read the finished article]

WHAT THE NOTES CONTAIN: [brief description — e.g., "meeting notes from an architecture
review, plus some scattered code comments and a partial decision log"]

WHAT I WANT ADDED THAT ISN'T IN THE NOTES:
- [e.g., "The failure mode we hit in production — Redis OOM under 10k concurrent sessions"]

WHAT I DO NOT WANT IN THE OUTPUT:
- [explicit exclusions]

LANGUAGE OF OUTPUT: [Chinese / English]

---

[PASTE NOTES / DRAFT BELOW THIS LINE]
```

---

## Skill Selection Quick Reference

| Starting point | Document type | Skill to use |
|---|---|---|
| Topic + opinion, no source material | Blog post, deep-dive | `tech-writing` |
| Architecture decision to record | ADR | `tech-writing` |
| New module to design and document | Module design doc | `tech-writing` |
| Technology selection to justify | Comparison guide | `tech-writing` |
| Existing doc with quality problems | Any type | `tech-rewrite` |
| AI-generated draft that needs improvement | Any type | `tech-rewrite` |
| Meeting notes / internal wiki | Blog post, design doc | `tech-rewrite` |
| Code comments + scattered notes | Module doc, ADR | `tech-rewrite` |
| Source material exists but is partial | Any type | `tech-rewrite` |

When in doubt: if you have existing written material, use `tech-rewrite`. If you are
starting from a topic and an opinion, use `tech-writing`.

---

## A Note on Quality Consistency

The reason both skills share identical writing standards rather than each defining their
own is that quality should be a function of the output, not of the production method.
A reader of a finished document should not be able to tell whether it was written from
scratch or reconstructed from poor source material. If the reconstruction is detectable
— if it reads like a "cleaned-up version" of something rather than a first-class document
— the `tech-rewrite` process was not applied correctly and the contamination patterns
reference should be consulted before proceeding.