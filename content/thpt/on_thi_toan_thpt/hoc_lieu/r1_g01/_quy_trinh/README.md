# R1-G01 — ứng viên Quarto v1.3

**Bộ hiện hành đã đồng bộ — 15/10/2026.** Cả tám PDF đã dựng từ QMD hiện hành,
đạt 17/17 phép kiểm mỗi tệp. Bản đầy đủ có 80 trang;
bản học sinh có 60 trang. Thẻ tải lấy số trang thực tế và
trạng thái provenance từng tệp. Nguồn hình HTML/PDF cùng bộ vector 0.4; BBT
dựng native từ JSON. Thiết kế chung kế thừa D0 đã được chủ trì duyệt; chủ trì
đã duyệt dựng 14 biến thể và yêu cầu xuất bản bốn trang lên zomath.vn.
Hồ sơ hiện hành: `ho_so/pdf_bundle_review.json` và `ho_so/pdf_full_review.json`.
Mọi trang màu đã được bao phủ bởi kiểm thị giác hoặc đối chiếu pixel vùng thân
đã xem; kiểm xám đại diện từng biến thể và các trang hình/bảng/cuối của bản đầy đủ.
Chưa in giấy, quét QR bằng điện thoại hoặc phản biện toán độc lập toàn gói.
Đang thực hiện xuất bản; chỉ báo cáo triển khai thành công mới xác nhận đã lên website.
Các trạng thái chưa PDF/chưa promotion/chờ duyệt ở phần lịch sử bên dưới chỉ
mô tả thời điểm của lượt ấy, không phải trạng thái bộ hiện hành.

Kiểm nhanh trước biên dịch: `python scripts/zo_python.py -B scripts/zo_pdf.py preflight
content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/index.qmd --variant full`.
Cổng chung `scripts/zo_course_release_audit.py --preflight --output <thu_muc_bao_cao>`
kiểm cả 16 cấu hình bằng TeX, không dựng lại sách. Lệnh nào cũng gọi qua launcher.


## Lịch sử triển khai trước lượt đồng bộ 15/10/2026

**Hiện hành DH_026/QD_031:** nguồn QMD/layout/binding đã sửa backlog theo owner; Nhật kí độc lập, Toàn văn/Sửa lỗi/Lời giải đúng thứ tự, bỏ hành động đề–đáp án cục bộ thừa, bảng chọn bài dùng chuẩn chung. Bản xem và evidence ở `_audit/zo_pair_backlog_2026-10-11/`; cổng nguồn/DOM `scripts/zo_web_2027_backlog_check.py` chạy trong adapter. Trạng thái chờ chủ trì duyệt HTML; PDF chưa đồng bộ, root docs/receipt/Git không sửa. Mọi mô tả “hiện hành” ở các đoạn dưới là lịch sử trước DH_026; không phục hồi quy tắc đã bị QD_031 thay.

Hiện hành DH_023/QD_030: bảng theo chức năng 0.4, binding chung `profiles/course-tables.json`, guard `scripts/zo_course_tables.py` trong adapter. HTML/kiểm kê mới tại `_audit/zo_course_tables_2026-10-11/`; trạng thái theo 03 của khóa. Giữ sửa ký pháp/số mục QD_029 và guard `zo_math_notation.py`. Các mốc/đường dẫn bên dưới là lịch sử, không chứng nhận bản mới. Chưa PDF học liệu, promotion root docs, Git hoặc phát hành.

**Hiện hành — QD_025 / DH_015:** đã áp dụng bản chốt do chủ trì sửa vào QMD, binding và HTML cô lập. [Bảng áp dụng](ap_dung_he_nhan.md) ghi 69 nhiệm vụ/62 lời giải, Ôn nền độc lập, ba nhịp Cách học và hợp đồng QD_024 ở Kiểm tra. Quy tắc chung có hiệu lực toàn bộ gói của chương trình, không chỉ R1. Bằng chứng hiện hành tại `_audit/r1_g01_ap_dung_ban_chot_2026-10-10/`; dùng `zo_r1_g01_labels_check.py` và `zo_learning_architecture.py labels --self-test` qua launcher. Chờ chủ trì duyệt HTML, không tự kế thừa nghiệm thu. Chưa promotion docs, dựng PDF hoặc sửa receipt. Chỉ bảng 03 sở hữu việc tiếp theo; các mốc bên dưới là lịch sử, không khôi phục quy tắc/câu chữ đã bị thay thế.

