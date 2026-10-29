# Remotion – tham chiếu component (build-scenes chỉ cần đọc file này, không đọc source)

Khung 1920x1080. Toạ độ x,y theo pixel. `asset` là đường dẫn trong assets/, ví dụ `backgrounds/forest.jpg`.
Ví dụ đầy đủ: core/templates/scenes.example.json

| component | asset | props |
|---|---|---|
| KenBurns | ảnh nền | z0,z1 (zoom), x0,x1,y0,y1 (pan px), filter, label, sub |
| TitleCard | ảnh nền (tối đi) | kicker, title, sub |
| Parallax | ảnh nền AI | cam (in, out, left, right), layers:[{asset (cutout PNG), x, y (giữa-đáy px), h (cao px), depth (0 xa..1 gần), at_s, enter (pop, rise, fade), sticker (mặc định true), flip, drift (px)}], label, sub |
| Collage | ảnh nền (làm tối) hoặc trống | items (≤3):[{asset, x, y (tâm), w (rộng px), rot (độ), at_s, photo (ảnh thật: viền trắng + credit), credit}], label, sub |
| GeoMap | không cần | center:[lon,lat], scale (2200 = Việt Nam, 260 = thế giới), cam (in, out), highlight:[mã ISO số, "704" = VN], markers (≤3):[{lon,lat,label,at_s}], arrows (≤2):[{from:[lon,lat], to:[lon,lat], at_s}] |
| SizeCompare | ảnh nền | title, items:[{name, size_m, label, cutout}] (cutout: PNG nhìn ngang, rộng ảnh = size_m; người: name "human", size_m = chiều cao) |
| GeoClock | ảnh nền | from_ma, to_ma (triệu năm trước), label, sub |
| MapDrift | ảnh bản đồ cổ (ảnh thật) | markers:[{x,y (0..1), label}], arrows:[{from:[x,y], to:[x,y]}], label, sub |
| PhotoCard | ảnh thật | credit (bắt buộc), label, sub, z (zoom cuối, mặc định 1.03) |

Mọi cảnh có thể thêm: `transition` ("fade" mặc định, "dip" khi sang chặng, "cut"), `props.recon: true` (thẻ "Tái hiện"),
`props.cards: [{text, at_s, dur_s}]` (thẻ keyword ≤6 từ), `props.badges: [{type: xac-nhan|co-the|tranh-cai, at_s}]`,
`props.annotate: [{type: circle|arrow|underline|highlight, x, y, w, h | from:[x,y], to:[x,y], at_s, color}]` (nét bút khoanh, mũi tên kiểu Vox).
Dựng từ srt: ghi `lines: [đầu, cuối]` thay cho `duration_s`, `fixed_s` cho TitleCard; `align_srt.py --apply` tự tính thời gian, thẻ và badge.
Chữ cố định trong component theo `theme.lang` (vi, ja). Phụ đề 1 dòng lấy từ timeline.json; tắt bằng theme.subtitles=false hoặc --no-subs.

Không có timeline.json: `narration` của cảnh hiện làm phụ đề nếu theme.subtitles khác false.

Hình minh hoạ là ảnh (gen_assets.py), không vẽ SVG. Creature và thư viện SVG trong registry.tsx chỉ giữ cho tập cũ, validate_scenes báo lỗi nếu dùng.
GeoMap luôn vẽ quần đảo Hoàng Sa, Trường Sa và nhãn Biển Đông khi nằm trong khung.

Render: `node core/scripts/render.mjs <tập>` (bản đầy đủ) hoặc thêm `--preview` (mỗi cảnh 2 giây, nửa độ phân giải, không âm thanh).
Asset: `python core/scripts/gen_assets.py <tập>` theo asset_plan.json (mẫu core/templates/asset_plan.example.json).
