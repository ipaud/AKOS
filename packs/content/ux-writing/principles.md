# Principles — UX Writing Pack

Durable rules of interface writing. Violating one requires an explicit tradeoff statement.

## UW1 — A label is a promise the code must keep

The words on a control describe what the system will actually do when it is used. A label that names an effect the handler doesn't produce is a defect of the same class as a wrong calculation — the user acts on it and is wrong about the world afterwards. Copy review therefore reads the handler, not just the string.

## UW2 — Never confirm what didn't happen

Success messaging is bound to the success branch of the operation it describes. A confirmation that fires optimistically, fires regardless of outcome, or describes a step further along than the code reached teaches users to distrust every message the product shows. When the outcome is genuinely asynchronous, the message says what is true now ("Queued for sending"), not what is hoped for.

## UW3 — Say the effect, not the mechanism

Users think in outcomes; systems are named in mechanisms. Interface words come from the user's side of that line: what changes in their world, in the vocabulary they already use for it. Internal names — table names, service names, status enums, engineering shorthand — never surface, however convenient they are to the team that built them.

## UW4 — One concept, one word

Each concept gets exactly one user-facing term and keeps it everywhere: buttons, headings, messages, docs, support replies. Synonyms are not variety; they are additional concepts in the user's model. Renaming is a product decision applied to all instances at once, never a per-screen preference.

## UW5 — Every message answers "what now"

Text that reports a state without offering a path is a dead end. Errors, empty states, blocked actions, and unavailable options all end with something the user can do — an action, a route, or an honest statement that there is nothing to do and why. Reporting is not the job; unblocking is.

## UW6 — Specific beats soothing

A vague, gentle message costs more than a precise, unwelcome one. "Something went wrong" and "Not available" leave the user to invent an explanation, usually a worse one than the truth. When the system knows the reason, the copy states it in user terms. Softness lives in tone, never in the omission of facts.

## UW7 — Blame the system, never the user

Interface copy never implies fault. Failures are described as states of the world rather than as things the user did wrong, and second-person accusations ("you entered an invalid…") are rewritten as observations plus the rule. This is not politeness theatre: users who feel blamed stop reading and start guessing.

## UW8 — Reassurance belongs at the point of commitment

The words that reduce anxiety must sit within the user's field of view at the moment they decide — beside the button, not on a linked page, not in a paragraph above the fold that scanning skipped. Each commitment point answers the questions it raises: what happens, is it reversible, who sees it, what does it cost, when does it end.

## UW9 — Cut first, write second

Text is the second-cheapest fix and the most easily overused. Before adding a sentence, try removing the need for it: rename the control, set a default, reorder the flow, split the step. A screen where every string is load-bearing reads faster than a screen where helpful text surrounds a confusing control.

## UW10 — Front-load, because copy is scanned under load

Interface text is read mid-task by someone with a goal. The decisive words go first — verb first on actions, subject first on messages, the answer before the explanation. Anything after the point where the user has enough to act is unread by default and should justify its existence.

## UW11 — Meaning must survive without a pointer

No word that a user needs may live only in a hover tooltip or a `title` attribute. Touch users never hover, keyboard users often can't reach it, and screen-reader users get inconsistent treatment. Tooltips carry secondary detail for people who go looking; they never carry the meaning of a control.

## UW12 — One action, one message

A single user action produces at most one confirmation. Duplicate feedback from stacked layers (component and page, optimistic and confirmed) reads as two separate events and makes users check whether they did the thing twice. Feedback volume is proportional to consequence: quiet for the routine, prominent for the irreversible.

## UW13 — Empty states teach; they don't announce

A surface with no data is the product's clearest teaching moment and its highest-leverage empty pixel. It says what belongs there, why it matters, and how to get the first one — and it distinguishes never-created from filtered-out from failed-to-load, because those need different responses.

## UW14 — Labels in a set share a grammar

Options presented together take one grammatical form: all nouns, or all verb phrases, or all questions. A mixed set forces the user to re-parse each item and quietly signals that the options aren't the same kind of thing. Consistency of form is part of consistency of meaning.

## UW15 — Copy has a source of truth

User-facing strings live in one owned layer — a resource file, a content module, a design-system token set — not scattered as literals through components. Anything without a single home drifts: the same concept gets reworded in three places, and no reviewer can check the terminology ledger against the product.

## UW16 — Write for the sentence, not the fragment

Every user-facing sentence is composed whole, with named placeholders, and is expected to be translated, grow in length, be read aloud, and appear away from its screen. Sentences assembled from concatenated pieces encode English grammar into the code and break in every other language — and often in English too, once the pieces are reused.
