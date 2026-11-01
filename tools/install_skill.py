#!/usr/bin/env python3
"""Install the bundled skill without downloads, shell commands or global packages."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
from pathlib import Path
import shutil
import tempfile

ROOT = Path(__file__).resolve().parents[1]
NAME = "draft-cad-from-images"
SOURCE = ROOT / "plugins/tsbecm-202/skills" / NAME


def inventory(path):
    result = {}
    for item in sorted(path.rglob("*")):
        if "__pycache__" in item.parts or item.suffix == ".pyc":
            continue
        if item.is_symlink():
            raise ValueError(f"Refusing symbolic link: {item}")
        if item.is_file():
            result[item.relative_to(path).as_posix()] = hashlib.sha256(item.read_bytes()).hexdigest()
    return result


def install(destination, *, replace=False, dry_run=False, source=SOURCE):
    source = Path(source)
    if not (source / "SKILL.md").is_file():
        raise ValueError("The complete repository is required; SKILL.md was not found")
    expected = inventory(source)
    destination = Path(destination).expanduser().absolute()
    target = destination / NAME
    if target.is_symlink():
        raise ValueError(f"Existing target is a symbolic link; inspect it manually: {target}")
    if target.exists():
        if not target.is_dir():
            raise ValueError(f"Target exists and is not a directory: {target}")
        if inventory(target) == expected:
            return {"status": "already installed", "path": str(target)}
        if not replace:
            raise FileExistsError(f"Existing installation differs: {target}. Use --replace to keep a backup and update.")
    if dry_run:
        return {"status": "dry run", "path": str(target), "files": len(expected)}
    destination.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".photo-cad-stage-", dir=destination))
    backup = None
    try:
        shutil.copytree(source, staging, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        if inventory(staging) != expected:
            raise OSError("Copied files did not match the source")
        if target.exists():
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
            backup = destination.parent / "photo-to-autocad-backups" / f"{NAME}-{stamp}"
            backup.parent.mkdir(parents=True, exist_ok=True)
            target.rename(backup)
        staging.rename(target)
    except Exception:
        if backup and backup.exists() and not target.exists():
            backup.rename(target)
        raise
    finally:
        if staging.exists():
            shutil.rmtree(staging)
    result = {"status": "installed", "path": str(target)}
    if backup:
        result["backup"] = str(backup)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=["codex", "gemini"], default="codex")
    parser.add_argument("--scope", choices=["user", "project"], default="user")
    parser.add_argument("--destination", type=Path, help="Explicit parent directory for the skill")
    parser.add_argument("--replace", action="store_true", help="Back up an existing different copy before updating")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    base = Path.home() if args.scope == "user" else Path.cwd()
    directory = ".agents" if args.target == "codex" else ".gemini"
    destination = args.destination or base / directory / "skills"
    try:
        result = install(destination, replace=args.replace, dry_run=args.dry_run)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Installation stopped: {exc}\n")
    for key, value in result.items():
        print(f"{key}: {value}")
    print("Open a new agent session. Python CAD dependencies are installed separately in your project environment.")


if __name__ == "__main__":
    main()
