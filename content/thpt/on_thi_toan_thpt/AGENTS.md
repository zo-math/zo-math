# Chỉ dẫn cho chuyên mục Ôn thi Toán THPT

Đây là tài liệu điều phối nội bộ, không phải nội dung xuất bản.

## Tiếp quản sau phát hành 15/10/2026

Bốn trang Nhà, D0, R1-G01, R1-G02 đã xuất bản. Trước công việc tiếp theo,
đọc mục A của `tot_nghiep_thpt/2027/_quy_trinh/03_dieu_hanh_chuong_trinh.md`,
receipt phát hành và hồ sơ khép việc được dẫn ở đó. Các trạng thái chờ
duyệt trong mốc DH/FB bên dưới chỉ mô tả lịch sử của mốc ấy. Quy tắc
chung vẫn có hiệu lực; một sửa đổi mới phải kiểm theo phạm vi ảnh hưởng.
Bộ ảnh bìa giữ đủ năm tỉ lệ theo `tot_nghiep_thpt/2027/giao_dien/bo_anh_bia.json`; bản
vuông do chủ trì thay đã khép tìm ảnh. Không phục hồi ảnh vuông từ
receipt nhập cũ. Trước dọn tài sản, đọc danh mục bảo toàn và chạy
`python scripts/zo_python.py -B scripts/zo_home_cover_check.py`.

## Phạm vi và thẩm quyền

Tuân thủ `AGENTS.md` ở gốc repository và các tài liệu bắt buộc được dẫn chiếu tại đó. Điểm vào điều hành khóa 2027 là `tot_nghiep_thpt/2027/_quy_trinh/README.md`; quy chuẩn gói hiện hành là `tot_nghiep_thpt/2027/_quy_trinh/quy_chuan_goi_qmd.md`; mẫu hồ sơ là `tot_nghiep_thpt/2027/_quy_trinh/mau/ho_so_goi.md`.

Kiến trúc đã được phê duyệt đặt chuyên mục tại `content/thpt/on_thi_toan_thpt`: học liệu dùng lại thuộc `hoc_lieu/<ma_goi>/`, điều hành khóa theo năm thuộc `tot_nghiep_thpt/<nam>/_quy_trinh/`. Không tạo một lớp điều hành song song bên ngoài chuyên mục sau khi hoàn tất chuyển đổi.

Kiến trúc học tập đang áp dụng cho R1-G01, R1-G02 và các gói R1 tiếp theo của khóa 2027 được điều hành bởi:

- `tot_nghiep_thpt/2027/_quy_trinh/01_kien_truc_hoc_tap.md`;
- `tot_nghiep_thpt/2027/_quy_trinh/02_quy_trinh_va_nghiem_thu.md`;
- `tot_nghiep_thpt/2027/_quy_trinh/07_quy_chuan_cau_truc_trang_nguoi_hoc.md` cho cấu trúc, điều hướng và nghiệm thu giao diện người học;
- `tot_nghiep_thpt/2027/_quy_trinh/goi/R1_G01.md` và `tot_nghiep_thpt/2027/_quy_trinh/goi/R1_G02.md` cho phạm vi từng gói;
- `tot_nghiep_thpt/2027/_quy_trinh/schema_kien_truc_hoc_tap.json` và `tot_nghiep_thpt/2027/_quy_trinh/danh_muc_kien_truc_hoc_tap.yml` cho hợp đồng máy đọc được.

Danh mục thẩm quyền của toàn bộ bộ điều hành là `tot_nghiep_thpt/2027/_quy_trinh/08_danh_muc_tham_quyen_dieu_hanh.md`; phải đọc khi tiếp quản hoặc đổi quyết định dùng chung. Chỉ 03 sở hữu việc hiện hành. Cổng đồng bộ tài liệu trong 02 phải khép trước khi biên tập tiếp; không sửa tài liệu lịch sử/receipt để hợp thức hóa ứng viên.

Manifest từng gói nằm tại `hoc_lieu/<ma_goi>/_quy_trinh/kien_truc_hoc_tap.yml`. Trước khi biên soạn nội dung theo kiến trúc này, chạy checker schema và readiness qua `scripts/zo_learning_architecture.py`; `planned` là khoảng trống nội dung thật, không được đổi thành hoàn tất chỉ để checker readiness đạt. Schema hợp lệ hoặc `planned=0` không chứng nhận nội dung/đường học đã đúng; không đổi manifest trong một lượt chỉ đồng bộ văn bản điều hành.

