# Bố cục PDF độc lập — hợp đồng áp dụng cho D0

Ngày 14/10/2026. Chủ trì giao nghiên cứu quy cách bản in từ bốn trang
hiện có/Ngôn ngữ thiết kế 0.4, thêm footer HTTPS và đồng bộ Ủng hộ HTML.
Chủ trì đã duyệt bản mẫu 9 trang và giao đồng bộ nguồn, quy tắc, dựng PDF
đầy đủ ngày 14/10/2026. Các thông số dưới đây là hồ sơ bản in D0 đang áp
dụng; không tự mở rộng sang PDF khác hoặc khóa Design 0.5. Việc duyệt bản
mẫu khác với nghiệm thu từng trang của PDF đầy đủ và với xuất bản website.

## 1. Bằng chứng và bài học thiết kế

Đã xem bốn HTML trong bộ hiện hành DH_043 tại
`_audit/home-layout-implementation/preview/` và mã nguồn kit. Đây là nguồn
đối chiếu thị giác; công cụ PDF không đọc các HTML audit để sinh sản phẩm.
Bộ bảo vệ QD_035 và bản DH_043 không bị thay thế hoặc chỉnh sửa bởi mẫu PDF.

| Bề mặt | Quan sát | Vận dụng cho bản in |
|---|---|---|
| Nhà | Hero rõ, vùng lớn trắng/xám rất nhẹ, thông tin theo nhịp, logo và Ủng hộ có cấu trúc | Bìa gọi rõ tài liệu; phân nhóm bằng vị trí và khoảng cách, không thêm nền toàn tờ để mô phỏng web |
| D0 | Năm khu vực, nhãn bài và ba trường chuẩn bị, câu hỏi khác phần đối chiếu | Dàn câu theo cột thông tin chuẩn bị và vùng đề; đối chiếu ở khu vực sau, có số trang qua lại |
| G01 | Kiểu chữ Be, phân cấp rõ, nội dung trong vùng đọc, tag nhỏ, bảng/hình theo chức năng | Bộ vai trò bản in cho tiêu đề/chữ/nhãn/bảng, hình cùng nhãn và chú thích; không nhập sidebar/toolbar vào giấy |
| G02 | Cùng hệ nhận diện với G01, vùng lời giải/tiêu chí có thứ bậc | Một cấu hình chung cho các vai trò, khác bản đồ trang theo nội dung gói |
| Ủng hộ chung | Logo stack bên trái, tiêu đề đỏ trầm, QR cạnh nhãn nhỏ/giá trị đậm, CTA vàng | Giữ quan hệ thị giác và nguồn HTML; đổi px sang kích thước in, bỏ hành vi hover/focus |

D0 HTML hiện tại chỉ có liên kết Ủng hộ ở rail, không có component đầy đủ
trong vùng nội dung. Mẫu PDF khai rõ binding đến component HTML dùng chung
G01/G02; không giả báo đã trích một vùng không tồn tại trong D0 HTML.
Home giữ lời mời/CTA riêng; không dùng biến thể Home thay bản chung ngầm.

PDF DH_042 đã có adapter TeX/Lua, nhưng mới đổi chi tiết trên dòng xuất
Pandoc và ép ngắt theo ID. Nó chưa sở hữu bộ vai trò/bản đồ trang riêng;
đây là nguyên nhân hệ dàn chưa tạo được cảm giác ấn phẩm hoàn chỉnh.

## 2. Kiến trúc vận hành

`QMD/JSON canonical → AST có vai trò → hồ sơ bản in → TeX → PDF → kiểm`.
HTML đi qua nhánh riêng. Không lấy DOM cuối của toàn trang HTML làm cách
dàn nội dung PDF, không chụp trang web rồi đóng vào A4, không viết lại một
bản văn học liệu song song để dễ thiết kế.

- Nội dung/ý nghĩa, công thức, ID và thứ tự thuộc QMD/JSON hiện hành.
- Hồ sơ bản in sở hữu khổ/lề, typography, bề rộng cột, vai trò trang, ghép
  đơn vị đọc, liên kết/số trang và ranh giới được phép ngắt.
