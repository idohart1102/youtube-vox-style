# YouTube Vox System — bản đồ định tuyến

Hệ thống sản xuất video thuyết minh + minh họa (Remotion) cho nhiều kênh.
`core/` = máy dùng chung. `channels/<slug>/` = hồn từng kênh. Đường dẫn luôn tương đối với thư mục gốc này.

## Việc gì → đọc file nào (chỉ đọc đúng file này)
| Việc | Skill | Đọc |
|---|---|---|
| Chọn đề tài | core/skills/plan-topics | channels/<slug>/backlog.csv, learnings.md |
| Viết kịch bản | core/skills/write-script | xem danh sách trong SKILL.md (brief, lang, style, 1 example, sources) |
| QA kịch bản (sau khi viết) | — | storyboard.md, channels/<slug>/qa-checklist.md (nếu kênh có) |
| Chia cảnh | core/skills/build-scenes | storyboard.md, core/remotion/README.md, assets/index.json (lọc theo tag) |
| Dựng video từ audio + srt của Sếp (tự tạo ảnh AI, tìm ảnh thật) | core/skills/build-video | timeline.json (lọc), channels/<slug>/visual.md, core/remotion/README.md, assets/index.json (lọc) |
| Giọng đọc, phụ đề, render | core/skills/produce | chỉ chạy lệnh, KHÔNG đọc source |
| Tiêu đề, mô tả, thumbnail | core/skills/package | brief.md, phần "Tiêu đề" của style.md |
| Học từ số liệu (hằng tuần) | core/skills/review-stats | stats.json của 7 tập gần nhất |

## Luật tiết kiệm token
- Không quét cả repo, không đọc `core/remotion/` hay `core/scripts/` trừ khi đang sửa lỗi chúng.
- Không đọc `episodes/*/audio|render|thumb`. Không mở ảnh trong `assets/`, dùng `assets/index.json`.
- Research vidIQ: đọc cache trong `research/` trước. Chỉ gọi vidIQ khi cache cũ hơn 30 ngày.
- `learnings.md` ≤40 dòng, viết đè không nối thêm. `style.md` ≤60 dòng.

## Lệnh nhanh
- Kênh mới: `python core/scripts/new_channel.py <slug>`
- Tập mới: `python core/scripts/new_episode.py <slug> <ten-tap>`
- Kiểm tra cảnh: `python core/scripts/validate_scenes.py channels/<slug>/episodes/<tap>/scenes.json`
- Asset ảnh: `python core/scripts/gen_assets.py <tập>` (ảnh AI qua 9router, ảnh thật có giấy phép mở). Nền vẽ tay painter.py chỉ để thử.
- Chạy cả pipeline (thêm `--preview` để xem nhanh): `python core/scripts/produce.py channels/<slug>/episodes/<tap>`
