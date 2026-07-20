# Anti-Patterns — Tool Design Pack

Named failure modes. Detection cue → why it fails → fix. The first block covers failures that produce *a wrong effect, an unrecoverable partial state, or a confidently unverified claim*; those are correctness defects and are scored as such.

## The tool that does too much

**Detect:** one call performs several unrelated side effects — creates the record, sends the notification, writes the audit row, invalidates the cache — and the name mentions one of them.
**Why it fails:** partial failure becomes unrecoverable. When the third effect fails, the caller gets one error and no way to learn what landed; retrying re-applies the first two, not retrying leaves the fourth undone, and there is no information available with which to choose. The convenience of one call is borrowed against the first bad run.
**Fix:** one effect per tool, describable in one clause without "and" (TD4, TDE12, TDE14). Where several effects genuinely must happen together, commit them atomically and report one outcome for the whole; where they can fail independently, split them and let the caller sequence them.

## The acknowledgement response

**Detect:** a write returns `{"status": "ok"}`, `{"success": true}`, or an empty 204, and the agent's next turn reports the operation as done.
**Why it fails:** the agent cannot distinguish "did exactly what you meant" from "did something and didn't throw," which is where the interesting failures live — valid arguments, wrong effect. Having nothing to verify against, the agent asserts success anyway, and an unverified claim enters the transcript that later turns treat as established fact.
**Fix:** return the resulting state — identifier, changed fields at their new values, count affected — so the caller can compare intent to effect inside the same call (TD6, TDE27–TDE29).

## The blind destructive call

**Detect:** a delete, bulk update, or recursive operation scoped by a filter, with no dry-run mode and no confirmation parameter, reachable by an agent in one call.
**Why it fails:** the number of affected entities depends on state the agent cannot see. Its filter matches four records in its model of the data and four thousand in the database, and the call is identical either way. The gap only becomes observable after the operation is irreversible.
**Fix:** expose a dry run returning the count and identity of what would be affected, in the same shape as the real response, and require a confirmation parameter that names the target, count, or scope (TD9, TDE51–TDE55).

## The unbounded return

**Detect:** a tool that returns whatever the query matched, with no default limit, no enforced maximum, and no cursor.
**Why it fails:** the failure mode is a success. The call that returns forty thousand rows does not error — it floods the context window, degrades every subsequent decision in the session, and removes the agent's capacity to notice that this is what happened. A defect in the tool arrives as a context failure one call later.
**Fix:** enforce a default limit and a hard maximum at the tool, return a cursor and a total count, and cap bytes as well as items (TD10, TDE58–TDE64; see [context-engineering](../context-engineering/README.md) CE1, CE6).

## The silent non-idempotent retry target

**Detect:** a side-effecting tool that says nothing about repeat-safety, sitting in a surface an agent retries through.
**Why it fails:** the agent will call it twice — after a late timeout, on a retry, when a replan re-executes a completed step — and whether that is safe is a fact about the tool that the agent can only discover by causing the duplicate. Silence gets resolved as whichever the agent assumed, and the assumption is not recorded anywhere.
**Fix:** every side-effecting tool is naturally idempotent, accepts an idempotency key reused across retries, or states plainly that it is not repeat-safe so a caller can gate it (TD8, TDE45–TDE50).

## The stringly-typed parameter

**Detect:** a parameter documented as a string in a format the description explains — `"status:open assignee:me sort:-created"`, a comma-separated list, a `key=value` blob.
**Why it fails:** the agent must serialize structure into text using a grammar it can only learn by example, so the tool can parse it back into structure. Every step is a chance to be silently wrong, and the failure is a misinterpretation rather than a rejection — the call succeeds against something the caller didn't mean.
**Fix:** express structure as schema structure. Objects and arrays for composite input, enums for closed sets, declared patterns with an example for genuine strings (TD5, TDE17–TDE20).

## The uninformative error

**Detect:** errors reading `400 Bad Request`, `invalid input`, `operation failed`, or an unmodified stack trace.
**Why it fails:** the agent's only decision on reading an error is what to do differently, and none of these inform it. So it falls back on its most expensive strategy — change something plausible and call again — turning one malformed parameter into six wasted calls, each leaving residue in the context.
**Fix:** name what failed, which input caused it, and what to do next, plus whether the condition is retryable. A missing prerequisite names the tool that satisfies it (TD7, TDE37–TDE44).

