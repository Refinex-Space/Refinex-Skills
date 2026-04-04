@@ AGENTS.md
<!-- HARNESS:MANAGED FILE -->
# ${PROJECT_NAME}

${PROJECT_SUMMARY}

## 启动顺序

1. 先读本文件
2. 再读 [开发计划](docs/PLANS.md)
3. 按任务类型进入对应文档
4. 进入目标目录后读取最近的 `AGENTS.md`

## 任务路由

| 任务类型 | 先读 | 再深入 |
| --- | --- | --- |
| 架构 / 分层 / 边界 | `ARCHITECTURE.md` | `docs/DESIGN.md` |
| 开发计划 / 进度 | `docs/PLANS.md` | `docs/exec-plans/active/` |
| 安全 / 权限 | `docs/SECURITY.md` | 相关源码与约束 |
| 可靠性 / 回滚 | `docs/RELIABILITY.md` | 相关实现与运行手册 |
| 可观测性 / 运行态排障 | `docs/OBSERVABILITY.md` | `docs/generated/` |
| 质量 / 评估 | `docs/QUALITY_SCORE.md` | `docs/generated/` |
${EXTRA_ROUTES}

## 关键约束

- `AGENTS.md` 只做入口地图，不做百科全书
- 根入口图必须短小、最新、可机械检查
- 采用渐进式披露：入口图 -> 专项文档 -> 局部 `AGENTS.md` -> 源码
- 所有正在进行的工作都应落到 `docs/exec-plans/active/`
- 完成后归档到 `docs/exec-plans/completed/`
- 结构性技术债进入 `docs/exec-plans/tech-debt-tracker.md`
- 结构化事实与索引应保持可验证、可更新

## 局部 AGENTS 覆盖

${LOCAL_AGENT_HINTS}

## 机械化入口

- 仓库自检：`python3 scripts/check_harness.py`
- Harness 清单：`docs/generated/harness-manifest.md`
@@ AGENTS.md.extra.frontend
| 前端 / 交互 / 产品行为 | `docs/FRONTEND.md` | `docs/PRODUCT_SENSE.md` |
@@ AGENTS.md.extra.design
| 设计决策 / 多模块演化 | `docs/DESIGN.md` | `docs/design-docs/index.md` |
@@ ARCHITECTURE.md
<!-- HARNESS:MANAGED FILE -->
# ${PROJECT_NAME} Architecture

## 目标

定义当前仓库中不可轻易破坏的系统边界、模块职责与依赖方向。

## 架构不变量

- 在边界处先解析数据，再向内传播
- 避免依赖方向逆流
- 让高风险约束可被测试、检查脚本或生成事实复用
- 对外接口变化需要同步文档、计划与生成事实

## 当前结构概览

${STRUCTURE_SUMMARY}

## 需要长期稳定的边界

- 目录边界：顶层工作区或服务边界保持清晰
- 文档边界：根 `AGENTS.md` 负责路由，细节进入 `docs/`
- 计划边界：执行细节进入 `docs/exec-plans/`
- 生成边界：结构化事实进入 `docs/generated/`
@@ docs/README.md
<!-- HARNESS:MANAGED FILE -->
# Docs

本目录承载仓库级知识系统，供智能体通过渐进式披露读取。

## 建议读取路径

1. 根 `AGENTS.md`
2. `docs/PLANS.md`
3. 对应专题文档
4. 最近的局部 `AGENTS.md`

## 目录

- `PLANS.md`：当前开发计划入口
- `SECURITY.md`：安全基线
- `RELIABILITY.md`：可靠性与回滚约束
- `OBSERVABILITY.md`：日志、指标、链路与运行态排障入口
- `QUALITY_SCORE.md`：质量评估口径
- `exec-plans/`：执行计划与归档
- `exec-plans/tech-debt-tracker.md`：记录结构熵、延后治理与运行盲点
- `generated/`：机械生成或同步的事实
- `references/`：稳定参考资料
${DOCS_EXTRA_INDEX}
@@ docs/README.md.extra.frontend
- `FRONTEND.md`：前端边界与质量要求
- `PRODUCT_SENSE.md`：产品判断规则
- `product-specs/`：行为与验收规格
@@ docs/README.md.extra.design
- `DESIGN.md`：跨模块设计约束
- `design-docs/`：长期设计决策与工程信念
@@ docs/PLANS.md
<!-- HARNESS:MANAGED FILE -->
# Development Plans

> 智能体启动任务前先阅读本文件，确认当前活跃计划与优先级。

## 当前状态

- **活跃计划**：`${ACTIVE_PLAN_PATH}`
- **Harness 状态**：通过 `scripts/check_harness.py` 持续维护
- **结构性技术债**：`docs/exec-plans/tech-debt-tracker.md`

## 活跃计划入口

- [${ACTIVE_PLAN_LABEL}](${ACTIVE_PLAN_PATH})

## 规则

1. 新任务需要创建或复用 `docs/exec-plans/active/` 中的活跃计划
2. 完成后归档到 `docs/exec-plans/completed/`
3. 结构性技术债与延后治理写入 `docs/exec-plans/tech-debt-tracker.md`
4. `PLANS.md` 保持短小，只做高层入口，不复制执行细节
@@ docs/SECURITY.md
<!-- HARNESS:MANAGED FILE -->
# Security Baseline

## 目标

将仓库的最小安全基线写成可复用约束，避免智能体在高吞吐修改中破坏边界。

## 基线

