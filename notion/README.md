# Notion Writing Artifacts

This directory contains Notion-native companion artifacts for the repository's Write Skills Suite. They are designed to be copied into Notion pages and then marked as Notion Agent Skills or Instructions.

These files are not Codex `SKILL.md` files. Notion Skills are ordinary Notion pages that you mark as Skills inside Notion.

## Layout

```text
notion/
├── README.md
├── instructions/
│   └── writing-agent.md
└── skills/
    ├── tech-planner.md
    ├── tech-writing.md
    └── tech-rewrite.md
```

## Import Flow

1. Create a Notion page such as `Refinex Writing Skills`.
2. Create one subpage per file in `notion/skills/`.
3. Paste the Markdown content into each page.
4. For each page, open `...` -> `Use with AI` -> `Use as AI Skill`.
5. Optional: paste `notion/instructions/writing-agent.md` into a separate page and set it with `...` -> `Use with AI` -> `Use as AI Instruction`.
6. Run a smoke test in Notion Agent:

```text
@Tech Planner - Notion Skill
Plan a 5-article series about Project Reactor for Java backend engineers.
Target version: 3.7.x.
Series goal: explain enough mechanism to make production debugging decisions.
```

## Artifact Intent

- `Tech Planner - Notion Skill`: produce a professional series outline and page backlog.
- `Tech Writing - Notion Skill`: produce one high-quality technical document from a blank page.
- `Tech Rewrite - Notion Skill`: rebuild a selected draft or source page into a strong document without inheriting weak structure.
- `Writing Agent Instructions`: keep persistent style and quality defaults active across Notion Agent chats.

Detailed setup and usage docs: `docs/reference/notion/README.md`.
