#!/usr/bin/env python3
"""Report deterministic repository-governance readiness findings.

The audit is read-only and advisory. It checks stable invariants that do not
require product judgment; the gatekeeper handles semantic reconciliation.

Exit codes: 0 no blockers (warnings may be present), 1 blockers, 2 unable to
inspect the requested root.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


CANONICAL_PATHS = (
    "AGENTS.md",
    "README.md",
    "docs/index.md",
    "docs/process/CURRENT_STAGE.md",
    "docs/process/PROJECT_MAP.md",
    "docs/process/DEVELOPMENT_WORKFLOW.md",
)

README_REFERENCES = (
    "AGENTS.md",
    "docs/index.md",
    "docs/process/CURRENT_STAGE.md",
    "docs/process/PROJECT_MAP.md",
    "docs/process/DEVELOPMENT_WORKFLOW.md",
)

README_PLACEHOLDERS = (
    "# <Project Name>",
    "Brief description of its purpose.",
)

CURRENT_STAGE_PLACEHOLDERS = (
    "<DATE>",
    "<ONE SENTENCE — which uncertainty we are resolving>",
    "<verified fact, not intention>",
    "<the active artifact or frontier>",
    "<imperative action>",
    "<exact file, decision ID, or gate>",
    "<observable completion condition>",
    "<work explicitly out of scope in this phase>",
    "<pending decision + who takes it + what evidence would unblock it>",
)

FRONTIER_HEADING = "## Next"
FRONTIER_FIELDS = ("Action:", "Target:", "Done when:")
VAGUE_FRONTIER_REFERENCE = re.compile(
    r"\b(?:remaining|pending|outstanding)\b(?:\W+\w+){0,3}\W+"
    r"\b(?:findings?|issues?|items?|tasks?)\b",
    re.IGNORECASE,
)
EXACT_FRONTIER_REFERENCE = re.compile(
    r"`[^`\n]*(?:/|\.md\b|#[\w-]+|[A-Z][A-Z0-9_]*-\d+)[^`\n]*`"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="project root (defaults to the parent of scripts/)",
    )
    parser.add_argument("--json", action="store_true", help="emit JSON")
    return parser.parse_args()


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def markdown_h2_section(text: str, heading: str) -> tuple[int, str] | None:
    """Return the offset and body of one exact H2 section."""
    match = re.search(rf"(?m)^{re.escape(heading)}\s*$", text)
    if match is None:
        return None
    body_start = match.end()
    next_heading = re.search(r"(?m)^##\s+", text[body_start:])
    body_end = (
        body_start + next_heading.start()
        if next_heading is not None
        else len(text)
    )
    return match.start(), text[body_start:body_end]


def add_finding(
    findings: list[dict[str, object]],
    severity: str,
    code: str,
    path: str,
    message: str,
    line: int | None = None,
) -> None:
    finding: dict[str, object] = {
        "severity": severity,
        "code": code,
        "path": path,
        "message": message,
    }
    if line is not None:
        finding["line"] = line
    findings.append(finding)


def read_text(root: Path, relative_path: str) -> str | None:
    path = root / relative_path
    if not path.is_file():
        return None
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None


def git_root_for(project_root: Path) -> Path | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(project_root), "rev-parse", "--show-toplevel"],
            text=True,
            capture_output=True,
            check=False,
        )
    except OSError:
        return None
    if result.returncode != 0:
        return None
    return Path(result.stdout.strip()).resolve()


def is_tracked(git_root: Path, project_root: Path, relative_path: str) -> bool:
    try:
        project_prefix = project_root.resolve().relative_to(git_root)
    except ValueError:
        return False
    repo_path = project_prefix / relative_path
    try:
        result = subprocess.run(
            [
                "git",
                "-C",
                str(git_root),
                "ls-files",
                "--error-unmatch",
                "--",
                str(repo_path),
            ],
            text=True,
            capture_output=True,
            check=False,
        )
    except OSError:
        return False
    return result.returncode == 0


def collect_findings(root: Path) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    texts: dict[str, str] = {}

    for relative_path in CANONICAL_PATHS:
        text = read_text(root, relative_path)
        if text is None:
            add_finding(
                findings,
                "BLOCKER",
                "MISSING_CANONICAL_FILE",
                relative_path,
                "required canonical entry file is missing or not UTF-8 text",
            )
        else:
            texts[relative_path] = text

    readme = texts.get("README.md")
    if readme is not None:
        for marker in README_PLACEHOLDERS:
            offset = readme.find(marker)
            if offset >= 0:
                add_finding(
                    findings,
                    "BLOCKER",
                    "UNRESOLVED_TEMPLATE",
                    "README.md",
                    f"unresolved foundation placeholder: {marker}",
                    line_number(readme, offset),
                )
        for reference in README_REFERENCES:
            if reference not in readme:
                add_finding(
                    findings,
                    "BLOCKER",
                    "README_NAVIGATION_MISSING",
                    "README.md",
                    f"repository navigation does not reference {reference}",
                    1,
                )

    current_stage = texts.get("docs/process/CURRENT_STAGE.md")
    if current_stage is not None:
        for marker in CURRENT_STAGE_PLACEHOLDERS:
            offset = current_stage.find(marker)
            if offset >= 0:
                add_finding(
                    findings,
                    "BLOCKER",
                    "UNRESOLVED_TEMPLATE",
                    "docs/process/CURRENT_STAGE.md",
                    f"unresolved state placeholder: {marker}",
                    line_number(current_stage, offset),
                )

        frontier = markdown_h2_section(current_stage, FRONTIER_HEADING)
        if frontier is None:
            add_finding(
                findings,
                "BLOCKER",
                "ACTIONABLE_FRONTIER_MISSING",
                "docs/process/CURRENT_STAGE.md",
                "current state must define one '## Next' frontier with Action, Target, and Done when",
            )
        else:
            frontier_offset, frontier_body = frontier
            missing_fields = [
                field for field in FRONTIER_FIELDS if field not in frontier_body
            ]
            vague_reference = VAGUE_FRONTIER_REFERENCE.search(frontier_body)
            has_exact_reference = EXACT_FRONTIER_REFERENCE.search(frontier_body)
            if missing_fields or (vague_reference and not has_exact_reference):
                reasons = []
                if missing_fields:
                    reasons.append("missing " + ", ".join(missing_fields))
                if vague_reference and not has_exact_reference:
                    reasons.append(
                        f"undefined collection reference '{vague_reference.group(0)}'"
                    )
                add_finding(
                    findings,
                    "BLOCKER",
                    "NON_ACTIONABLE_FRONTIER",
                    "docs/process/CURRENT_STAGE.md",
                    "; ".join(reasons)
                    + "; name one exact target and an observable completion condition",
                    line_number(current_stage, frontier_offset),
                )

        duplicate_frontier = markdown_h2_section(
            current_stage, "## Next session frontier"
        )
        if duplicate_frontier is not None:
            duplicate_offset, _ = duplicate_frontier
            add_finding(
                findings,
                "WARNING",
                "DUPLICATE_FRONTIER_SECTION",
                "docs/process/CURRENT_STAGE.md",
                "'## Next' is the sole frontier owner; remove the duplicate next-session section when that state file is next reconciled",
                line_number(current_stage, duplicate_offset),
            )

    git_root = git_root_for(root)
    if git_root is None:
        add_finding(
            findings,
            "WARNING",
            "GIT_NOT_AVAILABLE",
            ".",
            "project is not inside a Git worktree; canonical-file tracking cannot be verified",
        )
    else:
        for relative_path in CANONICAL_PATHS:
            if (root / relative_path).is_file() and not is_tracked(
                git_root, root, relative_path
            ):
                add_finding(
                    findings,
                    "WARNING",
                    "UNTRACKED_CANONICAL_FILE",
                    relative_path,
                    "canonical entry file is not tracked by Git",
                )

    return findings


def emit_text(root: Path, findings: list[dict[str, object]]) -> None:
    print("== governance-audit ==")
    print(f"Root: {root}")
    if not findings:
        print("OK — canonical entry files satisfy the mechanical checks.")
        return

    for finding in findings:
        coordinate = str(finding["path"])
        if "line" in finding:
            coordinate += f":{finding['line']}"
        print(
            f"[{finding['severity']}] {finding['code']} — "
            f"{coordinate}: {finding['message']}"
        )

    blockers = sum(item["severity"] == "BLOCKER" for item in findings)
    warnings = sum(item["severity"] == "WARNING" for item in findings)
    print(f"Findings: {blockers} blocker(s), {warnings} warning(s).")


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        print(f"governance-audit: root is not a directory: {root}", file=sys.stderr)
        return 2

    findings = collect_findings(root)
    if args.json:
        blockers = sum(item["severity"] == "BLOCKER" for item in findings)
        warnings = sum(item["severity"] == "WARNING" for item in findings)
        print(
            json.dumps(
                {
                    "root": str(root),
                    "findings": findings,
                    "summary": {"blockers": blockers, "warnings": warnings},
                },
                indent=2,
                sort_keys=True,
            )
        )
    else:
        emit_text(root, findings)
    return 1 if any(item["severity"] == "BLOCKER" for item in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
