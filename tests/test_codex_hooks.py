"""Verify truthful hook output and opt-in installation across real file layouts."""

import importlib.util
import io
import json
import runpy
import subprocess
import tempfile
import unittest
import urllib.error
from pathlib import Path
from contextlib import redirect_stdout
from unittest.mock import patch


KIT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "codex_hook", KIT / "adapters/codex/hooks/governance-update.py"
)
hook = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hook)


class CodexHookTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="governance hook ")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        subprocess.run([str(KIT / "bin/install.sh"), str(self.root), "--adapter", "codex"],
                       check=True, capture_output=True)
        self.manifest_path = self.root / ".governance-kit/manifest.json"
        manifest = json.loads(self.manifest_path.read_text())
        manifest["distribution"]["installed_version"] = "0.1.1"
        self.manifest_path.write_text(json.dumps(manifest))

    def test_available_equal_and_ahead_use_actual_comparison(self):
        for version, expected in [("v0.3.0", "0.1.1 -> v0.3.0"),
                                  ("v0.1.1", "no newer published release"),
                                  ("v0.1.0", "no newer published release")]:
            with self.subTest(version=version), patch("urllib.request.urlopen") as request:
                request.return_value = io.BytesIO(json.dumps({"tag_name": version}).encode())
                message = hook.check_message(self.root)
                self.assertIn(expected, message)
                self.assertIn("gtovar/governance-kit/releases/latest", request.call_args.args[0].full_url)

    def test_network_failure_never_claims_current(self):
        with patch("urllib.request.urlopen", side_effect=urllib.error.URLError("offline")):
            message = hook.check_message(self.root)
        self.assertIn("unavailable", message)
        self.assertNotIn("no newer", message)

    def test_installed_entrypoint_reports_available_release_as_ui_warning(self):
        output = io.StringIO()
        with patch("urllib.request.urlopen", return_value=io.BytesIO(b'{"tag_name":"v0.3.0"}')):
            with redirect_stdout(output), self.assertRaises(SystemExit) as exit_result:
                runpy.run_path(str(self.root / ".codex/hooks/governance-update.py"), run_name="__main__")
        self.assertEqual(exit_result.exception.code, 0)
        self.assertEqual(json.loads(output.getvalue())["systemMessage"],
                         "governance-kit update available: 0.1.1 -> v0.3.0")

    def test_missing_checker_is_visible_without_blocking_startup(self):
        (self.root / "scripts/governance-kit-update.py").unlink()
        result = subprocess.run(["python3", str(self.root / ".codex/hooks/governance-update.py")],
                                text=True, capture_output=True, check=True)
        self.assertIn("unavailable: FileNotFoundError", json.loads(result.stdout)["systemMessage"])

    def test_invalid_release_and_missing_source_report_uncertainty(self):
        with patch("urllib.request.urlopen", return_value=io.BytesIO(b'{"tag_name":"invalid"}')):
            self.assertIn("unavailable", hook.check_message(self.root))
        self.manifest_path.write_text('{"distribution": {}}')
        self.assertIn("not configured", hook.check_message(self.root))

    def test_configured_command_from_subdirectory_emits_ui_json_on_failure(self):
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        nested = self.root / "nested directory"
        nested.mkdir()
        self.manifest_path.write_text('{"distribution": {}}')
        config = json.loads((self.root / ".codex/hooks.json").read_text())
        command = config["hooks"]["SessionStart"][0]["hooks"][0]["command"]
        result = subprocess.run(command, shell=True, cwd=nested, capture_output=True, text=True, check=True)
        output = json.loads(result.stdout)
        self.assertIn("not configured", output["systemMessage"])
        self.assertEqual(output["hookSpecificOutput"]["hookEventName"], "SessionStart")
        self.assertNotIn("continue", output)

    def test_reinstall_keeps_version_custom_hooks_and_baselines(self):
        before = json.loads(self.manifest_path.read_text())
        hooks_path = self.root / ".codex/hooks.json"
        hooks_path.write_text('{"hooks": {}}')
        subprocess.run([str(KIT / "bin/install.sh"), str(self.root), "--adapter", "codex"],
                       check=True, capture_output=True)
        after = json.loads(self.manifest_path.read_text())
        self.assertEqual(after["distribution"]["installed_version"], "0.1.1")
        self.assertEqual(after["files"], before["files"])
        self.assertEqual(hooks_path.read_text(), '{"hooks": {}}')

    def test_update_adds_hooks_only_for_existing_codex_adapter(self):
        for relative in (".codex/hooks.json", ".codex/hooks/governance-update.py"):
            (self.root / relative).unlink()
        subprocess.run(["python3", str(KIT / "scripts/update.py"), "update", str(KIT), str(self.root)],
                       check=True, capture_output=True)
        self.assertTrue((self.root / ".codex/hooks.json").is_file())
        with tempfile.TemporaryDirectory() as plain:
            subprocess.run([str(KIT / "bin/install.sh"), plain], check=True, capture_output=True)
            subprocess.run(["python3", str(KIT / "scripts/update.py"), "update", str(KIT), plain],
                           check=True, capture_output=True)
            self.assertFalse((Path(plain) / ".codex/hooks.json").exists())

    def test_preexisting_hooks_are_not_claimed_as_kit_owned(self):
        with tempfile.TemporaryDirectory() as existing:
            root = Path(existing)
            (root / ".codex").mkdir()
            custom = root / ".codex/hooks.json"
            custom.write_text('{"hooks": {}, "description": "project owned"}')
            subprocess.run([str(KIT / "bin/install.sh"), existing, "--adapter", "codex"],
                           check=True, capture_output=True)
            manifest = json.loads((root / ".governance-kit/manifest.json").read_text())
            self.assertNotIn(".codex/hooks.json", manifest["files"])
            subprocess.run(["python3", str(KIT / "scripts/update.py"), "update", str(KIT), existing],
                           check=True, capture_output=True)
            self.assertEqual(json.loads(custom.read_text())["description"], "project owned")


if __name__ == "__main__":
    unittest.main()
