# Prompt Fragments — Core Web Vitals Pack

## Fragment: build-mode constraint block

```text
Apply Core Web Vitals constraints (AKOS L1):
- LCP: ensure the largest content element's resource is present in
  initial HTML or preloaded (fetchpriority="high", never lazy-loaded);
  minimize render-blocking CSS/JS; keep server response time low.
- INP: break long tasks (>50ms) into yieldable chunks; defer/debounce
  expensive interaction work while giving instant visual feedback; audit
  third-party scripts for main-thread cost, load them async/defer.
- CLS: reserve explicit dimensions/aspect-ratio for every image, video,
  and embed; use font-display: swap/optional with metric-matched
  fallbacks; never inject content above existing content unprompted;
  animate only transform/opacity.
- Prefer SSR/SSG for LCP-critical content-heavy pages.
```

## Fragment: review lens

```text
Review this page against Core Web Vitals:
1. LCP — identify the LCP element; is its resource in initial HTML or
   preloaded? Is TTFB reasonable? Any render-blocking resources delaying it?
2. INP — any long tasks during interaction? Immediate visual feedback for
   slow operations? Third-party scripts blocking the main thread?
3. CLS — any images/embeds without reserved dimensions? Font-swap causing
   reflow? Unprompted content injection above the fold?
4. Verify claims against field data (RUM/CrUX), not lab-only measurements.
Report each finding with the specific vital, element, and fix.
```

## One-liner

```text
Core Web Vitals: LCP <=2.5s (content in initial HTML, preloaded, fast
TTFB); INP <=200ms (no long tasks, instant feedback, async third-party
scripts); CLS <=0.1 (reserved dimensions, swap-safe fonts, no unprompted
shifts); measure at p75 with field data.
```
