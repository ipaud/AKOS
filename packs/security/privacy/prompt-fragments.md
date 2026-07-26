# Prompt Fragments — Privacy Pack

Copy-paste blocks for injecting this pack into an agent prompt. Read this file first — in
most tasks the build-mode block is all that needs to be loaded.

## Fragment: build-mode constraint block

```text
PRIVACY CONSTRAINTS (applies from the first real person's data, in every profile):

Before adding a field
- Name the purpose and the lawful basis. "Might be useful later" is a rejection.
- Record it in the data inventory: purpose, basis, retention, destination systems.
- Prefer not storing it. Prefer less precision. Prefer a pseudonym over a name.

Schema and defaults
- Personal data tables get row-level security at creation, not later.
- Analytics and telemetry are pseudonymous unless a stated purpose needs the join.
- Logs and error reports carry no credentials, tokens, or personal data beyond a
  pseudonymous identifier.
- The privacy-preserving option is the shipped default. No opt-out tracking, no
  public-by-default profiles.

Consent (only where consent is the chosen basis)
- Unticked by default, granular per purpose, reject as easy as accept.
- Store scope + wording version + timestamp + method, not a boolean.
- Withdrawal stops the processing downstream, not just the flag.
- Nothing non-essential loads or is stored client-side before the answer.

Lifecycle
- Every category has a retention period enforced by a job/TTL/partition drop, with a test.
- Deletion covers every destination in the inventory: child tables, storage objects, auth
  records, search index, warehouse, and third-party systems.
- Backups are bounded, and re-applying a deletion after a restore is documented.

Third parties
- Every external destination is a processor decision reviewed before the first send —
  SDKs, tag managers, session recorders, and model APIs included.
- Send the minimum that processor needs, not the full record because the API accepted it.

Non-production
- Synthetic or irreversibly anonymized data. Never a production copy.
```

## Fragment: review lens

```text
Review this surface against the AKOS privacy pack (security/privacy).

Report findings by severity, each citing its rule code (PR1–PR49). Treat as CRITICAL:
personal data reachable without access control, a live purpose with no lawful basis, a
deletion feature that leaves copies behind, consent stored as a bare boolean, withdrawal
that doesn't stop processing, no inventory at all, personal data sent to an unassessed
third party, and production data in a non-production environment.

For each finding give: the rule code, the file and line, what personal data is exposed and
to whom, and the smallest fix. Where a claim is made to users (a deletion button, a
retention statement, a privacy notice), verify the mechanism exists — a claim without a
mechanism is a defect, not a gap.

State which starred rules you could not check and why.
```

## Fragment: new-field intake

```text
Before this field is added, answer:

1. What decision or feature breaks without it?
2. What is the lawful basis, and was it chosen before now?
3. How long does it live, and what mechanism deletes it?
4. Which systems will it reach — including logs, analytics, backups, and vendors?
5. Could a pseudonym, a coarser value, or a derived flag serve instead?
6. When a user asks for erasure, what code path removes it from every place in (4)?

If (1) has no answer, stop — the field doesn't ship.
```

## One-liner (for tight token budgets)

```text
Privacy floor: don't collect what no decision needs; every personal field has a purpose,
lawful basis, retention mechanism and inventory entry; RLS at table creation; telemetry
and logs pseudonymous; privacy-preserving defaults; consent unticked, granular, reject as
easy as accept, withdrawal actually stops processing; retention enforced by a tested job;
deletion covers every destination including vendors and storage; every third party is a
reviewed processor including model APIs; synthetic data outside production; breach runbook
before launch.
```