## Viết và kiểm bản thảo gói mới

Khi chủ trì giao viết, sửa hoặc rà bản thảo gói R1 của khóa 2027, tự đọc và áp dụng:

- `tot_nghiep_thpt/2027/_quy_trinh/mau/ban_thao_goi.md`;
- `tot_nghiep_thpt/2027/_quy_trinh/mau/bang_kiem_ban_thao_goi.md`;
- cơ chế sử dụng, lưu kết quả và cập nhật tại `02_quy_trinh_va_nghiem_thu.md`, mục 1.4.

Yêu cầu tự nhiên như “Viết bản thảo gói R1-G04” kích hoạt việc nạp hai mẫu; không bắt chủ trì gọi tên mẫu hoặc biết lệnh. Trước viết phải có bảng đối chiếu theo chức năng với G01/G02; trước trình phải có kết quả bảng kiểm với vị trí bằng chứng và khác biệt có lí do. Đọc 01/07 và nguồn toán chính thức, không chỉ sao khung hoặc số lượng bài của gói trước. Gói đã có bản thảo ghi áp dụng hồi cứu; không giả đã dùng mẫu từ đầu. Không nâng PASS kí hiệu/liên kết thành đạt nội dung hoặc hình. Kết quả áp dụng thuộc `ho_so/` của gói; phần được chủ trì cho hoãn ghi đúng phạm vi, không đánh dấu Đạt. Không tạo thư mục hoặc gói tương lai ngoài phạm vi đã giao.

## Bắt đầu dựng QMD hoặc HTML: luôn áp dụng hệ nhãn

Yêu cầu chuyển bản thảo, dựng/hiệu chỉnh QMD hoặc HTML của gói R1 tự kích hoạt `07_quy_chuan_cau_truc_trang_nguoi_hoc.md`/6.2 và `02_quy_trinh_va_nghiem_thu.md`/2.4. Nạp `label_contract.display_contract` từ danh mục và `giao_dien/he_nhan.json` của gói trước khi dựng. Không dừng ở gắn metadata. Phải có nhãn chức năng/ngữ cảnh thật, số liên tục theo loại hiển thị toàn gói, cặp đề–lời giải, điểm dừng, loại kiến thức và ví dụ theo nội dung; không thêm nhãn đã lặp trong tiêu đề.

Gói dựng mới dùng `scripts/zo_course_labels.py` với `display_contract: qd025-display-v1`; các cổng QMD/Quarto kiểm binding nguồn và nhãn HTML. Cổng thiếu/sai phải được sửa trước trình, không bỏ qua hoặc thay bằng số đếm. Giữ adapter G01/G02 làm đối chứng; không chép quota hoặc ngoại lệ riêng. Bảng áp dụng hiển thị hiện hành của gói mới là binding này; chỉ dùng bảng di trú `ap_dung_he_nhan.json` khi thực sự làm di trú theo 02/2.4. Khi phát triển gói mới, nối adapter hiển thị vào cổng chung và kiểm trình duyệt; không sửa tay HTML đầu ra.

Nhãn và số hiện hành theo NUMBERING-20261018 tại 07/6.2: MẠCH HỌC/HỖ TRỢ; nhãn con chỉ thêm khu vực chứa, ví dụ MẠCH HỌC · BÀI HỌC. Mỗi loại hiển thị đánh số liên tục toàn gói, không theo chức năng; Tự kiểm tra đổi tên hiển thị thành Nhiệm vụ, cùng dãy Nhiệm vụ. G01–G04 khai numbering_scope: package-type-v1. Giữ chức năng/ID/cặp đề–đáp án, dùng zo_course_numbering.py và zo_course_labels.py; không gán chuỗi riêng trong adapter.

## Cổng đồ thị và bảng biến thiên

Công việc có hình/BBT tự kích hoạt 07/6.1.2 và 02/2.5: ma trận tài nguyên theo vai trò trước viết/chuyển nguồn; bộ dựng ZO Math, JSON BBT canonical, component hình dùng chung và kiểm đối chứng thực. CLI QMD/Quarto cùng cổng HTML gọi zo_course_math_assets.py cho G04/gói mới. Phân loại bảng hoặc chọn profile không thay kiểm component/vai trò/provenance. Giữ nguyên bản thảo/ảnh bìa đã duyệt; bản sửa hiển thị phải trình riêng. Không sao JSON rỗng hoặc sizing riêng từ gói không có BBT.

## Giới hạn tích hợp và đầu mối điều hành

