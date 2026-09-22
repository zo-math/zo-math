# R1-G01 — ứng viên Quarto v1.2

Ứng viên QMD/Quarto v1.2 chuyển đổi từ nội dung v1.1, đang kiểm chứng thiết kế
theo ma trận quyết định v0.2 đã duyệt; chưa được chủ dự án nghiệm thu sản phẩm và chưa xuất bản.
Nguồn có thẩm quyền vẫn là HTML v1.1 tại
`_projects/on_thi_toan_thpt_2027/goi/R1-G01/src/noi_dung.html` (đường dẫn từ gốc repository).
Chưa chuyển canonical; không phát triển song song nội dung hai bản.

`lich_su/v1_1.json` ghi commit đối chiếu và SHA-256 của đủ 40 tệp lịch sử.
Không nhân bản HTML/Markdown cũ thành nguồn biên soạn thứ hai ở đây.
Nội dung QMD được trích trực tiếp từ HTML. Nhãn trạng thái dành cho người học là
“R1-G01 · Bản xem trước · Chưa xuất bản”; phiên bản ứng viên ghi trong hồ sơ nội bộ.
Ngoài nhãn và chỉ dẫn tải PDF V1–V2 đã duyệt, không biên tập lại nội dung học thuật.

Mỗi gói có project.id, cấu hình và `_quy_trinh/ho_so/index.yml` riêng.
`extensions.artifact_identity: path` chọn tên receipt/phiên dựa trên đường dẫn;
`extensions.artifact_inputs` bổ sung dữ liệu, hình và filter vào hash PDF.
Hai dự án cũ không bật lựa chọn này nên giữ tên receipt/phiên hiện hành.

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
Một nguồn `index.qmd` sinh hai PDF qua cùng pipeline Quarto/LuaLaTeX:

- `index.pdf`: bản đầy đủ, có lời giải;
- `index_hoc_sinh.pdf`: loại toàn bộ phần `#loi-giai` và các vùng `.answer-link`,
  giữ ví dụ, đọc thêm, sửa lỗi và nhật kí theo V3.

HTML tải hai tệp trên bằng tên `download` lần lượt là
`R1-G01_hoc_lieu_day_du_v1.2.pdf` và `R1-G01_hoc_va_bai_tap_v1.2.pdf`.
Không tạo bản sao theo tên thân thiện, không dùng in trình duyệt làm PDF chính thức.
Không còn nút/listener in; giữ hành vi hash mở khối chứa đích.
Hình HTML dùng SVG gốc. Cả mười hình `do_thi_01` đến `do_thi_10` dùng trực tiếp
PDF vector khi dựng PDF học liệu; mỗi PDF và SVG được dựng từ TEX cùng tên bằng bộ
công cụ đồ thị ZO Math tại commit `354fb22`. Không còn tài sản PNG canonical hoặc
pipeline Matplotlib riêng cho bộ mười đồ thị này.

## Vận hành hai biến thể

Từ gốc repository, dùng launcher hiện hành:

```text
python scripts/zo_python.py scripts/zo_qmd.py check content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/index.qmd
python scripts/zo_python.py scripts/zo_pdf.py build content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/index.qmd --variant full
python scripts/zo_python.py scripts/zo_pdf.py build content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/index.qmd --variant student
python scripts/zo_python.py scripts/zo_pdf.py status content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/index.qmd --variant full
python scripts/zo_python.py scripts/zo_pdf.py status content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/index.qmd --variant student
```

Mặc định không truyền biến thể vẫn là `full`. Cấu hình `extensions.pdf_variants`
khai đầu ra/metadata; receipt nhận diện đường dẫn nguồn + biến thể, theo dõi nguồn,
JSON, hình, filter, cấu hình và pipeline. Hai dự án cũ không bật hợp đồng biến thể
nên giữ cách vận hành mặc định. Build biến thể chạy trong bản sao tạm cô lập dưới
`_audit`, chỉ thay đúng đầu ra sau render thành công; thất bại không xóa PDF cũ.

Trước mỗi render: xác nhận không có preview nền ngoài phiên kiểm chứng được quản lí,
ghi hash hai PDF hiện hành. Không render toàn repository thật để kiểm gói này.
HTML dùng `zo_qmd.py render` trong mirror riêng với profile `on-thi-preview`;
đặt đúng Git work-tree/index riêng của mirror khi dùng checker, không staging.
Dựng PDF trước lượt HTML cuối để resources tải xuống là đúng bản vừa kiểm.
QMD chỉ khai định dạng HTML; PDF được chọn tường minh qua pipeline/profile PDF,
không để preview HTML tự động sinh PDF cạnh nguồn.

Sidebar chuyên mục chỉ kích hoạt trong profile preview (host `127.0.0.1`), gồm
ba trang hiện có; chính cấu trúc đó sẽ dùng khi có quyền công bố, không tạo bản song song.
Metadata `draft` và hàng rào public vẫn giữ nguyên. Nhãn draft Quarto được đưa vào
vị trí trạng thái của gói, không làm mất trạng thái bản nháp hoặc thay chính sách xuất bản.

Nghiệm thu trực quan HTML/hai PDF, chấp thuận thiết kế và chuyển canonical là các
quyết định riêng của chủ dự án, không được suy từ PASS kỹ thuật. Cảnh báo hyphenation
tiếng Việt và cảnh báo lịch sử khóa `/Group` tiếp tục được ghi riêng trong báo cáo audit.
