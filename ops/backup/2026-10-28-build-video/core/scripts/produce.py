"""Pipeline không tốn token, chạy được trên Windows/macOS/Linux: kiểm tra cảnh → giọng đọc → render.
Dùng: python core/scripts/produce.py channels/<slug>/episodes/<tap> [--preview]"""
import subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ep = Path(sys.argv[1]).resolve()
py = sys.executable
subprocess.run([py, str(HERE / "validate_scenes.py"), str(ep / "scenes.json")], check=True)
if "--preview" not in sys.argv and not (ep / "audio" / "narration.mp3").exists():
    subprocess.run([py, str(HERE / "tts_elevenlabs.py"), str(ep)], check=True)
subprocess.run(["node", str(HERE / "render.mjs"), str(ep)] + sys.argv[2:], check=True)
