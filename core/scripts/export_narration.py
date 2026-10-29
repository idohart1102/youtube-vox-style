"""storyboard.md → script.md (chỉ lời thuyết minh, dán thẳng vào AI tạo giọng). Dùng: python core/scripts/export_narration.py <episode_dir>
Trong mỗi phần, các câu nối liền thành đoạn; chỉ xuống dòng ở chỗ storyboard có dòng trống giữa hai nhịp, để AI giọng ngắt lâu hơn. Mỗi phần cách nhau 1 dòng trống."""
import re, sys
from pathlib import Path

ep = Path(sys.argv[1]).resolve()
text = re.sub(r"<!--.*?-->", "", (ep / "storyboard.md").read_text(encoding="utf-8"), flags=re.S)
out, para, cur = [], [], []


def flush_line():
    global cur
    if cur:
        para.append(" ".join(cur)); cur = []


for line in text.splitlines():
    if line.startswith("## "):  # sang phần mới: đoạn mới, cách 1 dòng trống
        flush_line()
        if para:
            out.append("\n".join(para)); para = []
    if line.startswith("#"):
        continue
    if not line.strip():  # dòng trống giữa hai nhịp = ngắt nghỉ dài
        flush_line()
        continue
    s = re.sub(r"\s{2,}", " ", re.sub(r"\[[^\]]*\]", "", line)).strip()
    # Tên Latin kèm cách đọc, vd "Chicxulub (chích-xu-lúp)": giữ cách đọc để AI giọng không đọc hai lần
    s = re.sub(r"[A-Za-z]+(?: [A-Za-z]+)? \(([^()]*-[^()]*)\)", r"\1", s)
    if s:
        cur.append(s)
flush_line()
if para:
    out.append("\n".join(para))
(ep / "script.md").write_text("\n\n".join(out) + "\n", encoding="utf-8")
print(ep / "script.md", sum(len(p.split()) for p in out), "từ/âm tiết")
