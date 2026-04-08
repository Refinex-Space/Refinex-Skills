# ${title}

## 元信息

- **状态**: 🟡 Active
- **负责人**: ${owner}
- **创建日期**: ${date}
- **问题级别**: ${severity}
- **目标**: ${goal}
- **影响范围**: ${impact}
- **回滚方案**: ${rollback}
- **关联入口**: `docs/PLANS.md`
- **计划路径**: `${plan_path}`

## Harness 预检

- **仓库自检状态**: ${HARNESS_CHECK_STATUS}
- **Harness 关键观测面**:
${HARNESS_SURFACES}

## 症状与背景

- **Expected**: ${expected}
- **Observed**: ${observed}
- **Impact**: ${impact}
- **Evidence**:
${evidence}

## 优化后的问题定义

- **Reproduction**:
${reproduction}
- **Likely surfaces**:
${likely_surfaces}
- **Hypotheses**:
${hypotheses}
- **Validation**:
${validation}
- **Docs to sync**:
${docs_sync}

## 调查与修复切片

### Slice 1 — 复现或界定失败

- [ ] 复现 / 证据收集
- [ ] 记录结论

### Slice 2 — 根因隔离

- [ ] 定位
- [ ] 记录结论

### Slice 3 — 修复、回归保护与验证

- [ ] 修复
- [ ] 回归保护
- [ ] 验证
- [ ] 归档 active 计划并刷新 Harness 生成事实

## 风险与回滚

${risk_summary}
- ${rollback}

## 决策记录

| 日期 | 决策 | 原因 |
| ---- | ---- | ---- |

## 验证记录

- ${initial_validation_note}

## 完成归档说明

- 在归档前补充完成日期、摘要、周期和关键经验
- 归档后确认计划已进入 `docs/exec-plans/completed/`
- 若仓库存在 `docs/generated/harness-manifest.md`，归档后确认其已刷新
