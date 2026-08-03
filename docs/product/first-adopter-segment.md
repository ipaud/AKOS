# First-adopter segment and growth hypothesis

**Owner:** AKOS maintainer
**Decided:** 1 August 2026

`README.md` targets "any AI coding agent"; `CONTRIBUTING.md` frames AKOS as a
personal system. Both are true and neither answers who gets recruited for
the [activation baseline](activation-baseline.md) study, or whose experience
the next round of fixes should optimize for when two changes trade off
against each other. This file answers that, so the study has someone to
recruit and future prioritization has a tiebreak.

## Segment

**A solo developer, on a personal or small project, already using Claude
Code or Codex CLI.**

Not a guess — it's what the tool as built already optimizes for, checked
against evidence rather than asserted:

- **Distribution assumes one person, one machine.** `install.sh` symlinks a
  single `~/DEV/AKOS`; there is no account, no team config, no shared-profile
  mechanism. `packs/personal/pau-avila/` — the Level 0 layer every review
  loads — is one individual's preferences, not a team's.
- **The corpus weight matches it.** `scoring/overall-score.md`'s profile
  table gives Prototype and Startup MVP the lightest ceremony of the six
  profiles; the personal pack explicitly states "most of this owner's
  projects sit in Prototype or Startup MVP."
- **Claude Code and Codex CLI are the only two integrations with real
  skills**, not template fallback — `akos` and `akos-review` load on demand
  in both via the shared agent-skills format, with dedicated plugin
  marketplace entries for each. Cursor, Gemini CLI, and "other agents" all
  get a long-form Markdown template instead, a strictly weaker experience.
  `docs/product/activation-baseline.md`'s own "Primary job" already frames
  the target user as "a solo developer using Codex or Claude Code" — this
  file makes that explicit and load-bearing instead of implicit.

This doesn't contradict README's "any AI coding agent" — the Markdown-first
architecture really is tool-agnostic, and that claim stays true. It answers
a narrower question: whose *activation* gets measured and optimized for
first. Cursor/Gemini/generic support stays real but doesn't gate anything.

## Behavior that has to change

Today, without AKOS, this developer either re-explains review standards to
their agent every session, or skips systematic review and ships on the
agent's unaudited say-so. With AKOS installed, the hypothesis is: they run
`akos-review` (or ask for it in plain language) before merging or shipping,
instead of skipping that step — and they trust a finding more when it cites
a specific rule or pack than when the same agent asserts it unprompted,
because the citation is checkable.

## How they find it

Channels that already exist, no paid acquisition assumed:

- The public GitHub repo (`github.com/ipaud/AKOS`) and its README's install
  path.
- The Claude Code plugin marketplace (`/plugin marketplace add ipaud/AKOS`)
  and the Codex CLI equivalent.
- The public site (`akos-ai.lovable.app`).

## What would kill this hypothesis

The [activation baseline](activation-baseline.md) study, recruited from
exactly this segment (solo, Claude Code or Codex CLI, not maintainer-coached),
already defines the bar: at least 4 of 5 complete a review without
intervention, median time to first Review Summary ≤10 minutes, every
completed report cites inspected evidence. Falling short doesn't only mean
"fix onboarding" — if the shortfall traces to the segment itself (e.g. only
developers who already use Claude Code skills daily can self-serve, not
Claude Code users generally), the segment stated here needs narrowing before
the study is re-run, not just the install path.

## What this unblocks

The activation-baseline study can now recruit against a defined population
instead of an unstated one. It does not run the study — that still needs
five real people, which is the maintainer's task, not something a written
decision or an agent session produces.
