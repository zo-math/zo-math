# Điều hành chương trình — trạng thái và việc tiếp theo

Phiên bản: 0.1 · Cập nhật trạng thái: 16/10/2026.

Đây là nơi duy nhất ghi công việc đang mở và thứ tự sản xuất hiện hành. Chỉ cập nhật trạng thái từ bằng chứng trong hồ sơ gói. [Điểm vào](README.md).

**SYNC-RELEASE01 — bộ hiện hành và quyền xuất bản, 15/10/2026.**
Thay trạng thái đầu ra/chờ duyệt trong FIG-PDF01 và các mục lịch sử bên dưới.
Chủ trì đã trả lời “Duyệt thiết kế, dựng tiếp 14 biến thể”, sau đó yêu cầu
xuất bản Nhà, D0, R1-G01, R1-G02 lên zomath.vn thay các trang cũ.
Cả 16 PDF R1 hiện hành đạt 17/17 phép kiểm từng tệp; full G01 80 trang,
học sinh G01 60 trang; full G02 61 trang, học sinh G02 42 trang. D0 20 trang.
Số trang/mô tả thẻ tải, trạng thái PDF, provenance và hồ sơ gói đã đồng bộ.
Xem `hoc_lieu/r1_g01/_quy_trinh/ho_so/pdf_bundle_review.json` và hồ sơ tương ứng G02.
Mọi trang màu được bao phủ bằng xem trực quan hoặc đối chiếu pixel thân trang
đã xem; kiểm xám đại diện từng biến thể và các trang hình/bảng/cuối của bản đầy đủ.
Đã sửa ngắt trang tiêu đề, bảng trong khối lời giải và chữ tràn ngoài trang;
cổng hồi quy có fixture âm cho lỗi tiêu đề/chữ bị cắt. Không dựng lại sách
khi chỉ đồng bộ số trang thẻ tải; thay nội dung/hình thật vẫn làm STALE.
Kiểm nguồn ba gói đạt; kiểm điều hành 175/175; cổng xuất bản 38 kiểm thử đạt.
Đã bổ sung nhận diện provenance của một commit revert thông thường chỉ khi
cây công khai khôi phục đúng byte cây cha của lần xuất bản bị revert; trường
hợp khác vẫn bị từ chối. Không viết lại lịch sử Git hoặc bỏ qua kiểm nguồn.
Đường prepare website đã khóa render HTML tường minh, không tự dựng nhánh PDF của D0; dùng các PDF canonical đã kiểm. Cache phiên RStudio/Jupyter không được sao chép làm phụ thuộc render.
HTML tươi của prepare được render vào .quarto bằng đường dẫn tương đối rồi chuyển sang staging báo cáo, để adapter không đọc vùng audit lịch sử; kiểm tích hợp trang Nhà đã đạt.
Tên thư mục render tạm đã rút ngắn để các trang lịch sử tên dài nằm trong giới hạn Windows; fixture sao chép đúng trang dài nhất đã đạt.
Đã sửa đóng gói theo chuỗi tham chiếu HTML/CSS tới CSS, JS, ảnh, PDF và font; giới hạn HTML bằng --page đúng bốn trang. Kiểm tích hợp trên render tươi: 0 lỗi, đúng bốn HTML đổi, 101 tài nguyên phụ thuộc; HTML ngoài phạm vi giữ nguyên.
Trạng thái: **đã xuất bản và kiểm trực tiếp trên zomath.vn**. Nguồn `bb480547eea5b5dc4a191255db8904b2d012a3d6`, public `3f99deac4b95e2b2e05e4f6e40ffd14e49be157a`. Hồ sơ máy đọc: [ho_so_phat_hanh_20261015.json](ho_so_phat_hanh_20261015.json). Bốn HTML và 17 PDF trên mạng khớp SHA-256 của cây xuất bản; kiểm trình duyệt trực tiếp 13/13, gồm thanh mục lục khi cuộn ở chế độ xám và trang Nhà trên màn hình nhỏ.
Giới hạn kiểm: chưa in giấy/quét QR bằng điện thoại/phản biện toán độc lập.

## A. Công việc đang mở
**HOME-YT01 — nguồn YouTube và chuẩn bị riêng trang Nhà, 16/10/2026.**

- Nguồn `index.qmd`, CSS Home và ảnh chờ dùng video `SJ1bb9gWxDA`;
  đã bỏ MP4 khỏi HTML/chính sách public. Home 109/109 và runtime 7/7 đạt.
- YouTube xác nhận lịch 20:30 ngày 16/10/2026 UTC+07:00; giao diện chờ giờ
  hẹn và tải iframe khi người xem bấm. Chưa kiểm phát công khai sau giờ hẹn.
- Dùng `prepare --committed-source --page` để dựng đúng HEAD đã commit,
  loại thay đổi làm việc khác khỏi nguồn dựng, giữ nguyên PDF/trang ngoài phạm vi.
- Kết quả prepare hiện hành lấy từ `_audit/zo_publish_prepare_report.json`
  do công cụ tạo; chốt nguồn này không tự chứng nhận prepare hoặc xuất bản.
  Chưa push/phát hành; cần duyệt diff chuẩn bị rồi mới thực hiện theo quyền.
- Hồ sơ: `home_youtube_ban01_20261016.json`; biên nhận lịch YouTube ở
  `zo_math_media/xuat_ban/bien_nhan/ZO-V000001`.

**DRAFT-TEMPLATE01 — mẫu biên soạn và bảng kiểm, 16/10/2026.**

- Chủ trì đã chốt vị trí, vai trò và cơ chế gọi rồi giao hoàn thành. Đã tạo [mẫu bản thảo 1.0](mau/ban_thao_goi.md) và [bảng kiểm 1.0](mau/bang_kiem_ban_thao_goi.md) trong thư mục mau hiện có; không tạo thư mục hoặc gói tương lai.
- AGENTS chuyên mục tự kích hoạt mẫu từ yêu cầu viết/rà/sửa bản thảo R1. 02/1.4 sở hữu việc dùng: đối chiếu trước viết, kiểm bằng chứng trước trình, báo khác biệt có lí do, ghi phiên bản/hash và cập nhật mẫu cùng lượt khi có cải tiến đã chốt. Đồng bộ mẫu hồ sơ, quy chuẩn gói, README, hướng dẫn, danh mục thẩm quyền, QD_036 và danh sách phụ thuộc. Không tạo bộ kiến trúc hoặc mẫu trang thứ hai.
- Đã áp dụng hồi cứu cho [G03 0.8](../../../hoc_lieu/r1_g03/_quy_trinh/ho_so/bang_kiem_ban_thao_20261016.md), không sửa nội dung hoặc hình; hai tiêu chí về hình/bản xuất giữ hoãn theo phản hồi của chủ trì. Bảng áp dụng không nhận là đã dùng mẫu trước khi viết hoặc nghiệm thu G03.
- Kiểm tài liệu và tự kiểm cổng điều hành đạt 235/235; kiểm 35 liên kết mới, đọc Markdown của hai mẫu và bảng áp dụng đạt; nguồn và tài nguyên G03 giữ nguyên, các thay đổi ngoài phạm vi được bảo toàn. Bằng chứng kỹ thuật: `_audit/r1_g03_manuscript_20261016/template_setup_checks.json`.
- Cơ chế gọi là chỉ dẫn bắt buộc của agent, không phải chương trình tự sinh hay kiểm tự động chất lượng lời giảng. Bộ mẫu đã hoàn thành; trạng thái/bước tiếp của G03 ở mục dưới. Chưa commit hoặc phát hành lượt này.

**G03-LABEL01 — khép thiếu hệ nhãn và chống bỏ sót khi dựng, 16/10/2026.**

- Bìa riêng đã thay theo phản hồi chủ trì: nền ảnh/nhãn trong suốt, hai tiệm cận có nhãn, công thức đặt cách đầu nhánh. Chủ trì xác nhận “OK” rồi giao commit các giai đoạn đủ điều kiện. HTML hiện tại đã qua 847/847 kiểm, hệ nhãn 20/20; không suy thành duyệt toàn gói hoặc quyền phát hành. Không dựng PDF học liệu.


- Chủ trì phát hiện G03 thiếu nhãn hiển thị. QD_025, 07/6.2 và danh mục đã có quy tắc; lượt chuyển đổi ban đầu mới gắn metadata và bộ kiểm không kiểm đầy đủ nhãn thật. Kết quả kiểm của G03-SOURCE01 không chứng nhận phần nhãn này.
- Đã đối chiếu binding cùng HTML toàn văn G01/G02; dùng lại nguyên tắc chức năng/ngữ cảnh, một dãy số toàn nhóm, loại nội dung riêng, đề–lời giải cùng ánh xạ và bỏ nhãn lặp tiêu đề. Không tạo một chuẩn nhãn khác hoặc sửa hồi tố hai gói đối chứng.
- Danh mục chung sở hữu mẫu hiển thị; `zo_course_labels.py` áp dụng/kiểm từ binding gói, không cố định số bài. G03 dùng binding đầy đủ và nguồn QMD; các cổng QMD/Quarto/HTML chặn thiếu nhãn. AGENTS, 02 và quy chuẩn QMD tự kích hoạt bước này cho gói tiếp theo.
- Bằng chứng và ứng viên HTML mới: [biên nhận áp dụng nhãn](../../../hoc_lieu/r1_g03/_quy_trinh/ho_so/ap_dung_nhan_20261016.json). Bản thảo, công thức và hình giữ nguyên; chỉ hiệu chỉnh metadata/nhãn và cách đánh số các câu xác nhận nền.
- Trạng thái: ứng viên HTML có hệ nhãn chờ chủ trì xem; bước tiếp theo là duyệt hiển thị mới. Chưa dựng PDF học liệu, commit/push hoặc phát hành. Các phần kiểm ngoài nhãn của G03-SOURCE01 chỉ kế thừa theo đầu vào/phạm vi không đổi.

**G03-SOURCE01 — chuyển QMD và dựng ứng viên HTML, 16/10/2026.**

Thay trạng thái/bước tiếp về G03 ở G03-DRAFT01 và DRAFT-TEMPLATE01; các kết quả bản thảo bên dưới giữ làm căn cứ theo phiên bản.

- Chủ trì đã chốt trình tự nguồn QMD → dựng tài nguyên → tích hợp/kiểm HTML và giao “OK. Tiến hành.” Quyền này áp dụng bước chuyển đổi; không ghi thành nghiệm thu HTML, PDF hoặc phát hành.
- Nguồn hiện tại: [index.qmd](../../../hoc_lieu/r1_g03/index.qmd). Markdown 0.8 và tài nguyên bản thảo giữ nguyên, không sửa song song. Đã tạo cấu hình/hồ sơ QMD, manifest kiến trúc và binding nhiệm vụ/ví dụ; đăng ký ba đơn vị nền có thật của G03 vào danh mục chung.
- Đã dựng mới 11 cặp SVG/PDF hình từ TeX qua ZO Math graph 0.4, không lấy đầu ra nháp làm tài sản chính thức. Khung hình cắt tiệm cận được mở xuống dưới trục hoành; xem toàn bộ danh mục hình xác nhận các hệ trục giao nhau. Không thay dữ kiện toán. PDF ở đây là từng hình vector, không phải PDF học liệu.
- HTML dùng bộ khung chung G01/G02, có điều hướng, mục lục Bài học, vùng đọc, bảng phân loại và vùng bảo trợ/chân trang. Giữ cờ draft và danh mục công khai hiện hành. 42 cặp đề–lời giải giữ nguyên; lời giải Kiểm tra chỉ mở từ điểm dừng sau lượt.
- Bản xem và bằng chứng kiểm hiện hành: [hồ sơ chuyển đổi](../../../hoc_lieu/r1_g03/_quy_trinh/ho_so/chuyen_qmd_20261016.json). Đây là ứng viên kỹ thuật chờ chủ trì duyệt HTML; chưa có PDF học liệu G03, chưa commit/push/phát hành.
- Bước tiếp theo: chủ trì đọc ứng viên HTML, đặc biệt hình, Gợi mở và các tuyến hỗ trợ; hiệu chỉnh trong QMD theo góp ý. Sau khi HTML được duyệt, mới giao dựng và kiểm toàn văn PDF.

**G03-DRAFT01 — căn cứ bản thảo trước chuyển đổi, 16/10/2026 (trạng thái mới ở G03-SOURCE01).**

- Chủ trì giao sửa năm điểm được phát hiện khi rà bản 0.7 theo toàn văn Đơn điệu và cực trị. Đã áp dụng vào [bản nội dung 0.8](../../../hoc_lieu/r1_g03/_quy_trinh/ban_thao/noi_dung.md); duyệt phương án sửa chưa được ghi thành nghiệm thu nội dung mới.
- Bản thảo vẫn có tám ví dụ, 52 nhiệm vụ/câu ở cấp kiểm kê, ba phần nền, 11 hình và 42 cặp đề–lời giải tách vị trí. Gợi mở 01–06 nằm tại đầu sáu mục; Sửa lỗi 01–12 liên tục. Các bổ sung lần này nằm trong các ý của nhiệm vụ hiện có.
- R03-01: Nhiệm vụ 01 Sửa lỗi có ý b mới với giá trị riêng tại mốc và giới hạn trái vô cực, lời giải/tiêu chí tương ứng; Tự kiểm tra 06 dẫn thẳng đúng ý còn mới, không coi câu rút gọn là xác nhận thay thế. Nhật kí giả lập giữ trạng thái chưa xác nhận và chỉ rõ việc tự làm tiếp.
- R03-02: Nhiệm vụ 05 Sửa lỗi có nhánh phải tiến gần đường xiên đi xuống; dữ kiện, nguồn TeX, SVG/PDF, đề, lời giải và tiêu chí đã đồng bộ. Hình dựng lại qua công cụ ZO Math profile 0.4, kiểm vector và xem trực quan đạt; chỉ thuộc tài nguyên bản thảo.
- R03-03/04/05: các câu Sửa lỗi nhiều ý dẫn đúng phần học/nền theo ý; điểm Kiểm tra 02(b) tách ba thành phần rõ ràng, giữ tổng 20 điểm; đủ 21 đích số–tên trong bảng chọn bài. Quy tắc giữ bài ban đầu, dùng câu còn mới và quay về nơi gọi giữ nguyên.
- Kiểm bản 0.8: 19 đối chiếu toán/điểm chịu ảnh hưởng đạt; 1115 cụm toán chuyển MathML không cảnh báo, 145 ID không trùng, 365 liên kết không hỏng; 42 cặp đề–lời giải khớp tên và đường quay lại, kiểm số nhóm và hướng giới hạn đạt. [Biên nhận hiệu chỉnh và khép năm phát hiện](../../../hoc_lieu/r1_g03/_quy_trinh/ho_so/hieu_chinh_sau_ra_soat_20261016.json). Chưa thay phản biện độc lập, thử với học sinh hoặc kiểm giao diện sản xuất.
- [Hồ sơ phạm vi](goi/R1_G03.md) lên 0.11; [đề cương](goi/R1_G03_de_cuong_bien_soan.md) và [ma trận](goi/R1_G03_ma_tran_nhiem_vu.md) lên 0.8. [Biên nhận rà 0.7](../../../hoc_lieu/r1_g03/_quy_trinh/ho_so/ra_soat_toan_bo_theo_g01_20261016.json) cùng các biên nhận trước giữ nguyên theo phiên bản; năm phát hiện đã được tiếp quản bởi lượt này. Không sửa hồi tố G01/G02 hoặc kiến trúc chung.
- Tệp `ban_thao/noi_dung.pdf` đang có vẫn là nội dung 0.3 (51 trang), không phản ánh Markdown 0.8. Điểm vào đọc duyệt là Markdown ở trên. Chưa có QMD/HTML/PDF học liệu chính thức hoặc tài nguyên sản xuất G03.
- Áp dụng bảng kiểm mẫu 1.0 cho bản 0.8: kết quả và ngoại lệ ở [hồ sơ áp dụng](../../../hoc_lieu/r1_g03/_quy_trinh/ho_so/bang_kiem_ban_thao_20261016.md). Chủ trì nêu hai hình lạ, trong đó có hình hai trục không cắt nhau, và chọn xử lí khi dựng QMD/tài nguyên; chưa định danh đủ hai tệp, phải rà toàn bộ danh mục hình ở bước đó. Không tự coi công cụ hoặc visual PASS cũ đã giải quyết phản hồi mới. B19/B21 giữ hoãn, phải khép bằng xem hình thực trước trình HTML có các hình ấy.
- Trạng thái: bản 0.8 đã hiệu chỉnh năm điểm nội dung, chờ chủ trì duyệt nội dung; hai hình giữ vấn đề mở được cho hoãn, chưa có QMD/HTML hiện hành. Bộ mẫu đã được áp dụng hồi cứu, không sửa bản thảo hoặc ảnh lần nữa trong lượt lập mẫu. Bước tiếp theo: chủ trì chốt nội dung trước khi giao chuyển QMD và dựng/kiểm tài nguyên để khép vấn đề hình. Chưa nghiệm thu, commit hoặc phát hành. Các công việc khác giữ nguyên phạm vi.

**DOC-SYNC01 — dọn chỉ dẫn học tập lỗi thời, 16/10/2026.**

- Chủ trì giao xóa tài liệu cũ có thể bỏ và cập nhật tài liệu cần giữ; bốn bản toàn văn/PDF cũ trong Nguồn đã được chủ trì xóa.
- Đã gỡ ma trận chuyển đổi G02 tháng 9 sau sao lưu có SHA-256; cập nhật tám tài liệu tiếp quản/điều hành để dẫn đúng 01/QD_033 và 07. Chỉ mục và lý do giữ hồ sơ lịch sử ở 06.
- G01 v1.1, Design khóa, Kế hoạch 0.6, bản thảo/nhật kí/receipt lịch sử giữ nguyên; không sửa QMD, HTML/PDF, công cụ, nội dung toán hoặc kiến trúc.
- Khuyến nghị quản lý Nguồn ở 05: đọc workspace khi có thể, chỉ đóng gói snapshot theo nhiệm vụ khi không đọc được PC; không tự tải lại mọi gói sau mỗi lần sửa.
- Hồ sơ kiểm: `_audit/learning-document-cleanup-20261016/verification.json`. Lượt dọn tài liệu này đã khép; không mở thêm quyền biên soạn, commit hoặc phát hành. Công việc công cụ đã ghi dưới đây giữ nguyên phạm vi.

**CLOSE-RELEASE01 — khép hồ sơ xuất bản ngày 15/10/2026.**

- Phạm vi: bốn trang Nhà/D0/R1-G01/R1-G02 và 17 PDF thuộc bản phát hành
  SYNC-RELEASE01. Chủ trì giao dọn dẹp, khép hồ sơ; việc tìm ảnh đã được
  chủ trì khép sau khi tự tải lại và thay ảnh vuông vào đúng thư mục.
- Trạng thái sản phẩm: đã xuất bản; hai gói R1 vẫn là bản xem trước đang
  phát triển, không nâng thành hoàn tất toàn khóa. Không có việc tìm ảnh
  hoặc việc xuất bản tiếp đang mở trong phạm vi nhiệm vụ này.
- Một nguồn trạng thái: mục A này. README chuyên mục/khóa/kit dẫn về đây;
  các mốc DH/FB/SYNC bên dưới là lịch sử. Quy tắc QD_033 và các chủ đề
  khác giữ nguyên; khép việc không thay kiến trúc, nội dung hoặc thiết kế.
- Receipt phát hành gốc giữ nguyên tại
  [ho_so_phat_hanh_20261015.json](ho_so_phat_hanh_20261015.json).
  Kết quả dọn, tài sản và xác minh sau phát hành nằm tại
  [khep_ho_so_phat_hanh_20261015.json](khep_ho_so_phat_hanh_20261015.json).
- Bộ ảnh bìa có đủ năm tỉ lệ; bản vuông hiện tại do chủ trì cung cấp.
  Manifest `../giao_dien/bo_anh_bia.json` giữ dấu kiểm bộ đang dùng;
  receipt nhập cũ không bị sửa. Guard thư viện đọc manifest hiện hành,
  không đòi khôi phục lại ảnh vuông cũ. QMD chỉ hiển thị bản 3:4 như trước.
- Dọn phần chuẩn bị đã hết vai trò ra kho ngoài repo, xác minh SHA-256
  trước gỡ nguồn; giữ bằng chứng bản đã xuất bản và toàn bộ tài sản/bộ
  xem được bảo vệ. Không chạy kết sổ toàn repo hoặc dọn công việc khác.
- Giới hạn kiểm tại mốc phát hành vẫn giữ: chưa in giấy, quét QR bằng
  điện thoại hoặc phản biện toán độc lập. Đây không phải việc còn treo
  của lượt khép hồ sơ và không bị ghi thành đã kiểm.

## B. Lịch sử trước khép hồ sơ

**FIG-PDF01 — sửa phân kì nguồn hình và tầm soát đầu ra, 15/10/2026.**
Trạng thái lịch sử tại FIG-PDF01; đã được SYNC-RELEASE01 ở trên thay thế.
Nguyên nhân đã xác minh: QMD G01/G02 chọn hình cũ; HTML thay hình riêng sau
render, PDF chỉ đổi đuôi SVG thành PDF nên vẫn lấy hình cũ. Nay QMD chọn
`giao_dien/assets/figures_0_4/`; HTML/PDF dùng cặp vector từ cùng nguồn toán,
profile 0.4 và nhãn. 88 tài sản cũ không dùng đã lưu có checksum ngoài repository
tại `E:/zo_nhap/zo_math_archive/course-release-repair-20261014`, rồi gỡ khỏi
nguồn biên dịch. TeX toán, SVG mới đã duyệt và 14 PDF còn chờ giữ đúng byte.

