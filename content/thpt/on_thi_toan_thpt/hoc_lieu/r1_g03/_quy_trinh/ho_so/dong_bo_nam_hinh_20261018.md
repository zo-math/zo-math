# Đồng bộ năm ảnh G03 còn lệch cỡ — GRAPH-G03-02

Ngày 18/10/2026. Không có trở ngại kỹ thuật. Agent trước đó đã suy rộng việc giữ đối chứng thành giữ nguyên năm ảnh hiển thị sai tỉ lệ; hạn chế ấy đã được sửa trong điều hành.

Năm ảnh chèn trong đoạn văn không có figure nên không nhận selector đặt cỡ của G03. Bộ ghép nay gọi `zo_course_math_assets.apply_graph_display` giống các gói khác, nhận cùng helper tính cỡ và CSS không phụ thuộc figure. Cổng HTML chung và checker G03 kiểm đủ 11 ảnh. Không sửa tay HTML, không vẽ lại TEX/SVG hoặc PDF.

[Bản xem G03 mới](http://127.0.0.1:8877/_audit/g03_graph_display_20261018/html/content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g03/index.html?r1-view=toan-van).

- [Luyện tập — Một hình, ba hành vi](http://127.0.0.1:8877/_audit/g03_graph_display_20261018/html/content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g03/index.html?r1-view=toan-van#L09).
- [Kiểm tra — Đọc hai đầu và một mốc hữu hạn](http://127.0.0.1:8877/_audit/g03_graph_display_20261018/html/content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g03/index.html?r1-view=toan-van#K02).
- [Sửa lỗi — Đường đứng và đường xiên từ hai nhánh](http://127.0.0.1:8877/_audit/g03_graph_display_20261018/html/content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g03/index.html?r1-view=toan-van#S-L05).
- [Sửa lỗi — Điểm hở và nhánh bên kia](http://127.0.0.1:8877/_audit/g03_graph_display_20261018/html/content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g03/index.html?r1-view=toan-van#S-K04).
- [Sửa lỗi — Điểm kín và hai nhánh khác nhau](http://127.0.0.1:8877/_audit/g03_graph_display_20261018/html/content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g03/index.html?r1-view=toan-van#S-O03).

## Kiểm chứng

- CLI QMD dựng HTML-only cô lập đạt; không dựng lại website hoặc PDF học liệu.
- HTML G03 1299/1299; trình duyệt 30/30 ở 1440/430/390 px, đo đủ 11 ảnh. Sáu ảnh vốn đã đúng giữ width/height; năm ảnh sửa đạt cùng tỉ lệ. Kiểm không méo/tràn trang, cuộn cục bộ và nút mục lục.
- Bảo toàn/thử âm 58/58: chính văn theo bản nhãn hiện hành, công thức, heading, ID, bảng, alt không đổi; thiếu component trên từng ảnh không có figure hoặc mất namespace CSS bị chặn. Các HTML G01/G02/G04 vừa sửa trước vẫn qua cổng hiển thị. 1489 tệp bảo vệ không đổi, gồm QMD/TEX/SVG/PDF G03, bìa và docs công khai.
- Đã xem ảnh chụp năm vị trí trên trang. Bản xem và bằng chứng trước sửa giữ nguyên; báo cáo cũ không được ghi lại thành kết quả mới.

## Lưu trữ và trạng thái

HTML/runtime, số đo, thử âm và ảnh chụp lưu tại `_audit/g03_graph_display_20261018/`. Nguồn sửa là ba script được liệt kê trong JSON cùng tên; 07/03/04/08, chỉ dẫn/kit và con trỏ hồ sơ G03 đồng bộ để không giữ lỗi dưới danh nghĩa đối chứng. G03 vẫn chưa có bảng biến thiên.

Chờ chủ trì xem HTML sửa; chưa nghiệm thu hiển thị, PDF học liệu mới, commit/push hoặc phát hành. Bản sao build và profile trình duyệt tạm được dọn; giữ bản xem và bằng chứng cần đối chiếu.
