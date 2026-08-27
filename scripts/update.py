#!/usr/bin/env python3
"""update.py — governance-kit manifest and updater (stdlib only).

The installation manifest lives at <project>/.governance-kit/manifest.json and
records, for every kit-managed file: its kit source and the hash at install
time. This makes updates safe:

  - project file unchanged since install → safe to update from the kit
  - project file customized                → skip + report (never overwrite)
  - new kit file                           → install if target is absent
  - unknown file (not in manifest)         → skip + report (manual review)

Commands:
  update.py manifest <kit_root> <target> [--github-repo OWNER/REPO]
  update.py configure <kit_root> <target> OWNER/REPO
  update.py preview <kit_root> <target>
  update.py update <kit_root> <target>

Exit codes: 0 ok, 1 findings/conflicts, 2 cannot run.
"""

import hashlib
import json
import shutil
import sys
from pathlib import Path

MANIFEST_DIR = ".governance-kit"
MANIFEST_NAME = "manifest.json"

# Project-owned documents are authoritative inside the target and never updated.
ALWAYS_PROTECTED = {
    "PROJECT_STATE.md",
    "README_REENTRY.md",
    "Sprint_Log.md",
    "docs/process/CURRENT_STAGE.md",
    "docs/process/PROJECT_MAP.md",
    "docs/process/DEVELOPMENT_WORKFLOW.md",
}

BASE_PAIRS = [
    ("core/AGENTS.md", "AGENTS.md"),
    ("core/README.md", "README.md"),
    ("core/PROJECT_STATE.md", "PROJECT_STATE.md"),
    ("core/README_REENTRY.md", "README_REENTRY.md"),
    ("core/Sprint_Log.md", "Sprint_Log.md"),
    ("adapters/opencode/agent/reviewer.md", ".opencode/agent/reviewer.md"),
]

SKILL_DEST_ROOTS = (".opencode/skills", ".agents/skills")


def collect_pairs(kit_root: Path) -> list[tuple[str, str]]:
    pairs = list(BASE_PAIRS)
    docs_root = kit_root / "core/docs"
    for doc in sorted(docs_root.rglob("*")):
        if doc.is_file():
            relative_path = doc.relative_to(docs_root)
            pairs.append(
                (f"core/docs/{relative_path}", f"docs/{relative_path}")
            )
    for tpl in sorted((kit_root / "core/templates").iterdir()):
        if tpl.is_file():
            pairs.append((f"core/templates/{tpl.name}", f"docs/templates/{tpl.name}"))
    for script in sorted((kit_root / "scripts").iterdir()):
        if script.name in {"update.py", "check-skills-lock.py"}:
            continue  # kit-internal maintenance tools, not project scripts
        if script.suffix in {".sh", ".py"}:
            pairs.append((f"scripts/{script.name}", f"scripts/{script.name}"))
    for skill_dir in sorted((kit_root / "skills").iterdir()):
        for p in sorted(skill_dir.rglob("*")):
            if p.is_file():
                rel = p.relative_to(skill_dir)
                for dest_root in SKILL_DEST_ROOTS:
                    pairs.append(
                        (
                            f"skills/{skill_dir.name}/{rel}",
                            f"{dest_root}/{skill_dir.name}/{rel}",
                        )
                    )
    return pairs


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def kit_version(kit_root: Path) -> str | None:
    version_path = kit_root / "VERSION"
    if not version_path.is_file():
        return None
    value = version_path.read_text().strip()
    return value or None


def load_manifest(target: Path) -> dict:
    mpath = target / MANIFEST_DIR / MANIFEST_NAME
    if not mpath.exists():
        return {"version": 3, "files": {}}
    try:
        return json.loads(mpath.read_text())
    except json.JSONDecodeError:
        print(f"update: invalid manifest at {mpath} — refusing to update", file=sys.stderr)
        sys.exit(2)


def save_manifest(target: Path, manifest: dict) -> None:
    mdir = target / MANIFEST_DIR
    mdir.mkdir(exist_ok=True)
    (mdir / MANIFEST_NAME).write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")


def configure_distribution(manifest: dict, kit_root: Path, repository: str | None) -> None:
    distribution = manifest.get("distribution", {})
    if repository:
        distribution["github_repository"] = repository
    version = kit_version(kit_root)
    if version:
        distribution["installed_version"] = version
    if distribution:
        manifest["distribution"] = distribution


def cmd_manifest(kit_root: Path, target: Path, repository: str | None = None) -> int:
    previous = load_manifest(target)
    manifest = {"version": 3, "files": {}}
    if "distribution" in previous:
        manifest["distribution"] = previous["distribution"]
    configure_distribution(manifest, kit_root, repository)
    for src, dest in collect_pairs(kit_root):
        dest_path = target / dest
        if dest_path.is_file():
            manifest["files"][dest] = {"src": src, "hash": sha256(dest_path)}
    save_manifest(target, manifest)
    print(f"update: manifest recorded {len(manifest['files'])} files → {target / MANIFEST_DIR / MANIFEST_NAME}")
    return 0


