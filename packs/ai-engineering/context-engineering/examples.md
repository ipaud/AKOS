# Examples — Context Engineering Pack

Invented cases. Bad → good, with the rule applied. All scenarios are fabricated for calibration.

## The kitchen-sink prompt vs. progressive disclosure (CE2, CE3, CEE1–CEE2, CEE7–CEE8)

A code-review agent's system prompt concatenated the full `principles.md` and `engineering-rules.md` of all twelve of its available knowledge packs into every session — accessibility, security, performance, testing, architecture, and so on — on the theory that a reviewer should "have everything available." The prompt alone consumed a large share of the window before a single line of the diff under review was read, and the model's actual findings clustered around whichever pack happened to be summarized nearest the end of the prompt.

After: the prompt loads each pack's one-paragraph `prompt-fragments.md` block for all twelve, and only opens a pack's full `principles.md`/`engineering-rules.md` when the diff under review actually touches that pack's territory (a `.sql` file present → open the database pack's depth; no `.sql` file → the fragment was enough). Total context for a typical review dropped by most of its prior size, and findings stopped correlating with prompt position.

## Context poisoning across turns (CE5, CEE17–CEE22)

An agent investigating a slow API endpoint runs a search early in the session and reads a two-year-old internal wiki page stating "the `orders` table has no index on `customer_id`." Three tool calls later, without re-querying the actual schema, the agent recommends adding that index — and two turns after that, it cites "the missing index we identified" as established fact while proposing a broader caching layer, treating its own earlier statement as independent confirmation.

The index was added eighteen months ago; the wiki page was never updated. The fix isn't "read more carefully" — it's CEE18: a claim about the current schema is re-verified against the actual database before it's allowed to anchor a recommendation, and a claim's second appearance in the same session doesn't count as a second source.

## Lossy summarization dropping a constraint (CE9, CEE35–CEE39)

A long refactoring session gets auto-compacted after forty turns. Turn 6 established, in an aside, "don't change the public API of `PaymentProcessor` — three other services import it directly." The compacted summary reads well: "We refactored the payment module for clarity and improved error handling." It does not mention the constraint, because the constraint was a single sentence buried in exploratory discussion and the summarizer optimized for narrative coherence.

Turn 41 — after compaction — renames a public method on `PaymentProcessor` for consistency with the rest of the refactor. Nothing in the compacted context said not to.

Fix: before compacting, the decisions/constraints/open-questions list is written explicitly —

```
Constraints:
- PaymentProcessor's public API must not change (three external importers)
Decisions:
- Internal helper methods may be renamed freely
Open questions:
- none
```

— and that list is carried into the compacted context verbatim, independent of how hard the narrative around it compresses.

## The wrong-tier memory (CE10, CEE40–CEE44)

During a bug-fix task, an agent writes "the intermittent test failure traces to a stale fixture in `test_orders.py`" into the project's persistent memory file — a fact scoped to one task, promoted to a tier meant for durable, project-wide conventions. Three months later, after the fixture's been fixed twice more for unrelated reasons, a different session reads the stale note and wastes time chasing a cause that no longer applies.

Meanwhile, in the same project, a genuinely durable convention — "this team writes commit messages in imperative mood, no ticket numbers in the subject line" — was only ever stated once, in a session that later got discarded without being promoted anywhere. Every new session re-litigates the convention from scratch.

Fix: the task-scoped fact stays in task memory and is discarded when the task closes; the durable convention gets written once to project memory the first time it's stated, and applied by default afterward.

## The full-repo dump vs. targeted search (CE15, CEE55–CEE58)

Asked to find every place a feature flag `ENABLE_NEW_CHECKOUT` is read, an agent in a 60,000-line monorepo opens files one directory at a time, working through the tree top to bottom, reading each file in full to check whether it mentions the flag. By the time it reaches the `services/` directory — where the flag actually lives — it has spent most of its context budget on files with no relevance to the question.

After: `grep -rn "ENABLE_NEW_CHECKOUT"` returns eleven hits across four files in under a second; each hit is opened at a targeted range around the match rather than in full. The task that took a full-repo pass and ran out of budget partway through completes with a small fraction of the context spent.

## Worked example: `skills/akos/SKILL.md`'s routing table as dynamic context selection

AKOS's own build-mode skill is a running instance of this pack's CE13 (route dynamically) and CE3 (progressive disclosure), not a hypothetical one. [skills/akos/SKILL.md](../../../skills/akos/SKILL.md) step 4 holds a single routing table of roughly fifty packs, each with a one-line "reach for it when" description, and instructs an agent to load 2–5 of them per task, chosen by fit rather than by name — explicitly warning that "picking `laws-of-ux` when the question is really about visual craft wastes a slot." Step 4 also instructs reading each selected pack's `prompt-fragments.md` before its `principles.md`, and reaching for `principles.md`/`engineering-rules.md` "only when the task needs depth beyond the fragment" — CE3 and CEE7/CEE8 as a working mechanism rather than a design goal.

It's a useful worked example precisely because it isn't a strawman: it caps the load (CEE2), separates the always-loaded personal/project layer from the routed layer (CE12), and requires stating what was loaded so a wrong routing choice is correctable (CEE50, step 5's "state the active profile and the packs you loaded" instruction). A stricter context-engineering pass would still tighten two things: the fifty-row table itself is read in full on every invocation regardless of how few packs get selected from it (a candidate for CE3's own medicine — sub-tables gated by the project's stated `Stack:`), and the precedence between a loaded pack's guidance and something the agent has directly verified against the codebase is left implicit rather than stated as a rule (CE5/CE7's territory). See [decision-framework.md](decision-framework.md) for the full critique.

## Preloading "just in case" vs. just-in-time (CE4, CEE12–CEE16)

A documentation agent is given the task of updating one API reference page. Its harness preloads the full contents of every file in `docs/` at session start, on the reasoning that the agent "might need to check cross-references." Most of those files are never read during the session; the one page that does need updating shares context space with dozens that don't, for the entire session.

After: the harness loads a manifest of `docs/` filenames and titles (a few hundred tokens) and fetches individual files by path only when the agent's own reasoning identifies a specific cross-reference to check. The one preload that's kept as a deliberate exception is the site's redirect map — genuinely needed on nearly every doc edit and expensive to query on demand — which is loaded up front and stated as such.
