# Examples — Agent Foundations Pack

Invented cases. Bad → good, with the rule applied. All scenarios are fabricated for calibration.

## The agent that should have been a router plus a workflow (AF1, AF3, AFE5)

A support-inbox system is built as an agent: a loop, six tools, and a prompt describing how to triage incoming messages, look up the customer, check order status, draft a reply, and decide whether to send or hold. Each run takes eleven to thirty model calls, costs vary by an order of magnitude between messages, and two support engineers have separately reported that it "sometimes forgets to check the order before replying."

Twenty real messages are logged and their needed step sequences written out. They collapse into three: *password reset* (look up account → send reset link), *order status* (look up customer → look up order → draft status reply), and *everything else* (draft an acknowledgment → route to a human queue). Three sequences, stable, no fourth appeared in a further eighty messages.

After: a classifier at the front assigns one of the three classes, with an explicit fallback to *everything else* for anything below a stated confidence. Each class is a fixed workflow whose steps are code, with model calls where language work is genuinely needed (drafting the reply). The order lookup can no longer be skipped, because it is an edge in the graph rather than an instruction in a prompt. Cost per message became predictable, each step became independently testable, and the intermittent skipped-lookup defect disappeared as a category rather than being patched.

## Silent truncation returning a confident answer (AF13, AFE46–AFE47)

A research agent is asked to compile a competitive summary across eight named products. Its iteration cap is twenty; the run hits it after covering five products, and the harness returns the accumulated draft. The draft reads as a finished document — an introduction, five well-structured sections, a closing paragraph the model wrote at turn nineteen out of habit rather than completion. Nothing in the return value indicates that three products were never examined.

The document goes into a slide deck. The gap is noticed in the meeting.

After: the run returns a structured outcome rather than a bare string.

```
{ status: "exhausted",
  limit_hit: "max_iterations",
  completed: ["A", "B", "C", "D", "E"],
  not_started: ["F", "G", "H"],
  partial_result: <draft> }
```

The caller branches on `status` before touching `partial_result`. The cap didn't change; what changed is that hitting it is now a reported result rather than an invisible one. Note the shape of the fix: the bug was never the limit, it was that exhaustion and success were the same return type.

## The deterministic retry spiral (AF14, AFE51, AFE53)

A data-reconciliation agent calls an internal endpoint with a filter parameter the API renamed two releases ago. The call returns `400 unknown parameter: since_date`. The agent's error handler is a generic retry with exponential backoff, cap of eight. It retries eight times over four minutes, each time constructing the identical request, each time receiving the identical 400. The run then reports a timeout, and the trace shows the entire token budget consumed by a single step that could never have succeeded.

After: failures are classified before a response is chosen. A 400 with an identical request signature to the previous attempt is approach-level, not transient — it is routed to a replan, which reads the endpoint's current schema, discovers the parameter is now `updated_after`, and reconstructs the call. The retry path is reserved for 429s, 5xxs, and timeouts, with a cap of three. The distinguishing rule is mechanical and worth stating plainly: **identical request in, identical error out, twice → never a third retry.**

## Sectioning misapplied to dependent work (AF7, AFE16)

A migration agent is asked to update forty configuration files. To cut latency, the harness fans out forty workers, one per file. Each worker reads the shared `defaults.yaml`, computes its file's new values, and — because eleven of the forty files are supposed to also register themselves in `defaults.yaml` — writes back to it.

Eleven workers read `defaults.yaml` at roughly the same moment, each computes an update against the version it read, and each writes. Nine registrations are lost. Every individual worker succeeded; the aggregate is quietly wrong, and nothing failed loudly enough to notice.

After: the forty files are partitioned into the twenty-nine that only read shared state (genuinely independent — fan them out) and the eleven that write it (serialized through a single step that applies all registrations in one atomic update). The latency win is smaller and real. The rule applied is narrow and checkable: a fan-out's branches may share reads, never writes.

## The self-approving evaluator (AF9, AFE27–AFE28)

A documentation agent generates an API reference page, then passes it to an evaluator with the instruction "review this documentation and suggest improvements; approve when it is high quality." The evaluator — same model, same context, same understanding of the API — approves on iteration two, having suggested one wording change on iteration one. The published page documents a parameter that was removed in the current version, which both the generator and the evaluator believed still existed.

After: the criteria are written before the first generation, and one of them is external:

1. Every parameter documented appears in the current OpenAPI schema, and every required parameter in the schema is documented. *(Checked by a script against the schema, not by the model.)*
2. Every code sample parses and runs against the staging endpoint, returning a 2xx.
3. Each endpoint section contains a description, parameters, at least one example, and the error responses.

Criterion 1 fails on iteration one and names the specific parameter. The loop now has a ceiling set by the criteria rather than by the evaluator's satisfaction, and it exits on the criteria passing, on the cap of three, or on an iteration that fails to improve the score — whichever comes first.

## The double-charged retry (AF16, AFE63–AFE68)

