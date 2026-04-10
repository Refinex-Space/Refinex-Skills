English Version: [README.md](README.md)

# Refinex-Skills

基于 MIT License 开源的个人高质量 Skill 套件，覆盖三个互补的工程领域：
面向代码侧严谨性的 Harness Engineering、面向 Office 交付物的 Office
Skills，以及面向文档质量的 Write Skills。

---

## Skill 套件

### Office Skills 套件

四个配套 Skill，覆盖常见 Office 家族交付物。它们从原来的文件扩展名式
命名统一重命名为 `office-*`，目的是让整套能力在提示词、索引和文档里更
清晰，也避免与泛化文件类型词冲突：

- `office-docx`
- `office-pdf`
- `office-pptx`
- `office-xlsx`

1. `office-docx`
   用于创建、检查、编辑和验证 Word `.docx` 文档。
2. `office-pdf`
   用于读取、生成、转换、提取和填写 PDF 文档。
3. `office-pptx`
   用于构建、审阅和修改 PowerPoint `.pptx` 演示文稿。
4. `office-xlsx`
   用于创建、清洗、分析和重算电子表格交付物。

来源说明：
- 这四个 Skill 来源于 Anthropic 提供的 `anthropics/skills` 仓库，
  原始定位是其中的 document skills：
  https://github.com/anthropics/skills

文档：[docs/office-suite.zh.md](docs/office-suite.zh.md)

---

### Write Skills 套件

三个互补 Skill，分别覆盖技术文档的规划、从零写作、基于材料重建：

- `tech-planner`
- `tech-writing`
- `tech-rewrite`

1. `tech-planner`
   先规划，再动笔。定位在研究框架、提纲设计、系列文章规划、阶段命名、
   prompt 组织等前置工作，适合在正式写作前先把结构搭起来。

2. `tech-writing`
   从零创作。在生成任何正文之前，强制执行**写前协议**——中心论点、具体
   技术锚点、读者认知审计、范围边界、叙述声音，全部在写作开始前确定。
   对抗**锚点饥饿**：AI 在没有具体技术基础时自动滑向百科全书式输出——
   只描述事物是什么，从不对它们意味着什么作出判断。

   **触发场景：** 写一篇关于 X 的技术博客、为 Y 起草架构文档、对比 X 和 Y、
   写一份 ADR、深入解析 X 的工作原理、为 Z 编写 API 文档。

3. `tech-rewrite`
   基于任意质量的现有材料重建——内部笔记、会议纪要、AI 生成的草稿、遗留
   Wiki、代码注释。在提取阶段和写作阶段之间强制建立严格隔离。源材料绝不
   作为写作模板使用；所有事实被提取进结构化的 Fact Register，然后才开始
   写第一个字。对抗**风格污染**：结构镜像、虚空继承、模糊性漂白、语气渗透、
   决策理由缺失、虚假完整性、范围膨胀。

   **触发场景：** 重写这份文档、整理我的笔记、这份草稿质量很差帮我修好、
   把这些内容变成一篇正式文章、基于这份材料写一篇关于 X 的文档、改进这份文档。

文档：[docs/write-suite.zh.md](docs/write-suite.zh.md)

---

## 仓库结构

```text
Refinex-Skills/
├── docs/
│   ├── harness-suite.en.md
│   ├── harness-suite.zh.md
│   ├── office-suite.en.md
│   ├── office-suite.zh.md
│   ├── write-suite.en.md
│   └── write-suite.zh.md
├── skills/
│   ├── harness-bootstrap/
│   ├── harness-garden/
│   ├── harness-feat/
│   ├── harness-fix/
│   ├── office-docx/
│   ├── office-pdf/
│   ├── office-pptx/
│   ├── office-xlsx/
│   ├── tech-planner/
│   ├── tech-writing/
│   └── tech-rewrite/
├── .gitignore
├── LICENSE
├── README.md
└── README.zh.md
```

## 说明文档

**Harness Engineering 套件**
- English: [docs/harness-suite.en.md](docs/harness-suite.en.md)
- 中文: [docs/harness-suite.zh.md](docs/harness-suite.zh.md)

**Office Skills 套件**
- English: [docs/office-suite.en.md](docs/office-suite.en.md)
- 中文: [docs/office-suite.zh.md](docs/office-suite.zh.md)

**Write Skills 套件**
- English: [docs/write-suite.en.md](docs/write-suite.en.md)
- 中文: [docs/write-suite.zh.md](docs/write-suite.zh.md)

## 典型使用方式

**Harness Engineering — 在已接入或准备接入 Harness 的仓库里，推荐流程如下：**

```text
$harness-bootstrap  -> 首次安装 / 补齐控制面
$harness-garden     -> 漂移审计 / 修复
$harness-feat       -> 新功能 / 重构任务
$harness-fix        -> Bug / 回归 / 故障修复
```

**Write Skills — 推荐生命周期：**

```text
tech-planner  -> 先把主题变成研究计划 / 提纲 / 系列结构
tech-writing  -> 在锚点明确后，从空白页直接起草
tech-rewrite  -> 基于笔记、草稿或遗留文档做重建
```

**Write Skills — Skill 选择速查表：**

| 起点 | 目标文档类型 | 使用 Skill |
|---|---|---|
| 只有主题或想法，还没有结构 | 研究计划、提纲、系列地图 | `tech-planner` |
| 有主题和观点，无现有材料 | 博客、深度分析 | `tech-writing` |
| 需要记录一个架构决策 | ADR | `tech-writing` |
| 需要设计并记录一个新模块 | 模块设计文档 | `tech-writing` |
| 需要为技术选型提供依据 | 对比指南 | `tech-writing` |
| 现有文档存在质量问题 | 任意类型 | `tech-rewrite` |
| AI 生成的草稿需要改进 | 任意类型 | `tech-rewrite` |
| 会议纪要 / 内部 Wiki | 博客、设计文档 | `tech-rewrite` |
| 代码注释 + 散落笔记 | 模块文档、ADR | `tech-rewrite` |

完整使用模板（技术博客、ADR、模块设计、选型对比、重写、笔记变文章）
详见 [docs/write-suite.zh.md](docs/write-suite.zh.md)。

## 许可

MIT。详见 [LICENSE](LICENSE)。
