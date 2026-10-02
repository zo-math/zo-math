# D0 — đầu mối chuyển đổi canonical

## Quyết định hiện hành — tích hợp nội dung đã duyệt ngày 2026-10-02

### Điều chỉnh sau góp ý HTML

Theo yêu cầu trực tiếp mới của chủ dự án: bỏ riêng đoạn “Trước khi xem hướng
dẫn…” trong Chuẩn bị; nhãn Bài 00 dùng “Hàm số, đạo hàm, đồ thị” thay “R1”;
tiêu đề tám mạch trong Khảo sát thêm R1–R8. Thanh mạch cuộn ngang được thay
bằng mục lục dùng component `r1-section-toc` và nguồn liên kết `lesson-toc`;
hai cột trên desktop, một cột trên mobile. Không đổi 24 câu hay công thức.
Theo góp ý tiếp theo, bỏ tiêu đề “Hàm số, đạo hàm, đồ thị” trước ví dụ giả
lập trong Chuẩn bị; giữ tên mạch trong nhãn Bài 00 và toàn bộ nội dung ví dụ.
`dieu_chinh_sau_duyet.json` khóa đúng mười một phép thay văn bản QMD được giao;
checker đảo đúng các phép ấy rồi so toàn chuỗi/hash với bản trước sửa, không
ghi đè receipt duyệt gốc. Kiểm HTML cũng đối chiếu toàn chuỗi sau khi hoàn
nguyên đúng các delta được duyệt trên bản DOM kiểm thử, không sửa đầu ra.
Tệp sửa: `index.qmd`, `giao_dien/d0_script.html`, `giao_dien/d0.css`,
`cong_cu/kiem_chung.py`, `cong_cu/kiem_chung_da_duyet.py`,
`cong_cu/kiem_chung_tuong_tac.mjs`, cấu hình QMD và README này;
tệp mới: `_quy_trinh/dieu_chinh_sau_duyet.json`. Preview vẫn chưa xuất bản.
Render và checker nguồn/HTML đạt; runtime phiên sau điều chỉnh đạt 221/221
ở desktop 1366 px, mobile mô phỏng 430/390 px. Ảnh mục lục đóng/mở và các
trạng thái còn lại được giữ trong `_audit/d0_da_duyet_preview/` để nghiệm thu;
hồ sơ Chromium tạm được dọn tự động. Không sửa Downloads hoặc tài sản hình.

Người dùng đã duyệt nội dung `khao_sat_dau_vao_D0.html` và giao tích hợp,
render xem trước, chưa xuất bản. Quyết định này thay thế luồng bắt buộc điều
phối, hướng dẫn 6B/6B.1 và hàng rào cấm toàn bộ đáp án công khai của ứng viên cũ.

- Nguồn biên soạn công khai duy nhất: `../index.qmd`, nhập qua
  `../cong_cu/tich_hop_html_da_duyet.py`; không tái sinh bằng generator 6B cũ.
- `noi_dung_da_duyet.json` giữ hash nguồn được duyệt, hash QMD, dấu kiểm toàn
  chuỗi văn bản/công thức của từng phần và inventory liên kết. Đây là provenance,
  không phải bản văn để biên tập song song. Không cập nhật hash để bỏ qua sai biệt.
- Khảo sát tự nguyện: không cần làm đủ câu, đạt điểm hoặc điền hồ sơ để vào học.
- Giữ 24 câu khảo sát, Bài 00 giả lập, 25 phần đối chiếu thu gọn và lời dẫn đã duyệt.
- Điều hướng: Bắt đầu, Chuẩn bị, Làm khảo sát, Đối chiếu bài làm và Chọn mạch ôn.
  Không tạo thẻ Toàn văn hoặc PDF rỗng, không tự thêm bài học hay ngân hàng thử lại.
- D0 phát hành HTML-only theo quyết định ngày 2026-10-03: không tạo PDF nội dung
  kiểu bản học sinh, thử lại, lời giải hoặc hướng dẫn. PDF kỹ thuật của hình và
  PDF baseline lịch sử vẫn được bảo toàn; chúng không phải biến thể của trang D0.
- Các phần đối chiếu được duyệt là công khai; hồ sơ người tổ chức, ngân hàng thử
  lại và metadata biên soạn vẫn nội bộ, không được đưa vào DOM hoặc resources.
