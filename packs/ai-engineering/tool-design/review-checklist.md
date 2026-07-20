# Review Checklist — Tool Design Pack

Binary checks, ordered by severity. Each unchecked box is a finding at the listed severity. Checks marked ★ are safety-floor items (an unrecoverable partial effect, an unpreviewed destructive operation, or a claim the agent could not have verified) and block in every reasoning profile.

Reviewing a tool surface means reading the tool definitions, the schemas, real response payloads, and at least one agent call trace — not the description alone. Several checks require the trace or a live response; those say so.

## Critical (blocks in every profile)

- [ ] ★ No tool performs several independently-failing side effects behind one name; effects that must happen together commit atomically. (TDE12, TDE13)
- [ ] ★ Partial failure across multiple entities is reported per entity, not collapsed into one aggregate error. (TDE16)
- [ ] ★ No tool silently performs a side effect its name and description do not mention. (TDE14)
- [ ] ★ Every operation whose scope depends on unseen state exposes a dry-run mode. (TDE51)
- [ ] ★ Destructive and irreversible operations require an explicit confirmation parameter with no default. (TDE54)
- [ ] ★ Every side-effecting tool is idempotent, accepts an idempotency key, or states that it is not repeat-safe. (TDE45, TDE46, TDE48)
- [ ] ★ **Response check:** a write returns the resulting state, not a bare success token. (TDE27, TDE28)
- [ ] ★ No destructive effect is reachable through a tool whose name does not describe destruction. (TDE57)
- [ ] ★ Input is validated at the boundary before any side effect runs; an invalid call does not partially apply. (TDE23)

## High

- [ ] Every tool name states its effect as a verb plus an object, not a noun or a wrapped endpoint name. (TDE1)
- [ ] No two tools have names a caller could map to the same request. (TDE2)
- [ ] Each description states whether the call mutates state, and what it changes. (TDE4)
- [ ] No tool takes a discriminator parameter that changes which other parameters are required. (TDE10, TDE11)
- [ ] No parameter is conditionally required based on another parameter's value. (TDE11)
- [ ] No parameter carries structured content inside a string that the tool parses. (TDE19)
- [ ] Closed sets of values are declared as enums in the schema, not as prose. (TDE18)
- [ ] Every parameter has a declared type appropriate to what it represents. (TDE17)
- [ ] Every error names what failed, which input caused it, and what to do next. (TDE37)
- [ ] Errors are structured with a stable code, not a bare string or a raw exception. (TDE38)
- [ ] Errors distinguish retryable from non-retryable conditions explicitly. (TDE40)
- [ ] Every collection-returning tool enforces its own default limit and a hard maximum. (TDE58, TDE59)
- [ ] Paginated responses return a cursor and a total count, or state that a total is unavailable. (TDE60, TDE61)
- [ ] Truncation is marked in a structured field, not signalled by the absence of results. (TDE62)
- [ ] Every returned entity carries a stable identifier, and the tools acting on it accept that identifier. (TDE65, TDE66)
- [ ] Where a blind overwrite would lose information, the write requires a version token from a prior read. (TDE70)
- [ ] Success and failure are distinguishable structurally, not only by reading a message string. (TDE30)
- [ ] A dry-run response has the same shape as the real response and reports counts and identities. (TDE52, TDE53)

## Medium

- [ ] Descriptions open with what the call does and to what, before implementation detail. (TDE3)
- [ ] Descriptions name the situations the tool is for, and the neighbouring tool it is not for. (TDE5)
- [ ] Prerequisites are stated in the description rather than discovered by failing. (TDE6)
- [ ] Tool names are namespaced by provider or server. (TDE7)
- [ ] Terminology is consistent across a tool's description, parameters, and response fields. (TDE9)
- [ ] An invariant multi-call sequence repeated on every task is available as one tool. (TDE15)
- [ ] String parameters declare their expected format with an example value. (TDE20)
- [ ] Every parameter's description says what it selects or controls, not just its name again. (TDE21)
- [ ] Optional parameters document their defaults. (TDE22)
- [ ] Validation failures name the specific parameter and constraint. (TDE24)
- [ ] Parameter names avoid negation and non-universal abbreviations. (TDE25)
- [ ] No parameter requires a value the caller could only obtain by guessing. (TDE26)
- [ ] Operations affecting multiple entities return the count and identifiers affected. (TDE29)
- [ ] Response shapes are stable across calls; no field changes type based on the result. (TDE31)
- [ ] Responses omit fields the caller cannot act on. (TDE33)
- [ ] Large responses state their total size or count alongside the content. (TDE34)
- [ ] Response values are returned in the same format the tool's inputs accept. (TDE36)
- [ ] No error surfaces an unmodified stack trace or database error text. (TDE39)
- [ ] Malformed-argument errors suggest a valid form. (TDE41)
- [ ] Missing-prerequisite errors name the tool that satisfies the prerequisite. (TDE42)
- [ ] Idempotency keys are explicit parameters, reused across retries of the same logical action. (TDE47)
- [ ] Read-only tools are documented as read-only. (TDE49)
- [ ] Confirmation parameters are specific to the operation, not a generic boolean. (TDE55)
- [ ] Destructive operations state their reversibility. (TDE56)
- [ ] Document-returning tools support a range, offset, or section selector. (TDE63)
- [ ] Response size is capped in bytes or tokens as well as item count. (TDE64)
- [ ] Identifiers are accepted verbatim by consuming tools, with no reformatting required. (TDE67)
- [ ] Mutating capabilities are exposed as tools, readable material as resources, templates as prompts. (TDE73)
- [ ] Where primitives cannot be separated, every description states side-effect status explicitly. (TDE75)
- [ ] A stale version token is rejected with an error naming the read tool to re-fetch. (TDE71)

## Low

- [ ] No description relies on information unavailable at selection time. (TDE8)
- [ ] Both a stable identifier and a human-readable name are returned where both exist. (TDE68)
- [ ] Expiring cursors, handles, and tokens state their validity window. (TDE69)
- [ ] Where reading first is advisable but unenforced, the write tool's description says so. (TDE72)
- [ ] No read-only context is exposed as a tool merely for convenience. (TDE74)
- [ ] Resource identifiers are stable and re-fetchable. (TDE76)
- [ ] Tool descriptions are versioned alongside the tool. (TDE79)
- [ ] Deprecated tools are removed rather than annotated. (TDE84)
- [ ] Surface size is tracked against a stated ceiling. (TDE85)
- [ ] The surface loaded for a task is limited to relevant tools. (TDE82)

## Process

- [ ] The review read the actual tool definitions, schemas, and at least one real response payload — not the descriptions alone.
- [ ] **Trace check:** the surface has been exercised by a real agent on realistic tasks, and the traces were read. (TDE77)
- [ ] Observed wrong calls were fixed at the name, description, or schema — not only by adding prompt instructions. (TDE78)
- [ ] Every tool has tests for its success shape, error shapes, enforced limit, and repeated identical call. (TDE81)
- [ ] The repeat-safety guarantee is exercised by a test that calls the tool twice. (TDE50)
- [ ] Tool-selection accuracy was measured against an evaluation set before and after any rename or description change. (TDE80)
- [ ] Before any tool was added, the request it serves that nothing existing serves was named. (TDE83)
- [ ] Any tool never selected across a representative evaluation run was examined or removed. (TDE86)
- [ ] For each granularity finding, the review names the specific split or merge — never "this tool does too much" without the alternative shape.