Sửa đồng thời kiểm kê AST G02, ranh giới/thứ tự 16 phép chiếu PDF, liên kết
phần bị lược, caption trong khối Ôn nền, bảng Nhật kí và ngắt khối ngắn.
Kiểm TeX nhanh đủ 16 cấu hình trước biên dịch; chặn hình cũ, thiếu cặp hoặc
lệch fingerprint. Số trang thẻ tải được loại riêng khỏi fingerprint PDF để
không gây dựng sách lại vì thay đúng số trang; tên/nội dung/hình vẫn làm STALE.

Đầu ra hiện hành: full G01 79 trang, full G02 58 trang, D0 20 trang.
G01/G02 đạt 13/13 và đã xem mọi trang màu/xám; D0 đạt checker riêng và xem
mọi trang màu/xám. Hồ sơ ở `ho_so/pdf_full_review.json` từng gói và báo cáo
`_audit/course-release-repair/`. 14 biến thể khác chưa dựng lại, đang chờ
chủ trì duyệt full: bộ xét duyệt tự động từ chối thay cả bộ trước bước này.
HTML mới ghi chính xác từng PDF đã cập nhật hoặc đang chờ; nguồn và docs
đồng bộ từ Quarto mới. Bộ xem hiện hành ở `_audit/course-release-current/`.
Kiểm bộ xem cuối 282/282, điều hướng 61/61, hồi quy rail xám 119/119;
cổng tài liệu 233/233, kiểm nhãn nguồn và tự kiểm zo_pdf đạt. Cổng xuất bản
có 30 kiểm thử đạt, từ chối 14 PDF STALE và cây Git chưa kết sổ; không còn
lỗi nguồn hình, thiếu tài nguyên, đường dẫn riêng hoặc khoảng trắng HTML.
Các PDF full G01/G02 ngày 15/10 giữ đúng ảnh mọi trang trong; chỉ đổi ngày
tạo trên trang đầu/cuối so với bản đã xem, hai trang ấy đã xem lại.
Báo cáo cuối: `_audit/course-release-repair/repair_report.json`.
Chưa xuất bản, chưa nghiệm thu của chủ trì, chưa rà toán độc lập/in giấy/quét QR.

**GRAY-NAV01 — sửa điều hướng mất khi cuộn trong sắc xám, 14/10/2026.**
Sửa bộ lọc dùng chung từ body sang html để thanh cố định giữ vị trí theo
viewport; không đổi nội dung học liệu. Guard trình duyệt trong
`scripts/zo_web_2027_grayscale_check.py` được gắn vào đường dựng bộ bốn
HTML; kiểm cuộn trên sáu nền và fixture âm lỗi cũ. Bộ xem của lượt sửa
nằm tại `_audit/zo-course-grayscale-reviewed/html-current/`, báo cáo tại
`grayscale-qa.json` trong cùng bộ. Binding tải bản đầy đủ G01 đồng bộ
79 trang theo QMD/PDF vừa dựng; phép đối chiếu xác nhận chỉ số ấy đổi,
không cập nhật fingerprint để bỏ qua thay đổi nội dung khác. Bộ cũ giữ
để đối chiếu; không xuất bản website hoặc dựng lại PDF trong lượt này.

**Lịch sử R1-G01 PDF đầy đủ — 14/10/2026, đã được thay bằng FIG-PDF01.**
Đã dựng `hoc_lieu/r1_g01/index.pdf` từ QMD hiện hành: 79 trang.
Thiết kế trang đầu, trang cuối, header/footer theo mẫu D0 đã được chủ trì
duyệt; khung dùng chung nằm ở `assets/tex/zo-course-pdf-shell.tex` và
`assets/tex/zo-course-pdf-end.tex`, quy tắc ZO031 đã được cập nhật.
PDF đầy đủ có 20 bảng nội dung và 14 bảng biến thiên từ nguồn hiện hành;
liên kết nội bộ có số trang in. Nội dung toán QMD được giữ nguyên, chỉ
đồng bộ số trang bản đầy đủ từ 57 thành 79. Hồ sơ có thẩm quyền cho lượt
này: `hoc_lieu/r1_g01/_quy_trinh/ho_so/pdf_full_review.json` và
`pdf_provenance.json`: kiểm kĩ thuật 13/13, xem đủ 79 trang màu/sắc xám.
PDF D0, bảy PDF G01 còn lại và bộ bốn HTML bàn giao giữ nguyên.
Ảnh kiểm trung gian đã dọn, giữ ảnh bằng chứng đại diện. Chưa in giấy,
quét QR bằng điện thoại hoặc rà toán độc lập. Bước tiếp theo là chủ trì
xem bản đầy đủ này; chỉ tiếp tục bảy biến thể sau khi bản đầy đủ được duyệt.
Chưa xuất bản website.

**Lượt chính tả và bảo trợ — 14/10/2026.**
Theo yêu cầu trực tiếp của chủ trì: bốn QMD hiện hành dùng chính tả i
(định lí, kĩ, xử lí, nhật kí, đăng kí); Nhà đổi ủng hộ thành bảo trợ.
Component Bảo trợ và nhãn rail dùng chung đổi cùng nguồn; giữ ID/URL cũ.
Bộ HTML bàn giao của lượt này được dựng mới từ cả bốn nguồn tại
`_audit/zo-course-editorial-current/html-current/home-reading.html`,
cùng D0/G01/G02 trong thư mục ấy. Đây là bộ xem mới thay điểm vào DH_045
cho lượt chỉnh chữ; DH_045 và QD_035 được giữ để đối chiếu, không ghép
HTML cũ vào bản mới. Manifest và báo cáo trong cùng bộ ghi kết quả dựng
và kiểm; không tự kế thừa nghiệm thu thị giác. Chỉ dựng HTML trong lượt
này; các PDF chưa nhận những thay đổi chữ/component của lượt này.
Không commit/push/prepare/publish.

**D0 PDF — bản đầy đủ sau khi chủ trì duyệt mẫu DH_044, 14/10/2026.**
Mẫu 9 trang được duyệt làm hướng dàn; `d0/index.pdf` đã dựng lại từ QMD bằng
hồ sơ in độc lập, đủ Bài 00, 24 đề và 25 đối chiếu trên 20 trang. Ủng hộ
lấy từ component HTML hiện hành, footer `zomath.vn` có link từng trang.
Checker nguồn/PDF/bảng, font, link và metadata đạt; đã xem mọi trang màu
và sắc xám. PDF đã được khai là tài nguyên website; lần dựng HTML cô lập
chép đúng byte vào đầu ra. Đầu ra sẵn để chủ trì kiểm toàn bản trước quyết
định xuất bản.
Chưa in giấy/quét QR vật lý; chưa `prepare`/`publish`, commit hoặc push.
Quy tắc và biên nhận ở D0 `06_pdf_bo_cuc_doc_lap.md`, `pdf_build.json`,
`pdf_review.json`. Script/fixture/biên nhận thử và ảnh audit PDF dư đã dọn;
PDF mẫu đã duyệt còn mở để đối chiếu. Các đoạn DH_042/DH_044 bên dưới giữ
đúng lịch sử mốc cũ.


### Công việc tại các mốc trước khép hồ sơ

**15/10/2026 — sửa việc dọn nhầm bộ ảnh bìa (HOME-ASSET01).**

**Đã khép theo xác nhận chủ trì:** sau lượt khôi phục, chủ trì báo ảnh
vuông chưa đúng rồi tự tải lại, thay vào đúng thư mục và yêu cầu khép
nhiệm vụ tìm ảnh. Bản 1:1 mới được ghi ở manifest tài sản hiện hành;
biên bản nhập ảnh cũ giữ nguyên để truy nguyên. Không còn chờ tìm ảnh.

- Chủ trì phát hiện bộ nhiều kích cỡ chỉ còn một ảnh trong nguồn. Nguyên
  nhân: DH_045 đã suy từ yêu cầu hiển thị một ảnh 3:4 sang loại bỏ bốn
  định dạng 1:1, 4:3, 9:16, 16:9 khỏi thư viện. Hai phạm vi này khác nhau.
- Khôi phục bốn PNG từ Git `fb425ca1` vào `assets/illustrations/`; đủ năm
  tệp khớp SHA-256, byte và kích thước của biên bản nhập, đồng thời khớp
  các bản gốc còn tại `D:/Downloads/`. QMD vẫn hiển thị bản 3:4.
- Thư viện có README liệt kê toàn bộ kích cỡ; danh mục bảo toàn phân biệt
  tài sản truyền thông với ảnh hiển thị. Guard `zo_home_cover_check.py`
  kiểm đủ năm bản và nguyên byte để bắt lại lỗi mất định dạng.
- Kiểm thư viện đạt; bảy ca âm đều bị bắt: thiếu từng ảnh trong năm
  định dạng, ảnh bị đổi byte, minh họa dịch vụ cũ xuất hiện lại. Fixture
  trong `.quarto/` đã tự dọn; không tạo thêm bản xem hoặc báo cáo tạm.
- Minh họa dịch vụ cũ `hoc_truc_tiep_trao_doi.svg` không còn được nguồn
  thực thi tham chiếu và không nằm trong manifest bảo vệ DH_032: chuyển
  ra `E:/zo_nhap/zo_math_archive/home-cover-assets-20261015/`, xác minh
  SHA-256 trước gỡ nguồn. Giữ PNG/SVG `hoc_truc_tiep_buoi_hoc` đang dùng.
- Mốc DH_045 bên dưới giữ nguyên để truy nguyên; phần cho phép gỡ bốn
  ảnh đã bị thay bởi đính chính này. Không sửa receipt phát hành cũ.
  Lượt này khôi phục tài sản và dọn minh họa cũ; không dựng HTML/PDF,
  không thay nội dung website đang phục vụ, chưa commit hoặc xuất bản.

**DH_045 — khép bộ xem bốn trang và một ảnh bìa, 14/10/2026.**

- Xác minh lỗi bàn giao: Nhà dịch vụ mới đã ghép ba HTML từ
  `_audit/home-preview`, bỏ qua nguồn/hover mới; không phải lỗi nội dung
  toán cần hoàn nguyên. Chủ trì yêu cầu sửa nguồn và dọn bản ghép thừa.
- Dựng mới Nhà/D0/G01/G02 cùng snapshot bằng `zo_web_2027_bundle.py`.
  Điểm xem duy nhất của lượt này:
  `_audit/zo-course-consistent/html-current/home-reading.html`.
  Các thẻ, menu, chuyển gói và quay về Nhà nằm trong cùng bộ. Manifest
  khóa QMD, mã/CSS/profile, tài nguyên và HTML; nguồn/asset lệch phải dựng lại.
- Giữ đúng một ảnh bìa 3x4 desktop trên mọi chiều rộng: sửa QMD, profile,
  CSS, normalizer và guard; gỡ bốn biến thể không dùng khỏi nguồn theo
  yêu cầu chủ trì. Bản được bảo vệ QD_035 và phụ thuộc giữ nguyên.
- CLI QMD bổ sung `render --html-only` để kiểm nguồn/geometry/HTML mà không
  kích hoạt nhánh PDF D0; không có cờ giữ hành vi cũ. Adapter chạy trong
  nguồn cô lập với boundary hoạt động, không đọc HTML lịch sử làm đầu vào.
- Kiểm đồng bộ sau dọn 273/273, điều hướng static 61/61; không thiếu link.
  Ca âm/câu chữ nguồn/bìa 6/6, hồi quy HTML-only 8/8. Hai guard Home đòi
  câu cũ đã thay bằng kiểm hỗ trợ trong đúng vùng và danh mục canonical,
  không sửa lời văn chủ trì. Lời/toán QMD ba học liệu giữ nguyên.
- Mẫu/vùng dịch vụ đã được chủ trì duyệt thị giác ở lượt trước; bộ xem
  đồng bộ mới chưa tự kế thừa nghiệm thu toàn bộ. Chưa kiểm browser trực
  quan ở lượt này; có một ảnh nguồn, không còn nhánh đổi ảnh mobile.
  Cảnh báo link gốc ngoài cây cô lập vẫn ở log, không thuộc các đích khóa.
- Dọn các mirror/bản ghép lỗi và mẫu thử của nhiệm vụ, giữ bộ cuối, runtime,
  giấy phép font và báo cáo; không xóa bản QD_035 hoặc dọn toàn repository.
  Không ghi root docs/PDF, không stage/commit/push/xuất bản.

**Bước tiếp: chủ trì mở bộ xem DH_045 và xác nhận đích học liệu/bìa.**
Các đường xem Home dịch vụ/DH_043 bên dưới chỉ là lịch sử trước DH_045.

**Lịch sử: Học trực tiếp trên Nhà — triển khai mẫu chủ trì chốt, 14/10/2026.**

- Chỉ thay `#hoc-truc-tiep` trong QMD native và CSS Home. Chữ thật ở trái,
  minh họa ở phải, thông báo chưa mở đăng ký ở dưới; bỏ nhãn phía trên,
  giữ thông tin thu phí. Dấu nhấn sau phần chữ dùng đỏ/vàng 6:4.
- PNG minh họa và SVG tự chứa thuộc tài nguyên khóa; SVG ghép đúng logo
  vector 0.4 vào tranh treo tường. Không có phụ thuộc build vào `_audit/`.
- Dựng cô lập từ nguồn qua `zo_web_2027_home_check.py rebuild`; bản xem:
  `_audit/home-service-final-review/home-reading.html`, giữ ba trang học
  liệu đối chiếu và runtime. Riêng vùng mới 21/21; checker toàn Nhà 107/109,
  không thiếu link. Hai guard còn đòi câu cũ ở hỗ trợ/danh mục (`flexible
  help and return to own work`, `eight strands not fake available packages`),
  không sửa lời văn ngoài phạm vi để đạt guard. Log còn cảnh báo link đến
  các trang gốc không có trong cây dựng cô lập, không thuộc vùng dịch vụ.
- Chưa kiểm trực quan browser/responsive: công cụ trình duyệt chặn URL file.
  CSS đã có nhánh mobile nhưng không nhận kiểm nguồn là nghiệm thu thị giác.
  Mẫu ảnh đã được chốt; HTML dựng mới chờ chủ trì xem. Chưa commit/push,
  PDF hoặc xuất bản; không thay bộ bản được bảo vệ QD_035.


**DH_044 — Quy cách bố cục PDF độc lập và mẫu thử, 14/10/2026.**

Trang cuối tiếp tục bị chủ trì phản hồi không đúng yêu cầu. Đã sửa phạm
vi hai cột thành riêng mục Học tiếp (lời dẫn trái, QR/link phải), khung
Ủng hộ nằm dưới và rộng toàn vùng đọc. Ghi đè cùng PDF; xem trang cuối
và kiểm vị trí hai vùng/link đạt; chờ chủ trì xác nhận cách hiểu này.

**Phản hồi mới nhất:** chủ trì đánh giá mẫu vừa sửa 4/10, không đạt.
Đã ghi đè mẫu thay thế 9 trang: nhãn hình chính bằng thân bài 11 pt
(tính từ font nguồn và kiểm scale trong PDF); tám nhãn Bài … • R…;
bỏ kẻ ngang giữa bài và nền nhận xét; trang cuối hai cột, Ủng hộ có
khung mặt trắng/viền gray-3 0.4. Nội dung/QR/tài khoản vẫn lấy HTML.
Đã xem các trang thay đổi, kiểm bảng/font/link/footer, đủ bốn đối chiếu
trên hai trang và guard cỡ nhãn/hai cột đạt. Chờ chủ trì xem mẫu thay thế.

Lần thử trước phản hồi 4/10: chủ trì cho phép ghi đè
đúng PDF mẫu. Mẫu mới 9 trang, đề một cột; bốn đối chiếu trọn trên hai
trang vật lý 6–7, có kết quả/lời giải/lưu ý/ôn lại và link về đề ở đầu.
Hướng dẫn chung trùng nhau được gộp một lần. Đã xem cả 9 trang màu;
checker đạt font/đích/footer/HTML Ủng hộ/lưới bảng và guard ghi nhận
không có lưu ý bị rơi sang trang riêng. Bản 10 trang mô tả dưới đây là
lần thử trước, đã được ghi đè. Chờ chủ trì xem bố cục mới; chưa phát hành.

Kiến trúc học tập theo QD_033 không đổi. Chủ trì yêu cầu footer giữa có
link `zomath.vn`, Ủng hộ đồng bộ nội dung/thiết kế từ HTML hiện hành và
nghiên cứu quy cách dàn PDF chính thức từ nguồn, lấy bốn HTML/0.4 làm ý tưởng.

- Đã xem bốn trang của DH_043 và component Ủng hộ chung G01/G02/Home.
  D0 HTML hiện chỉ có link ở rail; mẫu PDF khai binding component chung,
  không giả báo đã trích vùng Ủng hộ đầy đủ từ D0 HTML. Bản audit chỉ để
  đối chiếu; không làm đầu vào dựng hoặc thay bộ bảo vệ QD_035.
- Cập nhật hướng dẫn PDF và `06_pdf_bo_cuc_doc_lap.md`: QMD/JSON sở hữu
  nội dung, hồ sơ/TeX riêng sở hữu dàn in theo vai trò. D0 DH_042 đã có
  adapter, nhưng chưa có bộ vai trò/bản đồ dàn trang riêng đủ hoàn thiện.
  Quy tắc mới thay riêng cách lấy Ủng hộ; không tự khóa Design 0.5.
- `scripts/zo_pdf_support.py` chiếu component HTML nguồn hiện hành:
  tiêu đề/lời mời, trường theo thứ tự, logo/QR, màu heading, CTA/URL;
  lấy lại mỗi lần dựng và fingerprint. Không hard-code bản khai tài khoản
  hoặc đọc HTML audit. Biến thể câu chữ Home cần binding riêng khi áp dụng.
- Mẫu và builder/checker thử riêng từng tạo PDF 10 trang. Script/fixture
  thử đã dọn sau khi duyệt mẫu cuối; PDF mẫu cuối giữ để đối chiếu.
  Có bìa/hướng dẫn, bốn đề/bốn đối chiếu, trích bảng tám mạch, trang kết;
  không phải toàn bộ học liệu. Font thân Be 11/16, toán STIX, cột thông tin
  chuẩn bị/đề, hình vector lớn hơn, bảng native và liên kết số trang.
- Kiểm PASS: nguồn tươi, tám đích trích đoạn, font nhúng; footer URL đúng
  và giữa đủ 10 trang; ca âm sai URL/lệch vị trí bị bắt. Thay tài khoản,
  lời HTML/màu heading trong bộ kiểm làm dữ liệu chiếu đổi; thiếu trường
  bị chặn. Raster đủ ngang/dọc năm bảng trên bốn trang.
- Agent xem đủ 10 trang màu/sắc xám. Chưa in giấy/quét QR điện thoại;
  cảnh báo hyphen-vietnamese còn từ môi trường. Cây dựng/profile browser
  và ảnh bản trung gian dọn; chỉ giữ mẫu/bằng chứng hiện hành để xem.
  Bốn QMD/HTML và D0 `index.pdf` trước mẫu giữ nguyên hash.

**Bước tiếp theo: chủ trì xem mẫu bố cục; sau chọn mới áp dụng toàn bộ D0.**
Chưa nghiệm thu mẫu, commit/push/phát hành. DH_043 Nhà vẫn chờ xem riêng;
DH_042 là bản PDF trước góp ý mới, không tự thỏa yêu cầu thiết kế DH_044.

**DH_043 — Chuyển thiết kế Nhà đã thống nhất vào nguồn, 14/10/2026.**

Kiến trúc học tập vẫn theo QD_033. Mẫu được chủ trì chỉ định
`_audit/home-preview/home-design-trial.html` chỉ đối chiếu thiết kế,
không làm đầu vào biên dịch hoặc nguồn biên tập.

- QMD canonical đặt Hiểu vì sao/Dành cho ai trong hero; Cách học ngay sau
  danh mục. Sáu panel lớn xen trắng–xám trắng, bỏ bốn nhãn động từ; hàng
  Cách học một cột full-width, bo góc/cách hàng/nền xen kẽ. Kiến thức và
  FAQ có khung riêng; học trực tiếp giữ điểm nhấn/minh họa đã duyệt.
- SVG chuyển vào `2027/assets/illustrations/hoc_truc_tiep_trao_doi.svg`,
  SHA-256 khớp mẫu, nạp qua Markdown. Adapter chỉ chuẩn hóa wrapper/ảnh;
  generator sinh số trình bày và partial kiến thức, không đổi thẻ/timer.
- Giữ lời QMD hiện tại thay lời catalog mẫu cũ, DOM thẻ CTA-only, đích,
  ID, toán/heading/disclosure. Phục hồi `trạng-thái-triển-khai` trên câu
  thông báo đã có, không đổi chữ; không còn link thiếu đích. Hai guard
  nguyên văn cũ không khớp nguồn chủ trì vẫn mở, không nới để đạt PASS.
- Bản cuối: `_audit/home-layout-implementation/preview/home-reading.html`.
  Home render từ nguồn bằng launcher Quarto trong cây cô lập; ba trang
  đi kèm chỉ rebase từ DH_039, không render hoặc sửa nội dung. Build từ
  nguồn không đọc audit; không ghi đè root docs hoặc mẫu/bản bảo vệ.
