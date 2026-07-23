# Tests

## Unit (`tests/unit/`, Python stdlib `unittest`)

The tests themselves use stdlib `unittest`; `coverage.py` is an optional,
development-only measurement dependency and is not required to run them:

```bash
python3 -m unittest discover -s tests/unit -p 'test_*.py' -v
```

Run the command above for the exact count — CI is the source of truth. The
suite covers the YAML parser, schema validator and registry, metadata
migration, marked-section parser, Python-version-floor helper, draft-pack
routing, personal-layer integrity, executable rule detectors, freshness,
review history, markdown link integrity, CI contracts, and Review Summary
template. A recurring pattern worth naming: **every detector's test file locks
down the specific bug that detector's own construction found** — e.g.
`test_a11y_input_no_label` asserts `htmlFor` (not just `for`) is recognized,
because that was a real false-positive this session hit before shipping. A
happy-path-only assertion would not have caught it; the near-miss matters.

Notable additions: `test_marked_sections.py` includes a deliberate sabotage test — reverting the parser to "grab the first START and first END" (the exact bug it replaces) must fail at least one case. `test_pack_lifecycle_routing.py` derives its expectations by reading the real corpus's `metadata.yaml` `status` fields at test time, never a hardcoded list of draft pack names, so a future promotion/demotion can't silently make the test stale.

## Integration (`tests/integration/`, bash)

```bash
for t in tests/integration/test_*.sh; do bash "$t"; done
```

Each script uses `mktemp -d`. The E2E test also copies AKOS into that owned
temporary root before invoking commands that scaffold profiles or packs, so a
test failure cannot mutate or clean up content in the launching checkout.

- `test_marker_replace.sh` — the exact scenario that caught `write_marked_section`'s BSD-awk bug (M4): install-project twice, with a real content change in between, confirming the rerun actually updates rather than silently no-op-ing. Also covers the shared parser's adversarial guarantees end to end: `install-project` preflights all 4 managed files and refuses (writing none of them) when one has an ambiguous marker structure; `profile use` rejects a malformed `.akos/config.md` instead of treating it as absent; a project path containing spaces still works.
- `test_python_required.sh` — `install.sh`/`update.sh`/every operational `akos` subcommand refuse to run (zero mutation) without a valid Python 3.10+, simulated deterministically via `AKOS_PYTHON_BIN` pointing at a trivial fixture script (never by altering the real interpreter); `doctor.sh` reports a missing/old Python as a build failure, not a warning; `help`/`doctor` are confirmed to still work without Python; `create-pack`'s date computation fails loudly rather than silently substituting today's date; the resolved interpreter is confirmed to be the one actually used (via a logging wrapper), not a second `python3` found on PATH.
- `test_update_preserves_personal.sh` — builds a real local git remote (a bare clone of the current working tree, no network) so the git-pull-**success** branch actually executes, not just "not a git repository." Covers: a real pull that modifies a personal-layer file (restored), one that deletes a file and adds a new one (both reverted — restore is a full-tree snapshot, not a partial fill), an untracked symlink surviving unfollowed, a failing pull, a non-git checkout, a concurrent run being rejected by the lock, a simulated restore failure (via an `AKOS_PYTHON_BIN` wrapper that fails only the `restore` subcommand — no fragile fs-permission tricks, no root-avoidance assumptions) reporting failure honestly, and a broken tree failing the final `doctor.sh` gate.
- `test_install_isolated.sh` — `install.sh` against a scratch `$HOME`: the symlinks it creates, idempotence, and the no-clobber guards that leave a user's real skill dir / agent file / `~/DEV` untouched.
- `test_uninstall_isolated.sh` — `uninstall.sh` against a scratch `$HOME`: foreign files left alone, declining keeps everything, typed confirmation backs up all of `packs/` before deleting, and a failed backup aborts rather than deleting.
- `test_end_to_end_project.sh` — doctor, validate, benchmark, profile
  create/use, create-pack (`schema_version: 1` and strict validation), and
  history record/list, all through the copied checkout's real `bin/akos`; it
  uses unique fixture names and keeps every output under one owned temp root.
- `test_e2e_isolation_contract.sh` plants pre-existing historical fixture names
  in a throwaway checkout and proves the E2E harness neither collides with nor
  deletes them.
- `test_path_with_spaces.sh` — a project directory with spaces in its path; would break first on any unquoted path in `bin/akos` or the Python tooling.
- `test_doctor_self_scan.sh`, `test_gitignore_reviews.sh`, `test_version_freshness.sh` — plant a defect, assert the relevant gate fires, then assert recovery.

## Coverage

Coverage is a development-only dependency; AKOS itself remains stdlib-only:

```bash
python3 -m pip install -r requirements-dev.txt
mkdir -p .cache
coverage erase
coverage run -m unittest discover -s tests/unit -p 'test_*.py' -v
coverage run benchmarks/runners/run.py run
python3 tests/ci/run_integrations.py --coverage
coverage report
```

`.coveragerc` enables branch and Python-subprocess measurement and fails below
80%. Bash itself is covered behaviorally by the integration suite, not counted
as Python lines. The final v1.11.1/v1.12.0 remediation run is recorded in
[`docs/testing/v1.12-remediation.md`](../docs/testing/v1.12-remediation.md).

## CI

See `.github/workflows/ci.yml`: Ubuntu runs lint, structural gates and measured
coverage; a functional matrix runs unit and integration suites on Ubuntu with
the supported Python 3.10 floor and on macOS with current Python.