- Template bản in sở hữu hiện thực các vai trò; không chứa đề/đáp án mới.
- Vùng Ủng hộ là ngoại lệ có thẩm quyền nguồn: component HTML tương ứng
  sở hữu câu chữ/tài khoản/logo/QR/CTA và quan hệ thị giác; bộ chiếu PDF
  chuyển chúng sang cấu trúc in, không giữ một bản khai độc lập.
- Bộ dựng đầy đủ kiểm inventory 25 đề (Bài 00 và 24 bài) và 25 đối chiếu,
  fingerprint nguồn trước khi thay đầu ra. Mẫu trích đoạn đã hoàn thành vai
  trò quyết định thiết kế, không còn là đầu vào của biên dịch chính thức.

## 3. Quy cách bản in D0 đã chọn

| Vai trò | Quy cách bản in |
|---|---|
| Tờ giấy | A4 trắng; lề trên/dưới 22 mm, trái/phải 21 mm; một trục nội dung chính |
| Chữ | Thân Be Vietnam Pro 11 pt/16 pt; toán STIX Two Math; tiêu đề trang 23 pt, bài 16 pt, lời giải 15 pt; không thu nhỏ toàn cuốn để vừa số trang |
| Bìa | Logo, chương trình, tên tài liệu lớn, nhận diện đỏ/vàng, tên bản, hướng dẫn ngắn, QR, phiên bản/ngày/bản quyền |
| Hướng dẫn | Một cột có khoảng cách đoạn rõ; tiêu đề và câu dẫn tạo điểm vào, không làm mỗi đoạn thành thẻ |
| Câu khảo sát | Một cột đọc; nhãn dạng Bài 01 • R1; tên bài chính; ba trường chuẩn bị gọn dưới tên, rồi đến đề đủ chiều rộng; phân nhóm bằng khoảng trắng, không kẻ ngang giữa mọi bài |
| Bảng và hình | Lưới .5 pt đủ ngang/dọc; JSON bảng dấu giữ nguyên; hình vector có nhãn chính cùng cỡ chữ thân bài, tính theo font nguồn thay vì phóng theo phần trăm trang; chỉ số dưới giữ tỉ lệ toán |
| Đối chiếu | Mã bài và link về đề cùng hàng; tên giống đề; kết quả lấy nguyên câu nguồn đặt trước lời giải; lưu ý/ôn lại là văn bản có nhãn; không tự đặt nền; giữ trọn cụm trong trang mẫu |
| Chọn mạch | Bảng thuật ngữ/mô tả rộng cột nội dung, đọc theo hàng; không biến thành grid trang web |
| Trang kết và Ủng hộ | Riêng mục Học tiếp có hai cột: nội dung trái, QR/liên kết phải; phía dưới là khung Ủng hộ riêng rộng hết vùng đọc, bo nhẹ, mặt trắng của component HTML, viền gray-3 của 0.4 theo yêu cầu chủ trì; logo stack, QR, trường HTML, CTA vàng; không có câu chữ/tài khoản độc lập |
| Footer | Chương trình trái, `zomath.vn` có link ở giữa, số trang phải; trang bìa cũng có liên kết giữa |

Phạm vi bản dựng chính thức: toàn bộ phần công khai của `index.qmd`, gồm lời
dẫn, Bài 00, 24 đề, 25 đối chiếu, bảng tám mạch, lời mời học tiếp, bìa/kết.
Hồ sơ bản in có thể chuyển hướng dẫn “Ghi điều em nhận ra” lên phần bắt đầu
để người đọc biết cách ghi từ đầu; câu chữ lấy nguyên nguồn. Hướng dẫn
“Em có thể đọc lại cách giải…” lặp giống hệt trong 24 đối chiếu được in
một lần; bộ dựng bắt buộc kiểm mọi bản lặp trùng nhau. Không lược toán,
đáp án, lưu ý hay nội dung cần ôn.

Ghép nhiều bài trên một trang khi toàn đơn vị đọc vừa trang; bài có hình
hoặc bảng lớn có thể có trang riêng. Không để đề bị cắt trong minipage;
đơn vị vượt chiều cao phải đổi vai trò trang/phân đoạn ở ranh giới nội dung,
không nén chữ/cắt/giấu overflow. Bản D0 hiện giữ trọn từng đề và đối chiếu;
nếu nguồn dài hơn khung trang, phải xây tiếp trang có nhãn bài trước khi dựng.

