# Engineering Rules — TDD Pack

- TD-E1. New feature/bugfix work for logic-bearing code follows Red-Green-Refactor: a failing test exists and is observed failing before implementation.
- TD-E2. Implementation added to pass a test is the minimum needed — no speculative generality beyond what the test requires.
- TD-E3. Refactor steps run the full relevant test suite before and after, with zero new failing tests introduced.
- TD-E4. Tests assert on behavior/outputs, not internal implementation details (private method calls, internal state shape).
- TD-E5. Commit history (where practical) reflects the cycle: test-added-and-failing, then implementation-and-passing, as distinguishable steps.
