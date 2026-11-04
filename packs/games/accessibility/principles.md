# Principles — Game Accessibility Pack

Durable rules for making a rendered game playable by more people, and safe for all of them.
This is the game-side operationalization of the safety floor in the
[constitution](../../../core/constitution.md). [ux/wcag](../../ux/wcag/README.md) stays
in force for page shells around a game, but its keyboard walk and accessibility tree mean
little inside a framebuffer, so this pack brings its own walks. The `GAX*` codes in
[engineering-rules.md](engineering-rules.md) derive from these.

Anything marked **AKOS position** is this pack's own synthesis, not a source's.

## Harm comes first

- **P1 — Seizure risk is taken out of the default game; it is not managed.** A seizure can
  arrive before anyone reaches a menu, and many people who have one never knew they could.
  So a warning screen and an option both come too late. Options are for comfort beneath the
  limit, never a way of staying above it.
- **P2 — The flash area limit is an angle, not a share of the screen.** The source limit is
  a solid angle at the eye, and the percentages quoted around it belong to the viewing
  distance they were written for. Broadcast's quarter of the screen assumes a television
  across a room. Applied to a panel held in the hand, it allows several times what the angle
  allows. *AKOS position:* compute from the panel's physical size and the closest plausible
  distance.
- **P3 — Flash evidence is frames, and only the frames that were played.** A flash can last
  one frame, so anything sampling less than every displayed frame can miss it. A tool that
  saw ten idle seconds says nothing about the boss fight. "No flashing found" means "none in
  this recording".

## Evidence has a location

- **P4 — Host evidence and device evidence are different things.** A simulator proves the
  logic and the pixels sent. It does not prove what a panel shows at arm's length, what a
  small speaker can reproduce, or how a real button feels with a hard press. Legibility on
  a panel has one source of evidence: a person looking at that panel. A review states which
  it has, and never upgrades one into the other.

## Who owns it, where it applies

- **P5 — Every requirement has an owner: engine or game.** A text scale setting is plumbing;
  a timed section is a design decision. A finding with no owner is not fixed, because each
  side assumes the other has it. The test: would every game need the same code? Then it is
  the engine's. Does it depend on what this game asks of the player? Then it is the game's.
- **P6 — Requirements are per surface.** A fixed device with few buttons, a desktop with a
  keyboard and pad, and a browser on a phone offer different things. Thresholds and walks
  are stated for the panel and input in use, never for one resolution assumed in advance.
  Shipping to a surface means meeting that surface's walks.
- **P7 — A missing feature is a recorded gap, not a softened rule.** If the engine cannot do
  it, the rule stays as written and the gap is stated with its owner. Softening rules to fit
  today's engine leaves nothing to close the gap against. An absent feature is also not
  automatically a floor violation; [decision-framework](decision-framework.md) says which
  are.

## Input

- **P8 — The primary task must be completable, and nobody gets trapped.** This is the floor's
  keyboard clause restated for games: with the default bindings of each shipped surface, a
  player can start, play, and leave. It is the question behind the control walk.
- **P9 — When buttons are few, the plain press path replaces remapping.** A device with
  three fixed buttons has no other device to move an action to, and gestures end up carrying
  the load. A long press and a chord ask for timing and dexterity a player may not have.
  *AKOS position:* every action needs a route of single presses, with gestures as shortcuts.
  This is the same idea the sources express as simpler schemes and alternatives to holds,
  applied to hardware they did not write for.
- **P10 — A press lost while the game is busy is an accessibility defect.** Everyone hates a
  dropped press. It costs most for the player whose press took real effort, who presses
  deliberately and briefly, or who cannot quickly tell whether it landed. Slow loading on a
  small device turns this from a rare bug into the normal state of a menu. *AKOS position*;
  the sources do not address it.

## Perception

- **P11 — Essential information travels on two channels.** What matters must not live only in
  colour, only in sound, or only in a vibration or LED. The floor part is narrow: a
  single-channel cue that stops a player finishing the primary task. Everything else is a
  normal finding.
- **P12 — On a restricted palette, luminance does the work.** A 4-tone ramp has nothing but
  luminance, and neighbouring tones often fall short. A 16-colour palette has pairs that
  differ in hue while matching in luminance, which is exactly where colour vision differences
  bite. The look is a real constraint and the rule still applies; the pairs that carry
  meaning get chosen first.
- **P13 — Text is measured on the glass, in millimetres.** The same pixel count is a different
  size on every panel. A font that looks fine scaled up on a monitor can be unreadable on
  the panel it ships to, so size rules convert through the panel's real density.
- **P14 — Accessibility outranks juice.** Shake, flashes, hit-stop and trembling letters
  are good, and they are optional or capped wherever they can harm or stop someone reading.
  Feel is the product in a game; it does not get to be the reason someone cannot play. The
  conflict is ruled here, in line with Ruling R1 in
  [conflict-resolution](../../../core/conflict-resolution.md).

## Time

- **P15 — Sort time pressure into three kinds before judging it.** A timer inside the
  challenge is design. A timer on reading or menus is a barrier with defined fixes. Time that
  keeps running while the player is away is a third kind the sources do not cover.
- **P16 — Absence is not a fault in the player.** *AKOS position, below the floor.* A pet or
  calendar game that runs on the wall clock asks for daily presence. Illness, a hospital stay,
  caring for someone, or plain life can make that impossible, and the player learns the cost
  afterwards. Neither source covers this: Xbox's time-limit guidance leaves core mechanics
  out, and Game Accessibility Guidelines addresses precise timing during play. So the
  position is this pack's, stated as such. Real time can be the charm of a game; irreversible
  loss from absence alone is what it opposes.

## Choice and honesty

- **P17 — Assists widen who finishes; they take nothing from anyone else.** A game may be
  hard, and that is a legitimate design. Whether to add difficulty options is a decision the
  designer records, with the cost of each answer visible. The pack treats most of this as
  Level 2 advice and does not moralize in either direction. Labels stay descriptive and
  never mock the player who uses them.
- **P18 — Settings arrive before the harm they prevent.** A sound setting found after a loud
  intro, or a subtitle option found after the speech, is late. The route to settings has to
  pass the same walks as the game.
- **P19 — Nobody here certifies a game as accessible.** The Xbox guidelines state they are not
  for validating compliance or legal requirements, and that caveat carries through this
  pack. A review reports which walks passed, on which surface, with what evidence, and what
  is known missing. "Accessible" is not a verdict it can give.

## Scope

This pack covers photosensitive safety, input, text, colour, sound, motion, real-time pressure,
difficulty, and settings inside rendered games. It does not cover page shells, launchers, or
web forms around a game ([ux/wcag](../../ux/wcag/README.md)), touch ergonomics in depth
([mobile/touch-ergonomics](../../mobile/touch-ergonomics/README.md)), Apple platform idiom
([ux/apple-hig](../../ux/apple-hig/README.md)), target-size reasoning
([ux/laws-of-ux](../../ux/laws-of-ux/README.md)), or test-harness craft, which belongs to the
game QA pack in `packs/games/qa`. Multiplayer voice and text chat (XAG 119 and 120) are noted
in [references.md](references.md) and left out: no target game has them.
