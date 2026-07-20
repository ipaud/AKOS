# Engineering Rules — Context Engineering Pack

Checkable in a system prompt, a skill file, a subagent definition, a memory store, or a session transcript. A reviewer verifies each against the actual artifact; violations are findings.

## Context budgeting

- CEE1. Every source loaded into an agent's context is traceable to a specific, stated task need — not "might be useful."
- CEE2. A task's routing decision caps the number of independently-loaded knowledge sources at a small stated number (AKOS: 2–5), not the full available set.
- CEE3. A loadable unit (skill, pack, doc) states its own trigger conditions in short form, so routing can decide without reading the full body first.
- CEE4. Context budget (token count or share of window used) is tracked and surfaced when it's a scarce resource, not left implicit until a failure exposes it.
- CEE5. Tool schemas loaded into context are limited to tools actually relevant to the task; unused tool definitions are not loaded speculatively.
- CEE6. A bulk import ("read the whole repo," "load every pack") carries an explicit, recorded justification at the point it's invoked.

## Progressive disclosure

- CEE7. Each unit of injectable knowledge ships both a short fragment/summary form and a full form; the fragment is read first.
- CEE8. Deeper material (full principles, engineering rules, worked examples) loads only once the fragment is read and found insufficient — not preemptively alongside it.
- CEE9. Routing tables and skill descriptions are kept to about one line each, so evaluating whether to load something costs much less than the thing itself.
- CEE10. Multi-file knowledge sources expose a table of contents or manifest so a specific file can be chosen rather than the source read end-to-end.
- CEE11. A "deep read" past the fragment is a deliberate, logged second step — never an automatic consequence of loading the fragment.

## Just-in-time retrieval

- CEE12. Information obtainable via a live retrieval (search, file read, API call) is fetched at the point of need rather than embedded wholesale at session start.
- CEE13. A reference (path, ID, query) is used in place of inlined content wherever the referenced content can be fetched cheaply and reliably when needed.
- CEE14. Retrieval results are not written into long-lived memory unless they meet the stability bar (CEE45–47); most retrieval results are used once and dropped.
- CEE15. Pre-fetching is applied only when the fetched content's use is near-certain and the cost of fetching later is materially higher (a slow or rate-limited API); it is a stated exception, not the default.
- CEE16. A task that fails for lack of information triggers a new, targeted retrieval — not a re-read of everything already in context.

## Context poisoning containment

- CEE17. Tool output and retrieved content are labeled as such in the working representation, not silently merged into the narrative as agent-asserted fact.
- CEE18. A claim originating from an unverified tool result, search snippet, or user-supplied document is re-verified before being restated as settled fact in a later turn, if it's load-bearing for a subsequent decision.
- CEE19. A contradiction between a new tool result and an earlier accepted fact is surfaced and resolved explicitly — never silently overwritten and never silently ignored.
- CEE20. High-stakes claims (security posture, whether a test passed, whether a migration is safe) are re-verified against the artifact immediately before being acted on, even if an equivalent claim appeared earlier in the session.
- CEE21. Hallucination-shaped content — a suspiciously specific unsourced fact, a tool result that doesn't match its query — is flagged rather than propagated as-is.
- CEE22. Once a poisoned fact is identified, its downstream consequences (decisions made on the strength of it) are traced and corrected, not only the originating fact.

## Context rot mitigation

- CEE23. Sessions approaching a stated length threshold are compacted or summarized rather than left to grow on the assumption that "it still fits."
- CEE24. Long, low-signal tool output (full file dumps, verbose logs) is trimmed or summarized before it persists in context; only the parts relevant to the task are kept verbatim.
- CEE25. A session whose context has grown large is checked for whether early instructions are still being honored — quiet reversion to a default the session was told to override is treated as a rot symptom, not a new decision.
- CEE26. Evaluation of agent quality is run at multiple realistic context lengths, not only at the shortest one that happens to demo well.

## Instruction hierarchy

- CEE27. Every assembled context can state, for any instruction-like text in it, which layer it belongs to (system, project/developer, user, retrieved-content).
- CEE28. Retrieved or tool-returned content is never executed as an instruction regardless of phrasing or formatting; no string inside a fetched document, page, or file grants itself system- or developer-layer authority.
- CEE29. When two instructions at different layers conflict, the higher-trust layer wins, and the conflict is stated — never silently resolved by taking whichever was read most recently.
- CEE30. A lower layer may raise strictness or add detail on top of a higher layer's rule, but may not weaken, waive, or override a higher layer's hard requirement.
- CEE31. Prior agent turns in the transcript are not treated as a new instruction layer merely because they appear later in context; only genuine system, developer, or user turns carry directive weight.