- Generator CURRENT, scope/native/projection/cú pháp đạt; bảo toàn và
  đối chiếu thiết kế 20/20. Home QA cuối 435/437, tất cả kiểm bố cục/tương
  tác đạt; chỉ hai guard câu chữ cũ chưa khép. Edge sáu độ rộng 1440–320
  px: một cột full-width, khung/nền/khoảng cách, FAQ mở, ảnh/tỉ lệ, không
  tràn, hover/Tab/Enter/no-JS/lọc/tìm/timer/điều hướng. Ca âm bốn cột bị
  bắt ở 1440/390. Đã xem intro/Cách học/kiến thức/FAQ/học trực tiếp rộng
  và điện thoại. Chưa Safari/Firefox/cảm ứng thật/screen reader.
- Giữ nguồn/bản xem/runtime và bằng chứng gọn, dọn mirror/profile/ảnh
  thừa/script đối chiếu một lần. Không sửa nguồn/PDF ba học liệu, Git
  index; cập nhật PDF D0 DH_042 riêng được giữ, không coi là tác vụ Home.

**Bước tiếp theo: chủ trì xem HTML Nhà mới; chưa nghiệm thu/phát hành.**
Không commit, push hoặc xuất bản. DH_042/DH_041 và mốc trước giữ bằng
chứng riêng; đoạn trạng thái PDF dưới đây thuộc tác vụ riêng.

Kiến trúc học tập hiện hành theo QD_033; lượt PDF dưới đây không thay đổi
quyết định đường học hoặc trạng thái nghiệm thu của các trang HTML.

### DH_042 — Cụ thể hóa hướng dẫn PDF 0.4 và dựng lại D0, 14/10/2026

Theo yêu cầu trực tiếp sau chủ trì xem DH_040, bổ sung hướng dẫn PDF tại
`_design/ngon_ngu_thiet_ke_zo_math_0_4/04_ap_dung/06_pdf.md`: bìa/kết,
ngày/phiên bản/bản quyền, Ủng hộ, chữ, bảng, phân trang và kiểm hồi quy.
Không khóa Design 0.5 hoặc tự áp dụng sang PDF G01/G02.

- D0 đã dựng lại từ QMD hiện tại, 24 trang vật lý; đề, toán, JSON, ID,
  lời giải và thứ tự giữ nguyên. Bảng dấu native từ JSON; bảng thường
  bỏ lớp phủ nền header che đường viền, nét .5 pt/căn theo chức năng;
  bảng mô tả 36/64. Bìa có ngày/bản quyền, cuối có logo/tài khoản/QR
  Bảo trợ đọc từ nguồn hiện hành. Thêm số trang đích đề/đối chiếu;
  lời giải R8-03 mở trang mới để không có dòng lẻ. HTML không dựng lại.
- Kiểm nguồn QMD PASS; checker D0 bảo toàn nguồn/toán lịch sử 48/48.
  PDF PASS: 50 đích, font nhúng, metadata/Ủng hộ, tham chiếu đã giải,
  một hình hộp vector và bảng dấu native. Kiểm raster đủ ngang/dọc
  bảy bảng trên sáu trang; hai ca âm xóa viền ngang/dọc bị từ chối.
- Agent đã xem đủ 24 trang màu; bìa/kết và mọi trang bảng/hình ở sắc xám.
  Chưa in giấy/quét QR bằng điện thoại. Cảnh báo thiếu hyphen-vietnamese
  còn từ môi trường; đã xem dòng dài, không tuyên bố môi trường hết cảnh báo.
- Bằng chứng ở D0 `pdf_build.json`, `pdf_review.json`, hồ sơ lỗi/guard
  `pdf_quality.md`; ảnh tạm DH_042 đã dọn sau bản dựng production.
  Cây dựng/ảnh trung gian checker được dọn; không stage/commit/push/phát hành.

**Bước tiếp theo: chủ trì xem PDF mới; nghiệm thu và xuất bản vẫn pending.**
DH_040 giữ bằng chứng lần dựng đầu, không chứng nhận chất lượng bản mới.

**DH_041 — Thẻ Nhà chỉ điều hướng qua dòng hành động, 14/10/2026.**

Kiến trúc học tập vẫn theo QD_033. Theo yêu cầu chủ trì, bỏ anchor phủ cả
thẻ; ảnh/tiêu đề/mô tả/nền không điều hướng. Chỉ “Làm khảo sát →” và
“Mở tài liệu →” là liên kết. Giữ hover viền/bóng/màu tiêu đề toàn thẻ;
CTA đổi màu/mũi tên, focus bàn phím rõ, không nền sáng hoặc gạch chân.

- Sửa generator, CSS Home, checker; sinh lại riêng `home_catalog.qmd`.
  Quy tắc cập nhật ở 07/README giao diện/kit; HOM-C01 ghi nguyên nhân và
  guard. Không sửa câu chữ QMD, nguồn/HTML D0 hoặc R1, đồng hồ hay PDF.
- Khi dựng, phát hiện generator còn ép D0 PDF mới vào hợp đồng tám PDF
  R1. Sửa tối thiểu nhận diện đúng D0 với PDF toàn trang đang chờ duyệt;
  giữ CTA khảo sát/không công bố link tải, ca âm không nới hợp đồng R1.
- Home render tươi trong cây cô lập, không ghi đè root docs hoặc QD_035.
  Bản xem: `_audit/home-card-actions/preview/home-reading.html`; ba trang
  liên kết là phép rebase từ DH_039, không render lại hoặc thay nội dung.
- Nguồn Home chưa có cấu hình CLI QMD: kiểm scope bằng checker lõi,
  kiểm native/projection bằng checker Home. Generator CURRENT, cú pháp
  Python và kiểm scope đạt. Edge sáu độ rộng: toàn bộ kiểm thẻ/CTA,
  pointer thật, Tab/Enter, focus, no-JS, tìm/lọc và không tràn đạt.
  Home QA mới 361/365, không gọi toàn bộ Home PASS: ba kiểm câu chữ/ID
  cũ khác QMD chủ trì đã sửa và link `#trạng-thái-triển-khai` mất đích.
  Giữ nguồn chủ trì, không sửa hay nới phép kiểm để đạt PASS.
- `build.json`, hai QA đầu/cuối và `source-state.json` lưu nguồn/guard/
  phạm vi; ảnh desktop/mobile giữ để xem. Dọn cây dựng, profile Edge và
  ảnh kiểm thừa. Chưa nghiệm thu chủ trì, Safari/Firefox/thiết bị thật;
  không stage, commit, push hoặc xuất bản.

**Bước tiếp theo: chủ trì xem tương tác thẻ; lỗi link nội bộ Nhà còn mở.**
DH_040 (PDF D0) và DH_039 (điều hướng) vẫn chờ xem riêng.

### DH_040 — PDF D0; chờ chủ trì xem

**DH_040 — Dựng PDF toàn trang Khảo sát đầu vào, 14/10/2026.**

Kiến trúc học tập vẫn theo QD_033; PDF không là điều kiện để vào học.

- Theo yêu cầu trực tiếp của chủ trì, dựng một `hoc_lieu/d0/index.pdf` từ
  `hoc_lieu/d0/index.qmd` hiện tại. PDF có 25 trang, đầy đủ 24 câu khảo sát,
  Bài 00 và 25 phần đối chiếu; không phục hồi bốn biến thể lịch sử.
- Bổ sung cấu hình PDF/lớp TeX–Lua cục bộ, font/logo 0.4 có giấy phép,
  bảng LaTeX đủ lưới, hai hình vector hiện có, mục lục, liên kết và QR.
  `cong_cu/dung_pdf.py` dùng launcher repo, cô lập trung gian, thay PDF
  sau thành công và tự dọn cây dựng. Nội dung QMD chỉ thêm metadata PDF;
  đề, toán, lời giải, ID và thứ tự không đổi. Không render hoặc sửa HTML.
- Sửa tối thiểu guard HTML-only: chỉ nhận đúng hợp đồng PDF toàn trang
  được giao và delta metadata đã khóa; receipt nghiệm thu cũ không đổi.
  Đảo delta trong bộ nhớ rồi đối chiếu lại toàn nguồn. Quyết định HTML-only
  trước đó không được tái áp dụng để cấm yêu cầu mới này. Nguồn/lệnh/
  phạm vi tại README D0; con trỏ README khóa/08 đã đồng bộ.
- Kiểm nguồn QMD đạt; checker D0 đạt, toán lịch sử 48/48; kiểm PDF đạt:
  50 đích đề/đối chiếu, font nhúng, khổ A4, hai hình vector và các URL.
  Cổng điều hành tài liệu 175/175. Đã xem đủ 25 trang, kiểm trang bảng,
  hình hộp/công thức và phần đối chiếu ở cỡ đọc; xem sắc xám đại diện.
  Chưa in giấy, quét QR bằng điện thoại hoặc nghiệm thu của chủ trì.
- Bằng chứng gọn ở D0 `_quy_trinh/pdf_build.json` và `pdf_review.json`.
  Giữ nguồn/PDF/receipt, dọn cây dựng, script chẩn đoán và ảnh kiểm tạm;
  không tạo bản nguồn song song trong `_audit/`. Không thay nguồn Nhà,
  G01/G02, các HTML/bản xem bảo vệ hoặc PDF khác; không stage/commit/push.
  Đã dọn 135 tệp kiểm/chẩn đoán tạm (30.108.731 byte); các tệp này có thể
  dựng lại. HEAD/index và 32 tệp thay đổi có sẵn ngoài phạm vi giữ nguyên.
- DH_039 vẫn chờ chủ trì xem điều hướng; hai kiểm câu chữ Nhà còn mở
  không được chứng nhận bằng việc dựng PDF D0.

**Bước tiếp theo: chủ trì xem PDF D0; chưa xuất bản.**

### DH_039 — Đồng bộ hover điều hướng; chờ chủ trì xem

**DH_039 — Đồng bộ hover điều hướng toàn khóa, 14/10/2026.**

Kiến trúc học tập vẫn theo QD_033; lượt này chỉ sửa hình thức điều hướng
QD_032, không thay đường học hoặc trạng thái nghiệm thu nội dung.

- Chủ trì chỉ rõ D0/G01/G02 còn kiểu cũ: nền hover sáng và gạch chân mục
  hiện tại. CSS chung nay dùng hover đổi màu chữ/icon như Nhà; giữ chữ
  đậm/`aria-current` cho trang hiện tại và outline focus bàn phím. Không
  đổi rail, tiêu đề, câu chữ, QMD, toán, tài sản hoặc mốc đồng hồ.
- Nguồn sửa: `course-navigation.css`, checker điều hướng; ghi quy tắc ở
  07 và nguyên nhân/guard ở README/kiểm thử kit. Không sửa generated HTML
  trực tiếp hoặc quay lại dùng lớp riêng của Nhà để chứng nhận ba trang.
- Bản xem: `_audit/navigation-preview/html-current/home-reading.html` và
  ba trang liên kết, cả bốn render tươi từ nguồn trong cây cô lập rồi nối
  adapter canonical. `build.json` ghi hash QMD lúc tạo bản xem;
  `source-state.json` phân biệt nguồn Home lúc render với lần lưu mới
  ngoài tác vụ lúc 00:11 ngày 14/10; không hoàn nguyên hoặc render đè
  lần sửa ấy. `qa-browser.json` ghi hash
  CSS/checker. URL bản xem được rebase riêng, không làm đầu vào render.
- Kiểm điều hướng: static 65/65; Edge 765/765 trên 1440/1000/768/430/390/320
  px, hover pointer thật của bốn mục/ba icon, mục hiện tại, focus, Escape,
  no-JS, chuyển trang thật, Top/ngữ cảnh, drawer/nền. Ca âm CSS cũ bị bắt.
  Text/heading/ID/math/disclosure bốn trang không đổi so bản xem trước
  `_audit/home-preview` được truyền tường minh. Đã xem ảnh D0 mobile/G02
  desktop; đây không là nghiệm thu toán, thiết bị thật hoặc phát hành.
- Đã dọn cây dựng 478.904.591 byte và 215 tệp delivery không được bản xem
  sử dụng (141.433.495 byte), bỏ script/plan tạm và ảnh kiểm trùng; không
  còn cache browser của lượt này. Giữ bốn HTML, phụ thuộc và bảy ảnh menu
  để chủ trì xem. Đối chiếu hash 4.037 tệp ngoài sáu tệp sửa: chỉ nguồn
  Home đổi ngoài tác vụ, được giữ nguyên; tất cả tệp còn lại, QD_035/các
  bản bảo vệ, root docs/PDF/HEAD/index không đổi. Không stage/commit/push.
- Hai kiểm câu chữ Home cũ của DH_038 vẫn chưa khép; kiểm điều hướng đạt
  không chứng nhận chúng đã đạt. Không sửa câu chữ chủ trì để ép PASS.

**Bước tiếp theo: chủ trì xem danh sách điều hướng trên bản DH_039.**

### DH_038 — Nguồn Nhà native và lượt tự biên tập; giữ bằng chứng

**DH_038 — Di trú nguồn biên tập Nhà sang Quarto native, 13/10/2026.**

- Chủ trì giao chuyển nguồn Nhà về QMD thật và dọn ngay trung gian không
  còn giá trị. `2027/index.qmd` nay chứa trực tiếp heading/đoạn văn/danh sách/
  FAQ/lời Ủng hộ; không còn wrapper include toàn trang raw HTML. Không đổi
  câu chữ đã chốt, UI, mốc đồng hồ, CSS/JS, ID, toán hoặc ba nguồn D0/R1.
- YAML/metadata thật cấp danh mục/mạch/mốc thi; generator chỉ sinh ba
  component dữ liệu/UI. Binding `scripts/zo_home_qmd.py` không chứa lời
  biên tập; guard chặn wrapper-only, HTML đổi đuôi và template cũ. Bốn đoạn
  Nhà đã di trú không còn bản biên tập YAML song song. Con trỏ thẩm quyền,
  bảo toàn, profile và registry đã theo nguồn mới; không sửa lịch sử QD.
- Bản mới: `_audit/zo_home_qmd_migration_20261013/delivered-final/home-reading.html`
  và ba trang liên kết. Home dựng từ nguồn hiện hành trong cây cô lập;
  ba trang kia là projection chỉ rebase URL của đúng DH_037 đã chỉ định,
  không phải dựng lại hoặc thay nguồn/HTML được bảo vệ. QD_035, DH_037,
  root `docs/`, PDF, checkpoint và mọi tài nguyên của chúng giữ nguyên.
- QA Home cuối 265/265: nguồn/component/runtime tươi, ca âm, sáu độ rộng,
  đồng hồ tick/tính giờ, hover/focus, FAQ/no-JS, đi và quay về Home mới qua
  D0/G01/G02. Đối chiếu độc lập DH_037: inventory và cây DOM/thuộc tính
  trừ URL rebase giống nhau; lời Ủng hộ cũng giữ nguyên. QA QD_033 nguồn/
  DOM bốn trang 1297/1297; không chạy lại toàn bộ routing browser hai gói
  vì đầu vào/DOM/runtime liên quan không đổi. Giới hạn QD_022 ghi tại report.
- Template/partial toàn trang cũ được lưu nguyên byte ngoài repo tại
  `E:/zo_math_ca_nhan/legacy_backup_archive/ZO_MATH_HOME_QMD_MIGRATION_20261013`,
  kiểm SHA-256 trước khi gỡ. Không dùng bản lưu làm input build. Cây dựng,
  preview thử và cache của lượt này chỉ gỡ sau kiểm phụ thuộc/đường dẫn;
  kết quả thật trong `final-checks.json` và `cleanup.json` cùng audit nhiệm vụ.
- Trạng thái: nguồn native và HTML kiểm kỹ thuật, chưa là nghiệm thu HTML
  của chủ trì, PDF hoặc phát hành. Đã xem ảnh desktop/mobile và vùng Cách
  học. Không stage, commit, push hoặc xuất bản; không khởi động kết sổ repo.

**Lượt dựng lại sau chủ trì tự biên tập QMD, 13/10/2026:** bản xem tại
`_audit/home-preview/home-reading.html`, nguồn vẫn là `2027/index.qmd`.
Giữ nguyên câu chữ chủ trì; chỉ thêm neo vào thông báo bổ sung tài liệu
hiện có để giữ đích mục lục. Đồng hồ sinh lại từ generator hiện hành.
Sửa bộ nối Home làm mất ID tiêu đề khi Quarto chuyển ID lên fenced div:
chỉ trả ID khai báo trong nguồn về tiêu đề, vẫn bỏ ID tự sinh; ca thử cả
hai trường hợp đạt. Guard neo Home hiện hành kiểm lại đạt.
QA mới tại `_audit/home-preview/qa-final.json`: 263/265, không thiếu
liên kết/tài nguyên; 175 kiểm trình duyệt đạt.
Hai kiểm chưa đạt vẫn đòi câu cũ về quay lại tự làm và danh mục hiện có;
không sửa lời chủ trì hoặc nới checker để đạt PASS. Không tuyên bố toàn
bộ QA đạt hay đã nghiệm thu. Cây dựng tạm được dọn sau kiểm phụ thuộc;
giữ bản xem, runtime và kết quả kiểm tại cùng thư mục. D0/G01/G02 chỉ
rebase bản xem trước, không dựng lại; các bản bảo vệ, docs/PDF/Git giữ nguyên.

**Bước tiếp theo: chủ trì xem HTML mới và phản hồi.** Hai kiểm nguyên văn
cũ cần được đối chiếu với cách viết mới trước khi khép QA/xuất bản; không
tự đổi quy tắc kiến trúc hoặc sửa câu chữ để đáp ứng phép kiểm cũ.

### DH_037 — Bản sửa QD_033 trước di trú nguồn Nhà; giữ lịch sử/bằng chứng

**DH_037 — Áp dụng bốn nhóm hiệu chỉnh QD_033, 13/10/2026.**

- Chủ trì đã duyệt sửa nguồn theo khảo sát bốn trang: A01 Nhật kí theo
  ngữ cảnh tại 12 Điểm dừng; A02 Sửa lỗi ở G02 chỉ khi cần; A03 kết thúc
  lượt Kiểm tra trước trợ giúp và giữ riêng bài ban đầu trên Nhà; A04 giữ
  nơi gọi khi xem lại Bài học, tải lại/Back và chuyển tiếp sang hỗ trợ.
- Nguồn QMD G01/G02, template/partial Nhà và controller dùng chung đã
  hiệu chỉnh; binding G01 chỉ cập nhật bốn đoạn và provenance controller.
  Không đổi kiến trúc, toán, ID, nhãn, CSS, tài sản toán hoặc nguồn D0.
- Bốn trang dựng từ nguồn canonical trong cây cô lập, không dùng HTML
  lịch sử làm đầu vào. Bản mới:
  `_audit/zo_qd033_apply_20261013/html-current/home-reading.html` và ba
  trang liên kết tại đó. Bản chọn QD_035, runtime, `docs/`, PDF và các
  checkpoint bảo toàn giữ nguyên. Không stage, commit, push hoặc xuất bản.
- Bằng chứng hiện hành ở `_audit/zo_qd033_apply_20261013/`: `qa-final/qa.json`
  kiểm A01–A04, nhãn/sở hữu, ma trận DH01–DH14 và runtime đại diện;
  `qa-browser.json` kiểm điều hướng bốn trang; `final-checks.json` kiểm
  phạm vi/hash/cổng điều hành. Lỗi tải trình duyệt của lượt đầu giữ riêng,
  không được tính PASS hoặc ghi lại receipt cũ.
- Trạng thái: nguồn/HTML kiểm trong phạm vi, chờ chủ trì duyệt bản mới;
  không phải kiểm toán toán độc lập, nghiệm thu PDF hay phát hành.
  Guard mới `scripts/zo_qd033_route_check.py` đã được dẫn trong kit và
  registry; không nới schema/checker hoặc tái áp dụng QD_021.

**Bước tiếp theo:** chủ trì xem bốn trang trong bản mới; chỉ sau khi duyệt
mới giao bước bảo toàn/commit hoặc thay bộ bản xem đã chọn. Không tự thay
QD_035 bằng bản mới và không mở gói khác.

### DH_036 — Commit bảo toàn cục bộ: đã khép, giữ để truy nguyên

**DH_036 — Khép phạm vi commit bảo toàn cục bộ, 13/10/2026.**

- Chủ trì đã duyệt báo cáo rà Git và giao làm tiếp: xử lí tối thiểu con trỏ
  thẩm quyền/provenance, chốt danh sách rồi tạo commit cục bộ sau kiểm.
  Không sửa bốn trang, render, dọn thêm, push hoặc xuất bản; QD_033/QD_035
  tiếp tục có hiệu lực, không tạo quyết định kiến trúc hoặc nghiệm thu mới.
- Danh sách đã rà gồm 877 mục Git. Phạm vi bảo toàn dự kiến 911 mục: bỏ
  ZIP .tmp khỏi Git nhưng giữ nguyên tệp; thêm 34 tham chiếu gốc bị ignore
  và một hồ sơ provenance binding. Các xóa tài liệu điều hành cũ đi cùng
  nguồn canonical thay thế; Kế hoạch 0.6 chuyển vị trí vẫn nguyên byte.
- Kit, binding Design, con trỏ tiếp nhận Web và thẩm quyền hồ sơ G01 lấy
  QD_033 thay chỉ dẫn QD_021 đã bị thay; số liệu QA/receipt/lịch sử không đổi.
  Công việc Design chỉ trỏ về đây, không duy trì roadmap khóa song song.
- Manifest Design gốc giữ nguyên: có một sai khác binding tích hợp cục bộ
  ở `04_ap_dung/01_web_2027.md`; hồ sơ provenance mới ghi rõ gốc/hiện tại,
  không thay hash hoặc nới checker để đạt PASS. Nguồn/mẫu khóa 06/07 và
  bộ bản xem chủ trì chọn QD_035 giữ nguyên, không đưa `_audit/`/`docs/` vào Git.