## The positional reference

**Detect:** an agent's second call identifies its target by position or description — "the third result," "the file from the earlier listing" — because the first call returned no stable identifier.
**Why it fails:** the agent re-derives an identity the tool already had and discarded, against a world that may have changed since. The list reordered, the index shifted, the name was ambiguous between two matches — and the wrong entity gets modified with no error anywhere.
**Fix:** return a stable identifier with every entity, and have the tools that act on it accept that identifier verbatim (TD11, TDE65–TDE68).

## The overloaded mode parameter

**Detect:** a tool taking `mode`, `action`, or `operation`, where the value determines which of the remaining parameters are required and which are ignored.
**Why it fails:** it is several tools sharing a name, and the schema cannot express its own rules — "these four fields matter only when mode is `export`" is a sentence in a description, not a constraint. The agent must first infer which variant it wants, then satisfy that variant's requirements while ignoring the others', with no validation catching a cross-variant mistake.
**Fix:** split into one tool per branch of the discriminator. A conditionally-required parameter is the split announcing itself (TD3, TDE10–TDE11).

## The collapsed primitive

**Detect:** a server exposing readable documents, mutating operations, and reusable templates all as tools, with names and shapes that give no clue which is which.
**Why it fails:** the agent loses the one distinction that matters most before calling something — whether calling is free. Either every document read is weighed with the caution due a deletion, wasting turns on deliberation, or a mutation sitting among read-shaped neighbours gets called with the freedom due a read.
**Fix:** separate tools, resources, and prompts per the MCP primitive split; where a surface genuinely cannot, state side-effect status explicitly in every description (TD13, TDE73–TDE75).

## The never-revised description

**Detect:** a tool description unchanged since it was written, with prompt-level instructions accumulating around it to correct the agent's calls ("when using X, remember to...").
**Why it fails:** the description was written from inside the knowledge of how the tool works, the exact vantage point that conceals its ambiguities. The prompt patches treat each symptom per-agent and per-session while the defect stays in the interface, so every new caller rediscovers it.
**Fix:** run realistic tasks, read the traces, and fix the observed wrong calls at the name, description, or schema rather than in the prompt (TD14, TDE77–TDE80).

## The catalogue surface

**Detect:** a surface that grew to dozens of tools, several near-synonymous, with selection errors answered by lengthening the descriptions of the ones being confused.
**Why it fails:** selection is a comparison across the whole set, so overlap between two tools cannot be fixed inside either one. Longer text is not greater discriminability — it costs budget and leaves the ambiguity exactly where it was, while every added neighbour lowers accuracy further.
**Fix:** merge or remove overlapping tools rather than disambiguating them with prose; before adding, name the request served by nothing existing; track surface size against a stated ceiling (TD15, TDE82–TDE86).

## The endpoint transliteration

**Detect:** a tool surface whose names, parameters, and response envelopes mirror an existing HTTP API one-for-one — `records_batch_mutate`, a `payload` object wrapping the real arguments, framework metadata in every response.
**Why it fails:** it exports an implementation as the agent's vocabulary. The names describe transport rather than effect, the envelopes cost budget and carry nothing actionable, and everything a human would have looked up in the API docs is simply missing — which the agent pays for in exploratory calls.
**Fix:** design the surface for the agent as its user, naming effects rather than endpoints, and carrying at the call site whatever a human would have looked up elsewhere (TD1, TDE1, TDE33).

## The untestable contract

**Detect:** a tool with no tests for its error shapes, its enforced limit, or its behavior on a repeated identical call — its contract living entirely in prose.
**Why it fails:** whatever the agent infers becomes the de facto contract, and that inference differs between models, between versions, and between the happy path and the third retry. Nothing detects the drift, because nothing ever asserted the shape.
**Fix:** test the success shape, the error shapes, the enforced limit, and the double call. The tests are the contract; the description is its summary (TD16, TDE81).