- 秘密信息不得明文提交
- 输入应在边界处校验
- 高风险外部调用需要显式约束
- 安全相关行为变化必须同步文档与验证

## 审查优先级

1. 秘钥与凭据
2. 权限边界
3. 输入校验
4. 日志与敏感信息暴露
@@ docs/RELIABILITY.md
<!-- HARNESS:MANAGED FILE -->
# Reliability

## 目标

定义仓库的运行可靠性约束、回滚意识与故障管理基线。

## 默认要求

- 关键路径需要有验证方案
- 失败时优先留下可诊断信息
- 变更应具备可回滚思路并限制爆炸半径
- 执行计划中应记录风险与验证证据
- 运行态可见性要求应沉淀到 `docs/OBSERVABILITY.md`
@@ docs/OBSERVABILITY.md
<!-- HARNESS:MANAGED FILE -->
# Observability

## 目标

让未来的智能体能够直接理解系统运行态，而不是依赖口头描述或零散记忆。

## 必备观测面

- 关键日志与错误证据
- 重要指标或耗时信号
- 可用时提供 traces / request flow 线索
- UI 场景尽量提供浏览器或端到端验证入口

## 默认要求

- 优先可脚本化的检查方式，减少纯人工描述
- 将命令、面板、调试入口保持可发现
- 如果仓库支持隔离 worktree 或按任务启动环境，应在此记录用法
- 重复出现的盲点记录到 `docs/exec-plans/tech-debt-tracker.md`
@@ docs/QUALITY_SCORE.md
<!-- HARNESS:MANAGED FILE -->
# Quality Score

## 目标

把“质量好不好”从主观判断转成结构化维度，供评估智能体和维护者复用。

## 评估顺序

1. Security
2. Correctness
3. Performance
4. Readability

## Harness 质量维度

- 路由是否清晰
- 文档是否可索引
- 计划是否闭环
- 生成事实是否同步
- 运行态是否足够可见、验证证据是否充分
- 局部 `AGENTS.md` 是否覆盖关键边界
@@ docs/FRONTEND.md
<!-- HARNESS:MANAGED FILE -->
# Frontend Guide

## 目标

为前端或界面相关工作提供专门路由、边界和体验约束。

## 关注点

- 组件边界与状态边界
- 体验一致性
- 无障碍与性能
- 前端不得绕开既定后端或服务边界
- 如仓库支持，应优先通过浏览器或端到端检查验证真实行为

## 建议继续阅读

- `docs/PRODUCT_SENSE.md`
- `docs/product-specs/index.md`
- `docs/OBSERVABILITY.md`
@@ docs/PRODUCT_SENSE.md
<!-- HARNESS:MANAGED FILE -->
# Product Sense

## 目标

记录产品判断原则，降低功能扩张和局部最优导致的偏离。

## 默认判断

- 先让主路径可用，再做外围优化
- 先提升可验证性，再增加复杂度
- 新能力需要明确用户价值与验收标准
@@ docs/product-specs/index.md
<!-- HARNESS:MANAGED FILE -->
# Product Specs Index

按需在本目录下补充产品行为规格、用户路径与验收标准。

## 推荐内容

- 核心用户路径
- 关键状态流
- 失败与边界条件
- 非功能要求
@@ docs/DESIGN.md
<!-- HARNESS:MANAGED FILE -->
# Design Guide

## 目标

记录跨模块设计约束与共享决策，避免不同区域独立演化后失去一致性。

## 适用场景

- 多模块协作
- 接口边界调整
- 数据流与职责迁移
- 长期设计共识沉淀
@@ docs/design-docs/index.md
<!-- HARNESS:MANAGED FILE -->
# Design Docs Index

在此索引长期有效的设计决策与深层架构说明。

## 推荐条目

- `core-beliefs.md`
- 关键分层与边界设计
- 重要技术选型与取舍
@@ docs/design-docs/core-beliefs.md
<!-- HARNESS:MANAGED FILE -->
# Core Beliefs

记录那些不会因一次功能实现而轻易改变的长期工程信念。

## 示例

- 优先保持边界清晰
- 先把经验写成系统能力，再依赖人工记忆
- 让计划、索引和生成事实始终可被下一个智能体继续接手
@@ docs/exec-plans/tech-debt-tracker.md
<!-- HARNESS:MANAGED FILE -->
# Tech Debt Tracker

在这里持续记录重复出现的 Harness 漂移、延后治理项和运行盲点。

## 推荐字段

- debt item
- impact or risk
- current workaround
- preferred fix
- owner or next checkpoint
@@ docs/exec-plans/completed/README.md
<!-- HARNESS:MANAGED FILE -->
# Completed Plans

> 已完成的执行计划归档目录。

## 归档格式

在已完成计划顶部补充：

```markdown
> ✅ Completed: YYYY-MM-DD
> Summary: <一句话总结>
> Duration: <实际周期>
> Key learnings: <关键经验>
```
@@ docs/generated/README.md
<!-- HARNESS:MANAGED FILE -->
# Generated Facts

本目录用于存放由脚本维护的机械事实。

## 默认生成内容

- `harness-manifest.md`：当前 Harness 覆盖情况与机械入口
- 未来可扩展为 schema 快照、路由清单、库存清单等
@@ docs/references/index.md
<!-- HARNESS:MANAGED FILE -->
# References Index

本目录用于存放智能体会反复查阅的稳定参考。

## 适合放入的内容

- runbooks
- 领域术语表
- 集成说明
- 重复排障命令
