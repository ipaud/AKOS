# Scoring Rubric — TypeScript Pack

| Finding | Deduction |
|---------|-----------|
| strict mode disabled | −15 (HIGH) |
| Unvalidated external data cast with `as` | −10 (HIGH) |
| Unjustified `any` on primary logic paths | −10 (HIGH) |
| Boolean-flag-soup state instead of discriminated union | −4 (MEDIUM) |
| Non-null assertion habitually masking null checks | −4 (MEDIUM) |
| `@ts-ignore` without a fix-tracking note | −2 (LOW) |

Anchors: 90 strict, validated boundaries, unions over flags · 75 solid with a few any's · 60 loose typing throughout · <50 strict mode off, casts everywhere.
