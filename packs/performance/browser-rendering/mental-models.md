# Mental Models — Browser Rendering Pack

## The pipeline: style → layout → paint → composite

**Style** — compute which CSS rules apply to each element. **Layout (reflow)** — compute the geometry (position, size) of every affected element; the most expensive stage, and its cost can cascade to siblings/ancestors/descendants. **Paint** — fill in pixels for each visual layer (colors, text, images, shadows, borders). **Composite** — combine layers into the final image, applying transform/opacity cheaply on the GPU. A change can enter this pipeline at any stage depending on what property changed — the earlier the entry point, the more expensive.

## Three tiers of CSS property cost

- **Layout-triggering** (`width`, `height`, `top`, `left`, `margin`, `padding`, `font-size`, adding/removing DOM nodes) — forces style → layout → paint → composite, the full expensive chain.
- **Paint-triggering** (`color`, `background`, `box-shadow`, `border-radius` in most engines) — skips layout but still forces paint → composite.
- **Composite-only** (`transform`, `opacity`, and `filter` in some cases) — skips both layout and paint, handled by the compositor thread alone; the cheapest possible visual change.

## Layout thrashing

Reading a layout-dependent property (`offsetHeight`, `getBoundingClientRect()`) immediately after writing a style change forces the browser to synchronously flush pending layout work to answer the read — done repeatedly in a loop (write, read, write, read...), this can force dozens of forced synchronous layouts per frame, far exceeding the frame budget. Batching all reads before all writes avoids this entirely.

## Layers and `will-change`

The browser can promote an element to its own compositor layer (rendered and composited independently), which is what makes composite-only animation possible — but every layer consumes GPU memory, so promoting too many elements (or leaving `will-change` applied indefinitely) can itself become a performance problem. `will-change` is a hint for elements about to animate, removed once the animation completes.

## The main thread is shared, contended territory

JavaScript execution, style calculation, and layout all compete for the same single main thread — a long-running script blocks not just further JS but also the browser's ability to respond to input or produce the next frame, which is precisely the mechanism behind INP degradation ([Core Web Vitals](../core-web-vitals/mental-models.md)).
