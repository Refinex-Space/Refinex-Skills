# Anti-Patterns

Use this catalog during drafting and validation. Each anti-pattern includes detection and repair guidance.

## 1. Encyclopedic Drift

**Symptom**: The article expands into history, definitions, feature lists, and generic pros/cons because it lacks a thesis.

**Detect**: Remove the title. If the first two sections could appear in any introductory article on the topic, drift is present.

**Repair**: Write the falsifiable thesis first. Cut any background that does not help prove it.

**Bad**: "Redis 是一个高性能的内存数据库，广泛应用于缓存、队列和分布式锁。"

**Good**: "把 Redis 锁当作事务边界，是很多订单系统偶发重复扣减的根因；它只能提供带过期时间的互斥提示，不能替代业务幂等。"

## 2. Background Stuffing

**Symptom**: The opening begins with "随着", "近年来", "在当今", or broad industry context.

**Detect**: The first paragraph can be deleted without losing the article's claim.

**Repair**: Start with the claim, failure mode, or decision context.

**Bad**: "随着微服务架构的快速发展，分布式锁变得越来越重要。"

**Good**: "分布式锁最危险的地方不是加锁失败，而是加锁成功后业务误以为自己拿到了强一致保证。"

## 3. Robotic Transitions

**Symptom**: Paragraphs are stitched with "首先/其次/此外/最后/总之/值得注意的是/不仅如此".

**Detect**: Search those words. If they carry the logic, the prose is mechanical.

**Repair**: Let the next sentence name the implication or contrast directly.

**Bad**: "此外，Kafka 也支持高吞吐。"

**Good**: "吞吐不是 Kafka 在订单系统里的主要争议点；真正的争议是业务消息语义要不要由 broker 承担。"

## 4. Hollow Titles

**Symptom**: Titles are topic tags, clickbait, or theatrical metaphors.

**Detect**: Title matches "X 简介", "一文读懂", "保姆级", "揭秘", "吊打", "深度解析", or over-clever punctuation.

**Repair**: Name the exact claim, system, or decision.

**Bad**: "一文读懂 Spring AI"

**Good**: "Spring AI ChatClient 的抽象边界"

## 5. False Balance

**Symptom**: The article avoids judgment with "各有优缺点，取决于实际需求".

**Detect**: A comparison section ends without a local winner under the stated context.

**Repair**: Define the decision context and make a scoped recommendation.

**Bad**: "Kafka 和 RocketMQ 各有优势，具体选择取决于业务需求。"

**Good**: "在订单主链路依赖事务消息和延迟消息时，RocketMQ 减少了应用层补偿逻辑；如果核心目标是跨团队事件流和生态集成，Kafka 才是更稳的默认项。"

## 6. Empty Superlatives

**Symptom**: "强大", "灵活", "高效", "稳定", "优秀" appears without evidence.

**Detect**: Every adjective should answer "compared with what, under what workload, measured how".

**Repair**: Replace praise with evidence or remove it.

**Bad**: "该框架提供了非常强大的扩展能力。"

**Good**: "扩展点集中在 Advisor 链路上，因此横切逻辑不需要侵入 ChatModel 调用方。"

## 7. Uplifting Ending

**Symptom**: The conclusion praises the future or congratulates the reader.

**Detect**: Ending contains "相信通过本文", "让我们一起", "未来可期", "拥抱".

**Repair**: Return to the thesis, state the final judgment, and name residual risk.

**Bad**: "相信通过本文的介绍，读者已经对 Redis 分布式锁有了深入理解。"

**Good**: "Redis 锁可以降低并发碰撞概率，但不能替业务承担一致性责任。真正要守住的是幂等边界。"

## 8. Passive Avoidance

**Symptom**: "需要注意的是", "值得一提的是", "应当看到" hides the authorial judgment.

**Detect**: The sentence avoids saying who decides, what fails, or what should change.

**Repair**: Use direct technical judgment.

**Bad**: "需要注意的是，锁超时可能带来一些问题。"

**Good**: "锁超时会把互斥窗口和业务执行窗口拆开；只要业务耗时超过 TTL，锁就不再保护临界区。"

## 9. Parallelism Overload

**Symptom**: Four-character adjective chains and paired slogans replace content.

**Detect**: Phrases like "高效可靠、灵活扩展、安全稳定、简单易用".

**Repair**: Replace each slogan with a mechanism, metric, or trade-off.

**Bad**: "该方案高效可靠、灵活扩展。"

**Good**: "该方案把重试状态写入本地表，牺牲一次额外写入，换取 broker 确认失败后的可恢复性。"

## 10. Depth Cliff

**Symptom**: The article reaches the core mechanism and stops with "细节超出本文范围" or "参考官方文档".

**Detect**: A promised anchor appears only as one sentence or a link.

**Repair**: Explain the mechanism to the depth promised in the Anchor Sheet, or remove it from scope through confirmation.

**Bad**: "Redlock 的具体算法这里不展开。"

**Good**: "Redlock 试图用多数节点成功和有效时间窗口降低单点故障风险，但它没有消除客户端暂停导致的过期后继续执行问题。"

## 11. Flat Depth

**Symptom**: The article begins at source-code depth and stays there without reader ramp.

**Detect**: The first three paragraphs require internal implementation knowledge the reader has not been given.

**Repair**: Start with observable behavior or decision pressure, then descend.

## 12. Documentation Mirroring

**Symptom**: The article follows official docs order and repeats concepts without a new argument.

**Detect**: Section titles map to doc chapters.

**Repair**: Reorder around the thesis and reader's decision path.

## 13. Example-Free Abstraction

**Symptom**: The article discusses design principles but never shows a concrete path, config, trace, or code shape.

**Detect**: A senior reader cannot apply the advice after reading.

**Repair**: Add one concrete mechanism or mini-case at the point of abstraction.

## 14. Version Fog

**Symptom**: The article talks about API behavior without version scope.

**Detect**: Claims about defaults, APIs, or limitations lack version names.

**Repair**: Add version anchors or state the uncertainty and avoid overclaiming.
