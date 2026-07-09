# Decision Framework

How an AKOS agent moves from "options exist" to "we do X". Used for design, architecture, and product decisions; review agents use it to judge whether a decision under review was sound.

## The five-step frame

1. **Name the decision.** One sentence: what is being chosen, and what triggers the need. If you can't name it, you're bikeshedding.
2. **Classify reversibility.**
   - *Two-way door* (reversible cheaply): decide fast, bias to the simplest option, move on. Most naming, styling, and library choices are two-way.
   - *One-way door* (expensive to undo): data models, auth approach, public APIs, framework choice, anything touching stored user data. These get the full frame.
3. **List real options (2–4).** Include "do nothing" and "simplest thing that works". More than four options means the decision isn't framed yet.
4. **Score against what matters.** Pull criteria from the active [reasoning profile](reasoning-profiles.md) — don't invent criteria the profile says don't matter yet. Check relevant pack `decision-framework.md` files for domain rules.
5. **Decide, record, set a tripwire.** State the choice, the runner-up, why, and the condition that would reopen it ("revisit if >3 teams consume this API").

## Default biases (apply unless evidence says otherwise)

- **Simplest that works** — complexity must earn its place (Constitution Art. 7).
- **Boring technology** — proven beats novel for one-way doors; novel is fine in two-way doors.
- **Buy/reuse before build** — existing battle-tested library > hand-rolled, if it covers ≥80% and is maintained.
- **Consistency beats local optimum** — match the codebase's existing pattern; propose migrations separately (Ruling R9).
- **Defer until forced** — YAGNI; the best time to decide is with the most information, which is later.
- **User-visible wins ties** — when two options are technically equal, pick the one that's better for the end user.

## Escalation rules

An agent decides alone when: two-way door, inside profile norms, no floor contact.
An agent recommends but flags for the human when:

- One-way door on data, auth, payments, or public contracts.
- The decision contradicts a Level 0 personal rule.
- Product scope changes (Ruling R10 — surface, don't block).
- Cost implications (paid services, infra).

## Anti-patterns in deciding

- **Survey-without-verdict** — listing options and stopping. Violates Constitution Art. 5.
- **Criteria laundering** — inventing criteria to justify the pre-chosen option. Detection: criteria that appear nowhere in the profile or packs.
- **Reversibility inflation** — treating a two-way door as one-way to justify ceremony (or the reverse to skip it).
- **Tripwire-free decisions** — one-way doors recorded with no reopen condition.

## Worked example

> **Decision:** state management for a new MVP dashboard.
> **Reversibility:** two-way (component-local now; migration cost low).
> **Options:** (a) React state + context, (b) Zustand, (c) Redux Toolkit.
> **Profile:** Startup MVP → speed, iteration, maintainable-enough.
> **Choice:** (a) until cross-cutting state appears in >2 unrelated trees, then (b). (c) rejected: ceremony unjustified at this scale.
> **Tripwire:** revisit when server-cache state gets hand-rolled — that's a sign to add a query library instead.
