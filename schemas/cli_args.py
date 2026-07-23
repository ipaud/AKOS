"""Shared argparse behavior for AKOS commands with 0/1/2 exit contracts."""

from __future__ import annotations

import argparse
import sys


class UsageArgumentParser(argparse.ArgumentParser):
    """Reserve exit 1 for usage/setup errors and 2 for completed findings."""

    def error(self, message):
        self.print_usage(sys.stderr)
        print(f"{self.prog}: error: {message}", file=sys.stderr)
        raise SystemExit(1)
