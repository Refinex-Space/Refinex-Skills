# Validation Checklist — Phase 4: Quality Gates

## Purpose

After Phase 3 produces the series architecture, run this checklist before delivering to the user. Every gate must pass. If any gate fails, revise the affected articles and re-validate.

---

## Anti-Pattern Gates

### Gate 1: No Documentation Mirroring
**Check**: Compare the series article sequence against the technology's official documentation table of contents (captured in the Phase 1 Research Dossier). The article titles, their ordering, and their grouping must not map 1:1 to documentation chapters.
**How to detect**: If more than 50% of article titles could serve as chapter headings in the official docs without modification, this gate fails.
**Remediation**: Restructure around cognitive progression. Merge documentation chapters that serve a single cognitive goal; split chapters that contain multiple distinct cognitive steps.

### Gate 2: No Topic-Tag Titling
**Check**: Every article title must express a claim or describe a specific action/outcome — not merely name a topic.
**How to detect**: If a title could be replaced with a documentation section heading without loss of meaning, it is a topic tag. Also check for banned sensationalist patterns: "揭秘", "一文读懂", "保姆级", "吊打", "颠覆认知", "你不知道的", "必看", "万字长文".
**Remediation**: Rewrite the title to express the article's central thesis in concise, editorial language. Use the Meituan Tech Blog / Anthropic Engineering Blog style as reference.

### Gate 3: No Phase-as-Difficulty-Label
**Check**: No phase is named "基础篇", "进阶篇", "高级篇", "入门", "Beginner", "Intermediate", "Advanced", or any synonym.
**How to detect**: Direct string match plus semantic check — "Foundation Phase" is also a difficulty label in disguise.
**Remediation**: Rename using the cognitive-action naming methodology in `references/phase-naming-guide.md`.

### Gate 4: No Prerequisite Amnesia
**Check**: For every concept referenced in an article, verify that either (a) the concept was introduced in a prior article listed in the prerequisite dependencies, or (b) the concept is declared in the series header as a prerequisite assumption for the entire series.
**How to detect**: Walk through each article in sequence. For each technical term or concept used, trace it back to its introduction point. If it appears without prior introduction and is not a series-level prerequisite, this gate fails.
**Remediation**: Either add the missing concept to an earlier article, reorder articles, or declare the concept as a series-level prerequisite.

### Gate 5: No Pseudo-Spiral
**Check**: If a concept appears in more than one article, every subsequent appearance must be tagged with a `spiral_note` in the prompt that specifies the new complexity layer added.
**How to detect**: Search for concepts appearing in multiple articles. For each, check that the later article's prompt explicitly states what new complexity is introduced. If the "new complexity" is merely "more detail" or "another example" without a genuinely new dimension, this is a pseudo-spiral.
**Remediation**: Either remove the redundant revisit or add genuine new complexity (e.g., concurrency implications, failure modes, production-scale behavior).

---

## Structural Gates

### Gate 6: Prompt Self-Sufficiency
**Check**: Every tech-writing prompt contains all mandatory fields from `references/prompt-template.md` with substantive content (not placeholders).
**How to detect**: For each prompt, verify the presence and non-emptiness of: 系列上下文, 文章标题, 中心论点, 目标读者状态 (all three sub-fields), 关键技术锚点, 范围边界 (both sub-fields), 前序依赖, 视觉说明计划, 深度契约, 写作约束 (all four sub-fields). Then verify conditional fields are present when their conditions apply.
**Remediation**: Fill in missing fields. If a field cannot be filled, the article's scope may be ill-defined — revisit the article specification.

### Gate 7: Knowledge Graph Coverage
**Check**: Every node marked `core` in the Phase 2 knowledge graph is covered by at least one article. At least 80% of nodes marked `important` are covered.
**How to detect**: Cross-reference the knowledge graph node list against the article specifications' technical anchors and scope statements.
**Remediation**: Add coverage for missing core concepts (either by expanding an existing article's scope or adding a new article). For missing important concepts, evaluate whether they can be folded into existing articles or should be left for a supplementary article.

### Gate 8: Cognitive Jump Threshold
**Check**: No single article introduces more than 3-4 new core concepts that were not covered in prior articles.
**How to detect**: For each article, count the concepts in its scope that are not listed in any prior article's coverage. If the count exceeds 4, the cognitive jump is too large.
**Remediation**: Split the article into two, or move one or more concepts to a prior article.

### Gate 9: Series Boundary Consistency
**Check**: Every article's scope falls within the boundaries declared in the series header. No article introduces topics that are outside the declared total scope.
**How to detect**: Compare each article's "本文覆盖" field against the series header's scope declaration.
**Remediation**: Either expand the series scope declaration to accommodate the topic, or remove the out-of-scope content from the article.

### Gate 10: Title Style Consistency
**Check**: All titles in the series follow a consistent style. No mixing of styles (e.g., some titles are topic-tags while others are thesis-driven). All titles pass both the "non-topic-tag" and "non-sensationalist" checks from Gate 2.
**How to detect**: Read all titles together as a list. They should feel like they belong to the same publication. Check for consistent use of language, punctuation, and structural patterns.
**Remediation**: Rewrite outlier titles to match the dominant style.

---

## Coherence Gates

### Gate 11: Dependency Chain Integrity
**Check**: The prerequisite declarations form a valid chain. If article 5 depends on article 3 which depends on article 1, article 5's reader state description must account for concepts from both articles 1 and 3.
**How to detect**: For each article, recursively expand its prerequisite chain and verify that the "读者此刻知道什么" field accurately reflects the cumulative knowledge.
**Remediation**: Update the reader state description to accurately reflect cumulative knowledge.

### Gate 12: Phase Transition Smoothness
**Check**: The last article of each phase naturally leads to the cognitive activity described by the next phase's name. There should be no abrupt topic shifts between phases.
**How to detect**: Read the last article of phase N and the first article of phase N+1 in sequence. The transition should feel motivated, not arbitrary.
**Remediation**: Add a bridging element to the last article of the phase (a forward-looking section that sets up the next phase's question) or reorder articles near the boundary.

---

## Execution

Run all 12 gates sequentially. Record each gate's result as PASS or FAIL with a brief note. If any gate fails, fix the issue and re-run all gates (fixes can introduce new failures elsewhere). Deliver to the user only when all 12 gates pass.