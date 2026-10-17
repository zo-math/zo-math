# Rà soát trình bày R1-G04 — bản thảo 0.2

Ngày 17/10/2026. Căn cứ trực tiếp: chủ trì phản hồi bản 0.1 vi phạm trình bày nội dung và ngôn ngữ thiết kế. Kết luận “Đạt” trình bày/hình của lượt 0.1 không được dùng chứng nhận bản này.

- [Bản thảo đang sửa duy nhất](../ban_thao/noi_dung.md).
- [Dữ liệu kiểm mới](ra_soat_trinh_bay_20261017.json).
- [Kiểm công cụ đồ thị ZO Math](kiem_hinh_zo_math_20261017.json).
- Bảng kiểm trước viết/kiểm lượt 0.1: [bằng chứng cũ](bang_kiem_ban_thao_20261017.md); không sửa lại số/hash cũ để biến thành kết quả 0.2.

## Nguyên nhân đã xác định và phần sửa

| Phát hiện | Căn cứ hiện hành đã bị bỏ sót | Hiệu chỉnh ở 0.2 |
|---|---|---|
| Dẫn “theo SGK”, “SGK nêu…” trong lời giảng; kể căn cứ biên soạn vào chính văn | Quy chuẩn gói, mục Công thức và nguồn đối chiếu: .zo-source-note; nguyên tắc tách nội dung học và hồ sơ | Phát biểu trực tiếp, năm chú thích nguồn chuẩn sau phần tương ứng; cuối bài là thông tin thư mục |
| Màu đỏ/xám, phông, nét, vạch và khung đồ thị được đặt bằng chương trình Matplotlib riêng | 07/6.1, profile 0.4 đã tích hợp; công cụ đồ thị ZO Math | Thay bộ sinh tại chỗ bằng adapter ZO Math, STIX Two, style 0.4, nền transparent-light; không còn chương trình vẽ Matplotlib độc lập |
| Gọi hình là “nháp” rồi để ngoại lệ diện mạo tới bước QMD | Không có chỉ thị cho phép ngoại lệ này | Dựng và xem đủ 35 hình bằng công cụ/profile hiện hành ngay trong bản thảo |
| Kiểm ngoặc chỉ đếm cân bằng nên bỏ lọt 13 cặp ngoặc chứa căn/phân số; số hiệu văn bản bị đưa vào math mode với dấu chia | Quy chuẩn dấu ngoặc LaTeX và guard zo_math_notation/math_errors đã có | Sửa đúng 13 cặp; số hiệu Thông tư là thông tin thư mục; gọi guard thật, không chỉ đếm dấu |
| Lời giải dùng details trần, chưa có vai trò solution | Hướng dẫn khối nội dung; 07/5.3 | 28 lời giải dùng khối xám/solution, mặc định đóng; giữ cặp đề/đáp án và ID |
| Chính văn nói việc đặt Khởi động/Gợi mở, đánh số, không lập nhóm đáp án | 07 phân biệt nội dung người học với lí do biên tập | Đổi thành hướng dẫn hành động học hoặc bỏ lời giải thích sản xuất |

Đây là sửa theo quy tắc/chỉ thị đã có, không đổi phạm vi B21, năm mục Bài học, kiến trúc QD_033 hoặc hệ nhãn QD_025. Đề toán, kết quả tính, ID và tuyến hỗ trợ được bảo toàn; chỉ sửa kí pháp/biên tập và hình.

## Đưa vào vận hành để tránh lặp

- 02/1.4 yêu cầu nạp quy cách chú thích, ngoặc, khối và hình trước viết/rà.
- 07/6.3 làm rõ cách viết chính văn và việc hình nháp cũng phải theo thiết kế.
- Mẫu nội dung tăng từ 1.0 lên 1.1; mẫu bảng kiểm từ 1.1 lên 1.2. B05 kiểm cách dẫn nguồn; B18 phải dùng guard kí pháp; B19 kiểm style/phông/nét/vạch/nền/cỡ và hình thực, không chỉ kiểm toán/vector.
- 04 ghi phản hồi/nguồn lỗi và phạm vi hiệu chỉnh; 08 nối đúng chủ sở hữu. Giữ các mốc mẫu cũ làm lịch sử; không sửa sản phẩm G01–G03.
- Công việc hiện hành và bước tiếp theo được ghi duy nhất tại 03; README gói chỉ dẫn vào bản đang xem và hồ sơ.

