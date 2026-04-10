# Research methodology

This file describes the operational procedure for Phase 1 of the tech-planner workflow. Phase 1 is the systematic consumption of all primary sources for the target framework or topic, and its output is a Research Dossier that feeds into the knowledge graph construction in Phase 2. The methodology is the operational core of the skill, because every downstream phase depends on the quality of what Phase 1 surfaces. A thin Phase 1 produces a thin outline regardless of how clever the Phase 3 work is.

The methodology has two load-bearing principles. The first is that source consumption is sequential, not parallel — the order in which sources are read matters because each source establishes terminology and context that the next source assumes. The second is that reading is active, not passive — every source is read with a specific extraction goal in mind, and the Research Dossier is updated as the reading proceeds, not at the end.

## The five source types in order

Phase 1 consumes five source types in a specific sequence. Skipping any of them, or consuming them out of order, weakens the dossier in predictable ways. The order is: official documentation, source code, release notes and changelogs, GitHub issues and discussions, and authoritative secondary sources.

### Source 1 — Official documentation

The first source is the framework's official documentation, read in its entirety rather than skimmed. The documentation establishes the terminology the rest of the research will use, names the official conceptual model, and reveals what the maintainers consider important enough to document. Reading the documentation first means later sources can be interpreted against the official baseline rather than being read in isolation.

The reading is exhaustive, not selective. The planner reads every page, including the pages that look like reference material rather than learning material, because reference pages often contain the precise terminology and the edge-case behaviors that the learning pages gloss over. A common shortcut is to skim the conceptual sections and skip the reference, which produces a research dossier that knows the broad strokes but not the corners. The corners are where the interesting articles live.

For each documentation page, the planner extracts five things into the Research Dossier. The first is the core concepts the page introduces, named in the page's own terminology, with a short note on what the page says each concept does. The second is the API surface the page documents, recorded as class names, method signatures, configuration keys, or CLI flags, depending on the framework's conventions. The third is the design rationale the page provides for any concept or API, when the page provides one — many pages do not, and the absence is itself worth recording as a gap. The fourth is the documented limitations and known issues, which are often buried in callout boxes or appendices. The fifth is the documentation's own organizational structure for this concept, recorded explicitly so Phase 3 can deliberately diverge from it.

The fifth point is critical. The planner records the documentation's structure not to follow it but to consciously not follow it. The Research Dossier should have a section labeled "Documentation Structure To Diverge From" that lists the docs' table of contents in order. When Phase 3 designs the outline, the planner consults this section and verifies that the outline's structure does not mirror it. The act of recording the structure is the first defense against documentation mirroring; if the planner cannot say what the docs' structure looks like, they cannot consciously diverge from it.

### Source 2 — Source code

The second source is the framework's source code, read for architecture rather than implementation detail. The goal is not to understand every line — it is to understand the code's macro shape, its core abstractions, its extension points, and its hidden contracts. The methodology for codebase reading comes from the engineering literature on onboarding to large codebases and applies the same techniques.

The reading proceeds top-down. The planner first locates the framework's entry point — the class or function the user invokes to start using the framework. For a Spring Boot library this is usually the auto-configuration class; for a CLI tool it is usually the main function; for an SDK it is usually the client constructor. The entry point is the root of the dependency tree the rest of the codebase forms, and starting elsewhere produces a fragmented mental model.

From the entry point, the planner traces the happy path. The happy path is the simplest, most common operation the framework performs, executed step by step through the codebase. For a database client, the happy path might be a successful query; for an LLM library, it might be a synchronous chat completion; for an HTTP framework, it might be a GET request returning a 200. Tracing the happy path reveals the order of operations and identifies the classes or functions that participate in every interaction. These classes are the framework's core abstractions, even when the documentation does not name them as such.

The planner then identifies the three to five core abstractions that keep recurring during the happy path. These are the classes or interfaces that every other class depends on; they form the framework's actual conceptual model, which is sometimes different from the conceptual model the documentation presents. For each core abstraction, the planner records the file path, the public interface, and the abstraction's role in the architecture. The Research Dossier's "Core Abstractions" section is one of the most valuable artifacts for Phase 2, because it surfaces the framework's real shape rather than its documented shape.

