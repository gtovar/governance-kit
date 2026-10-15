#!/usr/bin/env python3
"""Surface the installed checker's real result without changing the project."""

import importlib.util
import io
import json
from contextlib import redirect_stdout
from pathlib import Path


def check_message(root: Path) -> str:
    checker_path = root / "scripts/governance-kit-update.py"
    spec = importlib.util.spec_from_file_location("governance_update_checker", checker_path)
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)
    output = io.StringIO()
    with redirect_stdout(output):
        result = checker.cmd_check(root)
    message = output.getvalue().strip()
    if message:
        return message.splitlines()[0]
    if result != 0:
        raise RuntimeError(f"checker exited with status {result}")
    return "governance-kit: no newer published release found for the recorded installed version."


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    try:
        message = check_message(root)
    except Exception as error:
        # A broken optional checker must report uncertainty, never block startup.
        message = f"governance-kit update check unavailable: {type(error).__name__}: {error}"
    print(json.dumps({
        "systemMessage": message,
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": message + " This startup check is advisory; do not apply updates without user approval.",
        },
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
