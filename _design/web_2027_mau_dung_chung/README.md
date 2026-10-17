# Mẫu web dùng chung — khóa Ôn thi Toán THPT 2027

**Tiếp quản sau phát hành 15/10/2026:** bản tích hợp Nhà/D0/G01/G02 đã
xuất bản; trạng thái và hồ sơ khép việc ở mục A của bảng điều hành 03.
Ảnh học trực tiếp hiện dùng `hoc_truc_tiep_buoi_hoc.svg` cùng PNG nguồn;
minh họa `hoc_truc_tiep_trao_doi.svg` bên dưới là mốc lịch sử đã nghỉ dùng.
Thư viện bìa giữ đủ năm tỉ lệ, bản vuông do chủ trì thay; manifest hiện
hành ở `2027/giao_dien/bo_anh_bia.json`. Không dọn ảnh chỉ vì trang không
hiển thị ảnh đó. Các đoạn chờ xem của mốc cũ không phải trạng thái hiện tại.

**Home — bố cục đọc được giao ngày 14/10/2026:** QMD đặt “Hiểu vì sao.
Tự giải quyết.”/“Dành cho ai?” trong hero, Cách học ngay sau danh mục.
CSS Home scoped cho sáu panel trắng–xám trắng; hàng Cách học một cột toàn
chiều ngang ở mọi viewport, kiến thức/FAQ có khung riêng bo góc xen nền.
Bốn nhãn động từ đã bỏ. Giữ thẻ/CTA HOM-C01, các chữ/ID/đích khác, đồng hồ,
logo/font và nguồn ba trang học liệu. SVG học trực tiếp được quản lý tại
`2027/assets/illustrations/hoc_truc_tiep_buoi_hoc.svg`, QMD nạp ảnh native;
adapter chỉ chuẩn hóa wrapper/caption Quarto. Mẫu thử được chỉ định chỉ là
đối chiếu thiết kế, không phụ thuộc build. Guard HOM-L01 ở `kiem_thu.md`,
trạng thái/kết quả ở 03; không tự nghiệm thu/phát hành hoặc nâng Design 0.5.

**DH_038 — nguồn biên tập Nhà là QMD native:** `2027/index.qmd` sở hữu
tiêu đề, đoạn văn, danh sách, FAQ, lời Ủng hộ và vị trí các vùng; không còn
include toàn trang HTML sinh. YAML chỉ cấp dữ liệu danh mục/mạch/mốc thi
và dữ liệu Gateway còn dùng. Ba partial `home_countdown.qmd`,
`home_catalog.qmd`, `home_strands.qmd` là component dữ liệu/UI sinh tự động.
`scripts/zo_home_qmd.py` nối DOM native với giao diện đã có, không chứa
câu chữ biên tập. Không quay về template hoặc nguồn YAML câu chữ Nhà.
Hướng vận hành ở README Nhà, trạng thái/bản xem ở 03; QD_035 giữ nguyên.

**Home — tinh chỉnh phản hồi buổi sáng 12/10:** template/dữ liệu/generator
Home dùng ngôn ngữ người học, catalog ngay dưới bìa. Theo yêu cầu 14/10,
thẻ không còn là liên kết phủ ảnh/nội dung: chỉ dòng hành động là anchor
native, còn toàn thẻ vẫn phản hồi hover/focus-within. CSS Home riêng bỏ nền hover sáng và gạch chân, giữ
focus/trạng thái chọn/nút vàng; nhãn ngày 13px nowrap/căn tâm. Hợp đồng và
guard HOM-R01 ở `kiem_thu.md`, hướng vận hành ở README Nhà, trạng thái tại 03.
Phạm vi lượt 12/10 chỉ là Home. Yêu cầu 14/10 đồng bộ riêng điều hướng
toàn khóa trên D0/R1: `course-navigation.css` dùng hover đổi màu chữ/icon,
không nền hoặc gạch chân; trang hiện tại giữ chữ đậm và `aria-current`.
Không suy rộng sang rail/nội dung khác hoặc dùng QA đồng hồ cũ chứng
nhận bản mới. Không tự nâng Design 0.5/đổi mốc thi/PDF/phát hành.

