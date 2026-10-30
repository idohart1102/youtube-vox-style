---
name: plan-topics
description: Chọn đề tài tiếp theo cho một kênh và viết brief.md. Dùng khi cần tập mới.
---
1. Đọc `channels/<slug>/backlog.csv` (chỉ các dòng status=todo) và `learnings.md`.
2. Chọn đề tài có score cao nhất. Không chọn trùng trụ cột với 2 tập gần nhất, trừ khi learnings.md nói trụ cột đó đang thắng.
3. Chạy `python core/scripts/new_episode.py <slug> <ten-ngan>` rồi điền brief.md (≤15 dòng).
4. Đổi status của đề tài trong backlog.csv thành `doing`.
Không chọn nhân vật chính đã có trong `no_repeat_species` video gần nhất (`species` trong status.yaml). Chỉ khi backlog còn dưới 10 dòng todo mới mở `channels/<slug>/research/` (cache) để bổ sung. Gọi vidIQ chỉ khi cache cũ hơn 30 ngày, kết quả lưu vào `channels/<slug>/research/` có ngày.
