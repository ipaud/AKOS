# Heuristics — Apple HIG Pack

## Choosing containers

- Parallel peer sections users switch between → tab bar (2–5 tabs; more → "collapse into fewer concepts", not a More tab if avoidable).
- Drill-down into detail → navigation stack with Back; title reflects location.
- Self-contained task interrupting context (compose, edit, pick) → sheet; must have explicit Done/Cancel resolution.
- One critical decision → alert (rare); contextual options → menu/action sheet.
- If a modal has tabs inside it, the design has gone wrong somewhere.

## Fast checks

- Rotate + resize: does the layout survive iPad split view and iPhone landscape?
- Crank Dynamic Type to the largest accessibility size: what truncates, overlaps, or vanishes?
- Toggle dark mode: is every color intentional (system/semantic colors adapt free; hardcoded hex doesn't)?
- Swipe from the left edge everywhere: does back always work and always mean back?
- Watch the home indicator area and notch/island: content within safe areas, gestures unblocked?
- Turn on VoiceOver, do the primary task: labels, traits, order sensible?

## Platform-idiom judgment

- Coming from web/Android habits: hamburger menus, floating action buttons, toasts, and back buttons in the top-left content area are foreign on iOS — use tab bars, prominent inline actions, and the navigation bar.
- Sheets replaced full-screen modals as the default temporary context; full-screen only for immersive tasks (media, camera).
- Pull-to-refresh for content feeds; not for static screens.
- Swipe actions on list rows for frequent operations; always with a visible alternative path.
- On Mac: if a feature has no menu-bar item and no shortcut, it's not finished.

## Cross-platform products

- Keep: brand color/type personality, information architecture, feature parity.
- Adapt per-OS: navigation grammar, control styles, iconography, haptics, share/permission flows.
- Litmus: an iOS user should never feel Android grammar (and vice versa); a brand user should never feel like it's a different product.
