# Review Checklist — TypeScript Pack

## High
- [ ] strict mode enabled. (TE1)
- [ ] No unjustified `any`. (TE2)
- [ ] External data schema-validated at the boundary. (TE3)

## Medium
- [ ] Mutually exclusive state modeled as discriminated unions. (TE4)
- [ ] Type assertions rare and justified. (TE5)

## Low
- [ ] No `any`/`unknown` leaking into public API surfaces. (TE6)
