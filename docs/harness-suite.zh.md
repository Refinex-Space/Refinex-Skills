## Harness Engineering 套件

Harness Engineering 套件是一组面向 agent-first 软件开发的仓库控制面能力。稳定内核仍然是四个工作流技能，但现在补上了两个横切技能，分别负责任务路由与完成验证。它把随意编码转成可治理闭环：先做 preflight，再做版本化执行计划，再用验证证据收口，最后归档形成可交接资产。

这套能力面向真实仓库长期运行场景，目标是在持续交付代码的同时，保持架构一致性、可审计性和跨会话连续性。

---

## 为什么需要这套技能

没有仓库级 Harness 时，长流程 coding agent 往往会出现这些问题：

- 没有基线就开始改，回归归因混乱。
- 不做计划直接实现，意图无法追溯。
- 控制面文档长期漂移，后续会话持续被过期信息误导。
- 修 bug 只打补丁，不做根因隔离。

Harness 套件把这些风险拆解为四类职责：初始化、养护、建设、修复。

---

## 核心四件套 + 两个横切技能

| Skill | 核心使命 | 典型触发 |
| --- | --- | --- |
| `harness-bootstrap` | 初始化或补齐仓库控制面 | 新仓库、历史仓库未接入 Harness |
| `harness-garden` | 审计并修复控制面漂移 | 文档陈旧、链接失效、命令失效 |
| `harness-feat` | 在控制面内交付新功能与结构化重构 | 新能力开发、计划内增强 |
| `harness-fix` | 在控制面内诊断并修复 bug/回归/故障 | 测试失败、线上问题、flaky 路径 |
| `harness-using` | 为仓库任务路由到正确的 Harness 工作流 | 会话开始、工作流归属不明确 |
| `harness-verify` | 在宣称完成前强制要求新鲜证据 | “完成了/修好了/通过了/ready” 这类时刻 |

---

## 工作流定位

把它看作同一个操作模型：

1. `harness-using` 先判断任务应该进入哪条 Harness 流程。
2. `harness-bootstrap` 在缺基线时先建立控制面。
3. `harness-garden` 持续保证控制面描述仍然真实。
4. `harness-feat` 在控制面内做增量建设。
5. `harness-fix` 在控制面内做证据驱动修复。
6. `harness-verify` 在结束前拦截不具备证据的成功宣称。

推荐生命周期：

```text
$harness-using      -> 先路由任务
$harness-bootstrap  -> 建立控制面
$harness-garden     -> 保持控制面真实
$harness-feat       -> 安全交付新能力
$harness-fix        -> 基于根因证据修复故障
$harness-verify     -> 在收口前验证证据
```

---

## 共享控制面概念

四个技能使用同一套术语和工件：

- Control plane: AGENTS.md + docs + scripts + manifest
- Preflight: `python3 scripts/check_harness.py`
- Execution plans: `docs/exec-plans/active/` 与 `docs/exec-plans/completed/`
- 全局索引: `docs/PLANS.md`
- 漂移跟踪与生成状态: `docs/generated/harness-manifest.md`

统一语义的价值在于：不同技能之间切换时不需要重新建立上下文。

其中四件套 (`bootstrap`、`garden`、`feat`、`fix`) 仍然负责生命周期主流程；`harness-using` 与 `harness-verify` 负责横切约束，不争夺主流程所有权。

---

## 技能说明

### 1. harness-bootstrap

定位：
- 为仓库安装或补齐 Harness 控制面。

核心行为：
- 先 reconnaissance，再生成文件。
- 产物可验证、可重复。
- 保护团队已有文档（不做覆盖式破坏）。
- 使用 `scripts/check_harness.py` 做基线验证。

适用场景：
- 全新仓库。
- 已有仓库但控制面缺失或不完整。

主要产物：
- Root 与必要的 module AGENTS.md。
- docs 路由与治理文档。
- manifest 与 preflight 脚本。

### 2. harness-garden

定位：
- 持续发现并修复控制面漂移。

核心行为：
- 先做 manifest 完整性检查。
- 再做语义漂移审计（命令、路径、描述、链接）。
- 低风险漂移自动修复。
- 高风险项产出 remediation execution plan。

适用场景：
- agent 反馈说明不可信或过期。
- 文档结构与代码结构不再一致。
- 控制面健康状态不确定。

主要产物：
- 漂移清单与修复变更。
- 更新后的控制面文档。
- 审计报告与可追溯记录。

### 3. harness-feat

定位：
- 在治理流程内交付 feature 与结构化 refactor。

核心行为：
- 编码前 preflight。
- 将需求重写为 sprint contract。
- 创建版本化 execution plan。
- 小步实现并持续验证。
- 归档计划并同步 `docs/PLANS.md`。

适用场景：
- 用户提出新功能开发。
- 需要可验证的重构交付。

主要产物：
- 带证据日志的 feature execution plan。
- 与计划步骤绑定的增量提交。
- 可交接的归档记录。

### 4. harness-fix

定位：
- 诊断并修复 bug、回归、故障与 flaky 路径。

核心行为：
- 固化 known-broken baseline。
- 生成结构化 bug brief。
- 先复现再修复。
- 用假设-实验法隔离根因。
- 在 fix scope guard 下做最小修复。
- 增加 regression protection 并归档 fix plan。

适用场景：
- 测试出现非预期失败。
- 用户反馈功能故障。
- 间歇性失败需要诊断。

主要产物：
- 含 root cause 的 fix plan。
- 假设与证据链。
- 回归测试保护。

---

## 选择指南

