# ZO Math — Ôn thi Toán THPT, Ấn bản ôn thi 2027

## 1. Định danh và thẩm quyền

- Repo canonical: `E:\zo_math`.
- Gốc quản trị nội bộ: `_projects/on_thi_toan_thpt_2027/`.
- Vùng học liệu tương lai: `content/thpt/on_thi_toan_thpt_2027/`, chỉ chứa nguồn QMD và tài nguyên học liệu.
- `README.md` này là bảng điều khiển canonical duy nhất, xác định tài liệu current, trạng thái gói và việc tiếp theo.

Mỗi tài liệu chỉ có một bản current; Git lưu lịch sử phiên bản. Không tạo thư mục `current/`, `published/`, `archive/`; không lưu toàn bộ hội thoại hoặc bản xuất trung gian.

Tài liệu nội bộ không được render hoặc publish. Ranh giới này phải được thiết lập bằng cấu hình thực tế ngay trước khi tạo nguồn học liệu QMD đầu tiên; hiện chưa chỉnh cấu hình dùng chung.

## 2. Danh mục tài liệu canonical

Các đường dẫn dưới đây tính từ gốc quản trị nội bộ. Kế hoạch điều hành 0.6 đã nhập và đối chiếu bằng tệp trong repo; bốn tài sản còn lại chưa nhập và chưa nhận tệp để đối chiếu. Chỉ tài liệu đã tồn tại mới có liên kết; xác nhận của chủ dự án được ghi riêng với kết quả đối chiếu tệp.

SHA-256 của Kế hoạch 0.6 đã đối chiếu khớp mã chủ dự án cung cấp: `ec5221120abde5a43bb8ed10d849970b63d46652177f8270d43b60d164471c86`. Tệp ghi đúng tên dự án, ấn bản ôn thi 2027 và phiên bản 0.6; nội dung Kế hoạch được giữ nguyên.

| Tài sản | Vai trò | Đường dẫn đích đã phê duyệt | Trạng thái đối chiếu | Chủ dự án xác nhận |
|---|---|---|---|---|
| Kế hoạch điều hành 0.6 | Điều hành | [Kế hoạch điều hành](dieu_hanh/ke_hoach_dieu_hanh.md) | đã nhập và đối chiếu | Bản canonical là 0.6; số phiên bản lưu trong tài liệu |
| D0 v1.0 | Hồ sơ gói nền tảng | `goi/D0/D0.md` nếu là một tài liệu; `goi/D0/` nếu là bộ tài sản | chưa nhận tệp để đối chiếu | Đã hoàn tất v1.0; nếu là bộ tài sản, phải đối chiếu thành phần trước khi chốt từng đường dẫn |
| R1-G01/NB01 | Nghiên cứu đã khóa | `goi/R1-G01/nghien_cuu/NB01_dao_ham_va_don_dieu.md` | chưa nhận tệp để đối chiếu | Đạo hàm và Đơn điệu — đã khóa |
| R1-G01/NB02 | Nghiên cứu đã khóa | `goi/R1-G01/nghien_cuu/NB02_dao_ham_va_cuc_tri.md` | chưa nhận tệp để đối chiếu | Đạo hàm và Cực trị — đã khóa |
| R1-G01/Khung sản phẩm sống | Tài liệu sống | `goi/R1-G01/khung_san_pham_song.md` | chưa nhận tệp để đối chiếu | Đã có bản đầu |

## 3. Trạng thái các gói

Kế hoạch 0.6 đã được đối chiếu bằng tệp trong repo. Các trạng thái gói còn lại giữ theo xác nhận của chủ dự án; chưa đối chiếu bằng tệp tài sản tương ứng.

| Phạm vi | Trạng thái |
|---|---|
| Điều hành | Kế hoạch canonical 0.6; tệp đã nhập và đối chiếu |
| D0 | Hoàn tất v1.0; tệp hoặc bộ tài sản chưa được nhập và đối chiếu |
| R1-G01 | Đang triển khai |
| R1-G01/NB01 và NB02 | Đã khóa; chưa có tệp canonical trong repo |
| R1-G01/Khung sản phẩm sống | Đã có bản đầu; chưa được nhập |
| R1-G01/NB03 | Chưa mở |
| Học liệu R1-G01 | Chưa có học liệu được công bố chính thức |

## 4. Danh mục nguồn đang dùng

Chưa đăng ký nguồn canonical. Danh mục sẽ được đăng ký sau khi đối chiếu nguồn hiện có trong repo và bộ nguồn chính thức của dự án, ghi tên nguồn, xuất xứ, vị trí canonical hoặc địa chỉ chính thức và SHA-256 khi có bản tệp xác định. Tái sử dụng nguồn bằng liên kết; không tự sao chép PDF có giới hạn phân phối. Chưa sao chép PDF hoặc tạo thư mục nguồn trong giai đoạn này.

## 5. Việc tiếp theo duy nhất

Tiếp nhận và xác minh D0 v1.0 để nhập vào `_projects/on_thi_toan_thpt_2027/goi/D0/`.

Điều kiện hoàn tất:

- Nhận được tệp hoặc bộ tài sản thực tế.
- Chủ dự án xác nhận đúng D0 đã hoàn tất v1.0.
- Kiểm tra tên dự án, phiên bản, nội dung, phụ lục và tính đầy đủ của bộ tài sản; chốt từng đường dẫn đích trước khi nhập.
- Tính SHA-256 của từng tệp đầu vào.
- Chưa biên tập nội dung trong bước tiếp nhận.
