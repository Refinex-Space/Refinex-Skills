# Write Skills 技术写作套件

## 设计背景:为什么是三个 Skill,而不是一个

技术写作的失败模式不止一种,每一种都需要专门的防御机制。

把"帮我写一篇技术博客"和"帮我把这份会议纪要改写成一篇技术博客"交给同一个 Skill,看似合理——毕竟最终产物都是一篇博客。但这两个任务的核心风险完全不同。前者的风险是 **anchor hunger**:缺少具体技术锚点时,AI 会自动滑向百科全书式的描述。后者的风险是 **style contamination**:低质量源材料的结构、语气、含糊表述会悄悄渗入输出,即使你明确要求"改写"。两种风险需要两种不同的程序化防线。

再加上第三个场景——"我要写一个关于 Spring AI 的系列,帮我做规划"——就引入了第三种风险:**surface skating**,即 AI 生成的系列大纲看起来全面,实际上只是复制了官方文档的目录结构。

三个 Skill 解决三种不同的问题,但共享同一套质量标准。现在这套标准额外下沉出一层专门的 `mermaid-diagrams` 技能,负责把视觉计划落成稳定、克制、可移植的 Mermaid。设计核心不变:无论内容经由哪条路径产出,最终文档的质量不可区分,图表标准也不可分叉。

---

## 三个 Skill 的定位

### mermaid-diagrams — 共享图表执行层

解决的问题:一旦文档确认需要 Mermaid 图,真正困难的部分不是"知道 Mermaid 存在",而是把图写到语法稳定、跨 Markdown 渲染器可移植、视觉克制且不拥挤。这个 Skill 专门负责这一层。

核心防线:Portable Authoring Standard(可移植绘图标准)。它把 Mermaid 的工作拆成四步:先锁定读者问题和图类型,再设计几何结构和节点预算,随后只使用最低风险的 Markdown Mermaid 语法子集,最后在必要时追加极少量语义化样式。美观首先来自结构、方向、标签长度和拆图策略,不是来自花哨配色。

### tech-writing — 从零创作

解决的问题:用户有一个技术论点或决策要记录,但没有任何现成草稿。这是白纸起步的场景。

核心防线:Pre-writing Protocol(预写协议)。在写任何一句话之前,必须先产出一份 Anchor Sheet,包含五个要素——中心论点(可证伪的一句话)、技术锚点(真实数字、具体失败机制、被否决的备选方案)、读者画像、范围边界、叙事声音。Anchor Sheet 薄弱时,技能会拒绝进入写作阶段,而不是用泛泛的散文掩盖不足。

支持的文档类型:技术博客、ADR、架构设计文档、技术对比、源码深潜、API 文档、迁移指南。

### tech-rewrite — 从已有材料重建

解决的问题:用户有现成材料——内部笔记、会议纪要、AI 生成的初稿、遗留 wiki、代码注释——需要转化为高质量技术文档。

核心防线:Extraction Firewall(提取防火墙)。阅读源材料和写作输出是两个分离的阶段,中间由一份 Fact Register(事实登记表)作为唯一桥梁。Fact Register 将源材料中每一条具体、可验证的声明提取出来(KEPT),将含糊不清的声明标记为不可用(DISCARDED),将源材料遗漏的关键信息列为缺失项(MISSING),将歧义声明单独存放等待确认(AMBIGUOUS)。写作阶段从 Fact Register 工作,不再回看源材料。

识别并防御的十种污染机制:Structural Mirroring(结构镜像)、Void Inheritance(空缺继承)、Ambiguity Whitewashing(模糊粉饰)、Tone Infiltration(语气渗透)、Rationale Vacuum(理由真空)、False Completeness(虚假完整性)、Scope Inflation(范围膨胀)、Confidence Upgrade(信心升级)、Terminology Drift(术语漂移)、Pseudoanchor Import(伪锚点引入)。

### tech-planner — 系列规划

解决的问题:用户给出一个技术目标(如 "Spring AI"、"Project Reactor"、"Kubernetes Operators"),需要一份详尽的多篇博客系列创作大纲。

