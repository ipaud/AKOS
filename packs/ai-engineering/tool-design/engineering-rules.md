# Engineering Rules — Tool Design Pack

Checkable in a tool definition, a JSON Schema, a response payload, a server manifest, or a call trace. A reviewer verifies each against the actual artifact; violations are findings.

## Naming and description

- TDE1. Every tool's name states its effect as a verb plus an object (`create_invoice`, `list_open_incidents`), not a bare noun, an abbreviation, or the name of the endpoint it wraps.
- TDE2. No two tools in the same surface have names a caller could reasonably map to the same request; near-synonyms are merged or renamed with a stated distinction.
- TDE3. Each description opens with what calling the tool does and to what, before any detail about how it works internally.
- TDE4. Each description states explicitly whether the call mutates state, and if so what it changes.
- TDE5. Each description names the situations the tool is *for*, and — where a neighbouring tool exists — the situation it is not for, naming that neighbour.
- TDE6. Descriptions state prerequisites (a resource that must exist, a call that must have happened first) rather than leaving the ordering to be discovered by failing.
- TDE7. Tool names are namespaced by their provider or server (`github_create_issue`, not `create_issue`) so identical concepts from different sources stay distinguishable in one surface.
- TDE8. No description relies on information the agent lacks at selection time — no reference to "the usual flow," "as configured," or documentation the agent cannot read from the call.
- TDE9. Terms used in a description match the terms in its parameter names and response fields; the same concept does not appear as `project`, `repo`, and `workspace` across one tool's own surface.

## Granularity and composition

- TDE10. No tool takes a `mode`, `action`, or `operation` discriminator that changes which other parameters are required; such a tool is split into one tool per branch.
- TDE11. No parameter is conditionally required based on another parameter's value; a schema that cannot express its own requirement rules is a split waiting to happen.
- TDE12. Each tool performs one effect describable in a single clause without "and."
- TDE13. Where a tool performs several state changes, they commit atomically as one transaction, and the response reports one outcome for the whole.
- TDE14. No tool silently performs a side effect its name and description do not mention (sending a notification, writing an audit entry, invalidating a cache, triggering a webhook).
- TDE15. A fixed multi-call ritual repeated on every task is treated as a missing tool: where the sequence is invariant and its intermediate results are of no interest to the caller, it is collapsed into one tool.
- TDE16. Partial failure within a tool touching multiple entities is reported per entity (which succeeded, which failed, why), never collapsed into one aggregate error.

## Input design

- TDE17. Every parameter has a declared type; no parameter is typed as a string when it represents a number, a boolean, a date, or a member of a closed set.
- TDE18. Closed sets of values are declared as enums in the schema, not documented as prose in the description.
- TDE19. No parameter carries structured content inside a string the tool then parses (query mini-languages, delimiter-separated lists, key-value blobs); structure is expressed as schema structure.
- TDE20. Parameters that are genuinely strings (dates, identifiers, paths) declare their expected format in the schema, with an example value.
- TDE21. Every parameter's description states what it selects or controls, rather than restating its name.
- TDE22. Required and optional parameters are distinguished in the schema, and every optional parameter's default is documented.
- TDE23. Input is validated at the boundary before any side effect runs; an invalid call fails without partially applying.
- TDE24. Validation failures name the specific parameter and the specific constraint violated, not merely that validation failed.
- TDE25. Parameter names avoid negation (`include_archived`, not `exclude_active`) and avoid abbreviations that are not universal in the domain.
- TDE26. No parameter requires a value the caller could only obtain by guessing — internal IDs with no discovery tool, magic numbers, encoded flags.

## Output and evidence

- TDE27. A successful response returns the resulting state, not a status token: the created or modified entity, its identifier, and the fields that changed.
- TDE28. A response to a write returns enough for the caller to verify the effect matched the intent without a second call.
- TDE29. Operations affecting multiple entities return the count affected and the identifiers, not just a success indicator.
- TDE30. Success and failure are distinguishable structurally (a status field, a distinct response type), never only by reading prose in a message string.
- TDE31. Response shapes are stable across calls of the same tool; a field does not change type or vanish based on the values in the result.
- TDE32. Response field names are self-describing at the point of reading — a caller holding only the response can tell what each field means without re-reading the tool definition.
- TDE33. Responses omit fields the caller cannot act on (internal timestamps, storage keys, framework envelopes) rather than padding the payload with them.
- TDE34. Where a tool returns content that may be large, the response states the total size or count alongside the content, so the caller can tell what it is holding.
- TDE35. A tool returning nothing meaningful on success is treated as a design finding to fix, not a documented feature.
- TDE36. Timestamps, IDs, and enumerated values are returned in the same format the tool's own inputs accept, so a response value can be fed back in without transformation.

## Errors

- TDE37. Every error response names what failed, which input (if any) caused it, and what the caller should do next.
- TDE38. Error responses are structured — a stable code, a message, and where relevant the offending field — not a bare string or a raw exception.
- TDE39. No error surfaces an unmodified stack trace, framework exception, or database error text to the caller.
- TDE40. Errors distinguish retryable conditions (rate limit, timeout, transient upstream failure) from non-retryable ones (invalid input, missing permission, absent resource), and say which they are.
- TDE41. An error caused by a malformed argument suggests a valid form — an example value, the allowed enum members, or the expected pattern.
- TDE42. An error caused by a missing prerequisite names the tool that satisfies the prerequisite.
- TDE43. A failed call does not return the success response type with an embedded failure message.
- TDE44. Error codes are stable identifiers a caller can branch on, not message text subject to rewording.

