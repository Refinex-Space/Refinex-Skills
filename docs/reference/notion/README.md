# Notion 写作 Skills 使用手册

本目录说明如何把本仓库的 Write Skills Suite 迁移为 Notion 原生可用的写作能力。这里的产物不是 Codex `SKILL.md`，而是可复制到 Notion 的页面模板：

- `notion/skills/tech-planner.md`
- `notion/skills/tech-writing.md`
- `notion/skills/tech-rewrite.md`
- `notion/instructions/writing-agent.md`

## 官方模型

Notion 的 AI 能力分三层，边界要先分清：

| 能力 | 官方定位 | 适合放什么 |
| --- | --- | --- |
| Skill | 按需触发的已保存 prompt，本质是一个被标记为 Skill 的 Notion 页面 | 重复任务、当前选区或当前页面上的结构化操作 |
| Instructions | 个人 Notion Agent 的持久默认偏好，一次只能启用一份 | 语气、格式、长期写作规则、默认质量标准 |
| Custom Agent | 可自治运行、可后台触发、可拥有自己的 Instructions 和连接 | 定时巡检、数据库自动处理、跨系统自动化 |

官方文档给出的使用准则是：如果一个 prompt 会复制粘贴第二次，它适合做成 Skill；如果一个偏好会被反复纠正，它适合放进 Instructions。我们的三个写作能力是明确的按需任务，因此落为三个 Skill；长期写作偏好则放进一份可选 Instructions。

官方参考：

