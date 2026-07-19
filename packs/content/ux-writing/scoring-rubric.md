# Scoring Rubric — UX Writing Pack (Interface Copy)

Primary input to the copy dimension in [scoring/ux-score.md](../../../scoring/ux-score.md). Score = 100 − deductions, floor 0. Bands per [core/scoring-model.md](../../../core/scoring-model.md).

Truthfulness findings are scored as correctness defects, not style: a label that misdescribes behaviour misleads users about the state of the world.

## Deductions

| Finding | Deduction |
|---------|-----------|
| Label names an effect the code does not produce, on a primary path (UWE1) | −25 (CRITICAL) |
| Success/confirmation message can fire when the operation didn't succeed (UWE2) | −25 (CRITICAL) |
| Capability claim with no implementation behind it (UWE4) | −25 (CRITICAL) |
| Meaning available only via tooltip/`title`/hover (UWE38) | −25 (CRITICAL, safety floor) |
| Field error not in text or not associated with its field (UWE21, UWE40) | −25 (CRITICAL, safety floor) |
| Destructive confirmation misstates reversibility or omits object/scope (UWE14) | −25 (CRITICAL) |
| Label/behaviour mismatch off the primary path | −10 (HIGH) |
| Error or blocked state with no next action (UWE18) | −10 each (HIGH) |
| Synonym drift: one concept with multiple user-facing terms (UWE8) | −10 per concept (HIGH) |
| Developer vocabulary in user-facing strings (UWE9) | −10 (HIGH), −4 if a single isolated string |
| Dead-end empty state, or one message serving several zero states (UWE31, UWE32) | −10 per surface (HIGH) |
| Generic status where the system knows the specific cause (UWE5) | −10 (HIGH) |
| Bare code / exception as the only user-facing message (UWE19) | −10 (HIGH) |
| Two confirmations for one action (UWE34) | −10 (HIGH) |
| Yes/No/OK on a consequential dialog, or ambiguous escape option (UWE14, UWE15) | −10 (HIGH) |
| Placeholder-only labels (UWE25) | −4 each (MEDIUM) |
| Validation states the violation, not the rule (UWE22) | −4 each (MEDIUM) |
| Blame construction in error copy (UWE20) | −4 each (MEDIUM) |
| Format tantrum the code could normalize (UWE23) | −4 each (MEDIUM) |
| Missing reassurance at a commitment point (UW8) | −4 per point (MEDIUM) |
| Tone mismatch: humour/celebration in failure, loss, or cost moments | −4 each (MEDIUM) |
| Mixed grammar within a label set (UWE10) | −4 per set (MEDIUM) |
| Vague button label; bare spinner on a long operation (UWE13, UWE33) | −4 each (MEDIUM) |
| Concatenated sentences or `count === 1` plural grammar (UWE41, UWE42) | −4 each (MEDIUM) |
| Happy talk on a task screen; copy patching a control defect (UW9) | −1 each, cap −5 (LOW) |
| Capitalization inconsistency, internal code names, missing field rationale | −1 each, cap −5 (LOW) |
| Layout intolerant of string growth; strings as literals outside the resource layer | −1 each, cap −5 (LOW) |

## Hard caps

- Any open CRITICAL truthfulness finding: score ≤ 59 (BLOCKED). A product that lies about what it did fails this dimension regardless of how well the rest reads.
- No terminology ledger, Production profile: cap 79.
- Product ships in more than one language with no resource layer or plural API: cap 69.

## Modifiers

- Terminology ledger exists, enforced by a CI blocklist: +5 (cap 100).
- Label-behaviour audit performed on this change and recorded: +3.
- Pseudo-localized screenshots reviewed for the changed screens: +2.
- Repeat finding from a previous review, unfixed without a recorded tradeoff: double its deduction.

## Interpretation anchors

- **95** — labels verified against handlers; one vocabulary; all four states written per surface; remaining findings are wording polish.
- **85** — honest and consistent; a cluster of MEDIUMs (validation phrasing, missing reassurance, placeholder labels) to schedule.
- **72** — users can work it out, but the product's vocabulary wobbles and some states dead-end; acceptable pre-PMF with fixes queued.
- **58** — a label or confirmation misrepresents what the system did; BLOCKED until the copy or the code is corrected.
