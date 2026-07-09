# Examples — CI/CD Pack

## Fast-first pipeline ordering

```yaml
jobs:
  lint:       # ~10s
  typecheck:  # ~20s
  unit-test:  # ~30s
  build:      # ~2min, only after above pass
  e2e-test:   # ~5min, only after build passes
  deploy:     # only after all above pass, on main
```

## Secrets via CI secret manager, not YAML

Bad: `DEPLOY_KEY: "sk_live_abc123..."` in `.github/workflows/deploy.yml`.
Good: `DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}` referencing a value set in the CI platform's encrypted secrets store.

## One-command rollback

```bash
akos-deploy rollback --to-previous  # re-deploys the last known-good release artifact
```

## Decoupling deploy from release via feature flag

```js
if (featureFlags.isEnabled('new-checkout', user)) {
  return <NewCheckout />;
}
return <LegacyCheckout />;
```
Code deploys to production immediately; the flag controls actual user exposure, enabling gradual rollout.