**Bổ sung đồng hồ Home, 12/10/2026:** theo yêu cầu chủ trì, nguồn
`program.exam_countdown` cho phép mốc tham chiếu lịch Toán 2026 chuyển
sang năm 2027, bắt buộc ghi chưa phải lịch chính thức. Thay riêng guard
Home cũ buộc đồng hồ trống; không đổi palette, logo, phân cấp tiêu đề hay
D0/R1. Generator kiểm mốc, CSS/JS Home riêng thực thi; hướng vận hành và
đổi sang lịch chính thức tại README Nhà, trạng thái/bước tiếp chỉ ở 03.

**DH_028 — Home biên tập từ mẫu nhập ngày 12/10/2026:** chỉ trang Nhà chọn
`editorial-home-2027`; tại mốc đó generator từng đọc template HTML và
danh mục thật; DH_038 thay nguồn biên tập bằng QMD native, adapter vẫn nhận
raw Quarto mới và dùng CSS/JS riêng `course-home-landing.*`.
Hướng dẫn hiện hành ở `2027/giao_dien/README_web_2027.md`; checker mới
`zo_web_2027_home_landing_check.py` thay guard bố cục Home cũ trong phạm vi
này. Không đổi token/logo/font/kiến trúc của D0/R1, không áp phân cấp tiêu đề
chưa duyệt; bảng và ba biểu tượng điều hướng đã duyệt giữ guard chung.
Ảnh hành trình là minh họa ý niệm, không dùng làm dữ kiện toán học. HTML nhập
chỉ tham chiếu, không chạy JS hay đưa thẻ mô phỏng lên trang thật. Trạng thái
và bước tiếp chỉ ở bảng 03; chưa duyệt HTML, PDF, root docs, Git hoặc release.

**QD_032 — điều hướng khóa học đã duyệt:** bốn adapter Nhà/D0/G01/G02 gọi `scripts/zo_web_2027_navigation.py` sau khi dựng/rebase nội dung. Module thay hai liên kết toolbar cũ bằng Nhà → Danh sách → Đầu trang; CSS/JS riêng `course-navigation.*` chỉ tác động bốn trang, không đổi template của Gateway. Quy tắc tại 07; trạng thái tại 03/DH_027. Không áp dụng phân cấp tiêu đề mẫu chưa duyệt. Không JavaScript vẫn có danh sách native và liên kết thật. Guard tại `zo_web_2027_navigation_check.py`; không dùng mẫu audit làm runtime.

**RAD-01 / DH_024 — căn bậc hai mất cân đối:** dùng alias font `ZOMath` để thực sự chọn STIX đã có, không generic `Math`; bù cỡ glyph căn inline có số mũ theo phạm vi trong `web-shell.css`, giữ cỡ radicand và native baseline. Căn trong phân số/mũ hoặc cấu trúc cao/lồng không nhận bù này. Cổng chung ở `zo_math_notation.py` nối cả bốn adapter; hồ sơ nguyên nhân/guard tại `kiem_thu.md`. Không đổi toán, vùng đọc, font khóa hoặc receipt; trạng thái/HTML hiện hành chỉ ở 03. Lượt bảng QD_030 dưới đây vẫn có hiệu lực, QA bảng không chứng nhận tỉ lệ căn.

**QD_030 — Bảng theo chức năng, toàn khóa:** quy tắc ở 07/6.1.1; binding `profiles/course-tables.json`, CSS `course-tables.css` và bộ nối `scripts/zo_course_tables.py` dùng cho Nhà/D0/G01/G02. Không ép trái mọi header, không bỏ bảng có link. D0 bảng dấu native từ JSON hiện hành. Trạng thái lượt DH_023 và bước tiếp theo chỉ ở 03; các mục DH_021 bên dưới là lịch sử, không hạn chế phạm vi mới được giao. Design 06/07 khóa, shell/toán/ID/PDF không đổi.

**Lịch sử — DH_021/QD_028:** đối sánh và sửa có mục tiêu R1-G01/G02 theo báo cáo M01–M48; DH_022 tiếp quản ký pháp/số mục, DH_023 tiếp quản bảng. Chỉ 03 sở hữu trạng thái/bước tiếp hiện hành; giới hạn “không sửa Nhà/D0” của DH_021 không hạn chế nhiệm vụ bảng bốn trang được giao sau đó. Thiết kế 9/10 giữ nguyên ngoài phạm vi tinh chỉnh được giao; chưa khóa Design 0.5.

