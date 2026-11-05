# Changelog — accessibility

## [1.2.0] — 2026-11-05

### Calibrated against a third real audit

Third audit, on a wall-clock pet. GAX17 exempts a game that cannot stop time. GAX34 names a shortened life and GAX35 refuses a floor that still fails a later evaluation. GAX53 judges an effect by its own clock and takes a position on LEDs. GAX24 limits the tenfold rule to short limits. GAX10 says what `alike` means.

## [1.1.0] — 2026-11-05

### Calibrated against a second real audit

GAX2 measures changed pixels, adds effects in phase, and says so of stacked sprites. GAX6 requires a candidate to be inspected against mean brightness and scripts to press at a human pace. GAX10 defines plain input for action games. GAX24 lists countdowns that only decide for an idle player. The rubric's GAX7 row now matches the checklist, and GAX41 has a row.

## [1.0.0] — 2026-11-04

### Added

- First complete version, status draft. Authority level 1 (Xbox Accessibility Guidelines 3.2, WCAG 2.2,
  ITU-R BT.1702-3), review cadence 545 days (`review_after: 2028-05-02`), with Game Accessibility Guidelines
  and Valve's Steam Deck review as Level 2 by judgement.
- Principles P1–P19 and engineering rules GAX1–GAX55: 41 universal rules, plus labelled mappings for Pinyol
  (GAX42–GAX48) and the three-button FNK0104B (GAX49–GAX55). Eight rules are starred.

### The pack's organising decision: what it refuses to contain

**Any verdict that a game "is accessible", and any pass without evidence from where it counts.** The Xbox
guidelines disclaim compliance use, so a review reports walks, surfaces, evidence, and gaps. Flash results
need played frames. A simulator cannot pass legibility. Rules are not softened to fit an engine: a missing
feature is a recorded gap. This is enforced in the principles (P3, P4, P7, P19), the reviewer discipline,
the rubric's INCOMPLETE and cap of 79, and two anti-patterns.

### Other notable choices

- **The flash area limit is an angle.** Sources give 25 %, about 20 %, and 0.006 sr. The percentages suit their
  viewing context. The pack derives a limit from physical panel size at 20 cm, labelled AKOS's own. A whole
  handheld fills less of the visual field than a monitor, so the common phrasing is not quite right; the
  risk comes from a screen-share limit allowing several times the angle on a close panel.
- **Owner and surface on every finding.** Rules are tagged engine, game, or both, and thresholds are relative to
  the screen in use, never one assumed resolution.
- **Five walks replace WCAG's keyboard walk:** control, read, sound-off, colour, flash.
- **Few buttons.** A device with three buttons gets plain press routes in place of remapping. A costless software
  swap of equivalent buttons is still asked for. Lost presses under load are an accessibility defect.
- **Absence from a wall-clock game** is a third kind of timing, covered by neither XAG nor GAG, ruled as an AKOS
  position below the floor (GAX34 to GAX36).
- **Screen narration is a declared gap, not floor,** because a framebuffer has no way to meet the
  constitution's screen-reader clause. Flagged for the maintainer.
- **Juice loses to accessibility**, with no invented shake number: the rule requires a named cap and a zero
  setting, since no source gives a figure.

### Calibrated against one real audit

GAX4 separates moving from static patterns and states what does not count as regular. GAX20 defines
what the task needs and splits CRITICAL from HIGH at 3:1. GAX10 allows one recorded project exception
on few-button devices. GAX27 separates ambient speech. The rubric deducts once per root cause.

### Scope boundary

Recorded against `packs/ux/wcag` (page shells), `packs/mobile/touch-ergonomics` (touch in depth),
`packs/ux/apple-hig` (Apple idiom), `packs/ux/laws-of-ux` (target-size reasoning), and the game QA pack in
`packs/games/qa` (test craft, saves).
