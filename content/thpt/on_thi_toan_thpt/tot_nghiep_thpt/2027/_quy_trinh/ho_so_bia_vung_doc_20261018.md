# Kiểm kê bìa và vùng đọc — 18/10/2026

Phạm vi: sáu trang hiện có, đọc HTML tại `_audit/html_refresh_20261018/html`, sửa nguồn canonical; không dựng HTML/PDF. Ảnh chụp của chủ trì là bằng chứng triệu chứng, không là nguồn nội dung toán.

| Trang | Bìa hiện có | Vùng đọc và xử lí nguồn |
|---|---|---|
| Nhà khóa | Không có breadcrumb/nút bài học kiểu học liệu | Giữ các vùng biên tập Nhà theo giới thiệu, danh mục, cách học, kiến thức và FAQ; không áp giấy R1; giữ CTA đúng chức năng. |
| Khảo sát đầu vào | Breadcrumb cũ; không có nút thừa | Đổi nhãn từ mẫu chung. Giữ map hướng dẫn/từng câu khảo sát/đối chiếu/định hướng; mỗi câu đã có vùng trọn vẹn. |
| Đơn điệu và cực trị | Breadcrumb cũ; có nút thừa | Sửa binding bìa. Tách bốn nhiệm vụ Khởi động và bốn lời giải tương ứng đang gom giấy; giữ hướng dẫn/nhãn theo ngữ cảnh. |
| Giá trị lớn nhất và giá trị nhỏ nhất | Breadcrumb cũ; có nút thừa | Sửa bộ sinh. Bỏ quy tắc gom Khởi động theo G01 cũ; tách ba nhiệm vụ và ba lời giải tương ứng. |
| Đường tiệm cận | Breadcrumb cũ; có nút thừa | Sửa bộ sinh. Nhiệm vụ độc lập đã riêng vùng, giữ map; hai xác nhận trong một thẻ Ôn nền giữ theo tài nguyên hoàn chỉnh. |
| Khảo sát sự biến thiên và vẽ đồ thị của hàm số | Breadcrumb cũ; có nút thừa | Sửa bộ sinh. Giữ phân vùng nhiệm vụ, ví dụ và Gợi mở theo mục kiến thức. |

## Căn nguyên và sửa dùng chung

G01 dùng cây bố cục lịch sử; G02 khai báo nguyên văn “Cùng lượt Khởi động như G01… các nhiệm vụ cùng một vùng”; G03/G04 dùng chia theo semantic task. Quy tắc chung chưa có kiểm chống nhiều nhiệm vụ độc lập cùng giấy nên hai cách cùng tồn tại. Sửa chỉ dẫn G02, bổ sung hiện thực/guard `scripts/zo_course_reading_regions.py`, gọi sau giải mã nội dung qua `apply_editorial_policy` cho bốn gói. Giữ ID trên các phần tử gốc, không sửa nội dung hay receipt; thứ tự duyệt ID của container có thể đổi khi tiêu đề nhóm được đặt vào vùng đầu tiên, tập ID/đích liên kết và thứ tự chữ/toán giữ nguyên.

Chuỗi breadcrumb cũ ở mẫu dùng chung và bản đồ G01; CTA lại nằm riêng trong binding G01/bộ sinh G02–G04. Đã sửa đúng các nguồn đó, cả nhãn về khóa trong bộ sinh trang cổng. Trang chủ hiện hành không dùng nhánh Home prototype đã nghỉ; không mở lại luồng ấy hoặc sửa chứng cứ lịch sử.

Quy tắc mới ghi tại 07/6.1.3, hợp đồng kit và quy trình 02. Mỗi nhiệm vụ độc lập cùng hành động là một vùng; hướng dẫn chung riêng khi có nội dung, heading đơn độc đi cùng nội dung đầu. Ví dụ phụ thuộc, Gợi mở theo mục và thẻ Ôn nền có đối chiếu tại chỗ không bị chia vụn. Không ép mọi trang cùng số vùng.

## Kiểm và giới hạn

Hồi quy nguồn/DOM đọc bốn HTML cũ, giữ chữ, MathML, tập ID, hình và liên kết; thử phân vùng trong bộ nhớ và tính lặp không đổi. Mô phỏng G01: 174 → 180 vùng; G02: 161 → 167; G03: 147 giữ nguyên; G04: 113 giữ nguyên. Đây là kết quả mô phỏng, không là HTML mới hoặc chỉ tiêu số vùng. Nhà không dùng giấy R1, D0 giữ 58 vùng.

Trạng thái: sửa nguồn; kết quả kiểm nguồn ghi ở `_audit/reading_regions_20261018/`. Chưa dựng/duyệt HTML mới, chưa dựng PDF, chưa commit hoặc xuất bản. Các bản xem đang mở vẫn là bản trước lượt sửa này.

Kết quả cuối lượt: kiểm nguồn sáu trang đạt (`source-check-final.json`); hồi quy vùng đọc 34/34; nhãn ngữ cảnh sau phân vùng 1424/1424; tham chiếu đi–về 58/58; điều hành 242/242. Đối chiếu 644 tệp thành phẩm được bảo vệ: không đổi. Các thử toàn bộ chính sách biên tập trên HTML cũ bị dừng khi bước rà nhãn kéo dài, không dùng làm bằng chứng đạt; đã thay bằng kiểm đúng phần chịu ảnh hưởng (chia vùng rồi ghép/kiểm nhãn) cho cả bốn gói. Chưa kiểm bộ dựng sản xuất hoặc trình duyệt trên HTML mới vì chưa được dựng. Tổng hợp: `_audit/reading_regions_20261018/final.json`.
