import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "helpers"))
import paths  # noqa: F401,E402

import marked_sections as ms  # noqa: E402


class TestClassify(unittest.TestCase):
    def test_marker_absent_when_no_markers_present(self):
        self.assertEqual(ms.classify("just some text\n").status, ms.ABSENT)

    def test_marker_absent_for_empty_text(self):
        self.assertEqual(ms.classify("").status, ms.ABSENT)

    def test_marker_present_for_single_valid_pair(self):
        text = "before\n<!-- AKOS:START -->\nbody\n<!-- AKOS:END -->\nafter\n"
        state = ms.classify(text)
        self.assertEqual(state.status, ms.PRESENT)
        self.assertEqual(state.start_line, 1)
        self.assertEqual(state.end_line, 3)

    def test_marker_start_without_end_refuses(self):
        state = ms.classify("<!-- AKOS:START -->\nbody\n")
        self.assertEqual(state.status, ms.INVALID)
        self.assertTrue(any("no END marker" in r for r in state.reasons))

    def test_marker_end_without_start_refuses(self):
        state = ms.classify("body\n<!-- AKOS:END -->\n")
        self.assertEqual(state.status, ms.INVALID)
        self.assertTrue(any("no START marker" in r for r in state.reasons))

    def test_marker_end_before_start_refuses(self):
        state = ms.classify("<!-- AKOS:END -->\nx\n<!-- AKOS:START -->\n")
        self.assertEqual(state.status, ms.INVALID)
        self.assertTrue(any("appears before START" in r for r in state.reasons))

    def test_marker_multiple_starts_refuses(self):
        text = "<!-- AKOS:START -->\na\n<!-- AKOS:START -->\nb\n<!-- AKOS:END -->\n"
        state = ms.classify(text)
        self.assertEqual(state.status, ms.INVALID)
        self.assertTrue(any("multiple START" in r for r in state.reasons))

    def test_marker_multiple_ends_refuses(self):
        text = "<!-- AKOS:START -->\na\n<!-- AKOS:END -->\nb\n<!-- AKOS:END -->\n"
        state = ms.classify(text)
        self.assertEqual(state.status, ms.INVALID)
        self.assertTrue(any("multiple END" in r for r in state.reasons))

    def test_marker_nested_pair_refuses(self):
        # START START END END — a naive "first START + first END" reader
        # would treat this as ONE valid (outer) pair and silently swallow the
        # inner one. Nesting must be reported as INVALID via the same
        # cardinality check (2 starts, 2 ends), not silently accepted.
        text = "<!-- AKOS:START -->\nouter\n<!-- AKOS:START -->\ninner\n<!-- AKOS:END -->\nouter2\n<!-- AKOS:END -->\n"
        state = ms.classify(text)
        self.assertEqual(state.status, ms.INVALID)

    def test_marker_line_must_match_exactly_not_substring(self):
        # A line that merely MENTIONS the marker syntax inside prose must not
        # count — only an exact (stripped) match does.
        text = "See the <!-- AKOS:START --> marker syntax in the docs.\n"
        self.assertEqual(ms.classify(text).status, ms.ABSENT)

    def test_marker_line_matches_with_surrounding_whitespace(self):
        text = "before\n  <!-- AKOS:START -->  \nbody\n<!-- AKOS:END -->\nafter\n"
        self.assertEqual(ms.classify(text).status, ms.PRESENT)


