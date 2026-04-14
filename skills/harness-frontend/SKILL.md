---
name: harness-frontend
description: >-
  Use this skill for tasks that produce user-facing interfaces: landing pages, marketing sites, dashboards, admin tools, web apps, prototypes, components, forms, or any HTML/CSS/JSX/Vue output users will see. Trigger even if the user doesn’t say “design” (e.g. “build a page”, “make a dashboard”, “create a form”, “scaffold UI”, “polish this”, “convert Figma”, or UI screenshots). Applies to both new builds and redesigns. In repository work, this is a frontend specialization layered under `harness-feat` or `harness-fix`, not a replacement for lifecycle ownership. The workflow is opinionated and taste-driven: identify surface type, run quick structured option selection with the user, define visual/content/interaction direction, apply the correct rule set (landing/app/dashboard/game), generate production-ready code, and validate both design quality and repo delivery readiness. Goal: avoid generic AI UI patterns and produce deliberate, high-quality, ship-ready interfaces.
---

# harness-frontend

A taste-driven, brainstorm-first workflow for shipping production-grade frontend work that does not look like every other AI-generated page.

This is a **domain skill**, not a primary lifecycle owner. In repository work, `harness-using` routes first, `harness-feat` or `harness-fix` keeps control of preflight/plan/scope, `harness-frontend` owns the frontend-specific discovery/thesis/build decisions, and `harness-verify` closes the success claim with fresh evidence.

**Announce at start:** `I'm using harness-frontend to shape the frontend direction and implementation details for this task.`

## Workflow ownership

Use this skill in one of two modes:

1. **Repository mode** — the task changes a real codebase. `harness-feat` or `harness-fix` must already own the workflow. This skill may not bypass preflight, planning, or fresh verification evidence.
2. **Artifact mode** — the user wants a one-off frontend artifact, prototype, or design exploration outside a harnessed repo. In this case, this skill can run end-to-end on its own.

If the task is repository work and no process skill owns it yet, stop and route through `harness-using` first. Domain quality is not a substitute for workflow discipline.

## Why this skill exists

Underspecified frontend prompts make models fall back to the most frequent patterns in their training data: card grids, Inter font, white-with-purple-gradient hero, pill clusters, dashboard mosaics, Lorem ipsum, three feature columns, sign-up CTA at the bottom. The output is plausible but generic, and the user can feel it. This skill exists to interrupt that fallback with a short, opinionated workflow that forces five things to happen _before_ the first line of code is written:

1. The surface type is correctly diagnosed (a landing page, an internal dashboard, and a game UI need different rule packs — applying landing-page rules to a dashboard ruins the dashboard).
2. The user is briefly consulted with concrete option menus, not open-ended questions, so taste decisions get made deliberately rather than by default.
3. A short, written **Working Model** locks in mood, content sequence, and interaction ideas.
4. The implementation follows the rule pack appropriate for the surface type.
5. The result is checked against a litmus list before being shipped.

The "elicitation with options" step is the part most other frontend skills skip, and it is the single biggest lever for quality. People rarely volunteer their preferences upfront, but they reliably _recognise_ them when shown three good options.

## The five-phase workflow

Every invocation of this skill walks through these five phases in order. Do not skip phases. Do not collapse phases into one big prose response. The phases are explicit because each one fights a specific failure mode.

```
Phase 1 — Discover    : classify the surface type and capture hard constraints
Phase 2 — Elicit      : present 2–4 option menus with opinionated defaults
Phase 3 — Thesis      : write the Working Model (visual / content / interaction)
Phase 4 — Build       : implement using the rule pack for this surface type
Phase 5 — Verify      : run design litmus checks, then hand off to the delivery gate
```

A short response is fine. A landing page for "a coffee shop in Brooklyn" still goes through all five phases — they just take two sentences each. Skipping phases is what produces slop.

---

## Phase 1 — Discover

Before anything else, classify the surface type and capture the hard constraints. Output one short paragraph with these fields filled in. If a field is missing from the user's prompt, infer it and mark the inference with _(assumed)_ so the user can correct.

- **Surface type** — one of: _landing / marketing site / portfolio / dashboard / admin tool / web app / settings or form / onboarding / single-file artifact / game UI_. The rule pack used in Phase 4 depends on this.
- **Audience** — who actually looks at this (consumers, internal operators, developers, investors, kids, etc.).
- **Brand or product** — the name that must dominate visually. If the user has not given one, ask for it inline rather than inventing one — invented names create downstream rework.
- **Tech constraints** — framework (if any), single-file artifact vs full project, dark/light requirement, accessibility floor, target device.
- **Existing system** — if there is an existing design system, brand book, or codebase, that overrides everything in this skill. Read it first and conform.

