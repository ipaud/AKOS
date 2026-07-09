# Engineering Rules — Git Pack

- GT-E1. Commit messages follow `<type>: <description>` format (feat/fix/refactor/docs/test/chore/perf/ci), with a body explaining why when the reason isn't obvious.
- GT-E2. No commit mixes unrelated changes (e.g. a feature + an unrelated formatting pass) without justification.
- GT-E3. Secrets/credentials are never committed; `.gitignore` covers env files and credential paths from project start.
- GT-E4. Force-push (`--force`) is never used on shared/main branches; `--force-with-lease` preferred on personal branches to avoid clobbering others' pushes.
- GT-E5. Merge strategy is documented and consistent (e.g. squash-merge for feature branches into main).
- GT-E6. `.gitignore` is configured before the first commit of build artifacts/dependencies/local config.
