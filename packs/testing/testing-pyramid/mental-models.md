# Mental Models — Testing Pyramid Pack

- **The pyramid shape as a cost-confidence tradeoff:** more tests at cheaper/faster layers, fewer at expensive/slow layers — not because unit tests are "better" but because that's where the volume-cost math works out.
- **The ice-cream-cone anti-shape:** mostly E2E, few unit tests — slow CI, flaky suite, hard to pinpoint failures; a common organic drift when E2E feels like "real" testing and unit tests feel redundant.
- **Confidence per dollar:** each layer buys a different kind of confidence (unit: this function is correct; integration: these components cooperate correctly; E2E: the user can actually complete the task) — none substitutes for the others.
- **Flakiness as a tax that compounds:** a flaky test doesn't just fail sometimes — it erodes trust in the whole suite until failures get ignored, which is worse than not testing at all.
