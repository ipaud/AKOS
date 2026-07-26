# Heuristics — Philosophy of Software Design Pack

Defaults with known exceptions. Use while the design is open; the
[engineering rules](engineering-rules.md) apply once code exists.

- **Ask what the caller stops needing to know.** It is the fastest test for whether a
  boundary is real, and it works on interfaces, classes, services, and files alike.
- **When tempted to split, write the new unit's interface comment first.** If it's awkward
  to write, the boundary is wrong. Two minutes here saves the refactor.
- **Prefer one longer unit with a clear interface to three short ones sharing state.**
  Exception: a testing seam, or a piece with a genuinely different reason to change.
- **Count how many places a change touched, and treat a high number as a design report.**
  Change amplification is the most measurable of the three complexity symptoms — the diff
  tells you directly.
- **When two modules both know a format, one of them is wrong.** Usually the one that
  acquired the knowledge second, informally, because it was convenient.
- **Suspect any decomposition that follows the order operations happen in.** Read/process/
  write splits feel natural and leak by construction.
- **Before adding an error, try to make the condition impossible.** The cheapest exception
  handling is the exception that cannot occur.
- **Make idempotent things succeed quietly.** Deleting what is gone, closing what is
  closed, cancelling what stopped — raising on these pushes a branch onto every caller.
- **A boolean parameter usually wants a name.** At the call site, `true` means nothing;
  a named argument or two clearly-named operations both beat it.
- **If you need a comment to explain a name, change the name.** Unless the comment carries
  what a name cannot: units, ranges, ownership, invariants.
- **Write the comment you'd want to read in two years, not the one that proves you were
  here.** Intent and rejected alternatives age well; restatements of the code age badly and
  then lie.
- **Sketch a second design when the decision is expensive to reverse.** Schemas, public
  interfaces, module boundaries. Not for a helper function — the point is proportionality.
- **Spend a small fraction of every change on the design, rather than scheduling a
  cleanup.** The cleanup does not happen; the fraction compounds.
- **In Prototype profile, skip all of this.** Tactical is correct for code that is a
  question rather than an asset. Note the leakage in a comment and move on.
- **Never use "that's shallow" as a review verdict on its own.** Name what the caller would
  stop needing to know. If you can't, you have a preference.
