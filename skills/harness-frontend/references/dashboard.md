# Dashboard / admin / analytics rule pack

Read this file when the surface type from Phase 1 is *dashboard, admin tool, internal ops console, analytics view, monitoring screen, observability dashboard,* or *operator workspace*. Do not read it for marketing pages or for product UI that is not data-dense — those have different rule packs.

## The fundamental shift: utility, not marketing

The single biggest mistake in AI-generated dashboards is that they look like marketing pages. They have hero sections, aspirational headlines, gradient backgrounds, mood lighting, and "Welcome back, Sarah! Here's your week at a glance" copy. Operators hate this. They want orientation, status, and action.

A dashboard is a working surface. The operator opens it to do a job: monitor a metric, find an outlier, investigate an alert, run a query, change a setting. Every pixel should serve that job. If a pixel does not help the operator orient, monitor, or decide, cut it.

```
Marketing mode (wrong for dashboards)         Utility mode (right)
─────────────────────────────────              ─────────────────────────────────
Hero with brand promise                        Working surface immediately
Aspirational headlines                         Headings that name the thing
Mood photography                               Charts and tables
Pill clusters, badges, gradients               Numbers, labels, status dots
"Welcome back!" greetings                      Last sync timestamp
Generous whitespace                            Dense, scannable
```

## Start with the working surface

Open the page with the working surface itself, not with a hero. The first viewport should contain whatever the operator most needs to see: the KPI strip, the chart, the filter bar, the table, the alerts list. No introduction. No greeting. No "this dashboard shows you..." preamble.

The only exception is when the operator must make a context choice before any data is meaningful (e.g., "select a workspace to view" or "select a date range"). In that case, the first thing they see is the context selector, large and centered, and nothing else.

## Section headings name the thing

Headings on a dashboard say what the area *is* or what the user can *do* there. They are utility labels, not marketing copy.

- **Good:** *Selected KPIs*, *Plan status*, *Search metrics*, *Top segments*, *Last sync*, *Active alerts*, *Recent runs*
- **Wrong:** *Your performance at a glance*, *The metrics that matter*, *Insights*, *Overview* (lazy), *Welcome to your dashboard*

If a heading could appear in a homepage hero or an ad, rewrite it. Litmus test: does the heading help the operator find the section by scanning? If no, rewrite.

## Supporting text

Supporting text on a dashboard explains scope, freshness, behavior, or decision value in one short sentence. Examples:

- *"Updated 14 minutes ago. Includes test traffic."*
- *"Past 30 days. Excludes refunded orders."*
- *"Only shows users in the EU region per current filter."*

Not:

- *"This is where you can see how your business is performing."* (Says nothing.)
- *"Drive insights and unlock value with our analytics."* (Marketing soup.)

## Density management

Dashboards live and die by density. Too sparse and the operator scrolls forever. Too dense and the operator cannot find anything.

- Default to dense. Operators are looking at this all day; they want to see a lot at once.
- Use a 12-column grid with 16px or 24px gaps. KPI tiles span 2–3 columns each. Charts span 4–6 columns. Tables span the full 12.
- Stack vertically on screens narrower than 1280px. Dashboards on tablets and phones are a degraded experience by design — make them readable, do not try to make them ideal.
- Do not put a card border around every region. Use whitespace and subtle dividers instead. The dashboard is one continuous surface, not a mosaic of cards.

## KPI tiles

The KPI strip is usually the top of the dashboard. Each KPI tile contains, in this exact reading order:

1. The label, in small caps or muted body type — *Active users (7d)*
2. The number, in a large display weight — *24,318*
3. The delta vs the comparison period, in a small line — *+3.2% vs prior 7d*
4. (Optional) A sparkline, low-saturation, no axis labels

Do not add an icon to every KPI tile. Icons in KPI strips are decorative noise. Do not put a card border, shadow, or background on the tile by default — let the typography do the work and use vertical dividers between tiles only if separation is genuinely unclear.

## Charts

- Pick the chart type that fits the question, not the type that looks impressive. Most dashboard questions are answered by line charts (trends), bar charts (comparisons), and tables (lookups). Use anything else only when those three cannot answer the question.
- Strip chart chrome ruthlessly: no chart title repeating the section heading, no legend if there is only one series, no axis label if the units are obvious from the heading, no gridlines that fight the data.
- One color per series. The accent color is reserved for the most important series; everything else is a desaturated neutral.
- Tooltips on hover, not always-on labels.
- Empty state: *"No data in the selected range."* Not an illustration. Not an explanation of what the chart would show. Just the fact.

## Tables

Tables are the backbone of most dashboards. See `references/app.md` for the general table rules. Specific to dashboards:

- Show the most useful columns by default. Hide the rest behind a column toggle.
- Sort the table on the column the operator most likely cares about (usually the most recent timestamp or the largest value), not alphabetically.
- Allow filtering at the column level for any column with discrete values.
- Export to CSV is non-negotiable for any dashboard table over 20 rows.
- Numbers right-aligned, monospace if precision matters (financial data, latencies).

## Status communication

Dashboards constantly communicate state. Use a small, consistent vocabulary:

- A small filled circle for status: green, yellow, red, gray.
- A timestamp for freshness: *"Synced 2m ago"*, with the timestamp turning amber after a threshold and red after a longer threshold.
- A toast or banner for failures, with a clear next action: *"Sync failed. Retry"*. Not just *"Something went wrong."*

Status colors are semantic, not decorative. They appear only when status is being communicated. Do not use the success-green elsewhere on the page.

## What dashboards must not have

- Hero sections with aspirational copy
- "Welcome back, [name]!" greetings (operators see this 40 times a day; it is friction)
- Decorative gradients in the background
- Marketing-style imagery (people in offices, abstract gradients, brand lifestyle shots)
- Three-column "feature" grids
- Card-mosaic layout where every panel has a thick border and a shadow
- More than one accent color
- Animated number tickers on initial load (they obscure the actual value for 800ms)
- Carousel of "tips" or "what's new" content
- A "share this dashboard" button before the dashboard itself is visible

## Litmus checks specific to dashboards

In addition to the universal litmus checks in SKILL.md, ask:

1. **Operator scan test.** If an operator scanned only the headings, labels, and numbers — ignoring all other text — could they understand what they are looking at and what state things are in? They must.
2. **Marketing scrub.** Does any heading or sentence on the page sound like it could appear in a homepage hero or an ad? If yes, rewrite it in utility language.
3. **Freshness test.** Can the operator tell, at a glance, when the data was last updated? If no, add a sync timestamp.
4. **Action test.** When something is wrong (a metric is red, a sync failed, an alert is firing), is the next action obvious and one click away? It must be.
5. **Decard the dashboard.** Count the bordered card panels. For each one, ask: does the border earn its keep, or is the content already separated by whitespace and headings? Decard everything that does not need it.
6. **The 5-second test.** Show the page to someone who has never seen it. In 5 seconds, can they say what the page is for and what state things are in? If no, the orientation is failing.