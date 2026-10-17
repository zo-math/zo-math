# R1-G02 — nguồn canonical đang hoàn thiện kiến trúc 2027

**Nhãn cấp chứa — ứng viên sau phát hành, 17/10/2026.** Đã đồng bộ theo chỉ thị chủ trì; [HTML mới và hồ sơ](ho_so/dong_bo_nhan_20261017.md). Nguồn QMD/hình/PDF giữ nguyên. Chưa xuất bản lại hoặc dựng PDF; các xác nhận phát hành/CURRENT bên dưới thuộc bộ đã phát hành trước lượt nhãn này. Chủ trì giao commit mốc nguồn, không phải nghiệm thu HTML hoặc phát hành.


**Phát hành được giao — 17/10/2026.** Chủ trì yêu cầu xuất bản ba gói.
Đã dựng từ nguồn hiện hành đủ tám PDF mỗi gói, mỗi bản đạt 17/17 kiểm kỹ thuật
và provenance CURRENT. Hồ sơ: [PDF đợt này](ho_so/pdf_release_20261017.json).
Các mốc chờ PDF bên dưới là lịch sử; trạng thái phát hành thực tế lấy ở bảng 03.

**Đối sánh HTML — 17/10/2026.** Nguồn và HTML đã cập nhật theo chốt chung
của chủ trì tại 07/6.2; xem hồ sơ `ho_so/doi_sanh_chung_20261017.json` và
COMMON-HTML01 ở bảng điều hành khóa. Chưa dựng lại PDF trong lượt này;
các mô tả CURRENT/nghiệm thu của bộ trước dưới đây là lịch sử của bộ ấy,
không tự chứng nhận PDF đã đồng bộ với nguồn vừa chỉnh.

**Khép pipeline sau di dời công cụ — 16/10/2026.** Tám PDF của gói đã
dựng và đối chiếu lại; provenance cả tám bản là CURRENT. Mọi trang giữ nguyên
nội dung/bố cục so với bộ trước; các bản dựng qua nửa đêm chỉ cập nhật ngày
tạo tại bìa/trang kết. Xem [hồ sơ tái kiểm pipeline](ho_so/pdf_pipeline_revalidation_20261015.json).
Các hồ sơ `pdf_bundle_review.json`/`pdf_full_review.json` bên dưới ghi bộ trước
lượt tái dựng này và được giữ nguyên làm bằng chứng đối chiếu. Đây là cập
nhật kỹ thuật cục bộ, chưa xuất bản lại; receipt phát hành ngày 15/10 giữ nguyên.


**Bộ hiện hành đã đồng bộ — 15/10/2026.** Cả tám PDF đã dựng từ QMD hiện hành,
đạt 17/17 phép kiểm mỗi tệp. Bản đầy đủ có 61 trang;
bản học sinh có 42 trang. Thẻ tải lấy số trang thực tế và
trạng thái provenance từng tệp. Nguồn hình HTML/PDF cùng bộ vector 0.4; BBT
dựng native từ JSON. Thiết kế chung kế thừa D0 đã được chủ trì duyệt; chủ trì
đã duyệt dựng 14 biến thể và yêu cầu xuất bản bốn trang lên zomath.vn.
Hồ sơ hiện hành: `ho_so/pdf_bundle_review.json` và `ho_so/pdf_full_review.json`.
Mọi trang màu đã được bao phủ bởi kiểm thị giác hoặc đối chiếu pixel vùng thân
đã xem; kiểm xám đại diện từng biến thể và các trang hình/bảng/cuối của bản đầy đủ.
Chưa in giấy, quét QR bằng điện thoại hoặc phản biện toán độc lập toàn gói.
Đã xuất bản và xác minh trực tiếp trên zomath.vn ngày 15/10/2026; hồ sơ triển khai ở bảng 03 của khóa.
Các trạng thái chưa PDF/chưa promotion/chờ duyệt ở phần lịch sử bên dưới chỉ
mô tả thời điểm của lượt ấy, không phải trạng thái bộ hiện hành.

Kiểm nhanh trước biên dịch: `python scripts/zo_python.py -B scripts/zo_pdf.py preflight
content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g02/index.qmd --variant full`.
Cổng chung `scripts/zo_course_release_audit.py --preflight --output <thu_muc_bao_cao>`
kiểm cả 16 cấu hình bằng TeX, không dựng lại sách. Lệnh nào cũng gọi qua launcher.


