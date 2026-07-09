# Authority Model

Every piece of knowledge in AKOS carries an authority level. When sources agree, levels don't matter. When they conflict, levels decide who gets the benefit of the doubt — subject to [conflict-resolution.md](conflict-resolution.md) and the constitution's safety floor.

## The hierarchy

### Level 0 — Personal Project Rules

**Location:** `packs/personal/`
**Trust:** Highest priority *when they do not violate law, official standards' hard requirements, accessibility, or security.*

These are the owner's conventions: visual identity, naming, preferred stacks, project patterns, workflow preferences. They exist because consistency across one person's projects beats generic best practice. An agent applies them without being asked.

Examples: "Use React + Tailwind + Supabase by default", "every app ships empty/loading/error/success states", "challenge unnecessary complexity", "strong visual identity but interface stays obvious".

**Limit:** Level 0 rules cannot lower the safety floor. A personal preference for low-contrast aesthetics loses to WCAG contrast minima. A preference for speed loses to RLS on production Supabase tables.

### Level 1 — Official Standards & Platform Guidelines

**Trust:** Highest external authority. Their normative requirements ("must", "shall") are non-negotiable; their recommendations ("should") are near-mandatory with recorded justification for exceptions.

- WCAG (W3C) — accessibility
- OWASP (Top 10, API Top 10, ASVS) — security
- NIST (SSDF and related) — secure development
- Apple Human Interface Guidelines — Apple platforms
- Material Design — Android / Material surfaces
- IETF RFCs — protocols
- WHATWG / HTML Living Standard — the web platform

Platform guidelines are Level 1 *on their platform*. Apple HIG doesn't govern an Android app; on iOS it beats any generic UI advice.

### Level 2 — Industry Authorities

**Trust:** High. Broadly validated, decades of evidence, but not normative standards.

- Nielsen Norman Group (usability heuristics, research)
- Steve Krug (usability, testing)
- Don Norman (design of everyday things, human-centered design)
- Martin Fowler (refactoring, architecture)
- Kent Beck (TDD, XP)
- Google / Stripe engineering practice (as published)

When Level 2 sources conflict with each other, prefer the one closer to the domain (Krug on web usability, Fowler on refactoring) and say so.

### Level 3 — Books & Methodologies

**Trust:** Valuable but contextual. Methodologies encode a context (company size, era, market); applying them verbatim outside that context is a known failure mode.

- Inspired (Cagan), Lean Startup (Ries), Escaping the Build Trap (Perri), Continuous Discovery Habits (Torres)
- Clean Architecture (Martin), Domain-Driven Design (Evans), Design Patterns (GoF)
- Refactoring UI (Wathan & Schoger), Universal Principles of Design

Agents apply Level 3 ideas as decision frameworks, not commandments. Each Level 3 pack includes a "when NOT to use" section for this reason.

### Level 4 — Community Knowledge

**Trust:** Useful, unverified. Blog posts, GitHub repos, forum threads, Reddit, Medium.

Use for tactics and recent tooling knowledge, never as the sole basis for an architectural or security decision. Anything Level 4 that matters gets promoted into a pack with proper distillation — or it stays out of the reasoning.

## How agents use levels

1. **Cite the level.** "WCAG 1.4.3 (L1) requires…" / "Krug (L2) suggests…" / "team convention (L0)…"
2. **Higher level wins on hard requirements.** L1 "must" beats everything except law.
3. **Level 0 wins on preference.** Where standards are silent or permissive, personal rules decide — that's the point of having them.
4. **Proximity tiebreak.** Same level, both applicable → the source closer to the domain and platform wins.
5. **Never argue from level alone.** The level says who gets the benefit of the doubt; the agent still explains *why* the winning advice fits this case. See [conflict-resolution.md](conflict-resolution.md).

## Level vs. profile

Authority levels rank *sources*. [Reasoning profiles](reasoning-profiles.md) rank *concerns* (speed vs rigor). They compose: in Prototype profile an L1 "should" may be deferred with a note; an L1 "must" on the safety floor may not.

## Assigning levels to new packs

Every pack's `metadata.yaml` declares `authority-level`. Rules of thumb:

- Standards body or platform owner → 1
- Individual/organization with broad multi-decade acceptance → 2
- A book or named methodology → 3
- Everything else → 4
- Only `packs/personal/` is 0
