# ZO Math — Ôn thi Toán THPT, Ấn bản ôn thi 2027

## Tiếp quản hiện hành

Đọc **mục A của [03 — Điều hành](03_dieu_hanh_chuong_trinh.md)** để lấy
trạng thái và việc tiếp theo. Bốn trang Nhà, D0, R1-G01, R1-G02 đã xuất
bản ngày 15/10/2026; D0 có một PDF, hai gói R1 có tám PDF mỗi gói.
Các gói R1 vẫn được giới thiệu là bản xem trước; đã xuất bản không đồng
nghĩa đã hoàn thiện toàn bộ chương trình hoặc phản biện toán độc lập.

- [Receipt phát hành](ho_so_phat_hanh_20261015.json): nguồn, commit website,
  kết quả kiểm bản công khai và các giới hạn tại đúng mốc phát hành.
- [Hồ sơ khép việc](khep_ho_so_phat_hanh_20261015.json): tài sản hiện hành,
  dọn dẹp, kiểm sau phát hành và xác nhận khép việc tìm ảnh của chủ trì.
- Nguồn sản xuất vẫn là QMD, dữ liệu, CSS và script trong repository;
  HTML/PDF là đầu ra, `_audit/` chỉ chứa bằng chứng.
- Bộ năm ảnh bìa và bản vuông chủ trì vừa thay được giữ theo manifest
  `../giao_dien/bo_anh_bia.json`. Không xem ảnh ngoài lựa chọn hiển thị
  của trang là rác. Bản đối chiếu QD_035 và checkpoint vẫn được bảo vệ.
- Kiến trúc lấy từ 01/QD_033; Kiểm tra theo QD_024; nhãn theo QD_025;
  quy trình theo 02; cách thể hiện theo 07; phân vai tài liệu theo 08.
  Khép phát hành không thay đổi các quy tắc này.

Việc dùng Nguồn cuộc trò chuyện và workspace được hướng dẫn tại [05](05_huong_dan_su_dung.md); vai trò tài liệu cũ và kho sao lưu tại [06](06_nguon_va_chuyen_tiep.md). Khi đọc được PC, lấy nguồn gói hiện hành trực tiếp từ workspace; không dùng bản toàn văn/PDF đính kèm cũ để quyết định kiến trúc gói mới.

## Hồ sơ tiếp nhận và triển khai trước phát hành

Các mô tả trạng thái, bản chờ xem và bước tiếp trong phần dưới được giữ
theo mốc lịch sử. Chúng không thay trạng thái hiện hành ở mục A của 03.
Các liên kết nguồn, phạm vi quy tắc và chứng cứ gốc tiếp tục dùng theo
vai trò trong 08; không chạy lại lệnh lịch sử để phục hồi bản cũ.

**PDF D0 ngày 14/10/2026:** chủ trì giao dựng một bản đầy đủ từ QMD hiện tại.
[Nguồn và lệnh dựng](../../../hoc_lieu/d0/_quy_trinh/README.md).
Không khôi phục bốn biến thể lịch sử, thay HTML hoặc tự xuất bản.
Quyết định HTML-only trước đó không cấm tác vụ mới này; trạng thái ở 03.

**DH_038 — nguồn Nhà Quarto native:** sửa trực tiếp `../index.qmd`, không
sửa template HTML hoặc partial sinh. Hướng dựng/kiểm tại README giao diện
Nhà; DH_037 giữ kết quả đường học, QD_035 giữ bộ bản xem chủ trì chọn.
Trạng thái/bản mới/bước tiếp chỉ ở 03. Đây là di trú nguồn, không đổi kiến
trúc, câu chữ đã chốt hoặc nghiệm thu/phát hành.

**QD_035 — bảo vệ đúng bản chủ trì chọn:** Home tại `_audit/zo_home_refinement_2026-10-12/delivered/home-reading.html`, các trang nó liên kết và runtime là nguồn đối chiếu chính thức không được dọn/xóa hoặc tự thay bằng bản khác. Đọc [danh mục bảo toàn](bao_toan_bon_trang.md) trước dọn; manifest/checkpoint DH_032 nằm ngoài repo. Nguồn dựng vẫn là QMD/template/data/script canonical; không tự hoàn nguyên câu chữ hoặc thay nghiệm thu. Trạng thái và bước tiếp chỉ ở [03](03_dieu_hanh_chuong_trinh.md).

