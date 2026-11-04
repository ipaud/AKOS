# References — Game QA Pack

Attribution only. Nothing here is copied from these sources; the pack is an original operational
distillation, organized by the AKOS file contract rather than by any source's structure.

## Primary source (Level 2)

- **Certified Tester Game Testing (CT-GaMe) Syllabus, Version 1.0.1** — International Software
  Testing Qualifications Board, 21 October 2022.
  https://www.istqb.org/wp-content/uploads/2024/11/ISTQB_CT_GaMe_Syllabus_v1.0.1_LtrKuyi.pdf

**Read:** all 89 pages, on 2026-11-04, extracted locally from the PDF at that URL. A search the
same day found no newer version; the URL has not moved.

## What Level 2 covers here, and what it does not

The level applies to **the defect classes and test objectives**: game state and shown against
used values, saves by type, graphics, sound, levels, controllers, localisation, and the weighing
of likelihood against impact.

It does **not** extend to automation, determinism, or replay. The earlier reading holds: the
syllabus is manual and 3D-leaning. Automation appears only as route scripts for performance and
compatibility, capture tools, and comparison of strings and screenshots between localisations.
"Determinism" and "replay" appear nowhere. Three more gaps worth knowing:

- It never says "softlock". Its nearest ground is core mechanics defects stopping completion,
  and characters stuck in level geometry. P2 and GMQ1 are AKOS synthesis on that ground.
- Its section 2.2.4 names an inactive user in its heading, and its body does not treat that case.
  Long-running time is not sourced from it.
- It assumes a studio with named roles. The pack keeps the defect classes and drops the roles.

## Secondary sources (Level 4: corroboration only, never rule bases)

"Fetched" below and in the next two sections means a fetch tool read the page and answered set
questions about it. It was not read line by line, unlike the syllabus and the sections marked
as read from extracted text.

- **Automated Testing for League of Legends** — Jim Merrill, Riot Games, 2016.
  https://www.riotgames.com/en/news/automated-testing-league-legends
  **Fetched.** `technology.riotgames.com/node/33` returned 504 again; the article's slug on
  the same host redirects to the URL above. It corroborates in-game automated tests, and waiting
  by polling a condition rather than sleeping. It does **not** corroborate replay or determinism:
  it describes neither. It also keeps a staging set for unstable tests, and one example allows a
  10% tolerance, both of which differ from GMQ6 and GMQ10 because that game is not run as a
  deterministic replay.
- **Automated Testing of Gameplay Features in Sea of Thieves** — Robert Masella, Rare, GDC 2019.
  https://gdcvault.com/play/1026366/Automated-Testing-of-Gameplay-Features
  **Abstract only.** The talk is behind a membership. It supports only that a shipped game was
  built with automated gameplay tests. Nothing else is claimed from it.
- **Gauntlet Automation Framework Overview** — Epic Games.
  https://dev.epicgames.com/documentation/en-us/unreal-engine/gauntlet-automation-framework-overview-in-unreal-engine
  **Fetched.** Level 1 for Unreal only. It runs game sessions across platforms and says nothing on
  determinism. No rule rests on it.

## Papers, as ideas inside the pack, never as its basis

- **Stuck in the Middle: Generating Levels without (or with) Softlocks** — Seth Cooper and Mahsa
  Bazzaz, FDG 2025. https://pcgworkshop.com/archive/cooper2025softlocks.pdf
  **Abstract and introduction read from extracted text; the rest searched.** The source of the forward and backward reachability idea
  in P10. Its scope is player movement in 2D tile levels, not items or powerups, so GMQ2 goes
  beyond it. It also notes that a designer may want softlocks.
- **Cooperative Multi-agent Approach for Automated Computer Game Testing** — Samira
  Shirzadeh-hajimahmood, I. S. W. B. Prasetya, Mehdi Dastani, Frank Dignum, 2024.
  https://arxiv.org/abs/2405.11347
  **Abstract fetched, extracted text searched.** Commissioned as softlock detection; it is not. The word
  "softlock" never occurs. It tests reachability of game objects with cooperating agents on one
  3D game. No rule rests on it.
- **Towards Automated Video Game Testing: Still a Long Way to Go** — Cristiano Politowski,
  Yann-Gaël Guéhéneuc, Fabio Petrillo, 2022. https://arxiv.org/abs/2202.12777
  **Abstract fetched, survey section read from extracted text.** 12 accepted responses, confirmed in the text. Context
  only: developers there were sceptical of automated agents.

**Not read and not used:** Mawhorter and Smith on softlock detection with temporal logic (FDG
2021) surfaced in a search snippet only.

## Narrative data sources (Level 4 and tool reference)

These sources do not earn a narrative pack, and they do not state GMQ40–GMQ44. Those rules are
**AKOS synthesis** on the syllabus's level and mechanics scope, checked against a real story file.

- **Standard Patterns in Choice-Based Games** — Sam Kabo Ashwell, 2015.
  https://www.ifwiki.org/Standard_Patterns_in_Choice-Based_Games
  **Fetched** (the IFWiki copy). Names structural patterns, and states no rule on reachability,
  orphans, or unused variables.
- **Small-Scale Structures in CYOA** — Emily Short, 2016.
  https://emshort.blog/2016/11/05/small-scale-structures-in-cyoa/
  **Fetched.** Same: named structures, no such rule.
- **Writing with ink** — inkle.
  https://github.com/inkle/ink/blob/master/Documentation/WritingWithInk.md
  **Fetched, whole page.** Tool owner for ink only, reference rather than doctrine. It shows that a
  compiler warning for a flow running out is a real practice. It does not say how a missing
  divert target is handled, or say anything of unused variables.

## Determinism: what practice actually shows

Determinism is AKOS methodology, because only Level 4 sources describe it and those that were
read do not describe replay at all. Its basis is three real projects: Pinyol, public, and two private
MicroPython games by the same maintainer.

- Replay and framebuffer comparison are verified in Pinyol: `--crc` on two runs, compared by `ctest`'s
  `record_replay`. That CRC covers pixels, not state.
- A state digest and a blessed baseline are verified in a private project, and state replay with
  seeded bot reports in another.
- **First-divergence reporting is unverified** anywhere (GMQ9). Peer desync detection is unverified
  and has no rule.

## Methods verified against practice

The evidence ladder with separate host and board records, campaign bots, long-running time on a
fake clock, and save fixtures per schema version were each read in those projects and, where marked
**measured**, run on copies outside them on 2026-11-04. Host runs say nothing about a board.

Findings about a project stay in that project: a pack states rules, never the state of a codebase.

## Could not verify

- Any real-hardware claim. Figures from the projects' own reports were read, not reproduced.
- The GDC talk beyond its abstract.
- That the projects' ticked checklist rows are true, beyond what is listed above.

## Related AKOS packs

[testing/qa-checklists](../../testing/qa-checklists/README.md) ·
[testing/testing-pyramid](../../testing/testing-pyramid/README.md) ·
[testing/tdd](../../testing/tdd/README.md) ·
[testing/playwright](../../testing/playwright/README.md) ·
[performance/core-web-vitals](../../performance/core-web-vitals/README.md)
