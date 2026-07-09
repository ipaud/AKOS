# Philosophy — Refactoring Pack

## Refactoring is a discipline, not a cleanup event

Refactoring means restructuring code without changing its observable behavior — improving internal structure so future changes are cheaper. Done right, it isn't a separate project phase ("refactoring sprint"); it's a continuous habit interleaved with every feature and bug fix: make the change easy (this may involve refactoring first), then make the easy change.

## Small steps, always-green

The core practice is disciplined smallness: each individual transformation is tiny enough to be obviously correct, verified by running tests immediately after, committed or at least checkpointed before the next step. This is what separates refactoring from "rewriting while hoping" — the code is never broken for longer than one small step, and the safety net (tests) makes every step cheap to verify.

## Code smells are diagnostic, not moral judgments

A code smell (long method, large class, duplicated code, feature envy, shotgun surgery) is a surface symptom pointing at an underlying design problem — not a style violation to fix reflexively. The point of naming smells is to build a fast, shared vocabulary for "something about this design is making change harder than it should be," so the conversation moves straight to which refactoring addresses it.

## Two hats, never worn at once

Fowler's rule: when working on code, you're wearing either the "adding function" hat or the "refactoring" hat, never both simultaneously. Mixing behavior changes with structural changes in the same step makes it impossible to tell, if something breaks, which change caused it. Refactor first to make the feature easy to add, *then* switch hats and add it — as two clearly separable steps, ideally two separate commits.

## Rewrites are usually the wrong answer

Big-bang rewrites carry enormous risk (the old system's accumulated bug fixes and edge-case handling get silently lost) and rarely deliver on schedule. Continuous refactoring achieves the same end state — a codebase that's pleasant to work in — without the multi-month freeze or the risk of the "second-system effect."
