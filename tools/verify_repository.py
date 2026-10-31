#!/usr/bin/env python3
"""Offline verification of documentation links, skill metadata and bundled assets."""
from pathlib import Path
import json
import importlib.util
import re
import sys
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

import yaml
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
issues = []
checked_links = 0


def contained(path):
    return path.resolve().is_relative_to(ROOT.resolve())


for md in sorted(ROOT.rglob("*.md")):
    if any(p in {".git", ".venv", "dist"} for p in md.parts):
        continue
    content = md.read_text(encoding="utf-8")
    without_code = re.sub(r"```.*?```", "", content, flags=re.S)
    targets = re.findall(r"!?\[[^\]]*\]\(([^\s)]+)(?:\s+[^)]*)?\)", without_code)
    targets += re.findall(r'<img[^>]+src="([^"]+)"', without_code)
    for target in targets:
        url = urlsplit(target)
        if url.scheme or target.startswith("#"):
            continue
        if not url.path:
            continue
        resolved = md.parent / unquote(url.path)
        checked_links += 1
        if not contained(resolved) or not resolved.exists():
            issues.append(f"Broken local link in {md.relative_to(ROOT)}: {target}")

plugin = ROOT / "plugins/tsbecm-202"
manifest = json.loads((plugin / "plugin.json").read_text())
ui = manifest["extensions"]["com.openai"]["interface"]
if manifest["$schema"] != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
    issues.append("Invalid plugin schema declaration")
if manifest["version"] != (ROOT / "VERSION").read_text().strip():
    issues.append("Plugin and release versions differ")
if len(ui["displayName"]) > 30 or len(ui["shortDescription"]) > 30:
    issues.append("Plugin title or subtitle exceeds 30 characters")
if ui["category"] != "Productivity":
    issues.append("Unexpected plugin category")
for key in ("logo", "composerIcon"):
    icon = plugin / ui[key]
    if not contained(icon) or not icon.is_file():
        issues.append(f"Missing plugin icon: {key}")
    else:
        with Image.open(icon) as img:
            if img.format != "PNG" or img.width != img.height or img.width < 256:
                issues.append(f"Invalid PNG icon: {key}")
        if icon.stat().st_size > 5 * 1024 * 1024:
            issues.append("Icon exceeds 5 MiB")

skill = plugin / "skills/draft-cad-from-images"
front = yaml.safe_load((skill / "SKILL.md").read_text().split("---", 2)[1])
if front.get("name") != skill.name or not front.get("description"):
    issues.append("Skill frontmatter name/description mismatch")
agent = yaml.safe_load((skill / "agents/openai.yaml").read_text())
for key in ("icon_small", "icon_large"):
    if not (skill / agent["interface"][key]).is_file():
        issues.append(f"Missing skill icon: {key}")
if agent.get("policy", {}).get("allow_implicit_invocation") is not True:
    issues.append("Unexpected invocation policy")

market = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text())
for item in market["plugins"]:
    directory = ROOT / item["source"]["path"]
    if not contained(directory) or not (directory / "plugin.json").is_file():
        issues.append("Broken marketplace plugin path")

for svg in (ROOT / "docs/images").glob("*.svg"):
    ET.parse(svg)

for workflow in (ROOT / ".github/workflows").glob("*.yml"):
    data = yaml.safe_load(workflow.read_text())
    if not data.get("jobs"):
        issues.append(f"Workflow has no jobs: {workflow.name}")

spec = importlib.util.spec_from_file_location("chatgpt_kit", ROOT / "tools/build_chatgpt_kit.py")
kit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kit)
if not kit.OUTPUT.is_file() or kit.OUTPUT.read_text(encoding="utf-8") != kit.render():
    issues.append("ChatGPT attachment is missing or stale")
for prompt in ui.get("defaultPrompt", []):
    if not isinstance(prompt, str) or not prompt.strip() or len(prompt) > 128 or "\n" in prompt:
        issues.append("Invalid listing default prompt")
for locale, translated in manifest["extensions"]["com.openai"].get("publication", {}).get("translations", {}).items():
    if len(translated.get("subtitle", "")) > 30 or len(translated.get("description", "")) > 4000:
        issues.append(f"Translation too long: {locale}")

for required in ("README.md", "README.en.md", "README.fr.md", "LICENSE", "prompts/portable-knowledge.txt"):
    if not (ROOT / required).is_file():
        issues.append(f"Missing required distribution file: {required}")

print(json.dumps({"passed": not issues, "local_links_checked": checked_links,
                  "issues": issues}, ensure_ascii=False, indent=2))
sys.exit(1 if issues else 0)
