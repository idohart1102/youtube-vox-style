"""Kiểm tra hệ thống, không cần API key. Dùng: python core/tests/run.py [--smoke] [--keep]
vi: khớp srt cho kết quả giống hệt mốc so sánh. ja: chữ hiển thị và chữ đọc tách đúng, badge theo nhãn kênh, thẻ dài bị loại.
en: tạo kênh mới từ mẫu, không sửa core, dựng 15 giây đầu đến cuối. --smoke chỉ chạy phần dựng, dùng cho doctor.py."""
import json, re, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "core" / "scripts"
FIX = Path(__file__).resolve().parent / "fixtures"
sys.path.insert(0, str(SCRIPTS))
import channel as chan  # noqa: E402

PY = sys.executable
CHANNELS = ROOT / "channels"
fails = []


def run(*args, ok=(0,)):
    r = subprocess.run([str(a) for a in args], capture_output=True, text=True, cwd=ROOT)
    if r.returncode not in ok:
        raise RuntimeError(f"{' '.join(map(str, args))}\n{r.stdout[-1500:]}\n{r.stderr[-1500:]}")
    return r.stdout


def check(name, cond, detail=""):
    print(("  ✓ " if cond else "  ✗ ") + name + (f": {detail}" if detail and not cond else ""))
    if not cond:
        fails.append(name)


def temp_channel(slug, src=None, lang=None):
    d = CHANNELS / slug
    shutil.rmtree(d, ignore_errors=True)
    args = [PY, SCRIPTS / "new_channel.py", slug]
    if src:
        args += ["--from", src]
    if lang:
        args += ["--lang", lang]
    run(*args)
    ep = d / "episodes" / "t"
    (ep / "audio").mkdir(parents=True)
    return d, ep


