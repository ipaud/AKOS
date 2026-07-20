# Examples — Tool Design Pack

Invented cases. Bad → good, with the rule applied. All scenarios are fabricated for calibration, except the final section, which audits real code in this repository.

## The tool that did too much (TD4, TDE12–TDE16)

A CRM integration exposes `close_deal(deal_id, amount, notes)`. One call marks the deal closed, writes a commission row, sends a congratulations message to a Slack channel, and posts to an analytics endpoint. An agent closes a deal; the Slack call fails on an expired webhook. The tool returns `{"error": "notification failed"}`.

The agent now knows one thing: something about notification failed. It does not know whether the deal is closed, whether the commission row exists, or whether analytics recorded it. Retrying risks a duplicate commission row. Not retrying may leave the deal open. It picks one, and is wrong roughly half the time across a quarter.

After: `close_deal` does one thing, committing the deal state and its commission row in a single transaction and returning the closed deal with both. Notification and analytics become separate tools the agent calls next, each failing on its own terms. The Slack failure is now an error the agent can respond to correctly, because the thing it needed to know — the deal is closed — is already in the response it holds.

## Acknowledgement versus evidence (TD6, TDE27–TDE30)

A configuration service exposes `set_feature_flag(flag, environment, enabled)`, returning `{"status": "ok"}`. An agent asked to enable `new_checkout` in staging calls it, receives `ok`, and reports the flag enabled in staging. It was enabled in production: the `environment` parameter accepted any string, and the agent passed `"stage"`, which the service resolved through a legacy alias table to production.

Nothing errored. The agent's claim was an inference from a success token, and it reads in the transcript exactly like a verified fact.

After, the response carries state:

```
{ "flag": "new_checkout",
  "environment": "production",
  "enabled": true,
  "previous_value": false,
  "updated_at": "2026-07-19T14:02:11Z" }
```

The agent compares `environment` against what it intended, catches the mismatch in the same turn, and corrects — before the claim enters the transcript. `environment` also became an enum, which would have rejected `"stage"` outright. Two fixes, either of which catches this instance; the response fix also catches the class of mistakes nobody enumerated.

## Structure hidden in a string (TD5, TDE17–TDE20)

An issue tracker exposes `search_issues(query)` where `query` is a string documented as supporting `status:`, `assignee:`, `label:`, `created_before:`, and free text, with quoting rules for values containing spaces. An agent searching for open issues labelled `needs design` writes `status:open label:needs design`. The tool parses `label:needs` and treats `design` as free text. Eleven results come back, none of them right, and the call succeeded — so nothing signals the misparse.

After:

```
search_issues(
  status: "open",              // enum: open | closed | all
  labels: ["needs design"],    // array of strings
  assignee: null,
  created_before: null,        // ISO-8601 date, e.g. "2026-01-15"
  text: null,
  limit: 25                    // default 25, max 100
)
```

The quoting problem is gone because there is no grammar left to quote within. A misspelled status is now a rejected call naming the allowed values, rather than a silent zero-result search.

## The blind bulk delete (TD9, TDE51–TDE56)

A log-retention tool exposes `delete_logs(service, older_than)`. An agent asked to clear out old debug logs for the `checkout` service calls it with `older_than: "2026-07-01"`, intending to remove a few days of debug noise. The `service` field matches on prefix, so `checkout` also matched `checkout-worker` and `checkout-legacy`, and `older_than` applied to all severity levels, not just debug. Four million lines, including the error logs an incident review needed the following week.

After, two changes. `delete_logs` gains a dry-run mode returning the same shape as the real call:

```
{ "would_delete": 4112388,
  "services": ["checkout", "checkout-worker", "checkout-legacy"],
  "severity_breakdown": { "debug": 3901222, "info": 190144, "error": 21022 },
  "oldest": "2024-02-03", "newest": "2026-06-30" }
```