## HTML hiện hành — đồng bộ nguồn ngày 08/10/2026

**Nguồn QD_020/DH_011 — lịch sử biên tập:** QMD/manifest/binding và include đã cập nhật, HTML cô lập tại `_audit/r1_g01_bien_tap_2026-10-10/`. Sau đó chủ trì bác bỏ sơ đồ; QD_021 mở lại RD01/RD06, thu hồi xin duyệt đường học. 465/465 không kiểm đúng chuỗi quan hệ; giữ báo cáo gốc nhưng không dùng để chứng nhận đường học mới. QD_022 chỉ yêu cầu kiểm lại phần chịu ảnh hưởng; phần khác xét riêng theo đầu vào/phép kiểm, không khóa hiệu chỉnh. HTML docs/receipt/PDF giữ nguyên; PDF STALE.

**QD_021 — quy tắc hiện hành, trạng thái cũ đã được DH_015 thay thế:** đường học và 14 tình huống lấy từ 01/2.2.1–2.2.2; cổng thay thế/bằng chứng ở 02/1.2. DH_015 đã sửa RD01/RD06 và áp dụng QD_024/025 vào G01; G02 vẫn cần rà riêng. QA lịch sử không chứng nhận bản mới. Theo QD_022 chỉ kiểm lại phần bị ảnh hưởng, không hủy mọi QA hoặc chặn sửa chữa.

Guard biên tập hiện hành: `scripts/zo_r1_g01_editorial_check.py`, qua `scripts/zo_python.py`, nhận `--html`/`--raw` tường minh và `--output` dưới audit; `--browser` kiểm giao diện/ngữ cảnh. Bằng chứng lịch sử `_audit/r1_g01_bien_tap_2026-10-10/qa/editorial-qa.json` không đạt cổng QD_021. Nguồn nội dung là QMD tươi; audit chỉ là đầu ra/baseline kiểm. Bảng T19 đầu Luyện tập đưa hợp đồng HTML lên 19 bảng, giữ kiểm ID/cột/thứ tự. Các inventory/variant PDF phải cập nhật bằng lượt PDF riêng sau khi HTML được duyệt, không đoán số đếm/số trang hoặc sửa provenance. Checker lịch sử 18 bảng không là cổng nghiệm thu HTML mới; không nới guard để giữ số đếm cũ.

Điểm vào điều hành: [README khóa 2027](../../../tot_nghiep_thpt/2027/_quy_trinh/README.md); trạng thái/công việc chỉ ở bảng 03. QD_016–018 là lịch sử hợp nhất tài liệu; QD_020 đã mở biên tập học liệu. Bài học/Luyện tập không xen kẽ.

**Đồng bộ QD_019 — lịch sử:** danh mục thẩm quyền ở [08](../../../tot_nghiep_thpt/2027/_quy_trinh/08_danh_muc_tham_quyen_dieu_hanh.md). Audit G01 ghi 21 RD chưa sửa tại thời điểm rà; trạng thái sau biên tập thuộc QD_020/DH_011/hồ sơ G01. Không coi có đủ CP/N hoặc kiểm bố cục là đường học đã khép.

**FB036 — lịch sử 08/10, bị QD_021 tiếp quản về đường học:** chủ trì yêu cầu mở lại đúng các lỗi
liên gói. QMD, include Nhật kí, bản đồ binding và runtime đã được sửa; HTML cục bộ
đồng bộ tại `docs/content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/index.html`.
Bản sửa chờ chủ trì xem. Receipt FB033 giữ nguyên như mốc lịch sử, không được
ghi lại để làm phép kiểm nghiệm thu cũ PASS. Hồ sơ: `_audit/zo_web_pair_refinement_2026-10-08/README.md`.
Để kiểm bản sửa, dùng `scripts/zo_web_2027_pair_check.py`; lệnh checkpoint FB033
phía dưới chỉ đối chiếu mốc cũ và không phải cổng PASS của FB036.

**Mốc duyệt lịch sử FB033:** chủ trì đã duyệt HTML sau FB031/032:
“Mình đã xem kết quả, tốt.” Bản tại thời điểm đó nằm ở `docs/content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/index.html`,
SHA-256 `8b3a9a1ad532e72951edb415d9ab32a37990a80e13c2d754a2f57028fedc764a`.
Receipt nguồn: `giao_dien/web_2027_accepted.json`; có hash nội dung/ID/toán/runtime/nguồn và phạm vi duyệt.
Các mốc phía dưới là lịch sử xây dựng; receipt FB033 không chứng nhận bytes của HTML FB036 đang có tại cùng đường dẫn.

