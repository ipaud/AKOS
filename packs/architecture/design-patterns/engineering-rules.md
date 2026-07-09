# Engineering Rules — Design Patterns Pack

- DP-E1. No Strategy/Factory/Adapter pattern is introduced with fewer than 2 real (not hypothetical) implementations at time of introduction.
- DP-E2. Singleton classes are avoided in favor of dependency-injected shared instances; global mutable singletons are flagged wherever found.
- DP-E3. Before implementing a class-based Strategy/Command/Iterator, the codebase's language-native equivalent (function parameter, closure, built-in iterator) is considered and the choice justified if the class-based form is used instead.
- DP-E4. Decorator/Composite structures are used only where dynamic composition or uniform tree treatment is a real requirement — not for a single fixed combination.
- DP-E5. Pattern names used in code comments/naming (`OrderFactory`, `PaymentStrategy`) accurately reflect the GoF pattern's structure — misnamed "patterns" that don't match their claimed shape are corrected or renamed.
