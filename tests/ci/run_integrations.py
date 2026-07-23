#!/usr/bin/env python3
"""Run every Bash integration test from a Python parent.

The Python parent is intentional: coverage.py's subprocess patch can propagate
measurement through Bash to the Python commands those integrations exercise.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path


JSON_CAPTURE_SENSITIVE_TESTS = {
    "test_update_preserves_personal.sh",
    "test_version_freshness.sh",
}


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--coverage",
        action="store_true",
        help="measure Python files launched through AKOS_PYTHON_BIN",
    )
    parser.add_argument(
        "--pattern",
        default="test_*.sh",
        help="integration filename glob (default: test_*.sh)",
    )
    return parser


def _coverage_python(directory: Path) -> Path:
    wrapper = directory / "python-with-coverage"
    wrapper.write_text(
        f"#!{sys.executable}\n"
        "import os, platform, sys\n"
        "if sys.argv[1:] == ['--version']:\n"
        "    print('Python ' + platform.python_version())\n"
        "    raise SystemExit(0)\n"
        "if sys.argv[1:2] in (['-c'], ['-']):\n"
        "    os.execv(sys.executable, [sys.executable, *sys.argv[1:]])\n"
        "from coverage.cmdline import main\n"
        "raise SystemExit(main(['run', '--parallel-mode', *sys.argv[1:]]))\n"
    )
    wrapper.chmod(0o755)
    return wrapper


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    root = Path(__file__).resolve().parents[2]
    tests = sorted((root / "tests" / "integration").glob(args.pattern))
    if not tests:
        print("no integration tests discovered", file=sys.stderr)
        return 1

    with tempfile.TemporaryDirectory(prefix="akos-integration-runner-") as temp:
        env = os.environ.copy()
        if args.coverage:
            env["AKOS_PYTHON_BIN"] = str(_coverage_python(Path(temp)))
            # The explicit wrapper owns child measurement. Leaving automatic
            # startup enabled would try to start coverage twice in the wrapper.
            env.pop("COVERAGE_PROCESS_START", None)

        for test in tests:
            print(f"=== {test.relative_to(root)} ===", flush=True)
            test_env = env.copy()
            if args.coverage and test.name in JSON_CAPTURE_SENSITIVE_TESTS:
                # These scripts intentionally route doctor.sh output through
                # several capture layers. coverage CLI diagnostics would make
                # an otherwise-valid JSON self-scan look malformed.
                test_env.pop("AKOS_PYTHON_BIN", None)
            proc = subprocess.run(
                ["bash", str(test)],
                cwd=root,
                env=test_env,
                check=False,
            )
            if proc.returncode:
                return proc.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