- Liên kết khóa 2027 dẫn đúng `#hoc-lieu-hien-co`; chỉ R1-G01 và R1-G02 có đường
  học trực tiếp. Bảng tám mạch là mô tả chương trình, không phải tám khóa đã mở.
  Module trạng thái giao diện riêng đặt cạnh bảng, ghi rõ R2–R8 chưa có học liệu
  để mở. Đây là thông tin khả dụng được giao kiểm tra, không thay lời dẫn đã duyệt.
- Giữ tài sản bảng dấu BBT01 và hình hộp ZO Geometry đã duyệt; không sửa hình.
- Nội dung và HTML desktop/mobile đã được chủ dự án duyệt; kiểm định cuối đạt ở
  1366/430/390 px. `production: accepted`, `publication: pending`.

Kiểm định: `zo_qmd.py check/render` qua launcher, `cong_cu/kiem_chung.py`
(baseline bất biến và nguồn được duyệt), `cong_cu/kiem_chung_html.py`
(toàn chuỗi văn bản/TeX, liên kết, disclosure, tài sản). Bản ghi bên dưới là
lịch sử trước quyết định này, không được dùng để ghi đè nguồn hiện hành.

### Hồ sơ kiểm định tích hợp

- Import: `python scripts/zo_python.py content/thpt/on_thi_toan_thpt/hoc_lieu/d0/cong_cu/tich_hop_html_da_duyet.py --approved-html D:/Downloads/khao_sat_dau_vao_D0.html`.
  Importer chỉ dùng khi nhận bản duyệt mới; công việc biên soạn tiếp dùng QMD.
- Check: `python scripts/zo_python.py scripts/zo_qmd.py check content/thpt/on_thi_toan_thpt/hoc_lieu/d0/index.qmd`.
  Render: `python scripts/zo_python.py scripts/zo_qmd.py render content/thpt/on_thi_toan_thpt/hoc_lieu/d0/index.qmd`.
  Lần render trong sandbox bị lỗi quyền cache Quarto; chạy lại cùng lệnh với
  quyền cần thiết đã đạt, không lỗi/cảnh báo render.
- Checker gói: `python scripts/zo_python.py content/thpt/on_thi_toan_thpt/hoc_lieu/d0/cong_cu/kiem_chung.py` và
  `python scripts/zo_python.py content/thpt/on_thi_toan_thpt/hoc_lieu/d0/cong_cu/kiem_chung_html.py`.
  PASS: toàn chuỗi văn bản và TeX bản duyệt, 24 câu, Bài 00, 25 đối chiếu,
  sáu bảng thường, bảng dấu, hai hình vector và đích liên kết thật;
  baseline 25 tệp và ngân hàng nguyên byte, checker toán lịch sử 48/48.
- Runtime: `node content/thpt/on_thi_toan_thpt/hoc_lieu/d0/cong_cu/kiem_chung_tuong_tac.mjs --url http://127.0.0.1:8765/content/thpt/on_thi_toan_thpt/hoc_lieu/d0/index.html --out _audit/d0_da_duyet_preview`.
  Chromium headless, hồ sơ tạm độc lập, desktop 1366 và mobile mô phỏng 430/390.
  Kiểm năm thẻ, 24 cặp liên kết ở từng viewport, mở/đóng Bài 00, URL trực tiếp,
  lịch sử Back, sticky, Navbar kéo lên, công thức và bảng cuộn cục bộ,
  tài sản tải thành công, khả năng đọc không JS. Không phải nghiệm thu của chủ dự án.
  Bản cuối đạt 224/224 kiểm tra; không tràn ngang trang ở cả ba viewport và không
  còn điều khiển cuộn dọc giả cạnh công thức nội dòng.
- Đã sửa lỗi Quarto chuẩn hóa anchor thành URL đầy đủ làm bộ xử lý tab cũ
  không bắt được liên kết; đã sửa tràn công thức R7-03 bằng vùng cuộn riêng,
  không đổi công thức hoặc giảm chữ. Bộ kiểm thử runtime và ảnh cuối nằm ở
  `_audit/d0_da_duyet_preview/`, giữ để nghiệm thu; hồ sơ browser tạm được dọn.
- Browser plugin không kết nối được do lỗi Windows sandbox; dùng Chromium
  kiểm thử riêng, không dùng phiên hay hồ sơ browser cá nhân.
