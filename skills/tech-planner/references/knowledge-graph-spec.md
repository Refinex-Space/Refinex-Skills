# Knowledge Graph Specification — Phase 2: Knowledge Graph Construction

## Purpose

Transform the Phase 1 Research Dossier into a concept dependency graph that makes prerequisite relationships explicit and auditable. This graph is the primary defense against Prerequisite Amnesia.

---

## Node Definitions

Each concept from the Research Dossier becomes a node. Every node must have:

- **id**: A short, unique, kebab-case identifier (e.g., `auto-configuration`, `chatclient-api`, `vector-store-abstraction`)
- **label**: Human-readable concept name
- **category**: One of the following:
  - `core-abstraction` — A foundational mental model the reader must internalize (e.g., Spring Boot's opinionated defaults philosophy)
  - `api-surface` — A concrete API, class, or interface the reader must learn to use (e.g., `ChatClient`, `@RestController`)
  - `mechanism` — An internal process or algorithm the reader must understand (e.g., auto-configuration resolution order, vector similarity search)
  - `configuration` — Settings, properties, or tuning knobs (e.g., `spring.ai.openai.chat.options`)
  - `operational` — Deployment, monitoring, production concerns (e.g., connection pooling, rate limiting)
  - `pattern` — A design pattern or architectural approach (e.g., RAG pattern, circuit breaker pattern)
- **priority**: `core` (must be covered), `important` (should be covered, ≥80%), or `supplementary` (cover if series length permits)
- **official-narrative-gap**: If the official docs present this concept in a misleading or incomplete way, note the gap here. This is a rich source of article value.

---

## Edge Definitions

Edges are directed: `A → B` means "understanding A is a prerequisite for understanding B."

Each edge must have:

- **from**: Source node id
- **to**: Target node id
- **type**: One of:
  - `hard-prerequisite` — B is incomprehensible without A. The article covering B must come after the article covering A.
  - `soft-prerequisite` — B can be understood without A, but understanding is significantly enhanced. Preferred but not mandatory ordering.
  - `builds-on` — B revisits A at a deeper level (spiral relationship). The article covering B must explicitly mark the new complexity layer added.
  - `contrasts-with` — A and B are alternatives or competing approaches. Covering them in proximity aids comparison.
  - `composes-with` — A and B are commonly used together. Covering them in proximity aids integration understanding.
- **annotation**: A brief note explaining the dependency (e.g., "ChatClient's builder pattern relies on understanding Spring's auto-configuration injection")

---

## Construction Process

### Step 1: Extract Nodes
Walk through the Research Dossier's Concept Inventory. Create one node per concept. Assign category and priority.

### Step 2: Identify Edges
For each pair of nodes, ask: "Can a reader understand concept B without first understanding concept A?" If no, draw a `hard-prerequisite` edge. If "with difficulty," draw a `soft-prerequisite` edge.

Also identify `builds-on` edges by looking for concepts that are the "same thing but deeper" (e.g., "using ChatClient" → "extending ChatClient with custom advisors").

### Step 3: Gap Analysis
For each node, compare the official documentation's presentation with what the Research Dossier reveals about real-world usage. Record gaps in the `official-narrative-gap` field. Common gap types:
- **Omission gap**: The docs don't mention a concept that is critical in practice.
- **Framing gap**: The docs present a concept in a way that creates incorrect expectations.
- **Sequencing gap**: The docs introduce concepts in an order that doesn't match cognitive dependency.
- **Depth gap**: The docs cover a concept at a depth that is insufficient for production use.

### Step 4: Validate Acyclicity
Check that hard-prerequisite edges form a DAG (directed acyclic graph). If cycles exist, one of the edges is misclassified — re-examine and downgrade to soft-prerequisite or split the concept into sub-concepts.

### Step 5: Identify Entry Points and Terminal Nodes
- **Entry points**: Nodes with no incoming hard-prerequisite edges. These are candidates for early articles.
- **Terminal nodes**: Nodes with no outgoing edges. These are candidates for late-series articles.
- **High-fanout nodes**: Nodes with many outgoing edges. These are foundational concepts that must be covered thoroughly and early — if the article covering such a node is weak, many downstream articles suffer.

---

## Output Format

Present the Concept Dependency Map in two forms:

### Tabular Summary
A table with columns: id, label, category, priority, incoming hard-prerequisites, official-narrative-gap.

### Mermaid Graph
A Mermaid flowchart showing nodes and edges. Use solid arrows for hard-prerequisites, dashed for soft-prerequisites, and dotted for builds-on. Color-code by priority: core nodes in a distinct style, important in another, supplementary in a third.

This dual representation ensures the graph is both human-scannable (table) and structurally visible (diagram).

---

## Quality Criteria for Phase 2 Completion

- Every concept from the Research Dossier with priority `core` or `important` appears as a node.
- Every hard-prerequisite edge has been validated (ask: "Is it really impossible to understand B without A?").
- The graph is a DAG for hard-prerequisite edges.
- At least 3 official-narrative-gaps have been identified (if fewer, the research in Phase 1 may be insufficient — consider going back).
- Entry points and high-fanout nodes have been explicitly identified and flagged for early coverage.