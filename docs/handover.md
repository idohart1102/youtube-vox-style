# Bàn giao: cần gì để vận hành trên máy khác
Không ghi mật khẩu hay khóa vào repo. Khóa nằm trong `.env`, mật khẩu nằm trong trình quản lý mật khẩu của chủ kênh.

## Cài đặt
1. Cài Git, Git LFS, Node 22, Python 3.12, FFmpeg. macOS: `brew install git git-lfs node@22 python@3.12 ffmpeg`.
2. `git lfs install && git clone <repo> && cd <repo> && git lfs pull`.
3. macOS/Linux: `bash setup.sh`. Windows: `powershell -ExecutionPolicy Bypass -File setup.ps1`.
4. Điền `.env`, sửa `config/machine.yaml`.
5. `.venv/bin/python core/scripts/doctor.py --smoke` (Windows: `.\.venv\Scripts\python core\scripts\doctor.py --smoke`). Ra `ALL OK` là đạt. Dòng `!` là dịch vụ chưa sẵn sàng.

## Dịch vụ
| Dịch vụ | Để làm gì | Thiết lập | Nếu không có |
|---|---|---|---|
| Claude Code | Vai trò chính, đọc `CLAUDE.md` | Đăng nhập tài khoản được giao | Codex đọc `AGENTS.md` |
| 9router | Tạo ảnh, chấm, tìm ảnh | Chạy trên máy, khai `router_url`; khóa ở `NINEROUTER_API_KEY` hoặc tự đọc từ `~/.9router` | Chấm và tìm ảnh: `review_provider: codex`, `gen_assets.py --codex`. Tạo ảnh: chưa có phương án tự động, phải thiết lập 9router hoặc dịch vụ tương thích OpenAI |
| Codex CLI | Dự phòng chấm, tìm ảnh | `codex login` | Mất dự phòng |
| vidIQ | Nghiên cứu, số liệu | Kết nối trong tài khoản Claude | Sếp xuất số liệu từ YouTube Studio |
| ElevenLabs | Giọng đọc khi không có audio Sếp gửi | `ELEVENLABS_API_KEY` | Sếp gửi audio và srt |
| Google Drive | Lưu thành phẩm | `drive_mode: desktop` + `drive_path`, hoặc `rclone` + `drive_remote` | Không chạy được `publish_clean.py` |
| GitHub | Lưu repo | Quyền truy cập repo | Không đồng bộ được |
| YouTube | Đăng video | Chủ kênh đăng tay | Không đăng được |

Lưu ý rclone: nên tạo client_id riêng, client mặc định của rclone đang được thông báo ngừng trong 2026. Không chạy `rclone config show` vì lệnh này in token.

## Nhận việc
1. `git pull && git lfs pull`.
2. `python core/scripts/status.py` xem từng tập đang ở đâu.
3. Đọc `docs/decisions.md`, `core/standard/pipeline.md`, file vai trò của mình trong `core/roles/`.
4. `python core/scripts/learn.py brief --area <mảng>` trước khi làm.

Media của tập đang làm không có trong git. Đổi máy giữa chừng thì lấy gói nguồn trên Drive, hoặc chép thư mục tập sang máy mới.
