---
name: produce
description: Chạy pipeline giọng đọc, phụ đề, render cho một tập. Chỉ chạy lệnh, không đọc source.
---
Chạy `python core/scripts/produce.py channels/<slug>/episodes/<tap>` để ra bản cuối (render/final.mp4) và kiểm tra máy. Có `audio/voice.*` và `.srt` của Sếp thì dùng skill build-video (không gọi ElevenLabs). `--no-subs` để tắt phụ đề.
- Nếu lỗi: chỉ đọc 20 dòng cuối của log. Chỉ mở đúng script báo lỗi, không mở cả thư mục.
- Không in log dài ra cho người dùng. Báo kết quả gồm đường dẫn file mp4 và thời lượng.
