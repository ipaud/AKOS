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
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "helpers"))
import paths  # noqa: F401,E402

AKOS_HOME = Path(paths.AKOS_HOME)

# Assembled at runtime so this file's own source carries no detectable
# credential literal — the repo self-scan stays clean without a path exception
# (P0-4). Each still matches its detector pattern once built.
AWS_KEY = "AKIA" + "ABCDEFGHIJKLMNOP"
# header.payload.sig, payload base64url-decodes to {"role":"service_role"};
# split so the assembled source contains no contiguous JWT literal.
SERVICE_ROLE_JWT = "eyJhbGciOiJIUzI1NiJ9" + "." + "eyJyb2xlIjoic2VydmljZV9yb2xlIn0" + "." + "sig1234567890"


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


class TestSqlDetectorLexing(FixtureCase):
    def setUp(self):
        super().setUp()
        self.sql = load("rules/security/_sql_utils.py")

    def test_statement_splitter_ignores_semicolons_inside_sql_literals(self):
        source = (
            "select ';--not a comment'; /* real; comment */\n"
            "select $$body; -- still body$$;\n"
            "select 1"
        )
        statements = list(self.sql.iter_sql_statements(source))
        self.assertEqual(len(statements), 3)
        self.assertIn("--not a comment", statements[0][1])
        self.assertIn("-- still body", statements[1][1])
        self.assertEqual(statements[2][1].strip(), "select 1")

    def test_standard_string_backslash_does_not_escape_closing_quote(self):
        source = (
            "select 'C:\\';\n"
            "create table public.notes (id uuid primary key);"
        )
        statements = list(self.sql.iter_sql_statements(source))
        self.assertEqual(len(statements), 2)
        self.assertIn("create table public.notes", statements[1][1])

    def test_escape_string_backslash_still_escapes_a_quote(self):
        source = r"select E'it\'s; data'; select 1;"
        statements = list(self.sql.iter_sql_statements(source))
        self.assertEqual(len(statements), 2)
        self.assertIn(r"E'it\'s; data'", statements[0][1])

    def test_unicode_escape_string_keeps_an_internal_semicolon(self):
        source = r"select U&'d\0061t\0061; value'; select 1;"
        statements = list(self.sql.iter_sql_statements(source))
        self.assertEqual(len(statements), 2)
        self.assertIn(r"U&'d\0061t\0061; value'", statements[0][1])


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
        f = self.write(".env", f"SECRET={AWS_KEY}\n")
        self.assertEqual(self.rule.run([f]), [])

    def test_the_same_secret_in_tracked_source_is_reported(self):
        f = self.write("src/config.ts", f'export const K = "{AWS_KEY}";\n')
        self.assertEqual(len(self.rule.run([f])), 1)


if __name__ == "__main__":
    unittest.main()


class TestA11yMatchesElementsNotComponents(FixtureCase):
    """`<input\\b` with IGNORECASE matched `<Input>` — the React component,
    which JSX capitalises precisely to distinguish it from the element. On a
    design-system codebase 110 of 122 findings pointed at components, burying
    the 12 genuine `<input>` elements underneath them."""

    def setUp(self):
        super().setUp()
        self.rule = load("rules/accessibility/a11y-input-no-label.py")

    def test_capitalised_component_is_not_an_html_input(self):
        f = self.write("Form.tsx",
                       '<Field label="Nom comercial">\n'
                       '  <Input placeholder="Ex: Tech" {...register("name")} />\n'
                       "</Field>\n")
        self.assertEqual(self.rule.run([f]), [])

    def test_lowercase_html_input_is_still_reported(self):
        f = self.write("Form.tsx", '<input type="text" placeholder="Name" />\n')
        self.assertEqual(len(self.rule.run([f])), 1)


