#!/usr/bin/env python3
"""Check and apply signed-by-origin governance-kit GitHub releases.

This script is installed into governed projects. Checking is read-only and
fails open. Applying downloads a specific GitHub Release source archive and
delegates file-level safety decisions to that release's updater.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.error
import urllib.request
from pathlib import Path


MANIFEST_PATH = Path(".governance-kit/manifest.json")
API_ROOT = "https://api.github.com/repos"


def normalize_version(value: str) -> tuple[int, int, int] | None:
    value = value.strip().lstrip("v")
    parts = value.split(".")
    if len(parts) != 3 or not all(part.isdigit() for part in parts):
        return None
    return tuple(int(part) for part in parts)  # type: ignore[return-value]


def load_manifest(root: Path) -> dict:
    path = root / MANIFEST_PATH
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as error:
        raise RuntimeError(f"cannot read {path}: {error}") from error


def release_url(repository: str, tag: str | None = None) -> str:
    suffix = "latest" if tag is None else f"tags/{tag}"
    return f"{API_ROOT}/{repository}/releases/{suffix}"


def request_release(repository: str, tag: str | None = None) -> dict:
    request = urllib.request.Request(
        release_url(repository, tag),
        headers={"Accept": "application/vnd.github+json", "User-Agent": "governance-kit-update"},
    )
    try:
        with urllib.request.urlopen(request, timeout=4) as response:
            return json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError) as error:
        raise RuntimeError(f"could not check GitHub Releases: {error}") from error


def source_metadata(manifest: dict) -> tuple[str, str] | None:
    source = manifest.get("distribution", {})
    repository = source.get("github_repository")
    installed_version = source.get("installed_version")
    if not isinstance(repository, str) or not isinstance(installed_version, str):
        return None
    return repository, installed_version


def print_release(release: dict, installed_version: str) -> None:
    tag = release.get("tag_name", "unknown")
    notes = (release.get("body") or "No release notes were published.").strip()
    html_url = release.get("html_url", "")
    print(f"governance-kit update available: {installed_version} -> {tag}")
    if html_url:
        print(f"Release: {html_url}")
    print("Release notes:")
    print(notes)
    print(f"Next: python3 scripts/governance-kit-update.py apply --version {tag}")


def cmd_check(root: Path) -> int:
    try:
        metadata = source_metadata(load_manifest(root))
    except RuntimeError as error:
        print(f"governance-kit update check unavailable: {error}")
        return 0
    if metadata is None:
        print("governance-kit update check not configured: set an official GitHub repository first.")
        return 0

    repository, installed_version = metadata
    try:
        release = request_release(repository)
    except RuntimeError as error:
        print(f"governance-kit update check unavailable: {error}")
        return 0

    latest = release.get("tag_name")
    if not isinstance(latest, str):
        print("governance-kit update check unavailable: latest release has no tag.")
        return 0
    current_value = normalize_version(installed_version)
    latest_value = normalize_version(latest)
    if current_value is None or latest_value is None:
        print("governance-kit update check unavailable: release tags must use vMAJOR.MINOR.PATCH.")
        return 0
    if latest_value <= current_value:
        return 0
    print_release(release, installed_version)
    return 0


def safe_extract(archive: Path, destination: Path) -> None:
    with tarfile.open(archive, "r:gz") as tar:
        destination_root = destination.resolve()
        for member in tar.getmembers():
            member_path = (destination / member.name).resolve()
            if (
                not member_path.is_relative_to(destination_root)
                or member.issym()
                or member.islnk()
                or member.isdev()
            ):
                raise RuntimeError("release archive contains an unsafe path")
        for member in tar.getmembers():
            tar.extract(member, destination)


def find_release_root(destination: Path) -> Path:
    candidates = [path for path in destination.iterdir() if path.is_dir()]
    if len(candidates) != 1:
        raise RuntimeError("release archive must contain exactly one source directory")
    return candidates[0]


def cmd_apply(root: Path, tag: str) -> int:
    try:
        metadata = source_metadata(load_manifest(root))
    except RuntimeError as error:
        print(f"governance-kit update unavailable: {error}", file=sys.stderr)
        return 2
    if metadata is None:
        print("governance-kit update is not configured for this project.", file=sys.stderr)
        return 2

    repository, installed_version = metadata
    try:
        release = request_release(repository, tag)
        archive_url = release["tarball_url"]
    except (RuntimeError, KeyError) as error:
        print(f"governance-kit update unavailable: {error}", file=sys.stderr)
        return 2
    if release.get("tag_name") != tag:
        print("governance-kit update refused: release tag did not match the requested version.", file=sys.stderr)
        return 2
    requested_version = normalize_version(tag)
    current_version = normalize_version(installed_version)
    if requested_version is None:
        print("governance-kit update refused: release tag must use vMAJOR.MINOR.PATCH.", file=sys.stderr)
        return 2
    if current_version is None:
        print("governance-kit update refused: installed version must use MAJOR.MINOR.PATCH.", file=sys.stderr)
        return 2
    if requested_version <= current_version:
        print("governance-kit update refused: requested release is not newer than the installed version.", file=sys.stderr)
        return 2

    with tempfile.TemporaryDirectory(prefix="governance-kit-") as temp_dir:
        temp_path = Path(temp_dir)
        archive_path = temp_path / "release.tar.gz"
        try:
            urllib.request.urlretrieve(archive_url, archive_path)
            source_root = temp_path / "source"
            source_root.mkdir()
            safe_extract(archive_path, source_root)
            kit_root = find_release_root(source_root)
            release_version = (kit_root / "VERSION").read_text().strip()
        except (OSError, RuntimeError, tarfile.TarError, urllib.error.URLError) as error:
            print(f"governance-kit update unavailable: {error}", file=sys.stderr)
            return 2

        if normalize_version(release_version) != normalize_version(tag):
            print("governance-kit update refused: archive VERSION does not match release tag.", file=sys.stderr)
            return 2

        print(f"governance-kit update review: {installed_version} -> {tag}")
        preview = subprocess.run(
            [sys.executable, str(kit_root / "scripts/update.py"), "preview", str(kit_root), str(root)],
            text=True,
            check=False,
        )
        if preview.returncode != 0:
            return preview.returncode
        answer = input("Apply only the safe changes above? [y/N] ").strip().lower()
        if answer not in {"y", "yes"}:
            print("governance-kit update cancelled; no project files changed.")
            return 0
        return subprocess.run(
            [sys.executable, str(kit_root / "scripts/update.py"), "update", str(kit_root), str(root)],
            check=False,
        ).returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="Check or apply governance-kit GitHub Releases.")
    parser.add_argument("command", choices=("check", "apply"))
    parser.add_argument("--root", default=".", help="project root (default: current directory)")
    parser.add_argument("--version", help="release tag required for apply, for example v0.1.1")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if args.command == "check":
        return cmd_check(root)
    if not args.version:
        parser.error("apply requires --version vMAJOR.MINOR.PATCH")
    return cmd_apply(root, args.version)


if __name__ == "__main__":
    raise SystemExit(main())
