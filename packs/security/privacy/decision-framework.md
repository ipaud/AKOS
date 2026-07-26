# Decision Framework — Privacy Pack

The choices this domain actually presents, and how to settle each one. Engineering
decisions — the legal calls belong to a lawyer.

## Does this pack apply at all?

| Situation | Applies? |
|---|---|
| Local experiment, synthetic data, never deployed | Process rules no; PR13/PR16 still good practice. |
| Deployed, but only your own data | Yes, lightly — the mechanisms are cheap to add now and expensive later. |
| One real user who is not you | Fully. The starred rules are the floor from this point. |
| Users in the EU/EEA, or you are established there | Fully, and the regulatory exposure is real. |

The trigger is *one real person's data*, not scale, not funding, not launch.

## Which lawful basis?

Ask in order, and stop at the first that genuinely fits:

1. **Is the processing required to deliver what the user asked for?** → contract
   necessity. Account records, order fulfilment, the thing the product is.
2. **Is it required by law?** → legal obligation. Tax records, retention mandates.
3. **Is it something the user can meaningfully decline without the product breaking?** →
   consent. Marketing, non-essential analytics, optional personalization.
4. **Is it a narrow operational need a reasonable user would expect, and you can document
   the balancing?** → legitimate interest. Security logging, fraud prevention.
5. **None of the above** → don't process it.

Choosing consent commits you to PR7, PR8, and PR9 — recording it, making refusal equal,
and actually stopping. Choosing it out of caution for something that is genuinely
contract-necessary creates work and a worse user experience for no protection.

## Where does this data live?

| Data | Default placement |
|---|---|
| Account identity | Primary store, RLS-protected, in the chosen region. |
| Behavioral events | Pseudonymous, separate store, own retention window. |
| Logs and traces | No personal data beyond a pseudonymous identifier; short retention. |
| Support conversations | Treated as personal data including free text; in the deletion path. |
| Backups | Bounded retention, documented deletion re-application. |
| Anything sent to a third party | Listed in the processor inventory before the first send. |

## Retention: pick the number, then build the mechanism

| Category | Typical stance |
|---|---|
| Account data | While the account exists, plus a short grace window, then erase. |
| Transaction records | The legally mandated period, then erase — not "forever, just in case". |
| Behavioral analytics | Months, not years. Aggregate beyond that if the metric still matters. |
| Logs | Days to weeks for debugging, longer only for security events with a stated reason. |
| Backups | The shortest window that meets the recovery objective. |

A number without a job that enforces it (PR20) is documentation, not retention.

## Build the deletion path, or promise less?

If the full deletion path cannot be built now, the honest options are:

1. **Reduce the spread** — send personal data to fewer systems, so deletion has fewer
   destinations. Usually the cheapest fix.
2. **Build it partially and record the gap** with a named owner (PR25). Acceptable
   temporarily, visible in review.
3. **Change what you tell users** so the claim matches the mechanism.

What is not an option is a deletion button that clears one table while the data remains in
four others (P14).

## When does an assessment happen before the build?

Any of: large-scale profiling, systematic monitoring of a public space, special-category
data at scale, automated decisions with legal or similarly significant effect, or data
about children. If any applies, the assessment precedes implementation (PR38) — done
afterward it documents a decision instead of informing one.

## Profile modulation

- **Prototype** — starred rules apply from the first real user. Inventory can be a single
  file rather than a system; the breach runbook can be one page.
- **Startup MVP** — starred rules plus everything under High. Deletion path and retention
  jobs are not deferrable once accounts exist.
- **Production / Enterprise** — the full checklist, with the inventory verified against the
  schema each release and the notice verified against the inventory.

## When this pack is not the right one

- Protecting the data from attackers → [owasp-top-10](../owasp-top-10/README.md).
- Who can log in and how → [auth](../auth/README.md).
- Row-level enforcement and schema mechanics →
  [backend/supabase](../../backend/supabase/README.md),
  [backend/postgres](../../backend/postgres/README.md).
- The wording of a consent screen → [content/ux-writing](../../content/ux-writing/README.md),
  bounded by PR8 and PR42.
