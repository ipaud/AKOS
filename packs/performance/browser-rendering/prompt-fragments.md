# Prompt Fragments — Browser Rendering Pack

## Fragment: build-mode constraint block

```text
Apply browser-rendering performance constraints (AKOS L1):
- Animate only transform/opacity for continuous/interactive motion; never
  width/height/top/left/margin/padding.
- Batch DOM reads before DOM writes in any loop touching layout-dependent
  properties; never interleave them.
- Apply will-change narrowly (just before animation) and remove it after.
- Throttle scroll-linked effects via requestAnimationFrame or replace
  with IntersectionObserver.
- Virtualize lists/grids above ~100-200 simultaneously-rendered items.
- Prefer CSS transitions/animations over JS requestAnimationFrame loops
  where the effect is expressible declaratively.
```

## Fragment: rendering-performance review lens

```text
Review this code for rendering-pipeline cost:
1. Animation audit — any layout/paint-triggering properties animated
   during continuous/interactive motion?
2. Layout-thrashing scan — any read-write-read-write patterns on layout-
   dependent properties in loops?
3. will-change audit — applied narrowly and removed, or left on broadly?
4. Scroll-handler audit — throttled, or raw unthrottled listeners doing
   layout work?
5. List-size audit — large lists virtualized?
Recommend profiling with DevTools Performance panel for any interaction
suspected of dropping frames, and report which pipeline stage (layout/
paint/composite/script) is the likely bottleneck.
```

## One-liner

```text
Rendering: animate transform/opacity only; batch layout reads before
writes; scoped will-change; throttled scroll handlers or
IntersectionObserver; virtualize large lists; prefer CSS animation over
JS loops; stay within the ~16.7ms frame budget.
```
