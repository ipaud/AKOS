# Knowledge Schema

Every knowledge pack in `packs/` provides the same **required** files, plus **optional** ones present only when the source has something distinct to say. Uniform structure is what makes packs machine-loadable: an agent can fetch exactly the file type it needs (`heuristics.md` for a quick pass, `review-checklist.md` for a review) from any pack without reading the whole thing. The required set is what every consumer (agents, skills, scoring) actually loads; the optional set is `philosophy`, `mental-models`, `examples`, `prompt-fragments`, `glossary` — a pack with nothing unique to add there simply omits the file rather than shipping a stub. `doctor.sh` enforces the required set; the optional ones are checked only for non-emptiness when present.

## The contract

**Required** — every pack has these:

| File | Purpose | Loaded when |
|------|---------|-------------|
| `README.md` | What this pack covers, in one screen; map of the other files | Always first |
| `metadata.yaml` | Machine-readable: name, domain, authority level, sources, tags, related packs | Pack discovery |
| `principles.md` | Durable, context-independent rules ("what is true") | Most tasks |
| `heuristics.md` | Fast judgment rules with known exceptions ("what to try first") | Quick reviews |
| `engineering-rules.md` | Concrete, checkable implementation rules ("what the code must do") | Implementation, review |
| `decision-framework.md` | How to choose between options this domain presents | Design decisions |
| `anti-patterns.md` | Named failure modes with detection cues and fixes | Reviews |
| `review-checklist.md` | Binary pass/fail checks, ordered by severity | Reviews |
| `scoring-rubric.md` | How to score 0–100 in this pack's dimension | Scoring |
| `references.md` | Sources: title, author, org, official URL — nothing copied | Attribution |
| `CHANGELOG.md` | Pack history | Maintenance |
| `VERSION` | Semver | Maintenance |

**Optional** — present when the source has something distinct to say:

| File | Purpose | Loaded when |
|------|---------|-------------|
| `philosophy.md` | The worldview behind the source — why it thinks what it thinks | Deep work, teaching |
| `mental-models.md` | The named models/concepts the source contributes | Reasoning about design |
| `examples.md` | Concrete before/after or good/bad cases, original wording | Calibration |
| `prompt-fragments.md` | Copy-paste blocks for injecting this pack into an agent prompt | Prompt building |
| `glossary.md` | Terms this pack uses precisely | Disambiguation |

The personal layer (`packs/personal/<name>/` — e.g. `packs/personal/pau-avila/`, the shipped default) is the one sanctioned exception: it uses a preference-oriented file set because it encodes one person's rules, not a distilled external source. Multiple personal profiles can coexist as siblings under `packs/personal/`; `.akos/config.md`'s `personal_profile` field picks which one a given project loads (see `akos profile`).

## metadata.yaml format

```yaml
name: steve-krug
domain: ux
authority-level: 2        # 0-4, see core/authority-model.md
version: 1.0.0
tags: [usability, web, cognitive-load, testing]
sources:
  - title: "Don't Make Me Think, Revisited"
    author: Steve Krug
    url: https://sensible.com/dont-make-me-think/
related:
  - packs/ux/nielsen-norman-group
  - packs/ux/laws-of-ux
```

`sources` is attribution only — the pack body must be original distillation (see [source-policy.md](source-policy.md)).

## Content quality bar

- Every file has meaningful first-version content. No placeholders, no "TBD".
- Rules are operational: an agent reading them can *act*. "Reduce cognitive load" is philosophy; "one primary action per screen, visually dominant" is a rule.
- Checklists are binary. If a check can't fail, it isn't a check.
- Examples use invented cases, not excerpts from the source.
- File length: aim 40–200 lines. A 600-line principles file means the pack should split.

## Distinguishing principles / heuristics / engineering rules

- **Principle** — always true in the domain: "users scan, they don't read".
- **Heuristic** — default with exceptions: "three clicks with clear scent beats one ambiguous click; break it when the scent is strong".
- **Engineering rule** — checkable in an artifact: "interactive touch targets ≥ 44×44pt on iOS".

When unsure, ask: could a linter check it? → engineering rule. Would an expert say "usually"? → heuristic. Would they say "always"? → principle.

## Creating a pack

Clear the [source intake gate](source-policy.md#source-intake-gate) first — it decides
whether the source earns a pack at all. Then `akos create-pack <domain>/<name>` scaffolds
the contract, and:

1. Set `metadata.yaml` (authority level per [authority-model.md](authority-model.md)).
2. Write `principles.md` first — it forces the distillation.
3. Derive `review-checklist.md` and `engineering-rules.md` from the principles.
4. Fill the rest; link related packs in the relevant `graphs/` file.
5. Add the pack to the routing table in `skills/akos/SKILL.md` — a pack absent from it
   is a pack agents can't route to.
6. Run `./doctor.sh` — it verifies the required-file contract.

## Draft → stable

`akos create-pack` writes `status: draft`. A draft pack is readable but excluded from
automatic routing: it sits in the Experimental table in `skills/akos/SKILL.md`, loads
only when the user asks for it by name, and no stable agent or workflow may depend on
it (`schemas/routing_check.py` enforces both directions).

Promotion is a judgment call with a fixed evidence bar, not a calendar event. All of
these hold before `status` flips:

- **Content bar met in every required file** — no placeholders, no "TBD", nothing that
  reads as scaffolding output. See the bar above.
- **Rules are operational and binary.** Every `engineering-rules.md` entry is checkable
  in an artifact; every `review-checklist.md` item can fail.
- **Every cited rule code is defined in the pack that cites it**
  (`tests/unit/test_pack_citations.py`).
- **Every `sources[].title` is grounded in `references.md`, verbatim**
  (`tests/unit/test_sources_references_integrity.py`).
- **The rule-code prefix is globally unique** — one defining pack per prefix
  (`tests/unit/test_pack_prefix_uniqueness.py`).
- **`README.md` carries the independent-distillation line** (`doctor.sh`).
- **The pack is linked from `graphs/knowledge-graph.md`** (`doctor.sh`).

The criterion deliberately reuses checks that already exist rather than inventing new
ones — a promotion bar nothing enforces is a bar that drifts.

On promotion: set `status: stable`, re-stamp `last_reviewed` to the promotion date,
recompute `review_after` from the authority-level cadence, bump the patch version in
`VERSION` *and* `metadata.yaml` together, add a `CHANGELOG.md` entry, and move the
pack's row from the Experimental table into the stable routing table in
`skills/akos/SKILL.md`. `routing_check.py` fails if the row and the status disagree.
