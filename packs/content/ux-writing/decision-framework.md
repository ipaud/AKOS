# Decision Framework — UX Writing Pack

Decision rules for interface-copy calls. Compose with [core/decision-framework.md](../../../core/decision-framework.md).

## Cut, rename, or explain

Climb the microcopy ladder from the bottom and stop at the first rung that works:

1. Remove the need (redesign, default, fewer steps)
2. Rename the control
3. Restructure the control (split, reorder, group)
4. Inline hint, one line, always visible
5. Progressive disclosure
6. Documentation

**Rule:** never write at rung 4+ while 1–3 are unexplored. If you are drafting a sentence that explains what a button does, the finding is the button. Record which rung you stopped at — reviewers check whether a lower one was skipped for convenience.

## Naming a thing

Order of preference: **the word users already use** > the word the industry uses > a plain descriptive phrase > an invented term. Invent only when the concept genuinely doesn't exist elsewhere in the user's world, and then define it in place the first time it appears.

Tests before adopting a term: would a user type it into a search box? Does it survive being read alone in a notification? Does it already mean something else in this product? Is it in the terminology ledger — and if a synonym is there, why is this one better? Adopting a new term means renaming *every* existing instance in the same change.

## Confirm, undo, or neither

| Situation | Choose |
|-----------|--------|
| Reversible, low cost, visible result | Neither — the changed screen is the feedback |
| Reversible, but the user may not notice it happened | Brief success message, no confirmation |
| Reversible with effort (restorable from trash) | Undo affordance with a stated window |
| Irreversible, cheap to redo | Confirmation dialog naming object and scope |
| Irreversible, expensive or visible to others | Confirmation naming object, scope, and consequence |
| Catastrophic and organization-wide | Typed confirmation |

Undo outranks confirmation whenever it is technically possible: a dialog taxes every user to protect the rare mistake. Stacking both is a smell — pick the one that matches the true reversibility, and make the copy say which it is.

## Where a message goes

Decide by what the user must do with the information:

- **Must retain or act on later** → persistent surface (inline panel, list item, status area). Never a toast.
- **Must act on now, blocking** → modal or inline block at the point of action.
- **Must notice, no action** → toast or inline status.
- **Would like to know, no urgency** → the screen itself; consider saying nothing.
- **Happens while away from the product** → notification, written to stand alone.

Escalate intrusiveness only when the interrupt cost is clearly lower than the cost of missing the message. Two messages for one event is always the wrong answer (UWE34).

## Setting tone for a situation

Read the user's state from the situation, then set the dial:

1. **What are the stakes?** Money, data loss, visibility to others → precision up, personality off.
2. **Who caused it?** System fault → own it plainly, no humour. User slip → non-blaming, give the rule.
3. **How reversible is it?** Irreversible → concrete and specific about consequences.
4. **Are they in a hurry?** Repetitive task → shortest possible; strip everything decorative.
5. **Is this their first time?** Exploring → warmest register, teaching allowed.

Voice never changes; only warmth, brevity, and formality move. When in doubt, take one step plainer — plainness is never the thing users complain about.

## When brand voice and clarity collide

Clarity wins on anything users navigate or commit by: labels, actions, errors, confirmations, money, and data. Voice expresses itself in the places where nothing is at stake — empty states, onboarding, success moments, idle copy, and the rhythm of sentences rather than the choice of nouns.

If a brand term must appear on a functional control, pair it with the plain word rather than replacing it, and treat the pairing as debt with a review date.

## Specific vs. safe wording

When legal, support, or product pressure pushes toward vagueness ("Not available", "There was a problem"), decide with:

- Does the system **know** the specific cause? If no, vagueness is honest — say what's unknown and offer the next step.
- Does the specific cause expose security-sensitive detail, another user's data, or something legally constrained? If yes, generalize deliberately and record why.
- Otherwise, **be specific.** The vague version transfers the diagnostic work to the user and generates support load — quantify that when arguing the case.

## Writing under translation constraints

Choose the plainer construction whenever a clever one would need restructuring per language: no idioms, no puns on product terms, no sentences whose meaning depends on English word order in a placeholder. When punchiness and translatability genuinely conflict on a high-visibility string, keep punchy for the source locale only if the string is isolated, flagged for transcreation, and the layout tolerates growth — otherwise translatable wins.

## Deciding whether to ship the string at all

Before adding any new text, answer: what does the user do differently because they read this? If the answer is "nothing" or "feel better about us", cut it. If the answer is "understand the control they're looking at", climb the ladder. Only "take a specific action they otherwise couldn't" justifies new copy on a task screen.
