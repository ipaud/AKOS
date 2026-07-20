# Heuristics — Tool Design Pack

Fast defaults with known exceptions. Try these first; deviate with a reason.

## Naming

- **Verb plus object, always.** `cancel_subscription` beats `subscription` and beats `manage_billing`. If the name isn't a verb, the agent has to infer the effect from the description alone.
- **Name the effect, not the endpoint.** Wrapping `POST /v2/records:batchMutate` as `records_batch_mutate` exports your implementation as the agent's vocabulary.
- **Read your two most similar names side by side.** If you need the descriptions to tell them apart, so will the agent, and it only reads them under time pressure.
- **Namespace by source.** Three servers each offering `search` is three ways to be wrong.
- **Avoid names that could describe a read or a write.** `update_index` — does it fetch the index or rebuild it? Pick a verb that can only mean one of the two.

## Granularity

- **A `mode` parameter is two tools wearing a trench coat.** Split it.
- **Conditionally-required parameters mean the split is already there**, you just haven't made it.
- **If you can't describe the tool in one clause without "and," it's doing two things.**
- **Ask what a half-success looks like.** If the caller can't tell what landed, the tool is too coarse.
- **But notice the invariant ritual.** If every task starts with the same three calls in the same order, that sequence is a tool you haven't written.
- **Prefer the coarsest granularity at which every failure is still attributable.** That's the rung, not "as small as possible."

## Inputs

- **If the description explains a format, the schema should have enforced it.** Prose grammar is a parser you're asking the agent to implement.
- **Enums over documented strings.** A closed set in the schema is a whole error class deleted.
- **Never accept structure inside a string.** Query mini-languages, comma lists, `key:value` blobs — express them as objects and arrays.
- **Give every string parameter an example.** One concrete value teaches more than three sentences of format description.
- **Name parameters positively.** `include_drafts` beats `exclude_published`; negation compounds badly with a second flag.
- **If a parameter's value can only be guessed, add the tool that discovers it.** An ID with no lookup is a dead end.

## Outputs

- **Return the thing, not the news that there is a thing.** A created record beats `{"created": true}` plus an ID.
- **Ask what the caller can assert after reading only the response.** If it's "the call didn't error," you've returned an acknowledgement.
- **Return the changed fields on a write**, so the agent can check the effect matched the intent in the same turn.
- **Keep the shape stable.** A field that changes type based on the result forces defensive handling forever.
- **Strip what the caller can't act on.** Framework envelopes, internal keys, and storage timestamps are budget spent on nothing.
- **Return values in the format your own inputs accept**, so a response can be fed straight back in.

## Errors

- **Every error answers "what do I do differently."** If it doesn't, the agent's only move is to vary something and retry.
- **Name the field, name the constraint, show a valid value.** Three short facts beat a paragraph.
- **Say whether it's worth retrying.** Retryable and non-retryable are different instructions, and the agent can't tell them apart from a status code alone.
- **Never pass through a stack trace.** It's long, it's mostly irrelevant, and it invites the agent to reason about your internals.
- **A missing prerequisite error should name the tool that satisfies it.** That converts a dead end into a next call.
- **Codes for branching, messages for reading.** Don't make a caller match on prose.

## Repeat-safety

- **Assume it will be called twice.** Retries, late timeouts, and replans all produce duplicates; the question is only whether the second call is harmful.
- **Say so in the description, either way.** Silence gets read as whichever the agent assumed.
- **Idempotency key as an explicit parameter**, reused across retries of the same logical action — not regenerated per attempt.
- **Read-only tools should say they're read-only.** It's the cheapest way to make a tool freely retryable.
- **Test the second call.** A repeat-safety claim nobody exercised is a comment.

## Consequential and destructive operations

- **If the scope depends on the arguments, ship a dry run.** The agent cannot see the data; the tool can.
- **Dry run returns the same shape as the real thing**, or the caller has to interpret twice.
- **Preview reports counts and identities, not a sentence.** "Would affect 4,213 records" is checkable; "would update matching records" is not.
- **Confirmation parameters have no default.** A default is not a confirmation.
- **Make the confirmation specific.** Naming the target or the count forces the agent to have looked; a bare boolean does not.
- **State reversibility in the description.** Soft delete, recoverable, and gone forever are three different risks.

## Bounding results

- **Every collection-returning tool caps itself.** Caller restraint is not a bound.
- **Two numbers: a default and a hard maximum.** The caller can ask for less, never for more.
- **Cursors, not offsets**, wherever the underlying set can change between calls.
- **Say the total, or say you can't.** The agent needs to know the size of what it didn't get.
- **Cap bytes as well as items.** Ten items can be larger than a thousand.
- **Support ranged reads on anything document-shaped.** Whole-file reads are the default that quietly costs the most.

## References

- **Return an ID with everything.** The next call should never need to reconstruct which one you meant.
- **Accept the ID you emitted, verbatim.** Requiring the caller to reformat it is a derivation step you added back.
- **Return the name too, but act on the ID.** Names are for the agent's reasoning, IDs for its calls.
- **If a handle expires, say when.** A silently stale cursor fails at the least informative moment.

## Primitives

- **Ask "does calling this change anything" for every item in the surface.** Group by the answer; that's the primitive split.
- **Don't expose readable context as a tool** just because tools were the easy path.
- **If you can't separate them, say it in every description.** Explicit "read-only, no side effects" is the fallback when the surface can't carry the distinction.

## Iteration

- **Watch an agent use it before you call it done.** Not a demo — a realistic task, with the trace read afterwards.
- **Fix wrong calls at the interface, not in the prompt.** A prompt patch is per-agent and per-session; a description fix is permanent.
- **Every observed wrong call is a specification bug** until proven otherwise.
- **Measure selection accuracy across the surface before and after a rename.** Descriptions interact; a local fix can be a global regression.
- **A tool nothing ever selects is either misnamed or unnecessary.** Both are findings.

## Surface size

- **Before adding, name what it does that nothing else does.** If the sentence needs a qualifier, so will the agent.
- **Merge neighbours rather than disambiguating them with longer text.** Length is not discriminability.
- **Delete deprecated tools.** A deprecation note in a description is a trap with a warning label.
- **Load the tools the task needs, not the catalogue.** (See [context-engineering](../context-engineering/README.md) CEE5.)
