# Scoring Rubric — Material Design Pack (System Fidelity)

Feeds UX/frontend scores on Material surfaces.

| Finding | Deduction |
|---------|-----------|
| Semantics broken by theming / custom components without semantics | −25 (CRITICAL — also WCAG) |
| Actionable errors snackbar-only on primary flows | −10 (HIGH) |
| Pyramid bypass as a pattern (hex-ridden components) | −10 (HIGH) |
| State layers missing/amputated | −10 (HIGH) |
| Baseline theme in production | −10 (HIGH — template look) |
| Stretched-phone large-canvas UI | −10 (HIGH) |
| FAB abuse, filled-button inflation | −4 per screen, cap −12 (MEDIUM) |
| Elevation soup, type-role bypass, M2/M3 mixing | −4 each (MEDIUM) |
| Motion-semantics mismatches, density-by-squeezing | −1 each, cap −6 (LOW) |

Modifiers: full token pyramid + dynamic-color survivability: +5.

Anchors: **92** themed, token-clean, adaptive · **80** solid system, some bypass holes · **70** stock-default look or phone-only layouts · **<60** broken semantics/states after theming — BLOCKED.
