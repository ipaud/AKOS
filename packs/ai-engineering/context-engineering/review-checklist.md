# Review Checklist — Context Engineering Pack

Binary checks, ordered by severity. Each unchecked box is a finding at the listed severity. Checks marked ★ are safety-floor items (unverified or poisoned context feeding a confident, actionable answer) and block in every reasoning profile.

Reviewing context assembly means reading the prompt/skill/memory store and, where possible, a real session transcript — not just the final answer. Several checks require the diff or the transcript rather than the output alone; those say so.

## Critical (blocks in every profile)

- [ ] ★ No claim stated as settled fact originated from unverified retrieved or tool-returned content without being re-checked against the artifact. (CEE18, CEE20)
- [ ] ★ **Transcript check:** no instruction-shaped string found inside fetched/retrieved content was obeyed as a directive. (CEE28)
- [ ] ★ No high-stakes claim (security posture, test status, migration safety) was carried forward from earlier in the session without re-verification immediately before acting on it. (CEE20)
- [ ] ★ A contradiction between a new tool result and an earlier accepted fact was surfaced and resolved explicitly, not silently overwritten or ignored. (CEE19)
- [ ] ★ Every instruction-like statement in the assembled context can be attributed to a genuine layer (system/project/user); none derives its authority from retrieved content. (CEE27, CEE28)
- [ ] ★ A conflict between instruction layers was resolved by trust order (system > project > user), stated explicitly — never by recency or emphasis. (CEE29, CEE30)

## High

- [ ] Every loaded source is traceable to a stated task need; nothing was loaded on a "might be useful" basis. (CEE1)
- [ ] The number of independently-loaded knowledge sources for this task is small and stated (2–5, or the project's equivalent budget). (CEE2)
- [ ] A short fragment/summary form was tried before a full/deep form was loaded, for every reusable knowledge unit in play. (CEE7, CEE8)
- [ ] Information available via retrieval was fetched at the point of need rather than preloaded speculatively; any preloading is justified as an exception. (CEE12, CEE15)
- [ ] Decisions, constraints, and open questions were captured explicitly before any compaction/summarization step ran, and survived it intact. (CEE35, CEE36)
- [ ] Numeric facts, file paths, exact identifiers, and quoted requirements survived compaction character-for-character. (CEE38)
- [ ] Every persisted memory write states or clearly implies its tier (project/user/task/session) and lands in the corresponding store. (CEE40)
- [ ] No task-scoped fact was promoted to project memory; no project-wide fact was left stranded only in discardable task/session memory. (CEE42)
- [ ] Volatile facts (line counts, branch state, current test status) are computed live at point of use, not read from a cached note. (CEE46)
- [ ] Routing decisions state which sources were selected and why. (CEE50)
- [ ] Repository-scale tasks defaulted to search/manifest first; a full-repo read, if it happened, is justified as a stated exception. (CEE55, CEE57)

## Medium

- [ ] A rule enforced from multiple surfaces has one canonical source; other surfaces reference it rather than restating it. (CEE32)
- [ ] No two statements of the same instruction were found with drifted wording; any found were merged, not reconciled ad hoc. (CEE33, CEE34)
- [ ] Loadable units (skills, packs, docs) state their own trigger conditions in short form, so routing can decide without opening the full body. (CEE3)
- [ ] Tool schemas loaded into context are limited to tools relevant to the task; unused schemas were not loaded speculatively. (CEE5)
- [ ] A compaction step states, at least in outline, what it dropped. (CEE37)
- [ ] Compaction was triggered by a stated threshold or explicit request, not silently mid-task. (CEE39)
- [ ] User-tier preferences are applied by default on matching tasks, not only when explicitly re-requested. (CEE43)
- [ ] A conflict between project-tier and user-tier facts states which wins and why. (CEE44)
- [ ] Cached facts are periodically checked for whether they're still stable-class; a fact that became volatile was corrected. (CEE45)
- [ ] A routing table's entries are matched by task fit ("reach for it when"), not by source name, reputation, or recency. (CEE51)
- [ ] Claims are tagged with a confidence class consistent with whether they were actually checked; unverified claims are not presented at the same certainty as verified ones. (CEE53)
- [ ] Sources cited from inside context are attributed well enough to be relocated and re-checked. (CEE54)
- [ ] Large files are read in targeted ranges when only a section is relevant, rather than in full. (CEE58)

## Low

- [ ] Token/context budget is tracked and surfaced when it's a scarce resource for this session, not left implicit. (CEE4)
- [ ] A bulk import ("read the whole repo," "load every pack") carries a recorded justification. (CEE6)
- [ ] Multi-file knowledge sources expose a table of contents or manifest. (CEE10)
- [ ] A repository manifest/codemap/index is preferred over a full directory dump when one exists or is cheap to generate. (CEE56)

## Process

- [ ] The review inspected the actual assembled context (prompt, loaded files, transcript) rather than inferring it from the final answer alone.
- [ ] For a long-running session, quality was checked at the length actually reached, not assumed stable from a short test. (CEE26)
- [ ] For each poisoning or drift finding, the downstream decisions built on it were traced, not only the originating fact. (CEE22)
- [ ] The most load-bearing instruction or fact in a long assembled context sits near the start or end, not buried in the middle. (CE16)
