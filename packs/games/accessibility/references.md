# References — Game Accessibility Pack

Attribution only. Nothing here is copied from these sources; the pack is an original operational
distillation, organized by the AKOS file contract rather than by any source's structure. All access dates
are 2026-11-04.

## Primary sources (Level 1)

- **Xbox Accessibility Guidelines** — Microsoft, version 3.2 (June 8, 2023).
  https://learn.microsoft.com/en-us/gaming/accessibility/guidelines
- **Understanding SC 2.3.1: Three Flashes or Below Threshold** — W3C.
  https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold.html
- **Understanding SC 2.3.2: Three Flashes** — W3C.
  https://www.w3.org/WAI/WCAG22/Understanding/three-flashes.html
- **Web Content Accessibility Guidelines (WCAG) 2.2** — W3C. https://www.w3.org/TR/WCAG22/
- **Recommendation ITU-R BT.1702-3** — ITU, November 2023.
  https://www.itu.int/rec/R-REC-BT.1702/en

## Secondary sources (Level 2 by judgement)

- **Steam Deck and Steam Machine Compatibility Review** — Valve. Normative on Steam Deck only; used here
  for handheld text and input norms. https://partner.steamgames.com/doc/steamdeck/compat

- **Game Accessibility Guidelines** — gameaccessibilityguidelines.com, undated, no named editor.
  Used for one-handed, cognitive, and assist gaps. https://gameaccessibilityguidelines.com/full-list/

## What was actually read

- **XAG index and version history:** read; history read for its recent versions only.
- **XAG 101, 102, 103, 104, 105, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 120, 121,
  122, 123:** implementation sections read in full from the fetched pages; expandable examples only in part.
  XAG 123's closing portrayal list was read in part.
- **XAG 106 and 119:** implementation sections read in part. Screen narration is a recorded gap and chat is
  out of scope, so no rule depends on the unread parts.
- **WCAG 2.2:** the "general flash and red flash thresholds" and "relative luminance" glossary entries.
- **Understanding 2.3.1:** intent, thresholds, screen-size and distance notes, and techniques list.
  **Understanding 2.3.2:** read through a summarizing fetch, not line by line.
- **BT.1702-3:** the full PDF, including Annexes 1 to 5.
- **Steam Deck review:** the Input and Display sections.
- **Game Accessibility Guidelines:** the full list, and one detail page, on precise timing.

**Not read:** individual WCAG techniques G15, G19, and G176, ISO 9241-391, the PEAT and Harding tools, and the
Machado, Oliveira and Fernandes paper (named only because Pinyol's filter cites it). The check in the
decision framework has not been compared with a certified analyzer.

## What Level 1 covers here, and what it does not

The level applies to **thresholds and criteria these bodies publish**: WCAG's flash definitions, BT.1702-3's
broadcast guidance, and Microsoft's documented criteria. Two limits matter:

- **Domain transfer.** WCAG is written for web content and BT.1702 for television. Using them on game frames
  is an application by analogy, and [authority-model](../../../core/authority-model.md) makes platform
  guidelines Level 1 on their own platform: XAG is not binding on a Pinyol or MicroPython handheld. They are the strongest game-specific sources available, used as such.
- **Not compliance.** The XAGs state they are not intended to validate compliance or legal requirements. Nothing
  here says otherwise.

Most XAG items are "should", and several suit large teams more than a solo developer. Level 1 authority does
not make them floor here; the floor is the eight starred rules, chosen in the
[decision framework](decision-framework.md).

## AKOS's own positions

Marked where they appear, and not attributable to any source:

- The handheld flash limit: `0.006 × d²` at `d` = 20 cm, and counting area across the whole frame.
- Millimetre conversions of Valve's pixel figures (assuming a 7-inch panel, which the page does not state)
  and reading "character height" as the smallest letter height.
- Plain press routes as the replacement for remapping on few buttons (GAX10).
- Lost presses as an accessibility defect (GAX12, GAX13).
- All absence positions (GAX34 to GAX36). XAG 116 excludes core mechanics, and XAG 108 addresses pausing and
  saving. Game Accessibility Guidelines addresses precise timing during play. Neither addresses a game
  that runs while the player is away.
- The HOST and DEVICE evidence split (GAX41), adopted from the maintainer's own release practice.
- The choice of floor rules, and the screen narration ruling.

## Disagreements between sources

- **Flash area:** 25 % of the screen (BT.1702-3), about 20 % (XAG 118), 0.006 sr (WCAG). See the framework.
- **Red:** XAG 118 uses the older (R−G−B)×320 form; WCAG 2.2 adds a chromaticity form. GAX3 fails on either.
- **Patterns:** about 20 % and 10 % contrast (XAG 118); 40 % and 25 % with over five pairs (BT.1702-3,
  informative). GAX4 takes the stricter area.
- **Text size:** Xbox's mobile figure measures body height; Valve's minimum measures a character. They are
  not the same measure, so both are kept.

## Target evidence (read-only, not sources)

Pinyol, which is public: `docs/lua.md`, `docs/roadmap.md`, `docs/hardware.md`, `docs/fonts.md`, `src/flashcheck.c`,
`src/conf.c`, `src/conf.h`, `src/sysmenu.c`, `src/game.c`, `platform/null/main.c`, `platform/sdl/main.c`,
`tools/library.py`, `lib/juice.lua`. Two private MicroPython games by the same maintainer were read as
well. Findings about any project stay in that project.

## Related AKOS packs

[ux/wcag](../../ux/wcag/README.md) · [ux/apple-hig](../../ux/apple-hig/README.md) ·
[mobile/touch-ergonomics](../../mobile/touch-ergonomics/README.md) ·
[ux/laws-of-ux](../../ux/laws-of-ux/README.md)
