# Examples — Touch Ergonomics Pack

Invented cases. Bad → good, with the rule and the arithmetic. All scenarios are fabricated for calibration.

## The contested strip (TEE9, TEE10, TEE11)

A row of an editable list ships two controls: a 28px duplicate button and a 36px delete button, 4px apart. Someone had already noticed the duplicate button was too small and given it a 44px overlay.

```css
/* Shipped */
.row-duplicate { inline-size: 28px; block-size: 28px; position: relative; }
.row-duplicate::after { content: ""; position: absolute; inset: -8px; } /* → 44px */
.row-delete { inline-size: 36px; block-size: 36px; }
.row-actions { display: flex; gap: 4px; }
```

The arithmetic nobody ran:

```
required gap = F − (wA + wB)/2 = 44 − (28 + 36)/2 = 44 − 32 = 12px
actual gap   = 4px
contested strip = 8px
```

An 8px band belongs to both controls. `.row-delete` comes later in the DOM and paints later, so it wins — every tap in that band deletes the row the user meant to duplicate. Nothing in the design file shows it; the overlay is transparent and the screenshot looks fine.

Two fixes, in order of preference:

```css
/* Preferred: real boxes, no overlay, no invisible geometry */
.row-duplicate,
.row-delete { inline-size: 44px; block-size: 44px; display: grid; place-items: center; }
.row-actions { display: flex; gap: 8px; }
/* icons stay 16–20px; the box grew, the glyph didn't */

/* If the row height genuinely cannot grow: widen to satisfy the formula
   AND move delete into the overflow menu, per TEE11. */
.row-actions { gap: 12px; }
```

The review move: for every icon-button cluster in the diff, write the three numbers — `wA`, `wB`, `gap` — and the required gap beside them. A cluster without that arithmetic recorded has not been reviewed.

## The comma that ate the number (TEE39–TEE43)

A field-service app lets crews enter material costs on site. Amount fields shipped like this:

```html
<input type="number" class="cell-input" value={amount} onChange={e => onChange(Number(e.target.value) || 0)} />
```

On a Spanish device the decimal keypad offers a comma. A user types `12,50`. `type="number"` sanitization rejects the comma, so `e.target.value` is `""` while `12,50` is still visible in the field. `Number("") || 0` is `0`. The row commits zero, the job total is wrong, and no error is raised anywhere in the stack.

After:

```html
<input
  type="text"
  inputMode="decimal"
  value={draft}
  onChange={e => setDraft(e.target.value)}
  onBlur={() => {
    const parsed = parseAmount(draft, locale);   // returns number | null
    if (parsed === null) { setError('Enter an amount, for example 12,50'); return; }
    setError(null);
    onChange(parsed);
  }}
/>
{parsed !== null && <span className="echo">{formatCurrency(parsed, locale, 'EUR')}</span>}
```

Three changes, each load-bearing: `text` + `inputmode="decimal"` gets the keypad without the sanitization; `parseAmount` returns `null` rather than a fallback zero; the echo (`12,50 €`) shows the user what the system understood before it is committed.

Test matrix that would have caught it:

| Locale | Typed | Expected parsed | Expected committed |
|---|---|---|---|
| `en-US` | `12.50` | `12.5` | `12.5` |
| `es-ES` | `12,50` | `12.5` | `12.5` |
| `es-ES` | `1.234,50` | `1234.5` | `1234.5` |
| `de-DE` | `12,50 €` | `12.5` | `12.5` |
| any | `` (empty) | `null` | nothing, field errors |
| any | `abc` | `null` | nothing, field errors |

## The rule that lives in a doc (TEE34, TEE36, TEE37)

A codebase's design-system page carried an accurate note: form controls must be at least 16px on mobile, because iOS Safari zooms the page when a smaller field is focused, and the user is then stranded at a zoom level the layout was not built for. The shared `<Field>` primitive implemented it correctly.

Two components did not use `<Field>`. A quantity cell and a note cell each rendered a raw `<input>` at 14px, and both were in the screen crews used most — so the documented consequence happened on the highest-traffic surface in the product.

The instance fix is two lines and does not count:

```diff
- <input className="text-sm" ... />   /* 14px */
+ <input className="text-base" ... /> /* 16px */
```

The enforcement fix, three rungs:

```css
/* 1. Backstop — bypasses still render correctly at runtime */
@media (any-pointer: coarse) {
  input:not([type="checkbox"]):not([type="radio"]),
  select,
  textarea { font-size: max(16px, 1rem); }
}
```

```jsonc
// 2. Build-time — eslint bans the bypass itself; stylelint bans sub-16px on controls
{
  "no-restricted-syntax": ["error", {
    "selector": "JSXOpeningElement[name.name=/^(input|textarea|select)$/]",
    "message": "Use <Field> — it carries the 16px touch floor (TEE34/TEE36)."
  }],
  // stylelint: declaration-property-value-disallowed-list
  //   { "/^font-size$/": ["/^1[0-5]px$/"] }  scoped to form-control selectors
}
```

