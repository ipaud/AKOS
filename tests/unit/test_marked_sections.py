import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

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


class TestProjectInstallTransaction(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.base = Path(self._tmp.name)
        self.project = self.base / "project"
        self.project.mkdir()
        self.bodies = {
            "CLAUDE.md": "claude body",
            "AGENTS.md": "agents body",
            ".cursor/rules/akos.mdc": "cursor body",
            ".akos/config.md": "config body",
        }

    def tearDown(self):
        self._tmp.cleanup()

    def test_project_root_must_already_exist(self):
        missing = self.base / "missing"
        with self.assertRaises(ms.ProjectPathError):
            ms.install_project_files(missing, self.bodies)
        self.assertFalse(missing.exists())

    def test_explicit_root_symlink_is_resolved(self):
        alias = self.base / "alias"
        alias.symlink_to(self.project, target_is_directory=True)

        ms.install_project_files(alias, self.bodies)

        self.assertIn("claude body", (self.project / "CLAUDE.md").read_text())
        self.assertIn(".akos/reviews/", (self.project / ".gitignore").read_text())

    def test_symlinked_child_directory_is_rejected_before_any_write(self):
        outside = self.base / "outside"
        outside.mkdir()
        (self.project / ".akos").symlink_to(outside, target_is_directory=True)

        with self.assertRaises(ms.ProjectPathError):
            ms.install_project_files(self.project, self.bodies)

        self.assertFalse((self.project / "CLAUDE.md").exists())
        self.assertEqual(list(outside.iterdir()), [])

    def test_symlinked_gitignore_leaf_is_rejected_before_any_write(self):
        outside = self.base / "outside.gitignore"
        outside.write_text("outside\n")
        (self.project / ".gitignore").symlink_to(outside)

        with self.assertRaises(ms.ProjectPathError):
            ms.install_project_files(self.project, self.bodies)

        self.assertFalse((self.project / "CLAUDE.md").exists())
        self.assertEqual(outside.read_text(), "outside\n")

    def test_each_managed_leaf_symlink_is_rejected_before_any_write(self):
        for index, relative in enumerate(ms.PROJECT_MARKED_PATHS):
            with self.subTest(relative=relative):
                project = self.base / f"leaf-project-{index}"
                project.mkdir()
                outside = self.base / f"outside-{index}.txt"
                outside.write_text("outside\n")
                target = project / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.symlink_to(outside)

                with self.assertRaises(ms.ProjectPathError):
                    ms.install_project_files(project, self.bodies)

                self.assertTrue(target.is_symlink())
                self.assertEqual(outside.read_text(), "outside\n")
                self.assertFalse((project / ".gitignore").exists())
                for other_relative in ms.PROJECT_MARKED_PATHS:
                    other = project / other_relative
                    if other != target:
                        self.assertFalse(
                            other.exists(),
                            f"{other_relative} was written before rejecting {relative}",
                        )

    def test_reasserts_gitignore_after_a_later_exact_negation(self):
        gitignore = self.project / ".gitignore"
        gitignore.write_text(
            ".akos/reviews/\n!.akos/reviews/\n",
            encoding="utf-8",
        )

        result = ms.install_project_files(self.project, self.bodies)

        relevant = [
            line.strip()
            for line in gitignore.read_text(encoding="utf-8").splitlines()
            if line.strip() in {".akos/reviews/", "!.akos/reviews/"}
        ]
        self.assertTrue(result.gitignore_added)
        self.assertEqual(relevant[-1], ".akos/reviews/")

    def test_parent_swap_before_replace_never_writes_through_symlink(self):
        akos = self.project / ".akos"
        akos.mkdir()
        (akos / "config.md").write_text("original config\n", encoding="utf-8")
        outside = self.base / "outside-akos"
        outside.mkdir()
        outside_config = outside / "config.md"
        outside_config.write_text("outside config\n", encoding="utf-8")
        moved_akos = self.project / ".akos-original"
        real_replace = ms.os.replace
        calls = 0

        def swap_before_config_replace(source, destination, *args, **kwargs):
            nonlocal calls
            calls += 1
            if calls == 4:
                akos.rename(moved_akos)
                akos.symlink_to(outside, target_is_directory=True)
                if kwargs.get("src_dir_fd") is None:
                    # A path-based replace resolves its source again after the
                    # swap. Model an attacker moving the already-written temp
                    # leaf into the symlink target under the same observable
                    # name; fd-relative replace must remain anchored instead.
                    (moved_akos / Path(source).name).rename(
                        outside / Path(source).name
                    )
            return real_replace(source, destination, *args, **kwargs)

        with mock.patch.object(
            ms.os,
            "replace",
            side_effect=swap_before_config_replace,
        ):
            with self.assertRaises(ms.ProjectWriteError):
                ms.install_project_files(self.project, self.bodies)

        self.assertEqual(outside_config.read_text(encoding="utf-8"), "outside config\n")
        self.assertEqual(
            (moved_akos / "config.md").read_text(encoding="utf-8"),
            "original config\n",
        )

    def test_parent_swap_during_failure_cannot_redirect_rollback(self):
        cursor_file = self.project / ".cursor/rules/akos.mdc"
        cursor_file.parent.mkdir(parents=True)
        cursor_file.write_text("original cursor\n", encoding="utf-8")
        outside = self.base / "outside-cursor"
        outside_rules = outside / "rules"
        outside_rules.mkdir(parents=True)
        outside_file = outside_rules / "akos.mdc"
        outside_file.write_text("outside cursor\n", encoding="utf-8")
        moved_cursor = self.project / ".cursor-original"
        real_replace = ms.os.replace
        calls = 0

        def swap_then_fail(source, destination, *args, **kwargs):
            nonlocal calls
            calls += 1
            result = real_replace(source, destination, *args, **kwargs)
            if calls == 3:
                (self.project / ".cursor").rename(moved_cursor)
                (self.project / ".cursor").symlink_to(
                    outside,
                    target_is_directory=True,
                )
            if calls == 4:
                raise OSError("simulated write failure after parent swap")
            return result

        with mock.patch.object(ms.os, "replace", side_effect=swap_then_fail):
            with self.assertRaises(ms.ProjectWriteError):
                ms.install_project_files(self.project, self.bodies)

        self.assertEqual(outside_file.read_text(encoding="utf-8"), "outside cursor\n")
        self.assertEqual(
            (moved_cursor / "rules/akos.mdc").read_text(encoding="utf-8"),
            "original cursor\n",
        )

    def test_write_failure_rolls_back_every_prepared_target(self):
        claude = self.project / "CLAUDE.md"
        claude.write_text("original\n")
        claude.chmod(0o600)
        real_atomic_write = ms._atomic_write_at
        calls = 0

        def fail_fourth_write(parent_fd, leaf_name, content, mode):
            nonlocal calls
            calls += 1
            if calls == 4:
                raise OSError("simulated fourth-write failure")
            return real_atomic_write(parent_fd, leaf_name, content, mode)

        with mock.patch.object(ms, "_atomic_write_at", side_effect=fail_fourth_write):
            with self.assertRaises(ms.ProjectWriteError):
                ms.install_project_files(self.project, self.bodies)

        self.assertEqual(claude.read_text(), "original\n")
        self.assertEqual(stat.S_IMODE(claude.stat().st_mode), 0o600)
        self.assertFalse((self.project / "AGENTS.md").exists())
        self.assertFalse((self.project / ".cursor").exists())
        self.assertFalse((self.project / ".akos").exists())
        self.assertFalse((self.project / ".gitignore").exists())

    def test_symlink_appearing_mid_transaction_rolls_back_completed_writes(self):
        claude = self.project / "CLAUDE.md"
        agents = self.project / "AGENTS.md"
        claude.write_text("original claude\n")
        agents.write_text("original agents\n")
        outside = self.base / "outside-directory"
        outside.mkdir()
        real_atomic_write = ms._atomic_write_at
        writes = 0

        def introduce_symlink_before_config(parent_fd, leaf_name, content, mode):
            nonlocal writes
            writes += 1
            if writes == 4:
                akos_dir = self.project / ".akos"
                if akos_dir.exists():
                    akos_dir.rmdir()
                akos_dir.symlink_to(outside, target_is_directory=True)
            return real_atomic_write(parent_fd, leaf_name, content, mode)

        with mock.patch.object(
            ms,
            "_atomic_write_at",
            side_effect=introduce_symlink_before_config,
        ):
            with self.assertRaises(ms.ProjectWriteError):
                ms.install_project_files(self.project, self.bodies)

        self.assertEqual(claude.read_text(), "original claude\n")
        self.assertEqual(agents.read_text(), "original agents\n")
        self.assertFalse((self.project / ".cursor").exists())
        self.assertTrue((self.project / ".akos").is_symlink())
        self.assertEqual(list(outside.iterdir()), [])


class TestProjectProfileUpdate(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.base = Path(self._tmp.name)
        self.project = self.base / "project"
        self.project.mkdir()
        self.config = self.project / ".akos/config.md"
        self.config.parent.mkdir()
        self.original = (
            "before\n"
            "<!-- AKOS:START -->\n"
            "# AKOS Project Config\n"
            "personal_profile: old-profile\n"
            "keep: this value\n"
            "<!-- AKOS:END -->\n"
            "after\n"
        )
        self.config.write_text(self.original, encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def test_updates_profile_through_anchored_project_transaction(self):
        result = ms.set_project_personal_profile(self.project, "pau-avila")

        updated = self.config.read_text(encoding="utf-8")
        self.assertEqual(result, self.config.resolve())
        self.assertIn("personal_profile: pau-avila", updated)
        self.assertIn("keep: this value", updated)
        self.assertTrue(updated.startswith("before\n"))
        self.assertTrue(updated.endswith("after\n"))

    def test_rejects_symlinked_akos_parent_without_touching_outside(self):
        outside = self.base / "outside-akos"
        self.config.parent.rename(outside)
        (self.project / ".akos").symlink_to(outside, target_is_directory=True)
        snapshot = (outside / "config.md").read_bytes()

        with self.assertRaises(ms.ProjectPathError):
            ms.set_project_personal_profile(self.project, "pau-avila")

        self.assertEqual((outside / "config.md").read_bytes(), snapshot)

    def test_rejects_symlinked_config_leaf_without_touching_outside(self):
        outside = self.base / "outside-config.md"
        outside.write_text(self.original, encoding="utf-8")
        self.config.unlink()
        self.config.symlink_to(outside)
        snapshot = outside.read_bytes()

        with self.assertRaises(ms.ProjectPathError):
            ms.set_project_personal_profile(self.project, "pau-avila")

        self.assertEqual(outside.read_bytes(), snapshot)


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
