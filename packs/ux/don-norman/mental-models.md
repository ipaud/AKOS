# Mental Models — Norman Pack

The named vocabulary. Precision matters here — these terms get misused industry-wide.

## Affordance

A relationship between an object and an agent: what actions the object *actually permits* (a button affords pressing; a text field affords typing). Affordances exist whether or not anyone perceives them. Common misuse: calling the visual hint an "affordance" — that's a signifier.

## Signifier

Any perceivable cue that communicates an affordance: the raised look of a button, underlined link text, a drag handle's ridges, a "⌄" chevron. **Design controls signifiers, not affordances.** When reviewers say "this doesn't look clickable", the finding is: *affordance present, signifier missing.*

## Mapping

The spatial/logical relationship between controls and their effects. Natural mapping exploits physical analogy (slider up = value up; card order on screen = order in the playlist). Poor mapping forces memorization (which switch is which light?). Test: could a user predict the effect of a control they've never used?

## Feedback

Immediate, informative communication of what just happened. Must be: fast (<100ms acknowledgment), proportionate (subtle for minor, prominent for major), and informative (not just "something happened" but *what*). Absent feedback creates the gulf of evaluation; excessive feedback trains users to ignore all of it.

## Conceptual model

The user's internal story of how the thing works, built entirely from the system image. Good design projects a deliberately simplified model that yields correct predictions (files in folders; a shopping cart). The model needn't be true — it must be *useful and consistent*.

## System image

Everything the user can perceive of the product: UI, copy, docs, marketing, error messages. The only channel through which the designer's model reaches the user's model. Incoherent system image → wrong user model → "user errors".

## Constraints

Forces that limit possible actions, catching errors before they happen:
- **Physical** — the USB-C plug only fits one way; a disabled field can't be typed in.
- **Semantic** — meaning rules out actions (the rider goes on the horse's back).
- **Cultural** — conventions (red = stop/danger/destructive).
- **Logical** — one slot left, one piece left.
Forcing functions are hard constraints: interlocks (can't delete while syncing), lock-ins (confirm before leaving unsaved work), lockouts (stairwell door to basement).

## The two gulfs

- **Gulf of execution:** user knows the goal, can't see how to act. Bridged by signifiers, constraints, mapping, conventions.
- **Gulf of evaluation:** user acted, can't tell what happened. Bridged by feedback and visible state.
Every observed usability failure classifies into one gulf — the classification points at the fix.

## Seven stages of action

Goal → Plan → Specify → Perform ‖ Perceive → Interpret → Compare. The first three descend the execution side; the last three climb the evaluation side. Diagnostic use: walk a failing flow stage by stage and mark where users stall.

## Slips vs. mistakes

- **Slip:** right goal, wrong execution (typo, tapping the adjacent button, autopilot into the wrong menu). Cause: attention, not understanding. Fixes: spacing, confirmation on destructive, undo, distinct-looking dangerous actions.
- **Mistake:** wrong goal or wrong plan from a wrong model (user believes "archive" deletes; picks the wrong tool entirely). Cause: understanding. Fixes: better system image, clearer conceptual model, better labels.
Fixing a mistake with a confirmation dialog (a slip remedy) fails — the user confidently confirms the wrong action.

## Knowledge in the world vs. in the head

Users function with imprecise knowledge because information can live in the environment (labels, visible options, recognition) instead of memory (recall). Design principle: put the knowledge in the world. This underlies NN/g's "recognition rather than recall" ([nng pack](../nielsen-norman-group/mental-models.md)).

## Three levels of emotional processing

- **Visceral** — immediate aesthetic reaction (looks trustworthy/cheap).
- **Behavioral** — the feel of use (responsive, competent, frustrating).
- **Reflective** — the story after use (pride, identity, recommendation).
A product can win one level and lose another; review each separately.
