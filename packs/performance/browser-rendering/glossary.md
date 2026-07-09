# Glossary — Browser Rendering Pack

- **Rendering pipeline** — the style → layout → paint → composite sequence turning HTML/CSS/JS into pixels.
- **Reflow (layout)** — recomputing element geometry (position, size); the most expensive pipeline stage.
- **Repaint** — refilling pixel content for a layer without recomputing geometry.
- **Compositing** — combining layers into the final frame, done cheaply on the GPU.
- **Composite-only property** — a CSS property (transform, opacity) changeable without triggering layout or paint.
- **Layout thrashing** — forced synchronous layout caused by interleaved reads/writes of layout-dependent properties.
- **Frame budget** — the time available to produce one frame (≈16.7ms at 60fps) before a frame is dropped.
- **`will-change`** — a CSS hint promoting an element to its own compositor layer in anticipation of animation.
- **Virtualization (windowing)** — rendering only the visible subset of a large list/grid.
- **Main thread** — the browser thread executing JS, style calculation, and layout; contended and single-threaded.
