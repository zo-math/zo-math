# ZO Math — Ôn thi Toán THPT, Ấn bản ôn thi 2027

## 1. Định danh và thẩm quyền

- Gốc điều hành canonical của khóa 2027: `content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/` (tính từ gốc repository).
- Nguồn QMD của các gói tương lai nằm trong `content/thpt/on_thi_toan_thpt/hoc_lieu/<ma_goi>/`, dùng lại độc lập với năm thi; chưa tạo các thư mục gói trong Pha 2.
- Khóa 2027 đang ở trạng thái chưa xuất bản.
- `README.md` này là bảng điều khiển canonical duy nhất, xác định tài liệu current, trạng thái gói và việc tiếp theo.
- Đơn vị quản lí chính thức là các gói học liệu ngang cấp: D0, R1-G01, R1-G02, R1-G03 và các gói tiếp theo.

Mỗi tài liệu chỉ có một bản current; Git lưu lịch sử phiên bản. Không tạo thư mục `current/`, `published/`, `archive/`; không lưu toàn bộ hội thoại hoặc bản xuất trung gian.

Tài liệu nội bộ không được render hoặc publish. Pha 1 đã hoàn tất tại commit `1720df62f76213c88d482222f7e1c8c345c3f665`: cấu hình Quarto loại `_quy_trinh` khỏi render; `publish_public.yml` chặn toàn chuyên mục và tiếp tục chặn `_quy_trinh` khi các trang học được mở công khai trong tương lai. Không liên kết hồ sơ nội bộ từ trang người học.

## 2. Danh mục tài liệu canonical

Sổ canonical: [Truyền thông quá trình](truyen_thong_qua_trinh.md). Nội dung quá trình đã công khai chưa phải học liệu chính thức và không làm thay đổi trạng thái công bố học liệu R1-G01.

Các đường dẫn dưới đây tính từ README này. Kế hoạch điều hành 0.6 và D0 v1.0 đã chuyển nguyên trạng vào gốc điều hành mới. R1-G01 v1.1 vẫn tạm nằm trong `_projects/on_thi_toan_thpt_2027/goi/R1-G01/`, chờ Pha 3; Pha 2 không chuyển đổi, tái sinh hoặc thay đổi nội dung gói.

SHA-256 hiện hành của Kế hoạch 0.6: `1e5001e76e43d24e29894783548b95c56257a3c8e22edfd85480250a4ea9a343` (326184 byte), khớp byte với bản đã commit tại HEAD nguồn `1720df62f76213c88d482222f7e1c8c345c3f665`. Nội dung và phiên bản 0.6 giữ nguyên, không sửa đường dẫn trong Kế hoạch và không nâng lên 0.7.

| Tài sản | Vai trò | Đường dẫn đích đã phê duyệt | Trạng thái đối chiếu | Chủ dự án xác nhận |
|---|---|---|---|---|
| Kế hoạch điều hành 0.6 | Điều hành | [Kế hoạch điều hành](dieu_hanh/ke_hoach_dieu_hanh.md) | đã nhập và đối chiếu | Bản canonical là 0.6; số phiên bản lưu trong tài liệu |
| D0 v1.0 | Bộ tài sản khảo sát và định vị đầu vào | [Điểm vào canonical D0](goi/D0/README.md) | đã nhập và đối chiếu; chi tiết kiểm chứng bên dưới | Chủ dự án xác nhận D0 đã hoàn tất v1.0 |
| R1-G01 | Hồ sơ, nguồn sản xuất và đầu ra ứng viên của gói | [Điểm vào canonical R1-G01](../../../../../../_projects/on_thi_toan_thpt_2027/goi/R1-G01/README.md) | đã hợp nhất và tái sinh từ nguồn trong gói | Nghiên cứu đã kết tinh; v1.0 đã đọc và tiếp nhận góp ý; v1.1 đang thẩm định, chưa duyệt phát hành |

