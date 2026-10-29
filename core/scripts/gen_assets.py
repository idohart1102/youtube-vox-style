"""Tạo và tìm asset cho một tập theo <tập>/asset_plan.json, rồi xuất bảng hình asset_sheet.jpg để duyệt.
Dùng: python core/scripts/gen_assets.py <episode_dir> [--only ai|real] [--redo id1,id2] [--max 60] [--codex]
  kind "ai":   ảnh paleoart qua 9router (cx/gpt-image-2.5). role "bg" = ảnh nền 1920x1080; role "cutout" = PNG nền trong suốt.
  kind "real": ảnh thật, model tìm web qua 9router (--codex: dùng Codex CLI) → chỉ nhận giấy phép mở, ghi nguồn vào assets/credits.json.
  kind "reuse": hình có sẵn trong kho, chỉ kiểm tra tồn tại.
Asset đã có file thì bỏ qua (dùng lại giữa các tập), trừ khi nằm trong --redo."""
import argparse, io, json, re, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import requests
from PIL import Image, ImageDraw, ImageFont
from paths import assets_dir
import router

ap = argparse.ArgumentParser()
ap.add_argument("ep")
ap.add_argument("--only", choices=["ai", "real"])
ap.add_argument("--redo", default="")
ap.add_argument("--max", type=int, default=60)
ap.add_argument("--codex", action="store_true")
a = ap.parse_args()
ep = Path(a.ep).resolve()
A = assets_dir()
plan = json.loads((ep / "asset_plan.json").read_text(encoding="utf-8"))
theme = json.loads((ep.parents[1] / "theme.json").read_text(encoding="utf-8"))
STYLE = theme.get("art_style_prompt", "")
SPECIES = plan.get("species", {})
redo = set(filter(None, a.redo.split(",")))
OPEN = re.compile(r"(cc0|public domain|cc[ -]by(?![^,;]*\b(nc|nd)\b)|pd-)", re.I)  # cấm NC, ND
UA = {"User-Agent": "TienSuDatViet-asset-bot/1.0 (YouTube education channel)"}

todo = [x for x in plan["assets"] if x["kind"] != "reuse" and (x["id"] in redo or not (A / x["file"]).exists())]
todo = [x for x in todo if not a.only or x["kind"] == a.only]
for x in plan["assets"]:
    if x["kind"] == "reuse" and not (A / x["file"]).exists():
        print(f"Thiếu asset dùng lại: {x['file']}")
if sum(x["kind"] == "ai" for x in todo) > a.max:
    sys.exit(f"Cần tạo {sum(x['kind'] == 'ai' for x in todo)} ảnh AI, vượt --max {a.max}. Gộp cảnh dùng chung hình hoặc tăng --max.")


def fit_bg(im):  # cắt về 16:9 rồi đưa về 1920x1080
    w, h = im.size
    if w / h > 16 / 9:
        nw = int(h * 16 / 9); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:
        nh = int(w * 9 / 16); im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    return im.convert("RGB").resize((1920, 1080), Image.LANCZOS)


def clean_cutout(im):  # alpha gần đặc → đặc, cắt sát vật thể
    im = im.convert("RGBA")
    al = im.getchannel("A").point(lambda v: 255 if v > 240 else (0 if v < 10 else v))
    im.putalpha(al)
    box = al.getbbox()
    if box:
        p = 12
        im = im.crop((max(0, box[0] - p), max(0, box[1] - p), min(im.width, box[2] + p), min(im.height, box[3] + p)))
    return im


def gen_ai(x):
    sp = SPECIES.get(x.get("species", ""), "")
    if x.get("role") == "cutout":
        prompt = (f"{x['prompt']}. {sp} {STYLE}. Single subject, entire body visible with margin, "
                  "isolated on a fully transparent background, no ground, no cast shadow, no text, no letters, no watermark.")
        im = clean_cutout(Image.open(io.BytesIO(router.image(prompt, transparent=True))))
        out = A / x["file"]; out.parent.mkdir(parents=True, exist_ok=True); im.save(out.with_suffix(".png"))
    else:
        prompt = (f"{x['prompt']}. {sp} {STYLE}. Wide 16:9 cinematic composition, keep the main subject inside the central area, "
                  "leave calm areas for overlays, no text, no letters, no logos, no watermark.")
        im = fit_bg(Image.open(io.BytesIO(router.image(prompt))))
        out = A / x["file"]; out.parent.mkdir(parents=True, exist_ok=True); im.save(out, quality=90)
    return {"source": "ai", "prompt": x["prompt"]}


