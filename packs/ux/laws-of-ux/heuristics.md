# Heuristics — Laws of UX Pack

Fast application rules per law.

## Choice & decision (Hick)

- Count options at each decision point of the main flow; >5 undifferentiated → group, default, or cut.
- Every choice screen gets one recommended/default option unless choices are genuinely equipotent.
- Settings pages: bury rarely-changed options; surface the 3 people actually change.
- If analytics show hesitation (long dwell before click) at a step → Hick audit first.

## Targets & layout (Fitts)

- The most frequent action per screen: biggest and nearest target; audit primary flows for tiny/far frequent buttons.
- Put confirm near the triggering context (dialog buttons near the content, not across the screen).
- Desktop: exploit edges/corners for persistent chrome; never put frequent targets at 1px-precision locations.
- Touch: 44px/8px minimums; row actions big enough for thumbs, destructive ones not where thumbs rest.

## Convention (Jakob)

- Before designing any standard object (nav, form, cart, player), name the convention you're following; if none, that's a decision to justify.
- Redesigns: migrate, don't teleport — announce, overlap, allow switching back temporarily.

## Memory (Miller)

- Any screen asking users to *retype or recall* something shown earlier fails — restate it.
- Chunk all displayed identifiers (cards, phones, keys) in 3–4 char groups.
- Wizard steps: repeat the critical context (what/for-whom) in the header of every step.

## Complexity placement (Tesler)

- For each form field ask: can the system know this? (locale, timezone, card type, name from email) → infer + allow correction.
- For each error message ask: could code have absorbed this? ([Krug format tantrums](../steve-krug/anti-patterns.md))
- For each instruction ask: could a default make it unnecessary?

## Peaks & endings (Peak-End)

- Map each key journey's likely peak and its end; both get explicit design attention.
- Ends: success screens celebrate + orient next step; never end on silence or a form.
- Error moments are candidate negative peaks — the best error-state ROI in the app.
- Waiting is a negative peak candidate: entertain, inform, or shorten perceived duration (skeletons, progress, useful tips).

## Position (Serial Position)

- First nav slot: primary user goal; last slot: exit/profile/help; middle: everything else.
- Marketing lists: differentiator first, CTA-adjacent benefit last.

## Distinctiveness (Von Restorff)

- One accent per screen; audit with the squint test.
- If a stakeholder asks to "make X pop" — first ask what loses its pop to pay for it.
- Never make routine and destructive actions equally prominent.

## Polish (Aesthetic-Usability)

- Schedule a polish pass before any usability test on a rough prototype — otherwise cosmetic noise dominates findings.
- Discount user praise of pretty interfaces; count task success and time instead.
- When users forgive a flaw "because it's nice" in testing, still log the flaw — tolerance decays with exposure.

## Progress (Goal-Gradient)

- Any flow ≥3 steps shows progress; any flow ≥6 steps shows sub-goals.
- Show "what's left" near the end ("1 step remaining") — the gradient's steepest section.
- Setup checklists: seed with an already-completed item (honest one — "account created ✓").
