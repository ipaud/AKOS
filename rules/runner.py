#!/usr/bin/env python3
"""Discovers and runs AKOS's executable rules against a target directory.

Rules are filesystem-discovered — rules/<domain>/<id>.yaml + a sibling
<id>.py — never a hand-maintained central index. This mirrors how packs/
already works, and avoids recreating the exact drift risk doctor.sh's
routing-table guard exists to catch for the pack index.

Usage:
    python3 rules/runner.py <target-dir> [--rule ID ...] [--domain D ...]
                            [--target project-source|akos-packs|all]
                            [--profile NAME] [--max-files N]
                            [--max-file-bytes N] [--max-total-bytes N]
                            [--format text|json]

Fail-closed. Findings and operational errors are separate results: a detector
or a registry that cannot run is an ExecutionError, never a finding, and never
a clean exit. Exit codes:

    0  ran completely, no blocking finding
    1  usage/setup error, or the scan was incomplete (bad registry, unreadable
       input, exceeded resource budget, unloadable detector, detector with no
       run(), internal exception) — an incomplete scan cannot report "clean"
    2  ran completely and a blocking finding exists (CRITICAL, or a finding a
       rule explicitly marked blocking)

If findings and operational errors coexist, exit 1 wins: the scanner is
incomplete, so its "no CRITICAL" is not trustworthy.
"""

from __future__ import annotations

import argparse
import importlib.util
import inspect
import os
import re
import stat
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

AKOS_HOME = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AKOS_HOME / "schemas"))
sys.path.insert(0, str(AKOS_HOME / "rules" / "security"))
import yaml_subset  # noqa: E402
from cli_args import UsageArgumentParser  # noqa: E402
from rule_schema import (  # noqa: E402
    CONFIDENCE_LEVELS,
    SEVERITIES,
    RuleContractError,
    require_valid_rule_registry,
)
from _secret_utils import mask_js_comments  # noqa: E402
from _sql_utils import mask_sql_comments  # noqa: E402

DEFAULT_IGNORE_DIRS = {"node_modules", ".git", "dist", "build", "vendor", ".next", "__pycache__", ".venv"}
DEFAULT_MAX_FILES = 10_000
DEFAULT_MAX_FILE_BYTES = 2 * 1024 * 1024
DEFAULT_MAX_TOTAL_BYTES = 100 * 1024 * 1024

SUPPRESS_RE = re.compile(r"akos:allow\s+([A-Z0-9_]+)")


@dataclass(frozen=True)
class ExecutionError:
    """An operational failure that made the scan incomplete — distinct from a
    finding. Its presence forces status 'error' and exit 1."""
    phase: str            # "discovery" | "setup" | "detector" | "read"
    rule_id: str | None
    path: str | None
    message: str


@dataclass
class ScanResult:
    status: str           # "ok" | "findings" | "error"
    findings: list[dict] = field(default_factory=list)
    errors: list[ExecutionError] = field(default_factory=list)
    rules_discovered: int = 0
    rules_executed: int = 0


@dataclass(frozen=True)
class ScanLimits:
    max_files: int = DEFAULT_MAX_FILES
    max_file_bytes: int = DEFAULT_MAX_FILE_BYTES
    max_total_bytes: int = DEFAULT_MAX_TOTAL_BYTES

    def __post_init__(self):
        for name, value in asdict(self).items():
            if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
                raise ValueError(f"{name} must be a positive integer")


class ScanReadError(OSError):
    def __init__(self, path: Path, message: str):
        super().__init__(message)
        self.path = path


class ScanLimitError(ValueError):
    def __init__(self, message: str, path: Path | None = None):
        super().__init__(message)
        self.path = path


