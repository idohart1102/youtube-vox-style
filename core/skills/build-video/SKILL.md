---
name: build-video
description: Dựng video một tập từ audio và srt Sếp gửi cùng storyboard.md, cho mọi kênh. Tự lập danh sách asset, tạo ảnh AI qua 9router, tìm ảnh thật có giấy phép mở, rồi dựng chuyển động kiểu Vox bằng Remotion. Thời gian lấy từ srt, luật hình lấy từ channels/<slug>/visual.md.
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
3. Viết `asset_plan.json` (mẫu: `core/templates/asset_plan.example.json`). Mỗi hình cần cho video là 1 mục `{id, kind, role, file, prompt | query, species, tags}`:
   - Tra kho trước bằng lệnh lọc `assets/index.json` theo tag. Có hình hợp thì dùng `kind: "reuse"`.
   - `kind: "ai"`: paleoart, cảnh tái hiện. `role: "bg"` là ảnh nền không có nhân vật; `role: "cutout"` là 1 sinh vật hoặc vật thể, PNG nền trong suốt, để Remotion chồng lớp. Prompt viết tiếng Anh, tả bối cảnh Việt Nam cổ, không yêu cầu chữ trong ảnh.
   - Loài xuất hiện nhiều lần: khai báo 1 lần trong `species` (màu da, tỉ lệ, đặc điểm) rồi gắn `species` vào mọi mục của loài đó, để các cảnh trông cùng một con.
   - `kind: "real"`: hiện vật, hóa thạch, hang, địa điểm, hình khoa học có thật. `query` tả cụ thể cần tìm gì. Không bao giờ dùng AI để làm giả ảnh thật.
   - Bản đồ hiện đại không tạo ảnh, dùng component GeoMap. Bản đồ cổ dùng `kind: "real"` (PALEOMAP của Scotese, CC BY).
   - Một nền dùng cho nhiều cảnh (đổi cutout, đổi hướng máy). Tập 15 phút khoảng 30-50 ảnh AI.
   - Hình là đáp án của một `[HỎI: q]` trong storyboard: ghi `answer_of: "q"`. Không tạo ảnh riêng cho bản ẩn, Remotion tự ẩn bằng `hide`. Nếu storyboard có câu hỏi kết bằng "?" được trả lời về sau mà thiếu thẻ, thêm `[HỎI]`/`[ĐÁP]` (không sửa lời đọc) rồi chạy lại bước 1.
4. Chạy `python core/scripts/gen_assets.py <tập>`. Script tạo ảnh AI qua 9router, tìm ảnh thật có giấy phép mở, ghi nguồn vào `assets/credits.json`, rồi xuất `asset_sheet.jpg`.
   - Mở `asset_sheet.jpg` xem: sai giải phẫu, chữ rác, lệch nội dung thì sửa prompt rồi chạy lại với `--redo id1,id2`, tối đa 2 lần.
   - Ảnh thật không tìm được thì đổi `query`, hoặc chạy `--codex` để Codex CLI tìm. Vẫn không có thì ghi vào `missing_assets.md`.
5. Viết `scenes.json`. Mỗi cảnh gồm `id`, `lines: [câu đầu, câu cuối]`, `component`, `asset`, `props`, và nếu cần thì `transition`, `fixed_s`. Không ghi `duration_s`. Không tự viết chữ trên màn hình dài quá 6 từ. Không dùng Creature (hình SVG).
   - Chuyển động theo phần "Chuyển động" của README và visual.md: mỗi cảnh 1 chuyển động máy, tối đa 1 hiệu ứng chính, chỉ cutout chính có `motion`; đổi kiểu qua các cảnh để đa dạng nhưng không dồn nhiều hiệu ứng vào một cảnh.
   - Asset `answer_of` dùng trước câu [ĐÁP] phải có `hide`. Không cần ghi `unmask_s`, bước 6 tự điền.
6. Chạy `python core/scripts/align_srt.py <tập> --apply`. Bước này tính `duration_s` theo srt, điền narration, tự gắn badge, thẻ keyword và dòng nguồn ảnh thật.
7. Chạy `python core/scripts/validate_scenes.py <tập>/scenes.json`. Báo lỗi nhịp thì gộp hoặc tách cảnh, rồi lặp lại từ bước 6 cho tới khi OK.
8. Chạy `python core/scripts/produce.py <tập> --preview` để xem nhanh, rồi bỏ `--preview` để ra `render/final.mp4`. Thêm `--no-subs` nếu Sếp muốn bỏ phụ đề.
9. Điền vào meta.md:
   - chapters lấy từ `chapters` trong timeline.json, mốc đầu là 0:00;
   - mục "Nguồn ảnh" lấy từ `assets/credits.json`, chỉ các ảnh tập này dùng.
   Sau đó chuyển sang skill package để ghép thumbnail.

Báo Sếp: đường dẫn mp4, thời lượng, số cảnh, tỉ lệ khớp srt, số ảnh AI đã tạo, số ảnh thật, và các asset còn thiếu. Không dán log dài.
