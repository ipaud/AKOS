"""Unit tests for the 9 rule detectors, each with a temp-dir fixture. These
duplicate some ground already covered by benchmarks/, deliberately — the
benchmark suite is an integration-level regression guard; these are fast,
isolated tests for the detector logic itself, and each one locks down a
real bug this session found while building the detector."""

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "helpers"))
import paths  # noqa: F401,E402


def load_detector(rel_path: str):
    p = paths.AKOS_HOME / rel_path
    spec = importlib.util.spec_from_file_location(p.stem, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def write(tmp: Path, rel: str, content: str) -> Path:
    p = tmp / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)
    return p


# Built at runtime so this test file's own source carries no detectable
# credential literal — the repo self-scan must stay clean without a path
# exception (P0-4). The value still matches AKIA[0-9A-Z]{16} once assembled.
AWS_KEY = "AKIA" + "ABCDEFGHIJKLMNOP"


class TempDirCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()


class TestDetectorReadFailuresAreNotSuppressed(TempDirCase):
    """Every input read failure must reach the runner as phase=read.

    The runner verifies candidate readability before detector execution, but
    the file can become unreadable between that check and the detector read.
    A detector-level ``except OSError: continue`` would turn that race into a
    false clean scan.
    """

    DETECTORS = (
        "rules/accessibility/a11y-input-no-label.py",
        "rules/accessibility/a11y-select-no-label.py",
        "rules/devops/destructive-migration-no-guard.py",
        "rules/devops/migration-no-down-file.py",
        "rules/security/secret-in-source.py",
        "rules/security/service-role-in-client.py",
        "rules/security/supabase-policy-too-permissive.py",
        "rules/security/supabase-rls-disabled.py",
    )

    def test_oserror_from_any_detector_input_propagates(self):
        target = write(self.tmp, "input.sql", "CREATE TABLE t (id int);\n")
        original_read_text = Path.read_text

        def fail_target_read(path, *args, **kwargs):
            if path == target:
                raise PermissionError("simulated post-preflight read failure")
            return original_read_text(path, *args, **kwargs)

        for detector in self.DETECTORS:
            with self.subTest(detector=detector):
                module = load_detector(detector)
                with mock.patch.object(Path, "read_text", fail_target_read):
                    with self.assertRaises(PermissionError):
                        module.run([target])


class TestSupabaseRlsDisabled(TempDirCase):
    def setUp(self):
        super().setUp()
        self.mod = load_detector("rules/security/supabase-rls-disabled.py")

    def test_flags_table_with_no_rls(self):
        f = write(self.tmp, "m/0001.sql", "CREATE TABLE secrets (id uuid primary key);\n")
        findings = self.mod.run([f])
        self.assertEqual(len(findings), 1)

    def test_no_false_positive_when_rls_added_in_a_later_migration(self):
        f1 = write(self.tmp, "m/0001.sql", "CREATE TABLE orders (id uuid primary key);\n")
        f2 = write(self.tmp, "m/0002.sql", "ALTER TABLE orders ENABLE ROW LEVEL SECURITY;\n")
        findings = self.mod.run([f1, f2])
        self.assertEqual(findings, [])

    def test_commented_out_create_table_is_not_matched(self):
        f = write(self.tmp, "m/0001.sql", "-- CREATE TABLE ghost (id uuid);\nCREATE TABLE real_one (id uuid);\nALTER TABLE real_one ENABLE ROW LEVEL SECURITY;\n")
        findings = self.mod.run([f])
        self.assertEqual(findings, [])