**QD_025:** nhãn/owner/số lấy từ bộ điều hành toàn chương trình (kế thừa QD_023, thêm Gợi mở), không từ tên legacy hoặc số hộp của kit. G01 dùng binding `giao_dien/he_nhan.json`; G02 dùng binding riêng 59 nhiệm vụ. Controller hỗ trợ Ôn nền cấp gốc của cả hai; cấu trúc sâu chỉ giữ tương thích lịch sử.

Ngày cập nhật tài liệu: 13/10/2026. G01, G02, Nhà và D0 đã nối opt-in vào đường dựng nguồn; G02 theo DH_019, không còn chỉ có phép chiếu audit. Không phải toàn bộ Ngôn ngữ thiết kế 0.5 đã khóa. D0 theo DH_018/QD_027, giữ khảo sát tự nguyện/nội dung duyệt và map riêng; HTML mới chờ xem riêng.

Kiến trúc/trạng thái/nhiệm vụ theo [bộ điều hành khóa](../../content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/README.md); 01 sở hữu đường học, 07 sở hữu cấu trúc trang. README này giữ đường dùng kỹ thuật và bằng chứng, không điều hành khóa song song. Bài học/Luyện tập không xen kẽ; số vùng/view và nội dung từng gói không phải mẫu copy.

Bộ này tách hình thức đã được duyệt ở G01 khỏi nội dung riêng từng trang. Không mở lại vòng chọn hướng A/B/C; 1 điểm còn lại là dư địa tương lai, không phải điều kiện chặn.

**QD_033 hiện hành cho đường học:** lấy quy tắc và 14 tình huống từ 01/2.2.1–2.2.2; cổng thay thế/bằng chứng ở 02/1.2 theo QD_022. Bốn khu vực có chức năng khác nhau, không bắt buộc hoàn thành tuần tự; điểm vào theo nhu cầu, mức chuẩn bị và bằng chứng hiện có. Hỗ trợ độc lập được gọi theo ngữ cảnh; khi đang Kiểm tra phải tự lực, kết thúc lượt và giữ bài làm ban đầu trước nhận trợ giúp. Lưu bằng chứng tại Điểm dừng khác ghi Nhật kí; chỉ thêm link quay lại đề khi hai vị trí thực sự tách biệt. Các mốc DH_015/016/019/020 và QA QD_021 là lịch sử, không chứng nhận nguồn/HTML đã đạt QD_033; việc tiếp theo chỉ ở 03. Xác minh registry điều hành trước dựng/kiểm xin duyệt.

## Nhà canonical — DH_017

G02 canonical DH_019 dùng `scripts/zo_web_2027_g02_production.py`, cùng builder nhịp/binding với preview; không lấy HTML audit làm nguồn. [Hướng dẫn G02](../../content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g02/giao_dien/README_web_2027.md) có lệnh hiện hành. Hàng rào kiểm thêm nhịp Cách học/Khởi động, tổng quan ba chặng, nhãn thừa và kiểu chữ/giấy/bảng đối chiếu trực tiếp G01–G02. Tài liệu/QA mới không tự thành chủ trì duyệt hoặc promotion.

Nguồn và đường dựng hiện hành: [README Nhà](../../content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/giao_dien/README_web_2027.md). Adapter `zo_web_2027_home.py` tái dùng map/thuật toán Nhà và toàn bộ shell/font/token/footer; chỉ nhận raw Quarto vừa dựng. `zo_web_2027_home_check.py rebuild/preview/check` kiểm cô lập, không đọc audit cũ để sinh nội dung. Nhãn trùng tiêu đề bị ẩn, drawer chỉ biểu tượng, SVG bìa trong suốt/khung riêng. Header/CSS/controller G01/G02 không thay. Trạng thái/HTML và bằng chứng ở 03; chưa chủ trì duyệt bản mới, PDF hoặc phát hành.

## Điểm xem lịch sử

Đường D0 hiện hành ở [README vận hành D0](../../content/thpt/on_thi_toan_thpt/hoc_lieu/d0/giao_dien/README_web_2027.md).
Adapter `zo_web_2027_d0.py` nhận raw Quarto mới; `zo_web_2027_d0_check.py`
dựng/đổi URL xem/kiểm nguồn và browser. Không tải controller R1 hoặc script D0 cũ.