and the real call requires `confirm_count` to equal the number the dry run reported. The agent sees three services where it expected one and twenty-one thousand error lines it never intended to touch, and corrects the filter before anything is destroyed. The confirmation is specific — a count the agent could only supply by having previewed — rather than a boolean it could set reflexively.

## The unbounded return (TD10, TDE58–TDE64)

A monitoring integration exposes `get_metrics(service, from, to)`, returning every datapoint in the range at native resolution. An agent investigating a latency spike asks for a week of data on a high-traffic service. The call succeeds and returns roughly 600,000 datapoints. The session's remaining context is now mostly numbers; the agent's subsequent analysis is vague, it drops a constraint it was given four turns earlier, and it never identifies the spike — a failure that looks like poor reasoning and is a tool returning an unbounded payload.

After: a default of 500 datapoints and a hard maximum of 2,000, a required `resolution` parameter with the tool downsampling server-side, a `total_datapoints` field stating what the range actually contains, and a cursor. The response also carries `truncated: true` in a structured field rather than leaving the agent to notice the shortfall by counting.

## The positional reference (TD11, TDE65–TDE68)

A document tool's `search_documents` returns a list of `{title, snippet, folder}` objects with no identifiers. An agent finds the document it wants at position three and calls `update_document(title: "Q3 Planning", folder: "/strategy")` — the only handle available. Two documents in that folder share the title; the tool updates the older one. No error is raised anywhere, and the agent reports the update as done.

After, `search_documents` returns `document_id` on every result, and `update_document` takes `document_id` directly. The agent passes back a handle it was given rather than reconstructing an identity from attributes, and the ambiguity that produced the wrong write has nowhere left to enter.

## Iterating a description against observed calls (TD14, TDE77–TDE80)

A deployment surface has two tools: `rollback_service` (reverts to the previous release) and `restart_service` (restarts pods at the current release). Both descriptions were accurate: "Rolls back the named service to its previous release" and "Restarts the named service."

Twenty traced runs show the agent reaching for `rollback_service` on incidents where a restart was the correct remedy — six times out of twenty. A prompt-level fix ("prefer restart before rollback") was tried first and helped inconsistently.

Reading the traces showed the actual gap: the agent had no way to know that restart was cheaper, faster, and non-destructive of the current release, because neither description said anything about consequence. The revision:

- `restart_service` — "Restarts the named service's pods at the **current** release. Non-destructive; safe to call repeatedly. Try this first for transient failures (hung workers, memory pressure, stuck connections) before considering a rollback."
- `rollback_service` — "Reverts the named service to its **previous** release, replacing what is currently deployed. Use when the current release is itself the problem — not for transient failures, which `restart_service` handles without discarding the release."

Selection accuracy on the same twenty tasks went to twenty of twenty. Nothing about either tool's behavior changed; what changed is that each description now names the situation it is *not* for and points at its neighbour (TDE5).

---

## Checking our own house: `bin/akos` and `rules/runner.py`

The AKOS repository ships a CLI whose subcommands are, in practice, tools an agent calls — the `akos` skill instructs agents to run `akos rules run`, `akos history record`, `akos validate`, and others. It is worth auditing against this pack's own checklist, honestly, because it is a realistic surface: designed by someone competent, used by both humans and agents, and never reviewed specifically as an agent interface.

### What it gets right

**Verb-object naming across most of the surface (TDE1).** `list-packs`, `create-pack`, `show-profile`, `install-project`, `list-agents`, `list-skills` all state an effect and an object. An agent reading `akos help` can tell what most subcommands do without a trial call. This is not the norm for CLIs, which drift toward nouns and abbreviations.

**Errors that name the tool satisfying the prerequisite (TDE42).** This is the rule most surfaces miss, and `bin/akos` gets it right in three separate places. `profile use` against a project with no config fails with `"$config not found — run 'akos install-project' in $dir first"`. `profile show` on an unknown name fails with `"No such profile: $name (run 'akos profile list')"`. `rules explain` on an unknown ID fails with `"No such rule: $id (run 'akos rules list')"`. Each converts a dead end into a next call.