class TestA11yInputNoLabel(TempDirCase):
    """Locks down the real bug: JSX uses `htmlFor`, not `for`."""

    def setUp(self):
        super().setUp()
        self.mod = load_detector("rules/accessibility/a11y-input-no-label.py")

    def test_jsx_htmlfor_label_is_recognized(self):
        f = write(self.tmp, "Form.tsx", '<label htmlFor="e">Email</label>\n<input id="e" type="text" />\n')
        findings = self.mod.run([f])
        self.assertEqual(findings, [], "htmlFor (JSX convention) must be recognized, not just plain HTML 'for'")

    def test_unlabeled_input_is_flagged(self):
        f = write(self.tmp, "Form.tsx", '<input type="text" placeholder="x" />\n')
        findings = self.mod.run([f])
        self.assertEqual(len(findings), 1)

    def test_aria_label_suffices(self):
        f = write(self.tmp, "Form.tsx", '<input aria-label="Search" type="search" />\n')
        findings = self.mod.run([f])
        self.assertEqual(findings, [])

    def test_empty_aria_names_do_not_satisfy_the_rule(self):
        for attribute in (
            'aria-label=""',
            'aria-label="   "',
            'aria-labelledby=""',
            'aria-labelledby="   "',
            'aria-label={""}',
            "aria-labelledby={''}",
        ):
            with self.subTest(attribute=attribute):
                f = write(self.tmp, "Form.tsx", f"<input {attribute} type=\"text\" />\n")
                findings = self.mod.run([f])
                self.assertEqual(
                    len(findings), 1,
                    f"{attribute} declares an empty accessible name and must be flagged")

    def test_inputs_inside_source_comments_are_ignored(self):
        commented_inputs = (
            '// <input type="text" />\n',
            '/* <input type="text" /> */\n',
            '{/* <input type="text" /> */}\n',
            '<!-- <input type="text" /> -->\n',
        )
        for index, content in enumerate(commented_inputs):
            with self.subTest(content=content):
                f = write(self.tmp, f"Comment{index}.tsx", content)
                self.assertEqual(
                    self.mod.run([f]), [],
                    "commented-out markup is not a rendered input")

    def test_label_inside_a_comment_does_not_name_a_real_input(self):
        f = write(
            self.tmp,
            "Form.tsx",
            '/* <label htmlFor="e">Email</label> */\n'
            '<input id="e" type="email" />\n',
        )
        findings = self.mod.run([f])
        self.assertEqual(
            len(findings), 1,
            "a commented-out label must not suppress a real unlabeled input")
        self.assertEqual(findings[0]["evidence"][0]["line_start"], 2)

    def test_url_text_in_html_does_not_mask_a_later_input(self):
        f = write(
            self.tmp,
            "Page.html",
            '<p>Documentation: https://example.com</p><input type="text">\n',
        )
        findings = self.mod.run([f])
        self.assertEqual(
            len(findings), 1,
            "HTML text containing // is not a JavaScript line comment")

    def test_hidden_input_type_is_skipped(self):
        f = write(self.tmp, "Form.tsx", '<input type="hidden" value="x" />\n')
        findings = self.mod.run([f])
        self.assertEqual(findings, [])


class TestA11ySelectNoLabel(TempDirCase):
    """Found as a real gap: two AKOS review runs confirmed A11Y_INPUT_NO_LABEL's
    5 leads, then independently flagged unlabeled <select> elements the
    input-only pattern couldn't catch. Shares helpers with
    A11Y_INPUT_NO_LABEL — these tests focus on what's actually different
    (no type= skip list) rather than re-proving the shared logic already
    locked down above."""

    def setUp(self):
        super().setUp()
        self.mod = load_detector("rules/accessibility/a11y-select-no-label.py")

    def test_unlabeled_select_is_flagged(self):
        f = write(self.tmp, "Form.tsx", '<select><option value="a">A</option></select>\n')
        findings = self.mod.run([f])
        self.assertEqual(len(findings), 1)

    def test_jsx_htmlfor_label_is_recognized(self):
        f = write(
            self.tmp, "Form.tsx",
            '<label htmlFor="c">Country</label>\n<select id="c"><option value="es">ES</option></select>\n')
        findings = self.mod.run([f])
        self.assertEqual(findings, [], "htmlFor (JSX convention) must be recognized, not just plain HTML 'for'")

    def test_aria_label_suffices(self):
        f = write(self.tmp, "Form.tsx", '<select aria-label="Country"><option value="es">ES</option></select>\n')
        findings = self.mod.run([f])
        self.assertEqual(findings, [])

    def test_wrapping_label_suffices(self):
        f = write(self.tmp, "Form.tsx", '<label>Country <select><option value="es">ES</option></select></label>\n')
        findings = self.mod.run([f])
        self.assertEqual(findings, [])

    def test_capitalized_select_component_is_not_matched(self):
        # <Select> is a React component; its label almost always comes from
        # its own wrapper, same reasoning as the input detector's case-sensitivity.
        f = write(self.tmp, "Form.tsx", '<Select options={countries} />\n')
        findings = self.mod.run([f])
        self.assertEqual(findings, [])

    def test_select_inside_source_comments_is_ignored(self):
        f = write(self.tmp, "Form.tsx", '{/* <select><option value="a">A</option></select> */}\n')
        findings = self.mod.run([f])
        self.assertEqual(findings, [], "commented-out markup is not a rendered select")

    def test_bracket_in_onchange_does_not_truncate_the_tag(self):
        # Regression proof for the shared tag_span() brace-aware scan: a `>`
        # inside a JSX expression must not truncate the tag before aria-label.
        f = write(
            self.tmp, "Form.tsx",
            '<select aria-label="Country" onChange={(e) => setC(e.target.value)}>'
            '<option value="es">ES</option></select>\n')
        findings = self.mod.run([f])
        self.assertEqual(findings, [], "aria-label after a JSX expression prop must still be seen")


