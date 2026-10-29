import json, sys, os, base64, sqlite3, urllib.request, concurrent.futures as cf
STYLE = "Semi-realistic paleoart concept art, painterly digital illustration, scientifically informed, rich natural textures, muted earthy palette, no text, no watermark. "
CUTOUT = ("Isolated single cut-out sticker asset with a thin clean white paper border, entire subject fully inside the frame "
          "with generous margin, nothing cropped, transparent background, soft even lighting. Subject: ")
assets = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
key = sqlite3.connect(os.path.expanduser("~/.9router/db/data.sqlite")).execute(
    "select key from apiKeys where isActive=1 limit 1").fetchone()[0]
def gen(a):
    path = os.path.join(out, a["id"] + ".png")
    if os.path.exists(path): return a["id"], "skip"
    body = {"model": "cx/gpt-image-2.5", "prompt": STYLE + (CUTOUT if a["t"] else "Scene: ") + a["prompt"],
            "size": a["size"], "n": 1, "output_format": "png"}
    if a["t"]: body["background"] = "transparent"
    err = ""
    for attempt in range(3):
        try:
            req = urllib.request.Request("http://localhost:20128/v1/images/generations", data=json.dumps(body).encode(),
                headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
            d = json.load(urllib.request.urlopen(req, timeout=400))
            open(path, "wb").write(base64.b64decode(d["data"][0]["b64_json"]))
            return a["id"], "ok"
        except Exception as e:
            err = str(e)
    return a["id"], "FAIL " + err
with cf.ThreadPoolExecutor(4) as ex:
    for r in ex.map(gen, assets): print(*r, flush=True)
