# HTML canonical của trang Nhà khóa 2027

## Video giới thiệu Bản 01 ngày 16/10/2026

Chủ trì giao biên tập lại hoàn toàn vùng giới thiệu trong hero và đăng video
Bản 01 có giọng B, bộ bìa đã duyệt. Nguồn chữ/vị trí vẫn ở `../index.qmd`;
`.home-video-introduction` trong CSS Home bố trí chữ bên trái, video bên phải,
chuyển thành một cột trên màn hình nhỏ. Không dùng khẩu hiệu cũ của vùng này.

MP4 và ảnh chờ tại `../assets/video/`, lấy nguyên byte từ dự án sản xuất
`E:/zo_math_media/videos/on_thi_thpt_2027/gioi_thieu_khoa_hoc`.
Video dùng controls/playsinline, preload none, không autoplay. Phụ đề động
đã có trong hình, không bật thêm lớp phụ đề trùng. Bản nguồn dựng tiếp tục
được quản lý ngoài kho website; ở đây chỉ lưu hai tài sản công khai cần dùng.
Allowlist chỉ mở đúng MP4 này với ngoại lệ kích thước 20 MiB; validator và
phép gom phụ thuộc nhận cả thuộc tính poster. Dựng lại qua launcher Quarto,
kiểm phần giới thiệu và phát/tua thật trước khi xuất bản lại.

## Tiếp quản sau phát hành — 15/10/2026

Nhà, D0, R1-G01 và R1-G02 đã được xuất bản, kiểm trực tiếp và khép hồ sơ
theo mục A của bảng điều hành 03. Receipt phát hành ghi đúng nguồn/cây
website; hồ sơ khép việc ghi dọn tài sản và kiểm sau phát hành. Các trạng
thái chờ xem hoặc chưa xuất bản trong những mốc bên dưới là lịch sử.
Bộ bìa hiện hành có đủ năm tỉ lệ tại `../assets/illustrations/`; chủ trì
đã thay ảnh vuông và khép tìm ảnh. Dấu kiểm hiện tại ở `bo_anh_bia.json`,
không sửa receipt nhập ảnh cũ để hợp thức hóa ảnh mới.

## Bộ xem đồng bộ và một ảnh bìa — 14/10/2026

Điểm dựng bộ xem hiện hành là `scripts/zo_web_2027_bundle.py`, gọi qua
`scripts/zo_python.py`: `build --output <thư_mục_audit_mới>` dựng cả Nhà,
D0, G01 và G02 từ cùng snapshot nguồn. `check --output <bộ_đã_dựng>` từ
chối nguồn hoặc tài nguyên đã lệch fingerprint. Không lấy ba HTML của
`_audit/home-preview` để ghép vào Nhà mới. Mỗi trang đều quay về cùng Nhà,
giữ query/fragment. Các bản xem cũ chỉ là bằng chứng, không là runtime mới.

Khi dựng bộ HTML, CLI QMD dùng `render --html-only` cho ba học liệu: vẫn
kiểm nguồn/geometry/HTML nhưng truyền `--to html` tới Quarto, không khởi
động nhánh PDF D0. Render không có cờ giữ hành vi cũ. Adapter chạy trong
dự án nguồn cô lập với hàng rào `_audit` hoạt động, rồi mới tạo phép chiếu
liên kết để xem. Nguồn QMD các trang chân trang cũng được đưa vào snapshot.

Trang Nhà chỉ hiển thị `hanh_trinh_nguoi_hoc_toan_3x4.png` ở mọi chiều rộng;
CSS không đổi sang ảnh khác trên mobile. Bộ tài sản gồm đủ năm PNG 1:1,
3:4, 4:3, 9:16 và 16:9 vẫn phải được giữ trong `../assets/illustrations/`
để dùng cho các định dạng truyền thông. Việc gỡ bốn biến thể ở DH_045 đã
phân loại nhầm tài sản còn dùng; đã khôi phục nguyên byte ngày 15/10/2026.
Một ảnh hiển thị không có nghĩa thư viện chỉ được giữ một ảnh. Xem
`../assets/illustrations/README.md`; kiểm bằng `scripts/zo_home_cover_check.py`
qua launcher trước bàn giao hoặc dọn tài sản Nhà. Bản đối chiếu QD_035 và
phụ thuộc được bảo vệ vẫn giữ nguyên. Ảnh dịch vụ theo mục dưới đây.

