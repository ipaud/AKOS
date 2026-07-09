# Mental Models — Refactoring Pack

## The rule of three

First time: just do it. Second time (similar code): wince, duplicate, move on. Third time: refactor to remove the duplication. Waiting for the third occurrence prevents premature abstraction from a sample size of one or two — the abstraction that emerges from a real third case tends to fit better than one guessed in advance.

## Two hats

At any moment, code work is either **adding function** (behavior changes, new tests must pass) or **refactoring** (structure changes, all existing tests must keep passing, no new behavior). Switching hats mid-step is how "small" refactorings turn into risky ones.

## Make the change easy, then make the easy change

Kent Beck's formulation, adopted by Fowler: when a feature is hard to add because of the current structure, the fix isn't to force the feature in awkwardly — it's to refactor the structure until adding the feature *would be* easy, then add it. The refactoring step often looks unrelated to the feature on its surface, but it's the actual unlock.

## Preserve behavior, verify continuously

Every refactoring step is followed by running the test suite (or the smallest relevant subset) before the next step. A refactoring session with tests run only at the end isn't refactoring — it's a leap of faith with a large blast radius if wrong.

## Smell → refactoring → structure

Code smells are pattern-matched symptoms; each has one or more standard refactorings that address it (Long Method → Extract Function; Duplicated Code → Extract Function + call from both sites; Feature Envy → Move Function). Knowing the map from smell to refactoring turns "this feels off" into a concrete next action.
