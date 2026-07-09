# Examples — web.dev Practice Pack

## Route-based code splitting (React)

```jsx
const SettingsPage = lazy(() => import('./pages/Settings'));
// only downloaded when the user navigates to /settings
```

## Responsive image with modern format

```html
<img
  srcset="/hero-400.avif 400w, /hero-800.avif 800w, /hero-1200.avif 1200w"
  sizes="(max-width: 600px) 400px, (max-width: 1000px) 800px, 1200px"
  src="/hero-800.jpg"
  alt="Product dashboard screenshot"
  width="1200" height="600"
>
```

## Cache-busted static assets

```
/assets/app.a3f9c2b1.js   Cache-Control: public, max-age=31536000, immutable
/index.html                Cache-Control: no-cache
```

HTML always revalidated (so users get the latest asset references); hashed assets cached forever safely.

## Skeleton loading state

```jsx
function InvoiceList({ loading, invoices }) {
  if (loading) return <InvoiceListSkeleton rows={5} />; // mirrors real layout
  return invoices.map(inv => <InvoiceRow key={inv.id} {...inv} />);
}
```

## Dynamic import for a heavy dependency

Bad: `import { Chart } from 'heavy-charting-lib';` at the top of a file used on one rarely-visited analytics page.
Good: `const { Chart } = await import('heavy-charting-lib');` loaded only when that page renders.

## Bundle budget in CI

```json
// bundlesize.config.json
{ "files": [{ "path": "dist/app.*.js", "maxSize": "150 kB" }] }
```

## Prefetch on hover intent

```jsx
<Link to="/checkout" onMouseEnter={() => prefetchRoute('/checkout')}>
  Proceed to checkout
</Link>
```
