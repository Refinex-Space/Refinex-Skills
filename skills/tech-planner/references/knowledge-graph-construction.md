# Knowledge graph construction

This file describes the operational procedure for Phase 2 of the tech-planner workflow. Phase 2 takes the Research Dossier produced in Phase 1 and turns it into a Concept Dependency Map — a graph of the topic's concepts and the prerequisite relationships between them. The map is the artifact that lets Phase 3 sequence articles without guessing about ordering, because the map makes the topic's cognitive structure visible in a way that lets the planner read off the correct order rather than inventing one.

The construction is a four-step procedure: extract concepts, draw edges, identify clusters, and find the aha moments. Each step has a specific output, and each step depends on the previous one. The procedure is short enough to walk through in a single sitting for most topics, but the thinking it requires is the most demanding work in the whole skill — Phase 1 is mechanical reading, Phase 3 is mechanical assembly, but Phase 2 is the step where the planner actually has to understand the topic well enough to argue about its shape.

## Step 1 — Extract concepts as nodes

The first step extracts every distinct concept from the Research Dossier and adds it as a node in the graph. A concept, for the purposes of this graph, is a unit of understanding the reader must acquire to use or reason about the framework. Concepts are not the same as APIs or documentation pages — they are the mental models the reader must build, even when those models cross multiple API surfaces or are not named in any single documentation page.

The pragmatic test for whether something is a concept worth nodifying is whether a reader could be confused about it independently. If a reader can understand `ChatClient` without understanding `ChatModel`, then the two are separate concepts and become separate nodes. If they can only be understood together, they collapse into a single node. The collapse decision is a judgment call, and the planner should err toward separation rather than merging — it is easier to combine two nodes later than to separate one node into two after the graph has been built around it.

The concepts come from three sections of the Research Dossier: the Core Concepts section, the Core Abstractions section, and parts of the Hidden Behaviors section. Each entry in those sections becomes a candidate node. The planner reviews each candidate and decides whether it warrants nodehood or whether it should be merged into another node. A typical framework produces between fifteen and forty nodes; fewer than fifteen suggests the concept extraction was too coarse, more than forty suggests it was too fine and the planner should look for collapse opportunities.

