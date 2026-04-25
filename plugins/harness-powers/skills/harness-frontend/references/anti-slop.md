# Anti-slop reference

The maintained list of patterns that mark a frontend output as "obviously AI-generated", along with what to do instead. Read this file in Phase 5 verification and any time the build is starting to drift toward any of these patterns.

This list is a living document. When a new tell becomes common, it gets added here.

## The font tells

| Slop | Why it tells | What to do instead |
|---|---|---|
| Inter | Used in roughly 40% of AI-generated pages because it is what shadcn/ui ships with by default. Operators recognise it instantly. | Pick a deliberate display font. Recent good defaults: *Söhne, Geist, GT America, Space Mono (display only), Fraunces, Instrument Serif, Tiempos, Domaine Display, Reckless, Migra, JetBrains Mono*. Pair with a neutral body. |
| Roboto | Android default. Looks like a wireframe. | Anything intentional. |
| Arial / system-ui | Looks like nothing. | Anything intentional. |
| Space Grotesk | Was a refreshing choice three years ago, now overused in AI output specifically because every "tasteful" example uses it. | Use a more recent grotesk: *Geist, Söhne, GT America, Inter Display* (different from Inter), *Neue Haas Grotesk*. |
| Comic Sans (genuinely) | Only as a deliberate joke for a kids' app. | N/A. |
| Three different display fonts | Indecision. | Pick two: one display, one body. That is the system. |

## The color tells

| Slop | Why it tells | What to do instead |
|---|---|---|
| Purple-to-pink gradient on a white background | The single most common AI tell. Both LLMs and image generators converge on this. | Start with a real color choice from the visual thesis. Earth tones, monochrome with one violent accent, two-tone editorial — anything but `from-purple-500 to-pink-500`. |
| Blue (`#3B82F6`) as the only accent on a white page | The default Tailwind blue. It is everywhere. | If blue is right for the brand, pick a non-default shade: deeper, more saturated, more muted, or shifted toward teal/indigo/slate. |
| Sky-blue → indigo gradient | The "tech startup" cliché. | A solid color, or a gradient using brand-specific hues. |
| Five different hover colors | Color leak. | One accent. Period. |
| Background that is `#F9FAFB` for no reason | The default "soft gray" panel. Everywhere. | Pure white, or a meaningfully tinted off-white that supports the visual thesis. |
| Dark mode that is `#0A0A0A` text on `#FFFFFF` cards | "Dark mode" applied as an inversion, not designed. | Design dark mode as its own thing, with its own palette. |

## The layout tells

| Slop | Why it tells | What to do instead |
|---|---|---|
| Centered hero with a single column, max-width 768px, on every page | The default. | Full-bleed hero with an inner text column off-center. Or a split layout. Or a giant headline that breaks the grid. |
| Three-feature grid with icons above three blurbs | The most reliable AI tell in landing pages. | If the user genuinely wants three features, integrate them into the Detail section as paragraphs, photographs, or a single horizontal layout — not as a card grid. |
| "Trusted by" logo cloud immediately under the hero | Almost always invented. | Do not include unless the user asked for it AND provided real logos. |
| Stat strip ("10k+ users", "99.9% uptime", "4.8 ⭐") at the top of the page | Invented numbers. | Do not include unless the user provided real numbers and asked for them. |
| Dashboard mosaic of six bordered cards | The default. | Read `references/dashboard.md`. |
| Pricing tiers in three centered cards with the middle one scaled up | The SaaS template. | If pricing is needed, start from the visual thesis. A row of plain text columns can outperform a card trio. |
| Faq accordion at the bottom of every landing page | Filler. | Only if the user asked for it. |
| "Get started" CTA button in the top-right of the nav AND the hero AND the final section AND a sticky bottom bar | CTA panic. | Two CTAs maximum: one in the hero, one at the end. Maybe one in the nav if it is genuinely a top-level action. |
| Uniform `rounded-xl` (or `rounded-2xl`) on every element on the page | The default. | Pick a radius from the visual thesis. Sharp corners, soft corners, asymmetric corners, or a mix — make it a deliberate choice, not a default. |

