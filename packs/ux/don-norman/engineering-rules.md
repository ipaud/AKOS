# Engineering Rules — Norman Pack

Checkable rules. Overlapping rules with [Krug ER-series](../steve-krug/engineering-rules.md) are cross-referenced, not duplicated.

## Signifiers

- NR1. Every primary and secondary action has a visible, perceivable signifier (text, icon+label, or platform-standard control). Gesture-only or shortcut-only access to any function is forbidden unless a visible equivalent exists.
- NR2. Interactive and non-interactive elements are visually distinguishable without interaction (see Krug ER6–ER10).
- NR3. Drag-and-drop surfaces show drag handles or an equivalent cue; drop targets highlight during drag.
- NR4. Custom components mimic the signifier vocabulary of their platform (a thing that behaves like a select looks like a select).

## Mapping

- NR5. Controls that affect on-screen objects are positioned adjacent to or aligned with their objects (row actions in the row; pane settings on the pane).
- NR6. Directional controls match content movement consistently app-wide (one scroll/swipe convention, never mixed).
- NR7. Ordered controls mirror the order of their effects (steps left→right/top→bottom in LTR; volume/brightness sliders increase upward or rightward).
- NR8. When >2 similar controls exist (e.g. per-channel toggles), each is labeled — no positional memorization required.

## Feedback & state

- NR9. Every user action produces perceivable acknowledgment within 100ms.
- NR10. Operations >1s show determinate progress where knowable, honest indeterminate otherwise; >10s operations are cancelable and survive navigation.
- NR11. Current system state (signed-in account, active workspace, sync/offline status, unsaved changes) is visible or one glance away — never requires a test action to discover.
- NR12. State changes announce their *result and location* ("Saved to Drafts"), not just success.
- NR13. Feedback prominence matches importance: inline < toast < banner < modal; modals reserved for decisions that must block.

## Constraints & forcing functions

- NR14. Invalid inputs are prevented where feasible (pickers, filtered options, disabled-until-valid submit with visible reason) rather than validated after.
- NR15. Impossible actions in the current state are disabled or hidden — and disabled controls communicate why (Krug ER9).
- NR16. Irreversible destructive operations use a forcing function proportional to loss: bulk/permanent deletes require typed confirmation or a two-step commit.
- NR17. Unsaved-work destruction (navigation, close, refresh) is intercepted with save/discard choice.

## Error design

- NR18. Undo is available for every reversible mutating action, discoverable at the moment of action (toast with Undo, edit menu, ⌘Z).
- NR19. Destructive actions are visually distinct AND spatially separated (≥ one control-width) from frequent actions.
- NR20. Error messages: cause in user language + next step + no blame ("couldn't save — you're offline; changes kept locally" not "save failed").
- NR21. After any error, the user's data and place in the flow are preserved (Krug ER21).
- NR22. Recurring identical validation failures (analytics or support signal) are treated as design bugs — tracked with the same severity as code bugs.

## Conceptual model coherence

- NR23. One term per concept across UI, docs, and errors (not "workspace" here, "team" there, "org" in billing).
- NR24. Features never expose implementation details the model doesn't include (no cache/queue/shard vocabulary in user-facing surfaces).
- NR25. Mode changes (edit vs view, admin vs member, sandbox vs production) are globally visible while active; modes that look identical but behave differently are forbidden.