核心防线:Three-phase Research Protocol(三阶段研究协议)。Phase 1 是 Source Exhaustion(穷尽源头),系统性地消化官方文档、源代码、release notes、GitHub issues、权威二手资料。Phase 2 是 Knowledge Graph Construction(知识图谱构建),将概念、前置依赖、"官方叙事"与"真实使用模式"之间的差距可视化。Phase 3 是 Series Architecture Design(系列架构设计),基于知识图谱设计认知递进的文章序列,每篇文章配有一个可以直接复制粘贴到 tech-writing 的完整 prompt。

系列架构遵循 Bruner 的螺旋课程原则:真正的螺旋在每次重访概念时增加复杂度,而循环只是重复。tech-planner 的十二道质量门在交付前逐一验证大纲是否存在文档镜像、主题标签式标题、难度标签式阶段名、前置依赖遗忘、循环伪装成螺旋等失败模式。

---

## 三个 Skill 如何协同:Pipeline 架构

三个 Skill 形成一条流水线,每个阶段的输出是下一个阶段的输入,而 `mermaid-diagrams` 作为共享执行层插在所有需要图表的节点上:

```
tech-planner
    ↓ 产出:系列大纲 + 每篇文章的 tech-writing prompt
    ↓
tech-writing (从零创作) ← 或 → tech-rewrite (从已有材料重建)
    ↓                                ↓
    ↓ 产出:高质量技术文档              ↓ 产出:高质量技术文档
    ↓                                ↓
    └─── 共享质量标准 ──────────────────┘
                    ↓
            mermaid-diagrams
         负责任何 Mermaid 图的最终落地
```

关键的汇合点在 Anchor Sheet。tech-writing 的 Phase 1 直接产出 Anchor Sheet;tech-rewrite 的 Phase 2 从 Fact Register 产出 Anchor Sheet;tech-planner 生成的 prompt 包含足够信息让 tech-writing 的 Phase 1 自动填充 Anchor Sheet。三条路径在同一个格式上汇合,从此之后走同一套写作和验证流程。

这意味着:

如果你只需要写一篇文章,直接使用 tech-writing 或 tech-rewrite,不需要 tech-planner。

如果你要规划一个系列,先用 tech-planner 产出大纲,然后逐篇使用 tech-writing(或 tech-rewrite,如果某篇有现成素材)。

如果你不确定用哪个,参考下面的选择速查表。

---

## Skill 选择速查表

| 你的场景 | 使用的 Skill |
|---------|------------|
| 有一个技术论点,没有任何草稿,要写一篇文章 | tech-writing |
| 有现成笔记/草稿/wiki/AI 初稿,要转化为正式文档 | tech-rewrite |
| 要规划一个多篇文章的技术博客系列 | tech-planner |
| tech-planner 产出的某篇文章 prompt,要开始写作 | tech-writing |
| tech-planner 产出的某篇文章 prompt + 已有相关素材 | tech-rewrite |
| 已经知道要画什么图,现在只需要把视觉计划写成稳定的 Mermaid | mermaid-diagrams |
| 已有一篇已发布文章,要基于读者反馈改写 | tech-rewrite |
| 要做技术对比(X vs Y)并给出结论 | tech-writing |
| 有一份旧的技术对比文档,要更新到新版本 | tech-rewrite |
| 要写一篇 post-mortem | tech-writing |
| 有一份 incident report 草稿,要改写成 post-mortem 博客 | tech-rewrite |

判断标准分两层:先判断你是在写作还是在落图。只是在落 Mermaid 图 → `mermaid-diagrams`。如果是在写作,再看有没有现成源材料:有 → `tech-rewrite`;没有 → `tech-writing`;要规划一个系列 → `tech-planner`。

---

## 共享质量标准

三个 Skill 共享同一套质量规则。tech-writing 定义了这些规则,tech-rewrite 通过字面复制的 `shared-*` 文件继承它们,tech-planner 通过生成符合这些规则的 prompt 来保证下游输出质量。`mermaid-diagrams` 则接管所有 Mermaid 图的语法、排布和视觉克制标准,让写作 Skill 不再各自发明图表风格。

