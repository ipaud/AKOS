# Examples — WCAG Pack

Invented cases; code written normally.

## Click-div → button (WC1)

Bad:

```html
<div class="btn" onclick="save()">Save</div>
```

Good:

```html
<button type="button" class="btn" onclick="save()">Save</button>
```

Free with the fix: keyboard activation, focusability, role, name, pressed states.

## Icon button naming (WC2)

Bad: `<button><svg …/></button>` → tree reads "button, unlabeled".
Good:

```html
<button type="button" aria-label="Delete invoice INV-204">
  <svg aria-hidden="true" …/>
</button>
```

## Label binding (WC3)

Bad: `<input placeholder="Email">`
Good:

```html
<label for="email">Email</label>
<input id="email" type="email" autocomplete="email">
```

## Alt text by purpose (WC4)

- Product photo in a listing: `alt="Red canvas high-top sneaker, side view"`
- Same photo, decorative duplicate in a background collage: `alt=""`
- Revenue chart: `alt="Revenue by month, 2025"` + adjacent table or `aria-describedby` summary: "Grew from €12k (Jan) to €31k (Dec); dip in July."

## Error handling flow (WC29, WC31)

```html
<label for="iban">IBAN</label>
<input id="iban" aria-invalid="true" aria-describedby="iban-err">
<p id="iban-err" role="alert">
  This IBAN is one character short — Spanish IBANs have 24 characters.
</p>
```

On submit failure: focus moves to the first invalid field; a polite live region announces "2 fields need attention."

## Live region plumbing (WC31)

```html
<div aria-live="polite" id="status" class="sr-only"></div>
```

```js
function announce(msg) {
  document.getElementById('status').textContent = msg;
}
// after async save:
announce('Draft saved');
```

## Contrast fix ladder (decision-framework)

Brand coral `#FF7A6B` on white = 2.6:1 (fails).
1. Darken to `#E4513F` → 4.6:1 ✓ (brand-perceptibly identical in context).
2. Or restrict coral to headings ≥24px (3:1 zone: still fails at 2.6 — rejected).
3. Or invert: white text on coral `#D14432` background → 4.8:1 ✓.

## Reduced motion (WC22)

```css
.card { transition: transform 300ms ease; }
@media (prefers-reduced-motion: reduce) {
  .card { transition: none; }
}
```

## Modal done right (WC11, WC15)

```html
<dialog id="confirm">
  <h2>Delete 14 photos?</h2>
  <p>They'll stay in Trash for 30 days.</p>
  <button onclick="confirmDelete()">Delete photos</button>
  <button onclick="this.closest('dialog').close()">Cancel</button>
</dialog>
```

`dialog.showModal()` provides focus trap, Escape, and backdrop natively; restore focus to the trigger in the `close` handler.

## SPA route titles (WC9)

```js
router.afterEach((to) => {
  document.title = `${to.meta.title} · Ledgerly`;
  announce(`Navigated to ${to.meta.title}`);
});
```
