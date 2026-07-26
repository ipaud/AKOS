# Decision Framework — Auth Pack

The choices this domain actually presents, and how to settle each one.

## Build, delegate, or buy identity

| Situation | Choice |
|---|---|
| Any product with an existing platform auth (Supabase, the cloud provider's identity service) | Use it. Configure it properly — that *is* the work. |
| Consumer product, no enterprise buyer yet | Delegate to social/OIDC providers + the platform's own accounts. |
| Enterprise buyer requiring SSO, SCIM, custom IdP | Buy a dedicated identity vendor. Building SAML in-house is a product, not a feature. |
| Genuinely offline or air-gapped | Build, and accept that AU37–AU53 are now entirely yours. |

Deciding factor: whoever owns the credential store owns the breach. Delegating moves
the password-storage, reset, and breach-screening surface off your system.

## Where does the browser hold the session?

| Option | Choose when | Cost you are accepting |
|---|---|---|
| `HttpOnly` cookie, server-rendered or BFF | Default. Any app with a server you control. | One server hop; CSRF must be handled via `SameSite` + token. |
| `HttpOnly` cookie via the platform's SSR helper | Supabase/Next-class stack. | Ties session handling to that helper's lifecycle. |
| In-memory token, refresh via `HttpOnly` cookie | SPA calling a third-party API directly. | Token lost on reload; refresh path must be solid. |
| `localStorage` | Never for refresh tokens. Access tokens only in a prototype that will be rewritten before users. | Any XSS is total account compromise. |

## Password login, or none at all?

Ask in order:

1. Does a buyer contractually require local passwords? → keep passwords, apply AU37–AU44.
2. Is email delivery reliable for this audience? → magic link or OTP removes the password
   surface entirely.
3. Is the audience likely to already use one of the social providers? → OIDC login, with
   account linking designed up front rather than bolted on after two identities collide.
4. Otherwise → passwords, with breach screening and no composition rules.

Adding passwords later is easy. Removing them after users have them is a migration.

## How strict should session lifetime be?

Set both clocks from the blast radius of the account, not from a default:

| Account holds | Idle timeout | Absolute lifetime | Re-auth before sensitive actions |
|---|---|---|---|
| Nothing personal (prototype, public data) | Generous | Days | Not required |
| Personal data of the user only | Hours | Days, not weeks | Yes for password/MFA/delete |
| Other people's personal data, money, or admin power | Tens of minutes | Hours | Yes, always |

If a product cannot state which row it is in, it is in the third one until proven
otherwise.

## When is MFA worth the friction?

Introduce it when *any* of these is true: the account can spend money, can read another
person's data, can change access for others, or is a support/admin account. Below that
line, offer it and don't force it. Above it, forcing it is cheaper than the incident.

The decision that actually matters is not whether to offer MFA — it is whether the
recovery path is as strong as the factor (P15). An MFA rollout with email-only recovery
has bought a compliance checkbox, not security.

## Profile modulation

Reasoning profiles change the *depth of review*, never the starred floor:

- **Prototype** — AU-starred rules apply in full. The rest (session listing, sender
  constraining, JWKS cache tuning) may be deferred with a note.
- **Startup MVP** — starred rules plus everything under High. Enumeration safety and
  refresh rotation are not deferrable once real accounts exist.
- **Production / Enterprise** — the full checklist, plus a stated verification level from
  [owasp-asvs](../owasp-asvs/README.md) and evidence for each claim.

## When this pack is not the right one

- The question is "what may this authenticated user access?" → [backend/supabase RLS](../../backend/supabase/README.md)
  or [owasp-api-top-10](../owasp-api-top-10/README.md).
- The question is "what verification level do we claim?" → [owasp-asvs](../owasp-asvs/README.md).
- The question is "how do we secure the pipeline that ships this?" → [nist-ssdf](../nist-ssdf/README.md).
- The question is "what does the error message say?" → [content/ux-writing](../../content/ux-writing/README.md),
  bounded by AU50.
