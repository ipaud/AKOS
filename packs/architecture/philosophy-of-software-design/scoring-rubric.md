# Scoring Rubric — Philosophy of Software Design Pack

Feeds the maintainability dimension of
[scoring/architecture-score.md](../../../scoring/architecture-score.md). Deliberately
**shallow deductions and no CRITICAL band**: this is a Level 3 design pack, nothing in it
is a safety floor, and a rubric that lets design opinion push a score into the Blocked
band would make aesthetics outrank the things that genuinely block.

## Deductions (from 100)

| Finding | Deduction |
|---------|-----------|
| The same design decision (format, encoding, key layout, ordering rule) is known to two or more modules | −8 each, capped at −24 (MEDIUM) |
| Temporal decomposition producing that leakage — modules split by stage, sharing format knowledge | −8 (MEDIUM) |
| A caller must invoke methods in a fixed order for correctness | −8 (MEDIUM) |
| Public interface exposes an implementation choice (data structure, index, cache) | −6 (MEDIUM) |
| Change amplification demonstrated in this diff: one conceptual change, many files, no abstraction named | −6 (MEDIUM) |
| Shallow module — interface nearly as complex as the implementation it hides | −4 each, capped at −16 (MEDIUM) |
| An exception raised for a condition that could have been defined as normal | −4 (MEDIUM) |
| An identical `catch` repeated at every call site | −4 (MEDIUM) |
| Adjacent layers offering the same abstraction; pass-through methods or wrappers | −3 each, capped at −12 (LOW) |
| Interface comment describing implementation detail | −3 (LOW) |
| Non-obvious code with no *why* recorded; missing units, ranges, or null semantics | −3 (LOW) |
| Configuration parameter with no stated reason a caller should decide it | −2 (LOW) |
| Vague name where precision was available; one concept spelled two ways | −2 each, capped at −8 (LOW) |
| Comment restating the code below it | −1 (LOW) |
| Extension point with no present or scheduled second consumer | −2 (LOW) |

## Caps and floors

- **No finding from this pack scores above MEDIUM, and the total deduction is capped at
  −40.** A design-opinion pack cannot on its own put a score in the Blocked band, per
  [core/scoring-model.md](../../../core/scoring-model.md).
- **A finding without a named beneficiary does not score at all.** If the reviewer cannot
  say what a caller or reader stops having to know, it isn't a finding — see the reviewer
  discipline section of [review-checklist.md](review-checklist.md).
- **Prototype profile: this pack scores `n/a`.** Tactical is correct there; reporting a
  number would invent a problem.
- **Level 0 conventions win.** Where `packs/personal/<profile>/coding-preferences.md` sets
  a file-size or decomposition convention, code following it is not deducted for
  disagreeing with this pack (R4).

## Anchors

- **95** — boundaries hide real decisions, one owner per design decision, errors mostly
  defined out of existence, comments carry intent rather than restatement.
- **85** — sound overall; a few shallow wrappers or a leaked constant, all cheap to fix.
- **72** — one significant leak or a temporal decomposition that will amplify the next
  format change. Worth an explicit refactor ticket.
- **60** — change amplification is routine, and the team can name the module nobody
  understands. Not blocking, but this is what "hard to work in" measures.