class TestSecretInSource(TempDirCase):
    """Locks down two real bugs: the fixture-path substring match, and
    anon-role JWTs being wrongly flagged as secrets."""

    def setUp(self):
        super().setUp()
        self.mod = load_detector("rules/security/secret-in-source.py")

    def test_aws_vendor_key_flagged(self):
        f = write(self.tmp, "src/config.ts", f'const k = "{AWS_KEY}";\n')
        findings = self.mod.run([f])
        self.assertEqual(len(findings), 1)
        self.assertTrue(findings[0].get("blocking"), "a live vendor key must be blocking")

    def test_secret_in_test_directory_is_still_detected(self):
        # P0-4: a real credential under a test/ segment is still a real
        # credential. The old behavior suppressed the generic branch here;
        # the new contract detects it (path never downgrades or suppresses).
        test_dir = self.tmp / "test" / "src"
        test_dir.mkdir(parents=True)
        f = test_dir / "config.ts"
        import secrets as pysecrets
        token = pysecrets.token_urlsafe(24)
        f.write_text(f'const apiKey = "{token}";\n')
        findings = self.mod.run([f])
        self.assertEqual(len(findings), 1, "a real 'test/' path SEGMENT must not suppress the finding")
        self.assertTrue(findings[0].get("blocking"))

    def test_placeholder_value_not_flagged(self):
        f = write(self.tmp, "src/config.ts", 'const apiKey = "placeholder-not-a-real-key-value";\n')
        findings = self.mod.run([f])
        self.assertEqual(findings, [])

    def test_prefixed_env_var_names_are_caught(self):
        # The real bug: \b never fires between `_` and the keyword (`_` is a
        # word char), so STRIPE_API_KEY / OPENAI_API_KEY / DB_PASSWORD — the
        # dominant naming convention — all sailed past the generic branch.
        import secrets as pysecrets
        for name in ("STRIPE_API_KEY", "SUPABASE_SERVICE_ROLE_KEY", "DB_PASSWORD", "myApiKey"):
            with self.subTest(name=name):
                f = write(self.tmp, f"src/{name}.ts", f'const {name} = "{pysecrets.token_urlsafe(24)}";\n')
                findings = self.mod.run([f])
                self.assertEqual(len(findings), 1, f"{name} must be caught by the generic branch")

    def test_keyword_as_prefix_of_a_longer_word_is_not_matched(self):
        # `secretName`, `tokenizer`: keyword must END the identifier.
        f = write(self.tmp, "src/config.ts",
                  'const tokenizer = "abcdefghijklmnop1234";\nconst secretName = "abcdefghijklmnop1234";\n')
        findings = self.mod.run([f])
        self.assertEqual(findings, [])

    def test_secret_under_any_path_segment_is_detected(self):
        # P0-4: neither an ancestor 'test/' above the scan root nor a 'test/'
        # segment inside it changes the result — the path never downgrades or
        # suppresses a real credential.
        import secrets as pysecrets
        for rel in ("test/proj/src/config.ts", "proj/test/config.ts"):
            with self.subTest(path=rel):
                f = self.tmp / rel
                f.parent.mkdir(parents=True, exist_ok=True)
                token = pysecrets.token_urlsafe(24)
                f.write_text(f'const apiKey = "{token}";\n')
                findings = self.mod.run([f], scan_root=self.tmp)
                self.assertEqual(len(findings), 1,
                                 f"a secret at {rel} must be detected regardless of path")
                self.assertTrue(findings[0].get("blocking"))

    def test_anon_jwt_not_flagged(self):
        import base64
        import json as jsonlib
        h = base64.urlsafe_b64encode(jsonlib.dumps({"alg": "HS256"}).encode()).decode().rstrip("=")
        p = base64.urlsafe_b64encode(jsonlib.dumps({"role": "anon"}).encode()).decode().rstrip("=")
        f = write(self.tmp, "src/config.ts", f'const k = "{h}.{p}.sig1234567890";\n')
        findings = self.mod.run([f])
        self.assertEqual(findings, [], "anon-role keys are designed to be public — RLS constrains them")

    def test_service_role_jwt_flagged_critical(self):
        import base64
        import json as jsonlib
        h = base64.urlsafe_b64encode(jsonlib.dumps({"alg": "HS256"}).encode()).decode().rstrip("=")
        p = base64.urlsafe_b64encode(jsonlib.dumps({"role": "service_role"}).encode()).decode().rstrip("=")
        f = write(self.tmp, "src/config.ts", f'const k = "{h}.{p}.sig1234567890";\n')
        findings = self.mod.run([f])
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["severity_override"], "CRITICAL")

    def test_registry_scans_env_variants_shell_and_common_source_languages(self):
        import runner
        import yaml_subset

        registry = yaml_subset.load(
            paths.AKOS_HOME / "rules/security/secret-in-source.yaml"
        )
        expected_source_files = {
            ".env.local",
            ".env.production",
            "config.sh",
            "config.bash",
            "config.zsh",
            "config.fish",
            "config.ps1",
            "config.mjs",
            "config.cjs",
            "config.go",
            "Config.java",
            "config.rb",
            "config.php",
            "config.rs",
            "Config.kt",
            "Config.kts",
            "Config.swift",
            "Config.cs",
            "config.c",
            "config.h",
            "config.cc",
            "config.cpp",
            "config.hpp",
            "Config.vue",
            "Config.svelte",
            "config.toml",
            "main.tf",
            "secrets.tfvars",
            "config.properties",
            "config.ini",
            "config.conf",
        }
        for filename in expected_source_files | {"asset.png"}:
            write(self.tmp, f"src/{filename}", "placeholder\n")

        collected = {
            path.name
            for path in runner.collect_files(
                self.tmp, registry["applies_to"]["glob"]
            )
        }
        self.assertTrue(expected_source_files <= collected)
        self.assertNotIn(
            "asset.png", collected,
            "the secret rule must remain restricted to text/source formats",
        )


