# Feature Execution Plan Template

Use this template when creating a new file under
`docs/exec-plans/active/` for net-new work. Match the repository's
documentation language when writing the actual file.

Name the file with a date-prefixed kebab-case slug, for example
`2026-04-05-provider-context-window-config.md`. Do not create bare-slug
filenames.

When deterministic initialization is useful, prefer
`scripts/init_exec_plan.py` and then refine the generated file instead
of hand-writing the whole document from scratch.

Here `scripts/init_exec_plan.py` refers to the bundled script inside
this Skill, not to a script that must exist inside the target
repository.

```markdown
# <Feature / Task Name>

## 元信息
- **状态**: 🟡 Active
- **负责人**: Codex / Claude Agent
- **目标**: <one-sentence outcome>
- **范围**: <included work>
- **非目标**: <excluded work>
- **回滚方案**: <safe rollback path>
- **关联入口**: `docs/PLANS.md`

## Harness 预检
- **仓库自检状态**:
- **Harness 关键观测面**:

## 背景
<Why this task exists now and what problem it solves>

## 优化后的任务定义
- **Outcome**:
- **Constraints**:
- **Validation**:
- **Docs to sync**:
- **Open assumptions**:

## 渐进执行切片
### Slice 1 — <smallest useful slice>
- [ ] 实现
- [ ] 验证

### Slice 2 — <next slice>
- [ ] 实现
- [ ] 验证

## 风险与回滚
- <main technical or product risks>
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

- Keep the plan operational, not ceremonial.
- Record only facts that help the next agent continue correctly.
- Prefer short slices over large milestone dumps.
- Update the file during the work, not only at the end.
- Keep harness preflight and runtime surfaces visible when they matter to the task.
