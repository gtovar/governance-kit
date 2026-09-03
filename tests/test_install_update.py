#!/usr/bin/env python3
"""Integration tests for portable skill installation and safe updates."""

import hashlib
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path


KIT_ROOT = Path(__file__).resolve().parent.parent
INSTALLER = KIT_ROOT / "bin" / "install.sh"
CHECKER = KIT_ROOT / "scripts" / "governance-kit-update.py"


class InstallUpdateIntegrationTest(unittest.TestCase):
    def run_installer(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(INSTALLER), *args],
            check=True,
            cwd=KIT_ROOT,
            text=True,
            capture_output=True,
        )

    def run_updater(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(KIT_ROOT / "scripts/update.py"), *args],
            check=True,
            cwd=KIT_ROOT,
            text=True,
            capture_output=True,
        )

    def test_project_install_vendors_skills_for_opencode_and_codex(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "project"

            self.run_installer(str(target))

            skill_files = ("SKILL.md", "references/reconciliation.md")
            destinations = []
            for destination_root in (".opencode/skills", ".agents/skills"):
                for relative_path in skill_files:
                    source = (
                        KIT_ROOT
                        / "skills/governance-gatekeeper"
                        / relative_path
                    )
                    destination = (
                        target
                        / destination_root
                        / "governance-gatekeeper"
                        / relative_path
                    )
                    self.assertEqual(destination.read_bytes(), source.read_bytes())
                    destinations.append(destination)

            manifest = json.loads(
                (target / ".governance-kit/manifest.json").read_text()
            )
            for destination in destinations:
                relative_path = str(destination.relative_to(target))
                self.assertIn(relative_path, manifest["files"])
            for process_doc in (
                "docs/process/CURRENT_STAGE.md",
                "docs/process/PROJECT_MAP.md",
                "docs/process/DEVELOPMENT_WORKFLOW.md",
            ):
                self.assertIn(process_doc, manifest["files"])
            self.assertEqual(
                manifest["distribution"]["github_repository"],
                "gtovar/governance-kit",
            )
            self.assertEqual(manifest["distribution"]["installed_version"], "0.3.0")

            audit = target / "scripts/governance-audit.py"
            self.assertTrue(audit.is_file())
            self.assertTrue(os.access(audit, os.X_OK))
            self.assertTrue((target / "scripts/governance-kit-update.py").is_file())

    def test_install_records_configured_github_release_source(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "project"

            self.run_installer(str(target), "--github-repo", "example/governance-kit")

            manifest = json.loads(
                (target / ".governance-kit/manifest.json").read_text()
            )
            self.assertEqual(manifest["version"], 3)
            self.assertEqual(
                manifest["distribution"]["github_repository"],
                "example/governance-kit",
            )
            self.assertEqual(manifest["distribution"]["installed_version"], "0.3.0")

    def test_configure_update_migrates_a_legacy_install(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "project"
            self.run_installer(str(target))
            (target / "scripts/governance-kit-update.py").unlink()
            manifest_path = target / ".governance-kit/manifest.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["files"].pop("scripts/governance-kit-update.py")
            manifest.pop("distribution", None)
            manifest_path.write_text(json.dumps(manifest))

            result = subprocess.run(
                [
                    str(INSTALLER),
                    "configure-update",
                    str(target),
                    "--github-repo",
                    "example/governance-kit",
                ],
                check=True,
                cwd=KIT_ROOT,
                text=True,
                capture_output=True,
            )

            configured = json.loads(manifest_path.read_text())
            self.assertIn("configured GitHub Releases source", result.stdout)
            self.assertTrue((target / "scripts/governance-kit-update.py").is_file())
            self.assertEqual(
                configured["distribution"]["github_repository"],
                "example/governance-kit",
            )
            self.assertEqual(configured["distribution"]["installed_version"], "0.0.0")

    def test_installed_update_checker_fails_open_without_source(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "project"
            self.run_installer(str(target))
            manifest_path = target / ".governance-kit/manifest.json"
            manifest = json.loads(manifest_path.read_text())
            manifest.pop("distribution", None)
            manifest_path.write_text(json.dumps(manifest))

            result = subprocess.run(
                [sys.executable, "scripts/governance-kit-update.py", "check"],
                cwd=target,
                check=False,
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0)
            self.assertIn("not configured", result.stdout)

    def test_installed_update_checker_configures_default_source(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "project"
            target.mkdir()
            manifest_path = target / ".governance-kit/manifest.json"
            manifest_path.parent.mkdir()
            manifest_path.write_text(json.dumps({"version": 3, "files": {}}))

            result = subprocess.run(
                [sys.executable, str(CHECKER), "configure", "--root", str(target)],
                check=False,
                text=True,
                capture_output=True,
            )

            manifest = json.loads(manifest_path.read_text())
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("configured: gtovar/governance-kit", result.stdout)
            self.assertEqual(
                manifest["distribution"]["github_repository"],
                "gtovar/governance-kit",
            )
            self.assertEqual(manifest["distribution"]["installed_version"], "0.0.0")

    def test_update_checker_reports_a_newer_github_release(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "project"
            manifest_path = target / ".governance-kit/manifest.json"
            manifest_path.parent.mkdir(parents=True)
            manifest_path.write_text(
                json.dumps(
                    {
                        "version": 3,
                        "distribution": {
                            "github_repository": "example/governance-kit",
                            "installed_version": "0.1.0",
                        },
                        "files": {},
                    }
                )
            )
            spec = importlib.util.spec_from_file_location("kit_update_checker", CHECKER)
            assert spec and spec.loader
            checker = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(checker)
            checker.request_release = lambda _repository: {
                "tag_name": "v0.1.1",
                "body": "- Commit boundary\n",
                "html_url": "https://example.test/releases/v0.1.1",
            }
            output = io.StringIO()
            with redirect_stdout(output):
                result = checker.cmd_check(target)

            self.assertEqual(result, 0)
            self.assertIn("0.1.0 -> v0.1.1", output.getvalue())
            self.assertIn("Commit boundary", output.getvalue())

    def test_project_install_does_not_audit_unpersonalized_templates(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "project"

            result = self.run_installer(str(target))

            self.assertNotIn("advisory governance audit", result.stdout)

    def test_update_runs_trusted_audit_not_customized_project_copy(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "project"
            self.run_installer(str(target))
            project_audit = target / "scripts/governance-audit.py"
            project_audit.write_text(
                "from pathlib import Path\n"
                "Path('CUSTOM_AUDIT_RAN').write_text('yes')\n"
            )

            result = self.run_installer("update", str(target))

            self.assertFalse((target / "CUSTOM_AUDIT_RAN").exists())
            self.assertIn("advisory governance audit", result.stdout)
            self.assertIn(
                "resolve only the blocker coordinates above",
                result.stdout,
            )

    def test_installed_start_ritual_runs_governance_audit_once(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "project"

            self.run_installer(str(target))

            ritual = (target / "docs/session_rituals.md").read_text()
            self.assertIn(
                "run it once after reading the\n   canonical entry documents",
                ritual,
            )
            self.assertIn(
                "blockers: make `reconcile` the primary intent",
                ritual,
            )

    def test_project_install_delivers_proactive_commit_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "project"

            self.run_installer(str(target))

            constitution = (target / "AGENTS.md").read_text()
            git_hygiene = (target / "docs/git_hygiene.md").read_text()
            session_rituals = (target / "docs/session_rituals.md").read_text()
            self.assertIn("## Commit boundary", constitution)
            self.assertIn("before starting new implementation", constitution)
            self.assertIn("Commit boundary before scope expansion", git_hygiene)
            self.assertIn("`commit-readiness` decision", session_rituals)

            for destination_root in (".opencode/skills", ".agents/skills"):
                gatekeeper = (
                    target
                    / destination_root
                    / "governance-gatekeeper"
                    / "SKILL.md"
                ).read_text()
                self.assertIn("### Proactive commit boundary", gatekeeper)
                self.assertIn("Do not stage, stash, commit, push", gatekeeper)

    def test_update_delivers_automatic_audit_to_an_older_managed_ritual(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "project"
            self.run_installer(str(target))
            ritual_path = target / "docs/session_rituals.md"
            legacy_content = "# Session Rituals\n\nLegacy managed content.\n"
            ritual_path.write_text(legacy_content)

            manifest_path = target / ".governance-kit/manifest.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["files"]["docs/session_rituals.md"]["hash"] = (
                hashlib.sha256(legacy_content.encode()).hexdigest()
            )
            manifest_path.write_text(
                json.dumps(manifest, indent=2, sort_keys=True) + "\n"
            )

            result = self.run_installer("update", str(target))

            self.assertIn("docs/session_rituals.md", result.stdout)
            self.assertIn(
                "run it once after reading the\n   canonical entry documents",
                ritual_path.read_text(),
            )

    def test_update_reports_all_project_owned_process_documents_as_protected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "project"
            self.run_installer(str(target))
            current_stage = target / "docs/process/CURRENT_STAGE.md"
            customized_content = "# Project-owned current stage\n"
            current_stage.write_text(customized_content)
            manifest_path = target / ".governance-kit/manifest.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["files"] = {
                path: entry
                for path, entry in manifest["files"].items()
                if not path.startswith("docs/process/")
            }
            manifest_path.write_text(
                json.dumps(manifest, indent=2, sort_keys=True) + "\n"
            )

            result = self.run_installer("update", str(target))

            self.assertEqual(current_stage.read_text(), customized_content)
            self.assertIn(
                "protected project-owned docs — kept (conscious review): 6",
                result.stdout,
            )
            for process_doc in (
                "docs/process/CURRENT_STAGE.md",
                "docs/process/PROJECT_MAP.md",
                "docs/process/DEVELOPMENT_WORKFLOW.md",
            ):
                self.assertIn(f"  - {process_doc}", result.stdout)

    def test_update_refreshes_unchanged_constitution_but_keeps_project_state(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "project"
            next_kit = Path(temp_dir) / "next-kit"
            self.run_installer(str(target))
            original_state = (target / "PROJECT_STATE.md").read_text()
            shutil.copytree(KIT_ROOT, next_kit, ignore=shutil.ignore_patterns(".git"))
            next_constitution = next_kit / "core/AGENTS.md"
            next_constitution.write_text(
                next_constitution.read_text() + "\n## Test release rule\n\nTest only.\n"
            )

            result = self.run_updater("update", str(next_kit), str(target))

            self.assertIn("AGENTS.md", result.stdout)
            self.assertIn("Test release rule", (target / "AGENTS.md").read_text())
            self.assertEqual((target / "PROJECT_STATE.md").read_text(), original_state)

    def test_update_adds_codex_skills_to_a_legacy_install(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "project"
            self.run_installer(str(target))

            shutil.rmtree(target / ".agents")
            manifest_path = target / ".governance-kit/manifest.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["files"] = {
                path: entry
                for path, entry in manifest["files"].items()
                if not path.startswith(".agents/skills/")
            }
            manifest_path.write_text(
                json.dumps(manifest, indent=2, sort_keys=True) + "\n"
            )

            result = self.run_installer("update", str(target))

            installed_skill = (
                target / ".agents/skills/governance-gatekeeper/SKILL.md"
            )
            self.assertTrue(installed_skill.is_file())
            self.assertIn("installed (new from kit)", result.stdout)

    def test_reinstall_does_not_overwrite_project_skill_customization(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "project"
            self.run_installer(str(target))
            skill_path = target / ".agents/skills/governance-gatekeeper/SKILL.md"
            customized_content = "project-specific customization\n"
            skill_path.write_text(customized_content)

            self.run_installer(str(target))

            self.assertEqual(skill_path.read_text(), customized_content)

    def test_installed_doc_health_ignores_vendored_skill_documents(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "project"
            self.run_installer(str(target))

            result = subprocess.run(
                [str(target / "scripts/doc-health.sh")],
                check=False,
                cwd=target,
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_source_kit_doc_health_uses_core_layout(self) -> None:
        result = subprocess.run(
            [str(KIT_ROOT / "scripts/doc-health.sh")],
            check=False,
            cwd=KIT_ROOT,
            text=True,
            capture_output=True,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_source_kit_registry_check_uses_core_layout(self) -> None:
        result = subprocess.run(
            [sys.executable, str(KIT_ROOT / "scripts/check-registry.py")],
            check=False,
            cwd=KIT_ROOT,
            text=True,
            capture_output=True,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
