# ZO Math — Ôn thi Toán THPT, Ấn bản ôn thi 2027

## 1. Định danh và thẩm quyền

- Gốc điều hành canonical của khóa 2027: `content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/` (tính từ gốc repository).
- Nguồn canonical của các gói nằm trong `content/thpt/on_thi_toan_thpt/hoc_lieu/<ma_goi>/`, dùng lại độc lập với năm thi; hiện có D0, R1-G01 và R1-G02. D0 đã có nguồn QMD canonical và là ứng viên HTML-only đã nghiệm thu.
- Khóa 2027 đang ở trạng thái chưa xuất bản; các đầu ra đã duyệt đã được mở trong ranh giới ứng viên phát hành.
- `README.md` này là bảng điều khiển canonical duy nhất, xác định tài liệu current, trạng thái gói và việc tiếp theo.
- Đơn vị quản lí chính thức là các gói học liệu ngang cấp: D0, R1-G01, R1-G02, R1-G03 và các gói tiếp theo.

Mỗi tài liệu chỉ có một bản current; Git lưu lịch sử phiên bản. Không tạo thư mục `current/`, `published/`, `archive/`; không lưu toàn bộ hội thoại hoặc bản xuất trung gian.

Tài liệu nội bộ không được render hoặc publish. Pha 1 đã hoàn tất tại commit `1720df62f76213c88d482222f7e1c8c345c3f665`: cấu hình Quarto loại `_quy_trinh` khỏi render. Ranh giới ứng viên hiện chỉ chọn các trang và tài sản đã duyệt qua allowlist; `publish_public.yml` tiếp tục chặn `_quy_trinh`. Không liên kết hồ sơ nội bộ từ trang người học.

## 2. Danh mục tài liệu canonical

Sổ canonical: [Truyền thông quá trình](truyen_thong_qua_trinh.md). Nội dung quá trình đã công khai chưa phải học liệu chính thức và không làm thay đổi trạng thái công bố học liệu R1-G01.

Các đường dẫn dưới đây tính từ README này. Kế hoạch điều hành 0.6 giữ nguyên trong gốc điều hành. Bộ D0 v1.0 đã được chuyển nguyên vẹn sang ranh giới gói `hoc_lieu/d0/` để chuẩn bị chuyển đổi canonical; R1-G01 và R1-G02 đã có nguồn QMD canonical. Trạng thái xuất bản của các gói vẫn `pending`.

SHA-256 hiện hành của Kế hoạch 0.6: `1e5001e76e43d24e29894783548b95c56257a3c8e22edfd85480250a4ea9a343` (326184 byte), khớp byte với bản đã commit tại HEAD nguồn `1720df62f76213c88d482222f7e1c8c345c3f665`. Nội dung và phiên bản 0.6 giữ nguyên, không sửa đường dẫn trong Kế hoạch và không nâng lên 0.7.

| Tài sản | Vai trò | Đường dẫn đích đã phê duyệt | Trạng thái đối chiếu | Chủ dự án xác nhận |
|---|---|---|---|---|
| Kế hoạch điều hành 0.6 | Điều hành | [Kế hoạch điều hành](dieu_hanh/ke_hoach_dieu_hanh.md) | đã nhập và đối chiếu | Bản canonical là 0.6; số phiên bản lưu trong tài liệu |
| D0 v1.0 | Bộ khảo sát và định vị đầu vào tự nguyện | [Điểm vào canonical D0](../../../hoc_lieu/d0/_quy_trinh/README.md) | nguồn QMD và HTML đã nghiệm thu; không yêu cầu PDF nội dung | `production: accepted`; chủ dự án cho phép tiến hành quy trình xuất bản ngày 2026-10-03 |
| R1-G01 | Hồ sơ, nguồn sản xuất và đầu ra ứng viên của gói | [Điểm vào canonical R1-G01](../../../hoc_lieu/r1_g01/_quy_trinh/README.md) | nội dung/kỹ thuật đã hoàn tất; tám PDF canonical | Ứng viên có thể học; `publication: pending`, chưa xuất bản công khai |
| R1-G02 | Gói học liệu về giá trị lớn nhất và giá trị nhỏ nhất của hàm số | [Điểm vào canonical R1-G02](../../../hoc_lieu/r1_g02/_quy_trinh/README.md) | nội dung, HTML và tám PDF canonical đã nghiệm thu | `production: accepted`; `publication: pending` |

[Hồ sơ R1-G01](../../../hoc_lieu/r1_g01/_quy_trinh/ho_so/index.yml) giữ định danh, phiên bản và trạng thái sản xuất/xuất bản hiện hành. README của gói giữ hợp đồng vận hành và lịch sử chuyển đổi cần thiết.

Kiểm chứng bộ D0 v1.0:

- 23/23 tệp thuộc [manifest gốc](../../../hoc_lieu/d0/_quy_trinh/lich_su/v1_0/MANIFEST_SHA256.txt) đã khớp SHA-256; không thiếu tệp được liệt kê.
- `MANIFEST_SHA256.txt` không tự liệt kê chính nó.
- [HUONG_DAN_SU_DUNG.md](../../../hoc_lieu/d0/_quy_trinh/lich_su/v1_0/HUONG_DAN_SU_DUNG.md) là tài liệu bổ sung ngoài manifest, được chủ dự án xác nhận hợp lệ và thêm sau khi manifest gốc được lập. SHA-256 đã đối chiếu: `7853f36db073b2cac392f7fa029e67c732976c704dab2c3dd02d59d087e670f1`.
- Tổng cộng 25 tệp: 23 tệp thuộc manifest, manifest và tài liệu bổ sung. Giữ nguyên manifest và toàn bộ tệp D0; kiểm chứng tính nguyên vẹn không thay thế nghiệm thu nội dung.

