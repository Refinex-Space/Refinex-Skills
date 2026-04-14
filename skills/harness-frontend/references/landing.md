# Landing page rule pack

Read this file when the surface type from Phase 1 is *landing page, marketing site, brand site, portfolio, product launch page, event page,* or *campaign page*. Do not read it for dashboards, internal tools, or product UI — those have their own rule packs and these rules will harm them.

## The default sequence

A landing page is a piece of cinema, not a document. It has four beats. Use them in order. Add more sections only if the user asked for them — never invent a "trusted by" logo cloud, a "frequently asked questions" block, or a three-tier pricing grid that was not requested.

```
1. Hero       — establish identity and promise; one image, one headline, one CTA
2. Support    — one concrete proof point, feature, or offer
3. Detail     — atmosphere, depth, story, or workflow
4. Final CTA  — convert: start, visit, contact, or buy
```

If the brief is genuinely larger (e.g., the user asked for an "agency homepage with case studies"), expand by repeating the Support → Detail rhythm, not by adding card grids.

## Hero rules — the part that matters most

The hero is the entire game. If the hero is wrong, nothing downstream rescues the page. If the hero is right, even a sloppy footer gets forgiven.

### Composition
- **One composition.** The first viewport reads as a single picture, not as a stack of widgets. If you can describe the hero as "a hero section with a card and some pills and a stat strip", it is wrong.
- **Full bleed by default.** The hero image, color field, or video runs edge-to-edge with no inherited page gutters or framed container. Constrain only the inner text/action column, not the hero itself.
- **Brand first, headline second, body third, CTA fourth.** This is the reading order in pixels and in DOM. The brand is the loudest visual element on the page.
- **Hero budget.** The first viewport contains: brand + one headline + one short supporting sentence + one CTA group + one dominant visual. Nothing else. No stats, no event listings, no "this week" callouts, no metadata rows, no secondary marketing blocks, no pill clusters, no badge stickers.
- **No floating overlays on hero media.** No detached labels, no promo stickers, no info chips, no callout boxes layered on top of the image. If something belongs to the hero, it lives in the inner text column.
- **No hero cards.** Ever. Cards in the hero are the single most reliable tell of generic AI output.

### Sticky header math
If the page has a sticky or fixed header, the header counts against the hero. The combined header + hero content must fit in the initial viewport at common desktop and mobile sizes. When using `100vh` or `100svh` heroes, subtract persistent UI chrome:

```css
.hero { min-height: calc(100svh - var(--header-height)); }
```

Or overlay the header on top of the hero image (transparent header, white text, subtle gradient at the top) instead of stacking it in normal flow.

### Headline
- Keep desktop headlines to roughly 2–3 lines. Mobile headlines must be readable in one glance.
- The headline carries the meaning. The supporting sentence is one short clause that adds a single fact, not a paraphrase of the headline.
- No clichés: *"the future of X", "X, reimagined", "where Y meets Z", "experience the difference"*. These are tells.
- Product language, not design commentary. *"Roasted in Bushwick. Served on Bedford."* beats *"A premium coffee experience."*

### Imagery
- Imagery must do narrative work. The image shows the product, the place, the person, the atmosphere — not an abstract gradient.
- The text column must sit on a calm tonal area of the image. If the image is busy everywhere, crop it or pick another image.
- Strong contrast between text and background is non-negotiable. A subtle gradient overlay or a blurred rectangle behind the text is acceptable; relying on the image alone is not.
- One hero image, not a collage. If the brief needs multiple moments, that is what the Detail section is for.
- No images with embedded UI frames, fake browser chrome, screenshot frames, or fake device mockups in the hero unless the product is itself a piece of software being demoed.

## Support section
- One concrete thing. A single feature, a single proof point, a single quote, a single offer.
- Headline that names the thing in product language. Body that explains the thing in one sentence. That is the entire section.
- This is *not* the place for a feature grid. Feature grids belong in the Detail section, and only when the brief asks for them.

## Detail section
- Where atmosphere, depth, and story live. This is the section that earns the page its tone.
- Acceptable shapes: a long horizontal photograph with a paragraph beside it; a vertical stack of three product detail shots with a one-line caption each; a quote from the founder over a textured background; a workflow diagram.
- Unacceptable shapes: a card grid with three icons and three blurbs (the most generic landing page failure mode in existence); a stat strip with three big numbers; a logo cloud the user did not ask for.

## Final CTA
- One action. One verb. One sentence of supporting context if needed, no more.
- The CTA visually echoes the hero CTA. Same color, same shape, same weight. The page closes on the same note it opened with.
- The CTA section is allowed to be quiet. A single button on a clean field is better than a busy "ready to get started?" panel.

## Copy rules

- Write in product language, not design commentary. The page is not allowed to describe itself.
- The headline carries meaning. Supporting copy is usually one sentence.
- Cut repetition between sections ruthlessly. If two sections say the same thing in different words, one of them is wrong.
- Specific over general. *"3 lb of beans, ground that morning, in a paper bag with the roast date stamped on it"* beats *"premium quality coffee."*
- If deleting 30% of the copy improves the page, keep deleting.

## Reject these landing-page failures

These are the patterns the rule pack exists to prevent. If you see yourself producing one, stop and reconsider.

- Generic SaaS card grid as the first impression
- Beautiful image with weak brand presence
- Strong headline with no clear action
- Busy imagery behind text with no contrast treatment
- Hero with a floating "card" containing the CTA
- "Trusted by" logo cloud immediately under the hero, when the user did not ask for one
- Three-feature-column block as the only support content
- Carousel with no narrative purpose ("our customers love us")
- Section that repeats the same mood statement as the hero
- Pill cluster of "tags" or "categories" floating in the hero
- Stat strip with three big numbers and three labels
- Split-screen hero where the text side is a card with rounded corners

## Litmus checks specific to landing pages

In addition to the universal litmus checks in SKILL.md, ask:

1. Could the first viewport belong to another brand if the navigation were hidden? If yes, the branding is too weak.
2. Does the hero image carry actual narrative weight? If the hero still works after deleting the image, the image is decorative.
3. Is the brand visually louder than every section headline that follows it? It must be.
4. If the page were printed in black and white, would the hierarchy still read? If no, the design is leaning on color to do hierarchy's job.
5. Does the page close on the same note it opened? The final CTA should rhyme with the hero, not introduce a new mood.