# YouTube Vox System — bản đồ định tuyến

Hệ thống sản xuất video thuyết minh + minh họa (Remotion) cho nhiều kênh.
`core/` = máy dùng chung. `channels/<slug>/` = hồn từng kênh. Đường dẫn luôn tương đối với thư mục gốc này.
"Sếp" là người dùng: Sếp gửi audio + srt và duyệt kết quả. `<tap>` luôn là đường dẫn đầy đủ `channels/<slug>/episodes/<tap>`.

## Việc gì → đọc file nào (chỉ đọc đúng file này)
| Việc | Skill | Đọc |
|---|---|---|
| Chọn đề tài | core/skills/plan-topics | channels/<slug>/backlog.csv, learnings.md |
| Viết kịch bản | core/skills/write-script | brief.md, channel.yaml (vài khóa), core/lang/<lang>.md, style.md, 1 example, sources.md, theme.json (xem SKILL.md) |
| QA kịch bản (sau khi viết) | — | storyboard.md, channels/<slug>/qa-checklist.md (nếu kênh có) |
| Chia cảnh khi CHƯA có audio | core/skills/build-scenes | storyboard.md, core/remotion/README.md, assets/index.json (lọc theo tag) |
| Dựng video khi Sếp đã gửi audio + srt (tự tạo ảnh AI, tìm ảnh thật) | core/skills/build-video | timeline.json (lọc), channels/<slug>/visual.md, core/remotion/README.md, assets/index.json (lọc) |
| Giọng đọc, phụ đề, render | core/skills/produce | chỉ chạy lệnh, KHÔNG đọc source |
| Hoàn thiện meta + thumbnail (sau render) | core/skills/package | meta.md, storyboard.md, scenes.json, channels/<slug>/thumbnail.md, phần "Tiêu đề" + "Thumbnail" của style.md (brief.md chỉ khi meta.md trống) |
| Học từ số liệu (hằng tuần) | core/skills/review-stats | stats.json của 7 tập gần nhất |

File kênh không bắt buộc: `visual.md`, `thumbnail.md`, `sources.md`, `qa-checklist.md` (hiện chỉ tiensu-vn có). Kênh thiếu file thì bỏ qua bước đó và báo Sếp, không tự bịa luật.
`stats.json` chưa có script nào tạo: chưa có thì báo Sếp, không chạy review-stats.

## Luật tiết kiệm token
- Không quét cả repo, không đọc `core/remotion/` (trừ `README.md`) hay `core/scripts/` trừ khi đang sửa lỗi chúng.
- Không đọc `paleo-video/`, `node_modules/`, `ops/backup/` (bản cũ, kể cả các CLAUDE.md trong đó).
- Không đọc `episodes/*/audio|render|thumb`. Không mở ảnh trong `assets/`, dùng `assets/index.json`.
- Research vidIQ: đọc cache trong `research/` trước. Chỉ gọi vidIQ khi cache cũ hơn 30 ngày.
- `learnings.md` ≤40 dòng, viết đè không nối thêm. `style.md` ≤60 dòng.

## Lệnh nhanh
- Kiểm tra máy mới: `python core/scripts/doctor.py`
- Kênh mới: `python core/scripts/new_channel.py <slug>`
- Tập mới: `python core/scripts/new_episode.py <slug> <ten-tap>`
- Xuất lời đọc (tạo script.md từ storyboard.md): `python core/scripts/export_narration.py <tap>`
- Khớp srt: `python core/scripts/align_srt.py <tap>` (tạo timeline.json), thêm `--apply` sau khi viết scenes.json
- Asset ảnh: `python core/scripts/gen_assets.py <tap>` (ảnh AI qua 9router, ảnh thật có giấy phép mở; `--redo id1,id2`, `--only ai|real`, `--codex`). Nền vẽ tay painter.py chỉ để thử.
- Kiểm tra cảnh: `python core/scripts/validate_scenes.py <tap>/scenes.json`
- Chạy cả pipeline (thêm `--preview` để xem nhanh, `--no-subs` để tắt phụ đề): `python core/scripts/produce.py <tap>`
