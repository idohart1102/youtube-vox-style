# Remotion – tham chiếu component (build-scenes chỉ cần đọc file này, không đọc source)

Khung 1920x1080. Toạ độ x,y theo pixel. `asset` là đường dẫn trong assets/, ví dụ `backgrounds/forest.jpg`.
Ví dụ đầy đủ: core/templates/scenes.example.json

| component | asset | props |
|---|---|---|
| KenBurns | ảnh nền | z0,z1 (zoom), x0,x1,y0,y1 (pan px), filter, label, sub |
| TitleCard | ảnh nền (tối đi) | kicker, title, sub |
| Creature | ảnh nền | name (xem bên dưới), x (tâm), y (chân chạm, ~940), scale, flip, walk (px), label, sub, bg{…KenBurns} |
| SizeCompare | ảnh nền | title, items:[{name, size_m, label}] (người: name "human", size_m = chiều cao) |
| GeoClock | ảnh nền | from_ma, to_ma (triệu năm trước), label, sub |
| MapDrift | ảnh bản đồ | markers:[{x,y (0..1), label}], arrows:[{from:[x,y], to:[x,y]}], label, sub |
| PhotoCard | ảnh thật | credit (bắt buộc), label, sub, z (zoom cuối, mặc định 1.03) |

Mọi cảnh có thể thêm: `transition` ("fade" mặc định, "dip" khi sang chặng, "cut"), `props.recon: true` (thẻ "Tái hiện"),
`props.cards: [{text, at_s, dur_s}]` (thẻ keyword ≤6 từ), `props.badges: [{type: xac-nhan|co-the|tranh-cai, at_s}]`.
Dựng từ srt: ghi `lines: [đầu, cuối]` thay cho `duration_s`, `fixed_s` cho TitleCard; `align_srt.py --apply` tự tính thời gian, thẻ và badge.
Chữ cố định trong component theo `theme.lang` (vi, ja). Phụ đề 1 dòng lấy từ timeline.json; tắt bằng theme.subtitles=false hoặc --no-subs.

Không có timeline.json: `narration` của cảnh hiện làm phụ đề nếu theme.subtitles khác false.

Sinh vật có sẵn (components/registry.tsx): trex, mammal, turtle, bird, pterosaur, sauropod, triceratops, stegosaurus, asteroid, earth, fish_fossil, skull_fossil, fern, conifer, cycad, human.
Tên chưa có thì vẽ khối tạm. Thêm sinh vật: vẽ SVG trong lib/ rồi đăng ký 1 dòng ở registry.tsx.

Render: `node core/scripts/render.mjs <tập>` (bản đầy đủ) hoặc thêm `--preview` (mỗi cảnh 2 giây, nửa độ phân giải, không âm thanh).
Nền vẽ tay: `python core/scripts/painter.py` (tạo vào assets/backgrounds) rồi `python core/scripts/assets_index.py`.