class TestServiceRoleInClient(TempDirCase):
    def setUp(self):
        super().setUp()
        self.mod = load_detector("rules/security/service-role-in-client.py")

    def test_unambiguous_server_convention_paths_are_excluded(self):
        server_paths = (
            "pages/api/admin.ts",
            "app/api/admin/route.ts",
            "supabase/functions/admin/index.ts",
            "src/server/admin.ts",
            "src/admin.server.ts",
            "src/middleware.ts",
        )
        for relative_path in server_paths:
            with self.subTest(path=relative_path):
                f = write(
                    self.tmp,
                    relative_path,
                    "const key = process.env.SUPABASE_SERVICE_ROLE_KEY;\n",
                )
                self.assertEqual(self.mod.run([f], scan_root=self.tmp), [])

    def test_src_api_utility_is_not_assumed_to_be_server_side(self):
        f = write(
            self.tmp,
            "src/api/supabase.ts",
            "const key = process.env.SUPABASE_SERVICE_ROLE_KEY;\n",
        )
        findings = self.mod.run([f], scan_root=self.tmp)
        self.assertEqual(
            len(findings), 1,
            "src/api is commonly a browser API-client layer, not a server boundary",
        )

    def test_only_route_files_under_app_api_are_assumed_server_side(self):
        f = write(
            self.tmp,
            "app/api/supabase.ts",
            "const key = process.env.SUPABASE_SERVICE_ROLE_KEY;\n",
        )
        self.assertEqual(len(self.mod.run([f], scan_root=self.tmp)), 1)

    def test_generic_functions_folder_is_not_assumed_server_side(self):
        f = write(
            self.tmp,
            "src/functions/client.ts",
            "const key = process.env.SUPABASE_SERVICE_ROLE_KEY;\n",
        )
        self.assertEqual(len(self.mod.run([f], scan_root=self.tmp)), 1)

    def test_client_path_flagged(self):
        f = write(self.tmp, "src/client.ts", "const key = process.env.SUPABASE_SERVICE_ROLE_KEY;\n")
        findings = self.mod.run([f])
        self.assertEqual(len(findings), 1)

    def test_camel_case_service_role_identifier_is_flagged(self):
        f = write(
            self.tmp,
            "src/client.ts",
            "const serviceRoleKey = getAdminKey();\n",
        )
        self.assertEqual(len(self.mod.run([f], scan_root=self.tmp)), 1)

    def test_ancestor_api_dir_above_scan_root_does_not_silence(self):
        # The real bug: an ancestor named `api` above the project root made
        # is_server_convention_path true for EVERY file, silencing the rule.
        proj = self.tmp / "api" / "proj"
        f = proj / "src" / "client.ts"
        f.parent.mkdir(parents=True)
        f.write_text("const key = process.env.SUPABASE_SERVICE_ROLE_KEY;\n")
        findings = self.mod.run([f], scan_root=proj)
        self.assertEqual(len(findings), 1,
                         "an ancestor 'api/' ABOVE the scanned root must not classify files as server-side")


