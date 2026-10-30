"""storyboard.md → script.md (chỉ lời thuyết minh, dán thẳng vào AI tạo giọng). Dùng: python core/scripts/export_narration.py <episode_dir>
Trong mỗi phần, các câu nối liền thành đoạn; chỉ xuống dòng ở chỗ storyboard có dòng trống giữa hai nhịp, để AI giọng ngắt lâu hơn. Mỗi phần cách nhau 1 dòng trống.
Chữ đọc lấy từ công cụ ngôn ngữ của kênh (lang.speech trong channel.yaml)."""
import re, sys
from pathlib import Path

ep = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(Path(__file__).resolve().parent))
import channel as chan
cfg = chan.load(ep)
lang, sp = cfg["lang"], chan.speech(cfg)
SEP = "" if lang["tokenize"] == "char" else " "
text = re.sub(r"<!--.*?-->", "", (ep / "storyboard.md").read_text(encoding="utf-8"), flags=re.S)
out, para, cur = [], [], []
units = 0


def flush_line():
    global cur
    if cur:
        para.append(SEP.join(cur)); cur = []


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
    units += sp.count(s)
    s = sp.speak(s)
    if s:
        cur.append(s)
flush_line()
if para:
    out.append("\n".join(para))
(ep / "script.md").write_text("\n\n".join(out) + "\n", encoding="utf-8")
pace = lang["pace"]
print(ep / "script.md", units, pace["unit"], "≈", round(units / pace["per_min"], 1), "phút")
