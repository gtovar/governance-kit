#!/usr/bin/env python3
"""Integration tests for scripts/doc-health.sh (ignore file handling and failure reporting)."""

import os
import shutil
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path


KIT_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_SOURCE = KIT_ROOT / "scripts/doc-health.sh"
BROKEN_FENCE = "```\nnever closed\n"


class DocHealthTest(unittest.TestCase):
    def run_script(self, root: Path) -> subprocess.CompletedProcess[str]:
        # doc-health.sh resolves its root from its own location, so it is
        # copied into <root>/scripts/ exactly as it runs in an installed project.
        installed = root / "scripts/doc-health.sh"
        installed.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SCRIPT_SOURCE, installed)
        installed.chmod(installed.stat().st_mode | stat.S_IEXEC)
        return subprocess.run([str(installed)], cwd=root, check=False, text=True, capture_output=True)

    def write(self, root: Path, relative: str, text: str) -> None:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def installed_project(self, root: Path) -> None:
        self.write(root, "docs/index.md", "# Index\n\n- [kept](kept.md)\n")
        self.write(root, "docs/kept.md", "# Kept\n")

    def test_clean_project_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.installed_project(root)
            result = self.run_script(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("OK — doc-health limpio", result.stdout)

    def test_unbalanced_fence_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.installed_project(root)
            self.write(root, "docs/broken.md", BROKEN_FENCE)
            result = self.run_script(root)
            self.assertEqual(result.returncode, 1, result.stdout)
            self.assertIn("FENCE DESBALANCEADO: docs/broken.md", result.stdout)

    def test_ignore_entry_with_spaces_excludes_only_that_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.installed_project(root)
            self.write(root, "docs/generated screens/a b.md", BROKEN_FENCE)
            self.write(root, "docs/broken.md", BROKEN_FENCE)
            self.write(root, ".doc-health-ignore", "# generated\ndocs/generated screens/a b.md\n")
            result = self.run_script(root)
            # The spaced entry must not turn the whole run into a false "clean".
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("FENCE DESBALANCEADO: docs/broken.md", result.stdout)
            self.assertNotIn("a b.md", result.stdout)

    def test_ignore_entry_with_spaces_alone_keeps_a_clean_run_clean(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.installed_project(root)
            self.write(root, "docs/generated screens/a b.md", BROKEN_FENCE)
            self.write(root, ".doc-health-ignore", "docs/generated screens/a b.md\n")
            result = self.run_script(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_ignore_entry_is_repository_relative_in_source_layout(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            # Source layout: no docs/index.md at the root, only core/docs/index.md.
            self.write(root, "core/docs/index.md", "# Index\n\n- [kept](kept.md)\n")
            self.write(root, "core/docs/kept.md", "# Kept\n")
            self.write(root, "core/docs/ignored.md", BROKEN_FENCE)
            self.write(root, ".doc-health-ignore", "core/docs/ignored.md\n")
            result = self.run_script(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_unreadable_tree_fails_instead_of_reporting_clean(self) -> None:
        if os.geteuid() == 0:
            self.skipTest("permissions are not enforced for root")
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.installed_project(root)
            blocked = root / "docs/blocked"
            blocked.mkdir()
            blocked.chmod(0)
            try:
                result = self.run_script(root)
            finally:
                blocked.chmod(0o755)
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertNotIn("limpio", result.stdout)


if __name__ == "__main__":
    unittest.main()
