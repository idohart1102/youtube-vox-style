---
name: produce
description: Chạy pipeline giọng đọc, phụ đề, render cho một tập. Chỉ chạy lệnh, không đọc source.
---
Chạy `python core/scripts/produce.py channels/<slug>/episodes/<tap> --preview` để xem nhanh, rồi bỏ `--preview` để ra bản cuối (render/final.mp4).
- Nếu lỗi: chỉ đọc 20 dòng cuối của log. Chỉ mở đúng script báo lỗi, không mở cả thư mục.
- Không in log dài ra cho người dùng. Báo kết quả gồm đường dẫn file mp4 và thời lượng.
