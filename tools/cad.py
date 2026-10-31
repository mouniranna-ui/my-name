#!/usr/bin/env python3
"""Short entry point for doctor, example, audit and render commands."""
from pathlib import Path
import sys

SCRIPTS = Path(__file__).resolve().parents[1] / "plugins/photo-to-autocad/skills/draft-cad-from-images/scripts"
sys.path.insert(0, str(SCRIPTS))
from cad_tools import main

if __name__ == "__main__":
    raise SystemExit(main())
