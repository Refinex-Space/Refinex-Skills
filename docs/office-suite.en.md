# Office Skills Suite

## Overview

The Office Skills suite groups four file-format-specific skills under a
single `office-*` namespace. The rename from bare extension names to
prefixed names is intentional: it makes prompt routing clearer, keeps
skill indexes easier to scan, and signals that these skills are meant to
work as one document-delivery family rather than as unrelated utilities.

## The Four Skills

### 1. `office-docx`

Use for Word document creation, editing, XML-level repair, tracked
changes handling, and `.doc` to `.docx` conversion workflows.

Best fit:

- formal reports, memos, letters, templates, and reviewable `.docx`
  deliverables
- tracked-change cleanup, comment workflows, and XML-level fixes
- Word output that must preserve pagination, headings, or layout rules

### 2. `office-pdf`

Use for PDF reading, extraction, generation, transformation, form
filling, OCR-adjacent workflows, and image conversion.

Best fit:

- extracting text or tables from PDFs
- filling fillable or non-fillable PDF forms
- splitting, merging, rotating, watermarking, encrypting, or generating
  PDFs

### 3. `office-pptx`

Use for slide decks, pitch decks, presentation templates, and
PowerPoint editing workflows.

Best fit:

- creating or editing `.pptx` deliverables
- reviewing slide structure and content extracted from presentations
- template-driven slide work that needs thumbnails, unpacking, and
  repacking

### 4. `office-xlsx`

Use for spreadsheet creation, cleaning, analysis, formatting, and
formula-safe workbook delivery.

Best fit:

- `.xlsx`, `.xlsm`, `.csv`, and `.tsv` deliverables where the result
  must remain spreadsheet-native
- workbook repair, recalculation, and template-preserving updates
- spreadsheet outputs that must keep formulas dynamic rather than
  hardcoded

## Classic Use Cases

### Word-first deliverable

```text
$office-docx
Task: turn these interview notes into a reviewable .docx report with headings, page numbers, and tracked comments
```

### PDF extraction or form workflow

```text
$office-pdf
Task: extract the tables from this quarterly PDF and fill the attached application form
```

### Slide deck revision

```text
$office-pptx
Task: update this investor deck, keep the template style, and export a clean .pptx handoff
```

### Spreadsheet-native output

```text
$office-xlsx
Task: clean this CSV, rebuild formulas, and deliver a final .xlsx workbook with no formula errors
```

## Recommended Usage

Choose the skill by final deliverable first:

- If the output is a Word document, use `office-docx`.
- If the output is a PDF or the source of truth is a PDF, use
  `office-pdf`.
- If the work centers on slides or a presentation file, use
  `office-pptx`.
- If the output must remain a spreadsheet workbook, use `office-xlsx`.

## Repository Layout

```text
skills/
├── office-docx/
├── office-pdf/
├── office-pptx/
└── office-xlsx/
```

Each skill keeps its own `SKILL.md` and local scripts or references
needed for that file format.
