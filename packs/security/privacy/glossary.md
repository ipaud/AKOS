# Glossary — Privacy Pack

Terms this pack uses precisely. Legal terms are given in their engineering sense — what
the system has to do — not as definitions to rely on in a legal argument.

- **Personal data** — anything that can single out a person, directly or in combination.
  Includes IP addresses, device and session identifiers, and free text users paste in.
- **Special-category data** — the classes needing stronger justification: health,
  biometrics, genetics, race, religion, politics, sexuality, trade union membership.
- **Data subject** — the person the data is about. "User" in most product conversations,
  but also non-users whose data you hold (a contact in someone's invite list).
- **Controller** — whoever decides why and how personal data is processed. Usually you.
- **Processor** — whoever processes it on the controller's behalf: hosting, analytics,
  email, support tooling, and model APIs. Choosing one is a data-protection decision.
- **Sub-processor** — a processor's own processors. Inside your boundary whether or not
  you picked them.
- **Lawful basis** — the justification for a processing purpose. Consent is one of
  several, and often not the best fit.
- **Consent** — a freely given, specific, informed, unambiguous choice. Pre-ticked,
  bundled, or hard-to-refuse means no consent at all, only a record of one.
- **Purpose limitation** — data collected for one stated purpose is not silently reused
  for another.
- **Data minimization** — collecting and storing only what a stated purpose requires. A
  schema property, not a query property.
- **Privacy by design / by default** — protections built into the system rather than
  configured onto it, with the protective option shipped enabled.
- **Pseudonymization** — replacing identifiers with a stand-in, with the mapping held
  separately. Still personal data, but a smaller blast radius.
- **Anonymization** — irreversibly removing the ability to single someone out. If it can
  be reversed with data you or anyone else holds, it is pseudonymization.
- **Retention period** — how long a category of data lives. Real only when a mechanism
  enforces it.
- **Data inventory** — the record of what personal data exists, why, for how long, and
  where it goes. The artifact every other rule in this pack depends on.
- **Data subject rights** — access, rectification, erasure, portability, restriction, and
  objection. Product features with response windows, not support tickets.
- **Right to erasure** — deletion across every destination the data reached, not only
  where it started.
- **Portability** — supplying the subject's data in a structured, machine-readable format.
- **DPIA** — a written assessment done *before* building high-risk processing, naming the
  risk to the person and what would make the processing unacceptable.
- **Personal data breach** — any security failure leading to loss, alteration, or
  unauthorized disclosure of personal data. The reporting clock starts at awareness.
- **Data residency** — where the data physically sits. A deliberate configuration choice,
  not a project-creation default.
- **Essential cookie** — storage strictly necessary to deliver what the user asked for.
  Everything else needs consent, including analytics.
- **Dark pattern** — an interface shaped to produce the choice the operator wants rather
  than the one the user would make. In consent surfaces it invalidates the consent.
