# Fix Execution Plan Template

Use this template when creating a new file under
`docs/exec-plans/active/` for debugging or repair work. Match the
repository's documentation language when writing the actual file.

Name the file with a date-prefixed kebab-case slug, for example
`2026-04-05-provider-timeout-regression.md`. Do not create bare-slug
filenames.

When deterministic initialization is useful, prefer
`scripts/init_exec_plan.py` and then refine the generated file instead
of hand-writing the whole document from scratch.

Here `scripts/init_exec_plan.py` refers to the bundled script inside
this Skill, not to a script that must exist inside the target
repository.

```markdown
# <Bug / Regression / Incident Name>

## 元信息
- **状态**: 🟡 Active
- **负责人**: Codex / Claude Agent
- **问题级别**: <severity>
- **目标**: <restore which behavior>
- **影响范围**: <who/what is affected>
- **回滚方案**: <safe rollback or mitigation path>
- **关联入口**: `docs/PLANS.md`

## Harness 预检
- **仓库自检状态**:
- **Harness 关键观测面**:

## 症状与背景
- **Expected**:
- **Observed**:
- **Impact**:
- **Evidence**:

## 优化后的问题定义
- **Reproduction**:
- **Likely surfaces**:
- **Hypotheses**:
- **Validation**:
- **Docs to sync**:

## 调查与修复切片
### Slice 1 — Reproduce or bound
- [ ] 复现 / 证据收集
- [ ] 记录结论

### Slice 2 — Root cause isolation
- [ ] 定位
- [ ] 记录结论

### Slice 3 — Repair and regression protection
- [ ] 修复
- [ ] 回归保护
- [ ] 验证

## 风险与回滚
- <main risks>
- <rollback notes>

## 决策记录
| 日期 | 决策 | 原因 |
| ---- | ---- | ---- |

## 验证记录
- <command / result / manual evidence>

## 完成归档说明
- 在归档前补充完成日期、摘要、周期和关键经验
```

## Writing Rules

- Keep evidence ahead of opinion.
- Record confidence levels when reproduction is incomplete.
- Note mitigations separately from real fixes.
- Update the file during investigation, not just after the code change.
- Keep harness preflight and runtime surfaces visible when they matter to the issue.