Each node carries metadata with it. The planner records the node's name, a one-sentence definition in the planner's own words (not the documentation's words), the source from which it came, and a one-sentence note on why the concept matters. The "why it matters" note is the seed of the eventual article's central argument, and writing it down at the node-extraction step forces the planner to articulate the concept's purpose rather than leaving it implicit.

## Step 2 — Draw prerequisite edges

The second step adds directed edges between nodes. An edge from A to B means "to understand B, the reader must already understand A". The set of edges defines the prerequisite structure of the topic, and the structure determines how the articles can be ordered.

The planner walks through every pair of nodes and asks whether one is a prerequisite for the other. The question can yield three answers: A is a prerequisite for B (draw an edge from A to B), B is a prerequisite for A (draw an edge from B to A), or neither is a prerequisite for the other (draw no edge). Pairs that are mutually prerequisite suggest the two nodes should probably be collapsed into one — if neither can be understood without the other, they are not separable concepts.

Drawing the edges is the step where the planner has to think carefully about how the topic actually works in a reader's head, not how it is presented in the documentation. The documentation often presents concepts in an order that is convenient for explanation but not the order in which they are cognitively dependent. For example, a Reactor tutorial might introduce `Mono` and `Flux` as a pair before introducing the `Publisher` interface they both implement, because the tutorial wants to show concrete examples first. But cognitively, the reader cannot understand `Mono` without understanding the publish-subscribe model that `Publisher` formalizes — the dependency runs from the abstract to the concrete, not from the concrete to the abstract. The graph's edges should reflect the cognitive dependency, not the tutorial's presentation order.

Two anti-patterns to watch for during edge drawing. The first is the "everything depends on everything" failure, where the planner draws edges so liberally that almost every node points to every other node and the graph becomes useless for ordering. The fix is to be strict about what "prerequisite" means: A is a prerequisite for B only if B is genuinely incomprehensible without A, not if B is merely easier to understand once A is known. Strict prerequisites are rarer than loose ones, and the strict version produces a usable graph.

The second anti-pattern is the "shallow chain" failure, where the planner draws only the most obvious edges and misses the indirect prerequisites. If A is a prerequisite for B and B is a prerequisite for C, the planner should not need to also draw A-to-C, but the planner does need to recognize that any article on C implicitly depends on both B and A. The graph captures the direct edges, but the planner reasons about transitive dependencies during ordering.

The output of Step 2 is the graph with all its edges in place. For most topics, the graph has between thirty and a hundred edges across its fifteen-to-forty nodes. The graph at this point can usually be drawn on paper in a way that reveals its structure, with foundational nodes (no incoming edges) at the top and dependent nodes (many incoming edges) at the bottom.

## Step 3 — Identify concept clusters

The third step groups nodes into clusters that will eventually become articles. A cluster is a set of nodes that belong together in a single article — they are conceptually related, share prerequisites, and can be introduced together without overwhelming the reader.

The clustering uses three heuristics. The first is shared prerequisites: nodes that share the same set of prerequisite nodes are usually in the same cluster, because they become available to the reader at the same point in the series and can be introduced as a group. The second is conceptual proximity: nodes that are about the same aspect of the framework — say, all the nodes about error handling, or all the nodes about extension points — are usually in the same cluster, even when their prerequisites differ. The third is cognitive load: a single article can introduce roughly one cluster of new complexity without overwhelming the reader, so clusters should be sized to fit within an article's cognitive budget.

The cognitive budget heuristic is the hardest to apply because it depends on the planner's judgment about how much new material a reader can absorb in one sitting. A useful rule of thumb is that an article should introduce no more than three to five new concepts of comparable weight, plus any number of supporting details that reinforce the main concepts. An article that tries to introduce eight new concepts is too dense; an article that introduces only one concept may be too thin unless the concept is large enough to warrant a whole article on its own.

The clusters do not need to partition the graph perfectly. Some nodes belong to multiple clusters because they appear in multiple articles, with each appearance contributing different depth (the spiral curriculum at work). The planner records the cluster membership for each node and notes which appearances are introductions and which are revisits. Revisits will become spiral elements in the final outline.

The output of Step 3 is the list of clusters, each with its member nodes, its prerequisite clusters (computed from the prerequisite edges between clusters), and a one-sentence description of what the cluster covers.

## Step 4 — Find the aha moments

The fourth step identifies the aha moment dependencies — the specific concepts whose first correct understanding unlocks multiple other concepts. An aha moment is a concept that the reader has to grasp before the rest of the topic makes sense, even though the documentation may present it as just one concept among many.

The aha moments are identified by looking at the graph's structure. A concept is an aha moment if it has many outgoing prerequisite edges — that is, many other concepts depend on it. A concept that other concepts depend on heavily is a leverage point; understanding it unlocks the downstream concepts, while not understanding it blocks them. The planner identifies the top three to five such concepts and marks them as aha moments.

For each aha moment, the planner writes a short note describing what specifically must be understood about the concept to unlock the downstream understanding. The note is more specific than the concept's definition — it captures the particular insight that, once acquired, makes the related concepts click into place. For example, in Project Reactor, the concept "operator" is an aha moment, but the specific insight is "operators return new publishers; they do not mutate the source publisher". Once a reader internalizes that one sentence, dozens of operator behaviors become obvious; until they internalize it, every operator looks confusing in its own way.

Aha moments deserve their own articles, or at least their own dedicated section within an article, because they are the leverage points where the series can do the most good. A series that introduces an aha moment carefully and confirms the reader has understood it before moving on will produce dramatically better outcomes than a series that lets the aha moment slip past in a paragraph. The Phase 3 article placement should treat aha moments as anchor points around which other articles are organized.

## Capturing the docs-vs-reality gap

In addition to the four steps above, the knowledge graph should capture the gap between how the official documentation presents the topic and how real users experience it. This gap is one of the most valuable inputs to Phase 3 because it tells the planner where the series should diverge from the documentation in order to actually serve the reader.

The gap is captured in a separate Dossier section called "Docs vs Reality" that lists discrepancies. Each entry has three fields: what the docs say, what the reality is (drawn from the Hidden Behaviors and Community Pain Points sections of the Research Dossier), and the implication for the series. A typical entry might read: "Docs say `ChatClient` is a simple synchronous abstraction; reality is that streaming + tool-call breaks the AdvisorChain semantics in four ways; implication: the series needs an article that explicitly addresses the streaming case rather than treating it as an edge case".

These docs-vs-reality entries often become the most argumentative articles in the series, because they have a clear thesis (the docs are misleading or incomplete on this specific point) and clear evidence (drawn from the source code and the issue tracker). They are also the articles that distinguish the series from the official documentation, which is exactly what the divergence requirement in the quality checklist demands.

## A worked example

To make the procedure concrete, consider what the knowledge graph for a Spring AI series might look like at the end of Phase 2.

The node extraction would produce concepts like `ChatClient`, `ChatModel`, `Prompt`, `PromptTemplate`, `ChatOptions`, `Advisor`, `AdvisorChain`, `Tool`, `ToolCallback`, `ChatMemory`, `Embedding`, `EmbeddingModel`, `VectorStore`, `Document`, `DocumentReader`, `DocumentTransformer`, `RAG pipeline`, `OutputParser`, and a dozen others. Total: roughly twenty-five to thirty nodes for a serious treatment.

The prerequisite edges would link `Prompt` and `PromptTemplate` to `ChatClient` (you cannot use ChatClient without prompts), would link `ChatModel` to `ChatClient` (the client wraps the model), would link `Advisor` to `AdvisorChain` (the chain is composed of advisors), would link `Embedding` to `EmbeddingModel` to `VectorStore` to `RAG pipeline` (the RAG path), and so on. The total edge count would be around forty to sixty.

The clustering would produce groups like "the synchronous request path" (ChatClient + Prompt + ChatOptions + ChatModel), "the advisor system" (Advisor + AdvisorChain + the lifecycle), "tool calling" (Tool + ToolCallback + the streaming-vs-sync distinction), "memory" (ChatMemory + the storage backends), "RAG" (Embedding + VectorStore + Document + the indexing flow), "structured output" (OutputParser + the JSON-mode handling), and "observability" (the metrics and the integration points). Total: around six to eight clusters, which corresponds roughly to the eventual phase or article count.

The aha moments would include "ChatClient is a fluent builder over a lower-level ChatModel that is the actual state machine" (clarifies the relationship between the high-level and low-level APIs), "AdvisorChain.around() runs once per ChatClient.call() regardless of tool-call iterations" (explains the streaming + tool-call bug), and "the embedding model and the chat model are independent and can be from different providers" (clarifies an architectural decision that the docs do not emphasize). Each of these is a lever that, once pulled, makes a substantial portion of the rest of the framework comprehensible.

The docs-vs-reality entries would include the streaming + tool-call gap, the lack of documentation on AdvisorChain ordering semantics, the unclear relationship between `ChatMemory` and conversation history in tool-call scenarios, and several others drawn from the issue tracker. Each of these would become a candidate article — and probably a strong one — because each has both a clear thesis and concrete evidence to support it.

The output of Phase 2, in this example, would be roughly thirty nodes, sixty edges, seven clusters, four aha moments, and six docs-vs-reality entries. Phase 3 takes that material and turns it into a series outline with phases, articles, and per-article prompts.

## Anti-patterns to avoid

Three failure modes are common in Phase 2 and worth naming explicitly.

The first failure is treating documentation pages as nodes. The planner extracts a node for every doc page, ending up with a graph that mirrors the documentation's structure rather than the topic's conceptual structure. The fix is to treat documentation pages as sources, not as concept boundaries — a single page may introduce multiple concepts (each becoming a node), and a single concept may be discussed across multiple pages.

The second failure is drawing edges based on documentation order rather than cognitive dependency. The planner reads the docs in order and assumes that whatever appears first is a prerequisite for whatever appears later, even when the cognitive dependency runs the other way. The fix is the cognitive-dependency test from Step 2: A is a prerequisite for B only if B is genuinely incomprehensible without A, regardless of which one appears first in the docs.

The third failure is skipping Step 4 entirely and going straight to clustering and ordering. The planner produces a graph and clusters but does not identify the aha moments, with the result that the series treats every concept as roughly equally important and misses the leverage points. The fix is to enforce Step 4 as a mandatory step rather than an optional polish; the aha moments are what give the series its arc.