def srt_time(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"


def fake_srt(sentences, per_sentence=2.2):
    """Tạo srt theo chữ đọc: giả lập file Sếp gửi."""
    out, t = [], 0.3
    for n, s in enumerate(sentences, 1):
        out.append(f"{n}\n{srt_time(t)} --> {srt_time(t + per_sentence)}\n{s}\n")
        t += per_sentence + 0.2
    return "\n".join(out)


def test_vi():
    print("Tiếng Việt: giống hệt mốc so sánh")
    d, ep = temp_channel("_t-vi", "tiensu-vn")
    shutil.copy(FIX / "vi" / "storyboard.md", ep)
    shutil.copy(FIX / "vi" / "voice.srt", ep / "audio")
    run(PY, SCRIPTS / "align_srt.py", ep)
    check("timeline.json không đổi", (ep / "timeline.json").read_bytes() == (FIX / "vi" / "timeline.expected.json").read_bytes())
    check("phụ đề không đổi", (ep / "audio" / "subs.clean.srt").read_bytes() == (FIX / "vi" / "subs.expected.srt").read_bytes())
    run(PY, SCRIPTS / "export_narration.py", ep)
    txt = (ep / "script.md").read_text(encoding="utf-8")
    check("script.md sạch ghi chú", "[" not in txt and "#" not in txt)
    return d


def test_ja():
    print("Tiếng Nhật: chữ đọc, phụ đề, badge, thẻ")
    d, ep = temp_channel("_t-ja", "kodai-jp")
    story = "# テスト\n\n## 第1章\n[THẺ: 8500万年前] 8500万年前、穂別《ほべつ》の海に、地層《ちそう》が生まれました。\n[確定] 体長は7メートルです。\n[THẺ: これはとても長すぎるカードの文章なので表示しません] 証拠は、ここにあります。\n"
    (ep / "storyboard.md").write_text(story, encoding="utf-8")
    cfg = chan.load(d)
    sp = chan.speech(cfg)
    sents = ["8500万年前、穂別《ほべつ》の海に、地層《ちそう》が生まれました。", "体長は7メートルです。", "証拠は、ここにあります。"]
    (ep / "audio" / "voice.srt").write_text(fake_srt([sp.speak(s) for s in sents]), encoding="utf-8")
    run(PY, SCRIPTS / "align_srt.py", ep)
    doc = json.loads((ep / "timeline.json").read_text(encoding="utf-8"))
    check("khớp srt", doc["match"] >= 0.9, str(doc["match"]))
    check("phụ đề hiện kanji, không còn cách đọc", all("《" not in s["text"] for s in doc["subs"]) and "穂別" in "".join(s["text"] for s in doc["subs"]))
    check("phụ đề không quá dài", all(len(s["text"]) <= cfg["lang"]["subtitle"]["max"] + 6 for s in doc["subs"]))
    (ep / "scenes.json").write_text(json.dumps({"fps": 30, "scenes": [{"id": "a", "lines": [0, 2], "component": "KenBurns", "asset": "shared/textures/tang-da.jpg", "props": {}}]}), encoding="utf-8")
    out = run(PY, SCRIPTS / "align_srt.py", ep, "--apply")
    props = json.loads((ep / "scenes.json").read_text(encoding="utf-8"))["scenes"][0]["props"]
    check("badge nhận nhãn tiếng Nhật", any(b["type"] == "xac-nhan" for b in props.get("badges", [])))
    check("thẻ đúng giới hạn ký tự", props.get("cards", [{}])[0].get("text") == "8500万年前")
    run(PY, SCRIPTS / "export_narration.py", ep)
    txt = (ep / "script.md").read_text(encoding="utf-8")
    check("chữ đọc đã đổi sang kana", "ほべつ" in txt and "はっせんごひゃくまんねんまえ" in txt, txt[:80])
    check("nhãn bản đồ theo ngôn ngữ kênh", cfg["lang"]["labels"]["biendong"] == "南シナ海")
    return d


EN = {"xac-nhan": "Confirmed", "co-the": "Likely", "tranh-cai": "Debated", "clock": "EARTH CALENDAR", "hoangsa": "Paracel Islands", "truongsa": "Spratly Islands",
      "biendong": "South China Sea", "ai_notice": "Created with AI assistance", "today": "Today"}


def test_en(seconds=15):
    print(f"Ngôn ngữ mới (tiếng Anh): kênh mới từ mẫu, dựng {seconds} giây, không sửa core")
    d, ep = temp_channel("_t-en", lang="en")
    y = d / "channel.yaml"
    s = y.read_text(encoding="utf-8").replace('locale: ""', "locale: en-US").replace('country: ""', "country: US")
    for k, v in EN.items():
        s = s.replace(f'    {k}: ""', f'    {k}: "{v}"')
    for tpl in ("{n} billion years ago", "{n} million years ago", "{n} years ago"):
        s = s.replace('tpl: ""', f'tpl: "{tpl}"', 1)
    y.write_text(s, encoding="utf-8")
    run(PY, SCRIPTS / "channel.py", d)
    (d / "theme.json").write_text(json.dumps({"palette": {"bg": "#16120e", "fg": "#f1e7d3", "accent": "#c8963e", "danger": "#b8402a"}, "font": "Be Vietnam Pro", "grain": 0.3, "vignette": 0.4, "subtitles": True,
                                              "badges": {"xac-nhan": "#4f7a65", "co-the": "#c8963e", "tranh-cai": "#a5482b"}}), encoding="utf-8")
    sents = ["Sixty six million years ago, nobody heard the blast.", "The ground began to shake within the hour.", "Then the sky started to rain fire.", "Today the rocks still remember it.", "This is how we know."]
    n = max(1, min(len(sents), round(seconds / 3)))
    sents = sents[:n]
    (ep / "storyboard.md").write_text("# Test\n\n## Part one\n[THẺ: 66 million years] " + sents[0] + "\n[Confirmed] " + "\n".join(sents[1:]) + "\n", encoding="utf-8")
    per = seconds / n - 0.2
    (ep / "audio" / "voice.srt").write_text(fake_srt(sents, per), encoding="utf-8")
    run("ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", seconds, ep / "audio" / "voice.mp3")
    (ep / "assets").mkdir()
    shutil.copy(FIX / "assets" / "bg.jpg", ep / "assets")
    shutil.copy(FIX / "assets" / "cutout.png", ep / "assets")
    run(PY, SCRIPTS / "align_srt.py", ep)
    stage = {"cam": "in", "atmosphere": [{"type": "mist", "n": 3, "y": 450}], "layers": [{"asset": "cutout.png", "x": 900, "y": 800, "h": 300, "shadow": {"w": 200}}]}
    scenes = [{"id": "a", "lines": [0, min(1, n - 1)], "component": "Stage", "asset": "bg.jpg", "props": stage}]
    if n > 2:
        scenes.append({"id": "b", "lines": [2, min(3, n - 1)], "component": "GeoMap", "transition": "cut", "props": {"center": [107, 15], "scale": 2300, "strata_in": {"dir": "up", "dur_s": 1.0, "from_asset": "bg.jpg", "counter": {"from_ma": 66}}}})
    if n > 4:
        scenes.append({"id": "c", "lines": [4, n - 1], "component": "Stage", "asset": "bg.jpg", "props": {**stage, "cam": "out"}})
    (ep / "scenes.json").write_text(json.dumps({"fps": 30, "scenes": scenes}), encoding="utf-8")
    run(PY, SCRIPTS / "align_srt.py", ep, "--apply")
    run(PY, SCRIPTS / "validate_scenes.py", ep / "scenes.json")
    run("node", SCRIPTS / "render.mjs", ep)
    check("có video", (ep / "render" / "final.mp4").exists())
    out = run(PY, SCRIPTS / "render_check.py", ep, ok=(0, 1))
    probs = json.loads((ep / "qa" / "render_check.json").read_text(encoding="utf-8"))["problems"]
    probs = [p for p in probs if "Đứng hình" not in p]  # ảnh test tĩnh, không tính
    check("kiểm tra máy không có lỗi", not probs, str(probs))
    return d


if __name__ == "__main__":
    made = []
    try:
        if "--smoke" in sys.argv:
            made.append(test_en(3))
        else:
            made += [test_vi(), test_ja(), test_en(15)]
    except RuntimeError as e:
        fails.append(str(e))
        print(e)
    finally:
        if "--keep" not in sys.argv:
            for s in ("_t-vi", "_t-ja", "_t-en"):
                shutil.rmtree(CHANNELS / s, ignore_errors=True)
    print("ĐẠT" if not fails else f"KHÔNG ĐẠT: {len(fails)} mục")
    sys.exit(1 if fails else 0)