以下是所有文档必须通过的非妥协质量门:

**结构层面。** 标题承载论点,而非主题标签。每篇文档有头部信息块(范围、假设的前置知识、中心论点)。60 秒规则:开篇段落必须陈述中心论点。比较章节必须以明确的裁决结尾——永远不允许"两者各有优劣"。每个设计决策必须列出被否决的备选方案及其具体理由。

**深度层面。** 失败模式必须描述具体的因果链,而非笼统的类别。限制条件章节必须给出具体的阈值和边界条件。资深工程师测试:如果某个章节没有教给资深工程师任何他们从官方文档五分钟内学不到的东西,要么加深要么删除,没有第三选项。

**语言层面。** 中文输出时,技术术语保留英文(类名、方法名、配置键、协议名、CLI 标志、指标名)。语气是"资深工程师在设计评审中向同事解释",不是教程、不是营销、不是面向初学者的手把手。英文输出时,优先使用盎格鲁-撒克逊词汇(use 而非 utilize,start 而非 commence),默认主动语态,现在时描述行为。

**反模式层面。** 二十种已编目的 AI 气息反模式被逐一扫描:false balance、empty superlatives、background stuffing、passive responsibility avoidance、hedge stacking、Wikipedia-voice opening、restating the question、"comprehensive guide" framing、bullet-point avoidance of prose、encyclopedic drift、missing rejected alternatives、"under the hood, magic happens"、tutorial voice in non-tutorial pieces、the restating conclusion、"in this post" meta-references、bullet-list tabulation without synthesis、present-tense-about-the-future、"best practices" without context、invented precision、the senior-engineer-insulting paragraph。

---

## 六种叙事声音

每篇文档必须在写作前选定一种叙事声音,并在全文保持一致。声音不是语气(正式/随意),而是立场——作者对材料做什么。

**Production War Story** — 事后复盘、运营教训。以症状开篇,以结构性教训结尾。权威来源于事件的具体性。

**Design Tribunal** — 架构决策、技术对比。以标准和裁决为核心。每个备选方案被命名并以具体理由否决。不允许"两者各有优劣"的结论。

**Mechanism Autopsy** — 源码深潜、协议分析。以文件路径、行号、版本号为锚。权威来源于代码级的精确性。

**Migration Field Guide** — 升级指南、迁移手册。以命令式语气写作,以坑和回滚计划为核心。不写回滚计划的迁移指南不是指南。

**Benchmarker's Notebook** — 性能对比,数字和方法论为核心。权威来源于可复现性。

**Reference Librarian** — 纯 API 参考。不争论,只描述。唯一一种"只描述事物做什么"是正确做法的声音。

---

## 推荐使用模板

### 模板 1:从零写一篇技术博客

```
请帮我写一篇关于 [主题] 的技术博客。

中心论点:[一句可证伪的陈述]
目标读者:[具体描述,包括已知知识和可能的误解]
叙事声音:[从六种中选一种]
```

tech-writing 会先产出 Anchor Sheet,展示给你确认后再进入写作阶段。如果论点不够尖锐或锚点不足,它会告诉你缺什么并提出补充方案。

### 模板 2:改写现有材料

```
请帮我把以下材料改写成一篇 [文档类型]:

[粘贴源材料]

目标读者:[具体描述]
目标文档类型:[博客/ADR/设计文档/对比/深潜/API 文档/迁移指南]
```

tech-rewrite 会先产出 Fact Register,展示给你确认后再进入写作阶段。它会明确告诉你源材料中哪些声明被保留(KEPT)、哪些被丢弃(DISCARDED)、哪些是缺失的(MISSING)、哪些需要你确认(AMBIGUOUS)。

### 模板 3:规划一个技术博客系列