class TestCommentsAreNotEvidence(FixtureCase):
    """Two detectors reported their own warning text. The one that flagged
    `src/lib/supabase.ts` matched a comment reading 'A service_role key must
    NEVER be a VITE_* variable' — the warning against the defect, read as the
    defect."""

    def test_service_role_in_a_comment_is_not_a_finding(self):
        rule = load("rules/security/service-role-in-client.py")
        f = self.write("src/lib/supabase.ts",
                       "/**\n"
                       " * Only the anon key belongs here. A service_role key\n"
                       " * must NEVER be a VITE_* variable.\n"
                       " */\n"
                       "export const client = createClient(url, anonKey);\n")
        self.assertEqual(rule.run([f]), [])

    def test_service_role_in_real_code_is_still_reported(self):
        rule = load("rules/security/service-role-in-client.py")
        f = self.write("src/lib/admin.ts",
                       'const key = import.meta.env.VITE_SERVICE_ROLE_KEY;\n')
        self.assertEqual(len(rule.run([f])), 1)

    def test_drop_column_inside_a_comment_is_not_a_finding(self):
        rule = load("rules/devops/destructive-migration-no-guard.py")
        f = self.write("migrations/001.sql",
                       "-- PLANNED DEBT: a later migration must do\n"
                       "--   alter table requests drop column \"date\";\n"
                       "create table notes (id uuid primary key);\n")
        self.assertEqual(rule.run([f]), [])

    def test_a_real_drop_outside_a_comment_is_still_reported(self):
        rule = load("rules/devops/destructive-migration-no-guard.py")
        f = self.write("migrations/001.sql", "drop table activity_log;\n")
        self.assertEqual(len(rule.run([f])), 1)


class TestRlsDetectorUnderstandsDynamicSql(FixtureCase):
    """RLS enabled by `execute format(...)` over an array literal is stronger
    than per-table DDL — a table added to the list cannot be half-protected.
    The detector could not see it and reported 31 CRITICALs on a real
    repository against tables protected exactly that way."""

    def setUp(self):
        super().setUp()
        self.rule = load("rules/security/supabase-rls-disabled.py")

    LOOP = (
        "do $$\ndeclare t text;\nbegin\n"
        "  foreach t in array array['clients','contacts'] loop\n"
        "    execute format('alter table %I enable row level security;', t);\n"
        "  end loop;\nend $$;\n"
    )

    def test_tables_in_the_loop_array_are_not_reported(self):
        f = self.write("001.sql",
                       "create table clients (id uuid primary key);\n"
                       "create table contacts (id uuid primary key);\n" + self.LOOP)
        self.assertEqual(self.rule.run([f]), [])

    def test_a_table_outside_the_loop_array_is_still_reported(self):
        """The fix must not become a blanket amnesty for any file that
        happens to contain a dynamic-RLS loop."""
        f = self.write("001.sql",
                       "create table clients (id uuid primary key);\n"
                       "create table forgotten (id uuid primary key);\n" + self.LOOP)
        findings = self.rule.run([f])
        self.assertEqual(len(findings), 1)
        self.assertIn("forgotten", findings[0]["evidence"][0]["snippet"])

    def test_an_unrelated_array_is_not_attributed_to_the_rls_loop(self):
        unrelated_array = (
            "do $$\ndeclare t text;\nbegin\n"
            "  perform archive_tables(array['forgotten']);\n"
            "  foreach t in array array['clients'] loop\n"
            "    execute format("
            "'alter table %I enable row level security;', t);\n"
            "  end loop;\nend $$;\n"
        )
        f = self.write(
            "001.sql",
            "create table clients (id uuid primary key);\n"
            "create table forgotten (id uuid primary key);\n"
            + unrelated_array,
        )
        findings = self.rule.run([f])
        self.assertEqual(len(findings), 1)
        self.assertIn("forgotten", findings[0]["evidence"][0]["snippet"])

    def test_format_variable_must_occupy_the_table_identifier(self):
        misleading_loop = (
            "do $$\ndeclare t text;\nbegin\n"
            "  foreach t in array array['clients','contacts'] loop\n"
            "    execute format("
            "'alter table audit_log enable row level security /* %I */;', t);\n"
            "  end loop;\nend $$;\n"
        )
        f = self.write(
            "001.sql",
            "create table clients (id uuid primary key);\n"
            "create table contacts (id uuid primary key);\n"
            + misleading_loop,
        )
        findings = self.rule.run([f])
        self.assertEqual(len(findings), 2)

    def test_single_identifier_placeholder_rejects_qualified_array_values(self):
        qualified_loop = (
            "do $$\ndeclare t text;\nbegin\n"
            "  foreach t in array array['public.clients'] loop\n"
            "    execute format("
            "'alter table %I enable row level security;', t);\n"
            "  end loop;\nend $$;\n"
        )
        f = self.write(
            "001.sql",
            "create table public.clients (id uuid primary key);\n"
            + qualified_loop,
        )
        self.assertEqual(len(self.rule.run([f])), 1)

    def test_no_dynamic_loop_means_normal_behaviour(self):
        f = self.write("001.sql", "create table public.notes (id uuid primary key);\n")
        self.assertEqual(len(self.rule.run([f])), 1)