class ScanBudget:
    """A scan-wide budget charged once per unique resolved input file."""

    def __init__(self, limits: ScanLimits):
        self.limits = limits
        self.seen: set[Path] = set()
        self.traversal_seen: set[Path] = set()
        self.verified_readable: set[Path] = set()
        self.total_bytes = 0

    def charge_traversal(self, path: Path) -> None:
        """Bound discovery work, including non-matching files and directories.

        Ignored directories are pruned before this point. Counting every other
        unique entry prevents a repository full of non-matching paths or empty
        directories from making discovery unbounded while evading the input
        file budget.
        """
        # Do not resolve traversal entries: a repository-controlled symlink
        # must count toward the enumeration budget without causing us to
        # inspect or canonicalize its external target.
        lexical = Path(os.path.abspath(path))
        if lexical in self.traversal_seen:
            return
        if len(self.traversal_seen) + 1 > self.limits.max_files:
            raise ScanLimitError(
                f"scan traversal exceeds max files/entries limit "
                f"({self.limits.max_files})",
                path,
            )
        self.traversal_seen.add(lexical)

    def charge(self, path: Path, size: int) -> None:
        resolved = path.resolve()
        if resolved in self.seen:
            return
        if len(self.seen) + 1 > self.limits.max_files:
            raise ScanLimitError(
                f"scan exceeds max files limit ({self.limits.max_files})",
                path,
            )
        if size > self.limits.max_file_bytes:
            raise ScanLimitError(
                f"file exceeds max file bytes limit ({size} > {self.limits.max_file_bytes})",
                path,
            )
        if self.total_bytes + size > self.limits.max_total_bytes:
            raise ScanLimitError(
                f"scan exceeds max total bytes limit "
                f"({self.total_bytes + size} > {self.limits.max_total_bytes})",
                path,
            )
        self.seen.add(resolved)
        self.total_bytes += size

    def verify_readable(self, path: Path) -> None:
        resolved = path.resolve()
        if resolved in self.verified_readable:
            return
        try:
            with path.open("rb") as handle:
                while handle.read(64 * 1024):
                    pass
        except OSError as exc:
            raise ScanReadError(path, str(exc)) from exc
        self.verified_readable.add(resolved)


class RegistryError(Exception):
    """Raised by discover_rules when a registry is malformed and the caller did
    not pass an errors list to collect into — so a broken registry fails closed
    for count-only callers instead of silently shrinking the rule set."""


def _is_blocking(finding: dict) -> bool:
    """CRITICAL always blocks; a rule may also mark a specific finding blocking
    (e.g. a live vendor credential that defaults to HIGH)."""
    return finding.get("severity") == "CRITICAL" or bool(finding.get("blocking"))


class Rule:
    def __init__(self, yaml_path: Path, data: dict):
        self.yaml_path = yaml_path
        self.id = data["id"]
        self.title = data.get("title", self.id)
        self.domain = data.get("domain", yaml_path.parent.name)
        self.level = data.get("level", "A")
        self.confidence = data.get("confidence", "Moderate")
        self.severity_default = data.get("severity", {}).get("default", "MEDIUM")
        self.severity_profiles = data.get("severity", {}).get("profiles", {})
        self.related_packs = data.get("related_packs", [])
        self.applies_to = data.get("applies_to", {})
        self.target = self.applies_to.get("target", "project-source")
        self.globs = self.applies_to.get("glob", ["**/*"])
        self.detector_path = AKOS_HOME / data["detector"]
        self.recommendation = data.get("recommendation", "")
        self.status = data.get("status", "stable")
        self.suppressible = data.get("suppressible", True)

    def severity_for_profile(self, profile: str | None) -> str:
        if profile and profile in self.severity_profiles:
            return self.severity_profiles[profile]
        return self.severity_default


def discover_rules(domain_filter=None, rule_filter=None, target_filter=None, errors=None) -> list[Rule]:
    """Discover stable rules. A malformed registry, or one missing required
    keys, is an operational error — recorded in `errors` if a collector is
    passed, otherwise raised (RegistryError) so a count-only caller fails
    closed rather than quietly running fewer rules than it thinks."""
    rules = []
    for yaml_path in sorted((AKOS_HOME / "rules").glob("*/*.yaml")):
        rel = str(yaml_path.relative_to(AKOS_HOME))
        try:
            data = yaml_subset.load(yaml_path)
            require_valid_rule_registry(data, source=yaml_path)
            rule = Rule(yaml_path, data)
        except (yaml_subset.YamlSubsetError, RuleContractError, KeyError, ValueError, TypeError) as e:
            rule_id = None
            if isinstance(e, KeyError):
                # A KeyError here is a missing required registry field.
                msg = f"registry missing required field {e}"
            else:
                msg = f"unparseable/invalid registry: {e}"
            err = ExecutionError("discovery", rule_id, rel, msg)
            if errors is None:
                raise RegistryError(f"{rel}: {msg}") from e
            errors.append(err)
            continue
        if rule_filter and rule.id not in rule_filter:
            continue
        if domain_filter and rule.domain not in domain_filter:
            continue
        if target_filter and rule.target not in target_filter:
            continue
        if rule.status != "stable":
            continue
        rules.append(rule)
    return rules


