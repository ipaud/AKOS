# Philosophy — OWASP Top 10 Pack

## Security is a floor, enforced by the constitution

Per [AKOS core/constitution.md](../../../core/constitution.md), security sits on the safety floor no reasoning profile or personal preference can trade away for convenience. The OWASP Top 10 is the concrete, industry-consensus definition of that floor for web applications — it's not an opinion about best practice, it's the empirically-derived list of what actually gets exploited most, most damagingly, across the real internet.

## Trust nothing that crosses a boundary

Nearly every entry in the Top 10 reduces to one principle: data or requests crossing a trust boundary (user input, another service's response, a URL, a serialized blob, a dependency's code) must be validated, authenticated, or constrained at that boundary — never trusted because "it came from our own frontend" or "no one would guess that endpoint." Attackers don't use your frontend; they talk to your API directly.

## Insecure design vs. insecure implementation

A04 (Insecure Design) was added to the 2021 list specifically to separate *bugs in secure designs* from *designs that were never secure to begin with* — no amount of careful coding fixes a design that has no access-control model, no threat model, or no rate limiting concept at all. Fixing insecure design happens at architecture time, not in a late security-review pass; catching it late is far more expensive than designing it out early.

## Defense in depth, not one gate

No single control is assumed perfect. Authentication failures, access-control failures, and injection failures each get independent, layered defenses (input validation *and* parameterized queries *and* least-privilege database roles, for instance) so that one control's failure doesn't equal total compromise.
