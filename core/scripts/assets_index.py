"""Quét assets/ và thêm file mới vào index.json (tag lấy từ thư mục + tên file). Dùng: python core/scripts/assets_index.py"""
import json
from paths import assets_dir

A = assets_dir()
idx_p = A / "index.json"
idx = json.loads(idx_p.read_text(encoding="utf-8")) if idx_p.exists() else []
have = {e["file"] for e in idx}
added = 0
for f in sorted(A.rglob("*")):
    if f.is_file() and f.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".svg", ".mp3", ".wav"}:
        rel = f.relative_to(A).as_posix()
        if rel not in have:
            idx.append({"file": rel, "tags": [f.parent.name] + f.stem.replace("-", "_").split("_"), "period": "", "style": "", "used_in": []})
            added += 1
idx_p.write_text(json.dumps(idx, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"+{added} asset, tổng {len(idx)}")
