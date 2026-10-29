"""Pipeline không tốn token, chạy được trên Windows/macOS/Linux: (srt → thời gian cảnh) → kiểm tra cảnh → giọng đọc → render.
Dùng: python core/scripts/produce.py channels/<slug>/episodes/<tap> [--preview] [--no-subs]
Có audio/voice.* và audio/*.srt của Sếp thì dùng luôn, bỏ qua ElevenLabs."""
import subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ep = Path(sys.argv[1]).resolve()
py = sys.executable
srt = [p for p in (ep / "audio").glob("*.srt") if not p.name.endswith(".clean.srt")] if (ep / "audio").exists() else []
if srt:
    subprocess.run([py, str(HERE / "align_srt.py"), str(ep)], check=True)
    if '"lines"' in (ep / "scenes.json").read_text(encoding="utf-8"):
        subprocess.run([py, str(HERE / "align_srt.py"), str(ep), "--apply"], check=True)
subprocess.run([py, str(HERE / "validate_scenes.py"), str(ep / "scenes.json")], check=True)
has_voice = any((ep / "audio").glob("voice.*")) if (ep / "audio").exists() else False
if "--preview" not in sys.argv and not has_voice and not (ep / "audio" / "narration.mp3").exists():
    subprocess.run([py, str(HERE / "tts_elevenlabs.py"), str(ep)], check=True)
subprocess.run(["node", str(HERE / "render.mjs"), str(ep)] + sys.argv[2:], check=True)