def collect_files(target_dir: Path, globs: list[str], *,
                  budget: ScanBudget | None = None) -> list[Path]:
    # Symlinks are skipped, and anything whose real location falls outside the
    # scanned tree is skipped too (glob on Python <=3.12 recurses through
    # symlinked directories). Without this, scanning an untrusted repository
    # that plants `link -> ~/.ssh/id_rsa` makes the secret detectors read the
    # host's private key — and a review report quotes the evidence it finds.
    root_resolved = target_dir.resolve()
    budget = budget or ScanBudget(ScanLimits())
    files = []
    seen = set()

    # pathlib's recursive glob cannot prune ignored directories before descent.
    # Walk explicitly so node_modules/.git/etc. cost one directory entry rather
    # than an unbounded traversal of attacker-controlled contents.
    patterns = _glob_variants(globs)
    pending = [target_dir]
    while pending:
        directory = pending.pop()
        try:
            with os.scandir(directory) as entries:
                # Charge while enumerating, before materializing/sorting the
                # directory. This bounds a single attacker-controlled
                # directory and counts symlinks/non-matching entries too.
                enumerated = []
                for entry in entries:
                    p = Path(entry.path)
                    if (
                        entry.is_dir(follow_symlinks=False)
                        and entry.name in DEFAULT_IGNORE_DIRS
                    ):
                        continue
                    budget.charge_traversal(p)
                    enumerated.append(entry)
                ordered_entries = sorted(
                    enumerated, key=lambda entry: entry.name
                )
            child_directories = []
            for entry in ordered_entries:
                p = Path(entry.path)
                if entry.is_symlink():
                    continue
                if entry.is_dir(follow_symlinks=False):
                    child_directories.append(p)
                    continue
                if not entry.is_file(follow_symlinks=False):
                    continue
                relative_path = p.relative_to(target_dir).as_posix()
                if not _matches_glob(relative_path, patterns):
                    continue
                try:
                    file_stat = entry.stat(follow_symlinks=False)
                except OSError as exc:
                    raise ScanReadError(p, str(exc)) from exc
                if not stat.S_ISREG(file_stat.st_mode):
                    continue
                try:
                    resolved = p.resolve()
                    resolved.relative_to(root_resolved)
                except (ValueError, OSError):
                    continue
                if resolved in seen:
                    continue
                budget.charge(p, file_stat.st_size)
                budget.verify_readable(p)
                seen.add(resolved)
                files.append(p)
            # Reverse so the lexically first directory is visited first with a
            # LIFO stack, keeping errors and limits deterministic.
            pending.extend(reversed(child_directories))
        except (ScanReadError, ScanLimitError):
            raise
        except OSError as exc:
            raise ScanReadError(directory, str(exc)) from exc
    return sorted(files)


def _glob_variants(globs: list[str]) -> tuple[str, ...]:
    """Expand `**/` as zero-or-more directories for PurePath.match().

    PurePath.match treats `**/` as one-or-more on Python versions supported by
    AKOS, unlike Path.glob. Producing the zero-directory variants preserves the
    registry glob contract while still using a prunable walker.
    """
    variants: set[str] = set()
    pending = [pattern.replace("\\", "/").removeprefix("./") for pattern in globs]
    while pending:
        pattern = pending.pop()
        if pattern in variants:
            continue
        variants.add(pattern)
        marker = pattern.find("**/")
        if marker >= 0:
            pending.append(pattern[:marker] + pattern[marker + 3:])
    return tuple(sorted(variants))


def _matches_glob(relative_path: str, patterns: tuple[str, ...]) -> bool:
    path = Path(relative_path)
    return any(path.match(pattern) for pattern in patterns)


