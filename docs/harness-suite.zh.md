# Harness Skills 套件说明

## 概述

`Refinex-Skills` 是一组围绕 Harness Engineering 构建的高约束个人
Skill 套件，目标不是生成 demo 代码，而是让智能体在真实工程仓库中
稳定、可审计、可继续接手地工作。

这套技能的核心思想是：

- 把仓库当作唯一可信知识源
- 把连续性外化为 `AGENTS.md`、`docs/`、执行计划与生成事实
- 把运行态、验证与漂移治理纳入控制面
- 把“任务执行”与“控制面维护”解耦但联通

## 四个 Skill 的定位

### 1. `harness-bootstrap`

用于新仓库、旧仓库初次落地或补齐 Harness 控制面。

它负责：

- 初始化根与局部 `AGENTS.md`
- 初始化 `docs/PLANS.md`、`docs/OBSERVABILITY.md`
- 初始化 `docs/exec-plans/tech-debt-tracker.md`
- 生成 `docs/generated/harness-manifest.md`
- 安装 repo-local `scripts/check_harness.py`

适合场景：

- 新项目首次接入 agent-first 工程体系
- 老项目文档结构零散，需要建立控制面基线

调用方式：

```text
$harness-bootstrap
任务：为这个仓库建立 Harness Engineering 控制面
```

### 2. `harness-garden`

用于已存在 Harness 基线的仓库做持续 drift audit / repair。

它负责：

- 审计根路由与局部边界是否漂移
- 检查 managed docs / manifest / repo check 是否过期
- 自动修复低风险问题
- 对高风险语义漂移生成 remediation plan

适合场景：

- 根 `AGENTS.md`、`PLANS.md`、manifest 长期演化后发生漂移
- 需要做 doc gardening / harness health check

调用方式：

```text
$harness-garden
任务：检查并修复这个仓库的 Harness 漂移
```

### 3. `harness-feat`

用于新增功能、能力建设、结构化重构。

它负责：

- 重写原始任务 Prompt
- 执行 harness preflight
- 创建或更新活跃执行计划
- 小步实施并持续记录验证证据
- 用脚本同步 `docs/PLANS.md`
- 完成后确定性归档计划

适合场景：

- 新功能开发
- 子系统能力扩展
- 在明确边界内做结构化重构

调用方式：

```text
$harness-feat
任务：实现 provider 健康检查视图
```

### 4. `harness-fix`

用于 bug、回归、故障、flaky 路径、 incident repair。

它负责：

- 重写 bug brief
- harness preflight
- 复现或界定失败
- 创建或更新 fix plan
- 根因隔离
- 最小修复与回归保护
- 用脚本同步 `docs/PLANS.md`
- 完成后确定性归档计划

适合场景：

- 用户报告功能损坏
- 某条路径出现 crash / timeout / regression
- 需要 evidence-driven debugging

调用方式：

```text
$harness-fix
任务：修复 provider 切换后请求一直 loading 的问题
```

## 推荐工作流

### 新仓库

1. 先使用 `harness-bootstrap`
2. 后续定期使用 `harness-garden`
3. 新功能使用 `harness-feat`
4. 故障修复使用 `harness-fix`

### 老仓库

1. 如果还没有完整控制面，先 `harness-bootstrap`
2. 如果已有控制面但怀疑漂移，先 `harness-garden`
3. 再根据任务类型进入 `harness-feat` 或 `harness-fix`

## 套件优势

- 风格统一：四个 Skill 使用同一套 Harness 语言和工件生命周期
- 可机械验证：manifest、repo check、fixture/golden 回归都能复用
- 保守安全：不会盲目重写 unmanaged 战略文档
- 可继续接手：所有任务都以活跃计划和归档计划形成连续性
- 工程导向：优先解决真实项目中的稳定性、可验证性、可维护性问题

## 目录结构

```text
skills/
├── harness-bootstrap/
├── harness-garden/
├── harness-feat/
└── harness-fix/
```

每个 Skill 都包含：

- `SKILL.md`
- `agents/openai.yaml`
- `references/`
- `assets/`
- `scripts/`

其中部分 Skill 还包含固定 `fixture + golden` 回归测试。

## 许可

本仓库采用 MIT License 开源。
