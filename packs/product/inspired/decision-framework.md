# Decision Framework — Inspired Pack

## Should this go through full discovery?

| Signal | Action |
|--------|--------|
| Novel problem, uncertain value/usability, meaningful build cost | Full four-risk discovery before build |
| Well-understood pattern (e.g. "add CSV export," proven demand) | Light discovery (feasibility check only), build directly |
| High business viability risk (legal, pricing, compliance) | Involve those stakeholders in discovery explicitly, don't defer to launch |
| Reversible, cheap, low-risk experiment | Ship a lightweight version and measure — the fastest discovery is sometimes production |

## Prototype fidelity choice

Choose the *cheapest* prototype that resolves the *riskiest* open question:
- Value risk uncertain → concierge test, landing page, or customer interview with a mockup.
- Usability risk uncertain → clickable prototype + 5-user think-aloud test ([Krug](../../ux/steve-krug/decision-framework.md)).
- Feasibility risk uncertain → engineering spike, timeboxed.
- Viability risk uncertain → stakeholder review (legal/finance/sales) before build commitment.

## When a feature-team backlog is unavoidable (short term)

Some contexts (regulatory mandates, contractual commitments, urgent fixes) legitimately require pre-specified output delivery. Treat these as an explicit exception, not the team's steady-state operating model — and still ask "what outcome does this output serve?" even when the *what* is fixed.

## Killing an idea

An idea fails discovery when any one of the four risks can't be resolved to an acceptable confidence within a reasonable discovery budget. Killing it early is success, not failure — the alternative is learning the same thing after a multi-month build.