## Học trực tiếp — mẫu được chủ trì chốt ngày 14/10/2026

Vùng `#hoc-truc-tiep` dùng `.home-service-feature`: lời văn native bên trái,
minh họa riêng bên phải, thông báo chưa mở đăng ký ở dưới. Bỏ nhãn dịch vụ
phía trên nhưng giữ câu xác nhận thu phí. Dấu nhấn trang trí nằm sau câu
thu phí, hai phần CSS `flex:3`/`flex:2` cùng chiều cao, đỏ/vàng 6:4.

Tài nguyên được quản lý tại `assets/illustrations/hoc_truc_tiep_buoi_hoc.png`
và SVG cùng tên: PNG là cảnh tạo bằng imagegen; SVG nhúng PNG và logo vector
đúng từ `07_mau_thi_giac/logos/horizontal_color.svg` vào tranh trên tường.
SVG tự chứa, không đọc audit hoặc file ngoài repository khi dựng. Giữ hình
người đơn giản, hướng dẫn áo đỏ, học sinh áo trắng, bút mực không tẩy và
đèn vàng. Không lấy toàn ảnh mockup thay nội dung HTML.

QMD sở hữu cấu trúc/nội dung/alt; CSS Home sở hữu bố cục responsive. Giữ ID
tiêu đề bằng `.home-qmd-group` để normalizer trả ID từ wrapper về heading.
Không sửa HTML sinh. Nghiệm thu bản dựng và trạng thái ở bảng điều hành 03.

## Bố cục đọc — cập nhật nguồn ngày 14/10/2026

`../index.qmd` đặt phần Hiểu vì sao/Dành cho ai trong giới thiệu đầu trang;
Cách học ngay sau danh mục. `.home-reading-panel` chỉ áp sáu vùng đọc lớn,
không đổi thẻ học liệu hay Ủng hộ. Hàng Cách học là một cột ở mọi chiều
rộng; nội dung bên trong co từ ba cột xuống hai rồi một cột. Các khung
kiến thức/FAQ bo góc xen nền. Học trực tiếp hiện dùng tài nguyên
`../assets/illustrations/hoc_truc_tiep_buoi_hoc.svg` và `.home-service-feature`
theo mẫu chủ trì chốt sau lượt bố cục này; SVG trao đổi cũ chỉ là lịch sử.

Sửa bố cục bằng Markdown/div native và `course-home-landing.css`, không
sửa HTML hoặc nhét toàn trang vào partial. Generator chỉ thêm số trình
bày cho danh mục kiến thức và sinh `home_strands.qmd`; thẻ/countdown không
đổi. `zo_home_qmd.py` giữ class khai ở QMD và chuẩn hóa ảnh native. Bản mẫu
audit chỉ đối chiếu, không tham gia build. Giữ lời văn hiện hành, phục hồi
ID thông báo trạng thái ngay trên câu đã có, không khôi phục lời catalog cũ.
Guard HOM-L01 ở kit; kiểm/dựng vẫn qua launcher và đường cô lập bên dưới.

## Thẻ học liệu — cập nhật hành vi ngày 14/10/2026

Chỉ dòng **Làm khảo sát → / Mở tài liệu →** là liên kết. Ảnh, tiêu đề,
mô tả và nền thẻ không bấm để mở trang; không role/tabindex/handler trên
vỏ thẻ. Toàn thẻ giữ hover viền/bóng/màu tiêu đề, CTA có hover màu/mũi tên
và focus bàn phím, không gạch chân hoặc hộp sáng. Quy tắc này thay hành vi
link phủ thẻ của lượt 12/10 bên dưới. Sửa generator/CSS, không sửa partial
bằng tay; checker Home có ca âm phục hồi whole-card link và kiểm click thật.
PDF D0 ngày 14/10 còn chờ duyệt, không tự thêm link tải lên thẻ khảo sát.