- Preview tại URL trên, phục vụ `docs` chỉ ở `127.0.0.1`. Mobile dùng responsive
  viewport 390/430 px trên desktop; không mở server ra mạng LAN.
- Chưa có học liệu R2–R8, chưa có các gói R1 ngoài G01/G02; không tạo đích thay thế.
  D0 không yêu cầu PDF nội dung. Chưa prepare/publish/stage/commit/push.

Tệp tác động của lần tích hợp (đều dưới ranh giới D0): `index.qmd` tái sinh;
`cong_cu/tich_hop_html_da_duyet.py`, `kiem_chung_da_duyet.py`,
`kiem_chung_tuong_tac.mjs` mới; `cong_cu/tao_qmd_chuyen_doi.py`, `d0.lua`,
`kiem_chung.py`, `kiem_chung_html.py` cập nhật; `giao_dien/d0.css`,
`d0_script.html` cập nhật; `_quy_trinh/noi_dung_da_duyet.json` mới;
`_quy_trinh/README.md`, `hop_dong_nguon_canonical.md`,
`ma_tran_phep_chieu_noi_dung.md`, `manifest_chuyen_doi.yml`,
`cau_hinh_san_xuat_qmd.yml`, `ho_so/index.yml` cập nhật.
HTML và CSS đầu ra tương ứng dưới `docs/` được dựng lại; không sửa tay.
Không sửa shared component, R1-G01/R1-G02, file Downloads hoặc tài sản hình.

## Phạm vi

Thư mục `content/thpt/on_thi_toan_thpt/hoc_lieu/d0/` là ranh giới canonical của gói D0 trong hệ học liệu Ôn thi Toán THPT.

D0 là bộ khảo sát và định vị đầu vào. Gói không được mặc định có cùng cấu trúc nội dung, luồng học hoặc số biến thể PDF với R1-G01 và R1-G02. Việc chuyển đổi phải giữ vai trò riêng của D0, đồng thời tái sử dụng hệ thành phần, phong cách ZO Math, checker và pipeline canonical khi phù hợp.

## Trạng thái hiện tại

- Bộ D0 v1.0 đã được chuyển nguyên vẹn từ đầu mối điều hành khóa 2027 vào [`lich_su/v1_0/`](lich_su/v1_0/README.md).
- `lich_su/v1_0/` giữ nguyên 25 tệp, cấu trúc tương đối, manifest và byte của bộ đã được xác nhận hoàn tất.
- `index.qmd` là phép chiếu ngân hàng bất biến và hướng dẫn đã biên tập ở Bước 6B; toàn gói vẫn `in_production`.
- Cấu hình sản xuất, hồ sơ, checker chuyển đổi, bộ lọc riêng tư HTML và ma trận phép chiếu đã được thiết lập.
- HTML cũ đã được người dùng nghiệm thu và kết luận chưa đạt. Sau Bước 6B, nguồn đã đổi và HTML cũ là `stale`; chưa render lại và chưa có PDF canonical.
- Bốn PDF trong `lich_su/v1_0/` là thành phẩm lịch sử, không phải đầu ra canonical mới và không được sửa trực tiếp.
- `publication` vẫn là `pending`; chưa prepare hoặc publish.

## Nguồn và hàng rào bảo toàn

- Baseline nội dung chuyển đổi là toàn bộ D0 v1.0 trong `lich_su/v1_0/`.
- Chuỗi lịch sử được giữ nguyên: `src/bien_soan.py` sinh ngân hàng JSON; `src/dong_goi.py` sinh các bản Markdown; `src/xuat_pdf.py` sinh bốn PDF.
- Không sửa nội dung toán học, nhiệm vụ, mã câu, tiêu chí, lời giải hoặc trạng thái sư phạm trong khi chỉ thiết lập kiến trúc canonical.
- Không dùng riêng PDF hoặc Markdown sinh làm nguồn chỉnh sửa độc lập.
- Mọi phép chiếu mới phải có đối chiếu đầy đủ với baseline v1.0 và giữ checker toán hiện có như một lớp kiểm định.

## Việc tiếp theo

Bước 2 đã lập [`manifest_chuyen_doi.yml`](manifest_chuyen_doi.yml) và [`hop_dong_nguon_canonical.md`](hop_dong_nguon_canonical.md). Hai tệp phân loại nguồn, dữ liệu sinh, thành phẩm lịch sử, tài sản và bằng chứng kiểm định; đồng thời khóa đủ 24 nhiệm vụ chính, 24 câu thử lại, tám mạch và quan hệ cùng họ.

