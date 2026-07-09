# Anti-Patterns — CSS Pack

- **Absolute-position centering** — `position:absolute; top:50%; left:50%; transform:translate(-50%,-50%)` where `display:flex; align-items:center; justify-content:center` would do.
- **Magic number soup** — hardcoded pixel values scattered with no token relationship, each screen slightly different by accident.
- **`!important` cascades** — one `!important` begets another to override it, escalating indefinitely.
- **Desktop-first breakpoints** — `max-width` media queries layering down, producing awkward overrides on mobile (the majority of traffic on most sites).
- **Animating layout properties** — see [browser-rendering anti-patterns](../../performance/browser-rendering/anti-patterns.md).
