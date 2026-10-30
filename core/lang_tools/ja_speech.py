"""Tiếng Nhật: chữ hiển thị (phụ đề) và chữ an toàn cho giọng AI. Luật ở script/lang.md của kênh.
display(s): bỏ phần đọc 《》 và dấu ｜.   speak(s): lấy cách đọc 《》, tra ja-readings.tsv, đổi số + đơn vị sang kana."""
import re
from pathlib import Path

READINGS = None  # script/readings.tsv của kênh, do setup() gán
RUBY = re.compile(r"(?:｜([^《｜]+)|([一-鿿々〆ヵヶ0-9０-９A-Za-z.]+))《([^》]+)》")
DIG = "ゼロ いち に さん よん ご ろく なな はち きゅう".split()
HUNDRED = {1: "ひゃく", 3: "さんびゃく", 6: "ろっぴゃく", 8: "はっぴゃく"}
THOUSAND = {1: "せん", 3: "さんぜん", 8: "はっせん"}
UNITS = [("キロメートル", "キロメートル"), ("km", "キロメートル"), ("cm", "センチメートル"), ("kg", "キログラム"),
         ("m", "メートル"), ("t", "トン"), ("℃", "ど"), ("°C", "ど"), ("%", "パーセント"), ("％", "パーセント"),
         ("年前", "ねんまえ"), ("年後", "ねんご"), ("年間", "ねんかん"), ("年", "ねん"), ("倍", "ばい"), ("度", "ど"),
         ("種", "しゅ"), ("個", "こ"), ("回", "かい"), ("時間", "じかん"), ("秒", "びょう")]
SHOU = {1: "いっしょう", 6: "ろくしょう", 8: "はっしょう", 10: "じゅっしょう"}  # 第1章 → だいいっしょう
NUM = re.compile(r"(?:\d[\d,]*(?:\.\d+)?[兆億万]?)+")


def _under10k(n, big=False):
    th, hu, te, on = n // 1000, n // 100 % 10, n // 10 % 10, n % 10
    out = ""
    if th:
        out += "いっせん" if th == 1 and big else THOUSAND.get(th, DIG[th] + "せん")
    if hu:
        out += HUNDRED.get(hu, DIG[hu] + "ひゃく")
    if te:
        out += ("" if te == 1 else DIG[te]) + "じゅう"
    if on:
        out += DIG[on]
    return out


def kana_int(n):
    if n == 0:
        return "ゼロ"
    out = ""
    for unit, size in (("ちょう", 10**12), ("おく", 10**8), ("まん", 10**4)):
        if n >= size:
            out += _under10k(n // size, big=True) + unit
            n %= size
    return out + _under10k(n)


def kana_number(tok):
    tok = tok.replace(",", "")
    if "." in tok and not re.search(r"[兆億万]\d", tok):  # 2.5倍, 1.5万
        m = re.fullmatch(r"(\d+)\.(\d+)([兆億万]?)", tok)
        if m:
            unit = {"兆": "ちょう", "億": "おく", "万": "まん", "": ""}[m[3]]
            return kana_int(int(m[1])) + "てん" + "".join(DIG[int(d)] for d in m[2]) + unit
    total = 0
    for num, unit in re.findall(r"(\d+)([兆億万]?)", tok):
        total += int(num) * {"兆": 10**12, "億": 10**8, "万": 10**4, "": 1}[unit]
    return kana_int(total)


def _readings():
    pairs = []
    for line in READINGS.read_text(encoding="utf-8").splitlines():
        if line and not line.startswith("#") and "\t" in line:
            k, v = line.split("\t", 1)
            pairs.append((k.strip(), v.strip()))
    return dict(pairs)


def setup(cfg):
    global READINGS
    READINGS = Path(cfg["_dir"]) / "script" / "readings.tsv"


def words(text):
    return [c for c in text.lower() if re.match(r"\w", c)]


def count(s):
    return count_chars(display(s))


def display(s):
    return RUBY.sub(lambda m: m[1] or m[2], s).replace("｜", "")


def speak(s, readings=None):
    s = RUBY.sub(lambda m: m[3], s).replace("｜", "")
    readings = readings if readings is not None else _readings()
    if readings:
        rx = re.compile("|".join(map(re.escape, sorted(readings, key=len, reverse=True))))
        s = rx.sub(lambda m: readings[m[0]], s)
    s = re.sub(r"第(\d+)章", lambda m: "だい" + SHOU.get(int(m[1]), kana_int(int(m[1])) + "しょう"), s)
    unit_rx = "|".join(re.escape(u) for u, _ in UNITS)
    unit_map = dict(UNITS)

    def num(m):
        return kana_number(m[1]) + (unit_map[m[2]] if m[2] else "")
    return re.sub(rf"({NUM.pattern})({unit_rx})?", num, s)


def count_chars(s):
    return len(re.sub(r"[\s、。，．！？!?…「」『』（）()・]", "", s))


if __name__ == "__main__":
    for t in ["6600万年前、地層《ちそう》から化石が見つかりました。", "2億5200万年前", "気温は60℃、酸素は12%。",
              "体長12メートル、2.5倍", "1968年、穂別で3匹《さんびき》", "1000万年", "8000年前", "1.5万年前", "第1章と第2章、第8章"]:
        print(t, "→", speak(t), "|", display(t))
