# Pack: GOV.UK Content Design

**Domain:** Content · **Authority:** Level 2 (industry authority) · **Version:** 1.0.0

Operationalizes the Government Digital Service method of content design: content is not writing that decorates a product, it is the act of giving a person the answer to their question, in their words, at the moment they need it. Nice words that meet no need are waste. Content nobody maintains is a defect.

Independent distillation for personal engineering use. Not affiliated with or endorsed by the source authors. See [references.md](references.md) for the originals — read them; this pack is a lossy operational index, not a substitute.

## When to load this pack

- Writing or reviewing any surface whose job is to **explain, instruct, or answer**: help centres, docs, onboarding guides, policy and legal pages, support articles, transactional email, in-product guidance.
- Deciding how content should be *structured* — prose vs list vs table vs step-by-step.
- Auditing an information architecture that mirrors the organisation instead of the user's task.
- Running a content lifecycle pass: what to update, what to split, what to **retire**.
- Whenever someone asks for "copy" and what is actually missing is an answer.

## Scope boundary

This pack covers **content design** — meeting an information need. Interface microcopy (button labels, error strings, empty states, voice and tone systems) belongs to [ux-writing](../ux-writing/README.md). Screen-level usability belongs to [steve-krug](../../ux/steve-krug/README.md). They meet at the edges by design: when the question is about a *control's label*, defer to ux-writing; when it is about *the answer on the page*, this pack wins.

## What's inside

| File | Highlights |
|------|-----------|
| [philosophy.md](philosophy.md) | Content as a service; plain language as cognitive cost, not capability |
| [mental-models.md](mental-models.md) | User need statement, front-loading, task-not-topic, content decay |
| [principles.md](principles.md) | GC1–GC16 — durable rules of content design |
| [heuristics.md](heuristics.md) | Fast calls on need, structure, words, and lifecycle |
| [engineering-rules.md](engineering-rules.md) | GCE1–GCE40 — numeric, checkable rules |
| [decision-framework.md](decision-framework.md) | Format choice; new vs edit vs retire; user word vs legal term |
| [anti-patterns.md](anti-patterns.md) | Org-chart content, hidden actor, question nobody asked, zombie pages |
| [review-checklist.md](review-checklist.md) | Binary pass/fail content review, by severity |
| [examples.md](examples.md) | Invented before/after cases with the rule applied |
| [prompt-fragments.md](prompt-fragments.md) | Injectable blocks for build and review agents |
| [scoring-rubric.md](scoring-rubric.md) | Content-design scoring, 0–100 |
| [glossary.md](glossary.md) | Terms this pack uses precisely |

## Core claim, one line

Start from the user's question in the user's words — and a page that answers no question should be retired, not rewritten.

## Related packs

[ux-writing](../ux-writing/README.md) · [steve-krug](../../ux/steve-krug/README.md) · [wcag](../../ux/wcag/README.md) · [nielsen-norman-group](../../ux/nielsen-norman-group/README.md)