class TestSecretsBlockOnEveryPath(FixtureCase):
    """P0-4: a realistic credential is dangerous wherever it lives. The path
    (tests/, fixtures/, docs/) may color the evidence note, but it never
    downgrades or suppresses the finding — a live vendor key or a service_role
    JWT stays blocking from a test file exactly as from shipping source. AKOS's
    own corpus stays clean by keeping realistic values out of version control
    (materialized at scan time), not by a path exception here."""

    def setUp(self):
        super().setUp()
        self.rule = load("rules/security/secret-in-source.py")

    AWS = f'export const K = "{AWS_KEY}";\n'
    SERVICE_JWT = f'const k = "{SERVICE_ROLE_JWT}";\n'

    def _one(self, rel: str, body: str):
        f = self.write(rel, body)
        findings = self.rule.run([f])
        self.assertEqual(len(findings), 1, f"expected exactly one finding for {rel}")
        return findings[0]

    def test_vendor_key_in_source_is_blocking(self):
        f = self._one("src/config.ts", self.AWS)
        self.assertNotEqual(f.get("severity_override"), "LOW")
        self.assertTrue(f.get("blocking"))

    def test_vendor_key_in_fixture_is_not_downgraded_to_low(self):
        f = self._one("tests/fixture.ts", self.AWS)
        self.assertNotEqual(f.get("severity_override"), "LOW")
        self.assertTrue(f.get("blocking"), "a live vendor key in a fixture path is still blocking")

    def test_service_role_jwt_in_source_is_critical(self):
        f = self._one("src/client.ts", self.SERVICE_JWT)
        self.assertEqual(f.get("severity_override"), "CRITICAL")
        self.assertTrue(f.get("blocking"))

    def test_service_role_jwt_in_fixture_remains_critical(self):
        f = self._one("tests/fixture.ts", self.SERVICE_JWT)
        self.assertEqual(f.get("severity_override"), "CRITICAL")
        self.assertTrue(f.get("blocking"))

    def test_secret_in_docs_remains_blocking(self):
        f = self._one("docs/example.ts", self.AWS)
        self.assertTrue(f.get("blocking"), "a real key in a docs path is still blocking")

    def test_secret_in_fixture_remains_blocking(self):
        """The load-bearing half: not silenced, and still gates."""
        f = self._one("tests/fixture.ts", self.AWS)
        self.assertTrue(f.get("blocking"))


class TestRlsDetectorUnderstandsRevokeAll(FixtureCase):
    """A table closed by revoking every API-reachable role is stronger than
    one behind a policy — there is nothing to mis-write later. Reporting it
    as "no RLS" is a false positive on code more locked down than the rule's
    own happy path. Documented as a known gap when the schema fix landed;
    closed here."""

    def setUp(self):
        super().setUp()
        self.rule = load("rules/security/supabase-rls-disabled.py")

    def test_table_revoked_from_every_api_role_is_not_reported(self):
        f = self.write("001.sql",
                       "create table public.app_secrets (name text primary key);\n"
                       "revoke all on table public.app_secrets from public, anon, authenticated;\n")
        self.assertEqual(self.rule.run([f]), [])

    def test_a_partial_revoke_is_still_reported(self):
        """One role revoked is not the same as closed. The rule must not
        read a half-measure as a full one."""
        f = self.write("001.sql",
                       "create table public.half_open (id uuid primary key);\n"
                       "revoke all on table public.half_open from anon;\n")
        self.assertEqual(len(self.rule.run([f])), 1)

    def test_an_unrelated_revoke_does_not_cover_another_table(self):
        f = self.write("001.sql",
                       "create table public.exposed (id uuid primary key);\n"
                       "revoke all on table public.other from public, anon, authenticated;\n")
        findings = self.rule.run([f])
        self.assertEqual(len(findings), 1)
        self.assertIn("exposed", findings[0]["evidence"][0]["snippet"])


