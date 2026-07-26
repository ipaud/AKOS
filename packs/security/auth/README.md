# Pack: Auth — Login, Sessions and Tokens

**Domain:** Security · **Authority:** Level 1 (IETF, OpenID Foundation, NIST) · **Version:** 1.0.0

Turns the OAuth 2.0 security best current practice, OpenID Connect, and the NIST digital
identity guidelines into checkable rules for the flow a product actually builds: the
login, the callback, the token, the session, the logout, and the reset.

Independent distillation for personal engineering use. Not affiliated with or endorsed by
the IETF, the OpenID Foundation, or NIST. See [references.md](references.md) for the
normative documents — where this pack and a specification disagree, the specification
wins.

## When to load this pack

- Designing or changing a login, signup, password reset, or logout flow.
- Adding an OAuth/OIDC provider, or moving between identity providers.
- Anything touching token validation, session lifetime, or refresh handling.
- Reviewing a surface where "who is this user" is decided.

Not this pack when the question is *what may this user access* — that's
[owasp-api-top-10](../owasp-api-top-10/README.md) and
[backend/supabase](../../backend/supabase/README.md) — or *what verification level do we
claim*, which is [owasp-asvs](../owasp-asvs/README.md).

## What's inside

| File | Highlights |
|------|-----------|
| [principles.md](principles.md) | P1–P16. Authn ≠ authz, the client never decides, identity fails at the seams. |
| [engineering-rules.md](engineering-rules.md) | AU1–AU60, `★` marking the safety floor. Includes a Supabase mapping section. |
| [review-checklist.md](review-checklist.md) | Binary checks by severity, each citing its rule. |
| [heuristics.md](heuristics.md) | Defaults while the design is still open — starting with "don't build it". |
| [decision-framework.md](decision-framework.md) | Build/delegate/buy, where the browser holds the session, session-lifetime table, when MFA earns its friction. |
| [anti-patterns.md](anti-patterns.md) | The trusted client claim, the unverified session read, the wildcard redirect, the forever session. |
| [scoring-rubric.md](scoring-rubric.md) | Deductions, hard caps, anchors at 95/85/72/55. |
| [prompt-fragments.md](prompt-fragments.md) | Build-mode constraint block, review lens, tight-budget one-liner. |
| [glossary.md](glossary.md) | The terms this pack uses precisely. |
| [references.md](references.md) | The four normative sources. |

## Core claim, one line

Authentication rarely fails in its cryptography and almost always fails at a
transition — the redirect that wasn't matched exactly, the state that wasn't checked, the
session that wasn't regenerated, the token that outlived the logout.

## Stack note

The Supabase section of [engineering-rules.md](engineering-rules.md) (AU54–AU60) exists so
the pack doesn't re-litigate the default stack: it names where the platform already
satisfies a rule, and where the rule is a setting that ships switched off.

## Related packs

[owasp-top-10](../owasp-top-10/README.md) · [owasp-api-top-10](../owasp-api-top-10/README.md) ·
[owasp-asvs](../owasp-asvs/README.md) · [privacy](../privacy/README.md) ·
[backend/supabase](../../backend/supabase/README.md) · [backend/rest](../../backend/rest/README.md)
