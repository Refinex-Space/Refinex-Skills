# Language Standard

## Voice

Write as a senior engineer explaining a design review to peers. Be direct, evidence-based, and specific. The tone is neither textbook nor beginner tutorial.

Default to Chinese. Keep English technical terms where translation would reduce precision.

## Titles

Good titles are concise, accurate, and editorial.

Prefer:

- `DDD 在大众点评交易系统演进中的应用`
- `Writing effective tools for agents`
- `Spring AI ChatClient 的抽象边界`
- `订单系统消息队列选型的业务语义`

Ban:

- topic labels: `Redis 分布式锁简介`
- clickbait: `一文读懂`, `保姆级教程`, `吊打`, `揭秘`, `颠覆认知`
- vague depth claims: `深度解析`, `全面剖析`
- over-dramatic metaphors and punctuation-heavy titles

Section titles follow the same rule. They should tell the reader what the section proves or explains.

## Opening

The first paragraph must carry the thesis. Avoid industry preambles.

Strong opening pattern:

1. State the scoped claim.
2. Name the failure mode, design pressure, or decision context.
3. Preview the mechanism or evidence path.

## Transitions

Avoid transition words as scaffolding:

- `首先`
- `其次`
- `此外`
- `最后`
- `总之`
- `值得注意的是`
- `不仅如此`
- `需要注意的是`

These words are not absolutely forbidden in isolation, but repeated use is a failure. Prefer logical handoff:

- "这个判断在低并发下不明显，压测一旦引入长尾请求，TTL 和业务执行时间就会分离。"
- "问题不在 broker 能不能发送消息，而在业务状态和消息状态能不能共同恢复。"

## Evidence Language

Every evaluation needs evidence.

Replace:

- "性能很好" with workload, latency, throughput, contention, memory, or tail behavior.
- "扩展性强" with the exact extension point and what it avoids changing.
- "可靠性高" with failure model, recovery path, or consistency guarantee.

## Comparison Language

Do not use "各有优缺点" as a conclusion. A comparison must end with a scoped decision:

- "在这个上下文里，A 更适合，因为..."
- "B 的优势成立，但只有在..."
- "如果约束换成 X，结论会反转。"

## Ending

End by returning to the thesis. State the final judgment, residual boundary, or design implication.

Ban:

- "相信通过本文..."
- "让我们一起拥抱..."
- "未来可期..."
- "希望本文能帮助..."

## Sentence Rhythm

Mix short judgment sentences with longer explanatory sentences. Avoid repeated symmetrical clauses and four-character adjective strings.
