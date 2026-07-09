# Heuristics — Norman Pack

## Diagnosing failures

- **Classify by gulf first.** User couldn't start → execution gulf (fix signifiers/mapping). User acted then hesitated/repeated the action → evaluation gulf (fix feedback/state visibility).
- **Slip or mistake?** Ask: did they intend the right thing? Yes → slip → mechanical fix. No → mistake → communication fix.
- **Walk the seven stages** on any stubborn flow failure; mark the first stage where users stall — fix there, not downstream.
- **Read the support inbox as a model-diff.** Every repeated question names a screen whose system image lies.

## Designing interactions

- **New interaction? Steal the model.** Before inventing, find an existing conceptual model users already hold (cart, folder, timeline, feed) and bend it.
- **Signifier budget:** every primary action visible; secondary actions behind one conventional disclosure ("⋯"); accelerators (shortcuts, gestures) always duplicated by a visible path.
- **The two-second state test:** show a screen cold; can a user say what state the system is in (saved? syncing? offline? which account?) in two seconds?
- **Directional controls follow content, not device.** Scroll/swipe/drag should move the *content* the way the gesture moves — pick one convention and never mix.
- **If you write a validation error, first ask what constraint would have prevented it.** Date pickers over date-format errors; filtered lists over "not found".

## Error design

- **Undo > confirm.** Confirmation dialogs get auto-confirmed within days; undo works forever. Reserve confirmation for irreversible + rare.
- **Make dangerous different.** Destructive actions get distinct color, position, and extra distance from common actions — never adjacent to a frequent button.
- **Interlock the truly fatal.** For data-destroying operations, prefer forcing functions (type the project name) over checkboxes.
- **Every error message names the next step.** Same rule as Krug ER17 — plus: check whether the error reveals a broken conceptual model worth fixing upstream.

## Feedback calibration

- **<100ms acknowledge, <1s show progress, >10s allow leaving.** Long operations report progress honestly and survive navigation.
- **Match prominence to importance.** Toast for background success, inline for field errors, modal only for must-decide-now. A modal for a trivial notice trains modal-blindness.
- **Feedback states the *what*, not just the *that*:** "Saved to Drafts" beats a checkmark alone when the destination is ambiguous.

## Emotional levels

- **Review all three levels separately:** would you screenshot it (visceral)? does it feel instant and competent (behavioral)? would you tell someone about it (reflective)?
- **Personality lives at visceral/reflective; never spend behavioral budget on it.** Animation that delays input is identity at usability's expense — cut it.
