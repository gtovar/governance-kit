#!/usr/bin/env python3
"""Integration tests for scripts/log-hygiene.sh (size checks + archival)."""

import shutil
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path


KIT_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_SOURCE = KIT_ROOT / "scripts/log-hygiene.sh"


def entry_count(text: str) -> int:
    return sum(1 for line in text.splitlines() if line.startswith("## 20") or line.startswith("### 20"))


class LogHygieneTest(unittest.TestCase):
    def run_script(self, cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
        # log-hygiene.sh (like doc-health.sh) resolves its root from its own
        # location (dirname "$0")/..), not from the caller's cwd — it must be
        # invoked as <root>/scripts/log-hygiene.sh for <root> to be the target
        # under test, exactly as it runs once installed into a real project.
        installed = cwd / "scripts/log-hygiene.sh"
        installed.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SCRIPT_SOURCE, installed)
        installed.chmod(installed.stat().st_mode | stat.S_IEXEC)
        return subprocess.run(
            [str(installed), *args],
            cwd=cwd,
            check=False,
            text=True,
            capture_output=True,
        )

    def make_dated_log(self, root: Path, name: str, dates: list[str], level: str = "##") -> Path:
        path = root / name
        lines = [f"# {name}", "", "Intro line.", ""]
        for date in dates:
            lines += [f"{level} {date} — entry", "- did something", "- learned something", ""]
        path.write_text("\n".join(lines))
        return path

    # ---- check ----

    def test_check_clean_when_nothing_present(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            result = self.run_script(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("OK — log-hygiene limpio", result.stdout)

    def test_check_flags_oversized_project_state(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "PROJECT_STATE.md").write_text("line\n" * 401)
            result = self.run_script(root, "check")
            self.assertEqual(result.returncode, 1)
            self.assertIn("PROJECT_STATE.md EXCEDE", result.stdout)

    def test_check_flags_oversized_readme_reentry(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "README_REENTRY.md").write_text("line\n" * 301)
            result = self.run_script(root, "check")
            self.assertEqual(result.returncode, 1)
            self.assertIn("README_REENTRY.md EXCEDE", result.stdout)

    def test_check_flags_oversized_pending_work(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            docs = root / "docs"
            docs.mkdir()
            (docs / "PENDING_WORK.md").write_text("line\n" * 301)
            result = self.run_script(root, "check")
            self.assertEqual(result.returncode, 1)
            self.assertIn("docs/PENDING_WORK.md EXCEDE", result.stdout)

    def test_check_flags_oversized_sprint_log_and_recommends_archive(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "Sprint_Log.md").write_text("line\n" * 1501)
            result = self.run_script(root, "check")
            self.assertEqual(result.returncode, 1)
            self.assertIn("Sprint_Log.md EXCEDE el umbral de archivado", result.stdout)
            self.assertIn("log-hygiene.sh archive Sprint_Log.md", result.stdout)

    def test_check_flags_learning_inbox_entry_count(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.make_dated_log(
                root,
                "LEARNING_CAPTURE_INBOX.md",
                [f"2026-01-{i:02d}" for i in range(1, 22)],
                level="###",
            )
            result = self.run_script(root, "check")
            self.assertEqual(result.returncode, 1)
            self.assertIn("LEARNING_CAPTURE_INBOX.md EXCEDE 20 entradas", result.stdout)

    def test_check_healthy_files_stay_clean(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "PROJECT_STATE.md").write_text("line\n" * 50)
            (root / "README_REENTRY.md").write_text("line\n" * 50)
            self.make_dated_log(root, "Sprint_Log.md", ["2026-01-01", "2026-01-02"])
            result = self.run_script(root, "check")
            self.assertEqual(result.returncode, 0, result.stdout)

    # ---- archive ----

    def test_archive_moves_old_entries_and_preserves_content(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            dates = [f"2026-01-{i:02d}" for i in range(1, 26)]
            log = self.make_dated_log(root, "Sprint_Log.md", dates)
            original = log.read_text()

            result = self.run_script(root, "archive", "Sprint_Log.md", "--keep", "20")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

            active = log.read_text()
            archive = (root / "Sprint_Log_ARCHIVE.md").read_text()

            self.assertEqual(entry_count(active), 20)
            self.assertEqual(entry_count(archive), 5)
            self.assertIn("Older entries archived in", active)
            self.assertIn("Sprint_Log_ARCHIVE.md", active)

            # Byte-for-byte integrity: archive + active's entry region reproduces
            # the original entry region exactly (this caught a real off-by-one
            # bug for --keep 0 during development — kept as a regression test).
            first_heading = original.index("## 2026-01-01")
            active_first_heading = active.index("## 2026-01-06")
            reconstructed = archive + active[active_first_heading:]
            self.assertEqual(reconstructed, original[first_heading:])

    def test_archive_noop_when_within_keep(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            log = self.make_dated_log(root, "Sprint_Log.md", ["2026-01-01", "2026-01-02"])
            original = log.read_text()

            result = self.run_script(root, "archive", "Sprint_Log.md", "--keep", "20")
            self.assertEqual(result.returncode, 0)
            self.assertIn("nada que archivar", result.stdout)
            self.assertEqual(log.read_text(), original)
            self.assertFalse((root / "Sprint_Log_ARCHIVE.md").exists())

    def test_archive_keep_zero_archives_everything_without_corruption(self) -> None:
        # Regression test: --keep 0 originally produced broken sed ranges
        # (empty cutoff_line) and corrupted output. Found via testing against
        # a real 1.2MB production Sprint_Log.md, fixed before shipping.
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            log = self.make_dated_log(root, "Sprint_Log.md", ["2026-03-01", "2026-03-02"])

            result = self.run_script(root, "archive", "Sprint_Log.md", "--keep", "0")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertNotIn("sed:", result.stdout + result.stderr)

            active = log.read_text()
            archive = (root / "Sprint_Log_ARCHIVE.md").read_text()
            self.assertEqual(entry_count(active), 0)
            self.assertEqual(entry_count(archive), 2)
            self.assertIn("Older entries archived in", active)

    def test_archive_appends_to_existing_archive_cumulatively(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            log = self.make_dated_log(
                root, "LEARNING_CAPTURE_INBOX.md", ["2026-02-01", "2026-02-02", "2026-02-03"], level="###"
            )
            self.run_script(root, "archive", "LEARNING_CAPTURE_INBOX.md", "--keep", "1")

            with log.open("a") as f:
                for date in ["2026-02-04", "2026-02-05", "2026-02-06"]:
                    f.write(f"\n### {date} — entry\n- x\n")

            self.run_script(root, "archive", "LEARNING_CAPTURE_INBOX.md", "--keep", "1")

            archive = (root / "LEARNING_CAPTURE_INBOX_ARCHIVE.md").read_text()
            self.assertEqual(entry_count(archive), 5)  # 2 from first run + 3 from second
            self.assertEqual(entry_count(log.read_text()), 1)

    def test_archive_rejects_missing_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.run_script(Path(temp_dir), "archive", "nope.md")
            self.assertEqual(result.returncode, 2)

    def test_archive_rejects_non_numeric_keep(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.make_dated_log(root, "Sprint_Log.md", ["2026-01-01"])
            result = self.run_script(root, "archive", "Sprint_Log.md", "--keep", "abc")
            self.assertEqual(result.returncode, 2)

    def test_archive_rejects_file_without_dated_headings(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "plain.md").write_text("# Just a doc\n\nNo dated entries here.\n")
            result = self.run_script(root, "archive", "plain.md")
            self.assertEqual(result.returncode, 2)

    def test_unknown_command_is_usage_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.run_script(Path(temp_dir), "bogus")
            self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