def load_detector(rule: Rule):
    spec = importlib.util.spec_from_file_location(f"akos_rule_{rule.id}", rule.detector_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SUPPRESS_WINDOW = 5  # lines to look back from the evidence line
_JS_SUFFIXES = {
    ".cjs", ".js", ".jsx", ".mjs", ".ts", ".tsx", ".vue", ".svelte",
}


def _directive_is_in_comment(
    path: Path,
    text: str,
    start: int,
    end: int,
) -> bool:
    """Return whether a directive span belongs to source commentary.

    SQL and JS-family inputs use the same offset-preserving lexers as their
    detectors. For other text formats, accept only lines whose first
    non-whitespace token is an unambiguous comment marker; conservative
    rejection is safer than letting a string literal suppress a finding.
    """
    suffix = path.suffix.lower()
    if suffix == ".sql":
        masked = mask_sql_comments(text)
        return not masked[start:end].strip()
    if suffix in _JS_SUFFIXES:
        masked = mask_js_comments(text)
        return not masked[start:end].strip()

    line_start = text.rfind("\n", 0, start) + 1
    prefix = text[line_start:start].lstrip()
    return prefix.startswith(("#", "//", "--", "/*", "*", "<!--"))


def _validated_findings(raw_findings) -> list[dict]:
    """Materialize and validate one detector result before using any of it."""
    if raw_findings is None or isinstance(raw_findings, (str, bytes, dict)):
        raise TypeError("detector run() must return an iterable of finding objects")
    findings = list(raw_findings)
    for index, finding in enumerate(findings):
        if not isinstance(finding, dict):
            raise TypeError(f"finding {index} must be an object")
        evidence = finding.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            raise TypeError(f"finding {index}.evidence must be a non-empty list")
        for ev_index, item in enumerate(evidence):
            if not isinstance(item, dict):
                raise TypeError(
                    f"finding {index}.evidence[{ev_index}] must be an object"
                )
            if not isinstance(item.get("path"), str) or not item["path"]:
                raise TypeError(
                    f"finding {index}.evidence[{ev_index}].path must be a string"
                )
            line_start = item.get("line_start")
            if (
                not isinstance(line_start, int)
                or isinstance(line_start, bool)
                or line_start < 1
            ):
                raise TypeError(
                    f"finding {index}.evidence[{ev_index}].line_start "
                    "must be a positive integer"
                )
            line_end = item.get("line_end", line_start)
            if (
                not isinstance(line_end, int)
                or isinstance(line_end, bool)
                or line_end < line_start
            ):
                raise TypeError(
                    f"finding {index}.evidence[{ev_index}].line_end "
                    "must be an integer at or after line_start"
                )
            if "snippet" in item and not isinstance(item["snippet"], str):
                raise TypeError(
                    f"finding {index}.evidence[{ev_index}].snippet must be a string"
                )
        if "blocking" in finding and not isinstance(finding["blocking"], bool):
            raise TypeError(f"finding {index}.blocking must be boolean")
        if "detail" in finding and not isinstance(finding["detail"], str):
            raise TypeError(f"finding {index}.detail must be a string")
        if (
            "severity_override" in finding
            and finding["severity_override"] not in SEVERITIES
        ):
            raise TypeError(
                f"finding {index}.severity_override must be a known severity"
            )
        if (
            "confidence_override" in finding
            and finding["confidence_override"] not in CONFIDENCE_LEVELS
        ):
            raise TypeError(
                f"finding {index}.confidence_override must be a known confidence"
            )
    return findings


def is_suppressed(finding: dict, rule_id: str, file_text_cache: dict) -> bool:
    for ev in finding.get("evidence", []):
        path = Path(ev["path"])
        if path not in file_text_cache:
            file_text_cache[path] = path.read_text(
                encoding="utf-8", errors="replace"
            )
        text = file_text_cache[path]
        lines = text.splitlines(keepends=True)
        evidence_line = ev.get("line_start", 1)
        first_line = max(1, evidence_line - SUPPRESS_WINDOW + 1)
        absolute = sum(len(line) for line in lines[: first_line - 1])
        for line in lines[first_line - 1 : evidence_line]:
            for match in SUPPRESS_RE.finditer(line):
                if (
                    match.group(1) == rule_id
                    and _directive_is_in_comment(
                        path,
                        text,
                        absolute + match.start(),
                        absolute + match.end(),
                    )
                ):
                    return True
            absolute += len(line)
    return False


def run_rules(target_dir: Path, rules: list[Rule], profile: str | None,
              errors=None, limits: ScanLimits | None = None) -> list[dict]:
    """Run each rule's detector. A detector that cannot run (missing file, no
    run(), or an exception) is an ExecutionError recorded in `errors` — it is
    never turned into a finding, so a broken security detector can never read
    as a clean pass. Severity is the rule/finding severity as-is: there is no
    path-based downgrade (a real credential under tests/ is still a real
    credential — see P0-4)."""
    if errors is None:
        errors = []
    all_findings = []
    file_text_cache: dict = {}
    budget = ScanBudget(limits or ScanLimits())
    for rule in rules:
        scan_dir = AKOS_HOME if rule.target == "akos-packs" else target_dir
        try:
            files = collect_files(scan_dir, rule.globs, budget=budget)
        except ScanReadError as exc:
            errors.append(ExecutionError("read", rule.id, str(exc.path), str(exc)))
            continue
        except ScanLimitError as exc:
            errors.append(ExecutionError(
                "setup",
                rule.id,
                str(exc.path) if exc.path else None,
                str(exc),
            ))
            continue
        if not files:
            continue
        rel_detector = _rel_to_akos(rule.detector_path)
        try:
            if not rule.detector_path.exists():
                raise FileNotFoundError("detector file missing")
            module = load_detector(rule)
            if not hasattr(module, "run"):
                raise AttributeError("detector has no run() function")
            # Detectors that classify by path take the scan root so they can
            # judge the project-relative path, not the absolute one.
            if len(inspect.signature(module.run).parameters) >= 2:
                raw_findings = module.run(files, scan_dir)
            else:
                raw_findings = module.run(files)
            raw_findings = _validated_findings(raw_findings)
        except OSError as e:
            errors.append(ExecutionError(
                "read", rule.id, getattr(e, "filename", None), str(e)
            ))
            continue
        except Exception as e:  # noqa: BLE001 - captured as an operational error, not a finding
            errors.append(ExecutionError("detector", rule.id, rel_detector, str(e)))
            continue

        for f in raw_findings:
            suppressed = False
            if rule.suppressible:
                try:
                    suppressed = is_suppressed(f, rule.id, file_text_cache)
                except OSError as exc:
                    evidence = f.get("evidence", [])
                    evidence_path = evidence[0].get("path") if evidence else None
                    errors.append(ExecutionError(
                        "read",
                        rule.id,
                        evidence_path or getattr(exc, "filename", None),
                        str(exc),
                    ))
            if suppressed:
                continue
            severity = f.get("severity_override") or rule.severity_for_profile(profile)
            finding = {
                "rule_id": rule.id,
                "title": rule.title,
                "domain": rule.domain,
                "level": rule.level,
                "severity": severity,
                "confidence": f.get("confidence_override", rule.confidence),
                "evidence": f.get("evidence", []),
                "recommendation": f.get("detail", rule.recommendation),
                "blocking": bool(f.get("blocking")) or severity == "CRITICAL",
            }
            all_findings.append(finding)
    return all_findings


def _rel_to_akos(p: Path) -> str:
    try:
        return str(p.relative_to(AKOS_HOME))
    except ValueError:
        return str(p)


def scan(target_dir: Path, domain_filter=None, rule_filter=None, target_filter=None,
         profile: str | None = None, limits: ScanLimits | None = None) -> ScanResult:
    """Full pipeline: discover → run → classify. Setup problems (a filter that
    matches nothing, an unknown rule id, or — with no filter — an empty rule
    set) are operational errors, so an incomplete run never reports clean."""
    errors: list[ExecutionError] = []
    rules = discover_rules(
        domain_filter=domain_filter,
        rule_filter=rule_filter,
        target_filter=target_filter,
        errors=errors,
    )

    if rule_filter or domain_filter or target_filter:
        if not rules:
            requested = ", ".join(sorted(
                set(rule_filter or set())
                | set(domain_filter or set())
                | set(target_filter or set())
            ))
            errors.append(ExecutionError("setup", None, None,
                                         f"no rule matches the filter ({requested})"))
        elif rule_filter:
            unmatched = sorted(set(rule_filter) - {r.id for r in rules})
            if unmatched:
                errors.append(ExecutionError("setup", None, None,
                                             f"no such rule: {', '.join(unmatched)}"))
    elif not rules:
        errors.append(ExecutionError("setup", None, None,
                                     "no stable rules discovered — cannot report a clean scan"))

    findings = run_rules(
        target_dir,
        rules,
        profile,
        errors=errors,
        limits=limits,
    ) if rules else []
    failed_rules = {
        e.rule_id
        for e in errors
        if e.rule_id and e.phase in {"detector", "read", "setup"}
    }
    executed = len(rules) - len(failed_rules)

    if errors:
        status = "error"
    elif any(_is_blocking(f) for f in findings):
        status = "findings"
    else:
        status = "ok"
    return ScanResult(status=status, findings=findings, errors=errors,
                      rules_discovered=len(rules), rules_executed=executed)


def print_text(result: ScanResult):
    order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    c_red, c_yellow, c_reset, c_bold = "\033[31m", "\033[33m", "\033[0m", "\033[1m"
    glyph = {"CRITICAL": f"{c_red}✗{c_reset}", "HIGH": f"{c_red}!{c_reset}", "MEDIUM": f"{c_yellow}!{c_reset}", "LOW": "·"}
    findings = result.findings
    for f in sorted(findings, key=lambda x: order.get(x["severity"], 9)):
        loc = ""
        if f["evidence"]:
            ev = f["evidence"][0]
            loc = f" — {ev['path']}:{ev.get('line_start', '?')}"
        block = " [blocking]" if _is_blocking(f) else ""
        print(f"{glyph.get(f['severity'], '?')} [{f['severity']}]{block} {f['rule_id']}{loc}")
        print(f"    {f['title']}")
        if f["recommendation"]:
            print(f"    Fix: {f['recommendation']}")

    if result.errors:
        # Operational errors are printed separately and never phrased as a
        # clean result — the scan did not finish.
        print(f"\n{c_bold}{c_red}Execution errors{c_reset}  "
              f"(the scan is INCOMPLETE — do not read this as clean):")
        for e in result.errors:
            where = e.rule_id or e.path or e.phase
            print(f"{c_red}✗{c_reset} [{e.phase}] {where}: {e.message}")

    counts: dict = {}
    for f in findings:
        counts[f["severity"]] = counts.get(f["severity"], 0) + 1
    sev_summary = "  ".join(f"{k}: {v}" for k, v in sorted(counts.items(), key=lambda kv: order.get(kv[0], 9)))
    print(f"\n{c_bold}Summary{c_reset}  status: {result.status}  "
          f"rules discovered: {result.rules_discovered}  executed: {result.rules_executed}  "
          f"findings: {len(findings)}  errors: {len(result.errors)}")
    if findings:
        print(f"  {sev_summary}")


def _result_to_json(result: ScanResult) -> dict:
    return {
        "status": result.status,
        "summary": {
            "rules_discovered": result.rules_discovered,
            "rules_executed": result.rules_executed,
            "findings": len(result.findings),
            "errors": len(result.errors),
        },
        "findings": result.findings,
        "errors": [asdict(e) for e in result.errors],
    }


def _positive_int(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be a positive integer") from exc
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return parsed


def main(argv=None) -> int:
    ap = UsageArgumentParser(description=__doc__)
    ap.add_argument("target_dir", nargs="?", default=".", help="Directory to scan (project-source rules)")
    ap.add_argument("--rule", action="append", help="Only run this rule id (repeatable)")
    ap.add_argument("--domain", action="append", help="Only run rules in this domain (repeatable)")
    ap.add_argument("--target", choices=["project-source", "akos-packs", "all"],
                    default="all", help="Rule surface to run (default: all)")
    ap.add_argument("--profile", help="Reasoning profile — affects severity mapping")
    ap.add_argument("--max-files", type=_positive_int, default=DEFAULT_MAX_FILES)
    ap.add_argument("--max-file-bytes", type=_positive_int, default=DEFAULT_MAX_FILE_BYTES)
    ap.add_argument("--max-total-bytes", type=_positive_int, default=DEFAULT_MAX_TOTAL_BYTES)
    ap.add_argument("--format", choices=["text", "json"], default="text")
    args = ap.parse_args(argv)

    target_dir = Path(args.target_dir).resolve()
    if not target_dir.is_dir():
        print(f"error: not a directory: {target_dir}", file=sys.stderr)
        return 1

    try:
        result = scan(
            target_dir,
            domain_filter=set(args.domain) if args.domain else None,
            rule_filter=set(args.rule) if args.rule else None,
            target_filter=None if args.target == "all" else {args.target},
            profile=args.profile,
            limits=ScanLimits(
                max_files=args.max_files,
                max_file_bytes=args.max_file_bytes,
                max_total_bytes=args.max_total_bytes,
            ),
        )
    except RegistryError as e:
        # Belt-and-braces: scan() passes an errors collector, so this path is
        # only reached if a nested call raised. Fail closed either way.
        print(f"error: {e}", file=sys.stderr)
        return 1

    if args.format == "json":
        import json
        print(json.dumps(_result_to_json(result), indent=2))
    else:
        print_text(result)

    # Errors beat findings: an incomplete scan is exit 1, even if a blocking
    # finding also surfaced. A complete scan with a blocking finding is exit 2.
    return {"error": 1, "findings": 2, "ok": 0}[result.status]


if __name__ == "__main__":
    raise SystemExit(main())
