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

Bảng biến thiên dùng một JSON cho cả HTML và PDF qua `cong_cu/r1_g01.lua`.
Chú thích bảng trong QMD giữ đúng HTML (có chỗ khác title trong JSON).
PDF mở toàn bộ lời giải; tùy chọn in bản học sinh thuộc chức năng in HTML.
Hình HTML dùng SVG gốc, PDF dùng PNG gốc. Không chạy lại bộ sinh hình trong Pha 3.

Nghiệm thu trực quan toàn bộ PDF, HTML desktop/mobile và quyết định chuyển canonical
thuộc Pha 4/quyết định riêng, không được suy từ PASS kỹ thuật.