class TestCollectFilesSymlinks(TempDirCase):
    """Locks down the symlink escape: scanning an untrusted repository that
    plants a symlink out of its own tree must not read host files."""

    def setUp(self):
        super().setUp()
        # `paths` already puts rules/ on sys.path; a plain import registers the
        # module in sys.modules (which @dataclass in runner.py needs), unlike a
        # bare spec-exec that leaves it unregistered.
        import runner
        self.runner = runner

    def test_symlink_to_outside_file_is_skipped(self):
        outside = self.tmp / "outside"
        outside.mkdir()
        secret = outside / "id_rsa"
        secret.write_text("-----BEGIN OPENSSH PRIVATE KEY-----\n")
        proj = self.tmp / "proj"
        proj.mkdir()
        (proj / "real.ts").write_text("const x = 1;\n")
        (proj / "link.ts").symlink_to(secret)
        files = self.runner.collect_files(proj, ["**/*"])
        self.assertEqual([f.name for f in files], ["real.ts"])

    def test_file_reached_through_a_symlinked_directory_outside_the_tree_is_skipped(self):
        outside = self.tmp / "outside"
        (outside / "sub").mkdir(parents=True)
        (outside / "sub" / "creds.ts").write_text('const k = "x";\n')
        proj = self.tmp / "proj"
        proj.mkdir()
        (proj / "vendor-link").symlink_to(outside, target_is_directory=True)
        files = self.runner.collect_files(proj, ["**/*"])
        self.assertEqual(files, [], "files whose real location is outside the scanned root must be skipped")