**Điểm vào hiện hành — QD_033:** kiến trúc học tập ở [01](01_kien_truc_hoc_tap.md), cách thể hiện ở [07](07_quy_chuan_cau_truc_trang_nguoi_hoc.md), thẩm quyền ở [08](08_danh_muc_tham_quyen_dieu_hanh.md). **Bài học → Luyện tập → Kiểm tra → Ôn lại là tiến trình chuẩn được khuyến nghị, nhưng không phải điều kiện bắt buộc phải hoàn thành tuần tự**; hỗ trợ độc lập theo ngữ cảnh; lưu bằng chứng khác ghi Nhật kí; link quay lại đề chỉ khi tách vị trí. Công việc, trạng thái và bước tiếp theo chỉ ở [03](03_dieu_hanh_chuong_trinh.md). Các mốc/QA cũ bên dưới giữ để truy nguyên, không chứng nhận QD_033; G01/G02 chưa được đối chiếu lại ở cấp QMD/HTML với quyết định này nên chưa xác định có nội dung nào cần sửa. HTML chờ chủ trì duyệt, PDF chưa đồng bộ, chưa phát hành.

**QD_024 — Kiểm tra áp dụng toàn chương trình:** hai quy tắc quyền bắt đầu và không chia một lượt thành nhiều đợt ở 01/2.3–2.3.1 có hiệu lực cho mọi gói có hoạt động Kiểm tra, không chỉ R1. 07/4.4 và 02 dẫn cùng nguồn; không áp điều kiện cũ đòi bài làm độc lập trước khi vào Kiểm tra. Đây là cập nhật bộ điều hành; học liệu/HTML chưa tự được sửa hoặc nghiệm thu. Bản biên tập G01 do chủ trì sửa đã được nhận; tiến trình ở 03.

**QD_025 — hệ nhãn toàn chương trình:** kế thừa QD_023, bổ sung Gợi mở; nghĩa ở 01, từ vựng `label_contract` trong danh mục kiến trúc, hiển thị ở 07, hợp đồng máy trong chuẩn QMD/schema. [Bảng áp dụng G01](../../../hoc_lieu/r1_g01/_quy_trinh/ap_dung_he_nhan.json) đã áp dụng vào nguồn/binding, HTML mới cô lập chờ chủ trì duyệt; G02 đã áp dụng binding riêng 59 nhiệm vụ tại DH_016, HTML cô lập chờ chủ trì duyệt. Trạng thái và bước tiếp theo chỉ ở 03. Dùng `zo_learning_architecture.py labels --self-test` qua launcher để kiểm từ nguồn hiện tại; không nhận PASS tài liệu là đã đạt QMD/HTML.

Hợp nhất và đồng bộ các lớp điều hành theo QD_033 ngày 12/10/2026, kế thừa phần không bị thay của QD_021. Đọc [mục A của bảng điều hành](03_dieu_hanh_chuong_trinh.md) và [danh mục thẩm quyền](08_danh_muc_tham_quyen_dieu_hanh.md); không chọn bản từ chữ “current” trong hồ sơ lịch sử. Trước biên tập/kiểm nghiệm thu, xác minh `hop_dong_dieu_hanh.json` bằng `scripts/zo_2027_governance_check.py` qua `scripts/zo_python.py`. Cổng tài liệu không chứng nhận sản phẩm.

### QD_021 — lịch sử triển khai đường học; phần mâu thuẫn được thay bởi QD_033

QD_033 đã được áp dụng vào nguồn/HTML trong phạm vi bốn nhóm hiệu chỉnh
DH_037; xem 03 và hồ sơ hiện hành để lấy bản mới/bằng chứng. Vẫn chờ
chủ trì duyệt HTML; không dùng số PASS hoặc các mốc triển khai lịch sử
bên dưới thay nghiệm thu bản mới. Bộ bản xem QD_035 chưa bị thay thế.

