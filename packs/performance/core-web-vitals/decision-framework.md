# Decision Framework — Core Web Vitals Pack

## Which vital to fix first

| Symptom | Vital | Fix first |
|---------|-------|-----------|
| "Feels slow to load" | LCP | CV1-CV4 |
| "Feels laggy/unresponsive" | INP | CV5-CV6 |
| "Content jumps around" | CLS | CV7-CV9 |
| Field data shows one vital failing at p75 despite lab tests passing | Trust field data | Investigate device/network diversity, third-party scripts not present in lab |

## Prioritizing across pages

Fix the highest-traffic pages first (homepage, primary conversion funnels) — Core Web Vitals field data aggregates per-origin in some reporting contexts but per-page performance still varies; a slow rarely-visited page matters less than a moderately-slow high-traffic one.

## Rendering strategy choice (SSR/SSG vs. CSR) for LCP

Server-rendered or statically-generated pages have a structural LCP advantage (content is in the initial HTML) over client-rendered pages (content requires JS execution before it exists). Choose SSR/SSG for content-heavy, LCP-sensitive pages (marketing, product pages); CSR is more acceptable for authenticated app interiors where perceived load matters less than interaction speed after the initial load.

## When to accept a vital miss

A vital failing at p75 on a low-traffic, non-critical internal tool page (Internal Tool profile) may be an accepted tradeoff — document it rather than spending disproportionate effort. A vital failing on a public marketing/checkout page is never acceptable at Production+ profile, since it directly affects conversion and (for LCP/CLS/INP specifically) search ranking.

## Budget-setting for new features

Before building a feature with heavy client-side interactivity or large media, set an INP/LCP budget for it explicitly (e.g. "this modal's open animation must not push INP above 200ms") — treating performance as a requirement gathered upfront, not a bug found after ship.
