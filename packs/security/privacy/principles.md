# Principles — Privacy Pack

Durable rules for building systems that hold personal data. Engineering guidance, not
legal advice — where a decision carries real regulatory exposure, get a lawyer. The
`PR*` codes in [engineering-rules.md](engineering-rules.md) derive from these.

## The spine

- **P1 — Personal data is anything that can single out a person, not just the obvious
  fields.** An IP address, a device identifier, a session cookie, a support-ticket
  screenshot, and a "user_1847" analytics event are all in scope. Teams under-scope this
  by picturing name-and-email and missing the four other places a person is identifiable.
- **P2 — Every field must name why it exists before it is collected.** Not what it might
  be useful for. A column with no stated purpose has no lawful basis, no retention rule,
  and no one who will notice when it leaks.
- **P3 — Collection is the decision that cannot be undone.** Encryption, access control,
  and deletion jobs all reduce risk after the fact. Not collecting removes it. The
  cheapest privacy control in the system is the field you didn't add.
- **P4 — Privacy is a schema property, not a policy document.** A retention promise that
  lives only in a policy page will be false within a year. If it isn't a constraint, a
  job, or a test, it isn't a rule — it's a hope with a publication date.

## Lawfulness

- **P5 — Consent is one lawful basis among several, and usually the weakest one to
  build on.** Contract necessity and legitimate interest carry no withdrawal mechanism to
  implement. Choosing consent means committing to capture it, record it, honor its
  withdrawal, and function without it.
- **P6 — Consent that isn't refusable isn't consent.** Pre-ticked boxes, cookie walls
  where "reject" is three clicks deeper than "accept", and bundled all-or-nothing
  toggles produce a record with no legal weight and a design that reads as contempt.
- **P7 — Withdrawal must be as easy as granting.** If turning it on took one click, so
  does turning it off, and the system must actually stop the processing rather than
  merely record the preference.
- **P8 — A basis chosen at design time is a basis you can defend.** Retrofitting one
  after launch means discovering that the data you already hold has no justification and
  the choice is now deletion or exposure.

## Design

- **P9 — Minimize at the schema, not at the query.** Fields not stored cannot leak, be
  subpoenaed, be exported by mistake, or sit in a backup for seven years. Selecting fewer
  columns is not minimization.
- **P10 — Separate identity from behavior wherever the join isn't needed.** Analytics,
  logs, and telemetry rarely need to name a person; they need to count one. A pseudonym
  with the mapping held elsewhere converts most incidents from personal-data breaches to
  bad days.
- **P11 — Defaults are the setting almost everyone will keep.** Data protection by
  default means the privacy-preserving option is the one that ships enabled, not the one
  available to whoever reads the settings page.
- **P12 — Retention is a deletion job, not a number in a document.** Every category of
  personal data has a stated lifetime and a mechanism that enforces it, including in
  backups, logs, analytics, and the third-party systems it was copied into.

## Obligations

- **P13 — Subject rights are product features with SLAs, not support tickets.** Access,
  rectification, erasure, portability, and objection each need a path that works at
  volume. A manual process that works for three requests fails on the day it matters.
- **P14 — Erasure means everywhere it went, not everywhere it started.** The row, the
  backups, the search index, the analytics warehouse, the email provider, the CRM, the
  support tool, the logs. A deletion feature that only clears the primary table is a
  false claim with a UI.
- **P15 — Every processor you send data to is your responsibility to the user.** The
  hosting provider, the analytics vendor, the email sender, the LLM API. Choosing them is
  a data-protection decision, and their sub-processors are inside your boundary too.
- **P16 — A breach is a clock, and the clock starts at awareness, not at
  confirmation.** The reporting obligation is measured in tens of hours, so detection,
  triage, and decision-making must be prepared before the incident, not during it.
- **P17 — When processing is high-risk, the assessment happens before the build.** Large-
  scale profiling, sensitive categories, systematic monitoring, and automated decisions
  with legal effect are the triggers. Assessing afterwards produces a document, not a
  decision.

## Interface

- **P18 — If the user would be surprised, the design is the problem, not the
  disclosure.** Burying a genuinely unexpected use in a privacy policy does not make it
  expected. Surprise is a design signal — see
  [content/ux-writing](../../content/ux-writing/README.md) for saying it plainly.

## Scope

This pack covers building and reviewing systems that process personal data, from an EU
baseline. It is not legal advice, does not cover sector-specific regimes (health,
finance, children's services beyond the general rules), and does not restate other
jurisdictions. Security controls protecting that data live in
[owasp-top-10](../owasp-top-10/README.md) and [auth](../auth/README.md); the storage
rules live in [backend/supabase](../../backend/supabase/README.md) and
[backend/postgres](../../backend/postgres/README.md).
