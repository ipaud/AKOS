# Prompt Fragments — Tool Design Pack

Copy-paste blocks for injecting this pack into agent prompts.

## Fragment: build-mode constraint block

```text
Apply tool-design constraints (tool-design pack, AKOS L2):
- Design for the agent as the user. A tool wrapped from a human-facing API
  exports missing context as the agent's problem. Everything a person would
  have looked up elsewhere must be carried at the call site.
- Name every tool as a verb plus an object stating its effect - not a noun,
  an abbreviation, or the endpoint it wraps. Namespace by provider.
- The description states what calling does and to what, whether it mutates
  state, what prerequisites exist, and - where a neighbouring tool exists -
  the situation this tool is NOT for, naming that neighbour.
- One tool, one effect describable in one clause without "and". A `mode` or
  `action` discriminator that changes which parameters are required means
  the tool is several tools sharing a name: split it.
- Never let one call perform several independently-failing side effects. If
  they must happen together, commit them atomically and report one outcome.
- Type every parameter. Enumerate closed sets as enums in the schema. Never
  accept structure inside a string the tool parses (query mini-languages,
  delimited lists, key-value blobs) - express it as schema structure.
- Validate at the boundary before any side effect runs; an invalid call must
  not partially apply.
- Return evidence, not acknowledgement. A write returns the resulting state -
  identifier, changed fields at their new values, count affected - so the
  caller can verify the effect matched the intent without a second call.
- Every error names what failed, which input caused it, what to do next, and
  whether the condition is retryable. A missing-prerequisite error names the
  tool that satisfies it. Never pass through a raw stack trace.
- Declare repeat-safety in the description. Side-effecting tools are
  idempotent, accept an idempotency key reused across retries, or state
  plainly that they are not safe to repeat.
- Any operation whose scope depends on unseen state exposes a dry run
  returning counts and identities in the same shape as the real response.
  Irreversible operations require a confirmation parameter with no default,
  specific to the operation - never a generic boolean.
- Bound every collection at the tool: a default limit, a hard maximum the
  caller cannot exceed, a cursor, a total count, and a byte cap alongside
  the item cap. Mark truncation in a structured field.
- Return stable identifiers with every entity, and accept them verbatim in
  the tools that consume them. Never make a caller reconstruct a reference.
- Where a blind overwrite would lose information, require a version or hash
  obtained from a prior read and reject a stale one.
- Keep tools, resources, and prompts as distinct primitives. Where the
  surface cannot separate them, state side-effect status in every description.
- Treat the first description as a draft. Run realistic tasks, read the
  traces, and fix observed wrong calls at the name, description, or schema -
  not in the calling agent's prompt.
- Before adding a tool, name the request it serves that nothing existing
  serves. Selection is a comparison across the whole surface; a near-synonym
  degrades the accuracy of its neighbours.
```

## Fragment: review lens

```text
Review this work as a tool-design reviewer (tool-design pack). Read the tool
definitions, the schemas, real response payloads, and at least one agent call
trace - not the descriptions alone.
1. Selection pass - cover the implementation and read only each name,
   description, and schema. For each tool, can you say exactly what calling
   does, to what, and whether anything changes? Flag every pair of tools a
   caller could map to the same request.
2. Granularity pass - flag any tool performing several independently-failing
   side effects, any `mode`/`action` discriminator changing which parameters
   apply, and any conditionally-required parameter. For each, name the
   specific split. Then flag the opposite: an invariant multi-call ritual
   every task repeats, which is a missing tool.
3. Hidden-effect pass - CRITICAL. Flag any side effect the name and
   description do not mention (notifications, audit writes, cache
   invalidation, webhooks).
4. Input pass - flag untyped parameters, closed sets documented as prose
   instead of enums, structure carried inside strings, parameters whose value
   could only be guessed, and any validation that runs after a side effect.
5. Evidence pass - CRITICAL. For each write, read ONLY the response and say
   what the caller can now assert. If the answer is "that the call did not
   error," that is an acknowledgement response and a correctness finding.
6. Error pass - for each error shape: does it name what failed, which input,
   what to do next, and whether to retry? Flag raw stack traces, bare
   strings, and message-text branching.
7. Repeat-safety pass - for every side-effecting tool, what happens if it is
   called twice with identical arguments? Flag any that is silent on this and
   is neither idempotent nor keyed.
8. Blast-radius pass - CRITICAL. For each operation, is the number of
   affected entities knowable from the arguments alone? If it depends on
   unseen state, it needs a dry run. If it is irreversible, it needs a
   confirmation parameter specific to the operation.
9. Bounding pass - for every collection-returning tool: default limit, hard
   maximum, cursor, total count, byte cap, structured truncation marker.
   "The data is small today" is not a bound.
10. Reference pass - trace a two-step task. At step two, is the agent passing
    a handle step one gave it, or reconstructing one from position or
    attributes? Reconstruction means the surface dropped an identity.
11. Primitive pass - does calling each item change anything? Where
    similar-looking items answer differently with nothing marking it, the
    agent cannot tell a free call from a consequential one.
12. Iteration pass - has the surface been exercised by a real agent on
    realistic tasks, with the traces read? Flag any wrong call being corrected
    in the calling agent's prompt rather than at the interface.
13. Run review-checklist.md; report findings by severity, and for every
    granularity finding name the specific split or merge - never "this does
    too much" without the alternative shape.
```

