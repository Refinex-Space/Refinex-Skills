# Tech Planner - Notion Skill

Use this Skill to plan a professional multi-article technical series inside Notion. It is for series outlines, learning roadmaps, content calendars, and article backlogs.

## When To Use

Run this Skill when the user names a framework, library, protocol, product, architecture topic, or engineering practice and asks for a series plan.

Do not use it for one standalone article. Use `Tech Writing - Notion Skill` instead.

## Required Inputs

Ask for any missing item before producing the outline:

- Topic and version boundary.
- Target reader and what they already know.
- Series goal: what the reader should be able to do after finishing.
- Preferred article count or publishing cadence, if the user has one.
- Source constraints, such as official docs only, internal pages, source code, or meeting notes.

## Workflow

1. Build a Research Dossier before outlining.
   - Use official docs, source pages, release notes, issue threads, internal Notion pages, and authoritative secondary sources when available.
   - Extract concepts, APIs, version boundaries, known limitations, production pain points, and terminology.
   - Do not mirror the official documentation table of contents.
2. Build a Concept Dependency Map.
   - List concepts as nodes.
   - Mark prerequisite edges.
   - Identify aha-moment concepts, reader misconceptions, and places where real usage differs from official narrative.
3. Design the series architecture.
   - Start with the reader ladder: entry state, intermediate usable states, final payoff.
   - Group concepts into phases that unlock concrete reader abilities.
   - Use concise phase names. Put depth in the phase goal, not in theatrical headings.
4. Specify each article.
   - Title: concise editorial label.
   - Thesis: one falsifiable sentence.
   - Role: foundation, bridge, mechanism, diagnosis, comparison, synthesis, or field guide.
   - Required anchors: versions, source links, API names, failure mechanisms, numbers, examples, rejected alternatives, and boundaries.
   - Visual plan: state the reader question and diagram type if a diagram is needed.
   - Handoff prompt: complete enough for `Tech Writing - Notion Skill` to draft without asking the user to remember the series context.
5. Validate the outline.
   - Reject documentation mirroring.
   - Reject topic-tag titles.
   - Reject generic difficulty phases like beginner/intermediate/advanced unless the user explicitly wants that format.
   - Check prerequisites and intentional spiral revisits.
   - Check that every article teaches something a strong reader could not get from official docs in five minutes.

## Output Format

Create or update a Notion page with this structure:

```text
# Series Overview
- Topic and version boundary:
- Target reader:
- Reader ladder:
- Series argument:
- Scope:
- Explicit exclusions:
- Phase and article count:
- Why this structure differs from official docs:

# Research Dossier
[Concise research notes with source links.]

# Concept Dependency Map
[Concepts, prerequisite chains, aha moments, and misconceptions.]

# Series Outline
## Phase 1 - [short name]
[Phase goal and reader payoff.]

### Article 1.1 - [short title]
Thesis: [one falsifiable sentence.]
Role: [foundation | bridge | mechanism | diagnosis | comparison | synthesis | field guide]
Required anchors:
Visual plan:
Handoff prompt for Tech Writing:

# Coherence Notes
- Prerequisite chains checked:
- Intentional spiral revisits:
- Allowed overlaps:
- Phase transitions:
```

## Stop Rules

Stop and ask the user before outlining when:

- The topic is too broad for one series.
- The target version is unclear and version differences change the outline.
- The reader prerequisite level would change the first phase.
- Primary sources are unavailable but the user expects a researched plan.
