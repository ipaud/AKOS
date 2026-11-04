# Heuristics — Game QA Pack

Defaults with known exceptions. Use while deciding; the
[engineering rules](engineering-rules.md) apply once the game exists.

- **Ask what the script actually pressed before believing PASS.** Read the script. A line
  that sets a score or jumps to chapter six is a line where the evidence stops.
- **Start with a whole-game run, then add unit tests where it is blind.** If a headless
  playthrough takes seconds, it finds more per minute than anything else you can write.
  The exception is a rule with exact values, where a focused test states the rule better.
- **Look at the frames.** Take a screenshot of every screen with text and actually open
  them. This single habit catches what every logic test misses.
- **Write down what a hash covers before trusting it.** If you cannot list what it covers,
  you do not know what it proves.
- **Run it twice before writing anything else.** Same build, same inputs, compare. A game
  that cannot repeat itself cannot be debugged from a report.
- **When a test fails once, stop and find out why.** In a deterministic run, "it passed the
  second time" is the most interesting result of the day.
- **Ask which states a losing path leaves the player in.** Softlocks live on the paths
  nobody plays on purpose: the retry, the failed attempt, the wrong order.
- **Prefer checking backwards from the goal when the space is small.** A puzzle, a tile
  map, or a room graph can often be enumerated. An exception is a game whose designer wants
  a softlock: then it is declared, and it is not a defect.
- **Treat a cheap level checker as a filter.** If it says no, believe it. If it says yes,
  still play the level on the real rules.
- **Give the bots different habits, including a bad player.** The careless profile finds
  the paths a good player never takes, and it is usually the one that gets stuck.
- **Fake the clock from the start of a project.** Retrofitting a clock seam is much harder
  than writing one, and without it a calendar game cannot be tested at all.
- **Put the boundary test on the day before, the day, and the day after.** Off-by-one dates
  are a single-line check and an embarrassing bug.
- **Corrupt your own save on purpose.** Truncate it, flip a byte, edit a number by hand and
  recompute its checksum. The last one is the test most games fail.
- **Keep one real save from every version you ship.** A fixture built by hand tests what you
  remember about the format; a file written by the old build tests the format.
- **Run the longest game you can imagine and weigh the save at the end.** Lists that only
  ever grow are invisible in a short run.
- **Keep HOST and BOARD in separate columns from the first day.** Merging them later means
  someone has to remember which was which.
- **Use the desktop for ratios, never for milliseconds.** It can tell you a change doubled
  the cost of a screen. It cannot tell you the screen fits the target.
- **Search story data for names, not for meaning.** Unused variables and orphan knots are
  grep-level findings; the writing is someone else's job.
- **Read a silent fallback as a defect until shown otherwise.** A portrait that falls back
  to neutral, a language that falls back to the source, a sound that "continues silent": the
  game looks fine and the content is gone.
- **Line-length and reading-time budgets have no source here.** If a project keeps one, it
  is the project's own choice and must say so.
- **On a small project, one person can run all of this.** If a check feels like it needs a
  team, cut it to what one script can do, or mark it for a human and leave it open.
