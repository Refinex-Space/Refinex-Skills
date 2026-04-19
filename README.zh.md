# Refinex-Skills

基于 MIT License 的个人技能仓库，面向 agent-first 软件开发与技术交付。
当前包含三组互补能力，以及一组内部验证资产：

- Harness Engineering 套件：控制面初始化、漂移养护、功能交付、故障修复
- Office Skills 套件：DOCX、PDF、PPTX、XLSX 文档交付
- Write Skills 套件：技术规划、从零写作、基于材料重写

---

## Skill 套件

### Harness Engineering 套件

Harness 家族现由四个核心工作流技能与两个横切技能构成：

- `harness-bootstrap`：初始化或补齐仓库控制面
- `harness-garden`：审计并修复控制面漂移
- `harness-feat`：在执行计划下交付新功能与结构化重构
- `harness-fix`：基于根因证据修复 bug、回归与故障
- `harness-using`：为仓库任务路由到正确的 Harness 工作流
- `harness-verify`：在宣称完成前强制要求新鲜验证证据

套件还内嵌了一层行为纪律：显式管理假设、在设计阶段做简化检查、保持手术式 diff、以及让验证证据与结论严格同域。这些约束被吸收到 Harness 流程内部，而不是再额外发布一套并行 skill。

文档：[docs/harness-suite.zh.md](docs/harness-suite.zh.md)

### Office Skills 套件

四个 Office 交付技能：

- `office-docx`
- `office-pdf`
- `office-pptx`
- `office-xlsx`

文档：[docs/office-suite.zh.md](docs/office-suite.zh.md)

### Write Skills 套件

三个技术写作技能：

- `tech-planner`
- `tech-writing`
- `tech-rewrite`

文档：[docs/write-suite.zh.md](docs/write-suite.zh.md)

---

## 推荐 Harness 流程

```text
$harness-using      -> 先路由任务
$harness-bootstrap  -> 缺控制面时先建基线
$harness-garden     -> 怀疑漂移时先恢复真实性
$harness-feat       -> 安全交付新能力
$harness-fix        -> 证据驱动修复故障
$harness-verify     -> 宣称成功前做最终验证
```

---

## 仓库结构

```text
Refinex-Skills/
├── docs/
│   ├── harness-suite.en.md
│   ├── harness-suite.zh.md
│   ├── office-suite.en.md
│   ├── office-suite.zh.md
│   ├── write-suite.en.md
│   └── write-suite.zh.md
├── skills/
│   ├── harness-bootstrap/
│   ├── harness-garden/
│   ├── harness-feat/
│   ├── harness-fix/
│   ├── harness-using/
│   ├── harness-verify/
│   ├── office-docx/
│   ├── office-pdf/
│   ├── office-pptx/
│   ├── office-xlsx/
│   ├── tech-planner/
│   ├── tech-writing/
│   └── tech-rewrite/
├── .codex/
│   └── INSTALL.md
├── tests/
├── LICENSE
├── README.md
└── README.zh.md
```

---

## 文档索引

Harness Engineering：
- English: [docs/harness-suite.en.md](docs/harness-suite.en.md)
- 中文: [docs/harness-suite.zh.md](docs/harness-suite.zh.md)

Office Skills：
- English: [docs/office-suite.en.md](docs/office-suite.en.md)
- 中文: [docs/office-suite.zh.md](docs/office-suite.zh.md)

Write Skills：
- English: [docs/write-suite.en.md](docs/write-suite.en.md)
- 中文: [docs/write-suite.zh.md](docs/write-suite.zh.md)

## 验证

仓库现在包含：

- Harness skill 规则的静态/内容测试
- `check_harness.py` 的 validator fixture 集成测试
- 可选启用的 Codex live trigger 测试

本地完整测试入口：

```bash
bash tests/run-all.sh
```

---

## 许可证

MIT。详见 [LICENSE](LICENSE)。