```text
python scripts/zo_python.py scripts/zo_web_2027_g01_checkpoint.py check --output _audit/zo_g01_checkpoint_check
python scripts/zo_python.py scripts/zo_web_2027_g01_checkpoint.py rebuild --output _audit/zo_g01_checkpoint_rebuild
```

Lệnh thứ hai dựng từ nguồn repository trong mirror tạm, không đọc audit mirror hay HTML cũ làm nguồn;
so mốc đã duyệt và không promotion/ghi đè `docs`. Nguồn QMD/bản đồ/hình/bảng/luồng giữ nguyên.
Nhật kí 14 trường là schema dùng chung; 154 vùng và 12 view là dữ kiện mốc FB033, không ép vào mọi gói hoặc bản sửa sau.
PDF hiện có chưa đồng bộ; chưa nghiệm thu PDF, phát hành hoặc khóa Design 0.5.
Hồ sơ lượt này: `_audit/zo_g01_html_checkpoint_2026-10-08/README.md`.

Mốc đối chiếu được chủ trì chỉ định là
`_audit/zo_web_2027_g01_g02_doi_sanh_2026-10-08/g01-kit.html`, SHA-256
`5c97396dd9656971e442cb60a07aa799935d3233bf2ae15a53ebc57f76c77e3c`.
Không lấy `g01-reading.html`, B2/B3/B4 hoặc HTML cũ làm mẫu thay thế.

Đường dựng HTML hiện hành gồm:

- `index.qmd`: nguồn nội dung toán, nhiệm vụ, ID; Nhật kí 14 trường include từ `../_dung_chung/nhat_ki_hoc_tap.qmd`;
- `giao_dien/web_2027_layout.json`: bản đồ vùng đọc hiện hành và các binding nội dung,
  không phải bản thảo toán thứ hai;
- `_design/web_2027_mau_dung_chung/`: CSS, controller và UI đã được duyệt;
- `giao_dien/assets/`: các SVG trình bày của mốc đã duyệt, khóa bằng checksum;
- `scripts/zo_web_2027_production.py`: hook post-render nhận HTML Quarto vừa dựng,
  kiểm nội dung/ID/công thức/nguồn hình rồi nối vào bản đồ giao diện.

### Hình/bảng opt-in HTML — FB031 ngày 08/10/2026

Chủ trì đã duyệt mẫu FB030 và giao tích hợp vào G01, giữ khung trang đã chốt.
`giao_dien/web_2027_figures.json` chọn 13 nguồn TeX thật, bảng JSON và khung
bìa ngang nhỏ/nền Vàng ZO sáng. Khung là lựa chọn biên soạn, không thêm bộ
chọn cho người học. `scripts/zo_web_2027_figures.py` dựng vector riêng vào
`giao_dien/assets/figures_0_4/`, có manifest khóa đầu vào/font/style/sidecar
và hash SVG. Các SVG/PDF lịch sử trong `hinh/` không bị ghi đè.

Hook kiểm phép chiếu QMD/layout cũ đầy đủ trước khi bộ nối hình thay đúng
payload đồ thị/BBT. Bảng native và MathML lấy từ cùng JSON; giữ caption QMD,
cột loại, giới hạn một phía, lỗi cố ý và ID. CSS hình mới scope đúng marker
production G01; CSS/JS shell, 154 vùng đọc và 14 trường Nhật kí không đổi.

```text
python scripts/zo_python.py scripts/zo_web_2027_figures.py
```

Sau khi dựng, đầu vào không đổi và mọi SVG khớp hash mới được dùng
`--reuse-graphs`. Nếu đầu ra web cùng tên đã tồn tại và cần tái dựng, chỉ dùng
`--force` cho đúng thư mục web riêng này. Bộ nối đổi không buộc tái biên dịch
TeX; receipt ghi riêng hash builder, nguồn vector vẫn phải khớp đầy đủ.
Dựng HTML vẫn qua `zo_qmd.py render` trong mirror/index riêng; không lấy HTML
audit hoặc `docs/` làm nguồn. Audit `_audit/zo_g01_figure_integration_2026-10-08/`
ghi bằng chứng đối chiếu toàn trang và mốc hoàn tác. Đây chưa là nghiệm thu
HTML tích hợp mới, PDF đồng bộ, khóa Design 0.5 hoặc phát hành.

