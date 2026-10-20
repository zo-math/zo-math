# R1-G05 — Chuyển QMD và bàn giao HTML, 21/10/2026

**Cập nhật hiện hành:** [Đã sửa chú thích nguồn và căn giữa công thức](sua_chu_thich_va_can_giua_20261021.md) theo phản hồi; bản chuyển ban đầu dưới đây giữ làm lịch sử, số kiểm hiện hành là 1900/1900.

Bản HTML từ nguồn QMD hiện hành đã dựng vào `docs/content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g05/index.html`, đang chờ chủ trì xem. [Mở bản xem](http://127.0.0.1:8877/docs/content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g05/index.html). Bản thảo, sửa hình và hướng bìa đã duyệt ngày 20/10/2026; đây chưa là duyệt HTML hoặc bố cục bìa thành phẩm. Phạm vi được giao chỉ QMD, tài nguyên/bìa và HTML; chưa dựng PDF, commit, push hoặc xuất bản.

## Nguồn và thay đổi khi chuyển

`index.qmd` là nguồn biên tập hiện hành; bản thảo duy nhất và các tài nguyên bản thảo được giữ nguyên để đối chiếu, không biên tập hai nguồn song song. Đối chiếu tự động giữ nguyên đúng thứ tự toàn bộ 567 biểu thức toán của bản thảo. HTML có 576 biểu thức vì Nhật kí dùng chung bổ sung 9 biểu thức. Có 29 nhiệm vụ cùng lời giải, 8 Gợi mở, 8 ví dụ, 8 Điểm dừng; Gợi mở nằm trước giải thích trong từng mục con Bài học. Mục tiêu ở Bắt đầu; Câu hỏi dẫn đường và mục lục Bài học dùng đúng cơ chế dùng chung.

Có 58 dòng làm rõ câu chữ theo cổng biên tập hiện hành (ví dụ thay “miền” bằng điều kiện/tập giá trị của biến theo ngữ cảnh, viết đầy đủ tiêu chí chưa xác nhận và bài chưa xem đề/lời giải), đã đọc lại và chỉnh các câu kết quả thiếu tự nhiên; không đổi toán. Bảng Kiểm tra còn ba cột, phần “Nếu còn vướng” được giữ nguyên dưới bảng. Bảng Ôn nền dùng hai cột theo profile chung, vẫn giữ nguồn, tự kiểm và điểm trở về; lịch Ôn lại đưa ba thời điểm đã có vào bảng theo profile chung. Chín bảng gồm cả hai bảng Nhật kí lấy từ nguồn chung, không sao chép nội dung.

Các neo cũ của Luyện tập, Kiểm tra, Nhật kí được giữ làm alias. Liên kết đề–lời giải chỉ dùng “Xem lời giải” và “Xem đề bài”. Lời giải đóng mặc định; cổng kiểm đối chiếu đủ 29 cặp. Ôn nền dẫn sáu tài nguyên nền có nguồn QMD thực ở G01/G02; khi gọi hỗ trợ, ngữ cảnh Điểm dừng và đường trở lại được giữ. Không ép học sinh chạy toàn bộ hoạt động thành chuỗi; không dựng nút tải PDF giả.

## Tài nguyên và bìa

Nguồn chính thức: `du_lieu/minh_hoa.json`, `_quy_trinh/sinh_hinh.py`; đầu ra SVG/PNG ở `hinh/`, provenance và ràng buộc hình ở `giao_dien/minh_hoa_manifest.json`. Bộ sinh lấy quy chuẩn màu/phông từ `E:/zo_math_graphics` qua adapter hiện hành, không phụ thuộc `_audit/` hoặc vùng bản thảo. Năm hình thân bài (10 SVG/PNG) giống từng byte bản đã duyệt, gồm các sửa đường đo và quầy. HTML sử dụng SVG; các nhãn đo theo cỡ chữ thực 10 pt của bộ sinh, hình rộng cuộn trong khung riêng để vẫn đọc được trên điện thoại.

Các hàm hình chiếu, đường đo và cảnh tham số có thể tái sử dụng trong cảnh cùng cấu trúc, chưa là công cụ dựng mọi tình huống. Cổng kiểm giữ các ca sai đầu mút/đường dóng/vạch giới hạn, phối cảnh và kết nối cột quầy; ca sửa hỏng dữ liệu, mã sinh hoặc SVG phải bị từ chối. Hình bối cảnh có vai trò riêng, không giả là đồ thị hàm số và không tạo bảng biến thiên trống.

Bìa dùng hướng đã duyệt: hình trải phẳng và hộp gấp, không kế thừa bìa gói mẫu. Bố cục production thu gọn khoảng trắng để hai hình rõ hơn trong khung bìa. Hướng đã duyệt; bố cục và thành phẩm HTML hiện tại vẫn chờ chủ trì xem. Không ghi tự động là đã nghiệm thu bìa.

## Kiểm và giới hạn

- Cổng gói: 1893/1893, không có tệp/neo nội bộ hỏng; 576 biểu thức, 9 bảng, 90 vùng đọc. Có kiểm âm trên DOM tách rời và fixture tạm; không sửa đầu ra để chạy thử lỗi.
- Trình duyệt thật: 11 chế độ ở 1440 và 390 px, không tràn ngang toàn trang; hình/bảng rộng cuộn trong khung riêng. Đã kiểm 29 cặp đề–lời giải bằng bàn phím, đóng/mở lời giải và trở về đúng hoạt động; đã thử gọi Ôn nền G01 và quay lại G05, metadata tám Điểm dừng.
- Hồi quy nguồn G01–G04 qua CLI QMD; hồi quy profile bảng 812/812, bìa 10 ca, điều hướng 28/28. Không dựng lại sáu trang cũ.
- Kiểm 850 tệp sản phẩm/nguồn đã phát hành so với baseline: giữ nguyên. Bản thảo cũng giữ nguyên hash; không có PDF G05.
- Schema/readiness kiến trúc học tập qua cổng kỹ thuật; các khoảng trống xác nhận sau sửa được giữ rõ trong nguồn, không suy ra rằng mọi lỗi đã có đủ câu mới hoặc có dữ liệu quan sát học sinh. Việc xem HTML không thay duyệt toán độc lập hoặc nghiệm thu của chủ trì.

Bằng chứng kỹ thuật ở `_audit/g05_qmd_html_20261020/`: `g05_checks_delivery.json`, `render_support_context.json`, `editorial_changes.json`, `shared_source_regression.json`, thư mục `browser/` và bản bàn giao trình duyệt mới `handoff-confirmed.json`. Audit chỉ giữ bằng chứng; nguồn/ảnh/HTML chuẩn nằm ở vị trí chính thức. Chi tiết trạng thái có trong JSON cùng tên hồ sơ này.

## Bảo toàn và bước tiếp theo

Manifest bảo vệ cũ giữ nguyên các hash sản phẩm sáu trang và 33 PDF cùng trạng thái đã duyệt. Mười phụ thuộc nguồn/công cụ/hồ sơ thay đổi để tích hợp G05 được ghi chuyển tiếp trước–sau và căn cứ kiểm riêng; bản manifest trước chuyển tiếp được lưu nguyên vẹn làm bằng chứng. Đây là cập nhật tồn kho phụ thuộc hiện hành sau thay đổi nguồn và kiểm, không sửa receipt nghiệm thu lịch sử hoặc đổi hash để che lỗi. G05 có manifest bảo vệ riêng với trạng thái `pending_owner_review`.

Chủ trì xem HTML và bố cục bìa, gửi phản hồi hoặc duyệt bản hiện hành. Chưa chuyển sang PDF hoặc phát hành khi chưa được giao. Mọi sửa tiếp theo phải sửa nguồn → dựng → kiểm → sửa nguồn và ghi đè đầu ra chuẩn.
