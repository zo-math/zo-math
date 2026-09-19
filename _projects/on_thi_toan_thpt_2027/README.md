# ZO Math — Ôn thi Toán THPT, Ấn bản ôn thi 2027

## 1. Định danh và thẩm quyền

- Repository chứa dự án: `E:\zo_math`.
- Kho chuẩn duy nhất của dự án: `E:\zo_math\_projects\on_thi_toan_thpt_2027`.
- Vùng học liệu tương lai: `content/thpt/on_thi_toan_thpt_2027/`, chỉ chứa nguồn QMD và tài nguyên học liệu.
- `README.md` này là bảng điều khiển canonical duy nhất, xác định tài liệu current, trạng thái gói và việc tiếp theo.
- Đơn vị quản lí chính thức là các gói học liệu ngang cấp: D0, R1-G01, R1-G02, R1-G03 và các gói tiếp theo.

Mỗi tài liệu chỉ có một bản current; Git lưu lịch sử phiên bản. Không tạo thư mục `current/`, `published/`, `archive/`; không lưu toàn bộ hội thoại hoặc bản xuất trung gian.

Tài liệu nội bộ không được render hoặc publish. Ranh giới này phải được thiết lập bằng cấu hình thực tế ngay trước khi tạo nguồn học liệu QMD đầu tiên; hiện chưa chỉnh cấu hình dùng chung.

## 2. Danh mục tài liệu canonical

Sổ canonical: [Truyền thông quá trình](truyen_thong_qua_trinh.md). Nội dung quá trình đã công khai chưa phải học liệu chính thức và không làm thay đổi trạng thái công bố học liệu R1-G01.

Các đường dẫn dưới đây tính từ gốc quản trị nội bộ. Kế hoạch điều hành 0.6 và D0 v1.0 giữ trạng thái đã đối chiếu. R1-G01 đã được hợp nhất thành một gói tự chứa: kết quả nghiên cứu nằm trong hồ sơ chung của gói; nguồn sản xuất và các đầu ra ứng viên v1.1 nằm cùng gói.

SHA-256 của Kế hoạch 0.6 đã đối chiếu khớp mã chủ dự án cung cấp: `ec5221120abde5a43bb8ed10d849970b63d46652177f8270d43b60d164471c86`. Tệp ghi đúng tên dự án, ấn bản ôn thi 2027 và phiên bản 0.6; nội dung Kế hoạch được giữ nguyên.

| Tài sản | Vai trò | Đường dẫn đích đã phê duyệt | Trạng thái đối chiếu | Chủ dự án xác nhận |
|---|---|---|---|---|
| Kế hoạch điều hành 0.6 | Điều hành | [Kế hoạch điều hành](dieu_hanh/ke_hoach_dieu_hanh.md) | đã nhập và đối chiếu | Bản canonical là 0.6; số phiên bản lưu trong tài liệu |
| D0 v1.0 | Bộ tài sản khảo sát và định vị đầu vào | [Điểm vào canonical D0](goi/D0/README.md) | đã nhập và đối chiếu; chi tiết kiểm chứng bên dưới | Chủ dự án xác nhận D0 đã hoàn tất v1.0 |
| R1-G01 | Hồ sơ, nguồn sản xuất và đầu ra ứng viên của gói | [Điểm vào canonical R1-G01](goi/R1-G01/README.md) | đã hợp nhất và tái sinh từ nguồn trong gói | Nghiên cứu đã kết tinh; v1.0 đã đọc và tiếp nhận góp ý; v1.1 đang thẩm định, chưa duyệt phát hành |

[Hồ sơ R1-G01](goi/R1-G01/R1-G01_ho_so.md) giữ phạm vi, kết quả nghiên cứu, quyết định biên tập, nguồn và lịch sử trạng thái ở cấp gói. Các kết quả nghiên cứu tiền nhiệm đã được đối chiếu với đề cương, nội dung nền và hồ sơ biên tập trước khi hòa nhập; công cụ hoặc phiên nghiên cứu không còn là đơn vị quản lí.

Kiểm chứng bộ D0 v1.0:

- 23/23 tệp thuộc [manifest gốc](goi/D0/MANIFEST_SHA256.txt) đã khớp SHA-256; không thiếu tệp được liệt kê.
- `MANIFEST_SHA256.txt` không tự liệt kê chính nó.
- [HUONG_DAN_SU_DUNG.md](goi/D0/HUONG_DAN_SU_DUNG.md) là tài liệu bổ sung ngoài manifest, được chủ dự án xác nhận hợp lệ và thêm sau khi manifest gốc được lập. SHA-256 đã đối chiếu: `7853f36db073b2cac392f7fa029e67c732976c704dab2c3dd02d59d087e670f1`.
- Tổng cộng 25 tệp: 23 tệp thuộc manifest, manifest và tài liệu bổ sung. Giữ nguyên manifest và toàn bộ tệp D0; kiểm chứng tính nguyên vẹn không thay thế nghiệm thu nội dung.