An expense agent is authorized to issue small reimbursements. It calls `POST /payments`, which takes 31 seconds; the agent's HTTP client times out at 30 and raises. The retry handler fires, issues a fresh `POST /payments` with the same body, and this one returns in 2 seconds. Two payments were issued. The trace shows one, because the first call's response never arrived.

After: three changes, all of them small.

1. `POST /payments` accepts an `Idempotency-Key` header; the agent generates one per logical reimbursement, derived from the expense record's ID, not per attempt.
2. The retry path reuses that key, so the second call is recognized as the same logical action and returns the original payment rather than creating a second.
3. Before any retry of a timed-out side-effecting call, the recovery path queries the payment's state by key rather than assuming the timeout meant failure.

The generalizable rule: a timeout tells you nothing arrived back, not that nothing happened.

## The plan that outlived its premise (AF10, AFE33–AFE34)

A refactoring agent plans six steps, the first of which is "extract the shared validation logic from `OrderValidator` into a new module." At step 1 it discovers `OrderValidator` was already split in a previous refactor and its validation logic now lives in three separate classes with slightly different rules. The agent notes this, does its best to extract *something* from the largest of the three, and proceeds to steps 2 through 6 — each of which imports the module it just created, on the assumption that it contains all the validation logic. It does not. The run completes. Tests pass, because the tests exercise the largest class's paths.

After: the plan is declared revisable, with an explicit trigger list, one entry of which is *a named entity in the plan does not exist in the form the plan assumed*. Step 1's discovery fires that trigger. The agent replans against the actual three-class structure, keeps nothing (no steps had completed), and states in the trace what invalidated the original plan. Replans are capped at three; a fourth would escalate rather than produce plan five.

## Escalation conditions written down, and the boundary they draw (AF15, AFE57–AFE61)

A deployment agent is given tools that can run migrations, restart services, and roll back releases. Nobody writes an authority boundary. Asked to "fix the failing health check on staging," it diagnoses a schema drift and runs a migration that drops a column. On staging this is recoverable. The same agent is later pointed at production.

After, written into the agent's specification next to its success condition and its limits:

**May act alone:** read logs, query metrics, restart a service, roll back to the previous release, run any read-only diagnostic.

**Must confirm first:** run any migration; any operation touching production data; any action on more than one service at once; any spend above the stated per-incident cap.

**Never:** drop or truncate a table; modify access controls; disable monitoring or alerting.

**Escalates automatically:** the request is ambiguous about which environment; the same remediation has failed twice; a limit fired with the incident unresolved.

The escalation message that follows a confirmation gate carries what was attempted, what blocked it, the options, and a recommendation — so the on-call engineer decides in one round trip rather than three:

```
Blocked: migration required (adds `orders.settled_at`, no data loss).
Attempted: restart (no effect), rollback to v4.2 (health check still failing).
Cause: staging schema is one migration behind the deployed build.
Options: (a) apply migration 0142 — recommended, additive, reversible;
         (b) roll back to v4.1, which predates the column requirement;
         (c) hand over to me for manual inspection.
```

## Budget as an input rather than a cap (AF17, AFE45)

An autocomplete feature is specified as "suggest the next line as the user types." An agent is built for it: a loop that reads surrounding context, searches the codebase for similar patterns, and refines its suggestion against what it finds. In evaluation the suggestions are excellent. In use they arrive four to nine seconds after the user has moved on, and the team's response is to cap the loop at one iteration — producing a slow single call that is worse than the non-agentic version would have been, and now carries the agent's machinery for nothing.

After: the envelope is stated first — a P95 of 300ms and roughly 2,000 tokens per keystroke burst — and shapes are eliminated against it before design. A loop is inadmissible: even one iteration plus a tool call cannot fit. What fits is a single call with locally-assembled context. The retrieval that the agent was doing dynamically moves to a background index refreshed on save, so the single call gets good context without paying for a search at keystroke time. Same underlying insight — similar code in the repo improves the suggestion — implemented in a shape the envelope admits.

## Orchestrator-worker where it is genuinely earned (AF8, AFE21–AFE26)

Contrast two jobs that superficially resemble each other.

**Not earned:** "Generate the monthly report" — always six sections, always the same six data sources, always the same order. An orchestrator that decomposes this produces the identical six-item subtask list every month, at the cost of a model call and the risk that one month it produces five. This is a workflow. Write the six steps down.

**Earned:** "Audit this pull request." The subtasks depend entirely on the diff: a PR touching three React components, a migration, and a CI config needs a component review, a schema-change review, and a pipeline review; a PR touching one README needs one. The count and nature of the subtasks are a function of the input, and no fixed decomposition covers both cases without being wrong for one of them.

For the earned case, the bounds still apply: workers capped at eight and depth capped at one (workers cannot spawn workers), each worker briefed with just its own files and its own token budget drawn from the run's envelope, each worker returning a typed result the orchestrator handles explicitly, and a synthesis step with its own success condition — *every worker's findings appear in the output, ranked by severity, with duplicates merged* — rather than a concatenation of eight reports.
