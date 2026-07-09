# Decision Framework — Krug Pack

Domain-specific decision rules for usability calls. Compose with [core/decision-framework.md](../../../core/decision-framework.md).

## Convention vs. innovation

**Default: convention.** Deviate only when both hold:

1. The replacement is self-evident to a first-time user (testable claim — test it), **or** the value gained is large enough to justify a learning cost.
2. The pattern isn't safety-relevant (navigation, checkout, destructive actions stay conventional).

Score the temptation honestly: is the novel pattern serving users, or the portfolio?

## Clarity vs. cleverness (naming, copy, branding)

Decision order: **obvious > clever-and-clear > clever**. Brand voice lives in tone, illustration, and micro-moments — never in the words users navigate by. Test: would a distracted user, mid-task, parse it instantly? If unsure, it's not clear.

## Cutting vs. explaining

When users might not understand something, the options rank:

1. **Remove the need** (redesign so no explanation is required)
2. **Relabel** (better words in place)
3. **Explain in place** (one short line, adjacent)
4. **Tooltip/help icon** (secondary info only)
5. **Documentation page** (last resort; assume unread)

Never jump to 3–5 while 1–2 remain unexplored.

## Depth vs. breadth in navigation

Prefer depth with strong scent over broad shallow menus that force comparison of many ambiguous options. Rule of thumb: each level's options should be instantly distinguishable; if users must open items to know what they are, the labels failed — fix labels before restructuring.

## When to test vs. when to just fix

- Observed confusion in testing → fix, no debate.
- Team disagreement about user behavior → test (3 users settles it faster than the meeting).
- Obvious violation of this pack's engineering rules → fix without testing; testing is for genuine unknowns.
- New flow, pre-launch → at least one guerrilla round (3 users, think-aloud) before real traffic.

## Fix sizing ("do the least you can do")

For each observed problem choose the smallest of: reword → reorder/re-emphasize → add in-place cue → restructure component → redesign flow. Escalate only when the smaller fix demonstrably failed a re-test. Log the bigger fix as debt rather than blocking on it.

## Registration/data-capture walls

Asking users for anything (sign-up, email, permissions) before delivering value is a goodwill withdrawal. Decision rule: demonstrate value first; ask at the moment the ask unlocks obvious benefit; always explain what happens with the data in one line. Forced early registration requires product-owner sign-off as an explicit tradeoff.
