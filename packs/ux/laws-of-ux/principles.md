# Principles — Laws of UX Pack

Each law: statement → mechanism → operational rules.

## L1 — Hick's Law

**Statement:** decision time increases with the number and ambiguity of choices (logarithmically, for uniform choices).
**Mechanism:** each option must be perceived, parsed, and compared before commitment.
**Rules:**
- Cut options that serve <5% of users from primary surfaces; disclose progressively.
- Chunk long option sets into labeled groups — grouping resets the comparison space.
- Highlight a recommended option; a good default converts a choice into a confirmation.
- Never apply to expert surfaces reflexively: familiar choice sets are scanned, not deliberated (Hick's weakens with practice).
- Onboarding: one decision per screen beats a settings wall.

## L2 — Fitts's Law

**Statement:** time to acquire a target is a function of distance to it and its size.
**Mechanism:** pointing is a ballistic + correction movement; small/far targets need more correction.
**Rules:**
- Frequent actions: large targets, near the interaction locus (cursor position, thumb zone).
- Destructive actions: smaller-or-distant relative to frequent ones — inverse Fitts as safety ([Norman NR19](../don-norman/engineering-rules.md)).
- Screen edges/corners are effectively infinite-size targets on desktop (cursor pins) — prime real estate for persistent controls.
- Related sequential controls (wizard Next, form fields) placed to minimize travel.
- Touch minimums: ≥44px targets, ≥8px gaps ([Krug ER8](../steve-krug/engineering-rules.md)).

## L3 — Jakob's Law

**Statement:** users spend most of their time on other products; they prefer yours to work the same way.
**Mechanism:** transfer — existing mental models applied for free where patterns match, violated at cost where they don't.
**Rules:**
- Default to platform/industry convention for chrome, nav, forms, commerce flows.
- Spend novelty exclusively on the differentiator ([Krug decision framework](../steve-krug/decision-framework.md)).
- When changing an established product's pattern, offer a transition period (both paths / announcement / undoable switch).

## L4 — Miller's Law

**Statement:** working memory holds about 7±2 chunks; practical design number is lower (3–5).
**Mechanism:** chunking — grouping raw items into meaningful units — is how humans expand capacity.
**Rules:**
- Never require carrying information between screens ([NN/g H6](../nielsen-norman-group/principles.md)); the world remembers, not the head.
- Chunk displayed data: phone numbers, card numbers, IDs formatted in groups (also forgiving input, Krug ER20).
- Nav menus, toolbars, wizard steps: prefer ≤5–7 top-level items *because of scanning cost*, not a magic memory number — Miller's is about memory, misciting it for menu length is folklore; Hick's is the right citation there.

## L5 — Tesler's Law (Conservation of Complexity)

**Statement:** every application has irreducible complexity; the only question is who absorbs it — the system/developer or the user.
**Mechanism:** complexity removed from the interface doesn't vanish; it moves.
**Rules:**
- Push inherent complexity into: smart defaults, inference (detect timezone/locale/card type), normalization (accept all formats), automation (auto-save).
- Budget: every field, choice, or instruction shipped to users is complexity you charged them; justify each.
- Simplification that deletes *capability* isn't Tesler-compliant — it's scope cut; be honest about which you're doing.
- Beware over-absorption: hiding necessary control (no manual override for wrong inferences) trades complexity for helplessness ([Norman H3 exits](../nielsen-norman-group/principles.md)).

## L6 — Peak-End Rule

**Statement:** experiences are remembered by their emotional peak and their ending, not their average.
**Mechanism:** memory samples, it doesn't integrate.
**Rules:**
- Identify the peak (moment of most emotion — success, aha, or worst frustration) and the end (completion, confirmation, sign-off) of every key journey; design those two deliberately.
- Endings: never let a flow end on a form or a dead confirmation — end on accomplishment ("Invoice sent ✓ — track it here").
- Worst-moment engineering: error states and waiting are candidate negative peaks; invest there disproportionately.
- Applies to sessions too: the last interaction before close colors the session's memory.

## L7 — Serial Position Effect

**Statement:** first (primacy) and last (recency) items in a sequence are best remembered; middles blur.
**Rules:**
- Nav and menus: most important items first and last; park the utilitarian middle.
- Lists of features/benefits/steps: lead with the differentiator, end with the call to action.
- Long forms/wizards: users best recall what step 1 and the final step asked — repeat critical context mid-flow (Miller assist).

## L8 — Von Restorff Effect (Isolation Effect)

**Statement:** the item that differs from its group is the one remembered — and attended.
**Rules:**
- Exactly one visually isolated element per decision surface: the primary action ([Krug ER12](../steve-krug/engineering-rules.md)).
- Distinctiveness budget: highlighting everything highlights nothing; each additional accent devalues the rest.
- Use isolation for genuine outliers: destructive actions, current plan, live status.
- Accessibility: difference must not be color-only ([WCAG](../wcag/engineering-rules.md)).

## L9 — Aesthetic-Usability Effect

**Statement:** visually pleasing interfaces are *perceived* as more usable, and users tolerate their flaws longer.
**Rules:**
- Polish is functional: it buys trust, patience, and error tolerance ([Norman P11](../don-norman/principles.md)).
- Testing hazard: attractive prototypes suppress reported problems — in usability tests, probe beyond satisfaction ratings; watch behavior, not praise.
- Never let the effect launder real defects: "it demos well" is not a usability result.

## L10 — Goal-Gradient Effect

**Statement:** effort accelerates as the goal nears; perceived progress motivates.
**Rules:**
- Show progress in every multi-step flow — and start it non-zero when honest (profile 20% complete after signup step).
- Break long journeys into visible sub-goals with completion moments.
- Endowed progress must be honest: fake inflated bars burn trust when discovered (goodwill withdrawal, [Krug](../steve-krug/mental-models.md)).
- Near-complete states are high-leverage: "1 step left" prompts convert; abandoned near-done carts merit recovery.
