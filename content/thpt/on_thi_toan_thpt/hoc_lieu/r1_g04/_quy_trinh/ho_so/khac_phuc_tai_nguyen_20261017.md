# R1-G04 — nguyên nhân lệch đồ thị và bảng biến thiên

Ngày 17/10/2026. Phạm vi: bản sửa nguồn/HTML để chủ trì xem; không PDF học liệu, phát hành, commit hoặc push.

## Kết luận và trách nhiệm

Lỗi thuộc việc biên soạn, tích hợp và kiểm của agent. Công cụ dựng chạy đúng không chứng nhận việc chọn đúng vai trò/component. Lượt sửa bản thảo 0.2 trước đó chỉ thay Matplotlib bằng công cụ ZO Math; kết luận ấy chưa kiểm đủ tính nhất quán với sản phẩm đối chứng. Không quy nguyên nhân cho tài liệu tham khảo hoặc việc chủ trì chưa phát hiện khi đọc bản thảo.

## Chuỗi nguyên nhân và cách khép

| Tầng | Bằng chứng trước sửa tại mốc ebd68c9f | Nguyên nhân | Sửa nguồn và guard |
|---|---|---|---|
| Lập phương án tài nguyên | Hồ sơ rà 0.2 chỉ xác nhận profile 0.4/transparent-light cho toàn bộ hình; G01/G02 tách surface của hình trong bài và bìa | Không lập ma trận theo vai trò; đồng nhất tên công cụ/profile với component đã duyệt | 07/6.1.2, 02/2.5, mẫu/B19 và binding course-math-assets.json yêu cầu đối chứng cùng vai trò trước viết/chuyển QMD |
| Đồ thị | sinh_hinh.py dùng transparent-light cho cả bộ; adapter G04 tự tính --figure-em từ viewBox | Kế thừa cấu hình bìa và sizing riêng thay thành phần hình trong bài | Hình nội dung dùng paper, cùng production-figures.css, cỡ tự nhiên; bìa riêng giữ nguyên byte; guard role/surface/provenance và sizing |
| CSS runtime | body G04 chỉ có g02-preview; production-figures.css chọn .zo-web-2027-production | Nạp stylesheet nhưng thiếu lớp kích hoạt; mặc định ảnh max-width:100% vẫn thu nhỏ hình trên điện thoại | Bộ nối chung gắn lớp kích hoạt; cổng HTML và ca âm bỏ lớp; browser so kích thước ảnh thực với intrinsic width |
| Nguồn BBT | Có 35 bảng Markdown nhưng bang_bien_thien.json là danh sách rỗng; các bảng được ghi kind=variation trong binding bảng thường | Lấy G03 không có BBT làm mẫu tích hợp; phân loại được coi là đã dựng native | Chuyển dữ kiện sang JSON duy nhất, QMD chỉ gọi bằng ID; bộ nối bảng từ chối ordinary kind=variation; cổng nguồn chặn JSON rỗng/thiếu, bảng BBT viết tay |
| Phép kiểm | Chỉ đếm đủ bảng có loại, kiểm hash TEX/SVG và hình tải; không đòi .zo-variation-native hoặc class CSS hoạt động | Tiêu chí kiểm yếu hơn quy tắc hiện hành; báo PASS quá rộng | Kiểm dữ kiện từng ô, kiểu native, MathML, cùng component/cỡ/font/lưới trên desktop/mobile và thử âm |
| Diễn đạt giới hạn | Bộ dựng có một số token ghép đã hỗ trợ, nhưng chưa đầy đủ trường hợp số/vô cực trước/sau mũi tên | Tính năng công cụ còn thiếu không được phát hiện lúc lập phương án | Bổ sung tại máy BBT dùng chung, kiểm token cũ và HTML cũ nguyên byte; không mở máy dựng riêng trong gói |
| Phụ thuộc | Cache đồ thị G01 khóa cả mã dựng BBT vốn không sinh ra SVG đồ thị | Nhầm phụ thuộc hai loại tài nguyên, có thể kéo theo dựng hình/PDF không cần thiết | Tách phép kiểm cache graph khỏi dữ liệu/renderer native; vẫn kiểm dữ liệu BBT hiện hành khi gọi, vẫn từ chối đổi nguồn graph/style/phông; không sửa receipt cũ |

