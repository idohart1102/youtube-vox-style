# Tiêu chuẩn thumbnail — tiensu-vn (rút từ 11 thumbnail viral, 2026-10-27)

## Quy trình
1. Lúc viết kịch bản (write-script): chỉ chốt hook text, hook dự phòng và ý tưởng hình, kèm cảnh hoặc asset nên dùng. Chưa tạo ảnh.
2. Sau khi render (package): lấy asset đã dùng trong video (paleoart, bản đồ, ảnh thật, khung hình đẹp nhất) để ghép thumbnail theo phong cách Vox bên dưới. Nhờ vậy thumbnail luôn khớp với hình trong video.
3. Chỉ khi không có asset nào đạt mục "Hình" thì mới tạo ảnh mới bằng khung prompt AI ở cuối file.

## Phong cách Vox (ghép từ asset)
- Chủ thể chính được tách nền (cutout) và có viền trắng 6-10 px, như hình dán. Đặt chủ thể lên nền giấy tối có texture, hoặc lên khung hình của video đã làm mờ và tối đi.
- Bố cục kiểu collage, tối đa 3 lớp: chủ thể, một yếu tố ngữ cảnh (mảnh bản đồ Việt Nam có Hoàng Sa và Trường Sa, mốc thời gian, ảnh hóa thạch thật kèm ghi nguồn) và chữ.
- Có 1 nét chú thích kiểu Vox: khoanh tròn, gạch chân bằng bút dạ quang, mũi tên mảnh vẽ tay, hoặc khung highlight sau chữ. Chỉ 1 nét, màu accent.
- Bảng màu theo theme.json, chỉ 1 màu nhấn mạnh. Có grain giấy nhẹ.
Chuẩn đối chiếu: Soi Sáng 5,2M; Thế Giới Cổ Đại 2,67M; Máy Thời Gian 2,57M; Curious Fing 1,7M; WUFO 1,2M. Mẫu kém: "Kong Việt Nam" 131K trên kênh 1,56M sub.

## Hook text (ghép bằng Remotion/PIL, KHÔNG để AI vẽ chữ)
- 3-6 từ, 1-2 dòng, VIẾT HOA. Mỗi dòng cao 10-17% khung hình.
- Không lặp lại tiêu đề. Tiêu đề nêu sự thật, hook đặt câu hỏi tiếp theo hoặc lật góc. Ví dụ: tiêu đề "90% khủng long bị tiêu diệt", hook "10% CÒN LẠI ĐÃ ĐI ĐÂU?".
- Ưu tiên 1 trong 4 dạng: câu hỏi có "?", con số gây sốc, đối lập ("THÁI LAN 10+ · VIỆT NAM 0"), hoặc lật niềm tin ("TA ĐÃ HIỂU SAI").
- Font sans đậm (Be Vietnam Pro Black), chữ trắng hoặc vàng #FFD23F, viền đen dày 6-8 px và bóng đổ. Con số hoặc từ khoá tô màu khác. Dấu tiếng Việt phải nét, không vỡ.
- Đặt chữ ở vùng trống đối diện chủ thể. Không che mặt hay mắt của chủ thể. Không đặt chữ ở góc dưới phải (thời lượng video che mất).

## Hình (áp dụng cho cả asset ghép lẫn ảnh AI dự phòng)
- Một khoảnh khắc có chuyện xảy ra: nguy hiểm, hậu quả hoặc bí ẩn. Ví dụ: thiên thạch đang va, kẻ săn mồi đang lao tới, xác khổng lồ, kẻ đang rình. Cấm cảnh tĩnh lặng không có gì xảy ra.
- Một chủ thể chính chiếm 45-65% khung hình, đặt ở 1/3 trái hoặc phải. Mắt, mặt hoặc hàm hướng về người xem hoặc về phía hành động.
- Có vật so sánh kích thước khi được: người nhỏ đứng cạnh sinh vật khổng lồ, hoặc góc máy thấp để sinh vật trông áp đảo.
- Màu: một cặp tương phản (xanh lạnh và cam lửa), hoặc ảnh gần đơn sắc để chữ vàng nổi bật. Không dùng nhiều màu lòe loẹt.
- Giữ phong cách kênh theo theme.json (`art_style_prompt`): Semi-Realistic Paleoart Concept Art, giải phẫu đúng khoa học, ánh sáng điện ảnh, môi trường kiểu matte painting. Nền tối, có grain nhẹ.
- Cấm: cờ hay biểu tượng quốc gia, mặt người thật kiểu meme, mũi tên đỏ rẻ tiền, ảnh báo chí.

## Khung prompt AI dự phòng (EN), chỉ dùng khi không có asset đạt
"Semi-realistic paleoart concept art, scientifically accurate anatomy, cinematic lighting, rich painterly detail, atmospheric depth, matte-painting environment, YouTube thumbnail. [SUBJECT doing ACTION at the moment of DANGER/CONSEQUENCE], placed on the [left/right] third, filling ~55% of frame, [eyes/jaws] facing the viewer. [SCALE CUE: tiny human silhouette / low-angle hero shot]. Setting: [prehistoric place in today's Vietnam, e.g. limestone karst, red-soil plain, mangrove coast]. Lighting: [dramatic rim light / fiery glow vs cold blue shadows], high contrast, dark background #16120e, subtle film grain, slight vignette. Leave the [opposite] side as clean dark negative space for text. Wide 16:9 composition, keep key content inside the central 16:9 area. No text, no letters, no logos, no flags, no watermark."
- Model gpt-image-2.5 cho ảnh 1536x1024 (tỉ lệ 3:2); cắt về 1280x720 trước khi ghép chữ.

## Tự kiểm trước khi xuất
1. Thu nhỏ còn 160x90 px vẫn đọc được hook và nhận ra chủ thể.
2. Hook bổ sung cho tiêu đề, không lặp lại.
3. Có sự kiện hoặc xung đột, không phải cảnh tĩnh.
4. Đúng 1 chủ thể chính. Chữ không che mặt chủ thể.
5. Chữ do hệ thống ghép, dấu tiếng Việt đúng.
