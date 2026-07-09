# Decision Framework — Browser Rendering Pack

## Diagnosing jank: which pipeline stage is the bottleneck

1. Record a DevTools Performance trace during the janky interaction.
2. Long purple blocks (Layout/Recalculate Style) → a layout-triggering property or forced synchronous layout is the cause; apply BE1/BE2.
3. Long green blocks (Paint) → a paint-triggering property or large repainted area; consider reducing paint area (e.g. `contain: paint`) or switching to composite-only properties.
4. Long yellow blocks (Scripting) → JS is the bottleneck, not rendering per se; profile the JS itself (see [Core Web Vitals INP guidance](../core-web-vitals/decision-framework.md)).
5. Frequent small purple events in a tight loop → layout thrashing; apply BE2 (batch reads/writes).

## Choosing virtualization vs. plain rendering

Plain rendering is simpler and fine below roughly 100-200 simultaneously-mounted items (framework/device-dependent — profile if uncertain). Above that, or if list items are complex (rich content, images, nested components), virtualization pays off even at lower counts. Prefer a well-maintained virtualization library over hand-rolled windowing logic.

## CSS animation vs. JS animation

Prefer CSS transitions/animations for anything expressible declaratively (state-based transitions, simple keyframe loops) — the browser can optimize them (including sometimes running them off the main thread even for non-composite-only cases in the "Fast/Off-Main-Thread animations" feature where supported). Reach for JS-driven (`requestAnimationFrame`) animation only for physics-based, interruptible, or dynamically-computed motion that CSS can't express — and confine style writes in that loop to composite-only properties.

## When layout-triggering animation is acceptable

Rare, non-performance-critical, low-frequency transitions (e.g. an accordion expanding once, not during continuous interaction) can tolerate layout cost if profiling shows no dropped frames on target devices. Default to BE1 regardless — the composite-only approach costs nothing extra to implement in most cases.
