import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "helpers"))
import paths  # noqa: F401,E402

import history  # noqa: E402

# Assembled at runtime so this file's own source carries no detectable
# credential literal — the repo self-scan stays clean without a path exception
# (P0-4). Still matches AKIA[0-9A-Z]{16} once built.
AWS_KEY = "AKIA" + "ABCDEFGHIJKLMNOP"


class TestGitInfo(unittest.TestCase):
    """Locks down the real bug: `git rev-parse HEAD` on a repo with zero
    commits exits 128 but still echoes the literal string "HEAD" to stdout
    — checking stdout alone recorded that as a plausible-looking commit."""

    def test_commitless_repo_has_no_commit(self):
        with tempfile.TemporaryDirectory() as d:
            subprocess.run(["git", "init", "-q"], cwd=d, check=True)
            info = history.git_info(Path(d))
            self.assertIsNone(info["commit"], "a repo with zero commits must report commit: None, not the literal 'HEAD'")

    def test_real_commit_reports_a_real_sha(self):
        with tempfile.TemporaryDirectory() as d:
            subprocess.run(["git", "init", "-q"], cwd=d, check=True)
            (Path(d) / "f.txt").write_text("x")
            subprocess.run(["git", "add", "-A"], cwd=d, check=True)
            subprocess.run(["git", "-c", "user.email=t@t.com", "-c", "user.name=t", "commit", "-q", "-m", "init"], cwd=d, check=True)
            info = history.git_info(Path(d))
            self.assertIsNotNone(info["commit"])
            self.assertEqual(len(info["commit"]), 40)

    def test_non_git_directory_reports_none(self):
        with tempfile.TemporaryDirectory() as d:
            info = history.git_info(Path(d))
            self.assertIsNone(info["commit"])