**FB036 — lịch sử 08/10, trạng thái hiện hành chỉ ở 03; đường học theo QD_033:** G01 được sửa nguồn và đồng bộ HTML cục bộ tại mốc lịch sử;
G02 được đối sánh lại. Hai bản sửa chờ chủ trì xem, không tự kế thừa nghiệm thu FB033.
Hồ sơ/lỗi/giới hạn: [`pair refinement`](../../_audit/zo_web_pair_refinement_2026-10-08/README.md).
Quy tắc chung scoped G01/G02 tại `profiles/r1-consistency.json`,
`r1-consistency.css` và `scripts/zo_web_2027_consistency.py`.
Các đoạn FB029–035 dưới đây là lịch sử; receipt FB033 giữ nguyên để đối chiếu,
không chứng nhận HTML FB036. Chưa PDF, phát hành hoặc Design 0.5.

**Mốc duyệt lịch sử G01 FB033:** chủ trì đã duyệt HTML FB032. Đường HTML dùng tại thời điểm đó:
`docs/content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/index.html`; receipt tại
`content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/giao_dien/web_2027_accepted.json`.
G01 đã tích hợp nguồn opt-in, không còn chỉ là prototype. Các link audit bên dưới
là lịch sử hoặc preview của trang khác. Nhà/G02/D0 và PDF không được suy là đã
chuyển production từ mốc này. Hợp đồng dùng lại và lệnh kiểm/dựng cô lập ở
`hop_dong_vung_doc.md`, `kiem_thu.md`; chưa khóa 0.5.

Lịch sử FB029: [ma trận G01/G02 và hai HTML đối sánh](../../_audit/zo_web_2027_g01_g02_doi_sanh_2026-10-08/index.html). Khoảng trống Nền/Nhật kí/CP/Ôn lại là hiện trạng lúc đó, đã được sửa nguồn sau FB034–036; chưa tự thành nghiệm thu toàn gói. Hợp đồng kiểm và lịch sử lỗi ở [doi_sanh_lien_goi.md](doi_sanh_lien_goi.md). Không dùng các mốc dưới đây ghi đè ứng viên FB036.

