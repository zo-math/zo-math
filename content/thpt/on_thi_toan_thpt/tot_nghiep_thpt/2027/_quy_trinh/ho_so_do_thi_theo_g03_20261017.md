# GRAPH-G03-01 — cập nhật đồ thị theo mẫu G03

Chủ trì chọn G03 làm mẫu ngày 17/10/2026. Đã cập nhật nguồn công cụ, dựng lại và kiểm 52 đồ thị nội dung: G01 có 13, G02 có 4, G04 có 35. Chưa được chủ trì duyệt hình thức của các bản sửa, chưa PDF học liệu, commit/push hoặc xuất bản.

## Bản xem thực tế

- [Điểm xem đối chiếu](http://127.0.0.1:8877/_audit/graph_g03_standard_20261017/index.html).
- [G01](http://127.0.0.1:8877/_audit/graph_g03_standard_20261017/html/content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/index.html?r1-view=toan-van); [G02](http://127.0.0.1:8877/_audit/graph_g03_standard_20261017/html/content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g02/index.html?r1-view=toan-van); [G04](http://127.0.0.1:8877/_audit/graph_g03_standard_20261017/html/content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g04/index.html?r1-view=toan-van).
- Toàn bộ HTML/runtime và chín bảng ảnh của 52 hình lưu tại `_audit/graph_g03_standard_20261017/` trong repo; bản xem không là nguồn dựng production.

## Quy tắc và nguồn chính thức

07/6.1.2 sở hữu quy tắc. Công cụ độc lập `E:/zo_math_graphics/graph/profiles/lesson-g03.json` giữ một cấu hình: mỗi ô vẽ 11 × 7 cm; ngoại lệ cao 8 cm phải ghi lí do. Bộ dựng nhận `--style 0.4 --surface paper --layout lesson-g03 --check`. Hình ghép giữ bố trí từng ô. Phông, nét, màu, biểu thức, cửa sổ trục, miền lấy mẫu, vạch, nhãn và điểm giữ nguyên. G04 không còn ép các cửa sổ khác nhau vào khung có kích thước biến đổi theo đơn vị tọa độ; các giới hạn trục vẫn giữ nguyên.

`scripts/zo_graphics.py` đặt cỡ bằng viewBox_width / 16.5 em, CSS hình chung dùng đúng biến này. G01/G02/G04 gọi cùng helper; cổng HTML chung kiểm từng hình thay vì chỉ kiểm số profile. Nút mục lục hiện hành được giữ. Binding G01 đã cập nhật đúng tài nguyên hình và nối shell hiện hành của lượt DRAWER-ICON01; không sửa receipt nghiệm thu cũ.

## Bằng chứng

- Tái dựng hai hình G03 (khung thường và cao) cho SVG đúng từng byte bản đối chứng.
- Nguồn QMD ba gói qua CLI đạt; riêng cổng nguồn tài nguyên G04 360/360.
- HTML G04 1512/1512; hồi quy tài nguyên 28/28; công cụ đồ thị qua toàn bộ bộ kiểm, gồm chặn áp khung nội dung lên bìa.
- Trình duyệt 99/99 ở 1440/430/390 px: đo mọi hình, tỉ lệ, cuộn cục bộ, không méo/tràn trang; thử CSS width:auto và 100% bị bắt; kiểm nút mục lục. G03 đo đủ 11 hình nhưng chỉ 6 hình có wrapper đúng là mẫu hiển thị, 5 ngoại lệ được ghi riêng.
- Bảo toàn 181/181: nội dung học, công thức, tiêu đề, ID, bảng, alt; 1615 tệp bảo vệ không đổi. G01/G02 chỉ đổi câu trạng thái tải PDF thành chờ cập nhật, đúng thực tế hình HTML đã đổi. Đã xem đủ 52 hình qua chín bảng ảnh và các ảnh chụp HTML.
- `git -c core.whitespace=cr-at-eol diff --check` đạt. Lệnh diff mặc định coi CRLF là khoảng trắng thừa; không đổi hàng loạt tệp để chữa cảnh báo này.

## Giới hạn G03 đã phát hiện

Năm ảnh `l09_doc_hinh`, `k02_doc_hinh`, `s_l05_doc_hinh`, `s_k04_doc_hinh`, `s_o03_doc_hinh` không nằm trong figure; CSS cũ của G03 vì thế co giãn theo cách khác. Giữ nguyên G03 theo phạm vi đối chứng, không gọi toàn bộ G03 đã nhất quán và không nhân lỗi wrapper đó vào các bản cập nhật. Báo cáo browser lần đầu giữ riêng để không xóa dấu phát hiện.

## Tệp tác động

- Ngoài repo nội dung: bốn tệp trong `E:/zo_math_graphics` liệt kê tại JSON cùng tên.
- Repo nội dung: bộ nối `zo_graphics.py`, `zo_web_2027_figures.py`, `zo_web_2027_g02_payloads.py`, `zo_course_math_assets.py`, `zo_web_2027_consistency.py`; CSS hình chung và policy math-assets.
- G01/G02: cấu hình hình, SVG/PDF vector từng hình và manifest hiện hành; G01 thêm binding layout hiện hành. Các PDF vector này là cặp tài nguyên đã có của đồ thị, không phải PDF học liệu.
- G04: bộ sinh, TEX/SVG đồ thị, manifest và báo cáo/bảng ảnh khung G03 riêng. Giữ các báo cáo/bảng ảnh lượt trước đúng mốc cũ.
- Điều hành 02/03/04/07/08, registry, AGENTS chuyên mục, README/hợp đồng/kiểm kit, mẫu bản thảo/bảng kiểm và con trỏ hồ sơ ba gói đồng bộ. Các nguồn QMD, JSON toán/BBT, bản thảo, ảnh bìa, G03, docs/PDF công khai giữ nguyên.

JSON cùng tên lưu trạng thái, URL, kiểm chứng và các lỗi ban đầu đã xử lý. Bản sao build và profile trình duyệt tạm được dọn sau bàn giao; giữ HTML, ảnh đối chiếu, log và bằng chứng cần chủ trì xem.
