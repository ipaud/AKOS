# Heuristics — Coding Agents Pack

Fast defaults with known exceptions. Try these first; deviate with a reason.

## Orientation

- **Find the project's own commands before writing your own.** The manifest, the Makefile, and the CI config say how this repository builds and tests. A hand-rolled equivalent will differ in flags and give a different answer.
- **Read the repository's contributor and agent-instruction files first.** They are short, they are authoritative, and skipping them is how a change arrives in the wrong style with the wrong test framework.
- **Look at three neighbours before adding a fourth.** The nearest three files in the target directory tell you naming, imports, error handling, and test placement faster than any documentation.
- **Check the working tree is clean before you start.** Editing on top of someone else's uncommitted work produces a diff nobody can untangle later.
- **Match the installed version, not the current one.** Conventions and APIs come from what is in the lockfile, not from what the library's front page documents today.
- **Finish orienting before you start editing.** If the structure turns out different from the plan, restate the plan rather than absorbing the surprise silently.

## Search

- **Enumerate before you edit.** The number of call sites is the scope of the change; not knowing it means not knowing the scope.
- **A surprisingly small result set is a suspect search, not a small problem.** One hit on a widely-used symbol usually means the pattern was wrong.
- **Search the non-code too.** Docs, fixtures, config, migrations, and string literals reference symbols that grep across `*.ts` will never see.
- **Follow the re-exports.** A symbol reachable under a second name has call sites your search for the first name did not return.
- **Prefer a symbol-aware tool where one exists.** A language server's "find references" beats text search on anything with shadowing, aliasing, or a common name.
- **Search for the concept as well as the identifier.** Renaming `fetchUser` also means finding the places that talk about "user fetching" in comments and docs.

## Reading before writing

- **Never write a file you have not read this session.** Not "have seen before", not "know the shape of".
- **Prefer a targeted edit over a rewrite.** It errors when your assumption is wrong; a rewrite succeeds and destroys the evidence.
- **Re-read before a late write.** In a long session, the file you read forty turns ago may not be the file on disk now.
- **Treat an unexplained line as load-bearing until proven otherwise.** The odd-looking workaround usually encodes a bug you have not met yet.
- **Regenerate generated files; never hand-edit them.** The next regeneration silently reverts anything you wrote.

## Matching conventions

- **Copy the shape of the code next to you.** Formatting, naming, imports, error style, test structure — take all of it from the neighbours, not from preference.
- **Run the project's formatter instead of formatting by hand.** Reproducing its rules from memory produces diffs that fight it later.
- **A convention you dislike still wins inside this change.** Argue for it separately; do not implement the argument as a side effect.
- **Don't add a dependency the project could already satisfy.** Check what is installed and what the standard library covers before reaching for a new package.
- **Never reformat lines you did not otherwise change.** Every one of them is noise the reviewer has to read past.

## Scope

- **One problem per change.** If you can name two reasons the diff exists, it should be two diffs.
- **Write down the improvement instead of making it.** Noticing a cleanup is valuable; bundling it is not.
- **Refactor first, then fix — as separate changes.** A behavior-preserving refactor is reviewable at a glance; a fix inside one is not.
- **Separate the mechanical from the semantic.** Renames and moves in one commit, behavior in another, so review effort lands where it matters.
- **Delete your debugging before you commit.** Temporary logging, scratch files, and loosened checks are the residue of investigation, not part of the fix.
- **A new abstraction with one caller is premature.** Wait for the second.

## Not inventing APIs

- **Look it up rather than remember it.** The dependency is on disk; checking costs seconds and being wrong costs a review cycle.
- **Confidence about an API is not information about it.** The plausible name and the real name feel identical while writing.
- **Check flags against the installed tool's `--help`,** not against a flag set from a different version.
- **If you cannot confirm it, do not write it.** Report the gap; a plausible placeholder is worse than a stated unknown.
- **Verify the package exists before adding it to the manifest.** Well-formed package names are easy to generate and easy to get wrong.

## Testing

- **Reproduce first, always.** A fix with no observed failure is a fix for the bug as described, which may not be the bug that exists.
- **Record the red, then the green.** Two observations, both from real runs, are what makes a fix demonstrated rather than asserted.
- **Break every new test once on purpose.** A test never seen failing has not been shown to test anything.
- **Pair every "nothing happens" assertion with a "something happens" case.** An absence test passes trivially when the mechanism is broken.
- **Run the suite, not just your test.** The regression you introduced is by definition somewhere you were not looking.
- **When a test fails after your change, suspect the code first.** Amend the test only when it is demonstrably the wrong party, and say so.

## Build, lint, and types

- **Run the build, the type check, and the lint before calling anything done.** They are the cheapest oracle over the errors an agent most often makes.
- **Use the project's command verbatim.** A hand-built equivalent can pass while the real one fails.
- **Fix lint violations rather than leaving them for CI.** CI finding them costs a round trip and tells the reviewer you did not run it.
- **Re-verify after the last edit.** Any change made after the last green run is unverified, including the small one you made while writing the summary.
- **Name what you could not run.** An unrunnable check is a stated gap, not an omission.

## Executed evidence

- **Read the exit code, not the output.** A log that reads fine and a nonzero status disagree exactly when it matters.
- **Never pipe a check into anything.** `cmd | tail` reports `tail`'s status, which is almost always success. Capture the status first, or set the shell to propagate it.
- **Empty output is not success.** It is often a wrong invocation; the exit code decides.
- **Suspect a clean first run.** A suite that passes immediately on a change you expected to break something usually is not running what you think.
- **Prove your verification can fail.** Break the thing, confirm red, restore, confirm green — once, at the start, for anything you will rely on repeatedly.
- **Say what you ran.** The command and its result are the evidence; a summary without them is a claim.

## Interfaces and migrations

- **Count the consumers before changing the shape.** The count decides whether this is an edit or a migration.
- **In-repo consumers change in the same commit.** A commit where the definition and its callers disagree does not build.
- **Out-of-repo consumers mean add-new, migrate, remove-old** — three steps, in that order, never one.
- **Ship the down migration with the up one,** or record why the change cannot be reversed.
- **Drop the column after the code stops reading it, not with it.** The deploy window between the two is where the outage lives.
- **State the compatibility direction explicitly** for any persisted or transmitted format: old-reads-new, new-reads-old, or both.

## Commits and pull requests

- **Ask what reverting this commit alone would do.** Collateral damage means it is too big; a broken build means it was split wrong.
- **Every commit builds.** A sequence where intermediate states are broken cannot be bisected, which is what commit history is for.
- **Describe the change, not the effort.** "Various fixes" is a message that tells the next reader nothing.
- **Put the commands and their real output in the test plan.** A test plan describing intended coverage is not a test plan.
- **State the gaps.** The most useful line in a description is usually the one admitting what was not verified.
- **Inspect what you staged before committing.** Scratch files, local config, and credentials get committed by accident, not on purpose.

## Responding to CI and review

- **Fix the cause, never the check.** An ignore directive removes the signal and leaves the defect.
- **Suppress only a demonstrated false positive,** narrowly, in place, with a comment saying why the check is wrong here.
- **A flaky test is a bug report, not an inconvenience.** Retrying until green trains everyone to ignore the next real failure.
- **Answer the objection, not the misunderstanding you would rather address.** Restating your original reasoning does not resolve a review comment.
- **Re-run everything after responding.** The fix you just pushed is unverified until it has been.
