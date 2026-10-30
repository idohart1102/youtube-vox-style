# YouTube Vox System: bản đồ định tuyến
`core/standard/` = tiêu chuẩn chung, đúng với mọi ngôn ngữ. `channels/<slug>/` = riêng của kênh. Đường dẫn tương đối với thư mục gốc.
"Sếp" là người dùng: Sếp gửi audio + srt, duyệt brief, quyết định render lại, đăng YouTube. `<tap>` là `channels/<slug>/episodes/<tap>`.
Quyết định phải tuân theo: `docs/decisions.md`. Phân công AI: `config/ai_roles.yaml`, hướng dẫn: `core/roles/<vai-trò>.md`.

## Ngôn ngữ làm việc
- Trao đổi, báo cáo, hướng dẫn, QA: tiếng Việt.
- Sản phẩm video (kịch bản, tiêu đề, mô tả, tag, chữ thumbnail): ngôn ngữ của kênh, viết như người bản xứ.
- Từ nước ngoài nhắc trong trao đổi luôn có nghĩa tiếng Việt bên cạnh, ví dụ 大量絶滅 (đại tuyệt chủng).

## Việc gì → đọc file nào (chỉ đọc đúng file này)
| Việc | Skill | Đọc |
|---|---|---|
| Xem tiến độ | — | `python core/scripts/status.py` |
| Chọn đề tài | core/skills/plan-topics | backlog.csv, learnings.md của kênh |
| Viết kịch bản | core/skills/write-script | brief.md, channels/<slug>/script/, core/standard/viral-principles.md, accuracy.md |
| Chấm kịch bản | core/roles/reviewer.md | storyboard.md, brief.md, criteria.yaml, qa-checklist.md của kênh |
| Dựng video (đã có audio + srt) | core/skills/build-video | timeline.json (lọc), core/standard/visual.md, core/remotion/README.md |
| Chia cảnh khi chưa có audio | core/skills/build-scenes | storyboard.md, core/remotion/README.md |
| Giọng đọc, render | core/skills/produce | chỉ chạy lệnh, không đọc source |
| QC video | core/roles/qc-video.md | qa/qc_vN.md |
| Meta + thumbnail | core/skills/package | meta.md, timeline.json, core/standard/thumbnail.md, thumbnail.md của kênh |
| Lên Drive, dọn máy | core/skills/publish-clean | chỉ chạy lệnh |
| Học từ số liệu | core/skills/review-stats | stats.json 7 tập gần nhất, knowledge/README.md |

## Luật tiết kiệm token
- Không quét cả repo, không đọc `core/remotion/` (trừ `README.md`) hay `core/scripts/` trừ khi đang sửa lỗi chúng. Không đọc `node_modules/`.
- Không đọc `episodes/*/audio|render|thumb|assets`, trừ `asset_sheet.jpg`.
- Trước khi làm: `python core/scripts/learn.py brief --area <mảng> --channel <slug>`.
- Research: đọc cache trong `channels/<slug>/research/` trước. Chỉ gọi vidIQ khi cache cũ hơn 30 ngày.
- `learnings.md` ≤40 dòng, viết đè. `style.md` ≤60 dòng.

## Lệnh nhanh
- Kiểm tra máy: `python core/scripts/doctor.py --smoke`. Kiểm tra toàn bộ: `python core/tests/run.py`
- Kênh mới: `python core/scripts/new_channel.py <slug> --lang <mã>`. Tập mới: `python core/scripts/new_episode.py <slug> <ten-tap>`
- Xuất lời đọc: `python core/scripts/export_narration.py <tap>`
- Khớp srt: `python core/scripts/align_srt.py <tap>`, thêm `--apply` sau khi viết scenes.json
- Asset, tự QC tối đa 5 lần: `python core/scripts/gen_assets.py <tap>` (`--redo id1,id2`, `--only ai|real`, `--codex`)
- Rig nhân vật: `python core/scripts/rig_auto.py <tap> <file> --plan biped|quad`
- Kiểm tra cảnh: `python core/scripts/validate_scenes.py <tap>/scenes.json`
- Render và kiểm tra máy: `python core/scripts/produce.py <tap>`. QC độc lập: `python core/scripts/qc_video.py <tap>`
- Thumbnail: `node core/scripts/thumb.mjs <tap> <spec.json>`
- Tiến độ: `python core/scripts/status.py <tap> stage=<bước>`
- Lên Drive, dọn máy: `python core/scripts/publish_clean.py <tap> --dry-run`, bỏ `--dry-run` khi đã có `final=ok`. Hết hạn gói nguồn: `publish_clean.py --expire`
