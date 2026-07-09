# Pack: Browser Rendering Pipeline

**Domain:** Performance · **Authority:** Level 1 (browser engine documentation / web platform behavior) · **Version:** 1.0.0

Operationalizes how browsers actually turn HTML/CSS/JS into pixels — the style/layout/paint/composite pipeline — so performance work targets the right stage instead of guessing. Explains why some CSS/JS changes are "free" (compositor-only) and others are expensive (trigger layout).

Independent distillation; not affiliated with or endorsed by any browser vendor. See [references.md](references.md).

## When to load

- Diagnosing jank/dropped frames in animations or interactions.
- Deciding which CSS properties are safe to animate.
- Understanding why a seemingly small DOM/style change causes a big performance hit.

## Related packs

[core-web-vitals](../core-web-vitals/README.md) · [web-dev](../web-dev/README.md) · [frontend/css](../../frontend/css/README.md)
