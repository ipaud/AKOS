# Prompt Fragments — Design Patterns Pack

## Fragment: build-mode constraint block

```text
Apply design patterns only where their trigger condition is real (AKOS L3):
- Before applying any GoF pattern, state the plain-language problem it
  solves and confirm ≥2 real implementations/variants exist (not hypothetical).
- Check for a native language feature first (closures, first-class
  functions, built-in iterators) before a class-based pattern.
- Avoid Singleton; use dependency-injected shared instances instead.
- Decorator/Composite only where dynamic per-instance composition or
  tree-uniform treatment is an actual requirement.
- Pattern-named classes/files must match the pattern's real structure.
```

## Fragment: review lens

```text
Review this code for design-pattern usage:
1. For every pattern-shaped structure (Factory, Strategy, Observer,
   Decorator, etc.), verify the trigger condition is present — plain
   problem statement + real variant count.
2. Flag patterns applied for hypothetical future needs (YAGNI violation).
3. Flag Singleton usage; suggest dependency injection instead.
4. Check whether a language-native alternative (function, closure) would
   be simpler than the class-based pattern used.
5. Verify pattern-named identifiers match their claimed structure.
```

## One-liner

```text
Patterns: name the problem in plain language first; apply only with ≥2
real variants; check for a native-language alternative before a class
hierarchy; avoid Singleton (use DI); pattern names must match structure.
```
