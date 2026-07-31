# Chỉ dẫn cho agent trong dự án 100+ Hàm số

> Đây là tài liệu điều phối nội bộ cho dự án **100+ Hàm số: Sự biến thiên và đồ thị**.
>
> Đây không phải là nội dung xuất bản dành cho người đọc ZO Math.

## Phạm vi và quan hệ với chỉ dẫn cấp gốc

Tệp này áp dụng cho toàn bộ thư mục hiện tại và các thư mục con.

Mọi agent làm việc trong phạm vi này trước hết phải tuân thủ `AGENTS.md` ở gốc repository cùng hai tài liệu bắt buộc được dẫn chiếu tại đó. Tệp này chỉ bổ sung các chỉ dẫn chuyên biệt cho dự án 100+ Hàm số; không làm mất hiệu lực những quy định cấp gốc nếu không có tuyên bố thay thế rõ ràng.

## Cổng vào quy trình tạo bài khảo sát hàm số

Khi nhiệm vụ yêu cầu tạo mới, viết lại, hoàn thiện hoặc kiểm định một bài khảo sát về một hàm số cụ thể, trước khi viết nội dung bài phải đọc và tuân thủ:

- `_quy_trinh/quy_trinh_tao_bai_ham_so.md`;
- `_quy_trinh/quy_chuan_khao_sat_ham_so.md`;
- `_quy_trinh/quy_chuan_ki_thuat_bai_ham_so_qmd.md`.

Ba tài liệu có vai trò phân biệt:

- quy trình điều phối các giai đoạn, sản phẩm, điểm kiểm soát và bàn giao;
- quy chuẩn khảo sát điều khiển nội dung toán học, trục nhận thức và kiến trúc bài;
- quy chuẩn kĩ thuật điều khiển hợp đồng QMD, tài nguyên, HTML, PDF và kiểm định đầu ra.

Phải sử dụng:

- `_quy_trinh/ho_so_san_xuat_mac_dinh.yml` để khởi tạo hồ sơ sản xuất theo cách quy trình quy định;
- `_quy_trinh/mau_ki_thuat_qmd.qmd` làm khung kĩ thuật khi tạo tệp QMD mới.

Không bắt đầu bằng một mục lục khảo sát cố định. Hồ sơ khảo sát và đề cương vận hành phải được hình thành trước bài viết theo đúng các điểm kiểm soát của quy trình.

`mau_ki_thuat_qmd.qmd` hiện thực hóa phần khung ban đầu của quy chuẩn kĩ thuật. Tệp này không phải mẫu nội dung để điền lần lượt và không áp đặt cùng một kiến trúc nhận thức cho mọi hàm số. Khi mẫu và quy chuẩn kĩ thuật không thống nhất, phải báo sai lệch và sửa trong một nhiệm vụ cập nhật tài liệu điều khiển; không âm thầm chọn một bên.

## Tài liệu chuyên trách được kích hoạt theo điều kiện

Khi nhiệm vụ tạo mới, hoàn thiện hoặc kiểm định một bài QMD trong dự án này, phải đọc và tuân thủ:

- `../../../../quy_trinh_xay_dung/huong_dan_su_dung_khoi_noi_dung.md`.

Phải kiểm tra cả việc nội dung có thực sự cần tách thành khối hay không, trạng thái mở cố định hoặc thu gọn, màu theo chức năng và cú pháp lớp hiện hành. Các lớp cũ được giữ để tương thích không được xem là chuẩn cho nội dung mới. Không suy diễn cách dùng khối chỉ từ một bài tham chiếu.

Khi nhiệm vụ có đồ thị TikZ/PGFPlots, phải đọc và tuân thủ:

- `../../../../quy_trinh_xay_dung/quy_chuan_do_thi_sinh_ma_nguon_tikz_pgfplots.md`.

Khi người dùng hoặc hồ sơ sản xuất chỉ định một phong cách viết, phải đọc:

- `../../../../quy_trinh_xay_dung/phong_cach_viet/index.md`;
- tài liệu chuyên biệt của phong cách được chỉ định.

Phong cách **Học thuật tĩnh tại** chỉ được áp dụng khi đã được chỉ định rõ. Không mặc định áp dụng phong cách này cho toàn dự án.

## Vai trò của Khung khảo sát hàm số

`khung_khao_sat_ham_so.qmd` là trang nội dung công khai dành cho người đọc. Tệp này không phải mẫu kĩ thuật, không phải hồ sơ sản xuất và không thay thế `quy_chuan_khao_sat_ham_so.md` trong việc điều khiển agent tạo bài.

Khi nhiệm vụ chỉ liên quan đến biên tập hoặc xuất bản trang Khung khảo sát hàm số, không tự động kích hoạt toàn bộ quy trình sản xuất một bài về hàm số cụ thể.

## Giới hạn vận hành

Không suy diễn quy chuẩn từ một bài mẫu và không sao chép máy móc kiến trúc nội dung của bài đã có. Bài mẫu chỉ được dùng trong đúng vai trò tham chiếu được nhiệm vụ hoặc quy trình xác định.

Khi phát hiện vấn đề trong quy trình, quy chuẩn, mẫu kĩ thuật hoặc phong cách viết, phải ghi nhận và báo cáo. Không tự ý sửa các tài liệu điều khiển ấy trong phạm vi một nhiệm vụ sản xuất bài, trừ khi người dùng giao rõ việc cập nhật chúng.

Không sửa tệp ngoài phạm vi, không staging và không commit nếu người dùng chưa yêu cầu rõ.
