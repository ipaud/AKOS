# Anti-Patterns — UX Writing Pack

Named failure modes. Detection cue → why it fails → fix. The first block covers the copy defects that mislead users about system behaviour; those are correctness bugs, not style issues.

## The lying label

**Detect:** the control's verb names an effect the handler doesn't produce — a "send" that writes a status field, a "publish" that saves a draft, an "invite" that creates a row and dispatches nothing. Found by reading the handler, never by reading the screen.
**Why it fails:** the user believes the effect happened and acts on that belief downstream — waiting for a reply that was never sent, assuming a colleague was notified.
**Fix:** rename to the real effect ("Mark as sent"), or implement the promised effect. Never ship the mismatch as "we'll implement it later"; the label is live the moment it merges.

## Phantom confirmation

**Detect:** success copy fired before the result is known, unconditionally after dispatch, or from a `finally`; success wording on an operation that only queued or only persisted locally.
**Why it fails:** it manufactures certainty the system doesn't have, and it makes *every* confirmation in the product untrustworthy once a user catches one.
**Fix:** bind confirmations to the success branch; where the outcome is genuinely later, say what's true now ("Queued for sending").

## Capability cosplay

**Detect:** labels advertising capabilities the feature doesn't have — "(AI)" on deterministic logic, "Import" on a control that accepts no file, "Sync" on a one-way read, "Auto-" on something manual.
**Why it fails:** it sets expectations the product cannot meet and usually survives from a planning-era name after scope was cut.
**Fix:** re-derive the label from what shipped, at merge time. Treat descoping as a copy change, not just a code change.

## Euphemistic status

**Detect:** a generic unavailability label ("Not available", "Unavailable", "—") where the system knows the actual reason ("already committed for these dates", "needs approval", "outside your plan").
**Why it fails:** the user can't act on it and will invent an explanation — usually one that leads to a support ticket or a wrong workaround.
**Fix:** state the known condition and the route out of it. Reserve the generic wording for cases where the cause truly is unknown, and say so.

## Implementation vocabulary leak

**Detect:** engineering words in user-facing strings: stub, mock, dummy, null, payload, entity, record, enum, exception, config, sync, bare status codes.
**Why it fails:** it's unintelligible, it looks unfinished, and it often reveals that the feature *is* unfinished.
**Fix:** grep the string layer against a blocklist in CI; translate each hit into the user's word. If no user word exists, the concept probably shouldn't be exposed.

## Synonym drift

**Detect:** one concept, several words — "swap", "substitute" and "exchange" for the same action, sometimes on one screen. Found by grepping for the alternatives, not by reading.
**Why it fails:** every synonym reads as a distinct feature to someone still learning the product, which is everyone for longer than teams assume.
**Fix:** pick one word, record it in the terminology ledger with its banned synonyms, rename every instance in one change, and add the banned list to review.

## Tooltip-only meaning

**Detect:** a control whose purpose is carried by a `title` attribute or hover card — icon buttons, truncated labels, status dots explained on hover.
**Why it fails:** invisible on touch, unreachable by keyboard in many implementations, inconsistently announced by screen readers. Violates the accessibility floor.
**Fix:** visible text, or an accessible name plus a persistent visual cue. Tooltips carry secondary detail only.

## The dead-end empty state

**Detect:** an empty surface whose entire copy negates its content — "No lines in this section.", "Nothing here yet.", "No data."
**Why it fails:** it restates what the user can already see and offers no way forward, wasting the product's best teaching moment.
**Fix:** what belongs here + why it's useful + one action, placed in the empty state itself.

## One zero state for four situations

**Detect:** the same message for never-created, filtered-to-nothing, user-cleared, and failed-to-load.
**Why it fails:** it tells brand-new users their search found nothing and hides load failures behind a friendly empty illustration.
**Fix:** four messages; the load failure is an error state with retry, not an empty state.

## Double confirmation

**Detect:** one action, two messages — a component toast plus a page-level toast, or an optimistic message followed by a confirmed one.
**Why it fails:** it reads as two events; users check whether they submitted twice.
**Fix:** decide which layer owns feedback for the action and remove the other; cover shared handlers with a test asserting a single emission.

## Mixed label grammar

**Detect:** a set of options where forms don't match — an interrogative ("Which role?") among nouns ("Name", "Email", "Team"), or a verb phrase among noun labels.
**Why it fails:** the odd item forces re-parsing and implies it is a different kind of thing.
**Fix:** one grammatical form per group. Pick the form that suits the majority and rewrite the outlier.

## Copy as a patch over a design defect

**Detect:** a sentence explaining how to use the control directly beneath it; help text that grows every release.
**Why it fails:** it treats the symptom, adds weight to the screen, and is unread by exactly the users who needed it.
**Fix:** climb the ladder — rename, restructure, or default the control. Keep the sentence only if rungs 1–3 genuinely failed.

## Error message theatre

**Detect:** apologetic or jokey failure copy — "Oops! Something went wrong 🙈", mascot illustrations on data-loss screens, exclamation marks on payment failures.
**Why it fails:** it substitutes performed empathy for the two things the user needs (the cause and the next step), and it lands as contempt when something expensive just broke.
**Fix:** state the condition, the reason if known, and the action. Save the personality for low-stakes surfaces.

## Bare-code errors

**Detect:** the user-facing message is a code, an exception name, or an HTTP status.
**Why it fails:** it hands the system's internals to someone who can do nothing with them.
**Fix:** plain-language message first; a short reference ID afterwards for support.

## Yes/No dialogs

**Detect:** a question as the dialog title with `Yes`/`No` or `OK`/`Cancel` buttons.
**Why it fails:** the button alone is meaningless, so users must re-read the question — and misread it under time pressure, on exactly the actions where mistakes are irreversible.
**Fix:** the primary button repeats the verb ("Delete 3 files"); the escape option names what it protects ("Keep files").

## Placeholder as label

**Detect:** inputs whose only label is placeholder text, or whose format rule lives in the placeholder.
**Why it fails:** it vanishes at the moment of typing, defeats review of a filled form, and is unreliable for assistive tech.
**Fix:** persistent visible label; hints above the field; format shown by example.

## Format tantrums

**Detect:** validation messages about whitespace, letter case, dashes in card or phone numbers, pasted formatting.
**Why it fails:** the machine lectures the human about something the machine could fix in a line of code.
**Fix:** normalize on input; delete the message.

## Blame in the second person

**Detect:** "You entered an invalid…", "You forgot to…", "Your input is incorrect".
**Why it fails:** users who feel accused stop reading and start guessing.
**Fix:** state the condition and the rule: "That date is in the past. Choose today or later."

## Happy talk on task screens

**Detect:** welcomes, congratulations, and enthusiasm that would fit any product unchanged.
**Why it fails:** it costs attention before the useful words and dilutes what's scannable. (See [steve-krug](../../ux/steve-krug/anti-patterns.md).)
**Fix:** delete, or replace with the answer to "what can I do here?".

## Concatenated sentences

**Detect:** strings built by joining fragments, `"(s)"` plurals, `count === 1` branches producing grammar.
**Why it fails:** it encodes English grammar into control flow; every other language breaks, and the fragments get reused into nonsense even in English.
**Fix:** whole-sentence templates with named placeholders; plural-rule APIs.

## Truncation by design

**Detect:** labels in fixed-width containers, ellipsized buttons, layouts tested only against English strings.
**Why it fails:** translated copy commonly runs much longer; the cut usually removes the decisive word at the end.
**Fix:** flexible containers, +40% growth budget, pseudo-localized screenshots in review.