Build thường không đọc `_audit/`, không đọc HTML cũ trong `docs/` làm đầu vào.
Hook chỉ chạy cho HTML G01 nằm trong danh sách đầu ra của lượt render; không
chuyển G02, D0, Nhà khóa hoặc các trang khác. Marker production là điều kiện
bắt buộc của cấu hình G01, ngăn âm thầm quay về shell cũ. Khi nội dung hoặc hình
nguồn đổi, phải kiểm và cập nhật binding trong nhiệm vụ được giao; không nới guard
để bỏ qua nội dung mới. Khoảng trắng sát công thức thuộc binding trình bày và phải
được bảo toàn, không lấy khoảng trắng của một vị trí khác có cùng câu chữ.

HTML có 12 view trong ba nhóm điều hướng. Ôn lại và Nhật kí tách riêng; Nhật kí
dùng đủ 14 trường nguồn. Script legacy tạo sáu mục không được nạp trong HTML mới.
Các mô tả chín thẻ, docking Headroom và CSS riêng ở phần lịch sử bên dưới không
còn mô tả shell HTML hiện hành. Kiến trúc học tập vẫn lấy từ manifest gói và
quy chuẩn khóa 2027, không suy ra từ số thẻ hoặc số vùng đọc.

HTML được dựng qua `zo_qmd.py render` trong mirror với work-tree/index riêng,
kiểm trước khi chuyển riêng đầu ra G01 và runtime cần thiết vào `docs/`.
Bằng chứng và bản sao mốc nằm tại `_audit/zo_g01_source_sync_2026-10-08/`.
Nhiệm vụ này chỉ đồng bộ HTML: tám PDF, metadata số trang và publication chưa
được đồng bộ/nghiệm thu mới. Không gọi các link tải cũ là PDF hiện hành.

## Hồ sơ nền và lịch sử trước đồng bộ HTML

### FB032 — Tinh chỉnh tải PDF và nút drawer

Chủ trì đã xem HTML FB031 và nhận xét tất cả ổn, trừ mục tải PDF và chữ trên
nút drawer. Hook gọi thêm `scripts/zo_web_2027_downloads.py`;
`giao_dien/downloads.css` chỉ scope G01/mục tải/nút đó. Tám thẻ giữ tên,
mô tả, URL và download filename; số trang lấy trực tiếp từ tám PDF đang có.
Desktop ba cột; mobile tên/mô tả trên, số trang và nút tải dưới. Nút drawer
chỉ biểu tượng, vẫn có tên truy cập và giữ JS/luồng bàn phím hiện hành.
Mục tải nói rõ PDF chưa đồng bộ với HTML. Không sửa QMD hoặc PDF để đổi UI.
Hồ sơ kiểm và ảnh: `_audit/zo_g01_downloads_2026-10-08/README.md`.
Hai tinh chỉnh mới chờ chủ trì xem, không làm lại các phần đã được xem ổn.

`index.qmd` là nguồn canonical duy nhất của học liệu v1.3. Nội dung và kỹ thuật đã
hoàn tất theo các lượt nghiệm thu 3D–3F; giao diện ứng viên dùng nhãn “Có thể học”.
Hồ sơ vẫn giữ `publication: pending`: đây là ứng viên ra mắt cục bộ, chưa được
xuất bản công khai và chưa có URL/ngày công bố.

`lich_su/v1_1.json` là hồ sơ bất biến ghi commit đối chiếu và SHA-256 của đủ
40 tệp lịch sử. `lich_su/v1_1_verification_v2.json` giữ nguyên hồ sơ đó và dẫn
xuất 39 tệp bắt buộc cho snapshot release; chỉ `kiem_chung/pdf_build.log` được
xác định đích danh là bằng chứng chẩn đoán cục bộ không bắt buộc.
Không nhân bản HTML/Markdown cũ thành nguồn biên soạn thứ hai ở đây.
Nhãn trạng thái dành cho người học là “Có thể học”; tên hiển thị là “Kết nối hàm số, bảng biến thiên
và đồ thị”. Mã `R1-G01` chỉ dùng cho quản lí nội bộ, đường dẫn và tên tệp kỹ thuật.
Ngoài nhãn và chỉ dẫn tải PDF V1–V2 đã duyệt, không biên tập lại nội dung học thuật.

