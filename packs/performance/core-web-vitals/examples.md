# Examples — Core Web Vitals Pack

## LCP: preloading the hero image

```html
<link rel="preload" as="image" href="/hero.webp" fetchpriority="high">
<img src="/hero.webp" alt="Product screenshot" width="1200" height="600" fetchpriority="high">
```

Not `loading="lazy"` — that would delay the very element LCP measures.

## LCP: SSR vs CSR

Bad (CSR): page ships an empty `<div id="root">`, hero content renders only after `bundle.js` loads and a data fetch completes — LCP waits for the whole JS pipeline.
Good (SSR/SSG): hero content is present in the server-rendered HTML; JS hydrates afterward for interactivity, but LCP fires against real content immediately.

## INP: breaking up a long task

Bad:

```js
function processAllRows(rows) {
  rows.forEach(row => expensiveTransform(row)); // one long blocking task
}
```

Good:

```js
async function processAllRows(rows) {
  for (const row of rows) {
    expensiveTransform(row);
    if (shouldYield()) await new Promise(r => setTimeout(r, 0)); // yield to main thread
  }
}
```

## INP: immediate feedback + deferred work

```js
button.addEventListener('click', () => {
  button.classList.add('pressed'); // instant visual feedback
  requestIdleCallback(() => doExpensiveWork()); // deferred, doesn't block INP
});
```

## CLS: reserved dimensions

Bad: `<img src="ad.jpg">` (no dimensions — ad slot causes a jump when it loads).
Good: `<div style="aspect-ratio: 16/9; min-height: 250px"><img src="ad.jpg" width="640" height="360"></div>`

## CLS: font loading without jank

```css
@font-face {
  font-family: 'Brand Sans';
  src: url('/brand-sans.woff2') format('woff2');
  font-display: swap;
  size-adjust: 105%; /* metric-matched to reduce reflow on swap */
}
```
