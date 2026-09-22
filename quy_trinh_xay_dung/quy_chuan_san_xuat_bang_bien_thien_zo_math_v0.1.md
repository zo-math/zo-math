# Quy chuẩn sản xuất bảng biến thiên ZO Math

**Phiên bản:** 0.1
**Trạng thái:** áp dụng cho công cụ canonical và lượt chuyển đổi R1-G01.

## Nguyên tắc

Bảng biến thiên là biểu diễn có cấu trúc của miền, mốc, trạng thái đạo hàm và chiều
biến thiên; không được suy ngược máy móc từ hình đồ thị. Nguồn canonical phải ghi đủ
mốc hữu hạn/vô cực, điểm loại, giá trị hoặc trạng thái tại mốc, dấu trên từng khoảng,
chiều tăng–giảm–không đổi và giới hạn một phía khi cần. Nhãn hàm là nội dung toán học.

Phong cách là “Học thuật tĩnh tại”: STIX Two Text/STIX Two Math. Bảng không duy trì
một bảng màu gần đúng riêng: nền, khung, đường phân cách, chữ và màu nhấn phải tham
chiếu trực tiếp token của đồ thị canonical v0.2. Khung ngoài có đủ bốn cạnh, dùng
`zoGraphVTwoPlotBorder`, nét `0,45 pt`, bo bốn góc `2 mm`; nền
`zoGraphVTwoPlotBackground` phải được cắt theo chính khung bo này. Đường ngang/dọc
bên trong dùng cùng token màu và độ dày, kết thúc trong vùng clip, không xuyên qua
góc bo. Khoảng đệm phải đủ đọc ở desktop, mobile và PDF. Không dùng raster
canonical, không đặt tiêu đề hay lời giải bên trong tài sản vector.

Điểm xác định, điểm không xác định, đường phân cách, giới hạn và cực trị phải giữ
đúng nghĩa. Dấu đạo hàm phải tương thích với chiều biến thiên, trừ ví dụ sai được
đánh dấu rõ trong nguồn. Bảng không được tự bổ sung dữ kiện mà bài học không nêu.
Nội dung dài phải được giữ nguyên chữ và cỡ chữ. Khi chiều rộng tự nhiên của ô không
đủ, nguồn dữ liệu dùng `column_min_widths_mm` để đặt chiều rộng tối thiểu cho cả cột;
không viết nhánh theo mã bảng, không thu nhỏ riêng chữ hoặc toàn bảng. Chỉ cột được
khai báo mới mở rộng, trong giới hạn 8–60 mm.

Khi nhúng vào PDF học liệu, kích thước vật lí của asset là kích thước ưu tiên. Lớp
tích hợp chỉ được thu nhỏ khi asset vượt chiều rộng hoặc chiều cao khả dụng; không
được phóng bảng hẹp lên đầy dòng. Bảng giữ căn trái và không vượt khối văn bản.

PDF và SVG phải sinh từ cùng TEX, là vector, nhúng STIX và có hình học tương đương.
HTML giữ một bảng ngữ nghĩa trợ năng từ cùng JSON, nhưng phần nhìn dùng SVG để không
làm mất vị trí cao–thấp và mũi tên. QMD chỉ tham chiếu mã bảng. Tiêu đề hiển thị do
lớp tích hợp QMD tạo, dùng kiểu chú thích hình hiện hành: không đậm, màu phụ, cỡ và
khoảng cách tương ứng. Toàn bộ khối căn trái, giữ chiều rộng tự nhiên và co tối đa
theo chiều rộng màn hình.

Hợp đồng triển khai gồm ba phần độc lập: công cụ sinh TEX/PDF/SVG dùng chung; module
Lua/CSS tích hợp QMD dùng chung; JSON và khai báo build thuộc từng gói. Gói mới không
được sao chép Lua/CSS của R1-G01, chỉ cung cấp JSON canonical, gọi mã bảng trong QMD
và khai báo dữ liệu/tài sản trong cấu hình build.

Kiểm chứng bắt buộc gồm: schema, thứ tự mốc, số ô đồng nhất, quan hệ dấu–chiều,
PDF một trang không raster, font STIX, SVG có viewBox, khả năng đọc ở 1440/390 px
và nghiệm thu trực quan của con người.
