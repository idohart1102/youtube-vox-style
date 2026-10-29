# YouTube Vox System

## Cài trên máy mới
1. Copy hoặc `git clone` cả thư mục này về máy, đặt ở đâu cũng được.
2. Windows: `powershell -ExecutionPolicy Bypass -File setup.ps1`. macOS/Linux: `bash setup.sh`. Script sẽ kiểm tra node, python3 và ffmpeg, cài thư viện, rồi tạo `config/machine.yaml` và `.env`.
3. Điền API key vào `.env` và kiểm tra đường dẫn trong `config/machine.yaml`.
4. Thử chạy `python core/scripts/doctor.py` (macOS có thể là `python3`). Nếu ra "ALL OK" là dùng được.

## Vì sao chuyển máy được
- Không có đường dẫn tuyệt đối trong code. `core/scripts/paths.py` tự tìm thư mục gốc.
- Thứ riêng của từng máy (chromium, ffmpeg, số luồng render) nằm ở `config/machine.yaml`. File này không đưa vào git.
- Bí mật (API key) nằm ở `.env`. File này cũng không đưa vào git.
- Media (ảnh, audio, video, thumbnail) được lưu bằng Git LFS để mang theo khi chuyển máy. Cần cài Git LFS trước khi clone, rồi chạy `git lfs pull` để tải đủ file.
- Thư viện cài theo phiên bản cố định trong `package.json` và `requirements.txt`.

## Đồng bộ nhiều máy (khuyến nghị)
- Mã nguồn, nội dung các kênh, asset và media được đồng bộ trong repo GitHub riêng tư; không đưa `.env`, `config/machine.yaml`, `node_modules/` và `.venv/` lên Git.
- `assets/` và media dùng Git LFS. Nếu muốn dùng kho ảnh ngoài repo, khai báo đường dẫn trong `config/machine.yaml` ở mục `assets_dir`.

## Tiếp tục làm việc trên máy khác
1. Cài Git, Git LFS, Node.js/npm, Python 3 và FFmpeg. Đăng nhập GitHub bằng tài khoản có quyền truy cập repo private.
2. Tải repo và toàn bộ media:
   ```bash
   git lfs install
   git clone https://github.com/idohart1102/youtube-vox-style.git
   cd youtube-vox-style
   git lfs pull
   ```
3. Chạy `bash setup.sh` trên macOS/Linux hoặc `powershell -ExecutionPolicy Bypass -File setup.ps1` trên Windows.
4. Điền API key vào `.env`, kiểm tra `config/machine.yaml`. Thông tin đăng nhập 9router trên máy cũ không nằm trong repo; thiết lập lại dịch vụ/key nếu cần tạo ảnh.
5. Kiểm tra bằng `.venv/bin/python core/scripts/doctor.py` trên macOS/Linux hoặc `.\.venv\Scripts\python core\scripts\doctor.py` trên Windows.
6. Đọc `CLAUDE.md` để tiếp tục đúng quy trình; mở studio bằng `npm run studio`.

Sau mỗi phiên làm việc, commit/push các thay đổi. Ở máy còn lại, chạy `git pull` và `git lfs pull` trước khi làm tiếp.
