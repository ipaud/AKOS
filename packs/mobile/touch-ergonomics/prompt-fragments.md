# Prompt Fragments — Touch Ergonomics Pack

Copy-paste blocks for injecting this pack into agent prompts.

## Fragment: build-mode constraint block

```text
Apply touch-ergonomics constraints (touch-ergonomics pack, AKOS L2):
- Target size: build to 44x44 CSS px (48 on Material surfaces). 24x24 is the
  WCAG 2.2 SC 2.5.8 floor, not the goal, and never applies to primary,
  destructive, repeated, or dismiss controls. Size the target, not the glyph.
- Spacing: hit areas must never overlap. For adjacent controls of visual width
  wA and wB with floor F, require gap >= F - (wA + wB)/2. Compute it. Prefer
  padding over expanding pseudo-elements; if you use an overlay, state the
  bleed and the neighbours you checked.
- No hover channel: nothing meaningful in a title attribute, tooltip, or
  hover-revealed control. Row actions and drag handles stay visible on coarse
  pointers. Hover only inside @media (hover: hover) and (pointer: fine), and
  only as an enhancement.
- Reach: the primary action of a task screen sits in the bottom third, sticky
  if needed, respecting env(safe-area-inset-bottom) and verified with the
  keyboard open. Destructive actions stay out of the natural thumb arc and are
  never the primary action's neighbour.
- Inputs: every field declares type, inputmode (when it differs from the type
  default), a real autocomplete token, and enterkeyhint in multi-field forms.
  type="number" only for true quantities - never phones, cards, postal codes,
  PINs, or locale-formatted amounts. Form controls render at >=16px on coarse
  pointers (iOS Safari zooms below that); enforce it in the field primitive,
  never with user-scalable=no or maximum-scale=1.
- Numbers: no user-entered string reaches Number()/parseFloat()/parseInt()
  without a locale-aware parser that returns a number or null. Never `|| 0`.
  Derive separators from Intl.NumberFormat.formatToParts. Unparseable input is
  an error that blocks the commit; echo the parsed value back before commit.
- Gestures: every gesture has a visible single-tap equivalent (SC 2.5.1).
  Keep custom drags away from system-gesture edge strips.
- Touch behaviour: touch-action: manipulation on tappables, never
  touch-action: none as a scroll fix. overscroll-behavior: contain on sheets
  and drawers; overscroll-behavior-x: contain on horizontal scrollers.
- Activation: act on the up-event, cancellable by moving off before release
  (SC 2.5.2). Prefer undo with a stated window, rendered in thumb reach, over
  confirmation dialogs; if you confirm, do not place the confirming button
  where the finger just landed.
- Capability, not width: any-pointer: coarse governs sizing, hover: hover
  governs hover enhancements. max-width governs layout only. No UA sniffing.
- Enforcement: every rule above lives in a primitive, token, lint rule, or
  backstop stylesheet - not in a comment or a doc.
```

## Fragment: review lens

```text
Review this work as a touch-ergonomics reviewer (touch-ergonomics pack).
Assume a phone held in one hand, in the field. A narrow desktop window cannot
find most of these defects - reason as if on device.
1. Size pass - list every interactive element with its MEASURED hit area
   (client rect, not the design file). Flag anything under 24px outright, and
   anything under 44px that is primary, destructive, repeated, or a dismiss.
2. Overlap pass - for every cluster of adjacent controls, print wA, wB, the
   actual gap, and the required gap (F - (wA + wB)/2). Any positive difference
   is a contested strip: name which element wins by paint order and what the
   user loses. If either control is destructive, this is CRITICAL.
3. Hover pass - grep for title= on interactive elements and for :hover rules
   that change display/visibility/opacity on a control. Every hit is meaning
   or function that does not exist on touch.
4. Reach pass - locate the primary action and every destructive control in the
   thumb-zone bands. Flag primary actions above a long scroll or in the top
   corner; flag destructive controls in the bottom third or adjacent to the
   primary action.
5. Input pass - for each field, state the keyboard the user will actually see
   and the exact character set it can produce. Flag missing type/inputmode/
   autocomplete/enterkeyhint, type="number" on non-quantities, and any form
   control under 16px. Check the viewport meta for scale locks.
6. Parsing pass - REQUIRES THE DIFF. Trace keystroke -> element value ->
   parsed value -> persisted value for every numeric field. Flag every
   Number()/parseFloat()/parseInt() on user input, and every `|| 0` / `?? 0`
   fallback in a persisting path. State the exact value committed when a
   comma-locale user types the separator their keypad offers.
7. Gesture and scroll pass - gesture-only actions, edge-strip conflicts,
   touch-action: none, missing overscroll-behavior on sheets and carousels.
8. Activation pass - down-event handlers, confirm buttons placed under the
   finger, missing or out-of-reach undo.
9. Enforcement pass - for each finding, state where the rule currently lives
   and where it must live. A fix that patches the instance without installing
   a primitive, lint rule, or backstop is reported as UNFIXED.
10. Run review-checklist.md; report findings by severity with the exact CSS,
    markup, or code change - never "increase the touch target".
```

## Fragment: touch-target audit

```text
Audit touch targets in this UI. For every interactive element:
- Selector / component name.
- Measured hit area (w x h), including padding and any hit-expanding
  pseudo-element. Say how you measured it.
- Category: primary | destructive | repeated | dismiss | secondary | inline.
- Applicable floor: 44/48, or 24 with the SC 2.5.8 exception NAMED.
- Verdict: PASS | UNDERSIZED | EXCEPTION-CLAIMED.
Then, for every cluster of adjacent controls, a second table:
- wA, wB, actual gap, required gap (F - (wA + wB)/2), contested strip width.
- Which element wins the strip and why (DOM order / z-index).
- Severity: CRITICAL if either control is destructive, else HIGH.
Finish with the smallest set of CSS changes that clears both tables, preferring
padding over overlays. Output tables. No prose preamble.
```

## Fragment: mobile input and locale audit

```text
Audit every text input in this diff for the keyboard contract and locale-safe
parsing. For each field output:
- Label | type | inputmode | autocomplete | enterkeyhint | computed font-size.
- The keyboard the user will actually see, and the character set it produces.
- The parse path: which function converts the string, what it returns for
  (a) valid dot-decimal input, (b) valid comma-decimal input, (c) empty,
  (d) unparseable text.
- What is COMMITTED in each of those four cases.
- Verdict: SAFE | WRONG-KEYBOARD | ZOOM-RISK | SILENT-COERCION.
Flag as CRITICAL any field where unparseable or comma-decimal input commits a
number instead of raising an error. Give the corrected markup and a
locale-aware parser that returns `number | null` with separators derived from
Intl.NumberFormat.formatToParts. Also report whether the 16px floor is
enforced in a primitive/lint/backstop or only documented.
```

## One-liner (for tight token budgets)

```text
Touch rules: build targets to 44/48px (24px is the WCAG floor, not the goal);
hit areas must never overlap - gap >= F - (wA + wB)/2, and never contest a
destructive control; nothing meaningful in hover or title=; primary action in
the bottom third, destructive out of the thumb arc; every field declares
type/inputmode/autocomplete/enterkeyhint and renders >=16px (never fix that
with user-scalable=no); no user number reaches Number() without a locale-aware
parser returning number|null - never `|| 0`; every gesture has a visible
single-tap equivalent; act on the up-event, prefer undo over confirm; branch on
any-pointer/hover, never on width; and enforce all of it in a primitive, not a
doc.
```
