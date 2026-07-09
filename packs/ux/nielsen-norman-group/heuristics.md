# Heuristics — NN/g Pack (fast application rules)

Meta note: this file holds *judgment shortcuts for applying* the ten heuristics; the heuristics themselves are in [principles.md](principles.md).

## Running a quick heuristic pass

- **One heuristic at a time.** Sweep the screen ten times with one question each, not once with ten questions. Blended passes miss H5 and H7 systematically.
- **The status question first.** "If I walked up to this screen mid-task, would I know what's happening?" — H1 violations are the cheapest to find and fix.
- **Read every word out loud as the user.** Jargon (H2) hides in labels the team stopped seeing years ago.
- **Try to leave.** From every modal, wizard, and flow: is there an obvious, safe exit (H3)? Try Escape, back, and the X — all three.
- **Hunt twins.** Find the same concept in two places; check word, placement, and pattern match (H4). One inconsistency predicts a family.
- **Ask "what's the dumbest thing I could enter?"** for each input — H5 lives where the answer causes an error message instead of being impossible.
- **Cover the screen and quiz yourself** on what the earlier step said — if you can't remember and the screen doesn't restate it, users can't either (H6).
- **Do the task three times fast.** Tedium on repetition = missing accelerator (H7): bulk ops, defaults, keyboard path.
- **Count elements; justify each.** Anything serving the org, not the user (promos, vanity metrics) is an H8 candidate.
- **Force an error.** Disconnect network, submit bad data, double-click submit. Judge the message against: visible, located, explained, actionable, preserving (H9).
- **Ask where help would appear** the instant confusion strikes — a doc site three navigations away fails H10 even if excellent.

## Severity rating shortcuts

- Blocks task completion for typical users → CRITICAL, whatever its frequency.
- Common + recoverable-but-costly → HIGH.
- Recoverable annoyance, or rare + moderate → MEDIUM.
- Noticed-but-harmless → LOW.
- Persistence multiplier: a problem that hurts *every time* rates one level above the same problem that hurts once.

## Conflict shortcuts

- H7 vs H8 (power vs minimalism) → progressive disclosure.
- H4 vs improvement (consistency vs better pattern) → consistency now, migrate everywhere at once later ([R9](../../../core/conflict-resolution.md)).
- H1 vs H8 (status vs noise) → status for things users act on; log the rest.
- H10 pressure (help needed) → first ask if H2/H6 fix removes the need ([Krug: cut before explain](../steve-krug/decision-framework.md)).