## DH_038 — biên tập trực tiếp bằng Quarto/Markdown

**Sửa câu chữ tại `../index.qmd`.** Đây là nguồn biên tập duy nhất của trang
Nhà: tiêu đề dùng `#`/`##`/`###`, đoạn văn/danh sách/link dùng Markdown;
FAQ dùng heading trong vùng `data-home-tag="details"`. Các thuộc tính của
fenced div giữ lớp giao diện, ID và vị trí; không đổi chúng chỉ để sửa chữ.
Hai đoạn cuối `.home-support-copy` cấp lời Ủng hộ cho component dùng chung.

`../_data/chuong_trinh.yml` giữ danh mục thật, tên mạch, mốc đồng hồ và dữ
liệu Gateway còn dùng; không giữ bản sao bốn đoạn văn Nhà đã di trú.
`zo_build_on_thi.py` chỉ sinh ba component Nhà trong `_partials/`:
`home_countdown.qmd`, `home_catalog.qmd`, `home_strands.qmd`. Không sửa các
partial này bằng tay. `zo_home_qmd.py` ràng DOM Quarto vào đúng giao diện
hiện hành, không chứa lời biên tập, không đổi CSS/JS/toán hoặc ba trang khác.

Template cũ và `_partials/chuong_trinh.qmd` được thay, không còn đường dựng
hay nguồn biên tập hợp lệ. Bản trước di trú được lưu ngoài repo tại
`E:/zo_math_ca_nhan/legacy_backup_archive/ZO_MATH_HOME_QMD_MIGRATION_20261013`;
manifest khóa SHA-256 hai tệp cũ. QD_035 và các bản xem trước vẫn được bảo vệ;
không tự thay bản chủ trì chọn. Trạng thái/kiểm/bước tiếp chỉ ở bảng 03.

Sau sửa chữ: chạy generator kiểm đồng bộ, dựng Home cô lập qua
`zo_web_2027_home_check.py rebuild`, rồi checker Home mới với `--preview`
và **ba** đường dẫn `--d0/--g01/--g02` tường minh. Checker xác minh nguồn
QMD native, hash cả ba component, projection/ID/links và ca âm template/
HTML đổi đuôi/wrapper-only. Không dùng preview lịch sử làm đầu vào build.
Lệnh đều qua `scripts/zo_python.py`. Không tự render root docs hoặc xuất bản.

## Lịch sử DH_028 — nguồn template đã được DH_038 thay thế

### Bố cục biên tập từ mẫu trang Nhà được giao ngày 12/10/2026

### Bản câu chữ được chủ trì duyệt ngày 12/10

Áp dụng toàn bộ bản viết lại đã duyệt trong hội thoại vào template, mô tả
thẻ trong YAML, câu chữ đồng hồ/Ủng hộ Home và nhãn mục lục. Không dùng
“gói khảo sát D0”, mã R1 hoặc thuật ngữ điều hành trong lời hướng dẫn;
mã/URL/ID/trạng thái thật vẫn giữ trong dữ liệu và thuộc tính kỹ thuật.
Điểm dừng được giải thích ngay tại Luyện tập. Mốc đồng hồ và chức năng
hiện hành không đổi; QR, tài khoản và footer vẫn đầy đủ. Đây là biên tập
riêng trang Nhà, không sửa kiến trúc/nguồn D0 hoặc hai gói R1.

