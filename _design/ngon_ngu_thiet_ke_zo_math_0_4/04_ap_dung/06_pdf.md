# PDF và học liệu tải về

Nơi làm việc theo thông tin đã có: `E:/zo_math`. Trạng thái repo hiện tại: **cần AI tại máy xác minh**.

Quy tắc liên quan: ZO001, ZO012, ZO014, ZO015, ZO019, ZO031.

## Bản thử bộ sinh R1 ngày 19/10/2026

Theo yêu cầu chủ trì sau rà soát, `course-print-v2` được bật thử riêng cho G04 qua `extensions.course_pdf_shell.layout`; chưa áp dụng sang các gói còn lại. Hồ sơ vai trò chung ở `assets/tex/zo-course-print-profile.json`, phép chiếu ở `assets/lua/zo_course_package_pdf.lua`/`zo_course_print.lua`, template ở `assets/tex/zo-course-print-layout.tex`, cổng ở `scripts/zo_course_pdf_layout.py`. Chỉ 03 ghi bản xem và kết quả hiện hành.

- R1 dùng thân STIX Two Text, toán STIX Two Math, tiêu đề/nhãn và bìa/kết Be Vietnam Pro. Không mang quy cách thân Be Vietnam Pro riêng của D0 sang R1. Giữ khung bìa/kết/header/footer đã duyệt.
- Giữ cây khu vực/nhóm/nhiệm vụ từ QMD, chuyển cấp phù hợp bản in; mục lục in không thay bookmark. Biên dịch đủ lượt ổn định và đối chiếu từng số trang dẫn với footer thật của đích, không chỉ kiểm hết dấu hỏi.
- Bảng chức năng lấy tỉ lệ từ cùng `course-tables.json`; metadata tỉ lệ cũ không được ghi đè profile. BBT native lấy JSON canonical, giữ từng ô/mốc/dấu/cột loại. Nhãn chữ dùng chữ, không đưa tiếng Việt vào môi trường toán. Caption giữ dưới hình/bảng theo tình huống nguồn.
- Đồ thị dùng đúng cặp vector hiện hành và quy cách `lesson-g03`. Phép chiếu in giữ cùng tỉ lệ giữa các hình, quy đổi nhãn chính từ cỡ vector 12,8 pt về 11 pt theo hướng dẫn bản in; không dùng phần trăm chiều rộng trang để kéo đồng loạt hoặc sửa vector chỉ để đổi cách đặt. Kiểm luồng nội dung nhúng, hệ số đặt và biên hình thật.
- Liên kết nội bộ có đích riêng theo ID và số trang; đích ngoài biến thể giữ URL canonical/chế độ xem đúng ngữ cảnh. Không đổi chữ Xem lời giải/Xem đề bài. Cổng chặn thiếu glyph, sai phông vai trò, thiếu BBT, sai ô/dấu, sai profile cột, sai kích thước hình hoặc sai số trang trước khi thay thành phẩm.
- Dựng thử bằng `zo_pdf.py build <nguồn> --variant full --out-dir .quarto/<hồ sơ mới>` qua launcher. Bản thử và biên nhận lưu riêng, không cập nhật PDF/provenance canonical hoặc metadata thẻ tải. Sau kiểm kỹ thuật phải xem toàn bộ trang màu và các trang hình/bảng ở sắc xám. Chủ trì duyệt bản thử trước khi áp dụng rộng; không suy thành quyền commit/phát hành.

## Bổ sung vận hành ngày 14/10/2026

**Khung PDF dùng chung kế thừa D0 đã duyệt, 14/10/2026:** chủ trì yêu cầu
trang đầu, trang cuối, header và footer giữ cùng giao diện giữa các gói.
Nguồn dùng chung là `assets/tex/zo-course-pdf-shell.tex` và
`assets/tex/zo-course-pdf-end.tex`; `scripts/zo_pdf_course_shell.py` cấp
tên gói/phiên bản/URL/ngày dựng từ QMD, registry và hồ sơ hiện hành.
Bìa dùng logo 42 mm, tên 39/45 pt, hai nét đỏ/vàng, QR học liệu 24 mm;
header hai phía không kẻ ngang, footer khóa học trái–website giữa–số trang
phải. Trang kết giữ lời học tiếp trái–QR khóa phải, khung Bảo trợ bên dưới
rộng toàn vùng đọc, logo/QR/trường/CTA lấy component HTML nguồn hiện hành.
Tên/phiên bản/URL thay theo gói; vị trí, vai trò và kích thước giữ chung.
Bìa giữ footer website như D0; trang kết giữ footer trang ruột.
Chỉ gói opt-in qua `extensions.course_pdf_shell` mới nhận khung mới.
Lượt đầu dựng riêng biến thể đầy đủ G01 qua `zo_pdf.py build --variant full`;
không tự dựng bảy bản khác, G02 hoặc thay PDF D0 đã duyệt. Nghiệm thu G01
vẫn riêng; kế thừa thiết kế D0 không thay việc xem từng trang của G01.