class TestDestructiveMigrationNoGuard(TempDirCase):
    """Locks down the real bug: a fixed-width guard window let a comment
    for one statement suppress an unrelated one a few lines later."""

    def setUp(self):
        super().setUp()
        self.mod = load_detector("rules/devops/destructive-migration-no-guard.py")

    def test_guarded_statement_not_flagged(self):
        f = write(self.tmp, "m/0001.sql", "-- reviewed: safe, see PR #1\nDROP TABLE old_thing;\n")
        findings = self.mod.run([f])
        self.assertEqual(findings, [])

    def test_unguarded_statement_flagged(self):
        f = write(self.tmp, "m/0001.sql", "DROP TABLE temp_staging;\n")
        findings = self.mod.run([f])
        self.assertEqual(len(findings), 1)

    def test_guard_does_not_bleed_to_a_later_unrelated_statement(self):
        content = (
            "-- reviewed: column unused since v2\n"
            "ALTER TABLE orders DROP COLUMN legacy_status;\n"
            "\n"
            "DROP TABLE temp_import_staging;\n"
        )
        f = write(self.tmp, "m/0001.sql", content)
        findings = self.mod.run([f])
        self.assertEqual(len(findings), 1, "the guard comment on line 1 must not suppress the unrelated DROP on line 4")
        self.assertEqual(findings[0]["evidence"][0]["line_start"], 4)


class TestSupabasePolicyTooPermissive(TempDirCase):
    """Locks down the real bug: suppression only checked the exact evidence
    line, not the statement's opening line where the comment actually is."""

    def setUp(self):
        super().setUp()
        self.mod = load_detector("rules/security/supabase-policy-too-permissive.py")

    def test_always_true_policy_flagged(self):
        f = write(self.tmp, "schema.sql", 'CREATE POLICY "p" ON t FOR ALL USING (true);\n')
        findings = self.mod.run([f])
        self.assertEqual(len(findings), 1)

    def test_scoped_policy_not_flagged(self):
        f = write(self.tmp, "schema.sql", 'CREATE POLICY "p" ON t FOR ALL USING (auth.uid() = user_id);\n')
        findings = self.mod.run([f])
        self.assertEqual(findings, [])


class TestMigrationNoDownFile(TempDirCase):
    def setUp(self):
        super().setUp()
        self.mod = load_detector("rules/devops/migration-no-down-file.py")

    def test_project_without_the_convention_produces_zero_findings(self):
        f1 = write(self.tmp, "m/0001.sql", "CREATE TABLE a (id uuid);\n")
        f2 = write(self.tmp, "m/0002.sql", "ALTER TABLE a ADD COLUMN b text;\n")
        findings = self.mod.run([f1, f2])
        self.assertEqual(findings, [], "a forward-only project must not be flagged just for lacking down files")

    def test_missing_down_file_flagged_once_convention_adopted(self):
        # NOTE: the down file must be included in the `files` list passed to
        # run() — the detector infers "has this project adopted the
        # convention" from the files it's given, not from a directory scan.
        # (A real bug in this test, not the detector, on first write: the
        # down file was created on disk but omitted from this list, so
        # down_files came back empty and the early-return path fired.)
        f1 = write(self.tmp, "m/0001.up.sql", "CREATE TABLE a (id uuid);\n")
        f1_down = write(self.tmp, "m/0001.down.sql", "DROP TABLE a;\n")
        f2 = write(self.tmp, "m/0002.up.sql", "ALTER TABLE a ADD COLUMN b text;\n")
        findings = self.mod.run([f1, f1_down, f2])
        self.assertEqual(len(findings), 1)
        self.assertIn("0002", findings[0]["evidence"][0]["path"])


class TestPackExpired(TempDirCase):
    def setUp(self):
        super().setUp()
        self.mod = load_detector("rules/meta/pack-expired.py")
        self.mod.AKOS_HOME = self.tmp

    def test_expired_pack_flagged(self):
        f = write(self.tmp, "packs/testing/_fake/metadata.yaml",
                  "name: _fake\ndomain: testing\nid: testing/_fake\nreview_after: 2020-01-01\n")
        findings = self.mod.run([f])
        self.assertEqual(len(findings), 1)
        self.assertIn("overdue", findings[0]["evidence"][0]["snippet"])

    def test_fresh_pack_not_flagged(self):
        f = write(self.tmp, "packs/testing/_fake/metadata.yaml",
                  "name: _fake\ndomain: testing\nid: testing/_fake\nreview_after: 2099-01-01\n")
        findings = self.mod.run([f])
        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()
