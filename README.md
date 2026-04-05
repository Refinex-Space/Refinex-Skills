中文版本: [README.zh.md](README.zh.md)

# Refinex-Skills

MIT-licensed personal skill suite for agent-first software development,
covering two complementary engineering disciplines: Harness Engineering
for code-side rigor and Write Skills for documentation quality.

---

## Skill Suites

### Harness Engineering Suite

Four high-discipline skills for structured, agent-first software development:

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

Docs: [docs/harness-suite.en.md](docs/harness-suite.en.md)

---

### Write Skills Suite

Two companion skills for producing consistent, high-quality technical
documentation regardless of the starting point:

- `tech-writing`
- `tech-rewrite`

1. `tech-writing`
   Write from scratch. Enforces a mandatory Pre-Writing Protocol before
   generating any prose — central argument, technical anchors, reader
   audit, scope boundaries, and narrative voice are all locked in before
   writing begins. Guards against anchor starvation: AI drift toward
   encyclopedic, opinion-free output.

   **Trigger phrases:** "write a blog post about X", "draft an architecture
   doc for Y", "compare X and Y", "write an ADR", "explain how X works
   in depth", "create API docs for Z".

2. `tech-rewrite`
   Reconstruct from existing material of any quality — internal notes,
   meeting summaries, AI-generated drafts, legacy wikis, code comments.
   Enforces strict quarantine between extraction and writing phases.
   Source material is never used as a template; facts are extracted into
   a structured Fact Register before a single sentence of output is written.
   Guards against style contamination: structural mirroring, void
   inheritance, vagueness laundering, tone osmosis, rationale elision,
   false completeness, and scope inflation.

   **Trigger phrases:** "rewrite this doc", "clean up my notes", "this
   draft is bad, fix it", "turn this into a proper article", "based on
   this material, write a doc about X", "improve this documentation".

Docs: [docs/write-suite.en.md](docs/write-suite.en.md)

---

## Repository Layout

```text
Refinex-Skills/
├── docs/
│   ├── harness-suite.en.md
│   ├── harness-suite.zh.md
│   ├── write-suite.en.md
│   └── write-suite.zh.md
├── skills/
│   ├── harness-bootstrap/
│   ├── harness-garden/
│   ├── harness-feat/
│   ├── harness-fix/
│   ├── tech-writing/
│   └── tech-rewrite/
├── .gitignore
├── LICENSE
├── README.md
└── README.zh.md
```

## Docs

**Harness Engineering Suite**
- English: [docs/harness-suite.en.md](docs/harness-suite.en.md)
- 中文: [docs/harness-suite.zh.md](docs/harness-suite.zh.md)

**Write Skills Suite**
- English: [docs/write-suite.en.md](docs/write-suite.en.md)
- 中文: [docs/write-suite.zh.md](docs/write-suite.zh.md)

## Intended Usage

**Harness Engineering — typical flow inside a Harness-enabled repository:**

```text
$harness-bootstrap  -> first-time installation / completion
$harness-garden     -> drift audit / repair
$harness-feat       -> new feature / refactor work
$harness-fix        -> bug / regression / incident repair
```

**Write Skills — skill selection quick reference:**

| Starting point | Document type | Skill to use |
|---|---|---|
| Topic + opinion, no source material | Blog post, deep-dive | `tech-writing` |
| Architecture decision to record | ADR | `tech-writing` |
| New module to design and document | Module design doc | `tech-writing` |
| Technology selection to justify | Comparison guide | `tech-writing` |
| Existing doc with quality problems | Any type | `tech-rewrite` |
| AI-generated draft that needs improvement | Any type | `tech-rewrite` |
| Meeting notes / internal wiki | Blog post, design doc | `tech-rewrite` |
| Code comments + scattered notes | Module doc, ADR | `tech-rewrite` |

See [docs/write-suite.en.md](docs/write-suite.en.md) for full usage templates
(blog post, ADR, module design, comparison guide, rewrite, and notes-to-article).

## License

MIT. See [LICENSE](LICENSE).