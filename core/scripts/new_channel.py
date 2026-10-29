"""Tạo kênh mới từ channels/_template. Dùng: python core/scripts/new_channel.py <slug>"""
import shutil, sys
from paths import ROOT

slug = sys.argv[1]
dst = ROOT / "channels" / slug
if dst.exists():
    raise SystemExit(f"Đã có kênh {slug}")
shutil.copytree(ROOT / "channels" / "_template", dst)
print(f"Đã tạo {dst.relative_to(ROOT)}. Điền channel.yaml, style.md, theme.json, backlog.csv.")