## 3. Trạng thái các gói

Trạng thái được quản lí theo gói. Bản ứng viên không được coi là bản phát hành nếu chưa có quyết định duyệt của chủ dự án.

| Phạm vi | Trạng thái |
|---|---|
| Điều hành | Kế hoạch canonical 0.6; tệp đã nhập và đối chiếu |
| D0 | Chủ dự án xác nhận đã hoàn tất v1.0; bộ tài sản đã nhập và đối chiếu |
| R1-G01 | v1.3 đã hoàn tất nội dung/kỹ thuật; ứng viên có thể học |
| Học liệu R1-G01 | `publication: pending`; chưa công bố website và chưa kiểm tra HTTP live |
| Studio R1-G01 | Chưa sản xuất Studio chính thức; media thử nghiệm không thay đổi trạng thái này |
| R1-G02 | v0.2 đã hoàn tất nội dung, HTML và hệ PDF canonical; ứng viên có thể học |

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

- Pha 1–3 và các lượt hoàn thiện R1-G01 đã hoàn tất; chuyên mục có ứng viên ra mắt cục bộ, chưa xuất bản.
- Pha 2 đã hoàn tất chuyển quản trị khóa 2027. Bước 1 của đợt chuyển đổi D0 đã đưa nguyên bộ v1.0 sang `hoc_lieu/d0/_quy_trinh/lich_su/v1_0/`; bằng chứng bảo toàn nguồn tiếp tục được giữ bằng manifest gốc.
- README này là đầu mối điều hành canonical duy nhất. [README tại vị trí cũ](../../../../../../_projects/on_thi_toan_thpt_2027/README.md) chỉ là chỉ dẫn chuyển tiếp, không duy trì bảng trạng thái song song.
- R1-G01 v1.3 đã hoàn tất nội dung/kỹ thuật trong `hoc_lieu/r1_g01/`; nhãn giao diện “Có thể học” không thay đổi `publication: pending`.
- R1-G02 đã hoàn tất chuyển đổi tại `hoc_lieu/r1_g02/`; nguồn canonical là `index.qmd`, còn HTML và tám biến thể PDF là đầu ra đã nghiệm thu.
- Việc tiếp theo đối với D0: hoàn tất các cổng `check`, source-sync, `prepare` và `publish` theo quy trình website; D0 chỉ phát hành HTML cùng tài sản cần thiết, không tạo PDF nội dung.

Trạng thái vận hành khóa 2027 tiếp tục được ghi tại README này. Trạng thái chuyển đổi kỹ thuật của D0 được ghi tại `hoc_lieu/d0/_quy_trinh/README.md`; không viết lại quyết định, nội dung toán học hoặc trạng thái sư phạm trong Kế hoạch 0.6 và baseline D0 v1.0.

## 6. Nhật kí bước chân

### 2026-10-03 — Cụm sửa 01

- Đồng bộ danh mục và đường bắt đầu học cho D0, R1-G01 và R1-G02; giữ nguyên mã gói, URL và liên kết sâu.
- Chốt tên hiển thị `Đơn điệu và cực trị` cho R1-G01 v1.3 và `Giá trị lớn nhất và giá trị nhỏ nhất` cho R1-G02 v0.2; cả ba học liệu mang trạng thái `Có thể học`.
- Dựng lại ảnh bìa, tám PDF của mỗi gói và website chuyên mục từ nguồn canonical; không thay đổi nội dung toán học hoặc kiến trúc học tập.
- Trạng thái bàn giao: người chủ trì đã duyệt trực quan năm trang và cho phép commit; chưa chạy `prepare` hoặc xuất bản.

## 7. Nguồn gốc và dấu kiểm toàn vẹn

- Nguồn chuyển: `_projects/on_thi_toan_thpt_2027/` tại commit `1720df62f76213c88d482222f7e1c8c345c3f665`.
- Commit gần nhất sửa Kế hoạch 0.6 tại đường dẫn cũ: `ef331d376ccbd71575c3d384c8d3ce6a10318be0`; Git blob: `52618625ac9111a22f3043c1fff6d68dcda61852`.
- README điều hành cũ tại HEAD nguồn có SHA-256 `07d4927122ff58e922cb2f4979f5de58909d5f4958c285d6ef0163cc129e4510`; bản đầy đủ được bảo toàn trong Git, không tạo bản điều hành song song.
- Hash Kế hoạch `ec5221120abde5a43bb8ed10d849970b63d46652177f8270d43b60d164471c86` trong README cũ là ghi nhận lịch sử, không khớp blob Kế hoạch tại HEAD nguồn và không được dùng làm hash hiện hành. Hash hiện hành được đối chiếu trực tiếp ở mục 2.
- D0 gồm 25 tệp: 23 mục manifest, manifest và `HUONG_DAN_SU_DUNG.md`. SHA-256 của manifest giữ nguyên: `4a99567b0a20daab743586cf5d376f464a6e38fa6405d11433ad678e311f8b6c`. Bước 1 chuyển toàn bộ cây sang `hoc_lieu/d0/_quy_trinh/lich_su/v1_0/`; mọi byte và đường dẫn tương đối bên trong baseline được bảo toàn.
- Truyền thông quá trình giữ nguyên các bản ghi và trạng thái; chỉ cập nhật hai liên kết tương đối tới hồ sơ R1-G01 còn ở vị trí cũ. Không đổi URL công khai hoặc fragment.
- Các phát biểu trong hồ sơ D0 được giữ nguyên theo mốc lịch sử; việc chuyển và kiểm tra hash không phải một lần nghiệm thu sư phạm hay quyết định công bố mới.