Ngôn ngữ bảng QD_030 áp dụng toàn khóa 2027, theo chức năng tại `07_quy_chuan_cau_truc_trang_nguoi_hoc.md`/6.1.1 và mẫu Design 0.4 được dẫn chiếu. Trước dựng hoặc sửa bảng, kiểm ánh xạ trong `_design/web_2027_mau_dung_chung/profiles/course-tables.json`; bộ dựng dùng `scripts/zo_course_tables.py`. Không dùng quy tắc căn trái đại trà đã bị thay thế cho bảng giá trị/dấu/biến thiên hoặc suy kiểu từ tên; bảng chưa phân loại phải được xử lí trước khi trình HTML. Không sửa dữ liệu toán để khớp hình thức.

Hai quy tắc Kiểm tra QD_024 ở `01_kien_truc_hoc_tap.md`, Mục 2.3–2.3.1, áp dụng cho toàn bộ các gói của chương trình Ôn thi Toán THPT 2027, không chỉ R1: đã chuẩn bị kĩ hoặc đủ tự tin thì có thể bắt đầu; một lượt Kiểm tra không chia nhiều đợt. Quyền bắt đầu không chứng nhận đạt mục tiêu. Nạp 07/4.4 và phép kiểm ở 02 khi sản xuất/rà hoạt động này; không dùng điều kiện vào Kiểm tra cũ. Không ép hợp đồng R1 hoặc Kiểm tra lên Khảo sát D0/tài nguyên Nền. Cổng tài liệu của khóa phải kiểm chủ đề `assessment_policy`; PASS tài liệu không chứng nhận nguồn học liệu/HTML đã áp dụng.

Hệ nhãn học liệu QD_025 có hiệu lực cho toàn bộ các gói của chương trình, không chỉ R1: kế thừa QD_023 và bổ sung chức năng Gợi mở. Đọc 01/07, `label_contract` của danh mục kiến trúc và chuẩn QMD. Không tạo nhãn riêng, reset số theo chặng, suy chức năng từ tên hoặc dùng bố cục cũ để chứng nhận đã di trú. Khi rà/di trú học liệu cũ, lập/kiểm bảng `_quy_trinh/ap_dung_he_nhan.json` bằng `zo_learning_architecture.py labels --self-test` qua launcher; gói dựng mới dùng binding/cổng hiển thị theo mục Bắt đầu dựng QMD hoặc HTML và 02/2.4. Bảng mapping_only không cho phép tự sửa QMD, render hoặc tuyên bố đã nghiệm thu. G01/G02 có binding hiển thị canonical riêng `giao_dien/he_nhan.json`; G02 đã áp dụng nguồn và kiểm HTML cô lập tại DH_016, chưa nghiệm thu chủ trì. Quy tắc mới thay phần cũ nhưng không cấm hiệu chỉnh theo QD_022.

Trước biên tập hoặc kiểm xin duyệt gói R1 của khóa 2027, chạy `python scripts/zo_python.py scripts/zo_2027_governance_check.py` để xác minh bản điều hành và guard theo registry của khóa. Quyết định mới phải thay phần hoạt động cũ và đồng bộ những đích bị ảnh hưởng ngay trong cùng lượt theo mục 1.2 của quy trình 02. Cổng tài liệu đạt không chứng nhận sản phẩm; ứng viên có lỗi chặn không được trình như đã đạt. Theo QD_022/02/1.2, chỉ kiểm lại phần chịu ảnh hưởng của quy tắc, đầu vào hoặc phép kiểm thay đổi; không tái áp dụng quy tắc bị thay, không hủy toàn bộ QA vì hash tài liệu đổi hoặc cấm hiệu chỉnh hợp lệ. Không sửa hash/receipt/kết quả lịch sử để che lệch nguồn.