Mỗi gói có project.id, cấu hình và `_quy_trinh/ho_so/index.yml` riêng.
`extensions.artifact_identity: path` chọn tên receipt/phiên dựa trên đường dẫn;
`extensions.artifact_inputs` bổ sung dữ liệu, hình và filter vào hash PDF.
`extensions.artifact_root_inputs` bổ sung các phụ thuộc dùng chung ở gốc
repository. `extensions.pdf_provenance_manifest` bật manifest canonical được
theo dõi trong Git. Hai dự án cũ không bật lựa chọn này nên giữ nguyên cách xác
định trạng thái và tên receipt/phiên hiện hành.

Checker chung nhận diện cấu hình và kiểm tra tài nguyên; kiểm chứng bảo toàn riêng
được chạy bằng `cong_cu/kiem_chung.py`. Chưa đăng ký adapter nội dung chung mới.
Không suy diễn một module có tên trong cấu hình thành kiểm định sư phạm đã thực hiện.

Bảng biến thiên dùng một JSON canonical cho cả HTML và PDF. Công cụ bảng biến thiên
ZO Math sinh 13 bộ TEX/PDF/SVG. Lớp tích hợp QMD dùng chung trong thư mục công cụ
tra mã `BBT01`–`BBT13`, dùng SVG cho HTML và PDF vector cho LuaLaTeX; adapter
`cong_cu/r1_g01.lua` chỉ khai báo JSON và thư mục tài sản của gói. HTML giữ bảng
ngữ nghĩa trợ năng từ cùng JSON. Chú thích bảng trong QMD giữ đúng HTML (có chỗ
khác title trong JSON). CSS trình bày BBT thuộc công cụ dùng chung, không nằm trong
CSS riêng R1-G01. JSON và 39 tài sản TEX/PDF/SVG vẫn là cấu hình riêng của gói qua
`extensions.artifact_inputs`.
Một nguồn `index.qmd` sinh tám PDF qua cùng pipeline Quarto/LuaLaTeX:

- `index.pdf`: bản đầy đủ, có lời giải;
- `index_hoc_sinh.pdf`: loại toàn bộ phần `#loi-giai` và các vùng `.answer-link`,
  giữ ví dụ, đọc thêm, sửa lỗi và nhật kí theo V3;
- `index_bai_hoc.pdf`, `index_luyen_tap.pdf`, `index_kiem_tra.pdf`,
  `index_sua_loi.pdf`, `index_on_lai.pdf`, `index_loi_giai.pdf`: sáu phép chiếu
  theo phần từ AST của chính `index.qmd`, không có QMD con và không sao chép bản thảo.

Baseline PDF canonical của R1-G01 được chủ dự án nghiệm thu thị giác ngày
2026-09-30 và chốt ở Pha 5C với ma trận số trang: `full` 41, `student` 31,
`bai_hoc` 22, `luyen_tap` 7, `kiem_tra` 5, `sua_loi` 5, `on_lai` 3 và
`loi_giai` 12. Checker phải so sánh toàn bộ ma trận này và metadata hai thẻ tải
  phải khớp tệp thật của đúng mốc đó; 31/41 không phải số trang bắt buộc cho nguồn FB036 đã đổi. Không nới kiểm nội dung thành điều kiện chỉ lớn hơn 0. Khi được giao đồng bộ PDF, cập nhật kỳ vọng theo phạm vi mới và kiểm toàn bộ biến thể/tệp tải thực. Thay đổi nguồn
thuộc fingerprint PDF phải dựng lại đủ biến thể bị `STALE` và đưa manifest
provenance về `CURRENT`; không sửa receipt hoặc manifest bằng tay.

Manifest `r1-section-download-files` trong metadata là nguồn duy nhất cho ranh giới
ID, nhãn, tên tải và `r1-view`. Registry PDF chỉ khai output, branding và thuộc tính
pipeline. Filter từ chối ranh giới thiếu/trùng/sai thứ tự; sau phép chiếu, hash còn
đích được giữ nội bộ, còn hash vượt phạm vi được đổi sang URL canonical từ registry
với đúng `r1-view` và nhãn “mở trên trang học liệu”. Mỗi bản theo phần giữ phần mở
đầu chung, Cách học, đúng phần đã chọn và Nguồn đối chiếu; không mang vùng tải PDF
hoặc khung tài khoản. Luyện tập và Kiểm tra không mang lời giải hay thang chấm.