class TestRlsDetectorTracksFinalDatabaseState(FixtureCase):
    """The final state wins: later DDL can undo an earlier safe state."""

    def setUp(self):
        super().setUp()
        self.rule = load("rules/security/supabase-rls-disabled.py")

    def test_rls_disabled_after_enable_is_reported(self):
        f = self.write(
            "supabase/migrations/001.sql",
            "create table public.notes (id uuid primary key);\n"
            "alter table public.notes enable row level security;\n"
            "alter table public.notes disable row level security;\n",
        )
        findings = self.rule.run([f], self.dir)
        self.assertEqual(len(findings), 1)
        self.assertIn("public.notes", findings[0]["evidence"][0]["snippet"])

    def test_create_evidence_line_ignores_leading_statement_whitespace(self):
        f = self.write(
            "supabase/migrations/001.sql",
            "create schema private;\n\n"
            "create table public.notes (id uuid primary key);\n",
        )
        finding = self.rule.run([f], self.dir)[0]
        self.assertEqual(finding["evidence"][0]["line_start"], 3)

    def test_drop_and_recreate_resets_rls_state(self):
        f = self.write(
            "supabase/migrations/001.sql",
            "create table public.notes (id uuid primary key);\n"
            "alter table public.notes enable row level security;\n"
            "drop table public.notes;\n"
            "create table public.notes (id uuid primary key);\n",
        )
        self.assertEqual(len(self.rule.run([f], self.dir)), 1)

    def test_grant_after_revoke_reopens_the_table(self):
        f = self.write(
            "supabase/migrations/001.sql",
            "create table public.notes (id uuid primary key);\n"
            "revoke all on table public.notes from public, anon, authenticated;\n"
            "grant select on table public.notes to authenticated;\n",
        )
        self.assertEqual(len(self.rule.run([f], self.dir)), 1)

    def test_revoke_of_the_only_later_grant_locks_the_table_again(self):
        f = self.write(
            "supabase/migrations/001.sql",
            "create table public.notes (id uuid primary key);\n"
            "revoke all on table public.notes from public, anon, authenticated;\n"
            "grant select on table public.notes to authenticated;\n"
            "revoke select on table public.notes from authenticated;\n",
        )
        self.assertEqual(self.rule.run([f], self.dir), [])

    def test_schema_wide_grant_reopens_an_existing_revoked_table(self):
        f = self.write(
            "supabase/migrations/001.sql",
            "create table public.notes (id uuid primary key);\n"
            "revoke all on table public.notes from public, anon, authenticated;\n"
            "grant select on all tables in schema public to authenticated;\n",
        )
        self.assertEqual(len(self.rule.run([f], self.dir)), 1)

    def test_schema_wide_revoke_can_remove_a_schema_wide_grant(self):
        f = self.write(
            "supabase/migrations/001.sql",
            "create table public.notes (id uuid primary key);\n"
            "revoke all on table public.notes from public, anon, authenticated;\n"
            "grant select on all tables in schema public to authenticated;\n"
            "revoke select on all tables in schema public from authenticated;\n",
        )
        self.assertEqual(self.rule.run([f], self.dir), [])

    def test_non_data_grant_does_not_reopen_the_api_table(self):
        f = self.write(
            "supabase/migrations/001.sql",
            "create table public.notes (id uuid primary key);\n"
            "revoke all on table public.notes from public, anon, authenticated;\n"
            "grant trigger, references on all tables in schema public "
            "to authenticated;\n",
        )
        self.assertEqual(self.rule.run([f], self.dir), [])

    def test_alter_table_only_enables_rls(self):
        f = self.write(
            "supabase/migrations/001.sql",
            "create table public.notes (id uuid primary key);\n"
            "alter table if exists only public.notes enable row level security;\n",
        )
        self.assertEqual(self.rule.run([f], self.dir), [])

    def test_drop_table_list_removes_every_dropped_table(self):
        f = self.write(
            "supabase/migrations/001.sql",
            "create table public.notes (id uuid primary key);\n"
            "create table public.drafts (id uuid primary key);\n"
            "drop table public.notes, public.drafts;\n",
        )
        self.assertEqual(self.rule.run([f], self.dir), [])

    def test_rls_on_same_named_private_table_does_not_cover_public_table(self):
        f = self.write(
            "supabase/migrations/001.sql",
            "create schema private;\n"
            "create table public.notes (id uuid primary key);\n"
            "create table private.notes (id uuid primary key);\n"
            "alter table private.notes enable row level security;\n",
        )
        findings = self.rule.run([f], self.dir)
        self.assertEqual(len(findings), 1)
        self.assertIn("public.notes", findings[0]["evidence"][0]["snippet"])

    def test_custom_exposed_schema_is_loaded_from_supabase_config(self):
        self.write(
            "supabase/config.toml",
            '[api]\nschemas = ["public", "tenant_api"]\n',
        )
        f = self.write(
            "supabase/migrations/001.sql",
            "create table tenant_api.notes (id uuid primary key);\n",
        )
        findings = self.rule.run([f], self.dir)
        self.assertEqual(len(findings), 1)
        self.assertIn("tenant_api.notes", findings[0]["evidence"][0]["snippet"])

    def test_unreadable_supabase_config_fails_closed(self):
        config = self.write(
            "supabase/config.toml",
            '[api]\nschemas = ["public"]\n',
        )
        migration = self.write(
            "supabase/migrations/001.sql",
            "create table public.notes (id uuid primary key);\n",
        )
        original_read_text = Path.read_text

        def fail_config_read(path, *args, **kwargs):
            if path == config:
                raise PermissionError("simulated unreadable Supabase config")
            return original_read_text(path, *args, **kwargs)

        with mock.patch.object(Path, "read_text", fail_config_read):
            with self.assertRaises(PermissionError):
                self.rule.run([migration], self.dir)

    def test_symlinked_supabase_config_is_rejected(self):
        outside = self.dir / "outside-config.toml"
        outside.write_text('[api]\nschemas = ["private_host_schema"]\n')
        config = self.dir / "supabase" / "config.toml"
        config.parent.mkdir()
        config.symlink_to(outside)
        migration = self.write(
            "supabase/migrations/001.sql",
            "create table public.notes (id uuid primary key);\n",
        )

        with self.assertRaises(OSError):
            self.rule.run([migration], self.dir)

    def test_quoted_custom_schema_keeps_its_exact_identity(self):
        self.write(
            "supabase/config.toml",
            '[api]\nschemas = ["tenant-api"]\n',
        )
        f = self.write(
            "supabase/migrations/001.sql",
            'create table "tenant-api".notes (id uuid primary key);\n',
        )
        findings = self.rule.run([f], self.dir)
        self.assertEqual(len(findings), 1)
        self.assertIn('"tenant-api".notes', findings[0]["evidence"][0]["snippet"])


