# Bảng biến thiên

Nơi làm việc theo thông tin đã có: `E:/zo_math`. Trạng thái repo hiện tại: **cần AI tại máy xác minh**.

Quy tắc liên quan: ZO009, ZO010, ZO011, ZO013.

## Điều giữ lại

Nguồn hiện có tách JSON canonical, bộ dựng tài sản và lớp tích hợp QMD. Giữ dữ liệu, ID, validator, excluded_columns, intentional_error và cách gọi bảng theo mã. Không nhập lại bảng thủ công ở từng trang.

## Điều cần đổi để giống 0.4

Lớp tích hợp HTML hiện chèn SVG và một bảng ẩn. Muốn bảng native hiển thị phải bổ sung renderer dùng cùng dữ liệu, dàn toán đúng và giữ semantic headers/caption. Không chỉ hiện bảng ẩn cũ rồi coi đã xong: bảng ấy có thể còn Unicode/text và thiếu chuẩn hiển thị mới.

Tạo nhánh đầu ra HTML native và LaTeX tabular thường theo engine hiện có. Giữ đầu ra vector cũ cho sản phẩm chưa chuyển hoặc ca ngoại lệ có lí do. Không fork công cụ riêng cho từng bài. Cơ chế chọn đầu ra cần phiên bản và phạm vi rõ; không đổi mặc định toàn repo trước khi kiểm ca liên quan.

## Ca kiểm

Hai hàng/ba hàng theo dữ kiện; bảng rộng; dấu đạo hàm không tồn tại; điểm loại; giới hạn trái/phải khác nhau; hàm có cùng chiều nhưng đạo hàm bằng 0; ví dụ sai có chủ ý. Hàng hàm số duy nhất, không rowspan mô phỏng cao-thấp. Đủ lưới, không nền dư ngoài khung, công thức render từ LaTeX, không mất chú thích.

Đầu ra: adapter chung, dữ liệu không đổi hoặc migration được mô tả nếu thật sự cần, HTML/LaTeX/PDF tương ứng và báo cáo. 13 bảng trong mẫu 0.4 là tập đối chiếu có sẵn; thêm ca chỉ khi nó giải quyết rủi ro chưa được phủ.