HTML tải hai tệp trên bằng tên `download` lần lượt là
`R1-G01_hoc_lieu_day_du_v1.3.pdf` và `R1-G01_hoc_va_bai_tap_v1.3.pdf`.
Không tạo bản sao theo tên thân thiện, không dùng in trình duyệt làm PDF chính thức.
Không còn nút/listener in. HTML dùng chín thẻ theo thứ tự Cách học, Bài học,
Luyện tập, Kiểm tra, Sửa lỗi, Ôn lại, Lời giải, Tải PDF, Toàn văn. Tất cả thẻ
dùng chung một cây nội dung canonical và một `tabpanel`; JavaScript chỉ ẩn/hiện
các section sẵn có. Query `r1-view` giữ chế độ xem, hash giữ đích; liên kết hash
cũ vẫn mở đúng thẻ sở hữu đích, còn Toàn văn giữ nguyên chế độ khi đi tới hoặc
trở về từ lời giải. Khi không có JavaScript, toàn bộ nội dung vẫn đọc liên tục.
Hình HTML dùng SVG gốc. Cả mười hình `do_thi_01` đến `do_thi_10` dùng trực tiếp
PDF vector khi dựng PDF học liệu; mỗi PDF và SVG được dựng từ TEX cùng tên bằng bộ
công cụ đồ thị ZO Math tại commit `354fb22`. Không còn tài sản PNG canonical hoặc
pipeline Matplotlib riêng cho bộ mười đồ thị này.

## Vận hành tám biến thể — chỉ chạy khi nhiệm vụ PDF được giao

Từ gốc repository, dùng launcher hiện hành:

```text
python scripts/zo_python.py scripts/zo_qmd.py check content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/index.qmd
python scripts/zo_python.py scripts/zo_pdf.py build content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/index.qmd --variant full
python scripts/zo_python.py scripts/zo_pdf.py build content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/index.qmd --variant student
python scripts/zo_python.py scripts/zo_pdf.py status content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/index.qmd --variant full
python scripts/zo_python.py scripts/zo_pdf.py status content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/index.qmd --variant student
```

Sáu tên variant bổ sung là `bai_hoc`, `luyen_tap`, `kiem_tra`, `sua_loi`,
`on_lai`, `loi_giai`; dùng cùng hai lệnh `build` và `status` ở trên. Registry có
thể có thêm variant đã đăng ký, nhưng tên phải an toàn, output phải duy nhất và nằm
trong thư mục gói. Pipeline từ chối variant không đăng ký, output trùng hoặc đường
dẫn thoát phạm vi. Mọi build vẫn chạy cô lập và chỉ thay canonical sau khi render
và kiểm tra cấu trúc PDF thành công.

Mặc định không truyền biến thể vẫn là `full`. Cấu hình `extensions.pdf_variants`
khai đầu ra/metadata. Manifest `_quy_trinh/ho_so/pdf_provenance.json` theo dõi
nguồn, JSON, hình, filter, cấu hình, pipeline, hash và số trang của đủ tám PDF.
Với gói này, `status` chỉ báo CURRENT từ manifest deterministic; không dùng mtime
hoặc receipt `_audit`. Receipt vẫn được sinh làm bằng chứng dựng cục bộ. Builder
chỉ cập nhật bản ghi của variant vừa dựng sau khi đầu vào sau dựng còn khớp ảnh
chụp trước dựng. Build chạy trong bản sao tạm cô lập dưới `_audit`, chỉ thay đúng
đầu ra sau render thành công; thất bại không xóa PDF cũ. Dự án không bật manifest
canonical tiếp tục dùng hợp đồng hiện hành.

Trước mỗi render: xác nhận không có preview nền ngoài phiên kiểm chứng được quản lí,
ghi hash hai PDF hiện hành. Không render toàn repository thật để kiểm gói này.
HTML dùng `zo_qmd.py render` trong mirror riêng với profile `on-thi-preview`;
đặt đúng Git work-tree/index riêng của mirror khi dùng checker, không staging.
Khi pha đồng bộ PDF được giao, dựng PDF trước lượt HTML tải cuối để resources là đúng bản vừa kiểm. Trong pha HTML-only hiện tại không tự dựng PDF theo chỉ dẫn lịch sử này.
QMD chỉ khai định dạng HTML; PDF được chọn tường minh qua pipeline/profile PDF,
không để preview HTML tự động sinh PDF cạnh nguồn.