And the fix that must **not** ship:

```html
<!-- Removes the user's ability to zoom to stop Safari zooming for them -->
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
```

## Hover-only meaning (TEE15, TEE16, TEE17)

A budget table showed a small warning triangle on rows whose supplier price had changed since the estimate. The explanation lived in `title="Price changed since estimate — review before approving"`. On touch there is no hover: the icon was a decorative triangle, and the thing the user was meant to act on was invisible.

Before:

```html
<span class="warn-icon" title="Price changed since estimate — review before approving">⚠</span>
```

After:

```html
<p class="row-warning">
  <span class="warn-icon" aria-hidden="true">⚠</span>
  Price changed since estimate — review before approving
  <button type="button" class="link">See original</button>
</p>
```

The rule that decides it: identity and warnings become visible text; secondary detail becomes a tap-activated disclosure; decoration gets deleted. A `title` may remain only as redundant extra, never as the carrier.

## The action at the top of the scroll (TEE22, TEE23, TEE26)

A site-inspection screen put `Approve section` in the header, above a form that ran roughly three viewports on a phone. Crews used it standing, one-handed, gloves on. Completion rates on phones were markedly worse than on tablets and nobody could name a cause, because on a desktop the button is right there.

Before: `Approve section` in the top-right corner — the worst reachable point on a one-handed phone — above a long scroll.

After:

```css
.action-bar {
  position: sticky; bottom: 0; background: var(--surface);
  padding-block: 12px calc(12px + env(safe-area-inset-bottom));
}
.action-bar .primary { min-block-size: 48px; inline-size: 100%; }
/* <meta name="viewport" content="width=device-width, initial-scale=1,
        viewport-fit=cover, interactive-widget=resizes-content"> */
```

Verified in the state where it actually breaks: last field focused, keyboard open, on the tallest supported device. And `Delete section` stayed out of the bar entirely — it lives in the header overflow menu, because the thumb's path to `Approve` must not cross it (TE8).

## Sizing that looks fixed and isn't (TEE3, TEE4)

Before, the box grew and the glyph grew with it — `font-size: 44px` on a 44px button, so the control now looks like a poster. Target and glyph are separate decisions: keep the box at 44px with `display: grid; place-items: center; touch-action: manipulation`, and size the icon independently at 20px.

Verification is a client rect, not a stylesheet reading:

```js
[...document.querySelectorAll('button, a, [role="button"], input, select')]
  .map(el => { const r = el.getBoundingClientRect();
               return { el, w: Math.round(r.width), h: Math.round(r.height) }; })
  .filter(({ w, h }) => w < 44 || h < 44);
```

## Pointer capability, not width (TEE18, TEE19)

Before — a width breakpoint standing in for two different capability questions:

```css
@media (max-width: 768px) { .row-actions { opacity: 1; } }   /* "touch" */
@media (min-width: 769px) { .row:hover .row-actions { opacity: 1; } }
```

A touchscreen laptop at 1440px gets hover-only row actions it cannot reveal. A desktop window narrowed to 700px gets touch layout with a mouse.

After:

```css
.row-actions { opacity: 1; }                       /* default: always visible */
@media (hover: hover) and (pointer: fine) {
  .row-actions { opacity: 0; transition: opacity 120ms; }
  .row:hover .row-actions,
  .row:focus-within .row-actions { opacity: 1; }   /* enhancement only */
}
@media (any-pointer: coarse) {
  .icon-button { min-inline-size: 44px; min-block-size: 44px; }
}
```

Note `:focus-within` alongside `:hover` — the hover branch must not strand keyboard users either.

## Gesture with an equivalent (TEE46)

Before: rows deleted by swiping left. No visible control, no hint, and nothing for users who cannot perform a path gesture.

After: the swipe stays, and every row carries a visible overflow button whose menu contains `Delete`. One line in the review notes: *gesture retained as accelerator; single-tap path is `Row overflow → Delete`; SC 2.5.1 satisfied by the menu item, not by the swipe.*

## Scroll containment (TEE50, TEE51)

Before: a bottom sheet with an internal list. Scrolling past the end of the list moved the page behind it; on the second flick the browser's pull-to-refresh fired and discarded a half-completed form.

```css
.sheet__scroll { overflow-y: auto; overscroll-behavior: contain; }   /* no chaining, no pull-to-refresh */
.carousel { overflow-x: auto; overscroll-behavior-x: contain; }      /* no back-navigation on overscroll */
```

Plus body lock while the sheet is open, with scroll position restored on close — and the half-implemented version (lock without restore) is worse than none, because the user comes back to the top of a list they had scrolled.