class TestPolicyDetectorTracksAlterPolicy(FixtureCase):
    """CREATE/ALTER/DROP are folded into the policy's final definition."""

    def setUp(self):
        super().setUp()
        self.rule = load("rules/security/supabase-policy-too-permissive.py")

    def test_alter_policy_can_make_a_safe_policy_permissive(self):
        f = self.write(
            "001.sql",
            "create policy p on public.notes for select "
            "using (owner_id = auth.uid());\n"
            "alter policy p on public.notes using (true);\n",
        )
        findings = self.rule.run([f])
        self.assertEqual(len(findings), 1)
        self.assertIn("using (true)", findings[0]["evidence"][0]["snippet"].lower())

    def test_create_policy_detects_numeric_tautology(self):
        f = self.write(
            "001.sql",
            "create policy p on public.notes for select using (1 = 1);\n",
        )
        findings = self.rule.run([f])
        self.assertEqual(len(findings), 1)
        self.assertIn("1 = 1", findings[0]["evidence"][0]["snippet"])

    def test_with_check_detects_numeric_tautology(self):
        f = self.write(
            "001.sql",
            "create policy p on public.notes for insert with check (1=1);\n",
        )
        self.assertEqual(len(self.rule.run([f])), 1)

    def test_redundant_parentheses_do_not_hide_tautologies(self):
        using = self.write(
            "001.sql",
            "create policy p on public.notes for select using (((1 = 1)));\n",
        )
        check = self.write(
            "002.sql",
            "create policy q on public.notes for insert "
            "with check ((((true))));\n",
        )
        self.assertEqual(len(self.rule.run([using, check])), 2)

    def test_true_or_predicate_is_always_permissive(self):
        f = self.write(
            "001.sql",
            "create policy p on public.notes for select "
            "using (true OR auth.uid() = user_id);\n",
        )
        self.assertEqual(len(self.rule.run([f])), 1)

    def test_predicate_or_numeric_tautology_is_always_permissive(self):
        f = self.write(
            "001.sql",
            "create policy p on public.notes for insert "
            "with check ((owner_id = auth.uid()) OR ((1 = 1)));\n",
        )
        self.assertEqual(len(self.rule.run([f])), 1)

    def test_alter_policy_tracks_compound_tautology_final_state(self):
        f = self.write(
            "001.sql",
            "create policy p on public.notes for select "
            "using (owner_id = auth.uid());\n"
            "alter policy p on public.notes "
            "using (owner_id = auth.uid() or true);\n",
        )
        self.assertEqual(len(self.rule.run([f])), 1)

    def test_alter_policy_can_tighten_compound_tautology(self):
        f = self.write(
            "001.sql",
            "create policy p on public.notes for select "
            "using (true or owner_id = auth.uid());\n"
            "alter policy p on public.notes "
            "using (owner_id = auth.uid());\n",
        )
        self.assertEqual(self.rule.run([f]), [])

    def test_non_constant_boolean_combinations_are_not_reported(self):
        f = self.write(
            "001.sql",
            "create policy p on public.notes for select "
            "using (false OR owner_id = auth.uid());\n"
            "create policy q on public.notes for select "
            "using (true AND owner_id = auth.uid());\n",
        )
        self.assertEqual(self.rule.run([f]), [])

    def test_boolean_words_inside_strings_are_not_operators(self):
        f = self.write(
            "001.sql",
            "create policy p on public.notes for select "
            "using (message = 'true OR )' OR false);\n",
        )
        self.assertEqual(self.rule.run([f]), [])

    def test_boolean_words_inside_dollar_strings_are_not_operators(self):
        f = self.write(
            "001.sql",
            "create policy p on public.notes for select "
            "using (message = $$x OR true)$$);\n"
            "create policy q on public.notes for select "
            "using (message = $tag$x OR true)$tag$);\n",
        )
        self.assertEqual(self.rule.run([f]), [])

    def test_incomplete_boolean_expression_fails_safe(self):
        f = self.write(
            "001.sql",
            "create policy p on public.notes for select using (true OR);\n",
        )
        self.assertEqual(self.rule.run([f]), [])

    def test_alter_policy_can_make_a_safe_policy_numeric_tautology(self):
        f = self.write(
            "001.sql",
            "create policy p on public.notes for select "
            "using (owner_id = auth.uid());\n"
            "alter policy p on public.notes using (1=1);\n",
        )
        self.assertEqual(len(self.rule.run([f])), 1)

    def test_alter_policy_can_tighten_a_numeric_tautology(self):
        f = self.write(
            "001.sql",
            "create policy p on public.notes for select using (1=1);\n"
            "alter policy p on public.notes using (owner_id = auth.uid());\n",
        )
        self.assertEqual(self.rule.run([f]), [])

    def test_non_tautological_numeric_comparison_is_not_reported(self):
        f = self.write(
            "001.sql",
            "create policy p on public.notes for select using (attempts = 1);\n",
        )
        self.assertEqual(self.rule.run([f]), [])

    def test_parentheses_inside_quoted_values_are_not_clause_boundaries(self):
        f = self.write(
            "001.sql",
            "create policy p on public.notes for select "
            "using (label = 'not ) ''true''');\n"
            'create policy q on public.notes for select '
            'using ("field)""quoted" = 1);\n',
        )
        self.assertEqual(self.rule.run([f]), [])

    def test_non_redundant_parentheses_are_not_stripped(self):
        f = self.write(
            "001.sql",
            "create policy p on public.notes for select "
            "using ((attempts = 1) and active);\n",
        )
        self.assertEqual(self.rule.run([f]), [])

    def test_unclosed_policy_expression_fails_safe(self):
        f = self.write(
            "001.sql",
            "create policy p on public.notes for select using (true",
        )
        self.assertEqual(self.rule.run([f]), [])

    def test_alter_policy_can_tighten_a_permissive_policy(self):
        f = self.write(
            "001.sql",
            "create policy p on public.notes for select using (true);\n"
            "alter policy p on public.notes using (owner_id = auth.uid());\n",
        )
        self.assertEqual(self.rule.run([f]), [])

    def test_altering_one_clause_preserves_other_live_true_clause(self):
        f = self.write(
            "001.sql",
            "create policy p on public.notes for all "
            "using (true) with check (true);\n"
            "alter policy p on public.notes "
            "with check (owner_id = auth.uid());\n",
        )
        self.assertEqual(len(self.rule.run([f])), 1)

    def test_final_statement_without_semicolon_is_processed(self):
        f = self.write(
            "001.sql",
            "create policy p on public.notes for select using (true)",
        )
        self.assertEqual(len(self.rule.run([f])), 1)

    def test_quoted_policy_and_table_names_are_tracked(self):
        f = self.write(
            "001.sql",
            'create policy "Public read" on public."Release Notes" '
            "for select using (true);\n"
            'create policy "Public read" on public."Internal Notes" '
            "for select using (owner_id = auth.uid());\n",
        )
        self.assertEqual(len(self.rule.run([f])), 1)

    def test_standard_string_backslash_does_not_hide_a_later_policy(self):
        f = self.write(
            "001.sql",
            "select 'C:\\';\n"
            "create policy p on public.notes for select using (true);\n",
        )
        self.assertEqual(len(self.rule.run([f])), 1)


