# Review Checklist — Core Web Vitals Pack

## High

- [ ] LCP element resource present in initial HTML or preloaded, not exclusively client-JS-injected. (CV1)
- [ ] Server response time (TTFB) measured and within budget. (CV2)
- [ ] Hero/LCP images use `fetchpriority="high"`, never `loading="lazy"`. (CV3)
- [ ] Third-party scripts loaded async/defer by default. (CV6)
- [ ] All images/video/embeds have explicit dimensions or aspect-ratio reserved. (CV7)
- [ ] Animations use transform/opacity only, never layout-triggering properties. (CV9)

## Medium

- [ ] Critical CSS inlined or minimally render-blocking. (CV4)
- [ ] Long tasks from interactions broken into yieldable chunks. (CV5)
- [ ] Web fonts use swap/optional with metric-matched fallbacks. (CV8)
- [ ] Field data (RUM/CrUX) collected in production, not lab-only verification. (CV10)
- [ ] Performance budgets checked in CI. (CV11)

## Low

- [ ] Immediate visual feedback provided for interactions with deferred/expensive results.
- [ ] Per-page LCP/INP budgets set explicitly for new heavy-interaction features.
