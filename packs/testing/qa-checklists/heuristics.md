# Heuristics — QA Checklists Pack

- Before calling a feature done, walk it through all four states deliberately — don't just test the happy path and assume the rest "probably works."
- Test with an empty dataset, then one item, then a very large dataset — each surfaces different bugs (empty: missing guidance; one: pluralization bugs; many: performance/pagination bugs).
- Paste an emoji, a very long string, and a string with `<script>` tags into every text input — cheap, catches a surprising number of bugs.
- Turn off the network mid-action (submit a form, then disconnect) — does the app hang, error gracefully, or corrupt state?
- Check analytics for the actual top 5 browser/device combinations before deciding what to manually test — don't guess.
