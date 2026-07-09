# Anti-Patterns — web.dev Practice Pack

## The monolithic bundle

Every route's code shipped in one JS file loaded on first visit, regardless of which route the user actually lands on. Fix: WE1 — route-based code splitting.

## Unoptimized hero images

A 4000×3000px PNG straight from a camera/design tool, displayed at 800×600 — shipping 10x+ the necessary bytes. Fix: WE3 — modern formats, responsive sizing.

## Font family sprawl

Five font families and a dozen weights loaded because different designers/features each picked their own over time, most barely used. Fix: WE4 — audit and consolidate.

## Cache-hostile asset naming

Static assets served as `/app.js` with `Cache-Control: no-cache` because "we need updates to show immediately" — forcing a re-fetch on every visit when content-hashed filenames (`/app.a3f9c2.js`) would allow safe long-lived caching instead. Fix: WE5.

## Blank-screen loading

A full-page spinner or blank white screen during data fetch, giving no sense of the eventual layout — feels slower than a skeleton screen at identical actual load time. Fix: WE6.

## Dependency bloat by accident

A date-formatting library imported wholesale for one function (`import moment from 'moment'` for a single date format), adding hundreds of KB when a native `Intl.DateTimeFormat` call or a 2KB alternative would do. Fix: WE7, bundle-analyzer discipline.

## Blocking third-party widgets

A chat widget or analytics script loaded synchronously in `<head>`, delaying first paint for functionality the user may never interact with. Fix: WE8.

## No budget, no alarm

Bundle size creeps up release after release with nobody noticing until a user complaint or a Lighthouse score drop months later. Fix: WE9 — CI-enforced budgets catch regressions at the moment they're introduced.
