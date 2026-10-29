import sys
from PIL import Image
names, out = sys.argv[2:], sys.argv[1]
cols, cw, ch = 4, 480, 320
sheet = Image.new("RGB", (cols * cw, ((len(names) + cols - 1) // cols) * ch), (233, 223, 200))
for i, p in enumerate(names):
    im = Image.open(p).convert("RGBA"); im.thumbnail((cw - 10, ch - 10))
    sheet.paste(im, ((i % cols) * cw + (cw - im.width) // 2, (i // cols) * ch + (ch - im.height) // 2), im)
sheet.save(out, quality=85)
