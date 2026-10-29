# Quy định dựng hình — Tiền Sử Đất Việt (Sếp duyệt 2026-10-28)
Đọc cùng theme.json (màu, font) và thumbnail.md. Mục tiêu: cuốn như phim tài liệu, chính xác như sách giáo khoa, gọn gàng kiểu Vox. Kênh tiếng Việt: mọi chữ trên màn hình là tiếng Việt.

## Phong cách hình
- Paleoart theo `art_style_prompt` của theme.json: Semi-Realistic Paleoart Concept Art, giải phẫu đúng, ánh sáng điện ảnh, nền tối.
- Ảnh thật (hóa thạch, lớp đất, hang) dùng PhotoCard: giữ màu gốc, khung mảnh màu accent, `credit` bắt buộc. Hiện ít nhất 4 giây.
- Cảnh tái hiện đặt `props.recon: true` để hiện thẻ "Tái hiện".
- Bản đồ hiện đại luôn có Hoàng Sa và Trường Sa. Bản đồ cổ dùng tông giấy tối, chấm Việt Nam ngày nay màu vàng #FFD23F.
- Mỗi cảnh chỉ 1 màu nhấn. Dùng danger cho thảm họa, jade cho sự sống hồi phục. Grain 0,3 và vignette 0,4 cho cả video, không thêm bộ lọc khác.

## Chữ trên màn hình: ít, không làm slide
- Chỉ dùng keyword hoặc số liệu, tối đa 6 từ, ví dụ "66 triệu năm trước", "15.000 km", "3/4 số loài".
- Không viết câu, không gạch đầu dòng, không đoạn văn.
- Mỗi lúc chỉ 1 khối chữ, không tính phụ đề. Thẻ keyword hiện 3 giây.
- Thẻ lấy từ [THẺ: …] trong storyboard. align_srt chỉ giữ phần trước dấu phẩy và bỏ thẻ dài quá 6 từ.
- Đơn vị viết bằng ký hiệu (km, kg, %, °C), số viết theo kiểu Việt (15.000; 2,5).
- Font: Be Vietnam Pro cho mọi chữ trên màn hình (thẻ 800, phụ đề 600). Không dùng font serif hay font trang trí.
- Badge mức chắc chắn tự gắn từ storyboard. Badge là viên nhỏ ở góc trên phải, hiện 3 giây.

## Phụ đề (tuỳ chọn)
- Mặc định bật. Muốn tắt: đặt `"subtitles": false` trong theme.json, hoặc thêm `--no-subs` khi render.
- Mỗi lần hiện 1 dòng, tối đa 42 ký tự, chạy đúng theo thời gian trong srt.
- Chữ lấy từ storyboard nên viết hoa sau dấu chấm, dấu câu và tên riêng đều chuẩn. Tên Latin hiện dạng gốc (Chicxulub), không hiện cách đọc.
- align_srt xuất thêm `audio/subs.clean.srt` để tải lên YouTube làm phụ đề CC.

## Chuyển động máy
- Mỗi cảnh chỉ 1 chuyển động: zoom vào 1,00→1,06, zoom ra 1,06→1,00, hoặc lia ±40-60 px. Cảnh dưới 5 giây chỉ zoom 1,00→1,04.
- Hai cảnh liền nhau phải khác hướng chuyển động. Không zoom quá 1,12.
- Creature chỉ đi bộ hoặc trôi chậm, walk tối đa 200 px.

## Chọn component theo ghi chú trong storyboard
- [size:…] dùng SizeCompare, luôn có người hoặc vật quen thuộc làm thước đo.
- Mốc thời gian dùng GeoClock. Bản đồ hoặc khoảng cách dùng MapDrift, tối đa 3 marker và 2 mũi tên. Ảnh thật dùng PhotoCard. Còn lại dùng KenBurns.
- [THẺ CHẶNG …] dùng TitleCard với `fixed_s: 3`, `transition: "dip"`, kicker "CHẶNG 1".

## Nhịp cảnh
- Thời gian lấy từ srt, không đoán. Cắt cảnh ở đầu câu, mỗi cảnh 1-3 câu.
- 60 giây đầu: cảnh 4-8 giây. Sau đó: 8-20 giây. Không cảnh nào quá 20 giây.
- Ở mốc 25%, 50% và 75%: đổi hẳn loại hình, ví dụ từ paleoart sang bản đồ hoặc ảnh thật.
- Trước cú lật ở phần kết: chèn 1 cảnh tối, `asset` để trống.

## Chuyển cảnh
- Mặc định `fade` (0,4 giây). Sang chặng mới dùng `dip`. Chỉ dùng `cut` khi muốn nhịp giật mạnh ở cold open.
- Cấm: wipe, xoay, zoom-blur, slide.

## Âm thanh
- Giọng đọc lớn hơn nhạc nền 18-20 dB. Nhạc theo khung trong style.md. Không dùng nhạc horror, không jump-scare.

## Tự kiểm trước bản cuối
1. validate_scenes báo OK: tổng thời lượng khớp audio, nhịp cảnh đúng.
2. Mọi bản đồ hiện đại có Hoàng Sa và Trường Sa.
3. Mọi ảnh thật có credit.
4. Không khối chữ nào quá 6 từ.
5. Mở 3 khung hình bất kỳ để kiểm dấu tiếng Việt.
