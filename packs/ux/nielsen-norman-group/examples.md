# Examples — NN/g Pack

Invented cases, organized by heuristic.

## H1 — Status

- Bad: clicking "Generate report" does nothing visible; the report appears in email 4 minutes later.
- Good: button → "Generating… (~2 min)" inline + a Reports page listing runs with statuses; completion toast links there.

## H2 — Real-world match

- Bad: "Provision a new tenant instance."
- Good: "Create a workspace."
- Bad: expiry input demanding `MM/YY` and erroring on `07/2029`.
- Good: accepts `7/29`, `07/2029`, `July 2029`; normalizes silently.

## H3 — Control & freedom

- Bad: newsletter modal with hidden close; unsubscribe requiring login to a deleted account.
- Good: X + Escape + backdrop close; one-click unsubscribe from the email itself.
- Bad: 6-step import wizard where Back clears everything.
- Good: Back preserves; "Save & finish later" at every step.

## H4 — Consistency

- Bad: "Remove" in projects, "Delete" in files, "Archive" in chats — all permanent deletion.
- Good: one verb ("Delete") + one behavior (trash, 30 days) everywhere.

## H5 — Prevention

- Bad: timezone as free text, erroring on "PST".
- Good: searchable select seeded with the browser timezone.
- Bad: "Delete" as the right-side default-focused button in a dialog where Enter confirms.
- Good: Cancel focused; Delete requires explicit pointer/space; spacing between them.

## H6 — Recognition

- Bad: "Are you sure you want to proceed?" (with what?)
- Good: "Delete 14 photos from 'Lisbon 2025'? They'll stay in Trash for 30 days."
- Bad: plan-comparison table on one page, upgrade action three pages away, from memory.
- Good: compare and upgrade on the same surface.

## H7 — Efficiency

- Bad: archiving 200 emails one confirmation each.
- Good: select-all-matching + one bulk archive + one undo.
- Good layering: novice uses the visible Filter button; expert presses `f`; both exist (expert cliff avoided).

## H8 — Minimalism

- Bad: invoice-creation screen with an upsell banner, a satisfaction survey, and a "what's new" feed.
- Good: the invoice form. Marketing lives elsewhere.

## H9 — Error recovery

- Bad: `Error: 0x80070057`.
- Good: "Couldn't upload video.mp4 — files over 2 GB aren't supported. Compress it or upgrade your plan." (+ persists until dismissed, file list intact)

## H10 — Help

- Bad: empty dashboard = blank grid.
- Good: "No data yet. Connect a source to see traffic — takes ~3 minutes. [Connect source]"
- Bad: docs page "The Permissions Matrix v2".
- Good: docs page "Give a teammate read-only access", linked from the sharing dialog.

## Severity rating worked example

Finding: date field errors on locale format (H5). Frequency: high (every non-US user). Impact: medium (recoverable, retry works). Persistence: every time. → HIGH. Same defect on an admin-only screen used monthly: → MEDIUM.