## Kiến trúc dùng cho công việc tiếp theo

Đọc [01 — Kiến trúc học tập](../../../tot_nghiep_thpt/2027/_quy_trinh/01_kien_truc_hoc_tap.md) theo QD_033 và [07 — Cấu trúc trang](../../../tot_nghiep_thpt/2027/_quy_trinh/07_quy_chuan_cau_truc_trang_nguoi_hoc.md). Các thứ tự thẻ, sơ đồ học và trạng thái trong phần lịch sử dưới đây chỉ mô tả bản tại thời điểm đó; không dùng làm mẫu cho gói mới. Nguồn học liệu hiện hành là `../index.qmd` cùng các include, dữ liệu và manifest của gói.

## Lịch sử triển khai trước lượt đồng bộ 15/10/2026

**Hiện hành DH_026/QD_031:** nguồn QMD/layout/binding đã sửa backlog theo owner; Nhật kí độc lập, Toàn văn/Sửa lỗi/Lời giải đúng thứ tự, bỏ hành động đề–đáp án cục bộ thừa, bảng chọn bài dùng chuẩn chung. Năm SVG chính/nền/bìa đều dựng mới theo profile 0.4, manifest kiểm toàn bộ đầu vào và asset, không tái dùng cache canonical cũ. Bản xem/evidence ở `_audit/zo_pair_backlog_2026-10-11/`; cổng nguồn/DOM `scripts/zo_web_2027_backlog_check.py` chạy trong adapter. Chờ chủ trì duyệt HTML, PDF chưa đồng bộ, root docs/receipt/Git không sửa. Các mô tả “hiện hành” bên dưới là lịch sử trước DH_026, không phục hồi owner/nhóm lời giải/nhật kí/cache đã bị thay.

Hiện hành DH_023/QD_030: bảng theo chức năng 0.4, binding chung `profiles/course-tables.json`, guard `scripts/zo_course_tables.py` trong adapter. HTML/kiểm kê mới tại `_audit/zo_course_tables_2026-10-11/`; trạng thái theo 03 của khóa. Giữ sửa ký pháp/số mục QD_029 và guard `zo_math_notation.py`. Các mốc/đường dẫn bên dưới là lịch sử, không chứng nhận bản mới. Chưa PDF học liệu, promotion root docs, Git hoặc phát hành.

**DH_019 hiện hành:** G02 đã nối adapter canonical `scripts/zo_web_2027_g02_production.py` vào hook QMD chung, marker `zo-web-2027-g02`. HTML cô lập mới: `_audit/r1_g02_dong_bo_lai_g01_2026-10-11/html-current/g02-reading.html`; kiểm mới `qa-verified/qa.json` và đối sánh trực tiếp `pair-verified/pair.json`. Đã sửa nhịp Cách học/Khởi động, nhãn thừa, tổng quan ba chặng và tên Điểm dừng theo G01; giữ toán/ID/manifest/nhánh riêng/Journal14. Các câu “chưa production/chỉ audit” của DH_016 dưới đây là lịch sử trước nối đường dựng; root docs vẫn chưa promotion, HTML mới chờ duyệt, PDF vẫn cũ. Việc tiếp theo chỉ ở 03.

## DH_016 — bằng chứng trước lượt đồng bộ lại DH_019

**DH_016 / QD_025 — hiện hành 11/10/2026:** đã áp dụng thay đổi G01 theo vai trò riêng G02 vào nguồn QMD/layout và binding `../giao_dien/he_nhan.json`: 59 nhiệm vụ/59 đáp án, số liên tục theo chức năng, Ôn nền độc lập, Khởi động/Tự kiểm tra nguyên tử, Lời giải cùng tên nhiệm vụ. Nhật kí giữ nguồn chung 14 trường; lõi M1–M5 và chuyển giao M6 không đổi. Dùng `scripts/zo_r1_g02_labels_check.py` để dựng/kiểm phép chiếu riêng G02; không ép quota G01 hoặc tuyên bố CLI bảng G01 đã tự hỗ trợ mọi gói. HTML hiện tại: `_audit/r1_g02_ap_dung_he_nhan_2026-10-11/delivery-html/g02-reading.html`; báo cáo `qa-release-preview/qa.json`, điều hành `governance-current.json`. Chờ chủ trì duyệt, chưa production/PDF/Git/phát hành.

