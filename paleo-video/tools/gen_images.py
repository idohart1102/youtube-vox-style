import json, sys, os, base64, sqlite3, urllib.request, concurrent.futures as cf
STYLE = ("Semi-realistic paleoart concept art, painterly digital illustration, scientifically informed anatomy, "
         "rich natural textures, cinematic lighting, muted earthy palette with dramatic accents, "
         "documentary concept art quality, 16:9 widescreen composition, no text, no watermark. Scene: ")
scenes = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
key = sqlite3.connect(os.path.expanduser("~/.9router/db/data.sqlite")).execute(
    "select key from apiKeys where isActive=1 limit 1").fetchone()[0]
def gen(s):
    path = os.path.join(out, s["id"] + ".png")
    if os.path.exists(path): return s["id"], "skip"
    for attempt in range(3):
        try:
            req = urllib.request.Request("http://localhost:20128/v1/images/generations",
                data=json.dumps({"model": "cx/gpt-image-2.5", "prompt": STYLE + s["prompt"],
                                 "size": "1536x1024", "n": 1}).encode(),
                headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
            d = json.load(urllib.request.urlopen(req, timeout=400))
            open(path, "wb").write(base64.b64decode(d["data"][0]["b64_json"]))
            return s["id"], "ok"
        except Exception as e:
            err = str(e)
    return s["id"], "FAIL " + err
with cf.ThreadPoolExecutor(4) as ex:
    for r in ex.map(gen, scenes): print(*r, flush=True)
