# Outline quality checklist (Phase 4 validation gates)

This file is the executable validation loop for Phase 4 of the tech-planner workflow. The checklist runs against the Markdown deliverable produced during Phase 3, checks a series of gates, and either passes the deliverable for hand-off to the user or sends the planner back to an earlier phase to fix the underlying issue. The gates are structural — they check the shape of the deliverable and the relationships between its parts — rather than prose-level, because at this stage the underlying research and architecture must already be sound. If the checklist reveals a research-level or architecture-level failure, the fix is to return to Phase 1 or Phase 2, not to patch the outline in place.

The checklist is designed to run as a loop. The planner walks through the gates in order, marks each as PASS or FAIL with a one-line note, and returns to the appropriate phase to fix any failure before re-running the checklist. A first-pass deliverable typically fails two or three gates, which is normal; a deliverable that passes every gate on the first try is suspicious and usually means the planner has been insufficiently rigorous. After fixes, the full checklist is re-run from Gate 1 because earlier fixes can sometimes introduce later failures.

## Gate 1 — Series argument is falsifiable and sharp

The series overview contains a series argument. For this gate to pass, the series argument must state a specific claim that the series as a whole will convince the reader of, beyond what any individual article claims. The argument must be falsifiable in the same sense as an individual article's argument — a reader who disagreed would be able to point to specific evidence that would settle the disagreement. A series argument that is merely a topic description ("this series covers Spring AI") fails; a series argument that commits to a position ("Spring AI's architectural decisions are mostly correct for the Java ecosystem, but three of them will bite production users in ways the docs do not warn about, and this series identifies all three and shows how to work around them") passes.

The gate also checks whether the series argument is reflected in the individual article arguments. If the series claims one thing and the articles claim unrelated things, the series has no unifying narrative and should either have its argument rewritten to match the articles or the articles reorganized to support the argument. The check is straightforward: read the series argument and then read the seven to fifteen article arguments in sequence, and ask whether they collectively prove the series argument. If the answer is no, the gate fails.

The fix when this gate fails is usually in Phase 3 (the articles do not collectively support the argument) or in Phase 2 (the knowledge graph did not contain an aha moment that the argument depends on), not in the Phase 4 outline.

## Gate 2 — Every article title is concise, accurate, and non-theatrical

This gate is applied mechanically. For every article in the series, the planner reads the visible title and asks whether it would work as a professional table-of-contents entry. The title may carry a light claim, but it does not need to carry the full thesis. The full thesis belongs in the article's `Thesis:` line and prompt.

Titles of the form "Introduction to X", "Getting Started with Y", "Understanding Z", "X Explained", "An Overview of W", and "X for Beginners" are automatic fails. Titles that try to stuff thesis, teaser, metaphor, and payoff into one line also fail. The pass condition is simpler: the title should make one clean claim in editorial language. "Embedding 需要单独成篇" passes. "Embedding、VectorStore、ETL Pipeline 与过滤 DSL——你以为是一件事，其实是四件事" is probably trying to do too much and should usually be split or shortened.

Professional short labels can pass when the surrounding thesis line is specific: `版本基线`, `配置绑定`, `事务边界`, `Consumer Group`, `GC 日志`, `生产清单`. Generated-feeling sentence titles fail even when technically correct: `配置优先级不是记忆题，而是 ConfigData 构建出的搜索路径`, `从端口监听到错误响应都能解释`, `先跑通系统，再讨论组件`.

A gate failure on a single article title is easy to fix — rewrite the title. A gate failure on many titles at once is a deeper problem, usually meaning the Phase 3 architecture did not generate specific article arguments and the planner has been using topic labels as placeholders. The fix in that case is to return to Phase 3 and state the specific argument for each article, then derive the title from the argument.

## Gate 3 — Phase naming is clear, concise, and non-generic

For each phase in the series, the phase name is evaluated against the discipline in `phase-naming-guide.md`. Phase names that are generic buckets ("Basics", "Advanced Topics", "Core Features") or difficulty levels ("Beginner", "Intermediate") fail. Subject-area labels can pass when they are concrete and paired with a specific phase goal paragraph: `配置管理`, `自动配置`, `SQL 基础`, `事务并发`, `观测排障`. Inflated taxonomy labels and verb slogans that sound generated rather than editorial fail: `认知重建`, `机制精通`, `驯服配置`, `拆开魔法`, `穿透 Web`.

The test from `phase-naming-guide.md` applies here: a reader who reads the phase names together with the phase goal paragraphs should be able to describe the series' intellectual arc in their own words. If they fail this test, the naming and phase framing need to be rewritten.

## Gate 4 — Structural divergence from the official docs

The gate checks whether the series structure mirrors the official documentation's table of contents. The planner lists the section headings of the official docs (gathered during Phase 1 research) and lists the phase and article structure of the series side by side. For the gate to pass, the two structures must differ substantially. Specifically, the series must differ in at least two of three dimensions: the phase or top-level grouping must not match the docs' top-level grouping; the ordering of topics must differ; and the series must introduce argumentative framing that the docs lack.

