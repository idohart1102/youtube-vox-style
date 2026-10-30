"""Vai trò chấm độc lập: gửi ảnh cho AI và nhận JSON. Nhà cung cấp lấy từ config/machine.yaml (review_provider: 9router | codex).
Phân công đầy đủ ở config/ai_roles.yaml. Người viết hoặc tạo asset không tự chấm bài của mình."""
import base64, io, subprocess, tempfile
from pathlib import Path
import requests
from PIL import Image
from paths import machine
import router


def _jpeg(path, edge=1024, matte="#5a6470"):
    im = Image.open(path)
    if im.mode in ("RGBA", "LA"):
        bg = Image.new("RGBA", im.size, matte)
        bg.alpha_composite(im.convert("RGBA"))
        im = bg
    im = im.convert("RGB")
    im.thumbnail((edge, edge))
    b = io.BytesIO()
    im.save(b, "JPEG", quality=84)
    return b.getvalue()


def _via_9router(prompt, images):
    content = [{"type": "input_text", "text": prompt}]
    for b in images:
        content.append({"type": "input_image", "image_url": "data:image/jpeg;base64," + base64.b64encode(b).decode()})
    d = router._post("/responses", {"model": router.SEARCH_MODEL, "input": [{"role": "user", "content": content}]}, 300)
    return d.get("output_text") or "".join(c.get("text", "") for o in d.get("output", []) if o.get("type") == "message" for c in o.get("content", []))


def _via_codex(prompt, images):
    with tempfile.TemporaryDirectory() as td:
        files = []
        for n, b in enumerate(images):
            f = Path(td) / f"i{n}.jpg"
            f.write_bytes(b)
            files.append(str(f))
        out = Path(td) / "out.txt"
        cmd = ["codex", "exec", "--skip-git-repo-check", "--ephemeral", "-s", "read-only", "-o", str(out)]
        for f in files:
            cmd += ["-i", f]
        subprocess.run(cmd + ["--", prompt], stdin=subprocess.DEVNULL, capture_output=True, timeout=600, cwd=td, check=True)
        return out.read_text(encoding="utf-8")


def ask_images(prompt, paths, edge=1024, provider=None):
    """Trả về chữ câu trả lời. Nhà cung cấp chính lỗi thì chuyển sang nhà cung cấp còn lại."""
    images = [_jpeg(p, edge) for p in paths]
    first = provider or machine().get("review_provider", "9router")
    order = [first] + [x for x in ("9router", "codex") if x != first]
    err = None
    for name in order:
        try:
            return (_via_codex if name == "codex" else _via_9router)(prompt, images)
        except Exception as e:  # lỗi mạng, hết hạn mức: thử bên còn lại
            err = e
    raise RuntimeError(f"Không chấm được bằng {order}: {err}")


def ask_json(prompt, paths, edge=1024, provider=None):
    return router.json_in(ask_images(prompt, paths, edge, provider))


if __name__ == "__main__":
    import sys
    print(ask_images(sys.argv[1], sys.argv[2:]))