def cmd_configure(kit_root: Path, target: Path, repository: str) -> int:
    if "/" not in repository or repository.startswith("/") or repository.endswith("/"):
        print("update: GitHub repository must be OWNER/REPO", file=sys.stderr)
        return 2
    manifest = load_manifest(target)
    distribution = manifest.setdefault("distribution", {})
    distribution["github_repository"] = repository
    # Legacy manifests have no release identity. Treat them as pre-release so
    # the first published release is offered instead of being silently skipped.
    distribution.setdefault("installed_version", "0.0.0")
    checker_source = kit_root / "scripts/governance-kit-update.py"
    checker_destination = target / "scripts/governance-kit-update.py"
    if checker_source.is_file() and not checker_destination.exists():
        checker_destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(checker_source, checker_destination)
        manifest.setdefault("files", {})["scripts/governance-kit-update.py"] = {
            "src": "scripts/governance-kit-update.py",
            "hash": sha256(checker_destination),
        }
    save_manifest(target, manifest)
    print(f"update: configured GitHub Releases source {repository}")
    return 0


def classify_update(kit_root: Path, target: Path) -> dict[str, list[str]]:
    manifest = load_manifest(target)
    entries = manifest.get("files", {})
    result = {"safe": [], "customized": [], "new": [], "unknown": [], "protected": [], "conflicts": []}
    for src, dest in collect_pairs(kit_root):
        kit_path = kit_root / src
        dest_path = target / dest
        if dest in ALWAYS_PROTECTED:
            result["protected"].append(dest)
        elif not dest_path.exists():
            result["new"].append(dest)
        elif dest not in entries:
            result["unknown"].append(dest)
        elif sha256(dest_path) != entries[dest].get("hash"):
            result["customized"].append(dest)
        elif not kit_path.is_file():
            result["conflicts"].append(f"{dest}: removed from kit")
        elif sha256(kit_path) != sha256(dest_path):
            result["safe"].append(dest)
    return result


def report(title: str, items: list[str]) -> None:
    if items:
        print(f"update: {title}: {len(items)}")
        for item in items[:50]:
            print(f"  - {item}")


def cmd_preview(kit_root: Path, target: Path) -> int:
    result = classify_update(kit_root, target)
    report("safe to update", result["safe"] + result["new"])
    report("customized — review required", result["customized"])
    report("project-owned state — kept", result["protected"])
    report("unknown origin — skipped", result["unknown"])
    report("conflicts — manual review", result["conflicts"])
    return 0 if not result["conflicts"] else 1


def cmd_update(kit_root: Path, target: Path) -> int:
    manifest = load_manifest(target)
    entries = manifest.get("files", {})
    pairs = collect_pairs(kit_root)

    updated, customized, installed, skipped, conflicts, protected = [], [], [], [], [], []

    for src, dest in pairs:
        kit_path = kit_root / src
        dest_path = target / dest

        if dest in ALWAYS_PROTECTED:
            if dest_path.exists():
                protected.append(dest)
            elif kit_path.is_file() and dest not in entries:
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(kit_path, dest_path)
                installed.append(dest)
                entries[dest] = {"src": src, "hash": sha256(dest_path)}
            continue

        if not dest_path.exists():
            if kit_path.is_file():
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(kit_path, dest_path)
                installed.append(dest)
                entries[dest] = {"src": src, "hash": sha256(dest_path)}
            continue

        if dest not in entries:
            skipped.append(dest)
            continue

        installed_hash = entries[dest].get("hash")
        current_hash = sha256(dest_path)

        if current_hash == installed_hash:
            kit_hash = sha256(kit_path) if kit_path.is_file() else None
            if kit_hash is None:
                conflicts.append(f"{dest}: removed from kit — left in place (manual review)")
            elif kit_hash != current_hash:
                shutil.copy2(kit_path, dest_path)
                entries[dest]["hash"] = sha256(dest_path)
                updated.append(dest)
        else:
            customized.append(dest)

    for dest, entry in list(entries.items()):
        if not (target / dest).exists():
            conflicts.append(f"{dest}: in manifest but missing on disk (manual review)")

    manifest["files"] = entries
    manifest["version"] = 3
    configure_distribution(manifest, kit_root, None)
    save_manifest(target, manifest)

    report("updated from kit", updated)
    report("customized — kept (never overwrite)", customized)
    report("installed (new from kit)", installed)
    report("protected project-owned docs — kept (conscious review)", protected)
    report("unknown origin — skipped (manual review)", skipped)
    report("conflicts — manual review", conflicts)

    return 0 if not conflicts else 1


def main() -> int:
    if len(sys.argv) < 3:
        print("usage: update.py manifest|configure|preview|update ...", file=sys.stderr)
        return 2
    cmd = sys.argv[1]
    if cmd == "configure":
        if len(sys.argv) != 5:
            print("usage: update.py configure <kit_root> <target> OWNER/REPO", file=sys.stderr)
            return 2
        return cmd_configure(Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4])
    if len(sys.argv) < 4:
        print("usage: update.py manifest|preview|update <kit_root> <target> [--github-repo OWNER/REPO]", file=sys.stderr)
        return 2
    kit_root, target = Path(sys.argv[2]), Path(sys.argv[3])
    if cmd == "manifest":
        repository = None
        if len(sys.argv) == 6 and sys.argv[4] == "--github-repo":
            repository = sys.argv[5]
        elif len(sys.argv) != 4:
            print("usage: update.py manifest <kit_root> <target> [--github-repo OWNER/REPO]", file=sys.stderr)
            return 2
        return cmd_manifest(kit_root, target, repository)
    if cmd == "preview":
        return cmd_preview(kit_root, target)
    if cmd == "update":
        return cmd_update(kit_root, target)
    print(f"update: unknown command '{cmd}'", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