Lượt tinh chỉnh trước chưa đạt yêu cầu đọc hiểu của chủ trì; QA 255/255
không chứng nhận câu chữ dễ hiểu. Bản mới phải được so với bản đã duyệt
và đọc toàn trang, ngoài kiểm nguồn tươi/links/browser. Guard Home chặn
mã nội bộ trong chữ hiển thị và có ca âm cố ý thêm D0; không chặn mã trong
metadata. Hồ sơ kiểm bản chốt: `_audit/zo_home_copy_approved_2026-10-12/`.
Trạng thái và điểm xem hiện hành chỉ ở 03; không dùng bản trước để render.

### Tinh chỉnh theo phản hồi buổi sáng 12/10

Nguồn hiện hành đặt danh mục học liệu ngay dưới bìa, rồi mới đến “Biết vì sao.
Tự mình làm được.”; giữ ID, danh mục thật và các đích điều hướng. Không tạo
thẻ giả hay tự gọi một học liệu là mới cập nhật. Câu chữ dành cho học sinh,
không chép ngôn từ điều hành; tìm trợ giúp linh hoạt và quay lại tự làm,
ngoại trừ một lượt Kiểm tra đang diễn ra phải tự lực hoàn toàn.

Một thẻ có một liên kết native phủ ảnh và nội dung, tên truy cập lấy tiêu đề;
hover/focus rõ viền, bóng nhẹ và đổi màu tiêu đề, không đổi kích thước/ảnh.
Liên kết chữ không gạch chân, không có nền hover sáng. CSS chỉ scoped Home,
không sửa CSS shared khiến D0/G01/G02 thay đổi ngoài phạm vi. Nền của nút
hành động, bộ lọc đang chọn và focus bàn phím vẫn có ý nghĩa riêng.
“ngày còn lại” không xuống dòng, giữ 13px và căn theo tâm số; mốc/tính giờ
không đổi. Guard kiểm DOM, pointer thật, focus, native image click/no-JS,
nguồn tươi và sáu viewport; HTML cụ thể vẫn cần chủ trì duyệt.

Hồ sơ lượt này: `_audit/zo_home_refinement_2026-10-12/`; bản xem được ghi ở 03.
Không sửa HTML sinh bằng tay, không dùng bản checkpoint làm nguồn render.

Phần này thay hướng dẫn bố cục/kiểm của DH_017–023 bên dưới cho trang Nhà mới;
các mục cũ giữ để giải thích lịch sử, không dùng bản xem/guard cũ để chứng nhận
bố cục mới. Công việc và trạng thái vẫn chỉ ở bảng điều hành 03.

Nguồn biên tập: `trang_nha.html.tpl`; dữ liệu chương trình/danh mục vẫn tại
`../_data/chuong_trinh.yml` và metadata thật của ba học liệu. Bộ sinh
`zo_build_on_thi.py` nối template vào `_partials/chuong_trinh.qmd`, được
`index.qmd` include. Không sửa partial/HTML dựng bằng tay. Hook Home chọn
`editorial-home-2027`, từ chối raw cũ; kiểm phép chiếu nguyên văn, ID, heading,
disclosure và math từ Quarto tươi trước đổi shell.

Tài nguyên nhận tại `reference/`, biên bản SHA-256 tại
`reference/tai_nguyen_trang_nha_mau_3.json`. HTML nhập chỉ để đối chiếu, không
thực thi JS, không là quy chuẩn hay phụ thuộc chạy. Năm PNG tại
`../assets/illustrations/`; desktop dùng 3x4, mobile dùng 1x1 nguyên tỉ lệ.
Đây là minh họa ý niệm, không phải đồ thị dùng làm dữ kiện toán học. Đồ thị
trên thẻ R1 dùng SVG canonical Design 0.4 của từng gói; D0 dùng logo 0.4.

Giữ font/logo/token/giấy trắng, sáu chấm nền/Sắc xám, ba biểu tượng điều hướng
QD_032, nút mục lục chỉ có biểu tượng và footer thật. CSS/JS mới chỉ cho Home;
không thay phân cấp tiêu đề hoặc đường học D0/R1. Không dùng danh mục giả,
hộp mô phỏng, đăng ký dịch vụ chưa mở hoặc QR từ mẫu nhập.
Guard bảng QD_030 tiếp tục hoạt động; Home không có bảng.