- Tiếp quản từ mục A của bảng `03_dieu_hanh_chuong_trinh.md`, rồi hồ sơ gói và README vận hành, không từ mốc g01-kit/pilot/receipt lịch sử. QD_016–018 đã hợp nhất quyết định sau FB036: Bài học/Luyện tập không xen kẽ, Nhật kí một nguồn đủ 14 trường, vùng đọc theo nhịp và trạng thái đúng bản. Bản sửa hai gói chưa tự kế thừa nghiệm thu cũ; PDF/phát hành là nhiệm vụ riêng. Không suy trạng thái hiện hành từ số PASS hoặc metadata chưa đồng bộ.
- Không xem mẫu hồ sơ thiết kế của chuyên mục là schema CLI. Ứng viên R1-G01 có cấu hình và hồ sơ riêng trong `_quy_trinh/`; phải đọc README tại đó trước khi làm việc.
- Với khóa 2027, phải đọc `tot_nghiep_thpt/2027/_quy_trinh/README.md`: đây là điểm vào canonical duy nhất. Công việc hiện hành và việc tiếp theo chỉ được ghi tại `03_dieu_hanh_chuong_trinh.md`. README cũ trong `_projects/on_thi_toan_thpt_2027` chỉ dùng để chuyển tiếp.
- Tài liệu đã khóa và thành phẩm lịch sử chỉ được chuyển hoặc sửa trong phạm vi chủ dự án giao; không suy từ việc chuyển quản trị thành quyền chuyển đổi học liệu.
- Không tạo trước thư mục gói tương lai hoặc tài nguyên chưa dùng.
- Không tự thay nội dung toán học, nhiệm vụ, thuật ngữ hoặc thiết kế đã chốt.

## Sửa nhỏ: chọn đường cập nhật tối thiểu

Áp dụng mục 7.1 của `quy_trinh_xay_dung/quy_trinh_thuc_hien_nhiem_vu_ky_thuat.md`
ở gốc repo. Không coi một sửa ảnh/chữ là yêu cầu kiểm định lại toàn gói.
Lệnh render cả chuyên mục bên dưới dùng cho phạm vi cả chuyên mục; sửa một
trang dùng đường dẫn QMD cụ thể. Gói có cấu hình dùng
`python scripts/zo_python.py scripts/zo_qmd.py render <index.qmd> --html-only`
khi chỉ cần HTML, giữ các cổng bắt buộc. `draft: true` cần profile
`on-thi-preview` theo cơ chế preview hiện hành; không sửa trạng thái để lách.

Ví dụ khảo sát trước thay bìa G03 (16/10/2026): `scripts/zo_web_2027_g03.py` tạo hero
và gọi `PreviewBuilder.common_assets()` trong `scripts/zo_web_2027_preview.py`,
khi khảo sát lấy `_design/web_2027_mau_dung_chung/assets/cover-graph.svg` dùng chung.
Sau cập nhật, G03 dùng `hinh/bia_tiem_can.tex` và SVG riêng của gói; giữ ảnh
dùng chung nguyên vẹn.
Không sửa ảnh dùng chung để thay riêng bìa G03: cập nhật nguồn/binding riêng
của gói và phép đưa tài nguyên vào adapter trong phạm vi nhiệm vụ thay bìa.
Sau đó render HTML đúng trang, kiểm ảnh tải được, đúng ảnh, đúng đường dẫn,
không méo/cắt sai ở màn hình rộng và hẹp. Không sửa tay HTML/SVG đầu ra;
ảnh cần sinh phải dùng công cụ nguồn phù hợp. Không dựng lại các hình bài tập
hoặc PDF học liệu chỉ vì thay bìa HTML. Nếu yêu cầu gồm bìa PDF hay ảnh trên
trang danh mục thì bổ sung chính những đầu ra đó. Đây là đường thực hiện cho
lần thay bìa, không chứng nhận bìa hiện tại đã được sửa hay duyệt.

## Render, preview và xuất bản

Kế thừa dự án Quarto ở gốc; không tạo `_quarto.yml` độc lập. Hai trang cửa ngõ chưa thuộc một dự án QMD có cấu hình, nên dùng trình khởi chạy Quarto chung từ gốc repository:

```text
python scripts/zo_python.py scripts/zo_quarto.py render content/thpt/on_thi_toan_thpt --profile on-thi-preview
python scripts/zo_python.py scripts/zo_quarto.py preview content/thpt/on_thi_toan_thpt/index.qmd --profile on-thi-preview
```

Preview chỉ lắng nghe tại `127.0.0.1`. Navbar/sidebar nguồn dùng chung có đường vào ứng viên để kiểm tra đường đi; các trang và tài sản đã duyệt của chuyên mục chỉ được chọn qua allowlist publish. Khi cần bảo toàn đầu ra hiện có trong một nhiệm vụ kiểm thử, dùng bản sao dự án cô lập dưới `_audit/`, giữ nguyên cấu hình dự án và profile.

Metadata `draft: true` không thay thế hàng rào xuất bản. `publish_public.yml` chỉ cho phép đầu ra công khai đã duyệt và tiếp tục chặn `_quy_trinh` lâu dài. Không liên kết tài liệu điều hành từ trang dành cho người đọc, không khai báo resources quét cả cây chuyên mục.

