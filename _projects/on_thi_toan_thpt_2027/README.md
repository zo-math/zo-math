# ZO Math — Ôn thi Toán THPT, Ấn bản ôn thi 2027

## 1. Định danh và thẩm quyền

- Repo canonical: `E:\zo_math`.
- Gốc quản trị nội bộ: `_projects/on_thi_toan_thpt_2027/`.
- Vùng học liệu tương lai: `content/thpt/on_thi_toan_thpt_2027/`, chỉ chứa nguồn QMD và tài nguyên học liệu.
- `README.md` này là bảng điều khiển canonical duy nhất, xác định tài liệu current, trạng thái gói và việc tiếp theo.

Mỗi tài liệu chỉ có một bản current; Git lưu lịch sử phiên bản. Không tạo thư mục `current/`, `published/`, `archive/`; không lưu toàn bộ hội thoại hoặc bản xuất trung gian.

Tài liệu nội bộ không được render hoặc publish. Ranh giới này phải được thiết lập bằng cấu hình thực tế ngay trước khi tạo nguồn học liệu QMD đầu tiên; hiện chưa chỉnh cấu hình dùng chung.

## 2. Danh mục tài liệu canonical

Các đường dẫn dưới đây tính từ gốc quản trị nội bộ. Toàn bộ năm tài sản ban đầu đã nhập và đối chiếu bằng tệp trong repo: Kế hoạch điều hành 0.6, bộ tài sản D0 v1.0, R1-G01/NB01, R1-G01/NB02 và R1-G01 — Khung sản phẩm sống. Không còn tài sản ban đầu chưa nhập. Xác nhận của chủ dự án được ghi riêng với kết quả đối chiếu tệp.

SHA-256 của Kế hoạch 0.6 đã đối chiếu khớp mã chủ dự án cung cấp: `ec5221120abde5a43bb8ed10d849970b63d46652177f8270d43b60d164471c86`. Tệp ghi đúng tên dự án, ấn bản ôn thi 2027 và phiên bản 0.6; nội dung Kế hoạch được giữ nguyên.

| Tài sản | Vai trò | Đường dẫn đích đã phê duyệt | Trạng thái đối chiếu | Chủ dự án xác nhận |
|---|---|---|---|---|
| Kế hoạch điều hành 0.6 | Điều hành | [Kế hoạch điều hành](dieu_hanh/ke_hoach_dieu_hanh.md) | đã nhập và đối chiếu | Bản canonical là 0.6; số phiên bản lưu trong tài liệu |
| D0 v1.0 | Bộ tài sản khảo sát và định vị đầu vào | [Điểm vào canonical D0](goi/D0/README.md) | đã nhập và đối chiếu; chi tiết kiểm chứng bên dưới | Chủ dự án xác nhận D0 đã hoàn tất v1.0 |
| R1-G01/NB01 | Nghiên cứu đã khóa | [NB01 — Đạo hàm và Đơn điệu](goi/R1-G01/nghien_cuu/NB01_dao_ham_va_don_dieu.md) | đã nhập và đối chiếu | Đạo hàm và Đơn điệu — đã khóa theo xác nhận của chủ dự án |
| R1-G01/NB02 | Nghiên cứu đã khóa | [NB02 — Đạo hàm và Cực trị](goi/R1-G01/nghien_cuu/NB02_dao_ham_va_cuc_tri.md) | đã nhập và đối chiếu | Đạo hàm và Cực trị — đã khóa theo xác nhận của chủ dự án |
| R1-G01/Khung sản phẩm sống | Tài liệu sống current, không phải tài liệu đã khóa | [Khung sản phẩm sống](goi/R1-G01/khung_san_pham_song.md) | đã nhập và đối chiếu; phiên bản 0.1 | Bản current của R1-G01 |

Đối chiếu NB01: tệp mang tiêu đề “BẢN GHI CHÚ KẾT TINH PHIÊN NGHIÊN CỨU 01”, nội dung về dấu đạo hàm và tính đơn điệu, phù hợp bản kết tinh Đạo hàm và Đơn điệu. Mã R1-G01/NB01 được xác định theo vị trí canonical và chỉ định của chủ dự án; tệp không ghi trực tiếp mã đầy đủ này. SHA-256 của bản đã nhập: `eadff3c4720aa757d9432465cd8615c5726c260fa1046bb0de74cbfbd03155fb`. Giữ nguyên nội dung và trạng thái đã khóa theo xác nhận của chủ dự án.

Đối chiếu NB02: tệp mang tiêu đề “BẢN KẾT TINH CUỐI PHIÊN: ĐẠO HÀM VÀ CỰC TRỊ (NB02)”, nội dung phù hợp chủ đề. Gói R1-G01 được xác định theo vị trí canonical và chỉ định của chủ dự án. SHA-256 của bản đã nhập: `1abea1c4feee91223c40e4f09439b0d22343c731cac8c63ee42a0c922571154a`. Giữ nguyên nội dung và trạng thái đã khóa theo xác nhận của chủ dự án.

Đối chiếu Khung sản phẩm sống: tệp ghi rõ R1-G01 — Kết nối đạo hàm, bảng biến thiên và đồ thị, phiên bản 0.1, cập nhật sau NB01–NB02. Đây là tài liệu sống current, không phải tài liệu đã khóa hoặc học liệu công bố. SHA-256 tại thời điểm nhập: `efb71112cf9847377faaeac436ac42d91dd3ef2fd0573e3ca8fd9676302879af`. Nội dung được giữ nguyên; đề xuất chuẩn bị NB03 trong tệp không thay thế việc tiếp theo hiện hành tại mục 5 theo chỉ thị của chủ dự án.

