"""Ghép srt của Sếp với storyboard.md để lấy thời gian thật. Không tốn token, mọi ngôn ngữ.
Dùng: python core/scripts/align_srt.py <episode_dir>          → timeline.json + audio/subs.clean.srt
      python core/scripts/align_srt.py <episode_dir> --apply  → điền duration_s, narration, badge, thẻ vào scenes.json
srt chỉ dùng để lấy thời gian. Chữ phụ đề lấy từ storyboard (viết hoa, dấu câu, tên riêng chuẩn)."""
import json, re, sys
from difflib import SequenceMatcher
from pathlib import Path

ep = Path(sys.argv[1]).resolve()
MAX_CHARS = 42      # phụ đề 1 dòng
MIN_MATCH = 0.90    # dưới mức này thì dừng và báo câu lệch
LATIN = r"[A-Za-z]+(?: [A-Za-z]+)? \(([^()]*-[^()]*)\)"  # "Chicxulub (chích-xu-lúp)"
BADGES = {"đã xác nhận": "xac-nhan", "có thể": "co-the", "còn tranh cãi": "tranh-cai"}
# Đơn vị viết thành chữ cho giọng đọc, nhưng trên màn hình (phụ đề, thẻ) viết ký hiệu: "10 ki-lô-mét" → "10 km"
QA = re.compile(r"(HỎI|ĐÁP)\s*:\s*(\w+)$", re.I)  # đánh dấu câu hỏi và câu trả lời: [HỎI: q1] ... [ĐÁP: q1]
UNITS = [(r"ki-lô-mét vuông", "km²"), (r"ki-lô-mét", "km"), (r"ki-lô-gam", "kg"), (r"phần trăm", "%"), (r"độ C", "°C"), (r"mét", "m")]


def screen(text):
    for word, sym in UNITS:
        text = re.sub(rf"(\d[\d.,]*) {word}\b", (rf"\1{sym}" if sym in ("%", "°C") else rf"\1 {sym}"), text)
    return text


def ts(s):
    h, m, rest = s.replace(",", ".").split(":")
    return int(h) * 3600 + int(m) * 60 + float(rest)


