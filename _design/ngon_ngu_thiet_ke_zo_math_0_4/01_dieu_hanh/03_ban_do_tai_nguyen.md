# Bản đồ tài nguyên

| Bạn cần | Tệp/thư mục trong bộ | Cách dùng |
|---|---|---|
| Điểm bắt đầu | [00_BAT_DAU_O_DAY.md](../00_BAT_DAU_O_DAY.md) | Đọc trước, chỉ một đường khởi động |
| Giao AI làm việc | [Lệnh khởi động](00_LENH_KHOI_DONG_AI.txt) | Sao chép vào Codex ở repo web |
| Điều đã duyệt/còn thử | [Sổ yêu cầu](02_so_quyet_dinh.md) | Tra trạng thái và căn cứ |
| Toàn bộ nguồn được gửi | [Mục lục 30 đầu vào](../06_nguon/00_muc_luc.md) | Đọc sâu khi cần, không đọc lại mọi phiên |
| Giá trị màu | [color_system.json](../03_du_lieu/color_system.json) | Nguồn dữ liệu áp dụng; giá trị giữ từ 0.4 |
| Đổi tên token | [token_migration.json](../03_du_lieu/token_migration.json) | Chỉ dùng các ánh xạ có thật |
| Quy tắc cho phần mềm | [quy_tac.json](../03_du_lieu/quy_tac.json) | Đọc cùng trạng thái và evidence |
| Tuyến áp dụng | [ho_so_ap_dung.json](../03_du_lieu/ho_so_ap_dung.json) | Chọn hướng dẫn theo công cụ; chưa là plugin |
| Logo SVG | [Logo ngang](../07_mau_thi_giac/logos/horizontal_color.svg), [logo đứng](../07_mau_thi_giac/logos/stack_color.svg) | Nguồn vector ứng viên; các bản còn lại trong cùng thư mục |
| Dấu nhấn | [motif.svg](../07_mau_thi_giac/logos/motif.svg) | Hình học đề xuất, màu mới |
| Hình toán | [Danh mục tài sản](../03_du_lieu/tai_san.json) | graphics chứa SVG/PNG; source/tex chứa nguồn TeX |
| Bảng native | [Bộ mẫu](../07_mau_thi_giac/index.html) | Mục Bảng/Biến thiên; tables chứa HTML/QMD/TeX/PDF/PNG |
| Ảnh bìa | [Danh mục kích thước](../07_mau_thi_giac/design/distribution.json) | social; retained_0_2 là đối chiếu lịch sử |
| Video và âm | [Clip dọc](../07_mau_thi_giac/media/motion_doc.mp4), [cue mở](../07_mau_thi_giac/media/cue_focus.wav) | Mẫu để xem/nghe; không phải chuẩn âm đã chốt |
| Quy chuẩn PDF có hình | [ZO_Math_Quy_chuan_0_4.pdf](../07_mau_thi_giac/pdf/ZO_Math_Quy_chuan_0_4.pdf) | 14 trang mẫu và lí do |
| Học liệu PDF mẫu | [Danh mục tám PDF](../07_mau_thi_giac/design/pdf_editions.json) | Bìa/kết 0.4, ruột nguồn v1.3 |
| Mã dựng mẫu | [BUILD.txt](../07_mau_thi_giac/source/BUILD.txt) | Tham khảo; một số đường dẫn phụ thuộc môi trường nghiên cứu |
| Công việc hiện tại | [cong_viec_hien_tai.json](../09_nhat_ki/cong_viec_hien_tai.json) | Cập nhật cuối phiên |

## Tìm trong kho

`python 08_cong_cu/zo_design.py find ten_can_tim` từ gốc bộ. Danh mục tài sản ghi đường dẫn, loại, vai trò, trạng thái và hash. Các bản PNG/PDF/MP4 là đầu ra; nguồn TeX/SVG/script còn lại giúp AI thiết kế adapter, không mặc định chạy nguyên script mẫu vào repo sản xuất.

Bộ mẫu 0.4 và source_bundle được giữ nguyên cấu trúc nội bộ. Các tài liệu lịch sử có thể trỏ ra ngoài bộ; mục lục nguồn và lệnh find giúp tìm bản được gửi, nhưng không tạo lại tài liệu chưa có.