```
请帮我规划一个关于 [框架/库/协议名称] 的技术博客系列。

目标版本:[具体版本号]
目标读者:[具体描述,包括他们从哪个技术背景来]
系列目标:[读者完成系列后能做什么]
```

tech-planner 会先进行深度研究(官方文档、源代码、release notes、GitHub issues、权威二手资料),然后构建知识图谱,最后产出一份详细的系列大纲。大纲中每篇文章都附带一个完整的 tech-writing prompt,可以直接复制粘贴到 tech-writing 开始写作。

### 模板 4:从系列大纲到具体文章

当 tech-planner 产出大纲后,逐篇执行:

```
[直接复制粘贴 tech-planner 产出的某篇文章的 prompt block]
```

每个 prompt block 以 `/tech-write` 开头,包含 `<prompt>` 标签,内含中心论点、叙事声音、技术锚点、读者画像、前置知识、范围边界和参考链接。直接粘贴即可,无需额外编辑。

---

## 七种文档类型及其对应结构

三个 Skill 共享七种文档类型的结构定义。每种类型有自己的必需章节、排列规则和专属质量门。

| 文档类型 | 典型声音 | 核心结构要求 |
|---------|---------|------------|
| 技术博客 | 任意(Reference Librarian 除外) | 论点式标题、hook 开篇、60 秒规则、四种结尾手法之一 |
| ADR | Design Tribunal | Title/Status/Context/Decision/Consequences 五段式,Decision 用 "We will..." 语态 |
| 架构设计文档 | Design Tribunal(中性) | Goals/Non-goals、Detailed Design、Alternatives Considered、Cross-cutting Concerns |
| 技术对比 | Design Tribunal | 显式标准列表、逐标准评估、有条件的裁决、裁决翻转条件 |
| 源码深潜 | Mechanism Autopsy | 版本标注、代码锚点(文件路径+行号)、以可复用心智模型结尾 |
| API 文档 | Reference Librarian | 每个 endpoint 相同的 layout、穷尽 error 列表、可运行的 example |
| 迁移指南 | Migration Field Guide | "不要做这个迁移如果..."章节、坑列表、回滚计划、验证步骤 |

---

## 关于质量一致性的说明

这三个 Skill 的质量一致性不是靠"风格统一"实现的,而是靠结构性保证:

**同一份质量检查表。** tech-writing 定义了十三道质量门(Gate 0 到 Gate 12),tech-rewrite 通过 `shared-quality-standards.md` 文件字面继承了同一份检查表。两个 Skill 在 Phase 3 / Phase 4 中运行的是物理上相同的验证循环。

**同一份反模式目录。** 二十种 AI 气息反模式在 `shared-anti-patterns.md` 中编目,两个 Skill 在 Gate 9 中对同一份目录执行扫描。

**同一份声音目录。** 六种叙事声音在 `shared-narrative-voices.md` 中定义,含 before/after 示例和漂移诊断。两个 Skill 引用的是同一个文件。

**同一份语言规范。** 中英文写作规范在 `shared-language-conventions.md` 中定义。技术术语保留英文、中英文间加半角空格、中文标点在中文语境中使用等规则,两个 Skill 执行的是同一套。

**同一组文档类型定义。** 七种文档类型的结构在七份 `shared-doctype-*.md` 文件中定义。tech-writing 和 tech-rewrite 读取的是同一组文件。

**Anchor Sheet 作为汇合点。** tech-writing 的 Phase 1 直接产出 Anchor Sheet;tech-rewrite 的 Phase 2 从 Fact Register 产出 Anchor Sheet;tech-planner 的 prompt 包含足以填充 Anchor Sheet 的全部信息。三条路径汇合后,走的是同一段写作和验证流程。一个只看到 Anchor Sheet 的人,无法判断它来自哪个 Skill,这正是设计意图。

这意味着:如果你对 tech-writing 产出的一篇文章质量满意,你可以预期 tech-rewrite 在同一主题上的输出达到同等水平,反之亦然。两个 Skill 之间的差异仅在输入阶段(一个从零开始,一个从源材料提取),而在输出阶段完全收敛。

