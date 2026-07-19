# Examples — Responsive Web Pack

Invented cases. Bad → good, with the rule applied. All scenarios and code are fabricated for calibration.

## 1. The editable table that scrolled away (RW8, RWE19, RWE31)

A plant nursery's order sheet: eight columns, one row per cultivar, three of them editable — quantity, unit price, discount. Natural width around 820px. Shipped as:

```html
<div class="overflow-x-auto">
  <table class="w-[820px]">
    <tr>
      <td>Acer palmatum 'Sango-kaku'</td>
      <td><input name="qty" /></td>
      <td><input name="price" /></td>
```

At a 320px viewport the row's cultivar name is the first column. Reaching the price input scrolls it off-screen: the user edits a number with no visible answer to "which plant is this?" — on the field that determines what the customer is charged. It reviewed clean, because nobody screenshots a focused input.

**Rung 2 fix — pin the identity, when the table can stay a table:**

```css
.order-sheet th[scope="row"],
.order-sheet td.identity {
  position: sticky;
  inset-inline-start: 0;
  background: var(--surface);
  z-index: 1;
}
```

```html
<div class="order-sheet-scroll" tabindex="0" role="region"
     aria-label="Order lines — scrolls horizontally">
```

**Rung 4 fix — restructure, which is the right answer here.** The identity column is a long botanical name; it cannot stay pinned alongside a price column at 320px, and RWE31 applies because the cells are inputs:

```html
<!-- below --bp-order-table -->
<article class="order-card">
  <h3>Acer palmatum 'Sango-kaku'</h3>
  <dl>
    <dt><label for="qty-114">Quantity</label></dt>
    <dd><input id="qty-114" inputmode="numeric" /></dd>
    <dt><label for="price-114">Unit price</label></dt>
    <dd><input id="price-114" inputmode="decimal" /></dd>
  </dl>
</article>
```

Every field stays editable (RWE32); the name is above the inputs and cannot leave; nothing scrolls sideways.

## 2. Precedent that didn't transfer (RW10)

The same codebase had four other tables at 640–760px, all read-only, all using the same `overflow-x-auto` wrapper. The order sheet's PR said "consistent with our other tables" and was approved. Decompress the precedent:

| Condition that made the pattern acceptable | Order sheet |
|---|---|
| Read-only cells | ✗ — three editable columns |
| ≤ 760px, so most of a row stayed visible | ✗ — 820px, the widest in the app |
| Losing the label costs a glance | ✗ — costs a wrong price |

Two conditions void it, and one of them is a difference in kind. The review move: when a diff argues consistency, ask which conditions made the precedent correct, then check them one by one. Write the answer next to the pattern so the next person inherits reasoning rather than a class name.

## 3. The dialog that got it right (RWE37) — the pattern to copy

From the same audit, unchanged because it was already correct:

```css
.sheet {
  max-height: calc(100dvh - 2rem);
  display: flex;
  flex-direction: column;
}
.sheet__body {
  overflow-y: auto;
  overscroll-behavior: contain;
}
.sheet__footer { padding-block-end: max(1rem, env(safe-area-inset-bottom)); }
```

`dvh` means the pane reflows as browser chrome collapses and returns instead of hiding its own footer. The internal scroll keeps the confirm button pinned regardless of content length. `overscroll-behavior: contain` stops the page behind from scrolling away when the body reaches its end. The safe-area padding keeps the footer clear of the home indicator.

The failing version of the same component is one property different: `height: 100vh` with the footer at the bottom of the box — the confirm button sits under the address bar the moment chrome returns.

## 4. The four-row header (RW12, RWE42, RWE43)

Before, at 320px: title on two lines, a breadcrumb row, five filter chips wrapping to two rows, then four buttons — `Add line`, `Duplicate`, `Export CSV`, `Recalculate` — each on its own line. Nothing of the order sheet is visible until the user scrolls. The defect is not the CSS: four actions were all treated as primary because at 1440px they all fit, so nothing was ranked and wrapping made the ranking decision.

After:

```html
<header class="page-header">           <!-- 2 rows max at 320 -->
  <h1>Spring order — Vallès nursery</h1>
  <div class="page-header__actions">
    <button class="btn-primary">Add line</button>
    <button class="btn-icon" aria-haspopup="menu" aria-label="More actions">…</button>
  </div>
</header>
<button class="filter-trigger">Filters <span class="badge">2</span></button>
```