- Chỉ nhận khép khi receipt tại `_audit/zo_preservation_commit_20261013/`
  ghi cổng điều hành, kiểm phạm vi và tính toàn vẹn staged set/blob đạt. SHA commit và
  trạng thái Git sau thao tác tra `result.json`; không tự ghi mã commit
  của chính tài liệu này hoặc suy việc đã thêm tệp là đã commit.
- Kiểm tài liệu sau đồng bộ đạt 170/170 và self-test 228/228; ranh giới
  biên dịch kiểm 161 nguồn không lỗi, partial khóa vẫn CURRENT. Hồ sơ
  provenance binding khớp hash hiện tại; 360 tệp specimen khớp manifest.
  Đây không là kiểm nội dung/toán/UI hoặc chứng nhận bản bàn giao gốc
  nguyên byte. Kiểm cuối phạm vi/staged/commit ghi ở receipt riêng nêu trên.
- `git diff --cached --check` còn cảnh báo khoảng trắng/dòng trống cuối
  tệp trong nguồn/tham chiếu hiện có, kể cả PDF mẫu Git nhận là text.
  Giữ nguyên byte các tệp đã rà để bảo toàn; ghi riêng cảnh báo trong
  `staged-check.json`/`staged-whitespace.txt`, không báo phép kiểm này PASS,
  không sửa mẫu khóa, cấu hình phép kiểm, receipt hoặc nội dung để che lỗi.
  Danh sách và blob staged phải khớp chính xác phạm vi được duyệt.

**Bước tiếp theo:** sau khi commit bảo toàn kiểm đạt, đối chiếu việc áp dụng
QD_033 trên nguồn/bản xem bốn trang trong nhiệm vụ riêng khi chủ trì giao;
chưa tự biên tập hoặc dựng lại. Giữ nguyên các checkpoint và bản xem QD_035.

### DH_035 — Dọn phần lịch sử: đã khép, giữ để truy nguyên

**DH_035 — Dọn phần lịch sử còn lại, 13/10/2026: đã khép đúng bảy cache còn vướng bằng quyền thông thường.**

**QD_033 vẫn là thẩm quyền hiện hành của đường học**; DH_035 không thay quyết định này hoặc nâng nghiệm thu sản phẩm. QD_035 tiếp tục bảo vệ đúng bộ bản xem đã chọn.

- Đã lưu và gỡ **25.377 tệp/5.827.249.232 byte**: 25.367 tệp lịch sử `_audit/` và 10 tệp trong `.pytest_cache/`, thư mục giả `%SystemDrive%/`. Kho: `E:/zo_math_ca_nhan/legacy_backup_archive/ZO_MATH_FINAL_CLEANUP_20261013`. SHA-256 từng bản nguồn/bản lưu được kiểm trước khi gỡ; manifest lịch sử `36bb23ecb1bc0c849d2b90dab27f4873adc99b87056da9b05a46c34a000f5942`, cache `e69018a2ab888a4e1a779c43fa822849c9c4b52c9a617a7437d5dae75a0e9a11`. Chỉ mục [lưu trữ](luu_tru_lich_su.json) dẫn cách khôi phục; kho cùng ổ E, không coi số giảm trong repo là dung lượng trống ròng.
- Giữ nguyên **2.987 tệp được bảo vệ**, toàn bộ delivered QD_035, runtime và bộ DH_030. Payload hai checkpoint đã kiểm lại. Nguồn, nội dung, thiết kế, trạng thái nghiệm thu không đổi; HEAD/index và trạng thái Git không đổi bởi thao tác dọn. Các nguồn chưa commit không bị coi là rác. Hồ sơ QA lịch sử không được chỉnh để chứng nhận bản mới.
- Cổng tài liệu 228/228, ranh giới nguồn 161 tệp/không lỗi; hồi quy ranh giới 12/12 và hình học 33/33 chạy lại sau dọn. Không render, stage, commit, push hoặc xuất bản trong DH_035. Helper/kế hoạch một lần được lưu ngoài repo và gỡ khỏi thư mục làm việc; chỉ giữ receipt ngắn ở `_audit/zo_cleanup_final_20261013/`.
- Vướng quyền ở lượt trước giữ nguyên trong receipt `_audit/zo_cleanup_final_20261013/final-checks.json`: bảy cache chưa đọc/hash/sao lưu được và yêu cầu quản trị bị auto-review từ chối. Lượt tiếp nối theo chỉ thị mới chỉ kiểm lại đúng bảy đường dẫn bằng quyền thông thường; lần này đọc/hash được toàn bộ, không yêu cầu nâng quyền, đổi ACL hoặc vượt chặn.
- **Đã lưu và gỡ bổ sung đúng bảy cache, 630 tệp/59.785.703 byte**, không mục nào phải bỏ qua. Kho riêng: `E:/zo_math_ca_nhan/legacy_backup_archive/DH035_7_CACHE`, giữ cấu trúc repo trong `payload/` và thư mục rỗng; manifest SHA-256 `12d9655d6c6bfe06e2b943ef6a037688b5178f727e570b18f6d9487771e7e4f1`. Đã resolve từng đích, rà phụ thuộc/tệp tracked/danh mục bảo vệ, kiểm reparse/sharing và SHA-256 cả nguồn lẫn bản lưu trước gỡ. Kho dùng tên ngắn để tránh giới hạn đường dẫn Windows, không sử dụng thay đổi quyền; có `RESTORE.md` hướng dẫn khôi phục. Kho cùng ổ E nên số byte gỡ không phải dung lượng trống ròng.
- Kết quả cuối lượt bổ sung tra `scope-result.json` trong kho và `_audit/zo_cleanup_final_20261013/ordinary-cache-result.json`: chỉ nhận kiểm đạt khi bảo toàn nguồn/bản xem, HEAD/index/trạng thái Git và hai cổng điều hành đều đạt. Receipt trước không bị viết lại; không làm lại phần đã dọn hoặc khảo sát/dọn nhóm khác. **Không còn mục vướng trong danh sách bảy cache**, không suy thành chứng nhận toàn repo sạch. Helper tạm của lượt bổ sung được gỡ sau kiểm; không sửa nội dung/giao diện, render, stage, commit, push hoặc xuất bản.

**Bước tiếp theo khi khép DH_035 (lịch sử):** dừng lượt dọn DH_035; tiếp tục phát triển từ nguồn hiện hành và bộ bốn bản xem được bảo vệ khi chủ trì giao nhiệm vụ cụ thể. Không cần yêu cầu quyền quản trị cho bảy cache đã gỡ, không mở thêm vòng dọn hoặc tự biên tập học liệu. Việc hiện hành được DH_036 tiếp quản phía trên.

### DH_034 — Khép ranh giới nguồn biên dịch: đã kiểm đạt, giữ để truy nguyên

**DH_034 — Khép ranh giới nguồn biên dịch, 13/10/2026.**

- Chỉ thị chủ trì: xử lí tận gốc, không để `_audit/` tham gia biên dịch chính thức. Không thay QD_033, nội dung, thiết kế hoặc trạng thái nghiệm thu bốn trang.
- Cổng `scripts/zo_build_boundary.py` kiểm nguồn QMD/config/include và tham số dựng; launcher Quarto và runtime Python chặn đọc nguồn lịch sử trong `_audit/`. PDF/vector tạm chuyển sang `.quarto/`. Fixture hình học ở `scripts/fixtures/geometry/`, dùng helper/compiler/checker/style canonical.
- Bỏ việc tự chọn baseline theo ngày ở phép kiểm điều hướng và preview Nhà; bản nháp chủ trì của phép kiểm di trú G01 chỉ đọc khi truyền tường minh. Báo cáo ghi rõ phép đối chiếu lịch sử có được chạy hay không. Không chuyển bản xem QD_035 thành nguồn build.
- Đã dựng đủ Nhà/D0/G01/G02 trong cây nguồn không có `_audit/` trước và sau render, cả bốn adapter chạy thành công. Nguồn bốn trang/template và toàn bộ `docs/` khớp hash trước–sau. Bằng chứng: `_audit/zo_official_build_boundary_20261013_closed/result.json`; mirror biên dịch tự dọn. Đây là kiểm độc lập nguồn, không nghiệm thu lại nội dung/thị giác hoặc PDF.
- Kiểm ranh giới 12 ca, hồi quy hình học 33 ca, định danh/provenance QMD–PDF 18 ca và self-test PDF đạt. Cổng điều hành được chạy lại sau đồng bộ. Chưa commit, push hoặc xuất bản.

**Bước tiếp theo ghi khi khép DH_034 (lịch sử):** hoàn tất việc phân loại và chốt các nguồn có giá trị trong Git theo nhiệm vụ riêng; những bản xem QD_035 tiếp tục được bảo vệ. Không còn phải giữ lịch sử `_audit/` để dựng bốn trang. Việc dọn hiện hành tiếp quản ở DH_035 phía trên.

### DH_033 — Dọn bản sao thừa: đã hoàn tất, giữ để truy nguyên

**DH_033 — Dọn bản sao thừa, giữ thành quả và quy tắc đã duyệt.**

- Chỉ thị hiện hành ngày 13/10: chủ trì giao tự thực hiện dọn an toàn, không trình duyệt lại từng thủ tục kỹ thuật. Chỉ hỏi khi cần đổi nội dung/thiết kế đã chốt hoặc có nguy cơ mất kết quả chưa được bảo toàn. Việc lưu trữ, kiểm hash và rà phụ thuộc thuộc trách nhiệm agent, không là một vòng nghiệm thu học liệu.
- Giữ nguyên toàn bộ nguồn canonical, quy tắc sản xuất đã duyệt và bộ bản xem QD_035 ở `_audit/zo_home_refinement_2026-10-12/delivered/` cùng các đích/phụ thuộc trong manifest DH_032. **QD_033 vẫn là thẩm quyền hiện hành của đường học**; không sửa registry, checker, QMD, HTML/CSS, hình hay PDF, không render/Git/xuất bản.
- Đã rà tham chiếu từ nguồn/cấu hình/công cụ hiện hành, theo tiếp phụ thuộc HTML được giữ, loại tệp tracked và manifest bảo vệ. **Đã lưu và gỡ đúng 111 cây bản sao/đầu ra thử/hồ sơ trình duyệt cũ, 65.245 tệp/14.281.566.422 byte**, không phải bỏ qua cây nào trong danh sách được chọn. Kho ngoài repo: `E:/zo_math_ca_nhan/legacy_backup_archive/ZO_MATH_RESIDUAL_CLEANUP_20261013`; manifest SHA-256 `43b0cfeeff17276a93fe5f95c2d96fd9d8830c2ec8519f88c7ceac48bbab292f`. Từng bản sao đã kiểm khớp; trước xóa đã resolve đích, kiểm đúng tập tệp/thư mục, sharing/reparse và SHA-256 cả nguồn lẫn bản lưu. Đây là số byte bản sao giảm trong repo, không phải dung lượng trống ròng của ổ E.
- Giữ hồ sơ còn được tham chiếu, runtime/fixture còn dùng, hai thư mục chưa đọc được, `docs/`, `_freeze/`, `.quarto/_freeze/`, Design và `.git/`. Các bản điều hành trong cây lịch sử chỉ phục vụ khôi phục/đối chiếu; không tái áp dụng quy tắc bị thay.
- Bằng chứng khép tại kho này: `archive-verified.json`, `deletion.json`, `final-checks.json` và `result.json`. Chỉ nhận kiểm đạt khi hai tệp cuối đều `passed: true`: hai cổng điều hành, ba checkpoint hiện có, SHA-256 bản lưu, nguồn/bản xem được bảo vệ, HEAD/index và thay đổi ngoài phạm vi. [Chỉ mục khôi phục](luu_tru_lich_su.json) không là một nguồn điều hành mới; các checkpoint/kho cũ không bị ghi đè.

**Bước tiếp theo sau DH_033 kiểm khép đạt: Tiếp tục phát triển từ nguồn hiện hành của bốn trang và bộ bản xem đã bảo vệ khi chủ trì giao nội dung cần làm.** Không mở thêm vòng duyệt báo cáo dọn/checkpoint; lượt này không tự mở nhiệm vụ biên tập học liệu hoặc xin duyệt lại những quy tắc đã chốt.

### DH_032 — Bảo toàn đúng bộ bản xem chủ trì chọn: đã kiểm đạt, giữ để truy nguyên

- Chủ trì đã giao bảo vệ Home `_audit/zo_home_refinement_2026-10-12/delivered/home-reading.html` và các trang liên kết; QD_035 xác lập vai trò nguồn đối chiếu chính thức, không được dọn/xóa hoặc tự thay bằng bộ khác. [Danh mục bảo toàn](bao_toan_bon_trang.md) sở hữu phạm vi; nguồn dựng canonical không đổi.
- QD_035 chỉ điều hành bảo toàn đúng bản. **QD_033 vẫn là thẩm quyền hiện hành của đường học**; không đổi registry hoặc lấy bảo toàn làm chứng nhận học liệu đã đạt quyết định này.
- Checkpoint bổ sung riêng: `E:/zo_math_ca_nhan/checkpoints/DH032_20261013_BO_BAN_XEM_CHU_TRI_CHON` và ZIP cùng tên; chứa đúng delivered/runtime, các đích Home liên kết trực tiếp và nguồn/phụ thuộc đang được bảo vệ. Không ghi đè hai checkpoint cũ hoặc lấy lại driver đã nghỉ dùng. Manifest nêu rõ byte/hash, vai trò và giới hạn khác nhau giữa bản Home đối chiếu và nguồn hiện hành.
- Trạng thái bảo vệ: **đã xác lập danh mục không được dọn/xóa cho đúng bộ**. Kết quả checkpoint chỉ có hiệu lực theo `verification.json` và `scope.json` ngoài repo đều kiểm đạt cùng hai cổng điều hành; số tệp/hash tra manifest và kết quả kiểm mới. Không lấy việc đã thêm quy định bảo vệ làm bằng chứng checkpoint đã đạt.
- Phạm vi repo chỉ danh mục bảo toàn, 03/04/08 và README điều hành. Không sửa học liệu/bản xem/tài sản/PDF, không render, dọn thêm, Git hoặc xuất bản. Giữ lịch sử quyết định cũ nguyên byte; quyền bảo toàn không là quyền đổi nội dung hoặc nghiệm thu.

**Bước tiếp theo ghi khi khép DH_032 (lịch sử): Chủ trì duyệt báo cáo bảo toàn đúng bản; sau đó mới chốt phạm vi tinh chỉnh nguồn.** Checkpoint đã kiểm đạt; chỉ thị dọn an toàn không xin duyệt thủ tục của chủ trì tiếp quản tại DH_033. Không dùng yêu cầu duyệt báo cáo cũ để chặn lượt dọn hiện hành hoặc suy thành quyền biên tập học liệu.

### DH_031 — Khép lưu trữ và ngừng dùng công cụ lịch sử: đã kiểm đạt, giữ để truy nguyên

- Chủ trì cho phép tiếp tục phương án `phuong_an_go_phu_thuoc_lich_su_20261013.txt` với điều kiện an toàn và giữ thành quả. QD_034 chỉ điều hành lưu trữ/nghỉ dùng công cụ; **QD_033 vẫn là thẩm quyền hiện hành của đường học**. Không sửa 01/07/schema/registry hoặc checker canonical; không dùng PASS lưu trữ để nghiệm thu bốn trang.
- Đợt 1 đã dọn 52 mục cache, 1.035.792.982 byte. Đợt 2 đã lưu 36.495 tệp, 6.833.398.595 byte tại `E:/zo_math_ca_nhan/legacy_backup_archive/ZO_MATH_AUDIT_HISTORY_20261012`; mới gỡ một mirror và hai ZIP thiết kế, 2.711 tệp/957.103.390 byte. Bảy cây còn lại được giữ vì driver lịch sử; không đổi kết quả hoặc manifest của hai đợt này.
- Lượt tiếp nối: đã sao lưu nguyên byte 21 driver và bản trước sửa của 03/04/08 tại `E:/zo_math_ca_nhan/legacy_backup_archive/ZO_MATH_AUDIT_RETIREMENT_20261013`, 24 tệp/273.984 byte; SHA-256 từng bản sao khớp. [Chỉ mục truy nguyên](luu_tru_lich_su.json) dẫn manifest, vai trò và đường khôi phục; không là cấu hình build hoặc nguồn có thẩm quyền thứ hai.
- Trạng thái thao tác: **đã nghỉ dùng 21 script và gỡ đúng bảy cây lịch sử**, không mục nào phải bỏ qua; 33.805 tệp/5.876.405.502 byte được gỡ khỏi repo. Trước mỗi thao tác đã resolve đúng đích, đối chiếu tập tệp/cấu trúc và kiểm tiến trình/reparse; kiểm hash/sharing trước đó khớp từng tệp. Có bản lưu để khôi phục; không tuyên bố dung lượng trống ròng của ổ E từ số giảm trong repo.
- Kiểm trước sửa và trước gỡ: hai cổng điều hành 170/170 và 228/228; hai checkpoint nguyên trạng; 2.920 tệp bảo vệ đã chụp hash, 166 liên kết/tài nguyên trực tiếp của bốn bản xem đều tồn tại và không trỏ vào phạm vi gỡ. **Kết quả kiểm cuối chỉ có hiệu lực theo `evidence/result.json`/`passed: true` trong kho bổ sung**, kèm receipt hai cổng, checkpoint, kho lưu và so phạm vi sau gỡ; không lấy việc đã xóa làm chứng nhận kiểm đạt. Bằng chứng mới không ghi đè kết quả cũ.
- Giữ nguồn/bản xem Nhà, D0, G01, G02; `html-current`, `delivery`, bản Nhà `delivered`, mặc định figure `build`, docs/PDF/receipt, Design đã giải nén, hai checkpoint và các thư mục bị chặn đọc. Các phép kiểm cũ giữ nguyên ở kho để truy nguyên; không tái kích hoạt driver hoặc áp quy tắc cũ. Không render, stage/commit/push/xuất bản.

**Bước tiếp theo ghi khi khép DH_031 (lịch sử): Chủ trì duyệt báo cáo khép lưu trữ; sau đó mới mở lượt đối chiếu chỉ đọc nguồn/bản xem R1-G01 và R1-G02 với QD_033.** Công việc hiện hành tiếp quản tại DH_032 theo chỉ thị bảo toàn đúng bản; không dùng bước lịch sử để mở rộng dọn hoặc sửa học liệu.

### DH_030 — Bảo toàn bốn trang: đã hoàn tất, giữ để truy nguyên

- Chủ trì đã duyệt QD_033/DH_029 và giao làm bước bảo toàn. Chỉ ghi nhận duyệt, kiểm kê nguồn/phụ thuộc, sao lưu ngoài repo và kiểm SHA-256. Không sửa bốn trang, QMD/include học liệu, HTML/CSS/tài sản/PDF/bản xem cũ; không dọn repo, stage/commit/push hoặc xuất bản.
- Checkpoint: `E:/zo_math_ca_nhan/checkpoints/DH030_20261012_BON_TRANG` và ZIP cùng tên. Manifest bảo vệ cả tệp tracked/untracked/ignored cần giữ; tách nguồn chính thức, tài nguyên dùng chung, bản xem và bằng chứng lịch sử. [Danh mục bảo toàn và cách tiếp tục](bao_toan_bon_trang.md).
- Trạng thái lượt bảo toàn: **đã sao lưu và kiểm SHA-256 toàn bộ payload cùng từng thành viên ZIP**; bản ghi hoàn tất được đồng bộ vào checkpoint và kiểm lại trước bàn giao. Bằng chứng mới tại `_audit/zo_preservation_2026-10-12/`; số lượng/hash cuối tra `verification.json` ngoài repo. Cổng điều hành 224/224, đầu ra sinh trang Nhà CURRENT. Đối chiếu nguồn/bản xem của D0/G01/G02 với manifest và hash bản xem Nhà/các phép chiếu rebased đều khớp. SHA-256 của 2577 tệp tracked/untracked ngoài phạm vi và 2916 tệp bảo vệ được chọn (gồm ignored/bản xem) không đổi; HEAD/index không đổi. Không dùng việc sao lưu để chứng nhận trải nghiệm hoặc độ mới của PDF.
- QD_033 là thẩm quyền hiện hành của đường học; G01/G02 **chưa được đối chiếu lại ở cấp QMD/HTML với QD_033 nên chưa xác định có nội dung nào cần sửa**, không đổi trạng thái thành đã áp dụng. Đây không phải ghi nhận một lỗi đã biết. Nguồn/HTML hiện có được giữ nguyên để có thể quay lại trước bước kế tiếp.

**Bước tiếp theo ghi khi khép DH_030 (lịch sử): Kiểm kê toàn repo và trình phương án dọn dẹp, chỉ đọc.** Bước này đã hoàn tất và được chủ trì giao dọn có giới hạn; việc hiện hành tiếp quản tại DH_031. Không dùng chỉ thị lịch sử này để mở lại hoặc mở rộng phạm vi dọn.

### DH_029 — Khép kiến trúc học tập: đã duyệt, giữ để truy nguyên