---

## Skill 文件清单

### mermaid-diagrams（6 个文件）

```
mermaid-diagrams/
├── SKILL.md                              # 入口:共享 Mermaid 执行标准
├── agents/
│   └── openai.yaml                       # UI 元数据和默认触发提示
└── references/
    ├── authoring-standard.md             # 可移植语法子集和 parser 风险规则
    ├── styling-standard.md               # 克制配色与最小样式纪律
    ├── pattern-cookbook.md               # 各 Mermaid 图类型的默认模式
    └── final-checklist.md                # 交付前最后校验门
```

### tech-writing（14 个文件）

```
tech-writing/
├── SKILL.md                              # 入口:工作流、预写协议、质量标准摘要
└── references/
    ├── pre-writing-protocol.md           # Anchor Sheet 详细协议和示例
    ├── narrative-voices.md               # 六种声音定义、before/after 示例
    ├── quality-checklist.md              # 十三道质量门(可执行验证循环)
    ├── anti-patterns.md                  # 二十种 AI 气息反模式目录
    ├── language-conventions.md           # 中英文写作规范
    ├── doctype-blog-post.md             # 技术博客结构
    ├── doctype-adr.md                   # ADR 结构(Nygard + MADR)
    ├── doctype-design-doc.md            # 架构设计文档结构(Google 风格)
    ├── doctype-comparison.md            # 技术对比结构
    ├── doctype-deep-dive.md             # 源码深潜结构
    ├── doctype-api-doc.md               # API 文档结构
    └── doctype-migration-guide.md       # 迁移指南结构
```

### tech-rewrite（18 个文件）

```
tech-rewrite/
├── SKILL.md                              # 入口:提取工作流、污染机制、写作标准
└── references/
    ├── contamination-mechanisms.md       # 十种污染机制(含 before/after 示例)
    ├── extraction-protocol.md           # Fact Register 方法论和示例
    ├── fact-register-template.md        # Fact Register 工作模板
    ├── contamination-risk-assessment.md # 污染风险评估诊断工具
    ├── rewrite-checklist.md             # 改写专属质量门(Gate R1–R10)
    ├── shared-quality-standards.md      # ← 来自 tech-writing 的字面拷贝
    ├── shared-narrative-voices.md       # ← 来自 tech-writing 的字面拷贝
    ├── shared-anti-patterns.md          # ← 来自 tech-writing 的字面拷贝
    ├── shared-language-conventions.md   # ← 来自 tech-writing 的字面拷贝
    ├── shared-diagram-selection-guide.md # ← 来自 tech-writing 的字面拷贝
    ├── shared-doctype-blog-post.md      # ← 来自 tech-writing 的字面拷贝
    ├── shared-doctype-adr.md            # ← 来自 tech-writing 的字面拷贝
    ├── shared-doctype-design-doc.md     # ← 来自 tech-writing 的字面拷贝
    ├── shared-doctype-comparison.md     # ← 来自 tech-writing 的字面拷贝
    ├── shared-doctype-deep-dive.md      # ← 来自 tech-writing 的字面拷贝
    ├── shared-doctype-api-doc.md        # ← 来自 tech-writing 的字面拷贝
    └── shared-doctype-migration-guide.md # ← 来自 tech-writing 的字面拷贝
```

### tech-planner（9 个文件）

```
tech-planner/
├── SKILL.md                              # 入口:三阶段研究协议、系列架构方法论
└── references/
    ├── research-methodology.md          # Phase 1 详细事实搜集协议
    ├── knowledge-graph-construction.md  # Phase 2 概念依赖映射
    ├── series-patterns.md               # 六种系列架构模式及选择规则
    ├── phase-naming-guide.md            # 认知递进阶段命名规范
    ├── prompt-template.md               # tech-writing prompt 模板及示例
    ├── outline-quality-checklist.md     # 十二道大纲质量门
    ├── example-outlines.md              # 弱/强大纲配对示例(三个框架)
    └── worked-example.md                # Spring AI 系列完整 walkthrough
```
