"""Kiểm tra máy hiện tại đủ điều kiện vận hành chưa. Dùng: python core/scripts/doctor.py [--smoke]
--smoke: thêm bài dựng thử 3 giây từ đầu đến cuối, không cần API key."""
import json, shutil, subprocess, sys
from pathlib import Path
from paths import ROOT, load_env, machine
import channel as chan

m, env, bad, warn = machine(), load_env(), [], []


def ver(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=20).stdout.strip()
    except Exception:
        return ""


for tool in [m.get("ffmpeg", "ffmpeg"), "ffprobe", "node", "git", "git-lfs"]:
    if not shutil.which(tool):
        bad.append(f"thiếu {tool}")
want_node = (ROOT / ".nvmrc").read_text().strip()
have = ver(["node", "--version"]).lstrip("v").split(".")[0]
if have and have != want_node:
    warn.append(f"Node {have}, repo dùng Node {want_node}")
want_py = (ROOT / ".python-version").read_text().strip()
now_py = f"{sys.version_info[0]}.{sys.version_info[1]}"
if now_py != want_py:
    warn.append(f"Python {now_py}, repo dùng Python {want_py}")
if not (ROOT / "node_modules").exists():
    bad.append("chưa npm install (chạy setup.sh)")
if not (ROOT / "config" / "machine.yaml").exists():
    bad.append("chưa có config/machine.yaml")
if not list((ROOT / "assets" / "shared" / "textures").glob("*.jpg")):
    bad.append("thiếu asset dùng chung: chạy git lfs pull")
else:
    head = (ROOT / "assets" / "shared" / "textures" / "tang-da.jpg").read_bytes()[:40]
    if head.startswith(b"version https://git-lfs"):
        bad.append("asset dùng chung mới là con trỏ LFS: chạy git lfs pull")

# Dịch vụ: thiếu không chặn việc dựng nhưng phải báo rõ bước nào không chạy được
try:
    import requests
    url = m.get("router_url", "http://localhost:20128/v1")
    r = requests.get(url + "/models", timeout=5)
    if r.status_code >= 500:
        raise RuntimeError(r.status_code)
except Exception:
    warn.append("9router chưa chạy: tạo ảnh và QC sẽ không chạy (xem docs/handover.md)")
if not shutil.which("codex"):
    warn.append("chưa có Codex CLI: mất phương án dự phòng cho QC")
if not env.get("ELEVENLABS_API_KEY"):
    warn.append("chưa có ELEVENLABS_API_KEY: chỉ dựng được khi Sếp gửi audio và srt")
mode = m.get("drive_mode", "desktop")
if mode == "desktop" and not Path(str(m.get("drive_path", ""))).is_dir():
    warn.append("drive_path chưa đúng: publish_clean.py chưa chạy được")
if mode == "rclone" and not (shutil.which("rclone") and m.get("drive_remote")):
    warn.append("rclone hoặc drive_remote chưa sẵn sàng: publish_clean.py chưa chạy được")
for d in sorted((ROOT / "channels").glob("*/channel.yaml")):
    if d.parent.name.startswith("_"):
        continue
    bad += [f"kênh {d.parent.name}: {p}" for p in chan.check(chan.load(d.parent))]

if "--smoke" in sys.argv and not bad:
    r = subprocess.run([sys.executable, str(ROOT / "core" / "tests" / "run.py"), "--smoke"], cwd=ROOT)
    if r.returncode:
        bad.append("bài dựng thử thất bại")
for w in warn:
    print("! " + w)
print("ALL OK" if not bad else "\n".join("✗ " + b for b in bad))
sys.exit(1 if bad else 0)
