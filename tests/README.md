# Tests

## Unit (`tests/unit/`, Python stdlib `unittest`)

No pytest, no new dependency — matches this project's own constraint (`python3` is the one accepted external tool). Run:

```bash
python3 -m unittest discover -s tests/unit -p 'test_*.py' -v
```

Roughly 200 tests (run the command above for the exact count — CI is the source of truth) across the YAML parser, the schema validator, the metadata migration, all 8 rule detectors, freshness banding, review history, markdown link integrity, and the Review Summary template. A recurring pattern worth naming: **every detector's test file locks down the specific bug that detector's own construction found** — e.g. `test_a11y_input_no_label` asserts `htmlFor` (not just `for`) is recognized, because that was a real false-positive this session hit before shipping. A test that only asserts the happy path wouldn't have caught any of these; the near-miss case is the one that matters.

## Integration (`tests/integration/`, bash)

```bash
for t in tests/integration/test_*.sh; do bash "$t"; done
```

Each script uses `mktemp -d` and never writes outside it — except `test_end_to_end_project.sh`, which necessarily calls `akos profile create` (there is no "scratch AKOS repo" mode for that command) and cleans up via a `trap` on any exit path, not just success.

- `test_marker_replace.sh` — the exact scenario that caught `write_marked_section`'s BSD-awk bug (M4): install-project twice, with a real content change in between, confirming the rerun actually updates rather than silently no-op-ing.
- `test_update_preserves_personal.sh` — `update.sh` against a scratch copy, confirming `packs/personal/` survives and a durable backup lands under `~/.akos-backups/`.
- `test_install_isolated.sh` — `install.sh` against a scratch `$HOME`: the symlinks it creates, idempotence, and the no-clobber guards that leave a user's real skill dir / agent file / `~/DEV` untouched.
- `test_uninstall_isolated.sh` — `uninstall.sh` against a scratch `$HOME`: foreign files left alone, declining keeps everything, typed confirmation backs up all of `packs/` before deleting, and a failed backup aborts rather than deleting.
- `test_end_to_end_project.sh` — doctor, validate, benchmark, profile create/use, history record/list, all invoked for real through `bin/akos` in one run.
- `test_path_with_spaces.sh` — a project directory with spaces in its path; would break first on any unquoted path in `bin/akos` or the Python tooling.
- `test_doctor_self_scan.sh`, `test_gitignore_reviews.sh`, `test_version_freshness.sh` — plant a defect, assert the relevant gate fires, then assert recovery.

## Both run in CI

See `.github/workflows/ci.yml` — unit tests via `unittest discover`, integration tests by iterating `tests/integration/test_*.sh`.
