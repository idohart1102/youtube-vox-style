---
name: build-video
description: Dựng video một tập từ audio và srt Sếp gửi cùng storyboard.md, cho mọi kênh. Thời gian lấy từ srt, luật hình lấy từ channels/<slug>/visual.md.
---
Đầu vào trong thư mục tập:
- `audio/voice.mp3` (hoặc wav, m4a)
- `audio/voice.srt`
- `storyboard.md`

Nếu thiếu storyboard.md mà chỉ có script.md, viết storyboard trước: thêm `## chương` và ghi chú [ ] theo visual.md, không sửa lời đọc.

1. Chạy `python core/scripts/align_srt.py <tập>`. Script tạo `timeline.json` (từng câu có thời gian, chương và ghi chú) và `audio/subs.clean.srt`.
   - Báo khớp dưới 90% thì dừng lại, báo Sếp các câu lệch. Thường do audio đọc khác kịch bản.
2. Đọc đúng 3 nguồn này, không đọc thêm:
   - `timeline.json`: chỉ lấy `lines`, bằng lệnh lọc, không in cả file.
   - `channels/<slug>/visual.md`
   - `core/remotion/README.md`
   Tra asset bằng lệnh lọc `assets/index.json` theo tag.
3. Viết `scenes.json`. Mỗi cảnh gồm `id`, `lines: [câu đầu, câu cuối]`, `component`, `asset`, `props`, và nếu cần thì `transition`, `fixed_s`. Không ghi `duration_s`. Không tự viết chữ trên màn hình dài quá 6 từ.
4. Chạy `python core/scripts/align_srt.py <tập> --apply`. Bước này tính `duration_s` theo srt, điền narration, tự gắn badge và thẻ keyword.
5. Chạy `python core/scripts/validate_scenes.py <tập>/scenes.json`. Báo lỗi nhịp thì gộp hoặc tách cảnh, rồi lặp lại từ bước 4 cho tới khi OK.
   - Asset còn thiếu thì ghi vào `missing_assets.md` của tập.
6. Chạy `python core/scripts/produce.py <tập> --preview` để xem nhanh, rồi bỏ `--preview` để ra `render/final.mp4`. Thêm `--no-subs` nếu Sếp muốn bỏ phụ đề.
7. Điền chapters vào meta.md từ `chapters` trong timeline.json, mốc đầu là 0:00. Sau đó chuyển sang skill package để ghép thumbnail.

Báo Sếp: đường dẫn mp4, thời lượng, số cảnh, tỉ lệ khớp srt, và các asset còn thiếu. Không dán log dài.