## Nội dung toán và các bản đã duyệt

- Giữ nguyên bản thảo 0.2 cùng tài nguyên bản thảo độc lập; không viết lại lịch sử duyệt.
- Ảnh bìa đã duyệt giữ nguyên SVG và manifest duyệt. Surface trong suốt của bìa không bị thay bằng surface hình trong bài.
- BBT được đổi biểu diễn từ các cột khoảng gộp sang lưới mốc–khoảng native. Bộ kiểm đối chiếu trực tiếp với bảng trong bản thảo đã duyệt: mốc, giá trị/giới hạn hai phía, chiều đi, dấu đã cho, điểm loại và số hàng; không thêm hàng đạo hàm hoặc tự suy giá trị đạo hàm tại điểm.
- Giữ ID bảng, đề, đáp án, chức năng, dãy số và nhãn cấp chứa. Toán ngoài các bảng di trú được kiểm riêng với bản thảo, dữ liệu BBT được kiểm bằng ngữ nghĩa thay cho việc đếm biểu thức.
- Hồ sơ/ảnh kiểm lịch sử giữ đúng bản cũ. Bộ hình hiện tại được kiểm ở kiem_hinh_noi_dung_20261017.json và xem_hinh_noi_dung_01–06.png. Không dùng ảnh sáu hình một tờ thay kiểm kích thước sử dụng trên trang.

## Vận hành cho lần sau

Nguồn sở hữu quy tắc: 07/6.1.2. Nguồn sở hữu trình tự: 02/2.5. Mẫu/B19, AGENTS và chuẩn QMD dẫn đúng hai nơi này; kit chỉ hiện thực/binding, gói sở hữu dữ kiện và hồ sơ. Cổng tự chạy qua CLI QMD, launcher Quarto và kiểm HTML; thử lỗi bằng zo_course_math_assets.py --self-test, gồm cả các trường hợp metadata/tệp vẫn tồn tại.

Đối chứng là sản phẩm G01/G02 hiện hành theo vai trò; G03 không có BBT nên không chứng nhận đường dựng BBT mới. Không lấy G01 làm quota số hình hoặc ép cấu hình tọa độ/nhãn riêng của một bài lên bài khác. Không nâng hiệu chỉnh cục bộ thành Design 0.5 hoặc thay kiến trúc học tập.

Nguồn công cụ dùng chung ngoài repo nội dung: E:/zo_math_graphics/variation/zo_variation_build.py, kiem_thu/kiem_tra_cong_cu.py và README.md. Thay đổi là hỗ trợ/kiểm token ghép, không nhân bản máy vào gói. Hồ sơ JSON kèm hash của các tệp này; một commit repo nội dung không tự bao gồm nguồn công cụ bên ngoài.

## Bản xem và trạng thái

[Bản HTML sửa](http://127.0.0.1:8877/_audit/g04_math_assets_20261017/g04-reading.html?r1-view=bai-hoc#VD02).

Bản xem nằm ở E:/zo_math/_audit/g04_math_assets_20261017/g04-reading.html; HTML và tài nguyên đầy đủ ở thư mục html cùng cấp. Nguồn duy nhất tại index.qmd, du_lieu và giao_dien của gói. Kết quả kiểm thực tế, giới hạn và hash ghi trong JSON cùng tên với hồ sơ này. Chủ trì chưa duyệt bản hiển thị sửa; chưa PDF học liệu, commit/push hoặc xuất bản. G01–G03 và website/PDF hiện hành được kiểm bảo toàn.
