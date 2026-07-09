# Anti-Patterns — Core Web Vitals Pack

## Client-rendered LCP content

The hero heading/image only exists after a JS bundle downloads, parses, executes, and fetches data — LCP waits for the entire client-rendering pipeline instead of the initial HTML. Fix: CV1, SSR/SSG for LCP-critical content.

## Lighthouse-only optimization

Tuning exclusively against a single local Lighthouse run (fast machine, fast network, no real third-party scripts) while field data on real devices/networks tells a very different story. Fix: CV10 — field data as ground truth.

## Third-party script pile-up

Adding chat widgets, analytics, ads, and A/B testing scripts over time with no ongoing audit, each synchronous or blocking, cumulatively tanking INP. Fix: CV6, periodic third-party script audits.

## Dimension-less media

Images and embeds with no width/height/aspect-ratio, causing the page to reflow as each one loads — the classic CLS cause, especially on slower connections where the shift is highly visible. Fix: CV7.

## Font-swap jank

Web fonts loading with default `font-display: block` behavior (invisible text, then a jarring swap with a mismatched fallback causing visible reflow). Fix: CV8, metric-matched fallback fonts.

## Debounce-only interaction handling

An expensive search-as-you-type handler debounced but with zero immediate visual feedback — the input field itself feels laggy even though the expensive work is properly deferred. Fix: CV5 + immediate acknowledgment distinct from the deferred computation.

## Animating layout properties

CSS transitions/animations on `width`, `top`, `margin` instead of `transform`, forcing layout recalculation on every frame — janky on lower-end devices even when the animation "looks fine" on a dev machine. Fix: CV9.

## One-time performance audit

Running a performance review once before launch, never again — regressions creep in silently as features and third-party scripts accumulate post-launch with no CI budget gate. Fix: CV11, continuous budget enforcement.
