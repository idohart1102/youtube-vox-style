"""Kiểm tra scenes.json theo schema và kiểm tra asset có tồn tại. Không tốn token."""
import json, sys
from pathlib import Path
from jsonschema import validate
from paths import ROOT, assets_dir

p = Path(sys.argv[1])
data = json.loads(p.read_text(encoding="utf-8"))
validate(data, json.loads((ROOT / "core/templates/scenes.schema.json").read_text(encoding="utf-8")))
missing = [s["asset"] for s in data["scenes"] if s.get("asset") and not (assets_dir() / s["asset"]).exists()]
total = sum(s["duration_s"] for s in data["scenes"])
print(f"{len(data['scenes'])} cảnh, {total/60:.1f} phút")
if missing:
    print("Thiếu asset:", *missing, sep="\n  ")
    sys.exit(1)
print("OK")
