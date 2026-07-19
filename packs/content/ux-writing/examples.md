# Examples — UX Writing Pack

Invented cases. Bad → good, with the rule applied. All scenarios are fabricated for calibration.

## Labels that don't match the code (UWE1, UWE4)

A booking tool's crew-scheduling screen:

| Shipped | What the handler did | Honest version |
|---------|---------------------|-----------------|
| `Send` | set `status = 'sent'` on the shift row | `Mark as sent` — or implement the notification |
| `Import PDF (AI)` | opened a manual entry form | `Add entries manually` |
| `Sync calendar` | read once, on click | `Refresh from calendar` |
| `Auto-assign` | assigned by list order | `Assign in list order` |

The review move: for each button, write the sentence "after pressing this, the user could verify that ___". If the sentence can't be finished from the handler, the label is a finding.

## Phantom confirmation (UWE2)

Before — the toast fires whether or not anything was delivered:

```
markAsSent(shift);
toast.success("Roster sent to the crew");
```

After — the message describes what is actually true:

```
markAsSent(shift);
toast.success("Shift marked as sent");
```

And when delivery is genuinely asynchronous: `Sending — we'll tell you when the crew has it.`

## Synonym drift (UWE8)

One screen in a staffing tool used all three: **swap** (button), **substitute** (column header), **exchange** (confirmation dialog) — for one action.

Ledger entry that fixes it:

| Concept | Approved term | Banned synonyms |
|---------|---------------|-----------------|
| Replacing an assigned person with another | **replace** | swap, substitute, exchange, switch out |

Then: `Replace person` (button) · `Replaced by` (column) · `Replace Ana with Marc on this shift?` (dialog). One change, every instance.

## Euphemistic status (UWE5)

| Bad | Good |
|-----|------|
| `Not available` | `Already booked 12–15 Mar` |
| `Not available` (no licence) | `Needs a forklift licence` |
| `Not available` (unknown reason) | `Availability unknown — ask to confirm` |

Same two words hid three different situations, each with a different next step.

## Developer vocabulary (UWE9)

| Bad | Good |
|-----|------|
| `Stub created` | `Draft shift created` |
| `Entity saved (null owner)` | `Shift saved — no one assigned yet` |
| `Sync failed: 409` | `Someone else changed this shift. Reload to see their version.` (ref `SY-409`) |

## Tooltip-only meaning (UWE38)

Before: a row of status dots; the meaning of each colour lived in a `title` attribute. On a phone, the screen was unreadable.
After: dot plus a text label (`Confirmed`, `Pending`, `Declined`) beside it. The dot became redundant reinforcement, which is what colour should be.

## Empty states (UWE30–UWE32)

Before, for all four situations: `No lines in this section.`

After:

- **First run:** `No shifts scheduled yet. Add the first one and the week fills in automatically.` + `Add shift`
- **Filtered to nothing:** `No shifts match "night" in March.` + `Clear filters`
- **User cleared:** `Section emptied. You can undo this for 10 seconds.` + `Undo`
- **Failed to load:** `Couldn't load this section. Check your connection.` + `Try again`

## Error anatomy (UWE18, UWE22)

| Bad | Good | Structure |
|-----|------|-----------|
| `Error 422` | `That shift overlaps one Ana already has on 14 Mar. Pick another time or another person.` | what → why → next |
| `Invalid date` | `Start date is after the end date. Move the start to 12 Mar or earlier.` | what → why → next |
| `Password too short` | `Use at least 8 characters.` | the rule, not the violation |
| `You entered an invalid email` | `That email is missing an @. Check for typos.` | no blame |

## Format tantrums (UWE23)

Bad: `Phone numbers can't contain spaces or +.`
Good: no message at all — strip the spaces, keep the `+`, store normalized. If the number is genuinely unusable: `That number is too short for Spain (+34). Expected 9 digits.`

## Confirmation and destructive copy (UWE14–UWE16)

Before:

> **Are you sure?**  ·  `Cancel`  `OK`

After:

> **Delete "March roster" and its 14 shifts?**
> This can't be undone. Exported copies aren't affected.
> `Delete roster`  ·  `Keep roster`

Note the escape option: "Cancel" in a dialog about cancelling a booking is genuinely ambiguous, which is why it names what it preserves.

Where a trash exists, the truth changes and so does the copy: `Moves to Trash for 30 days.` — never claim irreversibility you don't have.

## Double toast (UWE34)

Before: the row component toasted `Shift updated` and the page container toasted `Changes saved` — one edit, two messages, users checking whether they'd saved twice.
After: the page owns feedback; the row emits nothing. A test asserts one toast per save.

## Mixed label grammar (UWE10)

Before: `Name` · `Email` · `Which role?` · `Start date`
After: `Name` · `Email` · `Role` · `Start date`

If a question genuinely helps, make the whole set questions — but on a form, nouns win.

## Anxiety at the commitment point (UW8)

Before, next to `Publish roster`: nothing. The reassurance lived in a help centre article.
After, directly beneath the button:

> Everyone assigned gets an email. You can edit shifts afterwards; they'll get a second notice.

Three facts, at the moment of hesitation: who sees it, is it final, what happens if I change it.

## Cutting entirely (UW9)

Before (31 words above an empty table):

> Welcome to your scheduling dashboard! To get started with creating your very first shift, simply click on the "Add shift" button located in the top right corner of this page.

After (0 words of instruction): make `Add shift` the visually dominant control inside the empty state, labelled `Add your first shift`. The sentence existed to explain a button the user couldn't find; moving the button fixed it.

## Writing for translation (UWE41–UWE43)

Before:

```
t("shift") + " " + count + " " + (count === 1 ? "person" : "people") + " assigned"
```

After:

```
t("shift.assigned", { count })
// en: "{count, plural, one {# person} other {# people}} assigned"
```

And in review: pseudo-localize (`Sh̃ìf̃t̃ às̃s̃ìg̃ñèd̃ ~~~~~`) before signing off on any screen with fixed-width labels.

## Success messaging (UWE35)

| Bad | Good |
|-----|------|
| `Success!` | `Roster published. 14 people notified.` + link to the roster |
| `Done` | `Invoice sent to maria@example.com` |
| `Saved` (on a visibly updated screen) | nothing — the screen already shows it |
