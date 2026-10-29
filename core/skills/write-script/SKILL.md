---
name: write-script
description: Viết storyboard.md, script.md và meta.md cho một tập theo phong cách kênh, dùng cho mọi ngôn ngữ. Đây là bước duy nhất dùng model mạnh.
---
Đọc đúng những file sau, không đọc thêm:
1. `brief.md` của tập.
2. `channels/<slug>/channel.yaml`: chỉ lấy `language`, `length_min`, `words_per_min`, `seo` (nếu có).
3. `core/lang/<language>.md`: luật ngôn ngữ, tốc độ đọc, cách viết cho TTS.
4. `channels/<slug>/style.md`: giọng kể, khung tập, tiêu đề, thumbnail, điều cấm. Nếu mâu thuẫn với skill, style.md thắng.
5. Một file trong `channels/<slug>/examples/`, ưu tiên file bắt đầu bằng `01-`.
6. `channels/<slug>/sources.md`, nếu có.
7. `channels/<slug>/theme.json`: chỉ lấy `art_style` và `palette`, để viết prompt thumbnail.

Quy tắc chung cho mọi kênh:
- Độ dài lấy từ `length_min` nhân `words_per_min`. Nếu kênh không có `words_per_min`, dùng tốc độ trong file lang.
- 60 giây đầu phải có cái móc, lời hứa và cảm giác cụ thể. Cứ 90-120 giây mở một vòng tò mò mới.
- Ghi chú hình trong [ ] ngay trong lời đọc, ví dụ [size:dunkleosteus-vs-human]. Badge mức chắc chắn cũng ghi trong [ ] nếu style.md yêu cầu. [THẺ: …] chỉ là keyword hoặc số liệu, tối đa 6 từ (xem visual.md của kênh nếu có).
- Câu hỏi có đáp án ở phía sau: ghi `[HỎI: q1]` ngay trước câu hỏi và `[ĐÁP: q1]` ngay trước câu trả lời (q1, q2… theo thứ tự). Ghi chú hình cho câu hỏi chỉ tả sự bí ẩn (bóng đen, sương, một chi tiết), không tả đáp án.
- Chỉ dùng sự thật có nguồn khoa học (brief hoặc sources.md). Không suy đoán gây sốc sai sự thật.

## Đầu ra: 3 file trong thư mục tập, đủ 5 phần
**storyboard.md** (bản làm việc, cho chia cảnh, chapter và QA)
1. Tiêu đề video, ở dòng đầu dạng `# <tiêu đề>`. Tiêu đề phải đúng nguyên văn tên tập trong backlog hoặc brief, không tự đổi.
2. Toàn bộ kịch bản: các heading `##` theo khung tập (heading cũng là chapter), lời đọc và ghi chú [ ]. Không có HTML comment.
Cuối file ghi dòng `# QA: <điểm>/10 (<điểm>/100), lỗi: …`.

**script.md** (chỉ lời thuyết minh, Sếp dán thẳng vào AI tạo giọng)
- Không viết tay. Sau khi storyboard.md đã qua QA, chạy `python core/scripts/export_narration.py <tập>`. Script này bỏ tiêu đề, heading, ghi chú [ ] và dòng QA. Mỗi phần thành một đoạn; trong đoạn chỉ xuống dòng ở chỗ storyboard có dòng trống (ngắt nghỉ dài, xem core/lang/vi.md). Không có ký hiệu nào ngoài lời đọc.
- Sửa lời đọc thì sửa ở storyboard.md rồi xuất lại; không sửa trực tiếp script.md.

**meta.md** (theo `core/templates/meta.md`)
3. Mô tả chuẩn SEO, khoảng 200-350 từ:
   - Có ít nhất 3 từ khoá chính, mỗi từ khoá xuất hiện ít nhất 3 lần và đọc tự nhiên, không nhồi. 2 dòng đầu phải chứa từ khoá quan trọng nhất và cái móc của tập.
   - Có chỗ chừa sẵn cho chapters, có phần "Nguồn tham khảo và ảnh" ghi đủ tác giả và giấy phép theo sources.md.
   - Kết bằng đúng 3 hashtag phổ biến. YouTube hiện 3 hashtag đầu trên tiêu đề, nên đặt hashtag mạnh nhất trước.
   - Từ khoá và hashtag lấy từ `seo` trong channel.yaml cộng 1-2 từ khoá riêng của tập. Chỉ gọi vidIQ khi cache trong `research/` cũ hơn 30 ngày.
4. Thẻ tag: đúng 5 tag, xếp từ rộng đến hẹp. Tag 1 là từ khoá chính của tập.
5. Thumbnail (chỉ ý tưởng, chưa tạo ảnh; ảnh được ghép sau khi render ở bước package). Nếu có `channels/<slug>/thumbnail.md` thì theo đúng file đó. Gồm:
   - Hook text 3-6 từ, bổ sung cho tiêu đề chứ không lặp lại (câu hỏi, con số, đối lập hoặc lật niềm tin), kèm 1 phương án dự phòng.
   - Ý tưởng hình: khoảnh khắc nguy hiểm, hậu quả hoặc bí ẩn, 1 chủ thể chính, vật so kích thước, và cảnh hoặc ghi chú [ ] trong storyboard nên lấy asset.
   - Chữ do hệ thống ghép, không bao giờ để AI vẽ chữ.

Sau khi viết xong:
- Nếu có `channels/<slug>/qa-checklist.md`, tự chấm storyboard.md theo checklist đó, thang 10. Dưới ngưỡng thì sửa rồi chấm lại, tổng cộng tối đa 3 vòng.
- Tự kiểm meta.md: đủ 5 phần, mỗi từ khoá chính xuất hiện ≥3 lần, đúng 3 hashtag, đúng 5 tag, tiêu đề trùng tên tập.
Viết thẳng vào các file, không giải thích lại cho người dùng.
