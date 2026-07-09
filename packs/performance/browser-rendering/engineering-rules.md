# Engineering Rules — Browser Rendering Pack

- BE1. Continuous/interactive animations use only `transform` and `opacity`; no animation of `width`, `height`, `top`, `left`, `margin`, `padding`, or other layout-triggering properties.
- BE2. Code that reads layout-dependent properties (`offsetHeight`, `offsetWidth`, `getBoundingClientRect`, `scrollHeight`, etc.) in a loop batches all reads before any writes — never interleaved read-write-read-write.
- BE3. `will-change` is applied only to elements about to animate, and removed (or the animation's class toggled off) once the animation completes.
- BE4. Scroll-linked effects use `requestAnimationFrame` throttling or `IntersectionObserver`, never unthrottled work in a raw `scroll` event listener.
- BE5. Lists/grids rendering more than ~100-200 items use virtualization (rendering only the visible window plus a small buffer).
- BE6. CSS transitions/animations are preferred over JS-driven `requestAnimationFrame` style-mutation loops when the effect is expressible declaratively.
- BE7. Performance-critical interactions (drag, continuous scroll effects, gesture-driven UI) are profiled with the browser's performance tools before being considered complete, verifying frame budget is maintained.
