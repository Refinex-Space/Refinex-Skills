<!-- HARNESS:MANAGED FILE -->
# Development Plans

> 智能体启动任务前先阅读本文件，确认当前活跃计划与优先级。

## 当前状态

- **活跃计划目录**: `docs/exec-plans/active/`
- **Harness 状态**: 通过 `scripts/check_harness.py` 持续维护
- **结构性技术债**: `docs/exec-plans/tech-debt-tracker.md`

## 活跃计划入口

${ACTIVE_PLANS}

## 规则

1. 新任务需要创建或复用 `docs/exec-plans/active/` 中的活跃计划
2. 完成后归档到 `docs/exec-plans/completed/`
3. 结构性技术债与延后治理写入 `docs/exec-plans/tech-debt-tracker.md`
4. `PLANS.md` 保持短小，只做高层入口，不复制执行细节