After the core abstractions, the planner examines the extension points. Extension points are the interfaces, callbacks, or SPI classes that users are expected to implement to customize the framework. They reveal what the maintainers consider customizable and, by absence, what they do not. A framework that has many extension points around HTTP handling but no extension points around serialization is telling the reader something about its design philosophy, and that something belongs in the dossier.

The last code-reading step is the search for hidden behaviors. Hidden behaviors are things the code does that the documentation does not mention: default values that fall through chains, error-handling fallbacks, retry logic, internal caching, lazy initialization, and so on. The planner searches the codebase for try/catch blocks, default value assignments, and fallback chains, recording any behavior whose existence would surprise a user reading only the documentation. These hidden behaviors are often the most valuable material for the series — they are what the experienced engineers hit in production and that the docs never warned them about.

### Source 3 — Release notes and changelogs

The third source is the project's release history, read as an evolutionary narrative rather than a list of changes. Release notes reveal three things that no other source captures: what the maintainers thought was worth fixing or adding, what they considered breaking changes (and therefore what users were depending on), and what features were deprecated and replaced.

The planner reads the release notes for at least the last twelve months of releases, or further back if the project is older and has had architectural changes. For each release, the planner extracts breaking changes (with the migration patterns they imply), notable additions (with the pain points they appear to address), and deprecated approaches (with their replacements). The result is an evolutionary timeline that reveals the framework's actual trajectory.

The evolutionary timeline is valuable for two reasons. The first is that it identifies which parts of the framework are stable and which are still moving. Articles about stable parts can be written confidently; articles about moving parts need to be either version-tagged carefully or scoped to avoid the moving target. The second is that it reveals where the maintainers themselves had to fix things — and the things that needed fixing are usually the things that were confusing or broken in earlier versions, which makes them excellent series topics.

For each notable change, the planner records the version it was introduced in, the rationale (when stated in the release notes), and the linked GitHub issues or pull requests. The linked issues become entry points for Source 4.

### Source 4 — GitHub issues and discussions

The fourth source is the project's issue tracker and discussion forum, read for community pain points and maintainer intent. This source is uniquely valuable because it captures information that no other source contains: what users actually struggled with, what they got wrong, and what the maintainers told them when they asked for clarification.

The reading is targeted, not exhaustive. The planner sorts issues by reaction count, comment count, or "most discussed" depending on the platform's filtering options, and reads the top thirty to fifty issues from the last year or two. The high-engagement issues are the ones that affected many users and that the maintainers had to address publicly, and they cluster around the same pain points the series should cover.

For each issue, the planner extracts four things. The first is the user's confusion or pain point, recorded in the user's own words. The second is the resolution or maintainer comment, recorded in the maintainer's own words. The third is whether the resolution involved a code change, a documentation update, a workaround, or no action. The fourth is any links to related issues, pull requests, or discussions. The dossier section that emerges from this reading is a list of community pain points, each with the maintainer's perspective on how it should be understood — which is exactly the material a series needs to address the questions real users have.

A particularly valuable subset of issues is the "good first issue" or "help wanted" labels, which often mark places where the maintainers know the framework has rough edges but have not had time to fix them. These rough edges are excellent material for blog articles because they are problems the reader is likely to hit and that no documentation has yet covered.

The planner also reads the discussions tab where the platform supports it (GitHub Discussions, the forum, the Discord, depending on the project). Discussions are usually less structured than issues but capture more open-ended questions about how to use the framework, which surface the conceptual confusions that the documentation has not addressed.

### Source 5 — Authoritative secondary sources

The fifth source is the set of authoritative secondary sources outside the project's own infrastructure. These are conference talks by maintainers, official blog posts, design documents, RFCs or JEPs or similar formal proposals, and interviews with the maintainers. The planner consumes these sources to triangulate the research against multiple perspectives and to capture material that the project's own documentation deliberately omits or that exists only in spoken form.