Hiệu chỉnh theo phản hồi chủ trì ngày 14/10/2026: bốn đối chiếu của mẫu
được ghép thành hai trang, có cùng thứ bậc kết quả/lời giải/lưu ý/ôn lại.
Bản dùng nền nhận xét và đường kẻ giữa bài bị chủ trì đánh giá 4/10,
không đạt; bản đã duyệt bỏ các chi tiết ấy.
Không lạm dụng đường kẻ; khối có nền chỉ được dùng đúng component/vai trò
của 0.4. Mẫu này dùng văn bản thường cho nhận xét. Đoạn hướng dẫn chung giống hệt ở
bốn bài được trình bày một lần trong phần đối chiếu; bộ dựng
kiểm các đoạn giống nhau trước khi gộp. Không viết lại đáp án: bộ chiếu
tách nguyên câu hoặc phần in đậm từ AST nguồn. Nguồn hiện thay đổi khiến
không nhận diện được kết quả/vai trò phải chặn dựng để rà lại.

## 4. Đồng bộ Bảo trợ từ HTML

Theo yêu cầu mới ngày 14/10/2026, khung bìa/kết/header/footer D0 đã duyệt
được cụ thể hóa thành hai template dùng chung trong `assets/tex/zo-course-pdf-*`.
Hướng tích hợp tại `06_pdf.md`; nội dung ruột, chọn phần, hình và bảng
vẫn do nguồn/hồ sơ từng gói sở hữu. D0 giữ nguyên PDF đã có; G01 opt-in
và dựng bản đầy đủ trước khi xem xét các biến thể còn lại.

`scripts/zo_pdf_support.py` đọc template HTML hiện hành và cấu trúc
`.support-content`, `.r1-support-details`, `.r1-support-link` cùng token
màu trong CSS. Khai bindings tài sản theo `PreviewBuilder.common_assets`:
QR tại `assets/images/`, logo tại bộ mẫu 0.4. Mỗi lần dựng lấy lại nguồn,
ghi fingerprint; thiếu trường/token/tài sản phải chặn dựng, không dùng
cache HTML/JSON của lần trước. Khi component HTML đổi, PDF phải dựng lại.

Đồng bộ gồm tiêu đề, lời mời, thứ tự nhãn/giá trị, nội dung chuyển khoản,
CTA/URL, QR/logo và vai trò màu. Dàn in có kích thước riêng. Token/layout
HTML đổi ngoài những vai trò bộ chiếu hỗ trợ phải mở lại kiểm thị giác,
không tuyên bố “tự đồng bộ mọi CSS”. Binding Home khác câu chữ chưa được
bộ mẫu D0 triển khai; khi dùng cần nạp nguồn QMD/adapter Home tương ứng.

## 5. Điểm vào production và cổng kiểm

Nguồn quản lý trong D0: `index.qmd`, JSON hình/bảng, `cong_cu/d0_print.lua`,
`cong_cu/d0_print_profile.json`, `giao_dien/d0_pdf.tex` và
`giao_dien/d0_pdf_end.tex`. `cong_cu/dung_pdf.py` dựng từ QMD bằng Quarto
trong cây cô lập `.quarto`, lấy Ủng hộ từ component HTML qua
`scripts/zo_pdf_support.py`, rồi thay `index.pdf` sau khi thành công. Bộ
dựng không đọc `_audit/` hoặc PDF mẫu làm đầu vào.

```text
python scripts/zo_python.py -B scripts/zo_qmd.py check content/thpt/on_thi_toan_thpt/hoc_lieu/d0/index.qmd
python scripts/zo_python.py -B content/thpt/on_thi_toan_thpt/hoc_lieu/d0/cong_cu/dung_pdf.py
python scripts/zo_python.py -B content/thpt/on_thi_toan_thpt/hoc_lieu/d0/cong_cu/kiem_chung_pdf.py
```

Checker kiểm toàn nguồn và ca âm, inventory đề/đối chiếu, công thức, lưới
bảng trên ảnh, hình vector, font nhúng, liên kết/đích nội bộ, footer từng
trang, metadata và đủ trường Ủng hộ HTML. Xem trực quan đủ trang màu/sắc
xám; in giấy và quét QR là phép kiểm riêng. Trạng thái nghiệm thu bản đầy
đủ và trạng thái xuất bản phải ghi riêng, không suy từ kết quả máy.
