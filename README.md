中文版本: [README.zh.md](README.zh.md)

# Refinex-Skills

MIT-licensed personal skill suite for Harness Engineering oriented
agent-first software development.

This repository packages four high-discipline Codex/agent skills:

- `harness-bootstrap`
- `harness-garden`
- `harness-feat`
- `harness-fix`

These skills are designed to work together as one control-plane stack:

1. `harness-bootstrap`
   Initialize or complete a repository's Harness Engineering baseline.
2. `harness-garden`
   Audit and repair Harness drift in an existing repository.
3. `harness-feat`
   Execute new feature work through deterministic plan lifecycle.
4. `harness-fix`
   Execute debugging and repair work through deterministic plan lifecycle.

## Repository Layout

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

## Docs

- English: [docs/harness-suite.en.md](docs/harness-suite.en.md)
- 中文: [docs/harness-suite.zh.md](docs/harness-suite.zh.md)

## Intended Usage

Typical flow inside a Harness-enabled repository:

```text
$harness-bootstrap  -> first-time installation / completion
$harness-garden     -> drift audit / repair
$harness-feat       -> new feature / refactor work
$harness-fix        -> bug / regression / incident repair
```

## License

MIT. See [LICENSE](LICENSE).
