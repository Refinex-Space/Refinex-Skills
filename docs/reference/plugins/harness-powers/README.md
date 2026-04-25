# Harness Powers Plugin 用户手册

## 插件介绍

Harness Powers 是一个面向 Codex App 的 agent-first 软件开发插件，维护在本仓库的 `plugins/harness-powers/` 目录下。它把 Harness Engineering 的仓库控制面能力和 Superpowers 的优秀工作流思想融合为一套统一的 `harness-*` skill surface。

它的设计目标不是破坏性 fork Superpowers，也不是保留两套会漂移的入口，而是用 Harness 控制面承接这些能力：

- 用 `AGENTS.md`、`docs/PLANS.md`、`docs/exec-plans/`、验证脚本和证据日志维持仓库级事实来源。
- 用 `harness-using` 作为入口路由，先判断任务应该进入哪条流程。
- 用 `harness-brainstorm`、`harness-plan`、`harness-execute` 承接需求澄清、计划编写、计划执行。
- 用 `harness-feat` 和 `harness-fix` 分别承接 feature/refactor 与 bug/regression/incident 生命周期。
- 用 `harness-verify` 在任何“完成、修好、通过、ready”声明之前要求新鲜验证证据。

第一版公开 14 个 skills：

| Skill | 用途 |
| --- | --- |
| `harness-using` | 全局入口路由，判断该使用哪条 Harness Powers 流程 |
| `harness-brainstorm` | 澄清意图、比较方案、写入批准后的 design spec |
| `harness-plan` | 将批准后的 spec 转成 active execution plan |
| `harness-execute` | 按 active plan 执行、更新 checkbox 与 evidence |
| `harness-bootstrap` | 初始化或补齐仓库 Harness Engineering 控制面 |
| `harness-garden` | 审计并修复控制面漂移 |
| `harness-feat` | 管理 feature、enhancement、结构化 refactor 生命周期 |
| `harness-fix` | 管理 bug、regression、incident、flaky path 修复生命周期 |
| `harness-verify` | 完成声明前的证据门禁 |
| `harness-review` | 执行 review、请求 review、处理 review feedback |
| `harness-dispatch` | 在计划执行中调度并行 worker 或 subagent |
| `harness-worktree` | 为实现工作创建隔离 worktree 与 branch |
| `harness-finish` | 完成分支后的 merge、PR、keep、discard 收口流程 |
| `harness-frontend` | 前端界面任务的领域专长，叠加在 Harness 生命周期内 |

Harness Powers 不发布 `brainstorming`、`writing-plans`、`executing-plans`、`using-superpowers` 等 legacy Superpowers skill 名称，避免同一套方法在两个公开入口之间长期漂移。

## 插件安装

### 目录结构

插件源码位于：

```text
plugins/harness-powers/
```

关键文件：

```text
plugins/harness-powers/.codex-plugin/plugin.json
plugins/harness-powers/README.md
plugins/harness-powers/skills/
plugins/harness-powers/assets/harness-powers-small.svg
```

`plugin.json` 中的 `skills` 字段指向 `./skills/`，Codex App 读取该插件后会从这个目录发现 `harness-*` skills。

插件结构遵循 Codex plugin 官方规则：`.codex-plugin/plugin.json` 是必需入口；`skills/`、`assets/` 等目录保留在 plugin root；manifest 里的路径必须相对 plugin root，并以 `./` 开头。

官方参考：

