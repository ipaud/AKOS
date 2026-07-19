# Mental Models — UX Writing Pack

Named models this pack contributes. Use them as diagnostic lenses during writing and review.

## The label-behaviour contract

Every control's words are a contract with the user, and the handler is the implementation. A review reads both sides: what does the label promise, what does the code do, do they match? Three failure shapes recur — the label promises more than the code does (`Send` that only flags a row), the label names a capability that isn't there (`(AI)` on a deterministic parser), and the label describes the mechanism rather than the effect (`Sync records` for what the user calls "get my latest orders").

**Diagnostic:** for each button in the diff, name the observable change a user could verify afterwards. If you can't, the label is unverifiable and probably untrue.

## Voice constant, tone dial

**Voice** is what the product always sounds like — one setting, defined once, expressed as a few adjectives with their opposites ("direct, not blunt; warm, not chummy"). **Tone** is the dial you turn per situation. The dial's input is the user's emotional state, which you read from the situation rather than guess:

| User state | Situation that creates it | Tone move |
|-----------|---------------------------|-----------|
| Curious | first run, exploring, empty states | warmest, teaching, can be playful |
| Focused | mid-task, repetitive work | shortest, no personality, get out of the way |
| Hesitant | commitment point, cost, irreversibility | precise, concrete, reassuring on specifics |
| Confused | validation failure they caused | plain, non-blaming, tells them the rule |
| Frustrated | system failure, lost work, outage | shortest and plainest, own it, no humour |
| Relieved | recovery, success after failure | brief confirmation, no celebration |

**Diagnostic:** read the string imagining the user has just lost thirty minutes of work. If it now reads as smug, the tone was set for the wrong state.

## The three questions

Any message about something that happened answers, in this order: **what happened → why → what now**. Errors need all three when the cause is known; success messages usually need one and a half (what happened, and where the result is). A message that stops after "what happened" is a dead end, which is the single most common defect in interface copy.

**Diagnostic:** cover the screen and read only the message. Can the user take an action from it alone?

## The microcopy ladder

When a user might not understand something, options rank by cost to them:

1. **Remove the need** — redesign so nothing needs saying.
2. **Rename** — better words on the control itself.
3. **Restructure the control** — split, reorder, or set a default so the question disappears.
4. **Inline hint** — one short line, adjacent, always visible.
5. **Progressive disclosure** — expandable detail, help icon.
6. **Documentation** — assume unread.

Never write at rung 4 while rungs 1–3 are unexplored. Copy that explains a control is evidence about the control, not a solution.

## The terminology ledger

Every concept in a product owns exactly one user-facing word, recorded in a list that reviewers can check against. The ledger has three columns: the concept, the approved word, and the banned synonyms (including the internal engineering word, which is the usual leak source). Adding a word is a decision; using a second one for the same thing is a bug.

**Diagnostic:** grep the UI strings for the banned column. Hits are findings, not style preferences.

## The four zero states

"No data" is four different situations that need four different messages:

1. **First run** — nothing exists yet. Teach: what belongs here, why it's useful, one action to create the first one.
2. **No results** — a filter or search excluded everything. Explain what was searched and offer to widen or clear it.
3. **Cleared** — the user emptied it themselves. Confirm calmly; offer undo if it exists.
4. **Unavailable** — data couldn't be loaded. That's an error state, not an empty one: say so and offer retry.

Shipping one generic message for all four is how products end up telling a brand-new user that their search returned nothing.

## Reading budget

Users read the fewest words that let them act, and they read them in a fixed order: the thing they clicked, the thing that changed, then anything else. Words spent before the answer are words spent on nothing. This is why front-loading matters more in interfaces than in prose — the first two or three words of a label often decide whether the rest is read at all.

## The anxiety map

Walk a flow and mark every point of irreversibility, cost, exposure to others, or data handover. Those marks are where microcopy earns its keep, and each one has a standard question behind it: *what exactly happens, can I undo it, who sees it, what will it cost, when does it stop*. Unmarked points need no reassurance; marked points that lack it are findings.

## Interrupt cost

A notification's value must exceed the cost of taking the user out of what they were doing. Cost rises with intrusiveness — inline < toast < banner < modal < push. The model forces the pairing question: does this message need to be *retained*, *acted on*, or merely *observed*? Only observed information belongs in something that disappears.

## Strings as shipped artifacts

A string is not the sentence on your screen; it is a template that will be translated, grow by up to half its length, be read aloud without visual context, appear on a lock screen, and possibly be truncated. Writing at the sentence level (not the fragment level) and expecting growth are what keep it intact through all of that.