## The motion tells

| Slop | Why it tells | What to do instead |
|---|---|---|
| Every element fades up on scroll | Decorative motion with no hierarchy. | Pick 2–3 specific motions that matter. Most elements should not animate. |
| Hover scale on every card (`hover:scale-105`) | Default. | Hover affordance should be specific: an underline fills, a label appears, a shadow grows, the cursor changes. |
| A "marquee" of customer logos sliding sideways forever | Filler motion. | Static logo grid if logos are needed at all. |
| Particle background, animated gradient mesh, or floating blobs | Decoration that fights the content. | If the page needs atmosphere, the imagery does that work. |
| Number counters that animate from 0 to the value on load | Hides the actual value for the first 800ms. | Show the number. |
| Typewriter effect on a headline | Almost always wrong. | Show the headline. |

## The copy tells

| Slop | Why it tells | What to do instead |
|---|---|---|
| Lorem ipsum | Inexcusable. | Write specific, plausible product copy in the user's voice. If the user did not give a voice, infer one from the visual thesis. |
| "The future of [X], reimagined." | Cliché. | A specific sentence about what the product actually does. |
| "Where [X] meets [Y]." | Cliché. | A specific sentence. |
| "Experience the difference." | Says nothing. | Cut entirely. |
| "Empower your team to..." | The B2B SaaS opener. | A sentence about what actually changes for the user. |
| "Seamlessly integrate with your existing workflow" | Says nothing. | If integration is real, name what it integrates with. |
| Headlines that paraphrase the body underneath them | The headline should carry the meaning; the body should add a fact. If they say the same thing, cut the body. |
| Section headings like "Overview", "Features", "Benefits" | Lazy. | Headings that name the thing or describe the action. |
| Filler product names like "ProductName" or "Acme" left in the final output | Forgot to replace placeholders. | Always replace placeholders before declaring done. |

## The component tells

| Slop | Why it tells | What to do instead |
|---|---|---|
| shadcn/ui `<Card>` used for every section of a landing page | shadcn was meant for product UI, not as a marketing-page primitive. | On landing pages, do not use `<Card>` at all. Use plain `<section>` with typography and spacing. |
| `<Badge variant="secondary">` floating in the hero | The "eyebrow" pill that everyone uses. | An eyebrow line in small caps body text, or no eyebrow at all. |
| Every form field wrapped in a card | Default. | Group form fields with whitespace. The form is the surface. |
| Toast notifications for every action including ones the user already saw confirm visually | Notification spam. | Toasts only for events the user did not directly cause or did not see the result of. |
| Skeleton loaders on every page even when the data loads in 80ms | Skeleton theater. | Skeleton loaders only when load time genuinely exceeds 300ms. Otherwise, a brief spinner or nothing at all. |

## The artifact tells (single-file Claude artifacts specifically)

| Slop | Why it tells | What to do instead |
|---|---|---|
| The artifact is a single centered card on a white background | The Claude artifact default. Both wrong and boring. | Treat the artifact viewport as its own canvas. Fill it. Bleed to the edges. |
| Tailwind's default `bg-gray-50` everywhere | Default. | Pick a real background. |
| The artifact uses `localStorage` despite the artifact environment not supporting it | Will silently break. | React state or in-memory variables only. |
| The artifact's "submit" button is a `<form>` with an `onSubmit` | Forms are explicitly forbidden in React artifacts. | `onClick` handlers on buttons. |
| The artifact requires three separate npm packages that the artifact environment does not provide | Will not run. | Check the artifact environment's allowed imports before reaching for libraries. |

## How to use this list

In Phase 5, scan the build for any of these patterns. If you find one, fix it. Do not negotiate with yourself. The presence of any single item on this list is enough to mark the build as slop.

This list is also useful in Phase 2: when offering option menus, never offer any of the slop choices as an option. If a user explicitly requests one (e.g., "I want a purple gradient hero"), give it to them — but flag the request and offer one alternative they might prefer.