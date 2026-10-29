# Báo cáo dựng tập thử Codex

- Video: `/Users/admin/Desktop/test-codex.mp4`
- Thời lượng tệp: 51,925 giây; 1920×1080; H.264 + AAC; phụ đề đã gắn trong hình.
- Khớp storyboard/SRT: 98%; validate_scenes.py: OK trước cả hai lượt render đầy đủ.
- Tổng thời gian chạy: 20 phút 39 giây, gồm tạo/tìm ảnh, chờ lỗi mạng, preview và hai lượt render.
- Ảnh sử dụng: 4 ảnh AI tạo mới; 1 cutout AI dùng lại; 1 ảnh thật mới tải (USGS, public domain). Một ảnh bản đồ từng tải bị loại sau khi duyệt vì không đúng mục đích.

## Các cảnh

| Cảnh | Dài (giây) | Component | Lines |
|---|---:|---|---|
| s01 | 4.705 | Parallax | [0, 0] |
| s02 | 4.663 | GeoMap | [1, 1] |
| s03 | 5.366 | Parallax | [2, 4] |
| s04 | 5.750 | GeoClock | [5, 7] |
| s05 | 4.968 | GeoMap | [8, 9] |
| s06 | 7.047 | KenBurns | [10, 12] |
| s07 | 7.379 | Collage | [13, 14] |
| s08 | 4.661 | GeoMap | [15, 18] |
| s09 | 7.312 | Parallax | [19, 20] |

## Lỗi và xử lý

- Wikimedia HTTP 429 cho lớp đá và chim: đổi query, thử lại đúng giới hạn. Lớp đá tải thành công từ USGS; nguồn chim Flickr sau đó trả HTTP 403. Dùng cutout chim có sẵn với nhãn Tái hiện, ghi thiếu ảnh thật trong missing_assets.md.
- Bản đồ đầu tìm được là hình phân bố địa điểm hóa thạch, không phù hợp. Lượt tìm lại hết 600 giây. Loại ảnh đó; dùng GeoMap với nhãn Việt Nam ngày nay, không diễn giải là vị trí cổ địa lý. Đây là sai khác so với storyboard.
- Nền rừng cũ không đạt phong cách: thay bằng ảnh AI mới, tổng 4 ảnh AI, dưới mức tối đa 8.
- Cảnh s06 ban đầu dài 9,464 giây: đổi điểm cắt theo đầu câu; mọi cảnh hiện dài 4–8 giây.
- GeoClock ban đầu hiển thị 74 triệu năm ở khung 17 giây: cố định from_ma/to_ma = 66, render lại và kiểm tra đúng.
- Không gặp lỗi mã nguồn hệ thống; không sửa core/, không cài gói, không git commit. Các tệp tập thử và ảnh được tạo theo quy trình.

## Giới hạn còn lại

- Không có bản đồ cổ phù hợp và ảnh thật chích bông; đã nêu phương án thay ở trên.
- s08 gộp 4 câu rất ngắn để giữ nhịp 4–8 giây, vượt hướng dẫn 1–3 câu/cảnh.
- Tiêu đề cố định của GeoClock dài hơn 6 từ; nội dung chữ do tập này tự khai báo giữ tối đa 6 từ. Không sửa component theo giới hạn không thay code.
- Cảnh tối dài khoảng 7 giây theo ranh giới câu; hiệu ứng mưa vật liệu trong nền trời cam chưa rõ.

## Nhận xét 8 khung hình

- **03s:** Rừng bình minh, cutout đầy đủ chân/đuôi; chữ và phụ đề rõ.
- **07s:** GeoMap thế giới, hai điểm Mexico–Việt Nam và mũi tên; thẻ 15.000 km đọc rõ.
- **12s:** Rừng trời cam, khủng long bên phải không che phụ đề. Hiệu ứng mưa vật liệu còn nhẹ, chưa nổi bật.
- **17s:** GeoClock hiển thị đúng 66 triệu năm sau khi sửa; có badge xác nhận. Chữ tiêu đề cố định của component nhiều hơn giới hạn 6 từ, chưa chỉnh vì không sửa code hệ thống.
- **26s:** Cảnh tối có chủ đích trước cú lật; chỉ còn phụ đề. Đoạn tối khá dài, giảm mật độ hình.
- **30s:** Tiếp tục khoảng tối trước tiết lộ vị trí cổ địa lý; phụ đề dễ đọc, nhưng hình ít thông tin.
- **37s:** Collage lớp đá thật và cutout chích bông; có nguồn USGS và nhãn Tái hiện, hai hình không lấn phụ đề.
- **44s:** GeoMap Việt Nam, có Hoàng Sa, Trường Sa, Biển Đông; phụ đề rõ.

Lưới kiểm tra: render/check.jpg. Nguồn ảnh: meta.md.
