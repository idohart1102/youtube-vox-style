# Luật tiếng Nhật (ja) cho kịch bản và giọng AI (v2, 2026-10-30)
Trao đổi với Sếp bằng tiếng Việt. Sản phẩm (lời đọc, tiêu đề, mô tả, tag, chữ thumbnail) bằng tiếng Nhật native.
Khi nhắc từ khóa tiếng Nhật trong trao đổi hoặc báo cáo, luôn ghi nghĩa tiếng Việt bên cạnh: 化石 (hóa thạch).

## Hai bản chữ
- storyboard.md viết tiếng Nhật tự nhiên (kanji + kana + số Ả Rập), dùng làm phụ đề và chữ trên màn hình.
- script.md (bản dán vào giọng AI) KHÔNG viết tay: `export_narration.py` tự đổi sang chữ an toàn: lấy cách đọc trong 《》, tra từ điển `script/readings.tsv`, đổi số và đơn vị sang kana.
- Tốc độ: khoảng 300 ký tự ≈ 1 phút (đếm ký tự lời đọc, không đếm dấu câu và khoảng trắng).

## Viết sao cho giọng AI không đọc sai
- Từ có nhiều cách đọc hoặc hiếm gặp: ghi cách đọc ngay sau bằng 《》 kiểu ruby: 上手《かみて》, 穂別《ほべつ》. Phụ đề vẫn hiện kanji, giọng đọc dùng phần trong 《》.
- Từ lặp lại nhiều video (tên kỷ, địa danh, thuật ngữ) thì thêm vào `script/readings.tsv` một lần, khỏi ghi 《》 nữa.
- Tên loài và tên người nước ngoài: viết katakana theo cách gọi chính thức ở Nhật (ティラノサウルス, フタバスズキリュウ). Không viết chữ Latin trong lời đọc; tên khoa học nếu cần thì để trong ghi chú [ ].
- Số: viết số Ả Rập kèm 万/億 (6600万年前, 2億5200万年前, 12メートル, 2.5倍). Script tự đổi sang kana. Không viết số kanji kiểu 六千六百万.
- Đơn vị script hiểu: メートル, キロメートル, センチ, トン, キログラム, ℃, %, km, m, kg, cm, t. Viết sát sau số.
- Lượng từ đọc biến âm (匹, 本, 人, 分, 階, 頭…) đi với số: ghi cả cụm bằng 《》: 3匹《さんびき》, 1人《ひとり》.
- Không dùng ký hiệu lạ trong lời đọc: 〜, ※, emoji, ・ giữa câu, ngoặc 「」 lồng nhau. Dấu chấm lửng dùng 「…」, tối đa 1 lần mỗi đoạn.
- Không quá 2 dấu 「、」 mỗi câu. Câu ≤40 ký tự. Một ý một câu.
- Ngắt nghỉ: không chèn ký hiệu ngắt. Chỗ cần dừng lâu (sau hook, trước cú lật, sau câu chốt) để 1 dòng trống trong storyboard, khoảng 1 lần mỗi 30-60 giây.

## Văn phong mặc định
- です/ます, xen 体言止め để nhấn, trừ khi style.md của kênh quy định khác.
- Tiếng Nhật phải đọc lên như người bản xứ viết: không cấu trúc dịch từ tiếng Anh hay tiếng Việt, không lạm dụng 「〜という」「〜することができます」.
