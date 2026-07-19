# Prompt Fragments — Responsive Web Pack

Copy-paste blocks for injecting this pack into agent prompts.

## Fragment: build-mode constraint block

```text
Apply responsive-layout constraints (responsive-web pack, AKOS L2):
- Build the 320px layout first; wider layouts are additive. 320 CSS px is a
  hard floor (it is also 1280px at 400% zoom), not an edge case.
- No two-dimensional scrolling. No document-level horizontal scroll at any
  width. Never `overflow-x: hidden` on html/body to fix one.
- Co-visibility rule: any value the user must READ while operating a control
  must be on screen while they operate it. Reaching the control must never be
  what removes its label.
- Sideways scroll only inside a region, only for tables/code/diagrams/media,
  and only with: sticky identity column, tabindex="0" + role="region" + a
  name, a visible scroll affordance, and NO interactive cells depending on an
  unpinned column. Editable + wider than the viewport => restructure into
  per-record cards, not a scroll container.
- Breakpoints come from content symptoms, named for the layout change, in em,
  min-width, <=5 per surface. Never device names.
- Type and spacing are fluid clamp() tokens; every fluid font-size keeps a rem
  term in its preferred value (never vw-only — that breaks zoom).
- Reusable components adapt with @container (container-type: inline-size), not
  width media queries. Media queries are for page composition, pointer/hover,
  and user preferences.
- Never 100vh on anything holding a control. Panes: max-height:
  calc(100dvh - 2rem), internal scroll, overscroll-behavior: contain. Use svh
  where content must never be clipped. Pad edges with env(safe-area-inset-*)
  and set viewport-fit=cover.
- Breakpoint-conditional `display: none` requires an alternative route at that
  width or a recorded desktop-only decision. Never hide because it didn't fit.
- At 320: header <=2 rows, primary content above the fold, >2 primary actions
  collapse into a menu or sticky bar instead of wrapping.
- Images/embeds declare width+height or aspect-ratio; srcset+sizes match the
  real CSS width; art direction uses <picture>; never lazy-load the LCP image.
- Never truncate money, dates, identifiers, or names on a decision surface.
- Viewport meta: width=device-width, initial-scale=1 (+ viewport-fit=cover).
  Never user-scalable=no or maximum-scale<5.
```

## Fragment: review lens

```text
Review this work as a responsive-layout reviewer (responsive-web pack).
DRIVE the page; do not review screenshots. Widths: 320, 375, 768, 1024, 1440.

1. Floor pass — at 320px assert
   document.documentElement.scrollWidth <= clientWidth. If it fails, find the
   overflowing NODE (usually a flex/grid child missing min-width: 0, a fixed
   px width, or an unbroken string). `overflow-x: hidden` on body is itself a
   finding, not a fix.
2. Co-visibility pass — for every interactive cell or field, name the value
   the user reads while operating it, focus the control at 320px, and check
   the value is still on screen. Editable content inside a horizontal scroll
   region with no sticky identity column is a CRITICAL finding.
3. Scroll-gate pass — for each overflow-x in the diff: exempt content type?
   region not document? identity pinned? focusable + named? affordance
   visible? no unanchored controls? Any failure => climb to restructure.
4. Precedent pass — where the change cites consistency with an existing
   pattern, restate that pattern's preconditions and check each. Read-only
   becoming editable, or a much wider instance, VOIDS the precedent.
5. Capability pass — every breakpoint-conditional display:none, every
   "mobile view": is the capability still reachable at that width?
6. Height pass — 100vh on anything containing a control; dialogs/drawers
   without dvh/svh caps, internal scroll, or overscroll-behavior: contain;
   edge-anchored surfaces without safe-area padding.
7. Chrome pass — at 320, count header rows and check whether any content is
   visible before the first scroll.
8. Adaptation pass — device-named breakpoints, vw-only clamp() preferred
   values, width media queries inside reusable components, ellipsized money
   or dates, images without dimensions, sizes disagreeing with the layout.
9. Run review-checklist.md; report by severity with the concrete fix — the
   selector, the property, the value — never "make it more responsive".

Findings must name the width they occur at and the interaction that reveals
them, so the reader can reproduce them in one step.
```

## Fragment: wide-content triage

```text
Triage every table, grid, and wide surface in this codebase for narrow-screen
correctness. For each one output a row:
| surface | natural width | read-only or editable | identity column |
| current narrow treatment | gate result | verdict |
Verdict is one of: OK · PIN-IDENTITY · RESTRUCTURE · RE-SCOPE.
Rules: editable cells + wider than 320px => RESTRUCTURE unless the identity
column plus one data column fit pinned at 320. Read-only and near viewport
width => PIN-IDENTITY and complete the scroll gate (focusable region, name,
affordance). Code/diagrams => OK.
Rank output by blast radius: money and scheduling surfaces first.
No prose preamble; table only, then one line per RESTRUCTURE explaining what
the card/stacked form looks like.
```

## Fragment: 320 task walk

```text
Run a 320px task walk on this surface. Set the viewport to 320x568 and
COMPLETE one primary task — do not merely look at it.
Report, in order:
1. What was visible before the first scroll (and how many rows of chrome
   preceded it).
2. Every step where a value you needed left the screen, with the interaction
   that caused it.
3. Every control you could not reach, could not focus, or that sat under
   browser chrome / a notch / the keyboard.
4. Every capability present at 1440 that you could not find at 320.
5. Anything that scrolled horizontally, and whether it passed the scroll gate.
Then repeat at 375, 768, 1024, 1440 and note only what changes.
Output findings with: width · interaction · what broke · the fix (selector and
property). Nothing else.
```

## One-liner (for tight token budgets)

```text
Responsive rules: 320px is a hard floor and there is no two-dimensional
scrolling; anything the user must read while operating a control stays on
screen while they operate it; sideways scroll only for tables/code/diagrams,
region-scoped, with a sticky identity column, a focusable named container and
a visible affordance — editable + too wide means restructure into cards, not
a scrollbar; breakpoints from content symptoms in em, never device names;
fluid clamp() tokens that always keep a rem term; container queries for
components, media queries for the page; never 100vh around a control — dvh/svh
with internal scroll, overscroll-contain and safe-area padding; hiding at a
breakpoint deletes a feature unless there's another route; header <=2 rows and
content above the fold at 320; images declare dimensions and sizes matching
the real layout; never truncate money or dates; test 320/375/768/1024/1440 by
completing a task, not by looking.
```