[Hồ sơ R1-G01](../../../../../../_projects/on_thi_toan_thpt_2027/goi/R1-G01/R1-G01_ho_so.md) giữ phạm vi, kết quả nghiên cứu, quyết định biên tập, nguồn và lịch sử trạng thái ở cấp gói. Các kết quả nghiên cứu tiền nhiệm đã được đối chiếu với đề cương, nội dung nền và hồ sơ biên tập trước khi hòa nhập; công cụ hoặc phiên nghiên cứu không còn là đơn vị quản lí.

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

## 5. Trạng thái chuyển đổi và việc tiếp theo duy nhất

- Pha 1 đã hoàn tất; chuyên mục vẫn là bản nháp, chưa xuất bản.
- Pha 2 đã hoàn tất chuyển quản trị khóa 2027 và nguyên bộ D0; kết quả chuyển và bằng chứng bảo toàn nguồn đã được chủ dự án duyệt.
- README này là đầu mối điều hành canonical duy nhất. [README tại vị trí cũ](../../../../../../_projects/on_thi_toan_thpt_2027/README.md) chỉ là chỉ dẫn chuyển tiếp, không duy trì bảng trạng thái song song.
- R1-G01 v1.1 vẫn là ứng viên đang thẩm định, chưa duyệt phát hành; nằm tạm trong `_projects` chờ Pha 3. Pha 3 chưa bắt đầu.
- Chưa bắt đầu R1-G02; không tạo trước thư mục gói.
- Việc tiếp theo duy nhất: chờ chỉ thị riêng cho Pha 3. Chưa bắt đầu chuyển R1-G01.

Trạng thái vận hành mới chỉ được ghi tại README này, không viết lại quyết định, nội dung toán học hoặc trạng thái sư phạm trong Kế hoạch 0.6 và D0. D0 giữ nguyên cấu trúc, hồ sơ, manifest, kiểm chứng và thành phẩm; không chuyển sang QMD và không tái sinh PDF trong pha này.

## 6. Nguồn gốc và dấu kiểm toàn vẹn

- Nguồn chuyển: `_projects/on_thi_toan_thpt_2027/` tại commit `1720df62f76213c88d482222f7e1c8c345c3f665`.
- Commit gần nhất sửa Kế hoạch 0.6 tại đường dẫn cũ: `ef331d376ccbd71575c3d384c8d3ce6a10318be0`; Git blob: `52618625ac9111a22f3043c1fff6d68dcda61852`.
- README điều hành cũ tại HEAD nguồn có SHA-256 `07d4927122ff58e922cb2f4979f5de58909d5f4958c285d6ef0163cc129e4510`; bản đầy đủ được bảo toàn trong Git, không tạo bản điều hành song song.
- Hash Kế hoạch `ec5221120abde5a43bb8ed10d849970b63d46652177f8270d43b60d164471c86` trong README cũ là ghi nhận lịch sử, không khớp blob Kế hoạch tại HEAD nguồn và không được dùng làm hash hiện hành. Hash hiện hành được đối chiếu trực tiếp ở mục 2.
- D0 gồm 25 tệp: 23 mục manifest, manifest và `HUONG_DAN_SU_DUNG.md`. SHA-256 của manifest giữ nguyên: `4a99567b0a20daab743586cf5d376f464a6e38fa6405d11433ad678e311f8b6c`. Mọi byte và đường dẫn tương đối bên trong D0 được bảo toàn.
- Truyền thông quá trình giữ nguyên các bản ghi và trạng thái; chỉ cập nhật hai liên kết tương đối tới hồ sơ R1-G01 còn ở vị trí cũ. Không đổi URL công khai hoặc fragment.
- Các phát biểu trong hồ sơ D0 được giữ nguyên theo mốc lịch sử; việc chuyển và kiểm tra hash không phải một lần nghiệm thu sư phạm hay quyết định công bố mới.
