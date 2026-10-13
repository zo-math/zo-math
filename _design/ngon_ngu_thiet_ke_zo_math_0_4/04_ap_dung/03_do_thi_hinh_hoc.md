# Đồ thị và hình học

Nơi làm việc theo thông tin đã có: `E:/zo_math`. Trạng thái repo hiện tại: **cần AI tại máy xác minh**.

Quy tắc liên quan: ZO001, ZO019, ZO021, ZO022.

## Hiện trạng có bằng chứng

Bộ công cụ đồ thị nhận TeX/TikZ/PGFPlots, xuất PDF vector và SVG; template dùng zo_graph_v02.tex. So với nguồn được cung cấp, style mẫu 0.4 chủ yếu đổi nền vùng vẽ từ #FFF9E9 sang #FBFAF8, màu nhấn nhạt sang #FFE9A9 và khoảng đệm khung từ 4mm sang 5mm; phần lớn hệ nét được kế thừa. Font path của mẫu là đường phục vụ bộ mẫu, không được chép nguyên sang repo.

## Cách tích hợp

Kiểm công cụ và style thực tế đang dùng. Thêm style 0.4 có phiên bản và cơ chế chọn style tương thích engine hiện tại; không ghi đè style v0.2 đang được các bài hoặc công cụ BBT khác dùng. Giữ biểu thức, dữ liệu điểm, giới hạn, sampling, nhãn và ý nghĩa Toán. Bảo toàn nguồn, PDF/SVG và hợp đồng nhúng.

Nếu bộ dựng chưa hỗ trợ chọn style, thêm điểm cấu hình nhỏ có giá trị mặc định cũ; sản phẩm thử mới chọn 0.4. Không cần thay cả bộ máy dựng. Phân biệt tên public API của style với tên màu; ánh xạ token có kiểm giá trị.

## Ca kiểm

Dùng ca hiện có: một đường và tiếp tuyến ngang; nhiều đường/nhãn; tiệm cận hoặc tập xác định rời; điểm hở/kín; hình 2D/3D khi tác vụ chạm hình học. Xem ở cỡ chèn web/PDF, không chỉ zoom lớn. Kiểm nét thấy/khuất, góc/độ dài nếu có ý nghĩa hình học, font, label attachment và clipping.

Đầu ra: style có phiên bản, mẫu nguồn, PDF/SVG trước/sau, báo cáo đúng Toán và nhận diện, cơ chế chọn lại style cũ. Cùng ngôn ngữ với video nhưng có thể cần engine dựng khác; không ép mọi đồ thị động phải là SVG tĩnh.
