"""Đọc script.md → audio/narration.mp3 bằng ElevenLabs. Dùng: python3 tts_elevenlabs.py <episode_dir>
voice_id và model lấy từ channel.yaml của kênh chứa tập đó."""
import re, sys
from pathlib import Path
import requests, yaml
from paths import load_env

ep = Path(sys.argv[1]).resolve()
ch = yaml.safe_load((ep.parents[1] / "channel.yaml").read_text(encoding="utf-8"))
v = ch["voice"]
text = (ep / "script.md").read_text(encoding="utf-8")
# Chỉ lấy lời đọc: bỏ dòng tiêu đề (#) và ghi chú cảnh [..]
text = "\n".join(l for l in text.splitlines() if l.strip() and not l.startswith("#"))
text = re.sub(r"\[[^\]]*\]", "", text)
r = requests.post(
    f"https://api.elevenlabs.io/v1/text-to-speech/{v['voice_id']}",
    headers={"xi-api-key": load_env()["ELEVENLABS_API_KEY"]},
    json={"text": text, "model_id": v.get("model", "eleven_multilingual_v2"),
          "voice_settings": {"stability": v.get("stability", 0.55), "similarity_boost": v.get("similarity", 0.75),
                             "style": v.get("style", 0.1), "speed": v.get("speed", 0.95)}},
    timeout=600,
)
r.raise_for_status()
(ep / "audio").mkdir(exist_ok=True)
(ep / "audio" / "narration.mp3").write_bytes(r.content)
print("audio/narration.mp3", len(r.content) // 1024, "KB")
