# Decision Framework — OWASP ASVS Pack

## Choosing the target ASVS level

| Signal | Level |
|--------|-------|
| Internal tool, small trusted audience, low-value data | L1 |
| Public app with user accounts and personal data | L1-L2 (lean L2 if data is sensitive: health, financial-adjacent) |
| Handles payments, health records, or significant personal data at scale | L2 |
| Regulated industry, critical infrastructure, high-value transactions, likely target of sophisticated attackers | L3 |

Map roughly to [AKOS reasoning profiles](../../../core/reasoning-profiles.md): Prototype/Internal Tool ≈ L1 floor only; Startup MVP ≈ L1 solid, L2 aspirational; Production ≈ L2; Enterprise ≈ L2 minimum, L3 where regulation/stakes demand it.

## When to invest in centralization vs. accept some duplication

Centralize (AS2) as soon as a second endpoint needs the same auth/validation logic — the [rule of three](../../architecture/martin-fowler-refactoring/mental-models.md) applies, but security logic should centralize earlier (on the second occurrence, not the third) because duplication risk here is asymmetric: one forgotten copy is a vulnerability, not just inconsistent UX.

## Business-logic modeling effort

Full state-machine modeling (AS9) is expensive; reserve it for workflows where abuse has real financial/business impact (checkout, financial transactions, limited-inventory reservations, approval workflows). Low-stakes workflows (updating a display name) don't need this level of rigor.

## Upgrading level over time

An application starting at L1 (Prototype/MVP) that gains real users/revenue should explicitly re-target L2 as part of its Production-profile promotion — this is a deliberate re-review against the higher bar, not an assumption that L1-era code automatically qualifies.