If the user's request is primarily a document, email, slide, poster, or another non-frontend artifact, do not force it into this taxonomy. Route to the appropriate writing or document skill instead.

### Why this phase is non-negotiable

Skipping discovery is the most common failure mode. Without the surface type, the model defaults to "marketing landing page" rules even for an internal dashboard, and produces a hero section on a settings screen. The surface type is the single most important fact about a frontend task.

---

## Phase 2 — Elicit (the brainstorming round)

This is the part that distinguishes this skill from instruction-only frontend skills. Present the user with **2 to 4 short option menus**, each with **3–5 mutually exclusive choices**, and **always pre-select the default you actually recommend**. Never ask open-ended questions like "what mood do you want?" — people freeze. Always give them tappable choices with a clear default.

Use the environment's structured choice-input tool when it is available. When it is not, present the menus inline as numbered lists so the user can reply with the numbers.

### Which menus to ask

Pick from the menu library below based on the surface type and on what is genuinely undecided. Do not ask about things the user already specified. **Cap the round at 4 questions** — fewer is better. The point is to make taste decisions visible, not to interview the user.

Always include menu **A (Tone)** and menu **B (Density)**. The other menus are situational.

#### Menu A — Tone (always ask)

- _Editorial & restrained_ — generous whitespace, serif or refined sans, magazine cadence (recommended default for brand pages, portfolios, premium products)
- _Brutalist & raw_ — heavy type, hard edges, exposed grid, monochrome with one violent accent
- _Soft & organic_ — warm palette, rounded forms, hand-feel, gentle motion
- _Technical & utilitarian_ — Linear/Vercel cadence, monospaced accents, tight grid, dense info (recommended default for dashboards and dev tools)
- _Maximalist & playful_ — saturated color, layered type, deliberate visual chaos
- _Retro-futurist_ — Y2K, vaporwave, late-90s OS, or 80s computing references — pick one era and commit

#### Menu B — Density (always ask)

- _Generous_ — large type, lots of whitespace, slow scroll
- _Balanced_ — most pages live here
- _Dense_ — Bloomberg / Linear / Notion levels of information per pixel

#### Menu C — Motion appetite

- _None_ — static page, no animation at all (good for utility tools, fast load)
- _Subtle_ — entrance fades, hover affordances, no scroll trickery
- _Confident_ — entrance sequence + 1 scroll-linked effect + 1 hover transition (the default for branded landing pages)
- _Showcase_ — multiple scroll-linked effects, parallax, sticky storytelling, shared layout transitions

#### Menu D — Imagery strategy

- _Real photography_ — described or generated, treated as the page's load-bearing visual anchor (default for venues, lifestyle, brand)
- _Product screenshots / UI captures_ — the product itself is the imagery (default for SaaS, tools)
- _Generated abstract_ — gradients, meshes, generative art (use only when the page is about an idea, not a thing)
- _Type-only_ — no imagery; typography carries the entire page (works for editorial and brutalist directions)

#### Menu E — Color direction

- _Monochrome + one accent_ — recommended default; hardest to mess up
- _Two-tone_ — a foreground/background pair plus one accent
- _Warm palette_ — earth tones, creams, terracotta
- _Cool palette_ — blues, slates, deep greens
- _High-contrast dark_ — black background, one or two saturated accents
- _User-specified hex codes_ — if the user already gave colors, skip this menu entirely

#### Menu F — Typography pairing

- _Editorial serif + clean sans_ — display serif paired with a neutral sans for body
- _Geometric sans only_ — one expressive sans, used at multiple weights
- _Mono + sans_ — monospaced display, sans body (works for tech/utility)
- _Display + grotesk_ — characterful display, neutral grotesk body (default)

> **Forbidden defaults**, never offer these as menu choices: Inter, Roboto, Arial, system-ui, Space Grotesk (overrepresented in AI output), purple→pink gradients on white, white-with-blue-CTA SaaS template.

### How to present the menus

Lead with one short sentence stating what the user is about to decide, then the menus. After the user picks, restate the decisions as a single line of "locked-in choices" so they can be referenced in Phase 3.

If the user replies with "you choose" or "just pick", proceed using the recommended defaults. Do not interview them again.

---

## Phase 3 — Thesis (Working Model)

Before writing any code, write three short artifacts. These are not for the user — they are for the model itself, to anchor every subsequent decision. Output them in the response so the user can sanity-check, but keep them tight.

