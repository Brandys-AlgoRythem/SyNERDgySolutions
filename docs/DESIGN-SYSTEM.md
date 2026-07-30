# Initial Website Design System

## Status

This is the structural Version 1 design foundation. It creates reusable rules without pretending the aesthetic is finished. Visual refinement follows after the content architecture and site shell can be reviewed in a browser.

## Brand principle

- **Visual metaphor:** the hive and honeycomb
- **Verbal metaphor:** seams, connections, and loose threads
- **Guardrail:** use both with restraint. The company must not resemble a sewing store, apiary gift shop, or generic glowing-tech startup.

## Working color tokens

These are development placeholders subject to accessibility testing and final approval.

| Token | Working value | Purpose |
|---|---:|---|
| `--color-ink` | `#1F1A17` | Primary dark text and dark surfaces |
| `--color-cream` | `#FFF9EC` | Warm primary background |
| `--color-gold` | `#D6A21E` | Primary accent and selected controls |
| `--color-gold-light` | `#F4C95D` | Decorative highlights, not body text |
| `--color-surface` | `#FFFFFF` | Cards and elevated surfaces |
| `--color-muted` | `#625B53` | Secondary text with contrast verification |
| `--color-border` | `#D8CDBD` | Subtle boundaries |
| `--color-focus` | `#7A4E00` | Keyboard focus indicator |
| `--color-success` | `#2F6B3A` | Status use when needed |

Gold must not be used as small text on cream backgrounds unless contrast testing proves it passes.

## Typography

### Version 1 stack

Use a system-font stack during structural development:

```css
font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
  "Segoe UI", sans-serif;
```

`Inter` remains optional unless a properly licensed local or hosted source is approved. The site must remain readable without it.

### Type roles

- Display heading: strong, compact, high contrast
- Section heading: clear hierarchy without decorative overload
- Body: comfortable line height and maximum line length
- Eyebrow or label: concise uppercase or small-caps treatment used sparingly
- Buttons: sentence case and action-oriented

## Working type scale

```text
--font-size-xs: 0.8rem
--font-size-sm: 0.925rem
--font-size-base: 1rem
--font-size-md: 1.125rem
--font-size-lg: 1.375rem
--font-size-xl: 1.75rem
--font-size-2xl: clamp(2rem, 5vw, 3.5rem)
--font-size-3xl: clamp(2.5rem, 7vw, 5rem)
```

## Spacing scale

Use a consistent scale rather than arbitrary one-off values:

```text
--space-1: 0.25rem
--space-2: 0.5rem
--space-3: 0.75rem
--space-4: 1rem
--space-5: 1.5rem
--space-6: 2rem
--space-7: 3rem
--space-8: 4.5rem
--space-9: 6rem
```

## Layout

- Maximum reading width: approximately 70 characters
- Maximum general content width: approximately 72rem
- Full-bleed sections may use internal constrained containers
- Mobile-first layout
- Breakpoints should follow content needs rather than device-brand folklore
- Major sections require generous vertical spacing

## Components

### Buttons

Primary:
- Dark ink or accessible gold background
- Strong text contrast
- Visible hover and focus states

Secondary:
- Transparent or light surface
- Clear border
- Must remain visibly interactive without hover

### Cards

- White or cream surface
- Subtle border
- Minimal shadow
- Consistent padding
- No excessive floating, glowing, or glass effects

### Navigation

- Clear active-page state
- Keyboard-visible focus
- Accessible mobile-menu control
- Contact CTA visually distinct but not dominant enough to bury navigation

### Call-to-action sections

- Strong headline
- One brief supporting statement
- One primary action and, only when useful, one secondary action
- Avoid decorative clutter around conversion areas

## Honeycomb usage

Allowed:
- Low-contrast geometric background accents
- Section dividers
- Cropped structural patterns
- Small brand marks

Avoid:
- Dense repeating wallpaper behind body text
- Honeycomb bullets on every list
- Literal honey drips
- Cartoon bees
- Making every container a hexagon, because rectangles have done nothing to deserve this abuse

## Seam-language usage

Approved high-impact placements:
- Hero
- Problem recognition
- Method or solution transition
- Closing CTA

Avoid repeating seam, thread, stitch, unravel, and patch language in every paragraph.

## Technology cues

Circuit-board or motherboard details may be added during aesthetic refinement when they support the systems-and-technology positioning. They must remain secondary to readability and the hive structure.

## Accessibility rules

- Target practical WCAG 2.2 AA compliance
- Text contrast must be tested, not guessed
- Visible focus states on all interactive elements
- Logical heading order
- Minimum comfortable tap targets
- No information conveyed only by color
- Respect `prefers-reduced-motion`
- Decorative graphics must be hidden from assistive technology
- Meaningful images require useful alternative text

## Motion

Version 1 starts with no required decorative animation. Later motion must be subtle, purposeful, and disabled or reduced for users who request reduced motion.
