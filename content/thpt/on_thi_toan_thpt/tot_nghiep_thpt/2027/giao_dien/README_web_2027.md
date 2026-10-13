# HTML canonical của trang Nhà khóa 2027

## DH_028 — bố cục biên tập từ mẫu trang Nhà được giao ngày 12/10/2026

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