class TestRunnerDoesNotDowngradeByPath(FixtureCase):
    """P0-4: the runner used to downgrade every finding under a fixture/tests/
    doc path to LOW, centrally, for every rule — so a real migration or a real
    credential parked under tests/ stopped gating. That path-based downgrade is
    gone: severity comes from the rule and the evidence, never the directory."""

    def setUp(self):
        super().setUp()
        sys.path.insert(0, str(AKOS_HOME / "rules"))
        import runner
        self.runner = runner

    def _findings(self, rel: str, body: str, rule_id: str):
        self.write(rel, body)
        rules = list(self.runner.discover_rules(rule_filter={rule_id}))
        return self.runner.run_rules(self.dir, rules, "Production")

    def test_real_migration_path_keeps_its_severity(self):
        sev = [f["severity"] for f in self._findings(
            "supabase/migrations/001.sql",
            "create table public.notes (id uuid primary key);\n", "SUPABASE_RLS_DISABLED")]
        self.assertEqual(sev, ["CRITICAL"])

    def test_fixture_path_keeps_full_severity(self):
        # Previously downgraded to LOW; now the path does not vote.
        sev = [f["severity"] for f in self._findings(
            "tests/fixtures/001.sql",
            "create table public.notes (id uuid primary key);\n", "SUPABASE_RLS_DISABLED")]
        self.assertEqual(sev, ["CRITICAL"])

    def test_akos_self_scan_does_not_depend_on_path_based_secret_downgrades(self):
        """A service_role JWT under a tests/ path stays CRITICAL and blocking
        through the runner — the exact case the central downgrade used to
        hide."""
        findings = self._findings(
            "tests/fixtures/config.ts", f'const k = "{SERVICE_ROLE_JWT}";\n', "SECRET_IN_SOURCE")
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["severity"], "CRITICAL")
        self.assertTrue(findings[0].get("blocking"))
