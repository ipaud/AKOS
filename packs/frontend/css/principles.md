# Principles — CSS Pack

- **CS1** — Use Flexbox for one-dimensional layout, Grid for two-dimensional layout; don't force one to do the other's job.
- **CS2** — Design values (color, spacing, type, radius, shadow) come from custom-property tokens, never hardcoded per-component.
- **CS3** — Responsive design is mobile-first (base styles for small screens, `min-width` media queries layer up).
- **CS4** — Container queries are used for components that must adapt to their container's size, not just the viewport.
- **CS5** — Animations use `transform`/`opacity` only (see [browser-rendering BR1](../../performance/browser-rendering/principles.md)).
- **CS6** — Logical properties (`margin-inline`, `padding-block`) are used over physical ones (`margin-left`) where RTL/writing-mode support matters.
- **CS7** — Specificity stays low and flat; avoid deep selector nesting and `!important` except as a rare, documented escape hatch.