- [Skills for Notion Agent](https://www.notion.com/help/skills-for-notion-agent)
- [Instructions for Notion Agent](https://www.notion.com/help/instructions-for-notion-agent)

本次设计也用 Context7 的 `/websites/notion_help` 源确认了同一组规则：Skills 是 on-demand action，Instructions 是 default mode，Custom Agents 才适合自治与后台触发。

## 本仓库提供的 Notion 产物

```text
notion/
├── README.md
├── instructions/
│   └── writing-agent.md
└── skills/
    ├── tech-planner.md
    ├── tech-writing.md
    └── tech-rewrite.md
```

### Tech Planner - Notion Skill

用于规划多篇技术文章系列。它继承 `tech-planner` 的核心机制：

- 先做 Research Dossier，不照抄官方文档目录。
- 再做 Concept Dependency Map，标出概念依赖、误解点和 aha moment。
- 最后设计认知递进的 Series Outline，并为每篇文章产出可交给写作 Skill 的 handoff prompt。

典型输入：

```text
@Tech Planner - Notion Skill
规划一个关于 Spring AI 1.0.x 的 8 篇技术博客系列。
目标读者：熟悉 Spring Boot，但刚开始把 LLM 接入生产系统的 Java 后端工程师。
系列目标：读者完成后能解释核心抽象、定位常见生产问题，并做出架构取舍。
```

### Tech Writing - Notion Skill

用于从零写一篇技术文档。它继承 `tech-writing` 的核心机制：

- 正文前必须先产出 Anchor Sheet。
- Anchor Sheet 必须包含中心论点、技术锚点、读者画像、视觉计划、范围边界、叙事声音和文档类型。
- Anchor Sheet 薄弱时先补锚点、查资料或收窄范围，不进入泛泛写作。

典型输入：

```text
@Tech Writing - Notion Skill
写一篇关于 PostgreSQL advisory lock 的技术博客。
中心论点：advisory lock 适合保护应用级临界区，但不适合替代数据库约束；当锁粒度和事务边界不一致时，它会制造隐蔽一致性问题。
目标读者：有 3 年以上后端经验，熟悉事务，但没有系统使用过 advisory lock。
叙事声音：Design Tribunal。
```

### Tech Rewrite - Notion Skill

用于把已有材料重建成高质量技术文档。它继承 `tech-rewrite` 的核心机制：

- 先从源材料提取 Fact Register。
- Fact Register 分为 KEPT、DISCARDED、MISSING、AMBIGUOUS。
- 评估十种污染风险，尤其是 Structural Mirroring、Void Inheritance、Ambiguity Whitewashing 和 Tone Infiltration。
- 写作阶段从 Fact Register 进入 Anchor Sheet，不直接照着源文结构重写。

典型输入：

```text
@Tech Rewrite - Notion Skill
请把当前页面改写成一篇面向工程团队的架构决策记录。
目标读者：后端平台组和 SRE。
目标文档类型：ADR。
请先输出 Fact Register 和缺失信息，不要直接改正文。
```

## 配置步骤

### 创建三个 Skill 页面

1. 在 Notion 中创建一个父页面，例如 `Refinex Writing Skills`。
2. 创建三个子页面，页面标题建议与文件标题一致：
   - `Tech Planner - Notion Skill`
   - `Tech Writing - Notion Skill`
   - `Tech Rewrite - Notion Skill`
3. 分别复制本仓库 `notion/skills/*.md` 的内容到对应页面。
4. 在每个页面右上角打开 `...`，选择 `Use with AI` -> `Use as AI Skill`。
5. 到 `Settings` -> `Notion AI` -> `Skills` 确认三个 Skill 已出现。
6. 如果希望它们出现在文本选择菜单中，在 Skills 设置中对相应页面选择 `Add to text editor menu`。

### 配置可选 Instructions

1. 创建一个页面，例如 `Refinex Writing Agent Instructions`。
2. 复制 `notion/instructions/writing-agent.md` 的内容。
3. 在页面右上角打开 `...`，选择 `Use with AI` -> `Use as AI Instruction`。
4. 到 `Settings` -> `Notion AI` -> `Instructions` 确认它是当前启用的 Instructions。

注意：Notion 个人 Agent 一次只能启用一份 Instructions。共享 Instructions 页面不会自动改变别人的 Agent；对方需要自己设为当前 Instructions。

## 在 Notion 中怎么用

### 从 Notion Agent 聊天触发

在 Notion Agent 聊天中输入 `@` 后选择 Skill 页面名称：

```text
@Tech Planner - Notion Skill
Plan a 6-article series about Kubernetes Operators.
Target version: Kubernetes 1.33.
Target reader: backend engineers who know Deployments and CRDs at a usage level.
Series goal: make controller reconciliation and failure handling understandable.
```

### 从文本选择菜单触发

选中页面中的草稿或笔记，然后从文本选择菜单运行：

```text
Tech Rewrite - Notion Skill
```

适合场景：

- 把会议纪要重建成文章。
- 把旧 wiki 重建成 design doc。
- 把 AI 初稿重建成更有判断力的技术博客。

### 作为 Custom Agent 的能力使用

如果你已经有一个 Notion Custom Agent，只要它有权限访问这三个 Skill 页面，就可以调用它们。只有当你需要后台运行、事件触发、定时处理数据库页面，才应该把这套写作能力包装成 Custom Agent。普通写作、规划和重写任务优先使用 Skills。

## 推荐 Notion 工作流

### 工作流 1：系列规划到单篇文章

1. 运行 `Tech Planner - Notion Skill`。
2. 在同一个 Notion 页面得到 Series Overview、Research Dossier、Concept Dependency Map 和 Series Outline。
3. 复制某篇文章的 handoff prompt。
4. 运行 `Tech Writing - Notion Skill`，让它先生成 Anchor Sheet。
5. 确认 Anchor Sheet 后再生成正文。

### 工作流 2：已有材料重建

1. 打开或选中已有材料页面。
2. 运行 `Tech Rewrite - Notion Skill`。
3. 先审阅 Fact Register，确认 KEPT、DISCARDED、MISSING、AMBIGUOUS。
4. 补齐缺失信息或明确 scope out。
5. 让 Skill 生成 Anchor Sheet 和重建后的正文。

### 工作流 3：长期风格一致

1. 启用 `Writing Agent Instructions`。
2. 把长期偏好放在 Instructions：中文默认、技术术语保留 English、证据先于结论、避免泛泛教程口吻。
3. 把具体任务放在 Skills：规划、写作、重写。

## First-Use Smoke Tests

安装后用下面三个最小任务确认配置正确。

### Planner

```text
@Tech Planner - Notion Skill
规划一个 4 篇文章系列：Project Reactor 错误处理。
目标读者：熟悉 Java Stream，但刚接触 Reactor 的后端工程师。
系列目标：读者能解释 retry、onErrorResume、backpressure 和调试边界。
```

期望：输出包含 Research Dossier、Concept Dependency Map、Series Outline 和 Coherence Notes。

### Writing

```text
@Tech Writing - Notion Skill
写一篇短技术博客：为什么 API timeout 不是一个单一配置。
中心论点：timeout 至少包含连接、读取、整体 deadline 和上游预算四层；只调大一个 HTTP client timeout 会让故障更慢暴露。
目标读者：后端工程师。
```

期望：先输出 Anchor Sheet，而不是直接生成正文。

### Rewrite

```text
@Tech Rewrite - Notion Skill
把当前选中文本改写成技术博客。
目标读者：后端工程师。
请先输出 Fact Register。
```

期望：先输出 KEPT、DISCARDED、MISSING、AMBIGUOUS 和污染风险评估。

## 维护规则

- 修改 Notion Skill 页面时，同步检查 `docs/reference/notion/README.md`。
- 不要把 Notion Skill 写成 Codex `SKILL.md`：不需要 YAML frontmatter，不需要本地路径触发规则。
- 不要把长期偏好塞进每个 Skill 页面；长期偏好属于 Instructions。
- 不要把一次性的具体文章主题写进 Skill 页面；主题来自用户运行 Skill 时的上下文。
- 如果 Notion 官方 UI 名称变化，优先更新配置步骤，但保留 Skill/Instructions/Custom Agent 的概念边界。
