# R1-G04 — Nguồn và HTML chờ duyệt

Đã chuyển bản thảo 0.2 đã được chủ trì xem thành một nguồn QMD của ứng viên. Giữ nguyên bản thảo/tài nguyên bản thảo để đối chiếu, không biên tập song song.

- [Mở bản HTML thực tế](../../../../../../../_audit/r1_g04_html_20261017/r1-g04-reading.html).
- [Nguồn QMD](../../index.qmd), [binding nhãn](../../giao_dien/he_nhan.json), [manifest kiến trúc](../kien_truc_hoc_tap.yml).
- [Kết quả và fingerprint](kiem_qmd_html_20261017.json).

## Nội dung và mẫu

Giữ nguyên 1042 biểu thức, năm mục kiến thức, năm Gợi mở trong đúng từng mục, bảy ví dụ và 28 cặp đề–lời giải. Khởi động không chứng nhận cả gói. Manifest giữ tiến trình khuyến nghị, không khóa hoạt động tuần tự.

Nhật kí gọi một nguồn chung đủ 14 trường, kèm ví dụ giả lập đã được component ghi rõ thuộc “Đơn điệu và cực trị”, không là nhiệm vụ thêm. Chín biểu thức bổ sung của HTML thuộc ví dụ dùng chung này.

Định hướng, Cách thực hiện, Ôn nền và lời giải dùng thành phần thu gọn hiện hành. Liên kết lời giải đưa đến đúng đơn vị; người học chủ động mở summary để xem. QD025 có owner/ngữ cảnh/số và nhãn nhìn thấy. QD030 phân biệt bảng biến thiên, rubric mục tiêu, process định tuyến/Nhật kí; không gán đại trà.

35 SVG chính thức được dựng bằng ZO Math từ dữ liệu sản xuất, cả 35 khớp byte hình đã xem. Nguồn TEX/SVG chính thức không phụ thuộc bản thảo. Bìa giữ đúng byte được duyệt và qua cổng nguồn/HTML. PDF vector chuyển đổi là trung gian được dọn, không là PDF học liệu.

## Kiểm định

- Nguồn và render qua CLI QMD đạt, không lỗi/cảnh báo; profile on-thi-preview, chỉ HTML đúng một trang.
- Schema/readiness kiến trúc đạt, planned=0; không thay nghiệm thu nội dung.
- HTML 715/715: đủ toán theo thứ tự sau mở include, liên kết/tài nguyên/fragment hợp lệ.
- Edge 234/234 phép kiểm hợp lệ ở 1440/430/390 px: các view, đóng/mở, căn bảng, tràn trang, ảnh, nguồn gọi hỗ trợ, Back/tải lại, lời giải về đề, mục lục và không JavaScript. Sau chỉnh phân loại bảng chỉ kiểm lại phần chịu ảnh hưởng. Phép kiểm mở summary đúng thao tác thực; không giả định link tự bung lời giải.
- Đã xem lát cắt desktop/mobile của bìa, Gợi mở, ví dụ, lời giải; hình có đối chiếu byte với bộ đã xem.
- Hồi quy bảng 18/18, điều hành 177/177 và self-test 235/235, điều hướng năm trang 10/10. Binding bảng và đích điều hướng cũ giữ nguyên.
- 1404 tệp docs và Git index không đổi; chín sản phẩm đối chứng G01–G03 khớp dấu vết trước viết.

## Chờ duyệt và vận hành

Chờ chủ trì xem HTML thực tế. Chưa duyệt đầu ra, chưa PDF học liệu, commit/push/xuất bản, thử với người học hoặc phản biện toán độc lập. Không đưa G04 vào danh mục công khai; menu riêng của bản xem có đích hiện tại.

Bản HTML, báo cáo và ảnh cần xem ở _audit/r1_g04_html_20261017/. Vùng dựng tạm .quarto/r1_g04_html_20261017/ và cache trình duyệt được dọn. Máy chủ chỉ nghe 127.0.0.1.

Điểm vào dựng lại là CLI zo_qmd.py render cho index.qmd của gói với --html-only và profile on-thi-preview, qua launcher zo_python.py. Để bảo toàn docs, dựng trong bản sao nguồn cô lập dưới .quarto, giữ cấu hình gốc, nguồn navbar/footer/include và Git index riêng; hook tự nối adapter G04, cổng nhãn/ảnh. Không dùng HTML/audit làm đầu vào chính thức. Bộ kiểm riêng: scripts/zo_web_2027_g04_check.py.
