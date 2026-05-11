# Research Protocol — Phase 1: Source Exhaustion

## Purpose

This document defines the systematic research methodology for Phase 1. The goal is to exhaust primary sources so that the resulting Research Dossier is comprehensive enough to prevent Documentation Mirroring in later phases.

---

## Search Strategy

### Mandatory Source Categories

Execute searches in this priority order. Each category must be attempted; mark categories as "no results" rather than skipping them.

**Tier 1 — Authoritative Primary Sources**

1. **Official Documentation**: Search for the technology's official docs site. Fetch and read the full table of contents to understand the official narrative structure. This is what you must *not* mirror — but you must understand it to deliberately depart from it.
2. **Source Code Key Paths**: For open-source projects, search GitHub for the main repository. Identify entry-point classes, core abstractions, and extension points. Look at package structure for architectural clues.
3. **Release Notes / Changelog**: Search for release notes across major versions. Note breaking changes, deprecated features, and migration guides — these reveal design evolution and common upgrade pain.

**Tier 2 — Design Intent and Community Feedback**

4. **GitHub Issues and Discussions**: Search `site:github.com {project} issues` and filter for high-reaction or highly-commented issues. These reveal real-world pain points that documentation often glosses over.
5. **Official Blog and Conference Talks**: Search for `{project} blog` and `{lead maintainer name} {project} talk`. Design rationale often lives here, not in docs.
6. **Stack Overflow High-Vote Q&A**: Search `site:stackoverflow.com {project}` sorted by votes. The top 20-30 questions reveal the community's actual confusion points.

**Tier 3 — Community Ecosystem**

7. **Notable Community Blog Posts**: Search `{project} tutorial`, `{project} deep dive`, `{project} production experience`. Look for posts that go beyond documentation — production war stories, performance benchmarks, migration reports.
8. **Comparison and Alternatives**: Search `{project} vs {alternative}`. Understanding what users compare the technology against reveals implicit expectations and mental models readers may carry.

### Search Execution Rules

- Use `web_search` for discovery, then `web_fetch` for content that looks substantive.
- Conduct at least 8-12 distinct searches across the categories above.
- Do not stop after finding "enough" — the protocol is called Source Exhaustion, not Source Sampling.
- Record every source URL for later reference in the Research Dossier.
- If a search returns mostly shallow content (listicles, marketing pages), refine the query and try again.

---

## Research Dossier Template

The output of Phase 1 is a structured Research Dossier. Use this template:

```markdown
# Research Dossier: {Technology Name} {Version}

## 1. Official Narrative Structure
- Documentation chapter list (to identify and avoid mirroring)
- Core abstractions as presented by the docs
- The "happy path" the docs want users to follow

## 2. Concept Inventory
For each concept discovered, record:
- Concept name
- Category: core abstraction / API surface / configuration / runtime behavior / operational concern
- Source where first encountered
- Brief description (1-2 sentences)

## 3. Design Decisions
Architectural choices the framework/tool has made and their implications:
- Decision description
- Rationale (if documented)
- Trade-offs and consequences
- Alternatives that were rejected (if known)

## 4. Known Limitations and Gotchas
- Documented limitations
- Undocumented behaviors discovered in Issues/SO
- Common misconfigurations
- Performance cliffs or scaling boundaries

## 5. Version History and Migration Points
- Major version milestones
- Breaking changes between versions
- Deprecated features and their replacements
- Migration pain points from community reports

## 6. Community Pain Points
- Top 10 Stack Overflow questions (by votes) and what they reveal
- High-activity GitHub Issues themes
- Recurring complaints in community posts

## 7. Ecosystem and Integration Points
- Common companion technologies
- Integration patterns
- Competing/alternative approaches

## 8. Source Registry
- List of all URLs consulted with brief annotation
```

---

## Quality Criteria for Phase 1 Completion

Phase 1 is complete when:
- All 8 source categories have been searched (some may legitimately yield no results for niche technologies).
- The Concept Inventory contains at least 15 distinct concepts for a moderately scoped topic.
- The Community Pain Points section has at least 5 substantive entries (not just "it's hard to install").
- The Design Decisions section captures at least 3 architectural choices with trade-off analysis.
- You can articulate how the official documentation structure differs from the cognitive progression a learner actually needs — this gap is the foundation of Phase 3's architecture.