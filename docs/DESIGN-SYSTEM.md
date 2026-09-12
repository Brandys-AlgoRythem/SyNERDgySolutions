# SyNERDgy Website Design System

## Status

Version 1 visual foundation approved for the MVP build. The system is intentionally restrained: high-contrast black, warm cream, and honey-gold; clean system typography; strong spacing; and geometric hive details used only where they clarify the brand.

## Brand principle

- **Visual metaphor:** hive cells and connected structure
- **Verbal metaphor:** seams, handoffs, and loose threads
- **Design posture:** corporate, precise, warm, and credible
- **Guardrail:** the site must not resemble a sewing store, apiary gift shop, or generic glowing-tech startup

## Color tokens

| Token | Value | Use |
|---|---:|---|
| `--color-ink` | `#191513` | Primary text and dark sections |
| `--color-ink-soft` | `#2A2420` | Dark gradients and elevated dark surfaces |
| `--color-cream` | `#FBF6E8` | Main page background |
| `--color-cream-deep` | `#F3EAD5` | Warm alternate surface |
| `--color-gold` | `#E2AE2D` | Primary accent |
| `--color-gold-strong` | `#C98B00` | Strong decorative accent |
| `--color-gold-dark` | `#704800` | Accessible accent text and hover state |
| `--color-gold-soft` | `#F8DF8E` | Gold section backgrounds and highlights |
| `--color-surface` | `#FFFDF8` | Cards and elevated light surfaces |
| `--color-surface-muted` | `#F7F0E1` | Secondary light surface |
| `--color-muted` | `#5C534B` | Secondary body text |
| `--color-border` | `#D8CCB8` | Standard boundaries |
| `--color-border-strong` | `#BCA98B` | Hover and high-emphasis boundaries |
| `--color-focus` | `#5B3700` | Keyboard focus ring |

Gold is not used for small body text on cream. Dark gold is used when the accent must carry text.

## Typography

The MVP uses a durable system-font stack:

```css
font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
  "Segoe UI", sans-serif;
```

The design does not depend on a remote font request. This avoids licensing, privacy, performance, and failure-mode complications.

### Type roles

- Display headings: compact, high-contrast, balanced line wrapping
- Section headings: strong hierarchy without ornamental typography
- Body: `1rem` base, comfortable `1.65` line height
- Eyebrows: concise uppercase labels used sparingly
- Buttons: sentence case, action-oriented, minimum `3.25rem` height

### Type scale

```text
--font-size-xs: 0.8rem
--font-size-sm: 0.925rem
--font-size-base: 1rem
--font-size-md: 1.125rem
--font-size-lg: 1.375rem
--font-size-xl: 1.75rem
--font-size-2xl: clamp(2rem, 5vw, 3.75rem)
--font-size-3xl: clamp(2.65rem, 7.8vw, 5.75rem)
```

## Layout and spacing

- General content width: `76rem`
- Reading measure: `44rem`
- Section spacing: `clamp(4.5rem, 9vw, 8rem)`
- Mobile gutters: never below `0.75rem` per side
- Main breakpoints: `72rem`, `68rem`, `64rem`, `52rem`, `38rem`, and `34rem`, selected by content behavior rather than device brands

The spacing scale extends from `0.25rem` through `8rem`. One-off spacing values are avoided unless geometry requires them.

## Components

### Buttons

- Minimum height: `3.25rem`
- Primary: ink background with white text
- Secondary: warm surface with a strong neutral border
- Gold: honey-gold background with ink text
- Hover lift is limited to fine-pointer devices so touch interfaces do not simulate unavailable states
- Active state removes lift and shadow

### Cards

- Warm-white surface
- Visible neutral border
- Low, soft shadow
- Consistent radius and padding
- Hover lift is subtle and decorative only; no card is presented as a link unless it is actually interactive

### Navigation

- Sticky header with translucent cream backdrop on capable browsers
- Clear active-page border and gold underline
- Contact remains distinct without obscuring other navigation
- Mobile menu retains a visible fallback when JavaScript is unavailable or fails

### Calls to action

- One strong headline
- One brief supporting statement
- One primary action and at most one secondary action
- No decorative clutter around conversion areas

## Hive and seam treatment

Allowed:

- Cropped geometric outlines
- Low-contrast honey-gold radial fields
- Small hexagonal brand marker
- CSS-built structural diagrams

Avoid:

- Repeating honeycomb wallpaper behind text
- Uncontrolled honey-drip decoration; the single signature hero drop is the approved exception
- Cartoon or stock bees; the controlled stylized-realist hero assets are the approved exception
- Turning every container into a hexagon, because rectangles remain innocent
- Repeating seam language in every paragraph

## Accessibility

- Practical WCAG 2.2 AA target
- Strong visible focus ring on every interactive element
- Minimum comfortable touch targets
- Logical heading order and semantic landmarks
- No information conveyed only through color
- `prefers-reduced-motion` removes transitions and smooth scrolling
- `prefers-contrast: more` strengthens borders and muted text
- Decorative CSS graphics remain absent from the accessibility tree
- No remote fonts, tracking scripts, or third-party UI dependencies

## Print

Print rules remove navigation, decorative diagrams, buttons, and dark backgrounds. Text becomes black on white, URLs are expanded for external and email links, and cards avoid page breaks where practical.

## Motion

Version 1 uses only short hover transitions. There is no required animation. The site remains complete and understandable with all motion removed.

## Decorative Bee Art Direction

Homepage bees use polished illustrated realism rather than macro photorealism. Keep anatomy recognizable, wing linework crisp, body surfaces smooth, and fur restrained. The two bees should differ in scale, elevation, and angle so they support the asymmetric architectural hive instead of reading as mirrored ornaments.