Tuân thủ `quy_trinh_xay_dung/quy_trinh_xuat_ban_website.md`. Chỉ dùng `zo_publish.py check` khi kiểm tra; `prepare`/`publish`, staging, commit và push cần yêu cầu riêng. Không dùng `_publish_exclude.md` hoặc `.gitignore` làm hàng rào public.

## ?nh ??i di?n g?i m?i

Khi chu?n b? d?ng QMD/HTML cho g?i m?i, b?t bu?c th?c hi?n m?c ?Ch?n ?nh
??i di?n khi d?ng g?i m?i? trong quy tr?nh 02 c?a kh?a: ?? xu?t theo n?i
dung, ch? tr? duy?t, r?i khai b?o `giao_dien/anh_bia.json`. Kh?ng k? th?a
?nh g?i m?u. `zo_course_cover.py` l? c?ng binding tr??c/sau adapter HTML;
kh?ng s?a hash ho?c t? ghi approved ?? v??t y?u c?u duy?t.

## Component shell không phụ thuộc tính năng của gói mẫu

Khi dựng/hiệu chỉnh HTML, áp dụng 07/6 và DRAWER-ICON01 trong hợp đồng kit: nút mở mục lục chỉ icon theo shell canonical, độc lập với việc gói có PDF. Cổng template/post-render dùng zo_web_2027_shell.py; phải kiểm kích thước, hình thức, tên truy cập và bàn phím/resize sau đổi view, có ca trang chưa PDF. Không dùng “click được”, cùng CSS hoặc PASS lĩnh vực khác thay kiểm component; không kéo thêm PDF/hình chỉ để nhận giao diện nút.


## GRAPH-G03-01 — khung và tỉ lệ đồ thị theo G03

Chủ trì chọn G03 làm mẫu ngày 17/10/2026. Áp dụng 07/6.1.2: preset `lesson-g03` của công cụ đồ thị, `set_lesson_graph_size` của adapter và CSS dùng `--figure-em`; không dùng width:auto của bản sửa trước. Giữ bố trí hình ghép, nội dung toán, bìa và BBT. Kiểm giá trị kích thước thật ở desktop/mobile cùng đối chứng G03, thử âm sai preset/hệ số/CSS. Trạng thái và bản xem tại 03; HTML sửa chưa tự là PDF đồng bộ, nghiệm thu hoặc xuất bản.


GRAPH-G03-02 (18/10/2026): bảo toàn đối chứng bằng bản chụp/số đo, không giữ lỗi hiển thị trong nguồn hiện hành. Cổng lesson_display_checks áp dụng đủ G01–G04, bao gồm ảnh không có figure. G03 gọi apply_graph_display như các gói khác; kiểm đủ 11 ảnh trên desktop/mobile, sáu ảnh cũ giữ geometry và năm ảnh sửa nhận cùng tỉ lệ. Không dựng lại TEX/SVG/PDF khi chỉ sửa lớp đặt ảnh.


## Biên tập thuật ngữ và câu chữ — EDITORIAL-20261018

Mọi nhiệm vụ viết/sửa/rà nguồn người học trong chuyên mục gọi 07/6.1.6 và 02/Rà thuật ngữ, gồm cả Nhà/D0 và nguồn include. Dùng tập xác định khi đúng nghĩa; phân biệt tập đang xét và điều kiện biến. Đọc ngữ cảnh, chuyển lời điều hành thành hành động rõ, bảo toàn điều kiện toán và điều hướng; không thay từ hàng loạt rồi coi là đã rõ nghĩa. Mẫu/bảng kiểm hiện hành 1.4/1.7 có B24. Cổng `zo_course_editorial.py` nối CLI nguồn và HTML; hồ sơ rà hết khớp thì đọc lại phần thay đổi, không tự gia hạn hash. Giữ nghiệm thu và fingerprint lịch sử; phép đảo G01 chỉ dùng để so sánh trong bộ nhớ, không dựng lại lời văn cũ.


Sau NUMBERING-20261018, G01–G04 kiểm số hiện hành bằng zo_course_numbering_selftest.py và cổng zo_course_labels.py. Bảng di trú ap_dung_he_nhan.json giữ nguyên làm bằng chứng của quy tắc cũ; không dùng inventory đánh số theo chức năng của bảng ấy để chứng nhận số mới.
