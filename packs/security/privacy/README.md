# Pack: Privacy — Personal Data as an Engineering Constraint

**Domain:** Security · **Authority:** Level 1 (EU regulation, EDPB, AEPD) · **Version:** 1.0.0

Turns EU data-protection law into checkable rules for the parts a codebase actually
decides: which fields exist, why, who they go to, how long they live, and what happens
when someone asks for them back.

Independent distillation for personal engineering use. Not affiliated with or endorsed by
the European Union, the EDPB, or the AEPD. See [references.md](references.md) for the
normative texts.

**Engineering guidance, not legal advice.** This pack helps build a system that *can*
comply. It does not tell you whether you do, and it does not adjudicate whether a specific
processing is lawful — that is a lawyer's call.

## When to load this pack

- Designing a schema that will hold anything about a person.
- Adding analytics, session recording, a support tool, an email provider, or a model API.
- Building signup, account deletion, data export, or a consent surface.
- Any review of a deployed product with real users.

The trigger is **one real person's data** — not scale, not launch, not funding.

## What's inside

| File | Highlights |
|------|-----------|
| [principles.md](principles.md) | P1–P18. Collection is the decision you can't undo; privacy is a schema property, not a policy document. |
| [engineering-rules.md](engineering-rules.md) | PR1–PR49, `★` marking the safety floor. Includes a Supabase/Postgres mapping. |
| [review-checklist.md](review-checklist.md) | Binary checks by severity, each citing its rule. |
| [heuristics.md](heuristics.md) | Defaults while the design is open — starting with "don't collect it". |
| [decision-framework.md](decision-framework.md) | Does this apply at all, which lawful basis, where data lives, retention numbers, when an assessment precedes the build. |
| [anti-patterns.md](anti-patterns.md) | The just-in-case column, the retention policy nobody enforces, the deletion that deletes one table, consent theatre. |
| [scoring-rubric.md](scoring-rubric.md) | Deductions, hard caps, anchors at 95/85/72/55. |
| [prompt-fragments.md](prompt-fragments.md) | Build-mode constraint block, review lens, tight-budget one-liner. |
| [glossary.md](glossary.md) | The terms this pack uses precisely. |
| [references.md](references.md) | The four normative sources, plus the scope note. |

## Core claim, one line

Privacy fails as a schema decision long before it fails as a legal one: the exposure is
created the moment a field is added, and every control after that is damage limitation.

## Why it lives under `security/`

Privacy is not security — they answer different questions about the same data. It is filed
here because a one-pack `legal/` domain would be speculative structure, and because it
routes through the same review lens. It moves when a second legal pack exists.

## Related packs

[auth](../auth/README.md) · [owasp-top-10](../owasp-top-10/README.md) ·
[owasp-asvs](../owasp-asvs/README.md) · [backend/supabase](../../backend/supabase/README.md) ·
[backend/postgres](../../backend/postgres/README.md) ·
[content/ux-writing](../../content/ux-writing/README.md)
