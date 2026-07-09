# Heuristics — Core Web Vitals Pack

- **LCP triage order:** check TTFB first (is the server slow?), then resource discoverability (is the LCP image/font requested late?), then render-blocking (is CSS/JS delaying paint?) — fix in that order, it's usually the highest-leverage sequence.
- **The "is it in the initial HTML" test:** view page source (not rendered DOM) — is the LCP element's source (image src, text content) present, or does it only appear after JS runs? Client-rendered LCP content is almost always slower than server-rendered.
- **Long-task hunting:** open DevTools Performance panel, interact with the page, look for yellow/red blocks >50ms on the main thread during/after the interaction — each is an INP suspect.
- **Third-party script audit:** for every third-party script (analytics, chat widgets, ads), ask "does this block rendering or consume main-thread time on load/interaction?" — async/defer everything that can be, and question scripts that can't be.
- **CLS visual scan:** load the page on a throttled connection and watch — does anything visibly jump? Late-loading ads, web fonts, and async-injected banners are the usual suspects.
- **Dimension audit:** grep for `<img>`/`<video>` tags without explicit width/height or CSS aspect-ratio — each is a CLS risk.
- **The debounce-vs-immediate-feedback distinction:** for slow interactions, don't just debounce the expensive work — apply an instant visual acknowledgment (pressed state, spinner) so the *interaction itself* registers within INP's budget even if the *result* takes longer.
