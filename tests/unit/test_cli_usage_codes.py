"""Documented CLI usage mistakes return 1, never a findings code."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

AKOS_HOME = Path(__file__).resolve().parents[2]


class TestCliUsageCodes(unittest.TestCase):
    def test_documented_python_commands_use_exit_one_for_bad_flags(self):
        scripts = (
            "schemas/validate.py",
            "schemas/freshness.py",
            "schemas/routing_check.py",
            "benchmarks/runners/run.py",
        )
        for relative in scripts:
            with self.subTest(script=relative):
                proc = subprocess.run(
                    [sys.executable, str(AKOS_HOME / relative), "--not-a-real-flag"],
                    cwd=AKOS_HOME,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(
                    proc.returncode,
                    1,
                    f"{relative} returned {proc.returncode}: {proc.stderr}",
                )


if __name__ == "__main__":
    unittest.main()