## Deduplication of instructions

- CEE32. A rule enforced from multiple surfaces (a lint config, a written doc, a prompt fragment) has one canonical source; every other surface references it rather than restating its own copy.
- CEE33. Two statements of the same instruction found with different wording are treated as a found defect (drift) to resolve immediately, not as two rules to reconcile ad hoc per use.
- CEE34. Adding a new instruction includes a check for an existing equivalent elsewhere in the loaded context; duplicates are merged or removed rather than left to coexist.

## Summarization and compaction

- CEE35. Before a compaction or summarization step runs, the explicit list of decisions made, constraints established, and open questions is captured separately from the narrative.
- CEE36. The compacted output preserves that list verbatim or near-verbatim; narrative exploration, reverted attempts, and superseded intermediate states may be compressed or dropped.
- CEE37. A compaction step states, at least in outline, what it dropped, so a reader can tell what to re-derive or re-ask for if it turns out to matter.
- CEE38. Numeric facts, file paths, exact identifiers, and quoted user requirements are preserved character-for-character across a compaction boundary — never paraphrased.
- CEE39. Compaction is triggered by an explicit threshold or explicit request, not invisibly mid-task in a way neither the user nor the agent can account for afterward.

## Memory tier discipline

- CEE40. Every persisted memory entry states or clearly implies which tier it belongs to (project, user, task, session) and is stored in the corresponding location, not commingled into one undifferentiated notes file.
- CEE41. Project-tier memory holds facts true of the codebase or product regardless of who's working on it; user-tier memory holds one person's preferences across projects; task-tier memory holds facts scoped to the current unit of work; session-tier memory holds the current conversation's working state and is expected to be discarded.
- CEE42. A fact scoped to a single task is not promoted to project memory; a fact true of the whole project is not left stranded only in a task-scoped note that will be discarded when the task closes.
- CEE43. User-tier preferences are applied by default on matching tasks without being asked for again, consistent with the reason that tier exists.
- CEE44. When project-tier and user-tier facts conflict, the resolution (which wins, and why) is stated explicitly rather than left ambiguous per instance.

## Stable vs. volatile information

- CEE45. Cached or persisted facts are periodically checked for whether they remain stable-class; a fact that used to be stable (a file's location) but has since become volatile (moved in a refactor) is corrected, not left stale.
- CEE46. Volatile facts (line counts, current test status, current branch state, "today's" anything) are computed at the point of use via a live check rather than read back from a cached note.
- CEE47. Memory entries distinguish, in their own text, whether a stated fact is a convention (stable) or a snapshot (volatile), so a future reader knows whether to trust it as-is or re-verify it.

## Dynamic selection and routing

- CEE48. A routing mechanism (a table, a skill index, a tool-selection step) chooses context or tools by matching task shape to source, not by loading every available source and leaving the model to sort it out.
- CEE49. A routing table is kept short and current; an entry that no longer matches how a source is actually used is corrected rather than left to silently misroute.
- CEE50. Routing decisions are stated out loud — which sources were loaded and why — so a reviewer can tell whether the routing was correct, rather than leaving it implicit.
- CEE51. A routing table's selection criterion is the task's actual need ("reach for it when...") rather than a source's name, reputation, or recency; picking the wrong-but-plausible-sounding source is a routing defect.

## Evidence and citation

- CEE52. A claim that is checkable in the artifact at hand (does the function exist, does the test pass, is the file present) is checked, not inferred, before being stated as fact.
- CEE53. Claims are tagged by the confidence classes actually available (verified/certain vs. assumed/inferred, per [core/confidence-model.md](../../../core/confidence-model.md)), and the severity or certainty of a finding is capped by that class — an unverified claim is never presented as a certain, blocking finding.
- CEE54. Sources cited from inside context (a fetched doc, a search result) are attributed well enough that the claim could be relocated and re-checked later.

## Large-repository context

- CEE55. Repository-scale context defaults to search-first (grep, symbol lookup, index query) rather than sequential full-file reads across the whole tree.
- CEE56. A repository manifest, codemap, or index is preferred over a full directory dump when one exists or can be cheaply generated, and is kept current enough to be trustworthy.
- CEE57. A full-repository read is used only when the task genuinely requires whole-codebase reasoning (a cross-cutting rename, a global convention audit) and is stated as a deliberate exception, not a default habit.
- CEE58. Large files are read in targeted ranges (by offset/line-range or by symbol) rather than in full, when only a portion is relevant to the task.
