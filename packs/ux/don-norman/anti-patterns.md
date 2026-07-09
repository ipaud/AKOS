# Anti-Patterns — Norman Pack

## Signifier-free minimalism

**Detect:** clean screens where actions exist but nothing indicates them (swipe-to-reveal without hint, invisible tap zones, borderless inputs indistinguishable from text).
**Why:** aesthetic won over discoverability; the affordance exists, the conversation doesn't.
**Fix:** restore minimum signifiers; hide only accelerators.

## Norman doors (digital)

**Detect:** elements whose signifier contradicts their behavior — links styled as buttons that navigate, cards that look clickable but aren't, a back arrow that abandons a form without warning.
**Fix:** align signifier with actual behavior; behavior wins if the signifier is conventional.

## Arbitrary mapping walls

**Detect:** rows of identical unlabeled toggles/icons; settings whose grouping mirrors the org chart or database schema, not user tasks.
**Fix:** label everything, group by user goal, natural-map where spatial analogy exists.

## Feedback deserts

**Detect:** button clicked → nothing for seconds; save with no acknowledgment; background sync with no state anywhere.
**Fix:** NR9–NR12. Users re-click, double-submit, and distrust — all downstream defects of silence.

## Feedback storms

**Detect:** toast for every trivial event, confirmation emails for reads, badges everywhere.
**Why:** each notice devalues the rest; users learn to dismiss unread.
**Fix:** calibrate to cost-of-missing; delete notices that don't change behavior.

## Confirmation wallpaper

**Detect:** "Are you sure?" on frequent, reversible actions.
**Why:** trains automatic Yes; the one dialog that matters gets the same reflex.
**Fix:** undo for reversible; save dialogs for irreversible-rare.

## Blame-the-user error copy

**Detect:** "Invalid input", "You entered an incorrect value", ALL-CAPS warnings, error codes without translation.
**Fix:** NR20 — cause, next step, no blame. And ask which constraint was missing.

## Leaky abstraction UI

**Detect:** user-facing surfaces speaking implementation ("flush cache to see changes", "re-index required", HTTP codes as messages).
**Fix:** either absorb the concept into the model or hide it (NR24).

## Vocabulary drift

**Detect:** same concept named differently across screens ("project" / "workspace" / "site").
**Why:** each synonym forks the user's model.
**Fix:** one term per concept, enforced in a product glossary (NR23).

## Invisible modes

**Detect:** app behaves differently with no persistent indicator (editing live vs draft, acting-as-admin, recording).
**Why:** classic mode-error factory — the costliest mistake class.
**Fix:** NR25 — global visible indicator or merge the modes.

## Tutorial as load-bearing wall

**Detect:** onboarding tour teaching things the UI should signify; feature unusable if the tour was skipped.
**Fix:** signifiers and knowledge-in-the-world; tours may celebrate, never carry.

## Attractive-but-hostile

**Detect:** high visceral polish over broken behavioral layer — animation delaying input, aesthetic layouts hiding state, brand fonts destroying scanability.
**Fix:** behavioral level first (P11); personality re-added where it doesn't tax interaction.
