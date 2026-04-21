# Refinex-Skills

MIT-licensed personal skill suite for agent-first software development and technical delivery. The repository currently includes three complementary suites, one shared diagram skill layer, plus internal verification assets:

- Harness Engineering Suite: control plane initialization, drift maintenance, feature delivery, and bug remediation
- Office Skills Suite: high-quality document deliverables across DOCX, PDF, PPTX, and XLSX
- Write Skills Suite: technical planning, blank-page writing, source-driven rewrite, plus a shared Mermaid diagram standard

---

## Skill Suites

### Harness Engineering Suite

The Harness family now consists of four core workflow skills plus two cross-cutting skills:

- `harness-bootstrap`: bootstrap or complete repository control plane
- `harness-garden`: audit and repair control plane drift
- `harness-feat`: deliver new features and structured refactors with execution plans
- `harness-fix`: diagnose and repair bugs/regressions with root-cause evidence
- `harness-using`: route repository work into the correct Harness workflow
- `harness-verify`: require fresh evidence before completion claims

The suite also embeds a behavioral discipline layer: explicit assumption management, simplicity checks, surgical diffs, and proof-matched verification. These rules are absorbed into the Harness workflows rather than shipped as a separate parallel skill.

Docs: [docs/harness-suite.en.md](docs/harness-suite.en.md)

### Office Skills Suite

Four office-oriented skills:

- `office-docx`
- `office-pdf`
- `office-pptx`
- `office-xlsx`

Docs: [docs/office-suite.en.md](docs/office-suite.en.md)

### Write Skills Suite

Three writing-focused skills plus one shared diagram skill:

- `mermaid-diagrams`
- `tech-planner`
- `tech-writing`
- `tech-rewrite`

The `tech-*` skills decide whether a document needs a diagram and what question it should answer; `mermaid-diagrams` turns that visual plan into syntax-correct, Markdown-portable, restrained Mermaid.

Docs: [docs/write-suite.en.md](docs/write-suite.en.md)

---

## Recommended Harness Flow

```text
$harness-using      -> route the task
$harness-bootstrap  -> establish control plane when missing
$harness-garden     -> restore truth when drift is suspected
$harness-feat       -> build new capabilities safely
$harness-fix        -> repair failures with evidence-driven diagnosis
$harness-verify     -> prove completion before claiming success
```

---

## Repository Layout

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
│   ├── mermaid-diagrams/
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

## Documentation Index

Harness Engineering:
- English: [docs/harness-suite.en.md](docs/harness-suite.en.md)
- 中文: [docs/harness-suite.zh.md](docs/harness-suite.zh.md)

Office Skills:
- English: [docs/office-suite.en.md](docs/office-suite.en.md)
- 中文: [docs/office-suite.zh.md](docs/office-suite.zh.md)

Write Skills:
- English: [docs/write-suite.en.md](docs/write-suite.en.md)
- 中文: [docs/write-suite.zh.md](docs/write-suite.zh.md)

## Validation

The repository now includes:

- static/content tests for Harness skill rules
- validator integration fixtures for `check_harness.py`
- opt-in live Codex trigger tests

Run the full local test entrypoint with:

```bash
bash tests/run-all.sh
```

---

## License

MIT. See [LICENSE](LICENSE).