**Chỉ thị tiếp theo ngày 14/10 — footer, Ủng hộ và bố cục độc lập:**
footer mỗi trang đặt liên kết `zomath.vn` ở giữa, đích `https://zomath.vn`.
Vùng Ủng hộ phải nhất quán với HTML tương ứng về cấu trúc, vai trò chữ,
logo, QR, thứ tự trường và điểm nhấn; cập nhật tự động từ nguồn component
HTML hiện hành ở mỗi lần dựng. Không chỉ lấy tài khoản rồi viết lại lời
mời/hình thức riêng trong PDF. Chỉ dẫn mới này thay cách D0 DH_042 đọc
riêng bảng tài khoản của trang Bảo trợ cho vùng Ủng hộ.

Nội dung PDF lấy QMD/JSON canonical, nhưng cách dàn phải do hồ sơ bản in
sở hữu, độc lập DOM/CSS/tương tác HTML. Quy cách, nghiên cứu bốn trang,
cơ chế production và cổng kiểm nằm ở [bố cục PDF độc lập](06_pdf_bo_cuc_doc_lap.md).
Chủ trì đã duyệt bản mẫu D0 và giao áp dụng toàn bộ từ QMD ngày 14/10/2026.

Chủ trì giao cụ thể hóa hướng dẫn PDF từ nền 0.4 và dựng lại D0 từ QMD.
Các yêu cầu chức năng dưới đây áp dụng khi tích hợp PDF theo bộ này;
thông số dàn trang là cấu hình khởi đầu để kiểm trên sản phẩm thật, không
tuyên bố khóa Design 0.5 hay tự động nghiệm thu các PDF khác. Nguồn/mẫu
khóa ở 06/07 được giữ nguyên. D0 là bản kiểm chứng đầu tiên của bổ sung này.

### Bìa và thông tin ấn bản

- Có logo, tên học liệu, chương trình, tên bản tải và mô tả sử dụng ngắn.
- Hiển thị phiên bản nội dung và ngày tạo PDF (dd/mm/yyyy), phân biệt ngày
  dựng với ngày nghiệm thu/phát hành. Không chỉ lưu ngày trong metadata.
- Có dòng © năm ZO Math và tuyên bố bản quyền nội dung thuộc ZO Math.
  Không tự thêm giấy phép, quyền tái phân phối, điều khoản thương mại hay
  quyền đối với tài sản bên thứ ba khi chủ trì chưa xác lập.
- QR trang học đi cùng nhãn mô tả đích; tên/phiên bản/URL lấy từ nguồn
  sản phẩm. Đủ vùng trắng quanh QR, không kéo méo; ưu tiên QR đen trên trắng
  khi in. Kiểm quét là phép kiểm riêng, không suy từ việc ảnh đã hiện.

### Trang ruột và nhịp đọc

- A4 là cấu hình khởi đầu của học liệu tự học; lề khoảng 23–24 mm, thân bài
  11 pt. Không thu nhỏ chữ toàn cuốn để ép số trang. Font thân/toán dùng
  STIX, tiêu đề/nhãn dùng Be Vietnam Pro theo vai trò; phải nhúng font.
- Tiêu đề bài và số bài tạo điểm tìm rõ; nhãn phụ nhỏ hơn thân bài nhưng
  vẫn đọc được. Tiêu đề từng lời giải phải nổi bật hơn các nhãn bên trong.
- Dàn theo chặng có nghĩa; có thể mở mỗi mạch ở trang mới. Không ép mọi
  tiêu đề thành trang mới gây trang gần rỗng. Giữ tiêu đề với phần đầu
  nội dung, bảng với lời dẫn/chú thích, tránh dòng lẻ và công thức tràn.
- Khoảng trắng phục vụ phân nhóm; không dùng khoảng trống lớn thiếu chức
  năng để tách hai hành động liên quan. Không bắt buộc lấp kín mọi trang.
- Đầu/chân trang có nhận diện học liệu và số trang; mục lục/bookmark đúng
  đích. Liên kết nội bộ phục vụ cả màn hình và bản in: bổ sung số trang đích
  khi lời dẫn chỉ có “Đối chiếu”/“Quay lại”. Không được có “trang ??” cuối.
- Giữa footer có chữ `zomath.vn` bấm được, đích HTTPS gốc; không căn theo
  phần nội dung còn lại hoặc chỉ xuất hiện ở bìa/kết. Kiểm vị trí/link
  trên từng trang, gồm cả trang mở đầu/tiếp trang.
