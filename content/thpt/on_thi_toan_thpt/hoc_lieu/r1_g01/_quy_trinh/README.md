# R1-G01 — ứng viên Quarto v1.2

`index.qmd` là nguồn canonical duy nhất của học liệu v1.2. Nội dung và kỹ thuật đã
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

Manifest `r1-section-download-files` trong metadata là nguồn duy nhất cho ranh giới
ID, nhãn, tên tải và `r1-view`. Registry PDF chỉ khai output, branding và thuộc tính
pipeline. Filter từ chối ranh giới thiếu/trùng/sai thứ tự; sau phép chiếu, hash còn
đích được giữ nội bộ, còn hash vượt phạm vi được đổi sang URL canonical từ registry
với đúng `r1-view` và nhãn “mở trên trang học liệu”. Mỗi bản theo phần giữ phần mở
đầu chung, Cách học, đúng phần đã chọn và Nguồn đối chiếu; không mang vùng tải PDF
hoặc khung tài khoản. Luyện tập và Kiểm tra không mang lời giải hay thang chấm.

HTML tải hai tệp trên bằng tên `download` lần lượt là
`R1-G01_hoc_lieu_day_du_v1.2.pdf` và `R1-G01_hoc_va_bai_tap_v1.2.pdf`.
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

## Vận hành tám biến thể

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
Dựng PDF trước lượt HTML cuối để resources tải xuống là đúng bản vừa kiểm.
QMD chỉ khai định dạng HTML; PDF được chọn tường minh qua pipeline/profile PDF,
không để preview HTML tự động sinh PDF cạnh nguồn.

Sidebar chuyên mục nằm trong cấu hình nguồn dùng chung, gồm cổng Ôn thi, ấn bản
2027 và học liệu này; profile preview chỉ cấu hình máy chủ cục bộ. Ranh giới public
đã duyệt chỉ chọn đầu ra qua allowlist và tiếp tục chặn hồ sơ nội bộ; trạng thái
“Có thể học” không thay thế `publication: pending` và không phải tuyên bố đã xuất bản.

Nghiệm thu trực quan HTML/hai PDF, chấp thuận thiết kế và chuyển canonical là các
quyết định riêng của chủ dự án, không được suy từ PASS kỹ thuật. Cảnh báo hyphenation
tiếng Việt và cảnh báo lịch sử khóa `/Group` tiếp tục được ghi riêng trong báo cáo audit.

## Hồi quy header và docking

Running header dùng template chung một dòng: ZO Math + tên chính thức, không có
nhãn biến thể. Nhãn hai bản vẫn nằm trên bìa/thẻ tải. Checker R1 kiểm tọa độ chữ
trong PDF thật qua `cong_cu/kiem_chung_header_pdf.py`; ưu tiên Poppler
`pdftotext -bbox` và dùng fallback chỉ-đọc bằng `pypdf` khi binary cục bộ thiếu
khả năng này.

Thanh thẻ di chuyển nguyên node vào header khi bám dính; slot giữ chỗ trong nội
dung. Cả cụm dùng chung transform Headroom; không đổi navbar toàn website.
Kiểm thử qua HTTP local bằng Chrome profile tạm, ví dụ:

```text
node content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/cong_cu/kiem_chung_navbar.mjs --url http://127.0.0.1:8781/content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/ --out _audit/r1_g01_navbar_regression
```

`--chrome` cho phép chỉ định executable khác. Công cụ đo từng khung hình ở
1440/430/390 px, lưu JSON và chuỗi PNG; kiểm cả menu, focus, history, guidance,
liên kết lời giải, bàn phím, no-JS và touch mô phỏng. Đây không phải nghiệm thu
trên thiết bị cảm ứng thật hoặc chấp thuận của chủ dự án.
