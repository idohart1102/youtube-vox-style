"""Tiếng Việt: giọng AI đọc đơn vị viết thành chữ, còn màn hình hiện ký hiệu; tên Latin kèm cách đọc trong ngoặc. Luật ở script/lang.md của kênh.
display: "Chicxulub (chích-xu-lúp), 10 ki-lô-mét" → "Chicxulub, 10 km".   speak: → "chích-xu-lúp, 10 ki-lô-mét"."""
import re
from plain import count, words  # noqa: F401

LATIN = r"[A-Za-z]+(?: [A-Za-z]+)? \(([^()]*-[^()]*)\)"
UNITS = [(r"ki-lô-mét vuông", "km²"), (r"ki-lô-mét", "km"), (r"ki-lô-gam", "kg"), (r"phần trăm", "%"), (r"độ C", "°C"), (r"mét", "m")]


def screen(text):
    for word, sym in UNITS:
        text = re.sub(rf"(\d[\d.,]*) {word}\b", (rf"\1{sym}" if sym in ("%", "°C") else rf"\1 {sym}"), text)
    return text


def display(s):
    return screen(re.sub(r" \(([^()]*-[^()]*)\)", "", s))


def speak(s):
    return re.sub(LATIN, r"\1", s)
