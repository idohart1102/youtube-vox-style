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
problems = []
tl = p.parent / "timeline.json"
if tl.exists():  # dựng từ audio + srt: tổng thời lượng phải khớp audio, nhịp cảnh theo style
    end = json.loads(tl.read_text(encoding="utf-8"))["audio_end"]
    if abs(total - end) > 1.0:
        problems.append(f"Tổng {total:.1f}s lệch audio {end:.1f}s")
    t = 0.0
    for s in data["scenes"]:
        if s["duration_s"] > 20.5:
            problems.append(f"Cảnh {s['id']} dài {s['duration_s']:.1f}s (> 20s)")
        elif t < 60 and s["duration_s"] > 8.5 and s["component"] != "TitleCard":
            problems.append(f"Cảnh {s['id']} ở phút đầu dài {s['duration_s']:.1f}s (> 8s)")
        t += s["duration_s"]
if problems:
    print("Cần sửa nhịp:", *problems, sep="\n  ")
if missing:
    print("Thiếu asset:", *missing, sep="\n  ")
    sys.exit(1)
if problems:
    sys.exit(1)
print("OK")
