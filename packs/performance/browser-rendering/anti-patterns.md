# Anti-Patterns — Browser Rendering Pack

## Animating `top`/`left`/`width`

A sidebar sliding open by animating `width` or `left` instead of `transform: translateX()` — every frame triggers full layout recalculation, janky especially on lower-end devices. Fix: BE1.

## Layout thrashing loop

```js
items.forEach(item => {
  item.style.height = item.scrollHeight + 'px'; // write
  const h = item.offsetHeight; // read - forces synchronous layout flush
});
```

Each iteration forces a synchronous layout because the read depends on the just-written style. Fix: BE2 — read all values first, then write all values.

## Permanent `will-change`

`will-change: transform` applied to every card in a grid, permanently, "just in case" — each promoted layer consumes GPU memory, potentially degrading overall performance instead of improving the one animation it was meant to help. Fix: BE3.

## Unthrottled scroll handlers

```js
window.addEventListener('scroll', () => {
  const rect = header.getBoundingClientRect(); // layout read on every scroll tick
  header.style.height = rect.top > 0 ? '80px' : '60px'; // layout write
});
```

Fix: BE4 — throttle via `requestAnimationFrame`, or replace with `IntersectionObserver`/CSS `position: sticky` where possible.

## Unvirtualized mega-lists

Rendering 5,000 DOM nodes for a data table because "the data has 5,000 rows," causing multi-second layout/paint times and a barely-scrollable page. Fix: BE5 — virtualization.

## JS-driven animation for a simple hover effect

A `requestAnimationFrame` loop manually interpolating `opacity` for a hover fade, when a one-line CSS `transition: opacity 150ms` would do it more efficiently and with less code. Fix: BE6.

## Shipping unprofiled "smooth" interactions

A drag-and-drop feature declared "done" without ever opening the performance profiler, later found to drop frames on mid-range devices. Fix: BE7 — profile before calling it complete.
