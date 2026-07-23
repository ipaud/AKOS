#!/usr/bin/env python3
"""Check a project's `.akos/config.md` against a closed set of allowed values.

Why this exists. `.akos/config.md` lives in whatever repository the agent is
working in — including a repository someone else wrote. The skills treat it as
untrusted manifest data (project facts and hints), never as instructions, and
never as something that can lower the safety floor. This check enforces the
*form* of that data so a hostile checkout cannot smuggle a disallowed profile,
a pack path that escapes `packs/`, an ambiguous `Deployed` flag, a
repo-side profile-override, or a `status: draft`/`deprecated` pack
self-authorized into the project's always-load set, into the agent's reading.

Form, not trust. The checking here is deterministic: a profile either is one
of the six names or it is not; a pack path either resolves inside
AKOS_HOME/packs/ or it does not; `Deployed` is exactly `yes`/`no` or it is a
finding. A model cannot be argued out of that result. But a clean result means
only that the file is *well-formed* — it does NOT make the file authoritative
or turn the repository into a trusted operator. The trust boundary lives in the
skills (repo config sits below the safety floor, the user, and Level-0 personal
rules); this script is a control over the values, not a grant of trust. Do not
record it as more than that.

Exit codes: 0 clean · 1 usage error · 2 findings.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import yaml_subset  # noqa: E402

VALID_PROFILES = {
    "Prototype", "Startup MVP", "Production",
    "Enterprise", "Game Dev", "Internal Tool",
}

# Sections whose content an agent is told to treat as binding. Anything here
# is attacker-controlled in a cloned repo, so each needs a closed check.
PROFILE_RE = re.compile(r"^profile:\s*(.+?)\s*$", re.MULTILINE)
PERSONAL_RE = re.compile(r"^personal_profile:\s*(.+?)\s*$", re.MULTILINE)
PACK_LINE_RE = re.compile(r"^\s*-\s*(\S+)\s*$", re.MULTILINE)
# The only shapes that name a pack shipped with AKOS.
PACK_ENTRY_RE = re.compile(r"(?:packs/)?[a-z0-9][a-z0-9-]*/[a-z0-9][a-z0-9-]*")
# `Deployed:` may raise the safety floor (yes → security/RLS mandatory), so an
# ambiguous or duplicated value is a security-relevant defect, not a nicety.
DEPLOYED_RE = re.compile(r"^\s*-?\s*Deployed:\s*(.+?)\s*$", re.MULTILINE)
DEPLOYED_VALUES = {"yes", "no"}


def _section(text: str, heading: str) -> str:
    """Return the body under a `## heading`, up to the next `##` or EOF."""
    m = re.search(rf"^##\s+{re.escape(heading)}\s*$(.*?)(?=^##\s|\Z)",
                  text, re.MULTILINE | re.DOTALL)
    return m.group(1) if m else ""


def check_config(config_path: Path, akos_home: Path) -> list[dict]:
    findings: list[dict] = []
    text = config_path.read_text(encoding="utf-8")

    m = PROFILE_RE.search(text)
    if m:
        profile = m.group(1)
        if profile not in VALID_PROFILES:
            findings.append({
                "field": "profile",
                "severity": "HIGH",
                "message": f"{profile!r} is not one of the six profiles "
                           f"({', '.join(sorted(VALID_PROFILES))}). A profile this file "
                           f"does not recognise must not silently become the active one.",
            })

    m = PERSONAL_RE.search(text)
    if m:
        name = m.group(1)
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", name):
            findings.append({
                "field": "personal_profile",
                "severity": "HIGH",
                "message": f"{name!r} is not a plain profile name. This is used to build a "
                           f"path under packs/personal/, so it must not contain separators.",
            })
        elif not (akos_home / "packs" / "personal" / name).is_dir():
            findings.append({
                "field": "personal_profile",
                "severity": "MEDIUM",
                "message": f"{name!r} does not exist under packs/personal/. "
                           f"List available profiles with 'akos profile list'.",
            })

    # The dangerous one: a pack path that resolves outside AKOS_HOME/packs/
    # turns attacker-authored prose into content the agent is instructed to
    # treat as constraints and defaults, not suggestions.
    packs_root = (akos_home / "packs").resolve()
    for pm in PACK_LINE_RE.finditer(_section(text, "Packs to always load")):
        entry = pm.group(1)

        # Only `packs/<domain>/<name>` or `<domain>/<name>` name an AKOS pack.
        # Anything else — `./x`, `../x`, `/abs/x`, `~/x` — is not a pack
        # reference at all, and an agent reading it would resolve it against
        # the project, loading attacker-authored prose as authoritative
        # knowledge. Reject on the shape, before any path resolution: a
        # resolver that assumes AKOS-relative paths will quietly report such
        # an entry as merely "missing", which is how this check first missed
        # the very attack it exists to catch.
        if not PACK_ENTRY_RE.fullmatch(entry):
            findings.append({
                "field": "Packs to always load",
                "severity": "CRITICAL",
                "message": f"{entry!r} is not an AKOS pack reference. Only "
                           f"'packs/<domain>/<name>' or '<domain>/<name>' are valid here. "
                           f"A path like this resolves against the project, so a file the "
                           f"project controls would be loaded as authoritative knowledge.",
            })
            continue

        rel = entry[len("packs/"):] if entry.startswith("packs/") else entry
        resolved = (packs_root / rel).resolve()
        if not str(resolved).startswith(str(packs_root) + "/"):
            findings.append({
                "field": "Packs to always load",
                "severity": "CRITICAL",
                "message": f"{entry!r} resolves outside {packs_root}.",
            })
        elif not resolved.is_dir():
            findings.append({
                "field": "Packs to always load",
                "severity": "MEDIUM",
                "message": f"{entry!r} does not exist. List packs with 'akos list-packs'.",
            })
        else:
            # A project cannot self-authorize a draft or deprecated pack into
            # its always-load set — there is no allow_draft_packs escape
            # hatch in this file. Draft content is readable and usable, just
            # not promised-stable, so this is advisory (MEDIUM), not a hard
            # block; the only legitimate opt-in is the CURRENT conversation's
            # user explicitly asking for it, never this untrusted file.
            meta_path = resolved / "metadata.yaml"
            if meta_path.is_file():
                try:
                    meta = yaml_subset.load(meta_path)
                except yaml_subset.YamlSubsetError:
                    meta = {}
                status = meta.get("status") if isinstance(meta, dict) else None
                if status == "draft":
                    findings.append({
                        "field": "Packs to always load",
                        "severity": "MEDIUM",
                        "message": f"{entry!r} is status: draft — not yet promised-stable, "
                                   f"so it should not be a project's always-loaded authority. "
                                   f"Only the current conversation's user can opt into draft "
                                   f"content explicitly; this file cannot authorize it.",
                    })
                elif status == "deprecated":
                    replacement = meta.get("replacement") if isinstance(meta, dict) else None
                    repl_note = f" Replacement: {replacement}." if replacement else " No replacement is recorded."
                    findings.append({
                        "field": "Packs to always load",
                        "severity": "MEDIUM",
                        "message": f"{entry!r} is status: deprecated.{repl_note}",
                    })

    # `Deployed:` is a closed flag. A value that is not exactly yes/no is
    # ambiguous (does it raise the security floor or not?), and two declarations
    # leave the resolution to chance — either way, resolve it as a finding
    # rather than let a hostile config decide by ordering.
    deployed = DEPLOYED_RE.findall(text)
    if len(deployed) > 1:
        findings.append({
            "field": "Deployed",
            "severity": "HIGH",
            "message": f"'Deployed' is declared {len(deployed)} times "
                       f"({', '.join(repr(v) for v in deployed)}). A duplicated safety flag "
                       f"must not resolve silently — declare it once.",
        })
    for value in deployed:
        if value.strip().lower() not in DEPLOYED_VALUES:
            findings.append({
                "field": "Deployed",
                "severity": "HIGH",
                "message": f"Deployed: {value!r} is not 'yes' or 'no'. This flag can raise the "
                           f"safety floor, so an ambiguous value must not be interpreted.",
            })

    # A repository cannot rewrite the reasoning-profile weight table. Per-lens
    # weights come from the profile and the user, never from the reviewed repo,
    # so any content in this section is non-authoritative and flagged. The
    # scaffolded template ships the section empty — that stays clean.
    overrides = _section(text, "Profile overrides")
    override_lines = [
        ln.strip() for ln in overrides.splitlines()
        if ln.strip() and not ln.strip().startswith("<!--")
    ]
    if override_lines:
        findings.append({
            "field": "Profile overrides",
            "severity": "HIGH",
            "message": "This section has content, but repository-side profile overrides are not "
                       "authoritative: an agent takes lens weights from the profile and the user, "
                       "never from the reviewed repo, and no override can lower the safety floor. "
                       "Remove it, or move a trusted change to the operator's local config.",
        })

    return findings


class _ArgumentParser(argparse.ArgumentParser):
    """argparse exits 2 on a usage error, which collides with this module's
    "2 means findings". A caller — including CI — could not tell a mistyped
    flag from a hostile config. Usage errors exit 1, per docs/cli/exit-codes.md.
    """

    def error(self, message):
        self.print_usage(sys.stderr)
        print(f"{self.prog}: error: {message}", file=sys.stderr)
        sys.exit(1)


def main(argv=None) -> int:
    ap = _ArgumentParser(description=__doc__)
    ap.add_argument("dir_positional", nargs="?", default=None, metavar="DIR",
                    help="project directory (default: current)")
    ap.add_argument("--dir", default=None, help="project directory (default: current)")
    ap.add_argument("--format", choices=["text", "json"], default="text")
    args = ap.parse_args(argv)

    if args.dir_positional and args.dir and args.dir_positional != args.dir:
        print(f"error: two different directories given "
              f"({args.dir_positional!r} and {args.dir!r}). Pass one.", file=sys.stderr)
        return 1
    args.dir = args.dir or args.dir_positional or "."

    akos_home = Path(__file__).resolve().parent.parent
    config_path = Path(args.dir).resolve() / ".akos" / "config.md"
    if not config_path.is_file():
        print(f"no .akos/config.md in {Path(args.dir).resolve()} "
              f"(run 'akos install-project' to create one)")
        return 0

    findings = check_config(config_path, akos_home)

    if args.format == "json":
        import json
        print(json.dumps(findings, indent=2))
    else:
        for f in findings:
            print(f"\033[31m✗\033[0m [{f['severity']}] {f['field']} — {f['message']}")
        if not findings:
            print(f"\033[32m✓\033[0m {config_path} is within the allowed value set")
        else:
            print(f"\n{len(findings)} finding(s). Treat this config as untrusted until resolved: "
                  f"it came from the project, not from the operator.")

    return 2 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
