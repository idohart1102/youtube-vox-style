# QA kịch bản — kodai-jp (chấm storyboard.md sau khi viết; dưới 90 điểm phải sửa, tối đa 3 vòng)
Mỗi dòng 5 điểm. Ghi kết quả ở dòng cuối storyboard.md dạng "# QA: 9,5/10 (95/100), lỗi: …" (phần lỗi viết tiếng Việt). Báo điểm cho Sếp theo thang 10.

## Giữ chân (55)
1. Câu đầu (0-5 giây) là cảnh nhập vai hoặc nghịch lý có số, không chào hỏi, không giới thiệu kênh.
2. Trước giây 20 có tiền cược (「実際に起きたことです」) và 2-3 câu hỏi.
3. Trước giây 45 có lời hứa (「この動画の最後で…」) và hé 1 chi tiết sẽ đến sau. 60 giây đầu khớp lời hứa của tiêu đề và thumbnail.
4. Lộ trình 3 chương ở giây 45-60; không kêu gọi đăng ký ở đầu video.
5. Mỗi nhịp 60-90 giây theo công thức: so sánh → số → 「ですが」 → bằng chứng → câu bắc cầu.
6. Có re-hook ở các mốc 25%, 50%, 75%; không đoạn nào quá 120 giây mà không mở vòng tò mò mới.
7. Chi tiết hay nhất nằm ở 1/3 cuối; mỗi chương mạnh hơn chương trước.
8. Đoạn 「その時、日本列島は？」 được cài từ cold open và trả thưởng ở mốc 60-80%.
9. Kết dưới 60 giây: cú lật, nối với hôm nay, 「地球は、すべてを覚えています。」 đúng 1 lần, 1 câu hỏi bình luận, nhắc đăng ký nhẹ đúng 1 lần, chỉ sang video sau.
10. Khoảng 1 con số hoặc 1 so sánh mỗi 10 giây, so sánh quen thuộc với người Nhật; số lớn được quy đổi ra trải nghiệm thật.
11. Ghi chú hình [ ] đổi mỗi 4-8 giây ở 60 giây đầu, không quá 20 giây sau đó.

## Giọng tiếng Nhật (25)
12. Thể です/ます xuyên suốt, có 体言止め và câu cực ngắn để nhấn; tiếng Nhật tự nhiên như người bản xứ viết, không có dấu vết dịch máy.
13. Ngôi đúng: 「あなた」 khi nhập vai, 「私たち」 khi suy luận; dùng 「この動画」「第◯章」; không 「僕」「俺」「エピソード」.
14. Không có câu cấm (衝撃, ヤバい, 閲覧注意, 最恐, lời chào); 「〜と言われています」 luôn có nguồn.
15. Câu ≤40 ký tự, tối đa 2 dấu 「、」; nhịp ngắt bằng dòng trống dùng tiết chế (khoảng 1 lần mỗi 30-60 giây).
16. An toàn cho giọng AI theo core/lang/ja.md: từ dễ đọc sai đã có 《cách đọc》 hoặc nằm trong core/lang/ja-readings.tsv; tên loài bằng katakana; không chữ Latin, không ký hiệu lạ trong lời đọc.

## Chính xác (20)
17. Mọi con số có nguồn trong brief hoặc sources.md; năm phát hiện, địa điểm, tên người khớp nguồn.
18. Badge 確定 / 有力 / 議論中 khớp lời đọc (「わかっています」「考えられています」「決着はついていません」).
19. Tên loài, địa danh, bảo tàng Nhật viết đúng chuẩn tiếng Nhật chính thức (ví dụ カムイサウルス・ジャポニクス, むかわ町).
20. Ảnh thật chỉ lấy từ nguồn được phép, kèm dòng ghi nguồn; không chính trị, không tranh chấp lãnh thổ.
