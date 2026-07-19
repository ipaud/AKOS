# Heuristics — UX Writing Pack

Fast defaults with known exceptions. Try these first; deviate with a reason.

## Buttons and actions

- **Verb + object, two to three words.** "Save draft", "Invite teammate". Exception: a single verb is fine when the object is the whole screen and unambiguous.
- **The button repeats the dialog's verb.** If the title asks about deleting, the button says "Delete", never "Yes" or "OK".
- **Name the destination when you're sending someone somewhere.** "Continue to payment" beats "Continue" whenever the next step costs money, time, or trust.
- **Say the count when the action is bulk.** "Archive 14 orders" — the number is the safety mechanism.
- **The escape option must never sound like an action.** In a "discard changes?" dialog the safe choice is "Keep editing", not "Cancel" (cancel *what* — the edits or the dialog?).
- **If you can't name the effect, don't ship the label.** Trace the handler first; the inability to describe it is the finding.

## Errors

- **Three beats: what happened → why → what to do.** Drop "why" only when the system genuinely doesn't know.
- **Lead with the state, not the apology.** "Card was declined by your bank" before any "Sorry".
- **Give the rule, not the violation.** "Use at least 8 characters" beats "Password too short" — one of them tells you what to type.
- **Never show a bare code.** A reference ID may accompany plain language for support; it may not replace it.
- **No humour, no mascots, no exclamation marks in failure states.** The user is not in the mood, and if data was lost, personality reads as contempt.
- **If the system can fix it, don't message about it.** Trim the whitespace, normalize the case, parse the pasted format. A message about something the code could have handled is a defect wearing a message.

## Empty states

- **Never negate and stop.** "No items." is not an empty state; it's the absence of one.
- **Three lines maximum:** what lives here · why it's worth having · one action.
- **Different message per zero state.** First run teaches, no-results offers to widen the filter, cleared confirms, failed-to-load offers retry.
- **Put the primary action in the empty state itself**, not only in a toolbar the new user hasn't noticed yet.

## Confirmations and destructive actions

- **Undo beats confirm.** A dialog interrupts everyone to protect the rare mistake; undo protects the mistake without taxing the rest.
- **Confirm only what's irreversible, expensive, or visible to others.** Confirmation on reversible actions trains users to click through the ones that matter.
- **Name the object and the scope in the dialog.** "Delete 'Q3 forecast' and its 4 revisions?" — vagueness here is where accidents come from.
- **"This can't be undone" only when true.** If a trash exists, say where it goes and for how long.
- **Typed confirmation only for the catastrophic** (deleting an org, dropping production data). Everywhere else it's ceremony.

## Forms

- **Visible label always; placeholder never carries meaning.** It disappears exactly when the user needs it.
- **Hints go above the input, before typing** — a rule discovered after failure is a rule delivered late.
- **Show format by example, not by rule.** "e.g. +34 600 123 456" beats a sentence about accepted formats — better still, accept everything and normalize.
- **Mark the minority case.** If most fields are required, mark the optional ones, and do it in words.
- **Explain any field a user might resent.** Phone number, birthdate, company size: one short line on why it's asked, next to it.

## Notifications, toasts, progress

- **Toasts hold observations only.** If it must be retained or acted on, it belongs in a persistent surface.
- **A notification must make sense with no screen behind it** — lock screens and email subjects strip all context.
- **Name the operation in progress copy.** "Uploading 3 of 12" beats a spinner; a bare spinner past a couple of seconds is an unanswered question.
- **Success copy names the resulting state and points at the result.** "Invoice sent to maria@…" plus a link beats "Success!".
- **Silence is legitimate.** When the change is visible on screen, the change *is* the feedback; adding a toast is noise.

## Voice, tone, terminology

- **Read it back in the user's worst moment.** If it survives being read by someone who just lost work, the tone is right.
- **Personality goes where stakes are low** — onboarding, empty states, idle moments. Never at payment, deletion, or failure.
- **Grep for the engineering vocabulary before shipping**: stub, null, invalid, payload, sync, entity, record, exception, config. Each hit is a translation task.
- **When two words tempt you, keep the boring one.** The word users would type into a search box wins over the one the team enjoys.
- **New term? Add it to the ledger or don't use it.** Untracked terms are how one concept becomes three words.

## Cutting

- **Halve it, then read it.** Most interface sentences survive losing their first clause.
- **Delete any sentence that could appear in any product.** Welcomes, congratulations, "we're excited" — all cuttable without loss.
- **If text explains a control, fix the control.** Instructions are evidence, not solutions.
- **Count the strings on the screen.** More than about seven pieces of text competing for attention means the screen, not the copy, needs work.

## Translation

- **Write whole sentences with named placeholders.** Never build a sentence from ordered fragments.
- **Assume 40% growth** and never design a label into a fixed-width box.
- **Let a plural API handle plurals.** English's two forms are not a universal rule.
- **Leave a note for the translator** on every ambiguous string — "Open" is a verb here, not an adjective.
