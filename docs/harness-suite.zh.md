## Harness Engineering 套件

Harness Engineering 套件是一组面向 agent-first 软件开发的四技能控制面能力。它把随意编码转成可治理闭环：先做 preflight，再做版本化执行计划，再用验证证据收口，最后归档形成可交接资产。

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

## 四个技能

| Skill | 核心使命 | 典型触发 |
| --- | --- | --- |
| `harness-bootstrap` | 初始化或补齐仓库控制面 | 新仓库、历史仓库未接入 Harness |
| `harness-garden` | 审计并修复控制面漂移 | 文档陈旧、链接失效、命令失效 |
| `harness-feat` | 在控制面内交付新功能与结构化重构 | 新能力开发、计划内增强 |
| `harness-fix` | 在控制面内诊断并修复 bug/回归/故障 | 测试失败、线上问题、flaky 路径 |

---

## 工作流定位

把它看作同一个操作模型：

1. `harness-bootstrap` 先建立控制面基线。
2. `harness-garden` 持续保证控制面描述仍然真实。
3. `harness-feat` 在控制面内做增量建设。
4. `harness-fix` 在控制面内做证据驱动修复。

推荐生命周期：

```text
$harness-bootstrap  -> 建立控制面
$harness-garden     -> 保持控制面真实
$harness-feat       -> 安全交付新能力
$harness-fix        -> 基于根因证据修复故障
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

## 质量模型

这套技能强调五条不变式：

1. 变更前先验证。
2. 实现前先计划。
3. 完成前先证据。
4. 交接前先归档。
5. 控制面始终与仓库现实同步。

这让团队可以在保持可维护性和运维信心的前提下，规模化使用自治编码 agent。
