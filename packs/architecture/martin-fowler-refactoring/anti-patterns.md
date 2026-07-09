# Anti-Patterns — Refactoring Pack

## Refactor-and-add-feature-in-one-commit

A PR titled "add discount feature" that also renames twelve variables and restructures three classes. Reviewers can't tell what's behavior change vs. structure change; a regression can't be bisected cleanly. Fix: MF1 — split.

## Refactoring without a safety net

Restructuring code with no tests, running nothing until "it looks done," then discovering three behaviors silently changed. Fix: MF3 — characterization tests first.

## Speculative abstraction from one example

Extracting a "reusable" helper after the first occurrence of similar-looking code, guessing at the general shape. Usually wrong in a way that costs more to un-abstract later than duplicating twice would have. Fix: RF7, rule of three.

## The never-ending refactor

A refactoring session that keeps discovering "just one more thing," growing from a 20-minute Extract Function into a two-day restructuring with no tests run in between. Fix: RF3 — small independently-verified steps; stop and commit at each green state.

## Refactoring as a hidden rewrite

Calling a full rewrite "refactoring" to avoid the scrutiny a rewrite decision would get. If behavior changes, tests are thrown out, or the codebase is unusable mid-way, it's not refactoring. Fix: MF6 — name it honestly, get the decision record.

## Big-bang legacy rewrite

Freezing feature work for months to rewrite a legacy system from scratch, losing accumulated edge-case fixes, missing the deadline, and often reverting. Fix: decision-framework — strangler fig incremental replacement.

## Smell-shaming without a fix path

Flagging "this is a god class" in review with no proposed refactoring, leaving the author to guess. Fix: RF5/RF6 — name the smell *and* the standard refactoring that addresses it.
