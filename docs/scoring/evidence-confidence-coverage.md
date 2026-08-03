# Evidence, confidence, and coverage in the Review Summary

Two small, additive changes to the unified Review Summary template (`agents/ux-reviewer.md`, mirrored in `core/review-pipeline.md`), so a score never implies more certainty than the review actually earned — without changing a single band, anchor, or decision rule already in place.

## What changed

1. **Every finding carries an inline confidence tag**: `(Confidence: Certain|High|Moderate|Low)`.
2. **A new `## Coverage` section**, between "Relevant Knowledge Packs Used" and "Scores":
   ```markdown
   ## Coverage
   - Inspected:
   - Not inspected / out of scope:
   - Confidence basis:
   ```

## What did *not* change

- `core/scoring-model.md`'s bands, severity anchors, and hard caps — unchanged.
- `core/review-pipeline.md`'s severity-based decision rules — unchanged by *this* addition. A CRITICAL blocks at *any* coverage level. Low coverage is a reason to say so in the Coverage section, never a reason to soften a finding actually made, and never a decision INPUT — only a reporting addition.
- The 13 agent files' own sections (Purpose, Packs to load, Review checklist, etc.) — untouched.

## INCOMPLETE is not a coverage concept, even though it looks adjacent

`core/review-pipeline.md` separately added a fourth decision state,
**INCOMPLETE**, in v1.17.4 — after this document was written, and worth
distinguishing precisely because the two are easy to conflate:

- **Coverage** describes a review that *happened*, honestly, at whatever
  depth it reached. "Static read only, no runtime check" is low coverage,
  not a failure — it's the Coverage section doing its job.
- **INCOMPLETE** describes a review that *didn't happen* for some dimension —
  a dispatched lens never returned. That's not thin coverage to disclose;
  there's no report from that lens to disclose coverage *of*.

The reason both rules exist together, stated once so it doesn't drift between
files: coverage must never lower severity (a thin review can't argue past a
real defect), but absence of a lens's report must never read as a clean
result either (a run where every lens silently failed would otherwise emit
the identical PASS/BLOCKED string as a run where every lens passed). One rule
protects against a false negative from softened findings; the other protects
against a false positive from findings that were never made at all. Silence
from a lens is not a pass — check INCOMPLETE first, then apply coverage
discipline to whatever did report.

## Why this is a formalization, not a new concept

`core/confidence-model.md` already fully defines four confidence levels (Certain/High/Moderate/Low) and already states "CRITICAL and HIGH findings require Certain or High confidence" (rule 1). What it never had was a *structured field* — confidence was expressed only implicitly through severity, plus occasional free-text parentheticals on sub-finding-bar notes. The inline tag makes that legible per-finding without requiring a reader to reconstruct it from severity alone.

**Coverage**, by contrast, genuinely didn't exist before in any form — informal or formal. Grepping `core/`, `scoring/`, and `agents/` before this change found zero references to "coverage" outside its narrow, literal meaning in `agents/testing-reviewer.md` (test coverage specifically). This is the one true addition.

## Confidence vs. coverage — two different axes

- **Confidence** is about *this specific claim*: how sure is the reviewer that this one finding is real?
- **Coverage** is about *the review as a whole*: how much of the actual surface area got looked at?

A review can have high confidence on everything it checked while covering only a fraction of the codebase — that's a narrow-but-solid review, and the Coverage section is exactly how it says so honestly, rather than reading as a comprehensive verdict it never claimed to be.

## Example

```markdown
## Critical Issues

**C1 — RLS disabled on the `invoices` table.** Confirmed by reading the
migration directly: `CREATE TABLE invoices` has no corresponding
`ENABLE ROW LEVEL SECURITY` anywhere in `supabase/migrations/`.
(Confidence: Certain)

## Coverage

- Inspected: `supabase/migrations/*.sql`, `src/features/invoices/*.tsx`
- Not inspected / out of scope: the Stripe webhook handler (out of scope
  for this security pass — flag for a follow-up review), anything under
  `docs/`
- Confidence basis: direct read of migration SQL for C1; UX findings are
  static-read only, no live click-through performed
```

## Where this is used

- `agents/ux-reviewer.md` — the canonical template copy.
- `core/review-pipeline.md` — the mirrored copy, plus the same explanatory note.
- `core/confidence-model.md` — updated "In review output" section, clarifying confidence vs. coverage as distinct axes.
- `core/scoring-model.md` — one added sentence in "Reporting," no formula changes.

No other agent file needed a change — all 12 of the other reviewers reference the canonical template by name rather than duplicating it, so they inherit this automatically.
