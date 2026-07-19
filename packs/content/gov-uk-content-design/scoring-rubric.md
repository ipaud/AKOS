# Scoring Rubric — GOV.UK Content Design Pack

Feeds the copy/content dimension of the AKOS review pipeline. Score = 100 − deductions, floor 0. Bands per [core/scoring-model.md](../../../core/scoring-model.md).

## Deductions

| Finding | Deduction |
|---------|-----------|
| Content is factually wrong or contradicts current reality (price, date, threshold, process) | −25 (CRITICAL) |
| An instruction, deadline, obligation or consequence does not name who must act | −25 (CRITICAL) |
| Page meets no user need, or the need's beneficiary is the organisation | −25 (CRITICAL) |
| Stale content (past review date, unverified) on a task-critical path | −25 (CRITICAL) |
| Task-completing content available only inside an attachment | −25 (CRITICAL) |
| Answer not in the first sentence / preamble before the answer | −10 each page (HIGH) |
| Readability target missed (grade level, or mean sentence length > 20 words) | −10 (HIGH) |
| Sequence, comparison or branching condition trapped in prose | −10 each (HIGH) |
| Page vocabulary diverges from the words users search with | −10 (HIGH) |
| Page serves two needs or two audiences without splitting | −10 (HIGH) |
| Duplicate page answering the same question | −10 (HIGH) |
| Title fails: not front-loaded, > 65 chars, or not honoured by the page | −10 (HIGH) |
| No named owner or no review date | −10 (HIGH) |
| Specialist term undefined at first use | −4 each, cap −12 (MEDIUM) |
| Heading fails the first-three-words test | −4 each, cap −12 (MEDIUM) |
| Metaphor or figurative language in instructional content | −4 each, cap −12 (MEDIUM) |
| Paragraph, bullet or page-length ceilings exceeded | −4 each, cap −12 (MEDIUM) |
| Formal filler, "simply"/"just", Latin abbreviations | −1 each, cap −6 (LOW) |
| Non-descriptive link text | −1 each, cap −6 (LOW) |
| Number, date, or emphasis-formatting convention breaches | −1 each, cap −5 (LOW) |

## Hard caps

- Any open CRITICAL: score ≤ 59 (Blocked). Wrong content and unassigned obligations are user-harm defects, not polish.
- No user need statement recorded for the content set: cap 69.
- Content set with no owner or no review schedule, Production profile: cap 74.
- Never revised since publication, Production profile: cap 79 (publish-and-forget guard).

## Modifiers

- Need statements evidenced by search data, support volume or research: +5 (cap 100).
- Post-launch iteration performed against real data with the top failure fixed: +5 (cap 100).
- Retirement pass completed in the last review cycle, with redirects recorded: +3.
- Repeat finding from a previous review, unfixed and without a recorded tradeoff: double its deduction.

## Interpretation anchors

- **95** — needs are evidenced, answers are first, structure matches content type, estate is owned and reviewed. Findings are convention-level.
- **85** — solid and current; a cluster of MEDIUMs (headings, undefined terms, length) to schedule.
- **72** — readers get there, but with work: preamble, prose hiding structure, vocabulary drift. Acceptable pre-launch with fixes queued.
- **60** — the estate is growing faster than it is maintained; duplicates and unowned pages present. Fix before adding anything.
- **≤59** — content is wrong, unassigned, or answers nobody's question. BLOCKED.
