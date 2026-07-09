# Mental Models — Krug Pack

Named models this pack contributes to design reasoning. Use them as diagnostic lenses.

## Scanning, not reading

Users treat pages like billboards at 100 km/h: they scan for words that match their goal and ignore the rest. Implication: hierarchy, headings, and link labels carry the whole page; body text is a fallback. If information only exists in a paragraph, most users don't have it.

**Diagnostic:** squint-test the page. What survives — is it the right stuff?

## Satisficing

Users don't hunt for the *best* option; they click the *first plausible* one. If it's wrong, back button, try again — guessing is cheaper than analyzing. Implication: penalties for wrong guesses must be low (fast back, no lost state), and the plausible-looking option had better be the right one.

**Diagnostic:** on this screen, what would a hurried person click first? Is that the correct move?

## Muddling through

Most users never learn how anything actually works; they find something that works and repeat it forever, even if it's suboptimal. Implication: don't count on onboarding being remembered, don't punish "wrong" paths that work, and don't break the path users have memorized.

## The self-evidence ladder

Every element sits on a ladder: **self-evident** (understood at a glance) → **self-explanatory** (understood with a small amount of reading, in place) → **requires figuring out** (fails). Aim for rung 1; accept rung 2 when the concept is genuinely new; treat rung 3 as a defect.

## The goodwill reservoir

Finite, personal, refillable. Withdrawals: hiding info (support numbers, prices), punishing formats ("no dashes in card number"), amateur visuals, marketing fluff, dead ends. Deposits: obviousness, effort-saving defaults, honesty about problems, printable/copyable info, graceful errors.

## Navigation as physical space

Users experience a site like a building: navigation is signage. It answers, at all times: *Where am I? What's here? How do I get around? How do I get home? How do I search?* Unlike physical space, web users teleport in (deep links) — every page must orient a visitor who has seen nothing else.

## Trunk test

Teleport a user to a random interior page, blindfolded. Can they immediately identify: site name, page name, major sections, local navigation, "you are here" indicators, search? If not, the navigation fails as signage.

## The three usability-test truths

1. Testing one user is 100% better than testing none.
2. Testing one user early beats testing fifty at the end.
3. The point isn't to prove anything — it's to inform your judgment.

Three users per round finds the worst problems; the worst problems mask the next tier, so fix and re-test rather than recruiting more.

## Mobile as forcing function

Small screens don't just shrink pages; they force the prioritization the desktop page always needed. If features must be ranked for mobile, that ranking was the truth all along. Beware trading usability for a cool mobile gesture nobody can discover, and never punish mobile users with a crippled subset of the product.