- Phạm vi được chủ trì giao ngày 12/10: cập nhật 01/03/04/07/08, con trỏ lỗi thời và phần hợp đồng/guard tối thiểu chịu ảnh hưởng; không sửa bốn trang hoặc bản xem, không dọn repo/Git/phát hành.
- Đã xác lập Bài học → Luyện tập → Kiểm tra → Ôn lại là tiến trình chuẩn được khuyến nghị nhưng không là điều kiện bắt buộc phải hoàn thành tuần tự; chọn điểm vào theo nhu cầu/chuẩn bị/bằng chứng; bốn hỗ trợ độc lập theo ngữ cảnh; tự lực trong lượt Kiểm tra, kết thúc lượt trước hỗ trợ và giữ riêng bài ban đầu; lưu bằng chứng khác ghi Nhật kí; liên kết quay lại đề chỉ khi tách vị trí. QD_033 ghi mới, lịch sử quyết định giữ nguyên.
- Registry chọn QD_033 cho `learning_route`; báo cáo QD_021 và audit profile G01/G02 được giữ như bằng chứng lịch sử. Đường học hai gói **chưa được đối chiếu lại ở cấp QMD/HTML với QD_033; chưa xác định có nội dung nào cần sửa**, không suy từ PASS tài liệu hoặc nâng nghiệm thu sản phẩm. Schema kiến trúc/nhãn và các quy tắc khác không đổi.
- Kiểm lượt này: `python scripts/zo_python.py scripts/zo_2027_governance_check.py --self-test` đạt **224/224**, phạm vi tài liệu; gồm ca âm quy tắc cũ, hợp đồng sai và giả nâng audit lịch sử thành hiện hành. Cổng ứng viên vẫn chặn cho đến khi QMD/HTML được đối chiếu lại với QD_033. Không tạo report/bản xem audit. Đã rà diff đầu lượt của cả tệp untracked; `git diff --check` không lỗi; SHA-256 tổng hợp của **2569 tệp tracked/untracked ngoài 10 tệp sửa không đổi**, snapshot kích thước/mtime của **144763 tệp ngoài phạm vi** (gồm audit/đầu ra ignored) không đổi; trạng thái Git giữ nguyên các mục sẵn có, index không stage.
- Trạng thái tiếp nối 12/10/2026: **chủ trì đã duyệt bản sửa bộ điều hành**. Không nâng nghiệm thu sản phẩm; việc bảo toàn tiếp quản tại DH_030.

**Bước tiếp theo ghi ở thời điểm kết thúc DH_029 (lịch sử): Chủ trì duyệt bản khép kiến trúc QD_033/DH_029.** Yêu cầu này đã hoàn tất; công việc hiện hành chỉ ở DH_030 phía trên.

### DH_028 — Trang Nhà: kết quả trước DH_029, giữ để truy nguyên

**Lượt câu chữ — đã áp dụng bản chủ trì duyệt ngày 12/10; không phải công việc đang mở DH_029.**
Chủ trì bác bỏ độ dễ hiểu của bản tinh chỉnh trước, rồi duyệt toàn bản viết
lại trong hội thoại và yêu cầu áp dụng. Đã thay toàn bộ câu chữ Home từ
template/YAML/generator/mục lục, bỏ mã D0/R1 khỏi chữ hiển thị nhưng giữ
ID/URL/metadata. Điểm dừng có giải thích; Kiểm tra tự làm, không chia buổi;
Khảo sát đầu vào tự nguyện. Giữ CSS/JS, đồng hồ thật/mốc tạm, QR/tài khoản,
logo, footer và điều hướng. Không sửa nguồn D0/G01/G02.

**Trạng thái: câu chữ đã được duyệt và áp dụng; HTML mới chờ chủ trì xem.**
Bản xem hiện hành duy nhất:
`_audit/zo_home_copy_approved_2026-10-12/delivered/home-reading.html`.
Đối chiếu độc lập bản duyệt **18/18**, không thiếu đoạn/tiêu đề/câu hỏi;
QA nguồn/Edge **258/258**, links/tài nguyên đầy đủ, 320–1440px, no-JS,
hover/focus/native click, timer/menu/theme/footer. Đã xem ảnh desktop/mobile.
**2218 tệp bảo vệ không đổi**; partial CURRENT. Guard chặn mã nội bộ trong
chữ hiển thị và có ca âm thêm D0; không đánh giá đọc hiểu bằng số PASS.
Hồ sơ và danh sách tệp/lệnh ở `report.json` trong audit này; QA cũ giữ nguyên.
Chưa thử trên học sinh thật, Safari/Firefox/thiết bị thật/screen reader;
không PDF, commit, push hoặc xuất bản.

**Việc còn lại của DH_028 (chưa mở trong lượt này): Xem và duyệt đúng HTML trang Nhà đã áp dụng bản câu chữ chốt.**

### Lượt tinh chỉnh trước bản câu chữ chốt — giữ để truy nguyên

**Phản hồi buổi sáng 12/10:** đã biên tập nguồn
trang Nhà, đưa danh mục lên ngay sau bìa/trước “Biết vì sao. Tự mình làm được.”,
giữ ngày/giờ/tính đồng hồ và logo/font/điều hướng. Nhãn ngày 13px một dòng
căn tâm; thẻ một anchor native phủ ảnh/nội dung, viền/bóng nhẹ/đổi màu tiêu đề;
Home không gạch chân hoặc thêm nền hover sáng. Trợ giúp linh hoạt, học sinh
quay lại tự làm; Kiểm tra vẫn tự lực. CSS chỉ scoped Home; chưa sửa hover
của D0/G01/G02, không áp phân cấp tiêu đề chưa duyệt hoặc nâng Design 0.5.

**Trạng thái lịch sử: đã kiểm kỹ thuật; chủ trì bác bỏ câu chữ.**
Bản xem lịch sử của lượt này:
`_audit/zo_home_refinement_2026-10-12/delivered/home-reading.html`.
QA cuối **255/255**, Edge 320–1440px, pointer hover, bàn phím, click thật
trên ảnh khi không JS, timer/tính giờ/đổi tab/hết hạn, catalog/menu/theme/
footer/links; không link hoặc tài nguyên thiếu. Đã xem ảnh desktop/mobile.
**2218 tệp bảo vệ nguyên trạng**, bao gồm D0/R1, Design 06/07, root docs,
Git index; nguồn/partial kiểm CURRENT. Hồ sơ ở audit lượt này; không commit,
push, PDF hoặc phát hành. Kiểm chưa bao gồm Safari/Firefox/thiết bị thật.

### Bằng chứng DH_028 trước lượt tinh chỉnh buổi sáng — giữ để truy nguyên

**Mốc đồng hồ đã sửa và kiểm trước lượt tinh chỉnh.**
Mốc tạm 11/06/2027 14:30 (giờ Việt Nam), tham chiếu lịch Toán 2026 đã
xác minh, không phải lịch chính thức 2027. Nguồn cấu hình duy nhất tại
`program.exam_countdown`; thay guard buộc để trống đồng hồ bằng guard
ngày/giờ/năm/trạng thái/chú thích. Bản xem mới trong
`_audit/zo_home_countdown_2026-10-12/preview/home-reading.html`.
Không coi QA 187/187 bên dưới là bằng chứng của đồng hồ mới. Những phần
còn lại của Home, D0/R1, Design khóa, root docs/PDF/Git giữ phạm vi cũ.
QA đồng hồ/Home cuối **212/212**, nguồn tươi và Edge 320–1440 px, no-JS,
tick thật, tính giờ/quay về tab/hết mốc/reduced-motion tại `preview/qa-*.json`;
cổng tài liệu 172/172 tại `governance-handoff.json`. Đã xem ảnh desktop/mobile;
projection phần ngoài đồng hồ bằng bản Home trước, 2217 tệp bảo vệ không đổi.
Chi tiết/tệp sửa/lệnh và giới hạn tại `report.json` trong audit đồng hồ.
Chờ chủ trì duyệt thiết kế cụ thể; chưa đồng bộ giờ mạng hoặc thử screen reader.
Chỉ Home được đổi bố cục/câu chữ theo tài liệu mới; không đổi nội dung toán,
ID, kiến trúc hoặc giao diện D0/G01/G02. Giữ kiến trúc QD_028, đường học
QD_021, Kiểm tra QD_024, nhãn QD_025, ký pháp QD_029, bảng QD_030 và điều hướng QD_032. Không triển khai phương
án phân cấp tiêu đề dùng chung chưa duyệt.

**Trạng thái: đã tích hợp nguồn và khép QA HTML, chờ chủ trì duyệt.**
Nguồn tại `2027/giao_dien/trang_nha.html.tpl`, dữ liệu/danh mục vẫn canonical;
`zo_build_on_thi.py` sinh partial cho index.qmd. Đã nhận đủ năm PNG và HTML,
đổi tên bản sao, kiểm SHA-256; không sửa Downloads. Mẫu nhập chỉ tham chiếu:
không dùng thẻ mô phỏng, JS/QR giả hoặc lịch thi chưa xác minh. Đối chiếu
Design 0.4 theo hồ sơ `_audit/zo_home_redesign_2026-10-12/README.md`.
HTML giao: `delivered/preview/home-reading.html` trong audit ấy. QA cuối
187/187 ở `delivered/preview/qa.json`, sáu độ rộng 320–1440 px, no-JS và mô phỏng reflow
200%; đã xem ảnh. Guard nguồn/shell/metadata/asset/link, dùng hỗ trợ riêng,
QR/footer thật; không chứng nhận native browser zoom, Safari/Firefox hoặc
kiểm toán nội dung hai gói. Bản sao preview của D0/R1 chỉ ánh xạ link, quay
về Home mới thay vì ứng viên cũ; không đổi nguồn. Cổng tài liệu 172/172 ở
governance-handoff.json. 2217 tệp bảo vệ không đổi, xem closure.json.
Không root docs, PDF, Git hoặc phát hành. Bản HTML cụ thể phải duyệt riêng.

Việc xin duyệt bản tinh chỉnh cũ đã được thay bởi bản câu chữ chốt ở đầu
mục A; không tiếp tục từ các bản xem lịch sử hoặc dùng QA cũ chứng nhận bản mới.

### DH_027 — điều hướng hiện hành, trước lượt thiết kế lại Home

**DH_027 / QD_032 — Cải tạo điều hướng toàn khóa học trên Nhà, D0, R1-G01, R1-G02.** Chủ trì duyệt mẫu V4; triển khai một nguồn dùng chung theo 07. Giữ kiến trúc QD_028, đường học QD_021, Kiểm tra QD_024, nhãn QD_025, ký pháp QD_029, bảng QD_030 và cấu trúc QD_031. Phân cấp tiêu đề chưa duyệt, không triển khai.

**Trạng thái: đã đồng bộ nguồn và dựng HTML cách ly, chờ chủ trì xem.** Hồ sơ/bốn trang mới: `_audit/zo_course_navigation_2026-10-12/index.html`; chi tiết tại README và closure.json cùng thư mục. Kiểm điều hướng/bảo toàn cuối đạt 480/480 ở sáu độ rộng 320–1440 px, gồm ca âm, bàn phím/no-JS, liên kết thật, các view hai gói, deep-link mobile và Top giữ view. Đã xem ảnh bốn trang. QMD, ID, logo, hệ tiêu đề, vùng đọc, PDF học liệu, root docs, receipt và Git index giữ nguyên; không stage/commit/push/phát hành. Báo cáo lỗi đầu được giữ; QA trước không chứng nhận thanh mới, kết quả lượt này không là kiểm toán toàn bộ toán hay nghiệm thu nội dung.

**Bước tiếp theo DH_027: Xem lại điều hướng trên bốn HTML mới.** Không suy rộng duyệt mẫu thành nghiệm thu toàn nội dung.

### DH_026 — lịch sử backlog trước cải tạo điều hướng

**DH_026 / QD_031 — Giải quyết một lượt backlog đối sánh G01/G02.** Giữ kiến trúc QD_028, đường học QD_021, Kiểm tra QD_024, nhãn QD_025, ký pháp QD_029 và bảng QD_030. QD_031 thay quy tắc cũ về Nhật kí trong Ôn lại, thứ tự/ownership Toàn văn, liên kết đề–đáp án cục bộ và thứ tự đánh số Sửa lỗi; không ghép các khu vực ngang hàng. Bộ điều hành 01/02/07/08, registry, kit, profile và hai adapter tham chiếu cùng quyết định.

**Trạng thái: đã áp dụng nguồn, HTML cách ly chờ chủ trì duyệt.** Hồ sơ mới: `_audit/zo_pair_backlog_2026-10-11/README.md`; bản xem: `index.html` trong cùng thư mục. Kiểm định cấu trúc/nhóm sở hữu ở `qa-structural.json`; kiểm browser bốn trang ở `qa-browser-verified.json` và `qa-browser-extra.json`; bảo toàn toán/ID/root docs/PDF/receipt/Git index được kiểm theo snapshot trước lượt. Năm SVG G02 đều dựng mới theo profile 0.4, manifest ghi đủ hash đầu vào/đầu ra, không dùng SVG cache cũ. Chỉ PDF hình trung gian trong audit; không dựng PDF học liệu. PASS không phải nghiệm thu chủ trì hoặc kiểm toán độc lập toàn bộ toán.

**Bước tiếp theo DH_026: Duyệt HTML G01/G02 mới, đặc biệt Toàn văn, Ôn nền và Sửa lỗi.** Chưa promotion root docs, staging, commit/push hay phát hành. DH_025 và các mục bên dưới là bằng chứng lịch sử, không phải bản xem hiện hành.

### DH_025 — lịch sử dấu ngoặc trước lượt backlog QD_031

**DH_025 / TEX-DEL-01 — Dấu ngoặc LaTeX co giãn.** Yêu cầu trực tiếp ngày 11/10/2026 áp dụng toàn ZO Math; quy chuẩn sở hữu tại `quy_trinh_xay_dung/quy_chuan_dau_ngoac_latex.md`, dẫn từ AGENTS gốc và chuẩn QMD khóa. Giữ kiến trúc QD_028, đường học QD_021, Kiểm tra QD_024, nhãn QD_025, ký pháp QD_029 và bảng QD_030. Chỉ thêm `\left`/`\right`, không đổi toán, ID hoặc nhịp đọc. DH_024 bên dưới là lịch sử kỹ thuật dấu căn, không bị hoàn tác.

**Trạng thái DH_025: đã sửa và kiểm, chờ chủ trì xem HTML.** Kiểm kê bốn trang và include tại `_audit/zo_latex_delimiters_2026-10-11/inventory.json`: G02 17, G01 1, D0 2, Ôn nền N-ĐH-02 dùng chung 1, Nhà không có lỗi thuộc quy tắc này. Guard dùng chung có fixture bắt lỗi và nhận cú pháp đúng; hai adapter gói gọi qua cổng ký pháp. 41 fixture nguồn/CSS đạt tại `source-qa-final.json`; QMD nguồn đạt; QA HTML cuối 1050/1050 tại `qa-verified.json`, mọi view/đóng–mở ở 1440/430/390/320 px. Đã xem ảnh công thức desktop/mobile: dấu ngoặc co giãn bao đủ phân số. Toán chỉ đổi lệnh sizing; ID, bảng, nhịp đọc và sửa dấu căn trước đó giữ nguyên. G01 binding cập nhật có đối chiếu đầy đủ; D0 checker đảo đúng hai delta đã giao, không sửa receipt và vẫn bắt ca âm đổi toán. Root docs, PDF, receipt và Git index thật không đổi. Giữ báo cáo đầu `qa.json` với lỗi phép so nguồn trước hiệu chỉnh; không ghi đè bằng chứng. Không tuyên bố đã rà/sửa mọi nguồn toàn repo hoặc đã kiểm PDF. Bản xem/hồ sơ: `_audit/zo_latex_delimiters_2026-10-11/index.html`.

**Bước tiếp theo DH_025: Duyệt dấu ngoặc co giãn trên HTML mới.** Chưa PDF, promotion root docs, Git hoặc phát hành.

### DH_024 — lịch sử sửa dấu căn trước phản hồi dấu ngoặc

**DH_024 / RAD-01 — Sửa dấu căn inline mất cân đối, giữ QD_029/QD_030.** Kiến trúc/phạm vi QD_028 cùng đường học QD_021, Kiểm tra QD_024 và nhãn QD_025 tiếp tục có hiệu lực; không mở quyết định kiến trúc mới. Tiếp quản HTML bốn trang của DH_023 sau ảnh phản hồi mới. Đã xác minh CSS đặt alias `Math` trùng generic nên Edge dùng Cambria Math thay STIX; riêng căn chứa số mũ còn chọn glyph quá cao. Sửa alias thành `ZOMath`, bù sign 0,8em/con 1,25em **chỉ cho căn inline trực tiếp, không nằm trong phân số/mũ và không chứa cấu trúc cao/lồng**. Giữ native baseline và nội dung MathML; không cắt/transform hoặc đổi biểu thức toán.

**Trạng thái DH_024: đã sửa nguồn kỹ thuật và kiểm, chờ chủ trì xem dấu căn trên HTML.** Bản mới/bằng chứng tại `_audit/zo_radical_balance_2026-10-11/index.html`. Dựng raw mới từ bốn QMD trong bản sao cô lập; QA cuối 1248/1248 tại `qa.json`, 18 fixture nguồn/CSS tại `source-scope-final.json`, guard điều hành đạt. Kiểm Edge 1440/430/390/320 px, mọi view/đóng–mở, bảng không đổi, căn có số mũ và căn trong phân số, font thực STIX trên G01/G02/D0; thêm no-JS 1440/390. Đã xem ảnh desktop/mobile; dấu căn báo lỗi giảm từ 41,16 xuống 28,11 px tại cùng cỡ chữ, radicand vẫn 18,02 px. 1992 tệp bảo vệ không đổi; layout G01 chỉ cập nhật checksum/binding hai CSS, cây vùng đọc/receipt không đổi. QMD, dữ liệu toán, ID, root docs, PDF học liệu và Design khóa không đổi; chưa Git hoặc phát hành.

Giữ `qa-initial.json`: lần đầu dùng phạm vi bù cỡ quá rộng, đã thu hẹp để không can thiệp cỡ native của căn trong phân số/mũ; ngưỡng dư chân căn được hiệu chuẩn theo các variant STIX và vẫn bắt ca âm của lỗi gốc. Không dùng QA chỉ đếm căn/baseline DH_022 hoặc QA bảng DH_023 để chứng nhận tỉ lệ glyph. Nguyên nhân/nguồn/guard trong kit `kiem_thu.md`; `zo_math_notation.py` là cổng chung bốn adapter. Safari/Firefox/thiết bị thật chưa kiểm; không là nghiệm thu hoặc kiểm toán độc lập toàn bộ toán.

**Bước tiếp theo DH_024: Duyệt dấu căn đã sửa trên HTML R1-G02.** Không mở PDF, promotion root docs, commit/push hoặc phát hành. QD_030/ngôn ngữ bảng tiếp tục có hiệu lực.

### DH_023 — lịch sử trước phản hồi dấu căn, được DH_024 tiếp quản bản HTML

**DH_023 / QD_030 — Ngôn ngữ bảng 0.4 theo chức năng trên Nhà, D0, G01 và G02.** Tiếp quản bản nguồn DH_022 của hai gói và DH_020 của Nhà/D0. Quy tắc tám loại bảng ở 07/6.1.1 thay căn trái đại trà; kit chỉ ánh xạ chức năng và hiện thực CSS/native. Giữ QD_021, QD_024, QD_025, QD_028 và ký pháp QD_029. Không sửa nội dung toán, ID, đường học, nguồn Design khóa, receipt hoặc báo cáo cũ.

**Trạng thái DH_023: đã sửa và kiểm trong phạm vi bảng, chờ chủ trì duyệt HTML.** Nguồn dựng chung và bảng ánh xạ đã nối cả bốn trang; thiếu/trùng/chưa phân loại/sai dữ liệu native chặn dựng. Bản xem/kiểm kê tại `_audit/zo_course_tables_2026-10-11/index.html`. QA cuối đạt 1442/1442: G01 34 bảng, G02 16, D0 7, Nhà 0; mọi view/disclosure đóng–mở ở 1440/430/390/320 px, từng ô văn bản/TeX/JSON, ngoài bảng/ID và guard ký pháp. Đã xem ảnh tám kiểu; 1839 tệp bảo vệ không đổi. Giữ `qa-initial.json`: phát hiện header bảng dấu D0 sai độ đậm đã sửa CSS, điều kiện QA nền nhấn/focus chỉnh theo chức năng rồi kiểm lại. Không lấy số kiểm làm kiểm toán độc lập toàn bộ toán hoặc nghiệm thu. Chưa Safari/Firefox/cảm ứng thật/screen reader; PDF/root docs/receipt/Git index và Design khóa không đổi.

**Bước tiếp theo DH_023: Duyệt các bảng trên bốn HTML mới**, sau khi QA đúng bản đạt. Chưa PDF, promotion root docs, Git hoặc phát hành. Công việc/trạng thái chỉ ở đây; các con trỏ kit/profile/Design không là roadmap khác.

### DH_022 — lịch sử trước yêu cầu bảng, được DH_023 tiếp quản

**DH_022 / QD_029 — Sửa ký pháp toán, số mục Bài học và baseline công thức.** Tiếp quản bản xem hai gói của DH_021 sau phản hồi mới: G02 thiếu số mục, phân số/đạo hàm không đúng ký pháp và MathML bị lệch hàng. Phạm vi: G01/G02, include Nền liên quan, shell chung, hai adapter và guard; không thay toán, ID, nhiệm vụ, đường học hoặc thiết kế đã duyệt. Giữ hợp đồng kiến trúc QD_021, QD_024, QD_025 và QD_028; chỉ bổ sung cổng ký pháp và số mục QD_029.

