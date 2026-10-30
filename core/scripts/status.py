"""Tiến độ từng tập: status.yaml trong thư mục tập cho biết đang ở bước nào, ai giữ, đã duyệt gì. Người hoặc AI nhận việc đọc đây trước.
  python core/scripts/status.py                         bảng mọi kênh
  python core/scripts/status.py <tập> stage=render final=ok   cập nhật (khóa: stage, owner, brief, final, note, species)
Bước: brief → script → audio → assets → build → render → qc → publish → done."""
import sys
from pathlib import Path
import yaml
from paths import ROOT

STAGES = ["brief", "script", "audio", "assets", "build", "render", "qc", "publish", "done"]
DEFAULT = {"stage": "brief", "owner": "", "approved": {"brief": None, "final": None}, "species": [], "qc_rounds": 0, "publish": {}, "note": ""}


def read(ep):
    p = Path(ep) / "status.yaml"
    d = yaml.safe_load(p.read_text(encoding="utf-8")) if p.exists() else {}
    return {**DEFAULT, **(d or {})}


def write(ep, d):
    (Path(ep) / "status.yaml").write_text(yaml.safe_dump(d, allow_unicode=True, sort_keys=False), encoding="utf-8")


def set_values(ep, pairs):
    d = read(ep)
    for k, v in pairs:
        if k in ("brief", "final"):
            d["approved"][k] = v
        elif k == "species":
            d["species"] = [x for x in v.split(",") if x]
        elif k == "stage" and v not in STAGES:
            raise SystemExit(f"Bước không hợp lệ: {v}. Dùng: {', '.join(STAGES)}")
        else:
            d[k] = v
    write(ep, d)


def recent_species(channel_dir, n):
    """Nhân vật chính của N tập gần nhất, để không lặp loài."""
    eps = sorted((Path(channel_dir) / "episodes").glob("*/status.yaml"))[-n:]
    out = []
    for p in eps:
        out += (yaml.safe_load(p.read_text(encoding="utf-8")) or {}).get("species", [])
    return out


if __name__ == "__main__":
    if len(sys.argv) > 2:
        set_values(sys.argv[1], [a.split("=", 1) for a in sys.argv[2:]])
        print(read(sys.argv[1]))
    else:
        print(f"{'KÊNH':<14}{'TẬP':<34}{'BƯỚC':<10}{'GIỮ':<10}DUYỆT")
        for ep in sorted(ROOT.glob("channels/*/episodes/*")):
            if ep.is_dir() and not ep.parent.parent.name.startswith("_"):
                d = read(ep)
                ok = ",".join(k for k, v in d["approved"].items() if v) or "-"
                print(f"{ep.parent.parent.name:<14}{ep.name[:32]:<34}{d['stage']:<10}{str(d['owner'])[:9]:<10}{ok}")