**An error that enumerates valid values (TDE41).** `akos review` with a bad domain returns `"Unknown review domain: '...'. Use: ux | security | architecture | full"` — the allowed set, inline, at the point of failure.

**Three distinguishable outcomes from one write (TDE30).** `write_marked_section` reports `created`, `updated AKOS section in`, or `appended AKOS section to`, depending on what it actually found. The caller learns which of three states the file was in rather than receiving one undifferentiated success.

**Guarded creates that are safe to call twice (TDE45–TDE46, in effect).** `create-pack` refuses when the directory exists (`"Pack already exists: $dest"`), and `profile create` does the same. `install-project` is genuinely idempotent by construction — the marker-delimited section is replaced rather than appended on a rerun, and a comment in the source records a real bug where exactly this silently failed to update. A rerun of any of the three cannot corrupt state.

**Evidence plus next action on success (TD6, TDE27).** `create-pack` returns `"Scaffolded pack at $dest (17 files). Fill principles.md first."`, followed by a warning naming the two follow-up steps (the routing table in `skills/akos/SKILL.md`, then `./doctor.sh`). The caller gets the path, the count, and what to do next.

**`rules/runner.py`'s `Finding` shape is the strongest part of the surface.** Each finding carries `rule_id`, `title`, `domain`, `level`, `severity`, `confidence`, `evidence` (a list of `{path, line_start}`), and `recommendation`. That is TDE37 and TDE65 in one structure: the evidence is a stable, directly-actionable reference the agent can open without re-deriving anything, and `recommendation` carries the next action in the payload rather than leaving it to be inferred. `--format json` makes it machine-consumable, and the exit codes are three genuinely distinct outcomes — 0 clean, 1 setup error, 2 an open CRITICAL — distinguishable without parsing prose.

**Partial failure reported rather than collapsed (TDE16).** A detector that throws does not crash the run; `run_rules` catches it and emits a finding carrying the error, so one broken rule degrades one rule rather than the whole scan. The source comment states this intent explicitly.

**Suppression keyed to a stable code (TDE44).** `akos:allow RULE_ID` matches on the rule's identifier, not on message text, so a reworded finding does not silently break existing suppressions.

### Where it falls short

**`link-project` is a pure alias for `install-project` — a direct TDE2 violation.** The two names sit in `akos help` as separate lines, and `main()` dispatches both to `cmd_install_project`. For a human this is a convenience. For an agent selecting from the help text it is two plausible candidates for the same request with no stated distinction — the exact condition TDE2 exists to prevent. The fix is to drop the alias from the help output, or remove it.

**`install-project` performs four independent writes behind one name (TDE12, TDE14, TDE16).** One call writes `CLAUDE.md`, `AGENTS.md`, `.cursor/rules/akos.mdc`, and `.akos/config.md`. Only the first is implied by the command name. Under `set -euo pipefail` a failure on the third leaves the first two written, and the caller gets a nonzero exit with no per-file report of what landed — the tool-that-does-too-much anti-pattern in miniature. The mitigating factor is real and worth stating: because each write is marker-scoped and idempotent, a rerun after a partial failure converges rather than compounding. The blast radius is bounded by construction even though the reporting is not.

**No structured output from any bash-native subcommand (TDE30, TDE32).** `list-packs` prints an indented, ANSI-colored tree; an agent consuming it must strip escape codes and infer the domain/pack nesting from leading whitespace. `list-agents`, `list-skills`, `rules list`, and `profile list` are the same. The Python-backed subcommands — `validate`, `rules run`, `benchmark`, `freshness` — do offer `--format json`, which makes the gap conspicuous rather than uniform: the surface teaches an agent that some subcommands are machine-readable and gives it no way to tell which without trying.