G01 DH_011 từng bị chủ trì bác bỏ sơ đồ; 465/465 giữ làm bằng chứng lịch sử, không chứng nhận quan hệ mới. DH_015 đã áp dụng bản chốt người dùng vào nguồn và dựng HTML cô lập; trạng thái/bằng chứng ở 03 và hồ sơ G01, chưa là chủ trì duyệt HTML. DH_016 đã áp dụng và kiểm G02 theo QD_021/024/025; chưa là nghiệm thu của chủ trì hoặc kiểm toán độc lập toàn gói. Theo QD_022, cổng `scripts/zo_2027_governance_check.py` chọn quy tắc hiện hành theo chủ đề; chỉ kiểm lại phần bị ảnh hưởng, không khóa hiệu chỉnh hoặc hủy toàn bộ QA vì hash tài liệu đổi. Giữ thiết kế 9/10, Nhật kí 14 trường và receipt lịch sử.

Trang Nhà đã nối kit canonical tại DH_017. Nguồn dữ liệu/partial/marker và lệnh dựng cô lập ở `../giao_dien/README_web_2027.md`; đường kiểm `zo_web_2027_home_check.py`. Không dùng preview lịch sử hoặc kiểm launch/PDF cũ chứng nhận bản Nhà mới. Trạng thái và bước tiếp theo chỉ ở 03, không suy quyền phát hành.

## 1. Định danh và thẩm quyền

D0 đã nối kit qua nguồn opt-in ở DH_018/QD_027, map khảo sát riêng; [lệnh/ranh giới](../../../hoc_lieu/d0/giao_dien/README_web_2027.md). Nội dung/receipt giữ nguyên, giao diện mới chờ chủ trì xem, không kế thừa nghiệm thu cũ. PDF toàn trang được giao riêng ngày 14/10, không là cổng vào học hoặc điều kiện nghiệm thu HTML.

- Gốc điều hành canonical của khóa 2027: `content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/` (tính từ gốc repository).
- Nguồn canonical của các gói nằm trong `content/thpt/on_thi_toan_thpt/hoc_lieu/<ma_goi>/`, dùng lại độc lập với năm thi; hiện có D0, R1-G01 và R1-G02. D0 có QMD canonical, HTML có nghiệm thu lịch sử; PDF mới chưa nghiệm thu.
- Khóa 2027 đang ở trạng thái chưa xuất bản; các đầu ra đã duyệt đã được mở trong ranh giới ứng viên phát hành.
- `README.md` này là điểm vào canonical duy nhất. [Bảng điều hành](03_dieu_hanh_chuong_trinh.md) là nơi duy nhất ghi công việc đang mở, trạng thái tổng hợp và việc tiếp theo.
- Đơn vị quản lí chính thức là các gói học liệu ngang cấp: D0, R1-G01, R1-G02, R1-G03 và các gói tiếp theo.

Mỗi tài liệu chỉ có một bản current; Git lưu lịch sử phiên bản. Không tạo thư mục `current/`, `published/`, `archive/`; không lưu toàn bộ hội thoại hoặc bản xuất trung gian.

### Bắt đầu công việc

Pha và việc tiếp theo hiện hành được ghi tại [Bảng điều hành, mục A](03_dieu_hanh_chuong_trinh.md). Các đánh giá 4/10 ở lượt đầu là lịch sử, không phải trạng thái current. Quyết định duyệt, phản hồi và lỗi đã kiểm được truy nguyên tại `_design/ngon_ngu_thiet_ke_zo_math_0_4/09_nhat_ki/phan_hoi_tich_hop_web_2027_0_4.md`. Duyệt HTML thử nghiệm không tự cấp quyền tích hợp production, PDF, commit/push hoặc phát hành.