Conference talks are particularly valuable because maintainers in conference talks tend to be more candid about design tradeoffs, regrets, and future directions than they are in written documentation. A talk might say "we knew this was a mistake when we shipped it but we were locked in by API stability requirements" — a statement that almost never appears in written documentation but that is exactly the kind of insight a series needs to convey. The planner records the timestamp of any such statement and the speaker's name, so the resulting article can cite the talk specifically.

Official blog posts often contain the rationale for major design decisions and the use cases the maintainers had in mind when designing a feature. These rationales are essential for the Phase 2 knowledge graph, because they explain why concepts exist and what they were designed to enable.

RFC-style design proposals (the JEP process for OpenJDK, the Spring Framework's design notes, the Kubernetes Enhancement Proposals) are the most rigorous form of secondary source available, when they exist. They describe the alternatives considered, the rejected options, and the rationale for the chosen path. Reading them is usually time-consuming but always worthwhile, because they provide the rejected-alternatives material that is otherwise impossible to get and that is essential for the Design Tribunal voice in derived articles.

## Anti-skim techniques

The single biggest risk during Phase 1 is skimming when the protocol calls for reading. Skimming feels productive — pages turn, sections are checked off — but the dossier that results is shallow in ways the planner will not notice until Phase 3 reveals the gaps. Three techniques defend against skimming.

The first technique is forced extraction. The planner does not move on from a source until they have written down the specific items the source contributed to the dossier. If a documentation page is read and produces no dossier entries, either the page contributed nothing or the planner skimmed it. The planner re-reads in the second case.

The second technique is the "what did this teach me" question. After every source, the planner asks themselves: what did I learn from this source that I did not know before, and that the previous sources did not cover? If the answer is "nothing", the source either was redundant or was skimmed. The check forces the planner to articulate the source's incremental contribution, which is impossible to do without actually reading.

The third technique is hostile reading of the documentation. The planner reads the official docs with the assumption that they are misleading or incomplete in specific ways, and looks for evidence of those gaps. The hostile stance is not because the docs are actually bad — they are usually written with care — but because the planner needs to find the gaps the docs leave, and a deferential reading will not surface them. The hostile reading produces a list of "what the docs don't tell you" entries that becomes one of the most valuable parts of the dossier.

## The Research Dossier

The Research Dossier is the structured output of Phase 1. It has eight sections: Core Concepts, Core Abstractions, API Surface, Documented Limitations, Hidden Behaviors, Evolutionary Timeline, Community Pain Points, and Documentation Structure To Diverge From. Each section is populated as the planner moves through the sources, with provenance tags noting which source each entry came from.

The dossier is not a polished document. It is a working research log, written for the planner's own use, optimized for quick lookup during Phase 2 and Phase 3. Entries are short and concrete, not narrative. A typical Core Concepts entry might read: "Advisor — Spring AI's interception primitive; runs around ChatClient.call() once per call, regardless of tool calls; lives in spring-ai-core, AdvisorChain.java; documented in advisors.html but missing the around-once semantics; pain point in issue #1234". That single entry compresses information from documentation, source code, and the issue tracker into a form Phase 2 can use immediately.

The dossier should be substantial. A serious topic produces dozens of Core Concepts entries, ten or more Core Abstractions, a long Hidden Behaviors list, and a long Community Pain Points list. A dossier that fits on one page is almost always a sign of skimming; a dossier that runs to many pages is normal for a serious framework.

## Time expectations

Phase 1 takes serious time on a serious topic. For a framework like Spring AI or Project Reactor, expect several hours of reading distributed across the five source types. The planner who spends thirty minutes on Phase 1 is producing a thin dossier and should expect Phase 3 to reveal the thinness. The planner who spends six hours on Phase 1 produces a dossier that makes Phase 2 and Phase 3 dramatically faster, because the material is already organized and the gaps are already visible.

The temptation to compress Phase 1 is the strongest temptation in the workflow. The planner should resist it. A thin Phase 1 propagates downstream as a thin outline, and the cost of the thin outline is paid by the user when they discover, articles into the writing, that the planning did not actually cover what they needed.