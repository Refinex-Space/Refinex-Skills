# Narrative Strategies

Use strategies as starting points, not templates. The article structure must serve the thesis. Hybrid strategies are allowed when the reason is clear.

## 1. 论证式

**适用场景**: The article argues for a judgment: a design choice, an adoption recommendation, a risk boundary, or a correction to common practice.

**展开逻辑**: State the claim, define the decision context, present evidence, address serious objections, land on a concrete judgment.

**节奏特征**: Dense opening, evidence-heavy middle, concise ending. Avoid tutorial pacing.

**陷阱**: Weak evidence turns it into opinion. Fake balance weakens the conclusion.

## 2. 机制拆解式

**适用场景**: The reader sees symptoms or APIs but lacks the internal model: lifecycle, execution path, consistency model, memory behavior, retry semantics.

**展开逻辑**: Start from an observable behavior, move inward layer by layer, connect each internal mechanism back to an engineering consequence.

**节奏特征**: Progressive depth. Each section should reveal one deeper mechanism and one practical implication.

**陷阱**: Dumping internals without a problem. Stopping at "source code says so" without explaining why it matters.

## 3. 问题驱动式

**适用场景**: A real problem, incident, performance cliff, integration failure, or debugging puzzle motivates the article.

**展开逻辑**: Present the concrete problem, rule out naive explanations, trace the failure path, derive the robust solution.

**节奏特征**: Strong narrative pull. Evidence appears as the investigation advances.

**陷阱**: Making the problem fictional or too generic. Hiding the final lesson until the end like a mystery story.

## 4. 时间线/演进式

**适用场景**: The article explains why a system, API, or architecture evolved across versions, scale stages, or organizational constraints.

**展开逻辑**: Show the pressure at each stage, the decision made, the new failure introduced, and the next adjustment.

**节奏特征**: Chronological, but not historical filler. Each stage must add a decision or constraint.

**陷阱**: Turning into a changelog. Dates and versions matter only when they explain a technical trade-off.

## 5. 对比裁决式

**适用场景**: The user needs a choice between technologies, designs, algorithms, protocols, or operational models.

**展开逻辑**: Define the decision context, select comparison axes from the workload, compare mechanisms rather than labels, make a clear recommendation.

**节奏特征**: Structured and decisive. Each axis ends with a local judgment; the article ends with a global judgment.

**陷阱**: "各有优缺点，取决于需求". If the context is specific, the article owes a decision.

## 6. 实战复盘式

**适用场景**: The article starts from a real project, migration, incident, performance optimization, or architecture refactor.

**展开逻辑**: Context, initial assumption, failure or constraint, diagnosis, intervention, result, residual risk.

**节奏特征**: Concrete and grounded. Numbers, configs, diagrams, and rejected options carry the argument.

**陷阱**: War story without transferable principle. Sanitized success narrative with no uncomfortable details.

## 7. 设计评审式

**适用场景**: The article explains why a design should be accepted, rejected, or changed before implementation.

**展开逻辑**: Define the design goal, state constraints, examine options, reason through failure modes, choose the design, document boundaries.

**节奏特征**: Direct, sober, and decision-oriented. Useful for architecture articles and internal engineering blogs.

**陷阱**: Becoming an ADR dump. The article still needs a readable argument and enough mechanism for outsiders.

## Strategy Selection Heuristic

- If the article's main job is to change a belief, choose 论证式.
- If the main job is to build a mental model, choose 机制拆解式.
- If the main job is to solve or debug, choose 问题驱动式.
- If the main job is to explain evolution, choose 时间线/演进式.
- If the main job is to decide between options, choose 对比裁决式.
- If the main job is to extract lessons from production, choose 实战复盘式.
- If the main job is to justify architecture before building, choose 设计评审式.
