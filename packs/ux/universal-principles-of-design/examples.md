# Examples — Universal Principles Pack

Invented cases.

## Gestalt lie → truth (UD1)

Settings page: "Email notifications" toggle sits 16px below the "Profile" section header and 16px above the "Notifications" header — equal spacing makes ownership ambiguous (it belongs to Notifications). Fix: 8px to its own header, 32px from the previous section. No new lines, boxes, or labels needed.

## 80/20 promotion (UD6)

Analytics: "duplicate project" used daily by 60% of users, lives in Project → ⋯ → More → Duplicate (4 interactions). "Transfer ownership" used twice a year, sits as a top-level button. Swap their billing: Duplicate onto the card's visible actions; Transfer into the ⋯ menu.

## Forgiveness inventory (UD9)

Notes app audit:
| Action | Current | Fix |
|--------|---------|-----|
| Delete note | confirm dialog, hard delete | Undo toast + 30-day trash (schema: `deleted_at` column) |
| Overwrite via sync conflict | silent last-write-wins | version history, restore |
| Bulk tag removal | instant | undo (operation log) |

## Flexibility pricing (UD10)

Request: "add a setting to choose where the sidebar goes". Price: 2 layouts × every future screen × docs × tests; serves ~3% (estimated). Decision: no setting; pick the better default. Recorded with tripwire: revisit if RTL localization lands (then it's not a preference, it's correctness).

## Open loop closed (UD12)

API product: each key has a monthly quota consumed invisibly → surprise 429s. Fix: usage meter on the keys page, 80% email, response headers with remaining quota — consequences now visible where users act.

## Chunked sequence (UD8)

12-field onboarding → three named phases: "About you" (4), "Your team" (4), "Preferences" (4, skippable), with per-phase progress. Same fields, different cognitive shape ([Goal-Gradient](../laws-of-ux/principles.md) bonus: named sub-goals).