## Repeat-safety

- TDE45. Every side-effecting tool documents, in its description, whether calling it twice with identical arguments is safe.
- TDE46. Tools that are not naturally idempotent accept an idempotency key, and a repeated call with the same key returns the original result rather than performing the effect again.
- TDE47. Idempotency keys are accepted as an explicit parameter or header, not derived from a payload hash the caller cannot control.
- TDE48. A tool whose repeated call is genuinely unsafe and cannot be made safe states that plainly, so a caller can gate it rather than retry it.
- TDE49. Read-only tools are documented as read-only, so a caller can retry them freely without reasoning about consequences.
- TDE50. The repeat-safety guarantee is covered by a test that calls the tool twice with identical arguments and asserts the resulting state.

## Consequential and destructive operations

- TDE51. Any operation whose scope depends on its arguments (a filtered update, a bulk delete, a recursive change) exposes a preview or dry-run mode.
- TDE52. A dry-run response has the same shape as the real response, so a caller can compare intent to effect without a second interpretation step.
- TDE53. A dry-run reports the count and identity of what would be affected, not a summary sentence.
- TDE54. Destructive and irreversible operations require an explicit confirmation parameter with no default, which the caller must set for the call to proceed.
- TDE55. The confirmation parameter is specific to the operation — naming the target, the count, or the scope — not a generic boolean a caller can set reflexively.
- TDE56. Destructive operations state their reversibility in the description: a soft delete, a recoverable state, or permanent loss.
- TDE57. No destructive effect is reachable through a tool whose name does not describe destruction.

## Bounded results

- TDE58. Every tool that can return a collection enforces a default result limit at the tool, independent of any limit the caller supplies.
- TDE59. Every such tool enforces a hard maximum that a caller-supplied limit cannot exceed.
- TDE60. Paginated responses return a cursor or continuation token; offset-derived page numbers are not used where the underlying set can change between calls.
- TDE61. Paginated responses state the total count, or explicitly state that a total is unavailable, so the caller knows the size of what it did not receive.
- TDE62. Truncated responses say so in a structured field, not by the absence of further results.
- TDE63. Tools returning file or document content support a range, offset, or section selector so a caller can read part of a large item.
- TDE64. Response size is capped in bytes or tokens as well as in item count, so a small number of large items cannot exceed the bound.

## Stable references

- TDE65. Every entity returned by a tool carries a stable identifier that remains valid across calls.
- TDE66. Tools acting on an entity accept that entity's identifier directly, without requiring the caller to supply a path, a name, or a position instead.
- TDE67. Identifiers returned by one tool are accepted verbatim by the tools that consume them; no reformatting, prefixing, or extraction is required of the caller.
- TDE68. Where an entity has both a stable identifier and a human-readable name, both are returned, and the tools acting on it accept the identifier.
- TDE69. Cursors, handles, and session tokens returned to a caller state their validity window in the description if they expire.

## Read-before-write in the surface

- TDE70. Where a blind overwrite would lose information, the write tool requires a version, etag, or content hash obtained from a prior read.
- TDE71. A stale version token is rejected with an error stating that the resource changed and naming the read tool to re-fetch it.
- TDE72. Where reading first is advisable but not enforced, the write tool's own description says so and names the read tool.

## Primitive separation

- TDE73. Capabilities that mutate state are exposed as tools, readable material as resources, and reusable parameterized templates as prompts — each in its own primitive rather than all as tools.
- TDE74. No read-only context is exposed as a tool solely because tools were the easiest primitive to reach for.
- TDE75. Where a surface cannot separate the primitives, every tool's description states unambiguously whether calling it is free of side effects.
- TDE76. Resource identifiers are stable and re-fetchable; a resource reference handed to a caller can be resolved again later.

## Iteration and evaluation

- TDE77. Every tool has been exercised by a real agent against realistic tasks before being considered finished, and the resulting call traces were read.
- TDE78. Observed wrong calls (wrong tool selected, parameter filled with the wrong kind of value, prerequisite missed) are addressed by changing the name, description, or schema — not only by adding instructions to the agent's prompt.
- TDE79. Tool descriptions are versioned alongside the tool, so a description change is reviewable as a change to the interface.
- TDE80. An evaluation set of realistic tasks exists for the surface, and tool-selection accuracy against it is measured before and after any change to a tool's name or description.
- TDE81. Every tool has tests covering its success shape, its error shapes, its enforced limit, and its behavior on a repeated identical call.

## Surface hygiene

- TDE82. The tool surface loaded for a task is limited to tools relevant to that task; the full catalogue is not loaded speculatively.
- TDE83. Before a tool is added, the request it serves that no existing tool serves is named; overlapping capability is merged into an existing tool instead.
- TDE84. Deprecated tools are removed from the surface rather than left in place carrying a deprecation note in the description.
- TDE85. The number of tools in a surface is a tracked quantity with a stated ceiling, not an unbounded catalogue.
- TDE86. A tool never selected by an agent across a representative evaluation run is examined for a naming or description defect, or removed.