**Trạng thái DH_022: đã sửa và kiểm trong phạm vi lỗi, chờ chủ trì duyệt HTML.** Hai bản ở `_audit/zo_math_notation_2026-10-11/after/`; `qa.json` đạt 928/928 kiểm ký pháp/phép chiếu/ID/vai trò và runtime, `source-qa.json` có 13 ca kiểm guard, `governance-verified.json` đạt 124/124 và CLI QMD đạt. Guard `zo_math_notation.py` kiểm nguồn/include/số mục và chặn CSS inline MathML cũ ngay trong adapter. Bốn công thức dài chuyển ra dòng riêng để không gây tràn trên 320 px. Edge headless 1440/430/390/320 px, thêm smoke test CSS trên bản xem Nhà/D0; chưa Safari/Firefox/cảm ứng thật/trình đọc màn hình hoặc kiểm toán độc lập toàn bộ toán. Receipt lịch sử, root docs, PDF, D0 và tài sản Design khóa giữ nguyên. Bằng chứng DH_021 không chứng nhận lỗi mới này đã hết; QA cũ giữ giá trị trong đúng phạm vi cũ, không sửa lại số PASS để gọi bản mới đạt.

**Bước tiếp theo DH_022: Duyệt hai HTML sau sửa ký pháp và số mục.** Chỉ trình khi kiểm nguồn, phép chiếu toán/ID và kiểm trình duyệt của chính bản mới không còn lỗi trong phạm vi này. Chưa PDF, promotion root docs, Git hoặc phát hành.

### DH_021 — lịch sử trước phản hồi ký pháp và số mục, bản xem được DH_022 tiếp quản

**DH_021 / QD_028 — Triển khai đối sánh 48 phát hiện G01–G02.** Tiếp quản phần hai gói từ DH_020 theo báo cáo nghiên cứu mới của chủ trì; lịch sử DH_020 không chứng nhận nguồn đã sửa trong lượt này. Phạm vi là hai QMD, include Nhật kí/Nền đang dùng, binding/bộ dựng và tài liệu điều hành liên quan. Giữ toán đúng, ID/luồng, thiết kế đã duyệt và Nhật kí 14 trường; thay tối thiểu câu trùng G02 khi có bằng chứng.

**Trạng thái DH_021: chờ chủ trì duyệt HTML.** Nguồn đã sửa có mục tiêu, kiểm từ raw Quarto mới và HTML cô lập tại `_audit/zo_pair_report_2026-10-11/`. Báo cáo `README.md` giữ ma trận M01–M48, danh sách tệp và ba lớp QA. `qa.json` đạt 2.415/2.415 kiểm nguồn/DOM/runtime, `negative-review.json` đạt 13/13 ca tái tạo lỗi, `prose-review.json` đạt 231/231 phép chiếu đoạn nhiệm vụ–đáp án, `math-review.json` đạt 23/23 phép tính các đơn vị chịu sửa; không coi số phép kiểm là kiểm toán độc lập toàn bộ toán. 765 tệp được bảo vệ, chỉ tài liệu điều hành được giao thay đổi; docs/PDF/Git index/Design khóa giữ nguyên. Edge headless 320/390/430/1440 px; chưa Safari/Firefox, cảm ứng thật hay trình đọc màn hình. Không kế thừa PASS/receipt cũ, chưa nghiệm thu chủ trì hoặc phát hành.

**Bước tiếp theo DH_021: Duyệt HTML G01–G02 sau đối sánh.** Chỉ khi QA mới không còn lỗi chặn được trình đúng hai bản dựng; chủ trì đọc nội dung/vùng đọc và phản hồi. Chưa PDF/Git/promotion/phát hành hoặc khóa 0.5.

### DH_020 — lịch sử trước báo cáo đối sánh mới, hai gói được DH_021 tiếp quản

**DH_020 — Sửa danh sách lệch thiết kế/kiến trúc cả cụm, rồi xét mẫu PDF D0.** Chủ trì giao xử lí danh sách đối sánh. Phạm vi nguồn gồm G01, G02, Nhà, D0, cửa vào chuyên mục và bộ dựng/kiểm dùng chung. Áp dụng quy tắc QD_021, QD_024 và QD_025 hiện hành; không mở kiến trúc mới, không dùng G01 làm chuẩn tuyệt đối khi chính G01 còn lỗi. Đầu ra chỉ trong `_audit/zo_2027_dong_bo_cum_2026-10-11/`; giữ root docs, PDF lịch sử, receipt và Git index. Toán/ID và Nhật kí chung 14 trường được kiểm bảo toàn. Chưa chủ trì duyệt bản mới, chưa phát hành.

**Trạng thái DH_020:** đã xử lí 13 lỗi xác định và 4 điểm cần làm rõ, ghi nguồn/guard ở `_audit/zo_2027_dong_bo_cum_2026-10-11/README.md`. Kiểm cụm HTML 1093/1093, G01 tình huống/hồi quy 150/150, G02 965/965, điều hành 137/137; 1268 tệp bảo vệ không đổi. Toán/ID/Nhật kí 14 trường được kiểm bảo toàn. Không còn mục mở trong danh sách này, chưa là nghiệm thu chủ trì hoặc kiểm toán độc lập toàn bộ toán. Mẫu PDF D0 bảy trang dựng riêng sau kiểm HTML từ nguồn D0 hiện tại/tài sản 0.4, chọn bốn câu trong 24 câu, không là toàn bộ học liệu. Hồ sơ/bằng chứng tại `pdf-specimen/` trong audit.

**Bước tiếp theo DH_020: Duyệt mẫu thiết kế PDF D0.** Chủ trì xem nhịp đọc/chữ/bảng/bìa/kết; có thể phản hồi cụm HTML hiện hành. Sau duyệt mới đề xuất profile PDF chung và phạm vi D0 đầy đủ. Không đổi hợp đồng D0 HTML-only hoặc tự dựng/promote PDF production. Giữ bằng chứng DH_015–019 lịch sử; không thay receipt/hủy mọi bằng chứng chỉ vì hash đổi. Chưa Git, promotion root docs, phát hành hoặc 0.5.

### DH_019 — lịch sử, được DH_020 tiếp quản

**DH_019 / QD_025 — Đồng bộ lại G02 theo G01 hiện hành.** Chủ trì yêu cầu sửa G02, không đổi bản G01. Áp dụng QD_021, QD_024 và QD_025 đã duyệt, không mở kiến trúc mới: Cách học ba nhịp như G01; cùng lượt Khởi động giữ các nhiệm vụ nguyên tử; mục tiêu/tiên quyết và Điểm dừng theo cùng cách trình bày; tổng quan ba chặng đặt trong Luyện tập; bỏ nhãn ngoài thừa ở Ôn nền/Lời giải. G02 nối opt-in vào hook QMD chung, dùng raw mới và nguồn canonical, không dùng HTML audit làm nguồn chạy. Chỉ dựng đầu ra cô lập, không promotion vào root docs.

**Trạng thái DH_019:** HTML để xem tại `_audit/r1_g02_dong_bo_lai_g01_2026-10-11/html-current/g02-reading.html`. Bằng chứng mới: `qa-verified/qa.json`, `pair-verified/pair.json`, `protected-final.json` trong audit này; không dùng kết quả DH_016 để chứng nhận bản sửa. Giữ toán/ID, 59 cặp nhiệm vụ–đáp án, 39 mã manifest, lõi M1–M5/Chuyển giao M6 và Nhật kí chung 14 trường. G01 dựng lại byte-identical; Nhà/D0/Design khóa/root docs/PDF/Git index được bảo vệ. Giao diện mới chờ chủ trì duyệt; chưa kiểm toán độc lập toàn gói, Safari/Firefox/cảm ứng thật/trình đọc màn hình; chưa PDF/Git/phát hành.

**Bước tiếp theo: Duyệt HTML G02 sau đồng bộ lại.** Xem Bắt đầu/Cách học, Khởi động, Luyện tập, Ôn nền và Lời giải trong bản mới; không tự mở xuất bản.

### DH_018 — đã triển khai D0; công việc hiện hành được DH_019 tiếp quản

**DH_018 / QD_027 — Hoàn thành giao diện D0 sau Nhà theo kit đã duyệt.** Chủ trì giao sau DH_017. QMD opt-in/adapter nhận raw Quarto mới; map nhịp riêng D0 dùng chung shell/giấy/font/nền/Sắc xám/rail/drawer/footer. Giữ nội dung/TeX/ID/thứ tự đã duyệt, 24 câu chính, Bài 00, 25 đối chiếu, tự nguyện và HTML-only. Không ép R1, không đưa ngân hàng thử lại/hồ sơ riêng vào HTML. Header bảng thường trái; hình cuộn cục bộ; disclosure đóng mặc định, nội dung chính mở cố định.

**Trạng thái DH_018:** nguồn/adapter và kiểm hồi quy đã triển khai. HTML mới `_audit/zo_2027_d0_dong_bo_thiet_ke_2026-10-11/html-current/d0-reading.html`; báo cáo `README.md` cùng audit, QA cuối `qa-verified/qa.json`. Nội dung/receipt D0 cũ bảo toàn, giao diện mới chờ chủ trì xem riêng. Hồ sơ/manifest/config/kit/registry cập nhật. Sửa checker cũ trỏ Kế hoạch đã chuyển và ghi nhận đúng hai nhãn liên kết đã đổi ở commit a46a8051; kiểm toàn chuỗi nguồn, năm phần văn bản/TeX, ngân hàng/historical math 48/48 vẫn bắt buộc. Browser bảy độ rộng, năm view/all-open/no-JS, đề–đối chiếu–quay lại–reload–Back, nền/keyboard/drawer/resize/scroll và đích học liệu. Giới hạn/bảo toàn ở audit. Chưa chủ trì duyệt, promotion root docs, PDF nội dung, Git hoặc phát hành. Không đổi nguồn Nhà/G01/G02 hoặc tài sản Design khóa.

**Bước tiếp theo: Duyệt HTML D0 sau đồng bộ.** Xem Chuẩn bị, câu khảo sát, Đối chiếu và Chọn mạch trong bản mới. Nhà DH_017/hai gói vẫn có trạng thái duyệt riêng; không tự mở phát hành.

QD_025 tiếp tục điều hành hệ nhãn chung trong phạm vi phù hợp; lượt D0 không đổi các tên/số câu đã duyệt hoặc đường học QD_021/024 của các gói R1. Registry chọn các quy tắc ấy theo chủ đề, không coi QD_027 là bản thay thế kiến trúc học tập.

### DH_017 — đã triển khai Nhà; việc hiện hành được DH_018 tiếp quản

**DH_017 / QD_026 — Dựng lại Nhà khóa học theo ngôn ngữ thiết kế G01/G02 và đồng bộ nguồn.** Chủ trì giao sau DH_016: áp dụng ngôn ngữ thiết kế hai gói lên trang Nhà, bao gồm mã nguồn. Đã nối marker opt-in QMD vào hook hiện có, sinh lại partial từ dữ liệu canonical và tái dùng shell/giấy/token/font/rail/drawer/footer. Hệ nhãn/nhịp đọc tiếp tục theo QD_025 trong phạm vi phù hợp. Map riêng Nhà không mang controller, nhiệm vụ hoặc chặng R1. Chỉ dẫn Cách học là các nguyên tắc, mạch chính và hỗ trợ không bị biến thành chuỗi sáu bước. Danh mục D0–G01–G02 giữ ID/URL, D0 tự nguyện HTML-only; G01/G02 hiện là bản xem trước, không nâng profile nghiệm thu để vượt builder. Nguồn riêng của hai gói và D0 giữ nguyên.

**Trạng thái DH_017:** đã sửa nguồn và dựng/kiểm HTML cô lập; bản mới chờ chủ trì duyệt. HTML: `_audit/zo_2027_nha_dong_bo_thiet_ke_2026-10-11/html-current/home-reading.html`; nguồn/lệnh vận hành tại `../giao_dien/README_web_2027.md`. Báo cáo chính cùng audit: `README.md`. Kiểm projection/nguồn tươi, nhãn/owner, liên kết, footer, availability và fixture; browser 7 độ rộng, cuộn, keyboard/drawer/resize, sáu nền/Sắc xám/persistence và no-JS. Bằng chứng cuối: `current-qa/qa.json` 219/219; `pair-regression.json` 327/327 (G01 dựng mới byte-identical; G02 kiểm binding/runtime hiện hành); điều hành 121/121. Các lỗi/source/guard và giới hạn ghi riêng trong báo cáo, không xóa lần kiểm đầu. Không promotion root docs, PDF, staging/commit/push hoặc phát hành; không sửa receipt/Design khóa. Trạng thái duyệt G01/G02 vẫn riêng, không nhận là được duyệt vì làm Nhà.

**Bước tiếp theo: Duyệt HTML trang Nhà sau đồng bộ.** Xem bản Nhà mới và các liên kết tới đúng HTML G01 DH_015/G02 DH_016; phản hồi trên chính nguồn hiện hành. Chỉ khi được giao mới sửa theo phản hồi hoặc mở nhiệm vụ khác. Chưa PDF, production promotion hay phát hành.

### DH_016 — đã triển khai; Nhà được DH_017 tiếp quản về việc hiện hành

**DH_016 / QD_021, QD_024, QD_025 — Áp dụng thay đổi G01 vào nguồn G02 và dựng HTML riêng.** Chủ trì giao: “Sau khi hoàn thành trên R1-G01, hãy áp dụng những thay đổi đã làm trên R1-G01 lên R1-G02.” Đã áp dụng Cách học ba nhịp, mạch chính bốn hoạt động và nhánh hỗ trợ; rút tên/tách nhiệm vụ Khởi động, số toàn nhóm; Ôn nền cấp gốc; kết quả Kiểm tra đúng owner; Lời giải đối ứng. Binding G02 có 59 nhiệm vụ/59 đáp án, không sao chép Gợi mở/số vùng G01. Giữ 39 mã manifest, toàn bộ công thức và ID cũ, mục tiêu/lõi M1–M5 và chuyển giao M6, Nhật kí chung 14 trường.

**Trạng thái DH_016:** nguồn và phép chiếu đã áp dụng; HTML cô lập ở `_audit/r1_g02_ap_dung_he_nhan_2026-10-11/delivery-html/g02-reading.html`. Kiểm mới ở `qa-release-preview/qa.json`: nguồn/đích/câu chữ DH01–DH14, 59 cặp đề–đáp án, ID/toán cũ, fixture lỗi; Edge headless 12 view × 4 độ rộng và tuyến runtime đại diện. Hồ sơ/registry và cổng điều hành đã cập nhật, không sửa báo cáo lịch sử hoặc coi việc đổi metadata là bằng chứng sửa nguồn. GOV-G02/KT-G02-01 khép trong phạm vi các phép kiểm nêu trên; chưa nghiệm thu chủ trì hoặc kiểm toán độc lập toàn bộ nội dung toán. SVG đồ thị 0.4 dựng từ TeX canonical vào audit, không sửa tài sản Design khóa; PDF học liệu không dựng. G01/D0/root docs/PDF/Git index được kiểm bảo toàn; helper mặc định G01 có kiểm tương đương đầu ra riêng.

**Bước tiếp theo: Duyệt HTML R1-G02 sau áp dụng bản chốt.** Đọc bản G02 mới, đối chiếu vai trò/vùng đọc với HTML G01 DH_015; góp ý riêng nội dung toán nếu cần. Chưa mở PDF, promotion production, Git hoặc phát hành. Trạng thái duyệt G01 vẫn là pending riêng, không suy thành được duyệt từ chỉ thị làm G02.

### DH_015 — đã triển khai G01; trạng thái G02 được DH_016 tiếp quản

**DH_015 / QD_025 — Áp dụng bản chốt do chủ trì sửa vào nguồn R1-G01 và dựng HTML.** Đã bổ sung Gợi mở vào từ vựng/schema/guard chung trước sửa học liệu, giữ đường học QD_021 và Kiểm tra QD_024. Đã áp dụng câu chữ Cách học, tên/số/ID con và cấu trúc Ôn nền/Sửa lỗi/Lời giải vào QMD và binding canonical. Các mô tả “chưa sửa/chưa có Gợi mở/mapping_only” của DH_012–014 bên dưới là lịch sử đã được lượt này tiếp quản, không là quy tắc hay trạng thái hiện hành của G01. G02 lúc đó chưa di trú; trạng thái được DH_016 tiếp quản, không kế thừa nghiệm thu G01.

**Trạng thái DH_015:** đã dựng HTML cô lập tại `_audit/r1_g01_ap_dung_ban_chot_2026-10-10/r1_g01-render/docs/content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/index.html`; QA đạt 752/752 tại `qa-bound-current.json`, gồm 14 tình huống nguồn/đích/câu chữ và các tuyến runtime đại diện. Hệ nhãn đạt 31/31 fixture; bản kiểm kê hiện hành ở `labels-current/`. Đã sửa RD01/RD06/KT-G01-01 theo bản chốt; không dùng QA cũ để khép lỗi. Bản chốt người dùng giữ nguyên hash. Thiết kế 9/10, toán, mã nhiệm vụ, ID cũ, Nhật kí 14 trường và receipt lịch sử được bảo toàn. Không sửa HTML root/docs, PDF, nguồn riêng G02 hoặc Git index; chưa chủ trì duyệt HTML, chưa phát hành. Kiểm Edge headless 1440/430/390/320 px, bàn phím/no-JS và tương thích include chung trên G02; chưa kiểm Safari/Firefox, thiết bị cảm ứng thật, trình đọc màn hình hoặc toán độc lập toàn gói.

**Bước tiếp theo của DH_015 được DH_016 bổ sung: Duyệt HTML hai gói sau áp dụng bản chốt.** Xem Cách học, Khởi động, Ôn nền độc lập và Lời giải trong bản mới sau khi QA khép. Đây là duyệt bản thực chạy, không duyệt lại phương án; chưa mở PDF/production/G02/Git/phát hành.

### DH_012–014 — lịch sử trước áp dụng nguồn, được DH_015 tiếp quản

**DH_012 — Khép mô hình đường học và chặn quy tắc/bằng chứng cũ theo QD_021.**

Đã cập nhật chủ sở hữu 01/02/07, nhật kí quyết định, danh mục thẩm quyền, hướng dẫn/mẫu, hồ sơ/README/profile hai gói và binding kit/Design. 14 tình huống trong 01/2.2.2 phân biệt mạch chính, ôn nguồn trong/ngoài gói, đối chiếu–sửa lỗi, Nhật kí và Kiểm tra đang diễn ra/đã kết thúc. Không sửa nguồn học liệu hoặc dựng HTML/PDF. QD_022 hiệu chỉnh cơ chế: registry chọn quy tắc hiện hành theo chủ đề; chỉ kiểm lại phần bị ảnh hưởng, không khóa hiệu chỉnh hoặc hủy mọi QA vì hash thay đổi. Đường học QD_021 giữ nguyên. Bằng chứng cơ chế mới: `_audit/zo_2027_quy_tac_thay_the_QD022_2026-10-10/governance-qa.json`. Báo cáo lượt này: `_audit/zo_2027_duong_hoc_QD021_2026-10-10/governance-qa.json`.

**Trạng thái sản phẩm:** G01 bị chặn xin duyệt vì sơ đồ DH_011 sai; RD01/RD06 mở lại. G02 bị chặn cho tới khi rà nguồn theo QD_021; chưa khẳng định toàn gói phù hợp. Không xóa kết quả kiểm cũ, không dùng 465/465 hoặc FB036 để đóng các lỗi này. Thiết kế 9/10 và Nhật kí 14 trường không bị mở lại. Giao diện hiện tại chưa được sửa trong lượt điều hành.

**DH_013 — Đồng bộ hệ nhãn QD_023 và lập bảng áp dụng G01.** Hệ nhãn đã được duyệt và giao đồng bộ/lập bảng. 01/07/danh mục/schema/chuẩn QMD và guard là nguồn quy tắc hiện hành; registry, hướng dẫn/mẫu, hồ sơ/profile và kit dẫn tới chúng, không có từ điển song song. [Bảng di trú canonical](../../../hoc_lieu/r1_g01/_quy_trinh/ap_dung_he_nhan.json) và [bảng toàn nguồn](../../../../../../_audit/zo_2027_he_nhan_QD023_2026-10-10/ap_dung_he_nhan.md) giữ ID/heading, đơn vị chưa có ID, loại/chức năng, số/tên, owner, nhiệm vụ–đáp án, include, dẫn chiếu và tài nguyên. Không sửa học liệu QMD/manifest hoặc giao diện, không render/PDF/Git/phát hành. Các lỗi đường học DH_012 chưa được đóng bằng đồng bộ nhãn.

**DH_014 — Nhận bản biên tập G01 do chủ trì sửa và đồng bộ Kiểm tra QD_024 toàn chương trình.** Chủ trì giao dùng [bản đã sửa](../../../../../../_audit/r1_g01_ban_chot_bien_tap_2026-10-10.md); hash ghi tại QD_024. Hai quy tắc Kiểm tra áp dụng cho toàn bộ các gói của chương trình, không chỉ R1: chuẩn bị kĩ hoặc đủ tự tin thì có thể bắt đầu; một lượt không chia nhiều đợt. Đã thay điều kiện vào Kiểm tra cũ tại 01/2.3, cập nhật 07/02, nhật kí, danh mục, điểm vào/hướng dẫn/mẫu, hồ sơ/profile, registry và guard. Quyền bắt đầu không chứng nhận đạt mục tiêu. Không đổi Khảo sát D0 hoặc nguyên mẫu các loại gói khác.

