import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "helpers"))
import paths  # noqa: F401,E402

import history  # noqa: E402


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

    def _record(self, decision: str, scores: dict, ts: str):
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
        history.cmd_record(a)

    def test_record_creates_expected_files(self):
        self._record("BLOCKED", {"ux": 50}, "20260101T000000Z")
        out_dir = self.project / ".akos/reviews/20260101T000000Z-ux-review"
        self.assertTrue((out_dir / "report.md").exists())
        self.assertTrue((out_dir / "report.json").exists())
        self.assertTrue((out_dir / "metadata.json").exists())

    def test_compare_reports_correct_decision_transition_and_score_delta(self):
        self._record("BLOCKED", {"ux": 50, "accessibility": 60}, "20260101T000000Z")
        self._record("PASS WITH FIXES", {"ux": 78, "accessibility": 80}, "20260102T000000Z")

        import io
        from contextlib import redirect_stdout

        class Args:
            pass
        a = Args()
        a.dir = str(self.project)
        a.review_a = "20260101T000000Z-ux-review"
        a.review_b = "20260102T000000Z-ux-review"

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
        self.assertEqual(self._review_dirs(), ["20260101T000000Z-ux-review"])


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
        return (self.project / ".akos/reviews/20260101T000000Z-security/report.md").read_text()

    def test_vendor_key_does_not_reach_disk(self):
        stored = self._record_and_read("Found AKIAABCDEFGHIJKLMNOP in src/config.ts:3\n")
        self.assertNotIn("AKIAABCDEFGHIJKLMNOP", stored)
        self.assertIn("REDACTED", stored)

    def test_the_finding_itself_survives_redaction(self):
        """Redaction that destroys the finding is not a fix — the reviewer
        still needs to know which file and line to go fix."""
        stored = self._record_and_read(
            "- **Hardcoded key** in `src/config.ts:3` — value AKIAABCDEFGHIJKLMNOP\n")
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

    def test_non_git_directory_is_left_alone(self):
        """Nothing to ignore into, and writing a .gitignore into a plain
        directory would be a surprise the caller did not ask for."""
        plain = Path(self._tmp.name) / "plain"
        plain.mkdir()
        self.assertFalse(history.ensure_gitignored(plain))
        self.assertFalse((plain / ".gitignore").exists())
