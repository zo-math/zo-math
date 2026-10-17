# R1-G04 — nút mục lục theo thiết kế đã chốt

Ngày 17/10/2026. Chỉ sửa component HTML và cơ chế chống tái diễn. Chưa có PDF học liệu, commit, push hay xuất bản trong lượt này.

## Nguyên nhân

Chủ trì gửi ảnh có nút dạng dài “Bài học · Mục lục”. Thiết kế đã chốt tại hợp đồng kit là nút icon danh sách, tròn 52×52px, có tên truy cập và giữ thao tác bàn phím.

Lỗi thuộc cách tích hợp của agent:
- Template page.html.tpl còn nút chữ dạng thử nghiệm và site-ui.js còn cập nhật tên view vào mobile-view.
- G01 đổi sang icon trong zo_web_2027_downloads.py và downloads.css; G02 lặp thao tác trong zo_web_2027_g02_payloads.py, đồng thời nạp CSS của G01. Đây là chức năng shell nhưng nằm trong nhánh tải PDF.
- G04 chưa có PDF nên không gọi nhánh ấy. Sao adapter/mẫu trang chưa bao gồm đầy đủ component đã chốt.
- Các kiểm trước chỉ xác nhận nút mở được mục lục, chưa kiểm kiểu icon, kích thước và tên truy cập. PASS của nhãn/hình/bảng không chứng nhận nút này.

Đây là lỗi xác định sai chủ sở hữu component và thiếu phép kiểm, không cần chọn một thiết kế mới hoặc thêm PDF để nhận giao diện nút.

## Sửa nguồn

| Chủ sở hữu | Nguồn hiện hành và trách nhiệm |
|---|---|
| Quy tắc | 07/6 và hợp đồng kit: chỉ icon, kích thước đã chốt, tên truy cập; không lộ tên view |
| Template | page.html.tpl chứa SVG danh sách của thiết kế G01, mode icon và tên truy cập; hook mobile-view chỉ giữ tương thích, luôn hidden |
| CSS shell | web-shell.css sở hữu kích thước/hình tròn/icon, không phụ thuộc body class của gói hoặc downloads.css |
| Hành vi | site-ui.js giữ mở/đóng/focus/resize; mode icon không bị cập nhật thành tên view |
| Cổng kiểm | zo_web_2027_shell.py kiểm template trước ghép và HTML/runtime CSS sau adapter. CLI checker G04 cũng gọi cùng cổng |
| Bước bàn giao | 02, AGENTS và kit/kiem_thu.md yêu cầu ca trang chưa PDF, đổi view/reload, Enter/Escape/focus/resize và ca âm |

Đoạn cũ trong G01/G02 giữ tương thích sản phẩm/receipt hiện hành; không là nguồn chuẩn cho gói mới. Không sửa các tệp PDF, CSS nguồn riêng của gói cũ hoặc cập nhật receipt của chúng.

## Kiểm và giới hạn

- Dựng mới đúng một trang G04 qua CLI QMD, HTML-only, trong source mirror cô lập; không đọc HTML cũ để sinh nội dung, không dựng lại đồ thị/BBT hoặc PDF.
- Đối chiếu trực tiếp với HTML trước sửa: main, rail, footer và site-top nguyên DOM. Nguồn QMD, nội dung toán, ảnh bìa, toàn bộ dữ liệu/hình và bản thảo giữ nguyên.
- Cổng mới từ chối chính HTML có nút cũ đã trình; thử âm riêng bắt mất mode, tên truy cập, icon/đích dialog, lộ chữ hoặc chiều rộng capsule.
- Trang G04 thật được kiểm ở 390/430/768/999/1000/1440px; icon 20px trong nút 52px, hit target thật, fixed khi cuộn, Enter mở, Escape trả focus, chọn view đóng, reload, resize và sắc xám. Không có stylesheet tải PDF trong trang này.
- Sáu fixture component dùng template/runtime canonical và các ngữ cảnh CSS Nhà, Nhà editorial, D0, G01/G02 có CSS PDF, G04 chưa PDF. Đây là kiểm tương thích component, không phải dựng hoặc nghiệm thu lại sáu sản phẩm.
- Báo cáo browser ban đầu được giữ riêng. Lượt đầu thiếu payload kí tự Enter nên chỉ phát key event, chưa tạo native click; đối chiếu cách kiểm G01 và trace sự kiện đã xác định lỗi ở phép mô phỏng. Lượt kiểm đúng thao tác đạt; không thêm handler bàn phím giả vào sản phẩm.
- Kết quả cụ thể, source/runtime hash và các tệp sửa nằm trong JSON cùng tên. Chưa có chủ trì duyệt bản hiển thị này hoặc kiểm thiết bị thật.

## Bản xem

[Bản HTML mới tại đúng vị trí chủ trì phản ánh](http://127.0.0.1:8877/_audit/g04_drawer_20261017/g04-reading.html?r1-view=bai-hoc#T05).

Tệp xem: E:/zo_math/_audit/g04_drawer_20261017/g04-reading.html. HTML đầy đủ cùng runtime ở html/; ảnh kiểm ở images/. Hồ sơ này ở _quy_trinh/ho_so của gói; chỉ 03 giữ trạng thái và việc tiếp theo.
