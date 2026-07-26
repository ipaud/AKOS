# Changelog — auth

## [1.0.0] — 2026-07-26

### Added

- First complete version. Authority level 1 (IETF, OpenID Foundation, NIST), review
  cadence 545 days (`review_after: 2028-01-22`). Closes a verified zero-coverage gap:
  before this pack, no AKOS pack mentioned OAuth, OIDC, PKCE, session fixation, or refresh
  rotation — `backend/supabase` covered row-level authorization, and `owasp-asvs` covered
  stating a verification level, but nothing covered designing the login itself.
- Principles P1–P16, organized as a spine plus flow, session, and credential. The spine:
  authentication and authorization are separate decisions with separate tokens, every
  credential is a bearer of blast radius until something binds it, the client is a
  delivery mechanism and never the decision point, and identity flows fail at the seams
  rather than in the primitives.
- Engineering rules AU1–AU60 across flow selection, the round trip, redirects, token
  validation, token storage and transport, session lifecycle, passwords and recovery,
  multi-factor, enumeration and abuse, and a Supabase mapping. Starred rules mark the
  safety floor, which no reasoning profile modulates.
- A Supabase section (AU54–AU60) that names where the default stack already satisfies a
  rule and where the rule is a setting shipped switched off — so the pack does not
  re-litigate the stack it will most often be loaded against. AU54 is the one most likely
  to be violated in practice: `getSession()` returns unverified cookie contents, and
  authorizing from it is a client-trusted claim wearing server-side clothing.
- Review checklist ordered by severity with every item citing its rule, and a scoring
  rubric whose hard caps encode two judgments: hand-rolled auth with any starred rule
  unmet caps at 49, and a login suite that never exercises a rejected credential caps at
  79 — a suite asserting only success has verified the door opens, not that it locks.
- Anti-patterns drawn from the principles: the trusted client claim, the unverified
  session read, the wildcard redirect, the open return-to, the forever session, the token
  in the URL, the ID token used as a key, the helpful login error, the self-service MFA
  bypass, the rotation race excuse, the default nobody read, and the prototype exemption.
- Decision framework covering build/delegate/buy, where the browser holds the session,
  whether to have passwords at all, a session-lifetime table keyed to blast radius, and
  when MFA earns its friction — with the note that the decision which actually matters is
  the strength of the recovery path, not the presence of the factor.
- Prompt fragments: build-mode constraint block, review lens, a pre-implementation
  question set, and a tight-budget one-liner.
- Scope boundary recorded against `packs/security/owasp-asvs` (verification level),
  `packs/security/owasp-api-top-10` (object-level authorization),
  `packs/backend/supabase` (row-level rules), and `packs/content/ux-writing` (writing the
  enumeration-safe message without making it useless).
