# Heuristics — Design Patterns Pack

- **Name the problem before the pattern.** If you can't state the pain in one plain sentence without naming a pattern, you don't have the trigger condition yet.
- **Count real implementations.** Strategy/Factory/Adapter all assume ≥2 real variants; with exactly one, skip the pattern and inline.
- **Check the language first.** Reaching for a Strategy class hierarchy in a language with first-class functions is usually one function parameter away from simpler.
- **Singleton smell check:** if you're reaching for Singleton, ask whether it's actually "I want one shared instance injected everywhere" (fine, use DI) vs. "I want global mutable state reachable from anywhere" (usually a bug generator).
- **Pattern named in a PR description ≠ pattern actually needed.** Review whether the trigger condition is present in the code, not just whether the pattern's shape is recognizable.
- **Simplify before patterning.** Often the "need" for a pattern is a symptom of a class doing too much (SRP) — fix that first; the pattern-shaped need sometimes disappears.