## Fragment: tool-definition worksheet

```text
Define this tool. Answer in order; an unanswerable question is a design gap,
not a documentation gap.

IDENTITY
- Name (verb + object, namespaced): ______
- The effect, in one clause without "and": ______
- Does calling it mutate state? YES / NO. What changes: ______
- Nearest existing tool: ______
- What this does that the nearest one does not: ______
  (If this needs a qualifier, the agent will need it too and will not have it.)

INPUTS
- Parameters, each with: type, required/optional, default, what it selects,
  and an example value: ______
- Closed sets declared as enums? YES / NO
- Any structure carried inside a string? (If yes, restructure.) ______
- Any parameter whose value the caller could only guess? ______
- Prerequisites the caller must satisfy first, and the tool that satisfies
  each: ______

OUTPUTS
- Success response fields: ______
- Reading ONLY that response, what can the caller assert? ______
  (If the answer is "it did not error," redesign it.)
- Stable identifier returned? YES / NO. Accepted by which tools: ______
- Collection returned? default limit / hard max / cursor / total / byte cap:
  ______

ERRORS
- Each error: code, what failed, which input, what to do next, retryable?
  ______

SAFETY
- Called twice with identical arguments, what happens? ______
- Idempotent / keyed / not repeat-safe (stated in description): ______
- Is the affected-entity count knowable from the arguments alone? ______
- Dry run needed? YES / NO. Confirmation needed? YES / NO. If yes, the
  operation-specific confirmation input: ______
- Reversible? Soft / recoverable / permanent: ______

VERIFICATION
- Tests for: success shape / error shapes / enforced limit / double call
- Has a real agent called this on a realistic task, with the trace read?
  YES / NO

Output the filled worksheet, then the tool definition. No prose preamble.
```

## Fragment: surface audit

```text
Audit this tool surface as a set, not tool by tool. Produce a table with one
row per tool:
- Name, and whether it reads or mutates (state UNMARKED if the description
  does not say).
- Nearest neighbour by name, and whether a caller reading only the two
  descriptions could pick correctly: DISTINCT / AMBIGUOUS.
- Effects performed: 1 / MULTIPLE (list them).
- Success response: EVIDENCE (returns resulting state) / ACKNOWLEDGEMENT.
- Collection returned: BOUNDED (default + max + cursor) / PARTIALLY BOUNDED /
  UNBOUNDED / N-A.
- Repeat-safety: IDEMPOTENT / KEYED / DECLARED-UNSAFE / SILENT.
- Blast radius: FIXED (determined by arguments) / STATE-DEPENDENT. If
  state-dependent: dry run PRESENT / ABSENT.
- Destructive: YES / NO. If yes: confirmation SPECIFIC / GENERIC / ABSENT.
Then report, in severity order: every MULTIPLE-effect tool, every ABSENT dry
run on a state-dependent operation, every ABSENT confirmation on a destructive
one, and every ACKNOWLEDGEMENT response on a write (all critical); every
UNBOUNDED collection, AMBIGUOUS pair, and SILENT repeat-safety (high).
Finally: the total tool count, the number of AMBIGUOUS pairs, and any tool
that an agent never selected across the evaluation set.
```

## One-liner (for tight token budgets)

```text
Tool rules: design for the agent as the user, not by wrapping a human-facing
API - the name, description, and schema are the whole interface, chosen blind
with no trial call; name tools verb-plus-object for their effect and say
whether they mutate; one tool, one effect describable without "and" - a mode
discriminator or a conditionally-required parameter means split it; never hide
several independently-failing side effects behind one name, because the caller
cannot tell what landed; type every parameter and enumerate closed sets, never
carrying structure inside a string the tool parses; validate before any side
effect runs; return evidence not acknowledgement - a write returns the
resulting state so the agent can verify its own work in the same turn; every
error names what failed, which input, what to do next, and whether to retry;
declare repeat-safety at the tool boundary and accept an idempotency key
reused across retries; give any operation whose scope depends on unseen state
a dry run, and any irreversible one an operation-specific confirmation with no
default; bound every collection at the tool with a default, a hard max, a
cursor, a total, and a byte cap - caller restraint is not a bound; return
stable identifiers the next call accepts instead of forcing positional
re-derivation; require a version token where a blind overwrite would lose
data; keep tools, resources, and prompts distinct so a free call is
distinguishable from a consequential one; treat the first description as a
draft and fix observed wrong calls at the interface, never in the caller's
prompt; and before adding a tool, name what it does that nothing else does -
selection is a comparison across the whole surface.
```