**1. Visual thesis** — one sentence describing mood, material, and energy.

> Example: _"Cold editorial restraint — a Brooklyn coffee shop that does not need to explain itself; warm grayscale photography, a single oxblood accent, magazine cadence."_

**2. Content plan** — the section sequence with one job per section. For landing pages, default to: Hero → Support → Detail → Final CTA. For apps and dashboards, replace this with the working surface itself (no marketing hero).

> Example: _Hero (brand + opening hours + a single hero photograph) → Support (the menu, one column, no cards) → Detail (about the roaster, single long photograph) → Final CTA (address + map + reserve a table)_.

**3. Interaction thesis** — 2–3 specific motions that change how the page feels. Each one has to be describable in a single phrase. If a motion cannot be described that simply, it is decoration and should not ship.

> Example: _"Hero photograph crossfades through three frames over 8 seconds; section headings reveal in a staggered upward translate on scroll; the menu items underline-fill on hover."_

### Why this phase exists

Models that skip the Working Model invariably ship sections that fight each other, motions that have no relationship to the rest of the page, and content sequences that are just a column of cards. Writing the thesis forces every later choice to be checkable against it: _does this section serve the visual thesis? does this motion match the interaction thesis?_ If the answer is no, it gets cut.

---

## Phase 4 — Build

Now implement. **Read the rule pack for the surface type before writing code.** Each rule pack lives in `references/` and is loaded only when relevant:

- **Landing page / marketing site / portfolio / brand site** → read `references/landing.md`
- **Dashboard / admin tool / internal ops / analytics** → read `references/dashboard.md`
- **Web app / settings / forms / onboarding / product UI** → read `references/app.md`
- **Game UI / interactive artifact / experimental** → read `references/landing.md` for the composition rules and ignore the marketing-copy section
- **Single-file Claude artifact** → read `references/app.md` and additionally apply the artifact constraints in `references/anti-slop.md`

The rule packs differ meaningfully. Applying landing-page rules to a dashboard produces a dashboard with a hero section, which is wrong. Applying dashboard rules to a landing page produces a Notion page, which is also wrong. Read the right one.

### Tech stack defaults

Choose based on the user's constraints. If the user did not specify, lean toward the first option that fits:

1. **Single-file HTML + Tailwind via CDN + vanilla JS** — for one-shot artifacts, prototypes, single-page demos, anything the user wants to copy-paste or share as one file. Most reliable, fastest to render, no build step.
2. **React + Tailwind + shadcn/ui** — for anything that will become a real product or has more than ~3 distinct screens. This is where the model has the most prior and produces the most polished output.
3. **Next.js + Tailwind + shadcn/ui** — only when the user explicitly asks for routing, SSR, SEO, or a deployable webapp.
4. **Vue / Svelte / Astro** — only when the user explicitly requests them. Do not volunteer them.
5. **Vanilla HTML + CSS, no Tailwind** — when the user asks for "no dependencies" or "pure HTML/CSS".

For motion, prefer in this order: pure CSS → Framer Motion (in React) → GSAP (only when CSS and Framer cannot do it).

For icons, prefer Lucide (works in React via `lucide-react` and as inline SVG elsewhere). Avoid emoji as iconography in product UI.

### Imagery sourcing

When the surface needs real imagery and the environment supports it:

- If image generation is available, use it to produce the hero image, briefing it with the visual thesis from Phase 3.
- If image search is available, use it to source 2–4 reference photographs and describe their treatment in the code (alt text, object-fit, focal point).
- If neither is available, use placeholder image services (`picsum.photos` with a fixed seed for reproducibility, or `placehold.co` with the brand colors) and clearly mark them as placeholders the user should replace.

Never commit `<img src="https://placeholder.example/foo.jpg">` without a comment explaining how to replace it.

### Code quality bar

This skill targets production-grade output, not snippets:

- **Responsive by default.** Test the layout mentally at 360px, 768px, and 1280px before declaring done. A landing page that breaks on mobile is broken.
- **Accessible by default.** Real semantic HTML (`<header>`, `<main>`, `<nav>`, `<button>` not `<div onclick>`), focus states that are visible, color contrast at WCAG AA minimum, alt text on every image, labels on every form field.
- **Self-contained.** No reliance on assets the user has to fetch separately unless explicitly noted.
- **Real content over Lorem ipsum.** If the user did not provide copy, write specific, plausible copy in product language. Lorem ipsum is a Phase 5 failure.
- **CSS variables for the design tokens** (colors, type scale, spacing scale, radius). This makes the whole page tunable from one block. The tokens also become the user's handoff document.
- **No dead code.** No leftover commented-out experiments, no unused imports, no `// TODO` left in the file.

