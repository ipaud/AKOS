# Scoring Rubric — React Pack

| Finding | Deduction |
|---------|-----------|
| Direct state mutation causing bugs | −10 (HIGH) |
| Conditional hook calls | −10 (HIGH) |
| Index keys on reorderable lists | −6 (MEDIUM) |
| Redundant state-sync effects | −6 (MEDIUM) |
| Everything-is-client-component pattern | −4 (MEDIUM) |
| Unjustified reflexive memoization | −2 (LOW) |
| Boolean-prop proliferation | −2 (LOW) |

Anchors: 90 clean hooks/state discipline, appropriate server/client split · 75 solid with gaps · 60 sync-effect and key bugs present · <50 broken rendering behavior from mutation/hook violations.
