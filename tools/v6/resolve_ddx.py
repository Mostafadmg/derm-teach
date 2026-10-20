#!/usr/bin/env python3
"""Resolve ddx_specs.SPECS into content/ddx-photos.json (name -> photo code), downloading dn:/cm: sources into the v6 set."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import dn, ddx_specs
ROOT = Path(__file__).resolve().parents[2]
prev = json.loads((ROOT / "content/ddx-photos.json").read_text()) if (ROOT / "content/ddx-photos.json").exists() else {}
out = {}
for name, spec in ddx_specs.SPECS.items():
    if spec.startswith("dn:"):
        _, t, i = spec.split(":"); code = "v6:" + dn.get(t, i, "ddx", "")
    elif spec.startswith("cm:"):
        code = "v6:" + dn.commons(spec[3:], "ddx", "")
    else:
        code = spec
    out[name] = code
out["_text"] = prev.get("_text", [])
(ROOT / "content/ddx-photos.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
print(len(out))
