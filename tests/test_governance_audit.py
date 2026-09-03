#!/usr/bin/env python3
"""Integration tests for the advisory governance readiness audit."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


KIT_ROOT = Path(__file__).resolve().parent.parent
AUDIT = KIT_ROOT / "scripts/governance-audit.py"


class GovernanceAuditIntegrationTest(unittest.TestCase):
    def write(self, root: Path, relative_path: str, content: str) -> None:
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    def create_project(
        self,
        root: Path,
        *,
        readme: str | None = None,
        current_extra: str = "",
        project_map: str = "# Mapa del proyecto\n\n**Fase actual:** F1\n",
        workflow_extra: str = "",
    ) -> None:
        if readme is None:
            readme = """# Example

Canonical purpose.

## Repository navigation

- [AGENTS.md](AGENTS.md)
- [docs/index.md](docs/index.md)
- [CURRENT_STAGE](docs/process/CURRENT_STAGE.md)
- [PROJECT_MAP](docs/process/PROJECT_MAP.md)
- [DEVELOPMENT_WORKFLOW](docs/process/DEVELOPMENT_WORKFLOW.md)
"""
        self.write(root, "AGENTS.md", "# Constitution\n")
        self.write(root, "README.md", readme)
        self.write(root, "docs/index.md", "# Index\n")
        self.write(
            root,
            "docs/process/CURRENT_STAGE.md",
            (
                "# Current Stage\n\n"
                "F0 — Foundation\n\n"
                "## Next\n\n"
                "Action: Verify repository entry\n"
                "Target: `README.md`\n"
                "Done when: README identifies the project and canonical navigation.\n\n"
                f"{current_extra}\n"
            ),
        )
        self.write(root, "docs/process/PROJECT_MAP.md", project_map)
        self.write(
            root,
            "docs/process/DEVELOPMENT_WORKFLOW.md",
            f"# Workflow\n\n{workflow_extra}\n",
        )

    def run_audit(self, root: Path) -> tuple[subprocess.CompletedProcess[str], dict]:
        result = subprocess.run(
            [sys.executable, str(AUDIT), "--root", str(root), "--json"],
            check=False,
            text=True,
            capture_output=True,
        )
        return result, json.loads(result.stdout)

    def test_clean_tracked_project_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "project"
            root.mkdir()
            self.create_project(
                root,
                current_extra="A literal <component> example is valid project prose.",
                workflow_extra="Gate: cualquier agente nuevo puede entrar.",
            )
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            subprocess.run(["git", "-C", str(root), "add", "."], check=True)

            result, report = self.run_audit(root)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(report["findings"], [])

    def test_reports_exact_templates_navigation_and_missing_git(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "project"
            root.mkdir()
            self.create_project(
                root,
                readme="# <Project Name>\n\nBrief description of its purpose.\n",
                current_extra="**Updated:** <DATE>",
                workflow_extra="Gate: any new agent can understand the project.",
            )

            result, report = self.run_audit(root)
            codes = {finding["code"] for finding in report["findings"]}

            self.assertEqual(result.returncode, 1)
            self.assertIn("UNRESOLVED_TEMPLATE", codes)
            self.assertIn("README_NAVIGATION_MISSING", codes)
            self.assertIn("GIT_NOT_AVAILABLE", codes)
            self.assertNotIn("UNVERIFIABLE_AGENT_CLAIM", codes)
            self.assertNotIn("CURRENT_PHASE_NOT_FOUND", codes)

    def test_reports_untracked_canonical_files_without_semantic_inference(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "project"
            root.mkdir()
            self.create_project(
                root,
                current_extra="Next: Personalize README.md.",
                project_map="# Project Map\n\nThe phase format is project-owned.\n",
                workflow_extra="Gate: any agent can enter.",
            )
            subprocess.run(["git", "init", "-q", str(root)], check=True)

            result, report = self.run_audit(root)
            codes = {finding["code"] for finding in report["findings"]}

            self.assertEqual(result.returncode, 0)
            self.assertEqual(codes, {"UNTRACKED_CANONICAL_FILE"})

    def test_reports_a_non_actionable_frontier_as_a_blocker(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "project"
            root.mkdir()
            self.create_project(root)
            self.write(
                root,
                "docs/process/CURRENT_STAGE.md",
                """# Current Stage

F0 — Foundation

## Next

- Review the remaining F0 findings before authorizing further changes.
""",
            )

            result, report = self.run_audit(root)
            findings = {
                finding["code"]: finding for finding in report["findings"]
            }

            self.assertEqual(result.returncode, 1)
            self.assertIn("NON_ACTIONABLE_FRONTIER", findings)
            self.assertEqual(
                findings["NON_ACTIONABLE_FRONTIER"]["severity"], "BLOCKER"
            )
            self.assertIn(
                "undefined collection reference",
                findings["NON_ACTIONABLE_FRONTIER"]["message"],
            )

    def test_reports_a_circular_process_reference_as_a_blocker(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "project"
            root.mkdir()
            self.create_project(
                root,
                project_map=(
                    "# Project Map\n\n"
                    "For current work, CURRENT_STAGE.md is authoritative; "
                    "read it directly.\n"
                ),
            )
            self.write(
                root,
                "docs/process/CURRENT_STAGE.md",
                """# Current Stage

F0 — Foundation

## Next

Action: Consult the project map
Target: `docs/process/PROJECT_MAP.md`
Done when: The next frontier has been selected.
""",
            )

            result, report = self.run_audit(root)
            findings = {
                finding["code"]: finding for finding in report["findings"]
            }

            self.assertEqual(result.returncode, 1)
            self.assertIn("CIRCULAR_FRONTIER_REFERENCE", findings)
            self.assertEqual(
                findings["CIRCULAR_FRONTIER_REFERENCE"]["severity"], "BLOCKER"
            )

    def test_duplicate_frontier_is_warning_and_does_not_fail(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "project"
            root.mkdir()
            self.create_project(
                root,
                current_extra=(
                    "## Next session frontier\n\n"
                    "- Repeat the same entry check.\n"
                ),
            )
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            subprocess.run(["git", "-C", str(root), "add", "."], check=True)

            result, report = self.run_audit(root)

            self.assertEqual(result.returncode, 0)
            self.assertEqual(
                {finding["code"] for finding in report["findings"]},
                {"DUPLICATE_FRONTIER_SECTION"},
            )

    def test_reports_a_missing_canonical_entry_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "project"
            root.mkdir()
            self.create_project(root)
            (root / "docs/process/PROJECT_MAP.md").unlink()

            result, report = self.run_audit(root)

            self.assertEqual(result.returncode, 1)
            self.assertTrue(
                any(
                    finding["code"] == "MISSING_CANONICAL_FILE"
                    and finding["path"] == "docs/process/PROJECT_MAP.md"
                    for finding in report["findings"]
                )
            )


if __name__ == "__main__":
    unittest.main()
