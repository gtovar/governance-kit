#!/usr/bin/env python3
"""check-registry.py — deterministic structural validator for instruction-registry.json.

Validates the registry against its schema shape (stdlib only, no network):
required fields, type enums, severity enums, duplicate ids, missing vehicle.

Exit codes:
  0 = registry valid
  1 = registry invalid (fix before trusting the catalog)
  2 = could not run reliably (file missing)

Usage: python3 scripts/check-registry.py [path-to-instruction-registry.json]
"""

import json
import sys
from pathlib import Path

VALID_TYPES = {"hard_rule", "soft_preference", "style", "memory", "workflow", "decision_gate"}
VALID_SEVERITIES = {"info", "warn", "block"}
REQUIRED_FIELDS = {"id", "type", "category", "requirement", "severity"}


def default_registry_path() -> Path:
    project_path = Path("docs/instruction-registry.json")
    if project_path.exists():
        return project_path

    kit_path = Path(__file__).resolve().parent.parent / "core/docs/instruction-registry.json"
    if kit_path.exists():
        return kit_path
    return project_path


def fail(msg: str) -> int:
    print(f"check-registry: {msg}", file=sys.stderr)
    return 1


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else default_registry_path()
    if not path.exists():
        print(f"check-registry: missing registry file: {path}", file=sys.stderr)
        return 2

    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        return fail(f"invalid JSON: {e}")

    errors = []

    if "version" not in data:
        errors.append("missing 'version'")
    rules = data.get("rules")
    if not isinstance(rules, list) or not rules:
        errors.append("'rules' must be a non-empty list")
        for msg in errors:
            print(f"check-registry: {msg}", file=sys.stderr)
        return 1

    seen_ids = set()
    for i, rule in enumerate(rules):
        rid = rule.get("id", f"<rule {i}>")
        missing = REQUIRED_FIELDS - set(rule.keys())
        if missing:
            errors.append(f"{rid}: missing fields {sorted(missing)}")
        if rule.get("type") not in VALID_TYPES:
            errors.append(f"{rid}: invalid type '{rule.get('type')}'")
        if rule.get("severity") not in VALID_SEVERITIES:
            errors.append(f"{rid}: invalid severity '{rule.get('severity')}'")
        if not rule.get("vehicle"):
            errors.append(f"{rid}: missing 'vehicle' — every rule needs an enforcement vehicle")
        if rid in seen_ids:
            errors.append(f"{rid}: duplicate id")
        seen_ids.add(rid)

    if errors:
        for msg in errors:
            print(f"check-registry: {msg}", file=sys.stderr)
        return 1

    blocks = sum(1 for r in rules if r["severity"] == "block")
    warns = sum(1 for r in rules if r["severity"] == "warn")
    print(f"check-registry: OK — {len(rules)} rules ({blocks} block, {warns} warn)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
