# Anti-Patterns — Privacy Pack

Named failure modes, how to spot them, and what to do instead.

## The just-in-case column

**Detect:** fields nobody reads — a phone number no flow uses, a birth date collected
"for personalization later", a full address on a digital-only product.
**Why it fails:** every unused field is exposure with no offsetting value: it appears in
exports, backups, breach scope, and subject-access responses forever.
**Fix:** delete the column. If a purpose appears later, add it then, with a basis and a
retention rule. (PR2, PR13)

## The retention policy nobody enforces

**Detect:** a privacy page stating "we keep data for 12 months" and no job, TTL, or
partition drop implementing it.
**Why it fails:** it is a public, dated, false statement — and the data it describes is
still accumulating.
**Fix:** make the number a mechanism with a test asserting old data is gone. If you can't
build the mechanism, change the statement. (PR20, PR47)

## The deletion that deletes one table

**Detect:** a "delete my account" path touching the primary record only, while the search
index, warehouse, email provider, support tool, and storage bucket keep their copies.
**Why it fails:** the product now claims erasure it does not perform, which is worse than
not offering it.
**Fix:** derive the deletion path from the inventory, enumerate every destination, and
list what you cannot yet reach with an owner. (PR21, PR25, PR46)

## The consent theatre banner

**Detect:** "Accept all" as a prominent button and "Manage preferences" as a small link
two screens from "Reject"; pre-ticked toggles; a cookie wall with no genuine alternative;
scripts that already loaded before the choice.
**Why it fails:** it produces a consent record with no legal weight while signaling to
users that their choice is an obstacle to route around.
**Fix:** equal-depth accept and reject, unticked by default, granular per purpose, and
nothing non-essential loading until the answer arrives. (PR8, PR10, PR11)

## The consent flag that changes nothing

**Detect:** withdrawal flips a boolean, but the nightly export, the recommendation job, or
the third-party sync still reads the row.
**Why it fails:** the user was told processing stopped, and it did not.
**Fix:** every consumer checks current consent state at read time, and the withdrawal path
has a test proving the downstream job skips the record. (PR9)

## The identified log line

**Detect:** email addresses, full names, request bodies, or tokens in application logs,
error reports, or an observability vendor's index.
**Why it fails:** logs are the least access-controlled, most widely replicated, longest-
retained store in the system. Personal data there is personal data everywhere.
**Fix:** log a pseudonymous identifier and correlate with it. Redact at the logger, not by
asking people to be careful. (PR15, PR23)

## The production copy in staging

**Detect:** a staging or demo environment seeded from a production dump, usually with
weaker access control and no retention.
**Why it fails:** it multiplies the breach surface while removing the controls that
justified the original storage.
**Fix:** synthetic or irreversibly anonymized fixtures. If a bug genuinely needs real
data, it needs the same protections as production. (PR18)

## The invisible processor

**Detect:** an SDK, tag manager, chat widget, session recorder, or model API added in a
feature PR, sending personal data to a vendor nobody assessed.
**Why it fails:** users were told which third parties receive their data, and this one
wasn't on the list.
**Fix:** treat every new external destination as a processor decision with its own review,
including AI APIs — they are processors like any other. (PR31, PR32)

## The default that shares

**Detect:** profiles public unless changed, tracking on unless disabled, sharing enabled
for new users, a new feature switched on for existing accounts.
**Why it fails:** almost nobody changes a default, so the default *is* the policy.
**Fix:** ship the privacy-preserving option enabled, and treat opt-out design as a finding
rather than a growth tactic. (PR16)

## The policy-page disclosure

**Detect:** a genuinely surprising use — training a model on user content, sharing with a
partner, recording sessions — disclosed only in the privacy notice.
**Why it fails:** disclosure is not consent, and burying a surprise does not make it
expected. It converts into a trust incident the moment someone notices.
**Fix:** surface it in context, at the moment it happens, in plain words. If it can't be
said plainly in context, reconsider the processing. (PR41, P18)

## The breach plan written during the breach

**Detect:** no runbook, no severity criteria, no named decision-maker, no detection for
bulk reads or export spikes.
**Why it fails:** the notification obligation runs on a clock measured in tens of hours,
starting at awareness. Improvising the process consumes the entire window.
**Fix:** write the runbook and wire the detection before launch. Rehearse once. (PR36,
PR37)

## The GDPR sprint

**Detect:** privacy treated as a pre-launch checklist item, or a one-off project with a
completion date.
**Why it fails:** the inventory drifts from the schema within one release, and the notice
becomes false without anyone editing it.
**Fix:** verify the inventory against the schema at each release and the notice against
the inventory. It is a standing check, like tests. (PR1, PR40)