## 3. Trạng thái các gói

Trạng thái được quản lí theo gói. Bản ứng viên không được coi là bản phát hành nếu chưa có quyết định duyệt của chủ dự án.

| Phạm vi | Trạng thái |
|---|---|
| Điều hành | Kế hoạch canonical 0.6; tệp đã nhập và đối chiếu |
| D0 | Chủ dự án xác nhận đã hoàn tất v1.0; bộ tài sản đã nhập và đối chiếu |
| R1-G01 | Nghiên cứu đã kết tinh ở cấp gói; v1.0 đã được đọc và tiếp nhận góp ý; v1.1 là ứng viên đang thẩm định |
| Học liệu R1-G01 | Chưa duyệt phát hành; chưa công bố website; chưa có dữ liệu học sinh sử dụng v1.1 |
| Studio R1-G01 | Chưa sản xuất Studio chính thức; media thử nghiệm không thay đổi trạng thái này |

## 4. Danh mục nguồn đang dùng

Kho nguồn cá nhân chỉ đọc: `E:\zo_math_ca_nhan\zo_math_on_thi_toan_thpt\nguon\`. Đây là vị trí truy cập cục bộ hiện hành, không phải thành phần của repo `E:\zo_math`. Tên tệp trong bảng được tính từ kho này; không sao chép PDF vào repo.

| ID | Tên chính thức | Cơ quan / nhà xuất bản | Tên tệp hiện tại | SHA-256 |
|---|---|---|---|---|
| SRC-CTGDPT-TOAN-2018 | Chương trình giáo dục phổ thông môn Toán | Bộ Giáo dục và Đào tạo; ban hành kèm Thông tư 32/2018/TT-BGDĐT ngày 26/12/2018 | `Chuong trinh giao duc pho thong mon Toan 2018.pdf` | `f35d34ff84da2ca3f9ab72d5d67482ada414684b611deea98c4b329801b661ab` |
| SRC-SGK12-KNTT-T1 | Toán 12 — Tập Một, Kết nối tri thức với cuộc sống | Nhà xuất bản Giáo dục Việt Nam | `Toan 12. Tap 1. Ket noi tri thuc voi cuoc song.pdf` | `faeb554bea9cf81189c5e790b1b1edb42f50b3648694acc80dc99682ada3f1fd` |
| SRC-SGK12-KNTT-T2 | Toán 12 — Tập Hai, Kết nối tri thức với cuộc sống | Nhà xuất bản Giáo dục Việt Nam | `Toan 12. Tap 2. Ket noi tri thuc voi cuoc song.pdf` | `3c642f2e80d86d699ea62bbcabd0c3074fd5118def96e4b3b8ce1f9ead7f97bb` |

Đã đối chiếu ngày 2026-09-13: chương trình là bản đầy đủ 123 trang được chủ dự án chọn; không đăng ký bản rút gọn 38 trang. Hai SGK được nhận diện trực quan qua bìa, trang tên sách và trang thông tin xuất bản: đúng bộ, lớp và tập; tổng chủ biên Hà Huy Khoái; bìa và trang tên sách ghi “Bản mẫu — Tháng 1-2024”, trang xuất bản ghi bản quyền 2024, một số trường in/ISBN còn để trống. Tập Một có 104 trang PDF, Tập Hai có 99 trang PDF; không coi đây là bản in thương mại đã xác minh ISBN đầy đủ.

Ba tệp với SHA-256 trên là các bản tham chiếu hiện hành cho việc thẩm định, biên tập tiếp R1-G01 và chuẩn bị các gói sau. Chúng nằm trong kho nguồn cá nhân chỉ đọc và không được sao chép vào repo chỉ để tạo một bản nguồn song song.

## 5. Việc tiếp theo duy nhất

Hoàn tất thẩm định ứng viên R1-G01 v1.1 trên HTML và PDF đã tái sinh từ nguồn canonical trong gói.

Điều kiện hoàn tất:

- Đọc vòng tiếp theo, tập trung vào thuật ngữ, tên hoạt động, các bài kiểm tra 03 và 05 cùng cách trình bày bảng biến thiên.
- Ghi lỗi theo vị trí cụ thể và sửa từ nguồn trong `goi/R1-G01/src/`; không sửa trực tiếp đầu ra.
- Chỉ sau khi thẩm định mới quyết định vòng sửa tiếp theo hoặc duyệt cho bước sử dụng thử.
- Không ghi v1.1 là đã phát hành, không công bố website và không sản xuất Studio chính thức trong bước này.
