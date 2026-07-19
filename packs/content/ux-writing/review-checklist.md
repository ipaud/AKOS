# Review Checklist — UX Writing Pack

Binary checks, ordered by severity. Used by [copy-reviewer](../../../agents/copy-reviewer.md). Each unchecked box is a finding at the listed severity. Checks marked ★ are safety-floor or truthfulness items and block in every reasoning profile.

Reviewing copy means reading the handler, not only the screen. Start with the truthfulness block; it is the only one that requires the diff.

## Critical (blocks in every profile)

- [ ] ★ Every action label names an effect the code actually produces. (UWE1, UWE6)
- [ ] ★ No success or confirmation message can fire for an operation that didn't succeed. (UWE2, UWE3)
- [ ] ★ No label claims a capability the feature doesn't have — AI, import, export, sync, automation. (UWE4)
- [ ] ★ No meaning is carried only by a tooltip, `title` attribute, or hover state. (UWE38)
- [ ] ★ Field errors are rendered in text, associated with their field, and not signalled by colour alone. (UWE21, UWE40)
- [ ] ★ Destructive confirmations name the object and scope, and state reversibility truthfully. (UWE14, UWE16)
- [ ] Every error message tells the user what to do next — no dead ends. (UWE18)
- [ ] Form failures preserve entered values. (UWE24)

## High

- [ ] One concept, one word: no synonyms for the same action or object anywhere in the product. (UWE7, UWE8)
- [ ] No developer or system vocabulary in user-facing strings. (UWE9)
- [ ] Status labels state the known specific reason rather than a generic unavailability. (UWE5)
- [ ] No raw codes, exception names, or HTTP statuses as the only user-facing message. (UWE19)
- [ ] Every empty state offers a path forward; none consists only of a negation. (UWE30, UWE31)
- [ ] First-run, no-results, cleared, and failed-to-load render distinct messages. (UWE32)
- [ ] One user action produces at most one confirmation message. (UWE34)
- [ ] Confirmation dialogs repeat the action verb; no Yes/No/OK on consequential actions. (UWE14)
- [ ] The dismissive option in a dialog cannot be misread as cancelling the user's work. (UWE15)
- [ ] Every input has a visible persistent label; no placeholder-only labels. (UWE25)
- [ ] Error copy contains no user-blaming construction. (UWE20)
- [ ] Transient messages carry nothing the user must retain or act on later. (UWE36)

## Medium

- [ ] Action labels are verb-first, name their object, and stay within ~3 words. (UWE13)
- [ ] Validation messages state the rule to satisfy, not just the failure. (UWE22)
- [ ] No error is shown for input the code could normalize itself. (UWE23)
- [ ] Labels within a group share one grammatical form. (UWE10)
- [ ] Capitalization convention is consistent product-wide. (UWE11)
- [ ] Hints render before typing, adjacent to their input; formats shown by example. (UWE26)
- [ ] Required/optional marked on the minority case, in words. (UWE27)
- [ ] Field labels use user vocabulary, not schema names. (UWE28)
- [ ] Operations over ~2s name what is happening; no bare spinners. (UWE33)
- [ ] Success messages name the resulting state and link to the result. (UWE35)
- [ ] Notification copy stands alone with no screen context. (UWE37)
- [ ] Link and button text is meaningful out of context. (UWE39)
- [ ] Reassurance sits at the commitment point, not on a linked page. (UW8)
- [ ] Tone matches the user's state — no humour or exclamation in failure or cost moments. (UW7)
- [ ] Bulk actions state the affected count. (UWE16)
- [ ] Disabled controls explain themselves without hover. (UWE17)

## Low

- [ ] No happy talk on task screens. (UW9)
- [ ] Copy does not explain a control that could be renamed or restructured instead. (UW9)
- [ ] Non-obvious fields carry a one-line reason. (UWE29)
- [ ] No internal code names, ticket references, or module names in the UI. (UWE12)

## Internationalization

- [ ] No sentence assembled from concatenated fragments; whole templates with named placeholders. (UWE41)
- [ ] Plurals use a plural-rule API; no "(s)", no `count === 1` grammar. (UWE42)
- [ ] Layout survives +40% string growth without truncation. (UWE43)
- [ ] Strings live in a resource layer with translator context notes. (UWE44)
- [ ] Dates, numbers, and currency formatted by locale APIs. (UWE45)

## Process

- [ ] A terminology ledger exists and this change was checked against it; new terms were added deliberately. (UWE7)
- [ ] Copy blocklist (developer vocabulary, banned synonyms) runs in CI or was grepped manually this review.
- [ ] Every new or changed string was read aloud in the user's worst plausible moment.