### Đồng hồ thật — bổ sung theo yêu cầu chủ trì ngày 12/10/2026

Một nguồn mốc tại `../_data/chuong_trinh.yml`, `program.exam_countdown`.
Mốc tham chiếu hiện tại: **11/06/2027, 14:30, UTC+07:00**, lấy ngày/giờ
thi Toán **11/06/2026, 14:30** chuyển sang năm của khóa. Đã đối chiếu
Cổng Thông tin điện tử Chính phủ; chưa tìm thấy lịch thi 2027 chính thức
trong lượt xác minh 12/10/2026. Đây không phải dự báo ngày thi chính thức.
Yêu cầu mới cho phép đếm tới mốc tham chiếu có ghi rõ, thay riêng guard
DH_028 cũ buộc để trống đồng hồ; không cho phép trình mốc tạm như lịch thật.

Generator kiểm năm khóa, múi giờ tường minh, nguồn HTTPS và quan hệ với mốc
năm trước, rồi sinh cả thời điểm/nhãn/chú thích. JS chỉ đọc dữ liệu ấy:
tính lại bằng `Date.now()` mỗi giây, khi quay về tab hoặc khôi phục trang;
không cộng tick, không tự suy một ngày mới. Hết mốc về 0, không số âm,
không tuyên bố kỳ thi đã bắt đầu khi đang dùng tham chiếu. Không JS vẫn
hiện ngày/giờ/chú thích, không giả đồng hồ đang chạy. Timer không thông báo
từng giây qua live region; hiệu ứng vòng giây tôn trọng reduced-motion.
Độ chính xác phụ thuộc đồng hồ thiết bị, không có dịch vụ đồng bộ giờ mạng.

Khi có lịch 2027 đã xác minh: cập nhật `status: official`, `target`,
`source_url`, `verified_on` trong cấu hình trên; giữ reference để truy nguyên.
Chạy generator, dựng và kiểm lại; không sửa ngày trong HTML/JS bằng tay.
Bản xem mới: `_audit/zo_home_countdown_2026-10-12/preview/home-reading.html`.
Phạm vi kiểm/duyệt/phát hành vẫn tách biệt; nhiệm vụ và bước tiếp ở bảng 03.

Dựng cách ly qua `zo_web_2027_home_check.py rebuild --output <audit_mới>`.
Sau đó kiểm/ánh xạ bản xem bằng `zo_web_2027_home_landing_check.py --html
<HTML_vừa_dựng> --build <build.json> --output <audit_preview> --preview --browser`
(tất cả lệnh qua `scripts/zo_python.py`). `--preview` hiện dùng rõ các ứng viên
D0/G01/G02 của DH_027; tạo bản sao chỉ đổi đường dẫn để quay về Home mới,
kiểm bảo toàn projection, không sửa nguồn ba trang. Muốn đổi mốc phải sửa mapping và kiểm lại link. Không
phụ thuộc mapping audit khi chạy production. Checker Home cũ đã điều phối
phép kiểm bố cục mới theo build report, không áp guard nhóm đọc cũ.

Bản xem lượt này: `_audit/zo_home_redesign_2026-10-12/delivered/preview/home-reading.html`.
Chờ chủ trì duyệt. Không PDF, root docs, Git hoặc phát hành.

## Lịch sử DH_017–023: bố cục trước DH_028

QD_030/DH_023: Nhà được kiểm trong phạm vi ngôn ngữ bảng toàn khóa (07/6.1.1); hiện không có bảng, không tạo bảng cho đủ kiểu. Adapter dùng chung guard từ chối bảng mới chưa phân loại. Bản xem mới `_audit/zo_course_tables_2026-10-11/html-current/home-reading.html`; công việc và trạng thái ở 03, không suy nghiệm thu từ cùng CSS.

