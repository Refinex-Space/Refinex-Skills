English Version: [README.md](README.md)

# Refinex-Skills

基于 MIT License 开源的个人高质量 Skill 套件，面向
Harness Engineering 风格的 agent-first 软件开发。

本仓库当前包含四个高约束、高工程规格的 Codex / Agent Skill：

- `harness-bootstrap`
- `harness-garden`
- `harness-feat`
- `harness-fix`

这四个 Skill 被设计为一整套互相配合的控制面：

1. `harness-bootstrap`
   为仓库初始化或补齐 Harness Engineering 基线。
2. `harness-garden`
   审计并修复已存在仓库中的 Harness 漂移。
3. `harness-feat`
   通过确定性的计划生命周期执行新功能与结构化重构任务。
4. `harness-fix`
   通过确定性的计划生命周期执行调试、修复与回归治理任务。

## 仓库结构

```text
Refinex-Skills/
├── docs/
│   ├── harness-suite.en.md
│   └── harness-suite.zh.md
├── skills/
│   ├── harness-bootstrap/
│   ├── harness-garden/
│   ├── harness-feat/
│   └── harness-fix/
├── .gitignore
├── LICENSE
├── README.md
└── README.zh.md
```

## 说明文档

- English: [docs/harness-suite.en.md](docs/harness-suite.en.md)
- 中文: [docs/harness-suite.zh.md](docs/harness-suite.zh.md)

## 典型使用方式

在一个已经接入或准备接入 Harness 的仓库里，推荐流程如下：

```text
$harness-bootstrap  -> 首次安装 / 补齐控制面
$harness-garden     -> 漂移审计 / 修复
$harness-feat       -> 新功能 / 重构任务
$harness-fix        -> Bug / 回归 / 故障修复
```

## 许可

MIT。详见 [LICENSE](LICENSE)。
