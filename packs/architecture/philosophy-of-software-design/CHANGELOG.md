# Changelog — philosophy-of-software-design

## [1.0.0] — 2026-07-26

### Added

- First complete version. Authority level 3 (a book), review cadence 270 days
  (`review_after: 2027-04-22`). Cleared the source intake gate in
  `core/source-policy.md` on a verified gap: `Ousterhout`, `deep module`, `shallow
  module`, `information hiding`, `change amplification`, `temporal decomposition`,
  `tactical programming` and `define errors out of existence` all returned zero hits
  across the 56-pack corpus. `information hiding` returning zero was the deciding signal —
  a foundational concept no architecture pack covered.
- Principles P1–P19 across what complexity is, modules, errors and special cases, and
  working method. The spine: complexity is whatever makes a system hard to understand or
  change; it presents as change amplification, cognitive load, and unknown unknowns; it has
  exactly two causes, dependencies and obscurity; and it accumulates incrementally, which
  is why no mess is ever small enough to ignore.
- Engineering rules PSD1–PSD36 across module depth, information hiding, interfaces, errors
  and special cases, naming, comments, and working method.
- **No rule is starred.** Every other pack marks a safety floor; this one has none, and the
  absence is deliberate — a Level 3 design opinion must not acquire floor authority. The
  scoring rubric enforces the same judgment: no CRITICAL band, total deduction capped at
  −40, and `n/a` under the Prototype profile.
- Mental models: module depth as a rectangle where splitting always adds width, the three
  symptoms as a review triage vocabulary, the two causes as a filter for design debates,
  complexity as sediment, pulling complexity downward, defining errors out of existence,
  design it twice, strategic versus tactical, and comments as a design tool.
- Anti-patterns including two failures of *applying* this pack rather than of the code:
  the unfalsifiable design objection ("this module is shallow", with no statement of what a
  caller would stop needing to know) and design theatre on a prototype. Both are the likely
  failure mode on a corpus that already carries `solid` and `clean-architecture`.
- A reviewer-discipline rule carried in three places (review checklist, scoring rubric,
  review-lens prompt fragment): a finding must name what a caller or the next reader stops
  having to know, or it is dropped. An unfalsifiable objection either blocks work
  arbitrarily or teaches people to ignore design feedback, and the second costs more than
  the shallow module did.

### Recorded disagreement

- **This pack disputes the common reading of `solid` and `clean-architecture` on
  decomposition granularity**, and the disagreement is stated rather than smoothed over.
  It is Level 3 against Level 3, both architecture sources, so
  `core/conflict-resolution.md` steps 4 (authority) and 5 (proximity) both tie.
  `decision-framework.md` resolves it in practice: the packs agree far more than they
  differ, the tiebreak question is what the split hides, the resolution requires an explicit
  tradeoff statement, and a Level 0 personal file-size convention outranks all of it (R4).
- The accurate reading — and the one that dissolves most of the conflict — is that this
  pack is about **interface** depth, not file length. `packs/personal/pau-avila/coding-preferences.md`
  keeps its 200–400 line convention untouched.

### Scope boundary

Recorded against `packs/architecture/clean-architecture` (dependency direction),
`packs/architecture/solid` (class responsibility), `packs/architecture/design-patterns`
(named structures), `packs/architecture/martin-fowler-refactoring` (mechanics of
restructuring), and `packs/architecture/domain-driven-design` (modeling a complex domain).
