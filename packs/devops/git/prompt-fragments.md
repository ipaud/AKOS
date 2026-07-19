# Prompt Fragments — Git Pack

Copy-paste blocks for injecting this pack into agent prompts.

## Fragment: build-mode constraint block

```text
Apply git hygiene (AKOS L2):
- One logical change per commit. A commit mixing a feature with an
  unrelated formatting pass gets split before it is pushed.
- Each commit leaves the tree working, so history stays bisectable and
  individual commits stay revertable.
- Subject format `<type>: <description>` using feat, fix, refactor, docs,
  test, chore, perf, ci. Imperative mood, no trailing period.
- The body explains why when the reason is not obvious — the diff already
  states what. Never ship "wip", "fix", "misc", or "updates".
- Secrets never enter history. Configure .gitignore for env files,
  credential paths, build artifacts, and dependencies before the first
  commit; a later removal commit removes nothing from history.
- Feature branches live days, not weeks. Rebase or merge from main
  frequently instead of absorbing one large conflict at integration.
- Never force-push a shared or protected branch. On personal branches use
  --force-with-lease, and check whether anyone has pulled it first.
- Merge strategy is documented once and applied consistently across the
  repo; default to squash-merge for feature branches into main.
```

## Fragment: review lens

```text
Review this branch's history as a git reviewer:
1. Atomicity — does any commit combine unrelated concerns? Name the
   commit and the split it needs.
2. Messages — valid type prefix and specific description on every
   subject? Any "wip"/"fix"? Any commit whose why is missing and not
   inferable from the diff?
3. Secrets — scan the full diff range for keys, tokens, passwords,
   private keys, .env files. Any hit is CRITICAL and forces rotation.
4. Ignore rules — are build artifacts, dependencies, or local config
   tracked that .gitignore should have excluded from the start?
5. Branch age and drift — commits behind main, size of the conflict
   surface, whether this should have been integrated sooner.
6. History rewrites — any force-push to a shared branch?
7. Merge strategy — consistent with the repo's documented convention?
Report by severity, each finding naming the exact commit SHA and the
corrective command.
```

## Fragment: commit-shaping pass

```text
Rewrite this working tree into clean commits:
- Group the diff by logical change; each group becomes one commit that
  builds and passes tests on its own.
- Stage per-hunk where a single file spans two concerns.
- Keep refactors in their own commits, separate from behavior changes.
- Write each subject as `<type>: <description>` under ~72 characters,
  with a body only where the why is non-obvious (constraint encountered,
  alternative rejected, bug being reproduced).
Output: the ordered commit list with subject and one-clause rationale,
then the commands to produce it.
```

## Fragment: committed-secret response

```text
A secret reached git history. Respond in this order:
1. Rotate the credential now. Treat it as compromised the moment it was
   pushed, including to a private repo. Rotation is the fix.
2. Check access logs for use of the exposed credential.
3. Purge it from history with git filter-repo or BFG — this is cleanup,
   not remediation, and only matters after rotation.
4. Coordinate the rewrite: every collaborator re-clones or resets.
5. Add the path to .gitignore and add a pre-commit secret scan so the
   same class of leak cannot recur.
Never treat a "remove secret" follow-up commit as a fix.
```

## One-liner (for tight token budgets)

```text
Git: atomic, bisectable commits with one logical change each; `type:
description` subjects with the why in the body, never "wip"; no secrets
in history — rotate first if leaked, rewriting is only cleanup;
.gitignore before the first commit; short-lived branches rebased from
main often; no force-push to shared branches and --force-with-lease
elsewhere; one consistent merge strategy.
```