| Nhiệm vụ | Tài liệu cần đọc |
|---|---|
| Kiểm hoặc sửa R1-G01 | [Bảng điều hành](03_dieu_hanh_chuong_trinh.md), [Kiến trúc](01_kien_truc_hoc_tap.md), [Quy trình](02_quy_trinh_va_nghiem_thu.md), [Hồ sơ G01](goi/R1_G01.md) |
| Kiểm hoặc sửa R1-G02 | Ba tài liệu chung trên và [Hồ sơ G02](goi/R1_G02.md); đọc kết quả G01 đã chốt khi có ảnh hưởng dùng chung |
| Sửa cấu trúc trang hoặc component người học | Các tài liệu của gói, [Quy chuẩn trang người học](07_quy_chuan_cau_truc_trang_nguoi_hoc.md) và [Quy chuẩn gói QMD](quy_chuan_goi_qmd.md) |
| Sản xuất một gói mới | [Kế hoạch 0.6](ke_hoach_dieu_hanh.md), ba tài liệu chung, [mẫu hồ sơ](mau/ho_so_goi.md), [mẫu bản thảo](mau/ban_thao_goi.md) và [bảng kiểm](mau/bang_kiem_ban_thao_goi.md), theo [02/1.4](02_quy_trinh_va_nghiem_thu.md#ap-dung-mau-ban-thao) |
| Tìm căn cứ quyết định | [Nhật kí quyết định](04_nhat_ki_quyet_dinh.md) và [Nguồn, chuyển tiếp](06_nguon_va_chuyen_tiep.md) |

Yêu cầu hiện hành của người chủ trì xác định phạm vi và quyền thực hiện. Kế hoạch 0.6 điều hành phạm vi/lộ trình còn hiệu lực, không phục hồi trạng thái, mô tả D0 hoặc lệnh gói đã được thay bởi quyết định mới. Kiến trúc và quy trình điều hành cách thiết kế, kiểm tra; hồ sơ gói giữ phạm vi và bằng chứng riêng; repo và bản thực chạy là bằng chứng về cái đã tồn tại. Danh mục 08 phân vai cả tài liệu ngoài thư mục này. Tài liệu lịch sử không tự ghi đè quyết định mới.

Thông tin đã xác minh khi hợp nhất ngày 07/10/2026:

| Thông tin | Giá trị |
|---|---|
| Repository | `E:\zo_math` |
| Gốc điều hành 2027 | `content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/` |
| Kế hoạch 0.6 | `content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/ke_hoach_dieu_hanh.md` |
| Nguồn QMD G01/G02 | `content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/index.qmd`; `content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g02/index.qmd` |
| Chỉ dẫn repo | `AGENTS.md`; hai quy trình bắt buộc ở `quy_trinh_xay_dung/`; `content/thpt/on_thi_toan_thpt/AGENTS.md`; README và cấu hình cục bộ của từng gói |
| Người chấp nhận sản phẩm | Người chủ trì ZO Math |

Giữ ổn định tên tệp hiện hành; không tạo các bản `final`, `final_2` hoặc `moi_nhat`. Lịch sử thay đổi thuộc Git và nhật kí quyết định.

Tài liệu nội bộ không được render hoặc publish. Pha 1 đã hoàn tất tại commit `1720df62f76213c88d482222f7e1c8c345c3f665`: cấu hình Quarto loại `_quy_trinh` khỏi render. Ranh giới ứng viên hiện chỉ chọn các trang và tài sản đã duyệt qua allowlist; `publish_public.yml` tiếp tục chặn `_quy_trinh`. Không liên kết hồ sơ nội bộ từ trang người học.

## 2. Danh mục tài liệu canonical

Sổ canonical: [Truyền thông quá trình](truyen_thong_qua_trinh.md). Nội dung quá trình đã công khai chưa phải học liệu chính thức và không làm thay đổi trạng thái công bố học liệu R1-G01.

Các đường dẫn dưới đây tính từ README này. Kế hoạch điều hành 0.6 giữ nguyên trong gốc điều hành. Bộ D0 v1.0 đã được chuyển nguyên vẹn sang ranh giới gói `hoc_lieu/d0/` để chuẩn bị chuyển đổi canonical; R1-G01 và R1-G02 đã có nguồn QMD canonical. Trạng thái xuất bản của các gói vẫn `pending`.

SHA-256 hiện hành của Kế hoạch 0.6: `1e5001e76e43d24e29894783548b95c56257a3c8e22edfd85480250a4ea9a343` (326184 byte), khớp byte với bản đã commit tại HEAD nguồn `1720df62f76213c88d482222f7e1c8c345c3f665`. Nội dung và phiên bản 0.6 giữ nguyên, không sửa đường dẫn trong Kế hoạch và không nâng lên 0.7.

| Tài sản | Vai trò | Đường dẫn đích đã phê duyệt | Trạng thái đối chiếu | Chủ dự án xác nhận |
|---|---|---|---|---|
| Kế hoạch điều hành 0.6 | Điều hành | [Kế hoạch điều hành](ke_hoach_dieu_hanh.md) | đã nhập và đối chiếu | Bản canonical là 0.6; số phiên bản lưu trong tài liệu |
| D0 v1.0 | Bộ khảo sát và định vị đầu vào tự nguyện | [Điểm vào canonical D0](../../../hoc_lieu/d0/_quy_trinh/README.md) | nguồn QMD và HTML đã nghiệm thu; không yêu cầu PDF nội dung | `production: accepted`; chủ dự án cho phép tiến hành quy trình xuất bản ngày 2026-10-03 |
| R1-G01 | Hồ sơ, nguồn sản xuất và đầu ra ứng viên của gói | [Điểm vào canonical R1-G01](../../../hoc_lieu/r1_g01/_quy_trinh/README.md) | DH_015 đã áp dụng bản chốt; HTML cô lập chờ chủ trì duyệt, PDF chưa đồng bộ | Thiết kế 9/10 giữ nguyên; không quay về pilot/g01-kit hoặc dùng receipt cũ nghiệm thu bản mới |
| R1-G02 | Gói giá trị lớn nhất và giá trị nhỏ nhất | [Điểm vào canonical R1-G02](../../../hoc_lieu/r1_g02/_quy_trinh/README.md) | DH_016 đã sửa nguồn và kiểm HTML cô lập; chờ chủ trì duyệt, chưa promotion vào docs hoặc đồng bộ PDF | Nghiệm thu HTML/PDF cũ là lịch sử, không chứng nhận nguồn mới |

[Hồ sơ R1-G01](../../../hoc_lieu/r1_g01/_quy_trinh/ho_so/index.yml) giữ định danh, phiên bản và trạng thái sản xuất/xuất bản hiện hành. README của gói giữ hợp đồng vận hành và lịch sử chuyển đổi cần thiết.

Kiểm chứng bộ D0 v1.0:

- 23/23 tệp thuộc [manifest gốc](../../../hoc_lieu/d0/_quy_trinh/lich_su/v1_0/MANIFEST_SHA256.txt) đã khớp SHA-256; không thiếu tệp được liệt kê.
- `MANIFEST_SHA256.txt` không tự liệt kê chính nó.
- [HUONG_DAN_SU_DUNG.md](../../../hoc_lieu/d0/_quy_trinh/lich_su/v1_0/HUONG_DAN_SU_DUNG.md) là tài liệu bổ sung ngoài manifest, được chủ dự án xác nhận hợp lệ và thêm sau khi manifest gốc được lập. SHA-256 đã đối chiếu: `7853f36db073b2cac392f7fa029e67c732976c704dab2c3dd02d59d087e670f1`.
- Tổng cộng 25 tệp: 23 tệp thuộc manifest, manifest và tài liệu bổ sung. Giữ nguyên manifest và toàn bộ tệp D0; kiểm chứng tính nguyên vẹn không thay thế nghiệm thu nội dung.

## 3. Trạng thái các gói

Trạng thái được quản lí theo gói và tổng hợp tại [bảng điều hành](03_dieu_hanh_chuong_trinh.md). Bản ứng viên không được coi là bản phát hành nếu chưa có quyết định duyệt của chủ dự án.

| Phạm vi | Trạng thái |
|---|---|
| Điều hành | Kế hoạch canonical 0.6; tệp đã nhập và đối chiếu |
| D0 | Chủ dự án xác nhận đã hoàn tất v1.0; bộ tài sản đã nhập và đối chiếu |
| R1-G01 | DH_015 áp dụng bản chốt vào QMD/binding; HTML cô lập chờ chủ trì duyệt. Bằng chứng mới ở hồ sơ/03; 465/465 giữ lịch sử. docs FB036/receipt FB033 giữ nguyên. PDF chưa đồng bộ |
| Học liệu R1-G01 | `publication: pending`; chưa commit, push hoặc phát hành trong lượt hiện hành |
| Studio R1-G01 | Chưa sản xuất Studio chính thức; media thử nghiệm không thay đổi trạng thái này |
| R1-G02 | DH_016 áp dụng bản chốt G01 theo vai trò riêng G02; bằng chứng mới ở hồ sơ/03, HTML cô lập chờ chủ trì duyệt. FB036 giữ lịch sử; PDF chưa đồng bộ |

## 4. Danh mục nguồn đang dùng

Kho nguồn cá nhân chỉ đọc: `E:\zo_math_ca_nhan\zo_math_on_thi_toan_thpt\nguon\`. Đây là vị trí truy cập cục bộ hiện hành, không phải thành phần của repo `E:\zo_math`. Tên tệp trong bảng được tính từ kho này; không sao chép PDF vào repo.

| ID | Tên chính thức | Cơ quan / nhà xuất bản | Tên tệp hiện tại | SHA-256 |
|---|---|---|---|---|
| SRC-CTGDPT-TOAN-2018 | Chương trình giáo dục phổ thông môn Toán | Bộ Giáo dục và Đào tạo; ban hành kèm Thông tư 32/2018/TT-BGDĐT ngày 26/12/2018 | `Chuong trinh giao duc pho thong mon Toan 2018.pdf` | `f35d34ff84da2ca3f9ab72d5d67482ada414684b611deea98c4b329801b661ab` |
| SRC-SGK12-KNTT-T1 | Toán 12 — Tập Một, Kết nối tri thức với cuộc sống | Nhà xuất bản Giáo dục Việt Nam | `Toan 12. Tap 1. Ket noi tri thuc voi cuoc song.pdf` | `faeb554bea9cf81189c5e790b1b1edb42f50b3648694acc80dc99682ada3f1fd` |
| SRC-SGK12-KNTT-T2 | Toán 12 — Tập Hai, Kết nối tri thức với cuộc sống | Nhà xuất bản Giáo dục Việt Nam | `Toan 12. Tap 2. Ket noi tri thuc voi cuoc song.pdf` | `3c642f2e80d86d699ea62bbcabd0c3074fd5118def96e4b3b8ce1f9ead7f97bb` |

Đã đối chiếu ngày 2026-09-13: chương trình là bản đầy đủ 123 trang được chủ dự án chọn; không đăng ký bản rút gọn 38 trang. Hai SGK được nhận diện trực quan qua bìa, trang tên sách và trang thông tin xuất bản: đúng bộ, lớp và tập; tổng chủ biên Hà Huy Khoái; bìa và trang tên sách ghi “Bản mẫu — Tháng 1-2024”, trang xuất bản ghi bản quyền 2024, một số trường in/ISBN còn để trống. Tập Một có 104 trang PDF, Tập Hai có 99 trang PDF; không coi đây là bản in thương mại đã xác minh ISBN đầy đủ.

Ba tệp với SHA-256 trên là các bản tham chiếu hiện hành cho việc thẩm định, biên tập tiếp R1-G01 và chuẩn bị các gói sau. Chúng nằm trong kho nguồn cá nhân chỉ đọc và không được sao chép vào repo chỉ để tạo một bản nguồn song song.

## 5. Trạng thái chuyển đổi và đầu mối việc hiện hành

- Pha 1–3 và các lượt hoàn thiện R1-G01 đã hoàn tất; chuyên mục có ứng viên ra mắt cục bộ, chưa xuất bản.
- Pha 2 đã hoàn tất chuyển quản trị khóa 2027. Bước 1 của đợt chuyển đổi D0 đã đưa nguyên bộ v1.0 sang `hoc_lieu/d0/_quy_trinh/lich_su/v1_0/`; bằng chứng bảo toàn nguồn tiếp tục được giữ bằng manifest gốc.
- README này là điểm vào canonical duy nhất. [README tại vị trí cũ](../../../../../../_projects/on_thi_toan_thpt_2027/README.md) chỉ là chỉ dẫn chuyển tiếp, không duy trì bảng trạng thái song song.
- Công việc hiện hành và việc tiếp theo chỉ ở [bảng điều hành](03_dieu_hanh_chuong_trinh.md). Ma trận FB029 là bằng chứng khoảng trống lúc đó; FB034–036 đã sửa nguồn. Không dùng nó hoặc receipt FB033 thay trạng thái bản mới.
- Nguồn canonical của R1-G01 và R1-G02 lần lượt là `hoc_lieu/r1_g01/index.qmd` và `hoc_lieu/r1_g02/index.qmd`; HTML/PDF là đầu ra sinh.
- Không suy quyền dựng PDF, commit, push hoặc phát hành từ trạng thái PASS kỹ thuật.

Trạng thái chuyển đổi kỹ thuật của D0 được ghi tại `hoc_lieu/d0/_quy_trinh/README.md`; không viết lại quyết định, nội dung toán học hoặc trạng thái sư phạm trong Kế hoạch 0.6 và baseline D0 v1.0.

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
