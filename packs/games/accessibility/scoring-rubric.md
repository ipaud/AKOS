# Scoring Rubric — Game Accessibility Pack

Feeds the accessibility dimension
([scoring/accessibility-score.md](../../../scoring/accessibility-score.md)) for rendered games, in place
of the WCAG rubric inside the game. Any page shell still scores under
[ux/wcag](../../ux/wcag/README.md), never twice.

A score here says what was checked on which surface. It is not a statement that a game is accessible
(P19).

## Deductions (from 100)

| Finding | Deduction |
|---------|-----------|
| Flash over the rate and area limit at default; red fails; pattern fails | −25 each (CRITICAL) |
| Risky flashing "handled" by a toggle or warning | −25 (CRITICAL) |
| Primary task not completable, or a trap, on a shipped surface | −25 (CRITICAL) |
| Essential text or icons under 3:1 | −25 (CRITICAL) |
| Single-channel cue blocks the primary task | −25 (CRITICAL) |
| Essential text or icons from 3:1 up to the target | −10 (HIGH) |
| No plain route to an action on the primary path | −10 (HIGH) |
| Required hold, mash, or chord with no alternative | −10 (HIGH) |
| Presses lost under load on the primary path | −10 (HIGH) |
| Doubled or spontaneous input; no acknowledgement | −10 (HIGH) |
| Wrong prompts after remap, or no remap where devices vary | −10 (HIGH) |
| Destructive action with only hold-to-confirm, or no cancel | −10 (HIGH) |
| Smallest text below 1.06 mm on the panel | −10 (HIGH) |
| Meaningful colour pairs fail grayscale or CVD review | −10 (HIGH) |
| Speech without subtitles, or important sound without an equivalent | −10 (HIGH) |
| Effects cannot be reduced to zero, or have no cap | −10 (HIGH) |
| Absence alone causes irreversible loss, unwarned | −10 (HIGH) |
| Settings unreachable before first harm, or not persisted | −10 (HIGH) |
| No flash inventory | −10 (HIGH) |
| Evidence unlabelled, or a DEVICE item claimed with no signature | −10 (HIGH) |
| Sequences over five seconds | −4 (MEDIUM) |
| No digital alternative for non-essential special input; touch rule gaps | −4 (MEDIUM) |
| No pause, weak menus, no 200 % scale with no recorded gap | −4 (MEDIUM) |
| UI timers that cannot be lifted; moving HUD or reading text | −4 (MEDIUM) |
| Missing mute or category control; cues inaudible on target | −4 (MEDIUM) |
| Absence cost untested or unbounded; punishing return | −4 (MEDIUM) |
| Objectives unreviewable; heavy progress loss | −4 (MEDIUM) |
| Text form, haptic or light toggles, camera options, unrecorded difficulty decision, no declaration | −1 each (LOW), cap −8 |

## Caps and floors

- Any open CRITICAL: score ≤ 59 (Blocked band), per
  [core/scoring-model.md](../../../core/scoring-model.md).
- **No flash evidence means INCOMPLETE.** Without GAX6 evidence on a route meeting GAX7, the dimension
  has no score and the verdict is INCOMPLETE. Reading code alone cannot show a pass, and a clean
  idle run is not evidence. If another CRITICAL is open the decision is still BLOCKED, with flash named
  as not verified.
- **One root cause, one deduction**, across every screen it touches. Below 40, compare severity counts
  across reviews, not the number.
- **No device evidence caps the score at 79.** The read, sound-off, and press-capture items need a person
  on real hardware (GAX41). Without them, they are reported `unverified`, the cap applies, and the summary
  says "host evidence only". A simulator screenshot may produce a failure, never a legibility pass.
- **`n/a` conditions.** Each only for what does not exist: a surface not shipped; speech rules if there
  is no speech; touch rules if there is no touch; haptics if there is no motor; time-away rules if the game
  does not run on the wall clock; difficulty options if none are wanted and the decision is recorded.
- **A missing engine feature is never `n/a`.** It is a recorded gap with an owner, and it costs what the
  table says unless the game covers it (P7).
- Floor rules are not waived by profile, including Prototype and Game Dev.
- Time-away rules are AKOS positions and may never produce a CRITICAL.

## Anchors

- **95** — all five walks pass on every shipped surface with device evidence, gaps declared, thresholds
  worked for each panel.
- **85** — floor solid, device walks signed, MEDIUM gaps scheduled.
- **79** — strong host evidence, device walks not yet signed.
- **70** — floor holds on the primary surface; remap, plain routes, or size gaps recorded.
- **≤ 59** — a seizure-risk failure, a player who cannot finish, or text they cannot read.
