# Language conventions

Default output language for this skill is **Chinese with technical terms in English**. English is secondary and should be used only when the user explicitly requests it, or when the document type is an API reference aimed at an international audience.

This file contains the conventions for both languages. The Chinese conventions are more detailed because they are the default and because Chinese technical writing has several pitfalls that English does not.

---

## Chinese technical writing conventions

### Target register

The register is **a senior engineer explaining to a peer in a design review**. Not a tutorial. Not a marketing post. Not a thread for juniors. Specifically:

- Direct and argumentative. The writer has an opinion and states it.
- No throat-clearing ("各位小伙伴大家好", "接下来让我们一起看一下").
- No marketing vocabulary ("强大的", "优雅的", "丝滑的", "史诗级", "王炸").
- No bootcamp vocabulary ("保姆级", "手把手", "小白也能懂").
- No PM-deck vocabulary ("赋能", "抓手", "链路", "对齐" in their management sense).
- Assumes the reader has done some real engineering work. Does not explain what a bean is, what `@Autowired` does, or what JVM heap means.

### Technical terms stay in English

Any of the following stay in English, unmodified, even inside Chinese prose:

- Class, interface, and method names (`ChatClient`, `AdvisorChain.nextAroundStream`, `HikariDataSource`).
- Configuration keys and property names (`spring.ai.openai.chat.options.temperature`, `hibernate.connection.pool_size`).
- Protocol names and versions (HTTP/2, TCP, TLS 1.3, gRPC, WebSocket, Server-Sent Events).
- Library, framework, and product names (Spring AI, Hibernate, PostgreSQL, CockroachDB, Kafka, Kubernetes).
- CLI flags and commands (`--max-connections`, `kubectl rollout restart`, `psql -c`).
- Error codes and HTTP status codes (`HTTP 429`, `ORA-01555`, `ECONNRESET`).
- Metric names (`http.server.requests`, `jvm.memory.used`).
- File paths and module names (`META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`).

Common nouns that have stable, unambiguous Chinese renderings may be written in Chinese where it reads more naturally: 线程 (thread), 进程 (process), 缓存 (cache), 索引 (index), 事务 (transaction), 分区 (partition), 副本 (replica). But use your judgment — if the English term is more common in the relevant community (for example, "connection pool" is often better than "连接池" in Java-community writing), keep it in English.

Never machine-translate proper nouns. "Spring AI" is Spring AI, never "弹簧 AI". "ChatClient" is ChatClient, never "聊天客户端". This is a hard rule.

### Spacing between Chinese and English

Put a half-width space between Chinese characters and adjacent English words or numbers. Exceptions: adjacent to Chinese punctuation, no space is needed because the punctuation already provides separation.

Correct:
```
Spring AI 的 ChatClient 在 streaming + tool-call 场景下会触发 AdvisorChain 的 bug。
```

Wrong:
```
Spring AI的ChatClient在streaming+tool-call场景下会触发AdvisorChain的bug。
```

Also wrong (over-spacing around punctuation):
```
Spring AI 的 ChatClient , 在 streaming 场景下 ...
```

### Punctuation

Chinese prose uses Chinese full-width punctuation: 。,;:?!《》""''()、. English quotations inside Chinese prose keep their English punctuation, and code samples keep their native punctuation.

The most common mistake is using English commas and periods inside Chinese prose. If the output is Chinese, the punctuation between Chinese words is Chinese. Only inline English phrases and code expressions use English punctuation.

Correct:
```
我们在生产环境里观察到,AdvisorChain.nextAroundStream() 在 tool-call 场景下只被调用一次。
```

Wrong:
```
我们在生产环境里观察到, AdvisorChain.nextAroundStream() 在 tool-call 场景下只被调用一次.
```

### Sentence structure

Chinese technical writing benefits from short, declarative sentences that front-load the claim. Avoid the Chinese academic writing habit of stacking subordinate clauses before the main clause — it reads as dense and evasive. Claim first, reasons after.

Avoid:
```
通过对 Spring AI 在各种生产环境下的大量实践经验总结,我们发现,在涉及到 streaming
以及 tool-call 同时存在的复杂场景下,存在着一些值得深入探讨的问题。
```

Prefer:
```
Spring AI 在 streaming 和 tool-call 同时启用时会出现四种生产 bug。根因是
AdvisorChain 的 around 语义假设 advisor 是纯函数式的,而 tool-call 本质上有状态。
```

Two short sentences that front-load the claim beat one long sentence that buries it.

### Words to avoid (Chinese)

The following are high-frequency AI-generated Chinese filler words. They should be used very sparingly or not at all.

"值得注意的是", "我们不难发现", "综上所述", "总的来说", "毫无疑问", "众所周知", "显而易见", "从某种程度上来说", "在某种意义上", "不可否认", "笔者认为", "接下来让我们一起", "让我们深入了解", "让我们一探究竟", "本文将详细介绍", "希望对大家有所帮助", "喜欢的话点赞收藏".

The fix is not to find Chinese synonyms. The fix is to delete the phrase and let the following sentence carry the weight on its own.

### Tone checks

Three questions to ask about a finished Chinese draft:

