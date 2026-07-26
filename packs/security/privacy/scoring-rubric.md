# Scoring Rubric — Privacy Pack

Primary input to [scoring/security-score.md](../../../scoring/security-score.md), for the
data-protection dimension. Where a finding is also a security finding (an unprotected
table, a leaked credential), score it once in the security rubric — this one covers what
is collected, why, for how long, and where it goes.

## Deductions (from 100)

| Finding | Deduction |
|---------|-----------|
| Personal data in a table with no access control, reachable by an anonymous or shared client key | −40 (CRITICAL) |
| No lawful basis identified for a processing purpose that is live | −25 (CRITICAL) |
| Deletion feature that demonstrably does not delete (primary table only, downstream copies retained) | −25 (CRITICAL) |
| Consent recorded as a boolean with no scope, wording version, or timestamp | −25 (CRITICAL) |
| Withdrawal that does not stop the processing | −25 (CRITICAL) |
| No data inventory at all — nobody can say what personal data the system holds | −25 (CRITICAL) |
| Personal data sent to an unassessed third party (SDK, vendor, model API) | −25 (CRITICAL) |
| Production personal data copied into a non-production environment | −25 (CRITICAL) |
| Retention documented but not enforced by any mechanism | −10 (HIGH) |
| Consent design where reject is harder than accept, or non-essential storage set before consent | −10 (HIGH) |
| Personal data in application logs or error reports | −10 (HIGH) |
| Named-user analytics where a pseudonym would serve | −10 (HIGH) |
| No implemented path for access, portability, or erasure requests | −10 (HIGH) |
| No breach runbook, or no detection for bulk-read/export anomalies | −10 (HIGH) |
| Privacy-invasive default (public by default, tracking opt-out) | −10 (HIGH) |
| Backup retention unbounded or deletion-after-restore undocumented | −6 (MEDIUM) |
| High-risk processing with no written assessment | −6 (MEDIUM) |
| Indirect identifiers absent from the inventory | −6 (MEDIUM) |
| Precision stored beyond the purpose (timestamp for a date, coordinates for a region) | −4 (MEDIUM) |
| Admin/support access to personal records unlogged or unrestricted | −4 (MEDIUM) |
| Privacy notice drifted from what the system does | −4 (MEDIUM) |
| Subject-rights requests untracked | −2 (LOW) |
| Hosting region inherited rather than chosen | −2 (LOW) |

## Hard caps

- Any CRITICAL finding: score ≤ 59 (Blocked band), per
  [core/scoring-model.md](../../../core/scoring-model.md).
- No inventory *and* no enforced retention: cap 39. Neither the current exposure nor its
  end date is known, so no higher claim is defensible.
- Erasure offered in the UI but not verified end-to-end: cap 59. A false claim to users is
  scored as a defect, not a gap.
- Findings claimed as fixed without an executed check: cap 69, per
  [core/confidence-model.md](../../../core/confidence-model.md).

## Anchors

- **95** — inventory current, basis per purpose, minimal schema, pseudonymous telemetry,
  retention enforced and tested, deletion covers every destination, processors listed,
  runbook rehearsed.
- **85** — the floor holds; MEDIUM items (backup documentation, assessment write-ups)
  scheduled.
- **72** — floor holds, several HIGH gaps: retention unenforced, personal data in logs,
  subject-rights paths manual. Acceptable pre-PMF with a named owner.
- **55** — a starred rule is unmet, or the product claims something it does not do.
- **≤ 40** — nobody can state what personal data the system holds or when it goes away.
