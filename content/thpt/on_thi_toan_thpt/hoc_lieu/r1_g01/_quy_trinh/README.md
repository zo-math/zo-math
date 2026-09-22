# R1-G01 — ứng viên Quarto v1.2

Chỉ là ứng viên kỹ thuật của Pha 3, chưa nghiệm thu và chưa xuất bản.
Nguồn có thẩm quyền vẫn là HTML v1.1 tại
`_projects/on_thi_toan_thpt_2027/goi/R1-G01/src/noi_dung.html` (đường dẫn từ gốc repository).
Chưa chuyển canonical; không phát triển song song nội dung hai bản.

`lich_su/v1_1.json` ghi commit đối chiếu và SHA-256 của đủ 40 tệp lịch sử.
Không nhân bản HTML/Markdown cũ thành nguồn biên soạn thứ hai ở đây.
Nội dung QMD được trích trực tiếp từ HTML, giữ cả nhãn “Phiên bản 1.1” trong thân bài;
phiên bản ứng viên 1.2 chỉ ghi ở hồ sơ kỹ thuật.

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
PDF mở toàn bộ lời giải; tùy chọn in bản học sinh thuộc chức năng in HTML.
Hình HTML dùng SVG gốc. Cả mười hình `do_thi_01` đến `do_thi_10` dùng trực tiếp
PDF vector khi dựng PDF học liệu; mỗi PDF và SVG được dựng từ TEX cùng tên bằng bộ
công cụ đồ thị ZO Math tại commit `354fb22`. Không còn tài sản PNG canonical hoặc
pipeline Matplotlib riêng cho bộ mười đồ thị này.

Nghiệm thu trực quan toàn bộ PDF, HTML desktop/mobile và quyết định chuyển canonical
thuộc Pha 4/quyết định riêng, không được suy từ PASS kỹ thuật.
