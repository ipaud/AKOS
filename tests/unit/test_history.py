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
        history.cmd_clean(a)

        remaining = list((self.project / ".akos/reviews").iterdir())
        self.assertEqual(len(remaining), 2)


if __name__ == "__main__":
    unittest.main()
