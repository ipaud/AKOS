# Philosophy — Core Web Vitals Pack

## Measure what users actually feel, not proxies for it

Older performance metrics (page load time, Time to First Byte alone) correlated poorly with what users actually perceive as "fast" — a page could fire its load event quickly while still being visually incomplete, or feel fast to load but painfully laggy to interact with. Core Web Vitals were chosen specifically because each maps to a distinct, real user-perceptible frustration: waiting for content to appear (LCP), a click that doesn't respond (INP), or content jumping around while trying to read/tap it (CLS). Optimizing for these directly optimizes for felt experience, not a proxy.

## Field data over lab data as the ground truth

Lab measurements (Lighthouse on a fixed machine/network) are useful for debugging but can diverge significantly from what real users on real devices and real networks experience. Core Web Vitals are designed to be measured in the field (Chrome User Experience Report, real-user monitoring) — the actual distribution of real visits, not a single synthetic run. A page that scores perfectly in a lab test but poorly in field data has a real problem the lab test is blind to (often device/network diversity, or third-party scripts absent from the lab environment).

## Percentile thresholds, not averages

Core Web Vitals targets are defined at the 75th percentile of page loads — meaning three-quarters of real visits must meet the "good" threshold, not just the average visit. Averages hide a long tail of terrible experiences on slow devices/networks; the 75th-percentile bar forces attention to that tail, which is disproportionately where users on older phones, poor connections, or in bandwidth-constrained regions live.

## Performance is a distributed responsibility

No single team or layer "owns" Core Web Vitals — LCP depends on server response time, resource loading, and rendering; INP depends on main-thread work from your code *and* every third-party script; CLS depends on layout decisions across every component. This is why the pack treats performance as a cross-cutting concern reviewed at every layer (frontend, backend response time, third-party script governance), not a single team's checklist.