Kiểm chứng bộ D0 v1.0:

- 23/23 tệp thuộc [manifest gốc](goi/D0/MANIFEST_SHA256.txt) đã khớp SHA-256; không thiếu tệp được liệt kê.
- `MANIFEST_SHA256.txt` không tự liệt kê chính nó.
- [HUONG_DAN_SU_DUNG.md](goi/D0/HUONG_DAN_SU_DUNG.md) là tài liệu bổ sung ngoài manifest, được chủ dự án xác nhận hợp lệ và thêm sau khi manifest gốc được lập. SHA-256 đã đối chiếu: `7853f36db073b2cac392f7fa029e67c732976c704dab2c3dd02d59d087e670f1`.
- Tổng cộng 25 tệp: 23 tệp thuộc manifest, manifest và tài liệu bổ sung. Giữ nguyên manifest và toàn bộ tệp D0; kiểm chứng tính nguyên vẹn không thay thế nghiệm thu nội dung.

## 3. Trạng thái các gói

Toàn bộ năm tài sản ban đầu đã được đối chiếu bằng tệp trong repo. Trạng thái đã khóa của NB01, NB02 giữ theo xác nhận của chủ dự án; Khung sản phẩm sống là tài liệu sống current phiên bản 0.1.

| Phạm vi | Trạng thái |
|---|---|
| Điều hành | Kế hoạch canonical 0.6; tệp đã nhập và đối chiếu |
| D0 | Chủ dự án xác nhận đã hoàn tất v1.0; bộ tài sản đã nhập và đối chiếu |
| R1-G01 | Đang triển khai |
| R1-G01/NB01 | Đã khóa theo xác nhận của chủ dự án; đã nhập và đối chiếu |
| R1-G01/NB02 | Đã khóa theo xác nhận của chủ dự án; đã nhập và đối chiếu |
| R1-G01/Khung sản phẩm sống | Tài liệu sống current 0.1, không phải tài liệu đã khóa; đã nhập và đối chiếu |
| R1-G01/NB03 | Chưa mở |
| Học liệu R1-G01 | Chưa có học liệu được công bố chính thức |

## 4. Danh mục nguồn đang dùng

Kho nguồn cá nhân chỉ đọc: `E:\zo_math_ca_nhan\zo_math_on_thi_toan_thpt\nguon\`. Đây là vị trí truy cập cục bộ hiện hành, không phải thành phần của repo `E:\zo_math`. Tên tệp trong bảng được tính từ kho này; không sao chép PDF vào repo.

| ID | Tên chính thức | Cơ quan / nhà xuất bản | Tên tệp hiện tại | SHA-256 |
|---|---|---|---|---|
| SRC-CTGDPT-TOAN-2018 | Chương trình giáo dục phổ thông môn Toán | Bộ Giáo dục và Đào tạo; ban hành kèm Thông tư 32/2018/TT-BGDĐT ngày 26/12/2018 | `Chuong trinh giao duc pho thong mon Toan 2018.pdf` | `f35d34ff84da2ca3f9ab72d5d67482ada414684b611deea98c4b329801b661ab` |
| SRC-SGK12-KNTT-T1 | Toán 12 — Tập Một, Kết nối tri thức với cuộc sống | Nhà xuất bản Giáo dục Việt Nam | `Toan 12. Tap 1. Ket noi tri thuc voi cuoc song.pdf` | `faeb554bea9cf81189c5e790b1b1edb42f50b3648694acc80dc99682ada3f1fd` |
| SRC-SGK12-KNTT-T2 | Toán 12 — Tập Hai, Kết nối tri thức với cuộc sống | Nhà xuất bản Giáo dục Việt Nam | `Toan 12. Tap 2. Ket noi tri thuc voi cuoc song.pdf` | `3c642f2e80d86d699ea62bbcabd0c3074fd5118def96e4b3b8ce1f9ead7f97bb` |

Đã đối chiếu ngày 2026-09-13: chương trình là bản đầy đủ 123 trang được chủ dự án chọn; không đăng ký bản rút gọn 38 trang. Hai SGK được nhận diện trực quan qua bìa, trang tên sách và trang thông tin xuất bản: đúng bộ, lớp và tập; tổng chủ biên Hà Huy Khoái; bìa và trang tên sách ghi “Bản mẫu — Tháng 1-2024”, trang xuất bản ghi bản quyền 2024, một số trường in/ISBN còn để trống. Tập Một có 104 trang PDF, Tập Hai có 99 trang PDF; không coi đây là bản in thương mại đã xác minh ISBN đầy đủ.

Ba tệp với SHA-256 trên là các bản tham chiếu hiện hành cho công việc từ NB03 trở đi. Đối với NB01–NB02, các tài liệu chính thức tương ứng đã được dùng theo xác nhận của chủ dự án; chưa có bằng chứng rằng các SHA-256 hiện tại chính là các bản tệp đã nạp trước đây.

## 5. Việc tiếp theo duy nhất

Chuẩn bị R1-G01/NB03 trong một phiên chat và một Notebook mới, dựa trên Khung sản phẩm sống current.

Điều kiện hoàn tất:

- Chuẩn bị câu hỏi và mục tiêu NB03 theo Khung sản phẩm sống current.
- Xác định phạm vi đọc từ ba bản tham chiếu hiện hành tại mục 4 để dùng trong phiên chat và Notebook mới.
- Giữ nguyên các bản kết tinh NB01–NB02 đã khóa; chưa chuyển sang sản xuất học liệu.