**Trạng thái DH_014:** bản chốt biên tập được nhận, chưa áp dụng nguồn hoặc duyệt HTML. Gợi mở đã được duyệt trong bản chốt nhưng chưa vào từ điển; đồng bộ bổ sung này thuộc đầu lượt triển khai G01, không dùng nhãn Tự kiểm tra để lấp tạm. Các tên/số/ID con và owner trong bản chốt được chấp nhận làm chỉ dẫn triển khai; bảng G01 vẫn mapping_only tới khi thực sự sửa/kiểm. Lỗi `KT-G01-01`: cần áp dụng lời dẫn Kiểm tra QD_024 khi sửa Cách học/đầu Kiểm tra. Lỗi `KT-G02-01`: Khởi động G02 còn điều kiện cũ, chưa sửa; kiểm toàn gói G02 còn mở. Không sửa QMD/include/manifest/layout/controller hoặc dựng HTML/PDF trong lượt này. Thiết kế, Nhật kí 14 trường, receipt và Git index giữ nguyên. Bằng chứng guard: `_audit/zo_2027_kiem_tra_QD024_2026-10-10/governance-qa.json`.

**Bước lịch sử của DH_014, đã được thực hiện ở DH_015: Áp dụng bản chốt đã sửa vào nguồn R1-G01 và dựng HTML kiểm tra.** Trước sửa học liệu, đồng bộ Gợi mở vào danh mục/guard và cập nhật bảng di trú; áp dụng câu chữ, tên/số/ID con, owner Ôn nền/Sửa lỗi theo bản chốt và QD_024. Kiểm nguồn/nhãn/đề–đáp án/DH01–DH14 và bản HTML cô lập trước trình. Chưa mở PDF, nguồn riêng G02, production hoặc phát hành.

**Kiểm DH_014:** guard tài liệu và ca hồi quy đạt 101/101; kiểm binding bằng chứng QD_024 đạt, báo cáo QD_023 cũ bị từ chối riêng khi dùng để chứng nhận chủ đề Kiểm tra. Không hủy bằng chứng thuộc chủ đề không đổi. Đối chiếu SHA-256 497 tệp ở chuyên mục/kit và các đầu vào được chọn: 17 tệp điều hành/profile/guard thay có chủ đích, 480 tệp không đổi, không thiếu tệp; bản biên tập người dùng, QMD/include/manifest/hình/kit và Git index giữ nguyên trong tập kiểm. Bằng chứng cuối: `_audit/zo_2027_kiem_tra_QD024_2026-10-10/governance-final.json` và `bao_toan.json`. Không là kiểm nội dung/HTML hoặc nghiệm thu sản phẩm.

**Kiểm DH_013:** 28/28 fixture nhãn, guard điều hành đạt trong phạm vi tài liệu; schema/readiness hai manifest vẫn đạt (G01 42, G02 39 nhiệm vụ trong manifest), không là chứng nhận toán/đường học. Bảng có 315 dòng, 116 heading, 241 ID và 245 dẫn chiếu; Nền có 8 xác nhận, không phải 7. Kiểm SHA-256 với 607 tệp trước nhiệm vụ xác nhận QMD/include/manifest, dữ liệu hình/BBT, layout/controller, HTML/PDF, preview và Git index không đổi; không có tệp bị xóa. Báo cáo: `_audit/zo_2027_he_nhan_QD023_2026-10-10/bao_cao.md`. Lượt kiểm đầu giữ riêng với hậu tố first-run, không thay bằng chứng lịch sử.

### Góp ý lịch sử — đã triển khai theo bản chốt tại DH_015

Các ghi chú dưới đây giữ nguyên bối cảnh khi tiếp nhận; QD_025/DH_015 đã thay thế trạng thái chưa áp dụng. Không dùng chúng để quay lại tên/owner/sơ đồ cũ hoặc nhận diện một việc tiếp theo khác.

Đây là ghi chú nội bộ theo yêu cầu của chủ trì, không phải nội dung công bố hoặc xác nhận đã sửa/kiểm/nghiệm thu.

1. **Làm rõ điều kiện chuyển sang gói tiếp theo.** Tên mục “Khi nào hoàn tất lượt chính?” trong bản xem trước khó hiểu. Hướng biên tập đã đề xuất: “Khi nào có thể chuyển sang gói tiếp theo?”. Diễn đạt bằng ngôn ngữ người học: đáp ứng các mục tiêu thiết yếu bằng bài làm độc lập phù hợp, kiểm tra lại lỗi chặn sau sửa, ghi phần còn hạn chế và lịch Ôn lại; gói tiếp theo phải phù hợp tiên quyết. Phân biệt đủ điều kiện chuyển gói với hoàn thành mọi lượt Ôn lại hoặc làm chủ mọi tình huống. Chốt câu chữ sau khi nhận đủ góp ý; chưa thay tên/nội dung trong preview hoặc QMD.
2. **Tách Ôn nền thành khu vực hỗ trợ độc lập của gói.** Ôn nền ngang cấp chức năng với Sửa lỗi, Nhật kí và Lời giải; không thuộc Bài học hoặc Câu hỏi khởi động và không trở thành chặng tuyến tính bắt buộc. Khởi động và các hoạt động khác chỉ dẫn tới Ôn nền khi cần, rồi quay về đúng nơi gọi; đang Kiểm tra phải tự lực. Hiện trạng đã xác minh: `hoc_lieu/r1_g01/index.qmd` đặt `#on-nen` ở heading cấp 4 dưới Khởi động; `_design/web_2027_mau_dung_chung/r1-controller.js` lấy `bai-hoc` làm phần chứa view Ôn nền. Có menu riêng chưa bảo đảm độc lập trong cấu trúc nguồn. Lượt sửa sau phải thống nhất nguồn, mục lục, binding và điều hướng; giữ nội dung toán, ID, liên kết sâu, đường quay về và các include Nền chung. Không sao chép nguồn Nền dùng chung thành bản sửa riêng. Phạm vi ghi chú triển khai trước mắt là R1-G01; chưa tự mở sửa R1-G02 hoặc tài liệu quy chuẩn.

3. **Chuẩn hóa nhãn, tiêu đề và số nhiệm vụ.** Quy tắc chung đã duyệt và đồng bộ QD_023; tên/số/anchor cụ thể và câu chữ G01 chờ chốt tại DH_013. Luyện tập một dãy xuyên chặng; đề xuất đánh lại số bị thay. Đồng bộ quy chuẩn không phải đã sửa nguồn.

Khi được giao sửa nguồn, đối chiếu các lời dẫn/đích hỗ trợ với 14 tình huống theo QD_021 trước khi dựng HTML cô lập; kiểm quan hệ và câu chữ người học rồi mới trình. Việc ghi nhận các ý này không đóng RD01/RD06, không thay thiết kế 9/10 hoặc Nhật kí 14 trường, không cấp quyền PDF/Git/phát hành.

### DH_011 — lịch sử biên tập, phần sơ đồ bị bác bỏ bởi QD_021

**DH_011 — Biên tập nguồn R1-G01 và kiểm HTML theo phương án đã duyệt.**

Chủ trì xác nhận: “Mình duyệt phương án biên tập R1-G01. Hãy thực hiện.” Căn cứ QD_020 và [phương án](../../../../../../_audit/r1_g01_phuong_an_bien_tap_thong_nhat_2026-10-10.md). Đã biên tập QMD, manifest, binding; cập nhật ví dụ Nhật kí dùng chung đúng 14 trường và giải thích hẹp N-LT. Giữ Bài học/Luyện tập không xen kẽ; ba chặng thuộc Luyện tập; 45 phút/20 điểm và điều kiện độc lập thuộc Kiểm tra. Đã dựng một HTML G01 cô lập từ canonical; không promotion vào docs.

Trạng thái DH_011: **lịch sử biên tập; chủ trì bác bỏ sơ đồ. Xin duyệt đường học bị thu hồi tại DH_012; 465/465 không chứng nhận quan hệ này**. Bằng chứng: `_audit/r1_g01_bien_tap_2026-10-10/qa/editorial-qa.json`. Theo dõi RD01–RD21 tại hồ sơ G01. Guard mới `scripts/zo_r1_g01_editorial_check.py` kiểm nội dung/quan hệ và ca lỗi cố ý; checker FB033/FB036 giữ làm lịch sử, không dùng số PASS cũ để chứng nhận bản mới. Không sửa CSS/controller, toán đề/đáp án/hình/BBT, G02 riêng, chuẩn 01/07, receipt hoặc PDF. Chưa stage/commit/push/phát hành.

**Bước tiếp theo lịch sử của DH_011, đã bị DH_012 thay thế: Duyệt HTML R1-G01 sau biên tập.** Chỉ trình duyệt bản HTML mới sau khi QA kết thúc. Chủ trì xem Cách học, đầu Luyện tập/Kiểm tra, checkpoint, đọc kết quả, tuyến sửa và Nhật kí. Duyệt phương án không phải duyệt thành phẩm. PDF và đối sánh biên tập G02 là các nhiệm vụ riêng sau đó, chưa tự mở.

### DH_010 — Lập phương án đã kết thúc

Đã lập phương án/câu chữ cho đủ 21 RD và kiểm bảo toàn, chưa sửa nguồn tại thời điểm lập. Chủ trì đã duyệt và giao triển khai qua DH_011. Báo cáo DH_010 giữ nguyên như lịch sử: `_audit/r1_g01_phuong_an_bien_tap_2026-10-10_qa.json`; câu “chờ duyệt/chưa sửa” trong phương án mô tả lúc lập, không thay trạng thái DH_011.

### DH_009 — Đồng bộ bộ điều hành đã kết thúc

**DH_009 — Hợp nhất và đồng bộ toàn bộ các lớp điều hành khóa 2027.**

Chủ trì giao ngày 10/10/2026: đồng bộ tất cả tài liệu điều hành trước khi biên tập tiếp gói. Căn cứ QD_019. Danh mục/ranh giới/chủ sở hữu tại [08](08_danh_muc_tham_quyen_dieu_hanh.md); gồm tài liệu khóa, hồ sơ/mẫu, vận hành D0/G01/G02, trạng thái máy đọc, kit, binding Design và chuyển tiếp dự án cũ. Không chỉnh nội dung học liệu hoặc giao diện, không dựng HTML/PDF, stage/commit/push/phát hành; không mở M8.R/Video hoặc khóa 0.5.

Trạng thái DH_009: **đã thực hiện đồng bộ tài liệu và kiểm phạm vi/bảo toàn**. Kết quả và phép kiểm của lượt này: `_audit/zo_2027_dong_bo_toan_bo_dieu_hanh_2026-10-10.md`. Hoàn thành đồng bộ tài liệu không phải nghiệm thu sản phẩm. Những khác biệt giữa quy tắc và nguồn chưa sửa được giữ là backlog có ID, không sửa metadata để biến thành đạt. Không có nhiệm vụ biên tập học liệu đang được tự thực hiện.

Rà G01 đã hoàn thành ở mức kiểm kê nguồn/DOM theo báo cáo `_audit/r1_g01_ra_noi_dung_va_duong_hoc_2026-10-10.md`: 21 phát hiện RD01–RD21; chưa biên tập QMD, chưa duyệt câu chữ/sơ đồ thay thế, chưa kiểm toàn bộ toán/đồ thị hoặc runtime mới. N07 không còn trạng thái “chưa rà”. G02 chưa được rà toàn bộ ở mức nội dung/đường học tương đương; kết quả FB036 chỉ có phạm vi đã ghi.

**Bước kế tiếp của DH_009 đã hoàn tất tại DH_010:** phương án đã được duyệt; triển khai và trạng thái hiện hành thuộc DH_011. Các mô tả chưa sửa trong DH_009 là lịch sử của lượt đồng bộ tài liệu.

### DH_008 — Lượt hợp nhất trước, đã kết thúc; không phải việc tiếp theo

**DH_008 — Hợp nhất bộ tài liệu điều hành khóa 2027 theo quyết định hiện hành.**

Chủ trì giao thực hiện bước của báo cáo khôi phục ngày 10/10/2026. Phạm vi chỉ tài liệu/hướng dẫn và trạng thái liên quan; không sửa QMD/toán, CSS/JS, schema/checker, manifest/cấu hình, đầu ra hoặc receipt. Căn cứ: QD_016–018; ma trận D01–35/N01–08 tại `_audit/zo_2027_quyet_dinh_hien_hanh_2026-10-10.md`.

Kết quả: đã hợp nhất kiến trúc không xen kẽ Bài học/Luyện tập; Nhật kí một nguồn đủ 14 trường; vùng đọc theo nhịp, rail/drawer và các tinh chỉnh FB027–036; làm rõ mốc duyệt/lịch sử và nguồn canonical. Bằng chứng kiểm tài liệu/bảo toàn tại `_audit/zo_2027_hop_nhat_dieu_hanh_2026-10-10.md`. Đây là hoàn thành nhiệm vụ tài liệu, không là nghiệm thu mới của học liệu.

**Trạng thái hai gói:** G01 thiết kế 9/10/HTML FB033 đã duyệt giữ làm lịch sử; HTML cục bộ G01 và HTML audit G02 FB036 chờ xem. Sau resume FB036, chủ trì mở góp ý nội dung G01, chưa chốt câu chữ/sơ đồ thay thế. Các phản hồi N01–07 nằm ở hồ sơ G01. PDF chưa đồng bộ; chưa phát hành/khóa 0.5.

**Bước kế tiếp của DH_008 đã được thực hiện:** rà nội dung/đường học G01, ghi 21 phát hiện tại báo cáo 10/10. Không còn là nhiệm vụ chờ giao. Việc hiện hành và đề xuất tiếp theo thuộc DH_009 phía trên.

### Lịch sử DH_007 / FB035 — không phải việc hiện hành

FB034 bị chủ trì chỉ ra còn lệch nhiều nội dung từ trang đầu, cấp/vùng đọc
và bảng. Không dùng 985/985 ca layout để nói đã đồng bộ kiến trúc.
FB035 sửa QMD và profile vai trò canonical G02, gom định hướng đúng cấp,
khởi động/Ôn nền h4, tách phương pháp/đề tự kiểm và reuse nguyên Nhật kí G01
bằng include chung. HTML hiện hành `_audit/zo_g02_consistency_2026-10-08/g02-reading.html`.
Semantic 144/144, layout/hành vi 985/985, toán bổ sung 28/28; G01 398/398 và
990 tệp bảo vệ nguyên trạng. Bằng chứng/ma trận/lỗi ở audit mới; chưa chủ trì duyệt.
G01/Nhà/D0, PDF, Git/phát hành và Design 0.5 vẫn ngoài phạm vi.

### DH_007 / FB034 — lần dựng trước phản hồi, lưu lịch sử

Chủ trì giao ngày 08/10/2026: hoàn thiện G02 từ nội dung trong repo, theo
kiến trúc 2027 và bộ khung G01 hiện hành. Tái dùng bài tập/lời giải đã có;
bổ sung chặng, điểm kiểm soát, Nền, Nhật kí 14 trường, ba lượt Ôn lại riêng
và nhánh chuyển giao có điều kiện. QMD là nguồn; HTML mới dựng cô lập để xem.
Không sửa G01/Nhà/D0, không dựng PDF, stage/commit/push hoặc phát hành.
Ma trận đối sánh FB029 là danh sách khoảng trống lịch sử, không phải chứng nhận
đồng bộ hiện tại. Chưa gọi G02 hoàn thiện hoặc đã nghiệm thu chỉ từ `planned=0`.

Đã triển khai nguồn thực: ba chặng, tám CP, chín đơn vị Nền, hai hình xác nhận
mới, Nhật kí đúng 14 trường, ba đề/lời giải Ôn lại riêng và nhánh chuyển giao.
HTML: `_audit/zo_g02_completion_2026-10-08/g02-reading.html`; nguồn và bằng
chứng: README, completion-qa, math-check, protected-result cùng thư mục.
G01 đã kiểm lại 398/398; 990 tệp bảo vệ không đổi. Các chỉ số là kiểm kỹ thuật,
không thay chủ trì duyệt nội dung và đường học. PDF vẫn là bản cũ, chưa đồng bộ.

Việc kế tiếp: chủ trì xem HTML G02; xử lí nhận xét trên chính nguồn hiện hành.
Sau khi duyệt, mới chốt receipt/guard G02 và nối đường dựng HTML production.
PDF, Git/phát hành, D0 và khóa 0.5 vẫn là các nhiệm vụ riêng chưa được mở.

### DH_006 — Lịch sử chốt G01; việc kiểm và ghi nhận đã xong

**DH_006 — Chốt HTML G01 và kiểm đường dựng canonical; không mở lại thiết kế.**

Ngày 08/10/2026 chủ trì duyệt FB032 “Mình đã xem kết quả, tốt.” và giao bốn việc:
ghi nhận duyệt; cập nhật hợp đồng dùng lại; chuyển guard vào scripts; dựng kiểm từ nguồn.
Receipt của mốc lịch sử FB033 ở `hoc_lieu/r1_g01/giao_dien/web_2027_accepted.json`, SHA HTML
`8b3a9a1ad532e72951edb415d9ab32a37990a80e13c2d754a2f57028fedc764a`.
Nguồn và cách kiểm ở hồ sơ G01; báo cáo `_audit/zo_g01_html_checkpoint_2026-10-08/README.md`.
DH_005 đóng trạng thái chờ chủ trì xem. Không quay về mốc g01-kit cũ.
Lượt cuối 398/398; dựng độc lập từ nguồn cho HTML/runtime byte-identical,
325 tệp bảo vệ và Git index nguyên trạng. Không ghi đè HTML root sau kiểm.

Việc kế tiếp đề xuất, **chưa thực hiện**: hoàn thiện nguồn/kiến trúc G02 theo chuẩn
2027 và ma trận đối sánh, giữ toán riêng; rồi áp dụng cùng bộ khung và kiểm liên gói.
Không sao chép 154 vùng/12 view hoặc bài toán G01 để giả đồng bộ. Nhà/D0 giữ nguyên;
PDF còn chưa đồng bộ, chưa commit/push/phát hành hoặc khóa Design 0.5.

### DH_005 — Lịch sử hình/bảng và tải PDF; đã được chủ trì duyệt, đóng bởi DH_006

Chủ trì duyệt kế hoạch ngày 08/10/2026: ảnh toán trên bìa trong suốt, ba dạng
khung × hai kích thước và sáu nền sáng/tối Đỏ/Vàng/Xám ZO; đồ thị opt-in 0.4,
bảng native từ JSON và vùng chèn hình tự nhiên trong vùng đọc. Mẫu xem tại
`_audit/zo_math_figure_profile_2026-10-08/index.html`; nguồn dùng lại ở
`_design/web_2027_mau_dung_chung/figure-profile-candidate/README.md`.

Giữ nguyên nguồn toán/ID/luồng, khung giao diện G01 và mốc `g01-kit.html`.
Các lỗi phát hiện/sửa trong mẫu có guard và bằng chứng ở WEB04-FB-030. Không
coi mẫu này là toàn bộ G01/G02 hoặc Design 0.5 đã hoàn thành. Việc duy nhất
tiếp theo đã được giao: tích hợp payload hình/bảng vào nguồn dựng G01,
kiểm toàn trang rồi bàn giao HTML cho chủ trì xem. Mẫu FB030 đã duyệt;
không suy nghiệm thu mẫu thành nghiệm thu HTML tích hợp mới. G02 vẫn
chưa hoàn thiện kiến trúc; không dựng PDF học liệu, commit/push/phát hành.

Kết quả thực hiện FB031: nguồn dựng và HTML cục bộ đã tích hợp, đạt 782/782
kiểm tra tại 1440/430/390/320px. Rà thị giác và sửa nhãn đồ thị 05/09/10 từ
nguồn; lưu guard, ảnh và hash tại `_audit/zo_g01_figure_integration_2026-10-08/`.
Đầu ra xem: `docs/content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/index.html`.
Đã kiểm 679/679 tệp bảo vệ còn lại không đổi và 45/45 tài sản runtime khớp
bản QA sau promotion. Việc tiếp theo là chủ trì xem HTML tích hợp này;
không tiếp tục các nhánh khác trước khi có yêu cầu.

**Cập nhật FB032:** chủ trì đã xem bản tích hợp và nhận xét mọi phần ổn,
chỉ giao tinh chỉnh Tải PDF và nút drawer. Đã thống nhất tám thẻ ba cột,
co bố cục mobile, đếm trang từ tệp thật, giữ URL/tên/mô tả và bỏ chữ nút
drawer nhưng giữ truy cập/bàn phím. Nguồn và HTML cục bộ đạt 164/164 kiểm;
ảnh/báo cáo tại `_audit/zo_g01_downloads_2026-10-08/README.md`.
Các PDF chưa đồng bộ với HTML mới và mục tải đã thông báo đúng. Việc tiếp
theo là xem riêng hai tinh chỉnh mới; không mở lại phần hình/bảng đã ổn,
chưa chuyển G02, dựng PDF, commit/push/phát hành hoặc khóa 0.5.

### DH_004 — Đồng bộ nguồn HTML R1-G01 theo mốc đã chốt: đã dựng và tự kiểm

Ngày 08/10/2026, chủ trì giao đưa bản mới nhất `g01-kit.html` vào đường dựng
production trước khi giải quyết các gói khác. Đã nối QMD vào bản đồ 154 vùng đọc,
bộ khung dùng chung và SVG trình bày đã duyệt; render qua mirror/index riêng,
đối chiếu đúng mốc SHA `5c97396dd9656971e442cb60a07aa799935d3233bf2ae15a53ebc57f76c77e3c`.
267 kiểm tra HTML/nội dung/runtime và 23 guard đạt. QMD chỉ thêm marker HTML,
không đổi thân bài; Nhật kí đủ 14 trường, Ôn lại và Nhật kí tách view.
Readiness G01 đạt `planned=0`.

Đầu ra cục bộ: `docs/content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/index.html`.
Hồ sơ: `_audit/zo_g01_source_sync_2026-10-08/README.md`; nguồn và cách dựng tại
`hoc_lieu/r1_g01/_quy_trinh/README.md`. Build thường không dùng audit hoặc HTML
cũ làm nguồn. Bản đối chứng giữ nguyên và được sao lưu đã kiểm hash.
G02/D0/Nhà khóa giữ nguyên; không dựng PDF, staging, commit, push hoặc phát hành.
Tám PDF vẫn là phần chưa đồng bộ; không dùng PASS HTML để gọi cả gói đã xuất bản.