- [HTML Nhà khóa mới](../../_audit/zo_web_2027_tuy_chinh_2026-10-08/home-reading.html): Nhà/footer đã được phản hồi rất tốt; chỉ tinh chỉnh câu nhận diện và thanh chọn nền theo FB-027.
- [G01 cùng tùy chỉnh mới](../../_audit/zo_web_2027_tuy_chinh_2026-10-08/g01-kit.html): áp dụng thành phần giao diện chung, không đổi nội dung/vùng đọc/luồng.
- [Nhà có footer trước tinh chỉnh](../../_audit/zo_web_2027_footer_2026-10-08/home-reading.html#site-footer): mốc đã được chủ trì phản hồi “Tốt, rất tốt”; giữ nguyên.
- [Nhà khóa trước footer](../../_audit/zo_web_2027_mau_dung_chung_2026-10-08/home-reading.html): giữ nguyên làm mốc đối chiếu.
- [G01 dùng bộ khung chung](../../_audit/zo_web_2027_mau_dung_chung_2026-10-08/g01-kit.html): đối chứng khi tách mã, không phải một hướng thiết kế mới.
- [G01 đã duyệt 9/10](../../_audit/zo_design_web_2027_discovery_2026-10-07/g01-reading.html): giữ nguyên, không ghi đè.
- [Mốc duyệt](../ngon_ngu_thiet_ke_zo_math_0_4/09_nhat_ki/moc_thiet_ke_web_2027_da_duyet_2026-10-08.md), [báo cáo lượt này](../../_audit/zo_web_2027_mau_dung_chung_2026-10-08/bao_cao.md).

## Cái gì dùng chung, cái gì phải lập riêng?

| Lớp | Nguồn | Trách nhiệm |
|---|---|---|
| Giấy đọc, chữ, khối chức năng, cỡ hình | `reading-regions.css` | Hình thức từ G01 đã duyệt; một cấp inset |
| Bìa, rail, toolbar, drawer, section ủng hộ | `web-shell.css`, `templates/*.html.tpl` | Khung chung, không chứa kiến thức của gói |
| Nền đọc, sắc xám, bàn phím, đóng/mở drawer | `site-ui.js` | Có JS thì tăng tiện ích; không JS vẫn đọc và đi theo link được |
| Tùy chỉnh trực tiếp theo FB-027 | `templates/appearance-inline.html.tpl`, `appearance-inline.css` | Sáu radio tròn tô chính màu nền, trạng thái chọn bằng viền; Sắc xám là nút biểu tượng có aria-pressed; tên chỉ ở ngữ nghĩa/tooltip |
| Luồng R1 và nhánh quay về điểm dừng | `r1-controller.js` | Chỉ cho trang R1 đúng hợp đồng; **không nạp vào trang Nhà** |
| Nhịp đọc và điều hướng trang Nhà | `profiles/course-home.json`, `course-home.css` | Bản đồ theo nội dung thật, không sao chép 12 view của G01 |
| Footer website | `templates/site-footer.html.tpl`, `site-footer.css` | Tách khỏi Ủng hộ/nội dung học, lấy link và bản quyền từ `website.page-footer` đang có; chỉ bật cho Nhà trong lượt FB-026 |
| Dựng/kiểm preview | `scripts/zo_web_2027_preview.py`, `scripts/zo_web_2027_check.py` | Nguồn lâu dài ở repo; đầu ra chỉ trong `_audit` |

Đọc [hợp đồng vùng đọc](hop_dong_vung_doc.md) trước khi nhân bản và [hướng dẫn kiểm](kiem_thu.md) trước khi bàn giao. Không sao chép 154 vùng của G01 sang gói khác. D0 cũng không được ép thành một gói R1.

## Dựng lại các lượt thử nghiệm lịch sử

Chạy từ gốc `E:/zo_math`:

Lượt FB-027 đã được chốt qua FB028 (lệnh lịch sử, không ghi đè mốc để cập nhật bản mới):

```powershell
python scripts/zo_python.py scripts/zo_web_2027_preview.py --output _audit/zo_web_2027_tuy_chinh_2026-10-08 --g01-reference _audit/zo_design_web_2027_discovery_2026-10-07/g01-reading.html --ui-baseline _audit/zo_web_2027_footer_2026-10-08/home-reading.html
python scripts/zo_python.py scripts/zo_web_2027_check.py --preview _audit/zo_web_2027_tuy_chinh_2026-10-08
```

`--ui-baseline` chỉ cho phép đổi hai nhóm node đã được yêu cầu: câu nhận diện ở rail/footer và `.appearance` cùng stylesheet cục bộ. Phần DOM còn lại, toàn bộ main, CSS vùng đọc/bìa/nav/Ủng hộ/footer và controller R1 giữ nguyên, có so hình học và ảnh vùng đọc. Nội dung câu mới nằm tại một hằng `BRAND_THOUGHT` trong builder để rail/footer/G01 không lệch nhau. Không tự nâng 0.5.

Các lệnh bên dưới mô tả lượt trước, không ghi đè audit đã duyệt để cập nhật UI mới. Template dropdown cũ chỉ giữ cho chế độ đối chiếu tương thích; điểm xem hiện hành dùng dãy màu trực tiếp.

```powershell
python scripts/zo_python.py scripts/zo_web_2027_preview.py --output _audit/zo_web_2027_mau_dung_chung_2026-10-08 --g01-reference _audit/zo_design_web_2027_discovery_2026-10-07/g01-reading.html
python scripts/zo_python.py scripts/zo_web_2027_check.py --preview _audit/zo_web_2027_mau_dung_chung_2026-10-08
```

Builder đọc HTML hiện hành để lấy nội dung và kiểm với dữ liệu canonical của trang Nhà. Nó **không render Quarto**. Nếu nguồn/đầu ra lệch, phải dừng và báo, không âm thầm sửa hoặc render production. G01 đối chứng là đầu vào được truyền rõ và khóa SHA-256; script không nhập builder/CSS/JS từ audit cũ. Khi tích hợp production sau này, phải có adapter từ QMD canonical, không dùng HTML audit làm nguồn chạy lâu dài.

Lượt bổ sung footer riêng (không ghi đè mốc trước):

```powershell
python scripts/zo_python.py scripts/zo_web_2027_preview.py --output _audit/zo_web_2027_footer_2026-10-08 --g01-reference _audit/zo_design_web_2027_discovery_2026-10-07/g01-reading.html --footer-baseline _audit/zo_web_2027_mau_dung_chung_2026-10-08/home-reading.html
python scripts/zo_python.py scripts/zo_web_2027_check.py --preview _audit/zo_web_2027_footer_2026-10-08
```

`--footer-baseline` là đầu vào đối chiếu được chỉ rõ, không phải phụ thuộc runtime. Builder từ chối nếu DOM cũ thay đổi sau khi bỏ đúng footer/stylesheet mới; checker khóa hash trong `footer-before.json`, đo và so ảnh trước–sau. Chỉ CSS dưới `.zo-site-footer` được thêm, không sửa ba stylesheet cũ hoặc JS. Không dùng `assets/html/footer.html` không hoạt động hay nhận `<footer class="prototype-note">` của Ủng hộ là footer website. G01 đối chứng không nhận footer trong phạm vi này.

Logo/phông lấy từ tài sản khóa 0.4 trong repo; bản preview sao chép đúng tệp và giấy phép OFL. Minh họa bìa là SVG của hướng đã duyệt, không lấy tài nguyên specimen 0.3. Thumbnail học liệu dùng bìa hiện hành của khóa; QR và thông tin ủng hộ giữ nguyên. `build-manifest.json` ghi nguồn/hash từng tài sản, nguồn nội dung và ánh xạ link. Đuôi template `.html.tpl` tránh bị quy tắc ignore `*.html` của repo bỏ qua; không sửa `.gitignore` để giải quyết việc đó.

## Giới hạn và đầu mối điều hành

Footer/FB027 và thiết kế 9/10 đã duyệt được giữ; FB036 mở lại đúng lỗi hai gói, không mở art direction. D0, PDF và phát hành cần nhiệm vụ riêng. Đề xuất 0.5 chưa là phiên bản khóa, không sửa tài sản 0.4 để giả nâng hệ. Thứ tự việc sau cùng chỉ tại bảng 03 của khóa; không dùng lộ trình FB028 làm lệnh tiếp tục.

Không commit, push, xuất bản hoặc chuyển bộ khung thành tài nguyên công khai trong nhiệm vụ này.

## Adapter HTML thử nghiệm R1-G02 — lịch sử FB028

```text
python scripts/zo_python.py scripts/zo_web_2027_preview.py --output _audit/zo_web_2027_g02_2026-10-08 --g02
python scripts/zo_python.py scripts/zo_web_2027_check.py --preview _audit/zo_web_2027_g02_2026-10-08
```

Hai CLI điều phối `scripts/zo_web_2027_g02.py`. `profiles/r1-g02.json` khóa bản đồ nhịp đọc riêng; `r1-g02-adapter.css` chỉ xử lí cấu trúc download/Ủng hộ và khoảng cuộn cho nhãn trên ID nhiệm vụ. Không đổi shell, giấy đọc, typography, token hay controller đã duyệt. 3.1–3.2 ở G02 cùng nhịp thực hiện phương pháp và ví dụ, không phải quyết định sao chép số mục G01.

Nguồn lấy từ HTML G02 hiện có; trước dựng phải đối chiếu toàn chuỗi công thức TeX hiển thị với QMD hiện hành (alt hình được kiểm riêng). Sau dựng so nguyên văn/thứ tự, MathML, ID, heading, trạng thái disclosure, mọi link và thuộc tính download. Chỉ một ID thiết kế mới `ung-ho`; ID nguồn không thay. Các mốc Nhà/G01 cũ giữ nguyên.

G02 chưa có Ôn nền, Nhật kí hay các CP độc lập trong nguồn đang dùng. Không dựng thẻ rỗng/giả hoặc tự thêm nội dung để đủ 12 view G01. Prototype có 10 view, vẫn mở Cách học; đây là bảo toàn hiện trạng, không xác nhận toàn bộ kiến trúc đích G02 đã hoàn tất. Link PDF cũ giữ nguyên, không dựng, đồng bộ hoặc nghiệm thu PDF.


Nhãn ngữ cảnh 17/10/2026: quy tắc tại 07/6.2, giá trị duy nhất tại danh mục kiến trúc/label_contract.display_contract.context_labels. G04/gói mới dùng parent-context-v1; bộ ghép chung zo_course_labels.py, cùng .role. Không dùng nhãn viết riêng hoặc profiles/r1-consistency.json/page_roles cũ để ghi đè nhãn cấp cha. Các giá trị cũ chỉ tương thích gói chưa di trú; không đổi thành phẩm đã phát hành trong lượt G04.
