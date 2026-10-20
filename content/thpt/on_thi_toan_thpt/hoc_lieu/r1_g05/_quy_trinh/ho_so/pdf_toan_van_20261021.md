# R1-G05 — PDF toàn văn để duyệt dàn trang, 21/10/2026

Bản toàn văn gồm 38 trang, đầu ra chuẩn `hoc_lieu/r1_g05/index.pdf`, từ QMD hiện hành qua `zo_pdf.py build --variant full`. Chỉ đăng ký và sinh biến thể `full` trong lượt này. Chưa sinh PDF theo chức năng, chưa thêm mục tải vào HTML, chưa commit, push hoặc xuất bản. PDF, bìa và dàn trang bản in đang chờ chủ trì duyệt.

## Tiếp nhận duyệt và nguồn

Biên nhận `duyet_sua_html_va_giao_pdf_20261021.json` giữ đúng lời chủ trì duyệt phần sửa nguồn/căn giữa công thức và đã đọc HTML không có góp ý thêm, cùng hash HTML được xem. Không suy thành nghiệm thu PDF hoặc toàn gói. Nguồn chính văn vẫn là `index.qmd`; bản thảo giữ nguyên. Chỉ thêm filter PDF vào metadata, không đổi chính văn, nhiệm vụ, lời giải hoặc biểu thức toán. Bộ 567 biểu thức của nội dung gói và 9 biểu thức Nhật kí chung được bảo toàn qua phép chiếu có đối chiếu trước–sau.

## Cách dựng và tài nguyên

Dùng `course-print-v2`: A4, thân STIX Two Text 11 pt, toán STIX Two Math, tiêu đề/nhãn Be Vietnam Pro, khung bìa–kết và footer chung. Bài học được phép nối tiếp phần kết Bắt đầu để tránh trang gần rỗng; các khu vực khác mở trang theo cấu hình in của gói. Đây là tổ chức bản in, không đổi trình tự nội dung hoặc HTML.

Các hình bối cảnh dùng vector từ nguồn chính thức. Bốn hình thân bài được chuyển trực tiếp từ SVG bằng Inkscape, giữ nhãn gốc 10 pt, khác profile nhãn đồ thị 11 pt; không thu toàn bộ hình xuống quá nhỏ để vừa trang. Riêng hình cắt–gấp được bố trí hai phần theo chiều dọc bằng `_quy_trinh/sinh_hinh_in.py`, gọi lại cùng hình học, dữ liệu và nhãn trong `sinh_hinh.py`; giữ kiểm sáu đường đo, không dựng lại hoặc sửa SVG/PNG web. Dữ liệu hình, bảng và ảnh bìa vẫn ở vị trí chuẩn của gói. `giao_dien/print_assets.json` khóa SVG nguồn, PDF vector, mã chuyển và bố trí in; cổng kiểm đối chiếu luồng vector thật đã nhúng, tỉ lệ, tâm và biên trang.

Cơ chế chuyển SVG và kiểm nguồn có thể dùng lại; hook bố trí in riêng dùng lại cho hình có cùng cấu trúc, chưa là bộ dàn mọi minh họa thực tế. Không tạo JSON bảng biến thiên trống: gói bối cảnh đã khai báo được phép không có bảng biến thiên; nếu nguồn có bảng native mà thiếu dữ liệu thì cổng vẫn chặn. Cổng biến thể nay cho phép đăng ký đúng một bản toàn văn trước, vẫn bắt buộc có `full` và kiểm đủ mọi tệp đã đăng ký, tên/đích an toàn, không trùng đầu ra và hash đúng.

## Kiểm và rà sản phẩm

- Đạt 20/20 kiểm PDF và 22/22 hợp đồng bố cục; provenance `CURRENT`. Font nhúng, đủ vùng học tập, footer website căn giữa, không ký tự thay thế, không heading bị bỏ cuối trang, không cắt chữ/tràn ngang.
- Đủ năm hình thân bài dạng vector và năm chú thích, đúng tỉ lệ nhãn đã khai báo, ở trong trang và căn giữa; không thay hình bằng ảnh chụp.
- 159 tham chiếu trang đúng đích in; 29 lời giải có đích riêng và neo nhiệm vụ đến đúng trang tiêu đề. Bảng dùng cùng profile chức năng, lặp header khi tiếp trang. Mục lục in và bookmark từ cây QMD.
- Bảy chú thích nguồn giữ câu đầy đủ, cỡ nhỏ khoảng 9,96 pt và màu xám. Công thức riêng dòng căn giữa. Hồi quy mới có fixture Pandoc thật chặn mất kiểu nguồn, cùng các ca không có bảng biến thiên/thiếu dữ liệu, mất caption và điều kiện registry toàn văn; 31 ca bộ in, 5 ca cô lập/biến thể đạt.
- Đã xem toàn bộ 38 trang màu và 38 trang thang xám qua bộ ảnh trang: bìa/mục lục, mọi khu vực, hình, bảng tiếp trang, Nhật kí, đủ lời giải, Nguồn và trang kết. Bản giao sau khi khép registry/định dạng dòng được render lại; đủ 76 ảnh trang khớp từng pixel với bản đã rà. Có ảnh phóng rõ trang hình và bảng nhiều chữ.
- HTML hiện hành giữ đúng byte trước nhiệm vụ, kiểm bảo toàn HTML đạt 1900/1900. Sáu HTML và 33 PDF đã phát hành giữ nguyên; không cập nhật hoặc gia hạn provenance lịch sử của các PDF cũ. Vùng staged của Git không đổi.

Trong lượt dựng, đã giữ lại lỗi khai báo thiếu nguồn nền trong mirror, cổng trạng thái khi registry còn khai báo bản chưa được giao, bản dàn đầu và lần sửa trình bày; không sửa báo cáo FAIL thành PASS. Các lỗi được sửa ở nguồn/cấu hình rồi dựng lại. PDF cuối không sửa tay và không sửa hash để che lệch nguồn.

## Bằng chứng và giới hạn

Hồ sơ máy đọc có trong JSON cùng tên; `_audit/g05_pdf_full_20261021/` giữ baseline, các log dựng, báo cáo kiểm, ảnh và `visual_review.json`. Nguồn, vector và PDF chuẩn ở chính gói, không có nguồn hoặc thành phẩm duy nhất trong audit.

Đây là kiểm kỹ thuật và tự rà thị giác, chưa thay chủ trì duyệt bản in hoặc kiểm toán toán độc lập. Chưa in thử trên giấy hoặc quét QR bằng thiết bị vật lý. URL G05 trên bìa là đích phát hành tương lai, chưa được xuất bản trong lượt này. Cảnh báo biên dịch về tệp ngắt từ tiếng Việt được giữ trong log; rà trang không thấy tràn chữ do cảnh báo này.

Bước tiếp theo: chủ trì xem và duyệt hoặc góp ý PDF toàn văn. Chỉ sau duyệt dàn trang mới đăng ký/sinh các PDF theo chức năng, nối mục tải HTML và kiểm bộ hoàn chỉnh theo đề xuất đã được chấp thuận. Commit và phát hành cần giao riêng.