## Đối chiếu bản sửa

| Mục kiểm chịu ảnh hưởng | Kết quả/vị trí | Phạm vi |
|---|---|---|
| A02/A07 | Đã nạp chuẩn gói về nguồn, quy chuẩn ngoặc, hướng dẫn khối, profile 0.4 và công cụ; nguồn/hash của lượt này trong JSON mới | Áp dụng hồi cứu lúc sửa 0.2, không tuyên bố đã đọc đủ trước viết 0.1 |
| B04/B07 | GM01–05 vẫn thuộc bh-01–05; mục/tiểu mục, nhãn/số và các ID giữ nguyên | Không tạo hệ đánh số mới để chiều parser QMD |
| B05/B20 | Năm .zo-source-note sau phát biểu; không còn câu dẫn SGK/Chương trình trong chính văn; tên tài liệu đầy đủ, trang rõ | Xuất xứ vẫn được giữ và có thể đối chiếu |
| B06/B17 | 28 cặp đề–lời giải giữ nguyên; đáp án trong solution mặc định đóng; link nội bộ/ảnh không thiếu | Chưa có kiểm tương tác HTML |
| B18 | Guard math_errors không còn lỗi; các biểu thức chuẩn hóa không đổi nghĩa toán | Không dùng outline_errors của G01/G02 để áp máy móc vào heading/anchor Markdown của bản thảo |
| B19 | 35 SVG dựng qua công cụ ZO Math với --style 0.4 --surface transparent-light --check; STIX Text/Math, vector, nền trong suốt. Xem tất cả sáu ảnh kiểm, dời nhãn tâm khỏi đường xiên ở nguồn rồi kiểm lại phần ảnh hưởng | Chưa phải chủ trì duyệt hình; không phải nghiệm thu dàn trang toàn trang |
| B21/B22 | Một bản 0.2, không QMD/HTML/PDF học liệu; không commit/push/xuất bản; báo cáo cũ không được kế thừa làm kết luận hiện hành | Chờ chủ trì xem bản sửa |

Bảng biến thiên Markdown giữ dữ kiện của bản thảo. Khi chuyển QMD theo quyền được giao sau này, áp ngôn ngữ bảng/native theo QD_030 và kiểm đúng đầu ra; không gọi bản Markdown là một bản dàn trang web đã đạt.

## Hình để xem thực tế

[Nhóm 1](xem_hinh_01.png) · [Nhóm 2](xem_hinh_02.png) · [Nhóm 3](xem_hinh_03.png) · [Nhóm 4](xem_hinh_04.png) · [Nhóm 5](xem_hinh_05.png) · [Nhóm 6](xem_hinh_06.png).

Nguồn dữ liệu và điều phối ở ban_thao/hinh/du_lieu_hinh.json và sinh_hinh.py. TEX là nguồn dựng được sinh từ dữ liệu, SVG là đầu ra; không sửa tay TEX/SVG. Hình có cửa sổ/tỉ lệ được khai báo, chỉ giữ vạch/điểm phục vụ đọc, không dùng lưới và bảng công thức lặp để lấp hình. Tâm trên phân thức dùng dấu chéo, không đặt điểm đặc làm giá trị tại điểm loại.

Công cụ đồ thị cần PDF vector trung gian để chuyển SVG và kiểm font/vector. PDF trung gian được tạo trong vùng tạm của công cụ và đã dọn; thư mục bản thảo không giữ PDF. Không dựng PDF học liệu hoặc HTML ở lượt này.

## Giới hạn và trạng thái

Đã sửa và tự kiểm phần trình bày/nội dung chịu ảnh hưởng. Bản 0.2 chưa được chủ trì duyệt. Chưa chuyển QMD; chưa dựng HTML/PDF học liệu, chọn/duyệt ảnh đại diện, kiểm trình duyệt hoặc phát hành. Kiểm máy và tự rà của người biên soạn không là phản biện toán độc lập.
