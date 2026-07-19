# Decision Framework — GOV.UK Content Design Pack

Domain-specific decision rules. Compose with [core/decision-framework.md](../../../core/decision-framework.md).

## Should this content exist at all?

Run in order; stop at the first "no".

1. Can you write a user need statement naming a person outside the organisation? No → do not publish.
2. Is there evidence the need exists (search volume, support tickets, research, task failure)? No → publish provisionally with a 3-month review trigger, or wait.
3. Does an existing page already answer it? Yes → improve that page. Never add a second answer.
4. Can you name an owner and a review date? No → do not publish (GC14). Unowned content is a future defect.

Publishing to satisfy an internal stakeholder is a recorded exception, not a route through this list.

## Choosing the format

| The content is | Format | Never |
|----------------|--------|-------|
| An ordered sequence of actions | Numbered steps | Prose paragraphs |
| Parallel, non-ordered options | Bullets with a lead-in line | A comma-separated sentence |
| Items compared on several attributes | Table with header row | Repeated near-identical paragraphs |
| Branching eligibility (3+ conditions) | Question sequence, or split pages | Nested "if… unless… except…" prose |
| One fact the reader needs | A single sentence, first | A section |
| Explanation, rationale, context | Prose — after the answer | Prose *before* the answer |

Default assumption: it is not prose. Prose must win the argument, not receive it by default.

## New page vs edit vs split vs retire

- **Edit** when the need is already covered but the answer is wrong, buried, or badly worded. This is the default and covers most cases.
- **Split** when one page serves two distinct audiences or tasks, and a major branch ("if you are a business, instead…") has appeared.
- **New page** only when a genuinely uncovered need exists and no host page can absorb it without breaking GC9.
- **Retire** when the need has gone, the content is superseded, or the page cannot be maintained. Redirect to the nearest correct answer; record the reason.

Bias order: retire > edit > split > new. Estates grow by default; the framework must push the other way.

## The user's word vs the correct term

Decision order:

1. If the plain term is accurate → use it alone.
2. If the plain term is what users search for but the official term is binding → lead with the user's term, put the official term in brackets at first mention, use one consistently after that.
3. If the official term is legally or clinically binding *and* substituting it changes meaning → use it, define it plainly at first use, and shorten the surrounding sentences to pay for the added cost.
4. Never keep the specialist term for tone, tradition, internal consistency, or because the source document used it.

## Completeness vs the answer

When "but it's more complicated than that" is raised:

1. Does the complication change what the reader does? No → cut it entirely.
2. Yes, for a minority → give the majority answer first, then a clearly labelled section for the exception.
3. Yes, for everyone → the page has more than one need; split it.

Never resolve this by hedging the main answer. A qualified answer that nobody can act on is worse than a clear answer plus a documented exception.

## Plain language vs precision

These conflict far less than claimed. When they genuinely do:

- Precision wins on the **fact**; plain language wins on the **sentence around it**. Keep the exact threshold, date or term; strip the register.
- If plainness would create ambiguity a reader could act wrongly on, keep the precise wording — and treat the added cost as a debt to pay elsewhere on the page (shorter sentences, a table, an example).
- Legal review changing meaning is legitimate. Legal review changing only tone is refused and escalated.

## When a page is failing, what to change first

Cheapest first, and re-measure between steps:

1. Title and first sentence (front-loading) — usually the whole problem.
2. Vocabulary swap to the user's terms.
3. Reformat structured content into steps or a table.
4. Split by task.
5. Restructure the surrounding navigation.
6. Rewrite from the need statement.

Escalate only when the previous step demonstrably failed against evidence, not against opinion.

## When to retire rather than fix

Retire when any two hold: negligible traffic over two review cycles; no owner willing to maintain it; superseded by another page; the need it served no longer exists; it is factually wrong and nobody can confirm the correct answer. A page that is wrong and unownable is retired immediately, not scheduled — wrong content is worse than absent content.
