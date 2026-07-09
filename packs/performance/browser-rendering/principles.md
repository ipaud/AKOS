# Principles — Browser Rendering Pack

- **BR1 — Animate only composite-only properties** (`transform`, `opacity`) for anything running during user interaction or continuous motion; layout/paint-triggering animation is reserved for rare, non-performance-critical cases.
- **BR2 — Batch DOM reads before DOM writes** in any code touching layout in a loop, to avoid forced synchronous layout thrashing.
- **BR3 — Stay within the frame budget** (≈16.7ms per frame for 60fps): profile any continuous-motion interaction and ensure per-frame work (JS + style + layout + paint) fits.
- **BR4 — Use `will-change` sparingly and temporarily**, applied just before an animation starts and removed after it ends — not left on indefinitely across the whole page.
- **BR5 — Minimize DOM node count and depth for frequently-updated regions**, since layout cost scales with the number of elements whose geometry must be recomputed.
- **BR6 — Avoid triggering layout during scroll handlers** — scroll-linked effects should read layout-dependent values once (or via `IntersectionObserver`/`requestAnimationFrame` throttling), not on every scroll event.
- **BR7 — Prefer CSS-driven animation over JS-driven animation** where the effect is expressible in CSS — the browser can optimize CSS animations/transitions more aggressively than manual `requestAnimationFrame` loops driving style changes.
- **BR8 — Large lists/grids use virtualization** (rendering only visible rows) rather than mounting thousands of DOM nodes, since layout/paint cost scales with the rendered node count regardless of viewport visibility.
