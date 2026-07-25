"""Detection and write-time redaction share the same secret-shape contract."""

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "helpers"))
import paths  # noqa: F401,E402

from secret_utils import redact_secrets  # noqa: E402


AKOS_HOME = Path(paths.AKOS_HOME)


def load_secret_detector():
    path = AKOS_HOME / "rules/security/secret-in-source.py"
    spec = importlib.util.spec_from_file_location("secret_contract_detector", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SecretShapeContractCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.detector = load_secret_detector()

    def tearDown(self):
        self._tmp.cleanup()

    def _detect(self, value: str, filename: str = "config.ts"):
        path = self.root / filename
        path.write_text(value, encoding="utf-8")
        return self.detector.run([path])

    def _assert_detected_and_redacted(self, value: str, expected_label: str, filename="config.ts"):
        findings = self._detect(value, filename)
        self.assertEqual(len(findings), 1, findings)
        redacted, labels = redact_secrets(value)
        self.assertNotIn(value, redacted)
        self.assertIn(expected_label, labels)
        return findings[0]

    def test_openssh_private_key_is_blocking_and_redacted_as_a_complete_block(self):
        private_key = (
            "-----BEGIN " + "OPENSSH PRIVATE KEY-----\n"
            "b3BlbnNzaC1rZXktdjEAAAAAFAKEBUTSHAPEDKEYMATERIAL123456789\n"
            "-----END " + "OPENSSH PRIVATE KEY-----"
        )
        finding = self._assert_detected_and_redacted(
            private_key, "openssh_private_key", "id_ed25519"
        )
        self.assertTrue(finding["blocking"])

    def test_common_pem_private_key_families_are_blocking_and_redacted(self):
        for family, label in (
            ("RSA PRIVATE KEY", "rsa_private_key"),
            ("EC PRIVATE KEY", "ec_private_key"),
            ("PRIVATE KEY", "pkcs8_private_key"),
        ):
            with self.subTest(family=family):
                private_key = (
                    f"-----BEGIN {family}-----\n"
                    "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQ\n"
                    f"-----END {family}-----"
                )
                finding = self._assert_detected_and_redacted(
                    private_key, label, "identity.pem"
                )
                self.assertTrue(finding["blocking"])

    def test_github_fine_grained_pat_is_blocking_and_redacted(self):
        token = "github_" + "pat_11AA22BB33CC" + "44DD55EE66FF77GG88HH"
        finding = self._assert_detected_and_redacted(
            f'const token = "{token}";', "github_fine_grained_pat"
        )
        self.assertTrue(finding["blocking"])

    def test_standalone_entropy_is_nonblocking_but_redacted(self):
        token = "Ax7_" + "qP9mZ2vK8sT4nR6wY3cD5fG7hJ9kL2u"
        source = f'const opaque = "{token}";'
        finding = self._assert_detected_and_redacted(
            source, "standalone_high_entropy"
        )
        self.assertFalse(finding.get("blocking", False))
        self.assertEqual(finding["severity_override"], "MEDIUM")

    def test_generic_assignment_contract_covers_quoted_and_unquoted_values(self):
        token = "Ax7_qP9m" + "Z2vK8sT4" + "nR6wY3cD"
        for rendered_value in (token, f'"{token}"'):
            with self.subTest(rendered_value=rendered_value):
                source = f"MY_API_KEY={rendered_value} # keep this context"
                finding = self._assert_detected_and_redacted(
                    source, "high_entropy_assignment", ".env.local"
                )
                self.assertTrue(finding["blocking"])
                redacted, _ = redact_secrets(source)
                self.assertIn("[REDACTED:high_entropy_assignment]", redacted)
                self.assertIn("# keep this context", redacted)

    def test_quoted_config_keys_share_the_blocking_assignment_contract(self):
        token = "Ax7_qP9m" + "Z2vK8sT4" + "nR6wY3cD"
        for source, filename in (
            (f'{{"apiKey": "{token}"}}', "config.json"),
            (f"'apiKey': '{token}'", "config.yaml"),
        ):
            with self.subTest(filename=filename):
                finding = self._assert_detected_and_redacted(
                    source, "high_entropy_assignment", filename
                )
                self.assertTrue(finding["blocking"])

    def test_dotted_unquoted_env_token_is_detected_and_redacted(self):
        token = "Ax7.qP9m" + "Z2vK8sT4" + "nR6wY3cD"
        source = f"export MY_API_KEY={token}"
        finding = self._assert_detected_and_redacted(
            source, "high_entropy_assignment", ".env.production"
        )
        self.assertTrue(finding["blocking"])

    def test_unquoted_generic_assignment_exclusions_stay_unchanged(self):
        for value in (
            "placeholder-not-a-real-key-value",
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            "${MY_API_KEY}",
        ):
            with self.subTest(value=value):
                source = f"MY_API_KEY={value}"
                self.assertEqual(self._detect(source, ".env.local"), [])
                self.assertEqual(redact_secrets(source), (source, []))

    def test_source_variable_references_are_not_unquoted_secret_literals(self):
        for source in (
            "const token = options.apiToken;",
            "const API_TOKEN = config.API_TOKEN;",
            "const token = someLongCredentialValue;",
        ):
            with self.subTest(source=source):
                self.assertEqual(self._detect(source), [])
                self.assertEqual(redact_secrets(source), (source, []))

    def test_hex_digest_is_not_treated_as_a_standalone_secret(self):
        digest = "0123456789abcdef" * 4
        source = f'const checksum = "{digest}";'
        self.assertEqual(self._detect(source), [])
        redacted, labels = redact_secrets(source)
        self.assertEqual(redacted, source)
        self.assertEqual(labels, [])

    def test_subresource_integrity_hash_is_not_treated_as_a_secret(self):
        integrity = (
            "sha512-"
            "QmFzZTY0UHVibGlj"
            "SW50ZWdyaXR5SGFz"
            "aDEyMzQ1Njc4OTBB"
            "QkNERUY="
        )
        source = f'{{"integrity": "{integrity}"}}'
        self.assertEqual(self._detect(source, "package-lock.json"), [])
        redacted, labels = redact_secrets(source)
        self.assertEqual(redacted, source)
        self.assertEqual(labels, [])


if __name__ == "__main__":
    unittest.main()
