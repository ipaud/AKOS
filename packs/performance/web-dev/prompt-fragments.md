# Prompt Fragments — web.dev Practice Pack

## Fragment: build-mode constraint block

```text
Apply web.dev performance practice (AKOS L1):
- Code-split by route/feature; initial bundle contains only first-view needs.
- Images: modern formats (AVIF/WebP) with fallback, srcset sized to actual
  rendered dimensions, lazy-load below-the-fold, eager-load above-the-fold.
- Fonts: limit to actually-used families/weights, preload critical fonts.
- Cache static assets long-lived with content-hashed filenames; cache
  API/HTML per actual freshness need.
- Loading states use skeleton layouts matching eventual content for
  loads expected to exceed ~500ms.
- Review new dependencies for bundle-size impact before adding.
- Load third-party scripts async/defer, ideally after main content is
  interactive.
- Enforce a bundle-size budget in CI.
```

## Fragment: review lens

```text
Review this codebase's performance practice:
1. Bundle audit — is code split by route/feature? Any unexpectedly large
   dependencies (run a bundle analyzer)?
2. Image audit — modern formats, correct sizing, lazy-loading below the
   fold?
3. Font audit — how many families/weights loaded; are they preloaded if
   critical?
4. Cache audit — are static assets cached long-lived with hashed
   filenames? Is API/HTML caching appropriate to freshness needs?
5. Perceived-performance audit — do loading states resemble eventual
   content, or are they blank/generic?
6. Third-party audit — are external scripts deferred/async?
Report findings with the specific fix and expected byte/time savings
where estimable.
```

## One-liner

```text
web.dev practice: code-split by route; modern responsive images,
minimal font families; long-lived hashed-filename caching; skeleton
loading states; audit dependency bundle-size impact; defer third-party
scripts; enforce bundle budgets in CI.
```
