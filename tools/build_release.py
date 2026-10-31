#!/usr/bin/env python3
"""Build portable source, skill and plugin archives; no upload or publication."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/photo-to-autocad"
SKILL = PLUGIN / "skills/draft-cad-from-images"
ROOT_FILES = {"README.md", "README.en.md", "README.fr.md", "LICENSE", "NOTICE.md", "CHANGELOG.md", "VERSION", "requirements.txt", "requirements-dev.txt", ".gitignore", ".gitattributes"}
ROOT_DIRS = {"plugins", "tools", "tests", "docs", "prompts", "examples", ".agents", ".github"}


def files_under(root):
    for p in sorted(root.rglob("*")):
        if "__pycache__" in p.parts or p.suffix == ".pyc":
            continue
        if p.is_symlink():
            raise ValueError(f"Symlink cannot be packaged: {p}")
        if p.is_file():
            yield p


def write_zip(path, files):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        for source, name in files:
            archive.write(source, name)
    with zipfile.ZipFile(path) as archive:
        if archive.testzip():
            raise ValueError(f"Corrupt archive: {path}")
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError("Duplicate archive entries")
        if any(n.startswith("/") or ".." in Path(n).parts for n in names):
            raise ValueError("Unsafe archive path")


def build(output):
    version = (ROOT / "VERSION").read_text().strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValueError("VERSION must contain a release version such as 1.0.0")
    manifest = json.loads((PLUGIN / "plugin.json").read_text())
    if manifest["version"] != version:
        raise ValueError("VERSION and plugin.json disagree")
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    source_files = [(p, "photo-to-autocad/" + p.relative_to(ROOT).as_posix())
                    for p in files_under(ROOT)
                    if p.relative_to(ROOT).parts[0] in ROOT_DIRS or p.relative_to(ROOT).as_posix() in ROOT_FILES]
    targets = {
        f"photo-to-autocad-source-{version}.zip": source_files,
        f"photo-to-autocad-plugin-{version}.zip": [(p, p.relative_to(PLUGIN).as_posix()) for p in files_under(PLUGIN)],
        f"photo-to-autocad-skill-{version}.zip": [(p, "draft-cad-from-images/" + p.relative_to(SKILL).as_posix()) for p in files_under(SKILL)],
    }
    for name, files in targets.items():
        write_zip(output / name, files)
    checksums = []
    for name in targets:
        digest = hashlib.sha256((output / name).read_bytes()).hexdigest()
        checksums.append(f"{digest}  {name}")
    (output / "SHA256SUMS.txt").write_text("\n".join(checksums) + "\n")
    return [str(output / name) for name in [*targets, "SHA256SUMS.txt"]]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    print("\n".join(build(args.output_dir)))
