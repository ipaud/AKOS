# Examples — Git Pack

## Good commit message

```
fix: prevent double-charge on rapid checkout button clicks

Stripe webhook could fire before the client-side disable state applied,
causing duplicate charges under fast double-clicks. Added idempotency
key on the charge request tied to the cart session.
```

## Bad commit message

```
fix stuff
```

## Splitting a mixed commit

Before: one commit with a new feature + an unrelated linter-driven reformat of 20 files.
After: `feat: add CSV export` (feature only) + `chore: apply eslint --fix to legacy files` (separate, reviewable independently).

## Secret exposure response

```bash
# 1. Rotate the secret immediately (new API key issued, old one revoked)
# 2. Clean history (secondary, not the fix)
git filter-repo --path .env --invert-paths
git push --force-with-lease  # coordinated with team, on a branch nobody else has
```
