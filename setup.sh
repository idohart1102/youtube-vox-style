#!/usr/bin/env bash
# Cài đặt trên máy mới. Chạy lại nhiều lần cũng an toàn.
set -e
cd "$(dirname "$0")"
ok=1
for c in node npm python3 ffmpeg; do
  if command -v $c >/dev/null 2>&1; then echo "✓ $c"; else echo "✗ thiếu $c (macOS: brew install ${c/npm/node})"; ok=0; fi
done
[ $ok = 1 ] || { echo "Cài các công cụ còn thiếu rồi chạy lại."; exit 1; }
[ -d .venv ] || python3 -m venv .venv
.venv/bin/pip install -q -r requirements.txt
npm install --silent
[ -f config/machine.yaml ] || cp config/machine.example.yaml config/machine.yaml
[ -f .env ] || cp .env.example .env
echo "Xong. Điền .env và kiểm tra config/machine.yaml, sau đó chạy: .venv/bin/python core/scripts/doctor.py"
