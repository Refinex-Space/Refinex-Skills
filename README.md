中文版本: [README.zh.md](README.zh.md)

# Refinex-Skills

MIT-licensed personal skill suite for agent-first software development,
covering three complementary disciplines: Harness Engineering for
code-side rigor, Office Skills for document deliverables, and Write
Skills for documentation quality.

---

## Skill Suites

### Office Skills Suite

Four companion skills for Office-family deliverables. These skills were
renamed from bare file-extension names to `office-*` names so they read
as one suite and avoid namespace ambiguity in prompts and indexes:

- `office-docx`
- `office-pdf`
- `office-pptx`
- `office-xlsx`

1. `office-docx`
   Create, inspect, edit, and validate Word `.docx` documents.
2. `office-pdf`
   Read, generate, transform, extract from, and fill PDF documents.
3. `office-pptx`
   Build, review, and modify PowerPoint `.pptx` presentations.
4. `office-xlsx`
   Create, clean, analyze, and recalculate spreadsheet deliverables.

Migration note:
- Legacy skill names `docx`, `pdf`, `pptx`, and `xlsx` are now
  `office-docx`, `office-pdf`, `office-pptx`, and `office-xlsx`.

Source note:
- These four skills are derived from Anthropic's `anthropics/skills`
  repository and were originally provided there as document skills:
  https://github.com/anthropics/skills

Docs: [docs/office-suite.en.md](docs/office-suite.en.md)

---

### Write Skills Suite

Three complementary skills for technical documentation across planning,
blank-page authoring, and source-driven reconstruction:

- `tech-planner`
- `tech-writing`
- `tech-rewrite`

1. `tech-planner`
   Plan before prose. Positioned for research framing, outline design,
   series planning, phase naming, and prompt shaping when an idea needs
   structure before drafting starts.

2. `tech-writing`
   Write from scratch. Enforces a mandatory Pre-Writing Protocol before
   generating any prose — central argument, technical anchors, reader
   audit, scope boundaries, and narrative voice are all locked in before
   writing begins. Guards against anchor starvation: AI drift toward
   encyclopedic, opinion-free output.

   **Trigger phrases:** "write a blog post about X", "draft an architecture
   doc for Y", "compare X and Y", "write an ADR", "explain how X works
   in depth", "create API docs for Z".

3. `tech-rewrite`
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
│   ├── office-suite.en.md
│   ├── office-suite.zh.md
│   ├── write-suite.en.md
│   └── write-suite.zh.md
├── skills/
│   ├── harness-bootstrap/
│   ├── harness-garden/
│   ├── harness-feat/
│   ├── harness-fix/
│   ├── office-docx/
│   ├── office-pdf/
│   ├── office-pptx/
│   ├── office-xlsx/
│   ├── tech-planner/
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

**Office Skills Suite**
- English: [docs/office-suite.en.md](docs/office-suite.en.md)
- 中文: [docs/office-suite.zh.md](docs/office-suite.zh.md)

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

**Write Skills — recommended lifecycle:**

```text
tech-planner  -> turn a topic into a research / outline / series plan
tech-writing  -> write from a blank page with locked anchors
tech-rewrite  -> rebuild from notes, drafts, or legacy material
```

**Write Skills — skill selection quick reference:**

| Starting point | Document type | Skill to use |
|---|---|---|
| Topic or idea, but no structure yet | Research plan, outline, series map | `tech-planner` |
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