- Bảo toàn toàn bộ câu chữ, toán và ID. Hồ sơ bản in D0 được chuyển phần
  hướng dẫn ghi nhận lên trước bài làm và gộp đoạn hướng dẫn giống hệt lặp
  ở 24 lời giải sau khi kiểm trùng. Các thay đổi thứ tự/gộp khác phải được
  ghi rõ và duyệt như quyết định thiết kế, không núp dưới dàn trang.

### Bảng, bảng dấu, bảng biến thiên và hình

- Lưới ngang/dọc đầy đủ, nét đồng đều khoảng 0,5 pt ở bản A4; kiểm cả
  viền ngoài, ô trống, hàng tiêu đề và phần tiếp trang. Tránh nền ô che
  đường kẻ. Không coi có lệnh hline trong nguồn là bằng chứng đủ lưới.
- Bảng mô tả hai cột ưu tiên khoảng 36/64; bảng số căn giữa theo chức năng,
  bảng lời căn trái. Điều chỉnh khi tiêu đề dài hoặc dữ liệu thực đòi hỏi.
- Bảng dấu/biến thiên lấy JSON hiện hành, dựng LaTeX native khi đủ khả
  năng biểu đạt. Giữ đúng mốc, dấu, giới hạn, điểm loại và số hàng; không
  thêm hàng hàm số cho bảng chỉ có dấu. Không dùng khung bo/nền dư của bản
  vector cũ nếu không có lý do kỹ thuật cụ thể đã ghi nhận.
- Tài sản hình học/đồ thị ưu tiên vector; không thay bằng ảnh chụp PDF.
  Kiểm nhãn, nét khuất, dấu và độ đọc ở cỡ sử dụng, không chỉ khi phóng lớn.

### Trang kết và Ủng hộ

- Có logo ZO Math, lời dẫn học tiếp, đường quay lại học và QR có nhãn.
- Khối Ủng hộ có ngân hàng, chủ tài khoản, số tài khoản dạng chữ, nội dung
  gợi ý và QR chuyển khoản; lời mời tự nguyện, không lấn mục đích học.
- Nguồn sở hữu là component Ủng hộ HTML đang dùng cho bề mặt tương ứng.
  Dựng component tươi từ template/dữ liệu nguồn quản lý, chiếu sang bản in;
  fingerprint template, CSS, logo và QR. Không đọc HTML audit làm đầu vào
  production, không hard-code lời mời/tài khoản/nút trong template PDF.
  Binding mẫu D0 dùng component HTML chung của G01/G02 tại
  `_design/web_2027_mau_dung_chung/templates/support.html.tpl`; Home có
  biến thể câu chữ riêng và cần binding riêng khi dựng PDF của Home.
  Đối chiếu tài khoản với nguồn Bảo trợ là kiểm tính nhất quán, không dùng
  nó để tự thay diện mạo/câu chữ của component HTML.
- QR học liệu và QR chuyển khoản có nhãn khác nhau. Trước phát hành phải
  xác nhận đích/tài khoản của QR, không chỉ so tên tệp hoặc nhìn logo ngân hàng.
- Lặp lại phiên bản, ngày tạo và bản quyền ở cuối; thông tin nguồn kỹ thuật
  chỉ là ghi chú nhỏ, không chiếm trọng tâm trang kết.

### Điều kiện kiểm và bàn giao

1. Checker nguồn xác nhận bảo toàn nội dung/toán/ID; PDF có đủ nhiệm vụ,
   lời giải, font nhúng, liên kết, metadata và khổ giấy.
2. Xem toàn bộ PDF màu; xem sắc xám mọi trang có bảng/hình và bìa/kết,
   kiểm tại cỡ đọc thực. Ghi rõ chưa in giấy/chưa quét QR nếu chưa làm.
3. Kiểm hồi quy bảng phải bao gồm bảng có ô tiêu đề trống, bảng nhiều dòng,
   bảng dấu có ô khoảng trống và bảng tiếp trang. Kiểm cấu trúc kết hợp
   hình ảnh; kiểm tự động không thay chủ trì duyệt thị giác.
4. Với lỗi tái diễn, ghi triệu chứng, nguyên nhân đã xác minh, nguồn sửa,
   guard và bằng chứng; tách sửa xong/kiểm xong/chủ trì duyệt/phát hành.
5. Dựng từ nguồn quản lý, không đọc `_audit/` làm đầu vào. Chỉ giữ bằng
   chứng còn phục vụ đối chiếu; dọn trung gian. Giao PDF mới cùng hướng
   dẫn đã cập nhật, biên nhận dựng và giới hạn kiểm còn lại.