class TestRenderWrite(unittest.TestCase):
    def test_marker_append_to_file_without_markers(self):
        new_text = ms.render_write("existing content\n", "new body")
        self.assertIn("existing content", new_text)
        self.assertIn("<!-- AKOS:START -->\nnew body\n<!-- AKOS:END -->", new_text)

    def test_marker_append_to_empty_text_has_no_leading_blank_line(self):
        new_text = ms.render_write("", "body")
        self.assertEqual(new_text, "<!-- AKOS:START -->\nbody\n<!-- AKOS:END -->\n")

    def test_marker_replace_single_valid_pair(self):
        original = "before\n<!-- AKOS:START -->\nold body\n<!-- AKOS:END -->\nafter\n"
        new_text = ms.render_write(original, "new body")
        self.assertIn("new body", new_text)
        self.assertNotIn("old body", new_text)

    def test_marker_preserves_content_before_and_after(self):
        original = "line one\nline two\n<!-- AKOS:START -->\nold\n<!-- AKOS:END -->\nline three\nline four\n"
        new_text = ms.render_write(original, "new")
        self.assertTrue(new_text.startswith("line one\nline two\n"))
        self.assertTrue(new_text.endswith("line three\nline four\n"))

    def test_marker_handles_no_final_newline(self):
        original = "no trailing newline"
        new_text = ms.render_write(original, "body")
        self.assertTrue(new_text.startswith("no trailing newline\n"))
        self.assertIn("<!-- AKOS:START -->\nbody\n<!-- AKOS:END -->", new_text)

    def test_marker_handles_crlf(self):
        original = "before\r\n<!-- AKOS:START -->\r\nold\r\n<!-- AKOS:END -->\r\nafter\r\n"
        new_text = ms.render_write(original, "new")
        self.assertNotIn("\n\n".replace("\r", ""), "")  # sanity no-op
        self.assertIn("\r\n<!-- AKOS:START -->\r\n", new_text)
        self.assertNotIn("<!-- AKOS:START -->\nnew", new_text, "must not have downgraded to bare LF")

    def test_marker_body_containing_marker_refuses(self):
        with self.assertRaises(ms.MarkerBodyError):
            ms.render_write("plain\n", "line one\n<!-- AKOS:START -->\nline two")

    def test_marker_refuses_to_render_over_invalid_structure(self):
        original = "<!-- AKOS:START -->\na\n<!-- AKOS:START -->\nb\n<!-- AKOS:END -->\n"
        with self.assertRaises(ValueError):
            ms.render_write(original, "new")


