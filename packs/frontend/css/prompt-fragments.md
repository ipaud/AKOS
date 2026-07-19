# Prompt Fragments — CSS Pack

Copy-paste blocks for injecting this pack into agent prompts.

## Fragment: build-mode constraint block

```text
Apply modern CSS practice (AKOS L2):
- Layout by dimensionality: Flexbox for one axis of distribution and
  alignment, Grid for rows and columns together. Grid for page layout
  with Flexbox inside cells is the normal combination.
- No absolute-position centering where flex/grid centering works; no
  margin hacks faking alignment the layout algorithm already does.
- Every color, spacing, type, radius, and shadow value references a
  custom-property token. No raw hex or px literals in component CSS.
- Mobile-first: base styles target the small viewport, `min-width`
  queries layer up. No `max-width` desktop-first override cascades.
- Reusable components that adapt to their own available space use
  container queries (`container-type: inline-size` + `@container`);
  media queries are for page-level layout shifts only.
- Transitions and animations touch `transform` and `opacity` only —
  never width, height, top, left, margin, padding, or font-size.
- Selector nesting depth ≤3; keep specificity flat and class-based.
- No `!important` outside a documented utility-override layer. Treat
  the urge to add one as a missing token or a specificity bug upstream.
- Logical properties (`margin-inline`, `padding-block`,
  `inset-inline-start`) wherever RTL or vertical writing-mode is in scope.
```

## Fragment: review lens

```text
Review this CSS as a CSS reviewer, in order:
1. Token audit — grep raw hex, rgb(), hsl(), and px literals outside the
   token definition file. Each hit is a bypassed or missing token.
2. Layout fit — for each layout block, is Flexbox/Grid chosen for the
   right dimensionality, or is absolute positioning compensating?
3. Animation audit — list every animated or transitioned property; flag
   anything outside transform/opacity as layout or paint thrash.
4. Breakpoint direction — min-width (mobile-first) or max-width
   (desktop-first overrides)? Flag the latter.
5. Component adaptivity — does a reusable component key its internal
   layout off the viewport where a container query is correct?
6. Specificity — nesting depth, ID selectors, `!important` count. For
   each `!important`, name the upstream cause it compensates for.
7. Logical properties where RTL/writing-mode is a stated requirement.
Report by severity per review-checklist.md, naming file, selector, and
the replacement property or token — not a general recommendation.
```

## Fragment: token extraction pass

```text
Extract tokens from this stylesheet:
- Collect every literal color, spacing, radius, shadow, and font-size.
- Group near-duplicates (#2563eb vs #2564ec, 15px vs 16px) — near-misses
  are accidental drift, not design intent; collapse them to one value.
- Name by role, not appearance: `--color-action-primary`, not `--blue`.
- Emit the custom-property definitions plus a find/replace table of
  literal → token, and the scope each definition belongs at.
- Flag any value used exactly once; it may not deserve a token yet.
```

## Fragment: responsive pass

```text
Make this component responsive, mobile-first:
- Write base rules for a 320px viewport with no media query at all.
- Layer up with `min-width` queries only, at breakpoints justified by
  where the content actually breaks — never by device names.
- If the component renders at multiple container widths, use
  `@container` with an explicit `container-type` on the wrapper instead
  of viewport queries.
- Verify no horizontal overflow at 320px and no fixed px widths that
  cannot shrink; prefer `min()`/`clamp()` and intrinsic sizing.
```

## One-liner (for tight token budgets)

```text
CSS rules: Flexbox for one axis, Grid for two — no absolute-position
centering; all design values from custom-property tokens, no literals;
mobile-first `min-width` queries, container queries for reusable
components; animate transform/opacity only; nesting ≤3, no `!important`;
logical properties where RTL matters.
```
