"""Tạo thư mục tập mới. Dùng: python core/scripts/new_episode.py <slug> <ten-tap>"""
import shutil, sys
from datetime import date
from paths import ROOT, channel_dir

slug, name = sys.argv[1], sys.argv[2]
ep = channel_dir(slug) / "episodes" / f"{date.today().isoformat()}_{name}"
ep.mkdir(parents=True, exist_ok=False)
for sub in ("audio", "render", "thumb"):
    (ep / sub).mkdir()
for t in ("brief.md", "storyboard.md", "meta.md"):
    shutil.copy(ROOT / "core" / "templates" / t, ep / t)
print(ep.relative_to(ROOT))