- [Build plugins](https://developers.openai.com/codex/plugins/build)
- [Plugins](https://developers.openai.com/codex/plugins)

### 推荐安装方式：Repo Marketplace

Harness Powers 已经存放在当前仓库推荐的位置：

```text
/Users/refinex/develop/code/Refinex-Skills/plugins/harness-powers/
```

按官方文档，本地 plugin 需要通过 marketplace 暴露给 Codex。面向这个仓库使用时，创建或更新：

```text
/Users/refinex/develop/code/Refinex-Skills/.agents/plugins/marketplace.json
```

内容示例：

```json
{
  "name": "refinex-skills-local",
  "interface": {
    "displayName": "Refinex Skills Local"
  },
  "plugins": [
    {
      "name": "harness-powers",
      "source": {
        "source": "local",
        "path": "./plugins/harness-powers"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Coding"
    }
  ]
}
```

关键规则：

- `source.path` 必须以 `./` 开头。
- `source.path` 指向 plugin 目录，而不是 `.codex-plugin/plugin.json`。
- repo marketplace 的 `source.path` 按仓库根目录解析，所以这里使用 `./plugins/harness-powers`。
- 每个 plugin entry 都应包含 `policy.installation`、`policy.authentication` 和 `category`。

然后重启 Codex，打开 Plugin Directory，选择 `Refinex Skills Local` 这个 marketplace，找到 `Harness Powers` 并安装。安装后新开一个 thread，再开始使用插件。

### 可选安装方式：Personal Marketplace

如果希望在多个仓库中作为个人插件使用，可以把插件复制到个人插件目录：

```bash
mkdir -p ~/.codex/plugins
cp -R /Users/refinex/develop/code/Refinex-Skills/plugins/harness-powers ~/.codex/plugins/harness-powers
```

然后创建或更新：

```text
~/.agents/plugins/marketplace.json
```

内容示例：

```json
{
  "name": "refinex-personal",
  "interface": {
    "displayName": "Refinex Personal Plugins"
  },
  "plugins": [
    {
      "name": "harness-powers",
      "source": {
        "source": "local",
        "path": "./.codex/plugins/harness-powers"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Coding"
    }
  ]
}
```

重启 Codex 后，在 Plugin Directory 中选择 `Refinex Personal Plugins`，安装 `Harness Powers`。

### CLI 添加 Marketplace

如果希望让 Codex 记录并跟踪一个 marketplace source，而不是手动编辑配置，可以使用官方 CLI：

```bash
codex plugin marketplace add /Users/refinex/develop/code/Refinex-Skills
```

如果 marketplace 来自远端仓库，也可以使用 GitHub shorthand、Git URL、`--ref` 或 `--sparse`。更新或移除 marketplace：

```bash
codex plugin marketplace upgrade
codex plugin marketplace upgrade refinex-skills-local
codex plugin marketplace remove refinex-skills-local
```

### 安装后的实际加载位置

通过 marketplace 安装后，Codex 会把 plugin 安装到缓存目录，而不是直接从 marketplace entry 指向的源目录运行：

```text
~/.codex/plugins/cache/$MARKETPLACE_NAME/$PLUGIN_NAME/$VERSION/
```

对本地 plugin，`$VERSION` 通常是 `local`。因此修改源目录后，需要更新 marketplace 指向的 plugin 内容并重启 Codex，必要时重新安装或刷新 marketplace，才能让本地安装拾取新文件。

插件启用状态存放在：

```text
~/.codex/config.toml
```

如果只想临时关闭插件，可以在对应 plugin 条目下设置：

```toml
enabled = false
```

然后重启 Codex。

### 使用前 Smoke Test

安装并启用后，新开一个 thread，确认可用 skill 列表中出现 `harness-powers:*`，例如：

```text
harness-powers:harness-using
harness-powers:harness-brainstorm
harness-powers:harness-plan
harness-powers:harness-execute
```

然后发起一个最小验证 prompt：

```text
@Harness Powers 请用 harness-using 路由这个任务：检查当前仓库是否需要 Harness 控制面维护。
```

也可以直接点名 skill：

```text
$harness-using 检查当前仓库任务应该进入哪条 Harness Powers 流程。
```

如果 `@Harness Powers` 或 `$harness-using` 无法解析，优先检查：

- marketplace 文件是否位于 `$REPO_ROOT/.agents/plugins/marketplace.json` 或 `~/.agents/plugins/marketplace.json`。
- `source.path` 是否以 `./` 开头，并且指向 plugin 目录。
- 是否已经重启 Codex。
- Plugin Directory 中是否已经安装并启用 `Harness Powers`。
- `~/.codex/config.toml` 中对应 plugin 是否被设置为 `enabled = false`。

不要直接编辑已安装缓存中的 Superpowers：

```text
/Users/refinex/.codex/plugins/cache/openai-curated/superpowers
```

该目录只作为上游参考。Harness Powers 的维护入口始终是本仓库的 `plugins/harness-powers/`。

### 安装前检查

从仓库根目录运行：

```bash
python3 -m json.tool plugins/harness-powers/.codex-plugin/plugin.json >/dev/null
find plugins/harness-powers/skills -maxdepth 2 -name SKILL.md | sort
```

预期结果：

- `plugin.json` 能被正常解析。
- `skills/` 下能看到 14 个 `SKILL.md`。
- skill 名称均为 `harness-*`，没有 legacy Superpowers 公开入口。

### 插件验证

插件专项测试：

```bash
python3 -m unittest tests.content.test_harness_powers_plugin -v
```

仓库完整测试：

```bash
tests/run-all.sh
```

检查是否误用了 Superpowers 旧存储路径：

```bash
rg -n "docs/superpowers/(specs|plans)" plugins/harness-powers/skills && exit 1 || true
```

## 使用指南

### 默认入口

多数仓库任务从 `harness-using` 开始：

```text
请用 harness-using 路由这个任务。
```

`harness-using` 会先读取用户指令、仓库规则和任务上下文，再决定是否进入控制面初始化、漂移修复、需求澄清、计划、执行、feature、fix、review 或 verify 流程。

### 常见场景路由

| 场景 | 推荐 skill |
| --- | --- |
| 仓库还没有 Harness 控制面，或控制面缺文件 | `harness-bootstrap` |
| `AGENTS.md`、docs、计划索引、验证命令可能过期 | `harness-garden` |
| 需求还模糊，需要先讨论方案 | `harness-brainstorm` |
| 已有批准后的 design spec，需要生成执行计划 | `harness-plan` |
| 已有 active execution plan，需要按计划执行 | `harness-execute` |
| 新功能、增强、结构化重构 | `harness-feat` |
| bug、regression、incident、flaky test、CI 失败 | `harness-fix` |
| 前端页面、Dashboard、表单、交互界面 | `harness-frontend` 叠加在 `harness-feat` 或 `harness-fix` 内 |
| 当前 diff、PR、review feedback | `harness-review` |
| 多个独立任务可并行 | `harness-dispatch` |
| 需要隔离分支和 worktree | `harness-worktree` |
| 准备声明完成、修好、通过、ready | `harness-verify` |
| 验证通过后准备 merge、PR、保留或丢弃分支 | `harness-finish` |

### 推荐工作流

从想法到实现：

```text
harness-using
  -> harness-brainstorm
  -> harness-plan
  -> harness-worktree
  -> harness-execute
  -> harness-verify
  -> harness-finish
```

直接交付 feature：

```text
harness-using -> harness-feat -> harness-verify -> harness-finish
```

修复问题：

```text
harness-using -> harness-fix -> harness-verify -> harness-finish
```

控制面维护：

```text
harness-using -> harness-bootstrap -> harness-garden -> harness-verify
```

### 计划与文档位置

Harness Powers 使用 Harness Engineering 的计划目录，不使用 Superpowers 旧路径。

| 工件 | 路径 |
| --- | --- |
| Design spec | `docs/exec-plans/specs/YYYY-MM-DD-<topic>-design.md` |
| Active execution plan | `docs/exec-plans/active/YYYY-MM-DD-<topic>.md` |
| Completed execution plan | `docs/exec-plans/completed/YYYY-MM-DD-<topic>.md` |
| Plan index | `docs/PLANS.md` |
| Repository instructions | `AGENTS.md` 与局部 `AGENTS.md` |
| Verification evidence | active/completed plan、`docs/OBSERVABILITY.md` 或任务约定的位置 |

禁止在新流程中使用：

```text
docs/superpowers/specs/
docs/superpowers/plans/
```

### Prompt 示例

需求澄清：

```text
用 harness-brainstorm 先把这个插件能力设计清楚，等我确认 spec 后再进入计划。
```

生成计划：

```text
根据 docs/exec-plans/specs/2026-04-25-example-design.md，用 harness-plan 生成 active execution plan。
```

执行计划：

```text
用 harness-execute 执行 docs/exec-plans/active/2026-04-25-example.md，按步骤更新 checkbox 和 evidence。
```

修复失败：

```text
用 harness-fix 排查这个测试失败。先给出复现证据，再判断 root cause。
```

完成前验证：

```text
用 harness-verify 确认现在是否可以声明完成，列出实际运行过的验证命令和结果。
```

分支收口：

```text
用 harness-finish 做最后收口。验证通过后给我 merge、PR、keep branch、discard work 四个选项。
```

### 使用纪律

- 先路由，再实现：仓库任务优先让 `harness-using` 判断入口。
- 先证据，再结论：没有当前会话的新鲜验证结果，不声明完成、修好或通过。
- 先复现，再修复：bug/fix 类任务必须有 reproduction evidence。
- 先 spec，再 plan：模糊需求不能直接跳到 execution plan。
- 领域 skill 不抢生命周期：例如 `harness-frontend` 负责界面质量，但仓库级 feature/fix 生命周期仍由 `harness-feat` 或 `harness-fix` 持有。

## 维护指南

维护 Harness Powers 时遵循这些约束：

- 只在 `plugins/harness-powers/` 中修改插件内容。
- 不直接修改 `/Users/refinex/.codex/plugins/cache/openai-curated/superpowers`。
- 不重新发布 legacy Superpowers skill 名称作为兼容 alias。
- 新增 skill 时保持 `harness-*` 命名，并补充插件测试。
- 大段机制说明优先放进 skill `references/`，避免 `SKILL.md` 变成不可快速加载的长手册。
- 每次修改后至少运行插件专项测试；涉及全仓规则时运行 `tests/run-all.sh`。
