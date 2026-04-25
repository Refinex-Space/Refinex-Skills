# Web app / product UI rule pack

Read this file when the surface type from Phase 1 is *web app, settings screen, form, onboarding flow, product UI, single-file Claude artifact,* or *internal tool*. Do not read it for landing pages or marketing surfaces — they have a different rule pack.

## The mental model: Linear, not Stripe Dashboard

Default to the cadence of Linear, Vercel, Notion, and Height: calm surfaces, strong typography, dense but readable information, very few colors, almost no decorative chrome. The product is the content. The interface gets out of the way so the user can do their work.

This is the opposite of the marketing-page mode, where the interface IS the content. Get the mode right or everything else falls apart.

## Surface hierarchy

Most product UIs decompose into four zones. Build them in this order:

```
1. Primary workspace      — where the user actually works
2. Navigation             — how the user moves between workspaces
3. Secondary context      — inspector, sidebar, detail panel, breadcrumbs
4. Action zone            — primary CTA, status, save state, sync indicator
```

The primary workspace gets the most visual weight, the most space, and the calmest treatment. Everything else exists to serve it.

### Calm surfaces
- Use one or two background tones across the whole app, not five. A subtle distinction between "page background" and "elevated surface" is enough.
- No drop shadows under everything. Reserve shadows for genuinely floating elements (modals, dropdowns, popovers). A card that is not floating does not need a shadow.
- No thick borders on every region. A 1px border at low opacity is the maximum default. If a region needs more separation, use whitespace instead.
- No decorative gradients behind routine product UI. Gradients in product UI are reserved for empty states, onboarding moments, and brand surfaces.

### Strong typography and spacing
- Type is the primary tool for hierarchy. Use weight (regular / medium / semibold) and size to create clear levels — not color.
- Default to at most 4 type sizes across the entire UI: a small label size, a body size, a heading size, and a display size for empty states. More than that is noise.
- Use a generous baseline grid (8px or 4px increments) and stick to it. Visual rhythm in product UI comes from consistent spacing more than from anything else.
- Truncate long strings with ellipsis and tooltips, do not let text wrap and reflow tables.

### Few colors
- One foreground, one muted foreground (for secondary text), one background, one elevated surface, one border, and **one accent**. That is the entire palette. Anything more is a color leak.
- The accent is for primary actions and active states. Not for headings, not for hover backgrounds, not for icons that are not interactive.
- Status colors (success, warning, error, info) are not the same as the accent. They live in a separate semantic layer and only appear when status is being communicated.

## The cards rule

This is the single rule that separates good product UI from generic SaaS:

> **Cards only when the card itself IS the interaction.**

A clickable list of items where each item navigates somewhere is acceptable as cards. A "dashboard" with three "summary cards" stacked next to each other is not — those are sections, and they should be drawn as plain layout with headings and dividers, not as bordered boxes with shadows.

The test: if you removed the border, the background, the shadow, and the radius from a "card", and the result still made sense as plain layout, then it never should have been a card.

## What to avoid

- **Dashboard-card mosaics.** Six bordered rectangles in a 3×2 grid, each with a tiny chart, is the most reliable failure mode in product UI. Use the dashboard rule pack (`references/dashboard.md`) for actual dashboards.
- **Thick borders everywhere.** A border on every panel makes the entire UI feel boxed in.
- **Multiple competing accent colors.** One accent. If you need more, you have a status color, not an accent.
- **Decorative icons that do not improve scanning.** Every icon should answer the question "would removing this make the row harder to scan?" If no, remove it.
- **Hero sections on product UI.** Settings screens and forms do not get hero sections. Start with the working surface.
- **Empty-state illustrations on every empty list.** Use them for major empty states (no projects yet, no notifications yet) but not for "no results match your filter" — that is just text.

## Component patterns

### Forms
- Labels above fields, not floating placeholders. Floating labels read clever in mockups and fail in real use.
- Errors inline with the field, not at the top of the form.
- The primary action is on the right (in LTR) or at the end of the form. The secondary action (cancel, back) is to its left.
- Required fields are marked with a subtle indicator (`*` or "Required" text), not by making optional fields say "Optional".
- Group related fields with whitespace, not with bordered cards.

### Tables
- Left-align text columns, right-align numeric columns, center icons.
- Row hover state is allowed. Row click state is allowed if the row is interactive. Stripes are not allowed by default — they add noise without aiding scanning.
- Sticky header on long tables. Sticky first column on wide tables. Both if both apply.
- A table of more than 50 rows needs pagination, virtualization, or filtering — never just a long scroll.

### Navigation
- Sidebar nav is the default for apps with more than 3 top-level sections. Top tab nav is for 2–3 sections.
- The active item is marked with the accent color and (subtly) a background. Not both at full strength.
- Collapse the sidebar on screens narrower than 1024px. The collapsed state shows icons only, with tooltips.

### Modals and dialogs
- Modals are for confirmation and for focused tasks that fit on one screen. They are not for multi-step flows — those go on their own page.
- A modal has one primary action and at most one secondary. The escape key and clicking outside both close it (unless it is destructive — then require an explicit cancel).
- The background dims to roughly 40-60% black. Not a blur unless the page underneath is meaningful as context.

## Single-file Claude artifact special rules

When the build is a single-file artifact for a Claude conversation:

- No `localStorage`, `sessionStorage`, or any browser storage API. Use React state or in-memory JS variables only.
- No external network requests except to `https://cdnjs.cloudflare.com` and named CDNs that the environment allows.
- Tailwind via the play CDN is fine for HTML; for React artifacts use the pre-defined Tailwind utility classes (no custom Tailwind config).
- Test mentally that the artifact works on a touch device — Claude artifacts get viewed on phones constantly.
- Keep the visible surface usable without scrolling on a mobile viewport whenever possible. Artifacts that demand scrolling on first paint feel broken.
- One file. No build step. No imports beyond what the artifact environment already provides.

## Litmus checks specific to product UI

In addition to the universal litmus checks in SKILL.md, ask:

1. Strip every shadow, every border, every background — does the hierarchy still read from typography and spacing alone? It must.
2. Count the accent colors used. More than one? Cut to one.
3. Count the cards on screen. For each one, ask: would this still make sense as plain layout? If yes, decard it.
4. Could a new user understand what they are looking at within 3 seconds? If no, the labels and headings are not doing their job — see `references/dashboard.md` for the orientation copy rules.
5. At a 360px width, does the layout collapse cleanly to a single column? Or does it produce a horizontal scrollbar of doom?