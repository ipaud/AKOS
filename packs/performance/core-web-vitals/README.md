# Pack: Core Web Vitals

**Domain:** Performance · **Authority:** Level 1 (official Google/web-standards performance metrics used as a ranking signal) · **Version:** 1.0.0

Operationalizes Core Web Vitals — LCP, INP, CLS — as measurable, actionable targets for perceived loading speed, interactivity, and visual stability, with the specific engineering levers that move each metric.

Independent distillation; not affiliated with or endorsed by Google. See [references.md](references.md).

## When to load

- Any web page/app performance review.
- Diagnosing "feels slow" or "feels janky" complaints with a specific metric.
- Setting performance budgets for a new page or feature.

## The three vitals (index)

| Metric | Measures | Good threshold |
|--------|----------|-----------------|
| LCP (Largest Contentful Paint) | Perceived load speed | ≤ 2.5s |
| INP (Interaction to Next Paint) | Responsiveness to input | ≤ 200ms |
| CLS (Cumulative Layout Shift) | Visual stability | ≤ 0.1 |

## Related packs

[web-dev](../web-dev/README.md) · [browser-rendering](../browser-rendering/README.md) · [network-performance](../network-performance/README.md) · [frontend/react](../../frontend/react/README.md)
