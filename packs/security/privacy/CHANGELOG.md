# Changelog — privacy

## [1.0.0] — 2026-07-26

### Added

- First complete version. Authority level 1 (EU regulation, EDPB guidelines, AEPD cookie
  guidance), review cadence 545 days (`review_after: 2028-01-22`). Closes a verified
  zero-coverage gap: before this pack, no AKOS pack mentioned GDPR, lawful basis, consent
  as a legal concept, retention, data-subject rights, or processors.
- Principles P1–P18 across a spine, lawfulness, design, obligations, and interface. The
  spine: personal data is anything that singles out a person rather than the obvious
  fields, every field names its purpose before collection, collection is the decision that
  cannot be undone, and privacy is a schema property rather than a policy document.
- Engineering rules PR1–PR49 across inventory and purpose, lawful basis and consent,
  minimization and design defaults, retention and deletion, subject rights, processors and
  transfers, incidents and high-risk processing, interface and disclosure, and a
  Supabase/Postgres mapping. Starred rules mark the safety floor, which applies from the
  first real person's data rather than from launch.
- The data inventory (PR1) is positioned as the artifact every other rule depends on:
  retention has nothing to enforce without it, deletion has no destination list, the
  privacy notice has nothing to be verified against, and a breach has no scope.
- Review checklist ordered by severity with every item citing its rule, and a scoring
  rubric whose hard caps encode two judgments: no inventory *and* no enforced retention
  caps at 39 because neither the current exposure nor its end date is known, and erasure
  offered in the UI but unverified end-to-end caps at 59 because a false claim to users is
  a defect rather than a gap.
- Anti-patterns drawn from the principles: the just-in-case column, the retention policy
  nobody enforces, the deletion that deletes one table, the consent theatre banner, the
  consent flag that changes nothing, the identified log line, the production copy in
  staging, the invisible processor, the default that shares, the policy-page disclosure,
  the breach plan written during the breach, and the GDPR sprint.
- Decision framework covering whether the pack applies at all (the trigger is one real
  person's data, not scale or launch), an ordered test for choosing a lawful basis that
  puts consent fourth rather than first, a placement table, retention stances per
  category, an honest set of options when the full deletion path cannot be built yet, and
  the triggers for assessing before building.
- Prompt fragments: build-mode constraint block, review lens, a new-field intake
  questionnaire, and a tight-budget one-liner.
- Filed under `security/` rather than a new `legal/` domain — a one-pack domain is
  speculative structure, and this routes through the existing security lens. Recorded so
  the decision is re-openable when a second legal pack exists.
- Carries a second disclaimer beside the standard distillation line: engineering guidance,
  not legal advice. The pack helps build a system that can comply; it does not adjudicate
  whether it does.
- Scope boundary recorded against `packs/security/owasp-top-10` and `packs/security/auth`
  (protecting the data and who may log in), `packs/backend/supabase` and
  `packs/backend/postgres` (enforcement mechanics), and `packs/content/ux-writing` (the
  wording of a consent screen).