Nguồn văn bản: `../_data/chuong_trinh.yml`; danh mục lấy metadata/hồ sơ gói,
không chép lại tên/phiên bản trong HTML. `scripts/zo_build_on_thi.py` sinh
`../_partials/chuong_trinh.qmd`; `../index.qmd` include một nguồn này.

Ngôn ngữ thị giác dùng bộ khung `_design/web_2027_mau_dung_chung` chung với
G01/G02: giấy trắng một cấp, trục/inset/font/token, rail/drawer, sáu chấm nền
và biểu tượng Sắc xám, câu nhận diện đầy đủ, footer từ cấu hình website.
Nhịp và điều hướng riêng theo `profiles/course-home.json`; không nạp controller
R1 hoặc tạo các chặng/nhiệm vụ của gói vào trang Nhà. Nhãn trùng tiêu đề được
bỏ khỏi hiển thị, nhưng owner/ID vẫn còn. SVG bìa trong suốt theo profile hình
0.4; nền và khung thuộc lớp trình bày, không sửa SVG/toán của G01.

`zo-web-2027-home` là marker opt-in. Hook Quarto đang có
`scripts/zo_web_2027_production.py` chỉ nhận trang Nhà vừa được render trong
danh sách đầu ra; gọi `zo_web_2027_home.py` lấy nội dung tươi, đối chiếu dữ liệu
và phép chiếu nguyên văn/thứ tự/ID/heading/disclosure trước đổi shell.
Không có phụ thuộc runtime vào HTML audit, nguồn specimen 0.3 hoặc docs cũ.
Mất marker/nội dung canonical phải FAIL, không âm thầm quay về giao diện cũ.

Hai gói R1 hiện là **bản xem trước** trong danh mục; trạng thái này không đổi
`workflow.production`, nghiệm thu hoặc quyền phát hành. D0 giữ HTML-only,
tự nguyện và đứng đầu danh mục. Liên kết gói R1 vào `bat-dau`, không vào tên
view cũ `cach-hoc`. ID/URL cũ được giữ.

## Dựng và kiểm

Luôn gọi Python qua `scripts/zo_python.py` từ gốc repo.

1. `scripts/zo_build_on_thi.py --check`: xác minh dữ liệu/partial/bìa đồng bộ.
2. `scripts/zo_2027_governance_check.py --self-test --report <audit.json>`:
   kiểm điều hành, không nghiệm thu HTML.
3. `scripts/zo_web_2027_home_check.py rebuild --output <audit_mới>`: sao nguồn
   và cấu hình vào cây cô lập, render đúng trang Nhà bằng `zo_quarto.py` với
   profile `on-thi-preview`, chạy hook mới. Không ghi đè root docs/Git index.
4. `scripts/zo_web_2027_home_check.py preview --html <HTML_canonical_vừa_dựng>
   --output <thư_mục_preview> --g01 <HTML_G01_hiện_hành> --g02 <HTML_G02_hiện_hành>`:
   chỉ ánh xạ liên kết của bản xem, không đổi nguồn hoặc đầu ra canonical.
5. `scripts/zo_web_2027_home_check.py check --html <preview/home-reading.html>
   --build <audit_dựng/build.json> --output <audit_kiểm_mới> --browser`: kiểm
   projection, nguồn tươi, tài nguyên/link/fragment, fixture và Edge 7 độ rộng,
   scroll, drawer/keyboard/resize, màu/Sắc xám/reload, no-JS và footer.

Checker ra mắt cũ `zo_check_on_thi_launch.py` kiểm mốc trước chuyển kit và cả
PDF/root website; không dùng PASS lịch sử của nó để nghiệm thu trang Nhà mới.
Quy trình phát hành vẫn là nhiệm vụ riêng. Không dùng số PASS HTML thay kiểm
PDF, duyệt của chủ trì hoặc thử trên Safari/Firefox/thiết bị thật/screen reader.

Trạng thái/bằng chứng hiện hành chỉ ở 03 của bộ điều hành; lượt này DH_017.
Các preview/footer/FB027 trước giữ nguyên lịch sử, không ghi đè để tạo bản mới.
