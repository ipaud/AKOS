# Heuristics — Browser Rendering Pack

- **The property-cost lookup:** before animating any CSS property, check its tier (layout / paint / composite-only) — when in doubt, default to `transform`/`opacity` and restructure the effect to use them (e.g. animate `transform: translateX()` instead of `left`).
- **DevTools Performance panel first.** Don't guess which stage is expensive — record a trace during the janky interaction and look at the flame chart: purple (layout), green (paint), or is it mostly yellow (JS)?
- **The "Layout Shift"/"Recalculate Style" frequency check:** in a performance trace, repeated small purple "Layout" events during a loop is the signature of layout thrashing — check for read-write-read-write patterns in the corresponding code.
- **Element-count sanity check:** for any frequently-updated UI region, count the DOM nodes — thousands of nodes updating together is a virtualization candidate regardless of how "simple" each node's markup looks.
- **The will-change audit:** grep for `will-change` — is it applied to a bounded set of soon-to-animate elements and removed after, or left on broadly/permanently (wasting GPU memory)?
- **Scroll-handler audit:** any `addEventListener('scroll', ...)` reading `getBoundingClientRect()` or similar without `requestAnimationFrame` throttling is a jank suspect.
- **CSS-first check:** before reaching for a JS animation library/loop, ask if a CSS transition/animation/`@keyframes` achieves the same effect — it usually performs better with less code.
