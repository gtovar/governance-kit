#!/usr/bin/env python3
"""check-skills-lock.py — deterministic skills integrity checker (stdlib only).

Verifies that every skill in skills/ matches its SHA-256 recorded in
skills-lock.json. Detects drift and tampering. The lock is the source of
truth for what the kit ships.

Usage:
  python3 scripts/check-skills-lock.py            — verify against the lock
  python3 scripts/check-skills-lock.py --update   — regenerate the lock from skills/
Exit codes: 0 valid, 1 drift detected, 2 cannot run.
"""

import hashlib
import json
import sys
from pathlib import Path

LOCK_PATH = Path(__file__).resolve().parent.parent / "skills-lock.json"


def hash_skill_dir(skill_dir: Path) -> dict[str, str]:
    """Hash every file in the skill dir, keyed by relative path."""
    return {
        str(p.relative_to(skill_dir)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(skill_dir.rglob("*"))
        if p.is_file()
    }


def collect() -> dict[str, dict[str, str]]:
    skills_root = Path(__file__).resolve().parent.parent / "skills"
    out = {}
    for skill_dir in sorted(skills_root.iterdir()):
        if skill_dir.is_dir():
            out[skill_dir.name] = hash_skill_dir(skill_dir)
    return out


def update_lock() -> int:
    lock = {"version": 1, "skills": collect()}
    LOCK_PATH.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n")
    print(f"check-skills-lock: wrote {len(lock['skills'])} skills → {LOCK_PATH}")
    return 0


def verify_lock() -> int:
    if not LOCK_PATH.exists():
        print(f"check-skills-lock: missing {LOCK_PATH}", file=sys.stderr)
        return 2
    try:
        lock = json.loads(LOCK_PATH.read_text())
    except json.JSONDecodeError as e:
        print(f"check-skills-lock: invalid JSON: {e}", file=sys.stderr)
        return 1

    current = collect()
    lock_skills = lock.get("skills", {})
    errors = []

    for name, files in sorted(current.items()):
        if name not in lock_skills:
            errors.append(f"{name}: not in lock (new skill — run --update)")
            continue
        locked = lock_skills[name]
        for rel, h in sorted(files.items()):
            if locked.get(rel) != h:
                errors.append(f"{name}/{rel}: hash mismatch (drift detected)")
        for rel in locked:
            if rel not in files:
                errors.append(f"{name}/{rel}: in lock but missing on disk")

    for name in lock_skills:
        if name not in current:
            errors.append(f"{name}: in lock but missing on disk")

    if errors:
        for e in errors:
            print(f"check-skills-lock: {e}", file=sys.stderr)
        return 1

    print(f"check-skills-lock: OK — {len(current)} skills verified")
    return 0


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--update":
        return update_lock()
    return verify_lock()


if __name__ == "__main__":
    sys.exit(main())
