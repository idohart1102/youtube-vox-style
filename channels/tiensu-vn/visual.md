# Quy định dựng hình — Tiền Sử Đất Việt (Sếp duyệt 2026-10-28)
Đọc cùng theme.json (màu, font) và thumbnail.md. Mục tiêu: cuốn như phim tài liệu, chính xác như sách giáo khoa, gọn gàng kiểu Vox. Kênh tiếng Việt: mọi chữ trên màn hình là tiếng Việt.

## Phong cách hình (kiểu Vox: ảnh thật + paleoart cắt lớp, chuyển động bằng Remotion)
- Mọi hình minh hoạ là ảnh, không vẽ SVG. Ảnh AI tạo bằng gpt-image-2.5 qua 9router theo `art_style_prompt` của theme.json: Semi-Realistic Paleoart Concept Art, giải phẫu đúng, ánh sáng điện ảnh. Trong ảnh không có chữ.
- Cảnh tái hiện dựng bằng Parallax: 1 ảnh nền không có nhân vật + 1-3 cutout PNG (sinh vật, thiên thạch, cây) có viền trắng sticker. Lớp gần trôi nhanh hơn lớp xa. Đặt `props.recon: true` để hiện thẻ "Tái hiện".
- Ảnh thật (hóa thạch, lớp đất, hang, hình khoa học) do gen_assets tìm, chỉ nhận CC0, public domain, CC BY, CC BY-SA. Dùng PhotoCard hoặc Collage (`photo: true`), giữ màu gốc, `credit` tự điền, hiện ít nhất 4 giây. Không bao giờ dùng ảnh AI thay ảnh thật.
- Bản đồ hiện đại dùng GeoMap (dữ liệu thật, tự có Hoàng Sa, Trường Sa, Biển Đông). Bản đồ cổ dùng ảnh thật PALEOMAP trong MapDrift, chấm Việt Nam ngày nay màu vàng #FFD23F.
- Mỗi cảnh chỉ 1 màu nhấn. Dùng danger cho thảm họa, jade cho sự sống hồi phục. Grain 0,3 và vignette 0,4 cho cả video, không thêm bộ lọc khác.
- Cùng một loài thì dùng cùng thẻ `species` trong asset_plan để trông nhất quán cả tập.

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
- Mỗi lần hiện 1 dòng, tối đa 42 ký tự, chạy đúng theo thời gian trong srt. Chữ trắng, không có màu nền, chỉ viền tối mảnh để đọc được trên ảnh sáng.
- Chữ lấy từ storyboard nên viết hoa sau dấu chấm, dấu câu và tên riêng đều chuẩn. Tên Latin hiện dạng gốc (Chicxulub), không hiện cách đọc.
- align_srt xuất thêm `audio/subs.clean.srt` để tải lên YouTube làm phụ đề CC.

## Chuyển động máy
- Mỗi cảnh chỉ 1 chuyển động: Parallax `cam` in, out, left, right; KenBurns zoom 1,00→1,06 hoặc lia ±40-60 px. Cảnh dưới 5 giây chỉ zoom 1,00→1,04.
- Hai cảnh liền nhau phải khác hướng chuyển động. Không zoom quá 1,08 (ảnh AI gốc nhỏ hơn khung 1080p).
- Cutout xuất hiện bằng pop hoặc rise, lệch nhau 0,5-1 giây. Trôi ngang (`drift`) tối đa 200 px.
- Chừa dải phụ đề: chân cutout `y` ≤ 900, ảnh trong Collage không xuống dưới y 920.
- Nét bút `annotate` (khoanh, mũi tên, gạch chân) để chỉ vào chi tiết đang nói tới, tối đa 2 nét mỗi cảnh.

## Chọn component theo ghi chú trong storyboard
- Cảnh tái hiện sinh vật, thảm họa, môi trường cổ: Parallax.
- Bằng chứng, so sánh 2-3 thứ, "trước và sau": Collage (ảnh thật + cutout), thêm `annotate` khoanh chỗ cần nhìn.
- Hiện vật thật cần nhìn rõ: PhotoCard.
- [size:…] dùng SizeCompare với cutout, luôn có người hoặc vật quen thuộc làm thước đo.
- Mốc thời gian dùng GeoClock. Bản đồ hiện đại, khoảng cách: GeoMap, tối đa 3 marker và 2 mũi tên. Bản đồ cổ: MapDrift.
- [THẺ PHẦN …] dùng TitleCard với `fixed_s: 3`, `transition: "dip"`, kicker "PHẦN 1".
- Không dùng Creature (hình SVG).

## Nhịp cảnh
- Thời gian lấy từ srt, không đoán. Cắt cảnh ở đầu câu, mỗi cảnh 1-3 câu.
- 60 giây đầu: cảnh 4-8 giây. Sau đó: 8-20 giây. Không cảnh nào quá 20 giây.
- Ở mốc 25%, 50% và 75%: đổi hẳn loại hình, ví dụ từ paleoart sang bản đồ hoặc ảnh thật.
- Trước cú lật ở phần kết: chèn 1 cảnh tối, `asset` để trống.

## Chuyển cảnh
- Mặc định `fade` (0,4 giây). Sang phần mới dùng `dip`. Chỉ dùng `cut` khi muốn nhịp giật mạnh ở cold open.
- Cấm: wipe, xoay, zoom-blur, slide.

## Âm thanh
- Giọng đọc lớn hơn nhạc nền 18-20 dB. Nhạc theo khung trong style.md. Không dùng nhạc horror, không jump-scare.

## Tự kiểm trước bản cuối
1. validate_scenes báo OK: tổng thời lượng khớp audio, nhịp cảnh đúng.
2. Mọi bản đồ hiện đại là GeoMap (có Hoàng Sa, Trường Sa).
3. Mọi ảnh thật có credit, meta.md có mục "Nguồn ảnh".
4. Không khối chữ nào quá 6 từ.
5. Mở asset_sheet.jpg và 3 khung hình bất kỳ: giải phẫu đúng, không chữ rác trong ảnh, dấu tiếng Việt đúng.
