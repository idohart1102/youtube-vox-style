"""Procedural painterly backgrounds: build a base color field, then paint it with brush strokes."""
import sys, math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy.ndimage import gaussian_filter, zoom

W, H = 2400, 1350
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "backgrounds")
os.makedirs(OUT, exist_ok=True)


def hexc(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], dtype=np.float32)


def vgrad(stops, h=H, w=W):
    """stops: list of (pos 0..1, hex)"""
    ys = np.linspace(0, 1, h)
    out = np.zeros((h, 3), np.float32)
    for c in range(3):
        out[:, c] = np.interp(ys, [s[0] for s in stops], [hexc(s[1])[c] for s in stops])
    return np.repeat(out[:, None, :], w, axis=1)


def noise(seed, scale=40, h=H, w=W):
    r = np.random.default_rng(seed)
    small = r.random((h // scale + 2, w // scale + 2)).astype(np.float32)
    big = zoom(small, scale, order=3)[:h, :w]
    big = gaussian_filter(big, scale / 3)
    big = (big - big.min()) / (big.max() - big.min() + 1e-6)
    return big


def blob(img, cx, cy, rx, ry, color, strength=1.0):
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    d = ((xs - cx * W) / (rx * W)) ** 2 + ((ys - cy * H) / (ry * H)) ** 2
    a = np.exp(-d * 2.5)[..., None] * strength
    return img * (1 - a) + hexc(color) * a


def mix_noise(img, seed, color, amt=0.25, scale=60, thresh=0.5, y0=0.0, y1=1.0):
    n = noise(seed, scale)
    ys = np.linspace(0, 1, H)[:, None]
    m = np.clip((ys - y0) / 0.04 + (y0 <= 0) * 9, 0, 1) * np.clip((y1 - ys) / 0.04 + (y1 >= 1) * 9, 0, 1)
    a = (np.clip((n - thresh) * 3, 0, 1) * m)[..., None] * amt
    return img * (1 - a) + hexc(color) * a


def band(img, y0, y1, color, soft=0.02, wav=0.0, seed=0, amt=1.0):
    """horizontal band between y0,y1 (fractions) with wavy edges"""
    ys = np.linspace(0, 1, H)[:, None]
    n = (noise(seed, 120)[0:1, :] - 0.5) * wav if wav else 0
    top = y0 + n
    a = np.clip((ys - top) / soft, 0, 1)
    if y1 < 1:
        a = a * np.clip((y1 + n - ys) / soft, 0, 1)
    a = a[..., None] * amt
    return img * (1 - a) + hexc(color) * a


def paint(base, seed, flow=0.0, flow_var=0.6, passes=None, final_blur=0.6):
    rng = np.random.default_rng(seed)
    base = np.clip(base, 0, 255)
    im = Image.fromarray(base.astype(np.uint8)).filter(ImageFilter.GaussianBlur(6))
    dr = ImageDraw.Draw(im, "RGBA")
    angf = noise(seed + 7, 160) * flow_var * math.pi - flow_var * math.pi / 2 + flow
    passes = passes or [(9000, 90, 22, 70), (22000, 50, 11, 80), (30000, 22, 5, 95)]
    for count, L, Wd, alpha in passes:
        xs = rng.integers(0, W, count)
        ys = rng.integers(0, H, count)
        for x, y in zip(xs, ys):
            c = base[y, x] + rng.normal(0, 9, 3)
            c = np.clip(c, 0, 255).astype(int)
            a = angf[y, x] + rng.normal(0, 0.12)
            l = L * rng.uniform(0.5, 1.2)
            bend = rng.normal(0, 0.25)
            pts = []
            for t in np.linspace(-0.5, 0.5, 5):
                aa = a + bend * t
                pts.append((x + math.cos(aa) * l * t, y + math.sin(aa) * l * t))
            wd = max(1, int(Wd * rng.uniform(0.6, 1.2)))
            dr.line(pts, fill=(int(c[0]), int(c[1]), int(c[2]), alpha), width=wd, joint="curve")
    im = im.filter(ImageFilter.GaussianBlur(final_blur))
    return im


def save(name, im):
    im.save(f"{OUT}/{name}.jpg", quality=90)
    print("saved", name, flush=True)


def build(name):
    if name == "space":
        b = vgrad([(0, "#070a14"), (0.6, "#0d1426"), (1, "#151a2c")])
        b = mix_noise(b, 1, "#3a2450", 0.55, 220, 0.45)
        b = mix_noise(b, 2, "#1c4a5a", 0.45, 160, 0.55)
        b = blob(b, 0.85, 0.5, 0.35, 0.5, "#2a3a66", 0.5)
        save(name, paint(b, 11, flow=-0.4, flow_var=1.2))
    elif name == "sunset":
        b = vgrad([(0, "#3b2a55"), (0.35, "#c4623d"), (0.55, "#f2b05a"), (0.62, "#f6d38c"), (0.66, "#9a6a54"), (1, "#5a3a2a")])
        b = blob(b, 0.62, 0.58, 0.18, 0.12, "#fff1c0", 0.9)
        b = mix_noise(b, 3, "#e48a5a", 0.35, 200, 0.5, y1=0.6)
        b = band(b, 0.6, 0.7, "#7a5470", 0.01, wav=0.06, seed=5, amt=0.7)
        b = band(b, 0.68, 1, "#a8743e", 0.02, wav=0.03, seed=6)
        b = mix_noise(b, 4, "#6a4a2a", 0.4, 50, 0.5, y0=0.7)
        save(name, paint(b, 12, flow=0.0, flow_var=0.3))
    elif name == "forest":
        b = vgrad([(0, "#9fc3c9"), (0.4, "#d9e6cf"), (0.62, "#c9d7b0"), (0.72, "#7f9a64"), (1, "#4f6a3a")])
        b = blob(b, 0.7, 0.25, 0.25, 0.3, "#fff6d8", 0.6)
        b = mix_noise(b, 7, "#eef3e6", 0.4, 200, 0.55, y1=0.7)
        b = band(b, 0.5, 0.75, "#8fac9c", 0.03, wav=0.1, seed=8, amt=0.55)
        b = band(b, 0.72, 1, "#5d7a3e", 0.02, wav=0.03, seed=9)
        b = mix_noise(b, 10, "#3f5a2e", 0.5, 40, 0.5, y0=0.74)
        b = mix_noise(b, 11, "#8a7a4a", 0.3, 30, 0.6, y0=0.74)
        save(name, paint(b, 13, flow=0.0, flow_var=0.4))
    elif name == "underground":
        b = vgrad([(0, "#b9cfc4"), (0.2, "#aac0a0"), (0.23, "#4f6a33"), (0.27, "#5b4430"), (0.5, "#6e4f35"), (0.75, "#4f3828"), (1, "#3a281d")])
        for i, (y, c) in enumerate([(0.4, "#7d5d3e"), (0.58, "#5a412c"), (0.8, "#806048"), (0.9, "#46321f")]):
            b = band(b, y, y + 0.05, c, 0.02, wav=0.05, seed=20 + i, amt=0.6)
        b = mix_noise(b, 30, "#2e2016", 0.4, 30, 0.55, y0=0.25)
        save(name, paint(b, 14, flow=0.0, flow_var=0.5))
    elif name == "water":
        b = vgrad([(0, "#b7d1cf"), (0.3, "#d8e4d0"), (0.42, "#8ea98a"), (0.5, "#6d8f8a"), (0.68, "#4f7478"), (0.72, "#6b5a3e"), (1, "#4a3a28")])
        b = blob(b, 0.3, 0.2, 0.2, 0.2, "#fff7dc", 0.5)
        b = band(b, 0.68, 1, "#6a5638", 0.02, wav=0.08, seed=40)
        b = mix_noise(b, 41, "#3e3020", 0.45, 30, 0.5, y0=0.72)
        b = mix_noise(b, 42, "#93b4ac", 0.25, 60, 0.6, y0=0.45, y1=0.7)
        save(name, paint(b, 15, flow=0.0, flow_var=0.15))
    elif name == "storm":
        b = vgrad([(0, "#2c3240"), (0.4, "#6a6a70"), (0.7, "#c49a6a"), (1, "#6a5040")])
        b = mix_noise(b, 50, "#1d2230", 0.6, 180, 0.45)
        b = mix_noise(b, 51, "#e0b88a", 0.35, 150, 0.6)
        save(name, paint(b, 16, flow=0.3, flow_var=1.0))
    elif name == "fire":
        b = vgrad([(0, "#2a0e0a"), (0.3, "#7a1f12"), (0.55, "#d8541e"), (0.68, "#f6a03a"), (0.74, "#4a1c10"), (1, "#1e0a06")])
        b = mix_noise(b, 60, "#3a0c08", 0.6, 180, 0.45, y1=0.72)
        b = mix_noise(b, 61, "#ffcf6a", 0.4, 150, 0.62, y1=0.72)
        b = band(b, 0.72, 1, "#2a120a", 0.02, wav=0.05, seed=62)
        save(name, paint(b, 17, flow=-0.2, flow_var=1.2))
    elif name == "dusk":
        b = vgrad([(0, "#1f1f3a"), (0.4, "#6a3a5a"), (0.6, "#e0703a"), (0.68, "#f8c070"), (0.7, "#3a2230"), (1, "#1a1018")])
        b = blob(b, 0.5, 0.66, 0.12, 0.08, "#fff0c0", 0.9)
        b = mix_noise(b, 70, "#a04a50", 0.35, 200, 0.5, y1=0.68)
        save(name, paint(b, 18, flow=0.0, flow_var=0.3))
    elif name == "strata":
        stops = [(0, "#c8b48e"), (0.12, "#b49a72"), (0.13, "#8a7050"), (0.3, "#9a8060"), (0.31, "#d6c6a0"), (0.42, "#c8b490"),
                 (0.43, "#5a3a2a"), (0.47, "#4a2e22"), (0.48, "#b8a080"), (0.7, "#a08868"), (0.71, "#7a6048"), (1, "#5a4636")]
        b = vgrad(stops)
        b = mix_noise(b, 80, "#6a5440", 0.35, 25, 0.55)
        b = mix_noise(b, 81, "#e2d6b8", 0.25, 35, 0.6)
        save(name, paint(b, 19, flow=0.0, flow_var=0.25))
    elif name == "parchment":
        b = vgrad([(0, "#e9dcbc"), (1, "#d9c79f")])
        b = mix_noise(b, 90, "#c9b285", 0.5, 60, 0.5)
        b = blob(b, 0.5, 0.5, 0.6, 0.6, "#f2e8cc", 0.4)
        save(name, paint(b, 20, flow=0.2, flow_var=1.5, passes=[(9000, 60, 18, 40), (20000, 25, 6, 50)]))
    elif name == "seafloor":
        b = vgrad([(0, "#cfe6e0"), (0.12, "#8fd0cc"), (0.3, "#3f9aa6"), (0.36, "#d8caa0"), (0.4, "#e8e0c8"),
                   (0.55, "#ddd2b4"), (0.56, "#c9bfa6"), (0.7, "#e2d8c0"), (0.71, "#bfb398"), (0.85, "#d6cdb6"), (0.86, "#a89c84"), (1, "#8a7e68")])
        b = mix_noise(b, 100, "#f4eedc", 0.3, 30, 0.6, y0=0.36)
        b = mix_noise(b, 101, "#9a8e74", 0.25, 25, 0.6, y0=0.36)
        save(name, paint(b, 21, flow=0.0, flow_var=0.15))
    elif name == "ocean":
        b = vgrad([(0, "#1d5a6e"), (0.5, "#2a8a96"), (1, "#56b9b4")])
        b = mix_noise(b, 110, "#8fdad0", 0.45, 50, 0.55)
        b = mix_noise(b, 111, "#14404e", 0.4, 70, 0.5)
        save(name, paint(b, 22, flow=0.4, flow_var=1.4))


def paper():
    rng = np.random.default_rng(5)
    g = rng.normal(0, 1, (1080, 1920)).astype(np.float32)
    fine = gaussian_filter(g, 0.7)
    coarse = noise(6, 50, 1080, 1920) - 0.5
    fib = gaussian_filter(rng.normal(0, 1, (1080, 1920)).astype(np.float32), (0.6, 6))
    v = 236 + fine * 10 + coarse * 22 + fib * 14
    im = Image.fromarray(np.clip(v, 0, 255).astype(np.uint8), "L")
    im.save(f"{OUT}/paper.png")
    print("saved paper")


if __name__ == "__main__":
    names = sys.argv[2:] or ["space", "sunset", "forest", "underground", "water", "storm", "fire", "dusk", "strata", "parchment", "seafloor", "ocean", "paper"]
    for n in names:
        paper() if n == "paper" else build(n)