## Phạm vi mẫu hiện có

0.4 có bìa và trang kết mới cho tám PDF R1-G01. Trang ruột giữ nguồn v1.3, một số tài liệu được thêm trang kết sau nội dung cuối thay vì thay trang có bài học. Metadata và bằng chứng nằm ở design/pdf_editions.json trong mẫu.

## Cách tích hợp

Đọc pipeline PDF hiện tại của gói, YAML/TeX/Lua, logo/font, quyền sử dụng, link canonical, đánh số và biến thể học sinh/giáo viên/bài học. Không giả định mọi PDF của khóa dùng pipeline bài viết chung trong _quarto-pdf.yml.

Dùng nội dung đang có để dựng lại; đưa thiết kế bìa/kết thành template có dữ liệu tên bài, biến thể, phiên bản và đường quay lại học. Không lấy PDF ruột 0.4 ghép vào bản học liệu mới. Chưa giao tái dàn ruột thì ghi rõ phạm vi chỉ bìa/kết; nếu giao ruột, xử lí font, tag, bảng native và ngắt trang cùng ca kiểm.

## Kiểm và đầu ra

Kiểm bìa/ruột/cuối tất cả biến thể bị tác động, bookmark, hyperlinks, số trang, font nhúng, QR, mã phiên bản nội dung và chữ trên giấy. Đối chiếu dữ liệu ủng hộ từ nguồn hiện dùng trước phát hành. Kiểm trắng đen và kích thước in. Đầu ra gồm template tích hợp, PDF từ nguồn hiện tại, đối chiếu bảo toàn nội dung và cách chọn lại template cũ.


### Đồng bộ cả khóa theo yêu cầu ngày 19/10/2026

Yêu cầu đồng bộ sáu trang của chủ trì thay giới hạn chỉ thử G04 ở mục trước: `course-print-v2` áp dụng G01–G04 và cả tám biến thể mỗi gói. D0 giữ quy cách in riêng đã duyệt; trang Khóa 2027 là trang cửa ngõ HTML, không tự tạo thêm loại PDF ngoài hệ sản phẩm hiện hành. Cùng nguồn chính thức phải tái tạo được HTML và PDF; mẫu, bộ chuyển, phông, hình vector, bảng và liên kết tải đều nằm trong hợp đồng đầu vào/đầu ra.

Hình ghép rộng hơn vùng in được xoay nguyên hình khi in, giữ nguyên thứ tự/hướng tương đối các ô, hình học và cỡ chữ/nét; không thu nhỏ riêng để ép vừa trang. Kiểm hình nhúng phải tính đầy đủ ma trận xoay và tỉ lệ. Nhãn đích có tiếng Việt được mã hóa nhất quán trong bộ chuyển PDF; URL trở về HTML giữ nguyên. Trạng thái văn bản trong ô BBT như “Không tồn tại” phải giữ đúng dữ liệu, không thay bằng phát biểu khác.

Mỗi biến thể kiểm theo đúng phạm vi của nó: đủ mục, bảng, hình, đề/lời giải và đích nội bộ; đích ngoài biến thể trở về đúng vùng trên HTML. Số trang của thẻ tải lấy từ PDF mới, hash tệp tải phải khớp bản vừa dựng. Bản đang duyệt được đăng ký bằng manifest `ban_dang_duyet.json` tại `_quy_trinh` của khóa; cổng kết sổ tự phát hiện và bảo vệ đủ phụ thuộc, kể cả ngoài thư mục HTML. Không dùng việc giữ bản xem thay cho bảo toàn nguồn, và không dùng kỹ thuật đạt thay chủ trì nghiệm thu.

### Bảo toàn nguồn và kiểm hình khi tái dựng

Ảnh có hoặc không có chú thích đều phải căn giữa trong cột đọc, giữ đúng kích thước in đã chốt và không tự sinh tên từ alt. Bộ chiếu đưa ảnh độc lập qua cùng thành phần Figure; cổng PDF đo vị trí hình vector thật, từ chối lệch tâm quá hai điểm in. Nhãn được kiểm ở nguồn đồ thị và bằng quan sát, không chỉ qua hash.

Ảnh bìa trên thẻ học liệu, bìa HTML và PDF lấy từ cùng `giao_dien/anh_bia.json`; chuyển SVG đã kiểm hash sang PDF vector chỉ đổi định dạng, không thay ảnh hoặc tự cấp duyệt. D0 giữ vai trò phông riêng đã chốt, có bookmark các phần; các bảng D0 nhận cùng tỉ lệ cột/căn cột từ profile chức năng như HTML. Không phục hồi bộ dựng bảng cố định theo số cột.
