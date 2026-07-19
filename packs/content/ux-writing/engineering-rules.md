# Engineering Rules — UX Writing Pack

Checkable in the artifact. A reviewer verifies each against the code and the rendered UI; violations are findings.

## Truthfulness (label ↔ behaviour)

- UWE1. Every action label names an effect the handler actually produces. If the handler only writes a status field, the label describes a status change, not a delivery, transfer, or send.
- UWE2. Success messages are emitted from the success branch of the operation they describe — never before the call, never in a `finally`, never unconditionally after dispatch.
- UWE3. Where the outcome is asynchronous or queued, the message states the queued state ("Queued — you'll get a copy when it sends"), not the final state.
- UWE4. Capability claims in labels ("AI", "Import", "Export", "Sync", "Auto-") correspond to an implemented capability. A control that accepts no file is not an import; a deterministic parser is not AI.
- UWE5. Status labels state the known specific condition rather than a generic unavailability. If the system knows *why*, the label says why.
- UWE6. Feature names in the UI match what shipped. When scope is cut in implementation, the label is re-derived from the remaining behaviour before merge.

## Terminology and consistency

- UWE7. Each concept has exactly one user-facing term, recorded in a terminology list checked into the repo.
- UWE8. No two synonyms for one concept appear anywhere in the product's strings (grep the banned-synonym column; hits are findings).
- UWE9. No developer or system vocabulary appears in user-facing strings. Blocklist at minimum: stub, mock, dummy, null, undefined, NaN, payload, endpoint, entity, record (as a noun for a row), enum, boolean, exception, foreign key, DTO, config, sync (as a user-facing verb), 4xx/5xx bare codes.
- UWE10. Labels within one control group share a grammatical form — all nouns, all verb phrases, or all questions; never mixed.
- UWE11. Capitalization follows one documented convention (sentence case recommended) across every string.
- UWE12. UI copy does not use the product's internal code names, ticket numbers, or module names.

## Buttons and actions

- UWE13. Action buttons are verb-first and name their object; ≤ 3 words / ~25 characters unless the count is included.
- UWE14. A confirmation dialog's primary button repeats the action verb. No `Yes`/`No`/`OK` on a dialog that asks a question about a consequential action.
- UWE15. The dismissive option in a dialog names what it preserves ("Keep editing") whenever "Cancel" could be read as cancelling the underlying work.
- UWE16. Bulk actions state the affected count in the label or the confirmation.
- UWE17. Disabled controls expose the reason in text reachable without hover (inline note, adjacent hint, or an enabled control that explains).

## Errors and validation

- UWE18. Every error message contains what happened and what to do next; it also contains why when the cause is known.
- UWE19. No raw error codes, exception names, stack fragments, or HTTP statuses as the sole user-facing content. A reference ID may accompany plain language.
- UWE20. Error copy contains no user-blaming construction; failures are stated as conditions, not as user mistakes.
- UWE21. Field validation messages are rendered as text adjacent to the field and programmatically associated with it (`aria-describedby`, error id) — colour or border alone never carries the error.
- UWE22. Validation messages state the rule to satisfy, not only the fact of failure.
- UWE23. No error is shown for an input the code could normalize itself (surrounding whitespace, letter case, separators, pasted formatting).
- UWE24. Form submission failures preserve entered values and identify the first offending field.

## Forms

- UWE25. Every input has a visible, persistent label; placeholders carry neither the label nor format requirements.
- UWE26. Hint text renders before the user types and sits adjacent to its input.
- UWE27. Required/optional is marked on the minority case, in words, not by a symbol alone.
- UWE28. Field labels use user vocabulary, not schema column names.
- UWE29. Any field whose purpose is non-obvious carries a one-line reason next to it.

## Empty, zero, and loading states

- UWE30. Every empty state states what belongs there and offers one primary action (or an explicit statement that no action is needed, and why).
- UWE31. No empty state consists solely of a negation of its content ("No X.", "Nothing here.").
- UWE32. First-run empty, no-results-after-filter, user-cleared, and failed-to-load render distinct messages; failed-to-load offers retry.
- UWE33. Operations expected to exceed ~2s show text naming the operation, not a bare spinner; determinate operations show progress in user terms.

## Feedback, toasts, notifications

- UWE34. One user action produces at most one confirmation message; nested layers do not both emit (assert this in tests for shared handlers).
- UWE35. Success messages name the resulting state and link to the result where one exists.
- UWE36. Transient messages (toasts) carry no information the user must retain or act on later; actionable outcomes render in persistent surfaces.
- UWE37. Notification and push copy is self-sufficient with no surrounding screen — it names the object and the event without pronouns referring to on-screen context.

## Copy accessibility

- UWE38. No meaning exists only in a `title` attribute or hover tooltip; icon-only controls carry an accessible name matching their visible purpose. (Safety floor — see [wcag](../../ux/wcag/engineering-rules.md).)
- UWE39. Link and button text is meaningful out of context; no "click here" / "learn more" without an object.
- UWE40. Copy conveying status is not carried by colour alone; the word states the status.

## Internationalization

- UWE41. No user-facing sentence is assembled by concatenating fragments; sentences are whole templates with named placeholders.
- UWE42. Plurals use the platform's plural-rule API; no `count === 1` branching, no "(s)".
- UWE43. Layouts tolerate at least +40% string length without truncation or overlap; labels are not placed in fixed-width containers.
- UWE44. All user-facing strings live in a resource layer, not as literals in components, and carry a context note for translators where the term is ambiguous.
- UWE45. Dates, times, numbers, and currency are formatted through locale APIs; no hardcoded formats or separators in copy.
