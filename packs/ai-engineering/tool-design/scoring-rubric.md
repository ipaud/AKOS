# Scoring Rubric — Tool Design Pack

Standalone 0–100 score for an agent-facing tool surface — how its tools are named, shaped, bounded, and reported. Not a dimension of the twelve-lens UI review pipeline (`core/review-pipeline.md` covers product/UX/accessibility/mobile/copy/frontend/architecture/security/performance/testing/database/release); this pack scores a different surface: what the agent reaches for, and whether reaching for it correctly is possible.

Score = 100 − deductions, floor 0. Bands per [core/scoring-model.md](../../../core/scoring-model.md).

Three classes of finding are scored as correctness defects rather than ergonomics concerns: **an unrecoverable partial effect**, **a destructive operation reachable without preview or confirmation**, and **a write returning no evidence of what it did**. All three change what the system does in the world or what the agent will claim about it; all three are graded like a wrong calculation, not like friction.

## Deductions

| Finding | Deduction |
|---------|-----------|
| One tool performs several independently-failing side effects behind one name (TDE12, TDE14) | −25 (CRITICAL) |
| Partial failure across entities collapsed into one aggregate error, leaving the caller unable to tell what landed (TDE16) | −25 (CRITICAL) |
| A destructive or irreversible operation is reachable with no confirmation parameter (TDE54) | −25 (CRITICAL) |
| An operation whose scope depends on unseen state has no dry-run mode (TDE51) | −25 (CRITICAL) |
| A write returns a bare success token with no resulting state (TDE27, TDE28) | −25 (CRITICAL) |
| Input is not validated before side effects run; an invalid call partially applies (TDE23) | −25 (CRITICAL) |
| A destructive effect is reachable through a tool whose name does not describe destruction (TDE57) | −25 (CRITICAL) |
| A side-effecting tool is silent on repeat-safety and is neither idempotent nor keyed (TDE45, TDE46) | −15 (HIGH) |
| A tool takes a discriminator parameter changing which other parameters are required (TDE10, TDE11) | −15 (HIGH) |
| A parameter carries structured content inside a string the tool parses (TDE19) | −10 each, cap −20 (HIGH) |
| A collection-returning tool enforces no default limit or no hard maximum (TDE58, TDE59) | −10 each, cap −20 (HIGH) |
| Two tools have names a caller could map to the same request (TDE2) | −10 per pair, cap −20 (HIGH) |
| Errors do not name what failed, which input caused it, or what to do next (TDE37) | −10 (HIGH) |
| A description does not state whether the call mutates state (TDE4) | −10 (HIGH) |
| Returned entities carry no stable identifier, or consuming tools do not accept it (TDE65, TDE66) | −10 (HIGH) |
| A blind overwrite that would lose information requires no version token (TDE70) | −10 (HIGH) |
| Success and failure are distinguishable only by reading a message string (TDE30) | −10 (HIGH) |
| Closed value sets documented as prose rather than declared as enums (TDE18) | −6 each, cap −18 (MEDIUM) |
| A tool name is a noun, an abbreviation, or a wrapped endpoint name (TDE1) | −6 each, cap −18 (MEDIUM) |
| Errors are unstructured, or surface a raw stack trace or database error (TDE38, TDE39) | −6 (MEDIUM) |
| Errors do not distinguish retryable from non-retryable conditions (TDE40) | −6 (MEDIUM) |
| Truncation is unmarked, or a paginated response states no total (TDE61, TDE62) | −6 (MEDIUM) |
| A dry-run response has a different shape from the real response (TDE52) | −6 (MEDIUM) |
| A confirmation parameter is a generic boolean rather than operation-specific (TDE55) | −6 (MEDIUM) |
| Mutating capabilities, readable material, and templates are all exposed as tools (TDE73) | −6 (MEDIUM) |
| Prerequisites are discoverable only by failing (TDE6) | −4 each, cap −16 (MEDIUM) |
| An invariant multi-call ritual repeated on every task is not available as one tool (TDE15) | −4 (MEDIUM) |
| Response shape varies across calls of the same tool (TDE31) | −4 (MEDIUM) |
| A parameter requires a value obtainable only by guessing (TDE26) | −4 (MEDIUM) |
| Tool names are not namespaced by provider or server (TDE7) | −4 (MEDIUM) |
| Response size capped by item count but not by bytes or tokens (TDE64) | −4 (MEDIUM) |
| Optional parameters do not document their defaults (TDE22) | −1 each, cap −5 (LOW) |
| String parameters declare no format or example (TDE20) | −1 each, cap −5 (LOW) |
| Responses carry fields the caller cannot act on (TDE33) | −1 each, cap −5 (LOW) |
| Parameter names use negation or non-universal abbreviations (TDE25) | −1 each, cap −5 (LOW) |
| A deprecated tool remains in the surface with a note (TDE84) | −1 each, cap −5 (LOW) |
| Expiring handles or cursors do not state their validity window (TDE69) | −1 (LOW) |

## Hard caps

- **Any open CRITICAL finding: score ≤ 59 (BLOCKED).** A surface that can leave an unrecoverable partial state, delete without a preview, or report a write it cannot evidence fails this dimension regardless of how well the rest of it is named and typed.
- The surface has never been exercised by a real agent, with the traces read (TDE77): cap 79. Every judgment about description quality is otherwise unverified.
- No tool has tests for its error shapes, enforced limit, and repeated identical call (TDE81): cap 79.
- Observed wrong calls are corrected in the agent's prompt rather than at the tool's name, description, or schema (TDE78): cap 69.
- No collection-returning tool in the surface enforces any bound (TDE58): cap 69.

## Modifiers

- Every tool's description states its side-effect status explicitly, whether or not the primitives are separated (TDE4, TDE75): **+3**.
- Every missing-prerequisite error names the tool that satisfies it (TDE42): **+3**.
- Repeat-safety is exercised by a test that calls each side-effecting tool twice and asserts the resulting state (TDE50): **+5**.
- Tool-selection accuracy was measured against an evaluation set before and after the last naming or description change (TDE80): **+5** (cap 100).
- Every tool's description was revised at least once against an observed wrong call (TDE78): **+3**.
- Repeat finding from a previous review, unfixed without a recorded tradeoff: **double its deduction**.

## Interpretation anchors

- **95** — names state effects, descriptions name the neighbour they are not for, inputs are typed and enumerated, writes return the resulting state, errors name the next call, every collection is bounded by the tool, destructive operations preview and confirm, and the descriptions have been revised against traces of real agent calls. Remaining findings are wording polish.
- **85** — sound and usable, with a cluster of MEDIUMs to schedule: a couple of enum sets still documented as prose, an unstructured error path, a dry run whose shape differs from the real call, one tool named for its endpoint.
- **72** — works for a careful caller and costs an incautious one: unbounded listings that happen to be small today, a surface that never states which calls mutate, prerequisites discovered by failing. Acceptable pre-production with the bounds and the mutation markers queued as real work.
- **58** — a bulk delete reachable in one call with no preview, or a four-effect tool that leaves the caller unable to tell what landed after a partial failure. BLOCKED until the operation is split or gated at the tool boundary — not until the calling agent is told to be careful, which leaves the next caller exposed.
