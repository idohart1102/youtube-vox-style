"""storyboard.md → script.md (chỉ lời thuyết minh, dán thẳng vào AI tạo giọng). Dùng: python core/scripts/export_narration.py <episode_dir>"""
import re, sys
from pathlib import Path

ep = Path(sys.argv[1]).resolve()
text = re.sub(r"<!--.*?-->", "", (ep / "storyboard.md").read_text(encoding="utf-8"), flags=re.S)
out, para = [], []
for line in text.splitlines():
    if line.startswith("## ") and para:  # mỗi chặng một đoạn, cách nhau 1 dòng trống
        out.append("\n".join(para)); para = []
    if line.startswith("#"):
        continue
    s = re.sub(r"\s{2,}", " ", re.sub(r"\[[^\]]*\]", "", line)).strip()
    # Tên Latin kèm cách đọc, vd "Chicxulub (chích-xu-lúp)": giữ cách đọc để AI giọng không đọc hai lần
    s = re.sub(r"[A-Za-z]+(?: [A-Za-z]+)? \(([^()]*-[^()]*)\)", r"\1", s)
    if s:
        para.append(s)
if para:
    out.append("\n".join(para))
(ep / "script.md").write_text("\n\n".join(out) + "\n", encoding="utf-8")
print(ep / "script.md", sum(len(p.split()) for p in out), "từ/âm tiết")