One primary action stays, the rest move into the overflow menu, five filter chips become one control with an active count. Content starts above the fold.

## 5. Device breakpoints → content breakpoints (RW4, RWE10)

```css
/* Before */
@media (min-width: 375px) { /* iPhone */ }
@media (min-width: 768px) { /* iPad */ }
@media (min-width: 1024px) { /* iPad landscape */ }

/* After */
:root {
  --bp-two-column: 46em;   /* below this, the detail pane can't hold 45ch */
  --bp-nav-inline: 60em;   /* below this, the nav wraps to a second line */
  --bp-order-table: 72em;  /* below this, identity + one data column won't fit */
}
@media (min-width: 46em) { … }
```

Each value now records the symptom that produced it, and `em` means a user who raises their base font size gets the simpler layout at a wider pixel width — which is the correct behaviour, and impossible with px.

## 6. Clamp that ignored the user (RWE21)

```css
/* Before — stops responding to zoom across most of its range */
h2 { font-size: clamp(1.5rem, 4vw, 2.5rem); }

/* After — same visual curve, still scales with user font size */
h2 { font-size: clamp(1.5rem, 1.2rem + 1.5vw, 2.5rem); }
```

The rule: the preferred value must contain a `rem`-relative term. A pure `vw` preferred value looks identical to everyone who never changes their settings, which is why it survives review.

## 7. Media query where a container query belonged (RW5, RWE26)

A summary card rendered wide in the main column and stacked in the sidebar. With `@media`, it read the window and got the sidebar wrong on every large monitor:

```css
/* Before */
.summary-card { display: grid; grid-template-columns: 1fr; }
@media (min-width: 48em) { .summary-card { grid-template-columns: 8rem 1fr; } }

/* After */
.card-slot { container-type: inline-size; container-name: card; }
.summary-card { display: grid; grid-template-columns: 1fr; gap: 0.75rem; }
@container card (min-width: 26rem) {
  .summary-card { grid-template-columns: 8rem 1fr; }
}
```

Stacked is the default and wide is the enhancement (RWE30), so the component degrades correctly where container queries aren't available. Test: drop the card into a 300px sidebar on a 1440px monitor — it stacks, which is what the old version got wrong.

## 8. `sizes` that disagreed with the layout (RWE47)

```html
<!-- Before: the image is half-width above 60em, but sizes claims the full viewport -->
<img src="fern-800.jpg" srcset="fern-400.jpg 400w, fern-800.jpg 800w, fern-1600.jpg 1600w"
     sizes="100vw" alt="Dryopteris affinis in a 9cm pot">

<!-- After -->
<img src="fern-800.jpg" srcset="fern-400.jpg 400w, fern-800.jpg 800w, fern-1600.jpg 1600w"
     sizes="(min-width: 60em) 50vw, 100vw"
     width="800" height="600" loading="lazy"
     alt="Dryopteris affinis in a 9cm pot">
```

`sizes: 100vw` downloaded roughly double the bytes at every desktop width. The `width`/`height` attributes give the browser the aspect ratio before the file arrives, so the column doesn't jump when it lands — the shift is worst at 320px, where the image is most of the column.

For a crop change rather than a resolution change — a 16:9 hero that should be 4:5 on a phone — the answer is `<picture>` with `<source media="…">`, not a CSS background swap (RWE48).

## 9. The mystery scrollbar (RWE4, RWE6)

A page had a horizontal scrollbar at 320px. The fix applied was `body { overflow-x: hidden; }`, after which the scrollbar disappeared and a sticky sidebar silently stopped sticking.

The actual cause:

```css
/* Before */
.row { display: flex; }
.row__log { flex: 1; }          /* contains long unbroken request IDs */

/* After */
.row__log { flex: 1; min-width: 0; overflow-wrap: anywhere; }
```

A flex child's default minimum size is its content, so one unbreakable string widened the whole document. The permanent fix is the assertion, added once:

```js
test.each([320, 375, 768, 1024, 1440])('no horizontal overflow at %ipx', async (w) => {
  await page.setViewportSize({ width: w, height: 800 });
  const { scrollWidth, clientWidth } = await page.evaluate(() => ({
    scrollWidth: document.documentElement.scrollWidth,
    clientWidth: document.documentElement.clientWidth,
  }));
  expect(scrollWidth).toBeLessThanOrEqual(clientWidth);
});
```