class TestRecordListShowCompare(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.project = Path(self._tmp.name)
        self.report = self.project / "report.md"
        self.report.write_text("# Review\n")

    def tearDown(self):
        self._tmp.cleanup()

    def _record(self, decision: str, scores: dict, ts: str) -> str:
        class Args:
            pass
        a = Args()
        a.dir = str(self.project)
        a.type = "ux-review"
        a.decision = decision
        a.profile = "Startup MVP"
        a.report = str(self.report)
        a.scores_json = json.dumps(scores)
        a.packs_json = None
        a.timestamp = ts
        before = set((self.project / ".akos/reviews").glob("*")) if (self.project / ".akos/reviews").exists() else set()
        self.assertEqual(history.cmd_record(a), 0)
        after = set((self.project / ".akos/reviews").glob(f"{ts}-ux-review-*"))
        new = sorted(after - before)
        self.assertEqual(len(new), 1, "one record should create exactly one review dir")
        return new[0].name

    def test_record_creates_expected_files(self):
        review_id = self._record("BLOCKED", {"ux": 50}, "20260101T000000Z")
        out_dir = self.project / ".akos/reviews" / review_id
        self.assertTrue((out_dir / "report.md").exists())
        self.assertTrue((out_dir / "report.json").exists())
        self.assertTrue((out_dir / "metadata.json").exists())

    def test_compare_reports_correct_decision_transition_and_score_delta(self):
        id_a = self._record("BLOCKED", {"ux": 50, "accessibility": 60}, "20260101T000000Z")
        id_b = self._record("PASS WITH FIXES", {"ux": 78, "accessibility": 80}, "20260102T000000Z")

        import io
        from contextlib import redirect_stdout

        class Args:
            pass
        a = Args()
        a.dir = str(self.project)
        a.review_a = id_a
        a.review_b = id_b

        buf = io.StringIO()
        with redirect_stdout(buf):
            history.cmd_compare(a)
        result = json.loads(buf.getvalue())

        self.assertEqual(result["decision_change"], "BLOCKED -> PASS WITH FIXES")
        self.assertEqual(result["score_deltas"]["ux"]["delta"], 28)
        self.assertEqual(result["score_deltas"]["accessibility"]["delta"], 20)

    def test_clean_keeps_only_the_requested_count(self):
        for i in range(5):
            self._record("PASS", {}, f"2026010{i+1}T000000Z")

        class Args:
            pass
        a = Args()
        a.dir = str(self.project)
        a.keep = 2
        # clean now refuses unless the caller confirms the exact count it
        # would delete — see TestCleanRequiresConfirmation for why.
        a.dry_run = False
        a.confirm_delete = 3
        self.assertEqual(history.cmd_clean(a), 0)

        remaining = list((self.project / ".akos/reviews").iterdir())
        self.assertEqual(len(remaining), 2)


if __name__ == "__main__":
    unittest.main()


class TestRecordDoesNotPartiallyApply(unittest.TestCase):
    """A malformed --scores-json used to throw between two writes, leaving a
    review directory with report.md but no metadata.json. `history list`
    skips such directories, so the orphan was invisible, and every retry
    minted a fresh timestamp — so they accumulated silently. The caller
    assembling that JSON is an LLM following skills/akos-review, which makes
    a malformed brace the expected failure rather than an edge case."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.project = Path(self._tmp.name)
        self.report = self.project / "report.md"
        self.report.write_text("# Review\n")

    def tearDown(self):
        self._tmp.cleanup()

    def _args(self, scores_json, packs_json=None):
        class Args:
            pass
        a = Args()
        a.dir = str(self.project)
        a.type = "ux-review"
        a.decision = "PASS"
        a.profile = "Startup MVP"
        a.report = str(self.report)
        a.scores_json = scores_json
        a.packs_json = packs_json
        a.timestamp = "20260101T000000Z"
        return a

    def _review_dirs(self):
        d = self.project / ".akos/reviews"
        return sorted(p.name for p in d.iterdir()) if d.exists() else []

    def test_malformed_scores_json_returns_1(self):
        self.assertEqual(history.cmd_record(self._args('{"ux": 72,}')), 1)

    def test_malformed_scores_json_writes_nothing_at_all(self):
        history.cmd_record(self._args('{"ux": 72,}'))
        self.assertEqual(self._review_dirs(), [],
                         "a rejected record must leave no directory behind")

    def test_malformed_packs_json_writes_nothing_at_all(self):
        history.cmd_record(self._args('{"ux": 72}', packs_json="[not json"))
        self.assertEqual(self._review_dirs(), [])

    def test_valid_json_still_records(self):
        self.assertEqual(history.cmd_record(self._args('{"ux": 72}')), 0)
        dirs = self._review_dirs()
        self.assertEqual(len(dirs), 1)
        self.assertTrue(dirs[0].startswith("20260101T000000Z-ux-review-"),
                        f"unexpected review id shape: {dirs[0]}")


class TestCleanRequiresConfirmation(unittest.TestCase):
    """`history clean` deleted with no confirmation and no preview, and
    --keep defaulted to 20 — so a bare call removed however many reviews
    happened to exist past 20, a count the caller had never seen.
    .akos/reviews/ is usually untracked, so that is unrecoverable."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.project = Path(self._tmp.name)
        report = self.project / "report.md"
        report.write_text("# Review\n")
        for i in range(1, 6):
            class Args:
                pass
            a = Args()
            a.dir = str(self.project)
            a.type = "ux-review"
            a.decision = "PASS"
            a.profile = "Startup MVP"
            a.report = str(report)
            a.scores_json = '{"ux": 70}'
            a.packs_json = None
            a.timestamp = f"2026010{i}T000000Z"
            history.cmd_record(a)

    def tearDown(self):
        self._tmp.cleanup()

    def _clean(self, keep, dry_run=False, confirm=None):
        class Args:
            pass
        a = Args()
        a.dir = str(self.project)
        a.keep = keep
        a.dry_run = dry_run
        a.confirm_delete = confirm
        return history.cmd_clean(a)

    def _count(self):
        return len(list((self.project / ".akos/reviews").iterdir()))

    def test_without_confirmation_refuses_and_deletes_nothing(self):
        self.assertEqual(self._clean(keep=1), 1)
        self.assertEqual(self._count(), 5)

    def test_dry_run_deletes_nothing(self):
        self.assertEqual(self._clean(keep=1, dry_run=True), 0)
        self.assertEqual(self._count(), 5)

    def test_wrong_confirmation_count_refuses(self):
        self.assertEqual(self._clean(keep=1, confirm=99), 1)
        self.assertEqual(self._count(), 5)

    def test_matching_confirmation_deletes(self):
        self.assertEqual(self._clean(keep=1, confirm=4), 0)
        self.assertEqual(self._count(), 1)

    def test_nothing_to_remove_is_not_an_error(self):
        self.assertEqual(self._clean(keep=99), 0)
        self.assertEqual(self._count(), 5)


class TestReportIsRedactedAtWriteTime(unittest.TestCase):
    """A security review is required to quote the credential it found — the
    report format demands concrete evidence — and `history record` copied
    that report byte-for-byte into the consuming project's .akos/reviews/.
    install-project added no .gitignore entry, so a key that was gitignored
    in .env could reach a remote via the audit trail. No attacker needed."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.project = Path(self._tmp.name)
        self.report = self.project / "report.md"

    def tearDown(self):
        self._tmp.cleanup()

    def _record_and_read(self, report_body: str) -> str:
        self.report.write_text(report_body)

        class Args:
            pass
        a = Args()
        a.dir = str(self.project)
        a.type = "security"
        a.decision = "BLOCKED"
        a.profile = "Production"
        a.report = str(self.report)
        a.scores_json = '{"security": 20}'
        a.packs_json = None
        a.timestamp = "20260101T000000Z"
        self.assertEqual(history.cmd_record(a), 0)
        dirs = sorted((self.project / ".akos/reviews").glob("20260101T000000Z-security-*"))
        self.assertEqual(len(dirs), 1)
        return (dirs[0] / "report.md").read_text()

    def test_vendor_key_does_not_reach_disk(self):
        stored = self._record_and_read(f"Found {AWS_KEY} in src/config.ts:3\n")
        self.assertNotIn(AWS_KEY, stored)
        self.assertIn("REDACTED", stored)

    def test_unquoted_generic_secret_assignment_does_not_reach_disk(self):
        token = "Ax7_qP9m" + "Z2vK8sT4" + "nR6wY3cD"
        stored = self._record_and_read(f"MY_API_KEY={token}\n")
        self.assertNotIn(token, stored)
        self.assertIn("[REDACTED:high_entropy_assignment]", stored)

    def test_the_finding_itself_survives_redaction(self):
        """Redaction that destroys the finding is not a fix — the reviewer
        still needs to know which file and line to go fix."""
        stored = self._record_and_read(
            f"- **Hardcoded key** in `src/config.ts:3` — value {AWS_KEY}\n")
        self.assertIn("src/config.ts:3", stored)
        self.assertIn("Hardcoded key", stored)

    def test_anon_jwt_is_preserved(self):
        """anon and authenticated keys are designed to be public and RLS
        constrains them. Redacting those would strip evidence a reviewer
        legitimately needs."""
        anon = "eyJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoiYW5vbiJ9.sig1234567890"
        stored = self._record_and_read(f"Anon key {anon} is fine, RLS covers it.\n")
        self.assertIn(anon, stored)

    def test_placeholder_is_not_redacted(self):
        stored = self._record_and_read('password = "changeme" is a placeholder\n')
        self.assertIn("changeme", stored)

    def test_ordinary_prose_is_untouched(self):
        body = "## Critical\n\n- The login form has no error state.\n"
        self.assertEqual(self._record_and_read(body), body)


class TestRecordEnsuresGitignore(unittest.TestCase):
    """install-project adds .akos/reviews/ to .gitignore, but a review can be
    recorded into a project that never ran it — which is what happened on the
    first real end-to-end run: the reports landed untracked and unprotected in
    a repo that had never been scaffolded. The protection has to live where
    the file is written, not only where the project is set up."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.project = Path(self._tmp.name)
        subprocess.run(["git", "init", "-q"], cwd=self.project, check=True)
        self.report = self.project / "report.md"
        self.report.write_text("# Review\n")

    def tearDown(self):
        self._tmp.cleanup()

    def _record(self, ts="20260101T000000Z"):
        class Args:
            pass
        a = Args()
        a.dir = str(self.project)
        a.type = "full"
        a.decision = "PASS"
        a.profile = "Startup MVP"
        a.report = str(self.report)
        a.scores_json = '{"ux": 70}'
        a.packs_json = None
        a.timestamp = ts
        return history.cmd_record(a)

    def _lines(self):
        p = self.project / ".gitignore"
        return p.read_text().splitlines() if p.is_file() else []

    def test_creates_gitignore_when_absent(self):
        self._record()
        self.assertIn(".akos/reviews/", self._lines())

    def test_does_not_duplicate_on_a_second_review(self):
        self._record("20260101T000000Z")
        self._record("20260102T000000Z")
        self.assertEqual(self._lines().count(".akos/reviews/"), 1)

    def test_preserves_existing_gitignore_content(self):
        (self.project / ".gitignore").write_text("node_modules/\ndist/\n")
        self._record()
        lines = self._lines()
        self.assertIn("node_modules/", lines)
        self.assertIn("dist/", lines)
        self.assertIn(".akos/reviews/", lines)

    def test_reasserts_ignore_rule_after_a_later_exact_negation(self):
        (self.project / ".gitignore").write_text(
            ".akos/reviews/\n!.akos/reviews/\n",
            encoding="utf-8",
        )

        self.assertEqual(self._record(), 0)

        relevant = [
            line.strip()
            for line in self._lines()
            if line.strip() in {".akos/reviews/", "!.akos/reviews/"}
        ]
        self.assertEqual(relevant[-1], ".akos/reviews/")

    def test_gitignore_change_is_rolled_back_when_publish_fails(self):
        gitignore = self.project / ".gitignore"
        gitignore.write_text("node_modules/\n", encoding="utf-8")
        original = gitignore.read_bytes()
        real_rename = history.os.rename

        def fail_review_publish(source, destination, *args, **kwargs):
            if "full" in str(destination):
                raise OSError("simulated publish failure")
            return real_rename(source, destination, *args, **kwargs)

        with mock.patch.object(
            history.os,
            "rename",
            side_effect=fail_review_publish,
        ):
            rc = self._record()

        self.assertEqual(rc, 1)
        self.assertEqual(gitignore.read_bytes(), original)

    def test_non_git_directory_is_left_alone(self):
        """Nothing to ignore into, and writing a .gitignore into a plain
        directory would be a surprise the caller did not ask for."""
        plain = Path(self._tmp.name) / "plain"
        plain.mkdir()
        self.assertFalse(history.ensure_gitignored(plain))
        self.assertFalse((plain / ".gitignore").exists())


class TestHistoryIsUniqueAndAtomic(unittest.TestCase):
    """Two records with the same second and type used to share a directory
    (id was timestamp+type, `mkdir(exist_ok=True)`), and the three files were
    written straight into the final dir, so a crash left a partial review.
    Uniqueness now comes from a random id suffix, and publish is an atomic
    rename of a staged temp dir."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.project = Path(self._tmp.name)
        self.report = self.project / "report.md"
        self.report.write_text("# Review\n")

    def tearDown(self):
        self._tmp.cleanup()

    def _args(self, ts="20260101T000000Z", rtype="security"):
        class Args:
            pass
        a = Args()
        a.dir = str(self.project)
        a.type = rtype
        a.decision = "PASS"
        a.profile = "Production"
        a.report = str(self.report)
        a.scores_json = '{"security": 90}'
        a.packs_json = None
        a.timestamp = ts
        return a

    def _dirs(self):
        d = self.project / ".akos/reviews"
        return [p for p in d.iterdir() if p.is_dir()] if d.exists() else []

    def test_history_same_second_does_not_overwrite(self):
        self.assertEqual(history.cmd_record(self._args()), 0)
        self.assertEqual(history.cmd_record(self._args()), 0)
        dirs = self._dirs()
        self.assertEqual(len(dirs), 2, "same-second, same-type records must not share a directory")
        # Each keeps its own valid, distinct content.
        for d in dirs:
            meta = json.loads((d / "metadata.json").read_text())
            self.assertEqual(meta["review_id"], d.name)

    def test_history_metadata_review_id_matches_directory(self):
        self.assertEqual(history.cmd_record(self._args()), 0)
        d = self._dirs()[0]
        meta = json.loads((d / "metadata.json").read_text())
        self.assertEqual(meta["review_id"], d.name)

    def test_history_existing_review_is_never_overwritten(self):
        self.assertEqual(history.cmd_record(self._args()), 0)
        published = self._dirs()[0]
        original = (published / "report.md").read_text()
        forced_id = published.name

        # Force every id attempt to collide with the published review.
        from unittest import mock
        with mock.patch.object(history, "make_review_id", return_value=forced_id):
            rc = history.cmd_record(self._args())
        self.assertEqual(rc, 1, "a forced permanent collision must fail, not overwrite")
        self.assertEqual((published / "report.md").read_text(), original,
                         "the already-published review must be untouched")
        self.assertFalse(list((self.project / ".akos/reviews").glob(".tmp-review-*")),
                         "no staging dir may be left behind")

    def test_history_collision_retries_with_new_id(self):
        self.assertEqual(history.cmd_record(self._args()), 0)
        taken = self._dirs()[0].name
        real = history.make_review_id

        # Collide once, then let the real generator produce a fresh id.
        seq = [taken]
        def fake(rtype, ts):
            return seq.pop(0) if seq else real(rtype, ts)

        from unittest import mock
        with mock.patch.object(history, "make_review_id", side_effect=fake):
            rc = history.cmd_record(self._args())
        self.assertEqual(rc, 0, "a single collision must be retried, not fatal")
        self.assertEqual(len(self._dirs()), 2, "the retry must publish a second, distinct review")

    def test_history_write_failure_leaves_no_partial_review(self):
        real_dumps = history.json.dumps

        def boom(obj, *a, **k):
            # Fail after report.md is staged, while writing metadata.json.
            if isinstance(obj, dict) and "review_id" in obj:
                raise RuntimeError("simulated disk failure")
            return real_dumps(obj, *a, **k)

        from unittest import mock
        with mock.patch.object(history.json, "dumps", side_effect=boom):
            rc = history.cmd_record(self._args())
        self.assertEqual(rc, 1)
        self.assertEqual(self._dirs(), [], "a failed record must leave no published review")
        self.assertFalse(list((self.project / ".akos/reviews").glob(".tmp-review-*")),
                         "a failed record must leave no staging dir")

    def test_history_parallel_records_are_atomic(self):
        import concurrent.futures

        history_py = str(Path(paths.AKOS_HOME) / "schemas" / "history.py")

        def one(_i):
            return subprocess.run(
                [sys.executable, history_py, "record",
                 "--type", "security", "--decision", "PASS", "--profile", "Production",
                 "--report", str(self.report), "--dir", str(self.project),
                 "--timestamp", "20260101T000000Z"],
                capture_output=True, text=True).returncode

        n = 8
        with concurrent.futures.ThreadPoolExecutor(max_workers=n) as ex:
            codes = list(ex.map(one, range(n)))

        self.assertTrue(all(c == 0 for c in codes), f"all records should succeed: {codes}")
        dirs = self._dirs()
        self.assertEqual(len(dirs), n, "every concurrent record must survive as its own review")
        for d in dirs:
            for name in ("report.md", "metadata.json", "report.json"):
                self.assertTrue((d / name).is_file(), f"{d.name} missing {name}")
            json.loads((d / "metadata.json").read_text())
        self.assertFalse(list((self.project / ".akos/reviews").glob(".tmp-review-*")),
                         "no orphan staging dirs may remain")

    def test_history_json_is_valid_before_publish(self):
        real_dumps = history.json.dumps

        def bad_dumps(obj, *a, **k):
            # Corrupt only the report.json payload (decision+scores dict) —
            # metadata.json must still write cleanly, so this isolates the
            # re-parse check from the metadata-focused failure test above.
            if isinstance(obj, dict) and "decision" in obj and "scores" in obj:
                return "{not valid json"
            return real_dumps(obj, *a, **k)

        from unittest import mock
        with mock.patch.object(history.json, "dumps", side_effect=bad_dumps):
            rc = history.cmd_record(self._args())
        self.assertEqual(rc, 1, "invalid report.json content must be caught before publish, not after")
        self.assertEqual(self._dirs(), [], "nothing may be published when report.json fails to reparse")
        self.assertFalse(list((self.project / ".akos/reviews").glob(".tmp-review-*")),
                         "a caught pre-publish corruption must leave no staging dir")

    def test_history_failure_removes_staging_directory(self):
        # A distinct failure point from test_history_write_failure_leaves_no_partial_review
        # (which fails during metadata construction): this fails at publish
        # time itself (os.rename), after all three files are already staged.
        from unittest import mock
        with mock.patch.object(history.os, "rename", side_effect=OSError(13, "Permission denied")):
            rc = history.cmd_record(self._args())
        self.assertEqual(rc, 1, "a publish-time failure must be reported, not silently swallowed")
        self.assertEqual(self._dirs(), [], "a failed publish must leave no final review directory")
        self.assertFalse(list((self.project / ".akos/reviews").glob(".tmp-review-*")),
                         "a failed publish must leave no staging directory behind")


class TestHistoryReadersHandleStagingAndCorruption(unittest.TestCase):
    """`list`/`latest`/`clean` must never mistake an in-flight staging dir for
    a published review, and a published-but-corrupt review must be reported,
    not silently hidden as if it never existed and not shown as if clean."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.project = Path(self._tmp.name)
        self.report = self.project / "report.md"
        self.report.write_text("# Review\n")

    def tearDown(self):
        self._tmp.cleanup()

    def _args(self, ts="20260101T000000Z", rtype="security"):
        class Args:
            pass
        a = Args()
        a.dir = str(self.project)
        a.type = rtype
        a.decision = "PASS"
        a.profile = "Production"
        a.report = str(self.report)
        a.scores_json = '{"security": 90}'
        a.packs_json = None
        a.timestamp = ts
        return a

    def _reviews_dir(self) -> Path:
        d = self.project / ".akos/reviews"
        d.mkdir(parents=True, exist_ok=True)
        return d

    def _capture(self, fn, *args):
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = fn(*args)
        return rc, buf.getvalue()

    def test_history_staging_directory_is_not_listed(self):
        self.assertEqual(history.cmd_record(self._args()), 0)
        staging = self._reviews_dir() / ".tmp-review-orphaned"
        staging.mkdir()
        (staging / "report.md").write_text("in flight")

        rc, out = self._capture(history.cmd_list, self._args())
        self.assertEqual(rc, 0)
        self.assertNotIn(".tmp-review-orphaned", out, "a staging dir must never appear in `list`")

        # `latest` must resolve to the real published review, never the
        # staging dir, regardless of how the two names happen to sort.
        args = self._args()
        rc, out = self._capture(history.cmd_latest, args)
        self.assertEqual(rc, 0)
        self.assertNotIn("no such review", out)

    def test_history_corrupt_published_review_is_reported(self):
        self.assertEqual(history.cmd_record(self._args()), 0)
        published = next(p for p in self._reviews_dir().iterdir() if p.is_dir())
        (published / "report.json").unlink()  # simulate a corrupted publish

        rc, out = self._capture(history.cmd_list, self._args())
        self.assertEqual(rc, 0, "list itself does not fail — it reports the corrupt entry")
        self.assertIn(published.name, out)
        self.assertIn("corrupt", out.lower())

        show_args = self._args()
        show_args.review_id = published.name
        rc, _ = self._capture(history.cmd_show, show_args)
        self.assertEqual(rc, 1, "show must refuse a corrupt review, not print partial/garbage data")

    def test_history_clean_never_deletes_a_staging_directory(self):
        self.assertEqual(history.cmd_record(self._args()), 0)
        staging = self._reviews_dir() / ".tmp-review-orphaned"
        staging.mkdir()
        (staging / "report.md").write_text("in flight")

        args = self._args()
        args.keep = 0
        args.dry_run = False
        args.confirm_delete = 1  # only the 1 real published review is a candidate
        rc, _ = self._capture(history.cmd_clean, args)
        self.assertEqual(rc, 0)
        self.assertTrue(staging.is_dir(), "clean must never sweep a staging directory")


class TestHistoryFilesystemHardening(unittest.TestCase):
    """Regression coverage for the history store's filesystem trust boundary."""

    def setUp(self):
        self._project_tmp = tempfile.TemporaryDirectory()
        self._outside_tmp = tempfile.TemporaryDirectory()
        self.project = Path(self._project_tmp.name)
        self.outside = Path(self._outside_tmp.name)
        self.report = self.project / "report.md"
        self.report.write_text("# Review\n", encoding="utf-8")

    def tearDown(self):
        self._project_tmp.cleanup()
        self._outside_tmp.cleanup()

    def _record_args(self):
        class Args:
            pass

        args = Args()
        args.dir = str(self.project)
        args.type = "security"
        args.decision = "PASS"
        args.profile = "Production"
        args.report = str(self.report)
        args.scores_json = '{"security": 90}'
        args.packs_json = None
        args.timestamp = "20260101T000000Z"
        return args

    def _clean_args(self, *, keep=0, confirm=1, dry_run=False):
        class Args:
            pass

        args = Args()
        args.dir = str(self.project)
        args.keep = keep
        args.confirm_delete = confirm
        args.dry_run = dry_run
        return args

    def _make_review(self, review_id: str, parent: Path | None = None) -> Path:
        review = (parent or (self.project / ".akos/reviews")) / review_id
        review.mkdir(parents=True)
        metadata = {
            "review_id": review_id,
            "decision": "PASS",
            "profile": "Production",
        }
        (review / "report.md").write_text("# Review\n", encoding="utf-8")
        (review / "metadata.json").write_text(json.dumps(metadata), encoding="utf-8")
        (review / "report.json").write_text(
            json.dumps({"decision": "PASS", "scores": {"security": 90}}),
            encoding="utf-8",
        )
        return review

    def _invoke_clean(self, args):
        try:
            return history.cmd_clean(args)
        except Exception as exc:  # the hardened contract is a clean rc=1, never an exception
            return exc

    def test_record_rejects_symlinked_reviews_root_before_publish(self):
        sentinel = self.outside / "sentinel.txt"
        sentinel.write_text("keep", encoding="utf-8")
        (self.project / ".akos").mkdir()
        (self.project / ".akos/reviews").symlink_to(self.outside, target_is_directory=True)

        rc = history.cmd_record(self._record_args())

        self.assertEqual(rc, 1)
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep")
        self.assertEqual(
            sorted(path.name for path in self.outside.iterdir()),
            ["sentinel.txt"],
            "record must not stage or publish through a symlinked reviews root",
        )

    def test_clean_rejects_symlinked_reviews_root_without_touching_target(self):
        review = self._make_review("20250101T000000Z-security-safe", self.outside)
        sentinel = review / "sentinel.txt"
        sentinel.write_text("keep", encoding="utf-8")
        (self.project / ".akos").mkdir()
        (self.project / ".akos/reviews").symlink_to(self.outside, target_is_directory=True)

        rc = self._invoke_clean(self._clean_args())

        self.assertEqual(rc, 1)
        self.assertTrue(review.is_dir())
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep")

    def test_clean_rejects_symlinked_review_entry_and_preserves_outside_sentinel(self):
        outside_review = self._make_review("outside-review", self.outside)
        sentinel = outside_review / "sentinel.txt"
        sentinel.write_text("keep", encoding="utf-8")
        reviews = self.project / ".akos/reviews"
        reviews.mkdir(parents=True)
        entry = reviews / "20250101T000000Z-security-linked"
        entry.symlink_to(outside_review, target_is_directory=True)

        rc = self._invoke_clean(self._clean_args())

        self.assertEqual(rc, 1)
        self.assertTrue(entry.is_symlink())
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep")

    def test_clean_rejects_each_symlinked_required_file(self):
        review = self._make_review("20250101T000000Z-security-file-link")
        originals = {
            name: (review / name).read_bytes()
            for name in history.REQUIRED_FILES
        }
        for name in history.REQUIRED_FILES:
            with self.subTest(name=name):
                sentinel = self.outside / name
                sentinel.write_bytes(b"keep")
                internal = review / name
                internal.unlink()
                internal.symlink_to(sentinel)

                rc = self._invoke_clean(self._clean_args())

                self.assertEqual(rc, 1)
                self.assertTrue(review.is_dir())
                self.assertTrue(internal.is_symlink())
                self.assertEqual(sentinel.read_bytes(), b"keep")
                internal.unlink()
                internal.write_bytes(originals[name])

    def test_record_rejects_symlinked_akos_directory(self):
        sentinel = self.outside / "sentinel.txt"
        sentinel.write_text("keep", encoding="utf-8")
        (self.project / ".akos").symlink_to(self.outside, target_is_directory=True)

        rc = history.cmd_record(self._record_args())

        self.assertEqual(rc, 1)
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep")
        self.assertEqual(sorted(path.name for path in self.outside.iterdir()), ["sentinel.txt"])

    def test_list_reports_symlinked_required_file_as_corrupt(self):
        sentinel = self.outside / "metadata.json"
        sentinel.write_text(
            json.dumps({"decision": "PASS", "profile": "outside"}),
            encoding="utf-8",
        )
        review = self._make_review("20250101T000000Z-security-file-link")
        (review / "metadata.json").unlink()
        (review / "metadata.json").symlink_to(sentinel)

        import io
        from contextlib import redirect_stdout

        output = io.StringIO()
        with redirect_stdout(output):
            rc = history.cmd_list(self._record_args())

        self.assertEqual(rc, 0)
        self.assertIn("corrupt", output.getvalue().lower())
        self.assertIn("symlink", output.getvalue().lower())

    def test_clean_rejects_unexpected_contents_without_partial_deletion(self):
        first = self._make_review("20250101T000000Z-security-first")
        malformed = self._make_review("20250102T000000Z-security-malformed")
        (malformed / "unexpected").mkdir()
        (malformed / "unexpected/sentinel.txt").write_text("keep", encoding="utf-8")

        rc = self._invoke_clean(self._clean_args(confirm=2))

        self.assertEqual(rc, 1)
        self.assertTrue(first.is_dir(), "clean must preflight every candidate before deleting any")
        self.assertTrue(malformed.is_dir())
        self.assertEqual(
            (malformed / "unexpected/sentinel.txt").read_text(encoding="utf-8"),
            "keep",
        )

    def test_clean_preflights_corrupt_entries_that_would_be_kept(self):
        removable = self._make_review("20250101T000000Z-security-removable")
        kept_but_corrupt = self._make_review("20250102T000000Z-security-kept")
        (kept_but_corrupt / "unexpected.txt").write_text("keep", encoding="utf-8")

        rc = self._invoke_clean(self._clean_args(keep=1, confirm=1))

        self.assertEqual(rc, 1)
        self.assertTrue(
            removable.is_dir(),
            "any corrupt published entry must abort the entire clean before deletion",
        )
        self.assertTrue(kept_but_corrupt.is_dir())

    def test_record_rejects_symlinked_gitignore_before_publish(self):
        subprocess.run(["git", "init", "-q"], cwd=self.project, check=True)
        sentinel = self.outside / "gitignore"
        sentinel.write_text("outside-content\n", encoding="utf-8")
        (self.project / ".gitignore").symlink_to(sentinel)

        rc = history.cmd_record(self._record_args())

        self.assertEqual(rc, 1)
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "outside-content\n")
        reviews = self.project / ".akos/reviews"
        self.assertFalse(reviews.exists() and any(reviews.iterdir()))

    def test_clean_parent_swap_cannot_unlink_an_outside_review(self):
        review_id = "20250101T000000Z-security-safe"
        self._make_review(review_id)
        outside_akos = self.outside / "akos"
        outside_review = self._make_review(review_id, outside_akos / "reviews")
        outside_snapshot = {
            name: (outside_review / name).read_bytes()
            for name in history.REQUIRED_FILES
        }
        original_akos = self.project / ".akos-original"
        real_unlink = history.os.unlink
        swapped = False

        def swap_parent_before_unlink(path, *args, **kwargs):
            nonlocal swapped
            if not swapped:
                swapped = True
                (self.project / ".akos").rename(original_akos)
                (self.project / ".akos").symlink_to(
                    outside_akos,
                    target_is_directory=True,
                )
            return real_unlink(path, *args, **kwargs)

        with mock.patch.object(
            history.os,
            "unlink",
            side_effect=swap_parent_before_unlink,
        ):
            rc = self._invoke_clean(self._clean_args())

        self.assertIn(rc, (0, 1))
        self.assertTrue(outside_review.is_dir())
        self.assertEqual(
            {
                name: (outside_review / name).read_bytes()
                for name in history.REQUIRED_FILES
            },
            outside_snapshot,
        )


class TestHistoryCliContract(unittest.TestCase):
    def test_usage_errors_exit_one(self):
        for argv in (["list", "--unknown"], ["record"]):
            with self.subTest(argv=argv), self.assertRaises(SystemExit) as raised:
                history.main(argv)
            self.assertEqual(raised.exception.code, 1)

    def test_clean_rejects_negative_keep_as_usage_error(self):
        with tempfile.TemporaryDirectory() as project:
            with self.assertRaises(SystemExit) as raised:
                history.main([
                    "clean",
                    "--dir",
                    project,
                    "--keep=-1",
                    "--dry-run",
                ])
        self.assertEqual(raised.exception.code, 1)