Sidebar chuyên mục nằm trong cấu hình nguồn dùng chung, gồm cổng Ôn thi, ấn bản
2027 và học liệu này; profile preview chỉ cấu hình máy chủ cục bộ. Ranh giới public
đã duyệt chỉ chọn đầu ra qua allowlist và tiếp tục chặn hồ sơ nội bộ; trạng thái
“Có thể học” không thay thế `publication: pending` và không phải tuyên bố đã xuất bản.

Nghiệm thu trực quan HTML/hai PDF, chấp thuận thiết kế và chuyển canonical là các
quyết định riêng của chủ dự án, không được suy từ PASS kỹ thuật. Cảnh báo hyphenation
tiếng Việt và cảnh báo lịch sử khóa `/Group` tiếp tục được ghi riêng trong báo cáo audit.

## Hồi quy header PDF và docking HTML legacy — lịch sử

Running header PDF vẫn cần kiểm khi được giao PDF; docking Headroom mô tả shell HTML cũ, không điều hành rail/drawer kit hiện hành. Không khôi phục đoạn HTML dưới đây vào nguồn mới.

Running header dùng template chung một dòng: ZO Math + tên chính thức, không có
nhãn biến thể. Nhãn hai bản vẫn nằm trên bìa/thẻ tải. Checker R1 kiểm tọa độ chữ
trong PDF thật qua `cong_cu/kiem_chung_header_pdf.py`; ưu tiên Poppler
`pdftotext -bbox` và dùng fallback chỉ-đọc bằng `pypdf` khi binary cục bộ thiếu
khả năng này.

Thanh thẻ giữ nguyên node trong slot và bám ở `top: 0`; Headroom chỉ quản lí
Navbar. Khi kéo xuống, Navbar ẩn còn thanh thẻ tiếp tục ở đầu khung nhìn; khi kéo
lên, Navbar xuất hiện lại. Không chuyển node thanh thẻ vào header và không ghép
thanh thẻ vào transform của Navbar.
Kiểm thử qua HTTP local bằng Chrome profile tạm, ví dụ:

```text
node content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/cong_cu/kiem_chung_navbar.mjs --url http://127.0.0.1:8781/content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/ --out _audit/r1_g01_navbar_regression
```

`--chrome` cho phép chỉ định executable khác. Công cụ đo từng khung hình ở
1440/430/390 px, lưu JSON và chuỗi PNG; kiểm cả menu, focus, history, guidance,
liên kết lời giải, bàn phím, no-JS và touch mô phỏng. Đây không phải nghiệm thu
trên thiết bị cảm ứng thật hoặc chấp thuận của chủ dự án.
# Bản đầy đủ PDF — khung D0 dùng chung, 14/10/2026

Theo yêu cầu trực tiếp của chủ trì, dựng riêng `full` từ QMD hiện tại,
kế thừa trang đầu/trang cuối/header/footer D0 đã duyệt qua
`extensions.course_pdf_shell`. Khung là hai template trong `assets/tex/zo-course-pdf-*`;
bộ dựng lấy Bảo trợ từ component HTML nguồn, dữ liệu gói từ QMD/hồ sơ.
Pipeline mirror sao chép đủ include canonical ngoài thư mục gói.

Adapter PDF dùng 20 bảng hiện hành theo ID, giữ số công thức/hình/BBT/
disclosure/liên kết đáp án của AST nguồn. BBT gồm BBT14 mới, dựng native
từ JSON; giữ cả các lỗi có chủ ý và mốc loại. Bảng thường native đủ lưới,
header lặp trên trang tiếp; số trang đích được giải cho bản in. Không
thay QMD/toán để khớp khuôn cũ; QMD chỉ cập nhật số trang bản đầy đủ.

Đầu ra canonical: `index.pdf`; trạng thái full qua `zo_pdf.py status --variant full`.
Báo cáo kỹ thuật/thị giác của bản này ở `_quy_trinh/ho_so/pdf_full_review.json`;
trạng thái hiện hành chỉ ở bảng 03 của khóa. Bảy biến thể còn lại giữ nguyên,
chưa đồng bộ hoặc nghiệm thu mới. Các ma trận 41/31 hay số PASS cũ bên
dưới không chứng nhận bản này. Lệnh dựng:

```text
python scripts/zo_python.py -B scripts/zo_pdf.py build content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/index.qmd --variant full
python scripts/zo_python.py -B scripts/zo_pdf_course_check.py content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/index.pdf
```
