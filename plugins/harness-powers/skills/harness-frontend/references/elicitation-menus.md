# Extended elicitation menus

Read this file when the menus in SKILL.md Phase 2 are not enough — for example, when the build is unusual (a game UI, an editorial site, a generative art piece) or when the user has rejected the default menus and asked for more options.

The principle remains the same: every question is a closed menu with a recommended default, never an open prompt.

## When to use these instead of the SKILL.md menus

- The user said "give me more options" after seeing the default menus
- The surface type is something the default menus do not cover well (game, editorial, generative art, calculator, data viz piece, custom widget)
- The user has clearly strong taste and the defaults are too generic
- The user has rejected the first round and you need a fresh angle

## Extended Tone menu

The 6 tones in SKILL.md cover most cases. Here are 8 more for unusual briefs.

- *Editorial swiss* — Helvetica or Akzidenz, strict grid, generous margins, black-and-white photography, magazine cadence
- *Late-90s OS* — chunky bevels, system fonts of the era, fixed-width forms, deliberate "computer" feel
- *Newspaper* — serif body, narrow columns, drop caps, hairline rules, beige paper background
- *Cyberpunk neon* — black background, cyan and magenta, scanlines, monospaced display type
- *Risograph print* — limited spot colors, slight misregistration, halftone textures, paper grain
- *Construction site* — yellow and black, hard sans, stencil display, danger-tape borders, deliberate utility
- *Botanical journal* — illustrated decorative elements, warm cream background, italic display serif, naturalist captions
- *Tactical / military* — olive and orange, monospaced, grid coordinates, callouts, deliberate density

For each, give the user a one-sentence example of what it means to commit. Do not let "tactical" mean "we added one army-green button."

## Extended Density menu

- *Sparse* — one idea per viewport, slow scroll, the page reads like a presentation
- *Generous* — the SKILL.md "Generous" default
- *Balanced* — the SKILL.md "Balanced" default
- *Dense* — the SKILL.md "Dense" default
- *Bloomberg* — maximum density, every pixel has a job, designed for operators who use this all day

## Extended Motion menu

- *None* — static, no animation
- *Subtle* — entrance fades, hover affordances
- *Confident* — entrance + 1 scroll-linked + 1 hover (the default)
- *Showcase* — multiple scroll-linked, parallax, sticky storytelling, shared layout transitions
- *Cinematic* — full-page sequenced reveals, choreographed, the page is a piece of cinema (only for genuinely premium brand pages)
- *Reactive* — the page responds to mouse position, gyroscope, audio input, etc. (only for art and game UIs)

## Layout architecture menu (for complex pages)

When the page is more than a simple top-to-bottom scroll, ask the user about layout shape:

- *Vertical scroll* — the default
- *Horizontal scroll* — for portfolios and editorial cases; works best with strong section transitions
- *Asymmetric grid* — sections live in a 12-column grid and break it deliberately
- *Sticky-side, scroll-other* — left side stays, right side scrolls (or vice versa); good for product detail pages
- *Pinned sections* — each section pins as you scroll past, then unpins (GSAP scrolltrigger territory)
- *Single screen, no scroll* — everything fits in one viewport (good for landing experiments and simple tools)

## Imagery treatment menu (when imagery is the main visual)

- *Full-bleed, untreated* — the photograph runs edge-to-edge with no overlay, text sits on a calm tonal area
- *Full-bleed, gradient overlay* — a vertical or radial gradient overlay where the text sits, for contrast
- *Inset with generous margin* — the image lives inside a margin, with whitespace as a frame
- *Cropped to a band* — the image becomes a horizontal band across the page, not a hero
- *Duotone* — the image is mapped to two brand colors, losing photographic fidelity for graphic strength
- *Halftone or grain* — the image is treated with print texture for a tactile feel

## Form architecture menu (for forms and onboarding)

- *Single page, all fields visible* — the default for short forms (≤ 8 fields)
- *Multi-step wizard with progress* — for forms with > 8 fields or with branching logic
- *Conversational* — one question per screen, chat-style, for emotional or sensitive content
- *Inline-as-you-go* — the user sees the result update live as they fill the form (good for calculators and configurators)

## Data presentation menu (for dashboards and analytics)

- *KPI strip + chart + table* — the default operator dashboard
- *Single big chart* — for dashboards built around one critical metric
- *Grid of small multiples* — for comparing the same metric across many segments
- *Spreadsheet-style* — for power users who want raw data with light formatting
- *Narrative scrollytelling* — for analytics meant to be read like an essay (rare; only when the user explicitly asks)

## Guidance for using this file

1. Read this file only when the SKILL.md menus are not enough. Do not over-elicit.
2. Pick the menus that are genuinely undecided. If the user has already said "I want a dashboard for my ops team", you do not need to ask the Tone menu — the answer is *Technical & utilitarian*.
3. Cap the round at 4 questions total, even from this extended set. More than 4 questions wears out the user's patience and the marginal value drops fast.
4. Always pre-select your recommended default. Never present a menu without saying which one you would pick.
5. After the user answers, restate their choices in one line so they know what is locked in.