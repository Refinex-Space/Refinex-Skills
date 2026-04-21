# Mermaid styling standard

This file defines the styling bar for Markdown Mermaid diagrams. The visual goal is calm technical clarity.

## Default aesthetic

Prefer diagrams that look intentional before any custom styling:

- balanced direction
- short labels
- consistent node roles
- whitespace created by small scope, not hacky spacing

Color is optional. Structure is not.

## Styling hierarchy

Apply styling in this order:

1. Simplify the diagram structure
2. Normalize labels and shapes
3. Add a single semantic accent if needed
4. Add one muted contrast role only if it improves the argument

If a diagram still needs more styling than this, it probably needs to be split.

## Palette discipline

Use a restrained palette:

- Neutral base for ordinary nodes
- One accent color for the load-bearing path, decision, or focus element
- One muted color for external systems, optional branches, or deprecated paths

Avoid rainbow semantics. A technical diagram is not a dashboard legend.

## Portable styling defaults

For maximum Markdown portability, prefer one of these two modes:

### Mode A — no custom styling

Use no theme block and no explicit styles. Let clarity come from structure.

### Mode B — minimal role styling

Use a tiny amount of styling only when it clarifies a semantic contrast:

- one `classDef default` or neutral node class
- one accent class
- optionally one muted class

Do not combine `themeVariables`, many `classDef`s, `style`, and `linkStyle` unless the environment is known and the benefit is real.

## Shape discipline

Use shape changes only when they encode meaning the reader needs:

- process or stage
- decision
- storage or external system

Do not rotate through shapes for visual variety.

## Edge discipline

- Use edge labels only when they carry meaning that the prose cannot safely imply.
- Keep arrow styles consistent within the same logical role.
- Avoid using styling to compensate for too many edges.

## When custom theming is acceptable

Custom theming is acceptable only when both of these are true:

1. The target renderer is known to support it.
2. The styling materially helps the reader separate roles or focus paths.

When theming is needed, keep the override surface small. Prefer a base theme with a few variables over a pile of ad hoc per-node styles.