Việc tiếp theo được đề xuất là hoàn thiện nguồn/kiến trúc G02 theo G01 và ma trận
đã lập, giữ bản chất toán riêng; chỉ mở khi chủ trì giao. Không quay lại chọn
hướng thiết kế hoặc lấy HTML cũ thay mốc hiện hành.

### DH_003 — hồ sơ bước trước, không còn là nguồn mô tả trạng thái G01

Ma trận current: `_audit/zo_web_2027_g01_g02_doi_sanh_2026-10-08/ma_tran_doi_sanh.md`, 46 tiêu chí và đủ 28 phản hồi cũ. Hai HTML đối sánh mới ở `index.html` cùng thư mục; sửa nhãn chức năng, câu dừng, header rỗng, giới thiệu lặp, danh sách tải và footer G01 riêng bản mới. Không đổi các mốc đã duyệt. Hợp đồng/nguồn lỗi/guard ở `_design/web_2027_mau_dung_chung/doi_sanh_lien_goi.md`. Kiểm local FB028 không chứng minh đồng bộ kiến trúc: Nền, Nhật kí 14 trường, CP, từng lượt Ôn lại và nhánh chuyển giao G02 vẫn thiếu/chưa hoàn tất.

- Căn cứ: QD_010 và nhiệm vụ prototype YC17; FB-024 ngày 08/10/2026 chủ trì duyệt thiết kế G01 9/10, 1 điểm còn lại dành cho tương lai. Chủ trì đã giao thực hiện bộ khung dùng chung và HTML Nhà khóa; không mở lại vòng chọn hướng.
- Mốc G01 đã duyệt: `_design/ngon_ngu_thiet_ke_zo_math_0_4/09_nhat_ki/moc_thiet_ke_web_2027_da_duyet_2026-10-08.md`. Bản `_audit/zo_design_web_2027_discovery_2026-10-07/g01-reading.html` giữ nguyên; B2/B3/B4 không đạt vẫn là lịch sử, không phải mẫu hiện hành.
- Nguồn bộ khung: `_design/web_2027_mau_dung_chung/README.md`, hợp đồng vùng đọc và hướng dẫn kiểm trong cùng thư mục. Hai script `scripts/zo_web_2027_preview.py`, `scripts/zo_web_2027_check.py` dựng/kiểm riêng preview; không dùng audit làm nguồn production lâu dài.
- Điểm xem mới: `_audit/zo_web_2027_g01_g02_doi_sanh_2026-10-08/index.html`. Bản FB028 G02 và hai HTML Nhà/G01 FB027 giữ nguyên làm đối chứng. Không lấy 154 vùng G01 làm khuôn G02. Hai lớp QA: bảo toàn/hình học từng trang và đối sánh cùng vai trò liên gói; thiếu kiến trúc được ghi OPEN riêng.
- Nhà khóa có chín nhịp đọc theo nội dung riêng, section ủng hộ riêng, mục lục theo vai trò Nhà; giữ dữ liệu/ID/thứ tự và ba gói D0–G01–G02. Không sao chép 12 view hoặc bản đồ 154 vùng G01 sang Nhà.
- Trạng thái duyệt: G01 đã duyệt 9/10; Nhà và footer đã duyệt; ngày 08/10/2026 chủ trì **chốt hai tinh chỉnh FB027** và giao HTML G02. Chỉ HTML G02 mới chờ xem. PASS không thay duyệt thị giác hoặc nghiệm thu toán/đường học; không hạ trạng thái đã duyệt.
- Sổ công việc/phản hồi canonical: `_design/ngon_ngu_thiet_ke_zo_math_0_4/09_nhat_ki/`, FB028; ghi việc chốt FB027 và lỗi/guard G02. Nguồn/đầu ra production và tài sản 0.4 khóa giữ nguyên. Không dựng/cập nhật PDF; các link PDF cũ chỉ được bảo toàn, không chứng nhận PDF hiện hành.
- G02 giữ view Cách học mặc định, 11 bài luyện theo thứ tự nguồn, 5 bài kiểm tra, sửa và ôn hiện có. Nguồn không có `on-nen`, `nhat-ky` hoặc các CP độc lập như G01; không tạo thẻ rỗng hoặc nội dung giả để đủ 12 view. Đây là giới hạn nguồn ghi rõ, không phải xác nhận G02 đã đạt toàn bộ kiến trúc đích 2027.
- Phạm vi chưa mở: D0, QMD/CSS/JS production, render HTML/PDF production, commit/push/phát hành và khóa toàn bộ 0.5.
- Việc tiếp theo: chốt phạm vi nhiệm vụ chuyển kiến trúc G02 ở nguồn theo ma trận; không tiếp tục vá CSS để thay Nền/Nhật kí/CP chưa tồn tại. Chưa có quyền đổi QMD/ID/toán/luồng trong lượt prototype; không mở production/PDF/phát hành hoặc vòng thiết kế mới.

### Baseline chức năng DH_002 đã đóng để chuyển sang thử nghiệm 0.4

- Phạm vi và kết quả chi tiết giữ tại [hồ sơ G01](goi/R1_G01.md), `_audit/r1_g01_doi_chieu_2026-10-06.md` và các báo cáo vòng giao diện ngày 07/10/2026; không sao chép toàn bộ lịch sử vào bảng điều hành.
- Baseline đã khóa các bất biến: ba chặng, ba tầng sửa, ba bài Ôn lại, tuyến S-K đúng họ lỗi, Nhật kí 14 trường; 42 nhiệm vụ quản lí, câu xác nhận con `G01-L08-XN01`, bảy nguồn N canonical và nhánh Phối hợp O02 được đếm tách loại.
- Các lỗi điều hướng đã xử lí và có hàng rào hồi quy: ba nhóm vai trò; Ôn lại ngay sau Kiểm tra; navbar sticky không biến mất hoặc giật; Ôn lại và Nhật kí là hai view riêng. Bằng chứng gồm kiểm 1440/430/390, bàn phím, no-JS và trace cuộn G01/G02.
- Điểm chuyển tiếp: baseline chức năng được giữ nguyên trong pilot 0.4. Chưa thử với người học, chưa đồng bộ tám PDF/metadata số trang, chưa commit, push hoặc phát hành.

Khi chuyển bước, thay nội dung hiện hành ở mục này; lịch sử quyết định quan trọng chuyển sang nhật kí, không chồng nhiều “việc đang mở”. Chỉ mở một việc sản xuất chính; có thể chuẩn bị nguồn cho việc tiếp theo theo Kế hoạch 0.6.

## B. Trạng thái toàn chương trình tại lúc bàn giao

| Hạng mục | Trạng thái có căn cứ | Còn phải xác minh | Hồ sơ |
|---|---|---|---|
| Chuẩn kiến trúc | QD_033 thay phần mâu thuẫn của QD_021; QD_024/025 và QD_028–032 giữ phần còn hiệu lực; DH_029 đã được chủ trì duyệt, DH_030 bảo toàn; QD_034/DH_031 chỉ xử lí lưu trữ | Nguồn/bản xem G01/G02 chưa đối chiếu lại với QD_033; PASS tài liệu/lưu trữ không chứng nhận nội dung/toán/HTML | 01, 02, 04, 07, 08, registry, chuẩn QMD và chỉ mục lưu trữ |
| D0 và Nhà | DH_027 đã kiểm điều hướng bốn trang; Nhà DH_028 đã áp dụng câu chữ chủ trì duyệt, kiểm 18/18 và QA 258/258; HTML mới vẫn chờ xem | Không lấy receipt lịch sử nghiệm thu bản mới; không kiểm lại trang/live trong DH_029; D0 giữ hợp đồng khảo sát riêng | Hồ sơ riêng; DH_027/028 và audit tương ứng |
| R1-G01 và R1-G02 | DH_026 đã kiểm backlog/DOM/hình trong phạm vi giao, DH_027 đã kiểm điều hướng; không còn ghi “đang kiểm DH_021”. QMD/HTML chưa được đối chiếu lại với QD_033; chưa xác định có nội dung nào cần sửa | Không dùng QA QD_021 chứng nhận QD_033; nếu phép đối chiếu tạo bản mới thì chờ chủ trì duyệt đúng bản; PDF stale, chưa xuất bản, chưa thử người học thật | Hồ sơ hai gói, DH_026/027, registry `learning_route`; báo cáo cũ giữ lịch sử |
| R1 còn thiếu; R2–R8 | Có định hướng trong Kế hoạch | Chưa lập đầy đủ danh mục gói/công sức | Lộ trình tham chiếu dưới đây |

## C. Danh sách làm sau

| Việc | Khi mở | Điều kiện |
|---|---|---|
| Đồng bộ PDF hai gói | Sau duyệt HTML và yêu cầu riêng | Dựng từ cùng nguồn, kiểm toán/nhịp đọc/provenance; không dùng tệp PDF cũ |
| Tiếp tục mẫu PDF D0 | Khi chủ trì quay lại nhiệm vụ này | Giữ D0 HTML-only cho đến quyết định riêng; mẫu DH_020 không là production |
| Tổng kết mẫu web thành đề xuất 0.5 | Sau duyệt đúng các HTML mẫu | Token/component/guard/backlog có nguồn, không chỉ đổi số phiên bản |
| Chọn gói tiếp và lịch sản xuất | Khi hai gói mẫu có bằng chứng và quỹ giờ | Không dùng lịch học làm lịch sản xuất |

## D. Cách cập nhật bảng này

Cuối phiên, ghi việc vừa đạt bằng chứng, điểm còn chặn, việc duy nhất tiếp theo. Khi đổi thứ tự hoặc phạm vi chương trình, ghi một quyết định ở tệp 04. Không sao chép toàn bộ báo cáo kiểm vào đây. Phiên bản nội dung tài liệu khác với trạng thái sản phẩm; cập nhật ngày sửa chỉ khi nội dung thực sự đổi.

## Lộ trình tham chiếu

## 6.1. Hai đường tiến độ cần quản lý khác nhau

Tiến độ học của học sinh và tiến độ sản xuất của ZO Math có liên hệ nhưng không cùng một lịch. Lịch 36 tuần, 6 giờ mỗi tuần trong Kế hoạch 0.6 là mô hình học tham chiếu; nó không cho biết người chủ trì có thể làm bao nhiêu gói mỗi tháng.

Tại ngày 06/10/2026, không nên tự gán một ngày hoàn tất toàn chương trình bằng cách đếm số gói còn lại. Cần đo công sức R1-G01 và R1-G02 sau khi tách chi phí xây hệ thống ban đầu, rồi dùng quỹ giờ sản xuất thực tế. Ngày thi 2027 và cấu hình thi phải lấy từ công bố áp dụng khi lập lịch; ngày giả định trong ví dụ Kế hoạch 0.6 không trở thành lịch chính thức.

## 6.2. Lộ trình sản xuất có điểm kết thúc

| Chặng sản xuất | Công việc chính | Khi nào được chuyển tiếp |
|---|---|---|
| 1. Đóng gói mẫu R1-G01 | Hoàn thiện nội dung và đường học ở hồ sơ `goi/R1_G01.md` và quy trình nghiệm thu; HTML rồi PDF và phát hành | Một bản nhất quán đã được chấp nhận, có giới hạn và lịch sử rõ |
| 2. Kiểm tra khả năng dùng lại trên R1-G02 | Áp dụng cùng hợp đồng, giữ nội dung riêng; rà các nhánh chuyển giao và thẻ nền cần thêm | Không phải phát minh lại điều hướng, cách chấm, vòng sửa hoặc nhật kí |
| 3. Hoàn thiện lõi R1 còn thiếu | Xác định phạm vi tiệm cận, khảo sát và các ứng dụng cần cho R1; chia gói theo mục tiêu và công sức | Sổ yêu cầu R1 có học liệu và nhiệm vụ tương ứng; phần còn thiếu được ghi cụ thể |
| 4. Mở rộng sang các mạch khác | Theo thứ tự nhu cầu ở bảng dưới; dùng lại kiến trúc, thay nội dung và tham số | Đủ cơ hội học, kiểm tra và ôn lại trên toàn phạm vi chung cần thiết |
| 5. Hoàn thiện phối hợp | Các cụm không báo sẵn phương pháp; đề giữa lộ trình và đề chuyển chặng | Có ma trận phủ các mạch, lời giải và câu mới sau sửa |
| 6. Luyện đề và củng cố cuối | Bộ đề, phân tích thời gian, sửa lỗi và phiếu ôn cuối theo cấu hình áp dụng | Thành phẩm và hướng dẫn sử dụng đủ; không bỏ thời gian chữa để tăng số đề |
| 7. Khép ấn bản | Rà phạm vi, lỗi còn tồn, bản phát hành và dữ liệu sử dụng; tổng kết sau thi | Kho 2027 truy nguyên được và danh sách chuyển sang năm sau có lý do |

Đóng chuẩn dùng chung sau hai gói mẫu nghĩa là khóa **hợp đồng** ở `01_kien_truc_hoc_tap.md` và `02_quy_trinh_va_nghiem_thu.md`, không khóa mọi con số hay mọi bài. R1-G02 là phép thử đầu tiên về khả năng dùng lại, chưa chứng minh bao quát mọi dạng toán. Gói đầu tiên của một mạch có đặc trưng khác, như hình học hoặc thống kê, được phép điều chỉnh cách biểu diễn và cách chia chặng; chỉ mở lại hạt nhân khi có mâu thuẫn vận hành thật.

Không tự cấp toàn bộ mã R1-G03 trở đi trong bản này: Kế hoạch 0.6 chưa ấn định đầy đủ số gói cho từng mạch. Chia gói quá sớm theo số trang sẽ tái tạo vấn đề R1-G01. Việc kế tiếp sau hai mẫu là khóa phạm vi gói R1 còn thiếu đầu tiên từ ma trận chương trình và dữ liệu công sức đã có.

## 6.3. Bản đồ toàn chương trình để không bỏ sót mạch

Thứ tự dưới đây kế thừa Mục 4.5, 4.6, 12.2 và 12.7 của Kế hoạch 0.6. Đây là thứ tự chuẩn bị ưu tiên, không là lịch cứng cho mọi học sinh.

| Thứ tự | Phạm vi học liệu cần sẵn sàng | Điều phải giữ khi sản xuất |
|---|---|---|
| Hiện tại | D0; R1-G01; R1-G02 | D0 định vị tự nguyện; hoàn thiện hai gói mẫu trước khi nhân rộng |
| Tiếp theo | R1 còn thiếu: tiệm cận, khảo sát, ứng dụng phù hợp | Không trộn mọi ý vào gói đơn điệu; giữ ranh giới với R8 |
| Sau lõi R1 | R2 thống kê và đọc dữ liệu; R3 hình học, vectơ và cầu nối tọa độ | Đơn vị, ý nghĩa dữ liệu, cách chọn biểu diễn, hình đúng và có căn cứ |
| Tiếp nối | R4 đếm và biến cố; R5 dãy số, mũ–lôgarit; R6 lượng giác | Điều kiện, đối tượng đếm, số kì nguyên, họ nghiệm và đơn vị góc |
| Theo tiên quyết lớp 12 | R7 nguyên hàm và tích phân; R3 tọa độ không gian; R4 xác suất có điều kiện | Cận và dấu, biểu diễn không gian, mẫu số xác suất và chiều điều kiện |
| Xuyên suốt rồi tăng trọng tâm | R8 mô hình hóa, tối ưu và phối hợp | Biến, ràng buộc, chọn công cụ, kiểm tra kết quả theo bối cảnh |
| Cuối lộ trình | Cụm trộn, đề giữa lộ trình, đề chuyển chặng, đề mô phỏng và ôn cuối | Bài chưa lộ, thời gian thực, phân tích lỗi, thử lại và duy trì |

Nền N được bổ sung theo nhu cầu của các gói, không cần hoàn thành toàn kho trước khi sản xuất tiếp. R8 không phải việc để dành hoàn toàn tới cuối. Không bỏ một mạch chỉ vì nó ít xuất hiện trong vài đề đã đọc.

Lịch học tham chiếu 36 tuần vẫn giữ các mốc: tuần 1 định vị; tuần 2–18 ôn trọng tâm; tuần 19–28 phối hợp và lấp khoảng trống; tuần 29–34 luyện đề có chữa; hai tuần cuối củng cố. Khi người học gia nhập muộn hoặc chưa học một phần ở trường, áp dụng Mục 12.10–12.11 của Kế hoạch 0.6 để tính lại quỹ giờ và thứ tự. Không ép hoàn thành nguyên lịch bằng cách học dồn.

## 6.4. Quy trình sản xuất lặp lại cho mỗi gói

| Bước | Đầu ra phải lưu | Điều kiện kết thúc |
|---|---|---|
| 1. Chọn phạm vi | Phiếu mục tiêu, tiên quyết, phần loại trừ và nguồn | Một gói có thể học và đánh giá rõ; không chỉ có tên chuyên đề |
| 2. Lập ma trận | Mục tiêu–hoạt động–bằng chứng–lỗi–ôn lại | Không có mục tiêu thiết yếu chỉ được giảng mà không được kiểm tra |
| 3. Nghiên cứu và tự giải | Lập luận, lời giải và các điểm còn phải xác minh | Giải quyết chỗ ảnh hưởng tính đúng đắn trước khi tạo bản xuất |
| 4. Viết lõi và đường học | Bài học, luyện, kiểm tra, sửa, ôn, nền cần thiết | Tất cả đường bắt buộc có đích thật; bài xác nhận không lẫn với bài đã lộ |
| 5. Kiểm nội dung và sử dụng | Bảng lỗi, kết quả rà toán, các đường học thử | Không còn lỗi chặn; phạm vi đúng; khối lượng học có thể phân buổi |
| 6. Tạo bản xuất và nghiệm thu | HTML, PDF cần thiết, phiên bản, hướng dẫn | Cùng nội dung và quyết định học ở các định dạng |
| 7. Phát hành và theo dõi | Bản công khai, lịch sử sửa, phản hồi và giờ thực | Người dùng mở đúng bản; lỗi được phân loại; có một việc sản xuất kế tiếp |

Không bắt mỗi gói phải có video, podcast, slide, sách hay bộ ảnh mạng xã hội. Chỉ làm tài nguyên phụ khi nó giải quyết một nhu cầu học hoặc truyền thông cụ thể và không lấy mất giờ kiểm định lõi. Cửa vào dành cho giáo viên được giữ như giả thuyết “một lõi, hai cửa vào”; không mở thành một dây chuyền sản xuất riêng trong lúc chương trình học sinh còn thiếu.

## 6.6. Cách lập lịch khả thi mà không bịa định mức

Tách giờ của R1-G01 thành hai nhóm: chi phí xây nền dùng chung một lần và chi phí viết/kiểm riêng nội dung. Ghi giờ người chủ trì làm thực, giờ chờ máy riêng và phần làm lại do lỗi. Làm tương tự ở R1-G02 để biết phần nào thực sự được dùng lại.

Với mỗi đợt hai tuần, lấy tổng giờ có thể làm, trừ việc bảo trì bắt buộc và dự phòng đã thống nhất; phần còn lại dành cho những đầu ra được chọn. Ước lượng theo loại gói tương tự, không lấy thời gian một gói hàm số nhân cho toàn bộ chương trình. Nếu không đủ, giảm định dạng phụ, số câu lặp và độ sâu ở phần đã đủ trước; không giảm kiểm định toán hoặc âm thầm bỏ mục tiêu chương trình.

Bản lịch cam kết còn cần ba dữ liệu từ quá trình triển khai: giờ sản xuất mỗi tuần, công sức hai gói mẫu sau khi tách chi phí chung, và mốc dùng học liệu thực. Việc chưa có ba số này không chặn sửa R1-G01 theo tài liệu; nó chỉ chặn việc hứa một ngày hoàn tất toàn chương trình có căn cứ.

## 6.7. Khi nào được gọi là hoàn thành dự án

Ấn bản 2027 được coi là hoàn thành ở cấp sản phẩm khi:

- Sổ yêu cầu cần đạt trong phạm vi đã chọn được đối chiếu; từng mục tiêu có vị trí học, nhiệm vụ đánh giá và trạng thái rõ. Không dùng số chương hoặc số gói thay phép kiểm này.
- Có đường nhập học qua D0 hoặc vào gói trực tiếp, cùng hướng dẫn lập lịch theo phần đã học và thời gian còn lại.
- Các gói lõi cần thiết ở R1–R8, Nền liên quan, phối hợp, đề và ôn cuối đã được kiểm và phát hành nhất quán.
- Có lời giải, phản hồi và nhiệm vụ thử lại; không chỉ có ngân hàng đề.
- Cấu hình mô phỏng và hướng dẫn thao tác thi đã được đối chiếu với công bố áp dụng cho kỳ thi 2027; mọi giả định cũ được xử lý.
- Không còn lỗi chặn đã biết trong bản phát hành; phần chưa được thực hiện hoặc ngoài phạm vi được công bố rõ.
- Bản nguồn, bản phát hành, quyết định thay đổi và cách tiếp tục cho năm sau truy nguyên được.

Kết quả học tập của mỗi học sinh được theo dõi riêng theo bằng chứng, không suy từ việc dự án đã làm xong tài liệu. Sau kỳ thi, tổng kết dữ liệu sử dụng và công sức để xây ấn bản tiếp theo; video và sản phẩm phụ có thể tiếp tục mà không làm dự án học liệu 2027 trở thành công việc không có điểm kết thúc.
