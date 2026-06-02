#!/usr/bin/env python3
"""One-time conversion of mapfiles/*.json → botwsave/data/*.yaml"""

import json
import sys
from pathlib import Path

try:
    from ruamel.yaml import YAML
except ImportError:
    sys.exit("pip install ruamel.yaml")

REPO_ROOT = Path(__file__).parent.parent
SRC_DIR = REPO_ROOT / "mapfiles"
DST_DIR = REPO_ROOT / "botwsave" / "data"

DST_DIR.mkdir(parents=True, exist_ok=True)

yaml = YAML()
yaml.default_flow_style = False
yaml.width = 4096

for json_file in sorted(SRC_DIR.glob("*.json")):
    data = json.loads(json_file.read_text())
    out_path = DST_DIR / json_file.with_suffix(".yaml").name
    with out_path.open("w") as f:
        yaml.dump(data, f)
    print(f"{json_file.name} → {out_path.relative_to(REPO_ROOT)}")

print(f"\nDone. {len(list(DST_DIR.glob('*.yaml')))} YAML files written to {DST_DIR.relative_to(REPO_ROOT)}/")