class TestCLIWrite(unittest.TestCase):
    """Exercises the actual CLI (subprocess) so atomic-write, mode
    preservation, and checksum/temp-file guarantees are tested end to end,
    not just the pure render_write() function."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def _write(self, file: Path, body: str):
        return subprocess.run(
            [sys.executable, str(paths.AKOS_HOME / "bin" / "marked_sections.py"), "write", str(file), "--body", "-"],
            input=body, capture_output=True, text=True,
        )

    def test_marker_preserves_file_mode(self):
        f = self.dir / "f.md"
        f.write_text("<!-- AKOS:START -->\nold\n<!-- AKOS:END -->\n")
        f.chmod(0o600)
        proc = self._write(f, "new")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(stat.S_IMODE(f.stat().st_mode), 0o600)

    def test_marker_failure_leaves_original_checksum(self):
        f = self.dir / "f.md"
        original = "<!-- AKOS:START -->\na\n<!-- AKOS:START -->\nb\n<!-- AKOS:END -->\n"
        f.write_text(original)
        proc = self._write(f, "new")
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(f.read_text(), original, "an INVALID target must be left byte-for-byte unchanged")

    def test_marker_failure_leaves_no_temp_files(self):
        f = self.dir / "f.md"
        f.write_text("<!-- AKOS:START -->\na\n<!-- AKOS:START -->\nb\n<!-- AKOS:END -->\n")
        self._write(f, "new")
        leftover = list(self.dir.glob(".*.tmp")) + list(self.dir.glob("*.tmp"))
        self.assertEqual(leftover, [], f"temp files leaked: {leftover}")

    def test_marker_body_refusal_leaves_no_temp_files(self):
        f = self.dir / "f.md"
        f.write_text("plain\n")
        proc = self._write(f, "<!-- AKOS:START -->\nbad")
        self.assertEqual(proc.returncode, 2)
        leftover = list(self.dir.glob(".*.tmp")) + list(self.dir.glob("*.tmp"))
        self.assertEqual(leftover, [], f"temp files leaked: {leftover}")

    def test_paths_with_spaces_still_work(self):
        d = self.dir / "a directory with spaces"
        d.mkdir()
        f = d / "file with spaces.md"
        proc = self._write(f, "hello")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("hello", f.read_text())


class TestCLICheckAndExtract(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def _run(self, *args):
        return subprocess.run(
            [sys.executable, str(paths.AKOS_HOME / "bin" / "marked_sections.py"), *args],
            capture_output=True, text=True,
        )

    def test_check_exit_codes(self):
        absent = self.dir / "absent.md"
        absent.write_text("no markers\n")
        self.assertEqual(self._run("check", str(absent)).returncode, 0)

        present = self.dir / "present.md"
        present.write_text("<!-- AKOS:START -->\nx\n<!-- AKOS:END -->\n")
        self.assertEqual(self._run("check", str(present)).returncode, 0)

        invalid = self.dir / "invalid.md"
        invalid.write_text("<!-- AKOS:START -->\nx\n")
        self.assertEqual(self._run("check", str(invalid)).returncode, 2)

    def test_check_on_missing_file_is_absent_not_an_error(self):
        missing = self.dir / "does-not-exist.md"
        proc = self._run("check", str(missing))
        self.assertEqual(proc.returncode, 0)
        self.assertIn("ABSENT", proc.stdout)

    def test_check_on_directory_is_a_usage_error(self):
        proc = self._run("check", str(self.dir))
        self.assertEqual(proc.returncode, 1)

    def test_extract_only_succeeds_on_present(self):
        present = self.dir / "present.md"
        present.write_text("<!-- AKOS:START -->\nthe body\n<!-- AKOS:END -->\n")
        proc = self._run("extract", str(present))
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(proc.stdout.strip(), "the body")

        absent = self.dir / "absent.md"
        absent.write_text("nothing here\n")
        self.assertEqual(self._run("extract", str(absent)).returncode, 2)

    def test_validate_all_install_project_preflights_all_four_files(self):
        ok1 = self.dir / "ok1.md"
        ok1.write_text("clean\n")
        bad = self.dir / "bad.md"
        bad.write_text("<!-- AKOS:START -->\nonly start\n")
        ok2 = self.dir / "ok2.md"
        ok2.write_text("<!-- AKOS:START -->\nx\n<!-- AKOS:END -->\n")
        missing = self.dir / "not-yet-created.md"

        proc = self._run("validate-all", str(ok1), str(bad), str(ok2), str(missing))
        self.assertEqual(proc.returncode, 2, "one malformed target must fail the whole preflight")
        self.assertIn("bad.md", proc.stdout)
        self.assertIn("INVALID", proc.stdout)

    def test_validate_all_passes_when_all_targets_are_safe(self):
        ok1 = self.dir / "ok1.md"
        ok1.write_text("clean\n")
        missing = self.dir / "not-yet-created.md"
        proc = self._run("validate-all", str(ok1), str(missing))
        self.assertEqual(proc.returncode, 0)


class TestSabotageFirstMatchLogicMustFail(unittest.TestCase):
    """Reverting to "grab the first START and first END, ignore the rest"
    (the exact bug this module replaces) must fail at least this test."""

    def test_reverting_to_first_match_would_wrongly_accept_multiple_starts(self):
        text = "<!-- AKOS:START -->\na\n<!-- AKOS:START -->\nb\n<!-- AKOS:END -->\n"
        state = ms.classify(text)
        # A first-match implementation would report this as PRESENT (using
        # the first START at line 0 and the only END at line 4). The correct
        # behavior is INVALID — this assertion is the sabotage tripwire.
        self.assertEqual(state.status, ms.INVALID)
        self.assertNotEqual(state.status, ms.PRESENT)


if __name__ == "__main__":
    unittest.main()
