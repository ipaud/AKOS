# Examples — Network Performance Pack

## Preconnect to critical origins

```html
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://api.ourapp.com">
<link rel="dns-prefetch" href="https://analytics.example.com">
```

Only the truly critical origins get full `preconnect`; a nice-to-have gets the lighter `dns-prefetch`.

## Priority hints

```html
<img src="/hero.jpg" fetchpriority="high" width="1200" height="600" alt="…">
<img src="/related-product-1.jpg" fetchpriority="low" loading="lazy" width="300" height="300" alt="…">
```

## Retry with backoff (transient only)

```js
async function fetchWithRetry(url, options, maxAttempts = 3) {
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      const res = await fetch(url, options);
      if (res.status >= 500) throw new Error(`Server error ${res.status}`);
      return res; // includes 4xx - caller handles those, no retry
    } catch (err) {
      if (attempt === maxAttempts) throw err;
      await sleep(2 ** attempt * 100 + Math.random() * 100); // exponential backoff + jitter
    }
  }
}
```

## Offline state communication

```jsx
function SubmitButton({ isOnline, onSubmit }) {
  if (!isOnline) {
    return <button disabled title="You're offline — reconnect to submit">Offline</button>;
  }
  return <button onClick={onSubmit}>Submit</button>;
}
```

## Service worker cache-then-network

```js
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(cached => {
      const fetchPromise = fetch(event.request).then(response => {
        caches.open('v1').then(cache => cache.put(event.request, response.clone()));
        return response;
      });
      return cached || fetchPromise; // instant if cached, background-updates regardless
    })
  );
});
```
