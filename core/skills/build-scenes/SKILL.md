---
name: build-scenes
description: Chuyển storyboard.md thành scenes.json cho Remotion, chọn asset theo tag.
---
1. Đọc storyboard.md (bản có ghi chú hình) và bảng component trong `core/remotion/README.md` (không đọc source .tsx).
2. Liệt kê asset cần có vào `asset_plan.json`, không mở ảnh.
3. Mỗi đoạn lời đọc tương ứng 1 cảnh dài 4–8 giây. Ghi chú [ ] quyết định component: size→SizeCompare, map→MapDrift, time→GeoClock, còn lại là KenBurns.
4. Asset còn thiếu thì ghi vào `missing_assets.md` của tập, không tự vẽ trong bước này.
5. Chạy `python core/scripts/validate_scenes.py <tập>/scenes.json` cho tới khi ra OK.