Điểm vào điều hành: [README khóa 2027](../../../tot_nghiep_thpt/2027/_quy_trinh/README.md); việc hiện hành chỉ ở bảng 03. QD_016–018 hợp nhất tài liệu ngày 10/10, không sửa QMD/HTML. Bài học/Luyện tập không xen kẽ; Nhật kí dùng cùng nguồn 14 trường với G01. Các mô tả “hiện hành/chờ xem” trong mục lịch sử thuộc thời điểm của mục, không cấp quyền hoặc nghiệm thu mới.

**QD_021/024 hiện hành:** đã sửa/kiểm nguồn, đích và câu chữ DH01–DH14, cùng tuyến runtime đại diện; Kiểm tra bắt đầu khi chuẩn bị kĩ hoặc đủ tự tin, tự lực và không chia lượt. Không dùng QA cũ thay kiểm mới, không lấy tự tin làm bằng chứng đạt; QD_022 vẫn cho sửa và chỉ kiểm lại phần ảnh hưởng. Việc tiếp theo chỉ ở 03; không phải kiểm toán độc lập toàn gói hoặc chủ trì duyệt HTML.

## FB036 — lịch sử đối sánh 08/10; cần rà lại QD_021

Theo QD_019, đọc [danh mục 08](../../../tot_nghiep_thpt/2027/_quy_trinh/08_danh_muc_tham_quyen_dieu_hanh.md). Hồ sơ máy đọc đã tách nghiệm thu lịch sử tháng 9 khỏi ứng viên FB036 pending; không coi accepted cũ là chốt bản sửa mới. G01 đã có 21 RD nguồn/DOM ngày 10/10; G02 chưa audit toàn bộ ở mức tương đương. Kế thừa quy tắc chung, không copy đoạn G01 còn lỗi hoặc triển khai đề xuất chưa chốt. Nhật kí giữ một nguồn 14 trường. Lệnh/ma trận nghiệm thu cũ bên dưới là evidence theo bản, không quyền chạy hiện hành.

HTML tại mốc FB036: `_audit/zo_web_pair_refinement_2026-10-08/g02/g02-reading.html`.
Nguồn QMD đã sửa nhãn/tên, routing S-L/S-K/S-O, nhóm lời giải, ownership của
xác nhận Nền, mục tiêu/điểm dừng/lỗi Ôn lại, typography Nguồn và bìa riêng từ
Luyện tập 02. Nhật kí include chung; mọi disclosure mặc định đóng. Giữ toán,
ID cũ và đích liên kết; không sao chép đồ thị G01. Hồ sơ và phép kiểm chống
tái diễn tại README audit và `scripts/zo_web_2027_pair_check.py`.
Chưa đủ điều kiện xin duyệt đường học theo QD_021; cần rà DH01–DH14. Chưa tích hợp HTML G02 vào `docs`, PDF/Git/phát hành/0.5.
Các mốc DH007/FB035 và FB034 dưới đây là lịch sử, không phải bản hiện hành.

## Mốc lịch sử — DH_007 / FB035, 08/10/2026

Chủ trì đã chỉ ra bản FB034 còn lệch vai trò/cấp/vùng đọc/bảng ngay từ đầu.
985/985 kiểm bố cục của mốc đó không chứng nhận nhất quán semantic.
Nguồn đã được tinh chỉnh: Bắt đầu/Cách học, định hướng, khởi động, Ôn nền
h4, khái niệm/ví dụ/tự kiểm/phương pháp và bảng; Nhật kí dùng include chung
`../_dung_chung/nhat_ki_hoc_tap.qmd`, khóa bằng phần inline G01 đã chốt.
HTML tại mốc FB035: `_audit/zo_g02_consistency_2026-10-08/g02-reading.html`.
Kiểm semantic mới: `scripts/zo_g02_consistency_check.py` (144/144), kèm
985/985 bố cục/hành vi; chưa là nghiệm thu chủ trì. Xem README audit mới.

### Mốc FB034 trước phản hồi — lịch sử, không phải HTML hiện hành

Nguồn `index.qmd` đã được tổ chức lại theo ba chặng, tám điểm kiểm soát,
chín thẻ Nền, Nhật kí 14 trường và ba lượt Ôn lại có đề/lời giải riêng.
Các nhiệm vụ toán đã có được tái dùng theo đúng vai trò; không sao chép toán G01.
HTML để chủ trì xem nằm tại `_audit/zo_g02_completion_2026-10-08/g02-reading.html`.
Hồ sơ và cách dựng/kiểm tại `giao_dien/README_web_2027.md` và README của audit.