1. If a senior engineer at your company read this, would they feel talked down to? If yes, rewrite.
2. Does the draft have any sentence that would embarrass you to say out loud in a design review? If yes, rewrite.
3. Does the draft use first-person plural ("我们") in a way that includes the reader as a co-investigator, or in a way that sounds like a marketing team ("我们很高兴地宣布")? The first is fine; the second must be cut.

---

## English technical writing conventions

### Target register

Professional, direct, peer-to-peer. Same stance as the Chinese register: senior engineer explaining to another senior engineer. The register is the same; only the language surface differs.

### Vocabulary: prefer Anglo-Saxon over Latinate

When a short Anglo-Saxon word and a longer Latinate word mean roughly the same thing, prefer the shorter word. Not as a religion, but as a default.

| Prefer       | Avoid         |
|--------------|---------------|
| use          | utilize       |
| start        | commence      |
| end          | terminate     |
| help         | facilitate    |
| show         | demonstrate   |
| try          | attempt       |
| need         | necessitate   |
| get          | obtain        |
| make         | manufacture   |
| about        | regarding     |
| before       | prior to      |
| after        | subsequent to |
| now          | at this time  |
| often        | frequently    |
| enough       | sufficient    |
| keep         | maintain      |
| build        | construct     |

The underlying principle: technical writing is not legal writing. The Latinate register signals distance and formality; the Anglo-Saxon register signals directness and confidence. Directness and confidence are what you want.

### Voice

Active voice by default. Passive voice only when the agent is genuinely unknown or irrelevant.

Passive voice is not wrong — it is a tool with a specific use. The test: if the sentence is passive, can you name the actor and put them in the subject position without loss? If yes, do so. "Mistakes were made" fails the test (you know who made them; rewrite as "We shipped the change without reviewing the schema migration"). "The connection was reset" passes the test (you do not know who reset it; leaving it passive is honest).

### Tense

Present tense for behavior. "`ChatClient` sends a request to the provider", not "will send". The present tense expresses timeless behavior, which is what you are describing — the library behaves this way whenever it is called.

Past tense for incidents and war stories. "On March 14 at 02:47, our checkout service started returning 503s." Incidents happened once, at a specific time; past tense is correct.

Future tense only for actual future events. "Spring AI 1.0.0-RC2 will add Anthropic tool-call support" is correct because it has not yet been released. "The connection pool will then reject the request" describing present behavior is wrong; rewrite as "The connection pool rejects the request".

### Precision over concision

When a short sentence is less precise and a slightly longer sentence is more precise, ship the longer sentence. Readers will forgive length; they will not forgive ambiguity.

Imprecise: "The cache is slow."
Precise: "At >200 concurrent writes, the cache's rebuild cost (O(n) per insert) dominates and drops hit latency from 0.4ms to 18ms."

The second is longer. The second is also the one the reader can act on.

### Sentence length

Vary sentence length. A string of long sentences reads as dense; a string of short sentences reads as choppy; alternating them reads as thoughtful. A reasonable target is an average of 15–22 words per sentence, with regular departures in both directions.

Very short sentences (4–8 words) are the strongest tool for landing a point. Use them at the end of a paragraph when you want the reader to stop and absorb.

### Paragraph length

Aim for 3–6 sentences per paragraph as a default. Single-sentence paragraphs are acceptable for emphasis but should be rare — one per section, at most. Long paragraphs (10+ sentences) are almost always reducible; the usual fix is to find the natural break where the argument turns.

### Words to avoid (English)

High-frequency AI-generated filler in English:

"It is worth noting that", "it should be noted", "it is important to understand", "essentially", "basically", "in essence", "at the end of the day", "when all is said and done", "needless to say", "it goes without saying", "as we can see", "as mentioned earlier", "as previously discussed", "in today's fast-paced world", "in the ever-evolving landscape of", "it's no secret that", "game-changer", "revolutionize", "harness the power of", "leverage" (as a verb — the noun is fine).

For each of these, the fix is deletion. The sentences almost always work better with the filler removed. If a sentence depends on "It is worth noting that..." to stand up, the sentence is not strong enough, and the fix is to rewrite the sentence, not to add more framing.

### Tone checks (English)

Three questions:

1. Could a good copyeditor cut 15% of the words without losing any meaning? If yes, cut.
2. Is the piece using words a non-native English speaker would struggle with for no good reason? If yes, prefer the simpler word.
3. Does the piece sound like it was written by a single person with a point of view, or by a committee? The first is what you want.

---

## Switching between languages

When the user asks for one language and then for the other partway through, commit fully to the switch. Do not write a bilingual document unless the user asks specifically for one. Bilingual documents almost always serve neither audience well.

If the piece has been drafted in Chinese and the user then asks for an English version, do not translate sentence-by-sentence. Translation usually preserves the Chinese sentence structure, which is wrong for English. Instead, re-draft the English version using the same Anchor Sheet — the argument and the anchors are language-independent, but the prose should be rebuilt in the target language's natural rhythm.

The reverse (English to Chinese) is the same: do not translate, re-draft from anchors. Chinese prose that is the shape of English prose reads as awkward and imported, and Chinese prose that reads as a bad translation undermines the authority the piece is trying to claim.