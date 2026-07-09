# Review Checklist — Norman Pack

## Critical

- [ ] No invisible modes: any state that changes behavior has a persistent indicator. (NR25)
- [ ] Irreversible destructive operations use proportional forcing functions. (NR16)
- [ ] Unsaved work cannot be silently destroyed by navigation/close. (NR17)
- [ ] Every error state preserves data and offers a next step. (NR20, NR21)

## High

- [ ] Every primary action has a visible signifier; nothing important is gesture-only or shortcut-only. (NR1)
- [ ] Acknowledgment <100ms; >1s operations show progress; >10s cancelable. (NR9, NR10)
- [ ] System state (account, mode, sync, unsaved) visible without test actions. (NR11)
- [ ] Undo available for reversible mutations; destructive actions visually and spatially distinct. (NR18, NR19)
- [ ] Invalid input prevented by constraints where feasible, not just validated. (NR14)
- [ ] Controls adjacent to what they affect; directions consistent app-wide. (NR5, NR6)

## Medium

- [ ] One term per concept across all surfaces. (NR23)
- [ ] No implementation vocabulary in user-facing text. (NR24)
- [ ] Similar controls labeled, not positional. (NR8)
- [ ] Feedback prominence matches importance; no modal-for-trivia, no toast storms. (NR13)
- [ ] State changes announce result + location, not bare success. (NR12)
- [ ] Custom components use platform signifier vocabulary. (NR4)
- [ ] Conceptual model statable in one sentence, and screens don't contradict it.

## Low

- [ ] Drag surfaces show handles; drop targets highlight. (NR3)
- [ ] Ordered controls mirror effect order. (NR7)
- [ ] Recurring validation failures tracked as design bugs. (NR22)
- [ ] Visceral/behavioral/reflective each considered; personality not taxing interaction.

## Diagnostic pass (for observed failures)

- [ ] Each failure classified: execution gulf vs evaluation gulf.
- [ ] Each error classified: slip vs mistake — and the fix matches the class.
- [ ] Fix lever chosen in order: constraint → mapping → signifier → feedback → model.
