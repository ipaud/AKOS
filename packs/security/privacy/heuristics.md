# Heuristics — Privacy Pack

Defaults with known exceptions. Use these while the design is open; the
[engineering rules](engineering-rules.md) decide once the schema exists.

- **Don't collect it.** The strongest privacy control available at any moment is the field
  you decline to add. Every other control is damage limitation on a decision already made.
- **Ask "what breaks without this field?" before "where do we store it?"** If nobody can
  name the decision the field feeds, it is being collected because the form template had a
  slot for it.
- **Reach for a lawful basis other than consent when one genuinely fits.** Contract
  necessity for things the product cannot do without is honest and carries no withdrawal
  mechanism to build. Consent for things the user can meaningfully decline is honest too.
  Consent as a blanket wrapper over everything is neither.
- **If the cookie banner is the privacy work, there is no privacy work.** The banner is the
  most visible and least important part. The schema, the retention jobs, and the deletion
  path are where the exposure lives.
- **Assume every analytics event will eventually be joined to a user.** Design it
  pseudonymous now, because the join is one product request away and by then the history
  is already personal data.
- **Write the deletion path when you write the create path.** Retrofitting erasure means
  archaeology across every system the data reached — and the archaeology is done under
  time pressure, by whoever is on call.
- **Treat any new SDK in the bundle as a processor decision.** A tag manager, a session
  recorder, a support widget, and a chat model API are all third parties receiving
  personal data, whatever the ticket called them.
- **Prefer a region choice you made to a region you inherited.** Project-creation defaults
  are a hosting decision that later reads as a data-residency decision.
- **Log the pseudonym, never the person.** A support engineer debugging tomorrow needs to
  correlate events, not to read an address. The identifier is enough.
- **When precision has no purpose, drop it.** Date instead of timestamp, region instead of
  coordinates, band instead of birth date. Less precision is less to lose and usually
  answers the same question.
- **If a user would be surprised, say it where it happens.** A disclosure that only exists
  in the policy converts surprise into resentment at exactly the wrong moment.
- **Prototype profile relaxes process, never the floor.** A never-deployed local
  experiment with fake data can skip nearly all of this. The moment one real person's data
  is in it, the starred rules apply — and prototypes reach real people without a rewrite
  gate.
- **Get a lawyer for the questions that are actually legal.** Whether a legitimate-interest
  assessment holds, whether a transfer mechanism is valid, whether a specific processing is
  high-risk — this pack helps you build correctly, it does not adjudicate.