def find_real(x):
    q = (f"Find ONE real photograph or scientific figure for this need: {x['query']}. "
         "Search Wikimedia Commons first, then open-access papers (CC BY) or museum sites. Licence MUST be CC0, public domain, CC BY or CC BY-SA "
         "(never NC or ND, never stock photos). Verify the licence on the file page. "
         'Reply ONLY with JSON: {"title":"","file_page_url":"","direct_image_url":"","license":"","author":""}. '
         "direct_image_url must be the original file URL (upload.wikimedia.org/... for Commons).")
    if a.codex:
        with tempfile.TemporaryDirectory() as d:
            subprocess.run(["codex", "--search", "exec", "--skip-git-repo-check", "--ephemeral", "-s", "read-only", "-o", f"{d}/out.txt", q],
                           stdin=subprocess.DEVNULL, capture_output=True, timeout=600, cwd=d)
            r = router.json_in(Path(f"{d}/out.txt").read_text())
    else:
        r = router.json_in(router.ask(q))
    if not OPEN.search(r.get("license", "")):
        raise RuntimeError(f"giấy phép không mở: {r.get('license')}")
    url = r["direct_image_url"]
    m = re.match(r"(https://upload\.wikimedia\.org/wikipedia/commons)/(\w/\w\w)/(.+)$", url)
    if m:  # bản thu nhỏ 2400px cho nhẹ (Commons tự tạo)
        url = f"{m[1]}/thumb/{m[2]}/{m[3]}/2400px-{m[3]}"
    resp = requests.get(url, headers=UA, timeout=120)
    if resp.status_code != 200:
        resp = requests.get(r["direct_image_url"], headers=UA, timeout=180)
    resp.raise_for_status()
    im = Image.open(io.BytesIO(resp.content)).convert("RGB")
    im.thumbnail((2400, 2400))
    out = A / x["file"]; out.parent.mkdir(parents=True, exist_ok=True); im.save(out, quality=92)
    return {"source": "real", "title": r.get("title"), "author": r.get("author"), "license": r["license"], "url": r.get("file_page_url") or r["direct_image_url"],
            "credit": f"Ảnh: {r.get('author') or r.get('title')} · {r['license']}"}


def run(x):
    try:
        meta = gen_ai(x) if x["kind"] == "ai" else find_real(x)
        print(f"  ✓ {x['id']}")
        return x, meta
    except Exception as e:  # ảnh lỗi không làm dừng cả lô
        print(f"  ✗ {x['id']}: {e}")
        return x, None


print(f"{len(todo)} asset cần làm ({sum(x['kind'] == 'ai' for x in todo)} AI, {sum(x['kind'] == 'real' for x in todo)} ảnh thật)")
with ThreadPoolExecutor(3) as pool:
    done = list(pool.map(run, todo))

# Ghi kho: index.json (tag để tập sau dùng lại), credits.json (nguồn ảnh thật)
idx_p, cr_p = A / "index.json", A / "credits.json"
idx = json.loads(idx_p.read_text(encoding="utf-8")) if idx_p.exists() else []
credits = json.loads(cr_p.read_text(encoding="utf-8")) if cr_p.exists() else {}
by_file = {e["file"]: e for e in idx}
for x, meta in done:
    if not meta:
        continue
    f = x["file"] if x.get("role") != "cutout" else str(Path(x["file"]).with_suffix(".png"))
    e = by_file.get(f) or {"file": f, "used_in": []}
    e.update({"tags": x.get("tags", []), "style": theme.get("art_style", "") if meta["source"] == "ai" else "photo", "source": meta["source"], "role": x.get("role", "bg")})
    if ep.name not in e["used_in"]:
        e["used_in"].append(ep.name)
    if f not in by_file:
        idx.append(e); by_file[f] = e
    if meta["source"] == "real":
        credits[f] = {k: meta[k] for k in ("title", "author", "license", "url", "credit")}
idx_p.write_text(json.dumps(idx, ensure_ascii=False, indent=1), encoding="utf-8")
cr_p.write_text(json.dumps(credits, ensure_ascii=False, indent=1), encoding="utf-8")

# Bảng hình thu nhỏ để duyệt (giải phẫu, chữ rác, đúng nội dung)
files = [(x["id"], A / (x["file"] if x.get("role") != "cutout" else str(Path(x["file"]).with_suffix(".png")))) for x in plan["assets"]]
files = [(i, p) for i, p in files if p.exists()]
if files:
    cols, tw, th = 4, 480, 300
    sheet = Image.new("RGB", (cols * tw, -(-len(files) // cols) * (th + 30)), "#16120e")
    dr = ImageDraw.Draw(sheet)
    for n, (i, p) in enumerate(files):
        im = Image.open(p); bgc = Image.new("RGBA", im.size, "#5a6470"); bgc.alpha_composite(im.convert("RGBA"))
        im = bgc.convert("RGB"); im.thumbnail((tw - 10, th - 10))
        x0, y0 = (n % cols) * tw, (n // cols) * (th + 30)
        sheet.paste(im, (x0 + 5, y0 + 5)); dr.text((x0 + 8, y0 + th + 4), i, fill="#f1e7d3", font=ImageFont.load_default(18))
    sheet.save(ep / "asset_sheet.jpg", quality=85)
fails = [x["id"] for x, m in done if not m]
print(f"Xong. Lỗi: {', '.join(fails) or 'không'}. Bảng hình: {ep / 'asset_sheet.jpg'}")
sys.exit(1 if fails else 0)
