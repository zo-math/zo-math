# Màu, logo và chữ

## Màu

Nguồn: [color_system.json](../03_du_lieu/color_system.json). Giữ 23 giá trị hex, dùng tên red-1..7, yellow-1..7 và gray-1..9. Ba màu gốc lần lượt red-4, yellow-4, gray-8. Trắng #FFFFFF là bề mặt trung tính, không thêm thang nhận diện thứ tư.

Các vai trò trong mẫu: chữ gray-8, nhãn gray-6, link red-5, đường cong red-4, trục gray-7, nền ngoài gray-3, khối đọc trắng. Đây là phân vai triển khai 0.4; yêu cầu tên/mã màu có căn cứ riêng với chi tiết phân vai. Xem ZO001–ZO007.

Đổi token không chỉ tìm-thay tên: yellow-08/yellow-02 ở nguồn TikZ cũ có thể mang mã khác. Dùng ánh xạ có kiểm tra giá trị; tên không nằm trong token_migration.json phải được đối chiếu, không đoán theo số. Mã #FFCF3D trong hướng dẫn Studio cũ đã được thay bằng #FFCA28 ở hệ đang áp dụng.

Sáu nền thử là red-1/2, yellow-1/2, gray-2/3. Khối trắng và vai trò chữ không thay khi người đọc chọn nền. Nền của vùng đồ thị có thể là gray-1 theo mẫu; đây là bề mặt hình riêng, không phải nền toàn trang.

## Logo và dấu nhấn

Dùng vector trong [logos](../07_mau_thi_giac/logos/horizontal_color.svg). Không dựng lại chữ bằng một font gần giống khi đã có SVG. Không kéo giãn, tự thêm viền O, bóng hoặc chuyển sắc. Hình chữ, tỉ lệ ô và khoảng hở cụ thể còn là mẫu thử, cần xem ở cỡ dùng thật.

Bản màu ưu tiên khi môi trường cho phép; bản một màu dùng khi đầu ra chỉ hỗ trợ một màu. Đừng đặt MATH trắng trên nền trắng trong bản dành cho nền tối. SVG gốc là tài sản chỉnh sửa; PNG là bản xuất, không phải nguồn hình học.

Dấu nhấn dựa trên tệp S01: đỏ dài 15u, khe 1.75u, vàng 8u, bo .5u, vùng trống 2u. Kích thước đó thuộc đề xuất kế thừa; không gọi là hình học đã được duyệt cuối. Dùng màu hiện tại và giữ nó ở vai trò nhận diện phụ, không làm dấu trừ, đường dữ liệu hoặc gạch chân một cụm chữ.

## Chữ

Mẫu 0.4 dùng Be Vietnam Pro cho giao diện/lời dẫn và STIX Two Text/Math cho học liệu/toán. Font kèm theo có tệp giấy phép trong assets của mẫu. Khi phân phối bản tích hợp, giữ giấy phép tương ứng; bộ bàn giao không xác lập quyền đối với mọi tài sản bên ngoài trong nguồn lịch sử.

Phân cấp bằng vai trò: tiêu đề, thân bài, nhãn phụ, chú thích, công thức. Không bê nguyên px từ web sang Manim hoặc pt của PDF. Cần kiểm tiếng Việt có dấu, công thức dài, xuống dòng, cỡ thực trên điện thoại và font trong bản xuất.

Tag: small caps nếu font hỗ trợ; nếu không, thử chữ hoa cỡ nhỏ với khoảng cách vừa đủ. Không đổi biến toán thành chữ hoa theo tag/phụ đề. Không dùng chữ mờ tới mức mất khả năng đọc.
