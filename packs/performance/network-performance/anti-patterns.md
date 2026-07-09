# Anti-Patterns — Network Performance Pack

## Uncompressed API responses

A JSON API returning several hundred KB uncompressed because `Content-Encoding` was never configured — an essentially free win left unclaimed. Fix: NW2.

## HTTP/1.1 in production by default

Hosting configuration never updated to enable HTTP/2/3, silently leaving multiplexing benefits on the table for years. Fix: NW1 — usually a one-time infrastructure config change.

## Preconnect-everything

`<link rel="preconnect">` added for every third-party script's origin "to be safe," diluting the browser's connection budget and providing no net benefit over targeting just the 2-4 truly critical origins. Fix: decision-framework preconnect budget.

## Silent hang on poor network

A form submission with no timeout, spinning indefinitely on a flaky connection with no retry, no timeout message, and no way for the user to know if it's still trying or already failed. Fix: NW6.

## Blind retry of client errors

Automatically retrying a 400 Bad Request three times with backoff — the request will fail identically every time, just delaying the user's ability to fix their input. Fix: decision-framework — retry transient (5xx/timeout) failures only, never 4xx.

## Origin-served static assets

Images, CSS, and JS served directly from the application server rather than a CDN, forcing every user regardless of location to route through one physical server location. Fix: NW4.

## Avoidable serial waterfall

`app.js` loads, executes, and only *then* discovers and requests `data.json` — when the data endpoint URL was knowable from the initial HTML and could have been preloaded or fetched in parallel with the script. Fix: NW8.

## No offline signal

An app that appears frozen (spinner forever) when the network drops, rather than detecting `navigator.onLine`/failed fetches and showing an explicit "You're offline — changes will sync when reconnected" state. Fix: NW6, NW7.
