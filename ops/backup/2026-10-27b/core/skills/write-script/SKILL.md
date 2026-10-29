---
name: write-script
description: Viết script.md cho một tập theo phong cách kênh, dùng cho mọi ngôn ngữ. Đây là bước duy nhất dùng model mạnh.
---
Đọc đúng những file sau, không đọc thêm:
1. `brief.md` của tập.
2. `channels/<slug>/channel.yaml`, chỉ để lấy `language`, `length_min`, `words_per_min`.
3. `core/lang/<language>.md`: luật ngôn ngữ, tốc độ đọc, cách viết cho TTS.
4. `channels/<slug>/style.md`: giọng kể, khung tập, điều cấm. File này thắng nếu mâu thuẫn với skill.
5. Một file trong `channels/<slug>/examples/`, ưu tiên file bắt đầu bằng `01-`.
6. `channels/<slug>/sources.md`, nếu có.

Quy tắc chung cho mọi kênh:
- Độ dài lấy từ `length_min` nhân `words_per_min`. Nếu kênh không có `words_per_min`, dùng tốc độ trong file lang.
- 60 giây đầu phải có cái móc, lời hứa và cảm giác cụ thể. Cứ 90-120 giây mở một vòng tò mò mới.
- Ghi chú hình trong [ ] ngay trong lời đọc, ví dụ [size:dunkleosteus-vs-human]. Badge mức chắc chắn cũng ghi trong [ ] nếu style.md yêu cầu.
- Chỉ dùng sự thật có nguồn khoa học (brief hoặc sources.md). Không suy đoán gây sốc sai sự thật.

Sau khi viết xong:
- Nếu có `channels/<slug>/qa-checklist.md`, tự chấm script theo checklist đó. Dưới ngưỡng thì sửa rồi chấm lại, tối đa 2 lần.
- Ghi dòng kết quả QA ở cuối script.md.
Viết thẳng vào script.md, không giải thích lại cho người dùng.