**Nothing in the surface states which subcommands mutate (TDE4, TDE75).** `akos help` lists seventeen commands in one undifferentiated block. `install-project`, `create-pack`, `profile create`, `profile use`, `history record`, and `history clean` change state on disk; the rest read. An agent choosing from that list has no way to tell a free call from a consequential one — this pack's collapsed-primitive anti-pattern (TD13), reproduced in a CLI. The fix is cheap: mark the mutating commands in the help text.

**`history clean` is advertised with no statement of scope or reversibility (TDE54, TDE56).** The help line reads `record|list|show <id>|latest|compare <a> <b>|clean`. Nothing says what `clean` removes, whether it confirms, or whether the removal is recoverable. Whatever the implementation does, the *surface* gives an agent no basis for caution, and the surface is what the agent selects from.

**No dry-run anywhere (TDE51).** `install-project` mutates four files in a user's project and `create-pack` writes seventeen, neither with a preview. In both cases the scope is fully determined by the arguments, which is the row in this pack's own table where a preview is not required — so this is a soft finding rather than a defect. It is worth naming because the exemption is load-bearing: if `install-project` ever gained a recursive or glob-scoped mode, the exemption would silently stop applying and nothing would flag it.

**`profile use` writes without a version check (TDE70).** It reads the marked section of `.akos/config.md`, rewrites the `personal_profile` line with `sed`, and writes the section back. Nothing detects a concurrent edit between the read and the write. The stakes are low — one line in a local config — but it is a blind read-modify-write in a file a human is also expected to edit by hand.

**`show-profile` changes behavior on arity, and duplicates `profile list` (TDE10, TDE2).** Called with no argument it lists profiles; called with one it prints a section. That is a discriminator changing what the call does, expressed as an arity rather than a parameter. Worse, the no-argument branch prints a hardcoded string of six reasoning-profile names while `profile list` enumerates `packs/personal/` from the filesystem — two commands, two different notions of "profile," one of them a literal that will drift from `core/reasoning-profiles.md` the first time a profile is added.

**No result bounds anywhere (TDE58, TDE59).** `list-packs` returns every pack, `rules list` every rule, `rules run` every finding. None has a default limit, a maximum, or a cursor. Today the counts are small enough that this never bites — the bound exists by accident of scale, not by design. TDE58's claim is precisely that caller restraint and small data are not bounds, and the first large repository scanned through `akos rules run --format json` is where that becomes visible.

**`list-skills` truncates in substance without marking it structurally (TDE62).** Descriptions are cut to 72 characters with `cut -c1-72` and an ellipsis appended. A human reader sees the ellipsis; a machine consumer would have no `truncated` field to read, because there is no structured output at all. Minor, and the same root cause as the previous finding.

**One error path passes through raw exception text (TDE39).** `run_rules`'s detector-failure branch emits `f"Detector error: {e}"` as the `recommendation`. This is a deliberate and defensible tradeoff — it keeps a broken detector debuggable instead of swallowing it — but it does put an unformatted Python exception string into a field whose contract is "what the caller should do next," and the caller cannot act on it.

### The honest summary

Scored against this pack's rubric, `bin/akos` lands well above the midpoint. It gets the two hardest things right — errors that name the next call, and a genuinely well-shaped finding structure in `rules/runner.py` — and its writes are idempotent by construction, which is the property most CLIs lack entirely. Its weaknesses cluster in one place and share one cause: it was designed for a human at a terminal, where ANSI color is a feature, an alias is a convenience, an undifferentiated help list is scannable, and small result sets need no bounds. Every one of those becomes a defect the moment the caller is an agent that can read only the help text and the output.

That is TD1, demonstrated on our own code: a tool built for a human is not automatically a good tool for an agent. The two cheapest fixes with the largest effect are marking the mutating subcommands in `akos help`, and extending `--format json` to the bash-native listings.
