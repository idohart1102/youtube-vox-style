"""Kiểm tra máy hiện tại đã đủ điều kiện chạy hệ thống chưa."""
import shutil, sys
from paths import ROOT, machine, load_env

m, env, bad = machine(), load_env(), []
for tool in [m.get("ffmpeg", "ffmpeg"), "node"]:
    if not shutil.which(tool):
        bad.append(f"thiếu {tool}")
if not (ROOT / "node_modules").exists():
    bad.append("chưa npm install (chạy setup.sh)")
if not env.get("ELEVENLABS_API_KEY"):
    bad.append("chưa có ELEVENLABS_API_KEY trong .env")
if not (ROOT / "config" / "machine.yaml").exists():
    bad.append("chưa có config/machine.yaml")
print("ALL OK" if not bad else "\n".join("✗ " + b for b in bad))
sys.exit(1 if bad else 0)
