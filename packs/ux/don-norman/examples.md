# Examples — Norman Pack

Invented cases.

## Slip vs. mistake — same symptom, different fix

Symptom: users delete the wrong environment in a deploy tool.

- **Investigation A:** they meant staging, hit production — the two rows are adjacent, identical, one click. → **Slip.** Fix: separate production visually (color, badge), add distance, typed confirmation for production only. Relabeling wouldn't help.
- **Investigation B:** they believed "Remove" detaches the environment from the dashboard, not destroys it. → **Mistake.** Fix: rename to "Delete environment permanently", add model-consistent copy. A confirmation dialog would get confidently accepted.

## Gulf classification

- "I don't see how to invite someone" → execution gulf → signifier fix: visible **Invite** button instead of an item buried in a "⋯" menu.
- "I clicked Save but I'm not sure it worked" → evaluation gulf → feedback fix: button state change + "Saved just now" timestamp, not a 300ms toast users miss.

## Mapping

- Bad: keyboard-brightness controls in a settings page listed alphabetically ("Backlight level: dropdown").
- Good: a slider oriented so up = brighter, next to a live preview.
- Bad: table bulk-actions toolbar at top-right affecting rows selected far below.
- Good: action bar appears attached to the selection.

## Constraint over validation

- Bad: free-text "Start date (DD/MM/YYYY)" + error on parse failure.
- Good: date picker bounded to valid range (constraint), typing allowed but auto-formatted (constraint + forgiveness).
- Bad: "Username may not contain spaces" error after submit.
- Good: spaces silently converted to hyphens with inline preview of the final handle.

## Forcing function proportionality

| Action | Guard |
|--------|-------|
| Archive note | none — instant + Undo toast |
| Delete note | instant + Undo, trash retained 30 days |
| Delete project (10 collaborators) | type project name + shows what's lost |
| Rotate API key used in production | two-step: create replacement first, then confirm revoke |

## Conceptual model coherence

A sync app projects: "your folder exists on all devices; the cloud is invisible plumbing."
Violation found in review: error toast "Upload queue full." — plumbing leaked (NR24). Model-consistent copy: "Some files aren't on your other devices yet — waiting for space."

## Invisible mode caught in review

Admin console: support staff can "impersonate" a customer; the only indicator is a small avatar change. Finding (CRITICAL, NR25): persistent full-width banner "Viewing as customer@example.com — Exit" required. Mode errors here = staff mutating customer data unknowingly.