The Structural Divergence note in the series overview is evaluated against the actual structure during this gate. The note must name specific differences, and those differences must be visible in the structure itself. A note that claims divergence while the underlying structure actually mirrors the docs is a gate failure, and the fix is either to redesign the structure (Phase 3) or to acknowledge the mirror honestly and justify it — though justification is rarely valid, because the docs' structure is almost always wrong for a learning progression.

## Gate 5 — The phase styles are chosen for this topic, not copied from a template

This gate verifies that the visible phase design follows the topic's reader payoff rather than a memorized pattern. The planner should be able to explain why this series starts with onboarding, failure, decision, happy path, internals, or synthesis, and that explanation should refer to the actual reader and actual learning problem.

If the same phase style could have been attached unchanged to five unrelated technologies, the gate is in danger of failing. Pattern reuse is allowed; pattern-shaped writing is not. The fix is to restate the reader ladder and redesign the early phases around the first real payoff the reader needs.

## Gate 6 — Entry ramp exists and knowledge flow has no gaps

This gate verifies two things. First, if the target reader does not already know the framework, the series contains an explicit entry ramp before the mechanism-heavy material starts. The entry ramp covers what the framework is for, version matching, minimal setup, a first runnable example, and the terminology the rest of the series will rely on. Second, every concept an article depends on has been covered by a previous article in the series (or is in the series' entry-state prerequisites). The check is a topological walk through the article sequence: for each article, the planner verifies that the article's listed prerequisites are either in the series' entry-state assumptions or are the key concepts of a previously-listed article.

A gap occurs when an article relies on a concept that was not covered and was not in the entry-state prerequisites. A special case of this failure is foundation skip: the planner opens with source-level architecture critique before the reader has ever run the framework once. The fix is either to add an earlier article covering the missing concept, to move the current article later in the series so a concept-introduction article can precede it, or to add the missing concept to the entry-state prerequisites with a note that readers need to know it before starting the series.

## Gate 7 — The reader ramp is smooth enough for the lowest-seniority reader claimed

This gate asks whether the series actually serves the lowest-seniority reader it claims to serve. If the series says it is for beginners or junior engineers, there must be a visible path from "what is this" to "I can use it" to "I know the defaults" to "I can understand the deeper why". If the planner jumps from a glossary to deep mechanism, the gate fails.

The key test is whether there is at least one bridge article or bridge phase between first use and deep internals. The fix is to insert the missing bridge, split a too-dense mechanism article, or narrow the declared audience honestly.

## Gate 8 — Articles do not overlap materially

This gate verifies that no two articles cover the same concept at the same depth. Some overlap is permitted for spiral-pattern series, where a concept is revisited across phases at increasing depth, but the overlap must be labeled as a spiral revisit and each revisit must cover a different aspect. Unlabeled overlap, or overlap that covers the same aspect twice, is a gate failure.

The check is tedious because it requires reading every article's key concepts list and comparing against every other article's list, but it is essential. A series with overlapping articles wastes the reader's time and confuses the series narrative. The fix is either to merge the overlapping articles into a single article, to narrow one of them so the overlap disappears, or (for legitimate spiral revisits) to tag the overlap and verify that each instance covers a distinct aspect.

## Gate 9 — Every article has reference links that are specific and annotated

For each article, the reference links are checked against three criteria. First, every link is specific — not a homepage, not a topic-level URL, but a link to the exact documentation page, source file, issue, or talk section that the article will draw from. Second, every link is annotated — the annotation explains what the writer should extract from the source, and the annotation is specific enough that someone who had never seen the source could understand the intended use. Third, there are enough links — a typical article should have at least three reference links, drawn from different source categories (documentation, source code, issue tracker, secondary sources), to reduce the risk of drawing all the article's material from a single source.

A gate failure on this check is almost always a signal that Phase 1 research was thin for the specific article's topic. The fix is to return to Phase 1, do more research specifically for the failing articles, and regenerate the reference links from the deepened research notes.

## Gate 10 — Every tech-writing prompt is self-contained

This gate verifies that each per-article tech-writing prompt contains all nine required pieces from `prompt-template.md`: central argument, narrative voice, technical anchors, reader profile, prerequisite knowledge, scope boundary, source references, visual explanation plan, and depth/completeness contract. A prompt missing any of the nine is a gate failure and must be completed before the deliverable is released. A prompt that contains all nine pieces but uses vague placeholders ("include relevant code examples", "add a diagram if helpful", "go deep where needed") is also a gate failure, because the prompt has deferred work to the writing phase that should have been done during planning.

This gate also checks the boundary between the prompt and the outer outline. If the outer article block repeats the prompt's detailed metadata above the prompt, the gate fails. The outer outline should carry navigation; the prompt should carry the article contract.

The fix for a prompt that is missing specific pieces is to fill them in from Phase 3's architecture output. If Phase 3 did not produce the needed content, the fix is to return to Phase 3 and generate it — often this means the planner skipped the prompt-generation step during Phase 3 and is trying to do it during Phase 4, which rarely works because the architectural context is not fresh.

## Gate 11 — Article counts within phases respect the working-memory bound

Each phase contains between three and seven articles. Fewer than three is a gate failure because the phase does not justify being a separate phase; more than seven is a gate failure because the phase becomes too much for a reader to hold in mind as a unit. The fix for a too-small phase is usually to merge it with an adjacent phase; the fix for a too-large phase is usually to split it into two phases with a cognitive boundary between them.

The gate has one legitimate exception: a series with a single "introduction" phase containing only one or two articles, followed by substantive phases with three or more articles each, is permitted. The introduction phase acts as a preface rather than a full phase, and the single-article case is acceptable when the article is the aha-moment piece for the whole series.

## Gate 12 — Series length matches scope instead of an arbitrary cap

The total article count is checked against the heuristic in `series-patterns.md`: five to eight articles for a short series, eight to sixteen for medium, sixteen to twenty-eight for long, and roughly twenty-eight to forty for a full framework spiral with onboarding and synthesis passes. A count below five is a gate failure because the series is probably not substantive enough to justify being a series rather than a single long article; a count above forty is a gate failure because the series has become a book and should either be split into multiple series or scoped down.

The gate also checks that the article count matches the knowledge graph from Phase 2. A graph with thirty nodes producing a series with six articles has under-decomposed the topic; a graph with eight nodes producing a series with twenty articles has over-decomposed it. The fix in either case is to return to Phase 2 or Phase 3 and recalibrate.

## Gate 13 — The series has at least one aha-moment article and, when needed, a synthesis payoff

Every series should have at least one aha-moment article — an article whose purpose is to deliver the insight that unlocks the rest of the framework for the reader. Aha-moment articles are identified during Phase 2 and should be flagged in the deliverable with a short note in the article section. A series with no aha-moment article will usually feel flat to readers, because the reader never gets the experience of their understanding snapping into place.

The gate checks whether at least one article is marked as an aha-moment article and whether that article appears early enough in the series (typically after the onboarding material and before the middle of the series) for the aha to pay off across subsequent articles. For larger framework series, the gate also checks for a late synthesis article or phase that cashes out design philosophy, architecture tradeoffs, or irreversible decisions for senior readers. An aha-moment article buried at the end of the series is almost as bad as no aha-moment article at all, because the reader has already slogged through the series without the benefit of the insight.

## Gate 14 — The knowledge-flow and overlap verification notes exist and are honest

The deliverable contains a series-level coherence notes section (see `output-template.md`) with explicit notes on knowledge flow, overlap, spiral revisits (if applicable), and phase-to-phase transitions. This gate verifies that those notes are present and that they are substantive — a note that says "knowledge flow is fine" with no specifics fails the gate, because the planner has not actually done the verification. A note that lists the specific inter-article dependencies the planner checked and confirmed passes.

The fix for a missing or shallow coherence notes section is to actually run the knowledge-flow and overlap checks against the deliverable, record the results, and write the notes honestly. This is tedious but necessary — the notes are the planner's certification that the series hangs together, and a deliverable without honest notes is missing its certification.

## Running the loop

The checklist is run in order from Gate 1 to Gate 14. For each gate, the planner marks PASS or FAIL with a one-line note explaining the judgment. After a full pass through the checklist, the planner groups the failures by where the fix lives: some failures are fixable within the Phase 4 document itself (rewriting a title, adding an annotation to a reference link), some require returning to Phase 3 (regenerating an article's arguments or concepts), some require returning to Phase 2 (the knowledge graph missed a concept), and some require returning to Phase 1 (the research was thin on the specific topic).

Fixes are applied in order from deepest to shallowest. A Phase 1 failure is fixed first, then the planner re-runs Phases 2, 3, and 4 on top of the deepened research. A Phase 3 failure is fixed next, regenerating the affected part of the architecture. Phase 4 document-level fixes are applied last. Running the fixes out of order — patching a Phase 4 symptom while leaving the Phase 1 or Phase 2 cause in place — tends to produce a deliverable that passes the checklist on a technicality while still being weak at its foundation.

After all fixes, the full checklist is re-run from Gate 1. The loop terminates when the checklist passes cleanly — every gate PASS, no outstanding failures. A typical medium-framework series plan passes cleanly on the second or third iteration. A plan that requires five or more iterations is a plan whose underlying research or architecture was thin, and the right response is to go back to the deepest failing phase and invest more time there rather than continuing to iterate on the outline.

## When the checklist cannot pass

Occasionally the checklist cannot be made to pass because the underlying topic is not well-suited to the series the user requested. For example, the user might have asked for a series on a framework that is too small for a substantive series, or on a topic that does not have a clear aha moment, or on a subject that has been covered so well by others that the planner cannot identify a defensible divergence from existing content. In these cases, the right response is not to force the checklist to pass by relaxing standards — it is to return to the user and explain the situation honestly. The options include narrowing or widening the scope, pivoting to a different nearby topic, or acknowledging that a single comprehensive article might serve the user better than a series.

Refusing to produce a weak series plan is a legitimate outcome of this skill. A planner who forces a weak plan through the checklist has served the user poorly; a planner who recognizes the impasse and raises it with the user has served them well.
