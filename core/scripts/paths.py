"""Tìm thư mục gốc và đọc cấu hình máy. Mọi script khác import file này, không dùng đường dẫn tuyệt đối."""
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[2]


def load_yaml(p):
    import yaml
    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def machine():
    p = ROOT / "config" / "machine.yaml"
    if not p.exists():
        p = ROOT / "config" / "machine.example.yaml"
    return load_yaml(p)


def load_env():
    try:
        from dotenv import load_dotenv
        load_dotenv(ROOT / ".env")
    except ImportError:
        pass
    return os.environ


def assets_dir():
    d = Path(machine().get("assets_dir", "assets"))
    return d if d.is_absolute() else ROOT / d


def channel_dir(slug):
    d = ROOT / "channels" / slug
    if not d.exists():
        raise SystemExit(f"Không có kênh: {slug}")
    return d
