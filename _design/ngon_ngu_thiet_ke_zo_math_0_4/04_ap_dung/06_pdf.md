# PDF và học liệu tải về

Nơi làm việc theo thông tin đã có: `E:/zo_math`. Trạng thái repo hiện tại: **cần AI tại máy xác minh**.

Quy tắc liên quan: ZO001, ZO012, ZO014, ZO015, ZO019.

## Phạm vi mẫu hiện có

0.4 có bìa và trang kết mới cho tám PDF R1-G01. Trang ruột giữ nguồn v1.3, một số tài liệu được thêm trang kết sau nội dung cuối thay vì thay trang có bài học. Metadata và bằng chứng nằm ở design/pdf_editions.json trong mẫu.

## Cách tích hợp

Đọc pipeline PDF hiện tại của gói, YAML/TeX/Lua, logo/font, quyền sử dụng, link canonical, đánh số và biến thể học sinh/giáo viên/bài học. Không giả định mọi PDF của khóa dùng pipeline bài viết chung trong _quarto-pdf.yml.

Dùng nội dung đang có để dựng lại; đưa thiết kế bìa/kết thành template có dữ liệu tên bài, biến thể, phiên bản và đường quay lại học. Không lấy PDF ruột 0.4 ghép vào bản học liệu mới. Chưa giao tái dàn ruột thì ghi rõ phạm vi chỉ bìa/kết; nếu giao ruột, xử lí font, tag, bảng native và ngắt trang cùng ca kiểm.

## Kiểm và đầu ra

Kiểm bìa/ruột/cuối tất cả biến thể bị tác động, bookmark, hyperlinks, số trang, font nhúng, QR, mã phiên bản nội dung và chữ trên giấy. Đối chiếu dữ liệu ủng hộ từ nguồn hiện dùng trước phát hành. Kiểm trắng đen và kích thước in. Đầu ra gồm template tích hợp, PDF từ nguồn hiện tại, đối chiếu bảo toàn nội dung và cách chọn lại template cũ.