def fmt(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"


def words(text):
    text = re.sub(r"(?<=\d)[.,](?=\d)", "", text.lower()).replace("-", " ")
    return re.findall(r"\w+", text)


def read_srt():
    srts = sorted((ep / "audio").glob("*.srt"))
    srts = [p for p in srts if not p.name.endswith(".clean.srt")]
    if not srts:
        sys.exit("Không thấy file .srt trong audio/")
    cues = []
    for block in re.split(r"\n\s*\n", srts[0].read_text(encoding="utf-8-sig").strip()):
        lines = block.strip().splitlines()
        i = next((k for k, l in enumerate(lines) if "-->" in l), None)
        if i is None:
            continue
        a, b = [ts(x.strip().split()[0]) for x in lines[i].split("-->")]
        cues.append((a, b, " ".join(lines[i + 1:])))
    return cues


def read_storyboard():
    """Mỗi câu lời đọc: chương, chữ hiển thị, chữ đọc, ghi chú [ ] đứng trước hoặc cùng dòng."""
    out, chapter, pending, pending_qa = [], "", [], []
    for raw in (ep / "storyboard.md").read_text(encoding="utf-8").splitlines():
        if raw.startswith("## "):
            chapter = raw[3:].strip()
            continue
        if raw.startswith("#"):
            continue
        notes = re.findall(r"\[([^\]]*)\]", raw)
        pending += notes
        # [HỎI: q1] / [ĐÁP: q1] gắn đúng câu đứng ngay sau thẻ (thẻ cuối dòng thì gắn câu ngay trước)
        marked = re.sub(r"\[([^\]]*)\]", lambda m: f"\x00{m[1].strip()}\x00" if QA.match(m[1].strip()) else "", raw)
        k = 0
        for seg in re.split(r"(?<=[.?!…])\s+", marked.strip()):
            qa = [QA.match(n) for n in re.findall(r"\x00([^\x00]*)\x00", seg)]
            qa = [f"{m[1].upper()}:{m[2]}" for m in qa]
            sent = re.sub(r"\s{2,}", " ", re.sub(r"\x00[^\x00]*\x00", "", seg)).strip()
            if not sent:
                if k:
                    out[-1].setdefault("qa", []).extend(qa)
                else:
                    pending_qa += qa
                continue
            out.append({"chapter": chapter, "text": screen(re.sub(r" \(([^()]*-[^()]*)\)", "", sent)),
                        "speak": re.sub(LATIN, r"\1", sent), "notes": pending if k == 0 else []})
            if pending_qa + qa:
                out[-1]["qa"] = pending_qa + qa
            if sent.endswith("?"):
                out[-1]["ask"] = True
            pending_qa, k = [], k + 1
        if k:
            pending = []
    return out


cues, sents = read_srt(), read_storyboard()
# Thời gian từng từ trong srt: chia đều theo độ dài chữ trong mỗi cue
sw, st = [], []
for a, b, text in cues:
    ws = words(text)
    tot = sum(len(w) for w in ws) or 1
    acc = 0
    for w in ws:
        st.append((a + (b - a) * acc / tot, a + (b - a) * (acc + len(w)) / tot))
        sw.append(w)
        acc += len(w)
bw, owner = [], []
for i, s in enumerate(sents):
    for w in words(s["speak"]):
        bw.append(w)
        owner.append(i)
sm = SequenceMatcher(None, bw, sw, autojunk=False)
t0, t1 = [None] * len(bw), [None] * len(bw)
for blk in sm.get_matching_blocks():
    for k in range(blk.size):
        t0[blk.a + k], t1[blk.a + k] = st[blk.b + k]
matched = sum(x is not None for x in t0)
ratio = matched / max(1, len(bw))
# Từ không khớp: nội suy giữa hai từ khớp gần nhất
known = [k for k, x in enumerate(t0) if x is not None]
for k in range(len(bw)):
    if t0[k] is None:
        prev = max((j for j in known if j < k), default=None)
        nxt = min((j for j in known if j > k), default=None)
        a = t1[prev] if prev is not None else 0.0
        b = t0[nxt] if nxt is not None else cues[-1][1]
        n0 = prev if prev is not None else -1
        n1 = nxt if nxt is not None else len(bw)
        frac = (k - n0) / (n1 - n0)
        t0[k] = t1[k] = a + (b - a) * frac
bad = []
for i, s in enumerate(sents):
    idx = [k for k, o in enumerate(owner) if o == i]
    s["start"], s["end"] = (round(t0[idx[0]], 3), round(t1[idx[-1]], 3)) if idx else (0.0, 0.0)
    hit = sum(1 for k in idx if k in set(known))
    if idx and hit / len(idx) < 0.6:
        bad.append(f"  câu {i}: {s['text'][:70]}")

# Phụ đề 1 dòng: cắt câu thành đoạn ≤ MAX_CHARS, ưu tiên sau dấu phẩy, thời gian chia theo số ký tự
subs = []
for s in sents:
    chunks, cur = [], ""
    for w in s["text"].split():
        if cur and len(cur) + 1 + len(w) > MAX_CHARS:
            cut = cur.rfind(", ")
            if cut > MAX_CHARS * 0.4:
                chunks.append(cur[:cut + 1]); cur = cur[cut + 2:]
            else:
                chunks.append(cur); cur = ""
        cur = f"{cur} {w}".strip()
    if cur:
        chunks.append(cur)
    tot, acc = sum(len(c) for c in chunks), 0
    for c in chunks:
        a = s["start"] + (s["end"] - s["start"]) * acc / tot
        acc += len(c)
        subs.append({"start": round(a, 3), "end": round(s["start"] + (s["end"] - s["start"]) * acc / tot, 3), "text": c})
chapters, seen = [], set()
for s in sents:
    if s["chapter"] and s["chapter"] not in seen:
        seen.add(s["chapter"]); chapters.append({"title": s["chapter"], "start": s["start"]})

if "--apply" not in sys.argv:
    doc = {"audio_end": cues[-1][1], "match": round(ratio, 3), "chapters": chapters,
           "lines": [{"i": i, **{k: s[k] for k in ("chapter", "start", "end", "text", "notes", "qa", "ask") if k in s}} for i, s in enumerate(sents)],
           "subs": subs}
    (ep / "timeline.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    (ep / "audio" / "subs.clean.srt").write_text(
        "\n".join(f"{n}\n{fmt(c['start'])} --> {fmt(c['end'])}\n{c['text']}\n" for n, c in enumerate(subs, 1)), encoding="utf-8")
    print(f"{len(sents)} câu, khớp {ratio:.0%}, audio {cues[-1][1] / 60:.1f} phút → timeline.json, audio/subs.clean.srt")
    if ratio < MIN_MATCH or bad:
        print("Câu lệch nhiều (kiểm lại storyboard và srt):", *bad[:20], sep="\n")
        sys.exit(2 if ratio < MIN_MATCH else 0)
    sys.exit(0)

# --apply: scenes.json có "lines": [đầu, cuối] (chỉ số câu trong timeline.json), tuỳ chọn "fixed_s" cho TitleCard
doc = json.loads((ep / "scenes.json").read_text(encoding="utf-8"))
sc, end = doc["scenes"], cues[-1][1] + 0.6
starts = []
for i, s in enumerate(sc):
    a = 0.0 if i == 0 else sents[s["lines"][0]]["start"]
    if i and sc[i - 1].get("fixed_s"):
        a = max(a, starts[-1] + sc[i - 1]["fixed_s"])
    starts.append(a)
for i, s in enumerate(sc):
    s["duration_s"] = round((starts[i + 1] if i + 1 < len(sc) else end) - starts[i], 3)
    lo, hi = s["lines"]
    s["narration"] = " ".join(x["text"] for x in sents[lo:hi + 1])
    props = s.setdefault("props", {})
    if s.get("fixed_s"):  # thẻ chương: không gắn badge hay thẻ keyword
        continue
    for x in sents[lo:hi + 1]:
        at = round(max(0.0, x["start"] - starts[i]), 2)
        for n in x["notes"]:
            key = BADGES.get(n.strip().lower())
            if key and not any(b["type"] == key for b in props.get("badges", [])):
                props.setdefault("badges", []).append({"type": key, "at_s": at})
            if n.upper().startswith("THẺ:") and "cards" not in props:
                card = screen(n.split(":", 1)[1].split(",")[0].strip())  # thẻ chỉ giữ keyword/số liệu
                if len(card.split()) <= 6:
                    props["cards"] = [{"text": card, "at_s": at}]
                else:
                    print(f"Bỏ thẻ quá dài ở cảnh {s['id']}: {card}")
# Ảnh thật: tự điền dòng nguồn từ assets/credits.json (gen_assets.py ghi khi tải ảnh)
sys.path.insert(0, str(Path(__file__).parent))
from paths import assets_dir
cr_p = assets_dir() / "credits.json"
credits = json.loads(cr_p.read_text(encoding="utf-8")) if cr_p.exists() else {}
for s in sc:
    pr = s.setdefault("props", {})
    if s["component"] == "PhotoCard" and not pr.get("credit") and s.get("asset") in credits:
        pr["credit"] = credits[s["asset"]]["credit"]
    for it in pr.get("items", []):
        if it.get("photo") and not it.get("credit") and it.get("asset") in credits:
            it["credit"] = credits[it["asset"]]["credit"]
# Asset đáp án (answer_of trong asset_plan.json) đang ẩn: tự điền unmask_s = lúc đọc câu [ĐÁP] nằm trong cảnh
plan_p = ep / "asset_plan.json"
answer_of = {}
if plan_p.exists():
    for x in json.loads(plan_p.read_text(encoding="utf-8")).get("assets", []):
        if x.get("answer_of"):
            answer_of[x["file"]] = answer_of[str(Path(x["file"]).with_suffix(".png"))] = x["answer_of"]
for i, s in enumerate(sc):
    lo, hi = s["lines"]
    ans = {q.split(":", 1)[1]: round(max(0.0, x["start"] - starts[i]), 2)
           for x in sents[lo:hi + 1] for q in x.get("qa", []) if q.startswith("ĐÁP:")}
    pr = s["props"]
    hidden = [(x, x.get("asset") or x.get("cutout")) for x in pr.get("layers", []) + pr.get("items", []) if x.get("hide")]
    if isinstance(pr.get("hide"), dict):
        hidden.append((pr["hide"], s.get("asset")))
    for x, f in hidden:
        q = x.get("answer_of") or answer_of.get(f)
        if q in ans and "unmask_s" not in x:
            x["unmask_s"] = ans[q]
(ep / "scenes.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"{len(sc)} cảnh, {sum(s['duration_s'] for s in sc) / 60:.1f} phút, khớp audio {end / 60:.1f} phút")