---

## Phase 5 — Verify (Design litmus + delivery gate)

Before declaring the work done, walk this design checklist. Any "no" answer means go back and fix, then re-check.

1. **Brand test** — if the navigation were removed, would the brand still be unmistakable in the first viewport? If no, the branding is too weak.
2. **Image test** — if the main image were removed, does the first viewport still work? If yes, the image is decorative and needs to do more work.
3. **Headline scan test** — reading only the headlines top to bottom, does the page make sense? If no, the section copy is doing work the headlines should be doing.
4. **One-job test** — does each section have exactly one job? If a section has two purposes, split it or cut one.
5. **Card audit** — are there any cards on the page that are not themselves the interaction? If yes, remove the card treatment and use plain layout.
6. **Slop scan** — does the page contain any of: Inter font, purple-to-pink gradient on white, generic three-column feature grid, decorative shadows under everything, unused pill clusters, a "trusted by" logo cloud the user did not ask for, lorem ipsum, or a centered single-column layout when the brief did not call for it? If yes, fix it.
7. **Responsive sanity** — at 360px width, does the hero still read in one composition? Are tap targets at least 44px? Is text readable without zooming?
8. **Motion audit** — would the motions still be visible in a quick screen recording? Are any of them purely decorative? If decorative, cut them.
9. **Strip test** — if every shadow, border, and decorative gradient were removed, would the design still feel premium? If no, the design is leaning on chrome to hide weak composition.
10. **Working Model match** — does the final result match the visual thesis from Phase 3? If the build drifted, name the drift and decide whether to bring the build back to the thesis or update the thesis.

Report the litmus result back to the user as a short pass/fail list. This is the moment of accountability.

### Repository delivery gate (mandatory in repository mode)

The litmus checklist proves design quality. It does **not** prove that the repository work is done.

If this task changed a real codebase:

1. Hand control back to the owning process skill (`harness-feat` or `harness-fix`).
2. Name the proving commands needed for the frontend surface:
   - relevant unit/integration tests
   - lint and typecheck
   - build command
   - visual regression / Playwright / screenshot diff command when the repo already has one
3. Require `harness-verify` to run those commands in the current turn before any "done", "fixed", "passing", or "ready" claim.
4. If the commands fail, report the actual blocker instead of hiding behind a good-looking UI.

In short:

```text
Design litmus PASS != repository completion
Repository completion = litmus PASS + fresh technical evidence via harness-verify
```

If the task is artifact mode rather than repository mode, report the litmus result plus any local preview command or usage note that helps the user inspect the artifact.

---

## Universal hard rules

These apply on every build, regardless of surface type. The rule packs in `references/` add more.

- No cards by default. Cards only when the card _is_ the interaction.
- No more than one dominant idea per section.
- No more than two typefaces without a stated reason.
- No more than one accent color unless the existing system already has more.
- No filler copy. Every word is product-language.
- No section headline that overpowers the brand on a branded page.
- No motion that is not describable in a single phrase.
- No `<div>` where a semantic element exists.
- No assumption that the user wants light mode. Ask, or build whichever fits the visual thesis.
- No "AI slop tells" — see `references/anti-slop.md` for the maintained list.

## Hand-off

When the work is complete, give the user these things in the closing message:

1. **The code itself** (or a link to the file/artifact).
2. **The Working Model** from Phase 3, restated, so the user knows what the design is committing to.
3. **The litmus result** from Phase 5.
4. **The technical proving command(s)** that were run, or the exact commands handed back to `harness-verify` for repository-mode completion.
5. **A short list of "obvious next moves"** — two or three specific things the user could ask for next (e.g., _"add a pricing section in the same cadence", "swap the hero for a video", "generate dark mode tokens"_). This turns the hand-off into an invitation to iterate, not a full stop.

## Reference files

- `references/landing.md` — landing page / marketing rule pack (hero rules, viewport budget, narrative sequence, copy rules)
- `references/app.md` — product UI / web app rule pack (Linear-style restraint, surface hierarchy, interaction patterns)
- `references/dashboard.md` — dashboard / admin rule pack (utility copy, KPI orientation, density management, chrome minimization)
- `references/anti-slop.md` — the maintained list of forbidden patterns with examples and what to do instead
- `references/elicitation-menus.md` — extended option menus for Phase 2 with rationale, for cases where the menus in this file are not enough

Read only the files relevant to the current build. Do not pre-load all of them.