快速路由：

| 场景 | Skill |
| --- | --- |
| 仓库没有 Harness 或 Harness 不完整 | `harness-bootstrap` |
| Harness 已存在但可能漂移 | `harness-garden` |
| 需要交付新能力 | `harness-feat` |
| 需要诊断并修复故障 | `harness-fix` |

若场景叠加，按顺序执行：

- 先缺失后交付：先 `harness-bootstrap`，再进入工作技能。
- 先漂移后交付：先 `harness-garden`，再 `harness-feat` 或 `harness-fix`。

---

## 最佳使用案例

建议把套件当作组合操作模型使用，而不是零散命令。以下场景通常收益最高。

| 使用案例 | 推荐顺序 | 适配原因 | 预期结果 |
| --- | --- | --- | --- |
| 历史仓库文档不一致，agent 缺乏稳定上下文 | `harness-bootstrap` -> `harness-garden` | 先补齐控制面，再清理陈旧假设 | 控制面稳定、AGENTS/docs 可可信、仓库可 preflight |
| 已接入 Harness 的仓库进入新一轮 feature 迭代 | `harness-garden` -> `harness-feat` | 先消除漂移，再进入功能交付，减少执行偏差 | feature 交付可预测，计划与验证证据完整 |
| 合并后 CI 失败且原因不明 | `harness-fix`（若文档明显陈旧可先 `harness-garden`） | fix 协议强制复现 -> 隔离 -> 最小修复 -> 回归保护 | 具备根因证据的修复计划、最小补丁、回归测试补齐 |
| 多模块 monorepo，agent 频繁交接 | `harness-bootstrap` -> 周期性 `harness-garden` -> 任务级 `harness-feat`/`harness-fix` | 统一术语 + 持续去漂移，保证跨会话连续性 | 交接成本低，模块间执行质量一致 |
| flaky 测试导致发布窗口不稳定 | 使用 `harness-fix` 的 flaky 诊断协议 | 统计复现与假设日志可避免“拍脑袋补丁” | 测试确定性恢复，或形成可升级的边界化诊断结果 |
| 新项目从 Day 1 计划大规模自治编码 | `harness-bootstrap` -> `harness-feat` -> 持续 `harness-garden` | 在代码规模上升前先建立治理，再持续维护真实性 | agent 规模化提速，同时保持可维护性 |

### 推荐落地节奏

多数团队可采用以下顺序获得最佳性价比：

1. 每个仓库基线阶段执行一次 `harness-bootstrap`。
2. 将 `harness-garden` 作为周期性养护任务。
3. 所有建设型任务走 `harness-feat`。
4. 所有修复型任务走 `harness-fix`。

这样可以在控制流程开销的同时，维持一致的执行标准。

---

## 推荐使用模板

### 模板 1：为新仓库或历史仓库建立控制面

```text
请为这个仓库建立 Harness Engineering 控制面。

上下文：
- 仓库类型：[frontend/backend/full-stack/monorepo/library]
- 当前状态：[新仓库 / 仅有部分文档 / 无 AGENTS.md]
- 约束条件：[安全/合规/性能/团队规范]

期望结果：
- Root + 必要 module AGENTS.md
- docs/ 控制面文件与 execution-plan 目录
- 生成的 manifest
- 可执行的 scripts/check_harness.py
```

适用：仓库没有可靠控制面，或已有控制面不完整。

### 模板 2：执行漂移审计并修复低风险问题

```text
请执行一次 Harness 漂移审计，并自动修复低风险问题。

重点范围：
- AGENTS.md 内容准确性
- docs 链接与路径有效性
- OBSERVABILITY 中命令新鲜度
- manifest 完整性

输出要求：
- 漂移问题摘要
- 自动修复清单
- 需要人工评审的高风险修复计划
```

适用：agent 输出出现“说明过期、链接失效、命令失效”等迹象。

### 模板 3：安全交付新功能

```text
请使用 Harness 工作流交付这个功能。

功能需求：
[粘贴用户需求]

要求：
- 先执行 preflight
- 先重写为任务简报 + sprint contract
- 在 docs/exec-plans/active 创建 execution plan
- 小步实现并逐步验证
- 归档计划并更新 docs/PLANS.md
```

适用：新功能开发、能力扩展、结构化重构。

### 模板 4：诊断并修复 Bug 或回归

```text
请按 Harness fix 协议诊断并修复这个问题。

问题描述：
[粘贴症状 / 报错 / 失败测试]

要求：
- 固化 known-broken baseline
- 生成结构化 bug brief
- 必须先复现再修复
- 用证据隔离 root cause
- 在 scope guard 下做最小修复
- 增加 regression protection 并归档 fix plan
```

适用：bug 修复、回归修复、故障响应、flaky 路径诊断。

### 模板 5：端到端迭代（建设 + 修复）

```text
请执行一次完整的 Harness 迭代周期。

阶段顺序：
1) 验证控制面健康状态
2) 执行计划内 feature 交付
3) 诊断并修复本轮引入或暴露的回归问题
4) 归档计划并输出结果总结

交付物：
- 已完成计划链接
- 验证证据摘要
- 剩余风险/tech-debt 记录
```

适用：团队希望在同一治理循环内完成“建设到稳定”的闭环。

---

## 质量模型

这套技能强调五条不变式：

1. 变更前先验证。
2. 实现前先计划。
3. 完成前先证据。
4. 交接前先归档。
5. 控制面始终与仓库现实同步。

这让团队可以在保持可维护性和运维信心的前提下，规模化使用自治编码 agent。
