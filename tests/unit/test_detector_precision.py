"""Precision regressions found by running the detectors on a real repository.

Every case here is a shape that produced a false positive on the first real
project scanned — a well-built Supabase app where all nine Level-A findings
turned out to be wrong. The benchmark suite reported precision 100% at the
same time, measured against synthetic fixtures written by the same process
that wrote the detectors. These fixtures are copied from real code instead.
"""

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "helpers"))
import paths  # noqa: F401,E402

AKOS_HOME = Path(paths.AKOS_HOME)


def load(rel: str):
    spec = importlib.util.spec_from_file_location(Path(rel).stem, AKOS_HOME / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class FixtureCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def write(self, name: str, body: str) -> Path:
        p = self.dir / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body, encoding="utf-8")
        return p


class TestPolicyDetectorIsMigrationOrderAware(FixtureCase):
    """Two of six findings named policies a later migration had dropped."""

    def setUp(self):
        super().setUp()
        self.rule = load("rules/security/supabase-policy-too-permissive.py")

    def test_policy_dropped_by_a_later_migration_is_not_reported(self):
        a = self.write("001_init.sql",
                       'CREATE POLICY "Cache writable" ON public.cache\n'
                       '  FOR INSERT TO authenticated WITH CHECK (true);\n')
        b = self.write("002_fix.sql",
                       'DROP POLICY IF EXISTS "Cache writable" ON public.cache;\n')
        self.assertEqual(self.rule.run([a, b]), [])

    def test_a_live_permissive_policy_is_still_reported(self):
        a = self.write("001_init.sql",
                       'CREATE POLICY "Everything" ON public.secrets\n'
                       '  FOR SELECT TO authenticated USING (true);\n')
        self.assertEqual(len(self.rule.run([a])), 1)

    def test_recreated_without_the_permissive_clause_is_not_reported(self):
        a = self.write("001.sql", 'CREATE POLICY "P" ON public.t FOR SELECT USING (true);\n')
        b = self.write("002.sql", 'DROP POLICY "P" ON public.t;\n'
                                  'CREATE POLICY "P" ON public.t FOR SELECT USING (user_id = auth.uid());\n')
        self.assertEqual(self.rule.run([a, b]), [])

    def test_a_drop_on_a_different_table_does_not_clear_it(self):
        a = self.write("001.sql", 'CREATE POLICY "P" ON public.a FOR SELECT USING (true);\n')
        b = self.write("002.sql", 'DROP POLICY "P" ON public.b;\n')
        self.assertEqual(len(self.rule.run([a, b])), 1)


class TestRlsDetectorSkipsNonExposedSchemas(FixtureCase):
    """`CREATE TABLE IF NOT EXISTS private.app_secrets` was parsed as table
    `private` and reported CRITICAL — for a secrets table deliberately kept
    out of the API and protected with REVOKE ALL, which is stronger than the
    RLS it was accused of lacking."""

    def setUp(self):
        super().setUp()
        self.rule = load("rules/security/supabase-rls-disabled.py")

    def test_table_in_a_private_schema_is_not_reported(self):
        f = self.write("001.sql",
                       "CREATE SCHEMA IF NOT EXISTS private;\n"
                       "CREATE TABLE IF NOT EXISTS private.app_secrets (name text PRIMARY KEY);\n"
                       "REVOKE ALL ON TABLE private.app_secrets FROM PUBLIC, anon, authenticated;\n")
        self.assertEqual(self.rule.run([f]), [])

    def test_public_table_without_rls_is_still_reported(self):
        f = self.write("001.sql", "CREATE TABLE public.notes (id uuid PRIMARY KEY);\n")
        self.assertEqual(len(self.rule.run([f])), 1)

    def test_schema_qualified_public_table_is_matched_by_its_own_name(self):
        """The old pattern only stripped a literal `public.`; anything else
        collapsed to the schema name, so RLS enabled on the real table did
        not match the create."""
        f = self.write("001.sql",
                       "CREATE TABLE IF NOT EXISTS public.notes (id uuid PRIMARY KEY);\n"
                       "ALTER TABLE public.notes ENABLE ROW LEVEL SECURITY;\n")
        self.assertEqual(self.rule.run([f]), [])


class TestDestructiveGuardAcceptsDataPreservation(FixtureCase):
    """The guard was an `INSERT ... SELECT` moving the data one statement
    above the DROP — expand-contract done correctly — but only a *comment*
    counted, so it was reported."""

    def setUp(self):
        super().setUp()
        self.rule = load("rules/devops/destructive-migration-no-guard.py")

    def test_column_copied_before_the_drop_is_guarded(self):
        f = self.write("migrations/001.sql",
                       "INSERT INTO backup (id, email) SELECT id, email FROM users;\n\n"
                       "ALTER TABLE users DROP COLUMN email;\n")
        self.assertEqual(self.rule.run([f]), [])

    def test_an_unrelated_insert_above_does_not_count(self):
        f = self.write("migrations/001.sql",
                       "INSERT INTO archive (id) SELECT id FROM other_table;\n\n"
                       "ALTER TABLE users DROP COLUMN email;\n")
        self.assertEqual(len(self.rule.run([f])), 1)

    def test_a_bare_drop_is_still_reported(self):
        f = self.write("migrations/001.sql", "ALTER TABLE users DROP COLUMN email;\n")
        self.assertEqual(len(self.rule.run([f])), 1)


class TestA11yMatcherHandlesMultilineJsx(FixtureCase):
    """8 of 21 findings were correctly-labelled inputs. `[^>]*` stopped at
    the `>` inside `onChange={(e) => ...}`, truncating the tag before the
    aria-label."""

    def setUp(self):
        super().setUp()
        self.rule = load("rules/accessibility/a11y-input-no-label.py")

    def test_aria_label_after_an_arrow_function_prop_is_seen(self):
        f = self.write("C.tsx",
                       "<input\n"
                       "  value={q}\n"
                       "  onChange={(e) => setQ(e.target.value)}\n"
                       '  type="search"\n'
                       '  aria-label="Search friends"\n'
                       "/>\n")
        self.assertEqual(self.rule.run([f]), [])

    def test_an_input_with_only_a_placeholder_is_still_reported(self):
        f = self.write("C.tsx",
                       "<input\n"
                       "  onChange={(e) => setQ(e.target.value)}\n"
                       '  placeholder="Search"\n'
                       "/>\n")
        self.assertEqual(len(self.rule.run([f])), 1)


class TestSecretDetectorRespectsGitignore(FixtureCase):
    """A `service_role` key in a gitignored `.env` is in the one place it
    belongs. The rule is titled "committed to source"; that file is not."""

    def setUp(self):
        super().setUp()
        self.rule = load("rules/security/secret-in-source.py")
        import subprocess
        subprocess.run(["git", "init", "-q"], cwd=self.dir, check=True)
        (self.dir / ".gitignore").write_text(".env\n")

    def test_secret_in_a_gitignored_env_is_not_reported(self):
        f = self.write(".env", "SECRET=AKIAABCDEFGHIJKLMNOP\n")
        self.assertEqual(self.rule.run([f]), [])

    def test_the_same_secret_in_tracked_source_is_reported(self):
        f = self.write("src/config.ts", 'export const K = "AKIAABCDEFGHIJKLMNOP";\n')
        self.assertEqual(len(self.rule.run([f])), 1)


if __name__ == "__main__":
    unittest.main()