Bước 3 đã thiết lập cấu hình dự án, hồ sơ trạng thái, dữ liệu canonical, checker nền và khung `index.qmd`.

Bước 4 đã lập [`ma_tran_phep_chieu_noi_dung.md`](ma_tran_phep_chieu_noi_dung.md), đưa đủ 24 nhiệm vụ chính và 24 hồ sơ/câu thử lại vào ứng viên QMD, đồng thời khóa nội dung người hướng dẫn trong vùng bị xóa khỏi AST HTML công khai. Checker hiện yêu cầu toàn bộ QMD khớp toàn chuỗi với phép chiếu xác định từ baseline.

Bước 5 đã bổ sung `giao_dien/d0.css`, render HTML bằng `scripts/zo_qmd.py render` và kiểm tra đầu ra bằng `cong_cu/kiem_chung_html.py`. Đầu ra đủ inventory và không rò nội dung riêng, nhưng nghiệm thu sau đó đã phát hiện thiếu nội dung, lỗi kiến trúc và sai biệt trình bày.

Bước 5A đã sửa lỗi ánh xạ tên mạch do lớp chuyển đổi tạo. Tám tên mạch hiện được khóa theo mục 4.5 của Kế hoạch 0.6; checker đọc nguồn này độc lập, kiểm tra mã B của từng nhiệm vụ và có fixture âm bắt buộc từ chối `R5 — Số phức`. Xem [`bao_cao_sua_loi_5a.md`](bao_cao_sua_loi_5a.md).

Hash trong `html_candidate.files` chỉ giữ dấu vết ứng viên cũ chưa đạt, không là khóa phát hành hoặc bằng chứng freshness cho nguồn hiện tại.

Bước 6A đã kiểm toán nội dung và kiến trúc. Bước 6B đã tạo hai nguồn hướng dẫn
canonical trong `du_lieu/`, bỏ mã quản lý khỏi lời dẫn và nhãn nhiệm vụ công khai,
bổ sung nội dung `Đọc kết quả`/`Thử lại`, đồng thời cập nhật hướng dẫn phân tích
theo Kế hoạch 0.6. Ngân hàng vẫn nguyên byte; toàn bộ 15 sai biệt của hướng dẫn
phân tích được ghi trong `bien_tap_6b.json` và kiểm tra độc lập với phép sinh QMD.

Bước 6C đã sửa cây nội dung: R1–R8 thuộc thẻ Khảo sát; Khai báo có thẻ riêng;
Đọc kết quả có mẫu hồ sơ và bản đồ tuyến; Bổ sung giới hạn ở việc thu bằng chứng.
Thẻ Tải PDF giữ trạng thái chưa sẵn sàng. Bản dựng 6C chỉ kiểm tra kiến trúc,
chưa là ứng viên nghiệm thu cuối.

Bước 6D đã tích hợp bảng dấu R1-03 qua công cụ bảng biến thiên dùng chung,
JSON tại `du_lieu/bang_bien_thien.json`, SVG cho HTML và PDF vector cho bản in.
Các bảng thường dùng component `r1-data-table`, ngữ nghĩa hàng/cột và vùng cuộn
cục bộ. Phương án và các ý hỏi có khoảng cách riêng; metadata dùng chữ thường.
Ngân hàng toán giữ nguyên byte. Kiểm định nguồn/render/HTML đạt; nghiệm thu
trực quan toàn trang vẫn chờ người dùng. Tiếp theo là hình theo
định dạng đầu ra (6E), checker hồi quy (6F), render và nghiệm thu HTML (6G).
Chỉ sau nghiệm thu HTML mới tạo bốn PDF ở Bước 7. Chưa prepare hoặc publish.

Đợt 5 hình học đã khóa baseline ZO Geometry v0.1 và tích hợp một pilot tại
`D0-R3-03`. Nguồn pilot nằm trong `pilot_hinh_hoc/`; TeX, PDF, SVG, PNG và receipt
`hinh_hop` được khóa checksum trong manifest, còn bản lịch sử vẫn bất biến. Pilot đã
đạt kiểm tra nguồn, HTML và PDF tài sản; nghiệm thu trực quan trong trang thật và
hệ bốn PDF canonical của D0 vẫn `pending`.
