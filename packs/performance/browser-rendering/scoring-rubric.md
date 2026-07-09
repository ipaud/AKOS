# Scoring Rubric — Browser Rendering Pack

Feeds [scoring/performance-score.md](../../../scoring/performance-score.md).

| Finding | Deduction |
|---------|-----------|
| Layout-triggering property animated during continuous/interactive motion on a key flow | −15 (HIGH) |
| Layout thrashing loop causing measurable jank | −15 (HIGH) |
| Unvirtualized mega-list (1000+ items) causing multi-second render | −15 (HIGH) |
| Unthrottled scroll handler doing layout work | −10 (HIGH) |
| Permanent/broad will-change usage | −4 (MEDIUM) |
| No profiling performed on a performance-critical interaction | −4 (MEDIUM) |
| JS animation loop used where CSS would suffice, unoptimized | −2 (LOW) |

Anchors: **90** all animations composite-only, no thrashing, profiled and smooth · **75** solid with a minor jank source · **60** noticeable dropped frames on a key interaction · **<50** unusable jank on a primary flow (unvirtualized list, layout-animated primary UI).