**Chờ chủ trì duyệt HTML/nội dung/đường học mới.** Không lấy nghiệm thu lịch sử
hoặc `planned=0` làm nghiệm thu nguồn hiện hành. PDF đang có chưa đồng bộ;
không dựng PDF hoặc sửa provenance bằng tay trong lượt này. G01/Nhà/D0 và
thiết kế đã chốt được giữ nguyên; chưa stage/commit/push/phát hành hoặc khóa 0.5.

## Hồ sơ lịch sử — không chứng nhận nguồn hiện hành

`index.qmd` là nguồn biên soạn canonical của gói sau khi nội dung từ bản thảo
HTML được chuyển đổi và đối chiếu. Nội dung, HTML và hệ PDF đã được nghiệm thu;
trạng thái xuất bản vẫn là `pending` cho đến khi quy trình website hoàn tất.

Nguồn đầu vào chỉ đọc:

```text
E:\zo_math_ca_nhan\zo_math_on_thi_toan_thpt\R1-G02\ZO_Math_R1-G02_ban_thao_noi_dung_v0.1_04.html
```

SHA-256 của nguồn: `7ee929aa7d2473d1b96f6136e9a93e8d94974b58bb3e01003a3aa896bd011f78`.

Không sửa ngược bản HTML nguồn. Mọi thay đổi tiếp theo của học liệu được thực
hiện trong `index.qmd` và tài sản canonical của gói. HTML/PDF là đầu ra sinh.

R1-G01 là baseline trình bày và vận hành đã nghiệm thu; không sao chép nội dung,
ID hoặc các hằng số kiểm định riêng của R1-G01 sang gói này.

Thanh thẻ dùng hành vi điều hướng chung của chuyên mục: giữ nguyên trong slot
`sticky` ở `top: 0`; Navbar ẩn khi kéo xuống và xuất hiện lại khi kéo lên. HTML
hiện có chỉ nhận thay đổi này ở lần render và tái xuất bản kế tiếp.

Ma trận chuyển đổi tháng 9 đã hết vai trò vận hành và được chuyển vào kho
lưu trữ ngày 16/10/2026; nơi lưu và checksum ở
[06 — Nguồn và chuyển tiếp](../../../tot_nghiep_thpt/2027/_quy_trinh/06_nguon_va_chuyen_tiep.md).
Để tiếp tục biên soạn, dùng 01/QD_033, 07,
[hồ sơ G02](../../../tot_nghiep_thpt/2027/_quy_trinh/goi/R1_G02.md)
và manifest hiện hành; không suy kiến trúc từ bản render tạm hoặc ma trận cũ.

Bước 2 đã hoàn tất: ghi chú hiệu đính, truy nguyên và lịch sử rà soát được bảo
toàn tại [`ho_so/lich_su_ban_thao_v0_1.md`](ho_so/lich_su_ban_thao_v0_1.md),
không còn nằm trong nội dung dành cho người học. `index.qmd` chỉ giữ phần nguồn
đối chiếu công khai, ngắn gọn.

Hệ thành phần học liệu dùng hợp đồng canonical của chuyên mục. CSS và phép
chuẩn hóa AST dùng chung lần lượt nằm tại
`assets/css/_zo_learning_components.scss` và
`assets/lua/zo_learning_components.lua`; adapter của gói chỉ ánh xạ các lớp
chuyển tiếp trong nguồn R1-G02. Bốn khối gợi ý là `hint`, không được tính là
`guidance`. Kiểm kê nguồn riêng của gói chạy bằng:

```text
python scripts/zo_python.py content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g02/cong_cu/kiem_chung_thanh_phan.py
```

Baseline PDF R1-G02 tháng 9/2026 là bằng chứng lịch sử: `full` 26,
`student` 17, `bai_hoc` 10, `luyen_tap` 6, `kiem_tra` 4, `sua_loi` 5,
`on_lai` 3 và `loi_giai` 10. Ma trận này chỉ đối chiếu đúng bản nguồn
tháng 9, không áp lên QMD/kiến trúc hiện hành. Bản đầy đủ mới có 58 trang;
các số trang tải theo phần chỉ cập nhật sau khi dựng và đo PDF tương ứng.
Thay nguồn thuộc fingerprint phải dựng các biến thể bị STALE bằng công cụ;
không sửa provenance hoặc receipt bằng tay để chuyển thành CURRENT.
